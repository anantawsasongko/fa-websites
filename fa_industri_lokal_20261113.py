# -*- coding: utf-8 -*-
"""13 Nov 2026 (Bos): halaman daerah FA harus jualan ke segmen yang dicari pemilik usaha setempat (UMKM, cafe, resto,
pabrik, travel umrah, dst.), sesuai ekonomi daerahnya. Syarat Bos: halaman yang sudah rapi TIDAK diubah tata letaknya.

Yang dikerjakan (bekerja di out/faindonesia, idempoten, penanda <!--fa-indlok-->):
- /jasa-audit-laporan-keuangan/<daerah>/ (543): satu baris lipat (details.rg, gaya sama dengan baris
  "Audit per industri" yang sudah ada) "Audit industri utama di <daerah>", dipasang tepat sebelum <!--fa-ind12x-->.
  Link ke halaman audit industri PROVINSI daerah itu (/audit-laporan-keuangan-<ind>/provinsi-<prov>/).
- /jasa-penyusunan-laporan-keuangan/<daerah>/ (543): idem "Laporan keuangan industri utama di <daerah>",
  link ke halaman LK industri provinsi + UMKM provinsi.
- /wilayah/<kota>/ (113): baris "Industri utama di <kota>" setelah <!--/fa-kw3x--> (di dalam lipatan Layanan Lain).
Urutan industri per daerah: sektor kota dari cariakuntan/cities.py (bila ada), lalu profil ekonomi provinsi di bawah.
Baris lama (fa-ind12x, fa-kw3x) tidak disentuh. Kecamatan dan kawasan tidak disentuh.
Urutan build: setelah fa_daerah_lipat_20261113.py (baris ini di luar/di dalam lipatan yang sudah ada, tidak
melintasi batas lipatan). Aman diulang; --buka/lipat ulang fa_daerah_lipat tidak memengaruhi penanda ini.
"""
import os, re, sys, glob, html
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faindonesia")
sys.path.insert(0, os.path.join(HERE, "fa_content")); sys.path.insert(0, os.path.join(HERE, "cariakuntan"))
from industri20261112 import IND
from cities import CITIES
E = html.escape
DRY = "--dry" in sys.argv
I = {i["slug"]: i for i in IND}
A = lambda s: "audit-laporan-keuangan-" + s
K = lambda s: ("laporan-keuangan-" + s) if I[s]["lk"] else I[s]["lk_lama"]
def sl(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def ex(u): return os.path.exists(os.path.join(OUT, u.strip("/"), "index.html"))

SEK = {"dagang": ["distributor"], "kesehatan": ["rumah-sakit", "klinik"], "manufaktur": ["manufaktur"],
       "logistik": ["logistik"], "tambang": ["pertambangan"], "perikanan": ["agribisnis"],
       "properti": ["developer-properti"], "konstruksi": ["kontraktor"], "wisata": ["hotel", "restoran-cafe"],
       "sawit": ["perkebunan-sawit"], "bumd": ["bumd"], "pendidikan": ["yayasan"], "migas": ["spbu", "pertambangan"],
       "smelter": ["manufaktur", "pertambangan"]}
PROV = {
 "aceh": "travel-umrah perkebunan-sawit distributor kontraktor agribisnis bumd yayasan",
 "sumatera-utara": "perkebunan-sawit manufaktur distributor logistik travel-umrah rumah-sakit developer-properti",
 "sumatera-barat": "travel-umrah restoran-cafe distributor hotel agribisnis yayasan koperasi",
 "riau": "perkebunan-sawit pertambangan spbu kontraktor logistik travel-umrah distributor",
 "kepulauan-riau": "manufaktur pma logistik kontraktor hotel developer-properti distributor",
 "jambi": "perkebunan-sawit pertambangan distributor spbu travel-umrah kontraktor",
 "sumatera-selatan": "pertambangan perkebunan-sawit kontraktor distributor travel-umrah spbu logistik",
 "bengkulu": "perkebunan-sawit pertambangan distributor travel-umrah koperasi kontraktor",
 "lampung": "agribisnis perkebunan-sawit manufaktur distributor logistik travel-umrah",
 "kepulauan-bangka-belitung": "pertambangan perkebunan-sawit hotel restoran-cafe distributor",
 "banten": "manufaktur pma logistik developer-properti kontraktor travel-umrah distributor",
 "dki-jakarta": "pma startup-teknologi distributor developer-properti data-center travel-umrah rumah-sakit restoran-cafe",
 "jawa-barat": "manufaktur pma data-center developer-properti travel-umrah distributor restoran-cafe yayasan",
 "jawa-tengah": "manufaktur distributor travel-umrah restoran-cafe koperasi yayasan rumah-sakit",
 "di-yogyakarta": "restoran-cafe hotel yayasan travel-umrah retail startup-teknologi",
 "jawa-timur": "manufaktur distributor travel-umrah restoran-cafe rumah-sakit koperasi logistik yayasan",
 "bali": "hotel pma restoran-cafe developer-properti retail logistik",
 "nusa-tenggara-barat": "pertambangan hotel pma travel-umrah restoran-cafe agribisnis distributor",
 "nusa-tenggara-timur": "hotel pma koperasi agribisnis distributor kontraktor yayasan",
 "kalimantan-barat": "perkebunan-sawit pertambangan distributor travel-umrah logistik kontraktor",
 "kalimantan-tengah": "perkebunan-sawit pertambangan kontraktor distributor spbu logistik",
 "kalimantan-selatan": "pertambangan perkebunan-sawit travel-umrah distributor logistik kontraktor",
 "kalimantan-timur": "pertambangan kontraktor developer-properti logistik spbu perkebunan-sawit hotel",
 "kalimantan-utara": "pertambangan perkebunan-sawit kontraktor logistik distributor",
 "sulawesi-utara": "hotel restoran-cafe agribisnis distributor logistik kontraktor",
 "gorontalo": "agribisnis distributor travel-umrah koperasi kontraktor",
 "sulawesi-tengah": "pertambangan manufaktur pma kontraktor logistik travel-umrah",
 "sulawesi-selatan": "travel-umrah distributor agribisnis rumah-sakit kontraktor restoran-cafe logistik",
 "sulawesi-barat": "perkebunan-sawit agribisnis distributor travel-umrah kontraktor",
 "sulawesi-tenggara": "pertambangan manufaktur pma kontraktor agribisnis travel-umrah",
 "maluku": "agribisnis distributor kontraktor logistik hotel",
 "maluku-utara": "pertambangan manufaktur pma kontraktor logistik",
 "papua": "pertambangan kontraktor distributor logistik bumd spbu",
 "papua-barat": "pertambangan kontraktor distributor logistik agribisnis",
 "papua-barat-daya": "pertambangan kontraktor distributor logistik hotel",
 "papua-selatan": "agribisnis kontraktor distributor logistik",
 "papua-tengah": "pertambangan kontraktor distributor logistik",
 "papua-pegunungan": "kontraktor distributor logistik",
}
CITY = {}
for nm, pv, rg, sek, cat in CITIES:
    CITY[sl(nm)] = sum((SEK.get(s, []) for s in sek), [])
PMA_WAJIB = {"bali", "nusa-tenggara-barat", "nusa-tenggara-timur"}   # Bos 13 Nov: Bali, NTB, NTT juga PT PMA
NONUMRAH = {"bali", "nusa-tenggara-timur", "sulawesi-utara", "maluku", "papua", "papua-barat", "papua-barat-daya",
            "papua-selatan", "papua-tengah", "papua-pegunungan"}

def urutan(slug, prov):
    base = slug
    for pre in ("kabupaten-", "kota-", "provinsi-"): base = base[len(pre):] if base.startswith(pre) else base
    out = []
    for s in CITY.get(slug, CITY.get(base, [])) + PROV.get(prov, "").split():
        if s in I and s not in out: out.append(s)
    wajib = (["pma"] if prov in PMA_WAJIB else []) + ["restoran-cafe"] + ([] if prov in NONUMRAH else ["travel-umrah"])   # segmen yang diminta Bos, selalu ada
    out = [s for s in out if s not in wajib][:7]
    if prov in PMA_WAJIB: return out[:1] + ["pma"] + out[1:] + wajib[1:]   # PT PMA tampil di urutan kedua
    return out + wajib

def lokasi(t, slug):
    if slug.startswith("provinsi-"):
        m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S); nm = re.sub(r"<[^>]+>", "", m.group(1)) if m else ""
        m = re.search(r" di ([^:]+)", nm); return "Provinsi " + html.unescape(m.group(1)).strip() if m else None
    m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    if not m: return None
    nm = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    m = re.search(r" di ([^:]+)", nm); return m.group(1).strip() if m else None

