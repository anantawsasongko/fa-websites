# -*- coding: utf-8 -*-
"""Pencarian di luar lokasi (3 Nov 2026): pemicu dokumen, pencarian karena masalah, cek vendor, dan notaris.
Output gen/peluang.json (dibaca otomatis build.py). Artikel singkat, tanpa nomor telepon tertulis (kontak lewat tombol WA)."""
import json, os
D = "2026-11-03"
FA = "https://faindonesia.co.id"
TEAM = ('<h2>Siapa yang Membantu</h2><ul>'
 f'<li><b>Ananta W. Sasongko, CPA</b>, koordinator (<a href="{FA}/ananta-w-sasongko/">profil</a>)</li>'
 f'<li><b>KJA Farhani</b>, pembukuan dan penyusunan laporan keuangan (<a href="{FA}/kja-farhani/">profil</a>)</li>'
 f'<li><b>KAP DHN &amp; Rekan</b>, audit, terdaftar OJK (<a href="{FA}/kap-dhn/">profil</a>)</li></ul>'
 '<p>Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda. Chat lewat tombol WhatsApp di halaman ini, konsultasi awal gratis.</p>')
S_SP1 = ["DDTCNews, WP Diberi Waktu 14 Hari untuk Tanggapi SP2DK", "https://news.ddtc.co.id/berita/nasional/1810725/wp-diberi-waktu-14-hari-untuk-tanggapi-sp2dk-bisa-lewat-coretax"]
S_SP2 = ["DDTCNews, PMK Baru: Jangka Waktu Tanggapi SP2DK Bisa Diperpanjang 7 Hari", "https://news.ddtc.co.id/berita/nasional/1816392/pmk-baru-jangka-waktu-tanggapi-sp2dk-bisa-diperpanjang-7-hari"]
S_AHU = ["IZIN.co.id, 28 Oktober 2026, Jadwal Sanksi Laporan Tahunan PT", "https://izin.co.id/blog/ditjen-ahu-umumkan-jadwal-sanksi-laporan-tahunan-pt-blokir-sabh-mulai-januari-2027/"]
S_YY = ["Pasal.id, UU Nomor 28 Tahun 2004 tentang Perubahan UU Yayasan", "https://pasal.id/peraturan/uu/uu-no-28-tahun-2004"]
A = []
def add(slug, title, tag, desc, msg, body, src=()):
    A.append({"slug": slug, "title": title, "tag": tag, "date": D, "desc": desc, "msg": "Selamat siang Pak Ananta, " + msg, "body": body + TEAM, "sources": list(src)})

# ---------- pemicu dokumen ----------
add("syarat-tender-laporan-keuangan-audited", "Syarat Tender Minta Laporan Keuangan Audited: Yang Perlu Disiapkan", "Tender dan Pengadaan",
 "Dokumen kualifikasi tender pemerintah, BUMN, atau swasta sering meminta laporan keuangan yang diaudit. Ini cara membaca syaratnya dan menyiapkan audit sebelum tenggat.",
 "perusahaan kami ikut tender dan diminta laporan keuangan audited.",
 "<p>Banyak penyedia baru sadar butuh laporan audited saat membaca Lembar Data Kualifikasi (LDK) atau dokumen pemilihan. Tenggat tender biasanya pendek, sementara audit butuh beberapa minggu.</p>"
 "<h2>Baca Dulu Syarat Persisnya</h2><ul><li>Laporan tahun buku berapa yang diminta.</li><li>Apakah tertulis diaudit akuntan publik, atau cukup laporan keuangan.</li><li>Apakah ada syarat opini atau KAP tertentu.</li><li>Rasio yang dinilai: modal kerja, kemampuan keuangan, atau sisa kemampuan paket.</li></ul>"
 "<h2>Bila Waktunya Mepet</h2><ol><li>Pastikan laporan keuangan dan neraca saldo sudah final.</li><li>Pilih KAP yang bisa menjadwalkan kerja lapangan segera.</li><li>Siapkan kontrak, faktur, dan rekening koran dalam satu folder.</li></ol>"
 "<p>Laporan audited juga terpakai untuk tender berikutnya dan kredit modal kerja, jadi audit tahunan rutin lebih hemat daripada audit mendadak tiap ada tender.</p>")

