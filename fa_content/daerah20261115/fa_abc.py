# -*- coding: utf-8 -*-
"""FA Indonesia: 3 artikel Unit Cost Activity Based Costing (Surabaya, Semarang, Makassar). Sudut: diagnosis dan pendampingan."""
from _k import A, n, rp, jt, pct, tbl

SRC_JKN = [
    ('Permenkes Nomor 3 Tahun 2023 tentang Standar Tarif Pelayanan Kesehatan dalam Penyelenggaraan Program JKN', 'https://peraturan.bpk.go.id/Details/275518'),
    ('ANTARA: Kemenkes Uji Coba Reformasi JKN di Muara Enim (Oktober 2026)', 'https://www.antaranews.com/berita/5771342/kemenkes-uji-coba-reformasi-jkn-di-muara-enim-pangkas-waktu-tunggu'),
]

# ------------------------------------------------------------------ 1. Surabaya
POOL = [  # aktivitas, biaya/bulan, pemicu, volume pemicu
    ('Admisi, verifikasi penjaminan, dan billing', 180e6, 'episode perawatan', 1200),
    ('Asuhan keperawatan rawat inap', 900e6, 'jam perawat', 18000),
    ('Kamar operasi: tim, alat, dan sterilisasi', 720e6, 'menit kamar operasi', 24000),
    ('Farmasi klinis dan penyiapan obat', 150e6, 'lembar resep', 15000),
    ('Gizi, linen, dan kebersihan ruang', 240e6, 'hari rawat', 3000),
]
RATE = [c / v for _, c, _, v in POOL]
TOT = sum(c for _, c, _, _ in POOL)
OBJ = [  # layanan, (episode, jam perawat, menit OK, resep, hari rawat), biaya langsung, tarif
    ('Persalinan normal', (1, 14, 0, 6, 2), 2.4e6, 4.5e6),
    ('Sectio caesarea', (1, 22, 75, 10, 3), 5.5e6, 9.0e6),
    ('Apendektomi laparoskopi', (1, 16, 90, 8, 2), 7.2e6, 10.5e6),
]
TRAD = TOT / 3000   # tarif tunggal per hari rawat
rows_abc, rows_m = [], []
for nm, use, direct, tarif in OBJ:
    oh_abc = sum(u * r for u, r in zip(use, RATE)); oh_tr = use[4] * TRAD
    rows_abc.append([nm, rp(oh_tr), rp(oh_abc), ('+' if oh_tr > oh_abc else '') + pct(oh_tr / oh_abc - 1, 0)])
    rows_m.append([nm, rp(tarif), rp(direct + oh_tr), rp(tarif - direct - oh_tr), rp(direct + oh_abc), rp(tarif - direct - oh_abc)])
sc_abc = sum(u * r for u, r in zip(OBJ[1][1], RATE))

