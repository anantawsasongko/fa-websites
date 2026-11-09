# -*- coding: utf-8 -*-
"""Push SEO "jasa audit" (2 Nov 2026, lead PT Gpms Sukabumi via /wilayah/sukabumi/: audit untuk laporan tahunan SABH).
- /jasa-audit-laporan-keuangan/ : halaman layanan utama (audit lewat KAP mitra berizin, biaya wajar, tahun pertama, ganti KAP, SABH)
- Semua /wilayah/<kota>/ : title dan description memuat "Jasa Audit", seksi "Jasa Audit Laporan Keuangan di <Kota>", item layanan ditautkan ke halaman audit
- Semua /wilayah/<kota>/<kawasan>/ : tautan ke halaman audit di seksi Persiapan Audit KAP
- Kotak CTA di artikel audit FA, /laporan-tahunan-pt/, /laporan-keuangan-umkm/, /jasa-penyusunan-laporan-keuangan/, /kap-dhn/; blok /layanan/; sitemap; llms.txt
Idempoten (penanda fa-audit). Jalankan setelah fa_dhn_20261101.py, sebelum kja_kota_20261101.py."""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-02"')
exec(compile(_src, "fa_lead_helpers", "exec"))

PA = "/jasa-audit-laporan-keuangan/"
pa_body = (
 "<h2>Kapan Perusahaan Butuh Audit</h2><ul>"
 "<li><b>Wajib menurut UU PT Pasal 68:</b> aset atau peredaran usaha minimal Rp50 miliar, menghimpun dana masyarakat, perseroan terbuka, atau diwajibkan peraturan lain.</li>"
 "<li><b>Laporan tahunan PT di SABH:</b> PT wajib audit menyertakan laporan audited saat persetujuan RUPS dibawa ke notaris (Permenkum 49/2025). Teguran tertulis dijadwalkan 1 sampai 31 Desember 2026 dan blokir akses SABH mulai 2 Januari 2027.</li>"
 "<li><b>Kredit bank:</b> bank meminta laporan audited dari KAP yang masuk daftar rekanannya.</li>"
 "<li><b>Investor, akuisisi, tender, dan IPO:</b> laporan audited menjadi syarat masuk.</li></ul>"
 "<h2>Audit Hemat, Bukan Audit Asal</h2>"
 "<p>Biaya audit ditentukan jam kerja tim auditor. Jam itu yang bisa kami tekan secara sah: pembukuan dirapikan, rekonsiliasi diselesaikan, dan dokumen disiapkan sebelum auditor datang. Yang tidak kami lakukan: menjanjikan opini tertentu, memangkas prosedur, atau menerbitkan laporan tanpa pemeriksaan. Laporan seperti itu berisiko ditolak bank dan notaris.</p>"
 + tbl(["Kondisi Perusahaan", "Yang Kami Kerjakan", "Dampaknya"], [
   ("Pembukuan belum rapi atau tertinggal", "Penyusunan ulang buku besar dan laporan keuangan oleh tim yang terpisah dari tim audit KAP", "Auditor tidak bekerja dua kali, biaya audit lebih wajar"),
   ("Belum pernah diaudit", "Bukti saldo awal: rekening koran, persediaan, aset tetap, ekuitas", "Audit tahun pertama tidak molor"),
   ("Laporan dari KAP lama tidak terbit", "Pemetaan penyebab, peralihan ke KAP baru, audit tahun yang benar-benar diminta", "Tidak membayar audit tahun yang tidak dibutuhkan"),
   ("Tenggat notaris atau bank dekat", "Jadwal kerja lapangan dan draf laporan disepakati tertulis di depan", "Tanggal laporan terbit lebih pasti"),
   ("Lokasi di luar kota besar", "Pengujian dokumen daring, kunjungan lapangan hanya untuk observasi", "Biaya perjalanan ditekan"),
 ])
 + "<h2>Alur Kerja</h2>" + flow([
   ("Diskusi awal", "Gratis. Tujuan audit, tahun buku, ukuran usaha, lokasi, dan tenggat."),
   ("Cek kesiapan", "Neraca saldo dan laporan keuangan dibaca untuk melihat celah sebelum auditor masuk."),
   ("Penawaran KAP", "Surat penawaran dari KAP berizin dengan ruang lingkup, jadwal, dan biaya tertulis."),
   ("Kerja lapangan", "Dokumen disiapkan, observasi persediaan dan aset, konfirmasi saldo."),
   ("Laporan terbit", "Pembahasan koreksi, surat representasi, laporan auditor independen siap dibawa ke notaris atau bank.")])
 + "<h2>KAP Mitra dan Pilihan Lain</h2>"
 "<p>Audit dilaksanakan oleh <a href=\"/kap-dhn/\">KAP mitra FA yang terdaftar OJK</a>, sehingga dapat dipakai untuk kebutuhan bank dan sektor jasa keuangan. Bila bank Anda mensyaratkan KAP dari daftar tertentu, kami bantu mencarikan kantor yang sesuai lewat <a href=\"https://cariakuntan.com/artikel/jasa-audit-laporan-keuangan-cara-memilih-kap/\">CariAkuntan</a>. Bila pembaca laporan tidak mensyaratkan audit, kami sarankan jasa yang lebih ringan: <a href=\"/jasa-penyusunan-laporan-keuangan/\">penyusunan laporan keuangan</a>, kompilasi, atau prosedur yang disepakati.</p>"
 "<h2>Industri yang Sering Kami Dampingi</h2>"
 "<p>Peternakan dan agribisnis (aset biologis, kemitraan plasma, observasi kandang), konstruksi, distribusi dan importir, rumah sakit dan klinik, hotel, manufaktur, yayasan, serta perusahaan PMA dengan pelaporan ke induk.</p>"
 "<h2>Data Awal untuk Perkiraan Biaya</h2><ul>"
 "<li>Laporan keuangan atau neraca saldo tahun buku yang akan diaudit.</li>"
 "<li>Laporan audit tahun lalu, bila ada.</li>"
 "<li>Jumlah lokasi, gudang, atau kandang.</li>"
 "<li>Untuk apa laporan dipakai dan kapan tenggatnya.</li></ul>"
 "<h2>Bacaan Terkait</h2><ul>"
 "<li><a href=\"/artikel/kapan-perusahaan-wajib-diaudit/\">Kapan Perusahaan Wajib Diaudit</a></li>"
 "<li><a href=\"/artikel/biaya-audit-kap-faktor-penentu/\">Biaya Audit KAP dan Faktor Penentunya</a></li>"
 "<li><a href=\"/artikel/persiapan-audit-pertama-kali-saldo-awal/\">Persiapan Audit Pertama Kali dan Saldo Awal</a></li>"
 "<li><a href=\"/artikel/kompilasi-review-audit/\">Kompilasi, Reviu, atau Audit</a></li>"
 "<li><a href=\"/laporan-tahunan-pt/\">Jasa Laporan Tahunan PT untuk SABH</a></li></ul>")
