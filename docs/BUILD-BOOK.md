# The build book — how to build KD PAY from these files, in order

For a first-time **vibe coder**: you will be directing an AI agent (Claude) rather than typing every line
yourself. This book is the order of operations. Follow it front to back; do not skip ahead to something
interesting.

**What you are building:** a PayFac / Merchant-of-Record platform. KD PAY is the merchant's counterparty — it
onboards them, runs KYB, issues invoices, takes a card payment **through someone else's licensed processor**
(Airwallex / Stripe / etc.), keeps the books in a double-entry ledger, and pays the merchant out. You never
touch a card number and you never hold merchant funds — that is the whole design, and the plan enforces it.

**How long it realistically takes:** 61 chapters, 253 agent-days of estimated work, 402 slices. At 2–3 slices a
day of human-supervised agent time, that is **roughly 6–9 months** for one person. Phase 0 + Phase 1 (a real
product taking real payments) is chapters 1–35, about 120 agent-days.

---

## 0. Read this first (the 20-minute version)

If you read nothing else, read these four, in this order. Everything else is reference.

| Order | File | Why | Time |
|---|---|---|---|
| 1 | **this file** | the order of operations and the rules of the road | 15 min |
| 2 | [`docs/COMPONENTS.md`](COMPONENTS.md) | ten components in plain language, one $100 payment traced end to end. This is the mental model you will need for every later decision | 20 min |
| 3 | [`CLAUDE.md`](../CLAUDE.md) | the rules your agent loads automatically — read them so you can enforce them | 5 min |
| 4 | [`docs/BUILD-WITH-CLAUDE.md`](BUILD-WITH-CLAUDE.md) | the day-to-day loop: commands, prompts, how to check the agent's work | 15 min |

Then **start at chapter 1** and never read ahead more than one chapter. The plan is deliberately large; reading
it end to end is how people lose a week and start improvising.

---

## 1. The whole library, in reading order

Twenty-two documents is a lot, which is exactly why order matters. Nothing below is optional reading — each
one has a moment when you need it.

### Tier 1 — read before your first slice (about 45 minutes)

| # | File | What it is | When you will use it |
|---|---|---|---|
| 1 | `README.md` | the map, 74 lines | once, now |
| 2 | `docs/BUILD-BOOK.md` (this file) | order of operations | keep it open for the first week |
| 3 | `docs/COMPONENTS.md` | the system in plain language | once now; again whenever you feel lost |
| 4 | `CLAUDE.md` | what your agent must never do | whenever you correct the agent |
| 5 | `docs/BUILD-WITH-CLAUDE.md` | the daily loop, prompts, checks | the first week, then as reference |
| 6 | `CONTRIBUTING.md` | commit format, PRs, how to accept agent work | before your first commit |

### Tier 2 — read the chapter you are about to work on (10–25 minutes each time)

| # | File | What it is | When |
|---|---|---|---|
| 7 | `spec.md` | 61 step packets: files, tests, verify command per step | **read only the chapter's packet** |
| 8 | `docs/MASTER_SPECIFICATION.md` | the rules: schema, ledger, security, API, 241 requirements | **only the sections the packet names** |
| 9 | `docs/slices.json` | the slice queue (generated — never edit) | read via `check-steps.mjs --slices` |
| 10 | `docs/steps.json` | the registry: dependencies, effort, status | read via `scripts/next.mjs` |

### Tier 3 — read when the situation calls for it

| # | File | Use it when |
|---|---|---|
| 11 | `docs/STEP-GRANULARITY.md` | a slice feels too big or too small; or you want to know why work is cut this small |
| 12 | `docs/AGENT_PLAYBOOK.md` | you want the deeper reasoning behind the loop, the evidence standard, the reviewer prompt |
| 13 | `docs/TROUBLESHOOTING.md` | **something is broken** — ten symptom families, cheapest check first |
| 14 | `spec.md` §7 (recipes) | you are writing a route, a server action, an idempotent mutation, a ledger post, a webhook, a PDF |
| 15 | `spec.md` §15 (contracts) | you are touching a signature that other steps import |
| 16 | `docs/CHANGE-PLAYBOOK.md` | after launch: add a processor, a currency, a country, a payment method, a report, a price |
| 17 | `docs/adr/` | you need to know *why* a decision was made; ADR 0001 is the interface freeze |
| 18 | `.claude/commands/*.md` | you want to know exactly what `/kickoff`, `/verify`, `/ui`, `/review`, `/ship` will do |
| 19 | `.claude/agents/reviewer.md` | before you run the second-agent review, so you know what it checks |
| 20 | `docs/PROGRESS.md` | start of every session: where the last one stopped |
| 21 | `docs/OPEN_QUESTIONS.md` | something is ambiguous — this is where the answer goes |
| 22 | `docs/runbooks/README.md` | Phase 1 exit: the operational procedures you must actually write |

**Two rules about reading.** First: never load `spec.md` or `MASTER_SPECIFICATION.md` whole — 3,950 and 5,990
lines respectively, and an agent that reads them starts inventing. Second: if two documents disagree, the
**master specification wins** and the disagreement is a bug to report.

