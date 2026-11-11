from _a import A

CAT = 'Akuntansi Forensik'
CTA = ('/akuntan-forensik/', 'Akuntan Forensik')
IAPI = ('https://iapi.or.id/', 'Institut Akuntan Publik Indonesia')
JDIH = ('https://peraturan.go.id/', 'Database Peraturan Perundang-undangan')
PENUTUP = ('<h2>Konsultasi Penghitungan Kerugian</h2><p>Laporan penghitungan kerugian di FA Indonesia ditandatangani akuntan publik yang bersertifikat forensik. '
           'Diskusi awal bisa langsung dengan Ananta W. Sasongko, CPA, dan bila sudah ada kuasa hukum, sebaiknya dilibatkan sejak awal supaya kebutuhan pembuktian sama. '
           'Informasi perkara dijaga kerahasiaannya.</p>')

A('laporan-penghitungan-kerugian-proyek-akuntan-publik',
  'Laporan Penghitungan Kerugian Proyek oleh Akuntan Publik',
  'Laporan Penghitungan Kerugian Proyek oleh Akuntan Publik: Isi dan Prosesnya',
  'Proyek merugi karena wanprestasi atau penggelapan? Ini isi laporan penghitungan kerugian oleh akuntan publik, prosesnya, dan dokumen yang dibutuhkan.',
  'laporan penghitungan kerugian proyek', CAT, 7, CTA,
  'Halo Pak Ananta, kami mengalami kerugian proyek dan butuh laporan penghitungan kerugian.',
  [IAPI, JDIH],
  ['metode-menghitung-kerugian-keuangan', 'dokumen-menghitung-kerugian-penggelapan', 'ahli-akuntansi-di-penyidikan-dan-persidangan', 'kerja-sama-kuasa-hukum-pembuktian-kerugian'],
  '''
<p>Ketika proyek tidak berjalan sesuai kontrak, dana tidak dipakai sebagaimana mestinya, atau ada dugaan penggelapan, pertanyaan pertama yang diajukan penyidik, kuasa hukum, atau pihak lawan adalah: berapa kerugiannya, dan bagaimana menghitungnya? Angka yang disampaikan tanpa metode yang jelas mudah dibantah. Karena itu banyak pihak menggunakan laporan penghitungan kerugian dari akuntan publik.</p>
<h2>Isi Laporan Penghitungan Kerugian</h2>
<ol>
<li><b>Latar belakang dan tujuan.</b> Perkara apa, untuk kepentingan apa laporan disusun.</li>
<li><b>Dokumen yang diperiksa.</b> Daftar lengkap bukti yang menjadi dasar.</li>
<li><b>Metode.</b> Cara menghitung kerugian dan alasan memilih metode tersebut.</li>
<li><b>Perhitungan.</b> Rincian angka yang bisa ditelusuri ke dokumen.</li>
<li><b>Kesimpulan dan batasan.</b> Nilai kerugian dan hal yang tidak dicakup.</li>
</ol>
<h2>Tahapan Pekerjaan</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Tahap</th><th>Kegiatan</th></tr></thead><tbody>
<tr><td>Diskusi awal</td><td>Memahami kronologi dan kebutuhan pembuktian</td></tr>
<tr><td>Review dokumen</td><td>Kontrak, pembayaran, rekening koran, bukti pekerjaan</td></tr>
<tr><td>Perhitungan</td><td>Menghitung dengan metode yang disepakati</td></tr>
<tr><td>Laporan</td><td>Laporan tertulis yang ditandatangani akuntan publik</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Laporan tertulis yang menjelaskan metode dan perhitungan dengan lengkap umumnya sudah memadai sebagai dasar pihak yang memerlukan. Bila kemudian penyidik atau pengadilan memerlukan penjelasan langsung, akuntan dapat hadir sebagai ahli. Kehadiran ini biasanya dihitung terpisah dari pembuatan laporan, karena jumlah dan jadwalnya tidak bisa dipastikan di awal.</p></div>
<h2>Independen, Bukan Membela</h2>
<p>Akuntan yang menghitung kerugian bekerja berdasarkan bukti. Hasilnya bisa lebih kecil atau lebih besar dari perkiraan pemberi tugas. Justru karena itu laporannya punya bobot. Laporan yang terkesan memihak mudah dipatahkan di persidangan.</p>
<div class="pf-fold"><p>Bila dokumen belum lengkap, perhitungan bisa dibuat dengan asumsi yang ditulis terang. Asumsi yang jelas lebih baik daripada angka yang tampak pasti tetapi tidak berdasar.</p></div>
''' + PENUTUP,
  [('Apakah laporan kerugian bisa dipakai di kepolisian?', 'Laporan tertulis dengan metode dan bukti yang jelas umumnya dapat menjadi bahan bagi penyidik. Penilaian akhirnya ada pada aparat penegak hukum.'),
   ('Berapa lama menyusun laporan kerugian?', 'Tergantung jumlah dan kelengkapan dokumen. Penawaran biasanya dikunci setelah dokumen awal dilihat.'),
   ('Apakah hadir sebagai ahli termasuk dalam laporan?', 'Umumnya dihitung terpisah per kehadiran, karena jumlah dan jadwalnya ditentukan proses hukum.')])