add("audit-dana-hibah-bantuan-pemerintah-yayasan-ormas", "Audit Dana Hibah dan Bantuan Pemerintah untuk Yayasan dan Ormas", "Yayasan dan Nirlaba",
 "Yayasan dan ormas penerima hibah pemda, bantuan kementerian, atau dana donor wajib mempertanggungjawabkan penggunaannya. Kapan perlu audit akuntan publik dan apa alternatifnya.",
 "lembaga kami menerima dana hibah dan perlu laporan pertanggungjawaban atau audit.",
 "<p>Penerima hibah menyusun laporan penggunaan dana sesuai perjanjian hibah. Untuk yayasan, ada kewajiban tambahan dari UU Yayasan.</p>"
 "<h2>Kapan Wajib Audit Akuntan Publik</h2><p>Pasal 52 UU Yayasan mewajibkan audit bila yayasan memperoleh bantuan negara, luar negeri, atau pihak lain Rp500 juta atau lebih dalam satu tahun buku, atau kekayaan di luar wakaf Rp20 miliar atau lebih. Perjanjian hibah atau donor juga bisa mensyaratkan audit walaupun nilainya di bawah ambang.</p>"
 "<h2>Pilihan Jasa</h2><table><tr><th>Kebutuhan</th><th>Jasa</th></tr><tr><td>Laporan keuangan lembaga</td><td>Penyusunan laporan sesuai ISAK 335</td></tr><tr><td>Bukti penggunaan dana per program</td><td>Prosedur yang disepakati (AUP) oleh KAP</td></tr><tr><td>Opini atas laporan keuangan</td><td>Audit oleh KAP</td></tr></table>"
 "<h2>Yang Disiapkan</h2><ul><li>Perjanjian hibah dan RAB yang disetujui.</li><li>Rekening khusus program dan mutasinya.</li><li>Bukti belanja per kegiatan.</li></ul>", [S_YY])

add("laporan-keuangan-audit-bumdes", "Laporan Keuangan dan Audit BUMDes: Panduan untuk Pengurus dan Pemerintah Desa", "Koperasi",
 "BUM Desa mempertanggungjawabkan modal desa lewat laporan keuangan ke musyawarah desa. Kapan perlu audit akuntan publik, dan cara merapikan pembukuan unit usaha.",
 "kami pengurus BUMDes dan perlu bantuan laporan keuangan atau audit.",
 "<p>BUM Desa mengelola penyertaan modal dari dana desa. Laporan keuangannya dibahas di musyawarah desa dan sering diminta pendamping, pemerintah daerah, atau pemeriksa.</p>"
 "<h2>Laporan yang Disusun</h2><ul><li>Laporan posisi keuangan, termasuk penyertaan modal desa.</li><li>Laporan laba rugi per unit usaha.</li><li>Laporan arus kas dan catatan.</li><li>Pembagian hasil usaha ke pendapatan asli desa.</li></ul>"
 "<h2>Kapan Perlu Audit</h2><p>Audit akuntan publik biasanya dilakukan bila diputuskan musyawarah desa, diminta mitra pembiayaan atau investor, atau ada pemeriksaan atas penggunaan modal. Untuk kebutuhan yang lebih ringan, prosedur yang disepakati (AUP) atas penggunaan modal bisa dipakai.</p>"
 "<h2>Langkah Merapikan</h2><ol><li>Pisahkan rekening per unit usaha.</li><li>Catat penyertaan modal sesuai berita acara.</li><li>Tutup buku bulanan, walau sederhana.</li></ol>"
 f"<p>Untuk koperasi desa, lihat juga <a href=\"{FA}/audit-koperasi-desa-merah-putih/\">Laporan Keuangan dan Audit KDMP</a>.</p>")

