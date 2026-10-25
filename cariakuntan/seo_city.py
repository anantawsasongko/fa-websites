# Dieksekusi di dalam build.py (exec) menggantikan loop halaman kota lama.
# Target kata kunci per kota: KAP / kantor akuntan publik / jasa audit, KJPP / jasa penilai,
# konsultan pajak, jasa penyusunan laporan keuangan / pembukuan / KJA.

SERVICES = [
 # key, slug, label pendek, judul layanan, sinonim untuk teks, kata kunci WA
 ("kap", "kap", "KAP", "Kantor Akuntan Publik (KAP) dan Jasa Audit", "kantor akuntan publik (KAP), auditor, dan jasa audit laporan keuangan", "KAP / audit"),
 ("kjpp", "kjpp", "KJPP", "Jasa Penilai dan KJPP", "Kantor Jasa Penilai Publik (KJPP), appraisal aset, dan penilaian bisnis", "KJPP / penilaian aset"),
 ("pajak", "konsultan-pajak", "Konsultan Pajak", "Konsultan Pajak", "konsultan pajak berizin (KKP), pendampingan SPT, Coretax, dan pemeriksaan pajak", "konsultan pajak"),
 ("lk", "jasa-laporan-keuangan", "Jasa Laporan Keuangan", "Jasa Penyusunan Laporan Keuangan", "jasa penyusunan laporan keuangan, pembukuan, dan Kantor Jasa Akuntansi (KJA)", "penyusunan laporan keuangan"),
 ("ltp", "laporan-tahunan-pt", "Laporan Tahunan PT", "Jasa Laporan Tahunan PT (Permenkum 49/2025)", "jasa penyusunan laporan tahunan PT untuk akta notaris dan SABH sesuai Permenkum 49/2025", "laporan tahunan PT untuk akta notaris (Permenkum 49/2025)"),
]
def has_page(city, key):
    return True
SV = {s[0]: s for s in SERVICES}

PRIORITY = ["Malang","Surabaya","Batam","Jakarta","Sidoarjo","Denpasar","Bandung","Semarang","Medan",
            "Makassar","Balikpapan","Yogyakarta","Tangerang","Bekasi","Pekanbaru","Palembang","Jember","Pasuruan"]

# kalimat per layanan x sektor, supaya isi tiap kota berbeda sesuai ekonominya
HOOK = {
 "kap": {"dagang":"distributor yang mengajukan kredit modal kerja","manufaktur":"pabrik yang mengajukan kredit investasi mesin","tambang":"kontraktor tambang yang diminta laporan audited oleh pemberi kerja","smelter":"pemasok kawasan smelter yang ikut tender","sawit":"grup perkebunan dengan kewajiban audit tahunan","perikanan":"usaha cold storage yang mengakses pembiayaan ekspor","wisata":"hotel dan vila PMA yang wajib laporan audited","migas":"penunjang migas yang perlu kualifikasi vendor","konstruksi":"kontraktor yang butuh LK audited untuk SBU dan tender","properti":"pengembang yang mengajukan kredit konstruksi","kesehatan":"rumah sakit yang baru pertama kali diaudit","bpr":"BPR dan koperasi dengan audit wajib regulator","pendidikan":"yayasan pendidikan dengan audit dana hibah","logistik":"perusahaan logistik yang membiayai armada","bumd":"BUMD dan mitra pemerintah daerah"},
 "kjpp": {"dagang":"gudang dan ruko yang dijadikan agunan","manufaktur":"mesin dan bangunan pabrik","tambang":"alat berat dan izin usaha","smelter":"aset kontraktor kawasan industri","sawit":"lahan dan tanaman perkebunan","perikanan":"kapal dan cold storage","wisata":"hotel, vila, dan tanah di kawasan wisata","migas":"peralatan penunjang migas","konstruksi":"alat berat kontraktor","properti":"tanah, ruko, dan proyek properti","kesehatan":"gedung dan alat kesehatan rumah sakit","bpr":"agunan kredit nasabah BPR","pendidikan":"tanah dan gedung yayasan","logistik":"armada truk dan kapal","bumd":"aset BUMD dan pemerintah daerah"},
 "pajak": {"dagang":"pedagang dengan omzet besar dan PPN","manufaktur":"pabrik dengan restitusi PPN","tambang":"jasa tambang dengan PPh potong pungut","smelter":"pemasok kawasan berikat","sawit":"perkebunan dengan pemeriksaan pajak","perikanan":"eksportir hasil laut","wisata":"hotel dan restoran dengan pajak daerah","migas":"vendor migas","konstruksi":"kontraktor dengan PPh final jasa konstruksi","properti":"pengembang dengan PPh final dan BPHTB","kesehatan":"rumah sakit dan klinik","bpr":"BPR dan koperasi","pendidikan":"yayasan dengan fasilitas pajak","logistik":"perusahaan logistik","bumd":"BUMD"},
 "ltp": {"dagang":"PT distributor yang mau ganti direksi atau jual saham","manufaktur":"PT pabrik dengan pemegang saham lebih dari satu","tambang":"PT jasa tambang yang sedang ganti pengurus","smelter":"PT pemasok kawasan industri","sawit":"PT perkebunan keluarga","perikanan":"PT perikanan dan cold storage","wisata":"PT pengelola hotel dan vila","migas":"PT penunjang migas","konstruksi":"PT kontraktor yang perlu data AHU bersih untuk tender","properti":"PT pengembang dengan banyak pemegang saham","kesehatan":"PT rumah sakit dan klinik","bpr":"PT BPR","pendidikan":"PT pengelola sekolah dan kampus","logistik":"PT logistik","bumd":"Perseroda BUMD"},
 "lk": {"dagang":"toko dan distributor dengan persediaan banyak","manufaktur":"pabrik dengan perhitungan harga pokok","tambang":"jasa tambang","smelter":"kontraktor kawasan industri","sawit":"perkebunan dan agribisnis","perikanan":"usaha perikanan","wisata":"hotel, restoran, dan kafe","migas":"penunjang migas","konstruksi":"kontraktor dengan proyek berjalan","properti":"pengembang dengan unit inden","kesehatan":"rumah sakit dan klinik","bpr":"koperasi","pendidikan":"yayasan dan sekolah","logistik":"usaha logistik","bumd":"BUMD"},
}

