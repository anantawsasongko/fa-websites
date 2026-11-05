# -*- coding: utf-8 -*-
"""5 Nov 2026 (permintaan Bos): push SEO rumah sakit sampai daerah, dengan foto tim (Ananta + dr. Sigit Riyarto)
dan tautan ke liputan media dr. Sigit. Menonjolkan deliverables yang jelas dan tools buatan FA.
- /dr-sigit-riyarto/ profil + daftar liputan media (TIMES Indonesia, Radar Jogja/JawaPos, BacaMalang, Media Citra Indonesia).
- Pilar baru: /konsultan-akreditasi-rumah-sakit/, /konsultan-bpjs-rumah-sakit/, /direktur-rumah-sakit/, /menjual-rumah-sakit/
  masing-masing + /<pilar>/<kota>/ untuk semua kota /wilayah/ (113).
- Baris "Layanan Rumah Sakit di <kota>" di /wilayah/<kota>/, /konsultan-rumah-sakit/<kota>/, /konsultan-unit-cost-rumah-sakit/<kota>/.
- Sitemap, llms. Blok foto tim dipasang oleh fa_rs_tim_20261105.py (jalankan script ini SEBELUM fa_rs_tim).
Idempoten. Dasar regulasi: Permenkes 6/2026 tentang Rumah Sakit (kelas A-D dihapus, pimpinan boleh non-tenaga medis dengan kompetensi manajemen RS)."""
import os, re, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-05"')
exec(compile(_src, "fa_lead_helpers", "exec"))
URLS = []
SIG = "/dr-sigit-riyarto/"
MEDIA = [
 ("TIMES Indonesia", "17 November 2020", "Direksi Baru Persada Hospital: RS Harus Future Proof", "https://timesindonesia.co.id/peristiwa-daerah/310259/direksi-baru-persada-hospital-rs-harus-future-proof",
  "Dilantik sebagai Direktur Persada Hospital Malang. Menekankan rumah sakit harus siap menghadapi persaingan, termasuk dari rumah sakit asing, dan menjadikannya peluang."),
 ("BacaMalang", "1 April 2022", "Persada Hospital Malang Siap Kembangkan Medical Tourism di Malang", "https://bacamalang.com/persada-hospital-malang-siap-kembangkan-medical-tourism-di-malang/",
  "Mengembangkan layanan baru (bedah jantung, bariatrik, kosmetik) dan program medical tourism dengan sports medicine sebagai andalan."),
 ("BacaMalang", "12 Juni 2022", "Menparekraf Apresiasi Inovasi Medical Tourism Persada Hospital", "https://bacamalang.com/menparekraf-apresiasi-inovasi-medical-tourism-persada-hospital/",
  "Mengajak masyarakat berobat di dalam negeri dan menyebut Malang Medical Tourism dapat mendukung pendapatan daerah."),
 ("Radar Jogja (JawaPos)", "2 Juli 2025", "Rumah Sakit Queen Latifa Yogyakarta Resmi Sandang Tipe C, Pelayanan dan Peralatan Kesehatan Lebih Lengkap", "https://radarjogja.jawapos.com/jogja/656215977/rumah-sakit-queen-latifa-yogyakarta-resmi-sandang-tipe-c-pelayanan-dan-peralatan-kesehatan-lebih-lengkap",
  "Sebagai Direktur Utama memimpin peningkatan rumah sakit ke tipe C dan pembukaan unit hemodialisa, termasuk kesiapan melayani pasien BPJS Kesehatan."),
 ("Media Citra Indonesia", "3 Juli 2025", "RS Queen Latifa Sleman Resmi Naik Status Jadi Rumah Sakit Tipe C dan Luncurkan Unit Hemodialisa Modern", "https://mediacitraindonesia.com/rs-queen-latifa-sleman-resmi-naik-status-jadi-rumah-sakit-tipe-c-dan-luncurkan-unit-hemodialisa-modern/",
  "Menyebut peningkatan status sebagai tonggak layanan yang lebih inklusif, terutama bagi pasien gagal ginjal kronis."),
]
def media_list(n=5):
    return "<ul>" + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a>, <i>{o}</i>, {d}. {E(s)}</li>' for o, d, t, u, s in MEDIA[:n]) + "</ul>"
