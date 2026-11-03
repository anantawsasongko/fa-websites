# -*- coding: utf-8 -*-
"""Tata letak halaman konten FA (.wrap.art) (3 Nov 2026, keluhan Bos: kap-dhn dsb masih berantakan).
1. CSS: judul bagian diberi jarak dan garis pemisah, lebar baris paragraf dibatasi, tombol/tabel/kartu diberi napas.
2. Pertanyaan Umum yang masih berupa paragraf <p><b>Tanya</b><br>Jawab</p> diubah jadi akordeon (teks tetap di HTML).
Dipanggil prep.py setelah tidy_polish. Idempoten (penanda id="art-layout")."""
import os, re

CSS = ('<style id="art-layout">'
       '.wrap.art{max-width:1000px}'
       '.wrap.art>h1{margin-bottom:18px}'
       '.wrap.art>p.t{max-width:62ch;font-size:17px;line-height:1.7;opacity:.92}'
       '.wrap.art>.cbtns{margin:24px 0 8px;display:flex;flex-wrap:wrap;gap:10px}'
       '.wrap.art h2{font-size:clamp(24px,2.5vw,32px)!important;line-height:1.22;margin:64px 0 18px!important;padding-top:30px;border-top:1px solid rgba(255,255,255,.12)}'
       '.wrap.art>.pf-map+h2,.wrap.art>nav+h2{border-top:0;padding-top:0;margin-top:40px!important}'
       '.wrap.art>p,.wrap.art .pf-fold>p{max-width:68ch;line-height:1.75;margin:0 0 14px}'
       '.wrap.art>p:has(+h2){margin-bottom:0}'
       '.wrap.art .tblwrap,.wrap.art .tidy-tw{margin:20px 0 24px}'
       '.wrap.art .flow5,.wrap.art ol.flow5{margin:20px 0 22px!important;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr))!important;gap:12px!important}''.wrap.art .flow5 li{padding:52px 18px 18px!important}.wrap.art .flow5 li:before{top:16px!important;left:18px!important}.wrap.art .flow5 li b{margin-bottom:6px!important;font-size:15px}'
       '.wrap.art .wj{margin:22px 0 16px}'
       '.wrap.art .pf-more{margin:4px 0 6px}'
       '.wrap.art .faq-acc{max-width:820px;margin:6px 0 26px;border-top:1px solid #333}.wrap.art .faq-i{border-bottom:1px solid #333}.wrap.art .faq-i summary{list-style:none;cursor:pointer;padding:16px 36px 16px 0;position:relative;font-weight:600;line-height:1.45}.wrap.art .faq-i summary::-webkit-details-marker{display:none}.wrap.art .faq-i summary:after{content:"+";position:absolute;right:4px;top:12px;font-size:22px;font-weight:300;transition:transform .25s}.wrap.art .faq-i[open] summary:after{transform:rotate(45deg)}.wrap.art .faq-i p{margin:0 0 16px;opacity:.85}'
       '@media (max-width:640px){.wrap.art h2{margin:44px 0 14px!important;padding-top:22px}.wrap.art>p.t{font-size:16px}}'
       '</style>')

FAQ_P = re.compile(r'<p(?: style="[^"]*")?><b>([^<]{6,220}\?)</b><br/?>(.*?)</p>', re.S)


def faq(t):
    k = t.find(">Pertanyaan Umum</h2>")
    if k < 0: return t, 0
    k += len(">Pertanyaan Umum</h2>")
    m = re.match(r"\s*((?:<p(?: style=\"[^\"]*\")?><b>[^<]{6,220}\?</b><br/?>.*?</p>\s*)+)", t[k:], re.S)
    if not m: return t, 0
    items = FAQ_P.findall(m.group(1))
    if len(items) < 2: return t, 0
    acc = '<div class="faq-acc">' + "".join('<details class="faq-i"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in items) + "</div>"
    return t[:k] + acc + t[k + m.end():], len(items)


def run(root):
    n = f = 0
    for d, _, fs in os.walk(root):
        for x in fs:
            if not x.endswith(".html"): continue
            p = os.path.join(d, x); t = open(p, encoding="utf-8").read()
            if 'class="wrap art"' not in t or 'id="art-layout"' in t: continue
            t, k = faq(t); f += k
            t = t.replace("</head>", CSS + "</head>", 1)
            open(p, "w", encoding="utf-8").write(t); n += 1
    return {"halaman": n, "faq": f}
