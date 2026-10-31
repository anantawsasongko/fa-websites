# Ruang Dosen UpdateSAK (31 Okt 2026): /dosen/ hub, daftar jurnal Scopus gratis/APC rendah, berita call for paper,
# dan bahan ajar PDF (maks 8 slide). Data jurnal dan CFP di dosen_jurnal.json dan dosen_cfp.json (diverifikasi manual dari sumber resmi).
# Dijalankan prep.py SETELAH build_jadwal.py. Idempoten: blok Eksplor memakai penanda dosen:start/end.
import os, re, sys, json, html, subprocess
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_seo as B
import dosen_slides as DS
esc = html.escape
SITE = B.SITE; BASE = B.BASE
UPD_ISO = "2026-10-31"; UPD = "31 Oktober 2026"
J = json.load(open(os.path.join(HERE, "dosen_jurnal.json"), encoding="utf-8"))
FREE = sum(1 for j in J if j["akses"] != "OA APC rendah" and "submit" not in j["apc"].lower())
C = sorted(json.load(open(os.path.join(HERE, "dosen_cfp.json"), encoding="utf-8")), key=lambda x: x["batas_iso"])
PDFDIR = os.path.join(SITE, "dosen", "pdf"); IMGDIR = os.path.join(SITE, "img", "dosen")
WA_DOSEN = B.WA + quote("Halo tim UpdateSAK, saya dosen akuntansi dan ingin mengusulkan topik bahan ajar berikutnya: ")
PANTAU = [("GAMAICEB, FEB Universitas Gadjah Mada", "https://gamaiceb.feb.ugm.ac.id/", "Konferensi internasional ekonomi dan bisnis tahunan"),
          ("Call for Papers FEB UGM", "https://feb.ugm.ac.id/en/call-for-papers", "Daftar pengumuman konferensi dan jurnal FEB UGM"),
          ("Ikatan Akuntan Indonesia (IAI)", "https://web.iaiglobal.or.id/", "Pengumuman Simposium Nasional Akuntansi (SNA) dari IAI KAPd")]

CSS = """<style>
.ds-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin:22px 0}
.ds-card{border:1px solid var(--line);background:#fff;padding:20px;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;gap:8px;transition:transform .2s,box-shadow .2s}
.ds-card:hover{transform:translateY(-2px);box-shadow:0 10px 26px -18px rgba(11,31,51,.5)}
.ds-card .k{font-size:.72rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.ds-card b{font-family:var(--serif,inherit);font-size:1.18rem;line-height:1.3}.ds-card span{color:var(--muted);font-size:.92rem}
.ds-card .n{margin-top:auto;font-weight:600;font-size:.88rem;color:var(--accent)}
.ds-tbl td small{display:block;color:var(--muted);font-size:.8rem;margin-top:2px}
.ds-tbl td:first-child{width:62%}.ds-tbl td small{max-width:52ch}
.ds-pill{display:inline-block;font-size:.72rem;font-weight:600;padding:2px 8px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.ds-pill.g{border-color:#12A39A;color:#0B6E4F}.ds-pill.b{border-color:var(--accent);color:var(--accent)}
.cfp{border:1px solid var(--line);background:#fff;padding:16px 18px;display:grid;grid-template-columns:120px minmax(0,1fr);gap:16px;margin:0 0 12px}
.cfp .dl{border-right:1px solid var(--line);padding-right:12px}
.cfp .dl b{display:block;font-size:1.5rem;line-height:1.1;color:var(--ink)}.cfp .dl span{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.cfp .dl em{display:block;font-style:normal;font-size:.78rem;font-weight:600;color:var(--accent);margin-top:6px}
.cfp h3{font-size:1.04rem;line-height:1.35;margin:4px 0}.cfp h3 a{color:var(--ink);text-decoration:none}.cfp h3 a:hover{color:var(--accent)}
.cfp p{margin:2px 0;font-size:.9rem;color:var(--muted)}
.cfp.lewat{opacity:.45}
.ba{border:1px solid var(--line);background:#fff;display:flex;flex-direction:column}
.ba img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-bottom:1px solid var(--line);display:block}
.ba>div{padding:16px 18px;display:flex;flex-direction:column;align-items:flex-start;gap:8px;flex:1}
.ba h3{font-size:1.04rem;line-height:1.35;margin:0}.ba p{margin:0;font-size:.9rem;color:var(--muted)}
.ba .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:auto;padding-top:6px}
.ds-src{font-size:.85rem;color:var(--muted)}
@media (max-width:560px){.cfp{grid-template-columns:1fr;gap:8px}.cfp .dl{border-right:0;border-bottom:1px solid var(--line);padding:0 0 8px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}.cfp .dl b{font-size:1.15rem}.cfp .dl em{margin:0}}
@media (prefers-color-scheme:dark){.ds-card,.cfp,.ba{background:#0f1a28;color:#e8edf5;border-color:#26364a}}
</style>"""

