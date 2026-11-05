# -*- coding: utf-8 -*-
"""SEO BPR (5 Nov 2026, permintaan Bos): audit LK BPR untuk laporan OJK (KAP DHN) dan penyusunan LK BPR (KJA Farhani), seluruh Indonesia.
- /jasa-audit-laporan-keuangan-bpr/ + /jasa-audit-laporan-keuangan-bpr/<provinsi>/ (34)
- /jasa-penyusunan-laporan-keuangan-bpr/ + /jasa-penyusunan-laporan-keuangan-bpr/<provinsi>/ (34)
- Blok "Audit dan Laporan Keuangan BPR" (penanda bpr-wil) di semua halaman /jasa-audit-laporan-keuangan/<wilayah>/.
Dasar aturan (dicek 5 Nov 2026): POJK 48/POJK.03/2017 Pasal 5 (aset >= Rp10 miliar wajib audit AP terdaftar OJK; laporan tahunan paling lambat akhir April),
POJK 23 Tahun 2024 (pelaporan dan transparansi BPR/BPRS), SEOJK 21/SEOJK.03/2024 (panduan akuntansi BPR), POJK 9 Tahun 2023 (penggunaan jasa AP/KAP).
Tanpa janji harga/hasil, tanpa klaim terbaik, kontak lewat tombol WA, tanpa link profil. Idempoten. Jalankan setelah fa_audit_kota_20261105.py, sebelum prep.py."""
import os, re, sys, csv
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-05"')
exec(compile(_src, "fa_lead_helpers", "exec"))
sys.path.insert(0, os.path.join(HERE, "cariakuntan")); sys.path.insert(0, os.path.join(HERE, "shared", "wilayah"))
from cities import CITIES

A = "/jasa-audit-laporan-keuangan-bpr/"; S = "/jasa-penyusunan-laporan-keuangan-bpr/"; AUD = "/jasa-audit-laporan-keuangan/"
W = os.path.join(HERE, "shared", "wilayah")
def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
def _t(x):
    s = " ".join(w.capitalize() for w in x.split())
    return s.replace("Dki ", "DKI ").replace("Di Yogyakarta", "DI Yogyakarta")

PROV = [(r[0], _t(r[1])) for r in csv.reader(open(os.path.join(W, "provinces.csv"), encoding="utf-8"))]
CITY_SLUGS = {slug(c[0]) for c in CITIES}
REG = {}
for code, pc, name in csv.reader(open(os.path.join(W, "regencies.csv"), encoding="utf-8")):
    jenis = "Kota" if name.startswith("KOTA ") else "Kabupaten"; base = _t(name.split(" ", 1)[1]); full = f"{jenis} {base}"
    u = f"{AUD}{slug(base)}/" if slug(base) in CITY_SLUGS else f"{AUD}{slug(full)}/"
    REG.setdefault(pc, []).append((full, u))

RULES = tbl(["Ketentuan", "Isi pokok"], [
    ("POJK 48/POJK.03/2017 Pasal 5", "BPR dengan total aset paling sedikit Rp10 miliar wajib menyampaikan laporan keuangan tahunan yang telah diaudit akuntan publik terdaftar OJK. BPR dengan aset di bawah Rp10 miliar menyampaikan laporan yang telah dipertanggungjawabkan dalam RUPS atau rapat anggota, atau yang diaudit."),
    ("Batas waktu laporan tahunan", "Laporan tahunan BPR disampaikan ke OJK paling lambat akhir April setelah tahun buku berakhir."),
    ("POJK 23 Tahun 2024", "Pelaporan BPR dan BPR Syariah melalui sistem pelaporan OJK serta transparansi kondisi keuangan, termasuk laporan penunjukan akuntan publik."),
    ("POJK 9 Tahun 2023", "Penggunaan jasa akuntan publik dan KAP di sektor jasa keuangan, termasuk pembatasan masa penugasan."),
    ("SEOJK 21/SEOJK.03/2024", "Panduan akuntansi perbankan bagi Bank Perekonomian Rakyat sebagai acuan penyusunan laporan keuangan BPR.")])

def team_bpr(kind):
    rows = [("Audit laporan keuangan BPR", '<a href="/kap-dhn/">KAP DHN &amp; Rekan</a> (KMK No. 592/KM.1/2023, terdaftar OJK)', "Audit laporan keuangan tahunan BPR dan BPR Syariah untuk laporan tahunan ke OJK")]
    if kind == "lk":
        rows.insert(0, ("Penyusunan laporan keuangan BPR", "KJA Farhani K.N. (izin 232/KM.1/PPPK/2020)", "Pembukuan, rekonsiliasi, dan penyusunan laporan keuangan BPR"))
    rows.append(("Kontak dan jadwal", "Tim FA Indonesia lewat WhatsApp", "Diskusi awal, ruang lingkup, jadwal, dan biaya"))
    return ("<h2>Tim yang Menangani</h2>" + tbl(["Peran", "Siapa", "Untuk Apa"], rows)
            + "<p>Untuk satu BPR, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda, sesuai prinsip independensi.</p>")

