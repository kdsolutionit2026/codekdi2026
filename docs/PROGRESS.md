# Build Progress

> Maintained by the AI agent per `spec.md` §13. Newest entry first. Update it at the end of every session.

## Status

- **Current phase:** Phase 0 — not started (0 of 61 steps done; 0 of 402 slices done)
- **Last completed step:** none
- **Next step:** S0.1 — repository scaffold and toolchain (`npm`-free: `pnpm`)
- **Steps total:** 61 (14 phase 0 · 21 phase 1 · 18 phase 2 · 8 phase 3) — see `docs/steps.json`
- **Slices:** 402, every one ≤ 1 agent-day, 279 reviewed (phases 0–1) — see `docs/slices.json`
- **Blocked by:** nothing
- **Last environment check:** 2026-11-01 — repository contains docs, the plan checkers, the slice registry and four decks (`deck/`); no application code yet

## Log (newest first)

### 2026-11-01 (fourth) — the build book
- Done: `docs/BUILD-BOOK.md` (700 lines) — the guide a first-time vibe coder follows end to end: what to read first (tiered, with time estimates), the 22-file library in reading order, the serial order of all 61 chapters in 4 acts, 20 milestones with the day each becomes demonstrable, the 9-step session procedure, context discipline for agents, the 9-rung test ladder with the 8 tests a PayFac always skips, the weekly 5-slice audit, the 6-step repair procedure and its 3 false fixes, the 3-seat model for cross-agent review, the processor rules in the order they bite, a 13-week plan, and a printable cheat sheet
- Done: `scripts/next.mjs` — `node scripts/next.mjs` prints the next chapter, its slices (reviewed / tested flags), the commands to run and what comes after; `--order` is the full serial build order (greedy topological sort in chapter order); `--all` lists only what is unblocked
- Done: spec §19.4 documents the book and the navigator; README, CONTRIBUTING and CLAUDE.md now start from the book; check-docs covers 11 documents
- Gate: check-docs 0 (11 files) · check-fr 241/241 · gen-slices --check current · check-steps --strict exit 0
- Deviations: none
- Next: S0.1

### 2026-11-01 (third) — the Claude operating kit
- Done: `CLAUDE.md` — auto-loaded project memory: what to read (and never read), the non-negotiables, the loop, the commands, the two-strike rule
- Done: `.claude/commands/` — six project slash commands with tool allowlists: `/kickoff`, `/verify`, `/ui`, `/review`, `/adapter`, `/ship`; `.claude/agents/reviewer.md` as a read-only subagent
- Done: `.claude/settings.json` — permission allowlist (gates, git, pnpm, Playwright MCP) and deny rules that block `--no-verify`, force-push and reading `.env*`; a `PostToolUse` hook runs the docs gate after any doc edit (silent when green, reports drift when red — verified both ways)
- Done: `docs/BUILD-WITH-CLAUDE.md` — the operating manual: 20-minute setup, Playwright MCP for live preview, the eight-step slice loop, the proof ladder (8 rungs), the UI checklist at 360/768/1440, the processor-adapter rules and 8 checks, the 10 failure modes, the plan-defect fast lane, metrics, and copy-paste prompts
- Done: S0.4 gains `tests/visual/shots.mjs` (`pnpm shots <route>` → screenshots at three widths + BN), so "Claude looked at the screen" is a repeatable command rather than an intention. Slices 401 → 402
- Gate: check-docs 0 (10 files) · check-fr 241/241 · gen-slices --check current · check-steps --strict --granularity exit 0
- Deviations: none
- Next: S0.1

### 2026-11-01 (later) — change playbook, troubleshooting ladder, ADRs
- Done: `docs/CHANGE-PLAYBOOK.md` — 12 extension recipes with a **do-not-touch** column (new provider/currency/country/method/report/permission/language/event/page/price/plan step), blast-radius tiers A/B/C, public-surface versioning + 90-day deprecation policy, and the metrics that say the platform is still easy to change
- Done: `docs/TROUBLESHOOTING.md` — ten symptom families with checks ordered cheapest-first (RLS empty results, wrong money, stuck payments, double posts, missing webhooks, dead jobs, bad PDFs, random sign-outs, local-vs-Vercel, CI-only flakes), each tied to the pitfall number in §11
- Done: `docs/adr/` — index + template + ADR 0001 (interface freeze); `check-docs` now validates 8 documents including the three new ones
- Done: `spec.md` §20.4 (change playbook + tiers), §20.5 (plan defect vs rule change — the fast lane), §11 pointer to the ladder
- Gate: check-docs 0 (8 files) · check-fr 241/241 · check-steps --strict exit 0 · gen-slices --check up to date
- Deviations: none
- Next: S0.1

