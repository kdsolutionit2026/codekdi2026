# Building KD PAY with Claude — the operating manual

This is the practical guide: how to sit down, what to type, what to look at, and how to know the work is real.
It assumes you are the human in the loop and Claude does the typing. It is written for **Claude Code** (the
CLI/IDE agent that can read this repo, run commands and drive a browser). Claude in a chat window cannot do
this — it cannot run your tests, so it cannot tell you the truth.

> **The one idea.** You are not asking Claude to build a product. You are asking it to complete a **slice** —
> a task with one seam, one test, one gate command, at most one day of work — and then you are checking the
> **evidence**. Everything below exists to keep that true.

---

## 0. What this repo already gives you (do not recreate it)

| You would normally have to invent | Where it already is |
|---|---|
| What to build, in what order | `spec.md` — 61 step packets, each with exact files |
| What to do in *this* session | `docs/slices.json` — 402 slices, ≤1 day each, with gate + test name |
| The rules | `docs/MASTER_SPECIFICATION.md` — wins every conflict |
| How to verify | each slice's `gate`, each step's `**Verify:**`, `docs/AGENT_PLAYBOOK.md` §5 |
| Where things go wrong | `spec.md` §11 pitfalls, `docs/TROUBLESHOOTING.md` ladder |
| How to add things later | `docs/CHANGE-PLAYBOOK.md` — 12 recipes |
| What Claude should never do | `CLAUDE.md` (auto-loaded), plus 6 slash commands in `.claude/commands/` |

If you find yourself writing a long prompt explaining the project to Claude, stop — `CLAUDE.md` already does
that, and it is loaded automatically in every session.

---

## 1. One-time setup (about 20 minutes)

### 1.1 Local toolchain

```bash
git clone https://github.com/kdsolutionit2026/codekdi2026 && cd codekdi2026
node -v                 # 22+ for the app; 20+ is enough for the plan gates
corepack enable && pnpm -v
docker info >/dev/null && echo "docker ok"      # needed for `supabase start` (S0.2+)
```

### 1.2 Prove the repo is healthy before you touch it

```bash
node scripts/check-docs.mjs                      # 0 problem(s) across 9 file(s)
node scripts/check-fr-coverage.mjs | tail -1     # 241 requirements · 241 owned · 61 steps
node scripts/gen-slices.mjs --check              # docs/slices.json up to date — 402 slices
node scripts/check-steps.mjs --strict            # exit 0
git config core.hooksPath .githooks              # the commit-message check
```

If any of these is red **before** you start, do not start. Something drifted; the gates are telling you.

### 1.3 Give Claude eyes and hands

```bash
npm i -g @anthropic-ai/claude-code     # if not installed
claude                                  # inside the repo — CLAUDE.md loads automatically
```

Inside the session:

```text
claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
```

Then `/mcp` to confirm `playwright` shows **connected**. This is the single most valuable tool in the whole
setup: it lets Claude open your preview, resize to a phone, click through a form and *look* at the result,
instead of describing what it thinks the code renders. A UI claim you cannot see is a guess.

**Verify it works, once:**

```text
Use playwright mcp. Open http://localhost:3000/design after S0.4 lands, resize to 390x844,
screenshot, and tell me every element that is clipped or under 44px tall.
```

If Claude answers "I cannot access a browser", the MCP server did not connect — fix that before you build UI.

### 1.4 Deploy preview (from S0.1 onward)

```bash
pnpm dlx vercel link          # once
pnpm dlx vercel env pull .env.local
```

Every push to a branch gets a **Vercel preview URL**. That is your live preview: the same build your users
would get, on a real domain, with real env vars. Keep the URL of the branch in the PR body so a reviewer can
open it without running anything.

Two previews, two purposes:

| Preview | Command | Use it for |
|---|---|---|
| Local | `pnpm dev` → `localhost:3000` | the fast loop; what Claude drives with Playwright |
| Branch | `git push` → Vercel URL | the honest check: same build, real env, real fonts, real CDN |