A('ahli-akuntansi-di-penyidikan-dan-persidangan',
  'Akuntan sebagai Ahli di Penyidikan dan Persidangan',
  'Akuntan sebagai Ahli di Penyidikan dan Persidangan: Peran dan Persiapannya',
  'Kapan akuntan diminta menjadi ahli dalam perkara pidana atau perdata? Ini peran ahli akuntansi, bedanya dengan saksi, dan persiapan memberi keterangan.',
  'ahli akuntansi persidangan', CAT, 6, CTA,
  'Halo Pak Ananta, perkara kami membutuhkan ahli akuntansi. Saya ingin bertanya prosesnya.',
  [JDIH, IAPI],
  ['laporan-penghitungan-kerugian-proyek-akuntan-publik', 'kerja-sama-kuasa-hukum-pembuktian-kerugian', 'metode-menghitung-kerugian-keuangan', 'dokumen-menghitung-kerugian-penggelapan'],
  '''
<p>Dalam perkara yang menyangkut uang, seperti penggelapan, penipuan, wanprestasi, atau sengketa bagi hasil, angka sering menjadi inti perdebatan. Penyidik, jaksa, hakim, atau kuasa hukum bisa membutuhkan keterangan ahli akuntansi untuk menjelaskan bagaimana angka itu diperoleh.</p>
<h2>Ahli Bukan Saksi Fakta</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th></th><th>Saksi Fakta</th><th>Ahli</th></tr></thead><tbody>
<tr><td>Dasar keterangan</td><td>Apa yang dilihat, didengar, dialami</td><td>Keahlian dan analisis atas bukti</td></tr>
<tr><td>Contoh</td><td>Staf yang mengetahui transaksi</td><td>Akuntan yang menganalisis transaksi</td></tr>
<tr><td>Yang disampaikan</td><td>Kejadian</td><td>Metode, perhitungan, pendapat profesional</td></tr>
</tbody></table></div>
<h2>Kapan Ahli Akuntansi Dibutuhkan</h2>
<ul>
<li>Nilai kerugian dipersoalkan pihak lawan.</li>
<li>Transaksi banyak dan berlapis, sulit dipahami tanpa analisis.</li>
<li>Ada laporan keuangan atau pembukuan yang perlu ditafsirkan.</li>
<li>Penyidik meminta klarifikasi atas laporan penghitungan kerugian.</li>
</ul>
<h2>Persiapan Sebelum Memberi Keterangan</h2>
<ol>
<li>Laporan tertulis selesai lebih dulu, karena keterangan ahli berpijak pada analisis yang terdokumentasi.</li>
<li>Ahli mempelajari ulang dokumen dan pertanyaan yang mungkin diajukan.</li>
<li>Kuasa hukum dan ahli menyamakan pemahaman tentang pokok perkara, tanpa mengarahkan isi pendapat.</li>
</ol>
<div class="pf-fold"><p>Ahli wajib menyampaikan pendapat secara jujur sesuai keahliannya. Kuasa hukum boleh menjelaskan konteks perkara, tetapi isi pendapat ahli tetap ditentukan oleh analisis atas bukti. Ini yang membuat keterangan ahli bernilai.</p></div>
<h2>Kredibilitas Ahli</h2>
<p>Hal yang biasanya diperhatikan: kualifikasi profesi seperti akuntan publik, sertifikasi forensik, pengalaman, serta konsistensi antara laporan tertulis dan keterangan lisan.</p>
<div class="pf-fold"><p>Jadwal pemeriksaan dan persidangan sering berubah. Karena itu kehadiran ahli biasanya dihitung per kehadiran, terpisah dari penyusunan laporan.</p></div>
''' + PENUTUP,
  [('Apa beda ahli dan saksi?', 'Saksi menerangkan apa yang ia alami. Ahli menerangkan pendapat berdasarkan keahlian dan analisis atas bukti.'),
   ('Apakah ahli bisa diminta oleh pihak pelapor?', 'Bisa diajukan oleh pihak yang berperkara sesuai hukum acara yang berlaku, dan juga bisa diminta penyidik.'),
   ('Apakah harus ada laporan tertulis dulu?', 'Sangat disarankan, supaya keterangan ahli berpijak pada analisis yang terdokumentasi.')])

