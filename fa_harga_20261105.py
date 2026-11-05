# -*- coding: utf-8 -*-
"""5 Nov 2026 (aturan Bos): di semua FA Apps tidak ada kata "bayar" dan tidak ada harga yang diumumkan di muka.
Semua aplikasi dan hasil ringkasnya gratis, ajak orang mencoba. Yang gratis bilang gratis + QRIS donasi.
Pembayaran (Mayar atau QRIS) hanya muncul saat pengguna mau mengunduh laporan hasil lengkap.
Script ini membersihkan teks sumber (Jupiter, Galaxy, /apps/, /toko/, kalkulator Venus). Idempoten.
Jalankan sebelum prep.py (setelah fa_venus_unggulan_20261104.py)."""
import os, re, json
M = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(M, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
JUP = os.path.join(M, "FA-Jupiter_SIAP-UPLOAD-v6", "audit-ready", "index.html")
MAYAR_DAY = "https://fa-indonesia-14404.myr.id/pl/fa-jupiter-audit-ready-day-pass-1-hari"
MAYAR_YEAR = "https://fa-indonesia-14404.myr.id/pl/fa-jupiter-audit-ready-tahunan-1-tahun"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t): open(p, "w", encoding="utf-8").write(t)
def rep(t, pairs, label):
    n = 0
    for a, b in pairs:
        if a in t: t = t.replace(a, b); n += 1
    print(f"  {label}: {n}/{len(pairs)} pola diganti")
    return t

# ---------- FA Jupiter ----------
t = rd(JUP)
t = rep(t, [
    ('["pay","Bayar akses","Day pass Rp39.000 atau tahunan Rp249.000.",`<a class="btn small" href="/bayar/?produk=ar-year">Bayar</a>`]',
     '["pay","Unduh hasil lengkap","Excel, Word CALK, dan file proyek. Pilih akses saat klik Download.",`<button class="btn small" data-tab="lk">Lihat Laporan</button>`]'),
    ('<p>Coba dulu dengan data contoh. Bayar kalau sudah yakin.</p>', '<p>Coba dulu dengan data contoh. Semua hasil tampil gratis, tanpa daftar.</p>'),
    ('<th>Fitur</th><th>Gratis</th><th>Berbayar</th>', '<th>Fitur</th><th>Gratis</th><th>Akses Penuh</th>'),
    ('<button class="btn small primary" data-tab="mulai">Harga &amp; aktivasi</button>', '<button class="btn small primary" data-tab="mulai">Aktivasi</button>'),
    ('Penyimpanan otomatis, file proyek, dan Download Excel tersedia dengan akses berbayar.', 'Penyimpanan otomatis, file proyek, dan Download Excel terbuka dengan kode akses.'),
    ('gate("Download Word CALK tersedia setelah akses diaktifkan.")', 'gate("Tempel kode akses untuk membuka Download Word CALK.")'),
    ('gate("Download Excel tersedia setelah akses diaktifkan.")', 'gate("Tempel kode akses untuk membuka Download Excel.")'),
    ('gate("Simpan file proyek tersedia setelah akses diaktifkan.")', 'gate("Tempel kode akses untuk membuka file proyek.")'),
], "jupiter teks")
# kotak aktivasi: tanpa harga; pilihan akses lewat tombol Download (paywall v4)
t = re.sub(r'<p class="note">Beli kode akses: <a href="[^"]*day-pass[^"]*"[^>]*>[^<]*</a> atau <a href="[^"]*tahunan[^"]*"[^>]*>[^<]*</a> \(termasuk PPN\)\. Kode tampil otomatis setelah pembayaran\. Semua fitur tetap bisa dicoba gratis\.</p>',
           '<p class="note">Belum punya kode? Klik <b>Download Excel</b> atau <b>Download Word CALK</b>, pilih masa akses, kode tampil otomatis setelah selesai. Semua fitur tetap bisa dicoba gratis.</p>', t)
assert "Rp39.000" not in t and "Rp249.000" not in t, "harga Jupiter masih ada"
wr(JUP, t)

