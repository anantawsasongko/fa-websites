#!/usr/bin/env python3
"""Rapikan teks dan tabel di FA, CariAkuntan, UpdateSAK (13 Nov 2026 malam).

Pemicu (Bos): paragraf tidak rapi marginnya, banyak yang tidak terlipat rapi di HP dan laptop.
Hanya merapikan, tidak mengubah isi: teks, link, id, title, description, JSON-LD tetap.

1. <style id="twr-css"> sebelum </head> di semua halaman out/{faindonesia,cariakuntan,updatesak}:
   kata panjang dilipat (overflow-wrap), judul seimbang, paragraf tanpa baris yatim,
   daftar link "Pencarian Populer" (.citylist) jadi grid kolom rata kiri,
   bahasa Inggris di HP pakai pemenggalan kata otomatis.
2. Tabel teks 2-3 kolom (class twr-s): di HP (<=600px) tiap baris jadi kartu bertumpuk,
   sel pertama tebal, sel lain diberi label kolom (data-l dari header). Desktop tidak berubah.
   Tabel 4+ kolom (class twr-w): di HP bisa digeser ke samping, tidak keluar layar.
   Tabel berisi input/select (kalkulator, apps) tidak disentuh.
Idempoten, aman diulang. Pakai: python3 teks_rapi_20261113.py [--dry]
"""
import re, sys, glob, html, os

DRY = '--dry' in sys.argv
SITES = ['out/faindonesia', 'out/cariakuntan', 'out/updatesak']

CSS = ('<style id="twr-css">'
 'p,li,dd,dt,td,th,blockquote,figcaption,summary,h1,h2,h3,h4{overflow-wrap:break-word}'
 'h1,h2,h3,h4{text-wrap:balance}'
 'p,li,dd,blockquote,figcaption,.lede{text-wrap:pretty!important}'
 # lebar paragraf mengikuti lebar kolom (sama dengan bagan, tabel, kartu di atas/bawahnya)
 'main p,main ul,main ol,main li,main dl,main blockquote,main figcaption,section p,section ul:not(nav ul),section ol,section li,section blockquote,article p,.lede,p.sub,p.t,p.lead{max-width:none!important}'
 '.citylist{display:grid!important;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px 28px!important;align-items:start}'
 '.citylist a{line-height:1.35}'
 '@media(max-width:600px){'
 '.citylist{grid-template-columns:1fr 1fr;gap:10px 16px!important;font-size:14px}'
 'html[lang|=en] p,html[lang|=en] li{-webkit-hyphens:auto;hyphens:auto}'
 'table.twr-s,table.twr-s>tbody,table.twr-s>thead,table.twr-s tr,table.twr-s td,table.twr-s th{display:block;width:auto!important;min-width:0!important;max-width:none!important;text-align:left!important}'
 'table.twr-s{border-collapse:collapse}'
 'table.twr-s>thead,table.twr-s tr.twr-h{display:none!important}'
 'table.twr-s tr{padding:12px 2px;border-bottom:1px solid rgba(128,128,128,.28)}'
 'table.twr-s tr:last-child{border-bottom:0}'
 'table.twr-s td,table.twr-s th{border:0!important;padding:2px 0!important;height:auto!important}'
 'table.twr-s td:first-child,table.twr-s th:first-child{font-weight:600}'
 'table.twr-s [data-l]::before{content:attr(data-l);display:block;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.6;margin:8px 0 2px}'
 'table.twr-w{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%}'
 '}</style>')

RE_STYLE = re.compile(r'<style id="twr-css">.*?</style>', re.S)
RE_TABLE = re.compile(r'<table\b[^>]*>.*?</table>', re.S)
RE_TR = re.compile(r'<tr\b[^>]*>.*?</tr>', re.S)
RE_CELL = re.compile(r'<(t[dh])\b([^>]*)>(.*?)</\1>', re.S)

def txt(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def addclass(tag, cls):
    if re.search(r'\bclass="[^"]*\b%s\b' % cls, tag):
        return tag
    if 'class="' in tag:
        return re.sub(r'class="', 'class="%s ' % cls, tag, count=1)
    return tag[:-1] + ' class="%s">' % cls

def fix_table(t):
    if t.count('<table') > 1 or re.search(r'<(input|select|textarea|button)\b|span=', t):
        return t
    rows = RE_TR.findall(t)
    if not rows:
        return t
    cells = [RE_CELL.findall(r) for r in rows]
    ncol = max(len(c) for c in cells)
    open_tag = re.match(r'<table\b[^>]*>', t).group(0)
    if ncol >= 4:
        return addclass(open_tag, 'twr-w') + t[len(open_tag):]
    if ncol < 2 or any(len(c) not in (0, ncol) for c in cells):
        return t
    body = [c for c in cells if c and not all(x[0] == 'th' for x in c)]
    vals = [txt(x[2]) for c in body for x in c]
    if not vals:
        return t
    num = sum(1 for v in vals if re.fullmatch(r'[-+()Rp$.,%\d\s]*\d[-+()Rp$.,%\d\s]*', v))
    if num > len(vals) / 2:
        return t
    # header
    head = None
    hdr_row = None
    m = re.search(r'<thead\b.*?</thead>', t, re.S)
    if m:
        hr = RE_TR.search(m.group(0))
        if hr:
            head = [txt(x[2]) for x in RE_CELL.findall(hr.group(0))]
    elif cells[0] and all(x[0] == 'th' for x in cells[0]):
        head = [txt(x[2]) for x in cells[0]]
        hdr_row = rows[0]
    out = addclass(open_tag, 'twr-s') + t[len(open_tag):]
    if hdr_row:
        new = re.sub(r'^<tr\b[^>]*>', lambda mm: addclass(mm.group(0), 'twr-h'), hdr_row)
        out = out.replace(hdr_row, new, 1)
    if head and len(head) == ncol:
        def row_fix(mr):
            r = mr.group(0)
            if r == hdr_row or 'twr-h' in r[:60]:
                return r
            i = [0]
            def cell_fix(mc):
                k = i[0]; i[0] += 1
                tag, attrs, inner = mc.group(1), mc.group(2), mc.group(3)
                if k == 0 or 'data-l=' in attrs or not head[k]:
                    return mc.group(0)
                return '<%s%s data-l="%s">%s</%s>' % (tag, attrs, html.escape(head[k], quote=True), inner, tag)
            return RE_CELL.sub(cell_fix, r)
        body_start = out.find('</thead>')
        if body_start < 0:
            out = RE_TR.sub(row_fix, out)
        else:
            out = out[:body_start] + RE_TR.sub(row_fix, out[body_start:])
    return out

def main():
    changed = 0; stacked = 0; wide = 0
    for site in SITES:
        for f in glob.glob(site + '/**/*.html', recursive=True):
            s = open(f, encoding='utf-8').read()
            if '</head>' not in s:
                continue
            o = RE_STYLE.sub('', s)
            o = o.replace('</head>', CSS + '</head>', 1)
            if '<table' in o:
                o = RE_TABLE.sub(lambda m: fix_table(m.group(0)), o)
            if o != s:
                changed += 1
                stacked += len(re.findall(r'<table[^>]*twr-s', o)) - len(re.findall(r'<table[^>]*twr-s', s))
                wide += len(re.findall(r'<table[^>]*twr-w', o)) - len(re.findall(r'<table[^>]*twr-w', s))
                if not DRY:
                    open(f, 'w', encoding='utf-8').write(o)
    print('file berubah', changed, 'tabel kartu baru', stacked, 'tabel geser baru', wide, '(dry)' if DRY else '')

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