def blok(kind, loc, prov, inds):
    items = []
    for s in inds:
        if kind == "lk":
            u = f"/{K(s)}/provinsi-{prov}/"; u = u if ex(u) else f"/{K(s)}/"
        else:
            u = f"/{A(s)}/provinsi-{prov}/"; u = u if ex(u) else f"/{A(s)}/"
        if ex(u) and all(u != x for x, _ in items): items.append((u, I[s]["pendek"]))
    if kind in ("lk", "wil"):
        u = f"/laporan-keuangan-umkm/provinsi-{prov}/"
        if ex(u): items.append((u, "UMKM"))
    lab = {"audit": "Audit industri utama di", "lk": "Laporan keuangan industri utama di", "wil": "Industri utama di"}[kind]
    return ('<!--fa-indlok--><details class="rg"><summary>' + E(f"{lab} {loc}") + f' <i>{len(items)}</i></summary><div class="rg-l">'
            + "".join(f'<a href="{u}">{E(n)}</a>' for u, n in items) + "</div></details><!--/fa-indlok-->")

RX = re.compile(r"<!--fa-indlok-->.*?<!--/fa-indlok-->", re.S)
n = 0; skip = []
for fam, kind, anchor, after in (("jasa-audit-laporan-keuangan", "audit", "<!--fa-ind12x-->", False),
                                 ("jasa-penyusunan-laporan-keuangan", "lk", "<!--fa-ind12x-->", False),
                                 ("wilayah", "wil", "<!--/fa-kw3x-->", True)):
    for p in sorted(glob.glob(os.path.join(OUT, fam, "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(p)); t = open(p, encoding="utf-8").read()
        base = RX.sub("", t)
        if slug.startswith("provinsi-"): prov = slug[9:]
        else:
            m = re.search(r'/laporan-keuangan-umkm/provinsi-([a-z0-9-]+)/', base); prov = m.group(1) if m else None
        loc = lokasi(base, slug)
        if not prov or not loc or base.count(anchor) != 1: skip.append((p, prov, loc)); continue
        b = blok(kind, loc, prov, urutan(slug, prov))
        new = base.replace(anchor, anchor + b) if after else base.replace(anchor, b + anchor)
        if new != t:
            n += 1
            if not DRY: open(p, "w", encoding="utf-8").write(new)
print("diubah", n, "lewat", len(skip))
for s in skip[:20]: print("  lewat", s)
