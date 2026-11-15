#!/usr/bin/env python3
"""15 Nov 2026 (Bos: "Munculkan nama saya dengan gelar lengkap sebagai penulis, simpan di web di Layanan sebagai metode
dasar layanan FA alongside tools digitalnya, dan push SEO-nya. Kesankan FA Indonesia advisor yang punya metode kuat,
tools yang kuat, dan deliverables jelas").

Tiga modul PDF (M&A, Transfer Pricing, Pendanaan dan Investor) disusun di sesi chat 15 Nov dan disimpan di
fa_content/metode20261115/ (PDF + sumber HTML). Script ini (out/faindonesia, idempoten, --dry):
1. menyalin PDF ke /metode/files/, membuat gambar sampul /img/metode/<key>.jpg dan og /img/og-page/metode-<key>.jpg;
2. membuat 4 halaman: /metode/ (hub) dan /metode/<slug>/ (ringkasan isi modul dalam HTML supaya terindeks, deliverables,
   tools FA Apps yang dipakai, FAQ, byline penulis, tombol Download PDF gratis); template = artikel live;
3. menyisipkan section berpenanda <!--fa-metode--> di /layanan/ setelah "Yang Kami Kerjakan": Metode, Tools, Deliverables;
4. link masuk berpenanda <!--fa-metode-l--> di pilar terkait; sitemap dan llms.txt berpenanda <!--metode15-->.
PDF gratis (materi metode, setara brosur), sesuai pengecualian keputusan 13 Nov.
Urutan bila build ulang: setelah generator yang menulis /layanan/ (fa_layanan_ringkas, fa_bumper_lini, fa_bpr_pisah),
sebelum fa_rendah_hati_20261112.py dan fa_lang_global_20261114.py.
"""
import os, re, sys, json, html, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'out', 'faindonesia')
SRC = os.path.join(HERE, 'fa_content', 'metode20261115')
DOMAIN = 'https://faindonesia.co.id'
DRY = '--dry' in sys.argv
TPL = os.path.join(ROOT, 'artikel', 'unit-cost-rumah-sakit-surabaya-activity-based-costing', 'index.html')
NAME = 'Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP'
DATE_ISO = '2026-11-15T21:00:00+07:00'
WA = 'https://wa.me/6282245260121'
E = lambda x: html.escape(x, quote=False)
A = lambda x: html.escape(x, quote=True)

