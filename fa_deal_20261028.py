# -*- coding: utf-8 -*-
"""Deal flow untuk mitra (28 Okt 2026):
- /mitra-investor/ : PE, family office, VC tahap lanjut, pembeli strategis, investor asing yang mencari investee / target akuisisi
- 4 artikel Eksplor: target penyaluran kredit (RM & Commercial Head), undisbursed loan, cara investor mencari target akuisisi,
  red flag calon investee sebelum term sheet
- kotak di halaman terkait (penanda fa-deal), footer "Mitra Investor", kartu Eksplor, sitemap, llms.txt
- blok Ekosistem (CariAkuntan + UpdateSAK) di halaman mitra
Helper (set_head, partner_page, art_page, flow, gain, tbl, dll.) diambil dari fa_mitra_20261027.py bagian atas.
Idempoten. Jalankan setelah fa_mitra_20261027.py, sebelum fa_rapi_20261027.py dan prep.py.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_mitra_20261027.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. MITRA RM BANK")]
_src = _src.replace('TODAY = "2026-10-27"', 'TODAY = "2026-10-28"').replace("27 Oktober 2026", "28 Oktober 2026")
exec(compile(_src, "fa_mitra_helpers", "exec"))

CA = "https://cariakuntan.com"
US = "https://updatesak.com"
ECO = ('<h2>Ekosistem yang Mendukung</h2>'
       + gain([
         ("CariAkuntan", f'Butuh KAP, KJPP, atau konsultan pajak yang diterima bank dan investor untuk audit, penilaian agunan, atau due diligence? <a href="{CA}/">cariakuntan.com</a> membantu memilihkan kantor berizin sesuai kelas rekanan.'),
         ("UpdateSAK", f'Cek cepat apakah laporan keuangan calon debitur atau investee sudah memakai PSAK terbaru, termasuk PSAK 118 yang berlaku 2027, di <a href="{US}/">updatesak.com</a>.'),
       ]).replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))

# ================= 1. MITRA INVESTOR =================
PIV = "/mitra-investor/"
WA_IV = "Halo FA Indonesia, saya investor dan ingin berdiskusi soal peluang investasi atau target akuisisi. Kriteria kami: sektor ..., ukuran ..., porsi ..."
iv_body = (
 "<h2>Siapa yang Kami Layani</h2>"
 + gain([
   ("Private Equity dan Growth Fund", "Mencari perusahaan dengan EBITDA nyata yang bisa dinormalisasi, rencana pertumbuhan jelas, dan jalur keluar lewat penjualan strategis atau IPO."),
   ("Family Office dan Investor Individu", "Mencari kepemilikan mayoritas atau minoritas di usaha yang arus kasnya stabil dan bisa dipantau tanpa harus mengelola sehari-hari."),
   ("Pembeli Strategis dan Grup Usaha", "Mencari akuisisi untuk menambah wilayah, kapasitas, atau lini layanan, misalnya grup rumah sakit, jaringan klinik, atau grup distribusi."),
   ("Investor Asing (PMA)", "Mencari mitra lokal atau target akuisisi dengan pemetaan bidang usaha, perizinan, dan struktur pajak yang sudah dicek sejak awal."),
 ])
 + "<h2>Peluang yang Kami Tangani</h2>"
 + tbl(["Sektor", "Jenis Transaksi", "Ketersediaan"], [
   ("Rumah Sakit Swasta", "Akuisisi mayoritas atau penuh, Jawa Tengah dan DIY", '<a href="/rumah-sakit-dijual/">Mandat aktif</a>'),
   ("BPR dan BPRS", "Akuisisi saham pengendali", '<a href="/bpr-dijual/">Mandat aktif</a>'),
   ("Klinik, Dental, dan Kecantikan", "Investasi pertumbuhan untuk ekspansi cabang", "Sesuai kriteria investor"),
   ("Distributor dan Importir", "Modal pertumbuhan, pembiayaan modal kerja berstruktur", "Sesuai kriteria investor"),
   ("Kontraktor dan Konstruksi", "Investasi ekuitas, pembiayaan proyek", "Sesuai kriteria investor"),
   ("Manufaktur dan Grup Keluarga", "Akuisisi, pre-IPO, penataan struktur grup", "Sesuai kriteria investor"),
 ])
 + "<p>Nama perusahaan tidak pernah kami sebut sebelum ada persetujuan pemilik dan NDA. Peluang disajikan secara privat kepada investor yang sudah menandatangani NDA, bukan penawaran umum.</p>"
 + "<h2>Apa yang Sudah Disiapkan Sebelum Anda Melihat Peluang</h2>"
 + tbl(["Area", "Yang Kami Siapkan dari Sisi Perusahaan"], [
   ("Laporan Keuangan", "Tiga tahun, diaudit KAP atau siap diaudit, memakai SAK yang berlaku termasuk kesiapan PSAK 118"),
   ("Normalisasi EBITDA", "Biaya pribadi pemilik, transaksi pihak berelasi, dan pos tidak berulang dipisahkan supaya laba yang dinilai adalah laba usaha"),
   ("Model Keuangan", "Proyeksi, kebutuhan dana, dan skenario, dengan asumsi yang bisa ditelusuri ke data historis"),
   ("Pajak", "Rekonsiliasi SPT dengan laporan keuangan, posisi Coretax, dan potensi eksposur yang sudah diidentifikasi"),
   ("Legal dan Aset", "Akta, izin usaha dan izin sektor, serta aset material atas nama perusahaan"),
   ("Data Room", "Tertata sesuai daftar due diligence investor, KAP, konsultan hukum, dan KJPP"),
 ])
 + "<h2>Alur Kerja Sama</h2>" + flow([
   ("Kriteria Investasi", "Sektor, wilayah, ukuran tiket, porsi kepemilikan, dan horizon. Cukup satu halaman."),
   ("NDA", "Ditandatangani sebelum identitas dan angka perusahaan dibuka."),
   ("Teaser Anonim", "Ringkasan usaha, angka kunci, dan alasan transaksi, tanpa nama perusahaan."),
   ("IM dan Data Room", "Information memorandum, model keuangan, dan akses data room setelah pemilik setuju."),
   ("Due Diligence dan Term Sheet", "Investor menunjuk penasihatnya sendiri. Kami mengawal pemenuhan data dari sisi perusahaan sampai penutupan transaksi.")])
 + "<h2>Peran dan Biaya</h2><ul>"
   "<li>FA Indonesia bekerja dari sisi perusahaan. Imbalan kami dibayar oleh klien sesuai kontrak pendampingan, sehingga investor tidak dikenai biaya untuk mengakses peluang.</li>"
   "<li>Kami bukan perusahaan efek, manajer investasi, atau penjamin emisi, dan tidak menawarkan efek kepada publik.</li>"
   "<li>Due diligence tetap dilakukan investor secara independen bersama KAP, konsultan hukum, dan KJPP pilihannya.</li>"
   "<li>Data perusahaan hanya dibuka setelah NDA dan persetujuan pemilik.</li></ul>"
 + "<h2>Saringan Cepat untuk Investor</h2><ul>"
   "<li><a href=\"/cek-kelayakan-ipo/\">Cek Kelayakan IPO</a>: menguji apakah calon investee realistis menuju IPO sebagai jalur keluar.</li>"
   "<li><a href=\"/cek-kapasitas-kredit/\">Cek Kapasitas Kredit</a>: melihat ruang utang dan DSCR sebelum menyusun struktur pendanaan.</li>"
   "<li><a href=\"/artikel/menilai-kesiapan-calon-investee-sebelum-term-sheet/\">7 red flag laporan keuangan calon investee</a> sebelum term sheet.</li>"
   "<li><a href=\"/artikel/valuasi-rumah-sakit-swasta/\">Valuasi rumah sakit swasta</a> dan <a href=\"/artikel/indikator-keuangan-rumah-sakit-yang-dilihat-investor/\">indikator keuangan rumah sakit</a>.</li></ul>"
 + "<h2>Rekam Jejak</h2><p>Tim FA Indonesia berpengalaman mendampingi akuisisi tiga rumah sakit di Jawa Tengah dari sisi pembeli, menggalang pendanaan investor sekitar US$1 sampai 3 juta untuk grup rumah sakit, "
   "memegang mandat divestasi rumah sakit dan BPR, serta mendampingi pembiayaan perbankan kumulatif lebih dari Rp1 triliun. Tim terdiri dari Chartered Accountant dan CPA dengan latar audit firma Big Four.</p>"
 + ECO
 + '<h2>For Foreign Investors</h2><p lang="en">FA Indonesia works on the company side to prepare Indonesian private companies for investment and acquisition: audited or audit-ready financial statements under current Indonesian SAK, normalized EBITDA, tax reconciliation, legal and licensing checks, and an organized data room. '
   'Opportunities include private hospitals in Central Java and Yogyakarta, rural banks (BPR/BPRS), clinics, distributors, contractors, and family business groups. Opportunities are shared privately after an NDA and owner consent. Investors pay no fee for access. '
   'Contact us by email at ananta@faindonesia.co.id with your sector, ticket size, and ownership criteria.</p>'
 + "<h2>Bacaan untuk Investor</h2><ul>"
   "<li><a href=\"/artikel/cara-investor-mencari-target-akuisisi-indonesia/\">Cara Investor Menemukan Target Akuisisi dan Peluang Investasi Perusahaan Swasta di Indonesia</a></li>"
   "<li><a href=\"/artikel/menilai-kesiapan-calon-investee-sebelum-term-sheet/\">Menilai Calon Investee Sebelum Term Sheet: 7 Red Flag Laporan Keuangan</a></li>"
   "<li><a href=\"/artikel/due-diligence-investor-yang-perlu-disiapkan/\">Due Diligence Investor: Apa yang Diperiksa</a></li>"
   "<li><a href=\"/artikel/private-equity-vs-utang-bank/\">Private Equity vs Utang Bank</a></li></ul>")
IV_FAQ = [
 ("Bagaimana investor bisa mendapatkan peluang investasi perusahaan swasta di Indonesia?", "Kirim kriteria investasi Anda: sektor, wilayah, ukuran tiket, dan porsi kepemilikan. Setelah NDA, kami mengirim teaser anonim untuk peluang yang cocok, lalu information memorandum dan data room bila pemilik setuju."),
 ("Apakah ada biaya untuk investor?", "Tidak. FA Indonesia bekerja dari sisi perusahaan dan dibayar oleh klien sesuai kontrak pendampingan. Investor membiayai penasihat due diligence pilihannya sendiri."),
 ("Sektor apa yang sedang tersedia?", "Mandat aktif saat ini mencakup rumah sakit swasta di Jawa Tengah dan DIY serta BPR dan BPRS. Untuk klinik, distributor, kontraktor, manufaktur, dan grup keluarga, peluang disesuaikan dengan kriteria investor."),
 ("Apakah laporan keuangan calon investee sudah diaudit?", "Sebagian sudah diaudit KAP, sebagian lagi siap diaudit. Status audit, kebijakan akuntansi, dan normalisasi EBITDA dijelaskan terbuka di information memorandum."),
 ("Apakah investor asing bisa masuk?", "Bisa, sepanjang bidang usahanya terbuka untuk penanaman modal asing dan perizinan sektornya dipenuhi. Pemetaan ini kami lakukan sejak awal sebelum peluang diperkenalkan."),
 ("Apakah FA Indonesia menawarkan saham kepada publik?", "Tidak. Peluang disajikan secara privat kepada investor yang sudah menandatangani NDA. Kami bukan perusahaan efek atau manajer investasi."),
]
partner_page(PIV, "Mitra · Investor, PE, Family Office & Pembeli Strategis",
  "Untuk Investor: Peluang Investasi dan Target Akuisisi Perusahaan Swasta Indonesia yang Datanya Siap Diuji",
  "Investor private equity, family office, dan pembeli strategis sering menemukan perusahaan menarik, tetapi angkanya belum bisa diuji: laporan keuangan belum diaudit, laba bercampur biaya pribadi pemilik, dan aset masih atas nama keluarga. FA Indonesia bekerja dari sisi perusahaan. Laporan keuangan, normalisasi EBITDA, pajak, legal, dan data room kami siapkan lebih dulu, baru kemudian perusahaan diperkenalkan kepada investor yang kriterianya cocok.",
  iv_body, IV_FAQ, "Peluang Investasi & Target Akuisisi Perusahaan Swasta Indonesia | FA Indonesia",
  "Investor, PE, family office, dan pembeli strategis mencari investee atau target akuisisi di Indonesia? FA Indonesia menyajikan peluang yang disaring, data siap due diligence. Tanpa biaya untuk investor.",
  "Investor private equity, family office, venture capital tahap lanjut, pembeli strategis, grup usaha, dan investor asing", WA_IV, "Mitra Investor",
  '<a class="btn line" href="/rumah-sakit-dijual/">Lihat Rumah Sakit Dijual</a>')

# blok Ekosistem juga di halaman RM dan Sekuritas (dibangun fa_mitra), sisipkan sebelum "Pertanyaan Umum"
for pth in ("mitra-rm-bank", "mitra-sekuritas"):
    p = P(pth, "index.html"); t = re.sub(r"<!--fa-deal-eco-->.*?<!--/fa-deal-eco-->", "", rd(p), flags=re.S)
    k = t.find("<h2>Pertanyaan Umum</h2>")
    if k > 0: wtxt(p, t[:k] + "<!--fa-deal-eco-->" + ECO + "<!--/fa-deal-eco-->\n" + t[k:])

# ================= 2. ARTIKEL =================
RM_BOX2 = ('<!--fa-deal--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
           '<p style="margin:0 0 6px;font-weight:600">RM atau Commercial Head Bank?</p><p style="margin:0 0 12px">Kami merujuk debitur korporasi yang berkasnya siap diproses, dan membantu debitur memenuhi syarat pencairan fasilitas yang belum ditarik.</p>'
           '<a class="btn solid" href="/mitra-rm-bank/">Kerja Sama untuk RM Bank</a></div><!--/fa-deal-->')
IV_BOX = ('<!--fa-deal--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
          '<p style="margin:0 0 6px;font-weight:600">Anda Investor atau Pembeli Strategis?</p><p style="margin:0 0 12px">Kirim kriteria investasi Anda. Kami menyajikan peluang yang sudah disaring dan datanya siap diuji, setelah NDA. Tanpa biaya untuk investor.</p>'
          '<a class="btn solid" href="/mitra-investor/">Peluang untuk Investor</a></div><!--/fa-deal-->')
WA_RM = "Halo FA Indonesia, saya Relationship Manager bank dan ingin berdiskusi soal kerja sama rujukan debitur korporasi."

A1 = "cara-mencapai-target-penyaluran-kredit-korporasi"
a1 = (
 "<p>Target penyaluran kredit korporasi biasanya dibagi per kuartal, lalu diturunkan ke tiap RM. Yang sering terjadi, angka di akhir kuartal meleset bukan karena prospeknya kurang, tetapi karena prospek yang ada tidak bergerak cukup cepat dari pertemuan pertama ke pencairan.</p>"
 "<p>Tulisan ini membahas cara menghitung kebutuhan prospek dari target, di tahap mana waktu paling banyak hilang, dan apa yang bisa dilakukan RM serta Commercial Head untuk mempercepatnya.</p>"
 "<h2>Hitung Mundur dari Target ke Jumlah Prospek</h2>"
 "<p>Target penyaluran lebih mudah dikelola kalau diterjemahkan menjadi jumlah prospek. Contoh dengan angka dummy berikut memakai target Rp100 miliar per kuartal dan rata-rata plafon Rp10 miliar.</p>"
 + tbl(["Tahap", "Asumsi Konversi", "Jumlah yang Dibutuhkan"], [
   ("Kredit cair dalam kuartal", "Target Rp100 miliar dibagi Rp10 miliar", "10 debitur"),
   ("Kredit disetujui komite", "70% yang disetujui cair dalam kuartal yang sama", "15 debitur"),
   ("Berkas diajukan ke analis", "60% berkas yang diajukan disetujui", "24 berkas"),
   ("Prospek yang ditemui", "40% prospek berlanjut ke pengajuan berkas", "60 prospek"),
 ])
 + "<p>Angka konversi di tiap bank berbeda. Yang penting, tabel ini menunjukkan dua tuas: menambah jumlah prospek, atau menaikkan konversi di tiap tahap. Menaikkan konversi dari 40% ke 60% di tahap pertama saja memangkas kebutuhan prospek dari 60 menjadi 40.</p>"
 "<h2>Di Mana Waktu Paling Banyak Hilang</h2><ul>"
 "<li><b>Menunggu laporan keuangan.</b> Prospek menjanjikan data minggu depan, tetapi laporan yang datang hanya versi internal tanpa CALK.</li>"
 "<li><b>Data tidak cocok.</b> Omzet di laporan keuangan berbeda jauh dengan SPT dan mutasi rekening, sehingga analis meminta penjelasan berulang.</li>"
 "<li><b>Agunan dan legal.</b> Sertifikat atas nama pihak lain, izin usaha belum diperbarui, atau penilaian KJPP belum dipesan.</li>"
 "<li><b>Syarat pencairan setelah disetujui.</b> Fasilitas sudah disetujui, tetapi laporan audit, dokumen proyek, atau pengikatan agunan belum lengkap, sehingga dana tidak bisa ditarik.</li></ul>"
 "<h2>Yang Bisa Dilakukan RM</h2><ol>"
 "<li>Saring di pertemuan pertama dengan lima pertanyaan: laporan keuangan tiga tahun, kecocokan dengan SPT, SLIK, DSCR proyeksi, dan legal agunan. Detailnya ada di artikel <a href=\"/artikel/cara-rm-bank-mencari-debitur-korporasi/\">cara RM mencari debitur korporasi</a>.</li>"
 "<li>Pakai alat <a href=\"/cek-kapasitas-kredit/\">Cek Kapasitas Kredit</a> untuk melihat indikasi plafon dari angka prospek sebelum mengajukan ke analis.</li>"
 "<li>Minta daftar dokumen lengkap di awal, bukan bertahap, memakai <a href=\"/artikel/dokumen-pengajuan-kredit-korporasi/\">checklist dokumen pengajuan kredit korporasi</a>.</li>"
 "<li>Rujuk prospek bagus yang berkasnya belum siap ke pihak yang bisa merapikannya, lalu kejar kembali saat berkas lengkap.</li></ol>"
 "<h2>Yang Bisa Dilakukan Commercial Head</h2><ul>"
 "<li><b>Review pipeline mingguan per tahap</b>, bukan per nasabah. Yang dilihat: berapa yang tertahan di tiap tahap dan sudah berapa lama.</li>"
 "<li><b>Fokus sektor.</b> Sektor yang analisisnya sudah dikuasai tim, misalnya kontraktor berbasis SPK atau rumah sakit swasta, diproses jauh lebih cepat.</li>"
 "<li><b>Pantau fasilitas yang belum ditarik.</b> Per September 2026, Bank Indonesia mencatat undisbursed loan sekitar Rp2.562,7 triliun atau 21,7% dari plafon. Fasilitas yang sudah disetujui tetapi belum ditarik adalah sumber penyaluran tercepat kalau syarat pencairannya bisa dipenuhi. Pembahasannya ada di artikel <a href=\"/artikel/undisbursed-loan-cara-mempercepat-pencairan-kredit/\">undisbursed loan</a>.</li>"
 "<li><b>Jaga kualitas setelah cair.</b> Debitur yang tertib melaporkan dan memenuhi covenant tidak menggerus kinerja portofolio di kuartal berikutnya.</li></ul>"
 "<h2>Bagaimana FA Indonesia Membantu</h2>"
 "<p>Tim FA Indonesia mendampingi perusahaan menyiapkan pengajuan kredit dari sisi debitur: laporan keuangan, rekonsiliasi pajak, proyeksi arus kas, DSCR, dan dokumen legal. Kami merujuk debitur yang berkasnya siap ke RM yang segmennya cocok, menerima rujukan prospek yang perlu dibenahi dulu, dan membantu debitur memenuhi syarat pencairan. Detailnya ada di halaman <a href=\"/mitra-rm-bank/\">kerja sama untuk RM dan Commercial Head</a>.</p>")
A1_FAQ = [
 ("Bagaimana cara mencapai target penyaluran kredit korporasi?", "Hitung mundur dari target ke jumlah prospek per tahap, saring prospek sejak pertemuan pertama, percepat kelengkapan berkas, dan kejar fasilitas yang sudah disetujui tetapi belum ditarik."),
 ("Berapa prospek yang dibutuhkan untuk target penyaluran tertentu?", "Bagi target dengan rata-rata plafon untuk mendapat jumlah debitur cair, lalu bagi berturut-turut dengan tingkat konversi tiap tahap: cair dari setuju, setuju dari berkas, dan berkas dari prospek."),
 ("Di tahap mana kredit korporasi paling sering tertahan?", "Paling sering di kelengkapan laporan keuangan, kecocokan data dengan pajak, legal agunan, dan syarat pencairan setelah kredit disetujui."),
 ("Apa yang dipantau Commercial Head setiap minggu?", "Jumlah dan umur prospek di tiap tahap pipeline, konsentrasi sektor, fasilitas yang belum ditarik, dan kualitas debitur yang sudah cair."),
]
art_page(A1, "Kredit Bank", "Cara Mencapai Target Penyaluran Kredit Korporasi: RM & Commercial Head | FA Indonesia",
  "Cara Mencapai Target Penyaluran Kredit Korporasi: Panduan untuk RM dan Commercial Head",
  "Cara mencapai target penyaluran kredit korporasi: hitung mundur target ke jumlah prospek, titik yang paling sering menahan, dan yang bisa dilakukan RM serta Commercial Head.",
  7, a1, A1_FAQ,
  [("/mitra-rm-bank/", "Kerja Sama untuk RM dan Commercial Head"), ("/artikel/undisbursed-loan-cara-mempercepat-pencairan-kredit/", "Undisbursed Loan: Cara Mempercepat Pencairan"),
   ("/artikel/cara-rm-bank-mencari-debitur-korporasi/", "Cara RM Bank Mencari Debitur Korporasi"), ("/artikel/rasio-keuangan-yang-dilihat-bank/", "Rasio Keuangan yang Dilihat Bank")],
  [("Investortrust, 21 Oktober 2026: BI, undisbursed loan Rp2.562,7 triliun per September 2026", "https://investortrust.id/macro/120075/bi-kredit-yang-belum-tersalurkan-undisbursed-loan-tembus-rp-2562-7-triliun-per-september-2026")],
  "/mitra-rm-bank/", "Kerja Sama untuk RM Bank", WA_RM, RM_BOX2)

A2 = "undisbursed-loan-cara-mempercepat-pencairan-kredit"
a2 = (
 "<p>Undisbursed loan adalah fasilitas kredit yang sudah disetujui dan diperjanjikan, tetapi belum ditarik oleh debitur. Bank Indonesia mencatat angkanya sekitar Rp2.562,7 triliun per September 2026, atau 21,7% dari total plafon kredit. Pada bulan-bulan sebelumnya angka ini juga bertahan di kisaran Rp2.500 triliun.</p>"
 "<p>Bagi bank, fasilitas yang menganggur berarti target penyaluran belum tercapai walaupun proses kredit sudah selesai. Bagi debitur, fasilitas yang tidak bisa ditarik sering berarti rencana usaha tertunda.</p>"
 "<h2>Kenapa Fasilitas Tidak Ditarik</h2>"
 + tbl(["Penyebab", "Contoh", "Bisa Dipercepat?"], [
   ("Debitur menunda ekspansi", "Menunggu kepastian permintaan, harga, atau kebijakan", "Sebagian, lewat proyeksi dan skenario yang lebih jelas"),
   ("Syarat pencairan belum terpenuhi", "Laporan audit belum terbit, pengikatan agunan, dokumen proyek, asuransi", "Ya, ini yang paling bisa dikejar"),
   ("Covenant keuangan tidak terpenuhi", "Rasio utang atau DSCR melewati batas di laporan terakhir", "Ya, lewat pembenahan laporan dan rencana perbaikan"),
   ("Proyek atau kontrak mundur", "SPK belum terbit, termin pembayaran bergeser", "Tergantung pemberi kerja"),
   ("Kebutuhan modal kerja turun", "Siklus kas membaik sehingga fasilitas jadi cadangan", "Tidak perlu dipaksa"),
 ])
 + "<h2>Syarat Pencairan yang Paling Sering Tertahan</h2><ul>"
 "<li><b>Laporan keuangan audit</b> untuk tahun terakhir, atau opini yang disyaratkan bank.</li>"
 "<li><b>Pengikatan agunan</b> beserta penilaian KJPP yang masih berlaku.</li>"
 "<li><b>Dokumen penggunaan dana</b>, misalnya SPK, kontrak, invoice, atau rencana anggaran proyek.</li>"
 "<li><b>Pemenuhan covenant</b> seperti batas rasio utang, DSCR, atau setoran modal sendiri.</li>"
 "<li><b>Perizinan dan legal</b> yang diperbarui, termasuk persetujuan RUPS bila disyaratkan.</li></ul>"
 "<h2>Cara Mempercepat Pencairan</h2><ol>"
 "<li><b>Petakan syarat yang belum terpenuhi</b> per debitur, lengkap dengan siapa penanggung jawabnya dan perkiraan tanggal selesai.</li>"
 "<li><b>Mulai dari yang paling lama.</b> Audit dan penilaian KJPP butuh waktu berminggu-minggu. Memesannya di awal memotong waktu tunggu terbesar.</li>"
 "<li><b>Rapikan laporan keuangan untuk covenant.</b> Banyak covenant terlihat terlanggar karena penyajian, misalnya utang jangka panjang yang belum direklasifikasi atau biaya pribadi yang masih tercatat di perusahaan.</li>"
 "<li><b>Siapkan dokumen penggunaan dana sesuai format bank</b>, sehingga analis tidak perlu meminta ulang.</li>"
 "<li><b>Jaga komunikasi tiga pihak</b> antara RM, debitur, dan penasihat debitur, dengan satu daftar periksa yang sama.</li></ol>"
 "<h2>Peran Masing-Masing</h2><ul>"
 "<li><b>Bank dan RM</b> menetapkan syarat dan memutuskan pencairan sesuai kebijakan.</li>"
 "<li><b>Debitur</b> memenuhi syarat dan menyediakan data.</li>"
 "<li><b>Penasihat dari sisi debitur</b> membantu menyiapkan laporan keuangan, dokumen, dan koordinasi dengan KAP serta KJPP, tanpa menggantikan keputusan bank.</li></ul>"
 "<p>Untuk kebutuhan KAP atau KJPP yang diterima bank, debitur bisa memakai <a href=\"https://cariakuntan.com/\">CariAkuntan</a> untuk memilih kantor berizin sesuai kelas rekanan.</p>"
 "<h2>Bagaimana FA Indonesia Membantu</h2>"
 "<p>Tim FA Indonesia membantu debitur memenuhi syarat pencairan: laporan keuangan dan CALK, rekonsiliasi pajak, koordinasi audit dan penilaian, serta pemenuhan covenant. RM dan Commercial Head yang punya fasilitas tertahan bisa merujuk debiturnya lewat halaman <a href=\"/mitra-rm-bank/\">kerja sama untuk RM bank</a>.</p>")
A2_FAQ = [
 ("Apa itu undisbursed loan?", "Fasilitas kredit yang sudah disetujui dan diperjanjikan bank, tetapi belum ditarik oleh debitur."),
 ("Berapa undisbursed loan perbankan Indonesia saat ini?", "Bank Indonesia mencatat sekitar Rp2.562,7 triliun per September 2026, atau 21,7% dari total plafon kredit."),
 ("Kenapa debitur tidak menarik fasilitas kredit?", "Penyebab umumnya adalah penundaan ekspansi, syarat pencairan yang belum terpenuhi, covenant keuangan yang tidak terpenuhi, proyek yang mundur, atau kebutuhan modal kerja yang turun."),
 ("Bagaimana mempercepat pencairan kredit yang sudah disetujui?", "Petakan syarat yang belum terpenuhi, kerjakan lebih dulu yang paling lama seperti audit dan penilaian KJPP, rapikan laporan keuangan untuk covenant, dan siapkan dokumen penggunaan dana sesuai format bank."),
]
art_page(A2, "Kredit Bank", "Undisbursed Loan: Cara Mempercepat Pencairan Kredit yang Sudah Disetujui | FA Indonesia",
  "Undisbursed Loan: Kenapa Fasilitas Kredit Belum Ditarik dan Cara Mempercepat Pencairan",
  "Undisbursed loan sekitar Rp2.562,7 triliun per September 2026. Penyebab fasilitas kredit belum ditarik, syarat pencairan yang paling sering tertahan, dan cara mempercepatnya.",
  6, a2, A2_FAQ,
  [("/mitra-rm-bank/", "Kerja Sama untuk RM dan Commercial Head"), ("/artikel/cara-mencapai-target-penyaluran-kredit-korporasi/", "Cara Mencapai Target Penyaluran Kredit Korporasi"),
   ("/artikel/jenis-opini-audit-dan-dampaknya-ke-bank/", "Jenis Opini Audit dan Dampaknya ke Bank"), ("/artikel/kapan-perusahaan-butuh-kjpp-jasa-penilai/", "Kapan Perusahaan Butuh KJPP")],
  [("Investortrust, 21 Oktober 2026: BI, undisbursed loan Rp2.562,7 triliun per September 2026", "https://investortrust.id/macro/120075/bi-kredit-yang-belum-tersalurkan-undisbursed-loan-tembus-rp-2562-7-triliun-per-september-2026"),
   ("Bisnis.com, 22 Juli 2026: Rp2.490 triliun kredit yang sudah disetujui belum dicairkan", "https://finansial.bisnis.com/read/20260722/11/1990121/rp2490-triliun-kredit-yang-sudah-disetujui-perbankan-tak-kunjung-dicairkan"),
   ("IDN Financials: Perbanas soal kredit mengendap Rp2.527 triliun", "https://www.idnfinancials.com/id/news/64368/kredit-mengendap-di-bank-rp2-527-triliun-perbanas-buka-suara")],
  "/mitra-rm-bank/", "Kerja Sama untuk RM Bank", WA_RM, RM_BOX2)

A3 = "cara-investor-mencari-target-akuisisi-indonesia"
a3 = (
 "<p>Perusahaan swasta yang menarik untuk diakuisisi jarang muncul di iklan. Pemiliknya tidak ingin karyawan, pemasok, atau bank tahu bahwa usahanya sedang ditawarkan. Akibatnya, investor yang hanya menunggu peluang datang sering melihat sisa pasar: usaha yang sudah lama dijual dan tidak laku.</p>"
 "<p>Tulisan ini merangkum dari mana peluang investasi perusahaan swasta di Indonesia biasanya datang, bagaimana menulis kriteria yang membuat penasihat bisa menyaring untuk Anda, dan regulasi yang perlu dicek sejak awal.</p>"
 "<h2>Sumber Peluang yang Paling Sering Menghasilkan Transaksi</h2>"
 "<h3>1. Penasihat dari Sisi Penjual</h3><p>Penasihat yang memegang mandat penjualan atau penggalangan dana sudah merapikan data perusahaan dan tahu motivasi pemiliknya. Peluang dari jalur ini biasanya paling cepat diuji.</p>"
 "<h3>2. Perusahaan yang Mentok di Batas Kredit</h3><p>Perusahaan yang plafon banknya tertahan rasio utang atau batas maksimum pemberian kredit sering membutuhkan ekuitas untuk tumbuh. Disiplin pelaporan ke bank membuat datanya relatif tertib.</p>"
 "<h3>3. Suksesi Usaha Keluarga</h3><p>Pemilik generasi pertama yang tidak punya penerus siap sering terbuka pada penjualan sebagian atau penuh, asalkan nama usaha dan karyawan terjaga.</p>"
 "<h3>4. Divestasi Grup</h3><p>Grup usaha yang menata ulang fokus bisnisnya melepas unit yang bukan inti. Unit seperti ini biasanya sudah punya laporan keuangan audit dan manajemen sendiri.</p>"
 "<h3>5. Jaringan Profesional</h3><p>KAP, KJPP, notaris, dan konsultan hukum korporasi tahu lebih awal ketika pemilik mulai serius. Rujukan dari jalur ini datang dengan konteks yang lebih lengkap.</p>"
 "<h2>Tulis Kriteria Investasi dalam Satu Halaman</h2>"
 + tbl(["Unsur", "Contoh"], [
   ("Sektor dan subsektor", "Rumah sakit tipe C dan D, klinik utama, distribusi alat kesehatan"),
   ("Wilayah", "Jawa Tengah dan DIY, atau seluruh Indonesia"),
   ("Ukuran", "Pendapatan Rp30 sampai 300 miliar, EBITDA positif minimal dua tahun"),
   ("Porsi kepemilikan", "Mayoritas, minoritas dengan hak tertentu, atau penuh"),
   ("Ukuran tiket", "Kisaran nilai investasi per transaksi"),
   ("Horizon dan jalur keluar", "3 sampai 7 tahun, penjualan strategis atau IPO"),
 ])
 + "<p>Kriteria yang jelas membuat penasihat bisa menolak peluang yang tidak cocok untuk Anda, sehingga yang sampai ke meja Anda sudah tersaring.</p>"
 "<h2>Saringan Awal Sebelum Masuk Due Diligence</h2><ul>"
 "<li>Laporan keuangan tiga tahun tersedia, diaudit atau setidaknya siap diaudit.</li>"
 "<li>EBITDA bisa dinormalisasi: biaya pribadi pemilik dan transaksi pihak berelasi terpisah.</li>"
 "<li>Data pajak bisa direkonsiliasi dengan laporan keuangan.</li>"
 "<li>Aset material atas nama perusahaan dan izin sektornya berlaku.</li>"
 "<li>Ada alasan transaksi yang masuk akal dari sisi pemilik.</li></ul>"
 "<p>Tanda bahaya yang lebih rinci ada di artikel <a href=\"/artikel/menilai-kesiapan-calon-investee-sebelum-term-sheet/\">7 red flag laporan keuangan calon investee</a>.</p>"
 "<h2>Regulasi yang Perlu Dicek Sejak Awal</h2><ul>"
 "<li><b>Bidang usaha untuk investor asing.</b> Keterbukaan bidang usaha bagi penanaman modal asing diatur Perpres 10 Tahun 2021 beserta perubahannya. Cek KBLI calon target sebelum negosiasi.</li>"
 "<li><b>Notifikasi KPPU.</b> Akuisisi saham yang nilai aset gabungannya melewati Rp2,5 triliun atau penjualan gabungannya melewati Rp5 triliun wajib diberitahukan ke KPPU paling lambat 30 hari kerja setelah efektif secara yuridis (PP 57 Tahun 2010 dan Peraturan KPPU 3 Tahun 2023). Untuk sesama bank, batas asetnya Rp20 triliun.</li>"
 "<li><b>Izin sektor.</b> Perubahan pengendali BPR memerlukan persetujuan OJK. Rumah sakit memerlukan kesinambungan izin operasional dan akreditasi.</li></ul>"
 "<h2>Bagaimana FA Indonesia Membantu</h2>"
 "<p>Tim FA Indonesia bekerja dari sisi perusahaan: menyiapkan laporan keuangan, normalisasi EBITDA, pajak, legal, dan data room sebelum perusahaan diperkenalkan. Investor yang mengirim kriterianya menerima teaser anonim untuk peluang yang cocok setelah NDA, tanpa biaya. Mandat aktif saat ini mencakup <a href=\"/rumah-sakit-dijual/\">rumah sakit swasta</a> dan <a href=\"/bpr-dijual/\">BPR dan BPRS</a>. Detailnya ada di halaman <a href=\"/mitra-investor/\">peluang untuk investor</a>.</p>")
A3_FAQ = [
 ("Di mana investor bisa menemukan target akuisisi perusahaan swasta di Indonesia?", "Sumber yang paling sering menghasilkan transaksi adalah penasihat dari sisi penjual, perusahaan yang mentok di batas kredit, suksesi usaha keluarga, divestasi grup, dan jaringan profesional seperti KAP, KJPP, dan notaris."),
 ("Apa yang perlu ditulis dalam kriteria investasi?", "Sektor, wilayah, ukuran pendapatan atau EBITDA, porsi kepemilikan, ukuran tiket, serta horizon dan jalur keluar."),
 ("Kapan akuisisi wajib dinotifikasi ke KPPU?", "Bila nilai aset gabungan melewati Rp2,5 triliun atau penjualan gabungan melewati Rp5 triliun, notifikasi paling lambat 30 hari kerja setelah transaksi efektif secara yuridis. Untuk sesama bank, batas asetnya Rp20 triliun."),
 ("Apakah investor asing bisa mengakuisisi perusahaan swasta Indonesia?", "Bisa sepanjang bidang usahanya terbuka untuk penanaman modal asing menurut Perpres 10 Tahun 2021 beserta perubahannya dan izin sektornya dipenuhi."),
]
art_page(A3, "Investor & IPO", "Cara Investor Mencari Target Akuisisi & Peluang Investasi di Indonesia | FA Indonesia",
  "Cara Investor Menemukan Target Akuisisi dan Peluang Investasi Perusahaan Swasta di Indonesia",
  "Cara investor dan PE menemukan target akuisisi perusahaan swasta Indonesia: sumber peluang, kriteria investasi satu halaman, saringan awal, dan regulasi PMA serta KPPU.",
  7, a3, A3_FAQ,
  [("/mitra-investor/", "Peluang untuk Investor"), ("/artikel/menilai-kesiapan-calon-investee-sebelum-term-sheet/", "7 Red Flag Laporan Keuangan Calon Investee"),
   ("/artikel/due-diligence-akuisisi-rumah-sakit-swasta/", "Due Diligence Akuisisi Rumah Sakit Swasta"), ("/artikel/valuasi-rumah-sakit-swasta/", "Valuasi Rumah Sakit Swasta")],
  [("Hukumonline, Persyaratan Notifikasi Merger dan Akuisisi ke KPPU", "https://www.hukumonline.com/klinik/a/persyaratan-notifikasi-merger-dan-akuisisi-ke-kppu--lt6ad98330ac876/"),
   ("Antara, BKPM: Perpres 10/2021 dorong investasi berdaya saing", "https://www.antaranews.com/berita/2015382/bkpm-perpres-10-2021-dorong-investasi-berdaya-saing")],
  "/mitra-investor/", "Peluang untuk Investor", WA_IV, IV_BOX)

A4 = "menilai-kesiapan-calon-investee-sebelum-term-sheet"
a4 = (
 "<p>Term sheet yang ditandatangani terlalu cepat sering harus dinegosiasi ulang setelah due diligence menemukan angka yang berbeda. Di perusahaan privat Indonesia, perbedaan itu hampir selalu berasal dari pola yang sama. Mengenalinya lebih awal menghemat biaya penasihat dan menjaga posisi tawar.</p>"
 "<h2>7 Red Flag Laporan Keuangan Calon Investee</h2>"
 + tbl(["Red Flag", "Cara Cek Cepat", "Dampak ke Valuasi"], [
   ("1. Laporan belum pernah diaudit", "Minta laporan audit tiga tahun dan surat representasi; bandingkan versi internal dengan versi bank", "Risiko penyajian ulang, diskon atau escrow"),
   ("2. EBITDA belum dinormalisasi", "Pisahkan gaji keluarga, biaya pribadi pemilik, dan pos tidak berulang", "Laba dasar valuasi bisa naik atau turun signifikan"),
   ("3. Transaksi pihak berelasi tanpa dokumen", "Daftar transaksi dengan perusahaan keluarga, harga, dan perjanjiannya", "Margin bisa berubah setelah transaksi dibuat wajar"),
   ('4. Piutang lama tanpa cadangan', f'Umur piutang dan matriks provisi kerugian kredit ekspektasian (<a href="{US}/psak/109/">PSAK 109</a>)', "Aset dan laba turun"),
   ('5. Pendapatan diakui terlalu awal', f'Uji kontrak dan kemajuan proyek terhadap <a href="{US}/psak/115/">PSAK 115</a>', "Pendapatan bergeser ke periode lain"),
   ('6. Sewa dan utang tersembunyi', f'Cek sewa jangka panjang (<a href="{US}/psak/116/">PSAK 116</a>), jaminan pribadi, dan utang ke pemegang saham', "Net debt naik, harga ekuitas turun"),
   ("7. Selisih dengan data pajak", "Rekonsiliasi omzet SPT dan Coretax dengan laporan keuangan", "Eksposur pajak menjadi indemnitas atau pengurang harga"),
 ])
 + "<h2>Quality of Earnings Sebelum Term Sheet</h2>"
 "<p>Tinjauan quality of earnings singkat sebelum term sheet tidak menggantikan due diligence penuh, tetapi cukup untuk menentukan kisaran harga yang realistis. Fokusnya tiga hal: laba yang berulang, modal kerja normal, dan utang bersih termasuk pos yang menyerupai utang.</p>"
 "<h2>Pertanyaan yang Sebaiknya Diajukan ke Pemilik</h2><ol>"
 "<li>Siapa yang menyusun laporan keuangan, dan apakah ada versi berbeda untuk bank atau pajak?</li>"
 "<li>Biaya apa saja yang sebenarnya untuk keperluan pribadi atau perusahaan lain?</li>"
 "<li>Aset apa yang dipakai usaha tetapi masih atas nama pribadi?</li>"
 "<li>Kontrak atau pelanggan mana yang menyumbang lebih dari 20% pendapatan?</li>"
 "<li>Apakah ada pemeriksaan pajak atau sengketa yang sedang berjalan?</li></ol>"
 "<h2>Calon Investee yang Datanya Sudah Dirapikan</h2>"
 f"<p>Sebagian besar red flag di atas bisa dibereskan sebelum perusahaan bertemu investor. Kalau calon investee belum diaudit, auditor berizin bisa dipilih lewat <a href=\"{CA}/\">CariAkuntan</a>. Tim FA Indonesia menyiapkan perusahaan dari sisi penjual: audit atau kesiapan audit, normalisasi EBITDA, rekonsiliasi pajak, dan data room. Investor yang ingin menerima peluang dengan data yang sudah dirapikan bisa mengirim kriterianya lewat halaman <a href=\"/mitra-investor/\">peluang untuk investor</a>.</p>")
A4_FAQ = [
 ("Apa red flag laporan keuangan calon investee yang paling sering?", "Laporan belum diaudit, EBITDA belum dinormalisasi, transaksi pihak berelasi tanpa dokumen, piutang lama tanpa cadangan, pendapatan diakui terlalu awal, sewa dan utang tersembunyi, serta selisih dengan data pajak."),
 ("Apa itu normalisasi EBITDA?", "Penyesuaian laba untuk memisahkan pos yang tidak mencerminkan usaha berjalan, misalnya biaya pribadi pemilik, gaji keluarga di atas atau di bawah pasar, dan biaya atau pendapatan tidak berulang."),
 ("Perlukah quality of earnings sebelum term sheet?", "Tinjauan singkat sangat membantu untuk menetapkan kisaran harga yang realistis, walaupun due diligence penuh tetap dilakukan setelah term sheet."),
 ("PSAK apa yang paling sering berpengaruh pada valuasi perusahaan privat?", "Yang sering muncul adalah PSAK 109 untuk cadangan piutang, PSAK 115 untuk pengakuan pendapatan, dan PSAK 116 untuk sewa."),
]
art_page(A4, "Investor & IPO", "Menilai Calon Investee Sebelum Term Sheet: 7 Red Flag | FA Indonesia",
  "Menilai Calon Investee Sebelum Term Sheet: 7 Red Flag Laporan Keuangan Perusahaan Privat",
  "Tujuh red flag laporan keuangan calon investee perusahaan privat Indonesia, cara cek cepatnya, dampaknya ke valuasi, dan pertanyaan untuk pemilik sebelum term sheet.",
  6, a4, A4_FAQ,
  [("/mitra-investor/", "Peluang untuk Investor"), ("/artikel/cara-investor-mencari-target-akuisisi-indonesia/", "Cara Investor Menemukan Target Akuisisi"),
   ("/artikel/due-diligence-investor-yang-perlu-disiapkan/", "Due Diligence Investor: Apa yang Diperiksa"), ("/artikel/private-equity-vs-utang-bank/", "Private Equity vs Utang Bank")],
  [], "/mitra-investor/", "Peluang untuk Investor", WA_IV, IV_BOX)

URLS = [PIV] + [f"/artikel/{a}/" for a in (A1, A2, A3, A4)]

# ================= 3. KOTAK DI HALAMAN TERKAIT =================
def strip_d(t): return re.sub(r"<!--fa-deal-->.*?<!--/fa-deal-->", "", t, flags=re.S)
INJ = {}
for parts in [("rumah-sakit-dijual",), ("bpr-dijual",), ("konsultan-persiapan-ipo",), ("artikel", "private-equity-vs-utang-bank"),
              ("artikel", "due-diligence-investor-yang-perlu-disiapkan"), ("artikel", "indikator-keuangan-rumah-sakit-yang-dilihat-investor"),
              ("artikel", "valuasi-rumah-sakit-swasta"), ("artikel", "due-diligence-akuisisi-rumah-sakit-swasta"),
              ("artikel", "menjual-rumah-sakit-persiapan-sisi-penjual"), ("artikel", "mengembangkan-usaha-tanpa-utang")]:
    INJ[parts] = IV_BOX
for parts in [("konsultan-kredit-distributor-importir",), ("artikel", "kredit-modal-kerja-kontraktor-berbasis-spk"), ("artikel", "kredit-bank-untuk-rumah-sakit-swasta"),
              ("artikel", "laporan-keuangan-untuk-kredit-bank"), ("artikel", "rasio-keuangan-yang-dilihat-bank"), ("artikel", "kmk-vs-kredit-investasi"),
              ("artikel", "kredit-sindikasi-kapan-dibutuhkan"), ("artikel", "jenis-opini-audit-dan-dampaknya-ke-bank"), ("artikel", "cara-memilih-kap-untuk-kredit-bank")]:
    INJ[parts] = RM_BOX2
for parts, b in INJ.items():
    p = P(*parts, "index.html")
    if not os.path.exists(p): print("skip", p); continue
    t = strip_d(rd(p))
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("</main>")
    wtxt(p, t[:k] + b + t[k:])

# footer: "Mitra Investor" setelah "Mitra Sekuritas"
FT = '<li><a href="/mitra-investor/">Mitra Investor</a></li>'
nf = 0
for d, _, fs in os.walk(FA):
    for f in fs:
        if not f.endswith(".html"): continue
        p = os.path.join(d, f); t = rd(p)
        if '/mitra-investor/">Mitra Investor' in t: continue
        k = t.find('Mitra Sekuritas</a></li>', max(t.find("<footer"), 0))
        if k < 0 or t.find("<footer") < 0: continue
        k += len('Mitra Sekuritas</a></li>')
        wtxt(p, t[:k] + FT + t[k:]); nf += 1
print("footer", nf)

# kartu Eksplor
ip = P("artikel", "index.html"); t = strip_d(rd(ip))
CARD = '<!--fa-deal--><a class="card2" href="/artikel/{s}/"><b>{h}</b><span>{d}</span></a><!--/fa-deal-->'
for tid, s, h, d in [
    ("t-kredit-bank", A1, "Cara Mencapai Target Penyaluran Kredit Korporasi", "Hitung mundur target ke jumlah prospek, titik yang paling sering menahan, dan yang bisa dilakukan RM serta Commercial Head."),
    ("t-kredit-bank", A2, "Undisbursed Loan: Cara Mempercepat Pencairan Kredit", "Kenapa fasilitas yang sudah disetujui belum ditarik, syarat pencairan yang paling sering tertahan, dan cara mengejarnya."),
    ("t-investor-ipo", A3, "Cara Investor Menemukan Target Akuisisi di Indonesia", "Sumber peluang investasi perusahaan swasta, kriteria satu halaman, saringan awal, regulasi PMA dan KPPU."),
    ("t-investor-ipo", A4, "Menilai Calon Investee Sebelum Term Sheet: 7 Red Flag", "Red flag laporan keuangan perusahaan privat, cara cek cepat, dan dampaknya ke valuasi.")]:
    k = t.find(f'id="{tid}"')
    if k < 0: print("topik tidak ada", tid); continue
    k = t.find('<div class="cards2">', k) + len('<div class="cards2">')
    t = t[:k] + CARD.format(s=s, h=E(h), d=E(d)) + t[k:]
wtxt(ip, t)

# sitemap
sm = re.sub(r"<!--fa-deal-->.*?<!--/fa-deal-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-deal-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for u in URLS) + "<!--/fa-deal-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)

# llms.txt
ll = re.sub(r"\n## Untuk Investor dan Commercial Head Bank.*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + ("\n\n## Untuk Investor dan Commercial Head Bank\n"
  "- Investor private equity, family office, pembeli strategis, dan investor asing yang mencari investee atau target akuisisi perusahaan swasta Indonesia: peluang disaring, data siap due diligence, setelah NDA, tanpa biaya untuk investor → https://faindonesia.co.id/mitra-investor/\n"
  "- RM, junior marketing kredit, dan Dept Head Commercial bank yang mencari prospek debitur korporasi siap cair dan ingin mempercepat pencairan fasilitas yang belum ditarik (undisbursed loan) → https://faindonesia.co.id/mitra-rm-bank/\n"
  "- Artikel: " + " , ".join(f"https://faindonesia.co.id/artikel/{a}/" for a in (A1, A2, A3, A4)) + "\n"
  "- Ekosistem: cariakuntan.com (memilih KAP, KJPP, konsultan pajak berizin untuk syarat bank dan due diligence), updatesak.com (cek kepatuhan PSAK terbaru)\n")
wtxt(P("llms.txt"), ll)
print("deal selesai:", URLS)
