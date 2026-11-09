"""Blok data lokal unik per halaman template kota/kabupaten/provinsi (9 Nov 2026).
Bos: "halaman identik ubah jadi beda, semua situs". Data: shared/lokal.py (registri PPPK Kemenkeu, data wilayah,
sektor 113 kota, jarak antarkota). Idempoten (penanda <!--uq-lokal--> ... <!--/uq-lokal-->).
FA: angka saja (tanpa nama kantor lain). CA: angka + nama kantor (situs direktori) bila halaman belum punya daftar registri.
Disisipkan sebelum H2 FAQ ("Pertanyaan Umum"/"Tanya Jawab"); kalau tidak ada, sebelum </main> dalam <div class="wrap">.
Halaman noindex dilewati. Jalankan setelah semua script FA/CA lain (paling akhir).
"""
import os, re, sys, glob, html
R = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(R, "shared"))
import lokal as L  # noqa: E402

OUT = os.path.join(R, "out")
M0, M1 = "<!--uq-lokal-->", "<!--/uq-lokal-->"
TGL = "5 November 2026"

# keluarga -> (fokus, grup)
FA_FAM = {
    "jasa-audit-laporan-keuangan": ("kap", "audit"), "jasa-audit-laporan-keuangan-bpr": ("kap", "bpr"),
    "jasa-pendampingan-audit": ("kap", "dampingi"), "akuntan-forensik": ("kap", "forensik"),
    "jasa-penyusunan-laporan-keuangan": ("kja", "lk"), "jasa-penyusunan-laporan-keuangan-bpr": ("kja", "bpr"),
    "laporan-tahunan-pt": ("kja", "sabh"), "jasa-buku-besar": ("kja", "bukubesar"), "konsultan-penerapan-psak": ("kja", "psak"),
    "menjual-rumah-sakit": ("kjpp", "jualrs"), "direktur-rumah-sakit": ("kap", "dirrs"),
    "wilayah": ("all", "hub"),
}
for f in ("konsultan-rumah-sakit", "konsultan-klinik", "konsultan-klinik-bpjs", "konsultan-simrs", "konsultan-unit-cost-rumah-sakit",
          "konsultan-farmasi-rumah-sakit", "konsultan-bpjs-rumah-sakit", "konsultan-akreditasi-rumah-sakit"):
    FA_FAM[f] = ("kap", "rs")
for f in ("umkm", "klinik", "perusahaan", "kontraktor", "koperasi", "yayasan-sekolah", "toko-distributor", "cafe-restoran"):
    FA_FAM["laporan-keuangan-" + f] = ("kja", "lkjenis")
CA_SVC = {"kap": ("kap", "audit"), "kap-murah": ("kap", "murah"), "pendampingan-audit": ("kap", "dampingi"),
          "akuntan-forensik": ("kap", "forensik"), "kja": ("kja", "lk"), "jasa-laporan-keuangan": ("kja", "lk"),
          "jasa-buku-besar": ("kja", "bukubesar"), "laporan-tahunan-pt": ("kja", "sabh"), "konsultan-psak": ("kja", "psak"),
          "kjpp": ("kjpp", "kjpp"), "konsultan-pajak": ("all", "pajak"), "konsultan-rumah-sakit": ("kap", "rs")}

