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
SITES = ['faindonesia', 'cariakuntan', 'updatesak']
M0, M1 = '<!--fa-arv-->', '<!--/fa-arv-->'

# kalimat utuh (kartu), kalimat sambung (di dalam paragraf yang sudah ada)
TXT = {
 'id': ('Sebelum pemeriksaan dimulai, tim FA Indonesia merapikan data dan pembukuan yang belum tertata sampai siap audit, jadi prosesnya lebih lancar, koreksi lebih sedikit, dan laporan auditor lebih cepat terbit.',
        'Data yang belum tertata dirapikan dulu oleh tim FA Indonesia sampai siap audit, sehingga pemeriksaan lebih lancar dan laporan auditor lebih cepat terbit.'),
}
STY = 'margin:4px 0 16px;padding-left:10px;border-left:2px solid #E9B949'

def lang_of(s):
    # semua titik sisip berbahasa Indonesia (juga di halaman /en/), jadi kalimat ikut ID
    return 'id'

def full(l):
    return f'{M0}<p class="arv" style="{STY}">{TXT[l][0]}</p>{M1}'

def inline(l):
    return f' {M0}{TXT[l][1]}{M1}'

# (regex, mode). mode 'after' = sisip <p> utuh setelah match; 'in' = sambung kalimat
# sebelum tag penutup yang ditangkap di grup 'end'.
PATS = [
 # FA pilar audit: hero
 (re.compile(r'lalu audit dilaksanakan KAP DHN &amp; Rekan yang terdaftar OJK\.(?P<end>)'), 'in'),
 # kartu KAP DHN (dhn2, FA + CA), dua varian teks
 (re.compile(r'<p>Izin Menteri Keuangan KMK No\. 592/KM\.1/2023, terdaftar OJK, anggota jaringan PA Global\. [^<]*</p>'), 'after'),
 # kotak lk2 FA
 (re.compile(r'Oleh KAP DHN &amp; Rekan, terdaftar OJK\. Untuk kredit bank, laporan tahunan PT di SABH, tender, atau investor\.(?P<end></p>)'), 'in'),
 # hero halaman audit per industri
 (re.compile(r'Audit dan opini oleh KAP DHN &amp; Rekan yang terdaftar di OJK\.(?P<end></p>)'), 'in'),
 # kartu tim (Dwi) di halaman audit
 (re.compile(r'Audit dan opininya dilakukan KAP DHN &amp; Rekan yang terdaftar OJK\. Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda\.(?P<end></p>)'), 'in'),
 # UpdateSAK beranda: kartu layanan audit
 (re.compile(r'Audit umum untuk bank, tender, investor, dan laporan tahunan PT\. Penyusun dan auditor selalu pihak berbeda\.(?P<end>\s*<)'), 'in'),
 # UpdateSAK: kalimat dibantu tim FA
 (re.compile(r'audit oleh KAP DHN &amp; Rekan \(terdaftar OJK\)\. Rinciannya di (?P<end>)'), 'pre'),
 # CariAkuntan halaman segmen: rekanan yang disarankan
 (re.compile(r'dengan FA Indonesia sebagai pintu kontaknya\. Penyusun dan auditor adalah kantor yang berbeda\.(?P<end>)'), 'in'),
 # FA pendampingan audit: paragraf independensi
 (re.compile(r'Bila auditor Anda adalah KAP DHN &amp; Rekan, penyiapan laporan keuangan dan skedul dilakukan pihak yang berbeda dari tim audit[^<]*(?P<end></p>)'), 'in'),
 # FA pendanaan RS provinsi: daftar layanan
 (re.compile(r'penyusunan oleh KJA Farhani K\.N\., audit oleh KAP DHN &amp; Rekan \(terdaftar OJK\)\.(?P<end></li>)'), 'in'),
 # FA akuntan forensik provinsi: FAQ siapa auditornya
 (re.compile(r'Audit dilakukan KAP DHN &amp; Rekan, kantor akuntan publik yang terdaftar OJK\. Penyusun laporan keuangan dan auditor selalu pihak yang berbeda\.(?P<end><)'), 'in'),
 # FA /layanan/ kartu Laporan Keuangan dan Audit
 (re.compile(r'Penyusunan oleh KJA Farhani K\.N\., audit oleh KAP DHN &amp; Rekan yang terdaftar OJK\. Untuk bank, laporan tahunan PT, tender, dan investor\.(?P<end></p>)'), 'in'),
 # FA penyusunan LK BPR
 (re.compile(r'Untuk satu BPR, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda, sesuai prinsip independensi\.(?P<end></p>)'), 'in'),
 # FA pembukuan bulanan
 (re.compile(r'</a>, pihak terpisah dari penyusun laporan\.(?P<end></p>)'), 'in'),
 # FA untuk notaris
 (re.compile(r'KJA Farhani untuk penyusunan laporan, KAP DHN &amp; Rekan untuk audit\.(?P<end></p>)'), 'in'),
 # FA akuntan terdekat: FAQ
 (re.compile(r'Audit dilakukan KAP DHN &amp; Rekan dengan kunjungan lapangan bila perlu, jadi jarak kantor tidak menghambat\.(?P<end><)'), 'in'),
]

RX_UNDO = re.compile(r' ?<!--fa-arv-->.*?<!--/fa-arv-->', re.S)

def undo(s):
    return RX_UNDO.sub('', s)

def apply(s):
    if UNDO:
        return undo(s)
    if M0 in s or 'KAP DHN' not in s:
        return s
    l = lang_of(s)
    best = None
    for rx, mode in PATS:
        m = rx.search(s)
        if m and (best is None or m.start() < best[0].start()):
            best = (m, mode)
    if not best:
        return s
    m, mode = best
    if mode == 'after':
        return s[:m.end()] + full(l) + s[m.end():]
    if mode == 'pre':
        # sisip kalimat sebelum "Rinciannya di"
        i = m.start() + len('audit oleh KAP DHN &amp; Rekan (terdaftar OJK).')
        return s[:i] + inline(l) + s[i:]
    i = m.start('end')
    return s[:i] + inline(l) + s[i:]

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
