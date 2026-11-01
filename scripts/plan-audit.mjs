#!/usr/bin/env node
// Plan audit — is the PLAN right, not just consistent?
//
//   node scripts/plan-audit.mjs
//
// The four existing gates answer "are the documents self-consistent?" (anchors, FR ownership, slice freshness,
// registry vs files). This one answers a different question: "is the plan structurally sound enough to build
// from?" It checks the things that produce expensive rework when wrong:
//
//   A1  every depends_on points at a real step          (a typo silently satisfies the dependency)
//   A2  no self-dependency, no dependency cycle         (a cycle means the order can never be satisfied)
//   A3  every step is reachable from S0.1               (an orphan step is planned work nobody will do)
//   A4  packet **Features:** == registry fr             (ranges expanded — drift here drops features)
//   A5  packet **Effort:** == registry effort
//   A6  slices sum to the step effort, none over the cap
//   A7  a step ≥ 3 days has ≥ 5 build items or authored overrides (thin packet = under-specified work)
//   A8  a step whose slices carry no test on a code seam (test-first gap, reported per step)
//
// Exit 0 always unless --strict; exit 1 under --strict when A1–A6 fail. A7/A8 are warnings by design —
// they are judgement calls, not defects.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const strict = process.argv.includes('--strict');
const problems = [];
const warnings = [];

const spec = readFileSync(join(root, 'spec.md'), 'utf8');
const reg = JSON.parse(readFileSync(join(root, 'docs/steps.json'), 'utf8'));
const sliceDoc = existsSync(join(root, 'docs/slices.json'))
  ? JSON.parse(readFileSync(join(root, 'docs/slices.json'), 'utf8'))
  : { slices: [], max_effort_per_slice: 1 };
const steps = reg.steps;
const ids = new Set(steps.map((s) => s.id));
const byStep = new Map();
for (const sl of sliceDoc.slices) {
  if (!byStep.has(sl.step)) byStep.set(sl.step, []);
  byStep.get(sl.step).push(sl);
}

