from _a import A

CAT = 'Valuasi & Investor'
CTA = ('/jasa-valuasi-usaha/', 'Jasa Valuasi Usaha')
OJK = ('https://www.ojk.go.id/', 'Otoritas Jasa Keuangan')
MAPPI = ('https://mappi.or.id/', 'MAPPI, Standar Penilaian Indonesia')
IAI = ('https://iaiglobal.or.id/', 'Ikatan Akuntan Indonesia')
PENUTUP = ('<h2>Diskusi dengan FA Indonesia</h2><p>Untuk valuasi dan persiapan bertemu investor, Anda bicara langsung dengan Ananta W. Sasongko, CPA. '
           'Biasanya dimulai dari melihat data yang sudah ada, lalu diusulkan urutan kerja yang paling hemat: rapikan laporan, hitung nilai, baru siapkan bahan untuk investor. '
           'Bila dibutuhkan penilaian aset oleh penilai berizin, dilakukan oleh KJPP.</p>')

A('valuasi-usaha-umkm-penjualan-marketplace',
  'Valuasi Usaha UMKM dengan Penjualan Marketplace',
  'Valuasi Usaha UMKM dengan Penjualan Shopee dan TikTok Shop: Cara Menghitungnya',
  'Usaha dengan penjualan marketplace bisa dinilai untuk investor. Ini data yang dipakai, cara menghitung, dan kenapa laporan keuangan menentukan nilai.',
  'valuasi usaha umkm marketplace', CAT, 7, CTA,
  'Halo Pak Ananta, usaha kami jualan di marketplace dan ingin tahu nilai usahanya untuk ditawarkan ke investor.',
  [OJK, IAI],
  ['valuasi-perusahaan-swasta-dcf-multiple-ebitda', 'modal-usaha-dari-investor-atau-bank', 'contoh-laporan-keuangan-umkm', 'due-diligence-investor-yang-perlu-disiapkan'],
  '''
<p>Banyak usaha kecil tumbuh pesat lewat Shopee, TikTok Shop, dan Tokopedia. Produk makanan, kue, fesyen, atau kosmetik bisa terjual ribuan pesanan per bulan. Saat pemilik ingin mengajak investor atau menjual sebagian saham, pertanyaannya: berapa nilai usaha ini?</p>
<h2>Apa yang Sebenarnya Dinilai</h2>
<p>Investor tidak membeli peralatan dapur atau stok barang saja. Yang dinilai adalah usaha secara utuh: merek, toko marketplace dengan ulasan dan pengikutnya, pelanggan tetap, resep atau desain produk, peralatan produksi, dan kemampuan menghasilkan laba ke depan.</p>
<h2>Data yang Dipakai</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Data</th><th>Sumber</th></tr></thead><tbody>
<tr><td>Penjualan per kanal per bulan</td><td>Laporan penjualan Shopee, TikTok, offline</td></tr>
<tr><td>Potongan marketplace</td><td>Biaya admin, ongkir subsidi, iklan, voucher</td></tr>
<tr><td>Harga pokok produk</td><td>Bahan baku, kemasan, tenaga produksi</td></tr>
<tr><td>Biaya operasional</td><td>Gaji, sewa, listrik, pemasaran</td></tr>
<tr><td>Dana yang benar-benar diterima</td><td>Rekening koran, penarikan saldo marketplace</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Hal yang sering ditemukan: penjualan di dasbor marketplace ternyata lebih besar daripada pemasukan yang dicatat pemilik, karena sebagian saldo ditarik ke rekening pribadi atau dipakai langsung. Setelah dirapikan, nilai usaha bisa justru lebih tinggi dari perkiraan pemilik.</p></div>
<h2>Cara Menghitung</h2>
<ol>
<li>Susun laporan laba rugi minimal 12 bulan, per kanal penjualan.</li>
<li>Normalisasi biaya: pisahkan biaya pribadi, masukkan gaji wajar pemilik yang ikut bekerja.</li>
<li>Hitung laba bersih atau EBITDA yang berkelanjutan.</li>
<li>Terapkan pendekatan pendapatan, misalnya kelipatan laba atau arus kas terdiskonto.</li>
<li>Bandingkan dengan nilai aset bersih sebagai batas bawah.</li>
</ol>
<div class="pf-fold"><p>Ketergantungan pada satu kanal adalah risiko yang diperhitungkan investor. Usaha yang 90 persen penjualannya dari satu marketplace lebih rentan terhadap perubahan algoritma atau kebijakan biaya. Penjualan yang tersebar di beberapa kanal biasanya dinilai lebih stabil.</p></div>
<h2>Kenapa Laporan Keuangan Didahulukan</h2>
<p>Valuasi dihitung dari angka laporan keuangan. Bila angkanya belum rapi, hasil valuasi hanya indikatif. Investor yang serius juga hampir pasti meminta laporan keuangan dan memeriksa pajaknya. Karena itu urutan yang paling hemat biasanya: rapikan laporan, bereskan pajak, hitung nilai, baru tawarkan.</p>
''' + PENUTUP,
  [('Berapa kali laba nilai usaha UMKM?', 'Tidak ada angka baku. Tergantung pertumbuhan, stabilitas, risiko ketergantungan kanal, dan kualitas laporan keuangan.'),
   ('Apakah toko marketplace ikut dinilai?', 'Ya, sebagai bagian dari usaha secara utuh, karena toko dengan ulasan dan pengikut menghasilkan penjualan.'),
   ('Bisakah valuasi tanpa laporan keuangan?', 'Bisa sebagai angka indikatif dari data pemilik, tetapi investor umumnya akan meminta laporan keuangan.')])

