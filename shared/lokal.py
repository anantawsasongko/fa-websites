"""Fakta lokal per kota/kabupaten/provinsi untuk blok unik halaman template (9 Nov 2026).
Sumber: shared/pppk/registry.json (Registri PPPK Kemenkeu, find-profkeu), shared/wilayah/*.csv (kode wilayah),
cariakuntan/cities.py (113 kota prioritas, sektor), cariakuntan/coords.py (koordinat 113 kota).
Tidak memuat telepon/alamat kantor.
"""
import csv, json, math, os, re, sys, unicodedata, hashlib
from collections import defaultdict, Counter

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, "cariakuntan"))
from cities import CITIES, SECTOR_LINES  # noqa: E402
from coords import COORDS  # noqa: E402

W = os.path.join(R, "shared", "wilayah")
REG = json.load(open(os.path.join(R, "shared", "pppk", "registry.json")))
UPDATED = REG.get("updated", "")
SRC = "https://find-profkeu.kemenkeu.go.id"


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def key(t):
    return re.sub(r"[^A-Z]", "", t.upper())


def nice(t):
    """'KABUPATEN S I A K' -> 'Siak', 'KOTA ADM. JAKARTA SELATAN' -> 'Jakarta Selatan'."""
    t = re.sub(r"^(KABUPATEN|KOTA ADM\.?|KOTA ADMINISTRASI|KOTA)\s+", "", t.strip(), flags=re.I)
    if re.fullmatch(r"(?:[A-Z] )+[A-Z]", t):
        t = t.replace(" ", "")
    out = []
    for w in t.lower().split():
        if re.fullmatch(r"[ivxl]+", w) and w not in ("ill",):
            out.append(w.upper())
        else:
            out.append(w.lower() if w == "dan" else w.capitalize())
    return " ".join(out)


# ---------- wilayah ----------
PROV = {r[0]: r[1] for r in csv.reader(open(os.path.join(W, "provinces.csv")))}
PROV_NICE = {c: nice(n).replace("Dki ", "DKI ").replace("Di ", "DI ") for c, n in PROV.items()}
REGS = {}  # kode -> (prov, nama asli, nama rapi, jenis)
for c, p, n in csv.reader(open(os.path.join(W, "regencies.csv"))):
    REGS[c] = (p, n, nice(n), "Kota" if n.upper().startswith("KOTA") else "Kabupaten")
KEC = defaultdict(list)  # reg -> [(kode, nama)]
for c, r, n in csv.reader(open(os.path.join(W, "districts.csv"))):
    KEC[r].append((c, nice(n)))
DESA = Counter()
for c, d, n in csv.reader(open(os.path.join(W, "villages.csv"))):
    DESA[d[:4]] += 1

# kunci nama -> kode (kota diutamakan)
BYKEY = defaultdict(list)
for c, (p, n, nn, j) in REGS.items():
    BYKEY[key(nn)].append(c)
for k in BYKEY:
    BYKEY[k].sort(key=lambda c: (REGS[c][3] != "Kota", c))

ALIAS = {  # nama kota prioritas -> nama kabupaten induk
    "Purwokerto": "Banyumas", "Singaraja": "Buleleng", "Sumbawa Besar": "Sumbawa", "Labuan Bajo": "Manggarai Barat",
    "Maumere": "Sikka", "Luwuk": "Banggai", "Weda": "Halmahera Tengah", "Biak": "Biak Numfor", "Timika": "Mimika",
}
PAPUA_BARU = {  # provinsi pemekaran 2022 (data wilayah masih 34 provinsi)
    "Papua Tengah": ["Mimika", "Nabire", "Paniai", "Puncak Jaya", "Puncak", "Dogiyai", "Intan Jaya", "Deiyai"],
    "Papua Pegunungan": ["Jayawijaya", "Lanny Jaya", "Mamberamo Tengah", "Nduga", "Pegunungan Bintang", "Tolikara", "Yahukimo", "Yalimo"],
    "Papua Selatan": ["Merauke", "Boven Digoel", "Mappi", "Asmat"],
    "Papua Barat Daya": ["Sorong", "Raja Ampat", "Sorong Selatan", "Maybrat", "Tambrauw"],
}
REG_PROV_OVERRIDE = {}
for pn, lst in PAPUA_BARU.items():
    for nm in lst:
        for c in BYKEY.get(key(nm), []):
            REG_PROV_OVERRIDE[c] = pn


def hub_label(c):
    p, n, nn, j = REGS[c]
    same = [x for x in BYKEY.get(key(nn), []) if prov_name(x) == prov_name(c)] if c in REGS else []
    return nn if len(same) > 1 else f"{j} {nn}"


