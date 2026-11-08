#!/usr/bin/env python3
"""SEO teknis rapi (8 Nov 2026). BEKERJA LANGSUNG DI out/faindonesia, idempoten.
Jalankan SETELAH prep.py dan script out/ lain, SEBELUM fa_langsung_20261108.py tidak masalah
(fa_langsung tidak menyentuh title/description).

Isi:
1. Title <= 60 karakter (artikel <= 65): buang item subjudul dari belakang, lalu brand, lalu subjudul.
   og:title dan twitter:title ikut.
2. Meta description <= 158 karakter, tidak terpotong di tengah kalimat. Halaman wilayah yang
   terpotong ("...: pemilihan vendor, rekam.") ditulis ulang dengan pola per layanan.
3. Entri Peta Isi (href="#id") yang id-nya tidak ada dihapus.
4. Sisa frasa makelar (KAP mitra, KJA mitra, mitra kami) diganti kalimat langsung.
5. /toko/uji/ noindex. Halaman indexable yang belum ada di sitemap ditambahkan; lastmod halaman
   yang berubah jadi tanggal hari ini.
6. img tanpa alt diberi alt dari konteks.
"""
import os, re, sys, html, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DOMAIN = 'https://faindonesia.co.id'
TODAY = '2026-11-08'
DRY = '--dry' in sys.argv
BRAND = ' | FA Indonesia'


def url_of(p):
    r = os.path.relpath(p, ROOT).replace(os.sep, '/')
    if r == 'index.html':
        return '/'
    if r.endswith('/index.html'):
        return '/' + r[:-10]
    return '/' + r


def esc(s):
    return html.escape(s, quote=True)


# ---------- 1. title ----------
def is_template(u):
    parts = u.strip('/').split('/')
    return len(parts) >= 2 and parts[0] not in ('artikel', 'en', 'zh', 'ja', 'saturn', 'toko', 'galaxy', 'buku')


def short_title(t, limit, template=True):
    if len(t) <= limit:
        return t
    brand = t.endswith(BRAND)
    core = t[:-len(BRAND)] if brand else t
    if not template:
        # halaman unik: cukup buang brand bila itu menolong (Google menampilkan nama situs terpisah)
        return core if brand and len(core) <= limit + 5 else t
    segs = core.split(' | ')
    primary_full, extra = segs[0], segs[1:]
    primary, sub = (primary_full.split(': ', 1) + [''])[:2] if ': ' in primary_full else (primary_full, '')
    items = [x.strip() for x in sub.split(', ') if x.strip()] if sub else []
    B = BRAND if brand else ''
    cands = []
    if items:
        cands.append(f'{primary}: {", ".join(items)}{B}')
        for k in range(len(items), 1, -1):
            cands.append(f'{primary}: {", ".join(items[:k])}')
    for e in extra:
        cands.append(f'{primary} | {e}')
    cands.append(f'{primary}{B}')
    if items:
        cands.append(f'{primary}: {items[0]}')
    cands.append(primary)
    for c in cands:
        if len(c) <= limit:
            return c
    return primary


