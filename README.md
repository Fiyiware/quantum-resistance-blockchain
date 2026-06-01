# QRB — Quantum-Resistance Blockchain

> _"All of the internet from the past 40 years will become an open book, and there is nothing you can do to save the past."_
>
> — **Gilles Brassard**, co-inventor of quantum cryptography (BB84, 1984), 2025 ACM A.M. Turing Award (announced March 2026)

**QRB is a research and prototype track for a post-quantum Layer 2 blockchain on Ethereum-compatible infrastructure.** Phase 0 today: a working Python prototype with real ML-DSA-65 (NIST FIPS 204) signatures, a 24-page whitepaper laying out the technical, economic and regulatory model, and the open-source artifacts to apply for non-dilutive grants. Phase 1+ ahead: EVM execution layer, account abstraction with PQ keys, rollup bridge to Ethereum, public testnet — and an evolving research line toward post-quantum confidentiality on STARKs (Phase 3+ vision).

This README is deliberately careful to distinguish **implemented**, **designed**, **research** and **vision**. We owe public credibility more than hype.

[![CI](https://github.com/Fiyiware/quantum-resistance-blockchain/actions/workflows/ci.yml/badge.svg)](https://github.com/Fiyiware/quantum-resistance-blockchain/actions/workflows/ci.yml)
![Status](https://img.shields.io/badge/status-Phase%200-0b3d91)
![License](https://img.shields.io/badge/license-MIT-green)
![Whitepaper](https://img.shields.io/badge/whitepaper-v0.2-orange)
![Made with](https://img.shields.io/badge/made%20with-Python%20%2B%20Dilithium-blueviolet)

---

## Status — what exists today vs what is on the roadmap

| Component | Status | Reference |
|-----------|--------|-----------|
| ML-DSA-65 (FIPS 204) signatures | ✅ Implemented | `prototype/qrb/crypto.py` |
| Account-based blockchain with signed blocks, transactions and state | ✅ Implemented | `prototype/qrb/` |
| CLI for wallets, transactions, block production and inspection | ✅ Implemented | `prototype/qrb_cli.py` |
| End-to-end tests (signatures, tampering, double-spend, proposer impersonation) | ✅ Implemented + CI | `prototype/tests/test_basic.py` |
| EVM-compatible execution layer with DSARECOVER precompile | 📐 Designed | Whitepaper §3.4 |
| ERC-4337-like Account Abstraction with PQ signatures | 📐 Designed | Whitepaper §3.3 |
| Optimistic rollup bridge to Ethereum L1 | 📐 Designed | Whitepaper §3.5 |
| STARK-based confidentiality (stealth addresses, confidential tx, view keys) | 🔬 Research / Phase 3+ vision | Whitepaper §7.5 |
| QKD institutional integration | 🔬 Research / Phase 3+ vision | Whitepaper §4.6 |
| Production L2 / mainnet | 🚧 Phase 2+ deliverable | Whitepaper §8 |

**The Phase 0 prototype is a single-node, local-only blockchain that demonstrates the post-quantum signature path end to end.** It does not yet implement L2 mechanics (rollup, bridge, data availability), EVM, networking, or decentralised consensus. Those are explicit Phase 1 and Phase 2 deliverables.

For the full technical and economic plan, read [`whitepaper/whitepaper-v0.2.pdf`](whitepaper/whitepaper-v0.2.pdf) (24 pages, Spanish).

---

## Why now

In **April 2026**, an independent researcher used a publicly accessible cloud quantum computer to break a 15-bit elliptic-curve cryptography key, winning Project Eleven's _Q-Day Prize_ ([CoinDesk coverage](https://www.coindesk.com/tech/2026/04/24/researcher-wins-1-bitcoin-bounty-for-largest-quantum-attack-on-underlying-tech)). Fifteen bits is far short of the 256 used by Bitcoin and Ethereum, and the resource cost of attacking larger keys does **not** scale linearly — but the demonstration shifts the conversation from theoretical to demonstrable.

Google now estimates that breaking ECDSA-256 requires **fewer than 500,000 physical qubits** (April 2026 technical report), down from 20 million in 2019. Caltech researchers and the startup Atomic published a separate study suggesting it could be done with on the order of **10,000 _logical_ qubits** using atomic-architecture hardware. A crucial caveat: today's commercial machines have 1,000–2,000 **noisy _physical_ qubits**, and a single fault-tolerant logical qubit requires on the order of hundreds to thousands of physical qubits for error correction. So the real gap between what exists today and what is needed remains **far larger** than a raw comparison of these numbers suggests. The direction of travel is clear; the arrival date of a cryptographically-relevant quantum computer is genuinely uncertain.

Vitalik Buterin (Ethereum founder): _"Crypto has until 2028 to avoid quantum collapse."_

Google has moved its **internal post-quantum migration deadline to 2029**, six years ahead of the NIST 2035 baseline.

In January 2026, Jefferies removed 10% of its Bitcoin allocation from model portfolios citing quantum risk explicitly.

Estimates remain estimates — the year of arrival of a cryptographically relevant quantum computer is genuinely uncertain. But the **direction is unambiguous**: in two years, the consensus window has contracted from "2040 or later" to **"2028–2032"**.

Regulatory pressure tracks the same trajectory: the EU's NIS2 (in force since October 2024) requires post-quantum resistance as a duty-of-care criterion for critical infrastructure, and MiCA (in force since December 2024) sets the regulatory framework under which any future QRB token will be issued.

---

## What QRB aims to combine

The columns below describe the **combination of capabilities QRB targets across its full roadmap**. As shown in the Status section above, only the first column is implemented in the Phase 0 prototype today; the others are designed in the whitepaper, planned for Phase 1, or part of the Phase 3+ research vision. The point of the table is not to claim feature parity now — it is to highlight that **no known project is pursuing all five together**.

| Project | PQ auth | PQ privacy | EVM | Account Abstraction | QKD-ready |
|---|:-:|:-:|:-:|:-:|:-:|
| Bitcoin / Ethereum L1 | ❌ | ❌ | ✅ Ethereum | partial | ❌ |
| QRL / Zond | ✅ | ❌ | partial | ❌ | ❌ |
| Quranium | ✅ | ❌ | partial | ❌ | ❌ |
| Aleo | ❌ (SNARK) | ✅ but NOT PQ-safe | ❌ | ❌ | ❌ |
| Aztec | ❌ (SNARK) | ✅ but NOT PQ-safe | partial | ✅ | ❌ |
| Monero | ❌ | ✅ but NOT PQ-safe | ❌ | ❌ | ❌ |
| **QRB (target across full roadmap)** | **✅ ML-DSA-65 (Phase 0)** | 🔬 STARKs (Phase 3+) | 📐 Phase 1 | 📐 Phase 1 | 🔬 Phase 3+ |

The privacy chains in the market today (Aleo, Aztec, Monero) build their privacy on SNARKs or non-PQ commitments — meaning their privacy is **broken at long horizons** under harvest-now-decrypt-later: data shielded today can be unshielded in the future once a cryptographically relevant quantum computer exists. QRB's research direction proposes to address this by basing its confidentiality layer on STARKs, which depend only on hash collision resistance and are therefore natively post-quantum.

---

## Repository contents

```
quantum-resistance-blockchain/
├── whitepaper/
│   ├── whitepaper-v0.2.md         Source markdown (full whitepaper, Spanish)
│   ├── whitepaper-v0.2.pdf        24-page PDF rendering for distribution
│   └── _build_pdf.js              Reproducible PDF build script (Node + Chrome)
├── prototype/
│   ├── qrb/                       Python package with the prototype
│   ├── qrb_cli.py                 Command-line interface
│   ├── tests/                     End-to-end tests
│   └── README.md                  Prototype setup and usage
├── marketing/                     Public launch materials (X thread, launch kit)
├── .github/workflows/             Continuous integration (GitHub Actions)
├── resumen.md                     ~700-word pitch (Spanish)
├── README.md                      This file
└── LICENSE                        MIT
```

---

## Quick start — run the prototype

The prototype is a minimal Python blockchain that demonstrates ML-DSA-65 signatures, account-based state, signed blocks, mempool and persistence. It runs locally on your laptop, single node, no networking.

**Requirements**: Python 3.10+

```bash
cd prototype
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python tests/test_basic.py
```

You should see all tests pass. **The same tests run on every push to `main` via GitHub Actions** (Python 3.10, 3.11 and 3.12) — see the CI badge above for current status.

Then play with the CLI:

```bash
python qrb_cli.py wallet create --name founder
python qrb_cli.py wallet create --name alice
python qrb_cli.py chain init --founder founder --supply 1000000000
python qrb_cli.py wallet list
# copy alice's address from the listing
python qrb_cli.py tx send --from founder --to <alice-address> --amount 1000
python qrb_cli.py chain mine --proposer founder
python qrb_cli.py wallet balance --name alice
python qrb_cli.py chain block --index 1
```

Blocks and state are persisted as JSON in `.qrb-data/` — open the files to inspect real ML-DSA-65 signatures (~3.3 KB each) and how they compose into a chain.

See [`prototype/README.md`](prototype/README.md) for full prototype documentation.

---

## Roadmap

| Phase | Period | Deliverables | Funding |
|-------|--------|--------------|---------|
| **0 — Validation** | Q2-Q3 2026 | Whitepaper v0.2 · Python prototype with ML-DSA signatures · Public repo · CI · Initial community | Self-funded |
| **1 — Public testnet** | Q4 2026 - Q3 2027 | Grants (NLNet, Ethereum Foundation, Optimism RetroPGF) · EVM execution layer · DSARECOVER precompile · ERC-4337-like AA with PQ · Devnet · Public testnet · SDK · 5-10 dApp demos · Optimistic rollup bridge | €100-250K (grants) |
| **2 — Mainnet beta** | Q4 2027 - Q2 2028 | Audits · Production bridge · MiCA-registered token · DEX listings · 50+ contracts | €500K-2M (seed + token) |
| **3 — GA + Privacy layer** | H2 2028 - 2030 | Sequencer decentralization · STARK confidentiality · Stealth addresses · QKD institutional pilots · Optimistic → ZK rollup migration | Self-sustaining via fees |

Read the full economic and technical model in [`whitepaper/whitepaper-v0.2.pdf`](whitepaper/whitepaper-v0.2.pdf).

---

## Funding philosophy

**Product first, money second.** QRB explicitly rejects the ICO-pre-product model.

1. Non-dilutive grants first: NLNet, Ethereum Foundation, Optimism RetroPGF, Web3 Foundation, Horizon Europe.
2. Then demonstrable product + community.
3. **Only then** — token issuance registered under MiCA with proper legal counsel and a notified whitepaper.

🚫 No ICO before product. 🚫 No vaporware. 🚫 No promises without code.

---

## Looking for collaborators

QRB is actively recruiting for Phase 0 and early Phase 1:

- **1 Rust / Go developer** with blockchain client experience (Geth, Reth, Erigon).
- **1 cryptographer or PhD student** with lattice / Dilithium / STARK expertise.
- **1 frontend developer** for wallet and block explorer.
- **1 technical writer / communicator** (Spanish/English).

Phase 1 contributions are **paid work, funded by grants** (see the roadmap and the NLNet application track) — not unpaid token promises. QRB does not offer token allocations in exchange for contributions today. Any future token-based recognition would be decided only after a product exists and a MiCA-compliant token process is in place; it is explicitly out of scope for Phases 0 and 1.

**Two doors, depending on what you want:**

- 👉 **[`CONTRIBUTING.md`](CONTRIBUTING.md)** — if you want to send a PR, file a bug, pick up a `good-first-issue`, or push back on the whitepaper. Conventions, review process, and an honest compensation section.
- 👉 **[`JOIN.md`](JOIN.md)** — if you're weighing a paid Phase 1 lead, a co-founder track, or something larger than a one-off PR. Concrete profiles wanted, what "joining" can look like, and how to reach me privately.

---

## How to cite

If you reference QRB in academic work, please cite:

> QRB Project. _Quantum-Resistance Blockchain: a post-quantum L2 on Ethereum_. Whitepaper v0.2. May 2026. https://github.com/Fiyiware/quantum-resistance-blockchain

---

## License

Released under the [MIT License](LICENSE) for maximum compatibility with the open-source ecosystem.

---

## AI assistance disclosure

QRB is developed with substantial AI assistance, primarily Anthropic's Claude. This includes code generation, technical documentation drafting, market research synthesis, and editorial review.

The role separation is intentional and explicit:

- **AI is the executor.** It accelerates writing, structures content, and removes friction.
- **The human founder is the director.** All strategic, architectural, economic and editorial decisions are made by the founder. AI does not choose what QRB is — it helps express what it is.

We believe transparent disclosure of AI assistance is more honest than hiding it. The software ecosystem of 2026 embraces AI tooling as a normal part of development workflows; what is not normal — and not acceptable — is pretending otherwise. Pretending to be a 10× engineer when standing on the shoulders of AI tooling is a worse signal than openly using and crediting it.

The founder is responsible for understanding, validating, and maintaining everything in this repository. If something is unclear, open an issue — the answer will come from a human who can defend it.

---

## Acknowledgments

- **Charles Bennett and Gilles Brassard** for inventing quantum cryptography in 1984 and receiving the 2025 ACM A.M. Turing Award (announced March 2026).
- **The NIST PQC team** for standardizing ML-DSA, FN-DSA, SLH-DSA and ML-KEM (FIPS 203-206).
- **Peter Shor** for proving in 1994 what the world is only now waking up to.
- **Vitalik Buterin and the Ethereum Foundation** for the open L2 ecosystem this project builds on.
- **StarkWare and the broader STARK research community** for showing that post-quantum-secure ZK proofs are practical today.
- **Project Eleven** for the Q-Day Prize that put quantum risk on the public agenda.
- **The first independent reviewer to push back on the original README's overpromising language.** That critique directly motivated the Status section above, the proposer-impersonation regression test, and continuous integration via GitHub Actions. Good critique makes projects stronger.

---

🛡️ **Help build the cryptographic infrastructure the world will need in the next decade.**
