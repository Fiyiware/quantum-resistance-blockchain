# Official NIST test vectors (vendored subset)

Known-Answer Tests (KAT) used by both the Python prototype and the Rust PoC to check
that the ML-DSA-65 implementations we depend on (`dilithium-py`, `fips204`) actually
interoperate with the **official NIST FIPS 204 standard** — not just with themselves.

## Provenance

Extracted from the NIST **ACVP-Server** repository (the official generator/validator
for NIST's Automated Cryptographic Validation Protocol):

- https://github.com/usnistgov/ACVP-Server/tree/master/gen-val/json-files

| File | Source | Contents |
|------|--------|----------|
| `ml-dsa-65/sigver-external-pure.json` | `ML-DSA-sigVer-FIPS204/internalProjection.json`, vsId 42, testGroup 3 | 15 signature-verification cases (ML-DSA-65, `external` interface, `pure` mode, no external μ): valid signatures plus tampered z / hint / commitment / message cases. Each case: `pk`, `message`, `context`, `signature` (hex) and the expected boolean `testPassed`. The `sk` field was stripped (not needed for verification). |
| `ml-dsa-65/keygen.json` | `ML-DSA-keyGen-FIPS204/internalProjection.json`, vsId 42, testGroup 2 | First 5 key-generation cases: 32-byte `seed` (ξ) → expected `pk`, `sk`. |

Vendored (rather than downloaded in CI) to keep tests hermetic and reviewable. The
subset is deliberately small; re-extraction from the URLs above is straightforward if
more coverage is ever needed.

## Consumed by

- `prototype/tests/test_basic.py` — `test_mldsa65_acvp_sigver_vectors`,
  `test_mldsa65_acvp_keygen_vectors` (checks `dilithium-py`).
- `poc/ml-dsa-precompile/tests/acvp_kat.rs` (checks the `fips204` crate).
