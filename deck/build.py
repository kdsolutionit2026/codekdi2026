# -*- coding: utf-8 -*-
"""Builds KD-PAY-Airwallex-Partnership.pptx — 18 slides, 16:9."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

prs = new_deck()

# =====================================================================
# 01 · TITLE
# =====================================================================
s = slide(prs, INK)
# left accent rule
rect(s, ML, 1.05, 0.06, 3.15, fill=ACCENT)
text(s, ML + 0.28, 1.02, 9.5, 0.26, "Partnership proposal  ·  Confidential", size=10,
     color=ACCENT, bold=True, caps=True, tracking=1.8)
text(s, ML + 0.28, 1.42, 10.9, 2.5,
     "Payments infrastructure for\nAsia's cross-border merchants", size=40, color=WHITE,
     bold=True, spacing=1.08)
text(s, ML + 0.28, 3.92, 9.8, 0.9,
     "KD PAY LLC — application to join Airwallex for Platforms as a regional payment platform.",
     size=15, color=DARK_MUT, spacing=1.3)

# meta strip
hy = 5.32
hline(s, ML, hy, CW, color=DARK_LN, weight=0.8)
for i, (v, l) in enumerate([("$800K", "monthly volume"), ("0.01%", "chargeback ratio"),
                            ("2022", "operating since"), ("Asia → global", "corridor roadmap")]):
    x = ML + i * (CW / 4)
    stat(s, x, hy + 0.26, CW / 4 - 0.25, v, l, dark=True,
         color=ACCENT if i < 2 else WHITE, vsize=22)
text(s, W - MR - 3.2, 1.02, 3.2, 0.26, "30 October 2026", size=10, color=DARK_MUT,
     align=PP_ALIGN.RIGHT, caps=True, tracking=1.4)
notes(s, "Opening (45 seconds). We are KD PAY LLC. We process about $800K a month at a 0.01% "
         "chargeback rate, and we want to build our platform on Airwallex. In this deck: who we are, "
         "the Asia gap we serve, our Phase 1 product, the exact partnership model we propose, "
         "and our security posture.")

# =====================================================================
# 02 · THE ASK
# =====================================================================
s = slide(prs)
y = header(s, "Executive summary", "What we are asking for",
           lead="Three things, and a commitment in return. Everything else in this deck supports this page.")
cards = [
 ("01", "Platform account, seller-ledger model",
  "KD PAY as your master platform account with seller ledgers per merchant. No per-merchant "
  "underwriting at launch — we onboard and monitor merchants ourselves, as your model allows."),
 ("02", "Asia-first corridor coverage",
  "Card acquiring plus local methods across South, South-East and East Asia as your licensing "
  "permits, then EU/UK, US and LatAm. We enable a corridor only when you confirm coverage."),
 ("03", "Commercials, pricing, a partner manager",
  "Transparent pricing at our current $800K/month and at growth volume, reserve terms that reflect "
  "a 0.01% chargeback record, and a technical contact who can unblock integration."),
]
cw = (CW - 0.5) / 3
for i, (n, t, b) in enumerate(cards):
    card(s, ML + i * (cw + 0.25), y + 0.15, cw, 2.5, n, t, b, body_size=11)

# commitment bar
by = y + 2.78
rect(s, ML, by, CW, 0.95, fill=ACCENT_S, radius=0.05)
text(s, ML + 0.3, by + 0.16, 3.0, 0.24, "Our commitment", size=9.5, color=ACCENT_D, bold=True,
     caps=True, tracking=1.4)
text(s, ML + 0.3, by + 0.40, CW - 0.6, 0.55,
     "Sandbox integration running within 14 days of approval. First live transaction inside eight weeks, "
     "with one named engineer on our side for the whole build.", size=12.5, color=TEXT, spacing=1.2)

wy = by + 1.1
text(s, ML, wy, CW, 0.24, "Why this is worth your time now", size=9, color=MUTED, bold=True,
     caps=True, tracking=1.3)
why = [("A corridor, not a campaign. ", "Verified Asian merchants into your rails, underwritten by us."),
       ("Small and clean. ", "$800K a month at 0.01% chargebacks — enough to prove the model."),
       ("Built to your contracts. ", "Real integration, reconciliation and evidence at every step.")]
for i, (h, b) in enumerate(why):
    x = ML + i * (CW / 3)
    rich(s, x, wy + 0.30, CW / 3 - 0.45, 0.45, [(h, True, TEXT), (b, False, MUTED)],
         size=9.3, spacing=1.25)
footer(s, 2)
notes(s, "This is the only slide that matters if the meeting is cut short. We want the ledger model at "
         "launch because it gets us live in weeks; connected accounts come later as volume justifies KYB cost. "
         "We are not asking for special treatment on risk — we are showing a 0.01% dispute record and asking "
         "for pricing that reflects it.")

# =====================================================================
# 03 · WHO WE ARE
# =====================================================================
s = slide(prs)
y = header(s, "Company", "Who we are")
left_w = 6.55
intro = ("KD PAY LLC is a US-registered payment platform for Asian merchants that sell to buyers "
         "anywhere. We provide the acceptance layer between a merchant and their buyer: onboarding, "
         "hosted checkout, invoicing, payouts, disputes and reconciliation.")
ih = text_h(intro, left_w, 13.5, spacing=1.35)
text(s, ML, y + 0.05, left_w, ih + 0.1, intro, size=13.5, color=TEXT, spacing=1.35)
paras = [
 ("Operating history. ", "Since 2022 through KD Solution IT (kdsolutionit.com). KD PAY LLC is the new "
  "contracting and processing entity, registered October 2026."),
 ("Today. ", "We process through private merchant accounts at incumbent providers — B2B and B2C, "
  "card-not-present, USD-first."),
 ("Why change now. ", "Private accounts cannot deliver Asian coverage, local payment methods or the "
  "economics that let us scale. We are consolidating onto one platform relationship."),
 ("How we work. ", "A small engineering team that ships. We build on a written specification: "
  "double-entry ledger, row-level tenant isolation, hash-chained audit trail — not a white-label reseller."),
]
para_list(s, ML, y + 0.05 + ih + 0.30, left_w, 2.9, paras, size=11.5, gap=9)

# right rail: facts
rx = ML + left_w + 0.55
rw = W - MR - rx
rect(s, rx, y, rw, 4.55, fill=SURFACE, radius=0.04)
text(s, rx + 0.3, y + 0.25, rw - 0.6, 0.24, "At a glance", size=9.5, color=MUTED, bold=True,
     caps=True, tracking=1.4)
facts = [("Legal entity", "KD PAY LLC (US)"),
         ("Operating since", "2022"),
         ("Website", "kdsolutionit.com"),
         ("Monthly volume", "≈ $800,000"),
         ("Chargeback ratio", "0.01%"),
         ("Mix", "B2B and B2C, card-not-present"),
         ("Regions served", "Asia, EU/UK, US, LatAm")]
fy = y + 0.62
for k, v in facts:
    text(s, rx + 0.3, fy, rw - 0.6, 0.2, k.upper(), size=8.5, color=MUTED, bold=True, tracking=0.9)
    text(s, rx + 0.3, fy + 0.2, rw - 0.6, 0.3, v, size=11.5, color=TEXT, bold=False)
    fy += 0.55
footer(s, 3)
notes(s, "Be upfront about the entity change before they ask: the team and book of business are from 2022, "
         "the LLC is new. We will provide statements from the current providers and references under NDA. "
         "The engineering claim is the differentiator — we are building a real ledger, not reselling a gateway.")

# =====================================================================
# 04 · BUSINESS TODAY
# =====================================================================
s = slide(prs)
y = header(s, "Business today", "A small book with clean risk",
           lead="Quality over count: verified business buyers, invoice-led volume, and a dispute rate two "
                "orders of magnitude below network thresholds.")
stats = [("$800K", "monthly volume", "≈ $9.6M annualised"),
         ("0.01%", "chargeback ratio", "network watchlist starts at 0.9%"),
         ("B2B + B2C", "merchant mix", "card-not-present, invoiced"),
         ("Oct 2026", "new entity", "operating team since 2022")]
for i, (v, l, sub) in enumerate(stats):
    x = ML + i * (CW / 4)
    stat(s, x, y + 0.05, CW / 4 - 0.3, v, l, sub=sub, vsize=26,
         color=ACCENT_D if i == 1 else TEXT)
    if i:
        vline(s, x - 0.18, y + 0.08, 1.25, color=LINE)

ty = y + 1.62
cols = [("Today", 0.22), ("Current setup", 0.26), ("Why we are switching", 0.26), ("With Airwallex", 0.26)]
rows = [
 ("Processing", "Private merchant accounts, several providers", "No single view of risk, revenue or reserves",
  "One platform, one ledger, one reconciliation"),
 ("Coverage", "US and EU acquiring only", "Asian buyers decline or pay in the wrong currency",
  "Asia-first acquiring plus local methods"),
 ("Merchants", "Onboarded case by case", "Each provider runs its own KYB, months of underwriting",
  "Our KYB pipeline runs once, in days"),
 ("Economics", "Opaque per-account pricing", "No volume leverage, no corridor pricing",
  "Transparent platform pricing that scales"),
]
table(s, ML, ty, CW, cols, rows, row_h=0.62, body_size=10.5)
footer(s, 4)
notes(s, "The point of this slide is risk quality, not size. $800K/month is small for Airwallex; 0.01% is "
         "unusually clean. Say it plainly: we would rather bring you 50 good merchants than 500 bad ones. "
         "We will supply 12 months of statements and dispute data under NDA.")

# =====================================================================
# 05 · THE GAP (why Asia)
# =====================================================================
s = slide(prs)
y = header(s, "The problem", "Asian merchants can sell globally. They cannot get paid globally.",
           title_size=27,
           lead="The constraint is not demand. It is acceptance infrastructure — and it is why merchants leave "
                "their current providers.")
blocks = [
 ("No local entity", "A merchant in Dhaka cannot open a local acquiring relationship. Offshore accounts "
  "mean materially higher declines."),
 ("Currency and settlement", "Paid in USD, converted twice, settled in 5–10 days. The FX margin is invisible "
  "until someone reconciles."),
 ("Local methods missing", "Bank transfer, wallets and local schemes are how Asia pays. No single gateway "
  "covers three markets well."),
 ("Onboarding friction", "Every provider repeats KYB, demands reserves, takes weeks. Merchants give up or "
  "route volume elsewhere."),
]
cost = ["Declines on the cross-border attempt",
        "Double conversion, invisible margin",
        "Abandonment at the payment step",
        "Weeks of underwriting, repeated"]
cw = (CW - 0.75) / 4
for i, (t, b) in enumerate(blocks):
    x = ML + i * (cw + 0.25)
    rect(s, x, y + 0.12, cw, 2.62, fill=SURFACE, radius=0.05)
    rect(s, x, y + 0.12, cw, 0.05, fill=ACCENT)
    text(s, x + 0.22, y + 0.32, cw - 0.44, 0.5, t, size=12.5, bold=True, color=TEXT, spacing=1.05)
    text(s, x + 0.22, y + 0.82, cw - 0.44, 1.1, b, size=10, color=MUTED, spacing=1.28)
    hline(s, x + 0.22, y + 2.0, cw - 0.44, color=LINE, weight=0.7)
    text(s, x + 0.22, y + 2.12, cw - 0.44, 0.42, cost[i], size=8.8, bold=True, color=ACCENT_D,
         spacing=1.15)

cy = y + 2.9
rect(s, ML, cy, CW, 0.85, fill=INK, radius=0.05)
text(s, ML + 0.35, cy + 0.17, CW - 0.7, 0.58,
     "Merchants do not need another dashboard. They need one relationship that accepts money where their "
     "buyers are, and pays them where they bank.", size=13, color=WHITE, spacing=1.2)
footer(s, 5)
notes(s, "This is the slide that explains the business. Every point is something we hear from merchants weekly. "
         "Avoid quoting decline percentages unless we have our own data in the appendix — 'materially higher' is "
         "defensible, a made-up number is not.")

# =====================================================================
# 06 · MARKET & SEQUENCE
# =====================================================================
s = slide(prs)
y = header(s, "Go-to-market", "Asia first, then the world",
           lead="Sequence matters: density in a few corridors beats thin coverage everywhere. Each corridor goes "
                "live only when Airwallex confirms coverage.")
grp = [("South Asia", "Bangladesh · India · Pakistan · Sri Lanka",
        "Cards, local bank transfer, wallets — the largest underserved merchant base"),
       ("South-East Asia", "Singapore · Malaysia · Indonesia · Philippines",
        "Cards plus FPX, DuitNow, QRIS, GCash, GrabPay-class wallets"),
       ("East Asia", "Hong Kong · Japan",
        "Cards and wallets; strongest buyer-side card acceptance"),
       ("Phase 3", "EU / UK · US / Canada · Brazil / Mexico",
        "SCA-ready 3DS2 for EEA; local rails where available")]
ty = y + 0.02
for i, (region, countries, note) in enumerate(grp):
    dark = i == 3
    hgt = 1.03
    rect(s, ML, ty, 5.1, hgt, fill=INK if dark else SURFACE, radius=0.05)
    text(s, ML + 0.25, ty + 0.11, 4.6, 0.22, region.upper(), size=9.2, bold=True,
         color=ACCENT if dark else ACCENT_D, caps=True, tracking=1.2)
    text(s, ML + 0.25, ty + 0.35, 4.6, 0.26, countries, size=10.3, bold=True,
         color=WHITE if dark else TEXT)
    text(s, ML + 0.25, ty + 0.65, 4.6, 0.28, note, size=8.8, color=DARK_MUT if dark else MUTED)
    ty += hgt + 0.1

rx = ML + 5.55
rw = W - MR - rx
text(s, rx, y + 0.12, rw, 0.3, "Why this order", size=9.5, color=MUTED, bold=True, caps=True, tracking=1.4)
para_list(s, rx, y + 0.5, rw, 2.6, [
 ("Wedge: ", "Asian merchants invoicing Western buyers in USD. The buyer's card is the rail; the "
  "merchant's bank account is the problem we solve."),
 ("Density: ", "A corridor is only worth opening when we can support the methods buyers actually use, "
  "not just cards."),
 ("Dependency: ", "Each corridor depends on your licensing and local acquiring. We plan around your "
  "coverage map, not our wish list."),
 ("Expansion: ", "EU/UK and US come once SCA and 3DS2 flows are certified — not before."),
], size=11, gap=10)
footer(s, 6)
notes(s, "Ask them directly: which of these corridors can you support today, and which are 6-12 months away? "
         "That answer re-orders our roadmap. We are deliberately not promising all of Asia on day one.")

# =====================================================================
# 07 · PHASE 1 PRODUCT
# =====================================================================
s = slide(prs)
y = header(s, "Product — Phase 1", "One integration, three ways for a merchant to plug in",
           title_size=27,
           lead="The smallest product that is genuinely useful: a merchant can take a card payment this week.")
prods = [
 ("01", "Hosted checkout", "A payment link or invoice page. No code, no plugin, works on any site, "
  "mobile-first, English and Bangla, no third-party trackers."),
 ("02", "Shopify & WooCommerce plugins", "Install, paste the API key, take payments. Webhooks keep orders "
  "and refunds in sync. This is how most Asian SMBs will onboard."),
 ("03", "REST API + webhooks", "Versioned endpoints, scoped keys, idempotency on every mutation, signed "
  "webhooks with retries. For custom storefronts and platforms."),
]
cw = (CW - 0.5) / 3
for i, (n, t, b) in enumerate(prods):
    card(s, ML + i * (cw + 0.25), y + 0.1, cw, 1.92, n, t, b, body_size=10.5)

# capability strip
cy = y + 2.28
rect(s, ML, cy, CW, 1.32, fill=SURFACE, radius=0.04)
text(s, ML + 0.3, cy + 0.18, CW - 0.6, 0.24, "Behind every channel — the same platform", size=9.5,
     color=MUTED, bold=True, caps=True, tracking=1.3)
caps = ["Merchant dashboard", "Invoicing & receipts", "Payouts", "Disputes",
        "Reconciliation", "API keys & logs", "Team roles", "Audit trail"]
for i, c in enumerate(caps):
    col, row = i % 4, i // 4
    x = ML + 0.3 + col * ((CW - 0.6) / 4)
    yy = cy + 0.48 + row * 0.4
    rect(s, x, yy + 0.08, 0.07, 0.07, fill=ACCENT)
    text(s, x + 0.18, yy, (CW - 0.6) / 4 - 0.3, 0.24, c, size=10.5, color=TEXT)

# deliberate exclusions
ey = cy + 1.62
text(s, ML, ey, CW, 0.24, "Deliberately not in Phase 1", size=9, color=MUTED, bold=True, caps=True,
     tracking=1.3)
for i, (t, b) in enumerate([
        ("Multi-currency wallets", "Phase 2 — priced once we know your FX spread."),
        ("Merchant of record", "Only on a signed programme, never implied."),
        ("Full white-label", "Phase 2 — brand, domain and email, end to end.")]):
    x = ML + i * (CW / 3)
    text(s, x, ey + 0.32, CW / 3 - 0.4, 0.28, t, size=10.5, bold=True, color=TEXT)
    text(s, x, ey + 0.62, CW / 3 - 0.4, 0.4, b, size=9.3, color=MUTED, spacing=1.15)
footer(s, 7)
notes(s, "Phase 1 is deliberately boring: hosted checkout, two plugins, an API. That is what gets merchants live. "
         "Everything else — invoicing, payouts, disputes — is already scoped and comes with the same release train.")

# =====================================================================
# 08 · PAYMENT FLOW
# =====================================================================
s = slide(prs)
y = header(s, "Architecture", "Where the card data goes — and where it never goes",
           title_size=27,
           lead="KD PAY is a SAQ-A scope: the card fields are yours, hosted in your components. We never see, "
                "log or store a card number.")
bw, gap = 2.42, 0.55
def flow(yy, boxes, dark_from, arrow_col):
    for i, (t, sub) in enumerate(boxes):
        x = ML + i * (bw + gap)
        dark = i >= dark_from
        rect(s, x, yy, bw, 1.28, fill=INK if dark else SURFACE, radius=0.06,
             line=None if dark else LINE)
        text(s, x + 0.12, yy + 0.22, bw - 0.24, 0.52, t, size=11.5, bold=True,
             color=WHITE if dark else TEXT, align=PP_ALIGN.CENTER, spacing=1.02)
        text(s, x + 0.12, yy + 0.92, bw - 0.24, 0.24, sub, size=8.5,
             color=DARK_MUT if dark else MUTED, align=PP_ALIGN.CENTER)
        if i < 3:
            arrow(s, x + bw + 0.1, yy + 0.64, gap - 0.2, color=arrow_col)

fy = y + 0.1
flow(fy, [("Buyer", "browser"), ("KD PAY\ncheckout", "hosted page"),
          ("Airwallex\nElements", "card fields"), ("Airwallex\nacquiring", "authorisation")], 2, ACCENT)
text(s, ML, fy + 1.42, 5.4, 0.24, "CARD DATA BOUNDARY", size=9, color=ACCENT_D, bold=True, tracking=1.2)
text(s, ML, fy + 1.68, 5.2, 0.55, "PAN, expiry and CVV exist only inside Airwallex's iframe. No line "
     "on this diagram above touches them.", size=9.5, color=MUTED, spacing=1.2)

sy = fy + 2.28
flow(sy, [("Airwallex\nseller ledger", "balance held by partner"), ("KD PAY ledger", "double-entry mirror"),
          ("Payout", "to merchant bank"), ("Receipt & webhook", "signed, idempotent")], 9, BLUE)
text(s, ML, sy + 1.42, 5.4, 0.24, "MONEY FLOW", size=9, color=BLUE, bold=True, tracking=1.2)
text(s, ML, sy + 1.68, 6.4, 0.55, "Merchant balances live in your ledger. Our ledger mirrors it entry by "
     "entry, so reconciliation is a query — not a spreadsheet.", size=9.5, color=MUTED, spacing=1.2)
footer(s, 8)
notes(s, "This slide answers the PCI question before they ask it. Card data lives and dies inside Airwallex "
         "Elements. Our servers see a token and a result. That is why we can launch as SAQ-A rather than "
         "spending a year and six figures on a full assessment.")

# =====================================================================
# 09 · WHY AIRWALLEX
# =====================================================================
s = slide(prs)
y = header(s, "Fit", "Why Airwallex, specifically",
           lead="We evaluated Stripe Connect, Adyen for Platforms and Airwallex. This is why you won.")
why = [
 ("01", "Licensed acquiring where our merchants are",
  "APAC coverage and local rails are the exact gap we cannot close as a platform. On the public "
  "coverage maps, your footprint is deeper in the corridors we care about first."),
 ("02", "Two models, one relationship",
  "Seller ledger at launch, full connected accounts when volume justifies per-merchant KYB. "
  "We can grow into your product instead of migrating off a competitor."),
 ("03", "Multi-currency by design",
  "Wallets, FX and payouts to 150+ countries, so a merchant in Dhaka can be paid in USD and settled "
  "in the currency their bank actually holds."),
 ("04", "An API we can build a ledger against",
  "Webhooks for capability and payment state changes, idempotent operations, a real sandbox, and "
  "reports we can reconcile against."),
]
cw = (CW - 0.25) / 2
for i, (n, t, b) in enumerate(why):
    x = ML + (i % 2) * (cw + 0.25)
    yy = y + 0.12 + (i // 2) * 2.02
    card(s, x, yy, cw, 1.72, n, t, b, body_size=10.5)

fy2 = y + 3.98
hline(s, ML, fy2 - 0.2, CW, color=LINE, weight=0.8)
text(s, ML, fy2, CW, 0.24, "What has to be true for this to work", size=9, color=MUTED, bold=True,
     caps=True, tracking=1.3)
conds = [("Corridor by corridor.",
          "You confirm which markets are live today. We do not assume coverage and then apologise for it."),
         ("Underwriting comfort.",
          "Your risk team is satisfied with how we hold and report merchant exposure."),
         ("Economics that hold at volume.",
          "Pricing that works at $800K a month and still works at ten times that.")]
for i, (h, b) in enumerate(conds):
    x = ML + i * (CW / 3)
    rich(s, x, fy2 + 0.32, CW / 3 - 0.45, 0.6,
         [(h + " ", True, TEXT), (b, False, MUTED)], size=9.3, spacing=1.25)
footer(s, 9)
notes(s, "Careful with the Stripe comparison — say it as a coverage observation, not a criticism. If they ask "
         "what would make us leave: coverage gaps in South Asia and pricing that does not reflect our dispute record.")

# =====================================================================
# 10 · PARTNERSHIP MODEL (dark)
# =====================================================================
s = slide(prs, INK)
y = header(s, "Partnership model", "Who does what — and who is merchant of record",
           dark=True, title_size=27,
           lead="Two of your models fit us at different stages. We propose starting with the lighter one.")
lx, rx2 = ML, ML + CW / 2 + 0.15
colw = CW / 2 - 0.3
for x, title, sub, accent in [(lx, "Launch — seller ledger", "KD PAY is the platform; merchants are not your customers", ACCENT),
                              (rx2, "Scale — connected accounts", "Each merchant onboarded and KYB'd by Airwallex", BLUE)]:
    text(s, x, y + 0.06, colw, 0.26, title.upper(), size=10, color=accent, bold=True, tracking=1.3)
    text(s, x, y + 0.32, colw, 0.45, sub, size=9.5, color=DARK_MUT, spacing=1.2)

rows = [("Merchant of record", "KD PAY, under the Airwallex master account", "The merchant, as a full connected account"),
        ("KYC / KYB", "Airwallex onboards KD PAY. We onboard merchants.", "Airwallex per merchant, via API"),
        ("Funds held", "Inside Airwallex — never in our bank account", "Inside each merchant's wallet"),
        ("Disputes & reserves", "KD PAY handles evidence and reserves", "Merchant-level liability"),
        ("Merchant experience", "Our brand, our support, our dashboard", "Airwallex onboarding inside our UI"),
        ("Time to first payment", "Weeks", "Per-merchant, days to weeks")]
ry = y + 0.95
for i, (label, a, b) in enumerate(rows):
    if i % 2 == 0:
        rect(s, ML - 0.12, ry - 0.10, CW + 0.24, 0.54, fill=INK_2, radius=0.04)
    text(s, ML, ry, 2.35, 0.3, label.upper(), size=8, color=DARK_MUT, bold=True, tracking=0.8)
    text(s, ML + 2.45, ry - 0.03, 4.55, 0.4, a, size=10.5, color=WHITE, spacing=1.1)
    text(s, rx2 + 0.05, ry - 0.03, colw - 0.05, 0.4, b, size=10.5, color=DARK_MUT, spacing=1.1)
    ry += 0.535

text(s, ML, ry + 0.22, CW, 0.3,
     "Recommendation: launch on the ledger model, migrate the top 20% of merchants to connected accounts in year two.",
     size=11.5, color=ACCENT, bold=True)
footer(s, 10, dark=True)
notes(s, "This is the slide that shows we read their documentation. Terminology matters: seller ledger vs full "
         "connected account, capability activation, payment acceptance requiring KYB. Ask them to confirm which "
         "model they would approve for a US platform onboarding merchants in Bangladesh and Pakistan. "
         "Also ask about white-label/brand-mention guidelines for the merchant UI.")

# =====================================================================
# 11 · RISK PROFILE
# =====================================================================
s = slide(prs)
y = header(s, "Risk", "Our dispute record, against the threshold that matters",
           lead="Card networks start monitoring a merchant above 0.9% chargebacks. We operate at 0.01%.")
bx, bw = ML, 6.55
# KD PAY bar
text(s, bx, y + 0.05, 5.0, 0.24, "KD PAY — 0.01%", size=10.5, bold=True, color=ACCENT_D)
rect(s, bx, y + 0.33, bw, 0.30, fill=SURFACE, radius=0.02)
rect(s, bx, y + 0.33, 0.07, 0.30, fill=ACCENT, radius=0.02)
text(s, bx + 0.16, y + 0.37, 6.0, 0.24, "1 dispute per 10,000 transactions", size=9.5, color=MUTED)
# threshold bar
text(s, bx, y + 0.85, 3.6, 0.24, "Network monitoring threshold — 0.9%", size=10.5, bold=True,
     color=TEXT)
text(s, bx + bw - 1.45, y + 0.86, 1.45, 0.24, "90× headroom", size=9.5, bold=True, color=ACCENT_D,
     align=PP_ALIGN.RIGHT)
rect(s, bx, y + 1.13, bw, 0.30, fill=RGBColor(0xC9, 0xD3, 0xDE), radius=0.02)

vy = y + 1.72
text(s, bx, vy, 6.3, 0.24, "HOW WE KEEP IT THERE", size=9, color=MUTED, bold=True, tracking=1.3)
para_list(s, bx, vy + 0.32, 6.9, 1.9, [
 ("Verified buyers. ", "Invoices to known business counterparties; consumer volume screened."),
 ("3DS2 by rule. ", "Forced on VPN/Tor or IP-country mismatch; AVS postal match for US/CA/UK."),
 ("Hard blocks. ", "Prohibited MCCs, card-fingerprint blocklists, velocity limits."),
 ("Evidence ready. ", "Reason-code checklists, 72/48/24-hour deadline alerts."),
], size=10, gap=7)

# right: reserve panel
rx3 = ML + 7.55
rw3 = W - MR - rx3
rect(s, rx3, y + 0.05, rw3, 2.5, fill=SURFACE, radius=0.05)
text(s, rx3 + 0.28, y + 0.28, rw3 - 0.5, 0.24, "ON RESERVES", size=9.5, color=ACCENT_D, bold=True,
     tracking=1.3)
para_list(s, rx3 + 0.28, y + 0.66, rw3 - 0.55, 1.75, [
 "We fund risk before we argue about it: merchant-level reserves held by us, plus a platform reserve "
 "where your policy requires one.",
 "Rolling reserve percentage, cap and release schedule are all negotiable.",
 "Dispute evidence and merchant follow-up stay with us — you keep the rail.",
], size=9.8, gap=8, bullet_color=ACCENT)

ay = y + 3.5
hline(s, ML, ay - 0.22, CW, color=LINE, weight=0.8)
text(s, ML, ay, CW, 0.24, "What we ask of you", size=9, color=MUTED, bold=True, caps=True,
     tracking=1.3)
for i, item in enumerate(["A reserve policy proportionate to a 0.01% profile",
                          "Dispute fees disclosed before we sign",
                          "A named escalation contact for high-value cases"]):
    text(s, ML + i * (CW / 3), ay + 0.32, CW / 3 - 0.4, 0.5, item, size=10, color=TEXT,
         spacing=1.2)
footer(s, 11)
notes(s, "Do not overclaim: 0.01% is the trailing average across the current book. Say that, and offer the "
         "statements. The reserve sentence is the one they want to hear — platforms that fight reserves get "
         "declined. We are signalling we will fund risk.")

# =====================================================================
# 12 · SECURITY (the big one)
# =====================================================================
s = slide(prs)
y = header(s, "Security", "Twelve controls we will not compromise on", title_size=28,
           lead="Payments security is an architecture decision, not a feature list. Each control below has a "
                "test that fails if it is removed.")
sec = [
 ("01", "PCI DSS SAQ-A scope", "Card data only in Airwallex-hosted fields. No PAN, CVV or track data in our code, logs or database — a CI rule blocks regressions."),
 ("02", "3-D Secure 2 and SCA", "Risk-based challenge; forced on VPN/Tor or IP-country mismatch; AVS postal match for US/CA/UK. SCA-ready for UK and EEA."),
 ("03", "Tokenisation only", "We store processor tokens and salted card fingerprints. A breach of our database yields no usable card data."),
 ("04", "Server-side sessions", "Opaque HttpOnly tokens, device binding, rotation on privilege change, instant revocation. No JWT in the browser."),
 ("05", "Step-up authentication", "TOTP or passkey re-auth for payouts, bank changes, API keys and refunds above threshold."),
 ("06", "AES-256-GCM encryption", "Envelope encryption with versioned keys for bank details, tax IDs and KYC documents. Secrets never reach the client."),
 ("07", "Default-deny row-level security", "Every table is tenant-scoped in Postgres itself. A cross-tenant read returns 404, not an error — proven by CI isolation tests."),
 ("08", "Double-payment prevention", "Row lock, unique index and state machine at the database level, plus idempotency keys on every money mutation."),
 ("09", "Tamper-evident audit log", "Hash-chained, append-only, UPDATE/DELETE revoked, daily signed checkpoints, 7-year WORM export."),
 ("10", "Webhook integrity", "Outbound HMAC signatures with replay protection; inbound verified, deduplicated and re-fetched from the source."),
 ("11", "Edge and transport", "Cloudflare WAF and DDoS, TLS 1.3, HSTS preload, DNSSEC, nonce-based CSP, no third-party trackers on checkout."),
 ("12", "Fraud controls", "Velocity per IP, device, email and card; blocklists; decline classification; retry caps; manual review with 5-day auth hold."),
]
cw = (CW - 0.5) / 3
for i, (n, t, b) in enumerate(sec):
    x = ML + (i % 3) * (cw + 0.25)
    yy = y + 0.06 + (i // 3) * 1.16
    rect(s, x, yy, cw, 1.04, fill=SURFACE, radius=0.05)
    text(s, x + 0.2, yy + 0.12, 0.35, 0.2, n, size=8.5, color=ACCENT_D, bold=True, tracking=1.0)
    text(s, x + 0.62, yy + 0.1, cw - 0.78, 0.24, t, size=10, bold=True, color=TEXT)
    text(s, x + 0.2, yy + 0.38, cw - 0.4, 0.6, b, size=8.2, color=MUTED, spacing=1.14)
footer(s, 12)
notes(s, "Do not read all twelve. Say: 'there are twelve controls, all tested; let me highlight four'. "
         "Highlight 01 (SAQ-A: we cannot see a card number), 07 (RLS: a bug in our app still cannot leak a "
         "tenant's data), 08 (double-payment), 09 (audit chain). Offer the security architecture document as a "
         "follow-up — it is already written.")

# =====================================================================
# 13 · COMPLIANCE & OPS
# =====================================================================
s = slide(prs)
y = header(s, "Compliance", "We take on the merchant risk so you focus on the rail",
           title_size=27, lead="Onboarding, monitoring and disputes are our job. That is the value of a "
                           "platform partner — and the reason our chargeback number is what it is.")
# three columns
cols3 = [("At onboarding", [
    "Business verification and UBO ownership to 25%",
    "Sanctions, PEP and adverse-media screening",
    "Website, MCC and prohibited-business review",
    "Bank account verification with micro-deposit and cooling period",
    "Risk tier that sets the review cycle"]),
 ("Ongoing", [
    "Velocity and transaction monitoring per merchant",
    "Volume, refund and dispute-ratio thresholds",
    "Periodic review: annual, 6-monthly or quarterly by tier",
    "Sanctions re-screening on a schedule",
    "Separate switches for charges and payouts"]),
 ("Evidence", [
    "Hash-chained audit log of every decision",
    "7-year retention with WORM export",
    "PITR backups and a quarterly restore drill",
    "Incident response runbook and breach clock",
    "Merchant activity feed and DSAR workflow"])]
cw = (CW - 0.5) / 3
maxh = 0
for i, (t, items) in enumerate(cols3):
    x = ML + i * (cw + 0.25)
    dark = i == 2
    hgt = 0.78 + sum(text_h(it, cw - 0.56, 9.8) + 0.09 for it in items)
    maxh = max(maxh, hgt)
    rect(s, x, y + 0.05, cw, hgt, fill=INK if dark else SURFACE, radius=0.05)
    text(s, x + 0.26, y + 0.26, cw - 0.5, 0.26, t.upper(), size=9.5,
         color=ACCENT if dark else ACCENT_D, bold=True, tracking=1.3)
    para_list(s, x + 0.26, y + 0.66, cw - 0.5, hgt - 0.75, items, size=9.8,
              color=WHITE if dark else TEXT, bullet_color=ACCENT, gap=7, spacing=1.16)
py = y + 0.05 + maxh + 0.4
text(s, ML, py, CW, 0.24, "In plain terms", size=9, color=MUTED, bold=True, caps=True, tracking=1.3)
plains = [("Scope, not theatre.",
           "PCI DSS SAQ-A: card data never reaches our servers, so our audit surface stays small."),
          ("No borrowed credentials.",
           "We do not claim SOC 2, ISO 27001 or PCI Level 1 that we have not earned. We publish the plan and the dates."),
          ("A platform, not an acquirer.",
           "We are not a licensed acquirer. Our model is deliberately built to sit on top of yours.")]
for i, (h, b) in enumerate(plains):
    x = ML + i * (CW / 3)
    text(s, x, py + 0.3, CW / 3 - 0.4, 0.55, h, size=10.5, bold=True, color=TEXT, spacing=1.1)
    text(s, x, py + 0.62, CW / 3 - 0.4, 0.75, b, size=9.3, color=MUTED, spacing=1.2)
footer(s, 13)
notes(s, "If they push back on the ledger model because 'we don't KYC the merchants', this is the answer: we run "
         "a real KYB pipeline, screen sanctions, monitor disputes and hold reserves. We are not a shell that "
         "pipes volume. Offer to walk them through the onboarding flow screen by screen.")

# =====================================================================
# 14 · INTEGRATION PLAN
# =====================================================================
s = slide(prs)
y = header(s, "Execution", "Eight weeks from approval to first live payment",
           lead="We are ready to start. The sandbox integration is scoped and the team is standing by.")
# timeline
tl_y = y + 0.45
phases = [("W1–2", "Contract & sandbox", "Model agreed in writing, API keys, entity and KYC pack submitted"),
          ("W3–4", "Build", "Checkout, webhooks, ledger mapping, payout flow, reconciliation skeleton"),
          ("W5", "Certification", "Joint test pass: 3DS2, declines, refunds, webhook replay, dispute intake"),
          ("W6", "Pilot", "10 merchants live on small limits, daily reconciliation with your team"),
          ("W7–8", "Go-live", "Limits raised, monitoring and on-call handover, first payout cycle")]
seg = CW / len(phases)
rect(s, ML, tl_y, CW, 0.03, fill=LINE)
for i, (w, t, b) in enumerate(phases):
    x = ML + i * seg
    done = i < 2
    gate = i >= 2
    shape = MSO_SHAPE.DIAMOND if gate else MSO_SHAPE.RECTANGLE
    sz = 0.2 if not gate else 0.24
    rect(s, x + 0.02, tl_y - sz / 2 + 0.015, sz, sz, fill=ACCENT if done else WHITE,
         line=ACCENT, radius=0.15, shape=shape)
    text(s, x + 0.34, tl_y - 0.13, seg - 0.4, 0.24, w, size=10.5, bold=True, color=ACCENT_D, tracking=1.0)
    text(s, x, tl_y + 0.30, seg - 0.22, 0.3, t, size=11.5, bold=True, color=TEXT, spacing=1.05)
    text(s, x, tl_y + 0.62, seg - 0.25, 0.9, b, size=9, color=MUTED, spacing=1.2)

# readiness strip
ry = tl_y + 1.95
rect(s, ML, ry, CW, 1.35, fill=SURFACE, radius=0.04)
text(s, ML + 0.3, ry + 0.16, 4.0, 0.24, "Technical readiness", size=9.5, color=MUTED, bold=True,
     caps=True, tracking=1.3)
ready = ["TypeScript / Next.js on Vercel", "Postgres with row-level security",
         "Signed webhook consumer", "Double-entry ledger and reconciliation",
         "Sandbox and live key separation", "Runbooks and on-call"]
for i, r in enumerate(ready):
    col, row = i % 3, i // 3
    x = ML + 0.3 + col * ((CW - 0.6) / 3)
    yy = ry + 0.48 + row * 0.4
    rect(s, x, yy + 0.08, 0.07, 0.07, fill=ACCENT)
    text(s, x + 0.18, yy, (CW - 0.6) / 3 - 0.3, 0.24, r, size=10, color=TEXT)
footer(s, 14)
notes(s, "The timeline is the credibility test. Most platforms say 'we'll integrate' without a plan. Ours has "
         "five gates and a joint certification week. If they ask what we need from them: sandbox keys by week 2 "
         "and one solutions engineer for the certification week.")

# =====================================================================
# 15 · WHAT SUCCESS LOOKS LIKE
# =====================================================================
s = slide(prs)
y = header(s, "Outlook", "What this looks like in twelve months",
           lead="Targets, not projections — we model them again once your pricing and corridor map are known.")
tl = [("Now", "$800K / month", "Private accounts, USD-first, card-not-present"),
      ("Month 6", "3 corridors live", "South and South-East Asia; plugins adopted; local methods where available"),
      ("Month 12", "Consolidated book", "Volume migrated under KD PAY LLC; connected accounts for top merchants"),
      ("Year 2", "Global corridors", "EU/UK with SCA, US/Canada, LatAm; multi-currency settlement")]
cw = (CW - 0.75) / 4
for i, (when, head, body) in enumerate(tl):
    x = ML + i * (cw + 0.25)
    dark = i == 3
    rect(s, x, y + 0.1, cw, 2.2, fill=INK if dark else SURFACE, radius=0.05)
    text(s, x + 0.24, y + 0.3, cw - 0.48, 0.22, when.upper(), size=9, bold=True,
         color=ACCENT, tracking=1.3)
    text(s, x + 0.24, y + 0.62, cw - 0.48, 0.55, head, size=14, bold=True,
         color=WHITE if dark else TEXT, spacing=1.08)
    text(s, x + 0.24, y + 1.18, cw - 0.48, 0.95, body, size=9.8,
         color=DARK_MUT if dark else MUTED, spacing=1.25)

by = y + 2.62
text(s, ML, by, CW, 0.3, "What Airwallex gets", size=9.5, color=MUTED, bold=True, caps=True, tracking=1.4)
benefits = ["Quality volume, not raw volume — verified merchants, 0.01% disputes, reserves funded",
            "A partner that owns merchant onboarding, support and disputes in-region",
            "Corridor expansion driven by real merchant demand, not speculation",
            "A technical team that integrates against your documented contracts"]
para_list(s, ML, by + 0.34, CW, 1.4, benefits, size=10.5, gap=9, bullet="—")
footer(s, 15)
notes(s, "Be careful not to inflate. The year-2 column is ambition. If they ask for a forecast with numbers, "
         "say we will model it with their pricing sheet and send it within a week — that is a stronger answer "
         "than an invented spreadsheet.")

# =====================================================================
# 16 · NEXT STEPS (dark)
# =====================================================================
s = slide(prs, INK)
y = header(s, "Next steps", "Four decisions to make this week", dark=True, title_size=30)
steps = [("01", "Confirm the model", "Seller ledger at launch, connected accounts as we scale — in writing, "
          "so both teams build against the same contract."),
         ("02", "Share the corridor map", "Which markets you can support today, which are 6–12 months out, "
          "and what local methods exist in each."),
         ("03", "Agree commercials", "Pricing at $800K/month and at growth volume, settlement timing, reserve "
          "terms and who carries dispute cost."),
         ("04", "Book the technical kickoff", "Sandbox keys and a named solutions engineer; our team can start "
          "the week after.")]
cw = (CW - 0.75) / 4
for i, (n, t, b) in enumerate(steps):
    x = ML + i * (cw + 0.25)
    text(s, x, y + 0.1, 1.0, 0.3, n, size=10, color=ACCENT, bold=True, tracking=1.4)
    text(s, x, y + 0.45, cw - 0.2, 0.4, t, size=13, bold=True, color=WHITE, spacing=1.06)
    text(s, x, y + 0.95, cw - 0.25, 1.4, b, size=9.8, color=DARK_MUT, spacing=1.25)
    if i < 3:
        vline(s, x + cw - 0.02, y + 0.12, 2.05, color=DARK_LN)

hline(s, ML, y + 2.42, CW, color=DARK_LN, weight=0.8)
text(s, ML, y + 2.6, CW, 0.24, "What we bring to the kickoff", size=9, color=ACCENT, bold=True,
     caps=True, tracking=1.3)
for i, item in enumerate(["Entity documents and the completed KYB pack",
                          "A named integration owner and sandbox API keys",
                          "Twenty pilot merchants, pre-screened"]):
    x = ML + i * (CW / 3)
    text(s, x, y + 2.95, CW / 3 - 0.35, 0.5, item, size=10, color=WHITE, spacing=1.2)

rect(s, ML, 5.32, CW, 1.06, fill=ACCENT, radius=0.04)
text(s, ML + 0.35, 5.48, CW - 0.7, 0.3,
     "Target: first live transaction eight weeks from approval.", size=15, bold=True, color=INK)
text(s, ML + 0.35, 5.86, CW - 0.7, 0.3,
     "KD PAY LLC  ·  [name] · [title] · [email] · [phone]", size=10,
     color=INK, spacing=1.1)
footer(s, 16, dark=True)
notes(s, "Close by asking for the two things that unblock everything: written confirmation of the model, and "
         "sandbox access. Replace the bracketed contact details before sending — they are intentionally left "
         "as placeholders.")

# =====================================================================
# 17 · APPENDIX — INTEGRATION DETAIL
# =====================================================================
s = slide(prs)
y = header(s, "Appendix A", "Integration and controls, for your solutions engineer")
cols = [("Area", 0.24), ("How we implement it", 0.5), ("Contract", 0.26)]
rows = [
 ("Checkout", "Hosted page with your Elements; no card data in our origin", "PCI SAQ-A scope"),
 ("Webhooks", "Signature verified, event deduplicated, retried with backoff", "At-least-once, idempotent"),
 ("Idempotency", "Client key on every mutating call, 24-hour replay window", "Safe retries"),
 ("Ledger", "Double-entry, append-only, hash-chained; mirrors your settlement", "Reconcilable daily"),
 ("Reconciliation", "Settlement import, matching, exception queue, daily close", "Variance < $1 investigated"),
 ("Reporting", "Merchant statements, fee reports, payout reconciliation", "CSV + PDF"),
 ("Environments", "Separate sandbox and live keys, no data crossover", "Test before live"),
 ("Disputes", "Intake from your webhooks, evidence portal, deadline alerts", "Response within SLA"),
]
ty = table(s, ML, y + 0.05, CW, cols, rows, row_h=0.44, body_size=10)
text(s, ML, ty + 0.15, CW, 0.4,
     "Stack: TypeScript / Next.js on Vercel · Postgres (Supabase) with row-level security · "
     "Cloudflare at the edge · double-entry ledger written from scratch, not bolted on.",
     size=9.5, color=MUTED, spacing=1.2)
footer(s, 17)
notes(s, "Hand this page to their engineer. It answers the integration questions in their language: idempotency, "
         "webhook semantics, reconciliation tolerance, environment separation.")

# =====================================================================
# 18 · APPENDIX — DUE DILIGENCE PACK
# =====================================================================
s = slide(prs)
y = header(s, "Appendix B", "What we can provide during due diligence",
           lead="We expect underwriting. Here is the pack, ready on request under NDA.")
pack = [("Corporate", ["Certificate of formation and good standing", "Operating agreement and ownership chart",
                       "Board resolution and signatory list"]),
        ("Financial", ["12 months of processing statements", "Chargeback and refund reports",
                       "Bank statements for the operating account"]),
        ("Merchant", ["Sample merchant agreements and KYB files (redacted)", "Merchant mix and MCC summary",
                      "Onboarding and monitoring procedures"]),
        ("Technical", ["Security architecture document", "PCI SAQ-A plan and ASV scan schedule",
                       "Data-flow diagram and sub-processor list"])]
cw = (CW - 0.75) / 4
ph = 0.72 + max(sum(text_h(it, cw - 0.5, 9.5) + 0.09 for it in items) for _, items in pack)
ph = max(ph, 1.95)
for i, (t, items) in enumerate(pack):
    x = ML + i * (cw + 0.25)
    rect(s, x, y + 0.1, cw, ph, fill=SURFACE, radius=0.05)
    text(s, x + 0.24, y + 0.3, cw - 0.48, 0.26, t.upper(), size=9.5, color=ACCENT_D, bold=True,
         tracking=1.3)
    para_list(s, x + 0.24, y + 0.66, cw - 0.45, ph - 0.75, items, size=9.5, gap=7, spacing=1.18)

ty2 = y + 0.1 + ph + 0.42
hline(s, ML, ty2 - 0.18, CW, color=LINE, weight=0.8)
text(s, ML, ty2, CW, 0.4,
     "Open item we will address first: the processing history sits with our operating entity; KD PAY LLC is new. "
     "We will provide continuity evidence and references so the underwriting risk is clear, not hidden.",
     size=10, color=MUTED, spacing=1.25)

by2 = 5.15
rect(s, ML, by2, CW, 1.05, fill=INK, radius=0.05)
text(s, ML + 0.35, by2 + 0.2, 4.0, 0.24, "WHAT WE NEED FROM YOU", size=9, color=ACCENT,
     bold=True, tracking=1.3)
for i, item in enumerate(["Pricing sheet and reserve terms at our volume",
                          "Capability and corridor matrix, today and roadmap",
                          "Draft term sheet, SLA and settlement timetable"]):
    text(s, ML + 0.35 + i * ((CW - 0.7) / 3), by2 + 0.55, (CW - 0.7) / 3 - 0.3, 0.42, item,
         size=9.8, color=WHITE, spacing=1.15)
footer(s, 18)
notes(s, "Ending on the entity issue is deliberate: it is the one thing underwriting will find, so we frame it "
         "before they do. Say we would rather over-share than have it surface late in the process.")

# document properties (visible in File > Info / Finder)
cp = prs.core_properties
cp.title = "KD PAY LLC — Airwallex partnership proposal"
cp.subject = "Payment platform partnership for Asia-first cross-border merchants"
cp.author = "KD PAY LLC"
cp.last_modified_by = "KD PAY LLC"
cp.category = "Partnership proposal"
cp.keywords = "Airwallex, payments, Asia, cross-border, platform, partnership"
cp.comments = ("18-slide proposal deck. Figures supplied by KD PAY: $800K monthly volume, 0.01% "
               "chargeback ratio, operating since 2022. See deck/SOURCES.md for the basis of every claim.")

out = os.path.join(os.path.dirname(__file__), "KD-PAY-Airwallex-Partnership.pptx")
prs.save(out)
print("saved", out, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
