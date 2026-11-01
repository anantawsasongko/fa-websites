# -*- coding: utf-8 -*-
"""Rapikan artikel dan halaman konten 3 situs (1 Nov 2026): tabel dibungkus kotak scroll sendiri (kolom tidak menyempit),
garis dan header tabel, jarak judul/paragraf/tabel. Dipanggil prep.py. Idempoten."""
import os, re
CSS = ('<style id="tidy-prose">'
       '.tx{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:10px 0 24px;border:1px solid rgba(127,127,127,.28);border-radius:10px}'
       '.tx table{border-collapse:collapse;width:100%;min-width:560px;margin:0;font-size:.93rem;line-height:1.5}'
       '.tx th,.tx td{padding:11px 14px;text-align:left;vertical-align:top;border-bottom:1px solid rgba(127,127,127,.2);min-width:120px}'
       '.tx th{font-weight:600;background:rgba(127,127,127,.09)}.tx tr:last-child td{border-bottom:0}'
       '.tblwrap table,.scroll table{min-width:560px}.tblwrap th,.tblwrap td,.scroll th,.scroll td{min-width:120px}'
       '.prose h2,article h2{margin-top:34px;margin-bottom:12px}.prose h3,article h3{margin-top:26px;margin-bottom:8px}'
       '.prose h2+p,.prose h3+p,article h2+p,article h3+p,.faq h3+p{margin-top:8px}'
       '.prose p,article p{margin-bottom:14px}.prose li{margin-bottom:6px}'
       '.prose .tx+p,.prose table+p,.prose .scroll+p,.tblwrap+p{margin-top:18px}'
       '.prose img,article img{max-width:100%;height:auto}'
       '.prose,article{overflow-wrap:break-word}'
       '</style>')
SKIP = ("apps", "galaxy", "saturn", "audit-ready", "cek-", "kalkulator", "simulasi", "screening", "bayar")
def _wrap_tables(t):
    out, i = [], 0
    for m in re.finditer(r"<table\b.*?</table>", t, flags=re.S):
        before = t[max(0, m.start() - 200):m.start()]
        if re.search(r'<div[^>]*class="[^"]*\b(tx|tblwrap|scroll|table-wrap|tbl-wrap)\b[^"]*"[^>]*>\s*$', before): continue
        out.append(t[i:m.start()]); out.append('<div class="tx">' + m.group(0) + "</div>"); i = m.end()
    out.append(t[i:]); return "".join(out)
def run(OUT):
    n = 0
    for site in ("faindonesia", "cariakuntan", "updatesak"):
        root = os.path.join(OUT, site)
        for d, _, fs in os.walk(root):
            if "index.html" not in fs: continue
            rel = os.path.relpath(d, root)
            if rel != "." and any(rel.split(os.sep)[0].startswith(s) for s in SKIP): continue
            p = os.path.join(d, "index.html"); t = open(p, encoding="utf-8").read()
            if 'id="tidy-prose"' in t or ("prose" not in t and "<article" not in t and "<table" not in t): continue
            if '<table' in t: t = _wrap_tables(t)
            t = t.replace("</head>", CSS + "</head>", 1)
            open(p, "w", encoding="utf-8").write(t); n += 1
    return n
