# Halaman /jadwal-ujian/ UpdateSAK: jadwal ujian sertifikasi CPA (IAPI), CA (IAI), CPMA (IAMI), dan Konsultan Pajak (BKP/USKP).
# Dijalankan prep.py SETELAH build_seo.py dan build_materi.py (menambah sitemap, llms.txt, tab nav, blok beranda).
# Data diperbarui manual dari sumber resmi; ubah UPD dan isi EX saat ada pengumuman baru.
import os, re, sys, json, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_seo as B
esc = html.escape
SITE = B.SITE; BASE = B.BASE
UPD_ISO = "2026-10-28"; UPD = "28 Oktober 2026"
URL = f"{BASE}/jadwal-ujian/"
KEY = "jadwal-ujian"

EX = [
 dict(id="cpa", kode="CPA", nama="Certified Public Accountant", org="IAPI", warna="#1F5BFF",
      ringkas="Ujian Profesi Akuntan Publik (UPAP), syarat menjadi Akuntan Publik yang menandatangani laporan audit.",
      next="Periode IV: November sampai Desember 2026", status="Dibuka",
      rows=[("Periode I", "Februari sampai Maret 2026", "Selesai"), ("Periode II", "Mei sampai Juni 2026", "Selesai"),
            ("Periode III", "Agustus sampai September 2026", "Selesai"), ("Periode IV", "November sampai Desember 2026", "Berikutnya")],
      info=[("Jenjang", "Tingkat Dasar dan Tingkat Profesional, lalu Penilaian Pengalaman Audit (AAEP, wawancara paper praktik audit, telaah KKP)"),
            ("Biaya Tingkat Dasar", "Pendaftaran Rp125.000, per mata uji Rp250.000"),
            ("Biaya Tingkat Profesional", "Pendaftaran Rp350.000, per mata uji Rp725.000, mata uji AAEP Rp2.150.000"),
            ("Lokasi", "Test Center mitra IAPI"),
            ("Jalur Workshop", "RPL ACPA Periode IV: 7 sampai 11 Desember 2026")],
      src=("Kalender UPAP Tahun 2026, IAPI", "https://iapi.or.id/kalender-upap-tahun-2026/")),
 dict(id="ca", kode="CA", nama="Chartered Accountant", org="IAI", warna="#12A39A",
      ringkas="Sertifikasi akuntan profesional Ikatan Akuntan Indonesia untuk akuntan di perusahaan, sektor publik, dan praktik.",
      next="Mulai 29 Oktober 2026, berlanjut sampai 18 Desember 2026", status="Berjalan",
      rows=[("29 Okt 2026", "PROF Manajemen Keuangan Lanjutan", "09.00"), ("30 Okt 2026", "PROF Akuntansi Manajemen Lanjutan", "08.00"),
            ("3 Nov 2026", "ADV Pelaporan Korporat · PROF Audit & Asurans", "09.00 · 14.00"),
            ("4 Nov 2026", "PROF Manajemen Keuangan Lanjutan · ADV Manajemen Strategik & Kepemimpinan", "09.00 · 14.00"),
            ("5 Nov 2026", "PROF Sistem Informasi & Pengendalian Internal · PROF Manajemen Perpajakan", "09.00 · 14.00"),
            ("6 Nov 2026", "PROF Akuntansi Manajemen Lanjutan", "08.00"), ("13 Nov 2026", "PROF Manajemen Keuangan Lanjutan", "08.00"),
            ("16 Nov 2026", "PROF Manajemen Perpajakan", "09.00"),
            ("17 Nov 2026", "ADV Pelaporan Korporat · PROF Audit & Asurans", "09.00 · 14.00"),
            ("18 Nov 2026", "PROF Manajemen Keuangan Lanjutan · ADV Manajemen Strategik & Kepemimpinan", "09.00 · 14.00"),
            ("19 Nov 2026", "PROF Sistem Informasi & Pengendalian Internal · PROF Manajemen Perpajakan", "09.00 · 14.00"),
            ("20 Nov 2026", "PROF Akuntansi Manajemen Lanjutan", "08.00"),
            ("23 Nov 2026", "PROF Sistem Informasi & Pengendalian Internal", "09.00"),
            ("24 Nov 2026", "PROF Sistem Informasi & Pengendalian Internal · PROF Manajemen Perpajakan", "09.00"),
            ("26 Nov 2026", "PROF Audit & Asurans", "09.00"), ("27 Nov 2026", "PROF Sistem Informasi & Pengendalian Internal", "08.00"),
            ("15 Des 2026", "ADV Pelaporan Korporat · PROF Audit & Asurans", "09.00 · 14.00"),
            ("16 Des 2026", "PROF Manajemen Keuangan Lanjutan · ADV Manajemen Strategik & Kepemimpinan", "09.00 · 14.00"),
            ("17 Des 2026", "PROF Sistem Informasi & Pengendalian Internal · PROF Manajemen Perpajakan", "09.00 · 14.00"),
            ("18 Des 2026", "PROF Akuntansi Manajemen Lanjutan", "08.00")],
      info=[("Jenjang", "Tingkat Profesional (PROF) dan Tingkat Lanjutan (ADV); jenjang dasar lewat CAFB"),
            ("Syarat Umum", "Anggota IAI dengan pendidikan akuntansi minimal D-IV/S-1, peserta PPAk, atau setara KKNI level 6"),
            ("Pendaftaran", "Lewat IAI Lounge, pilih tanggal dan mata ujian yang tersedia"),
            ("Catatan", "Satu mata ujian bisa punya beberapa pilihan tanggal; cukup ambil salah satu")],
      src=("Jadwal Sertifikasi Ujian CA, IAI", "https://web.iaiglobal.or.id/Sertifikasi/jadwal_sertifikasi/4")),
 dict(id="cpma", kode="CPMA", nama="Certified Professional Management Accountant", org="IAMI", warna="#F59E0B",
      ringkas="Sertifikasi akuntan manajemen dari Ikatan Akuntan Manajemen Indonesia untuk controller, FP&A, dan manajer keuangan.",
      next="Periode November 2026, tanggal pasti mengikuti pengumuman IAMI", status="Cek IAMI",
      rows=[("Periode Mei", "Ujian reguler semester pertama", "Pola tahunan"), ("Periode November", "Ujian reguler semester kedua", "Pola tahunan"),
            ("Ujian Khusus", "Bisa dibuka untuk kelompok atau asosiasi bila kuota minimal terpenuhi", "Sesuai kesepakatan")],
      info=[("Frekuensi", "Dua kali setahun, Mei dan November"),
            ("Syarat Umum", "Anggota IAMI, atau S-1/D-IV akuntansi atau S-1 nonakuntansi dengan pengalaman 3 tahun di akuntansi atau keuangan"),
            ("Fast Track", "Pemegang CA yang memenuhi syarat pengalaman cukup menempuh dua mata ujian ditambah penyetaraan IAMI"),
            ("Catatan", "Halaman jadwal IAMI memakai verifikasi robot; konfirmasi tanggal langsung ke IAMI sebelum mendaftar")],
      src=("Ujian CPMA, IAMI", "https://www.iamiglobal.or.id/page/sertifikasi-cpma.html")),
 dict(id="bkp", kode="BKP", nama="Konsultan Pajak Bersertifikat (USKP dan Uji Kompetensi Perpajakan)", org="BPPK Kemenkeu", warna="#7C3AED",
      ringkas="Sertifikasi konsultan pajak tingkat A, B, dan C sebagai syarat izin praktik konsultan pajak.",
      next="Uji Kompetensi Perpajakan skema baru: pertengahan Oktober sampai Desember 2026", status="Skema Baru",
      rows=[("USKP Periode I", "14 sampai 16 April 2026 (peserta mengulang)", "Selesai"),
            ("USKP Periode II", "11 sampai 13 Agustus 2026 (peserta mengulang)", "Selesai"),
            ("USKP Periode III", "14 sampai 15 Oktober 2026, daring, tingkat A dan B (periode mengulang terakhir skema transisi)", "Selesai"),
            ("Uji Kompetensi Perpajakan", "Pertengahan Oktober sampai Desember 2026, skema baru", "Berjalan"),
            ("Tahun 2027", "BPPK menyatakan ujian berikutnya digelar 2027 dengan kapasitas yang dievaluasi", "Tunggu Pengumuman")],
      info=[("Format Skema Baru", "Daring, satu hari, 3 sampai 3,5 jam, diawasi pengawas dan AI"),
            ("Kelulusan", "Nilai minimal 60 dari skala 100, hasil langsung keluar setelah ujian"),
            ("Biaya", "USKP tidak dipungut biaya; siapkan surat pernyataan bermeterai"),
            ("Pendaftaran", "Melalui portal USKP BPPK sesuai pengumuman Komite Pelaksana")],
      src=("Ortax: Uji Kompetensi Perpajakan Oktober 2026", "https://ortax.org/bppk-uji-kompetensi-perpajakan-digelar-mulai-pertengahan-oktober-2026")),
]
SRC2 = [("IKPI: USKP Periode II 2026", "https://ikpi.or.id/en/pendaftaran-uskp-periode-ii-2026-dibuka-kuota-3022-peserta-di-28-kota/"),
        ("MyConsultant: Jadwal USKP 2026", "https://myconsultant.id/info-uskp/jadwal/"),
        ("IKPI: Sosialisasi CPMA bersama IAMI", "https://ikpi.or.id/en/ikpi-gandeng-iami-sosialisasikan-sertifikasi-cpma-buka-peluang-penguatan-kompetensi-konsultan-pajak/")]