COUNT_JS = """<script>(function(){var t=new Date();t.setHours(0,0,0,0);document.querySelectorAll('.cfp[data-d]').forEach(function(e){var d=new Date(e.dataset.d+'T00:00:00'),n=Math.round((d-t)/864e5),m=e.querySelector('em');if(n<0){e.classList.add('lewat');m.textContent='Sudah ditutup'}else m.textContent=n===0?'Hari terakhir':'Sisa '+n+' hari'})})();</script>"""


def head(path, title, desc, crumbs, faq, key, kicker):
    url = BASE + path; img = f"{BASE}/img/share/{key}-og.jpg"
    ld = json.loads(B.ld_graph(url, title, desc, crumbs, faq, img))
    for g in ld["@graph"]:
        if g["@type"] == "Article": g["datePublished"] = g["dateModified"] = UPD_ISO
    B.make_images(key, kicker, title)
    h = B.HEAD.format(title=esc(title + " | UpdateSAK"), desc=esc(desc), url=url, ogt=esc(title), img=img, ld=json.dumps(ld, ensure_ascii=False))
    return h.replace(' aria-current="page">Eksplor', '>Eksplor')


def crumb(*parts):
    s = '<nav class="crumb"><a href="/">Beranda</a> / <a href="/eksplor/">Eksplor</a> / <a href="/dosen/">Ruang Dosen</a>'
    return s + "".join(f" / {esc(p)}" for p in parts) + "</nav>"


def cta_dosen():
    return (f'<aside class="cta-box dark"><div><b>Usulkan Topik Bahan Ajar Berikutnya</b><span>Butuh slide untuk mata kuliah tertentu? '
            f'Kirim usulan topiknya; usulan dari dosen menjadi bahan pertimbangan untuk bahan ajar berikutnya.</span></div>'
            f'<a class="btn arrow" target="_blank" rel="noopener" href="{WA_DOSEN}">Kirim Usulan via WhatsApp</a></aside>')


def badge(a):
    cls = {"Diamond OA": "g", "OA APC rendah": "b"}.get(a, "")
    return f'<span class="ds-pill {cls}">{esc(a)}</span>'


# ---------- 1. Jurnal ----------
GRP = [("Diamond OA", "Terbuka Tanpa Biaya (Diamond Open Access)", "Penulis tidak membayar dan pembaca tidak membayar. Biaya ditanggung institusi penerbit."),
       ("OA APC rendah", "Akses Terbuka dengan APC Rendah", "Ada article processing charge (APC) yang relatif terjangkau, dibayar setelah naskah diterima."),
       ("Langganan (gratis jalur non-OA)", "Jurnal Langganan, Gratis Lewat Jalur Non-Open Access",
        "Jurnal hybrid. Tidak ada biaya bila penulis tidak memilih open access; artikel dibaca pelanggan atau lewat repositori sesuai kebijakan penerbit.")]
