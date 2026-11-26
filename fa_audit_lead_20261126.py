#!/usr/bin/env python3
"""26 Nov 2026: optimasi Google + asisten AI untuk lead jasa audit (FA), tanpa halaman baru.

Dasar (GSC 28 hari, dibaca 26 Nov): query berisi "audit" 495 impresi, 0 klik, pos 19,4;
halaman berisi "audit" 71 klik, 6,83rb impresi (artikel yang menampung, pilar pos 18,1).

Yang dikerjakan (out/faindonesia, idempoten, --dry):
1. /wilayah/<kota>/ (113, sudah terindeks, pos 4 sampai 11 untuk "kap <kota>"): blok
   <!--fa-al26--> setelah dua kartu fa-ik2, berisi "Audit LK Terima Beres di <Kota>" + link
   ke halaman audit kota dan halaman penyusunan LK kota (jalan crawl + pembeli).
2. 543 halaman audit daerah: meta description + og + twitter jadi kalimat FA sendiri yang
   memuat "terima beres" (3 variasi, <= 158 karakter, tanpa nama KAP, tanpa harga).
3. Pilar audit: meta description terima beres.
4. 17 artikel audit: satu kalimat berpenanda <!--fa-al26a--> setelah paragraf pembuka,
   link anchor komersial ke pilar audit.
5. sitemap-audit.xml (keluarga audit, lastmod hari ini) + lastmod di sitemap.xml untuk URL
   yang sama + baris Sitemap di robots.txt FA (out + sumber v58).
Aturan: tidak menempel di kartu/kalimat KAP DHN, tanpa harga, tanpa janji opini/waktu,
tanpa kalimat nama Ananta. Title, H1, URL, JSON-LD tidak berubah.
"""
import glob, hashlib, html, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(ROOT, "out", "faindonesia")
SRC = os.path.join(ROOT, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
DRY = "--dry" in sys.argv
TODAY = "2026-11-26"
changed = []


def write(path, new, old):
    if new != old:
        changed.append(os.path.relpath(path, ROOT))
        if not DRY:
            open(path, "w").write(new)


def pick(slug, n):
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % n


def nama(s):
    h = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1)
    h = re.sub(r"<[^>]+>", "", h)
    m = re.search(r" di (.+?)(?::|$)", h)
    return m.group(1).strip() if m else ""


CSS = ('<style id="fa-geo-css">.geo-tb{box-sizing:border-box;max-width:760px;margin:20px 0 6px;'
       'padding:16px 18px;border:1px solid rgba(233,185,73,.5);border-left:4px solid #E9B949;'
       'border-radius:12px;background:rgba(233,185,73,.07)}.geo-tb b.geo-h{display:block;font-size:17px;'
       'margin:0 0 6px}.geo-tb ul{margin:0;padding-left:1.2em}.geo-tb li{margin:.25em 0;line-height:1.55}'
       '.geo-tb p{margin:0 0 8px;line-height:1.55}.geo-tb .geo-l{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:10px}'
       '.geo-tb .geo-l a{font-weight:600;text-decoration:underline;text-underline-offset:3px}'
       '@media(max-width:760px){.geo-tb{padding:14px}}</style>')

# ------------------------------------------------------------ 1. /wilayah/<kota>/
WV = [
    "Perlu laporan audit untuk bank, SBU, tender, atau RUPS? Kirim data seadanya, tim FA Indonesia yang merapikan "
    "sampai siap audit, lalu pemeriksaannya oleh KAP terdaftar OJK.",
    "Pembukuan belum rapi bukan halangan. Data dirapikan tim FA Indonesia sampai siap audit, auditnya oleh KAP "
    "terdaftar OJK, dan kami dampingi sampai laporan diterima pihak yang meminta.",
    "Laporan audit diminta bank, LSBU, atau calon mitra? Serahkan data yang ada, tim FA Indonesia melengkapi "
    "laporan keuangannya, lalu diaudit KAP terdaftar OJK.",
]
RE26 = re.compile(r"<!--fa-al26-->.*?<!--/fa-al26-->", re.S)
for f in sorted(glob.glob(os.path.join(FA, "wilayah", "*", "index.html"))):
    slug = f.split(os.sep)[-2]
    old = open(f).read()
    s = RE26.sub("", old)
    k = s.find("<!--/fa-ik2-->")
    if k == -1:
        continue
    h1 = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1))
    kota = re.search(r'"addressLocality":\s*"([^"]+)"', s)
    kota = kota.group(1) if kota else " ".join(w.capitalize() for w in slug.split("-"))
    css = "" if 'id="fa-geo-css"' in s else CSS
    b = (f'<!--fa-al26-->{css}<div class="geo-tb"><b class="geo-h">Audit LK Terima Beres di {kota}</b>'
         f'<p>{WV[pick(slug, 3)]}</p><div class="geo-l">'
         f'<a href="/jasa-audit-laporan-keuangan/{slug}/">Jasa Audit LK {kota}</a>'
         f'<a href="/jasa-penyusunan-laporan-keuangan/{slug}/">Penyusunan Laporan Keuangan {kota}</a>'
         f'</div></div><!--/fa-al26-->')
    j = k + len("<!--/fa-ik2-->")
    write(f, s[:j] + b + s[j:], old)

