# -*- coding: utf-8 -*-
"""Tunda semua pembelian sampai Midtrans aktif (1 Nov 2026, permintaan Bos).
- Tombol beli (href /bayar/?produk=...) jadi label nonaktif "Segera Dibuka".
- Link footer "Pembayaran" dihapus. Link /bayar/ lain jadi teks biasa.
- QRIS hanya untuk donasi (donasi.js, tidak disentuh).
Halaman /bayar/ asli (Snap + invoice) disimpan di backup/pembayaran-20261101/ untuk dipulihkan saat Midtrans aktif:
cukup kembalikan file itu dan hapus pemanggilan modul ini di prep.py."""
import os, re
CSS = ('<style id="pay-soon-css">.pay-soon{opacity:.6;cursor:not-allowed;pointer-events:none;white-space:nowrap}'
       '.pay-soon-note{font-size:.85rem;opacity:.7;margin-top:6px}</style>')
BUY = re.compile(r'<a\b([^>]*?)href="(?:https://faindonesia\.co\.id)?/bayar/\?[^"]*"([^>]*)>(.*?)</a>', re.S)
FOOT = re.compile(r'(\s*·\s*)?<a\b[^>]*href="(?:https://faindonesia\.co\.id)?/bayar/"[^>]*>\s*Pembayaran\s*</a>')
FOOTLI = re.compile(r'<li>\s*<a\b[^>]*href="(?:https://faindonesia\.co\.id)?/bayar/"[^>]*>\s*Pembayaran\s*</a>\s*</li>')
OTHER = re.compile(r'<a\b([^>]*?)href="(?:https://faindonesia\.co\.id)?/bayar/(?:selesai/)?"([^>]*)>(.*?)</a>', re.S)
def _cls(attrs):
    m = re.search(r'class="([^"]*)"', attrs); return m.group(1) if m else ""
def _buy(m):
    attrs = m.group(1) + m.group(2); inner = m.group(3)
    txt = re.sub(r"<[^>]+>", "", inner).strip()
    lab = "Segera Dibuka" if re.match(r"^(Beli|Bayar)\b", txt) else inner
    return f'<a class="{_cls(attrs)} pay-soon" role="link" aria-disabled="true" tabindex="-1" title="Pembayaran online segera dibuka">{lab}</a>'
def _other(m):
    attrs = m.group(1) + m.group(2)
    return f'<a class="{_cls(attrs)} pay-soon" role="link" aria-disabled="true" tabindex="-1">{m.group(3)}</a>'
def run(OUT):
    n = 0
    for site in os.listdir(OUT):
        root = os.path.join(OUT, site)
        if not os.path.isdir(root): continue
        for d, _, fs in os.walk(root):
            rel = os.path.relpath(d, root).replace(os.sep, "/")
            if rel.startswith("bayar") or rel.startswith("toko/uji"): continue
            for f in fs:
                if not f.endswith(".html"): continue
                p = os.path.join(d, f); t = open(p, encoding="utf-8").read()
                t0 = t
                t = t.replace('/js/fa-paywall.js"', '/js/fa-paywall.js?v=20261102b"').replace('/js/fa-ai.js"', '/js/fa-ai.js?v=20261102b"')
                if t != t0: open(p, "w", encoding="utf-8").write(t)
                if "/bayar/" not in t: continue
                o = t
                t = FOOTLI.sub("", t); t = FOOT.sub("", t)
                t = BUY.sub(_buy, t)
                body = t.find("<body")
                if body > 0:
                    head, rest = t[:body], t[body:]
                    rest = OTHER.sub(_other, rest); t = head + rest
                if t != o:
                    if "pay-soon-css" not in t and "pay-soon" in t: t = t.replace("</head>", CSS + "</head>", 1)
                    open(p, "w", encoding="utf-8").write(t); n += 1
    return n
