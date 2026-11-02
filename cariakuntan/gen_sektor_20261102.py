# -*- coding: utf-8 -*-
"""Artikel singkat sektor khusus (2 Nov 2026): audit dana kampanye, Koperasi Desa Merah Putih, SPPG. Output gen/sektor.json."""
import json, os
D = "2026-11-02"
FA = "https://faindonesia.co.id"
TEAM = ('<h2>Hubungi Tim Kami</h2><ul>'
 f'<li><b>Ananta W. Sasongko, CPA</b>, koordinator dan kontak lewat tombol WhatsApp di halaman ini (<a href="{FA}/ananta-w-sasongko/">profil</a>)</li>'
 f'<li><b>KJA Farhani</b>, pembukuan dan penyusunan laporan keuangan, izin KMK No. 232/KM.1/PPPK/2020 (<a href="{FA}/kja-farhani/">profil</a>)</li>'
 f'<li><b>KAP DHN &amp; Rekan</b>, audit laporan keuangan, izin KMK No. 592/KM.1/2023, terdaftar OJK (<a href="{FA}/kap-dhn/">profil</a>)</li></ul>'
 '<p>Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda. Konsultasi awal gratis.</p>')
S_DK = ["DDTCNews, KPU Atur Dana Kampanye, Peserta Pemilu Harus Siapkan 3 Laporan", "https://news.ddtc.co.id/berita/nasional/1797171/kpu-atur-soal-dana-kampanye-peserta-pemilu-harus-siapkan-3-laporan"]
S_KD = ["Kemenkeu Learning Center, Akuntansi dan Laporan Keuangan KDMP", "https://klc2.kemenkeu.go.id/kms/knowledge/akuntansi-dan-laporan-keuangan-kdmp-fondasi-akuntabilitas-program-koperasi-merah-putih-cf5cbb72/detail/"]
S_SP = ["Seantero News, 31 Oktober 2026, BGN Bekukan Operasional 6.097 SPPG", "https://www.seanteronews.com/2026/10/31/bgn-bekukan-operasional-6-097-sppg-imbas-laporan-dana-mbg/"]
S_YY = ["Pasal.id, UU Nomor 28 Tahun 2004 tentang Perubahan UU Yayasan", "https://pasal.id/peraturan/uu/uu-no-28-tahun-2004"]
A = [
 {"slug": "audit-dana-kampanye-ladk-lpsdk-lppdk", "title": "Audit Dana Kampanye: LADK, LPSDK, LPPDK dan Cara Menyiapkannya", "tag": "Audit dan Asurans", "date": D,
  "desc": "Peserta pemilu menyusun tiga laporan dana kampanye. LPPDK diaudit kantor akuntan publik sebelum hasilnya diserahkan ke KPU. Ini cara menyiapkannya agar tidak ada temuan.",
  "msg": "Selamat siang Pak Ananta, kami perlu pendampingan laporan dan audit dana kampanye.",
  "body": "<p>Setiap peserta pemilu wajib mempertanggungjawabkan dana kampanyenya. Untuk Pemilu 2024 aturannya ada di PKPU Nomor 18 Tahun 2023; pilkada memakai PKPU tersendiri dengan alur serupa.</p>"
   "<h2>Tiga Laporan Wajib</h2><table><tr><th>Laporan</th><th>Isi</th></tr><tr><td>LADK</td><td>Rekening khusus, saldo awal, sumbangan awal</td></tr><tr><td>LPSDK</td><td>Daftar pemberi sumbangan</td></tr><tr><td>LPPDK</td><td>Seluruh penerimaan dan pengeluaran, diaudit kantor akuntan publik</td></tr></table>"
   "<h2>Penyebab Temuan yang Paling Sering</h2><ul><li>Belanja dibayar dari rekening pribadi.</li><li>Identitas penyumbang tidak lengkap.</li><li>Bukti belanja tim daerah hilang.</li><li>Sumbangan barang dan jasa tidak dicatat.</li></ul>"
   f"<h2>Mulai dari Mana</h2><p>Buka rekening khusus, pakai satu format bukti untuk semua tim, dan rekap mingguan. Panduan lengkap ada di halaman <a href=\"{FA}/audit-dana-kampanye/\">Audit Dana Kampanye FA Indonesia</a>.</p>" + TEAM,
  "sources": [S_DK]},
 {"slug": "laporan-keuangan-audit-sppg-yayasan-mitra-mbg", "title": "Laporan Keuangan dan Audit SPPG: Pelajaran dari 6.097 SPPG yang Dibekukan", "tag": "Yayasan dan Nirlaba", "date": D,
  "desc": "BGN menghentikan sementara 6.097 SPPG mulai 2 November 2026 karena LPDH belum diunggah ke SIPGN. Ini laporan yang perlu disiapkan SPPG dan kapan yayasan mitra wajib diaudit.",
  "msg": "Selamat siang Pak Ananta, kami mitra/pengelola SPPG dan perlu bantuan laporan keuangan atau audit.",
  "body": "<p>Badan Gizi Nasional menghentikan sementara operasional 6.097 SPPG mulai 2 November 2026. Penyebabnya Laporan Penggunaan Dana Harian (LPDH) yang belum diunggah ke SIPGN, merujuk Surat Edaran Kepala BGN Nomor 24 Tahun 2026. Dana operasional ditahan sampai laporan diunggah dan diverifikasi.</p>"
   "<h2>Tiga Lapis Laporan</h2><table><tr><th>Lapis</th><th>Yang Disiapkan</th></tr><tr><td>Harian</td><td>LPDH dan bukti belanja, unggah ke SIPGN</td></tr><tr><td>Bulanan</td><td>Rekonsiliasi dana masuk, belanja, dan saldo</td></tr><tr><td>Tahunan</td><td>Laporan keuangan yayasan (ISAK 335) atau PT mitra</td></tr></table>"
   "<h2>Kapan Yayasan Mitra Wajib Diaudit</h2><p>Pasal 52 UU Yayasan mewajibkan audit akuntan publik bila yayasan menerima bantuan negara, luar negeri, atau pihak lain Rp500 juta atau lebih dalam setahun, atau kekayaannya di luar wakaf Rp20 miliar atau lebih. Yayasan yang mengelola dana program setahun penuh sangat mungkin melewati ambang ini.</p>"
   f"<p>Butuh bantuan menyusun LPDH yang tertunda atau laporan tahunan? Lihat <a href=\"{FA}/laporan-keuangan-audit-sppg/\">Laporan Keuangan dan Audit SPPG</a>.</p>" + TEAM,
  "sources": [S_SP, S_YY]},
]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen", "sektor.json")
json.dump(A, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
assert "—" not in open(out).read(); print("sektor.json", len(A))
