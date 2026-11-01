# -*- coding: utf-8 -*-
# Halaman /magang/ (1 Nov 2026): program magang akuntansi remote 6 bulan (KJA Farhani x FA Indonesia).
# Di-exec dari build.py, memakai head(), header(), footer(), write(), urls, ID, DOMAIN, tc, ldtag.

MG_SUBJ = "Magang – Nama – Kampus"
MG_BODY = ("Nama:\nKampus dan Prodi:\nSemester dan IPK:\nKota domisili:\n"
           "Jalur kontribusi yang dipilih (Riset dan Review / Data dan Analisis / Jejaring Usaha / Perangkat Kerja):\n"
           "Magang wajib kampus (MBKM/konversi SKS) atau mandiri:\n"
           "Tanggal mulai dan selesai:\n"
           "Dokumen yang diminta kampus (surat penerimaan, logbook, form penilaian, MoU, dll.):\n\n"
           "Terlampir CV, transkrip nilai, dan proposal kontribusi 1 halaman.")
MG_MAIL = mailto(MG_SUBJ, MG_BODY)

MG_TASKS = [
    ("Bulan 1–2", "Penyusunan Laporan Keuangan", "Jurnal, buku besar, neraca saldo, LK lengkap dan CALK dari data transaksi perusahaan yang kami berikan."),
    ("Bulan 3", "Perpajakan", "Rekonsiliasi fiskal, PPh Badan terutang, dan pajak tangguhan (PSAK 212)."),
    ("Bulan 4", "Konversi PSAK 118", "Konversi laba rugi satu emiten BEI ke format PSAK 118, plus memo dampak penyajian."),
    ("Bulan 5", "Kertas Kerja Audit", "Materialitas, walkthrough siklus pendapatan, uji substantif piutang dan persediaan, daftar temuan di FA Saturn."),
    ("Bulan 6", "Technical Paper", "Satu studi kasus PSAK (fakta, analisis, jurnal, kalimat CALK) dan presentasi hasil magang."),
]
MG_FLOW = [("01", "Kirim Lamaran", "CV, Transkrip, Proposal"), ("02", "Seleksi Proposal", "Kami Kabari via Email"),
           ("03", "Surat Penerimaan", "Untuk Kampus"), ("04", "Penugasan Bulanan", "Remote, Review Berkala"),
           ("05", "Surat Keterangan", "Setelah Semua Selesai")]
