#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ambil registri profesi keuangan dari PPPK Kemenkeu (find-profkeu.kemenkeu.go.id) menjadi shared/pppk/registry.json.
Dijalankan oleh GitHub Actions (.github/workflows/pppk.yml): tiap bulan, saat file ini berubah, atau manual (Run workflow).
Container Claude tidak bisa mengakses kemenkeu.go.id, jadi jangan dijalankan dari sana.

Dataset (semua tabel DataTables server-side, POST .../Data):
  kap     KAP               kota, provinsi, status   detail /Ap/PeriksaKap/<jenisEntitas>/<id>
  ap      Akuntan Publik    status, nama KAP         detail /Ap/PeriksaAp/<id>
  kja     KJA               kota, provinsi, status   detail /Ab/PeriksaKja/<jenisEntitas>/<id>
  ab      Akuntan Berpraktik  status, nama KJA       detail /Ab/PeriksaAb/<id>
  kjpp    KJPP              kota, provinsi, status   detail /Pp/PeriksaKjpp/<jenisEntitas>/<id>
  penilai Penilai Publik    no register, MAPPI       (tanpa halaman detail)
  kp      Konsultan Pajak   status (tanpa kota)      detail /Kp/PeriksaKp/<id>   NPWP TIDAK disimpan
Yang disimpan hanya data daftar (nama, nomor, kota, status). Telepon/email/alamat di halaman detail tidak diambil."""
import json, os, sys, time, datetime, urllib.request, urllib.parse

BASE = "https://find-profkeu.kemenkeu.go.id"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "registry.json")

# key, endpoint Data, kolom DataTables (urut seperti di halaman), peta field -> field kita, pola URL detail
SETS = [
    ("kap", "/Ap/PeriksaKap/Data", ["id", "", "namaKap", "noInduk", "kota", "provinsi", "statusId", ""],
     {"n": "namaKap", "no": "noInduk", "k": "kota", "p": "provinsi", "s": "status", "sid": "statusId", "je": "jenisEntitas"}, "/Ap/PeriksaKap/{je}/{id}"),
    ("ap", "/Ap/PeriksaAp/Data", ["id", "", "namaAp", "noRegistrasi", "namaKap", "statusId", ""],
     {"n": "namaAp", "no": "noRegistrasi", "o": "namaKap", "s": "status", "sid": "statusId"}, "/Ap/PeriksaAp/{id}"),
    ("kja", "/Ab/PeriksaKja/Data", ["id", "", "namaKja", "noInduk", "kota", "provinsi", "statusId", ""],
     {"n": "namaKja", "no": "noInduk", "k": "kota", "p": "provinsi", "s": "status", "sid": "statusId", "je": "jenisEntitas"}, "/Ab/PeriksaKja/{je}/{id}"),
    ("ab", "/Ab/PeriksaAb/Data", ["id", "", "namaAb", "noRegistrasi", "namaKja", "statusId", ""],
     {"n": "namaAb", "no": "noRegistrasi", "o": "namaKja", "s": "status", "sid": "statusId"}, "/Ab/PeriksaAb/{id}"),
    ("kjpp", "/Pp/PeriksaKjpp/Data", ["id", "", "nama", "noIzin", "badanUsaha", "kota", "provinsi", "statusId", ""],
     {"n": "nama", "no": "noIzin", "o": "badanUsaha", "k": "kota", "p": "provinsi", "s": "status", "sid": "statusId", "je": "jenisEntitas"}, "/Pp/PeriksaKjpp/{je}/{id}"),
    ("penilai", "/Pp/PeriksaPenilai/Data", ["id", "", "nama", "noRegister", "tglRegister", "noAnggotaMappi", ""],
     {"n": "nama", "no": "noRegister", "o": "noAnggotaMappi"}, ""),
    ("kp", "/Kp/PeriksaKp/Data", ["id", "", "namaKp", "noKepDirjen", "npwp", "status", ""],
     {"n": "namaKp", "no": "noKepDirjen", "s": "status"}, "/Kp/PeriksaKp/{id}"),
]
KP_STATUS = {"0": "Dicabut", "1": "Aktif", "2": "Ditegur", "3": "Dibekukan"}

def body(cols, start, length):
    p = [("draw", "1"), ("start", str(start)), ("length", str(length)), ("search[value]", ""), ("search[regex]", "false"),
         ("order[0][column]", "0"), ("order[0][dir]", "asc")]
    for i, c in enumerate(cols):
        p += [(f"columns[{i}][data]", c), (f"columns[{i}][name]", ""), (f"columns[{i}][searchable]", "true"),
              (f"columns[{i}][orderable]", "true"), (f"columns[{i}][search][value]", ""), (f"columns[{i}][search][regex]", "false")]
    return urllib.parse.urlencode(p).encode()

def post(path, data, tries=4):
    req = urllib.request.Request(BASE + path, data=data, method="POST", headers={
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8", "x-requested-with": "XMLHttpRequest",
        "accept": "application/json", "user-agent": "Mozilla/5.0 (cariakuntan.com registry mirror; contact ananta@faindonesia.co.id)",
        "referer": BASE + path.replace("/Data", "")})
    last = None
    for t in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last = e; time.sleep(5 * (t + 1))
    raise last

def norm(s):
    return " ".join(str(s or "").split())

def fetch_set(key, ep, cols, fmap, durl):
    first = post(ep, body(cols, 0, 50))
    total = int(first.get("recordsTotal") or 0)
    rows = list(first.get("data") or [])
    step = 2000
    start = len(rows)
    while start < total:
        j = post(ep, body(cols, start, step))
        d = j.get("data") or []
        if not d: break
        rows += d; start += len(d)
    out = []
    for r in rows:
        o = {"id": r.get("id")}
        for a, b in fmap.items():
            v = r.get(b)
            if v is None: continue
            o[a] = norm(v) if isinstance(v, str) else v
        if key == "kp":
            o["s"] = KP_STATUS.get(str(r.get("status")), norm(r.get("status")))
        if "je" in o and durl:
            o["u"] = durl.format(je=o["je"], id=o["id"])
        elif durl:
            o["u"] = durl.format(id=o["id"])
        o.pop("je", None)
        out.append(o)
    print(key, total, len(out), file=sys.stderr)
    return out

def main():
    reg = {"source": BASE, "updated": datetime.date.today().isoformat(), "sets": {}}
    prev = {}
    if os.path.exists(OUT):
        try: prev = json.load(open(OUT, encoding="utf-8")).get("sets", {})
        except Exception: prev = {}
    reg["failed"] = []
    for key, ep, cols, fmap, durl in SETS:
        try:
            reg["sets"][key] = fetch_set(key, ep, cols, fmap, durl)
        except Exception as e:
            # registri kadang error 500 per jenis (mis. Konsultan Pajak); pakai data bulan lalu bila ada
            print("GAGAL", key, e, file=sys.stderr)
            reg["failed"].append(key)
            reg["sets"][key] = prev.get(key, [])
    n = sum(len(v) for v in reg["sets"].values())
    if n < 5000:
        print("terlalu sedikit data (%d), registry.json tidak ditulis" % n, file=sys.stderr); sys.exit(1)
    json.dump(reg, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("ditulis", OUT, n, file=sys.stderr)

if __name__ == "__main__":
    main()
