# -*- coding: utf-8 -*-
"""Halaman layanan berbasis lead nyata (26 Okt 2026):
- /jasa-implementasi-psak-118/ (lead: implementasi PSAK 118, perusahaan sistem pembayaran)
- /konsultan-kredit-distributor-importir/ (lead: distributor/importir ingin memaksimalkan plafon kredit)
Plus kotak CTA di artikel terkait, blok di /layanan/, footer, sitemap, llms.txt.
Idempoten: halaman ditimpa, sisipan memakai penanda komentar fa-lead.
Jalankan setelah fa_seo_20261025.py, sebelum prep.py.
"""
import os, re, json, html
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
D = "https://faindonesia.co.id"
WA = "https://wa.me/6282245260121?text="
TODAY = "2026-10-26"
E = html.escape
def P(*a): return os.path.join(FA, *a)
def rd(p): return open(p, encoding="utf-8").read()
def wtxt(p, s): open(p, "w", encoding="utf-8").write(s)
def wa(msg): return WA + quote(msg)

TPL_SVC = rd(P("konsultan-kredit-bank", "index.html"))
TPL_ART = rd(P("artikel", "checklist-persiapan-ipo", "index.html"))
AUTHOR_BOX = re.search(r'<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333.*?</div></div>', TPL_ART, re.S).group(0)
PROVIDER = {"@type": "ProfessionalService", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"}
CSS = ('<style id="fa-lead">.tblwrap{overflow-x:auto;margin:8px 0 22px;-webkit-overflow-scrolling:touch}.tblwrap table{min-width:560px;margin:0}'
       '.art th,.art td{border:1px solid #333;padding:9px 10px;text-align:left;vertical-align:top}'
       '.flow5{list-style:none;padding:0;margin:10px 0 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;counter-reset:f}'
       '.flow5 li{border:1px solid #333;border-radius:10px;padding:14px 14px 14px 52px;position:relative;background:#1e1e1e;font-family:Poppins,sans-serif!important;font-size:14px!important;line-height:1.5!important}'
       '.flow5 li:before{counter-increment:f;content:counter(f);position:absolute;left:14px;top:13px;width:26px;height:26px;border-radius:50%;background:#fff;color:#171717;display:grid;place-items:center;font-size:12px;font-weight:600}'
       '.flow5 li b{display:block;font-weight:500;margin-bottom:2px}</style>')

def set_head(s, title, desc, url, ld):
    s = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', s, count=1)
    for a in ['name="description"', 'property="og:description"']:
        s = re.sub(rf'<meta {a} content="[^"]*">', f'<meta {a} content="{E(desc)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", s, count=1, flags=re.S)
    return s.replace("</head>", CSS + "</head>", 1)

def set_main(s, inner):
    i = s.find('<main id="top">'); j = s.find("</main>")
    return s[:i] + '<main id="top">\n' + inner + "\n" + s[j:]

def flow(items): return '<ol class="flow5">' + "".join(f"<li><b>{E(t)}</b>{E(d)}</li>" for t, d in items) + "</ol>"
def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
def faq_html(faq): return "".join(f'<p style="margin:0 0 18px"><b>{E(q)}</b><br>{E(a)}</p>' for q, a in faq)
def faq_ld(faq): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def crumbs(items): return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def svc_page(path, eyebrow, h1, lead, body, faq, title, desc, svc_name, svc_type, cta_href, cta_label, wa_msg, crumb_name):
    url = D + path
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": svc_name, "serviceType": svc_type, "provider": PROVIDER, "areaServed": {"@type": "Country", "name": "Indonesia"}, "url": url},
        faq_ld(faq), crumbs([("FA Indonesia", D + "/"), ("Layanan", D + "/layanan/"), (crumb_name, url)])]}
    main = (f'<section class="block">\n<div class="wrap art">\n<p class="eyebrow">{eyebrow}</p>\n'
            f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{E(h1)}</h1>\n'
            f'<p class="t" style="max-width:62em">{lead}</p>\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px"><a class="btn solid" href="{wa(wa_msg)}" rel="noopener" target="_blank">Chat Ananta, CPA</a><a class="btn line" href="{cta_href}">{cta_label}</a></div>\n'
            f'{body}\n<h2>Pertanyaan Umum</h2>\n{faq_html(faq)}\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px"><a class="btn solid" href="{wa(wa_msg)}" rel="noopener" target="_blank">Chat Ananta, CPA</a></div>\n'
            f'{AUTHOR_BOX}\n</div>\n</section>')
    p = P(*path.strip("/").split("/"), "index.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
    wtxt(p, set_main(set_head(TPL_SVC, title, desc, url, ld), main))

# ================= 1. JASA IMPLEMENTASI PSAK 118 =================
P118 = "/jasa-implementasi-psak-118/"
p118_body = (
 "<h2>Kenapa Harus Mulai Sekarang</h2>"
 "<p>PSAK 118 Penyajian dan Pengungkapan dalam Laporan Keuangan berlaku 1 Januari 2027 dan menggantikan PSAK 201. Penerapannya retrospektif, jadi angka 2026 ikut disajikan ulang sebagai komparatif. Data yang Anda catat tahun ini sudah menjadi data transisi. Laba bersih tidak berubah, tetapi susunan laba rugi, subtotal wajib, pengungkapan ukuran kinerja manajemen (MPM), dan klasifikasi arus kas berubah. Dampaknya sampai ke covenant bank, materi investor, dan KPI direksi.</p>"
 "<h2>Ruang Lingkup Pendampingan</h2>"
 + tbl(["Tahap", "Yang Dikerjakan", "Hasil"], [
   ("Gap assessment", "Membaca laporan keuangan 2025, bagan akun, kebijakan akuntansi, dan materi investor/bank", "Daftar perubahan dan prioritas per pos"),
   ("Mapping kategori", "Memetakan setiap akun ke Operasi, Investasi, Pendanaan, Pajak, Operasi Dihentikan, termasuk selisih kurs dan bagian laba asosiasi", "Matriks mapping akun ke kategori PSAK 118"),
   ("Aktivitas bisnis utama", "Menilai apakah entitas punya aktivitas utama investasi atau pemberian pembiayaan kepada pelanggan (relevan untuk fintech, sistem pembayaran, pembiayaan, grup holding)", "Memo kebijakan akuntansi"),
   ("MPM dan agregasi", "Mengidentifikasi EBITDA disesuaikan atau laba normalisasi yang dipakai di luar laporan keuangan, menyusun rekonsiliasi dan efek pajaknya, merapikan pos lain-lain", "Draf catatan MPM dan disagregasi"),
   ("Laporan proforma", "Menyajikan ulang laba rugi dan arus kas 2026 dalam format baru", "Laporan proforma plus rekonsiliasi transisi"),
   ("Sistem dan covenant", "Penyesuaian bagan akun dan template pelaporan, simulasi dampak ke rasio dan covenant", "Template pelaporan bulanan dan catatan untuk bank"),
   ("Koordinasi auditor", "Menyiapkan memo dan bukti pendukung agar diskusi dengan KAP efisien", "Paket diskusi auditor"),
 ])
 + "<h2>Alur Kerja</h2>" + flow([("Diskusi awal", "Gratis, 30 sampai 45 menit lewat video call."), ("NDA", "Data laporan keuangan dan bagan akun dikirim setelah NDA."), ("Diagnosis", "Gap assessment dan rencana kerja tertulis."), ("Implementasi", "Mapping, kebijakan, proforma, template."), ("Siap audit", "Paket transisi diserahkan ke tim keuangan dan auditor.")])
 + "<h2>Siapa yang Cocok</h2><ul>"
   "<li>Perusahaan yang diaudit dan menerapkan SAK Indonesia, termasuk anak usaha BUMN, perusahaan sistem pembayaran, fintech, dan grup usaha dengan pinjaman bank.</li>"
   "<li>Perusahaan yang sedang menyiapkan IPO atau penerbitan surat utang.</li>"
   "<li>Perusahaan dengan banyak pos lain-lain, investasi pada asosiasi, atau pinjaman valas.</li>"
   "<li>Tim keuangan yang sibuk dengan tutup buku dan butuh tim tambahan yang paham standar terbaru.</li></ul>"
 + "<h2>Mencoba Sendiri Dulu</h2><p>Anda bisa membaca <a href=\"/artikel/panduan-implementasi-psak-118/\">panduan implementasi PSAK 118</a> beserta template Excel gratis, atau mencoba <a href=\"/cek-psak-118/\">konversi laba rugi PSAK 118</a> secara gratis. Bila hasilnya menunjukkan banyak pos yang perlu dipetakan ulang, kami bisa melanjutkan dari sana.</p>"
 + "<h2>Siapa yang Menangani</h2><p>Ditangani tim Chartered Accountant dan CPA yang mengikuti SAK terbaru dan memahami cara kerja auditor. Untuk kebutuhan audit atau reviu, kami membantu menghubungkan dengan KAP berizin yang sesuai tanpa konflik kepentingan.</p>"
 + "<h2>Bacaan Terkait</h2><ul><li><a href=\"/artikel/panduan-implementasi-psak-118/\">Panduan Implementasi PSAK 118: Roadmap, Contoh Laba Rugi, dan Template Excel</a></li>"
   "<li><a href=\"/artikel/daftar-psak-isak-2026-2027/\">Daftar PSAK dan ISAK yang Berlaku 2026 sampai 2027</a></li>"
   "<li><a href=\"/artikel/amendemen-isak-335-entitas-nonlaba-psak-118/\">Amendemen ISAK 335 untuk Entitas Nonlaba dan PSAK 118</a></li></ul>")
P118_FAQ = [
 ("Kapan PSAK 118 mulai berlaku?", "1 Januari 2027, menggantikan PSAK 201. Karena retrospektif, angka 2026 ikut disajikan ulang sebagai komparatif dalam laporan keuangan 2027."),
 ("Apakah laba bersih berubah karena PSAK 118?", "Tidak. Yang berubah adalah kategori dan subtotal di laba rugi, pengungkapan ukuran kinerja manajemen, agregasi pos, dan klasifikasi arus kas."),
 ("Berapa lama implementasi PSAK 118?", "Untuk satu entitas dengan data yang rapi, gap assessment sampai laporan proforma umumnya 4 sampai 8 minggu. Grup dengan banyak entitas atau valas butuh waktu lebih panjang."),
 ("Apakah FA Indonesia sekaligus mengaudit laporan keuangan?", "Tidak. Kami mendampingi implementasi dan penyusunan. Audit tetap dilakukan KAP independen, dan kami menyiapkan paket pendukung agar proses audit lancar."),
 ("Berapa biayanya?", "Bergantung pada jumlah entitas, kompleksitas akun, dan kebutuhan proforma. Angka pasti disampaikan setelah diskusi awal dan diagnosis singkat, sebelum Anda berkomitmen."),
]
svc_page(P118, "Layanan · Standar Akuntansi", "Jasa Implementasi PSAK 118: Dari Gap Assessment sampai Siap Audit",
  "Pendampingan penerapan PSAK 118 Penyajian dan Pengungkapan dalam Laporan Keuangan yang berlaku 1 Januari 2027: mapping akun, kebijakan akuntansi, MPM, laporan proforma 2026, sampai paket diskusi dengan auditor.",
  p118_body, P118_FAQ, "Jasa Implementasi PSAK 118 (Berlaku 2027) | FA Indonesia",
  "Konsultan implementasi PSAK 118: gap assessment, mapping kategori laba rugi, MPM, proforma 2026, dan koordinasi auditor. Ditangani tim CPA. Seluruh Indonesia.",
  "Jasa Implementasi PSAK 118", "Accounting standard implementation (IFRS 18)",
  "/cek-psak-118/", "Coba Konversi PL PSAK 118", "Halo FA Indonesia, kami ingin konsultasi implementasi PSAK 118 untuk perusahaan kami.", "Implementasi PSAK 118")

# ================= 2. KREDIT DISTRIBUTOR & IMPORTIR =================
PDI = "/konsultan-kredit-distributor-importir/"
pdi_body = (
 "<h2>Masalah yang Paling Sering Kami Temui</h2><ul>"
 "<li>Penjualan naik, tetapi plafon kredit modal kerja tidak ikut naik karena laporan keuangan tidak menggambarkan perputaran usaha yang sebenarnya.</li>"
 "<li>Persediaan dan piutang besar, tetapi bank menilai agunan kurang karena data umur piutang dan stok tidak rapi.</li>"
 "<li>Semua fasilitas ada di satu bank, sehingga posisi tawar bunga dan plafon lemah.</li>"
 "<li>Importir membayar pemasok dengan kas sendiri, padahal bisa memakai fasilitas trade finance.</li></ul>"
 "<h2>Fasilitas yang Bisa Dioptimalkan</h2>"
 + tbl(["Fasilitas", "Fungsi", "Yang Menentukan Besar Plafon"], [
   ("Kredit modal kerja revolving", "Membiayai siklus beli, simpan, jual", "Perputaran persediaan dan piutang, arus kas operasi"),
   ("Letter of Credit (LC) dan SKBDN", "Pembayaran impor dan pembelian dalam negeri", "Riwayat transaksi, kontrak pemasok, margin"),
   ("Trust receipt", "Melunasi LC lalu barang dijual dulu", "Kecepatan barang terjual dan disiplin pelunasan"),
   ("Pembiayaan piutang (invoice financing)", "Mencairkan tagihan ke pelanggan besar", "Kualitas pelanggan dan umur piutang"),
   ("Bank garansi", "Jaminan ke prinsipal atau pemasok", "Kekuatan neraca dan agunan"),
   ("Kredit investasi", "Gudang, armada, sistem", "Proyeksi arus kas dan nilai agunan"),
 ])
 + "<h2>Cara Kami Membantu Memaksimalkan Plafon</h2>" + flow([
   ("Diagnosis", "Membaca laporan keuangan, rekening koran, umur piutang, stok, dan fasilitas yang berjalan."),
   ("Hitung kebutuhan wajar", "Kebutuhan modal kerja dari siklus kas, bukan sekadar angka yang diminta."),
   ("Rapikan data", "Laporan keuangan, CALK, rekonsiliasi dengan SPT, dan bila perlu audit oleh KAP rekanan bank."),
   ("Paket pengajuan", "Memo kredit, proyeksi, borrowing base, dan struktur fasilitas yang diusulkan."),
   ("Negosiasi", "Pendampingan ke bank yang ada, penambahan bank kedua, atau take over bila lebih menguntungkan.")])
 + "<h2>Rasio yang Dibaca Analis Kredit</h2>"
 + tbl(["Rasio", "Kenapa Penting untuk Distributor"], [
   ("Hari perputaran piutang", "Menunjukkan berapa lama kas tertahan di pelanggan"),
   ("Hari perputaran persediaan", "Stok lambat menurunkan nilai agunan dan kepercayaan bank"),
   ("Current ratio dan quick ratio", "Kemampuan membayar kewajiban jangka pendek"),
   ("Debt to equity", "Ruang tambahan utang yang masih wajar"),
   ("DSCR", "Kecukupan arus kas untuk pokok dan bunga"),
 ])
 + "<h2>Kerahasiaan Data</h2><p>Sebelum data perusahaan dikirim, kami menandatangani NDA lebih dulu. Data hanya dipakai untuk analisis dan pengajuan yang Anda setujui.</p>"
 + "<h2>Bacaan Terkait</h2><ul><li><a href=\"/konsultan-kredit-bank/\">Konsultan Kredit Bank</a></li>"
   "<li><a href=\"/artikel/kmk-vs-kredit-investasi/\">KMK vs Kredit Investasi</a></li>"
   "<li><a href=\"/artikel/rasio-keuangan-yang-dilihat-bank/\">Rasio Keuangan yang Dilihat Bank</a></li>"
   "<li><a href=\"/artikel/dokumen-pengajuan-kredit-korporasi/\">Dokumen Pengajuan Kredit Korporasi</a></li>"
   "<li><a href=\"/artikel/alasan-kredit-bank-ditolak/\">Alasan Kredit Bank Ditolak dan Cara Memperbaikinya</a></li></ul>")
PDI_FAQ = [
 ("Bisakah plafon kredit dinaikkan tanpa menambah agunan?", "Kadang bisa, bila arus kas dan perputaran usaha terbukti kuat dan datanya rapi. Struktur seperti trust receipt atau pembiayaan piutang juga mengandalkan transaksi, bukan hanya agunan tetap. Hasilnya tetap bergantung pada penilaian bank."),
 ("Apakah perlu pindah bank untuk mendapat plafon lebih besar?", "Tidak selalu. Sering kali langkah pertama adalah menata ulang fasilitas di bank yang ada. Bank kedua atau take over dipertimbangkan bila memberi bunga, plafon, atau syarat yang lebih baik."),
 ("Apakah laporan keuangan harus diaudit?", "Untuk plafon besar umumnya ya, dan sebagian bank mensyaratkan KAP dari daftar rekanannya. Kami membantu menyiapkan laporan dan menghubungkan dengan KAP yang sesuai."),
 ("Bagaimana skema biayanya?", "Umumnya retainer bulanan selama pendampingan ditambah success fee saat fasilitas cair. Angka pasti disampaikan setelah diskusi awal, sebelum Anda berkomitmen."),
]
svc_page(PDI, "Layanan · Distributor & Importir", "Konsultan Kredit untuk Distributor dan Importir: Memaksimalkan Plafon Modal Kerja dan Trade Finance",
  "Pendampingan bagi distributor, importir, dan pedagang besar yang ingin plafon kredit modal kerja, LC, trust receipt, dan pembiayaan piutang sesuai skala usahanya. Mulai dari diagnosis data sampai negosiasi dengan bank.",
  pdi_body, PDI_FAQ, "Konsultan Kredit Distributor & Importir: Plafon Modal Kerja, LC | FA Indonesia",
  "Maksimalkan plafon kredit distributor dan importir: modal kerja revolving, LC, SKBDN, trust receipt, invoice financing. Diagnosis, paket pengajuan, negosiasi bank.",
  "Konsultan Kredit Distributor dan Importir", "Working capital and trade finance advisory",
  "/konsultan-kredit-bank/", "Konsultan Kredit Bank", "Halo FA Indonesia, kami distributor/importir dan ingin memaksimalkan plafon kredit perusahaan.", "Kredit Distributor dan Importir")

URLS = [P118, PDI]

# ================= 3. SISIPAN CTA DI HALAMAN TERKAIT =================
def box(href, title, text):
    return (f'<!--fa-lead--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
            f'<p style="margin:0 0 6px;font-weight:600">{E(title)}</p><p style="margin:0 0 12px">{E(text)}</p>'
            f'<a class="btn solid" href="{href}">Lihat Layanan</a></div><!--/fa-lead-->')
INJ = {
 ("artikel", "panduan-implementasi-psak-118"): box(P118, "Butuh Tim untuk Implementasi PSAK 118?", "Kami mendampingi dari gap assessment, mapping akun, MPM, sampai laporan proforma 2026 yang siap dibahas dengan auditor."),
 ("artikel", "daftar-psak-isak-2026-2027"): box(P118, "Pendampingan Implementasi PSAK 118", "PSAK 118 berlaku 1 Januari 2027 dan angka 2026 ikut disajikan ulang. Mulai dari diskusi awal gratis."),
 ("konsultan-kredit-bank",): box(PDI, "Distributor atau Importir?", "Lihat cara memaksimalkan plafon modal kerja, LC, trust receipt, dan pembiayaan piutang."),
 ("artikel", "kmk-vs-kredit-investasi"): box(PDI, "Plafon Modal Kerja Distributor dan Importir", "Kebutuhan modal kerja dihitung dari siklus kas, lalu dikemas menjadi paket pengajuan ke bank."),
 ("artikel", "rasio-keuangan-yang-dilihat-bank"): box(PDI, "Distributor yang Ingin Plafon Lebih Besar", "Kami bantu rapikan rasio perputaran piutang dan persediaan sebelum mengajukan ke bank."),
}
for parts, b in INJ.items():
    p = P(*parts, "index.html")
    if not os.path.exists(p): print("skip", p); continue
    t = re.sub(r"<!--fa-lead-->.*?<!--/fa-lead-->", "", rd(p), flags=re.S)
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("</main>")
    wtxt(p, t[:k] + b + t[k:])

# footer sengaja tidak diubah (menyentuh ratusan file); tautan masuk lewat /layanan/ dan artikel terkait

# /layanan/
lp = P("layanan", "index.html")
t = re.sub(r"<!--fa-lead-svc-->.*?<!--/fa-lead-svc-->", "", rd(lp), flags=re.S)
blk = ('<!--fa-lead-svc--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Paling Banyak Ditanyakan</p><h2>Implementasi PSAK 118 dan Kredit Distributor</h2></div>'
       '<p class="t" style="max-width:62em">PSAK 118 berlaku 1 Januari 2027 dengan komparatif 2026. Distributor dan importir ingin plafon modal kerja dan trade finance yang sesuai skala usaha.</p>'
       '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn solid" href="/jasa-implementasi-psak-118/">Implementasi PSAK 118</a><a class="btn line" href="/konsultan-kredit-distributor-importir/">Kredit Distributor &amp; Importir</a></div></div></section><!--/fa-lead-svc-->')
i = t.find('<section class="block'); wtxt(lp, t[:i] + blk + t[i:])

# sitemap
sm = re.sub(r"<!--fa-lead-->.*?<!--/fa-lead-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-lead-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for u in URLS) + "<!--/fa-lead-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)

# llms.txt
ll = re.sub(r"\n## Layanan Spesifik.*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + ("\n\n## Layanan Spesifik\n- Jasa implementasi PSAK 118 (berlaku 1 Januari 2027): gap assessment, mapping kategori, MPM, proforma 2026, koordinasi auditor → https://faindonesia.co.id/jasa-implementasi-psak-118/\n"
       "- Konsultan kredit distributor dan importir: plafon modal kerja, LC, SKBDN, trust receipt, invoice financing → https://faindonesia.co.id/konsultan-kredit-distributor-importir/\n")
wtxt(P("llms.txt"), ll)
print("ok", URLS)
