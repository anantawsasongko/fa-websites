# Spec artikel SEO FA Indonesia (faindonesia.co.id, tab Eksplor)

Tulis setiap artikel sebagai SATU file JSON: `/home/claude/fa-websites/fa_content/articles/<slug>.json` (UTF-8, ensure_ascii false). Jangan menyentuh file lain di repo.

## Skema JSON
```
{
 "slug": "cara-menghitung-unit-cost-rumah-sakit",        // huruf kecil, tanda hubung, tanpa tahun kecuali perlu
 "title": "Cara Menghitung Unit Cost Rumah Sakit: Metode Distribusi Ganda dan Contohnya",  // 50-70 karakter ideal, kata kunci utama di depan, Title Case Indonesia (kata sambung huruf kecil)
 "description": "...",                                    // meta description 130-155 karakter, memuat kata kunci utama
 "keyword": "unit cost rumah sakit",                      // kata kunci utama
 "category": "Rumah Sakit",                               // salah satu: Rumah Sakit, Audit & KAP, Penilaian & KJPP, Kredit Bank, Investor & IPO, Pajak, Laporan Keuangan, CFO & Tata Kelola
 "minutes": 6,                                            // perkiraan menit baca
 "cta": {"href": "/konsultan-unit-cost-rumah-sakit/", "label": "Konsultan Unit Cost Rumah Sakit"},
 "wa": "Halo FA Indonesia, saya ingin konsultasi unit cost rumah sakit.",   // teks WA pembuka
 "body_html": "<p>...</p><h2>...</h2>...",                // 900-1400 kata, HTML sederhana saja
 "faq": [["Pertanyaan?", "Jawaban 1-3 kalimat."], ...],  // 3-5 butir, pertanyaan yang benar-benar dicari orang
 "sources": [["Judul sumber", "https://..."], ...]        // 2-5 sumber resmi/kredibel yang Anda cek (peraturan, IAI SAK Online, OJK, Kemenkes, DJP, BEI). Kosongkan [] bila murni praktik.
}
```

## body_html
- Tag yang boleh: p, h2, h3, ul, ol, li, b, i, a, table/thead/tbody/tr/th/td, blockquote. Jangan pakai h1 (judul sudah di template), jangan inline style, jangan script.
- Tabel dibungkus `<div class="tblwrap"><table class="tbl">...</table></div>`. Untuk alur bertahap boleh pakai daftar bernomor `<ol>`.
- Paragraf pendek (2-4 kalimat). Banyak subjudul h2 yang memuat variasi kata kunci (contoh: "unit cost rawat inap", "biaya satuan per tindakan").
- Wajib minimal 1 tabel atau daftar yang benar-benar berguna (contoh perhitungan, checklist dokumen, perbandingan).
- Akhiri dengan paragraf "Bagaimana FA Indonesia Membantu" (h2) yang singkat, rendah hati, menyebut bahwa klien ditangani langsung oleh Ananta W. Sasongko, CPA, dan link ke halaman layanan FA yang relevan. JANGAN tulis bagian FAQ di body (FAQ dirender otomatis dari field faq).
- Link internal (pakai path relatif untuk FA, absolut untuk CariAkuntan). Sisipkan 2-4 link yang relevan di dalam teks:
  FA: /konsultan-rumah-sakit/, /konsultan-unit-cost-rumah-sakit/, /konsultan-kredit-bank/, /konsultan-persiapan-ipo/, /pendampingan-gcg/, /jasa-penyusunan-laporan-keuangan/, /laporan-keuangan-umkm/, /cfo-paruh-waktu/, /cfo-direktur-keuangan-ipo/, /laporan-tahunan-pt/, /komite-audit-komisaris-independen/, /layanan/, /buku/ (e-book & materi gratis), /audit-ready/ (FA Jupiter, app penyusunan LK), /cek-psak-118/ (FA Venus, kalkulator PSAK 118), artikel lain di /artikel/<slug>/ dari daftar topik di bawah.
  CariAkuntan (layanan cari KAP/KJPP/konsultan pajak per kota): https://cariakuntan.com/layanan/kap/ , https://cariakuntan.com/layanan/kjpp/ , https://cariakuntan.com/layanan/konsultan-pajak/ , https://cariakuntan.com/layanan/jasa-laporan-keuangan/ , https://cariakuntan.com/kota/
