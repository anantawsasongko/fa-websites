from _a import A

CAT = 'Kredit Bank'
CTA = ('/konsultan-kredit-bank/', 'Konsultan Kredit Bank')
OJK = ('https://www.ojk.go.id/', 'Otoritas Jasa Keuangan')
BI = ('https://www.bi.go.id/', 'Bank Indonesia')
PENUTUP = ('<h2>Diskusi dengan FA Indonesia</h2><p>Untuk pengajuan kredit, Anda bicara langsung dengan Ananta W. Sasongko, CPA. '
           'Biasanya dimulai dari membaca rekening koran dan laporan keuangan, lalu disusun rencana kerja dan paket pengajuan yang sesuai dengan cara bank menilai.</p>')

A('penjualan-tunai-dan-money-changer-dibaca-bank',
  'Penjualan Tunai dan Money Changer: Cara Bank Membacanya',
  'Penjualan Tunai Lewat Sales dan Money Changer: Kenapa Bank Sulit Mengakuinya',
  'Banyak pelanggan bayar tunai ke sales, lalu uangnya dipakai bayar pemasok lewat money changer. Ini dampaknya ke analisis kredit dan cara merapikannya.',
  'penjualan tunai analisis kredit bank', CAT, 6, CTA,
  'Halo Pak Ananta, banyak penjualan kami tunai dan tidak masuk rekening perusahaan. Saya ingin tanya dampaknya ke pengajuan kredit.',
  [OJK, BI],
  ['cara-menaikkan-plafon-kredit-top-up', 'pisahkan-uang-pribadi-dan-perusahaan', 'rasio-keuangan-yang-dilihat-bank', 'alasan-kredit-bank-ditolak'],
  '''
<p>Di usaha distribusi dan perdagangan, masih banyak pelanggan yang membayar tunai ke sales. Uang tunai itu kemudian dipakai langsung untuk membayar pemasok, kadang lewat money changer bila pemasoknya di luar negeri. Secara operasional praktis. Masalahnya muncul saat perusahaan mengajukan atau memperpanjang kredit: omzet yang besar tidak terlihat di rekening.</p>
<h2>Kenapa Bank Bertumpu pada Rekening</h2>
<p>Analis kredit menilai kemampuan bayar dari arus kas yang bisa diverifikasi. Rekening koran adalah bukti paling kuat karena datang dari bank. Penjualan tunai yang tidak pernah masuk rekening sulit diverifikasi, sehingga sering tidak dihitung, atau dihitung dengan potongan besar.</p>
<div class="pf-fold"><p>Akibatnya, plafon yang disetujui bisa jauh di bawah kebutuhan. Perusahaan yang omzetnya besar terlihat kecil, dan rasio perputaran rekening terhadap omzet di laporan keuangan menjadi rendah. Bila selisihnya besar tanpa penjelasan, bank bahkan bisa meragukan laporan keuangannya.</p></div>
<h2>Risiko Tambahan dari Money Changer</h2>
<ul>
<li>Pembayaran ke pemasok tidak tercatat sebagai transaksi perusahaan di bank.</li>
<li>Bukti transaksi sering atas nama perorangan.</li>
<li>Sulit membuktikan harga pokok dan utang dagang.</li>
</ul>
<h2>Cara Merapikan secara Bertahap</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Langkah</th><th>Dampak ke Penilaian Bank</th></tr></thead><tbody>
<tr><td>Rekap penerimaan tunai per pelanggan, 3 sampai 6 bulan terakhir</td><td>Memberi gambaran omzet riil yang bisa dijelaskan</td></tr>
<tr><td>Kumpulkan bukti transaksi money changer untuk pembayaran pemasok</td><td>Menjelaskan aliran uang keluar</td></tr>
<tr><td>Arahkan penagihan ke rekening perusahaan mulai bulan ini</td><td>Mutasi rekening naik, paling berpengaruh ke plafon</td></tr>
<tr><td>Setor tunai harian ke rekening sebelum dipakai</td><td>Setiap rupiah penjualan tercatat bank</td></tr>
<tr><td>Bayar pemasok dari rekening perusahaan</td><td>Harga pokok dan utang dagang bisa diverifikasi</td></tr>
</tbody></table></div>
<p>Perubahan ini tidak harus sekaligus. Dua atau tiga bulan mutasi yang lebih lengkap sudah membuat perbedaan saat analisis.</p>
<div class="pf-fold"><p>Sambil merapikan, laporan keuangan perlu tetap mencerminkan penjualan sebenarnya, termasuk yang tunai, dengan rekap yang bisa ditelusuri. Laporan yang jujur dan dapat dijelaskan lebih kuat daripada laporan yang dibuat menyesuaikan rekening saja.</p></div>
<h2>Jelaskan, Jangan Sembunyikan</h2>
<p>Bank lebih menerima perusahaan yang terbuka menjelaskan pola tunainya beserta rencana perbaikan, daripada perusahaan yang omzetnya tiba-tiba tidak cocok dengan rekening tanpa penjelasan.</p>
''' + PENUTUP,
  [('Apakah penjualan tunai dihitung bank?', 'Bisa dihitung bila ada rekap dan bukti yang meyakinkan, tetapi bobotnya biasanya lebih rendah daripada penerimaan lewat rekening.'),
   ('Berapa lama mutasi rekening perlu dirapikan?', 'Banyak bank melihat 6 sampai 12 bulan terakhir. Perbaikan 2 sampai 3 bulan sudah mulai terlihat.'),
   ('Apakah money changer dilarang?', 'Tidak, tetapi pembayaran pemasok sebaiknya terdokumentasi atas nama perusahaan supaya bisa diverifikasi.')])

