# -*- coding: utf-8 -*-
"""13 Nov 2026 (Bos, kesal): halaman induk /cfo-paruh-waktu/ belum disentuh padahal jualan Fractional CFO.
Halaman ini jadi halaman utama Fractional CFO: kartu profil foto + gelar lengkap (permintaan Bos), lingkup kerja,
alur, Fractional CFO untuk PT PMA (Bali, NTB, NTT, nasional EN), tim. SEO lama TIDAK hilang: URL, canonical,
semua teks dan link lama tetap; title/H1 hanya ditambah kata "Fractional CFO" (kata lama tetap ada).
Bekerja di out/faindonesia, idempoten (penanda <!--fa-cfopw-prof-->, <!--fa-cfopw-->). Jalankan setelah fa_fcfo_pma_20261113.py.
"""
import os, re, json, html, urllib.parse, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "out", "faindonesia")
P = os.path.join(OUT, "cfo-paruh-waktu", "index.html")
E = html.escape; D = "https://faindonesia.co.id"
NAME = "Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP"
WA = "https://wa.me/6282245260121?text=" + urllib.parse.quote("Halo Pak Ananta, saya ingin diskusi soal fractional CFO (CFO paruh waktu) untuk perusahaan kami. Usaha: ... Jumlah entitas: ...", safe="")
TITLE = "Fractional CFO dan CFO Paruh Waktu Outsourced | FA Indonesia"
H1 = "Fractional CFO: CFO Paruh Waktu dan Fungsi Keuangan Outsourced"
OLD_TITLE = "CFO Paruh Waktu &amp; Fungsi Keuangan Outsourced | FA Indonesia"
OLD_H1 = "CFO Paruh Waktu dan Fungsi Keuangan Outsourced"

def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

# gaya kartu profil sama dengan halaman regional (fcfo-css), diambil dari fa_fcfo_pma_20261113.py tanpa menjalankannya
_src = open(os.path.join(HERE, "fa_fcfo_pma_20261113.py"), encoding="utf-8").read()
CSS = eval(re.search(r"^CSS = (\(.*?\))\n\n", _src, re.S | re.M).group(1))
PROF = ('<!--fa-cfopw-prof-->' + CSS + '<div class="fcp"><img alt="' + E(NAME) + '" decoding="async" height="875" src="/img/ananta-w-sasongko-cpa-rs.jpg" width="700"/><div>'
        '<small>Fractional CFO · FA Indonesia</small><b class="nm">' + E(NAME) + '</b><span class="rl">Fractional CFO dan penasihat keuangan untuk perusahaan swasta, grup usaha, dan PT PMA</span><ul>'
        '<li>Certified Public Accountant (CPA), Institut Akuntan Publik Indonesia (IAPI)</li><li>FMVA dan FPAP, Corporate Finance Institute</li>'
        '<li>Audit dan assurance di Ernst &amp; Young (EY)</li><li>Pernah Direktur Keuangan dan Group CFO grup rumah sakit multi-entitas: konsolidasi, akuisisi, pembiayaan bank</li>'
        '<li>Menyiapkan perusahaan swasta menuju IPO di Bursa Efek Indonesia; kandidat doktor akuntansi</li></ul>'
        f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn solid" href="{WA}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
        '<a class="btn line" href="/ananta-w-sasongko/">Profil Lengkap</a></div></div></div><!--/fa-cfopw-prof-->')

SEC = [
 ("lingkup-kerja-fractional-cfo", "Lingkup Kerja Fractional CFO", tbl(["Bidang", "Yang Anda Dapat"], [
   ["Tutup buku dan laporan bulanan", "Laporan manajemen untuk pemilik, komisaris, bank, dan investor, dengan ulasan singkat apa yang berubah dan apa yang perlu diputuskan"],
   ["Kas dan pengendalian", "Kendali kas dan bank harian, batas persetujuan, rekonsiliasi, dan pengendalian biaya"],
   ["Anggaran dan proyeksi", "Anggaran tahunan, arus kas 13 minggu, anggaran proyek atau belanja modal, dan analisis selisih"],
   ["Pajak dan kepatuhan", "Kalender dan reviu pajak bulanan dan tahunan bersama konsultan pajak; LKPM untuk PT PMA"],
   ["Bank dan investor", "Model keuangan, paket informasi, pengajuan kredit, dan laporan covenant"],
   ["Audit dan tata kelola", "Berkas tutup buku siap audit, SOP, pengendalian internal, dan penataan GCG"],
   ["Tim keuangan", "Rekrutmen, pelatihan, dan serah terima ke manajer keuangan atau CFO penuh waktu"]])),
 ("alur-kerja-sama", "Alur Kerja Sama", "<ol><li><b>Percakapan awal</b> lewat WhatsApp atau video call: struktur usaha, pemilik, dan laporan yang dibutuhkan.</li>"
   "<li><b>Diagnostik</b> pembukuan, kas, pajak, dan pengendalian, dengan daftar prioritas tertulis.</li>"
   "<li><b>Perikatan bulanan</b>: jumlah hari per bulan yang disepakati, kerja jarak jauh lewat folder bersama, dan kunjungan terjadwal.</li>"
   "<li><b>Serah terima</b> saat perusahaan siap merekrut manajer keuangan atau CFO penuh waktu.</li></ol>"),
 ("fractional-cfo-untuk-pt-pma", "Fractional CFO untuk PT PMA",
   "<p>Perusahaan PMA butuh laporan berbahasa Inggris untuk induk dan investor, LKPM triwulanan, pemotongan pajak atas pembayaran ke luar negeri, serta pinjaman pemegang saham yang tercatat rapi. Halaman per wilayah:</p>"
   '<div class="ftl"><a href="/fractional-cfo-pt-pma-bali/"><small>Bali</small><b>Fractional CFO PT PMA di Bali</b><span>Vila, resor, restoran, beach club, properti.</span></a>'
   '<a href="/fractional-cfo-pt-pma-ntb/"><small>NTB</small><b>Fractional CFO PT PMA di NTB dan Lombok</b><span>Gili, Mandalika, jasa tambang di Sumbawa.</span></a>'
   '<a href="/fractional-cfo-pt-pma-ntt/"><small>NTT</small><b>Fractional CFO PT PMA di NTT dan Labuan Bajo</b><span>Resor, kapal phinisi, operator selam, Sumba.</span></a></div>'
   '<p class="t">In English: <a href="/en/fractional-cfo-indonesia/">Fractional CFO in Indonesia</a> · <a href="/en/fractional-cfo-bali/">Bali</a> · '
   '<a href="/en/fractional-cfo-lombok-ntb/">Lombok and NTB</a> · <a href="/en/fractional-cfo-labuan-bajo-ntt/">Labuan Bajo and NTT</a></p>'),
 ("tim-kami", "Tim Kami", tbl(["Peran", "Siapa"], [
   ["Fractional CFO", "Ananta W. Sasongko, CPA, FA Indonesia"],
   ["Pembukuan dan penyusunan laporan keuangan", "KJA Farhani K.N., Kantor Jasa Akuntansi berizin"],
   ["Audit laporan keuangan", "KAP DHN &amp; Rekan, Kantor Akuntan Publik berizin Menteri Keuangan dan terdaftar OJK"]])
   + "<p>Peran CFO adalah bagian dari manajemen. Audit selalu dilakukan kantor yang berbeda.</p>"),
]
CPW_CSS = ('<style id="cpw-css">.cpw .tblwrap{overflow-x:auto;margin:14px 0 10px}.cpw .tbl{width:100%;border-collapse:collapse;font-size:15px}'
           '.cpw .tbl th,.cpw .tbl td{border:1px solid #333;padding:10px 12px;text-align:left;vertical-align:top;line-height:1.5}'
           '.cpw .tbl th{background:#1e1e1e;font-weight:600}.cpw .tbl td:first-child{width:32%}</style>')
