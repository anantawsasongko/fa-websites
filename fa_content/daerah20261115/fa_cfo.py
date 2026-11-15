# -*- coding: utf-8 -*-
"""FA Indonesia: 4 artikel Fractional CFO (Bekasi, Medan, Balikpapan, Bandung). Sudut: diagnosis dan pendampingan."""
from _k import A, n, rp, jt, pct, tbl

M = 1e9
S_PT = ('Undang-Undang Nomor 40 Tahun 2007 tentang Perseroan Terbatas (Pasal 66 sampai 68)', 'https://peraturan.bpk.go.id/Details/39965/uu-no-40-tahun-2007')
CTA = {'href': '/cfo-paruh-waktu/', 'label': 'Layanan CFO Paruh Waktu'}
REL = ['cfo-paruh-waktu-untuk-perusahaan-menengah', 'rasio-keuangan-yang-dilihat-bank', 'laporan-keuangan-bankable-investor-ready', 'rencana-kerja-3-bulan-sebelum-mengajukan-kredit']

# ------------------------------------------------------------------ 7. Bekasi
SALES = 240 * M; COGS = 192 * M; BUNGA = .10
def nwc(dio, dso, dpo):
    inv = COGS * dio / 365; ar = SALES * dso / 365; ap = COGS * dpo / 365
    return inv, ar, ap, inv + ar - ap
B0 = nwc(75, 60, 45); B1 = nwc(60, 50, 55); FREE = B0[3] - B1[3]

