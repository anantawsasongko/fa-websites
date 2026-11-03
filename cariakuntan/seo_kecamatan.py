# Dieksekusi di build.py setelah seo_murah.py (2 Nov 2026). Halaman per kecamatan: /kota/<kota>/kecamatan/<kec>/ dan hub /kota/<kota>/kecamatan/.
# Kecamatan diambil dari kota dan kabupaten yang sudah punya halaman kota (2.000+ kecamatan). Data: shared/wilayah (ODbL).
import sys as _s2
_s2.path.insert(0, os.path.join(ROOT, "..", "shared", "wilayah")); import kec as _kec
KEC = _kec.by_city(CITIES)
CIDX = {c[0]: c for c in CITIES}
KEC_COUNT = 0

def kec_faq(k, kab, city):
    return [
     (f"Apakah ada KAP di {k}?", f"Kantor akuntan publik umumnya berkantor di pusat kota. Perusahaan di Kecamatan {k}, {kab} biasanya dilayani KAP dari {city} atau kota besar terdekat: dokumen diperiksa daring, tim datang untuk observasi persediaan dan aset. Kami bantu pilihkan KAP berizin yang sesuai kebutuhan Anda."),
     (f"Berapa biaya audit KAP untuk usaha di {k}?", "Bergantung pada total aset, jumlah transaksi, kerapian pembukuan, dan tujuan audit. Biaya perjalanan tim biasanya ditagihkan terpisah. Kisaran biaya disampaikan setelah melihat laporan keuangan terakhir Anda."),
     (f"Siapa yang bisa menyusun laporan keuangan usaha di {k}?", f"Kantor Jasa Akuntansi (KJA) dan akuntan berpraktik dapat menyusun laporan keuangan sesuai SAK EMKM, SAK EP, atau PSAK untuk usaha di {k}, termasuk laporan tahunan PT untuk SABH."),
     (f"Bagaimana memastikan KAP atau konsultan pajak yang melayani {k} berizin?", "Cek nama akuntan publik dan KAP di registri resmi Kementerian Keuangan, dan untuk kebutuhan sektor jasa keuangan di daftar OJK. Konsultan pajak dicek izin praktiknya di DJP."),
    ]