JUDUL = {
    "audit": ["Data Kantor Akuntan Publik di {L}", "{L} dalam Angka: KAP Berizin", "Peta Auditor Berizin untuk {L}"],
    "bpr": ["BPR dan Kantor Berizin di {L}", "{L}: Data Auditor dan Penyusun Laporan", "Angka Kantor Berizin di {L}"],
    "dampingi": ["Auditor yang Aktif di {L}", "{L} dalam Angka: KAP dan Auditee", "Data KAP Aktif di {L}"],
    "forensik": ["Data KAP dan Auditor di {L}", "{L} dalam Angka untuk Pemeriksaan Khusus", "Kantor Berizin di {L}"],
    "lk": ["Data Kantor Jasa Akuntansi di {L}", "{L} dalam Angka: Penyusun Laporan Keuangan", "Penyusun Laporan Berizin di {L}"],
    "lkjenis": ["{L} dalam Angka", "Data Wilayah dan Kantor Berizin di {L}", "Sekilas {L} untuk Laporan Keuangan"],
    "sabh": ["Data KJA dan KAP di {L}", "{L} dalam Angka untuk Laporan Tahunan PT", "Kantor Berizin di {L}"],
    "bukubesar": ["Data Kantor Jasa Akuntansi di {L}", "{L} dalam Angka: Pembukuan dan KJA", "Sekilas KJA di {L}"],
    "psak": ["Data Kantor Akuntansi di {L}", "{L} dalam Angka untuk Penerapan PSAK", "Kantor Berizin dan Sektor di {L}"],
    "jualrs": ["Data Penilai Publik (KJPP) di {L}", "{L} dalam Angka untuk Transaksi RS", "KJPP dan Wilayah {L}"],
    "dirrs": ["Sekilas {L} untuk Manajemen RS", "{L} dalam Angka", "Data Wilayah dan Auditor di {L}"],
    "rs": ["Sekilas {L} untuk Rumah Sakit dan Klinik", "{L} dalam Angka: Wilayah dan Auditor", "Data Wilayah {L}"],
    "hub": ["{L} dalam Angka", "Data Kantor Berizin di {L}", "Sekilas {L}: Wilayah dan Kantor Berizin"],
    "murah": ["Berapa Banyak KAP di {L}?", "{L} dalam Angka: Pilihan KAP", "Data KAP Aktif di {L}"],
    "kjpp": ["Data KJPP Aktif di {L}", "{L} dalam Angka: Penilai Publik", "Sebaran KJPP untuk {L}"],
    "pajak": ["{L} dalam Angka", "Data Kantor Berizin di {L}", "Sekilas {L} untuk Urusan Pajak"],
    "kdmp": ["Data Wilayah dan KJA di {L}", "{L} dalam Angka untuk Koperasi", "Sekilas {L}: Desa dan Kantor Berizin"],
}

e = html.escape


def wilayah_kalimat(f, seed):
    lab, pv = f["label"], f["prov"]
    if f["kind"] == "provinsi":
        return (f"{lab} terdiri dari {f['n_kab']} kabupaten dan {f['n_kot']} kota, dengan {L.rp(f['n_kec'])} kecamatan "
                f"dan {L.rp(f['n_desa'])} desa atau kelurahan.")
    if f["name"] == "Jakarta":
        return f"DKI Jakarta terbagi menjadi 5 kota administrasi dan 1 kabupaten administrasi, dengan {f['n_kec']} kecamatan dan {f['n_desa']} kelurahan."
    al = L.ALIAS.get(f["name"])
    pre = f"{f['name']} masuk wilayah Kabupaten {al}, Provinsi {pv}. " if al else ""
    if al:
        return pre + f"Kabupaten {al} mencakup {f['n_kec']} kecamatan dan {L.rp(f['n_desa'])} desa atau kelurahan."
    if not f["n_kec"]:
        return f"{lab} berada di Provinsi {pv}."
    return L.pick(seed + "w", [
        f"{lab} berada di Provinsi {pv}, mencakup {f['n_kec']} kecamatan dan {L.rp(f['n_desa'])} desa atau kelurahan.",
        f"Secara administratif, {lab} ({pv}) terbagi menjadi {f['n_kec']} kecamatan dengan {L.rp(f['n_desa'])} desa dan kelurahan.",
        f"Wilayah {lab} meliputi {f['n_kec']} kecamatan dan {L.rp(f['n_desa'])} desa atau kelurahan di Provinsi {pv}.",
    ])