A('perpanjangan-prk-sambil-mengajukan-ke-bank-lain',
  'Perpanjangan PRK Sambil Mengajukan ke Bank Lain',
  'Perpanjangan PRK Sambil Mengajukan Kredit ke Bank Lain: Urutan yang Aman',
  'PRK hampir jatuh tempo tapi ingin pindah atau menambah bank? Ini urutan aman supaya fasilitas lama tetap jalan dan pengajuan baru tidak terganggu.',
  'perpanjangan prk dan pindah bank', CAT, 6, CTA,
  'Halo Pak Ananta, fasilitas PRK kami hampir jatuh tempo dan kami ingin mengajukan ke bank lain. Boleh diskusi urutannya?',
  [OJK],
  ['syarat-biaya-cara-take-over-kredit-usaha', 'kmk-vs-kredit-investasi', 'slik-ojk-perusahaan-pengurus-kolektibilitas', 'syarat-dokumen-kredit-modal-kerja-perusahaan-2026'],
  '''
<p>Pinjaman rekening koran (PRK) adalah fasilitas modal kerja yang umumnya diperpanjang setiap tahun. Banyak perusahaan memanfaatkan momen perpanjangan untuk membandingkan tawaran bank lain, entah untuk plafon lebih besar, bunga lebih ringan, atau tambahan fasilitas. Urutannya penting, karena salah langkah bisa membuat fasilitas lama terganggu sebelum fasilitas baru cair.</p>
<h2>Amankan Fasilitas Lama Lebih Dulu</h2>
<p>Selama fasilitas baru belum pasti cair, PRK yang berjalan adalah sumber modal kerja. Ajukan perpanjangan tepat waktu, lengkapi dokumen yang diminta, dan jaga kolektibilitas tetap lancar.</p>
<ul>
<li>Ketahui tanggal jatuh tempo dan batas waktu pengajuan perpanjangan.</li>
<li>Siapkan laporan keuangan terbaru dan rekening koran.</li>
<li>Pastikan tidak ada tunggakan bunga atau pelanggaran syarat perjanjian.</li>
</ul>
<h2>Paket Pengajuan ke Bank Baru</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Dokumen</th><th>Catatan</th></tr></thead><tbody>
<tr><td>Laporan keuangan 2 tahun + tahun berjalan</td><td>Sebaiknya sampai triwulan terakhir</td></tr>
<tr><td>Rekening koran semua rekening, 6 sampai 12 bulan</td><td>Termasuk rekening di bank lama</td></tr>
<tr><td>Surat perpanjangan atau perjanjian PRK yang berjalan</td><td>Bank baru ingin melihat fasilitas yang akan diambil alih atau tetap jalan</td></tr>
<tr><td>Daftar pelanggan dan pemasok utama</td><td>Menjelaskan perputaran usaha</td></tr>
<tr><td>Dokumen agunan</td><td>Sertifikat, BPKB, dan penilaian bila ada</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Bank baru akan melihat SLIK, sehingga semua fasilitas di bank lain akan terlihat. Lebih baik dijelaskan sejak awal: fasilitas mana yang akan dilunasi, mana yang tetap berjalan, dan bagaimana agunannya.</p></div>
<h2>Bandingkan Tawaran secara Utuh</h2>
<ul>
<li>Plafon dan jenis fasilitas.</li>
<li>Bunga, provisi, biaya administrasi, dan biaya pelunasan di bank lama.</li>
<li>Tenor dan jadwal perpanjangan.</li>
<li>Syarat perjanjian, misalnya rasio yang harus dijaga.</li>
<li>Agunan tambahan yang diminta.</li>
</ul>
<h2>Waktu Pelunasan dan Pengalihan</h2>
<p>Bila memutuskan pindah, koordinasikan tanggal pencairan bank baru dengan pelunasan bank lama, termasuk proses roya dan pengalihan agunan. Jangan melunasi fasilitas lama sebelum pencairan fasilitas baru benar-benar pasti.</p>
<div class="pf-fold"><p>Perusahaan yang sedang merapikan rekening, misalnya mengarahkan penagihan ke rekening perusahaan, sebaiknya tetap melakukannya selama proses. Mutasi yang membaik selama masa pengajuan sering membantu negosiasi plafon.</p></div>
''' + PENUTUP,
  [('Apakah boleh mengajukan ke bank lain saat PRK berjalan?', 'Boleh. Yang penting fasilitas lama tetap lancar dan bank baru mendapat penjelasan yang jelas.'),
   ('Apakah bank baru tahu fasilitas di bank lama?', 'Ya, lewat SLIK OJK. Karena itu sebaiknya dijelaskan terbuka sejak awal.'),
   ('Kapan sebaiknya mulai mengajukan?', 'Beberapa bulan sebelum jatuh tempo, supaya ada waktu bila prosesnya lebih lama dari perkiraan.')])

