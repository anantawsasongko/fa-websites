# -*- coding: utf-8 -*-
from _h import T
X = {}
D = {}
D['business-wrapping-sebelum-menjual-perusahaan']='Business wrapping merapikan legalitas, laporan keuangan, dan struktur usaha sebelum dijual. Ini yang dirapikan, urutan kerja, dan kesalahan umum.'
D['data-room-penjual-struktur-folder-kesalahan-umum']='Cara menyusun data room agar due diligence pembeli berjalan cepat: struktur folder, urutan upload, kontrol akses, dan kesalahan umum penjual.'
D['proyeksi-keuangan-untuk-bank-dan-investor']='Proyeksi keuangan yang dipercaya bank dan investor berangkat dari asumsi yang bisa diuji. Ini komponen, contoh asumsi, dan kesalahan umum.'
D['melanggar-kovenan-bank-langkah-pemilik-usaha']='Rasio melewati batas kovenan tidak otomatis membuat kredit ditarik. Ini jenis kovenan, langkah sebelum bank menghubungi, dan opsi waiver.'
D['laporan-keuangan-konsolidasian-grup-usaha-keluarga']='Punya beberapa PT tanpa laporan gabungan? Ini kapan konsolidasi dibutuhkan bank dan investor, langkah menyusunnya, dan jebakan transaksi antar PT.'
D['menjual-bpr-persiapan-penjual-persetujuan-ojk']='Pemilik BPR yang ingin menjual saham perlu menyiapkan laporan, kualitas kredit, dan calon pengendali yang lolos penilaian OJK. Ini urutan kerjanya.'
D['dokumen-transfer-pricing-master-file-local-file']='Bertransaksi dengan pihak afiliasi? Ini batas kewajiban master file dan local file menurut PMK 172/2023, isi dokumen, dan tenggat penyediaannya.'
D['pre-ipo-funding-investor-sebelum-ipo']='Pendanaan pre-IPO membawa investor masuk sebelum listing. Ini kapan cocok, apa yang dilihat investor, dampak ke harga IPO, dan persiapannya.'
D['cash-flow-forecast-13-minggu-perusahaan-menengah']='Forecast kas 13 minggu menunjukkan kapan kas mepet. Ini format, sumber data, contoh ilustrasi, dan cara memakainya untuk keputusan pembayaran.'
D['utang-pemegang-saham-dijadikan-modal-atau-tetap-pinjaman']='Dana pemilik di PT dicatat sebagai pinjaman atau modal? Ini perbedaannya, dampak ke bank, batas rasio utang terhadap modal 4:1, dan cara memutuskan.'

X['business-wrapping-sebelum-menjual-perusahaan']='''<h2>Contoh Ilustrasi: Dua Penjual dengan Laba yang Sama</h2>
<p>Bayangkan dua usaha distribusi dengan laba tahunan sama. Penjual pertama menyerahkan laporan tiga tahun yang cocok dengan SPT, daftar kontrak pelanggan, dan penjelasan tertulis atas biaya pribadi pemilik yang dikeluarkan dari laba. Penjual kedua menyerahkan laporan seadanya, dengan sebagian aset atas nama pemilik pribadi dan beberapa kontrak yang tidak ditemukan. Pembeli akan memberi nilai lebih tinggi dan proses lebih singkat kepada penjual pertama, bukan karena usahanya lebih baik, tetapi karena risikonya lebih mudah diukur.</p>
<h2>Apa yang Bukan Bagian dari Business Wrapping</h2>
<ul><li>Bukan mempercantik angka. Normalisasi laba hanya memisahkan hal yang memang bukan bagian dari operasi, dan semuanya harus bisa dibuktikan.</li>
<li>Bukan menyembunyikan masalah. Perkara, utang, dan risiko yang ada tetap diungkap dengan baik, karena pembeli yang menemukannya belakangan biasanya menuntut potongan harga lebih besar.</li>
<li>Bukan pengganti penasihat hukum. Perjanjian jual beli, perpindahan aset, dan akta tetap perlu notaris dan penasihat hukum.</li></ul>'''

X['data-room-penjual-struktur-folder-kesalahan-umum']='''<h2>Contoh Catatan Penjelasan yang Berguna</h2>
<p>Satu halaman catatan di depan folder keuangan sering menyelamatkan banyak pertanyaan. Contoh isinya (ilustrasi): "Pendapatan 2025 turun dibanding 2024 karena kontrak pelanggan terbesar berakhir pada Maret dan digantikan tiga pelanggan baru pada kuartal ketiga. Biaya sewa naik karena pindah gudang pada Juni. Beban lain-lain tahun 2024 berisi penghapusan piutang satu kali." Catatan semacam ini menunjukkan pemilik memahami usahanya dan tidak menyembunyikan apa pun.</p>
<h2>Tanda Data Room Sudah Siap Dibuka</h2>
<ul><li>Semua folder punya isi dan indeks terbaru.</li>
<li>Angka laba, aset, dan utang sama di laporan keuangan, SPT, dan laporan ke bank, atau selisihnya sudah dijelaskan.</li>
<li>Ada satu orang yang menjawab pertanyaan dan batas waktu jawab yang disepakati.</li>
<li>Dokumen sensitif sudah dipisah dan hanya dibuka bertahap.</li></ul>'''