- Untuk topik lokal, boleh sebut bahwa layanan menjangkau seluruh Indonesia (Jawa, Sumatera, Kalimantan, Sulawesi, Bali-Nusa Tenggara, Papua) secara daring dan kunjungan.

## Gaya bahasa (WAJIB)
- Bahasa Indonesia profesional tapi luwes, seperti praktisi yang menjelaskan ke pemilik usaha atau direktur. Tidak terdengar seperti tulisan AI: hindari frasa klise ("di era digital", "dalam dunia bisnis yang dinamis", "sangat penting untuk", "kesimpulannya"), hindari pembuka retoris yang bertele-tele.
- DILARANG memakai em dash (—) dan en dash (–) sebagai tanda baca. Pakai koma, titik dua, atau kalimat baru. Rentang angka tulis "2 sampai 4 minggu" atau "Rp1-5 miliar" dengan tanda hubung biasa.
- Istilah Inggris sehari-hari boleh dan dianjurkan: upload, file, review, update, link, data room, cash flow.
- Rendah hati, tidak bombastis, tidak menjanjikan hasil ("pasti cair" dilarang). Tidak menyebut nama klien, nama bank, atau merek pihak ketiga sebagai klien/mitra. Boleh menyebut regulator dan lembaga resmi (OJK, BEI, DJP, IAI, IAPI, Kemenkes, BPJS Kesehatan, MAPPI).
- Pengalaman yang BOLEH disebut (faktual): mendampingi akuisisi tiga rumah sakit di Jawa Tengah; pendampingan kredit perbankan kumulatif mendekati Rp1 triliun; pendanaan investor hingga US$3 juta untuk grup rumah sakit; mandat divestasi rumah sakit dan BPR; menyusun annual report perdana rumah sakit BUMN; pengalaman audit di firma Big Four. Jangan mengarang pengalaman lain.
- Angka contoh dalam ilustrasi boleh asumsi, tapi tandai jelas sebagai "contoh" / "ilustrasi".

## Akurasi (WAJIB)
- Penomoran SAK memakai penomoran baru SAK Indonesia (berlaku sejak 1 Januari 2024): contoh PSAK 201 Penyajian Laporan Keuangan, PSAK 207 Laporan Arus Kas, PSAK 109 Instrumen Keuangan, PSAK 115 Pendapatan dari Kontrak dengan Pelanggan, PSAK 116 Sewa, PSAK 216 Aset Tetap, PSAK 219 Imbalan Kerja, PSAK 224 Pihak Berelasi, PSAK 236 Penurunan Nilai Aset, PSAK 237 Provisi, PSAK 118 Penyajian dan Pengungkapan dalam Laporan Keuangan (berlaku 1 Januari 2027, menggantikan PSAK 201). SAK EP berlaku sejak 1 Januari 2025 menggantikan SAK ETAP. JANGAN pakai nomor lama (PSAK 1, 16, 23, 71, 72, 73) kecuali dalam kurung sebagai "dulu PSAK 72".
- Gunakan WebSearch/WebFetch untuk memverifikasi setiap klaim regulasi, angka ambang, tarif, dan tenggat sebelum menulisnya. Kalau tidak bisa diverifikasi, tulis secara umum tanpa angka spesifik. Cantumkan yang Anda cek di "sources".
- Tanggal hari ini 25 Oktober 2026.

## Selesai
Setelah semua file ditulis, jalankan `python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('/home/claude/fa-websites/fa_content/articles/*.json')];print('ok')"` untuk validasi, lalu cek tidak ada karakter — atau – di file Anda (`grep -l '[—–]' ...`). Laporkan daftar slug + judul yang Anda tulis (singkat).
