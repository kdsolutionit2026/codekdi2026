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
- [4. Phase 0 — Foundations (S0.3–S0.11)](#4-phase-0--foundations-s03s011)
- [5. Phase 1 — Money In (S1.1–S1.21)](#5-phase-1--money-in-s11s121)
- [6. Phase 2 and Phase 3 outline](#6-phase-2-and-phase-3-outline)
- [7. Implementation recipes](#7-implementation-recipes)
- [8. Migration map](#8-migration-map)
- [9. Test strategy and commands](#9-test-strategy-and-commands)
- [10. Deploy and promotion](#10-deploy-and-promotion)
- [11. Pitfalls that break real deployments](#11-pitfalls-that-break-real-deployments)
- [12. Per-step prompt template](#12-per-step-prompt-template)
- [13. Progress ledger and first commits](#13-progress-ledger-and-first-commits)
- [14. Global Definition of Done](#14-global-definition-of-done)

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
| 2 | The **single step** you are executing (§4 or §5) | Scope | 25–45 lines |
| 3 | Master spec **only** the sections referenced by that step | Correctness detail | 100–400 lines |
| 4 | The **recipe** (§7) for each pattern the step touches | Canonical code | 20–60 lines each |
| 5 | `docs/PROGRESS.md` tail (last 3 entries) | Where the last agent stopped | ~30 lines |

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
**Depends on:** nothing. **Master spec:** §5.4, §5.5, §31. **Effort:** 1 agent-day.

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
   pnpm add postgres zod @supabase/supabase-js @supabase/ssr pdf-lib resend nanoid
   pnpm add -D vitest @vitest/coverage-v8 playwright @playwright/test supabase \
     @types/node tsx dotenv-cli fast-check
   pnpm dlx shadcn@latest init   # choose CSS variables, slate base
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
8. `vitest.config.ts` with three projects: `unit` (node env, no DB), `integration` (serial, DB), `rls` (serial, DB + role switching).
9. `.gitignore`: add `.env*.local`, `.supabase/`, `test-results/`, `playwright-report/`, `coverage/`.
10. `docs/PROGRESS.md` from the template in §13.1.

**Tests:** a trivial `src/lib/env.test.ts` proving a missing var throws a readable error.
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

## 4. Phase 0 — Foundations (S0.3–S0.11)

Phase 0 outcome: one can sign in, the app knows who you are and what you may do, every table is tenant-isolated, every privileged action is audited, jobs run, and the public shell is branded from the database. **No invoices, no money yet.**

### S0.3 — Database bootstrap (extensions, schemas, roles, conventions)

**Goal:** a reproducible empty database with the right schemas, extensions, roles, and helper conventions.
**Depends on:** S0.2. **Master spec:** §6.1, §6.2, §6.14. **Effort:** 1 agent-day.

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

-- app roles used by tests and by the runtime SET LOCAL ROLE
do $$ begin
  if not exists (select 1 from pg_roles where rolname = 'app_authenticated') then
    create role app_authenticated nologin;
  end if;
end $$;

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

**Tests** (`tests/integration/0001-bootstrap.test.ts`): schemas exist; `anon` cannot `usage` on `private`; `money_amount` rejects 5 decimals.
**Verify:** `supabase db reset && pnpm test:integration`
**Done when:** reset runs from zero in < 60 s and is repeatable.
**Commit:** `feat(S0.3): db bootstrap, schemas, domains, shared triggers`

---

### S0.4 — Design tokens, primitives and app shells

**Goal:** the visual foundation exists once and every later screen reuses it.
**Depends on:** S0.1. **Master spec:** §31.2–§31.7. **Effort:** 2 agent-days.

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

**Build** `src/lib/db/`:

```ts
// client.ts  — server-only singleton
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
```

```ts
// tenant.ts — every authenticated read/write goes through this
import postgres from 'postgres';          // namespace gives TransactionSql types
import { sql } from './client';

export type TenantContext = { userId: string; merchantId: string | null };

export async function withTenant<T>(
  ctx: TenantContext,
  fn: (tx: postgres.TransactionSql) => Promise<T>,
): Promise<T> {
  return sql.begin(async (tx) => {
    await tx`select set_config('request.jwt.claims', ${JSON.stringify({ sub: ctx.userId })}, true)`;
    await tx`set local role authenticated`;
    return fn(tx);
  }) as Promise<T>;
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

**Build**

1. Migration `0003_identity.sql` — `app_users`, `sessions`, `device_fingerprints`, `mfa_factors`, `recovery_codes`, `login_attempts`, `step_up_challenges`, `blocked_ips`, `rate_limit_counters` exactly as master spec §6.4.
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

**Tests** (`tests/integration/session.test.ts`): expired session → 401; revoked session → 401; token rotation on privilege change; cookie flags asserted from the `Set-Cookie` header; replay from a different fingerprint → step-up required.
**Verify:** `pnpm test:integration -- session` + manual sign-in/sign-out in the browser.
**Done when:** DB has a `sessions` row per login and deleting it logs the user out on the next request.
**Commit:** `feat(FR-AUTH-001..005): opaque sessions, sign-in, lockout, csrf`

---

### S0.7 — RBAC: roles, permissions, guards, server-action wrapper

**Goal:** every action is permission-checked in one place; UI visibility is derived, never trusted.
**Depends on:** S0.6. **Master spec:** §20.4, §6.4, §6.14. **Effort:** 2 agent-days.

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

### Phase 0 gate (must all be true before S1.1)

- [ ] `pnpm verify` green from a clean clone.
- [ ] `supabase db reset` applies all migrations; `pnpm db:types` produces no diff.
- [ ] Sign-up → sign-in → MFA → sign-out works; revoked session is rejected on the next request.
- [ ] RLS coverage + isolation suites green; commenting out one policy makes them red.
- [ ] Audit chain verifies; tampering is detected.
- [ ] Worker processes an outbox event exactly once; dead letters visible.
- [ ] `/design` passes axe at 320/768/1440.
- [ ] Brand name/logo/address change in DB reflects on site and in an email.

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

**Build**

1. Migration `0008_merchants.sql` — `merchants`, `merchant_profiles`, `merchant_settings`, `merchant_limits`, `merchant_volume_counters`, `merchant_notes`, `merchant_countries` (master spec §6.5, §6.12). Include the RLS exposure block and the `protect_merchant_columns` trigger (§6.14).
2. `private.create_merchant(p_user uuid, p_input jsonb)` — creates merchant (`status='draft'`, `livemode=false`), profile, settings, limits, a `merchant_members` row with role `owner`, and `user_roles` scope row; idempotent per user+legal name; writes audit + outbox; returns `merchant_id`.
3. Ledger provisioning is **deferred to S1.5** (the ledger tables do not exist yet). S1.5 adds `private.provision_merchant_accounts` and backfills every existing merchant; nothing in S1.1 may reference ledger tables.
4. `rpc_update_merchant_profile` + `rpc_set_merchant_controls` (charges/payouts toggles, staff-only, audited).
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

**Build**

1. Migration `0009_kyb.sql` — `kyb_applications`, `kyb_documents`, `beneficial_owners`, `kyc_verifications`, `screening_results`, `merchant_compliance_flags` (master spec §6.5) + RLS.
2. Storage buckets (via `supabase/config.toml` + a migration of bucket policies): `kyc-docs` (private, 10 MB), `dispute-evidence` (private, 10 MB), `branding` (public read, 2 MB), `cms-media` (public read, 2 MB), `reports` (private), `pdfs` (private). Policies restrict object paths to `merchant/{auth_merchant_id}/…`.
3. `src/lib/storage/upload.ts`:
   - `createUploadUrl({ merchantId, bucket, path, contentType, maxBytes })` → Supabase `createSignedUploadUrl` with 5-minute TTL.
   - `finalizeUpload({ path, sha256, declaredMime })` → server downloads the first 4 KB, checks **magic bytes** (`%PDF`, `\xFF\xD8\xFF`, `\x89PNG`), verifies size, computes SHA-256, stores metadata, optionally runs a virus scan adapter (`VIRUS_SCAN=noop|clamav-http`).
   - Reject: password-protected PDFs, polyglots, > 50 pages, SVG for KYC, anything not PDF/JPG/PNG.
4. Wizard `(merchant)/app/onboarding/*` — 5 steps (business → owners/UBOs → documents → bank (S1.4) → tax form (S1.3) → review), progress bar, save-and-resume, per-step validation, clear rejection reasons, EN/BN strings.
5. UBO editor: name, DOB, nationality, residence, ownership %, flags (controller/director/signer), ID upload; validation: total ownership ≤ 100, at least one controller, ≥ 1 UBO ≥ 25% or an explicit "no 25% owner" attestation.
6. `rpc_submit_kyb` — validates completeness, sets `status='submitted'`, writes audit + outbox (`kyb.submitted`), notifies staff.
7. Document viewer (admin) with dynamic watermark (viewer email + IP + timestamp) rendered server-side; **audit on open**.

**Tests:** upload URL rejects wrong content type and oversized signatures; magic-byte mismatch is rejected even with a `.pdf` name; a 12 MB file is refused; resubmission creates a new `kyb_applications.version`; cross-tenant signed URLs are denied; wizard resume restores state.
**Verify:** `pnpm test:integration -- uploads` + Playwright onboarding happy path (sandbox PDF fixture).
**Done when:** a complete application can be submitted with real files and is visible to staff only.
**Commit:** `feat(FR-KYB-001..004): onboarding wizard, ubo capture, secure uploads`

---

### S1.3 — Admin KYB review, lifecycle controls, tax forms

**Goal:** staff can approve, reject, request documents, suspend, reinstate, and capture W-9/W-8 — all with audit and four-eyes where required.
**Depends on:** S1.2. **Master spec:** §3.6–§3.7, §20.4–§20.5, `FR-KYB-005..010,013`, `FR-TAX-001`. **Effort:** 3 agent-days.

**Build**

1. Migration `0010_tax_documents.sql` — `tax_documents`, `tax_filings`, `merchant_tax_registrations`; add `tax_id_ciphertext` encryption helper use (master spec §21.2).
2. `src/lib/security/crypto.ts` — AES-256-GCM envelope encryption: `encryptField(plaintext, aad)` → `v1:base64(iv):base64(ct):base64(tag)`, `decryptField(...)`, key version from env/KMS; AAD = `${table}:${column}:${recordId}`.
3. Screening adapter `src/lib/compliance/screening.ts` — `screenSubject({ type, name, dob, country })` with `SCREENING_PROVIDER=manual|sumsub|persona`; manual = staff uploads/records result; always writes `screening_results`.
4. Admin queues `/admin/compliance`: applications (SLA, assignee, filters), documents, UBOs, screening, flags, tax docs.
5. Decision RPC `rpc_kyb_decision(application_id, decision, reason_code, notes)` — enforces `compliance.review`, forbids self-review, requires step-up, writes audit, transitions merchant status, emits events.
6. Lifecycle RPCs: `rpc_suspend_merchant`, `rpc_reinstate_merchant` (compliance + risk), `rpc_terminate_merchant`; each requires a reason code and step-up; suspend flips `charges_enabled=false` and `payouts_enabled=false`.
7. Document request flow `rpc_request_documents(merchant_id, types[], due_date, message)` → notification + merchant action item.
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

**Build**

1. `payment_links` creation/revocation (`lnk_` public id, 256-bit token stored as SHA-256, expiry, max uses); constant-time lookup.
2. `/pay/[token]` — server component; loads invoice snapshot + merchant branding + platform settings in **one** query; 404 on expired/revoked; `noindex`; `no-store`.
3. Layout: merchant logo/name, invoice number, amount due, descriptor preview, collapsible line items, due date, support contact, terms link, PCI/TLS/3DS badge bar (master spec §26), EN/BN toggle, mobile-first at 320 px, WCAG 2.2 AA.
4. Buyer step: email + name + billing country (+ optional "save my details" consent → `customer_consents`); Turnstile; server-side Zod; rate limits per IP/token.
5. `POST /api/checkout/session` → risk stitch (S1.11 pipeline, Phase-1 stub = velocity + blocklist) → creates `checkout_sessions` row → returns the processor client config (publishable key + client secret **only**; never a secret key).
6. Card step mounts the processor iframe (S1.10 adapter contract); our code never reads those fields; CSP allows only the processor + Turnstile origins.
7. Success/failed/expired pages `/pay/[token]/success|failed|expired`; receipt link; no confetti, no dark patterns.
8. **Test-mode behavior:** with `PROCESSOR=sandbox`, the card step shows **buttons** ("Approve", "Decline: insufficient funds", "Require 3DS", "Decline: stolen card") — no free-form card input anywhere, preserving `N-01`.

**Tests:** expired/revoked token → 404; token cannot be reused across merchants; amount is server-derived (changing a hidden field changes nothing); Turnstile failure blocks; rate limit returns 429 with `Retry-After`; axe + Lighthouse (LCP budget ≤ 2.0 s on the local throttle); no third-party requests except processor/Turnstile.
**Verify:** `pnpm test:e2e --grep "checkout page"` + Lighthouse CI report.
**Done when:** the page passes a "would I pay here?" review on a phone and contains zero card inputs.
**Commit:** `feat(FR-CHK-001..010): hosted checkout, links, guest capture`

---

### S1.10 — Processor adapter interface + sandbox adapter + Stripe/Airwallex skeletons

**Goal:** business logic never imports a vendor SDK; the whole platform is testable without live credentials.
**Depends on:** S0.5. **Master spec:** §4, §16, `FR-PAY-001,008`, `FR-PAY-013` (interface only). **Effort:** 3 agent-days.

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

**Build**

1. Migration `0017_refunds.sql` — `refunds` (+ `refund_limit_guard` trigger), `credit_memos`, `credit_memo_lines`; add `payments.amount_refunded` check.
2. `rpc_request_refund(payment_id, amount, reason, detail)` — bounds (`≤ captured − refunded`), window (180 d), dispute block, negative-balance preview (`balance_after`), threshold → `approval_requests`.
3. `rpc_approve_refund` — four-eyes, step-up, then submit to processor with idempotency key `refund:{id}`.
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

## 6. Phase 2 and Phase 3 outline

Phase 2 and 3 get their own detailed packets **when Phase 1 closes** (each step reuses this file's structure). Below is the scope so nobody builds them early.

### 6.1 Phase 2 — Money out & scale (weeks 15–26)

| Step | Scope | Master spec | Exit criteria |
|---|---|---|---|
| S2.1 | **Disputes**: intake, fund freeze, evidence portal with reason-code checklists, submission, outcomes, ratio monitor | §12, `FR-DSP-001..010` | Evidence submitted before deadline in test; won/lost ledger correct; ratio alerts fire |
| S2.2 | **Reserves & negative balance**: full engine, rolling release, holds, dunning, offsets, write-off (maker-checker) | master spec §10.7–§10.8, `FR-PYT-008,011` | Reserve release at day 90; dunning ladder verified; write-off audited |
| S2.3 | **Fees, plans, subscriptions**: proration, dunning, entitlements, fee reports | §9, `FR-FEE-005..009` | Upgrade/downgrade without data loss; revenue vs processor cost report |
| S2.4 | **Tax**: rate catalog, exemptions, reports, W-8/W-9 renewal, year-end data | §14, `FR-TAX-002..006` | Tax report ties to invoices; exempt sales correct |
| S2.5 | **Reports & statements**: admin KPIs, cohorts, processor mix, scheduled emails, exports | master spec §32, `FR-RPT-001..005` | Materialized views < 5 min stale; 100k-row export < 5 min |
| S2.6 | **SDKs**: `@kdpay/node`, `@kdpay/embed` | master spec §28.2, `FR-SDK-001..003` | Publish to npm with provenance; embed handles 3DS + a11y |
| S2.7 | **WooCommerce plugin** v1 | master spec §28.3, `FR-WOO-001..008` | HPOS + Blocks; refunds; webhook verification; readme + screenshots |
| S2.8 | **CMS finalize**: blog, media, nav, legal versions approved, docs + generated API reference | master spec §27, `FR-CMS-002..010` | Legal text approved; docs complete; broken links zero |
| S2.9 | **Support system**: tickets, SLA, canned responses, CSAT | master spec §30, `FR-SUP-001..003` | SLA timers + escalation work; internal notes never visible to merchants |
| S2.10 | **Hardening**: pentest remediation, load test at 5× Phase-1 volume, a11y audit, DR drill | master spec §33, §36 | No highs open; RTO/RPO proven |

### 6.2 Phase 3 — Global & enterprise (weeks 27–40)

| Step | Scope | Master spec |
|---|---|---|
| S3.1 | Multi-processor routing + failover (Stripe Connect, Rainforest US, Tazapay evaluation) | master spec §4.2–§4.3, `FR-PAY-013` |
| S3.2 | FX: local payout rails, spread accounting, cross-border remittance advice | §7.5, §10.5, `FR-LDG-012` |
| S3.3 | Tax reporting: 1099-K / 1042-S generation, filer adapter, withholding automation | master spec §3.7, `FR-TAX-002,003,008` |
| S3.4 | Automated KYC/KYB (liveness, ongoing monitoring) + WebAuthn passkeys | master spec §3.6, §20.3, `FR-KYB-011,012` |
| S3.5 | Advanced risk: BIN intelligence, network alerts, explainable model behind the same decision API | master spec §17 |
| S3.6 | Enterprise: SSO (SAML), custom checkout domains, contractual SLA | master spec §27, §32 |
| S3.7 | Scale: partitioning, read replicas, multi-region DR | master spec §6.17, §32 |
| S3.8 | SOC 2 Type I readiness, ISO 27001 gap assessment | master spec §32.5 |

Rule: **no Phase 2/3 table or route may be created during Phase 1** except where a Phase-1 step explicitly says so (disputes tables may be created but stay unused until S2.1).

---

## 7. Implementation recipes

Copy these patterns. If a step's code deviates, the deviation must be justified in the PR.

### 7.1 Authenticated tenant read (server component)

```ts
// src/features/invoices/queries.ts
import 'server-only';
import { withTenant } from '@/lib/db/tenant';
import { getSession } from '@/lib/security/session';
import { assertMerchant } from '@/lib/db/assert-merchant';

export async function listInvoices(cursor?: string, limit = 20) {
  const s = await getSession();                     // throws UnauthorizedError
  const m = await assertMerchant(s, s.activeMerchantId);
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
  handler: async (input, ctx) => requestRefund(ctx, input),
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
| 0022 | `disputes.sql` | S2.1 | disputes, dispute_evidence, dispute_responses, dispute_events, `private.dispute_reason_codes`, `private.network_thresholds`, `private.holidays` |

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

---

## 12. Per-step prompt template

Paste this into the AI agent for every step. Replace the bracketed parts.

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
