from _a import A

CAT = 'Laporan Keuangan'
CTA = ('/jasa-penyusunan-laporan-keuangan/', 'Jasa Penyusunan Laporan Keuangan')
IAI = ('https://iaiglobal.or.id/', 'Ikatan Akuntan Indonesia, Standar Akuntansi Keuangan')
DJP = ('https://www.pajak.go.id/', 'Direktorat Jenderal Pajak')
PENUTUP = ('<h2>Penyusunan Laporan Keuangan lewat FA Indonesia</h2><p>Penyusunan laporan keuangan dikerjakan oleh KJA Farhani K.N. (Kantor Jasa Akuntansi berizin). '
           'Bila laporan perlu diaudit, auditnya oleh KAP DHN &amp; Rekan (terdaftar OJK), sehingga penyusun dan auditor tetap pihak yang berbeda. '
           'FA Indonesia menjadi pintu kontak: tanyakan dulu lewat WhatsApp, kebutuhan Anda langsung diarahkan ke kantor pelaksananya.</p>')

A('menyusun-laporan-keuangan-dari-rekening-koran',
  'Menyusun Laporan Keuangan dari Rekening Koran',
  'Menyusun Laporan Keuangan dari Rekening Koran: Bisa, Asal Datanya Tepat',
  'Belum punya pembukuan, hanya rekening koran? Laporan keuangan tetap bisa disusun. Ini caranya, data tambahan yang dibutuhkan, dan batasannya.',
  'laporan keuangan dari rekening koran', CAT, 6, CTA,
  'Halo Pak Ananta, usaha kami belum punya pembukuan, hanya rekening koran. Bisa dibantu susun laporan keuangan?',
  [IAI],
  ['laporan-keuangan-berantakan-cara-merapikan', 'contoh-laporan-keuangan-umkm', 'pisahkan-uang-pribadi-dan-perusahaan', 'biaya-jasa-penyusunan-laporan-keuangan'],
  '''
<p>Banyak usaha baru sadar butuh laporan keuangan ketika bank, calon mitra, atau panitia tender memintanya. Pembukuan belum ada, tetapi semua transaksi lewat rekening bank. Kabar baiknya, rekening koran adalah titik awal yang baik. Laporan keuangan bisa disusun dari sana, dengan beberapa data tambahan.</p>
<h2>Apa yang Bisa Dibaca dari Rekening Koran</h2>
<ul>
<li>Uang masuk dari pelanggan, yang menjadi dasar pendapatan.</li>
<li>Pembayaran ke pemasok, gaji, sewa, pajak, dan cicilan.</li>
<li>Setoran modal dan pinjaman dari pemilik.</li>
<li>Saldo kas di bank pada akhir periode.</li>
</ul>
<h2>Data Tambahan yang Dibutuhkan</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Data</th><th>Kenapa Dibutuhkan</th></tr></thead><tbody>
<tr><td>Daftar semua rekening yang dipakai usaha</td><td>Supaya tidak ada transaksi yang tertinggal</td></tr>
<tr><td>Invoice yang belum dibayar pelanggan</td><td>Menjadi piutang</td></tr>
<tr><td>Tagihan pemasok yang belum dibayar</td><td>Menjadi utang</td></tr>
<tr><td>Daftar aset: kendaraan, mesin, peralatan</td><td>Dicatat sebagai aset tetap dan disusutkan</td></tr>
<tr><td>Stok barang di akhir periode</td><td>Menjadi persediaan dan menentukan harga pokok</td></tr>
<tr><td>Penjelasan transaksi besar</td><td>Membedakan pendapatan, pinjaman, atau setoran modal</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Uang masuk tidak selalu pendapatan. Transfer dari pemilik bisa berupa setoran modal atau pinjaman, dan transfer antar rekening sendiri bukan pendapatan. Tanpa penjelasan transaksi, laporan bisa menunjukkan pendapatan yang lebih besar dari sebenarnya, dan bank yang teliti akan menemukannya.</p></div>
<h2>Kenapa File Rekening Koran Harus Asli</h2>
<p>Bila laporan keuangan akan dipakai untuk bank, rekening koran sebaiknya diunduh langsung dari internet banking atau dicetak bank, tanpa melewati aplikasi edit PDF. Bank sering mencocokkan sendiri mutasi rekening dengan laporan keuangan. Perbedaan sekecil apa pun akan merusak kepercayaan pada seluruh laporan.</p>
<h2>Batasan yang Perlu Dipahami</h2>
<ul>
<li>Transaksi tunai yang tidak lewat bank perlu bukti terpisah.</li>
<li>Aset tanpa bukti kepemilikan atau perolehan tidak bisa dicatat sembarangan.</li>
<li>Periode yang bisa disusun mengikuti periode rekening koran yang tersedia.</li>
</ul>
<div class="pf-fold"><p>Mulai sekarang, biasakan semua penerimaan pelanggan masuk ke rekening perusahaan dan pisahkan rekening pribadi. Langkah sederhana ini membuat laporan keuangan bulan berikutnya jauh lebih mudah dan lebih dipercaya.</p></div>
''' + PENUTUP,
  [('Berapa lama menyusun laporan keuangan dari rekening koran?', 'Tergantung jumlah rekening, banyaknya transaksi, dan kelengkapan penjelasan. Data yang lengkap di awal membuat prosesnya cepat.'),
   ('Bisakah disusun untuk beberapa bulan saja?', 'Bisa, misalnya laporan triwulan atau periode berjalan, sesuai kebutuhan pihak yang meminta.'),
   ('Bagaimana dengan transaksi tunai?', 'Perlu rekap dan bukti terpisah, misalnya nota, kuitansi, atau buku kas.')])

