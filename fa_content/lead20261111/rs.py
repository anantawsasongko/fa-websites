from _a import A

CAT = 'Rumah Sakit'
CTA = ('/konsultan-rumah-sakit/', 'Konsultan Rumah Sakit')
SRC_KEMKES = ('https://kemkes.go.id/', 'Kementerian Kesehatan RI')

A('pendampingan-keuangan-rsia-90-hari-pertama',
  'Pendampingan Keuangan RSIA: Yang Dikerjakan di 90 Hari Pertama',
  'Pendampingan Keuangan RSIA: Apa yang Dikerjakan di 90 Hari Pertama',
  'Pemilik RSIA ingin keuangan lebih sehat tapi bingung mulai dari mana? Ini urutan kerja pendampingan 90 hari: diagnosa, unit cost, klaim, dan arus kas.',
  'pendampingan keuangan rumah sakit ibu dan anak', CAT, 7, CTA,
  'Halo Pak Ananta, saya pengelola RSIA dan ingin diskusi pendampingan keuangan rumah sakit.',
  [SRC_KEMKES, ('https://www.bpjs-kesehatan.go.id/', 'BPJS Kesehatan')],
  ['cara-menghitung-unit-cost-rumah-sakit', 'piutang-klaim-bpjs-dan-arus-kas-rumah-sakit', 'konsultan-rumah-sakit-swasta-kapan-dibutuhkan', 'strategi-rumah-sakit-swasta-bertahan'],
  '''
<p>Rumah sakit ibu dan anak (RSIA) punya pola keuangan yang khas. Pendapatan sangat bergantung pada persalinan, layanan neonatal, dan poli anak, sementara biaya tetap seperti dokter jaga, perawat, dan NICU berjalan setiap hari. Ketika jumlah persalinan turun sedikit saja atau klaim BPJS tertahan, kas langsung terasa sesak. Karena itu pemilik RSIA yang meminta pendampingan biasanya datang dengan pertanyaan sederhana: mulai dari mana?</p>
<p>Jawabannya bukan langsung memotong biaya. Urutan yang aman adalah memahami angka dulu, baru memutuskan.</p>
<h2>Bulan Pertama: Diagnosa Angka</h2>
<ul>
<li><b>Laporan keuangan 2 tahun terakhir dan tahun berjalan.</b> Dibaca bersama mutasi rekening, supaya terlihat apakah laba di laporan benar-benar menjadi kas.</li>
<li><b>Pendapatan per layanan.</b> Persalinan normal, sectio, rawat inap anak, NICU, poli, farmasi. Banyak RSIA belum memisahkan angka ini dengan rapi.</li>
<li><b>Umur piutang klaim.</b> Klaim yang pending, dispute, dan belum diajukan dipetakan per bulan.</li>
<li><b>Struktur biaya tetap.</b> Jasa medis, gaji, sewa, cicilan bank, dan kontrak vendor.</li>
</ul>
<p>Hasil bulan pertama adalah satu peta: layanan mana yang menghidupi rumah sakit, mana yang menyedot kas, dan berapa lama rumah sakit bisa bertahan bila klaim tertahan.</p>
<h2>Bulan Kedua: Unit Cost dan Tarif</h2>
<p>Setelah peta jelas, unit cost dihitung untuk layanan utama. Untuk RSIA, yang paling menentukan biasanya sectio caesarea, persalinan normal, dan perawatan bayi di NICU. Unit cost dibandingkan dengan tarif INA-CBG dan tarif pasien umum.</p>
<div class="pf-fold"><p>Dari perbandingan ini sering muncul temuan yang tidak terduga. Misalnya, layanan yang ramai ternyata margin tipis karena pemakaian bahan habis pakai tidak terkendali, atau layanan pasien umum dihargai terlalu rendah dibanding rumah sakit sekitar. Keputusan tarif, kontrak jasa medis, dan negosiasi vendor diambil dari angka ini, bukan dari perasaan.</p>
<p>Pada tahap ini juga diperiksa kualitas koding dan resume medis, karena klaim yang dikembalikan sering berawal dari dokumen, bukan dari layanan medisnya.</p></div>
<h2>Bulan Ketiga: Arus Kas dan Rencana Pendanaan</h2>
<p>Bulan ketiga menyusun proyeksi arus kas 12 bulan dengan tiga skenario: klaim lancar, klaim tertunda dua bulan, dan jumlah pasien turun. Dari sini terlihat apakah rumah sakit perlu fasilitas modal kerja, restrukturisasi cicilan, atau cukup dengan disiplin penagihan.</p>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Bulan</th><th>Fokus</th><th>Hasil yang Diserahkan</th></tr></thead><tbody>
<tr><td>1</td><td>Diagnosa laporan keuangan, kas, piutang klaim</td><td>Peta kesehatan keuangan dan daftar prioritas</td></tr>
<tr><td>2</td><td>Unit cost layanan utama, tarif, koding</td><td>Tabel margin per layanan dan usulan tarif</td></tr>
<tr><td>3</td><td>Proyeksi arus kas, pendanaan</td><td>Rencana kas 12 bulan dan opsi pembiayaan</td></tr>
</tbody></table></div>
<h2>Siapa yang Perlu Terlibat dari Rumah Sakit</h2>
<p>Pendampingan berjalan cepat bila ada tiga orang yang bisa diajak bicara rutin: pemilik atau direktur, kepala keuangan, dan kepala casemix atau rekam medis. Rapat mingguan singkat lebih efektif daripada laporan panjang di akhir.</p>
<h2>Cara Tim FA Indonesia Bekerja</h2>
<p>Tim Rumah Sakit FA Indonesia terdiri dari orang yang pernah memegang langsung keuangan dan manajemen rumah sakit, sehingga bahasa yang dipakai adalah bahasa pengelola, bukan teori. Diskusi awal bisa dilakukan secara online, lalu proposal disusun sesuai kondisi rumah sakit. Data rumah sakit dijaga kerahasiaannya sejak percakapan pertama.</p>
''',
  [('Berapa lama pendampingan keuangan RSIA yang wajar?', 'Tiga bulan cukup untuk diagnosa, unit cost, dan rencana kas. Setelah itu banyak rumah sakit melanjutkan pendampingan bulanan yang lebih ringan.'),
   ('Apakah data rumah sakit aman?', 'Pendampingan dimulai dengan perjanjian kerahasiaan. Nama dan data rumah sakit tidak dipakai untuk keperluan lain.'),
   ('Apakah bisa dilakukan online?', 'Bisa. Sebagian besar diskusi dan pengolahan data dilakukan online, kunjungan dilakukan bila memang diperlukan.')])