# ---------- 2. description ----------
LEAD = {
    'konsultan-simrs': ('Konsultan SIMRS untuk rumah sakit dan klinik',
                        ['pilih vendor, RME, integrasi SATUSEHAT dan BPJS, biaya terkendali.',
                         'pilih vendor, RME, SATUSEHAT, dan BPJS.']),
    'konsultan-farmasi-rumah-sakit': ('Optimalisasi farmasi rumah sakit dan klinik',
                        ['stok, formularium, margin obat, dan kas yang tidak terkunci.',
                         'stok, formularium, dan margin obat.']),
    'jasa-penyusunan-laporan-keuangan': ('Jasa penyusunan laporan keuangan',
                        ['PT, CV, dan UMKM, siap untuk bank, pajak, dan audit.',
                         'PT, CV, UMKM, siap bank dan audit.']),
    'konsultan-klinik-bpjs': ('Konsultan klinik BPJS',
                        ['kapitasi, KBK, rujukan, dan kerja sama BPJS yang sehat.',
                         'kapitasi, KBK, dan rujukan.']),
}
RX_KEC = re.compile(r'^(?P<lead>.*?) di (?P<w>.+?), (?P<prov>[^()]+?) \((?P<n>\d+) kecamatan, termasuk (?P<names>[^)]*)\)?')
TAILS2 = {
    'konsultan-rumah-sakit': ['Ekspansi, kredit bank, jual beli RS, dan unit cost.', 'Ekspansi, kredit bank, jual beli RS.', 'Keuangan, M&A, unit cost.'],
    'konsultan-klinik': ['Studi kelayakan, kapitasi BPJS, unit cost, dan laporan keuangan.', 'Studi kelayakan, kapitasi BPJS, unit cost.', 'Kelayakan, BPJS, unit cost.'],
}
FAM = {
    'konsultan-akreditasi-rumah-sakit': ('Konsultan akreditasi rumah sakit', [
        'gap assessment, dokumen regulasi, simulasi telusur, indikator mutu, dan anggaran persiapan.',
        'gap assessment, dokumen regulasi, simulasi telusur, dan anggaran.',
        'gap assessment, dokumen, dan simulasi telusur.']),
    'konsultan-bpjs-rumah-sakit': ('Konsultan BPJS rumah sakit', [
        'klaim pending dan dispute, margin per kasus INA-CBG/iDRG, piutang BPJS, dan arus kas.',
        'klaim pending, margin INA-CBG/iDRG, dan arus kas.',
        'klaim pending dan arus kas.']),
    'konsultan-unit-cost-rumah-sakit': ('Konsultan unit cost rumah sakit dan klinik', [
        'rawat inap, rawat jalan, tindakan, penunjang, margin INA-CBG/iDRG, dan rekomendasi tarif.',
        'rawat inap, rawat jalan, tindakan, margin INA-CBG/iDRG, dan tarif.',
        'unit cost per layanan dan tarif.']),
}
RX_GEN = re.compile(r'^(?:.+?) (?:di|untuk) (?P<w>[A-Z].+?)(?:, (?P<prov>[^:(]+?))?(?: \([^)]*\))?: ')
RX_KL = re.compile(r'^(?P<lead>.+?) di (?P<w>.+?), (?P<prov>[^:]+): (?P<names>.*?), dan kecamatan lain\. ?')
RX_AUDIT = re.compile(r'^Audit laporan keuangan di (?P<w>.+?), (?P<prov>[^:]+): (?P<names>.*?), dan kecamatan lain\.')
LIMIT_D = 158


STOP = {'dan', 'yang', 'untuk', 'di', 'ke', 'dari', 'serta', 'atau', 'dengan', 'oleh', 'siap', 'sampai', 'hingga', 'the', 'and', 'for', 'of', 'Big'}


def bounds(d):
    out = []
    for i, ch in enumerate(d):
        if ch in '.!?' and (i + 1 == len(d) or d[i + 1] == ' '):
            w = d[:i].split(' ')[-1]
            if len(w) >= 3 and '.' not in w:
                out.append(i + 1)
    return out


def fit_sentences(d):
    d = re.sub(r'\s+', ' ', d).strip()
    last = d.rstrip('.!?').split(' ')[-1] if d else ''
    if len(d) <= LIMIT_D and d[-1:] in '.!?)' and last not in STOP:
        return d
    if len(d) <= LIMIT_D and last in STOP:
        words = d.rstrip('.').split(' ')
        while words and words[-1] in STOP:
            words.pop()
        return ' '.join(words).rstrip(',;:-') + '.'
    ok = [i for i in bounds(d) if i <= LIMIT_D]
    if ok and ok[-1] >= 100:
        return d[:ok[-1]].strip()
    cut = d[:LIMIT_D]
    c = cut.rfind(', ')
    if c >= 100:
        cut = cut[:c]
    else:
        cut = cut[:cut.rfind(' ')]
    words = cut.rstrip(',;:- ').split(' ')
    while words and words[-1] in STOP:
        words.pop()
    return ' '.join(words).rstrip(',;:-') + '.'


