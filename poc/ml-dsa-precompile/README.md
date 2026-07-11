# PoC — ML-DSA-65 verification (the core of the `MLDSAVERIFY` precompile)

A minimal, honest proof-of-concept in **Rust** that demonstrates the cryptographic
operation at the heart of QRB's planned EVM precompile: **verifying an ML-DSA-65
(NIST FIPS 204) signature** — the post-quantum replacement for `ECRECOVER`.

It uses the pure-Rust [`fips204`](https://crates.io/crates/fips204) implementation,
so it runs in the same ecosystem as the Reth client QRB will fork in Phase 1.

## What it proves

- ✅ ML-DSA-65 sign/verify works end-to-end in Rust.
- ✅ Tampered signatures **and** altered messages are rejected.
- ✅ Real sizes match the whitepaper (public key 1,952 B · secret key 4,032 B ·
  signature 3,309 B — vs 33/32/64 for ECDSA).
- ✅ **Interoperability with the standard, not just with itself**: `tests/acvp_kat.rs`
  validates the `fips204` crate against a vendored subset of the **official NIST ACVP
  test vectors** for ML-DSA-65 — 15 sigVer cases (valid + tampered z / hint /
  commitment / message) and 5 keyGen cases (seed ξ → exact expected key pair).
  Provenance: [`test-vectors/README.md`](../../test-vectors/README.md). (Issue #32)
- ✅ **A statistically sound `criterion` benchmark** (`benches/mldsa65.rs`) over varied
  message sizes, replacing the earlier rough single-input timing. (Issue #28)

## Run it

```bash
cd poc/ml-dsa-precompile
cargo run --release    # demo with assertions
cargo test --release   # NIST ACVP Known-Answer Tests
cargo bench            # criterion benchmark (report in target/criterion/)
```

Demo output (abridged):

```
[1] Valid signature verifies        -> true
[2] Tampered signature rejected      -> true
[3] Wrong message rejected           -> true

Sizes (vs classical ECDSA):
  public key:  1952 bytes   (ECDSA: 33)
  secret key:  4032 bytes   (ECDSA: 32)
  signature:   3309 bytes   (ECDSA: 64)
```

## Benchmark results (criterion, x86-64 cloud VM, July 2026)

| Operation | Time (median) |
|-----------|---------------|
| keygen | ~221 µs |
| sign (32 B – 4 KB message) | ~677–723 µs |
| **verify (32 B – 4 KB message)** | **~139–154 µs** |
| verify, tampered signature (rejection) | ~142 µs |

Two observations that feed the gas model:

- **Verification cost is nearly flat in message size** (the lattice operations
  dominate; hashing the message adds little), so a precompile can charge a mostly
  fixed base cost plus a small per-byte term.
- **Rejection costs the same as acceptance** (~142 µs vs ~139 µs) — there is no cheap
  early-exit, so correctly pricing the precompile does not open a
  feed-it-garbage DoS discount.
- For scale: `ECRECOVER` costs 3,000 gas for an operation in the same ~100–150 µs
  range on comparable hardware. ML-DSA-65 verification at ~140 µs suggests a
  **similar order of magnitude of compute gas** — the dominant real cost of PQ
  transactions is the ~5.3 KB of signature+pubkey calldata, not the verification
  itself.

Numbers vary with hardware; re-run `cargo bench` to reproduce on yours.

## Scope (honest)

This is **not** a Reth fork and **not** an EVM precompile yet — that is the funded
**Phase 1** deliverable (see [`grants/nlnet-commons-application-draft.md`](../../grants/nlnet-commons-application-draft.md),
deliverable 1). This PoC is the smallest thing that demonstrates the operation is
feasible, measures its cost, and gives a Phase 1 contributor a concrete starting
point. The next step is to expose this exact verification as a precompile at a
fixed address (e.g. `0x101` for ML-DSA-65) inside a Reth fork.

## License

Dual-licensed under MIT or Apache-2.0, like the rest of the repository.
