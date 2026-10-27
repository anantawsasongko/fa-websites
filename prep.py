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
# nav: Apps, Layanan, E-Book, Wawasan (artikel + berita), Cari Akuntan, Kontak
idx = os.path.join(fa, "index.html")
s = open(idx, encoding="utf-8").read()
old_nav = re.search(r'<nav aria-label="Navigasi utama" class="links">.*?</nav>', s, re.S).group(0)
new_nav = ('<nav aria-label="Navigasi utama" class="links"> <a data-i18n="kapp" href="/apps/">Apps</a> '
           '<a data-i18n="k2" href="/layanan/">Layanan</a> <a data-i18n="kebk" href="/buku/">E-Book</a> <a data-i18n="kwws" href="/artikel/">Eksplor</a> <a data-i18n="kcak" href="https://cariakuntan.com/" target="_blank" rel="noopener">Cari Akuntan</a> '
           '<a data-i18n="k321" href="#kontak">Kontak</a> </nav>')
s = s.replace(old_nav, new_nav)
s = s.replace(' data-netlify="true" netlify-honeypot="bot-field"', '')
open(idx, "w", encoding="utf-8").write(s)
NAV_CSS = '<style id="nav4">@media (max-width:820px){nav.links{justify-content:space-between!important;gap:8px!important;overflow-x:auto;scrollbar-width:none}nav.links::-webkit-scrollbar{display:none}nav.links a{flex:0 0 auto!important;font-size:12.5px!important;padding-left:0!important;padding-right:0!important;letter-spacing:0!important}}@media (max-width:370px){nav.links a{font-size:11.5px!important}}</style>'
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
        if 'Navigasi utama' in t2 and 'id="nav4"' not in t2:
            t2 = t2.replace('</head>', NAV_CSS + '</head>', 1)
            t2 = t2.replace('"en": {', '"en": {"kapp": "Apps", "kebk": "E-Books", "kcak": "Find Accountants", "kwws": "Explore", ').replace('"zh": {', '"zh": {"kapp": "应用", "kebk": "电子书", "kcak": "找会计师", "kwws": "探索", ')
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
        t = t.replace("</body>", "<script>window.FA_SECURE=" + cfg + "</script><script src=\"/js/secure.js\"></script></body>", 1)
        open(pth, "w", encoding="utf-8").write(t)
add_secure(fa, ["index.html", "cek-kapasitas-kredit/index.html", "kalkulator-dscr/index.html", "simulasi-plafon-kredit-usaha/index.html", "cek-kelayakan-ipo/index.html"],
    "{brand:'fa',mode:'send',theme:'dark',at:[{sel:'#kk',pos:'beforebegin'}]}")
add_secure(fa, ["cek-psak-118/index.html"], "{brand:'fa',mode:'local',theme:'dark',at:[{sel:'header.bar',pos:'afterend',cls:'bar'}]}")
add_secure(fa, ["audit-ready/index.html"], "{brand:'fa',mode:'drive',theme:'dark',at:[{sel:'header.bar',pos:'afterend',cls:'bar'}]}")
add_secure(fa, ["saturn/index.html"], "{brand:'fa',mode:'drive',theme:'dark',at:[{sel:'header.top',pos:'afterend',cls:'bar'}]}")
add_secure(os.path.join(OUT, "cariakuntan"), ["index.html", "en/index.html", "zh/index.html", "hokkien/index.html", "screening/index.html"],
    "{brand:'ca',mode:'send',theme:'light',at:[{sel:'#screening',pos:'afterbegin'}]}")
add_secure(u, ["index.html"], "{brand:'us',mode:'local',theme:'light',at:[{sel:'#kalkulator .calc',pos:'beforebegin'}]}")
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
       '.fa-cta{max-width:1080px;margin:40px auto;padding:26px 24px;border-radius:12px;background:#0f1f3d;color:#fff;font-family:inherit}'
       '.fa-cta h2{margin:0 0 6px;font-size:1.3rem;color:#fff}.fa-cta p{margin:0 0 16px;opacity:.85;font-size:.95rem;line-height:1.55}'
       '.fa-cta .b{display:flex;flex-wrap:wrap;gap:10px}.fa-cta a{display:inline-block;padding:11px 18px;border-radius:8px;font-weight:600;text-decoration:none;font-size:.92rem}'
       '.fa-cta a.w{background:#25D366;color:#06301a}.fa-cta a.l{border:1px solid rgba(255,255,255,.5);color:#fff}'
       '@media (max-width:720px){.fa-cta{margin:28px 16px}}</style>'
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
            if cta_dirs and 'class="fa-cta"' not in t and any(rel.startswith(d) for d in cta_dirs) and "konsultan-kredit-bank" not in rel:
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

# ---------- zip per project for Cloudflare Direct Upload (<=10MB per upload) ----------
Z = os.path.join(M, "zips")
if os.path.exists(Z): shutil.rmtree(Z)
os.makedirs(Z)
for n in sorted(os.listdir(OUT)):
    shutil.make_archive(os.path.join(Z, n), "zip", os.path.join(OUT, n))
    print("zip", n, round(os.path.getsize(os.path.join(Z, n + ".zip"))/1e6, 2), "MB")