A('kredit-konstruksi-developer-perumahan-dokumen',
  'Kredit Konstruksi Developer Perumahan: Dokumen dan Tahapan',
  'Kredit Konstruksi untuk Developer Perumahan: Dokumen, Tahapan, dan Rekening Proyek',
  'Developer perumahan butuh kredit konstruksi untuk membangun unit. Ini dokumen legal, teknis, dan keuangan yang diminta bank, serta soal rekening proyek.',
  'kredit konstruksi developer perumahan', CAT, 7, CTA,
  'Halo Pak Ananta, kami developer perumahan dan ingin mengajukan kredit konstruksi. Saya ingin diskusi persiapannya.',
  [OJK, ('https://www.btn.co.id/', 'Bank Tabungan Negara')],
  ['kredit-investasi-pabrik-gudang-mesin-syarat', 'dokumen-pengajuan-kredit-korporasi', 'kapan-perusahaan-butuh-kjpp-jasa-penilai', 'undisbursed-loan-cara-mempercepat-pencairan-kredit'],
  '''
<p>Developer perumahan, terutama di daerah, sering menghadapi pertanyaan yang sama dari bank: proyeknya sudah layak dibiayai atau belum? Kredit konstruksi membiayai pembangunan unit sebelum terjual, dan pelunasannya biasanya dari pencairan KPR pembeli. Karena itu bank menilai tiga hal sekaligus: legalitas lahan, kelayakan proyek, dan kemampuan developer.</p>
<h2>Dokumen Legal dan Perizinan</h2>
<ul>
<li>Akta perusahaan, NIB berbasis risiko, NPWP.</li>
<li>Sertifikat tanah induk atau pecahan.</li>
<li>Kesesuaian kegiatan pemanfaatan ruang (KKPR).</li>
<li>Persetujuan bangunan gedung dan site plan yang disahkan.</li>
<li>Sertifikat atau dokumen jalan lingkungan, bila sertifikat sudah dipecah.</li>
</ul>
<h2>Dokumen Teknis dan Keuangan</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Dokumen</th><th>Dipakai Bank Untuk</th></tr></thead><tbody>
<tr><td>Rencana anggaran biaya per tipe unit</td><td>Menentukan kebutuhan dana konstruksi</td></tr>
<tr><td>Jadwal pembangunan dan penjualan</td><td>Menyusun jadwal pencairan dan pelunasan</td></tr>
<tr><td>Data penjualan: booking, akad, KPR proses</td><td>Menilai daya serap pasar</td></tr>
<tr><td>Laporan keuangan dan rekening koran perusahaan</td><td>Menilai kemampuan developer</td></tr>
<tr><td>Rekening koran pribadi pengurus</td><td>Melihat aliran dana proyek yang lewat rekening pribadi</td></tr>
<tr><td>Penilaian agunan oleh KJPP atau taksasi bank</td><td>Menentukan nilai jaminan</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Banyak developer kecil menerima uang booking dan membayar kontraktor lewat rekening pribadi. Bank akan meminta rekening tersebut untuk melihat gambaran utuh proyek. Ini wajar. Yang lebih baik, mulai sekarang semua transaksi proyek dialirkan ke rekening perusahaan.</p></div>
<h2>Rekening Proyek</h2>
<p>Bank pemberi kredit konstruksi umumnya meminta rekening penampungan proyek di bank tersebut. Pencairan KPR pembeli masuk ke rekening ini, lalu sebagian dipakai melunasi kredit konstruksi per unit. Pahami mekanisme ini sejak awal supaya arus kas proyek tidak sesak.</p>
<h2>Kesalahan yang Sering Terjadi</h2>
<ul>
<li>Mengajukan kredit sebelum perizinan lengkap.</li>
<li>Rencana anggaran tidak dipisah per tahap.</li>
<li>Uang booking terpakai untuk proyek lain.</li>
<li>Tidak ada laporan keuangan perusahaan yang terpisah dari keuangan pemilik.</li>
</ul>
<div class="pf-fold"><p>Checklist dari bank biasanya panjang. Tidak perlu menunggu semuanya lengkap untuk mulai. Kirim dokumen yang sudah siap lebih dulu, sambil melengkapi sisanya, supaya analisis awal bisa berjalan.</p></div>
''' + PENUTUP,
  [('Apakah developer kecil bisa mendapat kredit konstruksi?', 'Bisa, bila legalitas lahan dan perizinan lengkap, proyek layak, dan keuangan developer bisa dipertanggungjawabkan.'),
   ('Kenapa bank meminta rekening pribadi pengurus?', 'Karena di developer kecil, aliran dana proyek sering lewat rekening pribadi. Bank ingin melihat gambaran utuh.'),
   ('Apa itu rekening penampungan proyek?', 'Rekening di bank pemberi kredit yang menampung pencairan KPR pembeli untuk melunasi kredit konstruksi per unit.')])

