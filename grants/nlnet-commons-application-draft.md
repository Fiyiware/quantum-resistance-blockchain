# NLNet NGI Zero Commons Fund — application draft

> **Status**: draft v0.3 — work in progress. NGI Assure closed its final call in 2023; this application now targets the **NGI Zero Commons Fund**, which runs rolling calls roughly every two months (the call that closed on 1 June 2026 was just missed; next expected call ~1 August 2026 — confirm the exact date before submitting).
>
> **Target program**: NGI Zero Commons Fund — https://nlnet.nl/commonsfund/ (grant range €5,000–€50,000; requires a clear European Dimension)
>
> **Project**: QRB — Quantum-Resistance Blockchain
>
> **Applicant**: Luiggi Leonel Cedeño Bermeo (natural person / persona física)
>
> **Correspondence email**: qrb.grants@proton.me
>
> **Maintainer of the draft**: Fiyiware (Luiggi Leonel Cedeño Bermeo)
>
> **Last update**: 11 June 2026

This document mirrors the typical sections of the NLNet submission form. Final wording and order will be adjusted to match the exact fields when copying into the online form at https://nlnet.nl/propose/.

---

## 1. Project name

**QRB — Quantum-Resistance Blockchain**

## 2. Project website

https://github.com/Fiyiware/quantum-resistance-blockchain

## 3. Abstract / one-paragraph summary (≤ ~1200 characters)

QRB is an open-source research and prototype track for a post-quantum Layer 2 blockchain compatible with Ethereum. It addresses two distinct quantum threats to existing crypto infrastructure: (1) signature forgery via Shor's algorithm on ECDSA, which puts millions of BTC (estimates of the immediately-exploitable subset vary) and the entire Ethereum state with exposed public keys at risk of impersonation; and (2) "harvest now, decrypt later" — the structural failure of today's privacy chains (Aleo, Aztec) whose SNARK-based proofs are themselves quantum-vulnerable. QRB's roadmap covers both: post-quantum authentication via NIST FIPS 204 ML-DSA-65, already implemented in the Phase 0 prototype; and a post-quantum confidentiality layer based on STARKs (hash-based, natively post-quantum) and lattice commitments, in Phase 3+ research. Fully EVM-compatible, with Account Abstraction PQ-native to absorb the larger signature footprint at the UX layer. NLNet funding would underwrite a focused Phase 1 core: an EVM client fork with an ML-DSA precompile (MLDSAVERIFY), a PQ-native ERC-4337 smart account, a public devnet, and a JavaScript SDK with a reference PQ wallet — with an Ethereum-Sepolia bridge framed as a stretch goal rather than a payment-gated commitment.

## 4. Have you been involved with the NGI initiative before?

No (first application).

## 5. Funding requested

**€50,000** (top of the NGI Zero Commons Fund range of €5,000–€50,000).

Milestone-based release with explicit deliverables tied to each tranche — see §11 below.

## 6. Project description (extended)

### 6.1 The problem

Every elliptic-curve signature in production today (ECDSA on secp256k1, EdDSA on Ed25519) is breakable in polynomial time by a sufficiently large quantum computer running Shor's algorithm. The center of gravity of expert estimates for the arrival of a Cryptographically Relevant Quantum Computer (CRQC) has contracted dramatically: from "2040 or later" in 2019 to the "2028–2032" range in early 2026. The exact arrival date remains genuinely uncertain — but the direction of travel is not.

Key public signals from the past 12 months:

- **NIST FIPS 203/204/205** finalised in August 2024, providing standardised post-quantum primitives (ML-KEM, ML-DSA, SLH-DSA) ready for production deployment; **FIPS 206** (FN-DSA / FALCON) remains in draft, expected late 2026–2027.
- **Google Quantum AI** (March 2026 paper): breaking 256-bit ECC now estimated at <500,000 physical qubits, down from 20 million in 2019.
- **Caltech + Oratomic** (March 2026): plausible path with as few as ~10,000–20,000 qubits using atomic-architecture systems. Current commercial quantum computers already operate 1,000–2,000 qubits.
- **Project Eleven Q-Day Prize** (April 2026): independent researcher Giancarlo Lelli broke a real 15-bit ECC key on a publicly accessible quantum computer, demonstrating a 512× capability jump in seven months.
- **Google internal migration deadline** moved to 2029, six years ahead of the NIST 2035 baseline.
- **Vitalik Buterin** (Devconnect 2025, Buenos Aires, citing Scott Aaronson): warned that a serious quantum threat could arrive around 2028, requiring crypto to complete its post-quantum migration before then.
- **Jefferies**: 10% reduction in Bitcoin allocation in model portfolios (January 2026), citing quantum risk explicitly.
- **MITRE / Post-Quantum Cryptography Coalition**: the *PQC Migration Roadmap* (May 2025) frames migration as a four-stage, multi-year organizational effort — reinforcing how slow and hard it is to migrate existing systems, and why a PQ-native chain (which has nothing to migrate) closes the gap faster.

