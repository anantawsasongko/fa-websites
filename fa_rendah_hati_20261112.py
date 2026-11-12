#!/usr/bin/env python3
"""Buang kalimat yang menonjolkan nama Ananta (12 Nov 2026 malam).
BEKERJA LANGSUNG DI out/faindonesia, idempoten, jalankan PALING AKHIR (setelah fa_lk2_lipat_20261112.py).

Pemicu (Bos): "Kayak gini itu paragraf songong. Ananta itu siapa sih, kan bukan orang besar. Hapus aja
kalimat gini gini, saya udah berulangkali ingatkan." Aturan 8 dan 9 Nov ("Anda bicara langsung dengan
Ananta W. Sasongko, CPA", "dijawab Ananta W. Sasongko, CPA") DICABUT. Yang boleh memuat nama: tombol
"Chat Ananta, CPA", kartu profil tim, byline artikel, halaman profil /ananta-w-sasongko/.

Yang dikerjakan (teks tampil, FAQ, meta description, JSON-LD):
- kalimat "Sejak chat pertama Anda bicara langsung dengan ...", "... dijawab Ananta ...", "Anda berdiskusi
  langsung dengan ...", "Diskusi awalnya langsung dengan ..." dibuang atau dinetralkan ke "tim FA Indonesia";
- judul blok "Ditangani Langsung, Bukan Diteruskan" jadi "Tim FA Indonesia"; label kartu "Kontak Anda
  Sejak Awal" jadi "FA Indonesia".
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv

N = r'(?:<a href="/ananta-w-sasongko/"[^>]*>)?(?:Dr\. \(C\) )?Ananta W\. Sasongko(?:, S\.E\., M\.S\.A\., Ak\., CPA, CTT, FMVA, FPAP|, CPA)?(?:</a>)?'

RULES = [
    # blok tim / paragraf "langsung"
    (r'Sejak chat pertama Anda bicara langsung dengan ' + N + r'\. (?:Ia yang membaca dokumen Anda, menyusun rencana kerja, dan memeriksa hasilnya sebelum diserahkan[^.<]*\. ?)?', ''),
    (r'Anda berdiskusi langsung dengan ' + N + r' sejak chat pertama: ia membaca dokumen Anda, menyusun rencana kerja, dan memeriksa hasilnya sebelum diserahkan\. ', ''),
    (r'Anda berdiskusi langsung dengan ' + N + r', yang mengikuti SAK terbaru dan memahami cara kerja auditor, termasuk auditor KAP besar\. ', 'Tim FA Indonesia mengikuti SAK terbaru dan memahami cara kerja auditor. '),
    # kotak kontak dan penutup artikel
    (r' ?Satu chat WhatsApp, dijawab ' + N + r', yang mendampingi sampai laporan selesai\.', ''),
    (r' ?Satu chat WhatsApp, dijawab ' + N + r'\.', ''),
    (r', sementara sisi keuangan, M&amp;A, dan valuasi dipegang ' + N + r'\.', '.'),
    (r' When you need hands-on support, you talk directly with ' + N + r'\.', ' When you need hands-on support, contact the FA Indonesia team.'),
    (r'需要协助时，直接与 ' + N + r' 沟通。', '需要协助时，请联系 FA Indonesia 团队。'),
    (r'(>)Ditangani Langsung, Bukan Diteruskan(<)', r'\1Tim FA Indonesia\2'),
    (r'pintu kontaknya: chat WhatsApp Anda dijawab ' + N + r'\.', 'pintu kontaknya.'),
    (r'lewat WhatsApp, dijawab ' + N + r'\.', 'lewat WhatsApp.'),
    (r' Your WhatsApp message is answered by Ananta directly\.', ''),
    # FAQ dan kalimat lepas
    (N + r' dan tim FA Indonesia melayani', 'Tim FA Indonesia melayani'),
    (r'didampingi daring dengan ' + N + r', dan kunjungan', 'didampingi daring oleh tim FA Indonesia, dengan kunjungan'),
    (r'Diskusi awalnya langsung dengan ' + N + r' lewat WhatsApp\.', 'Diskusi awalnya lewat WhatsApp.'),
    (r'Diskusi awal bisa langsung dengan ' + N + r', dan bila', 'Diskusi awal bisa lewat WhatsApp, dan bila'),
    (r'(Untuk [^.<]{5,80}), Anda bicara langsung dengan ' + N + r'\. Biasanya dimulai', r'\1, biasanya dimulai'),
    (r'Bila perlu pendampingan, Anda bicara langsung dengan ' + N + r'[^.<]*\.', 'Bila perlu pendampingan, hubungi tim FA Indonesia.'),
    (r'Anda cukup bicara dengan ' + N, 'Anda cukup menghubungi tim FA Indonesia'),
    (r'Anda bicara langsung dengan ' + N, 'Anda dilayani tim FA Indonesia'),
    (r'Anda berdiskusi langsung dengan ' + N, 'Anda berdiskusi dengan tim FA Indonesia'),
    (r', dikerjakan langsung bersama ' + N + r'(?=[.,"<])', ''),
    (r'Ditangani langsung: ' + N + r'[^.<]*\. ?', ''),
    (r'dengan peran CFO dijalankan oleh ' + N, 'dengan peran CFO dijalankan tim FA Indonesia'),
    (r'Peran CFO dijalankan oleh ' + N, 'Peran CFO dijalankan tim FA Indonesia'),
    (r', diawasi ' + N + r'(?=[.,"<])', ''),
    (r'Dipimpin ' + N, 'Dikerjakan tim FA Indonesia'),
    # judul dan label kartu
    (r'(<h2[^>]*>)Ditangani Langsung, Bukan Diteruskan(</h2>)', r'\1Tim FA Indonesia\2'),
    (r'(<small[^>]*>)Kontak Anda Sejak Awal(</small>)', r'\1FA Indonesia\2'),
    (r'(<span>)Kontak Anda Sejak Awal, (Persiapan Audit dan Laporan Keuangan</span>)', r'\1\2'),
    # sisa spasi dan paragraf kosong
    (r'<p>\s+', '<p>'),
    (r'<p[^>]*>\s*</p>', ''),
]
RULES = [(re.compile(a), b) for a, b in RULES]
SKIP = ('ananta-w-sasongko' + os.sep,)


def clean(t, p=''):
    if 'Ananta' not in t and 'Ditangani Langsung' not in t and 'Kontak Anda Sejak Awal' not in t:
        return t
    for rx, rep in RULES[:-2]:
        t = rx.sub(rep, t)
    return t


def main():
    n = 0
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            if os.path.relpath(p, ROOT).startswith(SKIP):
                continue
            o = open(p, encoding='utf-8').read()
            t = clean(o, p)
            if t != o:
                t = re.sub(r'<p>\s+(?=\S)', '<p>', t)
                t = re.sub(r'<p[^>]*>\s*</p>', '', t)
                n += 1
                if not DRY:
                    open(p, 'w', encoding='utf-8').write(t)
    print(f'diubah {n}' + (' (dry run)' if DRY else ''))


if __name__ == '__main__':
    main()
