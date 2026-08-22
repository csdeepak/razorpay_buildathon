"""Create the one captured test-mode payment the real refund rail needs.

Razorpay's API can create an *order* but cannot pay one -- a payment comes
from Checkout, which is a browser flow. So the fixture this repo needs (a
captured `pay_...` to refund against) takes exactly one manual step, and this
script reduces it to: run me, open the file I print, click pay.

    python scripts/checkout_fixture.py            # create order + write page
    python scripts/checkout_fixture.py --status   # list captured payments

Nothing here costs money. Test mode uses fake instruments end to end; the
card below is Razorpay's own published test card.

The generated page lands in `var/` (gitignored) because it embeds the
account's key id. That id is publishable by design -- it ships in the
checkout script of every Razorpay merchant's site -- but it is still
account-specific, so it is generated rather than committed.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys

import requests
from dotenv import load_dotenv

API = "https://api.razorpay.com/v1"
OUT = pathlib.Path("var/checkout.html")

# Razorpay's domestic test instruments. The generic 4111-1111-1111-1111 Visa
# is rejected by Indian test mode as an *international* card, so UPI is the
# default path here -- and it matches the demo's domain, since every order in
# this project was paid with a UPI handle.
TEST_UPI = "success@razorpay"
TEST_CARD = "4111 1111 1111 1111"

PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Warden — test-mode checkout fixture</title>
<style>
  body {{ font: 16px/1.6 system-ui, sans-serif; max-width: 42rem;
         margin: 4rem auto; padding: 0 1.5rem; background: #0E0B08; color: #EDE6DC; }}
  code {{ background: #1C1712; padding: .15em .4em; border-radius: 3px; color: #D9A353; }}
  button {{ font: inherit; background: #D9A353; color: #0E0B08; border: 0;
            padding: .8rem 1.6rem; border-radius: 4px; cursor: pointer; font-weight: 600; }}
  .card {{ border: 1px solid #2A2119; border-radius: 6px; padding: 1.25rem; margin: 1.5rem 0; }}
  #out {{ white-space: pre-wrap; word-break: break-all; }}
</style>
<h1>Test-mode checkout fixture</h1>
<p>This pays order <code>{order_id}</code> (₹{rupees:,.2f}) so the refund rail has a
captured payment to work against. <strong>Test mode — no real money.</strong></p>
<div class="card">
  <p><strong>Use Netbanking. No card number, no VPA, no OTP.</strong></p>
  <ol>
    <li>Click the button below</li>
    <li>Choose <strong>Netbanking</strong></li>
    <li>Pick any bank in the list — they are all simulated</li>
    <li>A mock bank page opens: click <strong>Success</strong></li>
  </ol>
  <p style="opacity:.7">Why not the others: <strong>UPI</strong> is not enabled
     on this test account, so it does not appear. <strong>Cards</strong> reject
     the generic Visa <code>{card}</code> as an international card. Netbanking
     needs no instrument details at all, which is why it is the path here.</p>
  <p style="opacity:.7">The method does not matter to what this fixture is for.
     A Razorpay refund returns to whatever instrument paid — that is the whole
     point being demonstrated, and it holds for netbanking exactly as it does
     for UPI.</p>
</div>
<button id="pay">Pay ₹{rupees:,.2f} (test)</button>
<div class="card" id="out">Payment id will appear here.</div>
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script>
document.getElementById('pay').onclick = function () {{
  new Razorpay({{
    key: "{key_id}",
    order_id: "{order_id}",
    amount: {paise},
    currency: "INR",
    name: "Warden (test fixture)",
    description: "Captured payment for the refund rail",
    handler: function (r) {{
      document.getElementById('out').textContent =
        "PAYMENT ID: " + r.razorpay_payment_id +
        "\\n\\nCopy that id — it is what the refund runs against.";
    }},
    modal: {{ ondismiss: function () {{
      document.getElementById('out').textContent = "Cancelled — reload to retry.";
    }} }}
  }}).open();
}};
</script>
"""


def creds() -> tuple[str, str]:
    load_dotenv(".env")
    kid = os.environ.get("RAZORPAY_KEY_ID", "")
    sec = os.environ.get("RAZORPAY_KEY_SECRET", "")
    if not kid or not sec:
        sys.exit("RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET missing from .env")
    if not kid.startswith("rzp_test_"):
        sys.exit(f"refusing to run: {kid[:9]}... is not a test-mode key")
    return kid, sec


def show_status(auth: tuple[str, str]) -> int:
    r = requests.get(f"{API}/payments", params={"count": 10}, auth=auth, timeout=20)
    r.raise_for_status()
    items = r.json().get("items", [])
    captured = [p for p in items if p["status"] == "captured"]
    if not captured:
        print("No captured payments yet. Run without --status, then pay in the browser.")
        return 1
    print(f"{len(captured)} captured payment(s):\n")
    for p in captured:
        refunded = p.get("amount_refunded", 0)
        print(f"  {p['id']}  Rs.{p['amount']/100:,.2f}  refunded=Rs.{refunded/100:,.2f}  {p.get('method')}")
    print("\nUse one of these ids as OrderRecord.razorpay_payment_id.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--amount", type=float, default=1250.0, help="rupees (default 1250)")
    ap.add_argument("--status", action="store_true", help="list captured payments and exit")
    args = ap.parse_args()

    kid, sec = creds()
    auth = (kid, sec)

    if args.status:
        return show_status(auth)

    paise = round(args.amount * 100)
    r = requests.post(
        f"{API}/orders",
        auth=auth,
        timeout=20,
        json={
            "amount": paise,
            "currency": "INR",
            "receipt": "warden-refund-fixture",
            "notes": {"purpose": "captured payment for the Warden refund rail"},
        },
    )
    if r.status_code != 200:
        sys.exit(f"order creation failed [{r.status_code}]: {r.text[:300]}")
    order_id = r.json()["id"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        PAGE.format(
            order_id=order_id,
            paise=paise,
            rupees=args.amount,
            key_id=kid,
            card=TEST_CARD,
            upi=TEST_UPI,
        ),
        encoding="utf-8",
    )

    print(f"Order created: {order_id}  (Rs.{args.amount:,.2f}, test mode)")
    print(f"Checkout page: {OUT.resolve()}")
    print("\nOpen that file in a browser and pay with the test card shown on it.")
    print("Then run:  python scripts/checkout_fixture.py --status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