A('menjual-rumah-sakit-dan-klinik-di-beberapa-pt',
  'Menjual RS dan Klinik yang Terpisah di Beberapa PT',
  'Menjual Rumah Sakit dan Klinik yang Terpisah di Beberapa PT: Cara Menyiapkan Datanya',
  'Pemilik grup RS dan klinik sering punya beberapa PT. Ini cara menyatukan akta, laporan keuangan, dan penilaian aset supaya calon pembeli mudah menilai.',
  'menjual rumah sakit beberapa PT', CAT, 7, ('/menjual-rumah-sakit/', 'Menjual Rumah Sakit'),
  'Halo Pak Ananta, kami berencana menjual rumah sakit dan klinik yang ada di beberapa PT. Ingin diskusi persiapannya.',
  [SRC_KEMKES, ('https://www.ojk.go.id/', 'Otoritas Jasa Keuangan, daftar penilai')],
  ['menjual-rumah-sakit-persiapan-sisi-penjual', 'harga-jual-rumah-sakit-cara-menghitung', 'jual-rsia-rumah-sakit-ibu-dan-anak', 'due-diligence-akuisisi-rumah-sakit-swasta'],
  '''
<p>Banyak grup kesehatan tumbuh secara bertahap. Rumah sakit pertama berdiri di satu PT, klinik di kota sebelah memakai PT lain, lalu rumah sakit kedua dibeli lewat PT ketiga. Saat pemilik memutuskan menjual, sebagian atau seluruhnya, struktur ini menjadi pertanyaan pertama calon pembeli: apa sebenarnya yang dijual?</p>
<h2>Petakan Dulu Struktur Grup</h2>
<p>Sebelum bicara harga, buat satu halaman yang menjelaskan setiap PT: nama, pemegang saham, unit yang dimiliki (rumah sakit, klinik, tanah, bangunan), izin yang melekat, dan hubungan antar PT. Hal yang sering terlewat:</p>
<ul>
<li>Tanah dan bangunan rumah sakit tercatat atas nama PT berbeda, atau atas nama pribadi pemilik.</li>
<li>Satu PT memegang izin klinik, tetapi pendapatannya masuk ke rekening PT lain.</li>
<li>Ada utang atau jaminan silang antar PT di bank yang sama.</li>
</ul>
<h2>Tiga Dokumen Inti per PT</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Dokumen</th><th>Kenapa Penting</th><th>Catatan</th></tr></thead><tbody>
<tr><td>Akta pendirian dan perubahan terakhir</td><td>Menunjukkan siapa pemilik sah dan kewenangan direksi</td><td>Pastikan sudah tercatat di sistem AHU</td></tr>
<tr><td>Laporan keuangan 2 tahun + tahun berjalan</td><td>Dasar menghitung EBITDA dan nilai usaha</td><td>Sebaiknya per PT, lalu digabung</td></tr>
<tr><td>Laporan penilaian aset (KJPP)</td><td>Dasar nilai tanah, bangunan, alat medis</td><td>Taksasi bank tidak sama dengan laporan KJPP</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Bila hanya satu PT yang punya laporan KJPP, bukan berarti penjualan harus ditunda. Nilai aset PT lain bisa digambarkan dulu dari harga perolehan dan kondisi fisiknya, lalu penilaian KJPP dilengkapi saat calon pembeli sudah serius. Yang penting, angka indikatif ditulis sebagai indikatif, tidak dicampur dengan nilai yang sudah dinilai penilai berizin.</p></div>
<h2>Laporan Keuangan Gabungan untuk Pembeli</h2>
<p>Calon pembeli menilai grup sebagai satu kesatuan. Karena itu setelah laporan per PT rapi, disusun laporan gabungan sederhana: pendapatan, biaya, dan EBITDA seluruh unit, dengan transaksi antar PT dieliminasi. Ini bukan laporan konsolidasi resmi, tetapi alat bantu supaya pembeli langsung melihat skala bisnis.</p>
<div class="pf-fold"><p>Transaksi yang perlu dieliminasi misalnya sewa gedung antar PT, jasa manajemen, atau rujukan pasien yang ditagihkan antar unit. Tanpa eliminasi, pendapatan grup terlihat lebih besar dari sebenarnya, dan pembeli yang teliti akan menemukannya saat due diligence.</p></div>
<h2>Pilihan Struktur Penjualan</h2>
<ul>
<li><b>Jual saham per PT.</b> Paling sederhana bila tiap unit berdiri sendiri.</li>
<li><b>Gabungkan dulu ke satu induk.</b> Cocok bila pembeli ingin membeli seluruh grup.</li>
<li><b>Jual aset.</b> Dipilih bila PT punya riwayat utang atau pajak yang ingin dipisahkan.</li>
</ul>
<p>Pilihan ini berdampak ke pajak, izin, dan waktu proses, sehingga sebaiknya diputuskan bersama konsultan pajak dan notaris sejak awal.</p>
<h2>Pendampingan Sisi Penjual</h2>
<p>Tim FA Indonesia membantu pemilik dari sisi penjual: merapikan data per PT, menyusun gambaran nilai, menyiapkan ringkasan untuk calon pembeli, dan mendampingi tanya jawab due diligence. Kerahasiaan dijaga dengan NDA sebelum data dibuka ke pihak mana pun.</p>
''',
  [('Apakah harus punya laporan KJPP untuk semua PT?', 'Tidak harus di awal. Nilai indikatif bisa dipakai untuk penjajakan, lalu laporan KJPP dilengkapi saat pembeli sudah masuk tahap serius.'),
   ('Apakah taksasi bank bisa dipakai sebagai nilai jual?', 'Taksasi bank dibuat untuk kepentingan agunan dan biasanya konservatif. Untuk transaksi jual beli, pembeli umumnya meminta laporan penilai berizin.'),
   ('Lebih baik jual saham atau aset?', 'Tergantung kondisi PT, riwayat pajak, dan keinginan pembeli. Keputusan ini sebaiknya diambil bersama konsultan pajak dan notaris.')])