### The `.claude/` and `scripts/` folders (one line each)

| Path | What it does for you |
|---|---|
| `CLAUDE.md` | auto-loaded rules for Claude; keeps every session consistent |
| `.claude/commands/kickoff.md` | `/kickoff S1.5.3` — preflight, read narrowly, propose a plan, stop |
| `.claude/commands/verify.md` | `/verify S1.5.3` — run the gate, prove the test can fail, run the plan gates |
| `.claude/commands/ui.md` | `/ui /app/invoices` — open the page in a real browser at 360/768/1440 and report what is broken |
| `.claude/commands/review.md` | `/review` — six-question read-only review of the current diff |
| `.claude/commands/adapter.md` | `/adapter airwallex` — implement a processor against the frozen contract |
| `.claude/commands/ship.md` | `/ship S1.5.3` — one commit, correct message, PR body with evidence |
| `.claude/agents/reviewer.md` | the read-only reviewer subagent used for the second opinion |
| `.claude/settings.json` | permissions (gates, git, pnpm, Playwright) and denials (`--no-verify`, force-push, `.env`) |
| `scripts/next.mjs` | **`node scripts/next.mjs`** — "where am I in the book?" |
| `scripts/check-docs.mjs` | docs integrity: fences, tables, anchors, §-refs, packet fields |
| `scripts/check-fr-coverage.mjs` | all 241 requirements have exactly one owner step |
| `scripts/check-steps.mjs` | the registry vs. reality; `--slices`, `--granularity`, `--strict` |
| `scripts/gen-slices.mjs` | regenerates the slice queue from `spec.md`; `--check` fails CI on drift |
| `scripts/check-commit-msg.mjs` | the commit-message rule, wired as a `commit-msg` hook |
| `scripts/hooks/doc-gate.mjs` | runs the docs gate after any doc edit inside a Claude session |

---

## 2. The serial build order — 61 chapters in 4 acts

This is the answer to "what do I do first". It is computed from the dependency graph, so it is the *only*
safe order: each chapter only needs things above it.

```bash
node scripts/next.mjs            # what to do now, with its slices and commands
node scripts/next.mjs --order    # the full order, with current state
node scripts/next.mjs --all      # only what is unblocked right now
```

| Act | Chapters | What is true at the end | Agent-days |
|---|---|---|---|
| **I — Foundations** | 1–14 · S0.1–S0.14 | It boots, it is deployed, it has a database, a design system, auth, RBAC, RLS, an audit chain, background jobs, a brand profile, security headers, backups, and four frozen contracts | 22 |
| **II — Money in** | 15–35 · S1.1–S1.21 | A merchant onboards, an invoice is issued, a card payment is taken through a processor, the ledger records it, a receipt goes out, a payout is approved — **a real product** | 79 |
| **III — Money out and scale** | 36–53 · S2.1–S2.18 | Disputes, reserves, subscriptions, reports, SDKs, WooCommerce, support, compliance, polish | 90 |
| **IV — Enterprise** | 54–61 · S3.1–S3.8 | Multi-processor routing, FX, tax reporting, passkeys, WORM audit, enterprise scale | 62 |

### The 61 chapters

`Days` is the agent estimate for the whole chapter; `Slices` is how many commits it should take.

