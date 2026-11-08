#!/usr/bin/env python3
"""Anti-makelar lanjutan (8 Nov 2026, Bos: "jangan terkesan makelar"). BEKERJA DI out/faindonesia, idempoten.
- Menu "Mitra KAP & KJA" jadi "Tim & Izin" (URL /mitra-kap-kja/ tetap supaya indeks dan link aman).
- Halaman /mitra-kap-kja/ ditulis ulang jadi "Tim dan Izin Praktik": tanpa mitra, satu pintu, referral.
- KJA Farhani tidak ditulis "Akuntan Berpraktik" (izin AB expired).
- Kalimat perantara lain: "minta kami carikan", "menghubungkan dengan KJPP", "beserta mitranya", artikel "Mitra FA Indonesia".
Jalankan setelah fa_langsung_20261108.py dan fa_seo_rapi_20261108.py.
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv

NAV = [('<a href="/mitra-kap-kja/">Mitra KAP &amp; KJA</a>', '<a href="/mitra-kap-kja/">Tim &amp; Izin</a>'),
       ('<a href="/mitra-kap-kja/">Mitra KAP, KJA, dan Konsultan Pajak FA</a>', '<a href="/mitra-kap-kja/">Tim dan Izin Praktik FA Indonesia</a>')]

T_OLD = 'Mitra KAP, KJA, dan Konsultan Pajak FA Indonesia: KAP DHN & Rekan, KJA DHN, KKP DHN, KJA Farhani'
T_NEW = 'Tim dan Izin Praktik FA Indonesia: Audit, Laporan Keuangan, dan Pajak'
D_NEW = 'Anda bicara langsung dengan Ananta W. Sasongko, CPA. Audit oleh KAP DHN & Rekan terdaftar OJK, laporan keuangan dan pajak oleh kantor berizin.'

PAGE = [
    ('data-tool="Mitra KAP, KJA, dan Konsultan Pajak FA Indonesia: KAP DHN &amp; Rekan, KJA DHN, KKP DHN, KJA F"', 'data-tool="Tim dan Izin Praktik FA Indonesia"'),
    ('Tim dan Izin Praktik: Audit, Laporan Keuangan, Pajak, KJA Farhani', 'Tim dan Izin Praktik: Audit, Laporan Keuangan, Pajak'),
    (T_OLD, T_NEW),
    ('Mitra KAP dan KJA: KAP DHN, KJA DHN, KKP DHN | FA Indonesia', 'Tim dan Izin Praktik: Audit, Laporan Keuangan, Pajak'),
    ('Mitra KAP dan KJA: KAP DHN, KJA DHN, KKP DHN', 'Tim dan Izin Praktik: Audit, Laporan Keuangan, Pajak'),
    ('"name": "Mitra KAP dan KJA"', '"name": "Tim dan Izin Praktik"'),
    ('Referral and financing readiness', 'Accounting, tax, and statutory audit services'),
    ('Mitra · KAP, KJA, dan Konsultan Pajak', 'Tim · Audit, Laporan Keuangan, dan Pajak'),
    ('Mitra Profesional FA Indonesia', 'Izin Praktik yang Dipakai'),
    ('dipimpin Akuntan Berpraktik', 'dipimpin Farhani Kautsar Nugraha, CA'),
    ('Satu Pintu dari Pembukuan sampai Dana Cair', 'Alur Kerja dari Pembukuan sampai Dana Cair'),
    ('satu-pintu-dari-pembukuan-sampai-dana-cair', 'alur-kerja-dari-pembukuan-sampai-dana-cair'),
    ('KJA mitra merapikan pembukuan dan menyusun laporan keuangan.', 'Pembukuan dirapikan dan laporan keuangan disusun oleh kantor jasa akuntansi berizin.'),
    ('KKP mitra merekonsiliasi pajak dan menyiapkan SPT', 'Pajak direkonsiliasi dan SPT disiapkan oleh konsultan pajak berizin'),
    ('KAP mitra mengaudit laporan keuangan secara independen.', 'KAP DHN & Rekan mengaudit laporan keuangan secara independen.'),
    ('Mitra kami melayani perusahaan', 'Kami melayani perusahaan'),
    ('Website mitra:', 'Website:'),
    ('Apakah FA Indonesia punya mitra KAP?', 'Siapa yang mengaudit laporan keuangan?'),
    ('Ya. FA Indonesia bermitra dengan KAP DHN & Rekan untuk audit laporan keuangan', 'KAP DHN & Rekan, kantor akuntan publik terdaftar OJK, untuk audit laporan keuangan'),
    ('FA Indonesia mengatur pembagian peran antar mitra sejak awal.', 'Pembagian peran diatur sejak awal perikatan.'),
    ('Bisa. Mitra melayani seluruh Indonesia', 'Bisa. Kami melayani seluruh Indonesia'),
    ('KAP, KJA, dan konsultan pajak mitra FA Indonesia: KAP DHN & Rekan, KJA DHN, KKP DHN, KJA Farhani. Audit, pembukuan, pajak, sampai kredit cair.', D_NEW),
    ('Kerja%20Sama%20Mitra%20FA%20Indonesia', 'Konsultasi%20FA%20Indonesia'),
    ('>Email Kerja Sama<', '>Email Ananta, CPA<'),
]
RX_PAGE = [
    (re.compile(r'Ingin membandingkan dengan kantor lain di kota Anda\? Gunakan <a [^>]*>Cari Akuntan</a>\s*\.\s*'), ''),
]

GLOBAL = [
    ('celah yang perlu ditutup beserta mitranya (KJA, KAP, KJPP, notaris).', 'celah yang perlu ditutup, dan checklist data room.'),
    ('"Audit and assurance referral"', '"Audit and assurance"'),
    ('"Referral and financing readiness partnership"', '"Financing readiness advisory"'),
    ('celah yang perlu ditutup beserta mitranya (KJA, KAP, KJPP, notaris), dan checklist data room', 'celah yang perlu ditutup, dan checklist data room'),
    ('Kami menyiapkan datanya dan menghubungkan dengan KJPP yang sesuai lewat', 'Kami menyiapkan datanya; KJPP berizin bisa dicek lewat'),
    ('FA Indonesia adalah mitra KAP DHN & Rekan. Melalui FA, perusahaan mendapat satu pintu: laporan keuangan dirapikan dulu',
     'Anda bicara langsung dengan Ananta W. Sasongko, CPA: laporan keuangan dirapikan dulu'),
    ('KAP dan KJA untuk Perusahaan: Bedanya, Kapan Butuh, dan Mitra FA Indonesia', 'KAP dan KJA untuk Perusahaan: Bedanya dan Kapan Butuh'),
    ('dipimpin Akuntan Berpraktik', 'dipimpin Farhani Kautsar Nugraha, CA'),
]
RX_GLOBAL = [
    (re.compile(r'atau minta kami carikan yang mau datang ke ([^.<]+)\.'), r'atau chat Ananta, CPA untuk atur kunjungan ke \1.'),
]


def both(pairs):
    out = []
    for a, b in pairs:
        out.append((a, b))
        if '&' in a and '&amp;' not in a:
            out.append((a.replace('&', '&amp;'), b.replace('&', '&amp;')))
    return out


def main():
    n = 0; stat = {}
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            if not f.endswith('.html'):
                continue
            p = os.path.join(d, f)
            s0 = s = open(p, encoding='utf-8').read()
            for a, b in NAV:
                s = s.replace(a, b)
            for a, b in both(GLOBAL):
                if a in s:
                    stat[a[:30]] = stat.get(a[:30], 0) + 1
                    s = s.replace(a, b)
            for rx, b in RX_GLOBAL:
                s = rx.sub(b, s)
            if p.endswith(os.path.join('mitra-kap-kja', 'index.html')):
                for a, b in both(PAGE):
                    s = s.replace(a, b)
                for rx, b in RX_PAGE:
                    s = rx.sub(b, s)
            if s != s0:
                n += 1
                if not DRY:
                    open(p, 'w', encoding='utf-8').write(s)
    print('files', n, stat)


if __name__ == '__main__':
    main()
