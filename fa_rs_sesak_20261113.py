#!/usr/bin/env python3
"""13 Nov 2026 (Bos: "Tempel artikel itu yang lagi viral, FA harus dompleng fenomena ini" lalu "Push SEO ke setiap daerah juga").
Pemicu: opini Laksono Trisnantoro, Kompas Nov 2026, "Sektor Kesehatan yang Sesak Napas" (Hari Kesehatan Nasional 2026).
BEKERJA DI out/faindonesia, idempoten. Dry run: --dry.
1. Artikel /artikel/rumah-sakit-sesak-napas-pendanaan/ (fa_content/articles/rumah-sakit-sesak-napas-pendanaan.json) lewat
   build() fa_artikel_lead_20261111.py (template live), + blok tim RS (fa-rstim) sebelum Pertanyaan Umum.
   Sisipan berpenanda <!--rssn-->: sitemap, llms.txt, kartu Eksplor, Baca Juga balik di artikel RS terkait.
2. Keluarga baru /pendanaan-rumah-sakit/ (pilar) + /pendanaan-rumah-sakit/<slug>/ untuk SEMUA slug /konsultan-rumah-sakit/<slug>/
   (113 kota + 393 kabupaten/kota + 37 provinsi). Halaman dibangun dari halaman live /konsultan-rumah-sakit/<slug>/:
   head (title, description, canonical, og, JSON-LD) dan isi main diganti; blok lokal yang sudah unik dipakai ulang
   (Konteks, Sekilas/uq-lokal, Area Layanan rsw-area, Layanan Lain fanas-x, daftar kab/kota di halaman provinsi, Kota Sekitar).
3. Link balik: <!--rssn-l--> di semua /konsultan-rumah-sakit/<slug>/ (sebelum Pertanyaan Umum), pilar /konsultan-rumah-sakit/,
   dan baris rsw-kec di 2.032 halaman kecamatan /wilayah/<kota>/kecamatan/<kec>/.
Urutan bila build ulang: setelah fa_rs_tim_20261105.py dan fa_artikel_lead_20261111.py; lalu fa_eksplor_rapi_20261113.py,
fa_rendah_hati_20261112.py.
"""
import os, re, json, html, sys, glob, hashlib
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'out', 'faindonesia')
DOMAIN = 'https://faindonesia.co.id'
WA = '6282245260121'
DRY = '--dry' in sys.argv
SLUG = 'rumah-sakit-sesak-napas-pendanaan'
FAM = 'pendanaan-rumah-sakit'
DATE = '2026-11-13'
sys.path.insert(0, os.path.join(HERE, 'shared'))
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location('lead', os.path.join(HERE, 'fa_artikel_lead_20261111.py'))
LEAD = importlib.util.module_from_spec(spec); spec.loader.exec_module(LEAD)
LEAD.DATE_ISO = '2026-11-13T15:00:00+07:00'; LEAD.DATE_ID = '13 November 2026'

E = lambda s: html.escape(s, quote=False)
written = []


def rd(p): return open(p, encoding='utf-8').read()


def wr(p, s):
    written.append(p)
    if DRY: return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)


def slugify(t):
    t = html.unescape(re.sub(r'<[^>]+>', '', t)).lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60]


def pick(key, opts):
    return opts[int(hashlib.md5(key.encode()).hexdigest(), 16) % len(opts)]


# ------------------------------------------------------------------ 1. artikel
def rstim_block(place=None):
    s = rd(os.path.join(ROOT, 'konsultan-rumah-sakit', 'purbalingga', 'index.html'))
    b = re.search(r'<!--fa-rstim-->.*?<!--/fa-rstim-->', s, re.S).group(0)
    msg = f'Halo Pak Ananta, saya ingin diskusi pendanaan rumah sakit di {place}.' if place else 'Halo Pak Ananta, saya ingin diskusi pendanaan rumah sakit.'
    return re.sub(r'(<a class="wa" href="https://wa\.me/\d+\?text=)[^"]*', lambda m: m.group(1) + quote(msg), b, count=1)


