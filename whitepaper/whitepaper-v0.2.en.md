# QRB — Quantum-Resistance Blockchain
## Technical & economic whitepaper
**Version 0.2 · Draft · May 2026**

> 🌐 **Language / Idioma:** **English** · [Español](whitepaper-v0.2.md)

> **⚠️ Status note (July 2026).** The central market premise of this document (§1.4: existing L1s cannot realistically migrate in time) has been superseded: the Ethereum Foundation runs a dedicated Post-Quantum team ([pq.ethereum.org](https://pq.ethereum.org)) whose mandate is precisely PQ signature verification via precompiles with migration through account abstraction ([EIP-8141](https://eips.ethereum.org/EIPS/eip-8141)), with fork milestones targeting ~2029. Consequently, **QRB will not build a competing PQ L2**: the project repositions toward contributing to Ethereum's public PQ process and toward the post-quantum confidentiality research line (§7.5), which remains an open gap. See the repository README for details. This document is preserved unchanged as the historical record until v0.3.

> *"All of the internet from the past 40 years will become an open book, and there is nothing you can do to save the past."*
>
> — **Gilles Brassard**, co-inventor of quantum cryptography (BB84 protocol, 1984), 2025 ACM A.M. Turing Award (announced March 2026)

---

## Prologue — The 9-minute attack

Picture a Bitcoin transaction in flight. The sender hits send. The ~10-minute average confirmation window starts ticking.

At minute 9, an attacker with a large enough quantum computer has derived the sender's private key from their public key — visible to anyone on-chain — and reroutes the funds to their own wallet. The original transaction dies in the mempool, unconfirmed. The sender believes they paid. The recipient is still waiting. The money evaporated in 9 minutes.

This is not science fiction. It is mathematics that has existed since 1994 (Shor's algorithm) and hardware whose rate of progress has accelerated sharply over the last 18 months:

- In **March 2026**, Google published that breaking Bitcoin's elliptic-curve cryptography requires **fewer than 500,000 physical qubits**, down from the 20 million the same company estimated in 2019.
- Days later, researchers at **Caltech** and the startup **Oratomic** showed that, using laser-controlled atomic architecture, on the order of **10,000–20,000 qubits** might suffice.
- Today's commercial quantum computers **already have between 1,000 and 2,000 qubits**.
- In **April 2026**, independent researcher **Giancarlo Lelli** broke the first public ECC key (15 bits) using a commercially accessible quantum computer and won Project Eleven's **Q-Day Prize** (1 BTC).
- In **January 2026**, the investment bank **Jefferies** removed 10% of its Bitcoin allocation from its model portfolios, explicitly citing quantum risk.
- **Google** has moved its own internal post-quantum migration deadline up to **2029**, six years ahead of NIST's baseline (2035).
- **Vitalik Buterin** (Ethereum's founder), speaking at Devconnect 2025 (Buenos Aires, November 2025) and citing computer scientist Scott Aaronson, warned that a serious quantum threat could arrive around **2028** and that crypto must prepare its post-quantum migration before then.

The center of gravity of expert estimates has shifted sharply. Two years ago the conversation centered on 2040; today much of it falls in the **2028–2032** range. The exact arrival date of a cryptographically relevant quantum computer remains genuinely uncertain — but the direction of travel is not.

Meanwhile, today's encrypted data is already being harvested — communications, blockchain transactions, medical records, classified emails — to be decrypted once the hardware exists. The practice has a name: *Harvest Now, Decrypt Later*. Brassard, awarded the 2025 ACM A.M. Turing Award (announced March 2026) for inventing quantum cryptography forty years before the world needed it, puts it plainly: *"all of the internet from the past 40 years will become an open book, and there is nothing you can do to save the past."*

**QRB exists so that the future is not that open book.**

---

## Executive summary

QRB (Quantum-Resistance Blockchain) is a Layer 2 (L2) blockchain built on Ethereum, designed from the ground up to resist quantum-computer attacks along **two complementary dimensions**:

1. **Post-quantum authentication**: digital signatures are replaced with algorithms standardized by NIST in 2024 (ML-DSA / CRYSTALS-Dilithium, FN-DSA / FALCON, SLH-DSA / SPHINCS+). This neutralizes Shor's attack against elliptic-curve keys — the 9-minute attack described in the prologue. **Implemented and demonstrable in the Phase 0 prototype (May 2026).**

2. **Post-quantum confidentiality** (Phase 3+ vision): a native privacy layer combining *stealth addresses*, confidential transactions with lattice-based commitments, zero-knowledge (ZK) proofs built on **STARKs** (hash-based, natively post-quantum), and optional *view keys* for MiCA compliance. This neutralizes the retroactive-harvesting attack against transaction history — data published today stays confidential even if someone has a quantum computer tomorrow.

On top of those two cryptographic dimensions:

- **Full EVM compatibility** and Ethereum developer tooling (Solidity, Hardhat, Foundry, MetaMask with a PQ adapter): any Ethereum app migrates without rewriting.
- **Native Account Abstraction**: hides the complexity and size of post-quantum signatures from the end user. UX equivalent to a normal Ethereum wallet.
- **Optional integration with QKD networks** (Quantum Key Distribution) for institutional clients already operating on physical quantum infrastructure (a research line, Phase 3+ vision; not a Phase 0 or Phase 1 goal). It is an exploratory possibility, not an early-delivery commitment. QRB would be the first blockchain to combine both families of quantum cryptography, the mathematical one (PQ) and the physical one (QKD/BB84).
- **A responsible funding strategy**: non-dilutive public grants in Phase 1 (NLNet, Ethereum Foundation, Optimism), a seed round in Phase 2, and only then a token issuance registered under a MiCA whitepaper with legal counsel.

This document describes the problem, the technical solution, the economic model, governance, the roadmap and the project's risks. It is aimed at developers, cryptographers, grant reviewers and, at a later stage, institutional investors.

---

## 1. The problem

### 1.1 Two quantum threats, not one

All of the public-key cryptography that underpins today's digital economy rests on two mathematical assumptions: the hardness of **factoring large integers** (RSA) and the hardness of the **elliptic-curve discrete logarithm** (ECDSA, EdDSA, Schnorr). In 1994, Peter Shor proved that a large enough quantum computer can solve both problems in polynomial time. This is not conjecture: it is proven mathematics.

From that single algorithm, **two distinct classes of threat** follow, which QRB neutralizes separately:

| Threat | What it breaks | Concrete example |
|---------|-----------|------------------|
| **A — Impersonation** (Shor on signatures) | The attacker derives the sender's private key and signs transactions in their name | The 9-minute attack on Bitcoin. Draining wallets with an exposed public key |
| **B — Retroactive harvesting** (Shor on channel encryption + decryption of stored data) | The attacker decrypts content captured years earlier | *Harvest now, decrypt later*. Retrospective reading of the chain's entire history |

Today's post-quantum industry fundamentally covers **Threat A** (resistant signatures). QRB is explicitly designed to cover **both A and B** — a combination we are not aware of any other blockchain pursuing (layer B is a Phase 3+ research line, not a delivered feature). Section 7.5 details layer B.

### 1.2 The timeline has contracted

| Year | Estimated qubits to break RSA-2048 / ECC-256 | Source |
|-----|---------------------------------------------|--------|
| 2012 | ~1 billion (physical, RSA-2048-era estimates) | Academic estimates |
| 2019 | ~20 million (physical, RSA-2048) | Gidney & Ekerå (Google) |
| May 2025 | ~1 million (physical) | Google Research (revised) |
| March 2026 | **< 500,000** (physical) | Google Quantum AI |
| March 2026 | **~10,000** (logical, atomic architecture) | Caltech + Oratomic |

> **Methodological caveat — these numbers are not apples-to-apples.** They mix *targets* (RSA-2048 factoring vs ECC-256 discrete log — the 2019 figure, for instance, is Gidney & Ekerå's estimate for **factoring RSA-2048**, not breaking ECC) and *qubit types* (noisy physical vs error-corrected logical). A fault-tolerant logical qubit today requires **on the order of hundreds to thousands of physical qubits** for its error correction; today's commercial computers (IBM, Google, Quantinuum, IonQ) have **1,000–2,000 noisy *physical* qubits**, without that error correction. So the real gap between what exists today and what is needed is **far larger** than a raw comparison suggests, and the cost of breaking larger keys does not scale linearly. The point of the table is the **downward trend in estimated resources**, not any single comparable figure.

The trend in the estimates, however, is unambiguously downward: several orders of magnitude of reduction in estimated resources over a decade. **The exact arrival date of a cryptographically relevant quantum computer (CRQC) is genuinely uncertain**; what is not uncertain is the direction, nor the fact that cryptographic infrastructure takes years to migrate. That asymmetry — slow migration versus a growing threat — is what justifies acting now.

Timelines published by serious actors:

- **Google**: internal migration completed by **2029**.
- **NIST**: transition standard set for 2035, but outpaced by industry timelines.
- **CNSA 2.0 (NSA, USA)**: classified systems fully migrated before 2035.
- **ANSSI (France), BSI (Germany)**: PQ cryptography mandatory for critical systems before 2030.
- **NIS2 (EU)**: the directive entered into force in January 2023, with a national-transposition deadline of October 2024; it establishes risk-management duties under which quantum resistance fits as a forward-looking duty-of-care criterion.
- **MiCA (EU, in force since December 2024)**: regulates crypto-asset issuers, opening the expectation of PQ requirements for tokens in critical infrastructure.

### 1.3 Harvest now, decrypt later: the heist that has already begun

Blockchain transactions are **public and permanent**. An ECDSA signature issued today will remain available for retrospective attack once a cryptographically relevant quantum computer (CRQC) exists. Addresses that have already spent have their public key exposed on-chain forever.

- In Bitcoin, **approximately 6.9 million BTC** (≈ a third of the total supply) sit in addresses with an exposed public key, including the estimated one million belonging to Satoshi Nakamoto himself. A caveat: estimates of how much is *immediately exploitable* vary — for example, CoinShares argues for a much smaller subset (on the order of 10,000 BTC in legacy P2PK addresses) — but the exposed-key surface grows over time as addresses are reused. What matters is the direction of the curve, not the exact figure.
- In Ethereum, the situation is similar for any account that has sent at least one transaction.
- The **encrypted communications** of 99% of internet traffic (TLS over elliptic curves) are being actively stored by state actors with long-term intelligence incentives.

The temporal asymmetry is what makes this attack devastating: the attacker does not need quantum capability **today**, they only need to **store**. Decryption can happen once the technology matures, against data that is 5, 10 or 20 years old.

### 1.4 Migrating existing L1s in time is mathematically improbable

A recent technical analysis of Bitcoin (arXiv:2410.16965) estimates that a full migration of the network's state to post-quantum addresses requires **a minimum of 76 days of continuous on-chain activity**, assuming unanimous community consensus from day one. Bitcoin's history shows that such consensus is never reached in less than 1–3 years. Ethereum has a more agile governance process but is equally slow. Solana, BNB Chain, Avalanche and the like have published no operational migration plan.

By contrast, **a PQ-native chain from day one has nothing to migrate**: it is born in the correct state. That is the structural window in which QRB exists.

---

## 2. State of the art

### 2.1 Extended comparison

| Project | PQ signatures | PQ privacy | EVM | AA | QKD-ready | Main limitation |
|----------|:---------:|:-------------:|:---:|:--:|:---------:|----------------------|
| Bitcoin / Ethereum L1 | ❌ | ❌ | partial / ✅ | ❌ / partial | ❌ | Migration politically blocked (76+ days, no consensus) |
| QRL / Zond | ✅ (XMSS → Dilithium) | ❌ | partial | ❌ | ❌ | Poor UX, minimal ecosystem |
| Quranium | ✅ (Dilithium) | ❌ | partial | ❌ | ❌ | Very small community and dev traction |
| Cellframe | ✅ (CRYSTALS, NTRU) | partial | ❌ | ❌ | ❌ | Complex architecture, hard to fork |
| Naoris Protocol | ✅ (hybrid) | ❌ | ❌ | ❌ | ❌ | More a security mesh than a general blockchain |
| Aleo | ❌ (SNARK) | ✅ (not PQ) | ❌ | ❌ | ❌ | Privacy not quantum-resistant |
| Aztec | ❌ (SNARK) | ✅ (not PQ) | partial | ✅ | ❌ | Privacy not quantum-resistant |
| Monero | ❌ | ✅ (not PQ) | ❌ | ❌ | ❌ | Privacy not quantum-resistant, no smart contracts |
| **QRB (roadmap goal)** | **✅ ML-DSA-65 (Phase 0)** | 🔬 STARKs (Phase 3+) | 📐 Phase 1 | 📐 Phase 1 | 🔬 Phase 3+ | Young project; L2 core still to be built |

> **Honest reading of this table.** The columns describe the **combination of capabilities QRB pursues across its entire roadmap**, not its current state. Only PQ authentication (ML-DSA-65) is implemented today in the Phase 0 prototype; EVM and Account Abstraction are designed for Phase 1, and PQ privacy and QKD integration are a research line / Phase 3+ vision. The value of the table is not to claim feature parity today, but to point out that **no known project pursues all five dimensions together**. The precise status of each component is in the roadmap section (§8) and in the status table of the repository README.

No project on the market combines all five columns. QRB positions itself in that gap.

### 2.2 Why L2 and not L1?

A dedicated L1 forces you to solve the **validator-incentive problem**: convincing node operators to commit hardware and capital, which requires significant inflationary issuance of a native token and community bootstrapping. For a project that does not start from a €20–50M fund, this is prohibitive and historically leads to insecure networks for the first 1–3 years.

An L2 on Ethereum, by contrast:
- **Inherits the security** of Ethereum's settlement layer.
- **Inherits the liquidity** via established bridges.
- **Reduces the initial cost** by a factor of 10× relative to an L1.
- **Lets the team focus on what is differential** (PQ cryptography, privacy and UX) instead of spending resources reinventing consensus.

---

## 3. Technical solution — PQ authentication layer

### 3.1 Cryptographic stack

QRB adopts the NIST post-quantum standards as its authentication base:

- **Primary digital signatures**: ML-DSA (FIPS 204, CRYSTALS-Dilithium), specifically **ML-DSA-65** as the default. Equivalent to 192 bits of classical security. Signature ~3,309 bytes; public key ~1,952 bytes. We default to the level-3 parameter set (ML-DSA-65) rather than the smaller level-2 ML-DSA-44 because a base-layer signature commits keys to a public ledger for decades, where a generous long-term security margin matters more than saving ~1 KB per signature; ML-DSA-87 (level 5) and FN-DSA remain available opt-in for users who want a larger margin or more compact signatures respectively.
- **Opt-in alternative signatures**: FN-DSA (FALCON, FIPS 206 — draft, expected late 2026–2027) for cases that require compact signatures (~700 bytes); SLH-DSA (SPHINCS+, FIPS 205) for maximally conservative hash-based scenarios.
- **Key exchange**: ML-KEM (FIPS 203, CRYSTALS-Kyber), specifically ML-KEM-768, for encrypted node-to-node communication.
- **Hashing**: Keccak-256 (EVM compatibility) and SHA3-512 as a precompile for applications with an explicit post-quantum margin against Grover.

### 3.2 Hybrid signatures during the transition

During mainnet's first 24 months, QRB will offer an optional **hybrid signature** mode: each transaction can be signed simultaneously with ECDSA-secp256k1 and with ML-DSA. The transaction is only considered valid if **both** signatures are. This mechanism enables progressive migration without an abrupt cutover.

### 3.3 PQ Account Abstraction

PQ signatures are ~50× larger than ECDSA. To prevent this from degrading the user experience, QRB implements **native Account Abstraction** (ERC-4337-like) from the first block:

- Each account is a smart contract with its own signature-validation logic.
- PQ signatures are verified via a dedicated **precompile** with stable gas cost.
- Users can define **key rotation**, **social recovery**, **paymasters**, **PQ multisig** and **delegated signing** without protocol changes.
- Addresses are derived from the **hash** of the public key (SHA3-256, last 20 bytes in hex), allowing the public key to stay hidden until the first spend from the address — elementary protection against *harvest now, decrypt later* in its basic form.

### 3.4 EVM compatibility

QRB's execution layer is a fork of the Reth (Rust) or Geth (Go) client, modified to:

- Replace the `ECRECOVER` opcode with `MLDSAVERIFY` in native transactions. Unlike `ECRECOVER`, which *recovers* the signer's public key from the signature, ML-DSA cannot recover the key — `MLDSAVERIFY` is `(message, signature, public key) → bool`. This is why the ~1,952-byte public key must travel with the transaction or live in the signer's smart account: a real data-availability cost, made explicit rather than hidden.
- Add precompiles at `0x100`–`0x103` for ML-DSA-44, ML-DSA-65, ML-DSA-87 and FN-DSA-512 respectively.
- Keep all other standard EVM opcodes unchanged — any Solidity contract compiles without modification.
- Keep `ECRECOVER` functional for bridges and historical compatibility, marked as deprecated.

### 3.5 Bridge to Ethereum

The bridge is the most security-critical component of any L2. QRB adopts the **optimistic rollup** model of the current OP Stack, with:

- Proposer and verifier signatures in ML-DSA-65 from day 1.
- A 7-day challenge period, aligned with Optimism.
- A migration plan to a **ZK-rollup with STARKs** once efficient provers for Dilithium signatures exist (active research in 2026).

---

## 4. Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    Application layer                            │
│  (DeFi, NFTs, PQ identity, RWA tokenization, games)            │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│         PQ Confidentiality layer (Phase 3+ — §7.5)             │
│  Stealth addresses · Confidential tx · STARK proofs · View keys │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│             Account layer (PQ Account Abstraction)              │
│   Contract wallets · Key rotation · PQ multisig                 │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│            Execution layer (EVM + PQ precompiles)               │
│ Reth fork · MLDSAVERIFY · ML-DSA / FN-DSA / SLH-DSA precompiles  │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│      Submission layer (standard HTTPS + optional QKD §4.6)      │
│      Public mempool + institutional QKD-secured channels        │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│         Data Availability & Settlement layer                    │
│   Calldata on Ethereum (Phase 1) → EIP-4844 blobs (Phase 2)     │
│   PQ fraud proofs · Optimistic bridge                           │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│                Ethereum L1 (settlement & DA)                    │
└────────────────────────────────────────────────────────────────┘
```

### 4.6 QKD integration for institutional clients (Phase 3+ vision)

Mathematical post-quantum cryptography (PQ) and physical quantum cryptography (QKD, *Quantum Key Distribution*) are **complementary, not competitors**. PQ runs over any TCP/IP network. QKD requires dedicated fiber or satellites (like Micius in China; Telefónica/Deutsche Telekom networks in the EU; Amazon Braket and the AWS Center for Quantum Networking in the US).

QRB optionally integrates QKD channels for **transaction submission** from institutional clients:

- **Use case**: a European bank with an internal QKD network (several already have them deployed after NIS2) can send its transactions to QRB over a QKD-secured channel, guaranteeing perfect confidentiality of the very act of sending the transaction, not just of its content.
- **How it works**: the institutional wallet signs with ML-DSA-65 like any user, but the submission channel to the nearest node is encrypted with a key established via BB84. The receiving node forwards to its normal mempool.
- **Possible differential interest**: we are not aware of any other blockchain that has published a formal integration with the existing QKD stack. If the QKD deployments underway across Europe (accelerated by NIS2) mature, an institutional B2B market could open. We present this as a hypothesis to explore, not an advantage already won.
- **Honest limitations**: QKD protects only the *submission channel*, not on-chain content (which is public unless the confidentiality layer §7.5 is used); QKD alone does not authenticate (hence its combination with ML-DSA signatures); and it requires dedicated fiber or satellite links, restricting it to institutional clients. It is not a silver bullet.
- **Status**: Phase 3+ research line / vision. Would require a partnership with one or more European QKD operators (possible paths: pilots via Cellnex, Telefónica Tech or Deutsche Telekom T-Systems). Not a Phase 0 or Phase 1 goal.

This framing is what sets QRB apart from *another* post-quantum project: it is built around the recognition that the quantum era has two answers, not one.

---

## 5. Tokenomics

### 5.1 The QRB token

The ecosystem's native token will be called **QRB**. Its functions are:

- **Gas payment**: all transactions are paid in QRB.
- **Staking** for decentralized sequencers and verifiers (Phase 2+).
- **Governance** of the protocol (Phase 2+).
- **Access to ecosystem services** (token deployment, naming service, paymasters, institutional QKD integration).

### 5.2 Total supply and distribution

Fixed (non-inflationary) supply: **1,000,000,000 QRB**.

| Category | % | Amount | Vesting / Unlock |
|-----------|---|----------|----------------------|
| Founder and initial team | 15% | 150,000,000 | 12-month cliff + 36-month linear vesting |
| Foundation treasury | 20% | 200,000,000 | Released by governance, max pace 2%/month |
| Validators / Stakers (rewards) | 30% | 300,000,000 | Gradual emission over 10 years |
| Ecosystem and dev grants | 25% | 250,000,000 | Released by governance |
| Initial liquidity and public offering | 10% | 100,000,000 | Activated at mainnet, subject to MiCA registration |

Deliberately conservative design: a 15% founder allocation with long vesting is below the industry standard, to avoid signaling centralization.

### 5.3 Protocol fees

Gas following the EIP-1559 model:

- **Base fee**: burned (deflationary).
- **Priority fee**: to the sequencer / proposer.
- **Protocol fee**: 15% on top of the priority fee, directed to the treasury to sustain development, audits and grants long-term.

### 5.4 Ecosystem value capture

Any token deployed on QRB (ERC-20-PQ, ERC-721-PQ, etc.) pays:

- A fixed deployment fee in QRB (~5–50 QRB depending on type).
- Transfers and operations consume gas in QRB.
- (Phase 3+) Using confidential transactions consumes a gas multiple to reflect the cost of generating the STARK proof.

---

## 6. Governance

QRB will follow a **progressively decentralized** governance model:

- **Phase 0–1**: governance centralized in the QRB Foundation (a legal entity to be constituted, probably in Spain or Switzerland). Technical decisions made by the core team, published openly.
- **Phase 2**: introduction of on-chain proposals (QRB Improvement Proposals, QIPs) binding for protocol parameters (gas, fees, treasury).
- **Phase 3+**: fully on-chain governance with a residual Foundation veto for security emergencies. An explicit plan to remove that veto after 5 years of stable mainnet.

---

## 7. Security

### 7.1 Threat model

QRB is designed against an attacker with:

- Growing quantum computational resources (potential CRQC ~2028–2032 per updated expert estimates; exact timing genuinely uncertain).
- *Harvest now, decrypt later* capability against the chain's public history.
- Control of up to 33% of the stake (standard BFT assumption).
- Full access to the source code (the entire project is open source MIT/Apache-2.0).

### 7.2 Audits and verification

Before mainnet (Phase 2):

- **Cryptographic audit** of the PQ signature module by a specialized firm (Trail of Bits, Least Authority, NCC Group). Estimated cost: €60,000–120,000.
- **EVM audit** of the modified execution client. €50,000–100,000.
- **Bridge audit**. €80,000–150,000.
- **Formal verification** of the PQ precompiles with Coq or Lean (24-month target).
- **Bug bounty** with a ceiling of 500,000 QRB for critical bugs.

### 7.3 Emergency plan

Emergency multisig (5 of 9, Foundation + reputable external ecosystem figures) with the power to **pause the bridge** for a maximum of 72 hours. No power over the chain's state or over user funds.

### 7.4 Risk of the PQ primitive itself

Post-quantum signatures are young cryptography. It is possible that a classical attack against Dilithium is discovered in the coming years. QRB mitigates this risk:

- **Algorithm-agnostic design**: the validation precompile is swappable.
- **A pre-established Plan B**: migration to SLH-DSA (hash-based, more conservative cryptographic assumptions) in under 30 days if Dilithium were compromised.
- **Optional hybrid signatures** during the first 24 months as an additional safety belt.

### 7.5 Confidentiality layer (Phase 3+ vision)

This section describes QRB's response to **Threat B** (retroactive harvesting). It is the piece that distinguishes QRB from every other post-quantum blockchain on the market and makes it a real privacy proposition, not just secure authentication.

#### 7.5.1 Stealth addresses

Each time a user receives a transaction, the sender's wallet derives a **single-use address** from the recipient's view and spend key pair (a model analogous to Ethereum's EIP-5564 and to Monero's, adapted to PQ primitives). The result: no observer can link two different payments to the same user. The public address QRB publishes for receiving never appears directly on-chain.

#### 7.5.2 Confidential transactions

The amount of each transaction is **encrypted** via a lattice-based cryptographic commitment (a post-quantum variant of Pedersen). Only the sender and recipient know the amount. The chain verifies that the sum of inputs equals the sum of outputs without revealing the specific amounts, by means of a range proof built on STARKs.

#### 7.5.3 ZK proofs on STARKs (a critical technical decision)

**SNARKs (Groth16, PLONK, BN254) are NOT post-quantum** — their parameters rest on elliptic-curve assumptions. The precise risk depends on the construction: information-theoretically *hiding* commitments (e.g. Pedersen) do **not** leak the committed value to a future quantum computer — but their *binding* can break (enabling undetectable inflation), and any payload encrypted with elliptic-curve key exchange (note encryption, stealth-address ECDH) **is** retroactively decryptable — genuine harvest-now-decrypt-later. Either way, privacy that rests on elliptic-curve assumptions does not hold at long horizons. This is the under-stated risk in projects like Aleo and Aztec: their privacy protects today, but on assumptions a CRQC breaks. STARKs avoid this entirely because they depend only on hash collision resistance.

**STARKs are natively post-quantum**: they depend only on collision-resistant hash functions (modelable as a random oracle) and on Reed-Solomon codes. Larger proof size (~50–200 KB today, improving rapidly), but solid security under the most conservative known assumptions.

QRB builds its entire privacy layer on STARKs. Reference implementations: StarkWare (Cairo, already in production on Starknet), RISC Zero, Plonky3 (Polygon).

#### 7.5.4 Selective disclosure / view keys

The user can generate a **read-only** key over their history and hand it to their bank, tax advisor or regulatory authority when required. This provides the balance between **privacy by default** and **MiCA / AML compliance** without making the system transparent to everyone.

For regulated companies (banks tokenizing assets, institutional custodians), QRB also supports an **opt-in transparency** mode per contract — the contract declares its balance and movements openly, keeping the rest of the ecosystem confidential.

#### 7.5.5 Forward secrecy and periodic key rotation

The privacy layer is designed with structural **forward secrecy**: view keys can be rotated periodically without losing access to prior history, limiting the damage a key leak at a specific moment can cause.

#### 7.5.6 Impact on the gas model

STARK proofs are compute-intensive. The user will pay a gas multiple (~10–50×) for confidential transactions relative to transparent ones. This incentivizes conscious use: small day-to-day payments can go in transparent mode; large, sensitive or institutional transactions in confidential mode. The user chooses.

---

## 8. Roadmap

| Phase | Period | Milestones | Budget |
|------|---------|-------|-------------|
| **Phase 0 — Validation** | Q2–Q3 2026 | Whitepaper v0.2 · Rust/Python prototype with working Dilithium signatures · Public GitHub · Landing page · Embryonic community | €0–2,000 (self-funded) |
| **Phase 1 — Public testnet** | Q4 2026 – Q3 2027 | Grants (NLNet, EF, Optimism RetroPGF) · Internal devnet · Incentivized public testnet · Faucet · Explorer · JS/Rust SDK · First 5–10 demo dApps · Initial Ethereum bridge | €100,000–250,000 (grants) |
| **Phase 2 — Mainnet beta** | Q4 2027 – Q2 2028 | Full audits · Production bridge · QRB token issued under MiCA · DEX listings · 50+ contracts deployed · Production Account Abstraction | €500,000–2,000,000 (seed or regulated token) |
| **Phase 3 — Mainnet GA + Privacy layer** | H2 2028 – 2030 | Sequencer decentralization · On-chain governance · Institutional QKD pilots · STARK confidentiality layer · Stealth addresses · View keys · Optimistic → ZK rollup migration | Self-sustaining via fees + B2B integrations |

---

## 9. Team and collaborators

**Founder**: Luiggi Leonel Cedeño Bermeo. Product vision, strategic direction, public representation.

**Collaborators actively sought (Phase 0)**:

- 1 Rust/Go developer with blockchain client experience (Geth, Reth, Erigon).
- 1 cryptographer or PhD student with lattice / Dilithium expertise.
- 1 frontend developer for wallet and explorer.
- 1 technical writer / communicator (ES/EN).

**Collaborators sought in Phase 1 (with grants already secured)**:

- 1 ZK engineer with STARK experience (StarkWare, RISC Zero, Polygon).
- 1 QKD / physical quantum cryptography specialist for the institutional pilot.
- 1 legal / regulatory lead specialized in MiCA and digital assets.

Any significant contributor receives an allocation from the "Ecosystem" category on terms to be defined with the Foundation.

The project is single-founder *by design* at Phase 0, but no longer single-*person* in practice: as of June 2026 it has already received merged external contributions (regression tests, bug fixes) from independent developers — see the repository's contributor graph. Growing that contributor base into a permanent Phase 1 team is the explicit purpose of the grant and the recruitment above.

---

## 10. Funding

### 10.1 General strategy

QRB follows a **staged and conservative** funding strategy, avoiding the *ICO-before-product* model of 2017–2018.

### 10.2 Sources by phase

**Phase 0** — self-funded (~€1,000 from the founder + time).

**Phase 1** — non-dilutive grants. Target programs:

- **NLNet / NGI Zero Commons Fund** (European Commission, https://nlnet.nl/commonsfund/) — funding for open-source internet technology, including open cryptography. Grants of €5,000–50,000, with the possibility to scale up for proven potential (up to €500,000 per project over the fund's lifetime).
- **Ethereum Foundation Ecosystem Support** — research and tooling grants, PQ research specifically welcome.
- **Optimism RetroPGF** — retroactive payments for public goods on the OP Stack.
- **Arbitrum Foundation Grants**.
- **Web3 Foundation** (Polkadot).
- **Horizon Europe** programs related to quantum and cybersecurity.

**Phase 2** — a combination of:

- A seed round with investors focused on crypto infrastructure and/or quantum cybersecurity (focus: a16z crypto, Variant, Hashed, specialized European funds).
- A public issuance of the QRB token formally registered under **MiCA**: whitepaper notified to the CNMV, specialized legal counsel (budget €5,000–15,000).

**Phase 3+** — self-sustaining via protocol fees + B2B integrations (institutional QKD clients) + treasury.

---

## 11. Risks and mitigations

| Risk | Impact | Likelihood | Mitigation |
|--------|:-------:|:------------:|------------|
| Cryptanalytic break of ML-DSA | Catastrophic | Low | Pre-established Plan B: migration to SLH-DSA. Modular design. |
| Ethereum accelerates its PQ migration and absorbs the value proposition | High | Medium | QRB positions itself as a PQ-first space while Ethereum migrates (4–7 years). When Ethereum migrates, QRB pivots to specialization: PQ privacy + institutional QKD. |
| **Ethereum's own L1 is itself broken by a CRQC** (settlement, bridge, upgrade multisigs all use ECDSA/BLS) | Catastrophic | Tied to CRQC timing | **Honest dependency, stated plainly:** like every L2, QRB settles on Ethereum and inherits its L1 cryptographic assumptions. QRB protects the layer where *user* keys and contract logic live, and buys migration time — it does **not**, and cannot, make Ethereum's L1 post-quantum on its own. The bridge is the most L1-exposed component (hence its conservative, stretch-goal treatment). If/when Ethereum migrates its L1 (its stated roadmap), the dependency resolves; until then QRB's protection is real but scoped to the execution/account layer. |
| No grants secured in Phase 1 | High | Medium-Low | Parallel strategy across 4–5 programs. Combined probability of securing at least one: >75%. If all fail, a reduced Phase 1 with own budget. |
| MiCA regulatory changes harden requirements | Medium | High | Ongoing legal counsel. Pure utility-token model (not a security). Willingness to register as a CASP if needed. |
| Critical bug in the bridge | Catastrophic | Low-Medium | Multiple audits before mainnet. Emergency withdrawal-only mode. Protocol insurance (Nexus Mutual or similar) for Phase 2+. |
| The privacy layer attracts adverse regulatory scrutiny | Medium-High | Medium | Design with native view keys and an opt-in transparent mode. MiCA compliance as a guiding principle. |
| Founder cannot commit full-time | Medium | Medium | The project is designed for part-time management in Phase 0–1. After the first grant, full-time commitment. |
| QKD does not mature as a B2B market on the expected timeline | Low | Medium | Phase 3+ vision, not critical for the product. The PQ privacy layer remains a sufficient differentiator. |

---

## 12. Conclusion

QRB does not aspire to replace Ethereum or Bitcoin. It aspires to be **the default network when an organization, a protocol or a user needs real post-quantum guarantees**: when a regulated financial entity needs to custody assets with NIS2 and MiCA compliance; when an identity protocol requires signatures valid 30 years out; when a user wants to protect not only their funds but their financial history from the risk of retroactive harvesting.

The project combines:

- A **real and verifiable problem**: the quantum threat documented by NIST, Google, Caltech, Project Eleven and acknowledged by the industry itself (Jefferies, Google, Vitalik).
- A **solid, dual technical solution**: PQ for authentication, STARKs + lattice for privacy, both standardized or on conservative cryptographic assumptions.
- A **realistic market strategy**: an L2 on Ethereum, not an L1 from scratch.
- A **unique differentiation**: the only blockchain with PQ authentication + PQ privacy + EVM + Account Abstraction + planned QKD integration.
- A **legal, staged funding model**: non-dilutive grants → seed → regulated token, not the other way around.
- An **open, modest team** that prioritizes execution over hype.

The window to build this closes with every month that passes. The algorithms are standardized, quantum hardware is advancing faster than expected, and European regulation is beginning to require what QRB will offer. The invitation is open to developers, cryptographers, grant reviewers and investors: this is the moment.

---

## Appendices

### A. Abbreviated glossary

- **CRQC**: Cryptographically Relevant Quantum Computer.
- **ML-DSA**: Module-Lattice Digital Signature Algorithm (FIPS 204, derived from CRYSTALS-Dilithium).
- **FN-DSA**: FFT over NTRU Digital Signature Algorithm (FALCON).
- **SLH-DSA**: Stateless Hash-based Digital Signature Algorithm (FIPS 205, SPHINCS+).
- **ML-KEM**: Module-Lattice Key Encapsulation Mechanism (FIPS 203, Kyber).
- **STARK**: Scalable Transparent ARgument of Knowledge — hash-based ZK proofs, natively post-quantum.
- **SNARK**: Succinct Non-interactive ARgument of Knowledge — ZK proofs typically based on elliptic curves, vulnerable to quantum attacks except for hash-only variants.
- **QKD**: Quantum Key Distribution — key distribution using quantum properties of light (BB84, E91 protocols).
- **L2 / Rollup**: a scaling layer built on top of Ethereum.
- **Account Abstraction**: a model where accounts are contracts with arbitrary validation logic.
- **Harvest now, decrypt later (HNDL)**: the practice of storing encrypted data today to decrypt it once quantum capability exists.
- **Stealth address**: a single-use derived address for a specific payment, hiding the recipient's identity.
- **View key**: a read-only key over an account's history, used for selective disclosure.

### B. Timeline of relevant quantum milestones

- **1984** — Bennett and Brassard publish the BB84 protocol.
- **1994** — Peter Shor publishes the quantum factoring algorithm.
- **1996** — Lov Grover publishes the quantum search algorithm.
- **1989** — First physical BB84 experiment at IBM (32 cm).
- **2017** — China launches the Micius quantum satellite.
- **2019** — Google estimates 20M qubits to break ECDSA-256.
- **2022** — NIST PQ standards finalization begins.
- **August 2024** — Official publication of FIPS 203, 204, 205.
- **October 2024** — NIS2 national-transposition deadline in the EU.
- **December 2024** — MiCA enters into force in the EU.
- **May 2025** — Google revises its estimate to 1M qubits.
- **January 2026** — Jefferies cuts 10% of Bitcoin in model portfolios over quantum risk.
- **March 2026** — Google publishes a <500K qubit estimate.
- **March 2026** — Caltech + Oratomic publish a 10,000–20,000-qubit architecture.
- **March 2026** — Google moves its internal migration deadline up to 2029.
- **April 2026** — Giancarlo Lelli wins the Q-Day Prize, breaking ECC-15 on a public quantum computer.
- **March 2026** — ACM announces the 2025 A.M. Turing Award for Bennett and Brassard.
- **May 2026** — QRB begins Phase 0.

### C. Key references

- NIST FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA) — published August 2024. FIPS 206 (FN-DSA) — draft, expected late 2026–2027.
- Project Eleven, *Q-Day Prize* (announced via PR Newswire, April 2026).
- ACM, *2025 A.M. Turing Award to Bennett and Brassard* (announced March 2026).
- *Bitcoin post-quantum migration analysis*, arXiv:2410.16965.
- Regulation (EU) 2023/1114 MiCA.
- Directive (EU) 2022/2555 NIS2.
- Buterin, V. et al., *Account Abstraction via Entry Point Contract Specification (ERC-4337)*.
- Optimism Bedrock specifications.
- Bennett, C. H., & Brassard, G. (1984). *Quantum cryptography: Public key distribution and coin tossing*. Proc. IEEE International Conference on Computers, Systems and Signal Processing.
- Shor, P. (1994). *Algorithms for quantum computation: discrete logarithms and factoring*.
- Google Quantum AI (2026). Revised qubit estimates for breaking ECDSA-256.
- Project Eleven, *Q-Day Prize* (April 2026).
- Post-Quantum Cryptography Coalition (MITRE et al.), *PQC Migration Roadmap* (May 2025).
- Technical documentation for CRYSTALS-Dilithium, FALCON and SPHINCS+.
- StarkWare Cairo specifications.
- Bit2Me Academy, *The largest Bitcoin and cryptocurrency heists in history*.

---

*This document is a draft (v0.2) open to technical and economic review. Comments, corrections and collaboration proposals are welcome in QRB's public repository.*

*Open source · MIT / Apache-2.0*
