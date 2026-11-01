# CLAUDE.md — read this first, every session

This repository is a **plan plus its execution layer**. There is no application code until S0.1 lands.

## What to read, in this order, and nothing more

1. This file, then `docs/BUILD-BOOK.md` §4 if you need the full session procedure.
2. The **step packet** you are working on: `spec.md` §3–§6A, one `### S<id> — ` block.
3. The **slices** for that step: `node scripts/check-steps.mjs --slices S1.5`.
4. The master-spec sections that packet names (typically 100–400 lines).

**Never load all of `spec.md` or all of `docs/MASTER_SPECIFICATION.md`.** They are 3,900 and 6,000 lines.
Read what the packet points at. If you catch yourself grepping the whole spec, stop and read the packet again.

## Non-negotiable rules

- **`docs/MASTER_SPECIFICATION.md` wins every conflict.** If the plan disagrees with it, report the conflict;
  do not reconcile it yourself.
- **Never edit** `spec.md`, `docs/MASTER_SPECIFICATION.md`, `docs/steps.json`, `docs/slices.json`, or a
  previous step's tests to make your change pass. (Plan defects have a fast lane — `spec.md` §20.5.)
- **Money is never a JS `number`.** `numeric(18,4)` in Postgres, string/integer micro-units in TypeScript.
- **No new table, column, route, error code, env var, or dependency** that is not in the spec. Stop and ask.
- **No card data** on our servers (PCI SAQ-A). **No merchant funds** in our bank account.
- **Every new table** ships RLS + isolation test + exposure block in the same migration.
- **One slice per commit.** One seam, one FR, one named test.
- **Never mark a step `done`.** Report evidence; a human decides.

## The loop (do not improvise a different one)

```bash
node scripts/next.mjs                        # what is next, computed from the dependency graph
node scripts/check-steps.mjs S1.5            # deps done? slices reviewed?
node scripts/check-steps.mjs --slices S1.5   # pick the next `pending` slice
```

1. **RED** — write the slice's named test first; paste it failing.
2. **BUILD** — implement until it passes. Typecheck after each chunk.
3. **GATE** — the slice's `gate` command from `docs/slices.json`, < 60 s.
4. **LOOK** — for any UI slice, `/ui` (Playwright MCP at 360/768/1440). Do not claim a screen works unseen.
5. **COMMIT** — one slice, `Slice:` trailer, conventional message (`spec.md` §13.1a).

## Commands

```bash
pnpm dev                     # local preview on http://localhost:3000 (after S0.1)
pnpm verify                  # lint + typecheck + unit + integration + RLS
node scripts/check-docs.mjs  # docs integrity      (always green before you stop)
node scripts/check-fr-coverage.mjs               # 241 FRs, one owner each
node scripts/gen-slices.mjs --check              # execution layer not stale
node scripts/check-steps.mjs --strict            # registry + slice rules
```

## When you are stuck

**Two strikes.** If the same error survives two fix attempts, stop. Write the exact command, the exact output,
and what you tried. Then read `docs/TROUBLESHOOTING.md` — its ladder is ordered cheapest-first.

Stop and ask (write to `docs/OPEN_QUESTIONS.md` + the PR body) when: a required table/route/error code does not
exist in the spec, a rule is wrong, an FR is ambiguous, or two documents disagree.

## Style of work

- Small diffs. If you touch > 20 files, justify it.
- No speculative abstraction. Write the thing the slice asks for.
- A test that cannot fail is not a test. Delete a line of the implementation and confirm it goes red.
- Paste real command output. "Should work" is not evidence.