Regulatory pressure tracks the same trajectory: NIS2 (EU; directive in force since January 2023, national-transposition deadline October 2024) establishes risk-management duties under which post-quantum resistance fits as a forward-looking duty-of-care criterion for critical infrastructure; MiCA (in force December 2024) governs future token issuance in this space.

The threats divide cleanly into two classes:

| Threat | What breaks | Existing remediation |
|--------|-------------|----------------------|
| **A — Impersonation**: Shor on ECDSA signatures | Funds, identity, contract calls | Migrate signatures to PQ (work-in-progress on Ethereum, no production solution) |
| **B — Retroactive decryption** ("harvest now, decrypt later") | All historical blockchain content and encrypted-channel transcripts | Almost nobody addresses this — privacy chains use SNARKs that are themselves quantum-vulnerable |

### 6.2 QRB's approach

QRB proposes a Layer 2 blockchain on Ethereum that addresses both threats coherently:

- **Threat A — Post-quantum authentication**. All signatures use **ML-DSA-65** (NIST FIPS 204, derived from CRYSTALS-Dilithium). FALCON (FN-DSA, FIPS 206) available opt-in for compact signatures; SPHINCS+ (SLH-DSA, FIPS 205) reserved as conservative fallback. Hybrid ECDSA+ML-DSA mode supported during the migration window.

- **Threat B — Post-quantum confidentiality**. A confidentiality layer (Phase 3+ research) using:
  - Stealth addresses (one-time addresses per receipt, à la EIP-5564 adapted to PQ).
  - Confidential transactions with lattice-based commitments.
  - **ZK proofs on STARKs** — critically, *not* SNARKs. STARKs depend only on hash collision resistance and are therefore natively post-quantum; SNARKs depend on elliptic-curve assumptions and break under Shor.
  - View keys for selective disclosure (MiCA / AML compliance).

- **Ethereum compatibility**. EVM execution layer with `MLDSAVERIFY` precompile alongside the legacy `ECRECOVER`; standard Solidity contracts compile without modification.

- **Account Abstraction** (ERC-4337-like, PQ-native from day one): contractual wallets verify their own signatures, supporting key rotation, social recovery, paymasters and multisig PQ — and absorbing the larger PQ signature footprint at the application layer.

- **Settlement on Ethereum L1** via an optimistic rollup bridge initially (Phase 1–2), with migration path to ZK-rollup on STARKs once provers for Dilithium become efficient.

### 6.3 What is already implemented (Phase 0)

The Phase 0 deliverables are public and verifiable on the project repository, with CI on GitHub Actions running the test suite across Python 3.10/3.11/3.12:

- ML-DSA-65 signature primitives via `dilithium-py` (`prototype/qrb/crypto.py`).
- Account-based blockchain with signed blocks and transactions (`prototype/qrb/block.py`, `transaction.py`, `chain.py`).
- World state with balances and nonces (`prototype/qrb/state.py`).
- Persistence in JSON for transparent inspection (`prototype/qrb/storage.py`).
- CLI with create/list/balance/send/mine/show commands (`prototype/qrb_cli.py`).
- End-to-end tests covering signature verification, tampering rejection, double-spend rejection, proposer impersonation rejection (`prototype/tests/test_basic.py`).
- **Rust proof-of-concept of the `MLDSAVERIFY` precompile core** (`poc/ml-dsa-precompile/`): ML-DSA-65 verification in Rust (via the `fips204` crate), rejecting tampered signatures/messages, with real sizes (1,952 / 4,032 / 3,309 bytes) and a verification benchmark (~200 µs/verify) — the direct starting point and gas-model input for Phase 1 deliverable 1.
- **Second Rust PoC binding that core to the real EVM precompile interface** (`poc/evm-precompile/`): the verifier is wrapped as a `revm` 41 `Precompile` (the EVM engine Reth uses), with real input/output ABI, linear gas accounting and a fixed address, and is exercised through revm's own `Precompile::execute` dispatch — the exact entry point used when EVM bytecode calls a precompile. This de-risks Phase 1 deliverable 1: registering this precompile into a Reth fork behind JSON-RPC is the remaining (funded) step, not an open question.
- 24-page whitepaper with full technical and economic specification (`whitepaper/whitepaper-v0.2.pdf`, plus an English version at `whitepaper/whitepaper-v0.2.en.md`).
- Open source under a dual MIT / Apache-2.0 licence.

