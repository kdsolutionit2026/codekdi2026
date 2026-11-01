#!/usr/bin/env node
// Step registry checker — see spec.md §19 and docs/STEP-GRANULARITY.md.
//
//   node scripts/check-steps.mjs                 table of every step vs. files on disk
//   node scripts/check-steps.mjs S0.6            one step
//   node scripts/check-steps.mjs --slices [S0.6] slice table (all steps, or one)
//   node scripts/check-steps.mjs --granularity   decomposition report; exit 1 on any rule breach
//   node scripts/check-steps.mjs --strict        the CI gate: registry integrity + granularity on
//                                                every step that is in_progress or done
//
// Granularity rules (docs/STEP-GRANULARITY.md §4):
//   G1  every step has slices and every slice id is "<step>.<n>", unique
//   G2  a slice costs more than 0 and at most max_effort_per_slice agent-days
//   G3  a step has at least ceil(effort) slices, and the slices sum to the step's effort
//   G4  every slice names a seam from the allowed set and a gate command
//   G5  a step that is in_progress or done has every slice reviewed and every slice carrying a
//       named test (test-first: the test exists before the code does)
//   G6  a done step has only done slices
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const reg = JSON.parse(readFileSync(join(root, 'docs/steps.json'), 'utf8'));
const slicesPath = join(root, 'docs/slices.json');
const sliceDoc = existsSync(slicesPath) ? JSON.parse(readFileSync(slicesPath, 'utf8')) : null;
const slices = sliceDoc?.slices ?? [];
const MAX = sliceDoc?.max_effort_per_slice ?? 1;
const SEAMS = new Set(sliceDoc?.seams ?? ['schema', 'domain', 'http', 'ui', 'test', 'docs', 'ops', 'module', 'contract']);

const args = process.argv.slice(2);
const strict = args.includes('--strict');
const granularity = args.includes('--granularity');
const showSlices = args.includes('--slices');
const only = args.find((a) => /^S\d\.\d+$/.test(a));

const pad = (v, n) => String(v).padEnd(n);
const done = new Set(reg.steps.filter((s) => s.status === 'done').map((s) => s.id));
const problems = [];
const fail = (msg) => problems.push(msg);

// ---------- slice index ----------
const byStep = new Map();
for (const sl of slices) {
  if (!byStep.has(sl.step)) byStep.set(sl.step, []);
  byStep.get(sl.step).push(sl);
}

const seenIds = new Set();
for (const sl of slices) {
  if (seenIds.has(sl.id)) fail(`G1 duplicate slice id ${sl.id}`);
  seenIds.add(sl.id);
  if (!/^S\d\.\d+\.\d+$/.test(sl.id)) fail(`G1 malformed slice id ${sl.id}`);
  else if (!sl.id.startsWith(`${sl.step}.`)) fail(`G1 slice ${sl.id} does not belong to ${sl.step}`);
  if (!(typeof sl.effort === 'number' && sl.effort > 0)) fail(`G2 ${sl.id} has no positive effort`);
  else if (sl.effort > MAX + 1e-9) fail(`G2 ${sl.id} costs ${sl.effort} agent-days (max ${MAX})`);
  if (!SEAMS.has(sl.seam)) fail(`G4 ${sl.id} has unknown seam "${sl.seam}"`);
  if (!sl.gate || !String(sl.gate).trim()) fail(`G4 ${sl.id} has no gate command`);
}

// ---------- per-step rules ----------
const rows = [];
let broken = 0;
let decomposed = 0;
let overBudget = 0;

