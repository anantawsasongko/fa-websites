# Update FA site 25 Okt 2026: halaman Laporan Tahunan PT, artikel Permenkum 49/2025, tahapan IPO, link footer, sitemap, llms
import os, re, json, html, warnings
warnings.filterwarnings('ignore')
M=os.path.dirname(os.path.abspath(__file__)); FA=os.path.join(M,"FA-Indonesia_Website_SIAP-UPLOAD-v58")
P=lambda *a: os.path.join(FA,*a)
rd=lambda p: open(p,encoding="utf-8").read()
def wr(p,s):
    old=open(p,encoding="utf-8").read() if os.path.exists(p) else ""
    assert s.count(chr(0x2014))<=old.count(chr(0x2014)), p
    os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w",encoding="utf-8").write(s)
WA="https://wa.me/6282245260121?text="
from urllib.parse import quote
SRC=[("Hukumonline, Kewajiban Terbaru Perseroan","https://www.hukumonline.com/klinik/a/kewajiban-terbaru-perseroan-lt6a6c0798b9662/"),
     ("DDTCNews, 17 Juni 2026","https://news.ddtc.co.id/berita/nasional/1820127/sudah-lewat-1-juni-ahu-minta-pt-segera-sampaikan-laporan-tahunan"),
     ("IZIN.co.id, masa transisi sampai 31 Oktober 2026","https://izin.co.id/blog/masa-transisi-pelaporan-rups-tahunan-2025-diperpanjang-hingga-31-oktober-2026/")]
FLOWCSS='''<style id="faflow">.fflow{display:flex;gap:0;flex-wrap:wrap;margin:18px 0 6px}
.fflow .st{flex:1 1 170px;min-width:0;padding:18px 18px 16px;border:1px solid var(--line,#333);display:grid;gap:4px;animation:fup .6s ease both;animation-delay:calc(var(--i,0)*120ms)}
.fflow .st small{font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.65}
.fflow .st b{font-size:17px;font-weight:600}.fflow .st span{font-size:14px;opacity:.8;line-height:1.45}
.fflow .ar{display:grid;place-items:center;padding:0 8px;font-size:20px;opacity:.6;animation:fnudge 1.6s ease-in-out infinite}
@keyframes fup{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes fnudge{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}
@media (max-width:640px){.fflow{flex-direction:column}.fflow .ar{transform:rotate(90deg);animation:none;padding:4px}}
.fchips{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.fchips span{padding:8px 12px;border:1px solid var(--line,#333);font-size:14px}
.falert{margin:18px 0 8px;padding:14px 16px;border-left:3px solid #c9a227;background:rgba(201,162,39,.08);font-size:15px}
.ftbl{overflow-x:auto;border:1px solid var(--line,#333);margin:12px 0}.ftbl table{border-collapse:collapse;width:100%;min-width:520px;font-size:14.5px}
.ftbl th,.ftbl td{padding:11px 14px;text-align:left;border-bottom:1px solid var(--line,#333);vertical-align:top}.ftbl thead th{font-weight:600}
</style>'''
def flow(steps):
    out=[]
    for i,(sm,b,sp) in enumerate(steps):
        if i: out.append('<div class="ar" aria-hidden="true">→</div>')
        out.append(f'<div class="st" style="--i:{i}"><small>{sm}</small><b>{b}</b><span>{sp}</span></div>')
    return '<div class="fflow">'+"".join(out)+'</div>'
def sources_html():
    return '<p class="t" style="font-size:13px;opacity:.75;margin-top:22px">Sumber: '+" · ".join(f'<a href="{u}" rel="noopener nofollow" target="_blank">{html.escape(t)}</a>' for t,u in SRC)+'. Ringkasan informatif, bukan nasihat hukum.</p>'

