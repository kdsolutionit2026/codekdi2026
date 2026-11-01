# Change playbook — adding to KD PAY after it is built

The build plan is engineered for the *first* build (61 steps, 401 slices). This file is for everything after:
a new processor, a new country, a new currency, a pricing change, a breaking API change. It exists because
"easy to change later" is not a property you get from clean code — it comes from knowing, before you start,
**which files are safe to touch and which ones are load-bearing**.

## 1. Ask three questions in this order

| Question | If the answer is… | Then |
|---|---|---|
| Does this change a **rule** (a ledger posting, a money invariant, a tenancy boundary, a contract in §15)? | yes | **Stop.** ADR (`docs/adr/`) + `docs/OPEN_QUESTIONS.md` + master spec update *before* code. Tier A. |
| Is this a change to a **plan document** (a wrong path, a missing file, a terse bullet), not a rule? | yes | **Fast lane** — fix it in the same session, separate commit, keep the gates green (§5 below). |
| Which **surface** does it touch? | see §2 | Follow the recipe; it lists what to touch and what you are forbidden to touch. |

## 2. Blast-radius tiers

| Tier | What is in it | Review | Gate |
|---|---|---|---|
| **A — money, auth, tenancy** | `supabase/migrations/*`, `private.ledger_*`, `private.commit_payment`, RLS policies, `src/lib/money`, `src/lib/ledger`, session/step-up code, payout eligibility, refunds, dispute fund moves | **Human + second AI session**, other model family, read-only | Full unit gate + release gate, plus a ledger proof query and a tenancy 404 test |
| **B — behaviour** | routes, server actions, workers, adapters, risk rules, reports, emails, PDFs, API/webhook payloads | AI review is enough if the slice is reviewed and green; human on anything user-visible in money flows | Unit gate + contract tests |
| **C — presentation, docs** | UI copy, CMS templates, docs, tests, tooling | Auto-merge on green | Slice gate (<60 s) |

A change that starts in C and discovers a Tier A need **stops** and gets re-cut. That is the most common way
a "small" change becomes an incident.

## 3. Recipes

Each recipe: **touch** these files, **do not touch** these, and **prove** it this way. The "do not touch" column
is the point — it is where the design's invariants live.

| # | Change | Touch | Do not touch | Prove |
|---|---|---|---|---|
| R1 | **New payment processor** | `src/lib/processors/<name>.ts` implementing `PaymentProcessor` (frozen in S0.14, normative in master spec §4.1); its capability flags; a row in `normalize.ts` mapping vendor codes → `declineClass`; processor row/config + env schema; CSP entries if it serves hosted fields; recorded fixtures | Checkout orchestration, ledger, risk, invoice state machine. If you must change one, the contract is wrong → ADR first | `tests/contract/provider-<name>.test.ts` green; one sandbox payment end-to-end; replayed webhook dedupes |
| R2 | **New currency** | Currency config row (code + ISO 4217 exponent), money parser/formatter, ledger account provisioning, statements/rounding, payout rail availability | Any assumption that money has 2 decimals — JPY is 0, KWD is 3; `numeric(18,4)` storage does **not** change, only display and rounding | Property test round-trip at exponent 0/2/3; per-currency ledger balance; one sandbox payment |
| R3 | **New country / KYB flow** | Country config (allowed MCCs, required documents, sanctioned-list config, tax rules, AVS/3DS availability), **versioned** checklist rows | Forking the onboarding wizard per country; a checklist is data with a version — applications in flight keep the version they started under | Golden-file test of the checklist; an in-flight application is unaffected when v2 publishes |
| R4 | **New payment method** (bank transfer, wallets, async) | Checkout `payment_methods` capability flag, provider capability flag, state machine states (async: `pending → paid`), webhook events, receipt, posting *timing* | Adding a second ledger builder — reuse the existing ones. A new posting *timing* is a new documented rule, not a new code path | Async state-machine test; double-post guard; refund path for the new method |
| R5 | **Change how the ledger posts** | Nothing directly. This is a **Tier A rule change**: ADR, a new posting rule with an effective date, and never a rewrite of history | `ledger_entries` / `ledger_postings` rows, ever. Corrections are **reversing transactions** | Balance proof before/after; audit chain still verifies; ADR merged |
| R6 | **New report/export** | Report registry row, query in `features/reports` reading `ledger_entries` (+ `payments` for metadata), export column list, scheduled delivery via outbox | Recomputing money from `payments` totals — statements derive from the ledger only (pitfall 17) | Totals reconcile to the ledger for a seeded merchant; CSV columns additive only |
| R7 | **New permission / role** | Permission constant, role→permission row, RLS policy + isolation test, action wrapper, nav/UI gate, master spec RBAC matrix | A UI-only permission check; every permission is enforced server-side first | Isolation test: the new role cannot read a foreign tenant; 404 not 403 on foreign ids |
| R8 | **New language** | Message catalog key with EN+<new> parity test, PDF font with shaping for the new script, layout snapshots at 320 px | Hardcoded strings anywhere; `uppercase` transforms on non-Latin text | Parity test fails when a key is missing; snapshot at 320/768/1440 |
| R9 | **New webhook event type** | Master spec Appendix C, `EVENT_TYPES`, payload zod schema, delivery/replay docs | Renaming or removing an existing field. Events are **additive only**, forever | Contract test that a consumer ignoring unknown fields still passes; replay produces no duplicate side effects |
| R10 | **New CMS page/block** | Page registry, block schema, white-label tokens, cache tag, EN/BN copy | Hardcoded brand strings — logo, address, footer come from the platform profile only | Renders with a swapped logo/footer; cache tag invalidation test |
| R11 | **Pricing / fee change** | Pricing rows with `effective_from`; invoice stores the pricing version it was issued under | Rewriting issued invoices or historical statements; repricing is forward-only | An invoice issued before the change still renders its original numbers |
| R12 | **New step in the plan** | Packet in §3–§6A format with numbered `**Build**` items, registry row with `effort`, FR ownership + Appendix B, then `node scripts/gen-slices.mjs --write` | Renumbering existing steps (append `S1.5b` instead) | All four plan gates green |

