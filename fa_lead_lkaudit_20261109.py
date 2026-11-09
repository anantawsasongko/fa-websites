#!/usr/bin/env python3
"""Lead WA penyusunan LK dan audit KAP (9 Nov 2026). BEKERJA LANGSUNG DI out/faindonesia, idempoten.
Jalankan PALING AKHIR (setelah fa_langsung, fa_seo_rapi, fa_tim_izin).

Temuan GSC 90 hari (9 Nov 2026):
- Query "kap <kota>", "audit <kota>", "kantor akuntan publik terdekat" mendarat di /wilayah/<kota>/
  (posisi 3 sampai 9) tapi CTR 0%. Description semua 2.350 halaman /wilayah/ masih
  "laporan keuangan oleh KJA Farhani" (bertentangan dengan keputusan anti-makelar 8 Nov) dan
  tidak menjawab niat pencari.
- Artikel audit/LK dapat impresi terbanyak (opini audit 461, KJA vs KAP 379, LK RS 180), tapi
  tombol WA baru muncul di bagian bawah dan pesannya umum (kredit bank).

Isi:
1. Description (+ og/twitter) /wilayah/**: kalimat baru yang menjawab niat "KAP <kota>", tanpa KJA Farhani.
2. Kotak "Perlu yang Mana?" (penanda <!--fa-lk2-->) tepat di bawah tombol hero, sebelum blok tim:
   dua tombol WA dengan pesan sudah terisi (susun LK / audit KAP) + nama kota.
   Halaman: /wilayah/**, /jasa-audit-laporan-keuangan/**, /jasa-penyusunan-laporan-keuangan/**,
   /laporan-keuangan-*/**, /akuntan-terdekat/, /kap-dhn/, /kja-farhani/.
3. Kotak CTA di tengah artikel audit/LK (penanda <!--fa-lk2a-->), sebelum H2 kedua, pesan WA
   menyebut topik artikel (GA4 generate_lead sudah mencatat link_url, jadi sumber lead terbaca).
"""
import os, re, sys, html
from urllib.parse import quote

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv
WA = 'https://wa.me/6282245260121?text='
M1, M1E = '<!--fa-lk2-->', '<!--/fa-lk2-->'
M2, M2E = '<!--fa-lk2a-->', '<!--/fa-lk2a-->'

ART_AUDIT = ['apakah-perusahaan-butuh-audit-kap', 'audit-rumah-sakit-pertama-kali', 'biaya-audit-kap-faktor-penentu',
             'cara-memilih-kap-untuk-kredit-bank', 'dari-opini-wdp-ke-wtp', 'jenis-opini-audit-dan-dampaknya-ke-bank',
             'kap-murah-apakah-bijak', 'kapan-perusahaan-wajib-diaudit', 'kja-vs-kap', 'kompilasi-review-audit',
             'laporan-audit-lama-keluar', 'mengembangkan-pt-tanpa-audit-kap', 'opini-tidak-menyatakan-pendapat-disclaimer',
             'persiapan-audit-pertama-kali-saldo-awal', 'laporan-tahunan-pt-permenkum-49-2025',
             'kap-dan-kja-mitra-fa-indonesia']
ART_LK = ['biaya-jasa-penyusunan-laporan-keuangan', 'contoh-laporan-keuangan-umkm', 'laporan-keuangan-bankable-investor-ready',
          'laporan-keuangan-berantakan-cara-merapikan', 'laporan-keuangan-kontraktor-psak-115',
          'laporan-keuangan-rumah-sakit-swasta-sesuai-psak', 'laporan-keuangan-untuk-kredit-bank',
          'panduan-implementasi-psak-118', 'psak-119-entitas-anak-tanpa-akuntabilitas-publik',
          'aplikasi-laporan-keuangan-gratis-sesuai-sak-emkm-ep-psak', 'pertanyaan-komisaris-atas-laporan-keuangan']