SIG_LINE = (f'<p><a href="{SIG}">dr. Sigit Riyarto, M.Kes, AAK</a> pernah memimpin Persada Hospital Malang dan RS Queen Latifa Yogyakarta, '
            f'termasuk membawa rumah sakit naik kelas dan membuka layanan baru. Liputannya antara lain di '
            f'<a href="{MEDIA[0][3]}" target="_blank" rel="noopener">TIMES Indonesia</a> dan <a href="{MEDIA[3][3]}" target="_blank" rel="noopener">Radar Jogja (JawaPos)</a>. '
            'Di FA Indonesia beliau memegang sisi medis, marketing, dan operasional, sementara sisi keuangan, M&amp;A, dan valuasi dipegang Ananta W. Sasongko, CPA.</p>')
TOOLS = ('<h2>Tools Buatan FA yang Dipakai</h2>' + tbl(["Tool", "Untuk Apa"], [
  ('<a href="/kalkulator-valuasi-rumah-sakit/">FA Venus · Valuasi Rumah Sakit</a>', "Harga RS before dan after pembenahan: EBITDA x multiple, aset, utang, porsi saham"),
  ('<a href="/kalkulator-valuasi-dcf/">FA Venus · Valuasi DCF</a>', "Proyeksi arus kas 5 tahun untuk investor dan bank"),
  ('<a href="/kalkulator-dscr/">FA Venus · Kalkulator DSCR</a>', "Kemampuan bayar kredit sebelum ekspansi atau take over"),
  ('<a href="/konsultan-unit-cost-rumah-sakit/">Model Unit Cost RS</a>', "Biaya per tindakan dan per kasus, dibanding tarif INA-CBG atau iDRG"),
  ('<a href="/audit-ready/">FA Jupiter</a>', "Laporan keuangan RS siap audit dan siap due diligence")])
  + "<p>Angka di setiap laporan bisa ditelusuri ke sumbernya, sehingga pemilik, bank, dan calon pembeli membaca hal yang sama.</p>")

