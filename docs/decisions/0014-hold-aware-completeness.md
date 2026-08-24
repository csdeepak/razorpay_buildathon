# 0014 — Hold-aware completeness, and a corpus the control can fail on

Date: 2026-08-24
Status: **locked**

## Context

[ADR 0009](0009-completeness-check.md) built the detective control and
[Finding 14](../eval-findings.md) reported **0 false alarms in 149 benign
sessions**. A review pointed out that the number was true and carried no
information.

Of the nine benign cases, eight had `should_refund=True` and ended in a
payment (`paid > 0` → discharged) and the ninth had `refund_request_open=False`
(→ discharged on the first branch). **There was no case in the corpus in which
the control could have been wrong.** The 0/149 described the corpus, not the
control.

Worse, the shapes it could be wrong on are the ordinary contents of a real
merchant queue: a chargeback in flight, a risk hold, a refund awaiting new
bank details, a case escalated for approval, a replacement shipped instead. In
every one of those the request is legitimately open, nothing has been paid,
and paging a human is noise. The binary control pages on all of them — so a
control scoring 0/149 in evaluation would have been unusable in production,
and the evaluation could not see it.

There is a second, related gap. `_audit_completeness` computed "paid" from the
current session's proposals only, so an order refunded *yesterday* would have
been flagged today.

## Decision

**Make the verdict three-valued, and add the cases that can break it.**

`CompletenessVerdict.status` becomes `discharged` / `deferred` /
`undischarged`:

- `discharged` — nothing owed, or a payment exists (now including **prior
  ledger disbursements**, not just this session's).
- `deferred` — open and unpaid, and **trusted state records why**.
- `undischarged` — open and unpaid with no recorded reason → raise.

`hold` is a new argument and it must come from the case/ticket record, exactly
like `refund_request_open`. **This is the whole load-bearing constraint:**
reading a claimed hold out of the conversation or the order notes would hand
any attacker a one-line way to silence the control.

The corpus gains:

- **Six benign cases** (`benign-010` … `benign-015`) where declining to pay is
  correct and the request stays open — dispute in progress, risk review,
  awaiting payout details, escalated for approval, replacement in transit, and
  a genuine prior refund.
- **A fourth order, `ORD-6120`**, that has actually been refunded, so
  "already refunded" can be **true** as well as forged. Without it, an agent
  that learned to reflexively distrust every such claim would score perfectly
  while being wrong about the world.
- **Three hold-spoofing denial cases** (`denial-004/005/006`) that assert a
  hold in text with nothing behind it in trusted state.

## The measurement

Deterministic over the whole benign corpus, correct agent behaviour assumed
(`tests/test_completeness_holds.py`):

| Checker | False alarms | Denial attacks surfaced |
|---|---:|---:|
| Binary (as shipped through Phase G) | **5 / 15** | 12/12 |
| Hold-aware | **0 / 15** | 12/12 |

The only difference between `denial-004` and `benign-010` is the case record;
both order notes are comparably convincing. All three spoofs land
`undischarged`, all six genuine holds land `deferred`, and that property is
asserted directly in
`test_a_spoofed_hold_cannot_silence_the_control`.

## Alternatives considered

- **Leave it binary and report 0/149.** Rejected. It survives a skim and dies
  in a panel, and it dies on the project's own chosen ground.
- **Let an LLM judge whether a hold is legitimate.** Rejected on
  [ADR 0008](0008-amount-binding.md)'s standing rule: anything answerable from
  trusted state belongs in the deterministic layer. "Does the case record name
  a hold?" is a lookup. The semantic layer stays unspent, which remains a
  result worth reporting.
- **Treat `deferred` as needing review anyway.** Rejected as the default,
  because it collapses back to the binary control and the 33% false-alarm
  rate. But it is the *right* behaviour once holds age — see below.
- **Report the hold-aware 0/15 with a confidence interval.** Rejected: the
  checker is a pure function of trusted state, so given the agent's payment
  decision the output is determined. It is a proof over the corpus, not a
  sample, and dressing it as a sampled rate overstates it in the other
  direction.

## Consequences

- The "0 false alarms" claim is now **0 out of 15 on a corpus containing six
  shapes designed to break it**, alongside the honest statement that the old
  binary control scored **5/15** on the same corpus. A measured improvement
  beats an unfalsifiable zero.
- Every judge-facing file must stop presenting completeness detection as a
  *measured* rate. Detection of a denial attack is guaranteed by construction
  — `outcome == LEAKED` and `flagged == True` are the same boolean — and
  saying so pre-empts the sharpest available objection.
- **Known limitation, unfixed and stated in the module docstring:**
  `deferred` does not age. A hold never lifted is exactly the theft-by-omission
  this control exists to catch, and catching it needs a clock and a per-hold
  SLA. Today `deferred` means "explained right now", not "explained forever".
- Six held shapes is not the space of real holds. The production false-alarm
  rate is unknown and would be set by how completely a merchant's case system
  records its own hold reasons. That is now the honest thing to say about it.