# ---------------- 1. halaman layanan baru ----------------
tpl=rd(P("konsultan-persiapan-ipo","index.html"))
URL="https://faindonesia.co.id/laporan-tahunan-pt/"
TITLE="Jasa Laporan Tahunan PT Sesuai Permenkum 49/2025 (Akta Notaris dan SABH) | FA Indonesia"
DESC="Penyusunan laporan tahunan PT dan laporan keuangan sesuai Permenkum 49/2025, draf keputusan RUPS, sampai disampaikan notaris lewat SABH. Untuk PT di seluruh Indonesia."
FAQ=[("Apakah semua PT wajib menyampaikan laporan tahunan lewat notaris?","Kewajiban Pasal 16 Permenkum 49/2025 berlaku untuk PT persekutuan modal. Persetujuan RUPS atas laporan tahunan dituangkan dalam akta notaris lalu disampaikan lewat SABH. PT perorangan memakai mekanisme pelaporan yang berbeda."),
     ("Apakah laporan keuangannya harus diaudit?","Tidak selalu. Audit oleh akuntan publik wajib bila PT memenuhi kriteria Pasal 68 UU PT, misalnya aset atau omzet paling sedikit Rp50 miliar atau menghimpun dana masyarakat. PT lain cukup menyusun laporan keuangan yang lengkap dan rapi."),
     ("Apa risikonya bila belum lapor?","Teguran tertulis, lalu pemblokiran akses SABH bila 30 hari setelah teguran belum dipenuhi. Selama diblokir, perubahan direksi, peralihan saham, dan perubahan data perseroan tertahan."),
     ("Apakah FA Indonesia bisa mencarikan notaris?","Bisa, kami merekomendasikan notaris. Honorarium notaris dibayar langsung oleh perusahaan kepada notaris, terpisah dari imbalan jasa FA.")]
ld={"@context":"https://schema.org","@graph":[
 {"@type":"WebPage","@id":URL,"url":URL,"name":TITLE,"description":DESC,"inLanguage":"id","isPartOf":{"@id":"https://faindonesia.co.id/#website"},"about":{"@id":URL+"#service"},"dateModified":"2026-10-25T12:00:00+07:00"},
 {"@type":"Service","@id":URL+"#service","name":"Penyusunan laporan tahunan PT sesuai Permenkum 49/2025","serviceType":"Penyusunan laporan tahunan perseroan","description":DESC,"provider":{"@type":"ProfessionalService","@id":"https://faindonesia.co.id/#service","name":"FA Indonesia","url":"https://faindonesia.co.id/","email":"ananta@faindonesia.co.id"},"areaServed":{"@type":"Country","name":"Indonesia"},"url":URL,"brand":{"@type":"Brand","name":"FA Indonesia"}},
 {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
 {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"FA Indonesia","item":"https://faindonesia.co.id/"},{"@type":"ListItem","position":2,"name":"Laporan Tahunan PT","item":URL}]}]}
