# -*- coding: utf-8 -*-
"""3 Nov 2026 (permintaan Bos: 'lipat semua'): daftar link panjang di halaman kota, kawasan, kecamatan, dan artikel
dilipat jadi <details> satu baris. Link tetap ada di HTML (aman untuk SEO), tampilan rapi. Kotak promo (pb-box) dan KAP DHN tidak dilipat."""
import os, re
CSS = ('<style id="fold-css">.fold{margin-top:30px;border-top:1px solid var(--line,#333);padding-top:14px}.fold summary{cursor:pointer;list-style:none;font-weight:600;display:flex;justify-content:space-between;align-items:center;gap:12px}'
       '.fold summary::-webkit-details-marker{display:none}.fold summary::after{content:"+";font-size:1.3em;line-height:1;opacity:.7}.fold[open] summary::after{content:"\\2212"}.fold .citylist,.fold p{margin-top:12px}</style>')
CA_RE = re.compile(r'<div class="more(?! pb-box)(?:\s[^"]*)?">\s*<h3>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)?(?:<div class="citylist">.*?</div>|(?:<a [^>]*>.*?</a>\s*){4,}))\s*</div>', re.S)
FA_RE = re.compile(r'<h2(?: [^>]*)?>([^<]{3,120})</h2>\s*(<p class="t">((?:(?!</p>).)*)</p>)', re.S)
US_RE = re.compile(r'<h2(?: [^>]*)?>((?:Standar Lain di Kelompok Ini|Standar Terkait|PSAK Terkait|Artikel Terkait|Baca Juga)[^<]*)</h2>\s*(<div class="sagrid">(?:(?!</div>).)*</div>)', re.S)
US_RE = re.compile(r'<h2(?: [^>]*)?>((?:Standar Lain di Kelompok Ini|Standar Terkait|PSAK Terkait|Artikel Terkait|Baca Juga)[^<]*)</h2>\s*(<div class="sagrid">(?:(?!</div>).)*</div>)', re.S)
def _many_links(inner):
    n = inner.count("<a ")
    txt = re.sub(r"<a [^>]*>.*?</a>", "", inner, flags=re.S); txt = re.sub(r"<[^>]+>|[·\s,.]", "", txt)
    return n >= 4 and len(txt) < 40
def run(root, kind):
    c = 0
    for d, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith(".html"): continue
            p = os.path.join(d, f); t = open(p, encoding="utf-8").read(); t0 = t
            if kind == "ca":
                t = CA_RE.sub(lambda m: f'<details class="fold"><summary>{m.group(1)}</summary>{m.group(2)}</details>' if m.group(2).count("<a ") >= 4 else m.group(0), t)
            elif kind == "us":
                t = US_RE.sub(lambda m: f'<details class="fold"><summary>{m.group(1)}</summary>{m.group(2)}</details>' if m.group(2).count("<a ") >= 4 else m.group(0), t)
            elif kind == "us":
                t = US_RE.sub(lambda m: f'<details class="fold"><summary>{m.group(1)}</summary>{m.group(2)}</details>' if m.group(2).count("<a ") >= 4 else m.group(0), t)
            else:
                t = FA_RE.sub(lambda m: f'<details class="fold"><summary>{m.group(1)}</summary>{m.group(2)}</details>' if _many_links(m.group(3)) else m.group(0), t)
            if t != t0:
                if "fold-css" not in t: t = t.replace("</head>", CSS + "</head>", 1)
                open(p, "w", encoding="utf-8").write(t); c += 1
    return c