MODS = [
 dict(key='ma', slug='merger-akuisisi', pdf='FA-Modul-01_Merger-dan-Akuisisi.pdf', no='01',
  short='Merger dan Akuisisi',
  title='Metode Merger dan Akuisisi: Due Diligence, Valuasi, Integrasi',
  h1='Metode Merger dan Akuisisi FA Indonesia',
  desc='Metode M&A yang dipakai Tim FA Indonesia: tesis investasi, due diligence, kualitas laba, equity bridge, notifikasi KPPU, dan integrasi. PDF gratis.',
  card='Tujuh langkah transaksi dari tesis investasi sampai integrasi 100 hari, dengan jembatan kualitas laba dan equity bridge.',
  intro='Modul ini adalah metode dasar Tim FA Indonesia untuk setiap penugasan merger, akuisisi, divestasi, dan jual beli usaha. Setiap transaksi dibaca dengan dua lensa: lensa strategi (kenapa transaksi ini menciptakan nilai) dan lensa angka (berapa nilainya dan apakah angkanya bisa dipegang di meja negosiasi). Metode ini mengikuti praktik penasihat transaksi global yang sudah banyak dipublikasikan, disesuaikan dengan aturan dan ukuran usaha di Indonesia.',
  steps=[('Strategi dan Tesis Akuisisi','Alasan transaksi ditulis dalam satu halaman sebelum harga dibicarakan, lengkap dengan kriteria target.'),
         ('Penapisan dan Pendekatan Target','Daftar panjang disaring dengan kartu skor menjadi tiga sampai lima target, lalu NDA dan penawaran tidak mengikat.'),
         ('Due Diligence','Komersial, keuangan, pajak, hukum, TI, dan SDM; temuan merah dilaporkan lebih dulu dan dikaitkan ke harga.'),
         ('Valuasi dan Sinergi','DCF, kelipatan pembanding, transaksi sebanding, serta sinergi yang dipisah menurut tingkat kepastian.'),
         ('Struktur dan Dokumen Transaksi','Saham atau aset, locked box atau completion accounts, earn-out, dan definisi keuangan di SPA.'),
         ('Persetujuan dan Closing','Persetujuan korporasi, izin sektor, notifikasi KPPU bila memenuhi ambang batas, dan rencana hari pertama.'),
         ('Integrasi Pascamerger','Kantor integrasi, rencana 100 hari, dan laporan sinergi bulanan sampai target tercapai.')],
  deliv=['Tesis investasi satu halaman dan kriteria target','Laporan kualitas laba (EBITDA dinormalisasi)','Model valuasi dan equity bridge sampai nilai ekuitas','Data room berindeks untuk calon pembeli atau investor','Review definisi keuangan di SPA dan perhitungan harga akhir','Rencana integrasi 100 hari dan laporan sinergi'],
  tools=[('FA Venus','/apps/venus/','Valuasi, DCF, dan analisis kelayakan transaksi.'),('Kalkulator Valuasi DCF','/kalkulator-valuasi-dcf/','Rentang nilai usaha dengan asumsi tertulis.'),('FA Jupiter','/apps/jupiter/','Merapikan laporan keuangan sebelum due diligence.')],
  faq=[('Apa beda due diligence keuangan dengan audit?','Audit menilai kewajaran laporan keuangan secara umum. Due diligence keuangan menguji hal yang mengubah harga: kualitas laba, modal kerja normal, utang bersih, dan pos setara utang.'),
       ('Kapan transaksi wajib dilaporkan ke KPPU?','Bila nilai aset gabungan di Indonesia lebih dari Rp2,5 triliun atau penjualan gabungan lebih dari Rp5 triliun (perbankan: aset lebih dari Rp20 triliun), terjadi perubahan pengendalian, dan bukan antarperusahaan terafiliasi; paling lambat 30 hari kerja sejak berlaku efektif secara yuridis.'),
       ('Apakah metode ini cocok untuk penjual?','Ya. Penjual memakai urutan yang sama, dimulai dari persiapan: laporan keuangan yang rapi, analisis kualitas laba versi penjual, dan data room sebelum calon pembeli datang.')],
  links=['/jasa-valuasi-usaha/','/rumah-sakit-dijual/','/bpr-dijual/','/menjual-rumah-sakit/']),
 dict(key='tp', slug='transfer-pricing', pdf='FA-Modul-02_Transfer-Pricing.pdf', no='02',
  short='Transfer Pricing',
  title='Metode Transfer Pricing: TP Doc, Benchmarking, PMK 172/2023',
  h1='Metode Transfer Pricing FA Indonesia',
  desc='Metode transfer pricing Tim FA Indonesia: uji kewajiban TP Doc PMK 172/2023, analisis fungsi, benchmarking, master file dan local file. PDF gratis.',
  card='Delapan langkah dokumen penentuan harga transfer sesuai PMK 172/2023, dari uji kewajiban sampai kesiapan pemeriksaan.',
  intro='Modul ini adalah metode dasar Tim FA Indonesia untuk grup usaha yang bertransaksi dengan pihak afiliasi. Urutannya mengikuti praktik transfer pricing jaringan akuntan publik global dan OECD Transfer Pricing Guidelines, disesuaikan dengan PMK 172/2023: transaksi afiliasi dipetakan, kewajiban dokumen diuji, fungsi dianalisis, lalu harga dibuktikan wajar dengan data pembanding.',
  steps=[('Pemetaan Grup dan Transaksi Afiliasi','Bagan grup dan matriks transaksi afiliasi yang cocok dengan catatan atas laporan keuangan.'),
         ('Uji Kewajiban Dokumen','Peredaran bruto lebih dari Rp50 miliar, barang berwujud afiliasi lebih dari Rp20 miliar, atau jasa, bunga, dan harta tak berwujud lebih dari Rp5 miliar pada tahun pajak sebelumnya.'),
         ('Analisis Industri dan Bisnis','Pemicu laba, siklus usaha, dan strategi grup yang memengaruhi harga.'),
         ('Analisis Fungsi, Aset, dan Risiko','Karakterisasi entitas dan pemetaan fungsi DEMPE untuk harta tak berwujud.'),
         ('Pemilihan Metode','Metode paling tepat dari PMK 172/2023, pihak yang diuji, dan indikator laba.'),
         ('Benchmarking','Perusahaan sebanding, saringan kuantitatif dan kualitatif, serta rentang interkuartil.'),
         ('Master File dan Local File','Tersedia paling lambat empat bulan setelah akhir tahun pajak, ikhtisarnya dilampirkan pada SPT Tahunan.'),
         ('Pemantauan dan Kesiapan Pemeriksaan','Margin dipantau tiap triwulan, harga disesuaikan sebelum tutup buku, dokumen siap diserahkan dalam satu bulan.')],
  deliv=['Memo kewajiban dokumen per entitas per tahun','Bagan grup dan matriks transaksi afiliasi','Analisis fungsi, aset, dan risiko','Segmentasi laba yang direkonsiliasi ke laporan keuangan','Kalender kepatuhan dan pemantauan margin triwulanan','Berkas siap pemeriksaan'],
  tools=[('Kalkulator TP Doc','/kalkulator-tp-doc/','Cek wajib master file dan local file, uji kewajaran interkuartil.'),('FA Jupiter','/apps/jupiter/','Laporan keuangan dan kertas kerja pajak yang rapi.'),('FA Galaxy','/galaxy/','Rujukan standar akuntansi dan istilah.')],
  faq=[('Siapa yang wajib menyusun master file dan local file?','Wajib pajak yang bertransaksi afiliasi dan pada tahun pajak sebelumnya memiliki peredaran bruto lebih dari Rp50 miliar, transaksi barang berwujud afiliasi lebih dari Rp20 miliar, atau transaksi jasa, bunga, dan harta tak berwujud afiliasi lebih dari Rp5 miliar, atau bertransaksi dengan afiliasi di yurisdiksi bertarif pajak lebih rendah.'),
       ('Kapan dokumen harus tersedia?','Master file dan local file paling lambat empat bulan setelah akhir tahun pajak, CbCR paling lambat 12 bulan, dan saat diminta DJP diserahkan paling lama satu bulan.'),
       ('Apakah transaksi afiliasi dalam negeri juga dihitung?','Ya. Kewajiban dokumen tidak terbatas pada transaksi dengan afiliasi luar negeri.')],
  links=['/kalkulator-tp-doc/','/cfo-paruh-waktu/']),
 dict(key='fd', slug='pendanaan-investor', pdf='FA-Modul-03_Pendanaan-dan-Investor.pdf', no='03',
  short='Pendanaan dan Investor',
  title='Metode Mencari Pendanaan dan Investor: Bank, PE, VC, IPO',
  h1='Metode Mencari Pendanaan dan Investor FA Indonesia',
  desc='Metode pendanaan Tim FA Indonesia: equity story, model keuangan, data room, pemetaan investor, term sheet, DSCR, sampai IPO. PDF gratis.',
  card='Delapan langkah menggalang dana dari kredit bank, private equity, venture capital, sampai IPO, dengan hitungan dilusi dan DSCR.',
  intro='Modul ini adalah metode dasar Tim FA Indonesia untuk setiap penugasan kredit bank, pencarian investor, dan persiapan IPO. Pendanaan disiapkan dengan dua lensa: cerita yang membuat pemberi dana tertarik, dan angka yang tahan diuji. Urutannya mengikuti praktik penasihat pendanaan global, disesuaikan dengan bank, investor, dan bursa di Indonesia.',
  steps=[('Diagnosis Kesiapan','Laporan keuangan, legalitas, tata kelola, dan pengendalian internal diperiksa sebelum dokumen pertama dikirim.'),
         ('Kebutuhan Dana dan Struktur Modal','Rencana penggunaan dana, kapasitas utang yang aman, dan dilusi yang bisa diterima.'),
         ('Equity Story dan Rencana Bisnis','Pasar, keunggulan, jalur pertumbuhan, dan indikator kinerja yang akan dilaporkan.'),
         ('Model Keuangan dan Valuasi','Model tiga laporan yang saling terhubung, skenario, sensitivitas, dan rentang valuasi.'),
         ('Data Room dan Vendor Due Diligence','Data berindeks dan temuan yang diketahui lebih dulu agar tidak menjadi alat menawar.'),
         ('Pemetaan dan Pendekatan Investor','Daftar panjang disaring menurut tiket, sektor, tahap, dan horizon; teaser, NDA, information memorandum.'),
         ('Term Sheet dan Due Diligence Investor','Valuasi dibaca bersama syaratnya: preferensi likuidasi, perlindungan dilusi, hak veto, kovenan.'),
         ('Closing dan 100 Hari Setelah Dana Masuk','Paket laporan berkala dan pemantauan kovenan.')],
  deliv=['Laporan diagnosis kesiapan pendanaan','Model keuangan tiga laporan dengan skenario','Rentang valuasi dan dasar perhitungannya','Equity story dan materi presentasi investor','Data room berindeks','Paket laporan berkala setelah dana masuk'],
  tools=[('Cek Kesiapan Pendanaan','/cek-kesiapan-pendanaan/','Skor kesiapan sebelum bertemu bank atau investor.'),('Cek Kapasitas Kredit','/cek-kapasitas-kredit/','DSCR dan plafon kredit per suku bunga dan tenor.'),('Cek Kelayakan IPO','/cek-kelayakan-ipo/','Jalur papan pencatatan BEI yang paling dekat.'),('FA Venus','/apps/venus/','Valuasi, DCF, bankability, dan rasio.')],
  faq=[('Jalur pendanaan mana yang paling cocok?','Tergantung kebutuhannya. Modal kerja dan aset dengan arus kas stabil cocok dengan kredit bank; ekspansi atau perubahan pemegang saham cocok dengan private equity atau investor strategis; pertumbuhan jangka panjang dengan kinerja dan tata kelola yang siap bisa ke IPO.'),
       ('Apa yang paling sering membuat pengajuan gagal?','Laporan keuangan yang belum bisa dibaca pemberi dana, model keuangan yang tidak tersambung, dan proses yang hanya mendekati satu atau dua nama.'),
       ('Bagaimana bank menilai kemampuan bayar?','Salah satunya dengan DSCR: arus kas yang tersedia untuk membayar utang dibagi pokok dan bunga jatuh tempo setahun. Batas minimumnya berbeda antarbank dan antarsektor.')],
  links=['/konsultan-kredit-bank/','/konsultan-persiapan-ipo/','/cek-kesiapan-pendanaan/','/cek-kapasitas-kredit/','/pendanaan-rumah-sakit/']),
]


