#!/usr/bin/env python3
"""CTR halaman daerah FA (14 Nov 2026). BEKERJA LANGSUNG DI out/faindonesia, idempoten, --dry.

Pemicu (Bos): "Push SEO lagi. Minggu ini gak ada klien. Konsultasi RS di daerah, audit di daerah,
penyusunan LK dan audit untuk lapor SABH di daerah." + "Halamannya sudah banyak, kurangi halaman baru."
Data GSC 90 hari (14 Nov): query "kap <kota>", "kantor akuntan publik <kota>", "audit <kota>" sudah
di posisi 3 sampai 10 (kap di padang 3,0; kap sidoarjo 6,4; kap cirebon 5,7; audit pontianak 7,4;
kantor akuntan publik terdekat 5,1) tapi 0 klik. Halaman yang muncul: /wilayah/<kota>/.
Jadi tanpa halaman baru: title dan description lima keluarga daerah ditulis ulang supaya cocok
dengan cara orang mencari (nama kota di depan, "KAP", "Jasa Audit", "SABH", "BPJS").

Yang diubah HANYA <title>, meta description, og:title/og:description, twitter:title/twitter:description.
H1, isi, URL, JSON-LD tidak disentuh. Title <= 60, description <= 158, kalimat utuh.
"""
import os, re, sys, glob, html, zlib

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv
TMAX, DMAX = 60, 158


def pick(cands, lim):
    for c in cands:
        if len(c) <= lim:
            return c
    return cands[-1]


def short(n):
    return re.sub(r'^Kabupaten ', 'Kab. ', n)


def var(slug, n):
    return zlib.crc32(slug.encode()) % n


FAM = {
    'wilayah': r'^Akuntan dan KAP (.+?)(?::| \||$)',
    'jasa-audit-laporan-keuangan': r'^Jasa Audit Laporan Keuangan (.+?)(?::| \||$)',
    'jasa-penyusunan-laporan-keuangan': r'^Jasa Penyusunan Laporan Keuangan (.+?)(?::| \||$)',
    'konsultan-rumah-sakit': r'^Konsultan Rumah Sakit (.+?)(?::| \||$)',
    'laporan-tahunan-pt': r'^Laporan Tahunan PT (?:SABH )?(.+?)(?::| \||$)',
}


def titles(fam, n, s):
    if fam == 'wilayah':
        return [f'KAP {n}: Kantor Akuntan Publik, Audit, SABH',
                f'KAP {n}: Audit Laporan Keuangan dan SABH',
                f'KAP {s}: Audit Laporan Keuangan dan SABH',
                f'KAP {s}: Audit dan Laporan Keuangan', f'KAP {s}']
    if fam == 'jasa-audit-laporan-keuangan':
        return [f'Jasa Audit Laporan Keuangan {n}: KAP OJK, Bank, SABH',
                f'Jasa Audit Laporan Keuangan {s}: KAP OJK, Bank, SABH',
                f'Jasa Audit Laporan Keuangan {s}: KAP Terdaftar OJK',
                f'Audit Laporan Keuangan {s}: KAP Terdaftar OJK',
                f'Audit Laporan Keuangan {s}: KAP OJK', f'Audit Laporan Keuangan {s}']
    if fam == 'jasa-penyusunan-laporan-keuangan':
        return [f'Jasa Laporan Keuangan {n}: Penyusunan untuk SABH dan Bank',
                f'Jasa Laporan Keuangan {s}: Penyusunan untuk SABH dan Bank',
                f'Jasa Laporan Keuangan {s}: untuk SABH dan Bank',
                f'Jasa Laporan Keuangan {s}: SABH, Bank',
                f'Laporan Keuangan {s}: SABH dan Bank', f'Jasa Laporan Keuangan {s}']
    if fam == 'konsultan-rumah-sakit':
        return [f'Konsultan Rumah Sakit {n}: Keuangan, BPJS, Kredit Bank',
                f'Konsultan Rumah Sakit {s}: Keuangan, BPJS, Kredit Bank',
                f'Konsultan Rumah Sakit {s}: Keuangan dan BPJS',
                f'Konsultan RS {s}: Keuangan dan BPJS', f'Konsultan Rumah Sakit {s}']
    if fam == 'laporan-tahunan-pt':
        return [f'Laporan Tahunan PT {n} untuk SABH: Siap Akta Notaris',
                f'Laporan Tahunan PT {s} untuk SABH: Siap Akta Notaris',
                f'Laporan Tahunan PT {s} untuk SABH', f'Laporan Tahunan PT {s}']


