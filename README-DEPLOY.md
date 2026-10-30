# Deploy Kit Website FA Indonesia (Cloudflare Pages)

Deploy OTOMATIS: push ke GitHub anantawsasongko/fa-websites (branch main) -> Cloudflare Pages project faindonesia-web (out/faindonesia) dan cariakuntan-web (out/cariakuntan). Project lama faindonesia/cariakuntan (upload manual) jadi cadangan. Deploy HANYA ke Cloudflare Pages (akun ananta.w.sasongko@gmail.com, account id afb677a1f9df62a249d390aef72c233c). Netlify sudah tidak dipakai.

## 7 Project Cloudflare Pages
| Project | Domain | Isi |
|---|---|---|
| cariakuntan | cariakuntan.com (+www) | Lead-gen makelar jasa (build dari cariakuntan/build.py) |
| faindonesia | faindonesia.co.id (+www) | Website FA + apps digabung (audit-ready, saturn, cek-psak-118) |
| faindonesia-jupiter | faindonesia-jupiter.pages.dev | Jupiter standalone, / redirect ke faindonesia.co.id/audit-ready/ |
| faindonesia-saturn | faindonesia-saturn.pages.dev | Saturn standalone + host /saturn/kk/ |
| faindonesia-venus | faindonesia-venus.pages.dev | Venus standalone, / redirect ke /cek-psak-118/ |
| faindonesia-apps | faindonesia-apps.pages.dev | Host /files/ (PDF, xlsx, cv noindex), / redirect ke faindonesia.co.id/apps/ |
| kja-farhani | kja-farhani.pages.dev | Website KJA Farhani |

## Alur Update
1. Update `cariakuntan/feed.json` (berita bisnis/pajak/bank/pasar modal terbaru, format [tanggal, judul, link, sumber]).
2. Opsional tambah artikel di `cariakuntan/gen/*.json`, lalu `python3 cariakuntan/build.py`.
3. `python3 prep.py` -> hasil di `out/` (zip di `zips/` hanya lokal, tidak di-commit sejak 28 Okt 2026 supaya clone Cloudflare cepat).
4. Cloudflare dashboard > Workers & Pages > project > Create deployment > upload zip project yang berubah.
5. Ping IndexNow (key c4f1a8e2b7d94e0f9a3c6b2d5e8f1a70) untuk cariakuntan.com.

## Catatan
- Sumber FA/KJA/apps: folder `FA-Indonesia_Website_SIAP-UPLOAD-v58`, `FA-*`, `KJA-Farhani_site_v12-netlify-primary`. Edit konten di sana, bukan di `out/`.
- Nav FA: Apps, Layanan, E-Book, Wawasan (/artikel/, artikel + berita otomatis), Cari Akuntan (ke cariakuntan.com), Kontak; diatur prep.py, i18n EN/ZH ikut. Mobile rata kiri-kanan, font 12.5px agar 6 tab muat di 360px.
- Kredit Netlify tinggal ±44: JANGAN deploy konten ke Netlify lagi, sisakan untuk 2 deploy redirect (faindonesia, cariakuntan).
- Email ananta@faindonesia.co.id via ImprovMX: MX mx1/mx2.improvmx.com (10/20) + TXT SPF. Jangan dihapus di DNS Cloudflare.
- Nomor HP tidak pernah tampil sebagai teks; WA hanya lewat tombol. Tanpa em dash.

## Anti Duplikat SEO
- `*.pages.dev` untuk cariakuntan, faindonesia, jupiter, saturn, venus diberi `X-Robots-Tag: noindex` (lewat _headers dari prep.py). Yang diindeks hanya domain asli.
- kja-farhani.netlify.app sudah 301 ke kja-farhani.pages.dev (deploy redirect-only, 25 Okt 2026).
- SETELAH nameserver faindonesia.co.id / cariakuntan.com aktif di Cloudflare dan custom domain terpasang: deploy `netlify-redirect/faindonesia.zip` ke Netlify project faindonesia dan `netlify-redirect/cariakuntan.zip` ke Netlify project cariakuntan (sekali saja). JANGAN sebelum itu, karena domain masih dilayani Netlify.
- Setelah itu Bos menghapus project Netlify faindonesia-jupiter, -saturn, -venus, -apps.

