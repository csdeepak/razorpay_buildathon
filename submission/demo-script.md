# Demo Script

**Do not fill this in until the Day 5 problem lock (Gate 2) is recorded as an
ADR in `docs/decisions/`.** Writing this before code is not a formality — if
90 compelling seconds can't be scripted here, the project is wrong, and Day 5
is a cheap day to learn that. Day 14 is not.

Every feature that ends up in `src/` must trace back to a line in this
script. Nothing else earns build time (`CLAUDE.md` rule 2).

## Template

- **Hook (0–10s):** the scenario, stated so a non-technical judge gets it
  immediately.
- **The failure shown (10–45s):** the agent gets hijacked / breaches a limit
  / is asked to do something it shouldn't — show it happening.
- **The catch (45–70s):** the system catches it. Show the mechanism, not just
  a green checkmark — what specifically fired, and why.
- **The evidence (70–85s):** the number. Catch rate across N adversarial
  cases, not a single staged run.
- **The close (85–90s):** why this matters to Razorpay specifically, in one
  sentence a judge could repeat back an hour later.

Target sentence to survive contact with a judge (see
`docs/context/Razorpay_16_Day_Battle_Plan.md` §7):

> "The one that showed an agent getting hijacked mid-transaction and the
> guardrail catching it, with the catch rate on screen."
