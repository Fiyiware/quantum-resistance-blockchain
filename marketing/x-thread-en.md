# English launch thread — ready to publish (Day 2)

Natural-English translation of the Spanish launch thread. Publish as a standalone
10-tweet thread the day after the Spanish one. Same mechanics: post tweet 1, then
reply to your own tweet with 2, reply to 2 with 3, etc.

URLs already in place.

---

**Tweet 1/10**

In April 2026, a researcher used a public quantum computer to derive a private key from its public key — and earned 1 BTC for it (the Q-Day Prize). The keys are still small. But the clock is ticking.

Google just moved its post-quantum migration up to 2029.

Vitalik Buterin (at Devconnect 2025, citing Scott Aaronson) warns crypto needs to be quantum-ready by ~2028.

The biggest heist in history has already begun.

🧵

---

**Tweet 2/10**

Meet QRB — Quantum-Resistance Blockchain.

A Phase 0 project (research + prototype) building a post-quantum L2 on Ethereum.

Not theory: a 24-page whitepaper + a Python prototype with real Dilithium signatures and green CI, already on GitHub.

---

**Tweet 3/10**

Picture the problem:

A Bitcoin transaction in flight. 10 minutes to confirm.

At minute 9, an attacker with a quantum computer derives your private key from your public key (visible on-chain) and drains your wallet.

You thought you paid. No one received anything.

This is the "9-minute attack."

---

**Tweet 4/10**

What almost no one explains: there are TWO quantum threats, not one.

1️⃣ Impersonation → they rob you by signing as you.
2️⃣ Retroactive harvesting → "harvest now, decrypt later." Your encrypted data today is decrypted tomorrow.

Bitcoin and Ethereum face both. Today's "solutions" only cover the first.

---

**Tweet 5/10**

QRB is designed to cover both:

🔐 ML-DSA-65 signatures (NIST 2024) → implemented TODAY in the prototype.
👁️ STARKs + lattice commitments → post-quantum privacy design for Phase 3+.

Why STARKs? Aleo's and Aztec's SNARKs rely on elliptic-curve pairings that do NOT resist a quantum computer. Their privacy protects you today, but not 30 years out. Harvest now, decrypt later.

---

**Tweet 6/10**

Why an L2 on Ethereum and not our own L1?

🔸 Inherits Ethereum's security and liquidity from day 1.
🔸 Any Solidity app migrates without rewriting anything.
🔸 10× cheaper to launch.

A brand-new PQ L1 takes years and dies for lack of validators. A PQ L2 delivers value in months.

---

**Tweet 7/10**

A bonus no one else is doing:
planned integration with QKD (Quantum Key Distribution).

📡 Physical quantum cryptography is already real.

Bennett and Brassard won the ACM Turing Award 2025 (announced March 2026) for their 1984 BB84 protocol.

And it's already deployed in real networks:
🔸 China
🔸 Germany
🔸 MadQCI, Telefónica's network in Madrid (validated in Nature, 2024)

QRB's bet? To be the first blockchain to unite both defenses:
🔹 the mathematical one (PQ)
🔹 the physical one (QKD)

Today it's a documented vision in the whitepaper. Institutional pilot planned for Phase 3+.

---

**Tweet 8/10**

Real status (Phase 0):

✅ Whitepaper v0.2 (PDF, 24 pp)
✅ Python prototype: real Dilithium signatures, tests, green CI on GitHub Actions
✅ Open source, MIT
⏳ What's NOT here yet: EVM, bridge, sequencer. That's Phase 1+, funded by grants.

Looking for: Rust/Go dev (blockchain client), cryptographer (lattices), frontend, technical writer EN/ES.

DMs open.

---

**Tweet 9/10**

Funding philosophy:

1️⃣ Non-dilutive grants (NLNet, @ethereumfndn, Optimism)
2️⃣ A working product + community
3️⃣ Only then a token, registered under MiCA

🚫 No ICO before product.
🚫 No vaporware.
🚫 No promises without code.

Crypto needs more projects built this way.

---

**Tweet 10/10**

📄 Whitepaper v0.2 (English):
https://github.com/Fiyiware/quantum-resistance-blockchain/blob/main/whitepaper/whitepaper-v0.2.en.md

💻 Open-source repo:
https://github.com/Fiyiware/quantum-resistance-blockchain

If you build crypto, if you have keys exposed on-chain, if you care about the post-quantum privacy of your data 30 years out — this is for you.

RT to support.

#PostQuantum #Ethereum #L2 #Cryptography

---

## Publishing notes

- Post in the same 16:00–17:00 Madrid window (morning/midday US crypto Twitter).
- Optional first reply after tweet 10, quote-tweeting the Spanish thread:
  "🇪🇸 Spanish version of this thread here 👉 [link to tweet 1 of the Spanish thread]"
  — this links both audiences and signals the project is bilingual.
- Pin tweet 1 of whichever thread is performing better after 24h.