def descs(fam, n, prov, slug):
    loc = f'{n}, {prov}' if prov and prov not in n else n
    v = var(slug, 3)
    if fam == 'wilayah':
        c = [
            [f'Mencari KAP di {loc}? Audit laporan keuangan oleh KAP DHN & Rekan (terdaftar OJK) dan penyusunan laporan keuangan oleh KJA Farhani, untuk bank dan SABH.',
             f'Mencari KAP di {n}? Audit oleh KAP DHN & Rekan (terdaftar OJK) dan penyusunan laporan keuangan oleh KJA Farhani, untuk bank dan SABH.'],
            [f'Kantor akuntan publik untuk perusahaan di {loc}: audit oleh KAP DHN & Rekan (terdaftar OJK), laporan keuangan oleh KJA Farhani. Untuk bank, SABH, dan tender.',
             f'Kantor akuntan publik untuk perusahaan di {n}: audit oleh KAP DHN & Rekan (terdaftar OJK), laporan keuangan oleh KJA Farhani.'],
            [f'Perlu laporan keuangan audited di {loc}? KAP DHN & Rekan (terdaftar OJK) mengaudit, KJA Farhani menyusun laporan keuangan. Untuk kredit bank dan SABH.',
             f'Perlu laporan keuangan audited di {n}? KAP DHN & Rekan (terdaftar OJK) mengaudit, KJA Farhani menyusun laporan keuangan.'],
        ][v]
    elif fam == 'jasa-audit-laporan-keuangan':
        c = [
            [f'Audit laporan keuangan untuk perusahaan di {loc}: kredit bank, laporan tahunan PT di SABH, yayasan, dan tender. Oleh KAP DHN & Rekan, terdaftar OJK.',
             f'Audit laporan keuangan di {n}: kredit bank, laporan tahunan PT di SABH, yayasan, dan tender. Oleh KAP DHN & Rekan, terdaftar OJK.',
             f'Audit laporan keuangan di {n}: bank, SABH, yayasan, tender. Oleh KAP DHN & Rekan, terdaftar OJK.'],
            [f'Butuh laporan keuangan audited di {loc}? KAP DHN & Rekan (terdaftar OJK) mengaudit untuk kredit bank, laporan tahunan PT di SABH, dan yayasan.',
             f'Butuh laporan keuangan audited di {n}? KAP DHN & Rekan (terdaftar OJK) mengaudit untuk kredit bank, SABH, dan yayasan.',
             f'Laporan keuangan audited di {n} oleh KAP DHN & Rekan (terdaftar OJK): bank, SABH, yayasan.'],
            [f'Jasa audit di {loc} oleh KAP DHN & Rekan, terdaftar OJK: audit untuk kredit bank, laporan tahunan PT di SABH, koperasi, dan yayasan.',
             f'Jasa audit di {n} oleh KAP DHN & Rekan, terdaftar OJK: untuk kredit bank, laporan tahunan PT di SABH, dan yayasan.',
             f'Jasa audit di {n} oleh KAP DHN & Rekan, terdaftar OJK: bank, SABH, yayasan.'],
        ][v]
    elif fam == 'jasa-penyusunan-laporan-keuangan':
        c = [
            [f'Penyusunan laporan keuangan PT, CV, yayasan, dan UMKM di {loc} oleh KJA Farhani: siap untuk laporan tahunan SABH, kredit bank, pajak, dan audit.',
             f'Penyusunan laporan keuangan PT, CV, yayasan, dan UMKM di {n} oleh KJA Farhani: siap untuk SABH, kredit bank, pajak, dan audit.',
             f'Laporan keuangan PT, CV, dan yayasan di {n} oleh KJA Farhani: siap SABH, bank, dan audit.'],
            [f'Laporan keuangan untuk lapor SABH, kredit bank, dan pajak di {loc}. Disusun KJA Farhani sesuai SAK EMKM, SAK EP, atau PSAK, siap diaudit.',
             f'Laporan keuangan untuk lapor SABH, kredit bank, dan pajak di {n}. Disusun KJA Farhani sesuai SAK EMKM, SAK EP, atau PSAK.',
             f'Laporan keuangan untuk SABH, bank, dan pajak di {n}, disusun KJA Farhani.'],
            [f'Jasa laporan keuangan di {loc}: PT, CV, yayasan, dan UMKM, disusun KJA Farhani untuk SABH, bank, dan pajak. Bila wajib audit, diaudit KAP terpisah.',
             f'Jasa laporan keuangan di {n}: PT, CV, yayasan, dan UMKM, disusun KJA Farhani untuk SABH, bank, dan pajak.',
             f'Jasa laporan keuangan di {n} oleh KJA Farhani: untuk SABH, bank, dan pajak.'],
        ][v]
    elif fam == 'konsultan-rumah-sakit':
        c = [
            [f'Konsultan keuangan rumah sakit dan klinik di {loc}: klaim BPJS dan arus kas, unit cost dan tarif, kredit bank, sampai akuisisi. Tim pernah menjabat direktur RS.',
             f'Konsultan keuangan rumah sakit dan klinik di {n}: klaim BPJS dan arus kas, unit cost, kredit bank, sampai akuisisi.',
             f'Konsultan keuangan rumah sakit di {n}: BPJS, unit cost, kredit bank, akuisisi.'],
            [f'Rumah sakit di {loc} tertekan klaim BPJS atau butuh dana? Pendampingan unit cost, arus kas, kredit bank, dan investor oleh tim yang pernah memimpin RS.',
             f'Rumah sakit di {n} tertekan klaim BPJS atau butuh dana? Pendampingan unit cost, arus kas, kredit bank, dan investor.',
             f'RS di {n} butuh dana atau tertekan klaim BPJS? Pendampingan unit cost, arus kas, kredit bank.'],
            [f'Pendampingan rumah sakit swasta di {loc}: arus kas dan pending claim BPJS, unit cost, kredit bank, studi kelayakan, dan jual beli RS.',
             f'Pendampingan rumah sakit swasta di {n}: arus kas dan pending claim BPJS, unit cost, kredit bank, dan jual beli RS.',
             f'Pendampingan RS swasta di {n}: arus kas, klaim BPJS, unit cost, kredit bank.'],
        ][v]
    elif fam == 'laporan-tahunan-pt':
        c = [[f'Laporan tahunan PT di {loc} untuk SABH (Permenkum 49/2025): laporan keuangan oleh KJA Farhani, audit bila wajib oleh KAP DHN & Rekan, siap akta notaris.',
              f'Laporan tahunan PT di {n} untuk SABH (Permenkum 49/2025): laporan keuangan, audit bila wajib, siap akta notaris.',
              f'Laporan tahunan PT di {n} untuk SABH, siap akta notaris.']]
        c = c[0]
    return c


