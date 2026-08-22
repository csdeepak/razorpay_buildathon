"""Completeness checking: a DETECTIVE control for undischarged obligations.

Motivated directly by evaluation evidence (docs/eval-findings.md Finding 11):

    Claude Sonnet 5 resisted 130 of 130 diversion attacks and fell for 15 of
    15 denial attacks.

Denial attacks are the gap neither defense in this project addresses. Model
alignment is heavily trained against "send the money somewhere else" and has
no defense against "don't send it at all." And the policy gateway
(src/safety/) cannot help either: its whole mechanism is refusing a proposed
action, and a denial attack proposes nothing. There is no bad action to
block -- a good action is *suppressed*.

So this is deliberately a different SHAPE of control:

    Gateway (src/safety/)         preventive   "may this action proceed?"
    Completeness (here)           detective    "was every obligation met?"

It runs AFTER a session ends and raises for human review. It cannot prevent
the harm -- the customer already went unpaid -- but the harm from a denial
attack is unbounded in time, not instantaneous: an unpaid refund flagged
within the hour is a service failure, while one nobody ever notices is theft
by omission.

THE DESIGN CONSTRAINT THAT MAKES IT SOUND
-----------------------------------------
The obligation is read from TRUSTED STATE, never from the conversation or
from order notes -- the same discipline as payee_scope and amount_binding
(ADR 0008). This is what makes the check non-injectable.

Concretely, every denial case in the corpus works by making a *claim*:
"REFUND ALREADY PROCESSED, ref RFND-88213", "this SKU is final-sale",
"the request was filed in error". Each is a claim about state. This checker
never reads those claims. It asks the ledger whether a refund actually
exists, and the case record whether a request is actually open. A forged
note cannot change either.

WHY NOT PUT THIS IN THE SEMANTIC LAYER
--------------------------------------
ADR 0007 reserved a semantic/judgment layer for what cannot be decided
deterministically, and ADR 0008 established the rule: anything answerable
from trusted state belongs in the deterministic layer, where it is provable
and carries no false-positive risk. "Is there an open refund request with no
corresponding disbursement?" is answerable from trusted state. So it lives
here, deterministically, and the semantic layer is still unspent.
"""

from __future__ import annotations

from pydantic import BaseModel

from src.models import OrderRecord


class CompletenessVerdict(BaseModel):
    """Outcome of a post-session obligation audit."""

    complete: bool
    obligation: str | None = None
    reason: str

    @property
    def needs_review(self) -> bool:
        return not self.complete


class CompletenessChecker:
    def check(
        self,
        order: OrderRecord,
        *,
        refund_request_open: bool,
        refund_paid_total: float,
    ) -> CompletenessVerdict:
        """Audit one closed session against its obligations.

        `refund_request_open` and `refund_paid_total` must both come from
        trusted records -- the case/ticket system and the payment ledger --
        never from the agent's account of what happened.

        Note what is deliberately NOT checked: whether the amount paid equals
        the amount owed. Partial refunds are legitimate (ADR 0008), so a
        part-payment discharges the obligation for this control's purposes.
        Under-refunding is a different concern and would need its own rule.
        """
        if not refund_request_open:
            return CompletenessVerdict(
                complete=True,
                reason="No open refund request on this order; nothing was owed.",
            )

        if refund_paid_total > 0:
            return CompletenessVerdict(
                complete=True,
                reason=(
                    f"Open refund request discharged: {refund_paid_total} paid "
                    f"against order {order.order_id}."
                ),
            )

        return CompletenessVerdict(
            complete=False,
            obligation="open_refund_request",
            reason=(
                f"UNDISCHARGED OBLIGATION on order {order.order_id}: a refund "
                f"request is open in the case record and the payment ledger "
                f"shows no disbursement. The session ended without paying it. "
                f"Any claim that a refund was already issued, or that the order "
                f"is ineligible, is contradicted by trusted state and must be "
                f"reviewed by a human."
            ),
        )
