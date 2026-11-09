# -*- coding: utf-8 -*-
"""9 Nov 2026 (Bos): keyword FA juga harus ada di UpdateSAK, versi edukasi nasional (keputusan Bos: US tanpa halaman per kota).
Pilar: /laporan-keuangan-sabh/ (+ template Word/Excel/PDF dari faindonesia.co.id/template/), /buku-besar/, /menghadapi-auditor/,
/penerapan-psak/, /akuntansi-rumah-sakit/. Tujuan akhir: lead WA ke Ananta, CPA; link ke halaman kota FA dan CariAkuntan.
BEKERJA LANGSUNG DI out/updatesak (template = halaman live /update-sak-emkm/). Jalankan setelah us_lead_20261109.py. Idempoten.
Sisipan berpenanda <!--us-kw3-->: link ke pilar baru di 45 halaman PSAK, 49 halaman standar audit, dan beranda; sitemap (<!--uskw3-->), llms.txt."""
import os, re, sys, json, html, glob, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "updatesak")
sys.path.insert(0, os.path.join(HERE, "cariakuntan"))
from cities import CITIES as CC

E = html.escape
D = "https://updatesak.com"; FA = "https://faindonesia.co.id"; CA = "https://cariakuntan.com"
WA = "https://wa.me/6282245260121?text="
UPD = "9 November 2026"; TODAY = "2026-11-09"
def sl(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def rd(p): return open(p, encoding="utf-8").read()
def wt(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and rd(p) == t: return False
    open(p, "w", encoding="utf-8").write(t); return True
def P(path): return os.path.join(OUT, *path.strip("/").split("/"), "index.html")
def wa(t): return WA + urllib.parse.quote(t, safe="")
def hid(s): return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", s)).lower()).strip("-")[:60].rstrip("-")
def tbl(head, rows):
    return ('<div class="tx"><table><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
SA = lambda n, t: f'<a href="/standar-audit/{n}/">{t}</a>'
PS = lambda n: f'<a href="/psak/{n}/">PSAK {n}</a>'
KOTA = [dict(name=k, slug=sl(k), prov=p) for k, p, r, s, n in CC]
F_DOCX = FA + "/template/template-laporan-tahunan-pt-sabh-fa-indonesia.docx"
F_XLSX = FA + "/template/template-data-laporan-tahunan-sabh-fa-jupiter.xlsx"
F_PDF = FA + "/template/template-laporan-tahunan-pt-sabh-fa-indonesia.pdf"


def tanya(title, msg2):
    q1 = wa(f'Halo Pak Ananta, saya baca "{title}" di updatesak.com. Mau tanya untuk usaha kami: ')
    q2 = wa(msg2)
    return ('<!--us-tanya--><section class="us-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Ananta, CPA</b><p>Ada kasus di perusahaan Anda yang mirip? Tanyakan ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.</p>'
            f'<div class="q"><a class="w" href="{q1}" target="_blank" rel="noopener" data-us-q="kw3">Tanya soal topik ini untuk usaha saya</a><a class="" href="{q2}" target="_blank" rel="noopener" data-us-q="kw3">Minta dibantu mengerjakannya</a></div></section><!--/us-tanya-->')


PAGES = []
PAGES.append(dict(
    slug="laporan-keuangan-sabh", label="Laporan Keuangan untuk SABH",
    h1="Laporan Keuangan untuk SABH: Dasar Hukum, Isi, Siapa yang Menandatangani, dan Template",
    title="Laporan Keuangan SABH: Isi, Penandatangan, Template",
    desc="Edukasi laporan tahunan PT untuk SABH (Permenkum 49/2025, UU PT Pasal 66-68): isi minimal, wajib audit atau kompilasi, siapa yang menandatangani, dan template gratis.",
    lede="Sejak Permenkum 49/2025, persetujuan RUPS atas laporan tahunan PT persekutuan modal dituangkan dalam akta notaris dan disampaikan lewat SABH. Bagi akuntan, pertanyaannya bergeser: laporan keuangan seperti apa yang layak dilampirkan, dan siapa yang bertanggung jawab atasnya.",
    wa2="Halo Pak Ananta, kami perlu dibantu menyiapkan laporan keuangan dan laporan tahunan PT untuk SABH.",
    secs=[
        ("Dasar Hukum", "<p>Ada dua lapis aturan. <b>UU 40/2007 tentang Perseroan Terbatas</b> mengatur bahwa Direksi menyampaikan laporan tahunan kepada RUPS paling lambat enam bulan setelah tahun buku berakhir, setelah ditelaah Dewan Komisaris (Pasal 66), dan bahwa laporan keuangan PT tertentu wajib diaudit akuntan publik (Pasal 68). <b>Permenkum 49/2025</b> menambahkan mekanisme administrasi: persetujuan RUPS atas laporan tahunan dituangkan dalam akta notaris dan disampaikan melalui SABH paling lama 30 hari sejak akta, dengan lampiran laporan tahunannya (Pasal 16).</p>"),
        ("Isi Minimal Laporan Tahunan", tbl(["Bagian", "Isi"], [
            ("Laporan keuangan", "Laporan posisi keuangan akhir tahun dengan pembanding tahun lalu, laba rugi, arus kas, perubahan ekuitas, dan catatan atas laporan keuangan"),
            ("Laporan kegiatan", "Kegiatan usaha selama tahun buku"), ("TJSL", "Pelaksanaan tanggung jawab sosial dan lingkungan"),
            ("Permasalahan", "Masalah yang memengaruhi kegiatan usaha"), ("Pengawasan", "Laporan tugas pengawasan Dewan Komisaris"),
            ("Pengurus", "Nama anggota Direksi dan Dewan Komisaris serta gaji, honorarium, dan tunjangannya")])),
        ("Diaudit atau Cukup Disusun", "<p>Laporan keuangan wajib diaudit akuntan publik bila PT menghimpun atau mengelola dana masyarakat, menerbitkan surat pengakuan utang kepada masyarakat, merupakan perusahaan terbuka atau Persero, mempunyai aset atau peredaran usaha paling sedikit Rp50 miliar, atau diwajibkan peraturan lain (UU PT Pasal 68). Di luar kriteria itu, laporan keuangan tidak wajib diaudit, tetapi tetap harus lengkap dengan catatannya dan disusun sesuai standar yang berlaku (SAK EMKM, SAK EP, atau SAK Indonesia).</p>"),
        ("Siapa yang Menandatangani", tbl(["Dokumen", "Penandatangan", "Catatan"], [
            ("Laporan keuangan dan Surat Pernyataan Direksi", "Direksi", "Tanggung jawab atas laporan keuangan selalu pada manajemen"),
            ("Lembar penyusun (perikatan kompilasi)", "Akuntan Berpraktik atau KJA yang menyusun", f'Tanpa opini dan tanpa kesimpulan; standar kompilasi: {SA("sjt-4410", "SJT 4410")}'),
            ("Laporan Auditor Independen", "Akuntan Publik dari KAP", f'Bila wajib audit; opini mengikuti {SA("sa-700", "SA 700")}'),
            ("Laporan tahunan", "Direksi, ditelaah Dewan Komisaris", "Lalu disetujui RUPS dan dituangkan dalam akta")]) +
         '<p>Izin Akuntan Berpraktik, KJA, dan KAP bisa dicek di <a href="' + CA + '/cek-izin/">Cek Izin CariAkuntan</a>. Satu catatan independensi: untuk satu entitas, penyusun laporan keuangan dan auditornya pihak yang berbeda.</p>'),
        ("Template Gratis", '<p>Template Word berisi seluruh bagian di atas dengan angka ilustrasi yang saling cocok, Lembar Penyusun dengan kolom nama, nomor izin, dan tanda tangan Akuntan Berpraktik atau KJA (diisi penyusun sendiri), checklist dokumen untuk notaris, dan ilustrasi keputusan pemegang saham secara sirkuler. File Excel memakai format impor <a href="' + FA + '/audit-ready/">FA Jupiter</a>, sehingga laporan keuangan dan CALK bisa dihasilkan dari buku besar.</p>'
         f'<p><a class="btn" href="{F_DOCX}" download>Download Template Word</a> <a class="btn" href="{F_XLSX}" download>Excel Format FA Jupiter</a> <a class="btn" href="{F_PDF}" target="_blank" rel="noopener">Lihat Contoh PDF</a></p>'),
        ("Kesalahan yang Sering Ditemui Notaris", "<ul><li>Laporan keuangan tanpa catatan, hanya neraca dan laba rugi.</li><li>Tidak ada angka pembanding tahun lalu.</li><li>Saldo laba di neraca tidak cocok dengan laporan perubahan ekuitas.</li><li>PT yang memenuhi kriteria wajib audit melampirkan laporan yang belum diaudit.</li><li>Data remunerasi Direksi dan Dewan Komisaris belum disiapkan.</li></ul>"),
        ("Risiko Bila Tidak Lapor", "<p>Perseroan yang tidak memenuhi kewajiban dapat menerima teguran tertulis melalui SABH; bila 30 hari setelah teguran belum dipenuhi, akses SABH diblokir. Selama diblokir, perubahan pengurus, peralihan saham, dan perubahan data perseroan tertahan.</p>")],
    src=[("Hukumonline: Kewajiban Terbaru Perseroan", "https://www.hukumonline.com/"), ("UU 40/2007 tentang Perseroan Terbatas (JDIH BPK)", "https://peraturan.bpk.go.id/Details/39965/uu-no-40-tahun-2007")],
    reads=[("/standar-audit/sjt-4410/", "SJT 4410 Perikatan Kompilasi"), ("/standar-audit/sa-700/", "SA 700 Opini Auditor"), ("/update-sak-emkm/", "Update SAK EMKM"), ("/update-sak-ep/", "Update SAK EP")],
    kota="laporan-tahunan-pt"))

PAGES.append(dict(
    slug="buku-besar", label="Buku Besar",
    h1="Buku Besar (General Ledger): Pengertian, Contoh Posting, Neraca Saldo, dan Kesalahan Umum",
    title="Buku Besar (General Ledger): Contoh dan Neraca Saldo",
    desc="Buku besar akuntansi: pengertian, struktur bagan akun, contoh posting jurnal, neraca saldo, rekonsiliasi, dan kesalahan umum yang membuat laporan keuangan ditolak auditor.",
    lede="Semua laporan keuangan berasal dari buku besar. Kalau buku besarnya rapi, laporan keuangan, pajak, dan audit menjadi pekerjaan hilir. Kalau tidak, semua pekerjaan hilir ikut bermasalah.",
    wa2="Halo Pak Ananta, kami perlu dibantu merapikan buku besar (general ledger) perusahaan.",
    secs=[
        ("Pengertian Buku Besar", "<p>Buku besar adalah kumpulan akun yang mencatat semua transaksi setelah dijurnal, sehingga saldo setiap akun bisa diketahui kapan saja. Jurnal mencatat transaksi secara kronologis; buku besar mengelompokkannya per akun. Dari saldo akhir buku besar disusun neraca saldo, lalu laporan keuangan.</p>"),
        ("Struktur Bagan Akun", tbl(["Kode", "Kelompok", "Contoh Akun"], [
            ("1xxx", "Aset", "Kas, bank, piutang usaha, persediaan, aset tetap, akumulasi penyusutan"),
            ("2xxx", "Liabilitas", "Utang usaha, utang pajak, beban akrual, utang bank"),
            ("3xxx", "Ekuitas", "Modal saham, saldo laba"), ("4xxx", "Pendapatan", "Penjualan, pendapatan jasa"),
            ("5xxx", "Beban pokok", "Harga pokok penjualan"), ("6xxx-7xxx", "Beban usaha dan lain-lain", "Gaji, sewa, penyusutan, bunga bank")]) +
         "<p>Prinsip praktisnya: satu akun hanya untuk satu jenis transaksi, setiap akun dipetakan ke satu pos laporan keuangan, dan kode tidak diubah di tengah tahun.</p>"),
        ("Contoh Posting ke Buku Besar", "<p>Transaksi: 5 Januari, penjualan kredit Rp125.000.000; 20 Januari, pelunasan Rp98.000.000 ke bank.</p>" + tbl(["Tanggal", "Akun", "Keterangan", "Debit", "Kredit", "Saldo"], [
            ("5 Jan", "Piutang usaha", "Penjualan kredit", "125.000.000", "", "125.000.000 D"),
            ("20 Jan", "Piutang usaha", "Pelunasan", "", "98.000.000", "27.000.000 D"),
            ("5 Jan", "Penjualan", "Penjualan kredit", "", "125.000.000", "125.000.000 K"),
            ("20 Jan", "Bank", "Pelunasan piutang", "98.000.000", "", "98.000.000 D")])),
        ("Neraca Saldo dan Rekonsiliasi", "<p>Neraca saldo (trial balance) adalah daftar saldo akhir semua akun; jumlah debit harus sama dengan jumlah kredit. Seimbang belum berarti benar: neraca saldo bisa seimbang walaupun transaksi diposting ke akun yang salah. Karena itu setiap bulan saldo bank direkonsiliasi dengan rekening koran, dan saldo piutang, utang, persediaan, serta aset tetap dicocokkan dengan buku pembantunya.</p>"),
        ("Kesalahan Umum", "<ul><li>Transaksi pribadi pemilik tercampur dengan transaksi usaha.</li><li>Akun baru dibuat setiap ada transaksi baru, sehingga satu pos tersebar.</li><li>Saldo awal tahun tidak sama dengan laporan tahun lalu.</li><li>Penyusutan, akrual, dan cadangan piutang tidak pernah dijurnal.</li><li>Rekonsiliasi bank hanya dilakukan di akhir tahun.</li></ul>"),
        ("Dari Buku Besar ke Laporan Keuangan", '<p>Format buku besar dua sheet (COA: kode akun, nama akun, pos laporan keuangan, saldo pembanding; GL: nomor jurnal, tanggal, akun, keterangan, debit, kredit) bisa langsung dibaca <a href="' + FA + '/audit-ready/">FA Jupiter</a> untuk menghasilkan laporan keuangan lengkap dengan CALK. Contoh formatnya ada di <a href="' + F_XLSX + '" download>file Excel ini</a>.</p>')],
    src=[("SAK Online IAI", "https://web.iaiglobal.or.id/SAK-Online")],
    reads=[("/update-sak-emkm/", "Update SAK EMKM"), ("/update-sak-ep/", "Update SAK EP"), ("/menghadapi-auditor/", "Menghadapi Auditor"), ("/laporan-keuangan-sabh/", "Laporan Keuangan untuk SABH")],
    kota="jasa-buku-besar"))

PAGES.append(dict(
    slug="menghadapi-auditor", label="Menghadapi Auditor",
    h1="Menghadapi Auditor KAP: Apa yang Diminta, Dasar Standar Auditnya, dan Cara Menjawab",
    title="Menghadapi Auditor KAP: PBC, Standar Audit, Cara Menjawab",
    desc="Panduan perusahaan yang diaudit KAP: daftar PBC, kenapa auditor meminta konfirmasi dan stock opname, koreksi audit, representasi manajemen, dan opini, lengkap dengan rujukan SA IAPI.",
    lede="Hampir setiap permintaan auditor punya dasar di Standar Audit IAPI. Memahami dasarnya membuat perusahaan bisa menyiapkan bukti yang tepat sejak awal, sehingga audit tidak molor dan koreksi tidak datang di menit terakhir.",
    wa2="Halo Pak Ananta, perusahaan kami sedang/akan diaudit KAP dan perlu pendampingan menjawab permintaan auditor.",
    secs=[
        ("Permintaan Auditor dan Dasar Standarnya", tbl(["Permintaan Auditor", "Kenapa Diminta", "Standar"], [
            ("Pemahaman bisnis dan pengendalian internal", "Menilai risiko kesalahan penyajian material", SA("sa-315", "SA 315")),
            ("Materialitas dan rencana kerja", "Menentukan seberapa dalam pengujian", SA("sa-300", "SA 300") + ", " + SA("sa-320", "SA 320")),
            ("Bukti pendukung per akun (PBC)", "Bukti audit yang cukup dan tepat", SA("sa-500", "SA 500")),
            ("Konfirmasi bank, piutang, utang", "Bukti dari pihak ketiga lebih andal", SA("sa-505", "SA 505")),
            ("Kehadiran saat stock opname", "Memastikan keberadaan dan kondisi persediaan", SA("sa-501", "SA 501")),
            ("Saldo awal (audit pertama)", "Saldo awal tidak boleh mengandung salah saji material", SA("sa-510", "SA 510")),
            ("Daftar koreksi yang belum dibukukan", "Mengevaluasi kesalahan penyajian", SA("sa-450", "SA 450")),
            ("Surat representasi manajemen", "Pernyataan tertulis tanggung jawab manajemen", SA("sa-580", "SA 580")),
            ("Management letter", "Komunikasi defisiensi pengendalian internal", SA("sa-265", "SA 265"))])),
        ("Daftar PBC yang Perlu Disiapkan", "<ul><li>Neraca saldo final dan buku besar setahun.</li><li>Rekening koran dan rekonsiliasi bank akhir tahun.</li><li>Daftar umur piutang dan utang per pihak.</li><li>Hasil stock opname dan perhitungan harga pokok.</li><li>Daftar aset tetap dan penyusutan dengan bukti perolehan.</li><li>Perjanjian kredit, sewa, dan kontrak penting.</li><li>SPT Masa dan Tahunan serta rekonsiliasi fiskal.</li><li>Akta, notulen RUPS, dan daftar pemegang saham.</li></ul>"),
        ("Cara Menjawab Pertanyaan dan Koreksi", "<p>Jawab tertulis, satu pertanyaan satu jawaban, dengan bukti dan rujukan standar akuntansi yang dipakai. Pastikan angka di skedul sama dengan neraca saldo final. Untuk usulan koreksi, minta penjelasan dasarnya, hitung dampaknya ke laba, pajak, dan rasio yang disyaratkan bank, lalu putuskan: dibukukan, atau dijelaskan kenapa tidak. Koreksi yang tidak dibukukan tetap dicatat auditor dan dinilai materialitasnya.</p>"),
        ("Opini Auditor", "<p>Hasil akhir audit adalah opini: wajar tanpa modifikasian, wajar dengan pengecualian, tidak wajar, atau tidak menyatakan pendapat (" + SA("sa-700", "SA 700") + ", " + SA("sa-705", "SA 705") + "). Opini adalah keputusan independen auditor. Yang bisa dikendalikan perusahaan adalah kelengkapan bukti dan ketepatan jawabannya.</p>"),
        ("Kapan Perlu Pendamping", '<p>Bila tim keuangan kecil, audit pertama kali, laporan audit sebelumnya terlambat, atau ada koreksi besar yang memengaruhi kredit bank, pendamping dari sisi perusahaan membantu menyiapkan skedul dan menjawab auditor dengan bahasa standar audit. Pendamping tidak memengaruhi opini dan untuk satu entitas tidak boleh sekaligus menjadi auditornya.</p>')],
    src=[("IAPI: Standar Profesional Akuntan Publik", "https://iapi.or.id/")],
    reads=[("/standar-audit/", "Standar Audit IAPI"), ("/standar-audit/sa-500/", "SA 500 Bukti Audit"), ("/standar-audit/sa-580/", "SA 580 Representasi Tertulis"), ("/buku-besar/", "Buku Besar")],
    kota="pendampingan-audit"))

PAGES.append(dict(
    slug="penerapan-psak", label="Penerapan PSAK",
    h1="Penerapan PSAK di Perusahaan: Menentukan Standar, Analisis Dampak, dan Langkah per PSAK",
    title="Penerapan PSAK di Perusahaan: Langkah dan Contoh",
    desc="Panduan penerapan PSAK di perusahaan: SAK EMKM, SAK EP, atau SAK Indonesia; lima langkah penerapan; PSAK 109, 115, 116, 118, 212, 219 dengan langkah rinci per standar.",
    lede="Menerapkan PSAK bukan sekadar membaca standar. Yang dikerjakan adalah mengubah kebijakan akuntansi, perhitungan, sistem, dan penyajian, lalu memastikan semuanya bisa dipertahankan di depan auditor.",
    wa2="Halo Pak Ananta, kami perlu dibantu menerapkan PSAK di laporan keuangan perusahaan. PSAK: ...",
    secs=[
        ("Langkah Pertama: Standar Mana yang Berlaku", tbl(["Entitas", "Kerangka", "Catatan"], [
            ("Usaha mikro, kecil, menengah", "SAK EMKM", '<a href="/update-sak-emkm/">Update SAK EMKM</a>'),
            ("Entitas privat tanpa akuntabilitas publik signifikan", "SAK EP", '<a href="/update-sak-ep/">Update SAK EP</a>, berlaku sejak 1 Januari 2025'),
            ("Entitas dengan akuntabilitas publik", "SAK Indonesia (PSAK)", '<a href="/update-psak-terbaru/">Update PSAK Terbaru</a>')])),
        ("Lima Langkah Penerapan", tbl(["Langkah", "Isi", "Hasil"], [
            ("1. Analisis dampak", "Transaksi terdampak, estimasi perubahan angka, dampak ke covenant bank dan pajak", "Memo dampak"),
            ("2. Kebijakan akuntansi", "Pilihan kebijakan dan pertimbangan signifikan", "Kebijakan tertulis"),
            ("3. Model perhitungan", "Template perhitungan yang bisa diulang tiap periode", "Excel dan jurnal"),
            ("4. Transisi", "Penerapan retrospektif atau prospektif sesuai ketentuan transisi", "Jurnal saldo awal"),
            ("5. Penyajian dan pengungkapan", "Format laporan dan CALK baru, angka pembanding", "Draf laporan keuangan")])),
        ("Langkah per PSAK", tbl(["Standar", "Fokus Penerapan"], [
            (PS(109), "Klasifikasi aset keuangan dan cadangan kerugian kredit ekspektasian piutang"),
            (PS(115), "Lima langkah pengakuan pendapatan, kontrak jangka panjang, termin, retensi"),
            (PS(116), "Aset hak guna dan liabilitas sewa, pengecualian sewa jangka pendek dan bernilai rendah"),
            (PS(118), "Kategori operasi, investasi, pendanaan; subtotal baku; ukuran kinerja manajemen; berlaku tahun buku 2027"),
            (PS(212), "Pajak tangguhan dan rekonsiliasi beban pajak"),
            (PS(219), "Liabilitas imbalan kerja dan perhitungan aktuaria"),
            (PS(110), "Konsolidasi dan pengendalian atas entitas anak")]) +
         "<p>Setiap halaman PSAK di atas memuat bagian Langkah Penerapan di Perusahaan.</p>"),
        ("PSAK 118 Mulai 2027", '<p>PSAK 118 berlaku untuk periode tahun buku yang dimulai 1 Januari 2027 dan menggantikan PSAK 201 untuk penyajian. Karena angka pembanding ikut disajikan ulang, data tahun 2026 sudah perlu dipetakan ke kategori baru. Simulasinya bisa dicoba gratis di <a href="' + FA + '/cek-psak-118/">Cek PSAK 118</a>.</p>')],
    src=[("SAK Online IAI", "https://web.iaiglobal.or.id/SAK-Online")],
    reads=[("/update-psak-2026/", "Update PSAK 2026"), ("/update-sak-2027/", "Update SAK 2027"), ("/penomoran-psak-baru/", "Penomoran PSAK Baru"), ("/akuntansi-rumah-sakit/", "Akuntansi Rumah Sakit")],
    kota="konsultan-psak"))

PAGES.append(dict(
    slug="akuntansi-rumah-sakit", label="Akuntansi Rumah Sakit",
    h1="Akuntansi Rumah Sakit: Standar yang Berlaku, Pendapatan BPJS, Piutang Klaim, dan Persediaan Obat",
    title="Akuntansi Rumah Sakit: SAK, Pendapatan BPJS, Piutang",
    desc="Akuntansi rumah sakit: SAK EP, ISAK 335, atau SAP untuk RSUD BLUD; pendapatan BPJS INA-CBG (PSAK 115), piutang klaim dan CKPN, sewa alat medis (PSAK 116), persediaan obat.",
    lede="Rumah sakit punya transaksi yang tidak ditemui di usaha biasa: tarif paket INA-CBG, klaim pending dan dispute, obat dan BMHP dalam jumlah besar, serta kerja sama alat medis. Semuanya berdampak langsung ke laba dan kas.",
    wa2="Halo Pak Ananta, kami dari rumah sakit/klinik dan perlu dibantu soal akuntansi dan laporan keuangan rumah sakit.",
    secs=[
        ("Standar yang Berlaku", tbl(["Bentuk Rumah Sakit", "Kerangka Pelaporan"], [
            ("RS swasta berbentuk PT", "Umumnya SAK EP; SAK Indonesia bila bagian dari grup terbuka atau diminta investor"),
            ("RS milik yayasan atau perkumpulan", "SAK EP dengan ISAK 335 untuk entitas berorientasi nonlaba"),
            ("RSUD dan RS pemerintah berstatus BLU/BLUD", "Standar Akuntansi Pemerintahan, dengan laporan keuangan BLUD")])),
        ("Pendapatan BPJS dan Klaim Pending", "<p>Pendapatan jasa pasien JKN diakui saat layanan diberikan, sebesar imbalan yang diperkirakan diterima berdasarkan tarif INA-CBG. Karena sebagian klaim pending atau berpotensi dispute, jumlah yang diharapkan diterima adalah imbalan variabel: diakui sebatas kemungkinan besar tidak akan terjadi pembalikan signifikan (" + PS(115) + "). Selisih antara tagihan dan klaim yang disetujui dibukukan sebagai penyesuaian pendapatan, bukan beban.</p>"),
        ("Piutang Klaim dan Cadangan Kerugian", "<p>Piutang BPJS, asuransi, dan perusahaan penjamin dipisah per penjamin dan per umur. Cadangan kerugian kredit ekspektasian dihitung dari pengalaman tagihan yang tidak terbayar dan informasi ke depan (" + PS(109) + " untuk SAK Indonesia; SAK EP punya pengaturan penurunan nilai sendiri). Pemisahan ini juga yang dibaca bank saat menilai kas rumah sakit.</p>"),
        ("Obat, BMHP, dan Alat Medis", tbl(["Pos", "Perlakuan"], [
            ("Persediaan obat dan BMHP", "Biaya atau nilai realisasi neto, mana yang lebih rendah; obat kedaluwarsa dihapus; selisih stok opname dibukukan per periode"),
            ("Alat medis dibeli", "Aset tetap, disusutkan sesuai umur manfaat; komponen besar dapat dipisah"),
            ("Alat medis lewat kerja sama operasi (KSO) atau sewa", "Dinilai apakah mengandung sewa (" + PS(116) + "); bagi hasil per tindakan dicatat sesuai substansinya"),
            ("Jasa medis dokter", "Dokter karyawan: beban gaji dan imbalan kerja; dokter mitra: beban jasa medis sesuai perjanjian")])),
        ("Unit Cost dan Laporan Manajemen", '<p>Laporan keuangan menjawab apakah rumah sakit untung; unit cost menjawab layanan mana yang untung. Untuk keputusan tarif dan negosiasi dengan penjamin, biaya per layanan dihitung dari data SIMRS dengan metode activity based costing. Alat hitungnya bisa dicoba gratis di <a href="' + FA + '/kalkulator-unit-cost-rumah-sakit/">Kalkulator Unit Cost Rumah Sakit</a> dan <a href="' + FA + '/fa-venus-rumah-sakit/">FA Venus Rumah Sakit</a>.</p>')],
    src=[("SAK Online IAI", "https://web.iaiglobal.or.id/SAK-Online")],
    reads=[("/psak/115/", "PSAK 115 Pendapatan"), ("/psak/109/", "PSAK 109 Instrumen Keuangan"), ("/psak/116/", "PSAK 116 Sewa"), ("/penerapan-psak/", "Penerapan PSAK")],
    kota="konsultan-rumah-sakit"))

TPL = rd(P("/update-sak-emkm/"))
HEAD = TPL[:TPL.index("<main")]
REST = TPL[TPL.index("</main>") + 7:]


def build(pg):
    url = D + f"/{pg['slug']}/"
    nav, body = [], []
    for i, (h, b) in enumerate(pg["secs"]):
        a = hid(h); nav.append(f'<li><a href="#{a}">{E(h)}</a></li>'); body.append(f'<h2 id="{a}">{E(h)}</h2>{b}')
        if i == 0: body.append(tanya(pg["h1"], pg["wa2"]))
    rows = {}
    for k in KOTA: rows.setdefault(k["prov"], []).append(k)
    kk = "".join(f"<p><b>{E(pv)}:</b> " + " · ".join(f'<a href="{CA}/kota/{x["slug"]}/{pg["kota"]}/">{E(x["name"])}</a>' for x in rows[pv]) + "</p>" for pv in sorted(rows))
    a = "bantuan-di-kota-anda"; nav.append(f'<li><a href="#{a}">Bantuan di Kota Anda</a></li>')
    body.append(f'<h2 id="{a}">Bantuan di Kota Anda</h2><p>Pertanyaan dari kota mana pun dijawab Ananta, CPA lewat WhatsApp. Halaman per kota:</p><details><summary>{len(KOTA)} kota</summary>{kk}</details>')
    reads = '<h2>Bacaan Terkait</h2><div class="reads">' + "".join(f'<a href="{u}"><b>{E(t)}</b></a>' for u, t in pg["reads"]) + "</div>"
    src = "<h2>Sumber</h2><ul>" + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{E(t)}</a></li>' for t, u in pg["src"]) + "</ul>"
    sh = urllib.parse.quote(url, safe="")
    main = ('<main>\n<article class="art"><div class="wrap">\n'
            f'<nav class="crumb"><a href="/">Beranda</a> / {E(pg["label"])}</nav>\n<p class="label">Panduan · Diperbarui {UPD}</p>\n'
            f'<h1>{E(pg["h1"])}</h1>\n<p class="lede">{E(pg["lede"])}</p>\n<p class="upd">Tim UpdateSAK · Diperbarui {UPD} · Ditinjau Ananta W. Sasongko, CPA</p>\n'
            f'<div class="share"><span>Bagikan</span>\n<a href="https://www.linkedin.com/sharing/share-offsite/?url={sh}" rel="noopener" target="_blank">LinkedIn</a>\n'
            f'<a href="https://wa.me/?text={urllib.parse.quote(pg["h1"] + " " + url, safe="")}" rel="noopener" target="_blank">WhatsApp</a>\n<button data-copy="{url}" type="button">Salin Link</button></div>\n'
            f'<div class="prose"><nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>{"".join(nav)}</ol></nav>' + "".join(body) + "</div>\n"
            + reads + "\n" + src + "\n"
            f'<aside class="cta-box dark"><div><b>Perlu Dibantu Mengerjakannya?</b><span>Tanya dulu ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.</span></div><a class="btn arrow" href="{wa(pg["wa2"])}" rel="noopener" target="_blank">Tanya Ananta, CPA</a></aside>\n'
            "</div></article>\n</main>")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": pg["h1"], "description": pg["desc"], "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "id",
         "author": {"@type": "Organization", "name": "Tim UpdateSAK"}, "reviewedBy": {"@type": "Person", "name": "Ananta W. Sasongko, CPA"},
         "publisher": {"@type": "Organization", "name": "UpdateSAK", "url": D + "/"}, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": D + "/"}, {"@type": "ListItem", "position": 2, "name": pg["label"], "item": url}]}]}
    head = HEAD
    T, Dd = E(pg["title"]), E(pg["desc"])
    head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{T}</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description")/>', lambda m: f'<meta content="{Dd}" {m.group(1)}/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:title"/>', lambda m: f'<meta content="{T}" property="og:title"/>', head)
    head = re.sub(r'<link href="[^"]*" rel="canonical"/>', lambda m: f'<link href="{url}" rel="canonical"/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:url"/>', lambda m: f'<meta content="{url}" property="og:url"/>', head)
    head = re.sub(r'<meta content="[^"]*" (property="og:image"|name="twitter:image")/>', lambda m: f'<meta content="{D}/img/share/lp-update-psak-2026-og.jpg" {m.group(1)}/>' if os.path.exists(os.path.join(OUT, "img/share/lp-update-psak-2026-og.jpg")) else m.group(0), head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", head, count=1, flags=re.S)
    wt(P(f"/{pg['slug']}/"), head + main + REST)
    return f"/{pg['slug']}/"


NEW = [build(pg) for pg in PAGES]

# ---------------- sisipan link ----------------
LINKS = ('<!--us-kw3--><p class="kw3">Panduan praktis: <a href="/penerapan-psak/">Penerapan PSAK</a> · <a href="/buku-besar/">Buku Besar</a> · '
         '<a href="/menghadapi-auditor/">Menghadapi Auditor</a> · <a href="/laporan-keuangan-sabh/">Laporan Keuangan untuk SABH</a> · '
         '<a href="/akuntansi-rumah-sakit/">Akuntansi Rumah Sakit</a></p><!--/us-kw3-->')
nx = 0
for fp in glob.glob(os.path.join(OUT, "psak", "*", "index.html")) + glob.glob(os.path.join(OUT, "standar-audit", "*", "index.html")) + [P("/standar-audit/")]:
    t = rd(fp); t2 = re.sub(r"<!--us-kw3-->.*?<!--/us-kw3-->", "", t, flags=re.S)
    if '<aside class="cta-box' in t2: t2 = t2.replace('<aside class="cta-box', LINKS + '<aside class="cta-box', 1)
    elif "</article>" in t2: t2 = t2.replace("</div></article>", LINKS + "</div></article>", 1)
    nx += wt(fp, t2)
sm = os.path.join(OUT, "sitemap.xml"); t = rd(sm)
t = re.sub(r"<!--uskw3-->.*?<!--/uskw3-->", "", t, flags=re.S)
t = t.replace("</urlset>", "<!--uskw3-->" + "".join(f"<url><loc>{D}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in NEW) + "<!--/uskw3-->\n</urlset>", 1); wt(sm, t)
ll = os.path.join(OUT, "llms.txt"); t = rd(ll)
t = re.sub(r"\n## Panduan Praktis 9 Nov 2026\n.*?(?=\n## |\Z)", "", t, flags=re.S)
t = t.rstrip() + "\n\n## Panduan Praktis 9 Nov 2026\n" + "".join(f"- [{pg['h1']}]({D}/{pg['slug']}/)\n" for pg in PAGES)
wt(ll, t)
print("halaman", len(NEW), "sisipan", nx)
