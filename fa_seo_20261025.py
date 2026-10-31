# -*- coding: utf-8 -*-
"""SEO push FA Indonesia (25 Okt 2026):
- 30 artikel baru dari fa_content/articles/*.json -> /artikel/<slug>/ + kartu per topik di Eksplor
- Layanan baru: /konsultan-rumah-sakit/, /konsultan-unit-cost-rumah-sakit/ (+ versi per kota)
- Halaman lokal: /wilayah/, /wilayah/<kota>/, /wilayah/<kota>/<kawasan>/ (kota & kawasan sama dengan cariakuntan)
- sitemap, llms.txt, link footer
Idempoten: halaman hasil generate ditimpa, blok sisipan memakai penanda komentar.
"""
import os, re, json, glob, html, sys, unicodedata
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
sys.path.insert(0, os.path.join(HERE, "cariakuntan"))
from cities import CITIES, REGIONS
from kawasan import KAWASAN, BOOST

D = "https://faindonesia.co.id"
WA = "https://wa.me/6282245260121?text="
TODAY = "2026-10-25"
def P(*a): return os.path.join(FA, *a)
def rd(p): return open(p, encoding="utf-8").read()
def wr(rel, s):
    p = P(*rel.strip("/").split("/"), "index.html") if not rel.endswith(".html") else P(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(s)
def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")
E = html.escape
def wa(msg): return WA + quote(msg)

EXTRA_CSS = ('<style id="fa-seo">.art p.eyebrow{font-size:12px!important;letter-spacing:.18em}.tblwrap{overflow-x:auto;margin:8px 0 22px;-webkit-overflow-scrolling:touch}.tblwrap table{min-width:560px;margin:0}'
             '.art th{border:1px solid #333;padding:9px 10px;text-align:left;vertical-align:top}.art blockquote{border-left:2px solid #555;margin:0 0 18px;padding:4px 0 4px 16px;color:#cfcfcf}'
             '.chips2{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 18px}.chips2 a{border:1px solid #3a3a3a;border-radius:999px;padding:7px 13px;font-size:13px;color:#fff;text-decoration:none}.chips2 a:hover{border-color:#fff}'
             '.topic{margin:36px 0 0}.topic h2{font-size:clamp(22px,2.6vw,28px);margin:0 0 14px}'
             '.flow5{list-style:none;padding:0;margin:10px 0 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;counter-reset:f}'
             '.flow5 li{border:1px solid #333;border-radius:10px;padding:14px 14px 14px 52px;position:relative;background:#1e1e1e;font-family:Poppins,sans-serif!important;font-size:14px!important;line-height:1.5!important}'
             '.flow5 li:before{counter-increment:f;content:counter(f);position:absolute;left:14px;top:13px;width:26px;height:26px;border-radius:50%;background:#fff;color:#171717;display:grid;place-items:center;font-size:12px;font-weight:600}'
             '.flow5 li b{display:block;font-weight:500;margin-bottom:2px}</style>')

TPL_ART = rd(P("artikel", "checklist-persiapan-ipo", "index.html"))
TPL_SVC = rd(P("konsultan-kredit-bank", "index.html"))
AUTHOR = "Ananta W. Sasongko, CPA, FMVA, FPAP"
PERSON = {"@type": "Person", "@id": D + "/ananta-w-sasongko/#person", "name": AUTHOR, "url": D + "/ananta-w-sasongko/"}
ORG = {"@type": "Organization", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/", "logo": {"@type": "ImageObject", "url": D + "/img/brand/mark-hero.png"}}
BULAN = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]

def set_head(s, title, desc, url, ld, og_type=None):
    s = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', s, count=1)
    for a in ['name="description"', 'property="og:description"']:
        s = re.sub(rf'<meta {a} content="[^"]*">', f'<meta {a} content="{E(desc)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    if og_type: s = re.sub(r'<meta property="og:type" content="[^"]*">', f'<meta property="og:type" content="{og_type}">', s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", s, count=1, flags=re.S)
    s = s.replace("</head>", EXTRA_CSS + "</head>", 1)
    return s

def set_main(s, inner):
    i = s.find('<main id="top">'); j = s.find("</main>")
    return s[:i] + '<main id="top">\n' + inner + "\n" + s[j:]

def faq_html(faq): return "".join(f'<p style="margin:0 0 18px"><b>{E(q)}</b><br>{E(a)}</p>' for q, a in faq)
def faq_ld(faq): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def crumbs(items): return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}
AUTHOR_BOX = re.search(r'<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333.*?</div></div>', TPL_ART, re.S).group(0)

def svc_page(path, eyebrow, h1, lead, body, faq, title, desc, ld_extra, cta_href, cta_label, wa_msg, crumb):
    url = D + path
    ld = {"@context": "https://schema.org", "@graph": ld_extra + [faq_ld(faq), crumbs(crumb)]}
    main = (f'<section class="block">\n<div class="wrap art">\n<p class="eyebrow">{eyebrow}</p>\n'
            f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{E(h1)}</h1>\n'
            f'<p class="t" style="max-width:62em">{lead}</p>\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px"><a class="btn solid" href="{wa(wa_msg)}" rel="noopener" target="_blank">Chat Ananta, CPA</a><a class="btn line" href="{cta_href}">{cta_label}</a></div>\n'
            f'{body}\n<h2>Pertanyaan Umum</h2>\n{faq_html(faq)}\n{AUTHOR_BOX}\n</div>\n</section>')
    s = set_head(TPL_SVC, title, desc, url, ld, "website")
    wr(path, set_main(s, main))
    return path

URLS = []

# ================= 1. ARTIKEL =================
ARTS = []
for f in sorted(glob.glob(os.path.join(HERE, "fa_content", "articles", "*.json"))):
    ARTS.append(json.load(open(f, encoding="utf-8")))