def setmeta(h, attr, key, val):
    pat = re.compile(r'<meta content="[^"]*" ' + attr + r'="' + re.escape(key) + r'"/>')
    if pat.search(h):
        return pat.sub(lambda m: f'<meta content="{val}" {attr}="{key}"/>', h, count=1)
    pat2 = re.compile(r'(<meta ' + attr + r'="' + re.escape(key) + r'" content=")[^"]*(")')
    return pat2.sub(lambda m: m.group(1) + val + m.group(2), h, count=1)


import json
PMAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fa_content', 'ctr_prov_20261114.json')
PROV = json.load(open(PMAP)) if os.path.exists(PMAP) else {}
changed = 0
for fam, rx in FAM.items():
    for f in sorted(glob.glob(os.path.join(ROOT, fam, '*', 'index.html'))):
        slug = f.split(os.sep)[-2]
        h = open(f, encoding='utf-8').read()
        rb = re.search(r'<meta[^>]*name="robots"[^>]*>', h)
        if rb and 'noindex' in rb.group(0):
            continue
        t0 = html.unescape(re.search(r'<title>(.*?)</title>', h, re.S).group(1))
        m = re.match(rx, t0)
        if not m:
            m = re.match(r'^(?:KAP|Jasa Audit Laporan Keuangan|Audit Laporan Keuangan|Jasa Laporan Keuangan|Laporan Keuangan|Konsultan Rumah Sakit|Konsultan RS|Laporan Tahunan PT) (.+?)(?: untuk SABH)?(?::| \||$)', t0)
        if not m:
            print('lewat', fam, slug, t0); continue
        n = m.group(1).replace('Kab. ', 'Kabupaten ').replace('(KAP) ', '')
        if n.endswith(' untuk SABH'):
            n = n[:-11]
        d0 = html.unescape(re.search(r'<meta content="([^"]*)" name="description"', h).group(1))
        pm = re.search(re.escape(n) + r', ([A-Z][A-Za-z .]+?)(?: oleh|:|\.)', d0)
        prov = pm.group(1).strip() if pm else ''
        if prov.startswith(('Kantor', 'KAP', 'Audit')):
            prov = ''
        key = fam + '/' + slug
        if key in PROV:
            prov = PROV[key]
        else:
            PROV[key] = prov
        T = pick(titles(fam, n, short(n)), TMAX)
        D = pick(descs(fam, n, prov, slug), DMAX)
        Te, De = html.escape(T, quote=True), html.escape(D, quote=True)
        h2 = re.sub(r'<title>.*?</title>', lambda _: f'<title>{Te}</title>', h, count=1, flags=re.S)
        h2 = setmeta(h2, 'name', 'description', De)
        for k in ('og:title',):
            h2 = setmeta(h2, 'property', k, Te)
        h2 = setmeta(h2, 'property', 'og:description', De)
        h2 = setmeta(h2, 'name', 'twitter:title', Te)
        h2 = setmeta(h2, 'name', 'twitter:description', De)
        if h2 != h:
            changed += 1
            if DRY and changed <= 12:
                print(fam, slug, '|', T, len(T), '|', D, len(D))
            if not DRY:
                open(f, 'w', encoding='utf-8').write(h2)
if not DRY:
    json.dump(PROV, open(PMAP, 'w'), ensure_ascii=False, indent=0, sort_keys=True)
print('berubah', changed)
