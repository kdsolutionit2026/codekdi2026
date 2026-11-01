# Architecture decisions (ADRs)

An ADR is required when a decision is one a reviewer could reasonably question in six months: a change to a
rule, a contract, a table shape, a money path, or a deliberate deviation from `spec.md`. One file per
decision, numbered, never deleted — superseding an ADR means writing a new one that says so.

`spec.md` §20.3 names this directory; S0.14's interface freeze is `0001`.

## Format (≥ 8 lines — short enough to actually be written)

```md
# NNN — <decision in one line>

- **Date:** YYYY-MM-DD
- **Status:** proposed | accepted | superseded by NNN
- **Step / slice:** S1.5.3
- **Tier:** A (money/auth/tenancy) | B (behaviour) | C (presentation)

## Context
What forced a decision. The constraint, the ambiguity, or the defect found. Facts only.

## Decision
What we will do, in the present tense. One paragraph, no hedging.

## Consequences
What becomes easier; what becomes harder or impossible; what must be revisited and when.

## Alternatives considered
Each with the reason it lost. "None" is not an answer.

## Proof
The test, query or gate that demonstrates the decision holds.
```

## Index

| # | Decision | Date | Status |
|---|---|---|---|
| [0001](0001-interface-freeze.md) | Freeze money, ledger, provider and event contracts | 2026-11-01 | accepted |

Add a row here in the same commit as the ADR. `node scripts/check-docs.mjs` does not verify this table — the
review rule is that an ADR without a row is an ADR nobody will find.
