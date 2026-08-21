"""The 'memory' stage: ground-truth order records that the rest of the
pipeline looks up, kept separate from anything the agent reads out of chat.

Thin by design (depth allocation table, src/README.md) -- an in-memory dict
for the vertical slice, not a database. What matters is architectural, not
technological: the reasoner's fallback destination and the verifier's
expected answer both come from here, never from the inbound message.
"""

from __future__ import annotations

from src.models import OrderRecord


class OrderStore:
    def __init__(self) -> None:
        self._orders: dict[str, OrderRecord] = {}

    def register(self, order: OrderRecord) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: str) -> OrderRecord:
        try:
            return self._orders[order_id]
        except KeyError:
            raise KeyError(f"no order record for {order_id!r}") from None
