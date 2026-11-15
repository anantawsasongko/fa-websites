# -*- coding: utf-8 -*-
"""Kompasiana (akun pribadi Bos): 10 opini/analisis, sudut pandang orang pertama, tanpa tabel, maksimal 2 link per artikel.
Tidak menyebut gelar, tidak menyebut nama perusahaan tempat bekerja, tidak ada angka pencapaian pribadi."""
from _k import A

FA = 'https://faindonesia.co.id'
US = 'https://updatesak.com'
CA = 'https://cariakuntan.com'
TAG_ABC = ['rumah sakit', 'unit cost', 'activity based costing', 'manajemen biaya', 'akuntansi manajemen']
TAG_PE = ['rumah sakit', 'private equity', 'venture capital', 'investasi', 'pendanaan']
TAG_CFO = ['fractional cfo', 'cfo', 'keuangan perusahaan', 'umkm', 'manajemen keuangan']
S_KEK = ('Bisnis.com: Warga RI Banyak Berobat ke Luar Negeri, KEK Disiapkan Jadi Pusat Kesehatan (12 Mei 2026)', 'https://ekonomi.bisnis.com/read/20260512/12/1973351/warga-ri-banyak-berobat-ke-luar-negeri-kek-disiapkan-jadi-pusat-kesehatan')
S_JKN = ('ANTARA: Kemenkes Uji Coba Reformasi JKN di Muara Enim (Oktober 2026)', 'https://www.antaranews.com/berita/5771342/kemenkes-uji-coba-reformasi-jkn-di-muara-enim-pangkas-waktu-tunggu')
S_QUAD = ('Business Wire: Quadria Capital Closes Oversubscribed US$1 Billion Fund III (26 Mei 2025)', 'https://www.businesswire.com/news/home/20250526754879/en/Quadria-Capital-Closes-Oversubscribed-US%241-Billion-Fund-III-to-Advance-Healthcare-Transformation-Across-Asia')
S_VISI = ('Fortune Indonesia: VISI Siapkan Rp286 M untuk Akuisisi RS Hasna Medika (27 Agustus 2026)', 'https://www.fortuneidn.com/business/visi-milik-nagita-raffi-siapkan-rp286-m-untuk-akuisisi-rs-hasna-medika-00-4vfn9-773b6y')

FQ = [('-', '-'), ('-', '-'), ('-', '-')]   # Kompasiana tidak memakai FAQ


def K(**a):
    a.setdefault('faq', FQ); a.setdefault('category', 'Money'); a.setdefault('wa', '-')
    a['seo_title'] = a['title'][:65]
    return A(site='ks', **a)


# ================================================================== ABC
K(topik='abc', kota='Malang', kota_slug='malang', slug='rumah-sakit-rajin-menghitung-pasien-lupa-menghitung-biaya',
  title='Rumah Sakit Rajin Menghitung Pasien, Lupa Menghitung Biaya',
  description='Catatan dari Malang tentang rumah sakit yang hafal jumlah pasiennya tetapi tidak tahu biaya satu layanan, dan mengapa activity based costing layak dicoba.',
  keyword='unit cost rumah sakit', tags=TAG_ABC, sources=[S_JKN],
  body_html=f'''
<p>Setiap kali pulang ke Malang, saya melewati beberapa rumah sakit yang halaman parkirnya selalu penuh. Dari luar semuanya tampak sehat. Namun pengalaman mengurus keuangan rumah sakit mengajarkan saya satu hal: parkiran penuh dan rekening penuh adalah dua hal yang berbeda.</p>
<p>Kebanyakan direktur rumah sakit hafal angka kunjungan, tingkat hunian tempat tidur, dan jumlah operasi bulan lalu. Ketika ditanya berapa biaya satu persalinan sesar atau satu tindakan cuci darah di rumah sakitnya, jawabannya sering berupa perkiraan, atau tarif. Padahal tarif adalah harga jual. Biaya adalah cerita lain.</p>
<h2>Angka rata-rata yang menenangkan</h2>
<p>Sebagian besar rumah sakit sebenarnya sudah menghitung unit cost. Caranya, biaya unit penunjang dibagikan ke unit pelayanan, lalu total biaya tiap unit dibagi jumlah hari rawat atau jumlah tindakan. Hasilnya satu angka rata-rata per unit.</p>
<p>Angka itu menenangkan karena sederhana. Masalahnya, pasien tidak datang sebagai rata-rata. Di bangsal yang sama ada ibu melahirkan normal yang pulang dua hari kemudian dan pasien pascabedah yang butuh perawat tiga kali lebih sering. Keduanya dibebani biaya per hari yang sama. Yang satu terlihat mahal, yang lain terlihat murah, dan keduanya keliru.</p>
<h2>Biaya mengikuti aktivitas, bukan mengikuti kamar</h2>
<p>Activity based costing, atau ABC, berangkat dari gagasan yang masuk akal: biaya timbul karena ada aktivitas, dan setiap layanan memakai aktivitas dalam takaran berbeda. Admisi, asuhan keperawatan, kamar operasi, farmasi, gizi. Masing-masing punya pemicu: jumlah pasien, jam perawat, menit kamar operasi, lembar resep, hari rawat.</p>
<p>Begitu biaya dibebankan lewat pemicu itu, peta margin rumah sakit biasanya berubah. Layanan yang selama ini dianggap andalan ternyata tipis, dan layanan sederhana bervolume besar ternyata penopang. Saya pernah menuliskan contoh hitungnya dengan angka di <a href="{FA}/artikel/unit-cost-rumah-sakit-surabaya-activity-based-costing/">artikel tentang unit cost rumah sakit dengan activity based costing</a>.</p>
<h2>Kenapa sekarang</h2>
<p>Ada dua alasan. Pertama, pembayaran JKN sedang diarahkan agar lebih mengikuti kompleksitas kasus. Uji coba reformasinya sudah diumumkan di empat daerah, dan salah satunya di Jawa Timur. Selama tarif ditentukan pihak lain, satu-satunya yang bisa dikelola rumah sakit adalah biaya, dan biaya hanya bisa dikelola bila diketahui per layanan.</p>
<p>Kedua, pasien umum dan asuransi makin pandai membandingkan. Rumah sakit di Malang tidak hanya bersaing dengan tetangga satu kota, tetapi juga dengan Surabaya yang dua jam perjalanan. Menetapkan tarif paket tanpa tahu biayanya sama dengan berdagang sambil menutup mata.</p>
<h2>Mulai dari yang kecil</h2>
<p>ABC sering ditakuti karena dianggap proyek besar. Tidak harus begitu. Saran saya untuk rumah sakit daerah:</p>
<ul>
<li>Pilih satu unit dulu, misalnya kamar operasi atau rawat inap kebidanan.</li>
<li>Pakai data yang sudah ada di sistem informasi rumah sakit, jangan menunggu sistem baru.</li>
<li>Cocokkan total biayanya dengan laporan keuangan. Kalau tidak cocok, cari tahu mengapa.</li>
<li>Pisahkan biaya kapasitas yang menganggur. Kamar operasi yang kosong setelah pukul dua siang adalah urusan manajemen, bukan beban pasien.</li>
</ul>
<p>Menghitung biaya memang tidak semenarik meresmikan gedung baru. Tetapi rumah sakit yang tahu biayanya bisa mengambil keputusan dengan tenang: layanan mana yang dikembangkan, tarif mana yang dinaikkan, dan kerja sama mana yang ditolak. Bagi yang ingin mencoba sendiri, contoh lembar kerjanya ada di <a href="{US}/artikel/contoh-perhitungan-activity-based-costing-rumah-sakit/">contoh perhitungan activity based costing rumah sakit</a>.</p>
''')

