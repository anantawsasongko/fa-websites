# Dieksekusi di build.py setelah seo_kecamatan.py (3 Nov 2026).
# Halaman andalan /jasa-pembukuan/ (terima beres: upload bon ke Drive, laporan jadi) + /jasa-pembukuan/malang/,
# lalu kotak tautan ke halaman andalan di semua halaman jasa laporan keuangan, kecamatan, dan beranda.
import subprocess as _sp
_sp.run(["python3", os.path.join(ROOT, "contoh_laporan_pdf.py")], check=True)
PB = "/jasa-pembukuan/"
PDF = "/files/contoh-laporan-keuangan-bulanan-jasa-pembukuan.pdf"
FAU = "https://faindonesia.co.id"
PAKET = "<style>.pbt table{min-width:900px}.pbt td:nth-child(3){min-width:400px}.pbt td:nth-child(2){white-space:nowrap;font-weight:600}.pbt th[scope=row]{min-width:190px}</style><div class=\"pbt\">" + tblx(["Paket", "Mulai", "Isi"], [
    ("Pembukuan UMKM dan Perorangan", "Rp900 ribu/bulan", "Input bon dan nota, rekonsiliasi bank, laporan laba rugi, neraca, arus kas, catatan akuntan setiap bulan (SAK EMKM)"),
    ("Pembukuan PT dan CV", "Rp2 juta/bulan", "Seperti paket UMKM, ditambah utang piutang per pihak, persediaan, aset tetap, dan laporan sesuai SAK EP"),
    ("Laporan Tahunan PT (SABH)", "Rp3 juta", "Laporan tahunan sesuai Permenkum 49/2025, siap dibawa ke notaris. Biaya notaris terpisah, biasanya Rp1 sampai 2 juta"),
    ("SPT Tahunan Badan", "Rp3 juta", "Penyusunan dan pelaporan SPT Tahunan PPh Badan dari laporan keuangan yang sudah kami susun"),
    ("Pajak Bulanan", "Rp3 juta", "PPh potput dan PPN masa, dikerjakan konsultan pajak (KKP) mitra"),
    ("Audit Laporan Keuangan", "Sesuai penawaran", "Dilaksanakan KAP mitra yang terdaftar OJK, terpisah dari tim penyusun")]) + "</div>"
PB_FAQ = [
 ("Berapa harga jasa pembukuan per bulan?", "Paket UMKM dan perorangan mulai Rp900 ribu per bulan, paket PT dan CV mulai Rp2 juta per bulan. Harga akhir bergantung pada jumlah transaksi, jumlah rekening, dan persediaan. Laporan tahunan PT, SPT Tahunan Badan, dan pajak bulanan dihitung terpisah, masing-masing mulai Rp3 juta."),
 ("Apa yang perlu saya kirim?", "Cukup upload foto atau scan bon dan nota, catatan kas sederhana (single entry, Excel, atau foto buku catatan), dan mutasi rekening ke folder Google Drive yang kami siapkan. Sisanya kami kerjakan."),
 ("Kapan laporan bulanan selesai?", "5 sampai 10 hari kerja setelah bukti bulan berjalan lengkap di Drive."),
 ("Bagaimana kalau bon saya tidak lengkap?", "Transaksi tetap dicatat dari mutasi rekening, lalu kami kirim daftar bon yang perlu dilengkapi. Contohnya ada di catatan akuntan pada contoh laporan."),
 ("Saya sudah langganan aplikasi akuntansi, apakah tetap bisa?", "Bisa. Kami dapat bekerja di aplikasi yang sudah Anda pakai, misalnya Jurnal, Accurate, atau Zahir, atau memakai format kami sendiri. Anda tidak perlu menginput sendiri."),
 ("Apakah melayani di luar Malang?", "Ya. Semua dikerjakan daring untuk klien di seluruh Indonesia. Kantor kami di Malang."),
 ("Apakah laporan bisa dipakai untuk bank dan audit?", "Ya. Laporan disusun sesuai SAK EMKM atau SAK EP, siap untuk pengajuan kredit, SPT, laporan tahunan PT, dan audit oleh KAP. Untuk satu perusahaan, penyusun laporan dan auditornya selalu pihak berbeda."),
]
PORTO = ("<div class=\"prose\"><h2>Pengalaman Tim dan Mitra</h2><ul>"
 "<li>Ribuan UMKM di seluruh Indonesia</li><li>Ratusan BPR</li><li>Puluhan rumah sakit di DKI Jakarta dan Jawa Tengah</li>"
 "<li>Puluhan hotel di Bali dan beberapa hotel di Papua</li><li>Perusahaan konstruksi di Sumatera, Batam, Kalimantan, dan Sulawesi</li></ul>"
 "<p>Semuanya dilayani daring. Klien tidak perlu datang ke kantor dan tidak perlu belajar akuntansi.</p></div>")
