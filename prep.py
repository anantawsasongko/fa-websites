import os, re, shutil, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.environ.get("KIT_ROOT", HERE)
OUT = os.path.join(M, "out")
FA = os.path.join(M, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
JUP = os.path.join(M, "FA-Jupiter_SIAP-UPLOAD-v6")
SAT = os.path.join(M, "FA-Saturn_SIAP-UPLOAD-v4")
VEN = os.path.join(M, "FA-Venus_SIAP-UPLOAD-v2")
KJA = os.path.join(M, "KJA-Farhani_site_v12-netlify-primary")
CA = os.path.join(M, "cariakuntan", "site")
FEED = json.load(open(os.path.join(M, "cariakuntan", "feed.json")))

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)

def feed_block(title="Berita Terkini", n=10, accent="#141414", font="inherit"):
    items = "".join(
        f'<li><a href="{html.escape(l)}" target="_blank" rel="noopener nofollow">{html.escape(t)}</a><span>{html.escape(s)} · {d}</span></li>'
        for d, t, l, s in FEED[:n])
    return f'''<section class="ca-feed" aria-label="{title}"><style>
.ca-feed{{max-width:1080px;margin:40px auto;padding:22px 22px 10px;border:1px solid rgba(127,127,127,.25);border-radius:10px;font-family:{font}}}
.ca-feed h2{{margin:0 0 4px;font-size:1.25rem}}.ca-feed p{{margin:0 0 10px;font-size:.82rem;opacity:.7}}
.ca-feed ul{{list-style:none;margin:0;padding:0}}.ca-feed li{{display:grid;gap:2px;padding:10px 0;border-top:1px solid rgba(127,127,127,.2)}}
.ca-feed li a{{color:inherit;text-decoration:none;font-weight:500}}.ca-feed li a:hover{{color:{accent};text-decoration:underline}}
.ca-feed li span{{font-size:.78rem;opacity:.65}}
@media (max-width:720px){{.ca-feed{{margin:28px 16px}}}}
</style><h2>{title}</h2><p>Berita bisnis, pajak, perbankan, dan pasar modal pilihan dari media nasional. Diperbarui otomatis.</p><ul>{items}</ul></section>'''

def inject_before_footer(path, block):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'<section class="ca-feed".*?</section>', "", s, flags=re.S)
    i = s.rfind("<footer")
    if i < 0: i = s.rfind("</body>")
    s = s[:i] + block + "\n" + s[i:]
    open(path, "w", encoding="utf-8").write(s)

# ---------- cariakuntan ----------
shutil.copytree(CA, os.path.join(OUT, "cariakuntan"))
r = os.path.join(OUT, "cariakuntan", "_redirects")
open(r, "w").write("")  # www -> apex handled by Cloudflare redirect rule

# ---------- FA main (with apps merged in, same URLs as Netlify proxy) ----------
fa = os.path.join(OUT, "faindonesia")
shutil.copytree(FA, fa)
for src, sub in [(JUP, "audit-ready"), (SAT, "saturn"), (VEN, "cek-psak-118")]:
    shutil.copytree(os.path.join(src, sub), os.path.join(fa, sub), dirs_exist_ok=True)
for root, _, files in os.walk(os.path.join(SAT, "img")):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), SAT)
        dst = os.path.join(fa, rel)
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(os.path.join(root, f), dst)
open(os.path.join(fa, "_redirects"), "w").write(
"""# Cloudflare Pages. www -> apex diatur lewat Redirect Rule di zone faindonesia.co.id.
# FA Apps digabung ke project ini saat deploy (folder audit-ready, saturn, cek-psak-118).
/saturnus/*      /saturn/:splat      301
/jupiter/*       /audit-ready/:splat 301
/unduhan/*       /buku/#unduhan      301
/unduhan         /buku/#unduhan      301
""")
# nav (30 Okt 2026): Apps, Layanan, Eksplor, Kontak
idx = os.path.join(fa, "index.html")
s = open(idx, encoding="utf-8").read()
old_nav = re.search(r'<nav aria-label="Navigasi utama" class="links">.*?</nav>', s, re.S).group(0)
new_nav = ('<nav aria-label="Navigasi utama" class="links"> <a data-i18n="kbrd" href="/">Beranda</a> <a data-i18n="kapp" href="/apps/">Apps</a> '
           '<a data-i18n="k2" href="/layanan/">Layanan</a> <a data-i18n="kwws" href="/artikel/">Eksplor</a> '
           '<a data-i18n="k321" href="#kontak">Kontak</a> </nav>')  # 30 Okt 2026: 4 tab saja; E-Book, Cari Akuntan, Update SAK lewat Eksplor, beranda, dan footer
