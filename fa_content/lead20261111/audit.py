from _a import A

CAT = 'Audit & KAP'
CTA = ('/jasa-audit-laporan-keuangan/', 'Jasa Audit Laporan Keuangan')
IAPI = ('https://iapi.or.id/', 'Institut Akuntan Publik Indonesia, Standar Audit')
PPPK = ('https://pppk.kemenkeu.go.id/', 'Pusat Pembinaan Profesi Keuangan, Kemenkeu')
PENUTUP = ('<h2>Kontak Audit lewat FA Indonesia</h2><p>Audit dilaksanakan secara independen oleh KAP DHN &amp; Rekan (terdaftar OJK). '
           'Bila laporan keuangan perlu dirapikan lebih dulu, penyusunannya oleh KJA Farhani K.N. FA Indonesia menjadi pintu kontak: '
           'pertanyaan lewat WhatsApp dijawab langsung, lalu kebutuhan Anda diteruskan ke kantor pelaksana yang sesuai.</p>')

A('laporan-keuangan-audited-untuk-tender-migas-bumn',
  'LK Audited untuk Tender Migas dan BUMN: Kapan Wajib',
  'Laporan Keuangan Audited untuk Tender Migas dan BUMN: Kapan Wajib, Kapan Cukup Disusun KJA',
  'Mau ikut tender migas atau BUMN dan diminta laporan keuangan? Pahami kapan harus audited KAP, kapan cukup disusun KJA, dan kenapa LK nol jarang lolos.',
  'laporan keuangan audit untuk tender', CAT, 7, CTA,
  'Halo Pak Ananta, perusahaan kami mau ikut tender dan diminta laporan keuangan. Saya ingin tanya perlu audit KAP atau tidak.',
  [IAPI, ('https://www.lkpp.go.id/', 'LKPP, Pengadaan Barang/Jasa Pemerintah')],
  ['kja-vs-kap', 'kapan-perusahaan-wajib-diaudit', 'kompilasi-review-audit', 'apakah-perusahaan-butuh-audit-kap'],
  '''
<p>Perusahaan yang ingin masuk daftar rekanan migas, BUMN, atau tender besar hampir selalu diminta laporan keuangan. Pertanyaan yang paling sering muncul: apakah harus diaudit KAP, atau cukup laporan keuangan yang disusun kantor jasa akuntansi? Jawabannya ada di dokumen tender itu sendiri, tetapi ada beberapa pola yang perlu dipahami sebelum mengeluarkan biaya.</p>
<h2>Baca Dulu Persyaratan Tendernya</h2>
<ul>
<li><b>Tertulis "diaudit akuntan publik" atau "audited".</b> Berarti laporan harus disertai laporan auditor independen dari KAP.</li>
<li><b>Tertulis "laporan keuangan" saja.</b> Sering cukup laporan yang disusun dan ditandatangani direksi, atau disusun KJA.</li>
<li><b>Ada penilaian kemampuan keuangan.</b> Misalnya skor kesehatan keuangan, kemampuan dasar, atau rasio tertentu. Di sini isi laporan lebih menentukan daripada status audited.</li>
</ul>
<p>Bila ragu, tanyakan langsung ke panitia atau bagian pengadaan. Jawaban tertulis lebih aman daripada menebak.</p>
<h2>Kenapa Laporan Keuangan Nol Jarang Lolos</h2>
<p>Perusahaan yang baru aktif kembali sering memiliki laporan keuangan dengan pendapatan nol, aset hanya saldo rekening kecil, dan modal yang belum disetor penuh. Laporan seperti ini bisa saja diaudit, tetapi hasilnya tetap menunjukkan angka nol. Penilaian kemampuan keuangan menghitung dari angka, bukan dari status audited.</p>
<div class="pf-fold"><p>Artinya, biaya audit tetap keluar, tetapi peluang lolos prakualifikasi tidak bertambah. Dalam kondisi ini, langkah yang lebih masuk akal biasanya:</p>
<ol>
<li>Pastikan modal disetor sesuai akta dan tercatat di rekening perusahaan.</li>
<li>Bangun riwayat transaksi lewat pekerjaan yang lebih kecil atau subkontrak.</li>
<li>Susun laporan keuangan yang rapi sejak awal, lalu audit saat angka sudah bermakna.</li>
<li>Pertimbangkan kerja sama operasi dengan perusahaan yang sudah punya rekam jejak.</li>
</ol></div>
<h2>Perbandingan Singkat</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Jenis Laporan</th><th>Disusun/Diperiksa Oleh</th><th>Kapan Cocok</th></tr></thead><tbody>
<tr><td>Laporan keuangan intern</td><td>Manajemen perusahaan</td><td>Tender yang tidak mensyaratkan pihak luar</td></tr>
<tr><td>Laporan keuangan disusun KJA</td><td>Kantor Jasa Akuntansi berizin</td><td>Butuh laporan rapi sesuai SAK tanpa opini auditor</td></tr>
<tr><td>Laporan keuangan audited</td><td>Kantor Akuntan Publik</td><td>Tender yang tegas mensyaratkan audit</td></tr>
</tbody></table></div>
<h2>Bila Memang Harus Audited</h2>
<p>Siapkan waktu. Audit pertama biasanya membutuhkan pengujian saldo awal, dan laporan keuangan perlu sudah rapi sebelum auditor mulai bekerja. Mengajukan audit mendekati batas waktu tender adalah penyebab paling umum tender terlewat.</p>
''' + PENUTUP,
  [('Apakah semua tender BUMN wajib laporan keuangan audited?', 'Tidak semua. Persyaratannya tertulis di dokumen pengadaan masing-masing. Tanyakan ke panitia bila tidak jelas.'),
   ('Apakah laporan yang disusun KJA sama dengan audited?', 'Tidak. KJA menyusun laporan keuangan, sedangkan audit dilakukan KAP dan menghasilkan opini auditor independen.'),
   ('Perusahaan baru aktif lagi, sebaiknya audit sekarang?', 'Bila angka laporan masih nol, audit jarang menambah peluang lolos. Lebih baik bangun transaksi dan rapikan laporan dulu.')])

