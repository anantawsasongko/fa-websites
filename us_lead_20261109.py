# UpdateSAK: edukasi lengkap + lead WA ke Ananta, CPA (9 Nov 2026, permintaan Bos).
# BEKERJA LANGSUNG DI out/updatesak (lihat PERINGATAN BUILD di README-DEPLOY.md). Idempoten.
# 1. Semua tombol WA ke nomor Bos: label "Tanya Ananta, CPA", pesan "Halo Pak Ananta, ..." menyebut topik halaman.
# 2. Kotak "Tanya Ananta, CPA" (penanda us-tanya) sebelum H2 kedua di halaman PSAK, SA, artikel, landing.
# 3. Halaman /psak/<n>/: bagian "Langkah Penerapan di Perusahaan" (data updatesak/psak_langkah_20261109.json), Peta Isi ikut.
# 4. Baris "Ditinjau Ananta W. Sasongko, CPA" di p.upd halaman edukasi.
# 5. Title: buang ekor ": Ringkasan dan Poin Kunci" / brand bila > 65. Description <= 158, kalimat utuh.
# 6. sitemap lastmod halaman yang berubah.
import os, re, json, html, sys, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'out', 'updatesak')
TODAY = '2026-11-09'; TGL = '9 November 2026'
WA = 'https://wa.me/6282245260121?text='
LANGKAH = json.load(open(os.path.join(ROOT, 'updatesak', 'psak_langkah_20261109.json'), encoding='utf-8'))
DRY = '--dry' in sys.argv
q = lambda t: urllib.parse.quote(t, safe='')

STYLE = ('<style id="us-tanya-css">.us-tanya{margin:28px 0;padding:20px 22px;border:1.5px solid #25D366;border-radius:8px;'
         'background:rgba(37,211,102,.06)}.us-tanya b.t{display:block;font-size:1.08rem;margin-bottom:4px}'
         '.us-tanya p{margin:0 0 12px;font-size:.95rem;line-height:1.55}.us-tanya .q{display:flex;flex-wrap:wrap;gap:8px}'
         '.us-tanya .q a{display:inline-block;padding:9px 14px;border-radius:8px;border:1px solid rgba(37,160,90,.55);'
         'text-decoration:none;font-size:.9rem;font-weight:600;color:inherit;background:#fff;line-height:1.35}'
         '.us-tanya .q a.w{background:#25D366;border-color:#25D366;color:#06301a}'
         '@media (max-width:720px){.us-tanya{padding:16px}.us-tanya .q a{width:100%;box-sizing:border-box}}</style>')

def topic_of(rel, h1):
    m = re.match(r'psak/(\d+)/', rel)
    if m: return 'PSAK ' + m.group(1)
    m = re.match(r'standar-audit/([a-z]+)-(\d+)/', rel)
    if m: return m.group(1).upper() + ' ' + m.group(2)
    t = re.sub(r'\s+', ' ', h1).strip()
    return t if len(t) <= 70 else t[:t.rfind(' ', 0, 67)]

def kind_of(rel):
    if re.match(r'psak/\d+/index\.html$', rel): return 'psak'
    if re.match(r'standar-audit/[^/]+/index\.html$', rel): return 'sa'
    if re.match(r'artikel/[^/]+/index\.html$', rel): return 'artikel'
    if re.match(r'(update-[a-z0-9-]+|penomoran-psak-baru)/index\.html$', rel): return 'landing'
    return 'other'

