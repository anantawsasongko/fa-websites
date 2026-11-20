#!/usr/bin/env python3
"""CariAkuntan jadi produk "LK Siap Bank" (20 Nov 2026, Bos: "ganti aja cari akuntan ini jadi model startup").
BEKERJA DI out/cariakuntan, idempoten, --dry. Sumber: fa_content/lsb20261120/ (app.html, home.html, home_demo.html, lsb.css, lsb.js).
1. /lk-siap-bank/ (alat: upload mutasi rekening CSV/Excel -> laba rugi, posisi keuangan, skor siap bank; semua di browser).
2. Beranda: hero dan bagian produk baru di antara <!--lsb20-home--> ... <!--/lsb20-home-->; bagian Screening dibuang dari beranda.
3. Tab pertama menu: "Cek Kebutuhan" -> "LK Siap Bank" di semua halaman bahasa Indonesia.
4. sitemap.xml dan llms.txt.
JALANKAN PALING AKHIR untuk CA (sesudah caus_ramping_20261120.py), karena generator lama menulis hero dan menu lama."""
import os, re, sys, hashlib, json
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, 'out', 'cariakuntan'); SRC = os.path.join(ROOT, 'fa_content', 'lsb20261120')
DRY = '--dry' in sys.argv; changed = []
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s):
    old = rd(p) if os.path.exists(p) else None
    if old == s: return
    changed.append(os.path.relpath(p, OUT))
    if not DRY:
        os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(s)
def src(n): return rd(os.path.join(SRC, n))
def ver(s): return hashlib.md5(s.encode()).hexdigest()[:8]
def sub1(pat, rep, s, flags=re.S):
    out, n = re.subn(pat, lambda m: rep, s, count=1, flags=flags)
    assert n == 1, 'pola tidak ketemu: ' + pat[:70]
    return out

CSS = src('lsb.css'); JS = src('lsb.js'); vc = ver(CSS); vj = ver(JS)
wr(os.path.join(OUT, 'css', 'lsb.css'), CSS); wr(os.path.join(OUT, 'js', 'lsb.js'), JS)
LINK = '<link href="/css/lsb.css?v=%s" id="lsb-css" rel="stylesheet"/>' % vc
NAVH = '<nav aria-label="Menu" class="tabs">'
NAV_OLD = NAVH + '<a href="/cek-kebutuhan/">Cek Kebutuhan</a>'
NAV_OLD2 = NAVH + '<a aria-current="page" href="/cek-kebutuhan/">Cek Kebutuhan</a>'
NAV_NEW = NAVH + '<a href="/lk-siap-bank/">LK Siap Bank</a>'

# ---------- 1. halaman alat ----------
T_TITLE = 'LK Siap Bank: Buat Laporan Keuangan dari Mutasi Rekening'
T_DESC = 'Upload mutasi rekening usaha (CSV atau Excel), langsung jadi laba rugi, posisi keuangan, dan skor kesiapan kredit bank. Gratis dicoba, tanpa daftar.'
U = 'https://cariakuntan.com/lk-siap-bank/'
assert len(T_TITLE) <= 65 and len(T_DESC) <= 158, (len(T_TITLE), len(T_DESC))
app = src('app.html')
faq = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', app, flags=re.S)
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebApplication", "name": "LK Siap Bank", "url": U, "applicationCategory": "FinanceApplication", "operatingSystem": "Web", "inLanguage": "id",
     "description": T_DESC, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR"}, "publisher": {"@type": "Organization", "name": "CariAkuntan", "url": "https://cariakuntan.com/"}},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": "https://cariakuntan.com/"}, {"@type": "ListItem", "position": 2, "name": "LK Siap Bank", "item": U}]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in faq]}]}
