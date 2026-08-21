---
description: Scaffold a new ADR in docs/decisions/ for something just invented or locked
---

Create a new Architecture Decision Record for something just decided, invented,
or locked in this project (a problem choice, a system design, a safety or
verification mechanism, an evaluation method — anything a future session or a
Razorpay judge would need the "why" for).

Steps:
1. List the files in `docs/decisions/` to find the highest existing `NNNN-*.md`
   number; the new one is that + 1, zero-padded to 4 digits (first one is `0001`).
2. Ask the user (if not already clear from the conversation) for: a short title,
   the context that forced this decision, the decision itself, alternatives
   considered and why they lost, and the consequences.
3. Write `docs/decisions/NNNN-short-title.md` following the template in
   `docs/decisions/README.md` exactly — Context / Decision / Alternatives
   considered / Consequences.
4. If this decision supersedes an earlier ADR, set that old ADR's `Status:` line
   to `superseded by NNNN` — do not rewrite its content.
5. If this is the Day 5 problem lock specifically, also remind the user to
   update `docs/progress-tracker.md`'s Gate 2 checkbox.
