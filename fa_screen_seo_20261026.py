# -*- coding: utf-8 -*-
"""Internal link ke alat screening (26 Okt 2026).
- CariAkuntan: kotak CTA /screening/ di semua halaman ID (kota, kawasan, layanan, artikel).
- FA: kotak CTA Cek Kredit & Pendanaan di semua halaman /wilayah/ dan /artikel/ yang belum punya.
Idempoten (penanda ca-scr / fa-kk-all). Jalankan setelah cariakuntan/build.py, sebelum prep.py."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
CA = os.path.join(HERE, "cariakuntan", "site")
FA = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")

def nice(slug): return " ".join(w.capitalize() for w in slug.split("-"))

n = 0
for root, dirs, files in os.walk(CA):
    rel = os.path.relpath(root, CA)
    if rel == "." or rel.split(os.sep)[0] in ("en", "zh", "hokkien", "screening"): continue
    if "index.html" not in files: continue
    p = os.path.join(root, "index.html"); s = open(p, encoding="utf-8").read()
    s = re.sub(r"<!--ca-scr-->.*?<!--/ca-scr-->", "", s, flags=re.S)
    parts = rel.split(os.sep)
    where = f" di {nice(parts[-1] if len(parts) > 2 and parts[0] == 'kota' else parts[1])}" if parts[0] == "kota" and len(parts) > 1 else ""
    box = ('<!--ca-scr--><div style="margin:30px 0 8px;padding:20px 22px;border:1px solid var(--line);background:var(--panel)">'
           f'<p style="margin:0 0 6px;font-weight:600">Screening Instan Gratis untuk Perusahaan{where}</p>'
           '<p style="margin:0 0 12px">Isi angka ringkas 3 tahun, lihat langsung rasio kredit bank dan jalur IPO BEI sebelum memilih KAP atau mengajukan kredit.</p>'
           '<a class="btn btn-wa arrow" href="/screening/">Mulai Screening</a>'
           + (f' <a class="btn btn-line" href="/kota/{parts[1]}/kap-murah/">KAP Murah di {nice(parts[1])}: Bijak atau Tidak?</a>' if parts[0] == "kota" and len(parts) > 1 and parts[-1] != "kap-murah" else "")
           + '</div><!--/ca-scr-->')
    k = s.rfind("</main>")
    if k < 0: continue
    s = s[:k] + box + s[k:]; open(p, "w", encoding="utf-8").write(s); n += 1
print("CA pages:", n)

m = 0
for sub in ("wilayah", "artikel"):
    for root, dirs, files in os.walk(os.path.join(FA, sub)):
        if "index.html" not in files: continue
        p = os.path.join(root, "index.html"); s = open(p, encoding="utf-8").read()
        s = re.sub(r"<!--fa-kk-all-->.*?<!--/fa-kk-all-->", "", s, flags=re.S)
        if root.rstrip(os.sep).endswith(os.sep + "artikel") or "cek-kapasitas-kredit" in s:
            open(p, "w", encoding="utf-8").write(s); continue
        rel = os.path.relpath(root, os.path.join(FA, sub)).split(os.sep)
        where = f" di {nice(rel[-1])}" if sub == "wilayah" else ""
        box = ('<!--fa-kk-all--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
               f'<p style="margin:0 0 6px;font-weight:600">Cek Kredit dan Pendanaan Gratis untuk Perusahaan{where}</p>'
               '<p style="margin:0 0 12px">Hitung DSCR, plafon kredit per suku bunga dan tenor, serta jalur IPO BEI dalam 3 menit.</p>'
               '<a class="btn solid" href="/cek-kapasitas-kredit/">Mulai Hitung</a>'
               + (f' <a class="btn line" href="https://cariakuntan.com/kota/{rel[0]}/kap-murah/">Cari KAP Murah di {nice(rel[0])}</a>' if sub == "wilayah" else ' <a class="btn line" href="/artikel/kap-murah-apakah-bijak/">KAP Murah, Apakah Bijak?</a>')
               + '</div><!--/fa-kk-all-->')
        k = s.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
        if k < 0: k = s.rfind("</main>")
        if k < 0: continue
        s = s[:k] + box + s[k:]; open(p, "w", encoding="utf-8").write(s); m += 1
print("FA pages:", m)

# ---------- FA artikel: KAP murah, apakah bijak (mengarah ke CariAkuntan) ----------
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
exec(_src[:_src.index("# ================= 1.")])
import importlib.util, sys as _sys, json as _json
_sys.path.insert(0, os.path.join(HERE, "cariakuntan"))
_spec = importlib.util.spec_from_file_location("cities", os.path.join(HERE, "cariakuntan", "cities.py")); _c = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_c)
CITIES = [c[0] for c in _c.CITIES]
def _sl(t): return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
TOP = ["Malang","Surabaya","Batam","Jakarta","Sidoarjo","Bandung","Semarang","Yogyakarta","Medan","Makassar","Denpasar","Jember","Pasuruan","Balikpapan","Pekanbaru","Palembang","Tangerang","Bekasi"]
AP = "/artikel/kap-murah-apakah-bijak/"
body = ("<h2>Murah karena Efisien, atau karena Prosedur Dipangkas?</h2><p>Mencari KAP murah itu wajar, apalagi bagi perusahaan yang baru pertama kali diaudit. Biaya audit bisa ditekan dengan cara yang sehat: laporan keuangan rapi sebelum auditor datang, lingkup penugasan yang tepat, kelas KAP sesuai yang diminta bank, dan jadwal di luar musim puncak. Yang berisiko adalah fee yang terlalu rendah sampai prosedur audit dikurangi. Laporannya bisa ditolak bank atau investor, lalu Anda membayar audit kedua.</p>"
        "<h2>Independen dan Dapat Dipercaya</h2><ul><li>KAP dan akuntan publiknya berizin Kementerian Keuangan, dan terdaftar OJK bila laporan untuk lembaga jasa keuangan atau emiten.</li>"
        "<li>Masuk daftar rekanan bank atau pihak yang meminta laporan.</li><li>Auditor tidak sekaligus menyusun laporan keuangan yang diauditnya.</li>"
        "<li>Fee masuk akal. Kode Etik Profesi Akuntan Publik memandang imbalan jasa yang terlalu rendah sebagai ancaman terhadap kompetensi dan kecermatan profesional.</li>"
        "<li>Tidak sedang dikenai sanksi dan berpengalaman di industri Anda.</li></ul>"
        "<h2>Diskusikan Dulu Kebutuhannya</h2><p>Untuk memilih KAP yang sesuai kebutuhan dan anggaran, diskusikan dulu di <a href=\"https://cariakuntan.com/kap-murah/\">cariakuntan.com</a>. Kebutuhan audit dipetakan dulu: untuk bank mana, plafon berapa, wajib audit, tender, atau investor. Setelah itu baru dibandingkan beberapa KAP berizin.</p>"
        "<h2>KAP Murah per Kota</h2><p>" + " · ".join(f'<a href="https://cariakuntan.com/kota/{_sl(c)}/kap-murah/">KAP Murah {c}</a>' for c in TOP if c in CITIES) + " · <a href=\"https://cariakuntan.com/kap-murah/\">Semua Kota</a></p>"
        "<h2>Supaya Biaya Audit Lebih Ringan</h2><p>Rapikan dulu laporan keuangan lewat <a href=\"/jasa-penyusunan-laporan-keuangan/\">jasa penyusunan laporan keuangan</a>, lalu cek posisi rasio Anda di <a href=\"/cek-kapasitas-kredit/\">Cek Kredit dan Pendanaan</a>.</p>")
FAQX = [("Apakah bijak memilih KAP murah?", "Bijak bila murahnya karena efisien: data rapi, lingkup tepat, kelas KAP sesuai kebutuhan. Tidak bijak bila murahnya karena prosedur dipangkas, karena laporan bisa ditolak dan harus diaudit ulang."),
        ("Bagaimana memastikan KAP independen?", "Pastikan auditor tidak menyusun laporan keuangan yang diauditnya, tidak punya kepentingan keuangan atau hubungan keluarga dengan perusahaan, dan menerapkan Kode Etik Profesi Akuntan Publik."),
        ("Di mana mencari KAP yang biayanya wajar?", "Diskusikan kebutuhan Anda di cariakuntan.com. Kami bantu memetakan lingkup dan kelas KAP yang diperlukan, lalu membandingkan beberapa KAP berizin.")]
svc_page(AP, "Eksplor · Audit", "KAP Murah: Apakah Bijak, Independen, dan Dapat Dipercaya?",
 "Cara menilai kantor akuntan publik yang biayanya hemat tetapi tetap independen dan diterima bank, investor, atau regulator.",
 body, FAQX, "KAP Murah: Apakah Bijak, Independen, dan Dipercaya Bank? | FA Indonesia",
 "Mencari KAP murah? Cara menilai independensi dan kredibilitas kantor akuntan publik, kapan hemat masih bijak, dan diskusi kebutuhan audit di cariakuntan.com.",
 "Panduan Memilih Kantor Akuntan Publik", "Auditor selection guidance", "https://cariakuntan.com/kap-murah/", "KAP Murah per Kota", "Halo FA Indonesia, kami ingin diskusi memilih KAP yang biayanya wajar.", "KAP Murah")
sm = re.sub(r"<!--fa-kapm-->.*?<!--/fa-kapm-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", f"<!--fa-kapm-->\n<url><loc>{D}{AP}</loc><lastmod>{TODAY}</lastmod><priority>0.7</priority></url>\n<!--/fa-kapm-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
print("FA artikel KAP murah ok")
