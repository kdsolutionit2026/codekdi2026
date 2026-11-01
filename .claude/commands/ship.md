---
description: Commit one slice, push, and draft the PR body with real evidence
argument-hint: S1.5.3
allowed-tools: Read, Grep, Glob, Bash
---

Ship slice **$ARGUMENTS**.

1. **Re-run the preconditions** and stop if any fails:
   `node scripts/check-docs.mjs` · `node scripts/gen-slices.mjs --check` · `node scripts/check-steps.mjs --strict`
   and the slice's own `gate` from `docs/slices.json`.

2. **Check the diff belongs to one slice.** `git diff --stat`. If it touches more than one seam, more than
   ~400 changed lines, or any file the slice did not name — stop and tell me which part to split off.

3. **Write the message** in the canonical form (`spec.md` §13.1a):

   ```text
   type(scope): summary in the imperative, ≤ 100 chars

   Why, in one or two sentences. What it does not do.

   Refs: FR-XXX-001
   Slice: S1.5.3
   ```

   `type` ∈ feat|fix|chore|ci|docs|test|refactor|perf|build|revert. `scope` = the step id, FR ids, or doc area.

4. **Commit and push** to the current branch. The `commit-msg` hook will reject a bad message — fix the
   message, never `--no-verify`.

5. **Draft the PR body** (do not open the PR unless I ask):

   ```text
   What changed (slice ids):
   Why:
   Evidence (pasted gate output, proof query, screenshots at 360/768/1440):
   Rollback (one line — spec.md §20.2):
   Not done / follow-ups:
   ```

6. **Update `docs/PROGRESS.md`** with one line: date, slice, what now works, gate result. If this slice
   completed a step, say so — but do not set the step to `done` yourself.
