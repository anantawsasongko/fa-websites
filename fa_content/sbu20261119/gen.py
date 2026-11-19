# -*- coding: utf-8 -*-
"""Artikel 19 Nov 2026: Audit LK untuk SBU kontraktor. Menulis fa_content/articles/<slug>.json"""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'baru20261117'))
from _h import T

SLUG = 'audit-laporan-keuangan-sbu-kontraktor-syarat-dokumen-alur'

body = '''<p>Banyak kontraktor baru memikirkan audit ketika SBU hampir habis atau ketika ingin naik ke kualifikasi Menengah. Padahal pada aturan terbaru, neraca yang diaudit kantor akuntan publik (KAP) adalah bahan penilaian kemampuan keuangan untuk kualifikasi Menengah dan Besar. Artikel ini merangkum syaratnya, dokumen yang diminta auditor, urutan kerjanya, dan penyebab audit sering molor.</p>
<h2>Dasar Aturan: Permen PU 6 Tahun 2025</h2>
<p>Permen PU Nomor 6 Tahun 2025 adalah turunan PP 28/2025 dan menggantikan Permen PUPR 6/2021. Kualifikasi SBU sekarang lima tingkat: Kecil 1, Kecil 2, Kecil 3, Menengah, dan Besar. SBU yang terbit sebelum aturan ini perlu dikonversi sesuai masa transisi, jadi cek jadwalnya ke LSBU yang Anda pakai.</p>
''' + T(['Kualifikasi','Penjualan tahunan','Modal bersih minimal','Laporan keuangan'],[
 ['Kecil 1','Sampai Rp2 miliar','Rp300 juta','Neraca keuangan'],
 ['Kecil 2','Di atas Rp2 miliar sampai Rp7,5 miliar','Rp1 miliar','Neraca keuangan'],
 ['Kecil 3','Di atas Rp7,5 miliar sampai Rp15 miliar','Rp2,5 miliar','Neraca keuangan'],
 ['Menengah','Di atas Rp15 miliar sampai Rp50 miliar','Rp5 miliar','<b>Neraca diaudit KAP berizin</b>'],
 ['Besar','Di atas Rp50 miliar','Rp10 miliar','<b>Neraca diaudit KAP berizin</b>']]) + '''
<p>Angka di atas dirangkum dari materi sosialisasi dan ringkasan Permen, bukan dari teks pasalnya. Sebelum mengajukan, cocokkan dengan skema sertifikasi di LSBU Anda.</p>
<h2>Siapa yang Wajib Memakai Laporan Audit</h2>
<p>Kualifikasi Kecil cukup memakai neraca keuangan perusahaan. Kualifikasi Menengah dan Besar memakai neraca hasil audit KAP yang berizin. Badan usaha PMA, terintegrasi, dan KPBU masuk kualifikasi Besar, sehingga otomatis perlu laporan audit. Untuk perpanjangan SBU, materi sosialisasi menyebut laporan pajak tahunan terakhir sebagai dokumen tambahan.</p>
<p>Audit memenuhi syarat keuangan saja. SBU baru terbit bila syarat lain juga lengkap: penjualan tahunan, tenaga kerja bersertifikat SKK, peralatan, dan kelengkapan administrasi lain.</p>
<h2>Yang Dinilai: Ekuitas di Luar Tanah dan Bangunan</h2>
<p>Kemampuan keuangan dinilai dari modal usaha atau ekuitas yang tidak termasuk tanah dan bangunan. Karena yang dipakai adalah neraca hasil audit, angka acuannya adalah ekuitas setelah koreksi auditor, bukan angka di pembukuan internal. Ilustrasi berikut memperlihatkan bagaimana ekuitas yang terlihat cukup bisa berubah.</p>
''' + T(['Komponen (ilustrasi, bukan data klien)','Rp miliar'],[
 ['Ekuitas menurut pembukuan','7,5'],
 ['Koreksi piutang usaha dan retensi yang diragukan tertagih','(0,8)'],
 ['Koreksi pengakuan pendapatan dan biaya proyek','(0,7)'],
 ['Ekuitas setelah audit','6,0'],
 ['Dikurangi nilai tanah dan bangunan','(1,5)'],
 ['Ekuitas untuk penilaian kemampuan keuangan','4,5'],
 ['Batas minimal kualifikasi Menengah','5,0']]) + '''
<p>Dalam contoh ini, perusahaan merasa aman di angka 7,5 tetapi tidak memenuhi batas Menengah setelah audit. Lebih baik mengetahuinya sebelum LSBU yang menilai. Cara membaca ekuitas akhirnya tetap mengikuti skema LSBU, jadi konfirmasikan dulu.</p>
<h2>Pos yang Biasanya Dikoreksi pada Laporan Kontraktor</h2>
<ul>
<li><b>Piutang usaha dan retensi.</b> Retensi yang sudah lama tidak cair atau terkena sengketa perlu dievaluasi kemungkinan tertagihnya.</li>
<li><b>Pengakuan pendapatan per kontrak.</b> Pendapatan, aset kontrak, dan liabilitas kontrak mengikuti PSAK 115 (dulu PSAK 72). Pembahasan lengkapnya ada di <a href="/artikel/laporan-keuangan-kontraktor-psak-115/">artikel PSAK 115 untuk kontraktor</a>.</li>
<li><b>Biaya proyek dan persediaan material.</b> Biaya yang belum dibebankan ke proyek yang tepat, atau material sisa yang tidak dihitung, mengubah laba dan ekuitas.</li>
<li><b>Aset tetap dan alat berat.</b> Bukti kepemilikan, umur manfaat, dan penyusutan sering tidak konsisten dengan daftar alat yang dilaporkan.</li>
<li><b>Utang pemegang saham dan pihak berelasi.</b> Pinjaman pemilik yang tidak jelas statusnya memengaruhi ekuitas. Pilihannya dibahas di <a href="/artikel/utang-pemegang-saham-dijadikan-modal-atau-tetap-pinjaman/">artikel utang pemegang saham</a>.</li>
<li><b>Kas, bank, dan pajak.</b> Rekening yang tidak tercatat dan selisih pajak final jasa konstruksi dengan pembukuan adalah temuan yang sering muncul.</li></ul>
<h2>Dokumen yang Disiapkan untuk Auditor</h2>
''' + T(['Kelompok','Dokumen'],[
 ['Legal dan pajak','Akta dan perubahannya, NIB, SBU yang sedang berjalan, NPWP, SPT Tahunan beserta bukti lapor, SPT Masa PPh final dan PPN'],
 ['Keuangan','Buku besar dan neraca saldo, rekening koran seluruh bank, rekonsiliasi bank, daftar piutang dan retensi, daftar utang'],
 ['Proyek','Kontrak atau SPK beserta addendum, berita acara progres dan serah terima, invoice termin, laporan biaya per proyek, jaminan (garansi) yang diterbitkan'],
 ['Aset dan persediaan','Daftar aset tetap, bukti kepemilikan alat, hasil stock opname material'],
 ['Pinjaman dan pihak berelasi','Perjanjian kredit bank, perjanjian pinjaman pemegang saham, daftar transaksi dengan pihak berelasi']]) + '''
<h2>Alur Audit untuk Pengajuan atau Perpanjangan SBU</h2>
<ol><li><b>Hitung mundur dari tenggat SBU.</b> Tentukan tanggal SBU habis atau jadwal pengajuan ke LSBU, lalu sisakan waktu untuk audit dan perbaikan.</li>
<li><b>Rapikan pembukuan dan rekonsiliasi.</b> Kas, bank, piutang, dan biaya per proyek sebaiknya sudah cocok sebelum auditor datang.</li>
<li><b>Perikatan dengan KAP.</b> Sepakati tahun buku, ruang lingkup, dan jadwal kerja.</li>
<li><b>Pemeriksaan.</b> Auditor meminta data, mengirim konfirmasi, dan menelusuri bukti ke dokumen proyek.</li>
<li><b>Diskusi koreksi.</b> Selisih dibahas, dan pembukuan disesuaikan bila diperlukan.</li>
<li><b>Laporan auditor independen terbit.</b> Laporan dan neraca teraudit diunggah ke LSBU bersama dokumen lain.</li></ol>
<h2>Kenapa Audit Sering Molor</h2>
<p>Hampir selalu penyebabnya ada di tahap dua: data proyek tercecer di beberapa orang, rekening koran tidak lengkap, atau pembukuan baru dikerjakan sekaligus di akhir tahun. Auditor menunggu jawaban, jadwal bergeser, dan SBU habis lebih dulu. SBU yang sudah lewat masa berlakunya tidak bisa dipakai untuk pembuktian kualifikasi tender. Gejala yang sama dibahas di <a href="/artikel/laporan-audit-lama-keluar/">artikel laporan audit lama keluar</a>.</p>
<h2>Audit oleh KAP DHN &amp; Rekan</h2>
<p>Audit dilakukan tim KAP DHN &amp; Rekan, kantor akuntan publik yang terdaftar di OJK, dengan mengikuti Standar Audit dan kode etik profesi akuntan publik. Auditor bekerja independen: opini sepenuhnya kewenangan auditor dan tidak ada janji hasil tertentu. Jenis opini dan dampaknya ke pihak lain dijelaskan di <a href="/artikel/jenis-opini-audit-dan-dampaknya-ke-bank/">artikel jenis opini audit</a>. Untuk kebutuhan SBU, sampaikan kualifikasi yang dituju dan tenggatnya sejak awal supaya jadwal perikatan disusun mundur dari tanggal tersebut. Halaman <a href="/audit-laporan-keuangan-kontraktor/">audit laporan keuangan kontraktor</a> merangkum ruang lingkup audit untuk perusahaan konstruksi.</p>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Keterlambatan biasanya terjadi sebelum auditor memulai. Karena itu FA Indonesia mendampingi kontraktor merapikan data dan pembukuan sampai siap diaudit: rekonsiliasi kas dan bank, rekap piutang dan retensi per proyek, pengakuan pendapatan per kontrak, daftar aset, dan paket dokumen untuk auditor. Data yang sudah tertata membuat permintaan auditor terjawab lebih cepat, koreksi lebih sedikit, dan laporan audit tidak molor mendekati tenggat SBU.</p>
<p>Penyusunan laporan keuangan dikerjakan KJA Farhani K.N., sedangkan audit dilakukan KAP DHN &amp; Rekan. Keduanya pihak yang berbeda, sehingga independensi auditor tetap terjaga. Layanannya ada di <a href="/jasa-pendampingan-audit/">pendampingan audit</a> dan <a href="/laporan-keuangan-kontraktor/">laporan keuangan kontraktor</a>, dan mencakup seluruh Indonesia secara daring maupun kunjungan.</p>'''

