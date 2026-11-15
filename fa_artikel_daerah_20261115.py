#!/usr/bin/env python3
"""15 Nov 2026 (Bos: "Tambahkan banyak artikel untuk SEO di daerah untuk FA, US, CA, Kompasiana ... poster gaya FA, foto gradasi,
pakai yang jas berdasi. Masing-masing 10 artikel: 3 Unit Cost ABC, 3 pendanaan RS dari PE dan VC global, 4 Fractional CFO").
Bagian FA: 10 artikel /artikel/<slug>/, satu kota per artikel. BEKERJA DI out/faindonesia, idempoten. Dry run: --dry.

Konten: fa_content/daerah20261115/{fa_abc,fa_pe,fa_cfo}.py (angka ilustrasi dihitung di modul, bukan diketik).
Halaman dibangun lewat build() fa_artikel_lead_20261111.py (template live), lalu:
- og:image diganti poster foto (fa_content/daerah20261115/poster_daerah.py) dan poster yang sama tampil di atas isi (figure.dae-fig);
- artikel rumah sakit mendapat blok tim RS (fa-rstim) sebelum Pertanyaan Umum;
- sisipan berpenanda <!--dae15-->: sitemap, llms.txt, kartu Eksplor, Baca Juga balik di artikel lama terkait;
- link balik berpenanda <!--dae15-l--> di halaman daerah kota yang bersangkutan dan di tiga pilar
  (/konsultan-unit-cost-rumah-sakit/, /pendanaan-rumah-sakit/, /cfo-paruh-waktu/). Halaman daerah juga menautkan artikel
  CariAkuntan dan UpdateSAK untuk kota itu (otoritas FA mengalir ke CA dan US).
Halaman lama hanya berubah di dalam blok berpenanda. Urutan bila build ulang: setelah fa_artikel_lead_20261111.py dan
fa_rs_sesak_20261113.py; sesudahnya fa_eksplor_rapi_20261113.py, fa_rendah_hati_20261112.py, fa_seo_rapi_20261108.py (--dry 0),
fa_rapi_tipografi_20261114.py (--dry 0). Kelas tabel untuk HP dipasang langsung di sini lewat fix_table() teks_rapi_20261113.py,
jadi teks_rapi tidak perlu dijalankan ulang untuk artikel ini.
"""
import os, re, sys, json, html, copy
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'out', 'faindonesia')
DOMAIN = 'https://faindonesia.co.id'
DRY = '--dry' in sys.argv
sys.path.insert(0, os.path.join(HERE, 'shared')); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'fa_content', 'daerah20261115'))
import importlib.util
spec = importlib.util.spec_from_file_location('lead', os.path.join(HERE, 'fa_artikel_lead_20261111.py'))
LEAD = importlib.util.module_from_spec(spec); spec.loader.exec_module(LEAD)
LEAD.DATE_ISO = '2026-11-15T16:00:00+07:00'; LEAD.DATE_ID = '15 November 2026'
import _k, fa_abc, fa_pe, fa_cfo, ca, us, ks
import poster_daerah as poster
_k.check()
ARTS = [a for a in _k.ARTS if a['site'] == 'fa']
OTHER = [a for a in _k.ARTS if a['site'] in ('ca', 'us')]
SITE = {'fa': DOMAIN, 'ca': 'https://cariakuntan.com', 'us': 'https://updatesak.com'}
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('teksrapi', os.path.join(HERE, 'teks_rapi_20261113.py'))
TR = _ilu.module_from_spec(_sp); _sp.loader.exec_module(TR)      # fix_table: kelas tabel untuk HP (kartu bertumpuk / geser)


def tbl_hp(s): return TR.RE_TABLE.sub(lambda m: TR.fix_table(m.group(0)), s)

E = lambda s: html.escape(s, quote=False)
written = []


def rd(p): return open(p, encoding='utf-8').read()


def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return
    written.append(os.path.relpath(p, ROOT))
    if DRY: return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)


CSS = ('<style id="dae-fig-css">.dae-fig{margin:4px 0 26px;padding:0}.dae-fig img{display:block;width:100%;height:auto;'
       'border:1px solid #2f2f2f;border-radius:2px}.dae15{margin:26px 0 0;font-size:.95em;line-height:1.6}</style>')


