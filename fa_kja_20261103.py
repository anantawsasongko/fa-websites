# -*- coding: utf-8 -*-
"""3 Nov 2026: /kja-farhani/ di FA menjadi rumah resmi KJA Farhani (situs pages.dev lama di-redirect ke sini).
Title/description untuk pencarian merek, blok paket dan wilayah (warisan halaman kota situs lama), alternateName di JSON-LD. Idempoten (penanda fa-kja)."""
import os, re, json
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FA-Indonesia_Website_SIAP-UPLOAD-v58", "kja-farhani", "index.html")
t = open(P, encoding="utf-8").read()
TITLE = "KJA Farhani K.N. Malang: Kantor Jasa Akuntansi Berizin, Jasa Pembukuan dan Laporan Keuangan | FA Indonesia"
DESC = "KJA Farhani K.N. (Kantor Jasa Akuntansi Farhani), Malang, izin KMK 232/KM.1/PPPK/2020: jasa pembukuan terima beres, laporan keuangan SAK EMKM dan SAK EP, laporan tahunan PT. UMKM mulai Rp900 ribu/bulan."
t = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", t, count=1, flags=re.S)
for a in ['name="description"', 'property="og:description"']:
    t = re.sub(rf'<meta {a} content="[^"]*">', f'<meta {a} content="{DESC}">', t, count=1)
t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{TITLE}">', t, count=1)
def ld_fix(m):
    try: d = json.loads(m.group(1))
    except Exception: return m.group(0)
    for g in d.get("@graph", []):
        if g.get("@type") == "AccountingService":
            g["alternateName"] = ["KJA Farhani", "KJA Farhani K.N.", "Kantor Jasa Akuntansi Farhani", "KJA Farhani Malang"]
            g["areaServed"] = ["Malang", "Batu", "Surabaya", "Sidoarjo", "Pasuruan", "Kediri", "Mojokerto", "Tuban", "Indonesia"]
            g["priceRange"] = "Mulai Rp900.000/bulan"
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"
t = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld_fix, t, count=1, flags=re.S)
t = re.sub(r"<!--fa-kja-->.*?<!--/fa-kja-->", "", t, flags=re.S)
CA = "https://cariakuntan.com"
blk = ('<!--fa-kja--><h2>Paket Jasa Pembukuan Terima Beres</h2>'
 '<p>Klien cukup upload foto bon, nota, dan catatan kas ke Google Drive. Tim KJA menginput, merekonsiliasi, dan mengirim laporan keuangan 5 sampai 10 hari kerja setelah bukti lengkap.</p>'
 '<div class="tblwrap"><table><tr><th>Paket</th><th>Mulai</th></tr>'
 '<tr><td>Pembukuan UMKM dan perorangan</td><td>Rp900 ribu/bulan</td></tr><tr><td>Pembukuan PT dan CV</td><td>Rp2 juta/bulan</td></tr>'
 '<tr><td>Laporan tahunan PT (SABH)</td><td>Rp3 juta, belum termasuk notaris</td></tr><tr><td>SPT Tahunan Badan</td><td>Rp3 juta</td></tr></table></div>'
 f'<p><a class="btn solid" href="{CA}/jasa-pembukuan/">Lihat Paket Lengkap</a> <a class="btn line" href="{CA}/files/contoh-laporan-keuangan-bulanan-jasa-pembukuan.pdf">Contoh Laporan (PDF)</a></p>'
 '<h2>Wilayah Layanan</h2><p>Berkantor di Malang, melayani daring ke seluruh Indonesia. Halaman per kota: '
 f'<a href="{CA}/jasa-pembukuan/malang/">Malang</a>, ' + ", ".join(f'<a href="{CA}/kota/{c}/kja/">{n}</a>' for c, n in [("batu", "Batu"), ("surabaya", "Surabaya"), ("sidoarjo", "Sidoarjo"), ("pasuruan", "Pasuruan"), ("kediri", "Kediri"), ("mojokerto", "Mojokerto"), ("tuban", "Tuban")])
 + '.</p><p style="font-size:13px;opacity:.75">Website KJA Farhani sebelumnya (kja-farhani.pages.dev) kini dialihkan ke halaman ini.</p><!--/fa-kja-->')
k = t.find("<h2>Kontak</h2>")
if k < 0: k = t.find("<h2>Pertanyaan Umum</h2>")
t = t[:k] + blk + t[k:]
open(P, "w", encoding="utf-8").write(t); print("fa_kja ok")
