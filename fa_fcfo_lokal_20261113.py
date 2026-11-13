# -*- coding: utf-8 -*-
"""13 Nov 2026 (Bos): "Pake bilingual ya agar bule juga nangkap SEO nya. Hanya lokasi Bali, NTT, NTB aja fokusnya di tiap
kota dan kecamatan." Halaman Fractional CFO PT PMA bilingual (EN + ID dalam satu halaman):
  /fractional-cfo/                          hub tiga provinsi
  /fractional-cfo/<kab>/                    41 kabupaten/kota (Bali 9, NTB 10, NTT 22)
  /fractional-cfo/<kab>/<kecamatan>/        ±480 kecamatan
Template: halaman live /en/fractional-cfo-bali/ (kartu profil fcfo-css, header/footer). Isi unik per halaman: profil usaha
kabupaten (fa_content/fcfo_lokal20261113.py), kawasan dikenal investor, daftar desa/kelurahan, kecamatan tetangga, variasi
kalimat per slug. Harga sama dengan halaman regional (USD 2.000 / 5.000, tagihan rupiah). Idempoten.
Link masuk: halaman regional Bali/NTB/NTT (EN + ID) dan baris fcfo di halaman daerah FA (fa_industri_lokal) diarahkan ke
halaman kabupaten; /cfo-paruh-waktu/ ke hub; sitemap <!--fcfol-->; llms.txt.
"""
import os, re, csv, json, html, glob, hashlib, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faindonesia")
sys.path.insert(0, os.path.join(HERE, "shared")); sys.path.insert(0, os.path.join(HERE, "fa_content"))
from lokal import nice
from fcfo_lokal20261113 import PROV, KAB, HOT, FIX
E = html.escape; D = "https://faindonesia.co.id"; TODAY = "2026-11-13"
NAME = "Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP"
def rd(p): return open(p, encoding="utf-8").read()
def P(u): return os.path.join(OUT, *[x for x in u.strip("/").split("/") if x], "index.html")
def wt(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and rd(p) == t: return 0
    open(p, "w", encoding="utf-8").write(t); return 1
def sl(s): return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")
def wa(t): return "https://wa.me/6282245260121?text=" + urllib.parse.quote(t, safe="")
def h(s, n): return int(hashlib.md5(s.encode()).hexdigest(), 16) % n
def nm(t): t = nice(t); return FIX.get(t, t)

W = os.path.join(HERE, "shared", "wilayah")
REG = [r for r in csv.reader(open(os.path.join(W, "regencies.csv"))) if r[1] in PROV]
DIS = [r for r in csv.reader(open(os.path.join(W, "districts.csv"))) if r[1][:2] in PROV]
VIL = {}
for r in csv.reader(open(os.path.join(W, "villages.csv"))):
    if r[1][:2] in PROV: VIL.setdefault(r[1], []).append(nm(r[2]))
names = {}
for c, p, n in REG:
    base = nm(n); names.setdefault(base, []).append(c)
KABS = []
for c, p, n in REG:
    base = nm(n); kota = n.upper().startswith("KOTA")
    slug = sl(base) if len(names[base]) == 1 else ("kota-" if kota else "kabupaten-") + sl(base)
    label = ("Kota " if kota else "Kabupaten ") + base if len(names[base]) > 1 else base
    KABS.append(dict(code=c, prov=p, base=base, label=label, kota=kota, slug=slug))
assert all(k["code"] in KAB for k in KABS), [k for k in KABS if k["code"] not in KAB]
KEC = {k["code"]: [] for k in KABS}
for c, kab, n in DIS:
    KEC[kab].append(dict(code=c, name=nm(n), slug=sl(nm(n)), vil=sorted(VIL.get(c, []))))

T = rd(P("/en/fractional-cfo-bali/"))
CSS = re.search(r'<style id="fcfo-css">.*?</style>', T, re.S).group(0)
X_CSS = ('<style id="fcfol-css">.fcl-bi{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:6px 0 10px}.fcl-bi>div{border-left:2px solid #333;padding-left:16px}'
         '.fcl-bi small{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;opacity:.6;margin-bottom:6px}'
         '.fcl-pr{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}.fcl-pr div{border:1px solid #333;border-radius:12px;padding:14px 16px;background:#1b1b1b}'
         '.fcl-pr b{display:block;font-size:20px;margin:2px 0 6px}.fcl-pr small{font-size:11px;letter-spacing:.16em;text-transform:uppercase;opacity:.7}'
         '.fcl-pr span{display:block;font-size:13px;line-height:1.5;opacity:.8}.fcl-v{column-count:3;column-gap:18px;font-size:14px;line-height:1.7;margin:8px 0 14px}'
         '.fcl-k{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 18px}.fcl-k a{border:1px solid #3a3a3a;border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;color:inherit}'
         '.fcl-k a:hover{border-color:#fff}@media(max-width:720px){.fcl-bi,.fcl-pr{grid-template-columns:1fr}.fcl-v{column-count:2}}</style>')

def profil(W):
    return (f'<div class="fcp"><img alt="{E(NAME)}" decoding="async" height="875" loading="lazy" src="/img/ananta-w-sasongko-cpa-rs.jpg" width="700"/><div>'
            f'<small>Fractional CFO · FA Indonesia</small><b class="nm">{E(NAME)}</b><span class="rl">Fractional CFO for PT PMA · Fractional CFO untuk PT PMA</span><ul>'
            '<li>Certified Public Accountant (CPA), Institut Akuntan Publik Indonesia (IAPI)</li><li>FMVA and FPAP, Corporate Finance Institute</li>'
            '<li>Audit and assurance, Ernst &amp; Young (EY)</li><li>Former Finance Director and Group CFO, multi-entity hospital group</li>'
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

def page(path, title, desc, h1, eyebrow, body, W, faq, crumbs):
    url = D + path
    main = (f'<main id="top"><!--fa-fcfol-page-->{CSS}{X_CSS}\n<section class="block">\n<div class="wrap art">\n'
            f'<nav class="crumb" style="font-size:13px;opacity:.75;margin:0 0 10px">' + " / ".join(f'<a href="{u}">{E(n)}</a>' for u, n in crumbs) + "</nav>"
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
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
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
def faqs(loc, sh):
    return [(f"How much does a fractional CFO cost in {loc}?", f"CFO Advisory starts from USD 2,000 per month and the Full Team package from USD 5,000 per month, confirmed after a diagnostic and invoiced in rupiah. Work is remote with scheduled visits to {loc}."),
            (f"Berapa biaya fractional CFO di {loc}?", f"CFO Advisory mulai USD 2.000 per bulan dan Tim Lengkap mulai USD 5.000 per bulan, dikonfirmasi setelah diagnostik, tagihan dalam rupiah. Kerja jarak jauh dengan kunjungan terjadwal ke {loc}."),
            ("Who audits the company? / Siapa yang mengaudit?", "The statutory audit is by a separate licensed firm, KAP DHN & Rekan, registered with OJK. Audit dilakukan kantor berbeda, KAP DHN & Rekan yang terdaftar OJK.")]

n = 0; URLS = []; BYPROV = {}
for k in KABS:
    pv_short, pv_long, pv_slug = PROV[k["prov"]]
    en_ctx, id_ctx = KAB[k["code"]]
    kpath = f"/fractional-cfo/{k['slug']}/"; BYPROV.setdefault(k["prov"], []).append((kpath, k["label"], len(KEC[k["code"]])))
    loc = f"{k['label']}, {pv_short}"
    W = wa(f"Hello Pak Ananta, we are a PT PMA in {k['label']} ({pv_short}) and would like to discuss fractional CFO support. Business: ...")
    crumbs = [("/fractional-cfo/", "Fractional CFO"), (f"/fractional-cfo-pt-pma-{pv_slug}/", pv_short), (kpath, k["label"])]
    kecs = KEC[k["code"]]
    hot = [f"{c['name']} ({HOT[(k['code'], c['name'])]})" for c in kecs if (k["code"], c["name"]) in HOT]
    body = (f'<div class="fcl-bi"><div><small>English</small><p>{E(EN_INTRO[h(kpath, 4)].format(loc=loc))} {E(k["label"])} at a glance: {E(en_ctx)}.</p></div>'
            f'<div lang="id"><small>Bahasa Indonesia</small><p>{E(ID_INTRO[h(kpath + "i", 4)].format(loc=loc))} Sekilas {E(k["label"])}: {E(id_ctx)}.</p></div></div>'
            + profil(W)
            + f'<h2 id="kecamatan">Areas We Cover in {E(k["label"])} · Kecamatan di {E(k["label"])}</h2>'
            + (f'<p>Known business areas / kawasan usaha: {E("; ".join(hot))}.</p>' if hot else "")
            + '<div class="fcl-k">' + "".join(f'<a href="{kpath}{c["slug"]}/">{E(c["name"])}</a>' for c in kecs) + "</div>"
            + f'<p class="t">{len(kecs)} kecamatan and {sum(len(c["vil"]) for c in kecs)} villages / desa dan kelurahan. Site visits are scheduled; most work runs remotely through a shared folder.</p>'
            + '<details class="faq-i"><summary>Villages by district · Desa per kecamatan</summary><div class="tblwrap"><table class="tbl"><thead><tr><th>Kecamatan</th><th>Villages</th><th>Including / antara lain</th></tr></thead><tbody>'
            + "".join(f'<tr><td><a href="{kpath}{c["slug"]}/">{E(c["name"])}</a></td><td>{len(c["vil"])}</td><td>{E(", ".join(c["vil"][:6]))}</td></tr>' for c in kecs) + "</tbody></table></div></details>"
            + '<h2 id="scope">What the Fractional CFO Does · Lingkup Kerja</h2>'
            + '<div class="fcl-bi"><div><small>English</small><ul><li>Monthly management accounts in English</li><li>Cash and bank control across outlets, platforms, and agents</li>'
              '<li>Budget, 13-week cash flow, project budget</li><li>Tax, withholding on payments abroad, quarterly LKPM</li><li>Shareholder loans and capital injections booked correctly</li>'
              '<li>Audit readiness, bank financing, investor pack, IPO readiness</li></ul></div><div lang="id"><small>Bahasa Indonesia</small><ul><li>Laporan manajemen bulanan berbahasa Inggris</li>'
              '<li>Kendali kas dan bank di outlet, platform, dan agen</li><li>Anggaran, arus kas 13 minggu, anggaran proyek</li><li>Pajak, pemotongan atas pembayaran ke luar negeri, LKPM triwulanan</li>'
              '<li>Pinjaman pemegang saham dan setoran modal tercatat benar</li><li>Kesiapan audit, pembiayaan bank, paket investor, kesiapan IPO</li></ul></div></div>'
            + '<h2 id="pricing">Pricing · Biaya</h2>' + PRICE + LOCAL
            + '<h2 id="faq">FAQ · Pertanyaan Umum</h2><div class="faq-acc">' + "".join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs(k["label"], pv_short)) + "</div>"
            + f'<p class="t">More: <a href="/fractional-cfo-pt-pma-{pv_slug}/">Fractional CFO PT PMA di {E(pv_long)}</a> · <a href="/en/fractional-cfo-{ {"bali":"bali","ntb":"lombok-ntb","ntt":"labuan-bajo-ntt"}[pv_slug] }/">English guide</a> · '
              f'<a href="/audit-laporan-keuangan-pma/provinsi-{sl(pv_long)}/">Audit PT PMA {E(pv_long)}</a> · <a href="/cfo-paruh-waktu/">CFO Paruh Waktu</a></p>'
            + f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px"><a class="btn solid" href="{W}" rel="noopener" target="_blank">Chat Ananta, CPA</a></div>')
    title = fit(f"Fractional CFO {k['label']}, {pv_short} | CFO PT PMA | FA Indonesia", f"Fractional CFO {k['label']}, {pv_short} | CFO PT PMA", f"Fractional CFO {k['label']} | CFO PT PMA")
    desc = cut(f"Fractional CFO for PT PMA in {k['label']}, {pv_short}: English reporting, tax and LKPM, audit, bank financing. From USD 2,000/month. CFO paruh waktu PT PMA di {k['label']}.")
    n += page(kpath, title, desc, f"Fractional CFO in {k['label']}, {pv_short} · CFO Paruh Waktu PT PMA", f"Fractional CFO · PT PMA · {pv_long}", body, W, faqs(k["label"], pv_short), crumbs)
    URLS.append(kpath)
    for i, c in enumerate(kecs):
        cpath = f"{kpath}{c['slug']}/"; locc = f"{c['name']}, {k['label']}"
        Wc = wa(f"Hello Pak Ananta, we are a PT PMA in {c['name']}, {k['label']} ({pv_short}) and would like to discuss fractional CFO support. Business: ...")
        hc = HOT.get((k["code"], c["name"]))
        nb = [kecs[j] for j in (i - 2, i - 1, i + 1, i + 2) if 0 <= j < len(kecs)]
        vil = c["vil"]
        en_hot = f" Investors know the area for {hc}." if hc else ""
        id_hot = f" Kawasan ini dikenal investor lewat {hc}." if hc else ""
        b = (f'<div class="fcl-bi"><div><small>English</small><p>{E(EN_INTRO[h(cpath, 4)].format(loc=locc))}{E(en_hot)} {E(k["label"])} at a glance: {E(en_ctx)}.</p></div>'
             f'<div lang="id"><small>Bahasa Indonesia</small><p>{E(ID_INTRO[h(cpath + "i", 4)].format(loc=locc))}{E(id_hot)} Sekilas {E(k["label"])}: {E(id_ctx)}.</p></div></div>'
             + profil(Wc)
             + f'<h2 id="villages">Villages in {E(c["name"])} · Desa dan Kelurahan</h2>'
             + f'<p>We serve PT PMA in all {len(vil)} villages of Kecamatan {E(c["name"])} / melayani PT PMA di {len(vil)} desa dan kelurahan:</p>'
             + '<div class="fcl-v">' + "".join(f"<div>{E(v)}</div>" for v in vil) + "</div>"
             + '<h2 id="pricing">Pricing · Biaya</h2>' + PRICE + LOCAL
             + f'<h2 id="nearby">Nearby · Kecamatan Sekitar</h2><div class="fcl-k">' + "".join(f'<a href="{kpath}{x["slug"]}/">{E(x["name"])}</a>' for x in nb)
             + f'<a href="{kpath}">All of {E(k["label"])}</a></div>'
             + f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px"><a class="btn solid" href="{Wc}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
               f'<a class="btn line" href="{kpath}">Fractional CFO {E(k["label"])}</a></div>')
        title = fit(f"Fractional CFO {c['name']}, {k['label']} | CFO PT PMA | FA Indonesia", f"Fractional CFO {c['name']}, {k['label']} | CFO PT PMA",
                    f"Fractional CFO {c['name']}, {k['label']}", f"Fractional CFO {c['name']}")
        desc = cut(f"Fractional CFO for PT PMA in {c['name']}, {k['label']}: English reporting, tax and LKPM, audit, bank financing, from USD 2,000/month. CFO paruh waktu PT PMA di {c['name']}.")
        cr = crumbs + [(cpath, c["name"])]
        n += page(cpath, title, desc, f"Fractional CFO in {c['name']}, {k['label']} · CFO PT PMA", f"Fractional CFO · {k['label']} · {pv_short}", b, Wc,
                  [(f"How much does a fractional CFO cost in {c['name']}?", "From USD 2,000 per month for CFO Advisory and USD 5,000 per month for the Full Team, invoiced in rupiah."),
                   (f"Berapa biaya fractional CFO di {c['name']}?", "Mulai USD 2.000 per bulan (CFO Advisory) dan USD 5.000 per bulan (Tim Lengkap), tagihan dalam rupiah.")], cr)
        URLS.append(cpath)

# hub
hb = ('<div class="fcl-bi"><div><small>English</small><p>Fractional CFO for foreign-owned companies (PT PMA) in Bali, West Nusa Tenggara, and East Nusa Tenggara, by regency and district.</p></div>'
      '<div lang="id"><small>Bahasa Indonesia</small><p>Fractional CFO untuk PT PMA di Bali, NTB, dan NTT, per kabupaten/kota dan kecamatan.</p></div></div>'
      + profil(wa("Hello Pak Ananta, we are a PT PMA and would like to discuss fractional CFO support. Location: ... Business: ..."))
      + "".join(f'<h2 id="{PROV[p][2]}">{E(PROV[p][1])}</h2><div class="fcl-k">' + "".join(f'<a href="{u}">{E(l)} <small style="opacity:.6">{c}</small></a>' for u, l, c in BYPROV[p]) + "</div>" for p in ("51", "52", "53"))
      + '<h2 id="pricing">Pricing · Biaya</h2>' + PRICE + LOCAL)
n += page("/fractional-cfo/", "Fractional CFO Bali, NTB, NTT for PT PMA | FA Indonesia",
          "Fractional CFO for PT PMA in Bali, Lombok, Sumbawa, Flores, Sumba, and Timor, by regency and district. From USD 2,000/month. CFO paruh waktu PT PMA.",
          "Fractional CFO for PT PMA in Bali, NTB, and NTT", "Fractional CFO · PT PMA", hb, "", [("Where do you work?", "Bali, NTB, and NTT, remote with scheduled visits.")],
          [("/fractional-cfo/", "Fractional CFO")])
URLS.insert(0, "/fractional-cfo/")

# link masuk: halaman regional (EN + ID) -> daftar kabupaten
def put(u, blk, anchors):
    p = P(u); t = rd(p); base = re.sub(r"<!--fa-fcfol-->.*?<!--/fa-fcfol-->", "", t, flags=re.S)
    for a in anchors:
        m = re.search(a, base)
        if m: return wt(p, base[:m.start()] + blk + base[m.start():])
    print("tanpa jangkar", u); return 0
nl = 0
for p, (sh, lg, ps) in PROV.items():
    blk = (f'<!--fa-fcfol--><h2 id="by-regency">By Regency · Per Kabupaten/Kota</h2><div class="fcl-k" style="display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 18px">'
           + "".join(f'<a href="{u}" style="border:1px solid #3a3a3a;border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;color:inherit">{E(l)}</a>' for u, l, c in BYPROV[p]) + "</div><!--/fa-fcfol-->")
    en = {"bali": "/en/fractional-cfo-bali/", "ntb": "/en/fractional-cfo-lombok-ntb/", "ntt": "/en/fractional-cfo-labuan-bajo-ntt/"}[ps]
    for u in (en, f"/fractional-cfo-pt-pma-{ps}/"):
        nl += put(u, blk, [r'<h2 id="faq">'])
nl += put("/cfo-paruh-waktu/", '<!--fa-fcfol--><p class="t"><b>Per kabupaten dan kecamatan (Bali, NTB, NTT):</b> <a href="/fractional-cfo/">Fractional CFO PT PMA, bilingual</a></p><!--/fa-fcfol-->',
          [r'<div class="head" style="margin-top:36px"><h2 id="tim-kami">'])

sm = os.path.join(OUT, "sitemap.xml"); x = rd(sm); x = re.sub(r"<!--fcfol-->.*?<!--/fcfol-->\n?", "", x, flags=re.S)
wt(sm, x.replace("</urlset>", "<!--fcfol-->" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in URLS) + "<!--/fcfol-->\n</urlset>"))
lp = os.path.join(OUT, "llms.txt"); l = rd(lp); l = re.sub(r"\n<!--fcfol-->.*?<!--/fcfol-->", "", l, flags=re.S)
wt(lp, l.rstrip("\n") + "\n<!--fcfol-->\n\n## Fractional CFO PT PMA per Kabupaten dan Kecamatan, Bali, NTB, NTT (13 Nov 2026)\n"
   f"- [Fractional CFO Bali, NTB, NTT]({D}/fractional-cfo/): hub bilingual\n" + "".join(f"- [Fractional CFO {l}]({D}{u})\n" for p in BYPROV for u, l, c in BYPROV[p]) + "<!--/fcfol-->\n")
json.dump({k["code"]: f"/fractional-cfo/{k['slug']}/" for k in KABS}, open(os.path.join(HERE, "fa_content", "fcfo_lokal_map.json"), "w"))
print("halaman", n, "total URL", len(URLS), "link masuk", nl)