def tafsir(f, t, seed, site):
    """Kalimat yang memakai angka kota ini."""
    lab = f["label"]
    if t == "all":
        tot = sum(f["off"].values())
        if tot == 0:
            return f"Belum ada KAP, KJA, atau KJPP aktif yang tercatat berkantor di {lab}. " + jauh(f, "kap", seed)
        return L.pick(seed + "a", [
            f"Total ada {tot} kantor berizin (KAP, KJA, dan KJPP) yang aktif di {lab}. Yang menentukan biasanya bukan jumlah, tapi kantor mana yang diterima bank, regulator, atau investor Anda.",
            f"Dengan {tot} kantor berizin yang aktif, pilihan di {lab} relatif {'luas' if tot >= 25 else 'terbatas'}. Cocokkan dulu syarat pemakai laporan sebelum memilih.",
            f"Registri mencatat {tot} kantor aktif di {lab}. Jadwal mereka padat di Januari sampai April, jadi pekerjaan yang direncanakan sejak kuartal IV biasanya lebih lancar.",
        ])
    c, S = f["off"][t], L.SHORT[t]
    if f["kind"] == "provinsi":
        if c == 0:
            return f"Belum ada {S} aktif yang tercatat di {lab}. Pekerjaan untuk perusahaan di provinsi ini dijalankan dari luar provinsi: dokumen dikirim digital, kunjungan lapangan dijadwalkan."
        return L.pick(seed + "t", [f"Ada {c} {S} aktif di {lab}.", f"Registri mencatat {c} {S} aktif di {lab}.",
                                   f"Jumlah {S} aktif di {lab} saat ini {c} kantor."]) + " Pekerjaan untuk kabupaten yang jauh dari kantor-kantor ini berjalan dari dokumen digital, dengan kunjungan lapangan terjadwal."
    if c >= 10:
        return L.pick(seed + "t", [
            f"Pilihan {S} di {lab} cukup banyak ({c} kantor aktif). Yang perlu dicek bukan jaraknya, tapi apakah kantor itu diterima bank atau regulator Anda dan apakah jadwalnya cocok.",
            f"Dengan {c} {S} aktif, {lab} termasuk wilayah yang pilihannya luas. Bandingkan ruang lingkup dan jadwal, bukan hanya harga.",
            f"{c} {S} aktif berkantor di {lab}. Banyaknya pilihan membuat syarat pemakai laporan (bank, OJK, investor) jadi penyaring utama.",
        ])
    if c >= 1:
        return L.pick(seed + "t", [
            f"Hanya ada {c} {S} aktif yang berkantor di {lab}. Saat musim laporan tahunan jadwalnya cepat penuh, jadi rencanakan dari awal.",
            f"{lab} punya {c} {S} aktif. Pilihan lokal terbatas, sehingga banyak perusahaan di sini juga memakai kantor dari kota lain di Provinsi {f['prov']}.",
            f"Registri mencatat {c} {S} aktif di {lab}. Untuk pekerjaan dengan tenggat bank atau RUPS, pastikan jadwalnya dikunci lebih awal.",
        ])
    return f"Belum ada {S} aktif yang tercatat berkantor di {lab}. " + jauh(f, t, seed)


def jauh(f, t, seed):
    near = f.get("near", {}).get(t) if f.get("near") else None
    S = L.SHORT[t]
    if near:
        s = ", ".join(f"{o} (sekitar {L.rp(d)} km, {c} {S})" for d, o, c in near)
        return f"{S} terdekat yang tercatat ada di {s}. Pekerjaan tetap bisa jalan: dokumen dikirim digital, kunjungan lapangan dijadwalkan bila perlu."
    pc = f.get("prov_off", {}).get(t, 0)
    if f.get("hub") and pc:
        s = ", ".join(n for n, c in f["hub"][:3])
        return f"Di Provinsi {f['prov']} ada {pc} {S} aktif, terbanyak di {s}. Sebagian besar pekerjaan berjalan dari dokumen digital, dengan kunjungan lapangan bila perlu."
    return f"Di Provinsi {f['prov']} pun belum ada {S} aktif yang tercatat. Pekerjaan dijalankan dari luar provinsi lewat dokumen digital dan kunjungan terjadwal."