BODY = {
 "kap": lambda c, p: [
   f"Perusahaan di {c} biasanya mencari KAP karena tiga hal: diminta bank saat mengajukan atau memperpanjang kredit, wajib audit karena aset atau omzet minimal Rp50 miliar (UU PT Pasal 68), atau syarat tender, investor, dan pemegang saham asing.",
   f"Bank memakai klasifikasi rekanan: kelas A (Big 4 dan jaringan internasional), kelas B (KAP terdaftar OJK), dan kelas C (KAP berizin Kementerian Keuangan). Kami cocokkan KAP untuk perusahaan di {c} dengan kelas yang diminta bank Anda, sehingga laporan audited tidak ditolak.",
   "Selain audit umum, tersedia review, agreed-upon procedures (AUP), dan audit pertama untuk perusahaan yang belum pernah diaudit."],
 "kjpp": lambda c, p: [
   f"Penilaian KJPP di {c} paling sering dibutuhkan untuk agunan kredit bank, revaluasi aset tetap (PSAK 216), jual beli atau merger, dan penyertaan modal.",
   f"Bank hanya menerima laporan dari KJPP rekanan. Kami carikan KJPP yang sudah menjadi rekanan bank tujuan Anda dan bisa menjadwalkan inspeksi lapangan di {c} dan sekitarnya.",
   "Objek penilaian: tanah dan bangunan, mesin, alat berat, kendaraan, persediaan, hingga nilai saham dan bisnis."],
 "pajak": lambda c, p: [
   f"Pemilik usaha di {c} mencari konsultan pajak untuk SPT Tahunan badan, transisi Coretax, pemeriksaan dan surat teguran, restitusi PPN, keberatan, serta perencanaan pajak sebelum ekspansi.",
   f"Kami hubungkan dengan konsultan pajak berizin (KKP) yang terbiasa menangani perusahaan sejenis di {p}, dan yang bisa berkoordinasi dengan KAP bila laporan Anda juga diaudit.",
   "Untuk PMA, tersedia pendampingan transfer pricing, tax treaty, dan pelaporan kepada investor asing."],
 "ltp": lambda c, p: [
   f"Sejak Permenkum 49/2025, persetujuan RUPS atas laporan tahunan PT di {c} wajib dituangkan dalam akta notaris lalu disampaikan lewat SABH paling lama 30 hari sejak akta. Kewajiban ini berlaku untuk PT persekutuan modal, termasuk PT tertutup yang tidak wajib audit.",
   f"Kami bantu PT di {c} menyusun laporan keuangan lengkap dengan catatan, laporan tahunan sesuai isi minimal Pasal 16, dan draf keputusan RUPS atau sirkuler, sampai siap dibawa ke notaris pilihan Anda di {p}.",
   "Bila tidak dilaporkan, perseroan bisa ditegur lalu diblokir aksesnya di SABH, sehingga ganti direksi, jual beli saham, dan perubahan data tertahan."],
 "lk": lambda c, p: [
   f"Banyak usaha di {c} punya omzet miliaran tapi belum punya laporan keuangan yang rapi. Kami bantu susun laporan keuangan sesuai SAK EMKM, SAK EP, atau PSAK, dari pembukuan bulanan sampai laporan tahunan lengkap dengan catatan.",
   f"Penyusunan dikerjakan bersama Kantor Jasa Akuntansi (KJA) dan akuntan berpraktik, sehingga laporan siap dipakai untuk kredit bank, SPT, tender, atau diaudit KAP. Bisa juga tutup buku tahunan saja untuk usaha di {c} yang pembukuannya tertinggal beberapa tahun.",
   "Bisa memakai software akuntansi apa pun, atau mulai dari template Excel."],
}

