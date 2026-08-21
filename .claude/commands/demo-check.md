---
description: Cross-check src/ against submission/demo-script.md for scope drift in either direction
---

Enforce `CLAUDE.md` rule 2 ("no feature that isn't in the demo script") and
rule 7 (no "because ASMOS has it" scope creep):

1. Read `submission/demo-script.md` and extract the concrete beats/features
   it names.
2. Look through `src/` (skip the placeholder READMEs) for what's actually
   implemented.
3. Report two lists:
   - Features in the demo script with no corresponding implementation yet —
     expected before Day 14, but worth surfacing if the gap looks large for
     where we are on `docs/progress-tracker.md`.
   - Implemented code with no corresponding beat in the demo script — this
     is the violation to flag hard. Ask whether it should be cut, or whether
     the demo script is stale and needs updating (and if so, that's worth an
     ADR if it reflects a real design change).
4. Do not silently fix either direction — this command reports, it doesn't edit.
