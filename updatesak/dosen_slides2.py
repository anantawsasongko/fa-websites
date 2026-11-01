# Bahan ajar tambahan (1 Nov 2026): SAK EMKM, PSAK 216, PSAK 212, PSAK 202, dan Menulis untuk Jurnal Scopus.
# Memakai helper dosen_slides; angka contoh adalah data ilustrasi yang dihitung di sini.
from dosen_slides import rp, table, note, flow, two

# ---------- SAK EMKM ----------
EM_LR = [("Pendapatan usaha", 480), ("Beban pokok penjualan", -288), ("Beban gaji karyawan", -60), ("Beban sewa tempat", -24),
         ("Beban listrik dan air", -12), ("Beban penyusutan peralatan", -10)]
EM_LB = sum(v for _, v in EM_LR)
EM_PAJ = -round(480 * 0.005, 1)  # PPh final 0,5% dari peredaran bruto (ilustrasi)
EM_NET = EM_LB + EM_PAJ


def em_lr(c, top):
    rows = [(a, rp(v)) for a, v in EM_LR] + [("Laba sebelum pajak", rp(EM_LB)), ("Beban pajak penghasilan (0,5% × pendapatan, ilustrasi)", rp(EM_PAJ, 1)), ("Laba setelah pajak", rp(EM_NET, 1))]
    y = table(c, ["Laporan Laba Rugi 2026 (Rp juta, data ilustrasi)", "Jumlah"], rows, [560, 150], 48, top, bold_rows=[6, 8], align_right=[1])
    note(c, "Gaji pemilik yang bekerja di usaha dicatat sebagai beban hanya bila memang dibayarkan sebagai gaji; pengambilan pribadi lain dicatat sebagai prive dan mengurangi ekuitas.", 48, y - 14, 864, "Perhatikan")


