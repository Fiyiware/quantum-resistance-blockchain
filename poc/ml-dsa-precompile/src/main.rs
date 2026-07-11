//! QRB proof-of-concept — ML-DSA-65 (FIPS 204) signature verification.
//!
//! This is the cryptographic core of QRB's planned `MLDSAVERIFY` EVM precompile:
//! given (message, signature, public key), decide if the signature is valid.
//! It demonstrates, in the Rust/Reth ecosystem, that the operation works, that
//! it rejects tampering, the real key/signature sizes, and how fast a single
//! verification is (which feeds the gas-cost model in Phase 1).
//!
//! NOT a full Reth fork — that is the funded Phase 1 deliverable. This is the
//! minimal, honest demonstrator of feasibility.

use fips204::ml_dsa_65::{self, PK_LEN, SIG_LEN, SK_LEN};
use fips204::traits::{SerDes, Signer, Verifier};
use std::time::Instant;

fn main() {
    println!("QRB PoC — ML-DSA-65 (NIST FIPS 204) verification\n");

    // 1. Generate a key pair (the wallet's PQ identity).
    let (pk, sk) = ml_dsa_65::try_keygen().expect("keygen failed");

    // 2. A transaction-like payload, as QRB would sign.
    let message = b"QRB tx | from=0xabc...12d to=0x8f5...26e amount=1000 nonce=0";
    let ctx = b""; // empty domain-separation context

    // 3. Sign it with the secret key.
    let sig = sk.try_sign(message, ctx).expect("sign failed");

    // 4. THE PRECOMPILE OPERATION: verify the signature with the public key.
    let valid = pk.verify(message, &sig, ctx);
    println!("[1] Valid signature verifies        -> {valid}");
    assert!(valid, "a freshly-signed message must verify");

    // 5. Tampering must be rejected (flip one byte of the signature).
    let mut tampered = sig;
    tampered[0] ^= 0xFF;
    let rejected = !pk.verify(message, &tampered, ctx);
    println!("[2] Tampered signature rejected      -> {rejected}");
    assert!(rejected, "a tampered signature must NOT verify");

    // 6. Tampering with the message must also be rejected.
    let other = b"QRB tx | from=0xabc...12d to=0xATTACKER amount=1000 nonce=0";
    let msg_rejected = !pk.verify(other, &sig, ctx);
    println!("[3] Wrong message rejected           -> {msg_rejected}");
    assert!(msg_rejected, "signature must not verify against a different message");

    // 7. Sizes — the price of quantum resistance (compare with ECDSA secp256k1).
    println!("\nSizes (vs classical ECDSA):");
    println!("  public key: {PK_LEN:>5} bytes   (ECDSA: 33)");
    println!("  secret key: {SK_LEN:>5} bytes   (ECDSA: 32)");
    println!("  signature:  {SIG_LEN:>5} bytes   (ECDSA: 64)");
    // sanity-check the round-trip serialisation a precompile would do
    let pk_bytes = pk.clone().into_bytes();
    assert_eq!(pk_bytes.len(), PK_LEN);

    // 8. Quick verification timing (orientation only — the authoritative,
    //    statistically sound numbers come from `cargo bench`, see
    //    benches/mldsa65.rs; the gas model uses those).
    let iters = 2000u32;
    let start = Instant::now();
    let mut acc = 0u64; // keep the optimiser honest
    for _ in 0..iters {
        if pk.verify(message, &sig, ctx) {
            acc += 1;
        }
    }
    let elapsed = start.elapsed();
    assert_eq!(acc, iters as u64);
    let per = elapsed / iters;
    println!("\nVerification benchmark ({iters} iterations):");
    println!("  total:    {elapsed:?}");
    println!("  per call: {per:?}  (~{:.1} us/verify)", per.as_secs_f64() * 1e6);

    println!("\nOK — ML-DSA-65 verification works, rejects tampering, and is fast.");
    println!("This is the operation QRB will expose as the MLDSAVERIFY precompile (Phase 1).");
}