A(site='fa', topik='cfo', kota='Bekasi', kota_slug='bekasi',
  slug='fractional-cfo-pabrik-kawasan-industri-bekasi',
  seo_title='Fractional CFO untuk Pabrik di Kawasan Industri Bekasi',
  title='Fractional CFO untuk Pabrik di Kawasan Industri Bekasi: Modal Kerja, Harga Pokok, dan Bank',
  description='Kapan pabrik di Bekasi dan Cikarang perlu fractional CFO, apa yang dikerjakan 90 hari pertama, dan contoh hitung kas yang terbebas dari siklus modal kerja.',
  keyword='fractional cfo bekasi', category='CFO & Tata Kelola', cta=CTA,
  wa='Halo Pak Ananta, kami perusahaan manufaktur di Bekasi dan ingin diskusi layanan fractional CFO.',
  related=REL, sources=[S_PT],
  body_html=f'''
<p>Kabupaten dan Kota Bekasi adalah salah satu kawasan industri terbesar di Indonesia. Di Cikarang dan sekitarnya, ribuan pabrik pemasok komponen otomotif, elektronik, kemasan, dan barang konsumsi bekerja dengan margin tipis dan tuntutan penurunan harga dari pelanggan setiap tahun. Banyak yang omzetnya sudah ratusan miliar rupiah, tetapi fungsi keuangannya masih berhenti di pembukuan dan pajak.</p>
<p>Fractional CFO, atau CFO paruh waktu, mengisi celah itu: seorang direktur keuangan berpengalaman yang bekerja beberapa hari dalam sebulan, dengan biaya sebagian dari CFO penuh waktu.</p>
<h2>Tanda Pabrik Anda Sudah Butuh Fungsi CFO</h2>
<ul>
<li>Laba di laporan naik, tetapi plafon kredit modal kerja selalu terpakai penuh.</li>
<li>Harga pokok per produk tidak pernah dihitung ulang sejak harga bahan dan upah berubah.</li>
<li>Laporan bulanan baru selesai setelah tanggal 20, sehingga keputusan selalu terlambat.</li>
<li>Bank meminta proyeksi arus kas dan perhitungan rasio, dan jawabannya disusun mendadak.</li>
<li>Induk usaha atau pemegang saham asing meminta paket pelaporan dengan format mereka.</li>
<li>Pemilik masih menandatangani semua pembayaran karena tidak ada yang dipercaya menilai prioritasnya.</li>
</ul>
<h2>Contoh: Kas yang Terikat di Siklus Modal Kerja</h2>
<p>Ilustrasi dengan angka contoh: pabrik komponen dengan penjualan {jt(SALES)} dan harga pokok penjualan {jt(COGS)} setahun. Umur persediaan 75 hari, umur piutang 60 hari, umur utang usaha 45 hari, sehingga siklus kas 90 hari.</p>
{tbl(['Pos', 'Kondisi awal', 'Setelah perbaikan', 'Dasar hitung'],
     [['Persediaan', jt(B0[0], 2), jt(B1[0], 2), 'Harga pokok x hari persediaan / 365 (75 menjadi 60 hari)'],
      ['Piutang usaha', jt(B0[1], 2), jt(B1[1], 2), 'Penjualan x hari piutang / 365 (60 menjadi 50 hari)'],
      ['Utang usaha', jt(B0[2], 2), jt(B1[2], 2), 'Harga pokok x hari utang / 365 (45 menjadi 55 hari)']],
     ['Modal kerja bersih', jt(B0[3], 2), jt(B1[3], 2), 'Persediaan + piutang - utang usaha'])}
<p>Siklus kas turun dari 90 menjadi 55 hari dan membebaskan kas <b>{jt(FREE, 2)}</b>. Dengan bunga kredit modal kerja {pct(BUNGA, 0)} per tahun, penghematan bunganya {jt(FREE * BUNGA, 2)} setahun, jauh di atas biaya seorang CFO paruh waktu. Angka seperti ini tidak muncul dari pembukuan. Ia muncul ketika ada yang menata kebijakan stok dengan produksi, termin dengan penjualan, dan jadwal bayar dengan pembelian.</p>
<h2>Yang Dikerjakan Fractional CFO di Pabrik</h2>
{tbl(['Bidang', 'Pekerjaan', 'Hasil yang dipegang direksi'],
     [['Harga pokok', 'Menyusun biaya standar per produk, analisis selisih bahan, upah, dan overhead', 'Margin per produk dan per pelanggan yang bisa dipercaya'],
      ['Kas', 'Proyeksi arus kas 13 minggu, kebijakan stok, termin, dan jadwal bayar', 'Kebutuhan kas diketahui tiga bulan ke depan'],
      ['Pelaporan', 'Tutup buku bulanan paling lambat hari kerja kesepuluh, paket laporan manajemen', 'Satu set angka untuk direksi, bank, dan pemegang saham'],
      ['Bank', 'Menghitung rasio yang diperjanjikan, menyiapkan perpanjangan dan tambahan fasilitas', 'Tidak ada kejutan saat tinjauan tahunan'],
      ['Pajak dan kepatuhan', 'Mengawasi pekerjaan konsultan pajak, dokumentasi transaksi pihak berelasi, laporan tahunan', 'Risiko koreksi dan sanksi terpetakan'],
      ['Investasi', 'Kelayakan mesin baru: arus kas, masa kembali, dan sumber dana', 'Keputusan belanja modal berdasarkan angka']])}
<h2>Rencana 90 Hari Pertama</h2>
<ol>
<li><b>Bulan pertama:</b> membaca laporan keuangan dua tahun, perjanjian kredit, dan struktur biaya. Memetakan kas dan menyusun proyeksi 13 minggu pertama.</li>
<li><b>Bulan kedua:</b> menetapkan kalender tutup buku, memperbaiki harga pokok untuk lima sampai sepuluh produk terbesar, dan menyusun paket laporan bulanan.</li>
<li><b>Bulan ketiga:</b> anggaran dan target modal kerja disepakati direksi, rasio bank dipantau bulanan, daftar perbaikan berikutnya diurutkan menurut nilai rupiahnya.</li>
</ol>
<h2>Bedanya dengan Konsultan Pajak, Kantor Jasa Akuntan, dan Auditor</h2>
<div class="pf-fold"><ul>
<li><b>Kantor jasa akuntan</b> menyusun pembukuan dan laporan keuangan.</li>
<li><b>Konsultan pajak</b> menghitung dan melaporkan pajak serta mendampingi pemeriksaan.</li>
<li><b>Kantor akuntan publik</b> mengaudit dan memberi opini, dan karena itu tidak boleh ikut mengambil keputusan manajemen.</li>
<li><b>Fractional CFO</b> berada di sisi manajemen: memakai hasil ketiganya untuk mengambil keputusan soal harga, kas, utang, dan investasi.</li>
</ul>
<p>Perseroan dengan aset atau peredaran usaha minimal Rp50 miliar wajib diaudit akuntan publik menurut Pasal 68 UU Perseroan Terbatas. Sebagian besar pabrik menengah di Bekasi sudah melewati batas itu, sehingga kesiapan audit otomatis menjadi bagian pekerjaan CFO.</p></div>
<h2>Cara Kerja dan Biaya</h2>
<p>Pola yang umum adalah retainer bulanan: dua sampai empat hari kerja di lokasi atau daring, rapat direksi bulanan, dan akses untuk konsultasi di antaranya. Di FA Indonesia retainer CFO paruh waktu untuk perusahaan lokal mulai Rp15 juta per bulan, disesuaikan dengan cakupan dan ukuran perusahaan. Perusahaan yang butuh pembukuan dan audit sekaligus dikerjakan bersama Kantor Jasa Akuntan dan Kantor Akuntan Publik sebagai perikatan terpisah.</p>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Perusahaan manufaktur di Bekasi, Cikarang, dan Karawang didampingi tim FA Indonesia dengan pengalaman direktur keuangan di perusahaan Indonesia sampai Singapura. Pekerjaan dimulai dari diagnosis kas dan harga pokok, lalu dijalankan sebagai rutinitas bulanan. Lihat <a href="/cfo-paruh-waktu/">layanan CFO paruh waktu</a>, <a href="/laporan-keuangan-manufaktur/">laporan keuangan manufaktur</a>, <a href="/wilayah/bekasi/">layanan FA Indonesia di Bekasi</a>, dan <a href="/konsultan-kredit-bank/">pendampingan kredit bank</a>.</p>
''',
  faq=[('Apa itu fractional CFO?', 'Direktur keuangan berpengalaman yang bekerja paruh waktu untuk perusahaan, biasanya beberapa hari per bulan dengan retainer bulanan, untuk mengurus kas, harga pokok, pelaporan, bank, dan keputusan investasi.'),
       ('Berapa biaya fractional CFO untuk pabrik di Bekasi?', 'Bergantung pada cakupan dan ukuran perusahaan. Di FA Indonesia retainer CFO paruh waktu untuk perusahaan lokal mulai Rp15 juta per bulan.'),
       ('Apakah fractional CFO menggantikan manajer keuangan?', 'Tidak. Manajer keuangan dan staf akuntansi tetap menjalankan operasional harian. Fractional CFO mengarahkan, menetapkan standar laporan, dan mendampingi direksi mengambil keputusan.'),
       ('Kapan sebaiknya beralih ke CFO penuh waktu?', 'Ketika perusahaan sudah membutuhkan kehadiran harian, misalnya menjelang IPO, saat mengelola banyak anak usaha, atau ketika volume transaksi pendanaan terus menerus.')])

