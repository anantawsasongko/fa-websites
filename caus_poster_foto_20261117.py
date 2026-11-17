# -*- coding: utf-8 -*-
"""Poster artikel dengan foto Ananta di CariAkuntan, UpdateSAK, dan poster Kompasiana (17 Nov 2026).

Bos: "Di artikel pribadi, CA, dan US masih belum menyebar foto-foto saya dengan gaya poster gradasi dan noise noir.
Pakenya foto yang itu itu saja" lalu "Malah di CA dan US sama sekali gak ada foto saya".

Yang dikerjakan (BEKERJA LANGSUNG DI out/, lihat PERINGATAN BUILD di README-DEPLOY; idempoten, --dry):
1. og:image semua artikel CA (out/cariakuntan/img/og-art/<slug>.jpg) dan US (out/updatesak/img/share/art-<slug>-og.jpg
   + -story.jpg) dibuat ulang: latar noir bergradasi warna brand + grain, foto Ananta (7 foto profesional, dipilih
   bergiliran per judul lewat shared/ananta_foto.py). URL gambar tetap, jadi meta tag tidak berubah.
2. 30 artikel daerah 15 Nov (FA, CA, US) dan 10 poster Kompasiana (out/faindonesia/img/kompasiana/) dibuat ulang
   dengan poster_daerah.py yang sekarang memakai foto bergiliran (sebelumnya selalu foto jas navy).
3. Artikel CA dan US yang belum punya gambar pembuka mendapat <figure class="dae-fig"> (poster artikel) di bawah
   judul, penanda <!--fotoart-->. Artikel daerah sudah punya, tidak disentuh.
Desain sama dengan sumber: shared/brand_poster.py (cache og CA v8, UpdateSAK .v8) sehingga build ulang konsisten.
Jalankan PALING AKHIR untuk CA/US, sesudah caus_hero_fa_20261117.py (gambar ditaruh tepat setelah hero gelap rxh).
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
DRY = '--dry' in sys.argv
NOIMG = '--noimg' in sys.argv          # hanya HTML (cek cepat)
sys.path.insert(0, os.path.join(HERE, 'shared'))
sys.path.insert(0, os.path.join(HERE, 'fa_content', 'daerah20261115'))
import brand_poster as bp
import poster_daerah as pd
import _k, fa_abc, fa_pe, fa_cfo, ca, us, ks  # mengisi _k.ARTS
_k.check()

CSS = ('<style id="dae-fig-css">.dae-fig{margin:14px 0 22px;padding:0}\n'
       '.dae-fig img{display:block;width:100%;height:auto;border:1px solid rgba(127,127,127,.28);border-radius:10px}\n</style>')
written, imgs = [], []


def rd(p): return open(p, encoding='utf-8').read()


def wr(p, s):
    if rd(p) == s: return
    written.append(os.path.relpath(p, OUT))
    if not DRY: open(p, 'w', encoding='utf-8').write(s)


def img(fn, *a):
    imgs.append(os.path.relpath(a[-1], OUT))
    if not DRY and not NOIMG: fn(*a)


def txt(s): return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def fig(src, title):
    return (f'<!--fotoart--><figure class="dae-fig"><img alt="{html.escape(title, quote=True)}" decoding="async" '
            f'height="630" src="{src}" width="1200"/></figure><!--/fotoart-->')


def add_css(s):
    if 'id="dae-fig-css"' in s: return s
    return s.replace('</head>', CSS + '</head>', 1)


def articles(site):
    d = os.path.join(OUT, site, 'artikel')
    for slug in sorted(os.listdir(d)):
        p = os.path.join(d, slug, 'index.html')
        if not os.path.exists(p): continue
        s = rd(p)
        if not re.search(r'"@type"\s*:\s*"(Article|NewsArticle|BlogPosting)"', s): continue
        yield slug, p, s


def assign():
    """Bagi foto bergiliran per kelompok (CA, US, daerah per situs, Kompasiana) lalu simpan ke shared/ananta/assign.json."""
    import json, ananta_foto as af
    groups = []
    for site in ('cariakuntan', 'updatesak'):
        groups.append([txt(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1)) for _, _, s in articles(site)])
    for st in ('fa', 'ca', 'us', 'ks'):
        groups.append([a['title'] for a in _k.ARTS if a['site'] == st])
    m = {}
    for g in groups:
        g = [t for t in g if t not in m]
        for i, t in enumerate(g): m[t] = af.NAMES[i % len(af.NAMES)]
    # daerah CA/US juga muncul di kelompok situs; kelompok daerah per situs yang menentukan (lebih kecil, harus merata)
    for st in ('fa', 'ca', 'us', 'ks'):
        g = [a['title'] for a in _k.ARTS if a['site'] == st]
        for i, t in enumerate(g): m[t] = af.NAMES[(i + 2 * 'fa ca us ks'.split().index(st)) % len(af.NAMES)]
    f = os.path.join(af.DIR, 'assign.json')
    if not DRY: json.dump(m, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    af._ASSIGN = m


def after_hero(s2):
    """Posisi gambar pembuka: tepat setelah hero gelap <header class="rxh"> (caus_hero_fa_20261117.py), kalau ada."""
    i = s2.find('<header class="rxh"')
    if i < 0: return None
    j = s2.find('</header>', i)
    return j + len('</header>') if j > 0 else None


def main():
    assign()
    dae = {a['slug']: a for a in _k.ARTS}
    # ---- CariAkuntan
    root = os.path.join(OUT, 'cariakuntan')
    for slug, p, s in articles('cariakuntan'):
        title = txt(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
        dst = os.path.join(root, 'img', 'og-art', slug + '.jpg')
        if slug in dae:
            a = dae[slug]; img(pd.og, 'ca', a['topik'], a['kota'], a['title'], dst); continue
        k = re.search(r'class="eyebrow"><a[^>]*>Eksplor · ([^<]+)<', s) or re.search(r'<p class="label"[^>]*>([^<]{2,40})</p>', s)
        kicker = html.unescape(k.group(1)).strip() if k else ''
        img(bp.og, 'ca', kicker, title, None, dst)
        s2 = re.sub(r' ?<!--fotoart-->.*?<!--/fotoart-->', '', s, flags=re.S)
        e = after_hero(s2)
        if e is None:
            m = re.search(r'<p class="meta-line">.*?</p>', s2, re.S); assert m, slug; e = m.end()
        s2 = s2[:e] + ' ' + fig(f'/img/og-art/{slug}.jpg', title) + s2[e:]
        wr(p, add_css(s2))
    # ---- UpdateSAK
    root = os.path.join(OUT, 'updatesak')
    for slug, p, s in articles('updatesak'):
        title = txt(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
        d = os.path.join(root, 'img', 'share')
        if slug in dae:
            a = dae[slug]; img(pd.og, 'us', a['topik'], a['kota'], a['title'], os.path.join(d, f'art-{slug}-og.jpg')); continue
        k = re.search(r'<p class="label"[^>]*>([^<]{2,40})</p>', s)
        kicker = html.unescape(k.group(1)).strip() if k else ''
        img(bp.og, 'us', kicker, title, 'updatesak.com', os.path.join(d, f'art-{slug}-og.jpg'))
        if os.path.exists(os.path.join(d, f'art-{slug}-story.jpg')):
            img(bp.story, 'us', kicker, title, 'updatesak.com', os.path.join(d, f'art-{slug}-story.jpg'))
        s2 = re.sub(r' ?<!--fotoart-->.*?<!--/fotoart-->', '', s, flags=re.S)
        e = after_hero(s2)
        if e is None:
            m = re.search(r'<div class="share">.*?</div>', s2, re.S) or re.search(r'<p class="upd">.*?</p>', s2, re.S)
            assert m, slug; e = m.end()
        s2 = s2[:e] + ' ' + fig(f'/img/share/art-{slug}-og.jpg', title) + s2[e:]
        wr(p, add_css(s2))
    # ---- FA daerah + Kompasiana (poster foto bergiliran)
    fa = os.path.join(OUT, 'faindonesia', 'img')
    for a in _k.ARTS:
        if a['site'] == 'fa':
            img(pd.og, 'fa', a['topik'], a['kota'], a['title'], os.path.join(fa, 'og-page', f'artikel-{a["slug"]}.jpg'))
        elif a['site'] == 'ks':
            img(pd.og, 'ks', a['topik'], a['kota'], a['title'], os.path.join(fa, 'kompasiana', a['slug'] + '.jpg'))
    print(('DRY ' if DRY else '') + f'HTML berubah: {len(written)}, gambar: {len(imgs)}')


if __name__ == '__main__':
    main()