def wr(path, s):
    if DRY:
        print('DRY write', path); return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(s)


def assets():
    import pypdfium2 as pdfium
    from PIL import Image
    for m in MODS:
        src = os.path.join(SRC, m['pdf'])
        dst = os.path.join(ROOT, 'metode', 'files', m['pdf'])
        if not DRY:
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(src, dst)
        im = pdfium.PdfDocument(src)[0].render(scale=1.6).to_pil().convert('RGB')
        th = im.copy(); th.thumbnail((600, 849))
        og = im.resize((1200, int(im.height * 1200 / im.width)))
        og = og.crop((0, 60, 1200, 690))
        if not DRY:
            os.makedirs(os.path.join(ROOT, 'img', 'metode'), exist_ok=True)
            th.save(os.path.join(ROOT, 'img', 'metode', m['key'] + '.jpg'), quality=84, optimize=True, progressive=True)
            og.save(os.path.join(ROOT, 'img', 'og-page', 'metode-' + m['key'] + '.jpg'), quality=84, optimize=True)
        m['size_kb'] = os.path.getsize(src) // 1024


CSS = '''<style id="fa-metode-css">.mt-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:24px}.mt-c{display:flex;flex-direction:column}.mt-c a.cv{display:block;aspect-ratio:210/297;overflow:hidden;border:1px solid var(--line);background:#111}.mt-c a.cv img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}.mt-c a.cv:hover img{transform:scale(1.02)}.mt-c .no{font-family:var(--mono);font-size:12px;letter-spacing:.14em;color:var(--muted);margin:16px 0 4px}.mt-c h3{margin:0 0 8px;font-size:21px;line-height:1.25}.mt-c p{margin:0 0 12px;color:var(--muted);font-size:15px;line-height:1.6}.mt-c .ac{margin-top:auto;display:flex;flex-wrap:wrap;gap:8px}.mt-row{margin-top:44px;padding-top:28px;border-top:1px solid var(--line)}.mt-row h3.k{font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-family:var(--body);font-weight:600;margin:0 0 6px;color:var(--muted)}.mt-tl{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:14px}.mt-tl a{display:block;padding:16px 18px;border:1px solid var(--line);text-decoration:none;color:inherit}.mt-tl a:hover{border-color:rgba(255,255,255,.55)}.mt-tl b{display:block;font-size:17px;margin-bottom:4px}.mt-tl span{font-size:14px;color:var(--muted);line-height:1.5}.mt-dl{width:100%;border-collapse:collapse;margin-top:14px;font-size:15px}.mt-dl th{text-align:left;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:600;padding:10px 14px 10px 0;border-bottom:1px solid rgba(255,255,255,.5)}.mt-dl td{padding:12px 14px 12px 0;border-bottom:1px solid var(--line);vertical-align:top;line-height:1.55}.mt-by{margin-top:22px;font-size:14px;color:var(--muted)}@media(max-width:860px){.mt-g{grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:min(70vw,280px);overflow-x:auto;scroll-snap-type:x mandatory;gap:18px;padding-bottom:8px}.mt-c{scroll-snap-align:start}.mt-tl{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.mt-tl{grid-template-columns:none}}</style>'''