t = rd(os.path.join(OUT, 'cek-kebutuhan', 'index.html'))
OT = re.search(r'<title>(.*?)</title>', t).group(1); OD = re.search(r'<meta content="([^"]*)" name="description"/>', t).group(1)
t = t.replace(OT, T_TITLE).replace(OD, T_DESC).replace('https://cariakuntan.com/cek-kebutuhan/', U)
t = sub1(r'<style id="kb-css">.*?</style>', '', t)
t = sub1(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>', t)
t = sub1(r'<script id="kb-js">.*?</script>', '', t)
t = sub1(r'(?<=<main class="wrap art">).*?(?=</main>)', app, t)
t = sub1(r'<!--rx13f-->.*?<!--/rx13f-->', '', t)
t = sub1(r'<section class="tshare">.*?</section>\s*(?=<!--dhn-->)', '', t)
t = t.replace(NAV_OLD2, NAV_NEW).replace(NAV_OLD, NAV_NEW).replace(NAV_NEW, NAV_NEW.replace('<a href="/lk-siap-bank/">', '<a aria-current="page" href="/lk-siap-bank/">'))
t = t.replace("at:[{sel:'#screening',pos:'beforebegin'}]", "at:[{sel:'#lsb',pos:'beforebegin'}]")
t = re.sub(r'%28Cek%20Izin%20KAP%2C%20KJA%2C%20KJPP%2C%20Konsultan%20Pajak%2C%20dan%20Penilai%20Publik%29', '%28LK%20Siap%20Bank%29', t)
t = t.replace('</head>', LINK + '</head>', 1) if 'id="lsb-css"' not in t else t
t = t.replace('</body>', '<script defer src="/js/lsb.js?v=%s"></script></body>' % vj, 1)
OG = '/img/og-page/lk-siap-bank.jpg'
if os.path.exists(os.path.join(OUT, OG.lstrip('/'))): t = t.replace('https://cariakuntan.com/img/og-page/screening.jpg', 'https://cariakuntan.com' + OG)
if 'property="og:image"' not in t: t = t.replace('<meta property="og:image:width"', '<meta property="og:image" content="%s"/><meta property="og:image:width"' % re.search(r'name="twitter:image" content="([^"]+)"', t).group(1), 1)
assert t.count('<h1') == 1 and '—' not in app
wr(os.path.join(OUT, 'lk-siap-bank', 'index.html'), t)

# ---------- 2. beranda ----------
H_TITLE = 'LK Siap Bank: Laporan Keuangan Usaha untuk Kredit | CariAkuntan'
H_DESC = 'Upload mutasi rekening usaha, lihat laba rugi, posisi keuangan, dan skor kesiapan kredit dalam 10 menit. Gratis dicoba. Direktori KAP, KJA, KJPP tetap ada.'
assert len(H_TITLE) <= 65 and len(H_DESC) <= 158, (len(H_TITLE), len(H_DESC))
demo = src('home_demo.html') if os.path.exists(os.path.join(SRC, 'home_demo.html')) else ''
block = '<!--lsb20-home-->' + src('home.html').replace('{{DEMO}}', demo).strip() + '<!--/lsb20-home-->'
p = os.path.join(OUT, 'index.html'); h = rd(p)
if '<!--lsb20-home-->' in h:
    h = sub1(r'<!--lsb20-home-->.*?<!--/lsb20-home-->', block, h)
else:
    h = sub1(r'<section class="hero">.*?</section>(?=\s*<section class="want")', block, h)
    h = sub1(r'<section class="rx-s alt" id="screen">.*?(?=<section class="rx-s" id="cek">)', '', h)
    h = h.replace('<p class="rx-ey">Alat Gratis 2</p>', '<p class="rx-ey">Cek Izin</p>', 1)
    h = sub1(r'<section class="final">.*?</section>', '<section class="final"><div class="wrap"><h2>Mulai dari Mutasi Rekening Anda.</h2><p>Gratis dicoba, tanpa daftar, hasil langsung tampil.</p><span style="display:inline-flex;gap:10px;flex-wrap:wrap;justify-content:center"><a class="btn btn-wa arrow" href="/lk-siap-bank/">Buat LK Sekarang</a><a class="btn btn-line" href="https://wa.me/6282245260121?text=Halo%20Pak%20Ananta%2C%20saya%20ingin%20tanya%20soal%20laporan%20keuangan%20untuk%20pengajuan%20kredit%20bank." rel="noopener" style="color:#fff;border-color:rgba(255,255,255,.5)" target="_blank">WhatsApp</a></span><p class="more"><a href="/artikel/">Panduan, tabel biaya, dan layanan per kota ada di Wawasan →</a></p></div></section>', h)
    h = h.replace("<script>window.FA_SECURE={brand:'ca',mode:'send',at:[{sel:'#screening',pos:'beforebegin'}]}</script>", "<script>window.FA_SECURE={brand:'ca',mode:'send',at:[]}</script>")
    h = re.sub(r"<script>window\.FA_DONASI=\{[^<]*?'#f_go1'[^<]*?</script>", "<script>window.FA_DONASI={accent:'#1F5BFF',accentInk:'#fff',guards:[]}</script>", h)
    OT = re.search(r'<title>(.*?)</title>', h).group(1); OD = re.search(r'<meta content="([^"]*)" name="description"/>', h).group(1)
    h = h.replace(OT + ' | cariakuntan.com', H_TITLE).replace(OT, H_TITLE).replace(OD, H_DESC)
h = re.sub(r'<link href="/css/lsb\.css\?v=[0-9a-f]+" id="lsb-css" rel="stylesheet"/>', '', h).replace('</head>', LINK + '</head>', 1)
assert h.count('<h1') == 1 and 'id="screening"' not in h
wr(p, h)

# ---------- 3. menu ----------
for dp, dn, fn in os.walk(OUT):
    for f in fn:
        if not f.endswith('.html'): continue
        fp = os.path.join(dp, f)
        if fp == os.path.join(OUT, 'lk-siap-bank', 'index.html'): continue
        s = rd(fp)
        if NAV_OLD in s or NAV_OLD2 in s: wr(fp, s.replace(NAV_OLD2, NAV_OLD).replace(NAV_OLD, NAV_NEW))

# ---------- 4. sitemap dan llms ----------
p = os.path.join(OUT, 'sitemap.xml'); s = rd(p)
if '/lk-siap-bank/' not in s: wr(p, s.replace('</urlset>', '<!--lsb20--><url><loc>%s</loc><lastmod>2026-11-20</lastmod></url><!--/lsb20-->\n</urlset>' % U))
p = os.path.join(OUT, 'llms.txt'); s = rd(p)
if '/lk-siap-bank/' not in s:
    line = '- [LK Siap Bank](%s): alat gratis, upload mutasi rekening usaha (CSV atau Excel) menjadi laba rugi, posisi keuangan, dan skor kesiapan kredit bank; diolah di browser\n' % U
    m = re.search(r'^- \[Cek Kebutuhan Jasa Akuntan\]', s, flags=re.M)
    wr(p, s[:m.start()] + line + s[m.start():] if m else s.rstrip('\n') + '\n' + line)
print(('DRY ' if DRY else '') + 'berubah: %d file' % len(changed)); print('\n'.join(changed[:12]))
