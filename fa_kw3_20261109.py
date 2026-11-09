# -*- coding: utf-8 -*-
"""9 Nov 2026 (Bos): keyword "Jasa Buku Besar", "Jasa Pendampingan Auditor / Menjawab Audit KAP [daerah]",
"Konsultan Penerapan PSAK [kota]", dan edukasi SABH + template untuk Notaris (nyambung FA Jupiter).
Keputusan Bos 9 Nov: FA dan CA per 113 kota + pilar, US pilar edukasi nasional; kolom TTD Akuntan Berpraktik di template KOSONG.

BEKERJA LANGSUNG DI out/faindonesia (template = halaman live /jasa-penyusunan-laporan-keuangan/<kota>/, lihat PERINGATAN BUILD
di README-DEPLOY). Jalankan setelah fa_lead_lkaudit_20261109.py. Idempoten.

Halaman baru (pilar + 113 kota):
  /jasa-buku-besar/<kota>/              (keluarga LK: kotak kontak KJA Farhani + KAP DHN)
  /jasa-pendampingan-audit/<kota>/      (pendampingan auditee menghadapi auditor KAP; tim langsung Ananta)
  /konsultan-penerapan-psak/<kota>/     (tim langsung Ananta)
  /laporan-tahunan-pt/<kota>/           (SABH per kota, kotak kontak KJA Farhani + KAP DHN; pilar lama /laporan-tahunan-pt/ dapat kotak template)
  /laporan-keuangan-sabh/               (pilar edukasi SABH + download template Word/Excel/PDF di /template/)
Sisipan berpenanda: <!--fa-kw3x--> setelah <!--/fanas-x--> di halaman kota yang sama, <!--fa-kw3t--> di /laporan-tahunan-pt/,
sitemap (<!--kw3-->), llms.txt (## Kata Kunci Baru 9 Nov)."""
import os, re, sys, json, html, glob, urllib.parse, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faindonesia")
sys.path.insert(0, os.path.join(HERE, "cariakuntan"))
from cities import CITIES as CC

