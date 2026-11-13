# -*- coding: utf-8 -*-
"""13 Nov 2026 (Bos): blok "Dikerjakan dengan Tools Buatan FA Sendiri" harus lebih meyakinkan di semua halaman:
"Ada video lho. At least bagan animasi."
Di setiap blok <!--fa-tools--> (±3.578 halaman FA):
  1. Bagan alur animasi (CSS, tanpa gambar) setelah paragraf pembuka: Data Anda -> FA Jupiter -> FA Saturn -> FA Venus -> Keputusan.
     Penanda <!--fa-tanim-->. Bukan heading, jadi struktur H2/Peta Isi tidak berubah.
  2. Video pratinjau 30 detik (360x640, tanpa suara, <700 KB) di atas tiap kartu FA Jupiter/Saturn/Venus
     (media/prev-fa-<app>.mp4 + poster .jpg, dibuat dari media/cara-kerja-fa-<app>.mp4). preload="none";
     js/fa-tanim.js baru memuat dan memutar video saat kartu terlihat, berhenti saat keluar layar.
  3. <link id="fa-tanim-css"> di <head>, <script id="fa-tanim-js"> sebelum </body>.
Teks, link, dan id lama tidak berubah. Idempoten. Jalankan paling akhir (setelah fa_daerah_lipat_20261113.py; blok di dalam lipatan tetap di tempat).
"""
import os, re, glob, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "faindonesia")
V = "20261113c"
CSS = f'<link href="/css/fa-tanim.css?v={V}" id="fa-tanim-css" rel="stylesheet"/>'
JS = f'<script defer id="fa-tanim-js" src="/js/fa-tanim.js?v={V}"></script>'
DIAG = ('<!--fa-tanim--><div aria-label="Alur kerja FA Indonesia" class="ftan" role="img"><p class="ttl">Alur Kerja FA <i>dari data mentah sampai keputusan</i></p><ol>'
        '<li class="d"><span class="n">01</span><div><b>Data Anda</b><span>Neraca saldo, rekening koran, dokumen</span></div></li>'
        '<li class="j"><span class="n">02</span><div><b>FA Jupiter</b><span>Laporan keuangan siap audit</span></div></li>'
        '<li class="s"><span class="n">03</span><div><b>FA Saturn</b><span>Diuji seperti KAP: materialitas, asersi</span></div></li>'
        '<li class="v"><span class="n">04</span><div><b>FA Venus</b><span>Model kredit, valuasi, IPO</span></div></li>'
        '<li class="k"><span class="n">05</span><div><b>Keputusan</b><span>Bank, investor, auditor</span></div></li>'
        '</ol><div aria-hidden="true" class="bar"><i></i><i></i><i></i><i></i><i></i></div></div><!--/fa-tanim-->')
def vid(app):
    return (f'<span aria-hidden="true" class="ftv"><video data-src="/media/prev-fa-{app}.mp4" loop muted playsinline preload="none" '
            f'poster="/media/prev-fa-{app}.jpg"></video></span>')
RX_D = re.compile(r"<!--fa-tanim-->.*?<!--/fa-tanim-->", re.S)
RX_V = re.compile(r'<span aria-hidden="true" class="ftv">.*?</span>', re.S)
def blk(m):
    b = RX_V.sub("", RX_D.sub("", m.group(1)))
    i = b.find('<div class="ftl">')
    j = b.rfind("</p>", 0, i)
    if i < 0 or j < 0: return m.group(0)
    b = b[:j + 4] + DIAG + b[j + 4:]
    b = re.sub(r'(<a href="[^"]*">)(<small>FA (Jupiter|Saturn|Venus)</small>)', lambda x: x.group(1) + vid(x.group(3).lower()) + x.group(2), b)
    return "<!--fa-tools-->" + b + "<!--/fa-tools-->"
n = 0
for p in glob.glob(os.path.join(OUT, "**", "index.html"), recursive=True):
    t = open(p, encoding="utf-8").read()
    if "<!--fa-tools-->" not in t: continue
    t2 = re.sub(r"<!--fa-tools-->(.*?)<!--/fa-tools-->", blk, t, flags=re.S)
    t2 = re.sub(r'<link href="/css/fa-tanim\.css[^"]*" id="fa-tanim-css" rel="stylesheet"/>', "", t2)
    t2 = re.sub(r'<script defer id="fa-tanim-js" src="[^"]*"></script>', "", t2)
    t2 = t2.replace("</head>", CSS + "</head>", 1).replace("</body>", JS + "</body>", 1)
    if t2 != t:
        open(p, "w", encoding="utf-8").write(t2); n += 1
print("halaman", n)