# ---------- pencarian karena masalah ----------
add("laporan-audit-ditolak-bank-penyebab-solusi", "Laporan Audit Ditolak Bank: 6 Penyebab dan Cara Memperbaikinya", "Kredit Bank",
 "Laporan audited sudah ada tetapi bank menolak atau minta ulang. Penyebab paling umum dan langkah cepat agar pengajuan kredit tidak tertunda lama.",
 "laporan audit perusahaan kami ditolak bank, mohon dibantu.",
 "<p>Ditolaknya laporan audit hampir selalu karena salah satu dari enam hal berikut, bukan karena auditnya buruk.</p>"
 "<h2>Penyebab Paling Umum</h2><ol><li>KAP tidak masuk daftar rekanan bank atau kelas yang diminta.</li><li>Tahun buku terlalu lama, bank minta tahun terakhir.</li><li>Opini dengan pengecualian atau tidak menyatakan pendapat.</li><li>Angka laporan berbeda jauh dengan SPT dan mutasi rekening.</li><li>Catatan atas laporan keuangan tidak lengkap.</li><li>Laporan tidak ditandatangani atau tidak lengkap halamannya.</li></ol>"
 "<h2>Langkah Perbaikan</h2><ul><li>Minta alasan tertulis dari analis kredit.</li><li>Bila soal daftar rekanan, pilih KAP yang ada di daftar bank tersebut untuk tahun berikutnya.</li><li>Bila soal selisih SPT, siapkan rekonsiliasi laba komersial dan fiskal.</li><li>Bila soal opini, perbaiki penyebab pengecualian sebelum audit berikutnya.</li></ul>"
 f"<p>Cek dulu kapasitas kredit perusahaan dengan <a href=\"{FA}/cek-kapasitas-kredit/\">Cek Kredit dan Pendanaan</a>.</p>")

add("opini-tidak-menyatakan-pendapat-langkah-perbaikan", "Opini Tidak Menyatakan Pendapat (Disclaimer): Langkah Perbaikan untuk Tahun Berikutnya", "Audit dan Asurans",
 "Opini tidak menyatakan pendapat membuat laporan audit sulit dipakai untuk bank dan investor. Penyebabnya, dampaknya, dan cara memperbaikinya agar audit berikutnya bersih.",
 "laporan audit perusahaan kami mendapat opini tidak menyatakan pendapat.",
 "<p>Opini tidak menyatakan pendapat muncul bila auditor tidak bisa memperoleh bukti yang cukup atas pos yang material. Artinya bukan laporan pasti salah, tetapi auditor tidak bisa menilainya.</p>"
 "<h2>Penyebab yang Sering Terjadi</h2><ul><li>Persediaan tidak dihitung pada akhir tahun.</li><li>Saldo awal belum pernah diaudit dan buktinya hilang.</li><li>Piutang atau utang besar tanpa konfirmasi atau dokumen.</li><li>Aset tetap tanpa daftar dan bukti kepemilikan.</li></ul>"
 "<h2>Rencana Perbaikan</h2><ol><li>Baca paragraf basis opini, catat setiap pos yang disebut.</li><li>Susun ulang bukti untuk pos tersebut.</li><li>Jadwalkan stock opname akhir tahun yang diobservasi auditor.</li><li>Pertimbangkan audit ulang tahun berjalan dengan persiapan yang lebih matang.</li></ol>"
 "<p>Dampaknya ke kredit dijelaskan di <a href=\"/artikel/opini-audit-wtp-wdp-tidak-wajar-disclaimer-dampak-kredit/\">Opini Audit dan Dampaknya ke Kredit</a>.</p>")

