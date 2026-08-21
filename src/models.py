"""Shared data models for the Warden pipeline (reason -> decide -> act(mocked) -> verify -> audit).

Vertical-slice scope note: this stage order matches
docs/context/Razorpay_16_Day_Battle_Plan.md's Day 6-7 line literally --
verify runs AFTER act, not before it. There is no pre-execution safety gate
yet; that's Day 8's job (docs/progress-tracker.md). Today's pipeline is a
detective control, not a preventive one.
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
    """What the agent (reason + decide) decided to do."""

    action_type: Literal["refund"] = "refund"
    amount: float
    destination_account: str
    rationale: str = Field(description="The agent's own stated reasoning, kept verbatim for audit.")


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