DEMKM = dict(slug="sak-emkm-laporan-keuangan-umkm", short="SAK EMKM", kick="Akuntansi Keuangan · Entitas Mikro, Kecil, dan Menengah",
             judul="SAK EMKM: Laporan Keuangan untuk Usaha Mikro, Kecil, dan Menengah", cover=["SAK EMKM: Laporan Keuangan", "Usaha Mikro, Kecil, Menengah"],
             sub="Siapa yang boleh memakai, tiga laporan, dan contoh angka", url="https://updatesak.com/update-sak-emkm/", psak=None,
             desk="Kriteria pengguna, asumsi dasar, tiga komponen laporan keuangan, dan contoh laba rugi toko roti.",
             slides=[
    dict(t="Tujuan Pembelajaran", k="Pertemuan ini", b=[
        "Menjelaskan entitas yang boleh memakai SAK EMKM dan kapan harus pindah ke SAK EP.",
        "Menyebutkan asumsi dasar: entitas bisnis, kelangsungan usaha, dasar akrual, biaya historis.",
        "Menyusun tiga komponen laporan keuangan SAK EMKM.",
        "Membedakan transaksi usaha dan transaksi pribadi pemilik."]),
    dict(t="Siapa yang Memakai SAK EMKM", k="Ruang lingkup", draw=two(
        ["Entitas tanpa akuntabilitas publik signifikan yang memenuhi kriteria usaha mikro, kecil, dan menengah menurut peraturan perundang-undangan.",
         "Boleh dipakai badan usaha maupun usaha perorangan yang ingin laporan keuangan rapi.",
         "Dirancang sederhana: sebagian besar pos diukur pada biaya historis."],
        ["Bila tidak lagi memenuhi kriteria, entitas beralih ke SAK EP (berlaku mulai 2025, pengganti SAK ETAP).",
         "Entitas boleh memilih SAK EP lebih awal bila butuh laporan yang lebih lengkap untuk bank atau investor.",
         "Perpindahan standar diungkapkan di catatan atas laporan keuangan."],
        "Pengguna", "Naik kelas")),
    dict(t="Tiga Komponen Laporan Keuangan", k="Isi laporan", draw=lambda c, top: table(c, ["Komponen", "Isi minimal", "Catatan"], [
        ("Laporan posisi keuangan", "Kas dan setara kas, piutang, persediaan, aset tetap, utang usaha, utang bank, ekuitas", "Pada akhir periode"),
        ("Laporan laba rugi", "Pendapatan, beban keuangan, beban pajak", "Untuk satu periode"),
        ("Catatan atas laporan keuangan", "Pernyataan kepatuhan pada SAK EMKM, ikhtisar kebijakan akuntansi, informasi tambahan pos material", "Ringkas tetapi wajib")], [250, 430, 184], 48, top)),
    dict(t="Contoh Laba Rugi Toko Roti", k="Data ilustrasi", draw=em_lr),
    dict(t="Kesalahan yang Sering Ditemukan", k="Praktik", b=[
        "Rekening usaha dan rekening pribadi tercampur sehingga pendapatan tidak bisa dicocokkan dengan mutasi bank.",
        "Peralatan dibebankan langsung saat dibeli, padahal seharusnya diakui sebagai aset dan disusutkan.",
        "Persediaan akhir tidak dihitung, sehingga harga pokok penjualan tidak akurat.",
        "Catatan atas laporan keuangan tidak dibuat sama sekali."]),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "Pemilik mengambil Rp3 juta dari kas toko untuk biaya sekolah anak. Bagaimana jurnalnya dan pengaruhnya ke laba?",
        "Toko membeli oven Rp24 juta dengan umur manfaat 4 tahun. Berapa beban penyusutan per tahun dan di mana oven disajikan?",
        "Kapan toko roti pada contoh sebaiknya beralih ke SAK EP?"]),
], ringkas=["SAK EMKM untuk entitas tanpa akuntabilitas publik signifikan yang memenuhi kriteria UMKM.",
            "Tiga komponen: posisi keuangan, laba rugi, catatan atas laporan keuangan.",
            "Asumsi entitas bisnis: transaksi pribadi pemilik dipisahkan sebagai prive.",
            "Bila sudah melewati kriteria, beralih ke SAK EP."])

# ---------- PSAK 216 Aset Tetap ----------
AT_COST, AT_RES, AT_LIFE = 120, 20, 5
SL = (AT_COST - AT_RES) / AT_LIFE
DDB = []
bv = AT_COST
for t in range(1, AT_LIFE + 1):
    d = bv * 2 / AT_LIFE if t < AT_LIFE else bv - AT_RES
    d = min(d, bv - AT_RES); DDB.append((t, bv, d, bv - d)); bv -= d


def at_tab(c, top):
    rows = [(f"Tahun {t}", rp(SL, 0), rp(b, 1), rp(d, 1), rp(e, 1)) for t, b, d, e in DDB]
    y = table(c, ["Tahun", "Garis lurus", "Saldo menurun: nilai awal", "Penyusutan 40%", "Nilai tercatat akhir"], rows, [120, 150, 230, 180, 184], 48, top, align_right=[1, 2, 3, 4])
    note(c, f"Garis lurus = ({AT_COST} − {AT_RES}) / {AT_LIFE} = {rp(SL)} per tahun. Saldo menurun ganda = 2/{AT_LIFE} × nilai tercatat awal, tidak boleh di bawah nilai residu Rp{AT_RES} juta; tahun terakhir disesuaikan.", 48, y - 14, 864, "Rumus")


