# Dieksekusi di build.py setelah seo_pembukuan.py (5 Nov 2026, permintaan Bos: push akuntan forensik sampai daerah).
# /akuntan-forensik/ (hub) + /kota/<kota>/akuntan-forensik/ untuk semua kota, kotak tautan di hub kota dan halaman kecamatan.
# Eksekusi laporan: tim FA Indonesia, ditandatangani AP KAP DHN & Rekan (Pemimpin Rekan pemegang CFI IAPI). Kerugian negara bukan wilayah kami (BPK/BPKP).
FAF = "https://faindonesia.co.id/akuntan-forensik/"
FR_MSG = "Selamat siang Pak Ananta, saya butuh laporan penghitungan kerugian (penipuan/penggelapan) untuk penyidik. Kota saya: "
FR_KASUS = tblx(["Kasus", "Yang Dihitung"], [
  ("Penipuan transaksi atau investasi", "Dana yang ditransfer dikurangi yang sudah kembali, per tanggal"),
  ("Penggelapan oleh karyawan atau kasir", "Selisih kas, penjualan tidak disetor, stok hilang"),
  ("Penggelapan oleh mitra usaha", "Bagi hasil tidak dibayar, dana dipakai di luar kesepakatan"),
  ("Proyek atau barang tidak diserahkan", "Pembayaran dikurangi nilai pekerjaan yang benar-benar diterima")])
FR_FAQ = [
 ("Berapa biaya akuntan forensik?", "Biaya tetap disepakati setelah review dokumen. Kasus perorangan dengan dokumen sederhana mulai Rp15 juta, DP 50% saat mulai, pelunasan saat laporan final."),
 ("Siapa yang menandatangani laporan?", "Akuntan publik dari KAP DHN & Rekan. Pemimpin rekannya memegang sertifikasi Certified Financial Investigator (CFI) dari IAPI."),
 ("Apakah ahli harus hadir ke penyidik?", "Laporan tertulis biasanya sudah cukup sebagai dasar penyidik. Kehadiran ahli dibahas terpisah bila penyidik memintanya."),
 ("Apakah melayani kerugian negara?", "Tidak. Perkara kerugian keuangan negara dihitung oleh BPK atau BPKP. Layanan ini untuk perkara antar pihak swasta.")]

def fr_page(path, crumb, h1, sub, title, desc, msg, intro="", area="Indonesia", extra=""):
    url = DOMAIN + path
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": "Akuntan Forensik dan Penghitungan Kerugian", "serviceType": "Forensic accounting", "url": url,
         "areaServed": {"@type": "Place", "name": area}, "provider": {"@type": "AccountingService", "name": "FA Indonesia", "url": "https://faindonesia.co.id/"},
         "offers": {"@type": "Offer", "price": "15000000", "priceCurrency": "IDR", "description": "Laporan penghitungan kerugian, kasus perorangan dokumen sederhana"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FR_FAQ]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]}]}
    html = head(title, desc, url, extra=ldtag(ld)) + header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / {crumb}</p>
  <p class="label" style="margin-top:14px">Akuntan Forensik · Laporan untuk Penyidik</p>
  <h1>{h1}</h1>
  <p class="sub">{sub}</p>
  <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px"><a class="btn btn-wa arrow" href="{wa(msg)}" target="_blank" rel="noopener">Tanya Ananta, CPA</a><a class="btn" style="border:1px solid var(--line)" href="{FAF}">Detail Layanan</a></div>
  <div class="prose">{intro}<h2>Kasus yang Kami Hitung</h2></div>
  {FR_KASUS}
  <div class="prose"><h2>Cara Kerja</h2><ol><li><b>Upload dokumen</b>: bukti transfer, kontrak, chat, nota, rekening koran, lewat WhatsApp atau Google Drive.</li>
  <li><b>Review dan biaya tetap</b> setelah kami cek kecukupan bukti.</li><li><b>Penghitungan</b>: setiap angka ditelusuri ke dokumen sumber; yang belum ada buktinya ditandai sebagai batasan.</li>
  <li><b>Laporan tertulis</b> ditandatangani akuntan publik, siap diserahkan ke penyidik atau kuasa hukum.</li></ol>
  <h2>Biaya</h2><p>Kasus perorangan dengan dokumen sederhana mulai Rp15 juta, DP 50% saat mulai, pelunasan saat laporan final diserahkan.</p>
  <h2>Yang Perlu Diketahui</h2><ul><li>Keterangan ahli adalah alat bukti yang sah dalam KUHAP baru (UU 20/2025, Pasal 235 ayat 1).</li>
  <li>Kami menghitung kerugian dari dokumen; ada tidaknya tindak pidana diputuskan penyidik dan hakim.</li>
  <li>Kerugian keuangan negara dihitung BPK atau BPKP, bukan layanan ini.</li></ul>
  <h2>Siapa yang Mengerjakan</h2><p>Tim FA Indonesia menghitung, laporan ditandatangani akuntan publik <a href="https://faindonesia.co.id/kap-dhn/">KAP DHN &amp; Rekan</a> yang pemimpin rekannya memegang Certified Financial Investigator (CFI) dari IAPI. Panduan: <a href="/artikel/cara-menghitung-kerugian-penipuan-untuk-laporan-polisi/">cara menghitung kerugian penipuan</a>, <a href="/artikel/dokumen-yang-disiapkan-untuk-laporan-kerugian-ke-penyidik/">dokumen yang disiapkan</a>.</p>
  <h2>Tanya Jawab</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FR_FAQ)}</div>
  {extra}
  <div class="cta-box"><h3>Ceritakan Kasusnya</h3><p style="color:var(--muted)">Kirim kronologi singkat dan perkiraan jumlah transaksi. Review awal dokumen gratis.</p><a class="btn btn-wa" style="justify-self:start" href="{wa(msg)}" target="_blank" rel="noopener">Tanya Ananta, CPA</a></div>
