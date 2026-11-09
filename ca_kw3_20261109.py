# -*- coding: utf-8 -*-
"""9 Nov 2026 (Bos): keyword FA juga harus ada di CariAkuntan: Konsultan Rumah Sakit [kota], Jasa Buku Besar, Pendampingan
Audit (menjawab auditor KAP) [kota], Konsultan PSAK [kota], edukasi SABH + template untuk Notaris (file di faindonesia.co.id/template/).
Sudut CariAkuntan berbeda dari FA (bukan salinan): cara memilih, checklist, standar mana yang berlaku, lalu Tanya Ananta, CPA.

BEKERJA LANGSUNG DI out/cariakuntan (template = halaman live /kota/<kota>/kap/). Jalankan setelah ca_ananta_20261109.py. Idempoten.
Halaman: pilar /konsultan-rumah-sakit/, /jasa-buku-besar/, /pendampingan-audit/, /konsultan-psak/, /laporan-keuangan-sabh/
+ /kota/<kota>/<konsultan-rumah-sakit|jasa-buku-besar|pendampingan-audit|konsultan-psak>/ (113 kota).
Sisipan: <!--ca-kw3--> di lipatan "Layanan Lain di X" semua halaman layanan kota dan di hub /kota/<kota>/, kotak template
<!--ca-kw3t--> di /kota/<kota>/laporan-tahunan-pt/ dan 4 artikel SABH, sitemap (<!--cakw3-->), llms.txt."""
import os, re, sys, json, html, glob, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "cariakuntan")
sys.path.insert(0, os.path.join(HERE, "cariakuntan"))
from cities import CITIES as CC