add("akses-sabh-diblokir-cara-membuka-laporan-tahunan-pt", "Akses SABH Diblokir karena Laporan Tahunan PT: Cara Membukanya", "Kepatuhan PT",
 "Ditjen AHU menjadwalkan teguran Desember 2026 dan blokir akses SABH mulai 2 Januari 2027 bagi PT yang belum melapor tahun buku 2025. Ini urutan langkah agar akses kembali normal.",
 "PT kami terancam atau sudah diblokir SABH karena laporan tahunan.",
 "<p>Blokir SABH membuat perubahan direksi, komisaris, pemegang saham, dan data perseroan tertahan. Kuncinya: laporan tahunan yang tertunda harus disampaikan lewat notaris.</p>"
 "<h2>Jadwal yang Diumumkan</h2><table><tr><th>Tanggal</th><th>Tahap</th></tr><tr><td>1 sampai 31 Desember 2026</td><td>Teguran tertulis untuk PT yang belum melapor tahun buku 2025</td></tr><tr><td>Mulai 2 Januari 2027</td><td>Blokir akses SABH bila 30 hari setelah teguran belum dipenuhi</td></tr></table>"
 "<h2>Urutan Langkah</h2><ol><li>Selesaikan laporan keuangan tahun buku 2025, audited bila PT wajib audit.</li><li>Susun laporan tahunan sesuai isi minimal.</li><li>RUPS atau keputusan sirkuler, lalu akta notaris.</li><li>Notaris menyampaikan ke SABH dan memantau status blokir.</li></ol>"
 "<p>Bagian yang paling lama biasanya laporan keuangan dan audit. Lihat <a href=\"/artikel/audit-laporan-tahunan-pt-sabh-jadwal-sanksi/\">Audit untuk Laporan Tahunan PT di SABH</a>.</p>", [S_AHU])

add("sp2dk-laporan-keuangan-rapi-cara-menanggapi", "Terima SP2DK dari Kantor Pajak: Kenapa Laporan Keuangan Rapi Jadi Kunci", "Pajak",
 "SP2DK harus ditanggapi dalam 14 hari dan kini bisa diperpanjang 7 hari. Penjelasan yang kuat butuh laporan keuangan dan rekonsiliasi yang rapi. Ini cara menyiapkannya.",
 "perusahaan kami menerima SP2DK dan perlu bantuan menyiapkan penjelasan dan laporan keuangan.",
 "<p>SP2DK adalah permintaan penjelasan atas data yang dimiliki kantor pajak, misalnya selisih omzet SPT dengan data pihak ketiga. Pemberitaan menyebut wajib pajak diberi waktu 14 hari untuk menanggapi, dan aturan baru memungkinkan perpanjangan 7 hari.</p>"
 "<h2>Yang Biasanya Dibandingkan</h2><ul><li>Peredaran usaha di SPT dengan faktur, mutasi rekening, dan data pihak ketiga.</li><li>Biaya yang dibebankan dengan bukti potong dan faktur pajak.</li><li>Aset yang dimiliki dengan yang dilaporkan.</li></ul>"
 "<h2>Cara Menyiapkan Tanggapan</h2><ol><li>Susun rekonsiliasi antara laporan keuangan, SPT, dan mutasi rekening.</li><li>Jelaskan setiap selisih dengan bukti.</li><li>Bila pembukuan belum rapi, rapikan dulu sebelum menanggapi.</li><li>Untuk kasus rumit, libatkan konsultan pajak berizin.</li></ol>"
 "<p>Laporan keuangan yang rapi tidak menghapus kewajiban pajak, tetapi membuat penjelasan Anda bisa diuji dan dipercaya.</p>", [S_SP1, S_SP2])

# ---------- cek vendor ----------
add("kap-big-4-vs-kap-lokal-mana-yang-dibutuhkan", "KAP Big 4 vs KAP Lokal: Mana yang Sebenarnya Dibutuhkan Perusahaan Anda", "Audit dan Asurans",
 "Tidak semua perusahaan perlu Big 4. Pilihan KAP ditentukan pembaca laporan: bank, investor asing, regulator, atau rencana IPO. Ini cara memutuskannya.",
 "kami bingung memilih antara KAP Big 4, jaringan internasional, atau KAP lokal.",
 "<p>Pertanyaan yang tepat bukan KAP mana yang paling besar, tetapi siapa yang akan membaca laporan dan apa syaratnya.</p>"
 "<h2>Perbandingan Singkat</h2><table><tr><th>Pilihan</th><th>Cocok Untuk</th></tr><tr><td>Big 4</td><td>Grup besar, anak usaha multinasional, IPO besar, investor global</td></tr><tr><td>KAP jaringan internasional</td><td>PMA menengah, calon IPO, bank yang minta KAP terdaftar OJK</td></tr><tr><td>KAP lokal terdaftar OJK</td><td>Kredit bank, BPR, IKNB, perusahaan menengah</td></tr><tr><td>KAP lokal berizin Kemenkeu</td><td>Wajib audit UU PT, SABH, tender, yayasan</td></tr></table>"
 "<h2>Yang Menentukan</h2><ul><li>Daftar rekanan bank tujuan.</li><li>Syarat investor atau kantor pusat.</li><li>Kewajiban regulator sektor.</li><li>Anggaran dan jadwal.</li></ul>"
 "<p>Lihat juga <a href=\"/artikel/kelas-kap-rekanan-bank-a-b-c-arti-dan-cara-memilih/\">kelas KAP rekanan bank</a>.</p>")