D216 = dict(slug="psak-216-aset-tetap-penyusutan", short="PSAK 216", kick="Akuntansi Keuangan · Aset Tetap",
            judul="PSAK 216 Aset Tetap: Pengakuan, Pengukuran, dan Penyusutan", cover=["PSAK 216: Aset Tetap", "dan Penyusutan"],
            sub="Biaya perolehan, model biaya dan revaluasi, metode penyusutan", url="https://updatesak.com/psak/216/", psak=216,
            desk="Unsur biaya perolehan, model biaya dan revaluasi, perbandingan garis lurus dan saldo menurun ganda.",
            slides=[
    dict(t="Tujuan Pembelajaran", k="Pertemuan ini", b=[
        "Menentukan unsur biaya perolehan aset tetap (PSAK 216, dahulu PSAK 16, adopsi IAS 16).",
        "Membedakan model biaya dan model revaluasi.",
        "Menghitung penyusutan garis lurus dan saldo menurun ganda.",
        "Mengenali pengeluaran setelah perolehan: dikapitalisasi atau dibebankan."]),
    dict(t="Biaya Perolehan", k="Pengukuran awal", draw=two(
        ["Harga beli termasuk bea masuk dan pajak yang tidak dapat dikreditkan, setelah dikurangi diskon.",
         "Biaya yang dapat diatribusikan langsung: pengiriman, instalasi, uji coba, honorarium profesional.",
         "Estimasi awal biaya pembongkaran dan restorasi lokasi bila ada kewajiban."],
        ["Biaya pembukaan fasilitas baru dan promosi.", "Biaya pelatihan staf.", "Biaya administrasi dan overhead umum.",
         "Biaya relokasi atau reorganisasi."], "Termasuk", "Tidak termasuk")),
    dict(t="Model Biaya dan Model Revaluasi", k="Pengukuran setelah awal", draw=lambda c, top: table(c, ["Aspek", "Model biaya", "Model revaluasi"], [
        ("Nilai tercatat", "Biaya perolehan dikurangi akumulasi penyusutan dan rugi penurunan nilai", "Nilai wajar pada tanggal revaluasi dikurangi akumulasi penyusutan sesudahnya"),
        ("Kenaikan nilai", "Tidak diakui", "Masuk penghasilan komprehensif lain, surplus revaluasi di ekuitas"),
        ("Penurunan nilai", "Uji penurunan nilai (PSAK 236)", "Mengurangi surplus revaluasi dulu, sisanya ke laba rugi"),
        ("Konsistensi", "Untuk satu kelompok aset", "Seluruh kelompok aset direvaluasi, secara teratur")], [180, 330, 354], 48, top)),
    dict(t="Contoh Perhitungan Penyusutan", k="Data ilustrasi (Rp juta)", draw=at_tab),
    dict(t="Jurnal dan Pengeluaran Setelah Perolehan", k="Pencatatan", b=[
        f"Penyusutan tahun 1 garis lurus: Dr Beban Penyusutan Rp{rp(SL)} juta / Cr Akumulasi Penyusutan Rp{rp(SL)} juta.",
        "Penggantian komponen besar (misalnya mesin utama) dikapitalisasi; komponen lama dihentikan pengakuannya.",
        "Perawatan rutin dibebankan saat terjadi.",
        "Umur manfaat, nilai residu, dan metode ditelaah minimal setiap akhir tahun; perubahan diperlakukan prospektif."]),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "Perusahaan membeli mesin Rp100 juta, ongkos kirim Rp5 juta, instalasi Rp3 juta, dan pelatihan operator Rp2 juta. Berapa biaya perolehannya?",
        "Pada contoh, di tahun 3 umur manfaat diubah menjadi 6 tahun total. Hitung penyusutan garis lurus tahun 3.",
        "Tanah direvaluasi naik Rp50 juta. Bagaimana penyajiannya di laporan laba rugi dan penghasilan komprehensif lain?"]),
], ringkas=["Biaya perolehan mencakup semua biaya sampai aset siap digunakan.",
            "Pilih model biaya atau revaluasi per kelompok aset.",
            "Metode penyusutan mencerminkan pola pemakaian manfaat ekonomik.",
            "Estimasi ditelaah tiap tahun; perubahannya prospektif."])

