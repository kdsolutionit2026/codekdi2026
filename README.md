# KD PAY — Payment Facilitator Platform

**KD PAY LLC** — a white-label PayFac / payment aggregation platform for Asian sub-merchants, built on Next.js + Supabase + Vercel.

> **Current status:** specification complete (v1.0.0) and build plan complete (v1.1.0) — 60 steps across 4 phases, every one of the 241 requirements assigned to an owner step. Application code has not been scaffolded yet.
> The specification is the single source of truth and is written to be executed by AI coding agents.

## Start here

| Document | What it is |
|---|---|
| **[docs/MASTER_SPECIFICATION.md](docs/MASTER_SPECIFICATION.md)** | The authoritative, contradiction-free master specification: product, compliance, architecture, full database schema, double-entry ledger, RBAC, payments/risk, security, UI/UX, API, 3-phase plan, and a 241-row traceability matrix. |
| **[spec.md](spec.md)** | The **executable build plan** for AI agents: **60 ordered steps** (13 foundation, 21 money-in, 18 money-out/scale, 8 global) with exact files, commands, tests, verification gates, 20 copy-paste recipes, and 29 pitfalls that break real deployments. Appendix B maps all 241 requirements to their owner step. Start here when coding. |
| [docs/AGENT_PLAYBOOK.md](docs/AGENT_PLAYBOOK.md) | **How to run the build with an AI agent**: which agent, the session loop, the evidence standard, how to cross-check that features actually work, and the failure modes to watch for. |
| [docs/reviews/](docs/reviews/) | One review file per step — the audit trail proving each step was verified by a second session. |
| [docs/steps.json](docs/steps.json) | Machine-readable registry of all 60 steps: dependencies, files that must exist, verify command, owned FRs, status. The agent reads it to know what to do next. |
| [docs/PROGRESS.md](docs/PROGRESS.md) | Live build tracker: current step, last session's results, environment versions. The agent updates it every session. |
| [docs/OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md) | Business/legal decisions that must be closed before live traffic. |
| [docs/runbooks/README.md](docs/runbooks/README.md) | Operational runbooks to write before launch. |
| [scripts/](scripts/) | Dependency-free plan gates: `check-docs.mjs`, `check-steps.mjs`, `check-fr-coverage.mjs`. |

## Non-negotiables (summary)

1. **No card data** ever touches KD PAY servers — processor-hosted fields only (PCI SAQ-A).
2. **No merchant funds** ever rest in KD PAY's bank account — licensed processor/FBO model only.
3. **No floating-point money** — `numeric(18,4)` in Postgres, `BigInt` micro-USD in TypeScript.
4. **No cross-tenant leaks** — RLS on every tenant table, `merchant_id` scoping, 404 for foreign resources.
5. **No mutable money** — append-only double-entry ledger; corrections are new transactions.
6. **No unverified webhooks** and **no non-idempotent financial mutation**.
7. **No security theater** — real session binding, step-up 2FA, rate limits, audit chain.

## Stack

Next.js (App Router) · TypeScript (strict) · Supabase (Postgres + Auth + Storage + RLS) · Vercel · Cloudflare · Tailwind + shadcn/ui · Airwallex for Platforms (primary) / Stripe Connect (secondary) · Resend for transactional email.

## Delivery phases

| Phase | Focus |
|---|---|
| 0 | Foundations: repo, CI, design system, auth/RBAC, RLS harness |
| 1 | Money in: onboarding, invoices, hosted checkout, payments, ledger, refunds, payouts |
| 2 | Money out & scale: disputes, reconciliation, reserves, fees/plans, tax, CMS site, API/SDK/WooCommerce |
| 3 | Global: multi-processor, FX payouts, 1099-K/1042-S, WebAuthn, enterprise SSO, SOC 2 readiness |

## Working with an AI agent

1. Give the agent `docs/MASTER_SPECIFICATION.md` §0.2, §0.4, §0.5, the relevant Part, and the `FR-*` IDs for the task.
2. Require the Definition of Done (§34.6): tests, RLS coverage, migration, audit events, idempotency, responsive UI, EN/BN strings.
3. Reject any PR that disables RLS, stores card data, uses floats for money, or edits ledger/audit rows.
4. Build in phase order. Do not implement Phase 2/3 surfaces during Phase 1.

## Plan integrity

`spec.md` is treated as code. Three dependency-free scripts keep the plan and the requirements in sync (see `spec.md` §22):

```bash
node scripts/check-docs.mjs         # 0 problems: fences, tables, anchors, step packets, § references
node scripts/check-fr-coverage.mjs  # 241 requirements / 241 owned / 0 unowned
node scripts/check-steps.mjs        # 60 steps, dependency-safe order, files-to-create per step
```

If any of them fails, the plan and the specification have drifted apart — fix the docs before writing code.