A('audit-laporan-keuangan-pt-pma-persiapan',
  'Audit Laporan Keuangan PT PMA: Kewajiban dan Persiapannya',
  'Audit Laporan Keuangan PT PMA: Kewajiban, Peruntukan, dan Persiapannya',
  'PT PMA sering diminta laporan keuangan audited untuk BKPM, bank, atau induk usaha. Pahami peruntukannya, jadwalnya, dan dokumen yang perlu disiapkan.',
  'audit laporan keuangan pt pma', CAT, 6, CTA,
  'Halo Pak Ananta, perusahaan kami PT PMA dan perlu audit laporan keuangan. Saya ingin tanya prosesnya.',
  [IAPI, ('https://www.bkpm.go.id/', 'Kementerian Investasi/BKPM')],
  ['kapan-perusahaan-wajib-diaudit', 'biaya-audit-kap-faktor-penentu', 'persiapan-audit-pertama-kali-saldo-awal', 'laporan-audit-lama-keluar'],
  '''
<p>Perusahaan penanaman modal asing (PT PMA) sering berurusan dengan laporan keuangan audited lebih awal dibanding perusahaan lokal sejenis. Permintaannya bisa datang dari induk usaha di luar negeri, bank, mitra usaha, atau kebutuhan pelaporan lain. Sebelum meminta penawaran audit, ada satu hal yang perlu jelas: untuk apa laporan audit itu dipakai.</p>
<h2>Peruntukan Menentukan Lingkup</h2>
<ul>
<li><b>Kebutuhan induk usaha.</b> Kadang diminta mengikuti kebijakan akuntansi grup atau paket pelaporan khusus.</li>
<li><b>Pengajuan kredit bank.</b> Bank melihat opini dan kualitas pengungkapan.</li>
<li><b>Kewajiban berdasarkan ukuran atau bentuk usaha.</b> Mengikuti peraturan yang berlaku untuk perseroan.</li>
<li><b>Perpajakan dan transfer pricing.</b> Laporan audit sering menjadi lampiran dokumen pendukung.</li>
</ul>
<p>Peruntukan dan batas waktu penyelesaian adalah dua hal yang paling memengaruhi lingkup dan jadwal audit.</p>
<h2>Hal Khas pada PT PMA</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Area</th><th>Yang Sering Diperiksa</th></tr></thead><tbody>
<tr><td>Mata uang</td><td>Mata uang fungsional, selisih kurs, pembukuan dalam mata uang asing</td></tr>
<tr><td>Transaksi pihak berelasi</td><td>Pinjaman dari induk, jasa manajemen, royalti, pembelian bahan dari grup</td></tr>
<tr><td>Modal</td><td>Kesesuaian setoran modal dengan akta dan bukti transfer</td></tr>
<tr><td>Pajak</td><td>PPh pasal 26, pajak tangguhan, dokumentasi harga transfer</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Pinjaman dari pemegang saham asing perlu didukung perjanjian, jadwal pembayaran, dan perhitungan bunga bila ada. Transaksi tanpa dokumen akan menjadi pertanyaan auditor dan bisa memperpanjang waktu audit.</p></div>
<h2>Dokumen yang Disiapkan</h2>
<ol>
<li>Laporan keuangan dan buku besar tahun yang diaudit.</li>
<li>Rekening koran seluruh rekening, rupiah maupun valuta asing.</li>
<li>Akta, perubahan modal, dan bukti setoran.</li>
<li>Perjanjian dengan pihak berelasi.</li>
<li>SPT tahunan dan bukti potong.</li>
<li>Laporan audit tahun sebelumnya, bila ada.</li>
</ol>
<h2>Audit Pertama Kali</h2>
<p>Bila tahun sebelumnya belum pernah diaudit, auditor perlu meyakini saldo awal. Ini menambah waktu. Laporan keuangan yang sudah dirapikan sebelum audit dimulai membuat proses lebih singkat.</p>
''' + PENUTUP,
  [('Apakah semua PT PMA wajib diaudit?', 'Kewajiban audit mengikuti peraturan yang berlaku dan kebutuhan pihak yang meminta. Banyak PT PMA tetap diaudit karena diminta induk usaha atau bank.'),
   ('Apakah laporan audit bisa dalam bahasa Inggris?', 'Bisa disepakati dalam perikatan, misalnya dwibahasa, sesuai kebutuhan induk usaha.'),
   ('Berapa lama audit PT PMA?', 'Tergantung ukuran, kesiapan data, dan peruntukan. Kesiapan dokumen adalah faktor yang paling bisa dikendalikan perusahaan.')])

