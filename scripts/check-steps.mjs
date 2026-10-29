#!/usr/bin/env node
// Step registry checker — see spec.md §19.
// Usage:
//   node scripts/check-steps.mjs            table of every step vs. files on disk
//   node scripts/check-steps.mjs S0.6       one step
//   node scripts/check-steps.mjs --strict   exit 1 if any step marked "done" is missing files
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const reg = JSON.parse(readFileSync(join(root, 'docs/steps.json'), 'utf8'));
const args = process.argv.slice(2);
const strict = args.includes('--strict');
const only = args.find((a) => /^S\d\.\d+$/.test(a));

const done = new Set(reg.steps.filter((s) => s.status === 'done').map((s) => s.id));
const rows = [];
let broken = 0;

for (const s of reg.steps) {
  if (only && s.id !== only) continue;
  const missing = (s.files ?? []).filter((f) => !existsSync(join(root, f)));
  const blockedBy = (s.depends_on ?? []).filter((d) => !done.has(d));
  let state = 'ready';
  if (s.status === 'done') state = missing.length ? 'BROKEN' : 'done';
  else if (s.status === 'in_progress') state = 'active';
  else if (missing.length) state = 'pending';
  if (state === 'BROKEN') broken += 1;
  rows.push({ id: s.id, phase: s.phase, state, missing, blockedBy });
}

const pad = (v, n) => String(v).padEnd(n);
console.log(`${pad('STEP', 7)}${pad('P', 3)}${pad('STATE', 9)}DETAIL`);
for (const r of rows) {
  const detail = r.state === 'BROKEN' ? `missing: ${r.missing.join(', ')}`
    : r.state === 'pending' ? `${r.missing.length} file(s) to create`
    : r.blockedBy.length ? `waits on ${r.blockedBy.join(', ')}`
    : 'startable';
  console.log(`${pad(r.id, 7)}${pad(r.phase, 3)}${pad(r.state, 9)}${detail}`);
}

const counts = rows.reduce((acc, r) => ((acc[r.state] = (acc[r.state] ?? 0) + 1), acc), {});
console.log(`\n${rows.length} step(s) · ${Object.entries(counts).map(([k, v]) => `${v} ${k}`).join(' · ')}`);

if (strict && broken) {
  console.error(`\nFAIL: ${broken} step(s) marked done are missing files.`);
  process.exit(1);
}
if (only && rows.length === 0) {
  console.error(`\nFAIL: no such step "${only}" in docs/steps.json`);
  process.exit(1);
}