A('keaslian-data-laporan-keuangan-untuk-bank',
  'Keaslian Data Laporan Keuangan untuk Kredit Bank',
  'Keaslian Data dalam Laporan Keuangan untuk Bank: Kenapa Tidak Bisa Ditawar',
  'Laporan keuangan untuk kredit bank harus dari data asli. Ini alasan bank sangat teliti, risiko data yang diubah, dan cara memperbaiki angka secara sah.',
  'keaslian data laporan keuangan bank', CAT, 6, CTA,
  'Halo Pak Ananta, kami butuh laporan keuangan untuk bank dan ingin memastikan datanya disusun dengan benar.',
  [('https://www.ojk.go.id/', 'Otoritas Jasa Keuangan'), IAI],
  ['laporan-keuangan-untuk-kredit-bank', 'alasan-kredit-bank-ditolak', 'laba-naik-kredit-ditolak-cara-bank-membaca-laba-utang-arus-kas', 'slik-ojk-perusahaan-pengurus-kolektibilitas'],
  '''
<p>Saat mengajukan kredit, wajar bila pemilik ingin laporan keuangannya terlihat sebaik mungkin. Masalah muncul ketika keinginan itu dilakukan dengan cara mengubah data: mutasi rekening disunting, aset dicatat tanpa bukti, atau penjualan ditambah. Penyusun laporan keuangan yang bertanggung jawab akan menolak, dan alasannya bukan sekadar aturan.</p>
<h2>Bank Punya Cara Sendiri untuk Mencocokkan</h2>
<ul>
<li>Mutasi rekening di bank yang sama bisa dilihat langsung dari sistem bank.</li>
<li>Analis meminta rekening koran dari bank lain dan memeriksa keasliannya.</li>
<li>Data SLIK menunjukkan seluruh pinjaman perusahaan dan pengurus.</li>
<li>Kunjungan lapangan melihat aset, stok, dan aktivitas usaha.</li>
<li>SPT pajak dibandingkan dengan pendapatan di laporan.</li>
</ul>
<p>Bila satu angka terbukti tidak benar, seluruh laporan kehilangan kepercayaan, termasuk angka yang sebenarnya benar.</p>
<h2>Risikonya Lebih dari Sekadar Ditolak</h2>
<div class="pf-fold"><p>Data yang dipalsukan untuk mendapatkan kredit bisa berujung pada masalah hukum, bukan hanya penolakan. Selain itu, catatan buruk di satu bank sering terbawa saat mengajukan ke bank lain. Kerugian jangka panjangnya jauh lebih besar daripada keuntungan sesaat.</p></div>
<h2>Cara Sah Memperbaiki Angka</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Masalah</th><th>Cara yang Sah</th></tr></thead><tbody>
<tr><td>Penjualan banyak yang tunai, tidak tercatat di bank</td><td>Arahkan penagihan ke rekening perusahaan mulai sekarang, rekap penjualan tunai dengan bukti</td></tr>
<tr><td>Aset dibeli atas nama pribadi</td><td>Dokumentasikan pengalihan atau sewa ke perusahaan</td></tr>
<tr><td>Laba kecil karena biaya pribadi masuk perusahaan</td><td>Pisahkan biaya pribadi, koreksi dengan bukti</td></tr>
<tr><td>Pembukuan berantakan</td><td>Susun ulang laporan dari dokumen asli</td></tr>
</tbody></table></div>
<p>Laporan keuangan yang disusun dari data asli, dengan penjelasan yang jujur, sering lebih kuat di mata bank daripada laporan yang tampak bagus tetapi rapuh.</p>
<h2>Kalau Datanya Memang Belum Cukup</h2>
<p>Kadang jawaban paling jujur adalah menunda pengajuan dua atau tiga bulan, sambil merapikan arus kas masuk ke rekening perusahaan. Riwayat transaksi yang terus membaik adalah bukti terkuat untuk analis kredit.</p>
''' + PENUTUP,
  [('Kenapa penyusun LK meminta file asli rekening koran?', 'Karena bank akan mencocokkan sendiri. File yang sudah melewati aplikasi edit tidak bisa dijadikan dasar laporan untuk bank.'),
   ('Bolehkah aset pribadi dimasukkan ke laporan perusahaan?', 'Hanya bila ada dasar yang sah, misalnya pengalihan atau penyetoran sebagai modal, dengan dokumen yang jelas.'),
   ('Laba kecil, apakah kredit pasti ditolak?', 'Tidak selalu. Bank juga melihat arus kas, agunan, dan prospek. Penjelasan yang jujur dan rencana perbaikan sering membantu.')])

