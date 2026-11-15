# -*- coding: utf-8 -*-
"""UpdateSAK: 10 artikel daerah. Sudut: standar dan perhitungan teknis (edukasi), lalu dibantu tim FA Indonesia.
Link internal US relatif (/psak/<no>/, /kertas-kerja/), link FA absolut. Field 'psak' = chip Standar Terkait."""
from _k import A, n, rp, jt, pct, tbl

FA = 'https://faindonesia.co.id'
M = 1e9; J = 1e6
S_SAK = ('IAI: SAK Online', 'https://web.iaiglobal.or.id/SAK-Online')
S_NOM = ('IAI: Perubahan Penomoran PSAK dan ISAK dalam SAK Indonesia', 'https://web.iaiglobal.or.id/assets/files/file_publikasi/Perubahan_Penomoran_PSAK_ISAK_dalam_SAK_Indonesia.pdf')
S_JKN = ('ANTARA: Kemenkes Uji Coba Reformasi JKN di Muara Enim (Oktober 2026)', 'https://www.antaranews.com/berita/5771342/kemenkes-uji-coba-reformasi-jkn-di-muara-enim-pangkas-waktu-tunggu')
S_HBR = ('Kaplan dan Anderson, Time-Driven Activity-Based Costing, Harvard Business Review (November 2004)', 'https://hbr.org/2004/11/time-driven-activity-based-costing')


def bantu(kota, slug, topik):
    t = {'abc': (f'{FA}/konsultan-unit-cost-rumah-sakit/{slug}/', f'konsultan unit cost rumah sakit di {kota}'),
         'pe': (f'{FA}/pendanaan-rumah-sakit/{slug}/', f'pendampingan pendanaan rumah sakit di {kota}'),
         'cfo': (f'{FA}/cfo-paruh-waktu/', 'layanan CFO paruh waktu')}[topik]
    return (f'<p>Sudah paham konsepnya tetapi belum sempat mengerjakan sendiri? Perhitungan seperti di artikel ini dikerjakan tim FA Indonesia untuk perusahaan di {kota} dan kota lain. '
            f'Lihat <a href="{t[0]}">{t[1]}</a> atau <a href="{FA}/wilayah/{slug}/">layanan FA Indonesia di {kota}</a>.</p>')


# ================================================================== ABC
# 1. Malang: lima tabel kerja
RES = [('Gaji perawat dan staf', 600), ('Penyusutan gedung dan alat', 240), ('Listrik, air, dan kebersihan', 120), ('Bahan umum dan administrasi', 90), ('Sistem informasi', 50)]
ACT = ['Pendaftaran dan kasir', 'Layanan poliklinik', 'Rawat inap', 'Laboratorium']
PCT = [(15, 30, 40, 15), (5, 25, 45, 25), (10, 20, 50, 20), (40, 20, 30, 10), (40, 20, 20, 20)]
ALLOC = [[c * p / 100 for p in ps] for (_, c), ps in zip(RES, PCT)]
POOL = [sum(r[i] for r in ALLOC) for i in range(4)]
DRV = [('kunjungan', 8500), ('menit layanan poli', 73000), ('hari rawat', 1780), ('pemeriksaan', 9650)]
RT = [POOL[i] * J / DRV[i][1] for i in range(4)]
OBJ = [('Konsultasi poli umum', (1, 10, 0, 0), 45e3), ('Tindakan kecil poli bedah', (1, 35, 0, 1), 150e3), ('Rawat inap demam berdarah, 4 hari', (1, 20, 4, 6), 1.4e6)]
o_rows = []
for nm, use, d in OBJ:
    oh = sum(u * r for u, r in zip(use, RT))
    o_rows.append([nm] + [rp(u * r) for u, r in zip(use, RT)] + [rp(oh), rp(d), rp(oh + d)])

A(site='us', topik='abc', kota='Malang', kota_slug='malang',
  slug='contoh-perhitungan-activity-based-costing-rumah-sakit',
  seo_title='Contoh Perhitungan Activity Based Costing Rumah Sakit',
  title='Contoh Perhitungan Activity Based Costing Rumah Sakit: Lima Tabel Kerja dari Biaya sampai Unit Cost',
  description='Contoh perhitungan activity based costing rumah sakit dalam lima tabel kerja: sumber daya, aktivitas, tarif aktivitas, dan unit cost layanan.',
  keyword='contoh perhitungan activity based costing rumah sakit', category='Akuntansi Manajemen', psak=['202', '216'],
  wa='Halo Pak Ananta, saya membaca contoh perhitungan ABC rumah sakit di UpdateSAK dan ingin dibantu menerapkannya di rumah sakit kami di Malang.',
  sources=[S_HBR, ('Permenkes Nomor 3 Tahun 2023 tentang Standar Tarif Pelayanan Kesehatan dalam Penyelenggaraan Program JKN', 'https://peraturan.bpk.go.id/Details/275518')],
  body_html=f'''
<p>Activity based costing (ABC) membebankan biaya ke layanan dalam dua tahap: dari sumber daya ke aktivitas, lalu dari aktivitas ke layanan. Konsepnya mudah, tetapi banyak mahasiswa dan staf keuangan rumah sakit tersendat saat harus menuangkannya ke lembar kerja. Artikel ini memperlihatkan lima tabel kerja dengan angka contoh untuk rumah sakit kecil, seperti banyak rumah sakit dan klinik utama di Malang Raya. Semua angka biaya per bulan dalam jutaan rupiah kecuali disebut lain.</p>
<h2>Tabel 1: Biaya Sumber Daya</h2>
<p>Mulai dari buku besar. Kumpulkan biaya tidak langsung, yaitu biaya yang tidak bisa ditelusuri ke pasien tertentu. Obat, bahan medis habis pakai, dan jasa medis tidak masuk karena ditelusuri langsung.</p>
{tbl(['Sumber daya', 'Biaya per bulan (Rp juta)'], [[a, n(c)] for a, c in RES], ['Jumlah', n(sum(c for _, c in RES))])}
<h2>Tabel 2: Dari Sumber Daya ke Aktivitas</h2>
<p>Setiap sumber daya dibagi ke aktivitas dengan pemicu sumber daya. Gaji dibagi menurut proporsi waktu pegawai, penyusutan menurut lokasi aset, listrik menurut luas dan daya, dan seterusnya. Persentase di bawah adalah hasil pemetaan itu.</p>
{tbl(['Sumber daya'] + ACT, [[RES[i][0]] + [f'{PCT[i][k]}% = {n(ALLOC[i][k])}' for k in range(4)] for i in range(5)],
     ['Biaya aktivitas'] + [n(p) for p in POOL])}
<p>Uji pertama: jumlah biaya aktivitas {' + '.join(n(p) for p in POOL)} = {n(sum(POOL))}, sama dengan jumlah Tabel 1. Bila tidak sama, ada sumber daya yang persentasenya tidak berjumlah 100.</p>
<h2>Tabel 3: Tarif Aktivitas</h2>
<p>Tiap aktivitas diberi satu pemicu yang volumenya tersedia di sistem informasi rumah sakit.</p>
{tbl(['Aktivitas', 'Biaya aktivitas (Rp juta)', 'Pemicu aktivitas', 'Volume per bulan', 'Tarif aktivitas'],
     [[ACT[i], n(POOL[i]), DRV[i][0], n(DRV[i][1]), rp(RT[i])] for i in range(4)])}
<h2>Tabel 4: Pembebanan ke Layanan</h2>
<p>Setiap layanan dibebani sebesar aktivitas yang dikonsumsinya. Rawat inap demam berdarah empat hari, misalnya, memakai satu kunjungan pendaftaran, 20 menit layanan poli atau gawat darurat, empat hari rawat, dan enam pemeriksaan laboratorium.</p>
{tbl(['Layanan'] + ACT + ['Biaya tidak langsung', 'Biaya langsung', 'Unit cost'], o_rows)}
<h2>Tabel 5: Rekonsiliasi</h2>
<p>Langkah yang paling sering dilewati. Kalikan unit cost dengan volume setiap layanan, jumlahkan, lalu cocokkan dengan total biaya di laporan laba rugi.</p>
{tbl(['Uji', 'Cara', 'Hasil yang diharapkan'],
     [['Tahap 1', 'Jumlah biaya aktivitas dibanding jumlah biaya sumber daya', 'Sama'],
      ['Tahap 2', 'Tarif aktivitas x volume pemicu, dijumlahkan seluruh aktivitas', 'Sama dengan jumlah biaya aktivitas'],
      ['Buku besar', 'Biaya tidak langsung + biaya langsung seluruh layanan dibanding total beban', 'Selisih dijelaskan, misalnya kapasitas menganggur']])}
<p>Selisih pada uji ketiga bukan kesalahan selama bisa dijelaskan. Penyebab yang sah adalah kapasitas menganggur dan layanan yang belum dihitung.</p>
<h2>Catatan untuk Laporan Keuangan</h2>
<div class="pf-fold"><p>Unit cost adalah alat akuntansi manajemen dan tidak mengubah angka laporan keuangan. Namun dua hal bersinggungan dengan standar:</p>
<ul>
<li>Persediaan farmasi diukur menurut PSAK 202 pada nilai yang lebih rendah antara biaya perolehan dan nilai realisasi neto. Biaya perolehan yang dipakai di unit cost harus sama dengan catatan persediaan.</li>
<li>Penyusutan alat mengikuti PSAK 216. Umur manfaat di daftar aset menentukan besarnya biaya kapasitas yang masuk ke Tabel 1.</li>
</ul></div>
<h2>Kesalahan Umum</h2>
<ul>
<li>Memasukkan jasa medis ke biaya tidak langsung.</li>
<li>Memakai jumlah pasien sebagai pemicu semua aktivitas, sehingga hasilnya sama dengan rata-rata biasa.</li>
<li>Tidak membedakan menit layanan antar jenis tindakan.</li>
<li>Menghitung sekali dan tidak memperbarui saat gaji atau volume berubah.</li>
</ul>
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Malang', 'malang', 'abc')}
<p>Kertas kerja siap pakai untuk standar lain tersedia di halaman <a href="/kertas-kerja/">Kertas Kerja</a>, dan ringkasan akuntansi khas rumah sakit ada di <a href="/akuntansi-rumah-sakit/">Akuntansi Rumah Sakit</a>.</p>
''',
  faq=[('Apa dua tahap dalam activity based costing?', 'Tahap pertama membebankan biaya sumber daya ke aktivitas dengan pemicu sumber daya. Tahap kedua membebankan biaya aktivitas ke layanan dengan pemicu aktivitas.'),
       ('Apakah obat dan jasa medis masuk ke pool biaya ABC?', 'Tidak. Keduanya biaya langsung yang ditelusuri ke pasien, lalu ditambahkan ke biaya tidak langsung hasil ABC untuk mendapat unit cost.'),
       ('Bagaimana menguji hasil perhitungan ABC?', 'Dengan rekonsiliasi: jumlah biaya aktivitas harus sama dengan jumlah biaya sumber daya, dan total biaya seluruh layanan dicocokkan dengan beban di laporan laba rugi.')])

