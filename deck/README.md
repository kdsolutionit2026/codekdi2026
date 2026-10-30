# KD PAY × Airwallex — partnership deck

`KD-PAY-Airwallex-Partnership.pptx` — 18 slides, 16:9, Arial, speaker notes on every slide.

| File | What it is |
|---|---|
| `KD-PAY-Airwallex-Partnership.pptx` | The deliverable. Open in PowerPoint / Keynote / Google Slides. |
| `SPEAKER-NOTES.md` | The same notes, readable outside PowerPoint. |
| `SOURCES.md` | Where every figure and claim comes from, plus what we deliberately do *not* claim. |
| `build.py` | Generates the deck from scratch (python-pptx). |
| `lib.py` | Layout toolkit: palette, type scale, `header()`, `card()`, `table()`, text metrics. |
| `render.py` | Approximate PPTX → PNG renderer used to check geometry without LibreOffice. |
| `audit.py` | Static check for off-slide shapes and text taller than its box. |

## Rebuild

```bash
python3 -m venv /tmp/pptenv && /tmp/pptenv/bin/pip install python-pptx pillow
cd deck
/tmp/pptenv/bin/python build.py                            # writes the .pptx
/tmp/pptenv/bin/python render.py KD-PAY-Airwallex-Partnership.pptx /tmp/preview   # all slides
/tmp/pptenv/bin/python render.py KD-PAY-Airwallex-Partnership.pptx /tmp/preview 4,7,11
/tmp/pptenv/bin/python audit.py KD-PAY-Airwallex-Partnership.pptx
```

`render.py` uses DejaVu at 0.88× the point size as a stand-in for Arial and flags any text box whose
content looks taller than the box. Red outlines in a preview are warnings, not errors — PowerPoint
re-wraps text to the real box, so check the flagged box on the slide before changing anything.

## Before sending

1. Replace the placeholders on slide 16: `[name] · [title] · [email] · [phone]`.
2. Re-read `SOURCES.md` section D — the 8-week timeline and the corridor sequence are *our* assumptions.
3. Confirm the date on slide 1 if the meeting moves.

## Narrative order

Ask → who we are → today's business → the Asia gap → corridors → Phase 1 product → architecture
(SAQ-A) → why Airwallex → partnership model (seller ledger vs connected accounts) → risk → security →
compliance → 8-week plan → 12-month outlook → four decisions → appendices (integration detail;
due-diligence pack).

Slides 1, 10 and 16 are dark; the rest are light, so a projector with poor contrast still reads.
