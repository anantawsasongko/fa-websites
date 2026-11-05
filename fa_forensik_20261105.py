# -*- coding: utf-8 -*-
"""5 Nov 2026 (permintaan Bos): push SEO akuntan forensik / penghitungan kerugian untuk laporan ke penyidik.
Latar: banyak permintaan dari Threads (penipuan, penggelapan) minta laporan kerugian ditandatangani akuntan publik.
- /akuntan-forensik/ (pilar) + /akuntan-forensik/<kota>/ untuk semua kota /wilayah/.
- Baris link di tiap /wilayah/<kota>/, tombol di /layanan/, sitemap, llms.
Posisi: laporan untuk perkara antar pihak swasta; kerugian keuangan negara tetap wilayah BPK/BPKP.
Kehadiran ahli tidak dijanjikan, dibahas bila diminta penyidik. Idempoten. Jalankan setelah fa_produk_20261105.py."""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-05"')
exec(compile(_src, "fa_lead_helpers", "exec"))
URLS = []
PIL = "/akuntan-forensik/"
MSG = "Halo FA Indonesia, saya butuh laporan penghitungan kerugian (penipuan/penggelapan) untuk diserahkan ke penyidik."

CITIES = []
for p in sorted(glob.glob(P("wilayah", "*", "index.html"))):
    slug = os.path.basename(os.path.dirname(p))
    m = re.search(r'"position": 3, "name": "([^"]+)", "item": "https://faindonesia\.co\.id/wilayah/' + re.escape(slug) + '/"', rd(p))
    if m: CITIES.append((slug, m.group(1)))

KAPAN = tbl(["Kasus", "Yang Dihitung"], [
  ("Penipuan transaksi atau investasi", "Dana yang sudah ditransfer dikurangi yang sudah kembali, per tanggal"),
  ("Penggelapan oleh karyawan atau kasir", "Selisih kas, penjualan tidak disetor, stok hilang"),
  ("Penggelapan oleh mitra usaha", "Bagi hasil yang tidak dibayar, aset atau dana yang dipakai di luar kesepakatan"),
  ("Proyek atau barang tidak diserahkan", "Uang muka dan pembayaran dikurangi nilai pekerjaan yang benar-benar diterima"),
  ("Sengketa perdata dan wanprestasi", "Kerugian langsung dan dasar perhitungan ganti rugi")])
ALUR = flow([("Upload dokumen", "Bukti transfer, kontrak, chat, nota, rekening koran. Cukup lewat WhatsApp atau Google Drive."),
             ("Review dan biaya tetap", "Kami cek kecukupan bukti, lalu kirim penawaran biaya tetap."),
             ("Penghitungan", "Setiap angka ditelusuri ke dokumen sumber. Bagian yang belum ada buktinya kami tandai."),
             ("Laporan tertulis", "Ditandatangani akuntan publik, siap diserahkan ke penyidik atau kuasa hukum.")])
ISI = ("<ul><li>Ringkasan kasus dan kronologi transaksi.</li><li>Daftar dokumen yang diperiksa.</li>"
       "<li>Metode penghitungan dan asumsinya.</li><li>Tabel kerugian per transaksi dan totalnya.</li>"
       "<li>Batasan: hal yang tidak dapat dihitung karena dokumennya tidak tersedia.</li></ul>")
BATAS = ("<h2>Yang Perlu Diketahui</h2><ul>"
         "<li>Keterangan ahli adalah salah satu alat bukti yang sah dalam KUHAP (UU 20/2025, Pasal 235 ayat 1). Laporan tertulis biasanya sudah cukup sebagai dasar penyidik; kehadiran ahli dibahas terpisah bila penyidik memintanya.</li>"
         "<li>Kami menghitung kerugian dari dokumen. Menentukan ada tidaknya tindak pidana adalah wewenang penyidik dan hakim.</li>"
         "<li>Layanan ini untuk perkara antar pihak swasta. Kerugian keuangan negara (perkara korupsi) dihitung oleh BPK atau BPKP.</li></ul>")
BIAYA = ("<h2>Biaya</h2><p>Biaya tetap disepakati setelah review dokumen, supaya tidak ada kejutan di tengah jalan. "
         "Kasus perorangan dengan dokumen sederhana mulai <b>Rp15 juta</b>, DP 50% saat mulai, pelunasan saat laporan final diserahkan.</p>")
FAQ = [("Apakah laporan ini diterima penyidik?", "Laporan ditandatangani akuntan publik dan menjelaskan metode serta dokumen sumbernya, sehingga bisa dipakai penyidik sebagai dasar. Penilaian akhir tetap ada pada penyidik dan hakim."),
       ("Berapa lama prosesnya?", "Kasus sederhana umumnya 5 sampai 10 hari kerja setelah dokumen lengkap."),
       ("Apakah harus datang ke kantor?", "Tidak. Dokumen dikirim daring dan diskusi lewat video call, dari kota mana pun di Indonesia."),
       ("Bagaimana kalau buktinya belum lengkap?", "Kami kirim daftar kekurangan. Bagian yang tidak ada buktinya dicatat sebagai batasan, tidak ikut dihitung.")]

body = ("<h2>Kapan Anda Butuh Akuntan Forensik</h2>" + KAPAN + "<h2>Cara Kerja</h2>" + ALUR + "<h2>Isi Laporan</h2>" + ISI + BIAYA + BATAS +
        "<h2>Siapa yang Mengerjakan</h2><p>Penghitungan dikerjakan tim FA Indonesia dan laporan ditandatangani akuntan publik dari "
        "<a href=\"/kap-dhn/\">KAP DHN &amp; Rekan</a>, kantor akuntan publik berizin Menteri Keuangan.</p>"
        "<p>Terkait: <a href=\"/akuntan-terdekat/\">Akuntan Terdekat</a> · <a href=\"/jasa-audit-laporan-keuangan/\">Audit Laporan Keuangan</a> · <a href=\"/wilayah/\">Cari per Kota</a></p>")
