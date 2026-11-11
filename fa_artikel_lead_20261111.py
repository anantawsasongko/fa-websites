#!/usr/bin/env python3
"""Artikel dari kebutuhan calon klien FA (11 Nov 2026, permintaan Bos): 6 klaster x 5 (RS, audit, LK, kredit, forensik, valuasi).
Turunan fa_artikel_wtp_20261108.py. Konten: fa_content/lead20261111/*.py -> fa_content/articles/*.json (jalankan merge_extra.py). BEKERJA DI out/faindonesia, idempoten.
Sumber konten: fa_content/articles/<slug>.json (slug, seo_title, title, description, keyword, category, minutes,
cta, wa, sources, related, body_html, faq). Bagian panjang ditulis sebagai <div class="pf-fold"> dan otomatis
diberi tombol "Baca Selengkapnya" (dilipat). Template: halaman live /artikel/jenis-opini-audit-dan-dampaknya-ke-bank/.
Sisipan: sitemap (penanda <!--lead11-->), llms.txt, kartu Eksplor (artikel/index.html), Baca Juga di artikel terkait,
blok link di /jasa-audit-laporan-keuangan/ (penanda fa-wtp). Jalankan lalu fa_seo_rapi_20261108.py --dry harus 0.
"""
import os, re, json, html, sys, copy
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'out', 'faindonesia')
SRC = os.path.join(HERE, 'fa_content', 'articles')
DOMAIN = 'https://faindonesia.co.id'
SLUGS = [
 "data-awal-konsultasi-keuangan-rumah-sakit",
 "memilih-konsultan-rumah-sakit-pertanyaan-pemilik",
 "menjual-rumah-sakit-dan-klinik-di-beberapa-pt",
 "pendampingan-keuangan-rsia-90-hari-pertama",
 "taksasi-bank-vs-penilaian-kjpp-rumah-sakit",
 "audit-laporan-keuangan-perusahaan-tambang-kontraktor-kalimantan",
 "audit-laporan-keuangan-pt-pma-persiapan",
 "audit-selesai-sebelum-akhir-tahun-target-realistis",
 "cara-membaca-surat-penawaran-audit-kap",
 "laporan-keuangan-audited-untuk-tender-migas-bumn",
 "keaslian-data-laporan-keuangan-untuk-bank",
 "laporan-keuangan-bank-dan-pajak-harus-sejalan",
 "laporan-keuangan-usaha-pariwisata-bali",
 "menyusun-laporan-keuangan-dari-rekening-koran",
 "pertanyaan-sebelum-menyusun-laporan-keuangan-pt",
 "kredit-konstruksi-developer-perumahan-dokumen",
 "laporan-keuangan-interim-triwulan-untuk-kredit",
 "penjualan-tunai-dan-money-changer-dibaca-bank",
 "perpanjangan-prk-sambil-mengajukan-ke-bank-lain",
 "rencana-kerja-3-bulan-sebelum-mengajukan-kredit",
 "ahli-akuntansi-di-penyidikan-dan-persidangan",
 "dokumen-menghitung-kerugian-penggelapan",
 "kerja-sama-kuasa-hukum-pembuktian-kerugian",
 "laporan-penghitungan-kerugian-proyek-akuntan-publik",
 "metode-menghitung-kerugian-keuangan",
 "menawarkan-usaha-kecil-ke-investor-langkah",
 "menentukan-harga-saham-usaha-keluarga-partner-baru",
 "studi-kelayakan-proyek-wisata-pemegang-saham",
 "valuasi-indikatif-vs-valuasi-lengkap",
 "valuasi-usaha-umkm-penjualan-marketplace"
]
TPL_SLUG = 'jenis-opini-audit-dan-dampaknya-ke-bank'
DATE_ISO = '2026-11-11T14:00:00+07:00'
DATE_ID = '11 November 2026'
WA = '6282245260121'
sys.path.insert(0, os.path.join(HERE, 'shared'))


