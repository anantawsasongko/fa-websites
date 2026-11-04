# -*- coding: utf-8 -*-
"""Semua halaman bisa dibagikan ke sosmed (4 Nov 2026, keluhan Bos: kalkulator valuasi RS dan halaman lain belum bisa di-share).
1. og:image: halaman yang belum punya poster mendapat poster brand (foto + gradasi, judul halaman).
   Halaman tunggal = poster sendiri. Halaman massal (wilayah, kota, kdmp, konsultan RS per kota) = satu poster per bagian.
2. Tombol share (IG Story, Threads, LinkedIn, X, WA, Salin Link) dari shared/share.js:
   baris tombol di bawah H1 semua halaman yang belum punya; alat/kalkulator juga mendapat blok ajakan di bawah.
Dipanggil prep.py setelah tool_share, sebelum add_share_js. Idempoten."""
import os, re, html, hashlib, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SKIP = re.compile(r"^((en|zh|ja|ko|hokkien|bayar|ai-admin|toko/uji|404|js|img|files|css)(/|$)|kebijakan-|syarat-)")
TOOL = re.compile(r"^(kalkulator-|cek-|simulasi-|bankability-index|screening)")
BASE = {"faindonesia": ("fa", "https://faindonesia.co.id"), "cariakuntan": ("ca", "https://cariakuntan.com"), "updatesak": ("us", "https://updatesak.com")}
# bagian massal: satu poster per bagian (kicker, judul)
SECTION = {
    "fa": {"wilayah": ("FA Indonesia per Kota", "Laporan Keuangan, Audit, dan Kredit Bank di Kota Anda"),
           "konsultan-rumah-sakit": ("Konsultan Rumah Sakit", "Kredit Bank, Investor, dan Unit Cost untuk Rumah Sakit Swasta"),
           "konsultan-unit-cost-rumah-sakit": ("Unit Cost Rumah Sakit", "Hitung Unit Cost dan Tarif Rumah Sakit Swasta")},
    "ca": {"kota": ("Cari Akuntan per Kota", "KAP, KJPP, Konsultan Pajak, dan Jasa Laporan Keuangan di Kota Anda"),
           "kdmp": ("Koperasi Desa Merah Putih", "Laporan Keuangan dan Audit KDMP di Seluruh Kecamatan"),
           "layanan": ("Cari Akuntan", "KAP, KJPP, Konsultan Pajak, dan Jasa Laporan Keuangan")},
    "us": {"standar-audit": ("UpdateSAK", "Standar Audit (SA) Terbaru dan Ringkasannya"),
           "psak": ("UpdateSAK", "PSAK yang Berlaku dan Ringkasannya")},
}
CSS = ('<style id="tshare-css">.tshare{max-width:1080px;margin:36px auto 8px;padding:22px 20px;border:1px solid rgba(127,127,127,.25);'
       'border-radius:14px;text-align:center}.tshare h3{margin:0 0 4px;font-size:1.15rem}.tshare p{margin:0 0 6px;opacity:.75;font-size:.95rem}'
       '.tshare .fxs{justify-content:center;margin:10px 0 0}.tshare-top .fxs{margin:14px 0 6px}@media(max-width:720px){.tshare{margin:28px 16px 8px}}</style>')


def _txt(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip().replace('"', "'")


def _poster(brand, kicker, title, key, root):
    import brand_poster as bp
    pb = brand if brand in ("fa", "ca") else "ca"
    cache = os.path.join(HERE, "og", "page-" + brand); os.makedirs(cache, exist_ok=True)
    h = hashlib.md5(("p1" + brand + kicker + title).encode()).hexdigest()[:6]
    c = os.path.join(cache, f"{key}-{h}.jpg")
    if not os.path.exists(c):
        for f in os.listdir(cache):
            if f.startswith(key + "-"): os.remove(os.path.join(cache, f))
        bp.og(pb, kicker, title, None, c)
    d = os.path.join(root, "img", "og-page"); os.makedirs(d, exist_ok=True)
    shutil.copy2(c, os.path.join(d, key + ".jpg"))
    return "/img/og-page/" + key + ".jpg"


def run(OUT):
    res = {}
    for site, (brand, base) in BASE.items():
        root = os.path.join(OUT, site); og = sh = 0; done = {}
        for d, _, fs in os.walk(root):
            if "index.html" not in fs: continue
            rel = os.path.relpath(d, root).replace(os.sep, "/"); rel = "" if rel == "." else rel
            if rel and SKIP.match(rel): continue
            p = os.path.join(d, "index.html"); t = open(p, encoding="utf-8").read()
            if 'http-equiv="refresh"' in t or "</head>" not in t: continue
            m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
            h1 = _txt(m.group(1)) if m else _txt((re.search(r"<title>(.*?)</title>", t, re.S) or [None, ""])[1]).split(" | ")[0]
            top = rel.split("/")[0] if rel else ""
            article = re.search(r'"@type"\s*:\s*"(Article|NewsArticle|BlogPosting)"', t) is not None
            ch = False
            # 1. og:image
            GEN = ("ananta-w-sasongko-cpa-og.jpg", "fa-indonesia-og.jpg")
            if any(g in t for g in GEN) and 'property="og:image"' in t and rel != "ananta-w-sasongko":
                t = re.sub(r'<meta[^>]*property="og:image(:width|:height|:alt|:type)?"[^>]*>\s*', "", t)
            if 'property="og:image"' not in t and h1:
                sec = SECTION.get(brand, {}).get(top) if rel.count("/") >= 1 or top in ("kota", "kdmp", "wilayah") else None
                if sec:
                    key = "sec-" + top
                    if key not in done: done[key] = _poster(brand, sec[0], sec[1], key, root)
                    img = done[key]
                else:
                    k = re.search(r'class="(?:eyebrow|label|kick)[^"]*"[^>]*>(.*?)</', t, re.S)
                    kicker = _txt(k.group(1))[:40] if k else {"fa": "FA Indonesia", "ca": "Cari Akuntan", "us": "UpdateSAK"}[brand]
                    key = re.sub(r"[^a-z0-9-]+", "-", (rel or "beranda").lower()).strip("-")[:80]
                    img = _poster(brand, kicker, h1, key, root)
                url = base + img
                tags = (f'<meta property="og:image" content="{url}"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/>'
                        f'<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:image" content="{url}"/>')
                t = re.sub(r'<meta (content="[^"]*" )?name="twitter:(card|image)"( content="[^"]*")?\s*/?>\s*', "", t)
                t = t.replace("</head>", tags + "\n</head>", 1); og += 1; ch = True
            # 2. tombol share
            if 'class="share"' not in t and not article and m:
                name = h1[:90]
                if "tshare-css" not in t: t = t.replace("</head>", CSS + "</head>", 1)
                k2 = re.search(r"</h1>", t)
                t = t[:k2.end()] + f'<div class="tshare-top"><div class="share" data-tool="{name}" data-lab="Bagikan"></div></div>' + t[k2.end():]
                if TOOL.match(rel) or rel.startswith("kalkulator") :
                    i = max(t.rfind("<footer"), 0) or t.rfind("</body>")
                    t = t[:i] + ('<section class="tshare"><h3>Bermanfaat? Ajak Rekan Mencoba</h3><p>Langsung di browser, tanpa daftar.</p>'
                                 f'<div class="share" data-tool="{name}" data-lab="Bagikan"></div></section>\n') + t[i:]
                sh += 1; ch = True
            if ch: open(p, "w", encoding="utf-8").write(t)
        res[site] = {"og": og, "share": sh}
    return res
