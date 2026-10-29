# Agent Playbook

> How to run this build with an AI agent, and how to prove the work is real.
> Companion to `spec.md` (the build plan) and `docs/MASTER_SPECIFICATION.md` (the rules).
> This file answers three questions: **which agent**, **what the working procedure is**, and **how you verify it**.

---

## 0. The short version

1. **The agent you pick matters far less than three things**: a spec that removes ambiguity (done), tests that can actually fail (per step), and a reviewer that is not the same session that wrote the code (this file).
2. **Best fit for the builder seat:** a *repo-native terminal agent* that can edit files, run commands, read test output, and loop — Claude Code or Codex CLI class. Chat-only assistants cannot do this job; IDE autocomplete cannot either.
3. **Never let the author be the only reviewer.** Every step gets a second session, a different model family, with no write access: read the diff, try to break it.
4. **"It compiles" is not evidence.** A step is done when five artefacts exist (§5): code, a test that fails without the code, pasted verify output, a database-level proof, and a human-visible demo.
5. **One step per session.** 60 steps, 252 agent-days of estimated work. Small, gated, committed increments beat one heroic prompt every time.

The uncomfortable truth: an AI agent will happily hand you a green build that cannot take a payment. The rest of this document is how to make that outcome unlikely.

---

## 1. What makes an agent fit for *this* job

This project is not "write a landing page". It is: read a long spec, create a migration, write domain code, run a database, fix failing tests, and never leak a tenant's data. The requirements that follow from that:

| Capability | Why it is load-bearing here | Deal-breaker if missing |
|---|---|---|
| Terminal execution + reading output | Migrations, `psql`, test runs, `pnpm` — the agent must see real errors, not imagine them | ❌ Yes |
| Multi-file editing in a loop | One step touches 5–15 files | ❌ Yes |
| Long context (≥ 150k) | A step + its master-spec sections + recipes is 20–40k tokens; a diff adds more | ❌ Yes |
| Instruction adherence over creativity | `N-01` (no card data), `N-03` (no float money), RLS rules are not suggestions | ❌ Yes |
| Repo awareness / no invented APIs | Hallucinated `pdf-lib` and PostgREST calls are the #1 time sink | ⚠️ Mitigate with docs-in-repo |
| Deterministic tool use (no flaky shell) | A dropped `psql` invocation silently skips a migration | ⚠️ |
| MCP / plugin support | Supabase, Playwright, GitHub integrations make verification cheaper | ➕ Nice |

Note what is **not** on the list: benchmark scores, "autonomy", marketing demos. A mid-tier model with a tight loop and a strict reviewer beats a frontier model writing unsupervised.

---

## 2. The recommended setup — four seats

| Seat | Who | Access | Job |
|---|---|---|---|
| **Builder** | Claude Code *or* OpenAI Codex CLI (frontier tier model) | Full repo write, shell, local DB | Executes one step per session, produces the five artefacts |
| **Reviewer** | A session in the **other** model family (if builder was Claude, reviewer is GPT/Codex — and vice versa) | Read-only checkout | Reads the diff against the step packet; looks for shortcuts, fake tests, spec drift |
| **Adversary** | Any fresh session, given **no source access** — only the running app + step "Done when" | Browser + sandbox credentials | Tries to make the feature fail as a user/attacker |
| **Human (you)** | You | Everything | Approves the demo, closes business/legal questions, decides go-live |

Why the other *family*: same-model review is correlated — it repeats the same blind spots. A different family catches different classes of error (and its disagreements are the most informative signal you will get).

**Tool notes (verify current versions/pricing before committing — this market moves monthly):**