## SEO Kota x Layanan (25 Okt 2026)
- `cariakuntan/seo_city.py` (di-exec build.py): 86 halaman kota (KAP, KJPP, konsultan pajak, jasa laporan keuangan + FAQ schema), 64 halaman layanan x 16 kota prioritas (`/kota/<kota>/<kap|kjpp|konsultan-pajak|jasa-laporan-keuangan>/`), 4 hub `/layanan/<...>/`, tabel "per kota" di beranda.
- Kota prioritas ada di daftar PRIORITY. Tambah kota di sana untuk membuat 4 halaman layanannya.
- Sudah request indexing GSC: /kota/malang|surabaya|batam|jakarta/, /kota/malang/jasa-laporan-keuangan/, /layanan/kap/. Sisanya digilir runner maksimal 8 URL per hari.

## Update 25 Okt 2026 (siang)
- FA: halaman baru /laporan-tahunan-pt/ (Permenkum 49/2025), artikel /artikel/laporan-tahunan-pt-permenkum-49-2025/, blok "Tahapan Kerja" di /konsultan-persiapan-ipo/, kartu Pelaporan Korporasi di beranda, link footer semua halaman, sitemap, llms.txt. Script: fa_update_20261025.py (idempoten, sudah dijalankan ke folder v58).
- cariakuntan: kartu kebutuhan "Laporan Tahunan PT" (ganti Koperasi), "Pendanaan & IPO" ditambah IPO mapping; 2 artikel baru di gen/berita.json dan gen/lk.json.
- Deploy 25 Okt: faindonesia dan cariakuntan sudah di-upload ke Cloudflare Pages (live di *.pages.dev).
- PENTING: domain faindonesia.co.id dan cariakuntan.com masih memakai nameserver NSONE (Netlify). Ganti nameserver di registrar ke amy.ns.cloudflare.com dan hans.ns.cloudflare.com (cek angka NS cariakuntan di dashboard zone-nya), lalu pasang Custom domain di tiap project Pages. Sebelum itu, domain masih menampilkan versi Netlify lama.

