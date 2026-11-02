# -*- coding: utf-8 -*-
"""/kap-dhn/ (1 Nov 2026): halaman mitra KAP DHN & Rekan di FA, menyasar pencarian "KAP DHN", "KAP Dwi Haryadi Nugraha".
Lead masuk lewat WA FA (referral), website resmi DHN tetap disebut di bagian bawah.
Juga: link "KAP DHN & Rekan" di /mitra-kap-kja/ diarahkan ke /kap-dhn/. Sitemap, llms. Idempoten (penanda fa-dhn).
Jalankan setelah fa_lead_20261101.py (pakai helper fa_lead_20261026.py)."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-01"')
exec(compile(_src, "fa_lead_helpers", "exec"))

PD = "/kap-dhn/"
body = (
 "<h2>Tentang KAP DHN &amp; Rekan</h2>"
 "<p>KAP DHN &amp; Rekan (Kantor Akuntan Publik Dwi Haryadi Nugraha dan Rekan) adalah kantor akuntan publik berizin Kementerian Keuangan yang juga terdaftar di OJK untuk sektor perbankan, pasar modal, IKNB, dan syariah, serta terdaftar di BPK RI. Kantor pusatnya di Denpasar, anggota jaringan internasional PA Global, dan berpengalaman mengaudit BPR serta lembaga keuangan.</p>"
 "<p>FA Indonesia adalah mitra KAP DHN &amp; Rekan. Melalui FA, perusahaan mendapat satu pintu: laporan keuangan dirapikan dulu, dokumen audit disiapkan, lalu audit berjalan di KAP DHN dengan jadwal yang jelas.</p>"
 "<h2>Layanan Audit dan Asurans</h2>"
 + tbl(["Layanan", "Untuk Siapa", "Kegunaan"], [
   ("Audit umum laporan keuangan", "PT, CV, yayasan, koperasi", "Wajib audit, RUPS, pemegang saham"),
   ("Audit untuk kredit bank", "Perusahaan yang mengajukan atau memperpanjang kredit", "Syarat analis kredit dan komite"),
   ("Audit BPR dan lembaga keuangan", "BPR, BPRS, koperasi simpan pinjam, IKNB", "Kewajiban regulator dan OJK"),
   ("Audit untuk tender dan kualifikasi vendor", "Kontraktor dan pemasok", "Syarat dokumen tender"),
   ("Reviu dan prosedur yang disepakati (AUP)", "Perusahaan, investor, bank", "Keyakinan terbatas atau temuan atas hal tertentu"),
 ])
 + "<h2>Kenapa Lewat FA Indonesia</h2>" + flow([
   ("Cek kebutuhan", "Kami pastikan jenis perikatan yang tepat: audit, reviu, atau AUP, dan apakah bank atau regulator Anda mensyaratkan KAP terdaftar OJK."),
   ("Rapikan laporan", "Bila laporan keuangan belum siap, KJA mitra merapikannya lebih dulu supaya audit tidak molor dan biaya tidak membengkak."),
   ("Siapkan dokumen", "Daftar PBC, lead schedule, dan rekonsiliasi disiapkan sebelum auditor datang."),
   ("Audit di KAP DHN", "Audit dilaksanakan KAP DHN &amp; Rekan secara independen."),
   ("Lanjut ke tujuan", "Laporan audit dipakai untuk kredit, tender, investor, atau kewajiban regulator, dan kami dampingi sampai tahap itu.")])
 + "<p>Independensi tetap dijaga: pihak yang menyusun laporan keuangan atau menjadi konsultan pajak Anda tidak mengaudit perusahaan yang sama.</p>"
 "<h2>Wilayah Layanan</h2><p>Berkantor pusat di Denpasar, melayani perusahaan di Bali dan seluruh Indonesia secara daring dan dengan kunjungan lapangan terjadwal. Lihat juga layanan per kota di <a href=\"/wilayah/\">FA per Kota</a>, misalnya <a href=\"/wilayah/denpasar/\">FA Denpasar</a>, <a href=\"/wilayah/malang/\">FA Malang</a>, dan <a href=\"/wilayah/surabaya/\">FA Surabaya</a>.</p>"
 "<h2>Mitra Lain dalam Satu Jaringan</h2><p>Untuk pembukuan dan penyusunan laporan keuangan tersedia KJA DHN dan KJA Farhani, untuk pajak tersedia KKP DHN. Selengkapnya di <a href=\"/mitra-kap-kja/\">Mitra KAP, KJA, dan Konsultan Pajak FA</a>.</p>"
 "<p style=\"font-size:13px;opacity:.75\">Halaman ini dikelola FA Indonesia sebagai mitra. Website resmi KAP DHN &amp; Rekan: <a href=\"https://kap.akuntan-dhnr.com/\" rel=\"nofollow noopener\" target=\"_blank\">kap.akuntan-dhnr.com</a>.</p>")
FAQ = [
 ("Bagaimana cara menghubungi KAP DHN & Rekan?", "Anda bisa menghubungi tim FA Indonesia lewat tombol WhatsApp di halaman ini. Kami membantu memastikan jenis perikatan, menyiapkan dokumen, dan menjadwalkan audit dengan KAP DHN & Rekan."),
 ("Apakah KAP DHN terdaftar di OJK?", "Ya. KAP DHN & Rekan terdaftar di OJK untuk sektor perbankan, pasar modal, IKNB, dan syariah, sehingga bisa dipakai untuk kebutuhan yang mensyaratkan KAP terdaftar OJK."),
 ("Apakah KAP DHN bisa mengaudit perusahaan di luar Bali?", "Bisa. Perusahaan di luar Bali dilayani secara daring dan dengan kunjungan lapangan terjadwal."),
 ("Berapa biaya audit di KAP DHN?", "Bergantung pada ukuran perusahaan, jumlah transaksi, kerapian laporan keuangan, dan tujuan audit. Estimasi disampaikan setelah diskusi awal dan melihat laporan keuangan terakhir."),
 ("Laporan keuangan saya belum rapi, apakah bisa langsung diaudit?", "Sebaiknya dirapikan dulu. Audit atas laporan yang belum rapi biasanya lebih lama, lebih mahal, dan berisiko opini tidak wajar. KJA mitra kami bisa membantu sebelum audit dimulai."),
]
svc_page(PD, "Mitra · Kantor Akuntan Publik", "KAP DHN & Rekan: Audit Laporan Keuangan, BPR, dan Kredit Bank Melalui FA Indonesia",
  "KAP DHN &amp; Rekan (Dwi Haryadi Nugraha dan Rekan) adalah kantor akuntan publik berizin Kemenkeu, terdaftar OJK dan BPK RI, berkantor pusat di Denpasar. Konsultasikan kebutuhan audit Anda lewat FA Indonesia sebagai mitra: laporan dirapikan, dokumen disiapkan, audit berjalan tepat waktu.",
  body, FAQ, "KAP DHN & Rekan: Kantor Akuntan Publik Terdaftar OJK, Denpasar | FA Indonesia",
  "KAP DHN & Rekan (Dwi Haryadi Nugraha dan Rekan): audit laporan keuangan, BPR, kredit bank, tender. Berizin Kemenkeu, terdaftar OJK dan BPK RI. Konsultasi lewat FA Indonesia.",
  "Audit melalui KAP DHN & Rekan", "Audit and assurance referral",
  "/mitra-kap-kja/", "Semua Mitra", "Halo FA Indonesia, saya ingin konsultasi audit dengan KAP DHN & Rekan.", "KAP DHN & Rekan")

# /mitra-kap-kja/: nama KAP DHN di kartu dan link website mitra diarahkan ke /kap-dhn/
mp = P("mitra-kap-kja", "index.html"); t = rd(mp)
t = re.sub(r'<a href="https://www\.kapdhn\.com/"[^>]*>KAP DHN &amp; Rekan</a>', '<a href="/kap-dhn/">KAP DHN &amp; Rekan</a>', t)
t = re.sub(r"<!--fa-dhn-->.*?<!--/fa-dhn-->", "", t, flags=re.S)
k = t.find("<h2>Satu Pintu")
if k > 0:
    t = t[:k] + '<!--fa-dhn--><p><a class="btn line" href="/kap-dhn/">Profil KAP DHN &amp; Rekan</a></p><!--/fa-dhn-->' + t[k:]
wtxt(mp, t)

sm = re.sub(r"<!--fa-dhn-->.*?<!--/fa-dhn-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", f"<!--fa-dhn-->\n<url><loc>{D}{PD}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n<!--/fa-dhn-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = rd(P("llms.txt"))
line = "- KAP DHN & Rekan (Dwi Haryadi Nugraha dan Rekan, Denpasar, terdaftar OJK dan BPK RI), mitra audit FA Indonesia → https://faindonesia.co.id/kap-dhn/\n"
ll = ll.replace(line, "")
ll = ll.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + line, 1) if "\n## Layanan Spesifik\n" in ll else ll.rstrip("\n") + "\n\n## Layanan Spesifik\n" + line
wtxt(P("llms.txt"), ll)
print("fa_dhn ok")