J_FAQ = [("Apakah ada jurnal Scopus akuntansi yang benar-benar gratis?", "Ada. Jurnal diamond open access seperti Gadjah Mada International Journal of Business dan Asian Journal of Accounting Research tidak memungut biaya dari penulis. Jurnal langganan (hybrid) juga gratis selama penulis tidak memilih open access."),
         ("Apa beda diamond open access dan jalur non-OA di jurnal hybrid?", "Diamond open access gratis untuk penulis dan pembaca. Jurnal hybrid gratis untuk penulis bila artikel diterbitkan dengan jalur langganan, tetapi pembaca perlu akses langganan, kecuali penulis membayar APC open access."),
         ("Bagaimana memastikan jurnal masih terindeks Scopus?", "Cari judul atau ISSN di Scopus Sources, pastikan status aktif dan cakupan sampai tahun berjalan, lalu cocokkan alamat situs dengan yang tercantum di halaman sumber Scopus untuk menghindari jurnal yang dibajak."),
         ("Apakah kuartil jurnal bisa berubah?", "Bisa. Kuartil SJR dan CiteScore diperbarui setiap tahun. Kuartil di halaman ini mencantumkan tahun datanya; cek ulang sebelum submit bila kuartil menjadi syarat angka kredit.")]


def p_jurnal():
    path = "/dosen/jurnal-scopus-gratis/"
    title = "Daftar Jurnal Scopus Akuntansi Gratis dan APC Rendah 2026"
    n_free = FREE
    desc = f"{len(J)} jurnal terindeks Scopus bidang akuntansi, keuangan, dan bisnis yang gratis atau berbiaya rendah untuk dosen: diamond open access, APC rendah, dan jalur non-OA. Diperbarui {UPD}."
    secs = ""
    for k, h, d in GRP:
        rows = "".join(
            f'<tr><td><a href="{esc(j["url"])}" target="_blank" rel="noopener"><b>{esc(j["nama"])}</b></a><small>{esc(j["penerbit"])}, {esc(j["negara"])} · {esc(j["bidang"])}</small>'
            + (f'<small>{esc(j["catatan"])}</small>' if j.get("catatan") else "") + f'</td><td>{esc(j["apc"])}</td><td>{esc(j["kuartil"]) or "Cek SJR"}</td></tr>'
            for j in J if j["akses"] == k)
        secs += f'''<h2 id="{re.sub(r"[^a-z]+", "-", k.lower()).strip("-")}">{esc(h)}</h2><p>{esc(d)}</p>
<div class="scroll"><table class="tbl ds-tbl"><thead><tr><th>Jurnal</th><th>Biaya Penulis</th><th>Kuartil</th></tr></thead><tbody>{rows}</tbody></table></div>'''
    key = "dosen-jurnal"
    out = f'''{CSS}<article class="art"><div class="wrap">
{crumb("Jurnal Scopus")}
<p class="label">Ruang Dosen · Publikasi</p>
<h1>{esc(title)}</h1>
<p class="lede">{len(J)} jurnal terindeks Scopus untuk riset akuntansi, audit, keuangan, dan keuangan syariah. {n_free} di antaranya tanpa biaya bagi penulis. Disusun untuk dosen yang mengejar publikasi internasional dengan anggaran terbatas.</p>
<p class="upd">Tim UpdateSAK · Diperbarui {UPD}</p>
{B.share(BASE + path, title, key)}
<div class="ds-grid">{"".join(f'<a class="ds-card" href="#{re.sub(r"[^a-z]+", "-", k.lower()).strip("-")}"><span class="k">{esc(k)}</span><b>{sum(1 for j in J if j["akses"] == k)} Jurnal</b><span>{esc(h)}</span></a>' for k, h, d in GRP)}</div>
{secs}
<h2>Cek Lima Hal Sebelum Submit</h2>
<div class="prose"><ol>
<li><b>Status Scopus aktif.</b> Cari ISSN di Scopus Sources dan pastikan cakupan sampai tahun berjalan, bukan "discontinued".</li>
<li><b>Alamat situs resmi.</b> Buka situs jurnal dari tautan di halaman sumber Scopus atau DOAJ, bukan dari email undangan. Jurnal yang dibajak memakai situs tiruan.</li>
<li><b>Biaya tertulis.</b> Baca halaman author guidelines: biaya submit, APC, dan biaya open access opsional.</li>
<li><b>Kesesuaian ruang lingkup.</b> Baca 3 sampai 5 artikel terbaru; naskah yang di luar scope biasanya ditolak tanpa review.</li>
<li><b>Waktu proses.</b> Jurnal diamond banyak peminat; antre review bisa lebih lama. Sesuaikan dengan tenggat angka kredit.</li>
</ol></div>
{B.faq_html(J_FAQ)}
<p class="ds-src">Status Scopus dan kuartil dicek lewat daftar Scopus, Scimago, dan situs penerbit; biaya dari halaman author guidelines jurnal, DOAJ, dan daftar jurnal penerbit per {UPD}. Biaya dan status bisa berubah sewaktu-waktu. Konversi ringgit ke rupiah bersifat perkiraan.</p>
{cta_dosen()}
</div></article>
'''
    B.write(path.strip("/"), head(path, title, desc, [("UpdateSAK", BASE + "/"), ("Ruang Dosen", BASE + "/dosen/"), ("Jurnal Scopus", BASE + path)], J_FAQ, key, "Ruang Dosen") + out + B.FOOT)
    return path, title, desc


