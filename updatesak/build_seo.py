# Generator halaman SEO UpdateSAK: /psak/<n>/, /artikel/<slug>/, hub Eksplor, sitemap, llms.txt, gambar share.
# Idempoten: jalankan ulang kapan saja (dipanggil prep.py sebelum menyalin updatesak/site).
import os, re, html, json, sys
from datetime import date
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from seo_psak import P, LAMA
from seo_artikel import A
SITE = os.path.join(HERE, "site")
BASE = "https://updatesak.com"
TODAY = "2026-10-27"
TGL = "27 Oktober 2026"
WA = "https://wa.me/6282245260121?text="
esc = html.escape

def aurl(a): return f"/{a['slug']}/" if a.get("root") else f"/artikel/{a['slug']}/"
def slug_psak(n): return f"/psak/{n}/"
PS = {p[0]: p for p in P}

HEAD = """<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B1F33">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600;700&family=Quicksand:wght@300;400&display=swap">
<link rel="stylesheet" href="/css/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="logo" href="/" aria-label="UpdateSAK beranda"><svg class="mk" viewBox="0 0 30 40" width="27" height="36" aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x=".6" y=".6" width="28.8" height="38.8" stroke="#1F5BFF" stroke-width="1.2"/><path d="M6.5 8v6.2a3.2 3.2 0 0 0 6.4 0V8" stroke="#1F5BFF" stroke-width="1.3"/><path d="M24.2 24.4c-.9-1.2-5.6-1.6-5.6 1.4 0 2.9 6.1 1.6 6.1 4.6 0 3.1-5.3 2.8-6.6 1.2" stroke="#1F5BFF" stroke-width="1.3"/></svg><b>Update<span>SAK</span></b></a>
  <nav class="tabs" aria-label="Menu utama"><a href="/">Beranda</a><a href="/eksplor/" aria-current="page">Eksplor</a><a href="/materi/">Materi</a></nav>
  <a class="btn btn-sm" href="https://wa.me/6282245260121?text=Halo%20tim%20UpdateSAK%2C%20saya%20ingin%20diskusi%20penerapan%20SAK%20di%20perusahaan%20kami." target="_blank" rel="noopener">Chat Ananta, CPA</a>
</div></header>
<main>
"""
FOOT = """</main>
<footer><div class="wrap">
  <span>© 2026 UpdateSAK · <a href="https://faindonesia.co.id/">FA Indonesia</a> · <a href="https://cariakuntan.com/">CariAkuntan</a></span>
  <span><a href="/eksplor/">Eksplor</a> · <a href="/materi/">Materi</a> · <a href="/eksplor/#standar">Daftar PSAK</a> · <a href="mailto:ananta@faindonesia.co.id">Email</a></span>
</div></footer>
<div class="bar-m"><a class="btn" href="https://wa.me/6282245260121?text=Halo%20tim%20UpdateSAK%2C%20saya%20ingin%20diskusi%20penerapan%20SAK%20di%20perusahaan%20kami." target="_blank" rel="noopener">Chat Ananta, CPA</a></div>
<script>document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{try{navigator.clipboard.writeText(b.dataset.copy);b.textContent='Link Tersalin'}catch(e){}}));</script>
</body>
</html>
"""

def ld_graph(url, title, desc, crumbs, faq, img):
    g = [{"@type": "Article", "headline": title, "description": desc, "inLanguage": "id", "url": url, "image": img,
          "datePublished": TODAY, "dateModified": TODAY,
          "author": {"@type": "Organization", "name": "Tim UpdateSAK", "url": BASE + "/"},
          "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": "https://faindonesia.co.id/"}},
         {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}]
    if faq:
        g.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]})
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False)

def share(url, title, key):
    from urllib.parse import quote
    return f'''<div class="share"><span>Bagikan</span>
<a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(url, safe='')}" target="_blank" rel="noopener">LinkedIn</a>
<a href="/img/share/{key}-story.jpg" download>Gambar IG Story</a>
<a href="https://wa.me/?text={quote(title + ' ' + url)}" target="_blank" rel="noopener">WhatsApp</a>
<button type="button" data-copy="{esc(url)}">Salin Link</button></div>'''

def cta(text, mode="std"):
    return f'''<aside class="cta-box"><div><b>{esc(text)}</b><span>Masukkan neraca dan laba rugi, hasil langsung keluar. Gratis.</span></div><a class="btn arrow" href="/#kalkulator">Buka Kalkulator</a></aside>'''

def wa_box(topic):
    from urllib.parse import quote
    return f'''<aside class="cta-box dark"><div><b>Butuh Pendampingan {esc(topic)}?</b><span>Tim akuntan bersertifikat CA dan CPA, terbiasa dengan prosedur auditor Big 4.</span></div><a class="btn arrow" target="_blank" rel="noopener" href="{WA}{quote('Halo tim UpdateSAK, saya butuh pendampingan ' + topic + '.')}">Chat Ananta, CPA</a></aside>'''

