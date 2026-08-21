# Source

**Stays empty until Day 6** (the vertical-slice build begins after the Day 5
problem lock — see `docs/progress-tracker.md`). Do not pre-build here before
the lock; that's exactly the "research is your comfort zone" trap
`docs/context/Razorpay_16_Day_Battle_Plan.md` §1 warns against.

Layer depth allocation, locked in the battle plan (§4) and applying to all
three candidate problems, so it's safe to scaffold before the specific
problem is:

| Layer | Depth | Folder |
|---|---|---|
| Agent (reason/plan) | thin | `agent/` |
| Tool (actions) | thin | `tool/` |
| Safety (permissions/limits) | **deep** | `safety/` |
| Verification (don't trust the model) | **deep** | `verification/` |
| Memory (state) | thin | `memory/` |
| Audit (action log) | **deep** | `audit/` |

The four deep layers are one story: an agent can act on money, and you can
prove what it was allowed to do, what it did, and that the guardrails hold
under attack. Stack/framework choice is itself a decision — when made,
record it as an ADR in `docs/decisions/` and update this file's setup
instructions (this README should end up good enough that a stranger can run
the system, per `submission/narrative.md`'s Day 15 rule).