def new_desc(u, d):
    for a in ('Sekolah', 'Restoran', 'Apotek', 'Distributor'):
        d = d.replace(' dan ' + a + ' di ', ' dan ' + a.lower() + ' di ')
    seg = u.strip('/').split('/')[0] if u != '/' else ''
    depth = len(u.strip('/').split('/'))
    m = RX_KEC.match(d)
    if seg in LEAD and m and depth == 2:
        lead, tails = LEAD[seg]
        nm = m.group('names').split(', ')
        first = nm[0] if len(nm) > 1 else ''
        for tail in tails:
            for withn in (True, False):
                s = f"{lead} di {m.group('w')}, {m.group('prov')}: {tail}"
                if withn and first:
                    s += f" Mencakup {m.group('n')} kecamatan, termasuk {first}."
                if len(s) <= LIMIT_D:
                    return s
    m = RX_GEN.match(d)
    if seg in FAM and m and depth == 2:
        lead, tails = FAM[seg]
        loc = m.group('w') + (', ' + m.group('prov') if m.group('prov') else '')
        for tail in tails:
            for x in (loc, m.group('w')):
                s = f'{lead} di {x}: {tail}'
                if len(s) <= LIMIT_D:
                    return s
    m = RX_KL.match(d)
    if seg in TAILS2 and m and depth == 2:
        names = m.group('names').split(', ')
        for tail in TAILS2[seg]:
            for k in (3, 2, 1, 0):
                if k:
                    s = f"{m.group('lead')} di {m.group('w')}, {m.group('prov')}: {', '.join(names[:k])}, dan kecamatan lain. {tail}"
                else:
                    s = f"{m.group('lead')} di {m.group('w')}, {m.group('prov')}. {tail}"
                if len(s) <= LIMIT_D:
                    return s
    m = RX_GEN.match(d)
    if seg == 'konsultan-klinik' and m and depth == 2:
        loc = m.group('w') + (', ' + m.group('prov') if m.group('prov') else '')
        for tail in ('studi kelayakan, kapitasi BPJS, unit cost dan tarif, laporan keuangan, dan kredit bank.',
                     'studi kelayakan, kapitasi BPJS, unit cost, dan laporan keuangan.'):
            s = f'Konsultan klinik di {loc}: {tail}'
            if len(s) <= LIMIT_D:
                return s
    m = RX_AUDIT.match(d)
    if seg == 'jasa-audit-laporan-keuangan' and m:
        w, prov = m.group('w'), m.group('prov')
        for s in (f'Audit laporan keuangan di {w}, {prov} oleh KAP terdaftar OJK: untuk kredit bank, laporan tahunan PT, koperasi, dan yayasan.',
                  f'Audit laporan keuangan di {w}, {prov} oleh KAP terdaftar OJK: kredit bank, PT, koperasi, yayasan.',
                  f'Audit laporan keuangan di {w} oleh KAP terdaftar OJK: kredit bank, PT, koperasi, yayasan.'):
            if len(s) <= LIMIT_D:
                return s
    # deskripsi terpotong satu kata setelah titik dua: "...): pemilihan."
    if re.search(r'\): \S+( \S+)?\.$', d):
        d = d[:d.rfind('): ') + 1] + '.'
    out = fit_sentences(d)
    if ', dan wilayah.' in out:
        o2 = out.replace(', dan wilayah.', ', dan wilayah lain.')
        out = o2 if len(o2) <= LIMIT_D else out.replace(', dan wilayah.', '.')
    return out


# ---------- 4. frasa makelar ----------
PLAIN = [
    ('Bila laporan keuangan belum siap, KJA mitra merapikannya lebih dulu', 'Bila laporan keuangan belum siap, kami rapikan lebih dulu'),
    ('yang disusun FA Indonesia atau KJA mitra', 'yang disusun FA Indonesia sendiri'),
    ('atas laporan yang disusun FA atau KJA mitra', 'atas laporan yang disusun FA sendiri'),
    ('dan audit oleh KAP mitra', 'dan audit oleh KAP DHN &amp; Rekan'),
    ('lalu KAP mitra mengaudit', 'lalu KAP DHN &amp; Rekan mengaudit'),
    ('Audit laporan keuangan oleh KAP mitra;', 'Audit laporan keuangan oleh KAP terdaftar OJK;'),
    ('bersama konsultan pajak berizin mitra kami', 'bersama konsultan pajak berizin'),
    ('dengan FA Consult dan KAP mitra', 'dengan FA Consult dan KAP DHN &amp; Rekan'),
]
SKIP_MAKELAR = ('/mitra-kap-kja/',)  # menunggu keputusan Bos


