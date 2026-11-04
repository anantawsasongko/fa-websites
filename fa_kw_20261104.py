# -*- coding: utf-8 -*-
"""4 Nov 2026: optimasi keyword dari data lead + GSC 28 hari.
Lead SEO (6): 3 dari /wilayah/<kota>/ (Purwokerto, Sukabumi, Labuan Bajo), 2 dari halaman jasa (/laporan-keuangan-umkm/, /layanan/),
1 tombol WA umum (kredit bank). 0 lead dari CariAkuntan dan UpdateSAK.
Query GSC yang dicari orang: "kap <kota>", "kantor akuntan publik <kota>", "kjpp <kota>", "konsultan pajak <kota>", "audit <kota>",
"akuntan publik terdekat", "accountant near me", "konsultan keuangan terdekat/terbaik", "konsultan manajemen keuangan" (posisi 62),
"jasa pembuatan laporan keuangan bulanan" (62), "konsultan ipo" (30), "audit services indonesia" (67).
Isi:
- /wilayah/<kota>/: title, description, H1 memuat Akuntan, KAP, KJPP, Pajak + baris link ke /akuntan-terdekat/.
- Halaman baru: /akuntan-terdekat/, /konsultan-keuangan/, /jasa-laporan-keuangan-bulanan/, /en/accountant-indonesia/.
- Title /konsultan-persiapan-ipo/ diawali "Konsultan IPO". 301 /konsultan-ipo/ dan /jasa-laporan-keuangan/.
- Blok di /layanan/, sitemap, llms. Idempoten. Jalankan setelah fa_layanan_rapi_20261103.py."""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-04"')
exec(compile(_src, "fa_lead_helpers", "exec"))
URLS = []
CA = "https://cariakuntan.com"

# ---------- daftar kota ----------
CITIES = []
for p in sorted(glob.glob(P("wilayah", "*", "index.html"))):
    slug = os.path.basename(os.path.dirname(p))
    m = re.search(r'"position": 3, "name": "([^"]+)", "item": "https://faindonesia\.co\.id/wilayah/' + re.escape(slug) + '/"', rd(p))
    if m: CITIES.append((slug, m.group(1)))
city_links = " · ".join(f'<a href="/wilayah/{s}/">{E(n)}</a>' for s, n in CITIES)

# ---------- 1. /wilayah/<kota>/ ----------
nw = 0
for slug, city in CITIES:
    p = P("wilayah", slug, "index.html"); t = re.sub(r"<!--fa-kw-w-->.*?<!--/fa-kw-w-->", "", rd(p), flags=re.S)
    title = f"Akuntan dan KAP {city}: Jasa Audit, Laporan Keuangan, KJPP, Pajak | FA Indonesia"
    desc = (f"Cari akuntan atau kantor akuntan publik (KAP) di {city}? Audit oleh KAP DHN & Rekan terdaftar OJK, laporan keuangan oleh KJA Farhani, "
            "kredit bank, valuasi, KJPP dan pajak. Daring, diskusi awal gratis.")
    t = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", t, count=1, flags=re.S)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', t, count=1)
    for a in ['name="description"', 'property="og:description"']:
        t = re.sub(rf'<meta {a} content="[^"]*">', f'<meta {a} content="{E(desc)}">', t, count=1)
    t = re.sub(r'(<h1[^>]*>)[^<]*</h1>', lambda m: f"{m.group(1)}Akuntan dan KAP di {E(city)}: Audit, Laporan Keuangan, dan Financial Advisor</h1>", t, count=1)
    add = (f'<!--fa-kw-w--><p class="t">Mencari <b>akuntan terdekat</b> atau <b>kantor akuntan publik di {E(city)}</b>? Kami bekerja daring untuk seluruh {E(city)} dan kabupaten sekitarnya: '
           f'audit lewat <a href="/kap-dhn/">KAP DHN &amp; Rekan</a>, laporan keuangan lewat <a href="/kja-farhani/">KJA Farhani</a>, rujukan KJPP dan konsultan pajak lewat '
           f'<a href="{CA}/kota/{slug}/">CariAkuntan {E(city)}</a>. Kota lain: <a href="/akuntan-terdekat/">Akuntan Terdekat di Seluruh Indonesia</a>.</p><!--/fa-kw-w-->')
    k = t.find("<h2>Layanan di ")
    if k < 0: k = t.find("<h2", t.find("</h1>"))
    if k < 0: continue
    wtxt(p, t[:k] + add + t[k:]); nw += 1