def chips(kind, tp):
    if kind == 'psak':
        return [(f'Apakah {tp} berlaku untuk perusahaan saya?', f'Halo Pak Ananta, saya baca {tp} di updatesak.com. Apakah {tp} berlaku untuk perusahaan kami? Usaha kami: '),
                (f'Contoh jurnal dan CALK {tp} untuk kasus saya', f'Halo Pak Ananta, kami perlu contoh jurnal dan CALK {tp} untuk kasus perusahaan kami. Kasusnya: '),
                (f'Persiapan {tp} sebelum diaudit KAP', f'Halo Pak Ananta, laporan keuangan kami akan diaudit KAP. Kami ingin siapkan penerapan {tp} dulu.')]
    if kind == 'sa':
        return [(f'Persiapan dokumen audit terkait {tp}', f'Halo Pak Ananta, perusahaan kami akan diaudit. Dokumen apa yang perlu disiapkan terkait {tp}?'),
                (f'Arti temuan auditor soal {tp}', f'Halo Pak Ananta, kami dapat temuan auditor terkait {tp}. Mau tanya artinya dan cara memperbaikinya.'),
                (f'Untuk KAP: kertas kerja {tp}', f'Halo Pak Ananta, saya dari KAP. Mau diskusi kertas kerja {tp}.')]
    return [('Tanya soal topik ini untuk usaha saya', f'Halo Pak Ananta, saya baca "{tp}" di updatesak.com. Mau tanya untuk usaha kami: '),
            ('Dibantu menerapkan di laporan keuangan', f'Halo Pak Ananta, kami ingin dibantu menerapkan "{tp}" di laporan keuangan perusahaan kami.')]

def box(kind, tp):
    lead = {'psak': f'Sedang menerapkan {tp} di laporan keuangan? Tanyakan kasus Anda ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.',
            'sa': f'Sedang diaudit atau menyiapkan audit terkait {tp}? Tanyakan ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.'}.get(
        kind, 'Ada kasus di perusahaan Anda yang mirip? Tanyakan ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.')
    a = ''.join(f'<a class="{"w" if i == 0 else ""}" href="{WA}{q(m)}" target="_blank" rel="noopener" data-us-q="{kind}">{html.escape(l)}</a>'
                for i, (l, m) in enumerate(chips(kind, tp)))
    return f'<!--us-tanya--><section class="us-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Ananta, CPA</b><p>{html.escape(lead)}</p><div class="q">{a}</div></section><!--/us-tanya-->'

def langkah(n):
    st = LANGKAH.get(str(n))
    if not st: return ''
    li = ''.join(f'<li>{html.escape(x)}</li>' for x in st)
    return (f'<!--us-langkah--><h2 id="langkah-penerapan">Langkah Penerapan di Perusahaan</h2>'
            f'<p>Urutan kerja yang biasa kami pakai saat menerapkan PSAK {n} di laporan keuangan klien, sebelum laporan diserahkan ke bank atau auditor.</p>'
            f'<ol class="us-steps">{li}</ol><!--/us-langkah-->')

def fit_desc(d, tail=''):
    d = re.sub(r'\s+', ' ', d).strip()
    sents = re.split(r'(?<=[.!?])\s+', d)
    out = ''
    for x in sents:
        cand = (out + ' ' + x).strip()
        if len(cand) <= 158: out = cand
        else: break
    if not out:
        # satu kalimat terlalu panjang: potong di koma atau titik dua terakhir, jangan di tengah frasa
        cut = d[:157]
        k = max(cut.rfind(', '), cut.rfind(': '))
        out = cut[:k].rstrip(',;: ') + '.' if k >= 70 else ''
        if not out: return d  # biarkan, lebih baik panjang daripada terpotong aneh
    if not re.search(r'[.!?]$', out): out += '.'
    return (out + tail) if tail and len(out + tail) <= 158 else out

TAIL = ' Ada kasusnya di perusahaan Anda? Tanya Ananta, CPA.'
def wrap_fix(s):
    # Perbaikan bug lama: </div> ganda setelah tabel .tx / lipatan pf-fold menutup .wrap terlalu awal,
    # sehingga sisa artikel nempel tepi kiri. Hapus penutup yang membuat kedalaman 0 sebelum akhir <article>,
    # lalu tutup sisanya tepat sebelum </article>.
    a = s.find('<article'); e = s.find('</article>')
    if a < 0 or e < 0: return s
    seg = s[a:e]
    while True:
        ms = list(re.finditer(r'<(/?)(div|section|aside|nav|details)\b', seg)); d = 0; cut = None
        for i, m in enumerate(ms):
            d += -1 if m.group(1) else 1
            if d <= 0 and i < len(ms) - 1 and m.group(1): cut = m; break
        if not cut: break
        end = seg.find('>', cut.start()) + 1
        seg = seg[:cut.start()] + seg[end:]
        seg = seg.rstrip()
        seg = seg + '</div>\n'  # tutup satu level sebelum </article>, menggantikan yang dihapus
    return s[:a] + seg + s[e:]

