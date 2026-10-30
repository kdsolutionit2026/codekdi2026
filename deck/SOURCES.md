# Sources, assumptions and open questions

Applies to **both** decks in this folder:

- `KD-PAY-Airwallex-White-Label-Proposal.pptx` — the business-model deck (17 slides). **Use this one.**
- `KD-PAY-Airwallex-Partnership.pptx` — the earlier product-focused deck (18 slides), kept for internal reference.

The rules are the same in both: every number is either yours, Airwallex's published documentation, a
widely published industry rule of thumb **(C)**, or an assumption we say out loud **(D)**. Nothing is
presented as fact unless it can be traced below.

---

## A. Figures supplied by KD PAY (use as-is, they are yours)

| Claim on the deck | Slide | Where it comes from |
|---|---|---|
| Monthly processing volume **$800,000** (≈ $9.6M annualised) | 1, 2, 3, 4, 9, 16 | Your brief. Only the ×12 annualisation is arithmetic. |
| Chargeback ratio **0.01%** | 1, 3, 4, 11 | Your brief. "1 dispute per 10,000 transactions" is the same figure restated. |
| Operating since **2022**; **KD PAY LLC** registered **October 2026** | 1, 3, 4, 18 | Your brief ("new corporate entity registered this month"). |
| Target geographies: **Asia, EU/UK, US, LatAm** | 3, 6, 15 | Your brief. Split into South Asia → South-East Asia → East Asia → Phase 3 by us. |
| **B2B and B2C**, card-not-present, USD-first | 3, 4 | Your brief ("private merchant accounts for B2B & B2C"). USD-first is stated on the slides as the current norm; correct it if a material share settles in EUR/GBP. |
| Asia-first, then global | 1, 6, 15 | Your brief. |
| Phase 1 = hosted checkout, Shopify/WooCommerce plugins, REST API | 7 | Your brief. |
| Website **kdsolutionit.com** | *not shown* | Your brief supplied it, but the site is under development, so the deck deliberately omits the URL and says "pre-launch, design-partner stage" instead. Give the URL verbally if asked. |

## B. Claims sourced from Airwallex's public documentation