K(topik='abc', kota='Purwokerto', kota_slug='purwokerto', slug='tarif-operasi-sama-biayanya-tidak',
  title='Tarif Operasi Boleh Sama, Biayanya Tidak Pernah Sama',
  description='Catatan untuk rumah sakit di Purwokerto dan Banyumas Raya: kamar operasi paling jujur dihitung per menit, dan kamar yang kosong juga punya biaya.',
  keyword='biaya kamar operasi', tags=TAG_ABC, sources=[S_JKN],
  body_html=f'''
<p>Purwokerto adalah pusat rujukan Banyumas Raya. Pasien dari Cilacap, Purbalingga, Banjarnegara, sampai Kebumen datang untuk tindakan yang tidak tersedia di kotanya. Kamar operasi rumah sakit di sini sibuk, dan kesibukan itu sering dianggap bukti bahwa instalasi bedah menguntungkan.</p>
<p>Belum tentu. Kamar operasi adalah tempat paling mahal di rumah sakit, dan cara kebanyakan rumah sakit menghitung biayanya terlalu kasar untuk tempat semahal itu.</p>
<h2>Kecil, sedang, besar</h2>
<p>Cara yang lazim adalah mengelompokkan operasi menjadi kecil, sedang, besar, dan khusus, lalu memberi bobot. Praktis, tetapi dua operasi yang sama-sama disebut sedang bisa berbeda satu jam. Satu jam di kamar operasi berarti satu tim, satu set alat, satu ruangan berpendingin yang tidak bisa dipakai pasien lain.</p>
<p>Satuan yang lebih jujur adalah menit. Hitung seluruh biaya kapasitas kamar operasi sebulan: perawat bedah, penata anestesi, penyusutan alat, sterilisasi, listrik. Bagi dengan menit yang secara wajar tersedia. Hasilnya biaya per menit. Setiap tindakan lalu dibebani sebesar menit yang dipakainya, termasuk waktu menyiapkan dan membersihkan ruangan.</p>
<h2>Kamar kosong juga mahal</h2>
<p>Cara ini dikenal sebagai time-driven activity based costing. Kelebihannya bukan hanya ketelitian. Ia memperlihatkan sesuatu yang tidak pernah muncul di laporan biasa: kapasitas yang menganggur.</p>
<p>Bila kamar operasi tersedia delapan jam sehari dan rata-rata terpakai lima jam, tiga jam sisanya tetap dibayar. Gaji tim tetap jalan, alat tetap menyusut. Pada cara lama, biaya tiga jam kosong itu diam-diam ikut dibagikan ke pasien yang dioperasi, sehingga biaya per operasi terlihat tinggi. Lalu ada yang mengusulkan tarif dinaikkan. Pasien berkurang, kamar makin kosong, biaya per operasi naik lagi.</p>
<p>Dengan hitungan per menit, biaya kamar kosong dipisahkan dan dilaporkan apa adanya. Pertanyaannya berubah dari berapa tarif yang pantas menjadi mengapa kamar kosong setelah pukul dua siang.</p>
<h2>Jawabannya jarang soal uang</h2>
<p>Dari yang saya lihat, penyebabnya hampir selalu soal jadwal. Operasi elektif menumpuk pagi karena dokter praktik di tempat lain sore harinya. Pergantian pasien memakan waktu karena ruang pemulihan penuh. Alat tertentu hanya satu sehingga dua operasi tidak bisa berjalan bersamaan.</p>
<p>Semua itu masalah manajemen yang bisa dirundingkan, asal angkanya ada di meja. Tanpa angka, rapat instalasi bedah hanya menjadi adu perasaan antara dokter, perawat, dan bagian keuangan.</p>
<h2>Syaratnya satu: catat jamnya</h2>
<p>Metode ini tidak membutuhkan perangkat mahal. Ia hanya membutuhkan disiplin mencatat empat waktu: pasien masuk kamar, sayatan dimulai, luka ditutup, pasien keluar kamar. Banyak rumah sakit sudah punya kolomnya di laporan operasi, tetapi diisi seadanya.</p>
<p>Kalau ada satu hal yang bisa dimulai besok pagi oleh rumah sakit di Purwokerto dan sekitarnya, itu dia. Tiga bulan catatan waktu yang rapi sudah cukup untuk menghitung biaya per menit dan melihat berapa jam kamar operasi sebenarnya menganggur. Uraian teknis dan contoh angkanya saya tulis di <a href="{FA}/artikel/time-driven-abc-kamar-operasi-rumah-sakit-semarang/">artikel tentang time-driven ABC untuk kamar operasi</a>.</p>
''')

