# -*- coding: utf-8 -*-
"""Logo A (wordmark serif gaya McKinsey) di header Cari Akuntan dan UpdateSAK (1 Nov 2026, pilihan Bos).
Sumber svg: shared/logo/make_logos.py. Dipanggil prep.py setelah favicon."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
def _inline(k, h):
    s = open(os.path.join(HERE, "logo", f"{k}-{'header' if h > 24 else 'icon'}.svg"), encoding="utf-8").read()
    s = re.sub(r'\swidth="\d+"\sheight="\d+"', f' height="{h}" class="wm" aria-hidden="true" focusable="false"', s, count=1)
    return s.replace(' xmlns="http://www.w3.org/2000/svg"', "")
CSS = ('<style id="wm-css">.logo .wm{display:block;height:32px;width:auto;color:%s}.logo{display:flex;align-items:center}'
       '@media(max-width:600px){.logo .wm{height:27px}}</style>')
def run(OUT):
    n = 0
    for site, k, word, col in (("cariakuntan", "ca", r"<b>cari<span>akuntan</span></b>", "#0B1F33"), ("updatesak", "us", r"<b>Update<span>SAK</span></b>", "#0E2A24")):
        head = _inline(k, 28); ic = _inline(k, 22)
        pat = re.compile(r'<svg[^>]*class="mk".*?</svg>\s*' + word, re.S)
        alone = re.compile(r'<svg[^>]*class="mk".*?</svg>', re.S)
        for d, _, fs in os.walk(os.path.join(OUT, site)):
            for f in fs:
                if not f.endswith(".html"): continue
                p = os.path.join(d, f); t = open(p, encoding="utf-8").read()
                if 'class="mk"' not in t: continue
                t = pat.sub(lambda m: head, t); t = alone.sub(lambda m: ic, t)
                if 'id="wm-css"' not in t: t = t.replace("</head>", (CSS % col) + "</head>", 1)
                open(p, "w", encoding="utf-8").write(t); n += 1
    return n
