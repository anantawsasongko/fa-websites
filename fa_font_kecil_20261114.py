# -*- coding: utf-8 -*-
"""Font isi FA dikecilkan (14 Nov 2026, Bos: terlalu besar). Body 16.5px -> 15px; .art p/li 17.5px -> 15.5px, line-height 1.75 -> 1.7.
Sapu semua HTML out/faindonesia + prep.py (supaya build ulang tetap). Idempoten. --dry"""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); DRY = "--dry" in sys.argv
R = [('body{font-family:var(--body);font-size:16.5px;letter-spacing:.005em', 'body{font-family:var(--body);font-size:15px;letter-spacing:.005em'),
     ('.art p,.art li{font-family:var(--body)!important;font-size:17.5px!important;line-height:1.75!important', '.art p,.art li{font-family:var(--body)!important;font-size:15.5px!important;line-height:1.7!important')]
def fix(p):
    t = open(p, encoding="utf-8").read(); o = t
    for a, b in R: t = t.replace(a, b)
    if t != o:
        if not DRY: open(p, "w", encoding="utf-8").write(t)
        return 1
    return 0
n = fix(os.path.join(ROOT, "prep.py")); tot = 0
for r, _, fs in os.walk(os.path.join(ROOT, "out", "faindonesia")):
    for f in fs:
        if f.endswith(".html"): tot += fix(os.path.join(r, f))
print("prep.py", n, "html berubah", tot)
