# Dieksekusi di build.py setelah seo_city.py. Halaman per kawasan bisnis (contoh /kota/jakarta/sunter/ dan /kota/jakarta/sunter/kap/).
from kawasan import KAWASAN

CORE = ["kap", "kjpp", "pajak", "lk"]
CITY_IDX = {c[0]: c for c in CITIES}

def kw_faq(k, adm, city, prov):
    return [
     (f"Di mana mencari kantor akuntan publik (KAP) di {k}?", f"Chat Ananta, CPA di cariakuntan.com dan ceritakan kebutuhan Anda. Kami pilihkan KAP yang sesuai kelas rekanan bank, skala usaha, dan jadwal perusahaan Anda di {k}, {adm}. Konsultasi awal gratis."),
     (f"Ada jasa penilai atau KJPP yang melayani {k}?", f"Ada. Kami carikan KJPP rekanan bank tujuan Anda yang bisa menjadwalkan inspeksi aset di {k} dan sekitarnya untuk agunan kredit, revaluasi aset tetap, atau penilaian bisnis."),
     (f"Berapa biaya audit KAP untuk perusahaan di {k}?", "Biaya audit bergantung pada total aset, jumlah transaksi, kondisi pembukuan, dan kelas KAP yang diminta. Kisaran biaya kami sampaikan setelah melihat laporan keuangan terakhir Anda, sebelum Anda berkomitmen."),
     (f"Saya butuh konsultan pajak di {k}, bisa dibantu?", "Bisa. Kami hubungkan dengan konsultan pajak berizin untuk SPT Tahunan badan, Coretax, pemeriksaan, restitusi, dan perencanaan pajak."),
     (f"Siapa yang bisa menyusun laporan keuangan perusahaan di {k}?", f"Kantor Jasa Akuntansi (KJA) dan akuntan berpraktik di jaringan kami menyusun laporan keuangan sesuai SAK EMKM, SAK EP, atau PSAK untuk usaha di {k}, siap untuk bank, pajak, dan audit."),
    ]

by_city = {}
for kw in KAWASAN:
    by_city.setdefault(kw[1], []).append(kw)

