# Dieksekusi di build.py setelah seo_pembukuan.py (3 Nov 2026).
# Halaman Koperasi Desa Merah Putih (KDMP) untuk SELURUH kecamatan Indonesia: /kdmp/<prov>/<kab>/<kec>/ beserta daftar desanya,
# plus hub /kdmp/, /kdmp/<prov>/, /kdmp/<prov>/<kab>/. Halaman ringan: CSS dipisah ke /css/ca-kdmp.css. Data: shared/wilayah (ODbL).
import csv as _csv, re as _re
_WD = os.path.join(ROOT, "..", "shared", "wilayah")
_s2.path.insert(0, _WD); import kec as _K
_P = {r[0]: _K.tc(r[1]).replace("Di ", "DI ").replace("Dki ", "DKI ") for r in _csv.reader(open(os.path.join(_WD, "provinces.csv"), encoding="utf-8"))} if os.path.exists(os.path.join(_WD, "provinces.csv")) else {}
_R = {r[0]: (r[1], _K.kab_name(r[2])) for r in _csv.reader(open(os.path.join(_WD, "regencies.csv"), encoding="utf-8"))}
_D = {}
for _r in _csv.reader(open(os.path.join(_WD, "districts.csv"), encoding="utf-8")): _D.setdefault(_r[1], []).append((_r[0], _K.tc(_r[2])))
_V = {}
for _r in _csv.reader(open(os.path.join(_WD, "villages.csv"), encoding="utf-8")): _V.setdefault(_r[1], []).append(_K.tc(_r[2]))
_css = "".join(_re.findall(r"<style[^>]*>(.*?)</style>", STYLE + EXTRA_CSS, _re.S))
os.makedirs(os.path.join(SITE, "css"), exist_ok=True)
open(os.path.join(SITE, "css", "ca-kdmp.css"), "w", encoding="utf-8").write(_css)
def _lean(title, desc, url, ld):
    h = head(title, desc, url, extra=ldtag(ld))
    h = h.replace(STYLE, "").replace(EXTRA_CSS, "")
    return h.replace("</head>", '<link rel="stylesheet" href="/css/ca-kdmp.css"></head>', 1)
FAU = "https://faindonesia.co.id"
ART = "/artikel/laporan-keuangan-kdmp-pakai-sak-apa-panduan-pengurus/"
def _crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + u} for i, (n, u) in enumerate(items)]}
_tree = {}
for rid, (pid, kab) in _R.items():
    if pid not in _P: continue
    _tree.setdefault(pid, []).append((rid, kab))
_n = 0
PAKET = ('<div class="tblwrap"><table class="tbl"><thead><tr><th>Layanan untuk KDMP</th><th>Mulai</th></tr></thead><tbody>'
 '<tr><th scope="row">Pembukuan bulanan koperasi (semua unit usaha)</th><td>Rp2 juta/bulan</td></tr>'
 '<tr><th scope="row">Laporan keuangan tahunan untuk RAT</th><td>Sesuai penawaran</td></tr>'
 '<tr><th scope="row">Audit atau AUP oleh KAP mitra terdaftar OJK</th><td>Sesuai penawaran</td></tr></tbody></table></div>')
SAKT = ('<div class="tblwrap"><table class="tbl"><thead><tr><th>Kegiatan Usaha KDMP</th><th>SAK (Permenkop UKM 2/2024)</th></tr></thead><tbody>'
 '<tr><th scope="row">Ada simpan pinjam anggota</th><td>SAK Indonesia atau SAK EP</td></tr>'
 '<tr><th scope="row">Hanya sektor riil</th><td>Standar instansi pembina; bila belum ada: SAK Indonesia, SAK EP, atau SAK EMKM</td></tr></tbody></table></div>')