TABLE = {
 "kap": [("Kredit bank baru atau perpanjangan","Laporan audited, kelas KAP sesuai bank","4 sampai 8 minggu"),("Wajib audit UU PT (aset/omzet ≥ Rp50 miliar)","Audit umum tahunan","Sebelum RUPS"),("Belum pernah diaudit","Audit pertama, saldo awal diperiksa","6 sampai 10 minggu"),("Permintaan investor atau mitra","Audit, review, atau AUP","2 sampai 6 minggu")],
 "kjpp": [("Agunan kredit","Penilaian tanah, bangunan, mesin","1 sampai 3 minggu"),("Revaluasi aset tetap","Laporan penilaian untuk PSAK 216","2 sampai 4 minggu"),("Merger, akuisisi, investor","Penilaian bisnis dan saham","3 sampai 6 minggu"),("Asuransi atau sengketa","Penilaian objek tertentu","1 sampai 3 minggu")],
 "pajak": [("SPT Tahunan badan","Penyusunan dan review SPT","Sebelum 30 April"),("Pemeriksaan atau SP2DK","Pendampingan dan tanggapan","Sesuai tenggat surat"),("Restitusi PPN","Persiapan dokumen dan pendampingan","Sesuai proses DJP"),("Ekspansi atau PMA","Perencanaan dan struktur pajak","Sebelum transaksi")],
 "ltp": [("Tahun buku 2025 belum dilaporkan","LK, laporan tahunan, draf keputusan RUPS","1 sampai 3 minggu"),("LK sudah ada, laporan tahunan belum","Laporan tahunan dan draf keputusan","3 sampai 7 hari"),("PT wajib audit","Koordinasi KAP lalu laporan tahunan","4 sampai 8 minggu"),("Mau ganti direksi atau jual saham","Laporan tahunan dulu agar SABH tidak terblokir","Segera")],
 "lk": [("Butuh LK untuk kredit bank","Penyusunan LK tahunan lengkap","2 sampai 4 minggu"),("Pembukuan tertinggal","Tutup buku dan rekonsiliasi","3 sampai 8 minggu"),("Persiapan audit","LK, lead schedule, dokumen pendukung","2 sampai 6 minggu"),("Pembukuan rutin","Laporan bulanan","Setiap bulan")],
}

