#!/usr/bin/env node
// Claude Code PostToolUse hook: after a Write/Edit to a markdown doc, run the docs gate immediately.
//
// The hook receives JSON on stdin from Claude Code (tool_name, tool_input, ...). We only act on edits to the
// documents `check-docs.mjs` validates; everything else is silent, so the hook never becomes noise.
//
// Wired in .claude/settings.json. Exits 0 always — a noisy exit code would stop Claude's work for a typo;
// the failure is reported in the output instead, which Claude reads and fixes on the next turn.
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative, isAbsolute } from 'node:path';
import { readFileSync } from 'node:fs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..');

let payload = '';
try {
  payload = readFileSync(0, 'utf8'); // stdin
} catch {
  process.exit(0);
}

let file = '';
try {
  const ev = JSON.parse(payload);
  file = ev?.tool_input?.file_path ?? ev?.tool_input?.path ?? '';
} catch {
  process.exit(0);
}
if (!file) process.exit(0);

const rel = isAbsolute(file) ? relative(root, file) : file;
const WATCHED = /^(spec\.md|CONTRIBUTING\.md|README\.md|docs\/.+\.md)$/;
if (!WATCHED.test(rel)) process.exit(0);

try {
  const out = execFileSync(process.execPath, [join(root, 'scripts', 'check-docs.mjs')], {
    cwd: root,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  // Only speak when something is wrong; silence keeps the context clean.
  if (out.includes('0 problem(s)')) {
    console.log(`doc-gate: ${rel} — docs integrity ok`);
  }
} catch (err) {
  const detail = `${err.stdout ?? ''}${err.stderr ?? ''}`.trim().split('\n').slice(0, 12).join('\n');
  console.log(
    `doc-gate: ${rel} broke a documentation rule. Fix it before continuing.\n${detail}`,
  );
}
process.exit(0);