A('laporan-keuangan-bank-dan-pajak-harus-sejalan',
  'Laporan Keuangan untuk Bank dan Pajak Harus Sejalan',
  'Laporan Keuangan untuk Bank dan untuk Pajak Harus Sejalan: Kenapa dan Caranya',
  'Laporan keuangan untuk bank berbeda dengan SPT? Ini risiko dua versi laporan, cara bank membandingkannya, dan cara menyelaraskan bersama konsultan pajak.',
  'laporan keuangan bank dan pajak berbeda', CAT, 6, CTA,
  'Halo Pak Ananta, laporan keuangan kami untuk bank dan untuk pajak berbeda. Saya ingin diskusi cara merapikannya.',
  [DJP, IAI],
  ['penyusutan-fiskal-vs-komersial-cara-hitung-pajak-tangguhan', 'laporan-keuangan-untuk-kredit-bank', 'coretax-untuk-badan-usaha-yang-perlu-disiapkan', 'memilih-konsultan-pajak-berizin'],
  '''
<p>Di banyak perusahaan keluarga, ada dua versi laporan keuangan: satu untuk lampiran SPT, satu lagi untuk bank. Versi pajak biasanya menunjukkan laba kecil, versi bank menunjukkan laba besar. Praktik ini dulu mungkin tidak terlalu terasa. Sekarang, ketika data pajak makin terhubung dan bank makin teliti, dua versi laporan menjadi masalah.</p>
<h2>Bank Membandingkan dengan SPT</h2>
<p>Analis kredit sering meminta SPT tahunan badan beserta lampiran laporan keuangannya. Bila pendapatan di laporan untuk bank jauh berbeda dengan SPT, bank akan bertanya: mana yang benar? Kedua jawaban sama-sama merugikan. Bila laporan bank yang benar, ada risiko pajak. Bila laporan pajak yang benar, laporan bank tidak bisa dipercaya.</p>
<h2>Beda yang Wajar dan yang Tidak</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Beda yang Wajar</th><th>Beda yang Bermasalah</th></tr></thead><tbody>
<tr><td>Penyusutan komersial vs fiskal</td><td>Pendapatan berbeda tanpa penjelasan</td></tr>
<tr><td>Biaya yang tidak boleh dikurangkan secara pajak (koreksi fiskal)</td><td>Aset muncul di satu versi saja</td></tr>
<tr><td>Pajak tangguhan</td><td>Utang bank tidak dicatat di salah satu versi</td></tr>
</tbody></table></div>
<p>Perbedaan yang wajar dijelaskan lewat rekonsiliasi fiskal. Laporan keuangan komersialnya tetap satu.</p>
<div class="pf-fold"><p>Prinsipnya sederhana: satu laporan keuangan komersial, lalu koreksi fiskal untuk menghitung pajak. Bank membaca laporan komersial, kantor pajak membaca hasil koreksi fiskal. Keduanya berasal dari angka yang sama.</p></div>
<h2>Cara Menyelaraskan</h2>
<ol>
<li>Kumpulkan kedua versi laporan dan SPT beberapa tahun terakhir.</li>
<li>Petakan perbedaan per akun dan cari penyebabnya.</li>
<li>Susun satu laporan keuangan dari data asli.</li>
<li>Diskusikan dampak pajaknya bersama konsultan pajak, termasuk pilihan pembetulan bila diperlukan.</li>
<li>Gunakan laporan yang sama untuk bank dan pajak ke depan.</li>
</ol>
<div class="pf-fold"><p>Langkah keempat penting. Penyusun laporan keuangan dan konsultan pajak sebaiknya duduk bersama, supaya laporan untuk bank dan posisi pajak perusahaan sejalan sejak awal. Keputusan pembetulan SPT tetap menjadi keputusan perusahaan dengan saran konsultan pajak berizin.</p></div>
<h2>Manfaat Jangka Panjang</h2>
<p>Laporan yang satu versi membuat pengajuan kredit lebih lancar, audit lebih mudah, dan perusahaan lebih siap bila suatu saat mengajak investor.</p>
''' + PENUTUP,
  [('Bolehkah laporan keuangan untuk bank berbeda dengan pajak?', 'Laporan keuangan komersialnya sebaiknya satu. Perbedaan dengan pajak dijelaskan lewat koreksi fiskal, bukan dua laporan.'),
   ('Apakah bank melihat SPT?', 'Banyak bank meminta SPT tahunan badan beserta lampirannya sebagai pembanding.'),
   ('Bagaimana bila sudah terlanjur dua versi?', 'Petakan perbedaannya, susun satu laporan dari data asli, lalu bahas dampak pajaknya bersama konsultan pajak.')])

