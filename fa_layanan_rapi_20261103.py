# -*- coding: utf-8 -*-
"""Rapikan tab Layanan FA (3 Nov 2026, keluhan Bos: berantakan, foto berulang, foto bersama bank hilang).
1. Galeri 12 foto "Di Balik Proses Pendampingan dan Pendanaan" (6 foto bank 31 Okt terhapus tak sengaja oleh commit 895ecc1e)
   dipulihkan di Eksplor dan ditampilkan juga di Layanan setelah Rekam Jejak.
2. Foto Ananta dan Farhani tidak lagi muncul dua kali: seksi Partner diganti kartu Tiga Orang (FA, KJA, KAP),
   blok fa-wajah terpisah di Layanan dihapus.
3. Jarak antar seksi Layanan dirapatkan.
Idempoten. Jalankan setelah fa_wajah_20261103.py dan fa_pendanaan_20261103.py."""
import os, re
R = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(R, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
GAL = open(os.path.join(R, "fa_content", "galeri_20261031.html"), encoding="utf-8").read()

# ---------- 1. Eksplor: galeri lengkap ----------
p = os.path.join(B, "artikel", "index.html"); t = open(p, encoding="utf-8").read()
t2 = re.sub(r'<section class="block" id="galeri">.*?</section>', lambda m: GAL, t, count=1, flags=re.S)
if t2 != t: open(p, "w", encoding="utf-8").write(t2)
print("eksplor galeri", t2.count("/img/galeri/") // 2)

# ---------- 2. Layanan ----------
p = os.path.join(B, "layanan", "index.html"); t = open(p, encoding="utf-8").read()
m = re.search(r'<!--fa-wajah-->.*?(<div class="wj">.*?</div></a></div>).*?<!--/fa-wajah-->', t, flags=re.S)
if m:
    wj = m.group(1)
    t = t[:m.start()] + t[m.end():]
    open(os.path.join(R, "fa_content", "layanan_wj.html"), "w", encoding="utf-8").write(wj)
else:
    wj = open(os.path.join(R, "fa_content", "layanan_wj.html"), encoding="utf-8").read()
TIM = '<!--fa-lay-tim-->' + wj + '<!--/fa-lay-tim-->\n'
if "<!--fa-lay-tim-->" in t:
    t = re.sub(r"<!--fa-lay-tim-->.*?<!--/fa-lay-tim-->\n", lambda _: TIM, t, count=1, flags=re.S)
else:
    s = t.find('id="pendiri"'); a = t.find('<div class="register two">', s); b = t.find('<div class="teamstrip">', a)
    assert s > 0 and a > 0 and b > a, "struktur Partner berubah"
    t = t[:a] + TIM + t[b:]
t = t.replace('<h2 data-i18n="k163">Partner</h2>', '<p class="eyebrow">Partner</p><h2>Tiga Orang di Balik FA, KJA, dan KAP</h2>')
t = re.sub(r'<p class="note" data-i18n="k170">.*?</p>',
           '<p class="note">Tim FA terdiri dari akuntan, auditor, analis keuangan, spesialis mutu, konsultan hukum, dan content strategist. '
           'Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak berbeda.</p>', t, count=1, flags=re.S)
# galeri setelah Rekam Jejak
GL = GAL.replace('<section class="block" id="galeri">', '<section class="block alt" id="galeri-layanan">', 1)
GL = re.sub(r'<p class="svcintro"[^>]*>.*?</p>\s*', '', GL, count=1, flags=re.S)
GL = "<!--fa-lay-galeri-->" + GL + "<!--/fa-lay-galeri-->"
t = re.sub(r"<!--fa-lay-galeri-->.*?<!--/fa-lay-galeri-->", "", t, flags=re.S)
s = t.find('id="rekam"'); e = t.find("</section>", s) + len("</section>")
assert s > 0
t = t[:e] + "\n" + GL + t[e:]
CSS = ('<style id="fa-lay-rapi">main section.block{padding-block:clamp(44px,5.5vw,76px)}'
       '#pendiri .wj{margin-top:6px}#pendiri .teamstrip{margin-top:22px}'
       '#galeri-layanan .gallery.bento{margin-top:8px}</style>')
t = re.sub(r'<style id="fa-lay-rapi">.*?</style>', "", t, flags=re.S).replace("</head>", CSS + "</head>", 1)
open(p, "w", encoding="utf-8").write(t)
print("layanan ok", "ananta foto:", t.count("ananta-w-sasongko-cpa.jpg"), "galeri:", t.count('data-full="/img/galeri/'))