PIL = {
 "konsultan-akreditasi-rumah-sakit": dict(
   short="Akreditasi Rumah Sakit", h1="Konsultan Akreditasi Rumah Sakit: Persiapan Survei, Mutu, dan Dampaknya ke Keuangan",
   lead="Pendampingan persiapan akreditasi untuk RS swasta: gap assessment standar, dokumen, telusur, sampai anggaran yang realistis. Kami tidak menjanjikan status; kami memastikan RS siap disurvei.",
   title="Konsultan Akreditasi Rumah Sakit: Persiapan Survei dan Mutu | FA Indonesia",
   desc="Konsultan akreditasi rumah sakit: gap assessment, dokumen regulasi, simulasi telusur, indikator mutu, dan anggaran persiapan. Deliverables jelas, tim dokter manajer dan CPA.",
   intro="<p>Akreditasi menentukan lebih dari sekadar sertifikat. Status ini ikut diperiksa saat kerja sama dengan BPJS Kesehatan, dibaca bank, dan menjadi bahan due diligence calon pembeli. Permenkes 6/2026 tentang Rumah Sakit juga menempatkan penyesuaian atau pencabutan status akreditasi sebagai salah satu sanksi administratif.</p>",
   dlv=[("Gap assessment per bab standar", "Laporan skor awal, temuan, dan prioritas", "Minggu 1-3"),
        ("Peta dokumen regulasi", "Daftar kebijakan, pedoman, SPO yang ada dan yang harus dibuat", "Minggu 3-4"),
        ("Rencana dan anggaran persiapan", "Timeline sampai survei, kebutuhan SDM, alat, renovasi, dan biayanya", "Minggu 4"),
        ("Simulasi telusur", "Uji telusur unit dan wawancara staf, plus daftar perbaikan", "Sebelum survei"),
        ("Dashboard indikator mutu", "Format bulanan indikator mutu dan keselamatan pasien", "Berjalan")],
   faq=[("Apakah FA Indonesia lembaga akreditasi?", "Bukan. Survei dan penetapan status dilakukan lembaga independen penyelenggara akreditasi. Kami mendampingi persiapan RS."),
        ("Berapa lama persiapan akreditasi?", "Bergantung hasil gap assessment. RS yang dokumennya sudah berjalan biasanya cukup beberapa bulan; RS yang mulai dari awal butuh lebih lama."),
        ("Kenapa konsultan akreditasi melibatkan akuntan?", "Karena persiapan akreditasi butuh anggaran: SDM, alat, dan renovasi. Kami hitung dampaknya ke arus kas dan ke nilai RS.")],
   wa="Halo FA Indonesia, saya ingin konsultasi persiapan akreditasi rumah sakit"),
 "konsultan-bpjs-rumah-sakit": dict(
   short="BPJS Rumah Sakit", h1="Konsultan BPJS Rumah Sakit: Klaim Pending, Tarif INA-CBG/iDRG, dan Arus Kas",
   lead="Untuk RS swasta yang klaim BPJS-nya sering pending, marginnya tipis, atau sedang menimbang kerja sama baru. Kami membaca data klaim Anda dan mengubahnya jadi keputusan.",
   title="Konsultan BPJS Rumah Sakit: Klaim Pending, Tarif, Arus Kas | FA Indonesia",
   desc="Konsultan BPJS untuk rumah sakit swasta: analisis klaim pending dan dispute, unit cost vs tarif INA-CBG/iDRG, piutang BPJS dan arus kas, kesiapan kerja sama. Deliverables jelas.",
   intro="<p>Bagi banyak RS swasta, pasien BPJS adalah mayoritas volume. Masalahnya jarang di jumlah pasien, tetapi di klaim yang tertahan, kasus yang biayanya melebihi tarif, dan piutang yang membuat kas seret. Persiapan perpindahan ke iDRG membuat analisis ini makin mendesak.</p>",
   dlv=[("Analisis klaim 12 bulan", "Klaim diajukan, dibayar, pending, dispute, per bulan dan per layanan", "Minggu 1-2"),
        ("Akar masalah klaim pending", "Penyebab per kategori (koding, berkas, administrasi) dan perbaikannya", "Minggu 2-3"),
        ("Margin per kasus", "Unit cost dibanding tarif INA-CBG/iDRG untuk kasus terbanyak", "Minggu 3-4"),
        ("Proyeksi arus kas", "Dampak percepatan klaim dan perbaikan margin ke kas 12 bulan", "Minggu 4"),
        ("Rencana tindak", "Daftar keputusan untuk direksi dan pemilik, lengkap dengan angka", "Minggu 4")],
   faq=[("Apakah RS harus terakreditasi untuk kerja sama BPJS?", "Akreditasi termasuk syarat yang diperiksa dalam kerja sama dengan BPJS Kesehatan, dan statusnya juga dibaca bank serta calon pembeli."),
        ("Kenapa klaim BPJS kami sering pending?", "Paling sering karena koding diagnosis dan tindakan, kelengkapan berkas, atau administrasi kepesertaan. Analisis data klaim menunjukkan mana yang dominan di RS Anda."),
        ("Apakah RS yang putus kerja sama BPJS masih bisa dijual?", "Bisa, dengan valuasi yang memperhitungkan risikonya. Baca artikel kami tentang RS putus kerja sama BPJS.")],
   wa="Halo FA Indonesia, saya ingin konsultasi BPJS untuk rumah sakit"),
 "direktur-rumah-sakit": dict(
   short="Direktur Rumah Sakit", h1="Direktur Rumah Sakit: Pendampingan Direksi, Direktur Interim, dan Rekrutmen",
   lead="Untuk pemilik RS yang butuh direktur yang tepat, direktur sementara selama transisi, atau pendampingan direksi agar kinerja RS naik dan laporannya bisa dibaca bank dan investor.",
   title="Direktur Rumah Sakit: Interim, Pendampingan, Rekrutmen | FA Indonesia",
   desc="Direktur rumah sakit: syarat menurut Permenkes 6/2026, direktur interim, pendampingan direksi, dan rekrutmen. Tim berpengalaman memimpin RS, deliverables bulanan yang jelas.",
   intro="<p>Permenkes 6/2026 tentang Rumah Sakit memberi ruang baru: unsur pimpinan dapat dijabat tenaga medis, tenaga kesehatan, atau tenaga profesional yang memiliki kompetensi manajemen rumah sakit. Pimpinan tertinggi harus WNI dan berpengalaman bekerja di rumah sakit, dan pemilik tidak boleh merangkap sebagai pimpinan. Memilih direktur kini soal kompetensi, bukan hanya gelar.</p>",
   dlv=[("Diagnosis 30 hari", "Kondisi layanan, SDM, keuangan, BPJS, dan akreditasi, dengan prioritas perbaikan", "Bulan 1"),
        ("KPI dan dashboard bulanan", "BOR, ALOS, pendapatan per layanan, margin, klaim BPJS, kas", "Bulan 1-2"),
        ("Rapat direksi dan laporan ke pemilik", "Notulen keputusan dan laporan bulanan satu halaman", "Bulanan"),
        ("Profil jabatan dan seleksi direktur", "Kriteria sesuai Permenkes 6/2026, shortlist, wawancara bersama pemilik", "Sesuai kebutuhan"),
        ("Serah terima ke direktur tetap", "Dokumen transisi dan target 6 bulan pertama", "Akhir penugasan")],
   faq=[("Apakah direktur rumah sakit harus dokter?", "Menurut Permenkes 6/2026, unsur pimpinan dapat dijabat tenaga medis, tenaga kesehatan, atau tenaga profesional yang memiliki kompetensi manajemen rumah sakit; pimpinan tertinggi wajib WNI dan berpengalaman di rumah sakit."),
        ("Apakah pemilik boleh menjadi direktur RS sendiri?", "Tidak. Ketentuan pelaksana UU Kesehatan melarang pemilik rumah sakit merangkap sebagai pimpinan."),
        ("Apa itu direktur interim?", "Direktur sementara selama masa transisi, misalnya direktur lama keluar, RS sedang dibenahi sebelum dijual, atau pemilik baru mengambil alih.")],
   wa="Halo FA Indonesia, saya ingin konsultasi soal direktur atau manajemen rumah sakit"),
 "menjual-rumah-sakit": dict(
   short="Menjual Rumah Sakit", h1="Menjual Rumah Sakit: Valuasi, Pembenahan, dan Mencari Pembeli yang Tepat",
   lead="Pendampingan sisi penjual untuk pemilik RS, RSIA, dan RS khusus: dari harga wajar, pembenahan sebelum dijual, materi pembeli, sampai negosiasi dan due diligence.",
   title="Menjual Rumah Sakit: Valuasi dan Pendampingan Penjual | FA Indonesia",
   desc="Jasa menjual rumah sakit: valuasi before dan after dengan FA Venus, pembenahan sebelum dijual, teaser dan information memorandum, data room, negosiasi. Deliverables jelas.",
   intro="<p>RS yang dijual dengan harga dari nilai gedung sering lama tidak laku, karena pembeli menghitung dari EBITDA, status BPJS, akreditasi, dan utang bank. Kami menyiapkan RS supaya dibaca pembeli dengan cara yang sama seperti penjual membacanya.</p>",
   dlv=[("Valuasi before dan after", "Laporan FA Venus Valuasi RS: harga apa adanya dan setelah pembenahan", "Minggu 1-2"),
        ("Rencana pembenahan", "Daftar perbaikan BPJS, unit cost, okupansi, audit, dan dampaknya ke harga", "Minggu 2-3"),
        ("Teaser dan information memorandum", "Materi anonim untuk calon pembeli, lalu IM setelah NDA", "Minggu 3-5"),
        ("Data room", "Struktur folder dan checklist dokumen due diligence", "Minggu 4-6"),
        ("Negosiasi dan due diligence", "Pendampingan sampai term sheet dan perjanjian jual beli", "Sampai closing")],
   faq=[("Berapa harga rumah sakit swasta?", "Pembeli umumnya menghitung dari EBITDA dikali multiple, dikoreksi status BPJS, akreditasi, BOR, dan utang. Coba hitung awal di kalkulator Valuasi Rumah Sakit FA Venus."),
        ("Apakah identitas RS dirahasiakan?", "Ya. Teaser dibuat anonim, identitas dibuka hanya ke calon pembeli yang sudah menandatangani NDA."),
        ("Bagaimana kalau RS masih punya utang bank?", "Bisa dijual. Utang diperhitungkan dalam harga saham dan dibahas strukturnya dengan bank dan pembeli.")],
   wa="Halo FA Indonesia, saya ingin konsultasi menjual rumah sakit"),
}

