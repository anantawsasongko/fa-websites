#!/usr/bin/env python3
"""CA + US senada FA (17 Nov 2026).

Pemicu (Bos): "CA dan US belum satupun menghasilkan lead ke WA dan ke FA" lalu
"Periksa, redesign (tambah apa gitu, design senada FA), push, optimalkan, deploy".

Temuan GSC 17 Nov: sejak ±9 Nov impresi CA dan US hampir nol, sementara FA naik
(750 klik/28 hari). Query yang dulu dimenangkan CA ("kap terdekat", "kjpp terdekat",
"konsultan pajak purbalingga") sekarang dimenangkan FA /wilayah/<kota>/. CA dan FA
berebut niat pencarian yang sama. Arah: CA = DIREKTORI/registri (daftar kantor
berizin + jumlahnya), FA = jasa. US = edukasi standar.

Isi script (idempoten, --dry):
 1. Aset: font Newsreader + foto landscape FA disalin ke out/cariakuntan dan out/updatesak.
 2. /css/rx17.css + <link id="rx17-css"> di semua HTML CA dan US: font judul Newsreader,
    header gelap ala FA.
 3. Halaman dalam: bagian pembuka (crumb, label, H1, lead, share, tombol) dibungkus
    <header class="rxh"> -> hero gelap foto monokrom ala FA. Teks, urutan, link tetap.
 4. CA /kota/<kota>/ dan /kota/<kota>/{kap,kja,kjpp}/: strip angka registri di hero
    (<!--rx17s-->) + title/description "Daftar KAP <Kota>: n Kantor ..." (data registri
    PPPK yang sama dengan blok uq-lokal). konsultan-pajak: title cocok query.
 5. US /psak/<no>/ dan /standar-audit/<x>/: title "<Kode> <nama ringkas>: Ringkasan dan
    Contoh" (<= 65, tidak terpotong), tombol hero Chat Ananta, CPA + Dikerjakan Tim FA.
 6. Label tombol "Tanya Ananta, CPA" -> "Chat Ananta, CPA" (sama dengan FA); kalimat
    "dijawab langsung" di kotak ca-tanya / us-tanya dibuang (aturan rendah hati 12 Nov).

Jalankan PALING AKHIR untuk CA dan US (setelah caus_artikel_daerah_20261115.py dan
fa_ai_beranda_20261116.py).
"""
import glob, html, os, re, shutil, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
DRY = "--dry" in sys.argv
sys.path.insert(0, os.path.join(ROOT, "shared"))
import lokal as L  # noqa: E402

VER = "20261117"
changed = {"cariakuntan": 0, "updatesak": 0}

