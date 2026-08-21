# Submission Narrative

**Written Day 15**, after `eval/` has produced real numbers (Gate 4). Structure,
per `docs/context/Razorpay_16_Day_Battle_Plan.md` §5:

1. **Problem** — narrow, evidenced, tied to a verified fact about Razorpay
   (`docs/context/` or a later-dated ADR), not a generic "AI for payments" framing.
2. **Evidence** — what real conversations (`outreach/`) surfaced. Never a
   synthetic user, never implied to be one.
3. **Insight** — the one sentence that reframes the problem, usually the
   thing a real conversation revealed that the spreadsheet didn't.
4. **System** — the architecture, deep layers vs thin layers, and why that
   split (link the relevant ADR(s) in `docs/decisions/`).
5. **Results** — the adversarial evaluation numbers from `eval/`. Multi-seed
   where applicable. This is the section almost no other student submission
   will have.
6. **Why Razorpay should care** — tie back to a named, dated, sourced fact
   (CERT-In mandate, NPCI UAP, the Mathur "agent never sees" stance, the
   unshipped third-party agent ecosystem) — not a vague appeal to "the future
   of fintech."
7. **What's next** — the honest scope-cut list: what got deliberately left
   out and why, per `CLAUDE.md` rule 3 (ugly and working beats elegant and
   half-built).

README a stranger can run: make sure `src/README.md` (once populated) gives
setup instructions good enough that this narrative's claims are checkable.