| Tool | Best for | Watch out for |
|---|---|---|
| **Claude Code** | Builder seat; long multi-file steps, strong at following a strict spec, good terminal loop | Token spend on big steps; insist on one step per session |
| **OpenAI Codex CLI / cloud** | Builder or Reviewer; good at isolated, well-scoped tasks and diff review | Can be terse about what it skipped — demand the evidence block |
| **Cursor (Agent/Composer)** | UI steps (S0.4, S1.15–S1.17) where you want to see the page while it edits | Tends to "improve" things outside scope; keep the diff small |
| **GitHub Copilot coding agent** | Small, well-specified PRs (docs, i18n, CMS copy) | Weak on DB/migration reasoning; never for money code |
| **Aider / Cline (bring your own key)** | Low-cost builder for Tier C steps; full control of model | Manual loop management — you become the orchestrator |
| **Fully-managed agents (Devin-class)** | Delegating whole features while you do something else | Opaque process; you still need the same gates, so the leverage is smaller than it looks |

**Do not** use: chat-only web assistants for implementation (no real execution), IDE tab-completion for domain logic, or any agent without shell access for steps that touch migrations.

---

## 3. Which model tier for which step

Not every step needs the most expensive model. `spec.md` marks each step's effort; this is the reasoning tier:

| Tier | Steps | Why |
|---|---|---|
| **A — frontier reasoning** | S0.5–S0.9 (tenant/RLS/audit/outbox), S0.12, S1.5, S1.11, S1.12, S1.13, S1.14, S1.20, S2.1–S2.3, S2.6, S3.1–S3.3 | Money, isolation, concurrency, compliance. A subtle error here is expensive and hard to see |
| **B — strong general** | S1.1–S1.4, S1.6, S1.7, S1.9, S1.10, S1.16, S1.18, S1.19, S2.4, S2.10, S2.12–S2.17, S3.4–S3.8 | Real domain logic with well-specified contracts |
| **C — fast/cheap, still gated** | S0.1–S0.4, S0.10, S0.11, S0.13, S1.8, S1.15, S1.17, S1.21, S2.5, S2.7–S2.11, S2.18 | Scaffolding, screens, copy, templates, docs — but they still go through the same five artefacts |

For Tier A steps, use the reviewer on the **same** tier (or higher). For Tier C, a Tier B reviewer is fine.

---

## 4. The working procedure

### 4.1 Per-step loop (the only loop that matters)

```text
1. PREFLIGHT   can I start?          → node scripts/check-steps.mjs S1.5
2. BRIEF       assemble the prompt    → §12 template + step packet + FRs
3. PLAN        agent proposes ≤10 lines + file list; you approve or correct
4. BUILD       agent implements in chunks; typecheck after each chunk
5. VERIFY      agent runs the step's Verify command and pastes real output
6. PROVE       the proof query / demo (§6, §7) — not the UI's word for it
7. REVIEW      a second session, other model family, read-only
8. CLOSE       commit with step id, registry → done, PROGRESS entry, handoff note
```

Rules that are not optional:

- **Stop at step 8.** Do not let the same session start the next step. Context carries stale assumptions, and the review gate gets skipped "just this once".
- **Two strikes.** If the same error survives two fix attempts, stop and report: exact command, exact output, what was tried. Thrashing is how agents burn a day.
- **No silent scope.** Any deviation gets written down and approved before it lands.
- **The agent never edits** `spec.md`, `docs/MASTER_SPECIFICATION.md`, `docs/steps.json` status, or the tests of a *previous* step to make the current one pass. That is the single most common failure mode (§8, row 1).

### 4.2 The kickoff prompt (Builder seat)

Paste this, filled in. It is the §12 template plus the anti-shortcut clauses that experience says you need:

```text
ROLE: Implementation engineer for KD PAY (PayFac platform). You write code that must
survive an audit and a chargeback, not a demo.

SOURCES OF TRUTH: docs/MASTER_SPECIFICATION.md (rules) and spec.md (plan).
When they disagree, the master spec wins; report the conflict, do not reconcile it yourself.

TASK: step [S1.11 — payment completion].
READ: spec.md §0, §1, §11, §15 (contracts), §16 (test infra); the S1.11 packet;
master spec [§15.2, §15.6, §16.5–§16.7, §18.1]; recipes §7.3, §7.5, §7.8, §7.9.
DEPENDENCIES: [S1.5, S1.6, S1.7, S1.9, S1.10] are done — verify with `node scripts/check-steps.mjs`.

DELIVERABLES: exactly the files listed in the step packet's Build section, plus the
tests it names. Nothing else. No refactors of neighbouring modules.

HARD RULES (violating any of these fails the step):
- No float money, ever. Micro-USD BigInt in TS, numeric(18,4) in Postgres.
- No new table, column, route, error code, env var, or dependency that is not in the
  spec. If you think one is needed, STOP and ask.
- Every new table: RLS + isolation test + exposure block, in the same change.
- You may not edit spec.md, docs/MASTER_SPECIFICATION.md, or previously-passing tests.
- You may not mark a step done. You report evidence; a human and a reviewer decide.

PROCESS:
1. Output a plan (≤10 lines) and the file list. Wait for approval.
2. Implement in chunks; run `pnpm typecheck` after each chunk (paste the result).
3. Paste the FULL output of the step's Verify command. Not a summary.
4. Provide the proof query result and the demo steps a human can follow in 5 minutes.
5. State any deviation explicitly, or write "none".

ACCEPTANCE (verbatim from the step):
[Done when: 50 parallel completions produce exactly one payment, one ledger
transaction, one receipt.]
```

### 4.3 The review prompt (Reviewer seat, read-only, other model family)

```text
You are reviewing a diff for a payment platform. You did not write it and you are not
allowed to change it.

INPUT: the branch diff, the step packet from spec.md, and the FR list the step owns.

Your job, in this order:
1. SCOPE: does the diff contain anything the step did not ask for? Flag every extra file.
2. TRUTH: does the code do what the step says, using only APIs/tables/routes that exist
   in the spec? Name any invented identifier.
3. TESTS: for each test added, ask "what would I delete to make this test fail?"
   If you cannot answer, the test is decorative — say so.
4. MONEY: trace one payment end to end. Is there any path that posts twice, skips the
   lock, or rounds in JS? 
5. TENANCY: is every query scoped to merchant_id, and does a foreign id return 404?
6. HONESTY: does the "verify output" look like real terminal output? Any step skipped,
   any test name that does not exist in the repo?

Output: BLOCKERS (must fix), RISKS (should fix), NITS (optional), and a one-line
verdict: SHIP / FIX-FIRST / FALSE-DONE.
```

### 4.4 The adversarial prompt (Adversary seat, no source access)

```text
You have a browser and sandbox credentials for staging. You are a hostile user.
Your goal is to prove this feature is fake.

[Feature under test + the step's "Done when" line]

Try, and record exactly what happened:
- pay the same invoice twice, quickly, in two tabs
- open another merchant's invoice id by editing the URL
- replay a webhook payload you already sent
- submit a price/amount that was tampered with in devtools
- submit garbage in every field, and a file with the wrong type
- use the back button after paying
- refresh during the payment step

Report: what you did, what happened, what should have happened. No opinions about
the code — only observed behaviour.
```

---

## 5. The evidence standard — what "done" means

A step is done when **all five** exist. Anything less is "in progress", whatever the agent says.

| # | Artefact | Where it lives | Fails if |
|---|---|---|---|
| **E1** | Code + migration, matching the packet's file list | Git | Extra files, missing files, or `TODO` left |
| **E2** | Tests that **fail without the code** | Git | A test passes with the guarded line deleted |
| **E3** | Verify output, pasted verbatim | `docs/PROGRESS.md` | Summarized, or from a different commit |
| **E4** | Database-level proof (the row, the balance, the 404) | `docs/PROGRESS.md` / review | Proof taken from the UI only |
| **E5** | A 5-minute human demo | You, live | "It should work now" |

E2 is the one people skip. It is also the one that decides whether the project survives. See §6.1.

---

## 6. How to cross-check the work (ordered by leverage per minute)

### 6.1 The break-it test — 2 minutes, catches most fake tests

Ask the Reviewer (or do it yourself) to delete the guard and re-run the test:

```bash
# 1. the test must pass
pnpm test:integration --grep "double payment"

# 2. remove the protection the test claims to cover
#    - delete `for update` from the lock query, or
#    - comment out the unique index in a scratch branch, or
#    - drop ONE RLS policy
pnpm test:integration --grep "double payment"

# 3. the test MUST now fail. If it still passes, the test is theatre.
git checkout -- .
```

