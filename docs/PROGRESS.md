# Build Progress

> Maintained by the AI agent per `spec.md` §13. Newest entry first. Update it at the end of every session.

## Status

- **Current phase:** Phase 0 — not started (0 of 60 steps done)
- **Last completed step:** none
- **Next step:** S0.1 — repository scaffold and toolchain (`npm`-free: `pnpm`)
- **Steps total:** 60 (13 phase 0 · 21 phase 1 · 18 phase 2 · 8 phase 3) — see `docs/steps.json`
- **Blocked by:** nothing
- **Last environment check:** 2026-10-29 — repository contains only docs (`README.md`, `spec.md`, `docs/`); no application code yet

## Log (newest first)

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
- Done: master specification v1.0.0 (`docs/MASTER_SPECIFICATION.md`); build plan v1.1.0 (`spec.md`) — 60 steps, Appendix B requirement map (241/241 owned), Phase 2/3 packets, security/ops steps S0.12/S0.13
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
