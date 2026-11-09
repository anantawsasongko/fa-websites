# -*- coding: utf-8 -*-
"""KJA Farhani: halaman kota baru (1 Nov 2026) dari template kantor-jasa-akuntan-tuban.
Sidoarjo, Pasuruan, Batu, Kediri, Mojokerto. Footer Wilayah semua halaman + sitemap + llms.txt.
Idempoten. Jalankan sebelum prep.py (prep menyalin folder KJA ke out/ dan mengganti netlify.app ke pages.dev)."""
import os, re, json, html
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(HERE, "KJA-Farhani_site_v12-netlify-primary")
BASE = "https://kja-farhani.netlify.app"
E = html.escape
def rd(p): return open(p, encoding="utf-8").read()
def wt(p, s): open(p, "w", encoding="utf-8").write(s)
TPL = rd(os.path.join(K, "kantor-jasa-akuntan-tuban", "index.html"))

CITIES = [
 dict(slug="sidoarjo", name="Sidoarjo", area=["Sidoarjo", "Surabaya", "Gresik"], near="Surabaya dan Gresik",
  ctx="Sidoarjo padat dengan pabrik, pergudangan, dan usaha keluarga yang tumbuh menjadi pemasok industri di Surabaya Raya, termasuk sentra kerajinan tas dan koper. Banyak di antaranya mulai diminta laporan keuangan oleh bank, pembeli besar, atau calon mitra, sementara pembukuannya masih dikerjakan seadanya.",
  types=[("Pemasok dan subkontraktor pabrik", "yang perlu laporan keuangan untuk daftar vendor dan negosiasi termin."),
         ("Usaha pergudangan dan logistik", "yang mengajukan kredit armada atau gudang."),
         ("Produsen dan pengrajin", "yang mulai ekspor atau masuk ke ritel modern."),
         ("CV dan PT keluarga", "yang PPN-nya mulai menumpuk dan pembukuannya belum rapi.")]),
 dict(slug="pasuruan", name="Pasuruan", area=["Kabupaten Pasuruan", "Kota Pasuruan", "Probolinggo"], near="Probolinggo dan Sidoarjo",
  ctx="Pasuruan menjadi lokasi banyak pabrik di kawasan industri dan sepanjang jalur Surabaya ke Malang. Di sekitarnya tumbuh usaha pemasok, transportasi, katering, dan jasa yang melayani pabrik. Pemberi kerja dan bank biasanya meminta laporan keuangan yang rapi sebelum kontrak atau kredit diberikan.",
  types=[("Pemasok bahan dan jasa ke pabrik", "yang perlu laporan keuangan untuk kualifikasi vendor."),
         ("Usaha transportasi dan katering industri", "yang mengajukan kredit modal kerja atau armada."),
         ("Peternakan dan pengolahan hasil pertanian", "yang mulai bermitra dengan pembeli besar."),
         ("CV dan PT keluarga", "yang ingin pembukuan bulanan dan pajak tertib.")]),
 dict(slug="batu", name="Batu", area=["Kota Batu", "Kabupaten Malang", "Kota Malang"], near="Malang",
  ctx="Ekonomi Batu digerakkan wisata: hotel, vila, restoran, taman rekreasi, dan agrowisata. Usaha seperti ini punya kebutuhan pembukuan yang khas, misalnya pencatatan pendapatan harian, pajak daerah atas hotel dan restoran, serta laporan keuangan untuk kredit renovasi atau penambahan kamar.",
  types=[("Hotel, vila, dan homestay", "yang butuh pembukuan harian dan laporan untuk kredit renovasi."),
         ("Restoran dan kafe", "yang mengurus pajak daerah dan PPh, dan ingin tahu margin per menu."),
         ("Agrowisata dan usaha pertanian", "yang mulai bermitra dengan pemasok atau investor."),
         ("Usaha keluarga", "yang uang pribadi dan usahanya masih bercampur.")]),
 dict(slug="kediri", name="Kediri", area=["Kota Kediri", "Kabupaten Kediri", "Nganjuk"], near="Nganjuk dan Tulungagung",
  ctx="Kediri adalah pusat dagang Jawa Timur bagian barat daya, dengan industri besar, perdagangan, dan banyak usaha keluarga. Banyak pemasok lokal yang melayani industri dan distributor besar perlu laporan keuangan untuk kontrak, kredit modal kerja, dan kepatuhan pajak.",
  types=[("Distributor dan toko grosir", "yang mengajukan kredit modal kerja."),
         ("Pemasok untuk industri besar", "yang diminta laporan keuangan dan rasio tertentu."),
         ("Usaha makanan olahan khas", "yang mulai masuk ke ritel modern dan perlu harga pokok yang jelas."),
         ("CV dan PT keluarga", "yang pembukuannya belum rapi dan PPN-nya mulai menumpuk.")]),
 dict(slug="mojokerto", name="Mojokerto", area=["Kota Mojokerto", "Kabupaten Mojokerto", "Jombang"], near="Jombang dan Sidoarjo",
  ctx="Mojokerto punya kawasan industri yang menampung banyak pabrik, ditambah sentra usaha alas kaki dan perdagangan. Usaha pemasok dan subkontraktor di sekitarnya sering harus menunjukkan laporan keuangan yang tersusun sesuai standar untuk masuk daftar vendor atau mendapat kredit.",
  types=[("Pemasok dan subkontraktor kawasan industri", "yang perlu laporan keuangan untuk daftar vendor."),
         ("Produsen alas kaki dan kerajinan", "yang mulai menerima pesanan besar."),
         ("Kontraktor lokal", "yang perlu laporan keuangan untuk SBU dan tender."),
         ("CV dan PT keluarga", "yang ingin pembukuan bulanan dan pajak tertib.")]),
]

