"""Entry point for the vertical slice.

    python -m src.cli --scenario attack
    python -m src.cli --scenario benign
    python -m src.cli --scenario attack --audit-log var/attack_run.jsonl
"""

from __future__ import annotations

import argparse
import sys

from src.agent.reasoner import default_reasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore, VelocityTracker
from src.models import MerchantPolicy
from src.pipeline import run_scenario
from src.safety.policy_gateway import PolicyGateway
from src.scenarios import ORDERS, SCENARIOS
from src.tool.razorpay_mock import MockRazorpayClient
from src.verification.verifier import Verifier

DEFAULT_POLICY = MerchantPolicy(
    max_single_amount=50_000.0,
    max_daily_amount=100_000.0,
    max_daily_count=5,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one Warden vertical-slice scenario.")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="attack")
    parser.add_argument("--audit-log", default="var/audit_log.jsonl")
    args = parser.parse_args(argv)

    order_store = OrderStore()
    for order in ORDERS:
        order_store.register(order)

    ledger = AuditLedger(args.audit_log)
    safety_gate = PolicyGateway(DEFAULT_POLICY, VelocityTracker())

    print(f"=== Warden vertical slice — scenario: {args.scenario} ===\n")

    result = run_scenario(
        args.scenario,
        reasoner=default_reasoner(),
        safety_gate=safety_gate,
        tool_client=MockRazorpayClient(),
        verifier=Verifier(),
        ledger=ledger,
        order_store=order_store,
    )

    action = result["action"]
    policy_verdict = result["policy_verdict"]
    exec_result = result["execution"]
    verdict = result["verdict"]

    print(f"1. REASON+DECIDE  proposed destination: {action.destination_account}")
    print(f"                  rationale: {action.rationale}\n")

    print(f"2. SAFETY GATE    allowed: {policy_verdict.allowed}" + (f"  rule fired: {policy_verdict.rule_fired}" if not policy_verdict.allowed else ""))
    print(f"                  {policy_verdict.reason}\n")

    if exec_result is not None:
        print(f"3. ACT (mocked)   tx_id: {exec_result.tx_id}  status: {exec_result.status}\n")
    else:
        print("3. ACT (mocked)   SKIPPED -- blocked by the safety gate before it reached the rail.\n")

    print(f"4. VERIFY         consistent: {verdict.consistent}")
    print(f"                  {verdict.reason}\n")

    if not policy_verdict.allowed:
        print("RESULT: *** ATTACK BLOCKED BEFORE EXECUTION. *** No money moved.")
        if not verdict.consistent:
            print("        Verification independently agrees it would have been wrong -- two")
            print("        different mechanisms catching the same attack, not one point of failure.")
    elif verdict.consistent:
        print("RESULT: refund executed to the correct destination.")
    else:
        print("RESULT: *** MONEY MOVED TO THE WRONG ACCOUNT AND THE SAFETY GATE MISSED IT. ***")
        print("        The gate allowed something verification disagrees with -- investigate the")
        print("        policy configuration before trusting this run.")

    ok, chain_message = ledger.verify_chain()
    print(f"\n5. AUDIT          {args.audit_log}: {chain_message}")
    if not ok:
        print("        WARNING: audit chain failed verification.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
