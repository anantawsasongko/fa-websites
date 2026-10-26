# -*- coding: utf-8 -*-
"""Cluster SEO jasa implementasi PSAK (26 Okt 2026, setelah lead WA implementasi PSAK 118 dari Threads).
- Hub /jasa-implementasi-psak/
- Halaman per standar: PSAK 109, 115, 116, 117, 212, 219, 110 (konsolidasi), transisi SAK EP ke PSAK
- Kotak CTA di artikel terkait, blok di /layanan/, sitemap, llms.txt
Penomoran PSAK mengikuti SAK Online IAI (berlaku sejak 1 Januari 2024).
Idempoten. Jalankan setelah fa_lead_20261026.py, sebelum prep.py.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
exec(_src[:_src.index("# ================= 1.")])  # helper: P, rd, wtxt, svc_page, tbl, flow, E, D, TODAY

HUB = "/jasa-implementasi-psak/"
WA_MSG = "Halo FA Indonesia, kami ingin konsultasi implementasi {}."
KERJA = ("<h2>Alur Kerja</h2>" + flow([
    ("Diskusi awal", "Gratis, 30 sampai 45 menit lewat video call."),
    ("NDA", "Data dikirim setelah NDA ditandatangani."),
    ("Diagnosis", "Gap assessment dan rencana kerja tertulis."),
    ("Implementasi", "Kebijakan, perhitungan, jurnal, dan template."),
    ("Siap audit", "Memo dan bukti pendukung untuk auditor.")]))
SIAPA = ("<h2>Siapa yang Menangani</h2><p>Ditangani tim Chartered Accountant dan CPA "
         "yang mengikuti SAK terbaru dan memahami cara kerja auditor, termasuk auditor KAP besar. Audit tetap dilakukan KAP independen; "
         "bila dibutuhkan, kami bantu menghubungkan dengan KAP berizin yang sesuai.</p>")
def baca(links):
    return "<h2>Bacaan Terkait</h2><ul>" + "".join(f'<li><a href="{u}">{E(t)}</a></li>' for u, t in links) + "</ul>"
FAQ_BIAYA = ("Berapa biaya pendampingannya?", "Bergantung pada jumlah entitas, volume transaksi, dan kondisi data. Angka pasti disampaikan setelah diskusi awal dan diagnosis singkat, sebelum Anda berkomitmen.")
FAQ_AUDIT = ("Apakah FA Indonesia sekaligus mengaudit?", "Tidak. Kami mendampingi implementasi dan penyusunan. Audit dilakukan KAP independen, dan kami menyiapkan paket pendukung agar audit lancar.")

PAGES = []  # (path, short, label untuk tabel hub, untuk siapa)
def page(path, std, judul, short, siapa, lead, why, scope, cocok, faq, title, desc, svc_type, related):
    body = (f"<h2>Kenapa Sering Jadi Temuan Audit</h2><p>{why}</p>"
            "<h2>Ruang Lingkup Pendampingan</h2>" + tbl(["Tahap", "Yang Dikerjakan", "Hasil"], scope)
            + KERJA + "<h2>Siapa yang Cocok</h2><ul>" + "".join(f"<li>{c}</li>" for c in cocok) + "</ul>"
            + SIAPA + baca([(HUB, "Semua Layanan Implementasi PSAK")] + related))
    svc_page(path, "Layanan · Standar Akuntansi", judul, lead, body, faq + [FAQ_AUDIT, FAQ_BIAYA], title, desc,
             f"Jasa Implementasi {std}", svc_type, HUB, "Semua Layanan PSAK", WA_MSG.format(std), f"Implementasi {std}")
    PAGES.append((path, std, short, siapa))

# ---------- PSAK 109 ----------
page("/jasa-implementasi-psak-109/", "PSAK 109", "Jasa Implementasi PSAK 109 Instrumen Keuangan: Klasifikasi, CKPN, dan Model ECL",
 "Instrumen keuangan, CKPN/ECL", "Pembiayaan, fintech, koperasi besar, perusahaan dengan piutang besar",
 "Pendampingan penerapan PSAK 109 Instrumen Keuangan: klasifikasi dan pengukuran aset keuangan, uji SPPI dan model bisnis, model kerugian kredit ekspektasian (ECL) untuk CKPN, sampai pengungkapan risiko kredit.",
 "Model ECL sering dibuat sekali lalu tidak diperbarui. Auditor akan menanyakan data historis gagal bayar, faktor makroekonomi forward looking, kriteria kenaikan risiko kredit signifikan (stage 1, 2, 3), dan alasan setiap asumsi. Tanpa dokumentasi, CKPN mudah dikoreksi dan berdampak langsung ke laba.",
 [("Gap assessment", "Inventarisasi aset dan liabilitas keuangan, kebijakan CKPN berjalan, data historis", "Daftar celah dan prioritas"),
  ("Klasifikasi", "Uji model bisnis dan SPPI, biaya perolehan diamortisasi, FVOCI, FVTPL", "Matriks klasifikasi per instrumen"),
  ("Model ECL", "Segmentasi portofolio, PD, LGD, EAD atau matriks provisi untuk piutang usaha, skenario makro", "Model Excel yang bisa diperbarui sendiri"),
  ("Staging", "Kriteria SICR, hari tunggakan, restrukturisasi, write off", "Memo kebijakan staging"),
  ("Pengungkapan", "Rekonsiliasi CKPN, analisis umur, sensitivitas", "Draf CALK risiko kredit")],
 ["Perusahaan pembiayaan, fintech, dan perusahaan sistem pembayaran.",
  "Koperasi simpan pinjam besar dan lembaga keuangan yang menerapkan SAK Indonesia.",
  "Distributor, kontraktor, dan rumah sakit dengan piutang usaha besar.",
  "Grup usaha dengan pinjaman antarperusahaan dan instrumen derivatif sederhana."],
 [("Apakah piutang usaha biasa perlu model ECL?", "Ya, tetapi PSAK 109 mengizinkan pendekatan yang disederhanakan untuk piutang usaha tanpa komponen pendanaan signifikan, misalnya matriks provisi berdasarkan umur piutang yang disesuaikan dengan informasi forward looking."),
  ("Sejak kapan PSAK 109 berlaku?", "Sejak 1 Januari 2020, saat itu dengan nomor PSAK 71. Sejak 1 Januari 2024 penomorannya menjadi PSAK 109 sesuai SAK Online IAI.")],
 "Jasa Implementasi PSAK 109 Instrumen Keuangan & Model ECL | FA Indonesia",
 "Konsultan PSAK 109: klasifikasi aset keuangan, uji SPPI, model ECL dan CKPN, staging, pengungkapan risiko kredit. Ditangani tim CPA. Seluruh Indonesia.",
 "Financial instruments and expected credit loss implementation (IFRS 9)",
 [("/artikel/daftar-psak-isak-2026-2027/", "Daftar PSAK dan ISAK yang Berlaku 2026 sampai 2027"), ("/artikel/amendemen-psak-109-107-berlaku-2026/", "Amendemen PSAK 109 dan PSAK 107 yang Berlaku 2026")])

# ---------- PSAK 115 ----------
page("/jasa-implementasi-psak-115/", "PSAK 115", "Jasa Implementasi PSAK 115 Pendapatan dari Kontrak dengan Pelanggan",
 "Pengakuan pendapatan kontrak", "Kontraktor, developer, rumah sakit, software dan langganan",
 "Pendampingan penerapan PSAK 115: lima langkah pengakuan pendapatan, identifikasi kewajiban pelaksanaan, alokasi harga transaksi, pengakuan sepanjang waktu atau pada suatu titik waktu, sampai aset dan liabilitas kontrak.",
 "Pendapatan adalah area risiko signifikan di hampir setiap audit. Masalah yang sering muncul: termin tagihan dicatat sebagai pendapatan, persentase penyelesaian tidak didukung, klaim dan variasi pekerjaan diakui terlalu cepat, serta paket layanan tidak dipisah menjadi kewajiban pelaksanaan.",
 [("Gap assessment", "Membaca kontrak utama, kebijakan pendapatan, dan pola penagihan", "Daftar celah per jenis kontrak"),
  ("Lima langkah", "Kontrak, kewajiban pelaksanaan, harga transaksi, alokasi, pengakuan", "Memo PSAK 115 per jenis kontrak"),
  ("Metode progres", "Input (biaya) atau output (opname), estimasi biaya sampai selesai", "Lembar kerja progres proyek"),
  ("Saldo kontrak", "Aset kontrak, liabilitas kontrak, retensi, uang muka", "Rekonsiliasi saldo kontrak"),
  ("Pengungkapan", "Disagregasi pendapatan, sisa kewajiban pelaksanaan", "Draf CALK pendapatan")],
 ["Kontraktor dan perusahaan EPC dengan kontrak multi tahun.",
  "Developer properti dengan penjualan inden.",
  "Rumah sakit dan klinik dengan paket layanan dan klaim penjamin.",
  "Perusahaan software, langganan, dan jasa berulang."],
 [("Apakah termin tagihan boleh langsung dicatat sebagai pendapatan?", "Belum tentu. Pendapatan diakui saat kewajiban pelaksanaan dipenuhi. Tagihan yang mendahului progres menjadi liabilitas kontrak, sedangkan progres yang belum ditagih menjadi aset kontrak."),
  ("Sejak kapan PSAK 115 berlaku?", "Sejak 1 Januari 2020, saat itu bernomor PSAK 72. Penomoran PSAK 115 berlaku sejak 1 Januari 2024 sesuai SAK Online IAI.")],
 "Jasa Implementasi PSAK 115 Pendapatan Kontrak | FA Indonesia",
 "Konsultan PSAK 115: kewajiban pelaksanaan, metode progres, aset dan liabilitas kontrak untuk kontraktor, developer, rumah sakit, software. Ditangani tim CPA.",
 "Revenue recognition implementation (IFRS 15)",
 [("/artikel/laporan-keuangan-kontraktor-psak-115/", "Laporan Keuangan Kontraktor Sesuai PSAK 115"), ("/artikel/laporan-keuangan-rumah-sakit-swasta-sesuai-psak/", "Laporan Keuangan Rumah Sakit Swasta Sesuai PSAK")])

# ---------- PSAK 116 ----------
page("/jasa-implementasi-psak-116/", "PSAK 116", "Jasa Implementasi PSAK 116 Sewa: Aset Hak Guna dan Liabilitas Sewa",
 "Sewa, aset hak guna", "Ritel, rumah sakit, logistik, kantor cabang",
 "Pendampingan penerapan PSAK 116 Sewa dari sisi penyewa: inventarisasi kontrak, pengecualian jangka pendek dan bernilai rendah, suku bunga pinjaman inkremental, jadwal amortisasi, sampai modifikasi sewa.",
 "Banyak perusahaan masih mencatat sewa sebagai beban atau biaya dibayar di muka. Temuan audit yang umum: kontrak sewa tidak lengkap, suku bunga diskonto tidak didukung, opsi perpanjangan diabaikan, dan modifikasi sewa tidak dihitung ulang. Dampaknya ke EBITDA, rasio utang, dan covenant bank.",
 [("Inventarisasi", "Mengumpulkan semua kontrak sewa: gedung, tanah, kendaraan, alat berat, alat medis", "Register sewa"),
  ("Penilaian", "Identifikasi sewa, komponen nonsewa, opsi perpanjangan dan penghentian", "Memo penilaian per kontrak"),
  ("Perhitungan", "Suku bunga pinjaman inkremental, nilai kini, jadwal aset hak guna dan liabilitas", "Model Excel per kontrak"),
  ("Jurnal dan pajak", "Jurnal bulanan, beda tetap dan temporer, pajak tangguhan", "Template jurnal berulang"),
  ("Covenant", "Simulasi dampak ke EBITDA, DER, DSCR", "Catatan untuk bank")],
 ["Ritel, restoran, dan klinik dengan banyak gerai sewa.",
  "Rumah sakit dengan sewa gedung atau alat medis.",
  "Perusahaan logistik dan kontraktor dengan sewa kendaraan dan alat berat.",
  "Perusahaan yang sedang mengajukan kredit dan perlu membaca dampaknya ke rasio."],
 [("Apakah semua sewa harus dicatat sebagai aset hak guna?", "Tidak. Sewa jangka pendek (12 bulan atau kurang) dan sewa aset bernilai rendah boleh dikecualikan dan diakui sebagai beban."),
  ("Apakah PSAK 116 mengubah rasio keuangan untuk bank?", "Ya. Liabilitas sewa menambah utang, sementara beban sewa berganti menjadi penyusutan dan bunga sehingga EBITDA naik. Rasio covenant perlu dibaca ulang bersama bank.")],
 "Jasa Implementasi PSAK 116 Sewa | FA Indonesia",
 "Konsultan PSAK 116 Sewa: register sewa, suku bunga inkremental, aset hak guna, liabilitas sewa, modifikasi, dampak covenant bank. Ditangani tim CPA.",
 "Lease accounting implementation (IFRS 16)",
 [("/artikel/rasio-keuangan-yang-dilihat-bank/", "Rasio Keuangan yang Dilihat Bank"), ("/artikel/laporan-keuangan-rumah-sakit-swasta-sesuai-psak/", "Laporan Keuangan Rumah Sakit Swasta Sesuai PSAK")])

# ---------- PSAK 117 ----------
page("/jasa-implementasi-psak-117/", "PSAK 117", "Jasa Implementasi PSAK 117 Kontrak Asuransi",
 "Kontrak asuransi", "Asuransi, reasuransi, penjaminan",
 "Pendampingan penerapan PSAK 117 Kontrak Asuransi yang berlaku sejak 1 Januari 2025: agregasi portofolio dan kelompok kontrak, pemilihan model pengukuran, CSM, data transisi, sampai penyajian dan pengungkapan.",
 "PSAK 117 mengubah cara pendapatan asuransi dan laba diakui. Tantangannya ada di data: kelompok kontrak per tahun penerbitan, arus kas pemenuhan, penyesuaian risiko, dan CSM. Kami membantu sisi akuntansi dan pelaporan, sementara perhitungan aktuaria tetap dikerjakan aktuaris Anda.",
 [("Gap assessment", "Portofolio produk, sistem polis, data historis", "Peta celah data dan kebijakan"),
  ("Model pengukuran", "General Model, Premium Allocation Approach, Variable Fee Approach", "Memo pemilihan model"),
  ("Transisi", "Pendekatan retrospektif penuh, modifikasian, atau nilai wajar", "Paket angka transisi"),
  ("Pelaporan", "Format laporan posisi keuangan dan laba rugi baru, CALK", "Template laporan dan CALK"),
  ("Koordinasi", "Aktuaris, tim TI, dan auditor", "Jadwal dan daftar dokumen")],
 ["Perusahaan asuransi umum, jiwa, dan syariah.",
  "Perusahaan reasuransi dan penjaminan.",
  "Perusahaan nonasuransi yang menerbitkan kontrak berkarakter asuransi."],
 [("Sejak kapan PSAK 117 berlaku?", "Sejak 1 Januari 2025, menggantikan standar kontrak asuransi sebelumnya. Penomoran PSAK 117 mengikuti SAK Online IAI."),
  ("Apakah FA Indonesia menghitung cadangan aktuaria?", "Tidak. Perhitungan aktuaria dikerjakan aktuaris. Kami menangani kebijakan akuntansi, penyajian, pengungkapan, dan koordinasi dengan auditor.")],
 "Jasa Implementasi PSAK 117 Kontrak Asuransi | FA Indonesia",
 "Konsultan PSAK 117 Kontrak Asuransi: model pengukuran, CSM, transisi, laporan dan CALK, koordinasi aktuaris dan auditor. Ditangani tim CPA.",
 "Insurance contracts implementation (IFRS 17)",
 [("/artikel/daftar-psak-isak-2026-2027/", "Daftar PSAK dan ISAK yang Berlaku 2026 sampai 2027")])

# ---------- PSAK 212 ----------
page("/jasa-implementasi-psak-212/", "PSAK 212", "Jasa PSAK 212 Pajak Penghasilan: Pajak Tangguhan dan Rekonsiliasi Fiskal",
 "Pajak tangguhan", "Semua perusahaan yang diaudit",
 "Pendampingan penerapan PSAK 212 Pajak Penghasilan: rekonsiliasi fiskal, beda temporer dan beda tetap, aset dan liabilitas pajak tangguhan, uji pemulihan aset pajak tangguhan, sampai rekonsiliasi tarif efektif di CALK.",
 "Pajak tangguhan sering dihitung di akhir tahun dengan terburu-buru. Temuan yang umum: beda temporer tidak lengkap, aset pajak tangguhan atas rugi fiskal diakui tanpa proyeksi laba yang meyakinkan, dan angka di laporan keuangan tidak cocok dengan SPT Tahunan Badan di Coretax.",
 [("Rekonsiliasi fiskal", "Mencocokkan laba akuntansi dengan SPT Tahunan Badan", "Kertas kerja koreksi fiskal"),
  ("Beda temporer", "Aset tetap, CKPN, imbalan kerja, sewa, provisi", "Daftar beda temporer per pos"),
  ("Pajak tangguhan", "Pengakuan, pengukuran, uji pemulihan rugi fiskal", "Lembar kerja pajak tangguhan"),
  ("CALK", "Rekonsiliasi tarif efektif dan mutasi pajak tangguhan", "Draf catatan pajak"),
  ("Konsistensi", "Kecocokan dengan SPT, bukti potong, dan Coretax", "Daftar selisih dan tindak lanjut")],
 ["Perusahaan yang diaudit dan menerapkan SAK Indonesia.",
  "Perusahaan dengan rugi fiskal yang ingin mengakui aset pajak tangguhan.",
  "Perusahaan yang baru revaluasi aset tetap atau baru menerapkan PSAK 116 dan PSAK 219."],
 [("Apa beda pajak kini dan pajak tangguhan?", "Pajak kini adalah pajak yang terutang di SPT tahun berjalan. Pajak tangguhan timbul dari beda temporer antara nilai buku akuntansi dan dasar pengenaan pajak yang akan berbalik di masa depan."),
  ("PSAK 212 dulu bernomor berapa?", "Sebelum 1 Januari 2024, standar ini bernomor PSAK 46. Penomoran saat ini mengikuti SAK Online IAI.")],
 "Jasa PSAK 212 Pajak Tangguhan & Rekonsiliasi Fiskal | FA Indonesia",
 "Konsultan PSAK 212: rekonsiliasi fiskal, beda temporer, aset dan liabilitas pajak tangguhan, rekonsiliasi tarif efektif, konsistensi dengan SPT Coretax.",
 "Income tax accounting (IAS 12)",
 [("/artikel/revaluasi-aset-tetap-psak-216-dan-pajak/", "Revaluasi Aset Tetap PSAK 216 dan Pajaknya")])

# ---------- PSAK 219 ----------
page("/jasa-implementasi-psak-219/", "PSAK 219", "Jasa PSAK 219 Imbalan Kerja: Liabilitas Pesangon dan Koordinasi Aktuaris",
 "Imbalan kerja, pesangon", "Perusahaan dengan banyak karyawan tetap",
 "Pendampingan penerapan PSAK 219 Imbalan Kerja: data karyawan untuk aktuaris, imbalan pascakerja sesuai peraturan ketenagakerjaan, pencatatan biaya jasa dan pengukuran kembali di penghasilan komprehensif lain, sampai pengungkapan.",
 "Liabilitas imbalan kerja sering tidak dicatat sama sekali oleh perusahaan menengah, lalu muncul sebagai koreksi besar saat pertama kali diaudit atau saat due diligence bank dan investor. Data karyawan yang tidak rapi juga membuat laporan aktuaris tidak bisa dipakai.",
 [("Data", "Menyiapkan data karyawan: tanggal masuk, gaji, status, program pensiun", "Data siap kirim ke aktuaris"),
  ("Program", "Membaca PKB, peraturan perusahaan, dan program pensiun", "Ringkasan manfaat untuk aktuaris"),
  ("Pencatatan", "Biaya jasa kini, biaya bunga, pengukuran kembali di OCI", "Jurnal dan mutasi liabilitas"),
  ("Pajak", "Beda temporer dan pajak tangguhan atas imbalan kerja", "Lembar kerja pajak tangguhan"),
  ("CALK", "Asumsi aktuaria, sensitivitas, profil jatuh tempo", "Draf catatan imbalan kerja")],
 ["Perusahaan yang baru pertama kali diaudit.",
  "Rumah sakit, manufaktur, dan perusahaan jasa dengan banyak karyawan tetap.",
  "Perusahaan yang sedang due diligence untuk kredit, investor, atau IPO."],
 [("Apakah perusahaan wajib mencatat liabilitas imbalan kerja?", "Bila menerapkan SAK Indonesia dan memiliki kewajiban imbalan pascakerja menurut peraturan ketenagakerjaan atau perjanjian kerja, liabilitasnya diakui sesuai PSAK 219 berdasarkan perhitungan aktuaria."),
  ("Apakah FA Indonesia menggantikan aktuaris?", "Tidak. Perhitungan dilakukan aktuaris. Kami menyiapkan data, membaca hasilnya, mencatat, dan menyusun pengungkapan.")],
 "Jasa PSAK 219 Imbalan Kerja & Pesangon | FA Indonesia",
 "Konsultan PSAK 219 Imbalan Kerja: data karyawan untuk aktuaris, liabilitas pesangon, OCI, pajak tangguhan, dan CALK. Ditangani tim CPA.",
 "Employee benefits accounting (IAS 19)",
 [("/jasa-penyusunan-laporan-keuangan/", "Jasa Penyusunan Laporan Keuangan")])

# ---------- PSAK 110 ----------
page("/jasa-konsolidasi-laporan-keuangan-psak-110/", "PSAK 110", "Jasa Konsolidasi Laporan Keuangan Grup Sesuai PSAK 110",
 "Konsolidasi grup", "Grup usaha, holding, grup rumah sakit",
 "Pendampingan penyusunan laporan keuangan konsolidasian sesuai PSAK 110: penilaian pengendalian, eliminasi transaksi antarperusahaan, kepentingan nonpengendali, akuisisi entitas anak, sampai paket konsolidasi bulanan.",
 "Grup yang tumbuh lewat akuisisi biasanya punya bagan akun berbeda per entitas, saldo antarperusahaan yang tidak cocok, dan goodwill yang belum dialokasikan. Bank dan investor membaca angka konsolidasian, jadi selisih kecil antarperusahaan pun bisa menghambat proses.",
 [("Struktur grup", "Penilaian pengendalian, entitas anak, asosiasi, ventura bersama", "Peta grup dan kebijakan konsolidasi"),
  ("Penyelarasan", "Bagan akun dan kebijakan akuntansi seragam", "Mapping akun per entitas"),
  ("Antarperusahaan", "Rekonsiliasi dan eliminasi saldo serta transaksi", "Lembar eliminasi"),
  ("Akuisisi", "Alokasi harga beli dan goodwill sesuai PSAK 103", "Memo kombinasi bisnis"),
  ("Paket konsolidasi", "Template bulanan dan tahunan termasuk KNP", "Laporan konsolidasian siap audit")],
 ["Grup usaha dengan beberapa PT di bawah satu pemilik.",
  "Grup rumah sakit dan klinik yang tumbuh lewat akuisisi.",
  "Holding yang menyiapkan kredit sindikasi, investor, atau IPO."],
 [("Kapan perusahaan wajib menyusun laporan konsolidasian?", "Entitas induk yang mengendalikan satu atau lebih entitas anak menyajikan laporan keuangan konsolidasian, kecuali memenuhi pengecualian tertentu dalam PSAK 110."),
  ("PSAK 110 dulu bernomor berapa?", "Sebelum 1 Januari 2024 bernomor PSAK 65, dan kombinasi bisnis (kini PSAK 103) dulu PSAK 22.")],
 "Jasa Konsolidasi Laporan Keuangan PSAK 110 | FA Indonesia",
 "Konsultan konsolidasi PSAK 110: pengendalian, eliminasi antarperusahaan, kepentingan nonpengendali, akuisisi dan goodwill PSAK 103, paket konsolidasi bulanan.",
 "Consolidated financial statements (IFRS 10)",
 [("/konsultan-persiapan-ipo/", "Konsultan Persiapan IPO"), ("/konsultan-rumah-sakit/", "Konsultan Rumah Sakit")])

# ---------- SAK EP -> PSAK ----------
page("/jasa-transisi-sak-ep-ke-psak/", "SAK EP ke PSAK", "Jasa Transisi Laporan Keuangan dari SAK EP ke PSAK (SAK Indonesia)",
 "Naik kelas ke SAK Indonesia", "Perusahaan menuju IPO, investor, atau kredit besar",
 "Pendampingan perusahaan yang pindah dari SAK EP (pengganti SAK ETAP sejak 1 Januari 2025) ke SAK Indonesia: neraca pembukaan, penerapan PSAK 109, 115, 116, 212, dan 219 sekaligus, sampai laporan komparatif yang siap diaudit.",
 "Perusahaan yang akan IPO atau masuk ke investor besar perlu laporan sesuai SAK Indonesia, sementara selama ini memakai SAK ETAP atau SAK EP. Bedanya bukan sekadar format: pengakuan sewa, instrumen keuangan, pendapatan, imbalan kerja, dan pajak tangguhan bisa mengubah ekuitas awal secara material.",
 [("Penilaian", "Membandingkan kebijakan saat ini dengan PSAK yang relevan", "Daftar perbedaan dan estimasi dampak"),
  ("Neraca pembukaan", "Penyesuaian per tanggal transisi", "Neraca pembukaan dan jurnal penyesuaian"),
  ("Kebijakan", "Kebijakan akuntansi baru untuk tiap pos material", "Buku kebijakan akuntansi"),
  ("Komparatif", "Menyajikan ulang tahun pembanding", "Laporan komparatif dan rekonsiliasi ekuitas"),
  ("CALK", "Catatan lengkap gaya auditor, dua bahasa bila perlu", "Draf CALK siap audit")],
 ["Perusahaan yang menyiapkan IPO di BEI.",
  "Perusahaan yang akan menerima investor PE atau VC.",
  "Perusahaan yang diminta bank memakai SAK Indonesia untuk fasilitas besar."],
 [("Apa itu SAK EP?", "SAK Entitas Privat, berlaku 1 Januari 2025 dan menggantikan SAK ETAP untuk entitas tanpa akuntabilitas publik signifikan."),
  ("Apakah perusahaan tertutup wajib pindah ke PSAK?", "Tidak selalu. Kewajiban biasanya datang dari rencana IPO, regulator sektor, atau permintaan pemberi dana. Kami bantu menilai apakah transisi memang diperlukan.")],
 "Jasa Transisi SAK EP ke PSAK (SAK Indonesia) | FA Indonesia",
 "Pindah dari SAK EP atau SAK ETAP ke SAK Indonesia untuk IPO, investor, atau kredit besar: neraca pembukaan, kebijakan, komparatif, CALK siap audit.",
 "First-time adoption of full SAK Indonesia",
 [("/konsultan-persiapan-ipo/", "Konsultan Persiapan IPO"), ("/jasa-penyusunan-laporan-keuangan/", "Jasa Penyusunan Laporan Keuangan")])

# ---------- HUB ----------
rows = [(f'<a href="/jasa-implementasi-psak-118/">PSAK 118</a>', "Penyajian dan pengungkapan, berlaku 2027", "Semua perusahaan yang diaudit")]
rows += [(f'<a href="{p}">{E(s)}</a>', E(sh), E(si)) for p, s, sh, si in PAGES]
hub_body = ("<h2>Pilih Standar yang Anda Butuhkan</h2>" + tbl(["Standar", "Topik", "Paling Relevan untuk"], rows)
  + "<h2>Kenapa Implementasi PSAK Perlu Didampingi</h2><p>Standar baru jarang gagal karena teorinya. Yang membuat repot adalah data, keputusan kebijakan, dan dokumentasi yang bisa dipertahankan di depan auditor, bank, dan investor. "
    "Kami bekerja dari laporan keuangan Anda yang sekarang, bukan dari template umum, lalu menyerahkan model dan kebijakan yang bisa dipakai tim Anda sendiri.</p>"
  + KERJA + SIAPA
  + "<h2>Coba Gratis Dulu</h2><p>Gunakan <a href=\"/cek-psak-118/\">FA Venus Cek PSAK 118</a> untuk mengonversi laba rugi ke format PSAK 118, atau baca <a href=\"/artikel/daftar-psak-isak-2026-2027/\">daftar PSAK dan ISAK yang berlaku 2026 sampai 2027</a>.</p>")
HUB_FAQ = [
 ("PSAK apa saja yang wajib diterapkan perusahaan saya?", "Bergantung pada kerangka yang dipakai (SAK Indonesia, SAK EP, atau SAK EMKM) dan jenis transaksinya. Diskusi awal gratis membantu memetakan standar mana yang paling berdampak."),
 ("Kenapa nomor PSAK berubah?", "Sejak 1 Januari 2024 IAI memakai penomoran baru di SAK Online, misalnya PSAK 71 menjadi PSAK 109, PSAK 72 menjadi PSAK 115, PSAK 73 menjadi PSAK 116, PSAK 46 menjadi PSAK 212, dan PSAK 24 menjadi PSAK 219."),
 ("Apakah bisa dikerjakan jarak jauh?", "Bisa. Sebagian besar pekerjaan dilakukan lewat video call dan pertukaran data aman setelah NDA, untuk klien di seluruh Indonesia."),
 FAQ_BIAYA]
svc_page(HUB, "Layanan · Standar Akuntansi", "Jasa Implementasi PSAK: Pendampingan Standar Akuntansi Terbaru sampai Siap Audit",
 "Pendampingan penerapan PSAK sesuai penomoran SAK Online IAI: PSAK 118 (berlaku 2027), PSAK 109, 115, 116, 117, 212, 219, konsolidasi PSAK 110, dan transisi dari SAK EP ke SAK Indonesia.",
 hub_body, HUB_FAQ, "Jasa Implementasi PSAK & Konsultan Standar Akuntansi | FA Indonesia",
 "Konsultan implementasi PSAK: PSAK 118, 109 (ECL), 115, 116, 117, 212, 219, konsolidasi 110, transisi SAK EP ke PSAK. Tim CPA, seluruh Indonesia.",
 "Jasa Implementasi PSAK", "Accounting standards implementation advisory",
 "/jasa-implementasi-psak-118/", "Implementasi PSAK 118", "Halo FA Indonesia, kami ingin konsultasi implementasi PSAK di perusahaan kami.", "Implementasi PSAK")

URLS = [HUB] + [p for p, *_ in PAGES]

# ---------- CTA di artikel terkait ----------
def box(href, title, text):
    return (f'<!--fa-psak--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
            f'<p style="margin:0 0 6px;font-weight:600">{E(title)}</p><p style="margin:0 0 12px">{E(text)}</p>'
            f'<a class="btn solid" href="{href}">Lihat Layanan</a></div><!--/fa-psak-->')
INJ = {
 ("jasa-implementasi-psak-118",): box(HUB, "Standar Lain yang Juga Berdampak", "PSAK 109, 115, 116, 212, 219, konsolidasi, dan transisi SAK EP ke PSAK. Lihat semua layanan implementasi PSAK."),
 ("artikel", "daftar-psak-isak-2026-2027"): box(HUB, "Butuh Pendampingan Implementasi PSAK?", "Dari PSAK 118 yang berlaku 2027 sampai PSAK 109, 115, dan 116. Mulai dari diskusi awal gratis."),
 ("artikel", "laporan-keuangan-kontraktor-psak-115"): box("/jasa-implementasi-psak-115/", "Pendampingan PSAK 115 untuk Kontraktor", "Metode progres, aset dan liabilitas kontrak, sampai CALK pendapatan yang siap diaudit."),
 ("artikel", "laporan-keuangan-rumah-sakit-swasta-sesuai-psak"): box("/jasa-implementasi-psak-116/", "Sewa Gedung dan Alat Medis?", "Lihat pendampingan PSAK 116 Sewa dan dampaknya ke rasio kredit rumah sakit."),
 ("artikel", "revaluasi-aset-tetap-psak-216-dan-pajak"): box("/jasa-implementasi-psak-212/", "Pajak Tangguhan Setelah Revaluasi", "Kami bantu hitung beda temporer dan pajak tangguhan sesuai PSAK 212."),
 ("artikel", "amendemen-psak-109-107-berlaku-2026"): box("/jasa-implementasi-psak-109/", "Pendampingan PSAK 109 dan Model ECL", "Klasifikasi instrumen keuangan, CKPN, dan staging yang terdokumentasi."),
 ("artikel", "psak-119-entitas-anak-tanpa-akuntabilitas-publik"): box("/jasa-konsolidasi-laporan-keuangan-psak-110/", "Grup Usaha dengan Banyak Entitas Anak?", "Lihat pendampingan konsolidasi sesuai PSAK 110."),
}
for parts, b in INJ.items():
    p = P(*parts, "index.html")
    if not os.path.exists(p): print("skip", p); continue
    t = re.sub(r"<!--fa-psak-->.*?<!--/fa-psak-->", "", rd(p), flags=re.S)
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("</main>")
    wtxt(p, t[:k] + b + t[k:])

# ---------- /layanan/: tambah tombol hub di blok fa-lead ----------
lp = P("layanan", "index.html"); t = rd(lp)
btn = '<!--fa-psak--><a class="btn line" href="/jasa-implementasi-psak/">Semua Layanan PSAK</a><!--/fa-psak-->'
t = re.sub(r"<!--fa-psak-->.*?<!--/fa-psak-->", "", t, flags=re.S)
anchor = '<a class="btn line" href="/konsultan-kredit-distributor-importir/">'
if anchor in t: t = t.replace(anchor, btn + anchor, 1)
wtxt(lp, t)

# ---------- sitemap & llms ----------
sm = re.sub(r"<!--fa-psak-->.*?<!--/fa-psak-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-psak-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for u in URLS) + "<!--/fa-psak-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = re.sub(r"\n## Implementasi PSAK.*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + "\n\n## Implementasi PSAK\n- Hub semua layanan implementasi PSAK → " + D + HUB + "\n" + "".join(f"- {s}: {sh} → {D}{p}\n" for p, s, sh, si in PAGES)
wtxt(P("llms.txt"), ll)
print("ok", len(URLS), URLS)
