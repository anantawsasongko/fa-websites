"""Rapikan blok sisipan (kotak CTA, strip KAP DHN/KJA) agar sejajar dengan lebar konten situs (2 Nov 2026).
Masalah: kotak CTA dengan style inline disisipkan langsung di <main> yang selebar layar, jadi melebar penuh
dan teksnya nempel kiri, tidak sejajar dengan isi halaman dan strip KAP DHN."""
import os
W = {"faindonesia": "1080px", "cariakuntan": "1008px", "updatesak": "1008px", "kja-farhani": "1008px"}
def css(w):
    sel = ('main>div[style*="border:1px solid"],main>aside[style*="border:1px solid"],main>section[style*="border:1px solid"],'
           'body>div[style*="border:1px solid"]:not([id]):not([class])')
    return ('<style id="tidy-layout">' + sel + '{box-sizing:border-box;width:min(' + w + ',calc(100% - 40px))!important;'
            'margin-left:auto!important;margin-right:auto!important}'
            '.dhns,.dhnc{box-sizing:border-box;width:min(' + w + ',calc(100% - 40px))!important;margin-left:auto!important;margin-right:auto!important}'
            '</style>')
def run(OUT):
    n = 0
    for site, w in W.items():
        root = os.path.join(OUT, site)
        if not os.path.isdir(root): continue
        tag = css(w)
        for d, _, fs in os.walk(root):
            for f in fs:
                if not f.endswith(".html"): continue
                p = os.path.join(d, f); t = open(p, encoding="utf-8").read()
                if 'id="tidy-layout"' in t or "</head>" not in t: continue
                t = t.replace("</head>", tag + "</head>", 1); open(p, "w", encoding="utf-8").write(t); n += 1
    return n
