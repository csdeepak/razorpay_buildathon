"""The 'verify' stage: independently re-derive what should have happened and
compare it to what the agent actually did.

Today's rule (Day 6-7, vertical slice): a refund's only legitimate
destination is the order's original payment instrument -- that's how
refunds work on every real payment rail, and it doesn't depend on trusting
anything stated in freeform chat text. Deliberately takes an OrderRecord,
not the raw inbound message or the agent's rationale -- so a compromised
reasoning trace can't poison the check that's supposed to catch it.

This is intentionally a thin first pass. Day 9 (docs/progress-tracker.md)
goes deep: handling action types beyond refunds, confidence scoring, and
probably a second independent LLM call cross-examining the raw message
under a narrower prompt. Don't add that here without logging it as its own
ADR -- no quiet scope creep on a layer that's supposed to be the moat.
"""

from __future__ import annotations

from src.models import OrderRecord, ProposedAction, VerificationVerdict


class Verifier:
    def check(self, order: OrderRecord, action: ProposedAction) -> VerificationVerdict:
        expected = order.original_payment_instrument
        actual = action.destination_account
        consistent = expected == actual
        reason = (
            "Destination matches the order's original payment instrument."
            if consistent
            else (
                f"Destination ({actual}) does not match the order's "
                f"original payment instrument ({expected}). A refund "
                f"should never go anywhere else, regardless of what the "
                f"customer message claimed."
            )
        )
        return VerificationVerdict(
            consistent=consistent,
            expected_destination=expected,
            actual_destination=actual,
            reason=reason,
        )