A('rencana-kerja-3-bulan-sebelum-mengajukan-kredit',
  'Rencana Kerja 3 Bulan Sebelum Mengajukan Kredit Usaha',
  'Rencana Kerja 3 Bulan Sebelum Mengajukan Kredit Usaha',
  'Pengajuan kredit lebih kuat bila disiapkan 3 bulan sebelumnya. Ini rencana kerja per bulan: diagnosa, perbaikan data, paket pengajuan, dan negosiasi.',
  'persiapan pengajuan kredit usaha', CAT, 6, CTA,
  'Halo Pak Ananta, kami berencana mengajukan kredit dalam beberapa bulan ke depan. Boleh dibantu menyusun persiapannya?',
  [OJK],
  ['prosedur-pengajuan-kredit-perusahaan-ke-bank', 'cara-mendapatkan-pinjaman-bank-untuk-usaha', 'kenapa-pengajuan-kredit-usaha-lama-diproses', 'dscr-adalah-cara-menghitung-kredit-bank'],
  '''
<p>Pengajuan kredit yang disiapkan mendadak sering berakhir dengan plafon kecil atau permintaan data yang tidak ada habisnya. Sebaliknya, perusahaan yang menyiapkan diri beberapa bulan sebelumnya datang ke bank dengan cerita yang jelas dan data yang konsisten. Berikut kerangka tiga bulan yang bisa disesuaikan.</p>
<h2>Bulan 1: Diagnosa dan Amankan yang Berjalan</h2>
<ul>
<li>Baca rekening koran 12 bulan terakhir, bandingkan dengan laporan keuangan.</li>
<li>Petakan semua fasilitas yang berjalan dan tanggal jatuh temponya.</li>
<li>Periksa SLIK perusahaan dan pengurus.</li>
<li>Amankan perpanjangan fasilitas yang akan jatuh tempo.</li>
<li>Hitung kebutuhan dana yang sebenarnya, bukan perkiraan kasar.</li>
</ul>
<h2>Bulan 2: Perbaiki Data dan Susun Paket</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Pekerjaan</th><th>Tujuan</th></tr></thead><tbody>
<tr><td>Rapikan laporan keuangan sampai bulan terakhir</td><td>Angka konsisten dengan rekening</td></tr>
<tr><td>Arahkan penerimaan ke rekening perusahaan</td><td>Mutasi rekening naik</td></tr>
<tr><td>Proyeksi arus kas dan kemampuan bayar</td><td>Menunjukkan DSCR yang aman</td></tr>
<tr><td>Ringkasan profil usaha dan rencana penggunaan dana</td><td>Analis cepat memahami usaha</td></tr>
<tr><td>Kumpulkan dokumen agunan</td><td>Menghindari tertunda di tahap akhir</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Ringkasan profil usaha sebaiknya pendek: apa usahanya, siapa pelanggan utamanya, bagaimana perputarannya, berapa kebutuhan dana dan untuk apa, serta bagaimana pengembaliannya. Analis kredit membaca banyak berkas setiap minggu. Berkas yang jelas akan didahulukan.</p></div>
<h2>Bulan 3: Ajukan, Jawab, dan Negosiasi</h2>
<ul>
<li>Ajukan ke bank yang paling sesuai dengan profil usaha.</li>
<li>Jawab pertanyaan analis dengan cepat dan konsisten.</li>
<li>Siapkan kunjungan lapangan.</li>
<li>Bandingkan tawaran: plafon, bunga, biaya, syarat perjanjian.</li>
</ul>
<div class="pf-fold"><p>Satu orang di perusahaan sebaiknya ditunjuk untuk berkomunikasi dengan bank, supaya jawaban tidak berbeda-beda. Perbedaan jawaban antara pemilik, keuangan, dan admin sering menimbulkan pertanyaan baru.</p></div>
<h2>Kenapa Tiga Bulan</h2>
<p>Tiga bulan cukup untuk memperbaiki pola mutasi rekening, menyusun laporan sampai triwulan terakhir, dan menyelesaikan dokumen yang tertinggal. Lebih pendek bisa, asalkan data dasarnya sudah rapi.</p>
''' + PENUTUP,
  [('Apakah harus tiga bulan?', 'Tidak selalu. Bila data sudah rapi, pengajuan bisa lebih cepat. Tiga bulan adalah kerangka untuk perusahaan yang masih perlu merapikan data.'),
   ('Apa yang paling berpengaruh ke plafon?', 'Arus kas yang terlihat di rekening, kemampuan bayar (DSCR), dan nilai agunan.'),
   ('Bolehkah mengajukan ke beberapa bank sekaligus?', 'Boleh, tetapi sebaiknya terarah. Pengajuan yang terlalu banyak bisa membingungkan dan menyita waktu.')])

