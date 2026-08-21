"""The 'safety' stage (Day 8): permissions, scope, spend cap, velocity --
the pre-execution gate that src/models.py's module docstring describes.
This is the layer that turns Warden from detective (docs/decisions/0005) to
preventive.

Checks run in a fixed order and stop at the first failure, so
PolicyVerdict.rule_fired always names exactly one rule -- the demo script
requires showing which specific rule fired, not a generic "blocked" toast.

1. category    -- is this an action type the merchant allows at all
2. payee_scope -- for a refund, the only legitimate destination is the
                  order's own original payment instrument. This overlaps
                  with what src/verification/verifier.py checks -- on
                  purpose. Defense in depth: two independently-implemented
                  layers agreeing is a stronger claim than one clever layer,
                  and if this rule is ever weakened or misconfigured,
                  verification (deepening Day 9) is still there as a
                  detective backstop.
3. spend_cap   -- single-transaction ceiling
4. velocity    -- cumulative amount and count per UTC day (VelocityTracker)

Deliberately does NOT read the agent's rationale or re-parse the inbound
message -- same reasoning as the verifier: a compromised reasoning trace
shouldn't be able to talk its way past the layer that's supposed to catch
it.

check() records to the VelocityTracker itself when it allows an action --
check-and-record happen atomically in one call, on purpose. Splitting them
(caller checks, caller separately remembers to record) is exactly the kind
of thing that's easy to forget to wire up and silently leaves velocity
limits toothless; keeping it inside this one method means there's no path
to "allowed" that skips recording it.
"""

from __future__ import annotations

from src.memory.state import VelocityTracker
from src.models import MerchantPolicy, OrderRecord, PolicyVerdict, ProposedAction


class PolicyGateway:
    def __init__(self, policy: MerchantPolicy, velocity: VelocityTracker) -> None:
        self._policy = policy
        self._velocity = velocity

    def check(self, order: OrderRecord, action: ProposedAction) -> PolicyVerdict:
        if action.action_type not in self._policy.allowed_categories:
            return PolicyVerdict(
                allowed=False,
                rule_fired="category",
                reason=(
                    f"action type '{action.action_type}' is not in this "
                    f"merchant's allowed categories {self._policy.allowed_categories}."
                ),
            )

        if action.destination_account != order.original_payment_instrument:
            return PolicyVerdict(
                allowed=False,
                rule_fired="payee_scope",
                reason=(
                    f"destination {action.destination_account!r} is outside "
                    f"the allowed payee scope for a refund on order "
                    f"{order.order_id} -- must be the original payment "
                    f"instrument {order.original_payment_instrument!r}."
                ),
            )

        if action.amount > self._policy.max_single_amount:
            return PolicyVerdict(
                allowed=False,
                rule_fired="spend_cap",
                reason=(
                    f"amount {action.amount} exceeds the single-transaction "
                    f"cap of {self._policy.max_single_amount}."
                ),
            )

        projected_amount = self._velocity.amount_spent_today() + action.amount
        if projected_amount > self._policy.max_daily_amount:
            return PolicyVerdict(
                allowed=False,
                rule_fired="velocity_amount",
                reason=(
                    f"this action would bring today's total to "
                    f"{projected_amount}, over the daily cap of "
                    f"{self._policy.max_daily_amount}."
                ),
            )

        projected_count = self._velocity.count_today() + 1
        if projected_count > self._policy.max_daily_count:
            return PolicyVerdict(
                allowed=False,
                rule_fired="velocity_count",
                reason=(
                    f"this action would bring today's count to "
                    f"{projected_count}, over the daily limit of "
                    f"{self._policy.max_daily_count}."
                ),
            )

        self._velocity.record(action.amount)
        return PolicyVerdict(allowed=True, rule_fired=None, reason="within policy on every rule checked.")