The Phase 0 prototype is a single-node, local-only blockchain. It is **not yet an L2** — that is the explicit deliverable of Phase 1, which this grant would fund.

### 6.4 What this grant would fund (Phase 1)

The €50,000 NGI Zero Commons Fund grant would underwrite a focused **6-month Phase 1**. The scope is deliberately conservative: four **core deliverables** that are fully fundable and achievable within the budget, plus **stretch goals** pursued only if the core completes ahead of schedule (otherwise proposed as a follow-on Commons Fund application — the fund explicitly supports scaling up proven projects).

**Core deliverables (the firm commitment of this grant):**

1. **ML-DSA verifier as EVM precompile**. Fork of Reth (Rust EVM client) adding precompiles at fixed addresses (`0x100`–`0x103`) for ML-DSA-44, ML-DSA-65, ML-DSA-87 and FN-DSA-512 verification. Gas cost model published with benchmarks.

2. **PQ Smart Account in Solidity**. Reference implementation of an ERC-4337-compatible smart account that validates ML-DSA signatures via the new precompile. Includes paymaster support, key rotation, and social recovery primitives.

3. **Public devnet**. Single-node devnet running the modified Reth fork with the precompiles active, exposed via standard JSON-RPC. Genesis-funded test wallets distributed via faucet. This is the milestone at which the work becomes externally evaluable: anyone can submit a transaction validated by an ML-DSA signature end-to-end.

4. **Developer SDK (JavaScript) + reference PQ wallet**. A JavaScript library for generating PQ wallets, signing transactions, deploying smart accounts and interacting with the devnet via RPC, plus one reference dApp (a browser PQ wallet) demonstrating the full flow.

**Stretch goals (vision; next tranche / follow-on application if the core lands early):**

- **Ethereum-Sepolia bridge prototype** — a minimal optimistic-rollup-style bridge for testnet deposit/withdrawal (7-day challenge window, Optimism convention). This is the hardest, highest-risk component and is intentionally *not* tied to a payment milestone; it is pursued only once the core is solid.
- **Rust SDK** and two further reference dApps (a PQ ERC-20 token and a PQ multisig).

All artefacts published under MIT/Apache-2.0 dual licence.

## 7. Comparison with the state of the art

| Project | Post-quantum signatures | Post-quantum privacy | EVM compatibility | Account Abstraction | Open source |
|---------|:-:|:-:|:-:|:-:|:-:|
| Bitcoin / Ethereum L1 | ❌ (in research) | ❌ | ✅ Ethereum | partial (ERC-4337) | ✅ |
| QRL / Zond | ✅ (XMSS → Dilithium) | ❌ | partial | ❌ | ✅ |
| Quranium | ✅ (Dilithium) | ❌ | partial | ❌ | ✅ |
| Cellframe | ✅ (CRYSTALS, NTRU) | partial | ❌ | ❌ | ✅ |
| Aleo | ❌ (SNARK-based) | ✅ but NOT PQ-safe | ❌ | ❌ | ✅ |
| Aztec | ❌ (SNARK-based) | ✅ but NOT PQ-safe | partial | ✅ | partial |
| Monero | ❌ | ✅ but NOT PQ-safe | ❌ | ❌ | ✅ |
| **QRB (target)** | ✅ ML-DSA-65 (Phase 0) | 🔬 STARKs (Phase 3+) | 📐 Phase 1 | 📐 Phase 1 | ✅ |

No known project pursues all five capabilities simultaneously. The privacy chains in the market (Aleo, Aztec, Monero) provide privacy that is **broken at long horizons** under harvest-now-decrypt-later. We are not aware of another project that has publicly identified this gap and designed its confidentiality layer on STARKs (natively post-quantum) from the ground up.

## 8. Significant technical challenges expected

- **Signature size in gas accounting**. ML-DSA-65 signatures are ≈3,309 bytes vs 64 for ECDSA. The precompile design must price PQ verification correctly without making PQ-only transactions prohibitively expensive. Calibrated benchmarks form part of deliverable 1.

