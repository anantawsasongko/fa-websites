# Artikel SEO UpdateSAK (Eksplor). Teks orisinal; rujukan standar memakai penomoran SAK Online IAI.
# Setiap item: slug, judul, desc, kat, body (HTML), faq [(q, a)], psak (nomor terkait untuk link)
A = []
def add(slug, judul, desc, kat, body, faq, psak=()):
    A.append(dict(slug=slug, judul=judul, desc=desc, kat=kat, body=body, faq=faq, psak=list(psak)))

add("contoh-calk-format-big-4", "Contoh CALK Lengkap Format Auditor Big 4: Catatan 1 Sampai Penutup",
 "Struktur Catatan atas Laporan Keuangan seperti yang dipakai KAP afiliasi Big 4 di Indonesia: Catatan 1 Umum, Catatan 2 Kebijakan Akuntansi Material, Catatan 3 Estimasi, lalu catatan per akun.",
 "CALK",
 """<p>Laporan keuangan audit perusahaan besar di Indonesia, terutama yang diaudit KAP afiliasi Big 4, punya pola Catatan atas Laporan Keuangan (CALK) yang hampir seragam. Kalau Anda membuka laporan keuangan emiten di situs Bursa Efek Indonesia, urutannya hampir selalu sama. Pola ini bisa Anda tiru untuk perusahaan privat agar laporan terlihat siap audit sejak awal.</p>
<h2>Urutan Baku CALK</h2>
<table class="tbl"><thead><tr><th>Catatan</th><th>Judul</th><th>Isi Utama</th></tr></thead><tbody>
<tr><td>1</td><td>Umum</td><td>Pendirian dan akta, kegiatan usaha, domisili, susunan Dewan Komisaris dan Direksi, jumlah karyawan, entitas anak, tanggal penyelesaian laporan keuangan</td></tr>
<tr><td>2</td><td>Ikhtisar Informasi Kebijakan Akuntansi Material</td><td>Dasar penyusunan, perubahan kebijakan dan standar baru, lalu kebijakan per akun: kas, instrumen keuangan, persediaan, aset tetap, sewa, pendapatan, imbalan kerja, pajak, valuta asing, pihak berelasi</td></tr>
<tr><td>3</td><td>Pertimbangan, Estimasi, dan Asumsi Akuntansi yang Signifikan</td><td>Mata uang fungsional, klasifikasi instrumen keuangan, cadangan piutang, umur manfaat aset tetap, asumsi aktuaria, pajak</td></tr>
<tr><td>4 dst.</td><td>Catatan per Akun</td><td>Mengikuti urutan laporan posisi keuangan lalu laba rugi, selalu komparatif dua tahun</td></tr>
<tr><td>Akhir</td><td>Penutup</td><td>Saldo dan transaksi pihak berelasi, manajemen risiko keuangan, manajemen permodalan, standar yang belum berlaku efektif, peristiwa setelah periode pelaporan</td></tr>
</tbody></table>
<h2>Catatan 1: Yang Sering Terlewat</h2>
<ul><li>Nomor dan tanggal akta perubahan anggaran dasar terakhir beserta SK atau surat penerimaan pemberitahuan dari Kementerian Hukum.</li><li>Tanggal laporan keuangan diotorisasi untuk terbit oleh Direksi. Tanggal ini menjadi batas peristiwa setelah periode pelaporan.</li><li>Jumlah karyawan tetap untuk dua tahun.</li></ul>
<h2>Catatan 2: Tulis Yang Material Saja</h2>
<p>Sejak amendemen standar penyajian, judulnya berubah menjadi <b>ikhtisar informasi kebijakan akuntansi material</b>. Artinya Anda tidak perlu menyalin seluruh standar. Tulis kebijakan yang benar-benar dipakai perusahaan, misalnya metode biaya persediaan, umur manfaat per kelompok aset tetap, dan kapan pendapatan diakui.</p>
<h2>Catatan per Akun: Selalu Komparatif</h2>
<p>Setiap catatan akun berisi tabel dua kolom (tahun berjalan dan tahun lalu), lalu narasi: rincian per bank, umur piutang, mutasi cadangan, mutasi aset tetap per kelompok, jaminan kredit, suku bunga, dan covenant. Auditor akan mencocokkan setiap angka ke kertas kerja, jadi pastikan totalnya sama persis dengan laporan posisi keuangan.</p>
<h2>Cara Cepat Menyusun</h2>
<ol><li>Isi neraca dan laba rugi dua tahun di Kalkulator CALK UpdateSAK.</li><li>Lengkapi data Catatan 1.</li><li>Salin hasil ke Word, lalu isi bagian bertanda kuning dengan data riil.</li><li>Cocokkan nomor catatan di laporan posisi keuangan dengan nomor di CALK.</li></ol>""",
 [("Apakah urutan CALK wajib sama dengan Big 4?", "Tidak wajib. Standar hanya mengatur isi minimum dan urutan yang sistematis. Pola Big 4 dipakai luas karena mudah ditelusuri auditor dan pembaca."),
  ("Apa beda kebijakan akuntansi signifikan dan material?", "Amendemen standar penyajian mengganti istilah signifikan dengan material dan menekankan agar hanya kebijakan yang relevan bagi pembaca yang diungkapkan, bukan salinan standar.")],
 [201, 208, 210])

add("penomoran-psak-3-digit", "Penomoran PSAK Baru 3 Digit: Cara Cepat Menghafal 1xx, 2xx, 3xx, 4xx",
 "Tabel lengkap nomor PSAK lama ke nomor baru dan jembatan keledai seri 100 (IFRS), 200 (IAS), 300 (khusus Indonesia), 400 (syariah).",
 "Update SAK",
 """<p>Sejak 1 Januari 2024, Dewan Standar Akuntansi Keuangan IAI mengganti nomor PSAK dan ISAK menjadi tiga digit. Isinya tidak berubah karena penomoran, tetapi semua laporan keuangan, kebijakan akuntansi, dan materi ujian kini memakai nomor baru.</p>
<h2>Jembatan Keledai</h2>
<div class="keys"><div><b>1xx</b><span>Diadopsi dari IFRS. Angka belakang mengikuti nomor IFRS: IFRS 16 menjadi PSAK 116.</span></div><div><b>2xx</b><span>Diadopsi dari IAS. IAS 16 menjadi PSAK 216.</span></div><div><b>3xx</b><span>Khusus Indonesia, tanpa padanan IFRS: PSAK 338 dan PSAK 370.</span></div><div><b>4xx</b><span>SAK Syariah: PSAK 401 dan seterusnya.</span></div></div>
<h2>Tabel Nomor Lama ke Nomor Baru</h2>
{{TABEL_LAMA}}
<h2>Tips Untuk Ujian dan Pekerjaan</h2>
<ul><li>Hafalkan pasangan IFRS atau IAS-nya, nomor PSAK otomatis ketemu.</li><li>Di laporan keuangan, sebut nomor baru. Nomor lama boleh ditulis dalam kurung saat masa transisi untuk memudahkan pembaca.</li><li>Periksa template kebijakan akuntansi lama yang masih menyebut PSAK 71, 72, atau 73.</li></ul>""",
 [("Kapan penomoran PSAK 3 digit berlaku?", "Penomoran baru berlaku sejak 1 Januari 2024 untuk SAK Indonesia."),
  ("Apakah isi PSAK berubah karena penomoran baru?", "Tidak. Penomoran hanya mengubah nomor. Perubahan isi tetap datang dari amendemen atau standar baru.")],
 [201, 109, 115, 116])