FAQ = [("Kapan ujian CPA IAPI berikutnya?", "Periode IV Ujian Profesi Akuntan Publik 2026 berlangsung November sampai Desember 2026 untuk Tingkat Dasar dan Tingkat Profesional, di Test Center mitra IAPI."),
       ("Kapan ujian CA IAI terdekat?", "Ujian CA berjalan mulai 29 Oktober 2026 dan berlanjut sampai 18 Desember 2026, dengan beberapa pilihan tanggal untuk tiap mata ujian Tingkat Profesional dan Lanjutan."),
       ("Berapa kali ujian CPMA dalam setahun?", "Ujian CPMA IAMI diadakan dua kali setahun, Mei dan November. Pemegang CA yang memenuhi syarat pengalaman bisa memakai jalur fast track dua mata ujian."),
       ("Apakah USKP masih ada di 2026?", "USKP 2026 hanya untuk peserta mengulang (April, Agustus, dan Oktober). Mulai pertengahan Oktober sampai Desember 2026 BPPK menggelar Uji Kompetensi Perpajakan skema baru secara daring."),
       ("Sertifikasi mana yang cocok untuk saya?", "CPA untuk yang ingin menjadi Akuntan Publik dan menandatangani audit. CA untuk akuntan profesional umum. CPMA untuk akuntan manajemen dan FP&A. Sertifikasi konsultan pajak untuk yang ingin berpraktik sebagai konsultan pajak.")]