---

## 2. The daily loop (one slice at a time)

This is the whole method. Every session, every slice, the same eight steps.

```text
1  PREFLIGHT   node scripts/check-steps.mjs S1.5
2  KICKOFF     /kickoff S1.5.3            → plan + failing test, then STOP for your approval
3  RED         Claude writes the named test first and pastes it failing
4  BUILD       implement until green; typecheck after each chunk
5  GATE        the slice's gate command, < 60 s
6  LOOK        /ui   (Playwright, 360/768/1440) — for anything with a screen
7  REVIEW      /review   in a second, read-only session
8  SHIP        /ship S1.5.3  → one commit, one PR body with evidence
```

### 2.1 What you actually type

```text
/kickoff S0.6.3
```

Claude runs preflight, reads only the packet and the sections it names, restates the slice in six lines, and
proposes a plan. **You read the plan, not the code.** Three questions:

1. Does this match the slice's title in `docs/slices.json`?
2. Is the test named and does it assert something a user could notice?
3. Is anything invented — a table, a route, an env var, a dependency — that the spec does not have?

If all three are fine: `go`. If not, correct it in one sentence. This ten-second check is where most defects
die, because it happens before any code exists.

### 2.2 Why you approve before code

An agent that plans badly will implement the bad plan perfectly. A 200-line diff that should have been 40 is
nearly impossible to spot at the end — but trivially obvious in a 6-line plan.

### 2.3 After each slice

```text
/verify S0.6.3     → gate output, the "break it and watch it fail" proof, plan gates
/review            → a second session, read-only, six questions
/ship S0.6.3       → one commit, correct message, PR body
```

Then **`/clear`**. Start the next slice in a fresh context. A long session accumulates stale assumptions and
Claude starts "remembering" code that no longer exists. Fresh context, one slice, is the cheapest reliability
win available.

### 2.4 Cadence that actually finishes the project

| Rhythm | What happens |
|---|---|
| Slice (~1–3 h with review) | one commit, gate green, `PROGRESS.md` line |
| Every ~8 slices | unit gate: `pnpm test:integration` + migration replay from zero + contract tests (~5 min) |
| End of a step | step `**Verify:**` + proof query + `/review` + human acceptance; step → `done` **by you** |
| End of a phase | release gate: full suite, fuzz, isolation, restore drill, all four plan gates (~30 min) |
| Weekly | read the metrics table in §9; skim `docs/PROGRESS.md` for drift |

---

## 3. Getting "nothing is missed" — the proof ladder

"All functions work" is not a claim, it is a **rung on this ladder**. A feature is only as proven as the
highest rung it has reached, and each rung is cheap to add *at the moment the slice is written* and expensive
to add later.

| Rung | Proof | Command | Catches |
|---|---|---|---|
| 1 | Compiles and types check | `pnpm typecheck` | invented fields, wrong shapes |
| 2 | Unit test fails without the code | `pnpm test` | logic errors, rounding, state machines |
| 3 | Integration test against real Postgres | `pnpm test:integration` | triggers, constraints, locks, idempotency |
| 4 | RLS isolation test | `pnpm test:rls` | a foreign tenant reading your rows |
| 5 | Contract test against the processor sandbox | `pnpm test:contract` | adapter drift, webhook shapes |
| 6 | E2E in a real browser at 3 breakpoints | `pnpm test:e2e` | the feature not being wired to the UI |
| 7 | Proof query / artefact | `select … from ledger_entries` | "it said it worked" |
| 8 | Adversary pass (a hostile user) | `/review` + Playwright | double pay, replay, tampering, broken states |

**The rule you enforce as the human:** every slice declares which rung it reaches. A money slice that stops at
rung 2 is not done. A UI slice that never reached rung 6 is not done.

### 3.1 The three questions that expose fake completion

Ask them every time, and require a pasted answer:

