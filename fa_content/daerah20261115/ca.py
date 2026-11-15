# -*- coding: utf-8 -*-
"""CariAkuntan: 10 artikel daerah. Sudut: cara memilih profesional dan kantor yang tepat, lalu rekanan (tim FA Indonesia).
Link internal CA relatif (/kota/<kota>/...), link FA absolut."""
from _k import A, n, rp, jt, pct, tbl

FA = 'https://faindonesia.co.id'
M = 1e9; J = 1e6
S_AUP = ('IAPI: Standar Jasa Terkait 4400, Perikatan Prosedur yang Disepakati', 'https://iapi.or.id/')
S_PMK6 = ('Permenkes Nomor 6 Tahun 2026 tentang Rumah Sakit (teks pada Pasal.id)', 'https://pasal.id/peraturan/permen/permenkes-no-6-tahun-2026')
S_PT = ('Undang-Undang Nomor 40 Tahun 2007 tentang Perseroan Terbatas', 'https://peraturan.bpk.go.id/Details/39965/uu-no-40-tahun-2007')
S_KEK = ('Bisnis.com: Warga RI Banyak Berobat ke Luar Negeri, KEK Disiapkan Jadi Pusat Kesehatan (12 Mei 2026)', 'https://ekonomi.bisnis.com/read/20260512/12/1973351/warga-ri-banyak-berobat-ke-luar-negeri-kek-disiapkan-jadi-pusat-kesehatan')
S_JKN = ('ANTARA: Kemenkes Uji Coba Reformasi JKN di Muara Enim (Oktober 2026)', 'https://www.antaranews.com/berita/5771342/kemenkes-uji-coba-reformasi-jkn-di-muara-enim-pangkas-waktu-tunggu')


def rek(kota, slug, topik):
    """Paragraf penutup: rekanan + link kota (CA) + link FA."""
    fa = {'abc': (f'{FA}/konsultan-unit-cost-rumah-sakit/{slug}/', f'konsultan unit cost rumah sakit di {kota}'),
          'pe': (f'{FA}/pendanaan-rumah-sakit/{slug}/', f'pendampingan pendanaan rumah sakit di {kota}'),
          'cfo': (f'{FA}/cfo-paruh-waktu/', 'layanan CFO paruh waktu')}[topik]
    return (f'<p>Di CariAkuntan, kebutuhan ini dikerjakan rekanan kami, tim FA Indonesia, bersama kantor jasa akuntan dan kantor akuntan publik yang berizin. '
            f'Lihat <a href="{fa[0]}">{fa[1]}</a>, daftar kantor di <a href="/kota/{slug}/">{kota}</a>, atau pastikan dulu jenis kantor yang Anda perlukan lewat <a href="/cek-kebutuhan/">Cek Kebutuhan</a>.</p>')


# ================================================================== ABC
# 1. Medan
W = [('Pengalaman di rumah sakit sekelas', 25), ('Metode dan kertas kerja yang diserahkan', 25), ('Tim: akuntan manajemen dan pemahaman klinis', 20),
     ('Rekonsiliasi ke laporan keuangan', 15), ('Alih pengetahuan ke tim rumah sakit', 15)]
SC = {'Konsultan A': (4, 5, 4, 5, 4), 'Konsultan B': (5, 3, 3, 2, 3), 'Vendor aplikasi': (3, 2, 2, 1, 2)}
tot = {k: sum(w * s for (_, w), s in zip(W, v)) / 100 for k, v in SC.items()}

A(site='ca', topik='abc', kota='Medan', kota_slug='medan',
  slug='memilih-konsultan-unit-cost-rumah-sakit-medan',
  seo_title='Memilih Konsultan Unit Cost Rumah Sakit di Medan',
  title='Memilih Konsultan Unit Cost Rumah Sakit di Medan: Kompetensi, Hasil Kerja, dan Cara Menilai',
  description='Panduan pemilik dan direksi rumah sakit di Medan memilih konsultan unit cost activity based costing: kompetensi, hasil kerja wajib, dan tabel penilaian.',
  keyword='konsultan unit cost rumah sakit medan', category='Manajemen Biaya',
  wa='Halo Pak Ananta, kami rumah sakit di Medan dan sedang mencari konsultan unit cost. Mohon arahannya.',
  sources=[('DDTCNews: Devisa Rp170 Triliun Hilang karena WNI Berobat ke Luar Negeri (14 Juni 2023)', 'https://news.ddtc.co.id/berita/nasional/1795060/jokowi-devisa-rp-170-triliun-hilang-karena-wni-berobat-ke-luar-negeri'), S_JKN],
  body_html=f'''
<p>Rumah sakit di Medan bersaing bukan hanya dengan sesama rumah sakit di Sumatera Utara. Medan termasuk kota asal warga yang berobat ke luar negeri, sehingga tarif dan mutu layanan pasien umum selalu dibandingkan dengan rumah sakit di negeri tetangga. Di sisi lain, tarif pasien JKN ditetapkan pemerintah. Dalam posisi itu, mengetahui biaya per layanan adalah kebutuhan, dan banyak direksi mulai mencari konsultan unit cost.</p>
<p>Masalahnya, unit cost bukan jasa yang izinnya diatur seperti audit atau penilaian. Siapa saja bisa menawarkan. Panduan ini membantu Anda menilai penawaran.</p>
<h2>Siapa yang Kompeten Menghitung Unit Cost</h2>
<ul>
<li><b>Akuntan manajemen.</b> Menguasai activity based costing, alokasi biaya, dan rekonsiliasi ke laporan keuangan. Kredensial yang relevan antara lain akuntan beregister (CA), akuntan publik (CPA), dan sertifikasi akuntan manajemen.</li>
<li><b>Orang yang paham proses klinis.</b> Dokter atau manajer rumah sakit berpengalaman yang bisa menerjemahkan clinical pathway menjadi aktivitas dan pemicu biaya.</li>
<li><b>Analis data.</b> Menarik dan membersihkan data SIMRS.</li>
</ul>
<p>Tim yang baik punya ketiganya. Kantor jasa akuntan boleh memberikan jasa akuntansi manajemen. Kantor akuntan publik yang mengaudit rumah sakit Anda sebaiknya tidak sekaligus menyusun unit cost yang nanti memengaruhi angka yang diauditnya.</p>
<h2>Hasil Kerja yang Harus Tertulis di Penawaran</h2>
<ol>
<li>Kamus aktivitas dan daftar pemicu biaya.</li>
<li>Kertas kerja perhitungan dalam Excel yang bisa dibuka dan diperbarui tim Anda, bukan hanya laporan PDF.</li>
<li>Unit cost per layanan untuk jumlah layanan yang disebut jelas, misalnya 30 tindakan dan 10 kelompok kasus terbesar.</li>
<li>Rekonsiliasi total biaya ke buku besar dan laporan keuangan.</li>
<li>Analisis margin per layanan dan per penjamin.</li>
<li>Sesi alih pengetahuan dan panduan pembaruan berkala.</li>
</ol>
<h2>Tabel Penilaian Penawaran</h2>
<p>Contoh cara menilai tiga penawaran dengan bobot. Nilai 1 sampai 5, angka di bawah hanya ilustrasi.</p>
{tbl(['Kriteria', 'Bobot'] + list(SC), [[c, f'{w}%'] + [str(SC[k][i]) for k in SC] for i, (c, w) in enumerate(W)],
     ['Nilai tertimbang', '100%'] + [n(tot[k], 2) for k in SC])}
<p>Penawaran termurah belum tentu paling rendah nilainya, dan sebaliknya. Yang perlu dihindari adalah penawaran tanpa rekonsiliasi ke laporan keuangan: unit cost yang tidak kembali ke buku besar tidak bisa dipakai di depan bank, asuransi, atau investor.</p>
<h2>Pertanyaan untuk Calon Konsultan</h2>
<div class="pf-fold"><ul>
<li>Metode apa yang dipakai: distribusi ganda, activity based costing, atau time-driven ABC, dan mengapa?</li>
<li>Data apa yang diminta dari kami dan berapa lama tim kami harus terlibat?</li>
<li>Bagaimana jasa medis dan obat diperlakukan?</li>
<li>Apakah kapasitas menganggur dipisahkan atau ikut dibebankan ke pasien?</li>
<li>Siapa yang mengerjakan sehari-hari, dan siapa yang bertanggung jawab atas hasil?</li>
<li>Apakah kertas kerja menjadi milik rumah sakit?</li>
</ul></div>
<h2>Tanda Bahaya</h2>
<ul>
<li>Menjanjikan angka penghematan sebelum melihat data.</li>
<li>Hasil hanya berupa aplikasi tanpa penjelasan metode.</li>
<li>Tidak ada anggota tim yang memahami akuntansi rumah sakit.</li>
<li>Menolak menyerahkan kertas kerja.</li>
</ul>
<h2>Langkah Berikutnya untuk Rumah Sakit di Medan</h2>
{rek('Medan', 'medan', 'abc')}
<p>Bila masih ragu apakah yang dibutuhkan konsultan unit cost atau pembenahan pembukuan lebih dulu, baca juga halaman <a href="/kota/medan/konsultan-rumah-sakit/">konsultan rumah sakit di Medan</a>.</p>
''',
  faq=[('Apakah konsultan unit cost harus berizin?', 'Tidak ada izin khusus untuk jasa unit cost. Karena itu kompetensi dinilai dari kredensial akuntansi tim, pengalaman di rumah sakit, dan hasil kerja yang dijanjikan tertulis.'),
       ('Berapa lama pekerjaan unit cost rumah sakit?', 'Umumnya 8 sampai 12 minggu untuk rumah sakit menengah, bergantung pada kesiapan data SIMRS dan pembukuan.'),
       ('Bolehkah auditor kami yang menghitung unit cost?', 'Sebaiknya tidak. Auditor harus independen dari angka yang diauditnya, sehingga penyusunan unit cost lebih tepat dikerjakan pihak lain.')])

