# -*- coding: utf-8 -*-
"""Saturn web: alur audit berwarna + warna risiko jelas (14 Nov 2026).
High merah, Moderate kuning, Low hijau; bagan 4 tahap (Planning, Penilaian Risiko, Respons Risiko, Pelaporan).
Patch sumber FA-Saturn_SIAP-UPLOAD-v4/saturn/index.html + out/faindonesia/saturn + out/faindonesia-saturn/saturn. Idempoten. --dry"""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
FILES = [os.path.join(ROOT, "FA-Saturn_SIAP-UPLOAD-v4", "saturn", "index.html"),
         os.path.join(ROOT, "out", "faindonesia", "saturn", "index.html"),
         os.path.join(ROOT, "out", "faindonesia-saturn", "saturn", "index.html")]

CSS = """<style id="fa-sat-warna">
:root{--cr-min:#5b6068;--cr-low:#1f9d55;--cr-mod:#f2c230;--cr-high:#e03a3e;--st1:#4f8cff;--st2:#b07cf5;--st3:#19b5a5;--st4:#ef7fb5}
.cell{font-weight:600;font-size:12px}
.cell[data-cr="mod"],.cell[data-cr="mod"] small{color:#1a1400}
.cell[data-cr="min"]{color:#e8eaed}
.cell[data-sr="1"]{box-shadow:inset 0 0 0 3px #fff}
.chip[style*="--cr-mod"]{color:#1a1400!important}
.legend i{width:14px;height:14px}
.flow .fbox{border-top:4px solid var(--stg,var(--line));background:linear-gradient(180deg,color-mix(in srgb,var(--stg,#888) 14%,var(--surface)),var(--surface) 60%)}
.flow .fbox small{color:var(--stg,var(--muted));font-weight:600}
.flow .fbox .rk{display:inline-block;font-size:10.5px;font-weight:600;line-height:1;padding:3px 7px;border-radius:999px;margin:6px 4px 0 0;color:#fff}
.flow .fbox .rk.h{background:var(--cr-high)}.flow .fbox .rk.m{background:var(--cr-mod);color:#1a1400}.flow .fbox .rk.l{background:var(--cr-low)}
.flow .farr{color:var(--muted)}
.flow .farr.gate{color:#f2c230;font-weight:600}
</style>"""

OLD = ("""'<div class="fbox" style="--i:0"><small>B · Planning</small><b>Risiko dan materialitas</b><span>Profil, NCE/Complex, B-7 materialitas, B-8 CRA, walkthrough SCOT</span></div><div class="farr gate">ASM</div>'+
   '<div class="fbox" style="--i:1"><small>C–V · Eksekusi</small><b>Prosedur per akun</b><span>Lead schedule, PSP per asersi, AJE, salah saji</span></div><div class="farr gate">SRM</div>'+
   '<div class="fbox" style="--i:2"><small>Z · Completion</small><b>Kesimpulan</b><span>Peristiwa kemudian, representasi, opini</span></div><div class="farr"></div>'+
   '<div class="fbox fend" style="--i:3"><small>Partner</small><b>LAI ditandatangani</b><span>Terkunci setelah semua sign-off lengkap</span></div></div>'+""")
NEW = ("""'<div class="fbox" style="--i:0;--stg:var(--st1)"><small>1 · Planning (B)</small><b>Kenali entitas dan materialitas</b><span>Penerimaan perikatan, profil, NCE/Complex, B-7 materialitas, walkthrough SCOT</span></div><div class="farr"></div>'+
   '<div class="fbox" style="--i:1;--stg:var(--st2)"><small>2 · Penilaian Risiko (B-8)</small><b>CRA per akun dan asersi</b><span>Risiko bawaan dan kontrol jadi risiko gabungan.</span><div><span class="rk h">Tinggi</span><span class="rk m">Sedang</span><span class="rk l">Rendah</span></div></div><div class="farr gate">ASM</div>'+
   '<div class="fbox" style="--i:2;--stg:var(--st3)"><small>3 · Respons Risiko (C–V)</small><b>Prosedur per akun</b><span>Lead schedule, PSP per asersi, sampel mengikuti tingkat risiko, AJE, salah saji</span></div><div class="farr gate">SRM</div>'+
   '<div class="fbox" style="--i:3;--stg:var(--st4)"><small>4 · Pelaporan (Z)</small><b>Kesimpulan dan opini</b><span>Peristiwa kemudian, representasi, opini, LAI ditandatangani Partner setelah semua sign-off lengkap</span></div></div>'+""")

n = 0
for p in FILES:
    if not os.path.exists(p): print("tidak ada:", p); continue
    t = open(p, encoding="utf-8").read(); o = t
    if 'id="fa-sat-warna"' not in t:
        if "</head>" in t: t = t.replace("</head>", CSS + "</head>", 1)
        else:
            i = t.find("</style>"); assert i > 0
            t = t[:i + 8] + CSS + t[i + 8:]
    if OLD in t: t = t.replace(OLD, NEW, 1)
    elif NEW not in t: print("PERINGATAN: blok flow tidak ketemu di", p)
    if t != o:
        n += 1
        if not DRY: open(p, "w", encoding="utf-8").write(t)
print("file berubah:", n)
