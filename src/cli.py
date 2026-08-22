"""Entry point for the vertical slice.

    python -m src.cli --scenario attack
    python -m src.cli --scenario benign
    python -m src.cli --scenario attack --audit-log var/attack_run.jsonl
    python -m src.cli --scenario benign --rail razorpay   # needs test-mode keys

`--reasoner` defaults to `naive` and is pinned deliberately. The CLI now loads
.env for the Razorpay credentials, which also puts ANTHROPIC_API_KEY on the
environment -- and `default_reasoner()` switches to a real LLM call whenever it
sees that. That would silently make `make demo` cost money and stop being
reproducible, so the default is explicit rather than inferred. `--reasoner auto`
restores the old inferring behaviour.

`--rail razorpay` runs against the real API (src/tool/razorpay_api.py) and
needs RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET plus an order carrying a captured
payment id. `--rail mock` (the default) needs nothing and is what the demo and
the eval harness use.
"""

from __future__ import annotations

import argparse
import sys

from dotenv import load_dotenv

from src.agent.reasoner import LLMReasoner, NaiveReasoner, default_reasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore, VelocityTracker
from src.models import MerchantPolicy, OrderRecord
from src.pipeline import run_scenario
from src.safety.policy_gateway import PolicyGateway
from src.scenarios import ORDERS, SCENARIOS
from src.tool.razorpay_api import RazorpayAPIClient, RazorpayRefundRail
from src.tool.razorpay_mock import MockRazorpayClient
from src.verification.verifier import Verifier

DEFAULT_POLICY = MerchantPolicy(
    max_single_amount=50_000.0,
    max_daily_amount=100_000.0,
    max_daily_count=5,
)


def main(argv: list[str] | None = None) -> int:
    # eval/run.py does the same at import; the CLI needs it too now that
    # --rail razorpay reads credentials from the environment.
    load_dotenv()

    parser = argparse.ArgumentParser(description="Run one Warden vertical-slice scenario.")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="attack")
    parser.add_argument("--audit-log", default="var/audit_log.jsonl")
    parser.add_argument(
        "--rail",
        choices=["mock", "razorpay"],
        default="mock",
        help="mock (default, no setup) or razorpay (real test-mode API)",
    )
    parser.add_argument(
        "--reasoner",
        choices=["naive", "llm", "auto"],
        default="naive",
        help="naive (default: offline, deterministic, hijackable by design) | "
             "llm (real Anthropic call, costs money, non-deterministic) | "
             "auto (llm if ANTHROPIC_API_KEY is set).",
    )
    parser.add_argument(
        "--payment-id",
        default=None,
        help="Rebuild the order from a real captured Razorpay payment "
             "(pay_...). Mint one with scripts/checkout_fixture.py.",
    )
    args = parser.parse_args(argv)

    order_store = OrderStore()
    for order in ORDERS:
        order_store.register(order)

    live_client = None
    if args.payment_id:
        # Rebuild the scenario's order from a REAL captured payment, so the
        # amount and the instrument are Razorpay's own values rather than
        # fixture constants. Mint one with scripts/checkout_fixture.py.
        live_client = RazorpayAPIClient.from_env()
        payment = live_client.fetch_payment(args.payment_id)
        if payment.get("status") != "captured":
            print(f"CANNOT RUN: {args.payment_id} is '{payment.get('status')}', not captured.")
            return 2
        instrument = payment.get("vpa") or f"{payment.get('method')}:{payment.get('bank') or '-'}"
        remaining = (payment["amount"] - payment.get("amount_refunded", 0)) / 100
        if remaining <= 0:
            print(f"CANNOT RUN: {args.payment_id} is fully refunded "
                  f"(Rs.{payment['amount']/100:,.2f} already returned).")
            print("            Mint a fresh one: python scripts/checkout_fixture.py")
            return 2
        # A refund is funded from merchant balance, not from the original
        # payment, so the refundable amount is bounded by BOTH. Razorpay
        # reports an over-balance refund as a bare "invalid request sent"
        # with no field and no reason, so cap it here and say so plainly
        # rather than let the demo die on an opaque 400.
        balance = live_client.fetch_balance() / 100
        refundable = min(remaining, balance)
        base = ORDERS[0]
        order_store.register(
            OrderRecord(
                order_id=base.order_id,
                original_payment_instrument=instrument,
                refund_amount=refundable,
                razorpay_payment_id=args.payment_id,
            )
        )
        print(f"LIVE ORDER  {args.payment_id}  instrument={instrument}")
        print(f"            Rs.{remaining:,.2f} unrefunded · Rs.{balance:,.2f} merchant balance"
              f" · refunding Rs.{refundable:,.2f}")
        if refundable < remaining:
            print("            (capped by BALANCE, not by the payment -- a refund is a fresh")
            print("             disbursement, so it can fail for reasons unrelated to the payment)")
        if refundable <= 0:
            print("CANNOT RUN: nothing refundable. Mint a fresh payment: "
                  "python scripts/checkout_fixture.py")
            return 2
        print()

    ledger = AuditLedger(args.audit_log)
    safety_gate = PolicyGateway(DEFAULT_POLICY, VelocityTracker())

    if args.rail == "razorpay":
        try:
            client = live_client or RazorpayAPIClient.from_env()
        except RuntimeError as exc:
            print(f"CANNOT RUN: {exc}")
            return 2
        if not client.is_test_mode:
            print("REFUSING: RAZORPAY_KEY_ID is not a test-mode key (rzp_test_...).")
            print("          This repo never runs against live keys.")
            return 2
        tool_client = RazorpayRefundRail(client)
        rail_label = "ACT (razorpay)"
    else:
        tool_client = MockRazorpayClient()
        rail_label = "ACT (mocked)  "

    print(f"=== Warden vertical slice — scenario: {args.scenario} · rail: {args.rail} ===\n")

    result = run_scenario(
        args.scenario,
        reasoner=(
            NaiveReasoner() if args.reasoner == "naive"
            else LLMReasoner() if args.reasoner == "llm"
            else default_reasoner()
        ),
        safety_gate=safety_gate,
        tool_client=tool_client,
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
        print(f"3. {rail_label}  tx_id: {exec_result.tx_id}  status: {exec_result.status}\n")
    elif result.get("inexpressible") is not None:
        print(f"3. {rail_label}  NOT EXPRESSIBLE -- the gate passed it, but Razorpay's refund")
        print("                  API has no field for a payee, so there is no request to send.\n")
    else:
        print(f"3. {rail_label}  SKIPPED -- blocked by the safety gate before it reached the rail.\n")

    print(f"4. VERIFY         consistent: {verdict.consistent}")
    print(f"                  {verdict.reason}\n")

    if result.get("inexpressible") is not None:
        exc = result["inexpressible"]
        print("RESULT: *** ACTION NOT EXPRESSIBLE ON THE RAZORPAY API. *** No money moved.")
        print(f"        {exc}")
        print("        Not a policy decision -- a fact about the API's shape. A refund")
        print("        carries no payee, so the diverted action has no request to send.")
    elif not policy_verdict.allowed:
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