# 2. Yogyakarta
A(site='ca', topik='abc', kota='Yogyakarta', kota_slug='yogyakarta',
  slug='unit-cost-rumah-sakit-yogyakarta-tim-internal-atau-konsultan',
  seo_title='Unit Cost Rumah Sakit di Yogyakarta: Internal atau Konsultan',
  title='Unit Cost Rumah Sakit dan Klinik di Yogyakarta: Dikerjakan Tim Internal, Kampus, atau Konsultan?',
  description='Rumah sakit dan klinik di Yogyakarta punya tiga pilihan mengerjakan unit cost activity based costing. Ini perbandingan, syarat data, dan peran tiap kantor.',
  keyword='unit cost rumah sakit yogyakarta', category='Manajemen Biaya',
  wa='Halo Pak Ananta, kami rumah sakit/klinik di Yogyakarta dan ingin menghitung unit cost. Sebaiknya mulai dari mana?',
  sources=[S_AUP, S_JKN],
  body_html=f'''
<p>Yogyakarta adalah kota pendidikan dan kesehatan. Rumah sakit yayasan, rumah sakit swasta keluarga, dan klinik utama tumbuh berdampingan dengan kampus yang punya program manajemen rumah sakit dan akuntansi. Ketika direksi memutuskan menghitung unit cost dengan activity based costing (ABC), pilihannya lebih banyak daripada di kota lain: tim internal, kerja sama kampus, atau konsultan.</p>
<h2>Tiga Pilihan dan Konsekuensinya</h2>
{tbl(['Aspek', 'Tim internal', 'Kerja sama kampus', 'Konsultan'],
     [['Biaya tunai', 'Paling rendah', 'Rendah sampai sedang', 'Paling tinggi'],
      ['Waktu selesai', 'Sering molor karena pekerjaan rutin', 'Mengikuti kalender akademik', 'Terjadwal dalam kontrak'],
      ['Pemahaman data rumah sakit', 'Paling baik', 'Perlu waktu belajar', 'Bergantung pengalaman tim'],
      ['Metode dan kedalaman', 'Bergantung satu dua orang', 'Kuat di teori', 'Kuat di praktik dan pembanding'],
      ['Keberlanjutan', 'Baik bila orangnya bertahan', 'Lemah setelah penelitian selesai', 'Baik bila ada alih pengetahuan'],
      ['Diterima pihak luar', 'Sering dipertanyakan', 'Cukup untuk kajian', 'Lebih mudah diterima bank dan asuransi']])}
<p>Banyak rumah sakit akhirnya menggabungkan: konsultan menyusun kerangka dan perhitungan pertama, tim internal memperbarui tiap semester.</p>
<h2>Uji Kesiapan Sebelum Memilih</h2>
<ul>
<li>Apakah pembukuan sudah memisahkan biaya per unit atau pusat biaya?</li>
<li>Apakah SIMRS bisa mengeluarkan jumlah tindakan, hari rawat, dan resep per layanan?</li>
<li>Apakah daftar aset dan penyusutan sudah diperbarui?</li>
<li>Apakah ada satu orang keuangan yang bisa dilepas separuh waktunya selama dua bulan?</li>
</ul>
<p>Bila dua jawaban pertama masih tidak, pekerjaan pertama bukan unit cost melainkan pembenahan pembukuan. Itu wilayah kantor jasa akuntan.</p>
<h2>Siapa Mengerjakan Apa</h2>
{tbl(['Kebutuhan', 'Kantor yang tepat'],
     [['Pembukuan dan laporan keuangan per unit', 'Kantor jasa akuntan (KJA)'],
      ['Perhitungan unit cost dan analisis margin', 'Akuntan manajemen atau konsultan rumah sakit'],
      ['Audit laporan keuangan', 'Kantor akuntan publik (KAP)'],
      ['Laporan atas perhitungan unit cost untuk pihak luar', 'KAP melalui perikatan prosedur yang disepakati'],
      ['Penilaian aset atau nilai usaha rumah sakit', 'Kantor jasa penilai publik (KJPP)']])}
<h2>Ketika Unit Cost Dipakai untuk Negosiasi</h2>
<div class="pf-fold"><p>Asuransi dan perusahaan penjamin kadang meminta dasar perhitungan tarif paket. Rumah sakit dapat meminta akuntan publik menjalankan prosedur yang disepakati atas perhitungan unit cost, misalnya mencocokkan total biaya ke laporan keuangan dan menghitung ulang alokasinya. Hasilnya berupa laporan temuan faktual, bukan opini, tetapi cukup memberi keyakinan bagi pihak yang membaca.</p>
<p>Pilihan ini relevan bagi rumah sakit di Yogyakarta, Sleman, dan Bantul yang melayani banyak peserta asuransi swasta dan jaminan perusahaan.</p></div>
<h2>Bila Memilih Konsultan</h2>
<ul>
<li>Minta contoh kertas kerja, bukan hanya proposal.</li>
<li>Pastikan ada rekonsiliasi ke laporan keuangan.</li>
<li>Pastikan kertas kerja menjadi milik rumah sakit dan ada sesi pelatihan.</li>
<li>Sepakati daftar layanan yang dihitung sejak awal.</li>
</ul>
<h2>Langkah Berikutnya untuk Rumah Sakit di Yogyakarta</h2>
{rek('Yogyakarta', 'yogyakarta', 'abc')}
''',
  faq=[('Apakah klinik juga perlu menghitung unit cost?', 'Perlu bila klinik menetapkan tarif paket, bekerja sama dengan asuransi, atau menimbang layanan baru. Skalanya lebih sederhana daripada rumah sakit.'),
       ('Bisakah unit cost dikerjakan mahasiswa atau dosen?', 'Bisa sebagai kajian. Untuk dipakai rutin, pastikan ada kertas kerja yang bisa diperbarui dan orang internal yang memahaminya setelah penelitian selesai.'),
       ('Apa itu perikatan prosedur yang disepakati?', 'Jasa akuntan publik untuk menjalankan prosedur tertentu yang disepakati dan melaporkan temuan faktualnya, tanpa memberi opini. Dikenal juga sebagai AUP.')])

# 3. Palembang
TL = [('Minggu 1 sampai 2', 'Permintaan data, wawancara unit, pemetaan pusat biaya', 'Keuangan, SIMRS, kepala unit'),
      ('Minggu 3 sampai 5', 'Rekonsiliasi buku besar, kamus aktivitas, pemicu biaya', 'Keuangan, keperawatan, penunjang'),
      ('Minggu 6 sampai 8', 'Perhitungan tarif aktivitas dan unit cost layanan', 'Keuangan, SIMRS'),
      ('Minggu 9 sampai 10', 'Analisis margin, simulasi tarif, paparan direksi', 'Direksi, komite medik'),
      ('Minggu 11 sampai 12', 'Alih pengetahuan dan panduan pembaruan', 'Tim keuangan')]

