# Gambar og:image per artikel (1200x630) untuk FA Indonesia dan CariAkuntan, supaya kartu share
# LinkedIn, Threads, WhatsApp, dan Facebook menampilkan poster judul artikel, bukan logo generik.
# Cache di shared/og/<brand>/ (nama = slug + hash judul), disalin ke out/<site>/img/og-art/. Dipanggil prep.py.
import os, re, html, hashlib, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "updatesak", "fonts")
BR = {"fa": dict(l1="F", dom="faindonesia.co.id", c0=(10, 10, 10), c1=(127, 29, 29), ac="#fca5a5", dot=(70, 40, 40), tag="Kredit Bank, Investor, IPO"),
      "ca": dict(l1="C", dom="cariakuntan.com", c0=(11, 31, 51), c1=(31, 91, 255), ac="#8FB2FF", dot=(70, 110, 200), tag="KAP, KJPP, Pajak, Laporan Keuangan")}


def _img(brand, kicker, title, out):
    import brand_poster as _bp  # desain foto + gradasi, Lora + Poppins (1 Nov 2026)
    _bp.og(brand, kicker, title, out, out)


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
        h = hashlib.md5(("v4" + brand + kicker + title).encode()).hexdigest()[:6]
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


def _share_assets(root):
    """Font brand (Lora, Poppins) dan foto latar poster share (1 Nov 2026)."""
    fd = os.path.join(root, "js", "fonts"); os.makedirs(fd, exist_ok=True)
    for f in ("LiberationSerif-Regular.ttf", "SourceSans3-300.woff2", "SourceSans3-400.woff2", "SourceSans3-600.woff2"):
        shutil.copy2(os.path.join(FONTS, f), os.path.join(fd, f))
    bd = os.path.join(root, "js", "share-bg"); os.makedirs(bd, exist_ok=True)
    sb = os.path.join(HERE, "share-bg")
    for f in os.listdir(sb): shutil.copy2(os.path.join(sb, f), os.path.join(bd, f))


def add_share_js(root, src):
    os.makedirs(os.path.join(root, "js"), exist_ok=True); _share_assets(root)
    shutil.copy2(src, os.path.join(root, "js", "share.js")) if os.path.isdir(os.path.join(root, "js")) else (os.makedirs(os.path.join(root, "js")), shutil.copy2(src, os.path.join(root, "js", "share.js")))
    v = hashlib.md5(open(src, "rb").read()).hexdigest()[:8]
    n = 0
    for d, _, fs in os.walk(root):
        if "index.html" not in fs: continue
        p = os.path.join(d, "index.html"); t = open(p, encoding="utf-8").read()
        if not (re.search(r'"@type"\s*:\s*"(Article|NewsArticle|BlogPosting)"', t) or 'class="share"' in t): continue
        t = re.sub(r'<script src="/js/share\.js[^"]*" defer></script>', "", t)
        t = t.replace("</body>", f'<script src="/js/share.js?v={v}" defer></script></body>', 1)
        open(p, "w", encoding="utf-8").write(t); n += 1
    return n