# 2. Surakarta: tiga metode alokasi
AD, LA, RI, RJ = 400.0, 200.0, 900.0, 500.0
# dasar alokasi: Adm (pegawai) -> Laundry 10, RI 60, RJ 30 ; Laundry (kg) -> Adm 5, RI 85, RJ 10
s_ri = RI + AD * 60 / 90 + LA * 85 / 95; s_rj = RJ + AD * 30 / 90 + LA * 10 / 95
sd_l = LA + AD * .10; sd_ri = RI + AD * .60 + sd_l * 85 / 95; sd_rj = RJ + AD * .30 + sd_l * 10 / 95
d_ad = LA * .05; d_la = AD * .10
dd_ri = RI + AD * .60 + LA * .85 + d_ad * 60 / 90 + d_la * 85 / 95; dd_rj = RJ + AD * .30 + LA * .10 + d_ad * 30 / 90 + d_la * 10 / 95

A(site='us', topik='abc', kota='Surakarta', kota_slug='surakarta',
  slug='step-down-double-distribution-activity-based-costing-perbandingan',
  seo_title='Step-Down, Double Distribution, dan ABC: Perbandingan Angka',
  title='Step-Down, Double Distribution, dan Activity Based Costing: Perbandingan dengan Angka yang Sama',
  description='Tiga metode alokasi biaya rumah sakit dihitung dengan data yang sama: distribusi sederhana, step-down, dan double distribution, lalu kapan perlu ABC.',
  keyword='step down double distribution activity based costing', category='Akuntansi Manajemen', psak=['202', '216'],
  wa='Halo Pak Ananta, saya membaca perbandingan metode alokasi biaya di UpdateSAK dan ingin diskusi metode yang tepat untuk rumah sakit kami di Solo.',
  sources=[S_HBR],
  body_html=f'''
<p>Rumah sakit di Solo Raya, seperti di kota lain, paling sering memakai double distribution untuk menghitung unit cost. Pertanyaan yang selalu muncul di kelas dan di ruang rapat sama: seberapa jauh hasilnya berbeda dari metode lain, dan kapan perlu pindah ke activity based costing (ABC)? Cara paling jelas menjawabnya adalah menghitung tiga metode dengan data yang sama.</p>
<h2>Data Contoh</h2>
<p>Dua unit penunjang dan dua unit produksi, biaya langsung per bulan dalam jutaan rupiah.</p>
{tbl(['Unit', 'Biaya langsung', 'Dasar alokasi keluar'],
     [['Administrasi (penunjang)', n(AD), 'Jumlah pegawai: laundry dan gizi 10%, rawat inap 60%, rawat jalan 30%'],
      ['Laundry dan gizi (penunjang)', n(LA), 'Kilogram dan porsi: administrasi 5%, rawat inap 85%, rawat jalan 10%'],
      ['Rawat inap (produksi)', n(RI), ''], ['Rawat jalan (produksi)', n(RJ), '']], ['Jumlah', n(AD + LA + RI + RJ), ''])}
<h2>Metode 1: Distribusi Sederhana</h2>
<p>Biaya penunjang langsung dibagi ke unit produksi, layanan antar penunjang diabaikan. Administrasi dibagi 60 banding 30, laundry 85 banding 10.</p>
<ul>
<li>Rawat inap = {n(RI)} + {n(AD * 60 / 90, 2)} + {n(LA * 85 / 95, 2)} = <b>{n(s_ri, 2)}</b></li>
<li>Rawat jalan = {n(RJ)} + {n(AD * 30 / 90, 2)} + {n(LA * 10 / 95, 2)} = <b>{n(s_rj, 2)}</b></li>
</ul>
<h2>Metode 2: Step-Down</h2>
<p>Unit penunjang dialokasikan berurutan, dimulai dari yang paling banyak melayani unit lain. Administrasi lebih dulu, termasuk ke laundry. Laundry lalu membagi biayanya yang sudah bertambah menjadi {n(sd_l)} hanya ke unit produksi.</p>
<ul>
<li>Rawat inap = {n(RI)} + {n(AD * .6)} + {n(sd_l * 85 / 95, 2)} = <b>{n(sd_ri, 2)}</b></li>
<li>Rawat jalan = {n(RJ)} + {n(AD * .3)} + {n(sd_l * 10 / 95, 2)} = <b>{n(sd_rj, 2)}</b></li>
</ul>
<h2>Metode 3: Double Distribution</h2>
<p>Distribusi pertama: setiap unit penunjang membagi biayanya ke semua unit lain, termasuk sesama penunjang. Administrasi menerima {n(d_ad)} dari laundry, laundry menerima {n(d_la)} dari administrasi. Distribusi kedua: biaya yang diterima unit penunjang itu dibagi ke unit produksi saja.</p>
<ul>
<li>Rawat inap = {n(RI)} + {n(AD * .6)} + {n(LA * .85)} + {n(d_ad * 60 / 90, 2)} + {n(d_la * 85 / 95, 2)} = <b>{n(dd_ri, 2)}</b></li>
<li>Rawat jalan = {n(RJ)} + {n(AD * .3)} + {n(LA * .1)} + {n(d_ad * 30 / 90, 2)} + {n(d_la * 10 / 95, 2)} = <b>{n(dd_rj, 2)}</b></li>
</ul>
<h2>Hasil Berdampingan</h2>
{tbl(['Metode', 'Rawat inap', 'Rawat jalan', 'Jumlah'],
     [['Distribusi sederhana', n(s_ri, 2), n(s_rj, 2), n(s_ri + s_rj)], ['Step-down', n(sd_ri, 2), n(sd_rj, 2), n(sd_ri + sd_rj)],
      ['Double distribution', n(dd_ri, 2), n(dd_rj, 2), n(dd_ri + dd_rj)]])}
<p>Jumlahnya selalu {n(AD + LA + RI + RJ)}: alokasi hanya memindahkan biaya, tidak menambah. Selisih terbesar antar metode pada rawat inap hanya {n(max(s_ri, sd_ri, dd_ri) - min(s_ri, sd_ri, dd_ri), 2)} atau {pct((max(s_ri, sd_ri, dd_ri) - min(s_ri, sd_ri, dd_ri)) / dd_ri, 1)}.</p>
<p>Pelajarannya: perdebatan soal metode alokasi antar unit sering berlebihan. Ketiganya berhenti di tingkat unit. Kesalahan yang jauh lebih besar terjadi di langkah berikutnya, ketika biaya unit dibagi rata ke semua layanan di dalamnya.</p>
<h2>Di Mana Activity Based Costing Mengambil Alih</h2>
<p>Ambil rawat inap dengan biaya {n(dd_ri, 2)} juta dan 3.000 hari rawat. Cara rata-rata memberi {rp(dd_ri * J / 3000)} per hari rawat untuk semua pasien. ABC memecah biaya itu menjadi aktivitas, misalnya asuhan keperawatan, visite, dan administrasi pasien, masing-masing dengan pemicunya. Pasien pascabedah yang butuh jam perawat tiga kali lipat akan menanggung biaya lebih besar daripada pasien observasi.</p>
<div class="pf-fold"><p>Urutan yang masuk akal bagi rumah sakit yang baru mulai:</p>
<ol>
<li>Pakai double distribution untuk mendapat biaya per unit produksi yang sudah memuat biaya penunjang.</li>
<li>Terapkan ABC di dalam unit yang layanannya paling beragam: kamar operasi, rawat inap, laboratorium, radiologi.</li>
<li>Untuk unit yang biayanya didominasi kapasitas, pertimbangkan time-driven ABC yang memakai menit sebagai pemicu.</li>
</ol></div>
<h2>Memilih Metode Menurut Keputusan</h2>
{tbl(['Keputusan', 'Metode yang memadai'],
     [['Anggaran dan evaluasi kinerja unit', 'Step-down atau double distribution'],
      ['Tarif kamar dan tarif poli', 'Double distribution'],
      ['Tarif tindakan dan paket layanan', 'Activity based costing'],
      ['Margin per kelompok kasus JKN', 'Activity based costing berbasis clinical pathway'],
      ['Jadwal dan kapasitas kamar operasi', 'Time-driven ABC']])}
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Surakarta', 'surakarta', 'abc')}
<p>Lihat juga contoh lima tabel kerja di artikel <a href="/artikel/contoh-perhitungan-activity-based-costing-rumah-sakit/">contoh perhitungan activity based costing rumah sakit</a>.</p>
''',
  faq=[('Apa beda step-down dan double distribution?', 'Step-down mengalokasikan unit penunjang secara berurutan dan unit yang sudah dialokasikan tidak menerima biaya lagi. Double distribution membagi biaya tiap unit penunjang ke semua unit lain lebih dulu, lalu membagi sisa di unit penunjang ke unit produksi.'),
       ('Metode mana yang paling akurat?', 'Di tingkat unit, hasil ketiganya biasanya berdekatan. Ketelitian di tingkat layanan lebih ditentukan apakah biaya unit dibagi rata atau dibebankan dengan activity based costing.'),
       ('Apakah total biaya berubah karena metode alokasi?', 'Tidak. Alokasi hanya memindahkan biaya dari unit penunjang ke unit produksi. Jumlah sebelum dan sesudah harus sama.')])

# 3. Bandung: kapasitas menganggur
FX = 180 * J; KN = 600; VOLS = [420, 380, 340]
RTN = FX / KN