A(site='ca', topik='abc', kota='Palembang', kota_slug='palembang',
  slug='data-unit-cost-activity-based-costing-rumah-sakit-palembang',
  seo_title='Data Unit Cost ABC yang Diminta Konsultan, RS Palembang',
  title='Menyiapkan Data Unit Cost Activity Based Costing: Panduan untuk Rumah Sakit di Palembang',
  description='Daftar data yang diminta konsultan unit cost dari rumah sakit di Palembang, jadwal kerja 12 minggu, dan peran tim internal agar pekerjaan tidak molor.',
  keyword='data unit cost rumah sakit', category='Manajemen Biaya',
  wa='Halo Pak Ananta, kami rumah sakit di Palembang dan ingin menyiapkan data untuk perhitungan unit cost.',
  sources=[S_JKN, ('Permenkes Nomor 3 Tahun 2023 tentang Standar Tarif Pelayanan Kesehatan dalam Penyelenggaraan Program JKN', 'https://peraturan.bpk.go.id/Details/275518')],
  body_html=f'''
<p>Sumatera Selatan ikut menjadi lokasi uji coba reformasi JKN: Kabupaten Muara Enim adalah satu dari empat daerah percontohan rujukan berbasis kemampuan layanan, kelas rawat inap standar, dan pembayaran iDRG. Rumah sakit di Palembang, sebagai pusat rujukan provinsi, akan merasakan dampaknya lebih awal. Banyak yang mulai menghitung ulang unit cost dengan activity based costing (ABC).</p>
<p>Pekerjaan unit cost jarang gagal karena metodenya. Ia gagal karena datanya tidak siap. Daftar berikut bisa dikerjakan tim rumah sakit sebelum konsultan datang.</p>
<h2>Data Keuangan</h2>
<ul>
<li>Buku besar 12 bulan terakhir dengan kode unit atau pusat biaya.</li>
<li>Laporan keuangan tahun terakhir, sebaiknya yang sudah diaudit.</li>
<li>Daftar aset tetap dengan lokasi unit, nilai perolehan, dan penyusutan.</li>
<li>Daftar gaji per pegawai dan unit penempatannya.</li>
<li>Rincian jasa medis per dokter dan per layanan.</li>
<li>Pembelian dan pemakaian obat serta bahan medis habis pakai per unit.</li>
</ul>
<h2>Data Layanan dari SIMRS</h2>
<ul>
<li>Jumlah kunjungan rawat jalan per poli dan per penjamin.</li>
<li>Hari rawat per ruang dan kelas.</li>
<li>Daftar tindakan dengan jumlah, dan untuk kamar operasi dengan jam mulai serta selesai.</li>
<li>Jumlah pemeriksaan laboratorium dan radiologi per jenis.</li>
<li>Jumlah resep dan lembar resep per unit.</li>
<li>Data klaim per kelompok kasus: jumlah kasus, lama rawat, dan nilai klaim.</li>
</ul>
<h2>Data Pemicu Biaya</h2>
<ul>
<li>Luas lantai per unit untuk alokasi gedung, kebersihan, dan listrik.</li>
<li>Kilogram cucian dan porsi makan per unit.</li>
<li>Jumlah perintah kerja pemeliharaan per unit.</li>
<li>Daya terpasang alat besar.</li>
</ul>
<h2>Jadwal Kerja 12 Minggu</h2>
{tbl(['Periode', 'Pekerjaan', 'Yang terlibat dari rumah sakit'], [list(r) for r in TL])}
<h2>Tiga Hal yang Paling Sering Membuat Molor</h2>
<div class="pf-fold"><ol>
<li><b>Biaya tidak punya kode unit.</b> Semua gaji dicatat di satu akun. Solusinya pemetaan dari daftar pegawai, tidak perlu menunggu sistem diubah.</li>
<li><b>Angka SIMRS dan keuangan tidak cocok.</b> Pendapatan menurut SIMRS berbeda dengan buku besar. Rekonsiliasi ini harus selesai sebelum unit cost dihitung.</li>
<li><b>Tidak ada penanggung jawab.</b> Tunjuk satu orang keuangan sebagai koordinator data dengan wewenang meminta data ke unit lain.</li>
</ol>
<p>Rumah sakit yang pembukuannya belum memisahkan biaya per unit sebaiknya membenahi itu lebih dulu bersama kantor jasa akuntan. Unit cost yang dibangun di atas pembukuan yang lemah hanya menghasilkan angka yang rapi tetapi keliru.</p></div>
<h2>Memilih Pihak yang Mengerjakan</h2>
<p>Unit cost dikerjakan akuntan manajemen atau konsultan rumah sakit. Audit laporan keuangan tetap dikerjakan kantor akuntan publik yang berbeda. Daftar kantor berizin bisa dicek di <a href="/cek-izin/">Cek Izin</a>.</p>
<h2>Langkah Berikutnya untuk Rumah Sakit di Palembang</h2>
{rek('Palembang', 'palembang', 'abc')}
''',
  faq=[('Data apa yang paling penting untuk unit cost?', 'Buku besar dengan kode unit dan volume layanan dari SIMRS. Tanpa keduanya, biaya tidak bisa ditelusuri ke layanan.'),
       ('Berapa orang tim internal yang perlu terlibat?', 'Minimal satu koordinator dari keuangan, satu orang SIMRS, dan perwakilan keperawatan serta penunjang untuk wawancara aktivitas.'),
       ('Apakah harus menunggu aturan iDRG berlaku?', 'Tidak. Unit cost berguna sejak sekarang untuk membaca margin kasus JKN dengan tarif yang berlaku dan untuk menetapkan tarif pasien umum.')])