```text
1. Paste the failing test output from BEFORE you wrote the implementation.
2. Delete one line of the implementation and show me the test going red. Restore it.
3. Show me the database row / ledger balance / email that proves this happened.
```

An agent that cannot produce (1) wrote the test after the code. One that cannot produce (2) wrote a test that
asserts whatever the code does. One that cannot produce (3) has not proven anything.

---

## 4. UI and UX — "responsive and user friendly" as a checklist, not a vibe

You cannot review a screen you have not seen, and Claude cannot either. So the loop is: **render it, look at
it, fix what you see** — three times, at three widths.

### 4.1 The visual loop

```text
/ui /app/invoices
```

That command opens the page in a real browser at **360, 768 and 1440**, reads the screenshots, and reports
what is actually broken: overflow, clipped buttons, sub-44 px tap targets, text that fails contrast, missing
empty/loading/error states, a hardcoded brand string.

Do this **before** `/ship` on every UI slice. It costs about two minutes and it is the difference between "the
component exists" and "the screen works".

### 4.2 The checklist the command enforces

| Dimension | Standard | How it is checked |
|---|---|---|
| Layout | no horizontal scroll, no overlap, nothing clipped | screenshot at 360/768/1440 |
| Touch | every interactive target ≥ 44 × 44 px | measured in the browser |
| Type | body ≥ 16 px mobile; Bangla 30 % longer than English, no `uppercase` | BN snapshot at 320 px |
| Contrast | 4.5:1 body, 3:1 large text | axe scan, zero serious |
| States | empty, loading, error (shows `request_id`), success, disabled | you click through them |
| Keyboard | tab order logical, focus always visible, skip-link works | keyboard-only pass |
| Brand | logo, address, footer from the platform profile — **never** hardcoded | grep + a swapped-logo render |
| Money | aligned decimal column, no float, no `$` on non-USD | the design gallery |

### 4.3 The rule that keeps quality from decaying

Every screen is built from `src/components/ui/*` and tokens from `globals.css`. **No page defines a raw hex
colour or a pixel spacing value.** If a screen needs something new, the primitive is added first, in a slice
of its own — otherwise you get 40 bespoke buttons and the UI becomes impossible to change.

Ask for this explicitly at review: *"Show me that no file in this diff contains a hex colour or a raw px
spacing."*

---

## 5. Developer friendly — what that means here, concretely

| Property | Mechanism already in the repo | How to keep it true |
|---|---|---|
| New dev productive in an hour | `CONTRIBUTING.md` | if you had to explain something that is not in it, add a line |
| Predictable structure | `src/app` thin, `features/<domain>` owns logic, `lib/` shared | reject a diff that puts a query in `app/` |
| Typed contracts | S0.14 freeze: money, ledger, processor, events | `/review` question 2: "name any invented identifier" |
| Documented API | OpenAPI 3.1 in S1.19, generated from zod | the spec and the code must be generated from one source |
| Errors you can act on | one error envelope with `request_id` | every error state in the UI shows the id |
| Onboarding by running | `pnpm verify` runs everything | keep it under the time budget in `spec.md` §9.1 |
| Change without fear | 3 gate tiers, 4 plan gates | if a gate is red on `main`, stop feature work |

---

## 6. Gateway / processor friendly — the part that is easiest to get wrong

A payment platform lives or dies on its processor integration. The repo encodes the rules; here is how to
apply them with Claude.

### 6.1 The shape

One interface, frozen in S0.14 and normative in master spec §4.1:

```text
src/lib/processors/
  types.ts      PaymentProcessor + ProcessorCapabilities   ← frozen; do not redesign
  normalize.ts  vendor status/decline code → declineClass  ← table-driven, unknown → requires_review
  sandbox.ts    deterministic fake, default in dev/test
  airwallex.ts  stripe.ts  …                               ← one file per processor
  registry.ts   resolves by merchants.processor_id, asserts capabilities
```

Business logic never imports a vendor SDK. If a diff adds `import … from '@stripe/…'` outside
`src/lib/processors/`, that is a blocker.

