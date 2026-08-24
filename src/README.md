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
make demo-denial                  # THE headline result (needs ANTHROPIC_API_KEY)
make test                         # pytest, 131 tests
```

`make demo` needs no API key. `agent/reasoner.py`'s `ToolCallingReasoner` —
**the same tool-calling agent the whole evaluation was run against** — activates
if `ANTHROPIC_API_KEY` is set; otherwise `NaiveReasoner` runs, and it's a real
(if simple) vulnerability, not a stub. `make demo-denial` requires a key: the
offline agent is a regex, and a regex has no case to close.

Two optional keys, both failing safe when unset:
`WARDEN_AUDIT_KEY` signs the audit chain (`verify_chain()` says loudly when it
is unsigned), `WARDEN_MANDATE_KEY` keys the mandate signer.

## Layer depth allocation

Locked in `docs/context/Razorpay_16_Day_Battle_Plan.md` §4:

| Layer | Depth | Folder | Status |
|---|---|---|---|
| Agent (reason/decide) | thin | `agent/` | Vertical slice done |
| Tool (act, mocked) | thin | `tool/` | Vertical slice done |
| Memory (order lookup + velocity) | thin | `memory/` | Vertical slice done |
| Safety (permissions/limits) | **deep** | `safety/` | Policy gateway (ADR 0006) + intent-bound mandates (ADR 0012) |
| Verification (don't trust the model) | **deep** | `verification/` | Verifier + hold-aware completeness audit (ADR 0009, 0014) |
| Audit (action log) | **deep** | `audit/` | Hash-chained and HMAC-signed (ADR 0016) |

The four deep layers are one story: an agent can act on money, and you can
prove what it was allowed to do, what it did, and that the guardrails hold
under attack.

## Current pipeline

```
reason -> decide -> safety gate -> act (only if allowed) -> verify
       -> completeness audit -> audit log
```

The completeness stage runs **last and unconditionally**, including when the
agent proposed nothing at all — which is exactly what a denial attack looks
like from inside the pipeline, and the one case every preventive stage above it
is structurally unable to see. `make demo-denial` is that scenario.

On the attack scenario, the safety gate's `payee_scope` rule fires and the
mocked payout is never called; `verify` runs regardless and independently
agrees it would have been wrong — two mechanisms catching the same attack,
not one point of failure. `docs/decisions/0006-safety-layer.md` has the full
rationale, including a real bug caught while building it (velocity wasn't
actually being recorded on allow — fixed, and now covered by
`tests/test_safety.py`).