# ------------------------------------------------------------------ 8. Medan
ENT = [('PT Kebun (tandan buah segar)', 60, 60, 12), ('PT Pabrik (minyak sawit mentah)', 110, 80, 9), ('PT Dagang (distribusi)', 95, 0, 5)]
GAB = sum(e[1] for e in ENT); IC = sum(e[2] for e in ENT); KONS = GAB - IC; LGAB = sum(e[3] for e in ENT)
UNR = 80 * .25 * .10; LKONS = LGAB - UNR

A(site='fa', topik='cfo', kota='Medan', kota_slug='medan',
  slug='fractional-cfo-grup-usaha-keluarga-medan',
  seo_title='Fractional CFO untuk Grup Usaha Keluarga di Medan',
  title='Fractional CFO untuk Grup Usaha Keluarga di Medan: Konsolidasi, Kas Keluarga, dan Bank',
  description='Grup usaha keluarga di Medan sering punya banyak PT tanpa laporan konsolidasian. Ini peran fractional CFO: eliminasi antar perusahaan, kas, dan suksesi.',
  keyword='fractional cfo medan', category='CFO & Tata Kelola', cta=CTA,
  wa='Halo Pak Ananta, kami grup usaha keluarga di Medan dan ingin diskusi layanan fractional CFO.',
  related=REL, sources=[S_PT],
  body_html=f'''
<p>Medan adalah kota bisnis terbesar di luar Jawa dan simpul perdagangan Sumatera. Banyak usahanya tumbuh sebagai grup keluarga: perkebunan dan pabrik kelapa sawit, distribusi, properti, sampai rumah sakit, masing-masing di perseroan sendiri dengan pemegang saham yang bersaudara. Usahanya kuat, tetapi jarang ada satu orang yang bisa menjawab pertanyaan sederhana dari bank: berapa penjualan, laba, dan utang grup ini sebenarnya?</p>
<p>Di sinilah fractional CFO berguna. Bukan untuk mengambil alih keuangan keluarga, tetapi untuk menyusun satu gambaran yang utuh dan dipercaya semua pihak.</p>
<h2>Masalah Khas Grup Usaha Keluarga</h2>
<ul>
<li>Setiap perseroan punya pembukuan sendiri dengan kebijakan dan bagan akun yang berbeda.</li>
<li>Jual beli antar perusahaan memakai harga kesepakatan keluarga, tanpa kontrak dan tanpa dokumentasi.</li>
<li>Kas berpindah antar perusahaan dan ke rekening pribadi sebagai pinjaman tanpa perjanjian.</li>
<li>Aset penting, misalnya lahan dan gudang, tercatat atas nama pribadi.</li>
<li>Generasi kedua mulai masuk, tetapi pembagian peran dan dividen belum pernah ditulis.</li>
</ul>
<h2>Contoh: Angka Gabungan Bukan Angka Grup</h2>
<p>Ilustrasi dengan angka contoh, dalam miliar rupiah. Tiga perseroan dalam satu grup saling bertransaksi: kebun menjual seluruh hasilnya ke pabrik, pabrik menjual sebagian besar minyak ke perusahaan dagang.</p>
{tbl(['Perseroan', 'Penjualan', 'Di antaranya ke perusahaan grup', 'Laba'],
     [[a, n(s), n(i), n(l)] for a, s, i, l in ENT], ['Jumlah gabungan', n(GAB), n(IC), n(LGAB)])}
<p>Bila tiga laporan itu dijumlahkan begitu saja, grup tampak beromzet Rp{n(GAB)} miliar. Setelah penjualan antar perusahaan Rp{n(IC)} miliar dieliminasi, penjualan konsolidasian kepada pihak luar hanya <b>Rp{n(KONS)} miliar</b>.</p>
<p>Laba juga perlu disesuaikan. Bila seperempat barang yang dibeli perusahaan dagang dari pabrik (Rp80 miliar x 25%) masih ada di gudang pada akhir tahun, dan pabrik mengambil margin 10 persen, maka laba Rp{n(UNR, 0)} miliar belum terealisasi dari sudut grup. Laba konsolidasian menjadi Rp{n(LKONS, 0)} miliar, bukan Rp{n(LGAB)} miliar.</p>
<p>Analis kredit menghitung dengan cara ini. Grup yang datang ke bank dengan angka gabungan akan dikoreksi, dan koreksi oleh pihak lain selalu lebih mahal daripada koreksi sendiri.</p>
<h2>Yang Dikerjakan Fractional CFO untuk Grup</h2>
{tbl(['Bidang', 'Pekerjaan', 'Hasil'],
     [['Konsolidasi', 'Menyeragamkan bagan akun dan kebijakan, menyusun laporan konsolidasian manajemen tiap bulan', 'Satu angka grup untuk keluarga dan bank'],
      ['Transaksi antar perusahaan', 'Menetapkan harga, kontrak, dan rekonsiliasi saldo bulanan', 'Saldo saling cocok, risiko pajak pihak berelasi terkendali'],
      ['Kas', 'Posisi kas grup harian, kebijakan pinjaman antar perusahaan dan ke pemegang saham', 'Kas keluarga dan kas usaha terpisah jelas'],
      ['Bank', 'Peta fasilitas, agunan, dan jaminan silang seluruh grup', 'Kapasitas pinjaman grup diketahui sebelum bank bertanya'],
      ['Tata kelola', 'Kebijakan dividen, kewenangan pembayaran, agenda rapat keluarga per triwulan', 'Keputusan keuangan tidak bergantung pada satu orang']])}
<h2>Kas Keluarga dan Pinjaman Pemegang Saham</h2>
<div class="pf-fold"><p>Pos yang paling sering mengganggu grup keluarga di mata bank adalah piutang kepada pemegang saham. Bagi keluarga, itu sekadar uang yang diambil dulu. Bagi analis, itu aset yang tidak menghasilkan dan cenderung dikeluarkan dari perhitungan modal.</p>
<p>Penataannya bertahap: dicatat dengan perjanjian, diberi jadwal pengembalian atau diselesaikan lewat dividen yang diputuskan rapat umum pemegang saham, lalu ke depan pengambilan keluarga dibatasi pada gaji, tunjangan, dan dividen. Pembagian laba dan kewajiban menyisihkan cadangan diatur dalam UU Perseroan Terbatas, sehingga tertib dividen sekaligus menertibkan kepatuhan.</p></div>
<h2>Menyiapkan Suksesi dari Sisi Angka</h2>
<ul>
<li>Laporan per perseroan dan per lini usaha yang memperlihatkan siapa menghasilkan apa.</li>
<li>Valuasi indikatif tiap perseroan sebagai dasar pembagian peran dan saham.</li>
<li>Struktur induk usaha bila keluarga ingin kepemilikan disatukan.</li>
<li>Laporan keuangan yang diaudit untuk perseroan yang memenuhi kriteria wajib audit.</li>
</ul>
<h2>Cara Kerja dan Biaya</h2>
<p>Untuk grup, fractional CFO biasanya bekerja dengan retainer bulanan dan hadir pada rapat keluarga atau rapat direksi tiap bulan. Di FA Indonesia retainer CFO paruh waktu mulai Rp15 juta per bulan dan menyesuaikan jumlah perseroan serta kedalaman pekerjaan. Kerahasiaan dituangkan dalam perjanjian sejak awal.</p>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Grup usaha di Medan dan Sumatera Utara didampingi tim FA Indonesia yang terbiasa menyusun konsolidasi dan berhadapan dengan bank maupun investor. Penyusunan laporan keuangan dan audit dikerjakan Kantor Jasa Akuntan dan Kantor Akuntan Publik sebagai perikatan terpisah. Lihat <a href="/cfo-paruh-waktu/">layanan CFO paruh waktu</a>, <a href="/wilayah/medan/">layanan FA Indonesia di Medan</a>, <a href="/jasa-penyusunan-laporan-keuangan/medan/">penyusunan laporan keuangan di Medan</a>, dan <a href="/laporan-keuangan-perkebunan-sawit/">laporan keuangan perkebunan sawit</a>.</p>
''',
  faq=[('Kenapa grup usaha keluarga butuh laporan konsolidasian?', 'Karena penjumlahan laporan tiap perseroan menghitung dua kali transaksi antar perusahaan. Bank dan investor menilai grup dari angka setelah eliminasi.'),
       ('Apakah fractional CFO ikut mengatur urusan keluarga?', 'Tidak. Perannya menyiapkan angka, kebijakan, dan pilihan yang jelas. Keputusan tetap pada pemegang saham.'),
       ('Bagaimana memperlakukan pinjaman kepada pemegang saham?', 'Dicatat dengan perjanjian dan jadwal pengembalian, atau diselesaikan melalui dividen yang diputuskan rapat umum pemegang saham. Setelah itu pengambilan keluarga dibatasi pada gaji dan dividen.'),
       ('Apakah setiap perseroan di grup wajib diaudit?', 'Kewajiban audit dinilai per perseroan menurut kriteria Pasal 68 UU Perseroan Terbatas, misalnya aset atau peredaran usaha minimal Rp50 miliar. Bank sering meminta audit meskipun kriteria itu belum terpenuhi.')])

