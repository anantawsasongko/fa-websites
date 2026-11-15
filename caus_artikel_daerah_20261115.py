#!/usr/bin/env python3
"""15 Nov 2026 (Bos): artikel SEO daerah untuk CariAkuntan dan UpdateSAK, masing-masing 10 (3 unit cost ABC, 3 pendanaan RS
dari PE dan VC, 4 fractional CFO), satu kota per artikel, dengan poster foto. Pasangan fa_artikel_daerah_20261115.py.
BEKERJA DI out/cariakuntan dan out/updatesak (template = halaman artikel live), idempoten. Dry run: --dry.

Konten: fa_content/daerah20261115/{ca,us}.py. Sudut CA: memilih profesional dan kantor, lalu rekanan (tim FA Indonesia).
Sudut US: standar dan perhitungan teknis, lalu dibantu tim FA Indonesia. Tidak ada teks yang disalin antar situs.
CA: /artikel/<slug>/ (template /artikel/audit-pajak-kredit-bank-malang-raya/), og /img/og-art/<slug>.jpg; kartu + chip di
    /artikel/ (<!--ca-dae15-->), sitemap, llms.txt, lipatan <!--ca-dae15l--> "Wawasan untuk <kota>" di hub /kota/<kota>/.
US: /artikel/<slug>/ (template /artikel/lima-langkah-psak-115-kontraktor/), og /img/share/art-<slug>-og.jpg;
    /img/share/art-<slug>-feed.jpg; grup di /eksplor/ (<!--us-dae15-->), sitemap, llms.txt, baris <!--us-dae15l--> di /psak/<no>/.
Halaman lama hanya berubah di dalam blok berpenanda. Jalankan sesudah caus_rapi_20261113.py dan segmen_caus_20261113.py,
Kelas tabel untuk HP dipasang langsung lewat fix_table() teks_rapi_20261113.py.
"""
import os, re, sys, json, html
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
DRY = '--dry' in sys.argv
sys.path.insert(0, os.path.join(HERE, 'fa_content', 'daerah20261115'))
import _k, ca, us
import poster_daerah as poster
_k.check()
CA_A = [a for a in _k.ARTS if a['site'] == 'ca']; US_A = [a for a in _k.ARTS if a['site'] == 'us']
CAD, USD = 'https://cariakuntan.com', 'https://updatesak.com'
DATE = '2026-11-15'; DATE_ID = '15 November 2026'
WA = '6282245260121'
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('teksrapi', os.path.join(HERE, 'teks_rapi_20261113.py'))
TR = _ilu.module_from_spec(_sp); _sp.loader.exec_module(TR)      # fix_table: kelas tabel untuk HP (kartu bertumpuk / geser)


def tbl_hp(s): return TR.RE_TABLE.sub(lambda m: TR.fix_table(m.group(0)), s)

E = lambda s: html.escape(s, quote=False)
EQ = lambda s: html.escape(s, quote=True)
written = []


def rd(p): return open(p, encoding='utf-8').read()


def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return
    written.append(os.path.relpath(p, OUT))
    if DRY: return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)


def wa(t): return f'https://wa.me/{WA}?text=' + quote(t, safe='')


def hid(t): return re.sub(r'[^a-z0-9]+', '-', html.unescape(re.sub(r'<[^>]+>', '', t)).lower()).strip('-')[:70]


def folds(b):
    """<div class="pf-fold">...</div> (boleh berisi div lain) -> lipatan ber-id + tombol Baca Selengkapnya."""
    out, pos, n = [], 0, 0
    while True:
        i = b.find('<div class="pf-fold">', pos)
        if i < 0: break
        j, depth = i + len('<div class="pf-fold">'), 1
        while depth:
            m = re.compile(r'<div\b|</div>').search(b, j)
            depth += 1 if m.group(0) != '</div>' else -1; j = m.end()
        n += 1; inner = b[i + len('<div class="pf-fold">'):j - 6]
        out.append(b[pos:i] + f'<div class="pf-fold" id="pf{n}">{inner}</div><button aria-controls="pf{n}" aria-expanded="false" '
                   f'class="pf-more" data-for="pf{n}" type="button">Baca Selengkapnya </button>')
        pos = j
    return ''.join(out) + b[pos:]


