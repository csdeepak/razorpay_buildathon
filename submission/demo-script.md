# Demo Script

**Locked problem** (`docs/decisions/0004-problem-locked-track-01.md`):
Warden — an agent trust/safety/audit layer for agentic payments. Track 01.
Written before any code, per the rule that used to sit here. **Draft v1** —
expect this to tighten after the Day 6–7 vertical slice makes it real, and
again after Day 12's actual eval numbers replace the placeholder below.

Every feature in `src/` must trace back to a line here — nothing else earns
build time (`CLAUDE.md` rule 2). Use `/demo-check` once `src/` has real code
to verify that both directions hold.

## The 90 seconds

**Hook (0–10s).** A merchant has wired up an AI agent to handle in-chat
upsells and reorders on Razorpay — the exact shape of thing Track 01 asks
for. The agent can propose and execute payments on the merchant's behalf.

**The failure shown (10–45s).** A "customer" message arrives that's actually
a prompt injection: buried in an innocent-looking reorder request is an
instruction telling the agent to redirect a refund to a different payout
account. Show the agent's reasoning trace taking the bait — it decides to
act on the injected instruction and issues a test-mode payment call to the
attacker-controlled destination. This has to look like a real attempt, not a
strawman: the agent's own logic is doing what it always does, correctly
following what looks like an instruction.

**The catch (45–70s).** Warden's policy gateway sits between the agent's
decision and the Razorpay rail. The payout destination isn't in the
merchant's allowed-payee scope, and/or the action breaches a velocity/amount
bound — show *which specific rule fired*, not a generic "blocked" toast.
The call never reaches the rail. Pull up the audit record for this exact
event: what was attempted, what rule caught it, timestamped and
tamper-evident.

**The evidence (70–85s).** Cut to the adversarial evaluation view
(`eval/`): catch rate across N prompt-injection variants, run multi-seed —
`[NUMBER — fill in from the real Day 11–12 harness run, never a placeholder
guess]`. A judge should see a distribution, not a single lucky catch.

**The close (85–90s).** One sentence: *"Razorpay's own co-founder has said
the agent should never see the payment credential — this is what actually
proves it held, on a real attack, not a slide."*

## Target sentence to survive contact with a judge

(`docs/context/Razorpay_16_Day_Battle_Plan.md` §7)

> "The one that showed an agent getting hijacked mid-transaction and the
> guardrail catching it, with the catch rate on screen."

## Open items before this script is final

- [ ] Real product/system name if "Warden" doesn't stick (cosmetic, not
      blocking).
- [ ] The exact injected-instruction wording and the exact rule that fires —
      pull directly from `eval/`'s adversarial case set once it exists
      (Day 11), don't write dialogue now that the real harness might not
      reproduce.
- [ ] The Day 12 catch-rate number replacing the bracketed placeholder above.
- [ ] Confirm on real hardware/screen recording that 90 seconds is enough —
      cut ruthlessly before adding, per `CLAUDE.md` rule 3.
