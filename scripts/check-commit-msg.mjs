#!/usr/bin/env node
// Commit-message check. See CONTRIBUTING.md §4 and spec.md §13.1a.
//
//   node scripts/check-commit-msg.mjs .git/COMMIT_EDITMSG
//
// Rules:
//   1. subject matches `type(scope): summary`, type from the allowed set, <= 100 chars
//   2. a commit touching code must carry `Slice: S<step>.<n>` naming a real slice
//   3. a docs-only commit must not claim a slice (it would corrupt the progress ledger)
//
// Installed via `git config core.hooksPath .githooks`. No dependencies.
import { readFileSync, existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const msgFile = process.argv[2];
if (!msgFile || !existsSync(msgFile)) {
  console.error('check-commit-msg: pass the message file, e.g. .git/COMMIT_EDITMSG');
  process.exit(2);
}

const message = readFileSync(msgFile, 'utf8');
const lines = message.split('\n');
const subject = (lines.find((l) => l.trim() && !l.startsWith('#')) ?? '').trim();
const TYPES = ['feat', 'fix', 'chore', 'ci', 'docs', 'test', 'refactor', 'perf', 'build', 'revert'];
const errors = [];

// ---- 1. subject ----
const m = subject.match(/^(\w+)(?:\(([^)]+)\))?: (.+)$/);
if (!m) {
  errors.push(`subject must be "type(scope): summary" — got: "${subject}"`);
} else {
  const [, type, scope, summary] = m;
  if (!TYPES.includes(type)) errors.push(`type "${type}" is not one of ${TYPES.join('|')}`);
  if (!scope) errors.push('scope is required: a step id (S1.5), FR ids (FR-LDG-001), or a doc area (docs, deck, plan)');
  if (summary.length < 10) errors.push('summary is too short to be useful');
}
if (subject.length > 100) errors.push(`subject is ${subject.length} chars (max 100)`);

// ---- 2. which files does this commit touch? ----
let staged = [];
try {
  staged = execSync('git diff --cached --name-only', { cwd: root, encoding: 'utf8' })
    .split('\n')
    .map((f) => f.trim())
    .filter(Boolean);
} catch {
  /* no index (e.g. --amend on the initial commit) — skip the file check */
}

// Product code only. `scripts/`, `.githooks/`, `docs/` and `deck/` are tooling — a change there is not a
// slice of product work and must not be forced to claim one (a false positive disables the hook).
const CODE = /^(src|supabase|tests)\//;
const isCode = staged.some((f) => CODE.test(f));
const isDocsOnly = staged.length > 0 && !isCode;
const sliceLine = message.match(/^Slice:\s*(\S+)\s*$/m);

if (staged.length === 0) {
  // Nothing in the index (amend with no changes, or a reword): we cannot tell code from docs, so we
  // do not judge the trailer either way.
} else if (isCode) {
  if (!sliceLine) {
    errors.push('this commit touches code but has no "Slice: S<step>.<n>" trailer (see CONTRIBUTING.md §4)');
  } else {
    const id = sliceLine[1];
    let known = [];
    const slicesPath = join(root, 'docs/slices.json');
    if (existsSync(slicesPath)) {
      known = JSON.parse(readFileSync(slicesPath, 'utf8')).slices.map((s) => s.id);
    }
    if (!/^S\d+\.\d+\.\d+$/.test(id)) errors.push(`"Slice: ${id}" is not a slice id (expected S1.5.3)`);
    else if (known.length && !known.includes(id)) {
      errors.push(`"Slice: ${id}" does not exist in docs/slices.json — check the id, or regenerate with gen-slices.mjs`);
    }
  }
} else if (isDocsOnly && sliceLine) {
  errors.push(`docs-only commit claims "Slice: ${sliceLine[1]}" — drop the trailer; plan work is not a slice`);
}

// ---- verdict ----
if (errors.length) {
  console.error('\nCommit message rejected:\n');
  for (const e of errors) console.error(`  ✗ ${e}`);
  console.error('\nFormat:\n  type(scope): summary\n\n  Why, in one or two sentences.\n\n  Refs: FR-XXX-001\n  Slice: S1.5.3\n');
  process.exit(1);
}
