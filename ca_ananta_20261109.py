# CariAkuntan: semua pertanyaan diarahkan ke Ananta, CPA (9 Nov 2026, permintaan Bos).
# BEKERJA LANGSUNG DI out/cariakuntan (lihat PERINGATAN BUILD di README-DEPLOY.md). Idempoten.
# 1. Tombol WA ke nomor Bos: label "Tanya Ananta, CPA", pesan header/bar menyebut topik halaman.
# 2. Kotak "Tanya Dulu ke Ananta, CPA" (penanda ca-tanya) di bawah tombol hero halaman kota/kawasan/layanan/KDMP,
#    dan sebelum H2 kedua di artikel. Tombol pertanyaan berisi pesan WA siap kirim (kota + kebutuhan).
# 3. Description halaman kota/kawasan/KDMP ditulis ulang (<= 158, kalimat utuh, ajakan tanya Ananta, CPA);
#    description lain > 158 dipendekkan di batas kalimat. Title > 65: buang " | cariakuntan.com".
# 4. FAQ ganda (h3 + p kembar berurutan) dihapus. "minta kami carikan" dan label "Mitra" di strip KAP dirapikan.
# 5. /kdmp/<prov>/<kab>/ (514 halaman tipis): blok panduan singkat + FAQ + kotak tanya.
# 6. /cek-izin/: canonical dan description sendiri. sitemap lastmod halaman yang berubah.
import os, re, html, sys, json, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'out', 'cariakuntan')
TODAY = '2026-11-09'
WA = 'https://wa.me/6282245260121?text='
DRY = '--dry' in sys.argv
q = lambda t: urllib.parse.quote(t, safe='')
E = lambda t: html.escape(t, quote=True)
SVC = ('kap', 'kjpp', 'kja', 'konsultan-pajak', 'jasa-laporan-keuangan', 'laporan-tahunan-pt', 'kap-murah', 'akuntan-forensik')

STYLE = ('<style id="ca-tanya-css">.ca-tanya{margin:22px 0 6px;padding:18px 20px;border:1.5px solid #25D366;border-radius:8px;'
         'background:rgba(37,211,102,.06)}.ca-tanya b.t{display:block;font-size:1.05rem;margin-bottom:4px}'
         '.ca-tanya p{margin:0 0 12px;font-size:.94rem;line-height:1.55}.ca-tanya .q{display:flex;flex-wrap:wrap;gap:8px}'
         '.ca-tanya .q a{display:inline-block;padding:9px 14px;border-radius:8px;border:1px solid rgba(37,160,90,.55);'
         'text-decoration:none;font-size:.9rem;font-weight:600;color:inherit;background:#fff;line-height:1.35}'
         '.ca-tanya .q a.w{background:#25D366;border-color:#25D366;color:#06301a}'
         '@media (max-width:720px){.ca-tanya{padding:16px}.ca-tanya .q a{width:100%;box-sizing:border-box}}</style>')

def label(p):
    try: s = open(p, encoding='utf-8').read()
    except (FileNotFoundError, NotADirectoryError): return None
    m = re.search(r'<p class="label"[^>]*>([^<]+)</p>', s)
    return html.unescape(m.group(1)).strip() if m else None

# peta nama tempat dari label halaman /kap/
PLACE = {}
for c in os.listdir(os.path.join(OUT, 'kota')):
    d = os.path.join(OUT, 'kota', c)
    if not os.path.isdir(d): continue
    lb = label(os.path.join(d, 'kap', 'index.html'))
    if lb and ',' in lb: PLACE[c] = tuple(x.strip() for x in lb.split(',', 1))
    for k in os.listdir(d):
        lk = label(os.path.join(d, k, 'kap', 'index.html'))
        if k not in SVC and lk and ',' in lk: PLACE[c + '/' + k] = tuple(x.strip() for x in lk.split(',', 1))

