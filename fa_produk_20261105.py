# -*- coding: utf-8 -*-
"""SEO push produk FA (5 Nov 2026): kalkulator FA Venus, FA Jupiter, FA Saturn, Cek PSAK 118, hub kalkulator.
- 7 kalkulator FA Venus (PPh 21, PPh Badan, Potput PPN, Penyusutan, Cicilan, DCF, Rasio): title keyword, H1, schema
  WebApplication (gratis) + FAQPage + Breadcrumb, blok SEO (untuk siapa, cara pakai, dasar hitung, FAQ accordion).
- FA Jupiter /audit-ready/, FA Saturn /saturn/, FA Venus /cek-psak-118/ (sumber FA-Jupiter/FA-Saturn/FA-Venus): title keyword,
  blok SEO statis di bawah <main> (halaman app dirender JS), schema SoftwareApplication + FAQ.
- Grid "Kalkulator dan Aplikasi FA Lainnya" di semua halaman alat (internal link silang).
- Hub baru: /kalkulator-pajak/, /kalkulator-keuangan/, /aplikasi-akuntansi-gratis/, /aplikasi-audit-kap/,
  /en/free-tax-finance-calculators-indonesia/. Link hub di /apps/, /toko/, /layanan/, sitemap, llms.txt.
- Artikel pendukung: fa_content/seo30_apps.json (dibangun fa_seo20_20261030.py).
Idempoten (penanda fa-prod). Jalankan setelah fa_tools_20261105.py, sebelum kja_kota_20261101.py."""
import os, re, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-05"')
exec(compile(_src, "fa_lead_helpers", "exec"))
JUP = os.path.join(HERE, "FA-Jupiter_SIAP-UPLOAD-v6", "audit-ready", "index.html")
SAT = os.path.join(HERE, "FA-Saturn_SIAP-UPLOAD-v4", "saturn", "index.html")
VEN = os.path.join(HERE, "FA-Venus_SIAP-UPLOAD-v2", "cek-psak-118", "index.html")
URLS = []
SHORT = {
"kalkulator-pph-21": "Kalkulator PPh 21 TER 2026 gratis: potongan bulanan kategori A, B, C, bulan THR, masa Desember tarif Pasal 17, BPJS, gross up, dan bukan pegawai.",
"kalkulator-pph-badan": "Kalkulator PPh Badan 2026 gratis: tarif 22%, fasilitas Pasal 31E, PPh final 0,5% UMKM, kurang bayar PPh 29, dan angsuran PPh 25 bulanan.",
"kalkulator-potput-ppn": "Hitung PPh 23, PPh 4(2), PPh 26, PPh 22 impor, dan PPN 12% DPP 11/12 dalam satu invoice. Gratis, langsung di browser.",
"kalkulator-penyusutan-fiskal": "Kalkulator penyusutan fiskal gratis: kelompok harta PMK 72/2023, jadwal fiskal vs komersial, koreksi fiskal, dan pajak tangguhan PSAK 212.",
"kalkulator-cicilan-pinjaman": "Kalkulator cicilan pinjaman usaha gratis: anuitas, flat, efektif, tabel amortisasi, bunga sesungguhnya setelah provisi, dan plafon dari DSCR.",
"kalkulator-valuasi-dcf": "Kalkulator valuasi DCF gratis: WACC dengan CAPM, proyeksi FCFF 5 tahun, nilai terminal, nilai ekuitas per saham, dan tabel sensitivitas.",
"kalkulator-rasio-keuangan": "Kalkulator rasio keuangan gratis: current ratio, DER, DSCR, margin, ROE, cash conversion cycle, dan Altman Z-Score dengan indikator warna.",
"audit-ready": "FA Jupiter: upload COA dan GL dari Accurate, Jurnal, atau Xero, jadi laporan keuangan, CALK, lead schedule, dan checklist PBC siap audit. Gratis dicoba.",
"saturn": "FA Saturn: software kertas kerja audit untuk KAP. Materialitas, risk assessment per asersi, program audit, review notes, sign-off berjenjang. Demo gratis.",
"cek-psak-118": "Ubah laba rugi PSAK 201 ke format PSAK 118 (IFRS 18) yang berlaku 2027: kategori operasi, investasi, pendanaan, subtotal wajib, MPM. Gratis.",
"/kalkulator-pajak/": "Kalkulator pajak online gratis 2026: PPh 21 TER, PPh Badan 22%, PPh 23, PPh 4(2), PPN 12% DPP 11/12, dan penyusutan fiskal. Tanpa daftar.",
"/kalkulator-keuangan/": "Kalkulator keuangan perusahaan gratis: DSCR, plafon kredit, cicilan pinjaman, rasio keuangan, Altman Z, valuasi DCF, dan cek kelayakan IPO.",
"/aplikasi-akuntansi-gratis/": "Aplikasi akuntansi gratis berbasis web: laporan keuangan dan CALK sesuai SAK EMKM, SAK EP, PSAK, FA Jupiter audit ready, konverter PSAK 118.",
"/aplikasi-audit-kap/": "Software audit untuk KAP: kertas kerja digital, materialitas, risk assessment, sign-off berjenjang (FA Saturn) dan laporan audit ready (FA Jupiter).",
"/en/free-tax-finance-calculators-indonesia/": "Free Indonesian calculators: PPh 21 payroll tax, corporate tax, withholding tax and 12% VAT, loan DSCR, ratios, DCF valuation. No sign-up."
}

# ====================== daftar produk (untuk grid link silang) ======================
TOOLS = [
 # slug/href, nama tampil, kicker, kelompok
 ("/kalkulator-pph-21/", "Kalkulator PPh 21 TER", "TER bulanan, Desember, THR, gross up", "pajak"),
 ("/kalkulator-pph-badan/", "Kalkulator PPh Badan", "Tarif 22%, Pasal 31E, PPh final 0,5%, PPh 25", "pajak"),
 ("/kalkulator-potput-ppn/", "Kalkulator PPh Potput dan PPN", "PPh 23, 4(2), 26, 22, PPN 12% DPP 11/12", "pajak"),
 ("/kalkulator-penyusutan-fiskal/", "Kalkulator Penyusutan Fiskal", "Susut fiskal vs komersial, pajak tangguhan", "pajak"),
 ("/cek-kapasitas-kredit/", "Cek Kapasitas Kredit", "DSCR, plafon, syarat IPO", "keuangan"),
 ("/kalkulator-dscr/", "Kalkulator DSCR", "Rumus, contoh, batas aman bank", "keuangan"),
 ("/simulasi-plafon-kredit-usaha/", "Simulasi Plafon Kredit Usaha", "KI, KMK, top up, take over", "keuangan"),
 ("/kalkulator-cicilan-pinjaman/", "Kalkulator Cicilan Pinjaman", "Anuitas, flat, efektif, biaya kredit", "keuangan"),
 ("/kalkulator-rasio-keuangan/", "Kalkulator Rasio Keuangan", "Likuiditas, DER, ROE, Altman Z", "keuangan"),
 ("/kalkulator-valuasi-dcf/", "Kalkulator Valuasi DCF", "WACC, FCFF, nilai terminal, sensitivitas", "keuangan"),
 ("/kalkulator-valuasi-rumah-sakit/", "Kalkulator Valuasi Rumah Sakit", "Harga jual RS before dan after", "keuangan"),
 ("/cek-kelayakan-ipo/", "Cek Kelayakan IPO", "Papan Utama, Pengembangan, Akselerasi", "keuangan"),
 ("/cek-kesiapan-pendanaan/", "Cek Kesiapan Pendanaan", "Skor siap kredit bank atau investor", "keuangan"),
 ("/bankability-index/", "Bankability Index", "Seberapa siap dibiayai bank", "keuangan"),
 ("/cek-psak-118/", "Konverter PSAK 118", "Laba rugi PSAK 201 ke PSAK 118", "akuntansi"),
 ("/audit-ready/", "FA Jupiter Audit Ready", "GL jadi laporan keuangan dan CALK", "akuntansi"),
 ("/saturn/", "FA Saturn Audit Workspace", "Kertas kerja audit untuk KAP", "audit"),
 ("https://updatesak.com/#kalkulator-psak", "Kalkulator PSAK (UpdateSAK)", "Kerangka SAK dan PSAK per akun", "akuntansi"),
 ("https://updatesak.com/#laporan-keuangan", "Penyusun Laporan Keuangan (UpdateSAK)", "Neraca, laba rugi, arus kas dari saldo", "akuntansi"),
 ("https://updatesak.com/#calk", "Penyusun CALK (UpdateSAK)", "Catatan atas laporan keuangan", "akuntansi"),
 ("https://cariakuntan.com/screening/", "Screening Instan (CariAkuntan)", "Rasio bank dan jalur IPO sebelum pilih KAP", "keuangan"),
]
HUBS = [("/kalkulator-pajak/", "Kalkulator Pajak"), ("/kalkulator-keuangan/", "Kalkulator Keuangan"),
        ("/aplikasi-akuntansi-gratis/", "Aplikasi Akuntansi Gratis"), ("/aplikasi-audit-kap/", "Aplikasi Audit untuk KAP")]

def grid(cur, dark=True):
    """Grid link silang, dipasang di tiap halaman alat."""
    items = "".join(f'<a href="{h}"{" target=_blank rel=noopener" if h.startswith("http") else ""}><b>{E(n)}</b><span>{E(k)}</span></a>'
                    for h, n, k, g in TOOLS if h != cur)
    hubs = " · ".join(f'<a href="{h}">{E(n)}</a>' for h, n in HUBS)
    return ('<section class="fa-prod-grid" aria-label="Kalkulator dan aplikasi FA lainnya"><h2>Kalkulator dan Aplikasi FA Lainnya</h2>'
            '<p>Semua gratis dipakai di browser, tanpa instal, tanpa kartu kredit.</p>'
            f'<div class="fpg">{items}</div><p class="fph">Hub: {hubs} · <a href="/apps/">Semua FA Apps</a> · <a href="/galaxy/">Panduan FA Galaxy</a></p></section>')

CSS = ('<style id="fa-prod">.fa-prod{margin:28px 0 8px}.fa-prod .sec{padding:18px 20px;margin-top:14px}.fa-prod h1{font-family:var(--f-display,Georgia,serif);font-weight:400;font-size:clamp(26px,3.4vw,38px);line-height:1.15;margin:0 0 10px}'
       '.fa-prod h2{font-family:var(--f-display,Georgia,serif);font-weight:400;font-size:clamp(21px,2.6vw,26px);line-height:1.2;margin:0 0 6px}.fa-prod p,.fa-prod li{font-size:14.5px;line-height:1.65;max-width:80ch}'
       '.fa-prod ul,.fa-prod ol{margin:4px 0 0;padding-left:22px;display:flex;flex-direction:column;gap:6px}.fa-prod details{border-top:1px solid var(--line,#2f2f2f);padding:10px 0}.fa-prod details:last-of-type{border-bottom:1px solid var(--line,#2f2f2f)}'
       '.fa-prod summary{cursor:pointer;font-weight:500;font-size:14.5px;list-style:none;display:flex;justify-content:space-between;gap:12px}.fa-prod summary::-webkit-details-marker{display:none}.fa-prod summary:after{content:"+";color:var(--muted,#a8a8a8)}.fa-prod details[open] summary:after{content:"\\2212"}'
       '.fa-prod details p{margin:8px 0 0;color:var(--muted,#a8a8a8)}.fa-prod a{color:inherit}'
       '.fa-prod-grid{margin:22px 0 10px;padding:18px 20px;border:1px solid var(--line,#2f2f2f);border-radius:8px;background:var(--panel,#1e1e1e)}.fa-prod-grid h2{font-family:var(--f-display,Georgia,serif);font-weight:400;font-size:clamp(21px,2.6vw,26px);margin:0 0 4px}'
       '.fa-prod-grid>p{margin:0 0 12px;font-size:13.5px;color:var(--muted,#a8a8a8)}.fpg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px}.fpg a{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border:1px solid var(--line,#2f2f2f);border-radius:6px;text-decoration:none;color:var(--ink,#fff);background:var(--soft,#242424)}'
       '.fpg a:hover{border-color:#fff}.fpg b{font-weight:500;font-size:13.5px}.fpg span{font-size:12px;color:var(--muted,#a8a8a8)}.fph{margin:12px 0 0!important;font-size:13px}.fph a{color:var(--ink,#fff)}</style>')