E = html.escape
D = "https://cariakuntan.com"; FA = "https://faindonesia.co.id"; US = "https://updatesak.com"
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
def cut(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    while len(s) > n and ". " in s: s = s.rsplit(". ", 1)[0] + "."
    if len(s) <= n: return s
    return s[:n].rsplit(" ", 1)[0].rstrip(",;:") + "."
def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

KOTA = [dict(name=k, slug=sl(k), prov=p, note=n) for k, p, r, s, n in CC]
BYPROV = {}
for k in KOTA: BYPROV.setdefault(k["prov"], []).append(k)
F_DOCX = FA + "/template/template-laporan-tahunan-pt-sabh-fa-indonesia.docx"
F_XLSX = FA + "/template/template-data-laporan-tahunan-sabh-fa-jupiter.xlsx"
F_PDF = FA + "/template/template-laporan-tahunan-pt-sabh-fa-indonesia.pdf"


def tbox(k=None):
    di = f" untuk PT di {E(k['name'])}" if k else ""
    return ('<!--ca-kw3t--><section class="ca-tanya" aria-label="Template SABH"><b class="t">Template Gratis: Laporan Tahunan PT untuk SABH' + di + '</b>'
            '<p>Format lengkap yang biasa diminta Notaris: laporan tahunan sesuai Pasal 16 Permenkum 49/2025, laporan keuangan dan CALK, Surat Pernyataan Direksi, '
            'Lembar Penyusun yang ditandatangani Akuntan Berpraktik, checklist dokumen, dan ilustrasi keputusan sirkuler. Angkanya bisa dihasilkan dari FA Jupiter.</p>'
            f'<div class="q"><a class="w" href="{F_DOCX}" download>Download Template Word</a><a href="{F_XLSX}" download>Excel Format FA Jupiter</a>'
            f'<a href="{F_PDF}" target="_blank" rel="noopener">Lihat Contoh PDF</a><a href="/laporan-keuangan-sabh/">Cek Kebutuhan SABH</a></div></section><!--/ca-kw3t-->')


def tanya(qs, k):
    dari = f" kami dari {k['name']}." if k else ""
    a = "".join(f'<a class="{"w" if i == 0 else ""}" href="{wa("Halo Pak Ananta," + dari + " " + m)}" target="_blank" rel="noopener">{E(l)}</a>' for i, (l, m) in enumerate(qs))
    return ('<!--ca-tanya--><section class="ca-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Dulu ke Ananta, CPA</b>'
            '<p>Belum yakin harus mulai dari mana? Tanyakan dulu ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.</p>'
            f'<div class="q">{a}</div></section><!--/ca-tanya-->')


FAM = {}
FAM["konsultan-rumah-sakit"] = dict(
    label="Konsultan Rumah Sakit", h1="Konsultan Rumah Sakit {n}: Cara Memilih Konsultan yang Paham Keuangan dan BPJS",
    title="Konsultan Rumah Sakit {n}: Keuangan, BPJS, Unit Cost", ptitle="Konsultan Rumah Sakit: Cara Memilih yang Paham Keuangan dan BPJS",
    desc="Cari konsultan rumah sakit di {n}? Checklist memilih konsultan: unit cost, klaim BPJS dan INA-CBG, akreditasi, farmasi, valuasi. Tanya Ananta, CPA dulu, gratis.",
    sub="Rumah sakit dan klinik di {n} biasanya mencari konsultan saat klaim BPJS tertunda, margin menipis, akreditasi mendekat, atau pemilik mulai berpikir menjual. Sebelum memilih, cek dulu apakah konsultannya pernah memimpin rumah sakit, bukan hanya membuat laporan.",
    wa="kami dari {n} sedang mencari konsultan rumah sakit.",
    qs=[("Klaim BPJS tertunda, kas seret", "klaim BPJS rumah sakit kami banyak pending dan kas seret. Bisa dibantu?"),
        ("Hitung unit cost dan tarif", "kami perlu menghitung unit cost dan tarif rumah sakit."),
        ("Rencana menjual atau mencari investor", "pemilik sedang menimbang menjual rumah sakit atau mencari investor.")],
    secs=lambda n, k: [
        ("Kapan Rumah Sakit Membutuhkan Konsultan", tbl(["Situasi", "Yang Biasanya Dibutuhkan"], [
            ("Klaim BPJS pending dan dispute menumpuk", "Audit koding INA-CBG, alur klaim, dan proyeksi kas"),
            ("Margin turun padahal pasien ramai", "Unit cost per layanan dan per DPJP, biaya obat per kasus"),
            ("Akreditasi atau perubahan kelas", "Kesiapan dokumen dan dampak biayanya"),
            ("Stok farmasi besar, kas tertahan", "ABC-VEN, dead stock, formularium"),
            ("Pemilik ingin menjual atau mencari investor", "Valuasi, data room, dan pendampingan negosiasi")])),
        ("Checklist Memilih Konsultan Rumah Sakit", "<p>Tanyakan lima hal ini sebelum menandatangani perikatan:</p><ol><li>Apakah konsultannya pernah menjabat direktur atau CFO rumah sakit?</li><li>Apakah mereka bisa menghitung unit cost dengan data SIMRS Anda sendiri, bukan angka rata-rata?</li><li>Apakah paham tarif INA-CBG dan alur klaim BPJS sampai ke dispute?</li><li>Apa deliverable tertulisnya, dan apakah model Excel-nya diserahkan?</li><li>Siapa yang benar-benar mengerjakan, dan apakah Anda bisa bicara langsung dengannya?</li></ol>"),
        ("Tim yang Kami Sarankan", f'<p>Untuk rumah sakit dan klinik di {E(n)}, pertanyaan pertama dijawab Ananta W. Sasongko, CPA (pernah direktur keuangan dan group CFO rumah sakit). Untuk sisi medis dan operasional, bersama dr. Sigit Riyarto, M.Kes, AAK (mantan direktur utama rumah sakit). Rincian layanan ada di <a href="{FA}/konsultan-rumah-sakit/{k["slug"] + "/" if k else ""}">FA Indonesia: Konsultan Rumah Sakit</a>, dan alat hitung gratisnya di <a href="{FA}/fa-venus-rumah-sakit/">FA Venus Rumah Sakit</a>.</p>')],
    faq=lambda n: [(f"Ada konsultan rumah sakit di {n}?", f"Ada. Rumah sakit dan klinik di {n} bisa mulai dengan tanya jawab lewat WhatsApp ke Ananta, CPA, lalu dilanjutkan daring atau kunjungan."),
                   ("Apakah konsultan bisa membantu klaim BPJS yang pending?", "Bisa, dengan memeriksa koding, kelengkapan berkas, dan alur verifikasi. Konsultan yang baik tidak menyarankan upcoding; yang dikejar adalah koding yang tepat dan berkas yang lengkap."),
                   ("Berapa lama hasilnya terlihat?", "Hitungan unit cost dan analisis farmasi biasanya 2 sampai 4 minggu. Perbaikan klaim dan kas terasa dalam 1 sampai 3 siklus klaim.")],
    fa="/konsultan-rumah-sakit/")

FAM["jasa-buku-besar"] = dict(
    label="Jasa Buku Besar", h1="Jasa Buku Besar {n}: Tanda Buku Besar Anda Perlu Dirapikan",
    title="Jasa Buku Besar {n}: Rapikan General Ledger", ptitle="Jasa Buku Besar: Tanda General Ledger Anda Perlu Dirapikan",
    desc="Jasa buku besar di {n}: tanda buku besar perlu dirapikan, apa yang diperiksa, dan siapa yang berizin mengerjakan (KJA atau Akuntan Berpraktik). Tanya Ananta, CPA, gratis.",
    sub="Buku besar adalah sumber semua laporan keuangan. Kalau buku besar di {n} tidak seimbang atau saldo banknya tidak cocok, laporan keuangan apa pun yang keluar dari situ akan dipertanyakan bank dan auditor.",
    wa="kami dari {n} perlu jasa buku besar.",
    qs=[("Neraca saldo saya tidak seimbang", "neraca saldo kami tidak seimbang dan saldo bank tidak cocok."),
        ("Rapikan buku besar beberapa tahun", "buku besar kami beberapa tahun berantakan dan perlu dirapikan."),
        ("Siapa yang berizin mengerjakan?", "siapa yang berizin mengerjakan buku besar dan laporan keuangan untuk usaha kami?")],
    secs=lambda n, k: [
        ("Tanda Buku Besar Perlu Dirapikan", tbl(["Tanda", "Akibatnya"], [
            ("Saldo bank di buku berbeda dengan rekening koran", "Kas tidak bisa dipercaya, auditor menambah prosedur"),
            ("Satu pos tersebar di banyak akun dengan nama mirip", "Laporan keuangan sulit dibaca dan tidak konsisten antar bulan"),
            ("Saldo awal tahun tidak sama dengan laporan tahun lalu", "Laba ditahan dan ekuitas tidak cocok"),
            ("Piutang dan utang tidak punya rincian per pihak", "Konfirmasi auditor dan penagihan sulit"),
            ("Transaksi pribadi dan usaha tercampur", "Laba usaha tidak terlihat dan pajak berisiko")])),
        ("Yang Diperiksa saat Merapikan Buku Besar", "<p>Bagan akun, saldo awal, rekonsiliasi bank per bulan, buku pembantu piutang, utang, persediaan, dan aset tetap, lalu jurnal penyesuaian sampai neraca saldo seimbang. Hasil akhirnya bisa langsung diolah menjadi laporan keuangan lengkap.</p>"
         f'<p>Format buku besar yang rapi juga bisa dibaca aplikasi gratis <a href="{FA}/audit-ready/">FA Jupiter</a> (sheet COA dan GL), yang mengubah buku besar menjadi laporan keuangan dengan catatan format auditor. Panduan lengkapnya ada di <a href="{US}/buku-besar/">UpdateSAK: Buku Besar</a>.</p>'),
        ("Siapa yang Berizin Mengerjakan", "<p>Jasa akuntansi untuk pihak lain dikerjakan oleh Akuntan Berpraktik atau Kantor Jasa Akuntansi (KJA) yang terdaftar di Kementerian Keuangan. Izinnya bisa dicek di <a href=\"/cek-izin/\">Cek Izin</a>. Untuk pertanyaan awal, Ananta, CPA menjawab gratis; pekerjaan buku besar dan laporan keuangan dilakukan KJA Farhani K.N.</p>")],
    faq=lambda n: [(f"Ada jasa buku besar di {n}?", f"Ada. Usaha di {n} cukup mengirim mutasi rekening dan bukti transaksi lewat Google Drive. Tanya dulu ke Ananta, CPA lewat WhatsApp."),
                   ("Apa beda buku besar dan neraca saldo?", "Buku besar memuat semua transaksi per akun. Neraca saldo adalah ringkasan saldo akhir semua akun yang jumlah debit dan kreditnya harus sama."),
                   ("Apakah harus pindah aplikasi akuntansi?", "Tidak. Buku besar bisa dirapikan di aplikasi yang sudah dipakai atau di Excel.")],
    fa="/jasa-buku-besar/")

FAM["pendampingan-audit"] = dict(
    label="Pendampingan Audit", h1="Pendampingan Audit {n}: Menghadapi Auditor KAP Tanpa Panik",
    title="Pendampingan Audit {n}: Menjawab Auditor KAP", ptitle="Pendampingan Audit: Menghadapi Auditor KAP Tanpa Panik",
    desc="Perusahaan di {n} akan diaudit KAP? Daftar dokumen yang diminta auditor (PBC), cara menjawab pertanyaan dan koreksi audit, dan kapan perlu pendamping. Tanya Ananta, CPA.",
    sub="Perusahaan di {n} yang pertama kali diaudit sering kaget dengan banyaknya permintaan auditor. Daftar di bawah membantu Anda bersiap, dan bila perlu, ada pendamping yang berdiri di sisi perusahaan.",
    wa="kami dari {n} akan diaudit KAP dan perlu pendampingan.",
    qs=[("Auditor minta dokumen, belum siap", "auditor KAP meminta banyak dokumen dan kami belum siap."),
        ("Ada koreksi audit, perlu dibahas", "ada usulan koreksi audit yang perlu kami bahas."),
        ("Pertama kali diaudit", "perusahaan kami pertama kali diaudit. Apa yang perlu disiapkan?")],
    secs=lambda n, k: [
        ("Dokumen yang Biasa Diminta Auditor (PBC)", tbl(["Akun", "Dokumen Pendukung"], [
            ("Kas dan bank", "Rekening koran setahun, rekonsiliasi bank akhir tahun, berita acara kas opname"),
            ("Piutang usaha", "Daftar umur piutang per pelanggan, faktur, bukti pelunasan setelah tanggal neraca"),
            ("Persediaan", "Hasil stok opname, kartu stok, perhitungan harga pokok"),
            ("Aset tetap", "Daftar aset dan penyusutan, bukti pembelian, sertifikat atau BPKB"),
            ("Utang dan pinjaman", "Daftar utang per pemasok, perjanjian kredit, jadwal angsuran"),
            ("Pajak", "SPT Masa dan Tahunan, bukti potong, rekonsiliasi fiskal"),
            ("Ekuitas dan legal", "Akta pendirian dan perubahan, notulen RUPS, daftar pemegang saham")])),
        ("Cara Menjawab Pertanyaan Auditor", "<ol><li>Jawab tertulis, satu pertanyaan satu jawaban, lengkap dengan buktinya.</li><li>Pastikan angka di skedul sama dengan neraca saldo final.</li><li>Kalau belum tahu, sampaikan tanggal kapan jawabannya diberikan, jangan menebak.</li><li>Untuk usulan koreksi, minta dasar standarnya, lalu hitung dampaknya ke pajak dan rasio pinjaman bank sebelum setuju.</li></ol>"
         f'<p>Standar yang dipakai auditor bisa dibaca ringkas di <a href="{US}/menghadapi-auditor/">UpdateSAK: Menghadapi Auditor</a>.</p>'),
        ("Kapan Perlu Pendamping", f'<p>Pendamping berguna bila tim keuangan kecil, audit pertama kali, laporan audit sebelumnya terlambat, atau ada koreksi besar yang memengaruhi kredit bank. Pendamping bekerja untuk perusahaan dan tidak memengaruhi opini auditor. Rincian layanan pendampingan ada di <a href="{FA}/jasa-pendampingan-audit/{k["slug"] + "/" if k else ""}">FA Indonesia: Pendampingan Audit</a>.</p>')],
    faq=lambda n: [(f"Ada pendampingan audit di {n}?", f"Ada. Perusahaan di {n} bisa didampingi daring sejak persiapan sampai laporan auditor terbit. Tanya dulu ke Ananta, CPA lewat WhatsApp."),
                   ("Apakah pendamping bisa menjamin opini WTP?", "Tidak. Opini adalah keputusan independen auditor. Pendamping membantu kesiapan data dan jawaban."),
                   ("Berapa lama audit biasanya berjalan?", "Untuk perusahaan menengah umumnya 4 sampai 8 minggu sejak data lengkap. Audit pertama biasanya lebih lama karena saldo awal ikut diperiksa.")],
    fa="/jasa-pendampingan-audit/")

FAM["konsultan-psak"] = dict(
    label="Konsultan PSAK", h1="Konsultan PSAK {n}: Standar Mana yang Berlaku untuk Usaha Anda",
    title="Konsultan PSAK {n}: Penerapan PSAK 109, 116, 118", ptitle="Konsultan PSAK: Standar Mana yang Berlaku untuk Usaha Anda",
    desc="Konsultan penerapan PSAK di {n}: tentukan dulu SAK EMKM, SAK EP, atau PSAK penuh, lalu PSAK yang terdampak (109, 115, 116, 118, 219). Tanya Ananta, CPA, gratis.",
    sub="Sebelum mencari konsultan PSAK di {n}, pastikan dulu standar akuntansi mana yang wajib dipakai usaha Anda. Banyak perusahaan menengah ternyata cukup memakai SAK EP, bukan PSAK penuh.",
    wa="kami dari {n} perlu konsultan penerapan PSAK.",
    qs=[("Usaha saya pakai SAK apa?", "standar akuntansi apa yang wajib dipakai usaha kami: SAK EMKM, SAK EP, atau PSAK?"),
        ("Persiapan PSAK 118 tahun 2027", "kami perlu persiapan PSAK 118 untuk tahun buku 2027."),
        ("Auditor minta penyesuaian PSAK", "auditor meminta penyesuaian PSAK (misalnya 116 sewa atau 219 imbalan kerja).")],
    secs=lambda n, k: [
        ("Standar Mana yang Berlaku", tbl(["Jenis Entitas", "Standar", "Contoh"], [
            ("Usaha mikro, kecil, dan menengah tanpa akuntabilitas publik", "SAK EMKM", "UMKM, usaha perorangan, CV kecil"),
            ("Entitas tanpa akuntabilitas publik signifikan", "SAK EP", "Sebagian besar PT tertutup, yayasan, rumah sakit swasta"),
            ("Entitas dengan akuntabilitas publik", "PSAK (SAK Indonesia)", "Emiten, bank, asuransi, dana pensiun, BUMN tertentu")])),
        ("PSAK yang Paling Sering Ditanyakan", tbl(["Standar", "Isi Singkat"], [
            (f'<a href="{US}/psak/109/">PSAK 109</a>', "Instrumen keuangan dan cadangan kerugian kredit ekspektasian"),
            (f'<a href="{US}/psak/115/">PSAK 115</a>', "Pendapatan dari kontrak dengan pelanggan"),
            (f'<a href="{US}/psak/116/">PSAK 116</a>', "Sewa: aset hak guna dan liabilitas sewa"),
            (f'<a href="{US}/psak/118/">PSAK 118</a>', "Penyajian laba rugi format baru, wajib mulai tahun buku 2027"),
            (f'<a href="{US}/psak/219/">PSAK 219</a>', "Imbalan kerja dan pesangon")])),
        ("Sebelum Menunjuk Konsultan", f'<p>Minta konsultan menunjukkan analisis dampak dulu (pos apa yang berubah dan berapa besar), baru kebijakan akuntansi dan template perhitungannya. Simulasi PSAK 118 bisa dicoba gratis di <a href="{FA}/cek-psak-118/">Cek PSAK 118</a>. Rincian layanan penerapan ada di <a href="{FA}/konsultan-penerapan-psak/{k["slug"] + "/" if k else ""}">FA Indonesia: Konsultan Penerapan PSAK</a>, dan langkah per standar di <a href="{US}/penerapan-psak/">UpdateSAK</a>.</p>')],
    faq=lambda n: [(f"Ada konsultan PSAK di {n}?", f"Ada. Perusahaan di {n} bisa didampingi daring oleh Ananta, CPA. Tanya dulu lewat WhatsApp, gratis."),
                   ("Apakah PT tertutup wajib PSAK penuh?", "Umumnya tidak. PT tanpa akuntabilitas publik signifikan bisa memakai SAK EP, kecuali diminta bank, investor, atau karena rencana IPO."),
                   ("Kapan PSAK 118 berlaku?", "Untuk tahun buku yang dimulai 1 Januari 2027, dengan angka pembanding tahun 2026 disajikan ulang.")],
    fa="/konsultan-penerapan-psak/")


def build(f, k, base, nearby):
    key = f["key"]; n = k["name"] if k else "Indonesia"
    path = f"/kota/{k['slug']}/{key}/" if k else f"/{key}/"
    h1 = f["h1"].format(n=n) if k else f["ptitle"]
    title = (f["title"].format(n=n) if k else f["ptitle"]) + " | cariakuntan.com"
    if len(title) > 65: title = title.replace(" | cariakuntan.com", "")
    desc = cut(f["desc"].format(n=n) if k else f["desc"].format(n="Indonesia").replace(" di Indonesia", ""))
    sub = f["sub"].format(n=n) if k else f["sub"].format(n="Indonesia").replace(" di Indonesia", "")
    msg = "Halo Pak Ananta, " + (f["wa"].format(n=n) if k else f["wa"].replace("kami dari {n} ", "kami "))
    crumb = (f'<p class="crumb"><a href="/">Beranda</a> / <a href="/kota/">Wilayah</a> / <a href="/kota/{k["slug"]}/">{E(n)}</a></p>' if k
             else f'<p class="crumb"><a href="/">Beranda</a> / <a href="/{key}/">{E(f["label"])}</a></p>')
    label = f'{E(n)}, {E(k["prov"])}' if k else "Seluruh Indonesia"
    secs = "".join(f'<div class="prose"><h2>{E(h)}</h2></div>{b}' if b.startswith("<div class=\"tblwrap\"") else f'<div class="prose"><h2>{E(h)}</h2>{b}</div>' for h, b in f["secs"](n, k))
    faq = f["faq"](n)
    fq = '<div class="prose"><h2>Tanya Jawab</h2>' + "".join(f"<h3>{E(q)}</h3><p>{E(a)}</p>" for q, a in faq) + "</div>"
    ar = ""
    if k and "<!--area-layanan-->" in base:
        i = base.index("<!--area-layanan-->"); j = base.index("<!--/area-layanan-->") + len("<!--/area-layanan-->")
        ar = re.sub(r"<p>Kami melayani .*?</p>", lambda m: f"<p>Pertanyaan soal {E(f['label'].lower())} dari seluruh {E(n)} kami jawab, termasuk kecamatan dan desa/kelurahan berikut. Pertemuan bisa daring atau di lokasi Anda.</p>", base[i:j], count=1, flags=re.S)
        ar = '<div class="prose">' + ar + "</div>"
    if k:
        other = " ".join(f'<a href="/kota/{k["slug"]}/{x}/">{E(FAM[x]["label"])} {E(n)}</a>' for x in FAM if x != key)
        lay = (f'<details class="fold"><summary>Layanan Lain di {E(n)}</summary><div class="citylist">{other} <a href="/kota/{k["slug"]}/kap/">KAP {E(n)}</a> '
               f'<a href="/kota/{k["slug"]}/kja/">KJA {E(n)}</a> <a href="/kota/{k["slug"]}/jasa-laporan-keuangan/">Jasa Laporan Keuangan {E(n)}</a> <a href="/kota/{k["slug"]}/laporan-tahunan-pt/">Laporan Tahunan PT {E(n)}</a></div></details>')
        sek = (f'<details class="fold"><summary>{E(f["label"])} di Kota Sekitar</summary><div class="citylist">'
               + " ".join(f'<a href="/kota/{s}/{key}/">{E(f["label"])} {E(nm)}</a>' for s, nm in nearby) + "</div></details>")
        fa = f'<details class="fold"><summary>Rincian Layanan di FA Indonesia</summary><div class="citylist"><a href="{FA}{f["fa"]}{k["slug"]}/">{E(f["label"])} {E(n)} (FA Indonesia)</a> <a href="{FA}/wilayah/{k["slug"]}/">FA {E(n)}</a></div></details>'
    else:
        rows = "".join(f"<p><b>{E(pv)}:</b> " + " · ".join(f'<a href="/kota/{x["slug"]}/{key}/">{E(x["name"])}</a>' for x in BYPROV[pv]) + "</p>" for pv in sorted(BYPROV))
        lay = f'<div class="prose"><h2>{E(f["label"])} per Kota</h2><details class="fold"><summary>{len(KOTA)} kota</summary>{rows}</details></div>'
        sek = ""; fa = f'<details class="fold"><summary>Rincian Layanan di FA Indonesia</summary><div class="citylist"><a href="{FA}{f["fa"]}">{E(f["label"])} (FA Indonesia)</a></div></details>'
    main = ('<main class="wrap art">\n' + crumb + f'\n<p class="label" style="margin-top:14px">{label}</p>\n'
            f'<h1>{E(h1)}</h1><div class="tshare-top"><div class="share" data-tool="{E(h1)}" data-lab="Bagikan"></div></div>\n<p class="sub">{E(sub)}</p>\n'
            f'<div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(msg)}" rel="noopener" target="_blank">Tanya Ananta, CPA</a><span style="color:var(--muted);font-size:.9rem">Diskusi Awal tanpa Biaya</span></div>'
            + tanya(f["qs"], k) + "\n" + secs + ar + fq + "\n" + lay + "\n" + sek + "\n" + fa + "\n</main>")
    url = D + path
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": h1, "serviceType": f["label"], "areaServed": ({"@type": "City", "name": n} if k else {"@type": "Country", "name": "Indonesia"}),
         "provider": {"@type": "ProfessionalService", "name": "cariakuntan.com", "url": D + "/"}, "url": url, "description": desc},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    head = base[:base.index("<main")]
    T, Dd = E(title), E(desc)
    head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{T}</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description")/>', lambda m: f'<meta content="{Dd}" {m.group(1)}/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:title"/>', lambda m: f'<meta content="{T}" property="og:title"/>', head)
    head = re.sub(r'<link href="[^"]*" rel="canonical"/>', lambda m: f'<link href="{url}" rel="canonical"/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:url"/>', lambda m: f'<meta content="{url}" property="og:url"/>', head)
    head = re.sub(r'<link[^>]*hreflang[^>]*>', "", head)
    lds = re.findall(r'<script type="application/ld\+json">.*?</script>', head, re.S)
    for x in lds: head = head.replace(x, "")
    head = head.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script></head>", 1)
    rest = base[base.index("</main>") + 7:]
    rest = re.sub(r"<!--area-layanan-->.*?<!--/area-layanan-->", "", rest, flags=re.S)  # salinan area di luar main (bila ada)
    wt(P(path), head + main + rest)
    return path