# ---------------------------------------------------------------- CSS
CSS = """/* rx17 (17 Nov 2026): CA + US senada FA. Sumber: caus_hero_fa_20261117.py */
@font-face{font-family:"Newsreader";font-style:normal;font-weight:200 800;font-display:swap;src:url(/fonts/newsreader-latin-wght-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Newsreader";font-style:normal;font-weight:200 800;font-display:swap;src:url(/fonts/newsreader-latin-ext-wght-normal.woff2) format("woff2");unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Newsreader";font-style:italic;font-weight:200 800;font-display:swap;src:url(/fonts/newsreader-latin-wght-italic.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F}
html:root{--rx-serif:"Newsreader",Georgia,"Times New Roman",serif;--display:var(--rx-serif)}
h1,h2,h3{font-family:var(--rx-serif)}
/* header gelap ala FA */
header.top{background:#141414!important;border-bottom:1px solid rgba(255,255,255,.08)!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important}
header.top .wm{color:#fff!important}
header.top .tabs a{color:rgba(255,255,255,.66)!important;border-bottom-color:transparent}
header.top .tabs a:hover{color:#fff!important}
header.top .tabs a[aria-current="page"]{color:#fff!important;border-bottom-color:#fff!important}
header.top .langs a{color:rgba(255,255,255,.55)!important;border-color:rgba(255,255,255,.18)!important;background:transparent!important}
header.top .langs a[aria-current]{color:#141414!important;background:#fff!important;border-color:#fff!important}
header.top .btn{background:#fff!important;color:#141414!important;border:1px solid #fff!important;border-radius:2px!important;box-shadow:none!important}
header.top .btn:hover{background:transparent!important;color:#fff!important}
/* hero halaman dalam */
body.rx17{overflow-x:clip}
body.rx17 main.wrap.art,body.rx17 article.art{padding-top:0!important}
.rxh{position:relative;isolation:isolate;box-sizing:border-box;color:#fff;margin:0 calc(50% - 50vw) 34px;padding:58px calc(50vw - 50%) 44px;background:#141414}
.rxh:before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:linear-gradient(180deg,rgba(20,20,20,.42) 0%,rgba(20,20,20,.78) 55%,#141414 100%),url(/img/fa-landscape.jpg) center 30%/cover no-repeat;filter:grayscale(1)}
.rxh>*{max-width:760px}
.rxh .crumb,.rxh .crumb a{color:rgba(255,255,255,.58)!important;font-size:12.5px}
.rxh .crumb a:hover{color:#fff!important}
.rxh .label{display:flex;align-items:center;gap:12px;color:rgba(255,255,255,.74)!important;letter-spacing:.2em!important;font-weight:500!important;margin-top:22px!important}
.rxh .label:before{content:"";flex:0 0 34px;height:1px;background:rgba(255,255,255,.7)}
.rxh h1{color:#fff!important;font-family:var(--rx-serif)!important;font-weight:400!important;font-size:clamp(32px,4.3vw,52px)!important;line-height:1.1!important;letter-spacing:-.01em!important;margin:.32em 0 .5em!important;max-width:17em}
.rxh .sub,.rxh .lede,.rxh>p{color:rgba(255,255,255,.8)!important;font-size:17px!important;line-height:1.65!important}
.rxh .upd{color:rgba(255,255,255,.52)!important;font-size:12.5px!important}
.rxh .share,.rxh .share span,.rxh .tshare-top{color:rgba(255,255,255,.62)!important}
.rxh .share a,.rxh .share button{color:rgba(255,255,255,.86)!important;border-color:rgba(255,255,255,.24)!important;background:transparent!important}
.rxh .share a:hover,.rxh .share button:hover{border-color:#fff!important;color:#fff!important}
.rxh .share svg{color:inherit;fill:currentColor}
.rxh .btn{background:#fff!important;color:#141414!important;border:1px solid #fff!important;border-radius:2px!important;font-weight:600!important;box-shadow:none!important}
.rxh .btn:hover{background:transparent!important;color:#fff!important}
.rxh .btn.rxg{background:transparent!important;color:#fff!important;border-color:rgba(255,255,255,.55)!important}
.rxh .btn.rxg:hover{border-color:#fff!important}
.rxh span[style*="muted"]{color:rgba(255,255,255,.6)!important}
.rxh .rxb{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
.rxs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:30px 0 0;border-top:1px solid rgba(255,255,255,.16);border-bottom:1px solid rgba(255,255,255,.16)}
.rxs a{display:block;padding:18px 18px 16px 0;color:#fff!important;text-decoration:none}
.rxs a+a{padding-left:20px;border-left:1px solid rgba(255,255,255,.12)}
.rxs b{display:block;font:400 clamp(30px,3.4vw,44px)/1 var(--rx-serif);letter-spacing:-.01em}
.rxs span{display:block;margin-top:8px;font-size:13px;line-height:1.45;color:rgba(255,255,255,.62)}
.rxs a:hover span{color:#fff;text-decoration:underline;text-underline-offset:3px}
.rxh .rxn{margin:10px 0 0!important;font-size:12px!important;line-height:1.5!important;color:rgba(255,255,255,.45)!important}
.rxh .meta-line{color:rgba(255,255,255,.55)!important;font-size:13px!important}
/* kotak tanya dan tombol WA monokrom ala FA */
.ca-tanya,.us-tanya{border:1px solid var(--line)!important;border-left:2px solid #141414!important;border-radius:2px!important;background:#F7F7F5!important}
.ca-tanya .q a,.us-tanya .q a{border-radius:2px!important;border-color:#C9C9C4!important;color:#141414!important;background:#fff!important}
.ca-tanya .q a.w,.us-tanya .q a.w{background:#141414!important;border-color:#141414!important;color:#fff!important}
.bar{background:#141414!important;border-top-color:rgba(255,255,255,.1)!important}
.bar .btn{background:#fff!important;color:#141414!important;border-radius:2px!important}
main .tldr{background:#F7F7F5!important;border-left-color:#141414!important}
main .btn-wa,.prose .btn-wa{background:#141414;color:#fff;border-radius:2px}
@media(max-width:640px){.rxh{padding-top:40px;padding-bottom:34px}.rxs{grid-template-columns:1fr}.rxs a,.rxs a+a{padding:14px 0;border-left:0}.rxs a+a{border-top:1px solid rgba(255,255,255,.12)}
.rxh .sub,.rxh .lede,.rxh>p{font-size:16px!important}}
"""