### 2026-11-01 — execution layer: slices, test-first and frozen contracts
- Done: `scripts/gen-slices.mjs` + `docs/slices.json` — every step decomposed mechanically from its `**Build**` list into **402 slices of ≤ 1 agent-day** (max 1.0, sum 253.0 = the plan's effort). Slices carry `seam`, `kind`, `gate`, `test`, `reviewed`, `status`; the file is generated, never hand-edited; `--check` fails CI on drift.
- Done: `docs/STEP-GRANULARITY.md` — two levels (step = product contract, slice = agent contract), rules G1–G6, the ≤400-line / one-FR / one-seam budget, the three gate tiers (<60 s / ~5 min / ~30 min), over-splitting hazards and their fixes, and the honest 60 → 402 arithmetic (most of the gain is the first split; ~1,500 is flat or worse).
- Done: `scripts/check-steps.mjs` gained `--slices` and `--granularity`, and `--strict` now also enforces G5/G6. **§19.1 preserved:** a bare run is still report-only and exits 0; only `--strict` / `--granularity` can fail. Verified both ways in a scratch copy (G2/G3/G5 fire, exit 1; bare run exit 0).
- Done: **S0.14 — interface freeze** (new step, phase 0): money, ledger posting, `PaymentProcessor` and the canonical webhook event are decided as types + a contract test *before* anything implements them. Splitting worsens interface drift; this is the fix. Phase 0 gate now requires it.
- Done: §9.1 gate tiers, §19.2 slice registry + G1–G6, §22 fourth gate + slice review rule; `docs/AGENT_PLAYBOOK.md` §4.1 rewritten as the slice loop (RED → BUILD → GATE → COMMIT); `.github/workflows/plan-gates.yml` runs all four gates on every PR.
- Gate: check-docs 0 · check-fr 241/241 (61 steps) · check-steps --strict --granularity exit 0 · gen-slices --check up to date
- Tests: n/a (no code)
- Deviations: step count 60 → 61 (S0.14 added); effort 252 → 253 agent-days
- Next: S0.1

### 2026-10-30 — component map
- Done: `docs/COMPONENTS.md` — 10 core components with plain-language purpose, owned tables, dependencies, failure symptoms and owning steps; traced $100 payment end to end; external-service table; glossary; audience guides; build-order/parallelism map; repo map; explicit non-goals
- Drift fixed while writing it: 7 tables named only in the Phase 2/3 packets (`review_schedules`, `monitoring_events`, `negative_balance_events`, `dunning_attempts`, `write_offs`, `wallet_tokens`, `offline_payments`, `import_jobs`) are now catalogued in master spec §6.16b; DB roles documented in §6.16c
- Gate: check-docs 0 (now also covers COMPONENTS.md and AGENT_PLAYBOOK.md) · check-fr 241/241 · check-steps --strict 0
- Next: S0.1

### 2026-10-29 — agent operating procedure
- Done: `docs/AGENT_PLAYBOOK.md` (agent selection, session loop, evidence standard, cross-check techniques, failure modes) + `docs/reviews/README.md`
- Verified in sandbox: PostgreSQL 18.4 runs locally via npm-bundled binaries (`embedded-postgres`) — schema, triggers, constraints and RLS are testable without Docker or the Supabase CLI
- Gate: check-docs 0 · check-fr 241/241 · check-steps --strict 0
- Next: S0.1

### 2026-10-29 — planning
- Done: master specification v1.0.0 (`docs/MASTER_SPECIFICATION.md`); build plan v1.1.0 (`spec.md`) — 61 steps, 402 slices, Appendix B requirement map (241/241 owned), Phase 2/3 packets, security/ops steps S0.12/S0.13
- Gate: `node scripts/check-docs.mjs` 0 problems · `node scripts/check-fr-coverage.mjs` 241/241 · `node scripts/check-steps.mjs --strict` exit 0
- Tests: n/a (no code)
- Deviations: none
- Next: S0.1

## Open questions raised by agents

| Date | Step | Question | Status |
|---|---|---|---|
| — | — | — | — |

## Environment record

| Item | Value |
|---|---|
| Node | (record on first run) |
| pnpm | (record on first run) |
| Next.js | (record on first run) |
| Supabase CLI | (record on first run) |
| Supabase Postgres | (record on first run) |
| Deploy target | Vercel — plan: (record; needed before S1.14 for 1-min cron) |
