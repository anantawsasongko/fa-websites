#!/usr/bin/env python3
"""27 Nov 2026: logo PA Global di semua kartu KAP DHN (FA, CA, US), tanpa mengubah desain kartu.

Bos: "Boleh dipasang di semua kartu, tapi jangan mengubah design keseluruhan kartu yang sudah bagus."
Dasar: KAP DHN & Rekan tercatat "Member of PA Global" di pa-global.com/locations/indonesia/
kap-dwi-haryadi-nugraha-partner/ (dicek 27 Nov 2026). Logo hanya tampil DI DALAM kartu KAP DHN,
sebagai keterangan keanggotaan KAP DHN. JANGAN dipasang di header, footer, hero, atau kartu lain:
FA, CariAkuntan, UpdateSAK, dan KJA Farhani bukan anggota PA Global.

Yang ditambah: satu baris kecil di bawah nama "KAP DHN & Rekan" (label + logo di atas alas putih
supaya terbaca di latar gelap maupun terang). Struktur, ukuran, warna, dan tombol kartu tetap.
Bekerja di out/ tiga situs. Idempoten, --dry. Jalankan sesudah semua generator kartu dhn.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
SITES = ("faindonesia", "cariakuntan", "updatesak")

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 279.44 71.07" role="img" aria-label="PA Global"><title>PA Global</title>
<g><polygon fill="#002c54" points="7.02 39.26 19.69 17.32 7.84 17.32 0 30.9 7.02 39.26"/><polygon fill="#002c54" points="15.79 49.71 37.91 11.4 26.07 11.4 8.77 41.35 15.79 49.71"/><polygon fill="#77c043" points="56.14 5.47 36.9 38.79 25.06 38.79 44.29 5.47 56.14 5.47"/><polygon fill="#002c54" points="24.56 60.17 17.54 51.8 23.58 41.35 35.42 41.35 24.56 60.17"/><polygon fill="#43a548" points="55.13 32.86 74.36 -.45 62.52 -.45 43.28 32.86 55.13 32.86"/><polygon fill="#002c54" points="33.33 70.62 26.31 62.26 41.8 35.43 53.65 35.43 33.33 70.62"/></g>
<g fill="#002c54"><path d="M98.41,17.32h-12.21v35.53h5.27v-14.45h0s6.94,0,6.94,0c5.82,0,10.54-4.72,10.54-10.54s-4.72-10.54-10.54-10.54ZM98.41,33.13h-6.94v-10.53h6.94c2.9,0,5.27,2.36,5.27,5.27s-2.36,5.27-5.27,5.27Z"/><path d="M125.12,17.32h-5.27l-12.93,35.53h5.27l3.44-9.48h13.71l3.44,9.48h5.27l-12.93-35.53ZM117.44,38.4l5.05-13.84,5.05,13.84h-10.09Z"/>
<path d="M201.55,27.87c-6.77,0-12.25,5.59-12.25,12.49s5.48,12.49,12.25,12.49,12.25-5.59,12.25-12.49-5.49-12.49-12.25-12.49ZM207.95,43.5c-.38.94-.9,1.73-1.55,2.37-.65.64-1.39,1.13-2.22,1.48-.83.35-1.73.53-2.62.53s-1.79-.17-2.62-.53c-.83-.35-1.57-.84-2.22-1.48-.65-.64-1.17-1.43-1.55-2.37-.38-.94-.58-1.96-.58-3.14s.19-2.2.58-3.14c.38-.94.9-1.73,1.55-2.37.65-.64,1.39-1.13,2.22-1.49.83-.35,1.73-.52,2.62-.52s1.79.17,2.62.52c.83.35,1.57.85,2.22,1.49.65.64,1.17,1.43,1.55,2.37.38.94.58,1.96.58,3.14s-.19,2.2-.58,3.14Z"/>
<path d="M175.71,33.42v14.3c-1.52,1.5-3.3,2.73-5.27,3.6-2.21.98-4.65,1.53-7.22,1.53-9.81,0-17.77-7.95-17.77-17.77s7.95-17.77,17.77-17.77c2.57,0,5.01.54,7.22,1.53,1.2.53,2.32,1.19,3.36,1.97l-3.4,4.05c-2.03-1.43-4.51-2.27-7.18-2.27-6.89,0-12.49,5.61-12.49,12.49s5.6,12.49,12.49,12.49c2.69,0,5.18-.85,7.22-2.3v-6.88h-7.22v-4.97h12.49Z"/>
<rect x="180.27" y="17.32" width="5.27" height="35.53"/><rect x="274.17" y="17.32" width="5.27" height="35.53"/>
<path d="M217.56,17.32v35.53s5.27,0,5.27,0v-3.47c1.09,1.08,3.89,3.38,7.73,3.47,4.83.11,7.83-3.07,8.46-3.81,2.03-2.37,3.04-5.52,3.04-8.68s-1.02-6.31-3.04-8.68c-.63-.74-3.63-3.92-8.46-3.81-3.83.09-6.63,2.39-7.73,3.47v-14.02s-5.27,0-5.27,0ZM222.83,40.36c0-1.18.19-2.2.58-3.14.38-.94.9-1.73,1.55-2.37.65-.64,1.39-1.13,2.22-1.49.83-.35,1.73-.52,2.62-.52s1.79.17,2.62.52c.83.35,1.57.85,2.22,1.49.65.64,1.17,1.43,1.55,2.37.38.94.58,1.96.58,3.14s-.19,2.2-.58,3.14c-.38.94-.9,1.73-1.55,2.37-.65.64-1.39,1.13-2.22,1.48-.83.35-1.73.53-2.62.53s-1.79-.17-2.62-.53c-.83-.35-1.57-.84-2.22-1.48-.65-.64-1.17-1.43-1.55-2.37-.38-.94-.58-1.96-.58-3.14Z"/>
<path d="M263.95,27.87v3.47c-1.09-1.08-3.89-3.38-7.73-3.47-4.83-.11-7.83,3.07-8.46,3.81-2.03,2.37-3.04,5.52-3.04,8.68s1.02,6.31,3.04,8.68c.63.74,3.63,3.92,8.46,3.81,3.83-.09,6.63-2.39,7.73-3.47v3.47s5.27,0,5.27,0v-24.99h-5.27ZM263.37,43.5c-.38.94-.9,1.73-1.55,2.37-.65.64-1.39,1.13-2.22,1.48-.83.35-1.73.53-2.62.53s-1.79-.17-2.62-.53c-.83-.35-1.57-.84-2.22-1.48-.65-.64-1.17-1.43-1.55-2.37-.38-.94-.58-1.96-.58-3.14s.19-2.2.58-3.14c.38-.94.9-1.73,1.55-2.37.65-.64,1.39-1.13,2.22-1.49.83-.35,1.73-.52,2.62-.52s1.79.17,2.62.52c.83.35,1.57.85,2.22,1.49.65.64,1.17,1.43,1.55,2.37.38.94.58,1.96.58,3.14s-.19,2.2-.58,3.14Z"/></g>
</svg>
'''

CSS = ('<style id="pag-css">.dhnc .pag{display:inline-flex;align-items:center;align-self:flex-start;gap:7px;margin:0 0 8px;'
       "font-size:11px;letter-spacing:.04em;line-height:1;opacity:.85}"
       ".dhnc .pag img.pagl{width:auto!important;height:15px!important;flex:none!important;margin:0!important;object-fit:contain;"
       "background:#fff;padding:3px 6px;border-radius:4px;box-sizing:content-box}</style>")
NAMA = '<b class="n">KAP DHN &amp; Rekan</b>'


def baris(en):
    return ('<!--pag--><span class="pag">%s<img class="pagl" src="/img/pa-global.svg" alt="PA Global" width="59" height="15" loading="lazy"></span><!--/pag-->'
            % ("Member of" if en else "Anggota jaringan"))


def fix(s):
    if NAMA not in s or 'class="dhnc"' not in s:
        return s
    s = re.sub(r"<!--pag-->.*?<!--/pag-->", "", s, flags=re.S)

    def kartu(m):
        k = m.group(0)
        en = "Public Accounting Firm" in k
        return k.replace(NAMA, NAMA + baris(en), 1)
    s = re.sub(r'<aside (?:class="dhnc" aria-label="KAP DHN &amp; Rekan"|aria-label="KAP DHN &amp; Rekan" class="dhnc")>.*?</aside>', kartu, s, flags=re.S)
    if "<!--pag-->" in s and 'id="pag-css"' not in s:
        s = s.replace("</head>", CSS + "</head>", 1)
    return s


def run():
    for site in SITES:
        root = os.path.join(ROOT, "out", site)
        svg = os.path.join(root, "img", "pa-global.svg")
        if not DRY and (not os.path.exists(svg) or open(svg, encoding="utf-8").read() != SVG):
            os.makedirs(os.path.dirname(svg), exist_ok=True)
            open(svg, "w", encoding="utf-8").write(SVG)
        n = kartu = 0
        for f in glob.glob(os.path.join(root, "**", "*.html"), recursive=True):
            old = open(f, encoding="utf-8", errors="ignore").read()
            new = fix(old)
            kartu += new.count("<!--pag-->")
            if new != old:
                n += 1
                if not DRY:
                    open(f, "w", encoding="utf-8").write(new)
        print("%-12s file berubah %5d, kartu berlogo %5d%s" % (site, n, kartu, " (dry)" if DRY else ""))


if __name__ == "__main__":
    run()