def tblx(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "".join("<tr>" + f'<th scope="row">{r[0]}</th>' + "".join(f"<td>{x}</td>" for x in r[1:]) + "</tr>" for r in rows)
    return f'<div class="tblwrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'

def hooks(key, secs):
    h = [HOOK[key][x] for x in secs if x in HOOK[key]]
    if not h: return ""
    return "; ".join(h[:-1]) + ("; serta " if len(h) > 1 else "") + h[-1]

def city_faq(c, p, secs):
    return [
     (f"Di mana mencari KAP di {c}?", f"Ceritakan kebutuhan Anda melalui WhatsApp ke Ananta, CPA di cariakuntan.com. Kami pilihkan KAP yang sesuai kelas rekanan bank, skala usaha, dan jadwal Anda di {c}, {p}. Konsultasi awal gratis."),
     (f"Berapa biaya audit KAP di {c}?", "Biaya audit bergantung pada total aset, jumlah transaksi, kondisi pembukuan, dan kelas KAP yang diminta. Kami sampaikan kisaran biaya setelah melihat laporan keuangan terakhir Anda, sebelum Anda berkomitmen."),
     (f"Apakah ada KJPP untuk penilaian aset di {c}?", f"Ada. Kami carikan KJPP rekanan bank tujuan Anda yang bisa menjadwalkan inspeksi di {c} dan sekitarnya untuk agunan kredit, revaluasi aset, atau penilaian bisnis."),
     (f"Saya butuh konsultan pajak di {c}, bisa dibantu?", "Bisa. Kami hubungkan dengan konsultan pajak berizin untuk SPT Tahunan badan, Coretax, pemeriksaan pajak, restitusi, dan perencanaan pajak."),
     (f"Apakah PT di {c} wajib menyampaikan laporan tahunan lewat notaris?", "Ya, untuk PT persekutuan modal sesuai Permenkum 49/2025: persetujuan RUPS dituangkan dalam akta notaris dan disampaikan lewat SABH paling lama 30 hari sejak akta. Kami siapkan laporan keuangan dan laporan tahunannya sampai siap dibawa ke notaris."),
     (f"Siapa yang bisa menyusun laporan keuangan perusahaan di {c}?", "Kantor Jasa Akuntansi (KJA) dan akuntan berpraktik di jaringan kami menyusun laporan keuangan sesuai SAK EMKM, SAK EP, atau PSAK, sehingga siap untuk bank, pajak, dan audit."),
    ]

def svc_section(key, c, p, secs, anchor=True, h="h2"):
    k, sl, short, title, syn, _ = SV[key]
    hk = hooks(key, secs)
    paras = BODY[key](c, p)
    lead = "objek yang paling sering dinilai adalah" if key == "kjpp" else "kebutuhan ini paling sering datang dari"
    extra = f"<p>Di {c}, {lead} {hk}.</p>" if hk else ""
    return (f'<{h} id="{sl}"' + '>' + f'{title} di {c}</{h}>'
            + f"<p>{paras[0]}</p>{extra}<p>{paras[1]}</p><p>{paras[2]}</p>")

def popular_links(cities, keys=("kap","kjpp","pajak","lk","ltp")):
    out = []
    for c in cities:
        for key in keys:
            k, sl, short, *_ = SV[key]
            href = f"/kota/{slug(c)}/{sl}/" if has_page(c, key) else f"/kota/{slug(c)}/#{sl}"
            out.append(f'<a href="{href}">{short} {c}</a>')
    return out

TRUST = tblx(["Kelas", "Jenis KAP", "Umumnya diminta untuk"], [
    ("A", "Big 4 dan jaringan internasional", "Fasilitas besar, perusahaan terbuka, investor asing"),
    ("B", "KAP terdaftar OJK", "Kredit menengah, lembaga jasa keuangan"),
    ("C", "KAP berizin Kementerian Keuangan", "Kredit UKM, wajib audit UU PT, tender")])

from kawasan import BOOST, KAWASAN as _KW
def boost_html(c, short=None):
    if c not in BOOST: return ""
    kws = [k for k in _KW if k[1] == c]
    ps = "".join(f"<p>{x}</p>" for x in BOOST[c])
    kl = ("<p>Kawasan yang sering kami layani di " + c + ": " + ", ".join(f'<a href="/kota/{slug(c)}/{slug(k[0])}/' + (SV[[s_ for s_ in SV if SV[s_][2]==short][0]][1] + "/" if short else "") + f'">{k[0]}</a>' for k in kws) + ".</p>") if kws else ""
    return f'<div class="prose"><h2>Mengenal Pasar {"" if not short else short + " "}{c}</h2>{ps}{kl}</div>'

def fa_box(c, area=None):
    w = f"https://faindonesia.co.id/wilayah/{slug(c)}/" + (f"{slug(area)}/" if area else "")
    return (f'<div class="more"><h3>Butuh Pendampingan sampai Dana Cair?</h3><p style="color:var(--muted);margin:0 0 10px">Untuk pendampingan laporan keuangan, kredit bank, investor, IPO, konsultan rumah sakit, dan unit cost di {area or c}, lihat juga FA Indonesia.</p>'
            f'<div class="citylist"><a href="{w}">Konsultan Keuangan {area or c}</a><a href="https://faindonesia.co.id/konsultan-rumah-sakit/{slug(c)}/">Konsultan Rumah Sakit {c}</a><a href="https://faindonesia.co.id/konsultan-unit-cost-rumah-sakit/{slug(c)}/">Konsultan Unit Cost {c}</a><a href="https://faindonesia.co.id/konsultan-kredit-bank/">Konsultan Kredit Bank</a></div></div>')

# ---------------- halaman kota ----------------
for name, prov, reg, secs, note in CITIES:
    s = slug(name); rname, rline = REGIONS[reg]
    near = sorted([c for c in CITIES if c[2]==reg and c[0]!=name], key=lambda c: c[1]!=prov)[:8]
    nlinks = " ".join(f'<a href="/kota/{slug(c[0])}/">{c[0]}</a>' for c in near)
    msg = f"Selamat siang Pak Ananta, kami dari {name} membutuhkan KAP / KJPP / konsultan pajak / penyusunan laporan keuangan."
    title = f"KAP, KJPP, Konsultan Pajak &amp; Jasa Laporan Keuangan {name} | cariakuntan.com"
    desc = f"Cari KAP (akuntan publik), KJPP, konsultan pajak, dan jasa penyusunan laporan keuangan di {name}, {prov}. Sesuai kelas rekanan bank, PMDN dan PMA. Konsultasi awal gratis."
    url = f"{DOMAIN}/kota/{s}/"
    faq = city_faq(name, prov, secs)
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"ProfessionalService","name":f"cariakuntan.com {name}","url":url,"description":desc,
         "areaServed":{"@type":"City","name":name,"containedInPlace":{"@type":"AdministrativeArea","name":prov}},
         "knowsAbout":["Kantor Akuntan Publik","Jasa Audit","KJPP","Penilaian Aset","Konsultan Pajak","Penyusunan Laporan Keuangan","Kantor Jasa Akuntansi"],
         "hasOfferCatalog":{"@type":"OfferCatalog","name":f"Layanan di {name}","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":f"{SV[k][3]} di {name}"}} for k in SV]}},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Beranda","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":"Wilayah","item":DOMAIN+"/kota/"},{"@type":"ListItem","position":3,"name":name,"item":url}]}]}
    html = head(title, desc, url, extra=ldtag(ld))
    pri = name in PRIORITY
    jump = " ".join(f'<a href="/kota/{s}/{SV[k][1]}/">{SV[k][2]} {name}</a>' if has_page(name, k) else f'<a href="#{SV[k][1]}">{SV[k][2]} {name}</a>' for k in SV)
    overview = tblx(["Kebutuhan", "Siapa yang mengerjakan", "Contoh di " + name], [
        ("Audit laporan keuangan", "KAP (akuntan publik)", (hooks("kap", secs) or "perusahaan yang mengajukan kredit").split("; ")[0]),
        ("Penilaian aset dan bisnis", "KJPP (penilai publik)", (hooks("kjpp", secs) or "agunan kredit").split("; ")[0]),
        ("Pajak badan dan pemeriksaan", "Konsultan pajak berizin", (hooks("pajak", secs) or "SPT Tahunan badan").split("; ")[0]),
        ("Penyusunan laporan keuangan", "KJA dan akuntan berpraktik", (hooks("lk", secs) or "usaha yang belum punya LK").split("; ")[0]),
        ("Laporan tahunan PT (Permenkum 49/2025)", "Penyusun laporan, lalu akta notaris", (hooks("ltp", secs) or "PT yang belum melapor ke SABH").split("; ")[0])])
    secs_html = "".join(svc_section(k, name, prov, secs) for k in SV)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)
    html += header(ID,"home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kota/">Wilayah</a> / <a href="/kota/#{reg}">{rname}</a></p>
  <p class="label" style="margin-top:14px">{prov}</p>
  <h1>KAP, KJPP, Konsultan Pajak, dan Jasa Laporan Keuangan di {name}</h1>
  <p class="sub">{name} adalah {note}. Kami menghubungkan perusahaan di {name} dengan kantor akuntan publik (KAP), KJPP, konsultan pajak, dan Kantor Jasa Akuntansi yang memenuhi persyaratan bank, regulator, atau investor.</p>
  <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(msg)}" target="_blank" rel="noopener">Chat Ananta, CPA</a><span style="color:var(--muted);font-size:.9rem">Diskusi awal tanpa biaya</span></div>
  <div class="citylist" style="margin-top:18px">{jump}</div>
  {boost_html(name)}
  <div class="prose"><h2>Siapa Mengerjakan Apa di {name}</h2></div>
  {overview}
  <div class="prose"><h2>Kebutuhan yang Paling Sering di {name}</h2></div>
  <div class="sectors">{"".join(sector_html(x) for x in secs)}</div>
  <div class="prose">{secs_html}
    <h2>KAP Sesuai Klasifikasi Bank</h2>
    <p>Sampaikan kriteria bank Anda, kami cocokkan dengan KAP yang memenuhinya.</p>
  </div>
  {TRUST}
  <div class="prose">
    <h2>Melayani {name} dan {rname}</h2>
    <p>{rline} Untuk perusahaan beraset Rp5 sampai 10 miliar, biaya disesuaikan dengan skala usaha. Untuk korporasi hingga Rp2 triliun, termasuk PMA, kantor dan tim dipilih sesuai kompleksitasnya, termasuk audit dan agreed-upon procedures.</p>
    <h2>Tanya Jawab: Akuntan dan Penilai di {name}</h2>
    {faq_html}
  </div>
  <div class="more"><h3>Kota Lain di {rname}</h3><div class="citylist">{nlinks}</div></div>
  {fa_box(name)}