A('audit-laporan-keuangan-perusahaan-tambang-kontraktor-kalimantan',
  'Audit LK Perusahaan Tambang dan Kontraktor di Kalimantan',
  'Audit Laporan Keuangan Perusahaan Tambang dan Kontraktor di Kalimantan',
  'Perusahaan tambang, hauling, dan kontraktor di Kalimantan butuh audit untuk bank dan mitra. Ini area yang biasa diuji auditor dan cara menyiapkannya.',
  'audit laporan keuangan perusahaan tambang', CAT, 7, CTA,
  'Halo Pak Ananta, perusahaan kami di Kalimantan bergerak di tambang/kontraktor dan perlu audit laporan keuangan.',
  [IAPI, ('https://www.esdm.go.id/', 'Kementerian ESDM')],
  ['laporan-keuangan-kontraktor-psak-115', 'persiapan-audit-pertama-kali-saldo-awal', 'cara-memilih-kap-untuk-kredit-bank', 'kredit-modal-kerja-kontraktor-berbasis-spk'],
  '''
<p>Di Kalimantan Selatan, Kalimantan Timur, dan Kalimantan Tengah, banyak perusahaan tumbuh dari usaha keluarga menjadi kontraktor tambang, jasa hauling, atau pemasok alat berat. Ketika kontrak makin besar, pemilik tambang, bank, dan perusahaan leasing mulai meminta laporan keuangan audited. Audit untuk usaha jenis ini punya area khusus yang sebaiknya disiapkan sejak awal.</p>
<h2>Area yang Biasa Diuji Auditor</h2>
<ul>
<li><b>Pendapatan kontrak.</b> Dicocokkan dengan kontrak, berita acara volume (misalnya per ton atau per BCM), dan invoice.</li>
<li><b>Alat berat.</b> Kepemilikan, pembiayaan leasing, penyusutan, dan keberadaan fisik unit.</li>
<li><b>Biaya bahan bakar dan suku cadang.</b> Biasanya biaya terbesar dan rawan selisih.</li>
<li><b>Utang leasing dan bank.</b> Dicocokkan dengan jadwal angsuran dan konfirmasi kreditur.</li>
<li><b>Uang muka dan retensi.</b> Termasuk potongan yang ditahan pemberi kerja.</li>
</ul>
<h2>Tantangan yang Sering Muncul</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Kondisi</th><th>Dampak ke Audit</th><th>Persiapan</th></tr></thead><tbody>
<tr><td>Unit alat berat atas nama pribadi pemilik</td><td>Aset tidak bisa diakui milik perusahaan</td><td>Perjanjian sewa atau pengalihan yang jelas</td></tr>
<tr><td>Pembayaran operasional tunai di site</td><td>Bukti pengeluaran lemah</td><td>Rekap kas site per minggu dengan bukti</td></tr>
<tr><td>Berita acara volume belum lengkap</td><td>Pendapatan sulit diuji</td><td>Arsipkan BA per periode tagihan</td></tr>
<tr><td>Belum pernah diaudit</td><td>Saldo awal perlu diyakini</td><td>Rapikan neraca awal tahun lebih dulu</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Inspeksi fisik alat berat di lokasi kerja kadang diperlukan. Jadwal kunjungan ke site sebaiknya diatur sejak awal perikatan supaya tidak menunda penyelesaian. Bila unit tersebar di beberapa lokasi, daftar unit dengan nomor rangka, lokasi, dan foto terbaru sangat membantu.</p></div>
<h2>Jarak Bukan Hambatan</h2>
<p>Sebagian besar pekerjaan audit kini bisa dilakukan dengan pertukaran dokumen digital dan pertemuan online. Kunjungan dilakukan untuk pekerjaan yang memang membutuhkan kehadiran, seperti inspeksi aset atau stock opname.</p>
<h2>Target Waktu yang Realistis</h2>
<p>Perusahaan sering membutuhkan laporan audit untuk perpanjangan kontrak atau pengajuan fasilitas dengan tenggat tertentu. Semakin rapi laporan keuangan sebelum audit dimulai, semakin realistis target waktunya.</p>
''' + PENUTUP,
  [('Apakah auditor harus datang ke site tambang?', 'Tergantung kebutuhan pengujian. Inspeksi fisik aset atau persediaan bisa memerlukan kunjungan, sisanya umumnya bisa online.'),
   ('Alat berat atas nama pribadi, bagaimana?', 'Perlu dokumen yang menjelaskan hubungan dengan perusahaan, misalnya perjanjian sewa. Tanpa itu, aset tidak diakui sebagai milik perusahaan.'),
   ('Apa yang paling memperlama audit kontraktor?', 'Dokumen pendapatan dan pengeluaran site yang tidak lengkap, serta saldo awal yang belum pernah diaudit.')])

