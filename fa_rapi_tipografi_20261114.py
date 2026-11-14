#!/usr/bin/env python3
"""FA: sapu tipografi semua halaman berpola artikel/layanan (.wrap.art), 14 Nov 2026.

Pemicu (Bos): "spacing ada yang terlalu mepet, lebar paragrafnya gak sesuai
tabel, sesuaikan keindahan paduan font".

Temuan audit 232 template (satu per keluarga): paragraf 1 baris sampai ±130
karakter di 207 template; paragraf tanpa jarak (margin 0) di wilayah,
profil, daftar kecamatan; tabel grid kotak-kotak; judul campur Times/EB
Garamond/Georgia (diselesaikan di fa_daerah_v2_20261114.py, alias ke
Newsreader).

<style id="fa-tipo"> sebelum </head> di semua HTML yang punya
class="wrap art":
- satu kolom baca 760 px untuk SEMUA isi (paragraf, tabel, daftar,
  akordeon, kartu), jadi lebar paragraf = lebar tabel; H1 boleh lebih lebar.
- ritme vertikal: paragraf .95em, H2 2.4em di atas, H3 1.6em, tabel dan
  blok 1.3em/1.8em; paragraf ber-style inline tidak disentuh.
- tabel desktop: garis rambut horizontal, kepala kolom kecil kapital.
- paduan font: judul Newsreader, isi Source Sans 3, angka tabel tabular.
Hanya CSS; teks, H1, URL, JSON-LD tidak berubah. Idempoten, --dry.
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv
W = '760px'
A = 'main .wrap.art'
CSS = (
    # kolom baca tunggal
    A + '>*:not(h1){max-width:' + W + '!important;box-sizing:border-box}'
    + A + '>h1{max-width:17em}'
    + A + ' .tblwrap,' + A + ' table{max-width:100%}'
    # ritme
    + A + ' p:not([style]){margin-top:0;margin-bottom:.95em!important}'
    + A + ' details>p:not([style]){margin-bottom:.55em!important}'
    + A + ' p:not([style]){line-height:1.7}'
    + A + '>h2,' + A + ' section>h2{margin-top:1.7em!important;margin-bottom:.55em!important;'
    'line-height:1.2!important;font-weight:400!important;letter-spacing:-.01em}'
    + A + '>h3,' + A + ' section>h3{margin-top:1.6em!important;margin-bottom:.45em!important;line-height:1.3!important}'
    + A + '>.tblwrap,' + A + '>table,' + A + ' .dfb>.tblwrap,' + A + ' section>.tblwrap{margin:1.3em 0 1.8em!important}'
    + A + '>ul,' + A + '>ol{margin:.2em 0 1.2em!important;padding-left:1.25em}'
    + A + '>ul>li,' + A + '>ol>li{margin:.35em 0;line-height:1.65}'
    + A + '>.faq-acc,' + A + '>.cbtns{margin-top:1.4em!important}'
    + A + '>p+details,' + A + ' .dfb>p+details,' + A + ' section>p+details{margin-top:.6em!important}'
    # tabel: garis rambut (desktop)
    + '@media(min-width:641px){'
    + A + ' table{border-collapse:collapse!important;border-spacing:0!important;border:0!important;width:100%}'
    + A + ' table th,' + A + ' table td{border:0!important;border-bottom:1px solid rgba(255,255,255,.1)!important;'
    'background:transparent!important;padding:12px 16px 12px 0!important;vertical-align:top;line-height:1.55}'
    + A + ' table thead th{font-family:var(--body,"Source Sans 3",sans-serif)!important;font-size:12px!important;'
    'font-weight:600!important;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.55)!important;'
    'border-bottom:1px solid rgba(255,255,255,.28)!important;padding-bottom:10px!important}'
    + A + ' table tbody td:first-child{color:#fff;font-weight:500}'
    + A + ' table tbody tr:last-child td{border-bottom-color:rgba(255,255,255,.18)!important}'
    + A + ' .tblwrap{border:0!important;background:transparent!important;border-radius:0!important;box-shadow:none!important}'
    + '}'
    + A + ' td,' + A + ' .num{font-variant-numeric:tabular-nums}'
    # tautan dan penekanan isi
    + A + ' p a:not(.btn),' + A + ' li a:not(.btn),' + A + ' td a{text-underline-offset:.18em;text-decoration-thickness:1px}'
    + A + ' p b,' + A + ' p strong,' + A + ' li b{font-weight:600}'
    + '@media(max-width:640px){' + A + '>h2,' + A + ' section>h2{margin-top:1.5em!important}}'
)
BLOCK = '<!--fa-tipo--><style id="fa-tipo">%s</style><!--/fa-tipo-->' % CSS
RX = re.compile(r'<!--fa-tipo-->.*?<!--/fa-tipo-->', re.S)


def main():
    n = 0
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            p = os.path.join(root, fn)
            h = open(p, encoding='utf-8', errors='surrogateescape').read()
            if 'class="wrap art"' not in h or '</head>' not in h:
                continue
            o = h
            if RX.search(h):
                h = RX.sub(lambda _: BLOCK, h, count=1)
            else:
                i = h.find('</head>')
                h = h[:i] + BLOCK + h[i:]
            if h != o:
                n += 1
                if not DRY:
                    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(h)
    print(('DRY ' if DRY else '') + 'berubah: %d file' % n)


if __name__ == '__main__':
    main()