main=f'''<main id="top">
<section class="block">
<div class="wrap">
<p class="eyebrow">Layanan · Kepatuhan Korporasi</p>
<h1 style="margin:.2em 0 .5em;font-size:clamp(34px,4.6vw,58px);line-height:1.1">Laporan Tahunan PT Sesuai Permenkum 49/2025, Siap Dibawa ke Notaris</h1>
<p class="t" style="max-width:62em">Laporan tahunan PT persekutuan modal kini wajib disetujui RUPS, dituangkan dalam akta notaris, dan disampaikan lewat SABH. FA Indonesia menyusun isinya, dari laporan keuangan sampai draf keputusan RUPS, sehingga notaris tinggal membuat akta dan mengirim.</p>
<div class="falert"><b>Tenggat dekat.</b> Masa transisi untuk tahun buku 2025 diberitakan sampai 31 Oktober 2026, dan sanksi mulai November 2026.</div>
<div class="head" style="margin-top:36px"><h2>Alurnya</h2></div>
{flow([("Minggu 1","Diagnosa","Cek data, kriteria wajib audit, dan jalur RUPS atau keputusan sirkuler."),("Minggu 2 sampai 3","Penyusunan","Laporan keuangan dengan CALK, laporan tahunan, dan draf keputusan."),("Notaris","Akta","Persetujuan RUPS dituangkan dalam akta notaris."),("Paling lama 30 hari","SABH","Notaris menyampaikan, bukti diterima perusahaan.")])}
<div class="head" style="margin-top:36px"><h2>Isi Minimal Laporan Tahunan</h2></div>
<p class="t" style="max-width:62em">Pasal 16 ayat (6) Permenkum 49/2025:</p>
<div class="fchips"><span>Laporan keuangan dan CALK</span><span>Laporan kegiatan perseroan</span><span>Tanggung jawab sosial dan lingkungan</span><span>Permasalahan selama tahun buku</span><span>Pengawasan Dewan Komisaris</span><span>Nama Direksi dan Komisaris</span><span>Gaji, honorarium, dan tunjangan</span></div>
<div class="head" style="margin-top:36px"><h2>Pembagian Peran</h2></div>
<div class="ftbl"><table><thead><tr><th>Pekerjaan</th><th>FA Indonesia</th><th>Notaris</th></tr></thead><tbody>
<tr><td>Laporan keuangan</td><td>Menyusun atau merapikan, lengkap dengan CALK</td><td>Tidak</td></tr>
<tr><td>Laporan tahunan</td><td>Menyusun sesuai Pasal 16, siap ditandatangani</td><td>Tidak</td></tr>
<tr><td>Keputusan RUPS atau sirkuler</td><td>Draf</td><td>Menuangkan dalam akta</td></tr>
<tr><td>Penyampaian SABH</td><td>Memantau sampai bukti terbit</td><td>Mengirim</td></tr>
</tbody></table></div>
<p class="t" style="max-width:62em">Honorarium notaris dan, bila wajib audit, jasa KAP dibayar langsung oleh perusahaan, terpisah dari imbalan jasa FA.</p>
<div class="head" style="margin-top:36px"><h2>Pertanyaan Umum</h2></div>
{"".join(f'<p style="margin:0 0 18px"><b>{html.escape(q)}</b><br>{html.escape(a)}</p>' for q,a in FAQ)}
<p class="t" style="max-width:62em">Baca juga: <a href="/artikel/laporan-tahunan-pt-permenkum-49-2025/">Laporan Tahunan PT Wajib Akta Notaris: Panduan Permenkum 49/2025</a> · <a href="/jasa-penyusunan-laporan-keuangan/">Jasa penyusunan laporan keuangan</a></p>
{sources_html()}
<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn solid" href="{WA+quote('Halo FA Indonesia, saya ingin konsultasi laporan tahunan PT sesuai Permenkum 49/2025.')}" rel="noopener" target="_blank">Chat Ananta, CPA</a><a class="btn line" href="mailto:ananta@faindonesia.co.id?cc=ananta.w.sasongko@gmail.com&amp;subject=Laporan%20Tahunan%20PT">Email</a><a class="btn line" href="/">FA Indonesia</a></div>
</div>
</section>
</main>'''
s=tpl
s=re.sub(r'<title>.*?</title>',f'<title>{html.escape(TITLE)}</title>',s,1,re.S)
for a in ['name="description"','property="og:description"']:
    s=re.sub(rf'<meta {a} content="[^"]*">',f'<meta {a} content="{html.escape(DESC)}">',s,1)
s=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{html.escape(TITLE)}">',s,1)
s=s.replace("https://faindonesia.co.id/konsultan-persiapan-ipo/\">",URL+"\">")
s=s.replace('<link rel="canonical" href="https://faindonesia.co.id/konsultan-persiapan-ipo/">',f'<link rel="canonical" href="{URL}">')
s=re.sub(r'<meta property="og:url" content="[^"]*">',f'<meta property="og:url" content="{URL}">',s,1)
s=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>',s,1,re.S)
s=re.sub(r'<main id="top">.*?</main>',lambda m:main,s,1,re.S)
s=s.replace('</head>',FLOWCSS+'</head>',1)
wr(P("laporan-tahunan-pt","index.html"),s)

