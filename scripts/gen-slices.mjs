#!/usr/bin/env node
// Generates docs/slices.json — the execution layer of the plan. See docs/STEP-GRANULARITY.md.
//
//   node scripts/gen-slices.mjs           summary only (writes nothing)
//   node scripts/gen-slices.mjs --write   rewrite docs/slices.json
//   node scripts/gen-slices.mjs --check    exit 1 if docs/slices.json is stale (used by CI)
//
// A step is a *planning* unit (goal, FRs, files, verify). A slice is an *execution* unit:
// at most 1 agent-day, one seam, one failing test before it starts. This script derives
// slices from each step packet's numbered Build items so the two layers can never drift.
//
// When a packet does not contain enough Build items to cover its effort, OVERRIDES supplies
// hand-written titles. Titles are never invented for a step that has real Build items.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const SPEC = join(root, 'spec.md');
const OUT = join(root, 'docs/slices.json');

const MAX_EFFORT = 1.0;   // hard ceiling for one slice, in agent-days
const MIN_EFFORT = 0.05;  // anything smaller is not worth a commit
const STEP = 0.05;        // effort granularity

// Seams are the only accepted "layers" of a slice. One slice touches one seam.
const SEAMS = ['schema', 'domain', 'http', 'ui', 'test', 'docs', 'ops', 'module', 'contract'];

// Steps whose packet has too few Build items for their effort: titles written by hand
// from the packet. Effort is still apportioned by this script, never hand-typed.
const OVERRIDES = {
  'S0.5': [
    'postgres.js client singletons (runtime + service), prepare: false',
    'withTenant(): claims, request id, transaction wrapper',
    'Numeric safety: money returns string, explicit parser for OID 1700',
    'Proof test: current_user is app_runtime and rolbypassrls is false',
  ],
  'S1.15': [
    'Portal — Home (balances, next payout, action items, checklist)',
    'Portal — Invoices (list, create, detail timeline, PDF, link, remind, void)',
    'Portal — Transactions (unified list, filters, bounded export, attempts)',
    'Portal — Balances (four buckets, "why?" explainer, ledger drill-down)',
    'Portal — Payouts (schedule, request, cancel, history, receipt, holds)',
    'Portal — Refunds (list, create dialog, status)',
    'Portal — Team (members, roles, invite, remove, pending)',
    'Portal — Settings (branding, bank accounts, notifications, security)',
    'Portal — Support and Developers (tickets, API keys, webhooks)',
    'Portal rules: query budget ≤ 6, no optimistic money, 44px targets, EN/BN',
  ],
  'S2.16': [
    'High-contrast light/dark token sets with per-user preference',
    'Contrast validator in CI (7:1 text, 3:1 borders)',
    'Full EN/BN parity: message lint on missing keys, Bengali numerals, Intl formatting',
    'Screenshot diff per locale for 10 key screens',
    'Accessibility gates: axe on 20 routes × 2 viewports × 2 themes',
    'Keyboard-only and screen-reader evidence in docs/QA-A11Y.md',
    'Performance gates: Lighthouse budgets, size-limit, query-count budget wired into CI',
  ],
  'S3.1': [
    'Routing table (country, MCC, amount band, brand, currency) → processor',
    'Routing rules admin UI with dry-run preview',
    'Circuit breaker: 5 failures / 60s → open 30s, before authorization only',
    'Cost-aware ordering (interchange + spread) as configurable tie-breaker',
    'Cross-processor idempotency: one attempt chain, one ledger posting',
    'Webhook normalisation and per-processor signature verification',
    '30-case routing matrix test and failover idempotency test',
    'A/B reporting: approval rate and cost per route, monthly review doc',
    'Kill-primary drill in staging: one ledger transaction through the secondary',
  ],
  'S3.2': [
    'Currency model: invoice vs settlement vs payout; fx_quotes with 60s window',
    'Locked quote at payout creation; spread posted as its own ledger entry',
    'Rate source: partner API plus fallback table with 15-minute staleness guard',
    'Corridor capability matrix, per-corridor limits and document requirements',
    'Local rail adapters (ACH/EFT/SEPA/UPI/bKash-class) behind the partner interface',
    'Remittance advice PDF: sent, rate, fee, received, reference, compliance footer',
    'Realized vs unrealized FX accounts and month-end revaluation job',
    'Revaluation report tying to the ledger; spread accounting test',
    'Disclosure UX: exact received amount before confirm, invoice currency to buyer',
    'Unsupported corridor returns a typed error, never a silent fallback',
    'Sandbox end-to-end: USD invoice paid, BDT payout executed, ledger proves spread',
    'Corridor and FX failure-mode runbook entry',
  ],
  'S3.3': [
    'Withholding: treaty rate by country and form type, applied at payout',
    'Payout blocked when the tax form is missing or expired',
    '1099-K aggregation: thresholds, per-payee totals, filer file export',
    '1042-S batch generation plus correction files',
    'TIN validation: format and checksum where applicable',
    'Filer adapter interface submitFiling(batch) with sandbox implementation',
    'Filing status tracking, retries and immutable filing records',
    'Tax engine adapter computeTax() with product tax-code mapping',
    'Fallback to the internal engine when the tax adapter fails',
    'Year-end packet: merchant PDF/CSV (gross, fees, refunds, disputes, withheld)',
    'Ledger tie-out: filings must match tax_withholding and fee_charged',
    'Threshold-boundary and adapter-failure test matrix',
  ],
  'S3.7': [
    'Digest engine: batching, quiet hours, dedupe window',
    'Scheduled reports: per-user cadence, format, signed expiring link',
    'Report delivery log, failure retry and bounce handling',
    'One-click unsubscribe per category, honoured everywhere',
    'Promotions and waivers: codes, scope, expiry, audit, granted-value report',
    'Preference centre: every channel × category with a "why am I getting this" note',
  ],
  'S3.8': [
    'SSO (SAML 2.0 / OIDC) for staff, with role mapping',
    'SSO for enterprise merchants plus SCIM-lite provisioning',
    'Break-glass local admin with hardware MFA',
    'Custom checkout domains: CNAME, certificate automation, per-host CSP',
    'Partitioning: ledger_entries, audit.log, api_request_logs by month',
    'Partition routing correctness test and maintenance job',
    'Read replica for reports, with a staleness-safe query path',
    'Connection pooling review and cache decisions recorded in an ADR',
    'Multi-region DR design documented (active-passive, RPO/RTO)',
    'Quarterly failover drill executed and the report filed',
    'SOC 2 Type I readiness: control matrix and evidence collection',
    'ISO 27001 gap assessment, DPAs and sub-processor list',
    'Security whitepaper for enterprise reviewers',
    'Contractual SLA, status page and incident comms templates',
    'Enterprise pilot rehearsal: SSO login on a custom domain, end to end',
  ],
};

