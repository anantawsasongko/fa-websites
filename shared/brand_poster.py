# -*- coding: utf-8 -*-
"""Poster share gaya FA (1 Nov 2026): foto latar + gradasi brand, paduan font FA: judul Times (Liberation Serif), teks Source Sans 3.
Dipakai poster.py (og artikel FA/CariAkuntan) dan updatesak/build_seo.py (og + story UpdateSAK). Sama dengan desain canvas di share.js."""
import os, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "updatesak", "fonts")
BG = os.path.join(HERE, "share-bg")
BR = {"fa": dict(l="F", dom="faindonesia.co.id", c2=(127, 29, 29), ac=(252, 165, 165), tag="Kredit Bank, Investor, IPO"),
      "ca": dict(l="C", dom="cariakuntan.com", c2=(31, 91, 255), ac=(143, 178, 255), tag="KAP, KJPP, Pajak, Laporan Keuangan"),
      "us": dict(l="U", dom="updatesak.com", c2=(14, 124, 102), ac=(126, 224, 195), tag="Kalkulator PSAK dan CALK")}
def F(name, s): return ImageFont.truetype(os.path.join(FONTS, name), s)
def _photo(key, W, H):
    fs = sorted(f for f in os.listdir(BG) if f.endswith(".jpg"))
    i = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(fs)
    ph = Image.open(os.path.join(BG, fs[i])).convert("RGB")
    sc = max(W / ph.width, H / ph.height); ph = ph.resize((int(ph.width * sc) + 1, int(ph.height * sc) + 1))
    x0 = (ph.width - W) // 2; y0 = int((ph.height - H) * .35)
    return ph.crop((x0, y0, x0 + W, y0 + H))
def _wrap(dr, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if dr.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines
def _base(brand, key, W, H, photo_box, fade):
    import numpy as np
    b = BR[brand]
    yy, xx = np.mgrid[0:H, 0:W].astype("float32")
    d = np.sqrt((xx / W) ** 2 + ((H - yy) / H) ** 2) / 1.25
    d = np.clip(d / .62, 0, 1)[..., None]
    c2 = np.array(b["c2"], "float32"); c0 = np.array([7, 7, 7], "float32")
    im = Image.fromarray((c2 + (c0 - c2) * d).astype("uint8"), "RGB")
    px, py, pw, ph = photo_box
    p = _photo(key, pw, ph)
    tint = Image.new("RGB", (pw, ph), tuple(int(v * .5) for v in b["c2"]))
    p = Image.blend(p, tint, .28)
    p = Image.blend(p, Image.new("RGB", (pw, ph), (0, 0, 0)), .30)
    m = np.ones((ph, pw), "float32")
    if fade == "down":
        y = np.linspace(0, 1, ph)[:, None]; m = np.clip((1 - y) / .55, 0, 1) * .95 * np.ones((1, pw))
    else:
        x = np.linspace(0, 1, pw)[None, :]; m = np.clip(x / .45, 0, 1) * .95 * np.ones((ph, 1))
    im.paste(p, (px, py), Image.fromarray((m * 255).astype("uint8"), "L"))
    return im, b
def _logo(dr, b, m, s=1.0):
    w, h = int(54 * s), int(72 * s)
    dr.rectangle([m, m, m + w, m + h], outline="white", width=max(2, int(3 * s)))
    dr.text((m + int(9 * s), m + int(8 * s)), b["l"], font=F("SourceSans3-300.woff", int(22 * s)), fill="white")
    dr.line([(m + int(30 * s), m + int(62 * s)), (m + int(37 * s), m + int(44 * s)), (m + int(44 * s), m + int(62 * s))], fill="white", width=max(2, int(2.5 * s)))
    dr.text((m + int(80 * s), m + h // 2), b["dom"], font=F("SourceSans3-400.woff", int(40 * s)), fill="white", anchor="lm")
def story(brand, kicker, title, url, out):
    W, H = 1080, 1920
    im, b = _base(brand, url or title, W, H, (0, 0, W, 1180), "down")
    dr = ImageDraw.Draw(im); m = 96
    top = Image.new("L", (W, 260)); 
    _logo(dr, b, m)
    size = 88
    while True:
        f = F("LiberationSerif-Regular.ttf", size); lines = _wrap(dr, title, f, W - 2 * m)
        if len(lines) <= 6 or size <= 52: break
        size -= 4
    lh = int(size * 1.18); y = H - 420 - len(lines) * lh
    if kicker: dr.text((m, y - 70), kicker.upper()[:44], font=F("SourceSans3-600.woff", 34), fill=b["ac"])
    for ln in lines: dr.text((m, y), ln, font=f, fill="white"); y += lh
    dr.rectangle([m, y + 26, m + 84, y + 32], fill=b["ac"])
    dr.text((m, H - 300), b["tag"], font=F("SourceSans3-300.woff", 34), fill=(225, 225, 225), anchor="lm")
    bx, by, bw, bh = m, H - 236, W - 2 * m, 112
    dr.rounded_rectangle([bx, by, bx + bw, by + bh], radius=56, fill="white")
    u = (url or b["dom"]).replace("https://", "").replace("http://", "")
    fnt = F("SourceSans3-600.woff", 36)
    if dr.textlength("Baca: " + u, font=fnt) > bw - 90: u = b["dom"]
    dr.text((W // 2, by + bh // 2), "Baca: " + u, font=fnt, fill=(10, 10, 10), anchor="mm")
    os.makedirs(os.path.dirname(out), exist_ok=True); im.save(out, "JPEG", quality=84, optimize=True, progressive=True)
def og(brand, kicker, title, url, out):
    W, H = 1200, 630
    im, b = _base(brand, url or title, W, H, (560, 0, 640, H), "right")
    dr = ImageDraw.Draw(im); m = 64
    _logo(dr, b, m, .7)
    maxw = 680; size = 56
    while True:
        f = F("LiberationSerif-Regular.ttf", size); lines = _wrap(dr, title, f, maxw)
        if len(lines) <= 4 or size <= 34: break
        size -= 3
    y = 200
    if kicker: dr.text((m, y - 50), kicker.upper()[:40], font=F("SourceSans3-600.woff", 22), fill=b["ac"])
    for ln in lines[:5]: dr.text((m, y), ln, font=f, fill="white"); y += int(size * 1.2)
    dr.rectangle([m, y + 18, m + 64, y + 23], fill=b["ac"])
    dr.text((m, H - m - 10), b["tag"], font=F("SourceSans3-300.woff", 24), fill=(225, 225, 225), anchor="ls")
    os.makedirs(os.path.dirname(out), exist_ok=True); im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
