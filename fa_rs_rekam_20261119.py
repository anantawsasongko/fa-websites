#!/usr/bin/env python3
"""Rekam jejak klien RS anonim (provinsi + jenis layanan) di halaman rumah sakit FA.

Cakupan: /konsultan-rumah-sakit/ dan /pendanaan-rumah-sakit/ (pilar + semua halaman daerah).
- Halaman yang sudah punya H2 Rekam Jejak: butir baru disisipkan ke daftar yang ada.
- Halaman lain: blok ringkas "Rekam Jejak Tim" tepat setelah blok Tim Konsultan Rumah Sakit.
Bekerja di out/faindonesia. Idempoten (penanda fa-rsrj). --dry untuk hitung saja.
Aturan isi: tanpa nama RS, tanpa kota, tanpa kata jual; klien yang belum TTD tidak disebut terpisah.
"""
import glob, re, sys

ROOT = 'out/faindonesia'
DRY = '--dry' in sys.argv
M = '<!--fa-rsrj-->'

RSIA = 'Pendampingan pembiayaan dan restrukturisasi RSIA swasta di Banten dan Jawa Barat.'
BUMN = 'Menyusun annual report perdana sebuah rumah sakit BUMN.'
DIR = 'Pengalaman memimpin rumah sakit swasta di Jawa Timur dan DI Yogyakarta sebagai direksi.'

ITEMS = [
    RSIA,
    'Mendampingi akuisisi tiga rumah sakit di Jawa Tengah.',
    'Fasilitas kredit hingga Rp300 miliar untuk grup rumah sakit swasta.',
    'Pendanaan investor hingga US$3 juta untuk grup rumah sakit.',
    BUMN,
    DIR,
]

CSS = ('<style id="fa-rsrj-css">.rsrj{margin:0 0 26px;max-width:780px;border:1px solid #333;border-radius:12px;'
       'background:#1e1e1e;padding:16px 18px}.rsrj .h{margin:0 0 8px;font-size:13px;font-weight:600;letter-spacing:.14em;'
       'text-transform:uppercase;opacity:.75}.rsrj ul{margin:0;padding-left:18px}.rsrj li{margin:4px 0;line-height:1.55;'
       'font-size:14.5px}@media(max-width:620px){.rsrj{padding:13px 14px}.rsrj li{font-size:13.5px}}</style>')

BLOCK = (M + '<div class="rsrj"><p class="h">Rekam Jejak Tim</p><ul>'
         + ''.join('<li>%s</li>' % t.replace('&', '&amp;') for t in ITEMS)
         + '</ul></div><!--/fa-rsrj-->')

# Halaman kota lokasi klien RSIA tidak memuat butir RSIA (hindari mudah ditebak).
SENS = ('purwakarta', 'tangerang')

RJ = re.compile(r'(<h2 id="rekam-jejak[^"]*">[^<]*</h2><ul>)(.*?)(</ul>)', re.S)


def li(t):
    return M + '<li>%s</li>' % t


def patch(s, sens=False):
    if M in s:
        return s, 'skip'
    m = RJ.search(s)
    if m:
        body = m.group(2)
        add_end = ''
        if 'BUMN' not in body:
            add_end += li(BUMN)
        if 'direksi' not in body:
            add_end += li(DIR)
        new = m.group(1) + ('' if sens else li(RSIA)) + body + add_end + m.group(3)
        return s[:m.start()] + new + s[m.end():], 'list'
    k = s.find('<!--/fa-rstim-->')
    if k < 0:
        return s, 'none'
    k += len('<!--/fa-rstim-->')
    s = s[:k] + (BLOCK.replace('<li>%s</li>' % RSIA, '') if sens else BLOCK) + s[k:]
    if 'id="fa-rsrj-css"' not in s:
        s = s.replace('</head>', CSS + '</head>', 1)
    return s, 'block'


def main():
    files = []
    for fam in ('konsultan-rumah-sakit', 'pendanaan-rumah-sakit'):
        files += sorted(glob.glob('%s/%s/**/index.html' % (ROOT, fam), recursive=True))
    stat = {}
    for f in files:
        s = open(f, encoding='utf-8').read()
        n, how = patch(s, any(x in f for x in SENS))
        stat[how] = stat.get(how, 0) + 1
        if how in ('list', 'block') and not DRY:
            open(f, 'w', encoding='utf-8').write(n)
    print(len(files), 'files', stat, '(dry)' if DRY else '')


if __name__ == '__main__':
    main()
