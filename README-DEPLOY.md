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
3. `python3 prep.py` -> hasil di `out/` dan `zips/<project>.zip` (semua < 10MB).
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
- QRIS donasi (25 Okt malam): widget `shared/donasi.js` + `shared/qris-fa-indonesia.jpg`, dipasang oleh prep.py (`add_donasi`) di /buku/ (materi gratis FA Edu, brosur FA Consult tidak), /cek-psak-118/ (tab Hasil + Download Excel), /audit-ready/ (Download Excel/Word CALK, dilewati kalau sudah aktivasi lisensi), dan screening cariakuntan (4 bahasa). Nominal Rp10.001, bisa dilewati, sekali per sesi per layanan; setelah hasil muncul ada pill "Donasi via QRIS" untuk buka QRIS lagi.

## SEO Push Lokal (25 Okt 2026 malam)
- cariakuntan: semua kota x 4 layanan inti punya halaman sendiri; 94 kota (+8 kota baru di kawasan.py EXTRA_CITIES); 89 kawasan bisnis (cariakuntan/kawasan.py, generator seo_kawasan.py) dengan hub + 4 halaman layanan (/kota/<kota>/<kawasan>/<kap|kjpp|konsultan-pajak|jasa-laporan-keuangan>/); BOOST konteks pasar untuk Malang, Surabaya, Jember, Pasuruan, Batam; kotak silang ke FA di setiap halaman kota/kawasan.
- FA: fa_seo_20261025.py (jalankan setelah fa_home_simple): 30 artikel dari fa_content/articles/*.json (spec di fa_content/SPEC-ARTIKEL.md), kartu per topik di Eksplor, /konsultan-rumah-sakit/ dan /konsultan-unit-cost-rumah-sakit/ (+ per kota), /wilayah/ (kota + kawasan), footer, sitemap, llms.txt.
- Urutan build: python3 fa_home_simple_20261025.py && python3 fa_seo_20261025.py && python3 fa_lead_20261026.py && python3 fa_psak_20261026.py && python3 fa_kredit_20261026.py && python3 fa_seller_20261026.py && python3 fa_tone_20261026.py && python3 cariakuntan/build.py && python3 prep.py

## Halaman dari Lead Nyata (26 Okt 2026)
- fa_lead_20261026.py: /jasa-implementasi-psak-118/ dan /konsultan-kredit-distributor-importir/ (dua lead WA hari itu: implementasi PSAK 118 dan plafon kredit distributor/importir), kotak CTA di artikel terkait, blok di /layanan/, sitemap, llms.txt. Idempoten.
- fa_seo_20261025.py diperbaiki: blok llms "Artikel Eksplor Terbaru" tidak lagi dobel saat dijalankan ulang.
- Push tanpa akses git: GitHub > Add file > Upload files per folder; commit perantara diberi [CF-Pages-Skip], commit terakhir tanpa tanda itu supaya Cloudflare build sekali.

## Cluster Implementasi PSAK (26 Okt 2026 sore)
- fa_psak_20261026.py: hub /jasa-implementasi-psak/ + 8 halaman (PSAK 109, 115, 116, 117, 212, 219, konsolidasi PSAK 110, transisi SAK EP ke PSAK). Penomoran SAK Online IAI. Kotak CTA di 7 halaman terkait, tombol di /layanan/, sitemap, llms.txt. Idempoten, jalankan setelah fa_lead_20261026.py.

## FA Venus Cek Kapasitas Kredit (26 Okt 2026 malam)
- fa_kredit_20261026.py: /cek-kapasitas-kredit/ (kredit baru, top up, take over): DSCR, plafon per batas (DSCR, Utang/EBITDA, DER, agunan LTV 70%, siklus modal kerja untuk KMK), matriks kemampuan bayar per bunga x tenor, bunga maksimal atau tenor minimal untuk plafon incaran, langkah lanjut. Lead ke Google Sheet CariAkuntan (goal diawali 'FA Cek Kapasitas Kredit'). QRIS Rp10.001 lewat prep.py add_donasi (key venus-kredit). Juga tertanam di beranda FA tepat di bawah hero (section #cek-kredit, penanda fa-kk-home). Kartu di /apps/, CTA di halaman kredit, tombol /layanan/, sitemap, llms.txt.

## Aturan Nada (26 Okt 2026)
- JANGAN PERNAH menulis "ditangani langsung oleh Ananta W. Sasongko, CPA" atau variasinya (EN/ZH juga) di FA, CariAkuntan, KJA, maupun slides. Pakai bahasa tim: "didampingi tim FA Indonesia", "tim CA dan CPA". fa_tone_20261026.py membersihkan semua sumber; jalankan sebelum prep.py.
