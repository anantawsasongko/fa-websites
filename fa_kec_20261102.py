# -*- coding: utf-8 -*-
"""SEO tingkat kecamatan + layanan khusus (2 Nov 2026).
1) /wilayah/<kota>/kecamatan/<kec>/ untuk 2.000+ kecamatan di kota/kabupaten yang sudah punya halaman wilayah, plus hub /wilayah/<kota>/kecamatan/.
2) Halaman layanan: /audit-dana-kampanye/, /audit-koperasi-desa-merah-putih/, /laporan-keuangan-audit-sppg/.
Setiap halaman memuat kotak tim: Ananta W. Sasongko (profil), KJA Farhani (laporan keuangan), KAP DHN & Rekan (audit), WA.
Idempoten. Jalankan setelah fa_audit_20261102.py."""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-02"')
exec(compile(_src, "fa_lead_helpers", "exec"))
sys.path.insert(0, os.path.join(HERE, "cariakuntan")); sys.path.insert(0, os.path.join(HERE, "shared", "wilayah"))
from cities import CITIES, SECTOR_LINES
import kec as KC

def team(ctx):
    return ('<h2>Tim yang Menangani</h2><div class="tblwrap"><table><tr><th>Peran</th><th>Siapa</th><th>Untuk Apa</th></tr>'
            '<tr><td>Koordinator dan kontak</td><td><a href="/ananta-w-sasongko/">Ananta W. Sasongko, Ak, CPA</a></td><td>Diskusi awal, ruang lingkup, jadwal, dan biaya</td></tr>'
            '<tr><td>Laporan keuangan</td><td><a href="/kja-farhani/">KJA Farhani</a> (izin KMK No. 232/KM.1/PPPK/2020)</td><td>Pembukuan dan penyusunan laporan keuangan ' + ctx + '</td></tr>'
            '<tr><td>Audit</td><td><a href="/kap-dhn/">KAP DHN &amp; Rekan</a> (KMK No. 592/KM.1/2023, terdaftar OJK)</td><td>Audit laporan keuangan dan prosedur yang disepakati</td></tr></table></div>'
            '<p>Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda. Hubungi kami lewat tombol WhatsApp di halaman ini.</p>')

# ================= 1. HALAMAN LAYANAN KHUSUS =================
SVC = []
P1 = "/audit-dana-kampanye/"
b1 = ("<h2>Laporan Dana Kampanye yang Wajib Disusun</h2>"
 + tbl(["Laporan", "Isi", "Diserahkan ke"], [
   ("LADK (Laporan Awal Dana Kampanye)", "Rekening khusus dana kampanye, saldo awal, dan penerimaan sumbangan", "KPU sesuai tingkatannya"),
   ("LPSDK (Laporan Pemberi Sumbangan)", "Sumbangan dari perseorangan, kelompok, dan badan usaha nonpemerintah", "KPU sesuai tingkatannya"),
   ("LPPDK (Laporan Penerimaan dan Pengeluaran)", "Pembukuan seluruh penerimaan dan pengeluaran dana kampanye", "Kantor akuntan publik untuk diaudit, hasilnya ke KPU")])
 + "<p>Untuk Pemilu 2024 ketentuannya diatur dalam PKPU Nomor 18 Tahun 2023 yang merujuk UU Pemilu. Pilkada punya PKPU tersendiri dengan alur serupa. Tahapan dan tenggatnya selalu mengikuti jadwal KPU untuk pemilihan yang bersangkutan.</p>"
 "<h2>Masalah yang Paling Sering Ditemukan Auditor</h2><ul>"
 "<li>Pengeluaran dibayar dari rekening pribadi, bukan rekening khusus dana kampanye.</li>"
 "<li>Sumbangan tanpa identitas lengkap atau melebihi batas.</li>"
 "<li>Bukti pengeluaran tim di daerah tidak lengkap, terutama belanja tunai.</li>"
 "<li>Sumbangan dalam bentuk barang dan jasa belum dinilai dan dicatat.</li></ul>"
 "<h2>Yang Kami Kerjakan</h2>" + flow([
   ("Rekening dan buku", "Rekening khusus, bagan akun, dan format bukti untuk tim pusat dan daerah."),
   ("Rekap berkala", "Penerimaan dan pengeluaran direkap mingguan, sumbangan dicek identitas dan batasnya."),
   ("Susun laporan", "LADK, LPSDK, dan LPPDK disusun sesuai format KPU dan tepat waktu."),
   ("Siap diaudit", "Dokumen pendukung disiapkan agar audit kepatuhan oleh KAP berjalan lancar.")])
 + team("dana kampanye partai, calon, atau tim pemenangan"))