| # | Step | Days | Slices | Milestone | Chapter title |
|---|---|---|---|---|---|
| 1 | **S0.1** | 1.0 | 1 | M0 | Repository scaffold and toolchain |
| 2 | **S0.2** | 0.5 | 1 | M0 | CI quality gates |
| 3 | **S0.3** | 1.0 | 1 | M0 | Database bootstrap (extensions, schemas, roles) |
| 4 | **S0.4** | 2.0 | 7 | M1 | Design tokens, primitives and app shells |
| 5 | **S0.5** | 1.5 | 4 | M2 | Data access layer (postgres.js, tenant transactions, money safety) |
| 6 | **S0.6** | 2.5 | 9 | M2 | Authentication with opaque server-side sessions |
| 7 | **S0.7** | 2.0 | 7 | M2 | RBAC: roles, permissions, guards, action wrapper |
| 8 | **S0.8** | 2.5 | 7 | M3 | RLS foundation, exposure rules and isolation harness |
| 9 | **S0.9** | 2.0 | 5 | M3 | Audit log with hash chain and signed checkpoints |
| 10 | **S0.10** | 2.0 | 7 | M4 | Outbox, job worker, scheduler, feature flags |
| 11 | **S0.11** | 1.5 | 6 | M4 | Platform profile (white-label) and public shell |
| 12 | **S0.12** | 1.5 | 6 | M4 | Security headers, CSP, edge controls, no-theater audit |
| 13 | **S0.13** | 1.0 | 1 | M5 | Operations baseline: backups, restore drill, runbooks, incident |
| 14 | **S0.14** | 1.0 | 1 | M5 | Interface freeze: the four contracts every later step imports |
| 15 | **S1.1** | 2.0 | 8 | M6 | Merchants, profiles, settings, limits, provisioning |
| 16 | **S1.2** | 3.0 | 7 | M6 | Onboarding wizard and secure document upload |
| 17 | **S1.3** | 3.0 | 9 | M6 | Admin KYB review, lifecycle controls, tax forms |
| 18 | **S1.4** | 2.5 | 6 | M6 | Bank accounts, verification and change protection |
| 19 | **S1.5** | 4.0 | 9 | M7 | Ledger core: accounts, posting, immutability, hash chain |
| 20 | **S1.6** | 2.5 | 6 | M7 | Plans, fee schedules and the fee engine |
| 21 | **S1.7** | 4.0 | 8 | M8 | Customers, invoices, numbering, tax lines |
| 22 | **S1.8** | 3.0 | 7 | M8 | Invoice PDF with security design |
| 23 | **S1.9** | 4.0 | 8 | M9 | Payment links and the hosted checkout page |
| 24 | **S1.10** | 3.0 | 7 | M9 | Processor adapter interface + sandbox + Stripe/Airwallex skeletons |
| 25 | **S1.11** | 5.0 | 7 | M9 | Payment completion: verification, locking, ledger, receipt |
| 26 | **S1.12** | 3.0 | 7 | M10 | Inbound and outbound webhooks |
| 27 | **S1.13** | 3.0 | 6 | M10 | Refunds, credit memos, negative-balance protection |
| 28 | **S1.14** | 4.0 | 9 | M10 | Payouts: eligibility, scheduling, approvals, receipts |
| 29 | **S1.15** | 5.0 | 10 | M11 | Merchant portal screens |
| 30 | **S1.16** | 5.0 | 7 | M11 | Admin console core |
| 31 | **S1.17** | 5.0 | 7 | M11 | The 17 CMS pages, legal versions, SEO |
| 32 | **S1.18** | 3.0 | 7 | M11 | Notifications and email infrastructure |
| 33 | **S1.19** | 5.0 | 7 | M12 | Public REST API v1, API keys, OpenAPI |
| 34 | **S1.20** | 4.0 | 6 | M12 | Statements, reconciliation (manual), daily close |
| 35 | **S1.21** | 6.0 | 8 | M12 | End-to-end hardening and the Phase 1 gate |
| 36 | **S2.1** | 6.0 | 9 | M13 | Disputes: intake, fund freeze, evidence, outcomes, ratio |
| 37 | **S2.2** | 4.0 | 7 | M13 | Reserves, negative balances, dunning, write-off |
| 38 | **S2.3** | 4.0 | 5 | M13 | Ledger operations: adjustments and period close |
| 39 | **S2.4** | 5.0 | 6 | M14 | Plans, subscriptions, entitlements and fee reporting |
| 40 | **S2.5** | 3.0 | 5 | M14 | Tax scale: reports, exemptions, jurisdiction data |
| 41 | **S2.6** | 5.0 | 6 | M14 | Reports, exports and statements at scale |
| 42 | **S2.7** | 6.0 | 6 | M14 | SDKs, public API docs and sandbox simulator |
| 43 | **S2.8** | 8.0 | 8 | M14 | WooCommerce plugin v1 |
| 44 | **S2.9** | 6.0 | 8 | M14 | CMS finalize: blog, media, navigation, legal, docs |
| 45 | **S2.10** | 4.0 | 6 | M15 | Support system: tickets, SLA, CSAT |
| 46 | **S2.11** | 4.0 | 6 | M15 | Email at scale: promotional separation, templates, delivery logs |
| 47 | **S2.12** | 6.0 | 6 | M15 | Compliance at scale: KYC, ongoing monitoring, periodic review |
| 48 | **S2.13** | 4.0 | 6 | M15 | Catalog and invoice extras |
| 49 | **S2.14** | 5.0 | 6 | M15 | Payment extras: wallets, partial capture, retries, offline payments |
| 50 | **S2.15** | 5.0 | 5 | M16 | Admin consoles: risk, finance, processors, countries |
| 51 | **S2.16** | 6.0 | 7 | M16 | UX scale: dark mode, full Bangla parity, a11y and performance gates |
| 52 | **S2.17** | 3.0 | 5 | M16 | Activity feed, retention and DSAR |
| 53 | **S2.18** | 6.0 | 7 | M16 | Phase 2 hardening, pentest and load |
| 54 | **S3.1** | 8.0 | 9 | M17 | Multi-processor routing and failover |
| 55 | **S3.2** | 10.0 | 12 | M17 | FX and cross-border payouts |
| 56 | **S3.3** | 10.0 | 12 | M18 | Tax reporting: 1099-K / 1042-S, withholding, engine adapter |
| 57 | **S3.4** | 5.0 | 5 | M18 | Passkeys (WebAuthn) and stronger MFA |
| 58 | **S3.5** | 5.0 | 5 | M18 | Bank confirmation matching |
| 59 | **S3.6** | 4.0 | 5 | M18 | Audit WORM export and 7-year retention |
| 60 | **S3.7** | 5.0 | 6 | M19 | Lifecycle marketing, digests and scheduled reports |
| 61 | **S3.8** | 15.0 | 15 | M19 | Enterprise readiness and scale |

