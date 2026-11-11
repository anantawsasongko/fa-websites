#!/usr/bin/env python3
"""Lead WA penyusunan LK dan audit KAP (9 Nov 2026). Revisi malam (Bos): FA = pintu kontak KJA Farhani dan KAP DHN di halaman LK/audit. BEKERJA LANGSUNG DI out/faindonesia, idempoten.
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
             'kap-dan-kja-mitra-fa-indonesia',
             # 11 Nov 2026 (fa_artikel_lead_20261111.py)
             'audit-laporan-keuangan-perusahaan-tambang-kontraktor-kalimantan', 'audit-laporan-keuangan-pt-pma-persiapan', 'audit-selesai-sebelum-akhir-tahun-target-realistis', 'cara-membaca-surat-penawaran-audit-kap', 'laporan-keuangan-audited-untuk-tender-migas-bumn']
ART_LK = ['biaya-jasa-penyusunan-laporan-keuangan', 'contoh-laporan-keuangan-umkm', 'laporan-keuangan-bankable-investor-ready',
          'laporan-keuangan-berantakan-cara-merapikan', 'laporan-keuangan-kontraktor-psak-115',
          'laporan-keuangan-rumah-sakit-swasta-sesuai-psak', 'laporan-keuangan-untuk-kredit-bank',
          'panduan-implementasi-psak-118', 'psak-119-entitas-anak-tanpa-akuntabilitas-publik',
          'aplikasi-laporan-keuangan-gratis-sesuai-sak-emkm-ep-psak', 'pertanyaan-komisaris-atas-laporan-keuangan',
          # 11 Nov 2026
          'keaslian-data-laporan-keuangan-untuk-bank', 'laporan-keuangan-bank-dan-pajak-harus-sejalan', 'laporan-keuangan-usaha-pariwisata-bali', 'menyusun-laporan-keuangan-dari-rekening-koran', 'pertanyaan-sebelum-menyusun-laporan-keuangan-pt']

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
    lk = wa(f'Halo Pak Ananta, saya{dari} perlu penyusunan laporan keuangan oleh KJA Farhani. Tahun buku: ... Jenis usaha: ...')
    au = wa(f'Halo Pak Ananta, saya{dari} perlu audit laporan keuangan oleh KAP DHN & Rekan. Keperluan: bank / SABH / tender / investor.')
    return (f'{M1}<div class="lk2" style="{BOX}"><b style="font-size:17px">Kontak KJA Farhani dan KAP DHN &amp; Rekan{di}</b>'
            f'<p style="margin:.3em 0 0;opacity:.85">FA Indonesia adalah pintu kontak untuk kedua kantor ini. Satu chat WhatsApp, '
            f'dijawab Ananta W. Sasongko, CPA, yang mendampingi sampai laporan selesai.</p>'
            f'<div style="{GRID}">'
            f'<div><b>Penyusunan Laporan Keuangan</b><p style="margin:.3em 0 .6em;opacity:.85">'
            f'Oleh KJA Farhani K.N. (Kantor Jasa Akuntansi berizin, Malang). Sesuai SAK EMKM, SAK EP, atau PSAK, siap dipakai bank dan auditor.</p>'
            f'<a class="btn solid" href="{lk}" rel="noopener" target="_blank">Tanya KJA Farhani</a></div>'
            f'<div><b>Audit Laporan Keuangan</b><p style="margin:.3em 0 .6em;opacity:.85">'
            f'Oleh KAP DHN &amp; Rekan, terdaftar OJK. Untuk kredit bank, laporan tahunan PT di SABH, tender, atau investor.</p>'
            f'<a class="btn solid" href="{au}" rel="noopener" target="_blank">Tanya KAP DHN &amp; Rekan</a></div>'
            f'</div><p style="margin:.7em 0 0;font-size:13px;opacity:.7">Untuk satu perusahaan, penyusun laporan keuangan dan auditornya selalu kantor yang berbeda.</p></div>{M1E}')


def art_box(kind, title):
    t = title.split(':')[0].strip()
    if kind == 'audit':
        head = 'Perusahaan Anda Perlu Audit KAP?'
        body = ('Audit dikerjakan KAP DHN &amp; Rekan (terdaftar OJK); FA Indonesia pintu kontaknya. Kirim tahun buku dan '
                'keperluannya (bank, SABH, tender, investor) lewat WhatsApp, dijawab Ananta W. Sasongko, CPA.')
        msg = f'Halo Pak Ananta, saya baca artikel "{t}". Perusahaan kami perlu audit laporan keuangan oleh KAP DHN & Rekan.'
        btn = 'Tanya KAP DHN &amp; Rekan'
    else:
        head = 'Laporan Keuangan Anda Belum Siap?'
        body = ('Laporan keuangan disusun KJA Farhani K.N. (Kantor Jasa Akuntansi berizin); FA Indonesia pintu kontaknya. '
                'Kirim jenis usaha dan tahun bukunya lewat WhatsApp, dijawab Ananta W. Sasongko, CPA.')
        msg = f'Halo Pak Ananta, saya baca artikel "{t}". Kami perlu penyusunan laporan keuangan oleh KJA Farhani.'
        btn = 'Tanya KJA Farhani'
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
    for d in (f'KAP dan akuntan di {city}: audit oleh KAP DHN & Rekan (terdaftar OJK), laporan keuangan oleh KJA Farhani. '
              f'Kontak lewat FA Indonesia via WhatsApp.',
              f'KAP dan akuntan di {city}: audit oleh KAP DHN & Rekan (terdaftar OJK), laporan keuangan oleh KJA Farhani.',
              f'KAP di {city}: audit oleh KAP DHN & Rekan, laporan keuangan oleh KJA Farhani.'):
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
            m = re.search(r'<meta content="(?:Cari akuntan atau kantor akuntan publik \(KAP\) di|Cari KAP atau akuntan di) ([^?]+)\?', h) if u.startswith('/wilayah/') else None
            if m:
                d = wil_desc(html.unescape(m.group(1))) if m else None
                if d:
                    h = set_desc(h, d); n['desc'] += 1
            if u.startswith('/wilayah/'):
                h2 = re.sub(r'(<meta content="[^"]*?)Audit oleh KAP terdaftar OJK\.([^"]*" (?:name|property)="(?:og:|twitter:)?description"/>)',
                            r'\1KAP DHN &amp; Rekan, KJA Farhani.\2', h)
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
