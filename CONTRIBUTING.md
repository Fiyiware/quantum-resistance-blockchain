# Contributing to QRB

Thanks for stopping by. This document tells you, plainly, **what contributing to QRB looks like today** and what it will look like in Phase 1 — so you can decide whether it's worth your time.

If you are weighing whether to join as a paid contributor or as a co-founder rather than send the occasional PR, read [JOIN.md](JOIN.md) instead — it's a different conversation.

---

## Where the project is right now

QRB is in **Phase 0 — Validation** (see the [roadmap in the README](README.md#roadmap)). That means:

- **Single founder** (Luiggi Leonel Cedeño Bermeo). No team yet, no paid contributors.
- **Working Python prototype**, **whitepaper v0.2**, **CI on every push**. That's it.
- **No paid track today.** Phase 1 contributions will be paid out of the [NLNet NGI Assure](grants/nlnet-assure-application-draft.md) grant we're submitting before 1 August 2026 (€50K over 6 months, milestone-released). That money does not exist yet. If you contribute today, you are contributing for free.
- **No token.** Not now, not in Phase 0, not in Phase 1. Read the [funding philosophy in the README](README.md#funding-philosophy). If you came looking for an allocation, this is not the project.

If that's still interesting to you, keep reading.

---

## How to contribute today

In order of "useful but low-effort" → "useful and high-effort":

### 1. Read the whitepaper and push back

`whitepaper/whitepaper-v0.2.pdf` (24 pages, Spanish). Open an issue with the label `feedback` for anything that smells wrong — a citation that doesn't check out, a quantum-resource claim that's off, an EVM-compatibility decision that ignores a known constraint, a MiCA reading you disagree with. The first external reviewer is in the README's Acknowledgments for a reason: substantive critique is the most valuable thing you can give Phase 0.

### 2. Run the prototype and break it

Follow the [Quick start in the README](README.md#quick-start--run-the-prototype). If a test fails on your platform, if the CLI behaves oddly, if persistence is corrupt after a crash — file an issue with the label `bug`, include your OS, Python version, exact commands, and the output. Even better: open a PR with a regression test that captures the bug.

### 3. Pick up a `good-first-issue`

Issues tagged [`good-first-issue`](https://github.com/Fiyiware/quantum-resistance-blockchain/labels/good-first-issue) are scoped to be doable in a few hours by someone who has read the prototype. They exist precisely so a new contributor can land a first PR without negotiating scope.

If none are open at the moment, that means I haven't backfilled the list — ping me on the [QRB Discussions](https://github.com/Fiyiware/quantum-resistance-blockchain/discussions) board (or DM [@QRB_PQ](https://x.com/QRB_PQ)) and I'll prioritize creating them.

### 4. Propose a non-trivial change

For anything larger than a `good-first-issue` — a new test suite, a refactor of the storage layer, a port of a helper to Rust as a precursor to the Reth fork — **open an issue first** describing what you want to build and why. I'd rather spend 20 minutes aligning before you spend a weekend on a PR I can't merge.

### 5. Documentation, translation, examples

The whitepaper is Spanish-only. A faithful English translation is on the wish list. So is a public block-explorer-style "tour" of a freshly-mined QRB block (showing the ML-DSA-65 signature, the state diff, the chain pointer). These are tagged `docs` and `examples`.

---

## How to run the tests

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

All tests must pass locally before you open a PR. CI runs the same tests on Python 3.10, 3.11 and 3.12 on every push — your PR will be blocked if any of those fail.

---

## Conventions

### Commits

- Imperative mood, present tense: *"Add proposer-impersonation test"*, not *"Added"* or *"Adds"*.
- One logical change per commit. If your PR has 12 commits of `wip`, squash before requesting review.
- If the commit closes an issue, end the body with `Closes #N`.

### Branches

- Branch off `main`.
- Name: `kind/short-slug`, where `kind` is one of `fix`, `feat`, `docs`, `test`, `chore`, `grants`. Examples: `fix/storage-corruption-on-crash`, `feat/cli-block-export`, `docs/translate-readme-en`.
- Open the PR against `main`. There is no `develop` branch.

### Pull requests

- **Small.** Under ~300 lines diff is the target. Bigger PRs are fine if the change is genuinely atomic (a refactor that can't be split) — but say so in the description.
- **Tested.** New behavior needs a new test. Bug fix needs a regression test. No exceptions.
- **Described.** Use the PR template. Two sentences on *what* and *why* is plenty if the code is clear; more is fine if it isn't.
- **Honest about status.** If the PR introduces something that's *designed* but not *implemented*, label it as such in the description — match the discipline of the README's Status table.

### Code style

Python: stdlib + `dilithium-py` only for the prototype core. No new dependencies without an issue first. Format with `black` (default config), lint with `ruff` (default config). The CI does not enforce these yet, but it will.

### What I will reject

- PRs that expand scope without an issue.
- PRs that add a dependency without discussion.
- PRs that change wording in the README or whitepaper to make claims stronger than the evidence supports. The Status table discipline is load-bearing.
- PRs that introduce features explicitly marked Phase 2+ or Phase 3+ in the whitepaper. We're not building those yet.

---

## Review process

- I (founder) am the only reviewer today. I aim to respond within 72 hours; if your PR sits longer than that, ping the issue or DM me.
- A PR merges when: CI is green, the description is clear, and I've left at least one approving review. There is no second reviewer to wait for in Phase 0.
- Disagreement is fine and welcome. If I push back on a PR and you think I'm wrong, say so on the PR. I have changed my mind on the README, the whitepaper, and the prototype scope in the past three weeks based on external critique — keep the receipts: commits `b0f551b` and `6e11eeb`.

---

## Compensation, honestly

| When | What | Source |
|---|---|---|
| **Today, Phase 0** | €0. Open source, MIT, no implicit IOU. | — |
| **Phase 1, if NLNet funds us** | Paid work for the contributors who join the milestone deliverables. Reference rate **35 €/h** (some lines 25-30 €/h). | NLNet NGI Assure grant — see [grants/nlnet-assure-application-draft.md](grants/nlnet-assure-application-draft.md) |
| **Phase 2+** | Decided later. Possibly a seed round, possibly a MiCA-compliant token process, possibly more grants. No promises today. | — |

If you do meaningful Phase 0 work and we get the NLNet grant, **you go to the top of the list** for paid Phase 1 work. That's not a contract — I can't make that legally binding from a free contribution — but it's the honest version.

If you want to talk about anything beyond that (a paid role from day one, co-founder track, dedicated milestone), read [JOIN.md](JOIN.md).

---

## Code of conduct

Be direct, be kind, be technically honest. No personal attacks, no harassment, no bad-faith engagement. Disagreement on technical or strategic decisions is welcome and expected — disagreement about whether someone deserves to be in the room is not.

If something happens that needs handling privately, email `qrb.grants@proton.me` (until we have a dedicated address).

---

## Asking questions

- **Code, prototype, tests** → [GitHub Issues](https://github.com/Fiyiware/quantum-resistance-blockchain/issues).
- **Roadmap, strategy, "should I build X?"** → [GitHub Discussions](https://github.com/Fiyiware/quantum-resistance-blockchain/discussions).
- **Quick public ping** → [@QRB_PQ on X](https://x.com/QRB_PQ).
- **Private, serious, not-just-a-PR** → see [JOIN.md](JOIN.md).

Thanks for reading this far. That's already more than most people do — and it's exactly the kind of attention this project needs.