F1 = [("Siapa yang mengaudit laporan dana kampanye?", "LPPDK diserahkan kepada kantor akuntan publik untuk diaudit, lalu hasil auditnya disampaikan kepada KPU sesuai jadwal tahapan pemilihan."),
      ("Apakah calon legislatif perorangan juga harus melapor?", "Ketentuannya berbeda untuk tiap jenis peserta. Partai politik melaporkan dana kampanye termasuk calegnya, dan calon perseorangan seperti calon DPD atau kepala daerah melapor sendiri. Kami bantu memetakan kewajiban sesuai jenis pemilihan."),
      ("Kapan sebaiknya mulai menyiapkan pembukuan dana kampanye?", "Sejak rekening khusus dana kampanye dibuka. Menyusun ulang bukti setelah kampanye selesai jauh lebih sulit dan berisiko temuan.")]
SVC.append((P1, "Layanan · Dana Kampanye", "Audit dan Laporan Dana Kampanye: LADK, LPSDK, LPPDK Siap Diaudit KAP",
  "Pendampingan pembukuan dan laporan dana kampanye untuk partai politik, calon kepala daerah, calon perseorangan, dan tim pemenangan, sampai siap diaudit kantor akuntan publik.",
  b1, F1, "Audit Dana Kampanye: Laporan LADK, LPSDK, LPPDK | FA Indonesia",
  "Pembukuan dan laporan dana kampanye LADK, LPSDK, LPPDK untuk partai, calon kepala daerah, dan tim pemenangan, siap diaudit KAP. Diskusi awal gratis.",
  "Pendampingan Laporan Dana Kampanye", "Campaign finance reporting", "Halo FA Indonesia, kami perlu pendampingan laporan dan audit dana kampanye.", "Dana Kampanye"))

P2 = "/audit-koperasi-desa-merah-putih/"
b2 = ("<h2>Kenapa Laporan Keuangan KDMP Penting Sejak Awal</h2>"
 "<p>Koperasi Desa/Kelurahan Merah Putih (KDMP) dibentuk serentak di seluruh desa dan kelurahan berdasarkan Inpres Nomor 9 Tahun 2025. Banyak KDMP mengelola modal, pinjaman, dan unit usaha dalam jumlah besar sejak tahun pertama. Laporan keuangan menjadi dasar Rapat Anggota Tahunan (RAT), pertanggungjawaban pengurus, dan pengajuan pembiayaan.</p>"
 "<h2>Laporan yang Disusun</h2>"
 + tbl(["Laporan", "Kegunaan"], [
   ("Laporan posisi keuangan", "Aset, utang pembiayaan, simpanan anggota, dan ekuitas koperasi"),
   ("Perhitungan hasil usaha", "Sisa hasil usaha (SHU) per unit usaha: gerai sembako, simpan pinjam, apotek desa, klinik, gudang, logistik"),
   ("Laporan arus kas", "Kemampuan membayar angsuran pembiayaan"),
   ("Catatan atas laporan keuangan", "Kebijakan akuntansi, rincian pinjaman, dan transaksi dengan pihak berelasi")])
 + "<h2>KDMP Pakai SAK yang Mana?</h2><p>Permenkop UKM 2/2024 tentang Kebijakan Akuntansi Koperasi (berlaku 16 Januari 2024, mencabut Permenkop 12, 13, dan 14 Tahun 2015) menentukan SAK dari kegiatan usaha. Pengingat yang sama disampaikan Ikatan Akuntan Indonesia pada 3 November 2026.</p>"
 + tbl(["Kegiatan Usaha", "SAK yang Dapat Dipakai"], [
   ("Simpan pinjam anggota", "SAK Indonesia atau SAK EP"),
   ("Sektor riil: gerai, jasa, logistik, pengolahan", "Standar instansi pembina bila ada; bila belum: SAK Indonesia, SAK EP, atau SAK EMKM")])
 + "<p>Satu koperasi menyusun satu set laporan dengan satu kerangka SAK. KDMP yang punya unit simpan pinjam praktis memakai SAK EP: pinjaman anggota dan pinjaman bank dengan metode bunga efektif, cadangan kerugian pinjaman berdasarkan bukti tunggakan, dan nilai wajar untuk pos tertentu. Kami bantu menetapkan kebijakan akuntansinya sejak tutup buku pertama. Ringkasan teknis: <a href=\"https://updatesak.com/artikel/sak-untuk-kdkmp-koperasi-desa-merah-putih-permenkop-2-2024/\">SAK untuk KDKMP di UpdateSAK</a>. Halaman per kecamatan seluruh Indonesia: <a href=\"https://cariakuntan.com/kdmp/\">KDMP per Kecamatan</a>.</p>"
 "<h2>Kapan KDMP Perlu Audit</h2><ul>"
 "<li>Diminta bank atau lembaga pembiayaan sebagai syarat pencairan atau evaluasi pinjaman.</li>"
 "<li>Diputuskan rapat anggota untuk memperkuat kepercayaan anggota.</li>"
 "<li>Diminta pemerintah daerah, pendamping, atau pemeriksa program.</li>"
 "<li>Koperasi menjalankan usaha simpan pinjam dengan skala yang mensyaratkan audit.</li></ul>"
 "<p>Bila audit penuh belum diperlukan, prosedur yang disepakati (AUP) atas penggunaan dana pinjaman bisa menjadi pilihan yang lebih ringan.</p>"
 "<h2>Paket untuk KDMP</h2>" + flow([
   ("Setup pembukuan", "Bagan akun per unit usaha, format kas harian, dan pemisahan simpanan anggota."),
   ("Laporan bulanan", "Laporan sederhana untuk pengurus dan pengawas."),
   ("Laporan tahunan dan RAT", "Laporan keuangan lengkap untuk RAT dan pembagian SHU."),
   ("Audit atau AUP", "Bila diminta bank, anggota, atau pemeriksa.")])
 + "<p>Bacaan terkait: <a href=\"https://cariakuntan.com/artikel/laporan-keuangan-koperasi-desa-merah-putih/\">Laporan Keuangan Koperasi Desa Merah Putih</a> dan <a href=\"https://cariakuntan.com/artikel/cicilan-pertama-kopdes-merah-putih-september-2026/\">Cicilan Pertama Kopdes Merah Putih</a>.</p>"
 + team("koperasi"))