# ------------------------------------------------------------ 2 + 3. description
DV = [
    "Jasa audit LK {d} terima beres: data seadanya dirapikan tim FA Indonesia, audit oleh KAP terdaftar OJK untuk bank, SBU, tender, dan SABH.",
    "Audit LK di {d} tanpa repot: pembukuan dirapikan tim FA Indonesia sampai siap audit, lalu diaudit KAP terdaftar OJK. Untuk bank, SBU, dan RUPS.",
    "Butuh audit LK di {d}? Terima beres: tim FA Indonesia merapikan data dan melengkapi laporan, audit oleh KAP terdaftar OJK.",
]
DSHORT = "Jasa audit LK {d} terima beres: data dirapikan tim FA Indonesia, audit oleh KAP terdaftar OJK."
DPILAR = ("Jasa audit laporan keuangan terima beres: data seadanya dirapikan tim FA Indonesia, audit oleh KAP "
          "terdaftar OJK. Untuk bank, SBU, tender, RUPS, dan SABH.")


def set_desc(s, desc):
    e = html.escape(desc, quote=True)

    def rep(m):
        tag = m.group(0)
        return re.sub(r'content="[^"]*"', f'content="{e}"', tag, count=1)
    return re.sub(r'<meta[^>]*(?:name="description"|property="og:description"|name="twitter:description")[^>]*>', rep, s)


fam = os.path.join(FA, "jasa-audit-laporan-keuangan")
for f in sorted(glob.glob(os.path.join(fam, "*", "index.html"))):
    slug = f.split(os.sep)[-2]
    old = open(f).read()
    d = nama(old)
    desc = DV[pick(slug, 3)].format(d=d)
    if len(desc) > 158:
        desc = min((v.format(d=d) for v in DV), key=len)
    if len(desc) > 158:
        desc = DSHORT.format(d=d)
    write(f, set_desc(old, desc), old)
f = os.path.join(fam, "index.html")
old = open(f).read()
write(f, set_desc(old, DPILAR), old)

# ------------------------------------------------------------ 4. artikel audit
REA = re.compile(r"<!--fa-al26a-->.*?<!--/fa-al26a-->", re.S)
LINE = ('<!--fa-al26a--><p style="margin:14px 0;font-size:.97em"><i>Butuh laporan audit tetapi pembukuan belum rapi? '
        'Lihat <a href="/jasa-audit-laporan-keuangan/">jasa audit laporan keuangan terima beres</a> dari tim FA Indonesia: '
        'data dirapikan dulu sampai siap audit, lalu diaudit KAP terdaftar OJK.</i></p><!--/fa-al26a-->')
SKIP = {"software-audit-untuk-kap-kecil-kertas-kerja-digital", "komite-audit-tugas-dan-syarat"}
for f in sorted(glob.glob(os.path.join(FA, "artikel", "*", "index.html"))):
    slug = f.split(os.sep)[-2]
    if "audit" not in slug or slug in SKIP:
        continue
    old = open(f).read()
    s = REA.sub("", old)
    h1 = s.find("</h1>")
    # paragraf isi pertama: <p> polos pertama yang panjang setelah H1
    j = -1
    for m in re.finditer(r"<p(?:\s[^>]*)?>(.*?)</p>", s[h1:], re.S):
        t = re.sub(r"<[^>]+>", "", m.group(1))
        if len(t) > 160 and "Oleh " not in t[:8]:
            j = h1 + m.end()
            break
    n = s.find('<nav aria-label="', h1)  # sebelum Peta Isi, supaya tidak memotong paragraf pembuka
    if n != -1 and 'Peta Isi' in s[n:n + 400]:
        j = n
    if j == -1:
        continue
    write(f, s[:j] + LINE + s[j:], old)

# ------------------------------------------------------------ 5. sitemap
urls = ["https://faindonesia.co.id/jasa-audit-laporan-keuangan/", "https://faindonesia.co.id/jasa-pendampingan-audit/"]
for famn in ("jasa-audit-laporan-keuangan", "jasa-pendampingan-audit"):
    for d in sorted(os.listdir(os.path.join(FA, famn))):
        if os.path.isfile(os.path.join(FA, famn, d, "index.html")):
            urls.append(f"https://faindonesia.co.id/{famn}/{d}/")
for d in sorted(os.listdir(os.path.join(FA, "wilayah"))):
    if os.path.isfile(os.path.join(FA, "wilayah", d, "index.html")):
        urls.append(f"https://faindonesia.co.id/wilayah/{d}/")
for d in sorted(os.listdir(os.path.join(FA, "artikel"))):
    if "audit" in d and os.path.isfile(os.path.join(FA, "artikel", d, "index.html")):
        urls.append(f"https://faindonesia.co.id/artikel/{d}/")
f = os.path.join(FA, "sitemap.xml")
old = open(f).read()
insm = set(re.findall(r"<loc>([^<]+)</loc>", old))
urls = [u for u in urls if u in insm]  # hanya URL yang memang ada di sitemap utama (bukan noindex)
uset = set(urls)


def lm(m):
    return m.group(1) + TODAY + m.group(3) if m.group(1)[len("<url><loc>"):-len("</loc><lastmod>")] in uset else m.group(0)


s = re.sub(r"(<url><loc>[^<]+</loc><lastmod>)([^<]+)(</lastmod>)", lm, old)
write(f, s, old)
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
f = os.path.join(FA, "sitemap-audit.xml")
write(f, sm, open(f).read() if os.path.exists(f) else "")
LINE_SM = "Sitemap: https://faindonesia.co.id/sitemap-audit.xml\n"
for f in (os.path.join(FA, "robots.txt"), os.path.join(SRC, "robots.txt")):
    if os.path.exists(f):
        old = open(f).read()
        if LINE_SM not in old:
            write(f, old.rstrip("\n") + "\n" + LINE_SM, old)

print(("DRY " if DRY else "") + f"{len(changed)} file berubah; sitemap-audit {len(urls)} URL")
for c in changed[:6]:
    print(" ", c)