TOOLS4 = [('FA Saturn', '/apps/saturn/', 'Audit dan kertas kerja KAP, alur risiko berwarna.'),
          ('FA Jupiter', '/apps/jupiter/', 'Laporan keuangan sampai siap audit, pajak, TP Doc.'),
          ('FA Venus', '/apps/venus/', 'Valuasi, DCF, kredit, DSCR, kesiapan pendanaan.'),
          ('FA Galaxy', '/galaxy/', 'Standar akuntansi, materi, dan kamus.')]


def btn_dl(m, cls='btn solid sm'):
    return (f'<a class="{cls}" href="/metode/files/{m["pdf"]}" download data-metode="{m["key"]}" '
            f'onclick="try{{gtag(\'event\',\'file_download\',{{file_name:\'{m["pdf"]}\'}})}}catch(e){{}}">Download PDF</a>')


def layanan_block():
    cards = ''.join(
        f'<div class="mt-c"><a class="cv" href="/metode/{m["slug"]}/"><img alt="Sampul modul {A(m["short"])} FA Indonesia" '
        f'loading="lazy" decoding="async" src="/img/metode/{m["key"]}.jpg" width="600" height="849"/></a>'
        f'<p class="no">MODUL {m["no"]}</p><h3><a href="/metode/{m["slug"]}/" style="text-decoration:none">{E(m["short"])}</a></h3>'
        f'<p>{E(m["card"])}</p><div class="ac"><a class="btn line sm" href="/metode/{m["slug"]}/">Ringkasan</a>{btn_dl(m)}</div></div>'
        for m in MODS)
    tools = ''.join(f'<a href="{u}"><b>{E(n)}</b><span>{E(d)}</span></a>' for n, u, d in TOOLS4)
    rows = ''.join(f'<tr><td>{E(m["short"])}</td><td>{E("; ".join([m["deliv"][0]] + [d[0].lower() + d[1:] for d in m["deliv"][1:4]]))}.</td></tr>' for m in MODS)
    return ('<!--fa-metode-->' + CSS +
        '<section class="block alt" id="metode"><div class="wrap">'
        '<div class="head"><p class="eyebrow">Metode, Tools, dan Deliverables</p><h2>Cara Kerja yang Tertulis dan Bisa Diuji</h2></div>'
        '<p class="lead" style="max-width:62ch;color:var(--muted)">Setiap penugasan FA Indonesia berjalan di atas tiga hal: metode tertulis yang sama untuk setiap klien, tools digital buatan tim sendiri, dan deliverables yang disepakati sejak awal. Ketiga modul di bawah adalah metode dasar layanan kami, terbuka untuk dibaca siapa saja.</p>'
        f'<div class="mt-g">{cards}</div>'
        f'<p class="mt-by">Ditulis oleh <a href="/ananta-w-sasongko/">{E(NAME)}</a> bersama Tim FA Indonesia. <a href="/metode/">Semua metode</a>.</p>'
        '<div class="mt-row"><h3 class="k">Tools Digital yang Dipakai dalam Penugasan</h3>'
        f'<div class="mt-tl">{tools}</div></div>'
        '<div class="mt-row"><h3 class="k">Deliverables yang Anda Terima</h3>'
        f'<table class="mt-dl"><thead><tr><th style="width:26%">Penugasan</th><th>Hasil kerja tertulis</th></tr></thead><tbody>{rows}</tbody></table></div>'
        '</div></section><!--/fa-metode-->')