A(site='us', topik='abc', kota='Bandung', kota_slug='bandung',
  slug='kapasitas-menganggur-unit-cost-kapasitas-normal-psak-202',
  seo_title='Kapasitas Menganggur dalam Unit Cost dan PSAK 202',
  title='Kapasitas Menganggur dalam Unit Cost: Prinsip Kapasitas Normal PSAK 202 dan Penerapannya di Rumah Sakit',
  description='Biaya tetap dibagi kapasitas normal, bukan volume aktual. Ini prinsip PSAK 202, contoh hitung biaya kapasitas menganggur, dan penerapannya di rumah sakit.',
  keyword='kapasitas menganggur unit cost', category='Akuntansi Manajemen', psak=['202', '216', '236'],
  wa='Halo Pak Ananta, saya membaca artikel kapasitas menganggur di UpdateSAK dan ingin diskusi penerapannya di perusahaan kami di Bandung.',
  sources=[S_SAK, S_NOM, S_JKN],
  body_html=f'''
<p>Kota Bandung termasuk lokasi uji coba reformasi JKN yang diumumkan Kemenkes pada 2026. Ketika pembayaran makin mengikuti kompleksitas kasus, rumah sakit perlu unit cost yang tidak ikut naik turun bersama jumlah pasien. Kuncinya ada pada satu prinsip yang sudah lama dikenal di akuntansi persediaan: biaya tetap dialokasikan berdasarkan kapasitas normal.</p>
<h2>Prinsip Kapasitas Normal dalam PSAK 202</h2>
<p>PSAK 202 Persediaan (dulu PSAK 14) mengatur bahwa overhead produksi tetap dialokasikan ke biaya konversi berdasarkan kapasitas normal fasilitas produksi. Kapasitas normal adalah produksi rata-rata yang diharapkan tercapai selama beberapa periode dalam keadaan normal, setelah memperhitungkan pemeliharaan terencana.</p>
<p>Dua akibatnya:</p>
<ul>
<li>Bila produksi rendah atau pabrik menganggur, overhead tetap per unit tidak dinaikkan. Overhead yang tidak teralokasi diakui sebagai beban pada periode terjadinya.</li>
<li>Bila produksi luar biasa tinggi, overhead tetap per unit diturunkan agar persediaan tidak diukur di atas biayanya.</li>
</ul>
<p>Standar ini berlaku untuk persediaan, jadi wajib bagi pabrik. Jasa rumah sakit bukan persediaan, tetapi logikanya dipakai penuh dalam akuntansi manajemen, termasuk time-driven activity based costing.</p>
<h2>Contoh: CT Scan dengan Volume yang Menurun</h2>
<p>Ilustrasi dengan angka contoh. Biaya tetap unit CT scan (penyusutan atau sewa alat, radiografer, pemeliharaan, ruang) {jt(FX)} per bulan. Kapasitas normal {n(KN)} pemeriksaan per bulan. Tarif alokasi biaya tetap = {jt(FX)} / {n(KN)} = {rp(RTN)} per pemeriksaan.</p>
{tbl(['Bulan', 'Volume aktual', 'Biaya tetap per pemeriksaan bila dibagi volume aktual', 'Biaya tetap per pemeriksaan pada kapasitas normal', 'Biaya kapasitas menganggur'],
     [[f'Bulan {i + 1}', n(v), rp(FX / v), rp(RTN), jt((KN - v) * RTN)] for i, v in enumerate(VOLS)])}
<p>Kolom ketiga memperlihatkan bahaya membagi dengan volume aktual. Volume turun, unit cost naik. Bila tarif ikut dinaikkan mengikuti unit cost itu, pasien makin berkurang dan unit cost naik lagi. Lingkaran ini dikenal sebagai spiral kematian.</p>
<p>Dengan kapasitas normal, biaya per pemeriksaan tetap {rp(RTN)}. Masalahnya muncul di tempat yang benar: baris biaya kapasitas menganggur yang membesar dari {jt((KN - VOLS[0]) * RTN)} menjadi {jt((KN - VOLS[2]) * RTN)}. Itu sinyal bagi manajemen untuk mencari rujukan, menata jadwal, atau meninjau ulang investasi, bukan untuk menaikkan tarif.</p>
<h2>Menentukan Kapasitas Normal dan Praktis</h2>
{tbl(['Istilah', 'Pengertian', 'Dipakai untuk'],
     [['Kapasitas teoretis', 'Semua jam tersedia tanpa jeda', 'Batas atas, jarang dipakai'],
      ['Kapasitas praktis', 'Kapasitas teoretis dikurangi jeda, pemeliharaan, dan libur, sering 80 sampai 85 persen', 'Time-driven ABC, keputusan tarif'],
      ['Kapasitas normal', 'Rata-rata yang diharapkan beberapa periode dalam keadaan normal', 'Pengukuran persediaan menurut PSAK 202'],
      ['Volume aktual', 'Yang benar-benar terjadi', 'Menghitung kapasitas menganggur']])}
<h2>Penerapan pada Pabrik: Jurnal Singkat</h2>
<div class="pf-fold"><p>Banyak pembaca di Bandung bekerja di tekstil dan garmen, jadi berikut versi pabriknya. Overhead tetap {jt(FX)}, kapasitas normal {n(KN)} unit, produksi aktual {n(VOLS[0])} unit.</p>
<ul>
<li>Overhead tetap yang masuk ke persediaan = {n(VOLS[0])} x {rp(RTN)} = {jt(VOLS[0] * RTN)}.</li>
<li>Overhead tetap yang tidak teralokasi = {jt(FX)} dikurangi {jt(VOLS[0] * RTN)} = {jt(FX - VOLS[0] * RTN)}, diakui sebagai beban periode berjalan.</li>
</ul>
<p>Jurnalnya: debit persediaan barang dalam proses {jt(VOLS[0] * RTN)}, debit beban overhead tidak teralokasi {jt(FX - VOLS[0] * RTN)}, kredit overhead pabrik {jt(FX)}. Auditor akan memeriksa apakah kapasitas normal yang dipakai masuk akal dan konsisten dari tahun ke tahun.</p></div>
<h2>Kaitan dengan Standar Lain</h2>
<ul>
<li><b>PSAK 216 Aset Tetap:</b> penyusutan tetap diakui meski aset menganggur, kecuali metode penyusutannya berbasis pemakaian.</li>
<li><b>PSAK 236 Penurunan Nilai Aset:</b> kapasitas menganggur yang berkepanjangan adalah indikasi penurunan nilai yang perlu diuji.</li>
</ul>
<h2>Cara Melaporkannya ke Direksi</h2>
<ul>
<li>Sajikan utilisasi tiap unit terhadap kapasitas praktis setiap bulan.</li>
<li>Tampilkan biaya kapasitas menganggur dalam rupiah sebagai baris tersendiri.</li>
<li>Bedakan penyebabnya: permintaan kurang, jadwal tidak merata, atau kapasitas memang berlebih.</li>
<li>Jangan memasukkannya ke unit cost yang dipakai untuk tarif.</li>
</ul>
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Bandung', 'bandung', 'abc')}
<p>Ringkasan standar terkait ada di <a href="/psak/202/">PSAK 202</a> dan <a href="/psak/236/">PSAK 236</a>.</p>
''',
  faq=[('Apa itu kapasitas normal menurut PSAK 202?', 'Produksi rata-rata yang diharapkan tercapai selama beberapa periode dalam keadaan normal, setelah memperhitungkan hilangnya kapasitas karena pemeliharaan terencana.'),
       ('Ke mana biaya kapasitas menganggur dicatat?', 'Overhead tetap yang tidak teralokasi diakui sebagai beban pada periode terjadinya, tidak ditambahkan ke biaya persediaan maupun ke unit cost layanan.'),
       ('Apakah PSAK 202 berlaku untuk rumah sakit?', 'PSAK 202 mengatur persediaan, misalnya obat dan bahan medis. Jasa rumah sakit bukan persediaan, tetapi prinsip kapasitas normal dipakai dalam akuntansi manajemen untuk menghitung unit cost.')])

# ================================================================== PE
# 4. Tangerang Selatan: klasifikasi instrumen
NOM = 100 * M; KUP = .04; MKT = .10; T = 5
ann = (1 - (1 + MKT) ** -T) / MKT; pvk = NOM * KUP * ann; pvp = NOM * (1 + MKT) ** -T; LIAB = pvk + pvp; EQ = NOM - LIAB
sch, bal = [], LIAB
for y in range(1, 4):
    i = bal * MKT; end = bal + i - NOM * KUP
    sch.append([f'Tahun {y}', jt(bal, 2), jt(i, 2), jt(NOM * KUP), jt(end, 2)]); bal = end