A('dokumen-menghitung-kerugian-penggelapan',
  'Dokumen untuk Menghitung Kerugian Penggelapan',
  'Dokumen yang Dibutuhkan untuk Menghitung Kerugian Penggelapan dan Penipuan',
  'Mau menghitung kerugian akibat penggelapan atau penipuan? Ini dokumen yang perlu dikumpulkan, cara menjaga keasliannya, dan urutan pengiriman ke akuntan.',
  'dokumen kerugian penggelapan', CAT, 5, CTA,
  'Halo Pak Ananta, kami mengalami penggelapan dan ingin tahu dokumen apa yang perlu disiapkan untuk menghitung kerugian.',
  [JDIH],
  ['laporan-penghitungan-kerugian-proyek-akuntan-publik', 'metode-menghitung-kerugian-keuangan', 'ahli-akuntansi-di-penyidikan-dan-persidangan', 'pisahkan-uang-pribadi-dan-perusahaan'],
  '''
<p>Kerugian yang dihitung tanpa dokumen hanya menjadi klaim. Kerugian yang dihitung dari dokumen menjadi bukti. Begitu ada dugaan penggelapan atau penipuan, langkah paling penting adalah mengumpulkan dan mengamankan dokumen sebelum hilang atau berubah.</p>
<h2>Dokumen Utama</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Dokumen</th><th>Membuktikan</th></tr></thead><tbody>
<tr><td>Kontrak, perjanjian, PO, surat penunjukan</td><td>Hak dan kewajiban para pihak</td></tr>
<tr><td>Rekening koran asli dari bank</td><td>Aliran uang keluar dan masuk</td></tr>
<tr><td>Bukti transfer, kuitansi, invoice</td><td>Pembayaran yang dilakukan</td></tr>
<tr><td>Berita acara, laporan progres, foto pekerjaan</td><td>Apa yang benar-benar dikerjakan</td></tr>
<tr><td>Pembukuan, laporan kas, stok</td><td>Catatan internal perusahaan</td></tr>
<tr><td>Percakapan WhatsApp dan email</td><td>Kesepakatan dan pengakuan</td></tr>
</tbody></table></div>
<h2>Menjaga Keaslian</h2>
<ul>
<li>Unduh rekening koran langsung dari bank, jangan diedit.</li>
<li>Ekspor percakapan WhatsApp lengkap, jangan hanya tangkapan layar terpilih.</li>
<li>Simpan salinan asli di tempat terpisah sebelum diolah.</li>
<li>Catat siapa yang menyerahkan dokumen dan kapan.</li>
</ul>
<div class="pf-fold"><p>Dokumen yang pernah diubah, sekecil apa pun, bisa membuat pihak lawan meragukan seluruh bukti. Bila ada dokumen yang hanya tersedia dalam bentuk foto atau salinan, sampaikan apa adanya. Akuntan akan mencatat keterbatasan itu dalam laporannya.</p></div>
<h2>Urutan Pengiriman</h2>
<ol>
<li>Kronologi singkat satu halaman: siapa, kapan, berapa, bagaimana.</li>
<li>Kontrak dan dokumen dasar.</li>
<li>Bukti pembayaran dan rekening koran.</li>
<li>Bukti pekerjaan atau barang yang diterima.</li>
<li>Dokumen pendukung lain.</li>
</ol>
<div class="pf-fold"><p>Kronologi membantu akuntan memahami perkara dalam beberapa menit, sehingga diskusi awal langsung fokus pada dokumen yang menentukan. Kronologi tidak perlu ditulis dengan bahasa hukum, cukup urutan kejadian dengan tanggal dan nilai.</p></div>
''' + PENUTUP,
  [('Apakah tangkapan layar WhatsApp bisa dipakai?', 'Bisa sebagai pendukung, tetapi ekspor percakapan lengkap lebih kuat karena konteksnya utuh.'),
   ('Bagaimana bila dokumen tidak lengkap?', 'Perhitungan tetap bisa dibuat dengan asumsi yang ditulis jelas, dan keterbatasannya dicatat dalam laporan.'),
   ('Siapa yang sebaiknya mengumpulkan dokumen?', 'Satu orang yang dipercaya, dengan catatan kapan dan dari siapa setiap dokumen diterima.')])