# ---------- 1b. /wilayah/<kota>/kecamatan/<kec>/ ----------
nk = 0
for p in glob.glob(P("wilayah", "*", "kecamatan", "*", "index.html")):
    t = rd(p); m = re.search(r"<title>(?:Jasa Audit dan Laporan Keuangan di|Akuntan dan KAP) ([^,<]+), ([^|<]+?)(?::[^|<]*)? \| FA Indonesia</title>", t)
    if not m: continue
    k, kab = m.group(1).strip(), m.group(2).strip()
    ti = f"Akuntan dan KAP {k}, {kab}: Jasa Audit, Laporan Keuangan | FA Indonesia"
    t = re.sub(r"<title>.*?</title>", f"<title>{E(ti)}</title>", t, count=1, flags=re.S)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(ti)}">', t, count=1)
    wtxt(p, t); nk += 1

# ---------- 2. /akuntan-terdekat/ ----------
PT = "/akuntan-terdekat/"
bt = ("<h2>Akuntan, KAP, dan KJA dalam Satu Tim</h2>"
 + tbl(["Kebutuhan", "Siapa", "Catatan"], [
   ("Audit laporan keuangan (bank, SABH, investor, tender)", "KAP DHN & Rekan", "Kantor akuntan publik berizin Menteri Keuangan, terdaftar OJK"),
   ("Pembukuan dan penyusunan laporan keuangan", "KJA Farhani", "Kantor jasa akuntansi berizin, bon cukup di-upload ke Drive"),
   ("Kredit bank, investor, valuasi, IPO", "FA Indonesia", "Koordinator: Ananta W. Sasongko, CPA"),
   ("Penilai aset (KJPP) dan konsultan pajak", "Rujukan mitra", "Lewat cariakuntan.com per kota")])
 + "<p>Untuk satu perusahaan, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda.</p>"
 "<h2>Kenapa Tidak Harus yang Paling Dekat</h2><ul><li>Dokumen dikirim daring, review lewat video call. Klien kami tersebar dari Aceh sampai Papua.</li>"
 "<li>Kunjungan lapangan dijadwalkan untuk observasi persediaan dan aset bila audit memerlukannya.</li>"
 "<li>Biaya disepakati di depan, tidak ada biaya perjalanan tersembunyi untuk pekerjaan daring.</li></ul>"
 "<h2>Cari per Kota</h2>"
 f'<details class="fold"><summary>Semua Kota ({len(CITIES)})</summary><p class="t">{city_links}</p></details>'
 f'<p>Per kecamatan: buka halaman kota lalu bagian <b>Layanan per Kecamatan</b>. Daftar KAP, KJA, KJPP, dan konsultan pajak lain: <a href="{CA}/">cariakuntan.com</a>.</p>')
FT = [("Apakah ada akuntan publik terdekat di kota saya?", "Kami melayani seluruh Indonesia secara daring. Audit dilakukan KAP DHN & Rekan dengan kunjungan lapangan bila perlu, jadi jarak kantor tidak menghambat."),
      ("Apa beda KAP dan KJA?", "KAP (kantor akuntan publik) memberi opini audit. KJA (kantor jasa akuntansi) menyusun pembukuan dan laporan keuangan, tidak boleh memberi opini audit."),
      ("Berapa biaya akuntan untuk usaha kecil?", "Pembukuan UMKM mulai Rp900 ribu per bulan, PT dan CV mulai Rp2 juta per bulan. Audit disepakati setelah melihat neraca saldo.")]
svc_page(PT, "Layanan · Seluruh Indonesia", "Akuntan Terdekat dan Kantor Akuntan Publik Terdekat, Melayani Seluruh Indonesia",
  "Cari akuntan, KAP, atau KJA terdekat? Satu tim untuk audit, laporan keuangan, kredit bank, dan pajak, melayani kota dan kabupaten di seluruh Indonesia secara daring.",
  bt, FT, "Akuntan Terdekat, Kantor Akuntan Publik (KAP) Terdekat, KJA | FA Indonesia",
  "Akuntan dan kantor akuntan publik terdekat untuk audit, laporan keuangan, kredit bank, pajak. KAP DHN & Rekan, KJA Farhani, melayani seluruh Indonesia.",
  "Akuntan dan Kantor Akuntan Publik", "Accountant near me", "/wilayah/", "Pilih Kota",
  "Halo FA Indonesia, saya cari akuntan/KAP terdekat untuk usaha saya.", "Akuntan Terdekat")