# ---------- PSAK 212 Pajak Penghasilan ----------
LBA, DEP_K, DEP_F, DENDA, TR = 1000, 200, 300, 20, 0.22
PKP = LBA + DENDA - (DEP_F - DEP_K)
KINI = PKP * TR
DTL = (DEP_F - DEP_K) * TR
BEBAN = KINI + DTL


def pph_tab(c, top):
    rows = [("Laba sebelum pajak (akuntansi)", rp(LBA)), ("Beda permanen: denda pajak tidak dapat dikurangkan", rp(DENDA)),
            ("Beda temporer: penyusutan fiskal lebih besar dari komersial", rp(-(DEP_F - DEP_K))), ("Penghasilan kena pajak", rp(PKP)),
            ("Pajak kini (22%)", rp(KINI, 1)), ("Beban pajak tangguhan: 22% × 100", rp(DTL, 1)), ("Total beban pajak penghasilan", rp(BEBAN, 1))]
    y = table(c, ["Rekonsiliasi fiskal (Rp juta, data ilustrasi)", "Jumlah"], rows, [560, 150], 48, top, bold_rows=[3, 6], align_right=[1])
    note(c, f"Tarif efektif = {rp(BEBAN, 1)} / {LBA} = {BEBAN / LBA * 100:.2f}%".replace(".", ",") + ". Selisih dari 22% berasal dari beda permanen denda (22% × 20 = 4,4).", 48, y - 14, 864, "Tarif efektif")


D212 = dict(slug="psak-212-pajak-penghasilan-tangguhan", short="PSAK 212", kick="Akuntansi Keuangan · Pajak Penghasilan",
            judul="PSAK 212 Pajak Penghasilan: Pajak Kini dan Pajak Tangguhan", cover=["PSAK 212: Pajak Kini", "dan Pajak Tangguhan"],
            sub="Beda temporer, beda permanen, dan rekonsiliasi tarif efektif", url="https://updatesak.com/psak/212/", psak=212,
            desk="Beda temporer dan permanen, aset dan liabilitas pajak tangguhan, rekonsiliasi fiskal, dan tarif efektif.",
            slides=[
    dict(t="Tujuan Pembelajaran", k="Pertemuan ini", b=[
        "Membedakan beda temporer dan beda permanen (PSAK 212, dahulu PSAK 46, adopsi IAS 12).",
        "Menghitung pajak kini dari laba akuntansi melalui rekonsiliasi fiskal.",
        "Mengakui aset atau liabilitas pajak tangguhan.",
        "Menyusun rekonsiliasi tarif pajak efektif untuk CALK."]),
    dict(t="Beda Temporer dan Beda Permanen", k="Konsep", draw=two(
        ["Selisih waktu pengakuan antara akuntansi dan pajak yang akan berbalik di masa depan.",
         "Contoh: penyusutan, cadangan piutang, imbalan kerja yang belum dibayar.",
         "Menimbulkan aset atau liabilitas pajak tangguhan."],
        ["Selisih yang tidak akan pernah berbalik.", "Contoh: denda pajak, sumbangan tertentu, penghasilan yang sudah dikenai PPh final.",
         "Tidak menimbulkan pajak tangguhan, tetapi mengubah tarif efektif."], "Beda temporer", "Beda permanen")),
    dict(t="Aset dan Liabilitas Pajak Tangguhan", k="Pengakuan", b=[
        "Beda temporer kena pajak (dasar pengenaan pajak aset lebih kecil dari nilai tercatat) menimbulkan liabilitas pajak tangguhan.",
        "Beda temporer dapat dikurangkan menimbulkan aset pajak tangguhan, diakui sepanjang kemungkinan besar ada laba kena pajak di masa depan.",
        "Diukur dengan tarif yang diharapkan berlaku saat beda temporer berbalik.",
        "Tidak didiskontokan."]),
    dict(t="Contoh Rekonsiliasi Fiskal", k="Data ilustrasi", draw=pph_tab),
    dict(t="Jurnal Pajak Penghasilan", k="Pencatatan", draw=lambda c, top: table(c, ["Transaksi", "Debit", "Kredit", "Jumlah (Rp juta)"], [
        ("Pajak kini", "Beban pajak kini", "Utang pajak penghasilan", rp(KINI, 1)),
        ("Pajak tangguhan", "Beban pajak tangguhan", "Liabilitas pajak tangguhan", rp(DTL, 1))], [200, 230, 270, 164], 48, top, align_right=[3])),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "Perusahaan membentuk cadangan kerugian piutang Rp50 juta yang belum boleh dikurangkan secara fiskal. Apa dampaknya pada pajak tangguhan?",
        "Mengapa aset pajak tangguhan dari rugi fiskal tidak selalu boleh diakui?",
        "Pada contoh, bila denda pajak Rp0, berapa tarif efektifnya dan mengapa?"]),
], ringkas=["Beban pajak = pajak kini + pajak tangguhan.",
            "Beda temporer menimbulkan pajak tangguhan; beda permanen tidak.",
            "Aset pajak tangguhan diakui bila laba kena pajak masa depan cukup.",
            "Rekonsiliasi tarif efektif menjelaskan selisih dari tarif berlaku."])