K(topik='abc', kota='Jember', kota_slug='jember', slug='unit-cost-bukan-tugas-bagian-keuangan-saja',
  title='Unit Cost Bukan Tugas Bagian Keuangan Saja',
  description='Catatan untuk rumah sakit di Jember dan tapal kuda: perhitungan unit cost gagal bukan karena rumus, tetapi karena dikerjakan sendirian oleh bagian keuangan.',
  keyword='unit cost rumah sakit', tags=TAG_ABC, sources=[],
  body_html=f'''
<p>Jember adalah pusat layanan kesehatan kawasan tapal kuda. Rumah sakit di sini menerima rujukan dari Bondowoso, Situbondo, Lumajang, dan Banyuwangi. Ada cerita yang berulang di rumah sakit daerah seperti ini: perhitungan unit cost sudah pernah dibuat, bahkan dengan bantuan konsultan, lalu berakhir sebagai dokumen tebal di lemari direktur.</p>
<p>Rumusnya tidak salah. Yang keliru adalah anggapan bahwa unit cost urusan bagian keuangan.</p>
<h2>Keuangan tahu angkanya, bukan ceritanya</h2>
<p>Bagian keuangan tahu berapa gaji perawat, berapa tagihan listrik, berapa penyusutan alat. Yang tidak mereka tahu adalah bagaimana semua itu dipakai. Berapa menit perawat mendampingi pasien pascabedah dibanding pasien observasi? Berapa kali satu set instrumen disterilkan dalam sehari? Pemeriksaan laboratorium mana yang sekali jalan bisa memproses seratus sampel dan mana yang hanya lima?</p>
<p>Jawaban atas pertanyaan itu ada di kepala kepala ruang, kepala instalasi, dan dokter. Tanpa mereka, bagian keuangan terpaksa membagi biaya dengan kunci yang paling mudah, yaitu jumlah pasien. Hasilnya angka yang rapi dan tidak dipercaya siapa pun.</p>
<h2>Kenapa klinisi enggan ikut</h2>
<p>Ada tiga alasan yang sering muncul. Pertama, takut hasilnya dipakai untuk memotong jasa. Kedua, merasa itu bukan pekerjaan klinis. Ketiga, pernah diminta mengisi formulir panjang lalu tidak pernah melihat hasilnya.</p>
<p>Ketiganya wajar, dan ketiganya bisa dijawab oleh direksi sejak awal: untuk apa angka ini akan dipakai, siapa yang akan melihatnya, dan kapan hasilnya dipaparkan kembali ke unit.</p>
<h2>Bahasa yang sama</h2>
<p>Activity based costing sebenarnya lebih dekat dengan cara berpikir klinisi daripada cara berpikir akuntan. Ia bertanya: untuk satu pasien dengan diagnosis ini, aktivitas apa saja yang dilakukan? Itu pertanyaan clinical pathway. Bedanya, setiap aktivitas diberi harga.</p>
<p>Ketika dokter melihat bahwa memperpendek lama rawat satu hari atau mengganti satu jenis bahan menurunkan biaya episode sekian ratus ribu rupiah tanpa mengurangi mutu, percakapannya berubah. Unit cost berhenti menjadi alat menghakimi dan mulai menjadi alat merancang layanan.</p>
<h2>Cara melibatkan tanpa membebani</h2>
<ul>
<li>Bentuk tim kecil lintas profesi: satu orang keuangan, satu perawat senior, satu dokter, satu orang sistem informasi.</li>
<li>Wawancara, jangan formulir. Tiga puluh menit dengan kepala ruang lebih berguna daripada kuesioner sepuluh halaman.</li>
<li>Mulai dari lima layanan yang paling banyak atau paling diperdebatkan.</li>
<li>Paparkan hasil ke unit lebih dulu sebelum ke direksi, dan beri kesempatan mengoreksi.</li>
<li>Sepakati bahwa perhitungan pertama dipakai untuk memahami, bukan untuk memberi sanksi.</li>
</ul>
<p>Rumah sakit daerah punya kelebihan yang tidak dimiliki rumah sakit besar di kota: orangnya saling kenal. Kepala keuangan bisa berjalan ke ruang bersalin dan bertanya langsung. Kelebihan itu sayang kalau tidak dipakai.</p>
<p>Bagi yang sedang menimbang apakah akan mengerjakannya sendiri atau memakai bantuan luar, saya menuliskan perbandingannya di <a href="{CA}/artikel/unit-cost-rumah-sakit-yogyakarta-tim-internal-atau-konsultan/">unit cost rumah sakit: tim internal, kampus, atau konsultan</a>.</p>
''')

