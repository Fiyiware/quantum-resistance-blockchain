# Ethereum Foundation — Ecosystem Support Program (ESP) — application draft

> **Status**: draft v0.2 — adapted from the (now-deferred) NLnet draft after the NGI
> Zero Commons Fund closed (June 2026), then revised to match EF ESP's **actual 2026
> process**: ESP is **not** a free-form inquiry. You apply to address a **specific
> Wishlist or RFP item**, or — if no item matches yet — you use **Office Hours** to
> talk to the team first. EF imposes no European-dimension requirement, which makes it a
> cleaner thematic fit than NLnet for QRB's post-quantum-Ethereum work.
>
> **⚠️ Before submitting, two open actions (see §7 and the appendix):**
> 1. **Find the matching Wishlist/RFP item** (PQ cryptography / cryptographic primitives
>    / account abstraction / client work) and tailor §3–§5 to *that item's* wording —
>    or, if none fits cleanly, **book Office Hours** and lead with the working PoC.
> 2. **Be ready to receive payment on-chain in ETH** (EF default) and to complete
>    identity verification + a formal grant letter.
>
> **Project**: QRB — Quantum-Resistance Blockchain
> **Applicant**: Luiggi Leonel Cedeño Bermeo (natural person), GitHub `Fiyiware`
> **Email**: qrb.grants@proton.me
> **Repo**: https://github.com/Fiyiware/quantum-resistance-blockchain
> **Licence**: MIT / Apache-2.0 (dual)
> **ETH payout address**: TODO — set up a wallet the founder controls for ETH grant payment
> **Last update**: 12 June 2026
>
> ESP: https://esp.ethereum.foundation — browse Wishlist / RFPs / Open Rounds /
> Office Hours. The Academic Grants rounds remain a parallel route for the Phase 3
> cryptography-research component.

---

## 1. What are you working on? (one-paragraph summary)

QRB is an open-source research-and-prototype track building the **post-quantum
cryptographic building blocks Ethereum will need before a cryptographically relevant
quantum computer (CRQC) arrives**, and validating them as a PQ-first Layer 2. Every
ECDSA key ever exposed on a public chain — every account that has sent a transaction —
becomes forgeable once Shor's algorithm is runnable at scale. The central deliverable
is an **`MLDSAVERIFY` EVM precompile** (ML-DSA-65 / NIST FIPS 204 signature verification)
plus a **post-quantum-native ERC-4337 smart account** that uses it. Both are designed to
be **upstreamable to Ethereum itself** — as an EIP and a PR to Reth — not locked to QRB.
A working Phase 0 prototype already exists, including two Rust PoCs that run the
precompile inside a real `revm` EVM end-to-end.

## 2. Why does this matter to Ethereum? (the public good)

This is the crux for EF, so it leads:

- **Ethereum needs a post-quantum migration path, and the primitives are not yet in the
  client stack.** NIST finalised ML-DSA (FIPS 204), ML-KEM (203) and SLH-DSA (205) in
  August 2024. What is missing for Ethereum is the *plumbing*: an efficient in-EVM way
  to verify these signatures (a precompile), a smart-account pattern that uses them, and
  a credible gas model. QRB is building exactly that plumbing and **committing to
  upstream it as a public good**.
- **The output is reusable infrastructure, not a walled garden.** An ML-DSA precompile is
  useful to *any* EVM chain or Reth-based client; a PQ-native ERC-4337 account is useful
  to Ethereum L1 directly. We will (a) propose the precompile as an **EIP**, (b) open a
  **PR / design discussion against Reth**, and (c) coordinate with **EF's own
  post-quantum efforts** rather than duplicate them. Even if QRB-the-L2 never reaches
  mainnet, a working, benchmarked, audited ML-DSA precompile + PQ smart account are
  durable contributions to Ethereum.
- **Timing.** Expert estimates for a CRQC have moved from "2040+" (2019) toward the
  "2028–2032" range (early 2026); exact timing is genuinely uncertain, but the migration
  itself is slow (coordinated Bitcoin-state migration alone is estimated at ≥76 days of
  continuous activity assuming day-one consensus — arXiv:2410.16965). Building the
  primitives *before* they are urgent is the cheap moment to do it.

## 3. The problem in detail

Two distinct quantum threats, only one of which the ecosystem is actively addressing:

| Threat | What breaks | State of remediation |
|--------|-------------|----------------------|
| **A — Impersonation** (Shor on ECDSA) | Funds, identity, contract calls — any exposed public key | PQ signatures standardised; in-EVM verification + account patterns still missing |
| **B — Retroactive decryption** ("harvest now, decrypt later") | All historical on-chain content, once channels/commitments are broken | Largely unaddressed; privacy chains (Aleo, Aztec) rely on SNARKs that are themselves quantum-vulnerable |