# ---------- 2. Call for paper ----------
C_FAQ = [("Di mana mencari call for paper akuntansi yang masih buka?", "Halaman ini merangkum konferensi dan special issue jurnal akuntansi bereputasi yang tenggatnya belum lewat, lengkap dengan tautan resmi. Untuk konferensi dalam negeri, pantau situs penyelenggara seperti GAMAICEB FEB UGM dan IAI."),
         ("Apa beda konferensi dan special issue?", "Konferensi meminta makalah untuk dipresentasikan, kadang dengan jalur ke jurnal mitra. Special issue adalah edisi khusus jurnal dengan tema tertentu; naskah langsung melalui review jurnal."),
         ("Apakah special issue lebih mudah tembus?", "Tidak selalu. Standar review sama dengan edisi reguler. Keuntungannya, tema sudah jelas sehingga naskah yang tepat sasaran punya peluang lebih baik.")]


def p_cfp():
    path = "/dosen/call-for-paper/"
    title = "Call for Paper Akuntansi Terbaru: Konferensi dan Special Issue"
    desc = f"{len(C)} call for paper akuntansi dan keuangan yang masih dibuka: konferensi internasional dan special issue jurnal Scopus tentang keberlanjutan, AI, audit, dan sektor publik. Tenggat terdekat {C[0]['batas']}. Diperbarui {UPD}."
    def item(x):
        d, m, y = x["batas"].split(" ")
        meta = " · ".join(v for v in (x["jenis"], x["penyelenggara"]) if v)
        extra = "".join(f"<p>{esc(v)}</p>" for v in (("Pelaksanaan: " + x["pelaksanaan"]) if x.get("pelaksanaan") else "", ("Luaran: " + x["luaran"]) if x.get("luaran") else "", x.get("catatan", "")) if v)
        return (f'<div class="cfp" data-d="{x["batas_iso"]}"><div class="dl"><span>Tenggat</span><b>{d} {m[:3]}</b><span>{y}</span><em></em></div>'
                f'<div><p>{esc(meta)}</p><h3><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["judul"])}</a></h3><p><b>Tema:</b> {esc(x["tema"])}</p>{extra}</div></div>')
    pantau = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a>: {esc(d)}</li>' for n, u, d in PANTAU)
    key = "dosen-cfp"
    out = f'''{CSS}<article class="art"><div class="wrap">
{crumb("Call for Paper")}
<p class="label">Ruang Dosen · Berita Call for Paper</p>
<h1>{esc(title)}</h1>
<p class="lede">{len(C)} kesempatan publikasi yang masih dibuka, diurutkan dari tenggat terdekat. Setiap judul menuju halaman resmi penyelenggara atau jurnal.</p>
<p class="upd">Tim UpdateSAK · Diperbarui {UPD}</p>
{B.share(BASE + path, title, key)}
<h2>Masih Dibuka</h2>
{"".join(item(x) for x in C)}
<h2>Konferensi Dalam Negeri: Pantau Pengumumannya</h2>
<p>Per {UPD}, konferensi akuntansi utama di Indonesia untuk 2027 belum membuka call for paper. Pantau halaman resmi berikut:</p>
<div class="prose"><ul>{pantau}</ul></div>
{B.faq_html(C_FAQ)}
<p class="ds-src">Tanggal diambil dari halaman resmi penyelenggara atau jurnal per {UPD}. Konfirmasi tenggat dan syarat di halaman resmi sebelum submit. Status "Sisa hari" dihitung otomatis di browser.</p>
{cta_dosen()}
</div></article>
{COUNT_JS}
'''
    B.write(path.strip("/"), head(path, title, desc, [("UpdateSAK", BASE + "/"), ("Ruang Dosen", BASE + "/dosen/"), ("Call for Paper", BASE + path)], C_FAQ, key, "Ruang Dosen") + out + B.FOOT)
    return path, title, desc