for cname, rows in KEC.items():
    if cname not in CIDX or not rows: continue
    _, prov, reg, secs, cnote = CIDX[cname]
    cs = slug(cname)
    hub = f"/kota/{cs}/kecamatan/"
    kabs = []
    for r in rows:
        if r["kab"] not in kabs: kabs.append(r["kab"])
    for r in rows:
        k, kab, ks = r["kec"], r["kab"], r["slug"]
        base = f"{hub}{ks}/"; url = DOMAIN + base
        desa = r["desa"]
        sibs = [x for x in rows if x["kab"] == kab and x["kec"] != k]
        faq = kec_faq(k, kab, cname)
        title = f"Cari KAP {k}, {kab}: Akuntan Publik, KJA, dan Konsultan Pajak | cariakuntan.com"
        desc = f"Cari KAP di Kecamatan {k}, {kab}: audit laporan keuangan, penyusunan laporan keuangan (KJA), konsultan pajak, dan KJPP untuk usaha di {k}. Konsultasi awal gratis."
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "ProfessionalService", "name": f"cariakuntan.com {k}", "url": url, "description": desc,
             "areaServed": {"@type": "AdministrativeArea", "name": f"Kecamatan {k}", "containedInPlace": {"@type": "AdministrativeArea", "name": kab}},
             "knowsAbout": ["Kantor Akuntan Publik", "Jasa Audit", "Kantor Jasa Akuntansi", "Konsultan Pajak", "KJPP"]},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": DOMAIN + "/"},
              {"@type": "ListItem", "position": 2, "name": cname, "item": f"{DOMAIN}/kota/{cs}/"},
              {"@type": "ListItem", "position": 3, "name": "Kecamatan", "item": DOMAIN + hub},
              {"@type": "ListItem", "position": 4, "name": k, "item": url}]}]}
        msg = f"Selamat siang Pak Ananta, kami dari Kecamatan {k}, {kab} sedang mencari KAP / jasa laporan keuangan / konsultan pajak."
        sline = "".join(f"<li>{SECTOR_LINES[s_]}</li>" for s_ in secs[:3] if s_ in SECTOR_LINES)
        overview = tblx(["Kebutuhan", "Dikerjakan Oleh", "Cara Melayani Usaha di " + k], [
            ("Audit laporan keuangan", "KAP (akuntan publik berizin)", f"Dokumen diperiksa daring, observasi lapangan dijadwalkan ke {k}"),
            ("Penyusunan laporan keuangan", "KJA atau akuntan berpraktik", "Sepenuhnya daring dari mutasi rekening dan bukti transaksi"),
            ("Pajak badan dan Coretax", "Konsultan pajak berizin", "Daring, pendampingan pemeriksaan bila diperlukan"),
            ("Penilaian aset dan agunan", "KJPP (penilai publik)", f"Inspeksi aset di {k} sesuai jadwal penilai")])
        desa_html = (f'<div class="prose"><h2>Desa dan Kelurahan di Kecamatan {k}</h2><p>Usaha dari {len(desa)} desa dan kelurahan berikut kami layani dengan cara yang sama:</p></div>'
                     f'<div class="citylist" style="margin-top:8px">{" ".join(f"<span>{d}</span>" for d in desa)}</div>') if desa else ""
        sib_html = " ".join(f'<a href="{hub}{x["slug"]}/">{x["kec"]}</a>' for x in sibs[:24])
        html = head(title, desc, url, extra=ldtag(ld)) + header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kota/{cs}/">{cname}</a> / <a href="{hub}">Kecamatan</a> / {k}</p>
  <p class="label" style="margin-top:14px">Kecamatan {k} · {kab} · {prov}</p>
  <h1>Cari KAP di {k}: Audit, Laporan Keuangan, dan Pajak untuk Usaha di Kecamatan {k}</h1>
  <p class="sub">Kantor akuntan publik jarang berkantor di tingkat kecamatan. Untuk usaha di {k}, {kab}, kami pilihkan KAP, KJA, konsultan pajak, atau KJPP berizin yang sanggup melayani dari {cname} atau kota terdekat, sesuai syarat bank, notaris, atau investor Anda.</p>
  <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(msg)}" target="_blank" rel="noopener">Chat Ananta, CPA</a><span style="color:var(--muted);font-size:.9rem">Diskusi awal tanpa biaya</span></div>
  <div class="citylist" style="margin-top:18px"><a href="/kota/{cs}/kap/">KAP {cname}</a> <a href="/kota/{cs}/kap-murah/">Biaya Audit {cname}</a> <a href="/kota/{cs}/laporan-tahunan-pt/">Laporan Tahunan PT {cname}</a> <a href="/artikel/jasa-audit-laporan-keuangan-cara-memilih-kap/">Cara Memilih KAP</a></div>
  <div class="prose"><h2>Siapa Mengerjakan Apa untuk Usaha di {k}</h2></div>
  {overview}
  <div class="prose"><h2>Kebutuhan yang Sering Muncul di Sekitar {k}</h2><p>{kab} termasuk wilayah {cname}, {cnote}. Kebutuhan yang paling sering kami tangani:</p><ul>{sline}<li>Laporan tahunan PT untuk akta notaris dan SABH, dengan laporan audited bila PT memenuhi kriteria wajib audit.</li></ul>
  <h2>Langkah Memilih Kantor yang Tepat</h2><ol><li>Tentukan siapa pembaca laporannya: bank, notaris, investor, atau kantor pajak.</li><li>Cek izin KAP atau konsultan di registri resmi.</li><li>Minta penawaran tertulis yang mencantumkan jadwal kunjungan ke {k} dan biaya perjalanan.</li></ol></div>
  {desa_html}
  <div class="prose"><h2>Tanya Jawab: KAP dan Akuntan di {k}</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)}</div>
  <style>.fold{{margin-top:30px;border-top:1px solid var(--line,#333);padding-top:14px}}.fold summary{{cursor:pointer;list-style:none;font-weight:600;display:flex;justify-content:space-between;align-items:center;gap:12px}}.fold summary::-webkit-details-marker{{display:none}}.fold summary::after{{content:"+";font-size:1.3em;line-height:1;opacity:.7}}.fold[open] summary::after{{content:"\2212"}}.fold .citylist,.fold p{{margin-top:12px}}</style><details class="fold"><summary>Kecamatan lain di {kab} ({len(sibs)})</summary><div class="citylist"><a href="{hub}">Semua Kecamatan {cname}</a> {sib_html}</div></details>
  <p style="font-size:.78rem;color:var(--muted);margin-top:18px">Data wilayah: kode wilayah Kemendagri ({r["kode"]}), diolah dari Wilayah Administratif Indonesia (ODbL).</p>
</main>
''' + footer(ID)
        write(base, html); urls.append(base); KEC_COUNT += 1
    # hub per kota
    blocks = "".join(f'<div class="prose"><h2>{kb}</h2></div><div class="citylist">' + " ".join(f'<a href="{hub}{x["slug"]}/">{x["kec"]}</a>' for x in rows if x["kab"] == kb) + "</div>" for kb in kabs)
    title = f"Cari KAP per Kecamatan di {cname}: {len(rows)} Kecamatan | cariakuntan.com"
    desc = f"Daftar {len(rows)} kecamatan di {', '.join(kabs)}. Pilih kecamatan Anda untuk mencari KAP, jasa laporan keuangan, konsultan pajak, dan KJPP."
    html = head(title, desc, DOMAIN + hub) + header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kota/{cs}/">{cname}</a> / Kecamatan</p>
  <h1>Cari KAP dan Akuntan per Kecamatan di {cname}</h1>
  <p class="sub">{len(rows)} kecamatan di {", ".join(kabs)}. Pilih kecamatan lokasi usaha Anda.</p>
  {blocks}
  <div class="more"><h3>Layanan di {cname}</h3><div class="citylist"><a href="/kota/{cs}/">{cname}</a> <a href="/kota/{cs}/kap/">KAP {cname}</a> <a href="/kota/{cs}/kap-murah/">Biaya Audit {cname}</a> <a href="/kota/{cs}/jasa-laporan-keuangan/">Jasa Laporan Keuangan {cname}</a></div></div>
</main>
''' + footer(ID)
    write(hub, html); urls.append(hub)
    # tautan dari halaman kota ke hub kecamatan
    _cp = os.path.join(SITE, "kota", cs, "index.html")
    if os.path.exists(_cp):
        _t = open(_cp, encoding="utf-8").read()
        if "kec-hub" not in _t:
            _top = " ".join(f'<a href="{hub}{x["slug"]}/">{x["kec"]}</a>' for x in rows[:30])
            _b = f'FOLDCSS<details class="fold kec-hub"><summary>Cari KAP per kecamatan di {cname} ({len(rows)})</summary><div class="citylist"><a href="{hub}">Semua {len(rows)} Kecamatan</a> {_top}</div></details>'.replace("FOLDCSS", '<style>.fold{margin-top:30px;border-top:1px solid var(--line,#333);padding-top:14px}.fold summary{cursor:pointer;list-style:none;font-weight:600;display:flex;justify-content:space-between;align-items:center;gap:12px}.fold summary::-webkit-details-marker{display:none}.fold summary::after{content:"+";font-size:1.3em;line-height:1;opacity:.7}.fold[open] summary::after{content:"\\2212"}.fold .citylist,.fold p{margin-top:12px}</style>')
            _i = _t.rfind("</main>"); _t = _t[:_i] + _b + _t[_i:]
            open(_cp, "w", encoding="utf-8").write(_t)
print("kecamatan pages:", KEC_COUNT)