A('audit-selesai-sebelum-akhir-tahun-target-realistis',
  'Audit Harus Selesai Akhir Tahun? Target yang Realistis',
  'Audit Harus Selesai Sebelum Akhir Tahun: Mana Target yang Realistis?',
  'Butuh laporan audit sebelum akhir tahun untuk bank atau tender? Ini faktor yang menentukan cepat lambatnya audit dan cara menyusun jadwal yang realistis.',
  'audit cepat selesai akhir tahun', CAT, 6, CTA,
  'Halo Pak Ananta, kami butuh laporan audit selesai sebelum akhir tahun. Saya ingin tanya jadwal yang memungkinkan.',
  [IAPI],
  ['laporan-audit-lama-keluar', 'persiapan-audit-pertama-kali-saldo-awal', 'biaya-audit-kap-faktor-penentu', 'jenis-opini-audit-dan-dampaknya-ke-bank'],
  '''
<p>Menjelang akhir tahun, permintaan audit dengan tenggat ketat meningkat. Ada yang butuh untuk perpanjangan kredit, ada yang untuk tender awal tahun, ada pula yang baru sadar laporan tahun lalu belum diaudit. Pertanyaannya selalu sama: bisa selesai kapan?</p>
<h2>Faktor yang Menentukan Waktu</h2>
<ol>
<li><b>Kesiapan laporan keuangan.</b> Laporan yang sudah final dengan rincian per akun bisa langsung diuji.</li>
<li><b>Audit pertama atau lanjutan.</b> Audit pertama memerlukan pengujian saldo awal.</li>
<li><b>Kecepatan konfirmasi.</b> Jawaban dari bank, pelanggan, dan pemasok tidak selalu cepat.</li>
<li><b>Jumlah koreksi.</b> Setiap koreksi besar harus disepakati dan diuji ulang.</li>
<li><b>Ketersediaan penanggung jawab di perusahaan.</b> Orang yang bisa menjawab pertanyaan auditor setiap hari.</li>
</ol>
<h2>Gambaran Jadwal</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Kondisi Perusahaan</th><th>Gambaran Proses</th></tr></thead><tbody>
<tr><td>LK final, pernah diaudit, dokumen siap</td><td>Pekerjaan lapangan bisa segera mulai, penyelesaian relatif cepat</td></tr>
<tr><td>LK final, audit pertama</td><td>Tambah waktu untuk saldo awal</td></tr>
<tr><td>LK belum rapi</td><td>Perlu tahap penyusunan atau perapian sebelum audit</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Gambaran di atas bukan janji. Waktu akhir selalu ditentukan oleh hasil pengujian auditor. Yang bisa dikendalikan perusahaan adalah kesiapan data dan kecepatan menjawab permintaan dokumen.</p></div>
<h2>Kenapa Tidak Bisa Sekadar Dipercepat</h2>
<p>Auditor independen harus memperoleh bukti yang cukup sebelum memberi opini. Mempercepat dengan mengurangi pengujian bukan pilihan, karena opini auditor dipakai pihak lain untuk mengambil keputusan. Yang bisa dipercepat adalah waktu menunggu.</p>
<h2>Langkah Bila Tenggat Sudah Dekat</h2>
<ul>
<li>Kirim laporan keuangan dan buku besar di hari pertama.</li>
<li>Siapkan daftar dokumen (PBC) per akun tanpa menunggu diminta.</li>
<li>Kirim permintaan konfirmasi bank dan pihak ketiga sejak awal.</li>
<li>Tanyakan ke pihak yang meminta laporan: apakah ada toleransi, misalnya surat keterangan proses audit.</li>
</ul>
<div class="pf-fold"><p>Beberapa bank dan panitia tender menerima surat keterangan bahwa audit sedang berjalan sambil menunggu laporan final. Ini perlu ditanyakan langsung ke pihak yang meminta, karena kebijakannya berbeda-beda.</p></div>
''' + PENUTUP,
  [('Bisakah audit selesai dalam beberapa minggu?', 'Bisa, bila laporan keuangan sudah final, dokumen lengkap, dan tidak banyak koreksi. Kepastiannya ditentukan hasil pengujian auditor.'),
   ('Apakah bayar lebih mahal membuat audit lebih cepat?', 'Biaya tidak mengurangi pengujian yang wajib dilakukan. Yang mempercepat adalah kesiapan data perusahaan.'),
   ('Apa itu surat keterangan proses audit?', 'Surat dari KAP bahwa audit sedang berjalan. Apakah diterima atau tidak tergantung kebijakan pihak yang meminta.')])