# ---------- 3. Bahan ajar ----------
def thumbs(res):
    os.makedirs(IMGDIR, exist_ok=True)
    for d, n in res:
        pdf = os.path.join(PDFDIR, d["slug"] + ".pdf"); out = os.path.join(IMGDIR, d["slug"])
        for pg, suf in ((1, "cover"), (4, "isi")):
            subprocess.run(["pdftoppm", "-f", str(pg), "-l", str(pg), "-r", "50", "-jpeg", "-jpegopt", "quality=80", "-singlefile", pdf, f"{out}-{suf}"], check=True)


BA_FAQ = [("Bolehkah slide ini dipakai di kelas?", "Boleh. Bahan ajar bebas dipakai dan dibagikan untuk perkuliahan dengan mencantumkan sumber updatesak.com."),
          ("Mengapa hanya maksimal 8 slide?", "Supaya mudah disisipkan ke satu pertemuan: konsep inti, satu contoh angka lengkap, soal diskusi, dan rangkuman. Detail tambahan ada di halaman PSAK terkait."),
          ("Apakah angka contohnya data perusahaan nyata?", "Tidak. Semua angka adalah data ilustrasi yang dihitung konsisten, sehingga aman dipakai untuk latihan dan ujian.")]


def p_bahan(res):
    path = "/dosen/bahan-ajar/"
    title = "Bahan Ajar Akuntansi Keuangan PDF Gratis: PSAK 118, 116, 115, 109"
    desc = f"{len(res)} bahan ajar slide PDF gratis untuk dosen akuntansi, maksimal 8 slide per topik: PSAK 118, penomoran PSAK baru, PSAK 116 sewa, PSAK 115 pendapatan, PSAK 109 ECL, dan laporan arus kas. Lengkap contoh angka dan soal diskusi."
    cards = "".join(
        f'''<article class="ba"><img src="/img/dosen/{d["slug"]}-cover.jpg" alt="Slide sampul {esc(d["judul"])}" width="480" height="270" loading="lazy">
<div><span class="ds-pill b">{n} slide · PDF</span><h3>{esc(d["judul"])}</h3><p>{esc(d["desk"])}</p>
<div class="row"><a class="btn btn-sm dl" href="/dosen/pdf/{d["slug"]}.pdf" download>Download PDF</a><a class="btn btn-sm btn-ghost" href="{d["url"].replace(BASE, "")}">Materi Lengkap</a></div></div></article>'''
        for d, n in res)
    key = "dosen-bahan-ajar"
    out = f'''{CSS}<article class="art"><div class="wrap">
{crumb("Bahan Ajar")}
<p class="label">Ruang Dosen · Bahan Ajar</p>
<h1>{esc(title)}</h1>
<p class="lede">Slide siap pakai untuk satu pertemuan, maksimal 8 slide per topik: tujuan pembelajaran, konsep inti, satu contoh angka lengkap, soal diskusi, dan rangkuman dengan QR code ke materi lanjutan.</p>
<p class="upd">Tim UpdateSAK · Diperbarui {UPD}</p>
{B.share(BASE + path, title, key)}
<div class="ds-grid">{cards}</div>
<h2>Cara Memakai di Kelas</h2>
<div class="prose"><ol>
<li><b>Sebelum kelas:</b> bagikan PDF ke mahasiswa agar mereka membaca contoh angka lebih dulu.</li>
<li><b>Di kelas:</b> bahas konsep 15 menit, lalu kerjakan contoh angka bersama dan minta mahasiswa mengulang hitungannya.</li>
<li><b>Diskusi:</b> pakai slide soal diskusi untuk kerja kelompok 20 menit.</li>
<li><b>Setelah kelas:</b> arahkan mahasiswa ke QR code di slide terakhir untuk ringkasan standar, contoh CALK, dan <a href="/materi/">studi kasus</a>.</li>
</ol></div>
{B.faq_html(BA_FAQ)}
{cta_dosen()}
</div></article>
'''
    B.write(path.strip("/"), head(path, title, desc, [("UpdateSAK", BASE + "/"), ("Ruang Dosen", BASE + "/dosen/"), ("Bahan Ajar", BASE + path)], BA_FAQ, key, "Ruang Dosen") + out + B.FOOT)
    return path, title, desc


