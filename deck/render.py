"""Approximate renderer: draws each slide's shapes from the PPTX to PNG so layout can be checked
without LibreOffice. Text metrics use DejaVu as a stand-in for Arial (slightly wider, so overflow
shown here is a conservative warning)."""
import sys, os
from pptx import Presentation
from pptx.util import Emu
from PIL import Image, ImageDraw, ImageFont
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

DPI = 120
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_cache = {}

def font(size_pt, bold):
    key = (round(size_pt, 1), bold)
    if key not in _cache:
        # DejaVu runs ~14% wider than Arial; scale so previews approximate real PowerPoint metrics
        px_size = max(6, int(round(size_pt * DPI / 72 * 0.88)))
        _cache[key] = ImageFont.truetype(BOLD if bold else REG, px_size)
    return _cache[key]

def emu_in(v):
    return v / 914400.0

def px(v):
    return int(round(emu_in(v) * DPI))

def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def rgb(color_obj, default=(0, 0, 0)):
    try:
        c = color_obj.rgb
        return (c[0], c[1], c[2])
    except Exception:
        return default

def _draw_line(d, tokens, x, y, align, maxw):
    txt = "".join(t[0] for t in tokens).rstrip()
    if not txt:
        return
    fnt = tokens[0][1]
    tw = d.textlength(txt, font=fnt)
    tx = x
    if align == PP_ALIGN.CENTER:
        tx = x + (maxw - tw) / 2
    elif align == PP_ALIGN.RIGHT:
        tx = x + maxw - tw
    # draw contiguous spans of the same colour *and* font, advancing with that font
    spans = []
    for tok, f, colr in tokens:
        if spans and spans[-1][0] == colr and spans[-1][1] is f:
            spans[-1][2] += tok
        else:
            spans.append([colr, f, tok])
    cx = tx
    for colr, f, txt_span in spans:
        d.text((cx, y), txt_span, font=f, fill=colr)
        cx += d.textlength(txt_span, font=f)


def render(path, outdir, pages=None):
    prs = Presentation(path)
    W, H = px(prs.slide_width), px(prs.slide_height)
    os.makedirs(outdir, exist_ok=True)
    outs = []
    for i, s in enumerate(prs.slides, 1):
        if pages and i not in pages:
            continue
        img = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(img)
        # background
        try:
            fill = s.background.fill
            if fill.type is not None and fill.fore_color.type is not None:
                img.paste(Image.new("RGB", (W, H), rgb(fill.fore_color)), (0, 0))
                d = ImageDraw.Draw(img)
        except Exception:
            pass
        for sh in s.shapes:
            kind = sh.shape_type
            name = str(kind)
            # connectors
            if "CONNECTOR" in name or sh.__class__.__name__ == "Connector":
                x1, y1 = px(sh.left), px(sh.top)
                x2, y2 = px(sh.left + sh.width), px(sh.top + sh.height)
                col = (200, 200, 200)
                try:
                    col = rgb(sh.line.color, (200, 200, 200))
                except Exception:
                    pass
                wd = 1
                try:
                    wd = max(1, int(sh.line.width.pt * DPI / 72))
                except Exception:
                    pass
                d.line([x1, y1, x2, y2], fill=col, width=wd)
                continue
            # shapes with fill
            try:
                if sh.fill.type is not None and sh.fill.type != 5:
                    col = rgb(sh.fill.fore_color, (255, 255, 255))
                    x, y, w, h = px(sh.left), px(sh.top), px(sh.width), px(sh.height)
                    ln = None
                    try:
                        if sh.line.color and sh.line.color.type is not None:
                            ln = rgb(sh.line.color, None)
                    except Exception:
                        ln = None
                    rounded = "ROUNDED" in str(getattr(sh, "auto_shape_type", ""))
                    if rounded:
                        d.rounded_rectangle([x, y, x + w, y + h], radius=int(min(w, h) * 0.12),
                                            fill=col, outline=ln, width=1 if ln else 0)
                    else:
                        d.rectangle([x, y, x + w, y + h], fill=col, outline=ln, width=1 if ln else 0)
            except Exception:
                pass
            # text
            if not sh.has_text_frame:
                continue
            tf = sh.text_frame
            txt = tf.text.strip()
            if not txt:
                continue
            x, y, w, h = px(sh.left), px(sh.top), px(sh.width), px(sh.height)
            ml = px(tf.margin_left) if tf.margin_left is not None else 0
            mt = px(tf.margin_top) if tf.margin_top is not None else 0
            mr = px(tf.margin_right) if tf.margin_right is not None else 0
            blocks = []
            total_h = 0
            for p in tf.paragraphs:
                runs = []
                for r in p.runs:
                    if r.text:
                        f0 = r.font
                        size = f0.size.pt if f0.size else 14
                        bold = bool(f0.bold)
                        colr = rgb(f0.color, (0, 0, 0)) if f0.color and f0.color.type is not None else (0, 0, 0)
                        runs.append((r.text, size, bold, colr))
                if not runs:
                    blocks.append(([], 12, 0)); total_h += 12; continue
                size = runs[0][1]
                ls = p.line_spacing if isinstance(p.line_spacing, float) else 1.15
                lh = int(round(size * DPI / 72 * 1.2 * ls))
                blocks.append((runs, lh, p.alignment))
                total_h += lh
                total_h += int(p.space_after.pt * DPI / 72) if p.space_after else 0
            anchor = tf.vertical_anchor
            cy = y + mt
            if anchor == MSO_ANCHOR.MIDDLE:
                cy = y + (h - total_h) // 2
            elif anchor == MSO_ANCHOR.BOTTOM:
                cy = y + h - total_h - mt
            for b in blocks:
                if not b[0]:
                    cy += b[1]; continue
                runs, lh, align = b
                maxw = w - ml - mr
                # tokenise into words, preserving per-run font/colour
                tokens = []
                for txt, size, bold, colr in runs:
                    fnt = font(size, bold)
                    for wi, word in enumerate(txt.split(" ")):
                        if wi:
                            tokens.append((" ", fnt, colr))
                        if word:
                            tokens.append((word, fnt, colr))
                line, cur_w = [], 0.0
                for tok, fnt, colr in tokens:
                    tw = d.textlength(tok, font=fnt)
                    if tok != " " and cur_w + tw > maxw and line:
                        _draw_line(d, line, x + ml, cy, align, maxw)
                        cy += lh
                        line, cur_w = [], 0.0
                    line.append((tok, fnt, colr)); cur_w += tw
                if line:
                    _draw_line(d, line, x + ml, cy, align, maxw)
                    cy += lh
            # overflow warning marker
            if total_h + mt > h + 8:
                d.rectangle([x - 2, y - 2, x + w + 2, y + h + 2], outline=(255, 0, 90), width=2)
        p = os.path.join(outdir, f"slide-{i:02d}.png")
        img.save(p)
        outs.append(p)
    return outs

if __name__ == "__main__":
    src = sys.argv[1]; out = sys.argv[2]
    pages = set(int(x) for x in sys.argv[3].split(",")) if len(sys.argv) > 3 else None
    for p in render(src, out, pages):
        print(p)