**If a recipe's "do not touch" column is in your diff, stop and write the ADR.** That column is the whole
design distilled: one provider interface, one ledger posting function, one event shape, one money type,
one tenant scoping rule, one pricing-versioned invoice.

## 4. Public surfaces: version before you need to

Merchants build against these. Breaking one silently is how a platform loses a customer at 2 a.m.

| Surface | Version scheme | Breaking change means |
|---|---|---|
| REST API | Path major (`/api/v1`) + date-pinned behaviour via header | New major; v1 runs **≥ 6 months** in parallel |
| Webhook events | Pinned per endpoint; payload is **additive only** | A new endpoint version; never mutate an existing event |
| Hosted checkout / embed | Script URL is versioned (`checkout.js?v=2`) | Both script versions served during migration |
| SDKs | Semver; deprecations warn for one minor before removal | Major bump + migration guide |
| Invoice / receipt PDFs | Document `version` field on the rendered artefact | New template version; old artefacts are **never** re-rendered |
| CSV exports | Columns additive; never reorder or rename | New export type, old one retained |
| Email templates | Versioned rows, not code | New template row; in-flight sends keep theirs |

**Deprecation procedure** (the same every time):

1. Ship the replacement and announce it — dashboard banner + email, **≥ 90 days** before removal.
2. Send `Deprecation` and `Sunset` headers on every v-old API response; log which merchants still use it.
3. Dual-run both versions, with a per-merchant flag to flip early.
4. Remove only when the usage log is zero for 30 consecutive days — or the sunset date passes and the
   merchant has been warned three times.
5. Changelog entry, plus a line in `docs/PROGRESS.md`.

## 5. Two classes of plan change (the fast lane)

§20.3 says "a step may not change a rule". Correct — but read literally it also means a typo in a packet
stops the build and waits for a human, which in practice means the rule gets bypassed. So:

| Class | Examples | Procedure |
|---|---|---|
| **Plan defect** | wrong file path, missing dependency, terse `**Build**` bullet, an estimate that was obviously wrong, a missing test name | Fix it **in the same session**, in a **separate commit** (`docs: fix S1.5 path`), keep all four plan gates green, add one line to `docs/PROGRESS.md`. No approval needed. |
| **Rule change** | ledger posting, money precision, tenancy boundary, a §15 signature, FR scope, phase order | **Stop.** `docs/OPEN_QUESTIONS.md` → decision → master spec + `spec.md` + registry in one PR. Tier A. |

The distinction is *who is harmed by being wrong*. A wrong path wastes an hour; a wrong ledger rule loses
money six months later. Anything that changes what the system guarantees is a rule change, no matter how
small the diff looks.

Every fixed plan defect also gets a line in `docs/TROUBLESHOOTING.md` if it was a symptom someone could hit
again — that file is how the next person (or agent) skips the hour you just spent.

## 6. What must never change without an ADR

1. `ledger_entries` and `ledger_postings` are append-only; corrections are reversing entries.
2. Money is never a JS float; `numeric(18,4)` in Postgres, integer micro-units in TypeScript.
3. Every tenant table has RLS with `force`, and a foreign id returns **404**, never 403.
4. The audit log is hash-chained and append-only; checkpoints are signed daily.
5. Card data never touches our servers (PCI SAQ-A); processor-hosted fields only.
6. Merchant funds never rest in a KD PAY bank account.
7. The four S0.14 contracts (money, ledger, `PaymentProcessor`, normalised event) change by ADR + version bump + fixture update in one PR.
8. Migrations are additive-first: expand → migrate code → contract later.
9. Every new table ships RLS + isolation test + exposure block in the same migration.

## 7. How you know it is still easy to change

| Signal | Healthy | Act when |
|---|---|---|
| Escaped defects per 10 slices | falling or flat | rising → under-specified slice, not a missing feature |
| Median time from "bug reported" to "red test that reproduces it" | < 1 hour | > 1 day → the reproduce step is missing from `TROUBLESHOOTING.md` |
| Slices merged without human review (Tier C) | > 50 % | falling → slices are too big or too risky; re-cut |
| Plan gates red on `main` | never | once means the gate is decorative; fix before the next change |
| Recipes used with an empty "do not touch" diff | always | a hit means the contract needs an ADR |
| New provider / country / currency added | data + one adapter, no core edits | core edits → the abstraction leaked; fix the seam, not the call site |