add("sak-ep-pengganti-sak-etap", "SAK EP Pengganti SAK ETAP: Perbedaan Utama dan Langkah Transisi",
 "SAK Indonesia untuk Entitas Privat berlaku sejak 1 Januari 2025 menggantikan SAK ETAP. Siapa yang wajib, apa yang berubah, dan langkah transisinya.",
 "Kerangka SAK",
 """<p>Mulai tahun buku 2025, entitas tanpa akuntabilitas publik yang sebelumnya memakai SAK ETAP beralih ke <b>SAK Indonesia untuk Entitas Privat (SAK EP)</b>. SAK EP lebih dekat ke standar internasional untuk entitas kecil dan menengah, sehingga laporan keuangan lebih mudah dibandingkan oleh bank dan investor.</p>
<h2>Siapa Yang Memakai SAK EP</h2>
<ul><li>Perseroan tertutup tanpa akuntabilitas publik.</li><li>Tidak menghimpun dana masyarakat dan tidak sedang menerbitkan efek ke publik.</li><li>Entitas yang memenuhi syarat boleh memilih SAK Indonesia penuh, misalnya karena berencana IPO.</li></ul>
<h2>Area Yang Paling Terasa Berubah</h2>
<table class="tbl"><thead><tr><th>Area</th><th>Dampak Praktis</th></tr></thead><tbody>
<tr><td>Instrumen keuangan</td><td>Pemisahan instrumen dasar dan lainnya, pengukuran biaya perolehan diamortisasi</td></tr>
<tr><td>Penurunan nilai piutang</td><td>Perlu dasar perhitungan cadangan yang terdokumentasi</td></tr>
<tr><td>Pajak penghasilan</td><td>Pajak tangguhan diakui</td></tr>
<tr><td>Imbalan kerja</td><td>Liabilitas imbalan pascakerja dihitung dengan dasar aktuaria</td></tr>
<tr><td>Penyajian</td><td>Komponen laporan lebih lengkap, termasuk laporan arus kas dan CALK</td></tr>
</tbody></table>
<h2>Langkah Transisi</h2>
<ol><li>Tetapkan tanggal transisi, yaitu awal periode komparatif.</li><li>Susun neraca pembukaan sesuai SAK EP dan rekonsiliasi ekuitas dari SAK ETAP.</li><li>Perbarui kebijakan akuntansi di Catatan 2.</li><li>Ungkapkan dampak transisi di CALK.</li></ol>
<p>Belum yakin kerangka mana yang tepat? Masukkan angka perusahaan di Kalkulator Standar Akuntansi UpdateSAK.</p>""",
 [("Apakah SAK ETAP masih boleh dipakai di 2026?", "SAK ETAP digantikan SAK EP yang berlaku sejak 1 Januari 2025, sehingga laporan keuangan tahun buku 2025 dan seterusnya memakai SAK EP."),
  ("Apakah perusahaan privat boleh memakai SAK Indonesia penuh?", "Boleh. Perusahaan yang berencana IPO atau menjadi entitas anak grup SAK Indonesia sering memilih SAK Indonesia penuh.")],
 [109, 212, 219])

add("sak-emkm-kriteria-umkm", "SAK EMKM dan Kriteria UMKM PP 7/2021: Siapa Yang Boleh Memakai",
 "Batas hasil penjualan dan modal usaha untuk usaha mikro, kecil, dan menengah menurut PP 7/2021, serta kapan SAK EMKM cocok dan kapan sebaiknya naik ke SAK EP.",
 "Kerangka SAK",
 """<p>SAK EMKM disusun untuk usaha mikro, kecil, dan menengah. Kriteria UMKM mengacu Peraturan Pemerintah Nomor 7 Tahun 2021, yang memakai modal usaha (tidak termasuk tanah dan bangunan) atau hasil penjualan tahunan.</p>
<h2>Kriteria UMKM</h2>
<table class="tbl"><thead><tr><th>Skala</th><th>Modal Usaha</th><th>Hasil Penjualan Tahunan</th></tr></thead><tbody>
<tr><td>Mikro</td><td>Sampai Rp1 miliar</td><td>Sampai Rp2 miliar</td></tr>
<tr><td>Kecil</td><td>Di atas Rp1 miliar sampai Rp5 miliar</td><td>Di atas Rp2 miliar sampai Rp15 miliar</td></tr>
<tr><td>Menengah</td><td>Di atas Rp5 miliar sampai Rp10 miliar</td><td>Di atas Rp15 miliar sampai Rp50 miliar</td></tr>
</tbody></table>
<h2>Kapan Cukup SAK EMKM</h2>
<ul><li>Laporan keuangan dipakai untuk pajak dan pemilik sendiri.</li><li>Belum mengajukan kredit bank skala menengah.</li><li>Transaksi sederhana: kas, piutang, persediaan, aset tetap.</li></ul>
<h2>Kapan Sebaiknya Naik ke SAK EP</h2>
<ul><li>Mengajukan kredit bank dengan plafon besar atau mencari investor.</li><li>Punya entitas anak atau transaksi valuta asing yang signifikan.</li><li>Hasil penjualan mendekati Rp50 miliar.</li></ul>""",
 [("Apakah usaha menengah boleh memakai SAK EMKM?", "Boleh selama memenuhi kriteria UMKM. Namun bila laporan keuangan dipakai untuk kredit bank atau investor, SAK EP lebih kuat."),
  ("Apa dasar hukum kriteria UMKM terbaru?", "Kriteria UMKM diatur dalam Peraturan Pemerintah Nomor 7 Tahun 2021 sebagai pelaksanaan UU Cipta Kerja.")],
 [])

add("kapan-pt-wajib-audit", "Kapan Laporan Keuangan PT Wajib Diaudit? Pasal 68 UU PT",
 "Kriteria wajib audit akuntan publik untuk perseroan terbatas menurut Pasal 68 UU 40/2007: dana masyarakat, surat utang, Tbk, Persero, dan aset atau peredaran usaha Rp50 miliar.",
 "Audit",
 """<p>Pasal 68 Undang-Undang Nomor 40 Tahun 2007 tentang Perseroan Terbatas mewajibkan Direksi menyerahkan laporan keuangan kepada akuntan publik untuk diaudit bila perseroan memenuhi salah satu kriteria berikut.</p>
<div class="keys"><div><b>1</b><span>Kegiatan usaha menghimpun dan/atau mengelola dana masyarakat</span></div><div><b>2</b><span>Menerbitkan surat pengakuan utang kepada masyarakat</span></div><div><b>3</b><span>Perseroan Terbuka</span></div><div><b>4</b><span>Persero (BUMN)</span></div><div><b>5</b><span>Aset dan/atau peredaran usaha paling sedikit Rp50 miliar</span></div><div><b>6</b><span>Diwajibkan peraturan perundang-undangan lain</span></div></div>
<h2>Di Luar Kewajiban Hukum</h2>
<p>Banyak perusahaan di bawah Rp50 miliar tetap diaudit karena diminta bank untuk kredit, oleh calon investor, atau mitra usaha. Audit sukarela juga melatih tim keuangan menyiapkan dokumen sesuai standar.</p>
<h2>Persiapan Sebelum Memanggil Auditor</h2>
<ol><li>Pastikan neraca balance dan saldo awal sama dengan laporan audit atau laporan tahun lalu.</li><li>Rekonsiliasi bank, piutang, utang, dan aset tetap.</li><li>Siapkan CALK lengkap dengan kebijakan akuntansi.</li><li>Siapkan daftar dokumen pendukung (PBC).</li></ol>
<p>Kalkulator Standar Akuntansi UpdateSAK otomatis menandai apakah perusahaan Anda masuk kriteria wajib audit Pasal 68.</p>""",
 [("Apakah aset Rp50 miliar dihitung dari total aset?", "Ya, kriteria memakai jumlah aset dan/atau peredaran usaha paling sedikit Rp50 miliar."),
  ("Apa akibat laporan keuangan wajib audit yang tidak diaudit?", "UU PT mengatur bahwa laporan keuangan yang wajib diaudit tetapi tidak diaudit tidak disahkan oleh RUPS.")],
 [201])