# ------------------------------------------------------------------ 9. Balikpapan
EB = 36 * M; TAX = 4 * M; CPX = 6 * M; PK = 14 * M; BG = 6 * M; COV = 1.25
CF = EB - TAX - CPX; DS = PK + BG; D0 = CF / DS; HEAD = CF - COV * DS
EB2 = EB + 7 * M; TAX2 = TAX + 1 * M; DS2 = DS + 4.8 * M; CF2 = EB2 - TAX2 - CPX; D1 = CF2 / DS2

A(site='fa', topik='cfo', kota='Balikpapan', kota_slug='balikpapan',
  slug='fractional-cfo-kontraktor-tambang-migas-balikpapan',
  seo_title='Fractional CFO Kontraktor Tambang dan Migas di Balikpapan',
  title='Fractional CFO untuk Kontraktor Tambang dan Migas di Balikpapan: Proyek, Alat Berat, dan DSCR',
  description='Kontraktor di Balikpapan hidup dari proyek dan alat berat. Ini peran fractional CFO: arus kas per proyek, pembiayaan alat, dan DSCR sesuai syarat bank.',
  keyword='fractional cfo balikpapan', category='CFO & Tata Kelola', cta=CTA,
  wa='Halo Pak Ananta, kami kontraktor di Balikpapan dan ingin diskusi layanan fractional CFO.',
  related=['cfo-paruh-waktu-untuk-perusahaan-menengah', 'kredit-modal-kerja-kontraktor-berbasis-spk', 'laporan-keuangan-kontraktor-psak-115', 'audit-laporan-keuangan-perusahaan-tambang-kontraktor-kalimantan', 'rasio-keuangan-yang-dilihat-bank'],
  sources=[S_PT],
  body_html=f'''
<p>Balikpapan dikenal sebagai kota minyak dan gas sekaligus gerbang menuju Ibu Kota Nusantara. Di sekelilingnya bekerja kontraktor jasa pertambangan, penyedia alat berat, perusahaan logistik, fabrikasi, dan katering lapangan. Ciri keuangannya sama: pendapatan datang per proyek, aset utamanya alat yang dibiayai utang, dan pembayaran pelanggan mengikuti termin yang panjang.</p>
<p>Dalam usaha seperti ini, laba di atas kertas dan kas di rekening bisa berjalan ke arah berlawanan. Fractional CFO bertugas menjaga keduanya searah.</p>
<h2>Empat Titik Rawan Keuangan Kontraktor</h2>
<ul>
<li><b>Pengakuan pendapatan.</b> Menurut PSAK 115, pendapatan kontrak diakui sesuai kemajuan pekerjaan. Tagihan termin yang lebih kecil dari kemajuan menjadi aset kontrak, bukan kas.</li>
<li><b>Retensi dan jaminan.</b> Sebagian tagihan ditahan sampai masa pemeliharaan selesai, sementara plafon bank garansi terpakai untuk jaminan pelaksanaan dan uang muka.</li>
<li><b>Alat berat.</b> Dibiayai sewa pembiayaan atau kredit investasi dengan angsuran tetap, padahal jam kerja alat mengikuti kontrak.</li>
<li><b>Biaya per proyek.</b> Solar, suku cadang, dan upah sering dicatat per perusahaan, bukan per proyek, sehingga proyek yang rugi baru ketahuan di akhir.</li>
</ul>
<h2>Contoh: DSCR dan Ruang Geraknya</h2>
<p>Bank yang membiayai alat hampir selalu mensyaratkan debt service coverage ratio (DSCR), yaitu kas yang tersedia untuk membayar utang dibagi kewajiban pokok dan bunga. Ilustrasi dengan angka contoh, dalam setahun:</p>
{tbl(['Pos', 'Saat ini', 'Setelah menambah lima unit alat'],
     [['EBITDA', jt(EB), jt(EB2)], ['Pajak dibayar', jt(TAX), jt(TAX2)], ['Belanja modal pemeliharaan', jt(CPX), jt(CPX)],
      ['Kas tersedia untuk membayar utang', jt(CF), jt(CF2)], ['Angsuran pokok dan bunga', jt(DS), jt(DS2, 1)]],
     ['DSCR', n(D0, 2) + ' kali', n(D1, 2) + ' kali'])}
<p>Dengan syarat minimal {n(COV, 2)} kali, kas yang harus tersedia {jt(COV * DS)}. Ruang geraknya hanya {jt(HEAD)}: EBITDA turun {pct(HEAD / EB)} saja sudah melanggar syarat. Satu kontrak yang mundur dua bulan cukup untuk itu.</p>
<p>Kolom kanan memperlihatkan hal yang sering luput. Menambah lima unit alat menaikkan EBITDA {jt(EB2 - EB)}, tetapi angsuran bertambah {jt(DS2 - DS, 1)} dan DSCR justru turun menjadi {n(D1, 2)} kali. Pertumbuhan yang dibiayai utang bisa memperlemah posisi di mata bank bila tenor dan jadwal angsurannya tidak dirancang mengikuti kontrak.</p>
<h2>Yang Dikerjakan Fractional CFO untuk Kontraktor</h2>
{tbl(['Bidang', 'Pekerjaan', 'Hasil'],
     [['Arus kas proyek', 'Proyeksi kas per proyek: termin, retensi, uang muka, dan biaya mobilisasi', 'Kebutuhan modal kerja tiap kontrak diketahui sebelum tanda tangan'],
      ['Biaya', 'Laba rugi per proyek dan per unit alat: jam kerja, solar, suku cadang, operator', 'Tarif sewa dan harga penawaran berdasarkan biaya nyata'],
      ['Pembiayaan alat', 'Membandingkan sewa pembiayaan, kredit investasi, dan sewa operasi; menyelaraskan tenor dengan kontrak', 'Angsuran sejalan dengan arus kas kontrak'],
      ['Bank', 'Memantau DSCR dan rasio lain tiap bulan, mengelola plafon bank garansi', 'Peringatan dini sebelum syarat terlanggar'],
      ['Pelaporan', 'Laporan keuangan sesuai PSAK 115 dan PSAK 116, siap diaudit', 'Memenuhi prakualifikasi tender dan permintaan bank']])}
<h2>Sebelum Menandatangani Kontrak Baru</h2>
<div class="pf-fold"><p>Daftar periksa yang kami pakai bersama direksi sebelum penawaran dimasukkan:</p>
<ol>
<li>Berapa kas yang keluar sebelum termin pertama diterima, termasuk mobilisasi dan jaminan?</li>
<li>Berapa persen retensi dan kapan cair?</li>
<li>Apakah alat yang dibutuhkan sudah ada, atau harus dibiayai baru, dan berapa tenornya dibanding masa kontrak?</li>
<li>Bagaimana DSCR dan plafon bank garansi setelah kontrak ini masuk?</li>
<li>Apa yang terjadi pada kas bila pembayaran pelanggan mundur 60 hari?</li>
</ol>
<p>Lima pertanyaan ini lebih sering menyelamatkan perusahaan daripada negosiasi harga.</p></div>
<h2>Cara Kerja dan Biaya</h2>
<p>Fractional CFO bekerja dengan retainer bulanan, hadir pada rapat direksi dan rapat dengan bank, dan dapat dihubungi saat ada penawaran yang perlu dihitung cepat. Di FA Indonesia retainer CFO paruh waktu untuk perusahaan lokal mulai Rp15 juta per bulan, menyesuaikan jumlah proyek dan badan usaha. Pekerjaan dijalankan daring dengan kunjungan berkala ke Balikpapan.</p>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Kontraktor dan perusahaan penunjang migas di Balikpapan, Samarinda, dan kawasan Ibu Kota Nusantara didampingi tim FA Indonesia untuk arus kas proyek, pembiayaan alat, dan hubungan dengan bank. Audit dikerjakan Kantor Akuntan Publik sebagai perikatan terpisah. Lihat <a href="/cfo-paruh-waktu/">layanan CFO paruh waktu</a>, <a href="/wilayah/balikpapan/">layanan FA Indonesia di Balikpapan</a>, <a href="/laporan-keuangan-kontraktor/">laporan keuangan kontraktor</a>, dan <a href="/artikel/kredit-modal-kerja-kontraktor-berbasis-spk/">kredit modal kerja kontraktor berbasis SPK</a>.</p>
''',
  faq=[('Apa itu DSCR dan kenapa penting bagi kontraktor?', 'Debt service coverage ratio adalah kas yang tersedia untuk membayar utang dibagi angsuran pokok dan bunga. Bank memakainya sebagai syarat kredit alat, dan pelanggaran syarat bisa memicu peninjauan fasilitas.'),
       ('Kenapa laba kontraktor tidak selalu menjadi kas?', 'Karena pendapatan diakui sesuai kemajuan pekerjaan, sedangkan kas mengikuti termin tagihan dan sebagian ditahan sebagai retensi.'),
       ('Apakah fractional CFO bisa bekerja jarak jauh untuk perusahaan di Balikpapan?', 'Bisa. Tutup buku, proyeksi kas, dan rapat rutin dijalankan daring, dengan kunjungan berkala untuk rapat direksi dan pertemuan bank.'),
       ('Lebih baik sewa pembiayaan atau kredit investasi untuk alat berat?', 'Tidak ada jawaban tunggal. Bandingkan total biaya dana, tenor terhadap masa kontrak, agunan tambahan, dan dampaknya ke DSCR sebelum memilih.')])

