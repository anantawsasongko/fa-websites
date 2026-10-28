# -*- coding: utf-8 -*-
"""Halaman untuk mitra perujuk (27 Okt 2026):
- /mitra-rm-bank/ : Relationship Manager bank yang mencari debitur korporasi (dua arah: FA merujuk klien, RM merujuk nasabah yang belum siap)
- /mitra-sekuritas/ : sekuritas dan penjamin emisi yang mencari calon emiten
- 2 artikel Eksplor: cara RM bank mencari debitur korporasi, cara sekuritas mencari calon emiten IPO
Plus kartu di Eksplor, blok di /layanan/, link footer, kotak di halaman terkait, sitemap, llms.txt.
Idempoten: halaman ditimpa, sisipan memakai penanda komentar fa-mitra.
Jalankan setelah fa_tone_20261026.py (atau script lain yang menyentuh v58), sebelum fa_rapi_20261027.py dan prep.py.
"""
import os, re, json, html
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
D = "https://faindonesia.co.id"
WA = "https://wa.me/6282245260121?text="
TODAY = "2026-10-27"
E = html.escape
def P(*a): return os.path.join(FA, *a)
def rd(p): return open(p, encoding="utf-8").read()
def wtxt(p, s): open(p, "w", encoding="utf-8").write(s)
def wa(msg): return WA + quote(msg)