def _cut(s, n=158):
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0].rstrip(" ,;:") + "."
def dlv_tbl(rows): return "<h2>Deliverables yang Anda Terima</h2>" + tbl(["Deliverable", "Isi", "Waktu"], rows)
def sig_sec(n=2): return "<h2>Pengalaman Memimpin Rumah Sakit</h2>" + SIG_LINE + media_list(n)
RELATED = lambda s: "<p>Layanan rumah sakit lain: " + " · ".join(
    f'<a href="/{k}/{s}">{v["short"]}</a>' for k, v in PIL.items()) + f' · <a href="/konsultan-rumah-sakit/{s}">Konsultan Rumah Sakit</a> · <a href="/konsultan-unit-cost-rumah-sakit/{s}">Unit Cost</a></p>'

CITIES = []
for p in sorted(glob.glob(P("wilayah", "*", "index.html"))):
    slug = os.path.basename(os.path.dirname(p))
    m = re.search(r'"position": 3, "name": "([^"]+)", "item": "https://faindonesia\.co\.id/wilayah/' + re.escape(slug) + '/"', rd(p))
    if m: CITIES.append((slug, m.group(1)))

for k, v in PIL.items():
    base = f"/{k}/"
    lst = " · ".join(f'<a href="{base}{s}/">{E(c)}</a>' for s, c in CITIES)
    body = (v["intro"] + dlv_tbl(v["dlv"]) + TOOLS + sig_sec(5) +
            f'<h2>Per Kota</h2><details class="fold"><summary>Semua Kota ({len(CITIES)})</summary><p class="t">{lst}</p></details>' + RELATED(""))
    svc_page(base, f"Layanan · {v['short']}", v["h1"], v["lead"], body, v["faq"], v["title"], v["desc"],
             v["short"], "Hospital consulting", "/konsultan-rumah-sakit/", "Konsultan Rumah Sakit", v["wa"] + ".", v["short"])
    URLS.append(base)
    for s, c in CITIES:
        b = (f"<p>Untuk rumah sakit, RSIA, dan klinik utama di {E(c)} dan kabupaten sekitarnya. Pekerjaan dilakukan daring dengan kunjungan lapangan bila diperlukan.</p>"
             + v["intro"] + dlv_tbl(v["dlv"]) + TOOLS + sig_sec(2) + RELATED(f"{s}/"))
        svc_page(f"{base}{s}/", f"{v['short']} · {c}", f"{v['short']} {c}: " + v["h1"].split(": ", 1)[1],
                 v["lead"], b, v["faq"], v["title"].replace(" | FA Indonesia", "").split(":")[0] + f" {c}: " + v["title"].split(": ", 1)[1],
                 _cut(v["desc"].split(":")[0] + f" di {c}:" + v["desc"].split(":", 1)[1]),
                 f"{v['short']} {c}", "Hospital consulting", base, "Semua Kota", f"{v['wa']} di {c}.", f"{v['short']} {c}")
        URLS.append(f"{base}{s}/")