BOX = ('border:1px solid rgba(233,185,73,.5);border-radius:12px;padding:16px 18px;margin:22px 0 8px;'
       'background:rgba(233,185,73,.07);max-width:760px')
GRID = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:10px'


def wa(msg):
    return WA + quote(msg, safe='')


def url_of(p):
    r = os.path.relpath(p, ROOT).replace(os.sep, '/')
    return '/' if r == 'index.html' else '/' + r[:-10]


def city_of(u, h):
    m = re.search(r'<h1[^>]*>([^<]*)', h)
    t = html.unescape(m.group(1)) if m else ''
    m = re.search(r'\bdi ([A-Z][^:,]{1,40}?)(?::|,|$)', t)
    if m and not u.rstrip('/').count('/') <= 1:
        c = m.group(1).strip()
        if not re.search(r'Indonesia|Seluruh|Usaha|Perusahaan', c):
            return c
    return ''


def lead_box(city):
    dari = f' dari {city}' if city else ''
    di = f' di {city}' if city else ''
    lk = wa(f'Halo Pak Ananta, saya{dari} perlu penyusunan laporan keuangan. Tahun buku: ... Jenis usaha: ...')
    au = wa(f'Halo Pak Ananta, saya{dari} perlu audit laporan keuangan oleh KAP. Keperluan: bank / SABH / tender / investor.')
    return (f'{M1}<div class="lk2" style="{BOX}"><b style="font-size:17px">Perlu yang Mana{di}?</b>'
            f'<div style="{GRID}">'
            f'<div><b>Laporan keuangan belum ada atau belum rapi</b><p style="margin:.3em 0 .6em;opacity:.85">'
            f'Disusun sesuai SAK EMKM, SAK EP, atau PSAK, siap dipakai bank dan auditor.</p>'
            f'<a class="btn solid" href="{lk}" rel="noopener" target="_blank">Tanya Susun Laporan Keuangan</a></div>'
            f'<div><b>Perlu laporan audit KAP</b><p style="margin:.3em 0 .6em;opacity:.85">'
            f'Untuk kredit bank, laporan tahunan PT di SABH, tender, atau investor. Diaudit KAP terdaftar OJK.</p>'
            f'<a class="btn solid" href="{au}" rel="noopener" target="_blank">Tanya Audit KAP</a></div>'
            f'</div></div>{M1E}')


def art_box(kind, title):
    t = title.split(':')[0].strip()
    if kind == 'audit':
        head = 'Perusahaan Anda Perlu Audit KAP?'
        body = ('Kirim tahun buku dan keperluannya (bank, SABH, tender, investor). Kami cek dulu kesiapan laporan '
                'keuangannya, lalu audit oleh KAP terdaftar OJK. Penyusun laporan dan auditor selalu pihak berbeda.')
        msg = f'Halo Pak Ananta, saya baca artikel "{t}". Perusahaan kami perlu audit laporan keuangan oleh KAP.'
        btn = 'Tanya Audit KAP via WhatsApp'
    else:
        head = 'Laporan Keuangan Anda Belum Siap?'
        body = ('Kirim jenis usaha dan tahun bukunya. Laporan keuangan disusun sesuai standar yang berlaku, '
                'siap dipakai bank, auditor, dan investor.')
        msg = f'Halo Pak Ananta, saya baca artikel "{t}". Kami perlu bantuan penyusunan laporan keuangan.'
        btn = 'Tanya Susun Laporan Keuangan'
    return (f'{M2}<div class="lk2a" style="{BOX}"><b style="font-size:17px">{head}</b>'
            f'<p style="margin:.4em 0 .8em">{body}</p>'
            f'<a class="btn solid" href="{wa(msg)}" rel="noopener" target="_blank">{btn}</a></div>{M2E}')


def put(h, start, end, block, anchor_fn):
    h = re.sub(re.escape(start) + r'.*?' + re.escape(end), '', h, flags=re.S)
    i = anchor_fn(h)
    if i < 0:
        return h, False
    return h[:i] + block + h[i:], True


