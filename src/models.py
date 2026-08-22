"""Shared data models for the Warden pipeline: reason -> decide -> safety
gate -> act(mocked) -> verify -> audit.

As of the Day 8 safety layer (docs/decisions/0006-safety-layer.md), the
gate sits BEFORE act -- this supersedes the Day 6-7 vertical slice's literal
stage order (docs/decisions/0005-vertical-slice-architecture.md), which had
verify running after act with no preventive check at all. That ADR is left
as-is per this repo's own rule against editing old decisions; this docstring
describes current behavior.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class OrderRecord(BaseModel):
    """Ground-truth order data, looked up from the 'memory' store -- never
    read out of the untrusted inbound message."""

    order_id: str
    original_payment_instrument: str
    refund_amount: float


class Scenario(BaseModel):
    """One demo scenario: which order it's about, and the inbound message
    that may or may not be a prompt-injection attack. Deliberately carries
    no payment-instrument data itself -- that only comes from OrderRecord."""

    name: str
    order_id: str
    inbound_message: str


class ProposedAction(BaseModel):
    """What the agent (reason + decide) decided to do.

    `payout` exists so scope escalation is testable: an agent authorised only
    for refunds should be refused on `category` when it reaches for a payout.
    A merchant policy that omits "payout" from allowed_categories is what
    makes that refusal happen.
    """

    action_type: Literal["refund", "payout"] = "refund"
    amount: float
    destination_account: str
    rationale: str = Field(description="The agent's own stated reasoning, kept verbatim for audit.")


class MerchantPolicy(BaseModel):
    """Static safety-layer configuration -- deliberately holds no
    order-specific data (payee scope for refunds is derived dynamically
    from the OrderRecord in the gateway itself, see src/safety/policy_gateway.py)."""

    max_single_amount: float
    max_daily_amount: float
    max_daily_count: int
    allowed_categories: list[str] = Field(default_factory=lambda: ["refund"])


class PolicyVerdict(BaseModel):
    """The safety gate's pre-execution decision. rule_fired names exactly
    which rule blocked the action, or is None if it passed -- the demo
    script requires showing which specific rule fired, not a generic
    'blocked' toast."""

    allowed: bool
    rule_fired: str | None
    reason: str


class ExecutionResult(BaseModel):
    """The (mocked) outcome of sending the action to the payment rail."""

    tx_id: str
    status: Literal["executed"]
    action: ProposedAction
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class VerificationVerdict(BaseModel):
    """Independent, post-hoc re-derivation of what should have happened,
    compared against what the agent actually did."""

    consistent: bool
    expected_destination: str
    actual_destination: str
    reason: str