## Beranda Ringkas (25 Okt 2026, sore)
- Beranda FA dibuat ringkas gaya cariakuntan: hero + angka, Peta Layanan (bagan 3 jalur), bar chart kredit cair per bank, Pendekatan (alur 5 tahap), rentang aset klien, Cara Mulai (4 langkah), Jelajahi, Kontak. Berita tidak lagi di beranda (hanya di Wawasan).
- Section detail dipindah: /layanan/ (layanan, paket, fee, rekam jejak, arsip, galeri, pendiri, grup, ekosistem, afiliasi) dan /unduhan/ (materi gratis, publikasi, kabar kanal; ditautkan dari /buku/). Tab Layanan sekarang ke /layanan/.
- Script: fa_home_simple_20261025.py, membangun dari backup/index-v58-full-20261025.html (sumber lengkap lama). Untuk edit konten section lama, edit backup lalu jalankan ulang script. Link lama /#rekam dsb otomatis diarahkan ke halaman barunya.
- Revisi 25 Okt malam: /unduhan/ dihapus (301 ke /buku/#unduhan). Materi gratis + publikasi disisipkan ke /buku/ (tab E-Book), galeri + kabar kanal ke /artikel/. Tab Wawasan diganti Eksplor (EN Explore, ZH 探索). Sisipan ditandai komentar fa-inj di file sumber dan dibangun ulang tiap script dijalankan. Label/tombol pakai Title Case.
- QRIS donasi (25 Okt malam): widget `shared/donasi.js` + `shared/qris-fa-indonesia.jpg`, dipasang oleh prep.py (`add_donasi`) di /buku/ (materi gratis FA Edu, brosur FA Consult tidak), /cek-psak-118/ (tab Hasil + Download Excel), /audit-ready/ (Download Excel/Word CALK, dilewati kalau sudah aktivasi lisensi), dan screening cariakuntan (4 bahasa). Nominal Rp19.001, bisa dilewati, sekali per sesi per layanan; setelah hasil muncul ada pill "Donasi via QRIS" untuk buka QRIS lagi.

## SEO Push Lokal (25 Okt 2026 malam)
- cariakuntan: semua kota x 4 layanan inti punya halaman sendiri; 94 kota (+8 kota baru di kawasan.py EXTRA_CITIES); 89 kawasan bisnis (cariakuntan/kawasan.py, generator seo_kawasan.py) dengan hub + 4 halaman layanan (/kota/<kota>/<kawasan>/<kap|kjpp|konsultan-pajak|jasa-laporan-keuangan>/); BOOST konteks pasar untuk Malang, Surabaya, Jember, Pasuruan, Batam; kotak silang ke FA di setiap halaman kota/kawasan.
- FA: fa_seo_20261025.py (jalankan setelah fa_home_simple): 30 artikel dari fa_content/articles/*.json (spec di fa_content/SPEC-ARTIKEL.md), kartu per topik di Eksplor, /konsultan-rumah-sakit/ dan /konsultan-unit-cost-rumah-sakit/ (+ per kota), /wilayah/ (kota + kawasan), footer, sitemap, llms.txt.
- Urutan build: python3 fa_home_simple_20261025.py && python3 fa_seo_20261025.py && python3 fa_lead_20261026.py && python3 fa_psak_20261026.py && python3 fa_kredit_20261026.py && python3 fa_seller_20261026.py && python3 fa_tone_20261026.py && python3 fa_mitra_20261027.py && python3 fa_deal_20261028.py && python3 fa_viral_20261028.py && python3 fa_viral_20261028b.py && python3 fa_seo20_20261030.py && python3 fa_rapi_20261027.py && python3 fa_beranda_20261030.py && python3 cariakuntan/build.py && python3 fa_screen_seo_20261026.py && python3 prep.py

## Halaman dari Lead Nyata (26 Okt 2026)
- fa_lead_20261026.py: /jasa-implementasi-psak-118/ dan /konsultan-kredit-distributor-importir/ (dua lead WA hari itu: implementasi PSAK 118 dan plafon kredit distributor/importir), kotak CTA di artikel terkait, blok di /layanan/, sitemap, llms.txt. Idempoten.
- fa_seo_20261025.py diperbaiki: blok llms "Artikel Eksplor Terbaru" tidak lagi dobel saat dijalankan ulang.
- Push tanpa akses git: GitHub > Add file > Upload files per folder; commit perantara diberi [CF-Pages-Skip], commit terakhir tanpa tanda itu supaya Cloudflare build sekali.

## Cluster Implementasi PSAK (26 Okt 2026 sore)
- fa_psak_20261026.py: hub /jasa-implementasi-psak/ + 8 halaman (PSAK 109, 115, 116, 117, 212, 219, konsolidasi PSAK 110, transisi SAK EP ke PSAK). Penomoran SAK Online IAI. Kotak CTA di 7 halaman terkait, tombol di /layanan/, sitemap, llms.txt. Idempoten, jalankan setelah fa_lead_20261026.py.

## FA Venus Cek Kapasitas Kredit (26 Okt 2026 malam)
- fa_kredit_20261026.py: /cek-kapasitas-kredit/ (kredit baru, top up, take over): DSCR, plafon per batas (DSCR, Utang/EBITDA, DER, agunan LTV 70%, siklus modal kerja untuk KMK), matriks kemampuan bayar per bunga x tenor, bunga maksimal atau tenor minimal untuk plafon incaran, langkah lanjut. Lead ke Google Sheet CariAkuntan (goal diawali 'FA Cek Kapasitas Kredit'). QRIS Rp19.001 lewat prep.py add_donasi (key venus-kredit). Juga tertanam di beranda FA tepat di bawah hero (section #cek-kredit, penanda fa-kk-home). Kartu di /apps/, CTA di halaman kredit, tombol /layanan/, sitemap, llms.txt.

## Aturan Nada (26 Okt 2026)
- JANGAN PERNAH menulis "ditangani langsung oleh Ananta W. Sasongko, CPA" atau variasinya (EN/ZH juga) di FA, CariAkuntan, KJA, maupun slides. Pakai bahasa tim: "didampingi tim FA Indonesia", "tim CA dan CPA". fa_tone_20261026.py membersihkan semua sumber; jalankan sebelum prep.py.

## SEO Alat Screening (26 Okt 2026 malam)
- CariAkuntan /screening/: tanpa email (hasil langsung di web, satu tombol kirim WhatsApp), indikator Jalur IPO BEI, FAQ + WebApplication schema. Kotak CTA screening di semua halaman ID (fa_screen_seo_20261026.py).
- FA: halaman keyword dengan kalkulator tertanam /kalkulator-dscr/, /simulasi-plafon-kredit-usaha/, /cek-kelayakan-ipo/ (dibuat di fa_kredit_20261026.py); CTA Cek Kredit & Pendanaan di semua halaman wilayah dan artikel.
- Batas rasio (DSCR 1,25x, utang/EBITDA 3,5x, DER 2,5x, LTV 70%; CA: DER 1/2,5x, utang/EBITDA 3/4,5x) adalah praktik analis kredit, bukan peraturan. Syarat IPO: Peraturan BEI I-A (opsi keuangan Papan Utama), perubahan berlaku 4 Feb 2026 (masa operasi, free float), POJK 53/2017 (Akselerasi).

## KAP Murah per Kota (26 Okt 2026 malam)
- cariakuntan/seo_murah.py (exec dari build.py setelah seo_kawasan): /kap-murah/ + /kota/<kota>/kap-murah/ (95 halaman). Sudut: "KAP murah, apakah bijak, independen, dan dapat dipercaya?" lalu ajak diskusi kebutuhan dulu di CariAkuntan. FAQ schema, link kawasan, kota terdekat, FA.
- fa_screen_seo_20261026.py: tombol "KAP Murah di <Kota>" di kotak CTA halaman kota CA, tombol "Cari KAP Murah di <Kota>" (ke CA) di halaman wilayah FA, artikel FA /artikel/kap-murah-apakah-bijak/ yang mengarah ke cariakuntan.com.

## Pembayaran Online Midtrans (27 Okt 2026)
- Produk berbayar (FA Jupiter day pass/tahunan, e-book, layanan sesuai penawaran) dibayar lewat Midtrans Snap di /bayar/ (tombol Bayar Online). Transfer BRI + invoice tetap ada sebagai cadangan.
- Server: `shared/pay/_worker.js` + `_routes.json` (hanya /api/*), disalin prep.py ke out/faindonesia. Harga dihitung di worker (tabel PRODUCTS), bukan dari browser. Kalau harga di /bayar/ diubah, ubah juga PRODUCTS.
- Env var project faindonesia-web: MIDTRANS_SERVER_KEY (Secret), MIDTRANS_CLIENT_KEY, MIDTRANS_PRODUCTION=true saat live. Tanpa Server Key tombol Bayar Online otomatis tersembunyi.
- Dashboard Midtrans: Payment Notification URL `https://faindonesia.co.id/api/pay/notify`; Finish/Unfinish/Error Redirect URL `https://faindonesia.co.id/bayar/selesai/`.
- Lunas: /bayar/selesai/?order_id=... menampilkan kode Audit Ready (dibuat otomatis, format sama dengan app) dan tombol aktivasi /audit-ready/?kode=...; e-book dikirim manual. Webhook mencatat order lunas/expire ke Google Sheet lead (goal diawali "FA Pembayaran Midtrans", kode akses ada di summary).
- Donasi QRIS layanan gratis naik ke Rp19.001 (semua titik).

## Mitra RM Bank & Sekuritas + Perapian (27 Okt 2026)
- fa_mitra_20261027.py: /mitra-rm-bank/ dan /mitra-sekuritas/ (dua arah rujukan, tanpa biaya untuk bank/sekuritas), 2 artikel Eksplor (cara-rm-bank-mencari-debitur-korporasi, cara-sekuritas-mencari-calon-emiten-ipo), link footer semua halaman, blok /layanan/, kotak di halaman kredit/IPO terkait, sitemap, llms.txt. Idempoten.
- fa_rapi_20261027.py (jalankan terakhir sebelum prep.py): FAQ jadi accordion di semua halaman, teks tebal artikel terlihat, artikel lama dapat eyebrow kategori + Baca Juga, Eksplor dapat topik PSAK & SAK Terbaru (tidak ada lagi "Artikel Lainnya"), en dash jadi tanda hubung, klaim "saat ini memimpin persiapan IPO" jadi "berpengalaman memimpin", "dipimpin Ananta" jadi kata tim, rentang aset Rp1-500 miliar diganti semua skala. Ikut mengoreksi backup beranda.

## Lencana Keamanan Data (27 Okt 2026)
- `shared/secure.js` dipasang prep.py (`add_secure`): FA Secure (beranda FA, Cek Kredit, kalkulator DSCR, simulasi plafon, cek IPO, Cek PSAK 118, FA Jupiter, FA Saturn), CariAkuntan Secure (screening 4 bahasa + /screening/), UpdateSAK Secure (kalkulator beranda).
- Mode harus sesuai perilaku kode: local (tidak ada data terkirim), drive (simpan ke Google Drive pengguna), send (dihitung di browser, hasil terkirim hanya saat klik Kirim). Kalau alat baru mengirim data otomatis, jangan beri mode local.
- FA Cek Kredit: tombol Hitung hanya mengirim kontak ke Sheet (tanpa angka keuangan); ringkasan lengkap terkirim saat klien klik Kirim WA/email.

## Deal Flow RM, Commercial Head, dan Investor (28 Okt 2026)
- fa_mitra_20261027.py: /mitra-rm-bank/ diperkuat untuk RM, junior marketing, dan Dept Head Commercial (prospek siap cair, target penyaluran, undisbursed loan); blok /layanan/ jadi RM Bank, Sekuritas, dan Investor.
- fa_deal_20261028.py (setelah fa_mitra): /mitra-investor/ (PE, family office, pembeli strategis, investor asing; bagian EN), 4 artikel (target penyaluran kredit, undisbursed loan, cara investor mencari target akuisisi, 7 red flag calon investee), kotak fa-deal di halaman terkait, footer "Mitra Investor", blok Ekosistem (CariAkuntan + UpdateSAK) di halaman mitra, sitemap, llms.txt.
- CariAkuntan: cariakuntan/gen/mitra.json (KAP & KJPP untuk syarat pencairan kredit; KAP & KJPP untuk due diligence investor), menautkan ke FA.
- UpdateSAK: 2 artikel di seo_artikel.py (checklist PSAK analis kredit; red flag PSAK due diligence). Tambahkan add() baru SEBELUM add("update-psak-2026") karena add() terakhir dipindah menjadi halaman pilar.
- PERBAIKAN Eksplor FA: kartu artikel dasar (di luar fa_content) disimpan di fa_content/eksplor_base_cards.html dan disisipkan fa_seo setiap build. Sebelumnya build kedua menghapus semua kartu Eksplor (fa_rapi memindah kartu dasar ke blok topik yang lalu dibuang fa_seo). Artikel baru di luar fa_content/script: tambahkan kartunya ke file itu.

## Artikel Lainnya dan Pola Judul Trafik Tinggi (28 Okt 2026)
- shared/related.py (dipanggil prep.py): blok "Artikel Lainnya" bergambar (sampul CSS+SVG, kategori, tanggal, judul, Baca Selengkapnya) di semua artikel FA, CariAkuntan, UpdateSAK. Relevansi dari kategori, topik, dan kata judul. Idempoten (penanda fxrel).
- Pola judul ala portal besar: "Syarat, Biaya, dan Cara ... Terbaru", tetap di bidang akuntansi, pajak, legal, kredit. fa_viral_20261028.py (FA: KUR 2026 + retitle 4 artikel), cariakuntan/gen/viral.json (PT, SPT Badan Coretax, NIB OSS), updatesak/seo_artikel.py (gaji akuntan dan auditor). Batch 2 (28 Okt 2026): fa_viral_20261028b.py (FA: take over kredit usaha), viral.json (daftar PKP Coretax), seo_artikel.py (contoh jurnal penyusutan PSAK 216).
- Artikel CariAkuntan baru: tambah ke cariakuntan/gen/*.json, lalu python3 cariakuntan/build.py && python3 fa_screen_seo_20261026.py && python3 prep.py.
- UpdateSAK Jadwal Ujian (28 Okt 2026): updatesak/build_jadwal.py (dipanggil prep.py setelah build_materi) membuat /jadwal-ujian/ (CPA IAPI, CA IAI, CPMA IAMI, Konsultan Pajak USKP/UKP BPPK), tab nav "Jadwal Ujian" di semua halaman, blok beranda (penanda jadwal:start/end), sitemap, llms.txt. Data di list EX; perbarui UPD dan isinya saat ada pengumuman baru (IAPI kalender UPAP, IAI jadwal_sertifikasi/4, IAMI, BPPK/IKPI).
- fa_beranda_20261030.py (setelah fa_rapi): beranda FA ringkas: Hero, Pilih Jalur 3 kartu (aset < Rp25 M rapikan LK via CariAkuntan; >= Rp25 M kredit komersial bank; aset bersih > Rp50 M berturut-turut investor institusi dan IPO), Cek Kredit, Rekam Jejak, Cara Mulai, Kontak. Cek Kredit menampilkan arahan CariAkuntan bila Total Aset < Rp25 M. Nav FA jadi 4 tab (Apps, Layanan, Eksplor, Kontak); E-Book, Cari Akuntan, Update SAK lewat chip Eksplor, beranda, dan footer.
