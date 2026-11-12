#!/usr/bin/env python3
"""Kotak kontak KJA Farhani + KAP DHN (fa-lk2) jadi terlipat (12 Nov 2026 sore).
BEKERJA LANGSUNG DI out/faindonesia, idempoten, jalankan PALING AKHIR (setelah dhn_dua_kartu_20261112.py).

Pemicu (Bos): "Bagian ini lipat aja lah". Kotak "Kontak KJA Farhani dan KAP DHN & Rekan" di bawah
tombol hero memakan satu layar penuh. Sekarang <details class="lk2"> tertutup: yang tampil hanya
judulnya, isi (intake keperluan + omzet, dua tombol WhatsApp) muncul saat diklik. Kelas lk2 dan
penanda <!--fa-lk2--> dipertahankan, jadi CSS rapi12 dan /js/fa-intake.js tetap jalan.
Kotak tengah artikel (fa-lk2a) tidak disentuh.
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv
M1, M1E = '<!--fa-lk2-->', '<!--/fa-lk2-->'

CSS = ('<style id="lk2d-css">'
       'details.lk2>summary{list-style:none;cursor:pointer;position:relative;padding-right:34px;line-height:1.4}'
       'details.lk2>summary::-webkit-details-marker{display:none}'
       'details.lk2>summary:after{content:"+";position:absolute;right:2px;top:50%;margin-top:-15px;font-size:24px;'
       'line-height:30px;font-weight:300;transition:transform .25s}'
       'details.lk2[open]>summary:after{transform:rotate(45deg)}'
       'details.lk2>summary:focus-visible{outline:2px solid rgba(233,185,73,.8);outline-offset:4px;border-radius:4px}'
       '</style>')

PAT = re.compile(r'^<div class="lk2" style="([^"]*)">(<b style="font-size:17px">.*?</b>)(.*)</div>$', re.S)


def fold(block):
    m = PAT.match(block)
    if not m:
        return None
    style, title, rest = m.groups()
    return f'<details class="lk2" style="{style}"><summary>{title}</summary>{rest}</details>'


def main():
    n = skip = bad = 0
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            t = open(p, encoding='utf-8').read()
            if M1 not in t:
                continue
            o = t
            i = t.index(M1) + len(M1)
            j = t.index(M1E, i)
            block = t[i:j]
            if block.startswith('<div class="lk2"'):
                new = fold(block)
                if new is None:
                    bad += 1
                    print('TIDAK COCOK:', p)
                    continue
                t = t[:i] + new + t[j:]
            if 'id="lk2d-css"' not in t and '<details class="lk2"' in t:
                t = t.replace('</head>', CSS + '</head>', 1)
            if t != o:
                n += 1
                if not DRY:
                    open(p, 'w', encoding='utf-8').write(t)
            else:
                skip += 1
    print(f'diubah {n}, sudah terlipat {skip}, tidak cocok {bad}' + (' (dry run)' if DRY else ''))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
