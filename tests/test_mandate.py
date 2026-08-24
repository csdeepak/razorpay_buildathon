"""Tests for the mandate layer (src/safety/mandate.py, ADR 0012).

The property worth testing hardest is the one the whole design rests on:
**a mandate cannot be widened by anything the agent says.** Several tests
below are deliberately written as "attacker holds a real mandate and tries to
stretch it" rather than "function returns expected value", because that is the
threat the layer exists for.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.memory.state import VelocityTracker
from src.models import MerchantPolicy, OrderRecord, ProposedAction
from src.safety.mandate import Mandate, MandateMinter, MandateVerifier, NonceRegistry
from src.safety.policy_gateway import PolicyGateway

SECRET = "test-secret-not-a-real-key"

ORDER = OrderRecord(
    order_id="ORD-4521",
    original_payment_instrument="upi:customer4521@okhdfcbank",
    refund_amount=4999.00,
)
ATTACKER = "upi:payments-recovery@fastbank"


def _gateway(require_mandate: bool = False):
    minter = MandateMinter(SECRET)
    verifier = MandateVerifier(minter, NonceRegistry())
    gateway = PolicyGateway(
        MerchantPolicy(max_single_amount=50_000, max_daily_amount=100_000, max_daily_count=5),
        VelocityTracker(),
        mandate_verifier=verifier,
        require_mandate=require_mandate,
    )
    return minter, verifier, gateway


def _action(amount=4999.00, destination=ORDER.original_payment_instrument, action_type="refund"):
    return ProposedAction(
        action_type=action_type,
        amount=amount,
        destination_account=destination,
        rationale="test",
    )


# ----------------------------------------------------------------- minting


def test_payee_is_derived_from_trusted_state_not_supplied():
    """There is no way to pass a payee in. That is the mechanism, not an
    ergonomics gap -- see src/safety/mandate.py's module docstring."""
    minter = MandateMinter(SECRET)
    mandate = minter.mint(ORDER)
    assert mandate.payee == ORDER.original_payment_instrument
    with pytest.raises(TypeError):
        minter.mint(ORDER, payee=ATTACKER)  # type: ignore[call-arg]


def test_mandate_may_narrow_the_amount():
    mandate = MandateMinter(SECRET).mint(ORDER, max_amount=1000.0)
    assert mandate.max_amount == 1000.0


def test_mandate_cannot_be_minted_wider_than_the_order():
    with pytest.raises(ValueError, match="never widen"):
        MandateMinter(SECRET).mint(ORDER, max_amount=49_990.0)


def test_signature_survives_a_json_round_trip():
    """A mandate crosses a process boundary in any real deployment. If the
    canonical payload were sensitive to datetime representation, verification
    would pass in-process and fail over the wire -- the worst possible split."""
    minter = MandateMinter(SECRET)
    verifier = MandateVerifier(minter)
    original = minter.mint(ORDER)
    revived = Mandate.model_validate_json(original.model_dump_json())
    assert verifier.verify(revived).valid


# ------------------------------------------------------------ authenticity


def test_forged_signature_is_refused():
    minter, _, gateway = _gateway()
    mandate = minter.mint(ORDER)
    mandate.signature = "0" * 64
    verdict = gateway.check(ORDER, _action(), mandate)
    assert not verdict.allowed and verdict.rule_fired == "mandate_signature"


def test_altering_a_field_after_minting_breaks_the_signature():
    """The attack this prevents: the agent holds a genuine mandate and edits
    the payee before presenting it."""
    minter, _, gateway = _gateway()
    mandate = minter.mint(ORDER)
    mandate.payee = ATTACKER
    verdict = gateway.check(ORDER, _action(destination=ATTACKER), mandate)
    assert not verdict.allowed and verdict.rule_fired == "mandate_signature"


def test_a_mandate_from_another_authorisation_boundary_is_refused():
    _, _, gateway = _gateway()
    foreign = MandateMinter("some-other-secret").mint(ORDER)
    verdict = gateway.check(ORDER, _action(), foreign)
    assert not verdict.allowed and verdict.rule_fired == "mandate_signature"


# ------------------------------------------------------------------ expiry


def test_expired_mandate_is_refused():
    minter, _, gateway = _gateway()
    past = datetime.now(timezone.utc) - timedelta(hours=2)
    mandate = minter.mint(ORDER, ttl_seconds=60, now=past)
    verdict = gateway.check(ORDER, _action(), mandate)
    assert not verdict.allowed and verdict.rule_fired == "mandate_expiry"