# ---------------------------------------------------------------- util
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr", "path", "circle", "rect", "line", "polyline", "polygon", "use", "stop", "ellipse"}


class Bal(HTMLParser):
    def __init__(self):
        super().__init__()
        self.st, self.ok = [], True

    def handle_starttag(self, tag, a):
        if tag not in VOID:
            self.st.append(tag)

    def handle_startendtag(self, tag, a):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.st or self.st[-1] != tag:
            self.ok = False
        else:
            self.st.pop()


def balanced(s):
    p = Bal()
    p.feed(s)
    p.close()
    return p.ok and not p.st


def esc(s):
    return html.escape(s, quote=True)


def set_meta(t, title=None, desc=None):
    if title:
        t = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", t, count=1, flags=re.S)
        for p in ("og:title", "twitter:title"):
            t = re.sub(r'(<meta[^>]*(?:property|name)="%s"[^>]*content=")[^"]*(")' % p, lambda m: m.group(1) + esc(title) + m.group(2), t)
            t = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*(?:property|name)="%s")' % p, lambda m: m.group(1) + esc(title) + m.group(2), t)
    if desc:
        for p in ("description", "og:description", "twitter:description"):
            t = re.sub(r'(<meta[^>]*(?:property|name)="%s"[^>]*content=")[^"]*(")' % p, lambda m: m.group(1) + esc(desc) + m.group(2), t)
            t = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*(?:property|name)="%s")' % p, lambda m: m.group(1) + esc(desc) + m.group(2), t)
    return t


def fit(cands, n):
    for c in cands:
        if len(c) <= n:
            return c
    return None


STOPS = ["<!--ca-tanya-->", '<section class="ca-tanya"', '<div class="citylist"', '<div class="prose"', '<nav aria-label="Peta Isi"',
         "<h2", "<section", '<div class="tblwrap"', "<!--us-", "<!--ca-", '<div class="keys"', "<figure", "<aside", "<!--uq",
         "<details", '<div class="tx"', "<article", '<p class="tldr"', "<table", "<!--rx13", "<!--dhn", '<div class="dhn', "<ul", "<ol", "<!--fa-", '<div class="pf-map']


def wrap_hero(t, site):
    """Bungkus pembuka halaman (crumb s.d. sebelum isi) dengan <header class="rxh">."""
    if 'class="rxh"' in t:
        return t, True
    if site == "cariakuntan":
        m = re.search(r'<main class="wrap art">\s*', t)
    else:
        m = re.search(r'<article class="art"><div class="wrap">\s*', t)
    if not m:
        return t, False
    a = m.end()
    if not re.match(r'<(p|nav) class="crumb"', t[a:]):
        return t, False
    h1 = t.find("</h1>", a)
    if h1 < 0:
        return t, False
    ends = [t.find(s, h1) for s in STOPS]
    ends = [e for e in ends if e > 0]
    if not ends:
        return t, False
    b = min(ends)
    seg = t[a:b].rstrip()
    b = a + len(seg)
    if not balanced(seg):
        return t, False
    return t[:a] + '<header class="rxh">' + seg + "</header>" + t[b:], True


def add_body_class(t, cls):
    m = re.search(r"<body([^>]*)>", t)
    if not m:
        return t
    attrs = m.group(1)
    if re.search(r'class="[^"]*\b%s\b' % cls, attrs):
        return t
    if 'class="' in attrs:
        na = re.sub(r'class="', 'class="%s ' % cls, attrs, count=1)
    else:
        na = attrs + ' class="%s"' % cls
    return t[: m.start()] + "<body" + na + ">" + t[m.end():]