def regs_block(pc, pv):
    items = sorted(REG.get(pc, []))
    return (f"<h2>Kabupaten dan Kota di {E(pv)}</h2><p>" + ", ".join(f'<a href="{u}">{E(n)}</a>' for n, u in items) + "</p>")

def post(path):
    fp = P(*path.strip("/").split("/"), "index.html"); t = open(fp, encoding="utf-8").read()
    open(fp, "w", encoding="utf-8").write(t.replace(AUTHOR_BOX, "").replace("Chat Ananta, CPA", "Chat WhatsApp"))

FAQ_A = [("Apakah semua BPR wajib diaudit?", "BPR dengan total aset paling sedikit Rp10 miliar wajib menyampaikan laporan keuangan tahunan yang diaudit akuntan publik terdaftar OJK. BPR dengan aset di bawah itu boleh menyampaikan laporan yang dipertanggungjawabkan dalam RUPS, atau tetap memilih diaudit."),
         ("Kapan audit BPR sebaiknya dimulai?", "Laporan tahunan disampaikan paling lambat akhir April, jadi penunjukan KAP dan perencanaan audit idealnya dilakukan sebelum atau segera setelah tutup buku Desember."),
         ("Apakah BPR Syariah juga bisa?", "Bisa. Ruang lingkup audit BPR Syariah dibahas di awal sesuai ketentuan yang berlaku bagi BPR Syariah."),
         ("Bagaimana cara memulai?", "Hubungi kami lewat tombol WhatsApp. Kami minta laporan keuangan terakhir dan laporan publikasi untuk menyusun ruang lingkup dan jadwal.")]
FAQ_S = [("Apakah laporan keuangan BPR bisa disusun pihak luar?", "Bisa. Penyusunan atau pembenahan laporan keuangan dikerjakan KJA, sedangkan audit dilakukan KAP yang berbeda, sehingga independensi tetap terjaga."),
         ("Acuan apa yang dipakai?", "Standar akuntansi yang berlaku bagi BPR dan panduan akuntansi perbankan BPR dari OJK (SEOJK 21/SEOJK.03/2024)."),
         ("Apakah termasuk laporan keuangan publikasi?", "Kami membantu menyiapkan angka dan rekonsiliasi yang dibutuhkan untuk laporan tahunan dan laporan keuangan publikasi. Penyampaian ke OJK tetap dilakukan oleh BPR."),
         ("Bisa dikerjakan jarak jauh?", "Bisa. Data dikirim lewat file, lalu pertanyaan dan konfirmasi dilakukan online, sehingga BPR di seluruh Indonesia bisa dilayani.")]