def wa(num, city): return f"https://wa.me/{num}?text=" + quote(f"Halo KJA Farhani, saya dari {city} ingin konsultasi laporan keuangan")

def page(c):
    n, url = c["name"], f"{BASE}/kantor-jasa-akuntan-{c['slug']}/"
    title = f"Kantor Jasa Akuntan {n} | Laporan Keuangan & Pajak, KJA Farhani K.N."
    desc = f"Kantor Jasa Akuntan untuk usaha di {', '.join(c['area'][:-1])}, dan {c['area'][-1]}: laporan keuangan, pembukuan bulanan, pajak, dan kredit bank, disusun Akuntan Berpraktik berizin Menkeu."
    faq = [(f"Apakah KJA Farhani bisa melayani klien di {n}?", f"Bisa. Pekerjaan rutin dilakukan online, dan kunjungan ke {n} dijadwalkan untuk pertemuan awal, pengambilan dokumen, atau rapat tutup tahun."),
           ("Apa bedanya KJA dengan KAP?", "KJA menyusun dan merapikan laporan keuangan serta pembukuan. KAP memberi opini audit atas laporan yang sudah disusun. Jika bank atau pemberi kerja mensyaratkan audit, kami dampingi sampai audit KAP."),
           ("Dokumen apa yang perlu disiapkan?", "Rekening koran, catatan penjualan dan pembelian, daftar utang-piutang, daftar aset, kontrak penting, serta bukti setor dan lapor pajak.")]
    s = TPL
    s = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", s, 1, re.S)
    for a in ['name="description"', 'property="og:description"']:
        s = re.sub(rf'<meta {a} content="[^"]*">', f'<meta {a} content="{E(desc)}">', s, 1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', s, 1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, 1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, 1)
    s = re.sub(r'<meta name="geo.placename" content="[^"]*">', f'<meta name="geo.placename" content="{n}">', s, 1)
    ld = [{"@context": "https://schema.org", "@type": "AccountingService", "@id": url + "#kja", "name": f"KJA Farhani K.N. - Kantor Jasa Akuntan {n}",
           "url": url, "image": BASE + "/og-kja.png", "email": "ananta@faindonesia.co.id",
           "address": {"@type": "PostalAddress", "streetAddress": "Pondok Mutiara Asri Blok F9 No. 2, Krajan, Pandanlandung", "addressLocality": "Wagir, Kabupaten Malang", "addressRegion": "Jawa Timur", "postalCode": "65158", "addressCountry": "ID"},
           "areaServed": [{"@type": "City", "name": x} for x in c["area"]] + [{"@type": "State", "name": "Jawa Timur"}],
           "parentOrganization": {"@id": BASE + "/#kja"}, "priceRange": "$$"},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "KJA Farhani K.N.", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": n, "item": url}]}]
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1) + '\n</script>', s, 1, re.S)
    main = (f'<main class="article">\n<h1>Kantor Jasa Akuntan untuk usaha di {n}</h1>\n<p class="meta">Izin KMK 232/KM.1/PPPK/2020, Akuntan Berpraktik AB.715</p>\n'
      f'<p>KJA Farhani K.N. melayani usaha di {n} dan sekitarnya, termasuk {c["near"]}, secara online dan kunjungan terjadwal. Laporan keuangan disusun KJA Farhani K.N. (Kantor Jasa Akuntansi berizin) berizin Menteri Keuangan.</p>\n'
      f'<h2>Layanan untuk usaha di {n}</h2>\n<ul>\n<li>Kompilasi laporan keuangan tahunan sesuai SAK EMKM atau SAK EP, dengan laporan praktisi.</li>\n<li>Outsourcing pembukuan bulanan dan rekonsiliasi bank.</li>\n'
      '<li>Perpajakan: SPT Masa PPh dan PPN, e-Faktur, SPT Tahunan Badan.</li>\n<li>Sistem akuntansi (Accurate, Jurnal, Zahir, Xero) dan SOP keuangan.</li>\n'
      '<li>Pendampingan sampai audit KAP dan pengajuan kredit bank bersama <a href="https://faindonesia.co.id/">FA Consult</a>.</li>\n</ul>\n'
      f'<h2>Kebutuhan khas usaha di {n}</h2>\n<p>{E(c["ctx"])}</p>\n'
      f'<h2>Usaha di {n} yang paling sering butuh KJA</h2>\n<ul>\n' + "".join(f"<li><b>{E(a)}</b> {E(b)}</li>\n" for a, b in c["types"]) + '</ul>\n'
      '<h2>Pertanyaan umum</h2>\n' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq) + '\n'
      f'<div class="box">\n<h2>Konsultasi gratis untuk usaha di {n}</h2>\n<p>Diskusi awal 30 menit tanpa biaya, lewat Zoom atau tatap muka. Hubungi salah satu partner kami.</p>\n'
      f'<a class="btn btn-primary" href="{wa("6282245260121", n)}" target="_blank" rel="noopener">Chat Ananta, CPA</a>\n'
      f'<a class="btn btn-line" href="{wa("6287872558626", n)}" target="_blank" rel="noopener">Chat Farhani, Ak., CA</a>\n</div>\n'
      f'<p>Wilayah lain: <a href="/kantor-jasa-akuntan-malang/">KJA Malang</a>, <a href="/kantor-jasa-akuntan-surabaya/">KJA Surabaya</a>, dan <a href="/kantor-jasa-akuntan-tuban/">KJA Tuban</a>. Cari KAP atau KJPP di {n}: <a href="https://cariakuntan.com/kota/{c["slug"]}/">Cari Akuntan {n}</a>. Baca juga <a href="/artikel/beda-kja-dan-kap/">beda KJA dan KAP</a> dan <a href="/artikel/laporan-keuangan-untuk-kredit-bank-kur/">laporan keuangan untuk kredit bank</a>.</p>\n</main>')
    s = re.sub(r'<main class="article">.*?</main>', lambda m: main, s, 1, re.S)
    d = os.path.join(K, f"kantor-jasa-akuntan-{c['slug']}"); os.makedirs(d, exist_ok=True)
    wt(os.path.join(d, "index.html"), s)