add("contoh-laba-rugi-psak-118", "Contoh Laporan Laba Rugi PSAK 118: Kategori Operasi, Investasi, Pendanaan",
 "Ilustrasi angka laporan laba rugi format PSAK 118 yang berlaku 1 Januari 2027, subtotal laba operasi, dan apa yang harus disiapkan dari sekarang.",
 "Update SAK",
 """<p>PSAK 118 menggantikan PSAK 201 mulai 1 Januari 2027. Perubahan paling terlihat ada di laporan laba rugi: setiap penghasilan dan beban masuk ke salah satu kategori, lalu ada subtotal baru yang wajib.</p>
<h2>Kategori dan Subtotal</h2>
<table class="tbl"><thead><tr><th>Pos</th><th class="r">Rp juta</th></tr></thead><tbody>
<tr><td>Pendapatan</td><td class="r">61.500</td></tr><tr><td>Beban pokok pendapatan</td><td class="r">(47.800)</td></tr><tr><td>Beban penjualan dan umum</td><td class="r">(8.500)</td></tr><tr><td>Penghasilan operasi lain</td><td class="r">150</td></tr>
<tr class="t"><td><b>Laba Operasi</b></td><td class="r"><b>5.350</b></td></tr>
<tr><td>Penghasilan investasi (bunga deposito)</td><td class="r">90</td></tr>
<tr class="t"><td><b>Laba Sebelum Pendanaan dan Pajak Penghasilan</b></td><td class="r"><b>5.440</b></td></tr>
<tr><td>Beban pendanaan (bunga utang bank dan sewa)</td><td class="r">(1.050)</td></tr>
<tr class="t"><td><b>Laba Sebelum Pajak</b></td><td class="r"><b>4.390</b></td></tr>
<tr><td>Beban pajak penghasilan</td><td class="r">(970)</td></tr>
<tr class="t"><td><b>Laba Tahun Berjalan</b></td><td class="r"><b>3.420</b></td></tr></tbody></table>
<p>Klasifikasi di atas berlaku untuk entitas yang aktivitas utamanya bukan investasi atau pembiayaan. Bank dan perusahaan pembiayaan punya aturan klasifikasi khusus.</p>
<h2>Ukuran Kinerja Yang Ditetapkan Manajemen</h2>
<p>Bila perusahaan memakai angka seperti EBITDA atau laba disesuaikan di komunikasi publik, PSAK 118 meminta ukuran itu diungkapkan di CALK beserta rekonsiliasinya ke subtotal standar.</p>
<h2>Yang Disiapkan Dari Sekarang</h2>
<ol><li>Petakan setiap akun laba rugi 2026 ke kategori baru, karena 2026 akan menjadi angka komparatif.</li><li>Pisahkan bunga utang dan bunga sewa ke kategori pendanaan.</li><li>Kurangi saldo lain-lain yang tidak jelas.</li></ol>""",
 [("Kapan PSAK 118 berlaku?", "PSAK 118 berlaku untuk periode yang dimulai pada atau setelah 1 Januari 2027 dan diterapkan retrospektif, sehingga angka 2026 disajikan ulang."),
  ("Apakah laporan posisi keuangan juga berubah?", "Perubahan terbesar ada di laporan laba rugi dan pengungkapan. Prinsip agregasi baru juga memengaruhi rincian pos di laporan posisi keuangan.")],
 [118, 201, 207])

add("cara-memilih-kerangka-sak", "Cara Memilih Kerangka SAK: SAK Indonesia, SAK EP, SAK EMKM, atau SAK Syariah",
 "Pohon keputusan memilih kerangka standar akuntansi untuk perusahaan Indonesia berdasarkan akuntabilitas publik, skala usaha, dan transaksi syariah.",
 "Kerangka SAK",
 """<p>Indonesia memakai empat pilar standar akuntansi keuangan. Kesalahan memilih kerangka berakibat laporan keuangan harus disusun ulang saat kredit bank, due diligence investor, atau IPO.</p>
<h2>Tiga Pertanyaan Penentu</h2>
<ol><li><b>Apakah perusahaan memiliki akuntabilitas publik?</b> Perusahaan Tbk, yang sedang IPO, bank, asuransi, dan lembaga yang menghimpun dana masyarakat memakai SAK Indonesia.</li><li><b>Apakah perusahaan masuk kriteria UMKM?</b> Bila ya dan kebutuhan pelaporan sederhana, SAK EMKM cukup.</li><li><b>Selain itu?</b> SAK EP, dengan opsi memilih SAK Indonesia penuh.</li></ol>
<p>Transaksi berbasis akad syariah tunduk pada SAK Syariah (PSAK 4xx) di samping kerangka utamanya.</p>
<h2>Tabel Ringkas</h2>
<table class="tbl"><thead><tr><th>Kerangka</th><th>Untuk</th><th>Kompleksitas</th></tr></thead><tbody>
<tr><td>SAK Indonesia</td><td>Akuntabilitas publik, calon IPO, entitas anak grup</td><td>Tinggi</td></tr>
<tr><td>SAK EP</td><td>Perusahaan privat</td><td>Menengah</td></tr>
<tr><td>SAK EMKM</td><td>Usaha mikro, kecil, menengah</td><td>Rendah</td></tr>
<tr><td>SAK Syariah</td><td>Transaksi akad syariah</td><td>Mengikuti akad</td></tr></tbody></table>""",
 [("Bolehkah memakai SAK Indonesia walau belum IPO?", "Boleh, dan justru disarankan bila IPO direncanakan dalam 2 sampai 3 tahun agar angka historis tidak perlu disajikan ulang."),
  ("Apakah SAK Syariah kerangka tersendiri?", "SAK Syariah mengatur transaksi syariah dan dipakai bersama kerangka utama perusahaan.")],
 [201, 118, 401])

add("kebijakan-akuntansi-material-calk", "Menulis Ikhtisar Informasi Kebijakan Akuntansi Material di CALK",
 "Panduan menulis Catatan 2 CALK: apa yang dianggap material, contoh kalimat per akun, dan kesalahan umum yang dikomentari auditor.",
 "CALK",
 """<p>Catatan 2 sering menjadi bagian terpanjang CALK karena berisi salinan standar. Pendekatan yang benar justru sebaliknya: ungkapkan informasi kebijakan yang material, yaitu yang membantu pembaca memahami angka perusahaan Anda.</p>
<h2>Tanda Kebijakan Itu Material</h2>
<ul><li>Ada pilihan kebijakan (misalnya model biaya atau revaluasi aset tetap).</li><li>Perlakuan khas industri (misalnya pendapatan proyek sepanjang waktu).</li><li>Akun yang nilainya besar atau penuh pertimbangan.</li><li>Perubahan kebijakan di tahun berjalan.</li></ul>
<h2>Contoh Kalimat yang Spesifik</h2>
<table class="tbl"><thead><tr><th>Akun</th><th>Generik (Hindari)</th><th>Spesifik (Pakai)</th></tr></thead><tbody>
<tr><td>Persediaan</td><td>Persediaan diukur sesuai standar yang berlaku.</td><td>Biaya ditentukan dengan rata-rata tertimbang dan diturunkan ke nilai realisasi neto per kelompok produk.</td></tr>
<tr><td>Aset tetap</td><td>Aset tetap disusutkan sesuai umurnya.</td><td>Garis lurus: bangunan 20 tahun, mesin 8 tahun, kendaraan 4 sampai 8 tahun.</td></tr>
<tr><td>Pendapatan</td><td>Pendapatan diakui saat terjadi.</td><td>Diakui saat barang diserahkan ke pelanggan; proyek diakui berdasarkan biaya terjadi terhadap estimasi total biaya.</td></tr></tbody></table>
<h2>Struktur Catatan 2</h2>
<ol><li>Dasar penyusunan dan pernyataan kepatuhan.</li><li>Perubahan kebijakan dan standar baru yang diterapkan.</li><li>Kebijakan per akun sesuai urutan laporan posisi keuangan.</li></ol>""",
 [("Apakah Catatan 2 boleh menyalin isi PSAK?", "Sebaiknya tidak. Standar meminta informasi kebijakan yang material dan spesifik bagi perusahaan, bukan salinan standar."),
  ("Di mana mengungkapkan standar baru yang belum efektif?", "Umumnya di Catatan 2 bagian perubahan kebijakan atau di catatan tersendiri menjelang penutup CALK.")],
 [201, 208])

