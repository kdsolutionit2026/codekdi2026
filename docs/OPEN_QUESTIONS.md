# Open Questions & Business Inputs

This file tracks decisions that **do not block engineering** but **do block live traffic**.
The canonical list lives in `MASTER_SPECIFICATION.md` §37. Add new items here, not in chat.

| # | Question | Owner | Needed by | Status | Default in spec |
|---|---|---|---|---|---|
| 1 | Processor contract & economics (Airwallex primary / Stripe secondary) | Founder | Phase 1 start | open | sandbox only |
| 2 | Counsel sign-off on funds flow & market entry | Founder + counsel | Phase 1 go-live | open | no live merchants |
| 3 | Supported countries + MCC allowlist | Compliance | Phase 1 | open | §0.7 |
| 4 | Reserve %, hold, payout delay per plan | Risk | Phase 1 | open | §0.7 / §9.4 |
| 5 | Refund fee policy | Finance | Phase 1 | open | fixed retained |
| 6 | Dispute fee & bearer | Finance | Phase 2 | open | $15 merchant |
| 7 | KYC/KYB vendor | Compliance | Phase 2 | open | manual + adapter |
| 8 | Sales-tax engine vendor | Product | Phase 2 | open | manual rates |
| 9 | 1099-K filer of record | Finance | Phase 3 | open | partner |
| 10 | Domain, support email, legal address | Founder | Phase 0 | open | placeholders |
| 11 | Plan pricing & entitlements | Business | Phase 2 | open | §9.4 |
| 12 | Contractual SLA | Business | Phase 2 | open | none in Phase 1 |
| 13 | Data residency region | Counsel | Phase 1 | open | US |
| 14 | Cyber/E&O insurance | Founder | Phase 2 | open | required before scale |
| 15 | Partial payments | Product | Phase 2 | open | off in Phase 1 |
| 16 | Chargeback thresholds per network | Risk | Phase 2 | open | §12.4 |
| 17 | WooCommerce embedded vs redirect | Product | Phase 2 | open | redirect |
| 18 | Absorb processor fees on refunds | Finance | Phase 2 | open | no |

**How to close an item:** record the decision, the date, and the person; update §37 and any affected `FR-*` row; if it changes data or money behavior, add a migration + test.
