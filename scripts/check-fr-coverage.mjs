#!/usr/bin/env node
// FR traceability gate. See spec.md Appendix B and §9.
// Fails if any requirement in the master spec §35 matrix is unowned, double-owned,
// or if Appendix B disagrees with docs/steps.json.
import { readFileSync } from 'node:fs';

const read = (p) => readFileSync(new URL(`../${p}`, import.meta.url), 'utf8');
const spec = read('docs/MASTER_SPECIFICATION.md');
const plan = read('spec.md');
const registry = JSON.parse(read('docs/steps.json'));

const FR = /FR-[A-Z]+-\d{3}/;

// 1. every FR row in the master spec traceability matrix
const frs = new Set();
for (const line of spec.split('\n')) {
  if (/^\|\s*`?FR-/.test(line)) {
    const m = line.match(FR);
    if (m) frs.add(m[0]);
  }
}

// 2. Appendix B reverse table: | `FR-X-NNN` | ... | owner |
const owner = new Map();
const appB = plan.slice(plan.indexOf('### B.1 Reverse lookup'));
for (const line of appB.split('\n')) {
  const cells = line.split('|').map((c) => c.trim());
  if (cells.length < 6) continue;
  const fr = cells[1].replaceAll('`', '');
  const step = cells[4];
  if (!/^FR-[A-Z]+-\d{3}$/.test(fr) || !/^S\d\.\d+$/.test(step)) continue;
  if (owner.has(fr)) {
    console.error(`double-owned: ${fr} → ${owner.get(fr)} and ${step}`);
    process.exitCode = 1;
  }
  owner.set(fr, step);
}

// 3. registry features must agree with Appendix B
const norm = (f) => (f.startsWith('FR-') ? f : `FR-${f}`);
const reg = new Map(registry.steps.map((s) => [s.id, new Set((s.fr ?? s.features ?? []).map(norm))]));
for (const [fr, step] of owner) {
  if (!reg.has(step)) { console.error(`unknown step ${step} for ${fr}`); process.exitCode = 1; continue; }
  if (!reg.get(step).has(fr) && reg.get(step).size) console.error(`registry/Appendix B mismatch: ${fr} owned by ${step}, missing from steps.json features`);
}

const unowned = [...frs].filter((f) => !owner.has(f));
const orphan = [...owner.keys()].filter((f) => !frs.has(f));
if (unowned.length) console.error(`unowned requirements (${unowned.length}): ${unowned.join(', ')}`);
if (orphan.length) console.error(`owned but not in master spec §35 (${orphan.length}): ${orphan.join(', ')}`);

console.log(`${frs.size} requirements · ${owner.size} owned · ${unowned.length} unowned · ${orphan.length} unknown · ${registry.steps.length} steps`);
if (unowned.length || orphan.length) process.exitCode = 1;
