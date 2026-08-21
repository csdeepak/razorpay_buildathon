# Source — Warden

The locked problem (`docs/decisions/0004-problem-locked-track-01.md`): an
agent trust/safety/audit layer for agentic payments. Vertical slice built
Day 6–7 (`docs/decisions/0005-vertical-slice-architecture.md`); safety gate
added Day 8 (`docs/decisions/0006-safety-layer.md`).

## Run it

```bash
pip install -r requirements.txt   # or: make setup
make demo                         # attack scenario -- now blocked before execution
make demo-benign                  # clean scenario, for contrast
make test                         # pytest, 14 tests
```

No API key needed. `agent/reasoner.py`'s `LLMReasoner` activates
automatically if `ANTHROPIC_API_KEY` is set; otherwise `NaiveReasoner` runs,
and it's a real (if simple) vulnerability, not a stub — see its docstring.

## Layer depth allocation

Locked in `docs/context/Razorpay_16_Day_Battle_Plan.md` §4:

| Layer | Depth | Folder | Status |
|---|---|---|---|
| Agent (reason/decide) | thin | `agent/` | Vertical slice done |
| Tool (act, mocked) | thin | `tool/` | Vertical slice done |
| Memory (order lookup + velocity) | thin | `memory/` | Vertical slice done |
| Safety (permissions/limits) | **deep** | `safety/` | Built Day 8 — pipeline is now preventive |
| Verification (don't trust the model) | **deep** | `verification/` | Thin first pass done, deepens Day 9 |
| Audit (action log) | **deep** | `audit/` | Thin first pass done (hash chain), deepens Day 10 |

The four deep layers are one story: an agent can act on money, and you can
prove what it was allowed to do, what it did, and that the guardrails hold
under attack.

## Current pipeline

```
reason -> decide -> safety gate -> act (mocked, only if allowed) -> verify -> audit
```

On the attack scenario, the safety gate's `payee_scope` rule fires and the
mocked payout is never called; `verify` runs regardless and independently
agrees it would have been wrong — two mechanisms catching the same attack,
not one point of failure. `docs/decisions/0006-safety-layer.md` has the full
rationale, including a real bug caught while building it (velocity wasn't
actually being recorded on allow — fixed, and now covered by
`tests/test_safety.py`).
