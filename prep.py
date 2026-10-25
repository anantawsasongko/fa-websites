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

for n in sorted(os.listdir(OUT)):
    cnt = sum(len(f) for _, _, f in os.walk(os.path.join(OUT, n)))
    print(n, cnt)

# ---------- anti duplikat SEO: *.pages.dev noindex untuk project yang punya domain sendiri ----------
for proj in ["cariakuntan", "faindonesia", "faindonesia-jupiter", "faindonesia-saturn", "faindonesia-venus"]:
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

# ---------- zip per project for Cloudflare Direct Upload (<=10MB per upload) ----------
Z = os.path.join(M, "zips")
if os.path.exists(Z): shutil.rmtree(Z)
os.makedirs(Z)
for n in sorted(os.listdir(OUT)):
    shutil.make_archive(os.path.join(Z, n), "zip", os.path.join(OUT, n))
    print("zip", n, round(os.path.getsize(os.path.join(Z, n + ".zip"))/1e6, 2), "MB")