def tpl_parts():
    s = open(TPL).read()
    head, rest = s[:s.find('</head>')], s[s.find('</head>'):]
    m0 = rest.find('<main'); m1 = rest.find('</main>')
    main = rest[m0:m1]
    k = main.rfind('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    author = main[k:main.find('</div></div>', k) + len('</div></div>')]
    assert 'Penulis' in author
    return head, rest[:m0], rest[m1:], author


def set_head(head, url, title, desc, og, ld, otype='article'):
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', h, flags=re.S)
    def meta(key, val, attr='name'):
        nonlocal h
        h = re.sub(r'<meta content="[^"]*" ' + attr + r'="' + re.escape(key) + r'"/?>', f'<meta content="{A(val)}" {attr}="{key}"/>', h)
    meta('description', desc); meta('twitter:image', og)
    for k, v in (('og:title', title), ('og:description', desc), ('og:url', url), ('og:image', og), ('og:type', otype)):
        meta(k, v, 'property')
    h = re.sub(r'<link href="[^"]*" rel="canonical"/?>', f'<link href="{url}" rel="canonical"/>', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>', h, count=1, flags=re.S)
    h = re.sub(r'<meta content="[^"]*" property="article:[a-z_]+"/?>', '', h)
    assert url in h and E(title) in h
    return h


def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


PERSON = {'@type': 'Person', '@id': DOMAIN + '/ananta-w-sasongko/#person', 'name': NAME, 'url': DOMAIN + '/ananta-w-sasongko/'}
ORG = {'@type': 'Organization', '@id': DOMAIN + '/#org', 'name': 'FA Indonesia', 'url': DOMAIN + '/', 'logo': {'@type': 'ImageObject', 'url': DOMAIN + '/img/brand/mark-hero.png'}}


def page_mod(m, parts):
    head, pre, post, author = parts
    url = f'{DOMAIN}/metode/{m["slug"]}/'
    og = f'{DOMAIN}/img/og-page/metode-{m["key"]}.jpg'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Article', '@id': url + '#article', 'headline': m['h1'], 'description': m['desc'], 'url': url, 'mainEntityOfPage': url,
         'inLanguage': 'id', 'datePublished': DATE_ISO, 'dateModified': DATE_ISO, 'author': PERSON, 'publisher': ORG, 'image': og,
         'articleSection': 'Metode FA Indonesia', 'keywords': m['short'].lower(),
         'associatedMedia': {'@type': 'MediaObject', 'name': m['h1'] + ' (PDF)', 'encodingFormat': 'application/pdf',
                             'contentUrl': f'{DOMAIN}/metode/files/{m["pdf"]}', 'author': PERSON}},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in m['faq']]},
        crumbs([('Beranda', DOMAIN + '/'), ('Layanan', DOMAIN + '/layanan/'), ('Metode', DOMAIN + '/metode/'), (m['short'], url)])]}
    steps = ''.join(f'<li><b>{E(t)}.</b> {E(d)}</li>' for t, d in m['steps'])
    deliv = ''.join(f'<li>{E(d)}</li>' for d in m['deliv'])
    tools = ''.join(f'<a href="{u}"><b>{E(n)}</b><span>{E(d)}</span></a>' for n, u, d in m['tools'])
    faq = ''.join(f'<details class="faq-acc"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in m['faq'])
    others = ''.join(f'<li><a href="/metode/{o["slug"]}/">{E(o["h1"])}</a></li>' for o in MODS if o is not m)
    main = (f'<main id="top">{CSS}<section class="block"><div class="wrap art">'
        f'<p class="eyebrow"><a href="/metode/" style="text-decoration:none">Metode FA Indonesia · Modul {m["no"]}</a></p>'
        f'<h1 style="margin:.2em 0 .4em;font-size:clamp(32px,4.4vw,52px);line-height:1.12">{E(m["h1"])}</h1>'
        f'<p class="meta">Oleh <a href="/ananta-w-sasongko/">{E(NAME)}</a> · Tim FA Indonesia · 15 November 2026 · PDF {m["size_kb"]} KB</p>'
        f'<div style="display:grid;grid-template-columns:minmax(0,220px) minmax(0,1fr);gap:28px;align-items:start;margin:22px 0 8px">'
        f'<a class="cv" href="/metode/files/{m["pdf"]}" style="display:block;border:1px solid var(--line)"><img alt="Sampul {A(m["h1"])}" src="/img/metode/{m["key"]}.jpg" width="600" height="849" style="width:100%;height:auto;display:block"/></a>'
        f'<div><p style="margin-top:0">{E(m["intro"])}</p><p style="display:flex;flex-wrap:wrap;gap:10px">{btn_dl(m, "btn solid")}'
        f'<a class="btn line" href="{WA}" rel="noopener" target="_blank">Chat Ananta, CPA</a></p></div></div>'
        f'<h2 id="langkah-kerja">Langkah Kerja</h2><ol>{steps}</ol>'
        f'<h2 id="deliverables">Deliverables yang Anda Terima</h2><ul>{deliv}</ul>'
        f'<h2 id="tools">Tools Digital yang Dipakai</h2><div class="mt-tl">{tools}</div>'
        f'<h2 id="pertanyaan-umum">Pertanyaan Umum</h2>{faq}'
        f'<h2 id="metode-lain">Metode Lain</h2><ul>{others}<li><a href="/layanan/#metode">Metode, tools, dan deliverables di halaman Layanan</a></li></ul>'
        f'{author}</div></section>')
    return set_head(head, url, m['title'], m['desc'], og, ld) + pre + main + post


def page_hub(parts):
    head, pre, post, author = parts
    url = f'{DOMAIN}/metode/'
    title = 'Metode Kerja FA Indonesia: M&A, Transfer Pricing, Pendanaan'
    desc = 'Tiga modul metode dasar layanan FA Indonesia: merger dan akuisisi, transfer pricing, serta pendanaan dan investor. Lengkap dengan tools dan deliverables.'
    og = f'{DOMAIN}/img/og-page/metode-ma.jpg'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', '@id': url + '#page', 'url': url, 'name': title, 'description': desc, 'inLanguage': 'id', 'author': PERSON, 'publisher': ORG,
         'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{DOMAIN}/metode/{m["slug"]}/', 'name': m['h1']} for i, m in enumerate(MODS)]}},
        crumbs([('Beranda', DOMAIN + '/'), ('Layanan', DOMAIN + '/layanan/'), ('Metode', url)])]}
    blk = layanan_block().replace('<section class="block alt" id="metode">', '<section class="block" id="metode">')
    blk = blk.replace('<h2>Cara Kerja yang Tertulis dan Bisa Diuji</h2>', '<h1 style="margin:.2em 0 .4em;font-size:clamp(32px,4.4vw,52px);line-height:1.12">Metode Kerja FA Indonesia</h1>')
    main = f'<main id="top">{blk}<section class="block"><div class="wrap art">{author}</div></section>'
    return set_head(head, url, title, desc, og, ld, 'website') + pre + main + post


