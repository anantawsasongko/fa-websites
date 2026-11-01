# -*- coding: utf-8 -*-
"""Halaman layanan dari lead nyata (1 Nov 2026):
- /jasa-valuasi-usaha/ (lead Faresta Cake, Kebumen, 29 Okt: "valuasi usaha", masih perorangan, cari investor)
Plus kotak CTA di artikel valuasi/investor terkait dan /laporan-keuangan-umkm/, blok di /layanan/, sitemap, llms.txt.
Helper diambil dari fa_lead_20261026.py. Idempoten (penanda fa-lead2).
Jalankan setelah fa_lead_20261026.py; urutan aman: tepat sebelum prep.py (setelah fa_screen_seo_20261026.py)."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-01"')
exec(compile(_src, "fa_lead_helpers", "exec"))

PV = "/jasa-valuasi-usaha/"
pv_body = (
 "<h2>Kapan Pemilik Usaha Butuh Valuasi</h2><ul>"
 "<li>Ada calon investor atau rekan yang ingin masuk dan bertanya, berapa nilai usaha ini dan berapa persen saham yang didapat.</li>"
 "<li>Ingin menjual sebagian atau seluruh usaha, atau membeli usaha orang lain.</li>"
 "<li>Usaha keluarga akan dibagi atau diwariskan, dan semua pihak perlu angka yang bisa dijelaskan.</li>"
 "<li>Usaha masih perorangan dan akan diubah menjadi CV atau PT, lalu aset dan modal perlu dicatat dengan nilai yang wajar.</li>"
 "<li>Ingin tahu posisi usaha sebelum mengajukan kredit bank atau ekspansi cabang.</li></ul>"
 "<h2>Tiga Pendekatan Valuasi</h2>"
 + tbl(["Pendekatan", "Cara Kerja Singkat", "Cocok Untuk"], [
   ("Pendapatan (DCF)", "Memproyeksikan arus kas beberapa tahun ke depan lalu didiskontokan dengan tingkat risiko yang wajar", "Usaha yang sudah stabil dan punya rencana pertumbuhan yang bisa dijelaskan"),
   ("Pasar (multiple)", "Membandingkan dengan transaksi atau perusahaan sejenis, misalnya kelipatan laba atau EBITDA", "Usaha di sektor yang punya banyak pembanding, seperti makanan, ritel, klinik"),
   ("Aset (nilai buku disesuaikan)", "Menjumlahkan aset dengan nilai wajarnya dikurangi utang", "Usaha yang nilainya banyak di aset: properti, armada, mesin, persediaan"),
 ])
 + "<p>Untuk usaha kecil dan menengah, hasil akhirnya biasanya berupa rentang nilai, bukan satu angka. Rentang itu yang dipakai sebagai dasar negosiasi dengan investor atau pembeli.</p>"
 "<h2>Khusus Usaha Perorangan</h2>"
 "<p>Banyak usaha yang dicari investor masih atas nama pribadi: rekening campur, aset atas nama pemilik, dan gaji pemilik tidak tercatat. Sebelum dinilai, kami bantu memisahkan mana yang milik usaha dan mana yang pribadi, menormalkan laba (misalnya gaji pemilik disesuaikan ke harga pasar, biaya pribadi dikeluarkan), lalu menyusun laporan keuangan sederhana sesuai SAK EMKM. Tanpa langkah ini, angka valuasi mudah dibantah calon investor.</p>"
 "<h2>Alur Kerja</h2>" + flow([
   ("Diskusi awal", "Gratis. Tujuan valuasi, jenis usaha, dan data yang tersedia."),
   ("Rapikan data", "Mutasi rekening, catatan penjualan, daftar aset, dan utang dikumpulkan dan dipisahkan dari keuangan pribadi."),
   ("Normalisasi", "Laba dan arus kas disesuaikan supaya mencerminkan kinerja usaha yang sebenarnya."),
   ("Valuasi", "Dua sampai tiga pendekatan, hasilnya rentang nilai beserta asumsi yang bisa dijelaskan."),
   ("Bahan investor", "Ringkasan usaha, proyeksi, dan usulan struktur porsi saham atau bagi hasil.")])
 + "<h2>Valuasi Indikatif dan Laporan Penilai Resmi</h2>"
 "<p>Valuasi dari kami bersifat indikatif untuk negosiasi dan perencanaan. Bila Anda butuh laporan penilaian bisnis yang resmi, misalnya untuk keperluan hukum, pajak, atau transaksi yang mensyaratkan penilai berizin, penilaian dilakukan oleh KJPP. Kami menyiapkan datanya dan menghubungkan dengan KJPP yang sesuai lewat <a href=\"https://cariakuntan.com/\">CariAkuntan</a>.</p>"
 "<h2>Data yang Perlu Disiapkan</h2><ul>"
 "<li>Mutasi rekening usaha (dan rekening pribadi yang dipakai untuk usaha) 12 sampai 24 bulan terakhir.</li>"
 "<li>Catatan penjualan dan pembelian, bisa dari aplikasi kasir, Excel, atau buku.</li>"
 "<li>Daftar aset (peralatan, kendaraan, bangunan) beserta perkiraan nilainya.</li>"
 "<li>Daftar utang dan cicilan.</li>"
 "<li>Rencana usaha 3 sampai 5 tahun ke depan, sesederhana apa pun.</li></ul>"
 "<h2>Bacaan Terkait</h2><ul>"
 "<li><a href=\"/artikel/valuasi-perusahaan-swasta-dcf-multiple-ebitda/\">Valuasi Perusahaan Swasta: DCF dan Multiple EBITDA</a></li>"
 "<li><a href=\"/artikel/modal-usaha-dari-investor-atau-bank/\">Modal Usaha dari Investor atau Bank</a></li>"
 "<li><a href=\"/artikel/cara-menjual-perusahaan-atau-sebagian-saham/\">Cara Menjual Perusahaan atau Sebagian Saham</a></li>"
 "<li><a href=\"/artikel/due-diligence-investor-yang-perlu-disiapkan/\">Due Diligence Investor yang Perlu Disiapkan</a></li>"
 "<li><a href=\"/laporan-keuangan-umkm/\">Jasa Laporan Keuangan UMKM</a></li></ul>")
PV_FAQ = [
 ("Apakah usaha perorangan bisa divaluasi?", "Bisa. Langkah pertamanya memisahkan keuangan usaha dari keuangan pribadi dan menormalkan laba, lalu valuasi dilakukan dengan pendekatan yang sama seperti perusahaan berbadan hukum."),
 ("Berapa lama proses valuasi usaha?", "Untuk usaha kecil dengan data yang cukup lengkap, umumnya 1 sampai 3 minggu. Bila data masih tercampur dan perlu dirapikan dulu, waktunya lebih panjang."),
 ("Apakah hasil valuasi bisa dipakai untuk investor?", "Ya. Hasilnya berupa rentang nilai beserta asumsi yang bisa dijelaskan, dilengkapi ringkasan usaha dan proyeksi, yang biasa dipakai sebagai dasar negosiasi porsi saham."),
 ("Apa bedanya dengan penilaian oleh KJPP?", "Valuasi kami bersifat indikatif untuk negosiasi dan perencanaan. Laporan penilaian bisnis resmi diterbitkan oleh KJPP berizin; kami bisa menyiapkan data dan menghubungkan dengan KJPP yang sesuai."),
 ("Berapa biayanya?", "Bergantung pada skala usaha, kerapian data, dan tujuan valuasi. Angka pasti disampaikan setelah diskusi awal, sebelum Anda berkomitmen."),
]
svc_page(PV, "Layanan · Investor & Valuasi", "Jasa Valuasi Usaha untuk UMKM, Usaha Perorangan, dan Persiapan Investor",
  "Berapa nilai usaha Anda dan berapa persen yang pantas untuk investor? Kami bantu rapikan data, normalisasi laba, dan menghitung rentang nilai dengan pendekatan DCF, multiple, dan aset. Untuk usaha perorangan, CV, maupun PT di seluruh Indonesia.",
  pv_body, PV_FAQ, "Jasa Valuasi Usaha UMKM dan Perorangan untuk Investor | FA Indonesia",
  "Valuasi usaha untuk UMKM dan usaha perorangan: pisahkan keuangan pribadi, normalisasi laba, DCF, multiple, nilai aset, sampai bahan negosiasi investor. Diskusi awal gratis.",
  "Jasa Valuasi Usaha", "Business valuation advisory",
  "/mitra-investor/", "Untuk Investor", "Halo FA Indonesia, saya ingin tanya jasa valuasi usaha untuk persiapan investor.", "Valuasi Usaha")
URLS = [PV]

def box(href, title, text):
    return (f'<!--fa-lead2--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
            f'<p style="margin:0 0 6px;font-weight:600">{E(title)}</p><p style="margin:0 0 12px">{E(text)}</p>'
            f'<a class="btn solid" href="{href}">Lihat Layanan</a></div><!--/fa-lead2-->')
B = box(PV, "Ingin Tahu Nilai Usaha Anda?", "Valuasi untuk UMKM dan usaha perorangan: data dirapikan, laba dinormalkan, hasilnya rentang nilai yang siap dibahas dengan investor.")
for parts in [("artikel", "valuasi-perusahaan-swasta-dcf-multiple-ebitda"), ("artikel", "modal-usaha-dari-investor-atau-bank"),
              ("artikel", "cara-menjual-perusahaan-atau-sebagian-saham"), ("artikel", "due-diligence-investor-yang-perlu-disiapkan"),
              ("laporan-keuangan-umkm",), ("mitra-investor",)]:
    p = P(*parts, "index.html")
    if not os.path.exists(p): print("skip", p); continue
    t = re.sub(r"<!--fa-lead2-->.*?<!--/fa-lead2-->", "", rd(p), flags=re.S)
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("</main>")
    wtxt(p, t[:k] + B + t[k:])

# /layanan/
lp = P("layanan", "index.html")
t = re.sub(r"<!--fa-lead2-svc-->.*?<!--/fa-lead2-svc-->", "", rd(lp), flags=re.S)
blk = ('<!--fa-lead2-svc--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Baru</p><h2>Valuasi Usaha untuk Investor</h2></div>'
       '<p class="t" style="max-width:62em">Untuk UMKM dan usaha perorangan yang didekati investor atau ingin menjual sebagian usaha.</p>'
       '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn solid" href="/jasa-valuasi-usaha/">Jasa Valuasi Usaha</a></div></div></section><!--/fa-lead2-svc-->')
i = t.find('<section class="block'); wtxt(lp, t[:i] + blk + t[i:])

sm = re.sub(r"<!--fa-lead2-->.*?<!--/fa-lead2-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-lead2-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for u in URLS) + "<!--/fa-lead2-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)

ll = rd(P("llms.txt"))
line = "- Jasa valuasi usaha untuk UMKM, usaha perorangan, dan persiapan investor: normalisasi laba, DCF, multiple, nilai aset → https://faindonesia.co.id/jasa-valuasi-usaha/\n"
ll = ll.replace(line, "")
if "\n## Layanan Spesifik\n" in ll:
    ll = ll.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + line, 1)
else:
    ll = ll.rstrip("\n") + "\n\n## Layanan Spesifik\n" + line
wtxt(P("llms.txt"), ll)
print("fa_lead2 ok", URLS)