A('taksasi-bank-vs-penilaian-kjpp-rumah-sakit',
  'Taksasi Bank vs Penilaian KJPP Rumah Sakit: Bedanya',
  'Taksasi Bank vs Penilaian KJPP untuk Rumah Sakit: Mana yang Dipakai Saat Menjual?',
  'Taksasi bank dan laporan KJPP sering berbeda jauh. Pahami tujuan, metode, dan kapan masing-masing dipakai saat menjual atau membiayai rumah sakit.',
  'taksasi bank vs kjpp rumah sakit', CAT, 6, ('/menjual-rumah-sakit/', 'Menjual Rumah Sakit'),
  'Halo Pak Ananta, saya ingin bertanya soal nilai aset rumah sakit kami untuk rencana penjualan.',
  [('https://mappi.or.id/', 'MAPPI, Standar Penilaian Indonesia'), ('https://www.ojk.go.id/', 'Otoritas Jasa Keuangan')],
  ['kapan-perusahaan-butuh-kjpp-jasa-penilai', 'valuasi-rumah-sakit-swasta', 'harga-jual-rumah-sakit-cara-menghitung', 'agunan-kredit-perusahaan-nilai-likuidasi-plafon'],
  '''
<p>Pemilik rumah sakit sering terkejut ketika angka taksasi bank berbeda jauh dengan harga yang dulu dibayar untuk tanah dan bangunan, atau dengan nilai dalam laporan KJPP. Ketiganya tidak salah. Mereka menjawab pertanyaan yang berbeda.</p>
<h2>Tiga Angka, Tiga Pertanyaan</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Angka</th><th>Pertanyaan yang Dijawab</th><th>Ciri Umum</th></tr></thead><tbody>
<tr><td>Harga perolehan</td><td>Berapa yang dulu dibayar?</td><td>Tercatat di laporan keuangan, tidak mengikuti harga pasar</td></tr>
<tr><td>Taksasi internal bank</td><td>Berapa yang aman dijadikan agunan?</td><td>Konservatif, sering memakai nilai likuidasi</td></tr>
<tr><td>Laporan KJPP</td><td>Berapa nilai wajar atau nilai pasarnya?</td><td>Disusun penilai berizin dengan standar penilaian</td></tr>
</tbody></table></div>
<h2>Kenapa Taksasi Bank Lebih Rendah</h2>
<p>Bank menilai agunan dengan pertanyaan: kalau kredit macet dan aset harus dijual cepat, berapa yang bisa kembali? Bangunan rumah sakit adalah bangunan khusus. Pembelinya terbatas, sehingga bank cenderung memberi potongan besar. Taksasi juga bisa berbeda antar bank karena kebijakan risiko masing-masing.</p>
<div class="pf-fold"><p>Ini sebabnya angka taksasi lama tidak bisa langsung dipakai sebagai patokan harga jual. Taksasi yang dibuat beberapa tahun lalu juga belum memasukkan renovasi, tambahan alat medis, dan perubahan harga tanah di sekitarnya.</p></div>
<h2>Kenapa Pembeli Meminta KJPP</h2>
<p>Calon pembeli, investor, dan bank pembiaya akuisisi umumnya meminta laporan penilai berizin karena metodenya terdokumentasi dan bisa diuji. Untuk rumah sakit, penilai biasanya memisahkan tanah, bangunan, sarana pelengkap, dan alat medis.</p>
<h2>Nilai Aset Bukan Nilai Rumah Sakit</h2>
<p>Hal yang paling penting dipahami pemilik: nilai aset hanyalah satu bagian. Rumah sakit yang sehat dihargai juga dari kemampuannya menghasilkan laba, yaitu dari izin, kerja sama BPJS dan asuransi, dokter, pasien, dan reputasi. Karena itu harga jual rumah sakit biasanya dihitung dari dua sisi: pendekatan aset dan pendekatan pendapatan (EBITDA atau arus kas).</p>
<div class="pf-fold"><p>Bila nilai dari pendekatan pendapatan jauh di atas nilai aset, berarti bisnisnya punya nilai lebih. Bila sebaliknya, pembeli akan cenderung menawar di sekitar nilai aset. Laporan keuangan yang rapi membantu pendekatan pendapatan terlihat meyakinkan.</p></div>
<h2>Urutan yang Disarankan</h2>
<ol>
<li>Kumpulkan harga perolehan dan taksasi yang sudah ada sebagai gambaran awal.</li>
<li>Rapikan laporan keuangan supaya EBITDA bisa dihitung.</li>
<li>Hitung nilai indikatif dari dua pendekatan.</li>
<li>Tunjuk KJPP saat calon pembeli sudah serius atau bank meminta.</li>
</ol>
''',
  [('Apakah laporan KJPP wajib untuk menjual rumah sakit?', 'Tidak selalu wajib, tetapi hampir selalu diminta pembeli serius atau bank yang membiayai akuisisi.'),
   ('Berapa lama laporan KJPP berlaku?', 'Laporan penilaian dibuat pada tanggal penilaian tertentu. Untuk transaksi, pembeli biasanya meminta penilaian yang masih baru.'),
   ('Apakah alat medis ikut dinilai?', 'Bisa. Penilai dapat menilai alat medis terpisah dari tanah dan bangunan bila diminta dalam lingkup penugasan.')])

