# -*- coding: utf-8 -*-
"""Dua artikel pendukung halaman /jasa-pembukuan/ (3 Nov 2026). Output gen/pembukuan.json."""
import json, os
D = "2026-11-03"
CTA = '<p><a href="/jasa-pembukuan/">Lihat paket Jasa Pembukuan Terima Beres</a> atau <a href="/files/contoh-laporan-keuangan-bulanan-jasa-pembukuan.pdf">unduh contoh laporan bulanan</a>.</p>'
A = [
 {"slug": "harga-jasa-pembukuan-2026-paket-dan-yang-menentukan", "title": "Harga Jasa Pembukuan 2026: Paket, Kisaran, dan Yang Menentukan", "tag": "Jasa Laporan Keuangan", "date": D,
  "desc": "Harga jasa pembukuan ditentukan jumlah transaksi, rekening, dan persediaan. Kisaran paket UMKM dan PT, biaya yang sering terpisah, dan cara membandingkan penawaran.",
  "msg": "Selamat siang Pak Ananta, saya ingin tahu harga jasa pembukuan untuk usaha saya.",
  "body": "<p>Harga jasa pembukuan jarang bisa dibandingkan langsung karena isi paketnya berbeda-beda. Cara paling aman: samakan dulu apa yang dikerjakan, baru bandingkan harganya.</p>"
   "<h2>Yang Menentukan Harga</h2><ul><li>Jumlah transaksi per bulan.</li><li>Jumlah rekening bank dan e-wallet.</li><li>Ada tidaknya persediaan dan aset tetap.</li><li>Kerapian bon dan catatan yang dikirim.</li><li>Standar laporan: SAK EMKM atau SAK EP.</li></ul>"
   "<h2>Kisaran Paket Kami</h2><table><tr><th>Paket</th><th>Mulai</th></tr><tr><td>Pembukuan UMKM dan perorangan</td><td>Rp900 ribu/bulan</td></tr><tr><td>Pembukuan PT dan CV</td><td>Rp2 juta/bulan</td></tr><tr><td>Laporan tahunan PT (SABH)</td><td>Rp3 juta, belum termasuk notaris</td></tr><tr><td>SPT Tahunan Badan</td><td>Rp3 juta</td></tr><tr><td>Pajak bulanan oleh KKP mitra</td><td>Rp3 juta</td></tr></table>"
   "<h2>Biaya yang Sering Terpisah</h2><ul><li>Lapor pajak bulanan dan SPT tahunan.</li><li>Laporan tahunan PT dan biaya notaris.</li><li>Penyusunan ulang pembukuan bulan-bulan yang tertinggal.</li><li>Audit oleh KAP.</li></ul>"
   "<h2>Cara Membandingkan Penawaran</h2><ol><li>Minta contoh laporan yang akan diterima.</li><li>Tanyakan kapan laporan dikirim setiap bulan.</li><li>Pastikan siapa yang mengerjakan dan izinnya.</li></ol>" + CTA, "sources": []},
 {"slug": "aplikasi-akuntansi-atau-jasa-pembukuan-mana-yang-tepat", "title": "Aplikasi Akuntansi atau Jasa Pembukuan: Mana yang Tepat untuk Usaha Anda", "tag": "Jasa Laporan Keuangan", "date": D,
  "desc": "Aplikasi akuntansi butuh orang yang sempat dan paham menginput. Jasa pembukuan cocok bila Anda ingin terima beres. Perbandingan jujur dan kapan keduanya digabung.",
  "msg": "Selamat siang Pak Ananta, saya sudah pakai aplikasi akuntansi tapi tidak sempat input, bisa dibantu?",
  "body": "<p>Banyak pemilik usaha berlangganan aplikasi akuntansi, lalu datanya berhenti diisi setelah dua atau tiga bulan. Masalahnya bukan aplikasinya, tetapi tidak ada orang yang sempat dan paham menginput.</p>"
   "<h2>Perbandingan Singkat</h2><table><tr><th></th><th>Aplikasi</th><th>Jasa Pembukuan</th></tr><tr><td>Yang menginput</td><td>Anda atau staf</td><td>Akuntan</td></tr><tr><td>Butuh paham akuntansi</td><td>Ya</td><td>Tidak</td></tr><tr><td>Biaya utama</td><td>Langganan plus gaji staf</td><td>Fee bulanan</td></tr><tr><td>Laporan siap bank dan pajak</td><td>Bergantung input</td><td>Ya, direview akuntan</td></tr></table>"
   "<h2>Kapan Aplikasi Cukup</h2><p>Bila sudah ada staf keuangan yang paham jurnal dan sempat menginput setiap hari, aplikasi adalah alat yang efisien.</p>"
   "<h2>Kapan Jasa Pembukuan Lebih Tepat</h2><ul><li>Pemilik mengurus semua sendiri.</li><li>Bon menumpuk dan laporan tidak pernah jadi.</li><li>Laporan dibutuhkan untuk bank, SPT, atau laporan tahunan PT.</li></ul>"
   "<h2>Bisa Digabung</h2><p>Kami bisa bekerja langsung di aplikasi yang sudah Anda pakai, misalnya Jurnal, Accurate, atau Zahir. Anda tetap memegang aplikasinya, kami yang mengisi dan merapikan.</p>" + CTA, "sources": []},
]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen", "pembukuan.json")
json.dump(A, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
assert "—" not in open(out).read(); print("pembukuan.json", len(A))