SEKTOR_LBL = {"dagang": "perdagangan", "manufaktur": "manufaktur", "tambang": "pertambangan", "smelter": "smelter",
              "sawit": "perkebunan", "perikanan": "perikanan", "wisata": "pariwisata", "migas": "migas", "konstruksi": "konstruksi",
              "properti": "properti", "kesehatan": "kesehatan", "bpr": "BPR dan koperasi", "pendidikan": "pendidikan",
              "logistik": "logistik", "bumd": "BUMD"}


def sektor(f, seed, grup):
    if not f.get("sectors"):
        return ""
    ss = f["sectors"]
    lbl = ", ".join(SEKTOR_LBL.get(s, s) for s in ss)
    pref = {"rs": "kesehatan", "dirrs": "kesehatan", "jualrs": "kesehatan", "bpr": "bpr"}.get(grup)
    order = ([pref] if pref in ss else []) + [s for s in L.sample(seed + "s", ss, len(ss)) if s != pref]
    line = L.SECTOR_LINES.get(order[0], "")
    return (f"<p>{e(f['name'])} dikenal sebagai {e(f['note'])}. Sektor yang menonjol: {e(lbl)}. "
            f"{e(line)}</p>")


def tabel(f, focus):
    rows = []
    for t in ("kap", "kja", "kjpp"):
        b = ' style="font-weight:600"' if t == focus else ""
        if f["kind"] == "provinsi":
            rows.append(f"<tr{b}><td>{L.LABEL[t]}</td><td>{f['off'][t]}</td></tr>")
        else:
            rows.append(f"<tr{b}><td>{L.LABEL[t]}</td><td>{f['off'][t]}</td><td>{f['prov_off'][t]}</td></tr>")
    if f["kind"] == "provinsi":
        head = f"<tr><th>Jenis kantor (status aktif)</th><th>{e(f['label'])}</th></tr>"
    else:
        head = f"<tr><th>Jenis kantor (status aktif)</th><th>{e(f['label'])}</th><th>Se-Provinsi {e(f['prov'])}</th></tr>"
    return ('<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;margin:10px 0 6px;font-size:15px">'
            f"<thead>{head}</thead><tbody>{''.join(rows)}</tbody></table></div>")


def daftar_kec(f, seed, txt):
    if "Area Layanan" in txt or not f["kec"]:
        return ""
    if f["kind"] == "provinsi":
        nm = sorted({(L.REGS[r][3] + " " + L.REGS[r][2]) for r in f["regs"]})
        return f"<p><b>Kabupaten dan kota di {e(f['label'])}:</b> {e(', '.join(nm))}.</p>"
    ks = L.sample(seed + "k", f["kec"], 14)
    sisa = f["n_kec"] - len(ks)
    return (f"<p><b>Kecamatan di {e(f['label'])}:</b> {e(', '.join(sorted(ks)))}"
            + (f", dan {sisa} kecamatan lain." if sisa > 0 else ".") + "</p>")


def nama_kantor(f, t, txt):
    """Khusus CA: daftar nama kantor aktif bila halaman belum punya daftar registri."""
    if 'class="pk-l"' in txt or f["kind"] == "provinsi" or t == "all":
        return ""
    lst = f["offlist"][t]
    if not lst:
        return ""
    li = "".join(f"<li>{e(x['n'])} <span style=\"color:var(--muted,#666)\">({e(x['no'])})</span></li>" for x in lst[:12])
    more = f"<p>Dan {len(lst) - 12} {L.SHORT[t]} aktif lainnya.</p>" if len(lst) > 12 else ""
    return (f"<p><b>{L.SHORT[t]} aktif yang berkantor di {e(f['label'])}:</b></p><ul>{li}</ul>{more}"
            '<p>Cek status izin terbaru di <a href="/cek-izin/">Cek Izin KAP, KJA, KJPP</a>.</p>')