A('memilih-konsultan-rumah-sakit-pertanyaan-pemilik',
  'Memilih Konsultan Rumah Sakit: 8 Pertanyaan Pemilik',
  'Memilih Konsultan Rumah Sakit: 8 Pertanyaan yang Sebaiknya Diajukan Pemilik',
  'Sebelum menunjuk konsultan rumah sakit, ajukan 8 pertanyaan ini: pengalaman nyata, lingkup, data yang diminta, kerahasiaan, dan hasil yang bisa diukur.',
  'memilih konsultan rumah sakit', CAT, 6, CTA,
  'Halo Pak Ananta, kami sedang mencari konsultan untuk rumah sakit kami. Boleh diskusi dulu?',
  [SRC_KEMKES],
  ['konsultan-rumah-sakit-swasta-kapan-dibutuhkan', 'strategi-rumah-sakit-swasta-bertahan', 'indikator-keuangan-rumah-sakit-yang-dilihat-investor', 'manajemen-biaya-rumah-sakit-berbasis-produk'],
  '''
<p>Menunjuk konsultan adalah keputusan yang menyita waktu manajemen dan biaya. Pemilik rumah sakit yang pernah kecewa biasanya bercerita hal yang sama: laporannya tebal, tetapi tidak ada yang berubah di rumah sakit. Delapan pertanyaan berikut membantu menyaring sejak awal.</p>
<h2>Pertanyaan tentang Pengalaman</h2>
<ol>
<li><b>Apakah timnya pernah mengelola rumah sakit secara langsung?</b> Pengalaman sebagai direktur atau kepala keuangan rumah sakit membuat saran lebih membumi.</li>
<li><b>Masalah apa yang pernah diselesaikan, dan bagaimana caranya?</b> Konsultan yang baik bisa bercerita tanpa menyebut nama klien.</li>
</ol>
<h2>Pertanyaan tentang Lingkup</h2>
<ol start="3">
<li><b>Apa saja yang dikerjakan, dan apa yang tidak?</b> Lingkup yang jelas mencegah kekecewaan di tengah jalan.</li>
<li><b>Apa hasil yang diserahkan setiap tahap?</b> Misalnya tabel unit cost, rencana kas, atau draf kebijakan, bukan sekadar presentasi.</li>
<li><b>Data apa yang diminta di awal?</b> Daftar data yang spesifik menandakan konsultan sudah paham pekerjaannya.</li>
</ol>
<div class="pf-fold"><p>Daftar data awal yang wajar untuk pendampingan keuangan biasanya berisi laporan keuangan, mutasi rekening, rincian pendapatan per layanan, umur piutang klaim, daftar kontrak dokter dan vendor, serta struktur organisasi. Bila konsultan tidak meminta data apa pun dan langsung menjanjikan hasil, itu tanda perlu berhati-hati.</p></div>
<h2>Pertanyaan tentang Cara Kerja</h2>
<ol start="6">
<li><b>Bagaimana kerahasiaan data dijaga?</b> Ada NDA, dan nama rumah sakit tidak dipakai sebagai bahan promosi tanpa izin.</li>
<li><b>Siapa yang benar-benar mengerjakan?</b> Pastikan orang yang hadir saat presentasi juga yang mengerjakan.</li>
<li><b>Bagaimana mengukur berhasil atau tidak?</b> Contohnya margin layanan, umur piutang, atau posisi kas di akhir periode.</li>
</ol>
<h2>Tanda yang Perlu Diwaspadai</h2>
<ul>
<li>Menjanjikan angka laba tertentu sebelum melihat data.</li>
<li>Menyebut nama rumah sakit lain yang didampingi, lengkap dengan angkanya.</li>
<li>Proposal sama persis untuk semua rumah sakit.</li>
</ul>
<div class="pf-fold"><p>Konsultan yang menahan diri menyebut nama klien justru menunjukkan ia akan menjaga data rumah sakit Anda dengan cara yang sama. Detail pengalaman bisa dibicarakan dalam pertemuan, tanpa membuka identitas pihak lain.</p></div>
<h2>Diskusi Awal dengan Tim FA Indonesia</h2>
<p>Tim Rumah Sakit FA Indonesia biasanya memulai dengan pertemuan online bersama pemilik dan direksi, mendengarkan masalahnya, lalu menyusun proposal yang lingkup dan hasilnya jelas per tahap.</p>
''',
  [('Kapan rumah sakit sebaiknya memakai konsultan?', 'Saat ada masalah yang berulang tanpa solusi, misalnya kas sering sesak, klaim sering dikembalikan, atau rencana ekspansi dan pendanaan.'),
   ('Apakah konsultan boleh menyebut klien lainnya?', 'Sebaiknya tidak tanpa izin klien. Kerahasiaan adalah bagian dari etika kerja konsultan.'),
   ('Bagaimana bentuk proposal yang baik?', 'Memuat lingkup, tahapan, hasil yang diserahkan, tim, jadwal, dan cara mengukur keberhasilan.')])