def slugify(t):
    t = html.unescape(re.sub(r'<[^>]+>', '', t)).lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:70]


def title_of(slug):
    p = os.path.join(ROOT, 'artikel', slug, 'index.html')
    s = open(p, encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip()


def body(a):
    b = a['body_html']
    # id h2 + peta isi
    heads = []
    def h2(m):
        t = m.group(1); i = slugify(t); heads.append((i, t))
        return f'<h2 id="{i}">{t}</h2>'
    b = re.sub(r'<h2>(.*?)</h2>', h2, b)
    n = [0]
    def fold(m):
        n[0] += 1; i = f'pfw{n[0]}'
        return (f'<div class="pf-fold" id="{i}">{m.group(1)}</div><button aria-controls="{i}" aria-expanded="false" '
                f'class="pf-more" data-for="{i}" type="button">Baca Selengkapnya </button>')
    b = re.sub(r'<div class="pf-fold">(.*?)</div>(?=\s*(?:<h2|<p|<div class="tblwrap"|$))', fold, b, flags=re.S)
    b = b.replace('<div class="tblwrap"><table class="tbl">', '<div class="tblwrap"><table class="tbl">')
    nav = '<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>' + ''.join(
        f'<li><a href="#{i}">{t}</a></li>' for i, t in heads) + '</ol></nav>'
    k = b.find('<h2 ')
    return b[:k] + nav + b[k:]


def build(a, tpl, titles):
    s = tpl
    old_url = f'{DOMAIN}/artikel/{TPL_SLUG}/'
    url = f'{DOMAIN}/artikel/{a["slug"]}/'
    # --- head
    head, rest = s.split('</head>', 1)
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(a['seo_title'], quote=False), head, flags=re.S)
    def meta(attr, key, val, h):
        def rep(m):
            tg = m.group(0)
            if re.search(r'%s="%s"' % (attr, re.escape(key)), tg):
                return re.sub(r'content="[^"]*"', 'content="%s"' % html.escape(val, quote=True), tg, count=1)
            return tg
        return re.sub(r'<meta\b[^>]*>', rep, h)
    head = meta('name', 'description', a['description'], head)
    head = meta('property', 'og:title', a['title'], head)
    head = meta('property', 'og:description', a['description'], head)
    head = meta('property', 'article:published_time', DATE_ISO, head)
    head = head.replace(old_url, url)
    # poster
    import share_all
    kicker = 'Eksplor · ' + a['category']
    img = share_all._poster('fa', kicker, a['title'], 'artikel-' + a['slug'], ROOT)
    head = head.replace(f'/img/og-page/artikel-{TPL_SLUG}.jpg', img)
    # JSON-LD
    def ld(m):
        d = json.loads(m.group(1))
        for g in d.get('@graph', []):
            t = g.get('@type')
            if t == 'Article':
                g.update({'@id': url + '#article', 'headline': a['title'], 'description': a['description'], 'url': url,
                          'mainEntityOfPage': url, 'datePublished': DATE_ISO, 'dateModified': DATE_ISO,
                          'image': DOMAIN + img, 'keywords': a['keyword'], 'articleSection': a['category']})
            elif t == 'BreadcrumbList':
                last = g['itemListElement'][-1]; last['name'] = a['title']; last['item'] = url
            elif t == 'FAQPage':
                g['mainEntity'] = [{'@type': 'Question', 'name': html.unescape(q), 'acceptedAnswer': {'@type': 'Answer', 'text': html.unescape(x)}} for q, x in a['faq']]
            elif t in ('WebPage',):
                g['url'] = url; g['@id'] = url + '#page'; g['name'] = a['title']
        return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)
    head = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, head, flags=re.S)
    if '"FAQPage"' not in head:
        pass
    s = head + '</head>' + rest
    # sisa judul template (mis. data-tool share)
    old_t = 'Jenis Opini Audit dan Dampaknya ke Bank: WTP, WDP, TW, dan TMP'
    s = s.replace(html.escape(old_t, quote=True), html.escape(a['title'], quote=True)).replace(old_t, a['title'])
    # --- main
    i = s.find('<main'); j = s.find('</main>')
    m = s[i:j]
    m = re.sub(r'(<p class="eyebrow"><a href="/artikel/" style="text-decoration:none">)Eksplor · [^<]*(</a></p>)',
               lambda x: x.group(1) + 'Eksplor · ' + html.escape(a['category'], quote=False) + x.group(2), m, count=1)
    h1a = m.find('<h1'); h1b = m.find('</h1>', h1a)
    m = m[:h1a] + re.sub(r'>.*$', '>', m[h1a:m.find('>', h1a) + 1]) + html.escape(a['title'], quote=False) + m[h1b:]
    mb = m.find('<p class="meta">'); me = m.find('</p>', mb) + 4
    meta_p = re.sub(r' · [^·<]+ · \d+ menit baca</p>$', f' · {DATE_ID} · {a["minutes"]} menit baca</p>', m[mb:me])
    m = m[:mb] + meta_p + m[me:]
    # isi dari setelah meta (dan share bila ada) sampai Pertanyaan Umum
    start = m.find('</p>', m.find('<p class="meta">')) + 4
    sh = m.find('<div class="tshare-top">', start)
    if 0 <= sh - start < 50:
        start = m.find('</div></div>', sh) + 12
    q = m.find('<h2>Pertanyaan Umum</h2>')
    m = m[:start] + '\n' + body(a) + '\n' + m[q:]
    # FAQ
    fa = m.find('<div class="faq-acc">'); fb = m.find('<h2>Baca Juga</h2>', fa)
    faq = '<div class="faq-acc">' + ''.join(f'<details class="faq-i"><summary>{qq}</summary><p>{xx}</p></details>' for qq, xx in a['faq']) + '</div>\n'
    m = m[:fa] + faq + m[fb:]
    # Baca Juga + Sumber + tombol
    bj = m.find('<h2>Baca Juga</h2>'); cb = m.find('<div class="cbtns"', bj); ce = m.find('</div>', cb) + 6
    rel = '<h2>Baca Juga</h2><ul>' + ''.join(f'<li><a href="/artikel/{r}/">{html.escape(titles[r], quote=False)}</a></li>' for r in a['related']) + '</ul>\n'
    if a['sources']:
        rel += '<h2>Sumber</h2><ul>' + ''.join(f'<li><a href="{u}" rel="noopener nofollow" target="_blank">{html.escape(t, quote=False)}</a></li>' for u, t in a['sources']) + '</ul>\n'
    btn = (f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn solid" href="{a["cta"]["href"]}">{a["cta"]["label"]}</a>'
           f'<a class="btn line" href="https://wa.me/{WA}?text={quote(a["wa"])}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
           f'<a class="btn line" href="/artikel/">Eksplor Lainnya</a></div>')
    m = m[:bj] + rel + btn + m[ce:]
    s = s[:i] + m + s[j:]
    return s


