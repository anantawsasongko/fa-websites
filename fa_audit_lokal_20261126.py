#!/usr/bin/env python3
"""26 Nov 2026 (3): isi lokal unik di halaman audit kota besar (akar "Crawled, currently not indexed").

Blok <!--fa-lok26--> setelah blok fa-geo di /jasa-audit-laporan-keuangan/<kota>/ untuk kota di
fa_content/audit_lokal_20261126.py: satu paragraf terlihat + lipatan "Selengkapnya" (paragraf kedua
dan tiga keperluan paling sering). Tambah kota = tambah entri di file konten. Idempoten, --dry.
Juga: og:image pilar audit diganti gambar umum (gambar lama memuat janji biaya dan waktu) dan
priceRange dibuang dari JSON-LD beranda (aturan 21 Nov: tanpa harga).
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "fa_content"))
from audit_lokal_20261126 import L  # noqa: E402

FA = os.path.join(ROOT, "out", "faindonesia")
DRY = "--dry" in sys.argv
changed = []


def write(path, new, old):
    if new != old:
        changed.append(os.path.relpath(path, ROOT))
        if not DRY:
            open(path, "w").write(new)


CSS = ('<style id="fa-lok26-css">.lok26{max-width:760px;margin:18px 0 6px}.lok26 b.lok-h{display:block;'
       'font-size:17px;margin:0 0 6px}.lok26 p{margin:0 0 10px;line-height:1.6}.lok26 details{margin:2px 0 0}'
       '.lok26 summary{cursor:pointer;font-weight:600;text-decoration:underline;text-underline-offset:3px;'
       'margin:0 0 10px}.lok26 ul{margin:0 0 6px;padding-left:1.2em}.lok26 li{margin:.25em 0;line-height:1.55}</style>')
RE = re.compile(r"<!--fa-lok26-->.*?<!--/fa-lok26-->", re.S)
for slug, (kota, p1, p2, need) in L.items():
    f = os.path.join(FA, "jasa-audit-laporan-keuangan", slug, "index.html")
    if not os.path.exists(f):
        print("TIDAK ADA", slug)
        continue
    old = open(f).read()
    s = RE.sub("", old)
    k = s.find("<!--/fa-geo-->")
    assert k != -1, slug
    k += len("<!--/fa-geo-->")
    b = (f'<!--fa-lok26-->{CSS}<div class="lok26"><b class="lok-h">Audit Laporan Keuangan di {kota}: Siapa yang '
         f'Biasanya Membutuhkan</b><p>{p1}</p><details><summary>Selengkapnya tentang audit di {kota}</summary>'
         f'<p>{p2}</p><p><b>Keperluan yang paling sering di {kota}:</b></p><ul>'
         + "".join(f"<li>{x}</li>" for x in need) + "</ul></details></div><!--/fa-lok26-->")
    write(f, s[:k] + b + s[k:], old)

# og:image pilar audit
f = os.path.join(FA, "jasa-audit-laporan-keuangan", "index.html")
old = open(f).read()
write(f, old.replace("https://faindonesia.co.id/img/og-page/jasa-audit-laporan-keuangan.jpg",
                     "https://faindonesia.co.id/img/og/fa-indonesia-og.jpg"), old)

# priceRange beranda
f = os.path.join(FA, "index.html")
old = open(f).read()


def fix(m):
    d = json.loads(m.group(1))
    hit = False
    for g in d.get("@graph", []):
        if isinstance(g, dict) and "priceRange" in g:
            del g["priceRange"]
            hit = True
    return ('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>") if hit else m.group(0)


write(f, re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, old, count=1, flags=re.S), old)
print(("DRY " if DRY else "") + f"{len(changed)} file berubah")