def faq(f, t, grup, seed):
    lab, pv = f["label"], f["prov"]
    q = []
    if t != "all":
        S, c = L.SHORT[t], f["off"][t]
        a = f"Per {TGL}, registri PPPK Kemenkeu mencatat {c} {L.LABEL[t]} berstatus aktif di {lab}"
        a += "." if f["kind"] == "provinsi" else f" dan {f['prov_off'][t]} di Provinsi {pv}."
        q.append((f"Berapa jumlah {S} aktif di {lab}?", a))
    else:
        tot = sum(f["off"].values())
        q.append((f"Berapa kantor akuntan dan penilai berizin di {lab}?",
                  f"Per {TGL}: {f['off']['kap']} KAP, {f['off']['kja']} KJA, dan {f['off']['kjpp']} KJPP berstatus aktif ({tot} kantor), menurut registri PPPK Kemenkeu."))
    if t != "all" and f["kind"] != "provinsi" and f["off"][t] == 0:
        near = (f.get("near") or {}).get(t)
        if near:
            d, o, c = near[0]
            q.append((f"Di mana {L.SHORT[t]} terdekat dari {lab}?", f"Yang terdekat tercatat di {o}, sekitar {L.rp(d)} km, dengan {c} {L.SHORT[t]} aktif."))
    Q2 = {
        "audit": (f"Apakah KAP untuk perusahaan di {lab} harus berkantor di {lab}?", "Tidak. Izin KAP berlaku nasional. Yang perlu dicek adalah status izinnya aktif dan, bila diminta, terdaftar di OJK atau masuk rekanan bank Anda."),
        "bpr": (f"Apakah BPR di {lab} boleh diaudit KAP dari kota lain?", "Boleh. Untuk BPR yang wajib diaudit, yang disyaratkan adalah KAP dan akuntan publik yang terdaftar di OJK, bukan lokasi kantornya."),
        "dampingi": (f"Apakah pendampingan audit bisa dilakukan untuk perusahaan di {lab} dari jarak jauh?", "Bisa. Permintaan data (PBC) dan tanya jawab dengan auditor umumnya lewat dokumen digital dan rapat daring; kunjungan dilakukan untuk stock opname atau cek fisik aset."),
        "forensik": (f"Siapa yang boleh melakukan audit investigasi untuk perusahaan di {lab}?", "Audit investigasi dan pemeriksaan khusus bisa dilakukan akuntan forensik. Bila hasilnya untuk pengadilan atau pihak ketiga, pastikan kualifikasi pemeriksa dan ruang lingkupnya tertulis sejak awal."),
        "lk": (f"Apakah laporan keuangan usaha di {lab} harus disusun KJA?", "Tidak wajib, tetapi bank dan investor lebih nyaman bila penyusunnya kantor berizin. KJA tercatat di registri Kemenkeu sehingga statusnya bisa dicek siapa saja."),
        "lkjenis": (f"Dokumen apa yang disiapkan usaha di {lab} untuk menyusun laporan keuangan?", "Rekening koran, nota penjualan dan pembelian, daftar aset, utang, dan stok akhir periode. Kalau belum rapi, mulai dari rekening koran dan daftar aset."),
        "sabh": (f"Apakah PT di {lab} wajib menyampaikan laporan tahunan?", "Laporan tahunan PT disetujui RUPS. Perusahaan dengan kriteria tertentu (antara lain aset atau omzet minimal Rp50 miliar) wajib laporan keuangannya diaudit KAP."),
        "bukubesar": (f"Berapa lama merapikan buku besar usaha di {lab}?", "Tergantung jumlah rekening bank dan transaksi. Satu tahun buku usaha kecil-menengah biasanya beberapa minggu bila rekening koran lengkap."),
        "psak": (f"PSAK apa yang paling sering ditanyakan perusahaan di {lab}?", "PSAK 116 (sewa), PSAK 115 (pendapatan), PSAK 109 (cadangan piutang), dan PSAK 224 (imbalan kerja) paling sering muncul saat audit pertama atau syarat bank."),
        "jualrs": (f"Apakah valuasi RS di {lab} perlu KJPP?", "Untuk negosiasi awal cukup analisis internal. Untuk agunan bank, transaksi dengan pihak berelasi, atau perusahaan terbuka, biasanya diminta laporan penilaian KJPP."),
        "dirrs": (f"Berapa kecamatan yang dicakup RS di {lab}?", f"{lab} mencakup {f['n_kec']} kecamatan dan {L.rp(f['n_desa'])} desa atau kelurahan. Luas cakupan ini memengaruhi strategi rujukan dan jejaring FKTP."),
        "rs": (f"Berapa luas wilayah layanan di {lab}?", f"{lab} mencakup {f['n_kec']} kecamatan dan {L.rp(f['n_desa'])} desa atau kelurahan. Kunjungan ke rumah sakit atau klinik dijadwalkan sesuai kebutuhan."),
        "hub": (f"Berapa kecamatan di {lab}?", f"{lab} mencakup {f['n_kec']} kecamatan dan {L.rp(f['n_desa'])} desa atau kelurahan."),
        "murah": (f"Kenapa harga KAP di {lab} bisa berbeda jauh?", "Selain kelas KAP, harga dipengaruhi jumlah entitas, kerapian pembukuan, dan apakah ini audit pertama. Biaya perjalanan tim juga dihitung bila KAP berkantor di kota lain."),
        "kjpp": (f"Apakah KJPP harus dari {lab}?", "Tidak. Yang penting KJPP itu masuk rekanan bank Anda dan izinnya aktif. KJPP dari kota lain biasanya menambahkan biaya perjalanan untuk inspeksi lapangan."),
        "pajak": (f"Apakah konsultan pajak harus berkantor di {lab}?", "Tidak. Urusan pajak hampir seluruhnya daring (Coretax). Yang perlu dicek adalah izin praktik konsultan pajaknya."),
        "kdmp": (f"Apakah koperasi desa di {lab} wajib menyusun laporan keuangan?", "Ya. Koperasi menyampaikan laporan pertanggungjawaban di RAT setiap tahun; koperasi dengan skala tertentu juga wajib diaudit."),
    }
    if grup in Q2 and f["kind"] == "provinsi" and grup in ("dirrs", "rs", "hub"):
        q.append((f"Berapa kabupaten dan kota di {lab}?", f"{f['n_kab']} kabupaten dan {f['n_kot']} kota, dengan {L.rp(f['n_kec'])} kecamatan."))
    elif grup in Q2:
        q.append(Q2[grup])
    return "".join(f'<details class="faq-i"><summary>{e(a)}</summary><p>{e(b)}</p></details>' for a, b in q)


