# -*- coding: utf-8 -*-
"""5 Nov 2026 sore (Bos: "belum di setiap kota, kecamatan, dan desa. Gak hanya RS, klinik juga. Push sampai mentok").
Pemicu: pencarian "jasa konsultan rumah sakit purbalingga" tidak menampilkan FA (Purbalingga tidak masuk 113 kota).
- Pilar baru /konsultan-klinik/ + /konsultan-klinik/<kota>/ (113 kota).
- /konsultan-rumah-sakit/<kabupaten-x|kota-x>/ dan /konsultan-klinik/<kabupaten-x|kota-x>/ untuk 393 kabupaten/kota lain
  (data shared/wilayah). Isi unik: semua kecamatan + nama desa/kelurahan (blok Area Layanan, sama dengan shared/area_layanan.py).
- Blok Area Layanan (kecamatan + desa) juga di /konsultan-rumah-sakit/<kota>/ dan /konsultan-klinik/<kota>/ (113 kota).
- Hub semua wilayah per provinsi di /konsultan-rumah-sakit/ dan /konsultan-klinik/.
- Baris link RS + klinik di 2.032 halaman kecamatan /wilayah/<kota>/kecamatan/<kec>/.
- Desa TIDAK dibuat halaman sendiri: halaman tipis berisiko dianggap doorway oleh Google, dan batas 20.000 file per deploy Cloudflare Pages.
  Nama desa tetap terindeks lewat blok Area Layanan di halaman kabupaten/kota.
Jalankan setelah fa_rs_daerah_20261105.py dan SEBELUM fa_rs_tim_20261105.py (blok foto tim + tombol WA). Idempoten."""
import os, re, csv, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_rs_daerah_20261105.py"), encoding="utf-8").read()
_src = _src[:_src.index("CITIES = []")]          # helper fa_lead + TOOLS, sig_sec, dlv_tbl, PIL
exec(compile(_src, "fa_rs_daerah_helpers", "exec"))
sys.path.insert(0, os.path.join(HERE, "cariakuntan")); sys.path.insert(0, os.path.join(HERE, "shared")); sys.path.insert(0, os.path.join(HERE, "shared", "wilayah"))
from cities import CITIES as CC
import kec as KC
import area_layanan as AL

