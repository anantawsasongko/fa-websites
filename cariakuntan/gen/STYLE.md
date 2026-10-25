# Aturan menulis artikel cariakuntan.com

Output: satu file JSON (array) di path yang diminta. Tiap item:
{"slug": "kebab-case-unik", "title": "Judul Title Case Indonesia", "desc": "1-2 kalimat ringkasan (maks 160 karakter), juga dipakai sebagai 'Intinya'", "tag": "kategori pendek", "msg": "Pesan WhatsApp pembuka, diawali 'Selamat siang Pak Ananta, '", "date": "YYYY-MM-DD", "body": "<p>..</p><h2>..</h2>..", "sources": [["Nama Media, 12 Mei 2026", "https://..."]]}
- "sources" wajib untuk artikel berbasis berita/data; boleh [] untuk panduan umum.
- "date": tanggal berita untuk artikel berita; "2026-10-25" untuk panduan.

Gaya:
- Bahasa Indonesia sederhana, profesional, ramah untuk pemilik usaha. Kalimat pendek. Tanpa em dash (—). Tanpa emoji.
- Judul dan H2 memakai Title Case Indonesia (kata depan/sambung seperti di, ke, dari, dan, untuk, yang, atau, dengan, bagi tetap huruf kecil).
- Panjang body 450-800 kata: 1 paragraf pembuka, 3-5 bagian <h2>, gunakan <ul>/<ol> dan boleh 1 <table> sederhana (class tidak perlu).
- Jangan menyebut nama KAP/KJA/KKP/KJPP/fintech mitra mana pun. Jangan menyebut nama orang. Identitas penulis cukup "Ananta, CPA" (tidak perlu ditulis di body).
- Jangan menjanjikan opini WTP, harga termurah, atau "pasti lolos". Jangan klaim angka yang tidak bisa diverifikasi. Untuk fakta/angka/regulasi, verifikasi lewat WebSearch/WebFetch dan cantumkan sumbernya; parafrase, jangan menyalin kalimat.
- Nomor PSAK/SAK harus mengikuti penomoran terbaru SAK Indonesia (mis. PSAK 201 penyajian, PSAK 116 sewa, PSAK 118 penyajian dan pengungkapan dalam laporan keuangan). Jika ragu, jangan sebut nomornya.
- Akhiri dengan paragraf ajakan singkat: ceritakan kondisi usaha, konsultasi awal gratis, kami bantu pilihkan kantor berizin yang sesuai (tanpa link WA, tombol sudah otomatis).
- Boleh menautkan internal: <a href="/kota/SLUG/">Nama Kota</a> hanya untuk slug kota yang ada di daftar, dan <a href="/artikel/tanya-jawab/">tanya jawab</a>.

Daftar slug kota yang ada:
ambon badung balikpapan banda-aceh bandar-lampung bandung banjarbaru banjarmasin banyuwangi batam baubau bekasi bengkulu biak bima bitung bogor bontang bukittinggi cilegon cirebon denpasar depok dumai fakfak gorontalo gresik jakarta jambi jayapura jember kediri kendari kolaka kudus kupang labuan-bajo lhokseumawe luwuk madiun magelang makassar malang mamuju manado manokwari mataram maumere medan merauke morowali nabire padang palangka-raya palembang palopo palu pangkalpinang parepare pasuruan pekalongan pekanbaru pematangsiantar pontianak purwokerto samarinda semarang serang sidoarjo singaraja singkawang sorong sumbawa-besar surabaya surakarta tangerang tanjungpinang tarakan tasikmalaya tegal ternate timika tual tuban weda yogyakarta

Konteks layanan: cariakuntan.com membantu perusahaan (aset Rp5 miliar s.d. Rp2 triliun, PMDN maupun PMA) menemukan KAP (audit, review, agreed-upon procedures), KJA (pembukuan, kompilasi), KKP (pajak), KJPP (penilaian), sekuritas, dan pendanaan, sesuai kelas rekanan bank (A Big 4/jaringan internasional, B terdaftar OJK, C izin Kemenkeu). UU PT Pasal 68: PT dengan aset atau omzet minimal Rp50 miliar wajib diaudit. PMK 28/2026: restitusi dipercepat butuh WTP 3 tahun berturut-turut.

Setelah menulis, validasi file dengan: python3 -c "import json;d=json.load(open('PATH'));print(len(d))" dan pastikan tidak ada karakter — di file.
