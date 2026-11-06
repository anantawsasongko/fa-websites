# -*- coding: utf-8 -*-
"""6 Nov 2026 (Bos: "kerjakan di seluruh Indonesia agar nemukan dan WA saya. Konsultan Rumah Sakit, Unit Cost, Klinik,
Klinik BPJS, Optimalisasi Farmasi, SIMRS, dll semuanya. Lalu Auditor KAP semua kota dan kecamatan. Penyusunan laporan
keuangan di semua kota dan kecamatan, perusahaan, UMKM, cafe, restoran, klinik, semuanya").
Pemicu: pencarian "konsultan klinik bpjs aceh" dan "audit laporan keuangan gayo aceh" tidak menampilkan FA.

BEKERJA LANGSUNG DI out/faindonesia (jalankan SETELAH prep.py). Alasan: build penuh dari sumber tidak sama dengan live
(README-DEPLOY, PERINGATAN BUILD), jadi halaman baru dibentuk dari halaman live sebagai template (head, header, footer,
strip KAP/KJA, CSS) dan sisipan di halaman lama dibatasi blok berpenanda. Idempoten.

Yang dibuat:
1. Layanan baru, pilar + per provinsi + 506 kabupaten/kota (blok Area Layanan: semua kecamatan + desa/kelurahan):
   /konsultan-klinik-bpjs/, /konsultan-farmasi-rumah-sakit/, /konsultan-simrs/, /jasa-penyusunan-laporan-keuangan/<wilayah>/.
2. /konsultan-akreditasi-rumah-sakit/ dan /konsultan-bpjs-rumah-sakit/ untuk 393 kabupaten/kota yang belum ada.
3. Halaman provinsi /<layanan>/provinsi-<prov>/ untuk semua layanan wilayah (RS, klinik, unit cost, akreditasi, BPJS RS,
   audit KAP, akuntan forensik, + layanan baru): daftar semua kabupaten/kota di provinsi itu.
4. Laporan keuangan per jenis usaha (cafe dan restoran, klinik dan apotek, perusahaan PT/CV, kontraktor, koperasi dan BUMDes,
   yayasan dan sekolah, toko dan distributor; UMKM memakai pilar lama) nasional + per provinsi.
5. Blok "Layanan Lain di <wilayah>" di semua halaman wilayah (penanda fanas-x), hub provinsi di pilar (fanas-hub),
   baris link di 2.032 halaman kecamatan (fanas-kec), sitemap (fanas), llms.txt.
Desa tidak dibuat halaman sendiri (doorway, batas 20.000 file Cloudflare Pages); nama kecamatan dan desa terindeks lewat blok
Area Layanan di halaman kabupaten/kota."""
import os, re, csv, sys, json, html, glob, urllib.parse, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faindonesia")
sys.path.insert(0, os.path.join(HERE, "cariakuntan")); sys.path.insert(0, os.path.join(HERE, "shared")); sys.path.insert(0, os.path.join(HERE, "shared", "wilayah"))
from cities import CITIES as CC
import kec as KC
import area_layanan as AL

E = html.escape
D = "https://faindonesia.co.id"
WA = "https://wa.me/6282245260121?text="
TODAY = datetime.date.today().isoformat()
W = os.path.join(HERE, "shared", "wilayah")


