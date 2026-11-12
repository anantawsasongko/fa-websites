#!/usr/bin/env python3
"""Entitas brand FA Indonesia di Google (12 Nov 2026 malam). BEKERJA LANGSUNG DI out/faindonesia, idempoten.

Pemicu (Bos): pencarian "fa indonesia" dibaca Google sebagai Football Association (PSSI); FA baru
muncul sebagai poin ke-3 AI Overview dan yang dikutip LinkedIn, bukan situs.

Yang diubah:
1. Beranda, JSON-LD Organization (#org): sameAs dilengkapi akun brand resmi yang memang sudah
   ditautkan di beranda (LinkedIn page, Instagram, Threads, X), ditambah disambiguatingDescription
   supaya Google membedakan FA Indonesia (penasihat keuangan dan akuntansi) dari arti lain "FA".
2. /layanan/: title dan og:title tidak lagi menyebut "Paket, Fee" (isinya sudah dibuang 12 Nov).

Jalankan sebelum fa_rendah_hati_20261112.py (yang tetap penutup). Argumen --dry hanya menghitung.
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv

SAME_AS = [
    'https://www.linkedin.com/company/faindonesia',
    'https://www.instagram.com/fa.co.id',
    'https://www.threads.com/@fa.co.id',
    'https://x.com/fa_co_id',
]
DISAMBIG = ('Firma penasihat keuangan dan akuntansi (financial advisory) berbasis di Malang, '
            'Indonesia, melayani klien sejak 2016.')
LD = re.compile(r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)', re.S)


def beranda():
    p = os.path.join(ROOT, 'index.html')
    h = open(p, encoding='utf-8').read()
    changed = [False]

    def fix(m):
        try:
            d = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        for n in d.get('@graph', []) if isinstance(d, dict) else []:
            if n.get('@id') == 'https://faindonesia.co.id/#org':
                if n.get('sameAs') != SAME_AS or n.get('disambiguatingDescription') != DISAMBIG:
                    n['sameAs'] = SAME_AS
                    n['disambiguatingDescription'] = DISAMBIG
                    changed[0] = True
        return m.group(1) + json.dumps(d, ensure_ascii=False) + m.group(3) if changed[0] else m.group(0)

    h2 = LD.sub(fix, h, count=1)
    if changed[0] and not DRY:
        open(p, 'w', encoding='utf-8').write(h2)
    return int(changed[0])


def layanan():
    p = os.path.join(ROOT, 'layanan', 'index.html')
    h = open(p, encoding='utf-8').read()
    h2 = h.replace('Layanan, Paket, Fee dan Rekam Jejak', 'Layanan dan Rekam Jejak')
    if h2 != h and not DRY:
        open(p, 'w', encoding='utf-8').write(h2)
    return int(h2 != h)


if __name__ == '__main__':
    print('diubah', beranda() + layanan())
