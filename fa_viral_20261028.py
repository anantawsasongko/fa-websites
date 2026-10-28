# -*- coding: utf-8 -*-
"""Artikel bertrafik tinggi pola "Syarat, Biaya, dan Cara ... Terbaru" (28 Okt 2026), versi FA:
- /artikel/syarat-bunga-cara-mengajukan-kur-2026/ : KUR 2026 (Permenko 1/2026) dan kapan naik ke kredit komersial
- kartu di Eksplor topik Kredit Bank, sitemap, llms.txt
Helper diambil dari fa_mitra_20261027.py. Idempoten (penanda fa-viral). Jalankan setelah fa_deal_20261028.py.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_mitra_20261027.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. MITRA RM BANK")]
_src = _src.replace('TODAY = "2026-10-27"', 'TODAY = "2026-10-28"').replace("27 Oktober 2026", "28 Oktober 2026")
exec(compile(_src, "fa_mitra_helpers", "exec"))

S1 = "syarat-bunga-cara-mengajukan-kur-2026"
body = (
 "<p><b>Kredit Usaha Rakyat (KUR) 2026</b> diatur Permenko Perekonomian Nomor 1 Tahun 2026 yang berlaku sejak 13 Januari 2026. "
 "Bunganya tetap rendah karena disubsidi pemerintah: 3% efektif per tahun untuk KUR Super Mikro dan 6% untuk KUR Mikro dan KUR Kecil pada akad pertama. "
 "Ringkasan di bawah memakai ketentuan yang diumumkan Kemenko Perekonomian dan dirangkum media keuangan. Angka final tetap dikonfirmasi ke bank penyalur.</p>"
 "<h2>Jenis, Plafon, dan Bunga KUR 2026</h2>"
 + tbl(["Jenis KUR", "Plafon per Akad", "Bunga Efektif per Tahun", "Agunan Tambahan"], [
   ("Super Mikro", "Sampai Rp10 juta", "3%", "Tidak diwajibkan"),
   ("Mikro", "Di atas Rp10 juta sampai Rp100 juta", "6% (akad pertama)", "Tidak diwajibkan"),
   ("Kecil", "Di atas Rp100 juta sampai Rp500 juta", "6% (akad pertama)", "Dapat diminta bank"),
 ])
 + "<p>Untuk sektor perdagangan nonekspor, bunga akad berikutnya bisa naik bertahap. Sektor produksi dan perdagangan berorientasi ekspor tidak dibatasi frekuensi akses. Kekayaan intelektual juga dapat dipakai sebagai agunan tambahan.</p>"
 "<h2>Syarat Umum Mengajukan KUR</h2>"
 "<ul><li>Usaha produktif dan layak, berjalan minimal enam bulan.</li>"
 "<li>Tidak sedang menerima kredit produktif dari bank lain. Kredit konsumtif seperti KPR atau kredit kendaraan dikecualikan.</li>"
 "<li>Identitas (KTP, KK) dan dokumen usaha seperti NIB atau surat keterangan usaha.</li>"
 "<li>Catatan keuangan sederhana: penjualan, pembelian, dan saldo rekening beberapa bulan terakhir.</li></ul>"
 "<h2>Cara Mengajukan</h2>"
 + flow([
   ("Pilih Bank Penyalur", "BRI, Mandiri, BNI, BSI, dan bank lain yang ditunjuk. Bandingkan proses dan cabang terdekat."),
   ("Siapkan Dokumen", "KTP, KK, NIB, foto usaha, dan catatan keuangan. NIB bisa dicek di OSS."),
   ("Ajukan", "Lewat situs atau aplikasi bank, atau langsung ke kantor cabang."),
   ("Survei dan Analisis", "Petugas mengunjungi usaha dan menghitung kemampuan bayar."),
   ("Akad dan Cair", "Kalau disetujui, akad ditandatangani dan dana dicairkan ke rekening."),
 ])
 + "<h2>Kapan KUR Tidak Lagi Cukup</h2>"
 "<p>Plafon KUR berhenti di Rp500 juta. Begitu usaha butuh modal kerja untuk kontrak proyek, stok distributor, atau ekspansi cabang, langkah berikutnya adalah kredit komersial: Kredit Modal Kerja (KMK) atau Kredit Investasi (KI). Di sini syaratnya berbeda jauh:</p>"
 + gain([
   ("Laporan Keuangan", "Bank meminta laporan keuangan dua sampai tiga tahun, sering kali sudah diaudit KAP untuk plafon menengah ke atas."),
   ("Rasio Kemampuan Bayar", "DSCR, utang terhadap EBITDA, dan siklus modal kerja dihitung dari laporan keuangan, bukan dari omzet saja."),
   ("Agunan dan Penilaian", "Tanah, bangunan, atau mesin dinilai KJPP rekanan bank."),
   ("Legalitas", "PT dengan akta, SK, NIB, dan KBLI yang sesuai kegiatan usaha."),
 ])
 + "<p>Cek berapa plafon kredit komersial yang realistis untuk usaha Anda dengan <a href=\"/cek-kapasitas-kredit/\">Cek Kapasitas Kredit</a>, atau pelajari "
 "<a href=\"/artikel/kmk-vs-kredit-investasi/\">beda KMK dan kredit investasi</a>.</p>"
)
faq = [
 ("Berapa bunga KUR 2026?", "Bunga efektif per tahun 3% untuk KUR Super Mikro dan 6% untuk KUR Mikro dan KUR Kecil pada akad pertama, sesuai Permenko Perekonomian 1/2026. Akad berikutnya untuk sektor perdagangan nonekspor dapat lebih tinggi."),
 ("Berapa plafon maksimal KUR?", "KUR Kecil sampai Rp500 juta per akad. KUR Mikro sampai Rp100 juta dan KUR Super Mikro sampai Rp10 juta."),
 ("Apakah KUR butuh agunan?", "KUR Super Mikro dan Mikro tidak mewajibkan agunan tambahan. Untuk KUR Kecil, bank dapat meminta agunan tambahan sesuai penilaiannya."),
 ("Butuh modal di atas Rp500 juta, apa pilihannya?", "Kredit modal kerja atau kredit investasi komersial. Syaratnya lebih ketat: laporan keuangan beberapa tahun, rasio kemampuan bayar, agunan yang dinilai KJPP, dan legalitas PT."),
]
art_page(S1, "Kredit Bank", "Syarat, Bunga, dan Cara Mengajukan KUR 2026 Terbaru | FA Indonesia",
         "Syarat, Bunga, dan Cara Mengajukan KUR 2026 Terbaru",
         "KUR 2026 sesuai Permenko 1/2026: plafon Super Mikro, Mikro, dan Kecil, bunga 3% dan 6%, syarat, cara mengajukan, dan kapan usaha harus naik ke kredit komersial.",
         6, body, faq,
         [("/cek-kapasitas-kredit/", "Cek Kapasitas Kredit"), ("/artikel/kmk-vs-kredit-investasi/", "KMK vs Kredit Investasi"),
          ("/artikel/alasan-kredit-bank-ditolak/", "Alasan Kredit Bank Ditolak"), ("/artikel/dokumen-pengajuan-kredit-korporasi/", "Dokumen Pengajuan Kredit Korporasi")],
         [("Kemenko Perekonomian: Konsolidasi Kredit Program 2026", "https://www.ekon.go.id/unduh/publikasi/6784/konsolidasi-kredit-program-pemerintah-2026-perkuat-pedoman-pelaksanaan-kredit-program-optimalkan-penyaluran-dan-wujudkan-pertumbuhan-ekonomi-inklusif-berbasis-usaha-mikro-dan-kecil"),
          ("Bisnis.com: Update KUR BRI Mei 2026", "https://ekonomi.bisnis.com/read/20260504/9/1971100/update-kur-bri-mei-2026-bunga-hanya-6-plafon-hingga-rp500-juta-ini-syarat-dan-cara-pengajuan")],
         "/cek-kapasitas-kredit/", "Cek Kapasitas Kredit",
         "Halo FA Indonesia, usaha kami sudah melewati batas KUR dan ingin mengajukan kredit modal kerja atau investasi ke bank.")

def strip_v(t): return re.sub(r"<!--fa-viral-->.*?<!--/fa-viral-->\n?", "", t, flags=re.S)
ip = P("artikel", "index.html"); t = strip_v(rd(ip))
k = t.find('id="t-kredit-bank"')
if k >= 0:
    k = t.find('<div class="cards2">', k) + len('<div class="cards2">')
    t = t[:k] + f'<!--fa-viral--><a class="card2" href="/artikel/{S1}/"><b>Syarat, Bunga, dan Cara Mengajukan KUR 2026</b><span>Plafon, bunga 3% dan 6%, syarat, dan kapan usaha harus naik ke kredit komersial.</span></a><!--/fa-viral-->' + t[k:]
    wtxt(ip, t)
sm = strip_v(rd(P("sitemap.xml")))
sm = sm.replace("</urlset>", f"<!--fa-viral-->\n<url><loc>{D}/artikel/{S1}/</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n<!--/fa-viral-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = re.sub(r"\n- \[KUR 2026\].*", "", rd(P("llms.txt")))
wtxt(P("llms.txt"), ll.rstrip("\n") + f"\n- [KUR 2026]({D}/artikel/{S1}/): syarat, bunga, plafon KUR 2026 dan kapan naik ke kredit komersial\n")

# judul pola "Syarat, Biaya, dan Cara ... Terbaru" untuk artikel yang isinya sudah cocok (title tag + og:title, URL tetap)
RETITLE = {
 "biaya-audit-kap-faktor-penentu": ("Biaya Audit KAP: 8 Faktor Penentu dan Kenapa Termurah Bisa Mahal", "Biaya Audit KAP 2026: 8 Faktor Penentu dan Kenapa Termurah Bisa Mahal"),
 "dokumen-pengajuan-kredit-korporasi": ("Dokumen Pengajuan Kredit Korporasi: Checklist Lengkap untuk Bank", "Syarat dan Dokumen Pengajuan Kredit Korporasi 2026: Checklist Lengkap untuk Bank"),
 "kredit-modal-kerja-kontraktor-berbasis-spk": ("Kredit Modal Kerja Kontraktor Berbasis SPK: Jenis dan Syarat Bank", "Syarat, Jenis, dan Cara Mengajukan Kredit Modal Kerja Kontraktor Berbasis SPK"),
 "biaya-jasa-penyusunan-laporan-keuangan": ("Biaya Jasa Penyusunan Laporan Keuangan: Rincian dan Cara Menghitung", "Biaya Jasa Penyusunan Laporan Keuangan 2026: Rincian dan Cara Menghitung"),
}
for slug, (old, new) in RETITLE.items():
    p = P("artikel", slug, "index.html")
    if not os.path.exists(p): continue
    t = rd(p); o = t
    t = t.replace(f"<title>{E(old)} | FA Indonesia</title>", f"<title>{E(new)} | FA Indonesia</title>")
    t = re.sub(r'(<meta property="og:title" content=")' + re.escape(E(old)), lambda m: m.group(1) + E(new), t)
    if t != o: wtxt(p, t)
    print("retitle", slug, t != o)
print("viral FA:", S1)