def insert_marked(path, marker, block, where):
    s = open(path).read()
    s0 = s
    s = re.sub(r'<!--' + marker + r'-->.*?<!--/' + marker + r'-->\n?', '', s, flags=re.S)
    k = where(s)
    assert k > 0, path
    s = s[:k] + block + s[k:]
    if s != s0:
        wr(path, s)
        return 1
    return 0


def main():
    parts = tpl_parts()
    assets()
    n = 0
    for m in MODS:
        for u in [t[1] for t in m['tools']] + m['links']:
            assert os.path.exists(os.path.join(ROOT, u.strip('/'), 'index.html')), u
        p = os.path.join(ROOT, 'metode', m['slug'], 'index.html')
        new = page_mod(m, parts)
        if not os.path.exists(p) or open(p).read() != new:
            wr(p, new); n += 1
    p = os.path.join(ROOT, 'metode', 'index.html'); new = page_hub(parts)
    if not os.path.exists(p) or open(p).read() != new:
        wr(p, new); n += 1
    # /layanan/
    n += insert_marked(os.path.join(ROOT, 'layanan', 'index.html'), 'fa-metode', layanan_block(),
                       lambda s: s.find('<section class="block alt" id="rekam">'))
    # link masuk di pilar
    pil = {}
    for m in MODS:
        for u in m['links']:
            pil.setdefault(u, []).append(m)
    for u, ms in pil.items():
        line = ('<!--fa-metode-l--><p class="mt-in" style="margin:28px 0 0;padding-top:16px;border-top:1px solid var(--line);font-size:15px">Metode kerja yang kami pakai: '
                + ', '.join(f'<a href="/metode/{m["slug"]}/">{E(m["h1"])}</a>' for m in ms) + ' (PDF gratis).</p><!--/fa-metode-l-->')
        n += insert_marked(os.path.join(ROOT, u.strip('/'), 'index.html'), 'fa-metode-l', line,
                           lambda s: s.rfind('</div>', 0, s.find('</main>')))
    # sitemap + llms
    urls = ['/metode/'] + [f'/metode/{m["slug"]}/' for m in MODS]
    sm = '<!--metode15-->' + ''.join(f'<url><loc>{DOMAIN}{u}</loc><lastmod>2026-11-15</lastmod><priority>0.8</priority></url>' for u in urls) + '<!--/metode15-->\n'
    n += insert_marked(os.path.join(ROOT, 'sitemap.xml'), 'metode15', sm, lambda s: s.rfind('</urlset>'))
    p = os.path.join(ROOT, 'llms.txt'); s = open(p).read(); s0 = s
    s = re.sub(r'\n<!--metode15-->.*?<!--/metode15-->', '', s, flags=re.S)
    s = s.rstrip('\n') + '\n<!--metode15-->\n## Metode Kerja FA Indonesia (penulis: ' + NAME + ')\n' + ''.join(
        f'- {m["h1"]} → {DOMAIN}/metode/{m["slug"]}/ (PDF: {DOMAIN}/metode/files/{m["pdf"]})\n' for m in MODS) + '<!--/metode15-->\n'
    if s != s0:
        wr(p, s); n += 1
    print('berubah:', n)


if __name__ == '__main__':
    main()