# ---------- PSAK 202 Persediaan ----------
BUY = [("Saldo awal", 100, 10.0), ("Pembelian 10 Mar", 200, 11.0), ("Pembelian 20 Jun", 150, 12.0)]
SOLD = 300
UNITS = sum(q for _, q, _ in BUY); COST = sum(q * p for _, q, p in BUY)
AVG = COST / UNITS
FIFO_HPP = 100 * 10 + 200 * 11
FIFO_END = COST - FIFO_HPP
AVG_HPP = SOLD * AVG
AVG_END = COST - AVG_HPP
NRV_U = 11.0


def inv_tab(c, top):
    rows = [(a, f"{q}", rp(p, 1), rp(q * p, 0)) for a, q, p in BUY] + [("Tersedia dijual", f"{UNITS}", "", rp(COST))]
    y = table(c, ["Mutasi (Rp ribu per unit)", "Unit", "Harga", "Jumlah"], rows, [360, 120, 160, 224], 48, top, bold_rows=[3], align_right=[1, 2, 3])
    rows2 = [("FIFO (MPKP)", rp(FIFO_HPP), rp(FIFO_END)), ("Rata-rata tertimbang", rp(AVG_HPP, 1), rp(AVG_END, 1))]
    table(c, [f"Terjual {SOLD} unit", "Harga pokok penjualan", "Persediaan akhir (150 unit)"], rows2, [360, 250, 254], 48, y - 16, align_right=[1, 2])