# ================================================================== PE
K(topik='pe', kota='Kediri', kota_slug='kediri', slug='kalau-investor-global-mengetuk-pintu-rumah-sakit-daerah',
  title='Kalau Investor Global Mengetuk Pintu Rumah Sakit di Kediri',
  description='Dana private equity kesehatan Asia makin besar dan mulai melihat rumah sakit daerah. Catatan untuk pemilik rumah sakit di Kediri sebelum membuka pintu.',
  keyword='private equity rumah sakit', tags=TAG_PE, sources=[S_QUAD, S_VISI],
  body_html=f'''
<p>Beberapa tahun lalu, cerita investor asing membeli rumah sakit hanya terdengar di Jakarta. Sekarang ceritanya bergeser. Pada 2025 sebuah dana private equity yang khusus berinvestasi di sektor kesehatan Asia menutup penggalangan dananya di atas satu miliar dolar AS. Pada 2026 jaringan rumah sakit jantung yang berbasis di Cirebon, bukan di ibu kota, diumumkan akan diambil alih sebuah emiten senilai ratusan miliar rupiah.</p>
<p>Kediri, pusat perdagangan Jawa Timur bagian barat, punya rumah sakit swasta yang melayani pasien dari Tulungagung, Blitar, Nganjuk, dan Trenggalek. Cepat atau lambat, salah satu pemiliknya akan menerima telepon dari seseorang yang memperkenalkan diri sebagai perwakilan investor. Apa yang sebaiknya dipikirkan sebelum menjawab?</p>
<h2>Mereka membeli masa depan, membayar dengan masa lalu</h2>
<p>Investor tertarik pada potensi: penduduk yang bertambah, kelas menengah yang mau membayar, layanan spesialis yang belum ada. Tetapi harga yang mereka tawarkan dihitung dari kinerja yang sudah terbukti, biasanya laba sebelum bunga, pajak, dan penyusutan, dikalikan sebuah angka.</p>
<p>Artinya, setiap rupiah laba yang tidak tercatat rapi mengurangi harga berkali lipat. Rumah sakit keluarga sering menanggung biaya pribadi pemilik, menyewa tanah dari keluarga tanpa kontrak, dan mengakui klaim yang belum tentu dibayar. Semua itu akan dibongkar saat uji tuntas.</p>
<h2>Uang masuk ke mana</h2>
<p>Pertanyaan yang jarang diajukan pemilik pada pertemuan pertama: dana ini masuk ke perusahaan atau ke saya? Keduanya sah, tetapi akibatnya berbeda. Dana yang masuk ke perusahaan dipakai membangun, dan pemilik lama terdilusi tanpa menerima uang. Dana yang membeli saham lama diterima pemilik, tetapi rumah sakit tidak bertambah kuat.</p>
<p>Kebanyakan transaksi menggabungkan keduanya. Mengetahui porsinya sejak awal menghindarkan salah paham di dalam keluarga.</p>
<h2>Harga hanya separuh perjanjian</h2>
<p>Separuh lainnya adalah hak. Investor institusi hampir selalu meminta kursi di dewan, hak menyetujui anggaran dan belanja besar, hak ikut menjual, dan jalan keluar setelah lima sampai tujuh tahun. Sebagian meminta jaminan imbal hasil minimum, yang pada praktiknya membuat dana mereka lebih mirip utang daripada modal.</p>
<p>Tidak ada yang salah dengan itu, selama pemilik paham apa yang ditandatangani. Yang berbahaya adalah menilai tawaran hanya dari angka valuasi di halaman pertama.</p>
<h2>Pekerjaan rumah sebelum membuka pintu</h2>
<ul>
<li>Laporan keuangan diaudit minimal dua tahun.</li>
<li>Laba rugi per layanan, supaya tahu apa yang sebenarnya dijual.</li>
<li>Tanah, bangunan, dan izin atas nama badan usaha rumah sakit.</li>
<li>Kontrak tertulis dengan dokter spesialis andalan.</li>
<li>Kesepakatan keluarga: siapa yang mau menjual, siapa yang mau bertahan.</li>
</ul>
<p>Butir terakhir paling sering dilupakan dan paling sering menggagalkan transaksi.</p>
<p>Saya tidak sedang menganjurkan pemilik rumah sakit daerah untuk menjual. Banyak rumah sakit keluarga lebih baik tumbuh pelan dengan dana bank. Tetapi menolak tawaran dengan paham jauh lebih baik daripada menerimanya dengan ragu. Bagi yang ingin melihat cara investor menghitung nilai rumah sakit, saya menuliskannya di <a href="{FA}/artikel/private-equity-global-rumah-sakit-jakarta-valuasi-term-sheet/">artikel tentang valuasi dan term sheet private equity untuk rumah sakit</a>.</p>
''')

K(topik='pe', kota='Tasikmalaya', kota_slug='tasikmalaya', slug='rumah-sakit-keluarga-dan-godaan-dana-private-equity',
  title='Rumah Sakit Keluarga dan Godaan Dana Private Equity',
  description='Rumah sakit keluarga di Tasikmalaya dan Priangan timur butuh dana untuk bertahan di tengah perubahan aturan. Bank, investor, atau keduanya? Sebuah timbangan.',
  keyword='pendanaan rumah sakit keluarga', tags=TAG_PE, sources=[S_JKN],
  body_html=f'''
<p>Di Tasikmalaya dan kota-kota Priangan timur, banyak rumah sakit lahir dari praktik seorang dokter. Ruang praktik menjadi klinik bersalin, klinik menjadi rumah sakit, lalu anak-anaknya yang juga dokter melanjutkan. Rumah sakit seperti ini punya sesuatu yang tidak dimiliki jaringan besar: nama keluarga yang dipercaya tiga generasi pasien.</p>
<p>Yang sering tidak mereka miliki adalah dana. Aturan baru menuntut penyesuaian ruang rawat inap, layanan harus dipetakan menurut kemampuan, alat harus diperbarui, dan pesaing bermodal besar membuka cabang di kota yang sama. Di titik itu, tawaran dana private equity terdengar seperti jawaban.</p>
<h2>Utang dan modal bukan sekadar soal bunga</h2>
<p>Pinjaman bank harus dikembalikan dengan bunga, apa pun yang terjadi. Sebagai gantinya, bank tidak ikut memiliki dan tidak ikut mengatur selama angsuran lancar. Modal dari investor tidak perlu dikembalikan, tetapi investor ikut memiliki, ikut mengatur, dan suatu hari ingin keluar dengan untung.</p>
<p>Bagi keluarga yang ingin mewariskan rumah sakit, perbedaan itu lebih penting daripada selisih biaya dana. Utang yang lunas mengembalikan rumah sakit seutuhnya kepada keluarga. Saham yang sudah dilepas hampir tidak pernah kembali.</p>
<h2>Kapan modal investor masuk akal</h2>
<ul>
<li>Rencana ekspansinya terlalu besar untuk ditanggung utang, misalnya membangun gedung baru atau membuka rumah sakit kedua.</li>
<li>Keluarga memang ingin mengurangi kepemilikan, karena generasi berikutnya tidak semuanya ingin mengelola.</li>
<li>Rumah sakit butuh lebih dari uang: sistem, jejaring dokter, dan disiplin manajemen yang dibawa investor.</li>
</ul>
<h2>Kapan sebaiknya ditahan</h2>
<ul>
<li>Kebutuhannya hanya menambah alat atau merenovasi ruangan. Itu wilayah kredit investasi.</li>
<li>Laporan keuangan belum rapi. Investor akan menawar rendah, dan keluarga tidak punya angka untuk membantah.</li>
<li>Keluarga belum sepakat. Investor yang masuk di tengah perselisihan memperbesar perselisihan.</li>
</ul>
<h2>Jalan tengah yang jarang dibicarakan</h2>
<p>Pilihannya tidak harus hitam putih. Ada beberapa bentuk yang lebih lunak: investor masuk hanya di rumah sakit baru sementara rumah sakit induk tetap milik keluarga, kerja sama operasi untuk satu layanan unggulan, atau pemisahan properti dari operasional sehingga investor memiliki gedung dan keluarga memiliki rumah sakitnya.</p>
<p>Setiap bentuk punya akibat akuntansi, pajak, dan hukum sendiri, dan di situlah penasihat yang berdiri di sisi pemilik dibutuhkan. Bukan untuk memutuskan, tetapi untuk memastikan setiap pilihan sudah dihitung.</p>
<p>Saya percaya rumah sakit keluarga di daerah adalah aset bagi kotanya. Mereka mengenal pasiennya dan bertahan ketika yang lain pergi. Karena itu keputusan mengundang pemilik baru layak diambil pelan-pelan, dengan angka di tangan. Timbangan yang lebih teknis antara dua sumber dana itu ada di <a href="{FA}/artikel/private-equity-vs-utang-bank/">private equity vs utang bank</a>, dan gambaran pendanaan untuk rumah sakit di wilayah ini saya rangkum di halaman <a href="{FA}/pendanaan-rumah-sakit/tasikmalaya/">pendanaan rumah sakit Tasikmalaya</a>.</p>
''')

