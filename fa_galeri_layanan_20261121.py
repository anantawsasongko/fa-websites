#!/usr/bin/env python3
"""Lima foto baru di galeri tab Layanan (21 Nov 2026). Idempoten, --dry, penanda <!--gal21-->.

Pemicu (Bos, kirim 5 foto): "Tambahkan sama Direksi RS klien foto yang pertama, dan sisanya itu
sama Bank Mitra. Di foto foto tab layanan web FA".

Bekerja di out/faindonesia/layanan/index.html DAN di sumber
FA-Indonesia_Website_SIAP-UPLOAD-v58/layanan/index.html (blok galeri yang sama), supaya build ulang
tidak menghilangkannya. Foto ada di img/galeri/ (sumber dan out), lebar 1200 px, tanpa metadata;
nama dan logo rumah sakit di latar dua foto disamarkan (aturan lama: nama klien tidak ditampilkan).

Tata letak: foto direksi satu baris penuh (g-wide), empat foto bank 2 x 2 (g-big), jadi bento tetap
penuh tanpa lubang. Posisi potong per foto diatur di CSS blok ini supaya wajah tidak terpotong.
Galeri di /artikel/ (Eksplor) tidak disentuh.

Sekalian: elemen <dialog id="lightbox"> sudah lama hilang dari halaman ini (CSS dan script-nya masih
ada), jadi klik foto tidak membuka apa pun. Dipasang lagi tepat setelah section galeri (penanda
<!--gal21-lb-->) supaya semua foto galeri bisa dibuka besar.
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FILES = [os.path.join(ROOT, 'out', 'faindonesia', 'layanan', 'index.html'),
         os.path.join(ROOT, 'FA-Indonesia_Website_SIAP-UPLOAD-v58', 'layanan', 'index.html')]
DRY = '--dry' in sys.argv

FOTO = [
    ('bersama-direksi-rs-klien', 1200, 1600, 'g-wide', 'g21a',
     'FA Indonesia bersama direksi rumah sakit klien',
     'Bersama Direksi Rumah Sakit Klien'),
    ('bersama-tim-bank-mitra-1', 1200, 900, 'g-big', 'g21b',
     'FA Indonesia bersama tim bank mitra seusai pertemuan',
     'Bersama Tim Bank Mitra seusai Pertemuan'),
    ('bersama-tim-bank-mitra-2', 1200, 1334, 'g-big', 'g21c',
     'FA Indonesia berdiskusi dengan tim bank mitra',
     'Diskusi bersama Tim Bank Mitra'),
    ('bersama-tim-bank-mitra-3', 1200, 1410, 'g-big', 'g21d',
     'FA Indonesia makan siang bersama tim bank mitra',
     'Makan Siang bersama Tim Bank Mitra'),
    ('bersama-tim-bank-mitra-4', 1200, 1290, 'g-big', 'g21e',
     'FA Indonesia dalam jamuan bersama tim bank mitra',
     'Jamuan bersama Tim Bank Mitra'),
]

CSS = ('<style id="gal21-css">'
       '.bento .g-wide{grid-column:1/-1;grid-row:span 2}'
       '.gi.g21a img{object-position:50% 60%}'
       '.gi.g21b img{object-position:50% 50%}'
       '.gi.g21c img{object-position:50% 80%}'
       '.gi.g21d img{object-position:50% 90%}'
       '.gi.g21e img{object-position:50% 95%}'
       '@media (max-width:720px){.bento .g-wide{grid-row:span 1}'
       '.gi.g21a img{object-position:50% 57%}'
       '.gi.g21b img{object-position:50% 90%}'
       '.gi.g21c img{object-position:50% 56%}'
       '.gi.g21d img{object-position:50% 81%}'
       '.gi.g21e img{object-position:50% 74%}}'
       '</style>')


def blok():
    f = ''.join(
        f'<figure class="gi {cls} {k}"><button class="gbtn" data-full="/img/galeri/{n}.jpg" type="button">'
        f'<img alt="{alt}" height="{h}" loading="lazy" src="/img/galeri/{n}.jpg" width="{w}"/></button>'
        f'<figcaption>{cap}</figcaption></figure>'
        for n, w, h, cls, k, alt, cap in FOTO)
    return '<!--gal21-->' + CSS + f + '<!--/gal21-->'


LB = ('<!--gal21-lb--><dialog aria-label="Foto galeri" class="lightbox" id="lightbox">'
      '<button aria-label="Tutup" class="lbclose" type="button">&times;</button><img alt=""/></dialog>')


def apply(t):
    if 'id="lightbox"' not in t:
        s = t.index('id="galeri-layanan"')
        e = t.index('</section>', s) + len('</section>')
        t = t[:e] + LB + t[e:]
    if '<!--gal21-->' in t:
        a = t.index('<!--gal21-->')
        b = t.index('<!--/gal21-->') + len('<!--/gal21-->')
        return t[:a] + blok() + t[b:]
    s = t.index('id="galeri-layanan"')
    g = t.index('<div class="gallery bento">', s)
    e = t.index('</section>', g)
    k = t.rfind('</figure>', g, e) + len('</figure>')
    if k < g:
        raise SystemExit('figure galeri tidak ditemukan')
    return t[:k] + blok() + t[k:]


def main():
    n = 0
    for p in FILES:
        t = open(p, encoding='utf-8').read()
        u = apply(t)
        if u != t:
            n += 1
            if not DRY:
                open(p, 'w', encoding='utf-8').write(u)
        for name, *_ in FOTO:
            img = os.path.join(os.path.dirname(os.path.dirname(p)), 'img', 'galeri', name + '.jpg')
            if not os.path.exists(img):
                raise SystemExit('foto belum ada: ' + img)
    print(('DRY ' if DRY else '') + f'{n} file berubah')


if __name__ == '__main__':
    main()