for (const s of reg.steps) {
  if (only && s.id !== only) continue;
  const missing = (s.files ?? []).filter((f) => !existsSync(join(root, f)));
  const blockedBy = (s.depends_on ?? []).filter((d) => !done.has(d));
  let state = 'ready';
  if (s.status === 'done') state = missing.length ? 'BROKEN' : 'done';
  else if (s.status === 'in_progress') state = 'active';
  else if (missing.length) state = 'pending';
  if (state === 'BROKEN') broken += 1;

  const list = byStep.get(s.id) ?? [];
  const effort = Number(s.effort ?? 0);
  const need = Math.max(1, Math.ceil(effort - 1e-9));
  const sum = Number(list.reduce((a, x) => a + (x.effort ?? 0), 0).toFixed(2));
  const started = s.status === 'in_progress' || s.status === 'done';

  if (!list.length) {
    fail(`G1 ${s.id} has no slices — run: node scripts/gen-slices.mjs --write`);
  } else {
    decomposed += 1;
    if (list.length < need) fail(`G3 ${s.id} has ${list.length} slices for ${effort} agent-days (needs ≥ ${need})`);
    if (Math.abs(sum - effort) > 0.011) fail(`G3 ${s.id} slices sum to ${sum}, registry says ${effort}`);
    if (list.length > need * 3) overBudget += 1;
    if (started) {
      const unreviewed = list.filter((x) => !x.reviewed).map((x) => x.id);
      // Docs slices are verified by the docs gate, not by a test — exempt them, or chapter one can never start.
      const untested = list.filter((x) => !x.test && x.seam !== 'docs').map((x) => x.id);
      if (unreviewed.length) fail(`G5 ${s.id} is ${s.status} but ${unreviewed.length} slice(s) are unreviewed: ${unreviewed.slice(0, 4).join(', ')}`);
      if (untested.length) fail(`G5 ${s.id} is ${s.status} but ${untested.length} slice(s) name no test: ${untested.slice(0, 4).join(', ')}`);
    }
    if (s.status === 'done') {
      const open = list.filter((x) => x.status !== 'done').map((x) => x.id);
      if (open.length) fail(`G6 ${s.id} is done but ${open.length} slice(s) are not: ${open.slice(0, 4).join(', ')}`);
    }
  }

  rows.push({ id: s.id, phase: s.phase, state, missing, blockedBy, slices: list.length, effort, sum });
}

// ---------- granularity report ----------
if (granularity || strict) {
  const reviewed = slices.filter((x) => x.reviewed).length;
  const unreviewed = slices.length - reviewed;
  const totalSlices = slices.reduce((a, x) => a + (x.effort ?? 0), 0);
  const biggest = slices.reduce((m, x) => Math.max(m, x.effort ?? 0), 0);
  const lines = [
    '',
    `GRANULARITY  ${decomposed}/${reg.steps.length} steps decomposed · ${slices.length} slices · ` +
      `${totalSlices.toFixed(1)} agent-days · largest slice ${biggest}d (max ${MAX})`,
    `             slices reviewed ${reviewed} · unreviewed ${unreviewed} (a step must be fully reviewed before it starts)`,
    `             steps with >3× the minimum slice count: ${overBudget}`,
  ];
  console.log(lines.join('\n'));
}

if (showSlices) {
  console.log(`\n${pad('SLICE', 9)}${pad('STEP', 7)}${pad('EFFORT', 8)}${pad('SEAM', 10)}${pad('REV', 5)}TITLE`);
  for (const sl of slices) {
    if (only && sl.step !== only) continue;
    console.log(
      `${pad(sl.id, 9)}${pad(sl.step, 7)}${pad(`${sl.effort}d`, 8)}${pad(sl.seam, 10)}` +
        `${pad(sl.reviewed ? 'yes' : 'no', 5)}${sl.title}`,
    );
  }
  console.log(`\n${slices.length} slice(s) · ${slices.filter((x) => !x.reviewed).length} awaiting review`);
}

// ---------- step table ----------
if (!showSlices || granularity) {
  console.log(`\n${pad('STEP', 7)}${pad('P', 3)}${pad('STATE', 9)}${pad('SLICES', 8)}DETAIL`);
  for (const r of rows) {
    const detail =
      r.state === 'BROKEN'
        ? `missing: ${r.missing.join(', ')}`
        : r.state === 'pending'
          ? `${r.missing.length} file(s) to create`
          : r.blockedBy.length
            ? `waits on ${r.blockedBy.join(', ')}`
            : 'startable';
    console.log(`${pad(r.id, 7)}${pad(r.phase, 3)}${pad(r.state, 9)}${pad(r.slices, 8)}${detail}`);
  }
  const counts = rows.reduce((acc, r) => ((acc[r.state] = (acc[r.state] ?? 0) + 1), acc), {});
  console.log(`\n${rows.length} step(s) · ${Object.entries(counts).map(([k, v]) => `${v} ${k}`).join(' · ')}`);
}

// ---------- verdict ----------
if (only && rows.length === 0 && !slices.some((x) => x.step === only)) {
  console.error(`\nFAIL: no such step "${only}" in docs/steps.json`);
  process.exit(1);
}

// --strict and --granularity are gates; the plain report is not.
if (problems.length && (strict || granularity)) {
  console.error(`\nFAIL: ${problems.length} granularity/registry problem(s)`);
  for (const p of problems.slice(0, 40)) console.error(' -', p);
  if (problems.length > 40) console.error(` ... and ${problems.length - 40} more`);
  process.exit(1);
}
if (problems.length) {
  console.log(`\n(${problems.length} deferred problem(s) — run --strict or --granularity to fail on them)`);
}
if (strict && broken) {
  console.error(`\nFAIL: ${broken} step(s) marked done are missing files.`);
  process.exit(1);
}