A('kerja-sama-kuasa-hukum-pembuktian-kerugian',
  'Kerja Bersama Kuasa Hukum dalam Pembuktian Kerugian',
  'Kerja Bersama Kuasa Hukum: Menyamakan Kebutuhan Pembuktian Angka Kerugian',
  'Perkara kerugian paling kuat bila akuntan dan kuasa hukum bekerja dari awal. Ini cara membagi peran, menyamakan kebutuhan bukti, dan menjaga independensi.',
  'akuntan dan pengacara kerugian', CAT, 5, CTA,
  'Halo Pak Ananta, kami sudah punya kuasa hukum dan butuh akuntan untuk menghitung kerugian. Boleh diskusi bertiga?',
  [JDIH],
  ['laporan-penghitungan-kerugian-proyek-akuntan-publik', 'ahli-akuntansi-di-penyidikan-dan-persidangan', 'dokumen-menghitung-kerugian-penggelapan', 'metode-menghitung-kerugian-keuangan'],
  '''
<p>Banyak pemberi tugas datang ke akuntan setelah menunjuk kuasa hukum, atau sebaliknya. Pekerjaan berjalan jauh lebih efektif bila keduanya berkomunikasi sejak awal. Kuasa hukum memahami apa yang perlu dibuktikan, akuntan memahami bagaimana angka dibuktikan.</p>
<h2>Pembagian Peran</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Kuasa Hukum</th><th>Akuntan</th></tr></thead><tbody>
<tr><td>Menentukan dasar hukum dan strategi perkara</td><td>Menentukan metode perhitungan</td></tr>
<tr><td>Menjelaskan unsur yang perlu dibuktikan</td><td>Menghitung nilai dari dokumen</td></tr>
<tr><td>Mengelola proses dengan penyidik atau pengadilan</td><td>Menyusun laporan dan memberi keterangan ahli bila diminta</td></tr>
</tbody></table></div>
<h2>Menyamakan Kebutuhan Sejak Awal</h2>
<ul>
<li>Perkara pidana atau perdata?</li>
<li>Kerugian apa yang ingin dibuktikan: dana yang hilang, pekerjaan yang tidak dikerjakan, atau keuntungan yang hilang?</li>
<li>Periode berapa?</li>
<li>Dokumen apa yang sudah diserahkan ke penyidik?</li>
</ul>
<div class="pf-fold"><p>Pertanyaan ini menentukan metode. Perhitungan untuk laporan polisi bisa berbeda fokusnya dengan perhitungan untuk gugatan ganti rugi. Bila tidak disamakan di awal, laporan bisa harus direvisi di tengah jalan.</p></div>
<h2>Komunikasi yang Praktis</h2>
<p>Grup percakapan bertiga, antara pemberi tugas, kuasa hukum, dan akuntan, sering menjadi cara paling praktis. Dokumen dan pembahasan berada di satu tempat, dan pemberi tugas tetap mengikuti setiap perkembangan.</p>
<h2>Independensi Tetap Dijaga</h2>
<p>Kuasa hukum mewakili kepentingan klien. Akuntan menghitung berdasarkan bukti. Pembagian ini justru menguntungkan klien, karena laporan yang independen lebih sulit dibantah pihak lawan.</p>
<div class="pf-fold"><p>Bila hasil perhitungan berbeda dengan angka yang semula diklaim, lebih baik diketahui di awal. Kuasa hukum bisa menyesuaikan strategi sebelum perkara berjalan jauh.</p></div>
''' + PENUTUP,
  [('Perlukah kuasa hukum sebelum menghitung kerugian?', 'Tidak wajib, tetapi bila perkara akan dibawa ke jalur hukum, melibatkan kuasa hukum sejak awal membuat perhitungan lebih tepat sasaran.'),
   ('Apakah kuasa hukum bisa mengarahkan hasil perhitungan?', 'Kuasa hukum menjelaskan kebutuhan pembuktian, tetapi hasil perhitungan ditentukan oleh bukti.'),
   ('Bagaimana komunikasi bertiga yang efektif?', 'Satu grup percakapan dan satu folder dokumen bersama, dengan pemberi tugas tetap ikut di dalamnya.')])