def tables(b, site):
    def rep(m):
        t = m.group(1)
        if site == 'us':
            t = re.sub(r'<tr>((?:<td><b>.*?</b></td>|<td></td>)+)</tr>', lambda x: '<tr class="t">' + x.group(1) + '</tr>', t)
            return f'<div class="scroll"><table class="tbl">{t}</table></div>'
        return f'<div class="tx"><table>{t}</table></div>'
    return re.sub(r'<div class="tblwrap"><table class="tbl">(.*?)</table></div>', rep, b, flags=re.S)


def body(a, tanya):
    b = tables(folds(a['body_html'].strip()), a['site'])
    heads = []
    def h2(m):
        i = hid(m.group(1)); heads.append((i, m.group(1))); return f'<h2 id="{i}">{m.group(1)}</h2>'
    b = re.sub(r'<h2>(.*?)</h2>', h2, b)
    nav = '<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>' + ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads) + '</ol></nav>'
    k = b.find('<h2 '); b = b[:k] + nav + b[k:]
    k2 = b.find('<h2 ', b.find('<h2 ') + 4)          # kotak tanya sebelum H2 kedua
    return b[:k2] + tanya + b[k2:]


def ld(graph): return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>'


def faq_ld(a): return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in a['faq']]}


def setmeta(h, attr, key, val):
    def rep(m):
        tg = m.group(0)
        return re.sub(r'content="[^"]*"', 'content="%s"' % EQ(val), tg, count=1) if re.search(r'%s="%s"' % (attr, re.escape(key)), tg) else tg
    return re.sub(r'<meta\b[^>]*>', rep, h)


FIG_CSS = ('<style id="dae-fig-css">.dae-fig{margin:14px 0 22px;padding:0}.dae-fig img{display:block;width:100%;height:auto;'
           'border:1px solid rgba(127,127,127,.28);border-radius:10px}</style>')


def fig(a, src): return f'<figure class="dae-fig"><img alt="{EQ(a["title"])}" decoding="async" height="630" src="{src}" width="1200"/></figure>'


# ====================================================================== CariAkuntan
CA_TPL = 'audit-pajak-kredit-bank-malang-raya'
CA_OLD = ['audit-pajak-kredit-bank-surabaya-sidoarjo-gresik', 'agreed-upon-procedures-aup-beda-dengan-audit', 'laporan-keuangan-untuk-investor-dan-due-diligence']


def ca_title(slug):
    return re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', rd(os.path.join(OUT, 'cariakuntan', 'artikel', slug, 'index.html')), re.S).group(1)).strip()