for c in CITIES: page(c)

# footer Wilayah di semua halaman
WIL = "<p>Wilayah: " + ", ".join(f'<a href="/kantor-jasa-akuntan-{s}/">KJA {n}</a>' for s, n in
      [("malang", "Malang"), ("surabaya", "Surabaya"), ("tuban", "Tuban")] + [(c["slug"], c["name"]) for c in CITIES]) + "</p>"
cnt = 0
for root, _, files in os.walk(K):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f); t = rd(p)
        t2 = re.sub(r"<p>Wilayah: <a href=\"/kantor-jasa-akuntan-malang/\">KJA Malang</a>.*?</p>", lambda m: WIL, t, count=1, flags=re.S)
        if t2 != t: wt(p, t2); cnt += 1

sm = rd(os.path.join(K, "sitemap.xml"))
sm = re.sub(r"<!--kja-kota-->.*?<!--/kja-kota-->\n?", "", sm, flags=re.S)
sm = sm.replace("</urlset>", "<!--kja-kota-->\n" + "".join(f"<url><loc>{BASE}/kantor-jasa-akuntan-{c['slug']}/</loc><lastmod>2026-11-01</lastmod></url>\n" for c in CITIES) + "<!--/kja-kota-->\n</urlset>")
wt(os.path.join(K, "sitemap.xml"), sm)

ll = rd(os.path.join(K, "llms.txt"))
ll = re.sub(r"\n## Wilayah Tambahan \(Nov 2026\).*?(?=\n## |\Z)", "", ll, flags=re.S)
ll = ll.rstrip("\n") + "\n\n## Wilayah Tambahan (Nov 2026)\n" + "".join(f"- KJA {c['name']}: {BASE}/kantor-jasa-akuntan-{c['slug']}/\n" for c in CITIES)
wt(os.path.join(K, "llms.txt"), ll)
print("kja kota:", len(CITIES), "halaman; footer diperbarui di", cnt, "file")