# ---------- Galaxy ----------
p = os.path.join(FA, "galaxy", "index.html"); t = rd(p)
t = rep(t, [
    ('<h3 data-i18n="j7">Gratis dan Berbayar</h3>', '<h3 data-i18n="j7">Gratis dan Akses Penuh</h3>'),
    ('<li data-i18n="jr2"><b>Akses berbayar:</b> simpan otomatis, file proyek untuk dibuka lagi, dan download Excel. Data tetap di laptop Anda.</li>',
     '<li data-i18n="jr2"><b>Akses penuh:</b> simpan otomatis, file proyek untuk dibuka lagi, dan download Excel serta Word CALK. Pilihan akses muncul saat klik Download. Data tetap di laptop Anda.</li>'),
    ('"j7": "Free and Paid"', '"j7": "Free and Full Access"'),
    ('"jr2": "<b>Paid access:</b> autosave, project files you can reopen, and Excel download. Your data stays on your laptop."',
     '"jr2": "<b>Full access:</b> autosave, project files you can reopen, and Excel and Word downloads. Access options appear when you click Download. Your data stays on your laptop."'),
    ('"j7": "免费与付费"', '"j7": "免费与完整版"'),
    ('"jr2": "<b>付费开通：</b>自动保存、可再次打开的项目文件，以及 Excel 下载。数据仍保存在您的电脑上。"',
     '"jr2": "<b>完整版：</b>自动保存、可再次打开的项目文件，以及 Excel 和 Word 下载。点击下载时会显示访问选项。数据仍保存在您的电脑上。"'),
], "galaxy")
wr(p, t)

# ---------- /apps/ ----------
p = os.path.join(FA, "apps", "index.html"); t = rd(p)
n = len(re.findall(r'<span class="cat">Rp\d+ rb</span>', t))
t = re.sub(r'<span class="cat">Rp\d+ rb</span>', '<span class="cat">Coba Gratis</span>', t)
t = rep(t, [
    ('<p class="lead">Bayar sekali per aplikasi lewat QRIS, akses tersimpan di perangkat Anda. Kalkulator memberi angka cepat.',
     '<p class="lead">Semua aplikasi gratis dicoba, hasil ringkas langsung tampil di layar. Kalkulator memberi angka cepat.'),
    ('<div class="meta vu-k"><b>Rp49 rb</b><span>bayar QRIS di aplikasi</span>', '<div class="meta vu-k"><b>Gratis</b><span>coba langsung, laporan lengkap bisa diunduh</span>'),
], "apps")
print(f"  apps: {n} badge harga -> Coba Gratis")
wr(p, t)

# ---------- /toko/ (halaman jualan: harga produk tetap, tapi tanpa kata bayar di kartu aplikasi) ----------
p = os.path.join(FA, "toko", "index.html")
if os.path.exists(p):
    t = rd(p)
    t = rep(t, [("termasuk PPN · bayar QRIS di aplikasi", "termasuk PPN · unduh laporan lengkap di aplikasi"), ("Termasuk PPN · Bayar QRIS di Aplikasi", "Termasuk PPN · Unduh laporan lengkap di aplikasi")], "toko")
    wr(p, t)

# ---------- kalkulator FA Venus: 6 kalkulator gratis (hapus FA_PAY), DCF dapat tombol unduh laporan ----------
FREE = ["kalkulator-pph-21", "kalkulator-pph-badan", "kalkulator-potput-ppn", "kalkulator-penyusutan-fiskal", "kalkulator-cicilan-pinjaman", "kalkulator-rasio-keuangan"]
for s in FREE:
    p = os.path.join(FA, s, "index.html"); t = rd(p)
    t2 = re.sub(r'<script>window\.FA_PAY=\{[^<]*\}\s*;?\s*</script>\s*<script src="/js/fa-paywall\.js"[^>]*></script>', "", t)
    if t2 != t: wr(p, t2); print(f"  {s}: FA_PAY dihapus (gratis)")
p = os.path.join(FA, "kalkulator-valuasi-dcf", "index.html"); t = rd(p)
t = re.sub(r'<script>window\.FA_PAY=\{[^<]*\}\s*;?\s*</script>\s*<script src="/js/fa-paywall\.js"[^>]*></script>', "", t)
if 'id="dcf_pdf"' not in t:
    t = t.replace('<p class="note">Baris = WACC, kolom = pertumbuhan terminal.',
                  '<p style="margin:14px 0 0"><button class="btn primary" id="dcf_pdf" type="button" data-fa-full="">Unduh Laporan Lengkap (PDF)</button></p>\n  <p class="note">Baris = WACC, kolom = pertumbuhan terminal.', 1)
    t = t.replace("calc();\n\n})();", 'calc();\n$("#dcf_pdf").addEventListener("click",()=>{calc();window.print()});\n\n})();', 1)
    t = t.replace("</style>", "@media print{header,nav,footer,.toast,#fapw,#faDon,#faDonPill,#faai-b,#faai,.fa-share,#dcf_pdf{display:none!important}body{background:#fff;color:#000}.sec{break-inside:avoid}}\n</style>", 1) if "@media print{header,nav,footer" not in t else t
    print("  dcf: tombol Unduh Laporan Lengkap (PDF) ditambah")
wr(p, t)
print("fa_harga_20261105 selesai")