BLK = "<!--fa-cfopw-->" + CPW_CSS + '<div class="cpw">' + "".join(f'<div class="head" style="margin-top:36px"><h2 id="{a}">{E(b)}</h2></div>{c}' for a, b, c in SEC) + "</div><!--/fa-cfopw-->"

t = open(P, encoding="utf-8").read(); t0 = t
t = re.sub(r"<!--fa-cfopw-prof-->.*?<!--/fa-cfopw-prof-->", "", t, flags=re.S)
t = re.sub(r"<!--fa-cfopw-->.*?<!--/fa-cfopw-->", "", t, flags=re.S)
t = re.sub(r'<li><a href="#(?:lingkup-kerja-fractional-cfo|alur-kerja-sama|fractional-cfo-untuk-pt-pma|tim-kami)">.*?</a></li>', "", t)
# title, H1, og, ld
t = t.replace(f"<title>{OLD_TITLE}</title>", f"<title>{E(TITLE)}</title>", 1)
t = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{E(TITLE)}" property="og:title"/>', t, count=1)
t = t.replace(f'line-height:1.1">{OLD_H1}</h1>', f'line-height:1.1">{E(H1)}</h1>', 1)
t = t.replace(f'data-tool="{OLD_H1}"', f'data-tool="{E(H1)}"', 1)
if 'hreflang="en"' not in t[:t.find("</head>")]:
    t = t.replace('<link href="https://faindonesia.co.id/cfo-paruh-waktu/" rel="canonical"/>',
                  '<link href="https://faindonesia.co.id/cfo-paruh-waktu/" rel="canonical"/><link href="https://faindonesia.co.id/cfo-paruh-waktu/" hreflang="id" rel="alternate"/>'
                  '<link href="https://faindonesia.co.id/en/fractional-cfo-indonesia/" hreflang="en" rel="alternate"/>', 1)
def fix_ld(m):
    g = json.loads(m.group(1))
    for n in g.get("@graph", []):
        if n.get("@type") == "WebPage": n["name"] = html.unescape(TITLE)
        if n.get("@type") == "Service":
            n["name"] = "Fractional CFO (CFO paruh waktu)"
            n["employee"] = {"@type": "Person", "name": NAME, "jobTitle": "Fractional CFO", "image": D + "/img/ananta-w-sasongko-cpa-rs.jpg", "url": D + "/ananta-w-sasongko/"}
    return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + "</script>"
t = re.sub(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@graph": \[\{"@type": "WebPage".*?)</script>', fix_ld, t, count=1, flags=re.S)
# kartu profil setelah paragraf pembuka
lead_end = t.index("</p>", t.index('<p class="t" style="max-width:62em">FA Indonesia menjalankan')) + 4
t = t[:lead_end] + PROF + t[lead_end:]
# blok baru setelah daftar Biaya, sebelum Wilayah Layanan
anc = '<div class="head" style="margin-top:36px"><h2 id="wilayah-layanan">'
assert t.count(anc) == 1
t = t.replace(anc, BLK + anc, 1)
# Peta Isi
t = t.replace('<li><a href="#wilayah-layanan">Wilayah Layanan</a></li>',
              "".join(f'<li><a href="#{a}">{E(b)}</a></li>' for a, b, _ in SEC) + '<li><a href="#wilayah-layanan">Wilayah Layanan</a></li>', 1)
if t != t0: open(P, "w", encoding="utf-8").write(t); print("cfo-paruh-waktu diperbarui")
else: print("tidak berubah")