A('menawarkan-usaha-kecil-ke-investor-langkah',
  'Menawarkan Usaha Kecil ke Investor: Urutan Persiapan',
  'Menawarkan Usaha Kecil ke Investor: Laporan Keuangan Dulu, Pitch Kemudian',
  'Ingin mengajak investor masuk ke usaha kecil atau menengah? Ini urutan persiapan yang hemat: laporan keuangan, pajak, valuasi, lalu bahan presentasi.',
  'menawarkan usaha ke investor', CAT, 6, CTA,
  'Halo Pak Ananta, saya ingin menawarkan usaha saya ke investor. Boleh diskusi persiapannya?',
  [OJK],
  ['modal-usaha-dari-investor-atau-bank', 'menilai-kesiapan-calon-investee-sebelum-term-sheet', 'due-diligence-investor-yang-perlu-disiapkan', 'cara-menjual-perusahaan-atau-sebagian-saham'],
  '''
<p>Pemilik usaha yang ingin mengajak investor sering memulai dari bahan presentasi: logo, foto produk, angka penjualan, dan rencana ekspansi. Presentasi memang penting, tetapi investor yang serius akan bertanya hal yang sama setelah slide terakhir: boleh lihat laporan keuangannya?</p>
<h2>Urutan yang Disarankan</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Tahap</th><th>Hasil</th></tr></thead><tbody>
<tr><td>1. Rapikan laporan keuangan</td><td>Laporan minimal 12 bulan sesuai standar akuntansi</td></tr>
<tr><td>2. Bereskan pajak</td><td>Kewajiban pajak jelas, tidak ada kejutan saat due diligence</td></tr>
<tr><td>3. Hitung nilai usaha</td><td>Rentang nilai yang bisa dipertanggungjawabkan</td></tr>
<tr><td>4. Susun bahan untuk investor</td><td>Ringkasan usaha, rencana penggunaan dana, proyeksi</td></tr>
<tr><td>5. Penjajakan dan negosiasi</td><td>Term sheet dan due diligence</td></tr>
</tbody></table></div>
<h2>Kenapa Tidak Langsung Pitch</h2>
<p>Bila presentasi dilakukan sebelum laporan siap, ada dua risiko. Pertama, nilai yang diajukan tidak bisa dipertahankan saat diperiksa, sehingga negosiasi melemah. Kedua, investor yang kecewa di tahap awal jarang kembali.</p>
<div class="pf-fold"><p>Usaha yang laporannya rapi sering mendapat nilai lebih baik, karena risiko di mata investor berkurang. Ketidakpastian selalu diterjemahkan investor menjadi potongan harga.</p></div>
<h2>Hal yang Biasanya Ditanyakan Investor</h2>
<ul>
<li>Berapa penjualan dan laba 12 sampai 24 bulan terakhir?</li>
<li>Apakah uang pribadi dan uang usaha sudah terpisah?</li>
<li>Siapa pemegang saham sekarang, dan apakah usahanya sudah berbadan hukum?</li>
<li>Untuk apa dana investor dipakai, dan berapa hasilnya?</li>
<li>Bagaimana investor keluar nanti?</li>
</ul>
<h2>Bentuk Badan Usaha</h2>
<p>Investor umumnya masuk dengan membeli atau mengambil saham. Usaha perorangan atau CV perlu dipertimbangkan untuk menjadi PT sebelum investor masuk. Diskusikan dengan notaris dan konsultan pajak tentang cara pengalihan aset dan usahanya.</p>
<div class="pf-fold"><p>Memilih paket kerja yang mencakup laporan keuangan, valuasi, dan bahan investor sekaligus sering lebih hemat daripada mengerjakannya terpisah, karena data yang sama dipakai untuk ketiganya.</p></div>
''' + PENUTUP,
  [('Apakah usaha kecil bisa menarik investor?', 'Bisa, terutama bila tumbuh stabil, laporannya rapi, dan rencana penggunaan dananya jelas.'),
   ('Perlukah menjadi PT dulu?', 'Umumnya ya, karena investor masuk lewat kepemilikan saham.'),
   ('Berapa lama persiapannya?', 'Tergantung kondisi laporan keuangan. Bila pembukuan sudah ada, beberapa minggu. Bila belum, lebih lama.')])

