# Security Policy

## Project status — read this first

QRB is an **early, Phase 0 research prototype**. The Python implementation under
`prototype/` and the Rust proofs-of-concept under `poc/` exist to demonstrate that
post-quantum signatures (ML-DSA-65, NIST FIPS 204) can work end-to-end in a blockchain
and EVM context. They are **not production software**:

- wallets are stored as **unencrypted JSON**;
- the prototype is **single-node and local** (no networking, no consensus hardening);
- the cryptography relies on **reference implementations** (`dilithium-py`, `fips204`),
  not production-hardened, side-channel-resistant libraries;
- gas constants in the EVM precompile PoC are **placeholders**.

**Do not use any of this code to protect real funds or real secrets.**

## Reporting a vulnerability

We still want to hear about security issues — especially anything that contradicts a
claim made in the README or whitepaper.

- **Email:** `qrb.grants@proton.me` with the subject line starting `SECURITY:`.
- **Please do not** open a public GitHub issue for a sensitive vulnerability. Use email
  first so we can assess and coordinate disclosure.
- For non-sensitive issues (e.g. a wrong claim, a weak test, a hardening suggestion that
  doesn't expose users), a regular [GitHub issue](https://github.com/Fiyiware/quantum-resistance-blockchain/issues)
  is fine.

### What to include

- A clear description of the issue and why it matters.
- Steps to reproduce, or a proof of concept, if you have one.
- The affected file(s)/component(s) and commit hash.
- Any suggested fix (optional).

### What to expect

This is currently a **single-maintainer project**, so timelines are best-effort, not
contractual:

- **Acknowledgement:** within ~5 days.
- **Initial assessment:** within ~14 days.
- **Coordinated disclosure:** we'll agree a timeline with you before anything is made
  public, and we'll credit you in the fix (unless you prefer to stay anonymous).

## Scope

In scope: the prototype (`prototype/`), the PoCs (`poc/`), and any security-relevant
**claim** in the README, whitepaper, or grant materials.

Out of scope: third-party dependencies themselves (report those upstream), the personal
workflow docs under `docs/`, and theoretical concerns already disclosed as known
limitations above or in the whitepaper.

## A note on the threat model

QRB's entire reason to exist is a long-horizon cryptographic threat (a future
cryptographically-relevant quantum computer). Reports that engage with the *correctness*
of our post-quantum claims are especially welcome — getting that right is the whole point.