CATS = ["Rumah Sakit", "Kredit Bank", "Audit & KAP", "Penilaian & KJPP", "Laporan Keuangan", "Pajak", "Investor & IPO", "CFO & Tata Kelola"]
by_cat = {c: [a for a in ARTS if a["category"] == c] for c in CATS}
for i, a in enumerate(ARTS):
    url = f"{D}/artikel/{a['slug']}/"
    hh, mm = 8 + (i % 10), (i * 7) % 60
    iso = f"{TODAY}T{hh:02d}:{mm:02d}:00+07:00"
    related = [x for x in by_cat.get(a["category"], []) if x["slug"] != a["slug"]][:4]
    if len(related) < 3: related += [x for x in ARTS if x["slug"] != a["slug"] and x not in related][: 3 - len(related)]
    rel_html = "<h2>Baca Juga</h2><ul>" + "".join(f'<li><a href="/artikel/{x["slug"]}/">{E(x["title"])}</a></li>' for x in related) + "</ul>"
    src_html = ("<h2>Sumber</h2><ul>" + "".join(f'<li><a href="{E(u)}" rel="noopener nofollow" target="_blank">{E(t)}</a></li>' for t, u in a["sources"]) + "</ul>") if a.get("sources") else ""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": a["title"], "description": a["description"], "url": url, "mainEntityOfPage": url, "inLanguage": "id",
         "datePublished": iso, "dateModified": iso, "author": PERSON, "publisher": ORG, "image": D + "/img/og/fa-indonesia-og.jpg", "keywords": a.get("keyword", ""), "articleSection": a["category"]},
        crumbs([("FA Indonesia", D + "/"), ("Eksplor", D + "/artikel/"), (a["title"], url)]), faq_ld(a["faq"])]}
    s = set_head(TPL_ART, a["title"] + " | FA Indonesia", a["description"], url, ld)
    s = re.sub(r'<meta property="article:published_time" content="[^"]*">', f'<meta property="article:published_time" content="{iso}">', s, count=1)
    body = (f'<p class="eyebrow"><a href="/artikel/" style="text-decoration:none">Eksplor · {E(a["category"])}</a></p>\n'
            f'<h1 style="margin:.2em 0 .4em;font-size:clamp(32px,4.4vw,52px);line-height:1.12">{E(a["title"])}</h1>\n'
            f'<p class="meta">Oleh <a href="/ananta-w-sasongko/">{AUTHOR}</a> · 25 Oktober 2026 · {a.get("minutes", 5)} menit baca</p>\n'
            f'{a["body_html"]}\n<h2>Pertanyaan Umum</h2>\n{faq_html(a["faq"])}\n{rel_html}\n{src_html}\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn solid" href="{a["cta"]["href"]}">{E(a["cta"]["label"])}</a><a class="btn line" href="{wa(a["wa"])}" rel="noopener" target="_blank">Chat Ananta, CPA</a><a class="btn line" href="/artikel/">Eksplor Lainnya</a></div>\n'
            f'{AUTHOR_BOX}')
    main = f'<section class="block">\n<div class="wrap art">\n{body}\n</div>\n</section>'
    wr(f"/artikel/{a['slug']}/", set_main(s, main)); URLS.append(f"/artikel/{a['slug']}/")

# kartu per topik di Eksplor
idx = rd(P("artikel", "index.html"))
idx = re.sub(r"<!--fa-seo-cards-->.*?<!--/fa-seo-cards-->", "", idx, flags=re.S)
chips = '<div class="chips2">' + "".join(f'<a href="#t-{slug(c)}">{E(c)}</a>' for c in CATS if by_cat[c]) + '<a href="/wilayah/">Per Kota</a></div>'
topics = "".join(f'<div class="topic" id="t-{slug(c)}"><h2>{E(c)}</h2><div class="cards2">' + "".join(
    f'<a class="card2" href="/artikel/{x["slug"]}/"><b>{E(x["title"])}</b><span>{E(x["description"])}</span></a>' for x in by_cat[c]) + "</div></div>" for c in CATS if by_cat[c])
blk = f'<!--fa-seo-cards-->{chips}{topics}<div class="topic"><h2>Artikel Lainnya</h2></div><!--/fa-seo-cards-->'
# Kartu dasar (artikel di luar fa_content) disimpan di fa_content/eksplor_base_cards.html supaya build berulang
# tidak menghapusnya (fa_rapi memindahkan kartu dasar ke dalam blok topik, lalu blok ini dibuang di build berikutnya).
_bp = os.path.join(HERE, "fa_content", "eksplor_base_cards.html")
_base = open(_bp, encoding="utf-8").read() if os.path.exists(_bp) else ""
idx = re.sub(r'<div class="cards2">(?:(?!</div>).)*</div>', "", idx, flags=re.S)
_ins = blk + '<div class="cards2">' + _base + '</div>'
_k = idx.find('<div style="margin:44px 0 0;max-width:900px', idx.find('<main id="top">'))
if _k < 0: _k = idx.find('</div>\n</section>\n</main>')
idx = idx[:_k] + _ins + idx[_k:]
if 'id="fa-seo"' not in idx: idx = idx.replace("</head>", EXTRA_CSS + "</head>", 1)
open(P("artikel", "index.html"), "w", encoding="utf-8").write(idx)