# ------------------------------------------------------------------ 10. Bandung
J = 1e6
CH = [('Toko sendiri', 900 * J, .45, .14), ('Marketplace', 600 * J, .45, .28), ('Reseller dan grosir', 300 * J, .60, .05)]
FIX = 480 * J
ch_rows, ts, tcm = [], 0, 0
for nm, s, h, v in CH:
    cm = s * (1 - h - v); ts += s; tcm += cm
    ch_rows.append([nm, jt(s), jt(s * h), jt(s * v), jt(cm), pct(cm / s, 0)])
ADD = 300 * J; ADD_CM = ADD * (1 - .45 - .28)

A(site='fa', topik='cfo', kota='Bandung', kota_slug='bandung',
  slug='fractional-cfo-usaha-fesyen-kuliner-bandung',
  seo_title='Fractional CFO untuk Usaha Fesyen dan Kuliner di Bandung',
  title='Fractional CFO untuk Usaha Fesyen dan Kuliner di Bandung yang Sedang Tumbuh',
  description='Merek fesyen dan kuliner di Bandung tumbuh lewat banyak kanal. Ini peran fractional CFO: margin kontribusi per kanal, anggaran, kas, dan kesiapan investor.',
  keyword='fractional cfo bandung', category='CFO & Tata Kelola', cta=CTA,
  wa='Halo Pak Ananta, kami usaha di Bandung yang sedang tumbuh dan ingin diskusi layanan fractional CFO.',
  related=['cfo-paruh-waktu-untuk-perusahaan-menengah', 'menawarkan-usaha-kecil-ke-investor-langkah', 'valuasi-usaha-umkm-penjualan-marketplace', 'mengembangkan-usaha-tanpa-utang', 'laporan-keuangan-bankable-investor-ready'],
  sources=[S_PT],
  body_html=f'''
<p>Bandung adalah pusat tekstil, industri kreatif, dan kuliner. Banyak merek pakaian, sepatu, kopi, dan makanan lahir di sini lalu tumbuh cepat lewat toko sendiri, marketplace, reseller, dan waralaba. Pertumbuhan seperti itu membawa masalah yang khas: penjualan naik setiap bulan, tetapi pemilik tidak yakin kanal mana yang sebenarnya menghasilkan uang.</p>
<p>Pada tahap ini usaha belum butuh direktur keuangan penuh waktu, tetapi sudah melewati kemampuan seorang admin pembukuan. Fractional CFO mengisi ruang di antaranya.</p>
<h2>Tanda Usaha Anda Sudah di Tahap Ini</h2>
<ul>
<li>Omzet tumbuh, saldo rekening tidak ikut tumbuh.</li>
<li>Stok menumpuk di beberapa model atau menu, kosong di yang laris.</li>
<li>Biaya iklan dan potongan marketplace naik lebih cepat daripada penjualan.</li>
<li>Ada calon investor atau mitra waralaba yang meminta laporan keuangan dan proyeksi.</li>
<li>Rencana membuka cabang atau pabrik kecil belum pernah dihitung titik impasnya.</li>
</ul>
<h2>Contoh: Margin Kontribusi per Kanal</h2>
<p>Ilustrasi dengan angka contoh sebuah merek pakaian, satu bulan. Biaya variabel kanal mencakup potongan platform, iklan, subsidi ongkos kirim, komisi, dan biaya pembayaran.</p>
{tbl(['Kanal', 'Penjualan', 'Harga pokok', 'Biaya variabel kanal', 'Margin kontribusi', 'Persen'],
     ch_rows, ['Jumlah', jt(ts), '', '', jt(tcm), pct(tcm / ts, 0)])}
<p>Setelah biaya tetap {jt(FIX)} (gaji, sewa, kantor), laba operasi bulan itu {jt(tcm - FIX)}. Marketplace menyumbang sepertiga penjualan tetapi hanya sekitar seperempat margin kontribusi.</p>
<p>Sekarang uji sebuah keputusan: menambah anggaran iklan agar penjualan marketplace naik {jt(ADD)}. Tambahan margin kontribusinya {jt(ADD)} x 27% = {jt(ADD_CM)}, belum dikurangi tambahan stok yang harus dibiayai. Penjualan yang sama lewat toko sendiri menghasilkan {jt(ADD * .41)}. Angka ini tidak melarang marketplace. Ia menunjukkan harga yang wajar untuk setiap pertumbuhan.</p>
<h2>Yang Dikerjakan Fractional CFO untuk Usaha yang Sedang Tumbuh</h2>
{tbl(['Bidang', 'Pekerjaan', 'Hasil'],
     [['Margin', 'Laba rugi per kanal, per cabang, dan per kelompok produk', 'Tahu di mana uang dihasilkan dan di mana terbakar'],
      ['Stok dan kas', 'Kebijakan pembelian, umur stok, proyeksi kas 13 minggu', 'Produksi dan pembelian mengikuti kas, bukan perasaan'],
      ['Anggaran', 'Anggaran tahunan dan prakiraan bergulir yang diperbarui tiap bulan', 'Target yang bisa dipantau, bukan sekadar harapan'],
      ['Ekspansi', 'Titik impas cabang baru, kelayakan dapur pusat atau konveksi sendiri', 'Keputusan ekspansi dengan angka'],
      ['Investor dan bank', 'Laporan keuangan yang rapi, proyeksi, valuasi indikatif, materi paparan', 'Siap ditanya dan siap diperiksa']])}
<h2>Dari Pembukuan ke Laporan yang Bisa Dipakai Memutuskan</h2>
<div class="pf-fold"><p>Urutan kerjanya hampir selalu sama:</p>
<ol>
<li>Pisahkan rekening usaha dari rekening pribadi dan rapikan pencatatan penjualan per kanal.</li>
<li>Susun laporan keuangan dengan standar yang sesuai. Usaha yang sudah berbadan hukum dan tumbuh umumnya memakai SAK Entitas Privat.</li>
<li>Tambahkan laporan manajemen: margin per kanal, umur stok, dan arus kas.</li>
<li>Tetapkan rapat angka bulanan satu jam bersama pemilik.</li>
</ol>
<p>Dua langkah pertama adalah pekerjaan kantor jasa akuntan atau tim pembukuan. Fractional CFO masuk mulai langkah ketiga dan memastikan langkah pertama dan kedua dikerjakan dengan benar.</p></div>
<h2>Kalau Ada Investor yang Datang</h2>
<ul>
<li>Investor membaca pertumbuhan dan margin kontribusi, bukan hanya omzet.</li>
<li>Laporan yang dipisah per kanal dan per cabang mempercepat penilaian.</li>
<li>Hitung dulu valuasi indikatif dan kebutuhan dana sebelum menyebut angka.</li>
<li>Pastikan merek, perizinan, dan kontrak sewa atas nama badan usaha.</li>
</ul>
<h2>Cara Kerja dan Biaya</h2>
<p>Untuk usaha yang sedang tumbuh, fractional CFO biasanya bekerja satu sampai dua hari per bulan ditambah rapat angka bulanan. Di FA Indonesia retainer CFO paruh waktu mulai Rp15 juta per bulan. Usaha yang belum sampai di tahap itu bisa memulai dari penyusunan laporan keuangan dan satu kali sesi diagnosis.</p>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Pemilik usaha di Bandung, Cimahi, dan sekitarnya didampingi tim FA Indonesia untuk membaca margin, menata kas, dan menyiapkan diri sebelum bertemu bank atau investor. Lihat <a href="/cfo-paruh-waktu/">layanan CFO paruh waktu</a>, <a href="/wilayah/bandung/">layanan FA Indonesia di Bandung</a>, <a href="/jasa-penyusunan-laporan-keuangan/bandung/">penyusunan laporan keuangan di Bandung</a>, dan <a href="/artikel/menawarkan-usaha-kecil-ke-investor-langkah/">langkah menawarkan usaha ke investor</a>.</p>
''',
  faq=[('Kapan usaha perlu fractional CFO, bukan sekadar pembukuan?', 'Ketika keputusan soal kanal penjualan, stok, cabang baru, utang, atau investor sudah bernilai besar dan pemilik butuh angka serta pendamping untuk memutuskannya.'),
       ('Apa itu margin kontribusi per kanal?', 'Penjualan suatu kanal dikurangi harga pokok dan biaya variabel kanal itu, seperti potongan platform, iklan, dan komisi. Angka ini menunjukkan sumbangan tiap kanal untuk menutup biaya tetap.'),
       ('Apakah usaha kecil di Bandung mampu membayar fractional CFO?', 'Bergantung pada skala. Sebagai patokan, layanan ini masuk akal bila nilai keputusan yang dibantu jauh di atas retainer bulanannya. Usaha yang lebih kecil bisa mulai dari laporan keuangan dan sesi diagnosis.'),
       ('Standar akuntansi apa yang dipakai usaha yang sedang tumbuh?', 'Usaha mikro dan kecil dapat memakai SAK EMKM. Usaha berbadan hukum yang tumbuh dan mencari pendanaan umumnya memakai SAK Entitas Privat yang berlaku sejak 1 Januari 2025.')])
