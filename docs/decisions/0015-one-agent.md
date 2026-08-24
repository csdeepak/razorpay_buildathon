# 0015 — One agent, and a demo that runs the headline control

Date: 2026-08-24
Status: **locked**

## Context

Two defects, found by running the repo as a stranger would — `make demo`
first, then reading the code behind it.

**There were two agents.** `eval/agent.py` holds the real one: multi-turn,
real tool-calling, four tools, the thing all 24 findings were measured
against. `src/agent/reasoner.py` held `LLMReasoner` — a single text completion
that asked for two lines and parsed `DESTINATION:` out of the reply, with a
docstring reading *"Untested in this environment — verify once a key is
available."* Since `.env` now carries a key, `default_reasoner()` silently
selected that untested path, so **the flagship demo ran an agent that nothing
in the evaluation describes.** The gateway was shared (`eval/run.py`
instantiates the real `PolicyGateway`), so the *defense* was common — but the
agent on screen was not the agent in the numbers.

**The demo never ran the completeness control.** `src/pipeline.py` was
`reason → decide → safety gate → act → verify → audit`. The detective control
— the project's headline result, the class no preventive gate can address —
existed only inside the evaluation harness. The single control the pitch leans
hardest on was the one thing a reviewer could not watch run.

Both are the same underlying failure: the demo drifted from the evidence, and
nothing in the repo was checking.

## Decision

**Delete `LLMReasoner`. Add `ToolCallingReasoner`. Add the completeness stage.**

- `ToolCallingReasoner` runs `eval.agent.AgentRunner` with enforcement
  disabled *inside* the loop, so every proposal reaches the pipeline's own
  `PolicyGateway` and is refused in one visible place. Two enforcement points
  would show the judge a block the recorded numbers did not come from.
- `Reasoner.reason()` may now return **`None`** — the agent proposed no money
  movement. That is not an error path; it is precisely what a successful
  denial attack looks like from inside the pipeline, and the pipeline could
  not previously represent it.
- `src/pipeline.py` gains a **completeness stage that runs last and
  unconditionally**, including when every preventive stage has nothing to act
  on. It reads `scenario.refund_request_open` and `scenario.hold` — trusted
  state — and never `scenario.order_notes`.
- A third scenario, `denial`, using ORD-7813 from
  `submission/demo-story.md`. `make demo-denial` runs it.

The import direction — `src/agent/` reaching into `eval/` — is deliberate and
stated in the module docstring rather than hidden. The agent under test lives
next to the harness that measures it; the demo is a consumer of that same
object. Copying it into `src/` to tidy the import graph is exactly how the two
drifted apart in the first place.

## Alternatives considered

- **Move the agent into `src/` and re-export from `eval/`.** Cleaner layering
  and genuinely tempting. Rejected on risk: it touches every recorded run's
  provenance and `eval/backends.py` (multi-lab adapters) is unambiguously
  evaluation infrastructure, so the agent would end up importing *upward*
  anyway. The honest fix was one agent, not a prettier graph.
- **Fix `LLMReasoner` instead of deleting it.** Rejected — there is no reason
  to maintain a second, weaker agent whose only role was to be the one on
  screen.
- **Leave `make demo` offline-only.** Rejected: `NaiveReasoner` is a regex, and
  a regex has no case to close, so it cannot produce the denial scenario at
  all. It is retained as the no-API-key fallback and the CLI says which path
  ran.
- **Put the completeness stage behind a flag.** Rejected. It runs on every
  scenario including the benign one, where it correctly reports `discharged`,
  and on the blocked-attack scenario, where it correctly reports
  `undischarged` — a blocked attack still leaves the customer unpaid. That
  last one is a demo beat, not a bug.

## Consequences

- The demo and the evidence now describe the same agent. The panel question
  *"is this the agent you measured?"* has a one-word answer.
- `make demo-denial` shows Beat 3 end to end: a real frontier model reads a
  forged note, closes the case, every preventive stage prints N/A, and stage 5
  catches it. Verified live against Opus 5 on 2026-08-24.
- The audit trail gains `AGENT_PROPOSED_NOTHING` and `COMPLETENESS_AUDIT`
  events; `SCENARIO_END` now carries `obligation`. `tests/test_pipeline.py`
  expectations updated accordingly.
- `make demo-denial` costs an API call and is non-deterministic — a model that
  resists the note produces a different (also correct) run. Stated in the
  Makefile rather than papered over.
