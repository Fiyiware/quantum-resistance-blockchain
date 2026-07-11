//! Known-Answer Tests (KAT): validate the `fips204` crate against the **official
//! NIST ACVP test vectors** for ML-DSA-65 (FIPS 204).
//!
//! Everything else in this PoC verifies signatures it generated itself. These tests
//! prove interoperability with the standard: NIST-generated valid signatures must
//! verify, NIST-tampered ones (z / hint / commitment / message) must be rejected,
//! and key generation from a NIST seed must reproduce the exact expected key pair.
//!
//! Vector provenance: see `test-vectors/README.md` at the repository root.
//! Addresses issue #32.

use fips204::ml_dsa_65::{PublicKey, KG, PK_LEN, SIG_LEN, SK_LEN};
use fips204::traits::{KeyGen, SerDes, Verifier};

fn hex(s: &str) -> Vec<u8> {
    assert!(s.len() % 2 == 0, "odd-length hex string");
    (0..s.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16).expect("invalid hex"))
        .collect()
}

#[test]
fn acvp_sigver_vectors() {
    let data: serde_json::Value = serde_json::from_str(include_str!(
        "../../../test-vectors/ml-dsa-65/sigver-external-pure.json"
    ))
    .expect("vendored sigVer vectors must parse");
    let tests = data["tests"].as_array().expect("tests array");
    assert_eq!(tests.len(), 15, "vendored subset incomplete");

    for t in tests {
        let tc_id = t["tcId"].as_u64().unwrap();
        let expected = t["testPassed"].as_bool().unwrap();
        let reason = t["reason"].as_str().unwrap();

        let pk_bytes: [u8; PK_LEN] = hex(t["pk"].as_str().unwrap())
            .try_into()
            .expect("pk length");
        let sig: [u8; SIG_LEN] = hex(t["signature"].as_str().unwrap())
            .try_into()
            .expect("signature length");
        let message = hex(t["message"].as_str().unwrap());
        let ctx = hex(t["context"].as_str().unwrap());

        let pk = PublicKey::try_from_bytes(pk_bytes).expect("pk must deserialize");
        let got = pk.verify(&message, &sig, &ctx);
        assert_eq!(
            got, expected,
            "ACVP tc {tc_id} ({reason}): expected {expected}, got {got}"
        );
    }
}

#[test]
fn acvp_keygen_vectors() {
    let data: serde_json::Value = serde_json::from_str(include_str!(
        "../../../test-vectors/ml-dsa-65/keygen.json"
    ))
    .expect("vendored keyGen vectors must parse");
    let tests = data["tests"].as_array().expect("tests array");
    assert!(!tests.is_empty());

    for t in tests {
        let tc_id = t["tcId"].as_u64().unwrap();
        let seed: [u8; 32] = hex(t["seed"].as_str().unwrap())
            .try_into()
            .expect("seed length");
        let expected_pk = hex(t["pk"].as_str().unwrap());
        let expected_sk = hex(t["sk"].as_str().unwrap());
        assert_eq!(expected_pk.len(), PK_LEN);
        assert_eq!(expected_sk.len(), SK_LEN);

        let (pk, sk) = KG::keygen_from_seed(&seed);
        assert_eq!(
            pk.into_bytes().to_vec(),
            expected_pk,
            "ACVP keyGen tc {tc_id}: pk mismatch"
        );
        assert_eq!(
            sk.into_bytes().to_vec(),
            expected_sk,
            "ACVP keyGen tc {tc_id}: sk mismatch"
        );
    }
}