def sl(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def rd(p): return open(p, encoding="utf-8").read()
def wt(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(t)
def P(path): return os.path.join(OUT, *path.strip("/").split("/"), "index.html")
def cut(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    while len(s) > n and ". " in s:          # buang kalimat terakhir dulu, baru potong kata
        s = s.rsplit(". ", 1)[0] + "."
    if len(s) <= n: return s
    s = s[:n].rsplit(" ", 1)[0].rstrip(",;:")
    return s + "."
def hid(s): return sl(html.unescape(re.sub(r"<[^>]+>", "", s)))[:60].rstrip("-")
def wa(txt): return WA + urllib.parse.quote(txt, safe="")
def num(x): return f"{x:,}".replace(",", ".")
def lw(s): return s if s[:2].isupper() else s[:1].lower() + s[1:]   # SIMRS, BPJS, RS tetap kapital
def pfix(n):
    n = KC.tc(n)
    return {"Dki Jakarta": "DKI Jakarta", "Di Yogyakarta": "DI Yogyakarta"}.get(n, n)


# ---------------- data wilayah ----------------
PROVC = {r[0]: pfix(r[1]) for r in csv.reader(open(os.path.join(W, "provinces.csv"), encoding="utf-8"))}
DIST = {}
for d in csv.reader(open(os.path.join(W, "districts.csv"), encoding="utf-8")): DIST.setdefault(d[1], []).append(d)
VIL = {}
for v in csv.reader(open(os.path.join(W, "villages.csv"), encoding="utf-8")): VIL.setdefault(v[1], []).append(KC.tc(v[2]))
CITY_ROWS = KC.by_city(CC)
HAVE = {sl(c[0]) for c in CC}
REG = []   # dict(slug, name, prov, rows)
for kota, prov, region, secs, note in CC:
    REG.append(dict(slug=sl(kota), name=kota, prov=prov, rows=CITY_ROWS.get(kota, []), note=note))
for code, pc, name in csv.reader(open(os.path.join(W, "regencies.csv"), encoding="utf-8")):
    jenis = "Kota" if name.startswith("KOTA ") else "Kabupaten"
    base = KC.tc(name.split(" ", 1)[1]).replace("Administrasi ", "")
    if sl(base) in HAVE: continue
    full = f"{jenis} {base}"
    rows = [dict(kab=full, kec=KC.tc(d[2]), slug=sl(d[2]), desa=sorted(VIL.get(d[0], [])), kode=d[0]) for d in sorted(DIST.get(code, []), key=lambda x: x[2])]
    REG.append(dict(slug=sl(full), name=full, prov=PROVC.get(pc, ""), rows=rows, note=""))
for r in REG:
    r["disp"] = f'{r["name"]} ({AL.ALIAS[r["name"]]})' if r["name"] in AL.ALIAS else r["name"]
    r["nk"] = len(r["rows"]); r["nd"] = sum(len(x["desa"]) for x in r["rows"])
    r["kk"] = ", ".join(x["kec"] for x in r["rows"][:3])
    r["pslug"] = "provinsi-" + sl(r["prov"])
BYPROV = {}
for r in REG: BYPROV.setdefault(r["prov"], []).append(r)
PROVS = sorted(BYPROV)
assert len(REG) >= 500, len(REG)

# ---------------- template dari halaman live ----------------
TPL = rd(P("/konsultan-klinik/kabupaten-gayo-lues/"))
LKP = rd(P("/jasa-penyusunan-laporan-keuangan/"))
def between(t, a, b, inc=True):
    i = t.index(a); j = t.index(b, i) + (len(b) if inc else 0)
    return t[i:j]
RSTIM = between(TPL, "<!--fa-rstim-->", "<!--/fa-rstim-->")
PENGALAMAN = between(TPL, '<h2 id="pengalaman-memimpin-rumah-sakit">', "<!--rsw-area-->", inc=False)
PENGALAMAN = PENGALAMAN.replace('<h2 id="pengalaman-memimpin-rumah-sakit">', "<h2>")
WAJAH = between(LKP, "<!--fa-wajah-->", "<!--/fa-wajah-->")
WAJAH = re.sub(r'<h2 id="[^"]*">', "<h2>", WAJAH)
TOOLS = between(LKP, "<!--fa-tools-->", "<!--/fa-tools-->")
TOOLS = re.sub(r'<h2 id="[^"]*">', "<h2>", TOOLS)
AKR = rd(P("/konsultan-akreditasi-rumah-sakit/malang/")); BPR_ = rd(P("/konsultan-bpjs-rumah-sakit/malang/"))
def sec_of(t, h2id):
    i = t.index(f'<h2 id="{h2id}">'); j = t.find("<h2", i + 5)
    return re.sub(r'<h2 id="[^"]*">', "<h2>", t[i:j])
def para2(t):
    m = t[t.index("<main"):]
    ps = re.findall(r"<p>(.*?)</p>", m[:m.index("<nav")], re.S)
    return ps[-1]
def faqs_of(t):
    return [(html.unescape(a), html.unescape(b)) for a, b in re.findall(r'<details class="faq-i"><summary>(.*?)</summary><p>(.*?)</p></details>', t)]
AKR_INTRO, BPJ_INTRO = para2(AKR), para2(BPR_)
AKR_SEC = sec_of(AKR, "deliverables-yang-anda-terima") + sec_of(AKR, "tools-buatan-fa-yang-dipakai")
BPJ_SEC = sec_of(BPR_, "deliverables-yang-anda-terima") + sec_of(BPR_, "tools-buatan-fa-yang-dipakai")
AKR_FAQ, BPJ_FAQ = faqs_of(AKR), faqs_of(BPR_)
assert "Malang" not in AKR_SEC + BPJ_SEC + AKR_INTRO + BPJ_INTRO

HEAD_END = TPL.index("<main")
MAIN_END = TPL.index("</main>")


def og_img(key, kicker, title):
    try:
        import share_all
        return share_all._poster("fa", kicker, title, key, OUT)
    except Exception as e:   # tanpa font/foto: pakai poster pilar terdekat
        print("og fallback", key, e)
        return "/img/og-page/konsultan-klinik.jpg"


def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")


def page(path, eyebrow, h1, lead, watxt, back, intro, secs, faq, title, desc, svc, stype, crumb, og, team="", area="", extra=""):
    """secs: list of (h2, html). Hasil: halaman lengkap memakai head/header/footer live."""
    url = D + path
    body, nav = [], []
    for h, hh in secs:
        i = hid(h); nav.append(f'<li><a href="#{i}">{E(h)}</a></li>'); body.append(f'<h2 id="{i}">{E(h)}</h2>{hh}')
    if area:
        m = re.search(r"<h2>(.*?)</h2>", area)
        i = hid(m.group(1)); area = area.replace("<h2>", f'<h2 id="{i}">', 1)
        nav.append(f'<li><a href="#{i}">{m.group(1)}</a></li>')
    pmap = f'<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>{"".join(nav)}</ol></nav>' if len(nav) >= 2 else ""
    btn = f'<a class="btn solid" href="{wa(watxt)}" rel="noopener" target="_blank">Chat WhatsApp</a>'
    fq = ('<h2>Pertanyaan Umum</h2><div class="faq-acc">' + "".join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq) + "</div>")
    main = ('<main id="top">\n<section class="block">\n<div class="wrap art">\n'
            f'<p class="eyebrow">{E(eyebrow)}</p>\n'
            f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{E(h1)}</h1><div class="tshare-top"><div class="share" data-lab="Bagikan" data-tool="{E(h1)}"></div></div>\n'
            f'<p class="t" style="max-width:62em">{lead}</p>\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px">{btn}<a class="btn line" href="{back[0]}">{E(back[1])}</a></div>\n'
            f'<p>{intro}</p>{pmap}' + "".join(body) + area + extra + "\n" + team + "\n" + fq
            + f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px">{btn}</div>\n</div>\n</section>\n')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": svc, "serviceType": stype,
         "provider": {"@type": "ProfessionalService", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"},
         "areaServed": {"@type": "Country", "name": "Indonesia"}, "url": url},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": D + u} for i, (n, u) in enumerate(crumb)]}]}
    head = TPL[:HEAD_END]
    title, desc = E(title), E(cut(desc))
    head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{title}</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description")/>', lambda m: f'<meta content="{desc}" {m.group(1)}/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:title"/>', lambda m: f'<meta content="{title}" property="og:title"/>', head)
    head = re.sub(r'<link href="[^"]*" rel="canonical"/>', lambda m: f'<link href="{url}" rel="canonical"/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:url"/>', lambda m: f'<meta content="{url}" property="og:url"/>', head)
    head = re.sub(r'(<meta content=")[^"]*(" (?:property="og:image"|name="twitter:image")/>)', lambda m: m.group(1) + D + og + m.group(2), head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", head, count=1, flags=re.S)
    if "area-layanan-css" not in head: head = head.replace("</head>", AL.CSS + "</head>", 1)
    t = head + main + TPL[MAIN_END:]
    wt(P(path), t)
    return path


def area(r, what):
    if not r["rows"]: return ""
    b = AL.block(r["name"], r["rows"], "fa")
    b = re.sub(r"<p>Kami melayani .*?</p>", f"<p>Kami melayani {what} di seluruh {E(r['disp'])}, termasuk kecamatan dan desa/kelurahan berikut. Pertemuan bisa di lokasi Anda atau daring.</p>", b, count=1, flags=re.S)
    b = b.replace("<details open>", "<details>").replace(' id="area-layanan"', "")
    b = re.sub(r"<h2>", "<h2>", b)
    return b.replace("<!--area-layanan-->", "<!--fanas-area-->").replace("<!--/area-layanan-->", "<!--/fanas-area-->")


def rstim(txt): return re.sub(r'(<a class="wa" href=")[^"]*(")', lambda m: m.group(1) + wa(txt) + m.group(2), RSTIM)


def wilintro(r, who):
    s = f"Untuk {who} di {E(r['disp'])}, {E(r['prov'])}"
    if r["nk"]: s += f", yang terdiri dari {r['nk']} kecamatan dan {num(r['nd'])} desa/kelurahan"
    if r["note"]: s += f". {E(r['name'])} adalah {E(r['note'])}"
    return s + ". Pekerjaan dilakukan daring dengan kunjungan lapangan terjadwal."


# ---------------- definisi layanan ----------------
F = {}
def fam(key, **kw): F[key] = dict(key=key, **kw)

fam("konsultan-klinik-bpjs", label="Konsultan Klinik BPJS", short="Klinik BPJS", kind="rs", stype="Primary care clinic BPJS consulting",
    who="klinik pratama, klinik utama, dan dokter praktik yang bekerja sama atau ingin bekerja sama dengan BPJS Kesehatan",
    what="pendampingan klinik BPJS: kerja sama FKTP, kapitasi dan KBK, biaya per peserta, rujukan, dan laporan keuangan klinik",
    h1="Konsultan Klinik BPJS di {n}: Kapitasi, KBK, dan Keuangan Klinik",
    title="Konsultan Klinik BPJS {n}: Kapitasi, KBK, Rujukan | FA Indonesia",
    desc="Konsultan klinik BPJS di {n}, {p}: kerja sama FKTP, kapitasi dan KBK, biaya per peserta, rasio rujukan, laporan keuangan klinik. Diskusi lewat WhatsApp.",
    lead="Untuk klinik yang ramai pasien BPJS tetapi marginnya tipis, atau sedang menimbang kerja sama sebagai FKTP. Kami menghitung kapitasi, indikator KBK, dan biaya per peserta dengan data klinik Anda.",
    rows=[("Kerja sama BPJS Kesehatan (FKTP)", "Persiapan dokumen, kredensialing, dan hitungan apakah kerja sama layak bagi klinik"),
          ("Kapitasi dan KBK", "Simulasi pendapatan kapitasi dari jumlah peserta terdaftar dan pemenuhan indikator Kapitasi Berbasis Kinerja"),
          ("Biaya per peserta", "Biaya dokter, obat, BMHP, dan laboratorium per peserta dibanding kapitasi yang diterima"),
          ("Rujukan dan Prolanis", "Pola rujukan kasus non spesialistik, kunjungan peserta Prolanis, dan pencatatan di PCare"),
          ("Non kapitasi", "Klaim persalinan, rawat inap tingkat pertama, dan layanan lain di luar kapitasi"),
          ("Laporan keuangan klinik", "Pendapatan kapitasi, non kapitasi, pasien umum, dan asuransi dipisah dalam laporan bulanan")],
    dlv=[("Analisis kelayakan kerja sama BPJS", "Peserta, kapitasi, biaya layanan, titik impas", "1-2 minggu"),
         ("Model kapitasi dan biaya per peserta", "Excel yang bisa diperbarui sendiri tiap bulan", "2-3 minggu"),
         ("Rencana perbaikan indikator KBK", "Angka kontak, rujukan non spesialistik, Prolanis", "2 minggu"),
         ("Laporan keuangan bulanan klinik", "Sesuai SAK EMKM atau SAK EP, siap kredit bank", "Berjalan")],
    faq=lambda n, p: [(f"Ada konsultan klinik BPJS di {n}?", f"Ada. Tim FA Indonesia melayani klinik di {n}, {p}, daring dengan kunjungan lapangan bila diperlukan."),
                      ("Kenapa klinik BPJS ramai tetapi untungnya tipis?", "Biasanya karena biaya obat, BMHP, dan jam dokter per peserta melebihi kapitasi, atau kapitasi terpotong karena indikator KBK belum terpenuhi. Kami menghitungnya dengan data klinik Anda."),
                      ("Apakah klinik baru bisa dibantu sampai kerja sama BPJS?", "Bisa. Mulai dari hitungan kelayakan, kelengkapan dokumen, sampai pencatatan keuangan setelah kerja sama berjalan.")],
    see='<a href="/konsultan-klinik/">Konsultan Klinik</a> · <a href="/konsultan-bpjs-rumah-sakit/">BPJS Rumah Sakit</a> · <a href="/konsultan-unit-cost-rumah-sakit/">Unit Cost</a> · <a href="/laporan-keuangan-klinik/">Laporan Keuangan Klinik</a>',
    og=("Konsultan Klinik BPJS", "Kapitasi, KBK, dan Keuangan Klinik di Seluruh Indonesia"))

fam("konsultan-farmasi-rumah-sakit", label="Optimalisasi Farmasi Rumah Sakit", short="Farmasi RS dan Klinik", kind="rs", stype="Hospital pharmacy optimization consulting",
    who="instalasi farmasi rumah sakit, apotek klinik, dan apotek mandiri",
    what="optimalisasi farmasi: ABC-VEN, dead stock, formularium dan Fornas, pengadaan, margin obat, dan biaya obat per kasus",
    h1="Optimalisasi Farmasi Rumah Sakit dan Klinik di {n}",
    title="Konsultan Farmasi Rumah Sakit {n}: Stok, Formularium, Margin | FA Indonesia",
    desc="Optimalisasi farmasi rumah sakit dan klinik di {n}, {p}: analisis ABC-VEN, dead stock, formularium dan Fornas, pengadaan e-katalog, margin dan HPP obat.",
    lead="Obat dan BMHP termasuk pos biaya terbesar rumah sakit dan klinik. Perbaikan kecil di pengadaan, stok, dan formularium langsung terasa di margin dan arus kas.",
    rows=[("Analisis ABC-VEN", "Mengelompokkan obat berdasarkan nilai belanja dan tingkat kepentingan untuk prioritas pengadaan"),
          ("Dead stock dan kedaluwarsa", "Menemukan obat yang tidak bergerak, mendekati kedaluwarsa, dan selisih stok opname"),
          ("Formularium dan Fornas", "Menyelaraskan formularium RS dengan Formularium Nasional untuk pasien JKN"),
          ("Pengadaan dan e-katalog", "Perbandingan harga e-katalog dan distributor (PBF), jadwal pemesanan, dan stok pengaman"),
          ("Margin dan HPP obat", "Harga pokok dan margin per kelompok pasien (umum, JKN, asuransi), kebijakan harga jual"),
          ("Biaya obat per kasus", "Porsi obat dan BMHP dalam biaya per kasus INA-CBG atau iDRG, bersama model unit cost")],
    dlv=[("Laporan ABC-VEN dan dead stock", "Daftar obat prioritas, obat lambat bergerak, dan nilainya", "2-3 minggu"),
         ("Rekomendasi formularium dan pengadaan", "Usulan item, jadwal pesan, stok minimum dan maksimum", "3-4 minggu"),
         ("Model margin obat", "Excel per kelompok pasien dan per kelas terapi", "3-4 minggu"),
         ("Dashboard persediaan bulanan", "Perputaran stok, nilai kedaluwarsa, selisih opname", "Berjalan")],
    faq=lambda n, p: [(f"Ada konsultan farmasi rumah sakit di {n}?", f"Ada. Tim FA Indonesia melayani instalasi farmasi RS, apotek klinik, dan apotek mandiri di {n}, {p}."),
                      ("Apakah harus memakai SIMRS tertentu?", "Tidak. Kami bekerja dengan data dari SIMRS, aplikasi apotek, atau Excel yang sudah dipakai."),
                      ("Apa hasil yang paling cepat terlihat?", "Biasanya penurunan dead stock dan obat kedaluwarsa, serta pembelian yang lebih terjadwal sehingga kas tidak tertahan di gudang.")],
    see='<a href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a> · <a href="/konsultan-unit-cost-rumah-sakit/">Unit Cost</a> · <a href="/konsultan-simrs/">SIMRS</a> · <a href="/konsultan-bpjs-rumah-sakit/">BPJS Rumah Sakit</a>',
    og=("Optimalisasi Farmasi", "Stok, Formularium, dan Margin Obat Rumah Sakit dan Klinik"))

fam("konsultan-simrs", label="Konsultan SIMRS", short="SIMRS", kind="rs", stype="Hospital information system (SIMRS) consulting",
    who="rumah sakit dan klinik yang memilih, mengganti, atau membenahi SIMRS",
    what="pendampingan SIMRS: pemilihan vendor, rekam medis elektronik, SATUSEHAT, bridging BPJS, dan integrasi SIMRS ke akuntansi",
    h1="Konsultan SIMRS di {n}: Pemilihan Vendor, RME, dan Integrasi ke Keuangan",
    title="Konsultan SIMRS {n}: Vendor, RME, SATUSEHAT, BPJS | FA Indonesia",
    desc="Konsultan SIMRS untuk rumah sakit dan klinik di {n}, {p}: pemilihan vendor, rekam medis elektronik, SATUSEHAT, bridging BPJS, integrasi ke akuntansi.",
    lead="SIMRS yang tidak tersambung ke keuangan membuat piutang BPJS, stok farmasi, dan pendapatan harus dicocokkan manual. Kami independen dari vendor dan membantu sejak memilih sampai datanya bisa dipakai manajemen.",
    rows=[("Kebutuhan dan pemilihan vendor", "Daftar kebutuhan per unit, perbandingan vendor, dan biaya total kepemilikan (lisensi, server, pemeliharaan)"),
          ("Rekam medis elektronik", "Kesiapan penerapan RME sesuai Permenkes 24 Tahun 2022"),
          ("Integrasi SATUSEHAT", "Pemetaan data yang dikirim ke platform SATUSEHAT Kementerian Kesehatan"),
          ("Bridging BPJS", "Alur pendaftaran, SEP, dan klaim BPJS dari SIMRS"),
          ("SIMRS ke akuntansi", "Jurnal otomatis pendapatan, piutang BPJS dan asuransi, persediaan farmasi, tutup buku bulanan"),
          ("Dashboard dan keamanan data", "Laporan manajemen, unit cost dari data SIMRS, hak akses, dan pelindungan data pribadi pasien (UU 27/2022)")],
    dlv=[("Dokumen kebutuhan SIMRS", "Per unit layanan, penunjang, farmasi, keuangan", "2-3 minggu"),
         ("Evaluasi vendor", "Skor fungsi, biaya total kepemilikan, referensi pengguna", "2-4 minggu"),
         ("Peta integrasi ke akuntansi", "Bagan akun, aturan jurnal, rekonsiliasi piutang BPJS", "3-4 minggu"),
         ("Pendampingan go-live", "Uji data, migrasi saldo awal, laporan bulan pertama", "Sesuai jadwal")],
    faq=lambda n, p: [(f"Ada konsultan SIMRS untuk rumah sakit di {n}?", f"Ada. Tim FA Indonesia melayani rumah sakit dan klinik di {n}, {p}, daring dengan kunjungan saat uji dan go-live."),
                      ("Apakah FA Indonesia menjual SIMRS?", "Tidak. Kami independen dari vendor: membantu memilih, mengevaluasi, dan menyambungkan SIMRS dengan keuangan."),
                      ("Apakah bisa untuk klinik?", "Bisa. Untuk klinik, fokusnya biasanya rekam medis elektronik, bridging BPJS, dan laporan keuangan bulanan yang keluar dari sistem.")],
    see='<a href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a> · <a href="/konsultan-farmasi-rumah-sakit/">Farmasi</a> · <a href="/konsultan-unit-cost-rumah-sakit/">Unit Cost</a> · <a href="/konsultan-bpjs-rumah-sakit/">BPJS Rumah Sakit</a>',
    og=("Konsultan SIMRS", "Pemilihan Vendor, RME, SATUSEHAT, dan Integrasi ke Keuangan"))

LK_ROWS = [("Perusahaan PT dan CV", "Laporan keuangan bulanan atau tahunan sesuai SAK EP, siap pajak, audit, dan kredit bank"),
           ("UMKM dan usaha perorangan", "Pembukuan sederhana sampai laporan keuangan SAK EMKM untuk KUR dan pinjaman"),
           ("Cafe dan restoran", "HPP menu, stok bahan, kas harian per outlet, dan laba per cabang"),
           ("Klinik dan apotek", "Pendapatan BPJS, pasien umum, dan asuransi dipisah; stok obat terkendali"),
           ("Kontraktor", "Pendapatan per proyek sesuai PSAK 115, termin, retensi, dan piutang"),
           ("Koperasi, BUMDes, yayasan, sekolah", "Laporan keuangan sesuai standar entitasnya untuk rapat anggota, donatur, dan pemeriksa")]
fam("jasa-penyusunan-laporan-keuangan", label="Jasa Penyusunan Laporan Keuangan", short="Penyusunan Laporan Keuangan", kind="lk", stype="Financial statement preparation",
    who="perusahaan, UMKM, cafe, restoran, klinik, kontraktor, koperasi, dan yayasan",
    what="penyusunan laporan keuangan, pembukuan bulanan, dan tutup buku tahunan",
    h1="Jasa Penyusunan Laporan Keuangan di {n}: Perusahaan, UMKM, Cafe, Klinik",
    title="Jasa Penyusunan Laporan Keuangan {n}: PT, CV, UMKM | FA Indonesia",
    desc="Jasa penyusunan laporan keuangan di {n}, {p}: PT, CV, UMKM, cafe, restoran, klinik, kontraktor, koperasi. Pembukuan bulanan dan tutup buku tahunan.",
    lead="Pembukuan bulanan, tutup buku tahunan, atau merapikan laporan beberapa tahun sekaligus. Hasilnya siap dipakai untuk pajak, audit, pengajuan kredit bank, dan investor.",
    rows=LK_ROWS,
    dlv=[("Laporan keuangan lengkap", "Neraca, laba rugi, arus kas, perubahan ekuitas, CALK", "Bulanan atau tahunan"),
         ("Rekonsiliasi", "Bank, piutang, utang, persediaan, aset tetap", "Bulanan"),
         ("Penyesuaian pajak", "Selaras dengan SPT dan pelaporan pajak", "Bulanan dan tahunan"),
         ("Paket kredit bank", "Laporan keuangan dan rasio yang dibaca analis kredit", "Saat dibutuhkan")],
    faq=lambda n, p: [(f"Ada jasa penyusunan laporan keuangan di {n}?", f"Ada. Tim FA Indonesia bersama KJA mitra melayani usaha di {n}, {p}. Dokumen bisa dikirim lewat Google Drive, pertemuan daring atau kunjungan."),
                      ("Usaha apa saja yang dilayani?", "PT dan CV, UMKM, cafe dan restoran, klinik dan apotek, kontraktor, koperasi, BUMDes, yayasan, dan sekolah."),
                      ("Apakah penyusun laporan keuangan juga mengaudit?", "Tidak. Untuk satu entitas, penyusun dan auditornya selalu pihak yang berbeda. Audit dilakukan KAP mitra yang terdaftar OJK.")],
    see='<a href="/jasa-penyusunan-laporan-keuangan/">Penyusunan Laporan Keuangan</a> · <a href="/laporan-keuangan-umkm/">Laporan Keuangan UMKM</a> · <a href="https://cariakuntan.com/jasa-pembukuan/">Jasa Pembukuan Terima Beres</a> · <a href="/audit-ready/">FA Jupiter</a>',
    og=None, pillar_exists=True)

# layanan lama (sudah ada di 113 kota / 506 wilayah) -> halaman provinsi + blok silang
OLD = [("konsultan-rumah-sakit", "Konsultan Rumah Sakit", "rs", "rumah sakit, RSIA, dan klinik utama", "konsultan rumah sakit: keuangan, M&amp;A, unit cost, akreditasi, BPJS, dan operasional"),
       ("konsultan-klinik", "Konsultan Klinik", "rs", "klinik pratama, klinik utama, dan klinik kecantikan", "konsultan klinik: studi kelayakan, perizinan, BPJS, unit cost, laporan keuangan, dan pendanaan"),
       ("konsultan-unit-cost-rumah-sakit", "Konsultan Unit Cost Rumah Sakit dan Klinik", "rs", "rumah sakit dan klinik", "perhitungan unit cost dan tarif rumah sakit serta klinik"),
       ("konsultan-akreditasi-rumah-sakit", "Konsultan Akreditasi Rumah Sakit", "rs", "rumah sakit dan RSIA", "persiapan akreditasi rumah sakit: gap assessment, dokumen, simulasi telusur, dan anggaran"),
       ("konsultan-bpjs-rumah-sakit", "Konsultan BPJS Rumah Sakit", "rs", "rumah sakit dan RSIA", "konsultan BPJS rumah sakit: klaim pending, margin INA-CBG/iDRG, dan arus kas"),
       ("jasa-audit-laporan-keuangan", "Jasa Audit Laporan Keuangan (KAP)", "audit", "perusahaan, koperasi, yayasan, BUMDes, dan badan usaha", "audit laporan keuangan oleh KAP mitra terdaftar OJK"),
       ("akuntan-forensik", "Akuntan Forensik", "audit", "perusahaan, yayasan, dan pemilik usaha", "akuntansi forensik: penelusuran kecurangan dan perhitungan kerugian")]
SHORT = {"konsultan-rumah-sakit": "Konsultan Rumah Sakit", "konsultan-klinik": "Konsultan Klinik", "konsultan-klinik-bpjs": "Klinik BPJS",
         "konsultan-unit-cost-rumah-sakit": "Unit Cost", "konsultan-akreditasi-rumah-sakit": "Akreditasi RS", "konsultan-bpjs-rumah-sakit": "BPJS Rumah Sakit",
         "konsultan-farmasi-rumah-sakit": "Farmasi RS dan Klinik", "konsultan-simrs": "SIMRS",
         "jasa-penyusunan-laporan-keuangan": "Penyusunan Laporan Keuangan", "jasa-audit-laporan-keuangan": "Audit Laporan Keuangan (KAP)", "akuntan-forensik": "Akuntan Forensik"}
HEALTH = ["konsultan-rumah-sakit", "konsultan-klinik", "konsultan-klinik-bpjs", "konsultan-unit-cost-rumah-sakit", "konsultan-akreditasi-rumah-sakit",
          "konsultan-bpjs-rumah-sakit", "konsultan-farmasi-rumah-sakit", "konsultan-simrs"]
FIN = ["jasa-penyusunan-laporan-keuangan", "jasa-audit-laporan-keuangan", "akuntan-forensik"]

SECTOR = [("laporan-keuangan-cafe-restoran", "Cafe dan Restoran", "cafe, restoran, kedai kopi, dan usaha kuliner",
           [("HPP per menu", "Resep standar, harga bahan, dan HPP per porsi yang diperbarui saat harga bahan naik"),
            ("Stok bahan dan waste", "Stok opname bahan, selisih pemakaian, dan bahan terbuang"),
            ("Kas harian per outlet", "Rekap kasir, QRIS, ojek online, dan setoran bank per outlet"),
            ("Laba per cabang", "Laporan laba rugi per outlet untuk keputusan buka atau tutup cabang"),
            ("Pajak", "PB1 daerah, PPh Final atau PPh Badan, dan PPh 21 karyawan")]),
          ("laporan-keuangan-klinik", "Klinik dan Apotek", "klinik pratama, klinik utama, klinik gigi, klinik kecantikan, dan apotek",
           [("Pendapatan per penjamin", "Kapitasi BPJS, non kapitasi, pasien umum, dan asuransi dipisah"),
            ("Jasa medis dokter", "Perhitungan bagi hasil dan honor dokter yang konsisten"),
            ("Stok obat dan BMHP", "Persediaan, kedaluwarsa, dan HPP obat"),
            ("Laporan untuk kredit", "Laporan keuangan dan rasio yang dibaca bank untuk alat dan gedung"),
            ("Pajak", "PPh Final atau PPh Badan, PPh 21 tenaga medis")]),
          ("laporan-keuangan-perusahaan", "Perusahaan PT dan CV", "PT dan CV skala kecil sampai menengah",
           [("Laporan keuangan SAK EP", "Neraca, laba rugi, arus kas, perubahan ekuitas, dan CALK"),
            ("Tutup buku bulanan", "Rekonsiliasi bank, piutang, utang, persediaan, dan aset tetap"),
            ("Laporan tahunan PT", "Bahan laporan tahunan direksi sesuai ketentuan yang berlaku"),
            ("Siap audit dan kredit", "Kertas kerja pendukung yang dibaca auditor dan analis bank"),
            ("Pajak", "Selaras dengan SPT Masa dan SPT Tahunan Badan")]),
          ("laporan-keuangan-kontraktor", "Kontraktor", "kontraktor sipil, MEP, interior, dan pengadaan",
           [("Pendapatan per proyek", "Pengakuan pendapatan sesuai PSAK 115 berdasarkan progres pekerjaan"),
            ("Termin dan retensi", "Tagihan termin, uang muka, retensi, dan piutang per pemberi kerja"),
            ("Biaya proyek", "Material, subkon, upah, dan alat per proyek"),
            ("Kredit modal kerja", "Laporan untuk KMK berbasis SPK dan bank garansi"),
            ("Pajak", "PPh Final jasa konstruksi dan PPN")]),
          ("laporan-keuangan-koperasi", "Koperasi dan BUMDes", "koperasi simpan pinjam, koperasi serba usaha, Koperasi Desa Merah Putih, dan BUMDes",
           [("Laporan keuangan koperasi", "Neraca, perhitungan hasil usaha, arus kas, dan catatan untuk RAT"),
            ("Simpanan dan pinjaman anggota", "Rekonsiliasi simpanan, pinjaman, dan kolektibilitas"),
            ("SHU", "Perhitungan dan pembagian sisa hasil usaha"),
            ("BUMDes", "Laporan untuk pemerintah desa dan musyawarah desa"),
            ("Siap audit", "Bahan untuk audit KAP bila diwajibkan")]),
          ("laporan-keuangan-yayasan-sekolah", "Yayasan dan Sekolah", "yayasan, sekolah, pesantren, dan lembaga nirlaba",
           [("Laporan entitas nirlaba", "Laporan posisi keuangan, penghasilan komprehensif, dan aset neto sesuai ISAK 335"),
            ("Dana terikat dan tidak terikat", "Pemisahan dana donatur, hibah, dan dana BOS"),
            ("SPP dan piutang siswa", "Pencatatan SPP, beasiswa, dan tunggakan"),
            ("Pertanggungjawaban hibah", "Laporan penggunaan dana untuk donatur dan pemberi hibah"),
            ("Siap audit", "Bahan audit KAP untuk yayasan yang diwajibkan")]),
          ("laporan-keuangan-toko-distributor", "Toko dan Distributor", "toko retail, grosir, distributor, dan importir",
           [("Persediaan dan HPP", "Kartu stok, metode HPP, dan selisih opname"),
            ("Piutang dan utang dagang", "Umur piutang, retur, diskon, dan utang ke pemasok"),
            ("Margin per produk", "Laba kotor per produk dan per pelanggan"),
            ("Kredit modal kerja", "Laporan dan siklus modal kerja yang dibaca bank"),
            ("Pajak", "PPN, PPh Final atau PPh Badan")]),
          ("laporan-keuangan-umkm", "UMKM", "usaha mikro, kecil, dan menengah", None)]


# ---------------- 1. halaman wilayah layanan baru ----------------
def rdesc(f, r):
    d = re.sub(r" Diskusi lewat WhatsApp\.$", "", f["desc"].format(n=r["disp"], p=r["prov"]))
    if not r["kk"]: return d
    head, svc = d.split(": ", 1)
    return f"{head} ({r['nk']} kecamatan, termasuk {r['kk']}): {svc}"
URLS, CNT = [], {}
def team_for(kind, txt): return rstim(txt) if kind == "rs" else WAJAH
OG = {}
for k, f in F.items():
    if f.get("og"): OG[k] = og_img("sec-" + k, *f["og"])
    else: OG[k] = "/img/og-page/jasa-penyusunan-laporan-keuangan.jpg" if os.path.exists(os.path.join(OUT, "img/og-page/jasa-penyusunan-laporan-keuangan.jpg")) else og_img("sec-" + k, f["label"], "Perusahaan, UMKM, Cafe, Restoran, Klinik di Seluruh Indonesia")

def fam_secs(f, n):
    s = [(f"Layanan {f['short']} di {n}", tbl(["Layanan", "Isi"], f["rows"])),
         ("Deliverables yang Anda Terima", tbl(["Deliverable", "Isi", "Waktu"], f["dlv"]))]
    if f["kind"] == "rs": s.append(("Pengalaman Memimpin Rumah Sakit", PENGALAMAN.split("</h2>", 1)[1]))
    return s

for k, f in F.items():
    n = 0
    for r in REG:
        path = f"/{k}/{r['slug']}/"
        txt = f"Halo FA Indonesia, saya ingin konsultasi {lw(f['short'])} di {r['name']}."
        n_ = r["disp"]
        secs = fam_secs(f, n_)
        extra = (TOOLS if f["kind"] == "lk" else "") + f'<p class="t">Lihat juga: {f["see"]}</p>'
        page(path, f"{f['short']} · {r['name']}", f["h1"].format(n=n_), E(f["lead"]), txt, (f"/{k}/{r['pslug']}/", f"{f['short']} {r['prov']}"),
             wilintro(r, f["who"]), secs, f["faq"](r["name"], r["prov"]), f["title"].format(n=n_), rdesc(f, r),
             f"{f['label']} {r['name']}", f["stype"],
             [("FA Indonesia", "/"), (f["label"], f"/{k}/"), (r["prov"], f"/{k}/{r['pslug']}/"), (r["name"], path)], OG[k],
             team=team_for(f["kind"], txt), area=area(r, f["what"]), extra=extra)
        URLS.append(path); n += 1
    CNT[k] = n

# ---------------- 2. akreditasi + BPJS RS untuk kab/kota yang belum ada ----------------
for base, lab, intro2, sec, faq, ogk in (("konsultan-akreditasi-rumah-sakit", "Akreditasi Rumah Sakit", AKR_INTRO, AKR_SEC, AKR_FAQ, "konsultan-akreditasi-rumah-sakit"),
                                         ("konsultan-bpjs-rumah-sakit", "BPJS Rumah Sakit", BPJ_INTRO, BPJ_SEC, BPJ_FAQ, "konsultan-bpjs-rumah-sakit")):
    n = 0
    og = f"/img/og-page/{ogk}.jpg" if os.path.exists(os.path.join(OUT, f"img/og-page/{ogk}.jpg")) else "/img/og-page/konsultan-rumah-sakit.jpg"
    for r in REG:
        if os.path.exists(P(f"/{base}/{r['slug']}/")) and "<!--fanas-page-->" not in rd(P(f"/{base}/{r['slug']}/")): continue
        path = f"/{base}/{r['slug']}/"; nm = r["disp"]
        if base.endswith("akreditasi-rumah-sakit"):
            h1 = f"Akreditasi Rumah Sakit {nm}: Persiapan Survei, Mutu, dan Dampaknya ke Keuangan"
            title = f"Konsultan Akreditasi Rumah Sakit {nm}: Persiapan Survei dan Mutu | FA Indonesia"
            lead = "Pendampingan persiapan akreditasi untuk RS swasta: gap assessment standar, dokumen, telusur, sampai anggaran yang realistis. Kami tidak menjanjikan status; kami memastikan RS siap disurvei."
            desc = f"Konsultan akreditasi rumah sakit di {nm}, {r['prov']}: gap assessment, dokumen regulasi, simulasi telusur, anggaran persiapan, dan dampak ke BPJS dan bank."
            txt = f"Halo FA Indonesia, saya ingin konsultasi persiapan akreditasi rumah sakit di {r['name']}."
        else:
            h1 = f"BPJS Rumah Sakit {nm}: Klaim Pending, Tarif INA-CBG/iDRG, dan Arus Kas"
            title = f"Konsultan BPJS Rumah Sakit {nm}: Klaim Pending, Tarif, Arus Kas | FA Indonesia"
            lead = "Untuk RS swasta yang klaim BPJS-nya sering pending, marginnya tipis, atau sedang menimbang kerja sama baru. Kami membaca data klaim Anda dan mengubahnya jadi keputusan."
            desc = f"Konsultan BPJS rumah sakit di {nm}, {r['prov']}: analisis klaim pending, margin per kasus INA-CBG/iDRG, proyeksi arus kas, dan rencana tindak direksi."
            txt = f"Halo FA Indonesia, saya ingin konsultasi BPJS untuk rumah sakit di {r['name']}."
        secs = []
        for h, body in re.findall(r"<h2>(.*?)</h2>(.*?)(?=<h2>|$)", sec, re.S): secs.append((html.unescape(h), body))
        secs.append(("Pengalaman Memimpin Rumah Sakit", PENGALAMAN.split("</h2>", 1)[1]))
        page(path, f"{lab} · {r['name']}", h1, E(lead), txt, (f"/{base}/{r['pslug']}/", f"{lab} {r['prov']}"),
             wilintro(r, "rumah sakit, RSIA, dan klinik utama") + f"</p><p>{intro2}", secs, faq, title,
             desc, f"Konsultan {lab} {r['name']}", "Hospital consulting",
             [("FA Indonesia", "/"), (lab, f"/{base}/"), (r["prov"], f"/{base}/{r['pslug']}/"), (r["name"], path)], og,
             team=rstim(txt), area=area(r, "konsultan rumah sakit: akreditasi, BPJS, unit cost, dan keuangan"),
             extra='<!--fanas-page--><p class="t">Lihat juga: <a href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a> · <a href="/konsultan-akreditasi-rumah-sakit/">Akreditasi</a> · <a href="/konsultan-bpjs-rumah-sakit/">BPJS</a> · <a href="/konsultan-unit-cost-rumah-sakit/">Unit Cost</a></p>')
        URLS.append(path); n += 1
    CNT[base] = n

# ---------------- 3. pilar layanan baru ----------------
def prov_fold(base, pred=lambda r: True):
    out = []
    for pv in PROVS:
        rs = [r for r in BYPROV[pv] if pred(r)]
        if not rs: continue
        out.append(f'<details class="fold"><summary>{E(pv)} ({len(rs)})</summary><p class="t"><a href="/{base}/{rs[0]["pslug"]}/"><b>Semua wilayah {E(pv)}</b></a> · '
                   + " · ".join(f'<a href="/{base}/{r["slug"]}/">{E(r["name"])}</a>' for r in sorted(rs, key=lambda x: x["name"])) + "</p></details>")
    return "".join(out)

for k, f in F.items():
    if f.get("pillar_exists"): continue
    path = f"/{k}/"; txt = f"Halo FA Indonesia, saya ingin konsultasi {lw(f['short'])}."
    secs = fam_secs(f, "Seluruh Indonesia")
    secs.append((f"{f['short']} per Provinsi", '<p class="t">' + " · ".join(f'<a href="/{k}/provinsi-{sl(pv)}/">{E(pv)}</a>' for pv in PROVS) + "</p>"))
    secs.append((f"{f['short']} di Semua Kabupaten dan Kota", prov_fold(k)))
    page(path, f"Layanan · {f['short']}", f["h1"].format(n="Seluruh Indonesia"),
         E(f["lead"]), txt, ("/konsultan-rumah-sakit/", "Konsultan Rumah Sakit"),
         f"Untuk {f['who']} di seluruh Indonesia, dari ibu kota provinsi sampai kabupaten. Pekerjaan dilakukan daring dengan kunjungan lapangan terjadwal.",
         secs, f["faq"]("seluruh Indonesia", "Indonesia"), f["title"].format(n="Indonesia"), f["desc"].format(n="seluruh Indonesia", p="dari Aceh sampai Papua"),
         f["label"], f["stype"], [("FA Indonesia", "/"), ("Layanan", "/layanan/"), (f["label"], path)], OG[k],
         team=rstim(txt), extra=f'<p class="t">Lihat juga: {f["see"]}</p>')
    URLS.append(path)

# ---------------- 4. halaman provinsi semua layanan wilayah ----------------
PFAM = [(k, f["label"], f["kind"], f["who"], f["what"]) for k, f in F.items()] + OLD
for base, lab, kind, who, what in PFAM:
    ogp = OG.get(base) or (f"/img/og-page/{base}.jpg" if os.path.exists(os.path.join(OUT, f"img/og-page/{base}.jpg")) else "/img/og-page/konsultan-rumah-sakit.jpg")
    sh = SHORT[base]
    for pv in PROVS:
        rs = [r for r in sorted(BYPROV[pv], key=lambda x: x["name"]) if os.path.exists(P(f"/{base}/{r['slug']}/"))]
        if not rs: continue
        path = f"/{base}/provinsi-{sl(pv)}/"
        nk = sum(r["nk"] for r in rs); nd = sum(r["nd"] for r in rs)
        txt = f"Halo FA Indonesia, saya ingin konsultasi {lw(sh)} di {pv}."
        lst = "<ul>" + "".join(f'<li><a href="/{base}/{r["slug"]}/">{E(lab if len(lab) < 40 else sh)} {E(r["disp"])}</a>'
                               + (f' <small>({r["nk"]} kecamatan)</small>' if r["nk"] else "") + "</li>" for r in rs) + "</ul>"
        secs = [(f"{sh} di {len(rs)} Kabupaten dan Kota di {pv}", lst)]
        if base in F: secs.append((f"Layanan {F[base]['short']}", tbl(["Layanan", "Isi"], F[base]["rows"])))
        other = [b for b in HEALTH + FIN if b != base and os.path.exists(P(f"/{b}/"))]
        secs.append((f"Layanan Lain di {pv}", '<p class="t">' + " · ".join(f'<a href="/{b}/provinsi-{sl(pv)}/">{E(SHORT[b])}</a>' for b in other) + "</p>"))
        faq = [(f"Apakah tim FA Indonesia melayani {lw(sh)} di {pv}?", f"Ya. Kami melayani {who} di seluruh {pv}: {len(rs)} kabupaten dan kota, termasuk kecamatan dan desa di dalamnya. Pekerjaan daring dengan kunjungan lapangan terjadwal."),
               ("Bagaimana memulai?", "Hubungi kami lewat tombol WhatsApp di halaman ini. Diskusi awal untuk memetakan kebutuhan, lalu ruang lingkup dan jadwal disepakati.")]
        if kind == "audit": faq.insert(1, ("Siapa auditornya?", "Audit dilakukan KAP DHN & Rekan, kantor akuntan publik mitra yang terdaftar OJK. Penyusun laporan keuangan dan auditor selalu pihak yang berbeda."))
        page(path, f"{sh} · {pv}", f"{lab} di {pv}", f"{what[0].upper() + what[1:]} untuk {E(who)} di seluruh {E(pv)}.", txt, (f"/{base}/", lab),
             f"{E(pv)} terdiri dari {len(rs)} kabupaten dan kota dengan {num(nk)} kecamatan dan {num(nd)} desa/kelurahan. Pilih wilayah Anda di bawah, atau langsung chat tim kami.",
             secs, faq, f"{lab} {pv}: Semua Kabupaten dan Kota | FA Indonesia",
             f"{lab} di {pv}: {', '.join(r['name'] for r in rs[:3])}, dan {max(len(rs) - 3, 0)} kabupaten/kota lain. Diskusi awal lewat WhatsApp.",
             f"{lab} {pv}", "Professional services", [("FA Indonesia", "/"), (lab, f"/{base}/"), (pv, path)], ogp,
             team=rstim(txt) if kind == "rs" else WAJAH)
        URLS.append(path)

# ---------------- 5. laporan keuangan per jenis usaha ----------------
for sk, sn, swho, srows in SECTOR:
    pillar = f"/{sk}/"
    if srows:
        txt = f"Halo FA Indonesia, saya ingin tanya jasa laporan keuangan untuk {lw(sn)}."
        secs = [(f"Yang Kami Kerjakan untuk {sn}", tbl(["Bagian", "Isi"], srows)),
                ("Deliverables yang Anda Terima", tbl(["Deliverable", "Isi", "Waktu"], F["jasa-penyusunan-laporan-keuangan"]["dlv"])),
                (f"Laporan Keuangan {sn} per Provinsi", '<p class="t">' + " · ".join(f'<a href="/{sk}/provinsi-{sl(pv)}/">{E(pv)}</a>' for pv in PROVS) + "</p>")]
        page(pillar, f"Laporan Keuangan · {sn}", f"Jasa Laporan Keuangan {sn}: Pembukuan, Pajak, dan Siap Kredit Bank",
             f"Pembukuan bulanan dan laporan keuangan untuk {E(swho)} di seluruh Indonesia, dikerjakan bersama KJA mitra. Hasilnya siap untuk pajak, audit, dan pengajuan kredit.",
             txt, ("/jasa-penyusunan-laporan-keuangan/", "Penyusunan Laporan Keuangan"),
             f"Setiap jenis usaha punya titik rawan sendiri dalam pembukuan. Untuk {E(swho)}, bagian di bawah ini yang paling sering membuat laporan tidak bisa dipakai untuk bank atau pajak.",
             secs, [(f"Apakah melayani {lw(sn)} di luar kota besar?", "Ya. Dokumen dikirim lewat Google Drive, pertemuan daring, dan kunjungan dijadwalkan bila diperlukan."),
                    ("Berapa biayanya?", "Tergantung jumlah transaksi dan kondisi pembukuan. Paket jasa pembukuan UMKM mulai Rp900 ribu per bulan, PT dan CV mulai Rp2 juta per bulan; perapian beberapa tahun dihitung setelah melihat data."),
                    ("Apakah bisa sekalian diaudit?", "Bisa diarahkan ke KAP mitra yang terdaftar OJK. Penyusun dan auditor selalu pihak yang berbeda.")],
             f"Jasa Laporan Keuangan {sn}: Pembukuan, Pajak, Kredit | FA Indonesia",
             f"Jasa laporan keuangan dan pembukuan untuk {swho} di seluruh Indonesia: pajak, siap audit, siap kredit bank. Diskusi awal lewat WhatsApp.",
             f"Jasa Laporan Keuangan {sn}", "Bookkeeping and financial statement preparation",
             [("FA Indonesia", "/"), ("Penyusunan Laporan Keuangan", "/jasa-penyusunan-laporan-keuangan/"), (sn, pillar)], OG["jasa-penyusunan-laporan-keuangan"],
             team=WAJAH, extra=TOOLS + '<p class="t">Lihat juga: <a href="https://cariakuntan.com/jasa-pembukuan/">Jasa Pembukuan Terima Beres</a> · <a href="/jasa-audit-laporan-keuangan/">Audit Laporan Keuangan</a> · <a href="/konsultan-kredit-bank/">Kredit Bank</a></p>')
        URLS.append(pillar)
    for pv in PROVS:
        rs = sorted(BYPROV[pv], key=lambda x: x["name"])
        path = f"/{sk}/provinsi-{sl(pv)}/"
        txt = f"Halo FA Indonesia, saya ingin tanya jasa laporan keuangan untuk {lw(sn)} di {pv}."
        rows = srows or [("Pembukuan sederhana", "Kas masuk dan keluar, stok, dan utang piutang yang rapi tiap bulan"),
                         ("Laporan keuangan SAK EMKM", "Neraca, laba rugi, dan catatan untuk KUR dan pinjaman"),
                         ("Pajak UMKM", "PPh Final 0,5% dan batas omzet yang berlaku")]
        secs = [(f"Yang Kami Kerjakan untuk {sn}", tbl(["Bagian", "Isi"], rows)),
                (f"Kabupaten dan Kota di {pv}", '<p class="t">' + " · ".join(f'<a href="/jasa-penyusunan-laporan-keuangan/{r["slug"]}/">{E(r["name"])}</a>' for r in rs) + "</p>"),
                ("Jenis Usaha Lain", '<p class="t">' + " · ".join(f'<a href="/{x[0]}/provinsi-{sl(pv)}/">{E(x[1])}</a>' for x in SECTOR if x[0] != sk) + "</p>")]
        page(path, f"Laporan Keuangan {sn} · {pv}", f"Jasa Laporan Keuangan {sn} di {pv}",
             f"Pembukuan dan laporan keuangan untuk {E(swho)} di seluruh {E(pv)}: siap pajak, audit, dan kredit bank.", txt, (pillar, f"Laporan Keuangan {sn}"),
             f"Melayani {len(rs)} kabupaten dan kota di {E(pv)}. Dokumen dikirim lewat Google Drive, pertemuan daring, kunjungan dijadwalkan bila diperlukan.",
             secs, [(f"Ada jasa laporan keuangan {lw(sn)} di {pv}?", f"Ada. Tim FA Indonesia bersama KJA mitra melayani {swho} di seluruh {pv}."),
                    ("Bagaimana memulai?", "Hubungi kami lewat tombol WhatsApp. Kirim gambaran usaha dan pembukuan yang ada, lalu kami usulkan ruang lingkupnya.")],
             f"Laporan Keuangan {sn} {pv}: Pembukuan dan Pajak | FA Indonesia",
             f"Jasa laporan keuangan dan pembukuan {lw(sn)} di {pv}: {', '.join(r['name'] for r in rs[:3])}, dan wilayah lain. Siap pajak, audit, kredit bank.",
             f"Laporan Keuangan {sn} {pv}", "Bookkeeping and financial statement preparation",
             [("FA Indonesia", "/"), (f"Laporan Keuangan {sn}", pillar), (pv, path)], OG["jasa-penyusunan-laporan-keuangan"], team=WAJAH)
        URLS.append(path)


# ---------------- 6. blok silang di semua halaman wilayah ----------------
def insert_before(t, blk, marks):
    for m in marks:
        k = t.find(m)
        if k >= 0: return t[:k] + blk + t[k:]
    return None
SECT_LINKS = lambda pv: " · ".join(f'<a href="/{x[0]}/provinsi-{sl(pv)}/">{E(x[1])}</a>' for x in SECTOR)
nx = 0
for r in REG:
    hs = [b for b in HEALTH if os.path.exists(P(f"/{b}/{r['slug']}/"))]
    fs = [b for b in FIN if os.path.exists(P(f"/{b}/{r['slug']}/"))]
    blk = (f'<!--fanas-x--><section class="fnx"><h2>Layanan Lain di {E(r["disp"])}</h2>'
           f'<p class="t"><b>Rumah sakit dan klinik:</b> ' + " · ".join(f'<a href="/{b}/{r["slug"]}/">{E(SHORT[b])}</a>' for b in hs) + "</p>"
           f'<p class="t"><b>Laporan keuangan dan audit:</b> ' + " · ".join(f'<a href="/{b}/{r["slug"]}/">{E(SHORT[b])}</a>' for b in fs)
           + (f' · <a href="/wilayah/{r["slug"]}/">FA {E(r["name"])}</a>' if os.path.exists(P(f"/wilayah/{r['slug']}/")) else "") + "</p>"
           f'<p class="t"><b>Laporan keuangan per jenis usaha di {E(r["prov"])}:</b> {SECT_LINKS(r["prov"])}</p></section><!--/fanas-x-->')
    for b in hs + fs + ["wilayah"]:
        p = P(f"/{b}/{r['slug']}/")
        if not os.path.exists(p): continue
        t = re.sub(r"<!--fanas-x-->.*?<!--/fanas-x-->", "", rd(p), flags=re.S)
        t2 = insert_before(t, blk, ["<!--fa-rstim-->", "<!--fa-tools-->", "<!--fa-wajah-->", "<h2>Pertanyaan Umum</h2>"])
        if t2: wt(p, t2); nx += 1

# ---------------- 7. hub provinsi di pilar ----------------
nh = 0
for base in [x[0] for x in PFAM] + [x[0] for x in SECTOR if not x[3]]:
    p = P(f"/{base}/")
    if not os.path.exists(p): continue
    t = re.sub(r"<!--fanas-hub-->.*?<!--/fanas-hub-->", "", rd(p), flags=re.S)
    if "provinsi-" in t and base in F and not F[base].get("pillar_exists"): continue   # pilar baru sudah memuat daftar provinsi
    sh = SHORT.get(base, "Laporan Keuangan UMKM")
    blk = (f'<!--fanas-hub--><h2>{E(sh)} per Provinsi</h2><p class="t">' + " · ".join(f'<a href="/{base}/provinsi-{sl(pv)}/">{E(pv)}</a>' for pv in PROVS if os.path.exists(P(f"/{base}/provinsi-{sl(pv)}/"))) + "</p>")
    if base == "jasa-penyusunan-laporan-keuangan":
        blk += ('<h2>Laporan Keuangan per Jenis Usaha</h2><p class="t">' + " · ".join(f'<a href="/{x[0]}/">{E(x[1])}</a>' for x in SECTOR) + "</p>"
                + f"<h2>Penyusunan Laporan Keuangan di Semua Kabupaten dan Kota</h2>" + prov_fold(base))
    blk += "<!--/fanas-hub-->"
    t2 = insert_before(t, blk, ["<!--rsw-hub-->", "<!--fa-rstim-->", "<!--fa-tools-->", "<!--fa-wajah-->", "<h2>Pertanyaan Umum</h2>"])
    if t2 is None:
        k = t.rfind("</div>\n</section>\n</main>")
        if k < 0: print("hub tidak tersisip", base); continue
        t2 = t[:k] + blk + t[k:]
    wt(p, t2); nh += 1

# ---------------- 8. baris link di halaman kecamatan ----------------
nkec = 0
for p in glob.glob(os.path.join(OUT, "wilayah", "*", "kecamatan", "*", "index.html")):
    city = p.split(os.sep)[-4]
    t = re.sub(r"<!--fanas-kec-->.*?<!--/fanas-kec-->", "", rd(p), flags=re.S)
    links = [b for b in ["konsultan-klinik-bpjs", "konsultan-farmasi-rumah-sakit", "konsultan-simrs", "konsultan-akreditasi-rumah-sakit", "konsultan-bpjs-rumah-sakit",
                         "jasa-penyusunan-laporan-keuangan", "jasa-audit-laporan-keuangan"] if os.path.exists(P(f"/{b}/{city}/"))]
    row = '<!--fanas-kec--><p class="t">Layanan lain di wilayah ini: ' + " · ".join(f'<a href="/{b}/{city}/">{E(SHORT[b])}</a>' for b in links) + "</p><!--/fanas-kec-->"
    k = t.find("<!--/rsw-kec-->")
    if k < 0: continue
    k += len("<!--/rsw-kec-->")
    wt(p, t[:k] + row + t[k:]); nkec += 1

# ---------------- 9. sitemap + llms ----------------
smp = os.path.join(OUT, "sitemap.xml")
sm = re.sub(r"<!--fanas-->.*?<!--/fanas-->\n?", "", rd(smp), flags=re.S)
have = set(re.findall(r"<loc>([^<]+)</loc>", sm))
add = "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in dict.fromkeys(URLS) if f"{D}{u}" not in have)
wt(smp, sm.replace("</urlset>", "<!--fanas-->\n" + add + "<!--/fanas-->\n</urlset>"))
llp = os.path.join(OUT, "llms.txt"); ll = re.sub(r"<!--fanas-->.*?<!--/fanas-->\n?", "", rd(llp), flags=re.S)
lines = ("<!--fanas-->\n"
         "- Konsultan Klinik BPJS (kapitasi, KBK, FKTP; per provinsi dan kabupaten/kota) → https://faindonesia.co.id/konsultan-klinik-bpjs/\n"
         "- Optimalisasi Farmasi Rumah Sakit dan Klinik → https://faindonesia.co.id/konsultan-farmasi-rumah-sakit/\n"
         "- Konsultan SIMRS (vendor, RME, SATUSEHAT, bridging BPJS, integrasi akuntansi) → https://faindonesia.co.id/konsultan-simrs/\n"
         "- Penyusunan laporan keuangan per kabupaten/kota dan per jenis usaha (cafe, restoran, klinik, PT/CV, kontraktor, koperasi, yayasan) → https://faindonesia.co.id/jasa-penyusunan-laporan-keuangan/\n"
         "<!--/fanas-->\n")
wt(llp, ll.rstrip("\n") + "\n" + lines)
print("fa_nasional:", CNT, "url", len(set(URLS)), "sitemap+", add.count("<url>"), "silang", nx, "hub", nh, "kecamatan", nkec)
