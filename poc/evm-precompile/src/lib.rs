//! QRB PoC — ML-DSA-65 (NIST FIPS 204) verification as a **revm/Reth precompile**.
//!
//! The sibling PoC (`poc/ml-dsa-precompile/`) proved the *cryptographic* core:
//! ML-DSA-65 verification works, rejects tampering, and is fast. This crate takes
//! the next honest step toward Phase 1 deliverable 1: it wraps that operation in
//! the **exact precompile interface of `revm` 41** (the EVM engine Reth uses), so
//! the verifier is type-checked against, and registrable into, a real EVM client.
//!
//! What this IS:
//!   * A `revm_precompile::Precompile` (the `MLDSAVERIFY` precompile) registered at
//!     a fixed address, callable through revm's own `Precompile::execute` dispatch
//!     — i.e. invoked exactly as the EVM would invoke it.
//!   * Real input/output ABI, real linear gas accounting, real error semantics.
//!
//! What this is NOT (yet — this is the funded Phase 1 work):
//!   * A full Reth fork running a devnet. Wiring this `Precompile` into a live
//!     client's precompile set + a public JSON-RPC devnet is Phase 1 deliverable 1.
//!     See the README for the exact one-call integration point.
//!
//! Honest status: Phase 0 PoC. The gas constants below are PLACEHOLDERS to be
//! calibrated from the criterion benchmarks (Phase 1 deliverable 1).

use std::borrow::Cow;

use fips204::ml_dsa_65::{PublicKey, PK_LEN, SIG_LEN};
use fips204::traits::{SerDes, Verifier};
use revm_precompile::primitives::Bytes;
use revm_precompile::{
    calc_linear_cost, eth_precompile_fn, u64_to_address, EthPrecompileOutput, EthPrecompileResult,
    Precompile, PrecompileHalt, PrecompileId,
};

/// Fixed address for the ML-DSA-65 verification precompile.
///
/// The whitepaper reserves `0x100`–`0x103` for ML-DSA-44/65/87 + FN-DSA-512.
/// `0x101` is the ML-DSA-65 slot. Final assignment is subject to avoiding a
/// collision with any standardised precompile (e.g. RIP-7212 P256VERIFY); it is
/// a single constant to change here and in the Reth fork.
pub const MLDSA65_VERIFY_ADDRESS: u64 = 0x101;

/// Base gas charged for an ML-DSA-65 verification.
///
/// PLACEHOLDER. ecRecover is 3,000 gas; ML-DSA-65 verification is heavier
/// (~200 µs in the sibling benchmark). The real value is an output of the
/// Phase 1 gas-model calibration, not a number to trust from this PoC.
pub const MLDSA65_VERIFY_BASE: u64 = 8_000;

/// Per-32-byte-word gas, covering the cost of moving the large PQ payload
/// (≈5.2 KB: a 1,952-byte key + a 3,309-byte signature + the message).
pub const MLDSA65_VERIFY_PER_WORD: u64 = 3;

eth_precompile_fn!(mldsa65_verify_precompile, mldsa65_verify_run);

/// The registrable precompile value: id `MLDSAVERIFY`, fixed address, verifier fn.
///
/// Drop this into a Reth/revm precompile set to expose ML-DSA-65 verification to
/// EVM bytecode — see the README integration note.
pub const MLDSA65_VERIFY: Precompile = Precompile::new(
    PrecompileId::Custom(Cow::Borrowed("MLDSAVERIFY")),
    u64_to_address(MLDSA65_VERIFY_ADDRESS),
    mldsa65_verify_precompile,
);

/// Input layout (fixed sizes for ML-DSA-65, so no length prefixes are needed):
///
/// ```text
///   [ public key : PK_LEN (1952) ] [ signature : SIG_LEN (3309) ] [ message : rest ]
/// ```
///
/// Output: a 32-byte big-endian word — `0x..01` if the signature is valid,
/// `0x..00` otherwise (the same boolean-word convention Solidity reads as `bool`).
///
/// Malformed input (too short, or a key that fails to deserialise) is treated as
/// a **valid call that returns `false`** — not a fatal EVM error — mirroring how
/// `ecRecover` returns empty rather than reverting. Out-of-gas is the only halt.
pub fn mldsa65_verify_run(input: &[u8], gas_limit: u64) -> EthPrecompileResult {
    let gas_used = calc_linear_cost(input.len(), MLDSA65_VERIFY_BASE, MLDSA65_VERIFY_PER_WORD);
    if gas_used > gas_limit {
        return Err(PrecompileHalt::OutOfGas);
    }
    let valid = verify_encoded(input).unwrap_or(false);
    Ok(EthPrecompileOutput::new(gas_used, bool_word(valid)))
}

