---
description: Read-only review of the current diff — scope, truth, tests, money, tenancy, honesty
argument-hint: (optional) a commit range or "staged"
allowed-tools: Read, Grep, Glob, Bash
---

You are reviewing a diff for a payment platform. **You did not write it and you may not change it.** Report
only; the human decides.

Input: `$ARGUMENTS` — or, if empty, `git diff main...HEAD` plus `git status`.

Answer these six questions, in this order, with file and line references:

1. **SCOPE** — does the diff contain anything the slice did not ask for? List every extra file, every
   "while I was here" refactor, every new dependency.
2. **TRUTH** — does the code do what the step packet says, using only tables, routes, error codes and env vars
   that exist in `docs/MASTER_SPECIFICATION.md`? Name any invented identifier.
3. **TESTS** — for each test added, ask: *what would I delete to make this fail?* If there is no answer, the
   test is decorative — say so. Also check the test asserts behaviour, not implementation detail.
4. **MONEY** — trace one payment end to end. Is there any path that posts twice, skips the lock, rounds in JS,
   or turns a `numeric` into a `number`? Check the idempotency key is per-payment, not per-attempt.
5. **TENANCY** — is every query scoped to the merchant? Does a foreign id return **404** (not 403, never 200)?
   Does any cache key omit the tenant or role?
6. **HONESTY** — does the pasted "verify" output look like a real terminal transcript? Do the test names it
   mentions actually exist? Was any test skipped, retried until green, or weakened to pass?

Output:

- **BLOCKERS** — must fix before merge.
- **RISKS** — should fix, with the reason.
- **NITS** — optional.
- One-line verdict: `SHIP` / `FIX-FIRST` / `FALSE-DONE`.
