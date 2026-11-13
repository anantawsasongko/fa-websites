# -*- coding: utf-8 -*-
"""13 Nov 2026 (Bos): jualan ke segmen yang dicari pemilik usaha (UMKM, cafe, resto, pabrik, travel umrah, dst.)
juga lewat UpdateSAK (edukasi) dan CariAkuntan (cari kantor). Halaman lama yang sudah rapi tidak diubah tata letaknya.

Konten: fa_content/segmen20261113.py (7 segmen). Bekerja di out/ (template = halaman live), idempoten.
1. UpdateSAK /akuntansi-<slug>/ (template live /akuntansi-rumah-sakit/): standar, perlakuan akuntansi khas industri,
   Tanya Jawab, kota (link ke halaman penyusunan LK FA per kota), Dikerjakan Tim FA Indonesia (link pilar FA + CariAkuntan).
   Link masuk: baris <!--us-ind--> setelah <!--/us-kw3--> di 95 halaman PSAK/SA/pilar; sitemap <!--usind-->; llms.txt.
   (/akuntansi-rumah-sakit/ yang sudah ada ikut masuk baris itu, halamannya tidak diubah.)
2. CariAkuntan /akuntan-<slug>/ (template live /konsultan-rumah-sakit/): kebutuhan per jenis kantor, checklist memilih,
   rekanan (KJA Farhani K.N., KAP DHN & Rekan lewat FA Indonesia), Tanya Jawab, kota per sektor (/kota/<kota>/).
   Link masuk: lipatan <!--ca-seg--> "Akuntan per jenis usaha di <kota>" setelah <!--/ca-kw3h--> di 113 hub /kota/<kota>/;
   sitemap <!--caseg-->; llms.txt.
3. FA: baris <!--fa-indedu--> "Bacaan" di pilar audit dan LK industri terkait (link ke US dan CA), sebelum Pertanyaan Umum.
Jalankan sesudah caus_rapi_20261113.py / fa_semua_berbayar (template sudah versi akhir). Aman diulang.
"""
import os, re, sys, json, html, glob, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "fa_content")); sys.path.insert(0, os.path.join(HERE, "cariakuntan"))
from segmen20261113 import SEG, STD
from industri20261112 import IND
from cities import CITIES
E = html.escape
OUT = os.path.join(HERE, "out")
US, CA, FA = "https://updatesak.com", "https://cariakuntan.com", "https://faindonesia.co.id"
TODAY = "2026-11-13"; UPD = "13 November 2026"
IX = {i["slug"]: i for i in IND}
def sl(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def rd(p): return open(p, encoding="utf-8").read()
def P(site, path): return os.path.join(OUT, site, *[x for x in path.strip("/").split("/") if x], "index.html")
def wt(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and rd(p) == t: return 0
    open(p, "w", encoding="utf-8").write(t); return 1
def wa(t): return "https://wa.me/6282245260121?text=" + urllib.parse.quote(t, safe="")
def hid(s): return sl(html.unescape(re.sub(r"<[^>]+>", "", s)))[:60].rstrip("-")
def fa_audit(s): return f"/audit-laporan-keuangan-{s['fa']}/" if s["fa"] else None
def fa_lk(s):
    if not s["fa"]: return "/laporan-keuangan-umkm/"
    i = IX[s["fa"]]; return "/" + (("laporan-keuangan-" + i["slug"]) if i["lk"] else i["lk_lama"]) + "/"
def kota(s):
    out = {}
    for nm, pv, rg, sek, cat in CITIES:
        if not s["sek"] or set(sek) & set(s["sek"]): out.setdefault(pv, []).append(nm)
    return dict(sorted(out.items()))
def us_tbl(h):  # tabel sederhana -> gaya UpdateSAK
    rows = re.findall(r"<tr>(.*?)</tr>", h, re.S)
    head = rows[0].replace("<th>", "<th>"); body = "".join(f"<tr>{r}</tr>" for r in rows[1:])
    return f'<div class="tx"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
def std_us():
    p, rows = STD
    return p + us_tbl("<table><tr><th>Bentuk Usaha</th><th>Kerangka Pelaporan</th></tr>" + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows) + "</table>")
def ld(graph): return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"
def faq_ld(faq): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def head_sw(t, title, desc, url, graph):
    t = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", t, count=1, flags=re.S)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{E(desc)}" name="description"/>', t, count=1)
    t = re.sub(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{url}" rel="canonical"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{E(title)}" property="og:title"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{E(desc)}" property="og:description"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{url}" property="og:url"/>', t, count=1)
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: ld(graph), t, count=1, flags=re.S)
    return t

# ---------------------------------------------------------------- UpdateSAK
UT = rd(P("updatesak", "/akuntansi-rumah-sakit/"))
OLDQ = re.findall(r'href="(https://wa\.me/6282245260121\?text=[^"]*Update%20SAK%20EMKM[^"]*)"', UT)
n_us = 0; US_URLS = []
for s in SEG:
    path = f"/akuntansi-{s['slug']}/"; url = US + path; US_URLS.append(path)
    secs = [(h, std_us() if b is None else (re.sub(r"<table>.*?</table>", lambda m: us_tbl(m.group()), b, flags=re.S))) for h, b in s["us"]]
    lk, au = fa_lk(s), fa_audit(s)
    tim = (f'<p>Kalau standar sudah dipahami tapi waktu dan tenaga tidak ada, Tim FA Indonesia bisa mengerjakannya: penyusunan laporan keuangan oleh KJA Farhani K.N., '
           f'audit oleh KAP DHN &amp; Rekan (terdaftar OJK). Rinciannya di <a href="{FA}{lk}">Jasa Laporan Keuangan {E(s["nama"])}</a>'
           + (f' dan <a href="{FA}{au}">Audit Laporan Keuangan {E(s["nama"])}</a>' if au else "")
           + f'. Untuk membandingkan kantor lain di kota Anda, lihat <a href="{CA}/akuntan-{s["slug"]}/">Akuntan untuk {E(s["nama"])}</a> di CariAkuntan.</p>')
    secs.append(("Dikerjakan Tim FA Indonesia", tim))
    kt = kota(s)
    secs.append(("Bantuan di Kota Anda", f'<p>Halaman jasa laporan keuangan per kota di FA Indonesia:</p><details><summary>{sum(len(v) for v in kt.values())} kota</summary>'
                 + "".join(f'<p><b>{E(pv)}:</b> ' + " · ".join(f'<a href="{FA}/jasa-penyusunan-laporan-keuangan/{sl(k)}/">{E(k)}</a>' for k in ks) + "</p>" for pv, ks in kt.items()) + "</details>"))
    faq_h = "".join(f"<h3>{E(q)}</h3><p>{E(a)}</p>" for q, a in s["faq"])
    secs.insert(len(secs) - 2, ("Tanya Jawab", faq_h))
    pmap = '<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>' + "".join(f'<li><a href="#{hid(h)}">{E(h)}</a></li>' for h, _ in secs) + "</ol></nav>"
    tanya = ('<!--us-tanya--><section class="us-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Ananta, CPA</b><p>Ada kasus di usaha Anda yang mirip? Tanyakan lewat WhatsApp, gratis.</p><div class="q">'
             f'<a class="w" href="{wa(chr(34).join(["Halo Pak Ananta, saya baca ", s["us_h1"], " di updatesak.com. Mau tanya untuk usaha kami: "]))}" target="_blank" rel="noopener" data-us-q="ind">Tanya soal topik ini untuk usaha saya</a>'
             f'<a class="" href="{wa("Halo Pak Ananta, kami usaha " + s["nama"].lower() + " dan perlu dibantu soal pembukuan dan laporan keuangan.")}" target="_blank" rel="noopener" data-us-q="ind">Minta dibantu mengerjakannya</a></div></section><!--/us-tanya-->')
    body = pmap
    for k, (h, b) in enumerate(secs):
        body += f'<h2 id="{hid(h)}">{E(h)}</h2>{b}' + (tanya if k == 0 else "")
    share_u = urllib.parse.quote(url, safe="")
    art = (f'<article class="art"><div class="wrap">\n<nav class="crumb"><a href="/">Beranda</a> / {E(s["us_h1"].split(":")[0])}</nav>\n'
           f'<p class="label">Panduan · Diperbarui {UPD}</p>\n<h1>{E(s["us_h1"])}</h1>\n<p class="lede">{E(s["us_lede"])}</p>\n'
           f'<p class="upd">Tim UpdateSAK · Diperbarui {UPD} · Ditinjau Ananta W. Sasongko, CPA</p>\n<div class="share"><span>Bagikan</span>\n'
           f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={share_u}" rel="noopener" target="_blank">LinkedIn</a>\n'
           f'<a href="https://wa.me/?text={urllib.parse.quote(s["us_h1"] + " " + url, safe="")}" rel="noopener" target="_blank">WhatsApp</a>\n'
           f'<button data-copy="{url}" type="button">Salin Link</button></div>\n<div class="prose">{body}</div>\n'
           '<h2>Bacaan Terkait</h2><div class="reads">' + "".join(f'<a href="{u}"><b>{E(n)}</b></a>' for u, n in
               [("/penerapan-psak/", "Penerapan PSAK"), ("/buku-besar/", "Buku Besar"), ("/menghadapi-auditor/", "Menghadapi Auditor"), ("/update-sak-emkm/", "Update SAK EMKM")]) + "</div>\n"
           '<h2>Sumber</h2><ul><li><a href="https://web.iaiglobal.or.id/SAK-Online" rel="noopener" target="_blank">SAK Online IAI</a></li></ul>\n'
           f'<aside class="cta-box dark"><div><b>Perlu Dibantu Mengerjakannya?</b><span>Tanyakan dulu lewat WhatsApp, gratis.</span></div><a class="btn arrow" href="{wa("Halo Pak Ananta, kami usaha " + s["nama"].lower() + " dan perlu dibantu soal pembukuan dan laporan keuangan.")}" rel="noopener" target="_blank">Tanya Ananta, CPA</a></aside>\n</div></article>')
    t = re.sub(r'<article class="art"><div class="wrap">.*?</div></article>', lambda m: art, UT, count=1, flags=re.S)
    g = [{"@type": "Article", "headline": s["us_h1"], "description": s["us_desc"], "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "id",
          "author": {"@type": "Organization", "name": "Tim UpdateSAK"}, "reviewedBy": {"@type": "Person", "name": "Ananta W. Sasongko, CPA"},
          "publisher": {"@type": "Organization", "name": "UpdateSAK", "url": US + "/"}, "mainEntityOfPage": url},
         {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": US + "/"},
                                                         {"@type": "ListItem", "position": 2, "name": s["us_h1"].split(":")[0], "item": url}]}, faq_ld(s["faq"])]
    t = head_sw(t, s["us_title"], s["us_desc"], url, g)
    newq = wa(f'Halo Pak Ananta, saya baca {s["us_h1"]} di updatesak.com. Mau tanya: ')
    for q in OLDQ: t = t.replace(q, newq if "menerapkan" not in q else wa(f'Halo Pak Ananta, kami ingin dibantu menerapkan {s["us_h1"]} di laporan keuangan perusahaan kami.'))
    n_us += wt(P("updatesak", path), t)

