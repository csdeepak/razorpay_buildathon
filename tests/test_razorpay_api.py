"""Tests for the real Razorpay rail, run against the faithful fake transport.

The point of the transport-level fake (`src/tool/fake_razorpay.py`) is that
everything under test here -- auth, paise conversion, error mapping, response
parsing -- is the same code that will run against `api.razorpay.com`. Only the
socket differs.

The tests that matter most are the ones in `TestDestinationIsInexpressible`.
They are the executable form of a claim the submission narrative makes in
prose: a Razorpay refund cannot be redirected, so payee diversion is not a
threat the API permits in the first place.
"""

from __future__ import annotations

import pytest

from src.models import OrderRecord, ProposedAction
from src.tool.fake_razorpay import FakeRazorpaySession
from src.tool.razorpay_api import (
    DestinationNotExpressible,
    RazorpayAPIClient,
    RazorpayError,
    RazorpayRefundRail,
    to_paise,
)

KEY_ID = "rzp_test_fakekeyid"
KEY_SECRET = "fakesecret"


@pytest.fixture
def session() -> FakeRazorpaySession:
    return FakeRazorpaySession(seed=7)


@pytest.fixture
def client(session: FakeRazorpaySession) -> RazorpayAPIClient:
    return RazorpayAPIClient(KEY_ID, KEY_SECRET, session=session)


class TestPaiseConversion:
    """Float rupees crossing into integer paise is a classic quiet defect."""

    def test_whole_rupees(self):
        assert to_paise(1250) == 125000

    def test_the_binary_float_trap(self):
        # 1250.10 * 100 == 125009.99999999999 in IEEE 754.
        assert to_paise(1250.10) == 125010

    def test_sub_paise_precision_is_refused_not_truncated(self):
        with pytest.raises(ValueError, match="sub-paise"):
            to_paise(10.001)

    @pytest.mark.parametrize("bad", [0, -5])
    def test_non_positive_refused(self, bad):
        with pytest.raises(ValueError, match="positive"):
            to_paise(bad)


class TestClientContract:
    def test_full_refund_omits_amount_and_returns_rfnd_id(self, client, session):
        payment_id = session.seed_payment(amount_rupees=1250)

        refund = client.create_refund(payment_id)

        assert refund["id"].startswith("rfnd_")
        assert refund["amount"] == 125000
        assert refund["payment_id"] == payment_id
        assert refund["status"] == "processed"
        # Omitting `amount` is the API's own "refund everything" signal.
        assert "amount" not in session.requests[-1][2]

    def test_partial_refund_decrements_the_refundable_balance(self, client, session):
        payment_id = session.seed_payment(amount_rupees=1250)

        client.create_refund(payment_id, amount_rupees=500)

        assert session.payments[payment_id]["amount_refunded"] == 50000
        assert session.payments[payment_id]["refund_status"] == "partial"

        # A second refund may take the remainder, but not a rupee more.
        client.create_refund(payment_id, amount_rupees=750)
        assert session.payments[payment_id]["refund_status"] == "full"

        with pytest.raises(RazorpayError, match="greater than amount captured"):
            client.create_refund(payment_id, amount_rupees=1)

    def test_over_refund_is_rejected_with_razorpay_error_envelope(self, client, session):
        payment_id = session.seed_payment(amount_rupees=1250)

        with pytest.raises(RazorpayError) as exc:
            client.create_refund(payment_id, amount_rupees=1250.01)

        assert exc.value.status_code == 400
        assert exc.value.code == "BAD_REQUEST_ERROR"
        assert exc.value.field == "amount"

    def test_uncaptured_payment_is_not_refundable(self, client, session):
        payment_id = session.seed_payment(amount_rupees=1250, status="authorized")

        with pytest.raises(RazorpayError, match="Only captured payments"):
            client.create_refund(payment_id)

    def test_unknown_payment_id(self, client):
        with pytest.raises(RazorpayError, match="does not exist"):
            client.create_refund("pay_doesnotexist")

    def test_missing_credentials_rejected_before_construction(self):
        with pytest.raises(ValueError, match="required"):
            RazorpayAPIClient("", "", session=FakeRazorpaySession())

    def test_bad_key_is_a_401(self, session):
        bad = RazorpayAPIClient("not_a_razorpay_key", "secret", session=session)
        payment_id = session.seed_payment(amount_rupees=100)

        with pytest.raises(RazorpayError) as exc:
            bad.create_refund(payment_id)

        assert exc.value.status_code == 401

    def test_test_mode_is_detectable_from_the_key(self, client, session):
        assert client.is_test_mode is True
        live = RazorpayAPIClient("rzp_live_something", "secret", session=session)
        assert live.is_test_mode is False