add("kelas-kap-rekanan-bank-a-b-c-arti-dan-cara-memilih", "Kelas KAP Rekanan Bank A, B, dan C: Arti dan Cara Memilih", "Kredit Bank",
 "Bank mengelompokkan KAP rekanan dalam beberapa kelas. Mengetahui kelas yang diminta sebelum audit mencegah laporan ditolak dan biaya ganda.",
 "bank kami meminta KAP dengan kelas tertentu.",
 "<p>Setiap bank punya daftar KAP rekanan dan sering mengelompokkannya berdasarkan ukuran dan pendaftaran. Istilah dan batasnya berbeda antarbank, tetapi pola umumnya serupa.</p>"
 "<h2>Pola Umum Pengelompokan</h2><table><tr><th>Kelas</th><th>Umumnya</th><th>Biasanya untuk</th></tr><tr><td>A</td><td>Big 4 dan jaringan internasional besar</td><td>Plafon besar, korporasi, sindikasi</td></tr><tr><td>B</td><td>KAP terdaftar OJK</td><td>Plafon menengah, komersial</td></tr><tr><td>C</td><td>KAP berizin Kemenkeu</td><td>Plafon kecil sampai menengah</td></tr></table>"
 "<h2>Cara Memastikan</h2><ol><li>Tanyakan ke RM bank kelas KAP untuk plafon yang diajukan.</li><li>Minta daftar KAP rekanan yang berlaku.</li><li>Pilih KAP sebelum audit dimulai, bukan sesudahnya.</li></ol>"
 "<p>Bacaan terkait: <a href=\"/artikel/audit-kap-untuk-pengajuan-kredit-bank/\">Audit KAP untuk Pengajuan Kredit Bank</a>.</p>")

# ---------- notaris ----------
add("notaris-butuh-akuntan-laporan-tahunan-pt-sabh", "Untuk Notaris: Rekan Akuntan untuk Laporan Tahunan PT Klien di SABH", "Kepatuhan PT",
 "Sejak Permenkum 49/2025, notaris menerima banyak PT yang laporan keuangannya belum siap. Cara kerja sama dengan akuntan agar akta laporan tahunan selesai tepat waktu.",
 "saya notaris dan ingin bekerja sama untuk laporan keuangan dan audit klien PT.",
 "<p>Persetujuan laporan tahunan PT kini dituangkan dalam akta notaris lalu disampaikan lewat SABH. Hambatan terbesar di kantor notaris biasanya bukan aktanya, tetapi laporan keuangan klien yang belum ada atau belum diaudit.</p>"
 "<h2>Yang Bisa Dirujuk ke Kami</h2><ul><li>PT tanpa laporan keuangan: penyusunan oleh KJA.</li><li>PT wajib audit: audit oleh KAP terdaftar OJK.</li><li>PT dengan laporan yang belum lengkap: perbaikan CALK dan laporan tahunan.</li></ul>"
 "<h2>Alur Kerja Sama</h2><ol><li>Notaris mengirim kontak klien.</li><li>Kami menghubungi klien dan menyepakati ruang lingkup dan biaya langsung dengan klien.</li><li>Laporan selesai, dikirim ke klien dan notaris untuk RUPS dan akta.</li></ol>"
 f"<p>Detail program ada di <a href=\"{FA}/mitra-notaris/\">Mitra Notaris FA Indonesia</a>.</p>")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen", "peluang.json")
json.dump(A, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
t = open(out).read(); assert "—" not in t and "0822" not in t
print("peluang.json", len(A))