PA_FAQ = [
 ("Berapa biaya jasa audit laporan keuangan?", "Bergantung pada ukuran aset dan omzet, jumlah lokasi, kerapian pembukuan, audit tahun pertama atau bukan, dan tenggat. Kirim laporan keuangan atau neraca saldo, perkiraan biaya disampaikan setelah diskusi awal dan tertulis di surat penawaran."),
 ("Bagaimana cara mendapatkan biaya audit yang murah tapi tetap sah?", "Rapikan pembukuan dan siapkan dokumen sebelum auditor datang, pilih ruang lingkup sesuai kebutuhan pembaca laporan, dan bandingkan penawaran KAP berizin. Hindari pihak yang menjanjikan opini atau laporan tanpa pemeriksaan."),
 ("Berapa lama proses audit?", "Untuk perusahaan dengan pembukuan rapi umumnya 4 sampai 6 minggu sejak dokumen lengkap. Audit tahun pertama atau beberapa tahun sekaligus memerlukan waktu tambahan."),
 ("Apakah bisa dijamin opini Wajar Tanpa Pengecualian?", "Tidak ada yang boleh menjamin opini sebelum pemeriksaan. Yang bisa kami lakukan adalah menyiapkan laporan keuangan dan bukti agar risiko pengecualian dapat ditekan sejak awal."),
 ("Laporan audit dari KAP lama tidak terbit, bisa pindah?", "Bisa. KAP baru akan berkomunikasi dengan auditor pendahulu sesuai kode etik, lalu mengaudit tahun yang memang diminta, dengan pengujian saldo awal bila diperlukan."),
 ("Apakah PT yang tidak wajib audit tetap perlu laporan untuk SABH?", "Ya. Semua PT persekutuan modal menyampaikan laporan tahunan, tetapi laporan keuangannya tidak harus diaudit bila di bawah kriteria Pasal 68 UU PT."),
 ("Apakah melayani perusahaan di luar Jawa?", "Ya. Pengujian dokumen dilakukan daring, kunjungan lapangan dijadwalkan untuk observasi persediaan dan aset."),
]
svc_page(PA, "Layanan · Audit", "Jasa Audit Laporan Keuangan oleh KAP Terdaftar OJK untuk Bank, SABH, dan Investor",
  "Audit untuk laporan tahunan PT di SABH, kredit bank, investor, atau tender. Kami siapkan pembukuan dan dokumennya, lalu audit dilaksanakan KAP mitra yang terdaftar OJK. Termasuk audit tahun pertama, ganti KAP, dan audit beberapa tahun sekaligus. Seluruh Indonesia.",
  pa_body, PA_FAQ, "Jasa Audit Laporan Keuangan oleh KAP Terdaftar OJK | FA Indonesia",
  "Jasa audit laporan keuangan lewat KAP mitra terdaftar OJK: untuk SABH, bank, investor, tender. Audit tahun pertama, ganti KAP, biaya wajar tanpa memangkas prosedur. Diskusi awal gratis.",
  "Jasa Audit Laporan Keuangan", "Financial statement audit coordination",
  "/kap-dhn/", "KAP Mitra FA", "Halo FA Indonesia, kami perlu jasa audit laporan keuangan.", "Jasa Audit")
