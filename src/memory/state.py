"""The 'memory' stage: ground-truth state the rest of the pipeline looks up
or records into, kept separate from anything the agent reads out of chat.

Thin by design (depth allocation table, src/README.md) -- in-memory for the
vertical slice, not a database. What matters is architectural, not
technological.
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.models import OrderRecord


class OrderStore:
    """The reasoner's fallback destination and the verifier's expected
    answer both come from here, never from the inbound message."""

    def __init__(self) -> None:
        self._orders: dict[str, OrderRecord] = {}

    def register(self, order: OrderRecord) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: str) -> OrderRecord:
        try:
            return self._orders[order_id]
        except KeyError:
            raise KeyError(f"no order record for {order_id!r}") from None


class VelocityTracker:
    """Records executed-and-allowed spend so the safety gate
    (src/safety/policy_gateway.py) can enforce daily amount/count limits.

    Deliberately holds state only -- it doesn't decide anything itself, that
    stays the safety layer's job. 'Today' is a UTC calendar day; there's no
    real rolling-24h window here, which is an honest simplification for a
    16-day build, not an oversight.
    """

    def __init__(self) -> None:
        self._records: list[tuple[datetime, float]] = []

    def record(self, amount: float) -> None:
        self._records.append((datetime.now(timezone.utc), amount))

    def _today_records(self) -> list[tuple[datetime, float]]:
        today = datetime.now(timezone.utc).date()
        return [r for r in self._records if r[0].date() == today]

    def amount_spent_today(self) -> float:
        return sum(amount for _, amount in self._today_records())

    def count_today(self) -> int:
        return len(self._today_records())
