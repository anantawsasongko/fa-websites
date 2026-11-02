# -*- coding: utf-8 -*-
"""Data kecamatan dan desa/kelurahan untuk halaman SEO tingkat kecamatan (FA dan CariAkuntan), 2 Nov 2026.
Sumber: edwardsamuel/Wilayah-Administratif-Indonesia (ODbL 1.0), kode wilayah Kemendagri.
by_city(CITIES) -> {nama_kota: [dict(kab, kec, slug, desa=[...], kode), ...]}"""
import csv, os, re
H = os.path.dirname(os.path.abspath(__file__))
ROMAN = {"Ii": "II", "Iii": "III", "Iv": "IV", "Vi": "VI", "Vii": "VII", "Viii": "VIII", "Ix": "IX", "Xi": "XI", "Xii": "XII"}
def tc(s):
    s = re.sub(r"\s+", " ", s.strip().lower()).title()
    s = re.sub(r"\b(Ii|Iii|Iv|Vi|Vii|Viii|Ix|Xi|Xii)\b", lambda m: ROMAN[m.group(1)], s)
    return re.sub(r"'S\b", "'s", s)
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def norm(s): return re.sub(r"[^a-z]", "", s.lower())
SPEC = {"Purwokerto": ["KABUPATEN BANYUMAS"], "Labuan Bajo": ["KABUPATEN MANGGARAI BARAT"], "Sumbawa Besar": ["KABUPATEN SUMBAWA"],
        "Singaraja": ["KABUPATEN BULELENG"], "Maumere": ["KABUPATEN SIKKA"], "Weda": ["KABUPATEN HALMAHERA TENGAH"], "Luwuk": ["KABUPATEN BANGGAI"],
        "Timika": ["KABUPATEN MIMIKA"], "Biak": ["KABUPATEN BIAK NUMFOR"], "Bandung": ["KOTA BANDUNG", "KABUPATEN BANDUNG", "KABUPATEN BANDUNG BARAT"],
        "Semarang": ["KOTA SEMARANG", "KABUPATEN SEMARANG"]}
def kab_name(v):
    v = tc(v)
    return v.replace("Kota Administrasi ", "Kota ")
def by_city(cities):
    R = {r[0]: r[2] for r in csv.reader(open(os.path.join(H, "regencies.csv"), encoding="utf-8"))}
    D = {}
    for d in csv.reader(open(os.path.join(H, "districts.csv"), encoding="utf-8")): D.setdefault(d[1], []).append(d)
    V = {}
    for v in csv.reader(open(os.path.join(H, "villages.csv"), encoding="utf-8")): V.setdefault(v[1], []).append(tc(v[2]))
    out = {}
    for c in cities:
        n = c[0]
        if n == "Jakarta": regs = [k for k, v in R.items() if v.startswith("KOTA JAKARTA") or v.startswith("KOTA ADMINISTRASI JAKARTA")]
        elif n in SPEC: regs = [k for k, v in R.items() if v in SPEC[n]]
        else: regs = [k for k, v in R.items() if norm(v) in (norm("KOTA " + n), norm("KABUPATEN " + n))]
        regs.sort(key=lambda k: (not R[k].startswith("KOTA"), R[k]))
        rows, seen = [], set()
        for r in regs:
            for d in sorted(D.get(r, []), key=lambda x: x[2]):
                kec = tc(d[2]); s = slug(kec)
                if s in seen: s = slug(kec + " " + kab_name(R[r]).replace("Kabupaten ", "kab ").replace("Kota ", "kota "))
                seen.add(s)
                rows.append(dict(kab=kab_name(R[r]), kec=kec, slug=s, desa=sorted(V.get(d[0], [])), kode=d[0]))
        out[n] = rows
    return out