MG_TRACK = [
    ("Riset dan Review", "Menelaah standar, regulasi, atau perangkat kerja kami, lalu menulis ringkasan dan usulan perbaikan yang siap dipakai."),
    ("Data dan Analisis", "Mengolah data keuangan publik atau data yang Anda miliki dari riset kampus menjadi benchmark dan analisis rasio."),
    ("Jejaring Usaha", "Mendampingi UMKM, koperasi, BUMDes, atau yayasan di daerah Anda yang ingin merapikan laporan keuangannya, bersama tim kami."),
    ("Perangkat Kerja", "Mengembangkan template Excel, checklist, atau ide fitur untuk aplikasi FA dan UpdateSAK."),
]
MG_FAQ = [
    ("Apa itu proposal kontribusi?", "Satu halaman berisi jalur kontribusi yang Anda pilih, apa yang ingin Anda kerjakan selama magang, dan hasil awal yang bisa Anda tunjukkan, misalnya review singkat atas salah satu artikel atau perangkat kerja kami beserta usulan perbaikannya. Lamaran tanpa proposal belum dapat kami proses."),
    ("Apakah ada pelatihan dari dasar?", "Program ini dirancang untuk mahasiswa yang sudah menguasai akuntansi keuangan dan perpajakan dasar dan terbiasa belajar mandiri. Materi rujukan tersedia di updatesak.com; pendampingan kami berupa review atas hasil kerja, bukan kelas."),
    ("Saya punya kenalan UMKM atau organisasi yang butuh pembenahan laporan keuangan. Apakah relevan?", "Sangat relevan. Usaha atau organisasi tersebut bisa menjadi proyek magang Anda di jalur Jejaring Usaha, dengan pendampingan dan review dari tim kami."),
    ("Apakah bisa untuk MBKM atau konversi SKS?", "Bisa. Kirim format dokumen dari kampus (surat penerimaan, logbook, form penilaian, MoU) bersama lamaran, nanti kami isi sesuai kegiatan dan periode yang sebenarnya."),
    ("Kalau kampus hanya mewajibkan 5 bulan?", "Penugasan bisa dipadatkan menyesuaikan tanggal mulai dan selesai dari kampus. Tulis periodenya di email lamaran."),
    ("Apakah harus datang ke kantor?", "Tidak. Seluruh program berjalan remote dari kota Anda. Komunikasi lewat email dan grup kerja, dengan logbook mingguan dan review hasil setiap dua minggu."),
    ("Apakah ada gaji atau uang saku?", "Tidak. Program ini tidak berbayar. Kompensasinya hanya surat keterangan magang dari KJA Farhani."),
    ("Siapa yang menerbitkan surat penerimaan dan surat keterangan?", "KJA Farhani. Surat keterangan hanya diterbitkan untuk peserta yang menyelesaikan seluruh penugasan dengan baik, sesuai kegiatan dan periode pengerjaan."),
    ("Boleh memakai AI untuk mengerjakan tugas?", "Boleh sebagai alat bantu, tetapi hasil akhir harus pekerjaan sendiri. Hasil copy-paste atau mentah dari AI langsung gugur."),
    ("Bagaimana jika periode magang saya baru mulai tahun depan?", "Tetap kirim lamaran sekarang dan tulis tanggal mulai yang direncanakan. Kami catat untuk batch sesuai periode tersebut."),
]

MG_CSS = """<style id="mg-css">
.mg-hero{padding-block:56px 40px;border-top:0}
.mg-hero h1{font-size:clamp(2rem,5.2vw,3.2rem);font-weight:500;line-height:1.08;margin-top:14px;animation:up .7s ease both}
.mg-hero .sub{font-size:1.08rem;color:var(--muted);margin-top:16px;max-width:52ch;animation:up .7s .1s ease both}
.mg-pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px;animation:up .7s .2s ease both}
.mg-pills span{border:1px solid var(--line);padding:6px 12px;font-size:.84rem;font-weight:600;color:var(--ink);background:var(--panel)}
.mg-pills span.off{color:#B4232C;border-color:#F1C6C9;background:#FDF2F2}
.mg-cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px;animation:up .7s .3s ease both}
.mg-cta .btn-o{background:transparent;color:var(--ink);border:1px solid var(--ink)}
.mg-flow{display:grid;grid-template-columns:repeat(5,1fr);border-top:1px solid var(--line);border-left:1px solid var(--line)}
.mg-flow div{padding:18px 16px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);display:grid;gap:4px;position:relative;animation:up .5s ease both;animation-delay:calc(var(--i)*90ms);min-width:0}
.mg-flow small{font-family:var(--display);font-size:1.3rem;color:var(--accent)}
.mg-flow b{font-family:var(--display);font-weight:600;font-size:1.04rem;line-height:1.25}
.mg-flow span{font-size:.84rem;color:var(--muted)}
.mg-flow div:not(:last-child)::after{content:"→";position:absolute;right:10px;top:16px;color:var(--accent);animation:nudge 1.6s ease-in-out infinite}
@media (max-width:860px){.mg-flow{grid-template-columns:1fr}.mg-flow div{grid-template-columns:44px 1fr;column-gap:10px;align-items:baseline}.mg-flow div b,.mg-flow div span{grid-column:2}.mg-flow small{grid-row:1/3}.mg-flow div:not(:last-child)::after{content:"↓";right:16px;top:auto;bottom:10px}}
.mg-tl{display:grid;gap:0;border-top:1px solid var(--line)}
.mg-tl>div{display:grid;grid-template-columns:130px 1fr;gap:18px;padding:16px 0;border-bottom:1px solid var(--line);animation:up .5s ease both;animation-delay:calc(var(--i)*80ms)}
.mg-tl em{font-style:normal;font-size:.78rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);padding-top:3px}
.mg-tl b{display:block;font-family:var(--display);font-weight:600;font-size:1.1rem}
.mg-tl p{color:var(--muted);font-size:.94rem;margin-top:2px}
.mg-tl .bar-p{height:4px;background:var(--line);margin-top:10px;position:relative;overflow:hidden}
.mg-tl .bar-p i{position:absolute;inset:0 auto 0 0;background:var(--accent);width:var(--w);transform-origin:left;animation:grow 1s ease both;animation-delay:calc(var(--i)*120ms + .2s)}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@media (max-width:640px){.mg-tl>div{grid-template-columns:1fr;gap:4px}}
.mg-two{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.mg-box{border-top:3px solid var(--ink);padding-top:14px}
.mg-box h3{font-size:1.15rem}
.mg-trkg{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:22px}.mg-trk{color:var(--muted);font-size:.95rem;margin-top:8px}
.mg-box ul{margin:10px 0 0;padding-left:18px;color:var(--muted);font-size:.95rem;display:grid;gap:6px}
.mg-box.warn{border-top-color:#B4232C}
.mg-mail{margin-top:14px;font-size:.88rem;color:var(--muted)}
.mg-mail code{font-family:var(--body);background:var(--panel);padding:2px 6px;color:var(--ink)}
@media (max-width:760px){.mg-two{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){.mg-flow div,.mg-tl>div,.mg-tl .bar-p i,.mg-hero h1,.mg-hero .sub,.mg-pills,.mg-cta{animation:none}.mg-flow div::after{animation:none}}
</style>"""

