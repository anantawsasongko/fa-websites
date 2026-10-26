# Dieksekusi build.py setelah seo_city.py dan seo_kawasan.py (exec, memakai helper yang sama).
# Target kata kunci: "cari KAP murah <kota>", "KAP murah <kota>", "jasa audit murah <kota>", "biaya audit KAP <kota>".
# Halaman: /kap-murah/ (hub) dan /kota/<kota>/kap-murah/ untuk setiap kota. Jujur: murah = fee sesuai skala dan tidak perlu audit ulang.

FA = "https://faindonesia.co.id"
HEMAT = [
 ("Kredit UKM atau perpanjangan kredit", "KAP berizin Kementerian Keuangan yang masuk daftar rekanan bank Anda", "Tanyakan kelas KAP ke bank dulu. Banyak fasilitas UKM cukup dengan KAP kelas C."),
 ("Wajib audit UU PT (aset atau omzet minimal Rp50 miliar)", "Audit umum tahunan oleh KAP berizin", "Jadwalkan di luar musim sibuk Januari sampai April."),
 ("Tender atau syarat mitra", "Audit umum, atau agreed-upon procedures (AUP) bila yang diminta hanya pos tertentu", "AUP biasanya lebih ringkas daripada audit penuh."),
 ("Lembaga jasa keuangan, IPO, investor besar", "KAP terdaftar OJK, sering kelas A atau B", "Tidak bisa dipaksa murah. Hematnya dari kesiapan data agar tidak ada audit ulang."),
]
CARA = [
 ("Rapikan laporan keuangan dulu", "Auditor menagih jam kerja. Neraca saldo yang belum rekonsiliasi, piutang tanpa rincian, dan aset tetap tanpa daftar membuat jam kerja membengkak."),
 ("Pilih kelas KAP sesuai kebutuhan", "Tidak semua kredit butuh KAP besar. Cocokkan dengan daftar rekanan bank, jangan membayar kelas yang tidak diminta."),
 ("Tentukan lingkup yang tepat", "Audit, reviu, kompilasi, atau AUP punya biaya berbeda. Pakai yang memang diminta pihak penerima laporan."),
 ("Hindari musim puncak", "Januari sampai April adalah musim audit. Penugasan di luar periode itu lebih mudah dinegosiasikan."),
 ("Kontrak beberapa tahun", "Penugasan berulang menurunkan biaya tahun kedua dan seterusnya karena auditor sudah memahami bisnis Anda."),
]
def murah_faq(c):
    return [
     (f"Apakah bijak memilih KAP murah di {c}?", "Bijak bila murahnya karena lingkup tepat, data rapi, dan kelas KAP sesuai kebutuhan. Tidak bijak bila murahnya karena prosedur audit dipangkas, karena laporan bisa ditolak bank atau investor dan Anda harus membayar audit ulang."),
     ("Apakah KAP dengan fee rendah tetap independen?", "Kode Etik Profesi Akuntan Publik memandang imbalan jasa yang terlalu rendah sebagai ancaman kepentingan pribadi terhadap kompetensi dan kecermatan profesional, karena sulit menjalankan prosedur sesuai standar dengan biaya tersebut. KAP yang dapat dipercaya akan menolak fee yang tidak memungkinkan prosedur memadai."),
     (f"Berapa biaya audit KAP di {c}?", "Bergantung pada total aset, jumlah transaksi, kerapian pembukuan, kelas KAP, dan tenggat. IAPI menerbitkan panduan penetapan imbalan jasa audit, dan fee yang terlalu rendah justru berisiko pada kualitas audit. Kisaran biaya kami sampaikan setelah melihat angka ringkas Anda, sebelum Anda berkomitmen."),
     (f"Apakah KAP murah di {c} tetap diterima bank?", "Bisa, asalkan KAP berizin Kementerian Keuangan dan masuk kelas rekanan yang diminta bank. Laporan dari KAP yang tidak sesuai daftar rekanan biasanya ditolak, sehingga Anda harus audit ulang dan biayanya jadi dua kali."),
     ("Bagaimana memastikan KAP berizin?", "Cek nama KAP dan akuntan publiknya di registri Kementerian Keuangan (PPPK) atau direktori IAPI. Untuk lembaga jasa keuangan dan emiten, pastikan juga terdaftar di OJK."),
     (f"Apakah KAP harus berkantor di {c}?", "Tidak harus. Banyak penugasan dikerjakan jarak jauh dengan kunjungan lapangan saat diperlukan, sehingga pilihan KAP lebih luas dan harga lebih kompetitif."),
    ]