- **Hybrid signature transition**. During the migration window, transactions can be signed with both ECDSA and ML-DSA; both must verify for the transaction to be valid. Smart-account semantics for hybrid mode require careful design to avoid signature-confusion attacks.

- **Bridge safety with PQ signatures by sequencer** (stretch-goal component). The optimistic rollup bridge must use PQ signatures for the sequencer and challenger roles to be coherent with the chain's threat model. Its difficulty is precisely why it is scoped as a stretch goal rather than a core, payment-gated deliverable.

- **Key rotation under PQ**. Stateless verification of frequent key rotations requires either stateful key trees (XMSS-style) or careful contract-account design. We default to ML-DSA (stateless) and address rotation at the AA-contract level.

- **Tooling friction**. Most Ethereum tooling (Hardhat, Foundry, MetaMask) assumes ECDSA. The SDK deliverable explicitly addresses this by exposing identical developer ergonomics with PQ keys underneath.

## 9. Why this project is important for an open internet

The quantum threat to elliptic-curve cryptography is no longer hypothetical. Once a cryptographically relevant quantum computer exists, every public key ever exposed on a public chain — that is, every wallet that has ever sent a transaction — becomes a forgery target. The total at-risk balance on Ethereum and Bitcoin alone exceeds 1 trillion USD at current valuations.

Existing L1s cannot realistically migrate in time. Coordinated migration of Bitcoin's state has been estimated (arXiv:2410.16965) at a minimum 76 days of continuous on-chain activity assuming community consensus from day one — a consensus that Bitcoin's governance has never achieved in less than 18 months. Ethereum's roadmap acknowledges the problem but does not commit to a concrete deadline before 2030. Meanwhile, regulated institutions in the EU (under NIS2's risk-management duties) will increasingly be expected to demonstrate forward-looking cryptographic resilience — post-quantum readiness included — for critical infrastructure.

The result is a clear infrastructure gap that no profit-driven L1 has a structural incentive to close. An open-source, grant-funded, L2 PQ-first project — designed for EVM compatibility so existing Ethereum apps and tooling can migrate without rewriting — is the cleanest path to closing that gap in the available time window. Phase 0 has demonstrated technical feasibility; Phase 1 (this grant) brings it to a public Ethereum-connected testnet.

## 10. Non-technical considerations

- **Regulatory positioning**. QRB explicitly aligns with MiCA. No token will be emitted during Phase 0 or Phase 1; any future token launch will be conducted via a MiCA-notified whitepaper with proper legal counsel. The privacy-layer design (Phase 3+) includes native view keys for selective disclosure, supporting compliance with NIS2 audit and AML/KYC obligations.
- **Token is out of scope of this grant**. All Phase 1 deliverables funded by this grant are released as open source under MIT/Apache-2.0 and have no dependency on any token. Grant funds will not be used for any token-related activity. The token described in the whitepaper (§5) is a long-term Phase 2+ contingency, conditional on a working product and a MiCA-compliant process — it plays no role in the work proposed here. QRB's funding philosophy is explicitly product-first: non-dilutive grants before any token consideration.

- **Open-source governance**. MIT/Apache-2.0 dual licence; all artefacts public; no closed-source dependencies in critical paths. Future Foundation entity (planned for Phase 2) will hold trademarks and grant disbursement authority but not change core protocol unilaterally.

- **AI assistance disclosure**. The current prototype has been built with substantial AI assistance (Anthropic Claude). This is declared openly in the project README. All architectural and strategic decisions are made by the human founder; AI is used for code generation, documentation drafting and editorial review. We believe transparent disclosure of AI tooling is a stronger signal than concealment.

- **Founder honesty**. The project is currently single-founder. The grant period will be used to recruit a small permanent team (Rust dev, cryptographer) under explicit allocations. This risk is declared up front rather than hidden behind an inflated team page.

## 11. Time and money — budget breakdown

The budget funds the **four core deliverables** of §6.4. Stretch goals (bridge, Rust SDK, extra dApps) are explicitly **not** funded by this tranche.

| Workstream | Hours | Rate (€/h) | Subtotal (€) |
|------------|------:|-----------:|-------------:|
| Reth fork + ML-DSA precompiles + gas benchmarks | 280 | 35 | 9,800 |
| PQ Smart Account in Solidity + paymaster + key rotation + social recovery | 240 | 35 | 8,400 |
| Public devnet, RPC, faucet, observability | 140 | 30 | 4,200 |
| Developer SDK (JS) + reference PQ wallet dApp | 160 | 30 | 4,800 |
| External security review (PQ precompile + smart account) | — | — | 9,000 |
| Documentation, dev examples, public update posts | 120 | 25 | 3,000 |
| Founder coordination, governance, dissemination | 200 | 25 | 5,000 |
| Contingency / buffer for integration and review fixes | — | — | 5,200 |
| Cloud, domains, registry fees, misc | — | — | 600 |
| **Total** | **1,140** | — | **€50,000** |