def rstim_block(kota):
    s = rd(os.path.join(ROOT, 'konsultan-rumah-sakit', 'purbalingga', 'index.html'))
    b = re.search(r'<!--fa-rstim-->.*?<!--/fa-rstim-->', s, re.S).group(0)
    css = re.search(r'<style id="fa-rstim-css">.*?</style>', s, re.S).group(0)
    msg = f'Halo Pak Ananta, saya membaca artikel FA Indonesia dan ingin diskusi untuk rumah sakit kami di {kota}.'
    return re.sub(r'(<a class="wa" href="https://wa\.me/\d+\?text=)[^"]*', lambda m: m.group(1) + quote(msg), b, count=1), css


def url_of(a):
    return ('' if a['site'] == 'fa' else SITE[a['site']]) + f'/artikel/{a["slug"]}/'


def targets(a):
    k = a['kota_slug']
    t = {'abc': [f'konsultan-unit-cost-rumah-sakit/{k}', f'konsultan-rumah-sakit/{k}'],
         'pe': [f'pendanaan-rumah-sakit/{k}', f'konsultan-rumah-sakit/{k}'],
         'cfo': [f'wilayah/{k}']}[a['topik']]
    return [x for x in t if os.path.exists(os.path.join(ROOT, x, 'index.html'))]