K(topik='pe', kota='Bandar Lampung', kota_slug='bandar-lampung', slug='dua-juta-orang-berobat-ke-luar-negeri-rumah-sakit-daerah-dapat-apa',
  title='Dua Juta Orang Berobat ke Luar Negeri, Rumah Sakit Daerah Dapat Apa?',
  description='Pemerintah membangun kawasan khusus kesehatan untuk menahan devisa. Bagi rumah sakit di Bandar Lampung, peluangnya lain: menahan pasien di kotanya.',
  keyword='rumah sakit daerah investasi kesehatan', tags=TAG_PE, sources=[S_KEK],
  body_html=f'''
<p>Pemerintah memperkirakan sekitar dua juta warga Indonesia berobat ke luar negeri setiap tahun, dengan belanja kira-kira Rp150 triliun. Jawabannya adalah kawasan ekonomi khusus kesehatan: Sanur di Bali sudah beroperasi, Batam sedang dibangun. Rumah sakit internasional, dokter asing, alat tercanggih.</p>
<p>Saya membaca berita itu sambil memikirkan Bandar Lampung, gerbang Sumatera dari Jawa. Pasien dari sini yang mampu tidak hanya pergi ke luar negeri. Lebih banyak lagi yang menyeberang ke Jakarta. Kebocorannya berlapis: dari kabupaten ke ibu kota provinsi, dari provinsi ke Jakarta, dari Jakarta ke luar negeri.</p>
<h2>Kawasan khusus tidak menjawab lapis pertama</h2>
<p>Rumah sakit di kawasan khusus dibangun untuk menahan pasien yang tadinya terbang ke Penang atau Singapura. Itu penting, tetapi jumlah pasien yang berpindah dari kota menengah ke kota besar di dalam negeri jauh lebih banyak. Mereka pergi bukan karena ingin kemewahan. Mereka pergi karena layanan yang dibutuhkan tidak ada, antreannya panjang, atau mereka tidak yakin.</p>
<p>Di sinilah peluang rumah sakit daerah, dan di sinilah investor mulai melihat. Dana yang masuk ke sektor kesehatan Indonesia tidak semuanya membangun menara di ibu kota. Sebagian mencari rumah sakit di kota lapis kedua yang sudah punya pasien dan tinggal ditambah layanannya.</p>
<h2>Apa yang sebenarnya dicari pasien</h2>
<p>Alasan pasien pergi umumnya berulang pada tiga hal: kepastian diagnosis, kepastian biaya, dan waktu tunggu. Tidak satu pun dari ketiganya mensyaratkan gedung baru.</p>
<ul>
<li>Kepastian diagnosis datang dari dokter spesialis yang menetap dan alat penunjang yang berfungsi.</li>
<li>Kepastian biaya datang dari tarif paket yang jelas, dan itu hanya bisa dibuat bila rumah sakit tahu biayanya sendiri.</li>
<li>Waktu tunggu datang dari jadwal dan kapasitas yang dikelola.</li>
</ul>
<h2>Di mana dana dibutuhkan</h2>
<p>Dana tetap dibutuhkan, tetapi untuk hal yang tepat: layanan jantung, kanker, atau cuci darah yang selama ini membuat pasien menyeberang. Sumbernya bisa kredit bank untuk alat, bisa investor untuk ekspansi yang lebih besar.</p>
<p>Apa pun sumbernya, pemberi dana akan bertanya hal yang sama: berapa pasien yang selama ini dirujuk keluar, berapa yang realistis ditahan, dan berapa margin layanan itu. Rumah sakit yang bisa menjawab dengan data rujukan dan perhitungan biaya akan didengar. Yang menjawab dengan keyakinan saja akan diminta kembali lain waktu.</p>
<h2>Urutan yang masuk akal</h2>
<ol>
<li>Petakan pasien yang dirujuk keluar setahun terakhir menurut diagnosis.</li>
<li>Pilih satu dua layanan yang volumenya paling besar dan paling mungkin ditangani sendiri.</li>
<li>Hitung kebutuhan dokter, alat, dan ruang, lalu biaya per layanan.</li>
<li>Rapikan laporan keuangan dan audit.</li>
<li>Baru bicara dengan bank atau investor.</li>
</ol>
<p>Kawasan khusus akan menahan sebagian devisa. Tetapi menahan pasien di kotanya sendiri, itu pekerjaan rumah sakit daerah, dan nilainya bagi keluarga pasien jauh lebih besar daripada angka devisa. Gambaran pilihan pendanaannya saya tulis di halaman <a href="{FA}/pendanaan-rumah-sakit/bandar-lampung/">pendanaan rumah sakit di Bandar Lampung</a>.</p>
''')