def fix_toc(s):
    ids = set(re.findall(r'\sid="([^"]+)"', s))
    def rep(m):
        return '' if m.group(1) not in ids else m.group(0)
    return re.sub(r'<li><a href="#([^"]+)">[^<]*</a></li>', rep, s)


def set_meta(head, attr, key, val):
    """ganti content meta (urutan atribut bebas)."""
    def rep(m):
        tg = m.group(0)
        if re.search(r'%s="%s"' % (attr, re.escape(key)), tg):
            return re.sub(r'content="[^"]*"', 'content="%s"' % esc(val).replace('&#x27;', "'"), tg, count=1)
        return tg
    return re.sub(r'<meta\b[^>]*>', rep, head)


def get_meta(head, attr, key):
    for m in re.finditer(r'<meta\b[^>]*>', head):
        tg = m.group(0)
        if re.search(r'%s="%s"' % (attr, re.escape(key)), tg):
            c = re.search(r'content="([^"]*)"', tg)
            return html.unescape(c.group(1)) if c else ''
    return None


def main():
    files = []
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.join(d, f))
    changed = []
    stat = dict(title=0, desc=0, toc=0, makelar=0, alt=0, noindex=0)
    indexable = []
    for p in files:
        u = url_of(p)
        s0 = s = open(p, encoding='utf-8').read()
        if '</head>' not in s:
            continue
        head, body = s.split('</head>', 1)
        h0 = head
        # 5. noindex halaman uji
        if u == '/toko/uji/':
            head = set_meta(head, 'name', 'robots', 'noindex,follow')
        robots = get_meta(head, 'name', 'robots') or ''
        noindex = 'noindex' in robots
        # 1. title
        tm = re.search(r'<title>(.*?)</title>', head, re.S)
        if tm and not noindex:
            t = html.unescape(tm.group(1).strip())
            lim = 65 if u.startswith('/artikel/') else 60
            if 'Provinsi ' in t and '/provinsi-' in u:
                lim += 9
            nt = short_title(t, lim, is_template(u))
            if len(nt) > lim and ' Rumah Sakit & Klinik ' in nt:
                nt = short_title(nt.replace(' Rumah Sakit & Klinik ', ' Rumah Sakit '), lim, is_template(u))
            if nt != t:
                head = head.replace(tm.group(0), '<title>%s</title>' % html.escape(nt, quote=False), 1)
                for k in ('og:title',):
                    if get_meta(head, 'property', k) == t:
                        head = set_meta(head, 'property', k, nt)
                if get_meta(head, 'name', 'twitter:title') == t:
                    head = set_meta(head, 'name', 'twitter:title', nt)
                stat['title'] += 1
        # 2. description
        d = get_meta(head, 'name', 'description')
        if d and not noindex:
            nd = new_desc(u, d)
            if nd != d:
                head = set_meta(head, 'name', 'description', nd)
                for k in ('og:description',):
                    if get_meta(head, 'property', k) == d:
                        head = set_meta(head, 'property', k, nd)
                if get_meta(head, 'name', 'twitter:description') == d:
                    head = set_meta(head, 'name', 'twitter:description', nd)
                stat['desc'] += 1
        # 7. halaman provinsi bernama sama dengan kota: tegaskan "Provinsi"
        pm = re.search(r'/provinsi-([a-z-]+)/$', u)
        if pm and not noindex:
            nm = ' '.join(w.capitalize() for w in pm.group(1).split('-'))
            city = os.path.join(ROOT, u.strip('/').split('/')[0], pm.group(1), 'index.html')
            if os.path.exists(city):
                tm = re.search(r'<title>(.*?)</title>', head, re.S)
                t = html.unescape(tm.group(1))
                if 'Provinsi' not in t and nm in t:
                    i = t.rfind(nm); nt = t[:i] + 'Provinsi ' + t[i:]
                    head = head.replace(tm.group(0), '<title>%s</title>' % html.escape(nt, quote=False), 1)
                    for k in ('og:title',):
                        if get_meta(head, 'property', k) == t:
                            head = set_meta(head, 'property', k, nt)
                    stat['title'] += 1
                d = get_meta(head, 'name', 'description') or ''
                if 'Provinsi' not in d and (' di %s' % nm) in d:
                    nd = d.replace(' di %s' % nm, ' di Provinsi %s' % nm, 1)
                    if len(nd) <= LIMIT_D:
                        head = set_meta(head, 'name', 'description', nd)
                        if get_meta(head, 'property', 'og:description') == d:
                            head = set_meta(head, 'property', 'og:description', nd)
                        stat['desc'] += 1
        s = head + '</head>' + body
        # 3. toc
        s2 = fix_toc(s)
        if s2 != s:
            stat['toc'] += 1
            s = s2
        # 4. makelar
        if u not in SKIP_MAKELAR:
            s2 = s
            for a, b in PLAIN:
                s2 = s2.replace(a, b)
                s2 = s2.replace(a.replace('&amp;', '&'), b.replace('&amp;', '&'))
            if s2 != s:
                stat['makelar'] += 1
                s = s2
        # 6. alt kosong
        def altfix(m):
            tg = m.group(0)
            if re.search(r'\balt="[^"]+', tg):
                return tg
            src = re.search(r'src="([^"]*)"', tg)
            name = os.path.splitext(os.path.basename(src.group(1)))[0] if src else 'gambar'
            alt = re.sub(r'[-_]+', ' ', name).strip() or 'FA Indonesia'
            if 'logo' in name or name.startswith('wm-'):
                alt = 'Logo FA Indonesia'
            stat['alt'] += 1
            tg = re.sub(r'\salt=""', '', tg)
            return tg[:-1].rstrip('/').rstrip() + ' alt="%s"' % esc(alt) + ('/>' if tg.endswith('/>') else '>')
        s = re.sub(r'<img\b(?![^>]*\+)[^>]*>', altfix, s)
        if not noindex and not u.endswith('.html'):
            indexable.append(u)
        if s != s0:
            changed.append(u)
            if not DRY:
                open(p, 'w', encoding='utf-8').write(s)
    # 5. sitemap
    smp = os.path.join(ROOT, 'sitemap.xml')
    sm = open(smp, encoding='utf-8').read()
    locs = set(re.findall(r'<loc>%s(/[^<]*)</loc>' % re.escape(DOMAIN), sm))
    add = [u for u in indexable if u not in locs]
    sm2 = sm
    if '/toko/uji/' in locs:
        sm2 = re.sub(r'<url><loc>%s/toko/uji/</loc>.*?</url>\n?' % re.escape(DOMAIN), '', sm2, flags=re.S)
    chg = set(changed)
    def lm(m):
        if m.group(1) in chg:
            return re.sub(r'<lastmod>[^<]*</lastmod>', '<lastmod>%s</lastmod>' % TODAY, m.group(0))
        return m.group(0)
    sm2 = re.sub(r'<url><loc>%s(/[^<]*)</loc>.*?</url>' % re.escape(DOMAIN), lm, sm2, flags=re.S)
    if add:
        block = ''.join('<url><loc>%s%s</loc><lastmod>%s</lastmod><priority>0.6</priority></url>\n' % (DOMAIN, u, TODAY) for u in sorted(add))
        sm2 = sm2.replace('</urlset>', '<!--seorapi-->\n' + block + '</urlset>')
    if sm2 != sm and not DRY:
        open(smp, 'w', encoding='utf-8').write(sm2)
    print(stat, 'files', len(changed), 'sitemap+', len(add))


if __name__ == '__main__':
    main()