# ================================================================== PE
# 4. Tangerang
A(site='ca', topik='pe', kota='Tangerang', kota_slug='tangerang',
  slug='kap-kjpp-konsultan-hukum-saat-investor-masuk-rumah-sakit-tangerang',
  seo_title='KAP, KJPP, Konsultan Hukum saat Investor Masuk RS Tangerang',
  title='Investor Masuk Rumah Sakit di Tangerang: Peran KAP, KJPP, Konsultan Hukum, dan Penasihat Keuangan',
  description='Saat private equity masuk ke rumah sakit di Tangerang, pemilik perlu KAP, KJPP, konsultan hukum, dan penasihat keuangan. Ini urutan dan perannya.',
  keyword='kap kjpp akuisisi rumah sakit', category='Pendanaan',
  wa='Halo Pak Ananta, rumah sakit kami di Tangerang sedang didekati investor. Kami perlu arahan soal KAP, KJPP, dan penasihat yang dibutuhkan.',
  sources=[('Bisnis.com: Siloam (SILO) Siapkan Rp6,91 Triliun Akuisisi 14 Rumah Sakit (15 Agustus 2026)', 'https://market.bisnis.com/read/20260815/192/1996555/siloam-silo-siapkan-rp691-triliun-akuisisi-14-rumah-sakit'),
           ('ANTARA Banten: Siloam Akuisisi Aset RS Rp6,9 Triliun Jadi Milik Sendiri (22 September 2026)', 'https://banten.antaranews.com/berita/391095/siloam-akuisisi-aset-rs-rp69-triliun-jadi-milik-sendiri'), S_PMK6],
  body_html=f'''
<p>Tangerang adalah rumah bagi sejumlah jaringan rumah sakit swasta besar. Pada 2026 salah satu emiten rumah sakit yang berkantor pusat di sini mengumumkan pengambilalihan 14 perusahaan pemilik properti rumah sakit senilai sekitar Rp6,91 triliun, yang disetujui pemegang saham pada September 2026. Transaksi sebesar itu melibatkan penilai, akuntan publik, dan konsultan hukum, masing-masing dengan laporan sendiri.</p>
<p>Rumah sakit privat di Tangerang, Tangerang Selatan, dan sekitarnya yang didekati private equity atau jaringan besar akan melewati proses serupa dalam skala lebih kecil. Pertanyaan pertama pemilik biasanya: kantor apa saja yang harus saya libatkan, dan kapan?</p>
<h2>Lima Profesi dan Tugasnya</h2>
{tbl(['Profesi', 'Tugas dalam transaksi', 'Bekerja untuk siapa'],
     [['Penasihat keuangan', 'Menyiapkan laporan, valuasi indikatif, data room, dan mendampingi perundingan', 'Pemilik rumah sakit'],
      ['Kantor akuntan publik (KAP)', 'Mengaudit laporan keuangan dua sampai tiga tahun terakhir', 'Perusahaan, hasilnya dibaca investor'],
      ['Kantor jasa penilai publik (KJPP)', 'Menilai tanah, bangunan, alat, atau nilai saham; pendapat kewajaran bila disyaratkan', 'Pihak yang memberi tugas'],
      ['Konsultan hukum', 'Uji tuntas hukum, struktur transaksi, perjanjian', 'Masing-masing pihak punya sendiri'],
      ['Konsultan pajak', 'Uji tuntas pajak dan dampak pajak struktur transaksi', 'Masing-masing pihak']])}
<h2>Urutan yang Masuk Akal</h2>
<ol>
<li><b>Penasihat keuangan lebih dulu.</b> Ia memetakan kesiapan dan menentukan apa yang perlu dibenahi sebelum pihak lain bekerja.</li>
<li><b>Audit KAP.</b> Bila laporan belum pernah diaudit, mulai dari tahun terakhir dan saldo awalnya. Pilih KAP yang reputasinya diterima calon investor.</li>
<li><b>Penilaian KJPP.</b> Dibutuhkan ketika nilai tanah dan bangunan menjadi bagian penting dari harga, atau ketika aset dipisahkan ke perusahaan lain.</li>
<li><b>Konsultan hukum dan pajak.</b> Masuk saat struktur transaksi mulai dibicarakan.</li>
</ol>
<h2>Menjaga Independensi</h2>
<ul>
<li>KAP yang mengaudit tidak boleh ikut menyusun laporan keuangan atau menjadi penasihat transaksi untuk perusahaan yang sama.</li>
<li>KJPP harus memiliki izin dan klasifikasi yang sesuai: penilai properti untuk aset, penilai bisnis untuk nilai saham. Untuk perusahaan terbuka, penilai juga harus terdaftar di otoritas pasar modal.</li>
<li>Penasihat keuangan pemilik tidak menerima imbalan dari investor.</li>
</ul>
<h2>Operasional dan Properti: Dua Nilai yang Berbeda</h2>
<div class="pf-fold"><p>Transaksi besar di Tangerang tadi memperlihatkan satu hal yang juga berlaku bagi rumah sakit kecil: bisnis rumah sakit dan propertinya bisa dimiliki pihak berbeda. Rumah sakit yang menyewa gedung membayar sewa, rumah sakit yang memiliki gedung menanggung penyusutan dan utang.</p>
<p>Investor akan bertanya di mana tanah dan bangunan berada. Bila atas nama pribadi pemilik, pilihannya dimasukkan ke perusahaan atau disewa dengan kontrak jangka panjang berharga pasar. Laporan KJPP menjadi dasar kedua pilihan itu, dan perlakuan sewanya di laporan keuangan mengikuti PSAK 116.</p></div>
<h2>Yang Perlu Disiapkan Pemilik</h2>
<ul>
<li>Laporan keuangan tiga tahun dan laporan manajemen bulanan.</li>
<li>Perizinan dan akreditasi yang masih berlaku.</li>
<li>Sertifikat tanah dan daftar aset.</li>
<li>Kontrak dokter, pemasok, dan penjamin.</li>
<li>Daftar perkara dan pengaduan.</li>
</ul>
<p>Masuknya investor asing juga mengubah status perusahaan menjadi penanaman modal asing dengan syarat khusus rumah sakit dalam Permenkes 6 Tahun 2026.</p>
<h2>Langkah Berikutnya untuk Rumah Sakit di Tangerang</h2>
{rek('Tangerang', 'tangerang', 'pe')}
<p>Daftar <a href="/kota/tangerang/kjpp/">KJPP di Tangerang</a> dan <a href="/layanan/kap/">kantor akuntan publik</a> dapat dilihat di CariAkuntan, dan izinnya bisa dicek di <a href="/cek-izin/">Cek Izin</a>.</p>
''',
  faq=[('Kantor apa yang pertama dihubungi saat ada investor mendekat?', 'Penasihat keuangan dari sisi pemilik. Ia memetakan kesiapan, lalu mengatur urutan kerja KAP, KJPP, konsultan hukum, dan konsultan pajak.'),
       ('Apakah rumah sakit privat perlu pendapat kewajaran dari KJPP?', 'Pendapat kewajaran diwajibkan untuk transaksi tertentu perusahaan terbuka. Bagi rumah sakit privat sifatnya pilihan, tetapi laporan penilaian sering diminta ketika nilai properti besar.'),
       ('Bolehkah KAP yang sama menjadi auditor dan penasihat transaksi?', 'Tidak untuk perusahaan yang sama, karena mengganggu independensi auditor.')])

# 5. Cirebon
P = 286 * M; ST = .729; NEW = 255 * M; OLD = 31 * M; AS = 563.5 * M; LI = 335.1 * M
POST = P / ST; PRE = POST - NEW; BV = AS - LI

A(site='ca', topik='pe', kota='Cirebon', kota_slug='cirebon',
  slug='investor-masuk-rumah-sakit-cirebon-pelajaran-bagi-pemilik',
  seo_title='Investor Masuk Rumah Sakit di Cirebon: Pelajaran Pemilik',
  title='Investor Masuk Rumah Sakit di Cirebon: Pelajaran bagi Pemilik Rumah Sakit di Daerah',
  description='Rencana akuisisi jaringan rumah sakit jantung di Cirebon senilai Rp286 miliar memberi pelajaran soal valuasi dan kantor yang perlu dilibatkan.',
  keyword='investor rumah sakit cirebon', category='Pendanaan',
  wa='Halo Pak Ananta, kami pemilik rumah sakit di wilayah Cirebon dan ingin diskusi kesiapan menerima investor.',
  sources=[('Fortune Indonesia: VISI Siapkan Rp286 M untuk Akuisisi RS Hasna Medika (27 Agustus 2026)', 'https://www.fortuneidn.com/business/visi-milik-nagita-raffi-siapkan-rp286-m-untuk-akuisisi-rs-hasna-medika-00-4vfn9-773b6y'),
           ('DealStreetAsia: Impact Investor Sweef Capital Invests in Indonesia\'s Avisena Healthcare', 'https://www.dealstreetasia.com/?p=474888')],
  body_html=f'''
<p>Pada Agustus 2026 sebuah emiten mengumumkan rencana mengambil alih 72,9 persen saham perusahaan pengelola dua rumah sakit jantung dan 11 klinik yang berbasis di Cirebon, dengan nilai transaksi Rp286 miliar. Menurut pemberitaan, Rp255 miliar berupa saham baru dan Rp31 miliar pembelian saham lama, dengan persetujuan pemegang saham dijadwalkan akhir September 2026.</p>
<p>Bagi pemilik rumah sakit di Cirebon, Indramayu, Majalengka, dan Kuningan, kabar itu menegaskan bahwa rumah sakit daerah dengan layanan unggulan memang dilirik investor. Media keuangan juga mencatat investor dampak dari luar negeri mulai masuk ke operator rumah sakit ibu dan anak di Indonesia. Ada beberapa pelajaran yang bisa dibaca dari angka yang diumumkan.</p>
<h2>Membaca Angka yang Diumumkan</h2>
<p>Hitungan kasar berikut memakai angka dari pemberitaan dan mengandaikan harga per saham sama untuk saham baru dan saham lama. Tujuannya latihan membaca, bukan penilaian atas transaksi itu.</p>
{tbl(['Langkah', 'Perhitungan', 'Hasil'],
     [['Nilai seluruh saham setelah dana masuk', f'{jt(P)} / 72,9%', jt(POST, 1)],
      ['Nilai sebelum dana baru masuk', f'{jt(POST, 1)} dikurangi saham baru {jt(NEW)}', jt(PRE, 1)],
      ['Ekuitas buku per akhir Maret 2026', f'Aset {jt(AS, 1)} dikurangi liabilitas {jt(LI, 1)}', jt(BV, 1)]])}
<p>Dengan pengandaian itu, nilai sebelum dana masuk berada di bawah ekuitas buku. Untuk perusahaan yang pada kuartal I 2026 masih mencatat rugi, investor memang cenderung menilai dari kemampuan menghasilkan laba, bukan dari nilai buku. Sebagian besar dana juga masuk ke perusahaan sebagai modal baru, bukan ke kantong pemilik lama.</p>
<h2>Tiga Pelajaran untuk Pemilik</h2>
<ol>
<li><b>Layanan unggulan menarik minat, laba menentukan harga.</b> Investor membayar untuk potensi, tetapi harga dihitung dari kinerja dan kebutuhan dana.</li>
<li><b>Dana baru berbeda dengan dana untuk pemilik.</b> Tanyakan sejak awal berapa bagian yang masuk ke perusahaan dan berapa yang membeli saham lama.</li>
<li><b>Kendali berpindah.</b> Di atas 50 persen, investor menjadi pengendali. Hak pemilik lama perlu diatur tertulis: kursi direksi dan komisaris, hak informasi, dan jalan keluar.</li>
</ol>
<h2>Kantor yang Dilibatkan dalam Transaksi Seperti Ini</h2>
{tbl(['Dokumen', 'Disusun oleh'],
     [['Laporan keuangan diaudit', 'Kantor akuntan publik (KAP)'],
      ['Laporan penilaian saham atau aset dan studi kelayakan', 'Kantor jasa penilai publik (KJPP)'],
      ['Uji tuntas dan perjanjian', 'Konsultan hukum'],
      ['Laporan manajemen, proyeksi, dan data room', 'Tim keuangan bersama penasihat keuangan']])}
<p>Untuk perusahaan terbuka, sebagian dokumen itu diwajibkan aturan pasar modal. Untuk rumah sakit privat tidak diwajibkan, tetapi investor yang serius akan memintanya.</p>
<h2>Menyiapkan Rumah Sakit Daerah agar Layak Dilirik</h2>
<div class="pf-fold"><ul>
<li>Badan hukum yang hanya bergerak di pelayanan kesehatan, dengan kepemilikan saham yang jelas.</li>
<li>Laporan keuangan diaudit minimal dua tahun.</li>
<li>Laba rugi per layanan, terutama layanan unggulan.</li>
<li>Piutang klaim yang bersih: mana yang tertunda, mana yang ditolak.</li>
<li>Kontrak dokter spesialis yang menjadi tulang punggung layanan.</li>
<li>Tanah dan bangunan atas nama perusahaan atau disewa dengan kontrak jelas.</li>
</ul>
<p>Pekerjaan ini makan waktu enam sampai dua belas bulan. Rumah sakit yang memulainya sebelum ada investor datang punya posisi tawar lebih baik daripada yang memulainya setelah menerima surat minat.</p></div>
<h2>Langkah Berikutnya untuk Rumah Sakit di Cirebon</h2>
{rek('Cirebon', 'cirebon', 'pe')}
<p>Daftar <a href="/kota/cirebon/kjpp/">KJPP di Cirebon</a> dan <a href="/kota/cirebon/konsultan-rumah-sakit/">konsultan rumah sakit di Cirebon</a> juga tersedia.</p>
''',
  faq=[('Apakah rumah sakit daerah diminati investor?', 'Ya, terutama yang punya layanan unggulan dan basis pasien kuat. Rencana akuisisi jaringan rumah sakit jantung di Cirebon pada 2026 adalah salah satu contohnya.'),
       ('Apa beda saham baru dan saham lama dalam transaksi?', 'Dana dari saham baru masuk ke perusahaan untuk ekspansi atau melunasi utang. Dana dari penjualan saham lama diterima pemegang saham yang menjual.'),
       ('Dokumen apa yang paling awal disiapkan?', 'Laporan keuangan diaudit, laba rugi per layanan, dan kejelasan kepemilikan aset serta perizinan.')])