# ================================================================== CFO
K(topik='cfo', kota='Pasuruan', kota_slug='pasuruan', slug='pabrik-sudah-besar-keuangannya-masih-dipegang-admin',
  title='Pabrik Sudah Besar, Keuangannya Masih Dipegang Admin',
  description='Banyak pabrik pemasok di Pasuruan beromzet ratusan miliar tetapi fungsi keuangannya berhenti di pembukuan. Di situ peran fractional CFO mulai terasa.',
  keyword='fractional cfo', tags=TAG_CFO, sources=[],
  body_html=f'''
<p>Kawasan industri di Pasuruan menampung pabrik-pabrik besar, dan di sekelilingnya tumbuh ratusan pemasok: pembuat komponen, kemasan, jasa pengerjaan logam, angkutan. Banyak di antaranya dimulai dari bengkel dengan lima orang dan sekarang mempekerjakan ratusan. Mesinnya bertambah, pelanggannya bertambah, sertifikat mutunya lengkap.</p>
<p>Satu hal sering tertinggal: fungsi keuangannya. Yang memegang masih orang yang sama sejak awal, seorang admin kepercayaan yang rajin dan jujur, dibantu konsultan pajak yang datang sebulan sekali.</p>
<h2>Pembukuan bukan keuangan</h2>
<p>Admin yang baik mencatat setiap transaksi, mengarsipkan faktur, dan menyiapkan pembayaran. Itu pembukuan, dan itu penting. Tetapi ada pertanyaan yang tidak pernah bisa dijawab pembukuan saja.</p>
<ul>
<li>Produk mana yang sebenarnya merugi setelah harga bahan naik?</li>
<li>Berapa kas yang tersedia delapan minggu lagi, ketika tunjangan hari raya, pajak, dan angsuran jatuh bersamaan?</li>
<li>Lebih baik membeli mesin baru dengan kredit atau menyewa?</li>
<li>Kalau pelanggan terbesar minta potongan harga tiga persen, bisakah diterima?</li>
</ul>
<p>Pertanyaan seperti itu adalah pekerjaan direktur keuangan. Di banyak pabrik menengah, pemilik menjawabnya sendiri dengan naluri. Naluri itu sering benar, sampai suatu hari tidak.</p>
<h2>Kenapa tidak merekrut saja</h2>
<p>Direktur keuangan yang berpengalaman mahal, dan pabrik dengan tim keuangan lima orang belum tentu punya pekerjaan penuh waktu untuknya. Akibatnya banyak pemilik menunda, lalu menunda lagi.</p>
<p>Di sinilah muncul pilihan yang di luar negeri sudah lazim dan di sini mulai dikenal: fractional CFO, direktur keuangan paruh waktu. Ia datang beberapa hari dalam sebulan, memimpin rapat angka, menyusun proyeksi kas, berbicara dengan bank, dan mendampingi pemilik saat keputusan besar. Sisanya dikerjakan tim yang sudah ada.</p>
<h2>Yang berubah di lapangan</h2>
<p>Dari yang saya amati, perubahan pertama hampir selalu sama. Laporan bulanan yang tadinya selesai tanggal dua puluh lima maju ke minggu pertama. Lalu muncul satu lembar proyeksi kas tiga bulan ke depan. Lalu, untuk pertama kalinya, pemilik melihat margin per pelanggan.</p>
<p>Lembar terakhir itu sering mengejutkan. Pelanggan terbesar ternyata bukan penyumbang laba terbesar, karena termin pembayarannya panjang dan permintaan potongannya rutin. Tidak ada yang berubah di pabrik, tetapi cara pemilik berunding berubah.</p>
<h2>Bukan untuk semua</h2>
<p>Saya tidak ingin terdengar seolah setiap usaha butuh ini. Bengkel yang masih kecil lebih membutuhkan pembukuan yang rapi. Perusahaan yang sudah sangat besar membutuhkan orang penuh waktu. Fractional CFO cocok di antara keduanya: usaha yang keputusannya sudah bernilai miliaran tetapi belum butuh kehadiran harian.</p>
<p>Tandanya sederhana. Bila pemilik sering berkata saya rasa, dan jarang berkata angkanya menunjukkan, mungkin sudah waktunya. Uraian yang lebih rinci tentang pekerjaan dan contoh hitungnya untuk pabrik saya tulis di <a href="{FA}/artikel/fractional-cfo-pabrik-kawasan-industri-bekasi/">artikel fractional CFO untuk pabrik</a>.</p>
''')