CSS = """<style>
.exnav{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 6px}.exnav a{border:1px solid #d5dbe5;padding:8px 14px;border-radius:999px;font-weight:600;text-decoration:none;color:inherit;font-size:14px}
.exgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin:22px 0}
.excard{border:1px solid #d5dbe5;border-top:4px solid var(--c);padding:16px 18px;background:#fff;text-decoration:none;color:#0B1F33;display:flex;flex-direction:column;gap:6px}
.excard b{font-size:22px;letter-spacing:.02em}.excard small{color:#5b6576;font-size:13px}.excard em{font-style:normal;font-size:14px;line-height:1.45}
.excard .st{align-self:flex-start;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--c)}
.exsec{margin:40px 0 0;padding-top:8px;scroll-margin-top:80px}.exsec h2{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
.exsec h2 span{font-size:13px;font-weight:700;letter-spacing:.06em;color:#fff;background:var(--c);padding:3px 9px}
.exsec .nx{border-left:4px solid var(--c);background:#f5f7fb;padding:12px 16px;margin:12px 0 16px;color:#0B1F33}
.tbl td.ok{white-space:nowrap}.exsrc{font-size:13px;color:#5b6576}
@media (prefers-color-scheme:dark){.excard{background:#0f1a28;color:#e8edf5;border-color:#26364a}.excard small{color:#9fb0c5}.exnav a{border-color:#26364a}.exsec .nx{background:#0f1a28;color:#e8edf5}}
</style>"""

def card(e, href):
    return f'<a class="excard" href="{href}" style="--c:{e["warna"]}"><span class="st">{esc(e["status"])}</span><b>{e["kode"]}</b><small>{esc(e["org"])} · {esc(e["nama"])}</small><em>{esc(e["next"])}</em></a>'