A(site='fa', topik='abc', kota='Surabaya', kota_slug='surabaya',
  slug='unit-cost-rumah-sakit-surabaya-activity-based-costing',
  seo_title='Unit Cost Rumah Sakit Surabaya dengan Activity Based Costing',
  title='Unit Cost Rumah Sakit di Surabaya: Activity Based Costing dari Pool Biaya sampai Tarif',
  description='Cara menyusun unit cost rumah sakit di Surabaya dengan activity based costing: pool biaya, pemicu, contoh hitung per layanan, dan dampaknya ke tarif.',
  keyword='unit cost rumah sakit surabaya', category='Rumah Sakit',
  cta={'href': '/konsultan-unit-cost-rumah-sakit/surabaya/', 'label': 'Konsultan Unit Cost Rumah Sakit Surabaya'},
  wa='Halo Pak Ananta, saya ingin diskusi unit cost activity based costing untuk rumah sakit kami di Surabaya.',
  related=['cara-menghitung-unit-cost-rumah-sakit', 'unit-cost-vs-tarif-ina-cbgs-rumah-sakit-swasta', 'manajemen-biaya-rumah-sakit-berbasis-produk', 'titik-impas-rumah-sakit-per-dpjp'],
  sources=SRC_JKN + [('DDTCNews: Devisa Rp170 Triliun Hilang karena WNI Berobat ke Luar Negeri (14 Juni 2023)', 'https://news.ddtc.co.id/berita/nasional/1795060/jokowi-devisa-rp-170-triliun-hilang-karena-wni-berobat-ke-luar-negeri')],
  body_html=f'''
<p>Rumah sakit swasta di Surabaya bersaing di dua pasar sekaligus. Di pasar JKN, tarif ditetapkan pemerintah lewat Permenkes 3 Tahun 2023 dan rumah sakit hanya bisa mengatur biaya. Di pasar pasien umum dan asuransi, rumah sakit bersaing dengan sesama rumah sakit di Surabaya Raya dan dengan rumah sakit di luar negeri. Pada 2023 Presiden menyebut sekitar 15 persen warga yang berobat ke luar negeri berasal dari Surabaya.</p>
<p>Di kedua pasar itu pertanyaan direksi sama: berapa biaya sebenarnya satu layanan? Metode distribusi ganda menjawabnya di tingkat unit. Activity based costing (ABC) menjawabnya di tingkat layanan, dan di tingkat itulah keputusan tarif dibuat.</p>
<h2>Kapan Distribusi Ganda Tidak Lagi Cukup</h2>
<p>Distribusi ganda memindahkan biaya unit penunjang ke unit produksi, lalu membaginya rata dengan satu dasar, biasanya hari rawat atau jumlah tindakan. Hasilnya wajar selama layanan di satu unit seragam. Begitu satu bangsal merawat pasien persalinan normal dan pasien pascabedah sekaligus, rata-rata itu mulai menyesatkan.</p>
<p>Tiga tanda rumah sakit Anda sudah perlu ABC:</p>
<ul>
<li>Bauran layanan melebar: ada layanan padat tindakan (bedah, kateterisasi, kemoterapi) di samping layanan padat perawatan.</li>
<li>Biaya tidak langsung sudah melewati sepertiga total biaya, sehingga cara membaginya menentukan hasil.</li>
<li>Negosiasi dengan asuransi dan perusahaan meminta rincian biaya per paket, bukan per hari rawat.</li>
</ul>
<h2>Lima Langkah Menyusun Activity Based Costing di Rumah Sakit</h2>
<ol>
<li><b>Susun kamus aktivitas.</b> Cukup 15 sampai 30 aktivitas utama, bukan ratusan. Contoh: admisi dan penjaminan, asuhan keperawatan, kamar operasi, farmasi klinis, gizi dan linen.</li>
<li><b>Bebankan sumber daya ke aktivitas.</b> Gaji, penyusutan, listrik, dan bahan dipetakan ke aktivitas dengan pemicu sumber daya: proporsi waktu pegawai, luas ruang, daya terpasang alat.</li>
<li><b>Tetapkan pemicu aktivitas.</b> Satu aktivitas, satu pemicu yang datanya memang tersedia di SIMRS: episode, jam perawat, menit kamar operasi, lembar resep, hari rawat.</li>
<li><b>Hitung tarif aktivitas.</b> Biaya pool dibagi volume pemicu.</li>
<li><b>Bebankan ke layanan.</b> Setiap layanan menanggung biaya sebesar aktivitas yang benar-benar dikonsumsinya, sebaiknya mengikuti clinical pathway.</li>
</ol>
<h2>Contoh Pool Biaya dan Tarif Aktivitas</h2>
<p>Ilustrasi berikut memakai angka contoh untuk rumah sakit 120 tempat tidur, satu bulan. Total biaya tidak langsung {jt(TOT)} sudah dibebankan ke lima aktivitas.</p>
{tbl(['Aktivitas', 'Biaya per bulan', 'Pemicu aktivitas', 'Volume pemicu', 'Tarif aktivitas'],
     [[a, jt(c), p, n(v), rp(c / v)] for a, c, p, v in POOL], ['Jumlah', jt(TOT), '', '', ''])}
<p>Dengan cara lama, seluruh {jt(TOT)} dibagi 3.000 hari rawat sehingga setiap hari rawat menanggung {rp(TRAD)}, apa pun layanannya.</p>
<h2>Unit Cost per Layanan: Cara Lama vs ABC</h2>
<p>Tiga layanan dibandingkan. Sectio caesarea, misalnya, memakai 22 jam perawat, 75 menit kamar operasi, 10 lembar resep, dan 3 hari rawat, sehingga biaya tidak langsungnya menurut ABC {rp(sc_abc)}.</p>
{tbl(['Layanan', 'Biaya tidak langsung, cara lama', 'Biaya tidak langsung, ABC', 'Selisih cara lama terhadap ABC'], rows_abc)}
<p>Cara lama membebani persalinan normal terlalu tinggi dan dua layanan bedah terlalu rendah. Polanya selalu sama: layanan sederhana bervolume besar menyubsidi layanan kompleks di atas kertas, lalu manajemen mengambil keputusan dari angka yang keliru.</p>
<h2>Dari Unit Cost ke Keputusan Tarif</h2>
<p>Setelah biaya langsung (obat, bahan medis habis pakai, jasa medis) ditambahkan, margin per layanan terlihat berbeda sekali antara dua metode. Tarif di tabel adalah tarif contoh untuk pasien umum.</p>
{tbl(['Layanan', 'Tarif contoh', 'Unit cost cara lama', 'Margin cara lama', 'Unit cost ABC', 'Margin ABC'], rows_m)}
<div class="pf-fold"><p>Menurut cara lama, dua layanan bedah adalah penyumbang margin terbesar dan persalinan normal yang paling tipis. Menurut ABC, urutannya berbalik: margin kedua layanan bedah menjadi negatif, sedangkan persalinan normal ternyata penyumbang margin yang sehat. Rumah sakit yang memakai angka cara lama cenderung memberi diskon paket bedah ke asuransi dan menaikkan tarif persalinan, dua keputusan yang sama-sama merugikan.</p>
<p>Untuk pasien JKN, tarif tidak bisa diubah. Yang bisa dikelola adalah sisi biaya: lama rawat, pemakaian kamar operasi, formularium, dan utilisasi. Karena itu unit cost ABC sebaiknya dibaca berdampingan dengan <a href="/artikel/unit-cost-vs-tarif-ina-cbgs-rumah-sakit-swasta/">perbandingan unit cost dan tarif INA-CBG</a> per kelompok kasus.</p></div>
<h2>Kesalahan yang Paling Sering Kami Temui</h2>
<ul>
<li>Kamus aktivitas terlalu rinci sehingga datanya tidak pernah lengkap. Mulai dari yang datanya sudah ada di SIMRS.</li>
<li>Jasa medis dimasukkan ke pool biaya tidak langsung, padahal bisa ditelusuri langsung ke pasien.</li>
<li>Total biaya ABC tidak direkonsiliasi ke buku besar. Unit cost yang tidak kembali ke laporan keuangan tidak akan dipercaya bank maupun investor.</li>
<li>Perhitungan dilakukan sekali lalu disimpan. Tarif aktivitas perlu diperbarui minimal tiap semester.</li>
</ul>
<h2>Rencana Kerja 90 Hari</h2>
{tbl(['Periode', 'Pekerjaan', 'Hasil'],
     [['Hari 1 sampai 30', 'Pemetaan pusat biaya, rekonsiliasi buku besar, kamus aktivitas', 'Struktur biaya dan daftar pemicu yang disepakati direksi'],
      ['Hari 31 sampai 60', 'Pengumpulan volume pemicu dari SIMRS, perhitungan tarif aktivitas', 'Tarif aktivitas dan unit cost 20 sampai 30 layanan utama'],
      ['Hari 61 sampai 90', 'Analisis margin per layanan dan per penjamin, simulasi tarif', 'Rekomendasi tarif, paket, dan efisiensi yang siap diputuskan']])}
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Rumah sakit di Surabaya, Sidoarjo, dan Gresik didampingi tim FA Indonesia yang menggabungkan sisi keuangan dan sisi manajemen rumah sakit. Perhitungan dikerjakan dengan <a href="/kalkulator-unit-cost-rumah-sakit/">kalkulator unit cost FA Venus</a> dan kertas kerja Excel yang bisa dilanjutkan sendiri oleh tim Anda. Lihat <a href="/konsultan-unit-cost-rumah-sakit/surabaya/">konsultan unit cost rumah sakit di Surabaya</a>, <a href="/konsultan-rumah-sakit/surabaya/">konsultan rumah sakit Surabaya</a>, atau baca dulu <a href="/artikel/cara-menghitung-unit-cost-rumah-sakit/">cara menghitung unit cost dengan distribusi ganda</a>.</p>
''',
  faq=[('Apa beda activity based costing dengan distribusi ganda di rumah sakit?', 'Distribusi ganda membagi biaya penunjang ke unit produksi lalu merata-ratakannya per hari rawat atau per tindakan. Activity based costing membebankan biaya ke layanan berdasarkan aktivitas yang dikonsumsi, sehingga layanan kompleks menanggung biaya lebih besar.'),
       ('Berapa lama menyusun unit cost ABC untuk rumah sakit di Surabaya?', 'Untuk rumah sakit 100 sampai 200 tempat tidur dengan data SIMRS yang cukup rapi, umumnya 8 sampai 12 minggu sampai unit cost layanan utama dan analisis margin selesai.'),
       ('Apakah ABC wajib untuk rumah sakit?', 'Tidak ada kewajiban memakai metode tertentu. ABC dipilih ketika bauran layanan sudah beragam dan keputusan tarif atau negosiasi paket membutuhkan biaya per layanan yang lebih teliti.'),
       ('Data apa yang perlu disiapkan?', 'Buku besar 12 bulan, daftar pegawai per unit, daftar aset dan penyusutan, serta volume layanan dari SIMRS: episode, hari rawat, menit kamar operasi, dan resep.')])

