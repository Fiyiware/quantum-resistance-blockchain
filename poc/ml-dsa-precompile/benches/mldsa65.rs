//! Criterion benchmark for ML-DSA-65 (FIPS 204) — keygen, sign and verify.
//!
//! This replaces the rough single-input `Instant` timing in `main.rs` with a
//! statistically sound benchmark over varied inputs. The **verify** numbers are
//! the input to the gas-cost model of the ML-DSA verification precompile
//! (compare with `ECRECOVER`'s 3,000 gas at ~100-150 µs). Addresses issue #28.
//!
//! Run with: `cargo bench` (results + HTML report under `target/criterion/`).

use criterion::{criterion_group, criterion_main, BenchmarkId, Criterion, Throughput};
use fips204::ml_dsa_65;
use fips204::traits::{Signer, Verifier};

/// Message sizes covering the realistic precompile input range: a 32-byte
/// digest, a typical signed transaction payload, and a large calldata blob.
const MSG_SIZES: [usize; 3] = [32, 512, 4096];

fn deterministic_message(len: usize) -> Vec<u8> {
    (0..len).map(|i| (i * 31 % 251) as u8).collect()
}

fn bench_keygen(c: &mut Criterion) {
    c.bench_function("ml_dsa_65/keygen", |b| {
        b.iter(|| ml_dsa_65::try_keygen().expect("keygen failed"));
    });
}

fn bench_sign(c: &mut Criterion) {
    let (_pk, sk) = ml_dsa_65::try_keygen().expect("keygen failed");
    let mut group = c.benchmark_group("ml_dsa_65/sign");
    for size in MSG_SIZES {
        let message = deterministic_message(size);
        group.throughput(Throughput::Bytes(size as u64));
        group.bench_with_input(BenchmarkId::from_parameter(size), &message, |b, msg| {
            b.iter(|| sk.try_sign(msg, b"").expect("sign failed"));
        });
    }
    group.finish();
}

fn bench_verify(c: &mut Criterion) {
    let mut group = c.benchmark_group("ml_dsa_65/verify");
    for size in MSG_SIZES {
        // A fresh key pair and signature per input size, so no single key or
        // signature shape dominates the measurement.
        let (pk, sk) = ml_dsa_65::try_keygen().expect("keygen failed");
        let message = deterministic_message(size);
        let sig = sk.try_sign(&message, b"").expect("sign failed");
        assert!(pk.verify(&message, &sig, b""));
        group.throughput(Throughput::Bytes(size as u64));
        group.bench_with_input(
            BenchmarkId::from_parameter(size),
            &(pk, message, sig),
            |b, (pk, msg, sig)| {
                b.iter(|| pk.verify(msg, sig, b""));
            },
        );
    }
    group.finish();
}

fn bench_verify_reject(c: &mut Criterion) {
    // Rejection cost matters for the gas model too: a precompile must charge
    // enough that feeding it garbage is not a cheap DoS vector.
    let (pk, sk) = ml_dsa_65::try_keygen().expect("keygen failed");
    let message = deterministic_message(512);
    let mut sig = sk.try_sign(&message, b"").expect("sign failed");
    sig[0] ^= 0xFF;
    assert!(!pk.verify(&message, &sig, b""));
    c.bench_function("ml_dsa_65/verify_reject_tampered", |b| {
        b.iter(|| pk.verify(&message, &sig, b""));
    });
}

criterion_group!(
    benches,
    bench_keygen,
    bench_sign,
    bench_verify,
    bench_verify_reject
);
criterion_main!(benches);