def murah_body(c, prov, secs, note, near, kws):
    s = slug(c)
    hk = hooks("kap", secs)
    nl = " ".join(f'<a href="/kota/{slug(x[0])}/kap-murah/">KAP Murah {x[0]}</a>' for x in near[:8])
    kl = " ".join(f'<a href="/kota/{s}/{slug(k[0])}/kap/">KAP {k[0]}</a>' for k in kws)
    return f'''
  <div class="prose"><h2>KAP Murah di {c}: Apakah Bijak?</h2>
  <p>{c} adalah {note}. Mencari kantor akuntan publik yang murah di {c} itu wajar. Pertanyaannya, apakah murahnya karena efisien, atau karena prosedur audit dikurangi? Yang kedua sering berujung laporan ditolak bank atau investor, lalu audit ulang dan biayanya jadi dua kali. {f"Di {c}, yang paling sering mencari jasa audit adalah {hk}." if hk else ""}</p></div>
  <div class="prose"><h2>Apakah Cukup Independen dan Dapat Dipercaya?</h2>
  <p>Opini audit hanya bernilai bila auditornya independen dan prosedurnya memadai. Sebelum memilih karena harga, cek lima hal ini:</p>
  <ol><li><b>Izin aktif.</b> KAP dan akuntan publiknya terdaftar di Kementerian Keuangan (PPPK), dan terdaftar OJK bila laporan untuk lembaga jasa keuangan atau emiten.</li>
  <li><b>Masuk rekanan pihak penerima.</b> Banyak bank punya daftar dan kelas KAP rekanan.</li>
  <li><b>Fee masuk akal.</b> Kode Etik Profesi Akuntan Publik memandang imbalan jasa yang terlalu rendah sebagai ancaman terhadap kompetensi dan kecermatan profesional.</li>
  <li><b>Tidak ada hubungan yang mengganggu independensi.</b> Auditor tidak sekaligus menyusun laporan keuangan yang ia audit, tidak punya kepentingan keuangan atau keluarga dengan perusahaan.</li>
  <li><b>Rekam jejak.</b> Tidak sedang dikenai sanksi dan berpengalaman di industri Anda.</li></ol>
  <h2>Kapan Hemat Masih Bijak</h2></div>
  {tblx(["Kebutuhan", "Pilihan paling hemat yang tetap diterima", "Catatan"], HEMAT)}
  <div class="prose"><h2>5 Cara Menekan Biaya Audit di {c} tanpa Mengorbankan Kualitas</h2>
  <ol>{"".join(f"<li><b>{a}.</b> {b}</li>" for a, b in CARA)}</ol>
  <p>Belum punya laporan keuangan yang rapi? Susun dulu lewat <a href="/kota/{s}/jasa-laporan-keuangan/">jasa laporan keuangan {c}</a> atau pendampingan <a href="{FA}/jasa-penyusunan-laporan-keuangan/">FA Indonesia</a>, sehingga jam kerja auditor lebih sedikit.</p>
  <h2>Hati-hati dengan KAP yang Terlalu Murah</h2>
  <p>Penawaran jauh di bawah kewajaran sering berarti prosedur dipangkas. Akibatnya opini bisa dipertanyakan bank, investor, atau regulator. Selalu cek izin KAP dan akuntan publiknya, serta pastikan kelasnya sesuai daftar rekanan bank.</p>
  <p><a class="btn btn-line" href="/#cek">Cek Izin KAP di Registri Resmi</a></p>
  <h2>Diskusikan Dulu Kebutuhan Anda</h2>
  <p>Setiap kebutuhan audit berbeda: untuk bank yang mana, berapa plafonnya, atau untuk investor dan tender. Ceritakan dulu ke kami lewat chat, kami bantu menentukan lingkup dan kelas KAP yang memang diperlukan, lalu membandingkan beberapa KAP berizin. Diskusi awal gratis.</p>
  <h2>Cek Dulu Angka Anda, Gratis</h2>
  <p>Isi angka ringkas 3 tahun di <a href="/screening/">screening instan</a> untuk melihat rasio yang dibaca bank dan jalur IPO. Ingin tahu plafon kredit yang realistis? Coba <a href="{FA}/cek-kapasitas-kredit/">Cek Kredit dan Pendanaan</a> di FA Indonesia.</p></div>
  {f'<div class="more"><h3>KAP per Kawasan di {c}</h3><div class="citylist">{kl}</div></div>' if kl else ""}
  <div class="more"><h3>Cari KAP Murah di Kota Lain</h3><div class="citylist">{nl} <a href="/kap-murah/">Semua Kota</a></div></div>
  <div class="more"><h3>Layanan Lain di {c}</h3><div class="citylist"><a href="/kota/{s}/kap/">KAP {c}</a><a href="/kota/{s}/kjpp/">KJPP {c}</a><a href="/kota/{s}/konsultan-pajak/">Konsultan Pajak {c}</a><a href="/kota/{s}/jasa-laporan-keuangan/">Jasa Laporan Keuangan {c}</a><a href="{FA}/wilayah/{s}/">Konsultan Keuangan {c} (FA Indonesia)</a></div></div>'''