def wil_desc(city):
    for d in (f'Cari KAP atau akuntan di {city}? Audit oleh KAP terdaftar OJK, penyusunan laporan keuangan siap audit, '
              f'dan cek izin KAP. Tanya dulu lewat WhatsApp.',
              f'Cari KAP atau akuntan di {city}? Audit oleh KAP terdaftar OJK dan penyusunan laporan keuangan siap audit.',
              f'KAP dan akuntan di {city}: audit oleh KAP terdaftar OJK dan laporan keuangan siap audit.'):
        if len(d) <= 158:
            return d
    return None


def set_desc(h, d):
    e = html.escape(d, quote=True)
    h = re.sub(r'(<meta content=")[^"]*(" name="description"/>)', lambda m: m.group(1) + e + m.group(2), h, count=1)
    h = re.sub(r'(<meta content=")[^"]*(" property="og:description"/>)', lambda m: m.group(1) + e + m.group(2), h, count=1)
    h = re.sub(r'(<meta content=")[^"]*(" name="twitter:description"/>)', lambda m: m.group(1) + e + m.group(2), h, count=1)
    return h


def main():
    n = {'desc': 0, 'box': 0, 'art': 0, 'files': 0}
    fam = re.compile(r'^/(wilayah/|jasa-audit-laporan-keuangan/|jasa-penyusunan-laporan-keuangan/|laporan-keuangan-[^/]+/|'
                     r'akuntan-terdekat/$|kap-dhn/$|kja-farhani/$)')
    for dp, _, fs in os.walk(ROOT):
        if 'index.html' not in fs:
            continue
        p = os.path.join(dp, 'index.html')
        u = url_of(p)
        art = u.strip('/').split('/')
        is_art = len(art) == 2 and art[0] == 'artikel' and (art[1] in ART_AUDIT or art[1] in ART_LK)
        if not fam.match(u) and not is_art:
            continue
        h0 = h = open(p, encoding='utf-8').read()
        if fam.match(u):
            city = city_of(u, h)
            if u.startswith('/wilayah/') and 'KJA Farhani, kredit bank.' in h:
                m = re.search(r'Cari akuntan atau kantor akuntan publik \(KAP\) di ([^?]+)\?', h)
                d = wil_desc(html.unescape(m.group(1))) if m else None
                if d:
                    h = set_desc(h, d); n['desc'] += 1
            if u.startswith('/wilayah/'):
                h2 = re.sub(r'(<meta content="[^"]*?)KAP DHN &amp; Rekan, KJA Farhani\.([^"]*" (?:name|property)="(?:og:|twitter:)?description"/>)',
                            r'\1Audit oleh KAP terdaftar OJK.\2', h)
                h2 = re.sub(r'(<meta content="[^"]*?), laporan keuangan oleh KJA Farhani([^"]*" (?:name|property)="(?:og:|twitter:)?description"/>)',
                            r'\1, penyusunan laporan keuangan\2', h2)
                if h2 != h:
                    h = h2; n['desc'] += 1
            h, ok = put(h, M1, M1E, lead_box(city), lambda s: s.find('<!--fa-tim-atas-->'))
            n['box'] += ok
        if is_art:
            kind = 'audit' if art[1] in ART_AUDIT else 'lk'
            t = re.search(r'<h1[^>]*>([^<]*)', h)
            title = html.unescape(t.group(1)) if t else ''

            def anchor(s):
                hs = [m.start() for m in re.finditer(r'<h2 id="', s)]
                return hs[1] if len(hs) >= 2 else (hs[0] if hs else -1)
            h, ok = put(h, M2, M2E, art_box(kind, title), anchor)
            n['art'] += ok
        if h != h0:
            n['files'] += 1
            if not DRY:
                open(p, 'w', encoding='utf-8').write(h)
    print(n)


if __name__ == '__main__':
    main()