def ca_page(a, tpl):
    url = f'{CAD}/artikel/{a["slug"]}/'; img = f'/img/og-art/{a["slug"]}.jpg'
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<title>.*?</title>', f'<title>{E(a["seo_title"])}</title>', head, count=1, flags=re.S)
    head = setmeta(head, 'name', 'description', a['description'])
    head = setmeta(head, 'property', 'og:title', a['title'] + ' | cariakuntan.com')
    head = setmeta(head, 'property', 'og:description', a['description'])
    head = head.replace(f'{CAD}/artikel/{CA_TPL}/', url).replace(f'/img/og-art/{CA_TPL}.jpg', img)
    graph = [{'@type': 'Article', 'headline': a['title'], 'description': a['description'], 'url': url, 'mainEntityOfPage': url, 'inLanguage': 'id-ID',
              'datePublished': DATE, 'dateModified': DATE, 'image': CAD + img, 'keywords': a['keyword'], 'articleSection': a['category'],
              'author': {'@type': 'Person', 'name': 'Ananta', 'honorificSuffix': 'CPA'},
              'publisher': {'@type': 'Organization', 'name': 'cariakuntan.com', 'url': CAD + '/'}},
             {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': CAD + '/'},
                                                             {'@type': 'ListItem', 'position': 2, 'name': 'Wawasan', 'item': CAD + '/artikel/'},
                                                             {'@type': 'ListItem', 'position': 3, 'name': a['title'], 'item': url}]}, faq_ld(a)]
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: ld(graph), head, count=1, flags=re.S)
    assert CA_TPL not in head, 'sisa template di head CA'
    if 'dae-fig-css' not in head: head += FIG_CSS
    t = a['title']
    tanya = ('<!--ca-tanya--><section class="ca-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Dulu ke Ananta, CPA</b>'
             '<p>Kasus Anda mirip dengan artikel ini? Tanyakan dulu, gratis, sebelum memilih kantor.</p><div class="q">'
             f'<a class="w" href="{wa(f"Halo Pak Ananta, saya baca \"{t}\" di cariakuntan.com. Mau tanya untuk usaha kami: ")}" target="_blank" rel="noopener" data-ca-q="artikel">Tanya soal ini untuk usaha saya</a>'
             f'<a class="" href="{wa(f"Halo Pak Ananta, saya baca \"{t}\" di cariakuntan.com. Kami bingung perlu KAP, KJA, atau konsultan pajak.")}" target="_blank" rel="noopener" data-ca-q="artikel">Perlu KAP, KJA, atau konsultan pajak?</a></div></section><!--/ca-tanya-->')
    faq = '<h2 id="tanya-jawab">Tanya Jawab</h2>' + ''.join(f'<h3>{E(q)}</h3><p>{E(x)}</p>' for q, x in a['faq'])
    src = ('<p class="src">Sumber: ' + '; '.join(f'<a href="{u}" rel="noopener nofollow" target="_blank">{E(tt)}</a>' for tt, u in a['sources'])
           + '. Ringkasan dan analisis ditulis oleh cariakuntan.com.</p>') if a['sources'] else ''
    same = [x for x in CA_A if x is not a and x['topik'] == a['topik']] + [x for x in CA_A if x is not a and x['topik'] != a['topik']][:2]
    more = ''.join(f'<a href="/artikel/{x["slug"]}/">{E(x["title"])}</a>' for x in same) + ''.join(f'<a href="/artikel/{s}/">{E(ca_title(s))}</a>' for s in CA_OLD)
    main = (f'<main class="wrap art">\n<p class="crumb"><a href="/">Beranda</a> / <a href="/artikel/">Wawasan</a></p>\n'
            f'<p class="label" style="margin-top:14px">{E(a["category"])}</p>\n<h1>{E(a["title"])}</h1>\n<p class="sub">{E(a["description"])}</p>\n'
            f'<p class="meta-line">Ananta, CPA · {DATE}</p>\n{fig(a, img)}\n'
            f'<article class="prose">{body(a, tanya)}\n{faq}</article>{src}\n'
            f'<div class="cta-box"><h3>Diskusikan Kebutuhan Anda</h3><p style="color:var(--muted)">Ceritakan kondisi usaha Anda. Kami bantu memetakan jenis kantor dan pekerjaan yang benar-benar diperlukan.</p>'
            f'<a class="btn btn-wa" href="{wa(a["wa"])}" rel="noopener" style="justify-self:start" target="_blank">Tanya Ananta, CPA</a></div>\n'
            f'<details class="fold"><summary>Wawasan Lainnya</summary>{more}</details>\n')
    i = rest.find('<main'); j = rest.find('</main>')
    s = head + '</head>' + rest[:i] + main + rest[j:]
    return tbl_hp(s.replace(EQ('Audit, Pajak, dan Kredit Bank untuk Usaha di Malang Raya'), EQ(t)))