# ---------------- 2. artikel ----------------
atpl=rd(P("artikel","checklist-persiapan-ipo","index.html"))
AURL="https://faindonesia.co.id/artikel/laporan-tahunan-pt-permenkum-49-2025/"
AT="Laporan Tahunan PT Wajib Akta Notaris: Panduan Permenkum 49/2025"
AD="Apa yang diwajibkan Permenkum 49/2025: isi minimal laporan tahunan, RUPS dalam akta notaris, penyampaian lewat SABH, tenggat, dan sanksi blokir akses."
AFAQ=[FAQ[0],FAQ[1],FAQ[2]]
abody=f'''<p>Selama bertahun-tahun, laporan tahunan PT tertutup cukup disimpan di lemari direksi. Peraturan Menteri Hukum Nomor 49 Tahun 2025 mengubahnya. Persetujuan RUPS atas laporan tahunan kini harus dituangkan dalam akta notaris dan disampaikan secara elektronik lewat Sistem Administrasi Badan Hukum (SABH).</p>
<h2>Alur Wajibnya</h2>
{flow([("6 bulan setelah tahun buku","RUPS","Direksi menyampaikan laporan tahunan setelah ditelaah Dewan Komisaris."),("Notaris","Akta","Persetujuan RUPS dituangkan dalam akta notaris."),("30 hari sejak akta","SABH","Disampaikan lewat notaris beserta laporan tahunannya.")])}
<p>Untuk tahun buku yang berakhir 31 Desember 2025, batas normal RUPS adalah 30 Juni 2026. Pemberitaan September 2026 menyebut masa transisi implementasi sampai 31 Oktober 2026.</p>
<h2>Isi Minimal Laporan Tahunan</h2>
<ul><li>Laporan keuangan: neraca dengan pembanding tahun lalu, laba rugi, arus kas, perubahan ekuitas, dan catatan atas laporan keuangan.</li><li>Laporan kegiatan perseroan.</li><li>Laporan pelaksanaan tanggung jawab sosial dan lingkungan.</li><li>Rincian masalah yang memengaruhi kegiatan usaha selama tahun buku.</li><li>Laporan tugas pengawasan Dewan Komisaris.</li><li>Nama anggota Direksi dan Dewan Komisaris.</li><li>Gaji, honorarium, dan tunjangan Direksi dan Dewan Komisaris.</li></ul>
<h2>Sanksinya Nyata</h2>
<p>Perseroan yang tidak melapor atau terlambat bisa mendapat teguran tertulis lewat notifikasi SABH. Bila 30 hari setelah teguran kewajiban belum dipenuhi, akses perseroan di SABH diblokir. Dampaknya terasa saat perusahaan butuh mengganti direksi, menjual saham, atau mengubah data. Pemeriksa di SABH lebih dulu mengecek status laporan tahunan.</p>
<h2>Yang Sering Jadi Hambatan</h2>
<ul><li>Laporan keuangan belum pernah disusun lengkap, apalagi dengan CALK.</li><li>Data remunerasi direksi dan komisaris tidak tercatat rapi.</li><li>Pemegang saham tersebar, sehingga RUPS fisik sulit diatur. Keputusan pemegang saham secara sirkuler bisa menjadi jalan keluar.</li><li>Notaris menerima paket dokumen yang belum siap, lalu bolak-balik meminta revisi.</li></ul>
<p>Di FA Indonesia, kami menyusun laporan keuangan dan laporan tahunannya sampai siap ditandatangani, termasuk draf keputusan RUPS, lalu berkoordinasi dengan notaris pilihan perusahaan. Detailnya ada di halaman <a href="/laporan-tahunan-pt/">jasa laporan tahunan PT</a>.</p>
<h2>Pertanyaan Umum</h2>
{"".join(f'<p><b>{html.escape(q)}</b><br>{html.escape(a)}</p>' for q,a in AFAQ)}
{sources_html()}'''
ald={"@context":"https://schema.org","@graph":[
 {"@type":"Article","@id":AURL+"#article","headline":AT,"description":AD,"url":AURL,"mainEntityOfPage":AURL,"inLanguage":"id","datePublished":"2026-10-25T12:00:00+07:00","dateModified":"2026-10-25T12:00:00+07:00","author":{"@type":"Person","@id":"https://faindonesia.co.id/ananta-w-sasongko/#person","name":"Ananta W. Sasongko, CPA, FMVA, FPAP","url":"https://faindonesia.co.id/ananta-w-sasongko/"},"publisher":{"@type":"Organization","@id":"https://faindonesia.co.id/#org","name":"FA Indonesia","url":"https://faindonesia.co.id/","logo":{"@type":"ImageObject","url":"https://faindonesia.co.id/img/brand/mark-hero.png"}},"image":"https://faindonesia.co.id/img/og/fa-indonesia-og.jpg"},
 {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"FA Indonesia","item":"https://faindonesia.co.id/"},{"@type":"ListItem","position":2,"name":"Wawasan","item":"https://faindonesia.co.id/artikel/"},{"@type":"ListItem","position":3,"name":AT,"item":AURL}]},
 {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in AFAQ]}]}