# ------------------------------------------------------------------ 2. Semarang (TDABC)
CAP = [('Perawat bedah, penata anestesi, dan asisten', 460e6), ('Penyusutan dan pemeliharaan alat', 330e6),
       ('Ruang, listrik, tata udara, dan gas medis', 160e6), ('Sterilisasi instrumen dan linen', 130e6), ('Manajemen dan administrasi instalasi', 72e6)]
CAPT = sum(c for _, c in CAP)
TEOR = 4 * 25 * 8 * 60; PRAK = int(TEOR * .8); CCR = CAPT / PRAK
PRO = [('Herniotomi, anestesi regional', 45, 0, 0, 120), ('Sectio caesarea, anestesi spinal', 50, 0, 0, 150),
       ('Kolesistektomi laparoskopi, anestesi umum', 80, 20, 15, 60), ('ORIF fraktur dengan C-arm, anestesi umum', 110, 20, 15, 30)]
rows_t, used, nops = [], 0, 0
for nm, ins, ga, alat, vol in PRO:
    t = 25 + ins + ga + alat; used += t * vol; nops += vol
    rows_t.append([nm, f'25 + {ins}' + (f' + {ga}' if ga else '') + (f' + {alat}' if alat else ''), n(t), n(vol), n(t * vol), rp(t * CCR)])