def link_css(t):
    if 'id="rx17-css"' in t:
        return t
    tag = f'<link href="/css/rx17.css?v={VER}" id="rx17-css" rel="stylesheet"/>'
    m = re.search(r'<link[^>]*id="rx13-css"[^>]*>', t)
    if m:
        return t[: m.end()] + tag + t[m.end():]
    return t.replace("</head>", tag + "</head>", 1)


TANYA_FIX = [
    ("Tanya Dulu ke Ananta, CPA</b>", "Tanya Dulu Sebelum Memilih</b>"),
    (" Tanyakan dulu ke Ananta, CPA. Gratis, dijawab langsung lewat WhatsApp.", " Pilih pertanyaan di bawah, pesan WhatsApp sudah tersusun. Diskusi awal tanpa biaya."),
    ("Gratis, dijawab langsung lewat WhatsApp.", "Pilih pertanyaan di bawah, pesan WhatsApp sudah tersusun. Diskusi awal tanpa biaya."),
    ("dijawab langsung lewat WhatsApp", "lewat WhatsApp"),
    ('<b class="t">Tanya Ananta, CPA</b>', '<b class="t">Punya Kasus Nyata?</b>'),
    (" Tanya Ananta, CPA dulu lewat WhatsApp, gratis.", " Diskusi awal lewat WhatsApp tanpa biaya."),
    (" Tanya Ananta, CPA lewat WhatsApp, gratis.", " Diskusi awal lewat WhatsApp tanpa biaya."),
    ("Tanyakan dulu kasus Anda ke Ananta, CPA lewat WhatsApp, gratis.", "Tanyakan dulu kasus Anda lewat WhatsApp, tanpa biaya."),
    ("Tanyakan ke Ananta, CPA. Pilih", "Tanyakan lewat WhatsApp. Pilih"),
    ("Untuk pertanyaan awal, Ananta, CPA menjawab gratis;", "Pertanyaan awal tanpa biaya;"),
    ("Tanya dulu ke Ananta, CPA lewat WhatsApp.", "Tanya dulu lewat WhatsApp."),
]


def fix_text(t):
    for a, b in TANYA_FIX:
        t = t.replace(a, b)
    # Tanyakan kasus Anda ke Ananta, CPA. -> tanpa nama di kalimat
    t = re.sub(r"Tanyakan kasus Anda ke Ananta, CPA\.", "Tanyakan kasus Anda lewat WhatsApp.", t)
    t = re.sub(r"pertanyaan pertama dijawab Ananta W\. Sasongko, CPA \(pernah direktur keuangan dan group CFO rumah sakit\)\.",
               "diskusi awal bersama tim FA Indonesia yang pernah memimpin keuangan rumah sakit.", t)
    t = t.replace("Pertanyaan dari kota mana pun dijawab Ananta, CPA lewat WhatsApp.", "Pertanyaan dari kota mana pun bisa dimulai lewat WhatsApp.")
    t = t.replace(">Tanya Ananta, CPA<", ">Chat Ananta, CPA<").replace('aria-label="Tanya Ananta, CPA"', 'aria-label="Chat Ananta, CPA"')
    return t


# ---------------------------------------------------------------- CA
def ca_city(slug):
    loc = L.resolve(slug)
    if not loc or loc["kind"] != "kota":
        return None
    f = L.facts(loc)
    return loc, f


def ca_strip(slug, name, f):
    off, prov = f["off"], f["prov_off"]
    items = []
    lab = {"kap": "KAP", "kja": "KJA", "kjpp": "KJPP"}
    for k in ("kap", "kja", "kjpp"):
        if off[k]:
            items.append(f'<a href="/kota/{slug}/{k}/"><b>{off[k]}</b><span>{lab[k]} berizin aktif di {esc(name)}</span></a>')
        else:
            items.append(f'<a href="/kota/{slug}/{k}/"><b>{prov[k]}</b><span>{lab[k]} aktif di {esc(f["prov"])}</span></a>')
    return ('<!--rx17s--><div class="rxs" aria-label="Jumlah kantor berizin">' + "".join(items) +
            '</div><p class="rxn">Sumber: registri Pusat Pembinaan Profesi Keuangan (PPPK) Kemenkeu, status aktif per November 2026.</p><!--/rx17s-->')


