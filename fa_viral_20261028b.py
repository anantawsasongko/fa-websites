# -*- coding: utf-8 -*-
"""Artikel bertrafik tinggi FA (28 Okt 2026, batch 2):
- /artikel/syarat-biaya-cara-take-over-kredit-usaha/ : take over kredit usaha ke bank lain
- kartu di Eksplor topik Kredit Bank, sitemap, llms.txt
Helper dari fa_mitra_20261027.py. Idempoten (penanda fa-viral-b). Jalankan setelah fa_viral_20261028.py.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_mitra_20261027.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. MITRA RM BANK")]
_src = _src.replace('TODAY = "2026-10-27"', 'TODAY = "2026-10-28"').replace("27 Oktober 2026", "28 Oktober 2026")
exec(compile(_src, "fa_mitra_helpers", "exec"))

S1 = "syarat-biaya-cara-take-over-kredit-usaha"
body = (
 "<p><b>Jawaban singkat:</b> take over kredit usaha adalah memindahkan pinjaman dari bank lama ke bank baru. Bank baru melunasi sisa pokok di bank lama, agunan dipindahkan, lalu perusahaan mencicil ke bank baru dengan bunga, tenor, atau plafon yang lebih cocok. "
 "Biayanya terdiri dari penalti pelunasan dipercepat di bank lama, provisi dan administrasi di bank baru, penilaian agunan, serta notaris. Take over layak dilakukan kalau penghematan bunga dan tambahan plafon lebih besar dari total biaya itu.</p>"
 "<h2>Kapan Take Over Kredit Masuk Akal</h2>"
 "<ul><li>Selisih bunga cukup lebar dan sisa tenor masih panjang, sehingga penghematan menutup biaya pindah.</li>"
 "<li>Usaha butuh tambahan plafon (top up) yang tidak diberikan bank lama.</li>"
 "<li>Struktur fasilitas tidak cocok, misalnya modal kerja dibiayai kredit investasi atau sebaliknya.</li>"
 "<li>Beberapa fasilitas di bank berbeda ingin disatukan supaya pelaporan dan covenant lebih sederhana.</li></ul>"
 "<p>Sebaliknya, take over sulit kalau kolektibilitas di SLIK sedang bermasalah, laporan keuangan menurun, atau agunan belum bersertifikat. Bank baru menilai debitur dari nol, sama seperti pengajuan kredit baru.</p>"
 "<h2>Rincian Biaya Take Over</h2>"
 + tbl(["Komponen", "Dibayar ke", "Kisaran yang Umum Dilaporkan"], [
   ("Penalti pelunasan dipercepat", "Bank lama", "Sekitar 2% sampai 3% dari sisa pokok, tergantung perjanjian kredit"),
   ("Provisi", "Bank baru", "Sekitar 1% dari plafon yang disetujui"),
   ("Administrasi", "Bank baru", "Ratusan ribu sampai jutaan rupiah, tergantung bank"),
   ("Penilaian agunan", "Penilai internal atau KJPP rekanan", "Naik seiring nilai dan jumlah agunan"),
   ("Notaris dan PPAT", "Notaris rekanan bank baru", "Akta kredit, roya hak tanggungan lama, pembebanan hak tanggungan baru"),
   ("Asuransi", "Asuransi rekanan bank", "Asuransi agunan dan, bila diminta, asuransi jiwa pengurus"),
 ])
 + "<p>Kisaran penalti, provisi, dan administrasi di atas adalah angka yang biasa dipakai bank untuk kredit beragunan properti. Untuk kredit modal kerja dan kredit investasi korporasi, angkanya tertulis di perjanjian kredit masing-masing dan sering bisa dinegosiasikan, terutama provisi dan biaya administrasi. "
 "Baca dulu pasal pelunasan dipercepat di perjanjian kredit lama sebelum menghitung.</p>"
 "<h2>Syarat dan Dokumen yang Diminta Bank Baru</h2>"
 "<ul><li>Legalitas perusahaan: akta pendirian dan perubahan terakhir, SK Kementerian Hukum, NIB, dan izin usaha.</li>"
 "<li>Laporan keuangan dua sampai tiga tahun terakhir. Untuk plafon menengah ke atas, umumnya laporan yang diaudit KAP.</li>"
 "<li>SPT Tahunan Badan dan rekening koran operasional enam sampai dua belas bulan.</li>"
 "<li>Surat keterangan sisa pinjaman (outstanding) dan riwayat pembayaran dari bank lama.</li>"
 "<li>Dokumen agunan: sertifikat, IMB atau PBG, dan PBB.</li>"
 "<li>Proyeksi arus kas yang menunjukkan kemampuan bayar setelah fasilitas baru.</li></ul>"
 "<p>Daftar lengkapnya ada di <a href=\"/artikel/dokumen-pengajuan-kredit-korporasi/\">checklist dokumen pengajuan kredit korporasi</a>.</p>"
 "<h2>Cara Take Over Kredit Usaha</h2>"
 + flow([
   ("Hitung Untung Rugi", "Bandingkan total biaya pindah dengan penghematan bunga selama sisa tenor dan nilai tambahan plafon."),
   ("Minta Data ke Bank Lama", "Surat keterangan sisa pinjaman, jadwal angsuran, dan ketentuan pelunasan dipercepat."),
   ("Ajukan ke Bank Baru", "Serahkan berkas lengkap. Bank baru menganalisis laporan keuangan, SLIK, dan rasio kemampuan bayar."),
   ("Penilaian Agunan", "Agunan dinilai ulang oleh penilai internal bank atau KJPP rekanan."),
   ("Persetujuan dan Akad", "Surat persetujuan kredit terbit, akad ditandatangani di notaris rekanan bank baru."),
   ("Pelunasan dan Pengalihan Agunan", "Bank baru melunasi sisa pokok ke bank lama, sertifikat diserahkan, hak tanggungan lama diroya dan dibebankan ulang untuk bank baru."),
 ])
 + "<h2>Contoh Hitungan Sederhana</h2>"
 "<p>Sisa pokok Rp10 miliar, sisa tenor 4 tahun. Penalti 2% sama dengan Rp200 juta, provisi 1% Rp100 juta, ditambah biaya notaris, penilaian, dan administrasi. Kalau bunga baru 1,5 poin persen lebih rendah, penghematan bunga tahun pertama sekitar Rp150 juta dan terus mengecil seiring pokok turun. "
 "Dalam contoh ini take over baru menguntungkan bila tenor cukup panjang atau ada tambahan plafon yang memang dibutuhkan. Hitungan versi Anda bisa dimulai dari <a href=\"/cek-kapasitas-kredit/\">Cek Kapasitas Kredit</a>.</p>"
 "<p>Bila agunan perlu dinilai ulang, ringkasan perannya ada di artikel CariAkuntan tentang <a href=\"https://cariakuntan.com/artikel/penilaian-agunan-kjpp-untuk-kredit/\">penilaian agunan oleh KJPP untuk kredit</a>.</p>"
)
faq = [
 ("Berapa biaya take over kredit usaha?", "Komponen utamanya penalti pelunasan dipercepat di bank lama (umumnya sekitar 2% sampai 3% dari sisa pokok), provisi bank baru (sekitar 1% dari plafon), administrasi, penilaian agunan, notaris, dan asuransi. Angka pasti mengikuti perjanjian kredit dan penawaran bank."),
 ("Apakah take over kredit bisa sekaligus menambah plafon?", "Bisa, selama kemampuan bayar dan nilai agunan mendukung. Bank baru menghitung ulang dari laporan keuangan, proyeksi arus kas, dan hasil penilaian agunan."),
 ("Berapa lama proses take over?", "Tergantung kelengkapan berkas dan antrean analisis bank. Yang paling sering memperlambat adalah laporan keuangan yang belum siap, data omzet yang berbeda dengan SPT, dan dokumen agunan yang belum lengkap."),
 ("Apakah debitur dengan kredit bermasalah bisa take over?", "Sulit. Bank baru melihat riwayat di SLIK. Debitur dengan kolektibilitas bermasalah biasanya perlu memperbaiki riwayat pembayaran atau membahas restrukturisasi dengan bank lama lebih dulu."),
]
art_page(S1, "Kredit Bank", "Syarat, Biaya, dan Cara Take Over Kredit Usaha ke Bank Lain Terbaru 2026 | FA Indonesia",
         "Syarat, Biaya, dan Cara Take Over Kredit Usaha ke Bank Lain Terbaru 2026",
         "Take over kredit usaha ke bank lain: rincian biaya (penalti, provisi, appraisal, notaris), syarat dan dokumen, enam langkah proses, dan contoh hitungan untung rugi.",
         6, body, faq,
         [("/cek-kapasitas-kredit/", "Cek Kapasitas Kredit"), ("/artikel/kmk-vs-kredit-investasi/", "KMK vs Kredit Investasi"),
          ("/artikel/rasio-keuangan-yang-dilihat-bank/", "Rasio Keuangan yang Dilihat Bank"), ("/artikel/alasan-kredit-bank-ditolak/", "Alasan Kredit Bank Ditolak")],
         [("OCBC: Cara Take Over KPR ke Bank Lain, Proses dan Biaya", "https://www.ocbc.id/id/article/2025/11/28/cara-take-over-kpr-ke-bank-lain-proses-biaya-dan-keuntungannya"),
          ("Cermati: Surat Roya Setelah Kredit Lunas", "https://www.cermati.com/artikel/cicilan-kpr-tinggal-sekali-bayar-segera-urus-surat-roya-apa-itu")],
         "/cek-kapasitas-kredit/", "Cek Kapasitas Kredit",
         "Halo FA Indonesia, kami ingin memindahkan kredit usaha ke bank lain (take over) dan ingin menghitung untung ruginya.")

def strip_v(t): return re.sub(r"<!--fa-viral-b-->.*?<!--/fa-viral-b-->\n?", "", t, flags=re.S)
ip = P("artikel", "index.html"); t = strip_v(rd(ip))
k = t.find('id="t-kredit-bank"')
if k >= 0:
    k = t.find('<div class="cards2">', k) + len('<div class="cards2">')
    t = t[:k] + f'<!--fa-viral-b--><a class="card2" href="/artikel/{S1}/"><b>Syarat, Biaya, dan Cara Take Over Kredit Usaha</b><span>Rincian biaya pindah bank, dokumen, enam langkah, dan contoh hitungan untung rugi.</span></a><!--/fa-viral-b-->' + t[k:]
    wtxt(ip, t)
sm = strip_v(rd(P("sitemap.xml")))
sm = sm.replace("</urlset>", f"<!--fa-viral-b-->\n<url><loc>{D}/artikel/{S1}/</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n<!--/fa-viral-b-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = re.sub(r"\n- \[Take Over Kredit Usaha\].*", "", rd(P("llms.txt")))
wtxt(P("llms.txt"), ll.rstrip("\n") + f"\n- [Take Over Kredit Usaha]({D}/artikel/{S1}/): syarat, biaya, dan cara memindahkan kredit usaha ke bank lain\n")
print("viral FA b:", S1)