A(site='us', topik='pe', kota='Tangerang Selatan', kota_slug='tangerang-selatan',
  slug='saham-preferen-pinjaman-konversi-investor-liabilitas-atau-ekuitas',
  seo_title='Saham Preferen dan Pinjaman Konversi: Liabilitas atau Ekuitas',
  title='Dana Investor Private Equity di Laporan Keuangan: Liabilitas atau Ekuitas Menurut PSAK 232 dan PSAK 109',
  description='Saham preferen, pinjaman konversi, dan opsi jual investor private equity bisa dicatat sebagai liabilitas menurut PSAK 232 dan PSAK 109. Ini contoh hitungnya.',
  keyword='saham preferen liabilitas atau ekuitas psak 232', category='Pendanaan dan Investor', psak=['232', '109', '113'],
  wa='Halo Pak Ananta, saya membaca artikel klasifikasi dana investor di UpdateSAK. Perusahaan kami di Tangerang Selatan sedang menerima investor dan perlu dibantu pencatatannya.',
  sources=[S_SAK, S_NOM],
  body_html=f'''
<p>Rumah sakit, klinik, dan perusahaan teknologi kesehatan di Tangerang Selatan dan sekitarnya makin sering menerima dana dari private equity dan venture capital. Dana itu jarang berbentuk saham biasa. Bentuknya saham preferen, pinjaman konversi, atau saham dengan opsi jual. Di perjanjian semuanya disebut investasi, tetapi di laporan keuangan sebagian harus dicatat sebagai utang.</p>
<p>Klasifikasinya diatur PSAK 232 Instrumen Keuangan: Penyajian (dulu PSAK 50), dan pengukurannya PSAK 109 Instrumen Keuangan (dulu PSAK 71). Yang menentukan adalah substansi kontrak, bukan nama instrumennya.</p>
<h2>Uji Dasar: Ada Kewajiban Menyerahkan Kas atau Tidak</h2>
<p>Instrumen adalah liabilitas keuangan bila penerbit punya kewajiban kontraktual menyerahkan kas atau aset keuangan lain yang tidak bisa dihindari. Instrumen adalah ekuitas bila tidak ada kewajiban seperti itu dan, bila diselesaikan dengan saham sendiri, jumlah sahamnya tetap untuk jumlah kas yang tetap.</p>
{tbl(['Instrumen', 'Ciri kontrak', 'Klasifikasi di penerbit'],
     [['Saham biasa', 'Dividen sepenuhnya diskresi, tidak ada penebusan', 'Ekuitas'],
      ['Saham preferen dengan dividen diskresi, tanpa penebusan', 'Tidak ada kewajiban membayar', 'Ekuitas'],
      ['Saham preferen wajib ditebus pada tanggal tertentu', 'Ada kewajiban menyerahkan kas', 'Liabilitas'],
      ['Saham preferen dengan dividen tetap yang wajib dibayar', 'Kewajiban kas berkala', 'Liabilitas, atau instrumen majemuk'],
      ['Pinjaman konversi dengan jumlah saham tetap', 'Utang ditambah hak konversi tetap untuk tetap', 'Instrumen majemuk: liabilitas dan ekuitas'],
      ['Pinjaman konversi dengan harga konversi mengikuti valuasi putaran berikutnya', 'Jumlah saham tidak tetap', 'Liabilitas dengan derivatif melekat'],
      ['Saham dengan opsi jual investor kepada perusahaan', 'Perusahaan bisa dipaksa membeli kembali', 'Liabilitas sebesar nilai kini jumlah penebusan']])}
<h2>Contoh: Memisahkan Pinjaman Konversi</h2>
<p>Ilustrasi dengan angka contoh. Perusahaan menerbitkan pinjaman konversi {jt(NOM)}, kupon {pct(KUP, 0)} per tahun, jatuh tempo {T} tahun, dapat dikonversi menjadi jumlah saham yang tetap. Suku bunga pasar untuk utang serupa tanpa hak konversi {pct(MKT, 0)}.</p>
{tbl(['Komponen', 'Perhitungan', 'Nilai'],
     [['Nilai kini kupon', f'{jt(NOM * KUP)} x faktor anuitas {n(ann, 4)}', jt(pvk, 2)],
      ['Nilai kini pokok', f'{jt(NOM)} x faktor diskonto {n((1 + MKT) ** -T, 4)}', jt(pvp, 2)],
      ['Komponen liabilitas', 'Jumlah nilai kini', jt(LIAB, 2)],
      ['Komponen ekuitas', f'{jt(NOM)} dikurangi {jt(LIAB, 2)}', jt(EQ, 2)]])}
<p>Jurnal saat penerbitan: debit kas {jt(NOM)}, kredit liabilitas keuangan {jt(LIAB, 2)}, kredit ekuitas (komponen ekuitas pinjaman konversi) {jt(EQ, 2)}. Setelah itu liabilitas diukur pada biaya perolehan diamortisasi dengan suku bunga efektif {pct(MKT, 0)}.</p>
{tbl(['Periode', 'Liabilitas awal', 'Beban bunga efektif', 'Kupon dibayar', 'Liabilitas akhir'], sch)}
<p>Beban bunga di laba rugi tahun pertama {sch[0][2]}, hampir dua kali kupon yang dibayar. Inilah yang sering mengejutkan pemilik: instrumen berkupon rendah tetap membawa beban bunga setara bunga pasar.</p>
<h2>Bila Harga Konversi Tidak Tetap</h2>
<p>Banyak pinjaman konversi dari venture capital memakai harga konversi berupa diskon atas valuasi putaran berikutnya. Jumlah saham yang diserahkan menjadi tidak tetap, sehingga hak konversi gagal memenuhi syarat ekuitas. Seluruh instrumen menjadi liabilitas, dan fitur konversinya adalah derivatif melekat yang diukur pada nilai wajar melalui laba rugi, atau seluruh instrumen ditetapkan pada nilai wajar melalui laba rugi. Pengukuran nilai wajarnya mengikuti PSAK 113.</p>
<h2>Opsi Jual dan Jaminan Imbal Hasil</h2>
<div class="pf-fold"><p>Term sheet private equity sering memuat hak investor menjual kembali sahamnya bila penawaran umum atau penjualan tidak terjadi dalam jangka waktu tertentu, dengan harga yang menjamin imbal hasil minimum.</p>
<ul>
<li>Bila kewajiban membeli ada pada <b>perusahaan</b>, perusahaan mengakui liabilitas keuangan sebesar nilai kini jumlah penebusan, meskipun di akta dana itu tercatat sebagai modal saham.</li>
<li>Bila kewajiban membeli ada pada <b>pemegang saham pendiri</b>, bukan perusahaan, liabilitas itu tidak muncul di laporan keuangan perusahaan, tetapi perlu diungkapkan dan memengaruhi laporan pendiri.</li>
</ul>
<p>Akibatnya terasa pada rasio. Dana yang dikira menambah ekuitas justru menambah utang, rasio utang terhadap ekuitas memburuk, dan syarat bank bisa terlanggar. Karena itu pasal ini perlu dibaca akuntan sebelum ditandatangani, bukan sesudahnya.</p></div>
<h2>Entitas yang Memakai SAK Entitas Privat</h2>
<p>SAK Entitas Privat juga mengenal pemisahan liabilitas dan ekuitas dengan aturan yang lebih sederhana. Perusahaan yang akan menerima investor institusi biasanya diminta menyusun laporan keuangan dengan SAK Indonesia penuh, sehingga transisi standar perlu direncanakan bersamaan dengan transaksinya.</p>
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Tangerang Selatan', 'tangerang-selatan', 'pe')}
<p>Ringkasan standar ada di <a href="/psak/232/">PSAK 232</a> dan <a href="/psak/109/">PSAK 109</a>.</p>
''',
  faq=[('Apakah saham preferen selalu ekuitas?', 'Tidak. Saham preferen yang wajib ditebus atau membawa kewajiban dividen tetap diklasifikasikan sebagai liabilitas keuangan menurut PSAK 232, seluruhnya atau sebagian.'),
       ('Bagaimana mencatat pinjaman konversi?', 'Bila jumlah saham hasil konversi tetap, pisahkan komponen liabilitas sebesar nilai kini arus kas dengan suku bunga pasar utang serupa, sisanya komponen ekuitas. Bila jumlah saham tidak tetap, seluruhnya liabilitas dengan derivatif melekat.'),
       ('Apa dampak opsi jual investor terhadap laporan keuangan?', 'Bila perusahaan wajib membeli kembali saham investor, perusahaan mengakui liabilitas keuangan sebesar nilai kini jumlah penebusan, sehingga utang naik dan ekuitas turun.')])

# 5. Bogor: PSAK 103
CONS = 240.0; BOOK = 150.0; FV1 = 60.0; FV2 = 20.0; TAXR = .22; PCTA = .80
DTL = (FV1 + FV2) * TAXR; NA = BOOK + FV1 + FV2 - DTL; NCI_P = (1 - PCTA) * NA; GW_P = CONS + NCI_P - NA; NCI_F = 55.0; GW_F = CONS + NCI_F - NA

A(site='us', topik='pe', kota='Bogor', kota_slug='bogor',
  slug='akuisisi-rumah-sakit-psak-103-goodwill-alokasi-harga-beli',
  seo_title='Akuisisi Rumah Sakit: PSAK 103, Goodwill, Alokasi Harga Beli',
  title='Akuntansi Akuisisi Rumah Sakit Menurut PSAK 103: Alokasi Harga Beli, Goodwill, dan Kepentingan Nonpengendali',
  description='Contoh akuntansi akuisisi rumah sakit menurut PSAK 103: aset teridentifikasi pada nilai wajar, pajak tangguhan, kepentingan nonpengendali, dan goodwill.',
  keyword='psak 103 akuisisi rumah sakit goodwill', category='Pendanaan dan Investor', psak=['103', '110', '236', '238', '212'],
  wa='Halo Pak Ananta, saya membaca artikel PSAK 103 di UpdateSAK. Grup kami sedang mengakuisisi rumah sakit di Bogor dan perlu dibantu alokasi harga belinya.',
  sources=[S_SAK, S_NOM],
  body_html=f'''
<p>Bogor dan kota penyangga Jakarta lainnya menjadi sasaran ekspansi jaringan rumah sakit dan investor. Ketika sebuah grup membeli saham pengendali rumah sakit, pekerjaan akuntansinya baru dimulai setelah akta ditandatangani. PSAK 103 Kombinasi Bisnis (dulu PSAK 22) mewajibkan metode akuisisi, dan hasilnya menentukan angka goodwill yang akan menempel di laporan konsolidasian bertahun-tahun.</p>
<h2>Empat Langkah Metode Akuisisi</h2>
<ol>
<li><b>Mengidentifikasi pihak pengakuisisi,</b> yaitu pihak yang memperoleh pengendalian menurut PSAK 110.</li>
<li><b>Menentukan tanggal akuisisi,</b> yaitu tanggal pengendalian beralih, yang bisa berbeda dari tanggal akta.</li>
<li><b>Mengakui dan mengukur aset teridentifikasi, liabilitas yang diambil alih, dan kepentingan nonpengendali.</b> Aset dan liabilitas diukur pada nilai wajar tanggal akuisisi.</li>
<li><b>Mengakui goodwill</b> atau keuntungan dari pembelian dengan diskon.</li>
</ol>
<h2>Aset yang Sering Muncul pada Akuisisi Rumah Sakit</h2>
<ul>
<li>Tanah dan bangunan yang nilai wajarnya jauh di atas nilai buku.</li>
<li>Alat medis yang nilai wajarnya bisa di bawah nilai buku.</li>
<li>Aset takberwujud yang sebelumnya tidak tercatat: merek rumah sakit, perizinan, dan hubungan kontraktual dengan penjamin atau perusahaan, sepanjang memenuhi kriteria keteridentifikasian PSAK 238.</li>
<li>Liabilitas kontinjensi yang merupakan kewajiban kini dan dapat diukur andal, misalnya sengketa klaim.</li>
</ul>
<p>Tenaga kerja yang terlatih, termasuk tim dokter, tidak diakui sebagai aset terpisah. Nilainya masuk ke goodwill.</p>
<h2>Contoh Hitung</h2>
<p>Ilustrasi dengan angka contoh, dalam miliar rupiah. Grup membeli {pct(PCTA, 0)} saham sebuah rumah sakit dengan imbalan {n(CONS)}. Aset neto menurut buku {n(BOOK)}. Penilai menetapkan kenaikan nilai wajar tanah dan bangunan {n(FV1)} serta aset takberwujud teridentifikasi {n(FV2)}. Tarif pajak penghasilan badan 22 persen.</p>
{tbl(['Langkah', 'Perhitungan', 'Nilai'],
     [['Aset neto menurut buku', '', n(BOOK)],
      ['Penyesuaian nilai wajar aset tetap', '', '+' + n(FV1)],
      ['Aset takberwujud teridentifikasi', '', '+' + n(FV2)],
      ['Liabilitas pajak tangguhan', f'({n(FV1)} + {n(FV2)}) x 22%', '-' + n(DTL, 1)]],
     ['Aset neto teridentifikasi pada nilai wajar', '', n(NA, 1)])}
<p>Liabilitas pajak tangguhan muncul karena nilai tercatat naik sedangkan dasar pajaknya tidak, sesuai PSAK 212.</p>
<p>Kepentingan nonpengendali 20 persen dapat diukur dengan dua cara, dan pilihannya dibuat per transaksi.</p>
{tbl(['Pos', 'Kepentingan nonpengendali proporsional', 'Kepentingan nonpengendali pada nilai wajar'],
     [['Imbalan yang dialihkan', n(CONS), n(CONS)],
      ['Kepentingan nonpengendali', f'20% x {n(NA, 1)} = {n(NCI_P, 2)}', n(NCI_F) + ' (dari penilai)'],
      ['Aset neto teridentifikasi', '-' + n(NA, 1), '-' + n(NA, 1)]],
     ['Goodwill', n(GW_P, 2), n(GW_F, 1)])}
<p>Cara kedua menghasilkan goodwill lebih besar karena memuat goodwill bagian nonpengendali.</p>
<h2>Hal yang Sering Terlewat</h2>
<ul>
<li><b>Biaya terkait akuisisi</b> seperti penasihat, uji tuntas, dan notaris dibebankan saat terjadi, tidak menambah harga perolehan.</li>
<li><b>Imbalan kontinjensi</b> (earn-out) diukur pada nilai wajar tanggal akuisisi dan menjadi bagian imbalan. Perubahan setelahnya umumnya masuk laba rugi.</li>
<li><b>Periode pengukuran</b> paling lama satu tahun untuk menyelesaikan angka sementara.</li>
<li><b>Akuisisi bertahap:</b> kepemilikan lama diukur kembali pada nilai wajar saat pengendalian diperoleh.</li>
</ul>
<h2>Setelah Akuisisi</h2>
<div class="pf-fold"><ul>
<li>Goodwill tidak diamortisasi. Ia diuji penurunan nilai paling sedikit setahun sekali menurut PSAK 236, dialokasikan ke unit penghasil kas, biasanya per rumah sakit.</li>
<li>Aset takberwujud dengan umur terbatas diamortisasi, sehingga laba konsolidasian lebih rendah daripada laba rumah sakit secara tersendiri.</li>
<li>Penyusutan dihitung dari nilai wajar, bukan nilai buku lama.</li>
<li>Laporan konsolidasian mengikuti PSAK 110, termasuk eliminasi transaksi antar perusahaan.</li>
</ul>
<p>Rumah sakit yang diakuisisi sering masih memakai SAK Entitas Privat, sedangkan induknya memakai SAK Indonesia penuh. Penyesuaian kebijakan akuntansi dikerjakan pada tingkat konsolidasi. Ketentuan kombinasi bisnis dan goodwill dalam SAK Entitas Privat tidak sama dengan PSAK 103, sehingga perlu dibaca tersendiri.</p></div>
<h2>Siapa Mengerjakan Apa</h2>
{tbl(['Pekerjaan', 'Pihak'],
     [['Penilaian nilai wajar aset dan aset takberwujud', 'Kantor jasa penilai publik'],
      ['Alokasi harga beli dan jurnal konsolidasi', 'Tim keuangan pengakuisisi, sering dibantu konsultan akuntansi'],
      ['Audit laporan konsolidasian', 'Kantor akuntan publik']])}
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Bogor', 'bogor', 'pe')}
<p>Ringkasan standar ada di <a href="/psak/103/">PSAK 103</a>, <a href="/psak/110/">PSAK 110</a>, dan <a href="/psak/236/">PSAK 236</a>.</p>
''',
  faq=[('Bagaimana menghitung goodwill menurut PSAK 103?', 'Goodwill adalah imbalan yang dialihkan ditambah kepentingan nonpengendali, dikurangi aset neto teridentifikasi yang diukur pada nilai wajar tanggal akuisisi.'),
       ('Apakah biaya penasihat akuisisi dikapitalisasi?', 'Tidak. Biaya terkait akuisisi dibebankan pada periode terjadinya dan tidak menambah imbalan maupun goodwill.'),
       ('Apakah goodwill diamortisasi?', 'Menurut SAK Indonesia penuh, goodwill tidak diamortisasi tetapi diuji penurunan nilai paling sedikit setahun sekali menurut PSAK 236.')])

