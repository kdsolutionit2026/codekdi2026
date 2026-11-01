# Step granularity — how work is cut so an AI agent cannot lose the plot

A plan is only as good as the unit of work it is handed to an agent. Give an agent a 15-day step and it will
truncate its own context, bundle four concerns into one diff, and "verify" with a smoke test it wrote from the
same misunderstanding as the code. This document defines the unit of work, the rules that bound it, and the
gates that catch an agent that breaks them.

It is enforceable, not aspirational: `docs/slices.json` is generated from `spec.md`, and
`node scripts/check-steps.mjs --strict` fails the build when a step violates the rules below.

---

## 1. Two levels, and only two

| Level | File | Size | Answers | Owner |
|---|---|---|---|---|
| **Step** | `spec.md` + `docs/steps.json` | ≤ 15 agent-days, average 4 | *what capability exists when this is done* | plan |
| **Slice** | `docs/slices.json` | **≤ 1 agent-day** | *what one agent does before its next commit* | execution |

The step is the **contract with the product**: one shippable capability, one FR group, one `**Done when:**`
the reviewer can check without reading the diff. The slice is the **contract with the agent**: one context
window, one seam, one gate command, one commit message.

Nothing sits between them. If a slice needs a sub-slice, the slice was a step in disguise — re-cut it.

### Why not just have 400 steps?

Because a step is a promise to a human: "when this is `done` the product can do X". 400 promises of that
weight cannot be reviewed, sequenced, or explained to anyone. The eight-phase, 61-step structure is the
product roadmap; the 402 slices are the queue an agent pulls from. Keeping both, with slices *derived* from
steps, is what stops the two from drifting apart.

---

## 2. The rules

Each rule has an ID that appears in `check-steps.mjs` output, so a failure tells you which rule broke.

**G1 — Slice ids are `<step>.<n>`, unique, and every step has at least one.**
Ids are load-bearing: the commit trailer (`Slice: S1.5.3`) and the progress table both key on them. A step
with no slices means the generator was not re-run — the fix is `node scripts/gen-slices.mjs --write`, never a
hand-written slice.

**G2 — A slice costs more than 0 and at most 1.0 agent-day.**
One day is the largest unit that reliably fits in a single context window together with its tests, and the
largest unit a reviewer can hold in their head at once. The floor exists because 0.05-day slices are noise:
they produce commits, not progress.

**G3 — A step has at least `ceil(effort)` slices, and its slices sum exactly to its effort.**
This is the arithmetic that makes the plan and the execution layer one system. If a step is 5 days and has 3
slices, the split is fake — two of those slices are multi-day and the whole exercise bought nothing. If the
sum drifts from the step's effort, either the plan changed without the registry or the slices were re-weighted
to hide a big one; both are failures.

**G4 — Every slice names a seam and a gate.**
The **seam** is the single layer the slice touches — `schema`, `domain`, `module`, `contract`, `http`, `ui`,
`test`, `ops`, `docs`. The **gate** is the exact command that must pass before the commit. A slice with no
seam is a slice that will leak across three files; a slice with no gate is a slice nobody can verify.

**G5 — A step cannot be `in_progress` or `done` unless every one of its slices is `reviewed: true` and
names a test.**
Test-first, mechanically: the slice carries the name of the test file *and* the test that must exist and fail
before the code is written. Review happens on the plan, not on the diff — that is what makes a one-day unit
safe to auto-merge. Today 279 of 402 slices are reviewed (all of phases 0 and 1); the remaining 122 are
phase 2–3 slices still awaiting a review pass. **No phase-2 step can start until its slices are reviewed**,
which is the intended meaning: the review is the gate, not a formality after the fact.

**G6 — A `done` step has only `done` slices.**
Status flows up, never sideways. A step cannot be marked done while a slice is still open; the reverse
(a slice done under a pending step) is normal and is how progress is counted.

---

## 3. What a slice may contain

A slice is **vertical**, not a layer. It changes at most:

- **400 changed lines** in total, tests included;
- **one FR** from `docs/MASTER_SPECIFICATION.md` (or none, for infrastructure slices);
- **one test file**, and the test names its own gate;
- **one seam** — the layer named in `docs/slices.json`.

A schema change plus the code that uses it is *two* slices when the code needs a day of its own, and *one*
slice when it does not. The test is the changed-line budget, not the file count. When a slice needs a second
layer to be verifiable at all (a route handler with no test harness), the harness is the earlier slice —
test infrastructure is allowed to precede the feature, never follow it.

Horizontal splitting is the common mistake: "all the migrations", then "all the services", then "all the UI".
That produces slices with no runnable checkpoint — nothing works until the last one lands — which is exactly
the defect class this document exists to prevent.

