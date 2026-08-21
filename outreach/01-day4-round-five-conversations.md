# Day 4 — Round 1: Five Real Conversations

Date: 2026-08-21 (Day 4 work, done ahead of the Day 5 24 Aug baseline).
Satisfies the plan's "3–5 real conversations" quota for Gate 2.

Reported by Deepak as reactions from five real people, each pitched all
three surviving candidates from `submission/one-pagers/`. This is a compact
scorecard, not full transcripts — if any of these conversations produced a
specific objection, quote, or "actually the real problem is X" moment worth
preserving for the narrative (`submission/narrative.md`) or the demo script,
add it under the relevant row below rather than losing it.

| Person | 01 — Agent Trust/Safety/Audit | 02 — Invoice Fraud Detector | 04 — Settlement Forensics |
|---|---:|---:|---:|
| Startup founder | 🟢 | 🔥 | 🟢 |
| Finance/CFO | 🔥 | 🔥 | 🔥🔥 |
| D2C merchant | 🟡 | 🔥🔥🔥 | 🟢/🔥 |
| Security engineer | 🔥🔥🔥🔥🔥 | 🟢 | 🟡 |
| Razorpay product/AI | 🔥🔥🔥🔥🔥 | 🟡 | 🔥🔥🔥 |
| **Overall** | **🔥🔥🔥🔥🔥** | **🔥🔥🔥** | **🔥🔥🔥** |

## What this actually says

- **Track 01 polarizes by audience, and it polarizes in the right
  direction.** The two respondents most predictive of Buildathon
  judging — a security engineer (technical rigor) and a Razorpay
  product/AI person (closest available proxy for an actual judge) — both
  gave it the maximum reaction, unprompted, independently. The two weakest
  reactions (D2C merchant 🟡, startup founder 🟢) are from the audiences
  least likely to be in the room when this gets judged.
- **That same D2C-merchant/founder lukewarmness is the abstract-demo risk
  already named in `submission/one-pagers/01-agent-trust-safety-audit-layer.md`**,
  now with real evidence behind it instead of a hunch: a merchant does not
  feel "an agent could get hijacked" as a visceral, current pain the way a
  security engineer does. This doesn't kill the candidate — it says the
  demo has to carry the visceral weight (the attack caught on screen), not
  the pitch.
- **Track 02 (invoice fraud) is a genuine D2C-merchant favorite** (🔥🔥🔥,
  its single strongest reaction of the whole table) but flat with the two
  most judge-relevant respondents. Consistent with its one-pager's own
  flagged risk: real pain for one audience, unclear AI-judgment story for
  the room that's actually scoring this.
- **Track 04 (settlement forensics) got its strongest reaction from the
  CFO** (🔥🔥, higher than that same CFO gave Track 01) plus a strong second
  read from Razorpay product/AI (🔥🔥🔥). Worth keeping in reserve exactly as
  named in `docs/decisions/0003-cut-to-three.md` — if Track 01 runs into
  trouble, this is not a cold fallback, it has real independent pull.

## Next

See `docs/progress-tracker.md` for Gate 2 status and whether this round is
being treated as sufficient to lock.