add("komite-audit-pojk-55-2015", "Komite Audit Menurut POJK 55/POJK.04/2015: Tugas, Syarat, dan Komposisi",
 "Ringkasan pembentukan komite audit emiten dan perusahaan publik: minimal tiga anggota, diketuai komisaris independen, rapat paling sedikit sekali tiga bulan.",
 "Tata Kelola",
 """<p>Emiten dan perusahaan publik wajib memiliki komite audit sesuai POJK Nomor 55/POJK.04/2015 tentang Pembentukan dan Pedoman Pelaksanaan Kerja Komite Audit. Bagi perusahaan yang bersiap IPO, komite audit dibentuk sebelum pencatatan saham.</p>
<h2>Komposisi</h2>
<div class="keys"><div><b>3+</b><span>Anggota paling sedikit tiga orang</span></div><div><b>Ketua</b><span>Komisaris independen</span></div><div><b>Pihak Luar</b><span>Anggota lain dari luar emiten</span></div><div><b>Keuangan</b><span>Minimal satu anggota berlatar akuntansi dan keuangan</span></div></div>
<h2>Tugas Utama</h2>
<ul><li>Menelaah informasi keuangan yang akan diterbitkan.</li><li>Menelaah kepatuhan terhadap peraturan pasar modal.</li><li>Memberi rekomendasi penunjukan akuntan publik.</li><li>Menelaah pelaksanaan audit internal dan eksternal.</li><li>Menelaah pengaduan terkait pelaporan keuangan.</li></ul>
<h2>Rapat</h2>
<p>Komite audit mengadakan rapat paling sedikit satu kali dalam tiga bulan. Risalah rapat didokumentasikan dan ditandatangani.</p>
<h2>Kaitannya dengan Laporan Keuangan</h2>
<p>Komite audit akan membaca CALK. Kebijakan akuntansi material yang jelas dan pengungkapan risiko yang lengkap memudahkan komite menjalankan fungsi telaahnya.</p>""",
 [("Berapa jumlah minimal anggota komite audit?", "Paling sedikit tiga orang yang berasal dari komisaris independen dan pihak dari luar emiten."),
  ("Siapa ketua komite audit?", "Komite audit diketuai oleh komisaris independen.")],
 [])

add("peta-belajar-psak-ujian-ca-cpa", "Peta Belajar PSAK Untuk Ujian CA dan CPA: Standar Berdampak Besar",
 "Urutan belajar PSAK yang efisien untuk persiapan ujian sertifikasi akuntan: mulai dari penyajian, instrumen keuangan, pendapatan, sewa, aset tetap, pajak, dan konsolidasi.",
 "Belajar",
 """<p>Materi standar akuntansi untuk ujian sertifikasi profesi sangat luas. Cara paling efisien adalah mulai dari standar yang muncul di hampir setiap laporan keuangan, lalu ke standar dengan perhitungan yang rumit.</p>
<h2>Urutan Belajar</h2>
<ol><li><b>Fondasi:</b> PSAK 201 (dan PSAK 118 untuk 2027), PSAK 207, PSAK 208, PSAK 210.</li><li><b>Perhitungan inti:</b> PSAK 109 (instrumen keuangan dan ECL), PSAK 115 (pendapatan), PSAK 116 (sewa).</li><li><b>Aset:</b> PSAK 202, PSAK 216, PSAK 236, PSAK 238, PSAK 240.</li><li><b>Liabilitas:</b> PSAK 212 (pajak tangguhan), PSAK 219 (imbalan kerja), PSAK 237 (provisi).</li><li><b>Grup:</b> PSAK 103, PSAK 110, PSAK 228, PSAK 338.</li></ol>
<h2>Teknik</h2>
<ul><li>Hafalkan penomoran 3 digit lewat pasangan IFRS dan IAS.</li><li>Latih jurnal dan angka, bukan definisi.</li><li>Biasakan membaca CALK laporan keuangan emiten untuk melihat penerapan nyata.</li></ul>
<p>Setiap standar di daftar ini punya halaman ringkas di Eksplor UpdateSAK beserta poin yang sering dipersoalkan auditor.</p>""",
 [("PSAK apa yang paling penting dipelajari dulu?", "Mulai dari penyajian laporan keuangan, lalu instrumen keuangan, pendapatan, dan sewa karena muncul di hampir semua laporan keuangan."),
  ("Apakah ujian sudah memakai nomor PSAK baru?", "Gunakan penomoran 3 digit yang berlaku sejak 2024 dan cek ketentuan resmi penyelenggara ujian.")],
 [201, 118, 109, 115, 116, 212])

add("laporan-arus-kas-metode-tidak-langsung", "Menyusun Laporan Arus Kas Metode Tidak Langsung dari Neraca dan Laba Rugi",
 "Langkah praktis menyusun laporan arus kas PSAK 207 metode tidak langsung dari dua neraca dan satu laba rugi, lengkap dengan contoh angka.",
 "Laporan Keuangan",
 """<p>Laporan arus kas metode tidak langsung dimulai dari laba sebelum pajak, lalu disesuaikan dengan pos nonkas dan perubahan modal kerja.</p>
<h2>Langkah</h2>
<ol><li>Mulai dari laba sebelum pajak.</li><li>Tambahkan kembali penyusutan dan amortisasi, beban imbalan kerja, cadangan piutang.</li><li>Keluarkan pendapatan bunga dan beban bunga bila dipisah ke aktivitas investasi atau pendanaan.</li><li>Sesuaikan perubahan piutang, persediaan, uang muka, utang usaha, dan akrual.</li><li>Kurangi pajak penghasilan yang dibayar.</li><li>Aktivitas investasi: perolehan aset tetap (selisih biaya perolehan ditambah penghapusan).</li><li>Aktivitas pendanaan: tambahan dan pembayaran utang bank, pembayaran sewa, dividen.</li></ol>
<h2>Contoh Ringkas (Rp juta)</h2>
<table class="tbl"><tbody>
<tr><td>Laba sebelum pajak</td><td class="r">4.390</td></tr><tr><td>Penyusutan</td><td class="r">1.200</td></tr><tr><td>Beban bunga</td><td class="r">1.050</td></tr>
<tr><td>Kenaikan piutang usaha</td><td class="r">(1.740)</td></tr><tr><td>Kenaikan persediaan</td><td class="r">(800)</td></tr><tr><td>Kenaikan utang usaha</td><td class="r">850</td></tr>
<tr class="t"><td><b>Kas dari operasi sebelum pajak dan bunga</b></td><td class="r"><b>4.950</b></td></tr></tbody></table>
<h2>Cek Akhir</h2>
<p>Kas awal ditambah kenaikan bersih harus sama dengan kas akhir di neraca. Bila tidak sama, biasanya ada transaksi nonkas yang keliru dimasukkan.</p>""",
 [("Apakah perusahaan privat wajib menyusun laporan arus kas?", "Ya, laporan arus kas adalah komponen laporan keuangan lengkap menurut SAK Indonesia dan SAK EP."),
  ("Bunga dibayar masuk aktivitas apa?", "Saat ini ada pilihan kebijakan; mulai PSAK 118 klasifikasinya diatur lebih ketat, umumnya pendanaan untuk entitas nonkeuangan.")],
 [207, 118, 116])