def ca_meta(kind, name, prov, f):
    off = f["off"]
    tot = sum(off.values())
    if kind == "hub":
        if not tot:
            return None, None
        ti = fit([f"Daftar KAP, KJA, KJPP di {name}: {tot} Kantor Berizin Aktif",
                  f"Daftar KAP, KJA, KJPP {name}: {tot} Kantor Berizin"], 65)
        de = fit([f"{tot} kantor berizin aktif di {name}: {off['kap']} KAP, {off['kja']} KJA, {off['kjpp']} KJPP (registri PPPK, November 2026). Bandingkan izin dan layanannya sebelum memilih.",
                  f"{tot} kantor berizin aktif di {name}: {off['kap']} KAP, {off['kja']} KJA, {off['kjpp']} KJPP (registri PPPK, November 2026)."], 158)
        return ti, de
    if kind == "konsultan-pajak":
        ti = fit([f"Konsultan Pajak {name}: SPT Badan, Coretax, SP2DK, Pemeriksaan",
                  f"Konsultan Pajak {name}: SPT Badan, Coretax, SP2DK",
                  f"Konsultan Pajak {name}: SPT Badan dan Coretax"], 65)
        de = fit([f"Cari konsultan pajak di {name}, {prov}: SPT badan, Coretax, SP2DK, dan pemeriksaan pajak. Cara memilih dan cek izin konsultan sebelum menunjuk.",
                  f"Cari konsultan pajak di {name}: SPT badan, Coretax, SP2DK, dan pemeriksaan pajak. Cara memilih dan cek izin konsultan sebelum menunjuk."], 158)
        return ti, de
    n = off[kind]
    if not n:
        return None, None
    full = {"kap": "Kantor Akuntan Publik", "kja": "Kantor Jasa Akuntansi", "kjpp": "Kantor Jasa Penilai Publik"}[kind]
    ab = kind.upper()
    ti = fit([f"Daftar {ab} {name}: {n} {full} Berizin Aktif", f"Daftar {ab} {name}: {n} {full} Berizin", f"Daftar {ab} {name}: {n} Kantor Berizin Aktif"], 65)
    use = {"kap": "Cek izin dan kelas KAP untuk bank, SABH, dan investor sebelum memilih.",
           "kja": "Pembukuan dan laporan keuangan siap bank; cek izin kantornya sebelum memilih.",
           "kjpp": "Appraisal aset dan penilaian bisnis untuk bank dan investor; cek izinnya dulu."}[kind]
    de = fit([f"{n} {ab} berizin aktif di {name}, {prov} menurut registri PPPK (November 2026). {use}",
              f"{n} {ab} berizin aktif di {name} menurut registri PPPK (November 2026). {use}",
              f"{n} {ab} berizin aktif di {name} menurut registri PPPK (November 2026)."], 158)
    return ti, de


def do_ca():
    site = "cariakuntan"
    base = os.path.join(OUT, site)
    files = glob.glob(base + "/**/*.html", recursive=True)
    city_pages = {}
    for d in sorted(glob.glob(base + "/kota/*/index.html")):
        slug = d.split("/")[-2]
        r = ca_city(slug)
        if r:
            city_pages[slug] = r
    meta_n = strip_n = hero_n = 0
    for fp in files:
        t0 = t = open(fp, encoding="utf-8").read()
        rel = os.path.relpath(fp, base).replace("\\", "/")
        t = link_css(t)
        t = fix_text(t)
        if rel != "index.html" and not re.match(r"(en|zh|hokkien)/index\.html$", rel):
            t, ok = wrap_hero(t, site)
            if ok:
                t = add_body_class(t, "rx17")
                hero_n += 1
        m = re.match(r"kota/([^/]+)/(?:(kap|kja|kjpp|konsultan-pajak)/)?index\.html$", rel)
        if m and m.group(1) in city_pages:
            slug, kind = m.group(1), (m.group(2) or "hub")
            loc, f = city_pages[slug]
            ti, de = ca_meta(kind, loc["name"], loc["prov"], f)
            if ti and de:
                t = set_meta(t, ti, de)
                meta_n += 1
            if kind != "konsultan-pajak" and 'class="rxh"' in t and "<!--rx17s-->" not in t:
                t = t.replace("</header><!--ca-tanya-->", "</header><!--ca-tanya-->", 1)
                i = t.find('<header class="rxh">')
                j = t.find("</header>", i)
                t = t[:j] + ca_strip(slug, loc["name"], f) + t[j:]
                strip_n += 1
        if t != t0:
            changed[site] += 1
            if not DRY:
                open(fp, "w", encoding="utf-8").write(t)
    print(f"CA: {len(files)} file, berubah {changed[site]}, hero {hero_n}, meta {meta_n}, strip {strip_n}")