def section(e):
    third = "Jam Mulai" if e["id"] == "ca" else "Status"
    first = "Tanggal" if e["id"] == "ca" else "Periode"
    second = "Mata Ujian" if e["id"] == "ca" else "Waktu"
    rows = "".join(f"<tr><td class=\"ok\">{esc(a)}</td><td>{esc(b)}</td><td class=\"ok\">{esc(c)}</td></tr>" for a, b, c in e["rows"])
    info = "".join(f"<tr><td class=\"ok\"><b>{esc(k)}</b></td><td>{esc(v)}</td></tr>" for k, v in e["info"])
    return f'''<section class="exsec" id="{e["id"]}" style="--c:{e["warna"]}">
<h2><span>{e["kode"]}</span>{esc(e["nama"])}</h2>
<p>{esc(e["ringkas"])} Penyelenggara: <b>{esc(e["org"])}</b>.</p>
<p class="nx"><b>Jadwal Terdekat:</b> {esc(e["next"])}</p>
<div class="scroll"><table class="tbl"><thead><tr><th>{first}</th><th>{second}</th><th>{third}</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="scroll"><table class="tbl"><tbody>{info}</tbody></table></div>
<p class="exsrc">Sumber: <a href="{e["src"][1]}" target="_blank" rel="noopener">{esc(e["src"][0])}</a></p>
</section>'''

def page():
    title = "Jadwal Ujian CPA, CA, CPMA, dan Konsultan Pajak 2026"
    desc = "Jadwal ujian sertifikasi akuntan 2026: CPA IAPI periode IV Nov–Des, CA IAI mulai 29 Oktober, CPMA IAMI November, dan USKP serta Uji Kompetensi Perpajakan BPPK. Diperbarui " + UPD + "."
    desc = desc.replace("–", " sampai ")
    img = f"{BASE}/img/share/{KEY}-og.jpg"
    crumbs = [("UpdateSAK", BASE + "/"), ("Jadwal Ujian", URL)]
    ld = json.loads(B.ld_graph(URL, title, desc, crumbs, FAQ, img))
    for g in ld["@graph"]:
        if g["@type"] == "Article": g["datePublished"] = g["dateModified"] = UPD_ISO
    ld = json.dumps(ld, ensure_ascii=False)
    srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in [e["src"] for e in EX] + SRC2)
    out = f'''{CSS}<article class="art"><div class="wrap">
<nav class="crumb"><a href="/">Beranda</a> / <a href="/jadwal-ujian/">Jadwal Ujian</a></nav>
<p class="label">Sertifikasi Profesi</p>
<h1>Jadwal Ujian CPA, CA, CPMA, dan Konsultan Pajak 2026</h1>
<p class="lede">Empat sertifikasi yang paling sering ditanyakan mahasiswa akuntansi dan praktisi, dalam satu halaman. Tanggal diambil dari pengumuman resmi penyelenggara.</p>
<p class="upd">Tim UpdateSAK · Diperbarui {UPD}</p>
{B.share(URL, title, KEY)}
<div class="exgrid">{"".join(card(e, "#" + e["id"]) for e in EX)}</div>
<div class="exnav">{"".join(f'<a href="#{e["id"]}">{e["kode"]}</a>' for e in EX)}<a href="#siapkan">Persiapan</a></div>
{"".join(section(e) for e in EX)}
<section class="exsec" id="siapkan" style="--c:#0B1F33"><h2>Persiapan Yang Bisa Dimulai Hari Ini</h2>
<div class="prose"><ol>
<li><b>Hafalkan penomoran PSAK baru.</b> Soal CA dan CPA memakai nomor 3 digit. Ringkasannya ada di <a href="/artikel/penomoran-psak-3-digit/">Penomoran PSAK Baru 3 Digit</a> dan <a href="/eksplor/#standar">Panduan Per Standar</a>.</li>
<li><b>Latihan studi kasus.</b> Kerjakan <a href="/materi/">Materi Studi Kasus</a>: jurnal, dampak laporan keuangan, kalimat CALK, dan prosedur auditor, cocok untuk mata ujian Pelaporan Korporat dan Audit & Asurans.</li>
<li><b>Bangun laporan keuangan dari nol.</b> Pakai <a href="/#kalkulator">Kalkulator Standar Akuntansi</a> untuk menyusun empat laporan dan CALK dari satu neraca dan laba rugi.</li>
<li><b>Ikuti perubahan yang berlaku 2027.</b> <a href="/artikel/contoh-laba-rugi-psak-118/">PSAK 118</a> mengubah format laba rugi dan mulai muncul di soal.</li>
</ol></div></section>
{B.faq_html(FAQ)}
<h2>Sumber Resmi</h2><ul class="exsrc">{srcs}</ul>
<p class="exsrc">Jadwal bisa berubah. Selalu konfirmasi ke penyelenggara sebelum mendaftar dan membayar.</p>
{B.wa_box("Laporan Keuangan")}
</div></article>
'''
    B.write("jadwal-ujian", B.HEAD.format(title=esc(title + " | UpdateSAK"), desc=esc(desc), url=URL, ogt=esc(title), img=img, ld=ld) + out + B.FOOT)
    B.make_images(KEY, "Jadwal Ujian 2026", "Jadwal Ujian CPA, CA, CPMA, dan Konsultan Pajak")