TPL_SVC = rd(P("konsultan-kredit-bank", "index.html"))
TPL_ART = rd(P("artikel", "alasan-kredit-bank-ditolak", "index.html"))
AUTHOR_BOX = re.search(r'<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333.*?</div></div>', TPL_ART, re.S).group(0)
PROVIDER = {"@type": "ProfessionalService", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"}
AUTHOR = {"@type": "Person", "@id": D + "/ananta-w-sasongko/#person", "name": "Ananta W. Sasongko, CPA", "url": D + "/ananta-w-sasongko/"}
MAIL = "ananta@faindonesia.co.id"
CSS = ('<style id="fa-mitra">.tblwrap{overflow-x:auto;margin:8px 0 22px;-webkit-overflow-scrolling:touch}.tblwrap table{min-width:560px;margin:0}'
       '.art th,.art td{border:1px solid #333;padding:9px 10px;text-align:left;vertical-align:top}'
       '.flow5{list-style:none;padding:0;margin:10px 0 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;counter-reset:f}'
       '.flow5 li{border:1px solid #333;border-radius:10px;padding:14px 14px 14px 52px;position:relative;background:#1e1e1e;font-family:Poppins,sans-serif!important;font-size:14px!important;line-height:1.5!important;'
       'opacity:0;transform:translateY(10px);animation:fm-in .5s ease forwards}'
       '.flow5 li:nth-child(2){animation-delay:.08s}.flow5 li:nth-child(3){animation-delay:.16s}.flow5 li:nth-child(4){animation-delay:.24s}.flow5 li:nth-child(5){animation-delay:.32s}'
       '@keyframes fm-in{to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.flow5 li{animation:none;opacity:1;transform:none}}'
       '.flow5 li:before{counter-increment:f;content:counter(f);position:absolute;left:14px;top:13px;width:26px;height:26px;border-radius:50%;background:#fff;color:#171717;display:grid;place-items:center;font-size:12px;font-weight:600}'
       '.flow5 li b{display:block;font-weight:600;margin-bottom:2px}'
       '.gain{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:10px 0 26px}'
       '.gain div{border:1px solid #333;border-radius:10px;padding:16px;background:linear-gradient(150deg,#262626,#161616)}'
       '.gain b{display:block;font-family:var(--display);font-weight:400;font-size:20px;margin-bottom:6px}'
       '.gain span{display:block;font-family:Poppins,sans-serif;font-size:14px;line-height:1.55;color:var(--muted,#bbb)}'
       '.twoway{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;margin:12px 0 24px;font-family:Poppins,sans-serif;font-size:14px}'
       '.twoway .n{border:1px solid #333;border-radius:10px;padding:14px;background:#1e1e1e;text-align:center}'
       '.twoway .n b{display:block;font-weight:600;margin-bottom:2px}.twoway .a{font-size:22px;opacity:.7;text-align:center}'
       '@media (max-width:560px){.twoway{grid-template-columns:1fr}.twoway .a{transform:rotate(90deg)}}</style>')

def set_head(s, title, desc, url, ld):
    s = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', s, count=1)
    for a in ['name="description"', 'property="og:description"']:
        s = re.sub(rf'<meta {a} content="[^"]*">', f'<meta {a} content="{E(desc)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", s, count=1, flags=re.S)
    s = re.sub(r'<style id="fa-(lead|mitra)">.*?</style>', "", s, flags=re.S)
    return s.replace("</head>", CSS + "</head>", 1)

def set_main(s, inner):
    i = s.find('<main id="top">'); j = s.find("</main>")
    return s[:i] + '<main id="top">\n' + inner + "\n" + s[j:]

def flow(items): return '<ol class="flow5">' + "".join(f"<li><b>{E(t)}</b>{E(d)}</li>" for t, d in items) + "</ol>"
def gain(items): return '<div class="gain">' + "".join(f"<div><b>{E(t)}</b><span>{E(d)}</span></div>" for t, d in items) + "</div>"
def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
def faq_html(faq): return "".join(f'<p style="margin:0 0 18px"><b>{E(q)}</b><br>{E(a)}</p>' for q, a in faq)
def faq_ld(faq): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def crumbs(items): return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}
def btns(wa_msg, extra=""):
    return (f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px"><a class="btn solid" href="{wa(wa_msg)}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
            f'<a class="btn line" href="mailto:{MAIL}?subject={quote("Kerja Sama Mitra FA Indonesia")}">Email Kerja Sama</a>{extra}</div>')

def partner_page(path, eyebrow, h1, lead, body, faq, title, desc, audience, wa_msg, crumb_name, extra_btn=""):
    url = D + path
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "id",
         "audience": {"@type": "BusinessAudience", "audienceType": audience}, "publisher": PROVIDER, "about": PROVIDER},
        {"@type": "Service", "name": crumb_name, "serviceType": "Referral and financing readiness partnership", "provider": PROVIDER,
         "audience": {"@type": "BusinessAudience", "audienceType": audience}, "areaServed": {"@type": "Country", "name": "Indonesia"}, "url": url},
        faq_ld(faq), crumbs([("FA Indonesia", D + "/"), ("Layanan", D + "/layanan/"), (crumb_name, url)])]}
    main = (f'<section class="block">\n<div class="wrap art">\n<p class="eyebrow">{eyebrow}</p>\n'
            f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{E(h1)}</h1>\n'
            f'<p class="t" style="max-width:62em">{lead}</p>\n{btns(wa_msg, extra_btn)}\n'
            f'{body}\n<h2>Pertanyaan Umum</h2>\n{faq_html(faq)}\n{btns(wa_msg)}\n{AUTHOR_BOX}\n</div>\n</section>')
    p = P(*path.strip("/").split("/"), "index.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
    wtxt(p, set_main(set_head(TPL_SVC, title, desc, url, ld), main))

def art_page(slug, cat, title, h1, desc, minutes, body, faq, related, sources, cta_href, cta_label, wa_msg, box=""):
    url = f"{D}/artikel/{slug}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": h1, "description": desc, "url": url, "mainEntityOfPage": url, "inLanguage": "id",
         "datePublished": TODAY + "T08:00:00+07:00", "dateModified": TODAY + "T08:00:00+07:00", "author": AUTHOR, "publisher": PROVIDER,
         "articleSection": cat, "image": D + "/img/ananta-w-sasongko-cpa.jpg"},
        faq_ld(faq), crumbs([("FA Indonesia", D + "/"), ("Eksplor", D + "/artikel/"), (h1, url)])]}
    rel = "".join(f'<li><a href="{h}">{E(t)}</a></li>' for h, t in related)
    src = "".join(f'<li><a href="{h}" rel="noopener" target="_blank">{E(t)}</a></li>' for t, h in sources)
    main = (f'<section class="block">\n<div class="wrap art">\n<p class="eyebrow"><a href="/artikel/" style="text-decoration:none">Eksplor · {E(cat)}</a></p>\n'
            f'<h1 style="margin:.2em 0 .4em;font-size:clamp(32px,4.4vw,52px);line-height:1.12">{E(h1)}</h1>\n'
            f'<p class="meta">Oleh <a href="/ananta-w-sasongko/">Ananta W. Sasongko, CPA, FMVA, FPAP</a> · 27 Oktober 2026 · {minutes} menit baca</p>\n'
            f'{body}\n<h2>Pertanyaan Umum</h2>\n{faq_html(faq)}\n<h2>Baca Juga</h2>\n<ul>{rel}</ul>\n'
            + (f'<h2>Sumber</h2>\n<ul>{src}</ul>\n' if src else "")
            + f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn solid" href="{cta_href}">{E(cta_label)}</a>'
            f'<a class="btn line" href="{wa(wa_msg)}" rel="noopener" target="_blank">Chat Ananta, CPA</a><a class="btn line" href="/artikel/">Eksplor Lainnya</a></div>\n'
            f'{box}{AUTHOR_BOX}\n</div>\n</section>')
    p = P("artikel", slug, "index.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
    wtxt(p, set_main(set_head(TPL_ART, title, desc, url, ld), main))

# ================= 1. MITRA RM BANK =================
PRM = "/mitra-rm-bank/"
WA_RM = "Halo FA Indonesia, saya Relationship Manager bank dan ingin berdiskusi soal kerja sama rujukan debitur korporasi."
rm_body = (
 "<h2>Yang RM Dapatkan dari Kerja Sama Ini</h2>"
 + gain([
   ("Calon Debitur yang Sudah Disaring", "Legalitas, SLIK pengurus, rasio dasar, dan kesesuaian data pajak dicek sebelum perusahaan diperkenalkan."),
   ("Berkas Kredit yang Rapi", "Laporan keuangan tiga tahun, CALK, rekonsiliasi SPT, proyeksi arus kas, DSCR, dan perhitungan kebutuhan modal kerja dalam satu paket."),
   ("Lawan Bicara yang Paham Bahasa Analis", "Pertanyaan analis dan komite dijawab tim yang terbiasa menyusun memo kredit, jadi berkas tidak bolak-balik."),
   ("Tanpa Biaya untuk Bank dan RM", "Pendampingan dibayar oleh perusahaan klien. Keputusan kredit sepenuhnya ada di bank."),
 ])
 + "<h2>Dua Arah Rujukan</h2>"
 + '<div class="twoway"><div class="n"><b>Klien FA</b>Butuh kredit dan berkasnya sudah dirapikan</div><div class="a">⇄</div><div class="n"><b>RM Bank</b>Butuh debitur yang cepat diproses</div></div>'
 + "<p>Arah pertama: perusahaan yang kami dampingi dan sedang mencari kredit kami perkenalkan ke RM yang segmen dan selera risikonya cocok, tentu setelah klien setuju.</p>"
 + "<p>Arah kedua: RM sering punya prospek bagus yang tertahan karena laporan keuangan belum diaudit, pembukuan belum rapi, atau angka omzet berbeda dengan SPT. Rujuk perusahaan itu ke kami. Setelah datanya dibenahi, pengajuannya kembali diproses melalui RM yang merujuk.</p>"
 + "<h2>Profil Calon Debitur yang Kami Dampingi</h2>"
 + tbl(["Sektor", "Kebutuhan yang Paling Sering"], [
   ("Rumah Sakit dan Klinik", "Kredit investasi gedung dan alat kesehatan, KMK untuk piutang BPJS, take over"),
   ("Kontraktor", "KMK berbasis SPK atau kontrak, bank garansi, invoice financing"),
   ("Distributor dan Importir", "KMK revolving, LC dan SKBDN, trust receipt, pembiayaan piutang"),
   ("Manufaktur", "Kredit investasi mesin dan pabrik, KMK bahan baku"),
   ("Logistik dan Kargo", "Kredit investasi armada, KMK operasional"),
   ("Grup Usaha Keluarga", "Refinancing, konsolidasi fasilitas, kredit sindikasi"),
 ])
 + "<p>Skalanya beragam, dari UMKM yang baru pertama kali mengajukan kredit sampai grup usaha dengan kebutuhan ratusan miliar rupiah. Layanan menjangkau seluruh Indonesia secara daring maupun kunjungan.</p>"
 + "<h2>Alur Kerja Sama</h2>" + flow([
   ("Kenalan", "Diskusi singkat soal segmen, sektor, plafon, dan selera risiko yang sedang dicari."),
   ("Pencocokan", "Kami cocokkan dengan klien yang kebutuhannya sesuai, setelah klien setuju dan NDA berjalan."),
   ("Paket Kredit", "Berkas dikirim dalam format yang biasa diminta analis: LK, proyeksi, DSCR, legal, agunan."),
   ("Proses Bank", "RM dan analis memproses sesuai kebijakan bank. Kami bantu menjawab pertanyaan dan melengkapi data."),
   ("Setelah Cair", "Kami bantu klien menjaga pelaporan berkala dan covenant supaya fasilitas tetap sehat.")])
 + "<h2>Untuk Dept Head Commercial dan Kepala Bisnis</h2>"
   "<p>Yang dipikirkan Commercial Head bukan satu nasabah, tetapi pipeline dan target penyaluran per kuartal. Kerja sama ini dirancang untuk membantu di tiga titik yang paling sering menahan angka:</p>"
 + gain([
   ("Pipeline Prospek yang Bisa Diproyeksikan", "Calon debitur yang sudah disaring masuk dengan perkiraan plafon, jenis fasilitas, dan kapan berkasnya lengkap, jadi bisa dimasukkan ke rencana penyaluran kuartal."),
   ("Fasilitas Sudah Disetujui tapi Belum Ditarik", "Undisbursed loan sering tertahan syarat pencairan: laporan audit, dokumen proyek, agunan, atau covenant. Kami bantu debitur memenuhi syaratnya supaya fasilitas bisa ditarik."),
   ("Kualitas Portofolio Setelah Cair", "Pelaporan berkala, covenant keuangan, dan rekonsiliasi pajak dijaga, sehingga debitur tidak berubah jadi nasabah dalam perhatian khusus."),
   ("Sesi Saringan untuk Tim RM", "Sesi singkat untuk tim RM cabang atau wilayah: cara membaca laporan keuangan calon debitur dan menyaring prospek dalam 15 menit dengan alat Cek Kapasitas Kredit."),
 ])
 + "<p>Per September 2026, Bank Indonesia mencatat kredit yang sudah disetujui tetapi belum ditarik debitur (undisbursed loan) sekitar Rp2.562,7 triliun. Sebagian dari angka itu tertahan karena debitur belum siap memenuhi syarat pencairan, bukan karena tidak butuh dana. Di situ peran kami dari sisi debitur. Pembahasan lengkapnya ada di artikel <a href=\"/artikel/undisbursed-loan-cara-mempercepat-pencairan-kredit/\">undisbursed loan dan cara mempercepat pencairan</a>.</p>"
 + "<h2>Kerahasiaan dan Batas Peran</h2><ul>"
   "<li>Data klien hanya dibuka setelah NDA dan persetujuan klien.</li>"
   "<li>FA Indonesia tidak menerima imbalan dari bank. Kami dibayar oleh klien sesuai kontrak pendampingan.</li>"
   "<li>Kami tidak menjanjikan persetujuan kredit. Analisis dan keputusan tetap di bank.</li>"
   "<li>Bila bank mensyaratkan audit oleh KAP rekanan, kami membantu klien menunjuk KAP yang sesuai dan menyiapkan berkas auditnya.</li></ul>"
 + "<h2>Rekam Jejak</h2><p>Tim FA Indonesia telah mendampingi pembiayaan perbankan kumulatif lebih dari Rp1 triliun di bank BUMN, bank syariah, dan bank swasta, mulai dari kredit modal kerja, kredit investasi, take over, sampai kredit sindikasi. "
   "Tim kami terdiri dari Chartered Accountant dan CPA dengan latar audit firma Big Four, bekerja bersama KAP dan KJPP mitra.</p>"
 + "<h2>Bacaan untuk RM</h2><ul>"
   "<li><a href=\"/artikel/cara-rm-bank-mencari-debitur-korporasi/\">Cara RM Bank Mencari Debitur Korporasi yang Layak dan Cepat Diproses</a></li>"
   "<li><a href=\"/artikel/cara-mencapai-target-penyaluran-kredit-korporasi/\">Cara Mencapai Target Penyaluran Kredit Korporasi: Panduan untuk RM dan Commercial Head</a></li>"
   "<li><a href=\"/artikel/undisbursed-loan-cara-mempercepat-pencairan-kredit/\">Undisbursed Loan: Kenapa Fasilitas Kredit Belum Ditarik dan Cara Mempercepat Pencairan</a></li>"
   "<li><a href=\"/artikel/alasan-kredit-bank-ditolak/\">Alasan Kredit Bank Ditolak dan Cara Memperbaikinya</a></li>"
   "<li><a href=\"/artikel/dokumen-pengajuan-kredit-korporasi/\">Dokumen Pengajuan Kredit Korporasi</a></li>"
   "<li><a href=\"/cek-kapasitas-kredit/\">Cek Kapasitas Kredit Gratis</a>, bisa dipakai untuk menyaring prospek</li></ul>")
RM_FAQ = [
 ("Apakah ada biaya untuk RM atau bank?", "Tidak. Pendampingan dibayar oleh perusahaan klien sesuai kontrak dengan FA Indonesia. Bank dan RM tidak membayar apa pun."),
 ("Apakah klien FA bisa diarahkan ke bank tertentu?", "Pilihan bank tetap di tangan klien. Kami menyampaikan opsi yang paling sesuai dengan kebutuhan dan profil risikonya, lalu memperkenalkan RM yang segmennya cocok."),
 ("Kalau saya merujuk nasabah yang belum siap, apakah nasabah itu pindah ke bank lain?", "Tidak. Setelah data dibenahi, pengajuan kembali diproses melalui RM yang merujuk, kecuali nasabah sendiri memutuskan lain."),
 ("Sektor dan skala apa yang paling banyak?", "Rumah sakit dan klinik, kontraktor, distributor dan importir, manufaktur, logistik, dan grup usaha keluarga, dari UMKM hingga perusahaan besar."),
 ("Bagaimana cara cari prospek kredit korporasi yang cepat cair?", "Mulai dari calon debitur yang laporan keuangannya sudah bisa dibaca analis: tiga tahun, konsisten dengan SPT, dan ada proyeksi arus kas. Kami merujuk perusahaan yang sudah melewati saringan itu, sehingga waktu dari pertemuan pertama ke pencairan lebih pendek."),
 ("Bisakah membantu debitur menarik fasilitas yang sudah disetujui tapi belum dicairkan?", "Bisa. Kami membantu debitur memenuhi syarat pencairan seperti laporan audit, dokumen proyek, kelengkapan agunan, atau pemenuhan covenant, dengan persetujuan debitur dan tetap mengikuti ketentuan bank."),
 ("Apakah ada program untuk tim RM satu cabang atau wilayah?", "Ada sesi saringan prospek untuk tim RM: membaca laporan keuangan calon debitur, rasio yang dilihat analis, dan pemakaian alat Cek Kapasitas Kredit. Hubungi kami untuk jadwalnya."),
 ("Bagaimana cara memulai?", "Kirim pesan lewat tombol Chat Ananta, CPA atau email ananta@faindonesia.co.id dengan segmen dan sektor yang sedang Anda cari."),
]
partner_page(PRM, "Mitra · Relationship Manager Bank",
  "Untuk RM dan Commercial Head Bank: Prospek Debitur Korporasi yang Siap Diproses dan Siap Cair",
  "Klien FA Indonesia adalah perusahaan yang sedang mencari kredit modal kerja, kredit investasi, take over, atau refinancing. Sebelum bertemu bank, laporan keuangan, rekonsiliasi pajak, proyeksi arus kas, dan dokumen legalnya kami rapikan lebih dulu. RM menerima calon debitur yang lebih cepat diproses analis dan komite, dan Commercial Head mendapat pipeline penyaluran yang lebih bisa diandalkan.",
  rm_body, RM_FAQ, "Cari Prospek Kredit Korporasi Siap Cair: Untuk RM & Commercial Head | FA Indonesia",
  "RM dan Commercial Head bank mencari prospek debitur korporasi untuk target penyaluran? FA Indonesia merujuk perusahaan yang berkas kreditnya rapi dan siap cair. Tanpa biaya untuk bank.",
  "Relationship Manager bank, account officer, junior marketing kredit, Dept Head Commercial dan kepala bisnis kredit korporasi dan komersial", WA_RM, "Mitra RM Bank")

# ================= 2. MITRA SEKURITAS =================
PSK = "/mitra-sekuritas/"
WA_SK = "Halo FA Indonesia, saya dari sekuritas atau penjamin emisi dan ingin berdiskusi soal calon emiten."
sk_body = (
 "<h2>Yang Kami Siapkan Sebelum Calon Emiten Diperkenalkan</h2>"
 + tbl(["Area", "Kondisi yang Kami Kejar"], [
   ("Laporan Keuangan", "Historis siap diaudit KAP terdaftar OJK, kebijakan akuntansi sesuai SAK terbaru termasuk PSAK 118 yang berlaku 1 Januari 2027"),
   ("Tata Kelola", "Komisaris Independen, Komite Audit, Sekretaris Perusahaan, dan Unit Audit Internal beserta piagamnya"),
   ("Legal dan Aset", "Aset material atas nama perusahaan, perizinan dan kontrak material tertib"),
   ("Pihak Berelasi", "Transaksi dengan perusahaan keluarga terdokumentasi dan diungkapkan"),
   ("Model Keuangan", "Proyeksi, rencana penggunaan dana, dan equity story yang bisa dipertahankan di depan investor"),
   ("Data Room", "Tertata untuk due diligence penjamin emisi, KAP, konsultan hukum, dan KJPP"),
 ])
 + "<h2>Apa Untungnya bagi Sekuritas</h2>"
 + gain([
   ("Waktu Mandat Lebih Pendek", "Pekerjaan rumah internal yang biasanya memakan berbulan-bulan sudah berjalan sebelum penjamin emisi masuk."),
   ("Risiko Penyajian Ulang Lebih Kecil", "Kebijakan akuntansi dikunci lebih awal sehingga laporan historis tidak perlu diubah di tengah jalan."),
   ("Satu Koordinator di Sisi Perusahaan", "Tim kami menjaga master timetable dan mengejar dokumen dari pihak internal emiten."),
   ("Pipeline Jangka Menengah", "Perusahaan yang belum siap tetap kami dampingi, sehingga siap dibahas lagi 1 sampai 3 tahun ke depan."),
 ])
 + "<h2>Saringan Awal Kelayakan</h2><p>Sebelum diperkenalkan, setiap calon emiten diuji cepat terhadap syarat keuangan papan pencatatan Bursa Efek Indonesia (Utama, Pengembangan, Akselerasi) memakai <a href=\"/cek-kelayakan-ipo/\">Cek Kelayakan IPO</a>. "
   "Alat yang sama bisa dipakai tim sekuritas secara gratis untuk menyaring prospek sendiri.</p>"
 + "<h2>Alur Kerja Sama</h2>" + flow([
   ("Kenalan", "Sektor, ukuran emisi, dan papan pencatatan yang sedang dibidik sekuritas."),
   ("Pencocokan", "Perkenalan dengan calon emiten yang cocok, setelah persetujuan klien dan NDA."),
   ("Readiness Mapping", "Diagnosis 6 sampai 8 minggu. Hasilnya dibagikan ke sekuritas atas persetujuan klien."),
   ("Pembenahan Bersama", "Laporan keuangan, GCG, legal, dan data room dikerjakan paralel dengan masukan penjamin emisi."),
   ("Mandat dan Pencatatan", "Penjamin emisi memimpin proses ke OJK dan BEI, kami tetap mengawal pekerjaan internal.")])
 + "<h2>Bila Prospek Belum Siap IPO</h2><p>Tidak semua pemilik yang ingin IPO sebaiknya langsung IPO. Sebagian lebih cocok memakai kredit bank atau investor privat lebih dulu. "
   "Rujuk prospek seperti itu ke kami. Kami bantu jalur pendanaan antaranya, lalu ketika angka dan tata kelolanya matang, perusahaan itu kembali ke sekuritas yang merujuk.</p>"
 + "<h2>Peran yang Jelas</h2><ul>"
   "<li>FA Indonesia bekerja dari sisi perusahaan. Kami bukan penjamin emisi dan bukan KAP, sehingga tidak mengaudit laporan yang kami bantu susun.</li>"
   "<li>Penunjukan penjamin emisi tetap keputusan perusahaan.</li>"
   "<li>Data calon emiten hanya dibuka setelah NDA dan persetujuan pemiliknya.</li></ul>"
 + "<h2>Rekam Jejak</h2><p>Tim FA Indonesia berpengalaman memimpin persiapan IPO dari sisi perusahaan, mendampingi akuisisi tiga rumah sakit di Jawa Tengah, menggalang pendanaan investor hingga US$3 juta untuk grup rumah sakit, "
   "dan memegang mandat divestasi rumah sakit dan BPR. Tim terdiri dari Chartered Accountant dan CPA dengan latar audit firma Big Four.</p>"
 + "<h2>Bacaan untuk Tim Sekuritas</h2><ul>"
   "<li><a href=\"/artikel/cara-sekuritas-mencari-calon-emiten-ipo/\">Cara Sekuritas Mencari Calon Emiten IPO: Sumber Prospek dan Tanda Siap</a></li>"
   "<li><a href=\"/artikel/checklist-persiapan-ipo/\">Checklist Persiapan IPO Sebelum Penjamin Emisi Masuk</a></li>"
   "<li><a href=\"/konsultan-persiapan-ipo/\">Pendampingan Persiapan IPO</a></li></ul>")
SK_FAQ = [
 ("Apakah FA Indonesia penjamin emisi efek?", "Bukan. Kami mendampingi perusahaan dari dalam: laporan keuangan, tata kelola, legal, model keuangan, dan data room. Penjaminan emisi tetap dikerjakan sekuritas berizin."),
 ("Seberapa siap calon emiten yang diperkenalkan?", "Minimal sudah melewati saringan syarat keuangan papan pencatatan BEI dan diskusi awal dengan pemilik. Yang sudah menjalani IPO Readiness Mapping punya daftar pembenahan tertulis."),
 ("Apakah sekuritas bisa merujuk prospek yang belum siap?", "Bisa. Kami bantu pembenahan atau jalur pendanaan antara, lalu perusahaan kembali ke sekuritas yang merujuk ketika sudah matang."),
 ("Sektor apa saja yang ada di pipeline?", "Terutama kesehatan (rumah sakit dan klinik), konstruksi, distribusi, manufaktur, dan grup usaha keluarga. Kami tidak menyebut nama perusahaan sebelum ada persetujuan dan NDA."),
 ("Bagaimana cara memulai?", "Kirim pesan lewat tombol Chat Ananta, CPA atau email ananta@faindonesia.co.id dengan sektor dan ukuran emisi yang sedang Anda cari."),
]
partner_page(PSK, "Mitra · Sekuritas & Penjamin Emisi",
  "Untuk Sekuritas dan Penjamin Emisi: Calon Emiten yang Pekerjaan Rumahnya Sudah Dikerjakan",
  "Tim sekuritas sering bertemu pemilik yang ingin IPO, tetapi laporan keuangannya belum pernah diaudit, aset masih atas nama pribadi, dan organ perseroan belum lengkap. FA Indonesia mendampingi calon emiten dari sisi perusahaan, sehingga ketika penjamin emisi masuk, angka dan dokumennya sudah bisa diuji.",
  sk_body, SK_FAQ, "Untuk Sekuritas: Calon Emiten IPO yang Siap Diproses | FA Indonesia",
  "Sekuritas dan penjamin emisi mencari calon emiten? FA Indonesia menyiapkan perusahaan dari dalam: laporan keuangan siap audit KAP terdaftar OJK, GCG, data room.",
  "Sekuritas, penjamin emisi efek, investment banker, dan investor ekuitas", WA_SK, "Mitra Sekuritas",
  '<a class="btn line" href="/cek-kelayakan-ipo/">Cek Kelayakan IPO</a>')

# ================= 3. ARTIKEL =================
A_RM = "cara-rm-bank-mencari-debitur-korporasi"
rm_art = (
 "<p>Target penyaluran kredit jarang turun, sementara calon debitur korporasi yang benar-benar siap diproses tidak banyak. Sebagian besar waktu RM habis untuk prospek yang ternyata belum punya laporan keuangan yang bisa dibaca analis, data pajaknya tidak cocok, atau legalitas agunannya belum beres.</p>"
 "<p>Tulisan ini merangkum dari mana debitur korporasi yang layak biasanya datang, bagaimana menyaringnya sejak pertemuan pertama, dan kapan lebih efisien bekerja sama dengan pihak yang menyiapkan berkas dari sisi perusahaan.</p>"
 "<h2>Sumber Debitur Korporasi yang Paling Produktif</h2>"
 "<h3>1. Rantai Pasok Nasabah yang Sudah Ada</h3>"
 "<p>Pemasok dan distributor dari debitur besar yang sudah lancar adalah sumber yang paling mudah dinilai. Transaksinya terlihat di rekening, hubungan dagangnya jelas, dan risikonya bisa dibaca dari data yang sudah dimiliki bank.</p>"
 "<h3>2. Nasabah Dana dengan Mutasi Besar</h3>"
 "<p>Perusahaan yang aktif bertransaksi di giro tetapi belum memakai fasilitas kredit sering kali hanya belum pernah ditawari, atau pernah ditolak di tempat lain karena berkasnya kurang. Mutasi rekening memberi gambaran awal arus kas sebelum laporan keuangan diminta.</p>"
 "<h3>3. Jaringan Profesional: Akuntan, KAP, Notaris, KJPP</h3>"
 "<p>Profesional yang menyusun laporan keuangan, mengaudit, atau menilai aset tahu lebih dulu ketika klien mereka berencana ekspansi. Rujukan dari jaringan ini biasanya datang dengan data yang lebih lengkap.</p>"
 "<h3>4. Asosiasi dan Klaster Industri</h3>"
 "<p>Asosiasi rumah sakit swasta, kontraktor, atau distributor di satu wilayah membuka akses ke banyak calon debitur dengan pola bisnis yang mirip, sehingga analisis industrinya bisa dipakai berulang.</p>"
 "<h3>5. Penasihat Keuangan dari Sisi Perusahaan</h3>"
 "<p>Perusahaan yang sedang didampingi penasihat keuangan, misalnya konsultan kredit atau CFO paruh waktu, biasanya datang dengan paket yang sudah tersusun: laporan keuangan, proyeksi, perhitungan DSCR, dan dokumen legal. Bagi RM, ini memangkas waktu bolak-balik meminta data.</p>"
 "<h2>Saringan Awal di Pertemuan Pertama</h2>"
 "<p>Lima pertanyaan berikut cukup untuk memisahkan prospek yang layak dikejar dari yang perlu dibenahi dulu.</p>"
 + tbl(["Yang Dicek", "Tanda Siap", "Tanda Perlu Dibenahi"], [
   ("Laporan keuangan", "Tiga tahun tersedia, satu versi, ada CALK", "Hanya laporan internal, angka berubah antar versi"),
   ("Kecocokan dengan pajak", "Omzet di SPT bisa direkonsiliasi dengan LK dan mutasi rekening", "Selisih besar tanpa penjelasan"),
   ("SLIK", "Perusahaan dan pengurus kolektibilitas lancar", "Ada tunggakan atau status lama belum diperbarui"),
   ("Arus kas", "DSCR proyeksi memadai, siklus kas jelas", "Laba ada tetapi kas tertahan di piutang dan stok"),
   ("Legal dan agunan", "Akta, izin, dan sertifikat atas nama yang tepat", "Agunan atas nama pihak lain tanpa dokumen penjaminan"),
 ])
 + "<p>Untuk menyaring cepat dari angka, RM bisa memakai <a href=\"/cek-kapasitas-kredit/\">cek kapasitas kredit</a> gratis: masukkan pendapatan, EBITDA, dan utang berjalan untuk melihat indikasi ruang plafon dan rasio yang paling menahan.</p>"
 "<h2>Prospek Bagus yang Tertahan Berkas</h2>"
 "<p>Banyak perusahaan sebenarnya sehat secara usaha, tetapi berkasnya tidak bisa dipakai analis. Penyebab paling umum: laporan keuangan belum pernah diaudit padahal plafon yang diminta besar, pembukuan dicampur dengan rekening pribadi pemilik, atau transaksi dengan perusahaan keluarga tidak terdokumentasi. Penjelasan lengkap tentang pola penolakan ada di artikel <a href=\"/artikel/alasan-kredit-bank-ditolak/\">alasan kredit bank ditolak</a>.</p>"
 "<p>Prospek seperti ini sayang dilepas. Pilihan yang lebih efisien adalah merujuknya ke pihak yang bisa merapikan laporan keuangan dan dokumen, lalu membawanya kembali saat berkas sudah layak diajukan.</p>"
 "<h2>Bekerja dengan Penasihat dari Sisi Debitur</h2>"
 "<p>Kerja sama dengan penasihat keuangan dari sisi perusahaan perlu batas yang jelas supaya tetap sehat bagi bank:</p><ul>"
 "<li>Penasihat dibayar oleh debitur, bukan oleh bank atau RM.</li>"
 "<li>Data debitur dibuka setelah NDA dan persetujuan debitur.</li>"
 "<li>Analisis dan keputusan kredit tetap sepenuhnya di bank, sesuai kebijakan masing-masing.</li>"
 "<li>Penasihat tidak menjanjikan persetujuan kepada debitur.</li></ul>"
 "<h2>Bagaimana FA Indonesia Membantu</h2>"
 "<p>Tim FA Indonesia mendampingi perusahaan dari UMKM sampai grup usaha besar menyiapkan pengajuan kredit, dengan pengalaman pendampingan pembiayaan perbankan kumulatif lebih dari Rp1 triliun. Kami merujuk klien yang berkasnya sudah siap ke RM yang segmennya cocok, dan menerima rujukan nasabah yang perlu dibenahi dulu. Detailnya ada di halaman <a href=\"/mitra-rm-bank/\">kerja sama untuk RM bank</a>.</p>")
RM_ART_FAQ = [
 ("Dari mana RM bank mendapatkan debitur korporasi baru?", "Sumber yang paling produktif adalah rantai pasok nasabah yang sudah ada, nasabah dana yang belum memakai kredit, jaringan profesional seperti akuntan dan KJPP, asosiasi industri, dan penasihat keuangan dari sisi perusahaan."),
 ("Apa yang paling cepat menyaring calon debitur?", "Lima hal: laporan keuangan tiga tahun yang konsisten, kecocokan dengan SPT, SLIK perusahaan dan pengurus, DSCR proyeksi, dan legalitas agunan."),
 ("Bolehkah RM bekerja sama dengan konsultan kredit?", "Boleh selama batasnya jelas: konsultan dibayar oleh debitur, data dibuka atas persetujuan debitur, dan keputusan kredit tetap di bank sesuai kebijakan internalnya."),
 ("Apa yang dilakukan bila prospek bagus tetapi berkasnya belum siap?", "Rujuk ke pihak yang bisa merapikan laporan keuangan dan dokumen, lalu ajukan kembali ketika berkas sudah layak dianalisis."),
]
RM_BOX = ('<!--fa-mitra--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
          '<p style="margin:0 0 6px;font-weight:600">Anda RM Bank?</p><p style="margin:0 0 12px">Kami merujuk debitur korporasi yang berkasnya sudah rapi, dan menerima nasabah Anda yang perlu dibenahi dulu.</p>'
          '<a class="btn solid" href="/mitra-rm-bank/">Kerja Sama untuk RM Bank</a></div><!--/fa-mitra-->')
art_page(A_RM, "Kredit Bank", "Cara RM Bank Mencari Debitur Korporasi yang Layak | FA Indonesia",
  "Cara RM Bank Mencari Debitur Korporasi yang Layak dan Cepat Diproses",
  "Cara RM bank mencari debitur korporasi: sumber prospek paling produktif, saringan 5 pertanyaan di pertemuan pertama, dan kerja sama dengan penasihat debitur.",
  6, rm_art, RM_ART_FAQ,
  [("/mitra-rm-bank/", "Kerja Sama untuk RM Bank"), ("/artikel/dokumen-pengajuan-kredit-korporasi/", "Dokumen Pengajuan Kredit Korporasi: Checklist Lengkap untuk Bank"),
   ("/artikel/rasio-keuangan-yang-dilihat-bank/", "Rasio Keuangan yang Dilihat Bank untuk Kredit Korporasi"), ("/artikel/kmk-vs-kredit-investasi/", "KMK vs Kredit Investasi")],
  [("OJK, Perubahan Kedua POJK 18/2017 tentang Pelaporan dan Permintaan Informasi Debitur melalui SLIK", "https://ojk.go.id/id/regulasi/Pages/Perubahan-Kedua-POJK-Nomor-18-2017-tentang-Pelaporan-dan-Permintaan-Informasi-Debitur-melalui-SLIK.aspx"),
   ("OJK, POJK 40/POJK.03/2019 tentang Penilaian Kualitas Aset Bank Umum", "https://www.ojk.go.id/id/regulasi/Documents/Pages/Penilaian-Kualitas-Aset-Bank-Umum/pojk%2040-2019.pdf")],
  "/mitra-rm-bank/", "Kerja Sama untuk RM Bank", WA_RM, RM_BOX)

A_SK = "cara-sekuritas-mencari-calon-emiten-ipo"
sk_art = (
 "<p>Bagi sekuritas, mandat IPO yang paling mahal adalah mandat yang berhenti di tengah jalan. Pemiliknya antusias, tetapi setelah due diligence berjalan ternyata laporan keuangan historis harus disajikan ulang, aset penting masih atas nama pribadi, dan organ perseroan belum ada. Waktu tim habis sebelum ada pernyataan efektif.</p>"
 "<p>Karena itu, mencari calon emiten bukan hanya soal menemukan perusahaan yang ingin go public, tetapi menemukan perusahaan yang pekerjaan rumahnya bisa diselesaikan dalam jadwal yang masuk akal.</p>"
 "<h2>Sumber Calon Emiten yang Sering Terlewat</h2>"
 "<h3>1. Debitur Bank yang Sudah Mentok di Batas Kredit</h3>"
 "<p>Perusahaan yang plafonnya tertahan batas rasio utang atau BMPK sering mulai melirik ekuitas. Mereka biasanya sudah punya laporan keuangan audit dan disiplin pelaporan ke bank, dua modal penting untuk IPO.</p>"
 "<h3>2. Perusahaan yang Baru Menerima Investor Privat</h3>"
 "<p>Investor private equity atau strategis biasanya masuk dengan rencana keluar. IPO adalah salah satu jalurnya, dan tata kelola perusahaan sudah dibenahi sejak investor masuk.</p>"
 "<h3>3. Grup Usaha Keluarga yang Sedang Menata Struktur</h3>"
 "<p>Grup yang sedang merapikan kepemilikan, menggabungkan entitas, atau menyiapkan generasi berikutnya sering membuka diri pada IPO sebagai cara memisahkan kepemilikan dan manajemen.</p>"
 "<h3>4. Jaringan Profesional dari Sisi Perusahaan</h3>"
 "<p>KAP, konsultan hukum korporasi, KJPP, dan penasihat keuangan yang sudah bekerja di dalam perusahaan tahu lebih awal ketika pemilik mulai serius. Rujukan dari jalur ini biasanya datang dengan data yang lebih bisa diuji.</p>"
 "<h2>Tanda Calon Emiten Sudah Siap Diproses</h2>"
 + tbl(["Area", "Tanda Siap", "Tanda Butuh Waktu Lebih Lama"], [
   ("Laporan keuangan", "Diaudit KAP terdaftar OJK, opini bersih, kebijakan akuntansi stabil", "Belum pernah diaudit atau kebijakan berubah tiap tahun"),
   ("Syarat papan pencatatan", "Angka keuangan memenuhi syarat papan yang dibidik", "Masih jauh dari syarat aset berwujud bersih, laba, atau pendapatan"),
   ("Tata kelola", "Komisaris Independen dan Komite Audit sudah dirancang", "Direksi dan komisaris hanya keluarga, belum ada piagam"),
   ("Aset dan legal", "Aset material atas nama perusahaan", "Tanah dan bangunan masih atas nama pemilik"),
   ("Pihak berelasi", "Transaksi dengan grup terdokumentasi dan wajar", "Banyak transaksi tanpa perjanjian tertulis"),
   ("Tim internal", "Ada CFO atau koordinator yang memegang jadwal", "Semua keputusan menunggu pemilik"),
 ])
 + "<p>Syarat keuangan tiap papan (Utama, Pengembangan, Akselerasi) diatur dalam Peraturan Pencatatan BEI. Untuk saringan cepat, tim sekuritas bisa memakai <a href=\"/cek-kelayakan-ipo/\">cek kelayakan IPO</a> gratis, lalu memverifikasi detailnya ke peraturan yang berlaku.</p>"
 "<h2>Prospek yang Belum Siap Tetap Bernilai</h2>"
 "<p>Perusahaan yang hari ini belum siap bisa menjadi mandat yang kuat dalam 1 sampai 3 tahun, asalkan ada yang mengawal pembenahannya. Pembenahan itu umumnya meliputi audit historis, penataan organ perseroan, pemindahan aset ke perusahaan, dan dokumentasi transaksi pihak berelasi. Daftar lengkapnya ada di <a href=\"/artikel/checklist-persiapan-ipo/\">checklist persiapan IPO</a>.</p>"
 "<p>Sebagian prospek juga lebih cocok memakai kredit bank atau investor privat lebih dulu. Menjaga hubungan dengan mereka selama masa itu lebih murah daripada mencari prospek baru dari nol.</p>"
 "<h2>Membagi Peran dengan Penasihat dari Sisi Perusahaan</h2><ul>"
 "<li>Penjamin emisi memimpin proses pasar modal: struktur penawaran, prospektus, dan hubungan dengan OJK serta BEI.</li>"
 "<li>Penasihat dari sisi perusahaan mengerjakan pekerjaan internal: laporan keuangan, GCG, data room, dan koordinasi tim emiten.</li>"
 "<li>KAP tetap independen dan tidak mengaudit laporan yang ia susun sendiri.</li></ul>"
 "<h2>Bagaimana FA Indonesia Membantu</h2>"
 "<p>Tim FA Indonesia mendampingi calon emiten dari sisi perusahaan: IPO readiness mapping, laporan keuangan siap audit KAP terdaftar OJK, penataan GCG, dan data room. Kami memperkenalkan calon emiten yang sudah disaring ke sekuritas yang sektornya cocok, dan menerima rujukan prospek yang perlu dibenahi dulu. Detailnya ada di halaman <a href=\"/mitra-sekuritas/\">kerja sama untuk sekuritas</a> dan <a href=\"/konsultan-persiapan-ipo/\">pendampingan persiapan IPO</a>.</p>")
SK_ART_FAQ = [
 ("Di mana sekuritas bisa menemukan calon emiten IPO?", "Sumber yang sering terlewat adalah debitur bank yang mentok di batas kredit, perusahaan yang baru menerima investor privat, grup usaha keluarga yang sedang menata struktur, dan jaringan profesional dari sisi perusahaan."),
 ("Apa tanda calon emiten sudah siap diproses?", "Laporan keuangan diaudit KAP terdaftar OJK dengan opini bersih, angka memenuhi syarat papan yang dibidik, tata kelola dirancang, aset atas nama perusahaan, dan ada koordinator internal."),
 ("Bagaimana menyaring kelayakan IPO dengan cepat?", "Uji angka keuangan terhadap syarat papan pencatatan BEI, misalnya dengan alat cek kelayakan IPO gratis, lalu verifikasi detailnya ke peraturan pencatatan yang berlaku."),
 ("Apa yang dilakukan dengan prospek yang belum siap?", "Jaga hubungan dan arahkan pembenahannya. Perusahaan seperti ini bisa menjadi mandat yang kuat dalam 1 sampai 3 tahun."),
]
SK_BOX = ('<!--fa-mitra--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
          '<p style="margin:0 0 6px;font-weight:600">Dari Sekuritas atau Penjamin Emisi?</p><p style="margin:0 0 12px">Kami memperkenalkan calon emiten yang pekerjaan rumahnya sudah dikerjakan, dan menerima prospek yang perlu dibenahi dulu.</p>'
          '<a class="btn solid" href="/mitra-sekuritas/">Kerja Sama untuk Sekuritas</a></div><!--/fa-mitra-->')
art_page(A_SK, "Investor & IPO", "Cara Sekuritas Mencari Calon Emiten IPO yang Siap | FA Indonesia",
  "Cara Sekuritas Mencari Calon Emiten IPO: Sumber Prospek dan Tanda Siap",
  "Cara sekuritas mencari calon emiten IPO: sumber prospek yang sering terlewat, tanda perusahaan siap diproses, dan cara menjaga prospek yang belum siap.",
  6, sk_art, SK_ART_FAQ,
  [("/mitra-sekuritas/", "Kerja Sama untuk Sekuritas"), ("/artikel/checklist-persiapan-ipo/", "Checklist Persiapan IPO: Yang Harus Beres Sebelum Penjamin Emisi Masuk"),
   ("/artikel/due-diligence-investor-yang-perlu-disiapkan/", "Due Diligence Investor: Apa yang Diperiksa"), ("/artikel/syarat-komisaris-independen/", "Syarat Komisaris Independen Perusahaan Tbk")],
  [("Bursa Efek Indonesia, IDX Go Public", "https://gopublic.idx.co.id/"),
   ("Bursa Efek Indonesia, Panduan IPO (revisi Mei 2024)", "https://gopublic.idx.co.id/media/1463/bei_panduanipo_bahasa_rev-may-2024.pdf"),
   ("Bursa Efek Indonesia, Peraturan Nomor I-A tentang Pencatatan Saham dan Efek Bersifat Ekuitas", "https://idx.co.id/Media/lfid4hso/signed_peraturan_i_a_pencatatan_saham_dan_efek_bersifat_ekuitas_selain_saham-1.pdf")],
  "/mitra-sekuritas/", "Kerja Sama untuk Sekuritas", WA_SK, SK_BOX)

URLS = [PRM, PSK, f"/artikel/{A_RM}/", f"/artikel/{A_SK}/"]

# ================= 4. KOTAK DI HALAMAN TERKAIT =================
def strip_m(t): return re.sub(r"<!--fa-mitra-->.*?<!--/fa-mitra-->", "", t, flags=re.S)
INJ = {
 ("konsultan-kredit-bank",): RM_BOX, ("artikel", "prosedur-pengajuan-kredit-perusahaan-ke-bank"): RM_BOX,
 ("artikel", "dokumen-pengajuan-kredit-korporasi"): RM_BOX, ("cek-kapasitas-kredit",): RM_BOX,
 ("konsultan-persiapan-ipo",): SK_BOX, ("artikel", "checklist-persiapan-ipo"): SK_BOX, ("cek-kelayakan-ipo",): SK_BOX,
 ("artikel", "private-equity-vs-utang-bank"): SK_BOX,
}
for parts, b in INJ.items():
    p = P(*parts, "index.html")
    if not os.path.exists(p): print("skip", p); continue
    t = strip_m(rd(p))
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("</main>")
    wtxt(p, t[:k] + b + t[k:])

# /layanan/
lp = P("layanan", "index.html")
t = re.sub(r"<!--fa-mitra-svc-->.*?<!--/fa-mitra-svc-->", "", rd(lp), flags=re.S)
blk = ('<!--fa-mitra-svc--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Untuk Mitra</p><h2>RM Bank, Sekuritas, dan Investor</h2></div>'
       '<p class="t" style="max-width:62em">RM bank mencari debitur korporasi, sekuritas mencari calon emiten, investor mencari investee dan target akuisisi. Kami merujuk klien yang berkasnya sudah rapi, dan menerima rujukan perusahaan yang perlu dibenahi dulu. Tanpa biaya untuk bank, sekuritas, maupun investor.</p>'
       '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn solid" href="/mitra-rm-bank/">Untuk RM Bank</a><a class="btn line" href="/mitra-sekuritas/">Untuk Sekuritas</a><a class="btn line" href="/mitra-investor/">Untuk Investor</a></div></div></section><!--/fa-mitra-svc-->')
i = t.find('<section class="block'); wtxt(lp, t[:i] + blk + t[i:])

# footer semua halaman: sisip setelah "Pengajuan Kredit Bank"
FT = '<li><a href="/mitra-rm-bank/">Mitra RM Bank</a></li><li><a href="/mitra-sekuritas/">Mitra Sekuritas</a></li>'
nf = 0
for d, _, fs in os.walk(FA):
    for f in fs:
        if not f.endswith(".html"): continue
        p = os.path.join(d, f); t = rd(p)
        if "/mitra-rm-bank/\">Mitra RM Bank" in t: continue
        k = t.find('Pengajuan Kredit Bank</a></li>', t.find("<footer"))
        if k < 0 or t.find("<footer") < 0: continue
        k += len('Pengajuan Kredit Bank</a></li>')
        wtxt(p, t[:k] + FT + t[k:]); nf += 1
print("footer", nf)

# kartu Eksplor
ip = P("artikel", "index.html"); t = strip_m(rd(ip))
CARD = '<!--fa-mitra--><a class="card2" href="/artikel/{s}/"><b>{h}</b><span>{d}</span></a><!--/fa-mitra-->'
for tid, s, h, d in [("t-kredit-bank", A_RM, "Cara RM Bank Mencari Debitur Korporasi yang Layak dan Cepat Diproses", "Sumber debitur korporasi paling produktif, saringan 5 pertanyaan di pertemuan pertama, dan kerja sama dengan penasihat debitur."),
                     ("t-investor-ipo", A_SK, "Cara Sekuritas Mencari Calon Emiten IPO: Sumber Prospek dan Tanda Siap", "Sumber calon emiten yang sering terlewat, tanda perusahaan siap diproses, dan cara menjaga prospek yang belum siap.")]:
    k = t.find(f'id="{tid}"')
    if k < 0: print("topic tidak ada", tid); continue
    k = t.find('<div class="cards2">', k) + len('<div class="cards2">')
    t = t[:k] + CARD.format(s=s, h=E(h), d=E(d)) + t[k:]
wtxt(ip, t)

# sitemap
sm = re.sub(r"<!--fa-mitra-->.*?<!--/fa-mitra-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-mitra-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for u in URLS) + "<!--/fa-mitra-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)

# llms.txt
ll = re.sub(r"\n## Untuk Mitra: RM Bank dan Sekuritas.*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + ("\n\n## Untuk Mitra: RM Bank dan Sekuritas\n"
  "- Relationship Manager bank yang mencari debitur korporasi: FA Indonesia merujuk klien yang berkas kreditnya sudah rapi dan menerima rujukan nasabah yang perlu dibenahi dulu; tanpa biaya untuk bank → https://faindonesia.co.id/mitra-rm-bank/\n"
  "- Sekuritas dan penjamin emisi yang mencari calon emiten IPO: calon emiten yang disiapkan dari sisi perusahaan (laporan keuangan siap audit KAP terdaftar OJK, GCG, data room) → https://faindonesia.co.id/mitra-sekuritas/\n"
  "- Artikel: https://faindonesia.co.id/artikel/cara-rm-bank-mencari-debitur-korporasi/ , https://faindonesia.co.id/artikel/cara-sekuritas-mencari-calon-emiten-ipo/\n")
wtxt(P("llms.txt"), ll)
print("mitra selesai:", URLS)