def chips_for(svc, X):
    T = {
     'kap': [(f'Apakah usaha saya wajib audit?', f'Halo Pak Ananta, kami dari {X}. Apakah usaha kami wajib diaudit KAP? Usaha kami: '),
             (f'Berapa kisaran biaya audit di {X}?', f'Halo Pak Ananta, kami dari {X}. Berapa kisaran biaya audit KAP untuk usaha kami? Total aset sekitar: '),
             ('KAP yang diterima bank saya', f'Halo Pak Ananta, kami dari {X}. Bank meminta laporan audit KAP. Bank kami: ')],
     'kap-murah': [(f'Berapa biaya audit usaha saya?', f'Halo Pak Ananta, kami dari {X}. Berapa kisaran biaya audit untuk usaha kami? Total aset sekitar: '),
                   ('Cara hemat tanpa audit ulang', f'Halo Pak Ananta, kami dari {X}. Mau tanya cara hemat biaya audit supaya tidak perlu audit ulang.'),
                   ('Audit murah tapi diterima bank', f'Halo Pak Ananta, kami dari {X}. Butuh audit dengan biaya wajar yang tetap diterima bank.')],
     'kjpp': [('Perlu KJPP untuk agunan kredit?', f'Halo Pak Ananta, kami dari {X}. Apakah kami perlu penilaian KJPP untuk agunan kredit bank?'),
              (f'Biaya appraisal di {X}', f'Halo Pak Ananta, kami dari {X}. Berapa kisaran biaya appraisal KJPP? Objeknya: '),
              ('Valuasi usaha untuk investor', f'Halo Pak Ananta, kami dari {X}. Kami butuh valuasi usaha untuk investor atau jual beli saham.')],
     'konsultan-pajak': [('SPT badan dan Coretax', f'Halo Pak Ananta, kami dari {X}. Mau tanya soal SPT badan dan Coretax.'),
                         ('Dapat SP2DK atau pemeriksaan', f'Halo Pak Ananta, kami dari {X}. Kami menerima SP2DK atau surat pemeriksaan pajak. Mau tanya langkahnya.'),
                         ('Biaya konsultan pajak', f'Halo Pak Ananta, kami dari {X}. Berapa kisaran biaya pendampingan pajak untuk usaha kami?')],
     'akuntan-forensik': [('Hitung kerugian penggelapan', f'Halo Pak Ananta, kami dari {X}. Kami perlu penghitungan kerugian penggelapan untuk laporan polisi.'),
                          ('Langkah sebelum lapor polisi', f'Halo Pak Ananta, kami dari {X}. Mau tanya langkah dan dokumen sebelum lapor polisi soal penipuan atau penggelapan.')],
     'lk': [('Laporan keuangan untuk bank', f'Halo Pak Ananta, kami dari {X}. Kami butuh laporan keuangan untuk pengajuan kredit bank.'),
            ('Berapa biaya penyusunan LK?', f'Halo Pak Ananta, kami dari {X}. Berapa kisaran biaya penyusunan laporan keuangan untuk usaha kami?'),
            ('Laporan tahunan PT untuk notaris', f'Halo Pak Ananta, kami dari {X}. Kami perlu laporan tahunan PT untuk notaris dan SABH.')],
     'hub': [('Perlu KAP atau cukup KJA?', f'Halo Pak Ananta, kami dari {X}. Kami bingung perlu audit KAP atau cukup laporan dari KJA. Keperluannya untuk: '),
             ('Laporan keuangan untuk kredit bank', f'Halo Pak Ananta, kami dari {X}. Kami butuh laporan keuangan untuk kredit bank.'),
             ('Urusan pajak usaha', f'Halo Pak Ananta, kami dari {X}. Mau tanya urusan pajak usaha kami.')],
     'kdmp': [('Laporan keuangan untuk RAT', f'Halo Pak Ananta, kami pengurus Koperasi Desa Merah Putih di {X}. Kami perlu laporan keuangan untuk RAT.'),
              ('Pembukuan bulanan koperasi', f'Halo Pak Ananta, kami pengurus Koperasi Desa Merah Putih di {X}. Kami perlu dibantu pembukuan bulanan.'),
              ('Audit Kopdes Merah Putih', f'Halo Pak Ananta, kami pengurus Koperasi Desa Merah Putih di {X}. Mau tanya soal audit koperasi.')],
    }
    k = svc if svc in T else ('lk' if svc in ('kja', 'jasa-laporan-keuangan', 'laporan-tahunan-pt') else 'hub')
    return T[k]