# 6. Depok: QoE
QO = [('Pendapatan klaim tertunda yang diakui penuh', -2.4, 'PSAK 115: imbalan variabel dibatasi sampai sangat mungkin tidak berbalik'),
      ('Jasa medis yang belum diakrual', -1.8, 'Dasar akrual PSAK 201'),
      ('Persediaan farmasi kedaluwarsa', -0.6, 'PSAK 202: nilai realisasi neto'),
      ('Biaya pribadi pemilik', +1.5, 'Bukan beban usaha berulang'),
      ('Biaya hukum sekali terjadi', +0.9, 'Tidak berulang')]
E0 = 30.0; E1 = E0 + sum(v for _, v, _ in QO); SEWA = 3.0; E2 = E1 - SEWA
fm = lambda v: ('+' if v > 0 else '-') + n(abs(v), 1)

A(site='us', topik='pe', kota='Depok', kota_slug='depok',
  slug='normalisasi-ebitda-rumah-sakit-quality-of-earnings',
  seo_title='Normalisasi EBITDA Rumah Sakit: Quality of Earnings',
  title='Normalisasi EBITDA Rumah Sakit: Membaca Quality of Earnings dengan Kacamata PSAK',
  description='Cara menyusun jembatan normalisasi EBITDA rumah sakit untuk investor: klaim tertunda, akrual jasa medis, persediaan farmasi, dan dampak sewa PSAK 116.',
  keyword='normalisasi ebitda rumah sakit', category='Pendanaan dan Investor', psak=['115', '116', '109', '202', '224'],
  wa='Halo Pak Ananta, saya membaca artikel normalisasi EBITDA di UpdateSAK. Rumah sakit kami di Depok ingin menyiapkan quality of earnings sebelum bertemu investor.',
  sources=[S_SAK, S_NOM],
  body_html=f'''
<p>Rumah sakit dan klinik di Depok tumbuh mengikuti penduduk penyangga Jakarta, dan beberapa mulai didekati investor. Hampir semua investor menilai dengan kelipatan EBITDA. Karena itu pekerjaan pertama mereka adalah menguji apakah EBITDA yang dilaporkan benar-benar mencerminkan laba yang berulang. Analisis ini disebut quality of earnings.</p>
<p>Sebagian besar penyesuaiannya sebenarnya soal penerapan standar akuntansi. Rumah sakit yang laporannya sudah sesuai PSAK akan mengalami lebih sedikit koreksi.</p>
<h2>EBITDA Bukan Istilah PSAK</h2>
<p>SAK Indonesia tidak mendefinisikan EBITDA. PSAK 118, yang berlaku efektif 1 Januari 2027, memperkenalkan subtotal laba operasi dan mengatur pengungkapan ukuran kinerja yang ditetapkan manajemen. Sampai saat itu, setiap pihak boleh mendefinisikan EBITDA sendiri, dan justru di situlah sumber selisih. Sepakati definisinya di awal.</p>
<h2>Contoh Jembatan Normalisasi</h2>
<p>Ilustrasi dengan angka contoh, dalam miliar rupiah setahun.</p>
{tbl(['Pos', 'Nilai', 'Dasar'], [['EBITDA menurut laporan manajemen', n(E0, 1), '']] + [[a, fm(v), d] for a, v, d in QO],
     ['EBITDA setelah normalisasi', n(E1, 1), ''])}
<h2>Penjelasan Tiap Penyesuaian</h2>
<ul>
<li><b>Klaim tertunda.</b> Pendapatan dari penjamin yang masih diverifikasi atau disengketakan mengandung imbalan variabel. PSAK 115 membatasi pengakuannya sampai jumlah yang sangat mungkin tidak mengalami pembalikan signifikan. Piutangnya juga dikenai penyisihan kerugian kredit ekspektasian menurut PSAK 109.</li>
<li><b>Jasa medis.</b> Jasa dokter atas layanan bulan Desember yang dibayar Januari tetap beban Desember.</li>
<li><b>Persediaan farmasi.</b> Obat kedaluwarsa dan yang perputarannya lambat diturunkan ke nilai realisasi neto.</li>
<li><b>Biaya pemilik dan biaya sekali terjadi.</b> Ditambahkan kembali, tetapi investor meminta bukti bahwa biaya itu memang tidak berulang.</li>
</ul>
<h2>Dampak PSAK 116: EBITDA Naik Tanpa Kas Bertambah</h2>
<p>Sejak PSAK 116 berlaku, sewa gedung atau alat tidak lagi dicatat sebagai beban sewa, melainkan sebagai penyusutan aset hak guna dan bunga liabilitas sewa. Keduanya berada di bawah EBITDA. Akibatnya EBITDA rumah sakit penyewa terlihat lebih tinggi.</p>
{tbl(['Ukuran', 'Perhitungan', 'Nilai'],
     [['EBITDA setelah normalisasi (laporan menerapkan PSAK 116)', '', n(E1, 1)],
      ['Pembayaran sewa setahun', '', '-' + n(SEWA, 1)],
      ['EBITDA setelah sewa', f'{n(E1, 1)} dikurangi {n(SEWA, 1)}', n(E2, 1)]])}
<p>Tidak ada yang benar atau salah di antara keduanya. Yang penting konsisten. Bila memakai EBITDA {n(E1, 1)}, liabilitas sewa harus dimasukkan ke utang bersih. Bila memakai {n(E2, 1)}, liabilitas sewa dikeluarkan. Mencampur keduanya menghasilkan nilai ekuitas yang terlalu tinggi atau terlalu rendah.</p>
<h2>Pos Lain yang Diperiksa</h2>
<div class="pf-fold"><ul>
<li><b>Transaksi pihak berelasi.</b> Sewa dari pemilik, pembelian dari perusahaan keluarga, dan pinjaman pemegang saham harus diungkapkan menurut PSAK 224 dan dinilai kewajarannya.</li>
<li><b>Pendapatan per penjamin.</b> Tren tarif dan volume dipisahkan agar pertumbuhan yang berasal dari satu kali penyesuaian tarif tidak dibaca sebagai pertumbuhan berulang.</li>
<li><b>Imbalan kerja.</b> Liabilitas imbalan pascakerja menurut PSAK 219 sering belum dicatat dan diperlakukan investor sebagai pos setara utang.</li>
<li><b>Belanja modal pemeliharaan.</b> EBITDA tidak memuatnya, tetapi alat medis harus diganti.</li>
</ul></div>
<h2>Cara Menyiapkannya Sendiri</h2>
<ol>
<li>Tutup buku bulanan dengan akrual yang lengkap minimal 24 bulan.</li>
<li>Pisahkan klaim menurut status: dibayar, tertunda, ditolak.</li>
<li>Lakukan penghitungan fisik persediaan dan hapus yang kedaluwarsa.</li>
<li>Daftar semua transaksi dengan pemilik dan keluarganya.</li>
<li>Susun jembatan normalisasi sendiri sebelum investor menyusunnya.</li>
</ol>
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Depok', 'depok', 'pe')}
<p>Ringkasan standar ada di <a href="/psak/115/">PSAK 115</a>, <a href="/psak/116/">PSAK 116</a>, dan <a href="/psak/118/">PSAK 118</a>.</p>
''',
  faq=[('Apa itu quality of earnings?', 'Analisis yang menguji apakah laba yang dilaporkan, biasanya EBITDA, mencerminkan kinerja berulang, dengan menyesuaikan pos tidak berulang dan pos yang pencatatannya belum sesuai standar.'),
       ('Apakah EBITDA diatur dalam PSAK?', 'Tidak. EBITDA bukan ukuran yang didefinisikan SAK Indonesia. PSAK 118 yang berlaku 1 Januari 2027 mengatur subtotal laba operasi dan pengungkapan ukuran kinerja yang ditetapkan manajemen.'),
       ('Bagaimana PSAK 116 memengaruhi EBITDA?', 'Beban sewa berubah menjadi penyusutan aset hak guna dan bunga liabilitas sewa, sehingga EBITDA naik. Konsistensinya dijaga dengan memasukkan liabilitas sewa ke utang bersih.')])