# link masuk US
NAMA = {"restoran-cafe": "Restoran dan Cafe", "manufaktur": "Manufaktur", "travel-umrah": "Travel Umrah", "umkm": "UMKM",
        "kontraktor": "Kontraktor", "hotel": "Hotel", "distributor": "Distributor"}
line = ('<!--us-ind--><p class="kw3">Akuntansi per industri: <a href="/akuntansi-rumah-sakit/">Rumah Sakit</a> · '
        + " · ".join(f'<a href="/akuntansi-{s["slug"]}/">{NAMA[s["slug"]]}</a>' for s in SEG) + "</p><!--/us-ind-->")
n_usl = 0
for p in glob.glob(os.path.join(OUT, "updatesak", "**", "index.html"), recursive=True):
    t = rd(p)
    if "<!--/us-kw3-->" not in t: continue
    t2 = re.sub(r"<!--us-ind-->.*?<!--/us-ind-->", "", t, flags=re.S).replace("<!--/us-kw3-->", "<!--/us-kw3-->" + line, 1)
    n_usl += wt(p, t2)

# ---------------------------------------------------------------- CariAkuntan
CT = rd(P("cariakuntan", "/konsultan-rumah-sakit/"))
n_ca = 0; CA_URLS = []
for s in SEG:
    path = f"/akuntan-{s['slug']}/"; url = CA + path; CA_URLS.append(path)
    lk, au = fa_lk(s), fa_audit(s)
    q = [("Kantor mana yang saya butuhkan?", f"Halo Pak Ananta, saya punya usaha {s['nama'].lower()}. Mau tanya, kantor akuntan seperti apa yang kami butuhkan?"),
         ("Laporan untuk kredit bank", f"Halo Pak Ananta, usaha {s['nama'].lower()} kami perlu laporan keuangan untuk pengajuan kredit bank."),
         ("Perlu audit KAP", f"Halo Pak Ananta, usaha {s['nama'].lower()} kami diminta laporan keuangan yang diaudit KAP.")]
    tanya = ('<!--ca-tanya--><section class="ca-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Dulu ke Ananta, CPA</b><p>Belum yakin harus mulai dari mana? Tanyakan lewat WhatsApp, gratis.</p><div class="q">'
             + "".join(f'<a class="{"w" if k == 0 else ""}" href="{wa(m)}" target="_blank" rel="noopener">{E(l)}</a>' for k, (l, m) in enumerate(q)) + "</div></section><!--/ca-tanya-->")
    need = ('<div class="prose"><h2>Kebutuhan dan Kantor yang Tepat</h2></div><div class="tblwrap"><table class="tbl"><thead><tr><th>Kebutuhan</th><th>Kantor yang Biasanya Dipakai</th></tr></thead><tbody>'
            + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in s["ca_need"]) + "</tbody></table></div>")
    cek = (f'<div class="prose"><h2>Checklist Memilih Akuntan untuk {E(s["nama"])}</h2><p>Tanyakan lima hal ini sebelum menandatangani perikatan:</p><ol>'
           + "".join(f"<li>{E(x)}</li>" for x in s["ca_cek"]) + "</ol></div>")
    rek = (f'<div class="prose"><h2>Rekanan yang Kami Sarankan</h2><p>Untuk {E(s["nama"].lower())} di seluruh Indonesia, penyusunan laporan keuangan dikerjakan KJA Farhani K.N. dan audit oleh KAP DHN &amp; Rekan (terdaftar OJK), '
           f'dengan FA Indonesia sebagai pintu kontaknya. Penyusun dan auditor adalah kantor yang berbeda. Rincian: <a href="{FA}{lk}">Jasa Laporan Keuangan {E(s["nama"])}</a>'
           + (f' · <a href="{FA}{au}">Audit Laporan Keuangan {E(s["nama"])}</a>' if au else "")
           + f'. Ingin paham dulu cara pencatatannya? Baca <a href="{US}/akuntansi-{s["slug"]}/">Akuntansi {E(s["nama"])}</a> di UpdateSAK.</p></div>')
    faq = '<div class="prose"><h2>Tanya Jawab</h2>' + "".join(f"<h3>{E(a)}</h3><p>{E(b)}</p>" for a, b in s["faq"]) + "</div>"
    kt = kota(s)
    kot = (f'<div class="prose"><h2>Cari Kantor di Kota Anda</h2><details class="fold"><summary>{sum(len(v) for v in kt.values())} kota</summary>'
           + "".join(f'<p><b>{E(pv)}:</b> ' + " · ".join(f'<a href="/kota/{sl(k)}/">{E(k)}</a>' for k in ks) + "</p>" for pv, ks in kt.items()) + "</details></div>")
    main = (f'<main class="wrap art">\n<p class="crumb"><a href="/">Beranda</a> / <a href="{path}">Akuntan untuk {E(s["nama"])}</a></p>\n<p class="label" style="margin-top:14px">Seluruh Indonesia</p>\n'
            f'<h1>{E(s["ca_h1"])}</h1><div class="tshare-top"><div class="share" data-tool="{E(s["ca_h1"])}" data-lab="Bagikan"></div></div>\n<p class="sub">{E(s["ca_sub"])}</p>\n'
            f'<div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center"><a class="btn btn-wa arrow" href="{wa(q[0][1])}" rel="noopener" target="_blank">Tanya Ananta, CPA</a><span style="color:var(--muted);font-size:.9rem">Diskusi Awal tanpa Biaya</span></div>'
            + tanya + "\n" + need + cek + rek + faq + "\n" + kot + "\n</main>")
    t = re.sub(r'<main class="wrap art">.*?</main>', lambda m: main, CT, count=1, flags=re.S)
    g = [{"@type": "Service", "name": s["ca_title"], "serviceType": "Akuntan untuk " + s["nama"], "areaServed": {"@type": "Country", "name": "Indonesia"},
          "provider": {"@type": "ProfessionalService", "name": "cariakuntan.com", "url": CA + "/"}, "url": url, "description": s["ca_desc"]}, faq_ld(s["faq"])]
    t = head_sw(t, s["ca_title"], s["ca_desc"], url, g)
    t = t.replace(urllib.parse.quote("saya dari cariakuntan.com (KAP Malang). Mau tanya: ", safe=""),
                  urllib.parse.quote(f"saya dari cariakuntan.com (Akuntan untuk {s['nama']}). Mau tanya: ", safe=""))
    n_ca += wt(P("cariakuntan", path), t)