# ================= 2. LAYANAN RUMAH SAKIT =================
RS_ARTS = [x for x in ARTS if x["category"] == "Rumah Sakit" or "rumah-sakit" in x["slug"]]
def art_list(xs): return "<ul>" + "".join(f'<li><a href="/artikel/{x["slug"]}/">{E(x["title"])}</a></li>' for x in xs) + "</ul>"
def flow(items): return '<ol class="flow5">' + "".join(f"<li><b>{E(t)}</b>{E(d)}</li>" for t, d in items) + "</ol>"
def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
PROVIDER = {"@type": "ProfessionalService", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"}

RS_SVC = [
 ("Studi kelayakan dan rencana ekspansi", "Gedung baru, penambahan tempat tidur, layanan unggulan, atau rumah sakit kedua, dihitung sampai proyeksi arus kas dan kemampuan bayar."),
 ("Kredit bank untuk rumah sakit", "Kredit investasi gedung dan alat kesehatan, kredit modal kerja untuk piutang klaim BPJS, refinancing. Pendampingan sampai dana cair."),
 ("Akuisisi dan divestasi", "Due diligence keuangan, pajak, dan perizinan, valuasi bersama KJPP, struktur transaksi, dan pendampingan negosiasi, dari sisi pembeli maupun penjual."),
 ("Investor dan pendanaan ekuitas", "Information memorandum, financial model, data room, dan pendampingan sampai dana investor masuk."),
 ("Unit cost dan tarif", "Perhitungan biaya satuan per layanan, perbandingan dengan tarif INA-CBG dan tarif umum, rekomendasi tarif."),
 ("Laporan keuangan, audit, dan GCG", "Laporan keuangan sesuai PSAK, persiapan audit pertama, annual report, SOP keuangan, dan struktur tata kelola."),
]
rs_body = ("<h2>Yang Kami Kerjakan untuk Rumah Sakit Swasta</h2>" + "".join(f"<h3>{E(t)}</h3><p>{E(d)}</p>" for t, d in RS_SVC)
  + "<h2>Alur Kerja</h2>" + flow([("Diskusi awal", "Gratis lewat WhatsApp atau video call."), ("Diagnosis", "Baca laporan keuangan, data klaim, dan rencana bisnis."), ("NDA dan kontrak", "Lingkup, jadwal, dan biaya disepakati di depan."), ("Eksekusi", "Dikerjakan tim FA Indonesia bersama mitra profesional sesuai kebutuhan."), ("Hasil", "Kredit cair, investor masuk, transaksi tuntas, atau laporan siap.")])
  + "<h2>Rekam Jejak di Sektor Rumah Sakit</h2><ul><li>Mendampingi akuisisi tiga rumah sakit di Jawa Tengah dari awal sampai tuntas.</li><li>Fasilitas kredit perbankan hingga Rp300 miliar untuk grup rumah sakit swasta.</li><li>Pendanaan investor hingga US$3 juta untuk grup rumah sakit.</li><li>Mandat divestasi rumah sakit yang sedang berjalan.</li><li>Menyusun annual report perdana sebuah rumah sakit BUMN.</li><li>Pengalaman sebagai Direktur Keuangan dan Group CFO rumah sakit.</li></ul>"
  + "<h2>Siapa yang Menangani</h2><p>Setiap klien didampingi tim FA Indonesia. Kami hanya mengambil beberapa klien setiap tahun supaya setiap penugasan benar-benar dikawal.</p>"
  + "<h2>Bacaan untuk Pengelola Rumah Sakit</h2>" + art_list(RS_ARTS)
  + '<h2>Konsultan Rumah Sakit per Kota</h2><p class="t">' + " · ".join(f'<a href="/konsultan-rumah-sakit/{slug(c[0])}/">{c[0]}</a>' for c in CITIES) + "</p>")
RS_FAQ = [
 ("Apa yang dikerjakan konsultan rumah sakit swasta?", "Untuk sisi keuangan dan bisnis: studi kelayakan ekspansi, kredit bank, akuisisi dan divestasi, pencarian investor, unit cost dan tarif, laporan keuangan dan audit, serta tata kelola."),
 ("Apakah FA Indonesia melayani rumah sakit di luar Jawa Timur?", "Ya. Kami melayani rumah sakit dan klinik di seluruh Indonesia, dengan diskusi daring dan kunjungan lapangan terjadwal."),
 ("Berapa biaya konsultan rumah sakit?", "Bergantung pada lingkup. Untuk pendampingan pendanaan umumnya berupa retainer bulanan ditambah success fee saat dana cair. Angka pastinya disampaikan setelah diskusi awal, sebelum Anda berkomitmen."),
 ("Apakah bisa membantu menjual atau membeli rumah sakit?", "Bisa. Kami mendampingi dari sisi pembeli maupun penjual: due diligence, valuasi bersama KJPP, struktur transaksi, sampai penandatanganan."),
]
svc_page("/konsultan-rumah-sakit/", "Layanan · Rumah Sakit", "Konsultan Rumah Sakit Swasta: Ekspansi, Kredit, Akuisisi, dan Unit Cost",
  "Pendampingan keuangan dan bisnis untuk rumah sakit dan klinik swasta: dari studi kelayakan, kredit bank, investor, akuisisi, sampai unit cost dan tarif. Ditangani tim yang berpengalaman di keuangan rumah sakit.",
  rs_body, RS_FAQ, "Konsultan Rumah Sakit Swasta: Kredit, Akuisisi, Unit Cost | FA Indonesia",
  "Konsultan rumah sakit swasta untuk ekspansi, kredit bank, akuisisi, investor, unit cost, dan tarif. Ditangani tim yang berpengalaman di keuangan rumah sakit. Seluruh Indonesia.",
  [{"@type": "Service", "name": "Konsultan Rumah Sakit Swasta", "serviceType": "Hospital financial advisory", "provider": PROVIDER, "areaServed": {"@type": "Country", "name": "Indonesia"}, "url": D + "/konsultan-rumah-sakit/"}],
  "/konsultan-unit-cost-rumah-sakit/", "Unit Cost Rumah Sakit", "Halo FA Indonesia, saya ingin konsultasi untuk rumah sakit kami.",
  [("FA Indonesia", D + "/"), ("Layanan", D + "/layanan/"), ("Konsultan Rumah Sakit", D + "/konsultan-rumah-sakit/")]); URLS.append("/konsultan-rumah-sakit/")

UC_ROWS = [("Rawat inap", "Biaya per hari rawat per kelas, termasuk visite dan asuhan keperawatan"), ("Rawat jalan", "Biaya per kunjungan per poliklinik"), ("Tindakan dan operasi", "Biaya per tindakan sesuai kelompok tindakan dan durasi kamar operasi"),
           ("Penunjang", "Biaya per pemeriksaan laboratorium dan radiologi"), ("Farmasi", "Biaya layanan farmasi di luar harga obat"), ("Paket JKN", "Biaya per kasus dibanding tarif INA-CBG per kelompok kasus")]
uc_body = ("<h2>Kenapa Unit Cost Penting</h2><p>Tanpa unit cost, tarif umum ditetapkan dengan menyalin pesaing, dan kerugian per kasus JKN baru terlihat di akhir tahun. Unit cost menunjukkan layanan mana yang menutup biaya, mana yang perlu diefisienkan, dan berapa tarif yang wajar untuk pasien umum dan asuransi.</p>"
  + "<h2>Output yang Anda Terima</h2>" + tbl(["Layanan", "Unit cost yang dihitung"], UC_ROWS)
  + "<ul><li>Model Excel yang bisa diperbarui sendiri tiap tahun, lengkap dengan peta pusat biaya dan dasar alokasi.</li><li>Analisis margin per layanan dan per kelompok kasus JKN.</li><li>Rekomendasi tarif umum dan prioritas efisiensi.</li><li>Presentasi untuk direksi dan pemilik.</li></ul>"
  + "<h2>Metodologi</h2>" + flow([("Peta pusat biaya", "Unit penunjang dan unit produksi dipisahkan."), ("Data biaya", "Laporan keuangan, gaji, penyusutan, dan pemakaian bahan."), ("Alokasi", "Distribusi ganda atau activity-based costing."), ("Volume layanan", "Hari rawat, kunjungan, tindakan, pemeriksaan."), ("Unit cost dan tarif", "Biaya satuan, margin, dan rekomendasi tarif.")])
  + "<p>Perhitungan memakai data rumah sakit Anda sendiri, bukan angka rata-rata. Waktu pengerjaan umumnya 4 sampai 8 minggu, bergantung pada kerapian data biaya dan statistik layanan.</p>"
  + "<h2>Bacaan Terkait</h2>" + art_list([x for x in ARTS if "unit-cost" in x["slug"] or "tarif" in x["slug"]] + [x for x in ARTS if x["slug"] == "laporan-keuangan-rumah-sakit-swasta-sesuai-psak"])
  + '<h2>Konsultan Unit Cost per Kota</h2><p class="t">' + " · ".join(f'<a href="/konsultan-unit-cost-rumah-sakit/{slug(c[0])}/">{c[0]}</a>' for c in CITIES) + "</p>")
UC_FAQ = [
 ("Apa itu unit cost rumah sakit?", "Biaya satuan untuk menghasilkan satu unit layanan, misalnya satu hari rawat inap kelas tertentu, satu kunjungan poliklinik, atau satu tindakan. Dihitung dengan mengalokasikan biaya unit penunjang ke unit produksi."),
 ("Metode apa yang dipakai untuk menghitung unit cost?", "Umumnya metode distribusi ganda (double distribution) untuk alokasi biaya penunjang, dan activity-based costing untuk layanan yang aktivitasnya beragam. Pilihannya disesuaikan dengan ketersediaan data."),
 ("Berapa lama menghitung unit cost rumah sakit?", "Umumnya 4 sampai 8 minggu, bergantung pada kerapian data biaya dan statistik layanan."),
 ("Apakah hasilnya bisa dipakai untuk menetapkan tarif?", "Bisa. Unit cost menjadi dasar tarif umum dan bahan evaluasi margin terhadap tarif INA-CBG, tanpa melanggar ketentuan tarif JKN yang berlaku."),
]
svc_page("/konsultan-unit-cost-rumah-sakit/", "Layanan · Rumah Sakit", "Konsultan Unit Cost Rumah Sakit dan Klinik: Biaya Satuan sampai Tarif",
  "Perhitungan unit cost per layanan untuk rumah sakit dan klinik swasta, analisis margin terhadap tarif INA-CBG, dan rekomendasi tarif. Hasilnya model Excel yang bisa Anda perbarui sendiri.",
  uc_body, UC_FAQ, "Konsultan Unit Cost Rumah Sakit & Klinik, Tarif INA-CBG | FA Indonesia",
  "Konsultan unit cost rumah sakit dan klinik: biaya satuan rawat inap, rawat jalan, tindakan, penunjang, margin JKN, dan rekomendasi tarif. Seluruh Indonesia.",
  [{"@type": "Service", "name": "Konsultan Unit Cost Rumah Sakit", "serviceType": "Hospital unit cost analysis", "provider": PROVIDER, "areaServed": {"@type": "Country", "name": "Indonesia"}, "url": D + "/konsultan-unit-cost-rumah-sakit/"}],
  "/konsultan-rumah-sakit/", "Konsultan Rumah Sakit", "Halo FA Indonesia, saya ingin konsultasi unit cost rumah sakit kami.",
  [("FA Indonesia", D + "/"), ("Layanan", D + "/layanan/"), ("Unit Cost Rumah Sakit", D + "/konsultan-unit-cost-rumah-sakit/")]); URLS.append("/konsultan-unit-cost-rumah-sakit/")

# ================= 3. PER KOTA =================
KW_BY = {}
for k in KAWASAN: KW_BY.setdefault(k[1], []).append(k)
SECT_TXT = {"kesehatan": "rumah sakit dan klinik", "manufaktur": "pabrik dan manufaktur", "dagang": "perdagangan dan distribusi", "properti": "pengembang properti", "konstruksi": "kontraktor",
            "logistik": "logistik dan ekspedisi", "wisata": "hotel dan pariwisata", "pendidikan": "yayasan pendidikan", "bpr": "BPR dan koperasi", "sawit": "perkebunan", "tambang": "jasa tambang",
            "migas": "penunjang migas", "perikanan": "perikanan", "smelter": "pemasok kawasan smelter", "bumd": "BUMD"}
def sect(secs): return ", ".join(SECT_TXT.get(x, x) for x in secs[:4])
def near(c):
    return [x for x in CITIES if x[2] == c[2] and x[0] != c[0]][:8]

for c in CITIES:
    name, prov, reg, secs, note = c
    cs = slug(name); rname, rline = REGIONS[reg]
    ca = f"https://cariakuntan.com/kota/{cs}/"
    nb = near(c)
    # --- konsultan rumah sakit per kota ---
    for kind in ["rs", "uc"]:
        if kind == "rs":
            path = f"/konsultan-rumah-sakit/{cs}/"; h1 = f"Konsultan Rumah Sakit di {name}"
            lead = f"Pendampingan keuangan dan bisnis untuk rumah sakit dan klinik swasta di {name}, {prov}: ekspansi, kredit bank, akuisisi, investor, unit cost, dan tarif. Dikerjakan bersama tim CA dan CPA FA Indonesia."
            title = f"Konsultan Rumah Sakit {name}: Kredit, Akuisisi, Unit Cost | FA Indonesia"
            desc = f"Konsultan rumah sakit swasta di {name}, {prov}: studi kelayakan, kredit bank, akuisisi dan divestasi, investor, unit cost dan tarif. Konsultasi awal gratis."
            items = RS_SVC; other = (f"/konsultan-unit-cost-rumah-sakit/{cs}/", f"Unit Cost Rumah Sakit {name}"); base = "/konsultan-rumah-sakit/"
            faq = [(f"Adakah konsultan rumah sakit swasta di {name}?", f"FA Indonesia melayani rumah sakit dan klinik di {name} dan sekitarnya untuk ekspansi, kredit bank, akuisisi, investor, unit cost, dan tarif, dengan diskusi daring dan kunjungan terjadwal."),
                   (f"Bisakah rumah sakit di {name} dibantu mengajukan kredit bank?", "Bisa. Kami siapkan laporan keuangan, proyeksi, dan paket kredit untuk kredit investasi gedung dan alat kesehatan atau modal kerja klaim BPJS, lalu dampingi sampai dana cair."),
                   RS_FAQ[2]]
        else:
            path = f"/konsultan-unit-cost-rumah-sakit/{cs}/"; h1 = f"Konsultan Unit Cost Rumah Sakit di {name}"
            lead = f"Perhitungan unit cost per layanan untuk rumah sakit dan klinik di {name}, {prov}, analisis margin terhadap tarif INA-CBG, dan rekomendasi tarif umum."
            title = f"Konsultan Unit Cost Rumah Sakit & Klinik {name} | FA Indonesia"
            desc = f"Hitung unit cost rumah sakit dan klinik di {name}: rawat inap, rawat jalan, tindakan, penunjang, margin JKN, dan rekomendasi tarif. Konsultasi awal gratis."
            items = [(a, b) for a, b in UC_ROWS]; other = (f"/konsultan-rumah-sakit/{cs}/", f"Konsultan Rumah Sakit {name}"); base = "/konsultan-unit-cost-rumah-sakit/"
            faq = [(f"Siapa yang bisa menghitung unit cost rumah sakit di {name}?", f"FA Indonesia menghitung unit cost untuk rumah sakit dan klinik di {name} memakai data biaya dan statistik layanan rumah sakit sendiri, dengan metode distribusi ganda atau activity-based costing."),
                   UC_FAQ[2], UC_FAQ[3]]
        body = (f"<h2>{'Layanan untuk Rumah Sakit di ' + name if kind=='rs' else 'Unit Cost yang Dihitung'}</h2>"
                + ("".join(f"<h3>{E(t)}</h3><p>{E(d)}</p>" for t, d in items) if kind == "rs" else tbl(["Layanan", "Unit cost yang dihitung"], items))
                + f"<h2>Konteks {name}</h2><p>{name} adalah {note}. Sektor yang aktif antara lain {sect(secs)}. {rline}</p>"
                + ("".join(f"<p>{E(x)}</p>" for x in BOOST.get(name, [])[:1]))
                + "<h2>Rekam Jejak</h2><ul><li>Mendampingi akuisisi tiga rumah sakit di Jawa Tengah.</li><li>Fasilitas kredit hingga Rp300 miliar untuk grup rumah sakit swasta.</li><li>Pendanaan investor hingga US$3 juta untuk grup rumah sakit.</li></ul>"
                + "<h2>Bacaan Terkait</h2>" + art_list(RS_ARTS[:5])
                + f'<h2>Kota Sekitar</h2><p class="t">' + " · ".join(f'<a href="{base}{slug(x[0])}/">{x[0]}</a>' for x in nb) + "</p>"
                + f'<p class="t">Butuh KAP, KJPP, atau konsultan pajak untuk rumah sakit di {name}? Cek <a href="{ca}">cariakuntan.com/{name}</a>.</p>')
        svc_page(path, f"Rumah Sakit · {E(name)}", h1, lead, body, faq, title, desc,
                 [{"@type": "Service", "name": h1, "serviceType": h1.split(" di ")[0], "provider": PROVIDER, "areaServed": {"@type": "City", "name": name, "containedInPlace": {"@type": "AdministrativeArea", "name": prov}}, "url": D + path}],
                 other[0], other[1], f"Halo FA Indonesia, saya dari rumah sakit di {name}, ingin konsultasi.",
                 [("FA Indonesia", D + "/"), (h1.split(" di ")[0], D + base), (name, D + path)]); URLS.append(path)

    # --- wilayah kota ---
    kws = KW_BY.get(name, [])
    path = f"/wilayah/{cs}/"
    svcs = [("Persiapan audit KAP", "/jasa-penyusunan-laporan-keuangan/", f"Laporan keuangan siap audit, lead schedule, dan pendampingan sampai opini terbit. KAP-nya bisa dicarikan di cariakuntan.com/{name}."),
            ("Pendampingan penilaian KJPP", "/konsultan-kredit-bank/", "Daftar aset, dokumen legal, dan rekonsiliasi aset tetap disiapkan agar penilaian KJPP untuk agunan atau revaluasi berjalan cepat dan hasilnya maksimal."),
            ("Kredit bank sampai cair", "/konsultan-kredit-bank/", "Financial model, paket kredit, due diligence, dan komite kredit."),
            ("Investor, M&A, dan IPO", "/konsultan-persiapan-ipo/", "Information memorandum, data room, valuasi, dan persiapan IPO."),
            ("Konsultan rumah sakit dan unit cost", f"/konsultan-rumah-sakit/{cs}/", "Ekspansi, kredit, akuisisi, unit cost, dan tarif rumah sakit serta klinik."),
            ("Laporan keuangan dan laporan tahunan PT", "/jasa-penyusunan-laporan-keuangan/", "Sesuai SAK EMKM, SAK EP, atau PSAK, termasuk laporan tahunan PT untuk Permenkum 49/2025."),
            ("CFO paruh waktu", "/cfo-paruh-waktu/", "Fungsi CFO tanpa merekrut penuh waktu.")]
    body = ("<h2>Layanan di " + E(name) + "</h2>" + "".join(f'<h3><a href="{h}">{E(t)}</a></h3><p>{E(d)}</p>' for t, h, d in svcs)
            + f"<h2>Konteks Bisnis {E(name)}</h2><p>{E(name)} adalah {E(note)}. Klien kami di wilayah ini umumnya bergerak di {sect(secs)}. {E(rline)}</p>"
            + ("".join(f"<p>{E(x)}</p>" for x in BOOST.get(name, [])))
            + (f'<h2>Kawasan Bisnis di {E(name)}</h2><p class="t">' + " · ".join(f'<a href="/wilayah/{cs}/{slug(k[0])}/">{E(k[0])}</a>' for k in kws) + "</p>" if kws else "")
            + f'<h2>Cari KAP, KJPP, dan Konsultan Pajak di {E(name)}</h2><p>Untuk memilih kantor akuntan publik, jasa penilai (KJPP), atau konsultan pajak berizin di {E(name)}, gunakan <a href="{ca}">cariakuntan.com/kota/{cs}</a>: <a href="{ca}kap/">KAP {E(name)}</a> · <a href="{ca}kjpp/">KJPP {E(name)}</a> · <a href="{ca}konsultan-pajak/">Konsultan Pajak {E(name)}</a> · <a href="{ca}jasa-laporan-keuangan/">Jasa Laporan Keuangan {E(name)}</a>.</p>'
            + f'<h2>KAP, KJA, dan Konsultan Pajak Mitra FA untuk {E(name)}</h2><p>FA {E(name)} bekerja dengan jaringan mitra lengkap: <b>KAP DHN &amp; Rekan</b> untuk audit, <b>KJA DHN</b> dan <b>KJA Farhani</b> untuk pembukuan dan penyusunan laporan keuangan, serta <b>KKP DHN</b> untuk konsultan pajak. Satu pintu dari pembukuan, audit, pajak, sampai kredit cair. <a href="/mitra-kap-kja/">Lihat mitra KAP dan KJA FA</a>.</p>'
            + f'<p>Ingin membandingkan kantor lain? Gunakan <a href="{ca}">Cari Akuntan {E(name)}</a> untuk KAP, KJA, KJPP, dan konsultan pajak berizin di {E(name)}. Untuk cek standar akuntansi terbaru (PSAK, SAK EP, SAK EMKM), buka <a href="https://updatesak.com/">Update SAK</a>.</p>'
            + f'<h2>Kota Sekitar</h2><p class="t">' + " · ".join(f'<a href="/wilayah/{slug(x[0])}/">FA {E(x[0])}</a>' for x in nb) + "</p>")
    faq = [(f"Apa itu FA {name}?", f"FA {name} adalah layanan FA Indonesia (financial advisor) untuk perusahaan di {name}: kredit bank sampai cair, investor dan IPO, laporan keuangan, serta audit dan pajak bersama KAP, KJA, dan KKP mitra."),
           (f"Apakah FA Indonesia melayani perusahaan di {name}?", f"Ya. Perusahaan di {name}, {prov} kami layani secara daring dan dengan kunjungan lapangan terjadwal, untuk laporan keuangan, persiapan audit, kredit bank, investor, IPO, dan rumah sakit."),
           (f"Di mana mencari KAP atau KJPP di {name}?", f"Gunakan cariakuntan.com/kota/{cs}/ untuk memilih KAP, KJPP, atau konsultan pajak di {name} sesuai syarat bank atau regulator. FA Indonesia menyiapkan laporan keuangan dan dokumennya agar proses audit dan penilaian berjalan lancar."),
           ("Berapa biaya konsultasi?", "Diskusi awal gratis. Lingkup dan biaya disepakati di depan sebelum pekerjaan dimulai.")]
    svc_page(path, f"Wilayah · {E(prov)}", f"FA {name}: Financial Advisor dan Konsultan Keuangan di {name}",
             f"FA {name} (FA Indonesia) mendampingi perusahaan di {name} dari laporan keuangan dan persiapan audit KAP, penilaian KJPP, sampai kredit cair, investor masuk, atau IPO. Dikerjakan bersama tim CA dan CPA FA Indonesia.",
             body, faq, f"FA {name}: Financial Advisor, KAP dan KJA Mitra | FA Indonesia",
             f"FA {name}: financial advisor di {name}, {prov}. Kredit bank, investor, IPO, laporan keuangan, audit KAP dan KJA mitra. Konsultasi awal gratis.",
             [{"@type": "ProfessionalService", "name": f"FA Indonesia {name}", "url": D + path, "provider": PROVIDER, **({"address": {"@type": "PostalAddress", "addressLocality": "Malang", "addressRegion": "Jawa Timur", "addressCountry": "ID"}, "email": "ananta@faindonesia.co.id"} if name == "Malang" else {}), "areaServed": {"@type": "City", "name": name, "containedInPlace": {"@type": "AdministrativeArea", "name": prov}}}],
             "/layanan/", "Semua Layanan", f"Halo FA Indonesia, kami dari {name} ingin konsultasi.",
             [("FA Indonesia", D + "/"), ("Wilayah", D + "/wilayah/"), (name, D + path)]); URLS.append(path)

    for kname, city, adm, ksecs, knote in kws:
        ks = slug(kname); path = f"/wilayah/{cs}/{ks}/"; cak = f"{ca}{ks}/"
        sib = [k for k in kws if k[0] != kname]
        body = (f"<h2>Persiapan Audit KAP di {E(kname)}</h2><p>Perusahaan di {E(kname)} biasanya mencari kantor akuntan publik (KAP) karena diminta bank, wajib audit, atau diminta investor. Masalahnya sering bukan di KAP, tapi di laporan keuangan yang belum siap diaudit. FA Indonesia menyiapkan laporan keuangan, rekonsiliasi, lead schedule, dan dokumen pendukung, lalu mendampingi sampai opini terbit. KAP-nya bisa Anda pilih lewat <a href=\"{cak}kap/\">KAP {E(kname)} di cariakuntan.com</a>.</p>"
                f"<h2>Jasa Penilai (KJPP) untuk Agunan dan Revaluasi di {E(kname)}</h2><p>Untuk agunan kredit atau revaluasi aset tetap, penilaian dilakukan KJPP rekanan bank. Kami siapkan daftar aset, dokumen legal, dan rekonsiliasi aset tetap agar inspeksi berjalan cepat dan nilainya tidak tergerus karena data kurang. Pilihan KJPP: <a href=\"{cak}kjpp/\">jasa penilai {E(kname)}</a>.</p>"
                f"<h2>Kredit Bank sampai Cair</h2><p>{E(kname)} adalah {E(knote)}. Untuk usaha di sektor {sect(ksecs)}, kami susun financial model, paket kredit, dan mendampingi due diligence sampai komite kredit. Rekam jejak pendampingan kredit kumulatif lebih dari Rp1,1 triliun.</p>"
                + (f"<h2>Rumah Sakit dan Klinik</h2><p>Untuk rumah sakit dan klinik di {E(kname)}: <a href=\"/konsultan-rumah-sakit/{cs}/\">konsultan rumah sakit {E(city)}</a> dan <a href=\"/konsultan-unit-cost-rumah-sakit/{cs}/\">unit cost rumah sakit {E(city)}</a>.</p>" if "kesehatan" in ksecs else "")
                + f'<h2>Kawasan Lain di {E(city)}</h2><p class="t"><a href="/wilayah/{cs}/">Semua {E(city)}</a> · ' + " · ".join(f'<a href="/wilayah/{cs}/{slug(k[0])}/">{E(k[0])}</a>' for k in sib) + "</p>")
        faq = [(f"Di mana mencari kantor akuntan publik di {kname}?", f"Pilih KAP sesuai kelas rekanan bank lewat cariakuntan.com/kota/{cs}/{ks}/kap/. FA Indonesia menyiapkan laporan keuangannya agar siap diaudit."),
               (f"Ada jasa penilai KJPP untuk aset di {kname}?", f"Ada. KJPP rekanan bank bisa dijadwalkan inspeksi di {kname}. FA Indonesia menyiapkan data aset dan mendampingi penilaiannya."),
               ("Apakah konsultasi awal berbayar?", "Tidak. Diskusi awal gratis lewat WhatsApp atau email.")]
        svc_page(path, f"Wilayah · {E(adm)}", f"KAP, Jasa Penilai KJPP, dan Kredit Bank di {kname}: Persiapan sampai Tuntas",
                 f"Pendampingan untuk perusahaan di {kname}, {adm}: laporan keuangan siap audit KAP, penilaian aset oleh KJPP, dan kredit bank sampai cair.",
                 body, faq, f"KAP & Jasa Penilai KJPP {kname}: Persiapan Audit dan Kredit | FA Indonesia",
                 f"Persiapan audit KAP, pendampingan jasa penilai KJPP, dan kredit bank untuk perusahaan di {kname}, {adm}. Tim CA dan CPA FA Indonesia. Konsultasi gratis.",
                 [{"@type": "ProfessionalService", "name": f"FA Indonesia {kname}", "url": D + path, "provider": PROVIDER, "areaServed": {"@type": "Place", "name": f"{kname}, {adm}"}}],
                 f"/wilayah/{cs}/", f"Wilayah {city}", f"Halo FA Indonesia, kami dari {kname} ({adm}) ingin konsultasi.",
                 [("FA Indonesia", D + "/"), ("Wilayah", D + "/wilayah/"), (city, D + f"/wilayah/{cs}/"), (kname, D + path)]); URLS.append(path)

# hub wilayah
rows = "".join(f"<h2>{E(rn)}</h2><p class=\"t\">" + " · ".join(f'<a href="/wilayah/{slug(c[0])}/">FA {E(c[0])}</a>' for c in CITIES if c[2] == r) + "</p>" for r, (rn, _) in REGIONS.items())
kwl = "<h2>Kawasan Bisnis</h2><p class=\"t\">" + " · ".join(f'<a href="/wilayah/{slug(k[1])}/{slug(k[0])}/">{E(k[0])}</a>' for k in KAWASAN) + "</p>"
svc_page("/wilayah/", "Wilayah", f"FA per Kota: Financial Advisor di {len(CITIES)} Kota dan {len(KAWASAN)} Kawasan Bisnis Indonesia",
         "FA Indonesia melayani perusahaan dari Aceh sampai Papua. Pilih kota atau kawasan untuk melihat layanan persiapan audit KAP, penilaian KJPP, kredit bank, investor, IPO, dan rumah sakit di wilayah Anda.",
         rows + kwl, [("Apakah FA Indonesia melayani seluruh Indonesia?", "Ya, dengan diskusi daring dan kunjungan lapangan terjadwal sesuai kebutuhan penugasan.")],
         "FA per Kota: FA Jakarta, FA Surabaya, FA Malang dan 90+ Kota | FA Indonesia",
         f"Konsultan keuangan FA Indonesia di {len(CITIES)} kota dan {len(KAWASAN)} kawasan bisnis: persiapan audit KAP, KJPP, kredit bank, investor, IPO, rumah sakit dan unit cost.",
         [], "/layanan/", "Semua Layanan", "Halo FA Indonesia, saya ingin konsultasi.", [("FA Indonesia", D + "/"), ("Wilayah", D + "/wilayah/")]); URLS.append("/wilayah/")

# ================= 4. FOOTER, LAYANAN, SITEMAP, LLMS =================
FOOT_ADD = '<li><a href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a></li><li><a href="/konsultan-unit-cost-rumah-sakit/">Unit Cost Rumah Sakit</a></li><li><a href="/wilayah/">Wilayah</a></li>'
for root, _, files in os.walk(FA):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f); t = rd(p)
        if '/konsultan-unit-cost-rumah-sakit/">Unit Cost Rumah Sakit</a></li><li><a href="/wilayah/">' in t: continue
        t2 = t.replace('<li><a href="/laporan-tahunan-pt/">Laporan Tahunan PT</a></li>', '<li><a href="/laporan-tahunan-pt/">Laporan Tahunan PT</a></li>' + FOOT_ADD, 1)
        if t2 != t: open(p, "w", encoding="utf-8").write(t2)