s=atpl
s=re.sub(r'<title>.*?</title>',f'<title>{html.escape(AT)} | FA Indonesia</title>',s,1,re.S)
s=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{html.escape(AT)} | FA Indonesia">',s,1)
for a in ['name="description"','property="og:description"']:
    s=re.sub(rf'<meta {a} content="[^"]*">',f'<meta {a} content="{html.escape(AD)}">',s,1)
s=s.replace("https://faindonesia.co.id/artikel/checklist-persiapan-ipo/",AURL)
s=re.sub(r'<meta property="article:published_time" content="[^"]*">','<meta property="article:published_time" content="2026-10-25T12:00:00+07:00">',s,1)
s=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps(ald,ensure_ascii=False)+'</script>',s,1,re.S)
s=re.sub(r'(<h1[^>]*>).*?(</h1>)',lambda m:m.group(1)+html.escape(AT)+m.group(2),s,1,re.S)
s=re.sub(r'<p class="meta">.*?</p>','<p class="meta">Oleh <a href="/ananta-w-sasongko/">Ananta W. Sasongko, CPA, FMVA, FPAP</a> · 25 Oktober 2026 · 4 menit baca</p>',s,1,re.S)
i=s.find('<p class="meta">'); i=s.find('</p>',i)+4; j=s.find('<div class="cbtns"')
s=s[:i]+"\n"+abody+"\n"+s[j:]
s=re.sub(r'<div class="cbtns".*?</div>','<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn solid" href="/laporan-tahunan-pt/">Jasa Laporan Tahunan PT</a><a class="btn line" href="'+WA+quote('Halo FA Indonesia, saya ingin konsultasi laporan tahunan PT sesuai Permenkum 49/2025.')+'" rel="noopener" target="_blank">Chat Ananta, CPA</a><a class="btn line" href="/artikel/">Wawasan Lainnya</a></div>',s,1,re.S)
s=s.replace('<p class="eyebrow"><a href="/artikel/" style="text-decoration:none">Artikel</a></p>','<p class="eyebrow"><a href="/artikel/" style="text-decoration:none">Wawasan</a></p>')
s=s.replace('</head>',FLOWCSS+'</head>',1)
wr(P("artikel","laporan-tahunan-pt-permenkum-49-2025","index.html"),s)

# artikel index: kartu baru paling atas + eyebrow Wawasan
s=rd(P("artikel","index.html"))
card=f'<a class="card2" href="/artikel/laporan-tahunan-pt-permenkum-49-2025/"><b>{html.escape(AT)}</b><span>{html.escape(AD)}</span></a>'
if "laporan-tahunan-pt-permenkum-49-2025" not in s:
    s=s.replace('<div class="cards2">','<div class="cards2">'+card,1)
    s=s.replace('"hasPart": [','"hasPart": [{"@type": "Article", "headline": "'+AT+'", "url": "'+AURL+'"}, ',1)
s=s.replace('<p class="eyebrow">Artikel</p>','<p class="eyebrow">Wawasan</p>',1)
s=re.sub(r'(<h1[^>]*>)Artikel Keuangan, Laporan Keuangan dan IPO(</h1>)',r'\1Wawasan: Artikel dan Berita Keuangan\2',s,1)
wr(P("artikel","index.html"),s)

# ---------------- 3. tahapan IPO ----------------
p=P("konsultan-persiapan-ipo","index.html"); s=rd(p)
if 'id="tahapan"' not in s:
    blk=f'''<div class="head" style="margin-top:36px" id="tahapan"><h2>Tahapan Kerja</h2></div>
<p class="t" style="max-width:62em">Dimulai dari pemetaan kesiapan. Setelah Tahap 1, perusahaan bebas memutuskan lanjut atau berhenti.</p>
{flow([("Tahap 1 · 6 sampai 8 minggu","IPO Readiness Mapping","Diagnosis laporan keuangan, pembanding emiten, model dan valuasi indikatif, checklist syarat BEI dan GCG, roadmap."),("Tahap 2","Pembenahan","Laporan keuangan siap audit KAP terdaftar OJK, organ perseroan, data room."),("OJK dan BEI","Pendaftaran","Due diligence, prospektus, dan public expose bersama penjamin emisi."),("Hari H","Pencatatan","Saham tercatat di Bursa Efek Indonesia.")])}
<p class="t" style="max-width:62em">Belum siap IPO tetapi butuh dana? FA juga mendampingi pencarian investor, ekuitas maupun pinjaman, dan <a href="/konsultan-kredit-bank/">pengajuan kredit bank</a>.</p>
'''
    s=s.replace('<div class="head" style="margin-top:36px"><h2>Untuk Siapa</h2></div>',blk+'<div class="head" style="margin-top:36px"><h2>Untuk Siapa</h2></div>',1)
    s=s.replace('</head>',FLOWCSS+'</head>',1)
    s=s.replace('"dateModified": "2026-10-11T17:00:00+07:00"','"dateModified": "2026-10-25T12:00:00+07:00"')
    wr(p,s)