def article():
    a = json.load(open(os.path.join(HERE, 'fa_content', 'articles', SLUG + '.json'), encoding='utf-8'))
    tpl = rd(os.path.join(ROOT, 'artikel', LEAD.TPL_SLUG, 'index.html'))
    titles = {r: LEAD.title_of(r) for r in a['related']}
    if DRY:
        print('artikel (dry)'); return a
    s = LEAD.build(a, tpl, titles)
    k = s.find('<h2>Pertanyaan Umum</h2>')
    s = s[:k] + '<div style="margin:34px 0">' + rstim_block() + '</div>\n' + s[k:]
    if 'fa-rstim-css' not in s.split('</head>')[0]:
        css = re.search(r'<style id="fa-rstim-css">.*?</style>', rd(os.path.join(ROOT, 'konsultan-rumah-sakit', 'purbalingga', 'index.html')), re.S).group(0)
        s = s.replace('</head>', css + '</head>', 1)
    wr(os.path.join(ROOT, 'artikel', SLUG, 'index.html'), s)
    return a


def rstim_css_ok():
    s = rd(os.path.join(ROOT, 'artikel', SLUG, 'index.html'))
    return '.rstb' in s or 'rstim' in s.split('</head>')[0]


# ------------------------------------------------------------------ 2. halaman daerah
INTRO = [
 'Pendampingan pendanaan untuk rumah sakit dan klinik swasta di {n}: kredit modal kerja untuk menjembatani klaim BPJS, kredit investasi alat dan gedung, investor, serta laporan keuangan yang siap dibaca bank.',
 'Rumah sakit di {n} yang kasnya tertahan klaim, ingin menambah alat, atau menyiapkan ekspansi bisa memulai dari angka: arus kas, kapasitas utang, dan laporan keuangan yang dipercaya pemberi dana.',
 'Untuk pemilik dan direksi rumah sakit di {n}: peta sumber dana yang realistis, mulai dari mengubah piutang klaim menjadi kas sampai kredit bank dan investor ekuitas.',
]
WHY = [
 'Opini Prof. Laksono Trisnantoro di Kompas pada Hari Kesehatan Nasional 2026 mencatat belanja kesehatan Indonesia baru sekitar 2,7% PDB, lebih rendah dari kisaran 3% saat BPJS dimulai. Di tingkat rumah sakit, kekurangan dana ini terasa sebagai piutang klaim yang menumpuk, margin JKN yang tipis, dan rencana alat atau gedung yang terus tertunda. Rumah sakit di {n} tidak harus menunggu kebijakan nasional berubah untuk mulai menata pendanaannya.',
 'Sektor kesehatan sedang "sesak napas": belanja kesehatan nasional sekitar 2,7% PDB (opini Laksono Trisnantoro, Kompas, November 2026). Bagi rumah sakit di {n}, dampaknya konkret: kas tertahan pending claim, biaya obat dan gaji naik lebih cepat dari tarif, dan ekspansi sulit dibiayai dari kas sendiri. Kebijakan nasional butuh waktu, sementara kewajiban rumah sakit jatuh tempo tiap bulan.',
]
STEPS = ['<b>Ubah piutang klaim menjadi kas.</b> Petakan umur piutang dan penyebab pending claim (koding, berkas, verifikasi) sebelum menambah utang.',
         '<b>Hitung unit cost per layanan.</b> Ketahui layanan yang menutup biaya dan yang perlu ditata ulang tanpa mengorbankan mutu.',
         '<b>Ukur kapasitas utang.</b> Proyeksi arus kas dan DSCR menjawab berapa utang yang aman dan cicilan yang sanggup dibayar.',
         '<b>Siapkan laporan keuangan siap bank.</b> Laporan sesuai PSAK, idealnya diaudit KAP terdaftar, sebagai tiket ke bank dan investor.',
         '<b>Pilih sumber dana yang cocok.</b> Kredit modal kerja, kredit investasi, sindikasi, atau investor ekuitas, dengan konsekuensi kendali yang disepakati pemegang saham sejak awal.']
TABLE = ('<div class="tblwrap"><table class="tbl"><thead><tr><th>Kebutuhan rumah sakit</th><th>Sumber dana yang lazim</th><th>Yang disiapkan</th></tr></thead><tbody>'
         '<tr><td>Kas tertahan klaim BPJS</td><td>Kredit modal kerja, fasilitas berbasis tagihan klaim</td><td>Aging piutang klaim, proyeksi arus kas 12 bulan</td></tr>'
         '<tr><td>Alat kesehatan baru</td><td>Kredit investasi, sewa pembiayaan</td><td>Studi kelayakan layanan, titik impas</td></tr>'
         '<tr><td>Gedung atau tambah tempat tidur</td><td>Kredit investasi jangka panjang, sindikasi</td><td>Proyeksi 5 sampai 10 tahun, laporan keuangan audited</td></tr>'
         '<tr><td>Rumah sakit kedua atau akuisisi</td><td>Investor ekuitas (PE/VC), mitra strategis</td><td>Valuasi, business plan, data room</td></tr>'
         '<tr><td>Utang lama terlalu berat</td><td>Take over, restrukturisasi, top up</td><td>Riwayat kredit, rencana pemulihan kas</td></tr></tbody></table></div>')