_flow = "".join(f'<div style="--i:{i}"><small>{n}</small><b>{tc(t)}</b><span>{s}</span></div>' for i, (n, t, s) in enumerate(MG_FLOW))
_tl = "".join(
    f'<div style="--i:{i}"><em>{m}</em><div><b>{tc(t)}</b><p>{d}</p><div class="bar-p"><i style="--w:{w}%"></i></div></div></div>'
    for i, ((m, t, d), w) in enumerate(zip(MG_TASKS, [33, 50, 67, 83, 100])))
_trk = "".join(f'<div class="mg-box"><h3>{tc(t)}</h3><p class="mg-trk">{d}</p></div>' for t, d in MG_TRACK)
_faq = "".join(f"<details><summary>{tc(q)}</summary><p>{a}</p></details>" for q, a in MG_FAQ)
_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in MG_FAQ]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Beranda", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Magang", "item": DOMAIN + "/magang/"}]}]}

url = DOMAIN + "/magang/"
html = head("Program Magang Akuntansi Remote 6 Bulan (MBKM) | cariakuntan.com",
            "Magang akuntansi remote 6 bulan untuk mahasiswa yang mandiri dan siap berkontribusi: riset dan review standar, analisis data, jejaring usaha, atau perangkat kerja. Seleksi berdasarkan proposal kontribusi. Bisa untuk MBKM.",
            url, extra=MG_CSS + ldtag(_ld))