A('cara-membaca-surat-penawaran-audit-kap',
  'Cara Membaca Surat Penawaran Audit KAP',
  'Cara Membaca Surat Penawaran Audit KAP: Lingkup, Jadwal, dan Asumsi',
  'Surat penawaran audit KAP bukan sekadar angka. Pahami lingkup, periode, peruntukan, jadwal, asumsi data, dan apa yang tidak termasuk sebelum menyetujui.',
  'surat penawaran audit kap', CAT, 6, CTA,
  'Halo Pak Ananta, kami sedang membandingkan penawaran audit dan ingin diskusi lingkupnya.',
  [IAPI, PPPK],
  ['biaya-audit-kap-faktor-penentu', 'kap-murah-apakah-bijak', 'cara-memilih-kap-untuk-kredit-bank', 'apakah-perusahaan-butuh-audit-kap'],
  '''
<p>Saat membandingkan dua atau tiga penawaran audit, perhatian biasanya langsung tertuju ke angka. Padahal penawaran yang tampak lebih murah bisa memiliki lingkup berbeda, dan penawaran yang tampak mahal bisa sudah mencakup pekerjaan yang di tempat lain dihitung terpisah. Bacalah bagian-bagian berikut lebih dulu.</p>
<h2>Bagian yang Perlu Dibaca</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Bagian</th><th>Pertanyaan</th></tr></thead><tbody>
<tr><td>Entitas dan periode</td><td>PT mana, tahun buku berapa, satu tahun atau dua tahun?</td></tr>
<tr><td>Peruntukan</td><td>Untuk bank, tender, pemegang saham, atau kewajiban lain?</td></tr>
<tr><td>Saldo awal</td><td>Apakah pengujian saldo awal sudah termasuk?</td></tr>
<tr><td>Jadwal</td><td>Kapan pekerjaan lapangan dan kapan draf laporan?</td></tr>
<tr><td>Asumsi data</td><td>Laporan keuangan dari siapa, kapan diserahkan?</td></tr>
<tr><td>Yang tidak termasuk</td><td>Penyusunan LK, pajak, kunjungan luar kota, revisi tambahan?</td></tr>
</tbody></table></div>
<h2>Saldo Awal dan Audit Pertama</h2>
<p>Bila tahun sebelumnya belum diaudit, auditor perlu meyakini saldo awal. Ada penawaran yang memasukkannya, ada yang tidak. Dua penawaran dengan angka mirip bisa jadi berbeda jauh lingkupnya hanya karena poin ini.</p>
<h2>Asumsi Kesiapan Laporan Keuangan</h2>
<p>Hampir semua penawaran audit mengasumsikan laporan keuangan sudah disusun perusahaan. Bila ternyata laporan belum siap, jadwal mundur dan bisa muncul pekerjaan tambahan. Pastikan sejak awal siapa yang menyusun laporan keuangan.</p>
<div class="pf-fold"><p>Auditor independen tidak boleh menyusun laporan keuangan yang ia audit sendiri, karena akan mengganggu independensi. Karena itu penyusunan laporan keuangan, bila diperlukan, dilakukan pihak lain seperti tim keuangan internal atau kantor jasa akuntansi.</p></div>
<h2>Tanda Penawaran yang Perlu Ditanyakan Ulang</h2>
<ul>
<li>Menjanjikan opini tertentu, misalnya pasti WTP.</li>
<li>Jadwal sangat singkat tanpa melihat data lebih dulu.</li>
<li>Tidak menyebut peruntukan dan periode dengan jelas.</li>
<li>Angka jauh di bawah kewajaran tanpa penjelasan lingkup.</li>
</ul>
<div class="pf-fold"><p>Opini auditor adalah kesimpulan independen setelah pengujian. Tidak ada pihak yang bisa menjanjikannya di awal. Penawaran yang menjanjikan hasil justru patut dipertanyakan.</p></div>
<h2>Setelah Penawaran Disetujui</h2>
<p>Penawaran yang disetujui dituangkan dalam surat perikatan audit. Simpan dokumen ini, karena menjadi acuan bila ada perbedaan pemahaman tentang lingkup di tengah pekerjaan.</p>
''' + PENUTUP,
  [('Kenapa penawaran audit antar KAP berbeda?', 'Karena lingkup, asumsi kesiapan data, pengujian saldo awal, jadwal, dan peruntukan bisa berbeda.'),
   ('Apakah KAP boleh menjanjikan opini WTP?', 'Tidak. Opini adalah kesimpulan independen auditor setelah pengujian.'),
   ('Apa itu surat perikatan audit?', 'Dokumen kesepakatan antara perusahaan dan KAP yang memuat lingkup, tanggung jawab, jadwal, dan biaya audit.')])