URLS = [PA]

# ---------- kotak CTA di halaman terkait ----------
def box(title, text):
    return (f'<!--fa-audit--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
            f'<p style="margin:0 0 6px;font-weight:600">{E(title)}</p><p style="margin:0 0 12px">{E(text)}</p>'
            f'<a class="btn solid" href="{PA}">Jasa Audit Laporan Keuangan</a></div><!--/fa-audit-->')
B1 = box("Perlu Laporan Audited?", "Audit lewat KAP mitra terdaftar OJK, dokumen disiapkan lebih dulu supaya biaya wajar dan laporan terbit sesuai tenggat.")
B2 = box("PT Anda Wajib Audit?", "Bila aset atau omzet minimal Rp50 miliar, laporan tahunan untuk SABH perlu laporan audited. Kami siapkan sampai laporan auditor terbit.")
targets = [(("laporan-tahunan-pt",), B2), (("laporan-keuangan-umkm",), B1), (("jasa-penyusunan-laporan-keuangan",), B1), (("kap-dhn",), B1)]
targets += [(("artikel", s), B1) for s in ("apakah-perusahaan-butuh-audit-kap", "audit-rumah-sakit-pertama-kali", "biaya-audit-kap-faktor-penentu",
            "jenis-opini-audit-dan-dampaknya-ke-bank", "kapan-perusahaan-wajib-diaudit", "kompilasi-review-audit", "persiapan-audit-pertama-kali-saldo-awal")]
nb = 0
for parts, b in targets:
    p = P(*parts, "index.html")
    if not os.path.exists(p): print("skip", p); continue
    t = re.sub(r"<!--fa-audit-->.*?<!--/fa-audit-->", "", rd(p), flags=re.S)
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("<h2>Pertanyaan Umum</h2>")
    if k < 0: k = t.find("</main>")
    wtxt(p, t[:k] + b + t[k:]); nb += 1

# ---------- /layanan/ ----------
lp = P("layanan", "index.html")
t = re.sub(r"<!--fa-audit-svc-->.*?<!--/fa-audit-svc-->", "", rd(lp), flags=re.S)
blk = ('<!--fa-audit-svc--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Audit</p><h2>Jasa Audit Laporan Keuangan</h2></div>'
       '<p class="t" style="max-width:62em">Untuk laporan tahunan PT di SABH, kredit bank, investor, dan tender. KAP mitra terdaftar OJK, biaya wajar, dokumen disiapkan lebih dulu.</p>'
       '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn solid" href="/jasa-audit-laporan-keuangan/">Jasa Audit Laporan Keuangan</a></div></div></section><!--/fa-audit-svc-->')
i = t.find('<section class="block'); wtxt(lp, t[:i] + blk + t[i:])