def box(chips, lead, kind):
    a = ''.join(f'<a class="{"w" if i == 0 else ""}" href="{WA}{q(m)}" target="_blank" rel="noopener" data-ca-q="{kind}">{E(l)}</a>'
                for i, (l, m) in enumerate(chips))
    return (f'<!--ca-tanya--><section class="ca-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Dulu ke Ananta, CPA</b>'
            f'<p>{E(lead)}</p><div class="q">{a}</div></section><!--/ca-tanya-->')

LEAD = 'Belum yakin perlu KAP, KJA, KJPP, atau konsultan pajak? Tanyakan dulu ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.'

LEAD_KDMP = 'Pengurus Kopdes bingung soal pembukuan, laporan RAT, atau audit? Tanyakan dulu ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.'
def desc_for(svc, X, prov):
    T = {'kap': 'Cari KAP di {X}? Audit untuk bank, SABH, dan investor oleh KAP terdaftar. Tanya Ananta, CPA dulu lewat WhatsApp, gratis.',
         'kjpp': 'Butuh KJPP di {X}? Appraisal aset dan penilaian bisnis untuk bank dan investor. Tanya Ananta, CPA dulu lewat WhatsApp, gratis.',
         'kja': 'Cari KJA di {X}? Pembukuan dan laporan keuangan siap bank oleh Kantor Jasa Akuntansi berizin. Tanya Ananta, CPA lewat WhatsApp, gratis.',
         'konsultan-pajak': 'Cari konsultan pajak di {X}? SPT badan, Coretax, SP2DK, dan pemeriksaan pajak. Tanya Ananta, CPA dulu lewat WhatsApp, gratis.',
         'jasa-laporan-keuangan': 'Jasa penyusunan laporan keuangan di {X} untuk bank, pajak, dan investor. Tanya Ananta, CPA soal kebutuhan Anda lewat WhatsApp, gratis.',
         'laporan-tahunan-pt': 'Jasa laporan tahunan PT di {X} sesuai Permenkum 49/2025 untuk notaris dan SABH. Tanya Ananta, CPA lewat WhatsApp, gratis.',
         'kap-murah': 'Kisaran biaya audit KAP di {X} per skala aset dan cara hemat tanpa audit ulang. Tanya Ananta, CPA soal biaya lewat WhatsApp, gratis.',
         'hub': 'Cari akuntan di {X}: KAP, KJA, KJPP, dan konsultan pajak berizin. Bingung mulai dari mana? Tanya Ananta, CPA lewat WhatsApp, gratis.',
         'kawasan': 'KAP, KJPP, konsultan pajak, dan jasa laporan keuangan di {X}. Bingung mulai dari mana? Tanya Ananta, CPA lewat WhatsApp, gratis.',
         'kdmp': 'Laporan keuangan RAT, pembukuan, dan audit Kopdes Merah Putih di {X}. Pengurus cukup upload bukti. Tanya Ananta, CPA lewat WhatsApp.'}
    t = T.get(svc)
    if not t: return None
    for x in ([f'{X}, {prov}', X] if prov else [X]):
        d = t.format(X=x)
        if len(d) <= 158: return d
    return None

def fit_desc(d):
    d = re.sub(r'\s+', ' ', d).strip()
    out = ''
    for x in re.split(r'(?<=[.!?])\s+', d):
        cand = (out + ' ' + x).strip()
        if len(cand) <= 158: out = cand
        else: break
    return out or d