def faqs(faq): return "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
def seo_block(h1, intro, who, steps, basis, faq, cur, h1_tag="h1", who_h="Untuk Siapa", steps_h="Cara Memakai", basis_h="Dasar Perhitungan"):
    return ('<!--fa-prod--><div class="fa-prod"><section class="sec">'
            + (f"<{h1_tag}>{E(h1)}</{h1_tag}>" if h1 else "") + "".join(f"<p>{p}</p>" for p in intro)
            + f'</section><section class="sec"><h2>{who_h}</h2><ul>' + "".join(f"<li>{w}</li>" for w in who) + "</ul></section>"
            + f'<section class="sec"><h2>{steps_h}</h2><ol>' + "".join(f"<li>{s}</li>" for s in steps) + "</ol></section>"
            + (f'<section class="sec"><h2>{basis_h}</h2>' + "".join(f"<p>{b}</p>" for b in basis) + "</section>" if basis else "")
            + f'<section class="sec"><h2>Pertanyaan Umum</h2>{faqs(faq)}</section>' + grid(cur) + "</div><!--/fa-prod-->")

def set_title(t, title, desc=None):
    t = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", t, count=1, flags=re.S)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', t, count=1)
    if desc:
        for a in ['name="description"', 'property="og:description"']:
            t = re.sub(rf'<meta {a} content="[^"]*">', f'<meta {a} content="{E(desc)}">', t, count=1)
    return t
def set_ld(t, ld):
    s = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"
    if re.search(r'<script type="application/ld\+json">', t):
        return re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: s, t, count=1, flags=re.S)
    return t.replace("</head>", s + "\n</head>", 1)
def add_css(t):
    t = re.sub(r'<style id="fa-prod">.*?</style>', "", t, flags=re.S)
    return t.replace("</head>", CSS + "</head>", 1)