svc_page(PIL, "Layanan · Akuntan Forensik", "Akuntan Forensik: Laporan Penghitungan Kerugian untuk Penyidik",
  "Untuk korban penipuan, penggelapan, atau sengketa usaha yang perlu angka kerugian yang rapi dan bisa dipertanggungjawabkan, ditandatangani akuntan publik.",
  body, FAQ, "Akuntan Forensik: Jasa Hitung Kerugian Penipuan dan Penggelapan untuk Laporan Polisi | FA Indonesia",
  "Jasa akuntan forensik: laporan penghitungan kerugian penipuan, penggelapan, dan sengketa usaha, ditandatangani akuntan publik, siap diserahkan ke penyidik. Daring.",
  "Akuntansi Forensik dan Penghitungan Kerugian", "Forensic accounting", "/wilayah/", "Pilih Kota", MSG, "Akuntan Forensik")
URLS.append(PIL)

# halaman per kota
for slug, city in CITIES:
    path = f"{PIL}{slug}/"
    b = (f"<p>Kasus penipuan atau penggelapan di {E(city)} sering macet karena angka kerugiannya belum jelas: transfer bercampur, sebagian uang sudah kembali, dan bukti tersebar di chat. "
         f"Kami menyusun laporan penghitungan kerugian yang bisa diserahkan ke penyidik di wilayah {E(city)}, dikerjakan daring.</p>"
         "<h2>Kasus yang Kami Hitung</h2>" + KAPAN + "<h2>Cara Kerja</h2>" + ALUR + BIAYA + BATAS +
         f"<p>Selengkapnya: <a href=\"{PIL}\">Akuntan Forensik FA Indonesia</a> · Layanan lain di kota ini: <a href=\"/wilayah/{slug}/\">Akuntan dan KAP {E(city)}</a></p>")
    svc_page(path, f"Akuntan Forensik · {city}", f"Akuntan Forensik {city}: Hitung Kerugian Penipuan dan Penggelapan",
      f"Laporan penghitungan kerugian untuk diserahkan ke penyidik di {city}, ditandatangani akuntan publik. Dokumen dikirim daring.",
      b, FAQ[:3], f"Akuntan Forensik {city}: Hitung Kerugian Penipuan, Penggelapan untuk Laporan Polisi | FA Indonesia",
      f"Butuh akuntan forensik di {city}? Laporan penghitungan kerugian penipuan dan penggelapan, ditandatangani akuntan publik, siap untuk penyidik. Mulai Rp15 juta.",
      f"Akuntan Forensik {city}", "Forensic accounting", PIL, "Semua Kota",
      f"Halo FA Indonesia, saya dari {city}, butuh laporan penghitungan kerugian untuk penyidik.", f"Akuntan Forensik {city}")
    URLS.append(path)

# hub: daftar kota di pilar
pp = P("akuntan-forensik", "index.html"); t = re.sub(r"<!--fa-forensik-kota-->.*?<!--/fa-forensik-kota-->", "", rd(pp), flags=re.S)
lst = " · ".join(f'<a href="{PIL}{s}/">{E(c)}</a>' for s, c in CITIES)
blk = f'<!--fa-forensik-kota--><h2>Per Kota</h2><details class="fold"><summary>Semua Kota ({len(CITIES)})</summary><p class="t">{lst}</p></details><!--/fa-forensik-kota-->'
k = t.find("<h2>Siapa yang Mengerjakan</h2>"); t = t[:k] + blk + t[k:]; wtxt(pp, t)

# link dari /wilayah/<kota>/
for slug, city in CITIES:
    p = P("wilayah", slug, "index.html"); t = re.sub(r"<!--fa-forensik-w-->.*?<!--/fa-forensik-w-->", "", rd(p), flags=re.S)
    add = (f'<!--fa-forensik-w--><p class="t">Jadi korban penipuan atau penggelapan? Kami menyusun laporan penghitungan kerugian untuk penyidik: '
           f'<a href="{PIL}{slug}/">Akuntan Forensik {E(city)}</a>.</p><!--/fa-forensik-w-->')
    k = t.find("<!--/fa-kw-w-->")
    if k < 0: continue
    k += len("<!--/fa-kw-w-->"); wtxt(p, t[:k] + add + t[k:])

lp = P("layanan", "index.html"); t = re.sub(r"<!--fa-forensik-lay-->.*?<!--/fa-forensik-lay-->", "", rd(lp), flags=re.S)
a = '<a class="btn line" href="/jasa-laporan-keuangan-bulanan/">Laporan Keuangan Bulanan</a>'
if a in t: wtxt(lp, t.replace(a, a + f'<!--fa-forensik-lay--><a class="btn line" href="{PIL}">Akuntan Forensik</a><!--/fa-forensik-lay-->', 1))

sm = re.sub(r"<!--fa-forensik-->.*?<!--/fa-forensik-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-forensik-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'0.9' if u == PIL else '0.6'}</priority></url>\n" for u in URLS) + "<!--/fa-forensik-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
line = "- Akuntan forensik: laporan penghitungan kerugian penipuan/penggelapan untuk penyidik, ditandatangani akuntan publik → https://faindonesia.co.id/akuntan-forensik/\n"
ll = rd(P("llms.txt")).replace(line, "")
ll = ll.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + line, 1) if "\n## Layanan Spesifik\n" in ll else ll.rstrip("\n") + "\n" + line
wtxt(P("llms.txt"), ll)
print("fa_forensik ok", len(URLS), "url, kota", len(CITIES))
