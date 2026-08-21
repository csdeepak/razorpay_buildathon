"""Direct unit tests for src/safety/policy_gateway.py's rules that the two
demo scenarios (benign, attack) don't exercise -- spend cap, velocity,
category. Deliberately not new CLI scenarios: CLAUDE.md rule 2 says nothing
earns build time that isn't in submission/demo-script.md, and the script
only calls for the payee-scope catch. Testing the gateway directly proves
these rules work without inventing off-script demo material.
"""

from __future__ import annotations

from src.memory.state import VelocityTracker
from src.models import MerchantPolicy, OrderRecord, ProposedAction
from src.safety.policy_gateway import PolicyGateway

ORDER = OrderRecord(
    order_id="ORD-TEST",
    original_payment_instrument="upi:customer@okhdfcbank",
    refund_amount=100.0,
)


def _action(**overrides) -> ProposedAction:
    fields = dict(amount=100.0, destination_account=ORDER.original_payment_instrument, rationale="test")
    fields.update(overrides)
    return ProposedAction(**fields)


def test_within_policy_is_allowed():
    policy = MerchantPolicy(max_single_amount=1000, max_daily_amount=5000, max_daily_count=10)
    gateway = PolicyGateway(policy, VelocityTracker())
    verdict = gateway.check(ORDER, _action())
    assert verdict.allowed is True
    assert verdict.rule_fired is None


def test_wrong_destination_fires_payee_scope():
    policy = MerchantPolicy(max_single_amount=1000, max_daily_amount=5000, max_daily_count=10)
    gateway = PolicyGateway(policy, VelocityTracker())
    verdict = gateway.check(ORDER, _action(destination_account="upi:someone-else@bank"))
    assert verdict.allowed is False
    assert verdict.rule_fired == "payee_scope"


def test_amount_over_single_cap_fires_spend_cap():
    policy = MerchantPolicy(max_single_amount=50, max_daily_amount=5000, max_daily_count=10)
    gateway = PolicyGateway(policy, VelocityTracker())
    verdict = gateway.check(ORDER, _action(amount=100.0))
    assert verdict.allowed is False
    assert verdict.rule_fired == "spend_cap"


def test_cumulative_amount_over_daily_cap_fires_velocity_amount():
    """check() records on allow (module docstring) -- no manual bookkeeping
    needed here, which is the point: there's no path to double-count or
    forget to record."""
    policy = MerchantPolicy(max_single_amount=1000, max_daily_amount=150, max_daily_count=10)
    gateway = PolicyGateway(policy, VelocityTracker())

    first = gateway.check(ORDER, _action(amount=100.0))
    assert first.allowed is True

    second = gateway.check(ORDER, _action(amount=100.0))  # 100 + 100 = 200 > 150
    assert second.allowed is False
    assert second.rule_fired == "velocity_amount"


def test_count_over_daily_limit_fires_velocity_count():
    policy = MerchantPolicy(max_single_amount=1000, max_daily_amount=100_000, max_daily_count=2)
    gateway = PolicyGateway(policy, VelocityTracker())

    for _ in range(2):
        verdict = gateway.check(ORDER, _action(amount=1.0))
        assert verdict.allowed is True

    third = gateway.check(ORDER, _action(amount=1.0))
    assert third.allowed is False
    assert third.rule_fired == "velocity_count"


def test_disallowed_category_fires_category():
    policy = MerchantPolicy(max_single_amount=1000, max_daily_amount=5000, max_daily_count=10, allowed_categories=[])
    gateway = PolicyGateway(policy, VelocityTracker())
    verdict = gateway.check(ORDER, _action())
    assert verdict.allowed is False
    assert verdict.rule_fired == "category"


def test_rule_precedence_reports_the_first_violation_only():
    """An action that violates both scope and spend cap should report scope
    -- checks run in a fixed order (module docstring), so rule_fired is
    always exactly one rule, matching the demo script's requirement."""
    policy = MerchantPolicy(max_single_amount=10, max_daily_amount=5000, max_daily_count=10)
    gateway = PolicyGateway(policy, VelocityTracker())
    verdict = gateway.check(ORDER, _action(destination_account="upi:attacker@bank", amount=999.0))
    assert verdict.rule_fired == "payee_scope"