IDLE = PRAK - used
AVG = CAPT / nops

A(site='fa', topik='abc', kota='Semarang', kota_slug='semarang',
  slug='time-driven-abc-kamar-operasi-rumah-sakit-semarang',
  seo_title='Time-Driven ABC Kamar Operasi Rumah Sakit di Semarang',
  title='Time-Driven ABC untuk Kamar Operasi: Membaca Biaya per Menit di Rumah Sakit Semarang',
  description='Time-driven activity based costing untuk kamar operasi rumah sakit di Semarang: biaya kapasitas per menit, persamaan waktu, dan biaya kapasitas menganggur.',
  keyword='time driven abc kamar operasi', category='Rumah Sakit',
  cta={'href': '/konsultan-unit-cost-rumah-sakit/semarang/', 'label': 'Konsultan Unit Cost Rumah Sakit Semarang'},
  wa='Halo Pak Ananta, saya ingin diskusi unit cost kamar operasi (time-driven ABC) untuk rumah sakit kami di Semarang.',
  related=['cara-menghitung-unit-cost-rumah-sakit', 'unit-cost-clinical-pathway-menghadapi-idrg', 'idrg-pengganti-ina-cbg-persiapan-rumah-sakit', 'titik-impas-rumah-sakit-per-dpjp'],
  sources=[('Kaplan dan Anderson, Time-Driven Activity-Based Costing, Harvard Business Review (November 2004)', 'https://hbr.org/2004/11/time-driven-activity-based-costing'),
           ('InfoPublik: Uji Coba Nasional Sistem Pembayaran JKN Beralih ke iDRG (27 Agustus 2025)', 'https://infopublik.id/kategori/nasional-sosial-budaya/935208/uji-coba-nasional-mulai-1-oktober-sistem-pembayaran-jkn-beralih-ke-idrg')] + SRC_JKN[1:],
  body_html=f'''
<p>Kamar operasi adalah pusat biaya termahal sekaligus sumber margin terbesar di rumah sakit. Semarang termasuk kota yang dipilih Kemenkes untuk uji coba iDRG sejak 2025, sehingga rumah sakit di sini lebih dulu merasakan bahwa tarif akan makin mengikuti kompleksitas kasus. Biaya juga harus bisa dibaca per kasus, dan untuk kamar operasi satuan yang paling jujur adalah menit.</p>
<p>Time-driven activity based costing (TDABC), yang diperkenalkan Kaplan dan Anderson, hanya membutuhkan dua angka: biaya kapasitas per menit dan jumlah menit yang dipakai setiap tindakan.</p>
<h2>Kenapa ABC Konvensional Sering Berhenti di Tengah Jalan</h2>
<p>ABC konvensional meminta pegawai memperkirakan pembagian waktu ke puluhan aktivitas. Di instalasi bedah, survei seperti itu melelahkan, hasilnya selalu berjumlah 100 persen, dan tidak pernah memperlihatkan waktu yang menganggur. TDABC membalik urutannya: mulai dari kapasitas yang disediakan, lalu hitung berapa yang terpakai.</p>
<h2>Langkah 1: Biaya Kapasitas per Menit</h2>
<p>Ilustrasi berikut memakai angka contoh instalasi bedah sentral dengan empat kamar operasi, satu bulan.</p>
{tbl(['Sumber daya kamar operasi', 'Biaya per bulan'], [[a, jt(c)] for a, c in CAP], ['Biaya kapasitas yang disediakan', jt(CAPT)])}
<p>Kapasitas teoretis: 4 kamar x 25 hari x 8 jam x 60 menit = {n(TEOR)} menit. Kapasitas praktis diambil 80 persen karena ada jeda, rapat, dan pemeliharaan, yaitu {n(PRAK)} menit. Biaya kapasitas per menit = {jt(CAPT)} / {n(PRAK)} menit = <b>{rp(CCR)} per menit</b>.</p>
<p>Obat, implan, dan bahan habis pakai tidak masuk ke angka ini karena ditelusuri langsung ke pasien. Jasa medis operator dan anestesi juga dihitung terpisah.</p>
<h2>Langkah 2: Persamaan Waktu per Tindakan</h2>
<p>Tindakan tidak dikelompokkan menjadi kecil, sedang, besar. Waktu dihitung dari penyebabnya:</p>
<blockquote>Menit kamar operasi = 25 (persiapan dan pembersihan) + menit insisi sampai tutup + 20 bila anestesi umum + 15 bila memakai menara laparoskopi atau C-arm</blockquote>
{tbl(['Tindakan', 'Persamaan waktu', 'Menit per tindakan', 'Volume per bulan', 'Total menit', 'Biaya kapasitas per tindakan'], rows_t,
     ['Jumlah', '', '', n(nops), n(used), ''])}
<p>Kalau {jt(CAPT)} dibagi rata ke {n(nops)} operasi, setiap operasi menanggung {rp(AVG)}. Angka itu terlalu tinggi untuk herniotomi dan sectio caesarea, dan terlalu rendah untuk kolesistektomi laparoskopi dan ORIF.</p>
<h2>Langkah 3: Membaca Kapasitas Menganggur</h2>
<p>Dari {n(PRAK)} menit kapasitas praktis, yang terpakai {n(used)} menit. Sisanya {n(IDLE)} menit, atau {pct(IDLE / PRAK)}, adalah kapasitas menganggur senilai <b>{jt(IDLE * CCR, 1)} per bulan</b>.</p>
<p>Biaya ini tidak dibebankan ke pasien. Ia dilaporkan sebagai baris tersendiri kepada direksi, karena penyebab dan obatnya ada di manajemen, bukan di tindakan:</p>
<ul>
<li>Jadwal operasi elektif menumpuk di pagi hari dan kosong setelah pukul 14.00.</li>
<li>Kamar keempat dibuka padahal volume belum menuntutnya.</li>
<li>Waktu pergantian pasien lebih lama dari standar.</li>
</ul>
<div class="pf-fold"><p>Kelebihan lain TDABC adalah kemudahan simulasi. Bila waktu persiapan dan pembersihan turun dari 25 menjadi 18 menit, {n(nops)} operasi membebaskan {n(nops * 7)} menit per bulan. Dengan persamaan waktu yang sama, itu setara dengan tambahan sekitar {n(nops * 7 // 68)} sectio caesarea (masing-masing 68 menit) tanpa menambah kamar, perawat, maupun alat.</p>
<p>Untuk kasus JKN, biaya kapasitas per tindakan ini digabungkan dengan biaya langsung dan biaya rawat inap menjadi biaya per episode, lalu dibandingkan dengan tarif kelompok kasusnya. Cara merangkainya kami bahas di <a href="/artikel/unit-cost-clinical-pathway-menghadapi-idrg/">unit cost berbasis clinical pathway</a>.</p></div>
<h2>Data yang Dibutuhkan dari Rumah Sakit</h2>
<ul>
<li>Laporan operasi 6 sampai 12 bulan: jam pasien masuk kamar, insisi, tutup, dan keluar kamar.</li>
<li>Jenis anestesi dan alat utama yang dipakai per tindakan.</li>
<li>Daftar pegawai dan jadwal dinas instalasi bedah serta penyusutan alat per kamar.</li>
<li>Pemakaian implan dan bahan habis pakai per pasien dari farmasi.</li>
</ul>
<p>Rumah sakit yang belum mencatat jam insisi dan jam tutup secara disiplin sebaiknya memulainya sekarang. Tanpa data waktu, tidak ada metode costing yang bisa menolong.</p>
<h2>Keputusan yang Bisa Diambil Setelahnya</h2>
<ul>
<li>Menyusun tarif paket bedah untuk pasien umum dan asuransi berdasarkan menit, bukan perkiraan.</li>
<li>Menilai usulan dokter untuk alat baru: berapa menit dan berapa kasus yang dibutuhkan agar investasinya kembali.</li>
<li>Menata blok jadwal operator supaya kamar terisi merata.</li>
<li>Menentukan kapan membuka kamar operasi tambahan atau justru menutup satu kamar pada hari tertentu.</li>
</ul>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Rumah sakit di Semarang dan sekitarnya didampingi tim FA Indonesia mulai dari pembersihan data waktu operasi, perhitungan biaya kapasitas, sampai laporan kapasitas menganggur yang bisa dibaca direksi setiap bulan. Hasilnya dituangkan dalam kertas kerja yang bisa diperbarui sendiri oleh tim rumah sakit. Lihat <a href="/konsultan-unit-cost-rumah-sakit/semarang/">konsultan unit cost rumah sakit di Semarang</a>, <a href="/konsultan-rumah-sakit/semarang/">konsultan rumah sakit Semarang</a>, dan perangkat <a href="/fa-venus-rumah-sakit/">FA Venus untuk rumah sakit</a>.</p>
''',
  faq=[('Apa itu time-driven activity based costing?', 'Metode costing yang membebankan biaya berdasarkan waktu. Biaya kapasitas yang disediakan dibagi kapasitas praktis dalam menit, lalu setiap tindakan dibebani sebesar menit yang dipakainya.'),
       ('Bagaimana menghitung biaya kamar operasi per menit?', 'Jumlahkan biaya pegawai, alat, ruang, dan sterilisasi instalasi bedah per bulan, lalu bagi dengan kapasitas praktis, yaitu sekitar 80 persen dari menit yang tersedia. Obat, implan, dan jasa medis dihitung terpisah.'),
       ('Apakah biaya kapasitas menganggur dibebankan ke pasien?', 'Tidak. Biaya kapasitas menganggur dilaporkan terpisah kepada manajemen agar tarif tidak ikut naik hanya karena kamar operasi kurang terisi.'),
       ('Apakah TDABC cocok untuk rumah sakit daerah?', 'Cocok selama waktu masuk, insisi, tutup, dan keluar kamar operasi dicatat. Metodenya lebih ringan daripada ABC konvensional karena tidak membutuhkan survei alokasi waktu pegawai.')])