</main>
''' + footer(ID)
    write(path, html); urls.append(path)

_fr_list = " ".join(f'<a href="/kota/{slug(c[0])}/akuntan-forensik/">{c[0]}</a>' for c in CITIES)
_fr_fold = f'<details class="fold"><summary>Akuntan Forensik per Kota ({len(CITIES)})</summary><div class="citylist">{_fr_list}</div></details>'
fr_page("/akuntan-forensik/", "Akuntan Forensik", "Akuntan Forensik: Laporan Penghitungan Kerugian Penipuan dan Penggelapan untuk Penyidik",
  "Untuk korban penipuan, penggelapan, dan sengketa usaha yang perlu angka kerugian rapi dan bisa dipertanggungjawabkan, ditandatangani akuntan publik. Melayani seluruh Indonesia secara daring.",
  "Akuntan Forensik: Hitung Kerugian Penipuan, Penggelapan untuk Laporan Polisi | cariakuntan.com",
  "Jasa akuntan forensik seluruh Indonesia: laporan penghitungan kerugian penipuan dan penggelapan, ditandatangani akuntan publik, siap untuk penyidik. Mulai Rp15 juta.",
  FR_MSG, extra=_fr_fold)
_frn = 0
for c in CITIES:
    s = slug(c[0]); nm = c[0]; prov = c[1]
    near = [x for x in CITIES if x[1] == prov and x[0] != nm][:8]
    nl = " ".join(f'<a href="/kota/{slug(x[0])}/akuntan-forensik/">{x[0]}</a>' for x in near)
    ex = f'<details class="fold"><summary>Akuntan Forensik di Kota Lain ({len(near)})</summary><div class="citylist">{nl} <a href="/akuntan-forensik/">Semua Kota</a></div></details>' if near else ""
    intro = (f"<p>Kasus penipuan atau penggelapan di {nm} sering macet karena angka kerugiannya belum jelas: transfer bercampur, sebagian uang sudah kembali, bukti tersebar di chat. "
             f"Kami menyusun laporan penghitungan kerugian yang bisa diserahkan ke penyidik di {nm} dan wilayah {prov}, tanpa Anda perlu datang ke kantor. "
             f"Layanan akuntan lain di kota ini: <a href=\"/kota/{s}/\">KAP, KJA, dan KJPP {nm}</a>.</p>")
    fr_page(f"/kota/{s}/akuntan-forensik/", f"Akuntan Forensik {nm}", f"Akuntan Forensik {nm}: Hitung Kerugian Penipuan dan Penggelapan",
      f"Laporan penghitungan kerugian untuk penyidik di {nm}, ditandatangani akuntan publik. Dokumen dikirim daring, review awal gratis.",
      f"Akuntan Forensik {nm}: Hitung Kerugian Penipuan, Penggelapan | cariakuntan.com",
      f"Butuh akuntan forensik di {nm}? Laporan penghitungan kerugian penipuan dan penggelapan untuk penyidik, ditandatangani akuntan publik. Mulai Rp15 juta.",
      FR_MSG + nm, intro=intro, area=nm, extra=ex)
    _frn += 1

# kotak di hub kota dan halaman kecamatan
_fb = 0
for _d, _, _fs in os.walk(os.path.join(SITE, "kota")):
    if "index.html" not in _fs: continue
    _rel = os.path.relpath(_d, os.path.join(SITE, "kota")).replace(os.sep, "/").split("/")
    if not (len(_rel) == 1 or (len(_rel) == 3 and _rel[1] == "kecamatan")): continue
    _cs = _rel[0]; _p = os.path.join(_d, "index.html"); _t = open(_p, encoding="utf-8").read()
    if "fr-box" in _t or "</main>" not in _t: continue
    _nm = next((c[0] for c in CITIES if slug(c[0]) == _cs), None)
    if not _nm: continue
    _box = (f'<!--fr-box--><div class="fr-box" style="box-sizing:border-box;width:min(1008px,calc(100% - 32px));margin:18px auto 8px;padding:16px 20px;border:1px solid var(--line);border-radius:10px">'
            f'<p style="margin:0">Jadi korban penipuan atau penggelapan? Kami menyusun laporan penghitungan kerugian untuk penyidik, ditandatangani akuntan publik: '
            f'<a href="/kota/{_cs}/akuntan-forensik/">Akuntan Forensik {_nm}</a>.</p></div><!--/fr-box-->')
    _i = _t.rfind("</main>"); open(_p, "w", encoding="utf-8").write(_t[:_i] + _box + _t[_i:]); _fb += 1
print("akuntan forensik: hub +", _frn, "kota, kotak di", _fb)