URLS.append(PT)

# ---------- 3. /konsultan-keuangan/ ----------
PK = "/konsultan-keuangan/"
bk = ("<h2>Yang Dikerjakan Konsultan Keuangan Kami</h2>"
 + tbl(["Masalah", "Pekerjaan", "Hasil"], [
   ("Laporan keuangan tidak dipercaya bank atau investor", "Penyusunan ulang laporan sesuai SAK, persiapan audit KAP", "Laporan keuangan siap audit"),
   ("Kas sering kurang padahal penjualan naik", "Analisis siklus kas, piutang, persediaan, proyeksi 12 bulan", "Rencana arus kas dan modal kerja"),
   ("Butuh tambahan kredit atau take over", "Analisis kapasitas kredit (DSCR), proposal ke bank", "Paket kredit siap diajukan"),
   ("Mau cari investor atau jual sebagian usaha", "Valuasi, information memorandum, pendampingan negosiasi", "Nilai wajar dan materi investor"),
   ("Persiapan IPO", "Gap assessment, laporan audited, tata kelola", "Peta jalan IPO"),
   ("Tim keuangan belum ada pemimpin", "CFO paruh waktu", "Laporan manajemen bulanan dan rapat bulanan")])
 + "<h2>Cara Kerja</h2>" + flow([("Diskusi awal", "Gratis, 30 sampai 45 menit."), ("NDA dan data", "Laporan keuangan, neraca saldo, rekening koran."), ("Diagnosis", "Temuan dan rencana kerja tertulis dengan biaya tetap."), ("Eksekusi", "Dikerjakan bersama tim keuangan Anda.")])
 + "<h2>Pengalaman</h2><p>Rumah sakit di DKI Jakarta dan Jawa Tengah, hotel di Bali dan Papua, kontraktor di Sumatra, Batam, Kalimantan, Sulawesi, ratusan BPR, dan ribuan UMKM.</p>"
 "<p>Terkait: <a href=\"/konsultan-kredit-bank/\">Konsultan Kredit Bank</a> · <a href=\"/cfo-paruh-waktu/\">CFO Paruh Waktu</a> · <a href=\"/jasa-valuasi-usaha/\">Valuasi Usaha</a> · <a href=\"/konsultan-persiapan-ipo/\">Konsultan IPO</a> · <a href=\"/akuntan-terdekat/\">Akuntan Terdekat</a></p>")
FK = [("Apa bedanya konsultan keuangan dan akuntan?", "Akuntan menyusun atau mengaudit laporan keuangan. Konsultan keuangan memakai laporan itu untuk keputusan: kredit, investor, arus kas, valuasi, IPO. Di FA keduanya satu tim."),
      ("Berapa biaya konsultan keuangan?", "Proyek dihitung tetap setelah diagnosis. CFO paruh waktu mulai Rp15 juta per bulan."),
      ("Apakah melayani di luar Jakarta?", "Ya, seluruh Indonesia secara daring, pertemuan langsung dijadwalkan bila perlu.")]
svc_page(PK, "Layanan · Konsultan Keuangan", "Konsultan Keuangan dan Manajemen Keuangan Perusahaan",
  "Untuk pemilik usaha yang butuh keputusan keuangan yang tepat: arus kas, kredit bank, investor, valuasi, sampai IPO. Didukung akuntan dan KAP dalam satu tim.",
  bk, FK, "Konsultan Keuangan Perusahaan dan Manajemen Keuangan: Kredit, Investor, IPO | FA Indonesia",
  "Konsultan keuangan dan manajemen keuangan untuk perusahaan dan UMKM: arus kas, kredit bank, investor, valuasi, IPO, CFO paruh waktu. Seluruh Indonesia.",
  "Konsultan Keuangan Perusahaan", "Financial consulting", "/layanan/", "Semua Layanan",
  "Halo FA Indonesia, saya butuh konsultan keuangan untuk usaha saya.", "Konsultan Keuangan")
URLS.append(PK)