# ------------------------------------------------------------------ 3. Makassar (hemodialisis)
HDF = [('Perawat dialisis dan dokter penanggung jawab', 210e6), ('Mesin dialisis: sewa atau penyusutan dan pemeliharaan', 96e6),
       ('Pengolahan air (RO), listrik, dan air', 54e6), ('Ruang dan alokasi biaya umum rumah sakit', 60e6)]
HDT = sum(c for _, c in HDF); VAR = 430e3; KAPT = 12 * 2 * 26; KAPP = 560; TARIF = 1250e3
uc = lambda v: VAR + HDT / v
BEP = HDT / (TARIF - VAR)
import math
BEPU = math.ceil(BEP)

A(site='fa', topik='abc', kota='Makassar', kota_slug='makassar',
  slug='unit-cost-hemodialisis-rumah-sakit-makassar-abc',
  seo_title='Unit Cost Hemodialisis Rumah Sakit di Makassar dengan ABC',
  title='Unit Cost Hemodialisis dan Penunjang Medik di Rumah Sakit Makassar dengan Activity Based Costing',
  description='Contoh unit cost hemodialisis rumah sakit di Makassar dengan activity based costing: biaya kapasitas, titik impas tindakan, dan keputusan sewa atau beli alat.',
  keyword='unit cost hemodialisis', category='Rumah Sakit',
  cta={'href': '/konsultan-unit-cost-rumah-sakit/makassar/', 'label': 'Konsultan Unit Cost Rumah Sakit Makassar'},
  wa='Halo Pak Ananta, saya ingin diskusi unit cost layanan penunjang (hemodialisis, laboratorium, radiologi) untuk rumah sakit kami di Makassar.',
  related=['cara-menghitung-unit-cost-rumah-sakit', 'idrg-pengganti-ina-cbg-persiapan-rumah-sakit', 'titik-impas-rumah-sakit-per-dpjp', 'piutang-klaim-bpjs-dan-arus-kas-rumah-sakit'],
  sources=[('IDN Times Sulsel: Makassar Pilot Project Reformasi JKN (Oktober 2026)', 'https://sulsel.idntimes.com/news/sulawesi-selatan/makassar-pilot-project-reformasi-jkn-pasien-bisa-dirujuk-langsung-00-5qckx-ys1x9q')] + SRC_JKN,
  body_html=f'''
<p>Makassar menjadi satu dari empat daerah uji coba reformasi JKN yang diumumkan Kemenkes pada 2026: rujukan berbasis kemampuan layanan, kelas rawat inap standar, dan pembayaran iDRG. Uji coba itu baru berjalan efektif setelah Perpres JKN ditandatangani, dan sampai artikel ini ditulis tarif INA-CBG dalam Permenkes 3 Tahun 2023 masih menjadi dasar klaim.</p>
<p>Arah kebijakannya sudah jelas: pasien akan dirujuk ke rumah sakit yang mampu, bukan ke yang kelasnya lebih tinggi. Rumah sakit di Makassar perlu tahu layanan mana yang layak dijadikan unggulan. Untuk layanan penunjang seperti hemodialisis, laboratorium, dan radiologi, jawabannya ada di unit cost yang dihitung dengan activity based costing (ABC).</p>
<h2>Kenapa Layanan Penunjang Butuh Cara Hitung Sendiri</h2>
<p>Biaya layanan penunjang didominasi kapasitas: mesin, ruang khusus, dan tenaga terlatih yang tetap dibayar berapa pun jumlah pasiennya. Membagi total biaya dengan jumlah tindakan bulan ini menghasilkan unit cost yang naik turun mengikuti volume, sehingga tidak bisa dipakai untuk memutuskan tarif atau investasi alat.</p>
<p>ABC memilah aktivitas menurut tingkatannya, dan tiap tingkatan punya pemicu biaya sendiri.</p>
{tbl(['Tingkat aktivitas', 'Contoh di hemodialisis', 'Contoh di laboratorium', 'Pemicu biaya'],
     [['Unit (per tindakan)', 'Dializer, selang darah, cairan dialisat', 'Reagen dan tabung per pemeriksaan', 'Jumlah tindakan'],
      ['Batch (per sesi)', 'Desinfeksi mesin dan priming tiap shift', 'Kalibrasi dan kontrol mutu tiap run', 'Jumlah sesi atau run'],
      ['Layanan', 'Pelatihan perawat dialisis, perizinan unit', 'Uji banding dan validasi metode', 'Jenis layanan'],
      ['Fasilitas', 'Ruang, pengolahan air, manajemen', 'Ruang, sistem informasi laboratorium', 'Kapasitas terpasang']])}
<h2>Contoh Unit Cost Hemodialisis</h2>
<p>Ilustrasi berikut memakai angka contoh unit hemodialisis dengan 12 mesin, dua shift, 26 hari kerja per bulan.</p>
{tbl(['Biaya kapasitas per bulan', 'Jumlah'], [[a, jt(c)] for a, c in HDF], ['Jumlah biaya kapasitas', jt(HDT)])}
<p>Kapasitas teoretis 12 x 2 x 26 = {n(KAPT)} tindakan. Kapasitas praktis diambil {n(KAPP)} tindakan karena ada pasien batal, mesin dirawat, dan hari libur. Biaya bahan per tindakan (dializer, selang darah, jarum fistula, dialisat, antikoagulan) dalam contoh ini {rp(VAR)}.</p>
{tbl(['Volume per bulan', 'Biaya kapasitas per tindakan', 'Bahan per tindakan', 'Unit cost'],
     [[f'{n(v)} tindakan' + (' (kapasitas praktis)' if v == KAPP else ''), rp(HDT / v), rp(VAR), rp(uc(v))] for v in (400, 480, KAPP)])}
<p>Unit cost yang dipakai untuk keputusan tarif adalah angka pada kapasitas praktis, {rp(uc(KAPP))}. Bila volume aktual 480 tindakan, selisih {n(KAPP - 480)} tindakan dikalikan {rp(HDT / KAPP)} adalah biaya kapasitas menganggur {jt((KAPP - 480) * HDT / KAPP)} per bulan yang dilaporkan terpisah.</p>
<h2>Titik Impas Tindakan</h2>
<p>Bila pendapatan bersih per tindakan dalam contoh ini {rp(TARIF)}, margin kontribusi per tindakan {rp(TARIF - VAR)}. Titik impas = {jt(HDT)} / {rp(TARIF - VAR)} = {n(BEP, 1)}, dibulatkan menjadi <b>{n(BEPU)} tindakan per bulan</b>.</p>
<p>Pada 480 tindakan unit ini masih rugi {jt(HDT - 480 * (TARIF - VAR), 1)}. Pada {n(KAPP)} tindakan labanya {jt(KAPP * (TARIF - VAR) - HDT, 1)}. Jadi persoalannya bukan tarif, melainkan {n(KAPP - 480)} kursi kosong setiap bulan. Angka pendapatan di sini hanya ilustrasi; untuk pasien JKN gunakan tarif yang berlaku bagi rumah sakit Anda.</p>
<h2>Sewa Alat, Beli, atau Kerja Sama Operasi</h2>
<div class="pf-fold"><p>Banyak unit penunjang di Sulawesi Selatan berjalan dengan skema kerja sama operasi: pemasok menaruh mesin, rumah sakit membeli bahan habis pakai dengan harga yang sudah memuat sewa alat. Di laporan laba rugi biayanya terlihat variabel, padahal kontraknya memuat pembelian minimum yang sifatnya tetap.</p>
<p>ABC membantu membandingkan pilihan itu secara setara:</p>
<ul>
<li>Pisahkan harga bahan dari komponen sewa alat di dalam harga paket.</li>
<li>Hitung biaya per tindakan pada volume minimum kontrak dan pada kapasitas praktis.</li>
<li>Bandingkan dengan pilihan membeli alat: penyusutan, pemeliharaan, dan biaya dana.</li>
<li>Perhatikan klausul kenaikan harga, masa kontrak, dan siapa yang menanggung kerusakan.</li>
</ul>
<p>Untuk laporan keuangan, kontrak penempatan alat seperti ini juga perlu dinilai apakah mengandung sewa menurut PSAK 116.</p></div>
<h2>Menerapkan Cara yang Sama di Laboratorium dan Radiologi</h2>
<ul>
<li><b>Laboratorium:</b> pemicu utamanya jumlah run, bukan jumlah pemeriksaan. Pemeriksaan bervolume kecil menanggung biaya kalibrasi dan kontrol mutu yang sama dengan pemeriksaan bervolume besar, sehingga sebagian lebih murah dirujuk.</li>
<li><b>Radiologi:</b> pemicunya menit pemakaian alat dan waktu baca dokter. CT scan dengan kontras memakai waktu dan bahan jauh lebih besar daripada tanpa kontras.</li>
<li><b>Semua penunjang:</b> laporkan utilisasi terhadap kapasitas praktis setiap bulan, bukan hanya jumlah tindakan.</li>
</ul>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Rumah sakit di Makassar dan kota lain di Sulawesi Selatan didampingi tim FA Indonesia untuk menghitung unit cost layanan penunjang, titik impas per unit, dan perbandingan skema alat. Sisi medis dan operasional dikerjakan bersama konsultan rumah sakit di dalam tim. Lihat <a href="/konsultan-unit-cost-rumah-sakit/makassar/">konsultan unit cost rumah sakit di Makassar</a>, <a href="/konsultan-rumah-sakit/makassar/">konsultan rumah sakit Makassar</a>, dan <a href="/kalkulator-unit-cost-rumah-sakit/">kalkulator unit cost rumah sakit</a>.</p>
''',
  faq=[('Bagaimana cara menghitung unit cost hemodialisis?', 'Jumlahkan biaya kapasitas unit per bulan (tenaga, mesin, pengolahan air, ruang), bagi dengan kapasitas praktis tindakan, lalu tambahkan biaya bahan per tindakan seperti dializer, selang darah, dan dialisat.'),
       ('Berapa titik impas unit hemodialisis?', 'Titik impas adalah biaya kapasitas per bulan dibagi margin kontribusi per tindakan, yaitu pendapatan bersih per tindakan dikurangi biaya bahan. Hasilnya berbeda untuk setiap rumah sakit.'),
       ('Apakah skema kerja sama operasi alat selalu lebih murah?', 'Belum tentu. Harga bahan dalam skema itu sudah memuat sewa alat dan biasanya ada pembelian minimum. Bandingkan biaya per tindakan pada volume minimum kontrak dan pada kapasitas praktis.'),
       ('Apakah uji coba reformasi JKN di Makassar sudah mengubah tarif?', 'Sampai artikel ini ditulis, uji coba baru efektif setelah Perpres JKN ditandatangani dan tarif INA-CBG dalam Permenkes 3 Tahun 2023 masih menjadi dasar klaim.')])