s = s.replace(old_nav, new_nav)
s = s.replace(' data-netlify="true" netlify-honeypot="bot-field"', '')
open(idx, "w", encoding="utf-8").write(s)
NAV_CSS = '<style id="nav4">@media (max-width:820px){nav.links{display:grid!important;grid-template-columns:repeat(5,1fr)!important;gap:0!important;overflow:visible!important;width:100%}nav.links a{text-align:center;white-space:nowrap;font-size:13px!important;padding:8px 0!important;letter-spacing:0!important}}@media (max-width:370px){nav.links a{font-size:11.8px!important}}</style>'
# same nav on other FA pages that carry the main nav
for root, _, files in os.walk(fa):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f)
        t = open(p, encoding="utf-8").read()
        m = re.search(r'<nav aria-label="Navigasi utama" class="links">.*?</nav>', t, re.S)
        if m and m.group(0) != new_nav:
            # pages outside home use absolute anchors
            nav2 = new_nav.replace('href="#layanan"', 'href="/#layanan"').replace('href="#kontak"', 'href="/#kontak"') if p != idx else new_nav
            t = t.replace(m.group(0), nav2)
        t2 = re.sub(r'<a class="btn solid sm" data-i18n="k8" href="/?#kontak">Kontak</a>', '', t)
        t2 = re.sub(r'<style id="nav4">.*?</style>', '', t2, flags=re.S)
        if '<li><a href="/buku/">Toko Buku</a></li>' in t2 and 'updatesak.com/">Update SAK</a></li>' not in t2:
            t2 = t2.replace('<li><a href="/buku/">Toko Buku</a></li>', '<li><a href="/buku/">Toko Buku</a></li><li><a href="https://cariakuntan.com/">Cari Akuntan</a></li><li><a href="https://updatesak.com/">Update SAK</a></li>', 1)
        if '<div class="chips2">' in t2 and 'chips2"><a href="/buku/">' not in t2:
            t2 = t2.replace('<div class="chips2">', '<div class="chips2"><a href="/buku/">E-Book</a><a href="https://cariakuntan.com/" target="_blank" rel="noopener">Cari Akuntan</a><a href="https://updatesak.com/" target="_blank" rel="noopener">Update SAK</a>', 1)
        if 'Navigasi utama' in t2 and 'id="nav4"' not in t2:
            t2 = t2.replace('</head>', NAV_CSS + '</head>', 1)
            if '"kbrd": "Home"' not in t2: t2 = t2.replace('"en": {', '"en": {"kbrd": "Home", "kapp": "Apps", "kebk": "E-Books", "kcak": "Find Accountants", "kusak": "SAK Updates", "kwws": "Explore", ').replace('"zh": {', '"zh": {"kbrd": "首页", "kapp": "应用", "kebk": "电子书", "kcak": "找会计师", "kusak": "SAK 更新", "kwws": "探索", ')
        if m or t2 != t: open(p, "w", encoding="utf-8").write(t2)
# beranda FA dibuat ringkas (25 Okt 2026): berita hanya di tab Wawasan
if os.path.exists(os.path.join(fa, "artikel", "index.html")):
    inject_before_footer(os.path.join(fa, "artikel", "index.html"), feed_block(n=20, font="Poppins,sans-serif"))

# ---------- QRIS donasi sukarela di semua layanan gratis (25 Okt 2026) ----------
DON_JS = os.path.join(M, "shared", "donasi.js"); DON_IMG = os.path.join(M, "shared", "qris-fa-indonesia.jpg")
def add_donasi(site_root, pages, cfg):
    os.makedirs(os.path.join(site_root, "js"), exist_ok=True); os.makedirs(os.path.join(site_root, "img"), exist_ok=True)
    shutil.copy2(DON_JS, os.path.join(site_root, "js", "donasi.js")); shutil.copy2(DON_IMG, os.path.join(site_root, "img", "qris-fa-indonesia.jpg"))
    for rel in pages:
        pth = os.path.join(site_root, rel)
        if not os.path.exists(pth): continue
        t = open(pth, encoding="utf-8").read()
        if "/js/donasi.js" in t: continue
        t = t.replace("</body>", "<script>window.FA_DONASI=" + cfg + "</script><script src=\"/js/donasi.js\"></script></body>", 1)
        open(pth, "w", encoding="utf-8").write(t)
add_donasi(fa, ["buku/index.html"], "{guards:[{sel:'#unduhan a.dl:not([href*=\"fa-consult-\"])',key:'materi'}]}")
add_donasi(fa, ["cek-kapasitas-kredit/index.html", "index.html", "kalkulator-dscr/index.html", "simulasi-plafon-kredit-usaha/index.html", "cek-kelayakan-ipo/index.html"], "{guards:[{sel:'#kk_go',key:'venus-kredit',skip:function(){var p=document.getElementById('kk_pt'),m=document.getElementById('kk_em');if(!(p&&m&&p.value.trim().length>2&&/^[^@\\s]+@[^@\\s]+\\.[^@\\s]{2,}$/.test(m.value.trim())))return true;return ['kk_rev','kk_ebit','kk_da','kk_eq','kk_os','kk_ds'].some(function(i){return !document.getElementById(i).value.trim()})}}]}")
add_donasi(fa, ["cek-psak-118/index.html"], "{guards:[{sel:'#btnXlsx,[data-tab=\"hasil\"]',key:'venus-psak118'}]}")
add_donasi(fa, ["audit-ready/index.html"], "{guards:[{sel:'#btnXlsx,[data-act=\"calkdoc\"]',key:'jupiter',skip:function(){try{return !!localStorage.getItem('fa-auditready-v1-lic')}catch(e){return false}}}]}")
add_donasi(os.path.join(OUT, "cariakuntan"), ["index.html", "en/index.html", "zh/index.html", "hokkien/index.html"],
    "{accent:'#1F5BFF',accentInk:'#fff',guards:[{sel:'#f_go1',key:'screening',skip:function(){var p=document.getElementById('f_pt');return !(p&&p.value.trim().length>2)}}]}")

