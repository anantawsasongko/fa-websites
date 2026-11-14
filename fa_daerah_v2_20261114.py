#!/usr/bin/env python3
"""FA: font judul baru + halaman daerah selevel beranda (14 Nov 2026).

Pemicu (Bos): "font-nya jelek", "halaman daerah masih jelek, gak serapi dan
gak semengesankan halaman induk".

A. SEMUA halaman out/faindonesia: font judul Times New Roman diganti
   Newsreader (self-hosted /fonts/, OFL). Caranya: @font-face dengan nama
   keluarga "Times New Roman" dan "Times" diarahkan ke file Newsreader, jadi
   semua aturan lama (termasuk style inline dan !important) ikut tanpa
   disentuh satu per satu. Blok <!--fa-type--> sebelum </head>.

B. Halaman daerah (semua keluarga /<layanan>/<wilayah>/..., pola hero
   eyebrow "X · Kota"): kelas body fa-dv2 + <style id="fa-dv2">:
   hero berlatar foto pegunungan monokrom seperti beranda (memudar ke gelap),
   strip angka rekam jejak seperti beranda (<!--fa-dv2f-->), kartu KAP DHN /
   KJA monokrom dengan garis aksen tipis, tombol kartu jadi tombol garis,
   kotak lk2 emas jadi monokrom, semua akordeon satu gaya, Peta Isi rapi,
   kartu tim tinggi sama (gelar panjang di kartu diringkas; gelar lengkap
   tetap di alt foto dan di halaman profil).

SEO tidak berubah: title, description, H1, teks, URL, JSON-LD, link tetap.
Idempoten. --dry untuk hitung saja.
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv

FONT = '/fonts/'
LAT = ('U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,'
       'U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD')
LATX = ('U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,'
        'U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,'
        'U+2113,U+2C60-2C7F,U+A720-A7FF')


def faces():
    out = []
    for fam in ('Newsreader', 'Times New Roman', 'Times', 'EB Garamond', 'Cormorant Garamond', 'Georgia', 'Garamond'):
        for style in ('normal', 'italic'):
            for sub, rng in (('latin', LAT), ('latin-ext', LATX)):
                out.append(
                    "@font-face{font-family:'%s';font-style:%s;font-weight:200 800;"
                    "font-display:swap;src:url(%snewsreader-%s-wght-%s.woff2) format('woff2');"
                    "unicode-range:%s}" % (fam, style, FONT, sub, style, rng))
    return ''.join(out)


TYPE_CSS = faces() + (
    ":root{--fa-serif:'Newsreader','Times New Roman',Georgia,serif}"
    "h1,h2,h3{font-optical-sizing:auto;text-rendering:optimizeLegibility;"
    "-webkit-font-smoothing:antialiased}"
    "h1{letter-spacing:-.015em!important}"
    "@media(min-width:861px){.hero:has(.hmark) h1{max-width:calc(100% - clamp(190px,19vw,280px))!important}}"
)
TYPE_BLOCK = ('<!--fa-type--><link rel="preload" href="/fonts/newsreader-latin-wght-normal.woff2" '
              'as="font" type="font/woff2" crossorigin/><style id="fa-type">%s</style><!--/fa-type-->'
              % TYPE_CSS)

S = 'body.fa-dv2'
DV2_CSS = (
    # hero: foto beranda, monokrom, memudar ke latar gelap
    S + ' main>section.block:first-child{position:relative;isolation:isolate}'
    + S + ' main>section.block:first-child::before{content:"";position:absolute;left:0;right:0;top:0;'
    'height:min(760px,100%);z-index:-1;pointer-events:none;'
    'background:linear-gradient(180deg,rgba(18,18,18,.30) 0%,rgba(18,18,18,.62) 45%,rgba(18,18,18,1) 100%),'
    'url(/img/fa/landscape.jpg) center 30%/cover no-repeat;filter:grayscale(1)}'
    + S + ' main>section.block:first-child>.wrap{position:relative}'
    + S + ' main>section.block:first-child>.wrap>*:not(h1){max-width:760px!important;box-sizing:border-box}'
    + S + ' main>section.block:first-child>.wrap>.dhn2{width:100%!important;margin-left:0!important}'
    + S + ' main .eyebrow{color:rgba(255,255,255,.72)!important}'
    + S + ' main>section.block:first-child h1{font-size:clamp(34px,4.4vw,58px)!important;'
    'line-height:1.08!important;font-weight:400!important;max-width:17em;margin:.25em 0 .45em!important}'
    + S + ' main>section.block:first-child>.wrap>p.t{font-size:17px;line-height:1.65;'
    'color:rgba(255,255,255,.78);max-width:40em!important}'
    # tombol hero: kotak tegas seperti beranda
    + S + ' main .cbtns .btn{border-radius:2px!important;font-weight:600;letter-spacing:.01em}'
    # strip angka
    + S + ' .dvf{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:34px 0 8px;'
    'border-top:1px solid rgba(255,255,255,.16);border-bottom:1px solid rgba(255,255,255,.16)}'
    + S + ' .dvf>div{padding:20px 22px 18px 0}'
    + S + ' .dvf>div+div{padding-left:22px;border-left:1px solid rgba(255,255,255,.12)}'
    + S + ' .dvf b{display:block;font-family:var(--fa-serif);font-weight:400;font-size:clamp(30px,3.4vw,44px);'
    'line-height:1;letter-spacing:-.01em;color:#fff}'
    + S + ' .dvf span{display:block;margin-top:8px;font-size:13px;line-height:1.45;color:rgba(255,255,255,.62)}'
    + '@media(max-width:640px){' + S + ' .dvf{grid-template-columns:1fr}'
    + S + ' .dvf>div,' + S + ' .dvf>div+div{padding:16px 0;border-left:0}'
    + S + ' .dvf>div+div{border-top:1px solid rgba(255,255,255,.12)}}'
    # kartu KAP DHN / KJA: monokrom, garis aksen tipis
    + S + ' .dhnc{background:rgba(255,255,255,.03)!important;border:1px solid rgba(255,255,255,.12)!important;'
    'border-top:2px solid #C8661A!important;border-radius:3px!important;padding:22px!important}'
    + S + ' .dhnc.kja{border-top-color:#4A72D9!important}'
    + S + ' .dhnc small{color:rgba(255,255,255,.55)!important;letter-spacing:.18em!important;font-weight:500!important}'
    + S + ' .dhnc b.n{font-family:var(--fa-serif)!important;font-weight:400!important;font-size:24px!important;'
    'letter-spacing:-.005em;margin:4px 0 8px!important}'
    + S + ' .dhnc p{font-size:14px!important;color:rgba(255,255,255,.72);opacity:1!important}'
    + S + ' .dhnc img{filter:grayscale(1) brightness(1.6);opacity:.85}'
    + S + ' .dhnc .dhnb,' + S + ' .dhnc.kja .dhnb{background:transparent!important;color:#fff!important;'
    'border:1px solid rgba(255,255,255,.32)!important;border-radius:2px!important;box-shadow:none!important;'
    'font-weight:600;font-size:13px;padding:10px 16px!important}'
    + S + ' .dhnc .dhnb:hover{background:#fff!important;color:#111!important;border-color:#fff!important}'
    # kotak kontak lk2 (emas) jadi monokrom
    + S + ' details.lk2{border:1px solid rgba(255,255,255,.14)!important;border-radius:3px!important;'
    'background:rgba(255,255,255,.03)!important}'
    + S + ' details.lk2>summary b{font-family:var(--fa-serif);font-weight:400!important;font-size:20px!important}'
    + S + ' details.lk2 .btn{border-radius:2px!important}'
    # kartu tim
    + S + ' .wj{align-items:stretch}'
    + S + ' .wj>a{display:flex!important;flex-direction:column;border-radius:3px!important;'
    'border:1px solid rgba(255,255,255,.1)!important}'
    + S + ' .wj>a>div{flex:1}'
    + S + ' .wj b{font-family:var(--fa-serif)!important;font-weight:400!important;font-size:19px!important;line-height:1.25!important}'
    + S + ' .fl-card{border-radius:3px!important;border-color:rgba(255,255,255,.12)!important}'
    + S + ' .fl-card b{font-family:var(--fa-serif)!important;font-weight:400!important;font-size:19px!important}'
    # Peta Isi
    + S + ' .pf-map{background:transparent!important;border:0!important;border-top:1px solid rgba(255,255,255,.16)!important;'
    'border-radius:0!important;padding:22px 0 6px!important;box-shadow:none!important}'
    + S + ' .pf-map a{border-radius:2px!important;background:rgba(255,255,255,.04)!important}'
    + S + ' .pf-map a:hover{background:rgba(255,255,255,.09)!important}'
    + S + ' .pf-map>b{font-size:11px!important;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.55)}'
    # akordeon: satu gaya untuk semua (kecuali FAQ)
    + S + ' main details.dfold,' + S + ' main details.rg,' + S + ' main section.fnx>details,'
    + S + ' main details[class^="fa-"],' + S + ' main details.uqd{border:0!important;'
    'border-bottom:1px solid rgba(255,255,255,.12)!important;border-radius:0!important;background:transparent!important;'
    'margin:0!important;padding:0!important;box-shadow:none!important}'
    + S + ' main details.dfold>summary,' + S + ' main details.rg>summary,' + S + ' main section.fnx>details>summary,'
    + S + ' main details[class^="fa-"]>summary,' + S + ' main details.uqd>summary{'
    'display:flex!important;align-items:baseline;gap:10px;list-style:none;cursor:pointer;'
    'padding:20px 36px 20px 0!important;position:relative;'
    'font-family:var(--fa-serif)!important;font-weight:400!important;font-size:21px!important;line-height:1.3!important;'
    'color:#f2f2f2!important;background:transparent!important;border:0!important}'
    + S + ' main details>summary::-webkit-details-marker{display:none}'
    + S + ' main details.dfold>summary h2{font:inherit!important;margin:0!important;padding:0!important;border:0!important;color:inherit!important}'
    + S + ' main details.rg>summary i,' + S + ' main section.fnx>details>summary i,'
    + S + ' main details[class^="fa-"]>summary i{font-style:normal;font-family:var(--body,sans-serif);'
    'font-size:12px;color:rgba(255,255,255,.45);letter-spacing:.06em}'
    + S + ' main details.dfold>summary::after,' + S + ' main details.rg>summary::after,'
    + S + ' main section.fnx>details>summary::after,' + S + ' main details[class^="fa-"]>summary::after,'
    + S + ' main details.uqd>summary::after{content:"+"!important;position:absolute;right:4px;top:50%;'
    'transform:translateY(-50%);font:300 22px/1 var(--body,sans-serif)!important;color:rgba(255,255,255,.55);'
    'margin-top:0!important;transition:transform .2s;background:none!important;border:0!important;width:auto!important;height:auto!important}'
    + S + ' main details[open]>summary::after{transform:translateY(-50%) rotate(45deg)!important}'
    + S + ' main details.dfold>summary::before,' + S + ' main details.rg>summary::before,'
    + S + ' main section.fnx>details>summary::before,' + S + ' main details[class^="fa-"]>summary::before{content:none!important}'
    + S + ' main details.dfold>.dfb,' + S + ' main details.rg>.rg-l{padding:0 0 22px!important}'
    # judul H2 terbuka dan FAQ
    + S + ' main .wrap>h2{font-weight:400!important;letter-spacing:-.01em}'
    + S + ' main .faq-i>summary{font-weight:500}'
    + S + ' main table{border-radius:2px}'
)
DV2_BLOCK = '<!--fa-dv2--><style id="fa-dv2">%s</style><!--/fa-dv2-->' % DV2_CSS

FACTS = ('<!--fa-dv2f--><div aria-label="Rekam jejak FA Indonesia" class="dvf">'
         '<div><b>Rp1,1 T+</b><span>Pembiayaan perbankan dicairkan, ditambah pendanaan investor hingga US$3 juta</span></div>'
         '<div><b>10+</b><span>Mandat divestasi aktif: rumah sakit dan BPR</span></div>'
         '<div><b>2016</b><span>Tahun berdiri</span></div>'
         '</div><!--/fa-dv2f-->')

NAMES = {
    '<b>Farhani Kautsar Nugraha, S.E., M.S.A., Ak., CA</b>': '<b>Farhani Kautsar Nugraha, CA</b>',
    '<b>Dr. (C) Dwi Haryadi Nugraha, SST, MSi, Ak, CA, BKP, ASEAN CPA, CPA, CFI</b>':
        '<b>Dr. (C) Dwi Haryadi Nugraha, CPA</b>',
}

HERO = re.compile(r'<main[^>]*>\s*<section class="block">\s*<div class="wrap art">\s*'
                  r'<p class="eyebrow">([^<]*)</p>\s*<h1')
SKIP_TOP = {'en', 'ja', 'ko', 'zh', 'artikel'}
RX_BLOCK = lambda m: re.compile(r'<!--%s-->.*?<!--/%s-->' % (m, m), re.S)


def put(h, marker, block, before):
    rx = RX_BLOCK(marker)
    if rx.search(h):
        return rx.sub(lambda _: block, h, count=1)
    i = h.find(before)
    if i < 0:
        return h
    return h[:i] + block + h[i:]


def is_daerah(rel, h):
    seg = rel.split('/')
    if len(seg) < 3 or seg[0] in SKIP_TOP:
        return False
    m = HERO.search(h)
    return bool(m and '·' in m.group(1))


def body_class(h):
    m = re.search(r'<body([^>]*)>', h)
    if not m or 'fa-dv2' in m.group(1):
        return h
    attrs = m.group(1)
    if re.search(r'\bclass="', attrs):
        attrs = re.sub(r'\bclass="', 'class="fa-dv2 ', attrs, count=1)
    else:
        attrs = attrs + ' class="fa-dv2"'
    return h[:m.start()] + '<body' + attrs + '>' + h[m.end():]


def add_facts(h):
    rx = RX_BLOCK('fa-dv2f')
    if rx.search(h):
        return rx.sub(lambda _: FACTS, h, count=1)
    i = h.find('<main')
    j = h.find('<div class="cbtns"', i)
    if j < 0:
        return h
    k = h.find('</div>', j)
    if k < 0:
        return h
    k += len('</div>')
    return h[:k] + FACTS + h[k:]


def main():
    n_all = n_dv = 0
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
            h = open(p, encoding='utf-8', errors='surrogateescape').read()
            if '</head>' not in h:
                continue
            o = h
            h = put(h, 'fa-type', TYPE_BLOCK, '</head>')
            if is_daerah(rel, h):
                h = put(h, 'fa-dv2', DV2_BLOCK, '</head>')
                h = body_class(h)
                h = add_facts(h)
                for a, b in NAMES.items():
                    h = h.replace(a, b)
                n_dv += 1
            if h != o:
                n_all += 1
                if not DRY:
                    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(h)
    print(('DRY ' if DRY else '') + 'berubah: %d file, halaman daerah: %d' % (n_all, n_dv))


if __name__ == '__main__':
    main()