A('studi-kelayakan-proyek-wisata-pemegang-saham',
  'Studi Kelayakan Proyek Wisata untuk Pemegang Saham',
  'Studi Kelayakan Proyek Wisata: Untuk Pemegang Saham, Otoritas, dan Kontrak Lahan',
  'Membangun atraksi wisata baru seperti zip line atau resort? Ini isi studi kelayakan, siapa yang membacanya, dan bedanya dengan penilaian aset oleh KJPP.',
  'studi kelayakan proyek wisata', CAT, 7, CTA,
  'Halo Pak Ananta, kami berencana membangun proyek wisata baru dan butuh studi kelayakan.',
  [MAPPI, ('https://kemenparekraf.go.id/', 'Kementerian Pariwisata')],
  ['cara-menghitung-wacc-dan-valuasi-dcf-perusahaan-indonesia', 'kapan-perusahaan-butuh-kjpp-jasa-penilai', 'kredit-investasi-pabrik-gudang-mesin-syarat', 'modal-usaha-dari-investor-atau-bank'],
  '''
<p>Pariwisata di kawasan seperti Labuan Bajo, Bali, Lombok, dan Danau Toba terus menarik investasi baru: atraksi petualangan, resort kecil, restoran dengan pemandangan, atau fasilitas wisata bahari. Sebelum dana besar dikeluarkan, pemegang saham dan sering juga otoritas pengelola kawasan ingin melihat satu dokumen: studi kelayakan.</p>
<h2>Siapa yang Membaca Studi Kelayakan</h2>
<ul>
<li><b>Pemegang saham.</b> Ingin tahu apakah investasi akan kembali dan kapan.</li>
<li><b>Otoritas kawasan atau pemilik lahan.</b> Ingin yakin proyek serius dan berkelanjutan sebelum memberi izin atau kontrak lahan.</li>
<li><b>Bank.</b> Bila sebagian dibiayai kredit investasi.</li>
</ul>
<h2>Isi Studi Kelayakan</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Bagian</th><th>Pertanyaan yang Dijawab</th></tr></thead><tbody>
<tr><td>Pasar</td><td>Berapa wisatawan, berapa yang mungkin datang, berapa harga yang sanggup dibayar?</td></tr>
<tr><td>Teknis dan operasional</td><td>Apa yang dibangun, kapasitas, jam operasi, tenaga kerja, keselamatan</td></tr>
<tr><td>Legal dan lahan</td><td>Status lahan, jangka waktu sewa, izin yang dibutuhkan</td></tr>
<tr><td>Biaya investasi</td><td>Konstruksi, peralatan, perizinan, modal kerja awal</td></tr>
<tr><td>Proyeksi keuangan</td><td>Pendapatan, biaya, arus kas, titik impas, NPV, IRR, payback</td></tr>
<tr><td>Risiko dan sensitivitas</td><td>Bagaimana bila pengunjung lebih sedikit atau biaya lebih besar?</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Proyek di atas lahan sewa perlu memperhatikan satu hal penting: masa pengembalian investasi harus jauh lebih pendek daripada masa sewa. Bila sewa 20 tahun tetapi payback 18 tahun, ruang untuk kesalahan hampir tidak ada.</p></div>
<h2>Studi Kelayakan Bukan Penilaian Aset</h2>
<p>Studi kelayakan menjawab apakah proyek layak dijalankan. Penilaian aset menjawab berapa nilai tanah, bangunan, atau peralatan pada tanggal tertentu, dan dilakukan oleh penilai berizin (KJPP). Keduanya bisa saling melengkapi, tetapi bukan dokumen yang sama.</p>
<h2>Pertanggungjawaban ke Pemegang Saham</h2>
<p>Setelah proyek berjalan, studi kelayakan menjadi pembanding. Laporan realisasi biaya dan pendapatan per periode dibandingkan dengan rencana, sehingga pemegang saham bisa menilai kinerja manajemen secara objektif.</p>
<div class="pf-fold"><p>Proyek baru sebaiknya dicatat terpisah sejak awal, misalnya dengan pusat biaya atau bahkan PT terpisah, supaya realisasi mudah dibandingkan dengan studi kelayakan.</p></div>
''' + PENUTUP,
  [('Apa beda studi kelayakan dan penilaian KJPP?', 'Studi kelayakan menilai apakah proyek layak dijalankan. Penilaian KJPP menilai nilai aset pada tanggal tertentu.'),
   ('Apakah otoritas kawasan meminta studi kelayakan?', 'Sering diminta sebagai bagian dari kontrak lahan atau perizinan, tergantung kebijakan otoritas setempat.'),
   ('Apa itu IRR dan payback?', 'IRR adalah tingkat imbal hasil proyek, payback adalah lama waktu sampai investasi kembali.')])

