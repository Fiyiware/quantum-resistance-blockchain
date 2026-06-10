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
- ✅ A verification benchmark (~200 µs/verify on a laptop) — a rough single-input
  timing that feeds the Phase 1 gas-cost model. A production benchmark would use
  `criterion` with varied inputs; this is deliberately minimal.

## Run it

```bash
cd poc/ml-dsa-precompile
cargo run --release
```

Expected output (abridged):

```
[1] Valid signature verifies        -> true
[2] Tampered signature rejected      -> true
[3] Wrong message rejected           -> true

Sizes (vs classical ECDSA):
  public key:  1952 bytes   (ECDSA: 33)
  secret key:  4032 bytes   (ECDSA: 32)
  signature:   3309 bytes   (ECDSA: 64)

Verification benchmark (2000 iterations):
  per call: ~200 µs/verify
```

## Scope (honest)

This is **not** a Reth fork and **not** an EVM precompile yet — that is the funded
**Phase 1** deliverable (see [`grants/nlnet-commons-application-draft.md`](../../grants/nlnet-commons-application-draft.md),
deliverable 1). This PoC is the smallest thing that demonstrates the operation is
feasible, measures its cost, and gives a Phase 1 contributor a concrete starting
point. The next step is to expose this exact verification as a precompile at a
fixed address (e.g. `0x101` for ML-DSA-65) inside a Reth fork.

## License

Dual-licensed under MIT or Apache-2.0, like the rest of the repository.
