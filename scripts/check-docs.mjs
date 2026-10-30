#!/usr/bin/env node
// Documentation QA. See spec.md §22. No dependencies.
// Validates the two specification files the whole build depends on.
import { readFileSync, existsSync } from 'node:fs';

const read = (p) => readFileSync(new URL(`../${p}`, import.meta.url), 'utf8');
const files = ['spec.md', 'docs/MASTER_SPECIFICATION.md', 'docs/COMPONENTS.md', 'docs/AGENT_PLAYBOOK.md'].filter((f) => existsSync(new URL(`../${f}`, import.meta.url)));
const fail = [];
const note = (file, msg) => fail.push(`${file}: ${msg}`);

const slug = (t) =>
  t.toLowerCase().replace(/[`*]/g, '').replace(/[^\p{L}\p{N}\- ]/gu, '').trim().replace(/ /g, '-');

for (const file of files) {
  const text = read(file);
  const lines = text.split('\n');

  // 1. code fences must be balanced
  const fences = lines.filter((l) => l.trim().startsWith('```')).length;
  if (fences % 2) note(file, `unbalanced code fences (${fences})`);

  // 2. table rows in one block must have the same column count
  let inCode = false, block = [], start = 0;
  const checkBlock = () => {
    if (block.length >= 2) {
      const counts = new Set(block.map((l) => (l.replace(/\\\|/g, '').match(/\|/g) ?? []).length));
      if (counts.size > 1) note(file, `table at line ${start + 1} has ragged columns ${[...counts]}`);
    }
    block = [];
  };
  lines.forEach((l, i) => {
    if (l.trim().startsWith('```')) { inCode = !inCode; return; }
    if (inCode) return;
    if (l.trim().startsWith('|')) { if (!block.length) start = i; block.push(l); } else checkBlock();
  });
  checkBlock();

  // 3. internal anchors resolve
  const headings = new Set();
  inCode = false;
  for (const l of lines) {
    if (l.trim().startsWith('```')) { inCode = !inCode; continue; }
    if (inCode) continue;
    const m = l.match(/^#{2,4} (.+)$/);
    if (m) headings.add(slug(m[1]));
  }
  for (const m of text.matchAll(/\]\(#([^)]+)\)/g)) {
    if (!headings.has(m[1])) note(file, `dead anchor #${m[1]}`);
  }
}

// 4. every step in the plan has a registry row, and vice versa
const plan = read('spec.md');
const reg = JSON.parse(read('docs/steps.json'));
const inPlan = new Set([...plan.matchAll(/^### (S\d\.\d+) — /gm)].map((m) => m[1]));
const inReg = new Set(reg.steps.map((s) => s.id));
for (const id of inPlan) if (!inReg.has(id)) note('docs/steps.json', `step ${id} exists in spec.md but not in the registry`);
for (const id of inReg) if (!inPlan.has(id)) note('spec.md', `step ${id} exists in the registry but not in spec.md`);

// 5. every step has the required packet fields
const parts = plan.split(/^### (S\d\.\d+) — .+$/m);
for (let i = 1; i < parts.length; i += 2) {
  const body = parts[i + 1].split('\n### ')[0];
  for (const field of ['**Goal:**', '**Depends on:**', '**Features:**', '**Verify:**', '**Done when:**', '**Commit:**']) {
    if (!body.includes(field)) note('spec.md', `step ${parts[i]} missing ${field}`);
  }
}

// 6. section references point at something real
const md = existsSync(new URL('../docs/MASTER_SPECIFICATION.md', import.meta.url)) ? read('docs/MASTER_SPECIFICATION.md') : '';
const planHeads = new Set([...plan.matchAll(/^#{2,4} (\d+(?:\.\d+)?)(?:\.| |$)/gm)].map((m) => m[1]));
const mdHeads = new Set([...md.matchAll(/^#{2,4} (\d+(?:\.\d+)?)(?:\.| |$)/gm)].map((m) => m[1]));
let inCode = false;
plan.split('\n').forEach((l, i) => {
  if (l.trim().startsWith('```')) { inCode = !inCode; return; }
  if (inCode) return;
  for (const m of l.matchAll(/§(\d+(?:\.\d+)?)/g)) {
    const ref = m[1];
    if (planHeads.has(ref)) continue;
    if (/master spec/i.test(l) && mdHeads.has(ref)) continue;
    note('spec.md', `unresolved §${ref} at line ${i + 1}`);
  }
});

console.log(`${fail.length} problem(s) across ${files.length} file(s)`);
for (const f of fail.slice(0, 40)) console.error(' -', f);
if (fail.length > 40) console.error(` ... and ${fail.length - 40} more`);
process.exit(fail.length ? 1 : 0);