def app_ld(url, name, desc, faq, crumb, free=True, cat="FinanceApplication"):
    app = {"@type": ["WebApplication", "SoftwareApplication"], "@id": url + "#app", "name": name, "url": url, "description": desc,
           "applicationCategory": cat, "operatingSystem": "Web (browser)", "inLanguage": "id", "isAccessibleForFree": free,
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR", "availability": "https://schema.org/InStock", "url": url},
           "publisher": {"@type": "Organization", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"},
           "author": {"@type": "Person", "name": "Ananta W. Sasongko", "url": D + "/ananta-w-sasongko/"}}
    return {"@context": "https://schema.org", "@graph": [app, faq_ld(faq), crumbs([("FA Indonesia", D + "/"), ("FA Apps", D + "/apps/"), (crumb, url)])]}

# ====================== 1. 7 kalkulator FA Venus ======================
VENUS = {
"kalkulator-pph-21": dict(
 title="Kalkulator PPh 21 TER 2026 Gratis: Bulanan, Desember, THR, Gross Up | FA Venus",
 desc="Kalkulator PPh 21 online gratis sesuai PP 58/2023 dan PMK 168/2023: TER bulanan kategori A, B, C, masa Desember tarif Pasal 17, THR dan bonus, BPJS, gross up, take home pay, PPh 21 bukan pegawai.",
 h1="Kalkulator PPh 21 TER 2026: Hitung Potongan Bulanan, THR, dan Masa Desember",
 intro=["Sejak Januari 2024 pemotongan PPh 21 pegawai tetap memakai <b>tarif efektif rata-rata (TER)</b> dari Januari sampai November, lalu dihitung ulang dengan tarif Pasal 17 pada masa Desember. Kalkulator ini menghitung keduanya sekaligus, termasuk bulan ada THR atau bonus, premi BPJS yang dibayar pemberi kerja, dan skema gross up.",
        "Hasilnya adalah angka potongan per bulan, take home pay, dan simulasi setahun yang bisa dibandingkan dengan bukti potong 1721-A1. Cocok untuk HR, staf payroll, pemilik usaha, dan pegawai yang ingin mengecek potongan gajinya sendiri."],
 who=["<b>HR dan payroll</b> yang menyiapkan potongan bulanan dan rekonsiliasi Desember.", "<b>Pemilik usaha dan UMKM</b> yang menggaji pegawai tanpa software payroll.",
      "<b>Pegawai</b> yang ingin memastikan potongan PPh 21 di slip gaji sudah benar.", "<b>Freelancer, komisaris, dan tenaga ahli</b> (bukan pegawai) yang dipotong dengan tarif Pasal 17 atas 50% bruto."],
 steps=["Pilih status PTKP (TK/0 sampai K/3). Kalkulator memetakannya ke kategori TER A, B, atau C.", "Isi gaji pokok, tunjangan, dan premi BPJS yang ditanggung perusahaan. Centang gross up bila pajak ditanggung pemberi kerja.",
        "Isi THR atau bonus pada bulan tertentu untuk melihat lonjakan potongan di bulan itu.", "Baca hasil bulan reguler, lalu buka simulasi Januari sampai Desember untuk melihat kurang atau lebih potong di masa Desember."],
 basis=["Tarif efektif bulanan dan harian mengikuti Lampiran PP 58 Tahun 2023, tata caranya PMK 168 Tahun 2023. PPh 21 masa Desember = PPh Pasal 17 setahun dikurangi PPh 21 yang sudah dipotong Januari sampai November. PTKP Rp54 juta, tambahan Rp4,5 juta untuk status kawin dan per tanggungan (maksimal 3), biaya jabatan 5% maksimal Rp6 juta setahun. Rincian aturan ada di bagian Dasar Hitung di atas."],
 faq=[("Apa itu TER PPh 21?", "TER (tarif efektif rata-rata) adalah tarif persentase yang langsung dikalikan penghasilan bruto bulanan, dibagi kategori A, B, C sesuai status PTKP. Dipakai Januari sampai November, lalu masa Desember dihitung ulang dengan tarif Pasal 17."),
      ("Kenapa potongan Desember beda jauh dengan bulan lain?", "Karena Desember adalah bulan penyesuaian. PPh setahun dihitung dengan tarif progresif Pasal 17, lalu dikurangi total potongan TER Januari sampai November. Selisihnya, positif atau negatif, masuk ke potongan Desember."),
      ("Apakah THR dan bonus kena TER?", "Ya. Di bulan pembayaran, THR atau bonus digabung dengan gaji bulan itu lalu dikalikan TER, sehingga potongan bulan tersebut melonjak. Penyesuaiannya terjadi di masa Desember."),
      ("Apakah kalkulator ini bisa untuk pegawai tidak tetap dan freelancer?", "Bisa. Tab Bukan Pegawai dan Harian menghitung upah harian dengan TER harian, serta tenaga ahli, komisaris, dan peserta kegiatan dengan tarif Pasal 17."),
      ("Apakah data gaji saya tersimpan?", "Tidak. Seluruh perhitungan berjalan di browser Anda dan tidak dikirim ke server mana pun."),
      ("Apakah kalkulator PPh 21 ini gratis?", "Gratis untuk dipakai tanpa batas. Pengguna yang terbantu bisa mendukung lewat donasi QRIS.")],
 crumb="Kalkulator PPh 21 TER"),
"kalkulator-pph-badan": dict(
 title="Kalkulator PPh Badan 2026 Gratis: Tarif 22%, Pasal 31E, Final 0,5%, PPh 25 | FA Venus",
 desc="Kalkulator PPh Badan online gratis: tarif umum 22%, fasilitas pengurangan 50% Pasal 31E untuk omzet sampai Rp50 miliar, PPh final 0,5% PP 55/2022 untuk UMKM, dan angsuran PPh 25 bulanan.",
 h1="Kalkulator PPh Badan 2026: Tarif 22%, Fasilitas Pasal 31E, dan PPh Final UMKM",
 intro=["Berapa PPh Badan yang harus dibayar PT atau CV Anda tahun ini? Kalkulator ini menghitung tiga skema yang paling sering dipakai: <b>tarif umum 22%</b>, <b>fasilitas Pasal 31E</b> (pengurangan 50% untuk bagian omzet sampai Rp4,8 miliar bagi wajib pajak beromzet sampai Rp50 miliar), dan <b>PPh final 0,5%</b> dari peredaran bruto untuk UMKM yang masih memenuhi syarat PP 55 Tahun 2022.",
        "Hasilnya langsung dibagi menjadi PPh terutang setahun, kredit pajak yang sudah dipotong pihak lain, kurang atau lebih bayar (PPh 29), dan angsuran PPh 25 untuk tahun berikutnya."],
 who=["<b>Pemilik PT dan CV</b> yang ingin memperkirakan pajak sebelum tutup buku.", "<b>UMKM</b> yang ingin membandingkan PPh final 0,5% dengan tarif umum, terutama menjelang batas waktu pemakaian tarif final.",
      "<b>Staf akuntansi</b> yang menyiapkan SPT Tahunan Badan dan menghitung angsuran PPh 25.", "<b>Konsultan dan akuntan</b> yang butuh angka cepat saat diskusi dengan klien."],
 steps=["Isi peredaran bruto (omzet) dan laba fiskal setahun. Laba fiskal adalah laba komersial setelah koreksi fiskal positif dan negatif.", "Pilih skema: tarif umum, Pasal 31E, atau final 0,5%. Kalkulator memberi tahu bila omzet melampaui batas skema yang dipilih.",
        "Isi kredit pajak: PPh 22, 23, 24, dan angsuran PPh 25 yang sudah dibayar.", "Baca PPh kurang atau lebih bayar, lalu angsuran PPh 25 bulanan untuk tahun depan."],
 basis=["Tarif PPh Badan 22% berlaku sejak tahun pajak 2022 (UU HPP). Pasal 31E UU PPh memberi pengurangan tarif 50% atas bagian penghasilan kena pajak dari peredaran bruto sampai Rp4,8 miliar bagi wajib pajak badan beromzet sampai Rp50 miliar. PPh final 0,5% mengikuti PP 55 Tahun 2022 dengan batas waktu pemakaian 3 tahun untuk PT dan 4 tahun untuk CV, firma, dan koperasi. Angsuran PPh 25 = (PPh terutang dikurangi kredit pajak) dibagi 12."],
 faq=[("Berapa tarif PPh Badan 2026?", "Tarif umum 22% dari penghasilan kena pajak. Wajib pajak badan beromzet sampai Rp50 miliar mendapat pengurangan 50% untuk bagian penghasilan dari omzet sampai Rp4,8 miliar (Pasal 31E)."),
      ("Apa beda PPh final 0,5% dengan tarif umum?", "PPh final 0,5% dihitung dari omzet bulanan tanpa melihat laba, berlaku untuk UMKM beromzet sampai Rp4,8 miliar selama jangka waktu tertentu. Tarif umum dihitung dari laba fiskal, sehingga perusahaan yang marginnya tipis bisa lebih hemat dengan tarif umum."),
      ("Bagaimana menghitung angsuran PPh 25?", "PPh terutang tahun lalu dikurangi kredit pajak (PPh 22, 23, 24), dibagi 12 bulan. Kalkulator menghitungnya otomatis dari SPT Tahunan yang Anda simulasikan."),
      ("Apakah laba di laporan keuangan sama dengan laba fiskal?", "Tidak selalu. Laba komersial dikoreksi dengan biaya yang tidak boleh dikurangkan (koreksi positif) dan penghasilan yang sudah kena PPh final atau bukan objek pajak (koreksi negatif). Untuk penyusutan, pakai Kalkulator Penyusutan Fiskal."),
      ("Apakah hasilnya bisa dipakai untuk SPT?", "Hasilnya adalah simulasi untuk perencanaan. Angka SPT tetap mengikuti pembukuan dan koreksi fiskal yang lengkap. Bila perlu, tim FA membantu rekonsiliasi SPT dengan laporan keuangan.")],
 crumb="Kalkulator PPh Badan"),
"kalkulator-potput-ppn": dict(
 title="Kalkulator PPh 23, 4(2), 26, 22 dan PPN 12% DPP 11/12 Gratis | FA Venus",
 desc="Kalkulator pajak potong pungut online gratis: PPh 23 jasa dan sewa, PPh 4 ayat 2 (sewa tanah bangunan, jasa konstruksi), PPh 26, PPh 22 impor, dan PPN 12% dengan DPP nilai lain 11/12 dalam satu invoice.",
 h1="Kalkulator PPh Potong Pungut dan PPN 12%: Hitung Satu Invoice Sekaligus",
 intro=["Satu invoice jasa sering memuat tiga pajak sekaligus: PPN yang dipungut, PPh 23 atau PPh 4 ayat 2 yang dipotong, dan kadang PPh 26 bila lawan transaksinya di luar negeri. Kalkulator ini menghitung semuanya dalam satu layar, dengan <b>PPN 12% atas DPP nilai lain 11/12</b> yang berlaku sejak 1 Januari 2025 sehingga beban efektifnya tetap 11% untuk barang dan jasa non mewah.",
        "Hasilnya adalah nilai yang dibayar ke vendor, pajak yang disetor ke kas negara, dan total biaya bagi pembeli. Cocok untuk staf AP, finance, dan pemilik usaha yang sering bingung menghitung potongan di invoice vendor."],
 who=["<b>Staf finance dan AP</b> yang memproses invoice vendor jasa, sewa, dan kontraktor.", "<b>Vendor dan freelancer</b> yang ingin tahu berapa yang akan diterima bersih setelah dipotong.",
      "<b>Kontraktor</b> yang menghitung PPh final jasa konstruksi berdasarkan kualifikasi.", "<b>Importir</b> yang memperkirakan PPh 22 impor dan PPN impor."],
 steps=["Pilih jenis transaksi: jasa, sewa, konstruksi, dividen, bunga, royalti, impor, atau pembayaran ke luar negeri.", "Isi nilai transaksi dan tentukan apakah harga sudah termasuk PPN.",
        "Centang status lawan transaksi: PKP atau bukan, punya NPWP atau tidak (tarif PPh 23 naik 100% bila tanpa NPWP), tarif tax treaty untuk PPh 26.", "Baca rincian: DPP, PPN, PPh yang dipotong, jumlah dibayar ke vendor, dan jumlah disetor."],
 basis=["PPh 23: 2% untuk jasa dan sewa selain tanah bangunan, 15% untuk dividen, bunga, royalti, hadiah. PPh 4 ayat 2: 10% sewa tanah dan bangunan, jasa konstruksi 1,75% sampai 6% sesuai kualifikasi (PP 9 Tahun 2022). PPh 26: 20% atau tarif tax treaty. PPh 22 impor: 2,5% dengan API, 7,5% tanpa API. PPN: tarif 12% atas DPP nilai lain 11/12 dari harga jual (PMK 131 Tahun 2024) untuk barang dan jasa selain barang mewah tertentu."],
 faq=[("Berapa PPN yang dipungut sejak 2025?", "Tarif resmi 12%, tetapi untuk barang dan jasa selain barang mewah tertentu DPP-nya adalah nilai lain sebesar 11/12 dari harga jual, sehingga PPN efektif tetap 11% dari harga."),
      ("Kapan memakai PPh 23 dan kapan PPh 4 ayat 2?", "PPh 23 untuk jasa, sewa aset selain tanah dan bangunan, dividen, bunga, royalti. PPh 4 ayat 2 (final) untuk sewa tanah dan bangunan, jasa konstruksi, pengalihan tanah bangunan, dan dividen orang pribadi tertentu."),
      ("Bagaimana jika vendor tidak punya NPWP?", "Tarif PPh 23 menjadi 100% lebih tinggi dari tarif normal. Kalkulator menerapkannya otomatis saat kotak NPWP tidak dicentang."),
      ("Apakah DPP PPh 23 termasuk PPN?", "Tidak. PPh 23 dipotong dari jumlah bruto tidak termasuk PPN. Kalkulator memisahkan DPP, PPN, dan PPh secara otomatis."),
      ("Siapa yang menyetor PPh 26 untuk vendor luar negeri?", "Pemberi penghasilan di Indonesia memotong, menyetor, dan melaporkan PPh 26. Tarif treaty hanya berlaku bila vendor menyerahkan SKD (DGT form) yang sah.")],
 crumb="Kalkulator Potput dan PPN"),
"kalkulator-penyusutan-fiskal": dict(
 title="Kalkulator Penyusutan Fiskal dan Komersial Gratis: Koreksi Fiskal, Pajak Tangguhan | FA Venus",
 desc="Kalkulator penyusutan fiskal online gratis: kelompok harta 1 sampai 4 dan bangunan, garis lurus dan saldo menurun, jadwal susut fiskal vs komersial, koreksi fiskal, dan pajak tangguhan PSAK 212.",
 h1="Kalkulator Penyusutan Fiskal vs Komersial: Jadwal Susut, Koreksi Fiskal, dan Pajak Tangguhan",
 intro=["Perusahaan menyusutkan aset dengan dua aturan sekaligus: masa manfaat ekonomis untuk laporan keuangan (komersial) dan kelompok harta menurut Undang-Undang PPh untuk SPT (fiskal). Selisih keduanya menjadi <b>koreksi fiskal</b> setiap tahun dan <b>aset atau liabilitas pajak tangguhan</b> di neraca.",
        "Kalkulator ini membuat jadwal penyusutan per aset untuk kedua versi, menghitung koreksi fiskal tahunan, dan beban pajak tangguhan sesuai PSAK 212 Pajak Penghasilan. Masukkan beberapa aset sekaligus untuk mendapatkan rekap satu perusahaan."],
 who=["<b>Staf akuntansi</b> yang menyusun daftar aset tetap dan lampiran penyusutan SPT Badan.", "<b>Perusahaan yang diaudit</b> dan harus menyajikan pajak tangguhan di laporan keuangan.",
      "<b>Pemilik usaha</b> yang membeli mesin, kendaraan, atau bangunan dan ingin tahu pengaruhnya ke pajak.", "<b>Mahasiswa dan peserta brevet</b> yang belajar penyusutan fiskal."],
 steps=["Isi nama aset, harga perolehan, tanggal perolehan, dan nilai residu komersial.", "Pilih kelompok harta fiskal (1, 2, 3, 4, atau bangunan) dan metode fiskal: garis lurus atau saldo menurun.",
        "Isi masa manfaat komersial dan metodenya.", "Baca jadwal tahunan kedua versi, koreksi fiskal, dan beban pajak tangguhan dengan tarif 22%."],
 basis=["Kelompok harta dan masa manfaat fiskal mengikuti Pasal 11 UU PPh dan PMK 72 Tahun 2023: kelompok 1 (4 tahun), 2 (8 tahun), 3 (16 tahun), 4 (20 tahun), bangunan permanen 20 tahun dan tidak permanen 10 tahun. Metode saldo menurun hanya untuk harta bukan bangunan. Pajak tangguhan dihitung dari perbedaan temporer nilai buku komersial dan fiskal dikali tarif pajak yang berlaku, sesuai PSAK 212."],
 faq=[("Apa beda penyusutan fiskal dan komersial?", "Komersial mengikuti estimasi masa manfaat ekonomis dan metode yang dipilih manajemen sesuai PSAK 216. Fiskal mengikuti kelompok harta dan tarif yang ditetapkan UU PPh. Selisihnya dikoreksi di SPT."),
      ("Aset saya masuk kelompok berapa?", "Daftar jenis harta per kelompok ada di lampiran PMK 72 Tahun 2023. Secara umum komputer dan peralatan kantor kelompok 1, kendaraan dan mesin ringan kelompok 2, mesin berat kelompok 3 dan 4, bangunan permanen 20 tahun."),
      ("Apa itu pajak tangguhan dan kenapa muncul?", "Pajak tangguhan adalah pajak yang akan dibayar atau dipulihkan di masa depan akibat perbedaan temporer antara nilai buku komersial dan fiskal. Penyusutan adalah sumber perbedaan temporer paling umum."),
      ("Bisakah mengubah metode penyusutan fiskal di tengah jalan?", "Perubahan metode fiskal harus konsisten dan memerlukan persetujuan Direktur Jenderal Pajak. Kalkulator mengasumsikan metode tetap sepanjang masa manfaat."),
      ("Bagaimana dengan revaluasi aset?", "Revaluasi mengubah dasar penyusutan komersial, dan bila diajukan untuk fiskal dikenai PPh final. Lihat artikel Revaluasi Aset Tetap PSAK 216 dan Pajak di Eksplor.")],
 crumb="Kalkulator Penyusutan Fiskal"),
"kalkulator-cicilan-pinjaman": dict(
 title="Kalkulator Cicilan Pinjaman Usaha Gratis: Anuitas, Flat, Efektif, Bunga Sesungguhnya | FA Venus",
 desc="Kalkulator cicilan pinjaman online gratis: angsuran anuitas, efektif, dan flat, tabel amortisasi, provisi dan biaya admin, bunga efektif sesungguhnya (APR), serta plafon maksimal dari kemampuan bayar DSCR.",
 h1="Kalkulator Cicilan Pinjaman: Anuitas, Flat, Efektif, dan Bunga yang Sebenarnya Anda Bayar",
 intro=["Bunga 10% flat tidak sama dengan bunga 10% efektif. Kalkulator ini menampilkan angsuran bulanan untuk ketiga metode, tabel amortisasi pokok dan bunga, serta <b>bunga efektif sesungguhnya</b> setelah memperhitungkan provisi, biaya administrasi, dan asuransi, sehingga penawaran dari beberapa bank bisa dibandingkan dengan adil.",
        "Ada juga mode terbalik: masukkan kemampuan bayar bulanan dari arus kas usaha (DSCR 1,25 kali), dan kalkulator menghitung plafon maksimal yang aman diambil pada bunga dan tenor tertentu."],
 who=["<b>Pemilik usaha</b> yang membandingkan penawaran KMK, kredit investasi, KUR, atau multifinance.", "<b>Debitur</b> yang ingin tahu porsi pokok dan bunga tiap bulan, dan sisa pokok bila ingin melunasi dipercepat.",
      "<b>RM bank dan marketing pembiayaan</b> yang butuh simulasi cepat untuk calon debitur.", "<b>Karyawan</b> yang menghitung cicilan KPR, KKB, atau pinjaman koperasi."],
 steps=["Isi plafon, suku bunga per tahun, tenor, dan metode bunga sesuai penawaran bank.", "Isi provisi, biaya admin, dan asuransi bila ada, agar bunga efektif sesungguhnya terhitung.",
        "Baca angsuran bulanan, total bunga, dan tabel amortisasi. Geser ke mode Plafon Maksimal untuk hitung dari kemampuan bayar.", "Simpan ringkasan untuk dibandingkan dengan penawaran bank lain."],
 basis=["Anuitas: angsuran tetap, porsi bunga menurun dan pokok naik, dihitung dari bunga efektif atas sisa pokok. Efektif (sliding): pokok tetap, bunga dari sisa pokok, angsuran menurun. Flat: bunga dari plafon awal sepanjang tenor, sehingga bunga efektifnya kira-kira 1,8 sampai 1,9 kali tarif flat. Bunga efektif sesungguhnya dihitung dengan IRR arus kas pinjaman setelah biaya di muka. Batas DSCR 1,25 kali adalah praktik analis kredit, bukan peraturan."],
 faq=[("Kenapa bunga flat terlihat murah tapi mahal?", "Karena bunga flat dihitung dari plafon awal walaupun pokoknya sudah berkurang tiap bulan. Bunga flat 6% per tahun kurang lebih setara bunga efektif 11% sampai 12%."),
      ("Apa itu bunga efektif sesungguhnya (APR)?", "Tingkat bunga yang membuat nilai kini seluruh angsuran sama dengan dana bersih yang diterima setelah provisi dan biaya. Angka ini yang adil untuk membandingkan antar bank."),
      ("Berapa cicilan yang aman untuk usaha?", "Praktik umum bank: total angsuran pokok dan bunga setahun tidak lebih dari 80% EBITDA (DSCR minimal 1,25 kali). Kalkulator menghitung plafon maksimal dari batas ini."),
      ("Bagaimana jika ingin melunasi lebih cepat?", "Tabel amortisasi menunjukkan sisa pokok di bulan mana pun. Tambahkan penalti pelunasan dipercepat sesuai perjanjian kredit untuk mendapat angka pelunasan."),
      ("Apakah kalkulator ini untuk KPR juga?", "Bisa, karena rumus anuitas dan efektifnya sama. Untuk kredit usaha, lanjutkan ke Cek Kapasitas Kredit agar melihat DSCR dan plafon yang bank setujui.")],
 crumb="Kalkulator Cicilan Pinjaman"),
"kalkulator-valuasi-dcf": dict(
 title="Kalkulator Valuasi DCF dan WACC Gratis: Nilai Perusahaan, Terminal Value, Sensitivitas | FA Venus",
 desc="Kalkulator valuasi DCF online gratis: WACC dengan CAPM, proyeksi free cash flow 5 tahun, nilai terminal, enterprise value ke equity value, nilai per saham, dan tabel sensitivitas WACC vs pertumbuhan.",
 h1="Kalkulator Valuasi DCF dan WACC: Hitung Nilai Perusahaan untuk Investor, Jual Beli Saham, dan IPO",
 intro=["Berapa nilai wajar perusahaan Anda? Metode <b>discounted cash flow (DCF)</b> menghitungnya dari arus kas bebas yang diproyeksikan, didiskonto dengan biaya modal rata-rata tertimbang (<b>WACC</b>). Kalkulator ini memandu dari asumsi pertumbuhan, margin EBITDA, capex, dan modal kerja sampai ke nilai ekuitas dan nilai per saham.",
        "Tabel sensitivitas WACC terhadap pertumbuhan terminal membantu melihat rentang nilai, bukan satu angka, sehingga negosiasi dengan investor, pembeli, atau penjamin emisi punya dasar yang jelas."],
 who=["<b>Pemilik usaha</b> yang akan menawarkan saham ke investor atau menjual sebagian perusahaan.", "<b>Investor dan analis</b> yang menilai target investasi atau akuisisi.",
      "<b>Perusahaan menuju IPO</b> yang ingin memperkirakan rentang valuasi sebelum berbicara dengan sekuritas.", "<b>Mahasiswa dan praktisi keuangan</b> yang belajar DCF dan WACC dengan angka nyata."],
 steps=["Isi pendapatan tahun dasar, pertumbuhan 5 tahun, margin EBITDA, tarif pajak, capex, dan perubahan modal kerja.", "Isi parameter WACC: suku bunga bebas risiko, beta, premi risiko pasar, biaya utang, dan porsi utang terhadap ekuitas.",
        "Isi pertumbuhan terminal (biasanya 2% sampai 4%) dan utang bersih untuk mendapat nilai ekuitas.", "Baca enterprise value, equity value, nilai per saham, dan tabel sensitivitas."],
 basis=["FCFF = EBIT x (1 - tarif pajak) + penyusutan - capex - kenaikan modal kerja. WACC = porsi ekuitas x biaya ekuitas (CAPM: Rf + beta x premi risiko pasar) + porsi utang x biaya utang x (1 - tarif pajak). Nilai terminal memakai Gordon growth: FCFF tahun ke-6 dibagi (WACC - g). Equity value = enterprise value dikurangi utang berbunga ditambah kas. Untuk perusahaan swasta, premi ukuran dan premi likuiditas sering ditambahkan ke biaya ekuitas."],
 faq=[("Apa beda enterprise value dan equity value?", "Enterprise value adalah nilai seluruh operasi perusahaan untuk pemberi utang dan pemegang saham. Equity value adalah bagian pemegang saham, yaitu enterprise value dikurangi utang bersih."),
      ("Berapa WACC yang wajar untuk perusahaan Indonesia?", "Untuk perusahaan menengah swasta umumnya 12% sampai 18%, tergantung sektor, struktur utang, dan premi risiko. Perusahaan besar tercatat bisa di bawah itu. Kalkulator menampilkan sensitivitas agar Anda melihat dampak tiap asumsi."),
      ("Kenapa nilai terminal mendominasi hasil DCF?", "Karena nilai terminal mewakili seluruh arus kas setelah tahun ke-5. Porsi 60% sampai 80% dari nilai total adalah hal biasa, sehingga asumsi pertumbuhan terminal harus konservatif."),
      ("Apakah hasil DCF bisa dipakai untuk transaksi?", "Sebagai dasar diskusi, ya. Untuk transaksi resmi, kredit, atau IPO, laporan penilaian dari KJPP berizin tetap diperlukan. Tim FA membantu menyiapkan model dan mendampingi sampai penilai."),
      ("Bagaimana valuasi untuk rumah sakit?", "Pakai Kalkulator Valuasi Rumah Sakit yang memakai EBITDA x multiple dan nilai aset, dengan penyesuaian kerja sama BPJS.")],
 crumb="Kalkulator Valuasi DCF"),
"kalkulator-rasio-keuangan": dict(
 title="Kalkulator Rasio Keuangan Gratis: Likuiditas, DER, DSCR, ROE, Altman Z-Score | FA Venus",
 desc="Kalkulator rasio keuangan online gratis: current ratio, quick ratio, DER, utang/EBITDA, DSCR, margin, ROA, ROE, perputaran piutang dan persediaan, cash conversion cycle, dan Altman Z''-Score dengan indikator sehat atau tidak.",
 h1="Kalkulator Rasio Keuangan: Cek Kesehatan Keuangan Perusahaan dan Altman Z-Score",
 intro=["Masukkan angka neraca dan laba rugi, dan kalkulator ini langsung menampilkan belasan rasio yang dipakai bank, investor, dan auditor: <b>likuiditas</b> (current ratio, quick ratio), <b>solvabilitas</b> (DER, utang terhadap EBITDA, DSCR), <b>profitabilitas</b> (margin kotor, margin EBITDA, ROA, ROE), <b>aktivitas</b> (perputaran piutang, persediaan, utang usaha, cash conversion cycle), dan <b>Altman Z''-Score</b> untuk perusahaan non publik.",
        "Setiap rasio diberi indikator warna berdasarkan batas yang lazim dipakai analis kredit, sehingga Anda tahu mana yang perlu dibenahi sebelum mengajukan kredit atau bertemu investor."],
 who=["<b>Pemilik dan direktur keuangan</b> yang ingin membaca laporan keuangannya sendiri.", "<b>Perusahaan yang akan mengajukan kredit</b> dan ingin tahu rasio yang akan dihitung analis bank.",
      "<b>Auditor dan konsultan</b> untuk prosedur analitis awal.", "<b>Mahasiswa akuntansi dan manajemen keuangan</b> untuk tugas analisis laporan keuangan."],
 steps=["Isi angka dari neraca: aset lancar, kas, piutang, persediaan, total aset, utang lancar, utang berbunga, ekuitas.", "Isi angka dari laba rugi: pendapatan, HPP, EBITDA, beban bunga, laba bersih, serta angsuran pokok setahun.",
        "Baca rasio per kelompok dengan indikator hijau, kuning, merah.", "Perbaiki angka yang merah, lalu simulasikan ulang. Lanjutkan ke Cek Kapasitas Kredit untuk melihat plafon."],
 basis=["Batas indikator mengikuti praktik analis kredit: current ratio di atas 1,2, DER di bawah 2,5 kali, utang berbunga terhadap EBITDA di bawah 3,5 kali, DSCR di atas 1,25 kali. Altman Z''-Score (versi non manufaktur dan perusahaan tertutup): zona aman di atas 2,6, abu-abu 1,1 sampai 2,6, bahaya di bawah 1,1. Cash conversion cycle = hari piutang + hari persediaan - hari utang usaha. Batas ini bukan peraturan dan bisa berbeda antar bank dan sektor."],
 faq=[("Rasio apa yang paling dilihat bank?", "DSCR, DER atau utang terhadap EBITDA, current ratio, dan tren margin. Bank juga melihat kualitas piutang dan persediaan lewat hari perputarannya."),
      ("Apa itu Altman Z-Score dan apakah berlaku untuk UMKM?", "Altman Z-Score memprediksi risiko kesulitan keuangan dari lima rasio. Versi Z'' dirancang untuk perusahaan tertutup dan non manufaktur, sehingga bisa dipakai sebagai indikator awal untuk perusahaan menengah di Indonesia."),
      ("DER saya 3 kali, apakah pasti ditolak bank?", "Tidak pasti, tetapi perlu penjelasan. Bank melihat jenis utang, jaminan, dan arus kas. Rasio tinggi karena utang pemegang saham sering bisa dinetralkan dengan subordinasi."),
      ("Berapa cash conversion cycle yang sehat?", "Tergantung sektor. Ritel bisa mendekati nol atau negatif, distributor 30 sampai 60 hari, kontraktor lebih panjang. Yang penting trennya tidak memburuk."),
      ("Apakah data keuangan saya dikirim ke server?", "Tidak. Semua perhitungan di browser Anda. Angka hanya dikirim bila Anda menekan tombol kirim ke WhatsApp untuk diskusi.")],
 crumb="Kalkulator Rasio Keuangan"),
}
nv = 0
for slug, c in VENUS.items():
    p = P(slug, "index.html"); t = re.sub(r"<!--fa-prod-->.*?<!--/fa-prod-->", "", rd(p), flags=re.S)
    c["desc"] = SHORT[slug]
    t = set_title(t, c["title"], c["desc"])
    # judul utama h2 pertama di main jadi h1
    i = t.find("<main>"); m = re.search(r"<h2>(.*?)</h2>", t[i:], re.S)
    if m and "<h1" not in t[i:]:
        t = t[:i + m.start()] + f"<h1 style=\"font-family:var(--f-display);font-weight:400;font-size:clamp(24px,3vw,30px);line-height:1.15;margin:0\">{m.group(1)}</h1>" + t[i + m.end():]
    url = D + f"/{slug}/"
    t = set_ld(t, app_ld(url, c["h1"].split(":")[0], c["desc"], c["faq"], c["crumb"]))
    t = add_css(t)
    blk = seo_block(c["h1"], c["intro"], c["who"], c["steps"], c["basis"], c["faq"], f"/{slug}/", h1_tag="h2")
    k = t.rfind("</div></main>")
    t = t[:k] + blk + t[k:]
    wtxt(p, t); nv += 1

# ====================== 2. FA Jupiter, FA Saturn, Cek PSAK 118 ======================
APPS = {
JUP: dict(url=D + "/audit-ready/", cur="/audit-ready/", cat="BusinessApplication",
 title="FA Jupiter: Aplikasi Laporan Keuangan Audit Ready dari General Ledger, CALK, Kertas Kerja | FA Indonesia",
 desc="Aplikasi laporan keuangan audit ready gratis dicoba: upload COA dan GL dari Accurate, Jurnal, atau Xero, jurnal penyesuaian, trial balance, neraca, laba rugi, arus kas, CALK, lead schedule, checklist PBC, dan kalkulator industri rumah sakit, konstruksi, BPR, manufaktur.",
 h1="FA Jupiter: Dari General Ledger ke Laporan Keuangan dan CALK yang Siap Diaudit",
 intro=["Setiap tahun perusahaan menyerahkan laporan keuangan ke auditor, lalu menghabiskan berminggu-minggu menjawab permintaan data dan memperbaiki penyajian. FA Jupiter membalik urutannya: upload <b>chart of accounts dan general ledger</b> dari Accurate, Jurnal, Xero, atau Excel, buat jurnal penyesuaian, dan aplikasi menyusun <b>trial balance, neraca, laba rugi, arus kas, perubahan ekuitas, dan CALK</b> dengan format yang biasa diminta kantor akuntan publik.",
        "Yang membedakan dari software akuntansi biasa: FA Jupiter membuat <b>lead schedule dan kertas kerja per akun</b>, menandai cek silang yang belum seimbang, dan menyiapkan <b>checklist PBC</b> (prepared by client) sehingga auditor datang ke data yang sudah rapi. Semua fitur bisa dicoba gratis dengan data contoh maupun data Anda sendiri."],
 who=["<b>Perusahaan yang pertama kali diaudit</b>: bank, investor, tender, atau laporan tahunan PT mensyaratkan laporan audited.", "<b>Tim keuangan PT dan CV</b> yang ingin memangkas waktu audit dan jumlah temuan.",
      "<b>Kantor jasa akuntan (KJA) dan konsultan</b> yang menyusun laporan keuangan untuk banyak klien.", "<b>Rumah sakit, kontraktor, BPR, dan manufaktur</b> yang perlu kalkulator industri khusus: klaim BPJS, obat multi gudang, pendapatan kontrak, kolektibilitas, HPP."],
 steps=["Pilih standar yang dipakai: SAK EMKM, SAK EP, atau PSAK (SAK Umum). Aplikasi menyesuaikan format laporan dan pengungkapan CALK.", "Upload COA dan GL (CSV atau Excel), atau mulai dari data contoh untuk melihat alurnya.",
        "Buat jurnal penyesuaian: akrual, penyusutan, cadangan, reklasifikasi. Trial balance dan laporan keuangan ter-update otomatis.", "Periksa tab Ringkasan untuk cek silang, lalu buka CALK dan Lead Schedule. Simpan proyek ke Google Drive Anda sendiri."],
 basis=["Format laporan dan pengungkapan mengikuti SAK EMKM, SAK EP, dan PSAK dengan penomoran SAK Indonesia yang berlaku sesuai SAK Online IAI. Lead schedule, asersi, dan checklist PBC disusun mengikuti cara KAP menilai risiko dan meminta bukti. Data diolah dan disimpan di browser atau di Google Drive milik Anda, tidak di server FA."],
 faq=[("Apakah FA Jupiter gratis?", "Ya, semua fitur bisa dicoba gratis dengan data contoh maupun data perusahaan Anda, dan hasil ringkasnya selalu gratis."),
      ("Software akuntansi apa yang didukung?", "Accurate, Jurnal, Xero, dan file Excel atau CSV dari sistem lain. Yang dibutuhkan hanya daftar akun dan buku besar per periode."),
      ("Apa itu laporan keuangan audit ready?", "Laporan yang sudah lengkap komponennya, saldo awalnya cocok, akun-akunnya didukung rincian dan rekonsiliasi, serta CALK-nya memuat kebijakan akuntansi dan pengungkapan wajib, sehingga auditor bisa langsung menguji bukti tanpa membereskan pembukuan dulu."),
      ("Apakah data perusahaan saya aman?", "Data diolah di browser dan disimpan di penyimpanan browser atau Google Drive akun Anda sendiri. Tidak ada data yang dikirim ke server FA Indonesia."),
      ("Apakah KJA atau konsultan boleh memakainya untuk banyak klien?", "Boleh. Banyak proyek bisa disimpan di Google Drive yang sama. Untuk kebutuhan tim besar, gunakan tombol WhatsApp."),
      ("Apakah hasilnya menggantikan auditor?", "Tidak. FA Jupiter menyiapkan laporan dan kertas kerja dari sisi perusahaan. Opini audit tetap diberikan oleh KAP yang independen, misalnya KAP mitra di jaringan FA Indonesia.")],
 crumb="FA Jupiter Audit Ready", h1_tag="h1", steps_h="Cara Memakai FA Jupiter", basis_h="Standar dan Keamanan Data"),
SAT: dict(url=D + "/saturn/", cur="/saturn/", cat="BusinessApplication",
 title="FA Saturn: Software Kertas Kerja Audit untuk KAP, Materialitas, Risk Assessment, Sign-off | FA Indonesia",
 desc="Software audit untuk kantor akuntan publik, gratis dicoba: template kertas kerja enam industri, Complex dan Non-Complex Entity, materialitas, walkthrough dan test of control, Combined Risk Assessment, program audit, sign-off berjenjang, dan tim KAP di Google Drive.",
 h1=None,
 intro=["<b>FA Saturn</b> adalah ruang kerja audit berbasis browser untuk <b>kantor akuntan publik</b> kecil dan menengah yang selama ini masih mengelola kertas kerja di Excel dan folder terpisah. Satu engagement memuat penerimaan klien, pemahaman entitas, materialitas, penilaian risiko, program audit per siklus, kertas kerja substantif, sampai sign-off berjenjang dari junior, senior, manajer, hingga partner.",
        "Template disediakan untuk enam industri (jasa, dagang, manufaktur, konstruksi, rumah sakit, dan BPR) dengan pembeda <b>Complex Entity</b> dan <b>Non-Complex Entity</b> sesuai SMM 1 dan SA 315. File engagement disimpan di Google Drive KAP sendiri sehingga tim bisa bekerja bersama tanpa server tambahan."],
 who=["<b>KAP kecil dan menengah</b> yang ingin kertas kerja seragam antar tim dan antar klien.", "<b>Partner dan manajer</b> yang perlu melihat progres dan review notes semua engagement dalam satu layar.",
      "<b>Auditor junior dan senior</b> yang butuh program audit dan template kertas kerja per siklus.", "<b>Perusahaan yang diaudit</b> untuk mode klien: mengisi checklist PBC dan upload dokumen ke folder engagement."],
 steps=["Buka demo dengan memilih industri dan peran (partner, manajer, senior, junior, klien).", "Isi penerimaan klien dan pemahaman entitas, tentukan materialitas keseluruhan, performance materiality, dan ambang salah saji.",
        "Jalankan walkthrough dan test of control, lalu Combined Risk Assessment per asersi menghasilkan program audit substantif.", "Kerjakan kertas kerja, sign-off berjenjang, dan arsipkan engagement ke Google Drive KAP."],
 basis=["Alur mengikuti Standar Audit (SA 200 sampai SA 810), SMM 1 dan SMM 2 edisi IAPI yang berlaku, serta penomoran SAK Indonesia sesuai SAK Online IAI untuk asersi dan pengungkapan. Ringkasan metodologinya ada di halaman Metodologi FA Saturn dan di UpdateSAK bagian Standar Audit."],
 faq=[("Apakah FA Saturn gratis?", "Demo dan semua template bisa dicoba gratis di browser. Untuk mencoba engagement nyata bersama tim dengan penyimpanan Google Drive KAP, hubungi tim FA lewat tombol WhatsApp."),
      ("Apa beda Complex dan Non-Complex Entity?", "Non-Complex Entity (entitas tidak kompleks) punya struktur sederhana, transaksi rutin, dan kontrol yang mudah dipahami, sehingga prosedur bisa disederhanakan sesuai SA. Template FA Saturn menyesuaikan kedalaman walkthrough dan program audit untuk keduanya."),
      ("Bisakah dipakai untuk audit BPR dan rumah sakit?", "Bisa. Keduanya punya template khusus: BPR dengan siklus kredit dan kolektibilitas, rumah sakit dengan pendapatan klaim BPJS, obat multi gudang, dan jasa medis."),
      ("Di mana file engagement disimpan?", "Di folder Google Drive milik KAP, bukan di server FA. Partner mengatur siapa yang bisa membuka engagement tertentu."),
      ("Apakah mendukung review berjenjang dan review notes?", "Ya. Tiap kertas kerja punya status disiapkan, direview senior, manajer, dan partner, dengan catatan review yang harus dijawab sebelum sign-off."),
      ("Apakah sesuai SMM 1 untuk sistem manajemen mutu KAP?", "FA Saturn membantu bagian dokumentasi engagement dan pemantauan mutu. Kebijakan SMM 1 KAP tetap disusun oleh KAP; template kebijakannya tersedia di Materi UpdateSAK.")],
 crumb="FA Saturn Audit Workspace", h1_tag="h2", steps_h="Cara Mencoba FA Saturn", basis_h="Standar yang Dirujuk"),
VEN: dict(url=D + "/cek-psak-118/", cur="/cek-psak-118/", cat="FinanceApplication",
 title="Konverter Laporan Laba Rugi PSAK 201 ke PSAK 118 Gratis: Kategori, Subtotal, MPM | FA Venus",
 desc="Kalkulator gratis untuk mengubah laporan laba rugi format PSAK 201 menjadi format PSAK 118 (adopsi IFRS 18) yang berlaku 1 Januari 2027: kategori operasi, investasi, pendanaan, subtotal laba operasi dan laba sebelum pendanaan dan pajak, rekonsiliasi MPM, download Excel.",
 h1="Konverter PSAK 118: Ubah Laba Rugi PSAK 201 ke Format PSAK 118 dalam Hitungan Menit",
 intro=["<b>PSAK 118 Penyajian dan Pengungkapan dalam Laporan Keuangan</b> (adopsi IFRS 18) berlaku untuk periode yang dimulai 1 Januari 2027 dan menggantikan PSAK 201. Perubahan paling terasa ada di laporan laba rugi: setiap pos harus masuk kategori <b>operasi, investasi, atau pendanaan</b>, dan ada subtotal wajib <b>laba operasi</b> serta <b>laba sebelum pendanaan dan pajak penghasilan</b>.",
        "Konverter ini menerima laba rugi format sekarang, memetakan tiap pos ke kategori PSAK 118, menyusun subtotal baru, dan membuat rekonsiliasi <b>management-defined performance measures (MPM)</b> seperti EBITDA yang disesuaikan. Hasilnya bisa dipakai sebagai laporan proforma 2026 untuk didiskusikan dengan auditor dan komite audit sebelum tahun pertama penerapan."],
 who=["<b>Perusahaan tercatat dan calon emiten</b> yang harus menyajikan komparatif PSAK 118 mulai laporan 2027.", "<b>Perusahaan yang diaudit</b> dan ingin tahu seberapa besar perubahan laporannya sebelum ditanya auditor.",
      "<b>Akuntan, auditor, dan analis kredit</b> yang perlu melihat laba operasi versi PSAK 118 untuk perbandingan antar perusahaan.", "<b>Dosen dan mahasiswa</b> yang mempelajari IFRS 18 dengan contoh laporan nyata."],
 steps=["Isi atau tempel pos-pos laba rugi format PSAK 201: pendapatan, HPP, beban usaha, pendapatan dan beban lain, bunga, pajak.", "Tentukan aktivitas utama perusahaan (umum, investasi, atau pembiayaan) karena klasifikasi beberapa pos bergantung pada itu.",
        "Periksa pemetaan tiap pos ke kategori operasi, investasi, pendanaan; ubah bila perlu.", "Baca laporan versi PSAK 118, rekonsiliasi MPM, dan download Excel untuk didiskusikan dengan auditor."],
 basis=["Kategori dan subtotal mengikuti PSAK 118 (DSAK IAI, adopsi IFRS 18). Laba operasi mencakup semua penghasilan dan beban yang tidak masuk kategori investasi, pendanaan, pajak, dan operasi yang dihentikan. Pos investasi: hasil dari aset yang menghasilkan imbal hasil secara terpisah (misalnya investasi asosiasi, properti investasi). Pos pendanaan: liabilitas dari transaksi pendanaan dan bunga lainnya. MPM wajib direkonsiliasi ke subtotal terdekat di laporan keuangan dan diungkapkan dalam satu catatan."],
 faq=[("Kapan PSAK 118 mulai berlaku?", "Untuk periode laporan yang dimulai pada atau setelah 1 Januari 2027, dengan komparatif 2026 disajikan ulang. Penerapan dini diperbolehkan."),
      ("Apa yang berubah di laporan laba rugi?", "Pos dikelompokkan ke kategori operasi, investasi, dan pendanaan; ada subtotal wajib laba operasi dan laba sebelum pendanaan dan pajak; ukuran kinerja yang didefinisikan manajemen (MPM) harus direkonsiliasi dan diungkapkan."),
      ("Apakah EBITDA masih boleh ditampilkan?", "Boleh sebagai MPM, tetapi harus direkonsiliasi ke subtotal PSAK 118 terdekat, dijelaskan cara hitungnya, dan konsisten antar periode."),
      ("Apakah PSAK 118 berlaku untuk UMKM dan SAK EP?", "Tidak. PSAK 118 bagian dari SAK Umum (PSAK). Entitas yang memakai SAK EP atau SAK EMKM mengikuti standarnya masing-masing. Cek kerangka SAK Anda di Kalkulator PSAK UpdateSAK."),
      ("Bagaimana memulai implementasi PSAK 118 di perusahaan?", "Mulai dari pemetaan akun ke kategori baru, tentukan MPM, susun laporan proforma 2026, lalu diskusikan dengan auditor. Tim FA menyediakan jasa implementasi PSAK 118 untuk mendampingi seluruh tahapan.")],
 crumb="Konverter PSAK 118", h1_tag="h1", steps_h="Cara Memakai Konverter", basis_h="Dasar Klasifikasi"),
}
na = 0
for path, c in APPS.items():
    c["desc"] = SHORT[c["cur"].strip("/")]
    t = re.sub(r"<!--fa-prod-->.*?<!--/fa-prod-->", "", rd(path), flags=re.S)
    t = set_title(t, c["title"], c["desc"])
    name = (c["h1"] or c["title"]).split(":")[0]
    t = set_ld(t, app_ld(c["url"], name, c["desc"], c["faq"], c["crumb"], cat=c["cat"]))
    t = add_css(t)
    blk = seo_block(c["h1"] or c["title"].split(" | ")[0], c["intro"], c["who"], c["steps"], c["basis"], c["faq"], c["cur"],
                    h1_tag=c["h1_tag"], steps_h=c["steps_h"], basis_h=c["basis_h"])
    blk = f'<div class="wrap">{blk}</div>'
    k = t.find("</main>") + len("</main>")
    t = t[:k] + blk + t[k:]
    wtxt(path, t); na += 1

# ====================== 3. grid link silang di alat lain ======================
ng = 0
for h, n, k, g in TOOLS:
    if h.startswith("http") or h.strip("/") in VENUS or h in ("/audit-ready/", "/saturn/", "/cek-psak-118/"): continue
    p = P(*h.strip("/").split("/"), "index.html")
    if not os.path.exists(p): continue
    t = re.sub(r"<!--fa-prod-g-->.*?<!--/fa-prod-g-->", "", rd(p), flags=re.S)
    t = add_css(t)
    blk = f'<!--fa-prod-g--><div class="wrap">{grid(h)}</div><!--/fa-prod-g-->'
    i = t.rfind("</main>")
    if i < 0: continue
    t = t[:i] + blk + t[i:]; wtxt(p, t); ng += 1

# ====================== 4. hub ======================
def tool_cards(group=None, hrefs=None):
    sel = [x for x in TOOLS if (group and x[3] == group) or (hrefs and x[0] in hrefs)]
    return ('<div class="fpg" style="grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:10px 0 24px">'
            + "".join(f'<a href="{h}"{" target=_blank rel=noopener" if h.startswith("http") else ""} style="padding:14px 16px;border:1px solid #333;border-radius:10px;background:#1e1e1e;text-decoration:none;color:#fff;display:flex;flex-direction:column;gap:3px"><b style="font-weight:500">{E(n)}</b><span style="color:#a8a8a8;font-size:13px">{E(k)}</span></a>'
                      for h, n, k, g in sel) + "</div>"), sel
def hub_page(path, eyebrow, h1, lead, body, faq, title, desc, crumb, items, lang="id"):
    desc = SHORT[path]
    url = D + path
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url, "name": h1, "description": desc, "url": url, "inLanguage": lang, "isPartOf": {"@id": D + "/#website"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": (h if h.startswith("http") else D + h)} for i, (h, n, k, g) in enumerate(items)]}},
        faq_ld(faq), crumbs([("FA Indonesia", D + "/"), ("FA Apps", D + "/apps/"), (crumb, url)])]}
    hubs = " · ".join(f'<a href="{h}">{E(n)}</a>' for h, n in HUBS if h != path)
    main = (f'<section class="block">\n<div class="wrap art">\n<p class="eyebrow">{eyebrow}</p>\n'
            f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{E(h1)}</h1>\n'
            f'<p class="t" style="max-width:62em">{lead}</p>\n{body}\n<h2>{"FAQ" if lang == "en" else "Pertanyaan Umum"}</h2>\n{faq_html(faq)}\n'
            f'<p>{"Other hubs" if lang == "en" else "Hub lain"}: {hubs} · <a href="/apps/">{"All FA Apps" if lang == "en" else "Semua FA Apps"}</a> · <a href="/toko/#free">Toko FA</a> · <a href="/galaxy/">FA Galaxy</a></p>\n'
            f'{AUTHOR_BOX}\n</div>\n</section>')
    p = P(*path.strip("/").split("/"), "index.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
    t = set_main(set_head(TPL_SVC, title, desc, url, ld), main)
    if lang == "en": t = re.sub(r'<html lang="[^"]*"', '<html lang="en"', t, count=1)
    wtxt(p, t); URLS.append(path)

cards, sel = tool_cards("pajak")
hub_page("/kalkulator-pajak/", "FA Apps · Kalkulator Pajak", "Kalkulator Pajak Online Gratis 2026: PPh 21, PPh Badan, PPh 23, PPN 12%, Penyusutan Fiskal",
 "Empat kalkulator pajak FA Venus yang dipakai staf finance, HR, pemilik usaha, dan konsultan setiap hari. Gratis, tanpa daftar, data tidak dikirim ke server.",
 "<h2>Pilih Kalkulator</h2>" + cards
 + "<h2>Kenapa Kalkulator Ini Berbeda</h2><ul><li>Mengikuti aturan terbaru: PP 58/2023 dan PMK 168/2023 untuk PPh 21 TER, UU HPP untuk tarif PPh Badan 22%, PMK 131/2024 untuk PPN 12% dengan DPP 11/12, PMK 72/2023 untuk kelompok harta fiskal.</li>"
 "<li>Hasil disertai dasar hitung dan langkah, bukan hanya angka, sehingga bisa dijelaskan ke atasan, auditor, atau pemeriksa pajak.</li>"
 "<li>Dibuat oleh tim CA dan CPA FA Indonesia yang sehari-hari menyusun laporan keuangan dan rekonsiliasi pajak klien.</li></ul>"
 "<h2>Kalkulator Pajak untuk Apa Saja</h2>" + tbl(["Kebutuhan", "Kalkulator", "Hasil"], [
   ("Potongan gaji karyawan tiap bulan, THR, masa Desember", '<a href="/kalkulator-pph-21/">PPh 21 TER</a>', "Potongan per bulan, take home pay, simulasi setahun"),
   ("Pajak perusahaan setahun dan angsuran bulanan", '<a href="/kalkulator-pph-badan/">PPh Badan</a>', "PPh terutang, PPh 29, angsuran PPh 25"),
   ("Potongan di invoice vendor jasa, sewa, kontraktor, luar negeri", '<a href="/kalkulator-potput-ppn/">Potput dan PPN</a>', "PPN, PPh 23, 4(2), 26, 22, jumlah dibayar dan disetor"),
   ("Daftar aset tetap untuk SPT dan laporan keuangan", '<a href="/kalkulator-penyusutan-fiskal/">Penyusutan Fiskal</a>', "Jadwal susut fiskal dan komersial, koreksi fiskal, pajak tangguhan")])
 + '<h2>Butuh Lebih dari Kalkulator</h2><p>Rekonsiliasi SPT dengan laporan keuangan, koreksi fiskal, dan pendampingan pemeriksaan dikerjakan bersama konsultan pajak berizin mitra kami. Mulai dari <a href="https://cariakuntan.com/">cariakuntan.com</a> atau <a href="/jasa-penyusunan-laporan-keuangan/">jasa penyusunan laporan keuangan</a>. Belajar standar akuntansinya di <a href="https://updatesak.com/">UpdateSAK</a>.</p>',
 [("Apakah kalkulator pajak ini gratis dan perlu daftar?", "Gratis, tanpa daftar, tanpa kartu. Perhitungan berjalan di browser dan data tidak dikirim ke server."),
  ("Apakah hasilnya sudah aturan 2026?", "Ya. Tarif dan aturan yang dipakai dicantumkan di bagian Dasar Perhitungan tiap kalkulator dan diperbarui saat ada perubahan peraturan."),
  ("Apakah bisa dipakai untuk mengisi SPT?", "Sebagai simulasi dan pengecekan, ya. Pengisian SPT tetap mengikuti pembukuan dan bukti potong resmi di Coretax."),
  ("Siapa yang membuat kalkulator ini?", "Tim FA Indonesia, kantor financial advisory yang didukung CA dan CPA, bersama mitra KJA dan KAP.")],
 "Kalkulator Pajak Online Gratis 2026: PPh 21, PPh Badan, PPh 23, PPN 12%, Penyusutan | FA Indonesia",
 "Kalkulator pajak online gratis 2026: PPh 21 TER bulanan dan Desember, PPh Badan 22% dan final 0,5%, PPh 23, PPh 4(2), PPh 26, PPN 12% DPP 11/12, penyusutan fiskal dan pajak tangguhan. Tanpa daftar.",
 "Kalkulator Pajak", sel)

cards, sel = tool_cards("keuangan")
hub_page("/kalkulator-keuangan/", "FA Apps · Kalkulator Keuangan", "Kalkulator Keuangan Perusahaan Gratis: DSCR, Plafon Kredit, Cicilan, Rasio, Valuasi",
 "Alat hitung yang dipakai analis kredit, investor, dan CFO, dibuka untuk pemilik usaha: dari cicilan pinjaman sampai valuasi perusahaan. Gratis dan dihitung di browser Anda.",
 "<h2>Pilih Kalkulator</h2>" + cards
 + "<h2>Urutan yang Disarankan Sebelum ke Bank atau Investor</h2>" + flow([
   ("Rasio Keuangan", "Cek likuiditas, DER, margin, dan Altman Z dari laporan terakhir."), ("Cek Kapasitas Kredit", "DSCR dan plafon per bunga dan tenor, atau syarat IPO."),
   ("Cicilan dan Plafon", "Bandingkan penawaran bank dengan bunga efektif sesungguhnya."), ("Valuasi", "DCF untuk perusahaan umum, kalkulator khusus untuk rumah sakit.")])
 + "<h2>Batas yang Dipakai</h2><p>DSCR minimal 1,25 kali, utang berbunga terhadap EBITDA maksimal 3,5 kali, DER maksimal 2,5 kali, LTV agunan 70%. Ini praktik analis kredit, bukan peraturan, dan bisa berbeda antar bank dan sektor. Syarat IPO mengikuti Peraturan BEI I-A dan POJK 53/2017.</p>"
 '<h2>Setelah Angkanya Jelas</h2><p>Bila rasio belum masuk, tim FA mendampingi merapikan laporan keuangan, menyusun proposal kredit, atau menyiapkan materi investor. Lihat <a href="/konsultan-kredit-bank/">Konsultan Kredit Bank</a>, <a href="/jasa-valuasi-usaha/">Jasa Valuasi Usaha</a>, dan <a href="/konsultan-persiapan-ipo/">Konsultan IPO</a>.</p>',
 [("Kalkulator mana untuk tahu berapa plafon kredit yang bisa saya dapat?", "Mulai dari Cek Kapasitas Kredit: isi EBITDA dan angsuran berjalan, hasilnya plafon per suku bunga dan tenor. Simulasi Plafon Kredit Usaha membedakan KI, KMK, top up, dan take over."),
  ("Apakah angkanya sama dengan hitungan bank?", "Pendekatannya sama (DSCR, leverage, LTV), tetapi tiap bank punya batas dan penyesuaian sendiri. Pakai hasilnya sebagai perkiraan dan bahan diskusi dengan RM."),
  ("Apakah data perusahaan saya tersimpan?", "Tidak. Semua kalkulator berjalan di browser. Angka hanya terkirim bila Anda menekan tombol kirim ke WhatsApp atau email."),
  ("Bisakah dipakai untuk tugas kuliah atau pelatihan?", "Bisa. Tiap kalkulator mencantumkan rumus dan dasar hitung. Untuk materi standar akuntansi, lihat UpdateSAK.")],
 "Kalkulator Keuangan Perusahaan Gratis: DSCR, Plafon Kredit, Cicilan, Rasio, Valuasi DCF | FA Indonesia",
 "Kalkulator keuangan online gratis untuk perusahaan: DSCR, kapasitas dan plafon kredit, cicilan pinjaman, rasio keuangan dan Altman Z, valuasi DCF dan WACC, valuasi rumah sakit, cek kelayakan IPO. Dihitung di browser.",
 "Kalkulator Keuangan", sel)

cards, sel = tool_cards(hrefs=["/audit-ready/", "/cek-psak-118/", "https://updatesak.com/#laporan-keuangan", "https://updatesak.com/#calk", "https://updatesak.com/#kalkulator-psak", "https://cariakuntan.com/screening/"])
hub_page("/aplikasi-akuntansi-gratis/", "FA Apps · Aplikasi Akuntansi", "Aplikasi Akuntansi dan Laporan Keuangan Gratis Berbasis Web, Sesuai SAK",
 "Dari saldo akun atau general ledger sampai neraca, laba rugi, arus kas, dan CALK dengan format SAK EMKM, SAK EP, atau PSAK. Semua berjalan di browser, data tetap di tangan Anda.",
 "<h2>Pilih Aplikasi</h2>" + cards
 + "<h2>Mana yang Cocok untuk Anda</h2>" + tbl(["Situasi", "Aplikasi", "Catatan"], [
   ("Punya saldo akun, ingin laporan keuangan lengkap sesuai SAK", '<a href="https://updatesak.com/#laporan-keuangan">Penyusun Laporan Keuangan UpdateSAK</a>', "Neraca, laba rugi, arus kas, perubahan ekuitas, gratis"),
   ("Butuh CALK format auditor", '<a href="https://updatesak.com/#calk">Penyusun CALK UpdateSAK</a>', "Kebijakan akuntansi, rincian akun, pengungkapan wajib"),
   ("Punya GL dari Accurate, Jurnal, Xero, akan diaudit", '<a href="/audit-ready/">FA Jupiter Audit Ready</a>', "Jurnal penyesuaian, lead schedule, checklist PBC; gratis dicoba"),
   ("Belum tahu pakai SAK EMKM, SAK EP, atau PSAK", '<a href="https://updatesak.com/#kalkulator-psak">Kalkulator PSAK UpdateSAK</a>', "Kerangka yang tepat dan kewajiban audit"),
   ("Laba rugi harus ikut PSAK 118 mulai 2027", '<a href="/cek-psak-118/">Konverter PSAK 118</a>', "Kategori, subtotal, rekonsiliasi MPM"),
   ("Ingin tahu posisi rasio sebelum memilih KAP", '<a href="https://cariakuntan.com/screening/">Screening Instan CariAkuntan</a>', "Rasio bank dan jalur IPO dalam 3 menit")])
 + "<h2>Aplikasi Gratis vs Software Akuntansi Berlangganan</h2><p>Aplikasi di halaman ini bukan pengganti software pembukuan harian seperti Accurate atau Jurnal. Fungsinya di tahap berikutnya: mengubah saldo dan buku besar menjadi laporan keuangan yang formatnya benar, lengkap dengan CALK, dan siap diaudit atau diserahkan ke bank. Untuk pembukuan bulanan terima beres, lihat <a href=\"https://cariakuntan.com/jasa-pembukuan/\">jasa pembukuan CariAkuntan</a>.</p>",
 [("Apakah aplikasi ini benar-benar gratis?", "Ya, semua bisa dipakai gratis dan hasil ringkasnya selalu gratis. Pengguna yang terbantu bisa mendukung lewat donasi QRIS."),
  ("Apakah perlu instal atau membuat akun?", "Tidak. Semua berbasis web dan berjalan di browser laptop maupun HP. Penyimpanan proyek FA Jupiter memakai Google Drive akun Anda sendiri."),
  ("Format laporannya sesuai standar apa?", "SAK EMKM, SAK EP, dan PSAK (SAK Umum) dengan penomoran SAK Indonesia yang berlaku sesuai SAK Online IAI."),
  ("Apakah laporannya bisa langsung diaudit KAP?", "Laporan yang dihasilkan sudah mengikuti format dan pengungkapan yang diminta auditor. Opini audit tetap diberikan KAP independen; FA Indonesia bermitra dengan KAP DHN & Rekan.")],
 "Aplikasi Akuntansi dan Laporan Keuangan Gratis Berbasis Web Sesuai SAK (EMKM, EP, PSAK) | FA Indonesia",
 "Aplikasi akuntansi gratis berbasis web: penyusun laporan keuangan dan CALK sesuai SAK EMKM, SAK EP, PSAK, FA Jupiter audit ready dari general ledger, kalkulator PSAK, konverter PSAK 118. Tanpa instal, data di browser Anda.",
 "Aplikasi Akuntansi Gratis", sel)

cards, sel = tool_cards(hrefs=["/saturn/", "/audit-ready/", "https://updatesak.com/#calk", "https://cariakuntan.com/screening/"])
hub_page("/aplikasi-audit-kap/", "FA Apps · Audit", "Aplikasi dan Software Audit untuk KAP: Kertas Kerja, Materialitas, Risk Assessment, Audit Ready",
 "Dua sisi meja audit dalam satu ekosistem: FA Saturn untuk kantor akuntan publik yang mengelola engagement, FA Jupiter untuk perusahaan yang menyiapkan laporan keuangan audit ready.",
 "<h2>Pilih Aplikasi</h2>" + cards
 + "<h2>Untuk Kantor Akuntan Publik</h2><p><a href=\"/saturn/\">FA Saturn</a> mengganti kumpulan file Excel dan folder yang tersebar dengan satu ruang kerja: penerimaan klien, materialitas, walkthrough dan test of control, Combined Risk Assessment, program audit per siklus, kertas kerja substantif, review notes, dan sign-off berjenjang sampai partner. Template untuk jasa, dagang, manufaktur, konstruksi, rumah sakit, dan BPR, dengan pembeda Complex dan Non-Complex Entity. File engagement disimpan di Google Drive KAP sendiri.</p>"
 "<h2>Untuk Perusahaan yang Diaudit</h2><p><a href=\"/audit-ready/\">FA Jupiter</a> mengubah general ledger menjadi trial balance, laporan keuangan, CALK, lead schedule, dan checklist PBC, sehingga auditor datang ke data yang sudah rapi dan jumlah temuan turun. Cocok untuk audit pertama kali, syarat kredit bank, laporan tahunan PT, dan persiapan IPO.</p>"
 "<h2>Standar yang Dirujuk</h2><ul><li>Standar Audit SA 200 sampai SA 810, SMM 1 dan SMM 2 edisi IAPI yang berlaku. Ringkasannya ada di <a href=\"https://updatesak.com/standar-audit/\">UpdateSAK Standar Audit</a>.</li>"
 "<li>SAK EMKM, SAK EP, dan PSAK dengan penomoran SAK Online IAI untuk asersi dan pengungkapan.</li><li>Metodologi lengkap di <a href=\"/saturn/metodologi/\">Metodologi FA Saturn</a> dan <a href=\"/galaxy/\">FA Galaxy</a>.</li></ul>"
 "<h2>Belum Punya KAP</h2><p>Perusahaan yang baru akan diaudit bisa memetakan kebutuhan dan kelas KAP yang sesuai di <a href=\"https://cariakuntan.com/\">cariakuntan.com</a>, atau langsung ke <a href=\"/kap-dhn/\">KAP DHN &amp; Rekan</a>, KAP mitra di jaringan FA.</p>",
 [("Apakah FA Saturn bisa dipakai KAP kecil dengan 2 sampai 5 staf?", "Justru untuk itu dirancang. Tidak perlu server, file di Google Drive KAP, dan template sudah siap untuk enam industri."),
  ("Apakah kertas kerjanya memenuhi SA 230 tentang dokumentasi audit?", "Struktur kertas kerja, referensi silang, penanggung jawab, tanggal, dan review notes disusun mengikuti SA 230 dan SA 220. Kelengkapan isi tetap tanggung jawab tim audit."),
  ("Apa beda FA Saturn dan FA Jupiter?", "FA Saturn dipakai auditor (KAP) untuk mengelola engagement. FA Jupiter dipakai perusahaan atau KJA untuk menyiapkan laporan keuangan yang siap diaudit. Keduanya bisa saling membaca checklist PBC."),
  ("Bagaimana mencoba bersama tim KAP?", "Buka demo FA Saturn, pilih industri dan peran, lalu gunakan tombol WhatsApp di dalamnya untuk aktivasi tim.")],
 "Software Audit untuk KAP: Kertas Kerja, Materialitas, Risk Assessment, Sign-off (FA Saturn) dan Audit Ready (FA Jupiter) | FA Indonesia",
 "Aplikasi audit untuk kantor akuntan publik: kertas kerja digital, materialitas, walkthrough, Combined Risk Assessment, program audit, sign-off berjenjang (FA Saturn), dan laporan keuangan audit ready dari GL (FA Jupiter). Gratis dicoba.",
 "Aplikasi Audit untuk KAP", sel)

# EN hub
en_items = [x for x in TOOLS if x[0] in ("/kalkulator-pph-21/", "/kalkulator-pph-badan/", "/kalkulator-potput-ppn/", "/kalkulator-penyusutan-fiskal/", "/kalkulator-dscr/", "/kalkulator-cicilan-pinjaman/", "/kalkulator-rasio-keuangan/", "/kalkulator-valuasi-dcf/", "/cek-kapasitas-kredit/", "/cek-kelayakan-ipo/", "/cek-psak-118/", "/audit-ready/")]
EN_NAMES = {"/kalkulator-pph-21/": ("Employee Income Tax (PPh 21) Calculator", "Monthly TER rates, December true-up, bonuses, gross-up"), "/kalkulator-pph-badan/": ("Corporate Income Tax (PPh Badan) Calculator", "22% rate, Article 31E relief, 0.5% final SME tax"),
  "/kalkulator-potput-ppn/": ("Withholding Tax and VAT 12% Calculator", "PPh 23, 4(2), 26, 22 and VAT on one invoice"), "/kalkulator-penyusutan-fiskal/": ("Tax Depreciation Calculator", "Fiscal vs book depreciation, deferred tax"),
  "/kalkulator-dscr/": ("DSCR Calculator", "Formula, example, bank thresholds"), "/kalkulator-cicilan-pinjaman/": ("Loan Installment Calculator", "Annuity, flat, effective, true APR"),
  "/kalkulator-rasio-keuangan/": ("Financial Ratio Calculator", "Liquidity, leverage, ROE, Altman Z"), "/kalkulator-valuasi-dcf/": ("DCF and WACC Valuation Calculator", "FCFF, terminal value, sensitivity"),
  "/cek-kapasitas-kredit/": ("Bank Loan Capacity Check", "DSCR and loan limit by rate and tenor"), "/cek-kelayakan-ipo/": ("IDX IPO Eligibility Check", "Main, Development, Acceleration boards"),
  "/cek-psak-118/": ("PSAK 118 (IFRS 18) Income Statement Converter", "Operating, investing, financing categories, MPM"), "/audit-ready/": ("FA Jupiter Audit-Ready Financial Statements", "From GL to statements, notes, lead schedules")}
en_cards = ('<div class="fpg" style="grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:10px 0 24px">'
            + "".join(f'<a href="{h}" style="padding:14px 16px;border:1px solid #333;border-radius:10px;background:#1e1e1e;text-decoration:none;color:#fff;display:flex;flex-direction:column;gap:3px"><b style="font-weight:500">{E(EN_NAMES[h][0])}</b><span style="color:#a8a8a8;font-size:13px">{E(EN_NAMES[h][1])}</span></a>' for h, n, k, g in en_items) + "</div>")
en_sel = [(h, EN_NAMES[h][0], EN_NAMES[h][1], g) for h, n, k, g in en_items]
hub_page("/en/free-tax-finance-calculators-indonesia/", "FA Apps · English", "Free Indonesian Tax, Loan, and Valuation Calculators for Companies and Expats",
 "Browser-based calculators built by FA Indonesia's CA and CPA team: Indonesian payroll tax (PPh 21), corporate tax, withholding tax and VAT, loan capacity, financial ratios, DCF valuation, and audit-ready financial statements. Interfaces are in Indonesian; this page explains what each does.",
 "<h2>Calculators</h2>" + en_cards
 + "<h2>Indonesian Tax Rules Behind the Calculators</h2><ul><li>Employee income tax (PPh 21) uses average effective rates (TER) from January to November and a December true-up at progressive rates (Government Regulation 58/2023, MoF Regulation 168/2023).</li>"
 "<li>Corporate income tax is 22%, with a 50% reduction on the portion of taxable income from gross revenue up to IDR 4.8 billion for companies with revenue up to IDR 50 billion (Article 31E), and an optional 0.5% final tax on turnover for qualifying SMEs (GR 55/2022).</li>"
 "<li>VAT is 12% on an 'other value' base of 11/12 of the selling price for non-luxury goods and services since 1 January 2025 (MoF Regulation 131/2024), so the effective rate stays 11%.</li>"
 "<li>Withholding taxes: PPh 23 (2% or 15%), PPh 4(2) final (land and building rent 10%, construction 1.75% to 6%), PPh 26 (20% or treaty rate), PPh 22 on imports.</li></ul>"
 "<h2>Who Uses These</h2><p>Finance teams of PT PMA (foreign-owned companies), expats checking payslips, lenders and investors screening Indonesian targets, and students. For statutory audit and bookkeeping in English, see <a href=\"/en/statutory-audit-indonesia/\">Statutory Audit for PT PMA</a> and <a href=\"/en/accountant-indonesia/\">Accountant and Audit Services in Indonesia</a>.</p>",
 [("Are the calculators free?", "Yes. They run in your browser, need no sign-up, and send no data to our servers. FA Jupiter can be tried for free."),
  ("Is the interface available in English?", "The calculators are in Indonesian, with field labels that are easy to follow. This page explains each tool, and our team can walk you through them in English."),
  ("Are the tax rates current?", "Each calculator lists the regulations it applies and is updated when rules change. Use results for planning; filings must follow your books and official withholding slips."),
  ("Can you help with audit or bookkeeping in English?", "Yes. Financial statements and audit reports can be issued in English and Indonesian through our partner firms. Use the WhatsApp button to start.")],
 "Free Indonesian Tax, Loan, DSCR, and Valuation Calculators | FA Indonesia",
 "Free browser-based calculators for Indonesia: employee income tax PPh 21 (TER), corporate tax 22%, withholding tax and VAT 12%, loan capacity and DSCR, financial ratios, DCF valuation, PSAK 118 converter, audit-ready statements. No sign-up.",
 "Free Calculators (EN)", en_sel, lang="en")
pe = P("en", "free-tax-finance-calculators-indonesia", "index.html"); t = rd(pe).replace("Chat Ananta, CPA", "Chat with Ananta, CPA"); wtxt(pe, t)

# ====================== 5. link hub di /apps/, /toko/, /layanan/ ======================
hub_row = ('<!--fa-prod-hub--><p style="margin:14px 0 0;font-size:13.5px;color:var(--muted,#a8a8a8)">Hub: '
           + " · ".join(f'<a href="{h}" style="color:inherit">{E(n)}</a>' for h, n in HUBS)
           + ' · <a href="/en/free-tax-finance-calculators-indonesia/" style="color:inherit">English</a></p><!--/fa-prod-hub-->')
ap = P("apps", "index.html"); t = re.sub(r"<!--fa-prod-hub-->.*?<!--/fa-prod-hub-->", "", rd(ap), flags=re.S)
t = set_title(t, "FA Apps: Kalkulator Pajak, Kalkulator Keuangan, dan Aplikasi Akuntansi Gratis | FA Indonesia")
i = t.find("</p>", t.find('<p class="lead">')) + 4; t = t[:i] + hub_row + t[i:]; wtxt(ap, t)
tp = P("toko", "index.html"); t = re.sub(r"<!--fa-prod-hub-->.*?<!--/fa-prod-hub-->", "", rd(tp), flags=re.S)
i = t.find('<h2 class="h" id="gratis">')
if i > 0:
    j = t.find("</h2>", i) + 5; t = t[:j] + hub_row + t[j:]
wtxt(tp, t)
lp = P("layanan", "index.html"); t = re.sub(r"<!--fa-prod-svc-->.*?<!--/fa-prod-svc-->", "", rd(lp), flags=re.S)
blk = ('<!--fa-prod-svc--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Gratis Dicoba</p><h2>Kalkulator Pajak, Keuangan, dan Aplikasi Akuntansi</h2></div>'
       '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn solid" href="/kalkulator-pajak/">Kalkulator Pajak</a><a class="btn line" href="/kalkulator-keuangan/">Kalkulator Keuangan</a>'
       '<a class="btn line" href="/aplikasi-akuntansi-gratis/">Aplikasi Akuntansi Gratis</a><a class="btn line" href="/aplikasi-audit-kap/">Aplikasi Audit untuk KAP</a></div></div></section><!--/fa-prod-svc-->')
i = t.find('<section class="block'); wtxt(lp, t[:i] + blk + t[i:])

# ====================== 6. sitemap, llms ======================
sm = re.sub(r"<!--fa-prod-->.*?<!--/fa-prod-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-prod-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.9</priority></url>\n" for u in URLS) + "<!--/fa-prod-->\n</urlset>")
# lastmod halaman alat yang diperbarui
for slug in list(VENUS) + ["audit-ready", "saturn", "cek-psak-118", "apps"]:
    sm = re.sub(rf"(<loc>{re.escape(D)}/{slug}/</loc>)(?:<lastmod>[^<]*</lastmod>)?", rf"\1<lastmod>{TODAY}</lastmod>", sm, count=1)
wtxt(P("sitemap.xml"), sm)
ll = re.sub(r"\n## Hub Kalkulator dan Aplikasi \(Nov 2026\).*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + "\n\n## Hub Kalkulator dan Aplikasi (Nov 2026)\n" + "".join(
    f"- [{n}]({D}{h})\n" for h, n in HUBS) + f"- [Free Indonesian tax and finance calculators (EN)]({D}/en/free-tax-finance-calculators-indonesia/)\n" + "".join(
    f"- {n}: {k} → {h if h.startswith('http') else D + h}\n" for h, n, k, g in TOOLS)
wtxt(P("llms.txt"), ll)
print("fa_produk ok: venus", nv, "apps", na, "grid", ng, "hub", URLS)