# ---------- hub ----------
def cards3(res, href=lambda p: p):
    nf = FREE
    return (f'<div class="ds-grid">'
            f'<a class="ds-card" href="{href("/dosen/jurnal-scopus-gratis/")}"><span class="k">Publikasi</span><b>Jurnal Scopus Gratis dan APC Rendah</b><span>{len(J)} jurnal akuntansi, keuangan, dan bisnis; {nf} tanpa biaya bagi penulis.</span><span class="n">Lihat Daftar →</span></a>'
            f'<a class="ds-card" href="{href("/dosen/call-for-paper/")}"><span class="k">Berita</span><b>Call for Paper yang Masih Dibuka</b><span>{len(C)} konferensi dan special issue. Tenggat terdekat {C[0]["batas"]}.</span><span class="n">Lihat Tenggat →</span></a>'
            f'<a class="ds-card" href="{href("/dosen/bahan-ajar/")}"><span class="k">Bahan Ajar</span><b>Slide PDF Maksimal 8 Halaman</b><span>{len(res)} topik: PSAK 118, penomoran PSAK, 116, 115, 109, dan arus kas.</span><span class="n">Download Gratis →</span></a></div>')


def p_hub(res):
    path = "/dosen/"
    title = "Ruang Dosen Akuntansi: Jurnal Scopus, Call for Paper, Bahan Ajar"
    desc = "Ruang Dosen UpdateSAK: daftar jurnal Scopus akuntansi gratis dan APC rendah, berita call for paper terbaru, dan bahan ajar slide PDF gratis maksimal 8 halaman."
    nxt = "".join(f'<li><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["judul"])}</a>: tenggat {esc(x["batas"])}</li>' for x in C[:4])
    key = "dosen"
    out = f'''{CSS}<article class="art"><div class="wrap">
<nav class="crumb"><a href="/">Beranda</a> / <a href="/eksplor/">Eksplor</a> / Ruang Dosen</nav>
<p class="label">Ruang Dosen</p>
<h1>Ruang Dosen Akuntansi</h1>
<p class="lede">Tiga kebutuhan rutin dosen akuntansi dalam satu tempat: jurnal Scopus yang terjangkau, tenggat call for paper, dan bahan ajar standar terbaru yang siap dipakai di kelas.</p>
<p class="upd">Tim UpdateSAK · Diperbarui {UPD}</p>
{B.share(BASE + path, title, key)}
{cards3(res)}
<h2>Tenggat Terdekat</h2>
<div class="prose"><ul>{nxt}</ul></div>
<p><a class="btn arrow" href="/dosen/call-for-paper/">Semua Call for Paper</a></p>
<h2>Bahan Pendukung untuk Mahasiswa</h2>
<div class="prose"><ul>
<li><a href="/eksplor/#standar">Panduan Per Standar</a>: ringkasan tiap PSAK, contoh kebijakan CALK, dan temuan auditor.</li>
<li><a href="/materi/">Studi Kasus</a>: soal dan pembahasan dengan data ilustrasi, siap untuk tugas atau ujian.</li>
<li><a href="/jadwal-ujian/">Jadwal Ujian CPA, CA, CPMA, dan Konsultan Pajak</a> untuk mahasiswa tingkat akhir.</li>
</ul></div>
{cta_dosen()}
</div></article>
'''
    B.write("dosen", head(path, title, desc, [("UpdateSAK", BASE + "/"), ("Ruang Dosen", BASE + path)], [], key, "Ruang Dosen") + out + B.FOOT)
    return path, title, desc


