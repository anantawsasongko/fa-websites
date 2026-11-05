# -*- coding: utf-8 -*-
"""Pembelian aktif (6 Nov 2026). Midtrans dipasang lagi di /bayar/ (Paket AI, layanan custom).
E-book dan FA Jupiter tetap lewat toko Mayar. Modul ini menyamakan link Mayar dan copy e-book.
Modul penundaan lama (1 Nov 2026) sudah dilepas.
- Tombol beli (href /bayar/?produk=...) jadi label nonaktif "Segera Dibuka".
- Link footer "Pembayaran" dihapus. Link /bayar/ lain jadi teks biasa.
- QRIS hanya untuk donasi (donasi.js, tidak disentuh).
Halaman /bayar/ asli (Snap + invoice) disimpan di backup/pembayaran-20261101/ untuk dipulihkan saat Midtrans aktif:
cukup kembalikan file itu dan hapus pemanggilan modul ini di prep.py."""
import os, re
# 4 Nov 2026: toko Mayar aktif (fa-indonesia-14404.myr.id). Produk di bawah ini langsung dijual lewat link Mayar
# (tombol "Beli ..." tetap aktif, buka tab baru). Produk lain (Paket AI, custom) masih "Segera Dibuka" sampai Midtrans aktif.
MAYAR_BASE = "https://fa-indonesia-14404.myr.id/pl/"
MAYAR = {
    "eb-psp":     "e-book-prosedur-audit-substantif-primer",
    "eb-auditee": "e-book-audit-untuk-auditee-umkm",
    "eb-lkumkm":  "e-book-menyusun-laporan-keuangan-umkm",
    "eb-akmen":   "e-book-akuntansi-manajemen-untuk-umkm",
    "eb-iso":     "e-book-panduan-iso-22000-sistem-manajemen-keamanan-pangan",
    "eb-makacua": "e-book-social-responsibility-dalam-budaya-makacua-nelayan-bugis",
    "eb-paket":   "paket-hemat-6-e-book-penerbit-fa",
    "ar-day":     "fa-jupiter-audit-ready-day-pass-1-hari",
    "ar-year":    "fa-jupiter-audit-ready-tahunan-1-tahun",
}
def mayar_url(pid): return MAYAR_BASE + MAYAR[pid] if pid in MAYAR else None
TEXT = [
    ("Pembayaran online lewat Midtrans segera dibuka.", "Pembayaran online lewat QRIS, virtual account, dan e-wallet."),
    ("pembayaran online lewat Midtrans (segera dibuka).", "pembayaran online lewat QRIS, virtual account, dan e-wallet."),
    ("pembayaran online segera dibuka", "pembayaran online lewat QRIS, virtual account, dan e-wallet"),
    ("Baca sampel gratis dulu. Pembelian online segera dibuka.", "Baca sampel gratis dulu, lalu beli dan unduh PDF-nya saat itu juga."),
    ("<li>Pembelian online lewat payment gateway resmi segera dibuka.</li><li>Setelah dibuka: klik <b>Beli</b>, bayar online, lalu file PDF dan password dikirim ke email Anda.</li>", "<li>Klik <b>Beli</b>, bayar online lewat QRIS, virtual account, atau e-wallet.</li><li>Setelah lunas, file PDF langsung bisa diunduh dan link unduhannya dikirim ke email Anda.</li>"),
    ("Baca sampel gratis, PDF dikirim dengan password setelah pembayaran online.", "Baca sampel gratis, PDF langsung bisa diunduh setelah pembayaran online."),
    ("File PDF dan password dikirim ke email atau WhatsApp Anda setelah pembayaran online berhasil, biasanya di hari yang sama pada jam kerja.", "File PDF langsung bisa diunduh setelah pembayaran online berhasil; link unduhannya juga dikirim ke email Anda."),
    ("File PDF e-book dan password dikirim ke email setelah pembayaran online berhasil, biasanya di hari yang sama pada jam kerja.", "File PDF e-book langsung bisa diunduh setelah pembayaran online berhasil; link unduhannya juga dikirim ke email."),
    ("E-book yang password-nya sudah dikirim tidak dapat di-refund", "E-book yang file-nya sudah diunduh tidak dapat di-refund"),
    ("E-book yang file dan password-nya sudah dikirim tidak dapat di-refund.", "E-book yang file-nya sudah diunduh tidak dapat di-refund."),
    ("File dan password hanya untuk pembeli.", "File hanya untuk pembeli."),
    ('<details><summary>Kenapa PDF memakai password?</summary><p>Supaya e-book hanya dibaca pembeli. Password membuka file untuk dibaca dan dicetak; menyalin teks dan mengubah isi dikunci. Mohon tidak membagikan file dan password.</p></details>', '<details><summary>Bagaimana cara mengunduh e-book?</summary><p>Setelah pembayaran berhasil, tombol unduh tampil di halaman pembayaran dan link-nya dikirim ke email Anda. File PDF bisa dibuka di HP, tablet, dan laptop. Mohon tidak membagikan file ke pihak lain.</p></details>'),
    ('{"@type": "Question", "name": "Kenapa PDF memakai password?", "acceptedAnswer": {"@type": "Answer", "text": "Supaya e-book hanya dibaca pembeli. Password membuka file untuk dibaca dan dicetak; menyalin teks dan mengubah isi dikunci. Mohon tidak membagikan file dan password."}}', '{"@type": "Question", "name": "Bagaimana cara mengunduh e-book?", "acceptedAnswer": {"@type": "Answer", "text": "Setelah pembayaran berhasil, tombol unduh tampil di halaman pembayaran dan link-nya dikirim ke email Anda. File PDF bisa dibuka di HP, tablet, dan laptop. Mohon tidak membagikan file ke pihak lain."}}'),
    ('"availability": "https://schema.org/PreOrder"', '"availability": "https://schema.org/InStock"'),
]

