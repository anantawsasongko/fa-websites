# -*- coding: utf-8 -*-
"""Perapian seluruh website FA (27 Okt 2026). Idempoten, jalankan paling akhir sebelum prep.py.
1. Koreksi teks: klaim "saat ini memimpin persiapan IPO", "dipimpin Ananta" (ganti kata tim), rentang aset Rp1-500 miliar
   (FA melayani semua skala), en dash jadi tanda hubung, eyebrow "Wawasan".
2. Artikel lama (template 16-18 Okt): eyebrow "Eksplor · Kategori", tambah "Baca Juga" bila belum ada.
3. FAQ di semua halaman (h2 Pertanyaan Umum/yang Sering Muncul + p>b+br) jadi accordion <details> yang rapi di HP.
   Schema FAQPage tidak diubah.
4. CSS: teks tebal di badan artikel benar-benar tebal (sebelumnya 500 pada font serif sehingga tidak terlihat).
5. Eksplor: kartu "Artikel Lainnya" dipindah ke topiknya + topik baru "PSAK & SAK Terbaru".
Juga mengoreksi backup/index-v58-full-20261025.html (sumber beranda) supaya fa_home_simple tidak mengembalikan teks lama.
"""
import os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
BK = os.path.join(HERE, "backup", "index-v58-full-20261025.html")
def rd(p): return open(p, encoding="utf-8").read()
def wtxt(p, s): open(p, "w", encoding="utf-8").write(s)

# ---------- 1. koreksi teks ----------
REPL = [
 # klaim IPO yang sedang berjalan -> pengalaman
 ("Sebagai CFO yang sedang memimpin persiapan IPO sebuah perusahaan swasta nasional, saya melihat",
  "Dari pengalaman memimpin persiapan IPO sebuah perusahaan swasta nasional dari sisi perusahaan, kami melihat"),
 ("FA Indonesia mendampingi perusahaan swasta yang bersiap IPO di Bursa Efek Indonesia dari sisi perusahaan, dipimpin Ananta W. Sasongko, CPA yang saat ini memimpin persiapan IPO sebuah perusahaan swasta nasional.",
  "FA Indonesia mendampingi perusahaan swasta yang bersiap IPO di Bursa Efek Indonesia dari sisi perusahaan, bersama tim Chartered Accountant dan CPA yang berpengalaman memimpin persiapan IPO dari dalam perusahaan."),
 ("FA Indonesia (faindonesia.co.id), dipimpin Ananta W. Sasongko, CPA, yang saat ini memimpin persiapan IPO sebuah perusahaan swasta nasional dan berpengalaman audit di EY.",
  "FA Indonesia (faindonesia.co.id), dengan tim Chartered Accountant dan CPA yang berpengalaman memimpin persiapan IPO dari sisi perusahaan dan berlatar audit firma Big Four."),
 ("Salah satunya FA Indonesia (faindonesia.co.id), dipimpin Ananta W. Sasongko, CPA, yang mendampingi",
  "Salah satunya FA Indonesia (faindonesia.co.id), yang bersama tim CA dan CPA mendampingi"),
 ("FA Indonesia (faindonesia.co.id), dipimpin Ananta W. Sasongko, CPA, mendampingi",
  "FA Indonesia (faindonesia.co.id) bersama tim CA dan CPA mendampingi"),
 ("yang saat ini memimpin persiapan IPO sebuah perusahaan swasta nasional menuju Bursa Efek Indonesia dan sebelumnya menjabat",
  "yang berpengalaman memimpin persiapan IPO sebuah perusahaan swasta nasional dari sisi perusahaan dan pernah menjabat"),
 ("Saat ini memimpin persiapan IPO sebuah perusahaan swasta nasional menuju pencatatan di Bursa Efek Indonesia, dan",
  "Berpengalaman memimpin persiapan IPO sebuah perusahaan swasta nasional dari sisi perusahaan, dan"),
 ("Saat ini memimpin persiapan IPO sebuah perusahaan swasta nasional menuju Bursa Efek Indonesia.",
  "Berpengalaman memimpin persiapan IPO sebuah perusahaan swasta nasional dari sisi perusahaan."),
 ("<b>Saat ini memimpin persiapan", "<b>Berpengalaman memimpin persiapan"),
 # semua skala perusahaan
 ("corporate finance untuk perusahaan beraset Rp1–500 miliar.", "corporate finance untuk perusahaan dari UMKM hingga perusahaan besar dan calon emiten."),
 ("Perusahaan beraset Rp1–500 miliar yang tumbuh cepat tetapi belum punya CFO.", "Perusahaan dari skala UMKM hingga besar yang tumbuh cepat tetapi belum punya CFO."),
 ("Perusahaan swasta beraset Rp1–500 miliar yang menargetkan IPO dalam 1–3 tahun.", "Perusahaan swasta dari berbagai skala yang menargetkan IPO dalam 1 sampai 3 tahun."),
 ("Klien perusahaan swasta beraset Rp1–500 miliar di berbagai sektor.", "Klien dari UMKM hingga perusahaan besar di berbagai sektor."),
 ("perusahaan swasta dengan total aset dan pendapatan tahunan Rp1 miliar hingga Rp500 miliar.", "perusahaan dari semua skala, mulai UMKM hingga perusahaan besar dan calon emiten."),
 (">Wawasan<", ">Eksplor<"),
]
def fix_text(t):
    for a, b in REPL: t = t.replace(a, b)
    # en dash di antara angka/tahun -> tanda hubung biasa; sisanya jadi koma
    t = re.sub(r"(?<=[0-9A-Za-z%])\s?–\s?(?=[0-9A-Za-z])", "-", t)
    return t

