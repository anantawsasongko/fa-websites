# -*- coding: utf-8 -*-
"""3 Nov 2026: kotak tautan dari halaman FA terkait ke halaman andalan cariakuntan.com/jasa-pembukuan/. Idempoten (penanda fa-pb)."""
import os, re
FA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FA-Indonesia_Website_SIAP-UPLOAD-v58")
CA = "https://cariakuntan.com/jasa-pembukuan/"
B = ('<!--fa-pb--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
     '<p style="margin:0 0 6px;font-weight:600">Jasa Pembukuan Terima Beres</p>'
     '<p style="margin:0 0 12px">Upload bon dan nota ke Google Drive, tim KJA Farhani yang menyusun laporan keuangan setiap bulan. UMKM mulai Rp900 ribu, PT dan CV mulai Rp2 juta per bulan.</p>'
     f'<a class="btn solid" href="{CA}">Lihat Paket dan Harga</a></div><!--/fa-pb-->')
pages = ["laporan-keuangan-umkm", "jasa-penyusunan-laporan-keuangan", "kja-farhani", "laporan-tahunan-pt", "wilayah/malang", "wilayah/batu"]
pages += [os.path.relpath(d, FA) for d in [os.path.join(FA, "wilayah", "malang", "kecamatan", x) for x in os.listdir(os.path.join(FA, "wilayah", "malang", "kecamatan"))] if os.path.isdir(d)] if os.path.isdir(os.path.join(FA, "wilayah", "malang", "kecamatan")) else []
n = 0
for rel in pages:
    p = os.path.join(FA, rel, "index.html")
    if not os.path.exists(p): continue
    t = re.sub(r"<!--fa-pb-->.*?<!--/fa-pb-->", "", open(p, encoding="utf-8").read(), flags=re.S)
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("<h2>Pertanyaan Umum</h2>")
    if k < 0: k = t.find("</main>")
    open(p, "w", encoding="utf-8").write(t[:k] + B + t[k:]); n += 1
print("fa_pb", n)