---

## 3. The 20 milestones (what to aim at, not just what to type)

A chapter is a unit of *work*. A milestone is a unit of *progress you can show someone*. Ship a milestone, then
celebrate; that is what keeps a 6-month build survivable.

| Milestone | Chapters | You can now demonstrate | Days |
|---|---|---|---|
| **M0** A skeleton that boots | S0.1–S0.3 | a deployed URL, a green CI, a database with roles | 2.5 |
| **M1** A design foundation | S0.4 | `/design` gallery at 360/768/1440, every primitive, every status badge | 2 |
| **M2** Safe data access and identity | S0.5–S0.7 | sign up, sign in, session cookie, roles enforced server-side | 6 |
| **M3** Isolation and an audit trail | S0.8–S0.9 | a foreign tenant's row returns 404; every mutation leaves a hash-chained entry | 4.5 |
| **M4** Background work, brand, perimeter | S0.10–S0.12 | a job runs from the outbox; the logo/address/footer are data; CSP blocks an injected script | 5 |
| **M5** Operations and frozen contracts | S0.13–S0.14 | a restore drill passes; the four contracts are frozen and their test is red when renamed | 2 |
| **M6** A merchant can onboard | S1.1–S1.4 | KYB submission with documents, admin approval, bank account added | 10.5 |
| **M7** Money can be recorded | S1.5–S1.6 | a double-entry ledger that refuses to be edited, and fee math that matches the schedule | 6.5 |
| **M8** An invoice can be issued | S1.7–S1.8 | invoice with tax lines and a security-printed PDF with watermark and QR | 7 |
| **M9** A payment can be taken | S1.9–S1.11 | hosted checkout → processor sandbox → webhook → ledger → receipt, exactly once | 12 |
| **M10** Money can move back and out | S1.12–S1.14 | refund, outbound webhook with signature, payout with approval and receipt | 10 |
| **M11** The product is usable | S1.15–S1.18 | merchant portal, admin console, 17 CMS pages, transactional email | 18 |
| **M12** Integrable and trusted | S1.19–S1.21 | REST API v1 + OpenAPI, statements, reconciliation, Phase 1 gate green | 15 |
| **M13** It survives reality | S2.1–S2.3 | a dispute with evidence and a fund freeze; reserves, dunning, period close | 14 |
| **M14** The business can grow | S2.4–S2.9 | subscriptions, tax reports, exports, SDKs, WooCommerce, CMS blog | 33 |
| **M15** It operates itself | S2.10–S2.14 | support tickets with SLA, email at scale, monitoring reviews, payment extras | 23 |
| **M16** Polished and hardened | S2.15–S2.18 | dark mode, full Bangla, a11y and perf gates, pentest and load test | 20 |
| **M17** Many processors, many corridors | S3.1–S3.2 | routing and failover across processors, FX and cross-border payouts | 18 |
| **M18** Tax and trust at the edges | S3.3–S3.6 | 1099-K/1042-S, passkeys, bank confirmation matching, WORM audit export | 24 |
| **M19** Growth and enterprise | S3.7–S3.8 | digests, scheduled reports, enterprise readiness | 20 |

**Two honest checkpoints.** After **M9** you have a demo that can take a real sandbox payment — this is when you
show it to a design partner. After **M12** you have a product you could put in front of a paying merchant.

---

## 4. The serial procedure, step by step

One slice at a time. This is the whole method; everything else in this book supports it.

### Step 0 — Start of a session (2 minutes)

```bash
cd codekdi2026
git pull --rebase
node scripts/next.mjs               # what is next, what it needs, what to type
node scripts/check-docs.mjs         # is the repo healthy?
claude
```

If `check-docs` is red, fix that first. A red gate on `main` means someone (probably an agent) drifted; do not
build on it.

### Step 1 — Preflight (1 minute)

```text
node scripts/check-steps.mjs S0.6
```