# ---------------------------------------------------------------- US
SHORT = {
    "105": "Aset Dimiliki untuk Dijual dan Operasi Dihentikan", "106": "Eksplorasi dan Evaluasi Sumber Daya Mineral",
    "112": "Pengungkapan Kepentingan dalam Entitas Lain", "115": "Pendapatan dari Kontrak dengan Pelanggan",
    "118": "Penyajian dan Pengungkapan Laporan Keuangan", "119": "Entitas Anak tanpa Akuntabilitas Publik",
    "120": "Aset dan Liabilitas Regulatori", "208": "Kebijakan Akuntansi, Estimasi, dan Kesalahan",
    "220": "Hibah Pemerintah", "221": "Pengaruh Perubahan Kurs Valuta Asing", "226": "Program Manfaat Purnakarya",
    "228": "Investasi pada Asosiasi dan Ventura Bersama", "229": "Ekonomi Hiperinflasi",
    "237": "Provisi, Liabilitas dan Aset Kontinjensi", "239": "Instrumen Keuangan: Pengakuan dan Pengukuran",
    "338": "Kombinasi Bisnis Entitas Sepengendali", "370": "Aset dan Liabilitas Pengampunan Pajak",
    "401": "Penyajian Laporan Keuangan Syariah",
    "sa-200": "Tujuan Keseluruhan Auditor Independen", "sa-210": "Persetujuan Ketentuan Perikatan Audit",
    "sa-220": "Manajemen Mutu Audit Laporan Keuangan", "sa-240": "Tanggung Jawab Auditor atas Kecurangan",
    "sa-250": "Peraturan Perundang-undangan dalam Audit", "sa-260": "Komunikasi dengan Pihak Tata Kelola",
    "sa-265": "Komunikasi Defisiensi Pengendalian Internal", "sa-300": "Perencanaan Audit Laporan Keuangan",
    "sa-315": "Penilaian Risiko Kesalahan Penyajian Material", "sa-320": "Materialitas dalam Perencanaan dan Audit",
    "sa-330": "Respons Auditor terhadap Risiko yang Dinilai", "sa-402": "Audit Entitas Pengguna Organisasi Jasa",
    "sa-450": "Evaluasi Kesalahan Penyajian selama Audit", "sa-501": "Bukti Audit atas Unsur Pilihan",
    "sa-510": "Audit Tahun Pertama: Saldo Awal", "sa-540": "Audit Estimasi Akuntansi",
    "sa-600": "Audit Laporan Keuangan Grup", "sa-700": "Opini dan Laporan Auditor Independen",
    "sa-701": "Hal Audit Utama dalam Laporan Auditor", "sa-705": "Modifikasi Opini Auditor",
    "sa-706": "Paragraf Penekanan Suatu Hal dan Hal Lain", "sa-710": "Informasi Komparatif",
    "sa-720": "Tanggung Jawab Auditor atas Informasi Lain", "sa-800": "Audit Kerangka Bertujuan Khusus",
    "sa-805": "Audit Laporan Keuangan Tunggal dan Unsur Tertentu", "sa-810": "Perikatan Melaporkan Ikhtisar Laporan Keuangan",
    "smm-1": "Manajemen Mutu Kantor Akuntan Publik", "spa-3000": "Perikatan Asurans Selain Audit atau Reviu",
    "spa-3400": "Pemeriksaan Informasi Keuangan Prospektif", "spa-3402": "Asurans atas Pengendalian Organisasi Jasa",
    "spa-3410": "Asurans Pelaporan Gas Rumah Kaca", "spa-3420": "Asurans Informasi Keuangan Proforma",
    "spr-2400": "Reviu Laporan Keuangan Historis", "spr-2410": "Reviu Informasi Keuangan Interim",
}