BUY = re.compile(r'<a\b([^>]*?)href="(?:https://faindonesia\.co\.id)?/bayar/\?[^"]*"([^>]*)>(.*?)</a>', re.S)
PID = re.compile(r'/bayar/\?produk=([a-z0-9-]+)')
def _buy(m):
    pm = PID.search(m.group(0))
    u = mayar_url(pm.group(1)) if pm else None
    if not u: return m.group(0)  # Paket AI dan layanan custom tetap ke /bayar/ (Midtrans)
    attrs = m.group(1) + m.group(2); inner = m.group(3)
    extra = re.sub(r'\s*href="[^"]*"', "", attrs).strip()
    return f'<a {extra} href="{u}" target="_blank" rel="noopener">{inner}</a>'
def run(OUT):
    n = 0
    for site in os.listdir(OUT):
        root = os.path.join(OUT, site)
        if not os.path.isdir(root): continue
        for d, _, fs in os.walk(root):
            rel = os.path.relpath(d, root).replace(os.sep, "/")
            if rel.startswith("bayar") or rel.startswith("toko/uji"): continue
            for f in fs:
                if not f.endswith(".html"): continue
                p = os.path.join(d, f); t = open(p, encoding="utf-8").read()
                t0 = t
                t = t.replace('/js/fa-paywall.js"', '/js/fa-paywall.js?v=20261106"').replace('/js/fa-ai.js"', '/js/fa-ai.js?v=20261106"')
                for a, b in TEXT: t = t.replace(a, b)
                if "/bayar/" in t:
                    t = re.sub(r'"url": "https://faindonesia\.co\.id/bayar/\?produk=([a-z0-9-]+)"', lambda mm: '"url": "' + (mayar_url(mm.group(1)) or mm.group(0)[8:-1]) + '"', t)
                    t = BUY.sub(_buy, t)
                if t != t0:
                    open(p, "w", encoding="utf-8").write(t); n += 1
    return n
