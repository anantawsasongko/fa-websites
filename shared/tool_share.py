# -*- coding: utf-8 -*-
"""Tombol share (Instagram, Threads, LinkedIn, X, WhatsApp, Salin Link) di semua kalkulator dan apps (1 Nov 2026).
Menyisipkan placeholder <div class="share" data-tool> yang dirender oleh shared/share.js.
Atas: tepat setelah H1. Bawah: blok ajakan sebelum footer. Idempoten. Dipanggil prep.py sebelum add_share_js."""
import os, re
TOOLS = {
 "faindonesia": {
   "cek-psak-118": "Cek Dampak PSAK 118 ke Laporan Laba Rugi",
   "cek-kapasitas-kredit": "Cek Kapasitas Kredit Usaha",
   "simulasi-plafon-kredit-usaha": "Simulasi Plafon Kredit Usaha",
   "kalkulator-dscr": "Kalkulator DSCR",
   "cek-kelayakan-ipo": "Cek Kelayakan IPO",
   "apps": "FA Apps, alat kerja akuntansi dan audit",
   "galaxy": "FA Galaxy, konversi laporan laba rugi PSAK 118",
   "saturn": "FA Saturn, kertas kerja audit untuk KAP (demo)",
   "audit-ready": "FA Jupiter, laporan keuangan audit ready",
 },
 "faindonesia-jupiter": {"audit-ready": "FA Jupiter, laporan keuangan audit ready"},
 "cariakuntan": {"screening": "Screening Instan Kebutuhan Akuntan"},
}
CSS = ('<style id="tshare-css">.tshare{max-width:1080px;margin:36px auto 8px;padding:22px 20px;border:1px solid rgba(127,127,127,.25);'
       'border-radius:14px;text-align:center}.tshare h3{margin:0 0 4px;font-size:1.15rem}.tshare p{margin:0 0 6px;opacity:.75;font-size:.95rem}'
       '.tshare .fxs{justify-content:center;margin:10px 0 0}.tshare-top .fxs{margin:14px 0 6px}@media(max-width:720px){.tshare{margin:28px 16px 8px}}</style>')
def ph(name, lab, url=None):
    u = f' data-url="{url}"' if url else ""
    return f'<div class="share" data-tool="{name}" data-lab="{lab}"{u}></div>'
def block(name, url=None):
    return ('<section class="tshare"><h3>Bermanfaat? Ajak rekan mencoba</h3>'
            '<p>Gratis, langsung di browser, tanpa daftar.</p>' + ph(name, "Bagikan", url) + '</section>')
def _end(t):
    for k in ("<footer", "</main>", "</body>"):
        i = t.rfind(k)
        if i > 0: return i
    return len(t)
def run(OUT):
    n = 0
    for site, pages in TOOLS.items():
        for slug, name in pages.items():
            p = os.path.join(OUT, site, slug, "index.html")
            if not os.path.exists(p): continue
            t = open(p, encoding="utf-8").read()
            if 'class="tshare"' in t: continue
            t = t.replace("</head>", CSS + "</head>", 1)
            m = re.search(r"</h1>", t)
            if m: t = t[:m.end()] + '<div class="tshare-top">' + ph(name, "Bagikan alat ini") + '</div>' + t[m.end():]
            i = _end(t); t = t[:i] + block(name) + "\n" + t[i:]
            open(p, "w", encoding="utf-8").write(t); n += 1
    # UpdateSAK: kalkulator di beranda (#kalkulator)
    p = os.path.join(OUT, "updatesak", "index.html")
    if os.path.exists(p):
        t = open(p, encoding="utf-8").read()
        k = t.find('id="kalkulator"')
        if k > 0 and 'class="tshare"' not in t:
            s0 = t.rfind("<section", 0, k)
            # cari </section> penutup dengan menghitung nesting
            depth, j = 0, s0
            while True:
                a = t.find("<section", j + 1); b = t.find("</section>", j + 1)
                if b < 0: break
                if 0 < a < b: depth += 1; j = a; continue
                if depth == 0: j = b + len("</section>"); break
                depth -= 1; j = b
            t = t.replace("</head>", CSS + "</head>", 1)
            j = j + len(CSS) - len("</section>")  # di dalam section kalkulator, supaya ikut bila section dipindah
            t = t[:j] + block("Kalkulator Standar Akuntansi dan Penyusun CALK", "/#kalkulator").replace('class="tshare"', 'class="tshare" style="margin:28px auto 0"') + t[j:]
            open(p, "w", encoding="utf-8").write(t); n += 1
    return n