Do this for: every RLS policy (S0.8), the ledger balance trigger (S1.5), the double-payment lock (S1.11), refund bounds (S1.13), payout idempotency (S1.14), the audit chain (S0.9). Six checks, ten minutes, and you will find the lies.

### 6.2 Database truth, not screen truth — 3 minutes

Every money feature is verified by querying Postgres, not by trusting a green toast. §7 has the queries. If the UI says "Paid" and `payments` has no row, you found a critical bug — and you found it in staging, not in production.

### 6.3 Cross-family review — 10 minutes

The §4.3 prompt, other model family, no write access. Expect 30–50% of real defects here: invented APIs, a missing tenant filter, a test that asserts on a mock.

### 6.4 Adversarial session — 15 minutes

The §4.4 prompt. The adversary has no source access, so it cannot rationalize — it can only observe. Run it on every step that touches money, auth, or tenancy.

### 6.5 The smoke script — 5 minutes, every deploy

`scripts/smoke.ts` (S1.21) drives a real end-to-end flow on a real sandbox: create merchant → approve → invoice → pay → ledger assertion → refund → payout → statement. It asserts **database state**, not HTML. Run it on every push to staging; if it is red, staging is broken regardless of what the tests say.

### 6.6 Mutation testing on the money core — 20 minutes, monthly

```bash
pnpm add -D @stryker-mutator/core @stryker-mutator/vitest-runner
npx stryker run --mutate "src/lib/money/**/*.ts,src/lib/ledger/**/*.ts"
```

Target: **≥ 95% mutation score** on `src/lib/money` and `src/lib/ledger`. This is the only automated measure of "your tests would notice a bug". Ordinary coverage can be 100% and still prove nothing.

### 6.7 Chaos and negative tests — built into the plan, verify they ran

Duplicate webhooks, out-of-order events, processor timeout, worker crash mid-payout, 50 parallel payments, tampered ledger row, cross-tenant fetch. The packets list these; your job is to confirm the test names exist and that they fail when the protection is removed (§6.1).

### 6.8 The human demo — 5 minutes, per step

You, personally: open two tabs, pay twice, watch what happens; open someone else's id; refund more than captured. It takes five minutes and it is the only check that tests the product rather than the code.

---

## 7. Proof queries for the critical steps

Run these against the dev/staging database after the step. Any query returning rows under "must be empty" is a **blocker**, not a bug report.

**S0.8 — tenancy (must return 0 rows each)**

```sql
-- tables with RLS missing
select c.relname from pg_class c join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relkind = 'r' and not c.relrowsecurity;

-- policies that are not restrictive-by-default (sanity: every table has ≥1 policy)
select c.relname from pg_class c join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relkind = 'r'
  and not exists (select 1 from pg_policies p where p.tablename = c.relname);

-- the runtime role must not be able to bypass RLS
select rolname, rolsuper, rolbypassrls from pg_roles
where rolname in ('app_runtime','app_service');   -- app_runtime: false/false
```

**S1.5 / S1.11 — the ledger is balanced (must return 0 rows)**

```sql
select t.public_id, sum(case when e.direction = 'debit' then e.amount else -e.amount end) as net
from ledger_transactions t join ledger_entries e on e.transaction_id = t.id
group by t.public_id
having sum(case when e.direction = 'debit' then e.amount else -e.amount end) <> 0;
```

**S1.11 — one payment, one ledger transaction, one receipt**

```sql
select count(*) from payments where checkout_session_id = '<session>';                    -- exactly 1
select count(*) from ledger_transactions
 where reference_type = 'payment' and reference_id = '<payment-id>';                      -- exactly 1
select count(*) from email_log where dedupe_key like 'receipt:<payment-id>%';             -- exactly 1
```

**S0.9 — the audit chain is intact and immutable**