X['proyeksi-keuangan-untuk-bank-dan-investor']='''<h2>Struktur Dokumen Proyeksi yang Rapi</h2>
''' + T(['Bagian','Isi'],[
 ['Ringkasan','Tujuan pembiayaan, jumlah, penggunaan dana, dan hasil utama proyeksi'],
 ['Asumsi','Daftar asumsi tertulis beserta dasarnya'],
 ['Tiga laporan','Laba rugi, posisi keuangan, dan arus kas, bulanan tahun pertama lalu tahunan'],
 ['Rasio','DSCR, DER, current ratio, dan rasio lain yang diminta bank, per skenario'],
 ['Sensitivitas','Dampak perubahan pendapatan, biaya, dan bunga terhadap kemampuan bayar'],
 ['Catatan risiko','Risiko utama dan langkah mitigasinya']]) + '''
<p>Dokumen yang tertata seperti ini membuat analis bank bisa menelusuri sendiri tanpa harus bertanya berulang, dan mempercepat proses penilaian.</p>'''

X['melanggar-kovenan-bank-langkah-pemilik-usaha']='''<h2>Contoh Ilustrasi: Rasio Melewati Batas karena Proyek Tertunda</h2>
<p>Sebuah kontraktor memiliki kovenan DSCR minimal 1,2 kali. Pada laporan akhir tahun rasionya 1,05 kali karena pembayaran termin proyek besar mundur ke kuartal berikutnya. Kontraktor ini menghitung ulang dengan definisi bank, menemukan bahwa uang muka proyek yang sudah diterima di awal Januari tidak masuk perhitungan, dan menyiapkan proyeksi bahwa rasio kembali 1,3 kali dalam dua kuartal. Dengan data itu, relationship manager punya dasar untuk mengusulkan waiver sementara kepada komite kredit. Perbedaannya dengan debitur yang diam adalah bank melihat debitur yang memahami masalahnya.</p>
<h2>Pertanyaan yang Biasanya Diajukan Bank</h2>
<ul><li>Apa penyebab rasio melewati batas, dan apakah sifatnya sementara?</li>
<li>Berapa kas yang tersedia dan kapan piutang besar tertagih?</li>
<li>Apa tindakan korektif yang sudah dijalankan?</li>
<li>Apakah pemegang saham siap menambah modal atau jaminan bila perlu?</li></ul>'''

X['laporan-keuangan-konsolidasian-grup-usaha-keluarga']='''<h2>Contoh Ilustrasi Eliminasi Transaksi Antar PT</h2>
<p>Misalkan PT Induk menjual barang Rp5 miliar ke PT Anak dalam satu tahun, dan PT Anak menjual sebagian ke pelanggan luar sebesar Rp4 miliar dari pembelian itu. Di laporan konsolidasian, penjualan Rp5 miliar antar PT dieliminasi dari pendapatan dan harga pokok, karena grup tidak menjual kepada dirinya sendiri. Barang Rp1 miliar yang masih tersisa di persediaan PT Anak perlu penyesuaian agar laba yang belum direalisasi tidak ikut diakui. Contoh ini sederhana, tetapi pada praktik yang melibatkan puluhan transaksi, rekonsiliasi inilah yang memakan waktu.</p>
<h2>Manfaat Selain untuk Bank dan Investor</h2>
<ul><li>Pemilik bisa melihat kinerja grup sebenarnya, termasuk PT yang selama ini ditutupi PT lain.</li>
<li>Utang antar PT dan utang pemegang saham menjadi terlihat, sehingga keputusan pendanaan lebih sehat.</li>
<li>Memudahkan persiapan audit, valuasi, dan rencana penjualan sebagian grup.</li></ul>'''

X['menjual-bpr-persiapan-penjual-persetujuan-ojk']='''<h2>Contoh Ilustrasi Pertanyaan Pembeli atas Sampel Kredit</h2>
<p>Pembeli biasanya memilih sampel kredit terbesar dan kredit bermasalah, lalu meminta berkas lengkap: permohonan, analisis, perjanjian, pengikatan agunan, dan riwayat pembayaran. Bila dari sepuluh berkas ada tiga yang agunannya belum diikat sempurna, pembeli akan memperlakukannya sebagai risiko dan meminta penyesuaian harga atau jaminan dari penjual. Karena itu, penjual yang memeriksa sendiri sampel kreditnya sebelum pembeli datang, dan melengkapi yang bisa dilengkapi, berada pada posisi tawar yang lebih baik.</p>
<h2>Peran Pihak Lain dalam Transaksi</h2>
<ul><li><b>Notaris dan penasihat hukum</b> untuk perjanjian dan akta.</li>
<li><b>Akuntan publik</b> untuk audit atau review laporan yang mendasari harga.</li>
<li><b>Penilai</b> bila dibutuhkan untuk aset tertentu.</li>
<li><b>Penasihat transaksi</b> untuk valuasi, mencari pembeli, dan mengatur jadwal.</li></ul>'''