A('data-awal-konsultasi-keuangan-rumah-sakit',
  'Data Awal untuk Konsultasi Keuangan Rumah Sakit',
  'Data yang Perlu Disiapkan Sebelum Konsultasi Keuangan Rumah Sakit',
  'Konsultasi keuangan rumah sakit jadi cepat dan tepat bila data awalnya siap. Ini daftar data yang perlu disiapkan, dari laporan keuangan sampai klaim BPJS.',
  'data konsultasi keuangan rumah sakit', CAT, 5, CTA,
  'Halo Pak Ananta, kami ingin konsultasi keuangan rumah sakit. Data apa saja yang perlu kami siapkan?',
  [('https://www.bpjs-kesehatan.go.id/', 'BPJS Kesehatan')],
  ['laporan-keuangan-rumah-sakit-swasta-sesuai-psak', 'piutang-klaim-bpjs-dan-arus-kas-rumah-sakit', 'cara-menghitung-unit-cost-rumah-sakit', 'titik-impas-rumah-sakit-per-dpjp'],
  '''
<p>Pertemuan pertama dengan konsultan sering habis untuk saling bertanya hal dasar. Bila data awal sudah disiapkan, pertemuan pertama bisa langsung membahas masalah dan pilihan solusinya. Daftar berikut tidak harus lengkap sempurna. Kirim yang sudah ada dulu, sisanya menyusul.</p>
<h2>Data Keuangan</h2>
<ul>
<li>Laporan keuangan 2 tahun terakhir dan tahun berjalan sampai bulan terakhir.</li>
<li>Rekening koran semua rekening operasional, termasuk rekening yang menerima pembayaran BPJS dan asuransi.</li>
<li>Daftar pinjaman bank: plafon, sisa pokok, bunga, jatuh tempo, dan agunan.</li>
<li>Rincian utang ke vendor obat dan alat kesehatan.</li>
</ul>
<h2>Data Operasional</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Data</th><th>Dipakai Untuk</th></tr></thead><tbody>
<tr><td>Pendapatan per layanan dan per penjamin (BPJS, asuransi, umum)</td><td>Melihat sumber pendapatan utama dan ketergantungan</td></tr>
<tr><td>Jumlah pasien rawat jalan, rawat inap, BOR, ALOS</td><td>Menilai pemanfaatan kapasitas</td></tr>
<tr><td>Umur piutang klaim, pending, dispute</td><td>Menghitung kas yang tertahan</td></tr>
<tr><td>Kontrak jasa medis dokter</td><td>Menghitung margin per layanan</td></tr>
<tr><td>Daftar karyawan per unit</td><td>Menghitung biaya tenaga per layanan</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Bila sistem informasi rumah sakit bisa mengekspor data ke Excel, itu sangat membantu. Data mentah dari sistem biasanya lebih berguna daripada laporan yang sudah diringkas, karena konsultan bisa mengolahnya sesuai pertanyaan yang muncul.</p></div>
<h2>Data Legal dan Izin</h2>
<ul>
<li>Akta PT dan perubahan terakhir.</li>
<li>Izin operasional dan status akreditasi.</li>
<li>Perjanjian kerja sama BPJS dan asuransi utama.</li>
<li>Status kepemilikan tanah dan bangunan.</li>
</ul>
<h2>Pertanyaan yang Perlu Dijawab Pemilik</h2>
<p>Selain data, konsultan perlu tahu tujuan pemilik. Apakah ingin memperbaiki kas, menambah layanan, mencari pendanaan, mengajak investor, atau menjual? Jawaban ini menentukan analisis mana yang didahulukan.</p>
<div class="pf-fold"><p>Data cukup dikirim melalui folder bersama yang aksesnya dibatasi. Hindari mengirim data pasien yang tidak diperlukan. Untuk analisis keuangan, data agregat per layanan sudah memadai.</p></div>
''',
  [('Apakah semua data harus lengkap sebelum konsultasi?', 'Tidak. Data yang ada dikirim dulu, konsultan akan membantu memetakan data mana yang masih perlu.'),
   ('Apakah data pasien perlu dikirim?', 'Umumnya tidak. Untuk analisis keuangan cukup data agregat per layanan dan per penjamin.'),
   ('Format data apa yang paling membantu?', 'Ekspor Excel dari sistem informasi rumah sakit dan PDF asli rekening koran dari bank.')])