def faq_html(faq):
    if not faq: return ""
    return '<h2>Tanya Jawab</h2>' + "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in faq)

def chip(n):
    p = PS.get(n)
    return f'<a class="pchip" href="{slug_psak(n)}"><b>PSAK {n}</b><span>{esc(p[1]) if p else ""}</span></a>' if p else ""

# ---------- gambar share ----------
def make_images(key, kicker, title):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return
    d = os.path.join(SITE, "img", "share"); os.makedirs(d, exist_ok=True)
    F = os.path.join(HERE, "fonts")
    serif = lambda s: ImageFont.truetype(os.path.join(F, "SourceSerif4-Semibold.ttf"), s)
    sans = lambda s, b=True: ImageFont.truetype(os.path.join(F, "IBMPlexSans-SemiBold.ttf" if b else "IBMPlexSans-Regular.ttf"), s)
    for kind, (W, H) in (("og", (1200, 630)), ("story", (1080, 1920))):
        out = os.path.join(d, f"{key}-{kind}.jpg")
        if os.path.exists(out) and os.environ.get("US_REIMG") != "1":
            continue
        import numpy as np
        yy, xx = np.mgrid[0:H, 0:W]
        t = (xx / W * .55 + yy / H * .45)[..., None]
        a0, a1 = np.array([11, 31, 51]), np.array([31, 91, 255])
        im = Image.fromarray((a0 + (a1 - a0) * t).astype("uint8"), "RGB")
        dr = ImageDraw.Draw(im)
        for gx in range(0, W, 26):
            for gy in range(0, H, 26):
                dr.point((gx, gy), fill=(70, 110, 200))
        m = 70 if kind == "og" else 90
        # logo
        dr.rectangle([m, m, m + 54, m + 54], fill="#1F5BFF")
        dr.text((m + 27, m + 27), "US", font=sans(22), fill="white", anchor="mm")
        dr.text((m + 70, m + 27), "UpdateSAK", font=serif(36), fill="white", anchor="lm")
        ky = m + 120 if kind == "og" else 520
        dr.text((m, ky), kicker.upper(), font=sans(26 if kind == "og" else 36), fill="#8FB2FF")
        size = 58 if kind == "og" else 84
        maxw = W - 2 * m
        words, lines, cur = title.split(), [], ""
        while True:
            lines, cur = [], ""
            for w in words:
                t = (cur + " " + w).strip()
                if dr.textlength(t, font=serif(size)) <= maxw: cur = t
                else: lines.append(cur); cur = w
            lines.append(cur)
            if len(lines) <= (4 if kind == "og" else 7) or size < 30: break
            size -= 4
        y = ky + (56 if kind == "og" else 80)
        for ln in lines:
            dr.text((m, y), ln, font=serif(size), fill="white"); y += int(size * 1.18)
        dr.rectangle([m, y + 18, m + 70, y + 24], fill="#1F5BFF")
        fy = H - m - 30
        dr.text((m, fy), "updatesak.com", font=sans(30 if kind == "og" else 40), fill="white")
        if kind == "story":
            dr.text((m, fy - 70), "Kalkulator PSAK dan CALK Format Auditor", font=sans(34, False), fill="#C9D8FF")
        im.save(out, "JPEG", quality=82, optimize=True, progressive=True)

pages = []  # (url, lastmod)