A('valuasi-indikatif-vs-valuasi-lengkap',
  'Valuasi Indikatif vs Valuasi Lengkap: Mana yang Dibutuhkan',
  'Valuasi Indikatif vs Valuasi Lengkap: Mana yang Anda Butuhkan?',
  'Butuh nilai usaha cepat untuk penjajakan atau laporan lengkap untuk transaksi? Ini beda valuasi indikatif dan valuasi lengkap, kegunaan, dan keterbatasannya.',
  'valuasi indikatif', CAT, 5, CTA,
  'Halo Pak Ananta, saya ingin tahu kisaran nilai usaha saya. Apakah cukup valuasi indikatif?',
  [MAPPI, OJK],
  ['valuasi-perusahaan-swasta-dcf-multiple-ebitda', 'cara-menghitung-wacc-dan-valuasi-dcf-perusahaan-indonesia', 'valuasi-rumah-sakit-swasta', 'cara-menjual-perusahaan-atau-sebagian-saham'],
  '''
<p>Pertanyaan "berapa nilai usaha saya?" bisa dijawab dengan dua cara. Cara cepat dengan data yang ada, atau cara lengkap dengan data yang sudah diperiksa. Keduanya berguna, asalkan dipakai untuk keperluan yang tepat.</p>
<h2>Perbandingan</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th></th><th>Valuasi Indikatif</th><th>Valuasi Lengkap</th></tr></thead><tbody>
<tr><td>Data</td><td>Data dari pemilik apa adanya</td><td>Laporan keuangan yang sudah dirapikan atau diaudit</td></tr>
<tr><td>Metode</td><td>Satu atau dua pendekatan sederhana</td><td>Beberapa pendekatan, dengan normalisasi dan sensitivitas</td></tr>
<tr><td>Hasil</td><td>Rentang nilai awal</td><td>Laporan dengan asumsi dan analisis terdokumentasi</td></tr>
<tr><td>Kegunaan</td><td>Keputusan internal, penjajakan awal</td><td>Negosiasi, transaksi, pemegang saham, bank</td></tr>
</tbody></table></div>
<h2>Kapan Indikatif Sudah Cukup</h2>
<ul>
<li>Pemilik ingin tahu kisaran sebelum memutuskan menjual atau tidak.</li>
<li>Penjajakan awal dengan calon investor, sebelum ada term sheet.</li>
<li>Perencanaan internal, misalnya pembagian saham keluarga.</li>
</ul>
<h2>Kapan Perlu Valuasi Lengkap</h2>
<ul>
<li>Transaksi jual beli saham sudah serius.</li>
<li>Investor meminta dasar perhitungan yang bisa diuji.</li>
<li>Ada pemegang saham yang perlu diyakinkan, misalnya saat ada perbedaan pendapat.</li>
<li>Dibutuhkan untuk keperluan yang diatur, misalnya transaksi perusahaan terbuka, yang umumnya memerlukan penilai berizin.</li>
</ul>
<div class="pf-fold"><p>Valuasi indikatif memakai angka dari pemilik apa adanya. Bila angka itu belum akurat, hasilnya juga belum akurat. Karena itu laporan indikatif selalu menuliskan keterbatasannya dengan jelas. Banyak pemilik memulai dari indikatif, lalu meningkatkan ke lengkap setelah laporan keuangan dirapikan.</p></div>
<h2>Jalur yang Paling Hemat</h2>
<p>Bila tujuan akhirnya transaksi, menyusun laporan keuangan lebih dulu lalu langsung valuasi lengkap biasanya lebih hemat daripada indikatif yang kemudian diulang.</p>
''' + PENUTUP,
  [('Apakah valuasi indikatif bisa dipakai bernegosiasi?', 'Bisa sebagai gambaran awal, tetapi investor serius umumnya meminta dasar yang lebih kuat sebelum sepakat harga.'),
   ('Berapa lama valuasi indikatif?', 'Relatif singkat bila data dasar tersedia, karena tidak ada pemeriksaan data mendalam.'),
   ('Kapan wajib memakai penilai berizin?', 'Untuk keperluan yang diatur peraturan, misalnya transaksi tertentu perusahaan terbuka atau penjaminan tertentu.')])