```sql
-- must raise: hash chain rejects mutation
update audit.log set action = 'forged' where id = (select min(id) from audit.log);
delete from audit.log where id = (select max(id) from audit.log);

-- chain continuity: every prev_hash equals the previous row's hash (must return 0 rows)
select id from (
  select id, prev_hash, lag(hash) over (order by id) as expected from audit.log
) x where expected is not null and prev_hash is distinct from expected;
```

**S1.13 — refunds cannot exceed capture**

```sql
select p.id, p.amount_captured, p.amount_refunded,
       coalesce(sum(r.amount) filter (where r.status in ('succeeded','processing')), 0) as refunded
from payments p left join refunds r on r.payment_id = p.id
group by p.id
having coalesce(sum(r.amount) filter (where r.status in ('succeeded','processing')), 0) > p.amount_captured;
-- must be empty
```

**S1.14 — no payout paid twice**

```sql
select processor_ref, count(*) from payouts
where processor_ref is not null group by processor_ref having count(*) > 1;   -- must be empty
```

**S3.6 / S0.9 — audit checkpoints verify with an independent path**

```bash
pnpm verify:audit --bundle ./tmp/audit-2026-10.zip   # must print OK with the public key only
```

---

## 8. Failure modes of AI agents on this repo — and the countermeasure

These are observed, not hypothetical. Every one of them has happened on payment projects.

| # | Symptom | How it fools you | Countermeasure |
|---|---|---|---|
| 1 | Agent edits a previous test, or the spec, so the new code passes | Everything is green | Reviewer diffs `spec.md`, `docs/**`, and any pre-existing test file — that diff must be empty |
| 2 | Tests assert on mocks, never touch the DB | High coverage, zero proof | §6.1 break-it test; rule: an integration test that does not open a transaction is a unit test |
| 3 | "Verify output" is written by the model, not pasted from a terminal | Looks like real output | Reviewer checks the test names exist in the repo and the commit hash matches |
| 4 | RLS silently disabled to make a query work | Feature works, tenant isolation gone | `select relrowsecurity` scan (§7 S0.8) in CI, not in review |
| 5 | Invented library API (`pdf-lib`, SimpleWebAuthn, postgres.js) | Compiles if types are `any` | `strict` + `noImplicitAny`; reviewer greps for `as any` / `@ts-ignore` (these need a written justification) |
| 6 | Float money sneaks in via `.toFixed()` or `/ 100` | Amounts look right on small values | Money test with 0.1+0.2 style cases and large values; grep for `toFixed`, `parseFloat`, `/ 100` in `src/features` |
| 7 | Non-idempotent webhook handler | Works in dev, double-pays in production | Replay test (§6.7) must exist and go red when the dedupe is removed |
| 8 | New dependency added "to save time" | Nothing breaks immediately | Dependency rule (spec §18): one-line justification + license check in the PR; reviewer blocks unrequested deps |
| 9 | Scope creep: refactors neighbours, renames contracts | Diff looks tidy | Scope check in §4.3; commit per step keeps the blast radius small |
| 10 | Bengali strings missing or machine-mangled | English looks perfect | `pnpm i18n:lint` key-set equality (S2.16) + screenshot diff per locale |
| 11 | `TODO` / `throw new Error('not implemented')` left in a shipped path | Tests don't cover that branch | grep for `TODO|not implemented|fixme` as a CI gate on `src/**` |
| 12 | Migration edited after it was pushed | Works locally, breaks other environments | CI: migrations are append-only; hash of each file recorded, mismatch fails |
| 13 | Agent "fixes" a failing RLS test by relaxing the policy | Green tests, broken promise | Policy changes require a reviewer + a line in the PR; the break-it test on the *specific* policy |
| 14 | Long session drifts: forgets `N-01`, adds card fields | Plausible-looking checkout | Re-brief per step (§4.2 restates hard rules); reviewer checks the FR list, not just the code |

---

## 9. Red flags — stop the session immediately

- The agent wants to change the spec, the master spec, or a passing test to proceed.
- It reports success without pasting command output.
- It removes a security control "temporarily".
- It adds a dependency you did not approve.
- It says "the rest is straightforward" about money code.
- The diff touches more than ~2× the files in the step packet.
- Coverage or test count **drops** in the same PR.
- It cannot explain, in one sentence, why a specific test would fail if the code were wrong.