def ca_all():
    root = os.path.join(OUT, 'cariakuntan')
    tpl = rd(os.path.join(root, 'artikel', CA_TPL, 'index.html'))
    for a in CA_A:
        s = ca_page(a, tpl)
        assert s.count('<h1') == 1 and 'Malang Raya' not in s.split('<main')[1].split('</main>')[0], a['slug']
        wr(os.path.join(root, 'artikel', a['slug'], 'index.html'), s)
        if not DRY: poster.og('ca', a['topik'], a['kota'], a['title'], os.path.join(root, 'img', 'og-art', a['slug'] + '.jpg'))
    # hub Wawasan
    p = os.path.join(root, 'artikel', 'index.html'); s = rd(p)
    s = re.sub(r'<!--ca-dae15-->.*?<!--/ca-dae15-->', '', s, flags=re.S); s = re.sub(r'<!--ca-dae15c-->.*?<!--/ca-dae15c-->', '', s, flags=re.S)
    cards = '<!--ca-dae15-->' + ''.join(f'<a class="card" data-t="{EQ(a["category"])}" href="/artikel/{a["slug"]}/"><span class="label">{E(a["category"])} · {DATE}</span>'
                                       f'<h2 style="font-size:1.2rem">{E(a["title"])}</h2><p>{E(a["description"])}</p></a>' for a in CA_A) + '<!--/ca-dae15-->'
    k = s.find('<a class="card" '); s = s[:k] + cards + s[k:]
    chips = set(re.findall(r'<button class="chip" data-t="([^"]+)"', s))
    newc = ''.join(f'<button class="chip" data-t="{EQ(c)}">{E(c)}</button>' for c in dict.fromkeys(a['category'] for a in CA_A) if c not in chips)
    if newc:
        k = s.find('</div><p class="cnt" id="cnt">'); s = s[:k] + '<!--ca-dae15c-->' + newc + '<!--/ca-dae15c-->' + s[k:]
    n = s.count('<a class="card" ')
    ms = list(re.finditer(r'(<button class="tidy-clipbtn" type="button">Lihat Semua \()\d+(\)</button>)', s))
    m = ms[-1]                                   # tombol terakhir = daftar artikel (yang pertama milik Berita Terkini)
    s = s[:m.start()] + m.group(1) + str(n) + m.group(2) + s[m.end():]
    wr(p, s)
    # sitemap + llms
    p = os.path.join(root, 'sitemap.xml'); sm = re.sub(r'<!--cadae15-->.*?<!--/cadae15-->\n?', '', rd(p), flags=re.S)
    blk = '<!--cadae15-->' + ''.join(f'  <url><loc>{CAD}/artikel/{a["slug"]}/</loc><lastmod>{DATE}</lastmod></url>\n' for a in CA_A) + '<!--/cadae15-->\n'
    wr(p, sm.replace('</urlset>', blk + '</urlset>'))
    p = os.path.join(root, 'llms.txt'); L = rd(p)
    add = ''.join(f'- [{a["title"]}]({CAD}/artikel/{a["slug"]}/): {a["description"]}\n' for a in CA_A if f'/artikel/{a["slug"]}/' not in L)
    if add:
        k = L.find('- [Cara Menghitung Kerugian Penipuan untuk Laporan Polisi]'); wr(p, L[:k] + add + L[k:] if k >= 0 else L.rstrip('\n') + '\n' + add)
    # hub kota
    for a in CA_A:
        p = os.path.join(root, 'kota', a['kota_slug'], 'index.html')
        if not os.path.exists(p): print('tidak ada hub kota CA', a['kota_slug']); continue
        s = re.sub(r'<!--ca-dae15l-->.*?<!--/ca-dae15l-->', '', rd(p), flags=re.S)
        items = [x for x in CA_A if x['kota_slug'] == a['kota_slug']]
        blk = (f'<!--ca-dae15l--><details class="fold"><summary>Wawasan untuk {E(a["kota"])}</summary><div class="citylist">'
               + ' '.join(f'<a href="/artikel/{x["slug"]}/">{E(x["title"])}</a>' for x in items) + '</div></details><!--/ca-dae15l-->')
        k = s.find('<!--/ca-seg-->')
        if k < 0: print('tanpa ca-seg', a['kota_slug']); continue
        k += len('<!--/ca-seg-->'); wr(p, s[:k] + blk + s[k:])


# ====================================================================== UpdateSAK
US_TPL = 'lima-langkah-psak-115-kontraktor'
US_OLD = {'abc': ['contoh-jurnal-penyusutan-aset-tetap-psak-216', 'laporan-arus-kas-cara-menyusun'],
          'pe': ['red-flag-psak-due-diligence-calon-investee', 'membaca-nilai-usaha-dari-laporan-keuangan'],
          'cfo': ['kalender-tutup-buku-akhir-tahun-2026', 'laporan-arus-kas-metode-tidak-langsung']}


def us_h1(path):
    return re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', rd(os.path.join(OUT, 'updatesak', *path.strip('/').split('/'), 'index.html')), re.S).group(1)).strip()


