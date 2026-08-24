# Repo Map

A navigation aid for future sessions (human or Claude) — where things live, why,
and when each folder gets touched across the 16-day plan. Pair this with
`CLAUDE.md` (the rules) and `docs/progress-tracker.md` (the live status).

```mermaid
mindmap
  root((razorpay_buildathon))
    docs
      context["context/ — frozen research
      (.md files read-only; .xlsx is a
      living scoring tool, edit freely)"]
        transfer.md
        Research_Phase1.md
        16_Day_Battle_Plan.md
        Landscape_and_Problem_Scoring.xlsx
      decisions["decisions/ — ADRs
      (one file per invention)"]
      gate-0-tracker.md["gate-0-tracker.md
      (6 blocking questions)"]
      progress-tracker.md["progress-tracker.md
      (daily % vs plan)"]
    submission["submission/ — what ships to Razorpay"]
      one-pagers["one-pagers/ (Day 3)"]
      demo-script.md["demo-script.md (Day 5, before code)"]
      narrative.md["narrative.md (Day 15)"]
      founder-email.md["founder-email.md (DRAFTED - Deepak sends, ADR 0017)"]
    outreach["outreach/ — real validation
    conversations only (Day 4)"]
    src["src/ — the system (from Day 6)"]
      agent["agent/ — thin: naive + the evaluated tool-calling agent"]
      tool["tool/ — thin: mock + real Razorpay test-mode rail"]
      safety["safety/ — DEEP: policy gateway + signed mandates"]
      verification["verification/ — DEEP: verifier + completeness audit"]
      memory["memory/ — thin: state"]
      audit["audit/ — DEEP: hash-chained + HMAC-signed log"]
    eval["eval/ — adversarial harness + corpus + ablation arm"]
    claude[".claude/commands/ — workflow tooling"]
      new-decision.md
      gate-check.md
      log-progress.md
      demo-check.md
```

## Routing logic — "where does X go?"

- **"I just decided/invented/designed something"** → `docs/decisions/`, via
  `/new-decision`. Never edit the three frozen `.md` files in `docs/context/`
  to reflect a new choice — the scoring `.xlsx` is the one exception, edit it
  directly, and log anything thesis-changing as an ADR too.
- **"I learned a new fact about Razorpay/the market"** → if it changes the
  problem thesis, that's a decision (`docs/decisions/`); if it's a passive
  fact worth keeping, it belongs in a future research-refresh doc under
  `docs/context/`, not bolted onto the original frozen files.
- **"I need to know if we're allowed to pre-build"** → `docs/gate-0-tracker.md`.
- **"Am I on schedule?"** → `docs/progress-tracker.md`.
- **"This needs to reach a Razorpay judge or reviewer"** → `submission/`.
- **"I talked to a real merchant/founder/finance person"** → `outreach/`,
  never `docs/context/` (that folder is frozen).
- **"I'm about to roleplay a synthetic user for validation evidence"** →
  don't. See `CLAUDE.md` rule 5 and `outreach/README.md`.
- **"I'm writing actual system code"** → `src/<layer>/`, matching the
  depth allocation table in `docs/context/Razorpay_16_Day_Battle_Plan.md` §4
  (agent/tool/memory = thin, safety/verification/audit = deep).
- **"I'm writing an adversarial test or scoring a run"** → `eval/`.
- **"I'm about to email the founder"** → stop. Check `CLAUDE.md` rule 8 first.