A('laporan-keuangan-usaha-pariwisata-bali',
  'Laporan Keuangan Usaha Pariwisata di Bali dan NTB',
  'Laporan Keuangan Usaha Pariwisata di Bali, Labuan Bajo, dan Lombok',
  'Biro perjalanan, villa, dan operator wisata di Bali punya pola keuangan musiman. Ini cara menyusun laporan keuangan yang siap bank dan pemegang saham.',
  'laporan keuangan usaha pariwisata bali', CAT, 6, CTA,
  'Halo Pak Ananta, usaha kami di bidang pariwisata di Bali dan butuh laporan keuangan.',
  [IAI, DJP],
  ['laporan-keuangan-untuk-kredit-bank', 'sak-emkm-vs-sak-ep', 'laporan-keuangan-berantakan-cara-merapikan', 'ppn-12-persen-dpp-11-12-cara-hitung-invoice-pph-23'],
  '''
<p>Usaha pariwisata di Badung, Denpasar, Gianyar, Labuan Bajo, dan Lombok tumbuh cepat, dan banyak dimiliki bersama oleh beberapa pemegang saham, termasuk pemegang saham asing. Ketika usaha membesar, laporan keuangan yang rapi dibutuhkan untuk bank, pertanggungjawaban ke pemegang saham, kontrak lahan, dan pajak.</p>
<h2>Ciri Keuangan Usaha Pariwisata</h2>
<ul>
<li><b>Musiman.</b> Pendapatan tinggi di musim liburan, rendah di luar musim. Bank perlu melihat pola setahun penuh.</li>
<li><b>Uang muka pelanggan.</b> Pembayaran paket tur atau booking villa diterima sebelum layanan diberikan. Ini utang (pendapatan diterima di muka), bukan pendapatan.</li>
<li><b>Mata uang asing.</b> Tamu membayar dalam dolar atau lewat agen luar negeri.</li>
<li><b>Komisi agen dan OTA.</b> Pendapatan perlu dicatat bruto atau neto sesuai perannya.</li>
<li><b>Sewa lahan jangka panjang.</b> Banyak villa dan atraksi wisata berdiri di atas lahan sewa.</li>
</ul>
<h2>Pos yang Perlu Perhatian</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Pos</th><th>Perlakuan Umum</th></tr></thead><tbody>
<tr><td>Uang muka tamu</td><td>Diakui pendapatan saat layanan diberikan</td></tr>
<tr><td>Sewa lahan dibayar di muka</td><td>Dicatat sebagai sewa dibayar di muka atau aset hak guna, sesuai standar yang dipakai</td></tr>
<tr><td>Bangunan di atas lahan sewa</td><td>Disusutkan sesuai masa manfaat atau masa sewa</td></tr>
<tr><td>Transaksi valuta asing</td><td>Dicatat dengan kurs transaksi, saldo akhir dengan kurs penutupan</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Standar akuntansi yang dipakai menentukan perlakuan beberapa pos, misalnya sewa. Usaha kecil dan menengah tanpa akuntabilitas publik umumnya memakai SAK EP atau SAK EMKM. Bila pemegang saham asing atau bank meminta standar tertentu, sampaikan sejak awal supaya laporan tidak perlu disusun ulang.</p></div>
<h2>Proyek Baru: Pisahkan Sejak Awal</h2>
<p>Usaha yang membuka proyek baru, misalnya atraksi wisata di lokasi lain, sebaiknya memisahkan biaya proyek sejak hari pertama. Biaya pembangunan dicatat sebagai aset dalam penyelesaian, bukan biaya operasional. Pemegang saham dan otoritas pemberi izin lahan biasanya ingin melihat pertanggungjawaban proyek secara terpisah.</p>
<div class="pf-fold"><p>Untuk proyek yang membutuhkan keputusan investasi, laporan keuangan historis sebaiknya dilengkapi studi kelayakan atau proyeksi arus kas. Bila dibutuhkan nilai pasar tanah atau bangunan, penilaian dilakukan oleh penilai berizin (KJPP).</p></div>
<h2>Kerja Jarak Jauh</h2>
<p>Penyusunan laporan keuangan bisa dilakukan sepenuhnya online: rekening koran, invoice, dan dokumen dikirim lewat folder bersama, diskusi lewat video call.</p>
''' + PENUTUP,
  [('Uang muka dari tamu dicatat sebagai apa?', 'Sebagai pendapatan diterima di muka (liabilitas) sampai layanan diberikan, lalu diakui sebagai pendapatan.'),
   ('Bisakah penyusunan laporan dilakukan dari luar Bali?', 'Bisa. Data dan diskusi dilakukan online, kunjungan hanya bila memang diperlukan.'),
   ('Standar akuntansi apa yang dipakai?', 'Umumnya SAK EP atau SAK EMKM untuk usaha tanpa akuntabilitas publik, kecuali bank atau pemegang saham meminta standar lain.')])