HOME = '''<!--jadwal:start-->{css}
<section id="jadwal"><div class="wrap">
  <div class="head"><h2>Jadwal Ujian Sertifikasi Terdekat</h2><p>CPA, CA, CPMA, dan konsultan pajak dalam satu tempat. Diperbarui {upd}.</p></div>
  <div class="exgrid">{cards}</div>
  <p><a class="btn arrow" href="/jadwal-ujian/">Lihat Jadwal Lengkap</a></p>
</div></section>
<!--jadwal:end-->'''

def wire():
    # tab nav di semua halaman
    n = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"): continue
            p = os.path.join(root, f); s = open(p, encoding="utf-8").read()
            m0 = re.search(r'<nav class="tabs".*?</nav>', s, flags=re.S)
            if not m0 or '/jadwal-ujian/' in m0.group(0): continue
            cur = ' aria-current="page"' if p.endswith(os.path.join("jadwal-ujian", "index.html")) else ""
            if cur: s = re.sub(r'(<nav class="tabs"[^>]*>.*?)</nav>', lambda m: m.group(1).replace(' aria-current="page"', '') + '</nav>', s, count=1, flags=re.S)
            s2 = re.sub(r'(<nav class="tabs"[^>]*>.*?)</nav>', lambda m: m.group(1) + f'<a href="/jadwal-ujian/"{cur}>Jadwal Ujian</a></nav>', s, count=1, flags=re.S)
            if s2 != s: open(p, "w", encoding="utf-8").write(s2); n += 1
    # blok beranda
    p = os.path.join(SITE, "index.html"); s = open(p, encoding="utf-8").read()
    blk = HOME.format(css=CSS, upd=UPD, cards="".join(card(e, "/jadwal-ujian/#" + e["id"]) for e in EX))
    if "<!--jadwal:start-->" in s: s = re.sub(r"<!--jadwal:start-->.*?<!--jadwal:end-->", lambda m: blk, s, flags=re.S)
    else:
        i = s.find('<section class="final">'); s = s[:i] + blk + "\n\n" + s[i:]
    s = s.replace('<span><a href="/eksplor/">Eksplor</a> · <a href="/materi/">Materi</a> · <a href="mailto:', '<span><a href="/eksplor/">Eksplor</a> · <a href="/materi/">Materi</a> · <a href="/jadwal-ujian/">Jadwal Ujian</a> · <a href="mailto:')
    open(p, "w", encoding="utf-8").write(s)
    # sitemap + llms
    p = os.path.join(SITE, "sitemap.xml"); s = open(p).read()
    if URL not in s: s = s.replace("</urlset>", f"<url><loc>{URL}</loc><lastmod>{UPD_ISO}</lastmod></url>\n</urlset>")
    open(p, "w").write(s)
    p = os.path.join(SITE, "llms.txt"); s = open(p, encoding="utf-8").read().split("\n## Jadwal Ujian Sertifikasi")[0].rstrip()
    s += f"\n\n## Jadwal Ujian Sertifikasi\n- [Jadwal Ujian CPA, CA, CPMA, dan Konsultan Pajak 2026]({URL}): " + "; ".join(f"{e['kode']} ({e['org']}): {e['next']}" for e in EX) + "\n"
    open(p, "w", encoding="utf-8").write(s)
    return n

if __name__ == "__main__":
    page(); n = wire(); print("jadwal-ujian ok, nav", n)