for kname, city, adm, secs, note in KAWASAN:
    if city not in CITY_IDX: continue
    _, prov, reg, csecs, cnote = CITY_IDX[city]
    cs, ks = slug(city), slug(kname)
    base = f"/kota/{cs}/{ks}/"
    disp = f"{kname}, {adm}"
    sibs = [x for x in by_city[city] if x[0] != kname]
    sib_links = " ".join(f'<a href="/kota/{cs}/{slug(x[0])}/">{x[0]}</a>' for x in sibs)
    faq = kw_faq(kname, adm, city, prov)
    url = DOMAIN + base
    title = f"KAP, Jasa Penilai (KJPP) &amp; Konsultan Pajak {kname}, {adm} | cariakuntan.com"
    desc = f"Cari kantor akuntan publik (KAP), jasa penilai KJPP, konsultan pajak, dan jasa laporan keuangan di {kname}, {adm}. Sesuai syarat bank dan regulator. Konsultasi awal gratis."
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"ProfessionalService","name":f"cariakuntan.com {kname}","url":url,"description":desc,
         "areaServed":{"@type":"Place","name":kname,"containedInPlace":{"@type":"City","name":city}},
         "knowsAbout":["Kantor Akuntan Publik","Jasa Audit","KJPP","Jasa Penilai","Konsultan Pajak","Penyusunan Laporan Keuangan"]},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Beranda","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":city,"item":f"{DOMAIN}/kota/{cs}/"},{"@type":"ListItem","position":3,"name":kname,"item":url}]}]}
    msg = f"Selamat siang Pak Ananta, kami dari {kname} ({adm}) membutuhkan KAP / KJPP / konsultan pajak / penyusunan laporan keuangan."
    jump = " ".join(f'<a href="{base}{SV[k][1]}/">{SV[k][2]} {kname}</a>' for k in CORE)
    overview = tblx(["Kebutuhan", "Siapa yang mengerjakan", "Contoh di " + kname], [
        ("Audit laporan keuangan", "KAP (akuntan publik)", (hooks("kap", secs) or "perusahaan yang mengajukan kredit").split("; ")[0]),
        ("Penilaian aset dan bisnis", "KJPP (jasa penilai publik)", (hooks("kjpp", secs) or "agunan kredit").split("; ")[0]),
        ("Pajak badan dan pemeriksaan", "Konsultan pajak berizin", (hooks("pajak", secs) or "SPT Tahunan badan").split("; ")[0]),
        ("Penyusunan laporan keuangan", "KJA dan akuntan berpraktik", (hooks("lk", secs) or "usaha yang belum punya LK").split("; ")[0])])
    secs_html = "".join(svc_section(k, kname, f"{adm}, {prov}", secs) for k in CORE)
    html = head(title, desc, url, extra=ldtag(ld)) + header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kota/">Wilayah</a> / <a href="/kota/{cs}/">{city}</a> / {kname}</p>
  <p class="label" style="margin-top:14px">{adm}, {prov}</p>
  <h1>KAP, Jasa Penilai (KJPP), Konsultan Pajak, dan Jasa Laporan Keuangan di {kname}</h1>
  <p class="sub">{kname} adalah {note}. Kami menghubungkan perusahaan di {kname} dan sekitarnya dengan kantor akuntan publik, KJPP, konsultan pajak, dan Kantor Jasa Akuntansi yang memenuhi syarat bank, regulator, atau investor.</p>
  <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(msg)}" target="_blank" rel="noopener">Chat Ananta, CPA</a><span style="color:var(--muted);font-size:.9rem">Diskusi awal tanpa biaya</span></div>
  <div class="citylist" style="margin-top:18px">{jump}</div>
  <div class="prose"><h2>Siapa Mengerjakan Apa di {kname}</h2></div>
  {overview}
  <div class="prose">{secs_html}<h2>KAP Sesuai Klasifikasi Bank</h2><p>Sampaikan kriteria bank Anda, kami cocokkan dengan KAP yang memenuhinya.</p></div>
  {TRUST}
  <div class="prose"><h2>Tanya Jawab: Akuntan dan Penilai di {kname}</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in faq)}</div>
  <div class="more"><h3>Kawasan Lain di {city}</h3><div class="citylist"><a href="/kota/{cs}/">Semua {city}</a> {sib_links}</div></div>
  {fa_box(city, kname)}