# 6. Pontianak
A(site='ca', topik='pe', kota='Pontianak', kota_slug='pontianak',
  slug='rumah-sakit-pontianak-mencari-investor-memilih-kap-kjpp',
  seo_title='Rumah Sakit Pontianak Mencari Investor: Memilih KAP, KJPP',
  title='Rumah Sakit di Pontianak Mencari Investor: Memilih KAP dan KJPP yang Tepat',
  description='Rumah sakit di Pontianak yang ingin menarik investor perlu audit KAP dan penilaian KJPP. Ini cara memilih kantor, syarat izin, dan urutan kerja yang efisien.',
  keyword='kap kjpp pontianak rumah sakit', category='Pendanaan',
  wa='Halo Pak Ananta, kami rumah sakit di Pontianak yang ingin mencari investor. Mohon arahan memilih KAP dan KJPP.',
  sources=[S_KEK, ('detikHealth: Wamenkes Sebut RI Rugi Rp160 T Imbas Warga Pilih Berobat ke Negara Tetangga (27 Januari 2026)', 'https://health.detik.com/berita-detikhealth/d-8327205/wamenkes-sebut-ri-rugi-rp-160-t-imbas-warga-62-pilih-berobat-ke-negara-tetangga'), S_PT],
  body_html=f'''
<p>Pemerintah memperkirakan sekitar dua juta warga Indonesia berobat ke luar negeri setiap tahun dengan belanja kira-kira Rp150 triliun. Kalimantan Barat, yang berbatasan darat dengan negara tetangga, merasakan arus itu dari dekat. Bagi investor, arus tersebut berarti permintaan layanan yang belum terpenuhi di Pontianak. Bagi pemilik rumah sakit, itu alasan kuat untuk mencari dana ekspansi: menambah layanan spesialis, alat, dan tempat tidur.</p>
<p>Investor, baik perorangan, grup rumah sakit, maupun dana private equity, akan meminta dua dokumen dasar: laporan keuangan yang diaudit dan laporan penilaian. Keduanya datang dari kantor yang berbeda.</p>
<h2>Memilih Kantor Akuntan Publik</h2>
<ul>
<li><b>Izin.</b> Akuntan publik dan kantornya berizin Menteri Keuangan. Cek di <a href="/cek-izin/">Cek Izin</a>.</li>
<li><b>Diterima pembaca laporan.</b> Tanyakan kepada calon investor atau bank apakah ada daftar KAP yang mereka terima. Sebagian mensyaratkan KAP yang terdaftar di otoritas jasa keuangan.</li>
<li><b>Pengalaman rumah sakit.</b> Pendapatan klaim, jasa medis, dan persediaan farmasi punya risiko audit sendiri.</li>
<li><b>Lokasi tidak menentukan.</b> KAP dari kota lain dapat mengaudit rumah sakit di Pontianak dengan kombinasi kerja daring dan kunjungan lapangan.</li>
</ul>
<h2>Memilih Kantor Jasa Penilai Publik</h2>
<ul>
<li><b>Klasifikasi izin.</b> Penilaian tanah, bangunan, dan alat membutuhkan penilai properti. Penilaian saham atau nilai usaha membutuhkan penilai bisnis.</li>
<li><b>Tujuan penilaian.</b> Laporan untuk agunan bank berbeda dengan laporan untuk transaksi. Sebutkan tujuan sejak awal agar dasar nilainya tepat.</li>
<li><b>Tanggal penilaian.</b> Selaraskan dengan tanggal laporan keuangan yang diaudit.</li>
</ul>
<h2>Urutan Kerja yang Efisien</h2>
{tbl(['Urutan', 'Pekerjaan', 'Dikerjakan oleh'],
     [['1', 'Merapikan pembukuan dan menyusun laporan keuangan sesuai standar', 'Kantor jasa akuntan atau tim internal'],
      ['2', 'Audit laporan keuangan tahun terakhir', 'KAP'],
      ['3', 'Penilaian aset, dan nilai usaha bila diperlukan', 'KJPP'],
      ['4', 'Proyeksi, valuasi indikatif, materi paparan, data room', 'Penasihat keuangan pemilik'],
      ['5', 'Uji tuntas oleh investor', 'Tim investor, dilayani pemilik dan penasihatnya']])}
<p>Membalik urutan, misalnya menilai aset sebelum pembukuan rapi, biasanya berakhir dengan pekerjaan ulang.</p>
<h2>Hal Khas Rumah Sakit di Kalimantan Barat</h2>
<div class="pf-fold"><ul>
<li>Banyak rumah sakit dimiliki yayasan atau keluarga. Investor ekuitas hanya bisa masuk ke perseroan terbatas, sehingga bentuk badan hukum perlu ditata lebih dulu.</li>
<li>Dokter spesialis terbatas. Investor akan bertanya bagaimana layanan baru diisi tenaganya.</li>
<li>Rujukan dari kabupaten sekitar adalah kekuatan. Tunjukkan dengan data asal pasien.</li>
<li>Laporan keuangan wajib diaudit bila aset atau peredaran usaha perseroan sudah mencapai Rp50 miliar menurut UU Perseroan Terbatas, terlepas dari ada tidaknya investor.</li>
</ul></div>
<h2>Kesalahan yang Sering Terjadi</h2>
<ul>
<li>Menunjuk KAP hanya dari harga, lalu laporannya tidak diterima investor.</li>
<li>Memakai laporan penilaian agunan untuk merundingkan harga saham.</li>
<li>Menyerahkan laporan keuangan ke investor sebelum diaudit.</li>
</ul>
<h2>Langkah Berikutnya untuk Rumah Sakit di Pontianak</h2>
{rek('Pontianak', 'pontianak', 'pe')}
<p>Lihat juga <a href="/kota/pontianak/kap/">KAP di Pontianak</a> dan <a href="/kota/pontianak/kjpp/">KJPP di Pontianak</a>.</p>
''',
  faq=[('Apakah KAP harus berkantor di Pontianak?', 'Tidak. Yang penting izin, pengalaman, dan penerimaan oleh investor atau bank. Audit dapat dijalankan dengan kerja daring dan kunjungan lapangan.'),
       ('Apa beda penilai properti dan penilai bisnis?', 'Penilai properti menilai tanah, bangunan, dan alat. Penilai bisnis menilai saham atau nilai usaha. Izin dan klasifikasinya berbeda.'),
       ('Apakah rumah sakit milik yayasan bisa menerima investor?', 'Investor ekuitas masuk melalui perseroan terbatas. Rumah sakit milik yayasan perlu menata struktur badan hukumnya lebih dulu bersama konsultan hukum.')])

