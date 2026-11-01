#!/usr/bin/env node
// "Where am I in the book?" — the serial build order, computed from the registry.
//
//   node scripts/next.mjs            the next step to work on, its slices, and the exact commands
//   node scripts/next.mjs --order    the full 61-chapter serial build order, with state
//   node scripts/next.mjs --all      only the steps that are unblocked right now
//
// The rule is the one `docs/BUILD-BOOK.md` describes: work in chapter order, never start a step whose
// dependencies are not done, and never start one whose slices are not all reviewed. Read-only and
// dependency-free; it never writes to the registry.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const reg = JSON.parse(readFileSync(join(root, 'docs/steps.json'), 'utf8'));
const sliceDoc = existsSync(join(root, 'docs/slices.json'))
  ? JSON.parse(readFileSync(join(root, 'docs/slices.json'), 'utf8'))
  : { slices: [] };

const steps = reg.steps;
const byStep = new Map();
for (const s of sliceDoc.slices) {
  if (!byStep.has(s.step)) byStep.set(s.step, []);
  byStep.get(s.step).push(s);
}
const done = new Set(steps.filter((s) => s.status === 'done').map((s) => s.id));
const chapterOf = new Map(steps.map((s, i) => [s.id, i + 1]));
const chapter = (id) => String(chapterOf.get(id)).padStart(2);

const ACTS = [
  { to: 14, name: 'Act I — Foundations: it runs, it is safe, it has contracts' },
  { to: 35, name: 'Act II — Money in: a merchant, an invoice, a payment, a ledger entry' },
  { to: 53, name: 'Act III — Money out and scale: payouts, disputes, support, reports' },
  { to: 61, name: 'Act IV — Enterprise: routing, FX, tax, hardening' },
];
const actOf = (ch) => ACTS.find((a) => ch <= a.to) ?? ACTS[ACTS.length - 1];

const slicesOf = (id) => byStep.get(id) ?? [];
const depsOf = (id) => (steps.find((s) => s.id === id)?.depends_on ?? []).filter((d) => !done.has(d));

// Greedy topological sort in chapter order: this is the canonical serial build order, independent of
// what has been done so far. Ties break by chapter, which keeps the book stable across runs.
function serialOrder() {
  const seen = new Set();
  const order = [];
  // Take ONE step per round — the lowest chapter among those whose dependencies are satisfied. Taking
  // every ready step at once scrambles the book: a late step with a shallow dependency graph would be
  // scheduled before the foundations it will import.
  while (order.length < steps.length) {
    const ready = steps.filter(
      (s) => !seen.has(s.id) && (s.depends_on ?? []).every((d) => seen.has(d) || !steps.some((x) => x.id === d)),
    );
    if (!ready.length) break;
    ready.sort((a, b) => chapterOf.get(a.id) - chapterOf.get(b.id));
    seen.add(ready[0].id);
    order.push(ready[0]);
  }
  // Anything left over (a dependency cycle) is appended in chapter order — nothing disappears silently;
  // check-steps.mjs is the place that reports the cycle.
  for (const s of steps) if (!seen.has(s.id)) order.push(s);
  return order;
}
const ORDER = serialOrder();

const state = (s) => {
  if (s.status === 'done') return 'done';
  const deps = depsOf(s.id);
  if (deps.length) return `blocked (${deps.join(', ')})`;
  const l = slicesOf(s.id);
  const un = l.filter((x) => !x.reviewed).length;
  if (un) return `needs review (${un}/${l.length} slices)`;
  return s.status === 'in_progress' ? 'active' : 'ready';
};

const args = process.argv.slice(2);

if (args.includes('--order')) {
  let act = '';
  for (const s of ORDER) {
    const ch = chapterOf.get(s.id);
    const a = actOf(ch).name;
    if (a !== act) {
      act = a;
      console.log(`\n${a}`);
    }
    console.log(
      `  ch ${chapter(s.id)}  ${s.id.padEnd(6)} ${`${s.effort}d`.padEnd(6)} ${String(slicesOf(s.id).length).padStart(2)}sl  ` +
        `${state(s).padEnd(24)} ${s.title}`,
    );
  }
  console.log(`\n${steps.length} chapters · ${steps.length && sliceDoc.slices.length} slices · ${steps.reduce((a, s) => a + s.effort, 0)} agent-days`);
  process.exit(0);
}

const open = steps.filter((s) => s.status !== 'done');
const active = open.find((s) => s.status === 'in_progress');
const next = active ?? ORDER.find((s) => s.status !== 'done' && depsOf(s.id).length === 0) ?? ORDER.find((s) => s.status !== 'done');

if (args.includes('--all')) {
  const ready = open.filter((s) => depsOf(s.id).length === 0);
  if (!ready.length) console.log('nothing unblocked — every step is done or waiting on a dependency');
  for (const s of ready) {
    const l = slicesOf(s.id);
    const un = l.filter((x) => !x.reviewed).length;
    console.log(
      `ch ${chapter(s.id)}  ${s.id.padEnd(6)} ${`${s.effort}d`.padEnd(6)} ${String(l.length).padStart(2)}sl  ` +
        `${(un ? `needs review ${un}/${l.length}` : 'ready').padEnd(20)} ${s.title}`,
    );
  }
  process.exit(0);
}

if (!next) {
  console.log('Every step is done. The build is finished — move on to docs/CHANGE-PLAYBOOK.md.');
  process.exit(0);
}

const ch = chapterOf.get(next.id);
const list = slicesOf(next.id);
const st = state(next);

console.log(`NEXT  ${next.id} — ${next.title}`);
console.log(`      ${actOf(ch).name}`);
console.log(`      chapter ${ch} of ${steps.length} · phase ${next.phase} · ${next.effort} agent-days · ${list.length} slice(s) · ${st}`);
console.log('');
for (const x of list) {
  const flag = x.reviewed ? (x.test ? ' ' : '!') : '·';
  console.log(`      ${flag} ${x.id.padEnd(9)} ${`${x.effort}d`.padEnd(6)} ${x.seam.padEnd(9)} ${x.title.slice(0, 76)}`);
}
console.log('');
console.log(`      read: spec.md "### ${next.id} — " + the sections it lists under **Master spec:**`);
console.log('      then:');
console.log(`        /kickoff ${list[0]?.id ?? next.id}`);
console.log(`        node scripts/check-steps.mjs --slices ${next.id}`);
console.log('');

const follow = ORDER.filter((s) => s.id !== next.id && s.status !== 'done').slice(0, 3);
if (follow.length) {
  console.log('after that:');
  for (const s of follow) console.log(`      ch ${chapter(s.id)}  ${s.id.padEnd(6)} ${`${s.effort}d`.padEnd(6)} ${s.title.slice(0, 62)}`);
}