# ================================================================== CFO
# 7. Karawang: paket laporan + 13 minggu
RC = [3.0, 2.6, 3.1, 2.4, 2.5, 2.9, 2.0, 3.2, 3.6, 3.0, 3.4, 3.2, 3.9]
SP = [2.1, 2.4, 2.0, 2.6, 2.2, 2.3, 2.5, 2.1, 2.2, 2.6, 2.0, 2.4, 2.2]
PAY = {4: 1.6, 8: 1.6, 13: 1.6}; TX = {2: .35, 6: .35, 10: .35}; LN = {1: .6, 5: .6, 9: .6, 13: .6}
OPEN = 1.8; MINC = 1.0
cf_rows, bal, lows = [], OPEN, []
for w in range(1, 14):
    out = SP[w - 1] + PAY.get(w, 0) + TX.get(w, 0) + LN.get(w, 0)
    end = bal + RC[w - 1] - out
    end = round(end, 2)
    if end < MINC: lows.append((w, end))
    cf_rows.append([str(w), n(bal, 2), n(RC[w - 1], 2), n(SP[w - 1], 2), n(PAY.get(w, 0) + TX.get(w, 0) + LN.get(w, 0), 2), n(end, 2) + (' *' if end < MINC else '')])
    bal = end
WMIN = min(lows, key=lambda x: x[1]) if lows else None

A(site='us', topik='cfo', kota='Karawang', kota_slug='karawang',
  slug='paket-laporan-manajemen-bulanan-proyeksi-kas-13-minggu',
  seo_title='Paket Laporan Manajemen Bulanan dan Proyeksi Kas 13 Minggu',
  title='Paket Laporan Manajemen Bulanan dan Proyeksi Kas 13 Minggu: Format yang Dipakai Fractional CFO',
  description='Isi paket laporan manajemen bulanan dan contoh proyeksi arus kas 13 minggu untuk perusahaan manufaktur, seperti yang disusun fractional CFO.',
  keyword='proyeksi arus kas 13 minggu', category='CFO dan Pelaporan', psak=['207', '201', '118'],
  wa='Halo Pak Ananta, saya membaca artikel paket laporan manajemen di UpdateSAK. Perusahaan kami di Karawang ingin dibantu menyusunnya.',
  sources=[S_SAK],
  body_html=f'''
<p>Karawang adalah salah satu pusat industri otomotif dan manufaktur nasional. Pemasok komponen di sini terbiasa dengan laporan mutu dan pengiriman yang ketat dari pelanggan, tetapi laporan keuangannya sering hanya terbit setahun sekali untuk pajak dan bank. Fractional CFO biasanya memulai dari dua hal: paket laporan manajemen bulanan dan proyeksi arus kas 13 minggu.</p>
<h2>Isi Paket Laporan Manajemen Bulanan</h2>
{tbl(['Bagian', 'Isi', 'Pertanyaan yang dijawab'],
     [['Ringkasan satu halaman', 'Lima sampai tujuh angka utama dan tiga hal yang butuh keputusan', 'Apa yang berubah bulan ini?'],
      ['Laba rugi', 'Aktual, anggaran, dan tahun lalu, dengan selisihnya', 'Di mana meleset dan mengapa?'],
      ['Margin per produk atau pelanggan', 'Penjualan, harga pokok, margin kontribusi', 'Siapa yang menghasilkan laba?'],
      ['Posisi keuangan', 'Modal kerja, utang, dan rasio yang diperjanjikan bank', 'Apakah masih aman?'],
      ['Arus kas', 'Arus kas bulan berjalan dan proyeksi 13 minggu', 'Cukupkah kas tiga bulan ke depan?'],
      ['Indikator operasional', 'Utilisasi mesin, tingkat cacat, umur persediaan, umur piutang', 'Apa penyebab di balik angka?']])}
<p>Laporan manajemen tidak harus berformat PSAK, tetapi angkanya harus berasal dari buku yang sama dengan laporan keuangan. Laporan arus kas tahunan tetap mengikuti PSAK 207.</p>
<h2>Kenapa 13 Minggu</h2>
<p>Tiga belas minggu sama dengan satu triwulan. Cukup panjang untuk melihat gaji, pajak, dan angsuran yang jatuh tempo, cukup pendek untuk disusun dari data nyata: faktur yang sudah terbit, pesanan pembelian yang sudah dibuat, dan jadwal pembayaran yang sudah diketahui. Proyeksi ini memakai metode langsung, yaitu penerimaan dan pengeluaran kas, bukan laba yang disesuaikan.</p>
<h2>Contoh Proyeksi Kas 13 Minggu</h2>
<p>Ilustrasi dengan angka contoh, dalam miliar rupiah. Saldo awal {n(OPEN, 1)}, saldo minimum yang ditetapkan direksi {n(MINC, 1)}. Kolom lain-lain memuat gaji (minggu 4, 8, dan 13), pajak (minggu 2, 6, dan 10), dan angsuran bank (minggu 1, 5, 9, dan 13).</p>
{tbl(['Minggu', 'Saldo awal', 'Penerimaan pelanggan', 'Pembayaran pemasok', 'Gaji, pajak, angsuran', 'Saldo akhir'], cf_rows)}
<p>Tanda bintang menunjukkan saldo di bawah batas minimum. Ada {len(lows)} minggu yang melanggar batas, dan titik terendahnya minggu ke-{WMIN[0]} dengan saldo {n(WMIN[1], 2)}. Tanpa proyeksi, hal ini baru diketahui pada minggu itu. Dengan proyeksi, direksi punya waktu beberapa minggu untuk bertindak.</p>
<h2>Tindakan yang Bisa Diambil</h2>
<ul>
<li>Menagih lebih awal pelanggan yang jatuh tempo di minggu berikutnya.</li>
<li>Menggeser pembayaran pemasok yang terminnya masih longgar, dengan kesepakatan.</li>
<li>Menarik fasilitas kredit modal kerja untuk beberapa minggu saja, bukan sepanjang bulan.</li>
<li>Menjadwal ulang pembelian bahan yang belum mendesak.</li>
</ul>
<h2>Cara Menyusunnya</h2>
<div class="pf-fold"><ol>
<li><b>Penerimaan:</b> ambil daftar piutang per faktur, taruh di minggu jatuh temponya, lalu koreksi dengan kebiasaan bayar tiap pelanggan.</li>
<li><b>Pembayaran pemasok:</b> ambil daftar utang dan pesanan pembelian terbuka.</li>
<li><b>Pengeluaran tetap:</b> gaji, jaminan sosial, pajak bulanan, sewa, listrik, dan angsuran.</li>
<li><b>Pengeluaran tidak rutin:</b> belanja modal, tunjangan hari raya, dividen, pajak tahunan.</li>
<li><b>Perbarui tiap minggu:</b> ganti minggu yang lewat dengan angka nyata, tambahkan satu minggu baru di ujung, dan catat selisihnya.</li>
</ol>
<p>Selisih antara proyeksi dan realisasi minggu lalu adalah bahan belajar terbaik. Dalam dua sampai tiga bulan, ketepatannya biasanya membaik dengan sendirinya.</p></div>
<h2>Kaitan dengan Laporan Keuangan</h2>
<ul>
<li>Saldo kas proyeksi minggu terakhir bulan harus cocok dengan kas di laporan posisi keuangan bulan itu.</li>
<li>Selisih laba dan arus kas operasi dijelaskan oleh perubahan modal kerja, seperti dalam metode tidak langsung PSAK 207.</li>
<li>Mulai 2027, penyajian laba rugi mengikuti PSAK 118. Paket laporan manajemen sebaiknya sudah memakai kategori operasi, investasi, dan pendanaan agar tidak ada dua versi angka.</li>
</ul>
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Karawang', 'karawang', 'cfo')}
<p>Baca juga <a href="/artikel/laporan-arus-kas-cara-menyusun/">cara menyusun laporan arus kas</a> dan ringkasan <a href="/psak/207/">PSAK 207</a>.</p>
''',
  faq=[('Apa itu proyeksi arus kas 13 minggu?', 'Proyeksi penerimaan dan pengeluaran kas mingguan untuk satu triwulan ke depan dengan metode langsung, diperbarui tiap minggu, untuk mengetahui kapan kas akan ketat.'),
       ('Apa isi paket laporan manajemen bulanan?', 'Ringkasan satu halaman, laba rugi terhadap anggaran, margin per produk atau pelanggan, posisi keuangan dan rasio bank, arus kas dan proyeksi 13 minggu, serta indikator operasional.'),
       ('Apakah laporan manajemen harus sesuai PSAK?', 'Formatnya bebas, tetapi angkanya harus bersumber dari pembukuan yang sama dengan laporan keuangan sehingga bisa direkonsiliasi.')])

