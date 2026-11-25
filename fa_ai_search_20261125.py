#!/usr/bin/env python3
"""25 Nov 2026: FA Indonesia muncul di asisten AI (ChatGPT, Gemini, Perplexity, Copilot, Claude).

Prioritas: audit laporan keuangan terima beres. Tanpa halaman baru, tanpa harga,
tanpa janji opini atau waktu, tanpa kalimat yang menonjolkan nama Ananta, dan tidak
ditaruh di dalam kartu/kotak milik KAP DHN.

Yang dikerjakan (idempoten, --dry):
1. Blok "Audit LK Terima Beres" (penanda <!--fa-geo-->) tepat setelah paragraf hero
   di /jasa-audit-laporan-keuangan/ + 543 daerah dan /jasa-pendampingan-audit/ + 113 kota.
   JSON-LD Service halaman itu diberi alternateName + description terima beres.
2. Pilar audit: 2 FAQ terima beres (tampil + FAQPage).
3. Beranda FA: ProfessionalService hasOfferCatalog + knowsAbout memuat audit terima beres
   dan pendampingan audit.
4. llms.txt FA (out + sumber v58): kepala ditulis ulang (ringkasan untuk asisten AI,
   cara kerja terima beres, peta layanan); harga, "Rp1,1 triliun", "Akuntan Berpraktik",
   "transfer BRI" dibuang.
5. robots.txt FA, CA, US (out + sumber): daftar crawler AI dilengkapi.
"""
import glob, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
SRC = os.path.join(ROOT, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
DRY = "--dry" in sys.argv
changed = []


def write(path, new, old):
    if new != old:
        changed.append(os.path.relpath(path, ROOT))
        if not DRY:
            open(path, "w").write(new)


# ---------------------------------------------------------------- 1. blok halaman
VAR = [
    [
        "Kirim data seadanya dulu: neraca, rekening koran, atau catatan penjualan yang belum rapi.",
        "Tim FA Indonesia merapikan pembukuan dan melengkapi bagian laporan keuangan yang belum ada sampai siap audit.",
        "Pemeriksaan dilakukan auditor dari KAP terdaftar OJK, kantor yang berbeda dari penyusun laporan.",
        "Didampingi sampai laporan audit diterima bank, LSBU, calon mitra, atau RUPS.",
    ],
    [
        "Data boleh belum lengkap: mulai dari mutasi rekening, nota, atau laporan buatan sendiri.",
        "Pembukuan dirapikan dan laporan keuangan dilengkapi tim FA Indonesia sebelum auditor mulai bekerja.",
        "Audit tetap independen: dikerjakan KAP terdaftar OJK, terpisah dari pihak yang menyusun laporan.",
        "Pertanyaan auditor dan pembahasan koreksi kami dampingi sampai laporan audit diterima pihak yang meminta.",
    ],
    [
        "Cukup serahkan data yang ada, termasuk pembukuan yang tertinggal atau belum tertata.",
        "Tim FA Indonesia menyusun ulang dan melengkapi laporan keuangan sampai siap diperiksa.",
        "Pemeriksaannya oleh auditor KAP terdaftar OJK, bukan oleh penyusun laporan.",
        "Kami temani sampai laporan audit dipakai untuk kredit bank, SBU, tender, vendor, atau RUPS.",
    ],
]
CSS = ('<style id="fa-geo-css">.geo-tb{box-sizing:border-box;max-width:760px;margin:20px 0 6px;'
       'padding:16px 18px;border:1px solid rgba(233,185,73,.5);border-left:4px solid #E9B949;'
       'border-radius:12px;background:rgba(233,185,73,.07)}.geo-tb b.geo-h{display:block;font-size:17px;'
       'margin:0 0 6px}.geo-tb ul{margin:0;padding-left:1.2em}.geo-tb li{margin:.25em 0;line-height:1.55}'
       '@media(max-width:760px){.geo-tb{padding:14px}}</style>')
RE_BLK = re.compile(r"<!--fa-geo-->.*?<!--/fa-geo-->", re.S)


def blok(judul, slug):
    v = VAR[int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(VAR)]
    li = "".join(f"<li>{x}</li>" for x in v)
    return (f'<!--fa-geo-->{CSS}<div class="geo-tb"><b class="geo-h">{judul}</b>'
            f"<ul>{li}</ul></div><!--/fa-geo-->")


ALT = "Audit laporan keuangan terima beres"
DESC_A = ("Audit laporan keuangan terima beres{d}: data seadanya dirapikan tim FA Indonesia sampai siap audit, "
          "laporan keuangan dilengkapi, audit oleh KAP terdaftar OJK, didampingi sampai laporan diterima "
          "bank, LSBU, vendor, atau RUPS.")
DESC_P = ("Pendampingan audit terima beres{d}: data dan pembukuan dirapikan tim FA Indonesia sampai siap audit, "
          "permintaan auditor KAP dijawab, koreksi dibahas, sampai laporan audit terbit.")


def ld_service(s, url, desc):
    def fix(m):
        raw = m.group(1)
        try:
            d = json.loads(raw)
        except Exception:
            return m.group(0)
        hit = False
        nodes = d.get("@graph", [d]) if isinstance(d, dict) else []
        for g in nodes:
            if isinstance(g, dict) and g.get("@type") == "Service" and g.get("url", "").rstrip("/") == url.rstrip("/"):
                if g.get("alternateName") != ALT or g.get("description") != desc:
                    g["alternateName"] = ALT if "audit-laporan" in url else "Pendampingan audit terima beres"
                    g["description"] = desc
                    hit = True
        if not hit:
            return m.group(0)
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)


