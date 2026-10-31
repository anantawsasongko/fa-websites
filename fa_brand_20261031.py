# -*- coding: utf-8 -*-
"""Halaman /mitra-kap-kja/ (31 Okt 2026): jaringan mitra FA Indonesia: KAP DHN & Rekan, KJA DHN, KKP DHN, KJA Farhani.
Target kata kunci: KAP, KJA, kantor jasa akuntansi, konsultan pajak, nama mitra. Footer "Mitra KAP & KJA", sitemap, llms.
Idempoten. Jalankan setelah fa_seo20_20261030.py, sebelum fa_rapi_20261027.py."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_mitra_20261027.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. MITRA RM BANK")]
_src = _src.replace('TODAY = "2026-10-27"', 'TODAY = "2026-10-31"').replace("27 Oktober 2026", "31 Oktober 2026")
exec(compile(_src, "fa_mitra_helpers", "exec"))

PTH = "/mitra-kap-kja/"
WA_M = "Halo FA Indonesia, kami butuh KAP / KJA / konsultan pajak untuk perusahaan kami. Kebutuhan kami: ..."
body = (
 "<h2>Mitra Profesional FA Indonesia</h2>"
 + gain([
   ("KAP DHN & Rekan", "Kantor Akuntan Publik untuk audit umum laporan keuangan, audit untuk kredit bank, BPR dan koperasi, serta perikatan reviu dan prosedur yang disepakati. Berkantor pusat di Bali."),
   ("KJA DHN", "Kantor Jasa Akuntansi untuk pembukuan, kompilasi, dan penyusunan laporan keuangan sesuai SAK EMKM, SAK EP, atau PSAK."),
   ("KKP DHN", "Kantor Konsultan Pajak untuk kepatuhan bulanan dan tahunan, rekonsiliasi fiskal, Coretax, serta pendampingan pemeriksaan pajak."),
   ("KJA Farhani, Malang", "Kantor Jasa Akuntansi di Malang untuk pembukuan dan laporan keuangan UMKM sampai perusahaan menengah, dipimpin Akuntan Berpraktik."),
 ])
 + "<h2>Satu Pintu dari Pembukuan sampai Dana Cair</h2>"
 + flow([("Pembukuan dan Laporan Keuangan", "KJA mitra merapikan pembukuan dan menyusun laporan keuangan."),
         ("Pajak", "KKP mitra merekonsiliasi pajak dan menyiapkan SPT agar angka laporan dan pajak sejalan."),
         ("Audit", "KAP mitra mengaudit laporan keuangan secara independen."),
         ("Kredit, Investor, atau IPO", "Tim FA Indonesia menyusun paket pendanaan dan mendampingi sampai dana cair.")])
 + "<h2>Kapan Butuh KAP, KJA, atau KKP</h2>"
 + tbl(["Kebutuhan", "Kantor yang Tepat", "Contoh"], [
   ("Laporan keuangan diaudit untuk bank, tender, atau wajib audit", "KAP", "Opini audit atas laporan keuangan tahunan"),
   ("Pembukuan rapi dan laporan keuangan siap pakai", "KJA", "Kompilasi laporan keuangan, pembukuan bulanan"),
   ("Kepatuhan dan pemeriksaan pajak", "KKP", "SPT tahunan, SP2DK, pemeriksaan"),
   ("Penilaian agunan atau aset", "KJPP", '<a href="https://cariakuntan.com/layanan/kjpp/">Pilih KJPP lewat CariAkuntan</a>'),
 ])
 + "<p>Independensi tetap dijaga. Kantor yang menyusun laporan keuangan atau menjadi konsultan pajak suatu perusahaan tidak mengaudit perusahaan yang sama. Pembagian peran diatur sejak awal perikatan.</p>"
 + "<h2>Layani Seluruh Indonesia</h2><p>Mitra kami melayani perusahaan dari Aceh sampai Papua secara daring dan dengan kunjungan lapangan terjadwal. Lihat layanan per kota di <a href=\"/wilayah/\">FA per Kota</a>, misalnya <a href=\"/wilayah/jakarta/\">FA Jakarta</a>, <a href=\"/wilayah/surabaya/\">FA Surabaya</a>, <a href=\"/wilayah/malang/\">FA Malang</a>, <a href=\"/wilayah/bandung/\">FA Bandung</a>, dan <a href=\"/wilayah/denpasar/\">FA Denpasar</a>.</p>"
 + "<p>Ingin membandingkan dengan kantor lain di kota Anda? Gunakan <a href=\"https://cariakuntan.com/\">Cari Akuntan</a>. Untuk cek standar akuntansi terbaru sebelum audit, buka <a href=\"https://updatesak.com/\">Update SAK</a>. Profil KJA Farhani: <a href=\"/kja-farhani/\">KJA Farhani, Malang</a>.</p>")
FAQ = [("Apakah FA Indonesia punya mitra KAP?", "Ya. FA Indonesia bermitra dengan KAP DHN & Rekan untuk audit laporan keuangan, termasuk audit untuk kredit bank, BPR, dan koperasi."),
       ("Apa beda KAP dan KJA?", "KAP memberi opini audit atas laporan keuangan. KJA menyusun pembukuan dan laporan keuangan tanpa memberi opini audit."),
       ("Apakah satu kantor bisa menyusun sekaligus mengaudit laporan keuangan?", "Tidak. Untuk menjaga independensi, penyusun laporan keuangan dan auditor adalah pihak berbeda. FA Indonesia mengatur pembagian peran antar mitra sejak awal."),
       ("Apakah bisa untuk perusahaan di luar Malang dan Bali?", "Bisa. Mitra melayani seluruh Indonesia secara daring dengan kunjungan lapangan terjadwal."),
       ("Berapa biayanya?", "Diskusi awal gratis. Lingkup dan biaya tiap kantor disepakati di depan sesuai kebutuhan perusahaan.")]
partner_page(PTH, "Mitra · KAP, KJA, dan Konsultan Pajak",
  "Mitra KAP, KJA, dan Konsultan Pajak FA Indonesia: KAP DHN & Rekan, KJA DHN, KKP DHN, KJA Farhani",
  "Butuh KAP untuk audit, KJA untuk pembukuan dan laporan keuangan, atau konsultan pajak? FA Indonesia bekerja dengan jaringan mitra lengkap, sehingga pembukuan, pajak, audit, sampai kredit bank dan investor bisa diurus dari satu pintu.",
  body, FAQ, "Mitra KAP dan KJA: KAP DHN, KJA DHN, KKP DHN, KJA Farhani | FA Indonesia",
  "KAP, KJA, dan konsultan pajak mitra FA Indonesia: KAP DHN & Rekan, KJA DHN, KKP DHN, KJA Farhani. Audit, pembukuan, pajak, sampai kredit cair. Konsultasi gratis.",
  "Pemilik usaha dan direksi yang membutuhkan KAP, KJA, atau konsultan pajak", WA_M, "Mitra KAP dan KJA")

# footer: "Mitra KAP & KJA" setelah "Mitra Investor"
FT = '<li><a href="/mitra-kap-kja/">Mitra KAP &amp; KJA</a></li>'
for d, _, fs in os.walk(FA):
    for f in fs:
        if not f.endswith(".html"): continue
        p = os.path.join(d, f); t = rd(p)
        if '/mitra-kap-kja/">Mitra KAP' in t or "<footer" not in t: continue
        k = t.find('Mitra Investor</a></li>', t.find("<footer"))
        if k < 0: continue
        k += len('Mitra Investor</a></li>')
        wtxt(p, t[:k] + FT + t[k:])

sm = re.sub(r"<!--fa-brand-->.*?<!--/fa-brand-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", f"<!--fa-brand-->\n<url><loc>{D}{PTH}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n<!--/fa-brand-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = re.sub(r"\n## Mitra KAP dan KJA.*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + f"\n\n## Mitra KAP dan KJA\n- FA Indonesia bermitra dengan KAP DHN & Rekan (audit), KJA DHN dan KJA Farhani Malang (pembukuan dan laporan keuangan), KKP DHN (konsultan pajak) → {D}{PTH}\n- Halaman per kota: FA Jakarta, FA Surabaya, FA Malang, FA Bandung, dan 90+ kota → {D}/wilayah/\n"
wtxt(P("llms.txt"), ll)
print("mitra kap kja ok")