# ================================================================== CFO
# 7. Sidoarjo
A(site='ca', topik='cfo', kota='Sidoarjo', kota_slug='sidoarjo',
  slug='fractional-cfo-kja-konsultan-pajak-kap-bedanya-sidoarjo',
  seo_title='Fractional CFO, KJA, Konsultan Pajak, KAP: Bedanya',
  title='Fractional CFO, KJA, Konsultan Pajak, atau KAP? Panduan untuk Pabrik dan Gudang di Sidoarjo',
  description='Pemilik pabrik dan gudang di Sidoarjo sering bingung memilih fractional CFO, KJA, konsultan pajak, atau KAP. Ini beda peran, hasil kerja, dan kapan perlu.',
  keyword='fractional cfo sidoarjo', category='CFO Paruh Waktu',
  wa='Halo Pak Ananta, kami perusahaan di Sidoarjo dan bingung perlu fractional CFO, KJA, atau konsultan pajak.',
  sources=[S_PT],
  body_html=f'''
<p>Sidoarjo adalah kawasan industri dan pergudangan penyangga Surabaya. Banyak perusahaan di sini tumbuh dari bengkel atau gudang keluarga menjadi pemasok tetap pabrik besar. Seiring tumbuh, pemilik berurusan dengan makin banyak profesi keuangan, dan sering memakai orang yang salah untuk pekerjaan yang benar.</p>
<h2>Peta Peran</h2>
{tbl(['Profesi', 'Pekerjaan utama', 'Hasil kerja', 'Izin atau register'],
     [['Staf pembukuan', 'Mencatat transaksi harian', 'Jurnal, buku bank, faktur', 'Tidak ada'],
      ['Kantor jasa akuntan (KJA)', 'Menyusun pembukuan dan laporan keuangan, jasa akuntansi manajemen', 'Laporan keuangan sesuai standar', 'Akuntan beregister, izin Menteri Keuangan'],
      ['Konsultan pajak', 'Menghitung, melaporkan pajak, mendampingi pemeriksaan', 'SPT dan surat menyurat pajak', 'Izin praktik konsultan pajak'],
      ['Kantor akuntan publik (KAP)', 'Mengaudit laporan keuangan', 'Laporan auditor independen dengan opini', 'Izin akuntan publik'],
      ['Fractional CFO', 'Mengarahkan keuangan: kas, harga pokok, bank, investasi', 'Proyeksi kas, paket laporan manajemen, rekomendasi keputusan', 'Tidak diatur; dinilai dari kredensial dan pengalaman']])}
<h2>Pertanyaan yang Membedakan</h2>
<ul>
<li>Butuh laporan keuangan yang rapi? Itu pekerjaan KJA.</li>
<li>Butuh pajak dihitung dan dilaporkan dengan benar? Konsultan pajak.</li>
<li>Bank atau prinsipal meminta laporan auditan? KAP.</li>
<li>Butuh seseorang yang membaca semua itu lalu membantu memutuskan harga, utang, dan investasi? Fractional CFO.</li>
</ul>
<h2>Salah Pakai yang Sering Terjadi</h2>
<ol>
<li><b>Konsultan pajak diminta mengurus kredit bank.</b> Laporan untuk pajak dan laporan untuk bank harus sejalan, tetapi cara membaca dan menyajikannya berbeda.</li>
<li><b>Auditor diminta menyusun laporan yang diauditnya.</b> Ini melanggar independensi dan laporan auditnya bisa dipersoalkan.</li>
<li><b>Staf pembukuan diminta menyusun proyeksi untuk investor.</b> Hasilnya jarang bertahan saat diuji.</li>
</ol>
<h2>Kapan Naik Kelas</h2>
{tbl(['Tahap usaha', 'Yang biasanya cukup', 'Yang mulai dibutuhkan'],
     [['Omzet sampai sekitar Rp5 miliar', 'Staf pembukuan dan konsultan pajak', 'KJA untuk laporan tahunan'],
      ['Rp5 miliar sampai Rp50 miliar', 'KJA dan konsultan pajak', 'Fractional CFO saat mengajukan kredit atau ekspansi'],
      ['Di atas Rp50 miliar', 'Tim keuangan internal, KAP, konsultan pajak', 'Fractional CFO rutin, lalu CFO penuh waktu']])}
<p>Batas rupiah di atas hanya patokan kasar. Yang lebih menentukan adalah keputusan yang sedang dihadapi. Perseroan dengan aset atau peredaran usaha minimal Rp50 miliar wajib diaudit menurut UU Perseroan Terbatas.</p>
<h2>Bagaimana Mereka Bekerja Bersama</h2>
<div class="pf-fold"><p>Susunan yang sehat untuk perusahaan menengah di Sidoarjo: KJA menutup buku tiap bulan, konsultan pajak mengurus kepatuhan, KAP mengaudit sekali setahun, dan fractional CFO memimpin rapat angka bulanan, memantau kas dan syarat bank, serta menjadi lawan bicara pemilik untuk keputusan besar.</p>
<p>Fractional CFO yang baik tidak mengambil pekerjaan pihak lain. Ia memastikan semuanya menghasilkan satu set angka yang sama.</p></div>
<h2>Langkah Berikutnya untuk Perusahaan di Sidoarjo</h2>
{rek('Sidoarjo', 'sidoarjo', 'cfo')}
<p>Lihat juga <a href="/kota/sidoarjo/kja/">KJA di Sidoarjo</a> dan <a href="/akuntan-manufaktur/">akuntan untuk usaha manufaktur</a>.</p>
''',
  faq=[('Apakah fractional CFO menggantikan konsultan pajak?', 'Tidak. Konsultan pajak tetap mengurus kepatuhan pajak. Fractional CFO memakai hasilnya untuk keputusan keuangan dan memastikan laporan pajak, bank, dan manajemen sejalan.'),
       ('Apakah fractional CFO perlu izin?', 'Tidak ada izin khusus. Nilai dari kredensial seperti CPA atau CA, pengalaman menjabat di bidang keuangan, dan rekam jejak di industri sejenis.'),
       ('Bisakah KJA merangkap fractional CFO?', 'Bisa bila orangnya punya pengalaman manajemen keuangan. Yang tidak bisa dirangkap adalah auditor, karena harus independen.')])