changed = []
for dp, dn, fn in os.walk(OUT):
    if 'index.html' not in fn: continue
    p = os.path.join(dp, 'index.html'); rel = os.path.relpath(p, OUT).replace(os.sep, '/')
    s0 = s = open(p, encoding='utf-8').read()
    if re.search(r'<meta(?=[^>]*name="robots")[^>]*noindex', s): continue
    kind = kind_of(rel)
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    h1 = html.unescape(re.sub('<[^>]+>', '', h1m.group(1))) if h1m else 'UpdateSAK'
    tp = topic_of(rel, h1) if rel != 'index.html' else 'PSAK dan SAK terbaru'

    s = wrap_fix(s)

    # 1. pesan dan label WA
    gen_old = q('Halo tim UpdateSAK, saya ingin diskusi penerapan SAK di perusahaan kami.')
    gen_new = q(f'Halo Pak Ananta, saya baca {tp} di updatesak.com. Mau tanya: ')
    s = s.replace(gen_old, gen_new)
    s = s.replace(q('Halo tim UpdateSAK, kami ingin dibantu menerapkan standar ini di laporan keuangan perusahaan kami.'),
                  q(f'Halo Pak Ananta, kami ingin dibantu menerapkan {tp} di laporan keuangan perusahaan kami.'))
    s = s.replace('Halo%20tim%20UpdateSAK%2C%20', 'Halo%20Pak%20Ananta%2C%20')
    s = re.sub(r'(<a\b[^>]*href="https://wa\.me/6282245260121[^"]*"[^>]*>)\s*(Chat Ananta, CPA|Chat WhatsApp|Konsultasi Gratis via WhatsApp)\s*</a>',
               r'\1Tanya Ananta, CPA</a>', s)
    s = s.replace('<p>Membaca standar itu satu hal, menerapkannya di laporan keuangan sampai lolos audit itu lain. Tim kami membantu dari jurnal penyesuaian, CALK, sampai pendampingan KAP.</p>',
                  '<p>Membaca standar itu satu hal, menerapkannya di laporan keuangan sampai lolos audit itu lain. Tanyakan dulu kasus Anda ke Ananta, CPA lewat WhatsApp, gratis. Bila perlu, kami bantu dari jurnal penyesuaian, CALK, sampai pendampingan KAP.</p>')

    s = s.replace('· Kantor Akuntan Publik Mitra, Terdaftar OJK', '· Kantor Akuntan Publik, Terdaftar OJK').replace('<small>Kantor Akuntan Publik Mitra</small>', '<small>Kantor Akuntan Publik</small>')

    # 3. langkah penerapan PSAK
    if kind == 'psak' and '<!--us-langkah-->' not in s:
        n = re.match(r'psak/(\d+)/', rel).group(1)
        blk = langkah(n)
        anchor = '<h2 id="yang-sering-dipersoalkan-auditor">'
        if blk and anchor in s:
            s = s.replace(anchor, blk + anchor, 1)
            s = s.replace('<li><a href="#yang-sering-dipersoalkan-auditor">',
                          '<li><a href="#langkah-penerapan">Langkah Penerapan di Perusahaan</a></li><li><a href="#yang-sering-dipersoalkan-auditor">', 1)

    # 2. kotak tanya sebelum H2 kedua (sesudah langkah penerapan untuk PSAK)
    if kind in ('psak', 'sa', 'artikel', 'landing') and '<!--us-tanya-->' not in s:
        main = s.find('<main'); endm = s.find('</main>')
        if kind == 'psak' and '<!--/us-langkah-->' in s:
            pos = s.find('<!--/us-langkah-->') + len('<!--/us-langkah-->')
        else:
            hs = [m.start() for m in re.finditer(r'<h2\b', s[main:endm])]
            pos = main + hs[1] if len(hs) >= 2 else (main + hs[0] if hs else -1)
        if pos > 0:
            s = s[:pos] + box(kind, tp) + s[pos:]
            if 'id="us-tanya-css"' not in s: s = s.replace('</head>', STYLE + '</head>', 1)

    # 4. ditinjau
    if kind in ('psak', 'sa', 'artikel', 'landing'):
        s = re.sub(r'(<p class="upd">)(?![^<]*Ditinjau)([^<]*)</p>', lambda m: m.group(1) + m.group(2).rstrip() + ' · Ditinjau Ananta W. Sasongko, CPA</p>', s, count=1)

    # 5. title dan description
    tm = re.search(r'<title>(.*?)</title>', s, re.S)
    if tm:
        t = tm.group(1); t2 = t
        if rel == 'jadwal-ujian/index.html': t2 = 'Jadwal Ujian CPA, CA, CPMA, dan Konsultan Pajak 2026 | UpdateSAK'
        if len(html.unescape(t2)) > 65: t2 = t2.replace(': Ringkasan dan Poin Kunci', '').replace(': Ringkasan dan Fokus Auditor', '')
        if len(html.unescape(t2)) > 65: t2 = t2.replace(' | UpdateSAK', '')
        if t2 != t:
            s = s.replace(tm.group(0), f'<title>{t2}</title>', 1)
            s = re.sub(r'(<meta content=")[^"]*(" property="og:title"/?>)', lambda m: m.group(1) + t2.replace(' | UpdateSAK', '') + m.group(2), s, count=1)
    dm = re.search(r'<meta content="([^"]*)" name="description"\s*/?>', s)
    if dm:
        d = html.unescape(dm.group(1))
        tail = TAIL if kind in ('psak', 'sa') else ''
        if rel == 'jadwal-ujian/index.html':
            nd = 'Jadwal ujian CPA IAPI, CA IAI, CPMA IAMI, dan USKP 2026, lengkap dengan materi belajar gratis per mata ujian. Diperbarui berkala.'
        elif rel == 'index.html':
            nd = 'Cek PSAK, SAK EP, SAK EMKM, atau SAK Syariah yang berlaku dari neraca dan laba rugi, lalu susun draf CALK format auditor. Gratis, langsung di browser.'
        elif tail and 'Ananta' not in d and len(d) + len(tail) <= 158:
            nd = d.rstrip() + tail
        elif len(d) > 158:
            nd = fit_desc(d, tail if tail and 'Ananta' not in d else '')
        else:
            nd = d
        if nd != d:
            e = html.escape(nd, quote=True)
            s = s.replace(dm.group(0), f'<meta content="{e}" name="description"/>', 1)
            s = re.sub(r'<meta content="[^"]*" property="og:description"\s*/?>', f'<meta content="{e}" property="og:description"/>', s, count=1)

    if s != s0:
        if kind in ('psak', 'sa', 'artikel', 'landing'):
            s = s.replace('"dateModified": "2026-10-27"', f'"dateModified": "{TODAY}"')
        changed.append(rel)
        if not DRY: open(p, 'w', encoding='utf-8').write(s)

# 6. sitemap lastmod
smp = os.path.join(OUT, 'sitemap.xml'); sm = open(smp, encoding='utf-8').read(); sm0 = sm
for rel in changed:
    u = 'https://updatesak.com/' + rel[:-len('index.html')]
    sm = re.sub(r'(<loc>' + re.escape(u) + r'</loc><lastmod>)[^<]+', r'\g<1>' + TODAY, sm)
if sm != sm0 and not DRY: open(smp, 'w', encoding='utf-8').write(sm)
print('changed', len(changed), 'dry' if DRY else '')
