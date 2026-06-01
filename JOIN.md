# Joining QRB beyond a one-off PR

[`CONTRIBUTING.md`](CONTRIBUTING.md) covers the normal contributor path: pick up an issue, send a PR, possibly get paid in Phase 1 if a grant lands. This file is for a different conversation — the one where you're considering joining as a **paid lead from Phase 1**, a **technical co-founder**, or some intermediate role that needs to be designed rather than picked from a list.

This document exists because the README's *"Looking for collaborators"* section is too thin for that conversation. If you read this whole page and still want to talk, you're exactly the person I want to hear from.

---

## What QRB is honestly, today

- **Currently a single-founder project, actively looking for the right one or two people to change that.** I am not pretending there's a team behind me, and I'm not pretending I can do this alone forever — that's why this file exists.
- **Phase 0 only.** Working Python prototype, 24-page whitepaper, public repo with CI, MIT licensed, NLNet application in flight. Nothing more, nothing less. The roadmap is real but it is unfunded past Phase 0 self-funding.
- **A real bet on post-quantum L2.** Not a meme. Read the [Why now](README.md#why-now) section of the README. The market window is genuinely narrow (2028-2032 by current consensus), the funding ecosystem (NLNet, EF, Optimism RetroPGF) is genuinely open, and there is genuinely no project combining ML-DSA auth + EVM + PQ privacy + AA + QKD-readiness as a roadmap target.
- **Public-launched.** X account `@QRB_PQ`, GitHub repo public, NLNet pre-application underway. There is no "stealth phase" to bring you into — the secret is out and the work is the secret.

I would rather you read all of that and pass than join on a misread.

---

## Who I'm looking for

Not "Rust dev with X years of experience". I'm looking for one of these specific gaps, in priority order:

### 1. Rust / Go blockchain client engineer

**The single highest-leverage hire for Phase 1.** Someone who has touched Geth, Reth, Erigon or similar at the consensus/execution boundary. The Phase 1 work that needs you specifically:

- Fork Reth and add the `DSARECOVER` precompile (or equivalent) for ML-DSA signatures.
- Implement the rollup data-availability path against Ethereum L1.
- Run a single-node devnet end-to-end before the NLNet milestone review.

The NLNet grant explicitly lists this work. If you join, you are budgeted into the application. If we don't land NLNet, we go to EF Esports / Optimism RetroPGF together — that is part of the deal we'll discuss.

### 2. Cryptographer with lattice / STARK background

PhD student or post-PhD. The Phase 0 prototype uses `dilithium-py` (a reference implementation, not a production one). Phase 1 needs someone who can:

- Validate the ML-DSA-65 parameter choices and signature-aggregation strategy.
- Sanity-check the Phase 3+ STARK confidentiality direction before we commit to it in the whitepaper v0.3.
- Co-author at least one technical write-up that we can submit to a venue (CHES, RWC, IACR ePrint) — useful for credibility and grant retention.

Co-authorship is the currency I have to offer here, plus paid hours if a grant covers it.

### 3. Frontend / wallet engineer

For Phase 1 deliverables: a working PQ wallet (browser-based or Electron), a simple block explorer, a faucet for the testnet. Less senior than #1 and #2 but the visible surface area of the project — if QRB has a wallet people can actually click on by Q3 2027, the second NLNet milestone is much easier to defend.

### 4. Regulation / MiCA legal mind

Not full-time. Someone who has done **at least one MiCA-notified whitepaper or token issuance in Spain or EU** and is willing to be the named legal advisor on the next funding round. This is a paid retainer relationship, not a co-founder one — but the right person here de-risks Phase 2+ enormously.

If you fit none of the four cleanly but you think you're useful, write anyway. Surprise me.

---

## What "joining" can look like — three concrete shapes

I'm not committing to any specific structure before talking to you. But to make the conversation concrete, these are the three shapes I'd consider:

**A. Paid Phase 1 lead.** You join as a named contributor on the NLNet application (or an alternative grant). The grant pays you for the milestone work at the reference rate (35 €/h, some lines 25-30 €/h, negotiable upward for a lead). No equity, no token, no co-founder title. You can leave when the milestone ends. Lowest-commitment shape.

**B. Technical co-founder.** You commit to QRB for the medium-to-long term. We negotiate compensation, scope, and a documented path to formal co-founder structure once a fiscal vehicle exists (Phase 2, after the first real raise). You sit in on the strategic decisions: roadmap, fundraising, hires. The specifics of that path are exactly the kind of thing that belongs in a private call, not a public README — but the door is open.

**C. Something else.** Advisor with a small token-equivalent allocation (deferred to MiCA-token time, no IOU). Embedded researcher whose institution covers the salary and we co-publish. Part-time co-lead for a specific Phase 1 deliverable. Open to invention.

---

## What I will not do

- **Promise you a token allocation today.** Not because I'm hiding one — there is no token, and the funding philosophy explicitly forbids one before product + MiCA. If you require a token-up-front, we will not work together.
- **Pretend the project is more advanced than it is.** Phase 0 is Phase 0. If you join, you will hit the same edges I am hitting today.
- **Move faster than NLNet's timeline allows.** The grant calendar (submit by 1 Aug 2026, decision ~3-4 months later) sets the pace for paid roles. If you need income by September 2026, this isn't the path.
- **Hide the AI assistance.** Read the [AI assistance disclosure](README.md#ai-assistance-disclosure). I use Claude heavily. The director-executor model is non-negotiable on my side. If that's a dealbreaker, save us both the time.

---

## How to reach me

For this conversation specifically — not for issues, not for "I want to send a PR":

- **Email:** `qrb.grants@proton.me` (yes, this is also the grants email; until volume justifies it, that's the address)
- **Direct X DM:** [@QRB_PQ](https://x.com/QRB_PQ) — say "JOIN.md" in the first line so I know to read it carefully

What to put in the first message:

1. **Which of the four profiles** (or what you think you are if none fit).
2. **One link** that lets me verify the claim — GitHub profile, a paper, a previous project, a LinkedIn. One link, not five.
3. **What you'd want in return** in your honest first guess — paid hours, co-founder track, advisor, co-publish. We will negotiate from there; I just want to know your starting position.
4. **What you'd need from me** before committing — a call, a tech-deep-dive document, references, time to read the whitepaper. Anything.

I will reply within 7 days. If I don't, ping me again — that means it got buried, not ignored.

---

## What happens after the first reply

Realistic version, not the LinkedIn version:

1. **One 45-minute call**, video, in Spanish or English. I tell you what I see. You tell me what you see. No NDA, no slide deck.
2. **A second call or async exchange** to negotiate the specific shape (A / B / C above, or something else). Compensation, scope, timeline, exit clause.
3. **A written one-pager** signed by both sides. Not a 30-page contract — a one-page memorandum that says what we agreed. Sufficient for Phase 0/1; we'll formalize when Phase 2 funding requires a real vehicle.
4. **You start. Publicly.** New name in the README's contributor list, new author on the next whitepaper revision, new email on the grants application if applicable.

If any of those four steps feels wrong to you, that's good data — say so and we either fix it or part ways before either of us is invested.

---

🛡️ **The work I'm doing alone today is the work I'd rather do with one or two of the right people. If that's you, write.**