NEW = []
TPLM = rd(P("/kota/malang/kap/"))
for key, f in FAM.items():
    f["key"] = key
    NEW.append(build(f, None, TPLM, []))
    for k in KOTA:
        base = rd(P(f"/kota/{k['slug']}/kap/"))
        m = re.search(r"<summary>KAP di Kota Sekitar</summary><div class=\"citylist\">(.*?)</div>", base, re.S)
        near = re.findall(r'href="/kota/([^/]+)/kap/">KAP ([^<]+)</a>', m.group(1)) if m else []
        NEW.append(build(f, k, base, near))

# pilar SABH CariAkuntan
SABH = dict(key="laporan-keuangan-sabh", label="Laporan Keuangan untuk SABH",
            ptitle="Laporan Keuangan untuk SABH: Cek Kebutuhan dan Template Notaris",
            desc="Cek kebutuhan laporan tahunan PT untuk SABH: wajib audit atau cukup disusun, siapa yang menandatangani, dokumen untuk notaris. Template Word dan Excel gratis.",
            sub="Sejak Permenkum 49/2025, laporan tahunan PT persekutuan modal disetujui RUPS, dituangkan dalam akta notaris, lalu disampaikan lewat SABH. Pertanyaan pertama yang perlu dijawab: laporan keuangan Anda cukup disusun, atau wajib diaudit?",
            wa="kami perlu laporan tahunan PT untuk SABH.",
            qs=[("PT saya wajib audit atau tidak?", "apakah PT kami wajib audit untuk laporan tahunan SABH? Total aset/omzet sekitar: "),
                ("Notaris minta laporan keuangan", "notaris meminta laporan keuangan untuk akta laporan tahunan PT kami."),
                ("Akses SABH diblokir", "akses SABH PT kami diblokir karena laporan tahunan.")],
            secs=lambda n, k: [
                ("Cek Kebutuhan dalam 3 Pertanyaan", tbl(["Pertanyaan", "Jika Ya", "Jika Tidak"], [
                    ("Apakah PT persekutuan modal (didirikan 2 orang atau lebih)?", "Wajib laporan tahunan lewat akta notaris dan SABH", "PT perorangan memakai mekanisme pelaporan yang berbeda"),
                    ("Aset atau omzet paling sedikit Rp50 miliar, menghimpun dana masyarakat, atau terbuka?", "Laporan keuangan wajib diaudit Akuntan Publik (KAP)", "Cukup laporan keuangan yang disusun lengkap dengan CALK"),
                    ("Laporan keuangan dan catatannya sudah ada?", "Siapkan laporan tahunan dan bawa ke notaris", "Susun dulu oleh Akuntan Berpraktik atau KJA")])),
                ("Template Gratis", tbox().replace("<!--ca-kw3t-->", "").replace("<!--/ca-kw3t-->", "") +
                 '<p>Template berisi laporan tahunan sesuai Pasal 16 ayat (6), Surat Pernyataan Direksi, Lembar Penyusun dengan kolom nama dan nomor izin Akuntan Berpraktik atau KJA (diisi penyusun sendiri), laporan keuangan dengan angka ilustrasi, kerangka CALK, checklist dokumen notaris, dan ilustrasi keputusan sirkuler.</p>'),
                ("Siapa yang Menandatangani", '<p>Direksi bertanggung jawab atas laporan keuangan. Penyusun dari luar perusahaan menandatangani Lembar Penyusun: Akuntan Berpraktik atau Kantor Jasa Akuntansi yang izinnya aktif, cek di <a href="/cek-izin/">Cek Izin</a>. Bila wajib audit, yang dilampirkan adalah Laporan Auditor Independen dari Kantor Akuntan Publik.</p>'
                 f'<p>Penjelasan lengkap ada di <a href="{US}/laporan-keuangan-sabh/">UpdateSAK: Laporan Keuangan untuk SABH</a> dan <a href="{FA}/laporan-keuangan-sabh/">FA Indonesia: Panduan dan Template SABH</a>.</p>')],
            faq=lambda n: [("Apakah PT kecil juga wajib lapor lewat SABH?", "Ya, kewajiban Pasal 16 Permenkum 49/2025 tidak bergantung pada ukuran usaha. Yang bergantung ukuran adalah kewajiban audit."),
                           ("Apa akibatnya bila terlambat?", "Teguran lewat SABH, lalu pemblokiran akses bila 30 hari setelah teguran belum dipenuhi. Perubahan pengurus dan peralihan saham ikut tertahan."),
                           ("Apakah template ini bisa langsung dipakai?", "Bisa sebagai format. Nama, angka, dan isi naratifnya diganti dengan data perusahaan Anda, dan bentuk akta mengikuti arahan notaris.")],
            fa="/laporan-keuangan-sabh/")