TIM = ("<div class=\"prose\"><h2>Siapa yang Mengerjakan</h2><ul>"
 f"<li><b>KJA Farhani</b>, Kantor Jasa Akuntansi berizin Kementerian Keuangan (KMK No. 232/KM.1/PPPK/2020), di Malang. <a href=\"{FAU}/kja-farhani/\">Profil</a></li>"
 f"<li><b>Ananta W. Sasongko, CPA</b>, koordinator dan kontak klien. <a href=\"{FAU}/ananta-w-sasongko/\">Profil</a></li>"
 f"<li><b>KAP DHN &amp; Rekan</b>, terdaftar OJK, untuk klien yang perlu audit. <a href=\"{FAU}/kap-dhn/\">Profil</a></li></ul></div>")
ALUR = ("<div class=\"prose\"><h2>Cara Kerjanya</h2><ol>"
 "<li><b>Diskusi singkat lewat WhatsApp.</b> Jenis usaha, jumlah transaksi, dan laporan yang dibutuhkan. Gratis.</li>"
 "<li><b>Kami buatkan folder Google Drive.</b> Subfolder per bulan: Bon Pembelian, Nota Penjualan, Biaya, Mutasi Rekening.</li>"
 "<li><b>Anda upload bon.</b> Foto dari HP sudah cukup. Catatan single entry atau buku kas juga boleh.</li>"
 "<li><b>Kami input, klasifikasi, dan rekonsiliasi.</b> Dikerjakan tim KJA Farhani.</li>"
 "<li><b>Laporan bulanan terkirim</b> 5 sampai 10 hari kerja setelah bukti lengkap, lengkap dengan catatan tindak lanjut.</li>"
 "<li><b>Akhir tahun siap dipakai</b> untuk SPT, laporan tahunan PT, kredit bank, atau audit.</li></ol></div>")
APP = ("<div class=\"prose\"><h2>Aplikasi Akuntansi atau Jasa Pembukuan?</h2>"
 "<p>Aplikasi akuntansi membantu bila ada orang di perusahaan yang sempat dan paham menginput setiap hari. Bila tidak ada, aplikasi berbayar tetap kosong dan laporan tidak pernah jadi. Jasa pembukuan menyelesaikan bagian itu: Anda cukup mengumpulkan bon, kami yang mencatat dan menyusun laporan.</p>"
 + tblx(["", "Aplikasi Akuntansi", "Jasa Pembukuan Terima Beres"], [
   ("Yang menginput", "Anda atau staf Anda", "Tim akuntan kami"),
   ("Butuh paham akuntansi", "Ya", "Tidak"),
   ("Laporan siap untuk bank dan pajak", "Bergantung pada kualitas input", "Ya, disusun dan direview akuntan"),
   ("Bisa digabung", "Ya, kami bisa bekerja di aplikasi yang Anda pakai", "")])
 + f"<p>Ulasan lengkapnya ada di <a href=\"/artikel/aplikasi-akuntansi-atau-jasa-pembukuan-mana-yang-tepat/\">Aplikasi Akuntansi atau Jasa Pembukuan</a> dan <a href=\"/artikel/harga-jasa-pembukuan-2026-paket-dan-yang-menentukan/\">Harga Jasa Pembukuan 2026</a>.</p></div>")

def pb_page(path, crumb, h1, sub, title, desc, msg, extra_top="", faq=PB_FAQ, area="Indonesia"):
    url = DOMAIN + path
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": "Jasa Pembukuan dan Laporan Keuangan", "serviceType": "Bookkeeping and financial statement preparation", "url": url,
         "areaServed": {"@type": "Place", "name": area}, "provider": {"@type": "AccountingService", "name": "KJA Farhani", "address": {"@type": "PostalAddress", "addressLocality": "Malang", "addressRegion": "Jawa Timur", "addressCountry": "ID"}},
         "offers": [{"@type": "Offer", "name": "Pembukuan UMKM dan Perorangan", "price": "900000", "priceCurrency": "IDR", "priceSpecification": {"@type": "UnitPriceSpecification", "price": "900000", "priceCurrency": "IDR", "unitText": "bulan"}},
                    {"@type": "Offer", "name": "Pembukuan PT dan CV", "price": "2000000", "priceCurrency": "IDR", "priceSpecification": {"@type": "UnitPriceSpecification", "price": "2000000", "priceCurrency": "IDR", "unitText": "bulan"}}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]}]}
    html = head(title, desc, url, extra=ldtag(ld)) + header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / {crumb}</p>
  <p class="label" style="margin-top:14px">Terima Beres · Dikerjakan Akuntan</p>
  <h1>{h1}</h1>
  <p class="sub">{sub}</p>
  <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(msg)}" target="_blank" rel="noopener">Chat Ananta, CPA</a><a class="btn" style="border:1px solid var(--line)" href="{PDF}" target="_blank" rel="noopener">Lihat Contoh Laporan (PDF)</a></div>
  {extra_top}
  {ALUR}
  <div class="prose"><h2>Paket dan Harga</h2><p>Harga mulai, sebelum pajak. Angka pasti disampaikan setelah melihat contoh transaksi satu bulan.</p></div>
  {PAKET}
  {PORTO}
  {APP}
  {TIM}
  <div class="prose"><h2>Tanya Jawab</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)}</div>
  <div class="cta-box"><h3>Mulai Bulan Ini</h3><p style="color:var(--muted)">Kirim jenis usaha, kota, dan perkiraan jumlah transaksi per bulan. Folder Drive bisa disiapkan hari ini.</p><a class="btn btn-wa" style="justify-self:start" href="{wa(msg)}" target="_blank" rel="noopener">Chat Ananta, CPA</a></div>