# link masuk CA: lipatan di hub kota
CS = {"wisata": ["hotel", "restoran-cafe"], "manufaktur": ["manufaktur"], "smelter": ["manufaktur"], "konstruksi": ["kontraktor"],
      "properti": ["kontraktor"], "dagang": ["distributor"], "logistik": ["distributor"]}
n_cal = 0
for nm, pv, rg, sek, cat in CITIES:
    p = P("cariakuntan", f"/kota/{sl(nm)}/")
    if not os.path.exists(p): continue
    t = rd(p); base = re.sub(r"<!--ca-seg-->.*?<!--/ca-seg-->", "", t, flags=re.S)
    if "<!--/ca-kw3h-->" not in base: continue
    order = []
    for x in sum((CS.get(z, []) for z in sek), []) + ["umkm", "restoran-cafe", "travel-umrah", "distributor", "kontraktor", "manufaktur", "hotel"]:
        if x not in order: order.append(x)
    blk = (f'<!--ca-seg--><details class="fold"><summary>Akuntan per Jenis Usaha di {E(nm)}</summary><div class="citylist">'
           + " ".join(f'<a href="/akuntan-{x}/">Akuntan {E(next(s["nama"] for s in SEG if s["slug"] == x))}</a>' for x in order) + "</div></details><!--/ca-seg-->")
    n_cal += wt(p, base.replace("<!--/ca-kw3h-->", "<!--/ca-kw3h-->" + blk, 1))

