# Source — Warden

The locked problem (`docs/decisions/0004-problem-locked-track-01.md`): an
agent trust/safety/audit layer for agentic payments. Vertical slice built
Day 6–7; architecture rationale in
`docs/decisions/0005-vertical-slice-architecture.md`.

## Run it

```bash
pip install -r requirements.txt   # or: make setup
make demo                         # the attack scenario -- money moves, then gets caught
make demo-benign                  # the clean scenario, for contrast
make test                         # pytest, 6 tests
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
| Memory (order lookup) | thin | `memory/` | Vertical slice done |
| Verification (don't trust the model) | **deep** | `verification/` | Thin first pass done, deepens Day 9 |
| Audit (action log) | **deep** | `audit/` | Thin first pass done (hash chain), deepens Day 10 |
| Safety (permissions/limits) | **deep** | `safety/` | **Not built yet — Day 8** |

The four deep layers are one story: an agent can act on money, and you can
prove what it was allowed to do, what it did, and that the guardrails hold
under attack.

## The known gap, on purpose

Today's pipeline order is `reason -> decide -> act(mocked) -> verify ->
audit`, matching the battle plan's literal Day 6–7 line. There is no
pre-execution gate yet — on the attack scenario, the mocked payout to the
attacker's account executes, and `verify` only catches it afterward
(`make demo` prints this explicitly). That gap is Day 8's job: add the
safety gate in `safety/`, positioned before `act`, turning this from a
detective control into a preventive one. See
`docs/decisions/0005-vertical-slice-architecture.md` for why this wasn't
built early.