TOOLS = ('<ul><li><a href="/cek-kapasitas-kredit/">Cek Kapasitas Kredit</a>: perkiraan plafon yang sanggup dibayar.</li>'
         '<li><a href="/kalkulator-dscr/">Kalkulator DSCR</a>: rasio yang dipakai bank menilai kemampuan bayar.</li>'
         '<li><a href="/kalkulator-valuasi-rumah-sakit/">Kalkulator Valuasi Rumah Sakit</a>: nilai indikatif sebelum bicara dengan investor.</li>'
         '<li><a href="/kalkulator-unit-cost-rumah-sakit/">Kalkulator Unit Cost Rumah Sakit</a>: biaya per layanan dibanding tarif.</li>'
         '<li><a href="/cek-kesiapan-pendanaan/">Cek Kesiapan Pendanaan</a>: daftar periksa sebelum mengajukan dana.</li></ul>')
READ = [(SLUG, 'Sektor Kesehatan Sesak Napas, Rumah Sakit Jangan Ikut Menahan Napas'),
        ('kredit-bank-untuk-rumah-sakit-swasta', None), ('piutang-klaim-bpjs-dan-arus-kas-rumah-sakit', None),
        ('indikator-keuangan-rumah-sakit-yang-dilihat-investor', None), ('dscr-adalah-cara-menghitung-kredit-bank', None)]


def read_list():
    out = []
    for s, t in READ:
        out.append(f'<li><a href="/artikel/{s}/">{E(t or LEAD.title_of(s))}</a></li>')
    return '<ul>' + ''.join(out) + '</ul>'


def faq(n):
    return [(f'Bisakah rumah sakit di {n} dibantu mengajukan kredit bank?', f'Bisa. Tim FA Indonesia menyiapkan laporan keuangan, proyeksi arus kas, dan paket kredit untuk rumah sakit dan klinik di {n}, lalu mendampingi sampai dana cair. Diskusi berjalan daring dengan kunjungan bila diperlukan.'),
            ('Apakah piutang klaim BPJS bisa dipakai untuk mendapat modal kerja?', 'Bisa menjadi dasar. Bank melihat umur piutang, riwayat pembayaran klaim, dan arus kas. Karena itu perapian piutang klaim biasanya dikerjakan lebih dulu.'),
            ('Bagaimana kalau pemegang saham belum sepakat soal utang atau investor?', 'Mulai dari proyeksi beberapa skenario (tanpa utang, dengan kredit, dengan investor) supaya keputusan diambil dari angka yang sama.'),
            ('Bagaimana memulai?', 'Hubungi tim lewat tombol WhatsApp. Diskusi awal untuk memetakan kebutuhan dana, lalu ruang lingkup dan jadwal disepakati.')]


def ld(url, name, n, prov, faqs, kind):
    area = {'@type': 'AdministrativeArea' if kind == 'prov' else 'City', 'name': n}
    if prov and kind != 'prov': area['containedInPlace'] = {'@type': 'AdministrativeArea', 'name': prov}
    g = [{'@type': 'Service', 'name': name, 'serviceType': 'Pendanaan Rumah Sakit',
          'provider': {'@type': 'ProfessionalService', '@id': DOMAIN + '/#org', 'name': 'FA Indonesia', 'url': DOMAIN + '/'},
          'areaServed': area, 'url': url},
         {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': DOMAIN + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'Pendanaan Rumah Sakit', 'item': f'{DOMAIN}/{FAM}/'},
             {'@type': 'ListItem', 'position': 3, 'name': n, 'item': url}]},
         {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in faqs]}]
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False) + '</script>'


def set_head(t, old_path, new_path, title, desc, ldtag, ogimg=None):
    head, rest = t.split('</head>', 1)
    head = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', head, flags=re.S)
    def meta(m):
        tg = m.group(0)
        if re.search(r'(name="description"|property="og:description")', tg):
            return re.sub(r'content="[^"]*"', 'content="%s"' % html.escape(desc, quote=True), tg, count=1)
        if 'property="og:title"' in tg:
            return re.sub(r'content="[^"]*"', 'content="%s"' % html.escape(title, quote=True), tg, count=1)
        return tg
    head = re.sub(r'<meta\b[^>]*>', meta, head)
    head = head.replace(f'{DOMAIN}{old_path}', f'{DOMAIN}{new_path}')
    head = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', '', head, flags=re.S)
    head = head + ldtag
    if ogimg:
        head = re.sub(r'(https://faindonesia\.co\.id)?/img/og-page/[^"]+\.jpg', DOMAIN + ogimg, head)
    return head + '</head>' + rest