/// Parse the fixed-layout input and run the actual ML-DSA-65 verification.
/// Returns `None` on any structural problem (caller maps that to `false`).
fn verify_encoded(input: &[u8]) -> Option<bool> {
    if input.len() < PK_LEN + SIG_LEN {
        return None;
    }
    let (pk_bytes, rest) = input.split_at(PK_LEN);
    let (sig_bytes, message) = rest.split_at(SIG_LEN);

    let pk_arr: [u8; PK_LEN] = pk_bytes.try_into().ok()?;
    let sig_arr: [u8; SIG_LEN] = sig_bytes.try_into().ok()?;

    let pk = PublicKey::try_from_bytes(pk_arr).ok()?;
    // Empty domain-separation context, matching the prototype's signing path.
    Some(pk.verify(message, &sig_arr, b""))
}

/// Encode a boolean as a 32-byte EVM word (`0x..01` / `0x..00`).
fn bool_word(b: bool) -> Bytes {
    let mut out = [0u8; 32];
    out[31] = b as u8;
    Bytes::copy_from_slice(&out)
}

/// Build the precompile input from its parts, for callers/tests.
/// `pk || sig || message`.
pub fn encode_input(pk: &[u8; PK_LEN], sig: &[u8; SIG_LEN], message: &[u8]) -> Vec<u8> {
    let mut v = Vec::with_capacity(PK_LEN + SIG_LEN + message.len());
    v.extend_from_slice(pk);
    v.extend_from_slice(sig);
    v.extend_from_slice(message);
    v
}

#[cfg(test)]
mod tests {
    use super::*;
    use fips204::ml_dsa_65;
    use fips204::traits::Signer;

    const PLENTY_GAS: u64 = 1_000_000;

    fn signed_fixture(message: &[u8]) -> ([u8; PK_LEN], [u8; SIG_LEN]) {
        let (pk, sk) = ml_dsa_65::try_keygen().expect("keygen");
        let sig = sk.try_sign(message, b"").expect("sign");
        (pk.into_bytes(), sig)
    }

    #[test]
    fn valid_signature_returns_true_word() {
        let message = b"QRB tx | to=0x8f5...26e amount=1000 nonce=0";
        let (pk, sig) = signed_fixture(message);
        let input = encode_input(&pk, &sig, message);

        // Call through revm's own Precompile dispatch, exactly as the EVM would.
        let out = MLDSA65_VERIFY
            .execute(&input, PLENTY_GAS, 0)
            .expect("not a fatal error");
        assert!(out.is_success());
        assert_eq!(out.bytes.len(), 32);
        assert_eq!(out.bytes[31], 1, "valid signature must encode true");
        assert!(out.gas_used >= MLDSA65_VERIFY_BASE);
    }

    #[test]
    fn tampered_signature_returns_false_word() {
        let message = b"QRB tx | to=0x8f5...26e amount=1000 nonce=0";
        let (pk, mut sig) = signed_fixture(message);
        sig[0] ^= 0xFF; // flip one byte of the signature
        let input = encode_input(&pk, &sig, message);

        let out = MLDSA65_VERIFY.execute(&input, PLENTY_GAS, 0).unwrap();
        assert_eq!(out.bytes[31], 0, "tampered signature must encode false");
    }

    #[test]
    fn wrong_message_returns_false_word() {
        let message = b"QRB tx | to=0x8f5...26e amount=1000 nonce=0";
        let (pk, sig) = signed_fixture(message);
        let attacker = b"QRB tx | to=0xATTACKER amount=1000 nonce=0";
        let input = encode_input(&pk, &sig, attacker);

        let out = MLDSA65_VERIFY.execute(&input, PLENTY_GAS, 0).unwrap();
        assert_eq!(out.bytes[31], 0, "signature over a different message must fail");
    }

    #[test]
    fn malformed_short_input_returns_false_not_fatal() {
        let input = vec![0u8; PK_LEN]; // missing the signature and message
        let out = MLDSA65_VERIFY.execute(&input, PLENTY_GAS, 0).unwrap();
        assert_eq!(out.bytes[31], 0, "too-short input must verify as false");
    }

    #[test]
    fn out_of_gas_halts() {
        let input = vec![0u8; PK_LEN + SIG_LEN];
        // gas_limit below the base cost must halt, not return a word.
        let err = MLDSA65_VERIFY.execute(&input, 1, 0);
        // Execute wraps the halt into a (non-fatal) halted output.
        let out = err.expect("halt is non-fatal at the provider boundary");
        assert!(out.is_halt(), "insufficient gas must halt the precompile");
    }

    #[test]
    fn registration_metadata_is_correct() {
        assert_eq!(MLDSA65_VERIFY.id().name(), "MLDSAVERIFY");
        assert_eq!(
            *MLDSA65_VERIFY.address(),
            u64_to_address(MLDSA65_VERIFY_ADDRESS)
        );
    }
}
