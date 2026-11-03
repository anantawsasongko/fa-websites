# -*- coding: utf-8 -*-
"""3 Nov 2026: UpdateSAK hijau putih sesuai logo (#0E7C66). Mengganti aksen biru di semua file keluaran updatesak."""
import os, re
MAP = [("#1F5BFF", "#0E7C66"), ("#1f5bff", "#0E7C66"), ("#8FB2FF", "#7EE0C3"), ("#8fb2ff", "#7EE0C3"), ("#EAF0FF", "#E6F3EE"), ("#eaf0ff", "#E6F3EE"),
       ("rgba(31,91,255", "rgba(14,124,102"), ("rgba(31, 91, 255", "rgba(14, 124, 102"), ("#0EA5E9", "#12A39A"),
       ("--ink:#0B1F33", "--ink:#0F241F"), ("--deep:#0B1F33", "--deep:#0E2A24"), ("--panel:#F3F5F8", "--panel:#F2F6F4"), ("--line:#DCE2E9", "--line:#D9E3DF"),
       ("--muted:#516173", "--muted:#4F625C"), ("#24384C", "#2A3F39"), ("#f5f7fb", "#F3F7F5"), ("#e8edf5", "#E5EEEA"), ("#d5dbe5", "#D3E0DA"), ("#F3F5F8", "#F2F6F4")]
def run(root):
    n = 0
    for d, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith((".html", ".css", ".js", ".svg", ".xml")): continue
            p = os.path.join(d, f)
            try: t = open(p, encoding="utf-8").read()
            except Exception: continue
            t2 = t
            for a, b in MAP: t2 = t2.replace(a, b)
            if t2 != t: open(p, "w", encoding="utf-8").write(t2); n += 1
    return n
