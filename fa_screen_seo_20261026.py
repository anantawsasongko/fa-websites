# -*- coding: utf-8 -*-
"""Internal link ke alat screening (26 Okt 2026).
- CariAkuntan: kotak CTA /screening/ di semua halaman ID (kota, kawasan, layanan, artikel).
- FA: kotak CTA Cek Kredit & Pendanaan di semua halaman /wilayah/ dan /artikel/ yang belum punya.
Idempoten (penanda ca-scr / fa-kk-all). Jalankan setelah cariakuntan/build.py, sebelum prep.py."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
CA = os.path.join(HERE, "cariakuntan", "site")
FA = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")

def nice(slug): return " ".join(w.capitalize() for w in slug.split("-"))

n = 0
for root, dirs, files in os.walk(CA):
    rel = os.path.relpath(root, CA)
    if rel == "." or rel.split(os.sep)[0] in ("en", "zh", "hokkien", "screening"): continue
    if "index.html" not in files: continue
    p = os.path.join(root, "index.html"); s = open(p, encoding="utf-8").read()
    s = re.sub(r"<!--ca-scr-->.*?<!--/ca-scr-->", "", s, flags=re.S)
    parts = rel.split(os.sep)
    where = f" di {nice(parts[-1] if len(parts) > 2 and parts[0] == 'kota' else parts[1])}" if parts[0] == "kota" and len(parts) > 1 else ""
    box = ('<!--ca-scr--><div style="margin:30px 0 8px;padding:20px 22px;border:1px solid var(--line);background:var(--panel)">'
           f'<p style="margin:0 0 6px;font-weight:600">Screening Instan Gratis untuk Perusahaan{where}</p>'
           '<p style="margin:0 0 12px">Isi angka ringkas 3 tahun, lihat langsung rasio kredit bank dan jalur IPO BEI sebelum memilih KAP atau mengajukan kredit.</p>'
           '<a class="btn btn-wa arrow" href="/screening/">Mulai Screening</a></div><!--/ca-scr-->')
    k = s.rfind("</main>")
    if k < 0: continue
    s = s[:k] + box + s[k:]; open(p, "w", encoding="utf-8").write(s); n += 1
print("CA pages:", n)

m = 0
for sub in ("wilayah", "artikel"):
    for root, dirs, files in os.walk(os.path.join(FA, sub)):
        if "index.html" not in files: continue
        p = os.path.join(root, "index.html"); s = open(p, encoding="utf-8").read()
        s = re.sub(r"<!--fa-kk-all-->.*?<!--/fa-kk-all-->", "", s, flags=re.S)
        if root.rstrip(os.sep).endswith(os.sep + "artikel") or "cek-kapasitas-kredit" in s:
            open(p, "w", encoding="utf-8").write(s); continue
        rel = os.path.relpath(root, os.path.join(FA, sub)).split(os.sep)
        where = f" di {nice(rel[-1])}" if sub == "wilayah" else ""
        box = ('<!--fa-kk-all--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
               f'<p style="margin:0 0 6px;font-weight:600">Cek Kredit dan Pendanaan Gratis untuk Perusahaan{where}</p>'
               '<p style="margin:0 0 12px">Hitung DSCR, plafon kredit per suku bunga dan tenor, serta jalur IPO BEI dalam 3 menit.</p>'
               '<a class="btn solid" href="/cek-kapasitas-kredit/">Mulai Hitung</a></div><!--/fa-kk-all-->')
        k = s.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
        if k < 0: k = s.rfind("</main>")
        if k < 0: continue
        s = s[:k] + box + s[k:]; open(p, "w", encoding="utf-8").write(s); m += 1
print("FA pages:", m)
