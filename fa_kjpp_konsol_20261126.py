#!/usr/bin/env python3
"""26 Nov 2026 (2): penilaian KJPP (tanah dan bangunan, merek, rumah sakit, alkes, bisnis) dan
pendampingan LK konsolidasian, untuk Google dan asisten AI.

Bos: "Untuk KJPP, merk, tanah bangunan, RS, alkes, dan jasa pendampingan penyusunan LK Konsol, dll juga".

1. SATU halaman pilar baru /jasa-penilaian-kjpp/ (FA belum punya halaman layanan penilaian),
   dibangun dari template live /jasa-konsolidasi-laporan-keuangan-psak-110/. Bukan keluarga massal.
   Nama KJPP tidak disebut (belum ada keputusan Bos); FA ditulis BUKAN KJPP; tanpa harga,
   tanpa janji nilai/waktu.
2. /jasa-konsolidasi-laporan-keuangan-psak-110/: blok terima beres <!--fa-geo-->, description,
   JSON-LD Service (alternateName + description).
3. Link masuk berpenanda <!--fa-kj26--> dari halaman dan artikel terkait.
4. sitemap.xml + beranda (hasOfferCatalog). llms.txt lewat fa_content/llms_head_20261125.md
   + fa_ai_search_20261125.py (jalankan sesudah script ini).
Idempoten, --dry.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(ROOT, "out", "faindonesia")
DRY = "--dry" in sys.argv
TODAY = "2026-11-26"
changed = []


def write(path, new, old):
    if new != old:
        changed.append(os.path.relpath(path, ROOT))
        if not DRY:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").write(new)


def rd(p):
    return open(p).read() if os.path.exists(p) else ""


CSS = ('<style id="fa-geo-css">.geo-tb{box-sizing:border-box;max-width:760px;margin:20px 0 6px;'
       'padding:16px 18px;border:1px solid rgba(233,185,73,.5);border-left:4px solid #E9B949;'
       'border-radius:12px;background:rgba(233,185,73,.07)}.geo-tb b.geo-h{display:block;font-size:17px;'
       'margin:0 0 6px}.geo-tb ul{margin:0;padding-left:1.2em}.geo-tb li{margin:.25em 0;line-height:1.55}'
       '@media(max-width:760px){.geo-tb{padding:14px}}</style>')


def geo(judul, items):
    return (f'<!--fa-geo-->{CSS}<div class="geo-tb"><b class="geo-h">{judul}</b><ul>'
            + "".join(f"<li>{x}</li>" for x in items) + "</ul></div><!--/fa-geo-->")


# ------------------------------------------------------------------ 1. halaman KJPP
SLUG = "jasa-penilaian-kjpp"
URL = f"https://faindonesia.co.id/{SLUG}/"
TITLE = "Jasa Penilaian KJPP: Tanah, Bangunan, Merek, RS, Alkes"
H1 = "Jasa Penilaian KJPP: Tanah dan Bangunan, Merek, Rumah Sakit, Alat Kesehatan, dan Bisnis"
DESC = ("Penilaian KJPP terima beres untuk tanah, bangunan, merek, rumah sakit, alat kesehatan, dan bisnis. "
        "Dokumen disiapkan tim FA Indonesia, dinilai KJPP berizin.")
assert len(TITLE) <= 65 and len(DESC) <= 158, (len(TITLE), len(DESC))
WA = "https://wa.me/6282245260121?text=Halo%20Pak%20Ananta%2C%20saya%20ingin%20tanya%20penilaian%20KJPP."
BTN = (f'<a class="btn solid" href="{WA}" rel="noopener" target="_blank">Chat Ananta, CPA</a>')
FAQ = [
    ("Apakah FA Indonesia sebuah KJPP?",
     "Bukan. FA Indonesia adalah firma penasihat keuangan. Penilaian dan opini nilainya dikerjakan penilai publik "
     "di Kantor Jasa Penilai Publik (KJPP) berizin Menteri Keuangan. Tim FA Indonesia menyiapkan dokumen dan data "
     "keuangan, mendampingi survei, dan memastikan laporan penilaian sesuai keperluan pihak yang memintanya."),
    ("Apakah nilai bisa disesuaikan dengan keinginan pemilik?",
     "Tidak. Nilai adalah opini independen penilai publik berdasarkan Standar Penilaian Indonesia. Yang bisa "
     "dikerjakan tim adalah memastikan data lengkap dan benar, supaya tidak ada aset atau pendapatan yang terlewat "
     "dari perhitungan."),
    ("Apakah laporan penilaian KJPP pasti diterima bank?",
     "Setiap bank punya daftar KJPP rekanan sendiri. Karena itu sebelum penilai ditunjuk, kami cek dulu ke bank "
     "yang dituju supaya laporan tidak perlu diulang."),
    ("Apa beda valuasi indikatif dengan laporan penilaian KJPP?",
     "Valuasi indikatif adalah perhitungan internal untuk bahan keputusan dan negosiasi, tanpa tanda tangan penilai "
     "publik. Laporan penilaian KJPP ditandatangani penilai publik berizin dan dipakai ketika bank, investor, "
     "auditor, atau aturan memintanya secara resmi."),
    ("Apakah merek yang belum terdaftar bisa dinilai?",
     "Sebaiknya merek didaftarkan dulu di Direktorat Jenderal Kekayaan Intelektual. Merek yang belum terdaftar "
     "sulit dialihkan atau dijadikan dasar transaksi, sehingga penilaiannya kurang bermanfaat bagi pihak lain."),
    ("Berapa biaya penilaian KJPP?",
     "Bergantung pada jenis objek, jumlah dan lokasi aset, serta tujuan penilaian. Biaya disampaikan dalam penawaran "
     "tertulis setelah diskusi awal, sebelum pekerjaan dimulai."),
]
ROWS = [
    ("Tanah dan bangunan", "Agunan kredit bank, revaluasi aset tetap, jual beli, sewa",
     "Sertifikat, PBB, izin bangunan, daftar aset tetap"),
    ("Merek dan aset takberwujud", "Jual beli merek, masuknya investor, lisensi dan waralaba, setoran modal nontunai",
     "Sertifikat merek, penjualan per merek, proyeksi"),
    ("Rumah sakit dan klinik", "Jual beli rumah sakit, masuknya investor, kredit investasi",
     "Izin operasional, laporan keuangan, data kunjungan dan BOR, daftar aset"),
    ("Alat kesehatan, mesin, dan peralatan", "Agunan, revaluasi, asuransi, pembelian aset bekas",
     "Daftar alat (merek, tipe, tahun), faktur, catatan pemeliharaan dan kalibrasi"),
    ("Bisnis dan saham", "Akuisisi, penjualan saham, masuknya investor, uji penurunan nilai",
     "Laporan keuangan, proyeksi, struktur kepemilikan"),
]
TB = geo("Penilaian KJPP Terima Beres, Singkatnya", [
    "Ceritakan aset atau usaha yang perlu dinilai dan untuk keperluan apa. Dokumen boleh menyusul.",
    "Tim FA Indonesia menyusun daftar aset, legalitas, dan data keuangan yang diminta penilai.",
    "Penilaian dan opini nilai sepenuhnya oleh penilai publik di KJPP berizin Menteri Keuangan, sesuai Standar Penilaian Indonesia.",
    "Didampingi sampai laporan penilaian diterima bank, investor, auditor, atau pihak lain yang memintanya.",
])
SEC = [
    ("yang-bisa-dinilai", "Yang Bisa Dinilai", None),
    ("penilaian-tanah-dan-bangunan", "Penilaian Tanah dan Bangunan",
     "<p>Paling sering diminta untuk agunan kredit: kantor, ruko, gudang, pabrik, hotel, sampai lahan kosong. "
     "Penilai properti meninjau lokasi, mencocokkan legalitas, lalu memakai pendekatan pasar, biaya, atau pendapatan "
     "sesuai jenis propertinya. Penilaian yang sama dipakai untuk revaluasi aset tetap di laporan keuangan, dan di "
     "sini angka penilai harus selaras dengan catatan akuntansi. Bagian itu yang kami rapikan lebih dulu: daftar aset "
     "tetap, sertifikat yang masih atas nama pribadi, dan bangunan yang belum tercatat.</p>"),
    ("penilaian-merek", "Penilaian Merek",
     "<p>Merek dinilai ketika akan dijual, dilisensikan, diwaralabakan, dijadikan setoran modal, atau ketika investor "
     "ingin tahu berapa bagian nilai usaha yang berasal dari nama. Penilai bisnis umumnya memakai pendekatan "
     "pendapatan, misalnya metode penghematan royalti, lalu mengujinya dengan pendekatan pasar atau biaya. Syarat "
     "praktisnya dua: merek sudah terdaftar, dan penjualan bisa dipisahkan per merek. Kalau pembukuan belum memisahkan "
     "penjualan per merek, tim kami menyusunnya dari data penjualan yang ada.</p>"),
    ("penilaian-rumah-sakit", "Penilaian Rumah Sakit dan Klinik",
     "<p>Rumah sakit dinilai dalam dua lapis. Lapis aset: tanah, bangunan, dan alat kesehatan. Lapis usaha: kemampuan "
     "rumah sakit menghasilkan arus kas, yang dihitung dengan arus kas terdiskonto dan pembanding seperti EV/EBITDA. "
     "Untuk jual beli dan masuknya investor, lapis usaha yang menentukan harga; untuk kredit bank, lapis aset yang "
     "dipakai. Sebelum menunjuk penilai, pemilik bisa melihat kisaran awal lewat "
     '<a href="/kalkulator-valuasi-rumah-sakit/">kalkulator valuasi rumah sakit</a>, dan membaca '
     '<a href="/artikel/taksasi-bank-vs-penilaian-kjpp-rumah-sakit/">beda taksasi bank dan penilaian KJPP</a>.</p>'),
    ("penilaian-alat-kesehatan", "Penilaian Alat Kesehatan, Mesin, dan Peralatan",
     "<p>Alat kesehatan dan mesin dinilai untuk agunan, revaluasi, asuransi, atau saat membeli aset bekas. Penilai "
     "melihat merek, tipe, tahun, kondisi, catatan pemeliharaan dan kalibrasi, lalu memakai pendekatan biaya (biaya "
     "pengganti baru dikurangi penyusutan) atau pendekatan pasar bila ada pembanding. Pekerjaan terberat biasanya "
     "justru daftar alatnya: ratusan baris tanpa tahun perolehan dan tanpa faktur. Tim kami menyusun daftar itu dari "
     "kartu aset, faktur, dan pengecekan fisik bersama tim Anda.</p>"),
    ("alur-kerja", "Alur Kerja", None),
    ("peran-fa-dan-kjpp", "Peran FA Indonesia dan Peran KJPP",
     "<p>Pembagiannya tegas. KJPP menilai dan menandatangani laporan penilaian secara independen. FA Indonesia "
     "menyiapkan klien: merapikan data aset dan laporan keuangan, memastikan penilai yang ditunjuk diterima pihak yang "
     "meminta, mendampingi survei, lalu menjelaskan hasilnya kepada pemilik, bank, atau investor. Untuk transaksi, "
     "tim juga menyiapkan bahan negosiasi dari hasil penilaian itu. Lihat juga "
     '<a href="/jasa-valuasi-usaha/">jasa valuasi usaha</a> untuk perhitungan indikatif sebelum penilaian resmi.</p>'),
]
REL = [
    ("/artikel/kapan-perusahaan-butuh-kjpp-jasa-penilai/", "Kapan Perusahaan Butuh KJPP"),
    ("/artikel/taksasi-bank-vs-penilaian-kjpp-rumah-sakit/", "Taksasi Bank vs Penilaian KJPP untuk Rumah Sakit"),
    ("/artikel/valuasi-rumah-sakit-swasta/", "Valuasi Rumah Sakit Swasta"),
    ("/artikel/revaluasi-aset-tetap-psak-216-dan-pajak/", "Revaluasi Aset Tetap: PSAK 216 dan Pajak"),
    ("/artikel/valuasi-indikatif-vs-valuasi-lengkap/", "Valuasi Indikatif vs Valuasi Lengkap"),
    ("/jasa-valuasi-usaha/", "Jasa Valuasi Usaha"),
    ("/konsultan-kredit-bank/", "Konsultan Kredit Bank"),
    ("/menjual-rumah-sakit/", "Menjual Rumah Sakit"),
]
REL = [(u, t) for u, t in REL if os.path.exists(os.path.join(FA, u.strip("/"), "index.html"))]


def body():
    o = ['<p class="eyebrow">Layanan · Penilaian</p>',
         f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{H1}</h1>',
         f'<div class="tshare-top"><div class="share" data-lab="Bagikan" data-tool="{html.escape(H1)}"></div></div>',
         '<p class="t" style="max-width:62em">Penilaian aset dan bisnis oleh Kantor Jasa Penilai Publik (KJPP) berizin '
         'Menteri Keuangan, untuk agunan kredit bank, revaluasi aset, jual beli usaha, masuknya investor, dan laporan '
         'keuangan. Tim FA Indonesia menyiapkan dokumen dan data keuangannya, mendampingi survei, sampai laporan '
         'penilaian diterima pihak yang memintanya.</p>',
         f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px">{BTN}'
         '<a class="btn line" href="/jasa-valuasi-usaha/">Jasa Valuasi Usaha</a></div>', TB,
         '<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>'
         + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t, _ in SEC) + "</ol></nav>"]
    for i, t, p in SEC:
        o.append(f'<h2 id="{i}">{t}</h2>')
        if i == "yang-bisa-dinilai":
            o.append('<p>Penilai properti menilai tanah, bangunan, mesin, dan peralatan. Penilai bisnis menilai usaha, '
                     'saham, dan aset takberwujud seperti merek. Banyak keperluan membutuhkan keduanya sekaligus, '
                     'misalnya rumah sakit yang akan dijual.</p>')
            o.append('<div class="tblwrap"><table class="twr-s tbl"><thead><tr><th>Objek</th><th>Biasanya Untuk</th>'
                     '<th>Yang Disiapkan Tim FA</th></tr></thead><tbody>'
                     + "".join(f'<tr><td>{a}</td><td data-l="Biasanya Untuk">{b}</td>'
                               f'<td data-l="Yang Disiapkan Tim FA">{c}</td></tr>' for a, b, c in ROWS)
                     + "</tbody></table></div>")
        elif i == "alur-kerja":
            o.append('<ol class="flow5"><li><b>Diskusi awal</b>Objek, tujuan penilaian, dan pihak yang meminta.</li>'
                     '<li><b>Dokumen</b>Tim FA menyusun daftar aset, legalitas, dan data keuangan.</li>'
                     '<li><b>Survei</b>Penilai meninjau lokasi dan aset, kami dampingi.</li>'
                     '<li><b>Analisis</b>Penilai menghitung nilai sesuai Standar Penilaian Indonesia.</li>'
                     '<li><b>Laporan</b>Laporan penilaian terbit dan kami jelaskan isinya.</li></ol>')
        else:
            o.append(p)
    o.append("<h2>Bacaan Terkait</h2><ul>" + "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in REL) + "</ul>")
    o.append("<h2>Pertanyaan Umum</h2>\n" + '<div class="faq-acc">'
             + "".join(f'<details class="faq-i"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + "</div>")
    o.append(f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px">{BTN}</div>')
    return "\n".join(o) + "\n"


T = rd(os.path.join(FA, "jasa-konsolidasi-laporan-keuangan-psak-110", "index.html"))
T = re.sub(r"<!--fa-geo-->.*?<!--/fa-geo-->", "", T, flags=re.S)
a = T.find('<p class="eyebrow">', T.find("<main"))
b = T.find('<div style="margin:44px 0 0;', a)
assert a != -1 and b != -1
page = T[:a] + body() + T[b:]
OLDU = "https://faindonesia.co.id/jasa-konsolidasi-laporan-keuangan-psak-110/"
OT = re.search(r"<title>(.*?)</title>", T).group(1)
OD = re.search(r'<meta content="([^"]*)" name="description"', T).group(1)
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Service", "name": "Jasa Penilaian KJPP", "alternateName": "Penilaian KJPP terima beres",
     "serviceType": "Pendampingan penilaian aset dan bisnis oleh KJPP",
     "description": ("Pendampingan penilaian tanah dan bangunan, merek, rumah sakit, alat kesehatan, mesin, dan "
                     "bisnis. Dokumen dan data keuangan disiapkan tim FA Indonesia; penilaian oleh penilai publik di "
                     "KJPP berizin Menteri Keuangan."),
     "provider": {"@type": "ProfessionalService", "@id": "https://faindonesia.co.id/#org", "name": "FA Indonesia",
                  "url": "https://faindonesia.co.id/"},
     "areaServed": {"@type": "Country", "name": "Indonesia"}, "url": URL},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in FAQ]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "FA Indonesia", "item": "https://faindonesia.co.id/"},
        {"@type": "ListItem", "position": 2, "name": "Layanan", "item": "https://faindonesia.co.id/layanan/"},
        {"@type": "ListItem", "position": 3, "name": "Penilaian KJPP", "item": URL}]}]}
page = re.sub(r'<script type="application/ld\+json">.*?</script>',
              lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
              page, count=1, flags=re.S)
page = page.replace(OLDU, URL).replace(OT, TITLE).replace(OD, html.escape(DESC, quote=True))
page = page.replace("https://faindonesia.co.id/img/og-page/jasa-konsolidasi-laporan-keuangan-psak-110.jpg",
                    "https://faindonesia.co.id/img/og/fa-indonesia-og.jpg")
assert "psak-110" not in page[:page.find("<main")] and "PSAK 110" not in page[page.find("<main"):page.find("<footer")]
f = os.path.join(FA, SLUG, "index.html")
write(f, page, rd(f))

# ------------------------------------------------------------------ 2. halaman konsolidasi
f = os.path.join(FA, "jasa-konsolidasi-laporan-keuangan-psak-110", "index.html")
old = rd(f)
s = re.sub(r"<!--fa-geo-->.*?<!--/fa-geo-->", "", old, flags=re.S)
kb = geo("Laporan Keuangan Konsolidasian Terima Beres, Singkatnya", [
    "Kirim laporan keuangan atau neraca saldo tiap entitas apa adanya, walau bagan akunnya berbeda-beda.",
    "Tim FA Indonesia menyelaraskan akun, merekonsiliasi saldo antarperusahaan, dan menyusun jurnal eliminasinya.",
    "Hasilnya laporan keuangan konsolidasian lengkap dengan kertas kerja, siap diperiksa auditor.",
    "Didampingi saat auditor, bank, atau investor menanyakan angkanya.",
])
h1 = s.find("</h1>")
cb = s.find('<div class="cbtns"', h1)
j = s.find("</div>", cb) + 6
s = s[:j] + kb + s[j:]
KD = ("Pendampingan penyusunan laporan keuangan konsolidasian (PSAK 110) terima beres: akun diselaraskan, "
      "saldo antarperusahaan dieliminasi, siap diaudit.")
assert len(KD) <= 158
e = html.escape(KD, quote=True)
s = re.sub(r'<meta[^>]*(?:name="description"|property="og:description"|name="twitter:description")[^>]*>',
           lambda m: re.sub(r'content="[^"]*"', f'content="{e}"', m.group(0), count=1), s)


def fix_k(m):
    d = json.loads(m.group(1))
    for g in d.get("@graph", []):
        if g.get("@type") == "Service":
            g["alternateName"] = ["Pendampingan penyusunan laporan keuangan konsolidasian",
                                  "Jasa laporan keuangan konsolidasi grup usaha"]
            g["description"] = KD
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"


s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_k, s, count=1, flags=re.S)
write(f, s, old)

# ------------------------------------------------------------------ 3. link masuk
RE_L = re.compile(r"<!--fa-kj26-->.*?<!--/fa-kj26-->", re.S)
LK = ('<!--fa-kj26--><p style="margin:14px 0;font-size:.97em"><i>Perlu laporan penilaian resmi? Lihat '
      '<a href="/jasa-penilaian-kjpp/">jasa penilaian KJPP</a> untuk tanah dan bangunan, merek, rumah sakit, alat '
      'kesehatan, dan bisnis: dokumen disiapkan tim FA Indonesia, penilaian oleh KJPP berizin.</i></p><!--/fa-kj26-->')
LC = ('<!--fa-kj26--><p style="margin:14px 0;font-size:.97em"><i>Grup usaha Anda perlu laporan konsolidasian? Lihat '
      '<a href="/jasa-konsolidasi-laporan-keuangan-psak-110/">pendampingan penyusunan laporan keuangan konsolidasian</a> '
      'dari tim FA Indonesia.</i></p><!--/fa-kj26-->')
for slug, line in (("kapan-perusahaan-butuh-kjpp-jasa-penilai", LK), ("taksasi-bank-vs-penilaian-kjpp-rumah-sakit", LK),
                   ("valuasi-rumah-sakit-swasta", LK), ("revaluasi-aset-tetap-psak-216-dan-pajak", LK),
                   ("valuasi-indikatif-vs-valuasi-lengkap", LK),
                   ("laporan-keuangan-konsolidasian-grup-usaha-keluarga", LC)):
    f = os.path.join(FA, "artikel", slug, "index.html")
    old = rd(f)
    if not old:
        continue
    s = RE_L.sub("", old)
    n = s.find('<nav aria-label="', s.find("</h1>"))
    if n == -1 or "Peta Isi" not in s[n:n + 400]:
        continue
    write(f, s[:n] + line + s[n:], old)
f = os.path.join(FA, "jasa-valuasi-usaha", "index.html")
old = rd(f)
s = RE_L.sub("", old)
k = s.find("<h2>Bacaan Terkait</h2><ul>")
if k != -1:
    k += len("<h2>Bacaan Terkait</h2><ul>")
    s = s[:k] + ('<!--fa-kj26--><li><a href="/jasa-penilaian-kjpp/">Jasa Penilaian KJPP: Tanah dan Bangunan, Merek, '
                 'Rumah Sakit, Alat Kesehatan</a></li><!--/fa-kj26-->') + s[k:]
    write(f, s, old)

# ------------------------------------------------------------------ 4. sitemap + beranda
f = os.path.join(FA, "sitemap.xml")
old = rd(f)
s = old
if f"<loc>{URL}</loc>" not in s:
    s = s.replace("</urlset>", f"<url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n</urlset>")
ku = "https://faindonesia.co.id/jasa-konsolidasi-laporan-keuangan-psak-110/"
s = re.sub(r"(<url><loc>" + re.escape(ku) + r"</loc><lastmod>)[^<]+", r"\g<1>" + TODAY, s)
write(f, s, old)
f = os.path.join(FA, "index.html")
old = rd(f)


def fix_home(m):
    d = json.loads(m.group(1))
    hit = False
    for g in d.get("@graph", []):
        if g.get("@type") == "ProfessionalService":
            ka = g.setdefault("knowsAbout", [])
            for k in ("Penilaian KJPP (tanah dan bangunan, merek, rumah sakit, alat kesehatan, bisnis)",
                      "Laporan keuangan konsolidasian PSAK 110"):
                if k not in ka:
                    ka.append(k); hit = True
            items = g.get("hasOfferCatalog", {}).get("itemListElement")
            if items is not None:
                urls = [x.get("itemOffered", {}).get("url") for x in items]
                for nm, u in (("Pendampingan penilaian KJPP: tanah dan bangunan, merek, rumah sakit, alat kesehatan, bisnis", URL),
                              ("Pendampingan penyusunan laporan keuangan konsolidasian", ku)):
                    if u not in urls:
                        items.append({"@type": "Offer", "itemOffered": {"@type": "Service", "name": nm, "url": u}})
                        hit = True
    return ('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>") if hit else m.group(0)


write(f, re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_home, old, count=1, flags=re.S), old)

print(("DRY " if DRY else "") + f"{len(changed)} file berubah")
for c in changed:
    print(" ", c)
