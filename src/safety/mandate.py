"""Intent-bound authority: the mandate layer.

`docs/decisions/0007-rearchitecture-intent-bound-authority.md` states the core
idea of this project -- *don't filter instructions, bind authority to verified
intent* -- and specifies a mandate as "a signed, scoped, single-use, expiring
capability minted from a verified human authorization." Until
`docs/decisions/0012-mandate-layer.md` that specification existed only in the
ADR and the submission narrative: what shipped was
`src/safety/policy_gateway.py`'s five ordered rules, which are sound but are
*policy*, not *capability*. This module closes that gap, and 0012 records why
it was a real defect rather than a wording quibble.

WHAT A MANDATE IS, AND WHAT IT IS NOT
-------------------------------------
It is **not a credential**. It carries no key, no token the rail understands,
and no ability to move money on its own. It is an assertion, signed by the
authorization side, that says:

    "this specific action, on this specific order, to this specific payee,
     up to this amount, once, before this moment."

The agent may hold it and present it. The agent cannot mint one, cannot widen
one, and cannot re-use one.

WHY THE PAYEE IS AN INPUT, NOT A PARAMETER
------------------------------------------
`mint()` derives the payee from the `OrderRecord` -- trusted state -- and
offers no way to pass one in. That is the entire mechanism, and it is
deliberately not configurable: if a caller could supply the payee, then any
path that reaches `mint()` with attacker-influenced data reintroduces exactly
the vulnerability the design exists to remove. The same argument applies to
`order_id`. Amount is the one field a caller may narrow (never widen -- see
`mint()`), because a partial refund is a legitimate business decision while an
inflated one is never legitimate (ADR 0008).

WHY HMAC AND NOT A PUBLIC-KEY SIGNATURE
---------------------------------------
The minter and the verifier are the same trust domain here -- both sit inside
the enforcement boundary, and the agent is outside it. A shared secret is
sufficient for that threat model and has no key-distribution story to get
wrong. A *public-key* signature buys something real the moment mandates are
minted by one service and verified by another (a merchant minting, Razorpay
verifying), and that is the upgrade path, not this build. Stated plainly here
so the choice reads as a decision rather than an omission.

SINGLE-USE IS ENFORCED BY THE VERIFIER, NOT BY THE MANDATE
----------------------------------------------------------
Nothing in a signed document can stop it being presented twice; replay
protection is always the verifier's job. `NonceRegistry` holds spent nonces
and `MandateVerifier.spend()` is called only on a *fully* allowed action --
the same check-and-record atomicity that `PolicyGateway` already applies to
velocity, and for the same reason: a path to "allowed" that forgets to record
leaves the limit toothless.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Literal

from pydantic import BaseModel, Field

from src.models import OrderRecord

DEFAULT_TTL_SECONDS = 300
"""Five minutes. A refund decision that a human authorized should be acted on
promptly; a mandate still valid hours later is the temporal-decoupling gap
that `docs/decisions/0007`'s taxonomy names as class 9."""


class Mandate(BaseModel):
    """A scoped, single-use, expiring capability. Signed; not a credential."""

    mandate_id: str
    action_type: Literal["refund", "payout"]
    order_id: str
    payee: str
    max_amount: float
    issued_at: datetime
    expires_at: datetime
    single_use: bool = True
    nonce: str
    signature: str = ""

    def signing_payload(self) -> str:
        """Canonical bytes the signature covers. Excludes `signature` itself,
        sorts keys, and renders datetimes in ISO-8601 UTC so that a mandate
        round-tripped through JSON verifies identically to one held in memory."""
        body = {
            "mandate_id": self.mandate_id,
            "action_type": self.action_type,
            "order_id": self.order_id,
            "payee": self.payee,
            "max_amount": float(self.max_amount),
            "issued_at": self.issued_at.astimezone(timezone.utc).isoformat(),
            "expires_at": self.expires_at.astimezone(timezone.utc).isoformat(),
            "single_use": self.single_use,
            "nonce": self.nonce,
        }
        return json.dumps(body, sort_keys=True, separators=(",", ":"))


class MandateVerdict(BaseModel):
    """Why a mandate was rejected. `rule_fired` names exactly one rule, matching
    `PolicyVerdict`'s contract -- the demo has to show which check refused."""

    valid: bool
    rule_fired: str | None = None
    reason: str = ""


class NonceRegistry:
    """Spent-nonce store. In-memory, matching the depth allocation in
    `src/README.md` -- a real deployment needs this durable and shared, which
    is a deployment concern, not an architectural one."""

    def __init__(self) -> None:
        self._spent: set[str] = set()

    def is_spent(self, nonce: str) -> bool:
        return nonce in self._spent

    def spend(self, nonce: str) -> None:
        self._spent.add(nonce)