Hourly rates reflect Spanish independent contractor norms for blockchain engineering work and are below market for Western-European salaried equivalents. Founder time is priced at a non-distorting rate consistent with grant-funded research. The explicit contingency line reflects honest estimation: integration and post-review fixes routinely consume more time than first planned.

Milestone release proposal (each tranche gated on an achievable core deliverable, not on the highest-risk work):

- **30% on signed agreement** — Reth fork branch and Solidity smart-account scaffold public.
- **30% on devnet live** — modified Reth running publicly with PQ precompiles active, faucet operational.
- **30% on PQ smart account end-to-end** — a transaction validated by an ML-DSA signature through the precompile, executed on the public devnet and documented in the repository.
- **10% on final report + SDK + reference wallet** — JS SDK published to npm and the reference PQ wallet dApp live.

## 12. Team and track record

**Founder — Luiggi Leonel Cedeño Bermeo** (GitHub: https://github.com/Fiyiware): coordinator of the QRB project, with primary responsibilities for product vision, technical specification, documentation, and external relations. Background in digital product and web development. First blockchain project under personal authorship; the working Phase 0 prototype (ML-DSA-65 signatures, full test suite, public CI) is direct evidence of delivery capability.

The team is currently single-founder by design at Phase 0. The grant period will be used to onboard:

- **Senior Rust / Go developer** with blockchain-client experience (Geth, Reth, Erigon) — primary contributor on the Reth fork and bridge components.
- **Cryptographer or advanced PhD student** with lattice / Dilithium / STARK expertise — review of the precompile implementation and design of the Phase 3 confidentiality layer foundations.

External peer review of the Phase 0 artefacts led directly to a security fix in the block proposer validation and to the addition of full CI; a subsequent manual QA pass found and fixed a recipient-address validation bug (with a regression test). The cycle of public peer review is documented in `marketing/reviewer-response.md` in the repository.

## 13. Standards and protocols used

- **NIST FIPS 203** (ML-KEM / Kyber) — key encapsulation.
- **NIST FIPS 204** (ML-DSA / Dilithium) — signatures, primary.
- **NIST FIPS 205** (SLH-DSA / SPHINCS+) — conservative fallback signature scheme.
- **NIST FIPS 206** (FN-DSA / FALCON) — compact signatures, opt-in (draft, expected late 2026–2027).
- **ERC-4337** — Account Abstraction.
- **EIP-1559** — fee market.
- **EIP-4844** — blob transactions (for Phase 2 data availability).
- **Ethereum yellow paper** — EVM compatibility.
- **OP Stack** — initial rollup architecture reference.
- **EIP-5564** — stealth addresses (adapted to PQ in Phase 3+).

## 14. Risks and mitigations (additional)

| Risk | Probability | Mitigation |
|------|:-----------:|------------|
| Cryptanalytic break of ML-DSA before mainnet | Low | Modular signature design enables hot-swap to SLH-DSA in <30 days; pre-existing plan documented |
| Ethereum L1 migrates to PQ faster than expected | Medium | QRB pivots to specialisation (confidential PQ, QKD institutional bridge) — capability the L1 will not absorb |
| Single founder bottleneck during Phase 1 | Medium-high | Grant is structured to fund team onboarding as primary first milestone; founder commits to fulltime for grant period |
| Security regression in precompile or smart account | Medium | Dedicated external security review tranche (€9,000) reserved for the PQ precompile + smart account; bug bounty programme set up before public testnet exposure. The bridge is a stretch goal and would carry its own review before any deployment |
| Regulatory turbulence (MiCA secondary acts) | Medium | Conservative governance; no token issuance during Phase 1; legal advice retained for Phase 2 token-issuance preparations |

## 15. Public communication and dissemination

The project commits to:

- All deliverables under MIT/Apache-2.0 in the public GitHub repository.
- Quarterly public progress reports on the project website and X (`@QRB_PQ`).
- Reproducible CI on GitHub Actions, with test pass status visible from the repository's main page.
- Two public technical write-ups during the grant period: one on the ML-DSA precompile gas accounting, one on the bridge design.
- Open issues for community contributions; documented contribution guide.

## 16. Why NLNet specifically?

The NGI Zero Commons Fund's mission — funding research and development of free and open-source technology for the public good of the open internet — aligns 1:1 with QRB's Phase 1 deliverables, which are post-quantum cryptographic infrastructure released entirely under MIT/Apache-2.0. Compared to industry funding sources, NLNet allows the project to:

- Maintain MIT/Apache-2.0 licensing without dilution pressure from venture capital.
- Prioritise long-term security and standards alignment over short-term token-launch incentives.
- Build a public-good infrastructure layer rather than a proprietary product.

**Reusable commons beyond QRB** (literally the point of this fund): the Phase 1 deliverables are not QRB-specific. The `MLDSAVERIFY` precompile is useful to *any* EVM chain or Reth-based client; a PQ-native ERC-4337 smart account is useful to Ethereum itself. We commit to upstreaming this work as public goods — proposing the precompile as an **EIP and/or a PR to the Reth project**, and coordinating with the **Ethereum Foundation's own post-quantum efforts** — so the output is shared infrastructure, not a walled garden. Even if QRB-the-L2 never reaches mainnet, a working, audited ML-DSA precompile and PQ smart account are durable commons.

**European Dimension** (a hard eligibility criterion for the Commons Fund): the project is led from Spain (EU) by a natural person registered there; it targets compliance with EU regulation specifically (MiCA for any future token, NIS2 duty-of-care for critical infrastructure); and it builds on European open-source and research ecosystems (Ethereum, StarkWare, the EU's own QKD deployments). The infrastructure gap it closes is one that European regulated institutions will be required to address before 2030.

The grant would be transformative for QRB's transition from credible Phase 0 prototype to public Ethereum-connected testnet, the milestone at which the project becomes evaluable by the wider ecosystem.

---

## Appendix A — Submission checklist (internal use)

Before clicking "Submit" at https://nlnet.nl/propose/:

- [ ] Verify the next NGI Zero Commons Fund call is open and confirm its exact deadline at https://nlnet.nl/commonsfund/ (calls run roughly every two months; the 1 June 2026 call has closed, next expected ~1 August 2026).
- [x] Confirm bank account in name of natural person or registered entity. **Decided: natural person (persona física), Luiggi Leonel Cedeño Bermeo.** No Estonia OÜ / SL for now — revisit only once recurring revenue exists.
- [x] Confirm NIF details for invoicing as persona física. **Decided: invoicing as a foreign natural person in Spain using the NIE as NIF.** (The actual NIE number is kept private and entered directly into the NLNet form — never committed to this public repository.)
- [ ] Confirm address details for legal correspondence.
- [ ] Cross-check the final wording against the actual form field names (some fields have character limits).
- [ ] Attach: link to GitHub repo, link to the **English** whitepaper (`whitepaper/whitepaper-v0.2.en.md`), link to CI badge.
- [x] Designate a primary correspondence email. **Decided: qrb.grants@proton.me** (dedicated, free).
- [ ] Save a copy of the final submitted version under `grants/nlnet-commons-submitted-YYYY-MM-DD.md`.
- [ ] Diarise the expected decision window (NLNet typically responds within 8–12 weeks).

## Appendix B — Founder decisions (resolved 31 May 2026)

The six previously-open items have been decided by the founder:

- **Founder identity**: ✅ Real name — **Luiggi Leonel Cedeño Bermeo**.
- **Fiscal vehicle**: ✅ **Persona física** (natural person). Estonia OÜ / SL deferred until recurring revenue justifies the ~€1,000/yr overhead.
- **Hourly rates**: ✅ **35 €/h** as the reference rate (some lines at 30/25 €/h for non-engineering work, per the budget table). Defensible against Spanish freelance norms without appearing inflated.
- **External security review supplier**: ✅ **Least Authority** as the named candidate for the €9,000 line (best fit for ticket size and PQ-primitive scope). Paid from the grant, not founder funds.
- **Reference dApps**: ✅ **PQ wallet + PQ ERC-20 token + PQ multi-sig.**
- **Correspondence email**: ✅ **qrb.grants@proton.me** (dedicated).

Still to do before pressing Submit (not founder-blocking):

- Verify the next NGI Zero Commons Fund call is open for the target round before submitting.
- Plan to accompany the application with a Reth-fork PoC (reason the deadline was moved to 1 August).
- Lock in the quarterly public communication cadence as a real commitment, not aspirational.