A('pertanyaan-sebelum-menyusun-laporan-keuangan-pt',
  '5 Hal Ditanyakan Sebelum Menyusun Laporan Keuangan PT',
  '5 Hal yang Ditanyakan Sebelum Menyusun Laporan Keuangan PT',
  'Sebelum memberi penawaran penyusunan laporan keuangan, penyusun akan menanyakan 5 hal ini. Siapkan jawabannya supaya lingkup dan jadwalnya tepat.',
  'menyusun laporan keuangan pt', CAT, 5, CTA,
  'Halo Pak Ananta, saya ingin konsultasi penyusunan laporan keuangan PT kami.',
  [IAI],
  ['biaya-jasa-penyusunan-laporan-keuangan', 'sak-emkm-vs-sak-ep', 'laporan-tahunan-pt-permenkum-49-2025', 'outsourcing-accounting-vs-rekrut-staf-biaya'],
  '''
<p>Pemilik usaha yang menghubungi penyusun laporan keuangan sering langsung bertanya biayanya. Jawaban yang jujur selalu dimulai dengan beberapa pertanyaan, karena laporan untuk lampiran SPT dan laporan untuk pengajuan kredit miliaran rupiah adalah pekerjaan yang berbeda. Lima pertanyaan berikut hampir selalu muncul.</p>
<h2>1. Nama Usaha, Bentuk, dan Bidangnya</h2>
<p>PT, CV, atau perorangan menentukan struktur laporan, terutama bagian ekuitas. Bidang usaha menentukan pos khusus: kontraktor punya pendapatan kontrak, dagang punya persediaan, jasa punya piutang dan uang muka.</p>
<h2>2. Untuk Keperluan Apa</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Keperluan</th><th>Yang Biasanya Ditekankan</th></tr></thead><tbody>
<tr><td>Lampiran SPT</td><td>Kesesuaian dengan data pajak</td></tr>
<tr><td>Kredit bank</td><td>Arus kas, utang, kesesuaian dengan rekening koran</td></tr>
<tr><td>Tender</td><td>Format sesuai dokumen pengadaan</td></tr>
<tr><td>Investor</td><td>Konsistensi beberapa tahun, catatan atas laporan keuangan</td></tr>
<tr><td>Laporan tahunan PT</td><td>Kelengkapan sesuai ketentuan pelaporan</td></tr>
</tbody></table></div>
<h2>3. Periode yang Dibutuhkan</h2>
<p>Satu tahun buku, dua tahun untuk perbandingan, atau periode berjalan sampai bulan terakhir. Bank sering meminta dua tahun terakhir plus tahun berjalan.</p>
<h2>4. Kondisi Pembukuan Saat Ini</h2>
<ul>
<li>Sudah ada di software akuntansi.</li>
<li>Ada di Excel.</li>
<li>Baru ada rekening koran dan nota.</li>
</ul>
<div class="pf-fold"><p>Semakin awal kondisinya, semakin banyak pekerjaan mencatat ulang. Tidak masalah, yang penting jujur sejak awal supaya jadwal realistis. Pembukuan yang sudah di software tetap perlu ditelaah, karena kesalahan klasifikasi sering terjadi.</p></div>
<h2>5. Gambaran Omzet dan Target Selesai</h2>
<p>Omzet memberi gambaran jumlah transaksi. Target selesai menentukan apakah pekerjaan perlu dijadwalkan lebih cepat. Bila ada tenggat dari bank atau tender, sampaikan tanggalnya.</p>
<h2>Setelah Pertanyaan Dijawab</h2>
<p>Dengan lima jawaban ini, penyusun bisa memberi lingkup, daftar data, jadwal, dan penawaran yang tepat. Surat perikatan ditandatangani, data dikirim, dan pekerjaan dimulai.</p>
<div class="pf-fold"><p>Simpan jawaban ini untuk tahun berikutnya. Usaha yang konsisten memakai penyusun dan standar yang sama akan memiliki laporan yang dapat dibandingkan dari tahun ke tahun, sesuatu yang sangat dihargai bank dan investor.</p></div>
''' + PENUTUP,
  [('Berapa biaya penyusunan laporan keuangan PT?', 'Tergantung keperluan, periode, kondisi pembukuan, dan jumlah transaksi. Lima pertanyaan di atas menentukan lingkupnya.'),
   ('Apakah bisa untuk CV atau perorangan?', 'Bisa. Strukturnya menyesuaikan bentuk usaha.'),
   ('Apa yang perlu dikirim di awal?', 'Rekening koran, data pembukuan yang ada, akta, dan NPWP. Daftar lengkapnya diberikan setelah lingkup disepakati.')])