# 8. Makassar
A(site='ca', topik='cfo', kota='Makassar', kota_slug='makassar',
  slug='memilih-fractional-cfo-makassar-kredensial-kontrak',
  seo_title='Memilih Fractional CFO di Makassar: Kredensial dan Kontrak',
  title='Memilih Fractional CFO di Makassar: Kredensial, Isi Kontrak, dan Ukuran Keberhasilan',
  description='Panduan pemilik usaha di Makassar memilih fractional CFO: kredensial yang dicek, pasal kontrak yang wajib ada, dan ukuran keberhasilan 90 hari pertama.',
  keyword='fractional cfo makassar', category='CFO Paruh Waktu',
  wa='Halo Pak Ananta, kami perusahaan di Makassar dan sedang menimbang fractional CFO. Mohon arahannya.',
  sources=[S_PT],
  body_html=f'''
<p>Makassar adalah gerbang bisnis Indonesia timur: perdagangan, logistik, konstruksi, perikanan, dan properti. Banyak perusahaan di sini sudah beroperasi lintas provinsi, tetapi direktur keuangan berpengalaman tidak mudah dicari, dan yang ada cenderung ditarik ke Jakarta. Fractional CFO menjadi jalan tengah. Karena profesi ini tidak diatur izin, pemilik perlu cara menilai sendiri.</p>
<h2>Kredensial yang Layak Dicek</h2>
<ul>
<li><b>Sertifikasi akuntansi:</b> akuntan publik (CPA) atau akuntan beregister (CA). Bisa dicek ke asosiasi profesinya.</li>
<li><b>Pengalaman jabatan:</b> pernah menjadi direktur keuangan, kepala keuangan, atau auditor senior, bukan hanya konsultan.</li>
<li><b>Pengalaman pendanaan:</b> pernah mengurus kredit bank, investor, atau persiapan penawaran umum.</li>
<li><b>Industri:</b> memahami usaha sejenis. Kontraktor, distributor, dan rumah sakit punya masalah kas yang berbeda.</li>
<li><b>Jaringan kerja:</b> mengenal kantor akuntan publik, penilai, dan bank yang relevan tanpa terikat pada salah satunya.</li>
</ul>
<h2>Pasal yang Wajib Ada di Kontrak</h2>
{tbl(['Pasal', 'Isi yang perlu jelas'],
     [['Ruang lingkup', 'Daftar pekerjaan rutin dan hasil tiap bulan, misalnya laporan manajemen dan proyeksi kas'],
      ['Waktu', 'Jumlah hari per bulan, jadwal rapat, dan waktu tanggap di luar jadwal'],
      ['Kewenangan', 'Apakah boleh mewakili ke bank, menandatangani apa, dan batasnya'],
      ['Kerahasiaan', 'Perlindungan data keuangan, berlaku setelah kontrak berakhir'],
      ['Benturan kepentingan', 'Tidak merangkap auditor perusahaan dan tidak menerima komisi dari bank atau pemasok'],
      ['Biaya', 'Retainer bulanan, biaya perjalanan, dan pekerjaan di luar lingkup'],
      ['Masa dan pengakhiran', 'Masa percobaan tiga bulan dan pemberitahuan pengakhiran'],
      ['Serah terima', 'Semua kertas kerja dan model menjadi milik perusahaan']])}
<h2>Ukuran Keberhasilan 90 Hari</h2>
<ol>
<li>Laporan bulanan selesai paling lambat hari kerja kesepuluh.</li>
<li>Proyeksi kas 13 minggu berjalan dan diperbarui tiap minggu.</li>
<li>Rasio yang dipersyaratkan bank dihitung dan dipantau.</li>
<li>Tiga keputusan besar pemilik didukung perhitungan tertulis.</li>
<li>Daftar perbaikan disusun menurut nilai rupiahnya.</li>
</ol>
<p>Ukuran seperti ini lebih adil daripada target laba, yang dipengaruhi banyak hal di luar kendali CFO.</p>
<h2>Pertanyaan Wawancara</h2>
<div class="pf-fold"><ul>
<li>Ceritakan proyeksi kas terakhir yang Anda susun dan keputusan apa yang berubah karenanya.</li>
<li>Bagaimana Anda membagi waktu antar klien, dan berapa klien yang Anda pegang?</li>
<li>Apa yang Anda kerjakan di bulan pertama?</li>
<li>Kapan Anda akan menyarankan kami merekrut CFO penuh waktu?</li>
<li>Siapa yang membantu Anda, dan siapa yang menggantikan bila Anda berhalangan?</li>
</ul></div>
<h2>Tanda Bahaya</h2>
<ul>
<li>Menjanjikan kredit pasti disetujui atau pajak pasti turun.</li>
<li>Meminta imbalan berupa persentase dari pinjaman tanpa pekerjaan yang jelas.</li>
<li>Tidak mau menuliskan ruang lingkup.</li>
<li>Merangkap sebagai auditor perusahaan Anda.</li>
</ul>
<h2>Langkah Berikutnya untuk Perusahaan di Makassar</h2>
{rek('Makassar', 'makassar', 'cfo')}
''',
  faq=[('Apa kredensial fractional CFO yang baik?', 'Sertifikasi akuntansi seperti CPA atau CA, pengalaman menjabat di bidang keuangan, pengalaman pendanaan, dan pemahaman industri klien.'),
       ('Berapa lama kontrak fractional CFO?', 'Umumnya enam sampai dua belas bulan dengan masa percobaan tiga bulan, lalu diperpanjang sesuai kebutuhan.'),
       ('Apakah fractional CFO bisa bekerja dari luar Makassar?', 'Bisa. Pekerjaan rutin berjalan daring dengan kunjungan berkala untuk rapat direksi dan pertemuan bank.')])

# 9. Pekanbaru
GAJI = 60 * J
FT = GAJI * 13 * 1.2; FR1 = 15 * J * 12; FR2 = 30 * J * 12
WC = 4 * M; HEMAT = WC * .10

A(site='ca', topik='cfo', kota='Pekanbaru', kota_slug='pekanbaru',
  slug='biaya-fractional-cfo-pekanbaru-cara-menghitung-manfaat',
  seo_title='Biaya Fractional CFO di Pekanbaru dan Cara Hitung Manfaat',
  title='Biaya Fractional CFO di Pekanbaru: Cara Menghitung Manfaatnya untuk Usaha Sawit dan Distribusi',
  description='Berapa biaya fractional CFO untuk usaha sawit dan distributor di Pekanbaru, apa penentunya, dan cara menghitung manfaat dibanding merekrut CFO penuh waktu.',
  keyword='biaya fractional cfo', category='CFO Paruh Waktu',
  wa='Halo Pak Ananta, kami perusahaan di Pekanbaru dan ingin tahu biaya serta cakupan fractional CFO.',
  sources=[S_PT],
  body_html=f'''
<p>Pekanbaru adalah pusat bisnis Riau yang digerakkan perkebunan, energi, dan perdagangan. Pemasok pabrik kelapa sawit, pengangkutan, kontraktor, dan distributor barang konsumsi di sini sering beromzet puluhan sampai ratusan miliar rupiah dengan tim keuangan yang ramping. Ketika bank atau pemegang saham mulai meminta laporan yang lebih tajam, muncul pertanyaan: merekrut direktur keuangan, atau cukup yang paruh waktu?</p>
<h2>Apa yang Menentukan Biaya</h2>
<ul>
<li><b>Jumlah badan usaha.</b> Satu perseroan berbeda dengan grup lima perseroan.</li>
<li><b>Kondisi pembukuan.</b> Bila laporan bulanan belum ada, bulan pertama lebih berat.</li>
<li><b>Agenda khusus.</b> Pengajuan kredit besar, masuknya investor, atau sengketa menambah jam kerja.</li>
<li><b>Frekuensi hadir.</b> Dua hari sebulan berbeda dengan empat hari.</li>
<li><b>Tim pendukung.</b> Apakah CFO bekerja sendiri atau membawa analis.</li>
</ul>
<p>Sebagai gambaran, rekanan kami menawarkan retainer CFO paruh waktu untuk perusahaan lokal mulai Rp15 juta per bulan, menyesuaikan cakupan.</p>
<h2>Perbandingan dengan CFO Penuh Waktu</h2>
<p>Ilustrasi dengan angka contoh. Gaji CFO penuh waktu diandaikan {jt(GAJI)} per bulan, dibayar 13 kali setahun, ditambah 20 persen untuk tunjangan, jaminan sosial, dan bonus.</p>
{tbl(['Pilihan', 'Dasar hitung', 'Biaya setahun'],
     [['CFO penuh waktu', f'{jt(GAJI)} x 13 x 1,2', jt(FT)],
      ['Fractional CFO, cakupan dasar', 'Rp15 juta x 12', jt(FR1)],
      ['Fractional CFO, cakupan lebih luas', 'Rp30 juta x 12', jt(FR2)]])}
<p>Selisihnya besar, tetapi perbandingan yang jujur juga melihat sisi lain: CFO penuh waktu hadir setiap hari dan memimpin tim. Fractional CFO cocok selama kebutuhan itu belum ada.</p>
<h2>Menghitung Manfaat, Bukan Hanya Biaya</h2>
<p>Cara paling sederhana adalah mendaftar keputusan yang akan dibantu dan menaksir nilainya. Contoh untuk distributor: menurunkan modal kerja yang terikat di stok dan piutang sebesar {jt(WC)} menghemat bunga {jt(HEMAT)} setahun pada bunga 10 persen. Itu saja sudah melampaui retainer cakupan dasar {jt(FR1)}.</p>
<p>Sumber manfaat lain yang biasa muncul:</p>
<ul>
<li>Bunga dan biaya bank yang lebih baik setelah laporan dan rasio tertata.</li>
<li>Denda dan koreksi pajak yang terhindar karena laporan pajak dan laporan keuangan sejalan.</li>
<li>Proyek atau cabang rugi yang dihentikan lebih cepat.</li>
<li>Harga jual yang dikoreksi setelah harga pokok dihitung ulang.</li>
</ul>
<h2>Khusus Usaha di Rantai Sawit</h2>
<div class="pf-fold"><ul>
<li>Harga komoditas bergerak cepat. Proyeksi kas perlu skenario harga, bukan satu angka.</li>
<li>Pemasok tandan buah segar dan pengangkut sering dibayar tunai sementara pabrik membayar bertermin. Selisih waktu itu harus dibiayai.</li>
<li>Alat angkut dan alat berat dibiayai utang dengan angsuran tetap.</li>
<li>Grup keluarga dengan kebun, pabrik, dan transportasi di perseroan berbeda butuh laporan konsolidasian.</li>
</ul></div>
<h2>Kapan Belum Perlu</h2>
<p>Bila pembukuan masih berantakan dan belum ada keputusan besar di depan mata, dana lebih baik dipakai untuk merapikan laporan keuangan lebih dulu bersama kantor jasa akuntan. Fractional CFO baru terasa nilainya setelah ada angka yang bisa dipercaya.</p>
<h2>Langkah Berikutnya untuk Perusahaan di Pekanbaru</h2>
{rek('Pekanbaru', 'pekanbaru', 'cfo')}
''',
  faq=[('Berapa biaya fractional CFO?', 'Bergantung pada cakupan, jumlah badan usaha, dan frekuensi hadir. Rekanan kami menawarkan retainer mulai Rp15 juta per bulan untuk perusahaan lokal.'),
       ('Apakah fractional CFO lebih hemat daripada CFO penuh waktu?', 'Dari sisi biaya tunai ya. Namun pilihan ditentukan kebutuhan: bila perusahaan butuh kehadiran harian, CFO penuh waktu lebih tepat.'),
       ('Bagaimana mengukur manfaatnya?', 'Daftar keputusan yang dibantu dan taksir nilainya: bunga yang dihemat, koreksi pajak yang terhindar, kerugian yang dihentikan, dan margin yang diperbaiki.')])