### 6.2 Adding a processor

```text
/adapter airwallex
```

The command implements the existing interface, writes the contract test first, records fixtures for success,
three decline classes, 3DS, timeout-then-fetch, partial refund and a replayed webhook — and then proves one
sandbox payment end to end with the webhook replayed twice landing once in the ledger.

### 6.3 The eight checks before a processor is "live-ish"

1. **Idempotency** — every create/capture/refund carries a key derived from the payment, not the attempt.
2. **Declines are data** — `{ ok: false, code, declineClass, retryable }`; never an exception, never a retry loop.
3. **Unknown → `requires_review`** — an unmapped code must never become a success. There is a test that fails
   on any unmapped code.
4. **Webhooks verified on the raw body**, deduped on `(processor, event_id)`, acknowledged in < 2 s, processed
   by the worker.
5. **Timeouts fetch state** — after a 10 s/30 s timeout, call `getPaymentIntent`/`getPayout`; never assume
   failure.
6. **Capabilities are data** — the UI hides a payout rail the processor cannot execute.
7. **Reconciliation** — daily settlement report matched against the ledger; a mismatch is an alert, not a guess.
8. **Sandbox parity** — the same contract matrix runs against sandbox, recorded fixtures and one live-mode
   smoke transaction in staging.

### 6.4 How to talk to Claude about processors

Instead of "integrate Stripe", say:

```text
Implement PaymentProcessor for stripe, in src/lib/processors/stripe.ts only.
Read master spec §4.1 and §4.4 first. Write the contract test first and show it failing.
Map decline codes in normalize.ts — anything unknown must land in requires_review.
Do not change any other file; if you need to, stop and tell me why.
```

The specificity is the point: it makes an out-of-scope change visible instead of invisible.

---

## 7. The ten ways this goes wrong, and the countermeasure

| # | Failure | What it looks like | Countermeasure |
|---|---|---|---|
| 1 | **FALSE-DONE** | "implemented and tested" with no pasted output | rung-1..3 questions (§3.1); `/verify` |
| 2 | **Test written after the code** | a test that asserts exactly what the code does | the three questions; `/verify` step 2 |
| 3 | **Scope creep** | the diff touches invoice UI while fixing a webhook | `/kickoff` file list; `/ship` diff check |
| 4 | **Invented schema** | a column or route the spec does not have | `/review` question 2 |
| 5 | **Money as a float** | one `Number(...)` on an amount | `/review` question 4; a unit test asserting `typeof === 'string'` |
| 6 | **Tenant leak** | a query without `merchant_id`, or 403 instead of 404 | `/review` question 5; `pnpm test:rls` |
| 7 | **UI never looked at** | "responsive" claimed, mobile nav overlapping | `/ui` before every `/ship` on a UI slice |
| 8 | **Context rot** | Claude "remembers" a function that was renamed | `/clear` between slices; never work two slices in one context |
| 9 | **Thrashing** | same error, five attempts, different guesses | two-strike rule: stop, paste command + output, read the ladder |
| 10 | **Gate bypass** | `--no-verify`, a skipped test, `test.skip` | deny rules in `.claude/settings.json`; grep the diff for `skip`/`only`/`--no-verify` |

### 7.1 The two-strike rule

If the same error survives two fix attempts, stop the session. Write down the exact command, the exact output,
and what was tried. Then read `docs/TROUBLESHOOTING.md` — the ladder is ordered cheapest-first and covers the
ten symptom families that account for almost every incident. An agent with a stuck loop and no new information
will burn an hour and make the diff worse.

### 7.2 Revert is a valid move

If a slice is going sideways: `git reset --hard HEAD` and start it again with a smaller cut. Losing 40 minutes
beats merging a mess you will spend two days untangling. Because every slice is one commit, reverting is
always a single command — that is a design property, not luck.

---

## 8. Working with the plan itself (when the plan is wrong)

