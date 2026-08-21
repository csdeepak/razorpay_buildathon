---
description: Report where the project stands against the 16-day plan's gates, and flag any rule violation
---

Audit current status against `docs/progress-tracker.md` and
`docs/context/Razorpay_16_Day_Battle_Plan.md`:

1. Read `docs/gate-0-tracker.md` — if any of the six questions are still
   unchecked, say so first; that's the standing blocker for everything else.
2. Read `docs/progress-tracker.md` — identify the current day/phase, whether
   the most recent gate was hit, and whether the log has a same-day or
   stale entry.
3. Check `docs/decisions/` for whether a problem-lock ADR exists. If today's
   date is past Day 5 of the plan (day 1 = 2026-08-20) and no lock ADR
   exists, flag it explicitly — that's rule 1 in `CLAUDE.md` at risk.
4. Skim `submission/demo-script.md` — if `src/` has any real code but the
   script is still the empty template, flag it (rule 2: no feature outside
   the demo script).
5. Report back concisely: what gate we're at, what's done, what's the single
   next blocking action, and any rule from `CLAUDE.md` currently at risk.
   Don't restate the whole plan — the user has read it.