D202 = dict(slug="psak-202-persediaan-fifo-rata-rata", short="PSAK 202", kick="Akuntansi Keuangan · Persediaan",
            judul="PSAK 202 Persediaan: Rumus Biaya dan Nilai Realisasi Neto", cover=["PSAK 202: Persediaan", "FIFO, Rata-rata, dan NRV"],
            sub="Biaya persediaan, rumus biaya, dan penurunan ke nilai realisasi neto", url="https://updatesak.com/psak/202/", psak=202,
            desk="Unsur biaya persediaan, FIFO dan rata-rata tertimbang, penurunan ke nilai realisasi neto, dan contoh angka.",
            slides=[
    dict(t="Tujuan Pembelajaran", k="Pertemuan ini", b=[
        "Menentukan biaya persediaan (PSAK 202, dahulu PSAK 14, adopsi IAS 2).",
        "Menerapkan rumus biaya FIFO dan rata-rata tertimbang; LIFO tidak diperkenankan.",
        "Mengukur persediaan pada nilai terendah antara biaya dan nilai realisasi neto.",
        "Mencatat penurunan nilai dan pemulihannya."]),
    dict(t="Biaya Persediaan", k="Pengukuran", draw=two(
        ["Biaya pembelian: harga beli, bea masuk, pajak tidak dapat dikreditkan, angkut masuk, dikurangi diskon.",
         "Biaya konversi: tenaga kerja langsung dan overhead produksi yang dialokasikan sistematis.",
         "Biaya lain sampai persediaan siap di lokasi dan kondisinya sekarang."],
        ["Pemborosan bahan, tenaga kerja, atau overhead yang tidak normal.", "Biaya penyimpanan, kecuali diperlukan dalam proses produksi.",
         "Overhead administrasi umum.", "Biaya penjualan."], "Termasuk", "Dibebankan saat terjadi")),
    dict(t="Contoh FIFO dan Rata-rata Tertimbang", k="Data ilustrasi", draw=inv_tab),
    dict(t="Nilai Realisasi Neto", k="Penurunan nilai", b=[
        "NRV = estimasi harga jual dikurangi estimasi biaya penyelesaian dan biaya penjualan.",
        f"Misal NRV per unit turun menjadi Rp{rp(NRV_U, 1)} ribu. Dengan FIFO, persediaan akhir 150 unit tercatat Rp{rp(FIFO_END)} ribu (Rp12 ribu per unit).",
        f"Penurunan = 150 × (12 − {rp(NRV_U, 0)}) = Rp{rp(150 * (12 - NRV_U))} ribu: Dr Beban Penurunan Nilai Persediaan / Cr Cadangan Penurunan Nilai Persediaan.",
        "Bila NRV pulih, penurunan dibalik maksimal sebesar yang pernah diakui."]),
    dict(t="Temuan Auditor yang Sering Muncul", k="Praktik audit", b=[
        "Stock opname akhir tahun tidak diobservasi atau selisihnya tidak ditelusuri.",
        "Barang usang dan lambat laku tidak dicadangkan.",
        "Pisah batas (cut-off) penerimaan dan pengiriman barang di sekitar tanggal neraca tidak tepat.",
        "Overhead pabrik dialokasikan dengan kapasitas aktual yang rendah sehingga biaya per unit menggelembung."]),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "Pada contoh, mengapa laba dengan FIFO lebih besar daripada rata-rata tertimbang saat harga naik?",
        "Barang dikirim FOB shipping point tanggal 30 Desember dan tiba 3 Januari. Masuk persediaan siapa per 31 Desember?",
        "Kapan penurunan nilai persediaan boleh dipulihkan dan bagaimana jurnalnya?"]),
], ringkas=["Biaya persediaan mencakup biaya pembelian, konversi, dan biaya lain sampai siap.",
            "Rumus biaya: FIFO atau rata-rata tertimbang; LIFO dilarang.",
            "Persediaan diukur pada nilai terendah antara biaya dan NRV.",
            "Penurunan nilai dapat dipulihkan, tidak melebihi jumlah semula."])