K(topik='cfo', kota='Tegal', kota_slug='tegal', slug='cfo-paruh-waktu-mewah-atau-perlu-untuk-pengusaha-daerah',
  title='CFO Paruh Waktu: Mewah atau Perlu untuk Pengusaha Daerah?',
  description='Pengusaha logam dan perdagangan di Tegal sering menganggap direktur keuangan urusan perusahaan besar. Sebuah hitungan sederhana untuk menimbangnya.',
  keyword='cfo paruh waktu', tags=TAG_CFO, sources=[],
  body_html=f'''
<p>Tegal dijuluki Jepangnya Indonesia karena industri logamnya. Dari bengkel-bengkel di sana keluar komponen kapal, suku cadang, sampai alat pertanian. Pengusahanya ulet dan hemat. Ketika istilah direktur keuangan paruh waktu disebut kepada pengusaha di pantura, tanggapan yang lazim terdengar jujur: itu untuk perusahaan besar di Jakarta, kami cukup pakai tukang pajak.</p>
<p>Tanggapan itu masuk akal. Tetapi mari kita hitung.</p>
<h2>Menghitung yang tidak terlihat</h2>
<p>Ambil usaha dengan penjualan Rp40 miliar setahun. Persediaan bahan dan barang jadi menumpuk tiga bulan, pelanggan membayar dua bulan setelah kirim, pemasok minta dibayar sebulan. Tanpa perlu rumus rumit, ada kira-kira empat bulan penjualan yang tertahan sebagai stok dan piutang, sebagian dibiayai pinjaman bank.</p>
<p>Kalau stok bisa dirampingkan dua minggu dan penagihan dipercepat dua minggu, uang yang kembali ke rekening lebih dari Rp2 miliar. Bunga yang dihemat setahun bisa ratusan juta rupiah. Tidak ada mesin baru, tidak ada pelanggan baru. Hanya ada seseorang yang memperhatikan angka yang selama ini tidak diperhatikan.</p>
<p>Itu satu contoh. Contoh lain: harga jual yang belum dinaikkan sejak upah naik, denda pajak karena laporan tidak cocok, kredit yang bunganya lebih tinggi dari seharusnya karena laporan keuangan tidak meyakinkan.</p>
<h2>Lalu kenapa belum banyak yang memakai</h2>
<p>Pertama, karena manfaatnya tidak terlihat sampai ada yang menghitungnya. Kerugian karena keputusan yang kurang tepat tidak pernah muncul sebagai tagihan.</p>
<p>Kedua, soal percaya. Membuka angka perusahaan kepada orang luar bukan hal ringan bagi usaha keluarga. Karena itu hubungan seperti ini biasanya dimulai dari pekerjaan kecil, misalnya menyiapkan pengajuan kredit, lalu berlanjut setelah kedua pihak saling kenal.</p>
<p>Ketiga, tidak semua yang menawarkan diri memang berpengalaman menjadi direktur keuangan. Ada beda antara orang yang pandai menyusun laporan dan orang yang pernah harus memutuskan dengan laporan itu.</p>
<h2>Cara menimbangnya</h2>
<ul>
<li>Tulis tiga keputusan keuangan terbesar yang akan Anda ambil tahun depan.</li>
<li>Taksir nilai rupiah setiap keputusan.</li>
<li>Tanyakan pada diri sendiri: apakah saya punya angka yang cukup untuk memutuskannya?</li>
</ul>
<p>Bila nilai keputusannya miliaran dan jawabannya tidak, biaya seorang pendamping keuangan paruh waktu menjadi kecil. Bila keputusannya masih seputar menambah satu mesin bubut, kemungkinan besar belum perlu.</p>
<h2>Mewah atau perlu</h2>
<p>Jawaban saya: bukan keduanya. Ia alat, seperti mesin. Mesin yang tepat untuk pekerjaan yang tepat menghasilkan lebih dari harganya. Mesin yang salah hanya memakan tempat.</p>
<p>Pengusaha daerah terbiasa menghitung dengan teliti sebelum membeli mesin. Cara menghitung yang sama layak dipakai untuk fungsi keuangan. Bagi yang ingin melihat perbandingan biayanya dengan merekrut penuh waktu, ada hitungan sederhananya di <a href="{CA}/artikel/biaya-fractional-cfo-pekanbaru-cara-menghitung-manfaat/">artikel tentang biaya fractional CFO dan cara menghitung manfaatnya</a>.</p>
''')

K(topik='cfo', kota='Kudus', kota_slug='kudus', slug='bank-menolak-bukan-karena-usahanya-jelek',
  title='Bank Menolak Bukan karena Usahanya Jelek',
  description='Usaha keluarga yang sehat di Kudus bisa ditolak bank karena cara menyajikan angkanya. Catatan tentang jarak antara usaha yang bagus dan laporan yang terbaca.',
  keyword='kredit bank ditolak laporan keuangan', tags=TAG_CFO, sources=[],
  body_html=f'''
<p>Kudus adalah kota industri dengan usaha keluarga yang besar-besar. Di balik nama-nama yang dikenal semua orang, ada ratusan usaha menengah di percetakan, konveksi, makanan, dan perdagangan yang sudah berjalan puluhan tahun. Usahanya nyata, pelanggannya setia, pemiliknya berhati-hati.</p>
<p>Justru karena itu, penolakan kredit terasa menyakitkan. Pertanyaan yang sering terdengar dari pemilik usaha kira-kira begini: usaha saya tidak pernah menunggak sehari pun, kenapa ditolak?</p>
<h2>Bank tidak melihat usaha, bank membaca laporan</h2>
<p>Analis kredit tidak pernah berdiri di gudang Anda pada jam sibuk. Yang sampai ke mejanya adalah berkas: laporan keuangan, rekening koran, daftar agunan. Dari berkas itu ia harus menyimpulkan dua hal, yaitu apakah usaha ini mampu membayar dan apakah angkanya bisa dipercaya.</p>
<p>Usaha yang bagus dengan laporan yang buruk, di mata analis, sama dengan usaha yang tidak jelas. Bukan karena ia curiga, tetapi karena ia tidak punya cara lain untuk mengetahuinya.</p>
<h2>Tiga hal yang paling sering menjatuhkan</h2>
<p><b>Angka yang tidak saling cocok.</b> Penjualan di laporan keuangan berbeda dengan penjualan di laporan pajak, dan keduanya berbeda dengan mutasi rekening. Masing-masing mungkin punya penjelasan, tetapi analis hanya melihat tiga angka untuk satu hal.</p>
<p><b>Uang usaha dan uang keluarga bercampur.</b> Pengeluaran rumah tangga keluar dari rekening usaha, setoran pribadi masuk sebagai penjualan. Laba yang tercatat menjadi tidak bisa dibaca.</p>
<p><b>Tidak ada cerita arus kas.</b> Pemohon menyebut jumlah pinjaman tetapi tidak bisa menunjukkan dari mana angsurannya dibayar bulan demi bulan.</p>
<h2>Yang bisa dibenahi dalam tiga bulan</h2>
<ul>
<li>Pisahkan rekening usaha dan rekening pribadi mulai bulan ini.</li>
<li>Susun laporan keuangan dua tahun terakhir dengan standar yang berlaku, dan cocokkan dengan laporan pajak serta rekening koran.</li>
<li>Buat proyeksi arus kas sederhana yang memuat angsuran pinjaman yang diminta.</li>
<li>Hitung sendiri rasio yang akan dihitung bank, terutama kemampuan membayar angsuran dari kas usaha.</li>
<li>Siapkan penjelasan tertulis untuk hal yang tidak biasa: penjualan musiman, pelanggan besar, utang ke keluarga.</li>
</ul>
<h2>Di sini peran pendamping keuangan</h2>
<p>Pekerjaan di atas bisa dikerjakan sendiri oleh pemilik yang telaten. Sebagian memakai kantor jasa akuntan untuk laporannya. Untuk usaha yang lebih besar, ada peran yang makin dikenal: direktur keuangan paruh waktu, yang memastikan laporan, pajak, dan cerita ke bank menjadi satu suara, lalu ikut duduk saat bank bertanya.</p>
<p>Saya sering berpikir, banyak usaha keluarga di daerah sebenarnya lebih sehat daripada perusahaan yang laporannya mengilap. Mereka hanya belum terbiasa bercerita dengan bahasa angka. Bahasa itu bisa dipelajari, dan hasilnya bukan hanya kredit yang disetujui, tetapi pemilik yang lebih paham usahanya sendiri.</p>
<p>Daftar rasio yang biasa dilihat analis saya uraikan di <a href="{FA}/artikel/rasio-keuangan-yang-dilihat-bank/">rasio keuangan yang dilihat bank</a>, dan bagi pelaku usaha di Kudus dan sekitarnya ada rangkuman layanan di <a href="{FA}/wilayah/kudus/">halaman FA Indonesia untuk Kudus</a>.</p>
''')