// Titles that read badly when cut from a Build item; keep the intent, lose the noise.
const TITLE_FIX = {
  'S0.6.1': 'Migration 0003_identity.sql — identity, sessions, MFA, login attempts',
  'S0.9.1': 'audit.log table, hash chain, append-only grants',
  'S1.5.1': 'Migration 0012_ledger.sql — accounts, entries, postings, constraints',
  'S1.11.1': 'Payment completion transaction: verify, lock, post, receipt',
  'S1.12.1': 'Inbound webhook endpoint: verify, dedupe, persist, enqueue',
  'S2.1.1': 'Migration 0022_disputes.sql — disputes, evidence, deadlines, ratio',
};

// Phase 0 and Phase 1 slices have been read against their packets; later phases are
// drafts the agent must confirm before it starts the step (the checker enforces this).
const REVIEWED_PHASES = [0, 1];

const spec = readFileSync(SPEC, 'utf8');
const lines = spec.split('\n');

// ---------- parse step packets ----------
const heads = [];
lines.forEach((l, i) => {
  const m = l.match(/^### (S\d+\.\d+) — (.+)$/);
  if (m) heads.push({ id: m[1], title: m[2].trim(), at: i });
});

const steps = heads.map((h, k) => {
  const body = lines.slice(h.at, k + 1 < heads.length ? heads[k + 1].at : lines.length).join('\n');
  const effort = Number((body.match(/\*\*Effort:\*\*\s*([\d.]+)/) ?? [])[1] ?? 0);
  const verify = (body.match(/\*\*Verify:\*\*\s*(.+)/) ?? [])[1]?.trim() ?? '';
  const build = body.match(/^\*\*Build[^*]*\*\*([\s\S]*?)(?=^\*\*|^---|^### )/m);
  let inner = build ? build[1] : '';
  inner = inner.replace(/```[\s\S]*?```/g, ''); // numbered lines inside code are not items
  const items = inner
    .split('\n')
    .filter((l) => /^\d+\.\s/.test(l))
    .map((l) => l.replace(/^\d+\.\s*/, '').replace(/\*\*/g, '').replace(/`/g, '').trim());
  const dependencies = (body.match(/\*\*Depends on:\*\*\s*([^.]*)\./) ?? [])[1]?.trim() ?? '';
  return { ...h, body, effort, verify, items, dependencies };
});

// ---------- helpers ----------
// The seam is decided by WHERE the change lands first, and only then by what the sentence says. Reading
// keywords out of a long step title mislabels slices ("add shadcn primitives … table …" is UI, not schema).
const slugSeam = (item, stepTitle = '') => {
  const text = String(item);

  // 1. an explicit path in the item wins outright
  const pathMatch = text.match(/(?:src|supabase|tests|scripts|docs|deck)\/[\w./()\[\]-]+/);
  if (pathMatch) {
    const p = pathMatch[0].toLowerCase();
    if (p.endsWith('.css')) return 'ui';
    if (p.startsWith('supabase/migrations')) return 'schema';
    if (p.startsWith('src/components') || p.startsWith('src/app/(') || p.startsWith('src/app/design')) return 'ui';
    if (p.startsWith('src/app/api') || p.startsWith('src/app/')) return 'http';
    if (p.startsWith('tests/') || p.startsWith('scripts/')) return 'test';
    if (p.startsWith('docs/')) return 'docs';
    if (p.includes('/ledger/') || p.includes('/money/')) return 'domain';
    if (p.includes('/processors/')) return 'contract';
    if (p.includes('/webhooks/')) return 'http';
    if (p.includes('/security/')) return 'module';
    return 'module';
  }

  // 2. otherwise, the item's own wording — never the whole step title
  const t = text.toLowerCase();
  if (/\b(migration|\.sql|schema|index|constraint|rls|policy|partition|column|trigger|grant)\b/.test(t)) return 'schema';
  if (/\b(page|screen|component|layout|form|portal|theme|css|nav|dialog|dashboard|badge|gallery|shot)\b/.test(t)) return 'ui';
  if (/\b(route|endpoint|openapi|sdk|webhook|http|csp|header)\b/.test(t)) return 'http';
  if (/\b(test|suite|harness|fixture|fuzz|matrix|drill|budget|lint|pass)\b/.test(t)) return 'test';
  if (/\b(adapter|interface|contract|provider|signature|normalis|normaliz)\b/.test(t)) return 'contract';
  if (/\b(doc|readme|runbook|adr|whitepaper|pack|onboarding guide)\b/.test(t)) return 'docs';
  if (/\b(scaffold|toolchain|tsconfig|eslint|package\.json)\b/.test(t)) return 'ops';
  if (/\b(ci|workflow|deploy|docker|vercel|backup|monitor|slo|environment|cron)\b/.test(t)) return 'ops';

  // 3. last resort: the step's own title, which is at least about one topic
  const tt = String(stepTitle).toLowerCase();
  if (/\b(design|ui|screen|portal|console|cms|shell)\b/.test(tt)) return 'ui';
  if (/\b(migration|schema|rls|bootstrap|trigger)\b/.test(tt)) return 'schema';
  if (/\b(api|webhook|rest|endpoint)\b/.test(tt)) return 'http';
  if (/\b(ci|deploy|operations|backup|monitor|scaffold|toolchain)\b/.test(tt)) return 'ops';
  if (/\b(ledger|fee|money|invoice|payment|payout|refund|tax|fx)\b/.test(tt)) return 'domain';
  return 'module';
};

const KIND = {
  schema: 'rls',
  domain: 'property+unit',
  module: 'unit',
  contract: 'contract',
  http: 'integration',
  ui: 'e2e',
  test: 'unit',
  ops: 'smoke',
  docs: null,
};

// The test file a slice must create *before* the code exists. Derived so that G5 (a step cannot start on a
// slice with no named test) is satisfiable on day one, and so the agent never has to invent a location.
// A packet may override it; the path is a proposal, not a rule.
const TEST_DIR = {
  rls: 'tests/rls',
  'property+unit': 'tests/unit',
  unit: 'tests/unit',
  contract: 'tests/contract',
  integration: 'tests/integration',
  e2e: 'tests/e2e',
  smoke: 'tests/smoke',
};
const slugOf = (s) =>
  s
    .toLowerCase()
    .replace(/`/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 42)
    .replace(/-$/, '');
const testPathFor = (kind, id, title) => {
  if (!kind) return null;
  const dir = TEST_DIR[kind] ?? 'tests/unit';
  const ext = kind === 'e2e' ? 'spec.ts' : 'test.ts';
  return `${dir}/${id.toLowerCase()}-${slugOf(title)}.${ext}`;
};

const clean = (s) =>
  s
    .replace(/`/g, '')
    .replace(/\*\*/g, '')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();

const truncate = (t, n) => (t.length <= n ? t : `${t.slice(0, n - 1).replace(/\s\S*$/, '')}…`);

const titleOf = (item) => {
  const raw = clean(item);
  const dash = raw.search(/\s+[—–]\s+/);
  if (dash === -1) return truncate(raw.replace(/[:\s]+$/, ''), 92);
  const left = raw.slice(0, dash).trim().replace(/[:\s]+$/, '');
  const right = raw.slice(dash).replace(/^\s+[—–]\s+/, '').trim();
  // A label of three or more words is descriptive enough on its own ("Migration 0012_ledger.sql"
  // is two, "Ledger builders src/lib/ledger/builders.ts" is four).
  if (left.split(/\s+/).length >= 3) return truncate(left, 92);
  const room = 92 - left.length - 3;
  return room < 20 ? truncate(left, 92) : `${left} — ${truncate(right, room)}`;
};

const apportion = (total, n) => {
  // Spread `total` over `n` slices, each ≤ MAX_EFFORT, summing exactly to total.
  const out = [];
  let left = total;
  for (let i = 0; i < n; i += 1) {
    const rest = n - i;
    let v = Math.min(MAX_EFFORT, left / rest);
    v = Math.round(v / STEP) * STEP;
    v = Math.max(MIN_EFFORT, v);
    if (i === n - 1) v = Number(left.toFixed(2));
    out.push(Number(v.toFixed(2)));
    left = Number((left - v).toFixed(2));
  }
  return out;
};

// ---------- build slices ----------
const slices = [];
const problems = [];

for (const s of steps) {
  const phase = Number(s.id.match(/^S(\d)/)[1]);
  const whole = s.effort <= MAX_EFFORT + 1e-9; // already slice-sized: do not shatter it
  const minSlices = Math.max(1, Math.ceil(s.effort - 1e-9));
  const titles = whole ? [s.title] : OVERRIDES[s.id] ?? s.items.map(titleOf);
  const wanted = Math.max(minSlices, titles.length, 1);
  let list = titles.slice(0, wanted);
  while (list.length < wanted) list.push(`${s.title} — remaining work`);

  const efforts = apportion(s.effort, list.length);
  list.forEach((t, i) => {
    const id = `${s.id}.${i + 1}`;
    const title = TITLE_FIX[id] ?? t;
    const seam = slugSeam(s.items[i] ?? title, title);
    slices.push({
      id,
      step: s.id,
      phase,
      title,
      seam,
      kind: KIND[seam],
      effort: efforts[i],
      gate: s.verify || 'pnpm gate',
      test: testPathFor(KIND[seam], id, title), // the file that must exist and fail before the code
      reviewed: REVIEWED_PHASES.includes(phase) || Boolean(OVERRIDES[s.id]),
      source: OVERRIDES[s.id] ? 'authored' : 'derived',
      status: 'pending',
    });
  });

  const sum = efforts.reduce((a, b) => a + b, 0);
  if (Math.abs(sum - s.effort) > 0.011) problems.push(`${s.id}: slices sum to ${sum}, packet says ${s.effort}`);
  if (efforts.some((e) => e > MAX_EFFORT + 1e-9)) problems.push(`${s.id}: a slice exceeds ${MAX_EFFORT} day`);
}

const doc = {
  version: 1,
  plan: 'spec.md',
  registry: 'docs/steps.json',
  doctrine: 'docs/STEP-GRANULARITY.md',
  updated: '2026-11-01',
  max_effort_per_slice: MAX_EFFORT,
  seams: SEAMS,
  note:
    'Execution layer. Every step in docs/steps.json is decomposed into slices of at most one ' +
    'agent-day, each touching one seam. Derived slices carry reviewed=false until the executing ' +
    'agent confirms them against the packet; a step cannot move to in_progress while any of its ' +
    'slices is unreviewed or has no named test. Regenerate with: node scripts/gen-slices.mjs --write',
  slices,
};

// ---------- output ----------
const totalEffort = steps.reduce((a, s) => a + s.effort, 0);

if (problems.length) {
  console.error('Slice derivation failed:');
  for (const p of problems) console.error(' -', p);
  process.exit(1);
}

if (process.argv.includes('--write')) {
  writeFileSync(OUT, `${JSON.stringify(doc, null, 2)}\n`);
  console.log(`wrote docs/slices.json — ${slices.length} slices over ${steps.length} steps`);
} else if (process.argv.includes('--check')) {
  const current = existsSync(OUT) ? readFileSync(OUT, 'utf8') : '';
  const next = `${JSON.stringify(doc, null, 2)}\n`;
  if (current !== next) {
    console.error('docs/slices.json is stale — run: node scripts/gen-slices.mjs --write');
    process.exit(1);
  }
  console.log(`docs/slices.json up to date — ${slices.length} slices over ${steps.length} steps`);
} else {
  const biggest = [...slices].sort((a, b) => b.effort - a.effort).slice(0, 3);
  console.log(`${steps.length} steps · ${slices.length} slices · ${totalEffort.toFixed(1)} agent-days`);
  console.log(`largest slices: ${biggest.map((b) => `${b.id} ${b.effort}d`).join(', ')}`);
  const bySeam = slices.reduce((a, s) => ((a[s.seam] = (a[s.seam] ?? 0) + 1), a), {});
  console.log(`by seam: ${Object.entries(bySeam).map(([k, v]) => `${k} ${v}`).join(' · ')}`);
  console.log('run with --write to regenerate docs/slices.json');
}
