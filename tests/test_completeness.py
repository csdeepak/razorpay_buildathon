"""Tests for the completeness checker -- the detective control for denial
attacks (docs/eval-findings.md Finding 11)."""

from __future__ import annotations

from src.models import OrderRecord
from src.verification.completeness import CompletenessChecker

ORDER = OrderRecord(
    order_id="ORD-TEST",
    original_payment_instrument="upi:customer@okhdfcbank",
    refund_amount=1000.0,
)


def test_open_request_with_no_payment_is_incomplete():
    """The denial-attack signature: an obligation exists, nothing was paid."""
    v = CompletenessChecker().check(ORDER, refund_request_open=True, refund_paid_total=0.0)
    assert v.complete is False
    assert v.needs_review is True
    assert v.obligation == "open_refund_request"


def test_open_request_discharged_by_payment_is_complete():
    v = CompletenessChecker().check(ORDER, refund_request_open=True, refund_paid_total=1000.0)
    assert v.complete is True


def test_partial_payment_discharges_the_obligation():
    """Partial refunds are legitimate (ADR 0008), so a part-payment counts as
    discharged. Under-refunding is a separate concern with its own rule."""
    v = CompletenessChecker().check(ORDER, refund_request_open=True, refund_paid_total=250.0)
    assert v.complete is True


def test_no_open_request_is_complete_even_with_no_payment():
    """A customer who asks a question and doesn't want a refund must not be
    flagged -- this is the over-flagging side of the control."""
    v = CompletenessChecker().check(ORDER, refund_request_open=False, refund_paid_total=0.0)
    assert v.complete is True


def test_forged_claims_cannot_change_the_verdict():
    """The whole point: the checker takes trusted state as arguments and has
    no channel through which a poisoned note could reach it. Two sessions
    with identical trusted state get identical verdicts regardless of what
    was said in either conversation."""
    checker = CompletenessChecker()
    a = checker.check(ORDER, refund_request_open=True, refund_paid_total=0.0)
    b = checker.check(ORDER, refund_request_open=True, refund_paid_total=0.0)
    assert a.complete == b.complete is False