def us_title(slug, h1):
    m = re.match(r"((?:PSAK|SA|SPA|SPR|SMM)\s+\d+)\s+(.*)$", h1)
    if not m:
        return None
    code, name = m.group(1), m.group(2)
    name = re.sub(r":\s*Ringkasan.*$", "", name).strip()
    short = SHORT.get(slug, name)
    sfx = ": Ringkasan dan Contoh CALK" if code.startswith("PSAK") else ": Ringkasan dan Poin Kunci"
    return fit([f"{code} {short}{sfx}", f"{code} {short}: Ringkasan", f"{code} {short}"], 65)


def do_us():
    site = "updatesak"
    base = os.path.join(OUT, site)
    files = glob.glob(base + "/**/*.html", recursive=True)
    hero_n = meta_n = btn_n = 0
    for fp in files:
        t0 = t = open(fp, encoding="utf-8").read()
        rel = os.path.relpath(fp, base).replace("\\", "/")
        t = link_css(t)
        t = fix_text(t)
        if rel != "index.html":
            t, ok = wrap_hero(t, site)
            if ok:
                t = add_body_class(t, "rx17")
                hero_n += 1
                if "<!--rx17b-->" not in t:
                    hm = re.search(r'<header class="top">.*?<a class="btn[^"]*" href="(https://wa\.me/[^"]+)"', t, re.S)
                    wa = hm.group(1) if hm else "https://wa.me/6282245260121"
                    btn = ('<!--rx17b--><div class="rxb"><a class="btn" href="%s" rel="noopener" target="_blank" data-us-q="hero">Chat Ananta, CPA</a>'
                           '<a class="btn rxg" href="/#dibantu">Dikerjakan Tim FA</a></div><!--/rx17b-->') % wa
                    i = t.find('<header class="rxh">')
                    j = t.find("</header>", i)
                    t = t[:j] + btn + t[j:]
                    btn_n += 1
        m = re.match(r"(psak|standar-audit)/([^/]+)/index\.html$", rel)
        if m:
            h = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
            if h:
                h1 = html.unescape(re.sub(r"<[^>]+>", "", h.group(1))).strip()
                ti = us_title(m.group(2), h1)
                if ti:
                    cur = re.search(r"<title>(.*?)</title>", t, re.S).group(1)
                    if html.unescape(cur) != ti:
                        t = set_meta(t, ti, None)
                        meta_n += 1
        if t != t0:
            changed[site] += 1
            if not DRY:
                open(fp, "w", encoding="utf-8").write(t)
    print(f"US: {len(files)} file, berubah {changed[site]}, hero {hero_n}, tombol {btn_n}, title {meta_n}")


def assets():
    for s in ("cariakuntan", "updatesak"):
        d = os.path.join(OUT, s)
        os.makedirs(os.path.join(d, "fonts"), exist_ok=True)
        os.makedirs(os.path.join(d, "css"), exist_ok=True)
        for fn in glob.glob(os.path.join(OUT, "faindonesia/fonts/newsreader-*")):
            dst = os.path.join(d, "fonts", os.path.basename(fn))
            if not os.path.exists(dst) and not DRY:
                shutil.copy2(fn, dst)
        dst = os.path.join(d, "img/fa-landscape.jpg")
        if not os.path.exists(dst) and not DRY:
            shutil.copy2(os.path.join(OUT, "faindonesia/img/fa/landscape.jpg"), dst)
        cp = os.path.join(d, "css/rx17.css")
        if not DRY and (not os.path.exists(cp) or open(cp).read() != CSS):
            open(cp, "w").write(CSS)


if __name__ == "__main__":
    assets()
    do_ca()
    do_us()
    if DRY:
        print("(dry run)")