</main>
''' + footer(ID)
    write(f"/kota/{s}/", html); urls.append(f"/kota/{s}/")

    # ---------- halaman layanan x kota (kota prioritas) ----------
    if True:
        for k in [k for k in SV if has_page(name, k)]:
            _, sl, short, stitle, syn, wak = SV[k]
            others = " ".join((f'<a href="/kota/{s}/{SV[o][1]}/">{SV[o][2]} {name}</a>' if has_page(name, o) else f'<a href="/kota/{s}/#{SV[o][1]}">{SV[o][2]} {name}</a>') for o in SV if o != k)
            nearsvc = " ".join(f'<a href="/kota/{slug(c[0])}/{sl}/">{short} {c[0]}</a>' if has_page(c[0], k) else f'<a href="/kota/{slug(c[0])}/#{sl}">{short} {c[0]}</a>' for c in near[:6])
            u2 = f"{DOMAIN}/kota/{s}/{sl}/"
            t2 = f"{stitle} di {name}: {short} Terpercaya Sesuai Kebutuhan Bank | cariakuntan.com"
            if len(t2) > 95: t2 = f"{stitle} di {name} | cariakuntan.com"
            d2 = f"Cari {syn} di {name}, {prov}. Dipilihkan sesuai syarat bank, regulator, atau investor. Chat Ananta, CPA, konsultasi awal gratis."
            q2 = [x for x in faq if (k!="ltp" and short.split()[0] in x[0]) or (k=="lk" and "laporan keuangan" in x[0]) or (k=="ltp" and "laporan tahunan" in x[0])]
            q2.append((f"Berapa biaya {short} di {name}?", "Biaya bergantung pada skala usaha, kondisi dokumen, dan tenggat yang diminta. Kami sampaikan kisaran biaya setelah melihat data Anda, sebelum Anda berkomitmen.") if k != "kap" else faq[1])
            ld2 = {"@context":"https://schema.org","@graph":[
                {"@type":"Service","name":f"{stitle} di {name}","serviceType":stitle,"areaServed":{"@type":"City","name":name},"provider":{"@type":"ProfessionalService","name":"cariakuntan.com","url":DOMAIN+"/"},"url":u2,"description":d2},
                {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in q2]},
                {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Beranda","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":name,"item":url},{"@type":"ListItem","position":3,"name":stitle,"item":u2}]}]}
            m2 = f"Selamat siang Pak Ananta, kami dari {name} sedang mencari {wak}."
            body = BODY[k](name, prov); hk = hooks(k, secs)
            h2 = head(t2, d2, u2, extra=ldtag(ld2))
            h2 += header(ID,"home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kota/">Wilayah</a> / <a href="/kota/{s}/">{name}</a></p>
  <p class="label" style="margin-top:14px">{name}, {prov}</p>
  <h1>{stitle} di {name}</h1>
  <p class="sub">Cari {syn} di {name}? Ceritakan kebutuhan Anda, kami pilihkan kantor yang sesuai syarat bank, regulator, atau investor, lengkap dengan perkiraan jadwal dan biaya.</p>
  <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(m2)}" target="_blank" rel="noopener">Chat Ananta, CPA</a><span style="color:var(--muted);font-size:.9rem">Diskusi awal tanpa biaya</span></div>
  <div class="prose"><h2>Kapan Perusahaan di {name} Membutuhkan {short}</h2><p>{body[0]}</p>{f"<p>Di {name}, {'objek yang paling sering dinilai adalah' if k=='kjpp' else 'yang paling sering menghubungi kami adalah'} {hk}.</p>" if hk else ""}</div>
  {tblx(["Situasi", "Yang dikerjakan", "Perkiraan waktu"], TABLE[k])}
  {boost_html(name, short)}
  <div class="prose"><h2>Cara Kami Memilihkan {short} untuk {name}</h2><p>{body[1]}</p><p>{body[2]}</p>
    <h2>Alurnya</h2><p>1. Anda chat dan kirim laporan keuangan terakhir atau gambaran kebutuhan. 2. Kami petakan syarat bank atau regulator. 3. Kami ajukan kantor yang cocok beserta kisaran biaya dan jadwal. 4. Anda memutuskan, kami dampingi sampai selesai.</p>
    {"<h2>KAP Sesuai Klasifikasi Bank</h2>" if k=="kap" else ""}</div>
  {TRUST if k=="kap" else ""}
  <div class="prose"><h2>Tanya Jawab</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in q2)}</div>
  <div class="more"><h3>Layanan Lain di {name}</h3><div class="citylist">{others}</div></div>
  <div class="more"><h3>{short} di Kota Sekitar</h3><div class="citylist">{nearsvc}</div></div>
  {fa_box(name)}
</main>
''' + footer(ID)
            write(f"/kota/{s}/{sl}/", h2); urls.append(f"/kota/{s}/{sl}/")