def us_page(a, tpl):
    url = f'{USD}/artikel/{a["slug"]}/'; img = f'/img/share/art-{a["slug"]}-og.jpg'; feed = f'/img/share/art-{a["slug"]}-feed.jpg'
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<title>.*?</title>', f'<title>{E(a["seo_title"])}</title>', head, count=1, flags=re.S)
    head = setmeta(head, 'name', 'description', a['description'])
    head = setmeta(head, 'property', 'og:title', a['title'])
    head = setmeta(head, 'property', 'og:description', a['description'])
    head = head.replace(f'{USD}/artikel/{US_TPL}/', url).replace(f'/img/share/art-{US_TPL}-og.jpg', img)
    graph = [{'@type': 'Article', 'headline': a['title'], 'description': a['description'], 'inLanguage': 'id', 'url': url, 'mainEntityOfPage': url,
              'image': USD + img, 'datePublished': DATE, 'dateModified': DATE, 'keywords': a['keyword'], 'articleSection': a['category'],
              'author': {'@type': 'Organization', 'name': 'Tim UpdateSAK', 'url': USD + '/'},
              'publisher': {'@type': 'Organization', 'name': 'FA Indonesia', 'url': 'https://faindonesia.co.id/'}},
             {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'UpdateSAK', 'item': USD + '/'},
                                                             {'@type': 'ListItem', 'position': 2, 'name': 'Eksplor', 'item': USD + '/eksplor/'},
                                                             {'@type': 'ListItem', 'position': 3, 'name': a['title'], 'item': url}]}, faq_ld(a)]
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: ld(graph), head, count=1, flags=re.S)
    assert US_TPL not in head, 'sisa template di head US'
    if 'dae-fig-css' not in head: head += FIG_CSS
    t = a['title']
    tanya = ('<!--us-tanya--><section class="us-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Ananta, CPA</b>'
             '<p>Ada kasus di perusahaan Anda yang mirip? Tanyakan dulu, gratis.</p><div class="q">'
             f'<a class="w" href="{wa(f"Halo Pak Ananta, saya baca \"{t}\" di updatesak.com. Mau tanya untuk usaha kami: ")}" target="_blank" rel="noopener" data-us-q="artikel">Tanya soal topik ini untuk usaha saya</a>'
             f'<a class="" href="{wa(a["wa"])}" target="_blank" rel="noopener" data-us-q="artikel">Dibantu menerapkan di perusahaan kami</a></div></section><!--/us-tanya-->')
    share = (f'<div class="share"><span>Bagikan</span>\n<a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(url, safe="")}" rel="noopener" target="_blank">LinkedIn</a>\n'
             f'<a href="https://wa.me/?text={quote(t + " " + url, safe=":/")}" rel="noopener" target="_blank">WhatsApp</a>\n'
             f'<button data-copy="{url}" type="button">Salin Link</button></div>')
    chips = ''.join(f'<a class="pchip" href="/psak/{nn}/"><b>PSAK {nn}</b><span>{E(re.sub(r"^PSAK " + nn + r"[:\s]*", "", us_h1("/psak/" + nn)))}</span></a>' for nn in a['psak'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(x)}</p></details>' for q, x in a['faq'])
    same = [x for x in US_A if x is not a and x['topik'] == a['topik']]
    reads = ''.join(f'<a href="/artikel/{x["slug"]}/"><b>{E(x["title"])}</b><small>{E(x["category"])}</small></a>' for x in same) + \
        ''.join(f'<a href="/artikel/{s}/"><b>{E(us_h1("/artikel/" + s))}</b><small>Laporan Keuangan</small></a>' for s in US_OLD[a['topik']])
    src = ('<h2 id="sumber">Sumber</h2><ul>' + ''.join(f'<li><a href="{u}" rel="noopener nofollow" target="_blank">{E(tt)}</a></li>' for tt, u in a['sources']) + '</ul>') if a['sources'] else ''
    main = (f'<main>\n<article class="art"><div class="wrap">\n<nav class="crumb"><a href="/">Beranda</a> / <a href="/eksplor/">Eksplor</a> / <a href="/eksplor/#artikel">{E(a["category"])}</a></nav>\n'
            f'<p class="label">{E(a["category"])}</p>\n<h1>{E(t)}</h1>\n<p class="lede">{E(a["description"])}</p>\n'
            f'<p class="upd">Tim UpdateSAK · Diperbarui {DATE_ID} · Ditinjau Ananta W. Sasongko, CPA</p>\n{share}\n{fig(a, img)}\n'
            f'<div class="prose">{body(a, tanya)}{src}</div>\n'
            f'<h2 id="standar-terkait">Standar Terkait</h2><div class="pchips">{chips}</div>\n<h2>Tanya Jawab</h2>{faq}\n<h2>Baca Juga</h2><div class="reads">{reads}</div>\n'
            f'<aside class="cta-box dark"><div><b>Butuh Pendampingan?</b><span>Tim akuntan bersertifikat CA dan CPA, terbiasa dengan prosedur auditor Big 4.</span></div>'
            f'<a class="btn arrow" href="{wa(a["wa"])}" rel="noopener" target="_blank">Tanya Ananta, CPA</a></aside>\n</div></article>\n')
    i = rest.find('<main'); j = rest.find('</main>')
    s = head + '</head>' + rest[:i] + main + rest[j:]
    return tbl_hp(s.replace(EQ('PSAK 115 Lima Langkah Pengakuan Pendapatan dengan Contoh Kontraktor'), EQ(t)))


def us_all():
    root = os.path.join(OUT, 'updatesak')
    tpl = rd(os.path.join(root, 'artikel', US_TPL, 'index.html'))
    for a in US_A:
        s = us_page(a, tpl)
        assert s.count('<h1') == 1 and 'Kontraktor sering mengakui' not in s, a['slug']
        wr(os.path.join(root, 'artikel', a['slug'], 'index.html'), s)
        if not DRY:
            poster.og('us', a['topik'], a['kota'], a['title'], os.path.join(root, 'img', 'share', f'art-{a["slug"]}-og.jpg'))
    # eksplor
    p = os.path.join(root, 'eksplor', 'index.html'); s = re.sub(r'<!--us-dae15-->.*?<!--/us-dae15-->', '', rd(p), flags=re.S)
    grp = ''
    for cat in dict.fromkeys(a['category'] for a in US_A):
        grp += f'<h3 class="gh">{E(cat)}</h3><div class="reads">' + ''.join(
            f'<a href="/artikel/{a["slug"]}/"><b>{E(a["title"])}</b><small>{E(a["description"][:110].rsplit(" ", 1)[0])}…</small></a>' for a in US_A if a['category'] == cat) + '</div>'
    m = re.search(r'\s*</div></section><section class="alt" id="tanya">', s)   # akhir section Artikel dan Panduan
    assert m; k = m.start()
    wr(p, s[:k] + '<!--us-dae15-->' + grp + '<!--/us-dae15-->' + s[k:])
    # sitemap + llms
    p = os.path.join(root, 'sitemap.xml'); sm = re.sub(r'<!--usdae15-->.*?<!--/usdae15-->\n?', '', rd(p), flags=re.S)
    blk = '<!--usdae15-->' + ''.join(f'<url><loc>{USD}/artikel/{a["slug"]}/</loc><lastmod>{DATE}</lastmod></url>\n' for a in US_A) + '<!--/usdae15-->\n'
    wr(p, sm.replace('</urlset>', blk + '</urlset>'))
    p = os.path.join(root, 'llms.txt'); L = rd(p)
    add = ''.join(f'- [{a["title"]}]({USD}/artikel/{a["slug"]}/): {a["description"]}\n' for a in US_A if f'/artikel/{a["slug"]}/' not in L)
    if add:
        k = L.find('- [Contoh CALK Lengkap Format Auditor Big 4'); wr(p, L[:k] + add + L[k:] if k >= 0 else L.rstrip('\n') + '\n' + add)
    # baris artikel terkait di halaman PSAK
    per = {}
    for a in US_A:
        for nn in a['psak']: per.setdefault(nn, []).append(a)
    for nn, items in sorted(per.items()):
        p = os.path.join(root, 'psak', nn, 'index.html'); s = re.sub(r'<!--us-dae15l-->.*?<!--/us-dae15l-->', '', rd(p), flags=re.S)
        blk = '<!--us-dae15l--><p class="kw3">Artikel terkait: ' + ' · '.join(f'<a href="/artikel/{x["slug"]}/">{E(x["title"])}</a>' for x in items) + '</p><!--/us-dae15l-->'
        k = s.find('<!--/us-ind-->')
        if k < 0: print('tanpa us-ind', nn); continue
        k += len('<!--/us-ind-->'); wr(p, s[:k] + blk + s[k:])


if __name__ == '__main__':
    ca_all(); us_all()
    print(('DRY ' if DRY else '') + 'berubah:', len(written)); [print('  ', w) for w in written]