# 10. Samarinda
Q = ['Laporan keuangan bulanan selesai setelah tanggal 20 atau tidak ada', 'Saldo kas tiga bulan ke depan tidak bisa diperkirakan',
     'Laba per proyek baru diketahui setelah proyek selesai', 'Syarat rasio dari bank belum pernah dihitung sendiri',
     'Pemilik menandatangani semua pembayaran', 'Laporan untuk pajak dan untuk bank menunjukkan angka berbeda',
     'Ada rencana menambah alat atau proyek besar dalam 12 bulan', 'Ada lebih dari satu badan usaha tanpa laporan gabungan']

A(site='ca', topik='cfo', kota='Samarinda', kota_slug='samarinda',
  slug='tanda-kontraktor-samarinda-butuh-fractional-cfo',
  seo_title='Delapan Tanda Kontraktor Samarinda Butuh Fractional CFO',
  title='Delapan Tanda Kontraktor dan Usaha Tambang di Samarinda Sudah Butuh Fractional CFO',
  description='Daftar periksa delapan tanda untuk kontraktor dan usaha penunjang tambang di Samarinda: kapan cukup pembukuan dan kapan sudah perlu fractional CFO.',
  keyword='fractional cfo samarinda', category='CFO Paruh Waktu',
  wa='Halo Pak Ananta, kami kontraktor di Samarinda. Setelah mengisi daftar periksa, sepertinya kami butuh fractional CFO.',
  sources=[S_PT],
  body_html=f'''
<p>Samarinda adalah pusat bisnis batu bara Kalimantan Timur. Kontraktor jasa pertambangan, penyewaan alat, angkutan, dan perdagangan suku cadang hidup dari kontrak yang nilainya besar dan pembayarannya bertermin. Pembangunan Ibu Kota Nusantara menambah peluang sekaligus kebutuhan modal. Dalam usaha seperti ini, masalah keuangan jarang datang sebagai kejutan. Tandanya sudah ada, hanya tidak dibaca.</p>
<h2>Daftar Periksa Delapan Tanda</h2>
<p>Beri nilai 1 untuk setiap pernyataan yang sesuai dengan kondisi perusahaan Anda.</p>
{tbl(['No', 'Pernyataan'], [[str(i + 1), q] for i, q in enumerate(Q)])}
<h2>Membaca Hasilnya</h2>
{tbl(['Jumlah nilai', 'Artinya', 'Langkah yang disarankan'],
     [['0 sampai 2', 'Fungsi keuangan berjalan', 'Pertahankan, tinjau tiap tahun'],
      ['3 sampai 4', 'Mulai ada celah', 'Rapikan pembukuan dan laporan bersama kantor jasa akuntan'],
      ['5 sampai 6', 'Keputusan sudah berisiko', 'Fractional CFO untuk enam sampai dua belas bulan'],
      ['7 sampai 8', 'Rawan masalah kas dan bank', 'Fractional CFO segera, mulai dari proyeksi kas dan syarat bank']])}
<h2>Kenapa Tanda Itu Penting bagi Kontraktor</h2>
<ul>
<li><b>Laporan terlambat</b> berarti masalah proyek baru terlihat setelah uangnya habis.</li>
<li><b>Kas tidak bisa diperkirakan</b> berarti angsuran alat dan gaji bergantung pada satu termin.</li>
<li><b>Laba per proyek tidak diketahui</b> berarti harga penawaran berikutnya hanya tebakan.</li>
<li><b>Syarat bank tidak dipantau</b> berarti pelanggaran baru ketahuan saat tinjauan tahunan.</li>
</ul>
<h2>Yang Dikerjakan Lebih Dulu</h2>
<ol>
<li>Proyeksi kas 13 minggu per proyek.</li>
<li>Laba rugi per proyek dan per unit alat.</li>
<li>Perhitungan rasio yang diperjanjikan dengan bank, termasuk DSCR.</li>
<li>Kalender tutup buku bulanan.</li>
<li>Kebijakan kewenangan pembayaran agar pemilik tidak menjadi leher botol.</li>
</ol>
<h2>Bedakan dengan Kebutuhan Lain</h2>
<div class="pf-fold"><ul>
<li>Bila yang diminta pelanggan adalah laporan auditan untuk prakualifikasi tender, yang dibutuhkan kantor akuntan publik.</li>
<li>Bila masalahnya pemeriksaan pajak, yang dibutuhkan konsultan pajak.</li>
<li>Bila pembukuan belum ada, mulai dari kantor jasa akuntan.</li>
<li>Fractional CFO dibutuhkan ketika semua itu sudah ada tetapi keputusan tetap sulit diambil.</li>
</ul>
<p>Perseroan dengan aset atau peredaran usaha minimal Rp50 miliar wajib diaudit menurut UU Perseroan Terbatas, dan banyak kontraktor di Samarinda sudah melewati batas itu.</p></div>
<h2>Langkah Berikutnya untuk Perusahaan di Samarinda</h2>
{rek('Samarinda', 'samarinda', 'cfo')}
<p>Lihat juga <a href="/akuntan-kontraktor/">akuntan untuk kontraktor</a> dan <a href="/kota/samarinda/kap/">KAP di Samarinda</a>.</p>
''',
  faq=[('Kapan kontraktor butuh fractional CFO?', 'Ketika laporan terlambat, kas sulit diperkirakan, laba per proyek tidak diketahui, dan syarat bank tidak dipantau, sementara ada rencana menambah alat atau proyek besar.'),
       ('Apakah fractional CFO sama dengan konsultan keuangan lepas?', 'Fractional CFO bekerja rutin dengan ruang lingkup tetap dan ikut bertanggung jawab atas mutu angka. Konsultan lepas biasanya mengerjakan satu proyek lalu selesai.'),
       ('Apa yang dikerjakan di bulan pertama?', 'Membaca laporan dan perjanjian kredit, memetakan kas, lalu menyusun proyeksi kas 13 minggu dan kalender tutup buku.')])
