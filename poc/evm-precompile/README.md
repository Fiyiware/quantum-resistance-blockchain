# QRB PoC — `MLDSAVERIFY` as a revm/Reth precompile

This crate wraps ML-DSA-65 (NIST FIPS 204) signature verification in the **exact
precompile interface of [`revm`](https://github.com/bluealloy/revm) 41** — the EVM
engine that [Reth](https://github.com/paradigmxyz/reth) executes. It is the second
step of the two PoCs that seed **Phase 1 deliverable 1** (a Reth fork with ML-DSA
precompiles):

| PoC | Question it answers |
|-----|---------------------|
| [`../ml-dsa-precompile/`](../ml-dsa-precompile/) | *Does the ML-DSA-65 operation work, reject tampering, and is it fast?* (the crypto core + benchmark) |
| **this crate** | *Does it fit the real EVM precompile interface, and can it be registered and invoked exactly as the EVM would?* |

## What it is — and what it is not

**It is** a real `revm_precompile::Precompile` value (`MLDSA65_VERIFY`), type-checked
against revm 41, with real input/output ABI, linear gas accounting, and error
semantics. Two layers of tests exercise it:

- **Unit tests** (`src/lib.rs`) call it through revm's own `Precompile::execute`
  dispatch — the entry point the EVM uses when bytecode `CALL`s a precompile address.
- **An end-to-end test** (`tests/end_to_end.rs`) spins up a full `revm` EVM with a
  custom `PrecompileProvider` that registers `MLDSAVERIFY` at `0x101`, then sends a
  **real transaction** calling that address and asserts the returned 32-byte word.
  The verification runs through the *entire* transaction pipeline (validation,
  intrinsic gas, the call frame, precompile dispatch, result construction) — the
  closest thing to running on a node without forking Reth.

**It is not** a running Reth fork or a public devnet. Wiring this `Precompile` into a
shipping client behind JSON-RPC with a faucet is exactly the funded Phase 1 work. But
the custom `PrecompileProvider` in the end-to-end test *is* the integration pattern a
Reth fork uses — so that step is now a known quantity, not a leap of faith.

> Honest note: the gas constants (`MLDSA65_VERIFY_BASE` etc.) are **placeholders**.
> The real numbers are an output of the Phase 1 gas-model calibration driven by the
> criterion benchmark in the sibling PoC — not values to trust from a Phase 0 demo.

## Interface (ABI)

ML-DSA-65 has fixed key/signature sizes, so the input needs no length prefixes:

```
input  = [ public key : 1952 bytes ] [ signature : 3309 bytes ] [ message : rest ]
output = 32-byte word — 0x..01 if valid, 0x..00 otherwise (read by Solidity as bool)
```

- **Address**: `0x0000…0101` (the ML-DSA-65 slot of the whitepaper's `0x100–0x103`
  range; a single constant, subject to final assignment so it never collides with a
  standardised precompile such as RIP-7212 `P256VERIFY`).
- **Malformed input** (too short, or an undeserialisable key) returns `0x..00` — a
  valid call that answers "false", not a fatal revert — mirroring `ecRecover`.
- **Out of gas** is the only halt.

## Run it

```bash
cargo test --release     # 8 tests: 6 unit + 2 full-EVM end-to-end
cargo clippy --all-targets --release
```

The **library** pulls `revm-precompile` with `default-features = false`, so consumers
of this crate need **no C toolchain** (no c-kzg / blst / cmake); only revm's precompile
*types* are used, and the verification itself is the pure-Rust `fips204` crate. The
full `revm` EVM is a **dev-dependency** (also trimmed of the C backends), pulled only
to run the end-to-end test.

## Integration point for the Reth fork (Phase 1)

The end-to-end test already shows the integration: a custom `PrecompileProvider` that
wraps the standard `EthPrecompiles`, claims address `0x101`, and dispatches it to
`MLDSA65_VERIFY`. A Reth fork uses the same pattern.

```rust
use qrb_evm_precompile_poc::MLDSA65_VERIFY;

// MLDSA65_VERIFY.id()      -> PrecompileId::Custom("MLDSAVERIFY")
// MLDSA65_VERIFY.address() -> 0x0000…0101
// MLDSA65_VERIFY.execute(input, gas_limit, reservoir) -> PrecompileResult
//
// In the provider's `run`, when inputs.bytecode_address == 0x101, dispatch to
// MLDSA65_VERIFY.execute(...) — see tests/end_to_end.rs for the working version.
```

What remains for Phase 1 deliverable 1 is wiring this provider into a *shipping* Reth
node and exposing it over JSON-RPC with a faucet — engineering, not an open question.
The EVM-level mechanism is done and verifiable today (`cargo test`).

## Licence

Dual MIT / Apache-2.0, like the rest of QRB.
