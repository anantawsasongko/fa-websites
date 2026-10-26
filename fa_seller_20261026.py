# -*- coding: utf-8 -*-
"""FA Seller Side: listing RS dan BPR yang dijual (anonim, angka dalam kisaran) untuk SEO.
Sumber angka: HL Company Profile FA Okt 2026 (Drive, 2. FA Advisory - Seller Side). Nama RS TIDAK boleh muncul.
Halaman: /rumah-sakit-dijual/ (hub listing RS + pipeline), /bpr-dijual/ (BPR & BPRS), CTA di halaman terkait, sitemap, llms.
Idempoten. Jalankan setelah fa_kredit_20261026.py, sebelum fa_tone dan prep.py.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
exec(_src[:_src.index("# ================= 1.")])

RS = [
 dict(code="RS-01", tipe="RS Umum Kelas D", wil="Jawa Tengah", akred="Paripurna", kap="±70 kamar rawat inap",
      metrics=[("Pendapatan FY2025 (audit)", "Rp30–35 M"), ("Margin EBITDA FY2025", "±30%"), ("Aset Tetap (Nilai KJPP)", "Rp35–40 M"), ("Porsi BPJS", "±80%")],
      offer="75% saham", harga="Rp8–12 M", note="Harga 100% ekuitas di bawah nilai buku. Desain dan RAB gedung pengembangan sudah tersedia. Volume 2026 sempat tertekan pesaing baru dan mulai pulih.", status="Due diligence terbuka"),
 dict(code="RS-02", tipe="RS Umum Kelas D", wil="Pusat Kota, DI Yogyakarta", akred="Paripurna", kap="50 tempat tidur",
      metrics=[("Pendapatan FY2025 (audit)", "Rp35–40 M"), ("EBITDA FY2025", "Rp5–6 M"), ("Ekuitas", "Rp45–50 M"), ("Utang Bank / EBITDA", "<1x")],
      offer="100% saham (termasuk mayoritas klinik anak usaha)", harga="Rp45–55 M", note="Sekitar 9–10x EBITDA dan mendekati nilai buku. Persetujuan RUPSLB untuk pengalihan saham sudah ada. Rawat jalan spesialis dominan.", status="Terbuka"),
 dict(code="RS-03", tipe="RS Khusus Bedah Kelas C", wil="DI Yogyakarta", akred="Paripurna", kap="25 tempat tidur, 2 kamar operasi",
      metrics=[("Pendapatan FY2025", "Rp2–2,5 M"), ("Pertumbuhan 2023–2025", "±29% per tahun"), ("Margin EBITDA FY2025", "35–40%"), ("Utang Bank", "Nihil")],
      offer="Going concern all-in (tanah SHM, gedung, alkes, izin)", harga="Rp22–28 M", note="Niche bedah dan bedah estetik. RAB gedung 6 lantai ±Rp37 M sudah final, cocok untuk investor yang ingin ekspansi.", status="Terbuka"),
 dict(code="RS-04", tipe="RS Ibu dan Anak, Urban", wil="Kota Besar, Jawa Tengah", akred="-", kap="Renovasi fasilitas selesai bertahap",
      metrics=[("Nilai Tanah (KJPP)", "Rp35–40 M"), ("Aset Tetap Tercatat", "Rp85–90 M"), ("Pendapatan Pra-Renovasi", "Rp5–7 M"), ("Porsi Ibu dan Anak", "±70%")],
      offer="Akuisisi PT, pembelian aset, atau KSO", harga="Disampaikan setelah NDA", note="Peluang turnaround dengan lahan dalam kota dan izin RS yang sulit direplikasi.", status="Terbuka"),
]
PIPE = [
 ("Portofolio Jaringan RS", "5 rumah sakit di DI Yogyakarta dan Jawa Tengah, untuk investor strategis atau PE", "Setelah NDA"),
 ("RS Umum Lainnya", "Beberapa RS umum swasta di Jawa Barat, Jawa Tengah, dan DI Yogyakarta, data sedang dilengkapi", "Setelah NDA"),
 ("BPR Konvensional", "2 BPR di Jawa Tengah dan DI Yogyakarta", "Setelah NDA"),
 ("BPR Syariah (BPRS)", "1 BPRS dengan LOI akuisisi saham yang sudah berjalan", "Setelah NDA"),
]

CSS = ('<style id="fa-sell">.lst{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:14px;margin:18px 0 28px}'
       '.lc{border:1px solid #3a3a3a;background:#1e1e1e;padding:20px 18px;display:flex;flex-direction:column;gap:10px;animation:up .4s ease both}'
       '.lc .top{display:flex;justify-content:space-between;gap:8px;align-items:baseline;flex-wrap:wrap}.lc .cd{font:600 13px/1 Poppins,sans-serif;letter-spacing:.12em;color:#bbb}'
       '.lc .st{font:500 12px/1 Poppins,sans-serif;border:1px solid #555;padding:5px 8px;color:#ddd}'
       '.lc h3{margin:0;font-size:21px;line-height:1.25}.lc .wl{margin:0;color:#bdbdbd;font-size:14px}'
       '.lc dl{display:grid;grid-template-columns:1fr auto;gap:6px 12px;margin:4px 0;font-size:14px}.lc dt{color:#bdbdbd}.lc dd{margin:0;text-align:right;font-weight:500;white-space:nowrap}'
       '.lc .pr{border-top:1px solid #333;padding-top:10px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:baseline}'
       '.lc .pr b{font:600 22px/1.1 Poppins,sans-serif}.lc .pr small{color:#bdbdbd;font-size:12.5px}.lc .nt{font-size:13.5px;color:#d0d0d0;margin:0;line-height:1.55}'
       '.lc .btn{align-self:flex-start;margin-top:auto}@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}</style>')

def card(r):
    msg = f"Halo FA Indonesia, saya tertarik dengan listing {r['code']} ({r['tipe']}, {r['wil']}). Mohon NDA dan teaser."
    dl = "".join(f"<dt>{E(k)}</dt><dd>{E(v)}</dd>" for k, v in r["metrics"])
    return (f'<article class="lc"><div class="top"><span class="cd">{r["code"]}</span><span class="st">{E(r["status"])}</span></div>'
            f'<h3>{E(r["tipe"])}</h3><p class="wl">{E(r["wil"])} · {E(r["kap"])} {(' · Akreditasi ' + E(r['akred'])) if r['akred'] != '-' else ' · Fase Re-aktivasi'}</p>'
            f'<dl>{dl}</dl><div class="pr"><div><small>Harga Indikatif · {E(r["offer"])}</small><br><b>{E(r["harga"])}</b></div></div>'
            f'<p class="nt">{E(r["note"])}</p><a class="btn solid" href="{wa(msg)}" target="_blank" rel="noopener">Minta Teaser (NDA)</a></article>')

ALUR = flow([("NDA", "Identitas aset dibuka setelah NDA ditandatangani."), ("Teaser dan HL Profile", "Ringkasan kinerja, aset, dan struktur transaksi."),
             ("Kunjungan dan LOI", "Site visit, lalu Letter of Intent dan eksklusivitas."), ("Due Diligence", "Keuangan, legal, pajak, dan medis lewat data room."),
             ("Closing", "Perjanjian jual beli, pembayaran lewat escrow notaris, serah terima.")])
PIPE_T = tbl(["Pipeline", "Gambaran", "Indikasi Harga"], [(E(a), E(b), E(c)) for a, b, c in PIPE])

body = (f"<h2>Listing Rumah Sakit</h2><p>Nama rumah sakit kami samarkan untuk menjaga kerahasiaan penjual. Angka ditampilkan dalam kisaran dan bersumber dari laporan keuangan audit atau manajemen serta laporan penilai independen. Data lengkap dibuka di data room setelah NDA.</p>"
        f'<div class="lst">{"".join(card(r) for r in RS)}</div>'
        f"<h2>Pipeline Lain: RS, BPR, dan BPRS</h2>{PIPE_T}"
        "<p>Untuk BPR dan BPRS, lihat <a href=\"/bpr-dijual/\">BPR dan BPRS dijual</a>.</p>"
        f"<h2>Alur untuk Calon Pembeli</h2>{ALUR}"
        "<h2>Punya RS, Klinik, atau BPR yang Ingin Dijual?</h2><p>Kami menyiapkan valuasi, teaser, HL company profile, information memorandum, NDA, dan data room, lalu menjajaki pembeli strategis, grup RS, dan investor. "
        "Kami juga membantu merapikan laporan keuangan dan dokumen legal sebelum dibuka ke pembeli, supaya harga tidak tergerus temuan due diligence.</p>"
        "<h2>Bacaan Terkait</h2><ul><li><a href=\"/konsultan-rumah-sakit/\">Konsultan Rumah Sakit</a></li><li><a href=\"/artikel/indikator-keuangan-rumah-sakit-yang-dilihat-investor/\">Indikator Keuangan Rumah Sakit yang Dilihat Investor</a></li>"
        "<li><a href=\"/cek-kapasitas-kredit/\">Cek Kredit dan Pendanaan untuk Akuisisi</a></li></ul>")
FAQ = [
 ("Kenapa nama rumah sakit tidak ditampilkan?", "Untuk melindungi penjual, karyawan, dan hubungan dengan pasien serta mitra. Identitas lengkap dibuka setelah calon pembeli menandatangani NDA."),
 ("Dari mana angka di listing ini?", "Dari laporan keuangan audit atau laporan manajemen terbaru dan laporan penilai independen (KJPP). Angka ditampilkan dalam kisaran dan diverifikasi saat due diligence."),
 ("Apakah harga bisa dinegosiasikan?", "Ya. Harga bersifat indikatif dan tunduk pada due diligence, struktur transaksi, dan dokumentasi definitif."),
 ("Bisakah akuisisi dibiayai bank?", "Bisa, umumnya dengan kombinasi ekuitas pembeli dan kredit investasi atau kredit akuisisi berbasis arus kas dan agunan aset RS. Kami bisa membantu menyusun struktur pendanaannya."),
 ("RS milik yayasan bisa dibeli?", "Yayasan tidak memiliki saham, sehingga strukturnya berupa konversi ke PT lalu akuisisi saham, pembelian aset, atau kerja sama operasi. Pilihannya dibahas di tahap LOI."),
]
P_RS = "/rumah-sakit-dijual/"
svc_page(P_RS, "FA Advisory · Sell Side", "Rumah Sakit Dijual: Peluang Akuisisi RS Swasta di Jawa Tengah dan DI Yogyakarta",
 "Daftar rumah sakit swasta yang sedang ditawarkan melalui FA Indonesia, dengan kisaran kinerja keuangan dan harga indikatif. Identitas aset dan data room dibuka setelah NDA.",
 body, FAQ, "Rumah Sakit Dijual: Akuisisi RS Swasta Jateng & DIY, Harga Rp8–55 M | FA Indonesia",
 "Listing rumah sakit dijual: RS umum kelas D, RS khusus bedah, RS ibu dan anak di Jawa Tengah dan DIY. Kisaran pendapatan, EBITDA, aset KJPP, harga indikatif. NDA dan data room.",
 "Penasihat Transaksi Jual Beli Rumah Sakit", "Sell-side M&A advisory for hospitals",
 "/bpr-dijual/", "BPR dan BPRS Dijual", "Halo FA Indonesia, saya tertarik mengakuisisi rumah sakit. Mohon info listing dan NDA.", "Rumah Sakit Dijual")
# tambah CSS + ItemList ke halaman RS
p = P("rumah-sakit-dijual", "index.html"); t = rd(p)
il = ('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "Rumah Sakit Dijual melalui FA Indonesia",
      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f'{r["code"]} {r["tipe"]}, {r["wil"]}',
      "description": f'{r["offer"]}, harga indikatif {r["harga"]}. {r["note"]}'} for i, r in enumerate(RS)]}, ensure_ascii=False) + "</script>")
wtxt(p, t.replace("</head>", CSS + il + "</head>", 1))

# ---------- BPR ----------
P_BPR = "/bpr-dijual/"
bpr_body = (f"<h2>Pipeline BPR dan BPRS</h2>{tbl(['Jenis', 'Gambaran', 'Indikasi Harga'], [(E(a), E(b), E(c)) for a, b, c in PIPE[2:]])}"
 "<p>Nama bank dan angka keuangan rinci hanya dibuka setelah NDA, karena menyangkut kerahasiaan bank dan nasabah.</p>"
 "<h2>Yang Perlu Disiapkan Pembeli BPR</h2><ul>"
 "<li>Perubahan pemegang saham pengendali BPR memerlukan persetujuan OJK, termasuk penilaian kemampuan dan kepatutan calon pengendali.</li>"
 "<li>Sumber dana akuisisi harus jelas dan dapat ditelusuri.</li>"
 "<li>Rencana bisnis pasca akuisisi: permodalan, kualitas kredit (NPL), dan tata kelola.</li>"
 "<li>Due diligence atas kualitas aset, CKPN, kepatuhan, dan sistem TI.</li></ul>"
 f"<h2>Alur Transaksi</h2>{ALUR}"
 "<h2>Ingin Menjual BPR?</h2><p>Kami membantu valuasi, information memorandum, pencarian pembeli, dan koordinasi dengan KAP dan konsultan hukum untuk proses persetujuan OJK.</p>"
 "<h2>Bacaan Terkait</h2><ul><li><a href=\"/rumah-sakit-dijual/\">Rumah Sakit Dijual</a></li><li><a href=\"/jasa-implementasi-psak-109/\">PSAK 109 dan CKPN untuk Lembaga Keuangan</a></li></ul>")
BPR_FAQ = [
 ("Apakah membeli BPR perlu izin OJK?", "Ya. Perubahan pemegang saham pengendali BPR atau BPRS memerlukan persetujuan OJK, termasuk penilaian kemampuan dan kepatutan."),
 ("Kenapa data BPR tidak ditampilkan?", "Data bank menyangkut kerahasiaan bank dan nasabah. Profil dan indikasi harga dibagikan setelah NDA kepada calon pembeli yang serius."),
 ("Bisakah perorangan membeli BPR?", "Bisa, sepanjang memenuhi persyaratan OJK sebagai calon pemegang saham pengendali, termasuk kejelasan sumber dana."),
]
svc_page(P_BPR, "FA Advisory · Sell Side", "BPR dan BPRS Dijual: Peluang Akuisisi Bank Perekonomian Rakyat",
 "BPR konvensional dan BPR syariah yang sedang ditawarkan melalui FA Indonesia. Identitas dan data keuangan dibuka setelah NDA.",
 bpr_body, BPR_FAQ, "BPR Dijual & BPRS Dijual: Akuisisi Bank Perekonomian Rakyat | FA Indonesia",
 "Peluang akuisisi BPR dan BPRS di Jawa Tengah dan DIY. Alur NDA, due diligence, persetujuan OJK, dan closing. Data lengkap setelah NDA.",
 "Penasihat Transaksi Jual Beli BPR", "Sell-side M&A advisory for rural banks",
 P_RS, "Rumah Sakit Dijual", "Halo FA Indonesia, saya tertarik mengakuisisi BPR atau BPRS. Mohon info dan NDA.", "BPR dan BPRS Dijual")

URLS = [P_RS, P_BPR]

def box(href, title, text, label):
    return (f'<!--fa-sell--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
            f'<p style="margin:0 0 6px;font-weight:600">{E(title)}</p><p style="margin:0 0 12px">{E(text)}</p>'
            f'<a class="btn solid" href="{href}">{label}</a></div><!--/fa-sell-->')
INJ = {
 ("konsultan-rumah-sakit",): box(P_RS, "Rumah Sakit yang Sedang Dijual", "RS umum, RS khusus bedah, dan RS ibu dan anak di Jawa Tengah dan DIY, lengkap dengan kisaran kinerja dan harga indikatif.", "Lihat Listing"),
 ("artikel", "indikator-keuangan-rumah-sakit-yang-dilihat-investor"): box(P_RS, "Mencari RS untuk Diakuisisi?", "Lihat listing rumah sakit yang sedang ditawarkan, dari Rp8 M sampai Rp55 M.", "Lihat Listing"),
 ("artikel", "konsultan-rumah-sakit-swasta-kapan-dibutuhkan"): box(P_RS, "Listing Rumah Sakit Dijual", "Peluang akuisisi RS swasta dengan data room setelah NDA.", "Lihat Listing"),
}
for parts, b in INJ.items():
    q = P(*parts, "index.html")
    if not os.path.exists(q): print("skip", q); continue
    t = re.sub(r"<!--fa-sell-->.*?<!--/fa-sell-->", "", rd(q), flags=re.S)
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("</main>")
    wtxt(q, t[:k] + b + t[k:])
lp = P("layanan", "index.html"); t = re.sub(r"<!--fa-sell-->.*?<!--/fa-sell-->", "", rd(lp), flags=re.S)
anchor = '<a class="btn line" href="/konsultan-kredit-distributor-importir/">'
if anchor in t: t = t.replace(anchor, f'<!--fa-sell--><a class="btn line" href="{P_RS}">RS &amp; BPR Dijual</a><!--/fa-sell-->' + anchor, 1)
wtxt(lp, t)

sm = re.sub(r"<!--fa-sell-->.*?<!--/fa-sell-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-sell-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for u in URLS) + "<!--/fa-sell-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = re.sub(r"\n## Peluang Akuisisi.*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + (f"\n\n## Peluang Akuisisi (Sell Side)\n- Rumah sakit dijual (anonim, kisaran kinerja dan harga indikatif Rp8–55 M, Jawa Tengah dan DIY) → {D}{P_RS}\n"
                        f"- BPR dan BPRS dijual (data setelah NDA, persetujuan OJK) → {D}{P_BPR}\n")
wtxt(P("llms.txt"), ll)
print("ok", URLS)