When any of these fire: `git stash` nothing, keep the branch, start a fresh session with the reviewer prompt. Do not argue with a drifting session; reset it.

---

## 10. Human gates

| Gate | When | Time | You check |
|---|---|---|---|
| **Step gate** | every step | 5 min | E1–E5 present; §6.1 break-it test done once per security/money control; demo clicked |
| **Weekly gate** | Friday | 45 min | Registry status vs reality; `pnpm check:docs && pnpm check:fr && pnpm check:steps --strict`; smoke on staging; open deviations reviewed; PROGRESS honest |
| **Phase gate** | end of Phase 0/1/2/3 | half day | The gate list at the end of each phase section in `spec.md`, verbatim; restore drill; pentest/load where applicable |
| **Money gate** | before the first real dollar | 2 h | Ledger proof queries, reconciliation on a full sandbox month, payout approved by two humans, refund bounds exercised |

The weekly gate is the one people drop and the one that saves the project. Fifteen minutes against a lying registry beats a month of "it's nearly done".

---

## 11. What to delegate — and what you must never delegate

**Delegate to the agent (with the gates above):** migrations and domain code, tests, UI screens, copy/CMS, email templates, PDF layout, documentation, refactors inside a step, dependency-free scripts, translation drafts (reviewed).

**Never delegate:**

| Thing | Why | Who |
|---|---|---|
| Card-data decisions (`N-01`) | PCI liability is criminal/contractual, not technical | You + acquirer |
| Legal text, KYB/AML policy, sanctions lists | Regulated | Counsel / compliance officer |
| Processor contracts, merchant-of-record model, reserve terms | Money and liability | You + counsel |
| Production credentials, key rotation, DNS | Irreversible | You |
| "Go live" | Only a human can own the consequences | You |
| Approving a payout or a write-off above threshold | Four-eyes is a control, not a UX detail | Two humans |

The agent can *build* the four-eyes control. It must never *be* one.

---

## 12. Cost and schedule realism

| Phase | Steps | Estimated agent-days | Realistic calendar (1 builder session/day + review) |
|---|---|---|---|
| 0 — Foundations | 13 | 21 | 3–4 weeks |
| 1 — Money in | 21 | 79 | 10–12 weeks |
| 2 — Money out & scale | 18 | 90 | 12–14 weeks |
| 3 — Global & enterprise | 8 | 62 | 8–10 weeks |
| **Total** | **60** | **252** | **~8–10 months solo** |

Multiply agent-days by ~1.6 for review, rework and the failures an agent produces. The estimate is per *working* step, not per prompt: a step that takes 3 agent-days will usually take 2–4 sessions.

Cost note: a frontier-model builder on a 3-day step typically consumes on the order of a few million tokens with reviews. Budget it as a real line item (order of magnitude: a few hundred USD per phase-1 month at current frontier prices — verify current rates). Cheap models on money steps are a false economy: rework costs more than the tokens you saved.

---

## 13. Appendix — step review template

Copy into `docs/reviews/S1.11.md` (one file per step; keep them, they are your audit trail).

```markdown
# Step S1.11 — Payment completion
- Commit: <sha>            Branch: arena/…
- Reviewer: <model / session>      Date: YYYY-MM-DD
- Builder session: <model / session id>

## Evidence
- [ ] E1 code + migration match the packet file list (extra files: none / list)
- [ ] E2 test fails without the code — break-it test performed on: <which guard>
- [ ] E3 verify output pasted in PROGRESS.md and matches this commit
- [ ] E4 proof query run: <paste result> → 0 rows / 1 row as expected
- [ ] E5 human demo performed by <name>, result: pass / fail

## Review
- BLOCKERS: …
- RISKS: …
- NITS: …
- Deviations approved: … / none
- Verdict: SHIP / FIX-FIRST / FALSE-DONE

## Notes for the next session
<what is true now, what is still fragile, what to watch>
```