Look at three things: are its `depends_on` steps `done`? are all its slices `reviewed`? which slice is next?
If any slice is `reviewed: false`, **you cannot start** — that is rule G5, enforced by `--strict`. Your job
first is to read those slices and mark them reviewed (or split them if they are not one day's work).

### Step 2 — Kickoff (5 minutes, then you approve)

```text
/kickoff S0.6.3
```

Claude restates the slice in six lines and proposes a plan. You check exactly three things:

1. **Is this the slice?** Compare with the title in `docs/slices.json`.
2. **Is the test named, and would a user notice it failing?**
3. **Is anything invented** — a table, a route, an env var, a package — that the spec does not have?

Three yeses → type `go`. One no → correct it in one sentence and wait for a new plan. **This is the highest
leverage 60 seconds in the entire project**, because plans are cheap to fix and code is not.

### Step 3 — Red (10–30 minutes)

Claude writes the test the slice names and pastes the failure. **Read the failure.** A test that fails for the
wrong reason ("cannot find module") has proven nothing. You want a failure that says the behaviour is missing.

### Step 4 — Build (1–3 hours)

Claude implements. Your job during this phase:

- let it run; do not interrupt for style
- if it says "I need to also change X", that is a scope question: is X part of this slice or the next? Usually
  the next.
- if it hits the same error twice, invoke the two-strike rule (below)

### Step 5 — Gate (2 minutes)

```text
/verify S0.6.3
```

Runs the slice's gate, then breaks the implementation to prove the test can fail, then runs the four plan gates.
You read the pasted output, not a summary. If it says `VERDICT: green`, continue.

### Step 6 — Look at it (3 minutes, UI slices only)

```text
/ui /app/invoices
```

Claude opens the page in a real browser at 360 / 768 / 1440, reads the screenshots, and lists what is actually
broken. **Never accept "responsive" as a claim.** The screenshots are the evidence.

### Step 7 — Review (5 minutes, and mandatory for money/auth/tenancy)

Open a **second** Claude session (different terminal, `/clear`, ideally a different model) and run:

```text
/review
```

Then answer its verdict: `SHIP`, `FIX-FIRST`, or `FALSE-DONE`. `FALSE-DONE` means the agent claimed something
that is not true — stop and redo the slice from Step 3.

### Step 8 — Ship (1 minute)

```text
/ship S0.6.3
```

One commit, correct message, PR body template with evidence and a rollback line. Then `/clear` before the next
slice. **Fresh context every slice** — this is the single cheapest reliability improvement available.

### Step 9 — Close the chapter (only when every slice is done)

1. Run the chapter's `**Verify:**` command from `spec.md` and paste it into `docs/PROGRESS.md`.
2. Run the proof query from the packet (a `select` showing the ledger balances or the audit chain).
3. Do the adversarial pass for that chapter (§7 below).
4. Update `docs/steps.json`: `"status": "done"` — **you**, not the agent. The agent is not allowed to.
5. Say it out loud: what can the product do now that it could not do before?

---

## 5. What "optimal" looks like with an AI agent

Same model, same repo, wildly different results. The difference is entirely in how you supervise.

### 5.1 Context discipline — the biggest lever

| Do | Don't |
|---|---|
| One slice per session | "build the invoicing module" |
| `/clear` after every slice | carry a 300-message session across three chapters |
| Let the packet tell you which spec sections to read | paste the whole master spec "for context" |
| Re-read a file before editing it | assume the agent remembers its exact contents |
| Ask for a plan before code | ask for 6 files at once |

An agent with a clean context and a precise slice is dramatically better than a brilliant agent drowning in
irrelevant text. This is why the repo is split into 402 slices: the split *is* the context management.

### 5.2 The three questions that separate real work from theatre

Ask them, require pasted answers:

```text
1. Paste the test failing BEFORE you wrote the implementation.
2. Delete one line of the implementation and show me that test going red. Restore it.
3. Show me the database row / ledger balance / email / screenshot that proves it happened.
```

An agent that cannot produce (1) wrote the test after the code. One that cannot produce (2) wrote a test that
asserts whatever the code happens to do. One that cannot produce (3) has proven nothing at all.

### 5.3 When the agent is stuck — the two-strike rule

Attempt 1: normal. Attempt 2: allowed. **Attempt 3: forbidden.**

```text
Stop. Do not try again. Write down: the exact command, the exact output, and the two things you tried.
Then read docs/TROUBLESHOOTING.md and tell me which symptom family this matches.
```

An agent that keeps guessing burns your budget and makes the diff worse. Ten minutes of diagnosis beats an hour
of thrashing, and the ladder in `TROUBLESHOOTING.md` is ordered so the cheapest checks come first.

### 5.4 Prompt patterns that work

**Narrow the blast radius** — say what may change, and require a stop if anything else must:

```text
Implement only src/lib/ledger/post.ts and its test. If anything else needs to change, stop and tell me why.
```

**Make lying hard** — demand artefacts, not adjectives:

```text
Do not tell me it works. Paste the command output and the database row.
```

**Force the trade-off into the open**:

```text
You have two options here. Name both, say which you recommend and why, then wait.
```

**Prevent test-weakening**:

```text
If a test fails, fix the code. You may not edit, skip, or delete an existing test to make it pass.
```

**Use a second agent as an adversary** (§7.3) rather than asking the author to grade its own homework.

### 5.5 What to spend your own attention on

You cannot read every line, and you should not try. Read these five things and nothing else:

1. the plan at Step 2 (60 seconds, catches most defects)
2. the pasted failing test at Step 3
3. the diff **stat** (`git diff --stat`) — files and line counts reveal scope creep instantly
4. the gate output at Step 5
5. the screenshots at Step 6

That is roughly 5 minutes of human attention per slice. It is what makes 402 slices tractable.

---

## 6. How to test *this* project — function by function

Generic advice ("write tests") is useless here. Payment software has a specific hierarchy of trust, and each
rung answers a different question. A slice declares which rung it reaches; a money slice that stops at rung 2
is not done.

| Rung | Question it answers | Command | Use it for |
|---|---|---|---|
| 1 | Does it even type-check? | `pnpm typecheck` | every slice; catches invented fields and wrong shapes |
| 2 | Is the logic right in isolation? | `pnpm test` | money parsing/formatting, fee math, state machines, risk rules, normalisers |
| 3 | Does it work against a real database? | `pnpm test:integration` | triggers, constraints, locks, idempotency, RPCs, jobs |
| 4 | Can another tenant see it? | `pnpm test:rls` | every table, every role, every tenant-scoped query |
| 5 | Does the processor agree with us? | `pnpm test:contract` | adapters, webhook payloads, API schema |
| 6 | Does it work in a real browser? | `pnpm test:e2e` | the six critical journeys × three breakpoints × EN/BN |
| 7 | Is it accessible? | inside E2E (axe) | zero serious violations on critical flows |
| 8 | Does it hold under load? | `pnpm test:load` | checkout 50 rps p95 < 1.5 s |
| 9 | Can a human see it happened? | a proof query | ledger balances, audit chain, PDF artefact, email |

### 6.1 The six critical journeys (what E2E must cover)

These are the only journeys that must never break. Everything else is tested at a lower rung.

1. **Sign up → verify email → sign in → step-up 2FA.**
2. **Onboard**: submit KYB with documents → admin approves → merchant can take payments.
3. **Invoice → checkout → pay → receipt → ledger entry** — the money path, exactly once.
4. **Refund** a settled payment, with the credit memo and the reversing ledger entry.
5. **Payout**: request → approve → processor call → receipt → statement reflects it.
6. **Dispute**: intake → evidence upload → submit → outcome moves funds correctly.

If you are ever unsure whether the product works, run those six. They are the product.

### 6.2 The tests that matter most in a PayFac (and are usually skipped)

| Test | Why it is the one that saves you |
|---|---|
| **Double-submit the same invoice** (two tabs, same second) | proves the DB-level lock and the partial unique index — the classic double-charge bug |
| **Replay a webhook** with the same `event_id` | proves dedupe; without it, every retry posts money twice |
| **Foreign id in the URL** (`/app/invoices/<someone-else's>`) | must be **404**, not 403 and never 200 — proves tenant scoping |
| **`typeof amount === 'string'`** | one `Number()` anywhere turns cents into floats and the ledger stops balancing |
| **Refund more than the captured amount** | must be refused by a constraint, not by a UI check |
| **Unknown processor decline code** | must map to `requires_review`, never to success |
| **Edit/delete a ledger row** | must be rejected by a trigger; corrections are reversing entries |
| **Tamper with the amount in devtools** | server recomputes from the invoice, never trusts the client |

Every one of these is a test a competent agent will skip unless you ask. Ask at review: *"show me the test that
blocks a double payment"*. If it cannot point at one, the slice is not done.

### 6.3 How to test when the feature is mostly UI

You cannot unit-test "it looks right". You test it in this order:

1. **tokens** — a test that no page file contains a raw hex colour or an arbitrary px spacing (grep in CI).
2. **states** — for every list/detail screen: empty, loading, error (with a `request_id`), success, disabled.
   An agent will build the success state and forget the other four. Ask for screenshots of each.
3. **breakpoints** — `/ui` at 360 / 768 / 1440; overflow, overlap, tap targets ≥ 44 px.
4. **keyboard** — tab order, visible focus, skip-link, and the form's error announcement.
5. **locale** — Bangla at 320 px; it runs ~30 % longer than English and will break a layout designed only in EN.
6. **screenshots** — `pnpm shots /design` writes them to `tests/visual/out/` so you can *see* the diff.

---

## 7. How to find and fix what the agent missed

It will miss things. The question is whether you find out in 10 minutes or in month three.

### 7.1 The weekly audit (30 minutes, do not skip)

Pick five slices shipped this week and check them at random:

| Check | How | If it fails |
|---|---|---|
| Scope | `git show --stat <sha>` — files match the slice? | note it; tighten `/kickoff` next time |
| Test is real | delete one line of the implementation, run the test | rewrite the test with the agent, then re-verify |
| Nothing skipped | `grep -rn -e "\.skip" -e "\.only" -e "no-verify" src tests` | fix immediately; a skipped test is a lie |
| Money is a string | `grep -rn -E -e "Number\(" -e "parseFloat" -e "toFixed\(" src --include=*.ts` | any hit near money is a blocker |
| Tenancy | is every query scoped to `merchant_id`? | run `pnpm test:rls`, add the missing case |

Five slices, thirty minutes, once a week. This is how you catch systematic drift before it becomes the codebase.

### 7.2 The symptom → cause ladder

When something is wrong, do not let the agent guess. Use the ordered checks in
[`TROUBLESHOOTING.md`](TROUBLESHOOTING.md): empty results (RLS, session, grants), wrong money (string vs
number, exponent, rounding, timezone), stuck payment (state, webhook, worker, ledger guard), double post
(idempotency, lock, dedupe), missing webhook (queue, signature, SSRF), dead job (cron, lease, flags), bad PDF
(template version, font), random sign-out (cookie flags, supabase-js), local-vs-Vercel (Edge runtime, pooler),
CI-only failure (clock, seeds, ordering).

Each family has an ordered list, cheapest check first. That ordering is the whole value: it stops the agent from
"investigating" the ledger when the real problem is a missing `GRANT`.

### 7.3 The repair procedure (when you find a real defect)

Never let an agent fix a bug by editing the code it just wrote, unsupervised — that is how tests get bent to
match bugs. Use this order:

1. **Freeze** — if money moved or a tenant could see another's data, stop the bleeding first:
   `payouts_enabled = false` or flip the feature flag. Correctness before diagnosis.
2. **Reproduce in a test.** The fix starts with a red test that fails for the *right* reason. No test, no fix.
3. **Fix the code, never the test.** If the test genuinely encoded a wrong expectation, that is a rule change:
   ADR + master-spec decision, not a quiet edit.
4. **Check the neighbours.** A bug in `postLedger` usually exists in every caller. Grep for the pattern,
   not just the instance.
5. **Add the row.** If the symptom was new, add it to `TROUBLESHOOTING.md`; if it is a class of bug, add a
   pitfall to `spec.md` §11. This is how the repo gets smarter than the people using it.
6. **Write the regression test** in the layer that would have caught it — usually one rung higher than where
   it appeared.

### 7.4 The three false-fixes to reject on sight

| The agent says | Why it is false | What to do instead |
|---|---|---|
| "I added a try/catch so it doesn't crash" | the error is now invisible, not fixed | find the cause; catch only at boundaries and re-throw typed errors |
| "I updated the test to match the new behaviour" | the test was the specification | decide which is right *before* changing either |
| "It works now" (after an unexplained change) | coincidence, caching, or a stale build | revert the change, prove the test fails, re-apply deliberately |

---

## 8. Getting a second AI to check the first one

An agent reviewing its own work shares its blind spots. The fix is structural, not more prompting.

### 8.1 The three-seat model

| Seat | Who | Access | Job |
|---|---|---|---|
| **Builder** | Claude session 1 | full write | implement one slice |
| **Reviewer** | Claude session 2 (fresh context; a different model family is better) | **read-only** | find what the builder rationalised away |
| **Adversary** | Claude session 3 or a human in a browser | no source, staging credentials | behave like a hostile user and try to break it |

### 8.2 Running the reviewer

```bash
claude            # second terminal, in the same repo
/review           # wired to .claude/agents/reviewer.md
```

It answers six questions: **scope, truth, tests, money, tenancy, honesty** — and returns `SHIP`, `FIX-FIRST`
or `FALSE-DONE`. Two rules make it useful:

- **Read-only.** The reviewer must not fix anything. The moment it edits, it stops being independent.
- **A different model family when possible.** Same-model review catches typos; cross-model review catches
  assumptions.

### 8.3 What to ask when you want a specific answer

```text
Review this diff as an auditor, not an author. Your job is to find the one thing that will lose money.
Start with: can this post twice? Then: can another tenant see it? Then: is any amount a float?
If you find nothing, tell me exactly what you tried to break and why it held.
```

```text
You are a hostile merchant. You have a login to staging. Try to:
pay the same invoice twice in two tabs; open another merchant's invoice by editing the URL;
replay a webhook; tamper with the amount in devtools; use the back button after paying.
Report only what you observed, not what you think of the code.
```

### 8.4 When the two agents disagree

This is the most valuable moment in the whole process — do not resolve it by asking the louder one.

1. Write both claims down, with the file and line each is about.
2. Ask the **master spec** which one is right. It is the arbiter, not seniority.
3. If the spec is silent, that is a gap: `docs/OPEN_QUESTIONS.md` and a human decision.
4. Record the outcome as an ADR if the decision will bind future work.

### 8.5 The one rule that makes cross-checking work

**The reviewer never sees the builder's reasoning.** Not the plan, not the summary, not "here is why I did it
this way". Give it the diff, the packet, and the FR list. A reviewer primed with the author's rationale reviews
the rationale, not the code.

---

## 9. Working with gateways and processors from day one

You are a PayFac/MOR on top of somebody else's licence, so the processor boundary is your most important
interface. The plan treats it that way: one frozen `PaymentProcessor` interface (S0.14, master spec §4.1), one
normalisation target for events, one place vendor SDKs may be imported.

### 9.1 The rules, in the order they bite

1. **Never import a vendor SDK outside `src/lib/processors/`.** Business logic does not know which processor it
   is talking to. A diff that breaks this is a blocker.
2. **A decline is data, not an exception.** `{ ok: false, code, declineClass, retryable }`.
3. **Unknown status or decline code → `requires_review`.** Never success. There is a test that fails on any
   unmapped code.
4. **Idempotency key derives from the payment, not the attempt.** Otherwise a retry charges twice.
5. **Verify webhooks on the raw body**, before parsing; dedupe on `(processor, event_id)`.
6. **A timeout is not a failure.** After 10 s (auth/capture) or 30 s (refund/payout), call
   `getPaymentIntent`/`getPayout` and find out what actually happened.
7. **Capabilities are data.** If the processor cannot do instant payouts to Malaysia, the UI must not offer it.
8. **Reconcile daily.** Settlement report vs. ledger; a mismatch is an alert, never a manual guess.
9. **One merchant = one home processor**, with a documented migration path. A merchant's ledger is
   processor-agnostic.
10. **Sandbox parity.** The same contract test matrix runs against sandbox, recorded fixtures, and one
    live-mode smoke transaction in staging.

### 9.2 Adding a processor

```text
/adapter airwallex
```

The command implements the interface as it exists, writes the contract test first, records fixtures (success,
three decline classes, 3DS, timeout-then-fetch, partial refund, replayed webhook), maps decline codes, registers
capabilities, and proves one sandbox payment end to end with the webhook replayed twice landing once in the
ledger.

### 9.3 What "processor friendly" means in review

Ask these and demand a file or a test for each:

- where is the idempotency key generated? (`grep -rn idempotencyKey src/lib/processors`)
- show me the test where an unknown decline code maps to `requires_review`
- show me the webhook signature verification happening on the raw body
- show me the timeout path calling `getPaymentIntent` instead of assuming failure
- show me the capability check that hides an unsupported payout rail
- show me the reconciliation report matching the processor's settlement file

If any of these has no answer, the integration is a demo, not an integration.

---

## 10. The 90-day plan (what to actually do, week by week)

| Weeks | Chapters | Milestone | Your focus |
|---|---|---|---|
| 1 | S0.1–S0.4 | M0–M1 | toolchain, CI, database, design system. Slow by design — everything after reuses it |
| 2 | S0.5–S0.8 | M2–M3 | data access, auth, RBAC, RLS. **Do not rush this**; tenancy bugs are unfixable later |
| 3 | S0.9–S0.14 | M4–M5 | audit chain, jobs, brand profile, security headers, backups, frozen contracts |
| 4–5 | S1.1–S1.4 | M6 | onboarding, KYB, bank accounts — your first real screens |
| 6 | S1.5–S1.6 | M7 | ledger and fees. The heart. Take the extra day |
| 7 | S1.7–S1.8 | M8 | invoices and the PDF |
| 8–9 | S1.9–S1.11 | M9 | **checkout → processor → ledger → receipt.** The demo moment |
| 10 | S1.12–S1.14 | M10 | webhooks, refunds, payouts |
| 11–12 | S1.15–S1.18 | M11 | portal, admin, CMS, email — where it starts to feel like a product |
| 13 | S1.19–S1.21 | M12 | API, statements, hardening. **Phase 1 gate — a sellable product** |

After chapter 35 you have something a design partner can use and pay with. Everything in Acts III and IV makes
it survive scale, disputes, tax and enterprise buyers.

---

## 11. When things go wrong (the short version)

| Situation | Do |
|---|---|
| Gate red on `main` | stop feature work; fix it today. A decorative gate is worse than none |
| Agent claims done, no output | `/verify`, then the three questions (§5.2) |
| Same error twice | two-strike rule (§5.3), then the symptom ladder |
| Money is wrong in production | freeze payouts first, then find the posting. Never edit ledger rows — post a reversal |
| A tenant saw another tenant's data | treat as an incident: runbook `suspected-breach.md`, even if you think it is small |
| The plan is wrong | plan defect → fix in a separate commit (fast lane). Rule change → stop, `OPEN_QUESTIONS.md`, ADR |
| A slice is going sideways | `git reset --hard HEAD` and re-cut it smaller. Losing 40 minutes beats merging a mess |
| You feel lost | `node scripts/next.mjs`, then re-read `COMPONENTS.md` — not the whole spec |

---

## 12. The compact version (print this)

```text
Every session:
  node scripts/next.mjs            → what is next
  /kickoff <slice>                 → plan; approve only if it is the right slice, the test is named,
                                     and nothing is invented
  (test fails first)               → read the failure, not the summary
  build                            → let it run; scope changes are questions, not decisions
  /verify <slice>                  → gate + "delete a line, watch it go red" + plan gates
  /ui <route>                      → for any screen: 360 / 768 / 1440, look at the images
  /review                          → second session, read-only, six questions
  /ship <slice>                    → one commit, Slice: trailer, evidence in the PR
  /clear                           → fresh context for the next slice

Every week:
  five random slices: scope, is the test real, nothing skipped, no float money, tenancy scoped
  node scripts/check-*             → all four gates green

Every chapter:
  the packet's Verify command, the proof query, the adversarial pass, then status: done (by you)

Never:
  start a slice that is not reviewed · let an agent mark a step done · skip /ui on a UI slice
  edit a test to make code pass · use --no-verify · read the whole spec · work two slices in one context
```
