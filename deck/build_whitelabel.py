# -*- coding: utf-8 -*-
"""Builds KD-PAY-Airwallex-White-Label-Proposal.pptx — 17 slides, business model first.

Narrative: proposition -> the ask -> who we are -> the gap -> corridors -> business model ->
what white-label means -> three structures -> distribution -> economics -> risk -> security ->
why us -> 12 months -> next steps -> appendix.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

prs = new_deck()
LABEL = "KD PAY LLC  ·  White-label partnership proposal  ·  Confidential"

# =====================================================================
# 01 · TITLE
# =====================================================================
s = slide(prs, INK)
rect(s, ML, 1.05, 0.06, 3.05, fill=ACCENT)
text(s, ML + 0.28, 1.02, 9.5, 0.26, "Partnership proposal  ·  Confidential", size=10,
     color=ACCENT, bold=True, caps=True, tracking=1.8)
text(s, ML + 0.28, 1.42, 10.9, 2.4,
     "White-label payments for Asia,\non Airwallex rails", size=40, color=WHITE,
     bold=True, spacing=1.08)
text(s, ML + 0.28, 3.82, 9.9, 0.9,
     "KD PAY LLC — proposal to operate the merchant-facing layer as your white-label and "
     "merchant-of-record partner.", size=15, color=DARK_MUT, spacing=1.3)

hy = 5.30
hline(s, ML, hy, CW, color=DARK_LN, weight=0.8)
for i, (v, l) in enumerate([("$800K", "monthly volume"), ("0.01%", "chargeback ratio"),
                            ("2022", "operating since"), ("Asia → global", "corridor roadmap")]):
    x = ML + i * (CW / 4)
    stat(s, x, hy + 0.26, CW / 4 - 0.25, v, l, dark=True,
         color=ACCENT if i < 2 else WHITE, vsize=22)
text(s, W - MR - 3.2, 1.02, 3.2, 0.26, "30 October 2026", size=10, color=DARK_MUT,
     align=PP_ALIGN.RIGHT, caps=True, tracking=1.4)
footer(s, 1, dark=True, label=LABEL)
notes(s, "Opening (45 seconds). We want to run the merchant-facing layer in Asia on your rails — our brand, "
         "our merchants, our merchant-level risk; your licence, your acquiring, your settlement. "
         "The deck is about the business model, not the software: who does what, how the money works, and "
         "what we need from you to start.")

# =====================================================================
# 02 · THE PROPOSITION
# =====================================================================
s = slide(prs)
y = header(s, "The proposition", "You own the rails. We own the merchant.",
           lead="One partnership, two layers. Nothing about how you underwrite us changes — we become the "
                "front office for merchants you would otherwise not reach.")
bw3 = (CW - 2 * 0.95) / 3
boxes = [
    ("AIRWALLEX", "The rail", "Licensing, acquiring, network membership, FX liquidity, settlement and the "
     "regulated obligations that sit with a provider.", INK, WHITE, DARK_MUT),
    ("KD PAY", "The merchant layer", "Brand, sales, onboarding and KYB operations, in-region support, "
     "dispute handling and merchant-level reserves.", ACCENT_S, TEXT, MUTED),
    ("THE MERCHANT", "One relationship", "One contract, one dashboard, local payment methods, and payouts in "
     "the currency their bank actually holds.", SURFACE, TEXT, MUTED),
]
for i, (kick, head, body, fill, tcol, bcol) in enumerate(boxes):
    x = ML + i * (bw3 + 0.95)
    rect(s, x, y + 0.05, bw3, 2.05, fill=fill, line=None, radius=0.05)
    if i == 1:
        rect(s, x, y + 0.05, bw3, 0.055, fill=ACCENT)
    text(s, x + 0.26, y + 0.26, bw3 - 0.5, 0.22, kick, size=8.5, bold=True, tracking=1.5,
         color=ACCENT if i != 0 else ACCENT)
    text(s, x + 0.26, y + 0.55, bw3 - 0.5, 0.34, head, size=15, bold=True, color=tcol, spacing=1.05)
    text(s, x + 0.26, y + 0.98, bw3 - 0.5, 0.95, body, size=9.5, color=bcol, spacing=1.2)
    if i < 2:
        arrow(s, x + bw3 + 0.2, y + 1.0, 0.52, color=ACCENT, weight=1.6)

qy = y + 2.35
rect(s, ML, qy, CW, 0.92, fill=INK, radius=0.04)
text(s, ML + 0.34, qy + 0.2, CW - 0.68, 0.6,
     "We are not asking to become a PSP. We are asking to rent the rails, put our name in front of the "
     "merchant, and carry the merchant-level risk that makes the volume possible.",
     size=12.8, color=WHITE, spacing=1.22)

gy = qy + 1.30
text(s, ML, gy, CW, 0.24, "What this gives you", size=9, color=MUTED, bold=True, caps=True, tracking=1.4)
gains = [("Corridor reach", "Verified Asian merchants, underwritten to your standards, without you building "
          "a regional sales or support operation."),
         ("Risk that is already tidy", "$800K a month at a 0.01% dispute rate, with reserves funded at "
          "merchant level before anything reaches you."),
         ("One counterparty", "A single US entity on your paper, one KYB file, one reconciliation, one "
          "escalation path — instead of hundreds of SMBs.")]
for i, (h, b) in enumerate(gains):
    x = ML + i * (CW / 3)
    text(s, x, gy + 0.30, CW / 3 - 0.42, 0.26, h, size=10.5, bold=True, color=TEXT)
    text(s, x, gy + 0.58, CW / 3 - 0.42, 0.75, b, size=9.2, color=MUTED, spacing=1.22)
footer(s, 2, label=LABEL)
notes(s, "This is the whole idea on one page. Airwallex keeps every regulated function — you stay the licensed "
         "party, you keep settlement, you keep the network relationships. We take the customer-facing side: "
         "brand, sales, onboarding ops, support, disputes, reserves. The merchant never has to deal with two "
         "companies. If they push: we are not trying to be a processor, we are trying to be your distribution "
         "channel in Asia.")

# =====================================================================
# 03 · THE ASK
# =====================================================================
s = slide(prs)
y = header(s, "The ask", "Three things, and what you get back",
           lead="Everything else in this deck supports this page.")
asks = [
    ("01", "Programme approval",
     "A white-label or merchant-of-record programme at launch, so the merchant contracts with KD PAY and we "
     "carry merchant-level risk and first-line support."),
    ("02", "Corridor commitment",
     "Written confirmation of which Asian corridors are live today, which are 6–12 months out, and which "
     "local payment methods exist in each."),
    ("03", "Commercials and support",
     "Pricing at $800K/month and at growth volume, reserve terms that reflect a 0.01% record, and a named "
     "partner manager plus solutions engineer."),
]
cw = (CW - 0.5) / 3
for i, (n, t, b) in enumerate(asks):
    card(s, ML + i * (cw + 0.25), y + 0.12, cw, 2.45, n, t, b, body_size=10.8)

by = y + 2.80
rect(s, ML, by, CW, 0.92, fill=ACCENT_S, radius=0.05)
text(s, ML + 0.3, by + 0.16, 3.4, 0.24, "What we bring", size=9.5, color=ACCENT_D, bold=True,
     caps=True, tracking=1.4)
text(s, ML + 0.3, by + 0.46, CW - 0.6, 0.4,
     "Entity pack and KYB file in week one  ·  sandbox integration in 14 days  ·  first live transaction in "
     "8 weeks  ·  20 pre-screened pilot merchants.", size=10.8, color=TEXT, spacing=1.2)

wy = by + 1.28
text(s, ML, wy, CW, 0.24, "Why this is worth your time now", size=9, color=MUTED, bold=True,
     caps=True, tracking=1.3)
why = [("A corridor, not a campaign. ", "One partner bringing verified Asian merchants into your rails."),
       ("Small and clean. ", "$800K a month at 0.01% chargebacks — enough to prove the model."),
       ("Built to your contracts. ", "Real onboarding, real reconciliation, real evidence.")]
for i, (h, b) in enumerate(why):
    x = ML + i * (CW / 3)
    rich(s, x, wy + 0.30, CW / 3 - 0.45, 0.45, [(h, True, TEXT), (b, False, MUTED)],
         size=9.3, spacing=1.25)
footer(s, 3, label=LABEL)
notes(s, "Say these three out loud, in this order. Programme approval is the gate — without it nothing else "
         "matters. The corridor list is what decides our roadmap; we will not promise a market we cannot "
         "service. Commercials can be fixed after the model is agreed, but the reserve terms should reflect "
         "the 0.01% record from day one.")

# =====================================================================
# 04 · WHO WE ARE
# =====================================================================
s = slide(prs)
y = header(s, "Company", "Who we are")
left_w = 6.55
intro = ("KD PAY LLC is a US-registered payment company for Asian merchants that sell to buyers anywhere. "
         "We own the merchant relationship: onboarding, local acquiring partnerships, payouts, disputes "
         "and reconciliation.")
ih = text_h(intro, left_w, 13.5, spacing=1.35)
text(s, ML, y + 0.05, left_w, ih + 0.1, intro, size=13.5, color=TEXT, spacing=1.35)
paras = [
 ("Operating history. ", "Since 2022 through our operating company. KD PAY LLC is the new contracting and "
  "processing entity, registered October 2026."),
 ("Today. ", "We process through private merchant accounts at incumbent providers — B2B and B2C, "
  "card-not-present, USD-first."),
 ("Why change now. ", "Private accounts cannot deliver Asian coverage, local payment methods or the "
  "economics that let us scale. We want one platform relationship instead of nine."),
 ("How we work. ", "A small team that ships, against a written specification. We run merchant operations "
  "ourselves — we are not a reseller passing tickets upstream."),
]
para_list(s, ML, y + 0.05 + ih + 0.28, left_w, 2.7, paras, size=11.2, gap=8)

tly = y + 3.62
hline(s, ML, tly, left_w - 0.3, color=LINE, weight=0.8)
for i, (when, what) in enumerate([("2022", "Trading starts"), ("Oct 2026", "KD PAY LLC registered"),
                                  ("Next", "White-label launch")]):
    x = ML + i * ((left_w - 0.3) / 3)
    rect(s, x, tly - 0.045, 0.11, 0.11, fill=ACCENT, radius=0.5)
    text(s, x, tly + 0.16, (left_w - 0.3) / 3 - 0.3, 0.22, when.upper(), size=8.5, bold=True,
         color=ACCENT_D, tracking=1.1)
    text(s, x, tly + 0.38, (left_w - 0.3) / 3 - 0.3, 0.4, what, size=9.2, color=MUTED, spacing=1.18)

rx = ML + left_w + 0.55
rw = W - MR - rx
rect(s, rx, y, rw, 4.5, fill=SURFACE, radius=0.04)
text(s, rx + 0.3, y + 0.25, rw - 0.6, 0.24, "At a glance", size=9.5, color=MUTED, bold=True,
     caps=True, tracking=1.4)
facts = [("Legal entity", "KD PAY LLC (US)"),
         ("Operating since", "2022"),
         ("Model sought", "White-label / merchant of record"),
         ("Monthly volume", "≈ $800,000"),
         ("Chargeback ratio", "0.01%"),
         ("Merchant mix", "B2B and B2C, card-not-present"),
         ("Target markets", "Asia, EU/UK, US, LatAm")]
fy = y + 0.62
for k, v in facts:
    text(s, rx + 0.3, fy, rw - 0.6, 0.2, k.upper(), size=8.5, color=MUTED, bold=True, tracking=0.9)
    text(s, rx + 0.3, fy + 0.2, rw - 0.6, 0.3, v, size=11, color=TEXT)
    fy += 0.55
footer(s, 4, label=LABEL)
notes(s, "Be upfront about the entity change before they ask: the team and the book are from 2022, the LLC is "
         "new. Underwriting will find it, so we frame it first — and slide 17 offers statements and references "
         "under NDA. The 'model sought' line is deliberate: we are applying for a white-label programme, we "
         "are not claiming we already have one.")

# =====================================================================
# 05 · THE GAP
# =====================================================================
s = slide(prs)
y = header(s, "The opportunity", "Asian merchants can sell globally. They cannot get paid globally.",
           title_size=27,
           lead="The constraint is not demand. It is acceptance infrastructure — and it is why merchants "
                "leave their current providers.")
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
cw4 = (CW - 0.75) / 4
for i, (t, b) in enumerate(blocks):
    x = ML + i * (cw4 + 0.25)
    rect(s, x, y + 0.12, cw4, 2.62, fill=SURFACE, radius=0.05)
    rect(s, x, y + 0.12, cw4, 0.05, fill=ACCENT)
    text(s, x + 0.22, y + 0.32, cw4 - 0.44, 0.5, t, size=12.5, bold=True, color=TEXT, spacing=1.05)
    text(s, x + 0.22, y + 0.82, cw4 - 0.44, 1.1, b, size=10, color=MUTED, spacing=1.28)
    hline(s, x + 0.22, y + 2.0, cw4 - 0.44, color=LINE, weight=0.7)
    text(s, x + 0.22, y + 2.12, cw4 - 0.44, 0.42, cost[i], size=8.8, bold=True, color=ACCENT_D,
         spacing=1.15)

cy = y + 2.90
rect(s, ML, cy, CW, 0.85, fill=INK, radius=0.05)
text(s, ML + 0.35, cy + 0.17, CW - 0.7, 0.58,
     "Merchants do not need another dashboard. They need one relationship that accepts money where their "
     "buyers are, and pays them where they bank.", size=13, color=WHITE, spacing=1.2)
footer(s, 5, label=LABEL)
notes(s, "This is the business case, not a product pitch. Every point is something we hear from merchants "
         "weekly. Avoid quoting decline percentages unless we have our own data — 'materially higher' is "
         "defensible, an invented number is not.")

# =====================================================================
# 06 · CORRIDORS
# =====================================================================
s = slide(prs)
y = header(s, "Go-to-market", "Asia first, then the world",
           lead="Density in a few corridors beats thin coverage everywhere. A corridor opens only when you "
                "confirm coverage.")
grp = [("South Asia", "Bangladesh · India · Pakistan · Sri Lanka",
        "Cards, local bank transfer, wallets — the largest underserved merchant base"),
       ("South-East Asia", "Singapore · Malaysia · Indonesia · Philippines",
        "Cards plus FPX, DuitNow, QRIS, GCash, GrabPay-class wallets"),
       ("East Asia", "Hong Kong · Japan", "Cards and wallets; strongest buyer-side card acceptance"),
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
 ("Wedge: ", "Asian merchants invoicing Western buyers in USD. The buyer's card is the rail; the merchant's "
  "bank account is the problem we solve."),
 ("Density: ", "A corridor is only worth opening when we can support the methods buyers actually use, not "
  "just cards."),
 ("Dependency: ", "Each corridor depends on your licensing and local acquiring. We plan around your coverage "
  "map, not our wish list."),
 ("Expansion: ", "EU/UK, US and LatAm come once SCA and 3DS2 flows are proven — not before."),
], size=11, gap=10)
footer(s, 6, label=LABEL)
notes(s, "Ask them directly: which of these corridors can you support today, and which are 6-12 months away? "
         "That answer re-orders our roadmap. We deliberately do not promise all of Asia on day one.")

# =====================================================================
# 07 · BUSINESS MODEL
# =====================================================================
s = slide(prs)
y = header(s, "Business model", "Four lines of revenue, one merchant relationship",
           lead="A platform business that earns on volume, not on licences or one-off fees.")
rev = [("01", "Take rate on volume", "Our margin over your cost of acceptance. Grows with the book, "
        "not with headcount."),
       ("02", "FX on settlement", "Merchants want to be paid in the currency their bank holds; the "
        "spread is priced into the conversion."),
       ("03", "Platform subscription", "A monthly fee per merchant for the dashboard, invoicing, payouts "
        "and support."),
       ("04", "Service fees", "Dispute handling, chargeback representation, faster payouts, premium "
        "onboarding.")]
cw = (CW - 0.5) / 4
for i, (n, t, b) in enumerate(rev):
    card(s, ML + i * (cw + 0.166), y + 0.1, cw, 2.15, n, t, b, body_size=9.6)

by = y + 2.35
rect(s, ML, by, CW, 1.02, fill=INK, radius=0.05)
text(s, ML + 0.34, by + 0.18, 3.2, 0.24, "Why this survives scale", size=9, color=ACCENT, bold=True,
     caps=True, tracking=1.4)
text(s, ML + 0.34, by + 0.45, CW - 0.68, 0.5,
     "Revenue per merchant grows with their volume while our cost to serve is fixed. That is why one book of "
     "hundreds of Asian SMBs is worth more to us — and to you — than the same number of separate applications.",
     size=11.2, color=WHITE, spacing=1.22)

my = by + 1.40
text(s, ML, my, CW, 0.24, "How the pricing conversation should go", size=9, color=MUTED, bold=True,
     caps=True, tracking=1.3)
ladder = [("$800K → $2M", "our volume, before any new merchant"),
          ("Take rate 2.0% → 1.5%", "our price falls as the book grows"),
          ("$16K → $30K", "monthly gross revenue at those two points"),
          ("Fixed cost base", "only support and operations scale")]
for i, (v, l) in enumerate(ladder):
    x = ML + i * (CW / 4)
    text(s, x, my + 0.32, CW / 4 - 0.28, 0.26, v, size=12.5, bold=True, color=ACCENT_D, spacing=1.0)
    text(s, x, my + 0.66, CW / 4 - 0.28, 0.45, l, size=8.8, color=MUTED, spacing=1.18)
footer(s, 7, label=LABEL)
notes(s, "They will want to know how we make money, because it tells them whether we will survive. Four lines, "
         "all volume-linked. Be explicit that we do not touch float: merchant funds sit in your ledger, not in "
         "our bank account. That single sentence removes most of the risk questions about a small partner.")

# =====================================================================
# 08 · WHAT WHITE-LABEL MEANS
# =====================================================================
s = slide(prs)
y = header(s, "White-label", "The merchant sees one company. You stay the rail.",
           lead="White-label is a product feature, not a way of hiding you. Here is exactly what changes hands.")
lw = 6.35
text(s, ML, y + 0.05, lw, 0.24, "What the merchant experiences", size=9, color=MUTED, bold=True,
     caps=True, tracking=1.3)
seen = [("Login and dashboard", "Our brand, our domain, our design — not a portal with someone else's logo."),
        ("Checkout and receipts", "Our name on the payment page, our receipts, our invoice template."),
        ("Support", "Our team answers, in-region and in the merchant's time zone."),
        ("Statements and payouts", "Our statement format, our payout schedule, our reconciliation view.")]
sy = y + 0.36
for i, (t, b) in enumerate(seen):
    rect(s, ML, sy, lw, 0.72, fill=SURFACE, radius=0.05)
    text(s, ML + 0.24, sy + 0.10, lw - 0.48, 0.24, t, size=10.5, bold=True, color=TEXT)
    text(s, ML + 0.24, sy + 0.36, lw - 0.48, 0.3, b, size=9, color=MUTED, spacing=1.15)
    sy += 0.81

rx = ML + lw + 0.62
rw = W - MR - rx
rect(s, rx, y + 0.05, rw, 2.32, fill=INK, radius=0.05)
text(s, rx + 0.3, y + 0.28, rw - 0.6, 0.24, "What stays yours", size=9, color=ACCENT, bold=True,
     caps=True, tracking=1.3)
for i, item in enumerate(["The licence and the network relationships",
                          "Acquiring, scheme and settlement obligations",
                          "Your name in the merchant agreement",
                          "The statement descriptor, where regulation requires it"]):
    text(s, rx + 0.3, y + 0.62 + i * 0.42, rw - 0.6, 0.4, item, size=9.5, color=WHITE, spacing=1.18)

rect(s, rx, y + 2.62, rw, 1.62, fill=ACCENT_S, radius=0.05)
text(s, rx + 0.3, y + 2.82, rw - 0.6, 0.24, "What we never ask for", size=9, color=ACCENT_D, bold=True,
     caps=True, tracking=1.3)
for i, item in enumerate(["Your brand", "Your balance sheet", "Your regulatory cover"]):
    text(s, rx + 0.3, y + 3.16 + i * 0.32, rw - 0.6, 0.3, "×  " + item, size=9.8, color=TEXT, spacing=1.1)
footer(s, 8, label=LABEL)
notes(s, "This slide exists to kill the two objections that come with the word white-label: 'are you hiding us "
         "from the merchant' and 'are you asking to use our licence'. The answer is no to both. Your name "
         "stays in the merchant agreement and on the statement descriptor where regulation requires it — that "
         "is what a defensible white-label programme looks like, and it is what we want to run.")

# =====================================================================
# 09 · THREE STRUCTURES
# =====================================================================
s = slide(prs)
y = header(s, "Structure", "Three ways to sign this — and why we recommend the first",
           title_size=27,
           lead="All three need your underwriting approval. The words 'merchant of record' are contractual, so "
                "nothing here is claimed until it is signed.")
cols = [("Structure", 0.215), ("A · White-label, KD PAY as MOR", 0.265),
        ("B · White-label, Airwallex as MOR", 0.26), ("C · Connected accounts", 0.26)]
rows = [
 ("Merchant contracts with", "KD PAY, on our paper", "KD PAY, on your paper", "The merchant directly"),
 ("Merchant of record", "KD PAY (proposed)", "Airwallex", "The merchant"),
 ("Who KYBs merchants", "Our ops team, to your standards", "Your team, we front it", "Your team, per merchant"),
 ("Who holds funds", "Your ledger + our reserve", "Your ledger", "Merchant's own wallet"),
 ("Chargeback and fraud loss", "KD PAY", "Split, negotiated", "The merchant"),
 ("Time to first payment", "Weeks", "2–3 months", "Days per merchant"),
]
ty = table(s, ML, y + 0.02, CW, cols, rows, row_h=0.52, body_size=9.6, header_size=8.6)

ry = ty + 0.22
rect(s, ML, ry, CW, 0.78, fill=ACCENT_S, radius=0.05)
text(s, ML + 0.3, ry + 0.14, 3.6, 0.24, "Our recommendation", size=9, color=ACCENT_D, bold=True,
     caps=True, tracking=1.3)
text(s, ML + 0.3, ry + 0.42, CW - 0.6, 0.35,
     "A at launch for the SMB book  ·  B if you need to hold the record yourself  ·  C in year two for "
     "enterprise merchants who want their own account.", size=10.4, color=TEXT, spacing=1.2)
footer(s, 9, label=LABEL)
notes(s, "Do not oversell A. Say: we think A is fastest for both of us, but B is a perfectly good starting "
         "point if your risk committee needs to hold the record — we can migrate to A later without "
         "re-papering merchants. C is the model you already run for marketplaces; we would use it only for "
         "the handful of enterprise merchants who need their own account and are happy to be KYC'd twice.")

# =====================================================================
# 10 · DISTRIBUTION
# =====================================================================
s = slide(prs)
y = header(s, "Distribution", "How merchants actually arrive",
           lead="In Asia, the integration is the sales channel. Phase 1 is deliberately the smallest thing that "
                "lets a merchant take a card payment this week.")
ch = [("01", "Shopify and WooCommerce",
       "Plugins for both platforms: install, paste a key, take payments. Most Asian SMBs have no developer — "
       "this is the whole go-to-market for the long tail."),
      ("02", "Hosted checkout and links",
       "For merchants with no store platform at all: invoice, send a link, get paid. Works on any site, "
       "mobile-first."),
      ("03", "Partner and agency channel",
       "Agencies, hosting companies and ERP integrators who already serve these merchants. One partner brings "
       "twenty merchants.")]
cw = (CW - 0.5) / 3
for i, (n, t, b) in enumerate(ch):
    card(s, ML + i * (cw + 0.25), y + 0.1, cw, 2.05, n, t, b, body_size=10.2)

sy = y + 2.42
text(s, ML, sy, CW, 0.24, "Why distribution beats features here", size=9, color=MUTED, bold=True,
     caps=True, tracking=1.3)
pts = [("Time to live", "Hours, not weeks — the merchant installs and starts."),
       ("Local methods", "Wallets and bank transfer decide conversion in Asia, not card branding."),
       ("Support language", "Bangla, Hindi, Bahasa and English at first line."),
       ("One contract", "The merchant deals with us, not with a queue at a provider.")]
for i, (h, b) in enumerate(pts):
    x = ML + i * (CW / 4)
    text(s, x, sy + 0.32, CW / 4 - 0.32, 0.26, h, size=10.3, bold=True, color=TEXT)
    text(s, x, sy + 0.6, CW / 4 - 0.32, 0.55, b, size=9.2, color=MUTED, spacing=1.2)
footer(s, 10, label=LABEL)
notes(s, "The user has asked to keep software out of this deck, so keep this high level: three ways in, no "
         "architecture. The point for Airwallex is distribution — we already sit next to these merchants. If "
         "they ask what is built today, be precise: the integration layer is in build, the merchant base and "
         "the operations are live.")

# =====================================================================
# 11 · ECONOMICS
# =====================================================================
s = slide(prs)
y = header(s, "Economics", "What the model is worth at our volume",
           lead="Take rate is the percentage we charge a merchant on card volume. Illustrative only — no price "
                "has been discussed with you yet.")
cols = [("Monthly volume", 0.36), ("1.0% take", 0.21), ("1.5% take", 0.21), ("2.0% take", 0.21)]
rows = [("Today — $800,000", "$8,000", "$12,000", "$16,000"),
        ("$2,000,000", "$20,000", "$30,000", "$40,000"),
        ("$5,000,000", "$50,000", "$75,000", "$100,000"),
        ("$10,000,000", "$100,000", "$150,000", "$200,000")]
ty = table(s, ML, y + 0.05, 7.1, cols, rows, row_h=0.62, body_size=11, header_size=8.8,
           col_colors={1: TEXT, 2: ACCENT_D, 3: TEXT})
text(s, ML, ty + 0.18, 7.1, 0.6,
     "Monthly gross revenue, before your cost of acceptance. The split between your fee and our margin is the "
     "commercial conversation — and it should get better as the book grows.",
     size=9.6, color=MUTED, spacing=1.25)

rx = ML + 7.5
rw = W - MR - rx
rect(s, rx, y + 0.05, rw, 3.55, fill=INK, radius=0.05)
text(s, rx + 0.3, y + 0.26, rw - 0.6, 0.24, "What the take has to cover", size=9, color=ACCENT,
     bold=True, caps=True, tracking=1.3)
for i, item in enumerate(["Your cost of acceptance",
                          "Merchant onboarding and KYB operations",
                          "First-line support and disputes",
                          "Chargeback and fraud losses",
                          "Reserves and working capital"]):
    text(s, rx + 0.3, y + 0.60 + i * 0.36, rw - 0.6, 0.32, "—  " + item, size=9.6, color=WHITE,
         spacing=1.15)
text(s, rx + 0.3, y + 2.52, rw - 0.6, 0.9,
     "At 0.01% disputes, the loss line is close to zero — which is why we can argue for a thinner spread "
     "than a generic SMB book.", size=9, color=DARK_MUT, spacing=1.2)
footer(s, 11, label=LABEL)
notes(s, "Be careful here: these are our take-rate scenarios, not their pricing. The purpose is to show the "
         "shape of the business — revenue scales linearly with volume, and our cost to serve is largely fixed. "
         "If they ask for a real model, say we will build it with their pricing sheet within a week. That is a "
         "much stronger answer than an invented spreadsheet.")

# =====================================================================
# 12 · RISK
# =====================================================================
s = slide(prs)
y = header(s, "Risk", "Our dispute record, against the threshold that matters",
           lead="Card networks start monitoring a merchant above 0.9% chargebacks. We operate at 0.01%.")
bx, bw = ML, 6.55
text(s, bx, y + 0.05, 5.0, 0.24, "KD PAY — 0.01%", size=10.5, bold=True, color=ACCENT_D)
rect(s, bx, y + 0.33, bw, 0.30, fill=SURFACE, radius=0.02)
rect(s, bx, y + 0.33, 0.07, 0.30, fill=ACCENT, radius=0.02)
text(s, bx + 0.16, y + 0.37, 6.0, 0.24, "1 dispute per 10,000 transactions", size=9.5, color=MUTED)
text(s, bx, y + 0.85, 3.6, 0.24, "Network monitoring threshold — 0.9%", size=10.5, bold=True, color=TEXT)
text(s, bx + bw - 1.45, y + 0.86, 1.45, 0.24, "90× headroom", size=9.5, bold=True, color=ACCENT_D,
     align=PP_ALIGN.RIGHT)
rect(s, bx, y + 1.13, bw, 0.30, fill=RGBColor(0xC9, 0xD3, 0xDE), radius=0.02)

vy = y + 1.72
text(s, bx, vy, 6.3, 0.24, "HOW A RECORD LIKE THIS IS KEPT", size=9, color=MUTED, bold=True, tracking=1.3)
para_list(s, bx, vy + 0.32, 6.9, 1.9, [
 ("Verified buyers. ", "Invoices to known business counterparties; consumer volume screened before onboarding."),
 ("Rules, not luck. ", "3DS2 forced on VPN or IP-country mismatch; AVS postal match for US/CA/UK."),
 ("Hard blocks. ", "Prohibited MCCs, card-fingerprint blocklists, velocity limits per merchant."),
 ("Evidence ready. ", "Reason-code checklists and deadline alerts inside the dispute window."),
], size=9.8, gap=7)

rx3 = ML + 7.55
rw3 = W - MR - rx3
rect(s, rx3, y + 0.05, rw3, 2.5, fill=SURFACE, radius=0.05)
text(s, rx3 + 0.28, y + 0.26, rw3 - 0.5, 0.24, "ON RESERVES", size=9.5, color=ACCENT_D, bold=True,
     tracking=1.3)
para_list(s, rx3 + 0.28, y + 0.62, rw3 - 0.55, 1.75, [
 "We fund risk before we argue about it: merchant-level reserves held by us, plus a platform reserve where "
 "your policy requires one.",
 "Rolling reserve percentage, cap and release schedule are negotiable.",
 "Dispute evidence and merchant follow-up stay with us — you keep the rail.",
], size=9.6, gap=8, bullet_color=ACCENT)

ay = y + 3.5
hline(s, ML, ay - 0.22, CW, color=LINE, weight=0.8)
text(s, ML, ay, CW, 0.24, "What we ask of you", size=9, color=MUTED, bold=True, caps=True, tracking=1.3)
for i, item in enumerate(["A reserve policy proportionate to a 0.01% profile",
                          "Dispute fees disclosed before we sign",
                          "A named escalation contact for high-value cases"]):
    text(s, ML + i * (CW / 3), ay + 0.32, CW / 3 - 0.4, 0.5, item, size=10, color=TEXT, spacing=1.2)
footer(s, 12, label=LABEL)
notes(s, "Say the 0.9% figure as 'around' — Visa and Mastercard use different programmes and bands. The point is "
         "the ratio, not the exact line. 90x headroom is arithmetic: 0.9 divided by 0.01. Then move straight to "
         "reserves: offering to fund them ourselves is what makes a small partner safe to board.")

# =====================================================================
# 13 · SECURITY
# =====================================================================
s = slide(prs)
y = header(s, "Security and compliance", "Eight commitments that protect your rails",
           lead="Not a feature list — the controls we will be audited on, in plain business terms.")
secs = [
 ("01", "Card data never touches us", "Hosted fields and elements. Our scope is PCI DSS SAQ-A, which keeps "
  "our audit surface small."),
 ("02", "Tokens, never card numbers", "We store processor tokens and salted fingerprints. A database breach "
  "yields no usable card data."),
 ("03", "3-D Secure 2 and SCA", "Risk-based challenge, mandatory where regulation requires it, forced on "
  "VPN or IP-country mismatch."),
 ("04", "Encryption everywhere", "TLS 1.3 in transit, AES-256-GCM at rest with versioned keys for bank and "
  "KYC documents."),
 ("05", "MFA and least privilege", "Two-factor on every staff account, role-based access, sessions bound to "
  "the device and revocable in one click."),
 ("06", "Fraud controls built in", "Velocity per IP, device and card; blocklists; instant rejection on your "
  "fraud signals."),
 ("07", "Tamper-evident records", "Append-only, hash-chained audit log of every decision, exported for "
  "your auditors on request."),
 ("08", "KYB, AML and sanctions", "Ownership to 25%, PEP and sanctions screening, ongoing monitoring, and "
  "a documented incident response."),
]
cw4 = (CW - 0.66) / 4
for i, (n, t, b) in enumerate(secs):
    x = ML + (i % 4) * (cw4 + 0.22)
    yy = y + 0.08 + (i // 4) * 1.78
    rect(s, x, yy, cw4, 1.58, fill=SURFACE, radius=0.05)
    text(s, x + 0.22, yy + 0.18, 0.8, 0.2, n, size=8.5, color=ACCENT, bold=True, tracking=1.2)
    text(s, x + 0.22, yy + 0.42, cw4 - 0.44, 0.3, t, size=10.5, bold=True, color=TEXT, spacing=1.05)
    text(s, x + 0.22, yy + 0.76, cw4 - 0.44, 0.75, b, size=8.8, color=MUTED, spacing=1.18)

by = y + 3.78
rect(s, ML, by, CW, 0.95, fill=INK, radius=0.05)
text(s, ML + 0.34, by + 0.16, 4.2, 0.24, "Scope, not theatre", size=9, color=ACCENT, bold=True,
     caps=True, tracking=1.3)
text(s, ML + 0.34, by + 0.44, CW - 0.68, 0.4,
     "We do not claim SOC 2, ISO 27001 or PCI Level 1 that we have not earned. Our card-data scope is "
     "SAQ-A today; the certification roadmap and dates are in the due-diligence pack.", size=10.2,
     color=WHITE, spacing=1.2)
footer(s, 13, label=LABEL)
notes(s, "Keep this at the business level: they are checking whether a small partner is a liability on their "
         "rails. The strongest sentence is the last one — an honest scope statement beats an inflated claim, "
         "and it invites them to tell us which controls their own risk team needs to see. Offer the security "
         "architecture document as follow-up rather than walking through it here.")

# =====================================================================
# 14 · WHY US
# =====================================================================
s = slide(prs)
y = header(s, "Fit", "Why us, and why now",
           lead="We evaluated Stripe Connect, Adyen for Platforms and Airwallex. This is why you won.")
why = [
 ("01", "Asia-first, not Asia-later",
  "Our merchants, our operations and our support are in the region. Your coverage map is the only constraint "
  "we plan around."),
 ("02", "We run the operations ourselves",
  "Onboarding, KYB, support, disputes and reserves. We are not a shell that pipes volume and forwards tickets."),
 ("03", "A clean, small, provable book",
  "$800K a month at 0.01% — enough to prove the model, clean enough to keep your risk team idle."),
 ("04", "White-label ready, not white-label aspirational",
  "Brand, domain, documents and support are ours from day one. Your rails stay untouched underneath."),
]
cw2 = (CW - 0.25) / 2
for i, (n, t, b) in enumerate(why):
    x = ML + (i % 2) * (cw2 + 0.25)
    yy = y + 0.12 + (i // 2) * 1.92
    card(s, x, yy, cw2, 1.72, n, t, b, body_size=10.5)

fy2 = y + 3.98
hline(s, ML, fy2 - 0.2, CW, color=LINE, weight=0.8)
text(s, ML, fy2, CW, 0.24, "What has to be true for this to work", size=9, color=MUTED, bold=True,
     caps=True, tracking=1.3)
conds = [("Corridor by corridor.", "You confirm which markets are live today. We do not assume coverage."),
         ("Underwriting comfort.", "Your risk team is satisfied with how we hold and report merchant exposure."),
         ("Economics that hold at volume.", "Pricing that works at $800K a month and still works at ten times that.")]
for i, (h, b) in enumerate(conds):
    x = ML + i * (CW / 3)
    rich(s, x, fy2 + 0.32, CW / 3 - 0.45, 0.62, [(h + " ", True, TEXT), (b, False, MUTED)],
         size=9.3, spacing=1.25)
footer(s, 14, label=LABEL)
notes(s, "Careful with the comparison — say it as a coverage observation, not a criticism of competitors. The "
         "honest answer to 'what would make you leave' is: coverage gaps in South Asia, and pricing that does "
         "not reflect our dispute record.")

# =====================================================================
# 15 · 12 MONTHS
# =====================================================================
s = slide(prs)
y = header(s, "Outlook", "Where this goes if it works",
           lead="Targets, not projections — we model them again once your pricing and corridor map are known.")
tl = [("Now", "$800K / month", "Private accounts, USD-first, card-not-present"),
      ("Month 6", "3 corridors live", "South and South-East Asia; plugin distribution adopted; pilot book live"),
      ("Month 12", "$2M run-rate ambition", "Volume migrated under KD PAY; enterprise merchants on connected accounts"),
      ("Year 2", "Global corridors", "EU/UK with SCA, US/Canada, LatAm; multi-currency settlement")]
cw = (CW - 0.75) / 4
for i, (when, head, body) in enumerate(tl):
    x = ML + i * (cw + 0.25)
    dark = i == 3
    rect(s, x, y + 0.08, cw, 1.78, fill=INK if dark else SURFACE, radius=0.05)
    text(s, x + 0.24, y + 0.26, cw - 0.48, 0.22, when.upper(), size=9, bold=True,
         color=ACCENT, tracking=1.3)
    text(s, x + 0.24, y + 0.56, cw - 0.48, 0.5, head, size=13.5, bold=True,
         color=WHITE if dark else TEXT, spacing=1.08)
    text(s, x + 0.24, y + 1.02, cw - 0.48, 0.7, body, size=9.1,
         color=DARK_MUT if dark else MUTED, spacing=1.25)

by = y + 2.0
text(s, ML, by, CW, 0.3, "What Airwallex gets", size=9.5, color=MUTED, bold=True, caps=True, tracking=1.4)
benefits = [("Quality volume, not raw volume — ", "verified merchants, 0.01% disputes, reserves funded"),
            ("Ownership in-region — ", "onboarding, support and disputes handled by us, not escalated to you"),
            ("Demand-led expansion — ", "corridors open because merchants ask, not because we speculate"),
            ("A team that integrates properly — ", "we build against your documented contracts")]
para_list(s, ML, by + 0.30, CW, 1.2, benefits, size=9.6, gap=4, bullet="—")

ry2 = by + 1.42
hline(s, ML, ry2 - 0.2, CW, color=LINE, weight=0.8)
text(s, ML, ry2, CW, 0.24, "What could slow this down — and how we handle it", size=9, color=MUTED,
     bold=True, caps=True, tracking=1.3)
risks = [("Corridor coverage arrives later than the market",
          "We sequence launches to your live corridors and sell only what we can service that week."),
         ("KYB throughput becomes the bottleneck",
          "Batch onboarding with your team: fixed weekly cut-off, pre-screened files, named reviewer."),
         ("Our operations team has to scale with volume",
          "Two additional merchant-ops staff by month six, funded from the platform subscription line.")]
for i, (h, b) in enumerate(risks):
    x = ML + i * (CW / 3)
    text(s, x, ry2 + 0.30, CW / 3 - 0.42, 0.3, h, size=9.6, bold=True, color=TEXT, spacing=1.12)
    text(s, x, ry2 + 0.60, CW / 3 - 0.42, 0.5, b, size=8.7, color=MUTED, spacing=1.18)
footer(s, 15, label=LABEL)
notes(s, "Be careful not to inflate. The $2M is our ambition, not a forecast — say so. If they ask for a "
         "numbered forecast, offer to model it with their pricing sheet and send it within a week; that is a "
         "stronger answer than an invented spreadsheet.")

# =====================================================================
# 16 · NEXT STEPS (dark)
# =====================================================================
s = slide(prs, INK)
y = header(s, "Next steps", "Four decisions to make this week", dark=True, title_size=30)
steps = [("01", "Confirm the structure", "A or B in writing, so both teams build against the same contract. "
          "Commercial detail can follow."),
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
     "KD PAY LLC  ·  [name] · [title] · [email] · [phone]", size=10, color=INK, spacing=1.1)
footer(s, 16, dark=True, label=LABEL)
notes(s, "Close by asking for the two things that unblock everything: written confirmation of the structure, "
         "and sandbox access. Replace the bracketed contact details before sending — they are intentionally "
         "left as placeholders.")

# =====================================================================
# 17 · APPENDIX
# =====================================================================
s = slide(prs)
y = header(s, "Appendix", "What we can provide during due diligence",
           lead="We expect underwriting. Here is the pack, ready on request under NDA.")
pack = [("Corporate", ["Certificate of formation and good standing",
                       "Operating agreement and ownership chart",
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

ty2 = y + 0.1 + ph + 0.38
text(s, ML, ty2, CW, 0.4,
     "Open item we will address first: the processing history sits with our operating entity; KD PAY LLC is new. "
     "We will provide continuity evidence and references so the underwriting risk is clear, not hidden.",
     size=9.8, color=MUTED, spacing=1.25)

by2 = 5.15
rect(s, ML, by2, CW, 1.05, fill=INK, radius=0.05)
text(s, ML + 0.35, by2 + 0.2, 4.0, 0.24, "WHAT WE NEED FROM YOU", size=9, color=ACCENT,
     bold=True, tracking=1.3)
for i, item in enumerate(["Pricing sheet and reserve terms at our volume",
                          "Capability and corridor matrix, today and roadmap",
                          "Draft term sheet, SLA and settlement timetable"]):
    text(s, ML + 0.35 + i * ((CW - 0.7) / 3), by2 + 0.55, (CW - 0.7) / 3 - 0.3, 0.42, item,
         size=9.8, color=WHITE, spacing=1.15)
footer(s, 17, label=LABEL)
notes(s, "Ending on the entity issue is deliberate: it is the one thing underwriting will find, so we frame it "
         "before they do. Say we would rather over-share than have it surface late in the process.")

# ---------- document properties ----------
cp = prs.core_properties
cp.title = "KD PAY LLC — white-label partnership proposal for Airwallex"
cp.subject = "Operating the merchant-facing layer for Asia on Airwallex rails"
cp.author = "KD PAY LLC"
cp.last_modified_by = "KD PAY LLC"
cp.category = "Partnership proposal"
cp.keywords = "Airwallex, white-label, merchant of record, Asia, cross-border payments"
cp.comments = ("17-slide business-model deck. Figures supplied by KD PAY: $800K monthly volume, 0.01% "
               "chargeback ratio, operating since 2022. See deck/SOURCES.md for the basis of every claim.")

out = os.path.join(os.path.dirname(__file__), "KD-PAY-Airwallex-White-Label-Proposal.pptx")
prs.save(out)
print("saved", out, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
