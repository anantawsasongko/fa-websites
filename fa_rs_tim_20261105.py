# -*- coding: utf-8 -*-
"""5 Nov 2026 (permintaan Bos): pekerjaan konsultan rumah sakit, M&A, dan seller side memakai foto tim
Ananta W. Sasongko, CPA (sisi keuangan) dan dr. Sigit Riyarto, M.Kes, AAK (sisi operasional: medis, marketing,
cost cutting, manajemen). Blok kartu 2 foto sebelum "Pertanyaan Umum" (atau sebelum kotak penulis / </main>).
Kalau halaman punya blok tiga wajah (fa-wajah), blok itu diganti. Idempoten (penanda fa-rstim).
Jalankan setelah fa_forensik_20261105.py."""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")

CSS = ('<style id="fa-rstim-css">.rstb{margin:22px 0 26px;max-width:560px}.rstb h2{margin:0 0 12px}'
 '.rst{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}'
 '.rst>*{display:block;border:1px solid #333;border-radius:12px;overflow:hidden;background:#1e1e1e;color:inherit;text-decoration:none}'
 '.rst a:hover{border-color:#777}.rst img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;background:#d9d9d9}'
 '.rst .t{padding:10px 12px 12px}.rst b{display:block;font-size:14px;line-height:1.3;font-weight:600}'
 '.rst small{display:block;font-size:11.5px;line-height:1.4;opacity:.72;margin-top:3px}'
 '.rstb .wa{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px;padding:13px 16px;border-radius:10px;background:#25d366;color:#0b1f12;font-weight:600;font-size:15px;text-decoration:none}'
 '.rstb .wa:hover{filter:brightness(1.05)}'
 '@media(max-width:620px){.rst{gap:8px}.rst b{font-size:12.5px}.rst small{font-size:10.5px}.rst .t{padding:8px 9px 10px}}'
 '</style>')

CARDS = [
 ("/ananta-w-sasongko/", "/img/ananta-w-sasongko-cpa-rs.jpg", "Ananta W. Sasongko", "CPA · Keuangan, M&amp;A, Seller Side"),
 ("/dr-sigit-riyarto/", "/img/dr-sigit-riyarto-mkes-aak.jpg", "dr. Sigit Riyarto", "M.Kes, AAK · Medis, Marketing, Operasional"),
]
WA = "https://wa.me/6282245260121?text="
from urllib.parse import quote

def block(city=None):
    cs = ""
    for h, im, n, r in CARDS:
        inner = f'<img src="{im}" alt="{n}, {r.split(' · ')[0]}" width="700" height="875" loading="lazy" decoding="async"><div class="t"><b>{n}</b><small>{r}</small></div>'
        cs += f'<a href="{h}">{inner}</a>' if h else f'<div class="c">{inner}</div>'
    msg = "Halo FA Indonesia, saya ingin konsultasi untuk rumah sakit" + (f" di {city}" if city else "") + "."
    return ('<!--fa-rstim--><div class="rstb"><h2>Tim Konsultan Rumah Sakit</h2>'
            f'<div class="rst">{cs}</div>'
            f'<a class="wa" href="{WA}{quote(msg)}" target="_blank" rel="noopener">Chat Tim Rumah Sakit via WhatsApp</a></div><!--/fa-rstim-->\n')

CITY = {}
def pages():
    out = []
    for x in ["konsultan-rumah-sakit", "konsultan-unit-cost-rumah-sakit", "rumah-sakit-dijual", "jasa-valuasi-usaha",
              "mitra-investor", "kalkulator-valuasi-rumah-sakit", "kalkulator-valuasi-dcf",
              "konsultan-akreditasi-rumah-sakit", "konsultan-bpjs-rumah-sakit", "direktur-rumah-sakit", "menjual-rumah-sakit"]:
        out.append(os.path.join(B, x, "index.html"))
    for base in ["konsultan-rumah-sakit", "konsultan-unit-cost-rumah-sakit", "konsultan-akreditasi-rumah-sakit", "konsultan-bpjs-rumah-sakit", "direktur-rumah-sakit", "menjual-rumah-sakit"]:
        out += glob.glob(os.path.join(B, base, "*", "index.html"))
    art = os.path.join(B, "artikel")
    KW = re.compile(r"rumah-sakit|klinik|rsia|idrg|akuisisi|menjual-perusahaan|due-diligence|valuasi|merger|seller|divest")
    for s in sorted(os.listdir(art)):
        if KW.search(s): out.append(os.path.join(art, s, "index.html"))
    return [p for p in out if os.path.exists(p)]

n = 0
import html as _h
for p in pages():
    t = open(p, encoding="utf-8").read()
    rel = os.path.relpath(os.path.dirname(p), B).split(os.sep)
    city = None
    if len(rel) == 2 and rel[0] in ("konsultan-rumah-sakit", "konsultan-unit-cost-rumah-sakit", "konsultan-akreditasi-rumah-sakit", "konsultan-bpjs-rumah-sakit", "direktur-rumah-sakit", "menjual-rumah-sakit"):
        m1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        mm = re.search(r" di ([^<:]+)$", re.sub(r"<[^>]+>", "", m1.group(1)).strip()) if m1 else None
        city = _h.unescape(mm.group(1)).strip() if mm else rel[1].replace("-", " ").title()
    t = re.sub(r"<!--fa-rstim-->.*?<!--/fa-rstim-->\n?", "", t, flags=re.S)
    t = re.sub(r'<style id="fa-rstim-css">.*?</style>', "", t, flags=re.S)
    if "<!--fa-wajah-->" in t:
        t = re.sub(r"<!--fa-wajah-->.*?<!--/fa-wajah-->", block(city), t, count=1, flags=re.S)
    else:
        m = re.search(r"<h2>Pertanyaan Umum", t) or re.search(r"<section class=\"rv-sec\"><h2>Pertanyaan Umum", t)
        k = m.start() if m else -1
        if k < 0: k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
        if k < 0: k = t.rfind("</main>")
        if k < 0: continue
        t = t[:k] + block(city) + t[k:]
    if "fa-rstim-css" not in t: t = t.replace("</head>", CSS + "</head>", 1)
    open(p, "w", encoding="utf-8").write(t); n += 1
print("fa_rs_tim", n)