lp = P("layanan", "index.html")
if os.path.exists(lp):
    t = rd(lp); t = re.sub(r"<!--fa-seo-rs-->.*?<!--/fa-seo-rs-->", "", t, flags=re.S)
    blk = ('<!--fa-seo-rs--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Sektor Kesehatan</p><h2>Rumah Sakit dan Klinik</h2></div>'
           '<p class="t" style="max-width:62em">Ekspansi, kredit bank, akuisisi, investor, unit cost, dan tarif untuk rumah sakit dan klinik swasta.</p>'
           '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn solid" href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a><a class="btn line" href="/konsultan-unit-cost-rumah-sakit/">Unit Cost Rumah Sakit</a><a class="btn line" href="/wilayah/">Layanan per Kota</a></div></div></section><!--/fa-seo-rs-->')
    i = t.find('<section class="block'); t = t[:i] + blk + t[i:]
    open(lp, "w", encoding="utf-8").write(t)

sm = rd(P("sitemap.xml"))
sm = re.sub(r"<!--fa-seo-->.*?<!--/fa-seo-->\n?", "", sm, flags=re.S)
add = "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'0.8' if u.count('/') <= 3 else '0.6'}</priority></url>\n" for u in URLS)
sm = sm.replace("</urlset>", "<!--fa-seo-->\n" + add + "<!--/fa-seo-->\n</urlset>")
open(P("sitemap.xml"), "w", encoding="utf-8").write(sm)

