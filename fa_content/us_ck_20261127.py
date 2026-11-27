"""27 Nov 2026: isi unik 11 halaman prioritas UpdateSAK (contoh angka/kasus + kesalahan umum).

Ditulis ulang oleh tim, bukan kutipan teks standar. Angka adalah ilustrasi.
Kunci = path di out/updatesak. Nilai = (judul contoh, html contoh, daftar kesalahan).
Dipakai tiga_niat_20261127.py (blok <!--us-ck27-->).
"""


def tbl(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return ('<div style="overflow-x:auto"><table style="width:100%%;border-collapse:collapse;margin:10px 0 6px;font-size:15px">'
            "<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b))


CK = {
    "psak/105": (
        "Contoh Angka: Gudang yang Akan Dijual",
        "<p>Ilustrasi: direksi memutuskan menjual satu gudang, sudah menunjuk agen, dan menargetkan penjualan selesai dalam 12 bulan. "
        "Biaya perolehan gudang Rp6.000 juta, akumulasi penyusutan Rp1.800 juta, jadi jumlah tercatatnya Rp4.200 juta. "
        "Nilai wajar Rp4.000 juta dan biaya untuk menjual Rp150 juta, sehingga nilai wajar dikurangi biaya menjual Rp3.850 juta.</p>"
        "<p>Gudang diukur pada angka yang lebih rendah, yaitu Rp3.850 juta. Selisih Rp350 juta diakui sebagai rugi penurunan nilai pada saat reklasifikasi.</p>"
        + tbl(["Jurnal Saat Reklasifikasi (Rp juta)", "Debit", "Kredit"], [
            ["Aset dimiliki untuk dijual", "3.850", ""],
            ["Akumulasi penyusutan gudang", "1.800", ""],
            ["Rugi penurunan nilai", "350", ""],
            ["Aset tetap: gudang", "", "6.000"]])
        + "<p>Sejak tanggal itu gudang tidak disusutkan lagi dan disajikan terpisah di aset lancar. "
        "Bila kemudian terjual dengan hasil bersih Rp3.900 juta, laba penjualan yang diakui Rp50 juta.</p>",
        ["Gudang atau mesin yang menganggur langsung dipindah ke pos ini padahal belum ada keputusan menjual dan belum dipasarkan secara aktif.",
         "Sudah lewat 12 bulan belum terjual, tetapi klasifikasinya tidak ditinjau ulang dan alasan keterlambatannya tidak didokumentasikan.",
         "Kenaikan nilai wajar setelah reklasifikasi diakui melebihi rugi penurunan nilai yang pernah dicatat.",
         "Liabilitas yang terkait langsung dengan aset itu digabung (saling hapus) dengan asetnya, padahal harus disajikan terpisah."]),
    "psak/220": (
        "Contoh Angka: Hibah untuk Pembelian Mesin",
        "<p>Ilustrasi: perusahaan membeli mesin Rp1.000 juta dengan umur manfaat 5 tahun dan menerima hibah pemerintah Rp600 juta untuk mesin itu. "
        "Syarat hibah sudah dipenuhi dan kasnya sudah diterima. Ada dua cara penyajian yang sama-sama diperbolehkan.</p>"
        + tbl(["Per Tahun (Rp juta)", "Penghasilan Ditangguhkan", "Pengurang Aset"], [
            ["Nilai mesin di neraca saat perolehan", "1.000", "400"],
            ["Penghasilan ditangguhkan saat perolehan", "600", "0"],
            ["Beban penyusutan", "200", "80"],
            ["Penghasilan hibah yang diakui", "120", "0"],
            ["Beban bersih di laba rugi", "80", "80"]])
        + "<p>Pada cara pertama jurnalnya: debit kas Rp600 juta, kredit penghasilan ditangguhkan Rp600 juta; lalu setiap tahun debit penghasilan ditangguhkan Rp120 juta, kredit penghasilan hibah Rp120 juta. "
        "Laba bersihnya sama pada kedua cara. Yang berbeda adalah total aset dan liabilitas, jadi rasio yang dibaca bank ikut berbeda.</p>",
        ["Seluruh hibah diakui sebagai pendapatan pada saat kas diterima, padahal manfaatnya untuk beberapa tahun.",
         "Hibah dicatat sebelum ada keyakinan memadai bahwa syaratnya dipenuhi dan dananya akan diterima.",
         "Pinjaman pemerintah berbunga di bawah pasar dicatat sebesar kas yang diterima tanpa memisahkan manfaat bunga rendahnya.",
         "Hibah dicatat langsung ke ekuitas, atau syarat yang belum dipenuhi tidak diungkapkan di CALK."]),
    "psak/116": (
        "Contoh Angka: Sewa Ruko 3 Tahun",
        "<p>Ilustrasi: perusahaan menyewa ruko selama 3 tahun dengan pembayaran Rp120 juta setiap akhir tahun. Suku bunga pinjaman inkremental 10% per tahun. "
        "Nilai kini tiga pembayaran itu Rp298,4 juta. Angka ini menjadi aset hak guna sekaligus liabilitas sewa pada awal masa sewa.</p>"
        + tbl(["Tahun (Rp juta)", "Bunga 10%", "Pembayaran", "Pokok", "Liabilitas Akhir", "Penyusutan"], [
            ["1", "29,8", "120,0", "90,2", "208,3", "99,5"],
            ["2", "20,8", "120,0", "99,2", "109,1", "99,5"],
            ["3", "10,9", "120,0", "109,1", "0,0", "99,5"]])
        + "<p>Beban tahun pertama Rp129,3 juta (bunga Rp29,8 juta ditambah penyusutan Rp99,5 juta), lebih tinggi dari uang sewa Rp120 juta, lalu menurun di tahun berikutnya. "
        "Total beban selama 3 tahun tetap Rp360 juta. Liabilitas sewa ikut dihitung sebagai utang oleh analis kredit.</p>",
        ["Opsi perpanjangan yang hampir pasti diambil tidak dimasukkan ke masa sewa, sehingga aset dan liabilitas terlalu kecil.",
         "Memakai suku bunga deposito atau angka kira-kira, bukan suku bunga pinjaman inkremental yang bisa dijelaskan sumbernya.",
         "Pengecualian sewa jangka pendek dipakai untuk kontrak yang jelas diperpanjang setiap tahun.",
         "Komponen jasa (service charge, perawatan) ikut dikapitalisasi tanpa dipisah, dan pembayaran di muka atau deposit tidak dimasukkan ke aset hak guna."]),
    "psak/118": (
        "Contoh Angka: Laba Rugi dengan Tiga Kategori",
        "<p>Ilustrasi untuk perusahaan dagang (bukan bank dan bukan perusahaan investasi). PSAK 118 berlaku untuk periode yang dimulai 1 Januari 2027 dan meminta penghasilan serta beban dikelompokkan ke kategori operasi, investasi, dan pendanaan, dengan dua subtotal wajib.</p>"
        + tbl(["Pos (Rp juta)", "Jumlah", "Kategori"], [
            ["Pendapatan", "10.000", "Operasi"],
            ["Beban pokok penjualan", "(6.000)", "Operasi"],
            ["Beban penjualan dan administrasi", "(2.200)", "Operasi"],
            ["<b>Laba operasi</b>", "<b>1.800</b>", "Subtotal wajib"],
            ["Bagian laba entitas asosiasi", "100", "Investasi"],
            ["Bunga deposito", "50", "Investasi"],
            ["<b>Laba sebelum pendanaan dan pajak penghasilan</b>", "<b>1.950</b>", "Subtotal wajib"],
            ["Bunga pinjaman bank", "(350)", "Pendanaan"],
            ["Laba sebelum pajak", "1.600", ""],
            ["Beban pajak penghasilan (22%)", "(352)", ""],
            ["Laba tahun berjalan", "1.248", ""]])
        + "<p>Laba bersihnya tidak berubah dibanding format lama. Yang berubah adalah letak pos dan subtotalnya, jadi angka laba operasi di kovenan bank dan bonus manajemen perlu dicek ulang definisinya.</p>",
        ["Seluruh selisih kurs ditaruh di operasi, padahal selisih kurs mengikuti kategori pos yang menimbulkannya (misalnya selisih kurs pinjaman masuk pendanaan).",
         "Ukuran kinerja buatan manajemen seperti EBITDA disesuaikan dipakai di paparan publik tanpa pengungkapan dan rekonsiliasinya di CALK.",
         "Pos lain-lain bernilai besar dibiarkan tanpa dirinci, padahal standar meminta agregasi dan disagregasi yang bermakna.",
         "Periode pembanding tidak disajikan ulang saat pertama kali menerapkan."]),
    "standar-audit/sa-700": (
        "Contoh Kasus: Urutan Tanggal Sebelum Opini Diterbitkan",
        "<p>Ilustrasi: materialitas keseluruhan Rp500 juta. Setelah koreksi, salah saji yang tidak dikoreksi tersisa Rp80 juta, tidak ada pembatasan lingkup, dan pengungkapan sudah memadai. "
        "Auditor menyimpulkan laporan keuangan bebas dari salah saji material, sehingga opininya tanpa modifikasian.</p>"
        + tbl(["Urutan", "Peristiwa", "Catatan"], [
            ["1", "Pekerjaan lapangan dan reviu kertas kerja selesai", "Bukti audit cukup dan tepat sudah diperoleh"],
            ["2", "Direksi menyetujui laporan keuangan final", "Termasuk seluruh catatan atas laporan keuangan"],
            ["3", "Surat representasi manajemen ditandatangani", "Tanggalnya sedekat mungkin dengan laporan auditor, tidak sesudahnya"],
            ["4", "Laporan auditor diberi tanggal dan ditandatangani", "Tidak boleh lebih awal dari butir 1 sampai 3"]])
        + "<p>Susunan laporannya: opini di bagian paling atas, lalu basis opini, tanggung jawab manajemen dan pihak yang bertanggung jawab atas tata kelola, serta tanggung jawab auditor. Hal audit utama ditambahkan untuk entitas yang wajib menurut SA 701.</p>",
        ["Laporan auditor bertanggal lebih awal dari surat representasi atau dari persetujuan direksi atas laporan keuangan.",
         "Kerangka pelaporan keuangan disebut tidak tepat, misalnya menulis Standar Akuntansi Keuangan di Indonesia padahal entitas memakai SAK EP atau SAK EMKM.",
         "Bagian basis opini tidak memuat pernyataan independensi dan kepatuhan etika.",
         "Informasi lain dalam laporan tahunan tidak dibaca, padahal bagian itu ikut dilaporkan menurut SA 720."]),
    "standar-audit/sa-250": (
        "Contoh Kasus: Dua Kelompok Peraturan",
        "<p>Ilustrasi pada audit rumah sakit swasta. SA 250 membedakan dua kelompok peraturan, dan kedalaman prosedurnya berbeda.</p>"
        + tbl(["Kelompok", "Contoh", "Yang Dilakukan Auditor"], [
            ["Berdampak langsung pada angka dan pengungkapan", "Pajak penghasilan, PPN, imbalan kerja menurut aturan ketenagakerjaan", "Memperoleh bukti yang cukup dan tepat atas kepatuhannya"],
            ["Tidak berdampak langsung, tetapi penting bagi kelangsungan operasi", "Izin operasional rumah sakit, izin lingkungan, akreditasi", "Bertanya kepada manajemen dan membaca korespondensi dengan regulator"]])
        + "<p>Misalnya izin operasional habis masa berlakunya tiga bulan sebelum tanggal neraca dan perpanjangannya masih diproses. Auditor menilai kemungkinan denda atau penghentian layanan, "
        "dampaknya pada asumsi kelangsungan usaha, kecukupan pengungkapan di CALK, lalu mengomunikasikannya kepada pihak yang bertanggung jawab atas tata kelola.</p>",
        ["Hanya mengandalkan representasi manajemen tanpa membaca surat dari kantor pajak, dinas kesehatan, atau regulator lain.",
         "Notulen rapat direksi dan komisaris tidak dibaca, padahal sering memuat masalah perizinan dan sengketa.",
         "Ketidakpatuhan yang ditemukan tidak dinilai dampaknya pada risiko kecurangan dan integritas manajemen.",
         "Temuan tidak didokumentasikan dan tidak dikomunikasikan kepada tingkat manajemen yang tepat."]),
    "standar-audit/sa-260": (
        "Contoh Kasus: PT Keluarga tanpa Komite Audit",
        "<p>Ilustrasi: sebuah PT keluarga dipimpin direktur utama yang juga pemegang saham mayoritas, dengan satu komisaris dari keluarga yang sama dan tanpa komite audit. "
        "Langkah pertama auditor adalah menetapkan siapa pihak yang bertanggung jawab atas tata kelola. Di sini pihak itu adalah dewan komisaris. "
        "Bila semua anggotanya juga terlibat mengelola perusahaan, hal yang sudah disampaikan kepada mereka sebagai manajemen tidak perlu diulang, selama auditor yakin semuanya sudah mendapat informasi.</p>"
        + tbl(["Waktu", "Yang Dikomunikasikan"], [
            ["Perencanaan", "Tanggung jawab auditor, gambaran ruang lingkup dan jadwal audit, risiko signifikan yang diidentifikasi"],
            ["Selama audit", "Kesulitan signifikan, misalnya data terlambat atau akses dibatasi"],
            ["Penyelesaian", "Pandangan atas kebijakan dan estimasi akuntansi, salah saji yang tidak dikoreksi, representasi tertulis yang diminta, rencana modifikasi opini bila ada"]]),
        ["Temuan signifikan hanya disampaikan lisan tanpa notulen atau surat, sehingga tidak ada bukti komunikasi di kertas kerja.",
         "Komunikasi baru dilakukan setelah laporan auditor terbit, sehingga tata kelola tidak sempat menanggapi.",
         "Surat kelemahan pengendalian internal (SA 265) dianggap sudah mewakili seluruh komunikasi SA 260.",
         "Pihak yang bertanggung jawab atas tata kelola tidak ditetapkan sejak awal, sehingga komunikasi berhenti di staf keuangan."]),
    "standar-audit/sa-450": (
        "Contoh Angka: Ikhtisar Salah Saji",
        "<p>Ilustrasi: materialitas keseluruhan Rp500 juta dan batas jelas tidak signifikan Rp25 juta. Salah saji di atas batas itu dikumpulkan dalam satu ikhtisar.</p>"
        + tbl(["Salah Saji", "Jenis", "Dampak pada Laba Sebelum Pajak (Rp juta)"], [
            ["Penjualan Januari dicatat di Desember (pisah batas)", "Faktual", "Lebih saji 120"],
            ["Cadangan kerugian piutang kurang", "Pertimbangan", "Lebih saji 90"],
            ["Selisih persediaan dari sampel, diproyeksikan ke populasi", "Proyeksi", "Lebih saji 60"],
            ["<b>Jumlah</b>", "", "<b>Lebih saji 270</b>"]])
        + "<p>Auditor meminta manajemen mengoreksi semuanya. Misalkan hanya pisah batas yang dikoreksi, maka sisa Rp150 juta masih di bawah materialitas. "
        "Tetapi angka bukan satu-satunya ukuran: bila Rp150 juta itu mengubah rugi menjadi laba atau membuat rasio kovenan bank terlihat terpenuhi, salah saji tersebut bisa material karena sifatnya. "
        "Salah saji yang tidak dikoreksi dilampirkan pada surat representasi dan dikomunikasikan kepada pihak yang bertanggung jawab atas tata kelola.</p>",
        ["Salah saji dinilai satu per satu dan tidak pernah dijumlahkan.",
         "Salah saji di pos yang berbeda saling dihapuskan, sehingga lebih saji pendapatan tertutup oleh lebih saji beban.",
         "Salah saji tahun lalu yang tidak dikoreksi tidak diperhitungkan dampaknya pada tahun berjalan.",
         "Materialitas tidak ditinjau ulang ketika laba aktual jauh lebih kecil dari angka yang dipakai saat perencanaan."]),
    "standar-audit/sa-705": (
        "Contoh Angka: Menentukan Jenis Modifikasi",
        "<p>Ilustrasi: materialitas keseluruhan Rp500 juta dan total aset Rp20 miliar. Jenis opini bergantung pada dua hal: sifat masalahnya (salah saji atau bukti tidak cukup) dan apakah dampaknya pervasif.</p>"
        + tbl(["Situasi", "Penilaian", "Opini"], [
            ["Piutang tak tertagih Rp900 juta tidak dicadangkan dan manajemen menolak koreksi", "Salah saji material, terbatas pada satu pos", "Wajar dengan pengecualian"],
            ["Entitas anak yang menyumbang 70% aset tidak dikonsolidasi", "Salah saji material dan pervasif", "Tidak wajar"],
            ["Persediaan Rp3 miliar (15% aset) tidak bisa diobservasi dan prosedur alternatif tidak memadai", "Bukti tidak cukup, dampak mungkin material tetapi tidak pervasif", "Wajar dengan pengecualian"],
            ["Catatan akuntansi sebagian besar hilang, saldo utama tidak bisa diverifikasi", "Bukti tidak cukup, dampak mungkin material dan pervasif", "Tidak menyatakan pendapat"]])
        + "<p>Bagian basis opini menjelaskan masalahnya dan, bila bisa dihitung, menyebut dampak rupiahnya pada pos yang terpengaruh. Bank biasanya membaca bagian ini lebih dulu sebelum angka lainnya.</p>",
        ["Dampak salah saji tidak dikuantifikasi di basis opini padahal angkanya bisa dihitung.",
         "Paragraf penekanan suatu hal dipakai sebagai pengganti modifikasi opini.",
         "Langsung tidak menyatakan pendapat padahal prosedur alternatif masih bisa dilakukan.",
         "Pembatasan lingkup dari manajemen tidak dikomunikasikan lebih dulu kepada pihak yang bertanggung jawab atas tata kelola."]),
    "standar-audit/spa-3420": (
        "Contoh Kasus: Proforma Akuisisi dalam Prospektus",
        "<p>Ilustrasi: calon emiten mengakuisisi satu perusahaan setelah tanggal laporan keuangan terakhir. Prospektus memuat informasi keuangan proforma yang menunjukkan posisi keuangan seolah-olah akuisisi terjadi pada tanggal laporan itu.</p>"
        + tbl(["Kolom", "Isi", "Sumber"], [
            ["Informasi keuangan yang belum disesuaikan", "Laporan keuangan historis emiten", "Laporan yang sudah diaudit atau direviu"],
            ["Penyesuaian proforma", "Angka perusahaan target, harga beli, goodwill, pendanaan akuisisi", "Perjanjian jual beli, laporan penilai, perjanjian kredit"],
            ["Proforma", "Penjumlahan dua kolom di atas", "Dihitung ulang oleh praktisi"]])
        + "<p>Yang menyusun proforma adalah pihak yang bertanggung jawab di emiten. Praktisi melaporkan apakah kompilasinya, dalam semua hal yang material, sudah mengikuti kriteria yang berlaku. "
        "Praktisi tidak memberi opini baru atas angka historis dan tidak menjamin hasil aktual akan sama dengan proforma.</p>",
        ["Penyesuaian memasukkan hal yang belum didukung fakta, misalnya penghematan sinergi yang masih rencana.",
         "Angka perusahaan target diambil dari laporan yang belum diaudit atau direviu tanpa prosedur tambahan atas sumbernya.",
         "Kebijakan akuntansi perusahaan target tidak diselaraskan dengan kebijakan emiten.",
         "Catatan penjelasan proforma tidak menyebut asumsi dan sumber setiap penyesuaian."]),
    "standar-audit/sjt-4400": (
        "Contoh Kasus: Prosedur yang Disepakati atas Piutang",
        "<p>Ilustrasi: bank meminta debitur menyampaikan laporan prosedur yang disepakati atas piutang usaha sebelum menambah plafon. Prosedurnya disepakati lebih dulu dengan pihak yang menugaskan, lalu praktisi melaporkan temuan apa adanya.</p>"
        + tbl(["Prosedur yang Disepakati", "Temuan Faktual"], [
            ["Mencocokkan jumlah daftar umur piutang dengan saldo buku besar per 30 September", "Jumlahnya sama, Rp8.420 juta"],
            ["Mengirim konfirmasi ke 20 saldo terbesar", "17 jawaban sesuai, 2 jawaban berselisih total Rp35 juta, 1 tidak dijawab"],
            ["Menghitung porsi piutang berumur di atas 90 hari", "Rp1.260 juta atau 15% dari jumlah piutang"]])
        + "<p>Laporan berhenti di temuan. Praktisi tidak memberi opini dan tidak menyimpulkan apakah piutang itu wajar; penilaiannya diserahkan kepada bank sebagai pemakai laporan. "
        "Karena itu laporan ini tidak bisa menggantikan laporan audit bila yang diminta adalah laporan keuangan audited.</p>",
        ["Prosedur ditulis dengan kata yang tidak terukur seperti menelaah, menganalisis, atau memastikan kewajaran.",
         "Laporan memuat kesimpulan atau opini, padahal isinya harus terbatas pada temuan faktual.",
         "Surat perikatan tidak menyebut tujuan perikatan dan siapa yang dimaksudkan memakai laporannya.",
         "Dipakai untuk memenuhi syarat tender atau bank yang sebenarnya meminta laporan audit."]),
}
