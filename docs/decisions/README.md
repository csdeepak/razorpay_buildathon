# Decisions (ADRs)

Every time something new is invented for this project — a locked problem, a
system design, a safety mechanism, a verification scheme, an evaluation
method, a naming/positioning choice worth defending to a judge — it gets a
numbered file here. This is the record that lets a future session (or a
Razorpay Q&A) reconstruct *why*, not just *what*.

Don't edit an old ADR to reflect a new choice. If a decision is superseded,
write a new ADR and note what it replaces — the old one stays as the honest
record of what was tried and why it changed.

Scaffold one with `/new-decision`, or copy the template below.

## Naming

`docs/decisions/NNNN-short-title.md`, zero-padded, sequential. Next number is
always (highest existing + 1). None exist yet — the first will likely be the
Day 5 problem lock.

## Template

```markdown
# NNNN — Title

Date: YYYY-MM-DD
Status: proposed | locked | superseded by NNNN

## Context

What situation forced this decision? What constraint, gate, or new fact
triggered it?

## Decision

What was decided, stated plainly enough that a judge could hear it back.

## Alternatives considered

What else was on the table and why it lost — especially if a "because I can"
temptation (e.g. an ASMOS feature) was rejected.

## Consequences

What this locks in, what it rules out, what it costs later if wrong.
```