def grab(m, pat):
    x = re.search(pat, m, re.S)
    return x.group(0) if x else ''


def city_page(slug, ogimg):
    src = os.path.join(ROOT, 'konsultan-rumah-sakit', slug, 'index.html')
    t = rd(src)
    m = t[t.find('<main'):t.find('</main>')]
    n = html.unescape(re.search(r'<p class="eyebrow">[^·<]*·\s*([^<]+)</p>', m).group(1).strip())
    kind = 'prov' if slug.startswith('provinsi-') else 'city'
    desc0 = html.unescape(re.search(r'<meta content="([^"]*)" name="description"', t).group(1))
    pm = re.search(r' di ' + re.escape(n) + r', ([^:]+):', desc0)
    prov = pm.group(1).strip() if pm else ''
    if not prov:
        h1 = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', m, re.S).group(1)))
        pm = re.search(re.escape(n) + r', (.+)$', h1); prov = pm.group(1).strip() if pm else ''
    if kind == 'prov': prov = ''
    nE = E(n)
    url = f'{DOMAIN}/{FAM}/{slug}/'
    title = f'Pendanaan Rumah Sakit {n}: Kredit Bank dan Investor'
    if len(title) > 60: title = f'Pendanaan Rumah Sakit {n}: Kredit dan Investor'
    if len(title) > 60: title = f'Pendanaan Rumah Sakit {n}'
    where = f'{n}, {prov}' if prov else n
    desc = f'Pendanaan rumah sakit dan klinik di {where}: kredit modal kerja klaim BPJS, kredit investasi alat dan gedung, investor, dan laporan keuangan siap bank.'
    if len(desc) > 158: desc = f'Pendanaan rumah sakit dan klinik di {n}: kredit modal kerja klaim BPJS, kredit investasi alat dan gedung, investor, dan laporan keuangan siap bank.'
    if len(desc) > 158: desc = f'Pendanaan rumah sakit di {n}: kredit modal kerja klaim BPJS, kredit investasi, investor, dan laporan keuangan siap bank.'
    faqs = faq(n)
    # blok lokal dari halaman sumber
    konteks = grab(m, r'<h2 id="konteks-[^"]*">.*?</p>')
    uq = grab(m, r'<!--uq-lokal-->.*?<!--/uq-lokal-->')
    area = grab(m, r'<!--rsw-area-->.*?<!--/rsw-area-->')
    fnx = grab(m, r'<!--fanas-x-->.*?<!--/fanas-x-->')
    sekitar = grab(m, r'<details class="fold"><summary>Kota Sekitar</summary>.*?</details>').replace('/konsultan-rumah-sakit/', f'/{FAM}/')
    provlist = ''
    if kind == 'prov':
        x = re.search(r'(<h2 id="konsultan-rumah-sakit-di-\d+[^"]*">)(.*?)(</h2>)(.*?)(?=<h2|<!--)', m, re.S)
        if x:
            body = x.group(4).replace('/konsultan-rumah-sakit/', f'/{FAM}/')
            ht = x.group(2).replace('Konsultan Rumah Sakit', 'Pendanaan Rumah Sakit')
            provlist = f'<h2 id="{slugify(ht)}">{ht}</h2>{body}'
    rsd = grab(m, r'<!--fa-rsd-->.*?<!--/fa-rsd-->')
    wa = f'https://wa.me/{WA}?text=' + quote(f'Halo Pak Ananta, saya dari rumah sakit di {n}, ingin diskusi pendanaan rumah sakit.')
    secs = []
    def sec(h, body, hid=None):
        hid = hid or slugify(h); secs.append((hid, h)); return f'<h2 id="{hid}">{h}</h2>{body}'
    parts = [
        sec(f'Mengapa Rumah Sakit di {nE} Perlu Menata Pendanaan Sekarang', f'<p>{E(pick(slug + "w", WHY).format(n=n))}</p><p>Bacaan lengkapnya: <a href="/artikel/{SLUG}/">Sektor Kesehatan Sesak Napas, Rumah Sakit Jangan Ikut Menahan Napas</a>.</p>'),
        sec(f'Sumber Dana untuk Rumah Sakit di {nE}', TABLE),
        sec('Lima Langkah Sebelum Mengajukan Dana', '<ol>' + ''.join(f'<li>{x}</li>' for x in STEPS) + '</ol>'),
        sec('Yang Dikerjakan Tim FA Indonesia', '<ul><li><b>Diagnosis awal:</b> laporan keuangan, piutang klaim, dan arus kas.</li><li><b>Business wrapping dan valuasi:</b> cerita bisnis, proyeksi, dan nilai rumah sakit dalam bahasa bank dan investor.</li><li><b>Laporan keuangan siap bank:</b> penyusunan oleh KJA Farhani K.N., audit oleh KAP DHN &amp; Rekan (terdaftar OJK).</li><li><b>Pendampingan pendanaan:</b> dari pengajuan kredit sampai pembicaraan dengan investor.</li></ul>'),
        sec('Ukur Dulu Posisi Rumah Sakit Anda', TOOLS),
    ]
    if provlist:
        x = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', provlist); secs.append((x.group(1), x.group(2))); parts.append(provlist)
    if konteks:
        konteks = re.sub(r'<h2 id="[^"]*">', f'<h2 id="konteks-{slug}">', konteks, count=1)
        x = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', konteks); secs.append((x.group(1), x.group(2))); parts.append(konteks)
    if area:
        x = re.search(r'<h2 id="([^"]+)">(.*?)</h2>', area)
        if x: secs.append((x.group(1), html.unescape(re.sub(r'<[^>]+>', '', x.group(2)))))
        area = re.sub(r'<p>Kami melayani .*?</p>', f'<p>Pendampingan pendanaan untuk rumah sakit, RSIA, dan klinik di seluruh {nE}, termasuk kecamatan dan desa/kelurahan berikut. Pertemuan bisa di lokasi Anda atau daring.</p>', area, count=1, flags=re.S)
        parts.append(area)
    parts.append(f'<h2 id="bacaan-pendanaan-rumah-sakit">Bacaan Terkait</h2>{read_list()}')
    secs.append(('bacaan-pendanaan-rumah-sakit', 'Bacaan Terkait'))
    if rsd:
        parts.append(rsd.replace('</p><!--/fa-rsd-->', f' · <a href="/{FAM}/{slug}/">Pendanaan Rumah Sakit</a></p><!--/fa-rsd-->') if f'/{FAM}/' not in rsd else rsd)
    else:
        parts.append(f'<p class="t">Layanan rumah sakit di {nE}: <a href="/konsultan-rumah-sakit/{slug}/">Konsultan Rumah Sakit</a> · <a href="/konsultan-klinik/{slug}/">Konsultan Klinik</a> · <a href="/konsultan-unit-cost-rumah-sakit/{slug}/">Unit Cost</a></p>' if os.path.exists(os.path.join(ROOT, 'konsultan-klinik', slug)) else f'<p class="t">Layanan rumah sakit di {nE}: <a href="/konsultan-rumah-sakit/{slug}/">Konsultan Rumah Sakit</a></p>')
    if sekitar: parts.append(sekitar)
    if fnx: parts.append(fnx)
    if uq: parts.append(uq)
    nav = '<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>' + ''.join(f'<li><a href="#{i}">{h}</a></li>' for i, h in secs) + '</ol></nav>'
    faq_html = '<h2>Pertanyaan Umum</h2>\n<div class="faq-acc">' + ''.join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{E(x)}</p></details>' for q, x in faqs) + '</div>\n'
    main = (f'<main id="top">\n<section class="block">\n<div class="wrap art">\n'
            f'<p class="eyebrow">Pendanaan Rumah Sakit · {nE}</p>\n'
            f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">Pendanaan Rumah Sakit di {nE}</h1>'
            f'<div class="tshare-top"><div class="share" data-lab="Bagikan" data-tool="Pendanaan Rumah Sakit di {html.escape(n, quote=True)}"></div></div>\n'
            f'<p class="t" style="max-width:62em">{E(pick(slug, INTRO).format(n=n))}</p>\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px"><a class="btn solid" href="{wa}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
            f'<a class="btn line" href="/konsultan-rumah-sakit/{slug}/">Konsultan Rumah Sakit {nE}</a></div>'
            f'<div style="margin:30px 0 8px">{rstim_block(n)}</div>\n'
            + nav + ''.join(parts) + faq_html + '</div>\n</section>\n')
    s = t[:t.find('<main')] + main + t[t.find('</main>'):]
    s = set_head(s, f'/konsultan-rumah-sakit/{slug}/', f'/{FAM}/{slug}/', title, desc, ld(url, f'Pendanaan Rumah Sakit di {n}', n, prov, faqs, kind), ogimg)
    return s, n