def kdmp_block(kab, prov, nkec):
    X = kab
    faq = [(f'Pakai SAK apa untuk laporan keuangan Kopdes Merah Putih di {X}?',
            'Menurut Permenkop UKM 2/2024, koperasi yang punya unit simpan pinjam anggota memakai SAK Indonesia atau SAK EP. Koperasi yang hanya bergerak di sektor riil memakai standar instansi pembina, atau bila belum ada: SAK Indonesia, SAK EP, atau SAK EMKM.'),
           ('Apa yang perlu disiapkan pengurus?',
            'Bukti kas masuk dan keluar, rekening koran, daftar simpanan dan pinjaman anggota, daftar aset, serta catatan setiap unit usaha. Semua cukup di-upload ke Google Drive, pembukuan dikerjakan dari sana.'),
           ('Kapan koperasi perlu diaudit?',
            'Bila diminta anggaran dasar atau keputusan RAT, diminta bank atau pemberi pembiayaan, atau disyaratkan instansi pembina. Audit dikerjakan KAP terdaftar, terpisah dari penyusun laporan keuangan.')]
    f = ''.join(f'<h3>{E(a)}</h3><p>{E(b)}</p>' for a, b in faq)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': a, 'acceptedAnswer': {'@type': 'Answer', 'text': b}} for a, b in faq]}, ensure_ascii=False)
    return (f'<!--ca-kdmp--><div class="prose" style="margin-top:26px"><h2>Laporan Keuangan Kopdes Merah Putih di {E(X)}</h2>'
            f'<p>Koperasi Desa dan Kelurahan Merah Putih di {nkec} kecamatan {E(X)}, {E(prov)}, perlu pembukuan yang rapi sejak bulan pertama: '
            f'untuk Rapat Anggota Tahunan, untuk pertanggungjawaban kepada anggota, dan untuk pengajuan pembiayaan ke bank. '
            f'Laporan yang disusun belakangan, menjelang RAT, biasanya sulit dicocokkan dengan bukti dan rekening koran.</p>'
            f'<h2>Cara Kerja</h2><ol><li>Pengurus upload bukti transaksi dan rekening koran ke Google Drive setiap bulan.</li>'
            f'<li>Pembukuan bulanan per unit usaha dikerjakan dari bukti tersebut, lengkap dengan laporan posisi keuangan dan laporan hasil usaha.</li>'
            f'<li>Menjelang RAT, laporan keuangan tahunan disusun sesuai SAK yang berlaku, siap dibacakan dan diserahkan ke instansi pembina.</li>'
            f'<li>Bila perlu audit, dikerjakan KAP terdaftar OJK yang terpisah dari penyusun laporan.</li></ol>'
            f'<h2>Tanya Jawab</h2>{f}</div><script type="application/ld+json">{ld}</script><!--/ca-kdmp-->')

