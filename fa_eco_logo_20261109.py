#!/usr/bin/env python3
"""9 Nov 2026 (Bos): Lini Usaha di /layanan/ FA.
- Logo CariAkuntan lama (kotak C/A + Poppins) diganti wordmark baru (SVG header cariakuntan.com).
- Tambah kartu UpdateSAK (wordmark header updatesak.com).
- Grid jadi 5 kolom (3 di tablet, 2 di HP, kartu terakhir melebar).
Idempoten. Kerja langsung di out/ dan sumber v58. Blok berpenanda <!--fa-eco5-->.
"""
import re, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent
FILES = [ROOT / "out/faindonesia/layanan/index.html",
         ROOT / "FA-Indonesia_Website_SIAP-UPLOAD-v58/layanan/index.html"]


def logo_svg(site):
    t = (ROOT / f"out/{site}/index.html").read_text(encoding="utf-8")
    i = t.find("<svg", t.find("<header"))
    j = t.find("</svg>", i) + 6
    svg = t[i:j]
    assert 'class="wm"' in svg, site
    return svg.replace('class="wm"', 'class="eco-wm"').replace(' height="28"', "")


CA = logo_svg("cariakuntan")
US = logo_svg("updatesak")

CARDS = (
    '<!--fa-eco5-->'
    '<a class="eco-ca" href="https://cariakuntan.com/" rel="noopener" target="_blank">'
    f'<span aria-label="CariAkuntan" class="lgbox eco-wmbox" role="img">{CA}</span>'
    '<span data-i18n="hs53">Pendampingan Cari KAP, KJPP, dan Profesi Penunjang</span></a>'
    '<a class="eco-ca" href="https://updatesak.com/" rel="noopener" target="_blank">'
    f'<span aria-label="UpdateSAK" class="lgbox eco-wmbox" role="img">{US}</span>'
    '<span data-i18n="kus5">Update PSAK, Kalkulator SAK, dan CALK</span></a>'
    '<!--/fa-eco5-->'
)

CSS = """<style id="fa-eco5">
.eco.eco5{grid-template-columns:repeat(5,minmax(0,1fr))}
.eco.eco5>*{border-right:1px solid var(--line)!important;border-bottom:0!important}
.eco.eco5>*:last-child{border-right:0!important}
.eco .eco-wmbox{height:48px;display:flex;align-items:center;color:var(--ink)}
.eco .eco-wm{height:30px;width:auto;max-width:100%;display:block;transition:transform .35s var(--ez)}
.eco a.eco-ca:hover .eco-wm{transform:scale(1.06);transform-origin:left center}
@media (max-width:1100px){.eco.eco5{grid-template-columns:repeat(3,minmax(0,1fr))}
.eco.eco5>*{border-bottom:1px solid var(--line)!important}
.eco.eco5>*:nth-child(3n){border-right:0!important}
.eco.eco5>*:nth-child(n+4){border-bottom:0!important}
.eco.eco5>*:last-child{grid-column:span 2}}
@media (max-width:860px){.eco.eco5{grid-template-columns:repeat(2,minmax(0,1fr))}
.eco.eco5>*,.eco.eco5>*:nth-child(3n),.eco.eco5>*:nth-child(n+4){border-right:1px solid var(--line)!important;border-bottom:1px solid var(--line)!important}
.eco.eco5>*:nth-child(2n){border-right:0!important}
.eco.eco5>*:last-child{grid-column:1/-1;border-right:0!important;border-bottom:0!important}}
@media (max-width:600px){.eco .eco-wm{height:25px}}
</style>"""

I18N = {"en": "PSAK updates, SAK calculators, and notes to financial statements",
        "zh": "PSAK 更新、SAK 计算器与财务报表附注"}


def patch(t):
    # kartu
    if "<!--fa-eco5-->" in t:
        t = re.sub(r"<!--fa-eco5-->.*?<!--/fa-eco5-->", lambda m: CARDS, t, count=1, flags=re.S)
    else:
        t2 = re.sub(r'<a class="eco-ca" href="https://cariakuntan\.com/".*?</a>', lambda m: CARDS, t, count=1, flags=re.S)
        assert t2 != t, "kartu CA lama tidak ketemu"
        t = t2
    # kelas grid
    t = re.sub(r'<div class="eco">(?=(?:(?!<div class="eco).)*?<!--fa-eco5-->)', '<div class="eco eco5">', t, count=1, flags=re.S)
    # CSS
    t = re.sub(r'<style id="fa-eco5">.*?</style>', "", t, flags=re.S)
    t = t.replace("</head>", CSS + "</head>", 1)
    # i18n
    done = '"kus5": ' in t
    for lang, txt in I18N.items():
        if done:
            break
        assert f'"{lang}": {{' in t, lang
        t = t.replace(f'"{lang}": {{', f'"{lang}": {{"kus5": {json.dumps(txt, ensure_ascii=False)}, ', 1)
    return t


for f in FILES:
    if not f.exists():
        print("skip", f); continue
    t = f.read_text(encoding="utf-8")
    n = patch(t)
    assert 'class="eco eco5"' in n and n.count("<!--fa-eco5-->") == 1
    f.write_text(n, encoding="utf-8")
    print("ok", f.relative_to(ROOT), n.count('"kus5"'))
