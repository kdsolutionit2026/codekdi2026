# Speaker notes — KD PAY × Airwallex

Compiled from the notes pane of `KD-PAY-Airwallex-Partnership.pptx`. The same text is embedded in the
deck, so Presenter View shows it while you speak. Numbers in brackets are rough timings for a 25-minute slot.

---

## Slide 01 — Payments infrastructure for Asia's cross-border merchants

Opening (45 seconds). We are KD PAY LLC. We process about $800K a month at a 0.01% chargeback rate, and we want to build our platform on Airwallex. In this deck: who we are, the Asia gap we serve, our Phase 1 product, the exact partnership model we propose, and our security posture.

## Slide 02 — What we are asking for

This is the only slide that matters if the meeting is cut short. We want the ledger model at launch because it gets us live in weeks; connected accounts come later as volume justifies KYB cost. We are not asking for special treatment on risk — we are showing a 0.01% dispute record and asking for pricing that reflects it.

## Slide 03 — Who we are

Be upfront about the entity change before they ask: the team and book of business are from 2022, the LLC is new. We will provide statements from the current providers and references under NDA. The engineering claim is the differentiator — we are building a real ledger, not reselling a gateway.

## Slide 04 — A small book with clean risk

The point of this slide is risk quality, not size. $800K/month is small for Airwallex; 0.01% is unusually clean. Say it plainly: we would rather bring you 50 good merchants than 500 bad ones. We will supply 12 months of statements and dispute data under NDA.

## Slide 05 — Asian merchants can sell globally. They cannot get paid globally.

This is the slide that explains the business. Every point is something we hear from merchants weekly. Avoid quoting decline percentages unless we have our own data in the appendix — 'materially higher' is defensible, a made-up number is not.

## Slide 06 — Asia first, then the world

Ask them directly: which of these corridors can you support today, and which are 6-12 months away? That answer re-orders our roadmap. We are deliberately not promising all of Asia on day one.

## Slide 07 — One integration, three ways for a merchant to plug in

Phase 1 is deliberately boring: hosted checkout, two plugins, an API. That is what gets merchants live. Everything else — invoicing, payouts, disputes — is already scoped and comes with the same release train.

## Slide 08 — Where the card data goes — and where it never goes

This slide answers the PCI question before they ask it. Card data lives and dies inside Airwallex Elements. Our servers see a token and a result. That is why we can launch as SAQ-A rather than spending a year and six figures on a full assessment.

## Slide 09 — Why Airwallex, specifically

Careful with the Stripe comparison — say it as a coverage observation, not a criticism. If they ask what would make us leave: coverage gaps in South Asia and pricing that does not reflect our dispute record.

## Slide 10 — Who does what — and who is merchant of record

This is the slide that shows we read their documentation. Terminology matters: seller ledger vs full connected account, capability activation, payment acceptance requiring KYB. Ask them to confirm which model they would approve for a US platform onboarding merchants in Bangladesh and Pakistan. Also ask about white-label/brand-mention guidelines for the merchant UI.

## Slide 11 — Our dispute record, against the threshold that matters

Do not overclaim: 0.01% is the trailing average across the current book. Say that, and offer the statements. The reserve sentence is the one they want to hear — platforms that fight reserves get declined. We are signalling we will fund risk.

## Slide 12 — Twelve controls we will not compromise on

Do not read all twelve. Say: 'there are twelve controls, all tested; let me highlight four'. Highlight 01 (SAQ-A: we cannot see a card number), 07 (RLS: a bug in our app still cannot leak a tenant's data), 08 (double-payment), 09 (audit chain). Offer the security architecture document as a follow-up — it is already written.

## Slide 13 — We take on the merchant risk so you focus on the rail

If they push back on the ledger model because 'we don't KYC the merchants', this is the answer: we run a real KYB pipeline, screen sanctions, monitor disputes and hold reserves. We are not a shell that pipes volume. Offer to walk them through the onboarding flow screen by screen.

## Slide 14 — Eight weeks from approval to first live payment

The timeline is the credibility test. Most platforms say 'we'll integrate' without a plan. Ours has five gates and a joint certification week. If they ask what we need from them: sandbox keys by week 2 and one solutions engineer for the certification week.

## Slide 15 — What this looks like in twelve months

Be careful not to inflate. The year-2 column is ambition. If they ask for a forecast with numbers, say we will model it with their pricing sheet and send it within a week — that is a stronger answer than an invented spreadsheet.

## Slide 16 — Four decisions to make this week

Close by asking for the two things that unblock everything: written confirmation of the model, and sandbox access. Replace the bracketed contact details before sending — they are intentionally left as placeholders.

## Slide 17 — Integration and controls, for your solutions engineer

Hand this page to their engineer. It answers the integration questions in their language: idempotency, webhook semantics, reconciliation tolerance, environment separation.

## Slide 18 — What we can provide during due diligence

Ending on the entity issue is deliberate: it is the one thing underwriting will find, so we frame it before they do. Say we would rather over-share than have it surface late in the process.
