# 0010 — The real Razorpay rail, and the threat-model correction it forced

Date: 2026-08-23
Status: accepted

## Context

Track 01 is the only Buildathon track that grants Razorpay test-mode API
access, and its brief names those APIs explicitly
(`docs/decisions/0001-gate-0-resolved.md`). Warden's execution stage was
`MockRazorpayClient`, which returns `f"mock_rfnd_{uuid4().hex[:12]}"` and
makes no network call. Choosing the sandbox track and not using the sandbox
is the most attackable thing in the submission: a Razorpay judge opens
`src/tool/` and sees `uuid.uuid4()`.

While reading the API docs to build the client, a fact surfaced that matters
more than the wiring:

> **`POST /v1/payments/:id/refund` has no destination parameter.** The entire
> documented request body is `amount`, `speed`, `notes`, `receipt`. Refunds
> return to the original payment instrument, and there is no field in which
> to name anywhere else.

Source: [Create a Normal Refund](https://razorpay.com/docs/api/refunds/create-normal/),
[Pay Refunds to Customers](https://razorpay.com/docs/payments/refunds/).

## The problem this creates

Warden's `payee_scope` rule enforces *"destination must equal the original
payment instrument."* **Razorpay enforces the identical constraint at the
rail, structurally.** So against the real refund API, the payee-diversion
attack — the one Haiku 4.5 falls for 47.7% of the time, and the whole of
Beat 1 in `submission/demo-script.md` — **cannot succeed even with Warden
switched off.** There is no field for the attacker's UPI handle.

Discovering this on stage would collapse Beat 1. Discovering it now does
something better.

## Decision

### 1. Wire the real rail, transport-fake first

`src/tool/razorpay_api.py` — `RazorpayAPIClient` (real HTTP, Basic auth,
paise conversion, Razorpay's error envelope) plus `RazorpayRefundRail`, a
drop-in for the mock. `src/tool/fake_razorpay.py` — a `requests.Session`-shaped
in-process fake, so the client's real auth, serialization and error mapping
execute in tests and **only the socket is fake**. Opt in with
`python -m src.cli --rail razorpay`; `--rail mock` stays the default so the
eval harness and demo are untouched.

The client refuses to run against a key that isn't `rzp_test_`.

### 2. Make the finding executable, not prose

The fake rejects **any** request key outside `{amount, speed, notes, receipt}`
with a 400. `tests/test_razorpay_api.py::TestDestinationIsInexpressible`
parametrizes over `destination`, `payee`, `vpa`, `account`, `fund_account_id`
— every name a compromised agent might reach for — and asserts each is
rejected. The claim "you cannot redirect a Razorpay refund" is now something
the test suite demonstrates.

### 3. `DestinationNotExpressible`, not a generic refusal

When a proposed payee isn't the original instrument, `RazorpayRefundRail`
raises **before any network call**, because there is no request that could
express it. The pipeline audits this as its own event, `ACTION_INEXPRESSIBLE`,
distinct from `ACTION_BLOCKED`. The distinction is the point: the gateway
makes a *decision*; this reports a *fact about the API's shape*.

### 4. Correct the threat model rather than hide the correction

Beat 1 is reframed, not deleted:

- **Payee diversion is real for RazorpayX Payouts**, which take an arbitrary
  fund account. It is *not* real for the Payments refund API. The corpus's
  diversion attacks are therefore a payouts-shaped threat demonstrated on a
  refunds-shaped scenario, and the writeup must say so.
- **Denial is unaffected**, and this makes it more important, not less. No API
  design can prevent an agent from simply never calling the endpoint. The one
  attack class every model fails 39/39 is exactly the one Razorpay's own
  structural defense cannot touch.

## Alternatives considered

**Wire RazorpayX Payouts instead**, where diversion is genuinely expressible.
Rejected: RazorpayX test access requires a business account, which a student
applicant does not have. Naming the product boundary precisely is a better
answer than a demo we cannot run.

**Quietly keep the mock and say nothing.** Rejected — it is the single
weakest point in the submission and a judge finds it in ninety seconds.

**Delete Beat 1.** Rejected. The 47.7% compromise rate and the 62/62 catch
are real measurements about *model behaviour*; what changed is which Razorpay
product they map onto. Deleting them would discard a true result to avoid
explaining a nuance.

## Consequences

- **The thesis gains a production witness.** ADR 0007 argues authority should
  be bound to trusted state rather than accepted from the caller. Razorpay's
  refund API *is* that argument, shipped. Warden generalises a principle a
  payments company already validated — which is a far stronger position than
  proposing one.
- **`OrderRecord` gains `razorpay_payment_id`** (optional). A real refund is
  against a captured *payment*, not an abstract order — an asymmetry the mock
  hid and which is now named in its docstring.
- **The rail is a genuine structural backstop.** Over-refunding is rejected by
  the API itself (ADR 0008's amount-binding attack fails at the rail as well
  as the gate), and diverted payees are unrepresentable.
- **CLOSED 2026-08-23 — verified end to end against live test-mode keys.**
  Real captured payment `pay_TSy9UxOPeF9lXs` (netbanking, Rs.1,250), real
  refund `rfnd_TSyITyRbE6z72y`, gate allowed, verifier agreed, audit chain
  intact. The attack scenario on the same live rail is refused at
  `payee_scope` and never reaches the API.
- **The live run found what the fake could not:** refunds are funded from
  *merchant balance*, not from the payment being refunded, and an
  over-balance refund returns a bare `invalid request sent` with no field or
  reason. See Finding 19 — it is independent corroboration of ADR 0009, since
  a correctly-decided, correctly-called refund can still leave a customer
  unpaid. `fetch_balance()` was added and the live CLI caps at
  `min(unrefunded, balance)`.
- **Two things the live run also forced.** `.env` is now loaded by the CLI,
  which silently switched `default_reasoner()` to a real LLM call; `--reasoner`
  now defaults to `naive` explicitly so `make demo` stays free and
  reproducible. And Razorpay test mode rejects the generic
  `4111 1111 1111 1111` Visa as an *international* card while UPI is not
  enabled on a fresh account — the fixture uses netbanking, which needs no
  instrument details at all.
- Tests: 24 → 47.
