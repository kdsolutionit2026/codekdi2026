# 0001 — Freeze money, ledger, provider and event contracts

- **Date:** 2026-11-01
- **Status:** accepted
- **Step / slice:** S0.14.1
- **Tier:** A (money/auth/tenancy)

## Context

The build plan is split into 401 slices of at most one agent-day so that no single agent session carries a
step that is too large for its context. That fixes two defect classes (context truncation, multi-concern
diffs) and **worsens a third**: interface drift. With four times as many sessions touching the codebase, two
agents will independently invent a different shape for the same concept — a `refundPayment` that returns a
boolean in one slice and throws in another, an event named `payment.succeeded` in one adapter and
`payments.success` in the next.

The same argument applies to the four concepts that cross the most boundaries: money, ledger posting,
the processor adapter, and the webhook event. Each is imported by 15–40 later steps. Deciding them late means
deciding them 40 times, differently.

## Decision

Before any feature step, S0.14 lands four **types-only** files plus a contract test:

1. `src/lib/money/types.ts` — `Money = string`, branded `MicroUsd`, parser/formatter signatures.
2. `src/lib/ledger/types.ts` — entry draft, posting, result, and `postLedger(tx, posting)` signature, with
   field names copied verbatim from master spec §8.7 so SQL and TypeScript cannot disagree.
3. `src/lib/processors/types.ts` — the **existing, already normative** `PaymentProcessor` interface from
   master spec §4.1 (15 methods), `ProcessorCapabilities` from §4.4, `ProcessorError`, and the canonical
   status/decline enums. Ported verbatim: this step freezes it, it does not design it.
4. `src/lib/processors/events.ts` — one `NormalizedEvent` shape, `VerifiedEvent`, and `EVENT_TYPES` from
   Appendix C. Adapters normalise into it; nothing else invents event names.

Runtime logic may not be added to these files. They change only by a new ADR that supersedes this one, with
the contract fixture updated in the same PR.

## Consequences

**Easier.** A new processor is one adapter file (`CHANGE-PLAYBOOK.md` R1), because the interface and the
normalisation target already exist. A ledger caller cannot disagree
with the SQL function. Event handling is written once. Parallel agent sessions can no longer invent competing
shapes, because the compiler rejects them.

**Harder.** The first version of each contract has to be right enough to survive the whole build; a mistake
here is felt by every later step. This is why S0.14 is gated in Phase 0 and why a deliberate field rename must
turn the contract test red.

**Revisit.** After Phase 1, when real processor traffic has exercised `PaymentProcessor` and the event shape.
Any friction found then is expected to be *additive*; a breaking change needs ADR 0002.

## Alternatives considered

- **Let contracts emerge from usage.** Rejected: with ~400 slices, "emerge" means 400 chances to diverge, and
  interface drift is the defect class that splitting makes worse, not better.
- **Generate types from the database schema only.** Rejected as sufficient: it freezes storage, not the
  provider boundary or the event shape, which are the two places drift actually costs money.
- **One mega `types.ts`.** Rejected: four small files with one contract test each are reviewable in a day;
  a single file becomes the shared-conflict hotspot.

## Proof

`tests/contract/interface-freeze.test.ts` — schema snapshots, a `satisfies` fixture per contract, no duplicate
event types, every type matches `domain.action`. Renaming a field on a scratch branch must make it red; that
negative test is part of the S0.14 `**Done when:**`.