F2 = [("Apakah Koperasi Desa Merah Putih wajib diaudit akuntan publik?", "Tidak semua. Audit diperlukan bila diminta bank atau lembaga pembiayaan, diputuskan rapat anggota, diminta pemeriksa program, atau koperasi menjalankan simpan pinjam dengan skala tertentu. Yang wajib bagi semua KDMP adalah laporan keuangan untuk RAT."),
      ("Standar akuntansi apa yang dipakai KDMP?", "Menurut Permenkop UKM 2/2024, ditentukan kegiatan usahanya. Bila ada unit simpan pinjam, SAK Indonesia atau SAK EP; bila murni sektor riil dan belum ada standar instansi pembina, boleh SAK Indonesia, SAK EP, atau SAK EMKM. Dalam praktik KDMP yang menjalankan simpan pinjam umumnya memakai SAK EP."),
      ("Apakah melayani KDMP di desa terpencil?", "Ya. Pembukuan dan penyusunan laporan bisa dikerjakan daring dari foto bukti dan mutasi rekening; kunjungan dijadwalkan bila diperlukan audit.")]
SVC.append((P2, "Layanan · Koperasi", "Laporan Keuangan dan Audit Koperasi Desa Merah Putih (KDMP)",
  "Pembukuan, laporan keuangan untuk RAT, dan audit atau AUP bagi Koperasi Desa/Kelurahan Merah Putih di seluruh Indonesia. Dikerjakan daring, siap untuk anggota, bank, dan pemeriksa.",
  b2, F2, "Laporan Keuangan dan Audit Koperasi Desa Merah Putih (KDMP) | FA Indonesia",
  "Pembukuan, laporan keuangan RAT, dan audit KDMP Kopdes Merah Putih: SAK EP/EMKM, SHU per unit usaha, siap untuk bank. Diskusi awal gratis.",
  "Laporan Keuangan dan Audit KDMP", "Cooperative accounting and audit", "Halo FA Indonesia, kami pengurus Koperasi Desa Merah Putih dan perlu bantuan laporan keuangan/audit.", "Koperasi Desa Merah Putih"))