def build():
    urls = []
    # Halaman nasional
    svc_page(A, "Layanan · Audit BPR", "Jasa Audit Laporan Keuangan BPR dan BPR Syariah untuk Laporan Tahunan OJK",
             "Audit laporan keuangan tahunan Bank Perekonomian Rakyat (BPR) dan BPR Syariah di seluruh Indonesia oleh KAP DHN &amp; Rekan yang terdaftar OJK, untuk memenuhi laporan tahunan ke OJK.",
             "<h2>Kenapa BPR Perlu Audit</h2>" + RULES
             + "<h2>Alur Audit BPR</h2>" + flow([("Diskusi awal", "Ruang lingkup, jadwal, dan dokumen awal."), ("Penunjukan KAP", "Perjanjian kerja dan laporan penunjukan akuntan publik ke OJK."), ("Pekerjaan lapangan", "Kredit, CKPN dan PPKA, AYDA, dana pihak ketiga, dan pendapatan bunga."), ("Laporan auditor", "Opini, surat komentar (management letter), dan laporan untuk OJK.")])
             + team_bpr("audit") + '<p>Butuh penyusunan laporan keuangan dulu? Lihat <a href="' + S + '">jasa penyusunan laporan keuangan BPR</a>.</p>'
             + "<h2>Audit BPR per Provinsi</h2><p>" + ", ".join(f'<a href="{A}{slug(pv)}/">{E(pv)}</a>' for _, pv in PROV) + "</p>",
             FAQ_A, "Jasa Audit Laporan Keuangan BPR untuk OJK | KAP Terdaftar OJK | FA Indonesia",
             "Audit laporan keuangan BPR dan BPR Syariah untuk laporan tahunan OJK, oleh KAP terdaftar OJK. Seluruh Indonesia. Konsultasi lewat WhatsApp.",
             "Jasa Audit Laporan Keuangan BPR", "Bank audit", AUD, "Semua Layanan Audit",
             "Halo FA Indonesia, kami dari BPR dan ingin tanya audit laporan keuangan untuk laporan OJK.", "Audit BPR")
    post(A); urls.append(D + A)
    svc_page(S, "Layanan · Laporan Keuangan BPR", "Jasa Penyusunan Laporan Keuangan BPR dan BPR Syariah di Seluruh Indonesia",
             "Pembukuan, rekonsiliasi, dan penyusunan laporan keuangan Bank Perekonomian Rakyat (BPR) dan BPR Syariah oleh KJA Farhani K.N., mengacu pada panduan akuntansi BPR dari OJK, siap untuk audit dan laporan tahunan.",
             "<h2>Yang Kami Kerjakan</h2>" + tbl(["Pekerjaan", "Isi"], [
                ("Rekonsiliasi dan pembenahan", "Kredit, CKPN dan PPKA, AYDA, tabungan dan deposito, antarbank, aset tetap."),
                ("Laporan keuangan tahunan", "Laporan posisi keuangan, laba rugi, perubahan ekuitas, arus kas, dan catatan atas laporan keuangan."),
                ("Dukungan laporan tahunan dan publikasi", "Angka dan rekonsiliasi untuk laporan tahunan dan laporan keuangan publikasi ke OJK."),
                ("Persiapan audit", "Kertas kerja pendukung supaya audit oleh KAP berjalan tanpa tertunda.")])
             + "<h2>Ketentuan yang Relevan</h2>" + RULES + team_bpr("lk")
             + '<p>Untuk audit, lihat <a href="' + A + '">jasa audit laporan keuangan BPR</a>.</p>'
             + "<h2>Penyusunan Laporan Keuangan BPR per Provinsi</h2><p>" + ", ".join(f'<a href="{S}{slug(pv)}/">{E(pv)}</a>' for _, pv in PROV) + "</p>",
             FAQ_S, "Jasa Penyusunan Laporan Keuangan BPR | KJA Berizin | FA Indonesia",
             "Penyusunan laporan keuangan BPR dan BPR Syariah oleh KJA berizin, mengacu panduan akuntansi BPR OJK, siap audit. Seluruh Indonesia. Konsultasi WhatsApp.",
             "Jasa Penyusunan Laporan Keuangan BPR", "Bank financial reporting", A, "Audit BPR",
             "Halo FA Indonesia, kami dari BPR dan ingin tanya jasa penyusunan laporan keuangan.", "Laporan Keuangan BPR")
    post(S); urls.append(D + S)
    # Per provinsi
    for pc, pv in PROV:
        n = len(REG.get(pc, []))
        pa = f"{A}{slug(pv)}/"
        svc_page(pa, f"Audit BPR · {E(pv)}", f"Jasa Audit Laporan Keuangan BPR di {pv}",
                 f"Audit laporan keuangan tahunan BPR dan BPR Syariah di {E(pv)} ({n} kabupaten dan kota) untuk laporan tahunan ke OJK, oleh KAP DHN &amp; Rekan yang terdaftar OJK. Pekerjaan bisa dilakukan jarak jauh dan di lokasi.",
                 "<h2>Ketentuan Audit BPR</h2>" + RULES + team_bpr("audit") + regs_block(pc, pv)
                 + f'<p>Lihat juga <a href="{S}{slug(pv)}/">penyusunan laporan keuangan BPR di {E(pv)}</a> dan <a href="{A}">audit BPR seluruh Indonesia</a>.</p>',
                 FAQ_A, f"Jasa Audit Laporan Keuangan BPR {pv} | Laporan OJK | FA Indonesia",
                 f"Audit laporan keuangan BPR dan BPR Syariah di {pv} untuk laporan tahunan OJK, oleh KAP terdaftar OJK. Konsultasi lewat WhatsApp."[:160],
                 f"Jasa Audit Laporan Keuangan BPR {pv}", "Bank audit", A, "Audit BPR Indonesia",
                 f"Halo FA Indonesia, kami BPR di {pv} dan ingin tanya audit laporan keuangan untuk OJK.", f"Audit BPR {pv}")
        post(pa); urls.append(D + pa)
        ps = f"{S}{slug(pv)}/"
        svc_page(ps, f"Laporan Keuangan BPR · {E(pv)}", f"Jasa Penyusunan Laporan Keuangan BPR di {pv}",
                 f"Pembukuan, rekonsiliasi, dan penyusunan laporan keuangan BPR dan BPR Syariah di {E(pv)} oleh KJA Farhani K.N., siap untuk audit dan laporan tahunan ke OJK.",
                 "<h2>Ketentuan yang Relevan</h2>" + RULES + team_bpr("lk") + regs_block(pc, pv)
                 + f'<p>Lihat juga <a href="{pa}">audit laporan keuangan BPR di {E(pv)}</a>.</p>',
                 FAQ_S, f"Jasa Penyusunan Laporan Keuangan BPR {pv} | FA Indonesia",
                 f"Penyusunan laporan keuangan BPR dan BPR Syariah di {pv} oleh KJA berizin, siap audit dan laporan OJK. Konsultasi lewat WhatsApp."[:160],
                 f"Jasa Penyusunan Laporan Keuangan BPR {pv}", "Bank financial reporting", ps.replace(S, A), "Audit BPR",
                 f"Halo FA Indonesia, kami BPR di {pv} dan ingin tanya jasa penyusunan laporan keuangan.", f"LK BPR {pv}")
        post(ps); urls.append(D + ps)
    return urls