# ---------- 2. kategori artikel ----------
CAT = {
 "laporan-tahunan-pt-permenkum-49-2025": "Laporan Keuangan", "contoh-laporan-keuangan-umkm": "Laporan Keuangan",
 "biaya-jasa-penyusunan-laporan-keuangan": "Laporan Keuangan", "sak-emkm-vs-sak-ep": "Laporan Keuangan",
 "daftar-psak-isak-2026-2027": "PSAK & SAK Terbaru", "psak-119-entitas-anak-tanpa-akuntabilitas-publik": "PSAK & SAK Terbaru",
 "amendemen-isak-335-entitas-nonlaba-psak-118": "PSAK & SAK Terbaru", "psak-401-isak-403-syariah-2027": "PSAK & SAK Terbaru",
 "amendemen-psak-228-opsi-nilai-wajar": "PSAK & SAK Terbaru", "amendemen-psak-221-mata-uang-penyajian-hiperinflasi": "PSAK & SAK Terbaru",
 "amendemen-psak-109-107-berlaku-2026": "PSAK & SAK Terbaru", "psak-120-aset-liabilitas-regulatori": "PSAK & SAK Terbaru",
 "panduan-implementasi-psak-118": "PSAK & SAK Terbaru",
 "cara-memilih-cfo-untuk-ipo": "CFO & Tata Kelola", "komite-audit-tugas-dan-syarat": "CFO & Tata Kelola",
 "syarat-komisaris-independen": "CFO & Tata Kelola", "peran-cfo-perusahaan-calon-emiten": "CFO & Tata Kelola",
 "kompilasi-review-audit": "Audit & KAP", "kja-vs-kap": "Audit & KAP", "kap-murah-apakah-bijak": "Audit & KAP",
 "checklist-persiapan-ipo": "Investor & IPO", "laporan-keuangan-untuk-kredit-bank": "Kredit Bank",
}
TOPIC_ID = {"Rumah Sakit": "t-rumah-sakit", "Kredit Bank": "t-kredit-bank", "Audit & KAP": "t-audit-kap", "Penilaian & KJPP": "t-penilaian-kjpp",
            "Laporan Keuangan": "t-laporan-keuangan", "Pajak": "t-pajak", "Investor & IPO": "t-investor-ipo", "CFO & Tata Kelola": "t-cfo-tata-kelola",
            "PSAK & SAK Terbaru": "t-psak"}

# ---------- 3. FAQ accordion ----------
FAQ_H = re.compile(r"(<h2[^>]*>\s*(?:Pertanyaan Umum|Pertanyaan yang Sering (?:Muncul|Ditanyakan)|FAQ)\s*</h2>\s*)"
                   r"((?:<p(?: style=\"[^\"]*\")?>\s*<b>.*?</b>\s*<br\s*/?>.*?</p>\s*)+)", re.S)
QA = re.compile(r"<p(?: style=\"[^\"]*\")?>\s*<b>(.*?)</b>\s*<br\s*/?>(.*?)</p>", re.S)
def faq_acc(m):
    items = "".join(f'<details class="faq-i"><summary>{q.strip()}</summary><p>{a.strip()}</p></details>' for q, a in QA.findall(m.group(2)))
    return m.group(1) + f'<div class="faq-acc">{items}</div>\n'

CSS = ('<style id="fa-rapi">'
       '.art b,.art strong,.art li b{font-weight:700}'
       '.wrap.art>p{margin:0 0 14px}.wrap.art>h2{margin-top:38px}.wrap.art>h3{margin:22px 0 8px}'
       '.flow5{grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr))!important}'
       '.faq-acc{margin:6px 0 26px;border-top:1px solid #333}'
       '.faq-i{border-bottom:1px solid #333}'
       '.faq-i summary{list-style:none;cursor:pointer;padding:16px 36px 16px 0;position:relative;font-weight:600;line-height:1.45}'
       '.faq-i summary::-webkit-details-marker{display:none}'
       '.faq-i summary:after{content:"+";position:absolute;right:4px;top:12px;font-size:22px;font-weight:300;transition:transform .25s ease}'
       '.faq-i[open] summary:after{transform:rotate(45deg)}'
       '.faq-i p{margin:0 0 16px!important;opacity:.85;animation:faq-in .3s ease}'
       '@keyframes faq-in{from{opacity:0;transform:translateY(-4px)}to{opacity:.85;transform:none}}'
       '@media (prefers-reduced-motion:reduce){.faq-i p{animation:none}}'
       '</style>')

