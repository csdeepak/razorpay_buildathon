"""Entry point for the Day 6-7 vertical slice.

    python -m src.cli --scenario attack
    python -m src.cli --scenario benign
    python -m src.cli --scenario attack --audit-log var/attack_run.jsonl
"""

from __future__ import annotations

import argparse
import sys

from src.agent.reasoner import default_reasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore
from src.pipeline import run_scenario
from src.scenarios import ORDERS, SCENARIOS
from src.tool.razorpay_mock import MockRazorpayClient
from src.verification.verifier import Verifier


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one Warden vertical-slice scenario.")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="attack")
    parser.add_argument("--audit-log", default="var/audit_log.jsonl")
    args = parser.parse_args(argv)

    order_store = OrderStore()
    for order in ORDERS:
        order_store.register(order)

    ledger = AuditLedger(args.audit_log)

    print(f"=== Warden vertical slice — scenario: {args.scenario} ===\n")

    result = run_scenario(
        args.scenario,
        reasoner=default_reasoner(),
        tool_client=MockRazorpayClient(),
        verifier=Verifier(),
        ledger=ledger,
        order_store=order_store,
    )

    action = result["action"]
    exec_result = result["execution"]
    verdict = result["verdict"]

    print(f"1. REASON+DECIDE  proposed destination: {action.destination_account}")
    print(f"                  rationale: {action.rationale}\n")
    print(f"2. ACT (mocked)   tx_id: {exec_result.tx_id}  status: {exec_result.status}\n")
    print(f"3. VERIFY         consistent: {verdict.consistent}")
    print(f"                  {verdict.reason}\n")

    if verdict.consistent:
        print("RESULT: refund went to the correct destination.")
    else:
        print("RESULT: *** MONEY MOVED TO THE WRONG ACCOUNT, CAUGHT ONLY AFTER THE FACT. ***")
        print("        This is exactly the gap Day 8's safety gate closes -- see")
        print("        docs/progress-tracker.md. Today's pipeline is detective, not preventive.")

    ok, chain_message = ledger.verify_chain()
    print(f"\n4. AUDIT          {args.audit_log}: {chain_message}")
    if not ok:
        print("        WARNING: audit chain failed verification.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