# ---------- pembayaran online Midtrans (27 Okt 2026): worker hanya untuk /api/* ----------
for f in ("_worker.js", "_routes.json"):
    shutil.copy2(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared", "pay", f), os.path.join(fa, f))

# ---------- apps standalone projects (for testing; public URLs stay on faindonesia.co.id) ----------
for name, src, sub in [("faindonesia-jupiter", JUP, "audit-ready"), ("faindonesia-saturn", SAT, "saturn"), ("faindonesia-venus", VEN, "cek-psak-118")]:
    d = os.path.join(OUT, name); shutil.copytree(src, d)
    open(os.path.join(d, "_redirects"), "w").write(f"/  https://faindonesia.co.id/{sub}/  301\n")
    open(os.path.join(d, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")

# ---------- faindonesia-apps (legacy redirect + host /files supaya zip FA < 10MB) ----------
d = os.path.join(OUT, "faindonesia-apps"); os.makedirs(d)
shutil.move(os.path.join(fa, "files"), os.path.join(d, "files"))
open(os.path.join(d, "_headers"), "w").write("/files/*\n  Cache-Control: public, max-age=604800\n/files/cv/*\n  X-Robots-Tag: noindex, nofollow, noarchive\n  Cache-Control: no-cache\n")
open(os.path.join(d, "_redirects"), "w").write("/  https://faindonesia.co.id/apps/  301\n")
open(os.path.join(d, "robots.txt"), "w").write("User-agent: *\nAllow: /files/\nDisallow: /files/cv/\n")
# saturn/kk dilayani dari project faindonesia-saturn
shutil.rmtree(os.path.join(fa, "saturn", "kk"), ignore_errors=True)
with open(os.path.join(fa, "_redirects"), "a") as f:
    f.write("/files/*      https://faindonesia-apps.pages.dev/files/:splat        302\n")
    f.write("/saturn/kk/*  https://faindonesia-saturn.pages.dev/saturn/kk/:splat  302\n")
open(os.path.join(d, "index.html"), "w").write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=https://faindonesia.co.id/apps/"><link rel="canonical" href="https://faindonesia.co.id/apps/"><title>FA Apps</title><a href="https://faindonesia.co.id/apps/">FA Apps</a>')

# ---------- KJA ----------
k = os.path.join(OUT, "kja-farhani"); shutil.copytree(KJA, k)
for root, _, files in os.walk(k):
    for f in files:
        if f.endswith((".html", ".xml", ".txt", ".json", ".js", ".css")):
            p = os.path.join(root, f)
            t = open(p, encoding="utf-8", errors="ignore").read()
            if "kja-farhani.netlify.app" in t:
                open(p, "w", encoding="utf-8").write(t.replace("kja-farhani.netlify.app", "kja-farhani.pages.dev"))
inject_before_footer(os.path.join(k, "index.html"), feed_block())
if os.path.exists(os.path.join(k, "artikel", "index.html")):
    inject_before_footer(os.path.join(k, "artikel", "index.html"), feed_block(n=20))

# ---------- updatesak.com (project Cloudflare ke-8, 27 Okt 2026) ----------
import subprocess as _sp; _sp.run(["python3", os.path.join(M, "updatesak", "build_seo.py")], check=True)
_sp.run(["python3", os.path.join(M, "updatesak", "build_materi.py")], check=True)
_sp.run(["python3", os.path.join(M, "updatesak", "build_sa.py")], check=True)
_sp.run(["python3", os.path.join(M, "updatesak", "build_landing.py")], check=True)
_sp.run(["python3", os.path.join(M, "updatesak", "build_jadwal.py")], check=True)
_sp.run(["python3", os.path.join(M, "updatesak", "build_dosen.py")], check=True)
US = os.path.join(M, "updatesak", "site")
u = os.path.join(OUT, "updatesak"); shutil.copytree(US, u)
inject_before_footer(os.path.join(u, "eksplor", "index.html"), feed_block(n=12, accent="#0B6E4F"))
add_donasi(u, [os.path.relpath(os.path.join(_d, "index.html"), u) for _d, _, _fs in os.walk(os.path.join(u, "materi")) if "index.html" in _fs],
    "{accent:'#1F5BFF',accentInk:'#fff',guards:[{sel:'a.dl',key:'materi-updatesak'}]}")

# ---------- lencana keamanan data FA Secure / CariAkuntan Secure / UpdateSAK Secure (27 Okt 2026) ----------
SEC_JS = os.path.join(M, "shared", "secure.js")
def add_secure(site_root, pages, cfg):
    os.makedirs(os.path.join(site_root, "js"), exist_ok=True); shutil.copy2(SEC_JS, os.path.join(site_root, "js", "secure.js"))
    for rel in pages:
        pth = os.path.join(site_root, rel)
        if not os.path.exists(pth): continue
        t = open(pth, encoding="utf-8").read()
        if "/js/secure.js" in t: continue
        _sv = __import__("hashlib").md5(open(SEC_JS, "rb").read()).hexdigest()[:8]
        t = t.replace("</body>", "<script>window.FA_SECURE=" + cfg + "</script><script src=\"/js/secure.js?v=" + _sv + "\"></script></body>", 1)
        open(pth, "w", encoding="utf-8").write(t)
add_secure(fa, ["index.html", "cek-kapasitas-kredit/index.html", "kalkulator-dscr/index.html", "simulasi-plafon-kredit-usaha/index.html", "cek-kelayakan-ipo/index.html"],
    "{brand:'fa',mode:'send',at:[{sel:'#kk',pos:'beforebegin'}]}")
add_secure(fa, ["cek-psak-118/index.html"], "{brand:'fa',mode:'local',at:[{sel:'header.bar',pos:'afterend',cls:'bar'}]}")
add_secure(fa, ["audit-ready/index.html"], "{brand:'fa',mode:'drive',at:[{sel:'header.bar',pos:'afterend',cls:'bar'}]}")
add_secure(fa, ["saturn/index.html"], "{brand:'fa',mode:'drive',at:[{sel:'header.top',pos:'afterend',cls:'bar'}]}")
add_secure(os.path.join(OUT, "cariakuntan"), ["index.html", "en/index.html", "zh/index.html", "hokkien/index.html", "screening/index.html"],
    "{brand:'ca',mode:'send',at:[{sel:'#screening',pos:'beforebegin'}]}")
add_secure(u, ["index.html"], "{brand:'us',mode:'local',at:[{sel:'#kalkulator .calc',pos:'beforebegin'}]}")
import hashlib as _hl
_ver = {f: _hl.md5(open(os.path.join(u, f), "rb").read()).hexdigest()[:8] for f in ("css/style.css", "js/app.js", "js/sak-data.js")}
for _d, _, _fs in os.walk(u):
    for _f in _fs:
        if not _f.endswith(".html"): continue
        _p = os.path.join(_d, _f); _t = open(_p, encoding="utf-8").read(); _o = _t
        for _k, _v in _ver.items():
            _t = re.sub(r'"/' + re.escape(_k) + r'(\?v=[0-9a-f]+)?"', '"/' + _k + '?v=' + _v + '"', _t)
        if _t != _o: open(_p, "w", encoding="utf-8").write(_t)
with open(os.path.join(u, "_headers"), "a") as _h:
    _h.write("\n/*.html\n  Cache-Control: public, max-age=0, must-revalidate\n/\n  Cache-Control: public, max-age=0, must-revalidate\n/css/*\n  Cache-Control: public, max-age=31536000, immutable\n/js/*\n  Cache-Control: public, max-age=31536000, immutable\n")

# ---------- FA: font body Georgia (30 Okt 2026), ganti EB Garamond yang tipis di layar; judul tetap Times ----------
FONT_CSS = '<style id="fa-font">:root{--serif:Georgia,"Noto Serif","Times New Roman",serif}p,.plan>p:not(.cmph),.note,.arsip li span:not(.yr),.cmp dd,.feerow span,.sysnote{font-size:1.05em;line-height:1.65}.art p,.art li{font-size:17.5px!important;line-height:1.72!important}.dl p:not(.cmph){font-size:16px}</style>'
for _r, _, _fs in os.walk(fa):
    for _f in _fs:
        if not _f.endswith(".html"): continue
        _p = os.path.join(_r, _f); _t = open(_p, encoding="utf-8").read()
        if 'id="fa-font"' in _t or "</head>" not in _t or "--serif" not in _t: continue
        open(_p, "w", encoding="utf-8").write(_t.replace("</head>", FONT_CSS + "</head>", 1))

# ---------- favicon CariAkuntan + UpdateSAK (Safari/Chrome/iOS): ico, png, svg, apple-touch (28 Okt 2026) ----------
_IC = os.path.join(M, "shared", "icons")
for _proj, _k in (("cariakuntan", "ca"), ("updatesak", "us")):
    _d = os.path.join(OUT, _proj)
    if not os.path.isdir(_d): continue
    for _src, _dst in ((f"{_k}.ico", "favicon.ico"), (f"{_k}.svg", "favicon.svg"), (f"{_k}-32.png", "favicon-32.png"), (f"{_k}-192.png", "favicon-192.png"), (f"{_k}-512.png", "favicon-512.png"), (f"{_k}-180.png", "apple-touch-icon.png")):
        shutil.copy(os.path.join(_IC, _src), os.path.join(_d, _dst))
    _tags = '<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">'
    for _r, _, _fs in os.walk(_d):
        for _f in _fs:
            if not _f.endswith(".html"): continue
            _p = os.path.join(_r, _f); _t = open(_p, encoding="utf-8").read()
            if "apple-touch-icon" in _t or "</head>" not in _t: continue
            _t2 = re.sub(r'<link[^>]*rel="icon"[^>]*>\s*', "", _t)
            _t2 = _t2.replace("</head>", _tags + "</head>", 1)
            open(_p, "w", encoding="utf-8").write(_t2)
    print("favicon", _proj)

for n in sorted(os.listdir(OUT)):
    cnt = sum(len(f) for _, _, f in os.walk(os.path.join(OUT, n)))
    print(n, cnt)

# ---------- anti duplikat SEO: *.pages.dev noindex untuk project yang punya domain sendiri ----------
for proj in ["cariakuntan", "faindonesia", "faindonesia-jupiter", "faindonesia-saturn", "faindonesia-venus", "updatesak"]:
    h = os.path.join(OUT, proj, "_headers")
    old = open(h).read() if os.path.exists(h) else ""
    extra = f"\n\nhttps://{proj}.pages.dev/*\n  X-Robots-Tag: noindex\n"
    if proj in ("faindonesia", "cariakuntan"):
        extra += f"\nhttps://{proj}-web.pages.dev/*\n  X-Robots-Tag: noindex\n"
    open(h, "w").write(old.rstrip() + extra)

# ---------- redirect-only untuk project Netlify lama (dipakai sekali, bukan deploy rutin) ----------
NR = os.path.join(M, "netlify-redirect")
if os.path.exists(NR): shutil.rmtree(NR)
for name, target in [("kja-farhani", "https://kja-farhani.pages.dev"), ("faindonesia", "https://faindonesia.co.id"), ("cariakuntan", "https://cariakuntan.com")]:
    d = os.path.join(NR, name); os.makedirs(d)
    open(os.path.join(d, "_redirects"), "w").write(f"/*  {target}/:splat  301!\n")
    open(os.path.join(d, "index.html"), "w").write(f'<!doctype html><meta charset="utf-8"><link rel="canonical" href="{target}/"><meta http-equiv="refresh" content="0;url={target}/"><a href="{target}/">{target}</a>')
    shutil.make_archive(d, "zip", d)

# ---------- Lead tracking + CTA silang (26 Okt 2026) ----------
GA_ID = "G-09VZKH3JRJ"
GA_TAG = ('<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA_ID + '"></script>'
          '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","' + GA_ID + '");</script>')
LEAD_JS = os.path.join(M, "shared", "lead.js")
WA_KREDIT = "https://wa.me/6282245260121?text=" + "Halo%20FA%20Indonesia%2C%20saya%20ingin%20konsultasi%20tentang%20pendampingan%20kredit%20bank."
CTA = ('<section class="fa-cta" aria-label="Konsultasi"><style>'
       '.fa-cta{width:min(1080px,calc(100% - 32px));box-sizing:border-box;margin:40px auto 0;padding:26px 24px;border-radius:8px;background:var(--surface,#1e1e1e);border:1px solid var(--line,#2f2f2f);color:var(--ink,#fff);font-family:inherit}'
       '.fa-cta h2{margin:0 0 6px;font-size:1.3rem;color:inherit}.fa-cta p{margin:0 0 16px;opacity:.85;font-size:.95rem;line-height:1.55}'
       '.fa-cta .b{display:flex;flex-wrap:wrap;gap:10px}.fa-cta a{display:inline-block;padding:11px 18px;border-radius:8px;font-weight:600;text-decoration:none;font-size:.92rem}'
       '.fa-cta a.w{background:var(--ink,#fff);color:var(--paper,#171717)}.fa-cta a.l{border:1px solid rgba(127,127,127,.45);color:inherit}.fa-cta a.l:hover{background:rgba(127,127,127,.14)}'
       '@media (max-width:720px){.fa-cta{margin-top:28px;padding:22px 18px}}</style>'
       '<h2>Mau Ajukan Kredit Bank atau Cari Investor?</h2>'
       '<p>Kami cek dulu rasio dan laporan keuangan perusahaan Anda, supaya pengajuan tidak ditolak dan biaya audit tidak terbuang. Diskusi awal gratis.</p>'
       '<div class="b"><a class="w" href="' + WA_KREDIT + '" target="_blank" rel="noopener">Konsultasi Kredit via WhatsApp</a>'
       '<a class="l" href="/konsultan-kredit-bank/">Lihat Layanan Kredit Bank</a>'
       '<a class="l" href="https://cariakuntan.com/screening/" target="_blank" rel="noopener">Screening Rasio Gratis</a></div></section>')

def add_lead(site_root, cta_dirs=()):
    os.makedirs(os.path.join(site_root, "js"), exist_ok=True)
    shutil.copy2(LEAD_JS, os.path.join(site_root, "js", "lead.js"))
    n = 0
    for root, _, files in os.walk(site_root):
        for f in files:
            if not f.endswith(".html"): continue
            p = os.path.join(root, f); t = open(p, encoding="utf-8").read()
            if "</body>" not in t or 'http-equiv="refresh"' in t: continue
            o = t
            if "googletagmanager.com/gtag/js" not in t and "</head>" in t:
                t = t.replace("</head>", GA_TAG + "</head>", 1)
            if "/js/lead.js" not in t:
                t = t.replace("</body>", '<script src="/js/lead.js" defer></script></body>', 1)
            rel = os.path.relpath(p, site_root).replace(os.sep, "/")
            t = re.sub(r'<section class="fa-cta".*?</section>\n?', "", t, flags=re.S)
            if cta_dirs and any(rel.startswith(d) for d in cta_dirs) and "konsultan-kredit-bank" not in rel:
                i = t.rfind("<footer"); i = i if i >= 0 else t.rfind("</body>")
                t = t[:i] + CTA + "\n" + t[i:]
            if t != o: open(p, "w", encoding="utf-8").write(t); n += 1
    return n
print("lead fa", add_lead(fa, cta_dirs=("artikel/", "buku/", "laporan-tahunan-pt/", "laporan-keuangan-umkm/", "jasa-penyusunan-laporan-keuangan/", "konsultan-persiapan-ipo/")))
print("lead ca", add_lead(os.path.join(OUT, "cariakuntan")))
print("lead kja", add_lead(k))

# ---------- Title Case judul dan poin (aturan Bos, 25 Okt 2026) ----------
import sys as _sys; _sys.path.insert(0, M)
import titlecase as _tcm
for _n in ("faindonesia", "cariakuntan", "kja-farhani", "updatesak"):
    _p = os.path.join(OUT, _n)
    if os.path.isdir(_p): print("titlecase", _n, _tcm.run(_p))

# ---------- backlink silang ke UpdateSAK (27 Okt 2026) ----------
US_BOX = ('<aside class="us-x" style="max-width:1080px;margin:32px auto;padding:20px 22px;border:1px solid #c9d6ff;background:#eef3ff;'
          'font-family:inherit;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between">'
          '<div style="max-width:60ch"><b style="display:block;font-size:1.05rem;margin-bottom:4px">Cek PSAK Yang Berlaku dan Susun CALK Otomatis</b>'
          '<span style="font-size:.9rem;opacity:.8">Kalkulator gratis UpdateSAK: masukkan neraca dan laba rugi, ketahui kerangka SAK dan PSAK per akun, '
          'lalu salin CALK format auditor ke Word.</span></div>'
          '<a href="https://updatesak.com/{path}" style="background:#1F5BFF;color:#fff;padding:11px 18px;font-weight:600;text-decoration:none;border-radius:4px">Buka UpdateSAK</a></aside>')
_n = 0
for _d, _, _fs in os.walk(os.path.join(OUT, "faindonesia", "artikel")):
    _slug = os.path.basename(_d)
    if "index.html" not in _fs or not re.search(r"psak|isak|sak-|calk|laporan-keuangan", _slug): continue
    _p = os.path.join(_d, "index.html"); _t = open(_p, encoding="utf-8").read()
    if "us-x" in _t: continue
    _m = re.search(r"psak-(\d{3})", _slug)
    _path = f"psak/{_m.group(1)}/" if _m and os.path.isdir(os.path.join(OUT, "updatesak", "psak", _m.group(1))) else ""
    _i = _t.rfind("<footer"); _i = _i if _i >= 0 else _t.rfind("</body>")
    open(_p, "w", encoding="utf-8").write(_t[:_i] + US_BOX.format(path=_path) + "\n" + _t[_i:]); _n += 1
print("backlink updatesak dari FA", _n)

# ---------- Artikel Lainnya bergambar (28 Okt 2026) ----------
_sys.path.insert(0, os.path.join(M, "shared")); import related as _rel
print("related fa", _rel.add_related(os.path.join(OUT, "faindonesia"), "fa"))
print("related ca", _rel.add_related(os.path.join(OUT, "cariakuntan"), "ca"))
print("related us", _rel.add_related(os.path.join(OUT, "updatesak"), "us", extra_dirs=("update-psak-2026",)))
import poster as _po
print("og artikel fa", _po.apply(os.path.join(OUT, "faindonesia"), "fa", "https://faindonesia.co.id"))
print("og artikel ca", _po.apply(os.path.join(OUT, "cariakuntan"), "ca", "https://cariakuntan.com"))
_SJ = os.path.join(M, "shared", "share.js")
for _n in ("faindonesia", "cariakuntan", "updatesak"): print("share", _n, _po.add_share_js(os.path.join(OUT, _n), _SJ))

# ---------- Gelar lengkap Ananta di semua situs (28 Okt 2026, permintaan Bos) ----------
GELAR = "S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP"
_G = [
 (re.compile(r"(?<!\(C\) )Ananta (W\.|Wahyu) Sasongko, S\.E\., M\.S\.A\., Ak\., CPA, CTT, FMVA, FPAP"), r"Dr. (C) Ananta \1 Sasongko, " + GELAR),
 (re.compile(r"(?<!\(C\) )Ananta (W\.|Wahyu) Sasongko, S\.E\., M\.S\.A\., Ak\., CPA(?!, CTT)"), r"Dr. (C) Ananta \1 Sasongko, " + GELAR),
 (re.compile(r"(?<!\(C\) )Ananta (W\.|Wahyu) Sasongko, CPA, FMVA, FPAP"), r"Dr. (C) Ananta \1 Sasongko, " + GELAR),
 (re.compile(r"(?<!\(C\) )Ananta (W\.|Wahyu) Sasongko, CPA(?!, (?:FMVA|CTT))"), r"Dr. (C) Ananta \1 Sasongko, " + GELAR),
]
_ng = 0
for _n in ("faindonesia", "cariakuntan", "kja-farhani", "updatesak", "faindonesia-jupiter", "faindonesia-saturn", "faindonesia-venus"):
    for _d, _, _fs in os.walk(os.path.join(OUT, _n)):
        if os.sep + "files" in _d: continue
        for _f in _fs:
            if not _f.endswith((".html", ".txt", ".xml", ".json", ".js")): continue
            _p = os.path.join(_d, _f)
            try: _t = open(_p, encoding="utf-8").read()
            except UnicodeDecodeError: continue
            _o = _t
            for _rx, _rep in _G: _t = _rx.sub(_rep, _t)
            if '"honorificPrefix"' not in _t:
                _t = re.sub(r'("@type": "Person", "@id": "https://faindonesia\.co\.id/ananta-w-sasongko/#person", "name": "Ananta W\. Sasongko")',
                            r'\1, "honorificPrefix": "Dr. (C)"', _t)
            if _t != _o: open(_p, "w", encoding="utf-8").write(_t); _ng += 1
print("gelar lengkap:", _ng, "file")

# ---------- backlink merek "Update SAK" di footer CariAkuntan (31 Okt 2026) ----------
for _r, _, _fs in os.walk(os.path.join(OUT, "cariakuntan")):
    for _f in _fs:
        if not _f.endswith(".html"): continue
        _p = os.path.join(_r, _f); _t = open(_p, encoding="utf-8").read()
        if "updatesak.com/\">Update SAK</a>" in _t or 'Kebijakan Privasi</a></span>' not in _t: continue
        _t = _t.replace(' · <a href="https://faindonesia.co.id/kebijakan-privasi/">Kebijakan Privasi</a></span>', ' · <a href="https://updatesak.com/">Update SAK</a> · <a href="https://faindonesia.co.id/kebijakan-privasi/">Kebijakan Privasi</a></span>', 1)
        open(_p, "w", encoding="utf-8").write(_t)

# ---------- Beranda jelas untuk pemilik usaha + bar ekosistem 3 situs (31 Okt 2026) ----------
ECO_CSS = ('<style id="ecobar-css">.ecobar{background:#0B0B0C;color:#cfcfcf;font:500 12.5px/1.2 Poppins,system-ui,sans-serif;position:relative;z-index:60}'
  '.ecobar .in{max-width:1180px;margin:0 auto;padding:7px 16px;display:flex;gap:6px 18px;align-items:center;justify-content:center;flex-wrap:wrap}'
  '.ecobar a{color:#cfcfcf;text-decoration:none;white-space:nowrap}.ecobar a b{color:#fff;font-weight:600}.ecobar a.on{color:#fff;border-bottom:1px solid #fff}'
  '.ecobar span{opacity:.55}@media(max-width:600px){.ecobar .in{gap:4px 16px;font-size:12px;flex-wrap:nowrap}.ecobar .lbl,.ecobar a span{display:none}}</style>')
def ECO(cur):
    it = [("fa", "https://faindonesia.co.id/", "FA Indonesia", "Kredit, Investor, IPO"), ("ca", "https://cariakuntan.com/", "Cari Akuntan", "KAP, KJA, Pajak"), ("us", "https://updatesak.com/", "Update SAK", "Standar Akuntansi")]
    return ('<div class="ecobar" id="ecobar"><div class="in"><span class="lbl">Ekosistem FA:</span>' + "".join(
        f'<a href="{u}"{" class=on" if k == cur else ""}><b>{n}</b> <span>{d}</span></a>' for k, u, n, d in it) + '</div></div>')
WANT_CSS = ('<style id="want-css">'
  '.want{padding:34px 16px 38px;background:var(--wbg);color:var(--wfg);border-top:1px solid var(--wln);border-bottom:1px solid var(--wln)}'
  '.want .in{max-width:1080px;margin:0 auto}.want h2:after,.want h2:before{display:none!important}'
  '.want .hd{display:flex;align-items:center;gap:12px;margin:0 0 18px}'
  '.want .hd:before{content:"";width:28px;height:1px;background:currentColor;opacity:.6}'
  '.want h2{margin:0;font:600 11.5px/1.2 Poppins,system-ui,sans-serif;letter-spacing:.22em;text-transform:uppercase;opacity:.75}'
  '.want .g{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}'
  '.want a.w{position:relative;display:flex;flex-direction:column;gap:16px;padding:20px 18px 18px;border:1px solid var(--wln);background:var(--wcard);'
  'color:inherit;text-decoration:none;border-radius:var(--wr);min-height:132px;overflow:hidden;'
  'opacity:0;transform:translateY(10px);animation:wIn .55s cubic-bezier(.2,.7,.2,1) forwards;transition:border-color .25s,transform .25s,box-shadow .25s}'
  '.want a.w:nth-child(2){animation-delay:.07s}.want a.w:nth-child(3){animation-delay:.14s}.want a.w:nth-child(4){animation-delay:.21s}'
  '@keyframes wIn{to{opacity:1;transform:none}}'
  '.want a.w:after{content:"";position:absolute;left:0;top:0;height:2px;width:0;background:var(--wac);transition:width .35s ease}'
  '.want a.w:hover{border-color:var(--wac);transform:translateY(-3px);box-shadow:0 14px 30px -18px var(--wsh)}.want a.w:hover:after{width:100%}'
  '.want a.w.main{border-color:var(--wac)}.want a.w.main:after{width:100%}'
  '.want .ic{width:42px;height:42px;border-radius:50%;border:1px solid var(--wln);display:grid;place-items:center;color:var(--wic)}'
  '.want .ic svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}'
  '.want a.w b{font:var(--wtf);letter-spacing:0;padding-right:18px}'
  '.want a.w i{position:absolute;right:16px;bottom:16px;font-style:normal;font-size:16px;opacity:.55;transition:transform .25s,opacity .25s}'
  '.want a.w:hover i{transform:translateX(4px);opacity:1}'
  '@media(max-width:860px){.want{padding:26px 16px 28px}.want .g{grid-template-columns:1fr 1fr;gap:10px}.want a.w{min-height:118px;padding:16px 14px 14px;gap:12px}.want .ic{width:36px;height:36px}}'
  '@media(prefers-reduced-motion:reduce){.want a.w{animation:none;opacity:1;transform:none}}</style>')
ICONS = {
 "bank": '<path d="M3 10h18M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18M12 3l9 5H3z"/>',
 "up": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
 "check": '<path d="M9 12l2 2 4-4"/><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/>',
 "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
 "tax": '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
 "home": '<path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M10 21v-6h4v6"/>',
 "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M16 11h0M8 15h2M12 15h2M8 18h2M12 18h2"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
 "grad": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
}
def WANT(theme, title, sub, items):
    v = {"dark": "--wbg:#121214;--wfg:#fff;--wln:#2a2a2d;--wcard:linear-gradient(155deg,#1c1c1f,#141416);--wac:#e9e9e9;--wic:#fff;--wsh:#000;--wr:2px;"
                 "--wtf:400 19px/1.25 'Times New Roman',Times,Georgia,serif",
         "light": "--wbg:#f7f9fd;--wfg:#0B1F33;--wln:#dde3ee;--wcard:#fff;--wac:#1F5BFF;--wic:#1F5BFF;--wsh:rgba(31,91,255,.45);--wr:10px;"
                  "--wtf:600 15.5px/1.3 Poppins,system-ui,sans-serif"}[theme]
    cards = "".join(f'<a class="w{" main" if i == 0 else ""}" href="{h}"{" target=_blank rel=noopener" if h.startswith("https://wa.me") else ""} title="{d}">'
                    f'<span class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[ic]}</svg></span><b>{t}</b><i>→</i></a>'
                    for i, (t, d, h, c, ic) in enumerate(items))
    return f'<section class="want" id="mulai-cepat" style="{v}"><div class="in"><div class="hd"><h2>{title}</h2></div><div class="g">{cards}</div></div></section>'
WA0 = "https://wa.me/6282245260121?text="
from urllib.parse import quote as _q
WANTS = {
 "faindonesia": ("dark", "Mulai dari Kebutuhan Anda", "", [
   ("Dapat Kredit Bank", "Hitung plafon yang realistis dalam 3 menit, lalu kami dampingi sampai cair.", "#cek-kredit", "Cek Kredit Gratis", "bank"),
   ("Cari Investor atau IPO", "Untuk aset bersih di atas Rp50 miliar: investor institusi, M&A, persiapan IPO.", "/mitra-investor/", "Lihat Jalurnya", "up"),
   ("Rapikan Laporan Keuangan", "Pembukuan, audit, dan pajak bersama KAP, KJA, dan KKP mitra.", "/mitra-kap-kja/", "Lihat Mitra", "doc"),
   ("Tanya Langsung", "Ceritakan kondisi usaha Anda lewat WhatsApp.", WA0 + _q("Halo FA Indonesia, saya ingin konsultasi soal usaha saya."), "Chat Ananta, CPA", "chat")]),
 "cariakuntan": ("light", "Saya Butuh", "", [
   ("Audit Laporan Keuangan", "KAP untuk bank, tender, investor, atau wajib audit.", "/layanan/kap/", "Cari KAP", "check"),
   ("Pembukuan dan Laporan Keuangan", "KJA untuk pembukuan bulanan dan laporan keuangan siap pakai.", "/kota/", "Cari KJA per Kota", "book"),
   ("Urusan Pajak", "Konsultan pajak berizin untuk SPT, Coretax, dan pemeriksaan.", "/layanan/konsultan-pajak/", "Cari Konsultan Pajak", "tax"),
   ("Penilaian Aset", "KJPP rekanan bank untuk agunan dan revaluasi.", "/layanan/kjpp/", "Cari KJPP", "home")]),
 "updatesak": ("light", "Mulai dari Sini", "", [
   ("Cek Standar Akuntansi Saya", "Isi neraca dan laba rugi, dapat kerangka SAK, laporan keuangan, dan CALK.", "/#kalkulator", "Mulai Gratis", "calc"),
   ("Update SAK Terbaru", "PSAK, SAK EP, SAK EMKM, dan SAK Syariah yang berlaku 2026 sampai 2027.", "/update-psak-terbaru/", "Baca Update", "spark"),
   ("Belajar Standar Audit", "Ringkasan SA IAPI 2025 untuk auditor dan ujian CPA.", "/standar-audit/", "Mulai Belajar", "grad"),
   ("Cari Akuntan Berizin", "KAP, KJA, dan konsultan pajak berizin di kota Anda.", "https://cariakuntan.com/", "Cari Akuntan", "search")]),
}
_ECOK = {"faindonesia": "fa", "cariakuntan": "ca", "updatesak": "us"}
for _proj, _k in _ECOK.items():
    _d = os.path.join(OUT, _proj)
    for _r, _, _fs in os.walk(_d):
        for _f in _fs:
            if not _f.endswith(".html"): continue
            _p = os.path.join(_r, _f); _t = open(_p, encoding="utf-8").read()
            if 'id="ecobar"' in _t or "</head>" not in _t: continue
            _m = re.search(r"<body[^>]*>", _t)
            if not _m: continue
            _t = _t.replace("</head>", ECO_CSS + "</head>", 1)
            _m = re.search(r"<body[^>]*>", _t)
            _t = _t[:_m.end()] + ECO(_k) + _t[_m.end():]
            if os.path.relpath(_p, _d) in ("index.html",):
                th, ti, su, items = WANTS[_proj]
                _t = _t.replace("</head>", WANT_CSS + "</head>", 1)
                _mm = _t.find("<main")
                _h1 = _t.find("<section", _mm) if _mm > 0 else -1
                _h2 = _t.find("<section", _t.find("</section>", _h1)) if _h1 > 0 else -1
                # setelah hero (+ blok angka FA bila ada) = sebelum section kedua di main
                if _h2 > 0: _t = _t[:_h2] + WANT(th, ti, su, items) + _t[_h2:]
            open(_p, "w", encoding="utf-8").write(_t)
    print("ecobar", _proj)

# ---------- Rapikan tab: penting di atas, tulisan panjang dilipat (31 Okt 2026) ----------
_sys.path.insert(0, os.path.join(M, "shared"))
import tidy_tabs as _tt
print("tidy tabs:", _tt.run(OUT))
# footer FA: deretan link dilipat jadi "Menu Lainnya" (31 Okt 2026)
_FTCSS = ('<style id="ftmore-css">details.ft-more>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:8px;'
          'padding:8px 14px;border:1px solid currentColor;border-radius:999px;font-size:12.5px;opacity:.7}'
          'details.ft-more>summary::-webkit-details-marker{display:none}details.ft-more>summary:hover{opacity:1}'
          'details.ft-more[open]>summary{margin-bottom:12px}details.ft-more>ul{animation:ftin .3s ease}'
          '@keyframes ftin{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}</style>')
_nf = 0
for _d, _, _fs in os.walk(os.path.join(OUT, "faindonesia")):
    for _f in _fs:
        if not _f.endswith(".html"): continue
        _p = os.path.join(_d, _f); _t = open(_p, encoding="utf-8").read()
        if "ft-more" in _t or '<ul class="ents flinks">' not in _t: continue
        _i = _t.index('<ul class="ents flinks">'); _j = _t.index("</ul>", _i) + 5
        _t = _t[:_i] + '<details class="ft-more"><summary>Menu Lainnya</summary>' + _t[_i:_j] + "</details>" + _t[_j:]
        _t = _t.replace("</head>", _FTCSS + "</head>", 1)
        open(_p, "w", encoding="utf-8").write(_t); _nf += 1
print("footer dilipat:", _nf)

# ---------- zip per project for Cloudflare Direct Upload (<=10MB per upload) ----------
Z = os.path.join(M, "zips")
if os.path.exists(Z): shutil.rmtree(Z)
os.makedirs(Z)
for n in sorted(os.listdir(OUT)):
    shutil.make_archive(os.path.join(Z, n), "zip", os.path.join(OUT, n))
    print("zip", n, round(os.path.getsize(os.path.join(Z, n + ".zip"))/1e6, 2), "MB")