ll = rd(P("llms.txt")); ll = re.sub(r"\n## Rumah Sakit dan Unit Cost.*?(?=\n## |\Z)", "", ll, flags=re.S)
ll = re.sub(r"\n## Artikel Eksplor Terbaru.*?(?=\n## |\Z)", "", ll, flags=re.S)
ll += ("\n## Rumah Sakit dan Unit Cost\n- Konsultan rumah sakit swasta (ekspansi, kredit bank, akuisisi, investor, unit cost, tarif) → https://faindonesia.co.id/konsultan-rumah-sakit/\n"
       "- Konsultan unit cost rumah sakit dan klinik, analisis tarif INA-CBG → https://faindonesia.co.id/konsultan-unit-cost-rumah-sakit/\n"
       f"- Versi per kota tersedia untuk {len(CITIES)} kota, contoh https://faindonesia.co.id/konsultan-rumah-sakit/malang/\n"
       f"- Halaman wilayah: https://faindonesia.co.id/wilayah/ ({len(CITIES)} kota, {len(KAWASAN)} kawasan bisnis seperti Sunter, Kelapa Gading, Cikarang, Cibinong, BSD)\n"
       "\n## Artikel Eksplor Terbaru\n" + "".join(f"- {a['title']} → {D}/artikel/{a['slug']}/\n" for a in ARTS))
open(P("llms.txt"), "w", encoding="utf-8").write(ll)
print("ok", len(URLS), "urls;", len(ARTS), "artikel")
