# -*- coding: utf-8 -*-
"""Logo A (gaya McKinsey) Cari Akuntan dan UpdateSAK, dipilih Bos 1 Nov 2026.
Teks dikonversi jadi path (tidak bergantung font browser). Output: svg di folder ini."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "updatesak", "fonts")
SER = TTFont(os.path.join(F, "LiberationSerif-Regular.ttf"))
SS6 = TTFont(os.path.join(F, "SourceSans3-600.woff"))
def run(font, text, size, x, y, ls=0.0):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font["head"].unitsPerEm; sc = size / upm
    pen = SVGPathPen(gs); cx = x
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None: cx += size * .3; continue
        tp = TransformPen(pen, (sc, 0, 0, -sc, cx, y)); gs[g].draw(tp)
        cx += gs[g].width * sc + ls
    return pen.getCommands(), cx
def build(word1, word2, w2font, w2size, desc, accent, desc_col, word_col="currentColor", w2col=None):
    # wordmark baris 1, aksen garis + deskriptor baris 2
    d1, x1 = run(SER, word1, 46, 0, 46)
    parts = [f'<path d="{d1}" fill="{word_col}"/>']
    xe = x1
    if word2:
        d2, xe = run(w2font, word2, w2size, x1 + 10, 46, 2)
        parts.append(f'<path d="{d2}" fill="{w2col or accent}"/>')
    return parts, xe
def svg(parts, w, h, extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h}" width="{w:.0f}" height="{h}">{"".join(parts)}{extra}</svg>'
def lockup(brand, mode):
    dark = mode == "dark"
    if brand == "ca":
        ac = "#8FB2FF" if dark else "#1F5BFF"; wc = "#ffffff" if dark else "#0B1F33"; dc = "#aab7c6" if dark else "#5b6b7c"
        parts, xe = build("Cari Akuntan", None, None, 0, "", ac, dc, wc); desc = "KAP · KJA · PAJAK · KJPP"
    else:
        ac = "#7EE0C3" if dark else "#0E7C66"; wc = "#ffffff" if dark else "#0E2A24"; dc = "#a9bdb7" if dark else "#5c716b"
        parts, xe = build("Update", "SAK", SS6, 36, "", ac, dc, wc); desc = "PSAK · SAK EP · SAK EMKM"
    dd, dx = run(SS6, desc, 11.5, 44, 70, 3)
    parts += [f'<rect x="0" y="62" width="34" height="3" fill="{ac}"/>', f'<path d="{dd}" fill="{dc}"/>']
    return svg(parts, max(xe, dx) + 2, 74)
def header(brand):
    # versi header: wordmark + garis aksen, tanpa deskriptor; warna teks ikut currentColor
    if brand == "ca":
        parts, xe = build("Cari Akuntan", None, None, 0, "", "#1F5BFF", "", "currentColor"); ac = "#1F5BFF"
    else:
        parts, xe = build("Update", "SAK", SS6, 36, "", "#0E7C66", "", "currentColor"); ac = "#0E7C66"
    parts.append(f'<rect x="1" y="57" width="30" height="3" fill="{ac}"/>')
    return svg(parts, xe + 2, 60)
def icon(brand, bg=None):
    # favicon / ikon: inisial serif + garis aksen
    txt, ac, fg, bgc = ("CA", "#8FB2FF", "#ffffff", "#0B1F33") if brand == "ca" else ("US", "#7EE0C3", "#ffffff", "#0E5C4C")
    bg = bgc
    d, xe = run(SER, txt, 34, 0, 0)
    w = xe; dx = (64 - w) / 2
    d, _ = run(SER, txt, 34, dx, 40)
    bgr = f'<rect width="64" height="64" rx="12" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">{bgr}<path d="{d}" fill="{fg}"/><rect x="{dx:.1f}" y="46" width="{w:.1f}" height="3.5" fill="{ac}"/></svg>'
if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    for b in ("ca", "us"):
        for m in ("light", "dark"): open(os.path.join(out, f"{b}-lockup-{m}.svg"), "w").write(lockup(b, m))
        open(os.path.join(out, f"{b}-header.svg"), "w").write(header(b))
        open(os.path.join(out, f"{b}-icon.svg"), "w").write(icon(b, "#ffffff"))
    print("ok")