EKS = '''<!--dosen:start-->{css}
<section id="dosen"><div class="wrap">
  <div class="head"><h2>Ruang Dosen</h2><p>Jurnal Scopus gratis dan berbiaya rendah, berita call for paper, dan bahan ajar slide PDF. Diperbarui {upd}.</p></div>
  {cards}
  <p><a class="btn arrow" href="/dosen/">Masuk Ruang Dosen</a></p>
</div></section>
<!--dosen:end-->'''


def wire(res, pages):
    p = os.path.join(SITE, "eksplor", "index.html"); s = open(p, encoding="utf-8").read()
    blk = EKS.format(css=CSS, upd=UPD, cards=cards3(res))
    if "<!--dosen:start-->" in s: s = re.sub(r"<!--dosen:start-->.*?<!--dosen:end-->", lambda m: blk, s, flags=re.S)
    else:
        i = s.find('<section id="standar">'); s = s[:i] + blk + "\n" + s[i:]
    open(p, "w", encoding="utf-8").write(s)
    # footer semua halaman: tautan Ruang Dosen
    n = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"): continue
            q = os.path.join(root, f); t = open(q, encoding="utf-8").read()
            if '<a href="/materi/">Materi</a> · ' in t and '/dosen/">Ruang Dosen' not in t:
                t = t.replace('<a href="/materi/">Materi</a> · ', '<a href="/materi/">Materi</a> · <a href="/dosen/">Ruang Dosen</a> · ', 1)
                open(q, "w", encoding="utf-8").write(t); n += 1
    p = os.path.join(SITE, "sitemap.xml"); s = open(p).read()
    for path, _, _ in pages:
        u = BASE + path
        if u not in s: s = s.replace("</urlset>", f"<url><loc>{u}</loc><lastmod>{UPD_ISO}</lastmod></url>\n</urlset>")
    open(p, "w").write(s)
    p = os.path.join(SITE, "llms.txt"); s = open(p, encoding="utf-8").read().split("\n## Ruang Dosen")[0].rstrip()
    s += "\n\n## Ruang Dosen\n" + "".join(f"- [{t}]({BASE}{pa}): {d}\n" for pa, t, d in pages)
    open(p, "w", encoding="utf-8").write(s)
    return n


if __name__ == "__main__":
    res = DS.build(PDFDIR); thumbs(res)
    pages = [p_hub(res), p_jurnal(), p_cfp(), p_bahan(res)]
    print("dosen ok, footer", wire(res, pages), "pdf", len(res))