A('laporan-keuangan-interim-triwulan-untuk-kredit',
  'Laporan Keuangan Interim Triwulan untuk Pengajuan Kredit',
  'Laporan Keuangan Interim (Triwulan) untuk Pengajuan Kredit: Kapan Diminta dan Cara Menyusunnya',
  'Bank sering meminta laporan keuangan sampai triwulan terakhir, bukan hanya laporan tahunan. Pahami kenapa, isinya apa, dan cara menyusunnya dengan cepat.',
  'laporan keuangan interim untuk bank', CAT, 5, CTA,
  'Halo Pak Ananta, bank meminta laporan keuangan sampai triwulan terakhir. Saya ingin tanya cara menyiapkannya.',
  [OJK, ('https://iaiglobal.or.id/', 'Ikatan Akuntan Indonesia')],
  ['laporan-keuangan-untuk-kredit-bank', 'rasio-keuangan-yang-dilihat-bank', 'syarat-dokumen-kredit-modal-kerja-perusahaan-2026', 'jasa-konsultan-kredit-bank-perusahaan'],
  '''
<p>Laporan tahunan menggambarkan kondisi sampai akhir tahun lalu. Bila pengajuan kredit dilakukan di bulan Oktober atau November, bank ingin tahu apa yang terjadi selama sembilan atau sepuluh bulan terakhir. Karena itu laporan keuangan interim, misalnya sampai akhir triwulan ketiga, hampir selalu diminta.</p>
<h2>Isi Laporan Interim</h2>
<ul>
<li>Laporan posisi keuangan pada akhir periode.</li>
<li>Laporan laba rugi dari awal tahun sampai akhir periode.</li>
<li>Pembanding: periode yang sama tahun lalu, atau akhir tahun lalu untuk neraca.</li>
<li>Catatan singkat untuk pos penting: utang bank, piutang, persediaan.</li>
</ul>
<h2>Yang Diperhatikan Bank</h2>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Hal</th><th>Pertanyaan Analis</th></tr></thead><tbody>
<tr><td>Tren pendapatan</td><td>Naik atau turun dibanding periode yang sama tahun lalu?</td></tr>
<tr><td>Kesesuaian dengan rekening koran</td><td>Pendapatan sejalan dengan mutasi masuk?</td></tr>
<tr><td>Utang bank</td><td>Sama dengan saldo di SLIK dan rekening pinjaman?</td></tr>
<tr><td>Piutang dan persediaan</td><td>Naik wajar atau menumpuk?</td></tr>
</tbody></table></div>
<div class="pf-fold"><p>Laporan interim tidak harus diaudit. Yang penting angkanya konsisten dengan rekening koran dan dengan laporan tahunan sebelumnya. Penyesuaian akhir tahun seperti penyusutan sebaiknya tetap dihitung secara proporsional, supaya laba interim tidak terlihat lebih tinggi dari seharusnya.</p></div>
<h2>Cara Menyusun dengan Cepat</h2>
<ol>
<li>Tutup buku per bulan: rekonsiliasi bank, piutang, utang.</li>
<li>Hitung penyusutan dan biaya dibayar di muka per bulan.</li>
<li>Lakukan hitung stok di akhir periode, atau gunakan data sistem yang andal.</li>
<li>Susun laporan dengan format yang sama seperti laporan tahunan.</li>
</ol>
<div class="pf-fold"><p>Perusahaan yang sudah terbiasa membuat laporan bulanan bisa menyerahkan laporan interim dalam hitungan hari. Perusahaan yang hanya membuat laporan setahun sekali sering butuh waktu lebih lama. Ini salah satu alasan laporan keuangan bulanan berguna, bukan hanya untuk bank tetapi juga untuk keputusan pemilik.</p></div>
''' + PENUTUP,
  [('Apakah laporan interim harus diaudit?', 'Umumnya tidak. Bank menerima laporan interim yang disusun perusahaan, asalkan konsisten dengan rekening dan laporan tahunan.'),
   ('Periode interim mana yang diminta?', 'Biasanya sampai akhir bulan atau triwulan terakhir sebelum pengajuan.'),
   ('Apakah penyusutan perlu dihitung di laporan interim?', 'Sebaiknya ya, secara proporsional, supaya laba interim tidak terlalu tinggi.')])
