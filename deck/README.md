# KD PAY × Airwallex — partnership decks

**Present this one:** `KD-PAY-Airwallex-White-Label-Proposal.pptx` — 17 slides, business model first.
`KD-PAY-Airwallex-Partnership.pptx` is the earlier product-focused version (18 slides), kept for reference.

| File | What it is |
|---|---|
| `KD-PAY-Airwallex-White-Label-Proposal.pptx` | **The deliverable.** White-label / MOR proposal, 17 slides, speaker notes on every slide. |
| `KD-PAY-Airwallex-Partnership.pptx` | Earlier product-focused deck (18 slides). Internal reference only. |
| `SPEAKER-NOTES.md` | Notes for the white-label deck, readable outside PowerPoint. |
| `SOURCES.md` | Where every figure and claim comes from, plus what we deliberately do *not* claim. |
| `preview-white-label.jpg` | Contact sheet of the 17 white-label slides. |
| `preview.jpg` | Contact sheet of the earlier 18-slide deck. |
| `build_whitelabel.py` | Generates the white-label deck. |
| `build.py` | Generates the earlier product deck (`build_product_focus.py` is a copy of the same). |
| `lib.py` | Layout toolkit: palette, type scale, `header()`, `card()`, `table()`, text metrics. |
| `render.py` | Approximate PPTX → PNG renderer used to check geometry without LibreOffice. |
| `audit.py` | Static check for off-slide shapes and text taller than its box. |

## White-label deck — narrative order

Proposition (you own the rails, we own the merchant) → the ask → who we are → the Asia gap → corridor
sequence → revenue model → what white-label actually means → three contract structures (A/B/C) →
distribution → economics → risk and reserves → eight security commitments → why us → 12-month outlook
→ four decisions → due-diligence pack.

Slides 1 and 16 are dark; the rest are light, so it still reads on a weak projector.

## Rebuild

```bash
python3 -m venv /tmp/pptenv && /tmp/pptenv/bin/pip install python-pptx pillow
cd deck
/tmp/pptenv/bin/python build_whitelabel.py        # white-label deck
/tmp/pptenv/bin/python build.py                   # earlier product deck
/tmp/pptenv/bin/python render.py KD-PAY-Airwallex-White-Label-Proposal.pptx /tmp/preview
/tmp/pptenv/bin/python render.py KD-PAY-Airwallex-White-Label-Proposal.pptx /tmp/preview 9,11,13
/tmp/pptenv/bin/python audit.py KD-PAY-Airwallex-White-Label-Proposal.pptx
```

`render.py` uses DejaVu at 0.88× the point size as a stand-in for Arial and outlines any text box whose
content looks taller than the box. Red outlines in a preview are warnings, not errors — PowerPoint re-wraps
text to the real box, so check the flagged box on the slide before changing anything.

## Before sending

1. Replace the placeholders on slide 16: `[name] · [title] · [email] · [phone]`.
2. Re-read `SOURCES.md` sections D and E — the 8-week timeline, the take-rate scenarios and structures
   A/B/C are *our* proposals, not agreed terms.
3. Confirm the date on slide 1 if the meeting moves.