</main>
''' + footer(ID)
    write(path, html); urls.append(path)

pb_page(PB, "Jasa Pembukuan", "Jasa Pembukuan dan Laporan Keuangan Terima Beres: Upload Bon ke Drive, Laporan Jadi",
  "Anda cukup upload foto bon, nota, dan catatan kas ke Google Drive. Akuntan kami yang menginput, merekonsiliasi, dan mengirim laporan keuangan setiap bulan, siap untuk bank, pajak, laporan tahunan PT, dan audit. Mulai Rp900 ribu per bulan untuk UMKM, Rp2 juta untuk PT dan CV.",
  "Jasa Pembukuan Terima Beres Mulai Rp900 Ribu/Bulan: Upload Bon, Laporan Jadi | cariakuntan.com",
  "Jasa pembukuan dan laporan keuangan terima beres: upload bon ke Google Drive, akuntan yang input. UMKM mulai Rp900 ribu/bulan, PT/CV mulai Rp2 juta. Laporan 5-10 hari kerja.",
  "Selamat siang Pak Ananta, saya tertarik jasa pembukuan terima beres. Jenis usaha saya: ")
MLG = ("<div class=\"prose\"><h2>Untuk Usaha di Malang Raya</h2><p>KJA Farhani berkantor di Malang dan melayani usaha di Kota Malang, Kabupaten Malang, dan Kota Batu: "
 "Klojen, Lowokwaru, Blimbing, Sukun, Kedungkandang, Singosari, Lawang, Kepanjen, Pakis, Karangploso, Dau, Batu, dan kecamatan lain. "
 "Semua dikerjakan lewat Drive dan WhatsApp; bila perlu, pertemuan langsung bisa dijadwalkan di Malang.</p></div>")
FAQ_M = [("Di mana jasa pembukuan terpercaya di Malang?", "KJA Farhani adalah Kantor Jasa Akuntansi berizin Kementerian Keuangan yang berkantor di Malang. Paket pembukuan UMKM mulai Rp900 ribu per bulan, PT dan CV mulai Rp2 juta per bulan.")] + PB_FAQ
pb_page(PB + "malang/", "Jasa Pembukuan Malang", "Jasa Pembukuan dan Laporan Keuangan di Malang: Terima Beres, Dikerjakan KJA Berizin",
  "Untuk UMKM, CV, dan PT di Kota Malang, Kabupaten Malang, dan Batu. Upload bon ke Google Drive, KJA Farhani yang menyusun laporan keuangan setiap bulan. Mulai Rp900 ribu per bulan.",
  "Jasa Pembukuan Malang Mulai Rp900 Ribu/Bulan: KJA Berizin, Terima Beres | cariakuntan.com",
  "Jasa pembukuan dan laporan keuangan di Malang oleh KJA Farhani berizin Kemenkeu. Upload bon ke Drive, laporan jadi. UMKM mulai Rp900 ribu, PT/CV Rp2 juta per bulan.",
  "Selamat siang Pak Ananta, saya di Malang dan tertarik jasa pembukuan terima beres. Jenis usaha saya: ", extra_top=MLG, faq=FAQ_M, area="Malang")

# kotak tautan ke halaman andalan
PBOX = (f'<div class="more pb-box"><h3>Jasa Pembukuan Terima Beres</h3><p style="color:var(--muted);margin:0 0 10px">Upload bon ke Google Drive, akuntan kami yang menyusun laporan keuangan tiap bulan. UMKM mulai Rp900 ribu, PT dan CV mulai Rp2 juta per bulan.</p>'
        f'<div class="citylist"><a href="{PB}">Lihat Paket Jasa Pembukuan</a> <a href="{PDF}">Contoh Laporan (PDF)</a></div></div>')
_n = 0
for _d, _, _fs in os.walk(SITE):
    if "index.html" not in _fs: continue
    _rel = os.path.relpath(_d, SITE).replace(os.sep, "/")
    if not (_rel == "." or "jasa-laporan-keuangan" in _rel or "/kecamatan/" in _rel + "/" or _rel.startswith("layanan")): continue
    if _rel.startswith("jasa-pembukuan"): continue
    _p = os.path.join(_d, "index.html"); _t = open(_p, encoding="utf-8").read()
    if "pb-box" in _t or "</main>" not in _t: continue
    _i = _t.rfind("</main>"); open(_p, "w", encoding="utf-8").write(_t[:_i] + PBOX + _t[_i:]); _n += 1
print("jasa pembukuan: 2 halaman, kotak di", _n)
