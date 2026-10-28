# Gambar og:image per artikel (1200x630) untuk FA Indonesia dan CariAkuntan, supaya kartu share
# LinkedIn, Threads, WhatsApp, dan Facebook menampilkan poster judul artikel, bukan logo generik.
# Cache di shared/og/<brand>/ (nama = slug + hash judul), disalin ke out/<site>/img/og-art/. Dipanggil prep.py.
import os, re, html, hashlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "updatesak", "fonts")
BR = {"fa": dict(l1="F", dom="faindonesia.co.id", c0=(10, 10, 10), c1=(127, 29, 29), ac="#fca5a5", dot=(70, 40, 40), tag="Kredit Bank, Investor, IPO"),
      "ca": dict(l1="C", dom="cariakuntan.com", c0=(11, 31, 51), c1=(31, 91, 255), ac="#8FB2FF", dot=(70, 110, 200), tag="KAP, KJPP, Pajak, Laporan Keuangan")}


def _img(brand, kicker, title, out):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    b = BR[brand]; W, H = 1200, 630
    serif = lambda s: ImageFont.truetype(os.path.join(FONTS, "SourceSerif4-Semibold.ttf"), s)
    sans = lambda s, bold=True: ImageFont.truetype(os.path.join(FONTS, "IBMPlexSans-SemiBold.ttf" if bold else "IBMPlexSans-Regular.ttf"), s)
    yy, xx = np.mgrid[0:H, 0:W]
    t = (xx / W * .55 + yy / H * .45)[..., None]
    a0, a1 = np.array(b["c0"]), np.array(b["c1"])
    im = Image.fromarray((a0 + (a1 - a0) * t).astype("uint8"), "RGB")
    dr = ImageDraw.Draw(im)
    for gx in range(0, W, 26):
        for gy in range(0, H, 26):
            dr.point((gx, gy), fill=b["dot"])
    m = 70
    dr.rectangle([m, m, m + 40, m + 54], outline="white", width=3)
    dr.text((m + 11, m + 15), b["l1"], font=sans(16, False), fill="white", anchor="mm")
    dr.line([(m + 23, m + 45), (m + 28, m + 33), (m + 33, m + 45)], fill="white", width=2)
    dr.text((m + 60, m + 27), b["dom"], font=sans(30), fill="white", anchor="lm")
    ky = m + 120
    if kicker: dr.text((m, ky), kicker.upper()[:48], font=sans(24), fill=b["ac"])
    size, maxw = 56, W - 2 * m
    while True:
        lines, cur = [], ""
        for w in title.split():
            tt = (cur + " " + w).strip()
            if dr.textlength(tt, font=serif(size)) <= maxw: cur = tt
            else: lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) <= 4 or size < 32: break
        size -= 4
    y = ky + 50
    for ln in lines[:5]:
        dr.text((m, y), ln, font=serif(size), fill="white"); y += int(size * 1.18)
    dr.rectangle([m, H - m - 52, m + 70, H - m - 46], fill=b["ac"])
    dr.text((m, H - m - 30), b["tag"], font=sans(24, False), fill="#e5e7eb")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, "JPEG", quality=78, optimize=True, progressive=True)


def apply(root, brand, base):
    cache = os.path.join(HERE, "og", brand); os.makedirs(cache, exist_ok=True)
    dst = os.path.join(root, "img", "og-art"); os.makedirs(dst, exist_ok=True)
    adir = os.path.join(root, "artikel"); n = 0; keep = set()
    for slug in sorted(os.listdir(adir)):
        p = os.path.join(adir, slug, "index.html")
        if not os.path.exists(p): continue
        t = open(p, encoding="utf-8").read()
        if not re.search(r'"@type"\s*:\s*"(Article|NewsArticle|BlogPosting)"', t): continue
        m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else slug
        k = re.search(r'class="eyebrow"><a[^>]*>Eksplor · ([^<]+)<', t) or re.search(r'<p class="label"[^>]*>([^<]{2,40})</p>', t)
        kicker = html.unescape(k.group(1)).strip() if k else ""
        h = hashlib.md5(("v2" + brand + kicker + title).encode()).hexdigest()[:6]
        c = os.path.join(cache, f"{slug}-{h}.jpg"); keep.add(os.path.basename(c))
        if not os.path.exists(c):
            try: _img(brand, kicker, title, c)
            except Exception as e: print("og gagal", slug, e); continue
        shutil.copy2(c, os.path.join(dst, slug + ".jpg"))
        url = f"{base}/img/og-art/{slug}.jpg"
        tags = (f'<meta property="og:image" content="{url}"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/>'
                f'<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:image" content="{url}"/>')
        t = re.sub(r'<meta (content="[^"]*" )?property="og:image(:width|:height)?"( content="[^"]*")?\s*/?>\s*', "", t)
        t = re.sub(r'<meta (content="[^"]*" )?name="twitter:(card|image)"( content="[^"]*")?\s*/?>\s*', "", t)
        t = t.replace("</head>", tags + "\n</head>", 1)
        open(p, "w", encoding="utf-8").write(t); n += 1
    for f in os.listdir(cache):
        if f not in keep: os.remove(os.path.join(cache, f))
    return n


def add_share_js(root, src):
    shutil.copy2(src, os.path.join(root, "js", "share.js")) if os.path.isdir(os.path.join(root, "js")) else (os.makedirs(os.path.join(root, "js")), shutil.copy2(src, os.path.join(root, "js", "share.js")))
    v = hashlib.md5(open(src, "rb").read()).hexdigest()[:8]
    n = 0
    for d, _, fs in os.walk(root):
        if "index.html" not in fs: continue
        p = os.path.join(d, "index.html"); t = open(p, encoding="utf-8").read()
        if not re.search(r'"@type"\s*:\s*"(Article|NewsArticle|BlogPosting)"', t): continue
        t = re.sub(r'<script src="/js/share\.js[^"]*" defer></script>', "", t)
        t = t.replace("</body>", f'<script src="/js/share.js?v={v}" defer></script></body>', 1)
        open(p, "w", encoding="utf-8").write(t); n += 1
    return n