murah_urls = []
for name, prov, reg, secs, note in CITIES:
    s = slug(name)
    near = sorted([c for c in CITIES if c[2] == reg and c[0] != name], key=lambda c: c[1] != prov)
    kws = [k for k in _KW if k[1] == name]
    u = f"{DOMAIN}/kota/{s}/kap-murah/"
    title = f"KAP Murah di {name}: Apakah Bijak? Cek Independensi dan Kredibilitasnya | cariakuntan.com"
    desc = f"Cari KAP murah di {name}, {prov}? Apakah bijak, independen, dan dipercaya bank? Cara menilai kantor akuntan publik, kapan hemat masih aman, dan diskusi kebutuhan audit gratis."
    faq = murah_faq(name)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": f"KAP Murah di {name}: Pendampingan Memilih KAP", "serviceType": "Rujukan Kantor Akuntan Publik dan Jasa Audit", "areaServed": {"@type": "City", "name": name, "containedInPlace": {"@type": "AdministrativeArea", "name": prov}},
         "provider": {"@type": "ProfessionalService", "name": "cariakuntan.com", "url": DOMAIN + "/"}, "url": u, "description": desc},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": name, "item": f"{DOMAIN}/kota/{s}/"}, {"@type": "ListItem", "position": 3, "name": "KAP Murah", "item": u}]}]}
    m = f"Selamat siang Pak Ananta, kami dari {name} ingin diskusi kebutuhan audit dan memilih KAP yang biayanya wajar dan diterima bank."
    html = head(title, desc, u, extra=ldtag(ld))
    html += header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kap-murah/">KAP Murah</a> / <a href="/kota/{s}/">{name}</a></p>
  <p class="label" style="margin-top:14px">{name}, {prov}</p>
  <h1>KAP Murah di {name}: Apakah Bijak, Independen, dan Dapat Dipercaya?</h1>
  <p class="sub">Sebelum memilih KAP karena harga, diskusikan dulu kebutuhannya: untuk bank apa, wajib audit, tender, atau investor. Kami bantu memilih kantor akuntan publik berizin yang independen dan biayanya wajar untuk skala usaha Anda.</p>
  <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(m)}" target="_blank" rel="noopener">Diskusikan Kebutuhan Audit</a><span style="color:var(--muted);font-size:.9rem">Diskusi awal tanpa biaya</span></div>
  {murah_body(name, prov, secs, note, near, kws)}
  <div class="prose"><h2>Tanya Jawab: KAP Murah di {name}</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)}</div>
  {fa_box(name)}
</main>
''' + footer(ID)
    write(f"/kota/{s}/kap-murah/", html); urls.append(f"/kota/{s}/kap-murah/"); murah_urls.append((name, prov, reg))

# ---------- hub ----------
hub_title = "KAP Murah: Apakah Bijak, Independen, dan Dipercaya? Panduan per Kota | cariakuntan.com"
hub_desc = "Cari KAP murah per kota di seluruh Indonesia. Kantor akuntan publik berizin dengan biaya audit sesuai skala usaha dan kelas rekanan bank. Konsultasi awal gratis."
groups = {}
for n, p_, r in murah_urls: groups.setdefault(REGIONS[r][0], []).append(n)
hub_list = "".join(f'<div class="more"><h3>{g}</h3><div class="citylist">' + " ".join(f'<a href="/kota/{slug(n)}/kap-murah/">KAP Murah {n}</a>' for n in ns) + "</div></div>" for g, ns in groups.items())
hfaq = murah_faq("kota Anda")
hld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": "Cari KAP Murah per Kota", "url": DOMAIN + "/kap-murah/", "description": hub_desc},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in hfaq]}]}
html = head(hub_title, hub_desc, DOMAIN + "/kap-murah/", extra=ldtag(hld))
html += header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / KAP Murah</p>
  <h1>KAP Murah: Apakah Bijak, Independen, dan Dapat Dipercaya?</h1>
  <p class="sub">KAP yang tepat adalah KAP berizin dan independen dengan biaya wajar untuk skala usaha Anda, serta diterima pihak yang meminta laporan audit. Diskusikan dulu kebutuhannya, lalu pilih kota Anda.</p>
  <div style="margin-top:22px"><a class="btn btn-wa arrow" href="{wa("Selamat siang Pak Ananta, kami mencari KAP dengan biaya audit yang hemat dan diterima bank.")}" target="_blank" rel="noopener">Chat Ananta, CPA</a></div>
  {tblx(["Kebutuhan", "Pilihan paling hemat yang tetap diterima", "Catatan"], HEMAT)}
  <div class="prose"><h2>5 Cara Menekan Biaya Audit</h2><ol>{"".join(f"<li><b>{a}.</b> {b}</li>" for a, b in CARA)}</ol></div>
  {hub_list}
  <div class="prose"><h2>Tanya Jawab</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in hfaq)}</div>
</main>
''' + footer(ID)
write("/kap-murah/", html); urls.append("/kap-murah/")
print("kap-murah pages:", len(murah_urls) + 1)