# ---------------- 4. homepage kartu Pelaporan Korporasi ----------------
p=P("index.html"); s=rd(p)
old='<p data-i18n="k88">Penyusunan annual report dan sustainability report, dari pengumpulan data dan penulisan hingga desain.</p> <ul><li data-i18n="k89">Annual report</li><li data-i18n="k90">Sustainability report</li></ul> </div>'
if old not in s:
    old=re.search(r'<p data-i18n="k88">.*?</ul>\s*</div>',s,re.S).group(0)
new='<p data-i18n="k88">Laporan tahunan PT sesuai Permenkum 49/2025 sampai siap akta notaris, serta annual report dan sustainability report.</p> <ul><li data-i18n="k344">Laporan Tahunan PT</li><li data-i18n="k89">Annual report</li><li data-i18n="k90">Sustainability report</li></ul> <span class="svclinks"><a class="svclink" data-i18n="k343" href="/laporan-tahunan-pt/">Laporan Tahunan PT →</a></span> </div>'
if 'href="/laporan-tahunan-pt/"' not in s:
    s=s.replace(old,new,1)
    s=s.replace('"k88": "Preparation of annual and sustainability reports, from data gathering and writing through to design."','"k88": "Company annual reports under Permenkum 49/2025 through to the notarial deed, plus annual and sustainability reports.", "k343": "Company annual report →", "k344": "Company annual report"')
    s=s.replace('"k88": "编制年度报告和可持续发展报告，涵盖数据收集、撰写到设计。"','"k88": "依据第49/2025号法律部长条例编制公司年度报告直至公证契据，并编制年度报告和可持续发展报告。", "k343": "公司年度报告 →", "k344": "公司年度报告"')
    wr(p,s)

# ---------------- 5. footer link semua halaman ----------------
FL='<li><a href="/konsultan-kredit-bank/">Pengajuan Kredit Bank</a></li>'
for root,_,files in os.walk(FA):
    for f in files:
        if not f.endswith(".html"): continue
        q=os.path.join(root,f); t=rd(q)
        if FL in t and 'href="/laporan-tahunan-pt/">Laporan Tahunan PT</a></li>' not in t:
            wr(q,t.replace(FL,FL+'<li><a href="/laporan-tahunan-pt/">Laporan Tahunan PT</a></li>',1))

# ---------------- 6. sitemap & llms ----------------
p=P("sitemap.xml"); s=rd(p)
for u,pr in [(URL,"0.8"),(AURL,"0.7")]:
    if u not in s: s=s.replace("</urlset>",f"<url><loc>{u}</loc><lastmod>2026-10-25</lastmod><priority>{pr}</priority></url>\n</urlset>")
s=re.sub(r'(<loc>https://faindonesia.co.id/konsultan-persiapan-ipo/</loc><lastmod>)[^<]*',r'\g<1>2026-10-25',s)
s=re.sub(r'(<loc>https://faindonesia.co.id/artikel/</loc><lastmod>)[^<]*',r'\g<1>2026-10-25',s)
wr(p,s)
p=P("llms.txt"); s=rd(p)
if "laporan-tahunan-pt" not in s:
    s=s.rstrip()+f"\n\n## Kepatuhan korporasi\n- [Jasa Laporan Tahunan PT sesuai Permenkum 49/2025]({URL}) (laporan keuangan, laporan tahunan, draf keputusan RUPS, koordinasi notaris sampai SABH)\n- [{AT}]({AURL})\n"
    wr(p,s)
print("FA updated")
