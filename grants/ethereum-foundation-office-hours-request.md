# EF ESP — Office Hours request (ready to paste)

> **What this is**: text for the EF ESP **Office Hours** request form
> (https://esp.ethereum.foundation → Office Hours). Office Hours is a short, informal
> 20-minute call for **non-financial guidance** — *not* a funding application and *not* a
> pitch. So this message asks for **alignment guidance**, not money.
>
> **Hard rules from EF's own page (do not break):**
> - Do **not** ask for financial support or pitch for funding here.
> - Do **not** mention tokens at all (EF explicitly does not engage with token topics;
>   QRB has no token anyway — keep it out entirely).
> - Do **not** ask for wallet/transaction/exchange help.
> - **Be specific** about what you need — that is what makes the call useful.
>
> **Goal of the call**: get a steer on whether QRB's post-quantum work fits a current
> Wishlist/RFP item (and which), and avoid duplicating any EF post-quantum effort —
> *before* investing in the Reth fork.

---

## Message (paste into the "what do you need / context" field)

**Context — what I'm working on**

QRB is an open-source project (MIT/Apache-2.0) building post-quantum cryptographic
building blocks for Ethereum. I have a working proof of concept: an `MLDSAVERIFY` EVM
precompile that verifies NIST FIPS 204 ML-DSA-65 signatures, wrapped as a `revm`
precompile and exercised **end-to-end** — a real transaction that calls the precompile
runs through a full `revm` EVM and returns the expected result. My next step is a
post-quantum ERC-4337 smart account that uses it, built in a Reth fork, with a published
gas-cost model. The intent is to upstream the precompile (EIP + Reth PR) as a public good,
not to keep it siloed. Repo: https://github.com/Fiyiware/quantum-resistance-blockchain

**What I'd like guidance on**

1. **Alignment** — does this kind of work (an upstreamable ML-DSA precompile + a PQ
   account-abstraction account) fit a current Wishlist or RFP item? If so, which one
   should I aim at?
2. **Avoiding duplication** — are there EF teams or projects already working on
   post-quantum signature verification in the EVM or clients that I should coordinate
   with rather than duplicate?
3. **Approach** — is forking Reth and proposing the precompile as an EIP the right venue,
   or would you suggest a different path?

I'm a solo founder at the proof-of-concept stage, and before I scale the work up I mainly
want to make sure I'm pointing my effort where it's genuinely useful to Ethereum.

---

## After the call (internal notes — fill in)

- Which Wishlist/RFP item they pointed to (name + URL): …
- EF teams / projects to coordinate with: …
- Their view on the Reth-fork + EIP approach: …
- Recommended next step (apply to item X / Academic Grants / other): …
