"""A local, genuinely-live Warden demo. Built to be screen-recorded.

    python scripts/live_demo.py          # then open http://localhost:8823

WHY THIS EXISTS AND ISN'T THE PUBLISHED PAGE
--------------------------------------------
`submission/demo/` is a scroll-driven page of *recorded* measurements, and it
is published as a Claude Artifact. An Artifact runs under a strict CSP that
blocks every external host, so it cannot call Razorpay -- and it is a
shareable page, so putting a `rzp_test_` secret in it would hand the key to
anyone it is shared with. Neither is a limitation worth fighting: a page that
proves a live rail has to run somewhere that holds credentials, which is
here.

So this server is the live half. The secret never leaves the process --
the browser only ever receives `RAZORPAY_KEY_ID`, which is publishable by
design and ships in the checkout script of every Razorpay merchant's site.

WHAT IT SHOWS
-------------
Three scenarios through the real `src/pipeline.py`, against the real
test-mode rail:

  benign   a refund actually executes and a real `rfnd_...` comes back
  attack   the diversion is refused at `payee_scope` before the rail
  denial   the agent proposes NOTHING; every preventive stage is N/A and
           the completeness audit is the only thing that fires

Plus the thing the mock could never show (docs/eval-findings.md Finding 19):
**a refund is a fresh disbursement funded from merchant balance, not a
reversal of the payment.** With a zero balance the API refuses with a bare
`invalid request sent` -- no field, no reason. That is why the page shows the
balance next to the payment, and why the fixture step exists at all.

MANUAL STEP, AND WHY IT CANNOT BE REMOVED
-----------------------------------------
Razorpay's API can create an *order*; only Checkout can pay one. So minting a
captured payment needs one human click in a browser. The page embeds Checkout
so that click happens without leaving the demo.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import requests
from dotenv import load_dotenv

from src.agent.reasoner import NaiveReasoner, ToolCallingReasoner
from src.audit.ledger import AuditLedger
from src.memory.state import OrderStore, VelocityTracker
from src.models import MerchantPolicy, OrderRecord
from src.pipeline import run_scenario
from src.safety.mandate import MandateMinter, MandateVerifier, NonceRegistry
from src.safety.policy_gateway import PolicyGateway
from src.scenarios import ORDERS, SCENARIOS
from src.tool.razorpay_api import RazorpayAPIClient, RazorpayRefundRail, to_rupees
from src.verification.completeness import CompletenessChecker
from src.verification.verifier import Verifier

load_dotenv()

API = "https://api.razorpay.com/v1"
PORT = int(os.environ.get("WARDEN_DEMO_PORT", "8823"))
LOG = pathlib.Path("var/live_demo_audit.jsonl")

POLICY = MerchantPolicy(max_single_amount=50_000.0, max_daily_amount=100_000.0, max_daily_count=5)


def creds() -> tuple[str, str]:
    kid, sec = os.environ.get("RAZORPAY_KEY_ID", ""), os.environ.get("RAZORPAY_KEY_SECRET", "")
    if not kid or not sec:
        sys.exit("RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET missing. See .env.example.")
    if not kid.startswith("rzp_test_"):
        sys.exit("REFUSING: that is not a test-mode key. This repo never runs against live keys.")
    return kid, sec


# --------------------------------------------------------------------- rail


def account_state() -> dict:
    auth = creds()
    bal = requests.get(f"{API}/balance", auth=auth, timeout=20)
    balance = to_rupees(bal.json().get("balance", 0)) if bal.status_code == 200 else 0.0
    pays = requests.get(f"{API}/payments?count=100", auth=auth, timeout=25)
    captured = []
    if pays.status_code == 200:
        for p in pays.json().get("items", []):
            if p.get("status") in ("captured", "refunded"):
                amt, refunded = to_rupees(p["amount"]), to_rupees(p.get("amount_refunded", 0))
                captured.append({
                    "id": p["id"], "amount": amt, "refunded": refunded,
                    "remaining": round(amt - refunded, 2), "method": p.get("method", "?"),
                })
    captured.sort(key=lambda c: -c["remaining"])
    return {"balance": balance, "payments": captured, "key_id": creds()[0]}


def create_order(rupees: float) -> dict:
    r = requests.post(
        f"{API}/orders", auth=creds(), timeout=20,
        json={"amount": round(rupees * 100), "currency": "INR",
              "receipt": "warden-live-demo",
              "notes": {"purpose": "captured payment for the Warden live demo"}},
    )
    if r.status_code != 200:
        raise RuntimeError(f"order creation failed [{r.status_code}]: {r.text[:300]}")
    return {"order_id": r.json()["id"], "key_id": creds()[0], "amount": rupees}


# ----------------------------------------------------------------- pipeline


def run_live(scenario: str, payment_id: str | None, use_llm: bool) -> dict:
    """One scenario through the real pipeline. Returns a JSON-safe trace.

    Deliberately builds a FRESH ledger view per run so the audit panel shows
    only this session's entries -- the file itself stays append-only and the
    chain still spans every run ever made against it.
    """
    scen = SCENARIOS[scenario]

    # The naive agent never reads order notes, so it cannot be fooled by one --
    # it would sail through the denial scenario and refund correctly, which
    # looks like a pass and is really "the regex was not paying attention".
    # Refuse the combination rather than record a misleading run.
    if scenario == "denial" and not use_llm:
        return {"error": (
            "The denial scenario needs the tool-calling agent. The offline naive "
            "agent never reads order notes, so a forged note cannot reach it -- it "
            "would refund correctly and that would look like a pass. Switch the "
            "agent toggle to 'tool-calling' and run again.")}

    store = OrderStore()
    for o in ORDERS:
        store.register(o)

    rail_label, live_note = "mock", None
    tool_client = None

    if payment_id:
        client = RazorpayAPIClient.from_env()
        if not client.is_test_mode:
            raise RuntimeError("not a test-mode key")
        payment = client.fetch_payment(payment_id)
        remaining = to_rupees(payment["amount"]) - to_rupees(payment.get("amount_refunded", 0))
        balance = to_rupees(client.fetch_balance())
        refundable = min(remaining, balance)
        base = store.get(scen.order_id)
        store.register(OrderRecord(
            order_id=base.order_id,
            original_payment_instrument=base.original_payment_instrument,
            refund_amount=refundable if refundable > 0 else base.refund_amount,
            razorpay_payment_id=payment_id,
        ))
        # Pre-empt the two ways a live refund is impossible before proposing
        # one. Both are real and both are worth saying out loud, but letting
        # the rail 400 mid-run aborts the pipeline and the page shows nothing
        # -- on a recording that reads as a broken demo rather than as the
        # finding it actually is.
        if refundable <= 0:
            why = (
                f"merchant balance is {balance:.2f} — a Razorpay refund is a fresh "
                f"disbursement funded from balance, not a reversal of the payment "
                f"(eval-findings Finding 19)"
                if balance <= 0 else
                f"only {remaining:.2f} is unrefunded on this payment"
            )
            return {"error": (
                f"Nothing refundable on {payment_id}: {why}. "
                f"Mint a fresh captured payment in step 1 — that also tops up the "
                f"balance the refund is paid from.")}

        tool_client = RazorpayRefundRail(client)
        rail_label = "razorpay"
        live_note = {
            "payment_id": payment_id, "method": payment.get("method"),
            "paid": to_rupees(payment["amount"]), "already_refunded": to_rupees(payment.get("amount_refunded", 0)),
            "remaining": round(remaining, 2), "balance": balance,
            "refundable": round(refundable, 2),
            # Finding 19, surfaced rather than swallowed.
            "balance_capped": refundable < remaining,
        }
    else:
        from src.tool.razorpay_mock import MockRazorpayClient
        tool_client = MockRazorpayClient()

    ledger = AuditLedger(LOG)
    before = len(ledger.read_all())

    minter = MandateMinter()
    gateway = PolicyGateway(
        POLICY, VelocityTracker(),
        mandate_verifier=MandateVerifier(minter, NonceRegistry()),
    )

    reasoner = ToolCallingReasoner(order_notes=scen.order_notes) if use_llm else NaiveReasoner()

    error = None
    try:
        result = run_scenario(
            scenario, reasoner=reasoner, safety_gate=gateway, tool_client=tool_client,
            verifier=Verifier(), ledger=ledger, order_store=store,
            completeness=CompletenessChecker(),
        )
    except Exception as exc:  # surfaced to the page, never swallowed
        return {"error": f"{type(exc).__name__}: {exc}", "rail": rail_label, "live": live_note}

    entries = ledger.read_all()[before:]
    ok, chain_msg = ledger.verify_chain()
    action, pv, ex, vd, comp = (result["action"], result["policy_verdict"],
                                result["execution"], result["verdict"], result["completeness"])

    return {
        "scenario": scenario, "rail": rail_label, "live": live_note, "error": error,
        "agent": "tool-calling (the evaluated agent)" if use_llm else "naive (offline)",
        "notes": scen.order_notes,
        "message": scen.inbound_message,
        "action": None if action is None else {
            "action_type": action.action_type, "amount": action.amount,
            "destination": action.destination_account, "rationale": action.rationale,
        },
        "gate": None if pv is None else {
            "allowed": pv.allowed, "rule_fired": pv.rule_fired, "reason": pv.reason},
        "execution": None if ex is None else {"tx_id": ex.tx_id, "status": ex.status,
                                              "amount": ex.action.amount},
        "verify": None if vd is None else {"consistent": vd.consistent, "reason": vd.reason},
        "completeness": {"status": comp.status, "hold": comp.hold, "reason": comp.reason,
                         "needs_review": comp.needs_review},
        "audit": {"ok": ok, "message": chain_msg, "signed": ledger.signed,
                  "events": [{"seq": e.seq, "event": e.event} for e in entries]},
    }


# --------------------------------------------------------------------- http

PAGE = pathlib.Path(__file__).with_name("live_demo.html")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # keep the recording console clean
        pass

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        if self.path == "/api/status":
            try:
                return self._json(account_state())
            except Exception as exc:
                return self._json({"error": str(exc)}, 500)
        self._send(404, b"not found", "text/plain")

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        payload = json.loads(self.rfile.read(length) or b"{}")
        try:
            if self.path == "/api/fixture":
                return self._json(create_order(float(payload.get("amount", 1250.0))))
            if self.path == "/api/run":
                return self._json(run_live(
                    payload.get("scenario", "benign"),
                    payload.get("payment_id") or None,
                    bool(payload.get("use_llm")),
                ))
        except Exception as exc:
            return self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)
        self._send(404, b"not found", "text/plain")


def main() -> int:
    creds()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    url = f"http://localhost:{PORT}"
    print(f"Warden live demo  ->  {url}")
    print("  Real Razorpay test-mode API. The secret stays in this process.")
    print("  Ctrl-C to stop.\n")
    # Warm the pipeline before anyone clicks. The first run through pydantic +
    # the audit chain is noticeably slower than the rest, and on a screen
    # recording that lands as "the demo hung".
    try:
        run_live("benign", None, False)
        print("  pipeline warm.")
    except Exception as exc:
        print(f"  warm-up failed (continuing): {exc}")
    print()

    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