# ---------- profil dr. Sigit ----------
sb = ('<p>dr. Sigit Riyarto, M.Kes, AAK adalah dokter dan manajer rumah sakit. Ia pernah menjabat Direktur Persada Hospital Malang dan Direktur Utama RS Queen Latifa Yogyakarta, '
      'dengan pengalaman mengembangkan layanan baru, medical tourism, peningkatan kelas rumah sakit, dan unit hemodialisa.</p>'
      '<p>Di tim konsultan rumah sakit FA Indonesia, dr. Sigit memegang sisi medis, marketing, dan operasional: akreditasi, layanan unggulan, cost cutting, dan manajemen. '
      'Sisi keuangan, valuasi, M&amp;A, dan seller side dipegang <a href="/ananta-w-sasongko/">Ananta W. Sasongko, CPA</a>.</p>'
      '<h2>Di Media</h2>' + media_list(5) +
      '<h2>Bidang yang Ditangani</h2><ul>'
      + "".join(f'<li><a href="/{k}/">{v["short"]}</a></li>' for k, v in PIL.items())
      + '<li><a href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a></li><li><a href="/konsultan-unit-cost-rumah-sakit/">Unit Cost Rumah Sakit</a></li></ul>')
SFAQ = [("Apa latar belakang dr. Sigit Riyarto?", "Dokter dan manajer rumah sakit, pernah menjabat Direktur Persada Hospital Malang dan Direktur Utama RS Queen Latifa Yogyakarta."),
        ("Bagaimana menghubungi dr. Sigit?", "Lewat tombol WhatsApp Tim Rumah Sakit FA Indonesia di halaman ini.")]