A('menentukan-harga-saham-usaha-keluarga-partner-baru',
  'Menentukan Harga Saham Usaha Keluarga untuk Partner Baru',
  'Masuk Partner Baru: Cara Menentukan Harga Saham Usaha Keluarga',
  'Partner atau investor ingin masuk ke usaha keluarga? Ini cara menentukan harga saham yang adil, pilihan setor modal atau beli saham, dan perjanjiannya.',
  'harga saham usaha keluarga', CAT, 6, CTA,
  'Halo Pak Ananta, ada partner yang ingin masuk ke usaha keluarga kami. Saya ingin tahu cara menentukan harga sahamnya.',
  [OJK, IAI],
  ['cara-menjual-perusahaan-atau-sebagian-saham', 'valuasi-perusahaan-swasta-dcf-multiple-ebitda', 'usaha-keluarga-siap-ipo-langkah-awal', 'private-equity-vs-utang-bank'],
  '''
<p>Usaha keluarga yang berkembang sering menarik orang luar: pemasok yang ingin terlibat, rekan bisnis yang punya jaringan, atau investor yang membawa modal. Begitu pembicaraan menyentuh porsi saham, muncul pertanyaan sulit: berapa harga yang adil?</p>
<h2>Dua Cara Partner Masuk</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th></th><th>Setor Modal Baru</th><th>Beli Saham Pemilik Lama</th></tr></thead><tbody>
<tr><td>Uang masuk ke</td><td>Perusahaan</td><td>Pemilik lama</td></tr>
<tr><td>Dampak ke perusahaan</td><td>Kas bertambah untuk ekspansi</td><td>Kas perusahaan tidak berubah</td></tr>
<tr><td>Cocok bila</td><td>Perusahaan butuh dana tumbuh</td><td>Pemilik ingin mencairkan sebagian nilai</td></tr>
</tbody></table></div>
<h2>Nilai Sebelum dan Sesudah Dana Masuk</h2>
<p>Pada setor modal baru, ada dua angka penting: nilai perusahaan sebelum dana masuk (pre-money) dan sesudahnya (post-money). Misalnya nilai usaha disepakati Rp8 miliar, partner menyetor Rp2 miliar, maka nilai sesudahnya Rp10 miliar dan partner memiliki 20 persen.</p>
<div class="pf-fold"><p>Banyak salah paham terjadi karena kedua pihak memakai angka berbeda. Pemilik menganggap Rp8 miliar sudah termasuk dana partner, partner menganggap sebaliknya. Tuliskan dengan jelas sejak awal mana nilai sebelum dan mana sesudah.</p></div>
<h2>Menentukan Nilai yang Adil</h2>
<ol>
<li>Susun laporan keuangan yang mencerminkan kondisi sebenarnya.</li>
<li>Normalisasi: pisahkan biaya pribadi keluarga, hitung gaji wajar anggota keluarga yang bekerja.</li>
<li>Hitung nilai dengan pendekatan pendapatan dan aset.</li>
<li>Diskusikan rentang nilai, bukan satu angka.</li>
</ol>
<h2>Hal di Luar Harga</h2>
<ul>
<li>Hak suara dan kursi di direksi atau komisaris.</li>
<li>Pembagian dividen.</li>
<li>Hak keluar dan hak beli lebih dulu bila salah satu pihak menjual.</li>
<li>Peran partner dalam operasional.</li>
</ul>
<div class="pf-fold"><p>Perjanjian pemegang saham yang jelas sering lebih penting daripada selisih harga beberapa persen. Banyak usaha keluarga retak bukan karena harga, tetapi karena peran dan hak yang tidak ditulis di awal. Perjanjiannya disusun bersama notaris atau kuasa hukum.</p></div>
''' + PENUTUP,
  [('Apa beda pre-money dan post-money?', 'Pre-money adalah nilai perusahaan sebelum dana partner masuk, post-money adalah nilai setelah ditambah dana tersebut.'),
   ('Lebih baik setor modal atau beli saham?', 'Setor modal cocok bila perusahaan butuh dana, beli saham cocok bila pemilik ingin mencairkan sebagian nilainya.'),
   ('Perlukah perjanjian pemegang saham?', 'Sangat disarankan, untuk mengatur hak suara, dividen, peran, dan hak keluar.')])
