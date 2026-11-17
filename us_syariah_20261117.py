#!/usr/bin/env python3
"""UpdateSAK: 11 halaman PSAK syariah 402-412 + kotak nomor lama/baru di PSAK 102-112 (17 Nov 2026).

Pemicu (Bos): pencarian "PSAK 105" di Google tidak menampilkan CA/US. Google (AI Overview) membaca
"PSAK 105" sebagai Akuntansi Mudharabah, padahal sejak 1 Januari 2024 standar itu bernomor PSAK 405
dan nomor PSAK 105 dipakai untuk aset dimiliki untuk dijual. US belum punya halaman PSAK 402-412.

Isi (out/updatesak, idempoten, --dry):
 1. /psak/402/ s.d. /psak/412/ dari template /psak/401/ live (data: updatesak/syariah_20261117.py).
    Title memuat nomor lama ("PSAK 405 Mudharabah (dulu PSAK 105): Ringkasan dan Jurnal").
 2. Kotak <!--us-syr--> di /psak/102/ ... /psak/112/ yang ada: "Mencari PSAK 105 lama tentang Mudharabah?
    Sejak 2024 nomornya PSAK 405" + description menyebut kedua makna.
 3. Chip di /eksplor/ (<!--us-syr4-->), /update-sak-syariah-terbaru/ (<!--us-syr4h-->), navigasi 401,
    sitemap (<!--ussyr-->), llms.txt.
Jalankan setelah caus_hero_fa_20261117.py.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
US = os.path.join(ROOT, "out", "updatesak")
DRY = "--dry" in sys.argv
sys.path.insert(0, os.path.join(ROOT, "updatesak"))
from syariah_20261117 import S  # noqa: E402

E = lambda s: html.escape(s, quote=True)
WA = "https://wa.me/6282245260121?text="
TODAY = "2026-11-17"
nchg = 0


def q(s):
    from urllib.parse import quote
    return quote(s, safe="")


def write(p, t):
    global nchg
    old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
    if old != t:
        nchg += 1
        if not DRY:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8").write(t)


def read(rel):
    return open(os.path.join(US, rel), encoding="utf-8").read()


def h1_of(rel):
    p = os.path.join(US, rel)
    if not os.path.exists(p):
        return None
    m = re.search(r"<h1[^>]*>(.*?)</h1>", read(rel), re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else None


def fit(c, n):
    for x in c:
        if len(x) <= n:
            return x
    return c[-1][:n]


BY = {d["no"]: d for d in S}


def chip(no):
    if no in BY:
        return f'<a class="pchip" href="/psak/{no}/"><b>PSAK {no}</b><span>{E(BY[no]["nama"])}</span></a>'
    h = h1_of(f"psak/{no}/index.html") or f"PSAK {no}"
    nm = re.sub(r"^PSAK \d+\s*", "", h)
    nm = re.sub(r":\s*Ringkasan.*$", "", nm)
    return f'<a class="pchip" href="/psak/{no}/"><b>PSAK {no}</b><span>{E(nm)}</span></a>'


def main_html(d, prev, nxt):
    no, old, nama = d["no"], d["old"], d["nama"]
    code = f"PSAK {no}"
    newold = h1_of(f"psak/{old}/index.html")
    newold_nm = re.sub(r"^PSAK \d+\s*", "", newold) if newold else None
    share_u = q(f"https://updatesak.com/psak/{no}/")
    o = []
    o.append(f'<header class="rxh"><nav class="crumb"><a href="/">Beranda</a> / <a href="/eksplor/">Eksplor</a> / <a href="/eksplor/#standar">Daftar PSAK</a> / {code}</nav>\n')
    o.append(f'<p class="label">Seri 400 · SAK Syariah · Dulu PSAK {old}</p>\n<h1>{code} {E(nama)}</h1>\n<p class="lede">{E(d["lede"])}</p>\n')
    o.append('<p class="upd">Penomoran sesuai SAK Online IAI · Diperbarui 17 November 2026 · Ditinjau Ananta W. Sasongko, CPA</p>\n')
    o.append(f'<div class="share"><span>Bagikan</span>\n<a href="https://www.linkedin.com/sharing/share-offsite/?url={share_u}" rel="noopener" target="_blank">LinkedIn</a>\n'
             f'<a href="https://wa.me/?text={q(code + " " + nama + " https://updatesak.com/psak/" + no + "/")}" rel="noopener" target="_blank">WhatsApp</a>\n'
             f'<button data-copy="https://updatesak.com/psak/{no}/" type="button">Salin Link</button></div>')
    o.append(f'<!--rx17b--><div class="rxb"><a class="btn" href="{WA}{q("Halo Pak Ananta, saya baca " + code + " di updatesak.com. Mau tanya: ")}" rel="noopener" target="_blank" data-us-q="hero">Chat Ananta, CPA</a>'
             '<a class="btn rxg" href="/#dibantu">Dikerjakan Tim FA</a></div><!--/rx17b--></header>\n')
    note = f'Sebelum 1 Januari 2024 standar ini bernomor <strong>PSAK {old}</strong>. Skripsi dan buku lama masih memakai nomor itu.'
    if newold_nm:
        note += f' Nomor PSAK {old} sekarang dipakai untuk standar lain: <a href="/psak/{old}/">PSAK {old} {E(newold_nm)}</a>.'
    o.append(f'<aside class="us-syr"><b>Nomor Lama: PSAK {old}</b>{note}</aside>\n')
    toc = [("inti-pengaturan", "Inti Pengaturan"), ("contoh-jurnal", "Contoh Jurnal"), ("contoh-kalimat-kebijakan-akuntansi-di-calk", "Contoh Kalimat Kebijakan Akuntansi di CALK"),
           ("langkah-penerapan", "Langkah Penerapan"), ("yang-sering-dipersoalkan-auditor", "Yang Sering Dipersoalkan Auditor"), ("standar-terkait", "Standar Terkait")]
    o.append('<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>' + "".join(f'<li><a href="#{a}">{b}</a></li>' for a, b in toc) + "</ol></nav>")
    o.append('<h2 id="inti-pengaturan">Inti Pengaturan</h2>\n<div class="keys">' + "".join(f"<div><b>{i:02d}</b><span>{E(k)}</span></div>" for i, k in enumerate(d["keys"], 1)) + "</div>\n")
    o.append('<h2 id="contoh-jurnal">Contoh Jurnal</h2>\n')
    for cap, rows in d["jurnal"]:
        o.append(f"<p><b>{E(cap)}</b></p>\n<div class=\"tx\"><table><thead><tr><th>Akun</th><th>Debit</th><th>Kredit</th></tr></thead><tbody>"
                 + "".join(f"<tr><td>{'&nbsp;&nbsp;&nbsp;&nbsp;' if c and not db else ''}{E(a)}</td><td>{db}</td><td>{c}</td></tr>" for a, db, c in rows) + "</tbody></table></div>\n")
    o.append(f'<p class="note">{E(d["jnote"])}</p>\n')
    o.append(f'<h2 id="contoh-kalimat-kebijakan-akuntansi-di-calk">Contoh Kalimat Kebijakan Akuntansi di CALK</h2>\n<blockquote class="calk">{E(d["calk"])}</blockquote>\n'
             '<p class="note">Sesuaikan dengan fakta entitas. Kalimat ini ditulis ulang oleh tim UpdateSAK dan bukan kutipan teks standar.</p>\n')
    o.append(f'<h2 id="langkah-penerapan">Langkah Penerapan</h2><p>Urutan kerja yang biasa dipakai saat menerapkan {code} sebelum laporan keuangan diserahkan ke auditor, dewan pengawas syariah, atau regulator.</p>'
             '<ol class="us-steps">' + "".join(f"<li>{E(x)}</li>" for x in d["langkah"]) + "</ol>")
    qs = [(f"Apakah {code} berlaku untuk entitas saya?", f"Halo Pak Ananta, saya baca {code} di updatesak.com. Apakah {code} berlaku untuk entitas kami? Usaha kami: ", "w"),
          (f"Contoh jurnal {code} untuk kasus saya", f"Halo Pak Ananta, kami perlu contoh jurnal dan CALK {code} untuk kasus kami. Kasusnya: ", ""),
          (f"Persiapan {code} sebelum diaudit", f"Halo Pak Ananta, laporan keuangan kami akan diaudit. Kami ingin siapkan penerapan {code} dulu.", "")]
    o.append(f'<!--us-tanya--><section class="us-tanya" aria-label="Chat Ananta, CPA"><b class="t">Punya Kasus Nyata?</b><p>Sedang menerapkan {code} di laporan keuangan? Pilih pertanyaan di bawah, pesan WhatsApp sudah tersusun. Diskusi awal tanpa biaya.</p><div class="q">'
             + "".join(f'<a class="{c}" href="{WA}{q(m)}" target="_blank" rel="noopener" data-us-q="psak">{E(t)}</a>' for t, m, c in qs) + "</div></section><!--/us-tanya-->")
    o.append('<h2 id="yang-sering-dipersoalkan-auditor">Yang Sering Dipersoalkan Auditor</h2>\n<ul class="flags">' + "".join(f"<li>{E(x)}</li>" for x in d["flags"]) + "</ul>\n")
    o.append('<h2 id="standar-terkait">Standar Terkait</h2>\n<div class="pchips">' + "".join(chip(r) for r in d["rel"]) + "</div>\n")
    o.append("<h2>Tanya Jawab</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in d["faq"]) + "\n")
    o.append(f'<aside class="cta-box dark"><div><b>Butuh Pendampingan Penerapan {code}?</b><span>Tim akuntan bersertifikat CA dan CPA, terbiasa dengan prosedur auditor Big 4.</span></div>'
             f'<a class="btn arrow" href="{WA}{q("Halo Pak Ananta, saya butuh pendampingan Penerapan " + code + ".")}" rel="noopener" target="_blank">Chat Ananta, CPA</a></aside>\n')
    pn = ""
    if prev:
        pn += f'<a href="/psak/{prev}/">← PSAK {prev}</a>'
    if nxt:
        pn += f'<a href="/psak/{nxt}/">PSAK {nxt} →</a>'
    o.append(f'<nav class="pn">{pn}</nav>\n')
    return "".join(o)


SYR_CSS = ('<style id="us-syr">.us-syr{margin:0 0 26px;padding:16px 18px;border:1px solid var(--line);border-left:2px solid #141414;background:#F7F7F5;font-size:.95rem;line-height:1.6}'
           '.us-syr>b{display:block;margin-bottom:4px;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase}.us-syr strong{display:inline!important;margin:0!important;font-size:inherit!important;letter-spacing:0!important;text-transform:none!important;font-weight:700}.us-syr a{font-weight:600}</style>')


def build_pages():
    tpl = read("psak/401/index.html")
    a = tpl.find('<main>\n<article class="art"><div class="wrap">\n')
    b = tpl.find("</div></article>\n</main>")
    assert a > 0 and b > a
    head, tail = tpl[: a + len('<main>\n<article class="art"><div class="wrap">\n')], tpl[b:]
    nos = [d["no"] for d in S]
    for i, d in enumerate(S):
        no, old = d["no"], d["old"]
        code = f"PSAK {no}"
        title = fit(([f"{code} {d['short']} (dulu PSAK {old}): Ringkasan dan Jurnal"] if d["jurnal"] else []) + [f"{code} {d['short']} (dulu PSAK {old}): Ringkasan", f"{code} {d['short']} (dulu PSAK {old})"], 65)
        desc = fit([f"{code} {d['nama']}, dulu PSAK {old}: ringkasan pengaturan, contoh jurnal, kalimat CALK, dan temuan auditor yang sering muncul.",
                    f"{code} {d['nama']}, dulu PSAK {old}: ringkasan, contoh jurnal, dan kalimat CALK."], 158)
        h = head.replace("psak/401/", f"psak/{no}/").replace("PSAK%20401", f"PSAK%20{no}")
        h = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", h, count=1, flags=re.S)
        for p in ("description", "og:description"):
            h = re.sub(r'(<meta content=")[^"]*(" (?:name|property)="%s"/>)' % p, lambda m: m.group(1) + E(desc) + m.group(2), h)
        h = re.sub(r'(<meta content=")[^"]*(" property="og:title"/>)', lambda m: m.group(1) + E(title) + m.group(2), h)
        h = re.sub(r'<meta content="[^"]*psak-401-og\.jpg" property="og:image"/>\n?', "", h)
        h = h.replace('<meta content="summary_large_image" name="twitter:card"/>', '<meta content="summary" name="twitter:card"/>')
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "headline": f"{code} {d['nama']}", "description": desc, "inLanguage": "id", "url": f"https://updatesak.com/psak/{no}/",
             "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": "Tim UpdateSAK", "url": "https://updatesak.com/"},
             "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": "https://faindonesia.co.id/"}},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "UpdateSAK", "item": "https://updatesak.com/"},
                {"@type": "ListItem", "position": 2, "name": "Eksplor", "item": "https://updatesak.com/eksplor/"},
                {"@type": "ListItem", "position": 3, "name": code, "item": f"https://updatesak.com/psak/{no}/"}]},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x, "acceptedAnswer": {"@type": "Answer", "text": y}} for x, y in d["faq"]]}]}
        h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", h, count=1, flags=re.S)
        h = re.sub(r'<style id="us-syr">.*?</style>', "", h)
        h = h.replace("</head>", SYR_CSS + "</head>", 1)
        tl = tail.replace("PSAK%20401", f"PSAK%20{no}").replace("PSAK 401", code)
        prev = "401" if i == 0 else nos[i - 1]
        nxt = nos[i + 1] if i + 1 < len(nos) else None
        page = h + main_html(d, prev, nxt) + tl
        assert "psak-401" not in page and "PSAK 401 " not in page.replace('href="/psak/401/"', ""), no
        write(os.path.join(US, f"psak/{no}/index.html"), page)


def disambig():
    for d in S:
        old = d["old"]
        rel = f"psak/{old}/index.html"
        p = os.path.join(US, rel)
        if not os.path.exists(p):
            continue
        t = read(rel)
        box = (f'<!--us-syr--><aside class="us-syr"><b>Mencari PSAK {old} Lama?</b>PSAK {old} {E(d["nama"])} sejak 1 Januari 2024 bernomor '
               f'<a href="/psak/{d["no"]}/">PSAK {d["no"]} {E(d["nama"])}</a>. Halaman ini membahas PSAK {old} dengan penomoran baru.</aside><!--/us-syr-->')
        t = re.sub(r"<!--us-syr-->.*?<!--/us-syr-->", "", t, flags=re.S)
        st = t.find('<header class="rxh">')
        if st > 0:
            j = t.find("</header>", st) + len("</header>")
            t = t[:j] + box + t[j:]
        t = re.sub(r'<style id="us-syr">.*?</style>', "", t)
        t = t.replace("</head>", SYR_CSS + "</head>", 1)
        h1 = h1_of(rel)
        nm = re.sub(r"^PSAK \d+\s*", "", h1)
        nm = re.sub(r":\s*Ringkasan.*$", "", nm)
        desc = fit([f"PSAK {old} penomoran baru: {nm}. Mencari PSAK {old} lama tentang {d['short']}? Sejak 2024 nomornya PSAK {d['no']}.",
                    f"PSAK {old} baru: {nm}. PSAK {old} lama tentang {d['short']} kini PSAK {d['no']}."], 158)
        for pp in ("description", "og:description", "twitter:description"):
            t = re.sub(r'(<meta content=")[^"]*(" (?:name|property)="%s"/>)' % pp, lambda m: m.group(1) + E(desc) + m.group(2), t)
        write(p, t)


def hubs():
    chips = "".join(chip(d["no"]) for d in S)
    rel = "eksplor/index.html"
    t = read(rel)
    t = re.sub(r"<!--us-syr4-->.*?<!--/us-syr4-->", "", t, flags=re.S)
    anc = '<a class="pchip" href="/psak/401/"><b>PSAK 401</b><span>Penyajian dan Pengungkapan dalam Laporan Keuangan Syariah</span></a>'
    assert anc in t
    t = t.replace(anc, anc + "<!--us-syr4-->" + chips + "<!--/us-syr4-->", 1)
    write(os.path.join(US, rel), t)
    rel = "update-sak-syariah-terbaru/index.html"
    p = os.path.join(US, rel)
    if os.path.exists(p):
        t = read(rel)
        t = re.sub(r"<!--us-syr4h-->.*?<!--/us-syr4h-->", "", t, flags=re.S)
        blk = ('<!--us-syr4h--><h2 id="ringkasan-per-standar">Ringkasan per Standar Syariah</h2><p>Nomor baru sejak 1 Januari 2024, nomor lama di kurung.</p><div class="pchips">'
               + chip("401") + "".join(f'<a class="pchip" href="/psak/{d["no"]}/"><b>PSAK {d["no"]} (dulu {d["old"]})</b><span>{E(d["nama"])}</span></a>' for d in S)
               + "</div><!--/us-syr4h-->")
        i = t.find("</header>", t.find('<header class="rxh">'))
        if i > 0:
            i += len("</header>")
            t = t[:i] + blk + t[i:]
            write(p, t)
    rel = "psak/401/index.html"
    t = read(rel)
    if 'href="/psak/402/"' not in t.split('<nav class="pn">')[-1][:200]:
        t = t.replace('<nav class="pn"><a href="/psak/370/">← PSAK 370</a></nav>', '<nav class="pn"><a href="/psak/370/">← PSAK 370</a><a href="/psak/402/">PSAK 402 →</a></nav>', 1)
        write(os.path.join(US, rel), t)
    # sitemap + llms
    sm = read("sitemap.xml")
    sm = re.sub(r"<!--ussyr-->.*?<!--/ussyr-->", "", sm, flags=re.S)
    urls = "".join(f"<url><loc>https://updatesak.com/psak/{d['no']}/</loc><lastmod>{TODAY}</lastmod></url>" for d in S)
    sm = sm.replace("</urlset>", "<!--ussyr-->" + urls + "<!--/ussyr--></urlset>", 1)
    write(os.path.join(US, "sitemap.xml"), sm)
    ll = read("llms.txt")
    ll = re.sub(r"\n?<!--ussyr-->.*?<!--/ussyr-->", "", ll, flags=re.S)
    lines = "\n".join(f"- [PSAK {d['no']} {d['nama']} (dulu PSAK {d['old']})](https://updatesak.com/psak/{d['no']}/): {d['lede']}" for d in S)
    ll = ll.rstrip("\n") + "\n<!--ussyr-->\n## PSAK Syariah (nomor baru, dulu PSAK 1xx)\n" + lines + "\n<!--/ussyr-->\n"
    write(os.path.join(US, "llms.txt"), ll)


if __name__ == "__main__":
    build_pages()
    disambig()
    hubs()
    print("berubah:", nchg, "(dry)" if DRY else "")
