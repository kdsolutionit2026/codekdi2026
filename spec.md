# KD PAY — Build Plan for AI Agents (`spec.md`)

| Field | Value |
|---|---|
| **Plan version** | 1.0.0 |
| **Date** | 2026-10-29 |
| **Companion** | [`docs/MASTER_SPECIFICATION.md`](docs/MASTER_SPECIFICATION.md) — v1.0.0 (authority) |
| **Purpose** | Turn the master specification into an ordered, testable, resumable build sequence that an AI coding agent can execute without guessing. |
| **Audience** | AI agents (primary), the founder reviewing progress, any human contractor joining later. |

> **Start in 30 seconds:** open your AI agent and paste the prompt from §12 with `TASK: Execute step [S0.1]`. Then follow the session protocol in §0.3. Do not skip ahead to invoices or checkout — Phase 0 exists to make every later step safe.

---

## Contents

- [0. How to use this file](#0-how-to-use-this-file)
- [1. Engineering rules baked into the code](#1-engineering-rules-baked-into-the-code)
- [2. Toolchain, environment and reality checks](#2-toolchain-environment-and-reality-checks)
- [3. Bootstrap (S0.1–S0.2)](#3-bootstrap-s01s02)
- [4. Phase 0 — Foundations (S0.3–S0.13)](#4-phase-0--foundations-s03s013)
- [5. Phase 1 — Money In (S1.1–S1.21)](#5-phase-1--money-in-s11s121)
- [6. Phase 2 — Money Out & Scale (S2.1–S2.18)](#6-phase-2--money-out--scale-s21s218)
- [6A. Phase 3 — Global & Enterprise (S3.1–S3.8)](#6a-phase-3--global--enterprise-s31s38)
- [7. Implementation recipes](#7-implementation-recipes)
- [8. Migration map](#8-migration-map)
- [9. Test strategy and commands](#9-test-strategy-and-commands)
- [10. Deploy and promotion](#10-deploy-and-promotion)
- [11. Pitfalls that break real deployments](#11-pitfalls-that-break-real-deployments)
- [12. Per-step prompt template](#12-per-step-prompt-template)
- [13. Progress ledger and first commits](#13-progress-ledger-and-first-commits)
- [14. Global Definition of Done](#14-global-definition-of-done)
- [15. Core contracts — the shared code every step assumes](#15-core-contracts--the-shared-code-every-step-assumes)
- [16. Test infrastructure](#16-test-infrastructure)
- [17. Database roles and connection security](#17-database-roles-and-connection-security)
- [18. UI stack decisions (stop agents from mixing libraries)](#18-ui-stack-decisions-stop-agents-from-mixing-libraries)
- [19. Step registry and machine-readable tracking](#19-step-registry-and-machine-readable-tracking)
- [20. Definition of Ready, rollback and change control](#20-definition-of-ready-rollback-and-change-control)
- [21. Context management for agents (how to work without losing the plot)](#21-context-management-for-agents-how-to-work-without-losing-the-plot)
- [22. Documentation quality gates (the plan is code)](#22-documentation-quality-gates-the-plan-is-code)
- [Appendix A — Agent readiness self-audit](#appendix-a--agent-readiness-self-audit)
- [Appendix B — Requirement ownership map](#appendix-b--requirement-ownership-map)
- [Appendix C — Route inventory, permissions and caching](#appendix-c--route-inventory-permissions-and-caching)

---

## 0. How to use this file

### 0.1 What this file is

- **This file** answers **what to build, in what order, with which files, tests, and commands.**
- **`docs/MASTER_SPECIFICATION.md`** answers **what is correct** — rules, schema, ledger postings, RBAC, security, UX. When the two ever disagree, the master specification wins and this file gets fixed in the same PR.

Nothing here overrides the master spec's **Non-Negotiables** (`N-01`…`N-12`) or the **Contradiction Register** (`CR-01`…`CR-20`).

**Reference convention:** in this file, a bare `§X` means *this plan*; `master spec §X` means `docs/MASTER_SPECIFICATION.md`. When a step cites `master spec §8`, open that section — not this file's §8.

### 0.2 Session reading order (keep context small)

An AI agent should **never** load the whole repository or the whole master spec at once. Load in this order:

| # | Read | Why | Typical size |
|---|---|---|---|
| 1 | This file, §0, §1, §11 | Rules and known traps | ~250 lines |
| 2 | The **single step** you are executing (§3, §4, §5, §6 or §6A) | Scope | 25–45 lines |
| 3 | **§15** (core contracts) on your first session, then §17 (roles) if the step touches the DB | The shared helpers the step imports | ~450 lines once |
| 4 | Master spec **only** the sections referenced by that step | Correctness detail | 100–400 lines |
| 5 | The **recipe** (§7) for each pattern the step touches | Canonical code | 20–60 lines each |
| 6 | The step's row in `docs/steps.json` + its FRs in **Appendix B** | Machine-checkable scope + test proof | ~10 lines |
| 7 | `docs/PROGRESS.md` tail (last 3 entries) | Where the last agent stopped | ~30 lines |

If a step references §6.5–§6.6 of the master spec, read those sections, not all of Part IV.

### 0.3 Session protocol

Every work session follows the same five phases. Do not skip any.

```text
1) SYNC      git pull; pnpm install; supabase start; pnpm db:reset; run the verification
             commands of the LAST completed step. If they fail, fix that first — do not
             start new work on a broken baseline.
2) PLAN      Read the step packet. Write a 5–10 line plan + the exact file list into the
             PR description before editing anything. If the step is ambiguous, stop (§0.6).
3) BUILD     Implement in small commits. One migration per step unless the step says
             otherwise. Never edit a migration that is already committed and pushed.
4) VERIFY    Run the step's Verify block verbatim. Paste the output summary into the PR.
             A step is not done on "looks right"; it is done on green commands.
5) RECORD    Update docs/PROGRESS.md (template §13.1), tick the step checkbox here,
             update the traceability row in the master spec if behaviour changed, commit,
             push to arena/c7b6c1ec-codekdi2026.
```

### 0.4 Working rules for the agent

1. **One step per branch/PR.** PR title: `S1.5 ledger core (FR-LDG-001..006)`.
2. **Never invent schema.** If a table/column is missing, stop and raise it (§0.6) — do not add "temporary" tables.
3. **Never leave the app unrunnable.** A merge to `main` must always build, migrate from scratch, and pass tests.
4. **Never disable a control to pass a test.** Fix the code, or mark the test `test.fixme` with a linked issue **and** tell the human in the PR body.
5. **Ask before spending money or touching live data.** No live processor keys, no production database, no real emails to third parties.
6. **Deterministic output.** No random IDs in snapshots, no wall-clock in tests (inject `now()`), no network in unit tests.
7. **Small diffs.** Prefer 15 focused commits over 1 giant one. If a step exceeds ~800 changed lines, split it and say so.
8. **Leave breadcrumbs.** Every non-obvious decision goes into `docs/adr/NNN-*.md` (one short page) or a code comment linking to the spec section.

### 0.5 Commit and branch protocol

```bash
# from repository root, branch arena/c7b6c1ec-codekdi2026
git pull --rebase
git switch -c feat/S1.5-ledger-core        # short-lived working branch (optional)
git commit -m "feat(FR-LDG-001..006): ledger accounts, posting function, hash chain"
git push origin arena/c7b6c1ec-codekdi2026  # the session branch is the integration branch
```

- Conventional Commits, scope = step ID, body lists `FR-*` IDs.
- Migrations are **append-only**: `supabase/migrations/0012_ledger.sql` is never edited after it lands; corrections come as a new file, e.g. `0022_fix_ledger_index.sql`.
- Each commit must leave `pnpm verify` green (lint + typecheck + unit + integration + RLS).
- Pushes go **only** to `arena/c7b6c1ec-codekdi2026`.

### 0.6 Stop conditions — ask the human, do not guess

Stop and write the question into `docs/OPEN_QUESTIONS.md` **and** the PR body if:

| Situation | Why it must be escalated |
|---|---|
| A required table/column/endpoint does not exist in master spec §6/§18 | Inventing schema causes permanent rework |
| A rule conflicts with another rule | The master spec must be amended first |
| A task needs live processor credentials, a paid plan, or a legal decision | Money/compliance risk |
| A test reveals a ledger imbalance or double-charge | P1-class financial bug |
| A security control would have to be weakened | Never negotiate this alone |
| A phase-2 feature is required to finish a phase-1 step | Phase order is deliberate (master spec §34) |

For a schema gap, propose the exact migration in the question (columns, types, RLS, tests) so the human can answer with "yes" in one line.

### 0.7 Forbidden actions (hard stop, no exceptions)

- Storing, logging, or transmitting PAN/CVV/track data in any form, including test cards with free-form input.
- Disabling RLS, `force row level security`, or webhook signature verification — even in tests. (Use fixtures and test roles instead.)
- `Number`, `parseFloat`, or JS arithmetic on money.
- `UPDATE`/`DELETE` on `ledger_*` or `audit.log`.
- Merchant principal flowing through a KD PAY-owned bank account.
- Service-role keys, processor secrets, or `DATABASE_URL` in client bundles or `NEXT_PUBLIC_*`.
- Editing `supabase/migrations/*.sql` that are already on the remote branch.
- Committing `.env`, dumps, customer data, or KYC documents.
- "Security theater" (right-click blocking, devtools detection, hidden fields as controls).

---

## 1. Engineering rules baked into the code

### 1.1 The ten code-level invariants

| # | Invariant | Enforced by |
|---|---|---|
| 1 | Every tenant row carries `merchant_id` | Migration check + RLS test |
| 2 | Money is `numeric(18,4)` in PG and `bigint` micro-USD in TS | `src/lib/money` + ESLint `no-float-money` |
| 3 | Every financial mutation is idempotent | `idempotency_keys` + `withIdempotency()` |
| 4 | Every financial mutation writes ledger + audit + outbox **in one transaction** | `postLedger()` + `audit()` + `enqueue()` inside `withTenant()` |
| 5 | Unknown processor state never maps to success | adapter `normalizeStatus()` returns `requires_review` |
| 6 | Cross-tenant access returns 404 with zero data | `assertMerchant()` + RLS |
| 7 | Every list endpoint is cursor-paginated and bounded | `paginate()` helper, `limit ≤ 100` |
| 8 | Every server action validates input with Zod allowlists | `action()` wrapper |
| 9 | No side-effect (email/PDF/webhook) runs inside a request transaction | outbox → worker |
| 10 | Public content is ISR-cached; financial data is never CDN-cached | cache tags + `no-store` headers |

### 1.2 Conventions

| Area | Rule |
|---|---|
| Language | TypeScript `strict`; `noUncheckedIndexedAccess`; no `any` in `src/lib/{money,ledger,security,processors}` |
| File names | `kebab-case.ts`, React components `PascalCase.tsx`, SQL `0012_ledger.sql` |
| Exports | Named exports only; no default exports except Next.js page/layout/route files |
| DB access | Only through `src/lib/db/*`; no `postgres()` calls inside components |
| Money in APIs | Strings: `"1234.5600"`; never JSON numbers |
| IDs in APIs | Public prefixed IDs (`inv_…`, `pay_…`); internal UUIDs never exposed |
| Dates | `timestamptz` UTC in DB; ISO-8601 strings in APIs; merchant timezone only in UI |
| Errors | Typed `AppError` with `code`, `httpStatus`, `message`, `details`; no raw PG errors to users |
| Logging | `logger.info({ request_id, merchant_id, action, duration_ms })`; never log PII/tokens |
| Config | Everything editable (fees, limits, flags, branding) lives in DB; code holds only safe fallbacks |
| i18n | No literal user-facing strings in components; use `messages/en.json` + `bn.json` |
| Tests | Co-located unit tests (`*.test.ts`), integration in `tests/integration`, RLS in `tests/rls` |

### 1.3 Canonical module layout (create once, then respect)

```text
src/
├─ app/                                  # routes only; thin. No business logic.
├─ features/<domain>/
│  ├─ schema.ts        zod input/output types
│  ├─ queries.ts       read functions (server-only, RLS-aware)
│  ├─ actions.ts       "use server" mutations
│  ├─ service.ts       domain logic, pure where possible
│  └─ components/      domain UI
├─ lib/
│  ├─ db/              client, withTenant, withService, types, paginate
│  ├─ money/           MicroUsd, parse, format, allocate
│  ├─ ledger/          postLedger, account codes, builders
│  ├─ security/        session, csrf, rate-limit, crypto, redact, turnstile
│  ├─ processors/      types, registry, sandbox, stripe, airwallex
│  ├─ jobs/            outbox, worker, handlers
│  ├─ email/           transport, templates, send
│  ├─ pdf/             invoice, payout, statement, watermark, guilloche
│  ├─ storage/         signed upload/download, validate
│  ├─ flags/           feature flags
│  ├─ errors.ts  logger.ts  env.ts  i18n.ts
└─ messages/           en.json, bn.json
```

Rule: **`app/` never talks to the database directly** except for trivial `select` in a page when no domain logic is involved. Domain reads live in `features/<domain>/queries.ts`.

---

## 2. Toolchain, environment and reality checks

### 2.1 Versions

Pin exact versions in `package.json` + `pnpm-lock.yaml`, and record them in `docs/PROGRESS.md` and an ADR.

| Tool | Requirement | Notes |
|---|---|---|
| Node.js | ≥ 22 LTS | Needed for native `fetch`, `crypto`, and Next 15+ |
| pnpm | ≥ 9 | `corepack enable` |
| Docker Desktop / Engine | Required for `supabase start` | If unavailable, use a hosted dev Supabase project (see §2.4) |
| Supabase CLI | ≥ 2.x | `supabase --version` |
| Next.js | latest stable, **App Router** (≥ 15) | Node runtime for DB/PDF routes; Edge only for middleware |
| React | version bundled with Next | Do not upgrade independently |
| TypeScript | 5.x, `strict` | `noUncheckedIndexedAccess: true` |
| Tailwind CSS | v4 preferred, v3 acceptable | Map master spec §31.2 tokens either way |
| shadcn/ui | current CLI | Components are vendored into `src/components/ui` (owned code) |
| postgres.js | 3.x | Direct SQL; no ORM |
| @supabase/supabase-js & @supabase/ssr | current | Auth/Storage only for browser; DB via postgres.js |
| Zod | 3.23+ | Shared schemas |
| Vitest | 3.x | Unit + integration |
| Playwright | current | E2E + screenshots |
| pdf-lib | 1.17+ | No headless Chromium |
| Resend SDK | current | Transactional email |
| pino (+ pino-pretty in dev) | 9.x | Structured, redacted logs; **no `console.log` in domain code** (§15.2) |
| ulid | 2.x | Sortable request/job ids (§15.3) |
| lucide-react, sonner, recharts, clsx, tailwind-merge | current | The only UI libraries allowed (§18) |
| react-hook-form + @hookform/resolvers | 7.x / 3.x | Large forms only (§18) |
| next-intl | 3.x | EN/BN routing and message keys (§18) |
| @simplewebauthn/server + /browser | current | Passkeys (S3.4) |

### 2.2 Local setup (exact)

```bash
git clone https://github.com/kdsolutionit2026/codekdi2026 && cd codekdi2026
corepack enable
node -v            # must be >= 22
pnpm -v            # must be >= 9
docker info >/dev/null && echo "docker ok"
supabase --version
```

### 2.3 Environment variables

Create `.env.example` (committed) and `.env.local` (never committed). Full list in master spec Appendix A. Minimum for local development:

```bash
APP_ENV=local
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_MARKETING_URL=http://localhost:3000
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<from `supabase status`>
SUPABASE_SERVICE_ROLE_KEY=<from `supabase status`>     # server only
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres
DATABASE_URL_SERVICE=postgresql://postgres:postgres@127.0.0.1:54322/postgres
CRON_SECRET=dev-cron-secret
SESSION_PEPPER=dev-session-pepper
ENCRYPTION_KEK_BASE64=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=   # 32-byte dev key only
TURNSTILE_SECRET_KEY=1x0000000000000000000000000000000AA            # Cloudflare always-pass test secret
NEXT_PUBLIC_TURNSTILE_SITE_KEY=1x00000000000000000000AA             # always-pass test site key
PROCESSOR=sandbox
EMAIL_TRANSPORT=console
EMAIL_FROM=KD PAY <no-reply@notify.kdpay.test>
STT_TAX_PROVIDER=manual
```

Rules: `src/lib/env.ts` validates with Zod **at boot** and fails fast; no `process.env.X!` scattered in code.

### 2.4 Supabase local vs hosted

| Path | When | Commands |
|---|---|---|
| **Local (preferred)** | Docker available | `supabase init` → `supabase start` → `supabase db reset` |
| **Hosted dev project** | No Docker / limited laptop | `supabase link --project-ref <ref>` → `supabase db push`; never use the production project for development |

Local ports: API `54321`, DB `54322`, Studio `54323`, Inbucket (email capture) `54324`.

### 2.5 Platform limits that change the design (check before choosing a plan)

| Limit | Reality | Consequence for this build |
|---|---|---|
| **Vercel Cron** | Hobby: only **daily** cron jobs (max 2) | 1-minute workers (outbox, webhook retry, payout scheduler) require **Pro** or an external scheduler |
| **Vercel function duration** | Default ~10–15 s; configurable higher per plan | Set `export const maxDuration = 60` on worker routes; chunk work |
| **Supabase free tier** | Project pauses after inactivity; no PITR | Staging/prod need a paid plan before real traffic (PITR is the RPO requirement) |
| **Supabase connection limit** | Small on free tier | Use the **pooler** with `prepare: false`; `max: 1–3` per instance |
| **Server Action body size** | 1 MB default | Uploads go **direct to Storage** via signed URLs, never through actions |
| **Resend** | Requires a verified domain to send to third parties | Local uses `EMAIL_TRANSPORT=console`; staging uses a verified subdomain |
| **Cloudflare Turnstile** | Real keys needed for production | Test keys (`1x000…AA` / `1x000…AA`) always pass locally and in CI |

**Decision to make before S0.10:** Vercel Pro (simplest) **or** GitHub Actions cron calling `/api/internal/worker` with `CRON_SECRET` (free). The code must support both; only the scheduler differs.

---

## 3. Bootstrap (S0.1–S0.2)

### S0.1 — Repository scaffold and toolchain

**Goal:** a runnable Next.js app with strict TypeScript, Tailwind, shadcn/ui, Supabase CLI, and a clean folder layout.
**Depends on:** nothing. **Master spec:** §5.4, §5.5, §31. **Features:** none — infrastructure step (owns no FR). **Effort:** 1 agent-day.

**Build**

1. Scaffold **outside** the repo, then copy in (the repo already has `README.md`, `docs/`, `spec.md`):
   ```bash
   pnpm dlx create-next-app@latest /tmp/scaffold \
     --ts --tailwind --eslint --app --src-dir --import-alias "@/*" --use-pnpm --no-turbopack
   # copy everything except node_modules/.git/README
   rsync -a --exclude node_modules --exclude .git --exclude README.md /tmp/scaffold/ .
   pnpm install
   ```
2. `tsconfig.json`: `"strict": true`, `"noUncheckedIndexedAccess": true`, `"noImplicitOverride": true`, `"paths": { "@/*": ["./src/*"] }`.
3. Install the baseline dependencies:
   ```bash
   pnpm add postgres zod @supabase/supabase-js @supabase/ssr pdf-lib resend nanoid \
     pino lucide-react sonner recharts react-hook-form @hookform/resolvers \
     date-fns date-fns-tz clsx tailwind-merge next-intl
   pnpm add -D vitest @vitest/coverage-v8 vite-tsconfig-paths playwright @playwright/test \
     supabase @types/node tsx dotenv-cli fast-check @faker-js/faker
   pnpm dlx shadcn@latest init --base-color slate        # CSS variables on
   pnpm dlx shadcn@latest add button input textarea select checkbox switch radio-group \
     label badge card table tabs dialog sheet drawer dropdown-menu popover tooltip \
     sonner alert skeleton progress avatar separator breadcrumb pagination
   ```
4. Create the folder skeleton from §1.3 with `.gitkeep` files so the structure is visible.
5. `src/lib/env.ts` — Zod-validated env, exported as `env`. Fail fast with a readable message listing missing keys.
6. `package.json` scripts:
   ```json
   {
     "dev": "next dev",
     "build": "next build",
     "start": "next start",
     "lint": "next lint",
     "typecheck": "tsc --noEmit",
     "test": "vitest run --project unit",
     "test:integration": "vitest run --project integration",
     "test:rls": "vitest run --project rls",
     "test:e2e": "playwright test",
     "db:start": "supabase start",
     "db:reset": "supabase db reset",
     "db:types": "supabase gen types typescript --local > src/lib/db/schema.types.ts",
     "verify": "pnpm lint && pnpm typecheck && pnpm test && pnpm test:integration && pnpm test:rls"
   }
   ```
7. `pnpm exec supabase init` (creates `supabase/config.toml`), then set `db.port = 54322`, `api.port = 54321`, `studio.port = 54323`, `inbucket.port = 54324`.
8. `vitest.config.ts` with the three projects from §16.1 (verbatim).
9. `.gitignore`: add `.env*.local`, `.supabase/`, `test-results/`, `playwright-report/`, `coverage/`, `tests/.auth/`.
10. `docs/PROGRESS.md` from the template in §13.1. `docs/steps.json` is already committed (registry, §19) — read it, don't recreate it.
11. The three documentation gates from §19.1–§19.2 and §22 (`scripts/check-steps.mjs`, `scripts/check-fr-coverage.mjs`, `scripts/check-docs.mjs`), each wired to a script:
   ```json
   "check:steps": "node scripts/check-steps.mjs",
   "check:fr": "node scripts/check-fr-coverage.mjs",
   "check:docs": "node scripts/check-docs.mjs",
   "verify": "pnpm lint && pnpm typecheck && pnpm check:docs && pnpm check:fr && pnpm test && pnpm build"
   ```
12. `src/instrumentation.ts` calling `assertBootConfig()` so a missing env var fails at boot, not at checkout.

**Tests:** `src/lib/env.test.ts` proving a missing var throws a readable error; `node scripts/check-steps.mjs` prints the registry and exits 0.
**Verify:**
```bash
pnpm typecheck && pnpm lint && pnpm test && pnpm build
```
**Done when:** `pnpm dev` serves a page, `pnpm verify` is green, no `any`, no secrets committed.
**Commit:** `chore(S0.1): scaffold Next.js app, toolchain, env validation`

---

### S0.2 — CI quality gates

**Goal:** every push is checked automatically; broken code cannot merge.
**Depends on:** S0.1. **Master spec:** §5.9. **Effort:** 0.5 agent-day.
**Features:** `FR-NFR-005`, `FR-NFR-006`, `FR-SEC-014`.

**Build** `.github/workflows/ci.yml`:

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main, 'arena/**']
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  quality:
    runs-on: ubuntu-latest            # Docker is available: supabase start works here
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: pnpm }
      - uses: supabase/setup-cli@v1
        with: { version: latest }
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test
      - run: supabase start
      - run: supabase db reset
      - name: Export local Supabase env
        run: supabase status -o env >> "$GITHUB_ENV"     # API_URL, ANON_KEY, SERVICE_ROLE_KEY, DB_URL
      - run: pnpm db:types && git diff --exit-code src/lib/db/schema.types.ts
      - run: pnpm test:integration
      - run: pnpm test:rls
      - run: pnpm build
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ env.API_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ env.ANON_KEY }}
          SUPABASE_SERVICE_ROLE_KEY: ${{ env.SERVICE_ROLE_KEY }}
          DATABASE_URL: ${{ env.DB_URL }}
          DATABASE_URL_SERVICE: ${{ env.DB_URL }}
          CRON_SECRET: test
          SESSION_PEPPER: test
          ENCRYPTION_KEK_BASE64: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gitleaks/gitleaks-action@v2
        env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
```

> Cost/time note: `supabase start` pulls several images on a cold runner (2–4 min). It is cached on repeat runs. If it proves flaky, swap it for a `postgres:15` service, apply `supabase/migrations/*.sql` in order with `psql`, and create the `anon`/`authenticated`/`service_role` roles in `tests/sql/bootstrap.sql` — keep the same test commands. Never skip the migration + RLS steps.

**Also add** `eslint-rules/no-float-money.js` (custom rule): flags `.toFixed(`, `parseFloat(`, and arithmetic on identifiers matching `/amount|price|fee|balance|total/i` that are typed `number`. Start with a warning; flip to error in S1.5.
**Verify:** open a throwaway PR; CI must fail on a deliberate `const x: number = parseFloat("1.00")`, then pass when reverted.
**Done when:** required status check configured on `main`; CI < 12 min.
**Commit:** `ci(S0.2): add lint/typecheck/test/migration/secrets pipeline`

---

## 4. Phase 0 — Foundations (S0.3–S0.13)

Phase 0 outcome: one can sign in, the app knows who you are and what you may do, every table is tenant-isolated, every privileged action is audited, jobs run, and the public shell is branded from the database. **No invoices, no money yet.**

### S0.3 — Database bootstrap (extensions, schemas, roles, conventions)

**Goal:** a reproducible empty database with the right schemas, extensions, roles, and helper conventions.
**Depends on:** S0.2. **Master spec:** §6.1, §6.2, §6.14. **Features:** none — infrastructure step (owns no FR). **Effort:** 1 agent-day.

**Build** `supabase/migrations/0001_extensions_and_schemas.sql`:

```sql
create schema if not exists private;
create schema if not exists audit;
create extension if not exists pgcrypto   with schema extensions;
create extension if not exists citext     with schema extensions;
create extension if not exists pg_trgm    with schema extensions;
create extension if not exists btree_gin  with schema extensions;

revoke all on schema private from anon, authenticated;
revoke all on schema audit   from anon, authenticated;
grant  usage on schema public to anon, authenticated;

alter default privileges in schema public revoke all on tables from anon, authenticated;
```

Plus `0002_domains_and_helpers.sql` — **no `CREATE TYPE`**: statuses are `text` + `CHECK` (master spec §6.1). Instead create small helper domains:

```sql
create domain public.money_amount as numeric(18,4);
create domain public.currency_code as char(3);
comment on domain public.money_amount is 'All monetary values. Never float. See MASTER_SPECIFICATION §7.';
```

And create the shared trigger function:

```sql
create or replace function private.set_updated_at() returns trigger
language plpgsql as $$
begin new.updated_at = now(); return new; end $$;
```

Then `0002b_app_roles.sql` creates `app_runtime` and `app_service` exactly as in §17.1 (roles only, **no passwords** — they are set per environment). From here on, `DATABASE_URL` connects as `app_runtime` and `DATABASE_URL_SERVICE` as `app_service`; a test asserts `select current_user` returns `app_runtime` and that `rolbypassrls = false`.

**Tests** (`tests/integration/0001-bootstrap.test.ts`): schemas exist; `anon` cannot `usage` on `private`; `money_amount` rejects 5 decimals.
**Verify:** `supabase db reset && pnpm test:integration`
**Done when:** reset runs from zero in < 60 s and is repeatable.
**Commit:** `feat(S0.3): db bootstrap, schemas, domains, shared triggers`

---

### S0.4 — Design tokens, primitives and app shells

**Goal:** the visual foundation exists once and every later screen reuses it.
**Depends on:** S0.1. **Master spec:** §31.2–§31.7. **Effort:** 2 agent-days.
**Features:** `FR-UX-001..003`, `FR-UX-010`.

**Build**

1. `src/app/globals.css` — the token block from master spec §31.2 verbatim (`--bg`, `--surface`, `--primary`, semantic colors, radii, spacing, shadows, fonts). Tailwind v4: expose via `@theme inline`; Tailwind v3: mirror in `tailwind.config.ts`.
2. Fonts: Inter + Noto Sans Bengali via `next/font/google`, `display: swap`, CSS variable `--font-sans`.
3. `src/components/ui/*` — add shadcn primitives: button, input, textarea, select, checkbox, switch, radio-group, label, badge, card, table, tabs, dialog, sheet, drawer, dropdown-menu, popover, tooltip, toast/sonner, alert, skeleton, progress, avatar, separator, breadcrumb, pagination.
4. Custom primitives (this repo owns them):
   - `src/components/ui/money-input.tsx` — accepts `1,234.56`, formats on blur, emits a **string**, never a number.
   - `src/components/ui/status-badge.tsx` — maps every enum in master spec Appendix D → label + tone; **text is always present**.
   - `src/components/ui/data-table.tsx` — server pagination, sticky header, empty/loading/error states, column chooser, row actions.
   - `src/components/ui/empty-state.tsx`, `error-state.tsx` (shows `request_id`), `page-header.tsx`.
   - `src/components/ui/date-display.tsx` — merchant timezone + UTC tooltip.
5. Layouts: `(marketing)`, `(auth)`, `(merchant)/app`, `(admin)/admin` with responsive shells: sidebar 240 px ≥ 1024, collapsible tablet, bottom nav (Home, Payments, Money, Support, More) < 640.
6. `src/app/design/page.tsx` — a dev-only gallery rendering every primitive and every status badge (gate behind `APP_ENV !== 'production'`).

**Tests:** Playwright screenshot of `/design` at 320/768/1440; axe scan with zero serious violations; a unit test asserting `status-badge` covers **every** enum value.
**Verify:** `pnpm test && pnpm test:e2e --grep design`
**Done when:** no page defines raw hex colors; all spacing uses tokens.
**Commit:** `feat(S0.4): design tokens, ui primitives, responsive shells`

---

### S0.5 — Data access layer (postgres.js, tenant transactions, numeric safety)

**Goal:** one safe way to talk to Postgres, and no other.
**Depends on:** S0.3. **Master spec:** §5.3, §6.14, §23.1. **Effort:** 1.5 agent-days.
**Features:** `FR-TEN-004`, `FR-SEC-009`.

**Build** `src/lib/db/`:

Migration `0002b_app_roles.sql` (from §17.1) creates `app_runtime` and `app_service`. `DATABASE_URL` **must** use `app_runtime` — never `postgres` — and `DATABASE_URL_SERVICE` uses `app_service`. Add the §17.3 proof test; it is what keeps every later RLS test meaningful.

```ts
// client.ts  — server-only singleton
import 'server-only';
import postgres from 'postgres';
import { env } from '@/lib/env';

export const sql = postgres(env.DATABASE_URL, {
  max: 3,                 // per instance; pooled by Supavisor
  idle_timeout: 20,
  connect_timeout: 10,
  prepare: false,         // REQUIRED for transaction-mode pooler
  transform: { undefined: null },
});

export const sqlService = postgres(env.DATABASE_URL_SERVICE, {
  max: 3, idle_timeout: 20, connect_timeout: 10, prepare: false,
});
// env.ts rejects a superuser (`postgres`) URL in production — see §17.1.
```

```ts
// tenant.ts — full implementation in §15.6; this is the shape only
import postgres from 'postgres';          // namespace: postgres.TransactionSql
import { sql } from './client';

export type TenantContext = { userId: string; merchantId: string; sessionId: string; requestId: string };

export async function withTenant<T>(
  ctx: TenantContext,
  fn: (tx: postgres.TransactionSql) => Promise<T>,
): Promise<T> {
  return sql.begin(async (tx) => {
    await tx`select set_config('request.jwt.claims', ${JSON.stringify({ sub: ctx.userId, sid: ctx.sessionId })}, true)`;
    await tx`select set_config('request.request_id', ${ctx.requestId}, true)`;
    await tx`set local role authenticated`;   // app_runtime must be a member of authenticated (§17)
    return fn(tx);
  }) as unknown as Promise<T>;
}

export async function withService<T>(
  reason: string,
  fn: (tx: postgres.TransactionSql) => Promise<T>,
): Promise<T> {
  // service_role bypasses RLS: log every use for the audit trail
  logger.warn({ reason }, 'service_role transaction');
  return sqlService.begin((tx) => fn(tx)) as Promise<T>;
}
```

Also:
- `src/lib/db/assert-merchant.ts` — `assertMerchant(ctx, merchantId)` throws `NotFoundError` (→ 404) when not a member. **Every** merchant-scoped query calls it, even though RLS also enforces it.
- `src/lib/db/paginate.ts` — keyset pagination helper `(created_at, id) < (cursor_ts, cursor_id)`, `limit 1..100`, returns `{ rows, nextCursor, hasMore }`.
- `src/lib/db/schema.types.ts` — generated via `pnpm db:types`; regenerated after every migration (CI checks for drift).

**Critical test** (`tests/integration/numeric.test.ts`):

```ts
const [{ v }] = await sql`select 1234.5678::numeric(18,4) as v`;
expect(typeof v).toBe('string');      // postgres.js returns numeric as string — enforce it
expect(v).toBe('1234.5678');
```

If the driver ever returns a JS number, add an explicit type parser for OID `1700`. **A number here would silently corrupt money.**

**Verify:** `pnpm test:integration` green; `pnpm db:types` produces no diff.
**Done when:** grepping `src/` finds `postgres(` only inside `src/lib/db/client.ts`.
**Commit:** `feat(S0.5): db client, tenant/service transactions, pagination, numeric safety`

---

### S0.6 — Authentication with opaque server-side sessions

**Goal:** real sign-in with sessions the server can revoke instantly; no JWT in the browser.
**Depends on:** S0.5. **Master spec:** §20.1, §20.2, §6.4, `CR-04`. **Effort:** 2.5 agent-days.
**Features:** `FR-AUTH-001..007`, `FR-SEC-004`, `FR-SEC-010`, `FR-SEC-011`.

**Build**

1. Migration `0003_identity.sql` — `app_users`, `sessions`, `device_fingerprints`, `mfa_factors`, `recovery_codes`, `login_attempts`, `step_up_challenges`, `blocked_ips`, `rate_limit_counters` exactly as master spec §6.4, **plus**:
   - `sessions.active_merchant_id uuid references public.merchants(id)` (needed in S1.1, reserved here; see §15.7 for the multi-merchant rule);
   - `private.handle_new_auth_user()` + trigger `on_auth_user_created after insert on auth.users` (security definer) that inserts the matching `public.app_users` row. **Without this trigger, sign-up succeeds but `getSession()` cannot resolve a user** — a classic agent failure.
   - `sessions.token_hash bytea unique` and `sessions.rotated_from uuid` for rotation.
2. `src/lib/security/token.ts`:
   ```ts
   import { randomBytes, createHash, timingSafeEqual } from 'node:crypto';
   export const newToken = () => randomBytes(32).toString('base64url');       // 256-bit
   export const hashToken = (t: string) =>
     createHash('sha256').update(t + env.SESSION_PEPPER).digest();            // pepper from env
   export const safeEqual = (a: Buffer, b: Buffer) =>
     a.length === b.length && timingSafeEqual(a, b);
   ```
3. `src/lib/security/session.ts` — `createSession(userId, req)`, `getSession()` (cookie → row → user, checks `expires_at`, `absolute_expires_at`, `revoked_at`), `revokeSession(id)`, `revokeAllForUser(userId)`, `touchSession()` (throttled to 1 write/min).
4. Cookie: `__Host-kdpay_session`, `HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/`, `Max-Age` per role. **Never** `Strict`.
5. Sign-in flow: Supabase Auth verifies email+password (`signInWithPassword`) → we **discard** the Supabase tokens → create our own session row + cookie. Create the server-side Supabase client with `{ auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false } }` so supabase-js **never writes its own cookies**; the only cookies in the browser are `__Host-kdpay_session` and `__Host-kdpay_csrf`. TOTP enroll/verify also delegated to Supabase MFA, then recorded in `mfa_factors` + `sessions.mfa_level`.
6. `src/middleware.ts` — **Edge runtime, cookie only**: presence + redirect rules; no DB call. Full validation happens in `src/app/(merchant)/app/layout.tsx` and `(admin)/admin/layout.tsx` via `requireSession()`.
7. `src/app/(auth)/sign-in|sign-up|verify-email|reset-password|mfa/page.tsx` — Turnstile on sign-in/sign-up/reset; accessible forms; EN/BN labels.
8. Lockout: 3 fails → Turnstile required; 5–8 fails in 15 min → 15-min lock; record every attempt in `login_attempts`.
9. CSRF: double-submit token in a `__Host-kdpay_csrf` cookie + hidden field, verified in the `action()` wrapper (S0.7).

**Also configure** `supabase/config.toml`: `auth.site_url = "http://localhost:3000"`, `auth.additional_redirect_urls = ["http://localhost:3000/auth/callback", "http://localhost:3000/reset-password"]`, `inbucket.port = 54324`. Local verification emails land in Inbucket at `http://localhost:54324` (document this in `docs/PROGRESS.md` so no agent wonders why mail "isn't sending").

**Tests** (`tests/integration/session.test.ts`): sign-up creates `auth.users` **and** `app_users` (trigger); expired session → 401; revoked session → 401; rotation on privilege change; cookie flags asserted from `Set-Cookie`; replay from a different fingerprint → step-up required; `active_merchant_id` set automatically for a single-membership user.
**Verify:** `pnpm test:integration -- session` + manual sign-in/sign-out in the browser.
**Done when:** DB has a `sessions` row per login and deleting it logs the user out on the next request.
**Commit:** `feat(FR-AUTH-001..005): opaque sessions, sign-in, lockout, csrf`

---

### S0.7 — RBAC: roles, permissions, guards, server-action wrapper

**Goal:** every action is permission-checked in one place; UI visibility is derived, never trusted.
**Depends on:** S0.6. **Master spec:** §20.4, §6.4, §6.14. **Effort:** 2 agent-days.
**Features:** `FR-SEC-003`.

**Build**

1. Migration `0004_rbac.sql` — `roles`, `permissions`, `role_permissions`, `user_roles`, `merchant_members`, `approval_requests`, plus the scope trigger.
2. Seed `supabase/seed/002_rbac.sql` — the 10 platform roles, 6 merchant roles, and every permission code from master spec §20.4, mapped exactly to the matrices. **This is data, not code**; a test asserts the seed matches the documented matrix.
3. `src/lib/security/permissions.ts`:
   ```ts
   export type Permission = /* union generated from the seed */;
   export function can(grants: Set<Permission>, p: Permission): boolean;
   ```
4. SQL helpers from master spec §6.14 (`private.current_uid`, `private.has_permission`, `private.is_merchant_member`, `private.merchant_permission`, `private.assert_permission`).
5. `src/lib/actions/action.ts` — the wrapper every server action must use:

```ts
export function action<S extends z.ZodTypeAny, R>(opts: {
  schema: S;
  permission: Permission | ((input: z.infer<S>) => Permission);
  merchantScoped: boolean;
  idempotent?: boolean;
  audit?: string;
  handler: (input: z.infer<S>, ctx: Ctx) => Promise<R>;
}) { /* parse → csrf → session → permission → merchant assert → run → audit → return */ }
```

6. `requirePermission()` in layouts to build navigation; unauthorized nav items are **not rendered** and their routes return 404.
7. Seeded demo users for local dev (`supabase/seed/001_dev_users.sql`, password `devpassword123!`, staff + merchant roles) — **seed only runs locally**.

**Tests:** table-driven test: for each role × each permission in the matrix, `private.has_permission` returns the documented boolean. Any drift fails CI.
**Verify:** `pnpm db:reset && pnpm test:rls -- permissions`
**Done when:** the matrix is executable, and adding a permission without updating the matrix test fails.
**Commit:** `feat(FR-ADM-003): dual-scope rbac, guards, action wrapper`

---

### S0.8 — RLS foundation, exposure rules and the isolation harness

**Goal:** tenant isolation is structural and continuously proven.
**Depends on:** S0.7. **Master spec:** §6.15, §23, `N-04`, `FR-SEC-001`, `FR-TEN-001..003`. **Effort:** 2.5 agent-days.
**Features:** `FR-TEN-001`, `FR-TEN-002`, `FR-SEC-001`.

**Build**

1. There is **no separate RLS migration**: every migration that creates a table adds its RLS block in the same file (§7.9). This step writes the policies for `0003_identity.sql` and `0004_rbac.sql`, and adds `tests/rls/coverage.test.ts` as the permanent gate.
2. **Exposure block** applied to every public table (put it in a macro/comment block and copy it):

```sql
alter table public.<t> enable row level security;
alter table public.<t> force  row level security;
revoke all on public.<t> from anon, authenticated;   -- Supabase default grants exist; revoke first
grant select on public.<t> to authenticated;         -- reads only, writes via RPC
create policy <t>_merchant_read on public.<t>
  for select to authenticated using (private.is_merchant_member(merchant_id));
create policy <t>_staff_read on public.<t>
  for select to authenticated using (private.has_permission('<domain>.read'));
```

3. A policy for **every** table in §6.15 of the master spec (identity tables in this step; the rest as their tables arrive).
4. `tests/rls/harness.ts`:

```ts
export async function asUser<T>(userId: string, fn: (tx: Tx) => Promise<T>) {
  return sql.begin(async (tx) => {
    await tx`select set_config('request.jwt.claims', ${JSON.stringify({ sub: userId })}, true)`;
    await tx`set local role authenticated`;
    return fn(tx);
  });
}
```

5. `tests/rls/isolation.test.ts` — fixtures: merchant A (owner, finance, viewer), merchant B (owner), staff (analyst, superadmin). For **every** table with `merchant_id`: A cannot see B's rows (`count = 0`), and writing is impossible (permission denied on insert/update/delete).
6. `tests/rls/coverage.test.ts` — queries `pg_class`/`pg_policies`; **fails** if any table in `public` has `relrowsecurity = false`, or zero policies, or `relforcerowsecurity = false`.
7. `src/lib/db/assert-merchant.ts` returns `NotFoundError` (404) for foreign IDs, and logs `tenant.isolation.violation`.

**Tests:** the three suites above, plus a fuzz test hitting 20 representative queries with random foreign UUIDs.
**Verify:** `pnpm test:rls` — must be green and must fail if you comment out one policy.
**Done when:** the coverage test is the gatekeeper for every future table.
**Commit:** `feat(FR-SEC-001,FR-TEN-001..003): rls policies + isolation harness`

---

### S0.9 — Audit log with hash chain and signed checkpoints

**Goal:** tamper-evident record of every privileged action from day one.
**Depends on:** S0.8. **Master spec:** §22, `N-08`, `FR-AUD-001..003`. **Effort:** 2 agent-days.
**Features:** `FR-AUD-001..003`.

**Build**

1. Migration `0005_audit.sql` — `audit.log`, `audit.checkpoints` exactly as master spec §6.13; revoke all from `anon`/`authenticated`, grant `select` only to a staff-role function path.
2. `private.audit_write(...)` security-definer function: takes actor, merchant, action, entity, before/after JSON, request metadata; computes `hash = sha256(prev_hash || canonical_json(row))` under `pg_advisory_xact_lock(hashtext('audit'))`.
3. `src/lib/audit.ts` — `audit(tx, event)` typed helper; called **inside** the same transaction as the mutation.
4. `src/app/api/internal/audit-checkpoint/route.ts` — daily: verify the last 90 days, sign the chain head (Ed25519, key in env/KMS), insert into `audit.checkpoints`, alert on mismatch.
5. `/admin/audit` page (search by actor/merchant/action/entity/date, diff view, masked fields) — behind `audit.read`.

**Tests:** insert 100 events; verify chain; attempt `UPDATE audit.log` → error; tamper a row via a superuser → verification job detects and fails; checkpoint signature verifies.
**Verify:** `pnpm test:integration -- audit`
**Done when:** any mutation without an audit event fails a test that lists "mutations must audit". Maintain the list in `src/lib/audit-required.ts`.
**Commit:** `feat(FR-AUD-001..003): hash-chained audit log and checkpoints`

---

### S0.10 — Outbox, job worker, scheduler, feature flags

**Goal:** no side-effect blocks a request; jobs are retryable and observable.
**Depends on:** S0.8. **Master spec:** §5.7, §5.10, `FR-NFR-003`. **Effort:** 2 agent-days.
**Features:** `FR-TEN-005`, `FR-SEC-005`.

**Build**

1. Migration `0006_jobs_flags.sql` — `private.jobs`, `private.outbox`, `platform_feature_flags`, `merchant_feature_flags`, `metrics_events`.
2. `src/lib/jobs/outbox.ts` — `enqueue(tx, { topic, aggregateType, aggregateId, merchantId, payload, dedupeKey })`.
3. `src/lib/jobs/worker.ts` — claim with `for update skip locked`, per-topic advisory lock, retry with exponential backoff, dead-letter after `max_attempts`, structured logs with duration.
4. `src/app/api/internal/worker/route.ts` — `POST`, `CRON_SECRET` header check, `runtime = 'nodejs'`, `maxDuration = 60`, idempotent.
5. `vercel.json` (Pro path):
   ```json
   { "crons": [{ "path": "/api/internal/worker?topic=outbox", "schedule": "* * * * *" }] }
   ```
   Hobby/alternative path: `.github/workflows/cron.yml` runs `curl -X POST .../api/internal/worker -H "x-cron-secret: ${{ secrets.CRON_SECRET }}"` every 5 minutes.
6. `src/lib/flags.ts` — `isEnabled(key, merchantId?)` with DB lookup cached 30 s in-process; kill switches list from master spec §5.10.
7. `/api/health` — DB `select 1`, storage head request, last worker run age, migration version. Returns 200/503.

**Tests:** enqueue → worker processes exactly once (dedupe); forced failure → retries → dead letter; concurrent workers do not double-process; `/api/internal/worker` rejects without secret.
**Verify:** `pnpm test:integration -- jobs` + `curl` the endpoints locally.
**Done when:** a thrown error in a handler never blocks the HTTP request that created it.
**Commit:** `feat(FR-NFR-003): outbox, worker, cron, feature flags, health`

---

### S0.11 — Platform profile (white-label) and public shell

**Goal:** brand, address, header and footer come from the database — nowhere hardcoded.
**Depends on:** S0.4, S0.10. **Master spec:** §25.4, `FR-CMS-008`, `CR-02`. **Effort:** 1.5 agent-days.
**Features:** `FR-CMS-008`, `FR-NFR-002`.

**Build**

1. Migration `0007_platform_cms.sql` — `platform_settings` (single row, `id boolean primary key default true`), `cms_pages`, `cms_page_localizations`, `cms_page_versions`, `cms_navigation`, `media_assets`, `legal_versions`, `legal_acceptances`.
2. Seed the single `platform_settings` row + the 17 page slugs from master spec §27.2 (draft status, placeholder content).
3. `src/features/platform/queries.ts` — `getPlatformProfile()` cached with tag `platform:profile`, 1 h TTL; safe fallbacks **only** if the row is missing at boot.
4. Public shell `(marketing)/layout.tsx` renders logo, nav, announcement bar, footer columns, legal links, social — all from DB.
5. `/admin/platform/profile` — edit with preview, step-up 2FA, publish (versioned), `revalidateTag('platform:profile')`. Logo upload ≤ 2 MB using the storage helper built in S1.2; until S1.2 lands, a validated external URL field is acceptable and gets replaced in S1.2.
6. `sitemap.ts`, `robots.ts`, `manifest.ts`, OG metadata helpers; `noindex` on app/admin.

**Tests:** changing brand name in DB changes header + footer + emails (snapshot); contrast validator rejects a low-contrast accent color; publish invalidates cache.
**Verify:** `pnpm test:e2e --grep "platform profile"`
**Done when:** `grep -ri "KD PAY" src/app` returns only i18n keys and legal fallbacks.
**Commit:** `feat(FR-CMS-008): white-label platform profile and public shell`

### S0.12 — Security headers, CSP, edge controls and the "no theater" audit

**Goal:** the app is born with a strict, non-broken security posture instead of bolting headers on at launch.
**Depends on:** S0.6, S0.11. **Master spec:** §19, §21.5, `FR-SEC-002`, `FR-SEC-012`, `FR-SEC-013`, `FR-SEC-020`, `CR-14`. **Effort:** 1.5 agent-days.
**Features:** `FR-SEC-002`, `FR-SEC-012`, `FR-SEC-013`, `FR-SEC-020`.

**Build**

1. `src/middleware.ts` (single place, no per-route copies):
   - Generates a per-request nonce (`randomBytes(16).toString('base64')`), forwards it as a request header, and emits it in `Content-Security-Policy`.
   - Admin/app profile CSP: `default-src 'self'; script-src 'self' 'nonce-<n>' 'strict-dynamic'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https://<branding-bucket>; connect-src 'self' https://api.<domain> https://<processor-js-host>; frame-src https://<processor-js-host>; frame-ancestors 'none'; base-uri 'none'; form-action 'self'; object-src 'none'; upgrade-insecure-requests`.
   - Checkout profile: identical plus `frame-ancestors 'none'` and the minimum processor hosts; **no** marketing/analytics origins. Two profiles, one function, tested separately (§7.19).
   - `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()`, `Cross-Origin-Opener-Policy: same-origin`.
2. Edge controls checklist in `docs/OPERATIONS.md` (done in Cloudflare, verified by a script): WAF managed + OWASP rules, bot fight, DDoS L3/4 + L7, rate limiting rules at the edge, TLS 1.3 only + HSTS, DNSSEC enabled on the zone, `/app` and `/admin` bypass cache, `noindex` on private paths.
3. `scripts/check-headers.mjs` — fetches 6 routes (marketing, checkout, sign-in, app, admin, API) on staging and fails if any security header is missing, if `unsafe-eval` appears, or if `frame-ancestors` is absent.
4. Secret hygiene: `src/lib/env.ts` marks every server secret with `server-only`; a lint rule (`eslint-plugin-no-restricted-imports` or a custom `no-restricted-imports` entry) forbids importing `@/lib/env` from a client component; `scripts/check-env.mjs` fails the build if a server secret name appears in `.next/static/**`.
5. The "no security theater" audit (FR-SEC-020): a doc + a test asserting the app does **not** ship `contextmenu` blocking, devtools detection, `user-select: none` on body, clipboard blocking, or console-clearing loops. The real controls are session binding, CSP, CSRF, and step-up.
6. Add the header assertions to S0.2's CI as a job that runs against the preview deployment when one exists (skip-with-warning on PRs without a preview).

**Tests:** unit — CSP builder produces a nonce and both profiles; integration — `/api/health` and a checkout route return every header; e2e — app still renders with CSP on (a violation would break hydration and fail the page-error assertion); `scripts/check-headers.mjs` green on staging.
**Verify:** `pnpm test && pnpm test:integration --grep headers && node scripts/check-headers.mjs --base "$STAGING_URL"`.
**Done when:** all six routes pass the header checker, the CSP has no `unsafe-eval`, and a deliberate `onClick` inline handler added to a test page is reported as a violation (proving the policy is enforced, not just present).
**Commit:** `feat(FR-SEC-002): security headers, nonce CSP and edge controls`

### S0.13 — Operations baseline: backups, restore drill, runbooks, incident response

**Goal:** the boring guarantees that decide whether an outage is an incident or a footnote.
**Depends on:** S0.3, S0.9. **Master spec:** §36.1–§36.4, §5.7, `FR-NFR-003`, `FR-NFR-004`, `FR-NFR-007`, `FR-SEC-019`. **Effort:** 1 agent-day.
**Features:** `FR-NFR-003`, `FR-NFR-004`, `FR-NFR-007`, `FR-SEC-019`.

**Build**

1. Supabase backups: confirm PITR is on for the project (plan-dependent, see §2.5); record RPO/RTO in `docs/OPERATIONS.md`. If the plan lacks PITR, add a nightly `pg_dump` to Supabase Storage via a scheduled worker job and say so explicitly.
2. `scripts/restore-drill.md` + `scripts/restore-drill.sh` — restore the latest backup into a scratch project, run `pnpm test:integration` against it, record the duration in `docs/PROGRESS.md`. Run quarterly; the first run happens before the Phase 1 gate.
3. `docs/runbooks/` — one file per scenario, each ≤ 1 page: `db-down.md`, `worker-stuck.md`, `processor-outage.md`, `webhook-backlog.md`, `payout-failure.md`, `security-incident.md`, `data-breach.md`, `rollback.md`. Every runbook: symptom → check → decision → action → comms.
4. Incident response (FR-SEC-019): severity ladder (P0–P3), who is paged, the 72-hour breach-notification timer, the evidence-preservation steps (snapshot logs **before** remediation), and the post-incident template.
5. Observability minimum (FR-NFR-003): structured logs (done in §15.3), `/api/health` (DB, worker heartbeat, queue depth, last audit checkpoint age), and 8 alerts — error rate, p95 latency, DB connections, queue backlog, dead letters, failed payouts, webhook delivery failures, audit-checkpoint staleness.
6. `docs/ONCALL.md` with the alert → runbook table.

**Tests:** `/api/health` degrades correctly (returns 503 with a machine-readable reason when the DB is unreachable — simulated); the alert rules file parses; every alert in `ONCALL.md` links to an existing runbook file (script check).
**Verify:** `pnpm test:integration --grep health && node scripts/check-runbooks.mjs`.
**Done when:** restore drill completed once with a recorded duration; all 8 runbooks exist and are linked from `ONCALL.md`.
**Commit:** `feat(FR-NFR-004): backups, restore drill, runbooks and incident response`

### Phase 0 gate (must all be true before S1.1)

- [ ] `pnpm verify` green from a clean clone.
- [ ] `supabase db reset` applies all migrations; `pnpm db:types` produces no diff.
- [ ] Sign-up → sign-in → MFA → sign-out works; revoked session is rejected on the next request.
- [ ] RLS coverage + isolation suites green; commenting out one policy makes them red.
- [ ] Audit chain verifies; tampering is detected.
- [ ] Worker processes an outbox event exactly once; dead letters visible.
- [ ] `/design` passes axe at 320/768/1440.
- [ ] Brand name/logo/address change in DB reflects on site and in an email.
- [ ] All six route profiles return the full security header set; CSP has no `unsafe-eval`; a CSP violation is actually blocked.
- [ ] One restore drill done end-to-end with the duration recorded; every alert has a runbook.

---

## 5. Phase 1 — Money In (S1.1–S1.21)

**Phase 1 outcome:** a merchant onboards (manual review), sends an American-standard invoice, a guest buyer pays by card on a hosted page, the money lands in an immutable double-entry ledger, the merchant can refund, and a scheduled payout reaches their verified bank account with a receipt — all audited, tenant-isolated, and observable.

**Build order:** steps are ordered by *dependency*, not strictly by number. S1.8, S1.10 and S1.17 are safe to pull forward; nothing may be pulled forward across a phase boundary.

**Dependency graph** (build left to right; `⇢` can run in parallel):

```text
Phase 0 ─┬─ S1.1 merchants ─┬─ S1.2 onboarding ─→ S1.3 admin review
         │                  ├─ S1.4 banking
         │                  └─ S1.5 ledger core ─→ S1.6 fees/plans ─→ S1.7 invoices
         │                                                            ├─ S1.8 invoice PDF
         │                                                            └─ S1.9 checkout page
         ├─ S1.10 processor adapter ⇢ (parallel with S1.7)
         └─ S1.17 CMS pages ⇢ (parallel after S0.11)

S1.7 + S1.9 + S1.10 + S1.5 + S1.6 ─→ S1.11 payment completion
S1.11 ─→ S1.12 webhooks ─→ S1.13 refunds ─→ S1.14 payouts
S1.11 + S1.13 + S1.14 + S1.7 ─→ S1.15 merchant portal
S1.3 + S1.14 + S1.15 ─→ S1.16 admin console
S1.10 ─→ S1.19 public API
S1.14 ─→ S1.20 reconciliation + statements
everything ─→ S1.21 hardening + Phase 1 gate
```

### S1.1 — Merchants, profiles, settings, limits, provisioning

**Goal:** a merchant record exists, is tenant-scoped, and can be created only through a controlled flow.
**Depends on:** Phase 0. **Master spec:** §6.5, `FR-KYB-002`, `FR-MER-001`, `FR-KYB-009`. **Effort:** 2 agent-days.
**Features:** `FR-MER-001`.

**Build**

1. Migration `0008_merchants.sql` — `merchants`, `merchant_profiles`, `merchant_settings`, `merchant_limits`, `merchant_volume_counters`, `merchant_notes`, `merchant_countries` (master spec §6.5, §6.12). Include the RLS exposure block and the `protect_merchant_columns` trigger (§6.14).
2. `private.create_merchant(p_user uuid, p_input jsonb)` — creates merchant (`status='draft'`, `livemode=false`), profile, settings, limits, a `merchant_members` row with role `owner`, and `user_roles` scope row; idempotent per user+legal name; writes audit + outbox; returns `merchant_id`.
3. Ledger provisioning is **deferred to S1.5** (the ledger tables do not exist yet). S1.5 adds `private.provision_merchant_accounts` and backfills every existing merchant; nothing in S1.1 may reference ledger tables.
4. `private.update_merchant_profile` + `private.set_merchant_controls` (charges/payouts toggles, staff-only, audited).
5. Zod schemas in `features/merchants/schema.ts`: legal name, DBA, business type enum, country (ISO-3166 from `merchant_countries` where `enabled`), registration number, MCC (from a seeded list), website URL, business description (10–500 chars).
6. Descriptor builder `features/merchants/descriptor.ts` — prefix from `platform_settings` + sanitized DBA, uppercase, `≤ 22` chars, allowed `[A-Z0-9 *.-]`, preview + validation messages.
7. `features/merchants/queries.ts` — `getMerchant(ctx)`, `getMerchantSummary(ctx)` (single query), no `select *`.
8. Seed `supabase/seed/003_countries_mcc.sql` — the §0.7 country list + a conservative MCC list (only MCCs the processor supports).

**Tests:** merchant creation is idempotent; a non-owner cannot create a second merchant; descriptor rejects 23 chars, URLs, and all-symbol strings; `protect_merchant_columns` blocks a merchant admin from flipping `charges_enabled`; RLS rows added to the coverage test.
**Verify:** `pnpm db:reset && pnpm test:integration -- merchants && pnpm test:rls`
**Done when:** a draft merchant exists end-to-end with owner membership and cannot be seen by another tenant.
**Commit:** `feat(S1.1): merchant core, controls, descriptor, limits`

---

### S1.2 — Onboarding wizard and secure document upload

**Goal:** a merchant can submit KYB with documents safely, resumably, and with real file validation.
**Depends on:** S1.1. **Master spec:** §3.6, §21.4, §24.2, `FR-KYB-001..004`, `FR-SEC-007`, `CR-05`. **Effort:** 3 agent-days.
**Features:** `FR-KYB-001..004`, `FR-TEN-003`, `FR-SEC-007`, `FR-AUD-004`.

**Build**

1. Migration `0009_kyb.sql` — `kyb_applications`, `kyb_documents`, `beneficial_owners`, `kyc_verifications`, `screening_results`, `merchant_compliance_flags` (master spec §6.5) + RLS.
2. Storage buckets (via `supabase/config.toml` + a migration of bucket policies): `kyc-docs` (private, 10 MB), `dispute-evidence` (private, 10 MB), `branding` (public read, 2 MB), `cms-media` (public read, 2 MB), `reports` (private), `pdfs` (private). Policies restrict object paths to `merchant/{auth_merchant_id}/…`.
3. `src/lib/storage/upload.ts`:
   - `createUploadUrl({ merchantId, bucket, path, contentType, maxBytes })` → Supabase `createSignedUploadUrl` with 5-minute TTL.
   - `finalizeUpload({ path, sha256, declaredMime })` → server downloads the first 4 KB, checks **magic bytes** (`%PDF`, `\xFF\xD8\xFF`, `\x89PNG`), verifies size, computes SHA-256, stores metadata, optionally runs a virus scan adapter (`VIRUS_SCAN=noop|clamav-http`).
   - Reject: password-protected PDFs, polyglots, > 50 pages, SVG for KYC, anything not PDF/JPG/PNG.
4. Wizard `(merchant)/app/onboarding/*` — 5 steps (business → owners/UBOs → documents → bank (S1.4) → tax form (S1.3) → review), progress bar, save-and-resume, per-step validation, clear rejection reasons, EN/BN strings.
5. UBO editor: name, DOB, nationality, residence, ownership %, flags (controller/director/signer), ID upload; validation: total ownership ≤ 100, at least one controller, ≥ 1 UBO ≥ 25% or an explicit "no 25% owner" attestation.
6. `private.submit_kyb` — validates completeness, sets `status='submitted'`, writes audit + outbox (`kyb.submitted`), notifies staff (server-only command, master spec §6.14).
7. Document viewer (admin) with dynamic watermark (viewer email + IP + timestamp) rendered server-side; **audit on open**.

**Tests:** upload URL rejects wrong content type and oversized signatures; magic-byte mismatch is rejected even with a `.pdf` name; a 12 MB file is refused; resubmission creates a new `kyb_applications.version`; cross-tenant signed URLs are denied; wizard resume restores state.
**Verify:** `pnpm test:integration -- uploads` + Playwright onboarding happy path (sandbox PDF fixture).
**Done when:** a complete application can be submitted with real files and is visible to staff only.
**Commit:** `feat(FR-KYB-001..004): onboarding wizard, ubo capture, secure uploads`

---

### S1.3 — Admin KYB review, lifecycle controls, tax forms

**Goal:** staff can approve, reject, request documents, suspend, reinstate, and capture W-9/W-8 — all with audit and four-eyes where required.
**Depends on:** S1.2. **Master spec:** §3.6–§3.7, §20.4–§20.5, `FR-KYB-005..010,013`, `FR-TAX-001`. **Effort:** 3 agent-days.
**Features:** `FR-KYB-005`, `FR-KYB-006`, `FR-KYB-008..010`, `FR-KYB-013`, `FR-TAX-001`, `FR-SEC-008`, `FR-UX-008`.

**Build**

1. Migration `0010_tax_documents.sql` — `tax_documents`, `tax_filings`, `merchant_tax_registrations`; add `tax_id_ciphertext` encryption helper use (master spec §21.2).
2. `src/lib/security/crypto.ts` — AES-256-GCM envelope encryption: `encryptField(plaintext, aad)` → `v1:base64(iv):base64(ct):base64(tag)`, `decryptField(...)`, key version from env/KMS; AAD = `${table}:${column}:${recordId}`.
3. Screening adapter `src/lib/compliance/screening.ts` — `screenSubject({ type, name, dob, country })` with `SCREENING_PROVIDER=manual|sumsub|persona`; manual = staff uploads/records result; always writes `screening_results`.
4. Admin queues `/admin/compliance`: applications (SLA, assignee, filters), documents, UBOs, screening, flags, tax docs.
5. Decision command `private.kyb_decision(application_id, decision, reason_code, notes)` — enforces `compliance.review`, forbids self-review, requires step-up, writes audit, transitions merchant status, emits events.
6. Lifecycle commands: `private.suspend_merchant`, `private.reinstate_merchant` (compliance + risk), `private.terminate_merchant`; each requires a reason code and step-up; suspend flips `charges_enabled=false` and `payouts_enabled=false`.
7. Document request flow `private.request_documents(merchant_id, types[], due_date, message)` → notification + merchant action item.
8. Tax form capture: in-app form for W-9 (legal name, entity type, address, TIN with confirm-TIN, certification checkboxes), W-8BEN, W-8BEN-E (simplified Phase-1 field set — full treaty logic is Phase 3). Store encrypted payload, masked TIN (`***-**-1234`), `form_version`, `signed_at`, `signed_ip`, `signature_hash`. Validate TIN format (SSN/EIN regex) but **never** call the IRS in Phase 1.
9. "More info needed" loop: merchant sees requested items; resubmission bumps `kyb_applications.version`.

**Tests:** approve/reject transitions; self-review blocked; step-up required; TIN is encrypted at rest (DB shows ciphertext) and masked in every API response; suspend blocks new payments (verified again in S1.11); audit rows for each action; four-eyes on reinstatement.
**Verify:** `pnpm test:integration -- kyb && pnpm test:e2e --grep "kyb review"`
**Done when:** a merchant can go draft → approved and be blocked/suspended/reinstated with a complete audit trail.
**Commit:** `feat(FR-KYB-005..010,FR-TAX-001): kyb review, lifecycle, tax forms`

---

### S1.4 — Bank accounts, verification, and change protection

**Goal:** payouts have a safe destination that cannot be silently hijacked.
**Depends on:** S1.1. **Master spec:** §10.6, §21.2, `FR-BNK-001..004`, `FR-PYT-001`, `CR-19`. **Effort:** 2.5 agent-days.
**Features:** `FR-BNK-001..004`.

**Build**

1. Migration `0011_banking.sql` — `bank_accounts`, `bank_verification_attempts`, `bank_account_changes` + RLS; encrypted `account_number_ciphertext`/`routing_value_ciphertext`; `account_number_last4` only for display.
2. `features/banking/validate.ts` — IBAN mod-97, ABA checksum, SWIFT/BIC format, local rail hints per country; reject if account holder ≠ merchant legal name (configurable name-match), require currency USD in Phase 1.
3. Verification: `micro_deposit` (two random amounts < $1, 3 attempts, 72 h expiry) with a `VerificationProvider` interface; `instant`/`partner` stubs for Phase 2. Local/dev uses a fixed test amount (`0.32`/`0.45`) behind `BANK_VERIFY=stub` — never in production.
4. Change flow: request → step-up → `bank_account_changes` (`cooling_ends_at = now() + 24h`) → notify **both** old and new contacts → second approver (different merchant admin **or** platform finance) → apply after cooling → block payouts to the new account until one successful payout (cap: `min(20% monthly volume, $10,000)`).
5. UI `/app/settings/bank`: masked accounts, "verify" flow, default badge, change-request status, warnings about fraud.
6. Payouts must read only `status='verified' and is_default` accounts (enforced again in S1.14).

**Tests:** invalid IBAN/ABA rejected; name mismatch blocked; change requires step-up + second approver + 24 h; payouts blocked during cooling; ciphertext present in DB and plaintext absent from logs; audit on every transition.
**Verify:** `pnpm test:integration -- banking`
**Done when:** no code path can add or change a payout destination without the full workflow.
**Commit:** `feat(FR-BNK-001..004): bank accounts, verification, protected changes`

---

### S1.5 — Ledger core: accounts, posting, immutability, hash chain

**Goal:** the financial heart. Every money movement from here on is a balanced, immutable, hash-chained transaction.
**Depends on:** S1.1. **Master spec:** §7, §8, §6.6, `N-03`, `N-05`, `FR-LDG-001..006`. **Effort:** 4 agent-days.
**Features:** `FR-LDG-001..006`, `FR-LDG-009`.

**Build**

1. Migration `0012_ledger.sql` — `ledger_accounts`, `ledger_transactions`, `ledger_entries`, `ledger_periods`, `ledger_adjustments`, `merchant_balances` view (`security_invoker`), all constraints and indexes from master spec §6.6.
2. Triggers: `ledger_no_mutation` (reject UPDATE/DELETE), `ledger_balance_guard` (deferred constraint trigger: debits = credits), `ledger_chain_guard` (sequence/hash computed by the function, verify on insert), `protect_closed_periods`.
3. `private.ledger_post(...)` — port **verbatim** from master spec §8.7 (string amounts, advisory lock, balance check, foreign-account check, pre-insert hash). Owned by `postgres` so `security definer` bypasses FORCE RLS.
4. `private.provision_merchant_accounts(merchant_id)` — six accounts; called on approval and idempotently on login for legacy drafts.
5. Ledger builders `src/lib/ledger/builders.ts` — `capture()`, `platformFee()`, `makeAvailable()`, `settlement()`, `refund()`, `disputeOpen/Won/Lost()`, `payoutRequested/Paid/Failed()`, `reserveHold/Release()`, `adjustment()` returning canonical, **sorted** entry arrays with string amounts.
6. `src/lib/ledger/post.ts` — `postLedger(tx, builder)` calling the RPC; throws `LedgerError` on `UNBALANCED_TRANSACTION`/`FOREIGN_ACCOUNT`; logs a P1 alert.
7. `src/lib/money/` — `MicroUsd`, `parseMoney` (rejects > 4 dp, exponent, NaN), `formatMoney`, `toDbNumeric`, `fromDbNumeric`, `mulRate`, `splitProportionally` (largest remainder), `assertBalanced`.
8. `src/app/api/internal/ledger-verify/route.ts` — recompute chain for the last 90 days daily; full chain monthly (chunked); on mismatch: alert + set `platform_feature_flags.payouts_enabled=false` (global kill switch) and a P1 audit event.
9. Merchant balance queries `features/ledger/queries.ts` — one query returning all four buckets + holds + reserves.

**Tests (the most important suite in the repo):**
- Property tests (`fast-check`): every builder balances to zero; allocations preserve sums; `parseMoney(format(x)) === x`.
- `ledger_no_mutation`: UPDATE/DELETE raise.
- Concurrent postings on one merchant never duplicate `sequence` and the chain verifies (run 50 parallel posts).
- A deliberately unbalanced builder is rejected by both TS and SQL.
- Worked examples from master spec §8.3–§8.5 reproduced exactly (assert every account balance).
- 4-dp boundary values (`0.0001`, `99999999.9999`), and rejection of `0.00001`.

**Verify:** `pnpm test -- money ledger` + `pnpm test:integration -- ledger` + `pnpm test:rls`
**Done when:** a scripted sequence (capture → fee → availability → payout → refund → dispute) leaves every account exactly as the master spec's worked examples predict, and the chain verifies.
**Commit:** `feat(FR-LDG-001..006): double-entry ledger, posting function, hash chain`

---

### S1.6 — Plans, fee schedules and the fee engine

**Goal:** pricing is data, snapshotted per charge, and never retroactive.
**Depends on:** S1.5. **Master spec:** §9, §7.4, `FR-FEE-001..004`, `FR-LDG-009`. **Effort:** 2.5 agent-days.
**Features:** `FR-FEE-003`, `FR-FEE-004`.

**Build**

1. Migration `0013_billing.sql` — `plans`, `fee_schedules`, `merchant_subscriptions`, `subscription_invoices`, `fee_charges` (note the partial unique index for `processing` fees).
2. Seed `supabase/seed/004_plans.sql` — Free/Pro/Business/Enterprise exactly as master spec §9.4 (percent, fixed, payout delay, reserve, entitlements in `features` JSON).
3. `features/fees/engine.ts` — pure `computeFees({ amount, schedule, plan, currency })` → `{ processingFee, netToMerchant, snapshot }` with half-up rounding at the cent and 4-dp storage; `resolveSchedule(merchant, plan, at)` implementing the resolution order in master spec §9.1.
4. `rateFees()` server function — writes `fee_charges` with `fee_snapshot` (schedule hash) inside the payment transaction.
5. Entitlement checks `features/billing/limits.ts` — users, API keys, invoices/month; typed `LimitExceededError` with an upgrade link; never deletes data.
6. Subscription billing: monthly invoice generation job + payment via the same payment engine (Phase 2 full dunning; Phase 1 generates + charges, retries 3× then `past_due`).

**Tests:** fee math table (incl. `0.01`, `29.99`, `1000.00`, rounding boundaries) against hand-computed values; snapshot immutability (change plan → old charge unchanged); plan limits enforced server-side; fee accrual posts exactly one ledger transaction per capture.
**Verify:** `pnpm test -- fees` + `pnpm test:integration -- billing`
**Done when:** changing a merchant's schedule affects only future captures.
**Commit:** `feat(FR-FEE-001..004): plans, fee schedules, snapshot fee engine`

---

### S1.7 — Customers, invoices, numbering, tax lines

**Goal:** merchants can create, finalize, send, and track invoices with correct totals — and the paid-lock rules are in place from the start.
**Depends on:** S1.5, S1.6. **Master spec:** §15.1, §15.5, §14.1, §6.7, `FR-INV-001..008,010,011,015`, `FR-CHK-008`. **Effort:** 4 agent-days.
**Features:** `FR-INV-001..005`, `FR-INV-007`, `FR-INV-008`, `FR-INV-011`, `FR-INV-015`, `FR-TAX-004`.

**Build**

1. Migration `0014_commerce.sql` — `customers`, `customer_consents`, `products`, `tax_rates`, `tax_exemptions`, `invoices`, `invoice_line_items`, `invoice_tax_lines`, `invoice_events`, `invoice_attachments`, `invoice_counters`, `credit_memos`, `credit_memo_lines`, `payment_links` (master spec §6.7).
2. Totals trigger `invoice_totals_guard` — recompute `subtotal/tax_total/total/balance_due` from lines with 4-dp math and largest-remainder tax allocation; enforce `balance_due = total − amount_paid − amount_credited`.
3. Numbering RPC — `select ... for update` on `invoice_counters(merchant_id, year)`, format `INV-2026-000123`, gapless per merchant/year.
4. State machine trigger `invoice_state_guard` — legal transitions only (master spec §15.1); once `paid`, amounts are frozen; `void` only when unpaid.
5. Draft/finalize/send/void RPCs + `invoice_events` rows; finalize writes `customer_snapshot` + `render_snapshot` (immutable) and allocates the number.
6. **Double-payment lock now, not later:** partial unique index `one_live_payment_per_invoice_idx` (declared with the payments table in S1.9/S1.11) plus the `invoice_payment_lock` trigger designed here.
7. Invoice editor UI `/app/invoices/new` and `/app/invoices/[id]` — line items, per-line tax, discounts, shipping, memo/terms, autosave draft, live totals from the same TS fee/tax math as the server, preview.
8. Reminder job + `overdue` transition (nightly), per-invoice throttle.

**Tests:** totals trigger survives malformed direct inserts; numbering has no gaps under 50 concurrent finalizes; editing after `paid` is rejected; illegal transitions rejected; tax allocation sums exactly; rounding table for 3-line 33.333% splits.
**Verify:** `pnpm test:integration -- invoices` + Playwright create→finalize→send.
**Done when:** the totals in the UI, the DB, and the PDF (S1.8) always agree.
**Commit:** `feat(FR-INV-001..011): invoice core, numbering, tax lines, state machine`

---

### S1.8 — Invoice PDF with security design

**Goal:** a professional US-format invoice PDF with guilloche, watermark, QR verification and a document hash — generated without a headless browser.
**Depends on:** S1.7. **Master spec:** §15.5, §31.8, `FR-INV-006`, `FR-UX-007`, `CR-02`. **Effort:** 3 agent-days.
**Features:** `FR-INV-006`, `FR-UX-007`.

**Build**

1. `src/lib/pdf/theme.ts` — fonts (embed Inter regular/bold + Noto Sans Bengali subset), margins (1 in), A4 + Letter support, color palette.
2. `src/lib/pdf/guilloche.ts` — deterministic vector pattern from `sha256(public_id)`; `drawGuilloche(page, { seed, opacity })`; microtext line (`KDPAY • <id> • <hash8>`) at 3.5 pt along the border; diagonal watermark at 8–12% opacity.
3. `src/lib/pdf/invoice.tsx`-equivalent builder using `pdf-lib` primitives (no React-PDF, no Chromium): seller block, `INVOICE` + number, dates, bill-to, table with pagination (repeat header), totals, `balance_due`, payment link + QR, terms, footer with `Document ID / SHA-256`.
4. QR encodes `https://<app>/verify/<public_id>?h=<hash prefix>`; a public `/verify/[id]` page shows issuer, date, amount, status (no PII beyond what the holder already has).
5. Render on **finalize** (job, not request path) → store in `pdfs` bucket → `invoices.pdf_path` + `pdf_sha256`; regeneration must reproduce identical **content** (compare normalized text + hash of the render payload, not PDF bytes).
6. `PAID` / `VOID` stamps as vector overlays; never obscure amounts.
7. Localization: labels from `messages/{en,bn}.json`; numbers/dates formatted with `Intl`; currency `USD`.

**Tests:** snapshot test of extracted text (pdf-lib parse) for a fixture invoice; watermark present on every page; QR decodes to the right URL; tampered render payload yields a different hash; PDF opens in macOS Preview/Adobe/Chrome (manual once, documented); EN and BN variants.
**Verify:** `pnpm test -- pdf` + open generated file in a viewer.
**Done when:** an invoice PDF looks like a bank-grade document and its hash is verifiable on `/verify`.
**Commit:** `feat(FR-INV-006,FR-UX-007): invoice pdf with guilloche, watermark, qr, hash`

---

### S1.9 — Payment links and the hosted checkout page

**Goal:** a guest buyer can open a link, see a trustworthy page, and reach the card step — with no card fields on our domain.
**Depends on:** S1.7, S1.10 (interface only). *If you build strictly in numeric order, create `src/lib/processors/types.ts` and `normalize.ts` first — they belong to S1.10 and are safe to land early.* **Master spec:** §15.2–§15.4, §26, §17, `FR-CHK-001..007,009,010`. **Effort:** 4 agent-days.
**Features:** `FR-INV-010`, `FR-CHK-001`, `FR-CHK-003..010`, `FR-UX-009`.

**Build**

1. `payment_links` creation/revocation (`lnk_` public id, 256-bit token stored as SHA-256, expiry, max uses); constant-time lookup.
2. `/pay/[token]` — server component; loads invoice snapshot + merchant branding + platform settings in **one** query; 404 on expired/revoked; `noindex`; `no-store`.
3. Layout: merchant logo/name, invoice number, amount due, descriptor preview, collapsible line items, due date, support contact, terms link, PCI/TLS/3DS badge bar (master spec §26), EN/BN toggle, mobile-first at 320 px, WCAG 2.2 AA.
4. Buyer step: email + name + billing country (+ optional "save my details" consent → `customer_consents`); Turnstile; server-side Zod; rate limits per IP/token.
5. `POST /api/checkout/session` → risk stitch (S1.11 pipeline, Phase-1 stub = velocity + blocklist) → creates `checkout_sessions` row → returns the processor client config (publishable key + client secret **only**; never a secret key).
6. Card step mounts the processor iframe (S1.10 adapter contract); our code never reads those fields; CSP allows only the processor + Turnstile origins.
7. Success/failed/expired pages `/pay/[token]/success|failed|expired` **and** `/pay/[token]/3ds-return` (redirect-based 3DS challenge; validates `state` + session before resuming); receipt link; no confetti, no dark patterns.
8. **Test-mode behavior:** with `PROCESSOR=sandbox`, the card step shows **buttons** ("Approve", "Decline: insufficient funds", "Require 3DS", "Decline: stolen card") — no free-form card input anywhere, preserving `N-01`.

**Tests:** expired/revoked token → 404; token cannot be reused across merchants; amount is server-derived (changing a hidden field changes nothing); Turnstile failure blocks; rate limit returns 429 with `Retry-After`; axe + Lighthouse (LCP budget ≤ 2.0 s on the local throttle); no third-party requests except processor/Turnstile.
**Verify:** `pnpm test:e2e --grep "checkout page"` + Lighthouse CI report.
**Done when:** the page passes a "would I pay here?" review on a phone and contains zero card inputs.
**Commit:** `feat(FR-CHK-001..010): hosted checkout, links, guest capture`

---

### S1.10 — Processor adapter interface + sandbox adapter + Stripe/Airwallex skeletons

**Goal:** business logic never imports a vendor SDK; the whole platform is testable without live credentials.
**Depends on:** S0.5. **Master spec:** §4, §16, `FR-PAY-001,008`, `FR-PAY-013` (interface only). **Effort:** 3 agent-days.
**Features:** `FR-PAY-009`, `FR-CHK-002`.

**Build**

1. `src/lib/processors/types.ts` — `PaymentProcessor` interface verbatim from master spec §4.1 + `ProcessorCapabilities`, canonical status enums, `ProcessorError { code, declineCode, retryable, raw }`.
2. `src/lib/processors/normalize.ts` — maps every vendor status/decline code → canonical `declineClass` (master spec §16.6). **Unknown → `requires_review`**, never success. Table-driven with a test that fails on unmapped codes.
3. `src/lib/processors/sandbox.ts` — deterministic `SandboxProcessor`:
   - `createPaymentIntent` → id (`sbx_pi_<nanoid>`), status `requires_confirmation`;
   - `confirm` with a chosen outcome → `succeeded` | `requires_action` (3DS) | `declined` with a specific code;
   - `capture`, `void`, `refund`, `payout` (success/fail/return switches), `listSettlements` (deterministic fixture generator), `verifyWebhook` (HMAC with `SANDBOX_WEBHOOK_SECRET`).
4. `src/lib/processors/stripe.ts` and `airwallex.ts` — real signatures, config from env, implemented only for `createPaymentIntent` + `verifyWebhook` + `refund` in Phase 1; the rest throw `NotImplemented` with a linked step. **Contract tests run against the same suite** as sandbox.
5. `src/lib/processors/registry.ts` — resolves by `merchants.processor_id`; validates capabilities before an action; `assertCapability('manualCapture')`.
6. `src/app/api/webhooks/processor/[processor]/route.ts` — raw body (`await req.text()`), verify, store, 200, enqueue (full logic in S1.12).
7. `processor_accounts` + `processor_routing_rules` seed.

**Tests:** shared contract suite × {sandbox, stripe (mocked HTTP fixtures), airwallex (mocked)}; unknown status → `requires_review`; capability gate blocks manual capture on a processor without it; webhook signature mismatch rejected; replay of the same event id is a no-op.
**Verify:** `pnpm test:contract`
**Done when:** the sandbox adapter can run the entire payment lifecycle with zero network access to third parties.
**Commit:** `feat(FR-PAY-001,FR-PAY-008): processor interface, sandbox, adapters, webhook intake`

---

### S1.11 — Payment completion: verification, locking, ledger, receipt

**Goal:** money is captured exactly once, verified server-side, posted to the ledger, and receipted.
**Depends on:** S1.5, S1.6, S1.7, S1.9, S1.10. **Master spec:** §15.2, §15.6, §16.5–§16.7, §18.1, `FR-CHK-008`, `FR-PAY-002..007`, `FR-INV-007`, `FR-LDG-002..004`. **Effort:** 5 agent-days.
**Features:** `FR-PAY-001..008`.

**Build**

1. Migration `0015_payments.sql` — `payments`, `payment_methods`, `payment_attempts`, `card_blocklist`, `fraud_rules`, `risk_decisions`, `manual_review_queue`, `velocity_counters`, `payment_retries`, `idempotency_keys`, `processor_webhook_events` (master spec §6.8, §6.4).
2. `private.commit_payment(p_checkout_session uuid, p_processor_ref text)` — **the single authoritative completion path**:
   - `select ... from invoices where id = $1 for update`;
   - re-fetch the payment from the processor API (never trust the browser or webhook body);
   - insert `payments` (unique `(merchant_id, idempotency_key)` and the partial unique index);
   - `ledger_post` capture + platform fee;
   - `rateFees()` snapshot;
   - flip invoice to `paid` (`paid_at`, `balance_due = 0`) and reject any later payment with `INVOICE_ALREADY_PAID`;
   - write audit + outbox (`payment.captured`, `invoice.paid`, `email.receipt`).
3. `withIdempotency(merchantId, key, scope, fn)` — stores request hash + response; same key + different payload → `422 idempotency_key_reuse`; replay returns the stored response with `Idempotent-Replay: true`.
4. Risk pipeline `features/risk/decide.ts` — velocity, blocklist, geo/IP stub, amount anomaly, merchant age → score + band + action (+ `risk_decisions`). Medium → `capture_method='manual'` + review queue (5-day auth hold, auto-void 12 h before expiry).
5. Decline handling: classify, store attempt, apply master spec §16.6 (block hard/fraud; schedule ≤5/24h for soft), safe buyer-facing messages.
6. Receipt: outbox → worker → email with PDF receipt + signed receipt link (30 days).
7. UI: `/app/transactions` list + detail (attempts, risk, processor refs, ledger links); admin payment detail.

**Tests (must all exist):**
- Two concurrent buyers on one invoice → exactly one success, one `INVOICE_ALREADY_PAID`, one ledger transaction. Run the test 20×.
- Duplicate webhook + duplicate client confirmation → single payment.
- Processor says declined but body says success → we follow the **API**, not the body.
- Amount tampering in the request is ignored.
- 3DS required → no capture until authenticated.
- Manual capture flow: approve → captured; expire → voided.
- Retry policy: 6th insufficient-funds attempt in 24 h is refused.
- Receipt email contains no PAN and a working signed link.

**Verify:** `pnpm test:integration -- payments && pnpm test:e2e --grep "pay invoice"`
**Done when:** the concurrency test is green 20/20 and the ledger balances after every scenario.
**Commit:** `feat(FR-CHK-008,FR-PAY-002..007): payment completion, locking, ledger, receipt`

---

### S1.12 — Inbound and outbound webhooks

**Goal:** merchant systems get reliable, signed, replayable events; processor events are trustworthy.
**Depends on:** S1.10, S1.11. **Master spec:** §18.2–§18.3, §21.1, `FR-API-006`, `N-07`. **Effort:** 3 agent-days.
**Features:** `FR-API-006`, `FR-SEC-006`.

**Build**

1. Migration `0016_webhooks.sql` — `webhook_endpoints`, `webhook_events`, `webhook_deliveries`.
2. `src/lib/webhooks/sign.ts` — `KDPAY-Signature: t=<unix>,v1=<hex hmac_sha256(secret, t + "." + raw_body)>`; 5-min tolerance; per-endpoint secret encrypted at rest; rotation with 24 h dual-signing.
3. `src/lib/webhooks/ssrf.ts` — HTTPS only; resolve DNS and reject private/link-local/loopback/metadata ranges **after** resolution (re-check on every delivery), no redirects, 10 s timeout, max 64 KB response read.
4. Delivery worker — retries 1 m, 5 m, 30 m, 2 h, 6 h, 24 h (max 8), jitter, `2xx` success, `410` disables endpoint with notice; per-attempt record; manual replay (audited).
5. Merchant UI `/app/developers/webhooks` — create/edit/test/rotate/disable, delivery log with response excerpt (redacted), replay button.
6. Event catalog from master spec Appendix C; `emit(tx, type, object)` writes `webhook_events` + outbox in the same transaction as the domain change.
7. Inbound processor webhooks: verify → unique `(processor, event_id)` → 200 in < 2 s → worker re-fetches and applies.

**Tests:** signature verify/reject (stale, wrong secret, wrong body); **dedupe**; retry schedule unit test with a fake clock; SSRF suite (localhost, `169.254.169.254`, `[::1]`, redirect to private, DNS rebinding via mocked resolver); 410 disables; replay is idempotent for the consumer.
**Verify:** `pnpm test:integration -- webhooks` + `pnpm test:contract -- webhooks`
**Done when:** killing the worker mid-flight never loses or duplicates a logical event.
**Commit:** `feat(FR-API-006): signed webhooks, retries, ssrf guard, replay`

---

### S1.13 — Refunds, credit memos, negative-balance protection

**Goal:** refunds are bounded, approved, ledgered, documented, and cannot silently create unrecoverable debt.
**Depends on:** S1.11. **Master spec:** §13, §8.4, `FR-RFD-001..008`, `FR-INV-009`, `CR-20`. **Effort:** 3 agent-days.
**Features:** `FR-RFD-001..008`, `FR-INV-009`.

**Build**

1. Migration `0017_refunds.sql` — `refunds` (+ `refund_limit_guard` trigger), `credit_memos`, `credit_memo_lines`; add `payments.amount_refunded` check.
2. `private.request_refund(payment_id, amount, reason, detail)` — bounds (`≤ captured − refunded`), window (180 d), dispute block, negative-balance preview (`balance_after`), threshold → `approval_requests`. Wrapped by `requestRefund(ctx, input)` in `src/features/refunds/service.ts` (§15.13), which is what Server Actions call.
3. `private.approve_refund(refund_id)` — four-eyes, step-up, then submit to processor with idempotency key `refund:{id}`; wrapper `approveRefund(ctx, id)`.
4. Worker: on `succeeded` → ledger reversal (master spec §8.4), fee policy (fixed retained, % returned), credit memo PDF (watermarked `CREDIT MEMO`), buyer email, merchant webhook; on `failed` → safe status + alert.
5. UI: refund dialog with refundable amount, reason, fee treatment and resulting balance; refunds list/detail; credit memo download.
6. Negative balance: when a refund would overdraw, show the projected negative balance and require an explicit "accept receivable" acknowledgement (audited) or reduce the amount.

**Tests:** refund > captured rejected (property test against random sequences); multiple partials summing to exactly captured allowed, +$0.01 rejected; refund during dispute rejected; refund after window rejected; threshold approval required; ledger reversal matches master spec §8.4 exactly; credit memo numbering + PDF hash.
**Verify:** `pnpm test:integration -- refunds`
**Done when:** no sequence of refunds can make the ledger unbalanced or exceed captured.
**Commit:** `feat(FR-RFD-001..008): refunds, credit memos, balance protection`

---

### S1.14 — Payouts: eligibility, scheduling, approvals, receipts

**Goal:** money reaches the merchant's verified bank account exactly once, with a receipt and a complete ledger trail.
**Depends on:** S1.5, S1.11, S1.13. **Master spec:** §10, §8.2, `FR-PYT-002..006,009,010,012`. **Effort:** 4 agent-days.
**Features:** `FR-PYT-001..007`, `FR-PYT-009`, `FR-PYT-010`, `FR-PYT-012`.

**Build**

1. Migration `0018_payouts.sql` — `payouts`, `payout_items`, `payout_holds`, `reserves`, `reserve_movements` + `payout_state_guard`, `payout_eligibility` view.
2. `features/payouts/eligibility.ts` — the ten checks in §10.1, evaluated inside one transaction with `for update` on the merchant.
3. `features/payouts/schedule.ts` — daily/weekly/manual, merchant timezone, cut-off 17:00, holiday calendar (`private.holidays`), minimum, caps, split when above cap.
4. Scheduler job (every hour + at cut-off) → `scheduled` payouts + `ledger_post(payout_requested)`; approval (maker-checker) when > $5,000 or bank changed < 7 days.
5. Submitter worker → `processor.createPayout` with idempotency `payout:{id}` → store partner reference; poll/webhook → `paid` posts `PAYOUT_CLEARING → PARTNER_FBO_CASH`, generates the watermarked receipt + remittance advice.
6. Failure/return: funds back to `AVAILABLE` (ledger `payout_failed`), bank flagged, merchant notified, retries ≤ 3.
7. Reserve engine (Phase 1 subset): daily hold of the plan %, release after `rolling_days`; visible to the merchant.
8. UI `/app/money/payouts` — next payout, schedule, history, receipt download, holds, reserve status, "why is my payout blocked?" explainer.
9. Notification + webhook on every transition.

**Tests:** eligibility matrix (10 cases, each individually failing); concurrent payout requests cannot exceed available balance (property test); double-submit returns the same payout; failure restores balance exactly; receipt hash; timezone/cut-off/holiday table tests; maker-checker enforced.
**Verify:** `pnpm test:integration -- payouts && pnpm test:e2e --grep payout`
**Done when:** a sandbox merchant earns a $100.00 charge, sees $96.80 available after the $3.20 platform fee (§8.3), requests a payout, and every ledger account equals the master spec's worked example.
**Commit:** `feat(FR-PYT-002..012): payouts, approvals, receipts, reserves`

---

### S1.15 — Merchant portal screens

**Goal:** the merchant can run their business without contacting support.
**Depends on:** S1.7–S1.14. **Master spec:** §24, §31, `FR-UX-001..010`. **Effort:** 5 agent-days.
**Features:** `FR-UX-006`, `FR-LDG-011`.

**Build** (each screen: server component, ≤ 6 queries, skeleton/empty/error, responsive, EN/BN, Playwright + axe test)

| Screen | Key elements |
|---|---|
| Home | available/pending/next payout, 30-day volume, action items, checklist, dispute banner (Phase 2) |
| Invoices | list (filters, search, cursor), create, detail (timeline, payments, PDF, link, remind), void |
| Transactions | unified payments/refunds, filters, export (bounded), detail with attempts |
| Balances | four buckets, formula explainer ("why?"), drill-down to ledger lines, CSV |
| Payouts | schedule, request, cancel, history, receipt, holds, reserve |
| Refunds | list + create dialog + status |
| Team | members, roles, invite, remove, pending invites |
| Settings | profile/branding (logo upload ≤ 2 MB, contrast check), bank accounts, notifications, security (MFA, sessions, password) |
| Support | ticket list (Phase 2 full thread; Phase 1 email link acceptable, flagged) |
| Developers | API keys + webhooks (S1.19, S1.12) |

Rules: no optimistic UI on money; every mutation returns a typed result and invalidates the right tags; numbers via `formatMoney`; timezone-aware dates; mobile bottom nav; 44 px targets.

**Tests:** Playwright journeys at 3 breakpoints; axe zero serious; visual snapshots; a "no raw color" lint; a query-count assertion in integration tests (instrument the DB client and fail above 6 per page load).
**Verify:** `pnpm test:e2e --grep portal && pnpm test -- query-budget`
**Done when:** a non-technical user can onboard, invoice, and get paid without a support ticket (usability test with 3 people).
**Commit:** `feat(FR-UX-001..010): merchant portal screens`

---

### S1.16 — Admin console core

**Goal:** staff can operate the platform safely and quickly.
**Depends on:** S1.3, S1.14, S1.15. **Master spec:** §25, §20.5, `FR-ADM-001..004,010,011`. **Effort:** 5 agent-days.
**Features:** `FR-ADM-001..004`, `FR-ADM-006`, `FR-ADM-009..011`, `FR-AUTH-008`.

**Build**

1. Admin shell: permission-gated nav, command palette (`/`), keyboard shortcuts, dense tables (40 px), saved views.
2. Overview: queue counts (KYB, approvals, payouts, review), today's volume/fees, alerts, system health.
3. Merchants list + detail tabs (Summary, KYB, Risk, Transactions, Payouts, Ledger, Tax, Notes, Audit) — notes are internal-only.
4. Approvals inbox: pending `approval_requests` (bank change, payout, refund, adjustment), requester/approver separation enforced in the UI **and** DB, step-up to approve.
5. Payments, refunds, payouts lists with safe actions; ledger explorer (accounts → transactions → entries, hash visible).
6. Staff & roles: invite, assign, remove; role change revokes sessions.
7. Audit search/diff/export (permission + step-up + audited).

**Tests:** every admin route 404s for a role without permission (table-driven); approver ≠ requester; step-up expiry; audit entry for each action; keyboard navigation; empty states.
**Verify:** `pnpm test:e2e --grep admin`
**Done when:** a support agent can resolve a routine merchant request without a superadmin.
**Commit:** `feat(FR-ADM-001..011): admin console core`

---

### S1.17 — The 17 CMS pages, legal versions, SEO

**Goal:** a credible public site, editable without deploys, in EN and BN.
**Depends on:** S0.11, S1.8 (PDF/branding reuse). **Master spec:** §27, `FR-CMS-001..009`, `CR-14`. **Effort:** 5 agent-days.
**Features:** `FR-CMS-001`, `FR-CMS-007`, `FR-SEC-018`.

**Build**

1. Block renderer for the block types in master spec §27.2 (hero, logos, features, steps, pricing table, testimonials, FAQ, CTA, rich text, legal table).
2. Build the **17 pages** with real copy (EN) and BN where meaningful; legal pages (`terms`, `privacy`, `cookies`, `refund-policy`, `acceptable-use`, `aml-kyc`, `merchant-agreement`) get versioned placeholders marked `DRAFT — LEGAL REVIEW REQUIRED`.
3. Admin CMS editor: block-based, live preview, schedule, versions + restore, publish with step-up, cache tags.
4. Navigation editor; footer columns; legal version registry (`legal_versions`) + acceptance capture at merchant sign-up (`legal_acceptances`).
5. SEO: metadata, canonical, hreflang, OG, `sitemap.xml`, `robots.txt`, JSON-LD (Organization, FAQPage); Lighthouse ≥ 95 SEO.
6. Contact form → support ticket + Turnstile + auto-reply.
7. Docs: `/docs` getting started; `/docs/api` placeholder until S1.19 generates OpenAPI.

**Tests:** all 17 slugs render 200 and are in the sitemap; draft pages 404 publicly; publish invalidates cache; broken-link check in CI; BN falls back to EN with a notice; Lighthouse budgets.
**Verify:** `pnpm test:e2e --grep cms && pnpm exec lighthouse-ci autorun`
**Done when:** the marketing site reads as a real company and every string is editable.
**Commit:** `feat(FR-CMS-001..009): 17 cms pages, legal versions, seo`

---

### S1.18 — Notifications and email infrastructure

**Goal:** the right people learn the right things, reliably, with strict transactional/promotional separation.
**Depends on:** S1.11, S1.14. **Master spec:** §29, `CR-13`, `FR-NTF-001..003`, `FR-EML-001,004,005`. **Effort:** 3 agent-days.
**Features:** `FR-NTF-001..003`, `FR-EML-001`, `FR-EML-005`.

**Build**

1. Migration `0019_support_notifications.sql` — `notifications`, `notification_preferences`, `email_templates`, `email_log`, `email_suppressions`, `support_tickets`, `support_messages`, `canned_responses`.
2. `src/lib/email/transport.ts` — `console` (dev), `resend` (prod), `failover` (SendGrid/Postmark on 5xx); always writes `email_log` with a dedupe key.
3. Templates with React Email (or plain HTML strings) for: invoice sent/paid/overdue, receipt, refund, payout paid/failed, KYB states, bank change, security (new device/MFA), tax form reminder. EN + BN; variables validated; plain-text alternative.
4. Event→channel matrix job (master spec §29.3) driven by `notifications.preferences`.
5. In-app bell + `/app/notifications`; unread counts batched.
6. Admin `/admin/emails`: templates, preview, test send (self only), logs, suppressions.
7. DNS checklist in `docs/runbooks/email-dns.md` (SPF, DKIM, DMARC progression, MAIL FROM, subdomain split).

**Tests:** every template renders with fixture data (no undefined vars); suppression blocks send; dedupe prevents double send; console transport in tests; email never contains PAN or full bank numbers; unsubscribe header only on promotional.
**Verify:** `pnpm test:integration -- email` + Mailpit/Inbucket inspection locally.
**Done when:** turning off `email_sending_enabled` stops all sends without errors.
**Commit:** `feat(FR-NTF,FR-EML): notifications, templates, delivery logs`

---

### S1.19 — Public REST API v1, API keys, OpenAPI

**Goal:** merchants integrate without human help; the API is the same code path as the UI.
**Depends on:** S1.11, S1.13, S1.12. **Master spec:** §18.4–§18.6, §28.1, `FR-API-001..005`. **Effort:** 5 agent-days.
**Features:** `FR-API-001..005`.

**Build**

1. Migration `0020_api_keys.sql` — `api_keys` (hashed key, prefix, `sk_test_`/`sk_live_`, scopes, last used, revoke), `api_request_logs`, `report_exports`, `report_schedules`.
2. `src/app/api/v1/**` route handlers for the Phase-1 catalog: `account`, `balance`, `invoices` (+finalize/send/void/pdf/payment_link), `payment_links`, `payments` (+capture/void), `refunds`, `customers`, `products`, `payouts`, `webhook_endpoints`, `events`.
3. `withApiAuth(handler)` — bearer key → hash → active key → scopes → rate limit → `request_id`; never accepts a merchant id from the body.
4. Consistent envelope + errors (Appendix B), cursor pagination, `Idempotency-Key` on all mutations, `livemode` flag, `KDPAY-Version` header.
5. Zod schemas → `zod-to-openapi` → `/docs/api` + `openapi.json`; examples in cURL/Node/PHP.
6. Sandbox simulator endpoints (`/v1/test/*`) gated to `livemode=false`.
7. Rate limits per key/plan with headers; 429 `Retry-After`.

**Tests:** contract tests per endpoint (auth, scope, 404 cross-tenant, validation, idempotency, pagination); OpenAPI validates against the implementation (schemathesis or a custom fuzz); rate-limit test; sandbox/live isolation.
**Verify:** `pnpm test:contract -- api && pnpm exec openapi-diff` (or schema validation)
**Done when:** a Node script can create a customer, invoice, link, payment (sandbox), refund, and read balance using only the docs.
**Commit:** `feat(FR-API-001..005): public api v1, keys, openapi`

---

### S1.20 — Statements, reconciliation (manual), daily close

**Goal:** finance can prove the ledger matches the processor every day — before volume makes it impossible.
**Depends on:** S1.11, S1.14. **Master spec:** §11, §32, `FR-RCN-001..006`, `FR-RPT-005`. **Effort:** 4 agent-days.
**Features:** `FR-RCN-001..006`, `FR-RPT-005`.

**Build**

1. Migration `0021_reconciliation.sql` — `settlement_reports`, `settlement_items`, `reconciliation_runs`, `reconciliation_items`, `statements`, `tax_reports`.
2. Settlement import: CSV upload (admin) + adapter `listSettlements` (sandbox/Stripe/Airwallex); normalize, dedupe by processor reference.
3. Matching: payment/refund/payout/fee keys; tolerance rules (master spec §11.3); exceptions with codes.
4. Daily close job: ledger verify + unmatched items > $500 + payout confirmations → `completed_with_exceptions` + alert.
5. Statements: monthly PDF (opening/closing, volume, refunds, fees, payouts, reserve change) + CSV; watermarked; delivered to merchant.
6. Admin `/admin/finance/reconciliation` — runs, exceptions, resolve with note/owner; `/app/reports` — sales/fees/payouts CSV exports (streamed, expiring links).

**Tests:** fixture settlement files with missing/duplicate/mismatched items produce the right exceptions; auto-match rate ≥ 98% on the fixture; a variance > $1 alerts; statement totals equal ledger sums; export streams (no memory blow-up at 100k rows).
**Verify:** `pnpm test:integration -- recon`
**Done when:** a full sandbox day reconciles to zero variance.
**Commit:** `feat(FR-RCN-001..006,FR-RPT-005): settlement import, recon, statements`

---

### S1.21 — End-to-end hardening and the Phase 1 gate

**Goal:** prove the whole thing works, safely, under load and under attack.
**Depends on:** all Phase 1. **Master spec:** §33, §32, §19, Appendix G. **Effort:** 6 agent-days.
**Features:** `FR-NFR-001`.

**Build / run**

1. **Smoke script** `scripts/smoke.ts` (also `pnpm smoke`): seed merchant → approve → invoice → pay (sandbox) → assert ledger → refund → payout → statement. Runs on every deploy to staging.
2. **E2E suite**: onboarding, invoice pay, refund, payout, admin approval, CMS publish, API flow — 3 breakpoints, EN/BN.
3. **Security pass**: ZAP baseline, Semgrep, dependency audit, secret scan, SSRF/uploads/IDOR fuzz, session replay, CSRF, mass assignment; fix criticals/highs.
4. **Performance pass**: k6 checkout 50 rps p95 < 1.5 s; dashboards p95 < 700 ms; query budget enforced; bundle budgets.
5. **Reliability pass**: chaos (duplicate webhooks, out-of-order, processor timeout, worker crash), restore drill, dead-letter replay.
6. **Accessibility pass**: axe + manual screen-reader on the 6 critical flows.
7. **Docs**: `docs/runbooks/*` written for the P1 scenarios; `docs/OPERATIONS.md` with daily/weekly/monthly checklists.
8. **Phase 1 gate review** against master spec Appendix G and §34.2 caps (≤ 50 merchants, ≤ $250k monthly, disputes manual).

**Verify:** `pnpm verify && pnpm test:e2e && pnpm smoke` all green on staging; zero P0/P1; pentest highs closed.
**Done when:** the checklist in §34.2 of the master spec is fully ticked and signed off in `docs/PROGRESS.md`.
**Commit:** `test(S1.21): e2e, security, perf, chaos, runbooks, phase 1 gate`

---

## 6. Phase 2 — Money Out & Scale (S2.1–S2.18)

**Phase 2 outcome:** disputes are fought and accounted; reserves, negative balances and write-offs are real; subscriptions and fee reporting pay for the platform; reports, SDKs, the WooCommerce plugin, the finished CMS, support and email marketing ship; the platform survives a pentest, a load test, and a restore drill.

**Rules for this phase**

- Phase 1 must be closed: the gate in §5 passed and signed in `docs/PROGRESS.md`.
- Same packet discipline as §5 — every step has Goal, Depends on, Master spec, Features, Build, Tests, Verify, Done when, Commit. A step is not done until its `docs/steps.json` row is `done` and `pnpm check:steps --strict` is green.
- Migration numbering continues at **0022**. Never renumber; never edit a pushed migration.
- No Phase 3 table, route or dependency may appear here. If a Phase 2 step needs one, it stops and asks (§0.6).

### S2.1 — Disputes: intake, fund freeze, evidence, outcomes, ratio

**Goal:** every chargeback is caught the hour it arrives, the money is frozen correctly, evidence is submitted before the deadline, and the outcome is accounted.
**Depends on:** S1.11, S1.13, S1.14. **Master spec:** §12, §8.5, §6.10, Appendix D. **Features:** `FR-DSP-001..010`. **Effort:** 6 agent-days.

**Build**

1. Migration `0022_disputes.sql` — `disputes`, `dispute_evidence`, `dispute_responses`, `dispute_events`, `private.dispute_reason_codes`, `private.network_thresholds`, `private.holidays` (master spec §12.2, §6.10) + RLS + exposure block.
2. Intake from the processor webhook (`dispute.created`, `dispute.updated`, `dispute.closed`): idempotent by processor id, reason code → evidence checklist, `needs_response` with the network deadline computed from business days and the holiday calendar.
3. Fund freeze: the transition to `needs_response` moves exactly the dispute amount from `AVAILABLE` to `DISPUTED` in one ledger transaction (`dispute_opened`, `FR-DSP-001`); if the balance is insufficient, still freeze what exists and record `negative_balance_offset` (S2.2 rules) — never fail silently.
4. Merchant evidence portal `/app/disputes/[id]`: reason-code checklist, file upload (10 MB, 20 files, magic bytes + scan, `FR-DSP-004`), narrative ≤ 3 000 chars, deadline countdown in the merchant timezone, alerts at 72/48/24 h (worker job, `FR-DSP-002`).
5. Submission (`FR-DSP-005`): action with `disputes.manage`, step-up, confirmation summary, audit, outbox; staff may submit on behalf of a merchant only with a second approver (`FR-DSP-009`).
6. Auto-generated evidence bundle (`FR-DSP-006`): invoice PDF, receipt, AVS/CVV/3DS results, customer IP/device, delivery/tracking, prior refund history, T&Cs version accepted — assembled into a single PDF with a cover sheet.
7. Outcomes (`FR-DSP-007`): won → `DISPUTED` → `AVAILABLE`; lost → `DISPUTED` → platform loss + `dispute_fee`; accepted → same as lost with a reason. Ledger test for all four transitions.
8. Retrieval/warning requests (`FR-DSP-010`) create a `dispute` row with `kind='inquiry'` and no fund movement.
9. Ratio monitor (`FR-DSP-008`): daily job computes chargeback ratio per merchant, per MCC and platform-wide; alerts at 0.65 % (warning) and 0.9 % (mandate risk); admin tile + email to risk.

**Tests:** each reason code renders its checklist; deadline math across a holiday; frozen amount equals dispute amount; won/lost/accepted ledger assertions; duplicate webhook does not double-freeze; 21st file rejected; late submission blocked with a business-rule error.
**Verify:** `pnpm test:integration --grep "dispute" && pnpm test:e2e --grep "dispute evidence"`.
**Done when:** a sandbox dispute travels intake → evidence → submit → won with correct ledger on both paths, and the ratio alert fires in a seeded scenario.
**Commit:** `feat(FR-DSP-001..010): disputes, evidence portal and ratio monitoring`

### S2.2 — Reserves, negative balances, dunning, write-off

**Goal:** the platform never eats a merchant's debt silently, and reserve money is released on time.
**Depends on:** S1.14, S2.1. **Master spec:** §10.7–§10.8, §8.4. **Features:** `FR-PYT-008`, `FR-PYT-011`. **Effort:** 4 agent-days.

**Build**

1. Migration `0023_negative_balance.sql` — `reserves` extensions (rolling percentage, release schedule), `reserve_releases`, `negative_balance_events`, `dunning_attempts`, `write_offs` + RLS.
2. Rolling reserve engine: percentage of captured volume held for N days, released by a daily job in FIFO order, partial release when a dispute is open on the released amount, forfeiture only via maker-checker.
3. Negative balance detection: every ledger post checks the merchant's `AVAILABLE`; a negative balance creates an event, blocks payouts, and starts the dunning ladder (day 0 notification, day 3 retry of the offset, day 7 suspension of charges, day 21 write-off proposal).
4. Offsets: incoming volume auto-applies to the negative balance before becoming available (`negative_balance_offset` entries), per the master spec's priority order.
5. Write-off (`FR-PYT-011`): propose (staff) → approve (different staff with `finance.adjust`) → ledger `write_off` + `reserves` adjustment + audit; never delete the debt row.
6. Admin screens: reserve schedule per merchant, negative balance queue with ageing, dunning timeline.
7. Notifications: reserve release, negative balance, suspension warning, write-off (see S1.18 templates).

**Tests:** reserve release on day N (± timezone); release blocked by an open dispute; negative balance triggers payout block; offset ordering; write-off requires two users; ageing bucket math.
**Verify:** `pnpm test:integration --grep "reserve|negative"`.
**Done when:** a merchant with a lost dispute larger than their balance ends suspended, offset by the next volume, and the remainder written off with two approvers, all visible in the ledger.
**Commit:** `feat(FR-PYT-008,011): reserves, negative balance and write-off`

### S2.3 — Ledger operations: adjustments and period close

**Goal:** finance can correct the ledger without breaking it, and close periods so history cannot move.
**Depends on:** S1.5, S1.13. **Master spec:** §7.6–§7.7, §8.6. **Features:** `FR-LDG-007`, `FR-LDG-008`, `FR-LDG-010`. **Effort:** 4 agent-days.

**Build**

1. Migration `0024_ledger_ops.sql` — `ledger_periods` extensions (`closed_at`, `closed_by`, `reopened_*`), `ledger_adjustment_requests` (maker/checker, reason code, evidence, amount), triggers `protect_closed_periods` (any post into a closed period raises `PERIOD_CLOSED`).
2. Adjustment flow: request (`finance.adjust` request) → different approver → single `adjustment` ledger transaction with a mandatory reason code and an attachment; both parties audited with a diff.
3. Period close: a monthly job proposes; staff close; reopening requires `finance.close` + step-up + a written reason and emits a high-severity audit event.
4. Admin ledger explorer (basis for `FR-ADM-007`): filter by merchant, type, reference, date; show entries with running balance; every row links to its source object.
5. Merchant-visible corrections: an adjustment appears in the merchant's statement with its reason code (no internal notes).

**Tests:** a post into a closed period fails with `PERIOD_CLOSED`; adjustment by the same user is rejected; reopened period allows posts and re-closes; explorer pagination is stable under inserts; the ledger chain still verifies after adjustments.
**Verify:** `pnpm test:integration --grep "adjustment|period"`.
**Done when:** close → attempt post (fail) → reopen with two approvals → post → re-close, with the chain verifying at the end.
**Commit:** `feat(FR-LDG-007,008,010): adjustments and period close`

### S2.4 — Plans, subscriptions, entitlements and fee reporting

**Goal:** the platform's own pricing runs on the platform, and fee revenue is provable against processor cost.
**Depends on:** S1.6, S1.11, S1.12. **Master spec:** §9.1–§9.5. **Features:** `FR-FEE-001`, `FR-FEE-002`, `FR-FEE-005..008`. **Effort:** 5 agent-days.

**Build**

1. Migration `0025_billing_scale.sql` — `plan_entitlements`, `subscription_changes`, `dunning_events`, `processor_cost_reports` + RLS.
2. Subscription billing: monthly/quarterly/annual cycles, proration on upgrade (credit + charge lines), downgrade at period end, cancel at period end, dunning ladder reusing S2.2's engine.
3. Entitlements (`FR-FEE-006`): users, API keys, invoices/month, storage — enforced in the action wrapper (`action({ entitlement: 'invoices.monthly' })`) with a friendly upgrade path, never a 500.
4. Upgrade/downgrade without data loss (`FR-FEE-007`): never deletes rows; over-limit state is read-only-extend, not deletion; test proves invoices/keys survive.
5. Fee reporting (`FR-FEE-008`): revenue = fee_charges − processor_cost (imported from settlement reports in S2.6) per merchant/plan/month; variance chart; CSV export.
6. Admin plan editor with effective dates and a preview calculator; changing a plan never mutates historical `fee_charges` (snapshot rule from S1.6).

**Tests:** proration math table (12 cases); entitlement block returns a typed error; downgrade keeps data; fee report reconciles to ledger fee accounts; plan change effective-date behavior.
**Verify:** `pnpm test:integration --grep "subscription|entitlement"`.
**Done when:** a merchant upgrades mid-cycle, is charged the correct proration, exceeds an invoice limit and sees the upgrade path, and finance reads a fee report that ties to the ledger.
**Commit:** `feat(FR-FEE-001,002,005..008): subscriptions, entitlements and fee reporting`

### S2.5 — Tax scale: reports, exemptions, jurisdiction data

**Goal:** sales tax is defensible in an audit — rates, exemptions and reports tie to invoices.
**Depends on:** S1.7, S2.6. **Master spec:** §14.1–§14.2. **Features:** `FR-TAX-005`, `FR-TAX-006`. **Effort:** 3 agent-days.

**Build**

1. Migration `0026_tax_scale.sql` — `tax_exemptions` extensions (certificate file, expiry, jurisdiction), `tax_jurisdiction_rates` history, `tax_report_runs`.
2. Exemption certificates (resale, nonprofit, government): upload, expiry, auto-apply at invoice time when the customer + jurisdiction match, audit trail, expiry reminders.
3. Tax reports by jurisdiction/period: taxable sales, tax collected, exempt sales, zero-rated, refunds of tax; CSV with the invoice-level backing rows.
4. Rate table maintenance: effective-dated import (CSV) with a diff preview before commit; historical invoices keep their snapshot (`FR-TAX-004` already snapshots).
5. Admin screen: rates, exemptions queue, report generator.

**Tests:** exempt customer produces zero tax with the certificate referenced; expired certificate stops applying; report totals equal the sum of `invoice_tax_lines`; rate import is idempotent and rejects overlaps.
**Verify:** `pnpm test:integration --grep "tax"`.
**Done when:** a quarter of invoices produces a tax report that ties exactly to invoice tax lines, including exempt sales.
**Commit:** `feat(FR-TAX-005,006): exemptions, jurisdiction rates and tax reports`

### S2.6 — Reports, exports and statements at scale

**Goal:** merchants and staff get answers in seconds without hammering the OLTP tables.
**Depends on:** S1.20, S2.4. **Master spec:** §32.1–§32.4, §11.4. **Features:** `FR-RPT-001`, `FR-RPT-002`, `FR-RPT-003`, `FR-RCN-008`. **Effort:** 5 agent-days.

**Build**

1. Migration `0027_reports.sql` — materialized views `mv_merchant_daily`, `mv_platform_daily`, `mv_fee_daily` + unique indexes + `refresh concurrently` schedule (worker, every 15 min, one at a time via advisory lock).
2. Merchant reports (`FR-RPT-001`): sales, fees, refunds, disputes, tax, payouts — date range, group by day/week/month/product/customer/country; totals must equal the ledger.
3. Admin reports (`FR-RPT-002`): GMV, take rate, net revenue, merchant cohorts (signup month retention), processor mix, approval funnel, dispute ratio, payout volume.
4. Exports (`FR-RPT-003`): streaming CSV (never build in memory), > 100 k rows allowed, written to the `reports` bucket, signed URL with 24 h expiry, `report_exports` row, email when ready; a worker job, not a request.
5. Reconciliation exports (`FR-RCN-008`): daily variance report, exception report, processor-vs-ledger settlement report — CSV + PDF summary.
6. Query budgets: every report page ≤ 4 queries; charts render from one aggregate query; no client-side joins.

**Tests:** report totals equal ledger aggregates for a seeded month; export streams 100 k rows under the memory ceiling; signed URL expires; `refresh concurrently` does not block reads; empty-range and timezone-boundary cases.
**Verify:** `pnpm test:integration --grep "reports" && pnpm test:e2e --grep "reports"`.
**Done when:** a seeded 100 k-payment month produces correct merchant + admin reports, and a 100 k-row CSV export completes without a memory spike.
**Commit:** `feat(FR-RPT-001..003,RCN-008): reports, exports and reconciliation exports`

### S2.7 — SDKs, public API docs and sandbox simulator

**Goal:** an integrator can build against KD PAY in an afternoon without reading our source.
**Depends on:** S1.19, S1.12. **Master spec:** §28.1–§28.2. **Features:** `FR-SDK-001..003`, `FR-API-007..009`. **Effort:** 6 agent-days.

**Build**

1. `packages/sdk-node` — typed client generated from the OpenAPI document (`openapi-typescript` + a thin fetch wrapper), automatic idempotency keys on POST (uuid v4 unless supplied), retries with exponential backoff on 429/5xx and `Retry-After`, typed errors mapped from Appendix B, webhook signature helper.
2. `packages/sdk-embed` — iframe embed that mounts the hosted checkout, handles 3DS redirect/return, posts messages only to the allowlisted origin, keyboard accessible, EN/BN strings, < 15 KB gzipped.
3. Sandbox simulator (`FR-API-007`): endpoints to force a decline, a 3DS challenge, a dispute, a payout failure — sandbox keys only, audited, refused in live mode.
4. Docs (`FR-API-008`): Scalar/Stoplight page generated from OpenAPI at `/docs/api`, plus guided pages (quickstart, webhooks, testing, errors) with copy-paste examples in curl, Node and PHP (WooCommerce audience).
5. Sampled request logs (`FR-API-009`): 1-in-N sampling of `api_request_logs` with headers redacted, 30-day retention, merchant-facing "recent requests" page with request id → support handoff.
6. Publishing: npm publish with provenance in CI, versioned by tag, `@kdpay/node` semver; a canary install test in CI.

**Tests:** SDK contract tests against the OpenAPI schema; idempotency replay; backoff honors `Retry-After`; embed works in the app's iframe-sandbox test page; simulator refuses in live mode; docs build has zero broken links.
**Verify:** `pnpm --filter @kdpay/node test && pnpm test:e2e --grep "embed" && node scripts/check-links.mjs docs/api`.
**Done when:** the quickstart in the docs, run verbatim against sandbox, creates an invoice, a payment link and receives a webhook.
**Commit:** `feat(FR-SDK-001..003,API-007..009): SDKs, docs and sandbox simulator`

### S2.8 — WooCommerce plugin v1

**Goal:** a Bangladeshi merchant installs a zip, pastes keys, and takes card payments in WooCommerce without touching code.
**Depends on:** S2.7. **Master spec:** §28.3. **Features:** `FR-WOO-001..008`. **Effort:** 8 agent-days.

**Build**

1. Plugin scaffold (PHP 8.1+, WP 6.4+, declared HPOS compatibility), settings screen with sandbox toggle, keys (encrypted at rest via WP options + our API), webhook secret, redacted debug log.
2. Connect + capability check (`FR-WOO-001`): server-side call to `/v1/account` verifying scopes, currency (USD), and that the merchant is approved — with actionable error messages.
3. Checkout redirect to the hosted page (`FR-WOO-002`): create invoice + payment link server-side, store the mapping, handle cancel/return, set order status from webhooks (never from the redirect alone), idempotent by order key.
4. Webhooks (`FR-WOO-003`): raw-body HMAC verification before any state change, `wp_schedule_single_event` retry, replay protection via a stored event id, and a mismatch log for debugging.
5. Refunds (`FR-WOO-004`): full/partial from the WooCommerce admin, idempotent, status synced back, failure surfaces to the admin.
6. HPOS + Blocks (`FR-WOO-005`): declare compatibility, use `$order->get_meta()`/CRUD APIs, Blocks checkout integration (React, `wc.wcSettings`).
7. i18n EN/BN + uninstall cleanup (`FR-WOO-007`), sandbox toggle + debug log (`FR-WOO-006`).
8. Distribution (`FR-WOO-008`): GitHub release zip + `readme.txt`, screenshots, changelog, install instructions; manual QA matrix on WP 6.4–latest with HPOS on/off.

**Tests:** PHP unit tests for signature verification and order transitions; a Playwright run against a dockerized WordPress with the plugin installed (happy path + decline + refund); webhook replay ignored.
**Verify:** `pnpm test:woo` (docker compose up WordPress, install plugin, run the three journeys).
**Done when:** the dockerized store completes a payment end-to-end from a sandbox card, refunds it, and the order statuses match the ledger.
**Commit:** `feat(FR-WOO-001..008): WooCommerce plugin v1`

### S2.9 — CMS finalize: blog, media, navigation, legal, docs

**Goal:** marketing can run the site without a developer, and the legal pages are versioned and provable.
**Depends on:** S0.11, S1.17. **Master spec:** §27.1–§27.6. **Features:** `FR-CMS-002..006`, `FR-CMS-009`, `FR-CMS-010`. **Effort:** 6 agent-days.

**Build**

1. Migration `0029_cms_scale.sql` — `blog_posts` (+localizations, versions), `media_variants`, `navigation_revisions`, `legal_acceptance_versions` if not present.
2. Blog (`FR-CMS-002`): MDX or rich text (choose one and document it), draft → review → scheduled → published, author, tags, canonical URL, OG image, RSS, reading time, `noindex` until published.
3. Navigation editor (`FR-CMS-003`): drag-to-reorder tree, max depth 2, per-locale labels, publish with revision history and rollback.
4. Media library (`FR-CMS-004`): 2 MB limit, WebP/AVIF conversion by the storage helper, alt text required (a11y), usage list ("where is this image used"), safe delete.
5. Legal versions (`FR-CMS-005`): publish a new version → merchants must re-accept at next login (modal, blocking for payments), acceptance rows with version + timestamp + IP, admin list of who has not accepted.
6. SEO (`FR-CMS-006`): per-page title/description/OG, sitemap with `lastmod`, hreflang pairs EN/BN, JSON-LD (Organization, Product, FAQ, BreadcrumbList), canonical rules, `robots.txt` per environment.
7. Draft/preview/publish with cache invalidation (`FR-CMS-009`): preview tokens (signed, 1 h, no index), publish bumps `revalidateTag`.
8. Docs (`FR-CMS-010`): `/docs` for merchant help articles managed in the CMS + the generated API reference from S2.7, with search.

**Tests:** scheduled publish flips at the right minute; preview link works only with the token; legal re-acceptance blocks payment until accepted; sitemap includes only published pages; media delete warns when referenced; hreflang reciprocity.
**Verify:** `pnpm test:e2e --grep "cms" && node scripts/check-links.mjs src/app/(marketing)`.
**Done when:** a non-technical run-through (documented) edits a page, publishes a legal version, schedules a blog post, and swaps a hero image — with no deploy.
**Commit:** `feat(FR-CMS-002..006,009,010): CMS blog, media, legal versions and docs`

### S2.10 — Support system: tickets, SLA, CSAT

**Goal:** buyer and merchant questions land in one queue with deadlines and history.
**Depends on:** S1.18, S1.17. **Master spec:** §30. **Features:** `FR-SUP-001..003`. **Effort:** 4 agent-days.

**Build**

1. Migration `0030_support_scale.sql` — `sla_policies`, `ticket_events`, `csat_responses`, `ticket_links` (merchant/payment/invoice/dispute) + RLS.
2. Ticket lifecycle (`FR-SUP-001`): new → open → pending customer → resolved → closed; SLA by priority (P1 1 h, P2 4 h, P3 1 business day), first-response + resolution timers, breach alerts, auto-escalation, reopen window.
3. Threads (`FR-SUP-002`): merchant/staff messages, **internal notes** (never selected by merchant RLS — a dedicated test proves it), attachments via the storage helper, email ↔ ticket sync (reply by email appends to the thread with signature verification).
4. Canned responses (`FR-SUP-003`) with variables (`{{merchant.name}}`, `{{invoice.number}}`), per-category, permission-gated editing.
5. CSAT: one-click survey after resolution, score on the admin dashboard.
6. Merchant portal `/app/support`: new ticket, thread, attachments, status; contact form from the marketing site creates a ticket (Turnstile + rate limit).

**Tests:** SLA timers across timezones and holidays; internal note invisible to merchant API/RLS; email reply appends; reopen after close creates an event; CSAT recorded once.
**Verify:** `pnpm test:integration --grep "ticket" && pnpm test:e2e --grep "support"`.
**Done when:** a merchant opens a ticket, staff replies by email, the merchant answers in the portal, SLA timers are correct, and the internal note never appears in any merchant response.
**Commit:** `feat(FR-SUP-001..003): support tickets, SLA and CSAT`

### S2.11 — Email at scale: promotional separation, templates, delivery logs

**Goal:** transactional mail never gets punished for marketing mail, and every send is traceable.
**Depends on:** S1.18. **Master spec:** §29.4–§29.5. **Features:** `FR-EML-002..004`. **Effort:** 4 agent-days.

**Build**

1. Migration `0031_email_scale.sql` — `email_delivery_events`, `email_template_versions`, `marketing_contacts`, `email_suppressions` extensions (bounce/complaint reason, scope: transactional vs marketing).
2. Promotional separation (`FR-EML-002`): separate subdomain (`mail.` vs `news.`), separate sending key, separate suppression scope — a marketing complaint must never block a receipt; the inverse is also true.
3. Template editor (`FR-EML-003`): variables with validation, live preview with sample data, per-locale versions, version history + rollback, test-send.
4. Delivery logs (`FR-EML-004`): webhook events from the provider (delivered, bounced, complained, opened) into `email_delivery_events`; bounce types (hard/soft), auto-suppress hard bounces and complaints; merchant-facing "recent emails to this customer" in the admin.
5. SPF/DKIM/DMARC runbook + a `scripts/check-email-auth.mjs` that verifies records for both subdomains.
6. Unsubscribe: signed, one-click (`List-Unsubscribe` + `List-Unsubscribe-Post`), transactional mail excluded by policy, marketing-only preference center.

**Tests:** marketing suppression does not block transactional; hard bounce suppresses; template variable validation rejects unknown vars; unsubscribe token tampering rejected; DMARC check script parses record syntax.
**Verify:** `pnpm test:integration --grep "email" && node scripts/check-email-auth.mjs`.
**Done when:** a receipt still delivers to an address that complained about a newsletter, and both subdomains pass the auth check.
**Commit:** `feat(FR-EML-002..004): email separation, templates and delivery logs`

### S2.12 — Compliance at scale: KYC, ongoing monitoring, periodic review

**Goal:** the platform can grow past manual KYB without losing the compliance trail.
**Depends on:** S1.3, S2.1. **Master spec:** §3.6, §17.4, §19.3. **Features:** `FR-KYB-007`, `FR-KYB-011`, `FR-KYB-012`. **Effort:** 6 agent-days.

**Build**

1. Migration `0032_compliance_monitoring.sql` — `review_schedules`, `monitoring_events`, `kyc_provider_calls`, `remediation_tasks` + RLS.
2. KYC for individuals (`FR-KYB-011`): provider adapter interface (`verifyIdentity`) with a manual fallback (document + selfie review), liveness result storage, decision merge into the KYB decision.
3. Periodic review (`FR-KYB-007`): risk-level schedule (L1 annual, L2 6 months, L3 quarterly), task generation, merchant document request, escalation on non-response (30/60/90 days → charges disabled).
4. Ongoing monitoring (`FR-KYB-012`): nightly job flags volume spikes (> 3× trailing 90-day average), dispute ratio breach, refund spikes, MCC/website changes, sanctions re-screen of UBOs; each flag creates a review task with a reason code.
5. Sanctions/PEP re-screening on a schedule (daily delta, weekly full) with match scoring and manual adjudication.
6. Admin queue: reviews due, monitoring alerts, remediation tasks — all with SLA and owner.

**Tests:** review dates computed correctly from risk level; a volume spike creates exactly one alert per day; re-screen match → task; charges disabled after the final escalation; provider adapter failure falls back to manual without losing data.
**Verify:** `pnpm test:integration --grep "monitoring|review"`.
**Done when:** a seeded merchant trips a volume rule, gets a review task, misses it, and ends with charges disabled — all audited.
**Commit:** `feat(FR-KYB-007,011,012): KYC adapter, periodic review and monitoring`

### S2.13 — Catalog and invoice extras

**Goal:** the invoice product is complete for real merchants, not just early adopters.
**Depends on:** S1.7, S1.9. **Master spec:** §15.2–§15.8. **Features:** `FR-INV-012..014`, `FR-INV-016`. **Effort:** 4 agent-days.

**Build**

1. Migration `0033_catalog_extras.sql` — `import_jobs`, `import_rows`, `reminder_runs` + RLS; index for catalog search (`pg_trgm`).
2. Product catalog (`FR-INV-012`): SKU, default price, tax code, unit, active flag, per-merchant; line-item autocomplete in the invoice editor; CSV import/export.
3. Customer/product CSV import (`FR-INV-013`): template download, dry-run preview with per-row errors, 5 000 rows per job, background job with progress, idempotent by external id.
4. Partial payments (`FR-INV-014`): opt-in per invoice (`allow_partial`), enforce `sum(payments) ≤ total`, show remaining balance, link each payment, block overpayment, allow the merchant to disable after the first partial payment only if unpaid remainder is zeroed.
5. Bulk reminders (`FR-INV-016`): select invoices → send, per-invoice throttle (max 1 reminder / 24 h, max 5 total), unsubscribe-respecting, audit, preview count before send.
6. Merchant UI: catalog page, import wizard, reminder scheduler.

**Tests:** partial payments never exceed the total (DB + app); import dry-run reports duplicate SKUs; bulk reminder respects throttle; product deletion blocked when used by a draft invoice.
**Verify:** `pnpm test:integration --grep "catalog|partial|reminder"`.
**Done when:** a 5 000-row import completes with a correct error report; an invoice paid in three parts closes exactly once.
**Commit:** `feat(FR-INV-012..014,016): catalog, imports, partial payments and reminders`

### S2.14 — Payment extras: wallets, partial capture, retries, offline payments

**Goal:** the payment engine handles the cases real merchants ask for in month two.
**Depends on:** S1.11, S1.13. **Master spec:** §16.4–§16.8. **Features:** `FR-PAY-010..012`, `FR-PAY-014`. **Effort:** 5 agent-days.

**Build**

1. Migration `0034_payment_extras.sql` — `wallet_tokens`, `offline_payments`, `offline_payment_proofs`, `retry_schedules` + RLS.
2. Wallets (`FR-PAY-010`): Apple Pay / Google Pay through the processor's hosted fields only (still SAQ-A); merchant-domain verification documented; hide the button when the processor or the buyer's device does not support it.
3. Partial capture (`FR-PAY-011`): capture any amount ≤ authorized, release the remainder, ledger posts for both, invoice `balance_due` reflects the uncaptured part, allowed only when `allow_partial`.
4. Retry reminders + cancel conditions (`FR-PAY-012`): schedule per decline class (soft ≤ 5/24 h per `FR-PAY-004`), buyer email with a fresh link, stop on success/cancel/expiry; a job, never inline.
5. Offline/recorded payments (`FR-PAY-014`): bank transfer/wire recorded by the merchant or staff with proof upload (hashed, scanned), reference, date, amount, maker-checker above a threshold, ledger entry type `adjustment`/`payment_captured` with `processor='offline'`, and a receipt PDF.
6. Reconciliation hook: offline payments appear in recon with `source='offline'` and never auto-match a processor settlement.

**Tests:** partial capture math + ledger; wallet button hidden when unsupported; retry schedule stops after success; offline payment above threshold requires approval; offline payment cannot be edited after capture (only reversed).
**Verify:** `pnpm test:integration --grep "capture|offline|wallet"`.
**Done when:** an authorization is captured partially, the remainder voided, and an offline wire is recorded with proof — all visible in the statement.
**Commit:** `feat(FR-PAY-010..012,014): wallets, partial capture, retries and offline payments`

### S2.15 — Admin consoles: risk, finance, processors, countries

**Goal:** operations can run the platform without touching SQL.
**Depends on:** S1.16, S2.3, S2.12. **Master spec:** §25.1–§25.4. **Features:** `FR-ADM-005`, `FR-ADM-007`, `FR-ADM-008`, `FR-ADM-012`. **Effort:** 5 agent-days.

**Build**

1. Migration `0035_admin_scale.sql` — `processor_accounts`, `country_configs`, `risk_rules` extensions, `blocklist_entries` + RLS.
2. Risk console (`FR-ADM-005`): queue (manual review from S1.11), decision detail with the exact rule hits, blocklist (card fingerprint, IP, email, device), rules editor with a JSON schema and a dry-run simulator against recent payments.
3. Finance console (`FR-ADM-007`): ledger explorer (from S2.3), recon runs, adjustment requests, fee reports, payout oversights.
4. Processor console (`FR-ADM-008`): accounts per entity (platform vs merchant of record), routing table, health (success rate, latency, error mix), sandbox/live badges, disable switch with an audit trail.
5. Country enablement (`FR-ADM-012`): per-country allowed/blocked, risk tier, processor mapping, required documents, currency, payout rail; a merchant from a non-enabled country is blocked at signup with a clear message.

**Tests:** blocklist blocks the next payment; rule dry-run does not mutate; processor disable stops new payments but not webhooks; country toggle blocks signup; every console action is audited.
**Verify:** `pnpm test:e2e --grep "admin"`
**Done when:** an operator blocks a card, disables a processor, and turns off a country — each with an audit entry and no deploy.
**Commit:** `feat(FR-ADM-005,007,008,012): risk, finance, processor and country consoles`

### S2.16 — UX scale: dark mode, full Bangla parity, accessibility and performance gates

**Goal:** the product feels finished in both languages, on a phone, in dark mode, with a screen reader.
**Depends on:** S1.15, S1.16, S1.17. **Master spec:** §31.8–§31.12, §5.6, §5.9. **Features:** `FR-UX-004`, `FR-UX-005`, `FR-NFR-008`. **Effort:** 6 agent-days.

**Build**

1. High-contrast light/dark themes (`FR-UX-004`): token sets with contrast ≥ 7:1 for text (AAA) on the dashboard, ≤ 3:1 for borders, no pure black; per-user preference stored server-side; system preference default; a contrast validator in CI.
2. Full EN/BN parity (`FR-UX-005`): every string in both locales, Bengali numerals option, date/number/currency formatting via `Intl`, RTL-safe layout primitives (for future), `next-intl` message lint that fails on a missing key, a screenshot diff per locale for 10 key screens.
3. Accessibility gates (`FR-NFR-008`): axe on 20 routes × 2 viewports × 2 themes, keyboard-only journey for the 6 critical flows, screen-reader script (VoiceOver/NVDA) recorded in `docs/QA-A11Y.md`, focus-visible everywhere, reduced-motion respected.
4. Performance gates: Lighthouse CI budgets (dashboard LCP < 2.5 s on 4G, CLS < 0.1, TBT < 200 ms; marketing < 2 s), bundle size budget per route (`size-limit`), query-count budget per page (instrumented in dev, asserted in tests).
5. Regression prevention: both gates wired into CI as required checks; a failing budget blocks the merge.

**Tests:** message lint catches a missing key; contrast validator passes both themes; axe zero criticals on 20 routes; Lighthouse budgets green; screenshots stable.
**Verify:** `pnpm test:a11y && pnpm test:lighthouse && pnpm i18n:lint`.
**Done when:** both locales render every screen with no missing key, axe has zero critical/serious issues, and every route is inside its budget.
**Commit:** `feat(FR-UX-004,005,NFR-008): dark mode, Bangla parity, a11y and performance gates`

### S2.17 — Activity feed, retention and DSAR

**Goal:** merchants see their own history, and privacy requests are answered on time with evidence.
**Depends on:** S0.9, S1.15. **Master spec:** §21.1–§21.5, §33.3. **Features:** `FR-AUD-006`, `FR-SEC-017`. **Effort:** 3 agent-days.

**Build**

1. Migration `0036_retention.sql` — `retention_policies`, `dsar_requests`, `dsar_exports`, `activity_feed` (view over audit + domain events, merchant-scoped) + RLS.
2. Merchant activity feed (`FR-AUD-006`): "who changed what, when" for the last 90 days — invoices, settings, team, bank details, API keys, logins; filters and CSV export; internal notes and staff-only fields excluded by the view definition.
3. Retention (`FR-SEC-017`): per-table policies (e.g. `api_request_logs` 30 days, `login_attempts` 90 days, `email_delivery_events` 1 year, financial records 7 years), a nightly purge job that records what it deleted, and a legal-hold flag that blocks purging for a merchant.
4. DSAR: access (export), deletion (with the financial-record exception), correction; identity verification before action; SLA timer (30 days); output as a signed zip with a manifest; deletion is anonymization where the law requires retention.
5. Privacy screens: consent history for a customer, cookie notice record, marketing opt-out state.

**Tests:** feed excludes internal fields (RLS-level test); purge deletes only expired rows and respects legal hold; DSAR export contains the right tables and no other tenant's data; deletion anonymizes but keeps ledger integrity.
**Verify:** `pnpm test:integration --grep "retention|dsar"`.
**Done when:** a DSAR runs end-to-end in a test tenant, the zip contains only that tenant's data, and the nightly purge is idempotent.
**Commit:** `feat(FR-AUD-006,SEC-017): activity feed, retention and DSAR`

### S2.18 — Phase 2 hardening, pentest and load

**Goal:** prove the scaled platform is safe and fast enough to raise limits.
**Depends on:** all Phase 2. **Master spec:** §33, §34.3, §36. **Features:** `FR-SEC-015`. **Effort:** 6 agent-days.

**Build**

1. External pentest (or a documented internal equivalent if budget is zero — say which in `docs/PROGRESS.md`); ASV-style scan; remediation log with severity, owner, date; no highs open.
2. Load test at 5× Phase-1 volume: checkout 100 rps p95 < 1.5 s, dashboards p95 < 700 ms, worker throughput > 50 events/s, DB connections < 80 % of the pooler limit.
3. Soak test 4 h: memory flat on the worker, no connection leak, queue depth stable.
4. Chaos: processor timeout, webhook storm ×10, DB connection drop, Redis-less mode (there is none — prove it), worker crash mid-payout.
5. Restore drill #2 with the new data volume; record RTO.
6. Raise caps in `docs/PROGRESS.md` only after all of the above; otherwise keep Phase 1 caps.
7. Update the master spec's §34.3 limits table if the evidence supports it (change-control, §20.3).

**Tests:** load/soak scripts in `tests/load/`; results committed as markdown, not screenshots.
**Verify:** `pnpm test:load:phase2` (k6) and the pentest report link in `docs/PROGRESS.md`.
**Done when:** zero open highs, all load targets met, RTO recorded, and the new caps signed off.
**Commit:** `test(FR-SEC-015): phase 2 hardening, pentest and load`

### Phase 2 gate (before any Phase 3 work)

- [ ] Disputes, reserves, adjustments, subscriptions, reports, SDKs, WooCommerce, CMS, support and email scale all shipped and tested.
- [ ] Every `FR-*` with phase 2 in master spec §35 is `done` in `docs/steps.json`.
- [ ] Pentest: no highs open; load and soak targets met; restore drill #2 done.
- [ ] `pnpm check:steps --strict` green; coverage thresholds unchanged or raised.

---

## 6A. Phase 3 — Global & Enterprise (S3.1–S3.8)

**Phase 3 outcome:** the platform routes across processors and countries, settles cross-border, files tax forms, and survives an enterprise security review.

**Rules:** one step at a time; each requires a written business decision in `docs/OPEN_QUESTIONS.md` (market, entity, partner) before code starts. Migration numbering continues at **0040**.

### S3.1 — Multi-processor routing and failover

**Goal:** a payment goes to the processor most likely to approve it, and a processor outage stops nothing.
**Depends on:** S1.10, S2.14. **Master spec:** §4.2–§4.3, §25.1. **Features:** `FR-PAY-013`. **Effort:** 8 agent-days.

**Build**

1. Routing table (country, MCC, amount band, card brand, currency) → processor account; rules editable in the admin console with a dry-run.
2. Health-based failover: circuit breaker per processor (5 failures / 60 s → open 30 s), failover only before authorization, never after; the buyer sees one attempt, not two declines.
3. Cost-aware ordering (interchange + platform spread) as a tie-breaker, configurable.
4. Idempotency across processors: one `payment_attempt` chain per checkout, processor refs stored per attempt, ledger posts once.
5. Webhooks from every processor normalized into one event bus (already built in S1.10/S1.12) with per-processor signature verification.
6. A/B reporting: approval rate and cost per route, with a monthly review doc.

**Tests:** breaker opens and closes; failover preserves idempotency; a duplicate webhook from a second processor cannot double-post; routing rules produce the expected processor for a matrix of 30 cases.
**Verify:** `pnpm test:integration --grep "routing|failover"`.
**Done when:** killing the primary processor in staging still completes a checkout through the secondary with exactly one ledger transaction.
**Commit:** `feat(FR-PAY-013): multi-processor routing and failover`

### S3.2 — FX and cross-border payouts

**Goal:** a merchant in Bangladesh gets paid in local currency, with the spread accounted for and disclosed.
**Depends on:** S1.14, S3.1. **Master spec:** §7.5, §10.5, §8.3. **Features:** `FR-LDG-012`. **Effort:** 10 agent-days.

**Build**

1. Currency model: invoice currency (USD) vs settlement currency vs payout currency; `fx_quotes` with a validity window (60 s), locked quote on payout creation, spread as a separate ledger entry (`fx_spread`), never hidden in the rate.
2. Payout rails per corridor: local ACH/EFT/SEPA/UPI/bKash-type partners via the partner adapter; capability check at onboarding; per-corridor limits and document requirements.
3. Remittance advice PDF (extends `FR-PYT-007`): amount sent, rate, fee, amount received, reference, compliance footer.
4. Rate source: partner API + a fallback table with a staleness guard (refuse to quote if older than 15 min).
5. Accounting: realized vs unrealized FX, revaluation job at month end, report tying to the ledger.
6. Disclosures: the merchant sees the exact received amount before confirming; the buyer sees the invoice currency only.

**Tests:** quote expiry; spread accounting balances; revaluation posts once per period; unsupported corridor blocked with a typed error; remittance advice totals match the ledger.
**Verify:** `pnpm test:integration --grep "fx|corridor"`.
**Done when:** a USD invoice is paid, a BDT payout is executed against a sandbox partner, and the ledger proves the spread and the received amount.
**Commit:** `feat(FR-LDG-012): FX, corridors and cross-border payouts`

### S3.3 — Tax reporting: 1099-K / 1042-S, withholding, engine adapter

**Goal:** year-end filing data is generated from the ledger, not from a spreadsheet.
**Depends on:** S1.3, S2.5. **Master spec:** §3.7, §14.2. **Features:** `FR-TAX-002`, `FR-TAX-003`, `FR-TAX-007`, `FR-TAX-008`. **Effort:** 10 agent-days.

**Build**

1. Withholding (`FR-TAX-002`): treaty rate by country + form type, application at payout time, `tax_withholding` ledger entry, payout blocked when the form is missing/expired.
2. 1099-K / 1042-S data generation (`FR-TAX-003`): thresholds, TIN validation (format + checksum where applicable), per-payee aggregation, file export in the filer's format, correction files.
3. Filer adapter: interface `submitFiling(batch)` with a sandbox implementation, retries, status tracking, immutable filing records.
4. Tax engine adapter (`FR-TAX-007`): `computeTax(lines, address)` behind an interface (Stripe Tax / Avalara / TaxJar / internal table), with product tax-code mapping and a fallback to the internal engine when the adapter fails.
5. Year-end packet (`FR-TAX-008`): merchant-facing PDF/CSV pack (gross, fees, refunds, disputes, net, tax withheld), generated on demand and archived.
6. Reconciliation with the ledger: filings must tie to `tax_withholding` and `fee_charged` accounts.

**Tests:** treaty rate matrix; threshold boundaries ($600 / 200 transactions); TIN validation; adapter failure falls back; filing correction flow; packet totals tie to the ledger.
**Verify:** `pnpm test:integration --grep "filing|withholding"`.
**Done when:** a seeded year produces 1099-K data that ties to the ledger, and a 1042-S batch is accepted by the sandbox filer.
**Commit:** `feat(FR-TAX-002,003,007,008): filings, withholding and tax adapters`

### S3.4 — Passkeys (WebAuthn) and stronger MFA

**Goal:** staff move from TOTP to phishing-resistant credentials without breaking existing logins.
**Depends on:** S0.6. **Master spec:** §20.3. **Features:** `FR-SEC-016`. **Effort:** 5 agent-days.

**Build**

1. Migration `0040_webauthn.sql` — `webauthn_credentials` (credential id, public key, sign counter, transports, AAGUID), `webauthn_challenges` (short TTL).
2. Registration + authentication using `@simplewebauthn/server` (server) and `@simplewebauthn/browser`; origin and RP ID from env; counter regression detection (cloned-authenticator alarm).
3. Staff policy: passkey required for `super_admin`/`finance` within 30 days of enrollment availability; merchants can adopt optionally; TOTP stays as fallback with a documented recovery path.
4. Step-up uses passkeys when available (better UX than TOTP for approvals).
5. Recovery codes rotate; losing all factors requires a documented, audited manual recovery by two staff.

**Tests:** registration ceremony; authentication ceremony; counter replay rejected; origin mismatch rejected; policy enforcement for staff roles; recovery path audited.
**Verify:** `pnpm test:integration --grep "webauthn" && pnpm test:e2e --grep "passkey"` (Chromium virtual authenticator).
**Done when:** a staff member enrolls a passkey, signs in with it, and a cloned-credential simulation is rejected and alerted.
**Commit:** `feat(FR-SEC-016): WebAuthn passkeys and MFA policy`

### S3.5 — Bank confirmation matching

**Goal:** every payout is confirmed by the bank file, not assumed from the processor's "paid".
**Depends on:** S1.20, S1.14. **Master spec:** §11.5. **Features:** `FR-RCN-007`. **Effort:** 5 agent-days.

**Build**

1. Migration `0041_bank_confirmations.sql` — `bank_statements`, `bank_statement_lines`, `bank_match_links` + RLS.
2. Import: MT940/CAMT.053/OFX/CSV adapters with a strict schema, per-bank profile, dedupe by bank reference.
3. Matching: payout amount + date window + beneficiary + reference; auto-match with a confidence score; manual resolution UI for the rest.
4. Status effects: a payout is `paid` only when the processor confirms **and** (policy) a bank confirmation exists or the configured grace period elapses; unmatched after N days creates an exception.
5. Reconciliation report extension: bank vs processor vs ledger three-way view.

**Tests:** MT940 parse fixtures (5 banks); duplicate import idempotent; fuzzy match thresholds; grace-period policy; three-way report ties.
**Verify:** `pnpm test:integration --grep "bank"`.
**Done when:** a month of sandbox bank statements matches 100 % of payouts, and the three-way report shows zero unexplained differences.
**Commit:** `feat(FR-RCN-007): bank confirmation matching`

### S3.6 — Audit WORM export and 7-year retention

**Goal:** prove immutability to an auditor without trusting the database.
**Depends on:** S0.9, S2.17. **Master spec:** §22, §33.3. **Features:** `FR-AUD-005`. **Effort:** 4 agent-days.

**Build**

1. Daily signed checkpoint (already in S0.9) → exported to immutable storage (S3 object lock or a WORM bucket) with the checkpoint hash, signature, and the day's chain head.
2. Monthly sealed bundle: `audit` rows for the month + Merkle root + signature, written to WORM storage, verified by a `verify` job with an independent code path.
3. 7-year retention policy enforced by the storage provider (compliance mode), not by our code.
4. Verifier CLI (`scripts/verify-audit.ts`) that takes a bundle and the public key and proves the chain — usable by an external auditor.
5. Documented recovery: restore a month from WORM and compare to the live chain.

**Tests:** Merkle root recomputation; tampered bundle detected; verification works with only the public key; restore-and-compare passes; retention mode cannot be shortened.
**Verify:** `pnpm verify:audit --bundle <path>` on a generated bundle.
**Done when:** an auditor can verify a month's bundle with the CLI and the public key alone.
**Commit:** `feat(FR-AUD-005): WORM audit export and verification CLI`

### S3.7 — Lifecycle marketing, digests and scheduled reports

**Goal:** communication scales without becoming spam, and reports arrive without anyone clicking.
**Depends on:** S2.11, S2.6. **Master spec:** §29.5, §32.1. **Features:** `FR-NTF-004`, `FR-RPT-004`, `FR-FEE-009`. **Effort:** 5 agent-days.

**Build**

1. Digest engine (`FR-NTF-004`): low-priority notifications batched per user (daily/weekly), quiet hours in the user's timezone, one-click unsubscribe per category, dedupe window.
2. Scheduled report emails (`FR-RPT-004`): per-user schedules (daily/weekly/monthly), report type, format (CSV/PDF link), signed expiring link, delivery log, failure retry.
3. Promotions/waivers (`FR-FEE-009`): promo codes and manual waivers with an expiry, scope (plan, fee type, merchant), audit, and a report of granted value; never silently changes a signed fee schedule.
4. Preference center: one page for every channel × category, with a "why am I getting this" explainer and a legal footer.

**Tests:** digest groups correctly; quiet hours respected; schedule fires in the user's timezone; waiver expiry; unsubscribe stops only that category.
**Verify:** `pnpm test:integration --grep "digest|schedule|waiver"`.
**Done when:** a user receives one digest instead of 12 emails, and a weekly report arrives with a working signed link.
**Commit:** `feat(FR-NTF-004,RPT-004,FEE-009): digests, scheduled reports and waivers`

### S3.8 — Enterprise readiness and scale

**Goal:** pass an enterprise security review and survive 10× volume without re-architecture.
**Depends on:** all Phase 3. **Master spec:** §27.6, §32.5, §33.3, §36. **Features:** *(no new FR IDs — operational and contractual)*. **Effort:** 15 agent-days.

**Build**

1. SSO (SAML 2.0 / OIDC) for staff and enterprise merchants, with SCIM-lite provisioning and role mapping; a break-glass local admin with hardware MFA.
2. Custom checkout domains per enterprise merchant (CNAME, certificate automation, domain verification, CSP per host).
3. Scale work: partition `ledger_entries`, `audit.log`, `api_request_logs` by month; read replica for reports; connection pooling review; cache layer decisions recorded in an ADR.
4. Multi-region DR: documented active-passive, quarterly failover drill, RPO/RTO verified.
5. Compliance: SOC 2 Type I readiness (control matrix, evidence collection), ISO 27001 gap assessment, DPAs, sub-processor list, security whitepaper.
6. Contractual SLA + status page + incident comms templates.

**Tests:** SSO login + role mapping; custom domain certificate issuance in staging; partition routing correctness; failover drill report.
**Verify:** `pnpm test:e2e --grep "sso" && node scripts/check-partitions.mjs`.
**Done when:** an enterprise pilot signs in through SSO on a custom domain, and the failover drill met the documented RTO.
**Commit:** `feat(S3.8): enterprise SSO, custom domains and scale readiness`

### Phase 3 gate (general availability)

- [ ] Every `FR-*` in master spec §35 is `done` — `node scripts/check-steps.mjs --strict` plus a traceability report listing FR → step → test.
- [ ] SOC 2 Type I evidence collected; pentest current (< 12 months); DR drill passed.
- [ ] Status page, SLA, support rotation and on-call schedule live.
- [ ] Pricing, contracts and the sub-processor list published.

---

## 7. Implementation recipes

Copy these patterns. If a step's code deviates, the deviation must be justified in the PR.

### 7.1 Authenticated tenant read (server component)

```ts
// src/features/invoices/queries.ts
import 'server-only';
import { withTenant } from '@/lib/db/tenant';
import { requireSession } from '@/lib/security/session';
import { assertMerchant } from '@/lib/db/assert-merchant';

export async function listInvoices(cursor?: string, limit = 20) {
  const s = await requireSession();                 // throws unauthorized() → 401 / redirect
  const m = await assertMerchant(s, s.activeMerchantId);   // throws notFound() for non-members
  return withTenant({ userId: s.userId, merchantId: m.id }, async (tx) => {
    const rows = await tx`
      select id, public_id, invoice_number, status, total, balance_due, due_date, created_at
      from public.invoices
      where merchant_id = ${m.id}
        ${cursor ? tx`and (created_at, id) < (${cursor})` : tx``}
      order by created_at desc, id desc
      limit ${limit + 1}`;
    const hasMore = rows.length > limit;
    return { rows: rows.slice(0, limit), hasMore };
  });
}
```

Never: `select *`, never a `merchant_id` taken from the URL without `assertMerchant`, never a service-role client in a page.

### 7.2 Server action (the only mutation shape)

```ts
// src/features/refunds/actions.ts
'use server';
import { action } from '@/lib/actions/action';
import { z } from 'zod';
import { requestRefund } from './service';

export const requestRefundAction = action({
  schema: z.object({
    paymentId: z.string().uuid(),
    amount: z.string().regex(/^\d+(\.\d{1,2})?$/),   // string money, never number
    reason: z.enum(['duplicate','fraudulent','requested_by_customer','product_not_received','product_defective','other']),
    detail: z.string().max(500).optional(),
  }),
  permission: 'refunds.create',
  merchantScoped: true,
  idempotent: true,
  audit: 'refund.requested',
  handler: async (input, ctx, tx) => requestRefund(tx, ctx, input),
});
```

The wrapper does: CSRF → session → Zod → permission → `assertMerchant` → `withTenant` → handler → audit → revalidate tags → typed result. **No action may bypass it.**

### 7.3 Idempotency

```sql
-- 0015_payments.sql
create table public.idempotency_keys (
  merchant_id uuid not null references public.merchants(id) on delete cascade,
  key text not null,
  scope text not null,
  request_hash bytea not null,
  response_status integer,
  response_body jsonb,
  resource_type text,
  resource_id uuid,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null,
  primary key (merchant_id, key, scope)
);
```

```ts
export async function withIdempotency<T>(tx, { merchantId, key, scope, payload }, fn) {
  const hash = sha256(canonicalJson(payload));
  const [existing] = await tx`
    select request_hash, response_body, response_status
    from public.idempotency_keys
    where merchant_id = ${merchantId} and key = ${key} and scope = ${scope}
    for update`;
  if (existing) {
    if (!buffersEqual(existing.request_hash, hash)) throw new AppError('idempotency_key_reuse', 422);
    return { replayed: true, result: existing.response_body as T };
  }
  const result = await fn();
  await tx`insert into public.idempotency_keys (...) values (...)`;
  return { replayed: false, result };
}
```

### 7.4 Outbox + worker handler

```ts
// domain transaction
await enqueue(tx, {
  topic: 'email.send',
  aggregateType: 'invoice', aggregateId: invoice.id, merchantId,
  payload: { template: 'invoice.paid', to: buyerEmail, data: { invoiceId: invoice.id } },
  dedupeKey: `email:invoice.paid:${invoice.id}`,
});

// src/lib/jobs/handlers.ts
export const handlers = {
  'email.send': async (job) => sendEmail(job.payload),          // idempotent by dedupeKey
  'webhook.deliver': async (job) => deliver(job.payload),
  'pdf.render': async (job) => renderAndStore(job.payload),
  'payout.submit': async (job) => submitPayout(job.payload),
};
```

Handler rules: idempotent, no unbounded loops, ≤ 30 s, throw on retryable failure, log with `job_id`.

### 7.5 Posting to the ledger

```ts
const txId = await postLedger(tx, {
  merchantId,
  type: 'payment_captured',
  occurredAt: payment.capturedAt,
  referenceType: 'payment',
  referenceId: payment.id,
  processor: payment.processor,
  processorRef: payment.processorPaymentId,
  description: `Capture ${payment.publicId}`,
  entries: [
    { account_code: 'PROCESSOR_CLEARING', direction: 'debit',  amount: toDbNumeric(payment.amount) },
    { account_code: `M:${merchantId}:PENDING`, direction: 'credit', amount: toDbNumeric(payment.amount) },
  ],  // sorted by account_code — required for a deterministic hash
});
```

Never write `ledger_entries` directly. Never pass JS numbers. Never post outside a transaction that also contains the business state change.

### 7.6 Money

```ts
parseMoney('1,234.56')    // 12345600n   (accepts commas)
parseMoney('0.00001')     // throws InvalidMoneyError (5 dp)
formatMoney(12345600n)    // "1,234.56"
toDbNumeric(12345600n)    // "1234.5600"
fromDbNumeric('1234.5600')// 12345600n
mulRate(10000000n, '2.9000') // 290000n  (exact, half-up at micro)
```

Rule: money enters the server as a **string**, leaves as a **string**, and is a `bigint` only in between.

### 7.7 Errors

```ts
export class AppError extends Error {
  constructor(
    public code: ErrorCode,
    public httpStatus: number,
    message?: string,
    public details?: Record<string, unknown>,
  ) { super(message ?? code); }
}
export const notFound = () => new AppError('not_found', 404);   // used for cross-tenant too
```

Mapping: `AppError` → JSON envelope (Appendix B); Zod → `validation_error` + `param`; PG `42501` → `permission_denied`; `23505` on an invoice payment → `invoice_already_paid`; anything else → `internal_error` + alert, generic message + `request_id`.

### 7.8 Audit inside the mutation

```ts
await audit(tx, {
  actorType: 'user', actorId: ctx.userId, merchantId,
  action: 'refund.requested', entityType: 'refund', entityId: refund.publicId,
  before: null, after: { amount: input.amount, status: 'pending' },
  requestId: ctx.requestId, ip: ctx.ip, userAgent: ctx.userAgent,
});
```

### 7.9 Table exposure block (every new table)

```sql
alter table public.<t> enable row level security;
alter table public.<t> force  row level security;
revoke all on public.<t> from anon, authenticated;
grant select on public.<t> to authenticated;
create policy <t>_tenant_read on public.<t> for select to authenticated
  using (private.is_merchant_member(merchant_id));
create policy <t>_staff_read on public.<t> for select to authenticated
  using (private.has_permission('<domain>.read'));
-- no insert/update/delete policies: writes are impossible for authenticated
```

Then add the table to `tests/rls/coverage.test.ts` expectations and write its isolation test.

### 7.10 Processor adapter (shape)

```ts
export class StripeProcessor implements PaymentProcessor {
  id = 'stripe' as const;
  capabilities: ProcessorCapabilities = { cardPayments: true, threeDSecure: true, manualCapture: true, /* … */ };
  async createPaymentIntent(i: CreatePaymentInput) {
    const res = await this.client.post('/v1/payment_intents', {
      // micro-USD → minor units: 1 USD = 10_000n micro = 100n cents, so cents = micro / 100n
      amount: Number(i.amount / 100n),    // ⚠️ only at the vendor boundary; assert exact divisibility first
      // if (i.amount % 100n !== 0n) throw new AppError('invalid_amount', 400) — no silent rounding
      currency: 'usd',
      capture_method: i.captureMethod === 'manual' ? 'manual' : 'automatic',
      payment_method: i.paymentMethodToken,
      confirm: true,
      metadata: { merchant_id: i.merchantId, invoice_public_id: i.invoicePublicId },
    }, { idempotencyKey: i.idempotencyKey });
    return normalize(normalizeStripeIntent(res));
  }
  async verifyWebhook(headers, rawBody) { /* constant-time HMAC */ }
}
```

Rules: vendor SDKs only inside `src/lib/processors/*`; every call carries an idempotency key; `normalize()` never returns success for an unknown status; raw payloads stored **encrypted** in `payment_attempts.raw_response_ciphertext`.

### 7.11 Inbound processor webhook route

```ts
// src/app/api/webhooks/processor/[processor]/route.ts
export const runtime = 'nodejs';

export async function POST(req: Request, { params }: { params: { processor: string } }) {
  const raw = await req.text();                       // raw body BEFORE parsing
  const adapter = registry.get(params.processor);
  let event;
  try { event = adapter.verifyWebhook(req.headers, raw); }
  catch { return new Response('invalid signature', { status: 400 }); }

  await withService('processor_webhook_intake', async (tx) => {
    const inserted = await tx`
      insert into public.processor_webhook_events (processor, event_id, event_type, payload, signature_verified, status)
      values (${params.processor}, ${event.id}, ${event.type}, ${JSON.parse(raw)}, true, 'received')
      on conflict (processor, event_id) do nothing
      returning id`;
    if (inserted.length) await enqueue(tx, { topic: 'processor.event', /* … */ });
  });

  return new Response(null, { status: 200 });         // always fast
}
```

### 7.12 Outbound webhook signature (and what merchants verify)

```ts
const t = Math.floor(Date.now() / 1000);
const v1 = createHmac('sha256', secret).update(`${t}.${rawBody}`).digest('hex');
headers.set('KDPAY-Signature', `t=${t},v1=${v1}`);
headers.set('KDPAY-Event-Id', event.publicId);
```

Consumer guidance in docs: recompute HMAC over the **raw** body, reject `|now − t| > 300`, dedupe on `KDPAY-Event-Id`.

### 7.13 Direct-to-storage upload

```ts
// 1) client asks for a URL
const { data } = await supabase.storage.from('kyc-docs')
  .createSignedUploadUrl(`${merchantId}/${applicationId}/${crypto.randomUUID()}.pdf`);
// 2) client PUTs the file directly (never through a Server Action)
// 3) client calls finalizeUpload({ path }) → magic bytes, size, sha256, scan, DB row
```

### 7.14 PDF watermark + QR

```ts
const seedHash = createHash('sha256').update(doc.publicId).digest();
drawGuilloche(page, { seed: seedHash, opacity: 0.06, inset: 18 });
const hashHex = createHash('sha256').update(canonicalJson(doc)).digest('hex');
page.drawText(`KDPAY • ${doc.publicId} • ${hashHex.slice(0, 8)}`,
  { x: 40, y: 24, size: 3.5, font, opacity: 0.5 });
drawWatermark(page, `${brand.name} · INVOICE · ${doc.publicId}`, { opacity: 0.09, angle: 32 });
// footer: Document ID + full SHA-256 of the render payload
```

### 7.15 Email send (worker only)

```ts
export async function sendEmail(p: EmailPayload) {
  if (!(await isEnabled('email_sending_enabled'))) return { skipped: true };
  if (await isSuppressed(p.to)) return { skipped: true };
  const rendered = await render(p.template, p.data, p.locale);
  const res = await transport.send({ ...p, ...rendered });
  await sqlService`insert into public.email_log (...) values (...)`;
}
```

### 7.16 Rate limit (DB-backed, works on serverless)

```ts
export async function rateLimit(bucket: string, limit: number, windowSec: number) {
  const windowStart = new Date(Math.floor(Date.now() / 1000 / windowSec) * windowSec * 1000);
  const [row] = await sqlService`
    insert into public.rate_limit_counters (bucket, window_start, counter)
    values (${bucket}, ${windowStart}, 1)
    on conflict (bucket, window_start) do update set counter = rate_limit_counters.counter + 1
    returning counter`;
  if (row!.counter > limit) throw new AppError('rate_limited', 429, undefined, { retryAfter: windowSec });
}
```

Edge rules in Cloudflare handle volumetric abuse; this handles per-user/per-key logic.

### 7.17 Feature flag

```ts
export async function isEnabled(key: FlagKey, merchantId?: string) {
  const flags = await getFlagsCached();            // 30 s in-process cache
  const global = flags.platform[key];
  if (!global?.enabled) return false;
  if (merchantId && flags.merchant[merchantId]?.[key] === false) return false;
  return true;
}
```

Mandatory kill switches: `checkout_enabled`, `payouts_enabled`, `api_enabled`, `new_onboarding_enabled`, `email_sending_enabled`, `webhooks_out_enabled`, `processor:<id>_enabled`.

### 7.18 Cache tags

```ts
// read
const profile = await unstable_cache(getPlatformProfile, ['platform-profile'], { tags: ['platform:profile'] })();
// write
revalidateTag('platform:profile');
```

Tags: `platform:profile`, `cms:page:<slug>`, `cms:blog`, `merchant:<id>:summary`. **Never** cache financial reads; authenticated responses use `Cache-Control: private, no-store`.

### 7.19 Security headers (two profiles)

```ts
// middleware.ts (Edge) — dynamic app surfaces: nonce CSP
const nonce = Buffer.from(crypto.randomUUID()).toString('base64');
const csp = `default-src 'self'; script-src 'self' 'nonce-${nonce}' 'strict-dynamic' https://challenges.cloudflare.com https://js.stripe.com; frame-src https://js.stripe.com https://challenges.cloudflare.com; connect-src 'self' https://api.stripe.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https://*.supabase.co; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`;
```

- **App/admin/checkout** (dynamic): nonce CSP as above, plus HSTS, `nosniff`, `Referrer-Policy`, `Permissions-Policy`, `COOP`.
- **Marketing** (ISR/static): a static CSP without nonce. Compensating control: the marketing origin sets **no session cookie** (`__Host-` cookie is scoped to the `app.` host), contains no user data, and renders no user-supplied HTML. Record this decision in `docs/adr/`.

### 7.20 Internal cron route

```ts
export const runtime = 'nodejs';
export const maxDuration = 60;

export async function POST(req: Request) {
  if (req.headers.get('x-cron-secret') !== env.CRON_SECRET) return new Response('forbidden', { status: 403 });
  const topic = new URL(req.url).searchParams.get('topic') ?? 'outbox';
  const result = await runWorker(topic, { maxJobs: 50, timeBudgetMs: 45_000 });
  return Response.json(result);
}
```

---

## 8. Migration map

Actual order for this build (the list in master spec §5.4 is illustrative; **this** table is authoritative for numbering). Rules: append only; never edit a pushed migration; one migration per step; RLS lives in the same file as its table.

| # | File | Step | Contents |
|---|---|---|---|
| 0001 | `extensions_and_schemas.sql` | S0.3 | schemas, extensions, default-privilege revokes |
| 0002 | `domains_and_helpers.sql` | S0.3 | `money_amount`/`currency_code` domains, `set_updated_at` |
| 0003 | `identity.sql` | S0.6 | users, sessions, devices, MFA, login attempts, step-up, rate limits |
| 0004 | `rbac.sql` | S0.7 | roles, permissions, role_permissions, user_roles, merchant_members, approval_requests |
| 0005 | `audit.sql` | S0.9 | audit schema, `audit.log`, `audit.checkpoints`, `private.audit_write` |
| 0006 | `jobs_flags.sql` | S0.10 | `private.jobs`, `private.outbox`, feature flags, metrics_events |
| 0007 | `platform_cms.sql` | S0.11 | platform_settings, cms_pages(+localizations, versions, navigation), media_assets, legal_* |
| 0008 | `merchants.sql` | S1.1 | merchants, profiles, settings, limits, volume counters, notes, countries |
| 0009 | `kyb.sql` | S1.2 | kyb_applications, kyb_documents, beneficial_owners, kyc_verifications, screening_results, compliance_flags |
| 0010 | `tax_documents.sql` | S1.3 | tax_documents, tax_filings, merchant_tax_registrations |
| 0011 | `banking.sql` | S1.4 | bank_accounts, bank_verification_attempts, bank_account_changes |
| 0012 | `ledger.sql` | S1.5 | ledger_accounts/transactions/entries/periods/adjustments, merchant_balances, `ledger_post`, triggers |
| 0013 | `billing.sql` | S1.6 | plans, fee_schedules, merchant_subscriptions, subscription_invoices, fee_charges |
| 0014 | `commerce.sql` | S1.7 | customers, consents, products, tax_rates, tax_exemptions, invoices(+lines, tax lines, events, attachments, counters), credit_memos(+lines), payment_links |
| 0015 | `payments.sql` | S1.11 | checkout_sessions, payments, payment_methods, payment_attempts, card_blocklist, fraud_rules, risk_decisions, manual_review_queue, velocity_counters, payment_retries, idempotency_keys, processor_webhook_events, `commit_payment` |
| 0016 | `webhooks.sql` | S1.12 | webhook_endpoints, webhook_events, webhook_deliveries |
| 0017 | `refunds.sql` | S1.13 | refunds, credit memo linkage, refund trigger |
| 0018 | `payouts.sql` | S1.14 | payouts, payout_items, payout_holds, reserves, reserve_movements |
| 0019 | `support_notifications.sql` | S1.18 | notifications, preferences, email_templates/log/suppressions, support_tickets/messages, canned_responses |
| 0020 | `api_keys.sql` | S1.19 | api_keys, api_request_logs, report_exports, report_schedules |
| 0021 | `reconciliation.sql` | S1.20 | settlement_reports/items, reconciliation_runs/items, statements, tax_reports |
| 0022 | `disputes.sql` | S2.1 | disputes, dispute_evidence, dispute_responses, dispute_events, reason codes, network thresholds |
| 0023 | `negative_balance.sql` | S2.2 | reserves extensions, reserve_releases, negative_balance_events, dunning_attempts, write_offs |
| 0024 | `ledger_ops.sql` | S2.3 | ledger_periods extensions, ledger_adjustment_requests, closed-period triggers |
| 0025 | `billing_scale.sql` | S2.4 | plan_entitlements, subscription_changes, dunning_events, processor_cost_reports |
| 0026 | `tax_scale.sql` | S2.5 | tax_exemptions extensions, tax_jurisdiction_rates, tax_report_runs |
| 0027 | `reports.sql` | S2.6 | materialized views (merchant/platform/fee daily) + refresh bookkeeping |
| 0029 | `cms_scale.sql` | S2.9 | blog_posts (+localizations, versions), media_variants, navigation_revisions |
| 0030 | `support_scale.sql` | S2.10 | sla_policies, ticket_events, csat_responses, ticket_links |
| 0031 | `email_scale.sql` | S2.11 | email_delivery_events, email_template_versions, marketing_contacts, suppression scopes |
| 0032 | `compliance_monitoring.sql` | S2.12 | review_schedules, monitoring_events, kyc_provider_calls, remediation_tasks |
| 0033 | `catalog_extras.sql` | S2.13 | import_jobs, import_rows, reminder_runs, catalog indexes |
| 0034 | `payment_extras.sql` | S2.14 | wallet_tokens, offline_payments, offline_payment_proofs, retry_schedules |
| 0035 | `admin_scale.sql` | S2.15 | processor_accounts, country_configs, risk_rules extensions, blocklist_entries |
| 0036 | `retention.sql` | S2.17 | retention_policies, dsar_requests, dsar_exports, activity_feed view |
| 0040 | `webauthn.sql` | S3.4 | webauthn_credentials, webauthn_challenges |
| 0041 | `bank_confirmations.sql` | S3.5 | bank_statements, bank_statement_lines, bank_match_links |
| 0042 | `partitioning.sql` | S3.8 | monthly partitions for ledger_entries, audit.log, api_request_logs + maintenance job |

Steps that need **no** migration (S0.12, S1.8, S1.15–S1.17, S1.21, S2.7, S2.8, S2.16, S2.18, S3.1–S3.3, S3.6, S3.7) are deliberate: they add code, docs or workers, not schema. The gap at 0028 exists so that Phase 2 numbering stays stable if S2.7 later needs a table (`api_simulator_runs` would take 0028). Never reuse a number.

`schema.types.ts` is regenerated after **every** migration and committed; CI fails if it drifts.

---

## 9. Test strategy and commands

| Layer | Command | Must prove |
|---|---|---|
| Unit | `pnpm test` | Money 100% branch, ledger builders, fee math, state machines, risk rules, normalizers |
| Property | included in unit | Ledger balance, refund bounds, allocation sums, money round-trip |
| Integration | `pnpm test:integration` | RPCs, triggers, constraints, idempotency, concurrency, job behaviour |
| RLS | `pnpm test:rls` | Every table × role × tenant; coverage gate |
| Contract | `pnpm test:contract` | Processor adapters, webhook payloads, API schema |
| E2E | `pnpm test:e2e` | 6 critical journeys × 3 breakpoints, EN/BN |
| A11y | in E2E | axe zero serious on critical flows |
| Perf | `pnpm test:load` (k6) | Checkout 50 rps p95 < 1.5 s; dashboard p95 < 700 ms |
| Smoke | `pnpm smoke` | Full sandbox flow on staging after deploy |
| Migration | `supabase db reset` in CI | Applies from zero, no drift |
| Plan drift | `pnpm check:steps --strict` | Every step marked `done` has its files; registry matches reality |
| Requirement traceability | `pnpm check:fr` | All 241 FRs in master spec §35 have exactly one owner step; `docs/steps.json` agrees with Appendix B |
| Docs integrity | `pnpm check:docs` | Fences, tables, anchors, step packets and `§` references are all valid (§22) |

**Plan gates:** `pnpm check:steps` (registry vs files), `pnpm check:fr` (every FR has one owner step), `pnpm check:docs` (fences, anchors, tables, §-references — §22).

**Coverage gates:** `src/lib/money` 100%, `src/lib/ledger` ≥ 95%, `src/features/payments` ≥ 90%, overall ≥ 70%. Coverage is a floor, not a goal — the scenario matrix in master spec §33.2 is the real definition.

**Test data rules:** factories in `tests/factories/*` (deterministic seeds); never real PII; never network in unit tests; fake clock injected via `now()`.

---

## 10. Deploy and promotion

### 10.1 Environments

| Env | Branch | Supabase | Processor | Email | Data |
|---|---|---|---|---|---|
| Local | any | CLI (Docker) | sandbox | console | seeded |
| Preview | PR | branch DB or shared preview | sandbox | console | anonymized seed |
| Staging | `main` | dedicated project | sandbox (+1 live if testing onboarding) | verified staging subdomain | prod-like, no real buyers |
| Production | `main` (tagged) | dedicated + PITR | live | live | real |

### 10.2 Deploy sequence

```text
1. CI green on main
2. Migrations: supabase db push --linked (staging)  → verify → production
   • migrations run BEFORE the app deploy, and must be backwards compatible (expand → migrate → contract)
3. Deploy app (Vercel) → /api/health 200 → smoke script on staging
4. Promote to production (same build artifact) → smoke → watch error rate 30 min
5. Rollback: redeploy previous build; forward-fix the migration (never a destructive down-migration)
```

### 10.3 Vercel project settings

- Node 22 runtime; regions close to Supabase (same continent) to cut DB latency.
- Env vars set per environment; `NEXT_PUBLIC_*` audited every release.
- `maxDuration`: 60 s on `/api/internal/*` and PDF/report routes; default elsewhere.
- Cron (Pro) or GitHub Actions (§2.5) hitting `/api/internal/worker` every minute.
- Domains: `www` (marketing), `app` (portal/checkout/api). `__Host-` cookie only on `app`.

### 10.4 Cloudflare

DNS + DNSSEC, proxied records, WAF managed rules + custom rules for `/api/*` and `/pay/*`, bot fight mode, Turnstile, rate limits at the edge, HSTS preload after verification.

### 10.5 Pre-launch checklist

Use master spec Appendix G verbatim. Do not launch with any unchecked security, money-correctness, or legal item.

---

## 11. Pitfalls that break real deployments

| # | Symptom | Cause | Exact fix |
|---|---|---|---|
| 1 | `prepared statement "s1" does not exist` / random 500s under load | `postgres.js` prepared statements + Supavisor transaction pooling | `prepare: false` in the client; keep `max` ≤ 3 |
| 2 | Money off by cents | driver returned `numeric` as a JS number | Assert `typeof === 'string'` in a test; add an OID 1700 parser if needed |
| 3 | RLS "does nothing" | connected as `postgres` (superuser) or table owner without `force` | App queries run as `authenticated`; `force row level security` on every table |
| 4 | SECURITY DEFINER RPC returns zero rows | owned by a non-bypass role + `force RLS` | Own ledger/RPC functions as `postgres`; test the RPC as `authenticated` |
| 5 | `permission denied for table` after adding a table | Supabase default grants absent or revoked incorrectly | Include the §7.9 exposure block in the same migration |
| 6 | Middleware crashes on deploy | `postgres` import in Edge runtime | Middleware: cookie presence only; DB checks in Node layouts/routes |
| 7 | Webhook signature always invalid | body was parsed before verification | `await req.text()` first; verify on the raw string |
| 8 | 1 MB upload errors | Server Action body limit | Never upload through actions; use signed URLs (§7.13) |
| 9 | Cron never runs / runs once a day | Vercel Hobby cron limits | Pro plan, or GitHub Actions hitting `/api/internal/worker` |
| 10 | Functions time out on PDF or export | headless browser / huge in-memory CSV | `pdf-lib` only; stream CSV; generate in a worker, store in Storage |
| 11 | 3DS redirect lands signed-out | `SameSite=Strict` cookie | `SameSite=Lax` + CSRF token (CR-04) |
| 12 | Cookie missing in production | `__Host-` requires `Secure` + `Path=/` + no `Domain` | Set exactly; on `localhost` browsers still allow it |
| 13 | CSP blocks checkout | processor frames/scripts missing from CSP | Add `js.stripe.com`, `*.airwallex.com`, `challenges.cloudflare.com` to `script-src`/`frame-src` |
| 14 | Marketing site can't be nonce-CSP'd | nonce forces dynamic rendering | Marketing uses the static CSP profile (§7.19); session cookie lives on `app.` only |
| 15 | Duplicate charges after retry | client retried without idempotency | `Idempotency-Key` + `(merchant_id,key,scope)` PK + partial unique index on invoice payments |
| 16 | Two payouts for one balance | balance read then written in separate transactions | Eligibility + insert inside one transaction with `for update` on the merchant |
| 17 | Statement totals disagree with ledger | totals computed from `payments` instead of entries | Statements are derived from `ledger_entries` only |
| 18 | Supabase project paused in staging | free tier inactivity | Paid plan for staging/prod; keep a keep-alive check |
| 19 | Emails go to spam | no SPF/DKIM/DMARC, shared subdomain | Separate subdomains, authenticate, warm up, monitor DMARC |
| 20 | `supabase db reset` fails in CI | missing Docker service or migrations out of order | Use the CI block in S0.2; migrations are strictly ordered |
| 21 | Types drift | `schema.types.ts` not regenerated | CI step: regenerate + `git diff --exit-code` |
| 22 | Test flakes on invoice totals | random numbers / `Date.now()` in tests | Factories with fixed seeds; injected clock |
| 23 | Locale strings break layout | Bangla text 30% longer | Test BN snapshots at 320 px; no `uppercase` on BN |
| 24 | "Works locally, fails on Vercel" | `APP_ENV`/URLs hardcoded | All URLs from env; `assertBootConfig()` on start |
| 25 | User randomly signed out / two session cookies fighting | supabase-js wrote its own auth cookies next to our `__Host-` session | `persistSession:false, autoRefreshToken:false` on the server client; assert only our cookies are set |
| 26 | Admin sees another tenant's numbers after switching accounts | cached RSC payload or tag reused across tenants | Cache keys include `merchant_id` + role; financial reads `no-store`; test account switching |
| 27 | A merchant "mints" a balance | a `public` ledger/payout RPC granted to `authenticated` | Keep money-moving functions in `private`, grant only `app_runtime`, call via `reset role` (§17.2) + the privilege test |
| 28 | Migrations work locally, fail on deploy | `psql` variables (`:'var'`) or env interpolation inside SQL files | Migrations contain no secrets/variables; roles are created without passwords (§17.1) |
| 29 | Sign-up succeeds but `getSession()` returns null | missing `on_auth_user_created` trigger into `public.app_users` | Add the trigger in `0003_identity.sql` and assert it in the session test (S0.6) |

---

## 12. Per-step prompt template

Paste this into the AI agent for every step. Replace the bracketed parts. The surrounding procedure — which agent, the review loop, the evidence standard and how to prove a feature works — is in [`docs/AGENT_PLAYBOOK.md`](docs/AGENT_PLAYBOOK.md).

```text
ROLE: Implementation engineer for KD PAY (PayFac platform).
SOURCE OF TRUTH: docs/MASTER_SPECIFICATION.md (v1.0.0) + spec.md (build plan).

TASK: Execute step [S1.5 — ledger core].
READ FIRST: spec.md §0, §1, §11; spec.md [S1.5]; master spec [§7, §8, §6.6]; spec.md recipes §7.5 and §7.9.
DEPENDENCIES MET: [S1.1 done, verified by `pnpm verify`].

DELIVERABLES (exact):
- supabase/migrations/[0012_ledger.sql] with RLS exposure block
- src/lib/[money/*, ledger/*]
- tests as listed in the step (property, integration, RLS)

CONSTRAINTS:
- N-01..N-12 and CR-01..CR-20 are absolute.
- No float money; no direct ledger writes; no ORM; no new tables outside the master spec.
- Every new table needs RLS + coverage test + isolation test in the same PR.

ACCEPTANCE (from the step, verbatim):
[copy the "Done when" line]

VERIFY (run and paste output):
pnpm lint && pnpm typecheck && pnpm test && pnpm test:integration && pnpm test:rls

OUTPUT FORMAT:
1) Plan (≤ 10 lines) and file list.
2) The diff.
3) Command output summary.
4) docs/PROGRESS.md entry.
5) Any deviation + reason (must be approved, not assumed).
```

---

## 13. Progress ledger and first commits

### 13.1 `docs/PROGRESS.md` template

```md
# Build Progress

## Status
- Current phase: Phase 1
- Last completed step: S1.7
- Next step: S1.8
- Blocked by: none

## Log (newest first)

### 2026-10-29 — S1.7 invoices (agent)
- Done: migrations 0014, invoice RPCs, totals trigger, editor UI
- Tests: 42 passing (integration 31, rls 11); coverage invoices 91%
- Deviations: none
- Notes: tax allocation uses largest-remainder; see ADR-004
- Next: S1.8 invoice PDF

## Open questions raised by agents
| Date | Step | Question | Status |
|---|---|---|---|
```

### 13.2 First ten commits (suggested)

```text
1  chore(S0.1): scaffold Next.js app, toolchain, env validation
2  ci(S0.2): lint/typecheck/test/migration/secrets pipeline
3  feat(S0.3): db bootstrap, schemas, domains, shared triggers
4  feat(S0.4): design tokens, ui primitives, responsive shells
5  feat(S0.5): db client, tenant transactions, pagination, numeric safety
6  feat(FR-AUTH-001..005): opaque sessions, sign-in, lockout, csrf
7  feat(FR-ADM-003): dual-scope rbac, guards, action wrapper
8  feat(FR-SEC-001,FR-TEN-001..003): rls policies + isolation harness
9  feat(FR-AUD-001..003): hash-chained audit log and checkpoints
10 feat(FR-NFR-003): outbox, worker, cron, feature flags, health
```

### 13.3 Resuming after a break

1. Read `docs/PROGRESS.md` (last 3 entries) and the "Next step" line.
2. Run the last step's Verify block. If red, fix before starting the next step.
3. Read only that step + its referenced spec sections.
4. Continue at §0.3 "PLAN".

---

## 14. Global Definition of Done

A step is done only when **all** are true:

- [ ] Implements the step's `FR-*` IDs and matches the master spec (no invented behavior, tables, or endpoints).
- [ ] `pnpm verify` green; new tests cover the new behavior (and a regression test exists for every bug fixed).
- [ ] Migration applies from zero in CI; `schema.types.ts` regenerated with no diff.
- [ ] Every new table: RLS enabled **and forced**, policies written, coverage + isolation tests added.
- [ ] Every financial mutation: idempotency + ledger (if money moves) + audit + outbox in one transaction.
- [ ] Every privileged action: permission check + step-up where required + audit event.
- [ ] UI: responsive at 320/768/1440, keyboard-accessible, EN + BN strings, loading/empty/error states.
- [ ] No secrets or PII in logs, client bundles, or `NEXT_PUBLIC_*`; no PAN anywhere.
- [ ] Performance budgets respected (queries per page, bundle size, latency).
- [ ] Docs updated: `PROGRESS.md`, this file's checkboxes, master spec §35 if behavior changed, ADR for non-obvious decisions.
- [ ] PR description states: what/why, FR IDs, test evidence, migration notes, rollback plan.
- [ ] Reviewed (human or a second agent pass with the "independent spec-compliance review" prompt from master spec Appendix H.8).

**Not done:** "it compiles", "tests pass but I deleted two", "RLS added later", "I'll add the audit in the next PR", "it works on my machine".

---

## 15. Core contracts — the shared code every step assumes

The recipes in §7 and the step text call helpers (`postLedger`, `enqueue`, `audit`, `getSession`, …) that must exist **once**, with these exact signatures, or steps will invent conflicting versions. This section is the contract. Build these files in the step that first needs them (indicated per item) and never change a public signature without an ADR + a migration-style sweep.

### 15.1 Module ownership map

| File | Built in | Owns |
|---|---|---|
| `src/lib/errors.ts` | S0.5 | `AppError`, subclasses, `mapPgError`, error codes |
| `src/lib/logger.ts` | S0.5 | pino logger, redaction, child loggers |
| `src/lib/request.ts` | S0.5 | `requestId()`, injectable `now()` clock |
| `src/lib/json.ts` | S0.5 | `canonicalJson`, `sha256Hex`, `buffersEqual` |
| `src/lib/db/client.ts` | S0.5 | `sql`, `sqlService` |
| `src/lib/db/tenant.ts` | S0.5 | `withTenant`, `withService`, `TenantContext` |
| `src/lib/db/paginate.ts` | S0.5 | `paginate` / `nextCursor` |
| `src/lib/db/assert-merchant.ts` | S0.8 | `assertMerchant` |
| `src/lib/security/session.ts` | S0.6 | `SessionContext`, `getSession`, `requireSession` |
| `src/lib/security/rbac.ts` | S0.7 | `Permission`, `requirePermission`, `can` |
| `src/lib/actions/action.ts` | S0.7 | `action`, `Ctx`, CSRF + Zod + permission pipeline |
| `src/lib/audit.ts` | S0.9 | `audit` |
| `src/lib/jobs/outbox.ts` | S0.10 | `enqueue` |
| `src/lib/jobs/worker.ts` | S0.10 | `handlers`, `runWorker`, `JobHandler` |
| `src/lib/flags.ts` | S0.10 | `isEnabled`, `getFlagsCached`, `FlagKey` |
| `src/lib/security/rate-limit.ts` | S0.10 | `rateLimit` |
| `src/lib/money/index.ts` | S1.5 | `MicroUsd` + all money functions |
| `src/lib/ledger/post.ts` | S1.5 | `postLedger`, `LedgerBuilder` |
| `src/lib/api/with-api-auth.ts` | S1.19 | `withApiAuth`, `ApiCtx` |
| `src/lib/env.ts` | S0.1 | `env`, `assertBootConfig` |

### 15.2 Errors (`src/lib/errors.ts`)

```ts
export type ErrorCode =
  | 'invalid_request' | 'validation_error' | 'authentication_required' | 'permission_denied'
  | 'not_found' | 'conflict' | 'idempotency_key_reuse' | 'business_rule_violation'
  | 'invoice_already_paid' | 'refund_exceeds_captured' | 'refund_window_expired'
  | 'insufficient_balance' | 'kyb_incomplete' | 'payouts_disabled' | 'bank_account_unverified'
  | 'card_declined' | 'three_ds_failed' | 'avs_failed' | 'risk_blocked'
  | 'rate_limited' | 'processor_unavailable' | 'limit_exceeded' | 'feature_disabled'
  | 'internal_error';

export class AppError extends Error {
  constructor(
    public readonly code: ErrorCode,
    public readonly httpStatus: number,
    message?: string,
    public readonly details?: Record<string, unknown>,
    public readonly cause?: unknown,
  ) { super(message ?? code); this.name = 'AppError'; }
}
export class ValidationError extends AppError {
  constructor(public readonly param: string, message: string, details?: Record<string, unknown>) {
    super('validation_error', 400, message, { param, ...details }); this.name = 'ValidationError';
  }
}
export class UnauthorizedError extends AppError {
  constructor() { super('authentication_required', 401); this.name = 'UnauthorizedError'; }
}
export class ForbiddenError extends AppError {
  constructor(message = 'You do not have permission to do this.') {
    super('permission_denied', 403, message); this.name = 'ForbiddenError';
  }
}
export const notFound = () => new AppError('not_found', 404);
export const conflict = (m: string) => new AppError('conflict', 409, m);
export const businessRule = (code: ErrorCode, m: string) => new AppError(code, 422, m);

/** PG error → AppError. Anything unrecognised becomes internal_error and is logged with the original. */
export function mapPgError(e: unknown): AppError {
  const err = e as { code?: string; constraint_name?: string; message?: string };
  if (e instanceof AppError) return e;
  switch (err.code) {
    case '42501': return new ForbiddenError();
    case '23505': return conflict('That record already exists.');
    case '23514': case '23503': return new ValidationError('unknown', 'Those values are not allowed.');
    case 'P0002': return notFound();
    default: return new AppError('internal_error', 500, 'Something went wrong.', undefined, e);
  }
}
```

Rules: **services and queries throw**; only the `action()` wrapper, route handlers and the API envelope turn errors into JSON. Never `throw new Error('...')` in domain code.

### 15.3 Logging and request tracing

```ts
// src/lib/logger.ts
import pino from 'pino';
export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  base: { app: 'kdpay', env: process.env.APP_ENV },
  redact: {
    paths: [
      'req.headers.authorization', 'req.headers.cookie', '*.password', '*.token', '*.secret',
      '*.pan', '*.cvv', '*.tax_id', '*.account_number', '*.authorization',
      'email', 'phone', '*.email', '*.phone', 'user.email',
    ],
    censor: '[redacted]',
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});
```

```ts
// src/lib/request.ts
import { AsyncLocalStorage } from 'node:async_hooks';
import { randomUUID } from 'node:crypto';

const als = new AsyncLocalStorage<{ requestId: string }>();

/** Wrap every request/job entry point once. Nested calls inherit the id. */
export function withRequestContext<T>(requestId: string, fn: () => Promise<T>): Promise<T> {
  return als.run({ requestId }, fn);
}
export const getRequestId = () => als.getStore()?.requestId ?? 'none';
export const newRequestId = (h?: Headers) => h?.get('x-request-id') ?? `req_${randomUUID()}`;

// Injectable clock: NEVER call Date.now() inside domain code (tests need a fake clock)
let clock: () => Date = () => new Date();
export const now = () => clock();
export const __setClock = (c: () => Date) => { clock = c; };
```

Entry points that must call `withRequestContext`: `middleware.ts` (header in, header out), each route handler, each Server Action wrapper, and the worker loop (one id per job). Everything else reads `getRequestId()`.

Rules: JSON logs only; one log line per request completion with `request_id`, `route`, `status`, `duration_ms`, `merchant_id` (never email/name/amount-of-card). No `console.log` in `src/` (ESLint `no-console`).

### 15.4 Shared string unions (single definition)

These three unions are referenced across modules; define them once in the owning file and import everywhere (never re-declare).

```ts
// src/lib/jobs/topics.ts
export type JobTopic =
  | 'email.send' | 'pdf.render' | 'webhook.deliver' | 'payout.submit'
  | 'processor.event' | 'statement.generate' | 'recon.import' | 'report.export';

// src/lib/api/scopes.ts
export type ApiScope =
  | 'account:read' | 'balance:read' | 'invoices:read' | 'invoices:write'
  | 'payment_links:read' | 'payment_links:write' | 'payments:read' | 'payments:write'
  | 'refunds:read' | 'refunds:write' | 'customers:read' | 'customers:write'
  | 'products:read' | 'products:write' | 'payouts:read' | 'payouts:write'
  | 'disputes:read' | 'disputes:write' | 'tax:read' | 'reports:read' | 'webhooks:manage';

// src/lib/ledger/types.ts — mirrors the CHECK constraint in master spec §6.6 exactly
export type LedgerTransactionType =
  | 'payment_authorized' | 'payment_captured' | 'payment_voided' | 'payment_failed'
  | 'refund_succeeded' | 'refund_reversed'
  | 'dispute_opened' | 'dispute_won' | 'dispute_lost' | 'dispute_fee' | 'dispute_accepted'
  | 'fee_charged' | 'fee_reversed'
  | 'payout_requested' | 'payout_paid' | 'payout_failed' | 'payout_returned'
  | 'reserve_hold' | 'reserve_release' | 'reserve_forfeit'
  | 'settlement_received' | 'fx_conversion' | 'fx_spread' | 'adjustment' | 'write_off'
  | 'negative_balance_offset' | 'subscription_fee' | 'tax_withholding';
```

A unit test asserts each union matches its source: `LedgerTransactionType` against the DB `CHECK` constraint text, `JobTopic` against the handler registry keys, `ApiScope` against the seeded scope list.

### 15.5 Canonical JSON and hashing

```ts
// src/lib/json.ts
import { createHash, timingSafeEqual } from 'node:crypto';
export function canonicalJson(v: unknown): string {
  if (v === null || typeof v !== 'object') return JSON.stringify(v);
  if (Array.isArray(v)) return `[${v.map(canonicalJson).join(',')}]`;
  const keys = Object.keys(v as Record<string, unknown>).sort();
  return `{${keys.map((k) => `${JSON.stringify(k)}:${canonicalJson((v as any)[k])}`).join(',')}}`;
}
export const sha256Hex = (s: string | Buffer) => createHash('sha256').update(s).digest('hex');
export const sha256Buf = (s: string | Buffer) => createHash('sha256').update(s).digest();
export const buffersEqual = (a: Buffer, b: Buffer) => a.length === b.length && timingSafeEqual(a, b);
```

`canonicalJson` is used for: ledger entry payloads, audit rows, idempotency request hashes, document hashes. It must be stable across Node versions — do not swap in `JSON.stringify` for objects.

### 15.6 Database context (`src/lib/db/tenant.ts`)

```ts
import postgres from 'postgres';           // namespace: postgres.TransactionSql
import { sql, sqlService } from './client';
import { logger } from '@/lib/logger';

export type TenantContext = {
  userId: string;
  merchantId: string;
  sessionId: string;
  requestId: string;
};

export async function withTenant<T>(
  ctx: TenantContext,
  fn: (tx: postgres.TransactionSql) => Promise<T>,
): Promise<T> {
  return sql.begin(async (tx) => {
    await tx`select set_config('request.jwt.claims', ${JSON.stringify({ sub: ctx.userId, sid: ctx.sessionId })}, true)`;
    await tx`select set_config('request.request_id', ${ctx.requestId}, true)`;
    await tx`set local role authenticated`;
    return fn(tx);
  }) as unknown as Promise<T>;
}

/** service role bypasses RLS — every call must state a reason and is logged. */
export async function withService<T>(
  reason: string,
  fn: (tx: postgres.TransactionSql) => Promise<T>,
  meta: { requestId?: string } = {},
): Promise<T> {
  logger.warn({ reason, requestId: meta.requestId ?? getRequestId() }, 'service_role transaction');
  return sqlService.begin((tx) => fn(tx)) as unknown as Promise<T>;
}
```

Two hard rules:

1. `withTenant` is the **only** way an authenticated request touches the DB. It sets the role *before* returning `tx`.
2. `withService` is only for jobs, webhooks, and migrations of legacy data. Every call has a `reason` string that shows up in logs and is grep-able in review.

### 15.7 Session (`src/lib/security/session.ts`)

```ts
export type SessionContext = {
  sessionId: string;
  userId: string;
  email: string;
  userType: 'staff' | 'merchant';
  mfaLevel: 'none' | 'totp' | 'webauthn' | 'recovery';
  /** selected merchant for this session; null for staff-only users */
  activeMerchantId: string | null;
  roles: string[];                 // role codes in the active scope
  permissions: Set<Permission>;    // resolved for the active scope
};

export async function getSession(): Promise<SessionContext>;        // throws UnauthorizedError
export async function requireSession(): Promise<SessionContext>;    // redirects to /sign-in
export async function requirePermission(...ps: Permission[]): Promise<SessionContext>; // throws ForbiddenError
export async function switchMerchant(merchantId: string): Promise<void>; // validates membership, rewrites session.active_merchant_id, audit
```

**Multi-merchant decision (was missing):** `sessions.active_merchant_id uuid` is a column on the session row (added in S0.6). A user with one membership gets it set automatically at sign-in; users with several see a switcher in the topbar (staff never "switch" — they act via explicit merchant detail routes with `merchants.read`). `switchMerchant` re-validates `merchant_members` and writes an audit event.

### 15.8 Action wrapper (`src/lib/actions/action.ts`)

```ts
export type Ctx = {
  session: SessionContext;
  merchantId: string;
  requestId: string;
  ip: string | null;
  userAgent: string | null;
};

export type ActionResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: { code: ErrorCode; message: string; param?: string } };

export function action<S extends z.ZodTypeAny, T>(opts: {
  schema: S;
  permission: Permission | ((input: z.infer<S>) => Permission);
  merchantScoped: boolean;
  idempotent?: boolean;
  audit?: string;
  stepUp?: boolean;
  handler: (input: z.infer<S>, ctx: Ctx) => Promise<T>;
}): (input: z.infer<S>) => Promise<ActionResult<T>>;
```

Order inside: `requestId` → CSRF (`Origin` + `Sec-Fetch-Site` + token) → session → Zod → permission → `assertMerchant` → optional step-up check → `withTenant` → handler → audit → `revalidateTag`. Errors are **returned**, never thrown to React (Server Actions throwing lose the message in production).

### 15.9 Audit, outbox, worker, flags, rate limit

```ts
export async function audit(tx: postgres.TransactionSql, e: {
  actorType: 'user' | 'system' | 'api_key' | 'processor' | 'buyer';
  actorId?: string | null; actorLabel?: string | null;
  merchantId?: string | null;
  action: string; entityType: string; entityId?: string | null;
  before?: unknown; after?: unknown; metadata?: Record<string, unknown>;
  requestId?: string; ip?: string | null; userAgent?: string | null;
}): Promise<void>;

export async function enqueue(tx: postgres.TransactionSql, e: {
  topic: JobTopic;                    // 'email.send' | 'pdf.render' | 'webhook.deliver' | 'payout.submit'
  aggregateType: string; aggregateId: string; merchantId?: string | null;
  payload: Record<string, unknown>; dedupeKey: string;
}): Promise<void>;

export type JobHandler = (job: { id: number; topic: JobTopic; payload: any; attempts: number }) => Promise<void>;
export const handlers: Record<JobTopic, JobHandler>;
export async function runWorker(topic: string, o: { maxJobs: number; timeBudgetMs: number }):
  Promise<{ processed: number; failed: number; dead: number }>;

export async function getFlagsCached(): Promise<{
  platform: Record<string, { enabled: boolean; rolloutPercent: number; allowedMerchantIds: string[] }>;
  merchant: Record<string, Record<string, boolean>>;
}>;
export async function isEnabled(key: FlagKey, merchantId?: string | null): Promise<boolean>;

export async function rateLimit(bucket: string, limit: number, windowSec: number):
  Promise<{ remaining: number; resetAt: Date }>;   // throws AppError('rate_limited', 429)
```

### 15.10 Ledger boundary (`src/lib/ledger/post.ts`)

```ts
export type LedgerEntry = { account_code: string; direction: 'debit' | 'credit'; amount: string };

export type LedgerBuilder = {
  merchantId: string;
  type: LedgerTransactionType;        // master spec §6.6 enum
  occurredAt: Date;
  referenceType: 'payment' | 'refund' | 'dispute' | 'payout' | 'reserve' | 'adjustment' | 'settlement' | 'subscription';
  referenceId: string;
  processor?: string | null;
  processorRef?: string | null;
  description: string;
  entries: LedgerEntry[];             // MUST be sorted by account_code, then direction
  metadata?: Record<string, unknown>;
};

/**
 * Validates locally (BigInt balance), then calls private.ledger_post.
 * Implementation detail (§17.2): `reset role` → call → `set local role authenticated`.
 * Never writes ledger tables directly, and the function is never exposed to an API role.
 */
export async function postLedger(tx: postgres.TransactionSql, b: LedgerBuilder): Promise<string>;
```

### 15.11 API auth (`src/lib/api/with-api-auth.ts`)

```ts
export type ApiCtx = { merchantId: string; apiKeyId: string; scopes: Set<ApiScope>; livemode: boolean; requestId: string };
export function withApiAuth(scopes: ApiScope[], h: (req: Request, ctx: ApiCtx) => Promise<Response>): (req: Request) => Promise<Response>;
```

Behavior: `Authorization: Bearer sk_live_…` → hash → active key → scope check → rate limit → attach `request_id` → JSON errors in the Appendix B envelope → `api_request_logs` row.

### 15.12 Environment (`src/lib/env.ts`)

```ts
export const env = /* zod-parsed, typed, frozen */;
export function assertBootConfig(): void;  // called from instrumentation.ts; fails fast with a list of missing/invalid keys
```

Rules: no `process.env` outside this file (ESLint `no-process-env` with an allowlist). `assertBootConfig` runs at boot so a missing key fails the deploy, not a customer's payment.

### 15.13 Function index (everything else the steps call)

Money functions are **normatively defined** in master spec §7.2 (`parseMoney`, `formatMoney`, `toDbNumeric`, `fromDbNumeric`, `mulRate`, `splitProportionally`, `assertBalanced`). The remaining app-owned helpers:

| Signature | File | Built in |
|---|---|---|
| `assertMerchant(session, merchantId): Promise<Merchant>` — throws `notFound()` for non-members | `src/lib/db/assert-merchant.ts` | S0.8 |
| `paginate<T>(tx, q, { cursor, limit }): Promise<{ rows: T[]; nextCursor: string \| null; hasMore: boolean }>` | `src/lib/db/paginate.ts` | S0.5 |
| `createUploadUrl(input): Promise<{ signedUrl: string; path: string; expiresAt: Date }>` | `src/lib/storage/upload.ts` | S1.2 |
| `finalizeUpload(tx, input): Promise<StoredFile>` — magic bytes, size, sha256, scan, DB row | `src/lib/storage/upload.ts` | S1.2 |
| `signedDownloadUrl(bucket, path, ttlSec): Promise<string>` — permission-checked first | `src/lib/storage/download.ts` | S1.2 |
| `encryptField(plain, aad): string` / `decryptField(cipher, aad): string` | `src/lib/security/crypto.ts` | S1.3 |
| `screenSubject(input): Promise<ScreeningResult>` | `src/lib/compliance/screening.ts` | S1.3 |
| `computeFees(input): FeeBreakdown` / `resolveSchedule(merchant, plan, at)` | `src/features/fees/engine.ts` | S1.6 |
| `renderInvoicePdf(doc): Promise<Uint8Array>` | `src/lib/pdf/invoice.ts` | S1.8 |
| `drawGuilloche(page, opts)` / `drawWatermark(page, text, opts)` | `src/lib/pdf/guilloche.ts` | S1.8 |
| `renderStatementPdf(doc): Promise<Uint8Array>` | `src/features/statements/pdf.ts` | S1.20 |
| `deliverWebhook(deliveryId): Promise<DeliveryResult>` | `src/lib/webhooks/deliver.ts` | S1.12 |
| `verifyKdpaySignature(rawBody, header, secret): boolean` | `src/lib/webhooks/sign.ts` | S1.12 |
| `requiresPublicUrl(url): Promise<URL>` (SSRF guard) | `src/lib/webhooks/ssrf.ts` | S1.12 |
| `submitPayout(payoutId): Promise<PayoutResult>` | `src/features/payouts/submit.ts` | S1.14 |
| `buildPayoutBatch(merchantId, at): Promise<PayoutDraft[]>` | `src/features/payouts/schedule.ts` | S1.14 |
| `commitPayment(checkoutSessionId, processorRef): Promise<Payment>` | `src/features/payments/service.ts` | S1.11 |
| `decideRisk(input): Promise<RiskDecision>` | `src/features/risk/decide.ts` | S1.11 |
| `requestRefund(ctx, input): Promise<Refund>` / `approveRefund(ctx, id)` | `src/features/refunds/service.ts` | S1.13 |
| `renderTemplate(key, data, locale): Promise<{ subject; html; text }>` | `src/lib/email/render.tsx` | S1.18 |
| `sendEmail(payload): Promise<{ skipped?: boolean; id?: string }>` | `src/lib/email/transport.ts` | S1.18 |
| `isSuppressed(email): Promise<boolean>` | `src/lib/email/suppression.ts` | S1.18 |
| `runReconciliation(day, opts): Promise<ReconSummary>` | `src/features/reconciliation/match.ts` | S1.20 |
| `verifyLedgerChain(range): Promise<ChainReport>` | `src/lib/ledger/verify.ts` | S1.5 |

Rules: each helper has exactly one implementation, one owner step, and unit tests in the same PR. If a step needs a helper that is not here and not in master spec §7.2, add it to this table **first**, then implement it.

### 15.14 Contract-change protocol

If a step genuinely needs a different signature: (1) write `docs/adr/NNN-<slug>.md` with the reason, (2) update this section **in the same PR**, (3) update every call site, (4) note it in `docs/PROGRESS.md`. Silent drift is a defect.

---

## 16. Test infrastructure

Agents fail here more than anywhere else. This section makes tests deterministic and cheap.

### 16.1 Vitest projects (`vitest.config.ts`)

```ts
import { defineConfig } from 'vitest/config';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    projects: [
      { test: { name: 'unit', include: ['src/**/*.test.ts'], exclude: ['**/*.int.test.ts'], environment: 'node' } },
      { test: { name: 'integration', include: ['tests/integration/**/*.test.ts'], environment: 'node',
                pool: 'forks', poolOptions: { forks: { singleFork: true } }, testTimeout: 30_000, setupFiles: ['tests/setup/db.ts'] } },
      { test: { name: 'rls', include: ['tests/rls/**/*.test.ts'], environment: 'node',
                pool: 'forks', poolOptions: { forks: { singleFork: true } }, testTimeout: 30_000, setupFiles: ['tests/setup/db.ts'] } },
    ],
    coverage: { provider: 'v8', reporter: ['text', 'lcov'], thresholds: { 'src/lib/money/**': 100, 'src/lib/ledger/**': 95 } },
  },
});
```

### 16.2 Database isolation

- `tests/setup/db.ts` loads `.env.test`, asserts `DATABASE_URL` points at **localhost** (guard: throw if the host is not `127.0.0.1`/`localhost`), and fails the whole run otherwise. This single guard prevents an agent from wiping a hosted project.
- Integration and RLS suites run **serially** (`singleFork`) — Postgres state is shared.
- Each test file seeds exactly what it needs via factories, then truncates with a helper that preserves migrations:

```ts
// tests/setup/truncate.ts
export async function truncateAll() {
  const rows = await sqlService<{ tablename: string }[]>`
    select tablename from pg_tables
    where schemaname = 'public'
      and tablename not in ('schema_migrations')`;
  if (!rows.length) return;
  await sqlService.unsafe(
    `truncate ${rows.map((r) => `public."${r.tablename}"`).join(', ')} restart identity cascade`,
  );
  await sqlService.unsafe(`truncate audit.log restart identity`);   // staff-only table, service role can
}
```

- Never `begin`/`rollback` around RLS tests: `set local role` inside an open transaction that also holds fixtures is easy to get wrong. Truncate + serial is slower but correct.
- Factories: `tests/factories/{merchant,user,invoice,payment,payout}.ts` — fixed seeds (`faker.seed(42)`), no real PII, one call returns a fully valid entity graph.

### 16.3 Auth users for tests and dev

`auth.users` cannot be safely seeded with raw SQL. Use the admin API:

```ts
// tests/setup/auth.ts + scripts/seed-users.ts (same helper)
export async function createTestUser(email: string, password = 'devpassword123!', type: 'staff' | 'merchant' = 'merchant') {
  const { data, error } = await supabaseService.auth.admin.createUser({
    email, password, email_confirm: true, user_metadata: { user_type: type },
  });
  if (error) throw error;
  return data.user;     // the on_auth_user_created trigger creates public.app_users
}
```

Seed order: users → merchants → memberships → RBAC → domain data. `pnpm db:seed` runs `supabase/seed/*.sql` after `db reset`; the user/merchant graph is created by `scripts/seed-dev.ts` (node + service role) because it needs the Auth API.

### 16.4 Playwright

```ts
// playwright.config.ts (essentials)
export default defineConfig({
  testDir: 'tests/e2e',
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'], baseURL: process.env.E2E_BASE_URL } },
    { name: 'mobile',  use: { ...devices['iPhone 13'],    baseURL: process.env.E2E_BASE_URL } },
  ],
  webServer: { command: 'pnpm dev', url: 'http://localhost:3000', reuseExistingServer: !process.env.CI },
});
```

- `tests/e2e/auth.setup.ts` signs in through the real form and saves `storageState` per role (`owner`, `finance`, `staff`, `superadmin`) into `tests/.auth/*.json` (git-ignored).
- Every authenticated spec starts with `test.use({ storageState: 'tests/.auth/owner.json' })`.
- Deterministic data: each spec calls an API/fixture endpoint (or a seed script) with a unique suffix; never rely on data from another spec.
- Screenshots on failure; `trace: 'retain-on-failure'`; no arbitrary `waitForTimeout` (ESLint rule on `tests/e2e`).

### 16.5 Clock, network, and randomness

- Domain code calls `now()` from `src/lib/request.ts`; tests call `__setClock(...)`.
- No outbound network in unit/integration: processor adapters are injected (`PROCESSOR=sandbox`); email transport is `console`; Turnstile is the always-pass test key.
- IDs: public IDs come from `nanoid`; tests assert **shape** (`/^inv_/`) not exact values. Where a deterministic value is required, pass an injectable ID generator.

### 16.6 What every test suite must prove (minimum)

| Suite | Non-negotiable assertions |
|---|---|
| money | 100% branch; property tests for parse/format round-trip and allocation sums |
| ledger | builders balance; immutability; chain verifies; concurrency (50 parallel posts) |
| rls | every table × {own, other, staff, anon}; coverage gate (no table without RLS) |
| actions | CSRF, permission, tenant 404, validation, idempotency replay |
| payments | two buyers one invoice → one success; duplicate webhook → one payment |
| payouts | eligibility matrix; concurrent payouts never exceed available |
| webhooks | signature, dedupe, retry schedule, SSRF |
| pdf | text snapshot, watermark on every page, QR target, hash stability |

---

## 17. Database roles and connection security

**The single most dangerous misconfiguration in this stack is connecting the app as `postgres`:** it is a superuser, which silently bypasses every RLS policy and makes the isolation tests pass while production leaks. This section prevents that.

### 17.1 Roles

| Role | Used by | Privileges |
|---|---|---|
| `postgres` | migrations only (`supabase db push`, `db reset`) | superuser. **Never** in `DATABASE_URL` for the app |
| `app_runtime` | Next.js (`DATABASE_URL`) | `login`, member of `authenticated`, no `bypassrls`, no DDL |
| `app_service` | workers/cron (`DATABASE_URL_SERVICE`) | `login`, member of `service_role` (bypasses RLS by design) |
| `authenticated` | assumed inside `withTenant` via `set local role` | table `select` only; RPC execute |
| `anon` | public pages before sign-in | `select` on published CMS rows only |

```sql
-- 0002b_app_roles.sql — roles only. NO passwords in migrations.
do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'app_runtime') then
    create role app_runtime login noinherit;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'app_service') then
    create role app_service login noinherit;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'service_role') then
    create role service_role nologin bypassrls;      -- Supabase defines this; plain PG needs it
  end if;
end $$;

grant authenticated to app_runtime;
grant service_role   to app_service;
```

**Passwords are set once, outside migrations**, because migrations are committed to git:

```bash
# local
psql "$DATABASE_URL_DIRECT" -c "alter role app_runtime password 'local-dev-only';"
psql "$DATABASE_URL_DIRECT" -c "alter role app_service password 'local-dev-only';"
# staging/production: set in the Supabase dashboard (SQL editor) or CI secret step, never in a file
```

Local/dev may use the `postgres` superuser for convenience, but `APP_ENV=production` **must** use `app_runtime`/`app_service` (enforced in `env.ts`, §17.3).

Grants for the RLS helpers belong in the migration that **creates** them (`0004_rbac.sql`), immediately after the function definitions:

```sql
grant usage on schema private to authenticated;
grant execute on function private.current_uid()                    to authenticated;
grant execute on function private.is_staff()                       to authenticated;
grant execute on function private.has_permission(text)             to authenticated;
grant execute on function private.is_merchant_member(uuid)         to authenticated;
grant execute on function private.merchant_permission(uuid, text)  to authenticated;
-- no table privileges in `private` → policies can call helpers, data stays sealed
```

In Supabase, `private` is not in the exposed schemas (`db-schemas = public`), so granting `USAGE` does not expose it over the API.

### 17.2 Ledger and audit functions must NOT be callable through the API

**This is a money-minting hazard.** If you expose `public.rpc_ledger_post(...)` and grant it to `authenticated`, any holder of a PostgREST JWT could post a balanced entry and invent a balance. The correct design: the ledger function is reachable **only by the server process**, never by an API role.

```sql
-- private.ledger_post is security definer, owned by postgres (bypasses RLS internally)
revoke all on function private.ledger_post(uuid,text,timestamptz,text,uuid,text,text,text,jsonb,jsonb) from public, anon, authenticated;
grant execute on function private.ledger_post(uuid,text,timestamptz,text,uuid,text,text,text,jsonb,jsonb) to app_runtime;   -- server only
grant usage on schema private to app_runtime;                                                                             -- needed to resolve it
```

The app calls it by temporarily dropping back to the session role inside the same transaction:

```ts
// src/lib/ledger/post.ts (core of postLedger)
await tx`reset role`;                       // authenticated → app_runtime (session user)
const [{ id }] = await tx`select private.ledger_post(
  ${b.merchantId}, ${b.type}, ${b.occurredAt}, ${b.referenceType}, ${b.referenceId},
  ${b.processor ?? null}, ${b.processorRef ?? null}, ${b.description},
  ${tx.json(b.metadata ?? {})}, ${tx.json(b.entries)}) as id`;
await tx`set local role authenticated`;     // restore the tenant scope immediately
```

`app_runtime` is a login role used **only** by our Next.js server (it is not a PostgREST role), so no browser can reach `private.ledger_post`. The same `reset role` / call / `set local role` pattern applies to `private.audit_write`, `private.enqueue`, and any other `security definer` helper the app must invoke.

This is how every write-side command in master spec §6.14 is built: the SQL function lives in `private`, the typed wrapper lives in `src/features/*`, and the Server Action/route calls the wrapper inside `withTenant`. No `public.rpc_*` functions exist.

Rule: **nothing that can create money, change balances, or write the audit chain is granted to `anon` or `authenticated`.** A test asserts this:

```ts
it('no API role can execute money-moving functions', async () => {
  const rows = await sql`
    select p.proname, r.rolname
    from pg_proc p
    join pg_namespace n on n.oid = p.pronamespace
    cross join (values ('anon'), ('authenticated')) as r(rolname)
    where n.nspname = 'public'
      and p.proname ~ '(ledger|audit|balance|payout_execute)'
      and has_function_privilege(r.rolname, p.oid, 'execute')`;
  expect(rows).toEqual([]);
});
```

### 17.3 Proof test (must exist before Phase 1)

```ts
it('the app connection cannot bypass RLS', async () => {
  const [{ current_user }] = await sql`select current_user`;
  expect(current_user).toBe('app_runtime');
  const [{ rolsuper, rolbypassrls }] = await sql`
    select rolsuper, rolbypassrls from pg_roles where rolname = current_user`;
  expect(rolsuper).toBe(false);
  expect(rolbypassrls).toBe(false);
});
```

`.env.example` documents `app_runtime` / `app_service`; `env.ts` rejects a `DATABASE_URL` whose user is `postgres` when `APP_ENV=production`.

---

## 18. UI stack decisions (stop agents from mixing libraries)

| Concern | Decision | Rationale |
|---|---|---|
| Data fetching | **RSC queries + Server Actions** only in Phase 1. No React Query/SWR. | Fewer round-trips, less client JS, no cache-invalidation bugs |
| Client mutations | Server Action → `ActionResult` → `toast` + `router.refresh()` (or `revalidateTag`) | One code path; typed errors |
| Complex forms | `react-hook-form` + `@hookform/resolvers/zod` **only** for the invoice editor and onboarding wizard | Those exceed `useActionState` ergonomics |
| Simple forms | `useActionState` + our `action()` wrapper | Less code |
| Validation | One Zod schema per domain in `features/<domain>/schema.ts`, shared by server and client | No duplicate rules |
| Icons | `lucide-react` | shadcn default, tree-shakeable |
| Charts | `recharts` via shadcn chart wrapper, **dynamically imported**, max 2 series | Keeps dashboard bundle within budget |
| Toasts | `sonner` | Already in the primitive set |
| Dates | `date-fns` + `date-fns-tz` for display only; DB is UTC | Predictable formatting |
| Tables | our `data-table` primitive (server pagination) | One a11y/behavior contract |
| Styling | Tailwind + CSS variables from master spec §31.2; `clsx` + `tailwind-merge` | Token discipline |
| Animation | CSS transitions only; no animation library | Bundle + reduced-motion |
| State | React state + URL search params for filters; no global store | Refresh-safe links |
| i18n | `next-intl`; keys `"<domain>.<screen>.<element>"`, e.g. `invoices.list.emptyTitle` | Greppable, no collisions |
| Icons in PDFs | none (vector only) | Deterministic rendering |

**Dependency rule:** every new runtime dependency needs a one-line justification in the PR and a license check (MIT/Apache/BSD only). No new dependency for something the platform already does.

### 18.1 i18n contract

- `src/messages/en.json` and `bn.json` are the only user-facing string sources; a test asserts the **key sets are identical**.
- Never concatenate translated fragments; use ICU messages with params (`{count, plural, ...}`).
- Brand names, currency codes and legal entity names are interpolated, never translated.
- Errors shown to users come from a key (`errors.<code>`), not from the raw `AppError.message` — except API responses, which use the documented English message.

---

## 19. Step registry and machine-readable tracking

`docs/steps.json` is the **machine-readable** mirror of §3–§6A: **60 steps** (13 phase 0, 21 phase 1, 18 phase 2, 8 phase 3), and for each step the FR IDs it owns. Agents and CI read it; humans read this file.

```jsonc
{
  "version": 1,
  "steps": [
    {
      "id": "S0.6",
      "phase": 0,
      "title": "Authentication with opaque server-side sessions",
      "depends_on": ["S0.5"],
      "fr": ["FR-AUTH-001", "FR-AUTH-002", "FR-AUTH-003", "FR-AUTH-004", "FR-AUTH-005",
             "FR-AUTH-006", "FR-AUTH-007", "FR-SEC-004", "FR-SEC-010", "FR-SEC-011"],
      "files": ["supabase/migrations/0003_identity.sql", "src/lib/security/session.ts", "src/app/(auth)/sign-in/page.tsx"],
      "verify": "pnpm test:integration --grep auth && pnpm test:e2e --grep sign-in",
      "done_when": "Revoked session rejected on the next request; HIBP rejects a known-breached password.",
      "status": "pending"
    }
  ]
}
```

Rules:

- `status` ∈ `pending | in_progress | blocked | done`. Only a human or the session that finished the step sets `done`, and only after the verify command passed.
- `files` lists the **existence checks** for the step (not every file). `node scripts/check-steps.mjs` prints a table and exits non-zero if a step marked `done` is missing files.
- CI runs `node scripts/check-steps.mjs --strict` so the registry cannot drift from reality.
- `fr` is the FR list the step owns (Appendix B). `node scripts/check-fr-coverage.mjs` fails if the registry and the master spec disagree.
- When a step is finished, append the evidence to `docs/PROGRESS.md` (verify output, PR link, date) — the registry says *what*, PROGRESS says *proved when*.
- If a step is split, add `S1.5a`, `S1.5b` with explicit `depends_on`; never renumber existing steps.

### 19.1 Checker script

The real, dependency-free implementation lives at **`scripts/check-steps.mjs`** (create it in S0.1, then never edit it unless you also update this section). It prints one row per step (`done`, `ready`, `pending`, `BROKEN`), accepts an optional step id (`node scripts/check-steps.mjs S1.5`), and `--strict` exits 1 when a step marked `done` is missing any of its `files` — the only failure that matters, because it means the registry is lying.

Contract (both files must keep it):

- reads `docs/steps.json` relative to the repository root;
- never writes anything;
- exit 0 = report only; exit 1 = `--strict` and at least one `BROKEN` step;
- no network, no dependencies, runs on Node 20+.

### 19.2 Requirement coverage script

`scripts/check-fr-coverage.mjs` enforces traceability in both directions:

1. reads every `FR-*` row of master spec §35 (241 IDs);
2. reads Appendix B's reverse table (FR → owner step);
3. reads `docs/steps.json` `features`;
4. fails if any FR is unowned, owned twice, owned by a step that does not exist, or missing from the registry entry that claims it.

CI runs `pnpm check:fr` on every PR. **The rule this enforces:** no requirement can be added to the master spec without an owner step, and no step can be marked `done` while it owns a requirement that is not implemented and tested.

---

## 20. Definition of Ready, rollback and change control

### 20.1 Definition of Ready (before starting a step)

- [ ] All `depends_on` steps are `done` in `docs/steps.json`.
- [ ] The verify command of the previous step passes on the current branch.
- [ ] The step's master-spec sections are read and any ambiguity is resolved (§0.6) **before** writing code.
- [ ] `docs/PROGRESS.md` says this is the next step.

If any box is unchecked, do the prerequisite instead. Starting "just the UI" of a later step is how phase order breaks.

### 20.2 Rollback policy per change type

| Change | Rollback |
|---|---|
| Code only | Revert the commit / redeploy the previous Vercel build |
| Additive migration (new table/column) | Leave it; drop in a later migration once no code references it |
| Destructive migration (drop/rename) | **Never** in one deploy: expand → migrate code → contract in a later release |
| Feature misbehaving in prod | Flip the feature flag/kill switch first, then fix |
| Ledger bug | Freeze payouts (`payouts_enabled=false`), snapshot, post a **reversing transaction**, never edit rows |
| Audit bug | Do not delete rows; add a corrective audit event and a checkpoint note |

Every PR states its rollback in one line.

### 20.3 Change control for this plan and the master spec

- A step may not change a rule; it can only implement it.
- If implementation reveals a rule is wrong: open `docs/OPEN_QUESTIONS.md`, propose the amendment, wait for a decision, then update master spec + this file + `docs/steps.json` in one PR.
- Versioning: this plan and the master spec are versioned together (major = scope change, minor = new step/section, patch = clarification).
- `docs/adr/NNN-<slug>.md` for any decision an agent makes that a reviewer could reasonably question (≥ 8 lines: context, decision, consequences).

---

## 21. Context management for agents (how to work without losing the plot)

1. **Never load the whole master spec.** Read only the sections named in the step (typically 100–400 lines).
2. **Write files in chunks.** For a file > 200 lines, create the skeleton, then fill sections; re-read before editing to avoid duplicating an import block.
3. **One step per session.** If a step is > 800 changed lines, stop at a coherent commit and record the remainder in `PROGRESS.md` as `S1.5 (part 2)`.
4. **Re-read before you rewrite.** Before editing an existing file, read it in full; do not assume its current contents from memory.
5. **No speculative dependencies.** If a helper does not exist in §15, write it in the step that owns it and register it there.
6. **Verify, don't claim.** Every "done" must be backed by pasted command output; "should work" is not evidence.
7. **Keep the diff reviewable.** If you touch > 20 files, justify it in the PR body.
8. **Stop at ambiguity, not at difficulty.** Difficulty is expected; ambiguity is a question for the human (§0.6).

---

## 22. Documentation quality gates (the plan is code)

The specification is the input to every agent session. If it drifts, an agent confidently builds the wrong thing. Three dependency-free scripts keep it honest; all three run in CI and must be green before any docs PR merges.

| Script | Command | Fails when |
|---|---|---|
| `scripts/check-docs.mjs` | `pnpm check:docs` | Unbalanced code fences, ragged table columns, dead internal anchors, a step missing any of Goal / Depends on / Features / Verify / Done when / Commit, a step in `spec.md` missing from `docs/steps.json` (or vice versa), or a `§` reference that points at a section that does not exist |
| `scripts/check-steps.mjs` | `pnpm check:steps --strict` | A step marked `done` is missing one of its `files` |
| `scripts/check-fr-coverage.mjs` | `pnpm check:fr` | A requirement in master spec §35 is unowned, owned twice, owned by a step that does not exist, or missing from the registry entry that claims it |

### 22.1 When you change the docs

1. Run all three scripts. A red `check:fr` after adding a feature means you forgot an owner step; a red `check:docs` means a reference or a table is broken.
2. If you add an FR to the master spec, you **must** add it to exactly one step's `**Features:**` line, to Appendix B, and to `docs/steps.json` `features`. Three places, one meaning.
3. If you add a step, add the packet (§5 format), the registry row, and its FRs. Renumbering is forbidden — append `S1.5b` instead.
4. If you change a contract (a signature in §15), update §15 **and** every step that calls it in the same PR (§15.14).

### 22.2 The rules the checkers cannot enforce (a human must)

- A step's **Verify** command must actually exist in `package.json` scripts and actually fail when the feature is broken. A step whose verify is `true` is not done.
- **Done when** must be observable from outside the code (a DB row, a PDF, an email, a ledger balance), never "code written".
- **Tests** must name the specific assertion that would catch a regression, not "unit tests".
- Estimates are not promises; the gate and the Definition of Done are.

### 22.3 Documentation change control

| Change | Needs |
|---|---|
| Typo, wording, table formatting | A direct commit (run the three scripts) |
| New/renamed step, FR ownership change | PR + `check:fr` green + a line in `docs/PROGRESS.md` |
| Schema, ledger, security, or contract change | ADR (§20.3) + master spec update + plan update in the same PR |
| Phase reorder | Written approval in `docs/OPEN_QUESTIONS.md` — this invalidates estimates |

---

## Appendix A — Agent readiness self-audit

Every item an AI agent needs to build this platform without guessing, and where it is answered.

| # | What the agent needs | Where | Status |
|---|---|---|---|
| 1 | What to build and in what order | §3–§6A (60 steps), `docs/steps.json` | ✅ |
| 2 | What is *correct* (rules, schema, ledger, RBAC) | master spec (referenced per step) | ✅ |
| 3 | Exact files per step | each step's **Build** + `docs/steps.json.files` | ✅ |
| 4 | Commands to verify | each step's **Verify**, §9, `pnpm verify` | ✅ |
| 5 | Definition of Done / Ready | §14, §20.1 | ✅ |
| 6 | Shared types and helper signatures | **§15** (new) | ✅ |
| 7 | Error taxonomy and HTTP mapping | §15.2 + master spec Appendix B | ✅ |
| 8 | Logging, request IDs, clock injection, canonical JSON | **§15.3, §15.5** (new) | ✅ |
| 9 | Session/tenant context incl. multi-merchant | **§15.6–§15.7** (new) | ✅ |
| 10 | DB role model that keeps RLS honest | **§17** (new) | ✅ |
| 11 | Test infra: isolation, seeding, auth state, clock | **§16** (new) | ✅ |
| 12 | UI library decisions (no library mixing) | **§18** (new) | ✅ |
| 13 | i18n key convention | **§18.1** (new) | ✅ |
| 14 | Migration numbering authority | §8 + master spec §5.4 note | ✅ |
| 15 | Where migrations/RLS/audit/idempotency go | §1.1, §7.5, §7.8, §7.9, §15.9 | ✅ |
| 16 | Copy-paste implementations of every pattern | §7.1–§7.20 | ✅ |
| 17 | What breaks in production and the fix | §11 (29 items) | ✅ |
| 18 | Environment variables and platform limits | §2.3, §2.5, master spec Appendix A | ✅ |
| 19 | Deploy/promotion/rollback | §10, §20.2 | ✅ |
| 20 | How to ask for help correctly | §0.6, `docs/OPEN_QUESTIONS.md` | ✅ |
| 21 | Progress tracking across sessions | §13, `docs/PROGRESS.md`, §19 | ✅ |
| 22 | Hard prohibitions | §0.7, §14, master spec §0.4 | ✅ |
| 23 | Realistic effort/timeline | per-step effort + dependency graph in `docs/steps.json` | ✅ (estimates) |
| 24 | **Every feature has an owner step — nothing silently dropped** | **Appendix B** + `pnpm check:fr` (241/241 FRs owned) | ✅ |
| 25 | Phase 2 and Phase 3 at the same rigor as Phase 1 | **§6 (S2.1–S2.18), §6A (S3.1–S3.8)** (new) | ✅ |
| 26 | Security headers, CSP, edge controls, no-security-theater rule | **S0.12** (new) | ✅ |
| 27 | Backups, PITR, restore drill, runbooks, incident response | **S0.13** (new) | ✅ |
| 28 | Machine-checkable traceability (FR → step → test) | Appendix B, §19.2, `scripts/check-fr-coverage.mjs` | ✅ |
| 29 | Lettered/renumbered cross-references that still resolve | §22 (`check-docs.mjs`) | ✅ |
| 30 | Every route, its permission and its cache policy | **Appendix C** (new) | ✅ |

**Known non-goals of this plan** (deliberately not answered here): exact vendor pricing and contract terms (business), legal text (counsel), production credentials, and the final visual design beyond the token/component system. Those are inputs, not engineering decisions.

---

## Appendix B — Requirement ownership map

Every requirement in master spec §35 (241 FR IDs) has **exactly one** owner step. Nothing is unowned, nothing is owned twice. Use this table two ways:

- Starting a step? The **Features** row is the checklist you must deliver, and it matches the `**Features:**` line in the step packet.
- Asked "is FR-X done?"? Find it: `grep -n "FR-PYT-004" spec.md` → the step, then check that step in `docs/steps.json`.

A CI check (`scripts/check-fr-coverage.mjs`, §9) re-derives this table from master spec §35 and fails if any FR is unowned, double-owned, or missing from the step it claims.

| Step | Phase | Owner of | Count |
|---|---|---|---|
| **S0.2** | P0 | `FR-NFR-005`, `FR-NFR-006`, `FR-SEC-014` | 3 |
| **S0.4** | P0 | `FR-UX-001..003`, `FR-UX-010` | 4 |
| **S0.5** | P0 | `FR-TEN-004`, `FR-SEC-009` | 2 |
| **S0.6** | P0 | `FR-AUTH-001..007`, `FR-SEC-004`, `FR-SEC-010`, `FR-SEC-011` | 10 |
| **S0.7** | P0 | `FR-SEC-003` | 1 |
| **S0.8** | P0 | `FR-TEN-001`, `FR-TEN-002`, `FR-SEC-001` | 3 |
| **S0.9** | P0 | `FR-AUD-001..003` | 3 |
| **S0.10** | P0 | `FR-TEN-005`, `FR-SEC-005` | 2 |
| **S0.11** | P0 | `FR-CMS-008`, `FR-NFR-002` | 2 |
| **S0.12** | P0 | `FR-SEC-002`, `FR-SEC-012`, `FR-SEC-013`, `FR-SEC-020` | 4 |
| **S0.13** | P0 | `FR-NFR-003`, `FR-NFR-004`, `FR-NFR-007`, `FR-SEC-019` | 4 |
| **S1.1** | P1 | `FR-MER-001` | 1 |
| **S1.2** | P1 | `FR-KYB-001..004`, `FR-TEN-003`, `FR-SEC-007`, `FR-AUD-004` | 7 |
| **S1.3** | P1 | `FR-KYB-005`, `FR-KYB-006`, `FR-KYB-008..010`, `FR-KYB-013`, `FR-TAX-001`, `FR-SEC-008`, `FR-UX-008` | 9 |
| **S1.4** | P1 | `FR-BNK-001..004` | 4 |
| **S1.5** | P1 | `FR-LDG-001..006`, `FR-LDG-009` | 7 |
| **S1.6** | P1 | `FR-FEE-003`, `FR-FEE-004` | 2 |
| **S1.7** | P1 | `FR-INV-001..005`, `FR-INV-007`, `FR-INV-008`, `FR-INV-011`, `FR-INV-015`, `FR-TAX-004` | 10 |
| **S1.8** | P1 | `FR-INV-006`, `FR-UX-007` | 2 |
| **S1.9** | P1 | `FR-INV-010`, `FR-CHK-001`, `FR-CHK-003..010`, `FR-UX-009` | 11 |
| **S1.10** | P1 | `FR-PAY-009`, `FR-CHK-002` | 2 |
| **S1.11** | P1 | `FR-PAY-001..008` | 8 |
| **S1.12** | P1 | `FR-API-006`, `FR-SEC-006` | 2 |
| **S1.13** | P1 | `FR-RFD-001..008`, `FR-INV-009` | 9 |
| **S1.14** | P1 | `FR-PYT-001..007`, `FR-PYT-009`, `FR-PYT-010`, `FR-PYT-012` | 10 |
| **S1.15** | P1 | `FR-UX-006`, `FR-LDG-011` | 2 |
| **S1.16** | P1 | `FR-ADM-001..004`, `FR-ADM-006`, `FR-ADM-009..011`, `FR-AUTH-008` | 9 |
| **S1.17** | P1 | `FR-CMS-001`, `FR-CMS-007`, `FR-SEC-018` | 3 |
| **S1.18** | P1 | `FR-NTF-001..003`, `FR-EML-001`, `FR-EML-005` | 5 |
| **S1.19** | P1 | `FR-API-001..005` | 5 |
| **S1.20** | P1 | `FR-RCN-001..006`, `FR-RPT-005` | 7 |
| **S1.21** | P1 | `FR-NFR-001` | 1 |
| **S2.1** | P2 | `FR-DSP-001..010` | 10 |
| **S2.2** | P2 | `FR-PYT-008`, `FR-PYT-011` | 2 |
| **S2.3** | P2 | `FR-LDG-007`, `FR-LDG-008`, `FR-LDG-010` | 3 |
| **S2.4** | P2 | `FR-FEE-001`, `FR-FEE-002`, `FR-FEE-005..008` | 6 |
| **S2.5** | P2 | `FR-TAX-005`, `FR-TAX-006` | 2 |
| **S2.6** | P2 | `FR-RPT-001..003`, `FR-RCN-008` | 4 |
| **S2.7** | P2 | `FR-SDK-001..003`, `FR-API-007..009` | 6 |
| **S2.8** | P2 | `FR-WOO-001..008` | 8 |
| **S2.9** | P2 | `FR-CMS-002..006`, `FR-CMS-009`, `FR-CMS-010` | 7 |
| **S2.10** | P2 | `FR-SUP-001..003` | 3 |
| **S2.11** | P2 | `FR-EML-002..004` | 3 |
| **S2.12** | P2 | `FR-KYB-007`, `FR-KYB-011`, `FR-KYB-012` | 3 |
| **S2.13** | P2 | `FR-INV-012..014`, `FR-INV-016` | 4 |
| **S2.14** | P2 | `FR-PAY-010..012`, `FR-PAY-014` | 4 |
| **S2.15** | P2 | `FR-ADM-005`, `FR-ADM-007`, `FR-ADM-008`, `FR-ADM-012` | 4 |
| **S2.16** | P2 | `FR-UX-004`, `FR-UX-005`, `FR-NFR-008` | 3 |
| **S2.17** | P2 | `FR-AUD-006`, `FR-SEC-017` | 2 |
| **S2.18** | P2 | `FR-SEC-015` | 1 |
| **S3.1** | P3 | `FR-PAY-013` | 1 |
| **S3.2** | P3 | `FR-LDG-012` | 1 |
| **S3.3** | P3 | `FR-TAX-002`, `FR-TAX-003`, `FR-TAX-007`, `FR-TAX-008` | 4 |
| **S3.4** | P3 | `FR-SEC-016` | 1 |
| **S3.5** | P3 | `FR-RCN-007` | 1 |
| **S3.6** | P3 | `FR-AUD-005` | 1 |
| **S3.7** | P3 | `FR-NTF-004`, `FR-RPT-004`, `FR-FEE-009` | 3 |
| **S3.8** | P3 |  | 0 |
| **Total** | | | **241** |

### B.1 Reverse lookup (FR → step)

| FR | Requirement (short) | Master spec phase | Owner |
|---|---|---|---|
| `FR-ADM-001` | Admin overview with queues + KPIs | 1 | S1.16 |
| `FR-ADM-002` | Merchant list/detail with tabs and notes | 1 | S1.16 |
| `FR-ADM-003` | Staff management + dual-scope RBAC | 1 | S1.16 |
| `FR-ADM-004` | Maker-checker approvals inbox | 1 | S1.16 |
| `FR-ADM-005` | Risk queue, rules, blocklists | 2 | S2.15 |
| `FR-ADM-006` | Compliance queues (KYB, screening, reviews) | 1 | S1.16 |
| `FR-ADM-007` | Finance: ledger explorer, recon, adjustments, fees | 2 | S2.15 |
| `FR-ADM-008` | Processors: accounts, routing, health | 2 | S2.15 |
| `FR-ADM-009` | Feature flags + kill switches | 1 | S1.16 |
| `FR-ADM-010` | Audit log search/diff/export | 1 | S1.16 |
| `FR-ADM-011` | Internal merchant notes (never merchant-visible) | 1 | S1.16 |
| `FR-ADM-012` | Country enablement + risk tier + processor mapping | 2 | S2.15 |
| `FR-API-001` | REST v1 with date versioning + OpenAPI 3.1 | 1 | S1.19 |
| `FR-API-002` | API keys hashed, scoped, sandbox/live | 1 | S1.19 |
| `FR-API-003` | Idempotency on all mutating endpoints | 1 | S1.19 |
| `FR-API-004` | Cursor pagination, consistent errors, request ids | 1 | S1.19 |
| `FR-API-005` | Rate limits per key/plan with headers | 1 | S1.19 |
| `FR-API-006` | Webhook endpoints with HMAC + retries + replay | 1 | S1.12 |
| `FR-API-007` | Sandbox simulator endpoints | 2 | S2.7 |
| `FR-API-008` | Public API docs + examples | 2 | S2.7 |
| `FR-API-009` | Sampled API request logs (redacted, 30-day retention) for… | 2 | S2.7 |
| `FR-AUD-001` | Hash-chained append-only audit log | 1 | S0.9 |
| `FR-AUD-002` | Daily signed checkpoints | 1 | S0.9 |
| `FR-AUD-003` | Audit search/diff/export | 1 | S0.9 |
| `FR-AUD-004` | Document access auditing (KYC/dispute/invoice) | 1 | S1.2 |
| `FR-AUD-005` | 7-year retention + WORM export | 3 | S3.6 |
| `FR-AUD-006` | Tenant-scoped activity feed for merchants | 2 | S2.17 |
| `FR-AUTH-001` | Email/password sign-up, verification, login, logout | 1 | S0.6 |
| `FR-AUTH-002` | TOTP MFA for staff, strongly prompted for merchants | 1 | S0.6 |
| `FR-AUTH-003` | Step-up re-auth for sensitive actions (≤5 min) | 1 | S0.6 |
| `FR-AUTH-004` | Session binding, rotation, revocation, device list | 1 | S0.6 |
| `FR-AUTH-005` | Lockout + Turnstile after 3 failures; unlock via email+TOTP | 1 | S0.6 |
| `FR-AUTH-006` | Breached-password check (HIBP k-anonymity) | 1 | S0.6 |
| `FR-AUTH-007` | Password reset invalidates all sessions | 1 | S0.6 |
| `FR-AUTH-008` | Invite-only staff accounts + role assignment | 1 | S1.16 |
| `FR-BNK-001` | Bank account add with masking + encryption | 1 | S1.4 |
| `FR-BNK-002` | Verification (micro-deposit/instant/document) | 1 | S1.4 |
| `FR-BNK-003` | Bank change: maker-checker + step-up + 24h cooling + noti… | 1 | S1.4 |
| `FR-BNK-004` | First-payout cap on new bank accounts | 1 | S1.4 |
| `FR-CHK-001` | Public hosted checkout, no buyer account | 1 | S1.9 |
| `FR-CHK-002` | Processor-hosted card fields only (no PAN in app) | 1 | S1.10 |
| `FR-CHK-003` | 3DS2 requested per §16.3 rules | 1 | S1.9 |
| `FR-CHK-004` | AVS postal enforcement US/CA/UK + fallback challenge | 1 | S1.9 |
| `FR-CHK-005` | Guest email/name capture with consent for saving | 1 | S1.9 |
| `FR-CHK-006` | Buyer receipt email + signed receipt link | 1 | S1.9 |
| `FR-CHK-007` | PCI/TLS/3DS badge bar, no trackers, noindex | 1 | S1.9 |
| `FR-CHK-008` | Double-payment prevention (link + lock + unique index + t… | 1 | S1.9 |
| `FR-CHK-009` | Expired/revoked links show safe state | 1 | S1.9 |
| `FR-CHK-010` | EN/BN checkout localization (core payment strings; full p… | 1 | S1.9 |
| `FR-CMS-001` | 17 pages editable (EN/BN) with versioning | 1 | S1.17 |
| `FR-CMS-002` | Blog with MDX, scheduling, SEO | 2 | S2.9 |
| `FR-CMS-003` | Navigation editor | 2 | S2.9 |
| `FR-CMS-004` | Media library with 2 MB limit + optimization | 2 | S2.9 |
| `FR-CMS-005` | Legal versions + merchant acceptance tracking | 2 | S2.9 |
| `FR-CMS-006` | SEO metadata, sitemap, hreflang, structured data | 2 | S2.9 |
| `FR-CMS-007` | Contact form → support ticket | 1 | S1.17 |
| `FR-CMS-008` | White-label platform profile (logo/address/header/footer) | 1 | S0.11 |
| `FR-CMS-009` | Draft/preview/publish + cache invalidation | 2 | S2.9 |
| `FR-CMS-010` | Docs + generated API reference | 2 | S2.9 |
| `FR-DSP-001` | Dispute intake from webhook with fund freeze | 2 | S2.1 |
| `FR-DSP-002` | Deadline tracking + alerts at 72/48/24h | 2 | S2.1 |
| `FR-DSP-003` | Reason-code evidence checklists | 2 | S2.1 |
| `FR-DSP-004` | Evidence upload 10 MB, 20 files, virus scan | 2 | S2.1 |
| `FR-DSP-005` | Response submission with confirmation + audit | 2 | S2.1 |
| `FR-DSP-006` | Auto-generated evidence bundle | 2 | S2.1 |
| `FR-DSP-007` | Outcome accounting (won/lost/accepted) + fees | 2 | S2.1 |
| `FR-DSP-008` | Chargeback ratio monitoring + alerts | 2 | S2.1 |
| `FR-DSP-009` | Staff submit-on-behalf with approval | 2 | S2.1 |
| `FR-DSP-010` | Warning/retrieval requests without fund movement | 2 | S2.1 |
| `FR-EML-001` | Transactional provider + failover | 1 | S1.18 |
| `FR-EML-002` | Promotional separation (subdomain/key/suppression) | 2 | S2.11 |
| `FR-EML-003` | Template editor with variables + preview | 2 | S2.11 |
| `FR-EML-004` | Delivery logs + bounce/complaint handling | 2 | S2.11 |
| `FR-EML-005` | SPF/DKIM/DMARC configuration | 1 | S1.18 |
| `FR-FEE-001` | Plan tiers with entitlements and limits | 2 | S2.4 |
| `FR-FEE-002` | Fee schedules (plan + merchant override, effective dates) | 2 | S2.4 |
| `FR-FEE-003` | Fee snapshot per charge (immutable) | 1 | S1.6 |
| `FR-FEE-004` | Fee types: processing + payout (Phase 1); dispute, refund… | 1 | S1.6 |
| `FR-FEE-005` | Subscription billing with proration + dunning | 2 | S2.4 |
| `FR-FEE-006` | Entitlement enforcement (users, keys, invoices) | 2 | S2.4 |
| `FR-FEE-007` | Upgrade/downgrade without data loss | 2 | S2.4 |
| `FR-FEE-008` | Fee revenue reporting vs processor cost | 2 | S2.4 |
| `FR-FEE-009` | Promo/waiver support with audit | 3 | S3.7 |
| `FR-INV-001` | Create/edit draft invoices with line items, qty, price, d… | 1 | S1.7 |
| `FR-INV-002` | Per-line tax rates + invoice tax breakdown by jurisdiction | 1 | S1.7 |
| `FR-INV-003` | Gapless invoice numbering per merchant per year | 1 | S1.7 |
| `FR-INV-004` | Finalize locks totals + snapshots customer/render payload | 1 | S1.7 |
| `FR-INV-005` | Send invoice email with hosted link + optional PDF | 1 | S1.7 |
| `FR-INV-006` | American-standard PDF with guilloche/watermark/QR/hash | 1 | S1.8 |
| `FR-INV-007` | View tracking, reminders, overdue status | 1 | S1.7 |
| `FR-INV-008` | Void unpaid invoice; paid invoices cannot be voided | 1 | S1.7 |
| `FR-INV-009` | Credit memos for refunds/adjustments, immutable, numbered | 1 | S1.13 |
| `FR-INV-010` | Payment links (invoice and standalone) with expiry/revoca… | 1 | S1.9 |
| `FR-INV-011` | Customer records, per-merchant, guest-friendly | 1 | S1.7 |
| `FR-INV-012` | Product catalog with tax codes | 2 | S2.13 |
| `FR-INV-013` | CSV import of customers/products | 2 | S2.13 |
| `FR-INV-014` | Partial payments (opt-in) with total enforcement | 2 | S2.13 |
| `FR-INV-015` | Invoice attachments (PDF/JPG/PNG/CSV, 10 MB, hashed) | 1 | S1.7 |
| `FR-INV-016` | Bulk payment reminders with per-invoice throttling | 2 | S2.13 |
| `FR-KYB-001` | 5-step onboarding wizard with save/resume | 1 | S1.2 |
| `FR-KYB-002` | Business profile: legal name, DBA, country, type, registr… | 1 | S1.2 |
| `FR-KYB-003` | UBO ≥25% capture (name, DOB, nationality, ownership, cont… | 1 | S1.2 |
| `FR-KYB-004` | Document upload with presigned URLs, 10 MB, PDF/JPG/PNG | 1 | S1.2 |
| `FR-KYB-005` | Sanctions/PEP/adverse-media screening with manual review | 1 | S1.3 |
| `FR-KYB-006` | KYB decision workflow with reason codes and more-info loop | 1 | S1.3 |
| `FR-KYB-007` | Periodic review scheduling (L1 annual, L2 6mo, L3 quarterly) | 2 | S2.12 |
| `FR-KYB-008` | Lifecycle: submit → review → approve/reject → suspend → r… | 1 | S1.3 |
| `FR-KYB-009` | Separate `charges_enabled` and `payouts_enabled` controls | 1 | S1.3 |
| `FR-KYB-010` | Prohibited-business list enforcement + website review | 1 | S1.3 |
| `FR-KYB-011` | KYC for individuals with ID + liveness (provider adapter… | 2 | S2.12 |
| `FR-KYB-012` | Ongoing monitoring (volume, disputes, refunds, site changes) | 2 | S2.12 |
| `FR-KYB-013` | Staff-requested specific documents with due date + mercha… | 1 | S1.3 |
| `FR-LDG-001` | Chart of accounts auto-provisioned per merchant | 1 | S1.5 |
| `FR-LDG-002` | Double-entry postings for every money event | 1 | S1.5 |
| `FR-LDG-003` | Buckets Pending/Available/Reserve/Disputed | 1 | S1.5 |
| `FR-LDG-004` | Immutable ledger (no UPDATE/DELETE) | 1 | S1.5 |
| `FR-LDG-005` | Hash chain + daily verification | 1 | S1.5 |
| `FR-LDG-006` | Balances view + drill-down + CSV | 1 | S1.5 |
| `FR-LDG-007` | Adjustments with maker-checker + reason | 2 | S2.3 |
| `FR-LDG-008` | Period close + reopen with approval | 2 | S2.3 |
| `FR-LDG-009` | Fee accounting separated from processor cost | 1 | S1.5 |
| `FR-LDG-010` | No posting in closed periods | 2 | S2.3 |
| `FR-LDG-011` | Merchant-facing "why is my balance" explainer | 1 | S1.15 |
| `FR-LDG-012` | Multi-currency FX postings (Phase 3) | 3 | S3.2 |
| `FR-MER-001` | Validated dynamic statement descriptor (≤22 chars, saniti… | 1 | S1.1 |
| `FR-NFR-001` | Performance budgets (master spec §5.6) | 1 | S1.21 |
| `FR-NFR-002` | Cached public pages + tag revalidation | 1 | S0.11 |
| `FR-NFR-003` | Observability + alerts | 1 | S0.13 |
| `FR-NFR-004` | Backups + PITR + quarterly restore drill | 1 | S0.13 |
| `FR-NFR-005` | CI quality gates (master spec §5.9) | 0 | S0.2 |
| `FR-NFR-006` | Test suites (master spec §33) | 1 | S0.2 |
| `FR-NFR-007` | Runbooks (master spec §36) | 1 | S0.13 |
| `FR-NFR-008` | Accessibility + performance regression in CI | 2 | S2.16 |
| `FR-NTF-001` | In-app notifications with read state | 1 | S1.18 |
| `FR-NTF-002` | Preferences per event/channel | 1 | S1.18 |
| `FR-NTF-003` | Event matrix per master spec §29.3 | 1 | S1.18 |
| `FR-NTF-004` | Digest for low-priority events | 3 | S3.7 |
| `FR-PAY-001` | Authorization, capture, void, status sync | 1 | S1.11 |
| `FR-PAY-002` | Manual capture with 5-day hold and review queue | 1 | S1.11 |
| `FR-PAY-003` | Tokenized payment methods (no PAN), per-merchant namespace | 1 | S1.11 |
| `FR-PAY-004` | Decline classification + retry caps (5/24h soft; block ha… | 1 | S1.11 |
| `FR-PAY-005` | Velocity limits per IP/device/email/card | 1 | S1.11 |
| `FR-PAY-006` | Card fingerprint blocklist | 1 | S1.11 |
| `FR-PAY-007` | Idempotency on all payment mutations | 1 | S1.11 |
| `FR-PAY-008` | Processor webhooks verified, deduped, async, re-fetched | 1 | S1.11 |
| `FR-PAY-009` | Sandbox/live strict separation | 1 | S1.10 |
| `FR-PAY-010` | Wallet support where processor allows (Apple/Google Pay) | 2 | S2.14 |
| `FR-PAY-011` | Partial capture | 2 | S2.14 |
| `FR-PAY-012` | Retry reminders + cancel conditions | 2 | S2.14 |
| `FR-PAY-013` | Multi-processor routing by country/MCC | 3 | S3.1 |
| `FR-PAY-014` | Offline/recorded payments (bank transfer) with proof, aud… | 2 | S2.14 |
| `FR-PYT-001` | Bank onboarding + default account rules | 1 | S1.14 |
| `FR-PYT-002` | T+N schedule engine (daily/weekly/manual, cut-off, holidays) | 1 | S1.14 |
| `FR-PYT-003` | Manual payout request with eligibility checks | 1 | S1.14 |
| `FR-PYT-004` | Maker-checker + step-up for payouts | 1 | S1.14 |
| `FR-PYT-005` | Partner submission with idempotency + status sync | 1 | S1.14 |
| `FR-PYT-006` | Failure/return handling (funds back to AVAILABLE) | 1 | S1.14 |
| `FR-PYT-007` | Payout receipt PDF (Phase 1) + cross-border remittance ad… | 1 | S1.14 |
| `FR-PYT-008` | Rolling reserves with hold/release/forfeit | 2 | S2.2 |
| `FR-PYT-009` | Payout holds (manual + risk + dispute) | 1 | S1.14 |
| `FR-PYT-010` | Minimum threshold, caps, split payouts | 1 | S1.14 |
| `FR-PYT-011` | Negative balance dunning + offsets + write-off | 2 | S2.2 |
| `FR-PYT-012` | Payout notifications + webhooks | 1 | S1.14 |
| `FR-RCN-001` | Settlement report import per processor/day | 2 | S1.20 |
| `FR-RCN-002` | Auto-match payments/refunds/disputes/fees/payouts | 2 | S1.20 |
| `FR-RCN-003` | Exception queue with codes, owner, SLA | 2 | S1.20 |
| `FR-RCN-004` | Daily close gate (balanced, verified, exceptions owned) | 2 | S1.20 |
| `FR-RCN-005` | Variance alerts > $1 | 2 | S1.20 |
| `FR-RCN-006` | Corrective ledger entries via approval | 2 | S1.20 |
| `FR-RCN-007` | Bank confirmation matching | 3 | S3.5 |
| `FR-RCN-008` | Reconciliation report export | 2 | S2.6 |
| `FR-RFD-001` | Full/partial refunds bounded by captured amount | 1 | S1.13 |
| `FR-RFD-002` | Maker-checker above threshold | 1 | S1.13 |
| `FR-RFD-003` | Processor refund with idempotency + status sync | 1 | S1.13 |
| `FR-RFD-004` | Ledger reversal + fee policy handling | 1 | S1.13 |
| `FR-RFD-005` | Credit memo generated automatically | 1 | S1.13 |
| `FR-RFD-006` | Buyer refund notification | 1 | S1.13 |
| `FR-RFD-007` | Refund blocked when disputed; window enforced | 1 | S1.13 |
| `FR-RFD-008` | Negative-balance warning before confirming | 1 | S1.13 |
| `FR-RPT-001` | Merchant reports: sales, fees, refunds, disputes, tax, pa… | 2 | S2.6 |
| `FR-RPT-002` | Admin reports: GMV, take rate, cohorts, processor mix | 2 | S2.6 |
| `FR-RPT-003` | CSV exports streamed + expiring links | 2 | S2.6 |
| `FR-RPT-004` | Scheduled report emails | 3 | S3.7 |
| `FR-RPT-005` | Statements monthly PDF/CSV | 2 | S1.20 |
| `FR-SDK-001` | Node SDK with typed client + auto idempotency | 2 | S2.7 |
| `FR-SDK-002` | Browser embed SDK (iframe, 3DS, a11y) | 2 | S2.7 |
| `FR-SDK-003` | Webhook signature helper | 2 | S2.7 |
| `FR-SEC-001` | Default-deny RLS + forced on all tenant tables | 0 | S0.8 |
| `FR-SEC-002` | Strict CSP with nonces + processor allowlist | 1 | S0.12 |
| `FR-SEC-003` | CSRF double-submit + Origin checks | 1 | S0.7 |
| `FR-SEC-004` | SameSite=Lax session cookies, `__Host-` prefix | 1 | S0.6 |
| `FR-SEC-005` | Rate limits (edge + app + business) | 1 | S0.10 |
| `FR-SEC-006` | SSRF-safe webhook URL validation | 1 | S1.12 |
| `FR-SEC-007` | Upload validation (magic bytes, MIME, SHA-256, virus) | 1 | S1.2 |
| `FR-SEC-008` | AES-256-GCM envelope encryption + key versioning | 1 | S1.3 |
| `FR-SEC-009` | PII redaction in logs + Sentry scrubbing | 1 | S0.5 |
| `FR-SEC-010` | HIBP password check | 1 | S0.6 |
| `FR-SEC-011` | Turnstile on auth/contact/checkout | 1 | S0.6 |
| `FR-SEC-012` | WAF/DDoS/DNSSEC/HSTS at edge | 1 | S0.12 |
| `FR-SEC-013` | Secrets never in client; service role server-only | 1 | S0.12 |
| `FR-SEC-014` | Dependency + secret scanning in CI | 1 | S0.2 |
| `FR-SEC-015` | Annual pentest + ASV scans | 2/3 | S2.18 |
| `FR-SEC-016` | WebAuthn-ready MFA | 3 | S3.4 |
| `FR-SEC-017` | Data retention + DSAR workflow | 2 | S2.17 |
| `FR-SEC-018` | Privacy policy + consent + cookie notice | 1 | S1.17 |
| `FR-SEC-019` | Incident response runbook + breach notification | 1 | S0.13 |
| `FR-SEC-020` | No security theater (no right-click blocking) | 1 | S0.12 |
| `FR-SUP-001` | Ticket lifecycle + SLA | 2 | S2.10 |
| `FR-SUP-002` | Threaded messages + internal notes | 2 | S2.10 |
| `FR-SUP-003` | Canned responses + variables | 2 | S2.10 |
| `FR-TAX-001` | W-9 / W-8BEN / W-8BEN-E collection with validation and ve… | 1 | S1.3 |
| `FR-TAX-002` | Withholding tracking + payout blocking on missing forms | 3 | S3.3 |
| `FR-TAX-003` | 1099-K / 1042-S data generation and filer status | 3 | S3.3 |
| `FR-TAX-004` | Sales-tax rate tables + snapshots | 1 | S1.7 |
| `FR-TAX-005` | Tax reports by jurisdiction/period + CSV | 2 | S2.5 |
| `FR-TAX-006` | Exemption certificates | 2 | S2.5 |
| `FR-TAX-007` | Tax engine adapter (Stripe Tax/Avalara/TaxJar) | 3 | S3.3 |
| `FR-TAX-008` | Year-end tax packet | 3 | S3.3 |
| `FR-TEN-001` | Tenant scoping by `merchant_id` on every tenant table | 0 | S0.8 |
| `FR-TEN-002` | Cross-tenant requests return 404 with no data | 0 | S0.8 |
| `FR-TEN-003` | Storage paths scoped per merchant with signed URLs | 1 | S1.2 |
| `FR-TEN-004` | Cache keys include tenant + role; financial data never CD… | 1 | S0.5 |
| `FR-TEN-005` | Background jobs re-verify merchant ownership | 1 | S0.10 |
| `FR-UX-001` | Responsive 320/768/1440, bottom nav on mobile | 1 | S0.4 |
| `FR-UX-002` | WCAG 2.2 AA, keyboard, screen reader | 1 | S0.4 |
| `FR-UX-003` | Design tokens + component library | 0 | S0.4 |
| `FR-UX-004` | High-contrast light/dark themes | 2 | S2.16 |
| `FR-UX-005` | EN/BN localization everywhere | 2 | S2.16 |
| `FR-UX-006` | Dashboard ≤6 queries, skeletons, empty/error states | 1 | S1.15 |
| `FR-UX-007` | PDF security design (guilloche/watermark/QR/hash) | 1 | S1.8 |
| `FR-UX-008` | KYC viewer dynamic watermark + audit | 1 | S1.3 |
| `FR-UX-009` | Merchant branding on invoice/checkout/receipts | 1 | S1.9 |
| `FR-UX-010` | Status badges never color-only | 1 | S0.4 |
| `FR-WOO-001` | Plugin connect + capability check | 2 | S2.8 |
| `FR-WOO-002` | Hosted checkout redirect + order lifecycle | 2 | S2.8 |
| `FR-WOO-003` | Webhook handling + signature verification | 2 | S2.8 |
| `FR-WOO-004` | Refunds + partial refunds | 2 | S2.8 |
| `FR-WOO-005` | HPOS + Blocks compatibility | 2 | S2.8 |
| `FR-WOO-006` | Sandbox toggle + redacted debug log | 2 | S2.8 |
| `FR-WOO-007` | i18n EN/BN + uninstall cleanup | 2 | S2.8 |
| `FR-WOO-008` | Distribution (wordpress.org/GitHub) + readme | 2 | S2.8 |

**Reading the two phase columns.** *Master spec phase* is when the spec says the feature lands. *Owner step phase* is when this plan builds it. They differ in exactly two places, both deliberate and both documented: `FR-RCN-001..006` (spec phase 2) are built in S1.20 because manual reconciliation must exist before volume arrives; `FR-RPT-005` (spec phase 2) is built in S1.20 for the same reason. Every other row agrees.

| Deliberate pull-forward | Spec phase | Built in | Why |
|---|---|---|---|
| `FR-RCN-001..006` | 2 | S1.20 | Without a daily close from day one, a mismatch found in month six is unrecoverable. |
| `FR-RPT-005` | 2 | S1.20 | Merchants expect a monthly statement in the first month of live money. |

---

## Appendix C — Route inventory, permissions and caching

Every route in the product, its layout group, who may reach it, what it may cache, and which step builds it. **If a route is not in this table, it does not exist** — add it here before creating the file. Routes are App Router paths under `src/app/`; `[id]` is a UUID or public id, `[token]` is a secret token.

Legend: **Auth** = `public` (anyone), `session` (signed in), `admin` (staff role with the permission in the next column), `token` (possession of an unguessable URL). **Cache** = `no-store` (never cached — money, PII, auth), `private` (per-user, `revalidate` allowed), `public` (CDN-cacheable with tags).

### C.1 Public and marketing

| Route | Group | Auth | Cache | Step |
|---|---|---|---|---|
| `/` | `(marketing)` | public | public, tag `cms:home` | S0.11 / S1.17 |
| `/[slug]` (17 CMS pages) | `(marketing)` | public | public, tag `cms:page:<slug>` | S1.17 |
| `/pricing`, `/features`, `/security`, `/contact`, `/legal/[doc]` | `(marketing)` | public | public | S1.17 |
| `/blog`, `/blog/[slug]` | `(marketing)` | public | public, tag `cms:blog` | S2.9 |
| `/docs`, `/docs/[slug]` | `(marketing)` | public | public | S2.9 |
| `/docs/api` (generated reference) | `(marketing)` | public | public | S2.7 |
| `/sitemap.xml`, `/robots.txt`, `/manifest.webmanifest` | root | public | public | S0.11 |
| `/status` (optional external) | — | public | public | S3.8 |

### C.2 Auth

| Route | Group | Auth | Cache | Step |
|---|---|---|---|---|
| `/sign-up`, `/sign-in`, `/verify-email`, `/reset`, `/reset/[token]`, `/invite/[token]` | `(auth)` | public | no-store | S0.6 |
| `/mfa`, `/mfa/recovery` | `(auth)` | session (pre-MFA) | no-store | S0.6 |
| `/security` (device list, MFA, passkeys, sessions) | `(merchant)` | session | no-store | S0.6 / S3.4 |
| `/accept-legal/[version]` | `(auth)` | session | no-store | S2.9 |

### C.3 Merchant portal (`/app/*`, layout `(merchant)`)

| Route | Permission | Cache | Step |
|---|---|---|---|
| `/app` (home, ≤ 6 queries) | session | private | S1.15 |
| `/app/onboarding`, `/app/onboarding/[step]` | session | no-store | S1.2 |
| `/app/payments` (list), `/app/payments/[id]` | `payments.read` | no-store | S1.15 |
| `/app/invoices`, `/app/invoices/new`, `/app/invoices/[id]` | `invoices.read/create/update` | no-store | S1.7 / S1.15 |
| `/app/payment-links`, `/app/payment-links/new` | `payment_links.read/create` | no-store | S1.9 |
| `/app/customers`, `/app/customers/[id]` | `customers.read` | private | S1.15 |
| `/app/products`, `/app/products/import` | `products.read/manage` | private | S2.13 |
| `/app/money` (balances, payouts, reserves) | `payouts.read` | no-store | S1.15 |
| `/app/money/payouts/[id]`, `/app/money/payouts/new` | `payouts.read/create` | no-store | S1.14 |
| `/app/money/statements` | `reports.read` | private | S1.20 |
| `/app/refunds`, `/app/refunds/[id]` | `refunds.read` | no-store | S1.13 |
| `/app/disputes`, `/app/disputes/[id]` | `disputes.read/manage` | no-store | S2.1 |
| `/app/reports`, `/app/reports/[type]` | `reports.read` | private | S2.6 |
| `/app/bank-accounts`, `/app/bank-accounts/change` | `bank.read/manage` | no-store | S1.4 |
| `/app/settings` (+ `/profile`, `/team`, `/notifications`, `/billing`, `/branding`) | `settings.read/manage` | private | S1.15 |
| `/app/compliance` (KYB status, documents, reviews) | session | no-store | S1.2 / S2.12 |
| `/app/developers` (+ `/keys`, `/webhooks`, `/requests`) | `developers.manage` | no-store | S1.19 / S2.7 |
| `/app/support`, `/app/support/[ticket]` | session | no-store | S2.10 |
| `/app/activity` | session | private | S2.17 |
| `/app/privacy` (DSAR history) | session | no-store | S2.17 |

### C.4 Admin console (`/admin/*`, layout `(admin)`)

| Route | Permission | Cache | Step |
|---|---|---|---|
| `/admin` (queues + KPIs) | staff | no-store | S1.16 |
| `/admin/merchants`, `/admin/merchants/[id]` (+ tabs) | `merchants.read` | no-store | S1.16 |
| `/admin/kyb`, `/admin/kyb/[id]`, `/admin/screening` | `compliance.review` | no-store | S1.3 |
| `/admin/approvals` (maker-checker inbox) | staff | no-store | S1.16 |
| `/admin/users`, `/admin/roles` | `users.manage` | no-store | S1.16 |
| `/admin/audit` (+ `/audit/[id]` diff) | `audit.read` | no-store | S1.16 |
| `/admin/flags` | `platform.manage` | no-store | S1.16 |
| `/admin/platform/profile` | `platform.manage` | no-store | S0.11 |
| `/admin/cms` (+ `/pages`, `/blog`, `/media`, `/nav`, `/legal`) | `cms.manage` | no-store | S1.17 / S2.9 |
| `/admin/finance` (+ `/ledger`, `/recon`, `/adjustments`, `/fees`) | `finance.view` | no-store | S2.3 / S2.15 |
| `/admin/disputes`, `/admin/disputes/[id]` | `disputes.manage` | no-store | S2.1 |
| `/admin/risk`, `/admin/risk/rules`, `/admin/risk/blocklists` | `risk.manage` | no-store | S2.15 |
| `/admin/processors`, `/admin/processors/[id]` | `platform.manage` | no-store | S2.15 |
| `/admin/countries` | `platform.manage` | no-store | S2.15 |
| `/admin/reports`, `/admin/reports/[type]` | `reports.read` | private | S2.6 |
| `/admin/support`, `/admin/support/[ticket]` | `support.manage` | no-store | S2.10 |
| `/admin/jobs`, `/admin/jobs/[id]` (outbox, dead letters) | `platform.manage` | no-store | S0.10 |
| `/admin/health` (env, migrations, worker, backups) | `platform.manage` | no-store | S0.13 |

### C.5 Buyer checkout (`(checkout)`, no account)

| Route | Auth | Cache | Step |
|---|---|---|---|
| `/pay/[token]` | token | no-store, `noindex` | S1.9 |
| `/pay/[token]/success`, `/failed`, `/expired` | token | no-store, `noindex` | S1.9 |
| `/pay/[token]/3ds-return` | token + state | no-store, `noindex` | S1.11 |
| `/receipt/[token]` | token | no-store, `noindex` | S1.11 |
| `/embed/checkout` (iframe host for `@kdpay/embed`) | token | no-store, `frame-ancestors` allowlist | S2.7 |

### C.6 API and machine surfaces

| Route | Auth | Notes | Step |
|---|---|---|---|
| `/api/v1/*` (REST v1) | API key | versioned by date, cursor paginated, idempotency on POST | S1.19 |
| `/api/webhooks/processor/[provider]` | HMAC + IP allowlist | raw body, 5-min tolerance, deduped | S1.12 |
| `/api/webhooks/email/[provider]` | HMAC | delivery events, suppression | S2.11 |
| `/api/internal/cron/[job]` | `CRON_SECRET` header | Vercel cron only; idempotent; advisory-locked | S0.10 |
| `/api/internal/health` | none (public, minimal) | DB, worker heartbeat, queue depth, checkpoint age | S0.13 |
| `/api/internal/metrics` | `METRICS_TOKEN` | Prometheus text format | S0.13 |
| `/api/dsar/[id]/download` | session + ownership | signed, expiring | S2.17 |
| `/design` | `APP_ENV !== 'production'` | component gallery | S0.4 |

### C.7 Route rules (enforced by tests, not by memory)

1. Every route group has **one** `layout.tsx`; child routes never re-implement the shell.
2. Money, PII and auth routes are `no-store`; `export const dynamic = 'force-dynamic'` where a fetch is involved. Public marketing routes use `revalidate` + tags, never `force-dynamic`.
3. `/app/**` and `/admin/**` are `noindex` and behind `middleware.ts`; a missing session redirects to `/sign-in?next=<path>` and never renders a blank shell.
4. A cross-tenant or non-member id returns **404**, not 403, and never leaks existence (§0.6, master spec §23.2).
5. Every page has an `error.tsx` and a `loading.tsx`; the error state shows the `request_id` (§15.3).
6. Route files contain no business logic — they call `features/<domain>/queries.ts` or an action.

---

**End of build plan.**
