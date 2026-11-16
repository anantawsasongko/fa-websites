#!/usr/bin/env python3
"""16 Nov 2026: Asisten AI (widget fa-ai.js) di beranda FA, CA, US.
Sebelumnya fa-ai.js hanya dipasang di halaman ber-paywall/donasi (FA 22 dari 12.237, CA 0, US 1).
Idempoten, penanda <!--fa-ai-home-->. --dry hanya melaporkan. Jalankan SESUDAH prep.py dan fa_*_rapi terakhir.
API tetap di faindonesia.co.id (CORS sudah mengizinkan cariakuntan.com dan updatesak.com)."""
import os, re, shutil, sys
M = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
SRC_JS = None
for p in ("out/updatesak/js/fa-ai.js", "out/faindonesia/js/fa-ai.js"):
    if os.path.exists(os.path.join(M, p)): SRC_JS = os.path.join(M, p); break
V = "20261116"
SITES = {"faindonesia": "beranda-fa", "cariakuntan": "beranda-ca", "updatesak": "beranda-us"}
for site, app in SITES.items():
    root = os.path.join(M, "out", site)
    dst = os.path.join(root, "js", "fa-ai.js")
    if not os.path.exists(dst):
        print(site, "copy js/fa-ai.js")
        if not DRY: os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(SRC_JS, dst)
    pth = os.path.join(root, "index.html")
    t = open(pth, encoding="utf-8").read()
    if "<!--fa-ai-home-->" in t: print(site, "sudah ada"); continue
    t = re.sub(r'<script[^>]*src="/js/fa-ai\.js[^"]*"[^>]*></script>', "", t)  # buang pasangan lama agar tidak dobel
    tag = '<!--fa-ai-home--><script>window.FA_AI={app:"%s"}</script><script src="/js/fa-ai.js?v=%s" defer></script>' % (app, V)
    assert t.count("</body>") == 1, site
    t = t.replace("</body>", tag + "</body>", 1)
    print(site, "dipasang")
    if not DRY: open(pth, "w", encoding="utf-8").write(t)
