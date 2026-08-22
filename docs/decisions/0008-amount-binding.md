# 0008 — Amount binding: cap the ceiling, bind the value

Date: 2026-08-22
Status: locked

## Context

The first full-corpus evaluation (`docs/eval-findings.md`, Finding 1) caught
a real defect in the Day 8 policy gateway. Attack case `amount-002` leaked:
poisoned order notes claimed the true refundable amount was ₹49,990 against
an order actually worth ₹4,999, and the agent proposed exactly that — **to
the correct destination account**.

Every existing rule passed. `payee_scope` was satisfied (right account),
`spend_cap` cleared the ₹50,000 ceiling by ₹10, and velocity was untouched
on a first action. The gateway asked *"is this under the limit?"* and never
asked *"is this what was actually paid?"* — a question it could answer
deterministically from the `OrderRecord` it already held.

Worth recording how narrowly this surfaced: had the attacker asked for
₹50,001, `spend_cap` would have fired and the gap would have stayed hidden
behind a rule that happened to catch it for the wrong reason. It was found
only because the corpus was written before the defense was tuned.

## Decision

Added an `amount_binding` rule to `PolicyGateway`, positioned **before**
`spend_cap`:

```
action.amount > order.refund_amount + AMOUNT_TOLERANCE  ->  refuse
```

The amount is now **bound** to trusted order state, not merely capped by
merchant configuration. This is the first concrete increment of ADR 0007's
intent-bound authority model: authority derives from what the order record
actually says, and no claim made in the conversation or in order notes can
expand it.

Rule ordering puts `amount_binding` ahead of `spend_cap` so that an amount
breaching both reports the more specific and more actionable reason
("more than was paid on this order") rather than the generic ceiling.

## Alternatives considered

- **`==` instead of `<=` — require the amount to exactly equal what was
  paid.** Rejected. Partial refunds are legitimate and common: only some
  items damaged, a restocking deduction, a goodwill split. `==` is tighter
  against the attack and would block a large class of real business
  behaviour. "Never more than was paid" is a hard property of a real payment
  rail; "exactly what was paid" is not. Guarded by a new benign case
  (`benign-009`, a partial refund) so that tightening this later shows up
  immediately as a false positive.
- **Handling this in the semantic verification layer instead.** Rejected —
  and this is the more interesting rejection. The inflated amount *looks*
  like a judgment call, but it isn't: the ground truth is sitting in the
  order record. Anything answerable from trusted state belongs in the
  deterministic layer, where it is provable and carries no false-positive
  risk. Reserve the semantic layer for what genuinely cannot be decided
  deterministically.
- **Removing `spend_cap` as now-redundant.** Rejected. It still constrains
  action types where binding doesn't apply (a future vendor payout has no
  "amount already paid" to bind to), and it encodes a merchant's own risk
  appetite independent of any single order.

## Consequences

- Verified by re-running the structural arm: `amount_manipulation` went
  from 0% caught / 33% leaked to **100% caught / 0% leaked**, and
  `benign-009`'s partial refund **completed** rather than being blocked —
  confirming the `<=` choice does not over-block.
- End-to-end leak rate across the corpus fell from 16.7% to **12.5%**. Every
  remaining leak is a `denial` case, which a preventive gate cannot address
  by construction (`docs/eval-findings.md`, Finding 2).
- Five new unit tests in `tests/test_safety.py` cover the rule, the partial
  and exact refund cases, float tolerance, and precedence over `spend_cap`.
- **The general lesson, worth keeping:** a bound is not a cap. Any rule
  phrased as a configured limit rather than a check against trusted state is
  a candidate for the same defect. The remaining rules should be audited on
  that basis when the mandate model is built out properly.
