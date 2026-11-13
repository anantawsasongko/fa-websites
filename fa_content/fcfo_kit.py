# -*- coding: utf-8 -*-
"""Perangkat bersama halaman Fractional CFO bilingual (13 Nov 2026): template, CSS, kartu profil, harga, sub-menu produk, page().
Dipakai fa_fcfo_lokal_20261113.py (halaman kabupaten/kecamatan) dan fa_fcfo_produk_20261113.py (halaman produk)."""
import os, re, json, html, urllib.parse, hashlib
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "out", "faindonesia")
E = html.escape; D = "https://faindonesia.co.id"; TODAY = "2026-11-13"
NAME = "Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP"
def rd(p): return open(p, encoding="utf-8").read()
def P(u): return os.path.join(OUT, *[x for x in u.strip("/").split("/") if x], "index.html")
def wt(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and rd(p) == t: return 0
    open(p, "w", encoding="utf-8").write(t); return 1
def wa(t): return "https://wa.me/6282245260121?text=" + urllib.parse.quote(t, safe="")
def h(s, n): return int(hashlib.md5(s.encode()).hexdigest(), 16) % n
SUB = [("/fractional-cfo/", "Overview"), ("/fractional-cfo/how-we-work/", "How We Work"), ("/fractional-cfo/pricing/", "Pricing"),
       ("/fractional-cfo/health-check/", "Health Check"), ("/fractional-cfo/pt-pma-groups/", "PT PMA &amp; Groups"),
       ("/fractional-cfo/profit-repatriation/", "Repatriation"), ("/fractional-cfo/fundraising/", "Fundraising"),
       ("/fractional-cfo/due-diligence/", "Due Diligence"), ("/fractional-cfo/lkpm-compliance/", "LKPM &amp; Compliance"),
       ("/fractional-cfo/interim-cfo/", "Interim CFO"), ("/fractional-cfo/for-cfos/", "For Group CFOs"),
       ("/fractional-cfo/team/", "Team"), ("/fractional-cfo/faq/", "FAQ")]
def subnav(cur):
    return ('<nav aria-label="Fractional CFO" class="fcl-sub">' + "".join(
        f'<a href="{u}"' + (' aria-current="page"' if u == cur else "") + f'>{n}</a>' for u, n in SUB) + "</nav>")

T = rd(P("/en/fractional-cfo-bali/"))
CSS = re.search(r'<style id="fcfo-css">.*?</style>', T, re.S).group(0)
X_CSS = ('<style id="fcfol-css">.fcl-bi{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:6px 0 10px}.fcl-bi>div{border-left:2px solid #333;padding-left:16px}'
         '.fcl-bi small{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;opacity:.6;margin-bottom:6px}'
         '.fcl-pr{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}.fcl-pr div{border:1px solid #333;border-radius:12px;padding:14px 16px;background:#1b1b1b}'
         '.fcl-pr b{display:block;font-size:20px;margin:2px 0 6px}.fcl-pr small{font-size:11px;letter-spacing:.16em;text-transform:uppercase;opacity:.7}'
         '.fcl-pr span{display:block;font-size:13px;line-height:1.5;opacity:.8}.fcl-v{column-count:3;column-gap:18px;font-size:14px;line-height:1.7;margin:8px 0 14px}'
         '.fcl-k{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 18px}.fcl-k a{border:1px solid #3a3a3a;border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;color:inherit}'
         '.fcl-k a:hover{border-color:#fff}.fcl-sub{display:flex;gap:6px;overflow-x:auto;padding:0 0 10px;margin:0 0 16px;border-bottom:1px solid #2c2c2c;scrollbar-width:none}'
         '.fcl-sub::-webkit-scrollbar{display:none}.fcl-sub a{flex:0 0 auto;font-size:12.5px;padding:6px 11px;border-radius:999px;border:1px solid #333;color:inherit;text-decoration:none;opacity:.85}'
         '.fcl-sub a[aria-current]{background:#e9b949;color:#111;border-color:#e9b949;opacity:1}.fcl-sub a:hover{opacity:1;border-color:#888}'
         '.fcl-st{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:14px 0 18px}.fcl-st div{border:1px solid #333;border-radius:12px;padding:14px;background:#1b1b1b}'
         '.fcl-st i{font-style:normal;font-size:12px;letter-spacing:.14em;color:#e9b949}.fcl-st b{display:block;margin:4px 0 6px}.fcl-st span{display:block;font-size:13px;line-height:1.5;opacity:.8}'
         '.fcl-tm{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:14px 0}.fcl-tm a{display:block;border:1px solid #333;border-radius:12px;overflow:hidden;background:#1b1b1b;color:inherit;text-decoration:none}'
         '.fcl-tm img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 18%}.fcl-tm div{padding:12px 14px}.fcl-tm b{display:block;font-size:14.5px;line-height:1.35}.fcl-tm span{display:block;font-size:12.5px;opacity:.75;margin-top:4px}'
         '@media(max-width:900px){.fcl-st{grid-template-columns:1fr 1fr}}@media(max-width:720px){.fcl-bi,.fcl-pr,.fcl-st,.fcl-tm{grid-template-columns:1fr}.fcl-v{column-count:2}}</style>')

def profil(W):
    return (f'<div class="fcp"><img alt="{E(NAME)}" decoding="async" height="875" loading="lazy" src="/img/ananta-w-sasongko-cpa-rs.jpg" width="700"/><div>'
            f'<small>Fractional CFO · FA Indonesia</small><b class="nm">{E(NAME)}</b><span class="rl">Fractional CFO for PT PMA · Fractional CFO untuk PT PMA</span><ul>'
            '<li>Certified Public Accountant (CPA), Institut Akuntan Publik Indonesia (IAPI)</li><li>FMVA and FPAP, Corporate Finance Institute</li>'
            '<li>Audit and assurance, Ernst &amp; Young (EY)</li><li>Finance Director and Group CFO roles from Indonesia to Singapore: consolidation, acquisitions, bank financing</li>'
            '<li>Prepared a private company for IPO on the Indonesia Stock Exchange</li></ul>'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn solid" href="{W}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
            '<a class="btn line" href="/ananta-w-sasongko/">Full Profile / Profil Lengkap</a></div></div></div>')
PRICE = ('<div class="fcl-pr"><div><small>CFO Advisory</small><b>USD 2,000 / month</b><span>Fractional CFO: monthly reporting, budget and cash, tax and LKPM, reporting to owners. '
         '<i lang="id">Mulai USD 2.000 per bulan.</i></span></div><div><small>Full Team · Tim Lengkap</small><b>USD 5,000 / month</b><span>Plus bookkeeping (KJA Farhani K.N.), audit readiness with KAP DHN &amp; Rekan, '
         'KJPP valuation, bank financing, IPO readiness. <i lang="id">Mulai USD 5.000 per bulan.</i></span></div></div>'
         '<p class="t" style="font-size:13px;opacity:.8">Indicative, confirmed after a diagnostic; invoiced in rupiah. Audit opinion and KJPP report are separate engagements with the licensed firms. '
         '<span lang="id">Harga indikatif, tagihan dalam rupiah; opini audit dan laporan KJPP adalah perikatan terpisah.</span></p>')
LOCAL = ('<div class="fcl-bi"><div><small>Why a local CFO</small><p>We work on the Indonesian side every day: the KAP that signs your audit, the KJPP your bank accepts, '
         'local bank credit analysts, the tax office, OSS and LKPM. Reports come to you in English.</p></div><div lang="id"><small>Mengapa CFO lokal</small>'
         '<p>Kami bekerja di sisi Indonesia setiap hari: KAP penanda tangan audit, KJPP yang diterima bank, analis kredit bank lokal, kantor pajak, OSS dan LKPM. Laporan tetap tersedia dalam bahasa Inggris.</p></div></div>')

EN_INTRO = [
 "Foreign-owned companies in {loc} need numbers their owners abroad can trust, tax and LKPM filed on time, and books a bank or auditor will accept. A fractional CFO gives you that for a few days a month.",
 "If you run a PT PMA in {loc}, a fractional CFO keeps your reporting in English, your cash under control, and your tax, LKPM, and audit on schedule, without the cost of a full-time hire.",
 "Owners of PT PMA in {loc} often manage from abroad. A fractional CFO is the senior finance person on the Indonesian side who reports to you, the parent, and the bank.",
 "Running a foreign-owned company in {loc} means rupiah books, Indonesian tax and LKPM, and owners who want reports in English. A fractional CFO bridges both sides.",
]
ID_INTRO = [
 "PT PMA di {loc} butuh angka yang dipercaya pemilik di luar negeri, pajak dan LKPM yang tepat waktu, serta pembukuan yang diterima bank dan auditor. Fractional CFO memberikannya beberapa hari dalam sebulan.",
 "Bila Anda mengelola PT PMA di {loc}, fractional CFO menjaga laporan berbahasa Inggris, kas terkendali, serta pajak, LKPM, dan audit tepat jadwal, tanpa biaya CFO penuh waktu.",
 "Pemilik PT PMA di {loc} sering mengelola dari luar negeri. Fractional CFO adalah orang keuangan senior di sisi Indonesia yang melapor ke Anda, induk, dan bank.",
 "Mengelola perusahaan PMA di {loc} berarti pembukuan rupiah, pajak dan LKPM Indonesia, serta pemilik yang ingin laporan berbahasa Inggris. Fractional CFO menjembatani keduanya.",
]

def page(path, title, desc, h1, eyebrow, body, W, faq, crumbs, cur=None):
    url = D + path
    main = (f'<main id="top"><!--fa-fcfol-page-->{CSS}{X_CSS}\n<section class="block">\n<div class="wrap art">\n'
            f'<nav class="crumb" style="font-size:13px;opacity:.75;margin:0 0 10px">' + " / ".join(f'<a href="{u}">{E(n)}</a>' for u, n in crumbs) + "</nav>" + subnav(cur) +
            f'<p class="eyebrow">{E(eyebrow)}</p>\n<h1 style="margin:.2em 0 .5em;font-size:clamp(28px,4vw,46px);line-height:1.14">{E(h1)}</h1>\n'
            + body + "\n</div>\n</section>\n</main>")
    t = re.sub(r'<main id="top">.*?</main>', lambda m: main, T, count=1, flags=re.S)
    t = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", t, count=1, flags=re.S)
    for prop, val in (("og:title", title), ("og:description", desc), ("og:url", url)):
        t = re.sub(rf'<meta content="[^"]*" property="{prop}"/>', f'<meta content="{E(val)}" property="{prop}"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{E(desc)}" name="description"/>', t, count=1)
    t = re.sub(r'<link href="[^"]*" rel="canonical"/><link href="[^"]*" hreflang="en" rel="alternate"/><link href="[^"]*" hreflang="id" rel="alternate"/>',
               f'<link href="{url}" rel="canonical"/>', t, count=1)
    g = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "name": h1, "description": desc, "url": url, "inLanguage": ["en", "id"],
         "provider": {"@type": "Organization", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"},
         "employee": {"@type": "Person", "name": NAME, "jobTitle": "Fractional CFO", "image": D + "/img/ananta-w-sasongko-cpa-rs.jpg", "url": D + "/ananta-w-sasongko/"},
         "priceRange": "USD 2,000 - 5,000 per month"},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": D + u} for i, (u, n) in enumerate(crumbs)]},
        ] + ([{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}] if faq else [])}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + "</script>", t, count=1, flags=re.S)
    return wt(P(path), t)

def fit(*cands):
    for c in cands:
        if len(c) <= 65: return c
    return cands[-1][:65]
def cut(s, n=158):
    if len(s) <= n: return s
    if " CFO paruh waktu" in s:   # buang ekor bahasa Indonesia dulu daripada memotong kalimat
        s2 = s[:s.index(" CFO paruh waktu")]
        if len(s2) <= n: return s2
    s = s[:n].rsplit(" ", 1)[0].rstrip(",;:")
    return s + "."
