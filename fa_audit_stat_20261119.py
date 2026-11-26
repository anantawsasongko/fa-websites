#!/usr/bin/env python3
"""19 Nov 2026: stat hero halaman AUDIT FA diganti dari rekam jejak umum
(Rp1,1 T+, 10+, 2016) jadi bukti yang relevan untuk pembeli audit:
57+ klien 2025, rilis LK ±2 minggu karena data dirapikan, audit lebih lancar lewat KAP mitra.

Permintaan Bos 19 Nov malam. Aturan yang dijaga:
- klaim milik FA Indonesia (layanan merapikan data), TIDAK menyebut nama KAP DHN dan tidak ditempel di kartu KAP.
- tanpa kata jaminan; angka 2 minggu ditulis "bisa".
Cakupan: /jasa-audit-laporan-keuangan/<daerah>/ dan /jasa-pendampingan-audit/<kota>/ (blok fa-dv2f).
Bekerja di out/faindonesia, idempoten. --dry hanya hitung, --buka mengembalikan stat lama.
JALANKAN PALING AKHIR (sesudah fa_daerah_v2_20261114.py, yang menulis ulang blok fa-dv2f).
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv
BUKA = '--buka' in sys.argv
FAMILIES = ('jasa-audit-laporan-keuangan/', 'jasa-pendampingan-audit/')

OLD = ('<!--fa-dv2f--><div aria-label="Rekam jejak FA Indonesia" class="dvf">'
       '<div><b>Rp1,1 T+</b><span>Pembiayaan perbankan dicairkan, ditambah pendanaan investor hingga US$3 juta</span></div>'
       '<div><b>10+</b><span>Mandat divestasi aktif: rumah sakit dan BPR</span></div>'
       '<div><b>2016</b><span>Tahun berdiri</span></div>'
       '</div><!--/fa-dv2f-->')

NEW = ('<!--fa-dv2f--><div aria-label="Rekam jejak FA Indonesia di audit" class="dvf" data-aud="1">'
       '<div><b>57+</b><span>Perusahaan klien FA Indonesia pada 2025</span></div>'
       '<div><b>2 minggu</b><span>Laporan keuangan bisa rilis secepat ini, karena data kami rapikan dulu sebelum diaudit</span></div>'
       '<div><b>KAP OJK</b><span>Audit oleh KAP terdaftar OJK berjalan lebih lancar, karena data sudah siap sebelum auditor datang</span></div>'
       '</div><!--/fa-dv2f-->')

RX = re.compile(r'<!--fa-dv2f-->.*?<!--/fa-dv2f-->', re.S)


def main():
    n = 0
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if fn != 'index.html':
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
            if not rel.startswith(FAMILIES):
                continue
            h = open(p, encoding='utf-8', errors='surrogateescape').read()
            m = RX.search(h)
            if not m:
                continue
            want = OLD if BUKA else NEW
            if m.group(0) == want:
                continue
            if not BUKA and m.group(0) != OLD:
                continue
            h2 = h[:m.start()] + want + h[m.end():]
            n += 1
            if not DRY:
                open(p, 'w', encoding='utf-8', errors='surrogateescape').write(h2)
    print(('DRY ' if DRY else '') + ('buka' if BUKA else 'terapkan') + ': %d file berubah' % n)


if __name__ == '__main__':
    main()