for pid in sorted(_tree):
    prov = _P[pid]; ps = slug(prov); purl = f"/kdmp/{ps}/"
    kabs = sorted(_tree[pid], key=lambda x: x[1])
    for rid, kab in kabs:
        ks = slug(kab); kurl = f"{purl}{ks}/"
        kecs = sorted(_D.get(rid, []), key=lambda x: x[1]); seen = set()
        rows = []
        for did, kec in kecs:
            s = slug(kec); s = s if s not in seen else s + "-" + did[-3:]; seen.add(s); rows.append((did, kec, s))
        for did, kec, s in rows:
            u = f"{kurl}{s}/"; url = DOMAIN + u; desa = sorted(_V.get(did, []))
            title = f"Laporan Keuangan dan Audit Kopdes Merah Putih Kecamatan {kec}, {kab} | cariakuntan.com"
            desc = f"Jasa pembukuan, laporan keuangan RAT sesuai SAK EP, dan audit untuk {len(desa)} Koperasi Desa Merah Putih di Kecamatan {kec}, {kab}, {prov}. Pengurus cukup upload bukti ke Drive."
            msg = f"Selamat siang Pak Ananta, kami pengurus Koperasi Desa Merah Putih desa ____ di Kecamatan {kec}, {kab}. Kami perlu bantuan laporan keuangan/RAT/audit."
            faq = [(f"Siapa yang bisa menyusun laporan keuangan KDMP di Kecamatan {kec}?", f"Kantor Jasa Akuntansi dapat menyusun laporan keuangan Koperasi Desa Merah Putih di {kec} secara daring dari foto bukti dan mutasi rekening, sesuai SAK yang ditentukan Permenkop UKM 2/2024."),
                   ("KDMP memakai SAK apa?", "Bila ada unit simpan pinjam, SAK Indonesia atau SAK EP. Bila murni sektor riil dan belum ada standar instansi pembina, boleh SAK Indonesia, SAK EP, atau SAK EMKM.")]
            ld = {"@context": "https://schema.org", "@graph": [
                {"@type": "Service", "name": f"Laporan Keuangan Koperasi Desa Merah Putih {kec}", "serviceType": "Akuntansi dan audit koperasi", "url": url,
                 "areaServed": {"@type": "AdministrativeArea", "name": f"Kecamatan {kec}, {kab}, {prov}"}, "provider": {"@type": "Organization", "name": "cariakuntan.com", "url": DOMAIN + "/"}},
                {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
                _crumbs([("Beranda", "/"), ("KDMP", "/kdmp/"), (prov, purl), (kab, kurl), (kec, u)])]}
            dl = (f'<div class="prose"><h2>Koperasi Desa Merah Putih di Kecamatan {kec}</h2><p>Layanan ini untuk pengurus dan pengawas KDMP di {len(desa)} desa dan kelurahan berikut:</p></div>'
                  f'<div class="citylist">{" ".join(f"<span>Kopdes Merah Putih {d}</span>" for d in desa)}</div>') if desa else ""
            sib = " ".join(f'<a href="{kurl}{x[2]}/">{x[1]}</a>' for x in rows if x[0] != did)[:6000]
            html = _lean(title, desc, url, ld) + header(ID, "home") + f'''<main class="wrap art">
  <p class="crumb"><a href="/">Beranda</a> / <a href="/kdmp/">KDMP</a> / <a href="{purl}">{prov}</a> / <a href="{kurl}">{kab}</a> / {kec}</p>
  <p class="label" style="margin-top:14px">Kecamatan {kec} · {kab} · {prov}</p>
  <h1>Laporan Keuangan dan Audit Koperasi Desa Merah Putih di Kecamatan {kec}</h1>
  <p class="sub">Untuk pengurus KDMP: pembukuan bulanan semua unit usaha, laporan keuangan untuk RAT sesuai SAK, sampai audit bila diminta bank atau anggota. Cukup foto bukti dan upload ke Google Drive, akuntan kami yang menyusun.</p>
  <div style="margin-top:22px"><a class="btn btn-wa arrow" href="{wa(msg)}" target="_blank" rel="noopener">Chat Ananta, CPA</a></div>
  {dl}
  <div class="prose"><h2>KDMP Pakai SAK yang Mana?</h2><p>Permenkop UKM 2/2024 menentukan standar dari kegiatan usaha koperasi. KDMP yang menjalankan simpan pinjam anggota praktis memakai SAK EP.</p></div>
  {SAKT}
  <div class="prose"><h2>Cara Kerja dan Paket</h2><ol><li>Pengurus upload nota gerai, bukti simpanan dan pinjaman anggota, mutasi rekening, dan perjanjian pinjaman bank ke folder Drive.</li><li>Tim KJA Farhani menyusun pembukuan dan laporan per unit usaha.</li><li>Laporan bulanan dan laporan tahunan untuk RAT dikirim ke pengurus.</li><li>Bila diminta, audit atau AUP dilaksanakan KAP DHN &amp; Rekan, pihak yang berbeda dari penyusun.</li></ol></div>
  {PAKET}
  <div class="prose"><h2>Tanya Jawab</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)}<p>Bacaan: <a href="{ART}">Laporan Keuangan KDMP Pakai SAK Apa?</a> · <a href="{FAU}/audit-koperasi-desa-merah-putih/">Laporan Keuangan dan Audit KDMP</a> · <a href="https://updatesak.com/artikel/sak-untuk-kdkmp-koperasi-desa-merah-putih-permenkop-2-2024/">Ringkasan SAK untuk KDKMP</a></p></div>
  <style>.fold{{margin-top:30px;border-top:1px solid var(--line,#333);padding-top:14px}}.fold summary{{cursor:pointer;list-style:none;font-weight:600;display:flex;justify-content:space-between;align-items:center;gap:12px}}.fold summary::-webkit-details-marker{{display:none}}.fold summary::after{{content:"+";font-size:1.3em;line-height:1;opacity:.7}}.fold[open] summary::after{{content:"\2212"}}.fold .citylist,.fold p{{margin-top:12px}}</style><details class="fold"><summary>Kecamatan lain di {kab} ({len(rows)-1})</summary><div class="citylist">{sib}</div></details>
  <p style="font-size:.78rem;color:var(--muted);margin-top:18px">Data wilayah: kode Kemendagri {did}, diolah dari Wilayah Administratif Indonesia (ODbL).</p>
</main>
''' + footer(ID)
            write(u, html); urls.append(u); _n += 1
        hl = " ".join(f'<a href="{kurl}{x[2]}/">{x[1]}</a>' for x in rows)
        ldk = {"@context": "https://schema.org", "@graph": [_crumbs([("Beranda", "/"), ("KDMP", "/kdmp/"), (prov, purl), (kab, kurl)])]}
        write(kurl, _lean(f"Laporan Keuangan Kopdes Merah Putih {kab}: Per Kecamatan | cariakuntan.com", f"Jasa laporan keuangan dan audit Koperasi Desa Merah Putih di {len(rows)} kecamatan {kab}, {prov}.", DOMAIN + kurl, ldk)
              + header(ID, "home") + f'<main class="wrap art"><p class="crumb"><a href="/">Beranda</a> / <a href="/kdmp/">KDMP</a> / <a href="{purl}">{prov}</a> / {kab}</p><h1>Laporan Keuangan Koperasi Desa Merah Putih di {kab}</h1><p class="sub">Pilih kecamatan Anda.</p><div class="citylist" style="margin-top:18px">{hl}</div><div style="margin-top:22px"><a class="btn btn-wa arrow" href="{wa(f"Selamat siang Pak Ananta, kami pengurus Koperasi Desa Merah Putih di {kab}. Kami perlu bantuan laporan keuangan/RAT/audit.")}" target="_blank" rel="noopener">Chat Ananta, CPA</a></div></main>' + footer(ID))
        urls.append(kurl)
    hp = " ".join(f'<a href="{purl}{slug(k)}/">{k}</a>' for _, k in kabs)
    write(purl, _lean(f"Laporan Keuangan Kopdes Merah Putih {prov} | cariakuntan.com", f"Jasa laporan keuangan dan audit Koperasi Desa Merah Putih di {prov}, per kabupaten dan kota.", DOMAIN + purl, {"@context": "https://schema.org", "@graph": [_crumbs([("Beranda", "/"), ("KDMP", "/kdmp/"), (prov, purl)])]})
          + header(ID, "home") + f'<main class="wrap art"><p class="crumb"><a href="/">Beranda</a> / <a href="/kdmp/">KDMP</a> / {prov}</p><h1>Laporan Keuangan Koperasi Desa Merah Putih di {prov}</h1><p class="sub">Pilih kabupaten atau kota.</p><div class="citylist" style="margin-top:18px">{hp}</div></main>' + footer(ID))
    urls.append(purl)
_hp = " ".join(f'<a href="/kdmp/{slug(_P[p])}/">{_P[p]}</a>' for p in sorted(_tree, key=lambda x: _P[x]))
write("/kdmp/", _lean("Laporan Keuangan dan Audit Koperasi Desa Merah Putih Seluruh Indonesia | cariakuntan.com", "Jasa pembukuan, laporan keuangan RAT sesuai SAK EP, dan audit Koperasi Desa Merah Putih untuk seluruh kecamatan di Indonesia. Pengurus cukup upload bukti ke Drive.", DOMAIN + "/kdmp/", {"@context": "https://schema.org", "@graph": [_crumbs([("Beranda", "/"), ("KDMP", "/kdmp/")])]})
      + header(ID, "home") + f'''<main class="wrap art"><p class="crumb"><a href="/">Beranda</a> / KDMP</p><h1>Laporan Keuangan dan Audit Koperasi Desa Merah Putih Seluruh Indonesia</h1>
<p class="sub">Pembukuan bulanan, laporan untuk RAT sesuai SAK, dan audit untuk KDMP di seluruh kecamatan. Dikerjakan daring: pengurus upload bukti ke Google Drive.</p>
<div style="margin-top:22px"><a class="btn btn-wa arrow" href="{wa("Selamat siang Pak Ananta, kami pengurus Koperasi Desa Merah Putih. Kami perlu bantuan laporan keuangan/RAT/audit.")}" target="_blank" rel="noopener">Chat Ananta, CPA</a></div>
{SAKT}{PAKET}<div class="prose"><h2>Pilih Provinsi</h2></div><div class="citylist">{_hp}</div><p style="margin-top:18px"><a href="{ART}">Panduan: Laporan Keuangan KDMP Pakai SAK Apa?</a></p></main>''' + footer(ID))
urls.append("/kdmp/")
print("kdmp pages:", _n)
