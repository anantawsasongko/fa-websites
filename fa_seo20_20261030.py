# -*- coding: utf-8 -*-
"""SEO push 30 Okt 2026: 15 artikel FA (kredit bank, sektor, investor/IPO/M&A, outsourcing akuntansi).
Konten di fa_content/seo20_a.json, seo20_b.json, seo20_c.json (format: slug, cat, topic, title, h1, desc, minutes, body, faq, related, sources, cta_href, cta_label, wa).
Helper art_page diambil dari fa_mitra_20261027.py. Kartu Eksplor (penanda fa-seo20), sitemap, llms.txt.
Idempoten. Jalankan setelah fa_viral_20261028b.py, sebelum fa_rapi_20261027.py.
5 artikel CariAkuntan ada di cariakuntan/gen/seo20.json (dibangun otomatis oleh cariakuntan/build.py)."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_mitra_20261027.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. MITRA RM BANK")]
_src = _src.replace('TODAY = "2026-10-27"', 'TODAY = "2026-10-30"').replace("27 Oktober 2026", "30 Oktober 2026")
exec(compile(_src, "fa_mitra_helpers", "exec"))

ARTS = []
for f in ("seo20_a.json", "seo20_b.json", "seo20_c.json"):
    ARTS += json.load(open(os.path.join(HERE, "fa_content", f), encoding="utf-8"))

for a in ARTS:
    art_page(a["slug"], a["cat"], a["title"], a["h1"], a["desc"], a["minutes"], a["body"],
             [tuple(x) for x in a["faq"]], [tuple(x) for x in a["related"]], [tuple(x) for x in a["sources"]],
             a["cta_href"], a["cta_label"], a["wa"])

# kartu Eksplor
ip = P("artikel", "index.html"); t = re.sub(r"<!--fa-seo20-->.*?<!--/fa-seo20-->", "", rd(ip), flags=re.S)
CARD = '<!--fa-seo20--><a class="card2" href="/artikel/{s}/"><b>{h}</b><span>{d}</span></a><!--/fa-seo20-->'
miss = 0
for a in reversed(ARTS):
    k = t.find(f'id="{a["topic"]}"')
    if k < 0: k = t.find('id="t-kredit-bank"'); miss += 1
    k = t.find('<div class="cards2">', k) + len('<div class="cards2">')
    t = t[:k] + CARD.format(s=a["slug"], h=E(a["h1"]), d=E(a["desc"])) + t[k:]
wtxt(ip, t)

# sitemap
sm = re.sub(r"<!--fa-seo20-->.*?<!--/fa-seo20-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-seo20-->\n" + "".join(f"<url><loc>{D}/artikel/{a['slug']}/</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for a in ARTS) + "<!--/fa-seo20-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)

# llms.txt
ll = re.sub(r"\n## Panduan Kredit, Investor, dan IPO \(Okt 2026\).*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + "\n\n## Panduan Kredit, Investor, dan IPO (Okt 2026)\n" + "".join(f"- [{a['h1']}]({D}/artikel/{a['slug']}/): {a['desc']}\n" for a in ARTS)
wtxt(P("llms.txt"), ll)
print("seo20 FA:", len(ARTS), "artikel, topik tidak ketemu:", miss)