X['dokumen-transfer-pricing-master-file-local-file']='''<h2>Contoh Ilustrasi: Pinjaman dari Induk</h2>
<p>Sebuah PT dengan peredaran bruto tahun lalu Rp60 miliar menerima pinjaman Rp10 miliar dari perusahaan induk dengan bunga 3 persen, sedangkan bank independen menawarkan bunga sekitar 10 persen untuk risiko serupa. Peredaran bruto sudah melewati Rp50 miliar sehingga dokumen lokal wajib disiapkan. Dalam dokumen itu, perusahaan perlu menjelaskan perjanjian, analisis kesebandingan bunga, dan alasan tingkat bunga yang dipakai. Angka ini ilustrasi; hasil analisis nyata bergantung pada data pembanding dan kondisi transaksi.</p>
<h2>Daftar Cek Singkat</h2>
<ul><li>Apakah ada transaksi dengan pihak afiliasi pada tahun pajak ini?</li>
<li>Apakah peredaran bruto tahun lalu melewati Rp50 miliar, atau nilai transaksi afiliasi melewati batas PMK?</li>
<li>Apakah ada perjanjian tertulis untuk setiap transaksi afiliasi?</li>
<li>Apakah dasar harga bisa dijelaskan dengan data pembanding?</li>
<li>Apakah ikhtisar sudah siap untuk dilampirkan pada SPT Tahunan?</li></ul>'''

X['pre-ipo-funding-investor-sebelum-ipo']='''<h2>Contoh Ilustrasi Dilusi</h2>
<p>Pemilik memegang 100 persen saham perusahaan bernilai Rp200 miliar. Investor pre-IPO masuk dengan Rp30 miliar pada valuasi pra-investasi Rp200 miliar, sehingga mendapat sekitar 13 persen. Saat IPO, perusahaan menerbitkan saham baru sekitar 20 persen dari modal ditempatkan setelah IPO. Kepemilikan pemilik lama turun lagi. Ilustrasi ini menunjukkan mengapa pemilik perlu menghitung kepemilikan akhir yang diinginkan sebelum menerima investor pertama.</p>
<h2>Pertanyaan yang Sebaiknya Dijawab Sebelum Menerima Investor</h2>
<ul><li>Untuk apa dana ini, dan apakah rencananya bisa dijelaskan secara tertulis?</li>
<li>Apakah hak yang diminta investor sejalan dengan rencana menjadi perusahaan terbuka?</li>
<li>Apa yang terjadi bila IPO tertunda atau batal?</li>
<li>Siapa yang akan duduk di direksi dan komisaris setelah investor masuk?</li></ul>'''

X['cash-flow-forecast-13-minggu-perusahaan-menengah']='''<h2>Rutinitas Mingguan yang Sederhana</h2>
''' + T(['Hari','Kegiatan'],[
 ['Senin','Perbarui saldo bank aktual dan realisasi penerimaan serta pembayaran minggu lalu'],
 ['Selasa','Bandingkan dengan prediksi, catat selisih dan penyebabnya'],
 ['Rabu','Perbarui daftar umur piutang dan jadwal tagih'],
 ['Kamis','Bahas minggu-minggu yang menembus batas kas minimum dan putuskan tindakan'],
 ['Jumat','Kirim ringkasan satu halaman kepada pemilik atau direksi']]) + '''
<p>Ringkasan satu halaman yang konsisten jauh lebih berguna daripada model rumit yang tidak pernah dibaca.</p>'''

X['utang-pemegang-saham-dijadikan-modal-atau-tetap-pinjaman']='''<h2>Contoh Ilustrasi Dampak ke Rasio</h2>
<p>Sebuah PT memiliki ekuitas Rp5 miliar, utang bank Rp8 miliar, dan utang pemegang saham Rp7 miliar. Bila semua dianggap utang, utang total Rp15 miliar dan rasio utang terhadap ekuitas 3 kali. Bila Rp7 miliar dijadikan modal disetor, ekuitas menjadi Rp12 miliar dan rasionya sekitar 0,67 kali. Selisihnya besar, dan bisa memengaruhi keputusan bank. Namun dana pemilik tidak lagi bisa ditarik sebagai pinjaman. Ini angka ilustrasi; keputusan nyata perlu melihat kebutuhan kas pemilik dan ketentuan perjanjian kredit yang berlaku.</p>
<h2>Bila Dijadikan Modal, Apa yang Perlu Disiapkan</h2>
<ul><li>Persetujuan RUPS dan akta notaris yang sesuai.</li>
<li>Pencatatan perubahan pada instansi terkait.</li>
<li>Penyesuaian laporan keuangan dan catatan atas perubahan modal.</li>
<li>Pemberitahuan atau persetujuan bank bila ada kovenan yang mengatur perubahan modal.</li></ul>'''
