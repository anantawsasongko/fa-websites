#!/usr/bin/env python3
"""19 Nov 2026: nilai tambah "data dirapikan tim FA sampai siap audit" di semua
layanan yang memakai KAP DHN & Rekan (FA, CariAkuntan, UpdateSAK).

Bos: "tim FA Indonesia bantu data klien yang sangat berantakan menjadi lebih rapi,
akuntabel, dan audit ready. Klien dapat value lebih, lebih cepat rilis, lebih clean
opininya. Implisitkan di semua layanan FA yang menggunakan KAP."

Cara kerja: BEKERJA DI out/ (lihat PERINGATAN BUILD di README-DEPLOY). Satu sisipan
per halaman, di titik KAP DHN yang paling awal di dokumen (kartu dhn2, kotak lk2,
hero audit industri, kartu tim audit, kartu US, kalimat rekanan CA/US, beberapa halaman FA).
Teks dibungkus <!--fa-arv-->...<!--/fa-arv--> supaya idempoten.
Tanpa janji opini, tanpa kata "mitra", tanpa nama orang.

Pakai: python3 fa_audit_ready_nilai_20261119.py [--dry] [--buka]
"""
import os, re, sys

DRY = '--dry' in sys.argv
UNDO = '--buka' in sys.argv  # buang semua sisipan fa-arv
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
SITES = ['faindonesia', 'cariakuntan', 'updatesak']  # --buka menyapu ketiganya
M0, M1 = '<!--fa-arv-->', '<!--/fa-arv-->'

# kalimat utuh (kartu), kalimat sambung (di dalam paragraf yang sudah ada)
TXT = 'Data dan pembukuan yang belum tertata kami rapikan dulu sampai akuntabel dan siap audit, jadi permintaan auditor terjawab lebih cepat, koreksi lebih sedikit, dan laporan audit Anda tidak molor.'

# REVISI 19 Nov malam (Bos): JANGAN menempel di kotak/kalimat KAP DHN (risiko aturan
# iklan IAPI). Hanya di layanan FA sendiri: hero /jasa-pendampingan-audit/ + 113 kota.
RX = re.compile(r'membahas koreksi audit dengan bahasa auditor\.</p>')
RX_UNDO = re.compile(r' ?<!--fa-arv-->.*?<!--/fa-arv-->', re.S)

def undo(s):
    return RX_UNDO.sub('', s)

def apply(s):
    if UNDO:
        return undo(s)
    if M0 in s:
        return s
    m = RX.search(s)
    if not m:
        return s
    blk = f'{M0}<p class="t arv" style="max-width:62em">{TXT}</p>{M1}'
    return s[:m.end()] + blk + s[m.end():]

def main():
    tot = {}
    for site in SITES:
        n = 0
        for root, _, fs in os.walk(os.path.join(ROOT, site)):
            for f in fs:
                if f != 'index.html':
                    continue
                p = os.path.join(root, f)
                s = open(p, encoding='utf-8').read()
                t = apply(s)
                if t != s:
                    n += 1
                    if not DRY:
                        open(p, 'w', encoding='utf-8').write(t)
        tot[site] = n
    print(('DRY ' if DRY else '') + 'diubah:', tot)

if __name__ == '__main__':
    main()