QRB addresses **A** as the funded near-term work, and researches **B** (a STARK-based,
hash-and-lattice confidentiality layer — STARKs are natively post-quantum, SNARKs are
not) as a later phase.

## 4. What already exists (Phase 0 — verifiable today)

Public on the repo, with CI (GitHub Actions, Python 3.10/3.11/3.12):

- **ML-DSA-65 signing/verification** in a working account-based chain prototype (signed
  blocks + transactions, world state, replay/tamper/impersonation rejection tests).
- **Rust PoC of the verification core** (`poc/ml-dsa-precompile/`) via the `fips204`
  crate, with real sizes (pk 1,952 / sk 4,032 / sig 3,309 bytes) and a ~200 µs/verify
  benchmark — the gas-model seed.
- **Rust PoC binding it to the real EVM** (`poc/evm-precompile/`): the verifier wrapped
  as a `revm` 41 `Precompile` (`MLDSAVERIFY`, address `0x101`), **exercised by a full
  end-to-end test that stands up a `revm` EVM with a custom `PrecompileProvider` and
  sends a real transaction calling `0x101`** — the ML-DSA-65 verification runs through
  the entire transaction pipeline and returns the expected result. This is the exact
  integration pattern a Reth fork uses, so Phase 1's hardest claim is already
  demonstrated.
- 24-page bilingual whitepaper; dual MIT/Apache-2.0 licence.

The prototype is single-node and local; it is **not yet an L2** — that is Phase 1.

## 5. What this grant would fund (Phase 1 — ~6 months)

Four **core deliverables**, conservatively scoped; stretch goals only if the core lands
early.

1. **`MLDSAVERIFY` precompile in a Reth fork** — precompiles for ML-DSA-44/65/87 and
   FN-DSA-512 at fixed addresses, with a published, benchmarked **gas-cost model**.
   Proposed upstream as an EIP + Reth discussion/PR.
2. **PQ smart account (Solidity)** — an ERC-4337-compatible account validating ML-DSA
   signatures via the precompile; paymaster, key rotation, social-recovery primitives.
3. **Public devnet** — single-node Reth fork with the precompiles active over standard
   JSON-RPC, faucet-funded test wallets. The point at which anyone can submit an
   ML-DSA-validated transaction end-to-end.
4. **JS SDK + reference PQ wallet** — generate PQ wallets, sign, deploy smart accounts,
   interact via RPC; one browser reference dApp.

**Stretch (not payment-gated):** an Ethereum-Sepolia bridge prototype; a Rust SDK; PQ
ERC-20 + PQ multisig reference dApps.

All artefacts MIT/Apache-2.0.

## 6. Budget and milestones

Requested: **€50,000** (~$54k), milestone-based. (Same conservative scope as the prior
NLnet draft; EF does not impose NLnet's first-proposal cap, but the scope is kept tight
on purpose.)

| Workstream | Hours | €/h | € |
|------------|------:|----:|--:|
| Reth fork + ML-DSA precompiles + gas benchmarks | 280 | 35 | 9,800 |
| PQ smart account + paymaster + key rotation + recovery | 240 | 35 | 8,400 |
| Public devnet, RPC, faucet, observability | 140 | 30 | 4,200 |
| JS SDK + reference PQ wallet dApp | 160 | 30 | 4,800 |
| External security review (precompile + smart account) | — | — | 9,000 |
| Documentation, examples, public updates | 120 | 25 | 3,000 |
| Founder coordination, governance, dissemination | 200 | 25 | 5,000 |
| Contingency / integration + review fixes | — | — | 5,200 |
| Cloud, domains, misc | — | — | 600 |
| **Total** | **1,140** | | **€50,000** |

Milestone release: 30% on signed agreement (Reth branch + smart-account scaffold
public) · 30% on devnet live (precompiles active, faucet) · 30% on a PQ-smart-account
transaction validated end-to-end on the public devnet · 10% on final report + SDK +
reference wallet.

Hourly rates reflect Spanish independent-contractor norms and are below salaried
Western-European equivalents. The contingency line is honest estimation, not padding.

## 7. Entry path and ESP fit

ESP supports work that **enables builders** — "strengthening Ethereum's infrastructure,
expanding the range of tools available to those building on Ethereum, gaining a deeper
understanding of cryptographic primitives." QRB hits three of these directly: an
`MLDSAVERIFY` precompile (**infrastructure**), a PQ SDK + reference wallet + smart
account (**tools for builders**), and a benchmarked, audited ML-DSA-in-EVM
implementation (**deeper understanding of a cryptographic primitive**).

Concrete entry path:
- **If a Wishlist/RFP item matches** (look under post-quantum cryptography, cryptographic
  primitives, account abstraction, or client/Reth work): apply to *that item* and tailor
  §3–§5 to its exact wording and deliverables.