| Claim on the deck | Slide | Basis |
|---|---|---|
| Two partnership models: **seller ledger** (platform is the merchant, its sellers are ledgers) vs **connected accounts** (each sub-merchant is KYC'd and holds their own account) | 2, 7, 10, 14, 15, 17 | Airwallex *Payments for Platforms / marketplaces* documentation. |
| Airwallex onboards and KYB-checks the **platform** in both models | 10, 13 | Same documentation. |
| Connected-account **capabilities arrive by webhook** | 9, 17 | Airwallex connected-accounts capability docs. |
| Multi-currency wallets, FX, **payouts to 150+ countries** | 9 | Airwallex payouts documentation. Confirm the current number with your account team — "150+" is their published figure, not ours. |
| **`capture_method: manual`**, idempotency keys, signed webhooks, 3DS/SCA support | 9, 12, 17 | Airwallex API reference. |
| UK/EEA SCA obligations sit with the entity that owns the user relationship | 6, 15 | Airwallex + PSD2 guidance; we phrase it as a sequencing constraint, not a legal opinion. |

## C. Industry figures used as context (not Airwallex-specific)

| Claim on the deck | Slide | Basis and caveat |
|---|---|---|
| Card networks begin **monitoring a merchant around 0.9% chargebacks** | 4, 11 | Visa's dispute-monitoring programmes use thresholds in the 0.9%–1.8% range depending on programme and volume band; Mastercard's are different again. The 0.9% line is the conservative end and is described on the slide as "the threshold that matters", not as a quoted rule. **Say "around" in the room.** |
| "**90× headroom**" | 11 | 0.9 ÷ 0.01 = 90. Pure arithmetic on the two figures above. |
| Cross-border card declines materially higher on offshore acquiring; 5–10 day settlement; double FX conversion | 5 | General market observation from merchant conversations, deliberately unquantified. If you have your own decline data, that is a stronger slide — bring it. |
| Prohibited MCCs, AVS postal matching for US/CA/UK, 3DS2 on VPN/Tor or IP-country mismatch | 11, 12 | Standard issuer/processor risk practice (also required in your product spec). |

## D. Assumptions we are making — confirm or correct before the meeting

| Assumption | Slide(s) | Why it matters |
|---|---|---|
| **8 weeks** from approval to first live payment (W1–2 contract, W3–4 build, W5 certification, W6 pilot, W7–8 go-live) | 14, 16 | This is *our* plan, contingent on Airwallex sandbox access, KYB turnaround and a named solutions engineer. If their onboarding is slower, the slide becomes a negotiation, not a promise. |
| **14 days** to a running sandbox integration; one named engineer on our side | 2 | Our commitment, within our control. |
| "**3 corridors live** by month 6", "**consolidated book** by month 12", "**global corridors** in year 2" | 15 | Targets, labelled as targets on the slide ("Targets, not projections"). Each is gated on their coverage map — which is ask #2 on slide 16. |
| **EU/UK, US, LatAm** are Phase 3, not Phase 1 | 6, 15 | Follows from "Asia first", but if Airwallex pushes a US-first motion the sequence should change. |
| Top **20%** of merchants migrate to connected accounts in year 2 | 10 | Illustrative segmentation to show we understand the cost trade-off. Not modelled. |
| `0.01%` will be believed without third-party verification | 4, 11, 18 | The processing history sits with the predecessor entity. Slide 18 discloses this and offers statements + references under NDA. **Do not skip that slide if the meeting runs long.** |
| Reserve terms, dispute fees and pricing are all open | 2, 11, 16, 18 | We are asking, not quoting. No Airwallex price appears anywhere in the deck — deliberately. |

## E. Extra assumptions that only appear in the white-label deck

| Assumption | Slide | Why it matters |
|---|---|---|
| **Three possible structures** — A: KD PAY is white-label + merchant of record; B: KD PAY is white-label but Airwallex holds MOR; C: connected accounts per merchant | 9 | These are *proposals*, not known Airwallex products. Ask which of the three they will actually approve; the whole deck is written so it still works if the answer is B. |
| **Take-rate scenarios of 1.0% / 1.5% / 2.0%** applied to $800K, $2M, $5M, $10M monthly volume | 7, 11 | Pure arithmetic we invented to show the shape of the business — the table says "Illustrative only". Airwallex pricing is unknown, so the split between our margin and their fee is not shown anywhere. |
| **$2M run-rate ambition by month 12** | 15 | Our ambition, labelled as ambition on the slide. Not a forecast and not backed by a signed merchant pipeline. |
| **Two additional merchant-ops staff by month six** | 15 | Our own resourcing plan, funded from the platform subscription line. Not a commitment to Airwallex. |
| **"White-label ready from day one"** — brand, domain, documents, support | 8, 14 | True of the product design; the *programme* is what we are asking them to approve. Do not imply the agreement exists today. |
| **Corridor split** (South Asia → South-East Asia → East Asia → EU/UK/US/LatAm) | 6 | Our sequencing, gated on their coverage map — ask #2 on slide 3. |
| **8-week timeline** (contract → build → certification → pilot → go-live) | 3, 16 | Our plan, contingent on their sandbox access, KYB turnaround and a named solutions engineer. |

## F. What changed from the first deck, and why

The first deck led with the **product** (checkout, architecture, 12 controls). This one leads with the
**business model**: the proposition, the ask, the revenue model, what white-label actually means, the three
contract structures, distribution, economics, risk, and then a single commercial security slide. The product
appears once, on slide 10, framed as the sales channel — which is what it is at this stage.

## Things the deck deliberately does **not** claim

- No **PCI DSS certification**, **SOC 2**, **ISO 27001**, **PCI Level 1** or **ASV scan completion**. Slide 13 says
  explicitly that we do not claim credentials we have not earned; slide 12 describes controls *we are building*.
- No **licence** of any kind (money transmitter, EMI, acquiring). Slide 13 states we are a platform sitting on
  top of a licensed acquirer.
- No **merchant-of-record** status. Slide 7 lists MOR under "deliberately not in Phase 1"; slide 10 answers the
  MOR question through the model comparison rather than by asserting a role.
- No **client names**, no **volume-by-country split**, no **launch dates presented as fact**, no **headcount**.
- No **live website URL** as a product link (the site is under development).

## Questions to put to Airwallex (they are on slide 16 / 18 too)

1. Which model do you want us on at launch — seller ledger or connected accounts — and what changes in underwriting?
2. Which of these corridors are live **today**, which are 6–12 months out, and what local methods exist in each?
3. What pricing applies at $800K/month, and what tiering exists at 5–10× that?
4. What is your standard rolling-reserve policy for a platform with a 0.01% dispute history?
5. Who carries dispute cost and chargeback fees at each stage?
6. What does KYB for KD PAY LLC require, given the entity is one month old and the trading history is with the
   predecessor entity?

---

*Deck built 30 October 2026. Speaker notes for every slide are embedded in the file and mirrored in
`SPEAKER-NOTES.md`. Contact details on slide 16 are placeholders (`[name] · [title] · [email] · [phone]`) —
fill them in before sending the file anywhere.*