p = build(SABH, None, TPLM, []); NEW.insert(0, p)
# pilar SABH: daftar per kota diarahkan ke halaman laporan tahunan PT kota yang sudah ada
fp = P(p); t = rd(fp); t = re.sub(r'(/kota/[^/]+/)laporan-keuangan-sabh/', r'\1laporan-tahunan-pt/', t).replace("Laporan Keuangan untuk SABH per Kota", "Laporan Tahunan PT per Kota"); wt(fp, t)

# ---------------- sisipan ----------------
def kw3(k):
    s = k["slug"]
    return ("<!--ca-kw3-->" + " ".join(f'<a href="/kota/{s}/{x}/">{E(FAM[x]["label"])} {E(k["name"])}</a>' for x in FAM) + " <!--/ca-kw3-->")
nx = 0
for k in KOTA:
    for fp in glob.glob(os.path.join(OUT, "kota", k["slug"], "*", "index.html")) + [P(f"/kota/{k['slug']}/")]:
        if any(f"/{x}/" in fp.replace(os.sep, "/") for x in FAM): continue
        t = rd(fp); t2 = re.sub(r"<!--ca-kw3-->.*?<!--/ca-kw3-->", "", t, flags=re.S)
        anchor = f'<summary>Layanan Lain di {k["name"]}</summary><div class="citylist">'
        if anchor in t2: t2 = t2.replace(anchor, anchor + kw3(k), 1)
        elif fp.endswith(os.path.join(k["slug"], "index.html")) and "</main>" in t2:
            blk = f'<details class="fold"><summary>Akuntansi, Audit, dan Rumah Sakit di {E(k["name"])}</summary><div class="citylist">{kw3(k)}</div></details>'
            blk = "<!--ca-kw3h-->" + blk + "<!--/ca-kw3h-->"
            t2 = re.sub(r"<!--ca-kw3h-->.*?<!--/ca-kw3h-->", "", t2, flags=re.S)
            t2 = t2.replace("<!--pk-->", blk + "<!--pk-->", 1) if "<!--pk-->" in t2 else t2.replace("</main>", blk + "</main>", 1)
        if "laporan-tahunan-pt" in fp:
            t2 = re.sub(r"<!--ca-kw3t-->.*?<!--/ca-kw3t-->", "", t2, flags=re.S)
            t2 = t2.replace("<!--/ca-tanya-->", "<!--/ca-tanya-->" + tbox(k), 1)
        nx += wt(fp, t2)