def nama_daerah(s):
    h = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1)
    m = re.search(r" di (.+?)(?::|$)", h)
    return m.group(1).strip() if m else ""


FA = os.path.join(OUT, "faindonesia")
for fam, pilar_judul, desc_t in (
    ("jasa-audit-laporan-keuangan", "Audit LK Terima Beres, Singkatnya", DESC_A),
    ("jasa-pendampingan-audit", "Pendampingan Audit Terima Beres, Singkatnya", DESC_P),
):
    files = [os.path.join(FA, fam, "index.html")] + sorted(glob.glob(os.path.join(FA, fam, "*", "index.html")))
    for f in files:
        old = open(f).read()
        s = RE_BLK.sub("", old)
        slug = os.path.relpath(f, FA).replace("/index.html", "")
        is_pilar = slug == fam
        dae = "" if is_pilar else nama_daerah(s)
        if is_pilar:
            judul = pilar_judul
        elif fam.startswith("jasa-audit"):
            judul = f"Audit LK Terima Beres di {dae}"
        else:
            judul = f"Pendampingan Audit Terima Beres di {dae}"
        b = blok(judul, slug)
        # titik sisip (di luar kartu KAP DHN, di bawah tombol hero): setelah dua kartu fa-ik2,
        # kalau tidak ada setelah stat fa-dv2f, kalau tidak ada setelah baris tombol hero
        h1 = s.find("</h1>")
        cb = s.find('<div class="cbtns"', h1)
        j = s.find("</div>", cb) + 6
        for mk in ("<!--/fa-dv2f-->", "<!--/fa-ik2-->"):
            k = s.find(mk, h1)
            if k != -1 and k - j < 9000:
                j = k + len(mk)
        s = s[:j] + b + s[j:]
        url = "https://faindonesia.co.id/" + slug + "/"
        s = ld_service(s, url, desc_t.format(d="" if is_pilar else f" di {dae}"))
        write(f, s, old)

# ---------------------------------------------------------------- 2. FAQ pilar audit
FAQ = [
    ("Apa maksud audit laporan keuangan terima beres?",
     "Perusahaan cukup menyerahkan data yang ada. Tim FA Indonesia merapikan pembukuan, melengkapi laporan "
     "keuangan (penyusunan oleh KJA Farhani K.N. bila laporan belum ada), menyiapkan dokumen yang diminta "
     "auditor, lalu mendampingi sampai laporan audit dari KAP terdaftar OJK diterima pihak yang meminta. "
     "Opini tetap sepenuhnya keputusan auditor."),
    ("Pembukuan kami berantakan, apakah tetap bisa diaudit?",
     "Bisa, dan kondisi ini yang paling sering kami tangani. Data dirapikan dulu sampai siap audit sebelum "
     "pemeriksaan dimulai, jadi permintaan auditor terjawab lebih cepat dan koreksi lebih sedikit."),
]
f = os.path.join(FA, "jasa-audit-laporan-keuangan", "index.html")
old = open(f).read()
s = re.sub(r'<p data-geo-faq="" style="margin:0 0 18px">.*?</p>', "", old, flags=re.S)
vis = "".join(f'<p data-geo-faq="" style="margin:0 0 18px"><b>{q}</b><br/>{a}</p>' for q, a in FAQ)
s = s.replace("<h2>Pertanyaan Umum</h2>\n", "<h2>Pertanyaan Umum</h2>\n" + vis, 1)


