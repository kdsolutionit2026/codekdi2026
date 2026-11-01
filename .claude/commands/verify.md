---
description: Prove the current slice — run the gate, the proof, and the plan gates; paste real output
argument-hint: S1.5.3
allowed-tools: Read, Grep, Glob, Bash
---

Verify slice **$ARGUMENTS**. Report evidence, never a summary of evidence.

1. **Read the slice's gate** from `docs/slices.json` (its `gate` and `test` fields). Run it. Paste the full
   output, including the summary line. If it fails, stop and show me the failure — do not start fixing blindly.

2. **Prove the test can fail.** Temporarily break the implementation in the smallest possible way (comment one
   line, invert one condition), re-run the slice's test, paste the failure, then restore. If the test still
   passes, say so plainly — the test is decorative and the slice is not done.

3. **Run the plan gates** and paste each verdict:
   `node scripts/check-docs.mjs` · `node scripts/check-fr-coverage.mjs` · `node scripts/gen-slices.mjs --check` ·
   `node scripts/check-steps.mjs --strict`

4. **Money or tenancy slice only** — add the proof query from the step packet (a `select` showing the ledger
   balances, the audit chain, or a cross-tenant read returning 404) and paste its output.

5. **State honestly**:
   - what passed, with the command that proved it;
   - what you could not verify and why;
   - any deviation from the packet (or "none").

End with one line: `VERDICT: green` or `VERDICT: blocked — <reason>`.
