#!/usr/bin/env python3
"""27 Nov 2026: kotak ajakan untuk pemilik usaha di artikel FA yang paling ramai (WA + email).

Bos: "bantu saya dapat klien atau minimal pemilik perusahaan itu lead WA ke saya atau email."
Data GSC 28 hari (27 Nov): 8 artikel ini membawa ±300 klik per 28 hari, tetapi tombol WA pertama
baru muncul di 17 sampai 93% isi dan tidak ada tombol email. Kotak ini ditaruh tepat sebelum Peta Isi:
satu kalimat sesuai topik artikel + tombol WA (pesan memuat judul artikel) + tombol email.
Tanpa harga, tanpa janji hasil, tanpa kalimat nama Ananta (hanya label tombol baku).
Bekerja di out/faindonesia. Idempoten, --dry. Tambah artikel = tambah entri A.
"""
import os, re, sys
from urllib.parse import quote
ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
WA = "https://wa.me/6282245260121?text="
MAIL = "ananta@faindonesia.co.id"
RS = "Chat Tim Rumah Sakit via WhatsApp"
AN = "Chat Ananta, CPA"

# slug: (kalimat, topik singkat untuk pesan, label tombol WA)
A = {
    "panduan-implementasi-psak-118": (
        "Laporan keuangan 2027 perusahaan Anda perlu mengikuti PSAK 118? Tim FA Indonesia membantu memetakan akun, menyusun format laba rugi baru, dan menyajikan ulang angka pembandingnya.",
        "penerapan PSAK 118", AN),
    "daftar-psak-isak-2026-2027": (
        "Belum yakin PSAK mana yang berdampak ke laporan keuangan perusahaan Anda? Kirim laporan keuangan terakhir, tim FA Indonesia memetakan standar yang relevan dan apa saja yang perlu disesuaikan.",
        "PSAK yang berdampak ke laporan keuangan kami", AN),
    "syarat-direktur-rumah-sakit-permenkes-6-2026": (
        "Sedang menata direksi atau menyiapkan rumah sakit untuk bank dan investor? Tim rumah sakit FA Indonesia mendampingi keuangan, unit cost, dan tata kelola rumah sakit swasta.",
        "direksi dan pendampingan rumah sakit", RS),
    "kapan-perusahaan-wajib-diaudit": (
        "Perusahaan Anda diminta laporan audited oleh bank, panitia tender, atau notaris dan waktunya mepet? Sampaikan keperluan dan tenggatnya, tim FA Indonesia menyiapkan datanya sampai diaudit KAP terdaftar OJK.",
        "kebutuhan audit laporan keuangan", AN),
    "laporan-keuangan-rumah-sakit-swasta-sesuai-psak": (
        "Laporan keuangan rumah sakit Anda diminta bank, yayasan, atau calon investor? Tim rumah sakit FA Indonesia menyusun dan merapikannya sesuai PSAK sampai siap diaudit.",
        "laporan keuangan rumah sakit", RS),
    "menyusun-laporan-keuangan-dari-rekening-koran": (
        "Pembukuan belum ada, tetapi laporan keuangan sudah diminta bank atau untuk lapor SABH? Cukup siapkan rekening koran; laporan keuangannya disusun KJA Farhani K.N. melalui FA Indonesia.",
        "penyusunan laporan keuangan dari rekening koran", AN),
    "sak-emkm-vs-sak-ep": (
        "Masih ragu perusahaan Anda memakai SAK EMKM atau SAK EP? Sampaikan omzet dan keperluan laporannya, tim FA Indonesia membantu menentukan dan menyusun laporan keuangannya.",
        "pilihan SAK EMKM atau SAK EP", AN),
    "menghitung-tarif-layanan-klinik-dan-rumah-sakit": (
        "Ingin unit cost dan tarif dihitung dari data klinik atau rumah sakit Anda sendiri? Tim rumah sakit FA Indonesia menghitungnya dari data SIMRS dan laporan keuangan Anda.",
        "perhitungan unit cost dan tarif", RS),
}
CSS = ('<style id="fa-lead27-css">.fa-lead27{margin:18px 0 22px;padding:16px 18px;border:1px solid rgba(233,185,73,.55);border-radius:10px;background:rgba(233,185,73,.07)}'
       ".fa-lead27 p{margin:0 0 12px;font-size:.98em;line-height:1.55}.fa-lead27 .r{display:flex;flex-wrap:wrap;gap:10px}</style>")


def blok(slug):
    kal, topik, label = A[slug]
    pesan = "Halo Pak Ananta, saya baca artikel di faindonesia.co.id tentang %s. Saya pemilik/pengurus perusahaan, mau tanya: " % topik
    subj = "Tanya %s (dari artikel faindonesia.co.id)" % topik
    body = "Nama dan perusahaan:\nKeperluan:\nTenggat:\n"
    return ('<!--fa-lead27--><aside class="fa-lead27" aria-label="Tanya Tim FA Indonesia"><p>%s</p><div class="r">'
            '<a class="btn solid" href="%s" target="_blank" rel="noopener" data-lead27="wa">%s</a>'
            '<a class="btn line" href="mailto:%s?subject=%s&amp;body=%s" data-lead27="email">Kirim Email</a></div></aside><!--/fa-lead27-->'
            % (kal, WA + quote(pesan, safe="/"), label, MAIL, quote(subj), quote(body)))


n = 0
for slug in A:
    f = os.path.join(ROOT, "out", "faindonesia", "artikel", slug, "index.html")
    s = open(f, encoding="utf-8").read()
    s2 = re.sub(r"<!--fa-lead27-->.*?<!--/fa-lead27-->", "", s, flags=re.S)
    assert s2.count('<nav aria-label="Peta Isi"') == 1, slug
    s2 = s2.replace('<nav aria-label="Peta Isi"', blok(slug) + '<nav aria-label="Peta Isi"', 1)
    if 'id="fa-lead27-css"' not in s2:
        s2 = s2.replace("</head>", CSS + "</head>", 1)
    if s2 != s:
        n += 1
        if not DRY:
            open(f, "w", encoding="utf-8").write(s2)
print("artikel berubah:", n, "(dry)" if DRY else "")