def pilar(ogimg, names):
    t = rd(os.path.join(ROOT, 'konsultan-rumah-sakit', 'index.html'))
    m = t[t.find('<main'):t.find('</main>')]
    hub = grab(m, r'<!--fanas-hub-->.*?<!--/fanas-hub-->').replace('/konsultan-rumah-sakit/', f'/{FAM}/').replace('Konsultan Rumah Sakit', 'Pendanaan Rumah Sakit').replace('<!--fanas-hub-->', '').replace('<!--/fanas-hub-->', '')
    rsw = grab(m, r'<!--rsw-hub-->.*?<!--/rsw-hub-->').replace('/konsultan-rumah-sakit/', f'/{FAM}/').replace('Konsultan Rumah Sakit', 'Pendanaan Rumah Sakit').replace('<!--rsw-hub-->', '').replace('<!--/rsw-hub-->', '')
    rsw = rsw.replace('konsultan-rumah-sakit-di-seluruh', 'pendanaan-rumah-sakit-di-seluruh')
    faqs = [('Apa saja sumber dana untuk rumah sakit swasta?', 'Kredit modal kerja (termasuk berbasis piutang klaim), kredit investasi alat dan gedung, sindikasi, sewa pembiayaan, serta investor ekuitas dan mitra strategis.'),
            ('Apakah utang berbahaya untuk rumah sakit?', 'Tidak, selama terukur. Kapasitas utang dihitung dari proyeksi arus kas dan DSCR supaya cicilan sanggup dibayar dari operasional.'),
            ('Apakah FA Indonesia melayani rumah sakit di daerah saya?', 'Ya. Pendampingan berjalan daring dengan kunjungan lapangan bila diperlukan, untuk rumah sakit dan klinik di seluruh kabupaten dan kota di Indonesia.')]
    secs = []
    def sec(h, body):
        i = slugify(h); secs.append((i, h)); return f'<h2 id="{i}">{h}</h2>{body}'
    wa = f'https://wa.me/{WA}?text=' + quote('Halo Pak Ananta, saya dari rumah sakit dan ingin diskusi pendanaan rumah sakit.')
    parts = [sec('Sektor Kesehatan Sedang Sesak Napas', '<p>Pada Hari Kesehatan Nasional 2026, opini Prof. Laksono Trisnantoro di Kompas mencatat belanja kesehatan Indonesia sekitar Rp600 triliun atau 2,7% PDB (2023), lebih rendah dari kisaran 3% saat BPJS dimulai, dan mengusulkan sasaran 4% PDB. Di tingkat rumah sakit, kekurangan dana terasa sebagai piutang klaim yang menumpuk, margin JKN yang tipis, dan ekspansi yang tertunda.</p>'
                 f'<p>Kebijakan nasional butuh waktu. Rumah sakit bisa mulai menata pendanaannya sekarang. Ulasan lengkap: <a href="/artikel/{SLUG}/">Sektor Kesehatan Sesak Napas, Rumah Sakit Jangan Ikut Menahan Napas</a>.</p>'),
             sec('Sumber Dana untuk Rumah Sakit', TABLE),
             sec('Lima Langkah Sebelum Mengajukan Dana', '<ol>' + ''.join(f'<li>{x}</li>' for x in STEPS) + '</ol>'),
             sec('Yang Dikerjakan Tim FA Indonesia', '<ul><li><b>Diagnosis awal:</b> laporan keuangan, piutang klaim, dan arus kas.</li><li><b>Business wrapping dan valuasi:</b> cerita bisnis, proyeksi, dan nilai rumah sakit dalam bahasa bank dan investor.</li><li><b>Laporan keuangan siap bank:</b> penyusunan oleh KJA Farhani K.N., audit oleh KAP DHN &amp; Rekan (terdaftar OJK).</li><li><b>Pendampingan pendanaan:</b> dari pengajuan kredit sampai pembicaraan dengan investor.</li></ul>'),
             sec('Ukur Dulu Posisi Rumah Sakit Anda', TOOLS)]
    if hub:
        x = re.search(r'<h2[^>]*>(.*?)</h2>', hub); h = x.group(1); i = 'pendanaan-rumah-sakit-per-provinsi'
        hub = hub.replace(x.group(0), f'<h2 id="{i}">{h}</h2>', 1); secs.append((i, h)); parts.append(hub)
    if rsw:
        x = re.search(r'<h2 id="([^"]+)">(.*?)</h2>', rsw); secs.append((x.group(1), x.group(2))); parts.append(rsw)
    parts.append(sec('Bacaan Terkait', read_list()))
    nav = '<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>' + ''.join(f'<li><a href="#{i}">{h}</a></li>' for i, h in secs) + '</ol></nav>'
    faq_html = '<h2>Pertanyaan Umum</h2>\n<div class="faq-acc">' + ''.join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{E(x)}</p></details>' for q, x in faqs) + '</div>\n'
    main = ('<main id="top">\n<section class="block">\n<div class="wrap art">\n<p class="eyebrow">Layanan · Rumah Sakit</p>\n'
            '<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">Pendanaan Rumah Sakit: Kredit Bank, Investor, dan Laporan Keuangan Siap Bank</h1>'
            '<div class="tshare-top"><div class="share" data-lab="Bagikan" data-tool="Pendanaan Rumah Sakit"></div></div>\n'
            '<p class="t" style="max-width:62em">Pendampingan pendanaan untuk rumah sakit dan klinik swasta di seluruh Indonesia: mengubah piutang klaim menjadi kas, mengukur kapasitas utang, menyiapkan laporan keuangan siap bank, sampai kredit bank dan investor.</p>\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px"><a class="btn solid" href="{wa}" rel="noopener" target="_blank">Chat Ananta, CPA</a><a class="btn line" href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a></div>'
            f'<div style="margin:30px 0 8px">{rstim_block()}</div>\n' + nav + ''.join(parts) + faq_html + '</div>\n</section>\n')
    s = t[:t.find('<main')] + main + t[t.find('</main>'):]
    title = 'Pendanaan Rumah Sakit: Kredit Bank dan Investor | FA Indonesia'
    desc = 'Pendanaan rumah sakit dan klinik swasta: kredit modal kerja klaim BPJS, kredit investasi alat dan gedung, investor, dan laporan keuangan siap bank.'
    g = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Service', 'name': 'Pendanaan Rumah Sakit', 'serviceType': 'Pendanaan Rumah Sakit',
         'provider': {'@type': 'ProfessionalService', '@id': DOMAIN + '/#org', 'name': 'FA Indonesia', 'url': DOMAIN + '/'},
         'areaServed': {'@type': 'Country', 'name': 'Indonesia'}, 'url': f'{DOMAIN}/{FAM}/'},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in faqs]}]}
    s = set_head(s, '/konsultan-rumah-sakit/', f'/{FAM}/', title, desc, '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + '</script>', ogimg)
    return s


# ------------------------------------------------------------------ 3. link balik + sitemap
def backlinks(slugs, names, a):
    n_rs = 0
    for slug in slugs:
        p = os.path.join(ROOT, 'konsultan-rumah-sakit', slug, 'index.html'); s = rd(p)
        s = re.sub(r'<!--rssn-l-->.*?<!--/rssn-l-->', '', s, flags=re.S)
        blk = (f'<!--rssn-l--><p class="t"><b>Pendanaan rumah sakit di {E(names[slug])}:</b> kredit modal kerja klaim BPJS, kredit investasi, dan investor. '
               f'<a href="/{FAM}/{slug}/">Pendanaan Rumah Sakit {E(names[slug])}</a> · <a href="/artikel/{SLUG}/">Sektor Kesehatan Sesak Napas</a></p><!--/rssn-l-->')
        k = s.find('<h2>Pertanyaan Umum</h2>')
        if k < 0: continue
        wr(p, s[:k] + blk + s[k:]); n_rs += 1
    # pilar konsultan RS
    p = os.path.join(ROOT, 'konsultan-rumah-sakit', 'index.html'); s = rd(p)
    s = re.sub(r'<!--rssn-l-->.*?<!--/rssn-l-->', '', s, flags=re.S)
    blk = f'<!--rssn-l--><p class="t"><b>Pendanaan rumah sakit:</b> kredit bank, investor, dan laporan keuangan siap bank di setiap kabupaten dan kota. <a href="/{FAM}/">Pendanaan Rumah Sakit</a> · <a href="/artikel/{SLUG}/">Sektor Kesehatan Sesak Napas</a></p><!--/rssn-l-->'
    k = s.find('<h2>Pertanyaan Umum</h2>'); wr(p, s[:k] + blk + s[k:])
    # kecamatan: baris rsw-kec
    n_kec = 0
    for p in glob.glob(os.path.join(ROOT, 'wilayah', '*', 'kecamatan', '*', 'index.html')):
        s = rd(p)
        x = re.search(r'<!--rsw-kec-->(.*?)<!--/rsw-kec-->', s, re.S)
        if not x: continue
        inner = re.sub(r'<!--rssn-k-->.*?<!--/rssn-k-->', '', x.group(1))
        cm = re.search(r'href="/konsultan-rumah-sakit/([^/]+)/"', inner)
        if not cm or not os.path.exists(os.path.join(ROOT, 'konsultan-rumah-sakit', cm.group(1))): continue
        inner = inner.replace('</p>', f'<!--rssn-k--> · <a href="/{FAM}/{cm.group(1)}/">Pendanaan Rumah Sakit</a><!--/rssn-k--></p>', 1)
        wr(p, s[:x.start(1)] + inner + s[x.end(1):]); n_kec += 1
    # Baca Juga balik di artikel RS terkait
    for r in a['related'][:4]:
        p = os.path.join(ROOT, 'artikel', r, 'index.html'); s = rd(p)
        s = re.sub(r'<!--rssn-->.*?<!--/rssn-->', '', s, flags=re.S)
        k = s.find('<h2>Baca Juga</h2><ul>')
        if k < 0: continue
        k += len('<h2>Baca Juga</h2><ul>')
        wr(p, s[:k] + f'<!--rssn--><li><a href="/artikel/{SLUG}/">{E(a["title"])}</a></li><!--/rssn-->' + s[k:])
    return n_rs, n_kec


def sitemap_llms_eksplor(slugs, a):
    p = os.path.join(ROOT, 'sitemap.xml'); sm = rd(p)
    sm = re.sub(r'<!--rssn-->.*?<!--/rssn-->\n?', '', sm, flags=re.S)
    urls = [f'/artikel/{SLUG}/', f'/{FAM}/'] + [f'/{FAM}/{s}/' for s in slugs]
    blk = '<!--rssn-->' + ''.join(f'<url><loc>{DOMAIN}{u}</loc><lastmod>{DATE}</lastmod><priority>{"0.8" if i < 2 else "0.6"}</priority></url>' for i, u in enumerate(urls)) + '<!--/rssn-->\n'
    wr(p, sm.replace('</urlset>', blk + '</urlset>'))
    p = os.path.join(ROOT, 'llms.txt'); L = rd(p)
    for line in [f'- {a["title"]} → {DOMAIN}/artikel/{SLUG}/', f'- Pendanaan Rumah Sakit (kredit bank, investor, per kabupaten/kota) → {DOMAIN}/{FAM}/']:
        if line not in L:
            k = L.find('- Titik Impas Rumah Sakit per DPJP')
            L = L[:k] + line + '\n' + L[k:] if k >= 0 else L + '\n' + line
    wr(p, L)
    p = os.path.join(ROOT, 'artikel', 'index.html'); s = rd(p)
    if f'href="/artikel/{SLUG}/"' not in s:
        card = f'<a class="card2" href="/artikel/{SLUG}/"><b>{E(a["title"])}</b><span>{E(a["description"])}</span></a>'
        k = s.find('<a class="card2" href="/artikel/')
        wr(p, s[:k] + card + s[k:])
    return len(urls)


def main():
    a = article()
    import share_all
    og = share_all._poster('fa', 'Rumah Sakit · Pendanaan', 'Pendanaan Rumah Sakit: Kredit Bank dan Investor', 'sec-pendanaan-rumah-sakit', ROOT) if not DRY else '/img/og-page/sec-konsultan-rumah-sakit.jpg'
    slugs = sorted(d for d in os.listdir(os.path.join(ROOT, 'konsultan-rumah-sakit'))
                   if os.path.exists(os.path.join(ROOT, 'konsultan-rumah-sakit', d, 'index.html')))
    names = {}
    for slug in slugs:
        s, n = city_page(slug, og); names[slug] = n
        wr(os.path.join(ROOT, FAM, slug, 'index.html'), s)
    wr(os.path.join(ROOT, FAM, 'index.html'), pilar(og, names))
    n_rs, n_kec = backlinks(slugs, names, a)
    nu = sitemap_llms_eksplor(slugs, a)
    print(f'ok: artikel 1, {FAM} {len(slugs)} daerah + pilar, link balik RS {n_rs}, kecamatan {n_kec}, sitemap {nu} URL, file ditulis {len(written)}' + (' (DRY)' if DRY else ''))


if __name__ == '__main__':
    main()