add("rekonsiliasi-tarif-pajak-efektif", "Rekonsiliasi Beban Pajak dan Tarif Efektif 22% di CALK",
 "Cara menyajikan rekonsiliasi antara laba sebelum pajak dikali tarif 22% dengan beban pajak di laporan laba rugi, sesuai PSAK 212.",
 "CALK",
 """<p>Auditor hampir selalu meminta rekonsiliasi tarif efektif. Tujuannya menjelaskan mengapa beban pajak di laporan laba rugi tidak sama dengan 22% dikali laba sebelum pajak.</p>
<h2>Format</h2>
<table class="tbl"><tbody>
<tr><td>Laba sebelum pajak</td><td class="r">4.390</td></tr><tr><td>Beban pajak dengan tarif 22%</td><td class="r">966</td></tr>
<tr><td>Beda tetap (beban tidak dapat dikurangkan)</td><td class="r">20</td></tr><tr><td>Penghasilan final dan bukan objek pajak</td><td class="r">(16)</td></tr>
<tr class="t"><td><b>Beban pajak penghasilan</b></td><td class="r"><b>970</b></td></tr></tbody></table>
<h2>Sumber Selisih Yang Umum</h2>
<ul><li>Beban natura, sumbangan, dan denda yang tidak dapat dikurangkan.</li><li>Penghasilan yang dikenakan PPh final, seperti bunga deposito dan sewa tanah bangunan.</li><li>Aset pajak tangguhan yang tidak diakui.</li><li>Koreksi tahun lalu.</li></ul>
<p>Kalkulator CALK UpdateSAK menyusun tabel rekonsiliasi ini otomatis dari angka laba rugi.</p>""",
 [("Berapa tarif PPh badan yang dipakai?", "Tarif umum PPh badan adalah 22%. Wajib pajak tertentu dapat memperoleh fasilitas pengurangan tarif sesuai ketentuan perpajakan."),
  ("Apakah perusahaan PPh final UMKM perlu rekonsiliasi?", "Perusahaan yang dikenakan PPh final atas peredaran bruto perlu menjelaskan dasar pengenaan pajaknya di CALK.")],
 [212])

add("imbalan-kerja-psak-219-pp-35-2021", "Liabilitas Imbalan Kerja PSAK 219 dan PP 35/2021: Yang Wajib Diungkap",
 "Dasar liabilitas imbalan pascakerja di Indonesia, asumsi aktuaria, dan pengungkapan minimum di CALK.",
 "CALK",
 """<p>Hampir semua perusahaan di Indonesia memiliki liabilitas imbalan pascakerja karena kewajiban pesangon dan uang penghargaan masa kerja menurut UU 6/2023 dan PP 35/2021. Kewajiban ini dihitung dengan metode aktuaria, bukan saat dibayar.</p>
<h2>Asumsi yang Diungkapkan</h2>
<table class="tbl"><thead><tr><th>Asumsi</th><th>Catatan</th></tr></thead><tbody>
<tr><td>Tingkat diskonto</td><td>Mengacu imbal hasil obligasi pemerintah jangka panjang</td></tr>
<tr><td>Kenaikan gaji</td><td>Sesuai kebijakan remunerasi perusahaan</td></tr>
<tr><td>Mortalitas</td><td>Umumnya Tabel Mortalitas Indonesia</td></tr>
<tr><td>Usia pensiun</td><td>Sesuai peraturan perusahaan</td></tr></tbody></table>
<h2>Pengungkapan Minimum</h2>
<ul><li>Nama aktuaris dan tanggal laporan.</li><li>Mutasi liabilitas: saldo awal, biaya jasa, bunga, pembayaran, pengukuran kembali.</li><li>Pengukuran kembali di penghasilan komprehensif lain.</li><li>Analisis sensitivitas tingkat diskonto dan kenaikan gaji.</li></ul>""",
 [("Apakah UMKM juga harus mencatat imbalan kerja?", "Kewajiban pesangon berlaku umum menurut ketentuan ketenagakerjaan; perlakuan akuntansinya mengikuti kerangka SAK yang dipakai."),
  ("Di mana keuntungan atau kerugian aktuaria dicatat?", "Dalam SAK Indonesia, pengukuran kembali diakui di penghasilan komprehensif lain.")],
 [219, 212])

add("matriks-provisi-ecl-piutang-psak-109", "Matriks Provisi ECL Piutang Usaha PSAK 109: Contoh Hitung",
 "Contoh menghitung cadangan kerugian kredit ekspektasian piutang usaha dengan pendekatan sederhana PSAK 109 memakai umur piutang.",
 "Laporan Keuangan",
 """<p>PSAK 109 mengizinkan pendekatan sederhana untuk piutang usaha: cadangan dihitung untuk kerugian kredit sepanjang umur piutang. Cara paling praktis adalah matriks provisi berdasarkan umur piutang.</p>
<h2>Contoh</h2>
<table class="tbl"><thead><tr><th>Umur</th><th class="r">Saldo</th><th class="r">Tingkat Kerugian</th><th class="r">Cadangan</th></tr></thead><tbody>
<tr><td>Belum jatuh tempo</td><td class="r">8.000</td><td class="r">0,5%</td><td class="r">40</td></tr>
<tr><td>1 sampai 30 hari</td><td class="r">2.500</td><td class="r">2%</td><td class="r">50</td></tr>
<tr><td>31 sampai 90 hari</td><td class="r">1.500</td><td class="r">10%</td><td class="r">150</td></tr>
<tr><td>Lebih dari 90 hari</td><td class="r">550</td><td class="r">50%</td><td class="r">275</td></tr>
<tr class="t"><td><b>Jumlah</b></td><td class="r"><b>12.550</b></td><td></td><td class="r"><b>515</b></td></tr></tbody></table>
<h2>Menentukan Tingkat Kerugian</h2>
<ol><li>Hitung tingkat gagal bayar historis per kelompok umur 2 sampai 3 tahun terakhir.</li><li>Sesuaikan dengan informasi masa depan, misalnya kondisi sektor pelanggan.</li><li>Dokumentasikan di kertas kerja sebagai dasar estimasi di Catatan 3.</li></ol>""",
 [("Apakah persentase tetap 1% dari piutang boleh?", "Tidak sesuai PSAK 109 bila tanpa dasar data historis dan informasi masa depan."),
  ("Apakah piutang pihak berelasi juga dicadangkan?", "Ya, piutang pihak berelasi tetap dinilai risiko kreditnya.")],
 [109, 107])