# ---------- 4. /jasa-laporan-keuangan-bulanan/ ----------
PB = "/jasa-laporan-keuangan-bulanan/"
bb = ("<h2>Terima Beres Setiap Bulan</h2>" + flow([
   ("Upload bon", "Nota, faktur, rekening koran di-upload ke folder Google Drive bersama."),
   ("Dikerjakan KJA Farhani", "Jurnal, buku besar, rekonsiliasi bank."),
   ("Laporan terbit", "Neraca, laba rugi, arus kas 5 sampai 10 hari kerja setelah bon lengkap."),
   ("Review", "Video call singkat membahas angka penting bulan itu.")])
 + "<h2>Paket</h2>" + tbl(["Paket", "Untuk", "Mulai"], [
   ("UMKM dan perorangan", "Catatan single entry, satu rekening usaha", "Rp900 ribu per bulan"),
   ("PT dan CV", "Laporan keuangan lengkap sesuai SAK EP atau SAK EMKM", "Rp2 juta per bulan"),
   ("Laporan tahunan PT", "Untuk RUPS dan SABH, belum termasuk biaya notaris", "Rp3 juta")])
 + f'<p>Rincian paket dan contoh laporan: <a href="{CA}/jasa-pembukuan/">Jasa Pembukuan Terima Beres</a>. Kalau perlu audit, dikerjakan <a href="/kap-dhn/">KAP DHN &amp; Rekan</a>, pihak terpisah dari penyusun laporan.</p>')
FB = [("Kenapa pakai jasa, bukan aplikasi akuntansi?", "Aplikasi tetap butuh orang yang menjurnal dan merekonsiliasi. Dengan jasa, Anda cukup upload bon dan menerima laporan jadi."),
      ("Apakah laporan bulanan bisa dipakai untuk kredit bank?", "Bisa sebagai laporan interim. Untuk plafon besar bank biasanya meminta laporan audited tahunan juga."),
      ("Bagaimana kalau bon belum lengkap?", "Kami kirim daftar kekurangan, laporan terbit setelah data lengkap.")]
svc_page(PB, "Layanan · Laporan Keuangan", "Jasa Pembuatan Laporan Keuangan Bulanan, Terima Beres",
  "Upload bon ke Drive, laporan keuangan bulanan jadi 5 sampai 10 hari kerja setelah bon lengkap. UMKM mulai Rp900 ribu, PT dan CV mulai Rp2 juta per bulan.",
  bb, FB, "Jasa Pembuatan Laporan Keuangan Bulanan Terima Beres, Mulai Rp900 Ribu | FA Indonesia",
  "Jasa laporan keuangan bulanan terima beres: upload bon ke Drive, neraca dan laba rugi jadi 5 sampai 10 hari. UMKM mulai Rp900 ribu, PT/CV mulai Rp2 juta.",
  "Jasa Laporan Keuangan Bulanan", "Monthly bookkeeping and financial statements", f"{CA}/jasa-pembukuan/", "Lihat Paket",
  "Halo FA Indonesia, saya mau jasa laporan keuangan bulanan.", "Laporan Keuangan Bulanan")
URLS.append(PB)

# ---------- 5. /en/accountant-indonesia/ ----------
PE = "/en/accountant-indonesia/"
be = ("<h2>One Team for Accounting, Audit, and Finance</h2><div class=\"tblwrap\"><table><tr><th>Need</th><th>Who</th></tr>"
 "<tr><td>Statutory audit</td><td><a href=\"/kap-dhn/\">KAP DHN &amp; Rekan</a>, licensed public accounting firm registered with OJK</td></tr>"
 "<tr><td>Bookkeeping and financial statements</td><td><a href=\"/kja-farhani/\">KJA Farhani</a>, licensed accounting services firm</td></tr>"
 "<tr><td>Bank loans, investors, valuation</td><td><a href=\"/ananta-w-sasongko/\">Ananta W. Sasongko, CPA</a></td></tr></table></div>"
 "<p>We serve Jakarta, Batam, Bali, Surabaya, and every province remotely, with field visits when an audit requires them. "
 "For foreign-owned companies see <a href=\"/en/statutory-audit-indonesia/\">Statutory Audit for PT PMA</a>.</p>")
FE = [("Is there an accountant near me in Indonesia?", "We work remotely across Indonesia, so location is not a barrier. Field visits are scheduled when needed."),
      ("Can reports be in English?", "Yes. Financial statements and audit reports can be issued in English and Indonesian.")]