# ---------- halaman PSAK ----------
def psak_page(p):
    n, judul, ref, lama, lingkup, inti, calk, auditor, terkait = p
    url = BASE + slug_psak(n)
    key = f"psak-{n}"
    title = f"PSAK {n} {judul}: Ringkasan, Kebijakan Akuntansi CALK, dan Fokus Auditor | UpdateSAK"
    if len(title) > 95: title = f"PSAK {n} {judul}: Ringkasan dan Fokus Auditor | UpdateSAK"
    desc = f"Ringkasan PSAK {n} {judul}" + (f" (dulu {lama})" if lama else "") + (f", padanan {ref}" if ref else "") + ": inti pengaturan, contoh kalimat kebijakan akuntansi di CALK, dan temuan auditor yang sering muncul."
    desc = desc[:300]
    faq = [(f"Apa yang diatur PSAK {n}?", lingkup)]
    if lama: faq.append((f"PSAK {n} dulu nomor berapa?", f"PSAK {n} dulunya {lama}. Penomoran 3 digit berlaku sejak 1 Januari 2024." + (f" Padanan internasionalnya {ref}." if ref else "")))
    faq.append((f"Apa temuan auditor yang sering terkait PSAK {n}?", "; ".join(auditor) + "."))
    img = f"{BASE}/img/share/{key}-og.jpg"
    crumbs = [("UpdateSAK", BASE + "/"), ("Eksplor", BASE + "/eksplor/"), (f"PSAK {n}", url)]
    seri = {1: "Seri 100 · Berbasis IFRS", 2: "Seri 200 · Berbasis IAS", 3: "Seri 300 · Khusus Indonesia", 4: "Seri 400 · SAK Syariah"}[n // 100]
    meta = " · ".join(x for x in [seri, f"Padanan {ref}" if ref else None, f"Dulu {lama}" if lama else None] if x)
    body = f'''<article class="art"><div class="wrap">
<nav class="crumb"><a href="/">Beranda</a> / <a href="/eksplor/">Eksplor</a> / <a href="/eksplor/#standar">Daftar PSAK</a> / PSAK {n}</nav>
<p class="label">{esc(meta)}</p>
<h1>PSAK {n} {esc(judul)}</h1>
<p class="lede">{esc(lingkup)}</p>
<p class="upd">Penomoran sesuai SAK Online IAI · Diperbarui {TGL}</p>
{share(url, f"PSAK {n} {judul}", key)}
<h2>Inti Pengaturan</h2>
<div class="keys">{"".join(f"<div><b>{i+1:02d}</b><span>{esc(x)}</span></div>" for i, x in enumerate(inti))}</div>
<h2>Contoh Kalimat Kebijakan Akuntansi di CALK</h2>
<blockquote class="calk">{esc(calk)}</blockquote>
<p class="note">Sesuaikan dengan fakta perusahaan. Kalimat ini ditulis ulang oleh tim UpdateSAK dan bukan kutipan teks standar.</p>
{cta(f"Cek Apakah PSAK {n} Berlaku di Perusahaan Anda")}
<p class="upd"><a href="/update-psak-2026/">Lihat semua Update PSAK 2026 →</a></p>
<h2>Yang Sering Dipersoalkan Auditor</h2>
<ul class="flags">{"".join(f"<li>{esc(x)}</li>" for x in auditor)}</ul>
<h2>Standar Terkait</h2>
<div class="pchips">{"".join(chip(t) for t in terkait)}</div>
{faq_html(faq)}
{wa_box(f"Penerapan PSAK {n}")}
<nav class="pn">{prevnext(n)}</nav>
</div></article>
'''
    ld = ld_graph(url, f"PSAK {n} {judul}", desc, crumbs, faq, img)
    write(f"psak/{n}", HEAD.format(title=esc(title), desc=esc(desc), url=url, ogt=esc(f"PSAK {n} {judul}"), img=img, ld=ld) + body + FOOT)
    make_images(key, f"PSAK {n}" + (f" · {ref}" if ref else ""), judul)
    pages.append((url, TODAY))

ORDER = [p[0] for p in P]
def prevnext(n):
    i = ORDER.index(n); s = ""
    if i > 0: s += f'<a href="{slug_psak(ORDER[i-1])}">← PSAK {ORDER[i-1]}</a>'
    else: s += "<span></span>"
    if i < len(ORDER) - 1: s += f'<a href="{slug_psak(ORDER[i+1])}">PSAK {ORDER[i+1]} →</a>'
    return s

def write(path, content):
    d = os.path.join(SITE, path); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(content)

# ---------- artikel ----------
def tabel_lama():
    rows = "".join(f"<tr><td>{k}</td><td><a href=\"{slug_psak(v)}\">PSAK {v}</a></td><td>{esc(PS[v][1])}</td><td>{esc(PS[v][2] or 'Khusus Indonesia')}</td></tr>"
                   for k, v in sorted(LAMA.items(), key=lambda kv: kv[1]))
    return f'<div class="scroll"><table class="tbl"><thead><tr><th>Nomor Lama</th><th>Nomor Baru</th><th>Judul</th><th>Padanan</th></tr></thead><tbody>{rows}</tbody></table></div>'

def art_page(a):
    path = a["slug"] if a.get("root") else f"artikel/{a['slug']}"
    url = f"{BASE}/{path}/"
    key = "art-" + a["slug"]
    img = f"{BASE}/img/share/{key}-og.jpg"
    title = (a["judul"].split(":")[0] + ": Perubahan SAK Terbaru DSAK IAI") if a.get("root") else a["judul"] + " | UpdateSAK"
    body_html = a["body"].replace("{{TABEL_LAMA}}", tabel_lama())
    body_html = re.sub(r"<table class=\"tbl\">", '<div class="scroll"><table class="tbl">', body_html)
    body_html = body_html.replace("</table>", "</table></div>").replace("</table></div></div>", "</table></div>")
    crumbs = [("UpdateSAK", BASE + "/"), ("Eksplor", BASE + "/eksplor/"), (a["judul"], url)]
    rel = [x for x in A if x["slug"] != a["slug"] and x["kat"] == a["kat"]][:3] or [x for x in A if x["slug"] != a["slug"]][:3]
    out = f'''<article class="art"><div class="wrap">
<nav class="crumb"><a href="/">Beranda</a> / <a href="/eksplor/">Eksplor</a> / <a href="/eksplor/#artikel">{esc(a["kat"])}</a></nav>
<p class="label">{esc(a["kat"])}</p>
<h1>{esc(a["judul"])}</h1>
<p class="lede">{esc(a["desc"])}</p>
<p class="upd">Tim UpdateSAK · Diperbarui {TGL}</p>
{share(url, a["judul"], key)}
<div class="prose">{body_html}</div>
{cta("Hitung Langsung Untuk Perusahaan Anda")}
{('<h2>Standar Terkait</h2><div class="pchips">' + "".join(chip(t) for t in a["psak"]) + '</div>') if a["psak"] else ""}
{faq_html(a["faq"])}
<h2>Baca Juga</h2><div class="reads">{"".join(f'<a href="{aurl(r)}"><b>{esc(r["judul"])}</b><small>{esc(r["kat"])}</small></a>' for r in rel)}</div>
{wa_box(a["kat"] if a["kat"] not in ("Belajar",) else "Laporan Keuangan")}
</div></article>
'''
    ld = ld_graph(url, a["judul"], a["desc"], crumbs, a["faq"], img)
    write(path, HEAD.format(title=esc(title), desc=esc(a["desc"]), url=url, ogt=esc(a["judul"]), img=img, ld=ld) + out + FOOT)
    make_images(key, a["kat"], a["judul"])
    pages.append((url, TODAY))

# ---------- hub Eksplor ----------
def hub():
    p = os.path.join(SITE, "eksplor", "index.html"); s = open(p, encoding="utf-8").read()
    groups = [("Seri 100 · Berbasis IFRS", 1), ("Seri 200 · Berbasis IAS", 2), ("Seri 300 dan 400 · Khusus Indonesia dan Syariah", 3)]
    g_html = ""
    for lab, k in groups:
        items = [q for q in P if (q[0] // 100 == k) or (k == 3 and q[0] // 100 == 4)]
        g_html += f'<h3 class="gh">{lab}</h3><div class="pchips">' + "".join(chip(q[0]) for q in items) + "</div>"
    cats = []
    for a in A:
        if a["kat"] not in cats: cats.append(a["kat"])
    a_html = "".join(f'<h3 class="gh">{esc(c)}</h3><div class="reads">' + "".join(f'<a href="{aurl(a)}"><b>{esc(a["judul"])}</b><small>{esc(a["desc"][:110])}…</small></a>' for a in A if a["kat"] == c) + "</div>" for c in cats)
    block = f'''<!--seo:start-->
<section id="standar"><div class="wrap">
  <div class="head"><h2>Panduan Per Standar</h2><p>Ringkasan setiap PSAK yang berlaku: inti pengaturan, contoh kebijakan akuntansi CALK, dan temuan auditor.</p></div>
  {g_html}
</div></section>
<section class="alt" id="artikel"><div class="wrap">
  <div class="head"><h2>Artikel dan Panduan</h2></div>
  {a_html}
</div></section>
<!--seo:end-->'''
    if "<!--seo:start-->" in s:
        s = re.sub(r"<!--seo:start-->.*?<!--seo:end-->", block, s, flags=re.S)
    else:
        i = s.find('<section class="alt" id="tanya">')
        s = s[:i] + block + "\n" + s[i:]
    # tabel PSAK berlaku: tautkan ke halaman standar
    s = re.sub(r"<tr><td>PSAK (\d{3})</td>", lambda m: f'<tr><td><a href="/psak/{m.group(1)}/">PSAK {m.group(1)}</a></td>' if int(m.group(1)) in PS else m.group(0), s)
    s = s.replace('<span id="updLbl">27 Oktober 2026</span>', f'<span id="updLbl">{TGL}</span>')
    open(p, "w", encoding="utf-8").write(s)

def sitemap():
    urls = [(BASE + "/", TODAY), (BASE + "/eksplor/", TODAY)] + pages
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n"
    open(os.path.join(SITE, "sitemap.xml"), "w").write(x)

def llms():
    p = os.path.join(SITE, "llms.txt"); s = open(p, encoding="utf-8").read()
    s = s.split("\n## Panduan Per Standar")[0].rstrip() + "\n\n## Panduan Per Standar\n" + "".join(f"- [PSAK {q[0]} {q[1]}]({BASE}{slug_psak(q[0])}): {q[4]}\n" for q in P)
    s += "\n## Artikel\n" + "".join(f"- [{a['judul']}]({BASE}{aurl(a)}): {a['desc']}\n" for a in A)
    open(p, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    for p in P: psak_page(p)
    for a in A: art_page(a)
    hub(); sitemap(); llms()
    print("seo pages", len(pages))