svc_page(SIG, "Tim Konsultan Rumah Sakit", "dr. Sigit Riyarto, M.Kes, AAK", "Konsultan operasional rumah sakit: medis, marketing, dan manajemen. Mantan direktur Persada Hospital Malang dan RS Queen Latifa Yogyakarta.",
         sb, SFAQ, "dr. Sigit Riyarto, M.Kes, AAK: Konsultan dan Mantan Direktur Rumah Sakit | FA Indonesia",
         "Profil dr. Sigit Riyarto, M.Kes, AAK, mantan Direktur Persada Hospital Malang dan Dirut RS Queen Latifa Yogyakarta, tim konsultan rumah sakit FA Indonesia.",
         "Konsultan Operasional Rumah Sakit", "Hospital management consulting", "/konsultan-rumah-sakit/", "Konsultan Rumah Sakit",
         "Halo FA Indonesia, saya ingin konsultasi rumah sakit dengan dr. Sigit.", "dr. Sigit Riyarto")
sp = P("dr-sigit-riyarto", "index.html"); t = rd(sp)
person = {"@context": "https://schema.org", "@type": "Person", "name": "dr. Sigit Riyarto, M.Kes, AAK", "jobTitle": "Konsultan Operasional Rumah Sakit",
          "image": D + "/img/dr-sigit-riyarto-mkes-aak.jpg", "url": D + SIG, "worksFor": {"@type": "Organization", "name": "FA Indonesia", "url": D + "/"},
          "subjectOf": [{"@type": "NewsArticle", "headline": tt, "url": u, "publisher": {"@type": "Organization", "name": o}} for o, d, tt, u, s in MEDIA]}