def link_regions():
    # Blok BPR di semua halaman audit wilayah, link ke halaman BPR provinsinya
    pv_by_slug = {slug(pv): pv for _, pv in PROV}
    reg_prov = {}
    for pc, items in REG.items():
        pv = dict(PROV).get(pc, "")
        for full, u in items: reg_prov.setdefault(u, pv)
    for c in CITIES: reg_prov[f"{AUD}{slug(c[0])}/"] = pv_by_slug.get(slug(c[1]), reg_prov.get(f"{AUD}{slug(c[0])}/", ""))
    root = P("jasa-audit-laporan-keuangan"); n = 0
    for d in os.listdir(root):
        fp = os.path.join(root, d, "index.html")
        if not os.path.isfile(fp): continue
        u = f"{AUD}{d}/"; pv = reg_prov.get(u, "")
        t = open(fp, encoding="utf-8").read(); t = re.sub(r"<!--bpr-wil-->.*?<!--/bpr-wil-->", "", t, flags=re.S)
        nm = re.search(r"<h1[^>]*>Jasa Audit Laporan Keuangan di ([^<:,]+)", t); nm = nm.group(1).strip() if nm else d.replace("-", " ").title()
        la = f"{A}{slug(pv)}/" if pv else A; ls = f"{S}{slug(pv)}/" if pv else S
        blk = (f'<!--bpr-wil--><h2>Audit dan Laporan Keuangan BPR di {E(nm)}</h2><p>BPR dan BPR Syariah di {E(nm)} dengan total aset paling sedikit Rp10 miliar wajib menyampaikan laporan keuangan tahunan yang diaudit akuntan publik terdaftar OJK. '
               f'Lihat <a href="{la}">jasa audit laporan keuangan BPR</a> dan <a href="{ls}">jasa penyusunan laporan keuangan BPR</a>.</p><!--/bpr-wil-->')
        k = t.find("<h2>Pertanyaan Umum</h2>")
        if k > 0: t = t[:k] + blk + t[k:]; n += 1
        open(fp, "w", encoding="utf-8").write(t)
    # Link dari halaman induk audit
    pp = P("jasa-audit-laporan-keuangan", "index.html"); t = open(pp, encoding="utf-8").read()
    t = re.sub(r"<!--bpr-hub-->.*?<!--/bpr-hub-->", "", t, flags=re.S)
    k = t.find("<!--audit-wil-->")
    if k > 0: t = t[:k] + f'<!--bpr-hub--><h2>Audit dan Laporan Keuangan BPR</h2><p><a href="{A}">Jasa audit laporan keuangan BPR untuk OJK</a> dan <a href="{S}">jasa penyusunan laporan keuangan BPR</a> untuk BPR dan BPR Syariah di seluruh Indonesia.</p><!--/bpr-hub-->' + t[k:]
    open(pp, "w", encoding="utf-8").write(t)
    return n

def sitemap(urls):
    sp = P("sitemap.xml"); s = open(sp, encoding="utf-8").read()
    add = "".join(f"<url><loc>{u}</loc><lastmod>2026-11-05</lastmod></url>" for u in urls if f"<loc>{u}</loc>" not in s)
    if add: open(sp, "w", encoding="utf-8").write(s.replace("</urlset>", add + "</urlset>"))

if __name__ == "__main__":
    u = build(); print("halaman BPR:", len(u)); print("blok BPR di halaman wilayah:", link_regions()); sitemap(u)