add("contoh-jurnal-psak-116-sewa", "Contoh Jurnal PSAK 116 Sewa Untuk Penyewa",
 "Contoh angka dan jurnal pengakuan aset hak guna dan liabilitas sewa gedung tiga tahun sesuai PSAK 116.",
 "Laporan Keuangan",
 """<p>Penyewa mengakui aset hak guna dan liabilitas sewa untuk hampir semua sewa, kecuali sewa jangka pendek 12 bulan atau kurang dan aset bernilai rendah.</p>
<h2>Fakta</h2>
<p>Sewa gudang 3 tahun, Rp400 juta dibayar setiap akhir tahun, suku bunga pinjaman inkremental 10%.</p>
<h2>Perhitungan</h2>
<table class="tbl"><thead><tr><th>Tahun</th><th class="r">Awal</th><th class="r">Bunga 10%</th><th class="r">Bayar</th><th class="r">Akhir</th></tr></thead><tbody>
<tr><td>1</td><td class="r">994,7</td><td class="r">99,5</td><td class="r">(400)</td><td class="r">694,2</td></tr>
<tr><td>2</td><td class="r">694,2</td><td class="r">69,4</td><td class="r">(400)</td><td class="r">363,6</td></tr>
<tr><td>3</td><td class="r">363,6</td><td class="r">36,4</td><td class="r">(400)</td><td class="r">0</td></tr></tbody></table>
<h2>Jurnal Tahun 1 (Rp juta)</h2>
<table class="tbl"><tbody>
<tr><td>Aset hak guna</td><td class="r">994,7</td><td></td></tr><tr><td class="i">Liabilitas sewa</td><td></td><td class="r">994,7</td></tr>
<tr><td>Beban bunga</td><td class="r">99,5</td><td></td></tr><tr><td>Liabilitas sewa</td><td class="r">300,5</td><td></td></tr><tr><td class="i">Kas</td><td></td><td class="r">400,0</td></tr>
<tr><td>Beban penyusutan</td><td class="r">331,6</td><td></td></tr><tr><td class="i">Akumulasi penyusutan aset hak guna</td><td></td><td class="r">331,6</td></tr></tbody></table>
<p>Di neraca akhir tahun 1, liabilitas sewa Rp694,2 juta dipisah bagian lancar Rp330,6 juta dan jangka panjang Rp363,6 juta.</p>""",
 [("Bagaimana jika sewa dibayar di muka sekaligus?", "Pembayaran di muka menambah aset hak guna; liabilitas sewa hanya untuk pembayaran yang belum dibayar."),
  ("Suku bunga apa yang dipakai?", "Suku bunga implisit sewa bila dapat ditentukan; bila tidak, suku bunga pinjaman inkremental penyewa.")],
 [116, 109, 236])

add("lima-langkah-psak-115-kontraktor", "PSAK 115 Lima Langkah Pengakuan Pendapatan dengan Contoh Kontraktor",
 "Penerapan model lima langkah PSAK 115 untuk kontrak konstruksi: kewajiban pelaksanaan, pengakuan sepanjang waktu, aset dan liabilitas kontrak.",
 "Laporan Keuangan",
 """<p>Kontraktor sering mengakui pendapatan berdasarkan termin tagihan. Menurut PSAK 115, pendapatan proyek umumnya diakui sepanjang waktu berdasarkan progres penyelesaian, bukan tagihan.</p>
<h2>Lima Langkah</h2>
<ol><li><b>Identifikasi kontrak</b>: SPK atau kontrak yang disetujui dan dapat ditagih.</li><li><b>Kewajiban pelaksanaan</b>: biasanya satu kewajiban terintegrasi untuk satu bangunan.</li><li><b>Harga transaksi</b>: nilai kontrak termasuk imbalan variabel yang sangat mungkin tidak berbalik.</li><li><b>Alokasi</b>: ke setiap kewajiban pelaksanaan.</li><li><b>Pengakuan</b>: sepanjang waktu bila pelanggan mengendalikan aset selama dibangun.</li></ol>
<h2>Contoh</h2>
<p>Kontrak Rp10 miliar, estimasi biaya Rp8 miliar, biaya terjadi Rp4 miliar, sudah ditagih Rp3,5 miliar.</p>
<table class="tbl"><tbody><tr><td>Progres (4 ÷ 8)</td><td class="r">50%</td></tr><tr><td>Pendapatan diakui</td><td class="r">5.000</td></tr><tr><td>Tagihan</td><td class="r">3.500</td></tr><tr class="t"><td><b>Aset kontrak</b></td><td class="r"><b>1.500</b></td></tr></tbody></table>
<h2>Yang Diungkap di CALK</h2>
<ul><li>Metode pengukuran progres.</li><li>Saldo aset dan liabilitas kontrak serta perubahannya.</li><li>Kontrak merugi dan provisi terkait.</li></ul>""",
 [("Apakah termin tagihan bisa dipakai sebagai dasar pendapatan?", "Hanya bila termin mencerminkan progres pekerjaan. Bila tidak, gunakan metode input atau output."),
  ("Apa itu aset kontrak?", "Hak atas imbalan untuk pekerjaan yang sudah dilaksanakan tetapi belum dapat ditagih tanpa syarat.")],
 [115, 237])

# ---- Pilar keyword "Update PSAK 2026" (URL root /update-psak-2026/) ----
# ---- Sinergi FA Indonesia / CariAkuntan (28 Okt 2026): analis kredit, RM, dan investor ----
add("checklist-psak-analis-kredit-membaca-laporan-keuangan-debitur", "Checklist PSAK untuk Analis Kredit dan RM: Membaca Laporan Keuangan Calon Debitur",
 "PSAK yang paling sering mengubah angka laporan keuangan calon debitur: cadangan piutang, pengakuan pendapatan proyek, sewa, imbalan kerja, dan klasifikasi utang. Lengkap dengan pertanyaan untuk debitur.",
 "Analisis Kredit",
 """<p>Analis kredit dan RM membaca laporan keuangan untuk menilai kemampuan bayar. Masalahnya, angka yang sama bisa berubah cukup besar tergantung apakah perusahaan sudah menerapkan PSAK dengan benar. Checklist berikut membantu menandai pos yang perlu ditanyakan sebelum menghitung rasio.</p>
<h2>Lima Pos yang Paling Sering Berubah</h2>
<table class="tbl"><thead><tr><th>Pos</th><th>Standar</th><th>Yang Dicek</th><th>Dampak ke Analisis</th></tr></thead><tbody>
<tr><td>Piutang usaha</td><td>PSAK 109</td><td>Ada cadangan kerugian kredit ekspektasian berbasis umur piutang atau hanya persentase tetap</td><td>Aset lancar dan laba bisa turun, current ratio berubah</td></tr>
<tr><td>Pendapatan proyek</td><td>PSAK 115</td><td>Pendapatan kontraktor diakui sesuai kemajuan, bukan saat tagihan</td><td>Laba dan piutang bisa bergeser antar periode</td></tr>
<tr><td>Sewa jangka panjang</td><td>PSAK 116</td><td>Sewa gudang, kantor, atau alat sudah dicatat sebagai aset hak guna dan liabilitas sewa</td><td>Utang naik, DER dan utang terhadap EBITDA berubah</td></tr>
<tr><td>Imbalan kerja</td><td>PSAK 219</td><td>Liabilitas pesangon dan pensiun dihitung aktuaria sesuai PP 35/2021</td><td>Liabilitas tersembunyi yang menurunkan ekuitas</td></tr>
<tr><td>Klasifikasi utang</td><td>PSAK 201</td><td>Utang bank yang covenant-nya dilanggar sudah direklasifikasi menjadi jangka pendek</td><td>Likuiditas jauh lebih ketat dari yang terlihat</td></tr>
</tbody></table>
<h2>Pertanyaan untuk Calon Debitur</h2>
<ol><li>Siapa yang menyusun laporan keuangan dan memakai kerangka SAK apa?</li><li>Bagaimana cadangan piutang dihitung, dan berapa piutang yang lewat 90 hari?</li><li>Apakah ada sewa jangka panjang yang belum tercatat sebagai liabilitas?</li><li>Apakah ada covenant bank lain yang dilanggar di akhir tahun?</li><li>Apakah liabilitas imbalan kerja dihitung aktuaris?</li></ol>
<h2>Mulai 2027: PSAK 118</h2>
<p>Laporan laba rugi entitas yang memakai SAK Indonesia akan disajikan dalam kategori operasi, investasi, dan pendanaan dengan subtotal laba usaha yang baku. Analis perlu menyesuaikan cara mengambil EBIT dan EBITDA dari laporan baru. Contohnya ada di artikel <a href="/artikel/contoh-laba-rugi-psak-118/">contoh laba rugi PSAK 118</a>.</p>
<h2>Kalau Berkas Debitur Belum Siap</h2>
<p>Debitur yang laporan keuangannya belum siap dianalisis bisa dirujuk ke penasihat dari sisi debitur. RM dan Commercial Head dapat melihat <a href="https://faindonesia.co.id/mitra-rm-bank/">kerja sama untuk RM bank di FA Indonesia</a>. Bila bank mensyaratkan audit atau penilaian agunan, debitur bisa memilih KAP dan KJPP berizin lewat <a href="https://cariakuntan.com/artikel/kap-dan-kjpp-untuk-syarat-pencairan-kredit-bank/">CariAkuntan</a>.</p>""",
 [("PSAK apa yang paling sering mengubah angka calon debitur?", "PSAK 109 untuk cadangan piutang, PSAK 115 untuk pendapatan proyek, PSAK 116 untuk sewa, PSAK 219 untuk imbalan kerja, dan PSAK 201 untuk klasifikasi utang."),
  ("Kenapa sewa memengaruhi rasio utang debitur?", "Sejak PSAK 116, sewa jangka panjang dicatat sebagai aset hak guna dan liabilitas sewa, sehingga total utang dan DER naik walaupun tidak ada pinjaman baru."),
  ("Apa dampak PSAK 118 bagi analis kredit?", "Mulai 2027 laba rugi disajikan dalam kategori operasi, investasi, dan pendanaan, sehingga cara mengambil EBIT dan EBITDA dari laporan perlu disesuaikan.")],
 [109, 115, 116, 219, 201, 118])