MANUAL = {
 '': 'Cari KAP, KJA, KJPP, dan konsultan pajak berizin di seluruh Indonesia. Bingung mulai dari mana? Tanya Ananta, CPA lewat WhatsApp, gratis.',
 'layanan/kap': 'Cari KAP dan jasa audit laporan keuangan di 113 kota, dari Aceh sampai Papua. Tanya Ananta, CPA dulu lewat WhatsApp, gratis.',
 'layanan/kja': 'Cari KJA dan jasa pembukuan di 113 kota, dari Aceh sampai Papua. Laporan keuangan siap bank. Tanya Ananta, CPA lewat WhatsApp, gratis.',
 'layanan/kjpp': 'Cari KJPP untuk appraisal aset dan penilaian bisnis di 113 kota, dari Aceh sampai Papua. Tanya Ananta, CPA dulu lewat WhatsApp, gratis.',
 'layanan/konsultan-pajak': 'Cari konsultan pajak untuk SPT badan, Coretax, dan pemeriksaan pajak di 113 kota. Tanya Ananta, CPA dulu lewat WhatsApp, gratis.',
 'layanan/jasa-laporan-keuangan': 'Jasa penyusunan laporan keuangan untuk bank, pajak, dan investor di 113 kota, dari Aceh sampai Papua. Tanya Ananta, CPA lewat WhatsApp.',
 'layanan/laporan-tahunan-pt': 'Jasa laporan tahunan PT sesuai Permenkum 49/2025 untuk notaris dan SABH di 113 kota. Tanya Ananta, CPA lewat WhatsApp, gratis.',
}
changed = []
for dp, dn, fn in os.walk(OUT):
    if 'index.html' not in fn: continue
    p = os.path.join(dp, 'index.html'); rel = os.path.relpath(dp, OUT).replace(os.sep, '/')
    rel = '' if rel == '.' else rel
    parts = rel.split('/') if rel else []
    s0 = s = open(p, encoding='utf-8').read()
    noidx = bool(re.search(r'<meta(?=[^>]*name="robots")[^>]*noindex', s))
    is_en = parts[:1] == ['en']

    # --- tipe halaman
    svc = None; X = None; prov = None
    if parts[:1] == ['kota'] and len(parts) >= 2:
        city = parts[1]
        if len(parts) == 2: svc = 'hub'; X, prov = PLACE.get(city, (None, None))
        elif len(parts) == 3 and parts[2] in SVC: svc = parts[2]; X, prov = PLACE.get(city, (None, None))
        elif len(parts) == 3 and parts[2] != 'kecamatan': svc = 'kawasan'; X, prov = PLACE.get(city + '/' + parts[2], (None, None))
        elif len(parts) == 4 and parts[3] in SVC: svc = parts[3]; X, prov = PLACE.get(city + '/' + parts[2], (None, None))
    elif parts[:1] == ['kdmp'] and len(parts) == 3:
        svc = 'kdmp'
        h1 = re.search(r'<h1>([^<]+)</h1>', s); X = re.sub(r'^.* di ', '', html.unescape(h1.group(1))) if h1 else None
        cr = re.findall(r'<a href="/kdmp/[^/"]+/">([^<]+)</a>', s); prov = html.unescape(cr[0]) if cr else ''
    elif parts[:1] == ['layanan'] and len(parts) == 2:
        svc = parts[1]; X = 'kota ...'; prov = None
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    h1 = html.unescape(re.sub('<[^>]+>', '', h1m.group(1))).strip() if h1m else 'cariakuntan.com'
    topic = h1.split(':')[0].strip()
    if len(topic) > 60: topic = topic[:topic.rfind(' ', 0, 57)]

    # --- 1. label dan pesan WA
    gen = q('Selamat siang Pak Ananta, saya ingin diskusi kebutuhan kami.')
    if gen in s:
        s = s.replace(gen, q(f'Halo Pak Ananta, saya dari cariakuntan.com ({topic}). Mau tanya: '))
    s = re.sub(r'(<a\b[^>]*href="https://wa\.me/6282245260121[^"]*"[^>]*>)\s*(Chat Ananta, CPA|Chat WhatsApp|Diskusikan Kebutuhan Audit|Minta rekomendasi di [^<]{1,40})\s*</a>',
               r'\1Tanya Ananta, CPA</a>', s)
    if is_en:
        s = re.sub(r'(<a\b[^>]*href="https://wa\.me/6282245260121[^"]*"[^>]*>)\s*(Chat on WhatsApp|Chat with Ananta, CPA)\s*</a>', r'\1Ask Ananta, CPA</a>', s)
    s = s.replace('atau minta kami carikan yang mau datang ke ', 'atau tanya Ananta, CPA siapa yang bisa datang ke ')
    s = s.replace('· Kantor Akuntan Publik Mitra, Terdaftar OJK', '· Kantor Akuntan Publik, Terdaftar OJK').replace('<small>Kantor Akuntan Publik Mitra</small>', '<small>Kantor Akuntan Publik</small>')
    s = s.replace('Audit atau AUP oleh KAP mitra terdaftar OJK', 'Audit atau AUP oleh KAP DHN &amp; Rekan (terdaftar OJK)')

    if svc == 'kdmp': s = s.replace('<p>' + E(LEAD) + '</p><div class="q"><a class="w" href="' + WA + q('Halo Pak Ananta, kami pengurus'), '<p>' + E(LEAD_KDMP) + '</p><div class="q"><a class="w" href="' + WA + q('Halo Pak Ananta, kami pengurus'))

    # --- 4. FAQ ganda berurutan
    s = re.sub(r'(<h3>([^<]+)</h3><p>(?:(?!</p>).)*</p>)\1', r'\1', s, flags=re.S)

    if not noidx:
        # --- 5. KDMP kabupaten
        if svc == 'kdmp' and '<!--ca-kdmp-->' not in s and X:
            nkec = len(re.findall(r'<a href="/kdmp/[^"]+/[^"]+/[^"]+/">', s))
            s = s.replace('<p class="sub">Pilih kecamatan Anda.</p>', f'<p class="sub">Pembukuan, laporan keuangan RAT, dan audit Koperasi Desa Merah Putih di {E(X)}. Pilih kecamatan Anda, atau tanya dulu ke Ananta, CPA.</p>', 1)
            m = re.search(r'<div style="margin-top:22px"><a class="btn btn-wa arrow"[^>]*>[^<]*</a></div></main>', s)
            if m:
                s = s[:m.start()] + kdmp_block(X, prov, nkec) + s[m.start():]

        # --- 2. kotak tanya
        if '<!--ca-tanya-->' not in s:
            ins = None
            if svc and X:
                m = re.search(r'<div style="margin-top:22px[^"]*"><a class="btn btn-wa arrow"[^>]*>[^<]*</a>(?:<span[^>]*>[^<]*</span>)?</div>', s)
                ch = chips_for(svc, X)
                if X == 'kota ...': ch = [(l.replace(' di kota ...', ''), mm) for l, mm in ch]
                if m: ins = (m.end(), box(ch, LEAD_KDMP if svc == 'kdmp' else LEAD, svc))
                elif svc == 'kdmp':
                    m = re.search(r'<!--ca-kdmp-->', s)
                    if m: ins = (m.start(), box(chips_for(svc, X), 'Pengurus koperasi bisa bertanya dulu ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.', svc))
            elif parts[:1] == ['artikel'] and len(parts) == 2:
                main = s.find('<main'); endm = s.find('</main>')
                hs = [mm.start() for mm in re.finditer(r'<h2\b', s[main:endm])]
                if len(hs) >= 2:
                    ch = [('Tanya soal ini untuk usaha saya', f'Halo Pak Ananta, saya baca "{topic}" di cariakuntan.com. Mau tanya untuk usaha kami: '),
                          ('Perlu KAP, KJA, atau konsultan pajak?', f'Halo Pak Ananta, saya baca "{topic}" di cariakuntan.com. Kami bingung perlu KAP, KJA, atau konsultan pajak.')]
                    ins = (main + hs[1], box(ch, 'Kasus Anda mirip dengan artikel ini? Tanyakan dulu ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.', 'artikel'))
            if ins:
                s = s[:ins[0]] + ins[1] + s[ins[0]:]
                if 'id="ca-tanya-css"' not in s: s = s.replace('</head>', STYLE + '</head>', 1)

        # --- 3. title dan description
        tm = re.search(r'<title>(.*?)</title>', s, re.S)
        if tm and len(html.unescape(tm.group(1))) > 65 and tm.group(1).endswith(' | cariakuntan.com'):
            s = s.replace(tm.group(0), '<title>' + tm.group(1)[:-len(' | cariakuntan.com')] + '</title>', 1)
        dm = re.search(r'<meta content="([^"]*)" name="description"\s*/?>', s)
        if dm:
            d = html.unescape(dm.group(1)); nd = d
            if rel in MANUAL:
                nd = MANUAL[rel]
            elif rel == 'cek-izin':
                nd = 'Cek izin resmi KAP, akuntan publik, KJA, KJPP, dan penilai publik dari registri PPPK Kemenkeu, per kota. Ragu? Tanya Ananta, CPA lewat WhatsApp.'
            elif svc and X and X != 'kota ...' and svc != 'akuntan-forensik':
                nd = desc_for(svc, X, prov) or (fit_desc(d) if len(d) > 158 else d)
            elif len(d) > 158:
                nd = fit_desc(d)
            if nd != d:
                e = E(nd)
                s = s.replace(dm.group(0), f'<meta content="{e}" name="description"/>', 1)
                s = re.sub(r'<meta content="[^"]*" property="og:description"\s*/?>', f'<meta content="{e}" property="og:description"/>', s, count=1)
        if rel == 'cek-izin':
            s = s.replace('<link href="https://cariakuntan.com/screening/" rel="canonical"/>', '<link href="https://cariakuntan.com/cek-izin/" rel="canonical"/>')
            s = s.replace('<meta content="https://cariakuntan.com/screening/" property="og:url"/>', '<meta content="https://cariakuntan.com/cek-izin/" property="og:url"/>')

    if s != s0:
        changed.append((rel, noidx))
        if not DRY: open(p, 'w', encoding='utf-8').write(s)

smp = os.path.join(OUT, 'sitemap.xml'); sm = open(smp, encoding='utf-8').read(); sm0 = sm
for rel, noidx in changed:
    if noidx: continue
    u = 'https://cariakuntan.com/' + (rel + '/' if rel else '')
    sm = re.sub(r'(<loc>' + re.escape(u) + r'</loc>\s*<lastmod>)[^<]+', r'\g<1>' + TODAY, sm)
if sm != sm0 and not DRY: open(smp, 'w', encoding='utf-8').write(sm)
print('changed', len(changed), 'indexable', sum(1 for r in changed if not r[1]), 'dry' if DRY else '')
