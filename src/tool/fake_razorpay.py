"""An in-process fake of the Razorpay API, faithful at the HTTP boundary.

This is deliberately *not* a second implementation of the client. It is a
`requests.Session`-shaped object, so `RazorpayAPIClient` runs its real auth,
serialization, status handling and error mapping against it. Only the socket
is missing.

## What "faithful" has to mean here

A fake that accepts anything proves nothing. The properties below are the
ones this project's claims actually rest on, so the fake enforces each of
them and the tests assert the enforcement:

1. **The refund body accepts exactly `amount`, `speed`, `notes`, `receipt`.**
   Any other key is a 400. This is the one that matters most: it is what
   makes "you cannot redirect a Razorpay refund" a property the test suite
   demonstrates rather than a sentence in a document.
2. **Amounts are integer paise.** A float amount is a 400, not a silent
   coercion.
3. **You cannot refund more than the payment's unrefunded balance**, and
   partial refunds decrement it.
4. **Only captured payments are refundable.**
5. Errors use Razorpay's own envelope, so `RazorpayError` parsing is
   exercised for real.

Where the real API and this fake are allowed to differ: settlement timing,
`speed=optimum` behaviour, batch refunds, and webhooks. None are load-bearing
for anything Warden claims. That list is here so the gap is stated rather
than discovered.
"""

from __future__ import annotations

import json as _json
import random
import string
import time
from typing import Any

REFUND_BODY_KEYS = frozenset({"amount", "speed", "notes", "receipt"})
"""The complete set of documented request parameters for a normal refund.

`destination`, `payee`, `vpa`, `account`, `fund_account_id` are conspicuously
not here, and that is the point.
"""


def _rzp_id(prefix: str, rng: random.Random) -> str:
    alphabet = string.ascii_letters + string.digits
    return f"{prefix}_{''.join(rng.choice(alphabet) for _ in range(14))}"


class FakeResponse:
    """`requests.Response`-shaped, to the extent the client touches it."""

    def __init__(self, status_code: int, payload: Any) -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = _json.dumps(payload)

    def json(self) -> Any:
        return self._payload


def _error(
    description: str,
    *,
    status: int = 400,
    code: str = "BAD_REQUEST_ERROR",
    field: str | None = None,
) -> FakeResponse:
    err: dict[str, Any] = {
        "code": code,
        "description": description,
        "source": "business",
        "step": "payment_initiation",
        "reason": "input_validation_failed",
        "metadata": {},
    }
    if field:
        err["field"] = field
    return FakeResponse(status, {"error": err})


class FakeRazorpaySession:
    """A stand-in for `requests.Session` holding an in-memory payment book.

    Seeded RNG so ids are reproducible across a test run; `seed_payment`
    builds the captured payment a refund needs to exist against.
    """

    def __init__(self, *, seed: int = 0, base_url: str = "https://api.razorpay.com/v1") -> None:
        self._rng = random.Random(seed)
        self._base = base_url.rstrip("/")
        self.payments: dict[str, dict[str, Any]] = {}
        self.refunds: dict[str, dict[str, Any]] = {}
        self.requests: list[tuple[str, str, dict | None]] = []

    # ---- test setup -------------------------------------------------

    def seed_payment(
        self,
        *,
        amount_rupees: float,
        vpa: str = "rmehta@okaxis",
        status: str = "captured",
        order_id: str | None = None,
    ) -> str:
        payment_id = _rzp_id("pay", self._rng)
        self.payments[payment_id] = {
            "id": payment_id,
            "entity": "payment",
            "amount": round(amount_rupees * 100),
            "currency": "INR",
            "status": status,
            "order_id": order_id or _rzp_id("order", self._rng),
            "method": "upi",
            "amount_refunded": 0,
            "refund_status": None,
            "captured": status == "captured",
            "vpa": vpa,
            "created_at": int(time.time()),
        }
        return payment_id

    # ---- transport --------------------------------------------------

    def _check_auth(self, auth: tuple[str, str] | None) -> FakeResponse | None:
        if not auth or not auth[0] or not auth[1]:
            return _error(
                "Authentication failed",
                status=401,
                code="BAD_REQUEST_ERROR",
            )
        if not auth[0].startswith("rzp_"):
            return _error("The api key provided is invalid", status=401, field="key_id")
        return None

    def get(self, url: str, *, auth: tuple[str, str], timeout: float = 15.0) -> FakeResponse:
        self.requests.append(("GET", url, None))
        if (bad := self._check_auth(auth)) is not None:
            return bad

        path = url[len(self._base) :] if url.startswith(self._base) else url
        parts = [p for p in path.split("/") if p]
        if len(parts) == 2 and parts[0] == "payments":
            payment = self.payments.get(parts[1])
            if payment is None:
                return _error(
                    "The id provided does not exist", status=400, field="payment_id"
                )
            return FakeResponse(200, dict(payment))
        return _error("The requested URL was not found on the server.", status=404)

    def post(
        self,
        url: str,
        *,
        json: dict,
        auth: tuple[str, str],
        timeout: float = 15.0,
    ) -> FakeResponse:
        self.requests.append(("POST", url, dict(json)))
        if (bad := self._check_auth(auth)) is not None:
            return bad

        path = url[len(self._base) :] if url.startswith(self._base) else url
        parts = [p for p in path.split("/") if p]
        if len(parts) == 3 and parts[0] == "payments" and parts[2] == "refund":
            return self._create_refund(parts[1], json)
        return _error("The requested URL was not found on the server.", status=404)

    def _create_refund(self, payment_id: str, body: dict) -> FakeResponse:
        # (1) Unknown parameters are rejected. This is the property that makes
        # payee diversion inexpressible rather than merely discouraged.
        unknown = set(body) - REFUND_BODY_KEYS
        if unknown:
            key = sorted(unknown)[0]
            return _error(
                f"{key} is not a valid parameter for this request", field=key
            )

        payment = self.payments.get(payment_id)
        if payment is None:
            return _error("The id provided does not exist", field="payment_id")

        # (4) Only captured payments can be refunded.
        if payment["status"] != "captured":
            return _error(
                f"The payment has been {payment['status']}. Only captured payments "
                "can be refunded",
                field="payment_id",
            )

        refundable = payment["amount"] - payment["amount_refunded"]
        amount = body.get("amount", refundable)

        # (2) Integer paise only.
        if isinstance(amount, bool) or not isinstance(amount, int):
            return _error(
                "The amount must be an integer in the smallest unit of the currency",
                field="amount",
            )
        if amount <= 0:
            return _error("The amount must be atleast INR 1.00", field="amount")

        # (3) Cannot exceed the unrefunded balance.
        if amount > refundable:
            return _error(
                "The refund amount provided is greater than amount captured",
                field="amount",
            )

        speed = body.get("speed", "normal")
        if speed not in {"normal", "optimum"}:
            return _error("Invalid speed provided", field="speed")

        payment["amount_refunded"] += amount
        payment["refund_status"] = (
            "full" if payment["amount_refunded"] == payment["amount"] else "partial"
        )

        refund_id = _rzp_id("rfnd", self._rng)
        refund = {
            "id": refund_id,
            "entity": "refund",
            "amount": amount,
            "currency": "INR",
            "payment_id": payment_id,
            "notes": body.get("notes", {}),
            "receipt": body.get("receipt"),
            "acquirer_data": {"arn": _rzp_id("arn", self._rng)},
            "created_at": int(time.time()),
            "batch_id": None,
            "status": "processed",
            "speed_requested": speed,
            "speed_processed": speed,
        }
        self.refunds[refund_id] = refund
        return FakeResponse(200, dict(refund))