</main>
''' + footer(ID)
    write(base, html); urls.append(base)

    for k in CORE:
        _, sl, short, stitle, syn, wak = SV[k]
        u2 = f"{DOMAIN}{base}{sl}/"
        t2 = f"{stitle} di {kname}, {adm} | cariakuntan.com"
        d2 = f"Cari {syn} di {kname}, {adm}. Dipilihkan sesuai syarat bank, regulator, atau investor. Chat Ananta, CPA, konsultasi awal gratis."
        body = BODY[k](kname, f"{adm}, {prov}"); hk = hooks(k, secs)
        q2 = [faq[{"kap":0,"kjpp":1,"pajak":3,"lk":4}[k]], (f"Berapa biaya {short} di {kname}?", faq[2][1] if k == "kap" else "Biaya bergantung pada skala usaha, kondisi dokumen, dan tenggat yang diminta. Kisaran biaya kami sampaikan setelah melihat data Anda, sebelum Anda berkomitmen.")]
        ld2 = {"@context":"https://schema.org","@graph":[
            {"@type":"Service","name":f"{stitle} di {kname}","serviceType":stitle,"areaServed":{"@type":"Place","name":f"{kname}, {adm}"},"provider":{"@type":"ProfessionalService","name":"cariakuntan.com","url":DOMAIN+"/"},"url":u2,"description":d2},
            {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in q2]},
            {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Beranda","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":city,"item":f"{DOMAIN}/kota/{cs}/"},{"@type":"ListItem","position":3,"name":kname,"item":url},{"@type":"ListItem","position":4,"name":short,"item":u2}]}]}
        others = " ".join(f'<a href="{base}{SV[o][1]}/">{SV[o][2]} {kname}</a>' for o in CORE if o != k)
        sibsvc = " ".join(f'<a href="/kota/{cs}/{slug(x[0])}/{sl}/">{short} {x[0]}</a>' for x in sibs[:10])
        m2 = f"Selamat siang Pak Ananta, kami dari {kname} ({adm}) sedang mencari {wak}."
        h2 = head(t2, d2, u2, extra=ldtag(ld2)) + header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kota/{cs}/">{city}</a> / <a href="{base}">{kname}</a> / {short}</p>
  <p class="label" style="margin-top:14px">{disp}</p>
  <h1>{stitle} di {kname}</h1>
  <p class="sub">Cari {syn} di {kname}? Ceritakan kebutuhan Anda, kami pilihkan kantor yang sesuai syarat bank, regulator, atau investor, lengkap dengan perkiraan jadwal dan biaya.</p>
  <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(m2)}" target="_blank" rel="noopener">Chat Ananta, CPA</a><span style="color:var(--muted);font-size:.9rem">Diskusi awal tanpa biaya</span></div>
  <div class="prose"><h2>Kapan Perusahaan di {kname} Membutuhkan {short}</h2><p>{body[0]}</p>{f"<p>{kname} dikenal sebagai {note}. Di sini, {'objek yang paling sering dinilai adalah' if k=='kjpp' else 'yang paling sering menghubungi kami adalah'} {hk}.</p>" if hk else ""}</div>
  {tblx(["Situasi", "Yang dikerjakan", "Perkiraan waktu"], TABLE[k])}
  <div class="prose"><h2>Cara Kami Memilihkan {short} untuk {kname}</h2><p>{body[1]}</p><p>{body[2]}</p>
    <h2>Alurnya</h2><p>1. Anda chat dan kirim laporan keuangan terakhir atau gambaran kebutuhan. 2. Kami petakan syarat bank atau regulator. 3. Kami ajukan kantor yang cocok beserta kisaran biaya dan jadwal. 4. Anda memutuskan, kami dampingi sampai selesai.</p>
    {"<h2>KAP Sesuai Klasifikasi Bank</h2>" if k=="kap" else ""}</div>
  {TRUST if k=="kap" else ""}
  <div class="prose"><h2>Tanya Jawab</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in q2)}</div>
  <div class="more"><h3>Layanan Lain di {kname}</h3><div class="citylist">{others} <a href="/kota/{cs}/{sl}/">{short} {city}</a></div></div>
  <div class="more"><h3>{short} di Kawasan Lain {city}</h3><div class="citylist">{sibsvc}</div></div>
  {fa_box(city, kname)}
</main>
''' + footer(ID)
        write(f"{base}{sl}/", h2); urls.append(f"{base}{sl}/")

# blok "Kawasan" di halaman kota induk dan halaman layanan kota
for city, kws in by_city.items():
    if city not in CITY_IDX: continue
    cs = slug(city)
    for sub, label in [("", "Kawasan Bisnis di " + city)] + [(SV[k][1] + "/", f"{SV[k][2]} per Kawasan di {city}") for k in CORE]:
        pth = os.path.join(SITE, "kota", cs, sub, "index.html")
        if not os.path.exists(pth): continue
        t = open(pth, encoding="utf-8").read()
        if 'id="kawasan"' in t: continue
        links = " ".join(f'<a href="/kota/{cs}/{slug(x[0])}/{sub}">{(SV[[k for k in CORE if SV[k][1]+"/"==sub][0]][2] + " ") if sub else ""}{x[0]}</a>' for x in kws)
        blk = f'<div class="more" id="kawasan"><h3>{label}</h3><div class="citylist">{links}</div></div>\n'
        t = t.replace("</main>", blk + "</main>", 1)
        open(pth, "w", encoding="utf-8").write(t)
