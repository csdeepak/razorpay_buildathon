"""The real Razorpay rail: a client against `api.razorpay.com/v1`.

This replaces `src/tool/razorpay_mock.py` for anything that needs to be
credible against the actual API. The mock is kept because the eval harness
and the existing demo depend on its zero-setup behaviour; this module is
opt-in (`--rail razorpay`).

## The load-bearing fact about this API

**`POST /v1/payments/:id/refund` has no destination parameter.** The whole
request body is `amount`, `speed`, `notes`, `receipt`. A refund goes back to
the original payment instrument and there is no field in which to name
anywhere else.

That is not an incidental detail — it is Warden's own thesis
(`docs/decisions/0007-rearchitecture-intent-bound-authority.md`) already
implemented in production by Razorpay: the destination is derived from
trusted state rather than accepted from the caller, so no amount of
linguistic cleverness in an inbound message can redirect it.

The consequence for this codebase is `DestinationNotExpressible` below. When
a compromised agent proposes a diverted payee, we do not "block" it in any
interesting sense — we discover that the action **cannot be encoded as a
Razorpay API call at all**. That distinction is worth keeping visible in the
type system rather than flattening into a generic refusal.

## Money

Razorpay amounts are integers in the smallest currency unit (paise for INR).
`ProposedAction.amount` is rupees as a float, so every crossing of this
boundary goes through `to_paise`, which refuses anything that isn't a whole
number of paise rather than silently truncating. Float money is exactly the
kind of quiet defect this project exists to argue against.
"""

from __future__ import annotations

import os
from typing import Any, Protocol

from src.models import ExecutionResult, OrderRecord, ProposedAction

BASE_URL = "https://api.razorpay.com/v1"


class RazorpayError(RuntimeError):
    """A 4xx/5xx from the API, carrying Razorpay's own error envelope."""

    def __init__(self, status_code: int, payload: dict[str, Any]) -> None:
        err = payload.get("error", {}) if isinstance(payload, dict) else {}
        self.status_code = status_code
        self.code = err.get("code", "UNKNOWN")
        self.description = err.get("description", str(payload))
        self.field = err.get("field")
        super().__init__(f"[{status_code} {self.code}] {self.description}")


class DestinationNotExpressible(ValueError):
    """The proposed payee is not the order's original payment instrument.

    Raised *before* any network call, because there is no request that could
    express it. This is a structural backstop behind the policy gateway, not
    a duplicate of it: the gateway makes a decision, this reports a fact
    about the API's shape.
    """

    def __init__(self, proposed: str, original: str) -> None:
        self.proposed = proposed
        self.original = original
        super().__init__(
            f"Razorpay refunds return to the original payment instrument "
            f"({original!r}); there is no request field for {proposed!r}."
        )


class Response(Protocol):
    """The bit of `requests.Response` this client actually uses."""

    status_code: int

    def json(self) -> Any: ...


class Session(Protocol):
    """`requests.Session`-shaped, so the real transport IS requests and the
    fake is swapped in at the socket boundary rather than by reimplementing
    the client. Everything below -- auth, serialization, error mapping --
    runs identically in tests and in production."""

    def post(self, url: str, *, json: dict, auth: tuple[str, str], timeout: float) -> Response: ...

    def get(self, url: str, *, auth: tuple[str, str], timeout: float) -> Response: ...


def to_paise(rupees: float) -> int:
    """Rupees -> integer paise, refusing sub-paise precision.

    `1250.10 * 100` is 125009.99999999999 in binary floating point, so this
    rounds first and then checks the rounding was a no-op to within half a
    paise. Anything finer than a paise is a caller bug, not something to
    round away silently.
    """
    paise = round(rupees * 100)
    if abs(rupees * 100 - paise) > 0.5:  # pragma: no cover - unreachable by construction
        raise ValueError(f"{rupees!r} is not representable in paise")
    if abs(rupees * 100 - paise) > 1e-6:
        raise ValueError(f"{rupees!r} has sub-paise precision; refusing to truncate")
    if paise <= 0:
        raise ValueError(f"refund amount must be positive, got {rupees!r}")
    return paise