t = re.sub(r'<script type="application/ld\+json" id="sig-person">.*?</script>', "", t, flags=re.S)
t = t.replace("</head>", f'<script type="application/ld+json" id="sig-person">{json.dumps(person, ensure_ascii=False)}</script></head>', 1)
k = t.find("<p>dr. Sigit Riyarto, M.Kes, AAK adalah")
if k > 0 and "sig-foto" not in t:
    t = t[:k] + '<img class="sig-foto" src="/img/dr-sigit-riyarto-mkes-aak.jpg" alt="dr. Sigit Riyarto, M.Kes, AAK" width="700" height="875" style="width:min(280px,70%);height:auto;border-radius:12px;margin:8px 0 18px">' + t[k:]
wtxt(sp, t); URLS.append(SIG)

# ---------- baris layanan RS di halaman kota yang sudah ada ----------
nl = 0
for s, c in CITIES:
    row = (f'<!--fa-rsd--><p class="t">Layanan rumah sakit di {E(c)}: ' + " · ".join(f'<a href="/{k}/{s}/">{v["short"]}</a>' for k, v in PIL.items())
           + f' · <a href="/konsultan-rumah-sakit/{s}/">Konsultan Rumah Sakit</a> · <a href="/konsultan-unit-cost-rumah-sakit/{s}/">Unit Cost</a></p><!--/fa-rsd-->')
    for rel in (("wilayah", s), ("konsultan-rumah-sakit", s), ("konsultan-unit-cost-rumah-sakit", s)):
        p = P(*rel, "index.html")
        if not os.path.exists(p): continue
        t = re.sub(r"<!--fa-rsd-->.*?<!--/fa-rsd-->", "", rd(p), flags=re.S)
        k = t.find("<!--/fa-forensik-w-->")
        k = k + len("<!--/fa-forensik-w-->") if k > 0 else t.find("<h2>Pertanyaan Umum</h2>")
        if k < 0: continue
        wtxt(p, t[:k] + row + t[k:]); nl += 1
for base in ("konsultan-rumah-sakit", "konsultan-unit-cost-rumah-sakit"):
    p = P(base, "index.html"); t = re.sub(r"<!--fa-rsd-->.*?<!--/fa-rsd-->", "", rd(p), flags=re.S)
    row = ('<!--fa-rsd--><p class="t">Layanan rumah sakit lain: ' + " · ".join(f'<a href="/{k}/">{v["short"]}</a>' for k, v in PIL.items())
           + f' · <a href="{SIG}">Profil dr. Sigit Riyarto</a></p><!--/fa-rsd-->')
    k = t.find("<h2>Pertanyaan Umum</h2>")
    if k > 0: wtxt(p, t[:k] + row + t[k:]); nl += 1

sm = re.sub(r"<!--fa-rsd-->.*?<!--/fa-rsd-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-rsd-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'0.9' if u.count('/') == 2 else '0.6'}</priority></url>\n" for u in URLS) + "<!--/fa-rsd-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
lines = "".join(f"- {v['short']}: {_cut(v['desc'], 125)} → https://faindonesia.co.id/{k}/\n" for k, v in PIL.items()) + "- dr. Sigit Riyarto, M.Kes, AAK (tim RS FA, mantan Direktur Persada Hospital Malang dan Dirut RS Queen Latifa Yogyakarta) → https://faindonesia.co.id/dr-sigit-riyarto/\n"
ll = rd(P("llms.txt"))
for x in lines.splitlines(True): ll = ll.replace(x, "")
ll = ll.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + lines, 1) if "\n## Layanan Spesifik\n" in ll else ll.rstrip("\n") + "\n" + lines
wtxt(P("llms.txt"), ll)
print("fa_rs_daerah ok", len(URLS), "url, baris kota", nl)