def test_unexpired_mandate_passes():
    minter, _, gateway = _gateway()
    assert gateway.check(ORDER, _action(), minter.mint(ORDER)).allowed


# ------------------------------------------------------------- single-use


def test_replay_is_refused_on_second_use():
    minter, _, gateway = _gateway()
    mandate = minter.mint(ORDER)
    assert gateway.check(ORDER, _action(), mandate).allowed
    second = gateway.check(ORDER, _action(), mandate)
    assert not second.allowed and second.rule_fired == "mandate_replay"


def test_a_blocked_action_does_not_burn_the_mandate():
    """If a refused attempt spent the nonce, an attacker could disable a
    legitimate refund just by proposing one bad action first -- turning the
    replay guard into a denial-of-service primitive."""
    minter, _, gateway = _gateway()
    mandate = minter.mint(ORDER)
    blocked = gateway.check(ORDER, _action(destination=ATTACKER), mandate)
    assert not blocked.allowed
    assert gateway.check(ORDER, _action(), mandate).allowed


# ---------------------------------------------------------------- binding


def test_mandate_for_another_order_does_not_transfer():
    minter, _, gateway = _gateway()
    other = OrderRecord(
        order_id="ORD-9002",
        original_payment_instrument="upi:sharma.biz@oksbi",
        refund_amount=22_400.00,
    )
    verdict = gateway.check(ORDER, _action(), minter.mint(other))
    assert not verdict.allowed and verdict.rule_fired == "mandate_order_scope"


def test_refund_mandate_does_not_authorise_a_payout():
    """Scope escalation, the ADR 0007 taxonomy's class 7, at the authority
    layer rather than the policy layer."""
    minter, _, gateway = _gateway()
    mandate = minter.mint(ORDER, action_type="refund")
    verdict = gateway.check(ORDER, _action(action_type="payout"), mandate)
    assert not verdict.allowed and verdict.rule_fired == "mandate_action_scope"


def test_destination_outside_the_mandate_is_refused():
    minter, _, gateway = _gateway()
    verdict = gateway.check(ORDER, _action(destination=ATTACKER), minter.mint(ORDER))
    assert not verdict.allowed and verdict.rule_fired == "mandate_payee_scope"


def test_amount_above_the_mandate_ceiling_is_refused():
    minter, _, gateway = _gateway()
    mandate = minter.mint(ORDER, max_amount=1000.0)
    verdict = gateway.check(ORDER, _action(amount=4999.00), mandate)
    assert not verdict.allowed and verdict.rule_fired == "mandate_amount_scope"


def test_partial_refund_inside_the_mandate_is_allowed():
    """ADR 0008's `<=` rule, carried into the mandate layer: narrowing is a
    legitimate business decision and must not be blocked."""
    minter, _, gateway = _gateway()
    assert gateway.check(ORDER, _action(amount=1200.00), minter.mint(ORDER)).allowed


# ------------------------------------------------------------ configuration


def test_require_mandate_blocks_an_unmandated_action():
    _, _, gateway = _gateway(require_mandate=True)
    verdict = gateway.check(ORDER, _action())
    assert not verdict.allowed and verdict.rule_fired == "mandate_missing"


def test_mandate_presented_to_a_gateway_with_no_verifier_is_refused():
    """Failing closed. Ignoring an unverifiable mandate would be strictly
    worse than requiring none, because it looks like authority and isn't."""
    gateway = PolicyGateway(
        MerchantPolicy(max_single_amount=50_000, max_daily_amount=100_000, max_daily_count=5),
        VelocityTracker(),
    )
    verdict = gateway.check(ORDER, _action(), MandateMinter(SECRET).mint(ORDER))
    assert not verdict.allowed and verdict.rule_fired == "mandate_unverifiable"


def test_default_gateway_is_unchanged_when_no_mandate_is_used():
    """Backwards compatibility is load-bearing, not incidental: every number in
    docs/eval-findings.md was measured against the policy rules alone, so the
    mandate layer must be additive or the recorded results stop describing the
    system. ADR 0012 records this constraint."""
    gateway = PolicyGateway(
        MerchantPolicy(max_single_amount=50_000, max_daily_amount=100_000, max_daily_count=5),
        VelocityTracker(),
    )
    assert gateway.check(ORDER, _action()).allowed
    blocked = gateway.check(ORDER, _action(destination=ATTACKER))
    assert not blocked.allowed and blocked.rule_fired == "payee_scope"