def main():
    tpl = open(os.path.join(ROOT, 'artikel', TPL_SLUG, 'index.html'), encoding='utf-8').read()
    arts = [json.load(open(os.path.join(SRC, x + '.json'), encoding='utf-8')) for x in SLUGS]
    titles = {a['slug']: a['title'] for a in arts}
    for a in arts:
        for r in a['related']:
            if r not in titles: titles[r] = title_of(r)
    for a in arts:
        d = os.path.join(ROOT, 'artikel', a['slug']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(build(a, tpl, titles))
    # sitemap
    p = os.path.join(ROOT, 'sitemap.xml'); sm = open(p, encoding='utf-8').read()
    sm = re.sub(r'<!--lead11-->.*?<!--/lead11-->\n?', '', sm, flags=re.S)
    blk = '<!--lead11-->' + ''.join(f'<url><loc>{DOMAIN}/artikel/{a["slug"]}/</loc><lastmod>2026-11-11</lastmod><priority>0.8</priority></url>' for a in arts) + '<!--/lead11-->\n'
    open(p, 'w', encoding='utf-8').write(sm.replace('</urlset>', blk + '</urlset>'))
    # llms
    p = os.path.join(ROOT, 'llms.txt'); L = open(p, encoding='utf-8').read()
    for a in arts:
        line = f'- {a["title"]} → {DOMAIN}/artikel/{a["slug"]}/'
        if line not in L:
            k = L.find('- Titik Impas Rumah Sakit per DPJP')
            L = L[:k] + line + '\n' + L[k:] if k >= 0 else L + '\n' + line
    open(p, 'w', encoding='utf-8').write(L)
    # kartu Eksplor
    p = os.path.join(ROOT, 'artikel', 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--lead11-->.*?<!--/lead11-->', '', s, flags=re.S)
    cards = '<!--lead11-->' + ''.join(f'<a class="card2" href="/artikel/{a["slug"]}/"><b>{html.escape(a["title"], quote=False)}</b><span>{html.escape(a["description"], quote=False)}</span></a>' for a in arts) + '<!--/lead11-->'
    k = s.find('<a class="card2" href="/artikel/')
    s = s[:k] + cards + s[k:]
    open(p, 'w', encoding='utf-8').write(s)
    # Baca Juga balik: 2 artikel lama pertama di related tiap artikel baru dapat link ke artikel baru
    back = {}
    for a in arts:
        for r in [r for r in a['related'] if r not in SLUGS][:2]:
            back.setdefault(r, []).append(a['slug'])
    for old, news in back.items():
        p = os.path.join(ROOT, 'artikel', old, 'index.html')
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<!--lead11-->.*?<!--/lead11-->', '', s, flags=re.S)
        add = '<!--lead11-->' + ''.join(f'<li><a href="/artikel/{n}/">{html.escape(titles[n], quote=False)}</a></li>' for n in news[:3]) + '<!--/lead11-->'
        k = s.find('<h2>Baca Juga</h2><ul>')
        if k >= 0:
            k += len('<h2>Baca Juga</h2><ul>'); s = s[:k] + add + s[k:]
            open(p, 'w', encoding='utf-8').write(s)
    # blok bacaan di halaman pilar per klaster
    PIL = {'Rumah Sakit': ('konsultan-rumah-sakit', 'Bacaan untuk Pemilik dan Direksi Rumah Sakit'),
           'Audit & KAP': ('jasa-audit-laporan-keuangan', 'Bacaan Seputar Audit KAP'),
           'Laporan Keuangan': ('jasa-penyusunan-laporan-keuangan', 'Bacaan Seputar Penyusunan Laporan Keuangan'),
           'Kredit Bank': ('konsultan-kredit-bank', 'Bacaan Seputar Pengajuan Kredit'),
           'Akuntansi Forensik': ('akuntan-forensik', 'Bacaan Seputar Penghitungan Kerugian'),
           'Valuasi & Investor': ('jasa-valuasi-usaha', 'Bacaan Seputar Valuasi dan Investor')}
    for cat, (pg, h) in PIL.items():
        p = os.path.join(ROOT, pg, 'index.html'); s = open(p, encoding='utf-8').read()
        s = re.sub(r'<!--fa-lead11-->.*?<!--/fa-lead11-->', '', s, flags=re.S)
        items = [a for a in arts if a['category'] == cat]
        hid = slugify(h)
        blk = (f'<!--fa-lead11--><div class="wrap"><h2 id="{hid}">{h}</h2><ul>'
               + ''.join(f'<li><a href="/artikel/{a["slug"]}/">{html.escape(a["title"], quote=False)}</a></li>' for a in items) + '</ul></div><!--/fa-lead11-->')
        k = s.rfind('</main>')
        s = s[:k] + blk + s[k:]
        open(p, 'w', encoding='utf-8').write(s)
    print('ok', [a['slug'] for a in arts])


if __name__ == '__main__':
    main()