# 8. Gresik: tutup buku 5 hari
A(site='us', topik='cfo', kota='Gresik', kota_slug='gresik',
  slug='tutup-buku-bulanan-lima-hari-kalender-closing',
  seo_title='Tutup Buku Bulanan Lima Hari: Kalender Closing dan Akrual',
  title='Tutup Buku Bulanan dalam Lima Hari Kerja: Kalender Closing, Pisah Batas, dan Akrual',
  description='Kalender tutup buku bulanan lima hari kerja untuk perusahaan industri: pisah batas, akrual, rekonsiliasi, dan pengendalian yang dipasang fractional CFO.',
  keyword='tutup buku bulanan closing', category='CFO dan Pelaporan', psak=['201', '202', '216', '115'],
  wa='Halo Pak Ananta, saya membaca artikel kalender tutup buku di UpdateSAK. Perusahaan kami di Gresik ingin mempercepat closing bulanan.',
  sources=[S_SAK],
  body_html=f'''
<p>Gresik adalah kota industri dengan pabrik pupuk, semen, kimia, smelter, dan ratusan perusahaan penunjangnya. Di perusahaan penunjang, laporan bulanan sering baru selesai setelah tanggal 20. Pada saat itu angkanya sudah tidak berguna untuk memutuskan apa pun. Fractional CFO hampir selalu memulai dengan target yang sama: tutup buku selesai pada hari kerja kelima.</p>
<h2>Dasar: Akrual dan Pisah Batas</h2>
<p>PSAK 201 mensyaratkan laporan keuangan disusun dengan dasar akrual. Pendapatan dan beban diakui pada periode terjadinya, bukan saat kas diterima atau dibayar. Dua disiplin yang menopangnya:</p>
<ul>
<li><b>Pisah batas (cut-off):</b> transaksi dicatat di periode yang benar. Barang yang dikirim tanggal 31 adalah penjualan bulan ini bila pengendalian sudah berpindah menurut PSAK 115.</li>
<li><b>Akrual:</b> beban yang sudah terjadi tetapi belum ditagih tetap dicatat, misalnya listrik, lembur, dan jasa angkut.</li>
</ul>
<h2>Kalender Lima Hari Kerja</h2>
{tbl(['Hari', 'Pekerjaan', 'Penanggung jawab'],
     [['H-3 sampai H-1', 'Pengingat pisah batas ke gudang dan penjualan, daftar akrual rutin disiapkan, stok opname bila dijadwalkan', 'Kepala akuntansi'],
      ['Hari 1', 'Tutup modul penjualan dan pembelian, rekonsiliasi bank, pencocokan pengiriman dan faktur', 'Staf piutang, utang, kas'],
      ['Hari 2', 'Persediaan dan harga pokok, penyusutan, amortisasi biaya dibayar di muka', 'Staf biaya dan aset'],
      ['Hari 3', 'Akrual beban, gaji dan lembur, bunga pinjaman, pajak bulanan', 'Staf buku besar'],
      ['Hari 4', 'Rekonsiliasi akun neraca, telaah analitis, jurnal koreksi', 'Kepala akuntansi'],
      ['Hari 5', 'Paket laporan manajemen, telaah CFO, laporan ke direksi', 'CFO']])}
<h2>Akrual yang Paling Sering Terlewat</h2>
{tbl(['Pos', 'Cara menaksir', 'Bukti'],
     [['Listrik dan gas', 'Pemakaian meter sampai akhir bulan x tarif', 'Catatan meter'],
      ['Lembur dan insentif', 'Rekap absensi yang belum dibayar', 'Rekap sumber daya manusia'],
      ['Jasa angkut dan bongkar muat', 'Surat jalan yang belum ditagih x tarif kontrak', 'Surat jalan'],
      ['Barang diterima belum difaktur', 'Laporan penerimaan barang tanpa faktur x harga pesanan', 'Laporan penerimaan'],
      ['Bunga pinjaman', 'Saldo pokok x suku bunga x hari berjalan', 'Jadwal angsuran'],
      ['Bonus dan tunjangan hari raya', 'Seperduabelas taksiran tahunan', 'Kebijakan perusahaan']])}
<h2>Rekonsiliasi Wajib Sebelum Laporan Terbit</h2>
<ul>
<li>Bank: saldo buku dengan rekening koran.</li>
<li>Piutang dan utang: buku pembantu dengan buku besar.</li>
<li>Persediaan: catatan gudang dengan buku besar, dan pengukuran menurut PSAK 202.</li>
<li>Aset tetap: daftar aset dengan buku besar, penyusutan menurut PSAK 216.</li>
<li>Pajak: buku besar dengan pelaporan pajak bulanan.</li>
<li>Antar perusahaan: saldo saling cocok bila ada grup.</li>
</ul>
<h2>Kenapa Closing Lambat dan Cara Memangkasnya</h2>
<div class="pf-fold">{tbl(['Penyebab', 'Perbaikan'],
     [['Menunggu faktur pemasok', 'Akrual berdasarkan penerimaan barang, koreksi bulan berikutnya'],
      ['Stok opname setiap akhir bulan', 'Perhitungan berkala bergilir, opname penuh tiap semester'],
      ['Rekonsiliasi bank menumpuk', 'Rekonsiliasi mingguan'],
      ['Jurnal manual banyak', 'Jurnal berulang dibuat templat'],
      ['Koreksi berulang untuk hal yang sama', 'Perbaiki di sumbernya, bukan di jurnal penyesuaian'],
      ['Tidak ada batas materialitas', 'Tetapkan ambang: selisih kecil diselesaikan bulan berikutnya']])}
<p>Menutup buku lebih cepat bukan berarti kurang teliti. Taksiran yang wajar pada hari kelima lebih berguna daripada angka pasti pada hari kedua puluh, selama selisihnya dipantau dan dikoreksi.</p></div>
<h2>Ukuran Keberhasilan</h2>
<ul>
<li>Hari kerja sampai laporan terbit.</li>
<li>Jumlah dan nilai jurnal koreksi setelah laporan terbit.</li>
<li>Jumlah akun neraca yang belum direkonsiliasi.</li>
<li>Selisih antara laporan bulanan dan laporan auditan akhir tahun.</li>
</ul>
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Gresik', 'gresik', 'cfo')}
<p>Lihat juga <a href="/artikel/kalender-tutup-buku-akhir-tahun-2026/">kalender tutup buku akhir tahun 2026</a> dan <a href="/buku-besar/">panduan buku besar</a>.</p>
''',
  faq=[('Berapa lama idealnya tutup buku bulanan?', 'Banyak perusahaan menengah menargetkan lima hari kerja. Yang penting konsisten dan laporan terbit sebelum keputusan bulan berikutnya diambil.'),
       ('Apa beda pisah batas dan akrual?', 'Pisah batas memastikan transaksi dicatat di periode yang benar. Akrual mencatat beban atau pendapatan yang sudah terjadi meskipun belum ditagih atau dibayar.'),
       ('Apakah akrual boleh berupa taksiran?', 'Boleh selama dasarnya wajar dan terdokumentasi. Selisih dengan tagihan sebenarnya dikoreksi pada periode berikutnya.')])

# 9. Cilegon: kovenan
EBI = 80.0; BNG = 18.0; POK = 30.0; LIA = 420.0; EKU = 200.0; AL = 150.0; LL = 130.0; LT = 250.0; RUGI = 45.0
DSC = EBI / (BNG + POK); DER = LIA / EKU; CR = AL / LL; DER2 = LIA / (EKU - RUGI); CR2 = AL / (LL + LT)

A(site='us', topik='cfo', kota='Cilegon', kota_slug='cilegon',
  slug='kovenan-bank-dscr-der-klasifikasi-utang-psak-201',
  seo_title='Kovenan Bank: DSCR, DER, dan Klasifikasi Utang PSAK 201',
  title='Kovenan Bank dan Klasifikasi Utang: Menghitung DSCR dan DER serta Dampaknya Menurut PSAK 201',
  description='Cara menghitung DSCR, DER, dan rasio lancar dalam perjanjian kredit, serta dampak pelanggaran kovenan terhadap klasifikasi utang menurut amendemen PSAK 201.',
  keyword='kovenan bank dscr der psak 201', category='CFO dan Pelaporan', psak=['201', '109', '118', '207'],
  wa='Halo Pak Ananta, saya membaca artikel kovenan bank di UpdateSAK. Perusahaan kami di Cilegon ingin dibantu memantau kovenan kredit.',
  sources=[S_SAK, S_NOM],
  body_html=f'''
<p>Cilegon adalah kota industri berat: baja, petrokimia, dan pembangkit, dengan banyak perusahaan penunjang yang mesin dan gudangnya dibiayai kredit investasi. Perjanjian kreditnya hampir selalu memuat kovenan keuangan, yaitu rasio yang wajib dijaga. Banyak direksi baru membacanya ketika bank mengirim surat peringatan. Padahal sejak 1 Januari 2024, amendemen PSAK 201 membuat kovenan berpengaruh langsung pada penyajian utang di laporan keuangan.</p>
<h2>Tiga Rasio yang Paling Sering Diperjanjikan</h2>
<p>Ilustrasi dengan angka contoh, dalam miliar rupiah.</p>
{tbl(['Rasio', 'Rumus umum', 'Perhitungan', 'Hasil', 'Syarat contoh'],
     [['DSCR', 'EBITDA / (bunga + angsuran pokok)', f'{n(EBI)} / ({n(BNG)} + {n(POK)})', n(DSC, 2) + ' kali', 'Minimal 1,25 kali'],
      ['DER', 'Total liabilitas / ekuitas', f'{n(LIA)} / {n(EKU)}', n(DER, 2) + ' kali', 'Maksimal 2,50 kali'],
      ['Rasio lancar', 'Aset lancar / liabilitas jangka pendek', f'{n(AL)} / {n(LL)}', n(CR, 2) + ' kali', 'Minimal 1,00 kali']])}
<p>Rumus di atas hanya bentuk umum. Setiap perjanjian punya definisi sendiri: apakah EBITDA dikurangi pajak dan belanja modal, apakah utang pemegang saham dihitung sebagai liabilitas, apakah liabilitas sewa PSAK 116 dimasukkan. Hitung selalu dengan definisi di perjanjian, bukan definisi buku teks.</p>
<h2>Ruang Gerak</h2>
<ul>
<li>DSCR: EBITDA boleh turun sampai {n(1.25 * (BNG + POK), 1)} sebelum melanggar, atau turun {pct(1 - 1.25 * (BNG + POK) / EBI)}.</li>
<li>DER: ekuitas boleh turun sampai {n(LIA / 2.5)} sebelum melanggar, atau rugi sampai {n(EKU - LIA / 2.5)}.</li>
</ul>
<p>Angka ruang gerak inilah yang seharusnya dilaporkan ke direksi tiap bulan, bukan hanya rasionya.</p>
<h2>Apa Kata PSAK 201 tentang Kovenan</h2>
<ul>
<li>Liabilitas diklasifikasikan jangka panjang bila entitas memiliki hak, pada akhir periode pelaporan, untuk menangguhkan penyelesaian sekurangnya 12 bulan.</li>
<li>Kovenan yang harus dipenuhi <b>pada atau sebelum</b> akhir periode pelaporan memengaruhi klasifikasi itu, walaupun pengujiannya baru dilakukan setelah tanggal pelaporan.</li>
<li>Kovenan yang baru harus dipenuhi <b>setelah</b> akhir periode pelaporan tidak memengaruhi klasifikasi, tetapi harus diungkapkan bila ada risiko liabilitas menjadi jatuh tempo dalam 12 bulan.</li>
<li>Bila kovenan terlanggar pada akhir periode sehingga pinjaman dapat ditagih seketika, pinjaman disajikan sebagai jangka pendek, kecuali pemberi pinjaman sudah menyetujui masa tenggang sekurangnya 12 bulan <b>sebelum</b> akhir periode pelaporan. Surat pelepasan yang terbit setelah tanggal pelaporan tidak mengubah klasifikasi.</li>
</ul>
<h2>Contoh Dampak Pelanggaran</h2>
<p>Lanjutkan contoh di atas. Perusahaan mencatat rugi selisih kurs {n(RUGI)} menjelang akhir tahun, ekuitas turun menjadi {n(EKU - RUGI)}.</p>
{tbl(['Ukuran', 'Sebelum', 'Sesudah'],
     [['DER', n(DER, 2) + ' kali', n(DER2, 2) + ' kali (melanggar batas 2,50)'],
      ['Pinjaman jangka panjang', n(LT) + ' di jangka panjang', n(LT) + ' pindah ke jangka pendek'],
      ['Liabilitas jangka pendek', n(LL), n(LL + LT)],
      ['Rasio lancar', n(CR, 2) + ' kali', n(CR2, 2) + ' kali']])}
<p>Satu pelanggaran menyeret rasio lain. Rasio lancar jatuh ke {n(CR2, 2)} kali, auditor mempertimbangkan ketidakpastian kelangsungan usaha, dan bank lain yang memegang klausul wanprestasi silang ikut bereaksi.</p>
<h2>Yang Dikerjakan Sebelum Tanggal Pelaporan</h2>
<div class="pf-fold"><ol>
<li>Proyeksikan rasio pada tanggal pelaporan sejak triwulan ketiga.</li>
<li>Bila pelanggaran mungkin terjadi, ajukan permohonan pelepasan atau perubahan kovenan ke bank lebih awal, dan pastikan persetujuan tertulis terbit sebelum akhir tahun.</li>
<li>Pertimbangkan tindakan yang memperbaiki rasio: setoran modal, konversi pinjaman pemegang saham, lindung nilai, atau penjadwalan ulang.</li>
<li>Siapkan pengungkapan kovenan di catatan atas laporan keuangan.</li>
</ol>
<p>Penyajian liabilitas keuangan dan pengungkapannya juga terkait PSAK 109 dan, mulai 2027, struktur laporan menurut PSAK 118.</p></div>
<h2>Memantau Kovenan sebagai Rutinitas</h2>
<ul>
<li>Buat daftar semua kovenan dari setiap perjanjian kredit: definisi, batas, dan tanggal uji.</li>
<li>Hitung tiap bulan bersama tutup buku.</li>
<li>Laporkan ruang gerak, bukan hanya lulus atau tidak.</li>
<li>Uji setiap rencana investasi dan dividen terhadap kovenan sebelum diputuskan.</li>
</ul>
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Cilegon', 'cilegon', 'cfo')}
<p>Ringkasan standar ada di <a href="/psak/201/">PSAK 201</a> dan <a href="/psak/118/">PSAK 118</a>.</p>
''',
  faq=[('Apa itu kovenan dalam perjanjian kredit?', 'Syarat yang wajib dijaga debitur selama kredit berjalan. Kovenan keuangan biasanya berupa rasio seperti DSCR, DER, dan rasio lancar dengan definisi yang ditetapkan perjanjian.'),
       ('Apa akibat melanggar kovenan terhadap laporan keuangan?', 'Bila pelanggaran pada akhir periode membuat pinjaman dapat ditagih seketika, pinjaman disajikan sebagai liabilitas jangka pendek, kecuali masa tenggang sekurangnya 12 bulan sudah disetujui sebelum akhir periode pelaporan.'),
       ('Apakah surat pelepasan dari bank setelah tutup tahun membantu?', 'Tidak untuk klasifikasi. Persetujuan yang diperoleh setelah akhir periode pelaporan diungkapkan sebagai peristiwa setelah periode pelaporan, tetapi pinjaman tetap disajikan jangka pendek.')])

