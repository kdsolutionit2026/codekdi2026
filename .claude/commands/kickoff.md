---
description: Start a step or slice — preflight, read only what is needed, propose a plan
argument-hint: S1.5 or S1.5.3
allowed-tools: Read, Grep, Glob, Bash
---

Kick off work on **$ARGUMENTS**.

Do exactly this, in order, and stop at step 4 until I approve. Do not write code before I approve.

1. **Preflight.** Run `node scripts/check-steps.mjs $ARGUMENTS` (or, for a slice id, its step). Report:
   - is every `depends_on` step `done`?
   - are all slices for the step `reviewed`? If any is `reviewed: false`, **stop here** and say so — an
     unreviewed slice cannot start (`docs/STEP-GRANULARITY.md` G5).
   - which slice is next (`pending`), and its `seam`, `gate`, `test`.

2. **Read narrowly.** Read only:
   - the step packet in `spec.md` (the `### <step> — ` block),
   - the master-spec sections that packet lists under **Master spec:**,
   - the FR rows the packet lists under **Features:**, from `docs/MASTER_SPECIFICATION.md` §35,
   - the relevant recipe in `spec.md` §7 if the slice names one.

3. **Restate the slice** in ≤ 6 lines: what will exist when it is done, what test proves it, what the gate
   command is, and what it explicitly will *not* do.

4. **Plan.** Output:
   - the file list you will create or edit (nothing outside it),
   - the **failing test** you will write first, with its assertion in one sentence,
   - anything in the spec that is ambiguous or missing — as a question, not an assumption,
   - the rollback line for the PR (`spec.md` §20.2).

Then wait. If I say go, begin with RED.