add("red-flag-psak-due-diligence-calon-investee", "Red Flag PSAK dalam Due Diligence Calon Investee: Panduan untuk Investor dan Analis",
 "Pola penerapan PSAK yang sering membuat laba perusahaan privat terlihat lebih baik dari kenyataannya, dan cara mengujinya sebelum menetapkan harga.",
 "Due Diligence",
 """<p>Dalam transaksi investasi, harga biasanya dihitung dari kelipatan laba. Karena itu, setiap pos yang membuat laba terlihat lebih tinggi akan ikut menaikkan harga. Di perusahaan privat, pola berikut paling sering muncul.</p>
<h2>Pola yang Menaikkan Laba</h2>
<table class="tbl"><thead><tr><th>Pola</th><th>Standar Terkait</th><th>Cara Menguji</th></tr></thead><tbody>
<tr><td>Cadangan piutang terlalu kecil</td><td>PSAK 109</td><td>Bandingkan cadangan dengan umur piutang dan tingkat gagal bayar historis</td></tr>
<tr><td>Pendapatan diakui sebelum kewajiban pelaksanaan selesai</td><td>PSAK 115</td><td>Uji sampel kontrak dan bukti serah terima</td></tr>
<tr><td>Biaya pinjaman dikapitalisasi berlebihan</td><td>PSAK 223</td><td>Cek apakah aset benar memenuhi syarat aset kualifikasian</td></tr>
<tr><td>Persediaan usang tidak diturunkan nilainya</td><td>PSAK 202</td><td>Bandingkan nilai tercatat dengan nilai realisasi neto dan perputaran</td></tr>
<tr><td>Liabilitas imbalan kerja belum dihitung</td><td>PSAK 219</td><td>Minta laporan aktuaria dan rekonsiliasi dengan jumlah karyawan</td></tr>
<tr><td>Transaksi pihak berelasi tidak diungkapkan</td><td>PSAK 224</td><td>Daftar perusahaan keluarga, harga, dan saldo akhir tahun</td></tr>
</tbody></table>
<h2>Pola yang Menyembunyikan Utang</h2>
<ul><li>Sewa jangka panjang yang belum dicatat sesuai PSAK 116.</li><li>Utang ke pemegang saham atau pihak berelasi yang dicatat sebagai ekuitas tanpa perjanjian.</li><li>Jaminan perusahaan untuk utang pihak lain yang tidak diungkapkan.</li></ul>
<h2>Urutan Pengujian yang Efisien</h2>
<ol><li>Mulai dari rekonsiliasi laporan keuangan dengan SPT dan mutasi rekening.</li><li>Normalisasi EBITDA: pisahkan pos tidak berulang dan biaya pribadi pemilik.</li><li>Uji tiga pos dengan dampak terbesar terhadap laba di sektor tersebut.</li><li>Hitung utang bersih termasuk pos yang menyerupai utang.</li></ol>
<h2>Bacaan dan Bantuan Lanjutan</h2>
<p>Daftar red flag dari sisi transaksi ada di artikel <a href="https://faindonesia.co.id/artikel/menilai-kesiapan-calon-investee-sebelum-term-sheet/">7 red flag calon investee</a> di FA Indonesia. Investor yang mencari peluang dengan data yang sudah dirapikan bisa melihat <a href="https://faindonesia.co.id/mitra-investor/">peluang untuk investor</a>. Untuk memilih KAP dan KJPP due diligence yang independen, lihat panduan di <a href="https://cariakuntan.com/artikel/kap-dan-kjpp-untuk-due-diligence-investor/">CariAkuntan</a>.</p>""",
 [("PSAK apa yang paling sering membuat laba perusahaan privat terlihat lebih tinggi?", "Yang sering muncul adalah PSAK 109 untuk cadangan piutang, PSAK 115 untuk pengakuan pendapatan, PSAK 202 untuk penurunan nilai persediaan, PSAK 219 untuk imbalan kerja, dan PSAK 223 untuk kapitalisasi biaya pinjaman."),
  ("Bagaimana menemukan utang tersembunyi calon investee?", "Cek sewa jangka panjang sesuai PSAK 116, utang ke pemegang saham atau pihak berelasi, dan jaminan perusahaan untuk utang pihak lain."),
  ("Apa langkah pertama due diligence keuangan?", "Rekonsiliasi laporan keuangan dengan SPT dan mutasi rekening, lalu normalisasi EBITDA sebelum menguji pos-pos besar.")],
 [109, 115, 116, 202, 219, 223, 224])

