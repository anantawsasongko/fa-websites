# -*- coding: utf-8 -*-
"""14 Nov 2026 (Bos: "bahasa Inggris dan Mandarinnya kalau buka dari layanan masih indo aja. Beresin.")
Pasang js/fa-lang.js di semua halaman FA yang belum punya kamus I18N sendiri (semua kecuali beranda, /layanan/, dan
halaman lain yang memuat "var I18N"). Skrip itu menambah tombol ID/EN/中文 di header bila belum ada, memakai halaman versi
bahasa resmi (hreflang) bila tersedia, dan selain itu menerjemahkan otomatis di browser (Google) sesuai pilihan bahasa
pengunjung yang tersimpan (localStorage fa-lang, sama dengan beranda). Penanda: <script id="fa-lang-js">. Idempoten.
Jalankan paling akhir setiap build FA (setelah fa_tools_anim_20261113.py)."""
import os, re, glob
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "faindonesia")
TAG = '<script defer id="fa-lang-js" src="/js/fa-lang.js?v=20261114a"></script>'
n = 0
for p in glob.glob(os.path.join(OUT, "**", "index.html"), recursive=True) + glob.glob(os.path.join(OUT, "*.html")):
    t = open(p, encoding="utf-8").read()
    t2 = re.sub(r'<script defer id="fa-lang-js" src="[^"]*"></script>', "", t)
    if "var I18N" not in t2 and "</body>" in t2 and "<header" in t2:
        t2 = t2.replace("</body>", TAG + "</body>", 1)
    if t2 != t:
        open(p, "w", encoding="utf-8").write(t2); n += 1
print("halaman", n)
