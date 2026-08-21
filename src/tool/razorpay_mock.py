"""The 'act (mocked)' stage: a stand-in for Razorpay's payout/refund API.

Genuinely mocked, not a stub pretending to be real -- no network call, no
API key. Swap for a real Razorpay test-mode client once Gate 0's confirmed
sandbox access (Track 01 only, docs/gate-0-tracker.md) is actually wired
up; that's an infrastructure change to this module only, nothing upstream
should need to change.
"""

from __future__ import annotations

import uuid

from src.models import ExecutionResult, ProposedAction


class MockRazorpayClient:
    """No preventive checks here on purpose -- see module docstring in
    src/models.py about the Day 6-7 stage order. This layer just executes
    whatever it's handed."""

    def create_refund(self, action: ProposedAction) -> ExecutionResult:
        tx_id = f"mock_rfnd_{uuid.uuid4().hex[:12]}"
        return ExecutionResult(tx_id=tx_id, status="executed", action=action)