def put_block(s, blk):
    """Sisipkan blok link di tempat yang aman: sebelum H2 Pertanyaan Umum (bukan yang di dalam summary), atau sebelum
    tombol penutup, atau sebelum kotak penulis."""
    s = re.sub(r'<!--dae15-l-->.*?<!--/dae15-l-->\n?', '', s, flags=re.S)
    cands = [m.start() for m in re.finditer(r'<h2[^>]*>\s*Pertanyaan Umum\s*</h2>', s)]
    cands = [c for c in cands if not s[max(0, c - 9):c].endswith('<summary>')]
    if cands: k = cands[-1]
    else:
        k = s.rfind('<div class="cbtns"')
        if k < 0: k = s.rfind('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
        if k < 0: return None
    return s[:k] + blk + '\n' + s[k:]


def main():
    tpl = rd(os.path.join(ROOT, 'artikel', LEAD.TPL_SLUG, 'index.html'))
    titles = {a['slug']: a['title'] for a in ARTS}
    for a in ARTS:
        for r in a['related']:
            if r not in titles: titles[r] = LEAD.title_of(r)
    for a in ARTS:
        b = copy.deepcopy(a)
        b['sources'] = [(u, t) for t, u in a['sources']]
        b['faq'] = [(E(q), E(x)) for q, x in a['faq']]
        fig = (f'<figure class="dae-fig"><img alt="{html.escape(a["title"], quote=True)}" decoding="async" height="630" '
               f'src="/img/og-page/artikel-{a["slug"]}.jpg" width="1200"/></figure>')
        b['body_html'] = fig + a['body_html'].strip()
        if DRY:
            written.append(f'artikel/{a["slug"]}/index.html (dry)'); continue
        s = LEAD.build(b, tpl, titles)
        poster.og('fa', a['topik'], a['kota'], a['title'], os.path.join(ROOT, 'img', 'og-page', f'artikel-{a["slug"]}.jpg'))
        import glob, shutil                      # cache share_all ikut diganti supaya build penuh tidak mengembalikan poster lama
        for c in glob.glob(os.path.join(HERE, 'shared', 'og', 'page-fa', f'artikel-{a["slug"]}-*.jpg')):
            shutil.copy2(os.path.join(ROOT, 'img', 'og-page', f'artikel-{a["slug"]}.jpg'), c)
        head, rest = s.split('</head>', 1)
        if 'dae-fig-css' not in head: head += CSS
        if a['category'] == 'Rumah Sakit':
            blk, css = rstim_block(a['kota'])
            k = rest.find('<h2>Pertanyaan Umum</h2>')
            rest = rest[:k] + '<div style="margin:34px 0">' + blk + '</div>\n' + rest[k:]
            if 'fa-rstim-css' not in head: head += css
        s = tbl_hp(head + '</head>' + rest)
        assert s.count('<h1') == 1 and '—' not in s.split('<main')[1].split('</main>')[0]
        wr(os.path.join(ROOT, 'artikel', a['slug'], 'index.html'), s)
    # ---- sitemap
    p = os.path.join(ROOT, 'sitemap.xml'); sm = rd(p)
    sm = re.sub(r'<!--dae15-->.*?<!--/dae15-->\n?', '', sm, flags=re.S)
    blk = '<!--dae15-->' + ''.join(f'<url><loc>{DOMAIN}/artikel/{a["slug"]}/</loc><lastmod>2026-11-15</lastmod><priority>0.8</priority></url>' for a in ARTS) + '<!--/dae15-->\n'
    wr(p, sm.replace('</urlset>', blk + '</urlset>'))
    # ---- llms
    p = os.path.join(ROOT, 'llms.txt'); L = rd(p)
    for a in ARTS:
        line = f'- {a["title"]} → {DOMAIN}/artikel/{a["slug"]}/'
        if line not in L:
            k = L.find('- Titik Impas Rumah Sakit per DPJP')
            L = L[:k] + line + '\n' + L[k:] if k >= 0 else L + '\n' + line
    wr(p, L)
    # ---- kartu Eksplor (dipilah ulang oleh fa_eksplor_rapi_20261113.py)
    p = os.path.join(ROOT, 'artikel', 'index.html'); s = rd(p)
    have = set(re.findall(r'<a class="card2" href="/artikel/([^/"]+)/"', s))
    cards = ''.join(f'<a class="card2" href="/artikel/{a["slug"]}/"><b>{E(a["title"])}</b><span>{E(a["description"])}</span></a>'
                    for a in ARTS if a['slug'] not in have)
    if cards:
        k = s.find('<a class="card2" href="/artikel/')
        wr(p, s[:k] + cards + s[k:])
    # ---- Baca Juga balik di artikel lama (2 artikel lama pertama tiap artikel baru)
    new = {a['slug'] for a in ARTS}; back = {}
    for a in ARTS:
        for r in [r for r in a['related'] if r not in new][:2]:
            back.setdefault(r, []).append(a['slug'])
    for old, news in back.items():
        p = os.path.join(ROOT, 'artikel', old, 'index.html')
        if not os.path.exists(p): continue
        s = rd(p); s = re.sub(r'<!--dae15-->.*?<!--/dae15-->', '', s, flags=re.S)
        add = '<!--dae15-->' + ''.join(f'<li><a href="/artikel/{x}/">{E(titles[x])}</a></li>' for x in news[:3]) + '<!--/dae15-->'
        k = s.find('<h2>Baca Juga</h2><ul>')
        if k >= 0:
            k += len('<h2>Baca Juga</h2><ul>'); wr(p, s[:k] + add + s[k:])
    # ---- link balik di halaman daerah (FA + CA + US untuk kota yang sama)
    per = {}
    for a in ARTS + OTHER:
        for t in targets(a): per.setdefault(t, []).append(a)
    miss = []
    for t, items in sorted(per.items()):
        p = os.path.join(ROOT, t, 'index.html'); s = rd(p)
        kota = items[0]['kota']
        links = ' · '.join(f'<a href="{url_of(x)}">{E(x["title"])}</a>' for x in items)
        blk = f'<!--dae15-l--><p class="dae15"><b>Bacaan untuk {E(kota)}:</b> {links}</p><!--/dae15-l-->'
        s2 = put_block(s, blk)
        if s2 is None: miss.append(t); continue
        wr(p, s2)
    # ---- pilar
    PIL = {'abc': ('konsultan-unit-cost-rumah-sakit', 'Unit cost per kota'), 'pe': ('pendanaan-rumah-sakit', 'Pendanaan dari investor per kota'),
           'cfo': ('cfo-paruh-waktu', 'Fractional CFO per kota')}
    for tp, (pg, lab) in PIL.items():
        p = os.path.join(ROOT, pg, 'index.html'); s = rd(p)
        links = ' · '.join(f'<a href="/artikel/{x["slug"]}/">{E(x["kota"])}: {E(x["title"])}</a>' for x in ARTS if x['topik'] == tp)
        blk = f'<!--dae15-l--><p class="dae15"><b>{lab}:</b> {links}</p><!--/dae15-l-->'
        s2 = put_block(s, blk)
        if s2 is None: miss.append(pg); continue
        wr(p, s2)
    # ---- poster artikel Kompasiana (akun pribadi Bos): di-host di sini karena editor Kompasiana menerima gambar lewat URL,
    #      sedangkan upload file dari sesi otomatis tidak bisa. Tidak di-link dari halaman mana pun.
    if not DRY:
        for a in [x for x in _k.ARTS if x['site'] == 'ks']:
            poster.og('ks', a['topik'], a['kota'], a['title'], os.path.join(ROOT, 'img', 'kompasiana', a['slug'] + '.jpg'))
    print(('DRY ' if DRY else '') + 'berubah:', len(written)); [print('  ', w) for w in written]
    if miss: print('TIDAK ADA TITIK SISIP:', miss)


if __name__ == '__main__':
    main()
