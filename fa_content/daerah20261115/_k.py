# -*- coding: utf-8 -*-
"""Perangkat bersama konten artikel daerah 15 Nov 2026 (FA, CA, US, Kompasiana).
Semua angka ilustrasi dihitung di sini/di modul konten, bukan diketik manual, supaya tabel dan narasi selalu cocok."""
import re, html

ARTS = []          # semua artikel terdaftar
TODAY = '2026-11-15'
TODAY_ID = '15 November 2026'


def n(x, d=0):
    """Angka format Indonesia: 1.234.567,8"""
    s = f'{x:,.{d}f}'
    return s.replace(',', '#').replace('.', ',').replace('#', '.')


def rp(x, d=0):
    return ('-Rp' if x < 0 else 'Rp') + n(abs(x), d)


def _trim(x, maxd=3):
    s = f'{x:.{maxd}f}'.rstrip('0').rstrip('.')
    if '.' in s:
        a, b = s.split('.'); return n(int(a)) + ',' + b
    return n(int(s))


def jt(x, d=None):
    """x dalam rupiah -> 'Rp12,5 juta' / 'Rp1,152 miliar'. d = jumlah desimal tetap (opsional)."""
    sg = '-' if x < 0 else ''; x = abs(x)
    for lim, nm in ((1e12, 'triliun'), (1e9, 'miliar'), (1e6, 'juta')):
        if x >= lim:
            return f"{sg}Rp{n(x / lim, d) if d is not None else _trim(x / lim)} {nm}"
    return sg + 'Rp' + n(x)


def pct(x, d=1):
    return n(x * 100, d) + '%'


def tbl(head, rows, total=None):
    """Tabel artikel. head: list judul kolom; rows: list of list; total: baris jumlah (tebal)."""
    h = '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in head) + '</tr></thead>'
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    if total:
        b += '<tr>' + ''.join(f'<td><b>{c}</b></td>' if c != '' else '<td></td>' for c in total) + '</tr>'
    return f'<div class="tblwrap"><table class="tbl">{h}<tbody>{b}</tbody></table></div>'


def words(h):
    return len(re.sub(r'<[^>]+>', ' ', h).split())


ERR = []


def A(**a):
    """Daftarkan artikel + validasi dasar (kesalahan dikumpulkan di ERR; panggil check() sebelum build)."""
    e = lambda *x: ERR.append((a.get('slug'),) + x)
    req = ['site', 'topik', 'kota', 'kota_slug', 'slug', 'seo_title', 'title', 'description', 'keyword', 'category',
           'body_html', 'faq', 'sources', 'wa']
    for k in req:
        if k not in a: e('kurang', k)
    if not (a['site'] in ('fa', 'ca', 'us', 'ks') and a['topik'] in ('abc', 'pe', 'cfo')): e('site/topik')
    if not re.fullmatch(r'[a-z0-9-]+', a['slug']): e('slug')
    if len(a['seo_title']) > 65: e('seo_title', len(a['seo_title']))
    if not 110 <= len(a['description']) <= 158: e('description', len(a['description']))
    blob = ' '.join(str(v) for v in a.values())
    if '\u2014' in blob or '\u2013' in blob: e('em/en dash')
    for bad in ('ditangani langsung', 'Ditangani Langsung', 'dijawab Ananta', 'bicara langsung dengan Ananta', 'pasti cair',
                'tolok ukur', 'imbalan jasa', 'model keterlibatan', 'di era digital', 'Rp-', 'nan', 'None'):
        if re.search(r'(?<![A-Za-z])' + re.escape(bad) + r'(?![A-Za-z])', blob): e('frasa terlarang', bad)
    if a['body_html'].count('<h2>') < 4: e('h2 kurang')
    if '<h1' in a['body_html']: e('h1')
    a.setdefault('minutes', max(4, round(words(a['body_html']) / 190)))
    a.setdefault('related', [])
    if not 3 <= len(a['faq']) <= 5: e('faq')
    if (a['site'], a['slug']) in [(x['site'], x['slug']) for x in ARTS]: e('slug dobel')
    ARTS.append(a)
    return a


def check():
    assert not ERR, ERR