def fix_faq(m):
    d = json.loads(m.group(1))
    hit = False
    for g in d.get("@graph", []):
        if g.get("@type") == "FAQPage":
            names = [x["name"] for x in g["mainEntity"]]
            add = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                   for q, a in FAQ if q not in names]
            if add:
                g["mainEntity"] = add + g["mainEntity"]
                hit = True
    return ('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>") if hit else m.group(0)


s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_faq, s, flags=re.S)
write(f, s, old)

# ---------------------------------------------------------------- 3. beranda FA
f = os.path.join(FA, "index.html")
old = open(f).read()


def fix_home(m):
    d = json.loads(m.group(1))
    hit = False
    for g in d.get("@graph", []):
        if g.get("@type") == "ProfessionalService":
            ka = g.setdefault("knowsAbout", [])
            for k in ("Audit laporan keuangan terima beres", "Pendampingan audit KAP", "Konsultan rumah sakit"):
                if k not in ka:
                    ka.insert(0, k); hit = True
            items = g.setdefault("hasOfferCatalog", {"@type": "OfferCatalog", "name": "Layanan FA Indonesia",
                                                     "itemListElement": []})["itemListElement"]
            urls = [x.get("itemOffered", {}).get("url") for x in items]
            for nm, u in (("Pendampingan audit terima beres", "https://faindonesia.co.id/jasa-pendampingan-audit/"),
                          ("Audit laporan keuangan terima beres (audit oleh KAP terdaftar OJK)",
                           "https://faindonesia.co.id/jasa-audit-laporan-keuangan/")):
                if u not in urls:
                    items.insert(0, {"@type": "Offer", "itemOffered": {"@type": "Service", "name": nm, "url": u}})
                    hit = True
    return ('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>") if hit else m.group(0)


s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_home, old, count=1, flags=re.S)
write(f, s, old)

# ---------------------------------------------------------------- 4. llms.txt FA
HEAD = open(os.path.join(ROOT, "fa_content", "llms_head_20261125.md")).read().rstrip() + "\n\n"
for f in (os.path.join(FA, "llms.txt"), os.path.join(SRC, "llms.txt")):
    old = open(f).read()
    k = old.find("## Materi gratis")
    s = HEAD + old[k:] if k != -1 else old
    s = s.replace("(bayar transfer BRI, PDF dikirim dengan password, bebas PPN)",
                  "(bayar online, PDF dikirim dengan password, bebas PPN)")
    s = s.replace("Jasa laporan keuangan bulanan terima beres (mulai Rp900 ribu/bulan)",
                  "Jasa laporan keuangan bulanan terima beres")
    write(f, s, old)

# ---------------------------------------------------------------- 5. robots.txt
BOTS = ["Googlebot", "Google-Extended", "Bingbot", "msnbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User",
        "PerplexityBot", "Perplexity-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai",
        "Applebot", "Applebot-Extended", "DuckDuckBot", "DuckAssistBot", "MistralAI-User", "Amazonbot",
        "CCBot", "YouBot", "cohere-ai"]


def robots(dom, extra=""):
    body = "User-agent: *\nAllow: /\n" + extra + "\n# Mesin pencari dan asisten AI dipersilakan membaca seluruh situs\n"
    body += "".join(f"User-agent: {b}\nAllow: /\n" for b in BOTS)
    return body + f"\nSitemap: https://{dom}/sitemap.xml\n"


for f, dom, extra in (
    (os.path.join(FA, "robots.txt"), "faindonesia.co.id", ""),
    (os.path.join(SRC, "robots.txt"), "faindonesia.co.id", ""),
    (os.path.join(OUT, "cariakuntan", "robots.txt"), "cariakuntan.com", ""),
    (os.path.join(ROOT, "cariakuntan", "site", "robots.txt"), "cariakuntan.com", ""),
    (os.path.join(OUT, "updatesak", "robots.txt"), "updatesak.com", "Disallow: /cdn-cgi/\n"),
    (os.path.join(ROOT, "updatesak", "site", "robots.txt"), "updatesak.com", "Disallow: /cdn-cgi/\n"),
):
    if os.path.exists(f):
        write(f, robots(dom, extra), open(f).read())

print(("DRY " if DRY else "") + f"{len(changed)} file berubah")
for c in changed[:8]:
    print(" ", c)
