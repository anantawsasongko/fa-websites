#!/usr/bin/env python3
"""Tiga video FA Jupiter, Saturn, Venus PALING ATAS di tab Apps (/apps/), narasi jualan (13 Nov 2026).
BEKERJA LANGSUNG DI out/faindonesia/apps/index.html, idempoten (penanda <!--bmp3a--> ... <!--/bmp3a-->).

Pemicu (Bos): "Ini juga ada di paling atas tab apps ya. Dengan narasi yang beda. Kalau di layanan, lebih ke
penunjang. Kalau di apps, lebih ke jualan."
Beda dengan blok /layanan/ (fa_bumper_apps_20261113.py, penanda bmp3, narasi cara kerja tanpa ajakan):
di sini tiap video punya kalimat manfaat dan tombol membuka aplikasinya. Video dan poster sama
(media/cara-kerja-fa-*.mp4, sudah disalin ke out/ oleh fa_bumper_apps_20261113.py).
H1 halaman tidak diubah; judul blok ini H2. Aturan apps tetap: tanpa kata "bayar", tanpa janji berlebihan.

URUTAN: setelah fa_bumper_apps_20261113.py, sebelum fa_rendah_hati_20261112.py. Dry run: --dry.
"""
import os, re, sys, json
import fa_bumper_apps_20261113 as base

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'out', 'faindonesia')
P = os.path.join(OUT, 'apps', 'index.html')
BASE = 'https://faindonesia.co.id'
# slug, nama, judul manfaat, kalimat, label tombol, link tombol
ITEMS = [
    ('jupiter', 'FA Jupiter', 'Buku Besar Jadi Laporan Keuangan Siap Audit',
     'Upload COA dan buku besar, lalu neraca saldo, jurnal penyesuaian, dan laporan keuangan sesuai PSAK atau SAK EMKM '
     'tersusun otomatis.', 'Buka FA Jupiter', '/audit-ready/'),
    ('saturn', 'FA Saturn', 'Audit Rapi dari Perencanaan sampai Sign-off',
     'Untuk KAP: perencanaan, kertas kerja, pengujian, dan sign-off dalam satu tempat, sehingga setiap kesimpulan '
     'punya jejak.', 'Buka FA Saturn', '/saturn/'),
    ('venus', 'FA Venus', 'Valuasi, Kredit, dan Pajak Terjawab dalam Hitungan Menit',
     'Isi angka usaha Anda, hasil langsung keluar: valuasi, kapasitas kredit, PPh, PPN, sampai unit cost rumah sakit.',
     'Lihat Aplikasi FA Venus', '#grid'),
]

CSS = ('<style id="bmp3a-css">'
       '.bmp3.bmp3a{margin:0;padding:0;border-bottom:0}'
       '.bmp3a h3.k{margin:16px 0 4px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);'
       'font-family:inherit;font-weight:600}'
       '.bmp3a h4{margin:0 0 8px;font-family:var(--f-display,"Times New Roman",Times,serif);font-weight:400;font-size:21px;'
       'line-height:1.25;color:var(--ink,#fff)}'
       '.bmp3a .go{display:inline-flex;align-items:center;height:40px;padding:0 18px;margin-top:14px;border-radius:999px;'
       'background:#fff;color:#111;font-weight:600;font-size:14px;text-decoration:none}'
       '.bmp3a .go:hover{opacity:.88}'
       '.bmp3a .sh{margin-top:12px}'
       '</style>')


def item(slug, name, head, cap, btn, href):
    vid = '/media/cara-kerja-fa-%s.mp4' % slug; pos = '/media/cara-kerja-fa-%s.jpg' % slug
    url = BASE + '/apps/#video-' + slug; title = name + ': ' + head
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'VideoObject', 'name': title, 'description': cap,
                     'thumbnailUrl': BASE + pos, 'contentUrl': BASE + vid, 'uploadDate': '2026-11-13', 'duration': 'PT30S',
                     'inLanguage': 'en', 'publisher': {'@type': 'Organization', 'name': 'FA Indonesia', 'url': BASE + '/'}},
                    ensure_ascii=False)
    return ('<div class="it" id="video-%s"><div class="v"><video controls playsinline preload="none" poster="%s" '
            'aria-label="Video %s"><source src="%s" type="video/mp4"/></video></div>'
            '<h3 class="k">%s</h3><h4>%s</h4><p>%s</p>'
            '<a class="go" href="%s" data-bmp3a="%s">%s</a>'
            '<div class="sh"><div class="share" data-url="%s" data-tool="%s" data-kick="FA Indonesia" data-lab="Bagikan">'
            '<span data-story="%s" data-title="%s" hidden></span></div></div>'
            '<script type="application/ld+json">%s</script></div>'
            % (slug, pos, name, vid, name, head, cap, href, slug, btn, url, title, pos, title, ld))


BLOCK = ('<!--bmp3a-->' + base.CSS + CSS
         + '<section class="sec" id="video" aria-label="Video FA Apps"><div class="bmp3 bmp3a">'
         '<h3>FA Apps dalam 30 Detik</h3>'
         '<h2>Tiga Aplikasi, Satu Alur Kerja Keuangan</h2>'
         '<p class="lead">Tonton 30 detik, lalu coba dengan data Anda sendiri. Download template Excel, isi, upload, '
         'dan hasilnya langsung keluar di browser Anda.</p>'
         '<div class="g">' + ''.join(item(*x) for x in ITEMS) + '</div></div></section><!--/bmp3a-->\n')


def main(dry=False):
    for slug in ('jupiter', 'saturn', 'venus'):
        for ext in ('mp4', 'jpg'):
            f = os.path.join(OUT, 'media', 'cara-kerja-fa-%s.%s' % (slug, ext))
            if not os.path.exists(f):
                sys.exit('aset tidak ada di out/: %s (jalankan fa_bumper_apps_20261113.py dulu)' % f)
    h = open(P, encoding='utf-8').read()
    new = re.sub(r'<!--bmp3a-->.*?<!--/bmp3a-->\n?', '', h, flags=re.S)
    m = new.find('<main'); k = new.find('<section class="sec">', m)
    if m < 0 or k < 0:
        sys.exit('section pertama di <main> /apps/ tidak ditemukan')
    new = new[:k] + BLOCK + new[k:]
    changed = new != h
    if changed and not dry:
        open(P, 'w', encoding='utf-8').write(new)
    print('bmp3a:', 'berubah' if changed else 'tidak berubah', '(dry run)' if dry else '')


if __name__ == '__main__':
    main('--dry' in sys.argv)