E = html.escape
D = "https://faindonesia.co.id"
WA = "https://wa.me/6282245260121?text="
TODAY = "2026-11-09"
def sl(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def rd(p): return open(p, encoding="utf-8").read()
def wt(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and rd(p) == t: return False
    open(p, "w", encoding="utf-8").write(t); return True
def P(path): return os.path.join(OUT, *path.strip("/").split("/"), "index.html")
def wa(t): return WA + urllib.parse.quote(t, safe="")
def hid(s): return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", s)).lower()).strip("-")[:60].rstrip("-")
def cut(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    while len(s) > n and ". " in s: s = s.rsplit(". ", 1)[0] + "."
    if len(s) <= n: return s
    return s[:n].rsplit(" ", 1)[0].rstrip(",;:") + "."
def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
def between(t, a, b):
    i = t.index(a); return t[i:t.index(b, i) + len(b)]

KOTA = []
for kota, prov, region, secs, note in CC:
    KOTA.append(dict(name=kota, slug=sl(kota), prov=prov, note=note))
BYPROV = {}
for k in KOTA: BYPROV.setdefault(k["prov"], []).append(k)

TPLM = rd(P("/jasa-penyusunan-laporan-keuangan/malang/"))
TIM = between(TPLM, "<!--fa-tim-atas-->", "<!--/fa-tim-atas-->")
TOOLS = between(TPLM, "<!--fa-tools-->", "<!--/fa-tools-->")
TOOLS = re.sub(r'<h2 id="[^"]*">', "<h2>", TOOLS)
TIM = re.sub(r'<h2 id="[^"]*">', "<h2>", TIM)

TPL_DL = "/template/"
F_DOCX = TPL_DL + "template-laporan-tahunan-pt-sabh-fa-indonesia.docx"
F_XLSX = TPL_DL + "template-data-laporan-tahunan-sabh-fa-jupiter.xlsx"
F_PDF = TPL_DL + "template-laporan-tahunan-pt-sabh-fa-indonesia.pdf"


def lk2(base, k):
    """kotak kontak KJA Farhani + KAP DHN dari halaman kota (k=None: versi nasional dari Malang)."""
    b = between(base, "<!--fa-lk2-->", "<!--/fa-lk2-->")
    if k is None:
        b = b.replace(" di Malang</b>", " untuk Seluruh Indonesia</b>").replace("dari%20Malang%20", "")
    return b


def area(base, what):
    if "<!--fanas-area-->" not in base: return ""
    b = between(base, "<!--fanas-area-->", "<!--/fanas-area-->")
    b = re.sub(r"<p>Kami melayani .*?</p>", lambda m: f"<p>Kami melayani {what}, termasuk kecamatan dan desa/kelurahan berikut. Pertemuan bisa di lokasi Anda atau daring.</p>", b, count=1, flags=re.S)
    return re.sub(r'<h2 id="[^"]*">', "<h2>", b)


def fanx(base):
    return between(base, "<!--fanas-x-->", "<!--/fanas-x-->") if "<!--fanas-x-->" in base else ""


def sabh_box(k=None):
    di = f" untuk PT di {E(k['name'])}" if k else ""
    return ('<!--fa-kw3t--><div class="kw3t" style="border:1px solid rgba(233,185,73,.5);border-radius:12px;padding:16px 18px;margin:22px 0 8px;background:rgba(233,185,73,.07);max-width:760px">'
            f'<b style="font-size:17px">Template Laporan Tahunan PT untuk SABH{di}</b>'
            '<p style="margin:.3em 0 .6em;opacity:.85">Contoh format lengkap untuk diserahkan ke Notaris: laporan tahunan (Pasal 16 Permenkum 49/2025), laporan keuangan dengan CALK, '
            'Surat Pernyataan Direksi, Lembar Penyusun yang ditandatangani Akuntan Berpraktik, checklist dokumen, dan ilustrasi keputusan sirkuler. Angkanya bisa dihasilkan dari FA Jupiter.</p>'
            f'<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn solid" href="{F_DOCX}" download>Download Template Word</a>'
            f'<a class="btn line" href="{F_XLSX}" download>Excel Format FA Jupiter</a><a class="btn line" href="{F_PDF}" target="_blank" rel="noopener">Lihat Contoh PDF</a>'
            '<a class="btn line" href="/laporan-keuangan-sabh/">Panduan SABH</a></div></div><!--/fa-kw3t-->')


def kw3x(k):
    s = k["slug"]
    return (f'<!--fa-kw3x--><p class="t"><b>Akuntansi dan audit lainnya di {E(k["name"])}:</b> <a href="/jasa-buku-besar/{s}/">Jasa Buku Besar</a> · '
            f'<a href="/jasa-pendampingan-audit/{s}/">Pendampingan Audit</a> · <a href="/konsultan-penerapan-psak/{s}/">Penerapan PSAK</a> · '
            f'<a href="/laporan-tahunan-pt/{s}/">Laporan Tahunan PT (SABH)</a></p><!--/fa-kw3x-->')

# ---------------- definisi keluarga ----------------
PSAKS = [("PSAK 109", "Instrumen keuangan: klasifikasi aset keuangan dan cadangan kerugian kredit ekspektasian (CKPN) piutang", "/jasa-implementasi-psak-109/", "109"),
         ("PSAK 115", "Pendapatan dari kontrak dengan pelanggan: lima langkah, kontraktor, termin, retensi", "/jasa-implementasi-psak-115/", "115"),
         ("PSAK 116", "Sewa: aset hak guna dan liabilitas sewa untuk gedung, kendaraan, alat berat", "/jasa-implementasi-psak-116/", "116"),
         ("PSAK 117", "Kontrak asuransi: pengukuran kontrak dan CSM", "/jasa-implementasi-psak-117/", "117"),
         ("PSAK 118", "Penyajian laba rugi format baru (kategori operasi, investasi, pendanaan), wajib mulai tahun buku 2027", "/jasa-implementasi-psak-118/", "118"),
         ("PSAK 212", "Pajak penghasilan: pajak tangguhan dan rekonsiliasi fiskal", "/jasa-implementasi-psak-212/", "212"),
         ("PSAK 219", "Imbalan kerja: liabilitas pesangon UU Cipta Kerja dan aktuaria", "/jasa-implementasi-psak-219/", "219"),
         ("PSAK 110", "Laporan keuangan konsolidasian untuk grup usaha", "/jasa-konsolidasi-laporan-keuangan-psak-110/", "110"),
         ("SAK EP", "Transisi dari SAK ETAP ke SAK EP atau dari SAK EP ke PSAK penuh", "/jasa-transisi-sak-ep-ke-psak/", None)]
US = "https://updatesak.com"
FAM = {}
FAM["jasa-buku-besar"] = dict(
    kind="lk", eyebrow="Jasa Buku Besar", short="Buku Besar",
    h1="Jasa Buku Besar (General Ledger) di {n}: Rapi, Seimbang, Siap Jadi Laporan Keuangan",
    title="Jasa Buku Besar {n}: General Ledger dan Neraca Saldo", ptitle="Jasa Buku Besar (General Ledger): Rapi dan Siap Audit",
    desc="Jasa buku besar di {n}: posting jurnal, rekonsiliasi bank, buku pembantu piutang, utang, persediaan, neraca saldo seimbang. Oleh KJA Farhani, kontak via FA Indonesia.",
    lead="Buku besar yang tidak seimbang, akun yang bercampur, atau saldo bank yang tidak cocok membuat laporan keuangan tidak bisa dipercaya bank dan auditor. Kami merapikan dari jurnal sampai neraca saldo, lalu laporan keuangan langsung bisa disusun.",
    wamsg="Halo Pak Ananta, saya{dari} perlu jasa buku besar (general ledger). Periode: ... Jumlah transaksi per bulan: ...",
    what="jasa buku besar, posting jurnal, dan rekonsiliasi",
    secs=lambda n: [
        ("Yang Dikerjakan dalam Jasa Buku Besar", tbl(["Pekerjaan", "Isi"], [
            ("Bagan akun (COA)", "Menyusun atau merapikan kode akun supaya setiap pos laporan keuangan punya akun yang jelas"),
            ("Posting jurnal", "Jurnal penjualan, pembelian, kas dan bank, gaji, dan jurnal umum dicatat per tanggal dengan bukti"),
            ("Rekonsiliasi bank", "Saldo buku dicocokkan dengan rekening koran setiap bulan, selisih dicari sampai jelas"),
            ("Buku pembantu", "Piutang per pelanggan, utang per pemasok, persediaan, dan aset tetap yang cocok dengan saldo buku besar"),
            ("Jurnal penyesuaian", "Penyusutan, akrual, biaya dibayar dimuka, cadangan piutang, dan pajak"),
            ("Neraca saldo", "Trial balance yang seimbang, siap diolah menjadi laporan keuangan lengkap")])),
        ("Kenapa Buku Besar Sering Tidak Bisa Dipakai", "<p>Tiga penyebab yang paling sering kami temui: transaksi pribadi dan usaha tercampur di satu rekening, akun dibuat sesuka hati sehingga satu pos tersebar di banyak akun, dan saldo awal tahun tidak pernah dicocokkan dengan laporan tahun lalu. Akibatnya laporan laba rugi naik turun tanpa alasan dan auditor meminta koreksi berkali-kali.</p>"
         "<p>Perbaikannya dimulai dari saldo awal dan rekening bank, lalu mundur ke transaksi. Untuk usaha yang belum punya pembukuan sama sekali, buku besar disusun dari mutasi rekening dan bukti yang ada.</p>"),
        ("Nyambung dengan FA Jupiter", f'<p>Format buku besar kami sama dengan format impor <a href="/audit-ready/">FA Jupiter</a>: sheet COA (kode akun, nama akun, pos laporan keuangan, saldo pembanding) dan GL (nomor jurnal, tanggal, akun, keterangan, debit, kredit). Begitu buku besar selesai, laporan keuangan lengkap dengan CALK format auditor keluar otomatis. Contoh formatnya ada di <a href="{F_XLSX}" download>file Excel ini</a>.</p>'),
        ("Deliverables yang Anda Terima", tbl(["Deliverable", "Isi", "Waktu"], [
            ("Buku besar per akun", "Excel, bisa ditelusuri ke bukti transaksi", "Bulanan"),
            ("Neraca saldo", "Seimbang, saldo awal cocok dengan tahun lalu", "Bulanan"),
            ("Rekonsiliasi bank dan buku pembantu", "Bank, piutang, utang, persediaan, aset tetap", "Bulanan"),
            ("Laporan keuangan", "Neraca, laba rugi, arus kas, perubahan ekuitas, CALK (opsional)", "Bulanan atau tahunan")]))],
    faq=lambda n: [(f"Ada jasa buku besar di {n}?", f"Ada. Usaha di {n} cukup mengirim mutasi rekening dan bukti transaksi lewat Google Drive. Pekerjaan dilakukan KJA Farhani K.N., kontak lewat FA Indonesia."),
                   ("Apa beda jasa buku besar dan jasa pembukuan?", "Pembukuan biasanya berhenti di pencatatan transaksi. Jasa buku besar memastikan semua akun seimbang, saldo cocok dengan bank dan buku pembantu, dan siap diolah menjadi laporan keuangan yang dipakai bank dan auditor."),
                   ("Bisa merapikan buku besar beberapa tahun yang sudah berantakan?", "Bisa. Kami mulai dari saldo awal yang bisa dibuktikan, lalu menyusun ulang per tahun sampai tahun berjalan."),
                   ("Aplikasi akuntansi apa yang dipakai?", "Bisa memakai aplikasi yang sudah Anda pakai (Accurate, Jurnal, Zahir, dan lainnya) atau Excel. Hasil akhirnya tetap bisa diekspor ke format FA Jupiter.")],
    see='<a href="/jasa-penyusunan-laporan-keuangan/">Penyusunan Laporan Keuangan</a> · <a href="/jasa-laporan-keuangan-bulanan/">Laporan Keuangan Bulanan</a> · <a href="https://cariakuntan.com/jasa-pembukuan/">Jasa Pembukuan Terima Beres</a> · <a href="/audit-ready/">FA Jupiter</a> · <a href="https://updatesak.com/buku-besar/">Panduan Buku Besar (UpdateSAK)</a>')

FAM["jasa-pendampingan-audit"] = dict(
    kind="tim", eyebrow="Pendampingan Audit", short="Pendampingan Menghadapi Auditor",
    h1="Jasa Pendampingan Audit di {n}: Siap Menjawab Permintaan Auditor KAP",
    title="Jasa Pendampingan Audit {n}: Menjawab Auditor KAP", ptitle="Jasa Pendampingan Audit: Siap Menjawab Auditor KAP",
    desc="Pendampingan perusahaan di {n} saat diaudit KAP: menyiapkan PBC list, skedul pendukung, konfirmasi, menjawab temuan dan koreksi audit sampai laporan auditor terbit.",
    lead="Audit sering molor bukan karena auditornya, tetapi karena data yang diminta belum siap dan pertanyaan auditor dijawab seadanya. Kami berdiri di sisi perusahaan: menyiapkan dokumen, menjawab pertanyaan teknis, dan membahas koreksi audit dengan bahasa auditor.",
    wamsg="Halo Pak Ananta, saya{dari} sedang/akan diaudit KAP dan perlu pendampingan menjawab permintaan auditor. Tahun buku: ...",
    what="pendampingan perusahaan yang sedang diaudit",
    secs=lambda n: [
        ("Yang Kami Bantu Selama Audit", tbl(["Tahap Audit", "Pendampingan dari Sisi Perusahaan"], [
            ("Sebelum audit", "Menyiapkan daftar PBC (prepared by client), neraca saldo final, dan skedul pendukung per akun"),
            ("Perencanaan auditor", "Menjelaskan proses bisnis, pengendalian internal, dan transaksi tidak biasa kepada auditor"),
            ("Konfirmasi dan pengujian", "Membantu mengirim dan mengejar konfirmasi bank, piutang, utang; menyiapkan sampel bukti yang diminta"),
            ("Pertanyaan dan temuan", "Menyusun jawaban tertulis yang lengkap dengan dasar SAK dan bukti, bukan jawaban lisan yang berubah-ubah"),
            ("Koreksi audit", "Membahas usulan jurnal koreksi, menilai dampaknya ke pajak dan covenant bank, lalu membukukannya"),
            ("Akhir audit", "Mereviu draf laporan keuangan audited dan CALK, surat representasi manajemen, dan management letter")])),
        ("Supaya Audit Tidak Molor", "<p>Auditor bekerja berdasarkan Standar Audit IAPI: setiap angka harus didukung bukti yang cukup dan tepat. Bila skedul pendukung tidak cocok dengan neraca saldo, atau satu permintaan dijawab dengan dokumen yang berbeda-beda, auditor harus menambah prosedur dan jadwal mundur.</p>"
         "<p>Kami menyusun skedul pendukung dengan pola kertas kerja KAP, karena tim FA menulis aplikasi audit FA Saturn dari Standar Audit yang sama. Pertanyaan auditor dijawab dengan bahasa dan rujukan yang auditor pakai.</p>"),
        ("Independensi Tetap Terjaga", "<p>Pendampingan ini untuk perusahaan, bukan untuk auditor. Kami tidak ikut menyatakan opini dan tidak menekan auditor. Bila auditor Anda adalah KAP DHN &amp; Rekan, penyiapan laporan keuangan dan skedul dilakukan pihak yang berbeda dari tim audit, karena untuk satu entitas penyusun dan auditornya selalu pihak yang berbeda.</p>"),
        ("Deliverables yang Anda Terima", tbl(["Deliverable", "Isi", "Waktu"], [
            ("Daftar PBC dan status", "Per akun, siapa yang menyiapkan, tenggat, status kirim", "Minggu pertama"),
            ("Skedul pendukung", "Kas dan bank, piutang dan umur, persediaan, aset tetap, utang, pajak, ekuitas", "1-3 minggu"),
            ("Jawaban tertulis atas pertanyaan auditor", "Dengan rujukan SAK dan bukti", "Selama audit"),
            ("Analisis koreksi audit", "Dampak ke laba, pajak, dan rasio covenant bank", "Akhir audit")]))],
    faq=lambda n: [(f"Ada jasa pendampingan audit di {n}?", f"Ada. Perusahaan di {n} bisa didampingi daring sejak persiapan audit sampai laporan auditor terbit, dengan kunjungan bila diperlukan."),
                   ("Apakah pendampingan ini menjamin opini WTP?", "Tidak. Opini adalah keputusan independen auditor. Yang kami bantu adalah kesiapan data, kelengkapan bukti, dan jawaban yang tepat, sehingga auditor punya dasar yang cukup."),
                   ("Kapan sebaiknya mulai didampingi?", "Idealnya sebelum auditor datang, saat neraca saldo final disusun. Tetapi pendampingan juga bisa dimulai di tengah audit yang sudah berjalan."),
                   ("Bisa membantu bila auditnya dari KAP lain?", "Bisa. Pendampingan diberikan kepada perusahaan, siapa pun KAP yang mengaudit.")],
    see='<a href="/jasa-audit-laporan-keuangan/">Audit Laporan Keuangan</a> · <a href="/artikel/laporan-audit-lama-keluar/">Laporan Audit Lama Keluar</a> · <a href="/artikel/dari-opini-wdp-ke-wtp/">Dari Opini WDP ke WTP</a> · <a href="/saturn/">FA Saturn</a> · <a href="https://updatesak.com/menghadapi-auditor/">Panduan Menghadapi Auditor (UpdateSAK)</a>')

FAM["konsultan-penerapan-psak"] = dict(
    kind="tim", eyebrow="Penerapan PSAK", short="Penerapan PSAK",
    h1="Konsultan Penerapan PSAK di {n}: PSAK 109, 115, 116, 118, 219, dan Lainnya",
    title="Konsultan Penerapan PSAK {n}: 109, 115, 116, 118, 219", ptitle="Konsultan Penerapan PSAK: 109, 115, 116, 118, 219",
    desc="Konsultan penerapan PSAK di {n}: PSAK 109 CKPN, 115 pendapatan, 116 sewa, 118 penyajian laba rugi 2027, 212 pajak tangguhan, 219 imbalan kerja. Langsung dengan Ananta, CPA.",
    lead="Standar baru biasanya terasa saat auditor meminta penyesuaian atau saat format laporan keuangan berubah. Kami menerjemahkan PSAK ke kebijakan akuntansi, jurnal, dan template Excel yang dipakai tim keuangan Anda sendiri.",
    wamsg="Halo Pak Ananta, saya{dari} perlu konsultan penerapan PSAK ... (nomor PSAK). Standar yang dipakai sekarang: SAK EP / PSAK.",
    what="pendampingan penerapan PSAK",
    secs=lambda n: [
        ("PSAK yang Paling Sering Diterapkan", tbl(["Standar", "Yang Dikerjakan", "Rincian"], [
            (a, b, f'<a href="{c}">Layanan</a>' + (f' · <a href="{US}/psak/{u}/">Ringkasan</a>' if u else "")) for a, b, c, u in PSAKS])),
        ("Cara Kerja Penerapan", tbl(["Langkah", "Isi"], [
            ("1. Diagnosa dampak", "Transaksi mana yang terdampak, berapa besar perubahan angka, dan apakah covenant bank ikut terpengaruh"),
            ("2. Kebijakan akuntansi", "Kebijakan tertulis yang sesuai standar dan bisa dipertahankan di depan auditor"),
            ("3. Model dan jurnal", "Template Excel perhitungan (misalnya CKPN, jadwal sewa, alokasi harga transaksi) dan jurnal transisi"),
            ("4. Penyajian dan CALK", "Format laporan keuangan dan pengungkapan baru, termasuk angka pembanding"),
            ("5. Serah terima", "Pelatihan singkat tim keuangan supaya perhitungan bisa diulang sendiri setiap periode")])),
        ("PSAK 118 Mulai Tahun Buku 2027", '<p>PSAK 118 mengganti cara laba rugi disajikan: ada kategori operasi, investasi, dan pendanaan, subtotal laba usaha yang baku, serta pengungkapan ukuran kinerja yang ditetapkan manajemen. Karena angka pembanding tahun 2026 ikut disajikan ulang, persiapannya sebaiknya dimulai sekarang. Simulasi gratis tersedia di <a href="/cek-psak-118/">Cek PSAK 118</a>.</p>'),
        ("Deliverables yang Anda Terima", tbl(["Deliverable", "Isi", "Waktu"], [
            ("Analisis dampak PSAK", "Pos terdampak dan estimasi angka", "1-2 minggu"),
            ("Kebijakan akuntansi tertulis", "Siap direviu auditor", "2-3 minggu"),
            ("Template perhitungan Excel", "Bisa dipakai ulang tiap periode", "2-4 minggu"),
            ("Draf penyajian dan CALK", "Termasuk angka pembanding", "Saat tutup buku")]))],
    faq=lambda n: [(f"Ada konsultan penerapan PSAK di {n}?", f"Ada. Perusahaan di {n} didampingi daring dengan Ananta W. Sasongko, CPA, dan kunjungan bila diperlukan."),
                   ("PSAK mana yang wajib untuk perusahaan saya?", "Tergantung standar yang dipakai. Entitas dengan akuntabilitas publik (misalnya emiten dan lembaga keuangan) memakai PSAK penuh; perusahaan lain umumnya SAK EP, dan UMKM SAK EMKM. Kami cek dulu dari laporan keuangan terakhir Anda."),
                   ("Apakah bisa hanya satu PSAK?", "Bisa. Banyak klien datang untuk satu standar, misalnya PSAK 116 sewa atau PSAK 219 imbalan kerja, karena diminta auditor."),
                   ("Apakah hasilnya diterima auditor?", "Kebijakan dan perhitungan disusun dengan dasar standar dan dokumentasi yang auditor butuhkan. Penilaian akhir tetap di tangan auditor.")],
    see='<a href="/jasa-implementasi-psak/">Jasa Implementasi PSAK</a> · <a href="/cek-psak-118/">Cek PSAK 118</a> · <a href="https://updatesak.com/penerapan-psak/">Langkah Penerapan PSAK (UpdateSAK)</a> · <a href="https://updatesak.com/update-psak-2026/">Update PSAK 2026</a>')

FAM["laporan-tahunan-pt"] = dict(
    kind="lk", eyebrow="Laporan Tahunan PT · SABH", short="Laporan Tahunan PT (SABH)",
    h1="Laporan Tahunan PT untuk SABH di {n}: Siap Dibawa ke Notaris",
    title="Laporan Tahunan PT SABH {n}: Siap Akta Notaris", ptitle=None,
    desc="Laporan tahunan PT di {n} untuk SABH (Permenkum 49/2025): laporan keuangan dan CALK, laporan tahunan Pasal 16, siap akta notaris. Template gratis. Kontak via FA Indonesia.",
    lead="Persetujuan RUPS atas laporan tahunan PT kini dituangkan dalam akta notaris dan disampaikan lewat SABH. Yang paling sering belum siap adalah laporan keuangan dan catatannya. Kami siapkan sampai notaris tinggal membuat akta.",
    wamsg="Halo Pak Ananta, saya{dari} perlu laporan tahunan PT untuk SABH (akta notaris). Tahun buku: ... Wajib audit: ya/tidak/belum tahu",
    what="penyusunan laporan tahunan PT dan laporan keuangan untuk SABH",
    secs=lambda n: [
        ("Isi Laporan Tahunan yang Diminta Notaris", tbl(["Bagian", "Keterangan"], [
            ("Laporan keuangan", "Neraca dengan pembanding, laba rugi, arus kas, perubahan ekuitas, dan catatan atas laporan keuangan"),
            ("Laporan kegiatan perseroan", "Kegiatan usaha selama tahun buku"),
            ("Tanggung jawab sosial dan lingkungan", "Program TJSL yang dijalankan"),
            ("Permasalahan", "Masalah yang memengaruhi kegiatan usaha"),
            ("Pengawasan Dewan Komisaris", "Laporan tugas pengawasan"),
            ("Direksi dan Dewan Komisaris", "Nama serta gaji, honorarium, dan tunjangan")])),
        ("Pembagian Peran", tbl(["Pekerjaan", "Penyusun (KJA Farhani)", "Notaris"], [
            ("Laporan keuangan dan CALK", "Menyusun, Lembar Penyusun ditandatangani Akuntan Berpraktik", "Tidak"),
            ("Laporan tahunan", "Menyiapkan draf sesuai Pasal 16", "Tidak"),
            ("Keputusan RUPS atau sirkuler", "Draf ilustrasi", "Menuangkan dalam akta"),
            ("Penyampaian SABH", "Memantau sampai bukti terbit", "Mengirim")]) +
         "<p>Bila PT wajib audit (Pasal 68 UU PT, misalnya aset atau omzet paling sedikit Rp50 miliar), laporan keuangan diaudit KAP DHN &amp; Rekan yang terdaftar OJK. Penyusun dan auditornya pihak yang berbeda.</p>"),
        ("Template Gratis untuk Notaris dan Direksi", sabh_box() .replace("<!--fa-kw3t-->", "").replace("<!--/fa-kw3t-->", "")),
    ],
    faq=lambda n: [(f"Bisa dibantu laporan tahunan PT untuk SABH di {n}?", f"Bisa. PT di {n} cukup mengirim data lewat Google Drive. Laporan keuangan disusun KJA Farhani K.N., audit (bila wajib) oleh KAP DHN & Rekan, kontak lewat FA Indonesia."),
                   ("Apakah semua PT harus lewat notaris?", "Kewajiban Pasal 16 Permenkum 49/2025 berlaku untuk PT persekutuan modal. PT perorangan memakai mekanisme pelaporan yang berbeda."),
                   ("Apa risikonya bila belum lapor?", "Teguran tertulis lewat SABH, lalu pemblokiran akses bila 30 hari setelah teguran belum dipenuhi. Selama diblokir, perubahan pengurus dan peralihan saham tertahan."),
                   ("Siapa yang menandatangani laporan keuangannya?", "Direksi bertanggung jawab atas laporan keuangan. Lembar Penyusun ditandatangani Akuntan Berpraktik atau Kantor Jasa Akuntansi yang menyusun; bila wajib audit, diganti Laporan Auditor Independen dari KAP.")],
    see='<a href="/laporan-keuangan-sabh/">Panduan SABH dan Template</a> · <a href="/laporan-tahunan-pt/">Laporan Tahunan PT</a> · <a href="/mitra-notaris/">Untuk Notaris</a> · <a href="/jasa-audit-laporan-keuangan/">Audit Laporan Keuangan</a> · <a href="https://cariakuntan.com/laporan-keuangan-sabh/">Cek Kebutuhan SABH (CariAkuntan)</a>')


def build_main(base, f, k, path, back):
    n = k["name"] if k else "Indonesia"
    nm = k["name"] if k else ""
    dari = f" dari {nm}" if k else ""
    h1 = f["h1"].format(n=n) if k else (f["ptitle"] or f["h1"].format(n="Indonesia"))
    if not k: h1 = re.sub(r" di Indonesia", "", h1)
    msg = f["wamsg"].format(dari=dari)
    btn = f'<a class="btn solid" href="{wa(msg)}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
    secs = f["secs"](n)
    nav, body = [], []
    for h, hh in secs:
        i = hid(h); nav.append(f'<li><a href="#{i}">{E(h)}</a></li>'); body.append(f'<h2 id="{i}">{E(h)}</h2>{hh}')
    ar = ""
    if k:
        ar = area(base, f"{f['what']} di seluruh {E(nm)}")
        if ar:
            m = re.search(r"<h2>(.*?)</h2>", ar); i = hid(m.group(1)); ar = ar.replace("<h2>", f'<h2 id="{i}">', 1); nav.append(f'<li><a href="#{i}">{m.group(1)}</a></li>')
    else:
        rows = []
        for pv in sorted(BYPROV):
            rows.append(f"<p><b>{E(pv)}:</b> " + " · ".join(f'<a href="/{f.get("citykey", f["key"])}/{x["slug"]}/">{E(x["name"])}</a>' for x in BYPROV[pv]) + "</p>")
        i = "per-kota"; nav.append(f'<li><a href="#{i}">Layanan per Kota</a></li>')
        ar = f'<h2 id="{i}">Layanan per Kota</h2><details><summary>{len(KOTA)} kota di {len(BYPROV)} provinsi</summary>' + "".join(rows) + "</details>"
    pmap = f'<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>{"".join(nav)}</ol></nav>'
    if k:
        intro = f"Untuk perusahaan, UMKM, klinik, kontraktor, koperasi, dan yayasan di {E(nm)}, {E(k['prov'])}" + (f". {E(nm)} adalah {E(k['note'])}" if k["note"] else "") + ". Dokumen dikirim lewat Google Drive, pertemuan daring atau kunjungan terjadwal."
    else:
        intro = f"Untuk perusahaan di seluruh Indonesia, dari {len(KOTA)} kota di {len(BYPROV)} provinsi sampai kabupaten. Dokumen dikirim lewat Google Drive, pertemuan daring atau kunjungan terjadwal."
    kontak = lk2(base, k) if f["kind"] == "lk" else ""
    fx = (fanx(base) + kw3x(k)) if k else ""
    faq = f["faq"](n)
    fq = '<h2>Pertanyaan Umum</h2><div class="faq-acc">' + "".join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq) + "</div>"
    main = ('<main id="top">\n<section class="block">\n<div class="wrap art">\n'
            f'<p class="eyebrow">{E(f["eyebrow"])}{" · " + E(nm) if k else ""}</p>\n'
            f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{E(h1)}</h1><div class="tshare-top"><div class="share" data-lab="Bagikan" data-tool="{E(h1)}"></div></div>\n'
            f'<p class="t" style="max-width:62em">{E(f["lead"])}</p>\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px">{btn}<a class="btn line" href="{back[0]}">{E(back[1])}</a></div>'
            + kontak + TIM + f"\n<p>{intro}</p>{pmap}" + "".join(body) + ar + fx + TOOLS
            + f'<p class="t">Lihat juga: {f["see"]}</p>\n\n' + fq
            + f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px">{btn}</div>\n</div>\n</section>\n</main>')
    return h1, main, faq


def page(f, k):
    key = f["key"]
    path = f"/{key}/{k['slug']}/" if k else f"/{key}/"
    base = rd(P(f"/jasa-penyusunan-laporan-keuangan/{k['slug']}/")) if k else TPLM
    back = (f"/{key}/", f["short"] + " Seluruh Indonesia") if k else ("/layanan/", "Semua Layanan FA")
    h1, main, faq = build_main(base, f, k, path, back)
    n = k["name"] if k else "Indonesia"
    title = (f["title"].format(n=n) if k else (f["ptitle"] or f["title"].format(n="Indonesia"))) + " | FA Indonesia"
    if len(title) > 65: title = title.replace(" | FA Indonesia", "")
    desc = cut(f["desc"].format(n=n))
    url = D + path
    crumb = [("Beranda", "/"), (f["short"], f"/{key}/")] + ([(k["name"], path)] if k else [])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": h1, "serviceType": f["short"],
         "provider": {"@type": "ProfessionalService", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"},
         "areaServed": ({"@type": "City", "name": k["name"]} if k else {"@type": "Country", "name": "Indonesia"}), "url": url},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a, "item": D + u} for i, (a, u) in enumerate(crumb)]}]}
    head = base[:base.index("<main")]
    T, Dd = E(title), E(desc)
    head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{T}</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description")/>', lambda m: f'<meta content="{Dd}" {m.group(1)}/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:title"/>', lambda m: f'<meta content="{T}" property="og:title"/>', head)
    head = re.sub(r'<link href="[^"]*" rel="canonical"/>', lambda m: f'<link href="{url}" rel="canonical"/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:url"/>', lambda m: f'<meta content="{url}" property="og:url"/>', head)
    head = re.sub(r'<link[^>]*hreflang[^>]*>', "", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", head, count=1, flags=re.S)
    t = head + main + base[base.index("</main>") + 7:]
    wt(P(path), t)
    return path


NEW = []
for key, f in FAM.items():
    f["key"] = key
    if key != "laporan-tahunan-pt": NEW.append(page(f, None))
    for k in KOTA: NEW.append(page(f, k))

# ---------------- pilar edukasi SABH ----------------
S = dict(FAM["laporan-tahunan-pt"]); S["key"] = "laporan-keuangan-sabh"; S["citykey"] = "laporan-tahunan-pt"
S.update(eyebrow="Panduan SABH · Template Gratis", short="Laporan Keuangan untuk SABH",
         ptitle="Laporan Keuangan untuk SABH: Panduan dan Template untuk Notaris", title="Laporan Keuangan SABH: Panduan dan Template Notaris",
         desc="Panduan laporan tahunan PT untuk SABH (Permenkum 49/2025) dan template gratis Word/Excel: format laporan keuangan, CALK, Lembar Penyusun Akuntan Berpraktik, checklist notaris.",
         lead="Sejak Permenkum 49/2025, persetujuan RUPS atas laporan tahunan PT persekutuan modal dituangkan dalam akta notaris dan disampaikan lewat SABH. Halaman ini merangkum alurnya dan menyediakan template yang bisa langsung dipakai Direksi dan Notaris.",
         wamsg="Halo Pak Ananta, saya{dari} sudah lihat template SABH dan perlu dibantu menyusun laporan tahunan PT. Tahun buku: ...",
         secs=lambda n: [
             ("Download Template", sabh_box().replace("<!--fa-kw3t-->", "").replace("<!--/fa-kw3t-->", "") +
              tbl(["Isi Template Word", "Keterangan"], [
                  ("Bagian A, Laporan Tahunan", "Kegiatan, TJSL, permasalahan, pengawasan Komisaris, susunan pengurus, gaji dan tunjangan, kolom tanda tangan"),
                  ("Surat Pernyataan Direksi", "Tanggung jawab Direksi atas laporan keuangan"),
                  ("Lembar Penyusun", "Kolom nama, nomor izin, dan tanda tangan Akuntan Berpraktik atau KJA yang menyusun (perikatan kompilasi)"),
                  ("Laporan keuangan", "Posisi keuangan, laba rugi, perubahan ekuitas, arus kas dengan angka ilustrasi yang saling cocok"),
                  ("Catatan atas laporan keuangan", "Kerangka CALK dari umum sampai peristiwa setelah periode pelaporan"),
                  ("Bagian C, Lampiran untuk Notaris", "Checklist dokumen dan ilustrasi keputusan pemegang saham secara sirkuler")])),
             ("Alur dari Laporan Keuangan sampai SABH", tbl(["Tahap", "Siapa", "Keterangan"], [
                 ("1. Laporan keuangan", "Penyusun (Akuntan Berpraktik/KJA) atau KAP bila wajib audit", "Lengkap dengan CALK dan angka pembanding"),
                 ("2. Laporan tahunan", "Direksi, ditelaah Dewan Komisaris", "Isi minimal Pasal 16 ayat (6) Permenkum 49/2025"),
                 ("3. RUPS atau keputusan sirkuler", "Pemegang saham", "Paling lambat 6 bulan setelah tahun buku berakhir"),
                 ("4. Akta notaris", "Notaris", "Persetujuan RUPS dituangkan dalam akta"),
                 ("5. Penyampaian SABH", "Notaris", "Paling lama 30 hari sejak akta, dengan lampiran laporan tahunan")])),
             ("Nyambung dengan FA Jupiter", '<p>Template Excel memakai format impor <a href="/audit-ready/">FA Jupiter</a> (sheet COA dan GL). Isi buku besar, upload ke FA Jupiter, lalu salin Neraca, Laba Rugi, Perubahan Ekuitas, Arus Kas, dan CALK yang keluar ke bagian B template Word. Data contoh di FA Jupiter bebas dicoba dan diunduh.</p>'),
             ("Siapa yang Menandatangani", '<p>Direksi menandatangani Surat Pernyataan dan bertanggung jawab atas laporan keuangan. Bila laporan keuangan disusun pihak luar, Lembar Penyusun ditandatangani Akuntan Berpraktik atau Kantor Jasa Akuntansi yang menyusun, dengan nama dan nomor izinnya sendiri, dalam perikatan kompilasi (tanpa opini). Bila PT wajib audit, lembar itu diganti Laporan Auditor Independen dari Kantor Akuntan Publik. Ringkasan standar kompilasi ada di <a href="https://updatesak.com/standar-audit/sjt-4410/">UpdateSAK: SJT 4410</a>.</p>'),
             ("Untuk Notaris", '<p>Notaris yang menerima klien dengan laporan keuangan belum siap bisa membagikan template ini, atau merujuk klien lewat <a href="/mitra-notaris/">program Untuk Notaris</a>. Laporan keuangan disusun KJA Farhani K.N.; audit, bila wajib, oleh KAP DHN &amp; Rekan yang terdaftar OJK. Honorarium notaris dibayar langsung oleh perusahaan.</p>')],
         see='<a href="/laporan-tahunan-pt/">Jasa Laporan Tahunan PT</a> · <a href="/mitra-notaris/">Untuk Notaris</a> · <a href="https://updatesak.com/laporan-keuangan-sabh/">Edukasi SABH (UpdateSAK)</a> · <a href="https://cariakuntan.com/laporan-keuangan-sabh/">Cek Kebutuhan SABH (CariAkuntan)</a>')
NEW.insert(0, page(S, None))

# ---------------- sisipan ----------------
nx = 0
for k in KOTA:
    for fp in glob.glob(os.path.join(OUT, "*", k["slug"], "index.html")):
        t = rd(fp)
        if "<!--/fanas-x-->" not in t: continue
        t2 = re.sub(r"<!--fa-kw3x-->.*?<!--/fa-kw3x-->", "", t, flags=re.S)
        t2 = t2.replace("</section><!--/fanas-x-->", "</section><!--/fanas-x-->" + kw3x(k), 1) if "</section><!--/fanas-x-->" in t2 else t2.replace("<!--/fanas-x-->", "<!--/fanas-x-->" + kw3x(k), 1)
        nx += wt(fp, t2)
# kotak template di pilar /laporan-tahunan-pt/
fp = P("/laporan-tahunan-pt/"); t = rd(fp)
t = re.sub(r"<!--fa-kw3t-->.*?<!--/fa-kw3t-->", "", t, flags=re.S)
i = t.index("</p>", t.index('class="t"', t.index("<h1"))) + 4
t = t[:i] + sabh_box() + t[i:]
t = re.sub(r"<!--fa-kw3k-->.*?<!--/fa-kw3k-->", "", t, flags=re.S)
rows = "".join(f"<p><b>{E(pv)}:</b> " + " · ".join(f'<a href="/laporan-tahunan-pt/{x["slug"]}/">{E(x["name"])}</a>' for x in BYPROV[pv]) + "</p>" for pv in sorted(BYPROV))
t = t.replace("<h2>Pertanyaan Umum</h2>", f'<!--fa-kw3k--><h2>Laporan Tahunan PT per Kota</h2><details><summary>{len(KOTA)} kota</summary>{rows}</details><!--/fa-kw3k--><h2>Pertanyaan Umum</h2>', 1)
wt(fp, t)

# sitemap
sm = os.path.join(OUT, "sitemap.xml"); t = rd(sm)
t = re.sub(r"<!--kw3-->.*?<!--/kw3-->", "", t, flags=re.S)
urls = [D + p for p in NEW]
blk = "<!--kw3-->" + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "<!--/kw3-->"
t = t.replace("</urlset>", blk + "</urlset>", 1); wt(sm, t)
# llms
ll = os.path.join(OUT, "llms.txt"); t = rd(ll)
t = re.sub(r"\n## Kata Kunci Baru 9 Nov 2026\n.*?(?=\n## |\Z)", "", t, flags=re.S)
t = t.rstrip() + ("\n\n## Kata Kunci Baru 9 Nov 2026\n"
                  f"- [Laporan Keuangan untuk SABH: Panduan dan Template]({D}/laporan-keuangan-sabh/): template Word/Excel laporan tahunan PT untuk Notaris, format FA Jupiter\n"
                  f"- [Jasa Buku Besar]({D}/jasa-buku-besar/): general ledger, rekonsiliasi, neraca saldo, per kota\n"
                  f"- [Jasa Pendampingan Audit]({D}/jasa-pendampingan-audit/): menyiapkan PBC dan menjawab auditor KAP, per kota\n"
                  f"- [Konsultan Penerapan PSAK]({D}/konsultan-penerapan-psak/): PSAK 109, 115, 116, 118, 212, 219, per kota\n"
                  f"- [Laporan Tahunan PT per Kota]({D}/laporan-tahunan-pt/malang/): SABH per kota\n")
wt(ll, t)
print("halaman baru", len(NEW), "sisipan kw3x", nx)