D = 'Audit laporan keuangan untuk SBU kontraktor: syarat kualifikasi Menengah dan Besar, ekuitas minimal, dokumen untuk auditor, dan alur agar audit tidak molor.'
a = dict(
 slug=SLUG,
 seo_title='Audit LK untuk SBU Kontraktor: Syarat, Dokumen, Alur',
 title='Audit Laporan Keuangan untuk SBU Kontraktor: Syarat, Dokumen, dan Alur',
 description=D,
 keyword='audit laporan keuangan sbu kontraktor',
 category='Audit & KAP', minutes=7,
 cta={'href': '/audit-laporan-keuangan-kontraktor/', 'label': 'Audit Laporan Keuangan Kontraktor'},
 wa='Halo Pak Ananta, saya kontraktor dan perlu audit laporan keuangan untuk SBU. Boleh tanya syarat dan alurnya?',
 sources=[['https://industri.kontan.co.id/news/gapensi-soroti-peluang-kontraktor-lokal-dari-aturan-baru-proyek-pemerintah', 'Kontan, Gapensi Soroti Peluang Kontraktor Lokal dari Aturan Baru Proyek Pemerintah (14 Oktober 2026)'],
          ['https://www.slideshare.net/slideshow/sosialisasi-permen-pu-nomor-6-tahun-2025-regulasi-dan-perizinan-usaha-jasa-konstruksi/288944032', 'Materi Sosialisasi Permen PU 6/2025: Regulasi dan Perizinan Usaha Jasa Konstruksi']],
 related=['laporan-keuangan-kontraktor-psak-115', 'kapan-perusahaan-wajib-diaudit', 'laporan-audit-lama-keluar', 'jenis-opini-audit-dan-dampaknya-ke-bank'],
 body_html=body,
 faq=[
  ['Apakah SBU kualifikasi Kecil wajib diaudit KAP?', 'Menurut materi sosialisasi Permen PU 6/2025, kualifikasi Kecil cukup memakai neraca keuangan perusahaan. Audit KAP dipakai untuk kualifikasi Menengah dan Besar.'],
  ['Apakah tanah dan bangunan dihitung sebagai kemampuan keuangan?', 'Tidak. Kemampuan keuangan dinilai dari modal usaha atau ekuitas yang tidak termasuk tanah dan bangunan. Konfirmasikan cara hitungnya ke LSBU Anda.'],
  ['Berapa lama proses audit untuk SBU?', 'Tergantung ukuran perusahaan dan kesiapan data. Sebagian besar waktu hilang saat menunggu dokumen proyek, rekening koran, dan rekonsiliasi, jadi merapikan data lebih awal biasanya mempercepat.'],
  ['Apakah audit menjamin SBU terbit?', 'Tidak. Audit memenuhi syarat kemampuan keuangan. SBU juga membutuhkan penjualan tahunan, tenaga kerja bersertifikat, peralatan, dan kelengkapan administrasi.'],
  ['Perpanjangan SBU Menengah perlu audit lagi?', 'Kualifikasi Menengah dan Besar memakai neraca hasil audit, dan materi sosialisasi menyebut laporan pajak tahunan terakhir untuk perpanjangan. Pastikan ke LSBU dokumen mana yang diminta pada jadwal Anda.']])
s = json.dumps(a, ensure_ascii=False)
assert '—' not in s and '–' not in s
import re
words = len(re.sub(r'<[^>]+>', ' ', body).split())
print('title', len(a['title']), 'seo', len(a['seo_title']), 'desc', len(D), 'words', words)
out = os.path.join(HERE, '..', 'articles', SLUG + '.json')
json.dump(a, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', out)