def blok(site, loc, focus, grup, seed, txt):
    f = L.facts(loc)
    t = focus
    h2 = L.pick(seed + "h", JUDUL[grup]).format(L=f["label"])
    parts = [M0, f"<h2>{e(h2)}</h2>", f"<p>{e(wilayah_kalimat(f, seed))}</p>", tabel(f, t),
             f"<p>{e(tafsir(f, t, seed, site))}</p>"]
    if grup in ("jualrs", "dirrs", "bpr", "murah", "forensik", "rs", "kdmp", "lkjenis") and f.get("near") and f["off"].get(t if t != "all" else "kap", 1):
        tt = t if t != "all" else "kap"
        nr = L.nearest_with(tt, f["name"], 5)
        if nr:
            s_ = ", ".join(f"{o} ({L.rp(d)} km, {c} {L.SHORT[tt]})" for d, o, c in nr)
            parts.append(f"<p>{e(L.pick(seed + 'n', ['Kota terdekat dari ', 'Pilihan di kota sekitar ', 'Jarak ke kota lain yang punya ' + L.SHORT[tt] + ' dari ']))}{e(f['label'])}: {e(s_)}.</p>")
    if f["kind"] == "provinsi" and f.get("hub"):
        parts.append("<p>" + e(f"Kabupaten dan kota dengan kantor berizin terbanyak di {f['label']}: " + ", ".join(f"{n} ({c} kantor)" for n, c in f["hub"])) + ".</p>")
    parts.append(sektor(f, seed, grup))
    parts.append(daftar_kec(f, seed, txt))
    if site == "ca":
        parts.append(nama_kantor(f, t, txt))
    parts.append(f'<div class="faq-acc">{faq(f, t, grup, seed)}</div>')
    parts.append(f'<p style="font-size:13px;color:var(--muted,#666)">Sumber: registri PPPK Kemenkeu ({L.SRC.replace("https://", "")}), data per {TGL}; data wilayah administrasi Kemendagri. Jumlah kantor dihitung dari kota tercatat di registri.</p>')
    parts.append(M1)
    return "".join(p for p in parts if p)