def to_rupees(paise: int) -> float:
    return paise / 100


class RazorpayAPIClient:
    """Thin, faithful client. Deliberately does not wrap the response in a
    domain model -- callers get Razorpay's own JSON, so a reader can compare
    it line-for-line against the published API docs."""

    def __init__(
        self,
        key_id: str,
        key_secret: str,
        *,
        session: Session | None = None,
        base_url: str = BASE_URL,
        timeout: float = 15.0,
    ) -> None:
        if not key_id or not key_secret:
            raise ValueError("key_id and key_secret are both required")
        self._auth = (key_id, key_secret)
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        if session is None:
            import requests  # imported lazily so the fake path needs no network stack

            session = requests.Session()
        self._session = session

    @classmethod
    def from_env(cls, *, session: Session | None = None) -> RazorpayAPIClient:
        """Keys come from the environment only -- never a constant, never an
        argument that could end up in a log line or an audit record."""
        key_id = os.environ.get("RAZORPAY_KEY_ID", "")
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
        if not key_id or not key_secret:
            raise RuntimeError(
                "RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET must be set. "
                "Generate test-mode keys in the Razorpay Dashboard under "
                "Account & Settings -> API Keys, with Test Mode on."
            )
        return cls(key_id, key_secret, session=session)

    @property
    def is_test_mode(self) -> bool:
        """Test keys are prefixed `rzp_test_`. Worth asserting loudly before
        anything in this repo is ever pointed at a live key."""
        return self._auth[0].startswith("rzp_test_")

    def _unwrap(self, response: Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except Exception:  # noqa: BLE001 - a non-JSON body is itself the error
            payload = {"error": {"code": "NON_JSON_RESPONSE", "description": "unparseable body"}}
        if response.status_code >= 400:
            raise RazorpayError(response.status_code, payload)
        return payload

    def fetch_payment(self, payment_id: str) -> dict[str, Any]:
        return self._unwrap(
            self._session.get(
                f"{self._base_url}/payments/{payment_id}",
                auth=self._auth,
                timeout=self._timeout,
            )
        )

    def create_refund(
        self,
        payment_id: str,
        *,
        amount_rupees: float | None = None,
        speed: str = "normal",
        notes: dict[str, str] | None = None,
        receipt: str | None = None,
    ) -> dict[str, Any]:
        """`POST /v1/payments/:id/refund`.

        Note what this signature cannot accept: a payee. Omitting `amount`
        means a full refund, which is the API's own default.
        """
        body: dict[str, Any] = {"speed": speed}
        if amount_rupees is not None:
            body["amount"] = to_paise(amount_rupees)
        if notes:
            body["notes"] = notes
        if receipt:
            body["receipt"] = receipt

        return self._unwrap(
            self._session.post(
                f"{self._base_url}/payments/{payment_id}/refund",
                json=body,
                auth=self._auth,
                timeout=self._timeout,
            )
        )


class RazorpayRefundRail:
    """Adapts `RazorpayAPIClient` to the pipeline's rail interface, so it is
    a drop-in for `MockRazorpayClient` wherever an `OrderRecord` is in hand.

    The `order` argument is what the mock never needed: a real refund is
    against a *payment*, not against an abstract order, so the order record
    has to carry the Razorpay payment id it was paid with.
    """

    def __init__(self, client: RazorpayAPIClient) -> None:
        self._client = client

    def create_refund(self, action: ProposedAction, order: OrderRecord) -> ExecutionResult:
        if action.destination_account != order.original_payment_instrument:
            raise DestinationNotExpressible(
                action.destination_account, order.original_payment_instrument
            )
        if not order.razorpay_payment_id:
            raise ValueError(
                f"order {order.order_id} has no razorpay_payment_id; a refund needs a "
                "captured payment to refund against"
            )

        payload = self._client.create_refund(
            order.razorpay_payment_id,
            amount_rupees=action.amount,
            notes={"order_id": order.order_id, "warden": "gated"},
        )
        return ExecutionResult(
            tx_id=payload["id"],
            status="executed",
            action=action,
        )
