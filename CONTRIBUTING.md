# Contributing to KD PAY

This repo is a **plan plus its machine-checkable gates**. There is no application code yet — `S0.1` creates it.
That changes what "getting started" means: today you read, run four scripts, and pick a slice; after S0.1 you
also run the app.

## 1. First 15 minutes

```bash
git clone https://github.com/kdsolutionit2026/codekdi2026 && cd codekdi2026
node -v                       # 20+ is enough for the gates; the app needs 22+
node scripts/check-docs.mjs   # 0 problem(s) across 8 file(s)
node scripts/check-fr-coverage.mjs | tail -1   # 241 requirements · 0 unowned · 61 steps
node scripts/gen-slices.mjs --check            # docs/slices.json up to date — 402 slices
node scripts/check-steps.mjs --slices S1.5     # the actual work queue for one step
```

Then read three documents, in this order — or follow the full guide in [docs/BUILD-BOOK.md](docs/BUILD-BOOK.md). Resist the urge to read more:

1. **[docs/COMPONENTS.md](docs/COMPONENTS.md)** — ten components in plain language, one payment traced end to
   end. 20 minutes, and you will understand the system.
2. **[docs/AGENT_PLAYBOOK.md](docs/AGENT_PLAYBOOK.md) §4** — the loop: pull a slice, write the test, build,
   gate, commit.
3. **The step packet you are about to work on** — `spec.md` §3–§6A. Not the whole file. Never the whole file.

## 2. Where the answer to your question lives

| You want to know… | Read |
|---|---|
| What the product does, in plain language | `docs/COMPONENTS.md` |
| What the rule is (money, security, PCI, tenancy) | `docs/MASTER_SPECIFICATION.md` — **it wins any conflict** |
| What to build next, in what order | `spec.md` step packet + `docs/steps.json` |
| What exactly to do in this session | `docs/slices.json` for that step |
| How to write this kind of code (recipes) | `spec.md` §7 |
| What has gone wrong before | `spec.md` §11 (causes) and `docs/TROUBLESHOOTING.md` (ordered checks) |
| How to add a provider/currency/country/price later | `docs/CHANGE-PLAYBOOK.md` |
| Why the work is cut this small | `docs/STEP-GRANULARITY.md` |
| What "done" means and how to prove it | `docs/AGENT_PLAYBOOK.md` §5, `spec.md` §14 |
| Why a decision was made | `docs/adr/` |

**When two documents disagree, the master specification wins, and the disagreement is a bug** — report it,
do not reconcile it silently.

## 3. Picking up work

```bash
node scripts/check-steps.mjs --slices S1.5        # what the step is made of
node scripts/check-steps.mjs S1.5                 # but first: are its dependencies done?
```

Rules that apply to humans and agents identically:

- **One slice per commit.** A slice is at most one agent-day, one seam, one FR, one named test.
- **Do not start a step whose slices are `reviewed: false`** — 122 of 402 are still unreviewed (phases 2–3).
  Reviewing a slice means agreeing it is one day, one seam, one test. `check-steps.mjs --strict` enforces it.
- **The test exists before the code.** Write the failing test named in the slice, paste the failure, then build.
- **Do not edit** `spec.md`, `docs/MASTER_SPECIFICATION.md`, `docs/steps.json`, or a previous step's tests to
  make your change pass. Found a wrong path or a terse bullet? That is a *plan defect* — fix it in a separate
  commit (`spec.md` §20.5). Found a wrong **rule**? Stop, write `docs/OPEN_QUESTIONS.md`, get a decision.

## 4. Commits

One format, enforced by a hook:

```text
type(scope): summary in the imperative, ≤ 100 chars

Why this change, in one or two sentences. What it does not do.

Refs: FR-LDG-001, FR-LDG-002
Slice: S1.5.3
```

- `type` ∈ `feat|fix|chore|ci|docs|test|refactor|perf|build|revert`.
- `scope` is **what the commit is about**: a step id (`S1.5`), FR ids (`FR-AUTH-001..005`), or a doc area
  (`docs`, `deck`, `plan`). All three are legal — this is the single canonical rule; §13.1a of the plan is
  the same text.
- `Slice:` is **required for any commit that touches product code** (`src/`, `supabase/`, `tests/`), and must
  name a slice that exists in `docs/slices.json`. Tooling and docs commits (`scripts/`, `.githooks/`, `docs/`,
  `deck/`) omit it — a false trailer corrupts the progress ledger.
- Install the check once per clone:

```bash
git config core.hooksPath .githooks
```

A malformed message is caught at commit time, not in review.

## 5. Branches and pull requests

- Work on a short-lived branch; `arena/c7b6c1ec-codekdi2026` is the integration branch for agent sessions.
- Never rewrite a migration that has landed. Corrections are a new numbered file.
- Every PR body answers three lines:

```text
What changed (and the slice ids):
Rollback (one line — see spec.md §20.2):
Evidence (pasted gate output, proof query, screenshots):
```

- Keep the diff reviewable: if it touches more than 20 files, justify it in the PR body.

## 6. If an agent wrote the code and you are the human

Six checks, in this order. If any fails, it is not done, regardless of what the agent reported.

1. **Scope** — does the diff contain files the step did not ask for?
2. **Real output** — is the "verify" output a pasted terminal transcript, or a summary in prose?
3. **The test can fail** — delete one line of the implementation; does a test go red? If not, the test is
   decorative.
4. **Money** — trace one payment end to end. Is there any path that posts twice, skips the lock, or rounds in JS?
5. **Tenancy** — open another merchant's id by editing the URL. It must be 404, not 403 and never 200.
6. **Honesty** — does every identifier it used exist in the spec? (tables, routes, error codes, env vars)

That is what `docs/AGENT_PLAYBOOK.md` §4.3 automates with a second, read-only session.

## 7. Repo map

| Path | Today | After S0.1 |
|---|---|---|
| `spec.md` | plan, 61 packets | same |
| `docs/` | rules, plan mirrors, gates, ADRs, runbooks | + `PROGRESS.md` entries per session |
| `scripts/` | four dependency-free gates | + `check-commit-msg.mjs` |
| `deck/` | investor/partner decks (Python build scripts) | untouched |
| `src/app/`, `src/features/`, `src/lib/` | — | routes, domain logic, shared libraries |
| `supabase/migrations/` | — | append-only numbered SQL |
| `tests/` | — | unit (co-located), `integration/`, `rls/`, `e2e/`, `contract/`, `factories/` |
| `.githooks/` | commit-message check | same |

## 8. When you are stuck

Two strikes: if the same error survives two fix attempts, stop and write down the exact command, the exact
output, and what you tried. Then use `docs/TROUBLESHOOTING.md` — the symptom ladder is ordered cheapest-first
and covers the ten families that account for almost every incident. An hour spent on a new symptom earns a new
row in that file; that is how it stays useful.