A('metode-menghitung-kerugian-keuangan',
  'Metode Menghitung Kerugian Keuangan dalam Perkara',
  'Metode Menghitung Kerugian Keuangan: Dana Hilang, Biaya Pengganti, dan Keuntungan yang Hilang',
  'Kerugian bisa dihitung dengan beberapa metode: dana yang tidak dipertanggungjawabkan, selisih pekerjaan, biaya pengganti, dan keuntungan yang hilang.',
  'metode menghitung kerugian', CAT, 7, CTA,
  'Halo Pak Ananta, saya ingin tahu metode yang tepat untuk menghitung kerugian dalam kasus kami.',
  [IAPI, JDIH],
  ['laporan-penghitungan-kerugian-proyek-akuntan-publik', 'dokumen-menghitung-kerugian-penggelapan', 'ahli-akuntansi-di-penyidikan-dan-persidangan', 'kerja-sama-kuasa-hukum-pembuktian-kerugian'],
  '''
<p>Tidak ada satu rumus kerugian untuk semua perkara. Metode yang dipilih bergantung pada apa yang terjadi dan apa yang ingin dibuktikan. Memilih metode yang tepat sering lebih menentukan daripada ketelitian hitungannya.</p>
<h2>Metode yang Umum Dipakai</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Metode</th><th>Cocok Untuk</th><th>Inti Perhitungan</th></tr></thead><tbody>
<tr><td>Dana yang tidak dapat dipertanggungjawabkan</td><td>Penggelapan, penyalahgunaan dana</td><td>Dana diterima dikurangi penggunaan yang sah dan terbukti</td></tr>
<tr><td>Selisih nilai pekerjaan</td><td>Proyek tidak selesai, wanprestasi</td><td>Pembayaran dikurangi nilai pekerjaan yang benar-benar dikerjakan</td></tr>
<tr><td>Biaya pengganti</td><td>Pekerjaan harus diselesaikan pihak lain</td><td>Tambahan biaya untuk menyelesaikan pekerjaan</td></tr>
<tr><td>Keuntungan yang hilang</td><td>Usaha terganggu, kontrak batal</td><td>Laba yang wajar diharapkan dikurangi laba yang diperoleh</td></tr>
</tbody></table></div>
<h2>Contoh Sederhana</h2>
<p>Sebuah proyek dibayar Rp1 miliar. Pekerjaan yang dikerjakan, berdasarkan berita acara dan pemeriksaan, senilai Rp600 juta. Dengan metode selisih nilai pekerjaan, kerugian awal adalah Rp400 juta. Bila pemilik proyek harus membayar kontraktor lain Rp500 juta untuk menyelesaikan sisa pekerjaan yang seharusnya senilai Rp400 juta, ada tambahan biaya pengganti Rp100 juta.</p>
<div class="pf-fold"><p>Angka di atas hanya ilustrasi. Dalam praktik, setiap komponen harus didukung dokumen: kontrak, berita acara, penilaian progres, dan bukti pembayaran ke kontraktor pengganti. Metode yang dipakai juga dijelaskan alasannya di laporan.</p></div>
<h2>Hal yang Sering Diperdebatkan</h2>
<ul>
<li><b>Penggunaan dana yang diklaim sah.</b> Pihak lawan menunjukkan pengeluaran, akuntan menilai apakah ada buktinya dan apakah relevan.</li>
<li><b>Nilai pekerjaan terpasang.</b> Kadang perlu penilai teknis untuk menghitung progres fisik.</li>
<li><b>Keuntungan yang hilang.</b> Paling sering dibantah karena bersifat perkiraan, sehingga asumsinya harus kuat.</li>
<li><b>Bunga atau nilai waktu uang.</b> Apakah dimasukkan tergantung kebutuhan perkara dan dasar hukumnya.</li>
</ul>
<div class="pf-fold"><p>Gabungan beberapa metode boleh dipakai, asalkan tidak menghitung kerugian yang sama dua kali. Ini kesalahan yang sering dimanfaatkan pihak lawan.</p></div>
''' + PENUTUP,
  [('Metode mana yang paling kuat?', 'Yang paling sesuai dengan kejadian dan paling didukung dokumen. Kekuatan metode ada pada bukti yang menopangnya.'),
   ('Apakah keuntungan yang hilang bisa diklaim?', 'Bisa dihitung, tetapi asumsinya harus kuat karena bersifat perkiraan dan sering dibantah.'),
   ('Perlukah penilai teknis untuk proyek fisik?', 'Kadang perlu, terutama bila nilai pekerjaan terpasang dipersoalkan.')])