# ---------- Menulis untuk Jurnal Scopus ----------
DSC = dict(slug="menulis-dan-submit-artikel-jurnal-scopus", short="Publikasi", kick="Ruang Dosen · Publikasi Internasional",
           judul="Menulis dan Submit Artikel Akuntansi ke Jurnal Scopus", cover=["Menulis dan Submit Artikel", "ke Jurnal Scopus"],
           sub="Memilih jurnal, menyusun naskah, cover letter, dan membalas reviewer", url="https://updatesak.com/dosen/panduan-submit-scopus/", psak=None,
           desk="Langkah dari memilih jurnal sampai membalas reviewer, cocok untuk pelatihan internal prodi atau bimbingan mahasiswa S2 dan S3.",
           slides=[
    dict(t="Memilih Jurnal yang Tepat", k="Langkah 1", b=[
        "Mulai dari daftar pustaka naskah sendiri: jurnal yang paling sering Anda kutip biasanya paling cocok.",
        "Cek status di Scopus Sources: aktif, cakupan sampai tahun berjalan, dan bukan discontinued.",
        "Buka situs jurnal dari tautan di Scopus atau DOAJ, bukan dari email undangan, untuk menghindari jurnal yang dibajak.",
        "Baca aims and scope serta 3 sampai 5 artikel terbaru; cocokkan metode dan konteks negara."]),
    dict(t="Struktur Naskah yang Dibaca Editor", k="Langkah 2", draw=lambda c, top: table(c, ["Bagian", "Pertanyaan yang harus dijawab"], [
        ("Judul dan abstrak", "Apa temuan utamanya dan untuk siapa penting? Abstrak terstruktur bila jurnal memintanya"),
        ("Pendahuluan", "Celah riset apa yang diisi dan apa kontribusinya, dalam 3 sampai 4 paragraf"),
        ("Tinjauan pustaka dan hipotesis", "Teori apa yang dipakai dan bagaimana hipotesis diturunkan"),
        ("Metode", "Data, sampel, model, dan uji ketahanan yang bisa direplikasi"),
        ("Hasil dan pembahasan", "Apa artinya dibanding studi terdahulu, bukan sekadar mengulang tabel"),
        ("Kesimpulan", "Implikasi bagi regulator, praktisi, dan peneliti, serta keterbatasan")], [250, 614], 48, top)),
    dict(t="Konteks Indonesia sebagai Kekuatan", k="Kontribusi", b=[
        "Jelaskan kelembagaan yang khas: struktur kepemilikan keluarga, BUMN, regulasi OJK, adopsi SAK dan penomoran PSAK baru.",
        "Tunjukkan mengapa temuan di Indonesia memperluas atau menguji teori yang dibangun di negara maju.",
        "Hindari judul yang hanya mengganti nama negara dari studi lama tanpa argumen kelembagaan.",
        "Libatkan rekan penulis lintas negara bila memungkinkan."]),
    dict(t="Cover Letter dan Proses Submit", k="Langkah 3", b=[
        "Cover letter satu halaman: judul, pertanyaan riset, kontribusi utama, alasan cocok dengan jurnal, pernyataan orisinalitas.",
        "Siapkan file terpisah: halaman judul dengan identitas, naskah anonim, tabel, dan pernyataan konflik kepentingan.",
        "Ikuti format referensi jurnal sejak awal; editor sering desk reject karena format.",
        "Ungkapkan penggunaan alat AI sesuai kebijakan penerbit."]),
    dict(t="Membalas Reviewer", k="Langkah 4", b=[
        "Buat tabel respon: komentar reviewer, tanggapan, dan lokasi perubahan di naskah (halaman dan baris).",
        "Ucapkan terima kasih secukupnya, lalu jawab substansi; jangan defensif.",
        "Bila tidak setuju, beri argumen dan rujukan, dan tawarkan kompromi.",
        "Tandai perubahan di naskah revisi dengan warna atau track changes sesuai permintaan editor."]),
    dict(t="Etika Publikasi", k="Wajib dijaga", b=[
        "Tidak mengirim naskah yang sama ke dua jurnal sekaligus.",
        "Cek similarity sebelum submit, termasuk terhadap tesis atau prosiding sendiri.",
        "Kepengarangan sesuai kontribusi nyata; tidak ada penulis titipan.",
        "Hindari jurnal yang menjanjikan terbit cepat dengan biaya tinggi tanpa review yang jelas."]),
], ringkas=["Pilih jurnal dari daftar pustaka sendiri dan verifikasi di Scopus Sources.",
            "Kontribusi dan konteks kelembagaan Indonesia adalah nilai jual naskah.",
            "Cover letter singkat, file lengkap, format sesuai pedoman.",
            "Balas reviewer dengan tabel respon yang rapi dan argumen yang sopan."])

DECKS = [DEMKM, D216, D212, D202, DSC]
