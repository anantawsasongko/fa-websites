# -*- coding: utf-8 -*-
"""Poles global 3 situs (3 Nov 2026 malam, audit kerapian semua template):
1. Tabel di HP: kolom pertama tidak lagi melebar sampai mendorong kolom lain keluar layar; sel isi diberi lebar baca minimal.
   Tabel tetap tabel dan bergulir di kotaknya sendiri.
2. UpdateSAK Sertifikasi: kartu .exgrid tidak lagi 2 kolom sempit di HP / 4 kolom sempit di laptop.
3. FA: halaman yang sudah memuat kartu Tiga Orang tidak lagi menampilkan foto Ananta kedua kali di kotak Penulis.
Idempoten (penanda id="polish-global")."""
import os, re
CSS = ('<style id="polish-global">'
       '@media (max-width:700px){'
       '.tblwrap table th:first-child,.tidy-tw table th:first-child,.scroll table th:first-child,table th[scope=row]{min-width:118px!important;width:140px;max-width:150px;white-space:normal!important}'
       '.tblwrap td,.tidy-tw td,.scroll td{min-width:168px!important;white-space:normal}'
       '}'
       '.exgrid{grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr))!important}'
       '</style>')
AUTHOR = re.compile(r'(<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333;[^"]*?)grid-template-columns:72px minmax\(0,1fr\);([^"]*">)<img[^>]*ananta-w-sasongko-cpa\.jpg[^>]*>')


def run(roots):
    n = a = 0
    for root in roots:
        for d, _, fs in os.walk(root):
            for x in fs:
                if not x.endswith(".html"): continue
                p = os.path.join(d, x); t = open(p, encoding="utf-8").read()
                if 'id="polish-global"' in t or "</head>" not in t: continue
                if 'class="wj"' in t:
                    t, k = AUTHOR.subn(lambda m: m.group(1) + "grid-template-columns:minmax(0,1fr);" + m.group(2), t); a += k
                t = t.replace("</head>", CSS + "</head>", 1)
                open(p, "w", encoding="utf-8").write(t); n += 1
    return {"halaman": n, "foto penulis dobel dihapus": a}