html += header(ID, "mag") + f'''<main>
<section class="mg-hero"><div class="wrap">
  <p class="label">Program Magang</p>
  <h1>Magang Akuntansi Remote 6 Bulan</h1>
  <p class="sub">Untuk mahasiswa yang terbiasa belajar mandiri dan ingin hasil kerjanya benar-benar dipakai. Bekerja dari kota Anda dengan perangkat kerja FA Indonesia dan KJA Farhani, dari laporan keuangan sampai kertas kerja audit.</p>
  <div class="mg-pills"><span>Remote Penuh</span><span>5–6 Bulan</span><span>Bisa MBKM / Konversi SKS</span><span>Seleksi Berdasarkan Proposal Kontribusi</span><span class="off">Tidak Berbayar</span></div>
  <div class="mg-cta"><a class="btn btn-wa" href="{MG_MAIL}">Kirim Lamaran via Email</a><a class="btn btn-o" href="#penugasan">Lihat Penugasan</a></div>
</div></section>
<section id="alur"><div class="wrap">
  <div class="head"><p class="label">Alur</p><h2>Alur Pendaftaran</h2></div>
  <div class="mg-flow">{_flow}</div>
</div></section>
<section id="kontribusi"><div class="wrap">
  <div class="head"><p class="label">Kontribusi</p><h2>Pilih Satu Jalur Kontribusi</h2><p>Setiap peserta datang dengan satu fokus kontribusi: ide, data, atau jejaring. Jalur yang Anda pilih menjadi dasar seleksi dan proyek utama selama magang.</p></div>
  <div class="mg-trkg">{_trk}</div>
</div></section>
<section id="penugasan"><div class="wrap">
  <div class="head"><p class="label">Penugasan</p><h2>Lima Penugasan Inti, Semuanya Wajib</h2><p>Dikerjakan mandiri dengan rujukan materi di updatesak.com, berjalan bersama proyek kontribusi Anda. Output berupa file kerja Excel/Word dan logbook mingguan; tim kami memberi review atas hasilnya.</p></div>
  <div class="mg-tl">{_tl}</div>
  <p class="note">Perangkat kerja: <a href="https://faindonesia.co.id/apps/" target="_blank" rel="noopener">faindonesia.co.id/apps</a> (penyusunan LK, konversi PSAK 118, FA Saturn) dan materi teknis <a href="https://updatesak.com/" target="_blank" rel="noopener">updatesak.com</a>.</p>
</div></section>
<section id="daftar"><div class="wrap">
  <div class="mg-two">
    <div class="mg-box"><h3>Yang Perlu Dikirim</h3><ul>
      <li>CV dan Transkrip Nilai</li>
      <li>Proposal Kontribusi 1 Halaman: Jalur, Rencana Kerja, dan Hasil Awal</li>
      <li>Data atau Jejaring yang Bisa Anda Akses, Jika Ada</li>
      <li>Status Magang: Wajib Kampus (MBKM, Konversi SKS) atau Mandiri</li>
      <li>Tanggal Mulai dan Selesai</li>
      <li>Format Dokumen dari Kampus: Surat Penerimaan, Logbook, Form Penilaian, MoU</li>
    </ul>
    <p class="mg-mail">Subjek email: <code>{MG_SUBJ}</code></p>
    <div class="mg-cta"><a class="btn btn-wa" href="{MG_MAIL}">Kirim Lamaran via Email</a></div></div>
    <div class="mg-box warn"><h3>Ketentuan</h3><ul>
      <li>Seleksi Berdasarkan Proposal Kontribusi; Lamaran Tanpa Proposal Belum Dapat Diproses</li>
      <li>Peserta Diharapkan Sudah Menguasai Akuntansi Keuangan dan Perpajakan Dasar</li>
      <li>Pendampingan Berupa Review Hasil Kerja, Bukan Kelas atau Bimbingan Harian</li>
      <li>Tidak Berbayar, Tanpa Gaji atau Uang Saku</li>
      <li>Kompensasi Hanya Surat Keterangan Magang dari KJA Farhani</li>
      <li>Surat Keterangan Hanya untuk Peserta yang Menyelesaikan Seluruh Penugasan dengan Baik</li>
      <li>Hasil Copy-Paste atau Mentah dari AI Langsung Gugur</li>
    </ul></div>
  </div>
</div></section>
<section id="tanya"><div class="wrap">
  <div class="head"><p class="label">Tanya Jawab</p><h2>Pertanyaan yang Sering Masuk</h2></div>
  {_faq}
</div></section>
</main>
''' + footer(ID)
# tombol bawah (mobile): lamaran via email, bukan chat WA
html = re.sub(r'<div class="bar"><a class="btn btn-wa" href="[^"]*"[^>]*>Chat Ananta, CPA</a></div>',
              f'<div class="bar"><a class="btn btn-wa" href="{MG_MAIL}">Kirim Lamaran via Email</a></div>', html, count=1)
write("/magang/", html); urls.append("/magang/")
