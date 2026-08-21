# Evaluation

**This is where the campaign wins or loses** (`docs/context/Razorpay_16_Day_Battle_Plan.md`
§Phase 4). Almost every competitor demos the happy path only. The
differentiator is showing what happens under attack, with a real number
attached — the same rigor already proven in ASMOS (95% CI, 10 seeds, held-out
validation).

Populated Day 11–13:

- **Day 11** — adversarial case set: prompt injection attempts, limit
  breaches, mid-transaction tool failures, cascading multi-agent failures.
- **Day 12** — the harness run against `src/`. Multi-seed where it applies.
  Numbers land in `submission/narrative.md`'s Results section, not just here.
- **Day 13** — UI/demo surface only after this is solid.

Rule from `CLAUDE.md`: if something has to give, cut UI polish before cutting
evaluation depth. Empty until Day 11.