# 10. Purwakarta: anggaran fleksibel
BV, BP, BVC, BF = 10000, 50000.0, 30000.0, 120e6
AV, AP, AVC, AF = 9000, 52000.0, 31500.0, 125e6
STAT = BV * (BP - BVC) - BF; ACTL = AV * (AP - AVC) - AF; FLEX = AV * (BP - BVC) - BF
V_VOL = FLEX - STAT; V_PR = AV * (AP - BP); V_VC = -AV * (AVC - BVC); V_FX = -(AF - BF)
uf = lambda v: jt(abs(v)) + (' menguntungkan' if v > 0 else ' merugikan')

A(site='us', topik='cfo', kota='Purwakarta', kota_slug='purwakarta',
  slug='anggaran-fleksibel-analisis-selisih-prakiraan-bergulir',
  seo_title='Anggaran Fleksibel, Analisis Selisih, Prakiraan Bergulir',
  title='Anggaran Fleksibel, Analisis Selisih, dan Prakiraan Bergulir: Contoh Hitung untuk Perusahaan Menengah',
  description='Contoh hitung anggaran fleksibel dan analisis selisih volume, harga, dan biaya, serta cara menyusun prakiraan bergulir 12 bulan untuk perusahaan menengah.',
  keyword='anggaran fleksibel analisis selisih', category='CFO dan Pelaporan', psak=['201', '118', '202'],
  wa='Halo Pak Ananta, saya membaca artikel anggaran fleksibel di UpdateSAK. Perusahaan kami di Purwakarta ingin dibantu menyusun anggaran dan prakiraan.',
  sources=[S_SAK],
  body_html=f'''
<p>Purwakarta dan kawasan industrinya dihuni pabrik tekstil, komponen, dan barang konsumsi yang volume pesanannya naik turun mengikuti pelanggan. Di perusahaan seperti ini, membandingkan laba aktual dengan anggaran awal tahun hampir tidak memberi pelajaran apa pun, karena volumenya sudah berbeda. Dua alat yang dipasang fractional CFO adalah anggaran fleksibel dan prakiraan bergulir.</p>
<h2>Anggaran Statis dan Kelemahannya</h2>
<p>Anggaran statis disusun untuk satu tingkat volume. Ketika volume aktual berbeda, selisih biaya bercampur antara efek volume dan efek efisiensi. Manajer produksi bisa terlihat hemat hanya karena produksinya turun.</p>
<h2>Contoh Data</h2>
{tbl(['Pos', 'Anggaran', 'Aktual'],
     [['Volume penjualan (unit)', n(BV), n(AV)], ['Harga jual per unit', rp(BP), rp(AP)], ['Biaya variabel per unit', rp(BVC), rp(AVC)], ['Biaya tetap', jt(BF), jt(AF)]],
     ['Laba operasi', jt(STAT), jt(ACTL)])}
<p>Laba aktual {jt(ACTL)} dibanding anggaran {jt(STAT)}: selisih {uf(ACTL - STAT)}. Pertanyaannya, dari mana?</p>
<h2>Langkah 1: Susun Anggaran Fleksibel</h2>
<p>Anggaran fleksibel memakai harga dan biaya anggaran pada volume aktual: {n(AV)} x ({rp(BP)} dikurangi {rp(BVC)}) dikurangi {jt(BF)} = {jt(FLEX)}.</p>
<h2>Langkah 2: Uraikan Selisih</h2>
{tbl(['Selisih', 'Perhitungan', 'Hasil'],
     [['Selisih volume penjualan', f'Anggaran fleksibel {jt(FLEX)} dikurangi anggaran statis {jt(STAT)}', uf(V_VOL)],
      ['Selisih harga jual', f'{n(AV)} x ({rp(AP)} dikurangi {rp(BP)})', uf(V_PR)],
      ['Selisih biaya variabel', f'{n(AV)} x ({rp(AVC)} dikurangi {rp(BVC)})', uf(V_VC)],
      ['Selisih biaya tetap', f'{jt(AF)} dikurangi {jt(BF)}', uf(V_FX)]],
     ['Jumlah selisih', '', uf(V_VOL + V_PR + V_VC + V_FX)])}
<p>Sekarang ceritanya jelas. Hampir seluruh penurunan laba berasal dari volume. Kenaikan harga jual hampir menutup kenaikan biaya variabel dan biaya tetap, tersisa selisih {uf(V_PR + V_VC + V_FX)}. Tanpa uraian ini, rapat direksi akan menghabiskan waktu menyalahkan biaya, padahal masalahnya di penjualan.</p>
<h2>Menguraikan Lebih Dalam</h2>
<div class="pf-fold"><ul>
<li><b>Selisih biaya variabel</b> dipecah menjadi selisih harga bahan dan selisih pemakaian, selisih tarif upah dan selisih efisiensi jam kerja.</li>
<li><b>Selisih volume penjualan</b> dipecah menjadi selisih bauran produk dan selisih kuantitas bila produknya lebih dari satu.</li>
<li><b>Overhead tetap</b> yang tidak terserap karena volume rendah dilaporkan sebagai kapasitas menganggur. Untuk pengukuran persediaan, PSAK 202 mengharuskan overhead tetap dialokasikan pada kapasitas normal dan selisihnya dibebankan pada periode berjalan.</li>
</ul></div>
<h2>Prakiraan Bergulir 12 Bulan</h2>
<p>Anggaran tahunan tetap dipakai sebagai target. Prakiraan bergulir menjawab pertanyaan lain: dengan informasi hari ini, ke mana angka akan mendarat? Setiap bulan, bulan yang lewat diganti angka aktual dan satu bulan baru ditambahkan, sehingga selalu ada pandangan 12 bulan ke depan.</p>
{tbl(['Unsur', 'Anggaran tahunan', 'Prakiraan bergulir'],
     [['Tujuan', 'Target dan dasar penilaian kinerja', 'Perkiraan terbaik saat ini'],
      ['Frekuensi', 'Setahun sekali', 'Bulanan atau triwulanan'],
      ['Cakrawala', 'Sampai akhir tahun buku', 'Selalu 12 bulan ke depan'],
      ['Tingkat rinci', 'Per akun', 'Per pemicu utama: volume, harga, bahan, tenaga kerja'],
      ['Dipakai untuk', 'Insentif dan pengendalian', 'Kas, kovenan bank, dan keputusan investasi']])}
<h2>Pemicu yang Cukup Dipantau</h2>
<ul>
<li>Volume pesanan per pelanggan utama.</li>
<li>Harga jual dan klausul penyesuaian harga.</li>
<li>Harga bahan baku utama dan kurs.</li>
<li>Upah minimum dan jumlah tenaga kerja.</li>
<li>Utilisasi mesin terhadap kapasitas.</li>
</ul>
<p>Lima sampai tujuh pemicu biasanya menjelaskan sebagian besar pergerakan laba. Prakiraan yang dibangun dari pemicu lebih cepat diperbarui daripada anggaran yang dibangun dari ratusan akun.</p>
<h2>Dibantu Tim FA Indonesia</h2>
{bantu('Purwakarta', 'purwakarta', 'cfo')}
<p>Baca juga <a href="/akuntansi-manufaktur/">akuntansi manufaktur</a> dan ringkasan <a href="/psak/202/">PSAK 202</a>.</p>
''',
  faq=[('Apa itu anggaran fleksibel?', 'Anggaran yang dihitung ulang pada volume aktual dengan harga dan biaya per unit sesuai anggaran, sehingga selisih efisiensi bisa dipisahkan dari selisih volume.'),
       ('Apa beda anggaran dan prakiraan bergulir?', 'Anggaran adalah target tahunan yang tetap. Prakiraan bergulir adalah perkiraan terbaik yang diperbarui berkala dan selalu memandang 12 bulan ke depan.'),
       ('Bagaimana menghitung selisih volume penjualan?', 'Laba anggaran fleksibel pada volume aktual dikurangi laba anggaran statis. Hasilnya setara dengan selisih volume dikali margin kontribusi anggaran per unit.')])