K(topik='cfo', kota='Banjarmasin', kota_slug='banjarmasin', slug='yang-dikerjakan-fractional-cfo-di-bulan-pertama',
  title='Yang Dikerjakan Fractional CFO di Bulan Pertama',
  description='Empat minggu pertama seorang fractional CFO di perusahaan perdagangan dan angkutan di Banjarmasin: membaca, memetakan kas, menata jadwal, lalu melapor.',
  keyword='fractional cfo bulan pertama', tags=TAG_CFO, sources=[],
  body_html=f'''
<p>Banjarmasin adalah kota dagang dan pelabuhan. Usaha di sini bergerak di perdagangan bahan bangunan, distribusi, angkutan sungai dan laut, serta jasa penunjang tambang. Pemilik usaha yang tertarik pada gagasan direktur keuangan paruh waktu biasanya bertanya hal yang sama: sebenarnya apa yang dia kerjakan? Jangan-jangan hanya rapat.</p>
<p>Pertanyaan yang adil. Berikut gambaran empat minggu pertama, seperti yang lazim dijalankan.</p>
<h2>Minggu pertama: membaca</h2>
<p>Belum ada saran apa pun. Yang dibaca: laporan keuangan dua sampai tiga tahun, laporan pajak, rekening koran enam bulan, semua perjanjian kredit dan sewa pembiayaan, daftar piutang dan utang, serta kontrak dengan pelanggan dan pemasok utama.</p>
<p>Lalu berbicara dengan orang-orangnya. Staf keuangan, kepala gudang, kepala penjualan. Pertanyaannya sederhana: bagaimana pesanan menjadi tagihan, dan tagihan menjadi uang.</p>
<h2>Minggu kedua: memetakan kas</h2>
<p>Hasil pertama yang bisa dipegang pemilik adalah proyeksi kas tiga belas minggu. Isinya penerimaan dari pelanggan per minggu, pembayaran ke pemasok, gaji, pajak, angsuran. Dari situ terlihat minggu mana kas akan ketat.</p>
<p>Untuk usaha angkutan dan perdagangan di Kalimantan Selatan, pola yang sering muncul: tagihan ke perusahaan tambang cair enam puluh sampai sembilan puluh hari, sedangkan solar, gaji awak, dan angsuran armada tidak bisa menunggu. Proyeksi membuat jarak itu terlihat dalam rupiah.</p>
<h2>Minggu ketiga: menata jadwal</h2>
<p>Sebagian besar masalah keuangan usaha menengah adalah masalah jadwal. Maka yang ditata:</p>
<ul>
<li>Kalender tutup buku, supaya laporan bulanan terbit paling lambat minggu kedua.</li>
<li>Jadwal penagihan, siapa menagih siapa dan kapan.</li>
<li>Jadwal pembayaran, supaya pemilik tidak perlu memutuskan satu per satu setiap hari.</li>
<li>Daftar syarat dari bank yang harus dipantau tiap bulan.</li>
</ul>
<h2>Minggu keempat: melapor dan mengurutkan</h2>
<p>Bulan pertama ditutup dengan satu pertemuan bersama pemilik. Bahannya ringkas: posisi kas dan proyeksinya, tiga sampai lima temuan terpenting beserta nilai rupiahnya, dan urutan perbaikan untuk tiga bulan berikutnya.</p>
<p>Temuan yang baik berbentuk seperti ini: piutang di atas sembilan puluh hari sekian miliar, dan separuhnya dari dua pelanggan. Bukan: manajemen piutang perlu ditingkatkan. Yang pertama bisa ditindaklanjuti besok pagi. Yang kedua hanya menambah tebal laporan.</p>
<h2>Yang tidak dikerjakan</h2>
<p>Ia tidak menggantikan staf pembukuan, tidak mengisi laporan pajak, dan tidak mengaudit. Ia juga tidak mengambil keputusan menggantikan pemilik. Tugasnya memastikan pemilik memutuskan dengan angka yang benar dan pada waktunya.</p>
<p>Kalau setelah bulan pertama pemilik belum memegang proyeksi kas dan daftar temuan bernilai rupiah, ada yang keliru, entah pada orangnya atau pada kesepakatannya. Untuk itu sejak awal sebaiknya ada ruang lingkup tertulis. Hal-hal yang perlu ada di dalamnya saya tulis di <a href="{CA}/artikel/memilih-fractional-cfo-makassar-kredensial-kontrak/">panduan memilih fractional CFO</a>, dan contoh format laporannya ada di <a href="{US}/artikel/paket-laporan-manajemen-bulanan-proyeksi-kas-13-minggu/">paket laporan manajemen dan proyeksi kas 13 minggu</a>.</p>
''')