def _load_secret() -> bytes:
    """WARDEN_MANDATE_KEY if set, otherwise a per-process random secret.

    The random fallback is deliberate: it keeps `make demo` and the tests
    runnable with no configuration, and it fails *closed* across processes --
    a mandate minted by one process will not verify in another, which is the
    safe direction for a signing key to be wrong in."""
    configured = os.environ.get("WARDEN_MANDATE_KEY")
    if configured:
        return configured.encode("utf-8")
    return secrets.token_bytes(32)


class MandateMinter:
    """The authorization side. Mints mandates from trusted state only."""

    def __init__(self, secret: bytes | str | None = None) -> None:
        if secret is None:
            self._secret = _load_secret()
        else:
            self._secret = secret.encode("utf-8") if isinstance(secret, str) else secret

    def sign(self, payload: str) -> str:
        return hmac.new(self._secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()

    def mint(
        self,
        order: OrderRecord,
        *,
        action_type: Literal["refund", "payout"] = "refund",
        max_amount: float | None = None,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
        now: datetime | None = None,
    ) -> Mandate:
        """Mint a mandate for one action on one order.

        There is deliberately no `payee` parameter: the payee is the order's
        original payment instrument, read from trusted state. See this module's
        docstring.

        `max_amount` may only NARROW the ceiling. Passing more than the order
        records as owed raises -- silently clamping would make an over-wide
        request look like it succeeded, and a caller asking for authority it
        cannot have is a bug worth surfacing at mint time rather than a policy
        decision to defer to the gateway.
        """
        now = now or datetime.now(timezone.utc)
        ceiling = order.refund_amount
        if max_amount is None:
            amount = ceiling
        elif max_amount > ceiling:
            raise ValueError(
                f"cannot mint a mandate for {max_amount} on order "
                f"{order.order_id}: only {ceiling} was actually paid. A mandate "
                f"may narrow authority, never widen it."
            )
        else:
            amount = max_amount

        mandate = Mandate(
            mandate_id=f"mdt_{secrets.token_hex(8)}",
            action_type=action_type,
            order_id=order.order_id,
            payee=order.original_payment_instrument,
            max_amount=amount,
            issued_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
            nonce=secrets.token_hex(16),
        )
        mandate.signature = self.sign(mandate.signing_payload())
        return mandate


class MandateVerifier:
    """The enforcement side. Checks a presented mandate before any policy rule
    runs -- authority first, then whether the action fits inside it."""

    def __init__(self, minter: MandateMinter, registry: NonceRegistry | None = None) -> None:
        self._minter = minter
        self._registry = registry or NonceRegistry()

    def verify(self, mandate: Mandate, *, now: datetime | None = None) -> MandateVerdict:
        """Validate the mandate itself. Says nothing about the action -- that
        binding happens in `PolicyGateway`, so that a forged mandate and an
        in-scope-but-disallowed action fire visibly different rules."""
        now = now or datetime.now(timezone.utc)

        expected = self._minter.sign(mandate.signing_payload())
        if not hmac.compare_digest(expected, mandate.signature):
            return MandateVerdict(
                valid=False,
                rule_fired="mandate_signature",
                reason=(
                    f"mandate {mandate.mandate_id} does not carry a valid "
                    f"signature. It was not minted by this authorization "
                    f"boundary, or a field was altered after minting."
                ),
            )

        expires = mandate.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if now > expires:
            return MandateVerdict(
                valid=False,
                rule_fired="mandate_expiry",
                reason=(
                    f"mandate {mandate.mandate_id} expired at "
                    f"{expires.isoformat()}; it is now {now.isoformat()}. "
                    f"Authority does not survive the conditions it was granted "
                    f"under."
                ),
            )

        if mandate.single_use and self._registry.is_spent(mandate.nonce):
            return MandateVerdict(
                valid=False,
                rule_fired="mandate_replay",
                reason=(
                    f"mandate {mandate.mandate_id} is single-use and has "
                    f"already been spent. Re-presenting it is a replay, not a "
                    f"second authorization."
                ),
            )

        return MandateVerdict(valid=True, reason="mandate is authentic, unexpired and unspent.")

    def spend(self, mandate: Mandate) -> None:
        """Burn the nonce. Called by `PolicyGateway` only once an action has
        passed every check -- see this module's docstring on why the verifier
        owns replay protection."""
        if mandate.single_use:
            self._registry.spend(mandate.nonce)