- **If none matches cleanly**: book **Office Hours** ("still exploring possibilities,
  connect with our team for guidance") and lead with the working end-to-end revm PoC —
  it is the fastest way to get a real conversation and possibly a tailored scope.

## 8. How this maps to ESP's selection criteria

- **Technical approach** — methodology is concrete and already partly demonstrated: NIST
  FIPS 204 ML-DSA-65 via `fips204`, wrapped as a `revm` precompile and exercised end-to-end
  inside a real EVM (see §4). The plan is an incremental Reth fork, not a from-scratch chain.
- **Ecosystem impact** — the precompile and PQ ERC-4337 account are upstreamable to
  Ethereum itself (EIP + Reth PR), useful to any EVM chain — a positive-sum public good,
  not a QRB silo.
- **Open source** — dual MIT/Apache-2.0, public repo, public CI, public issues; no token
  funds or gates any of this work (see §10).
- **Budget** — €35/h tops out below salaried Western-European equivalents; EF expects some
  flexibility below market rates and this budget already reflects that. Milestone-based,
  with an honest contingency line.
- **Experience** — a working Phase 0 prototype + two Rust PoCs are the delivery evidence;
  external peer review already produced a real security fix and full CI. Single founder,
  AI-assisted and openly disclosed (see §10); first milestone funds a Rust lead + a
  cryptographer.
- **Alignment** — QRB's whole thesis (PQ-native, EVM-compatible, AA-first, upstream-first)
  is built around Ethereum's own needs and values; it contributes to, rather than competes
  with, EF's post-quantum direction.

## 9. Comparison with the state of the art

No known project pursues **PQ signatures + PQ privacy + EVM compatibility + AA** together.
QRL/Zond and Quranium do PQ signatures with weak EVM/AA support; Aleo/Aztec/Monero do
privacy that is **not** post-quantum (SNARK- or curve-based). QRB's differentiator is
addressing both quantum threats with Ethereum-native tooling; the immediate, fundable
slice is the `MLDSAVERIFY` precompile + PQ AA account.

## 10. Non-technical / honesty

- **Single founder, AI-assisted, openly disclosed.** Prototype built with substantial
  AI assistance (Anthropic Claude); all architecture/strategy decisions are the human
  founder's. Disclosed in the README. Phase 1's first milestone funds onboarding a Rust
  client engineer and a cryptographer (roles named in `JOIN.md`).
- **No token is involved in this work.** All Phase 1 deliverables are open source with no
  token dependency; grant funds will not touch any token activity. Any future token is a
  long-term, product-first, separately-counselled contingency — irrelevant here.
- **Track record signal**: external peer review of Phase 0 already produced a real
  security fix (block-proposer validation) and full CI; the public review cycle is
  documented in `marketing/reviewer-response.md`.

## 11. Team and contributors

Founder — **Luiggi Leonel Cedeño Bermeo** (`Fiyiware`): product vision, technical
specification, documentation, external relations; background in digital product / web
development. The working Phase 0 prototype + PoCs are the delivery evidence. The grant
funds onboarding a senior Rust/Reth engineer (lead on the fork) and a cryptographer
(lattice/STARK; review of the precompile + the Phase 3 confidentiality direction).

## 12. Links

- Repository: https://github.com/Fiyiware/quantum-resistance-blockchain
- Whitepaper (EN): `whitepaper/whitepaper-v0.2.en.md`
- Precompile PoCs: `poc/ml-dsa-precompile/`, `poc/evm-precompile/`
- Collaboration terms: `JOIN.md`

---

## Appendix — submission checklist (internal)

- [ ] **Browse the current Wishlist + RFPs + Open Rounds** at https://esp.ethereum.foundation
      and identify the item QRB best addresses (post-quantum crypto / cryptographic
      primitives / account abstraction / Reth-client work). Record the item name + URL.
- [ ] **If a clear item exists** → apply to it; rewrite §3–§5 to match its exact wording
      and deliverables. **If not** → book **Office Hours** and open with the working
      end-to-end revm PoC.
- [ ] Consider routing the Phase 3 confidentiality (STARK) research to an **EF Academic
      Grants** round instead of / in addition to ESP.
- [ ] **Set up an ETH wallet the founder controls** for on-chain grant payment; be ready
      for identity verification + a formal grant letter. Fill the "ETH payout address"
      field above (keep any seed phrase private — never in the repo).
- [ ] Declare AI assistance explicitly in the application (consistent with the README).
- [ ] Attach repo + whitepaper + CI links; mention the working end-to-end PoC explicitly.
- [ ] Keep the NLnet Open Call draft warm for when it reopens after summer 2026.
