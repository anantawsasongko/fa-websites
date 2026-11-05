# -*- coding: utf-8 -*-
"""Artikel dari Google Trends Indonesia Bisnis & Keuangan (3 Nov 2026: komisaris, kenapa ihsg turun, kebangkrutan, inflasi), versi FA:
- /artikel/pertanyaan-komisaris-atas-laporan-keuangan/ : pertanyaan wajib komisaris atas LK (topik CFO & Tata Kelola)
- /artikel/ihsg-turun-persiapan-perusahaan-privat-cari-investor/ : pasar turun, investor selektif (topik Investor & IPO)
- /artikel/laba-naik-kredit-ditolak-cara-bank-membaca-laba-utang-arus-kas/ : laba vs kas di mata bank (topik Kredit Bank)
- kartu di Eksplor, sitemap, llms.txt
Helper diambil dari fa_mitra_20261027.py. Idempoten (penanda fa-trend).
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_mitra_20261027.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. MITRA RM BANK")]
_src = _src.replace('TODAY = "2026-10-27"', 'TODAY = "2026-11-03"').replace("27 Oktober 2026", "3 November 2026")
exec(compile(_src, "fa_mitra_helpers", "exec"))

# ================= 1. KOMISARIS =================
S1 = "pertanyaan-komisaris-atas-laporan-keuangan"
body1 = (
 "<p>Menurut Pasal 108 Undang-Undang Nomor 40 Tahun 2007 tentang Perseroan Terbatas, Dewan Komisaris melakukan pengawasan atas kebijakan pengurusan dan jalannya pengurusan perseroan, serta memberi nasihat kepada Direksi. "
 "Pasal 114 menambahkan bahwa setiap anggota Dewan Komisaris wajib menjalankan tugas itu dengan itikad baik dan kehati-hatian, dan dapat ikut bertanggung jawab secara pribadi atas kerugian perseroan bila lalai. "
 "Artinya, menerima laporan keuangan lalu menyetujuinya tanpa bertanya bukan pilihan yang aman, baik di PT privat maupun di perusahaan yang sedang bersiap IPO.</p>"
 "<p>Tim kami merangkum enam kelompok pertanyaan yang paling sering membuka masalah sejak dini. Pertanyaan ini tidak menuntut komisaris menjadi akuntan, hanya menuntut keberanian bertanya dan meminta data pendukung.</p>"
 "<h2>Arus Kas Dibanding Laba</h2>"
 "<p>Laba bisa naik sementara kas menipis. Penyebab paling umum adalah piutang yang membengkak, persediaan menumpuk, atau pendapatan yang diakui sebelum kas diterima. Pertanyaan yang layak diajukan:</p>"
 "<ul><li>Berapa arus kas operasi dibanding laba bersih tahun ini, dan kenapa selisihnya sebesar itu?</li>"
 "<li>Apakah ada pendapatan besar yang diakui menjelang tutup tahun, dan kapan kasnya benar-benar masuk?</li>"
 "<li>Apakah dividen atau ekspansi tahun depan dibiayai kas operasi atau utang baru?</li></ul>"
 "<h2>Utang Jatuh Tempo, Covenant, dan Piutang Menua</h2>"
 "<p>Banyak kasus kesulitan keuangan, bahkan kebangkrutan, berawal dari utang yang jatuh tempo bersamaan dengan kas yang tertahan di piutang. Dua area ini sebaiknya dibaca bersama.</p>"
 + tbl(["Area", "Pertanyaan Komisaris", "Data yang Diminta"], [
   ("Jadwal Utang", "Berapa utang yang jatuh tempo dalam 12 bulan dan dari mana sumber pelunasannya?", "Jadwal jatuh tempo per fasilitas dan proyeksi arus kas bulanan"),
   ("Covenant Bank", "Apakah ada rasio covenant yang mendekati batas, misalnya DSCR atau utang terhadap ekuitas?", "Perhitungan covenant per tanggal laporan dan proyeksinya"),
   ("Piutang Menua", "Berapa porsi piutang di atas 90 hari, dan apakah cadangan kerugiannya memadai?", "Aging piutang per pelanggan dan riwayat penagihan"),
   ("Pelanggan Utama", "Apakah ada konsentrasi piutang pada satu atau dua pelanggan?", "Daftar sepuluh pelanggan terbesar dan saldo piutangnya"),
 ])
 + "<p>Pelanggaran covenant dapat membuat utang jangka panjang harus disajikan sebagai utang jangka pendek. Dampaknya terasa ke rasio lancar dan ke kepercayaan bank, jadi lebih baik diketahui komisaris sebelum tanggal laporan, bukan sesudahnya.</p>"
 "<h2>Transaksi dengan Pihak Berelasi</h2>"
 "<p>Di perusahaan keluarga, transaksi dengan perusahaan lain milik pemegang saham hampir selalu ada: sewa gedung, pinjaman antarperusahaan, pembelian dari pemasok yang dimiliki kerabat. Transaksi seperti ini sah, tetapi perlu wajar dan diungkapkan. Tanyakan:</p>"
 "<ul><li>Daftar lengkap pihak berelasi dan saldo piutang serta utang dengan masing-masing.</li>"
 "<li>Apakah harga dan syaratnya setara dengan transaksi dengan pihak ketiga?</li>"
 "<li>Apakah ada pinjaman ke pemegang saham atau afiliasi yang tidak berbunga dan tanpa jadwal pelunasan?</li></ul>"
 "<p>Bagi calon emiten, area ini termasuk yang paling diperhatikan penjamin emisi dan investor, sehingga merapikannya sejak awal menghemat waktu persiapan IPO.</p>"
 "<h2>Opini Audit dan Management Letter</h2>"
 "<p>Opini audit hanya satu halaman, padahal informasi yang lebih berguna sering ada di management letter, yaitu surat auditor tentang kelemahan pengendalian internal yang ditemukan selama audit.</p>"
 + flow([
   ("Baca Opininya", "Wajar tanpa pengecualian, wajar dengan pengecualian, tidak wajar, atau tidak menyatakan pendapat. Tanyakan alasan bila bukan yang pertama."),
   ("Cek Paragraf Penekanan", "Perhatikan paragraf tentang ketidakpastian material kelangsungan usaha atau hal penting lain."),
   ("Minta Management Letter", "Komisaris berhak meminta salinannya, bukan hanya ringkasan dari Direksi."),
   ("Tagih Tindak Lanjut", "Setiap temuan perlu penanggung jawab dan tenggat. Cek apakah temuan tahun lalu masih muncul."),
 ])
 + "<p>Temuan yang berulang dari tahun ke tahun adalah tanda bahwa pengendalian internal belum dianggap prioritas. Untuk memahami dampak tiap jenis opini, baca <a href=\"/artikel/jenis-opini-audit-dan-dampaknya-ke-bank/\">jenis opini audit dan dampaknya ke bank</a>.</p>"
 "<h2>Peran Komite Audit</h2>"
 "<p>Di perusahaan terbuka, Komite Audit wajib ada dan membantu Dewan Komisaris menelaah laporan keuangan, independensi auditor, dan pengendalian internal. PT privat tidak diwajibkan, tetapi membentuk komite audit sederhana, atau setidaknya menunjuk satu anggota komisaris yang paham akuntansi, membuat pertanyaan di atas dibahas rutin, bukan hanya saat RUPS tahunan.</p>"
 "<p>Untuk calon emiten, kebiasaan ini sekaligus menjadi latihan tata kelola sebelum Komisaris Independen dan Komite Audit resmi dibentuk. Informasi tentang peran dan pencarian anggotanya ada di halaman <a href=\"/komite-audit-komisaris-independen/\">Komite Audit dan Komisaris Independen</a> serta <a href=\"/bursa-komite-audit/\">Bursa Komite Audit</a>.</p>"
 "<p>Sebagai saringan awal, komisaris dapat memasukkan angka laporan keuangan ke <a href=\"/kalkulator-rasio-keuangan/\">Kalkulator Rasio Keuangan</a> untuk melihat rasio likuiditas, solvabilitas, dan skor Altman Z sebagai sinyal awal risiko kesulitan keuangan. Hasilnya bukan kesimpulan, tetapi bahan pertanyaan untuk rapat berikutnya dengan Direksi.</p>"
)
faq1 = [
 ("Apa dasar hukum tugas pengawasan Dewan Komisaris?", "Pasal 108 UU 40/2007 tentang Perseroan Terbatas mengatur pengawasan atas kebijakan dan jalannya pengurusan serta pemberian nasihat kepada Direksi. Pasal 114 mengatur kewajiban itikad baik, kehati-hatian, dan tanggung jawab pribadi bila lalai."),
 ("Apakah komisaris PT privat perlu membaca management letter?", "Sebaiknya ya. Management letter memuat kelemahan pengendalian internal yang ditemukan auditor, dan sering lebih informatif daripada opini audit itu sendiri."),
 ("Apakah PT privat wajib punya Komite Audit?", "Tidak diwajibkan seperti emiten. Namun komite audit sederhana atau komisaris yang paham akuntansi membantu pengawasan berjalan rutin, dan menjadi persiapan tata kelola bila perusahaan berencana IPO."),
 ("Pertanyaan apa yang paling mendesak bila waktu rapat terbatas?", "Mulai dari arus kas operasi dibanding laba, jadwal utang jatuh tempo 12 bulan beserta posisi covenant, dan porsi piutang di atas 90 hari."),
]
art_page(S1, "CFO & Tata Kelola", "Pertanyaan yang Wajib Diajukan Komisaris atas Laporan Keuangan | FA Indonesia",
         "Pertanyaan yang Wajib Diajukan Komisaris atas Laporan Keuangan",
         "Daftar pertanyaan komisaris PT privat dan calon emiten atas laporan keuangan: arus kas vs laba, utang dan covenant, piutang menua, pihak berelasi, opini audit, management letter, dan komite audit.",
         7, body1, faq1,
         [("/komite-audit-komisaris-independen/", "Komite Audit dan Komisaris Independen"), ("/bursa-komite-audit/", "Bursa Komite Audit"),
          ("/artikel/komite-audit-tugas-dan-syarat/", "Komite Audit Perusahaan Tbk: Tugas dan Syarat"),
          ("/artikel/syarat-komisaris-independen/", "Syarat Komisaris Independen"),
          ("/artikel/jenis-opini-audit-dan-dampaknya-ke-bank/", "Jenis Opini Audit dan Dampaknya ke Bank")],
         [("UU 40/2007 Pasal 114 (pasal.id)", "https://pasal.id/peraturan/uu/uu-no-40-tahun-2007/pasal-114"),
          ("Hukumonline: Bolehkah Dewan Komisaris Ikut Mengurus Operasional PT", "https://www.hukumonline.com/klinik/a/bolehkah-dewan-komisaris-ikut-mengurus-operasional-pt-cl4600/")],
         "/kalkulator-rasio-keuangan/", "Cek Rasio Keuangan",
         "Halo FA Indonesia, saya komisaris perusahaan dan ingin berdiskusi soal penelaahan laporan keuangan dan pembentukan komite audit.")

# ================= 2. IHSG TURUN, INVESTOR SELEKTIF =================
S2 = "ihsg-turun-persiapan-perusahaan-privat-cari-investor"
body2 = (
 "<p>Pertanyaan \"kenapa IHSG turun\" sedang banyak dicari. Indeks bursa memang sedang melemah dalam beberapa pekan terakhir. "
 "Bagi pemilik perusahaan privat yang sedang mencari investor, pergerakan pasar saham ini terasa tidak langsung tetapi nyata: investor menjadi lebih selektif, proses due diligence lebih panjang, dan angka valuasi lebih konservatif.</p>"
 "<p>Tulisan ini tidak membahas arah pasar. Fokusnya adalah apa yang bisa disiapkan perusahaan supaya tetap layak dibicarakan ketika investor sedang berhati-hati.</p>"
 "<h2>Kenapa Valuasi Makin Konservatif Saat Pasar Turun</h2>"
 "<p>Investor ekuitas swasta dan investor strategis membandingkan harga perusahaan privat dengan perusahaan sejenis yang tercatat di bursa. Ketika harga saham turun, beberapa hal ikut bergeser:</p>"
 + gain([
   ("Multiple Pembanding Turun", "Kelipatan EV/EBITDA perusahaan tercatat yang dijadikan acuan ikut turun, sehingga nilai perusahaan privat yang dihitung dengan metode pasar juga turun."),
   ("Tingkat Diskonto Naik", "Persepsi risiko yang lebih tinggi menaikkan biaya modal. Dalam metode DCF, arus kas masa depan yang sama menghasilkan nilai kini yang lebih kecil."),
   ("Jalur Keluar Lebih Jauh", "Investor yang berencana keluar lewat IPO melihat jendela pencatatan lebih tidak pasti, lalu meminta harga masuk yang lebih rendah atau perlindungan tambahan."),
   ("Modal Lebih Dijaga", "Dana yang tersedia diprioritaskan untuk perusahaan dengan data paling rapi dan risiko paling mudah diukur."),
 ])
 + "<p>Akibatnya, perusahaan dengan kinerja sama bisa mendapat penawaran yang berbeda jauh hanya karena kualitas datanya berbeda.</p>"
 "<h2>Data yang Dicek Investor</h2>"
 + tbl(["Area", "Yang Diminta Investor", "Kenapa Penting"], [
   ("Laporan Keuangan Audit", "Dua sampai tiga tahun, diaudit KAP, sebaiknya dengan opini wajar tanpa pengecualian", "Menjadi dasar semua angka lain dalam negosiasi"),
   ("EBITDA Normalisasi", "EBITDA setelah dikoreksi pos sekali terjadi, gaji pemilik yang tidak wajar, dan transaksi pihak berelasi", "Dasar perhitungan multiple dan harga"),
   ("Arus Kas", "Arus kas operasi, kebutuhan modal kerja, dan belanja modal rutin", "Menunjukkan apakah laba benar-benar menjadi kas"),
   ("Utang dan Komitmen", "Jadwal utang, covenant, jaminan pribadi pemilik, dan kontrak material", "Memengaruhi nilai ekuitas yang tersisa untuk pemegang saham"),
   ("Tata Kelola", "Struktur organ perseroan, pemisahan keuangan pribadi dan usaha, kebijakan pihak berelasi", "Mengukur risiko setelah investor masuk"),
 ])
 + "<p>Daftar dokumen yang lebih rinci ada di artikel <a href=\"/artikel/due-diligence-investor-yang-perlu-disiapkan/\">due diligence investor yang perlu disiapkan</a>.</p>"
 "<h2>Menyiapkan Valuasi yang Bisa Dipertahankan</h2>"
 "<p>Di pasar yang sedang turun, angka valuasi yang terlalu optimistis justru menghentikan pembicaraan lebih awal. Pendekatan yang lebih berguna adalah menyiapkan rentang nilai dengan asumsi yang jelas, sehingga negosiasi bergerak di atas data, bukan perasaan.</p>"
 + flow([
   ("Rapikan Angka Historis", "Pastikan laporan keuangan konsisten dengan SPT dan pembukuan, lalu susun koreksi normalisasi EBITDA."),
   ("Susun Proyeksi Realistis", "Proyeksi tiga sampai lima tahun dengan asumsi pertumbuhan yang bisa dijelaskan dari data historis."),
   ("Hitung Beberapa Metode", "DCF dan multiple pembanding, lalu bandingkan hasilnya dalam rentang."),
   ("Uji Sensitivitas", "Lihat dampak perubahan tingkat diskonto dan pertumbuhan terhadap nilai."),
   ("Siapkan Data Room", "Dokumen tersusun rapi sebelum investor pertama meminta."),
 ])
 + "<p>Simulasi awal bisa dilakukan dengan <a href=\"/kalkulator-valuasi-dcf/\">Kalkulator Valuasi DCF</a>. Untuk penilaian yang akan dipakai dalam negosiasi atau transaksi, tim kami mendampingi lewat <a href=\"/jasa-valuasi-usaha/\">Jasa Valuasi Usaha</a>, dan bila diperlukan laporan penilaian resmi, dikerjakan oleh KJPP. "
 "Perusahaan yang sudah siap juga dapat diperkenalkan kepada investor melalui halaman <a href=\"/mitra-investor/\">peluang investasi dan target akuisisi</a>, setelah pemilik setuju dan NDA berjalan.</p>"
 "<h2>Opsi Pendanaan Alternatif</h2>"
 "<p>Bila kebutuhannya modal kerja atau investasi dengan arus kas yang bisa diprediksi, kredit bank sering lebih masuk akal daripada menjual saham di valuasi rendah. Pemilik tetap memegang kendali, dan pembicaraan dengan investor bisa ditunda sampai kondisi lebih baik.</p>"
 "<ul><li>Kredit modal kerja untuk kontrak atau pesanan yang sudah ada.</li>"
 "<li>Kredit investasi untuk mesin, gedung, atau cabang baru.</li>"
 "<li>Kombinasi: kredit bank sekarang, lalu ekuitas setelah kinerja dan pasar membaik.</li></ul>"
 "<p>Pertimbangan memilih antara investor dan bank dibahas di <a href=\"/artikel/modal-usaha-dari-investor-atau-bank/\">modal usaha dari investor atau bank</a>, dan pendampingan pengajuan kredit ada di <a href=\"/konsultan-kredit-bank/\">Konsultan Kredit Bank</a>. "
 "Keputusan akhir tetap ada di investor atau bank, tetapi data yang rapi membuat perusahaan lebih mudah dinilai dengan adil.</p>"
)
faq2 = [
 ("Apakah IHSG turun memengaruhi valuasi perusahaan yang tidak tercatat di bursa?", "Secara tidak langsung, ya. Investor memakai perusahaan tercatat sebagai pembanding, dan persepsi risiko yang lebih tinggi menaikkan tingkat diskonto, sehingga nilai perusahaan privat cenderung dihitung lebih konservatif."),
 ("Apa itu EBITDA normalisasi?", "EBITDA yang sudah dikoreksi pos sekali terjadi, biaya atau gaji pemilik yang tidak wajar, dan transaksi pihak berelasi yang tidak setara harga pasar, sehingga mencerminkan kemampuan laba usaha yang berulang."),
 ("Apakah sebaiknya menunda cari investor saat pasar turun?", "Tergantung kebutuhan dana. Bila kebutuhannya bisa dipenuhi kredit bank, menunda penjualan saham dapat menghindari valuasi rendah. Waktu tunda itu bisa dipakai untuk merapikan laporan audit dan tata kelola."),
 ("Berapa tahun laporan keuangan audit yang biasanya diminta investor?", "Umumnya dua sampai tiga tahun terakhir, ditambah laporan interim tahun berjalan bila prosesnya berlangsung di tengah tahun."),
]
art_page(S2, "Investor & IPO", "IHSG Turun, Investor Makin Selektif: Persiapan Perusahaan Privat Sebelum Cari Investor | FA Indonesia",
         "IHSG Turun, Investor Makin Selektif: Yang Harus Disiapkan Perusahaan Privat Sebelum Cari Investor",
         "Saat IHSG turun, investor lebih selektif dan valuasi lebih konservatif. Data yang dicek investor, EBITDA normalisasi, cara menyiapkan valuasi, dan opsi kredit bank untuk perusahaan privat.",
         7, body2, faq2,
         [("/jasa-valuasi-usaha/", "Jasa Valuasi Usaha"), ("/kalkulator-valuasi-dcf/", "Kalkulator Valuasi DCF"),
          ("/mitra-investor/", "Peluang Investasi dan Target Akuisisi"),
          ("/artikel/due-diligence-investor-yang-perlu-disiapkan/", "Due Diligence Investor yang Perlu Disiapkan"),
          ("/artikel/valuasi-perusahaan-swasta-dcf-multiple-ebitda/", "Valuasi Perusahaan Swasta: DCF dan Multiple EBITDA"),
          ("/artikel/modal-usaha-dari-investor-atau-bank/", "Modal Usaha dari Investor atau Bank")],
         [],
         "/kalkulator-valuasi-dcf/", "Coba Kalkulator Valuasi DCF",
         "Halo FA Indonesia, perusahaan kami sedang mencari investor dan ingin menyiapkan laporan keuangan serta valuasi yang realistis.")

# ================= 3. LABA NAIK TAPI KREDIT DITOLAK =================
S3 = "laba-naik-kredit-ditolak-cara-bank-membaca-laba-utang-arus-kas"
body3 = (
 "<p>Salah satu keluhan yang paling sering kami dengar dari pemilik usaha: laba tahun lalu naik, tetapi pengajuan kredit ditolak atau plafonnya dipotong. "
 "Penjelasannya hampir selalu sama. Bank tidak membayar pinjaman dari laba, melainkan dari kas. Analis kredit membaca laba, utang, dan arus kas sebagai satu cerita, dan cerita itu bisa berbeda dari laporan laba rugi saja.</p>"
 "<h2>Laba Tidak Sama dengan Kas</h2>"
 "<p>Laba dihitung dengan dasar akrual: penjualan diakui saat barang dikirim atau jasa selesai, bukan saat dibayar. Karena itu laba bisa naik sementara kas justru tertahan di:</p>"
 "<ul><li>Piutang pelanggan yang makin lama dibayar.</li>"
 "<li>Persediaan yang dibeli lebih banyak untuk mengejar penjualan.</li>"
 "<li>Uang muka proyek atau pembelian aset yang dibayar dari kas operasional.</li></ul>"
 "<p>Bila arus kas operasi jauh di bawah laba bersih selama dua tahun berturut-turut, analis akan bertanya dari mana sebenarnya cicilan akan dibayar.</p>"
 "<p>Contoh sederhana: sebuah distributor mencatat laba bersih naik dari Rp2 miliar menjadi Rp3 miliar. Pada periode yang sama, piutang naik Rp2,5 miliar karena pelanggan besar meminta tempo lebih panjang, dan persediaan naik Rp1 miliar untuk mengantisipasi kenaikan harga. "
 "Hasilnya, arus kas operasi justru negatif. Di mata analis, perusahaan ini sedang membiayai pertumbuhannya dari utang pemasok dan saldo bank, sehingga tambahan kredit dinilai berisiko meskipun laporan laba ruginya terlihat sehat. "
 "Angka contoh ini ilustratif, tetapi polanya sangat sering kami temui pada usaha yang sedang tumbuh cepat.</p>"
 "<h2>Tiga Ukuran Utama yang Dihitung Bank</h2>"
 + tbl(["Ukuran", "Cara Membaca", "Yang Membuat Analis Ragu"], [
   ("DSCR", "Kas yang tersedia untuk membayar utang dibagi cicilan pokok dan bunga dalam setahun", "Hasil mendekati atau di bawah 1 kali, artinya kas pas-pasan atau kurang untuk membayar cicilan"),
   ("Utang terhadap EBITDA", "Berapa tahun EBITDA yang dibutuhkan untuk melunasi seluruh utang berbunga", "Angka tinggi karena utang bertambah lebih cepat daripada EBITDA"),
   ("Siklus Modal Kerja", "Hari piutang ditambah hari persediaan dikurangi hari utang usaha", "Siklus makin panjang, sehingga kebutuhan modal kerja naik lebih cepat dari penjualan"),
 ])
 + "<p>Batas yang dipakai berbeda antar bank dan sektor, jadi angka di atas sebaiknya dibaca sebagai arah, bukan patokan pasti. Hitung DSCR usaha Anda dengan <a href=\"/kalkulator-dscr/\">Kalkulator DSCR</a>, dan baca rasio lainnya di <a href=\"/artikel/rasio-keuangan-yang-dilihat-bank/\">rasio keuangan yang dilihat bank</a>.</p>"
 "<h2>Bagaimana Inflasi Biaya Menekan Arus Kas</h2>"
 "<p>BPS mencatat inflasi September 2026 sebesar 0,30% secara bulanan dan 3,28% secara tahunan, dengan pendorong utama kelompok makanan, minuman, dan tembakau. "
 "Angka ini terlihat moderat, tetapi bagi usaha dengan bahan baku pangan, kemasan, atau upah yang ikut menyesuaikan, dampaknya muncul di tiga tempat sekaligus:</p>"
 + gain([
   ("Margin Tergerus", "Kenaikan biaya tidak selalu bisa langsung diteruskan ke harga jual, terutama pada kontrak harga tetap."),
   ("Modal Kerja Membengkak", "Nilai persediaan dengan volume yang sama menjadi lebih mahal, sehingga lebih banyak kas tertahan di gudang."),
   ("Proyeksi Dipertanyakan", "Analis akan menguji apakah proyeksi sudah memasukkan kenaikan biaya, atau masih memakai margin tahun lalu."),
 ])
 + "<p>Usaha yang laba tahun lalunya naik karena harga jual sempat naik lebih dulu bisa terlihat baik di laporan laba rugi, padahal arus kas tahun berjalan mulai tertekan. Analis yang teliti akan melihat celah ini dari laporan interim dan mutasi rekening.</p>"
 "<h2>Cara Menyiapkan Pengajuan yang Lebih Mudah Dibaca Analis</h2>"
 + flow([
   ("Rekonsiliasi Laba ke Kas", "Jelaskan selisih laba dan arus kas operasi: piutang, persediaan, dan pos nonkas."),
   ("Rapikan Piutang", "Tagih piutang lama, cadangkan yang sulit tertagih, dan siapkan aging per pelanggan."),
   ("Hitung Kebutuhan Riil", "Plafon modal kerja dihitung dari siklus modal kerja, bukan sekadar persentase omzet."),
   ("Uji Proyeksi", "Masukkan skenario kenaikan biaya dan lihat apakah DSCR tetap memadai."),
   ("Lengkapi Dokumen", "Laporan keuangan, SPT, mutasi rekening, dan rincian utang yang konsisten satu sama lain."),
 ])
 + "<p>Penyebab penolakan lain yang sering terjadi, seperti data omzet yang berbeda dengan SPT atau riwayat SLIK, dibahas di <a href=\"/artikel/alasan-kredit-bank-ditolak/\">alasan kredit bank ditolak</a>. "
 "Untuk perkiraan plafon yang realistis sebelum bertemu bank, gunakan <a href=\"/cek-kapasitas-kredit/\">Cek Kapasitas Kredit</a>. "
 "Tim kami tidak bisa menjamin kredit disetujui karena keputusan sepenuhnya ada di bank, tetapi berkas yang menjawab pertanyaan analis sejak awal biasanya diproses lebih lancar.</p>"
)
faq3 = [
 ("Kenapa kredit ditolak padahal laba naik?", "Bank menilai kemampuan membayar dari arus kas, bukan dari laba saja. Laba bisa naik sementara kas tertahan di piutang dan persediaan, sehingga DSCR tetap rendah."),
 ("Berapa DSCR yang biasanya diharapkan bank?", "Tiap bank dan sektor punya batas sendiri. Secara umum, DSCR di atas 1 kali berarti kas cukup untuk membayar cicilan, dan bank biasanya meminta ruang aman di atas angka itu."),
 ("Apa hubungan inflasi dengan pengajuan kredit?", "Inflasi biaya menekan margin dan menaikkan kebutuhan modal kerja. Analis akan menguji apakah proyeksi sudah memperhitungkan kenaikan biaya tersebut."),
 ("Apa yang bisa diperbaiki sebelum mengajukan ulang?", "Rekonsiliasi laba ke kas, rapikan dan tagih piutang lama, hitung kebutuhan modal kerja dari siklusnya, dan pastikan laporan keuangan konsisten dengan SPT dan mutasi rekening."),
]
art_page(S3, "Kredit Bank", "Laba Naik tapi Kredit Ditolak: Cara Bank Membaca Laba, Utang, dan Arus Kas | FA Indonesia",
         "Laba Naik tapi Kredit Ditolak: Cara Bank Membaca Laba, Utang, dan Arus Kas",
         "Kenapa kredit bisa ditolak padahal laba naik? Cara analis bank membaca DSCR, utang terhadap EBITDA, siklus modal kerja, laba vs kas, dan dampak inflasi biaya 2026.",
         7, body3, faq3,
         [("/kalkulator-dscr/", "Kalkulator DSCR"), ("/cek-kapasitas-kredit/", "Cek Kapasitas Kredit"),
          ("/artikel/alasan-kredit-bank-ditolak/", "Alasan Kredit Bank Ditolak"),
          ("/artikel/rasio-keuangan-yang-dilihat-bank/", "Rasio Keuangan yang Dilihat Bank"),
          ("/artikel/dscr-adalah-cara-menghitung-kredit-bank/", "DSCR Adalah: Cara Menghitung untuk Kredit Bank")],
         [("Kontan: BPS, Inflasi Naik Menjadi 0,30% pada September 2026", "https://nasional.kontan.co.id/news/bps-inflasi-naik-menjadi-030-pada-september-2026")],
         "/kalkulator-dscr/", "Hitung DSCR",
         "Halo FA Indonesia, laba usaha kami naik tetapi pengajuan kredit ditolak, kami ingin berdiskusi soal arus kas dan kemampuan bayar.")

# ================= KARTU EKSPLOR, SITEMAP, LLMS =================
CARDS = [
 ("t-cfo-tata-kelola", S1, "Pertanyaan yang Wajib Diajukan Komisaris atas Laporan Keuangan", "Arus kas vs laba, utang dan covenant, piutang menua, pihak berelasi, opini audit, dan peran komite audit."),
 ("t-investor-ipo", S2, "IHSG Turun, Investor Makin Selektif: Persiapan Sebelum Cari Investor", "Kenapa valuasi makin konservatif, data yang dicek investor, dan opsi pendanaan alternatif."),
 ("t-kredit-bank", S3, "Laba Naik tapi Kredit Ditolak: Cara Bank Membaca Laba, Utang, dan Arus Kas", "DSCR, utang terhadap EBITDA, siklus modal kerja, dan dampak inflasi biaya."),
]
def strip_t(t): return re.sub(r"<!--fa-trend-->.*?<!--/fa-trend-->\n?", "", t, flags=re.S)
ip = P("artikel", "index.html"); t = strip_t(rd(ip))
for tid, slug, h, d in CARDS:
    k = t.find(f'id="{tid}"')
    if k < 0: k = t.find('id="t-kredit-bank"')  # topik terdekat
    k = t.find('<div class="cards2">', k) + len('<div class="cards2">')
    t = t[:k] + f'<!--fa-trend--><a class="card2" href="/artikel/{slug}/"><b>{E(h)}</b><span>{E(d)}</span></a><!--/fa-trend-->' + t[k:]
wtxt(ip, t)
sm = strip_t(rd(P("sitemap.xml")))
urls = "".join(f"<url><loc>{D}/artikel/{s}/</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for s in (S1, S2, S3))
sm = sm.replace("</urlset>", f"<!--fa-trend-->\n{urls}<!--/fa-trend-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
LL = [("Pertanyaan Komisaris atas Laporan Keuangan", S1, "pertanyaan wajib komisaris PT privat dan calon emiten atas laporan keuangan"),
      ("IHSG Turun dan Persiapan Cari Investor", S2, "valuasi konservatif saat pasar turun, data yang dicek investor, opsi kredit bank"),
      ("Laba Naik tapi Kredit Ditolak", S3, "cara bank membaca laba, utang, arus kas, DSCR, dan inflasi biaya")]
ll = rd(P("llms.txt"))
for name, s, d in LL: ll = re.sub(r"\n- \[" + re.escape(name) + r"\].*", "", ll)
wtxt(P("llms.txt"), ll.rstrip("\n") + "\n" + "".join(f"- [{n}]({D}/artikel/{s}/): {d}\n" for n, s, d in LL))
print("trending FA:", S1, S2, S3)