---

## 4. When you may over-split (and when you must not)

Over-splitting is a real defect, not a safe default. The rules above bound it (G2's floor, G3's
`ceil(effort)` minimum, the 3× note in the report), but the judgment is human:

| Symptom | What it means | Fix |
|---|---|---|
| Two slices always change the same three files | Shared-file conflict — `schema.sql`, the FR registry, `steps.json` | Merge them, or give the file **one owner slice** and have the others wait |
| Slice N cannot pass its gate until slice N+1 lands | The cut is horizontal | Re-cut along a user-visible behaviour |
| A slice's title needs "and" twice | Multi-concern diff | Cut at the second "and" |
| A slice exists only to update a doc | Doc-only slices ride along with the code slice they describe, except the plan-level docs | Absorb it into the code slice |
| A slice is 0.05 d | Noise | Merge upward |

The generator applies the first rule mechanically: **a step whose effort is ≤ 1.0 day is exactly one slice.**
Splitting a 1-day step into twelve 0.05-day slices "for consistency" was an early bug in this design and it
made the queue worse, not better.

---

## 5. Gates: three tiers, continuous

Checking is not an event at the end of a phase; it is three loops that run at different frequencies. A gate
that takes longer than its budget gets skipped, so the budget is part of the definition.

| Tier | When | Budget | Runs |
|---|---|---|---|
| **Slice/step gate** | before every commit | **< 60 s** | typecheck, lint, unit tests for the touched files, RLS smoke on the touched tables, the slice's named test |
| **Unit gate** | every ~8 commits / end of a step | ~5 min | integration tests, migration replay from scratch, contract tests (S0.14), tenant-isolation spot check |
| **Release gate** | every ~10 steps / end of a phase | ~30 min | full suite, fuzz, isolation suite, restore drill, `check-docs` + `check-fr-coverage` + `check-steps --strict`, escape review |

The plan-level gates (`check-docs`, `check-fr-coverage`, `check-steps --strict`) run in the release tier **and**
in CI on every PR, because they are cheap and they catch drift the moment it is introduced.

**Nothing here relaxes §19.1.** `check-steps.mjs` with no flags is a report and always exits 0. `--strict`
and `--granularity` are the only failing modes, and they are opt-in.

---

## 6. Does splitting actually work? The honest arithmetic

The number of escaped defects per 10 steps, by unit size, from the analysis this design is based on:

| Commit size | Escaped defects per 10 steps |
|---|---|
| 60 fully-specified packets (~4 days each) | **60–75 %** |
| ~250 commits (~1 day each) | 75–82 % |
| ~500 commits (~½ day each) | 78–85 % |
| ~1,500 commits | flat or worse |

Two things follow, and they are the reason this document is short.

1. **Most of the gain is in the first split.** Going from 60 multi-day packets to one-day slices buys nearly
   everything. Going from 250 to 1,500 buys approximately nothing and costs review fatigue, merge conflicts,
   and lost intent. **402 slices is the right neighbourhood; the target is not 1,500.**
2. **Splitting only fixes half the problem.** It reduces context truncation and multi-concern diffs. It does
   **nothing** for unverifiable acceptance (fixed by test-first, G5) and it actively *worsens* interface drift
   (fixed by the frozen contracts in S0.14). A split plan with no test-first rule and no frozen interfaces is
   worse than the coarse plan it replaced, because more agents now touch the same boundaries.

**The measurement that decides whether to keep splitting:** escaped defects per 10 steps — defects found in
steps N+1..N+10 that belong to step N. Falling after a change → keep going. Flat → stop, you are at the
plateau. Rising → you are under-specifying, not over-splitting; go back to `spec.md` and the FR text.

---

## 7. Operating the registry

```bash
node scripts/gen-slices.mjs              # summary: counts, effort, largest slices, seams
node scripts/gen-slices.mjs --write      # regenerate docs/slices.json from spec.md
node scripts/gen-slices.mjs --check       # exit 1 if docs/slices.json is stale (CI)
node scripts/check-steps.mjs              # step table vs. files on disk (report only)
node scripts/check-steps.mjs --slices S1.5
node scripts/check-steps.mjs --granularity   # G1–G4 report; exit 1 on any breach
node scripts/check-steps.mjs --strict        # CI gate: registry integrity + G5/G6 on started work
```

`docs/slices.json` is **generated** — edit `spec.md`'s `**Build**` list or `scripts/gen-slices.mjs`'s
`OVERRIDES`, never the JSON. Titles for under-specified packets are hand-authored in `OVERRIDES`; if a slice
title reads badly, that is a signal the packet's `**Build**` list is too terse, and the fix belongs in
`spec.md`.