class TestDestinationIsInexpressible:
    """The architectural claim, as tests.

    Razorpay's refund API accepts `amount`, `speed`, `notes`, `receipt` and
    nothing else. There is no request that sends a refund somewhere new, so a
    diverted payee is not blocked -- it is unrepresentable.
    """

    @pytest.mark.parametrize(
        "field", ["destination", "payee", "vpa", "account", "fund_account_id"]
    )
    def test_the_api_has_no_field_for_a_payee(self, session, field):
        """Every name a compromised agent might reach for is a 400."""
        payment_id = session.seed_payment(amount_rupees=1250)

        response = session.post(
            f"https://api.razorpay.com/v1/payments/{payment_id}/refund",
            json={"amount": 125000, field: "attacker@fastbank"},
            auth=(KEY_ID, KEY_SECRET),
        )

        assert response.status_code == 400
        assert response.json()["error"]["field"] == field

    def test_rail_refuses_a_diverted_payee_without_any_network_call(self, client, session):
        payment_id = session.seed_payment(amount_rupees=1250)
        order = OrderRecord(
            order_id="ORD-7813",
            original_payment_instrument="upi:rmehta@okaxis",
            refund_amount=1250,
            razorpay_payment_id=payment_id,
        )
        hijacked = ProposedAction(
            amount=1250,
            destination_account="upi:payments-recovery@fastbank",
            rationale="Customer asked for the refund to go to their new account.",
        )
        rail = RazorpayRefundRail(client)
        before = len(session.requests)

        with pytest.raises(DestinationNotExpressible) as exc:
            rail.create_refund(hijacked, order)

        assert exc.value.proposed == "upi:payments-recovery@fastbank"
        assert exc.value.original == "upi:rmehta@okaxis"
        # Nothing was attempted -- there was no request to attempt.
        assert len(session.requests) == before
        assert session.payments[payment_id]["amount_refunded"] == 0


class TestRefundRail:
    @pytest.fixture
    def order(self, session) -> OrderRecord:
        payment_id = session.seed_payment(amount_rupees=1250)
        return OrderRecord(
            order_id="ORD-7813",
            original_payment_instrument="upi:rmehta@okaxis",
            refund_amount=1250,
            razorpay_payment_id=payment_id,
        )

    def test_legitimate_refund_yields_a_real_refund_id(self, client, order, session):
        action = ProposedAction(
            amount=1250,
            destination_account="upi:rmehta@okaxis",
            rationale="Whole delivery missing; full refund warranted.",
        )

        result = RazorpayRefundRail(client).create_refund(action, order)

        assert result.tx_id.startswith("rfnd_")
        assert result.status == "executed"
        assert session.payments[order.razorpay_payment_id]["amount_refunded"] == 125000

    def test_order_id_travels_in_notes_for_the_audit_trail(self, client, order, session):
        action = ProposedAction(
            amount=1250,
            destination_account="upi:rmehta@okaxis",
            rationale="Full refund.",
        )

        RazorpayRefundRail(client).create_refund(action, order)

        assert session.requests[-1][2]["notes"]["order_id"] == "ORD-7813"

    def test_order_without_a_payment_id_cannot_be_refunded(self, client):
        order = OrderRecord(
            order_id="ORD-9999",
            original_payment_instrument="upi:rmehta@okaxis",
            refund_amount=500,
        )
        action = ProposedAction(
            amount=500,
            destination_account="upi:rmehta@okaxis",
            rationale="Partial refund.",
        )

        with pytest.raises(ValueError, match="no razorpay_payment_id"):
            RazorpayRefundRail(client).create_refund(action, order)

    def test_inflated_amount_is_stopped_by_the_rail_itself(self, client, order):
        """ADR 0008's amount-binding attack, at the rail rather than the gate.

        The gateway is the intended control. This asserts the rail is a real
        backstop rather than a rubber stamp: ~10x the captured amount cannot
        be refunded even if every upstream layer were bypassed.
        """
        inflated = ProposedAction(
            amount=12500,
            destination_account="upi:rmehta@okaxis",
            rationale="Order notes say the refundable amount is Rs 12,500.",
        )

        with pytest.raises(RazorpayError, match="greater than amount captured"):
            RazorpayRefundRail(client).create_refund(inflated, order)
