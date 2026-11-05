# -*- coding: utf-8 -*-
"""Area layanan per kota (5 Nov 2026). Dipanggil dari prep.py sebelum thin_noindex.
Masalah: halaman kecamatan sengaja noindex (halaman tipis), sehingga nama kecamatan dan desa/kelurahan
(mis. Kalasan, Purwomartani) tidak pernah muncul di halaman yang terindeks. Pencarian lokal seperti
"audit KAP jogja purwomartani" tidak punya halaman FA/CariAkuntan yang cocok.
Solusi: di halaman kota yang terindeks (FA /wilayah/<kota>/, CA /kota/<kota>/ dan /kota/<kota>/kap/)
ditambahkan blok "Area Layanan" berisi semua kecamatan + desa/kelurahan (data Kemendagri, shared/wilayah),
plus nama populer kota (Jogja untuk DIY, Solo untuk Surakarta) di judul, H1, dan intro.
Idempoten (penanda area-layanan)."""
import os, re, sys, html
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, "wilayah")); sys.path.insert(0, os.path.join(H, "..", "cariakuntan"))
import kec as KC
from cities import CITIES
E = html.escape

ALIAS = {"Yogyakarta": "Jogja", "Sleman": "Jogja", "Bantul": "Jogja", "Kulon Progo": "Jogja", "Gunungkidul": "Jogja", "Gunung Kidul": "Jogja",
         "Surakarta": "Solo"}
CSS = ('<style id="area-layanan-css">.arl details{border-top:1px solid rgba(127,127,127,.28);padding:10px 0}.arl summary{cursor:pointer;font-weight:600;list-style:none;'
       'display:flex;justify-content:space-between;gap:12px}.arl summary::-webkit-details-marker{display:none}.arl summary::after{content:"+";opacity:.6}'
       '.arl details[open] summary::after{content:"\\2212"}.arl p{margin:8px 0 0;font-size:14px;line-height:1.65}.arl p b{font-weight:600}</style>')


GENERIC = {"Kota", "Baru", "Lama", "Lor", "Kidul", "Wetan", "Kulon", "Tengah", "Utara", "Selatan", "Timur", "Barat", "Ilir", "Ulu", "Hulu", "Hilir",
           "Darat", "Laut", "Pasar", "Kampung", "Desa", "Dusun", "Jaya", "Indah", "Satu", "Dua", "Tiga", "I", "II", "III", "IV", "Raya", "Atas", "Bawah", "Dalam", "Luar"}


def desa_txt(d):
    """Data Kemendagri sering memisah nama (Purwo Martani); di lapangan ditulis Purwomartani. Tampilkan dua-duanya."""
    w = d.split()
    if len(w) == 2 and not (set(w) & GENERIC) and all(x.isalpha() and len(x) >= 3 for x in w):
        return f"{w[0]}{w[1].lower()} ({d})"
    return d


# nama kecamatan yang di data Kemendagri berbeda dari nama yang dipakai orang saat mencari
KEC_ALIAS = {("Malang", "Sumbermanjing"): "Sumbermanjing Wetan (Sumawe)", ("Malang", "Kalipare"): "Kalipare", ("Malang", "Ngajum"): "Ngajum"}


def kec_txt(city, k):
    a = KEC_ALIAS.get((city, k))
    return f"{a}, nama resmi {k}" if a and a != k else k


def block(city, rows, site):
    alias = ALIAS.get(city)
    nm = f"{city} ({alias})" if alias and alias != city else city
    kabs = []
    for r in rows:
        if r["kab"] not in kabs: kabs.append(r["kab"])
    ndesa = sum(len(r["desa"]) for r in rows)
    what = ("jasa audit laporan keuangan lewat KAP mitra, penyusunan laporan keuangan, pajak, kredit bank, dan valuasi" if site == "fa"
            else "KAP, KJA, konsultan pajak, dan KJPP")
    out = [f'<!--area-layanan--><section class="arl" id="area-layanan"><h2>Area Layanan di {E(nm)}: {len(rows)} Kecamatan, {ndesa} Desa dan Kelurahan</h2>',
           f'<p>Kami melayani {what} untuk perusahaan, yayasan, koperasi, dan rumah sakit di seluruh {E(nm)}, termasuk kecamatan dan desa/kelurahan berikut. '
           'Pertemuan bisa di lokasi Anda atau daring.</p>']
    for kb in kabs:
        sub = [r for r in rows if r["kab"] == kb]
        lines = "".join(f'<p><b>Kecamatan {E(kec_txt(city, r["kec"]))}:</b> {E(", ".join(desa_txt(x) for x in r["desa"]))}.</p>' for r in sub if r["desa"])
        lab = f"{kb} ({len(sub)} kecamatan)" if len(kabs) > 1 else f"Semua kecamatan dan desa di {E(nm)}"
        out.append(f'<details{" open" if len(kabs) == 1 else ""}><summary>{E(lab)}</summary>{lines}</details>')
    out.append("</section><!--/area-layanan-->")
    return "".join(out)


def alias_head(t, city):
    a = ALIAS.get(city)
    head = t[:t.find("</h1>")] if "</h1>" in t else t
    if not a or a == city or f"{city} ({a})" in head: return t
    t = re.sub(r"(<title>[^<]*?\b)" + re.escape(city) + r"\b", lambda m: m.group(1) + f"{city} ({a})", t, count=1)
    t = re.sub(r"(<h1[^>]*>(?:(?!</h1>).)*?\b)" + re.escape(city) + r"\b", lambda m: m.group(1) + f"{city} ({a})", t, count=1, flags=re.S)
    t = re.sub(r'(<meta name="description" content="[^"]*?\b)' + re.escape(city) + r"\b", lambda m: m.group(1) + f"{city} ({a})", t, count=1)
    return t


def inject(p, city, rows, site):
    if not os.path.exists(p): return 0
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"<!--area-layanan-->.*?<!--/area-layanan-->", "", t, flags=re.S)
    b = block(city, rows, site)
    k = -1
    for mark in ("<!--fa-tools-->", "<!--fa-wajah-->", "<h2>Pertanyaan Umum</h2>", "<h2>Tanya Jawab</h2>"):
        k = t.find(mark)
        if k >= 0:
            if mark.startswith("<h2>"):
                j = t.rfind("<section", 0, k); k = j if j > t.rfind("</section>", 0, k) else k
            break
    if k < 0: k = t.rfind("</main>")
    if k < 0: return 0
    t = t[:k] + b + t[k:]
    if "area-layanan-css" not in t: t = t.replace("</head>", CSS + "</head>", 1)
    t = alias_head(t, city)
    open(p, "w", encoding="utf-8").write(t)
    return 1


def run(OUT):
    data = KC.by_city(CITIES)
    n = {"fa": 0, "ca": 0}
    for city, rows in data.items():
        if not rows: continue
        s = KC.slug(city)
        n["fa"] += inject(os.path.join(OUT, "faindonesia", "wilayah", s, "index.html"), city, rows, "fa")
        for sub in ("", "kap"):
            n["ca"] += inject(os.path.join(OUT, "cariakuntan", "kota", s, sub, "index.html"), city, rows, "ca")
    return n


if __name__ == "__main__":
    print(run(os.path.join(H, "..", "out")))