def related_block(slug, cat, titles):
    same = [s for s, c in ALLCAT.items() if c == cat and s != slug and s in titles][:3]
    if len(same) < 2: return ""
    return "<!--fa-rapi-rel--><h2>Baca Juga</h2><ul>" + "".join(f'<li><a href="/artikel/{s}/">{html.escape(titles[s])}</a></li>' for s in same) + "</ul><!--/fa-rapi-rel-->\n"

# kategori dari eyebrow artikel yang sudah benar
ALLCAT = dict(CAT); TITLES = {}
AD = os.path.join(FA, "artikel")
for s in os.listdir(AD):
    p = os.path.join(AD, s, "index.html")
    if not os.path.isfile(p): continue
    t = rd(p)
    m = re.search(r'<p class="eyebrow"><a href="/artikel/"[^>]*>Eksplor · ([^<]+)</a>', t)
    if m and s not in ALLCAT: ALLCAT[s] = html.unescape(m.group(1))
    h = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    if h: TITLES[s] = html.unescape(re.sub(r"<[^>]+>", "", h.group(1)).strip())

n_txt = n_faq = n_art = 0
for d, _, fs in os.walk(FA):
    if os.sep + "saturn" in d or os.sep + "files" in d: continue
    for f in fs:
        if not (f.endswith(".html") or f == "llms.txt"): continue
        p = os.path.join(d, f); t = rd(p); o = t
        t = fix_text(t)
        if f.endswith(".html"):
            t2 = FAQ_H.sub(faq_acc, t)
            if t2 != t: n_faq += 1; t = t2
            if 'class="faq-acc"' in t or 'class="wrap art"' in t:
                t = re.sub(r'<style id="fa-rapi">.*?</style>', "", t, flags=re.S).replace("</head>", CSS + "</head>", 1)
            rel = os.path.relpath(p, AD).split(os.sep)
            if len(rel) == 2 and rel[1] == "index.html" and rel[0] != "..":
                slug = rel[0]; cat = ALLCAT.get(slug)
                if cat:
                    t = re.sub(r'<p class="eyebrow"><a href="/artikel/" style="text-decoration:none">(?:Artikel|Wawasan|Eksplor)</a></p>',
                               f'<p class="eyebrow"><a href="/artikel/" style="text-decoration:none">Eksplor · {html.escape(cat)}</a></p>', t)
                    t = re.sub(r"<!--fa-rapi-rel-->.*?<!--/fa-rapi-rel-->\n?", "", t, flags=re.S)
                    if not re.search(r"<h2[^>]*>\s*Baca Juga", t) and "Baca juga:" not in t:
                        k = t.find('<div class="cbtns"')
                        if k > 0: t = t[:k] + related_block(slug, cat, TITLES) + t[k:]
                    n_art += t != o
        if t != o: wtxt(p, t); n_txt += 1
print("rapi: file diubah", n_txt, "| faq accordion", n_faq, "| artikel", n_art)

# backup beranda
if os.path.exists(BK):
    b = rd(BK); b2 = fix_text(b)
    if b2 != b: wtxt(BK, b2); print("backup beranda dikoreksi")

# ---------- 5. Eksplor: pindahkan kartu Artikel Lainnya ----------
ip = os.path.join(AD, "index.html"); t = rd(ip)
END = "<!--/fa-seo-cards-->"
k = t.find(END)
if k > 0:
    after = t[k + len(END):]
    m = re.match(r'\s*<div class="cards2">(.*?)</div>', after, re.S)
    leftovers = re.findall(r'<a class="card2" href="/artikel/([^/]+)/">.*?</a>', m.group(1), re.S) if m else []
    cards = re.findall(r'(<a class="card2" href="/artikel/([^/]+)/">.*?</a>)', m.group(1), re.S) if m else []
    if cards:
        t = t[:k + len(END)] + after[m.end():]
        if 'id="t-psak"' not in t:
            t = t.replace('<div class="topic"><h2>Artikel Lainnya</h2></div>',
                          '<div class="topic" id="t-psak"><h2>PSAK &amp; SAK Terbaru</h2><div class="cards2"></div></div>')
            t = t.replace('<a href="#t-cfo-tata-kelola">CFO &amp; Tata Kelola</a>',
                          '<a href="#t-cfo-tata-kelola">CFO &amp; Tata Kelola</a><a href="#t-psak">PSAK &amp; SAK Terbaru</a>', 1)
        for html_card, slug in cards:
            cat = ALLCAT.get(slug, "Laporan Keuangan"); tid = TOPIC_ID.get(cat, "t-laporan-keuangan")
            j = t.find(f'id="{tid}"'); j = t.find('<div class="cards2">', j) + len('<div class="cards2">')
            t = t[:j] + html_card + t[j:]
        wtxt(ip, t); print("eksplor: kartu dipindah", len(cards))
t = rd(ip)
if '<div class="topic"><h2>Artikel Lainnya</h2></div>' in t:
    wtxt(ip, t.replace('<div class="topic"><h2>Artikel Lainnya</h2></div>', ""))