P3 = "/laporan-keuangan-audit-sppg/"
b3 = ("<h2>Kondisi Terbaru</h2>"
 "<p>Badan Gizi Nasional menghentikan sementara operasional 6.097 SPPG mulai 2 November 2026 karena Laporan Penggunaan Dana Harian (LPDH) belum diunggah ke SIPGN, merujuk Surat Edaran Kepala BGN Nomor 24 Tahun 2026. Dana operasional untuk unit tersebut ditahan sampai laporan diunggah dan diverifikasi. Pelajarannya jelas: pencatatan harian SPPG harus rapi sejak hari pertama.</p>"
 "<h2>Tiga Lapis Pelaporan</h2>"
 + tbl(["Lapis", "Siapa", "Yang Dibutuhkan"], [
   ("Harian", "SPPG", "LPDH: belanja bahan, operasional, dan bukti, diunggah ke SIPGN"),
   ("Bulanan", "SPPG dan mitra", "Rekonsiliasi dana masuk, belanja, dan sisa dana; rekap per menu dan porsi"),
   ("Tahunan", "Yayasan atau badan usaha mitra", "Laporan keuangan lengkap; untuk yayasan sesuai ISAK 335")])
 + "<h2>Kapan Mitra SPPG Wajib Diaudit</h2>"
 "<p>Pasal 52 UU Yayasan mewajibkan laporan keuangan yayasan diaudit akuntan publik bila yayasan memperoleh bantuan negara, bantuan luar negeri, atau pihak lain sebesar Rp500 juta atau lebih dalam satu tahun buku, atau memiliki kekayaan di luar wakaf Rp20 miliar atau lebih. Yayasan mitra yang mengelola dana program dalam setahun penuh sangat mungkin melewati ambang ini. Mitra berbentuk PT mengikuti kriteria Pasal 68 UU PT.</p>"
 "<h2>Yang Kami Kerjakan</h2>" + flow([
   ("Rapikan LPDH", "Format harian, bukti, dan alur persetujuan supaya unggahan SIPGN tidak tertunda."),
   ("Rekonsiliasi bulanan", "Dana masuk, belanja, dan saldo dicocokkan dengan rekening."),
   ("Laporan tahunan mitra", "Laporan keuangan yayasan (ISAK 335) atau PT (SAK EP)."),
   ("Audit", "Audit laporan keuangan yayasan atau PT mitra oleh KAP.")])
 + team("SPPG dan yayasan atau badan usaha mitra"))
F3 = [("Apakah yayasan mitra SPPG wajib diaudit?", "Bila yayasan menerima bantuan negara atau pihak lain Rp500 juta atau lebih dalam setahun, atau kekayaannya di luar wakaf Rp20 miliar atau lebih, laporan keuangannya wajib diaudit akuntan publik menurut Pasal 52 UU Yayasan."),
      ("Kenapa SPPG dibekukan BGN?", "Pemberitaan akhir Oktober 2026 menyebut 6.097 SPPG dihentikan sementara mulai 2 November 2026 karena LPDH belum diunggah ke SIPGN. Operasional dibuka kembali setelah laporan diunggah dan diverifikasi."),
      ("Apakah bisa membantu menyusun LPDH yang tertunda?", "Bisa. Bukti dan mutasi rekening disusun ulang per hari sesuai format, lalu direkonsiliasi agar siap diunggah.")]
SVC.append((P3, "Layanan · SPPG", "Laporan Keuangan dan Audit SPPG serta Yayasan Mitra MBG",
  "LPDH harian, rekonsiliasi bulanan, laporan keuangan tahunan yayasan atau PT mitra, sampai audit akuntan publik untuk Satuan Pelayanan Pemenuhan Gizi (SPPG) di seluruh Indonesia.",
  b3, F3, "Laporan Keuangan dan Audit SPPG, Yayasan Mitra MBG | FA Indonesia",
  "LPDH SIPGN, rekonsiliasi, laporan keuangan yayasan ISAK 335, dan audit KAP untuk SPPG dan mitra MBG. Diskusi awal gratis.",
  "Laporan Keuangan dan Audit SPPG", "Nutrition program financial reporting and audit", "Halo FA Indonesia, kami mitra/pengelola SPPG dan perlu bantuan laporan keuangan atau audit.", "SPPG"))

for (pth, eb, h1, lead, body, faq, title, desc, sn, st, wam, cr) in SVC:
    svc_page(pth, eb, h1, lead, body, faq, title, desc, sn, st, "/jasa-audit-laporan-keuangan/", "Jasa Audit", wam, cr)
