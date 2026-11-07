#!/usr/bin/env python3
"""FA Venus Advanced Hospital Toolkit (7 Nov 2026, permintaan Bos).

Membuat 5 halaman di out/faindonesia (BEKERJA LANGSUNG DI out/, jalankan SETELAH prep.py,
lihat PERINGATAN BUILD di README-DEPLOY.md):
  /fa-venus-rumah-sakit/                  hub Advanced Hospital Toolkit
  /kalkulator-unit-cost-rumah-sakit/      Advanced Unit Cost berbasis Activity Based Costing
  /analisis-abc-ven-obat-rumah-sakit/     Advanced Drug Management (ABC-VEN, EOQ, ROP, ITOR, ED)
  /cek-koding-bpjs-ina-cbg/               Advanced BPJS Coding (under/over coding, pending, dispute)
  /analis-ai-rumah-sakit/                 AI Analis RS, Powered by Claude (/api/ai/ask, app venus-rs-ai)
Template: halaman live /kalkulator-valuasi-rumah-sakit/ (head, header, footer, CSS, tim RS).
Sumber konten: fa_content/rs_advanced/*.html (+ common.css, common.js).
Gratis dicoba; laporan lengkap = tombol WA berisi link prefill ?...&laporan=1 (Bos buka di laptop,
otomatis print ke PDF, kirim lewat WA). Tanpa kata "bayar" dan tanpa harga di muka.
Juga menyisipkan (penanda fa-rsadv): kartu di /apps/, blok link di pilar RS/klinik/unit cost/farmasi/BPJS
dan valuasi RS, sitemap.xml, llms.txt. Idempoten.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out", "faindonesia")
SRC = os.path.join(ROOT, "fa_content", "rs_advanced")
BASE = "https://faindonesia.co.id"
TPL_PATH = os.path.join(OUT, "kalkulator-valuasi-rumah-sakit", "index.html")
OLD_TOOL = "RS Dijual Tapi Belum Ada Pembeli? Hitung Harga Before dan After"
TODAY = "2026-11-07"

PAGES = [
    dict(slug="fa-venus-rumah-sakit", src="hub.html", app=None, ai_js=False,
         title="Tools Konsultan Rumah Sakit: Unit Cost ABC, Obat, Koding BPJS, AI | FA Venus",
         desc="Advanced Hospital Toolkit FA Venus: unit cost RS berbasis ABC, analisis ABC-VEN obat, cek koding BPJS INA-CBG, AI analis RS berbasis Claude. Gratis dicoba.",
         tool="Advanced Hospital Toolkit FA Venus", name="FA Venus · Advanced Hospital Toolkit", short="Advanced Hospital Toolkit"),
    dict(slug="kalkulator-unit-cost-rumah-sakit", src="abc.html", app="venus-rs-abc", ai_js=True,
         title="Kalkulator Unit Cost Rumah Sakit Berbasis Activity Based Costing (ABC) | FA Indonesia",
         desc="Hitung unit cost rumah sakit per layanan dengan Activity Based Costing: pool overhead, cost driver, unit cost ABC vs tradisional, layanan rugi tersembunyi. Gratis.",
         tool="Unit Cost Rumah Sakit Berbasis Activity Based Costing", name="FA Venus · Unit Cost Rumah Sakit ABC", short="Unit Cost RS ABC"),
    dict(slug="analisis-abc-ven-obat-rumah-sakit", src="obat.html", app="venus-rs-obat", ai_js=True,
         title="Analisis ABC-VEN Obat Rumah Sakit: EOQ, ROP, ITOR, Kedaluwarsa | FA Indonesia",
         desc="Advanced drug management RS: klasifikasi ABC-VEN, EOQ, titik pesan ulang, ITOR, stok berlebih, dan risiko kedaluwarsa. Tempel dari Excel, gratis dicoba.",
         tool="Advanced Drug Management: Analisis ABC-VEN Obat Rumah Sakit", name="FA Venus · Drug Management Rumah Sakit", short="Drug Management RS"),
    dict(slug="cek-koding-bpjs-ina-cbg", src="coding.html", app="venus-rs-coding", ai_js=True,
         title="Cek Koding BPJS INA-CBG: Under-Coding, Pending Klaim, Dispute | FA Indonesia",
         desc="Hitung kebocoran klaim BPJS rumah sakit: under-coding diagnosis sekunder, over-coding, klaim pending, dispute, kas tertahan, dan cek kasus. Gratis dicoba.",
         tool="Advanced BPJS Coding: Cek Kualitas Koding INA-CBG dan Kebocoran Klaim", name="FA Venus · Cek Koding BPJS INA-CBG", short="Cek Koding BPJS"),
    dict(slug="analis-ai-rumah-sakit", src="ai.html", app="venus-rs-ai", ai_js=False,
         title="AI Analis Keuangan Rumah Sakit, Powered by Claude | FA Indonesia",
         desc="Dashboard indikator RS (EBITDA, piutang BPJS, DSCR, BOR, ALOS, TOI, BTO) dan AI analis berbasis Claude dari Anthropic untuk prioritas perbaikan. Gratis dicoba.",
         tool="AI Analis Keuangan dan Operasional Rumah Sakit", name="FA Venus · AI Analis Rumah Sakit", short="AI Analis RS"),
]

CTA2_NEW = ('<h2>Hasilnya Sudah Keluar. Mau Dikerjakan Bersama Tim Rumah Sakit FA?</h2><p>Alat ini membantu membaca angka. Untuk perbaikannya, '
            'tim FA Indonesia bersama praktisi direktur RS mendampingi dari data sampai eksekusi.</p><ul><li>Unit cost, tarif, dan clinical pathway</li>'
            '<li>Farmasi, casemix, dan klaim BPJS</li><li>Turn around keuangan, pendanaan bank dan investor, penjualan RS</li></ul>'
            '<div class="b"><a class="w" href="https://wa.me/6282245260121?text=Halo%20Tim%20FA%20Indonesia%2C%20saya%20baru%20memakai%20tools%20rumah%20sakit%20FA%20Venus%20dan%20ingin%20diskusi." rel="noopener" target="_blank">Konsultasi Gratis via WhatsApp</a>'
            '<a class="l" href="https://faindonesia.co.id/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a><a class="l" href="https://faindonesia.co.id/fa-venus-rumah-sakit/">Tools RS Lainnya</a></div>')


def rd(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def faq_from(content):
    qs = []
    for m in re.finditer(r'<details class="rv-more"><summary><b>(.*?)</b></summary><p>(.*?)</p></details>', content, re.S):
        q = html.unescape(re.sub("<[^>]+>", "", m.group(1)))
        a = html.unescape(re.sub("<[^>]+>", "", m.group(2)))
        qs.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return qs


def ldjson(pg, content):
    url = f"{BASE}/{pg['slug']}/"
    g = []
    if pg["src"] == "hub.html":
        items = [(p["short"], f"{BASE}/{p['slug']}/") for p in PAGES[1:]] + [("Valuasi Rumah Sakit", f"{BASE}/kalkulator-valuasi-rumah-sakit/")]
        g.append({"@type": "CollectionPage", "@id": url, "url": url, "name": pg["title"], "description": pg["desc"], "isPartOf": {"@id": f"{BASE}/#website"},
                  "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": u} for i, (n, u) in enumerate(items)]}})
    else:
        g.append({"@type": "WebApplication", "@id": url + "#app", "name": pg["name"], "url": url, "applicationCategory": "FinanceApplication", "operatingSystem": "Web",
                  "description": pg["desc"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR", "description": "Gratis dicoba; laporan lengkap dikirim lewat WhatsApp"},
                  "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": f"{BASE}/"}})
        g.append({"@type": "WebPage", "@id": url, "url": url, "name": pg["title"], "description": pg["desc"], "isPartOf": {"@id": f"{BASE}/#website"}})
        fq = faq_from(content)
        if fq:
            g.append({"@type": "FAQPage", "mainEntity": fq})
    bc = [("Beranda", f"{BASE}/"), ("Apps", f"{BASE}/apps/")]
    if pg["src"] != "hub.html":
        bc.append(("Advanced Hospital Toolkit", f"{BASE}/fa-venus-rumah-sakit/"))
    bc.append((pg["short"], url))
    g.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(bc)]})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False) + "</script>"


def build_pages():
    tpl = rd(TPL_PATH)
    assert "<!--RSADV-TPL-->" not in tpl
    common_css = rd(os.path.join(SRC, "common.css"))
    common_js = rd(os.path.join(SRC, "common.js"))
    m0 = tpl.index('<main id="top">') + len('<main id="top">')
    m1 = tpl.index('<section class="block">', m0)
    rv_css = tpl[m0:m1].replace("rv_rep", "ra_rep")
    g0 = tpl.index("<!--fa-prod-g-->")
    rs0 = tpl.index("<!--fa-rstim-->")
    rs1 = tpl.index("<!--/fa-rstim-->") + len("<!--/fa-rstim-->")
    rstim = tpl[rs0:rs1]
    ld0 = tpl.index('<script type="application/ld+json">')
    ld1 = tpl.index("</script>", ld0) + len("</script>")
    for pg in PAGES:
        content = rd(os.path.join(SRC, pg["src"])).replace("/*COMMON*/", common_js)
        tim = '<section class="rv-sec">' + rstim + "</section>"
        k = content.find('<section class="rv-sec"><h2>Pertanyaan Umum')
        if k >= 0:
            content = content[:k] + tim + content[k:]
        else:
            content = content.replace("</div></section>\n", tim + "</div></section>\n", 1) if content.rstrip().endswith("</div></section>") else content + tim
        h = tpl[:ld0] + ldjson(pg, content) + tpl[ld1:m0] + rv_css + '<style id="ra-css">' + common_css + "</style>" + content + "\n" + tpl[g0:]
        url = f"{BASE}/{pg['slug']}/"
        old_t = re.search(r"<title>(.*?)</title>", tpl).group(1)
        old_d = re.search(r'<meta content="([^"]*)" name="description"/>', tpl).group(1)
        h = h.replace(f"<title>{old_t}</title>", f"<title>{html.escape(pg['title'], quote=False)}</title>")
        h = h.replace(f'content="{old_t}" property="og:title"', f'content="{html.escape(pg["title"])}" property="og:title"')
        h = h.replace(f'content="{old_d}"', f'content="{html.escape(pg["desc"])}"')
        h = h.replace(f"{BASE}/kalkulator-valuasi-rumah-sakit/", url)
        h = h.replace(OLD_TOOL, pg["tool"])
        # CTA bawah versi RS
        c0 = h.find('<h2>Hasilnya Sudah Keluar.')
        if c0 >= 0:
            c1 = h.index("</section>", c0)
            h = h[:c0] + CTA2_NEW + h[c1:]
        # Asisten AI: app sendiri, atau dilepas (AI page punya panel sendiri, hub tidak perlu)
        tag = re.search(r'<script defer="" src="/js/fa-ai\.js\?v=[^"]+"></script>', h).group(0)
        h = h.replace(tag, (f'<script>window.FA_AI={{app:"{pg["app"]}"}}</script>' + tag) if pg["ai_js"] else "")
        if pg["src"] == "hub.html":
            h = h.replace("<script>window.FA_DONASI=", "<script>window.FA_DONASI_OFF=")
        assert "Chat Ananta" not in content and "—" not in content and " bayar" not in content.lower().replace("/bayar/", "")
        wr(os.path.join(OUT, pg["slug"], "index.html"), h)
        print("page", pg["slug"], len(h))


BLOCK_CSS = ('<style id="fa-rsadv-css">.rsadv{margin:30px 0}.rsadv h2{margin:0 0 6px}.rsadv>p{margin:0 0 14px;opacity:.85}'
             '.rsadv-g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}'
             '.rsadv-g a{display:flex;flex-direction:column;gap:4px;border:1px solid rgba(127,127,127,.35);border-radius:12px;padding:14px;color:inherit;text-decoration:none}'
             '.rsadv-g a:hover{border-color:currentColor}.rsadv-g em{font-style:normal;font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.7}'
             '.rsadv-g b{font-weight:500;line-height:1.3}.rsadv-g span{font-size:13px;opacity:.75;line-height:1.45}'
             '@media(max-width:820px){.rsadv-g{grid-template-columns:1fr 1fr}}@media(max-width:480px){.rsadv-g{grid-template-columns:1fr}}</style>')
CARDS = [("kalkulator-unit-cost-rumah-sakit", "Unit Cost ABC", "Unit Cost RS Berbasis Activity Based Costing", "Unit cost per layanan, layanan rugi tersembunyi"),
         ("analisis-abc-ven-obat-rumah-sakit", "Drug Management", "Analisis ABC-VEN Obat RS", "EOQ, titik pesan ulang, kas terkunci, kedaluwarsa"),
         ("cek-koding-bpjs-ina-cbg", "BPJS Coding", "Cek Koding INA-CBG", "Under-coding, pending, dispute, kas tertahan"),
         ("analis-ai-rumah-sakit", "AI · Claude", "AI Analis Keuangan RS", "Indikator Barber-Johnson dan analisis AI")]


def block(h2="Tools Rumah Sakit FA Venus, Gratis Dicoba"):
    cards = "".join(f'<a href="/{s}/"><em>{e}</em><b>{b}</b><span>{t}</span></a>' for s, e, b, t in CARDS)
    return (f'<!--fa-rsadv-->{BLOCK_CSS}<section class="rsadv" aria-label="Tools rumah sakit"><h2>{h2}</h2>'
            f'<p>Alat yang dipakai tim FA Indonesia saat mendampingi RS dan klinik. Laporan lengkap dikirim lewat WhatsApp. '
            f'<a href="/fa-venus-rumah-sakit/" style="color:inherit">Lihat semua tools RS</a></p><div class="rsadv-g">{cards}</div></section><!--/fa-rsadv-->')


def strip(h):
    return re.sub(r"<!--fa-rsadv-->.*?<!--/fa-rsadv-->", "", h, flags=re.S)


def inject():
    for p in ["konsultan-rumah-sakit", "konsultan-unit-cost-rumah-sakit", "konsultan-farmasi-rumah-sakit", "konsultan-bpjs-rumah-sakit",
              "konsultan-klinik", "kalkulator-valuasi-rumah-sakit"]:
        f = os.path.join(OUT, p, "index.html")
        h = strip(rd(f))
        i = h.index("<!--fa-rstim-->")
        if p == "kalkulator-valuasi-rumah-sakit":
            h = h[:i] + block("Tools Rumah Sakit Lainnya di FA Venus") + h[i:]
        else:
            h = h[:i] + block() + h[i:]
        wr(f, h)
        print("inject", p)
    # /apps/
    f = os.path.join(OUT, "apps", "index.html")
    h = strip(rd(f))
    i = h.index("<!--/fa-venus-top-->") + len("<!--/fa-venus-top-->")
    sec = block("Advanced Hospital Toolkit: Unit Cost ABC, Obat, Koding BPJS, AI Analis").replace('<section class="rsadv"', '<section class="sec rsadv" id="venus-rs"')
    h = h[:i] + sec + h[i:]
    h = h.replace("FA Apps · 19 Aplikasi Live", "FA Apps · 23 Aplikasi Live")
    wr(f, h)
    print("inject apps")
    # sitemap
    f = os.path.join(OUT, "sitemap.xml")
    h = re.sub(r"<!--rsadv-->.*?<!--/rsadv-->", "", rd(f), flags=re.S)
    urls = "".join(f"<url><loc>{BASE}/{p['slug']}/</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>" for p in PAGES)
    anchor = f"<url><loc>{BASE}/kalkulator-valuasi-rumah-sakit/</loc><lastmod>2026-11-04</lastmod></url>"
    assert anchor in h
    h = h.replace(anchor, anchor + "<!--rsadv-->" + urls + "<!--/rsadv-->", 1)
    wr(f, h)
    # llms
    f = os.path.join(OUT, "llms.txt")
    h = re.sub(r"\n<!--rsadv-->.*?<!--/rsadv-->", "", rd(f), flags=re.S)
    lines = "\n".join(f"- {p['name'].replace('FA Venus · ', 'FA Venus ')}: {p['desc']} → {BASE}/{p['slug']}/" for p in PAGES)
    anchor = "- Aplikasi unggulan FA Venus: Valuasi Rumah Sakit (harga jual RS before dan after) → https://faindonesia.co.id/kalkulator-valuasi-rumah-sakit/"
    assert anchor in h
    h = h.replace(anchor, anchor + "\n<!--rsadv-->\n" + lines + "\n<!--/rsadv-->", 1)
    wr(f, h)
    print("sitemap + llms")


if __name__ == "__main__":
    build_pages()
    inject()