for a in ["permenkum-49-2025-laporan-tahunan-pt-wajib-akta-notaris-sabh", "notaris-butuh-akuntan-laporan-tahunan-pt-sabh", "audit-laporan-tahunan-pt-sabh-jadwal-sanksi", "akses-sabh-diblokir-cara-membuka-laporan-tahunan-pt"]:
    fp = P(f"/artikel/{a}/"); t = rd(fp); t2 = re.sub(r"<!--ca-kw3t-->.*?<!--/ca-kw3t-->", "", t, flags=re.S)
    t2 = t2.replace("<!--/ca-tanya-->", "<!--/ca-tanya-->" + tbox(), 1); nx += wt(fp, t2)

sm = os.path.join(OUT, "sitemap.xml"); t = rd(sm)
t = re.sub(r"<!--cakw3-->.*?<!--/cakw3-->", "", t, flags=re.S)
t = t.replace("</urlset>", "<!--cakw3-->" + "".join(f"<url><loc>{D}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in NEW) + "<!--/cakw3-->\n</urlset>", 1); wt(sm, t)
ll = os.path.join(OUT, "llms.txt"); t = rd(ll)
t = re.sub(r"\n## Kata Kunci Baru 9 Nov 2026\n.*?(?=\n## |\Z)", "", t, flags=re.S)
t = t.rstrip() + ("\n\n## Kata Kunci Baru 9 Nov 2026\n" + "".join(f"- [{FAM[x]['ptitle']}]({D}/{x}/): per kota di /kota/<kota>/{x}/\n" for x in FAM)
                  + f"- [Laporan Keuangan untuk SABH]({D}/laporan-keuangan-sabh/): cek kebutuhan dan template Word/Excel untuk Notaris\n")
wt(ll, t)
print("halaman", len(NEW), "sisipan", nx)