# ---------------------------------------------------------------- FA: baris Bacaan di pilar industri
n_fa = 0
for s in SEG:
    line = (f'<!--fa-indedu--><p class="t"><b>Bacaan:</b> <a href="{US}/akuntansi-{s["slug"]}/">Akuntansi {E(s["nama"])} (UpdateSAK)</a> · '
            f'<a href="{CA}/akuntan-{s["slug"]}/">Memilih Akuntan untuk {E(s["nama"])} (CariAkuntan)</a></p><!--/fa-indedu-->')
    for u in [x for x in (fa_audit(s), fa_lk(s)) if x]:
        p = P("faindonesia", u)
        if not os.path.exists(p): print("FA tidak ada", u); continue
        t = rd(p); base = re.sub(r"<!--fa-indedu-->.*?<!--/fa-indedu-->", "", t, flags=re.S)
        m = re.search(r'<h2[^>]*>Pertanyaan Umum</h2>', base) or re.search(r'<div class="faq-acc">', base)
        if not m: print("FA tanpa jangkar", u); continue
        n_fa += wt(p, base[:m.start()] + line + base[m.start():])

# ---------------------------------------------------------------- sitemap + llms
for site, dom, mk, urls, label in (("updatesak", US, "usind", US_URLS, "Akuntansi per Industri (13 Nov 2026)"),
                                    ("cariakuntan", CA, "caseg", CA_URLS, "Akuntan per Jenis Usaha (13 Nov 2026)")):
    sm = os.path.join(OUT, site, "sitemap.xml"); x = rd(sm)
    x = re.sub(rf"<!--{mk}-->.*?<!--/{mk}-->\n?", "", x, flags=re.S)
    wt(sm, x.replace("</urlset>", f"<!--{mk}-->" + "".join(f"<url><loc>{dom}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + f"<!--/{mk}-->\n</urlset>"))
    lp = os.path.join(OUT, site, "llms.txt"); l = rd(lp)
    l = re.sub(rf"\n<!--{mk}-->.*?<!--/{mk}-->", "", l, flags=re.S)
    tt = {u: (s["us_title"] if site == "updatesak" else s["ca_title"]) for u, s in zip(urls, SEG)}
    wt(lp, l.rstrip("\n") + f"\n<!--{mk}-->\n\n## {label}\n" + "".join(f"- [{tt[u]}]({dom}{u})\n" for u in urls) + f"<!--/{mk}-->\n")
print(f"US halaman {n_us}, link US {n_usl}; CA halaman {n_ca}, link kota CA {n_cal}; FA pilar {n_fa}")