def prov_name(regcode):
    return REG_PROV_OVERRIDE.get(regcode) or PROV_NICE[REGS[regcode][0]]


def regs_for_city(name):
    """Kode wilayah untuk kota prioritas (Jakarta = 6 wilayah DKI)."""
    if name == "Jakarta":
        return [c for c in REGS if c.startswith("31")]
    nm = ALIAS.get(name, name)
    cs = BYKEY.get(key(nm), [])
    return cs


# ---------- registri ----------
FIX = {"SELARAN": "SELATAN", "SELATA": "SELATAN"}


def reg_key(k):
    k = re.sub(r"\d+", "", k or "")
    k = re.sub(r"^(Kota\s+Adm\.?|Kota\s+Administrasi|Kota|Kab\.?|Kabupaten)\s+", "", k.strip(), flags=re.I)
    w = [FIX.get(x.upper(), x.upper()) for x in k.split()]
    k = "".join(w)
    k = {"PALANGKARAYA": "PALANGKARAYA", "PONTIANAKSELATAN": "PONTIANAK", "BANJARBARU": "BANJARBARU"}.get(k, k)
    return re.sub(r"[^A-Z]", "", k)


OFFICES = defaultdict(lambda: defaultdict(list))  # jenis -> regkey -> [entri]
OFF_PROV = defaultdict(Counter)  # jenis -> provinsi rapi -> jumlah
P_NORM = {"Nanggroe Aceh Darussalam": "Aceh", "Nangroe Aceh Darussalam": "Aceh", "Papua Irian Jaya": "Papua",
          "Bangka Belitung": "Kepulauan Bangka Belitung", "DI Yogyakarta": "DI Yogyakarta"}
for t in ("kap", "kja", "kjpp"):
    for x in REG["sets"].get(t, []):
        if not str(x.get("s", "")).startswith("Aktif") or not x.get("k"):
            continue
        rk = reg_key(x["k"])
        if rk.startswith("JAKARTA"):
            rk2 = "JAKARTA"
        else:
            rk2 = rk
        OFFICES[t][rk2].append(x)
        if rk2 == "JAKARTA" and rk != "JAKARTA":
            OFFICES[t][rk].append(x)
        cs = BYKEY.get(rk) or (BYKEY.get("JAKARTASELATAN") if rk2 == "JAKARTA" else None)
        p = prov_name(cs[0]) if cs else P_NORM.get(x.get("p"), x.get("p") or "")
        OFF_PROV[t][p] += 1

LABEL = {"kap": "Kantor Akuntan Publik (KAP)", "kja": "Kantor Jasa Akuntansi (KJA)", "kjpp": "Kantor Jasa Penilai Publik (KJPP)"}
SHORT = {"kap": "KAP", "kja": "KJA", "kjpp": "KJPP"}


def offices(t, name_keys):
    seen, out = set(), []
    for k in name_keys:
        for x in OFFICES[t].get(k, []):
            if x["no"] not in seen:
                seen.add(x["no"]); out.append(x)
    return sorted(out, key=lambda x: x["n"])


# ---------- lokasi ----------
CITY = {c[0]: c for c in CITIES}
CITY_BY_SLUG = {slug(c[0]): c[0] for c in CITIES}
PROV_BY_SLUG = {}
for c, n in PROV_NICE.items():
    PROV_BY_SLUG[slug(n)] = n
for pn in PAPUA_BARU:
    PROV_BY_SLUG[slug(pn)] = pn
PROV_BY_SLUG["di-yogyakarta"] = "DI Yogyakarta"
PROV_BY_SLUG["kepulauan-bangka-belitung"] = PROV_BY_SLUG.get("kepulauan-bangka-belitung", "Kepulauan Bangka Belitung")
REG_BY_SLUG = {}
for c, (p, n, nn, j) in REGS.items():
    REG_BY_SLUG.setdefault(slug(f"{j} {nn}"), c)
    REG_BY_SLUG.setdefault(slug(n.replace("KOTA ADM.", "KOTA")), c)


def dist(a, b):
    (la1, lo1), (la2, lo2) = COORDS[a], COORDS[b]
    r = math.pi / 180
    x = math.sin((la2 - la1) * r / 2) ** 2 + math.cos(la1 * r) * math.cos(la2 * r) * math.sin((lo2 - lo1) * r / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(x))


def city_counts(name):
    keys = [key(name)] if name != "Jakarta" else ["JAKARTA"]
    if name in ALIAS:
        keys.append(key(ALIAS[name]))
    return {t: offices(t, keys) for t in ("kap", "kja", "kjpp")}


def nearest_with(t, name, n=3):
    if name not in COORDS:
        return []
    res = []
    for o in COORDS:
        if o == name or o not in CITY:
            continue
        c = len(city_counts(o)[t])
        if c:
            res.append((round(dist(name, o)), o, c))
    return sorted(res)[:n]