W = os.path.join(HERE, "shared", "wilayah")
def sl(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
PROV = {r[0]: KC.tc(r[1]) for r in csv.reader(open(os.path.join(W, "provinces.csv"), encoding="utf-8"))}
DIST = {}
for d in csv.reader(open(os.path.join(W, "districts.csv"), encoding="utf-8")): DIST.setdefault(d[1], []).append(d)
VIL = {}
for v in csv.reader(open(os.path.join(W, "villages.csv"), encoding="utf-8")): VIL.setdefault(v[1], []).append(KC.tc(v[2]))
CITY_ROWS = KC.by_city(CC)
HAVE = {sl(c[0]) for c in CC}
URLS = []

def area_block(name, rows, kind):
    b = AL.block(name, rows, "fa")
    what = ("konsultan rumah sakit: keuangan, M&amp;A, unit cost, akreditasi, BPJS, dan operasional" if kind == "rs"
            else "perhitungan unit cost dan tarif rumah sakit serta klinik" if kind == "uc"
            else "konsultan klinik: studi kelayakan, perizinan, BPJS, unit cost dan tarif, laporan keuangan, dan pendanaan")
    b = re.sub(r"<p>Kami melayani .*?</p>", f"<p>Kami melayani {what} untuk rumah sakit, RSIA, dan klinik di seluruh {E(name)}, termasuk kecamatan dan desa/kelurahan berikut. Pertemuan bisa di lokasi Anda atau daring.</p>", b, count=1, flags=re.S)
    b = b.replace("<details open>", "<details>")   # tertutup default supaya tombol WA tidak tenggelam
    return b.replace("<!--area-layanan-->", "<!--rsw-area-->").replace("<!--/area-layanan-->", "<!--/rsw-area-->")

def inject_area(p, blk):
    t = rd(p)
    t = re.sub(r"<!--rsw-area-->.*?<!--/rsw-area-->", "", t, flags=re.S)
    k = -1
    for mark in ("<!--fa-rsd-->", "<!--fa-tools-->", "<h2>Pertanyaan Umum</h2>"):
        k = t.find(mark)
        if k >= 0: break
    if k < 0: return 0
    t = t[:k] + blk + t[k:]
    if "area-layanan-css" not in t: t = t.replace("</head>", AL.CSS + "</head>", 1)
    wtxt(p, t); return 1

def finish(path):
    fp = P(*path.strip("/").split("/"), "index.html"); t = rd(fp)
    wtxt(fp, t.replace(AUTHOR_BOX, "").replace("Chat Ananta, CPA", "Chat WhatsApp"))

# ---------------- konten ----------------
RS_ROWS = [("Studi kelayakan dan ekspansi", "Gedung baru, tambah tempat tidur, layanan unggulan, atau RS kedua"),
           ("Kredit bank rumah sakit", "Kredit investasi gedung dan alat kesehatan, modal kerja klaim BPJS"),
           ("Akuisisi dan jual rumah sakit", "Due diligence, valuasi, teaser anonim, sampai closing"),
           ("Unit cost dan tarif", "Biaya per tindakan dan per kasus dibanding tarif INA-CBG atau iDRG"),
           ("Akreditasi dan BPJS", "Gap assessment, dokumen, simulasi telusur, kerja sama BPJS Kesehatan"),
           ("Laporan keuangan dan audit", "Laporan keuangan sesuai PSAK, siap audit dan siap due diligence")]
KL_ROWS = [("Studi kelayakan klinik", "Lokasi, pasar, investasi alat dan gedung, proyeksi arus kas, titik impas"),
           ("Perizinan dan standar", "Peta dokumen izin klinik pratama atau utama lewat OSS dan dinas kesehatan"),
           ("Kerja sama BPJS Kesehatan", "Hitung untung rugi kapitasi FKTP, rasio rujukan, dan kebutuhan dokter"),
           ("Unit cost dan tarif", "Biaya per kunjungan dan per tindakan, tarif pasien umum dan asuransi"),
           ("Laporan keuangan dan pajak", "Pembukuan bulanan, laporan keuangan SAK EMKM atau SAK EP, siap kredit"),
           ("Pendanaan, jual beli, naik ke RS", "Kredit bank, investor, valuasi klinik, peta jalan klinik menjadi rumah sakit")]
KL_DLV = [("Studi kelayakan", "Analisis pasar, investasi, proyeksi 5 tahun, titik impas", "2-4 minggu"),
          ("Model unit cost dan tarif", "Excel per layanan yang bisa diperbarui sendiri", "3-6 minggu"),
          ("Analisis kapitasi BPJS", "Peserta, kapitasi, biaya layanan, rasio rujukan", "1-2 minggu"),
          ("Laporan keuangan", "Bulanan atau tahunan sesuai SAK EMKM / SAK EP", "Berjalan"),
          ("Paket kredit atau investor", "Financial model, profil, data room", "3-6 minggu")]
def faq_rs(n, pv):
    return [(f"Ada konsultan rumah sakit untuk RS di {n}?", f"Ada. Tim FA Indonesia melayani rumah sakit, RSIA, dan klinik di {n}, {pv}, secara daring dengan kunjungan lapangan bila diperlukan."),
            (f"Bisa bantu jual atau beli rumah sakit di {n}?", "Bisa. Due diligence, valuasi, teaser anonim, dan pendampingan negosiasi sampai closing."),
            ("Bagaimana memulai?", "Hubungi Tim Rumah Sakit lewat tombol WhatsApp. Diskusi awal untuk memetakan kebutuhan, lalu ruang lingkup dan jadwal disepakati.")]
def faq_kl(n, pv):
    return [(f"Ada konsultan klinik di {n}?", f"Ada. Tim FA Indonesia melayani klinik pratama, klinik utama, dan klinik kecantikan di {n}, {pv}, daring maupun kunjungan."),
            ("Apakah kapitasi BPJS menguntungkan untuk klinik?", "Tergantung jumlah peserta, biaya layanan, dan rasio rujukan. Kami hitung dengan data klinik Anda sebelum memutuskan kerja sama."),
            ("Bisakah klinik dibantu naik menjadi rumah sakit?", "Bisa. Kami susun peta jalan keuangan, perizinan, SDM, dan pendanaannya bersama tim operasional rumah sakit.")]

UC_ROWS = [("Rawat inap", "Biaya per hari rawat per kelas, termasuk visite dan asuhan keperawatan"), ("Rawat jalan", "Biaya per kunjungan per poliklinik"),
           ("Tindakan dan operasi", "Biaya per tindakan dan per jam kamar operasi"), ("Penunjang", "Biaya per pemeriksaan laboratorium dan radiologi"),
           ("Paket JKN", "Biaya per kasus dibanding tarif INA-CBG atau iDRG")]
UC_DLV = [("Peta pusat biaya", "Unit penunjang dan produksi, dasar alokasi", "Minggu 1-2"), ("Model unit cost Excel", "Bisa diperbarui sendiri tiap tahun", "Minggu 3-6"),
          ("Analisis margin dan tarif", "Per layanan dan per kelompok kasus JKN, rekomendasi tarif", "Minggu 6-8")]
def faq_uc(n):
    return [(f"Siapa yang bisa menghitung unit cost rumah sakit di {n}?", f"Tim FA Indonesia menghitung unit cost untuk rumah sakit dan klinik di {n} memakai data biaya dan statistik layanan Anda sendiri."),
            ("Metode apa yang dipakai?", "Double distribution untuk alokasi biaya penunjang, dan activity based costing untuk tindakan yang kompleks, disesuaikan dengan ketersediaan data."),
            ("Berapa lama prosesnya?", "Umumnya 4 sampai 8 minggu, tergantung kerapian data biaya dan statistik layanan.")]
def rs_body(n, pv, intro, blk):
    return (f"<p>{intro}</p><h2>Layanan untuk Rumah Sakit di {E(n)}</h2>" + tbl(["Layanan", "Isi"], RS_ROWS) + TOOLS + sig_sec(2) + blk
            + f'<p class="t">Lihat juga: <a href="/konsultan-klinik/">Konsultan Klinik</a> · <a href="/konsultan-akreditasi-rumah-sakit/">Akreditasi</a> · <a href="/konsultan-bpjs-rumah-sakit/">BPJS</a> · <a href="/menjual-rumah-sakit/">Menjual RS</a> · <a href="/kalkulator-valuasi-rumah-sakit/">Kalkulator Valuasi RS</a></p>')
def kl_body(n, pv, intro, blk):
    return (f"<p>{intro}</p><h2>Layanan untuk Klinik di {E(n)}</h2>" + tbl(["Layanan", "Isi"], KL_ROWS) + dlv_tbl(KL_DLV) + sig_sec(2) + blk
            + f'<p class="t">Lihat juga: <a href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a> · <a href="/konsultan-unit-cost-rumah-sakit/">Unit Cost</a> · <a href="/artikel/tata-kelola-keuangan-klinik-menjadi-rumah-sakit/">Klinik Menjadi Rumah Sakit</a> · <a href="/artikel/menghitung-tarif-layanan-klinik-dan-rumah-sakit/">Menghitung Tarif Klinik</a></p>')

# ---------------- 1. pilar klinik ----------------
KL = "/konsultan-klinik/"
svc_page(KL, "Layanan · Klinik", "Konsultan Klinik: Studi Kelayakan, BPJS, Unit Cost, Laporan Keuangan, dan Pendanaan",
         "Pendampingan untuk klinik pratama, klinik utama, dan klinik kecantikan: dari studi kelayakan dan perizinan, hitung kapitasi BPJS, unit cost dan tarif, sampai kredit bank dan rencana naik menjadi rumah sakit.",
         "<p>Klinik yang ramai belum tentu untung. Kapitasi BPJS, tarif pasien umum, biaya dokter, dan alat sering dihitung terpisah, sehingga margin baru terlihat di akhir tahun. Kami menyatukannya dalam satu model keuangan.</p>"
         + "<h2>Layanan untuk Klinik</h2>" + tbl(["Layanan", "Isi"], KL_ROWS) + dlv_tbl(KL_DLV) + sig_sec(3),
         faq_kl("seluruh Indonesia", "Indonesia"), "Konsultan Klinik: Studi Kelayakan, BPJS, Unit Cost, Tarif | FA Indonesia",
         "Konsultan klinik pratama, utama, dan kecantikan: studi kelayakan, perizinan, kapitasi BPJS, unit cost dan tarif, laporan keuangan, kredit bank. Seluruh Indonesia.",
         "Konsultan Klinik", "Clinic consulting", "/konsultan-rumah-sakit/", "Konsultan Rumah Sakit",
         "Halo FA Indonesia, saya ingin konsultasi untuk klinik kami.", "Konsultan Klinik")
finish(KL); URLS.append(KL)

# ---------------- 2. klinik 113 kota + area di RS/klinik kota ----------------
na = 0
for kota, prov, region, secs, note in CC:
    s = sl(kota); rows = CITY_ROWS.get(kota, [])
    path = f"{KL}{s}/"
    intro = f"Untuk klinik pratama, klinik utama, klinik gigi, dan klinik kecantikan di {E(kota)}, {E(prov)}. {E(kota)} adalah {E(note)}."
    svc_page(path, f"Klinik · {kota}", f"Konsultan Klinik di {kota}: Kelayakan, BPJS, Unit Cost, dan Pendanaan",
             f"Pendampingan keuangan dan bisnis untuk klinik di {E(kota)}: studi kelayakan, perizinan, kapitasi BPJS, unit cost dan tarif, laporan keuangan, sampai kredit bank.",
             kl_body(kota, prov, intro, area_block(kota, rows, "kl") if rows else ""), faq_kl(kota, prov),
             f"Konsultan Klinik {kota}: Kelayakan, BPJS, Unit Cost | FA Indonesia",
             _cut(f"Konsultan klinik di {kota}, {prov}: studi kelayakan, perizinan, kapitasi BPJS, unit cost dan tarif, laporan keuangan, kredit bank. Diskusi awal lewat WhatsApp."),
             f"Konsultan Klinik {kota}", "Clinic consulting", KL, "Konsultan Klinik", f"Halo FA Indonesia, saya ingin konsultasi untuk klinik di {kota}.", f"Klinik {kota}")
    finish(path); URLS.append(path)
    if rows:
        for base in ("konsultan-rumah-sakit", "konsultan-unit-cost-rumah-sakit"):
            p = P(base, s, "index.html")
            if os.path.exists(p):
                na += inject_area(p, area_block(kota, rows, "uc" if "unit-cost" in base else "rs")); wtxt(p, AL.alias_head(rd(p), kota))
        p = P("konsultan-klinik", s, "index.html"); wtxt(p, AL.alias_head(rd(p), kota))

# ---------------- 3. 393 kabupaten/kota lain: RS + klinik ----------------
HUB = []   # (provinsi, nama, slug)
for k, v in [(c[0], c) for c in CC]:
    HUB.append((v[1], v[0], sl(v[0])))
nk = 0
for code, pc, name in csv.reader(open(os.path.join(W, "regencies.csv"), encoding="utf-8")):
    jenis = "Kota" if name.startswith("KOTA ") else "Kabupaten"
    base = KC.tc(name.split(" ", 1)[1]).replace("Administrasi ", ""); full = f"{jenis} {base}"
    if sl(base) in HAVE: continue
    s = sl(full); pv = PROV.get(pc, "")
    rows = [dict(kab=full, kec=KC.tc(d[2]), slug=sl(d[2]), desa=sorted(VIL.get(d[0], [])), kode=d[0]) for d in sorted(DIST.get(code, []), key=lambda x: x[2])]
    nd = sum(len(r["desa"]) for r in rows)
    kk = ", ".join(r["kec"] for r in rows[:3])
    intro = f"{E(full)}, {E(pv)}, terdiri dari {len(rows)} kecamatan dan {nd} desa/kelurahan. Pekerjaan dilakukan daring dengan kunjungan lapangan terjadwal."
    # RS
    path = f"/konsultan-rumah-sakit/{s}/"
    svc_page(path, f"Rumah Sakit · {full}", f"Konsultan Rumah Sakit di {full}, {pv}",
             f"Pendampingan keuangan dan operasional untuk rumah sakit, RSIA, dan klinik utama di {E(full)}: ekspansi, kredit bank, akuisisi dan jual RS, unit cost, akreditasi, dan BPJS.",
             rs_body(full, pv, "Untuk rumah sakit di " + intro, area_block(full, rows, "rs")), faq_rs(full, pv),
             f"Konsultan Rumah Sakit {full}: Keuangan, M&A, Unit Cost | FA Indonesia",
             _cut(f"Konsultan rumah sakit di {full}, {pv}: {kk}, dan kecamatan lain. Ekspansi, kredit bank, jual beli RS, unit cost, akreditasi, BPJS."),
             f"Konsultan Rumah Sakit {full}", "Hospital consulting", "/konsultan-rumah-sakit/", "Konsultan Rumah Sakit",
             f"Halo FA Indonesia, saya ingin konsultasi untuk rumah sakit di {full}.", f"Rumah Sakit {full}")
    finish(path); URLS.append(path)
    # klinik
    path = f"{KL}{s}/"
    svc_page(path, f"Klinik · {full}", f"Konsultan Klinik di {full}, {pv}",
             f"Pendampingan untuk klinik pratama, klinik utama, dan klinik kecantikan di {E(full)}: studi kelayakan, perizinan, kapitasi BPJS, unit cost, laporan keuangan, dan pendanaan.",
             kl_body(full, pv, "Untuk klinik di " + intro, area_block(full, rows, "kl")), faq_kl(full, pv),
             f"Konsultan Klinik {full}: Kelayakan, BPJS, Unit Cost | FA Indonesia",
             _cut(f"Konsultan klinik di {full}, {pv}: {kk}, dan kecamatan lain. Studi kelayakan, kapitasi BPJS, unit cost, laporan keuangan, kredit."),
             f"Konsultan Klinik {full}", "Clinic consulting", KL, "Konsultan Klinik",
             f"Halo FA Indonesia, saya ingin konsultasi untuk klinik di {full}.", f"Klinik {full}")
    finish(path); URLS.append(path)
    # unit cost
    path = f"/konsultan-unit-cost-rumah-sakit/{s}/"
    svc_page(path, f"Unit Cost · {full}", f"Konsultan Unit Cost Rumah Sakit dan Klinik di {full}, {pv}",
             f"Perhitungan unit cost per layanan untuk rumah sakit dan klinik di {E(full)}: metode double distribution atau activity based costing, analisis margin terhadap tarif INA-CBG atau iDRG, dan rekomendasi tarif.",
             (f"<p>Untuk rumah sakit dan klinik di {intro}</p><h2>Unit Cost yang Dihitung</h2>" + tbl(["Layanan", "Unit cost"], UC_ROWS)
              + dlv_tbl(UC_DLV) + TOOLS + area_block(full, rows, "uc")
              + '<p class="t">Lihat juga: <a href="/konsultan-unit-cost-rumah-sakit/">Konsultan Unit Cost</a> · <a href="/artikel/cara-menghitung-unit-cost-rumah-sakit/">Cara Menghitung Unit Cost RS</a> · <a href="/artikel/unit-cost-vs-tarif-ina-cbgs-rumah-sakit-swasta/">Unit Cost vs Tarif INA-CBG</a></p>'),
             faq_uc(full), f"Konsultan Unit Cost Rumah Sakit & Klinik {full} | FA Indonesia",
             _cut(f"Hitung unit cost rumah sakit dan klinik di {full}, {pv}: rawat inap, rawat jalan, tindakan, penunjang, margin INA-CBG/iDRG, rekomendasi tarif."),
             f"Konsultan Unit Cost {full}", "Hospital unit cost analysis", "/konsultan-unit-cost-rumah-sakit/", "Konsultan Unit Cost",
             f"Halo FA Indonesia, saya ingin konsultasi unit cost rumah sakit/klinik di {full}.", f"Unit Cost {full}")
    finish(path); URLS.append(path)
    HUB.append((pv, full, s)); nk += 1

# ---------------- 4. hub per provinsi di dua pilar ----------------
groups = {}
for pv, n, s in HUB: groups.setdefault(pv or "Lainnya", []).append((n, s))
for base, lab in (("konsultan-rumah-sakit", "Konsultan Rumah Sakit"), ("konsultan-klinik", "Konsultan Klinik")):
    p = P(base, "index.html"); t = rd(p)
    t = re.sub(r"<!--rsw-hub-->.*?<!--/rsw-hub-->", "", t, flags=re.S)
    blk = (f'<!--rsw-hub--><h2>{lab} di Seluruh Kabupaten dan Kota</h2>'
           + "".join(f'<details class="fold"><summary>{E(g)} ({len(v)})</summary><p class="t">' + " · ".join(f'<a href="/{base}/{s}/">{E(n)}</a>' for n, s in sorted(v)) + '</p></details>'
                     for g, v in sorted(groups.items())) + '<!--/rsw-hub-->')
    k = t.find("<h2>Pertanyaan Umum</h2>")
    if k > 0: wtxt(p, t[:k] + blk + t[k:])

# ---------------- 5. baris link di halaman kecamatan ----------------
nkec = 0
for p in glob.glob(P("wilayah", "*", "kecamatan", "*", "index.html")):
    city = p.split(os.sep)[-4]
    t = re.sub(r"<!--rsw-kec-->.*?<!--/rsw-kec-->", "", rd(p), flags=re.S)
    m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    kecn = re.sub(r"<[^>]+>", "", m.group(1)).split(",")[0].replace("Akuntan dan KAP", "").strip() if m else ""
    row = (f'<!--rsw-kec--><p class="t">Rumah sakit dan klinik di {E(kecn) or "wilayah ini"}: <a href="/konsultan-rumah-sakit/{city}/">Konsultan Rumah Sakit</a> · '
           f'<a href="/konsultan-klinik/{city}/">Konsultan Klinik</a> · <a href="/konsultan-unit-cost-rumah-sakit/{city}/">Unit Cost</a></p><!--/rsw-kec-->')
    k = t.find("<!--/fa-forensik-k-->")
    k = k + len("<!--/fa-forensik-k-->") if k > 0 else t.find("<!--fa-tools-->")
    if k < 0: continue
    wtxt(p, t[:k] + row + t[k:]); nkec += 1

# ---------------- 6. sitemap + llms ----------------
sm = re.sub(r"<!--rsw-->.*?<!--/rsw-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
have = set(re.findall(r"<loc>([^<]+)</loc>", sm))
add = "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in URLS if f"{D}{u}" not in have)
wtxt(P("sitemap.xml"), sm.replace("</urlset>", "<!--rsw-->\n" + add + "<!--/rsw-->\n</urlset>"))
ll = rd(P("llms.txt")); line = "- Konsultan Klinik (pratama, utama, kecantikan: kelayakan, BPJS, unit cost, pendanaan; per kabupaten/kota) → https://faindonesia.co.id/konsultan-klinik/\n"
if line not in ll: wtxt(P("llms.txt"), ll.rstrip("\n") + "\n" + line)
print("fa_rs_wilayah: url", len(URLS), "kab/kota baru", nk, "area kota", na, "kecamatan", nkec)
