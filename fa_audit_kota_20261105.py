# -*- coding: utf-8 -*-
"""Tier 1 SEO audit per kota (5 Nov 2026, disetujui Bos: struktur bertingkat).
/jasa-audit-laporan-keuangan/<kota>/ untuk 113 kota yang sudah punya halaman /wilayah/<kota>/.
Isi per kota: sektor usaha dominan (SECTOR_LINES), kebutuhan audit, FAQ kota, tim audit KAP DHN.
Aturan konten (Bos, 5 Nov 2026): tanpa janji harga/hasil, tanpa klaim terbaik,
tim audit tampil sebagai tim KAP DHN, kontak lewat tombol WA. Tanpa link profil KAP DHN.
Idempoten. Jalankan setelah fa_kec_20261102.py dan sebelum prep.py."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-05"')
exec(compile(_src, "fa_lead_helpers", "exec"))
sys.path.insert(0, os.path.join(HERE, "cariakuntan")); sys.path.insert(0, os.path.join(HERE, "shared", "wilayah"))
from cities import CITIES, SECTOR_LINES

PARENT = "/jasa-audit-laporan-keuangan/"
def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

def team_audit(kota):
    return ('<h2>Tim Audit untuk ' + E(kota) + '</h2>'
            + tbl(["Peran", "Siapa", "Untuk Apa"], [
                ("Audit laporan keuangan", '<a href="/kap-dhn/">KAP DHN &amp; Rekan</a> (KMK No. 592/KM.1/2023, terdaftar OJK)', "Audit umum, audit untuk kredit bank, dan laporan tahunan PT"),
                ("Kontak dan jadwal", "Tim FA Indonesia lewat WhatsApp", "Diskusi awal, ruang lingkup, jadwal, dan biaya")])
            + '<p>Penyusunan laporan keuangan dan audit dilakukan oleh pihak yang berbeda, sesuai prinsip independensi. Hubungi kami lewat tombol WhatsApp di halaman ini.</p>')

def body_for(kota, prov, note, sectors):
    rows = [(SECTOR_LINES.get(s, s).split(":")[0], SECTOR_LINES.get(s, s).split(":", 1)[-1].strip()) for s in sectors]
    return ("<h2>Kebutuhan Audit di " + E(kota) + "</h2>"
            f"<p>{E(kota)} di {E(prov)} adalah {E(note)}. Perusahaan dan badan usaha di kota ini biasanya butuh audit laporan keuangan karena tiga alasan: "
            "permintaan bank untuk kredit, kewajiban laporan tahunan PT, dan persiapan investor atau mitra usaha.</p>"
            "<h2>Sektor Usaha yang Sering Kami Tangani</h2>"
            + tbl(["Sektor", "Fokus audit"], rows)
            + "<h2>Yang Perlu Disiapkan Sebelum Audit</h2>"
            "<p>Laporan keuangan tahunan, buku besar, rekening koran, daftar aset tetap, rincian piutang dan utang, serta akta dan izin usaha. "
            "Tim kami membantu memeriksa kelengkapannya sebelum lapangan dimulai, supaya proses audit tidak tertunda.</p>")

def faq_for(kota, prov):
    return [
        (f"Apakah bisa audit laporan keuangan perusahaan di {kota}?",
         f"Bisa. Ruang lingkup, lokasi kerja, dan jadwal dibahas di awal. Perusahaan di {kota} dan {prov} bisa diaudit oleh KAP DHN &amp; Rekan."),
        (f"Berapa lama proses audit untuk perusahaan di {kota}?",
         "Lamanya tergantung kompleksitas usaha, kelengkapan dokumen, dan jumlah entitas. Waktu pastinya disepakati setelah kami melihat data awal."),
        ("Apakah bisa dibantu persiapan laporan keuangan sebelum audit?",
         "Bisa. Penyusunan atau pembenahan laporan keuangan dikerjakan oleh tim penyusun yang terpisah dari auditor, lalu audit dilakukan oleh KAP."),
    ]

def build():
    n = 0
    for kota, prov, region, sectors, note in CITIES:
        s = slug(kota); path = f"{PARENT}{s}/"
        h1 = f"Jasa Audit Laporan Keuangan di {kota}: Audit oleh KAP Terdaftar OJK"
        lead = (f"Audit laporan keuangan untuk perusahaan, yayasan, dan badan usaha di {kota}, {prov}. "
                "Auditor berasal dari KAP DHN &amp; Rekan yang terdaftar OJK, dengan ruang lingkup dan jadwal yang disepakati di awal.")
        body = body_for(kota, prov, note, sectors) + team_audit(kota)
        faq = faq_for(kota, prov)
        title = f"Jasa Audit Laporan Keuangan {kota} | KAP Terdaftar OJK | FA Indonesia"
        desc = f"Audit laporan keuangan di {kota}, {prov}: audit kredit bank, laporan tahunan PT, dan persiapan investor. KAP terdaftar OJK. Konsultasi awal lewat WhatsApp."
        wa_msg = f"Halo FA Indonesia, saya di {kota} dan ingin tanya jasa audit laporan keuangan."
        svc_page(path, f"Audit · {kota}", h1, lead, body, faq, title, desc,
                 f"Jasa Audit Laporan Keuangan {kota}", "Jasa Audit", PARENT, "Semua Layanan Audit",
                 wa_msg, f"Audit {kota}")
        # Pasca-proses: tanpa kotak profil penulis dan tanpa label nama+CPA di tombol (permintaan Bos)
        fp = P(*path.strip("/").split("/"), "index.html")
        t = open(fp, encoding="utf-8").read()
        t = t.replace(AUTHOR_BOX, "").replace("Chat Ananta, CPA", "Chat WhatsApp")
        open(fp, "w", encoding="utf-8").write(t)
        n += 1
    return n

def update_sitemap():
    p = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58", "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    urls = [f"{D}{PARENT}{slug(c[0])}/" for c in CITIES]
    add = "".join(f"<url><loc>{u}</loc><lastmod>2026-11-05</lastmod></url>" for u in urls if u not in s)
    if add:
        s = s.replace("</urlset>", add + "</urlset>")
        open(p, "w", encoding="utf-8").write(s)
    return len(urls)

if __name__ == "__main__":
    print("halaman dibuat:", build())
    print("sitemap cek:", update_sitemap())

# ================= TIER 1b: SEMUA 514 KABUPATEN/KOTA (5 Nov 2026 sore) =================
# Halaman /jasa-audit-laporan-keuangan/<kabupaten-x|kota-x>/ untuk kabupaten/kota yang belum ada di 113 kota.
# Isi unik: daftar kecamatan (BPS/Kemendagri) + jumlah desa/kelurahan per kecamatan.
import csv
def _t(x): return " ".join(w.capitalize() for w in x.split())
def build_regencies():
    W = os.path.join(HERE, "shared", "wilayah")
    prov = {r[0]: _t(r[1]) for r in csv.reader(open(os.path.join(W, "provinces.csv"), encoding="utf-8"))}
    kec = {}
    for r in csv.reader(open(os.path.join(W, "districts.csv"), encoding="utf-8")): kec.setdefault(r[1], []).append((r[0], _t(r[2])))
    nv = {}
    for r in csv.reader(open(os.path.join(W, "villages.csv"), encoding="utf-8")): nv[r[1]] = nv.get(r[1], 0) + 1
    have = {slug(c[0]) for c in CITIES}
    out = []
    for code, pc, name in csv.reader(open(os.path.join(W, "regencies.csv"), encoding="utf-8")):
        jenis = "Kota" if name.startswith("KOTA ") else "Kabupaten"
        base = _t(name.split(" ", 1)[1]); full = f"{jenis} {base}"
        if slug(base) in have: continue
        s = slug(full); path = f"{PARENT}{s}/"; pv = prov.get(pc, "")
        ks = sorted(kec.get(code, []), key=lambda x: x[1]); nd = sum(nv.get(k[0], 0) for k in ks)
        rows = [(E(k[1]), str(nv.get(k[0], 0))) for k in ks]
        body = ("<h2>Kebutuhan Audit di " + E(full) + "</h2>"
                f"<p>{E(full)}, {E(pv)}, terdiri dari {len(ks)} kecamatan dan {nd} desa/kelurahan. Perusahaan, koperasi, yayasan, BUMDes, dan badan usaha di wilayah ini "
                "biasanya butuh audit laporan keuangan untuk kredit bank, laporan tahunan PT, pertanggungjawaban dana, atau persiapan investor.</p>"
                "<h2>Area Layanan: Kecamatan di " + E(full) + "</h2>"
                + tbl(["Kecamatan", "Jumlah desa/kelurahan"], rows)
                + "<h2>Yang Perlu Disiapkan Sebelum Audit</h2>"
                "<p>Laporan keuangan tahunan, buku besar, rekening koran, daftar aset tetap, rincian piutang dan utang, serta akta dan izin usaha. "
                "Tim kami membantu memeriksa kelengkapannya sebelum audit dimulai, dan pekerjaan bisa dilakukan jarak jauh untuk wilayah di luar kota besar.</p>"
                + team_audit(full))
        faq = faq_for(full, pv)
        kk = ", ".join(k[1] for k in ks[:3])
        title = f"Jasa Audit Laporan Keuangan {full} | KAP Terdaftar OJK | FA Indonesia"
        desc = f"Audit laporan keuangan di {full}, {pv}: {kk}, dan kecamatan lain. Audit kredit bank, laporan tahunan PT, koperasi. Konsultasi lewat WhatsApp."[:160]
        svc_page(path, f"Audit · {full}", f"Jasa Audit Laporan Keuangan di {full}, {pv}",
                 f"Audit laporan keuangan untuk perusahaan, koperasi, yayasan, dan badan usaha di {E(full)} dan seluruh kecamatannya. Auditor dari KAP DHN &amp; Rekan yang terdaftar OJK.",
                 body, faq, title, desc, f"Jasa Audit Laporan Keuangan {full}", "Jasa Audit", PARENT, "Semua Layanan Audit",
                 f"Halo FA Indonesia, saya di {full} dan ingin tanya jasa audit laporan keuangan.", f"Audit {full}")
        fp = P(*path.strip("/").split("/"), "index.html"); t = open(fp, encoding="utf-8").read()
        open(fp, "w", encoding="utf-8").write(t.replace(AUTHOR_BOX, "").replace("Chat Ananta, CPA", "Chat WhatsApp"))
        out.append(f"{D}{path}")
    return out

def hub_and_sitemap(urls_all):
    # Daftar semua wilayah di halaman induk (link terlipat rapi dalam <details> per huruf)
    pp = P("jasa-audit-laporan-keuangan", "index.html"); t = open(pp, encoding="utf-8").read()
    t = re.sub(r"<!--audit-wil-->.*?<!--/audit-wil-->", "", t, flags=re.S)
    items = sorted(((u.rstrip("/").rsplit("/", 1)[1].replace("-", " ").title(), u.replace(D, "")) for u in urls_all))
    groups = {}
    for nm, u in items: groups.setdefault(nm[0], []).append((nm, u))
    blk = ('<!--audit-wil--><h2>Jasa Audit di Seluruh Kabupaten dan Kota</h2>'
           + "".join(f'<details><summary>{g} ({len(v)})</summary><p>' + ", ".join(f'<a href="{u}">{E(n)}</a>' for n, u in v) + '</p></details>' for g, v in sorted(groups.items()))
           + '<!--/audit-wil-->')
    k = t.find("<h2>Pertanyaan Umum</h2>")
    if k > 0: t = t[:k] + blk + t[k:]
    open(pp, "w", encoding="utf-8").write(t)
    sp = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58", "sitemap.xml"); s = open(sp, encoding="utf-8").read()
    add = "".join(f"<url><loc>{u}</loc><lastmod>2026-11-05</lastmod></url>" for u in urls_all if u not in s)
    if add: open(sp, "w", encoding="utf-8").write(s.replace("</urlset>", add + "</urlset>"))

if __name__ == "__main__":
    r = build_regencies(); print("kabupaten/kota tambahan:", len(r))
    hub_and_sitemap([f"{D}{PARENT}{slug(c[0])}/" for c in CITIES] + r)