URLS = [x[0] for x in SVC]

# ================= 2. KECAMATAN =================
KEC = KC.by_city(CITIES); CIDX = {c[0]: c for c in CITIES}; n = 0
for cname, rows in KEC.items():
    if cname not in CIDX or not rows: continue
    _, prov, reg, secs, cnote = CIDX[cname]; cs = KC.slug(cname)
    if not os.path.exists(P("wilayah", cs, "index.html")): continue
    hub = f"/wilayah/{cs}/kecamatan/"
    kabs = []
    for r in rows:
        if r["kab"] not in kabs: kabs.append(r["kab"])
    for r in rows:
        k, kab = r["kec"], r["kab"]; pth = f"{hub}{r['slug']}/"
        sibs = [x for x in rows if x["kab"] == kab and x["kec"] != k][:20]
        sline = "".join(f"<li>{E(SECTOR_LINES[s_])}</li>" for s_ in secs[:3] if s_ in SECTOR_LINES)
        desa = r["desa"]
        body = (f"<h2>Layanan untuk Usaha di Kecamatan {E(k)}</h2>"
          + tbl(["Kebutuhan", "Yang Kami Kerjakan"], [
            ("Audit laporan keuangan", f"Audit oleh KAP mitra untuk SABH, bank, atau investor; dokumen diperiksa daring, observasi lapangan dijadwalkan ke {k}"),
            ("Laporan keuangan dan pembukuan", "Disusun daring dari mutasi rekening dan bukti, sesuai SAK EMKM, SAK EP, atau PSAK"),
            ("Laporan tahunan PT", "Paket laporan tahunan untuk akta notaris dan SABH (Permenkum 49/2025)"),
            ("Kredit bank dan investor", "Analisis kapasitas kredit, paket pengajuan, dan valuasi usaha"),
            ("Koperasi, yayasan, SPPG", "Laporan keuangan KDMP, yayasan (ISAK 335), dan mitra SPPG")])
          + f"<h2>Karakter Usaha di Sekitar {E(k)}</h2><p>{E(k)} berada di {E(kab)}, wilayah {E(cname)} yang merupakan {E(cnote)}.</p><ul>{sline}</ul>"
          + (f"<h2>Desa dan Kelurahan di {E(k)}</h2><p class=\"t\">{' · '.join(E(d) for d in desa)}</p>" if desa else "")
          + team("perusahaan, CV, koperasi, dan yayasan")
          + f"<h2>Kecamatan Lain di {E(kab)}</h2><p class=\"t\"><a href=\"{hub}\">Semua kecamatan</a> · " + " · ".join(f'<a href="{hub}{x["slug"]}/">{E(x["kec"])}</a>' for x in sibs) + "</p>"
          + f"<p class=\"t\">Lihat juga <a href=\"/wilayah/{cs}/\">FA {E(cname)}</a>, <a href=\"/jasa-audit-laporan-keuangan/\">Jasa Audit Laporan Keuangan</a>, dan <a href=\"https://cariakuntan.com/kota/{cs}/kecamatan/{r['slug']}/\">Cari KAP {E(k)}</a>.</p>")
        faq = [(f"Apakah FA Indonesia melayani usaha di Kecamatan {k}?", f"Ya. Usaha di {k}, {kab} dilayani daring untuk pembukuan, laporan keuangan, dan persiapan audit, dengan kunjungan lapangan terjadwal bila diperlukan."),
               (f"Di mana mencari KAP untuk perusahaan di {k}?", f"Audit dapat dilaksanakan KAP DHN & Rekan, mitra FA yang terdaftar OJK, untuk perusahaan di {k}. Hubungi kami lewat WhatsApp untuk diskusi awal."),
               (f"Berapa biaya laporan keuangan atau audit di {k}?", "Bergantung pada skala usaha, kerapian bukti, dan tujuan laporan. Perkiraan biaya disampaikan setelah diskusi awal, sebelum Anda berkomitmen.")]
        svc_page(pth, f"Kecamatan · {E(kab)}", f"FA {k}: Jasa Audit, Laporan Keuangan, dan Kredit Usaha di Kecamatan {k}",
          f"Pendampingan untuk perusahaan, CV, koperasi, dan yayasan di Kecamatan {E(k)}, {E(kab)}: laporan keuangan, audit lewat KAP mitra, laporan tahunan PT, dan kredit bank. Dikerjakan daring, kunjungan lapangan terjadwal.",
          body, faq, f"Jasa Audit dan Laporan Keuangan di {k}, {kab} | FA Indonesia",
          f"Jasa audit, laporan keuangan, laporan tahunan PT, dan kredit usaha di Kecamatan {k}, {kab}. KAP DHN & Rekan, KJA Farhani. Diskusi awal gratis.",
          f"Jasa Audit dan Laporan Keuangan {k}", "Audit and accounting services", f"/wilayah/{cs}/", f"FA {cname}",
          f"Halo FA Indonesia, kami dari Kecamatan {k}, {kab} ingin konsultasi laporan keuangan/audit.", f"{cname} · {k}")
        URLS.append(pth); n += 1
    blocks = "".join(f"<h2>{E(kb)}</h2><p class=\"t\">" + " · ".join(f'<a href="{hub}{x["slug"]}/">{E(x["kec"])}</a>' for x in rows if x["kab"] == kb) + "</p>" for kb in kabs)
    svc_page(hub, "Wilayah · Kecamatan", f"FA {cname} per Kecamatan: {len(rows)} Kecamatan",
      f"Pilih kecamatan lokasi usaha Anda di {E(', '.join(kabs))} untuk layanan audit, laporan keuangan, dan kredit usaha.",
      blocks, [], f"Jasa Audit dan Laporan Keuangan per Kecamatan di {cname} | FA Indonesia",
      f"{len(rows)} kecamatan di {', '.join(kabs)}: jasa audit, laporan keuangan, laporan tahunan PT, dan kredit usaha.",
      f"FA {cname} per Kecamatan", "Audit and accounting services", f"/wilayah/{cs}/", f"FA {cname}", "Halo FA Indonesia, saya ingin konsultasi.", f"{cname} Kecamatan")
    URLS.append(hub)
    # tautan dari halaman kota
    cp = P("wilayah", cs, "index.html"); t = re.sub(r"<!--fa-kec-->.*?<!--/fa-kec-->", "", rd(cp), flags=re.S)
    top = " · ".join(f'<a href="{hub}{x["slug"]}/">{E(x["kec"])}</a>' for x in rows[:40])
    blk = f'<!--fa-kec--><h2>Layanan per Kecamatan di {E(cname)}</h2><p class="t"><a href="{hub}">Semua {len(rows)} kecamatan</a> · {top}</p><!--/fa-kec-->'
    i = t.find("<h2>Kota Sekitar</h2>")
    if i < 0: i = t.find("<h2>Pertanyaan Umum</h2>")
    if i > 0: wtxt(cp, t[:i] + blk + t[i:])