# ---------- wilayah ----------
nc = nk = 0
for p in sorted(glob.glob(P("wilayah", "*", "index.html"))):
    t = re.sub(r"<!--fa-audit-w-->.*?<!--/fa-audit-w-->", "", rd(p), flags=re.S)
    m = re.search(r"<title>FA ([^:<]+): Financial Advisor, KAP dan KJA Mitra \| FA Indonesia</title>", t) or re.search(r"<title>FA ([^:<]+): Jasa Audit", t)
    if not m: continue
    city = m.group(1)
    title = f"FA {city}: Jasa Audit Laporan Keuangan, KAP Mitra, dan Financial Advisor | FA Indonesia"
    t = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", t, count=1, flags=re.S)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', t, count=1)
    desc = f"Jasa audit laporan keuangan di {city} lewat KAP mitra terdaftar OJK: untuk SABH, kredit bank, investor. Laporan keuangan, kredit, IPO. Diskusi awal gratis."
    for a in ['name="description"', 'property="og:description"']:
        t = re.sub(rf'<meta {a} content="[^"]*">', f'<meta {a} content="{E(desc)}">', t, count=1)
    t = re.sub(r'(<h1[^>]*>)FA ([^:<]+): Financial Advisor dan Konsultan Keuangan di ([^<]+)</h1>', r'\1FA \2: Jasa Audit, Laporan Keuangan, dan Financial Advisor di \3</h1>', t, count=1)
    t = t.replace('<h3><a href="/jasa-penyusunan-laporan-keuangan/">Persiapan audit KAP</a></h3>', f'<h3><a href="{PA}">Jasa audit laporan keuangan</a></h3>', 1)
    sec = (f'<!--fa-audit-w--><h2>Jasa Audit Laporan Keuangan di {E(city)}</h2>'
           f'<p>Perusahaan di {E(city)} yang perlu laporan audited untuk laporan tahunan PT di SABH, kredit bank, investor, atau tender kami dampingi dari kesiapan pembukuan sampai laporan auditor terbit. Audit dilaksanakan KAP mitra terdaftar OJK; dokumen diuji daring dan tim datang untuk observasi persediaan dan aset.</p>'
           '<ul><li>Audit tahun pertama dan pengujian saldo awal</li><li>Pindah KAP bila laporan dari auditor lama tidak terbit</li><li>Biaya wajar karena dokumen disiapkan lebih dulu, tanpa memangkas prosedur</li></ul>'
           f'<p><a class="btn line" href="{PA}">Lihat Jasa Audit</a></p><!--/fa-audit-w-->')
    k = t.find("<h2>Layanan di ")
    if k < 0: continue
    wtxt(p, t[:k] + sec + t[k:]); nc += 1
for p in sorted(glob.glob(P("wilayah", "*", "*", "index.html"))):
    t = re.sub(r"<!--fa-audit-w-->.*?<!--/fa-audit-w-->", "", rd(p), flags=re.S)
    m = re.search(r"<h2>Persiapan Audit KAP di [^<]*</h2>.*?</p>", t, re.S)
    if not m: continue
    add = f'<!--fa-audit-w--><p>Butuh laporan audited untuk SABH, bank, atau investor? Lihat <a href="{PA}">jasa audit laporan keuangan</a> bersama KAP mitra terdaftar OJK.</p><!--/fa-audit-w-->'
    wtxt(p, t[:m.end()] + add + t[m.end():]); nk += 1

# ---------- sitemap & llms ----------
sm = re.sub(r"<!--fa-audit-->.*?<!--/fa-audit-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-audit-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.9</priority></url>\n" for u in URLS) + "<!--/fa-audit-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = rd(P("llms.txt"))
line = "- Jasa audit laporan keuangan lewat KAP mitra terdaftar OJK: laporan tahunan PT (SABH), kredit bank, investor, audit tahun pertama, ganti KAP → https://faindonesia.co.id/jasa-audit-laporan-keuangan/\n"
ll = ll.replace(line, "")
ll = ll.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + line, 1) if "\n## Layanan Spesifik\n" in ll else ll.rstrip("\n") + "\n\n## Layanan Spesifik\n" + line
wtxt(P("llms.txt"), ll)
print("fa_audit ok", URLS, "boxes", nb, "kota", nc, "kawasan", nk)