// ---------- packet parsing ----------
const parts = spec.split(/^### (S\d+\.\d+) — .+$/m);
const packets = new Map();
for (let i = 1; i < parts.length; i += 2) {
  packets.set(parts[i], parts[i + 1]);
}
const expandFr = (text) => {
  const out = new Set();
  for (const m of text.matchAll(/FR-([A-Z]+)-(\d+)(?:\.\.(\d+))?/g)) {
    const lo = Number(m[2]);
    const hi = m[3] ? Number(m[3]) : lo;
    for (let i = lo; i <= hi; i += 1) out.add(`FR-${m[1]}-${String(i).padStart(3, '0')}`);
  }
  return out;
};
const featuresOf = (body) => {
  const m = body.match(/\*\*Features:\*\*(.+?)(?=\n\s*\n|\n\*\*[A-Z])/s);
  return m ? expandFr(m[1]) : null;
};
const effortOf = (body) => {
  const m = body.match(/\*\*Effort:\*\*\s*([\d.]+)/);
  return m ? Number(m[1]) : null;
};
// Packets use "**Build**" but a few use "**Build / run**"; both are valid, so match any **Build…** label.
const buildItemsOf = (body) => {
  const m = body.match(/\*\*Build[^*]*\*\*\n([\s\S]*?)(?=\n\*\*|\n### |\n---)/);
  return m ? (m[1].match(/^\d+\.\s/gm) ?? []).length : 0;
};

// ---------- A1 / A2 dependencies ----------
const graph = new Map();
for (const s of steps) {
  const deps = s.depends_on ?? [];
  for (const d of deps) {
    if (!ids.has(d)) problems.push(`A1 ${s.id} depends on "${d}", which is not a step in the registry`);
    if (d === s.id) problems.push(`A2 ${s.id} depends on itself`);
  }
  graph.set(s.id, deps.filter((d) => ids.has(d)));
}
const color = new Map(); // 0 unvisited, 1 in-stack, 2 done
const cycles = [];
function dfs(node, stack) {
  color.set(node, 1);
  for (const next of graph.get(node) ?? []) {
    if (color.get(next) === 1) cycles.push([...stack.slice(stack.indexOf(next)), next].join(' → '));
    else if (!color.has(next)) dfs(next, [...stack, next]);
  }
  color.set(node, 2);
}
for (const s of steps) if (!color.has(s.id)) dfs(s.id, [s.id]);
for (const c of cycles) problems.push(`A2 dependency cycle: ${c}`);

// ---------- A3 reachability from the first step ----------
const rooted = steps[0]?.id;
if (rooted) {
  const reach = new Set([rooted]);
  let changed = true;
  while (changed) {
    changed = false;
    for (const s of steps) {
      if (reach.has(s.id)) continue;
      if ((s.depends_on ?? []).some((d) => reach.has(d))) {
        reach.add(s.id);
        changed = true;
      }
    }
  }
  const orphans = steps.filter((s) => !reach.has(s.id)).map((s) => s.id);
  if (orphans.length) problems.push(`A3 ${orphans.length} step(s) unreachable from ${rooted}: ${orphans.join(', ')}`);
}

// ---------- A4 / A5 packet vs registry ----------
for (const s of steps) {
  const body = packets.get(s.id);
  if (!body) {
    problems.push(`A4 ${s.id} has no packet in spec.md`);
    continue;
  }
  const pf = featuresOf(body);
  const rf = new Set(s.fr ?? []);
  if (pf === null) {
    if (rf.size) problems.push(`A4 ${s.id} has no **Features:** line but the registry claims ${rf.size} FR(s)`);
  } else {
    const missingInPacket = [...rf].filter((f) => !pf.has(f));
    const missingInRegistry = [...pf].filter((f) => !rf.has(f));
    if (missingInPacket.length) problems.push(`A4 ${s.id} registry owns ${missingInPacket.join(', ')} but the packet does not list them`);
    if (missingInRegistry.length) problems.push(`A4 ${s.id} packet lists ${missingInRegistry.join(', ')} but the registry does not own them`);
  }
  const pe = effortOf(body);
  if (pe === null) problems.push(`A5 ${s.id} packet has no **Effort:** line`);
  else if (Math.abs(pe - s.effort) > 1e-9) problems.push(`A5 ${s.id} packet says ${pe} days, registry says ${s.effort}`);
}

// ---------- A6 slices ----------
const MAX = sliceDoc.max_effort_per_slice ?? 1;
for (const s of steps) {
  const list = byStep.get(s.id) ?? [];
  const sum = Number(list.reduce((a, x) => a + (x.effort ?? 0), 0).toFixed(2));
  if (!list.length) problems.push(`A6 ${s.id} has no slices`);
  else {
    if (Math.abs(sum - s.effort) > 0.011) problems.push(`A6 ${s.id} slices sum to ${sum}, packet says ${s.effort}`);
    const over = list.filter((x) => (x.effort ?? 0) > MAX + 1e-9).map((x) => `${x.id}=${x.effort}d`);
    if (over.length) problems.push(`A6 slice(s) over ${MAX}d: ${over.join(', ')}`);
  }
}

// ---------- A7 thin packets ----------
const AUTHORED = new Set(
  sliceDoc.slices.filter((x) => x.source === 'authored').map((x) => x.step),
);
for (const s of steps) {
  const items = buildItemsOf(packets.get(s.id) ?? '');
  const list = byStep.get(s.id) ?? [];
  if (s.effort >= 3 && items < 5 && !AUTHORED.has(s.id)) {
    warnings.push(`A7 ${s.id} is ${s.effort}d with only ${items} build item(s) and no authored override — likely under-specified`);
  }
  if (items > list.length && s.effort > 1) {
    warnings.push(`A7 ${s.id} has ${items} build items but ${list.length} slice(s) — some items were merged`);
  }
}

// ---------- A8 test-first gaps ----------
const noTest = sliceDoc.slices.filter((x) => !x.test && x.kind !== null);
if (noTest.length) {
  const byStepCount = new Map();
  for (const x of noTest) byStepCount.set(x.step, (byStepCount.get(x.step) ?? 0) + 1);
  warnings.push(
    `A8 ${noTest.length} slice(s) on ${byStepCount.size} step(s) name no test yet (kind ≠ docs) — they cannot start until one is named`,
  );
}

// ---------- report ----------
const totalEffort = steps.reduce((a, s) => a + s.effort, 0);
console.log(
  `PLAN AUDIT  ${steps.length} steps · ${sliceDoc.slices.length} slices · ${totalEffort} agent-days · ` +
    `${packets.size} packets · max ${MAX}d/slice`,
);
console.log(
  `  dependencies ${graph.size} nodes · ${[...graph.values()].reduce((a, d) => a + d.length, 0)} edges · ` +
    `${cycles.length} cycle(s) · ${steps.filter((s) => !(s.depends_on ?? []).length).length} root(s)`,
);

if (problems.length) {
  console.log(`\nFAIL (${problems.length}) — structural defects that will cost rework:`);
  for (const p of problems) console.log('  -', p);
} else {
  console.log('\nOK  A1–A6 all pass: dependencies resolve, no cycles, every step reachable, packets and registry agree, slices sum.');
}
if (warnings.length) {
  console.log(`\nWARN (${warnings.length}) — judgement calls, not defects:`);
  for (const w of warnings) console.log('  -', w);
}

if (strict && problems.length) process.exit(1);