The plan will be wrong somewhere. That is expected, and it is not a reason to improvise — it is a reason to
use the fast lane.

| You found | Do this |
|---|---|
| A wrong path, a missing dependency, a terse bullet, a bad estimate | **Plan defect.** Fix in the same session, separate commit, keep the four gates green, one line in `PROGRESS.md`. No approval. |
| A rule that is wrong (ledger, money, tenancy, a §15 signature) | **Rule change.** Stop. `docs/OPEN_QUESTIONS.md` → decision → master spec + `spec.md` + registry in one PR. |
| A requirement nobody owns | Stop. It is a plan defect *and* a coverage gap: add the owner, run `check-fr-coverage`. |

Say this to Claude, verbatim, when it wants to "fix" something:

```text
Before you change anything: is this a plan defect or a rule change?
If it changes what the system guarantees, stop and write the question instead of the code.
```

---

## 9. Measuring whether it is working

Track four numbers weekly. They tell you what to change, and none of them require new tooling.

| Metric | How | Healthy |
|---|---|---|
| **Escaped defects per 10 slices** | defects found later that belong to an earlier slice | falling or flat. Rising → under-specified slices, not missing features |
| **Gate time** | clock the slice gate | < 60 s. Growing → the gate is becoming a reason to skip it |
| **Human-review rate** | slices you actually read vs. merged on green | falling is fine for tier C, never for money/auth/tenancy |
| **Rework rate** | slices re-opened after "done" | < 10 %. Higher → the plan or the review is too shallow |

And one qualitative check, monthly: **can a new person add a processor in a day using only the repo?** If not,
the abstraction leaked — read `docs/CHANGE-PLAYBOOK.md` §7 and fix the seam, not the call site.

---

## 10. Copy-paste prompts

### 10.1 Session start (first message of every session)

```text
Read CLAUDE.md. We are doing slice S1.11.2 only.
Run preflight, then restate the slice in ≤6 lines and show me the failing test you will write.
Do not write implementation code until I say go.
```

### 10.2 When you suspect fake completion

```text
Stop. I do not accept the summary.
Paste: (1) the test failing before the implementation, (2) the test going red after you delete one
line of the implementation, (3) the database row or ledger entry that proves it.
If you cannot paste all three, say which one you cannot and why.
```

### 10.3 UI review

```text
Use playwright mcp on http://localhost:3000/app/invoices.
Screenshot at 360x800, 768x1024, 1440x900 and read the images.
List every element that is clipped, misaligned, under 44px tall, or fails contrast —
with the file that owns it. Then fix them and re-capture.
```

### 10.4 Before merging a money slice

```text
Act as an auditor, not the author. Trace one $100 payment from the checkout page to the ledger entry.
For each step, name the file and the database row. Then try to make it post twice: describe three
attack paths and show the test that blocks each.
```

### 10.5 End of a step

```text
The step is finished. Run the step's Verify command and paste the real output.
Then update docs/PROGRESS.md with what now works, the gate result, and any deviation.
Do not mark the step done — I will.
```

---

## 11. What to expect, honestly

- **The first 3–5 slices will feel slow.** You are learning the rhythm and fixing plan defects. After S0.4 the
  pace roughly doubles because the primitives, tokens and test harness exist.
- **Roughly 15–25 % of slices will reveal a plan defect.** That is the system working, not failing — the fast
  lane turns each one into a five-minute fix instead of a week of drift.
- **Claude will occasionally be confidently wrong.** The gates exist for exactly that, and the three questions
  in §3.1 catch almost all of it. Trust the pasted output, never the summary.
- **The 122 unreviewed phase-2/3 slices are real work.** Reviewing them is how you avoid discovering, 300
  commits in, that a slice was never a day's work. Budget an afternoon per phase.
- **Nothing here removes judgment.** It removes the *avoidable* mistakes: forgotten features, invented schema,
  untested money paths, UI nobody looked at. What is left — product taste, market decisions, pricing — is yours.