svc_page(PE, "Services · English", "Accountant and Audit Services in Indonesia",
  "Bookkeeping, financial statements, statutory audit, and financial advisory for companies in Indonesia, coordinated in English.",
  be, FE, "Accountant and Audit Services in Indonesia: Bookkeeping, Statutory Audit | FA Indonesia",
  "English-speaking accountants in Indonesia: bookkeeping, financial statements, statutory audit by an OJK-registered firm, bank loans and valuation. Nationwide.",
  "Accounting and Audit Services Indonesia", "Accountant near me", "/en/statutory-audit-indonesia/", "PT PMA Audit",
  "Hello FA Indonesia, I need an accountant / audit services in Indonesia.", "Accountant Indonesia (EN)")
pe = P("en", "accountant-indonesia", "index.html"); t = rd(pe)
t = re.sub(r'<html lang="[^"]*"', '<html lang="en"', t, count=1)
t = t.replace("Chat Ananta, CPA", "Chat with Ananta, CPA").replace("<h2>Pertanyaan Umum</h2>", "<h2>FAQ</h2>")
wtxt(pe, t); URLS.append(PE)

# ---------- 6. title IPO, redirect ----------
ip = P("konsultan-persiapan-ipo", "index.html")
if os.path.exists(ip):
    t = rd(ip); ti = "Konsultan IPO: Jasa Pendampingan dan Persiapan IPO di BEI | FA Indonesia"
    t = re.sub(r"<title>.*?</title>", f"<title>{E(ti)}</title>", t, count=1, flags=re.S)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(ti)}">', t, count=1)
    wtxt(ip, t)
rp = P("_redirects"); r = re.sub(r"# fa-kw\n.*?# /fa-kw\n", "", rd(rp), flags=re.S)
r = r.rstrip("\n") + "\n# fa-kw\n/konsultan-ipo/ /konsultan-persiapan-ipo/ 301\n/konsultan-ipo /konsultan-persiapan-ipo/ 301\n/jasa-laporan-keuangan/ /jasa-penyusunan-laporan-keuangan/ 301\n/jasa-laporan-keuangan /jasa-penyusunan-laporan-keuangan/ 301\n/akuntan-publik-terdekat/ /akuntan-terdekat/ 301\n# /fa-kw\n"
wtxt(rp, r)

# ---------- 7. /layanan/, sitemap, llms ----------
lp = P("layanan", "index.html"); t = re.sub(r"<!--fa-kw-svc-->.*?<!--/fa-kw-svc-->", "", rd(lp), flags=re.S)
blk = ('<!--fa-kw-svc--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Paling Dicari</p><h2>Akuntan, Konsultan Keuangan, Laporan Bulanan</h2></div>'
       '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn solid" href="/akuntan-terdekat/">Akuntan Terdekat</a><a class="btn line" href="/konsultan-keuangan/">Konsultan Keuangan</a>'
       '<a class="btn line" href="/jasa-laporan-keuangan-bulanan/">Laporan Keuangan Bulanan</a><a class="btn line" href="/en/accountant-indonesia/">English</a></div></div></section><!--/fa-kw-svc-->')
i = t.find('<section class="block'); wtxt(lp, t[:i] + blk + t[i:])
sm = re.sub(r"<!--fa-kw-->.*?<!--/fa-kw-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-kw-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.9</priority></url>\n" for u in URLS) + "<!--/fa-kw-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
lines = ("- Akuntan dan KAP terdekat, seluruh Indonesia daring → https://faindonesia.co.id/akuntan-terdekat/\n"
         "- Konsultan keuangan dan manajemen keuangan perusahaan → https://faindonesia.co.id/konsultan-keuangan/\n"
         "- Jasa laporan keuangan bulanan terima beres (mulai Rp900 ribu/bulan) → https://faindonesia.co.id/jasa-laporan-keuangan-bulanan/\n")
ll = rd(P("llms.txt"))
for x in lines.splitlines(True): ll = ll.replace(x, "")
ll = ll.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + lines, 1) if "\n## Layanan Spesifik\n" in ll else ll.rstrip("\n") + "\n\n## Layanan Spesifik\n" + lines
wtxt(P("llms.txt"), ll)
print("fa_kw ok", URLS, "wilayah", nw, "kecamatan", nk, "kota", len(CITIES))