add("update-psak-2026", "Update PSAK 2026: Daftar Lengkap Perubahan SAK Terbaru dari DSAK IAI",
 "Update PSAK 2026 terlengkap: pengesahan PSAK 120 (14 Oktober 2026), Amendemen PSAK 228, Amendemen ISAK 335, PSAK 338 revisi, Amendemen PSAK 109 dan 107, serta persiapan PSAK 118 dan PSAK 119 yang berlaku 1 Januari 2027.",
 "Update SAK",
 """<div class="keys"><div><b>14 Okt 2026</b><span>DSAK IAI mengesahkan PSAK 120 Aset Regulatori dan Liabilitas Regulatori (berbasis IFRS 20).</span></div><div><b>1 Jul 2026</b><span>Amendemen PSAK 228: opsi nilai wajar untuk investasi pada entitas asosiasi dan ventura bersama.</span></div><div><b>3 Jun 2026</b><span>Amendemen ISAK 335: penyajian entitas nonlaba diselaraskan dengan PSAK 118.</span></div><div><b>1 Jan 2027</b><span>PSAK 118 menggantikan PSAK 201, PSAK 119 berlaku untuk entitas anak tanpa akuntabilitas publik.</span></div></div>
<p><b>Jawaban singkat:</b> sepanjang 2026, Dewan Standar Akuntansi Keuangan (DSAK) IAI mengesahkan tiga produk utama, yaitu <a href="/psak/120/">PSAK 120</a>, Amendemen <a href="/psak/228/">PSAK 228</a>, dan Amendemen ISAK 335. Untuk tahun buku 2026 sendiri, yang mulai berlaku efektif adalah <a href="/psak/338/">PSAK 338</a> revisi, Amendemen <a href="/psak/109/">PSAK 109</a> dan <a href="/psak/107/">PSAK 107</a>, serta Penyesuaian Tahunan SAK 2024. Perubahan terbesar, <a href="/psak/118/">PSAK 118</a>, berlaku 1 Januari 2027 tetapi wajib disiapkan di 2026 karena angka komparatifnya adalah tahun 2026.</p>
<h2>Kronologi Update PSAK 2026</h2>
<div class="scroll"><table class="tbl"><thead><tr><th>Tanggal</th><th>Keputusan DSAK IAI</th><th>Dampak</th></tr></thead><tbody>
<tr><td>3 Juni 2026</td><td>Pengesahan Amendemen ISAK 335 Penyajian Laporan Keuangan Entitas Berorientasi Nonlaba</td><td>Yayasan, perkumpulan, dan lembaga nonlaba menyesuaikan format laporan dengan PSAK 118</td></tr>
<tr><td>1 Juli 2026</td><td>Pengesahan Amendemen PSAK 228 Investasi pada Entitas Asosiasi dan Ventura Bersama</td><td>Opsi pengukuran nilai wajar untuk investasi tertentu</td></tr>
<tr><td>26 Agustus 2026</td><td>Pengesahan Draf Eksposur PSAK 120</td><td>Dengar pendapat publik, merujuk IFRS 20</td></tr>
<tr><td>14 Oktober 2026</td><td>Pengesahan PSAK 120 Aset Regulatori dan Liabilitas Regulatori</td><td>Utilitas listrik, air, gas, jalan tol, dan usaha dengan tarif diatur regulator</td></tr>
</tbody></table></div>
<h2>Standar Yang Berlaku Efektif 1 Januari 2026</h2>
<div class="scroll"><table class="tbl"><thead><tr><th>Standar</th><th>Pokok Perubahan</th><th>Siapa Yang Terdampak</th></tr></thead><tbody>
<tr><td><a href="/psak/338/">PSAK 338</a> (revisi)</td><td>Kombinasi bisnis entitas sepengendali, penerapan dini diizinkan</td><td>Grup usaha yang melakukan restrukturisasi atau merger internal</td></tr>
<tr><td>Amendemen <a href="/psak/109/">PSAK 109</a> dan <a href="/psak/107/">PSAK 107</a></td><td>Klasifikasi aset keuangan (fitur ESG dan nonrecourse), penghentian pengakuan liabilitas via transfer elektronik, kontrak listrik energi terbarukan (PPA)</td><td>Perusahaan dengan pinjaman terkait ESG, pembeli listrik energi terbarukan</td></tr>
<tr><td>Penyesuaian Tahunan SAK 2024</td><td>Klarifikasi kecil pada beberapa PSAK</td><td>Semua pengguna SAK Indonesia</td></tr>
</tbody></table></div>
<h2>Kenapa PSAK 118 Harus Dikerjakan Tahun 2026</h2>
<p>PSAK 118 berlaku untuk periode yang dimulai 1 Januari 2027 secara retrospektif. Laporan keuangan 2027 wajib menyajikan angka 2026 dalam format baru, sehingga data 2026 harus sudah bisa dipetakan ke lima kategori laba rugi: operasi, investasi, pendanaan, pajak penghasilan, dan operasi yang dihentikan. Ada dua subtotal wajib, yaitu laba operasi serta laba sebelum pendanaan dan pajak. Ukuran kinerja yang ditetapkan manajemen (MPM) juga wajib diungkapkan dan direkonsiliasi di CALK. Baca rinciannya di <a href="/artikel/contoh-laba-rugi-psak-118/">Contoh Laba Rugi PSAK 118</a>.</p>
<h2>Linimasa 2026 Sampai 2029</h2>
<ul><li><b>2026</b>: PSAK 338 revisi, Amendemen PSAK 109/107, Penyesuaian Tahunan 2024 berlaku. Siapkan pemetaan akun untuk PSAK 118.</li><li><b>1 Januari 2027</b>: PSAK 118, <a href="/psak/119/">PSAK 119</a>, Amendemen ISAK 335 berlaku. Amendemen PSAK 228 berlaku bersama PSAK 118.</li><li><b>1 Januari 2029</b>: PSAK 120 berlaku, penerapan dini dibatasi sesuai ketentuan transisinya.</li></ul>
<h2>Checklist CFO dan Auditor Untuk Tutup Buku 2026</h2>
<ol><li>Ungkapkan di CALK daftar standar yang telah disahkan tetapi belum berlaku (PSAK 118, PSAK 119, PSAK 120, Amendemen PSAK 228) beserta estimasi dampaknya.</li><li>Petakan bagan akun ke kategori PSAK 118 dan uji ulang angka 2026 dalam format baru.</li><li>Tinjau kontrak pinjaman berpersyaratan ESG dan kontrak PPA energi terbarukan terhadap Amendemen PSAK 109.</li><li>Untuk grup usaha, tinjau transaksi restrukturisasi internal terhadap PSAK 338 revisi.</li><li>Entitas privat: pastikan sudah memakai <a href="/artikel/sak-ep-pengganti-sak-etap/">SAK EP</a>, bukan SAK ETAP.</li><li>Perbarui kebijakan akuntansi material di Catatan 2. Draf cepat bisa disusun di <a href="/#kalkulator">Kalkulator CALK</a>.</li></ol>
<h2>Sumber Resmi</h2>
<p>Seluruh tanggal di halaman ini diambil dari kanal SAK Update dan SAK Online Ikatan Akuntan Indonesia, dan dipantau setiap minggu. Teks lengkap standar tetap merujuk SAK Online IAI.</p>""",
 [("Apa saja update PSAK 2026?", "Sepanjang 2026, DSAK IAI mengesahkan Amendemen ISAK 335 (3 Juni 2026), Amendemen PSAK 228 (1 Juli 2026), Draf Eksposur PSAK 120 (26 Agustus 2026), dan PSAK 120 Aset Regulatori dan Liabilitas Regulatori (14 Oktober 2026). Yang berlaku efektif 1 Januari 2026 adalah PSAK 338 revisi, Amendemen PSAK 109 dan PSAK 107, serta Penyesuaian Tahunan SAK 2024."),
  ("Kapan PSAK 118 berlaku?", "PSAK 118 Penyajian dan Pengungkapan dalam Laporan Keuangan berlaku untuk periode yang dimulai 1 Januari 2027 dan menggantikan PSAK 201. Penerapannya retrospektif, sehingga angka 2026 harus disajikan ulang sebagai komparatif."),
  ("Kapan PSAK 120 berlaku?", "PSAK 120 disahkan DSAK IAI pada 14 Oktober 2026 dan berlaku 1 Januari 2029, untuk entitas dengan aktivitas bertarif yang diatur regulator."),
  ("Apakah UMKM terdampak update PSAK 2026?", "Entitas yang memakai SAK EMKM atau SAK EP tidak langsung terdampak PSAK 118 dan PSAK 120. Perubahan ini berlaku untuk entitas yang memakai SAK Indonesia, termasuk perusahaan yang bersiap IPO."),
  ("Berapa nomor PSAK baru untuk PSAK 1?", "PSAK 1 Penyajian Laporan Keuangan kini bernomor PSAK 201, dan mulai 2027 digantikan PSAK 118.")],
 [118, 119, 120, 228, 338, 109, 107, 201])

A.insert(0, A.pop())
A[0]["root"] = True