# /layanan/ blok
lp = P("layanan", "index.html")
t = re.sub(r"<!--fa-kec-svc-->.*?<!--/fa-kec-svc-->", "", rd(lp), flags=re.S)
blk = ('<!--fa-kec-svc--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Sektor Khusus</p><h2>Dana Kampanye, Koperasi Desa, dan SPPG</h2></div>'
       '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px">' + "".join(f'<a class="btn line" href="{u}">{l}</a>' for u, l in [(P1, "Audit Dana Kampanye"), (P2, "Koperasi Desa Merah Putih"), (P3, "Laporan dan Audit SPPG")]) + '</div></div></section><!--/fa-kec-svc-->')
i = t.find('<section class="block'); wtxt(lp, t[:i] + blk + t[i:])

# sitemap terpisah (supaya sitemap utama tidak membengkak) + llms
SM = "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in URLS)
wtxt(P("sitemap-kecamatan.xml"), '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + SM + "</urlset>\n")
rb = rd(P("robots.txt"))
if "sitemap-kecamatan.xml" not in rb: wtxt(P("robots.txt"), rb.rstrip("\n") + f"\nSitemap: {D}/sitemap-kecamatan.xml\n")
ll = rd(P("llms.txt"))
for u, l in [(P1, "Audit dan laporan dana kampanye (LADK, LPSDK, LPPDK)"), (P2, "Laporan keuangan dan audit Koperasi Desa Merah Putih (KDMP)"), (P3, "Laporan keuangan dan audit SPPG serta yayasan mitra MBG")]:
    line = f"- {l} → {D}{u}\n"; ll = ll.replace(line, "")
    ll = ll.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + line, 1)
wtxt(P("llms.txt"), ll)
print("fa_kec ok: layanan", len(SVC), "kecamatan", n)
