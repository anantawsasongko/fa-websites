# -*- coding: utf-8 -*-
"""3 Nov 2026: tiga wajah ekosistem FA. FA = Ananta, KJA = Farhani, KAP = Dwi (foto masing-masing).
Mengganti tabel 'Tim yang Menangani' di halaman layanan dan kecamatan dengan kartu foto, dan memasang kartu di halaman inti.
Juga profil Dwi Haryadi Nugraha di /kap-dhn/. Idempoten (penanda fa-wajah). Jalankan setelah fa_peluang_20261103.py."""
import os, re, glob
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FA-Indonesia_Website_SIAP-UPLOAD-v58")
CSS = ('<style id="fa-wajah-css">.wj{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:14px 0 10px}'
 '.wj a{display:block;border:1px solid #333;border-radius:12px;overflow:hidden;background:#1e1e1e;color:inherit;text-decoration:none}'
 '.wj a:hover{border-color:#777}.wj img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 18%}'
 '.wj div{padding:12px 14px 14px}.wj small{display:block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;opacity:.7;margin-bottom:4px}'
 '.wj b{display:block;font-size:15.5px;line-height:1.3;font-weight:600}.wj span{display:block;font-size:12.5px;line-height:1.45;opacity:.75;margin-top:4px}'
 '@media(max-width:620px){.wj{grid-template-columns:1fr;gap:10px}.wj a{display:grid;grid-template-columns:96px 1fr;align-items:center}.wj img{aspect-ratio:1/1;height:100%}}'
 '</style>')
CARDS = [
 ("/ananta-w-sasongko/", "/img/ananta-w-sasongko-cpa.jpg", "FA Indonesia", "Ananta W. Sasongko, CPA", "Koordinator, kredit, investor, dan pendampingan audit"),
 ("/kja-farhani/", "/img/farhani-k-nugraha-fa-indonesia.jpg", "KJA Farhani", "Farhani Kautsar Nugraha, S.E., M.S.A., Ak., CA", "Pembukuan dan penyusunan laporan keuangan"),
 ("/kap-dhn/", "/img/dwi-haryadi-nugraha-kap-dhn-v2.jpg", "KAP DHN &amp; Rekan", "Dr. (C) Dwi Haryadi Nugraha, SST, MSi, Ak, CA, BKP, ASEAN CPA, CPA, CFI", "Pemimpin Rekan, audit laporan keuangan"),
]
def block(title="Tim yang Menangani"):
    cards = "".join(f'<a href="{h}"><img src="{im}" alt="{n}" width="700" height="1050" loading="lazy" decoding="async"><div><small>{r}</small><b>{n}</b><span>{d}</span></div></a>' for h, im, r, n, d in CARDS)
    return (f'<!--fa-wajah--><h2>{title}</h2><div class="wj">{cards}</div>'
            '<p>Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda. Hubungi kami lewat tombol WhatsApp di halaman ini.</p><!--/fa-wajah-->')
TEAM_RE = re.compile(r"<h2>Tim yang Menangani</h2><div class=\"tblwrap\"><table>.*?</table></div><p>Untuk satu entitas.*?</p>", re.S)
def put(p, title="Tim yang Menangani"):
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"<!--fa-wajah-->.*?<!--/fa-wajah-->", "", t, flags=re.S)
    if TEAM_RE.search(t): t = TEAM_RE.sub(lambda m: block(title), t, count=1)
    else:
        k = t.find("<h2>Pertanyaan Umum</h2>")
        if k < 0: k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
        if k < 0: k = t.rfind("</main>")
        t = t[:k] + block(title) + t[k:]
    if "fa-wajah-css" not in t: t = t.replace("</head>", CSS + "</head>", 1)
    open(p, "w", encoding="utf-8").write(t)
n = 0
# halaman yang sudah punya tabel tim (layanan sektor + kecamatan)
for p in glob.glob(os.path.join(B, "wilayah", "*", "kecamatan", "*", "index.html")) + [os.path.join(B, x, "index.html") for x in ("audit-dana-kampanye", "audit-koperasi-desa-merah-putih", "laporan-keuangan-audit-sppg")]:
    if os.path.exists(p): put(p); n += 1
# halaman inti
CORE = ["kja-farhani", "kap-dhn", "jasa-audit-laporan-keuangan", "mitra-notaris", "mitra-kap-kja", "laporan-keuangan-umkm", "jasa-penyusunan-laporan-keuangan",
        "laporan-tahunan-pt", "layanan", "audit-back-office-kap", "konsultan-kredit-bank"] + [f"wilayah/{c}" for c in os.listdir(os.path.join(B, "wilayah")) if os.path.isdir(os.path.join(B, "wilayah", c))]
for x in CORE:
    p = os.path.join(B, x, "index.html")
    if os.path.exists(p): put(p, "Tiga Orang di Balik FA, KJA, dan KAP"); n += 1
# profil Dwi di /kap-dhn/
p = os.path.join(B, "kap-dhn", "index.html"); t = open(p, encoding="utf-8").read()
t = re.sub(r"<!--fa-dwi-->.*?<!--/fa-dwi-->", "", t, flags=re.S)
dwi = ('<!--fa-dwi--><h2>Dr. (C) Dwi Haryadi Nugraha, SST, MSi, Ak, CA, BKP, ASEAN CPA, CPA, CFI</h2>'
       '<p>Pemimpin Rekan KAP DHN &amp; Rekan, akuntan publik dengan nomor register AP.1723. Memimpin perikatan audit laporan keuangan, audit BPR dan lembaga keuangan, serta prosedur yang disepakati untuk perusahaan di Bali, Kalimantan Timur, dan seluruh Indonesia.</p><!--/fa-dwi-->')
k = t.find("<!--fa-wajah-->"); k = k if k > 0 else t.find("<h2>Pertanyaan Umum</h2>")
open(p, "w", encoding="utf-8").write(t[:k] + dwi + t[k:])
print("fa_wajah", n)