FAQ_RE = re.compile(r'<h2[^>]*>\s*(Pertanyaan Umum|Tanya Jawab|FAQ)', re.I)


def apply(path, site, loc, focus, grup, seed):
    txt = open(path, encoding="utf-8").read()
    if re.search(r'<meta[^>]*name="robots"[^>]*noindex|<meta[^>]*noindex[^>]*name="robots"', txt):
        return 0
    base = re.sub(re.escape(M0) + r".*?" + re.escape(M1), "", txt, flags=re.S)
    base = base.replace('<div class="wrap uq-w"></div>', "")
    b = blok(site, loc, focus, grup, seed, base)
    m = FAQ_RE.search(base)
    if m:
        new = base[:m.start()] + b + base[m.start():]
    elif "</main>" in base:
        i = base.rfind("</main>")
        new = base[:i] + '<div class="wrap uq-w">' + b + "</div>" + base[i:]
        new = new.replace('<div class="wrap uq-w">' + b + "</div>", '<div class="wrap uq-w">' + b + "</div>")
    else:
        return 0
    if new != txt:
        open(path, "w", encoding="utf-8").write(new)
        return 1
    return 0


def run():
    n = {"fa": 0, "ca": 0}
    fa = os.path.join(OUT, "faindonesia")
    for fam, (focus, grup) in FA_FAM.items():
        for p in glob.glob(os.path.join(fa, fam, "*", "index.html")):
            s = p.split(os.sep)[-2]
            loc = L.resolve(s)
            if loc:
                n["fa"] += apply(p, "fa", loc, focus, grup, fam + "/" + s)
    for p in glob.glob(os.path.join(fa, "wilayah", "*", "kecamatan", "index.html")):
        s = p.split(os.sep)[-3]
        loc = L.resolve(s)
        if loc:
            n["fa"] += apply(p, "fa", loc, "all", "hub", "wilkec/" + s)
    ca = os.path.join(OUT, "cariakuntan")
    for d in glob.glob(os.path.join(ca, "kota", "*")):
        s = os.path.basename(d)
        loc = L.resolve(s)
        if not loc:
            continue
        if os.path.exists(os.path.join(d, "index.html")):
            n["ca"] += apply(os.path.join(d, "index.html"), "ca", loc, "all", "hub", "ca/" + s)
        for sub in os.listdir(d):
            p = os.path.join(d, sub, "index.html")
            if not os.path.exists(p) or sub == "kecamatan":
                continue
            if sub not in CA_SVC:
                continue  # halaman kawasan: blok kota akan sama persis antar-kawasan, dilewati
            focus, grup = CA_SVC[sub]
            n["ca"] += apply(p, "ca", loc, focus, grup, f"ca/{s}/{sub}")
    for p in glob.glob(os.path.join(ca, "kdmp", "*", "*", "index.html")):
        s = p.split(os.sep)[-2]
        loc = L.resolve(s)
        if loc:
            n["ca"] += apply(p, "ca", loc, "kja", "kdmp", "kdmp/" + s)
    print("uq-lokal diperbarui:", n)


if __name__ == "__main__":
    run()