def resolve(s):
    """slug halaman -> dict lokasi atau None."""
    s = s.strip("/").split("/")[-1]
    if s in CITY_BY_SLUG:
        name = CITY_BY_SLUG[s]
        cs = regs_for_city(name)
        prov = CITY[name][1]
        return dict(kind="kota", name=name, label=name, regs=cs, prov=prov, keys=[key(name)] if name != "Jakarta" else ["JAKARTA"],
                    sectors=CITY[name][3], note=CITY[name][4])
    if s.startswith("provinsi-") or s in PROV_BY_SLUG:
        pn = PROV_BY_SLUG.get(s[9:] if s.startswith("provinsi-") else s)
        if not pn:
            return None
        if pn in PAPUA_BARU:
            regs = [c for c in REGS if REG_PROV_OVERRIDE.get(c) == pn]
        else:
            pc = [c for c, n in PROV_NICE.items() if n == pn]
            regs = [c for c in REGS if pc and REGS[c][0] == pc[0] and c not in REG_PROV_OVERRIDE]
        return dict(kind="provinsi", name=pn, label=f"Provinsi {pn}", regs=regs, prov=pn, keys=None, sectors=[], note="")
    c = REG_BY_SLUG.get(s)
    if c:
        p, n, nn, j = REGS[c]
        return dict(kind=j.lower(), name=nn, label=f"{j} {nn}", regs=[c], prov=prov_name(c), keys=[key(nn)], sectors=[], note="")
    return None


def facts(loc):
    """Angka dan daftar untuk blok."""
    f = dict(loc)
    kec = [k for r in loc["regs"] for k in KEC.get(r, [])]
    f["n_kec"] = len(kec)
    f["kec"] = sorted({k[1] for k in kec})
    f["n_desa"] = sum(DESA[r] for r in loc["regs"])
    if loc["kind"] == "provinsi":
        f["n_kab"] = sum(1 for r in loc["regs"] if REGS[r][3] == "Kabupaten")
        f["n_kot"] = sum(1 for r in loc["regs"] if REGS[r][3] == "Kota")
        f["off"] = {t: OFF_PROV[t].get(loc["name"], 0) for t in ("kap", "kja", "kjpp")}
        f["offlist"] = {t: [] for t in ("kap", "kja", "kjpp")}
        # kota/kab dengan KAP terbanyak di provinsi ini
        cnt, seenk = Counter(), set()
        for r in loc["regs"]:
            k = key(REGS[r][2])
            if k in seenk:
                continue
            seenk.add(k)
            for t in ("kap", "kja", "kjpp"):
                cnt[hub_label(r)] += len(OFFICES[t].get(k, []))
        if loc["name"] == "DKI Jakarta":
            cnt = Counter({"Jakarta": sum(len(OFFICES[t]["JAKARTA"]) for t in ("kap", "kja", "kjpp"))})
        f["hub"] = [(n, c) for n, c in cnt.most_common(4) if c]
    else:
        if loc["kind"] == "kota" and loc["name"] in CITY:
            cc = city_counts(loc["name"])
        else:
            cc = {t: offices(t, loc["keys"]) for t in ("kap", "kja", "kjpp")}
        f["offlist"] = cc
        f["off"] = {t: len(v) for t, v in cc.items()}
        f["prov_off"] = {t: OFF_PROV[t].get(loc["prov"], 0) for t in ("kap", "kja", "kjpp")}
        f["near"] = {t: nearest_with(t, loc["name"]) for t in ("kap", "kja", "kjpp")} if loc["name"] in COORDS else {}
        # kab/kota lain di provinsi yang punya kantor (untuk kabupaten tanpa koordinat)
        hub, seenk = Counter(), set()
        for c, (p, n, nn, j) in REGS.items():
            k = key(nn)
            if prov_name(c) != loc["prov"] or c in loc["regs"] or k in (loc["keys"] or []) or k in seenk:
                continue
            seenk.add(k)
            hub[hub_label(c)] = sum(len(OFFICES[t].get(k, [])) for t in ("kap", "kja", "kjpp"))
        if loc["prov"] == "DKI Jakarta":
            hub = Counter()
        f["hub"] = [(n, c) for n, c in hub.most_common(3) if c]
    return f


def pick(seed, options):
    h = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    return options[h % len(options)]


def sample(seed, items, n):
    """Ambil n item deterministik tapi berbeda per halaman."""
    if len(items) <= n:
        return list(items)
    h = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    st = h % len(items)
    return [items[(st + i * (len(items) // n)) % len(items)] for i in range(n)]


def rp(n):
    return f"{n:,}".replace(",", ".")