# ---------------- hub per layanan ----------------
for k in SV:
    _, sl, short, stitle, syn, wak = SV[k]
    rows = ""
    for r,(rname, rline) in REGIONS.items():
        ls = " ".join((f'<a href="/kota/{slug(c[0])}/{sl}/">{short} {c[0]}</a>' if has_page(c[0], k) else f'<a href="/kota/{slug(c[0])}/#{sl}">{short} {c[0]}</a>') for c in CITIES if c[2]==r)
        rows += f'<h2 id="{r}" style="margin-top:30px">{short} di {rname}</h2><div class="citylist">{ls}</div>'
    u3 = f"{DOMAIN}/layanan/{sl}/"
    t3 = f"{stitle} di Seluruh Indonesia, {len(CITIES)} Kota | cariakuntan.com"
    d3 = f"Cari {syn} di {len(CITIES)} kota, dari Aceh sampai Papua: Malang, Surabaya, Batam, Jakarta, Denpasar, Makassar, dan lainnya. Konsultasi awal gratis."
    ld3 = {"@context":"https://schema.org","@type":"Service","name":stitle,"serviceType":stitle,"areaServed":{"@type":"Country","name":"Indonesia"},"provider":{"@type":"ProfessionalService","name":"cariakuntan.com","url":DOMAIN+"/"},"url":u3}
    body = BODY[k]("kota Anda", "provinsi Anda")
    h3 = head(t3, d3, u3, extra=ldtag(ld3)) + header(ID,"home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kota/">Wilayah</a> / {short}</p>
  <h1>{stitle} di Seluruh Indonesia</h1>
  <p class="sub">{body[0]}</p>
  <div style="margin-top:22px"><a class="btn btn-wa arrow" href="{wa("Selamat siang Pak Ananta, kami sedang mencari " + wak + ".")}" target="_blank" rel="noopener">Chat Ananta, CPA</a></div>
  {tblx(["Situasi", "Yang dikerjakan", "Perkiraan waktu"], TABLE[k])}
  <div class="prose"><p>{body[1]}</p></div>
  {rows}
</main>
''' + footer(ID)
    write(f"/layanan/{sl}/", h3); urls.append(f"/layanan/{sl}/")
