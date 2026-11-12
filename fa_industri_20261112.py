# -*- coding: utf-8 -*-
"""12 Nov 2026. Bos: keyword "Audit LK Rumah Sakit" belum nyantol ke FA; harus ada sampai restoran, cafe, manufaktur,
data center. Halaman daerah jangan dikurangi, justru ditambah.

BEKERJA LANGSUNG DI out/faindonesia (lihat PERINGATAN BUILD di README-DEPLOY). Idempoten.
Template: halaman live /laporan-keuangan-cafe-restoran/provinsi-bali/ (head, header, footer) dan blok tim live.

Yang dibuat:
1. /audit-laporan-keuangan-<industri>/ (pilar) + /provinsi-<prov>/ untuk tiap industri di fa_content/industri20261112.py.
2. /laporan-keuangan-<industri>/ (pilar) + /provinsi-<prov>/ untuk industri yang belum punya pilar LK.
3. Hub /audit-laporan-keuangan-per-industri/.
4. Sisipan berpenanda <!--fa-ind12--> (daftar industri) di pilar audit, pilar penyusunan LK, pilar LK jenis usaha lama,
   pilar RS; baris <!--fa-ind12x--> di halaman audit dan penyusunan LK per kota/kabupaten/provinsi; sitemap <!--ind12-->; llms.
Urutan: jalankan sebelum fa_seo_rapi_20261108.py dan uniq_lokal_20261109.py (keluarga baru sudah didaftarkan di uniq_lokal).
Aturan isi: audit oleh KAP DHN & Rekan, penyusunan oleh KJA Farhani K.N., FA Indonesia pintu kontak, WA dijawab Ananta.
Tanpa janji harga atau hasil, tanpa klaim terbaik, tanpa em dash."""
import os, re, sys, json, html, glob, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faindonesia")
sys.path.insert(0, os.path.join(HERE, "fa_content")); sys.path.insert(0, os.path.join(HERE, "shared"))
from industri20261112 import IND, UMUM_WAJIB

E = html.escape
D = "https://faindonesia.co.id"
TODAY = "2026-11-12"
DRY = "--dry" in sys.argv
CHANGED = []


def sl(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def rd(p): return open(p, encoding="utf-8").read()
def P(path): return os.path.join(OUT, *[x for x in path.strip("/").split("/") if x], "index.html")
def wt(p, t):
    if os.path.exists(p) and rd(p) == t: return 0
    CHANGED.append(p)
    if DRY: return 1
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(t); return 1
def wa(txt): return "https://wa.me/6282245260121?text=" + urllib.parse.quote(txt, safe="")
def hid(s): return sl(html.unescape(re.sub(r"<[^>]+>", "", s)))[:60].rstrip("-")
KEEP = {"PT", "PMA", "PBF", "BBM", "LPG", "SPBU", "BUMD", "BUMDes", "Perumda"}
def lw(s): return " ".join(w if w.strip(",") in KEEP else w.lower() for w in s.split(" "))
def cut(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    while len(E(s)) > n and ". " in s: s = s.rsplit(". ", 1)[0] + "."
    assert len(E(s)) <= n, (len(s), s)
    return s
def between(t, a, b):
    i = t.index(a); j = t.index(b, i) + len(b); return t[i:j]


# ---------------- template live ----------------
TPL = rd(P("/laporan-keuangan-cafe-restoran/provinsi-bali/"))
HEAD = TPL[:TPL.index("<main")]
HEAD = re.sub(r'<style id="uq-[^"]*">.*?</style>', "", HEAD, flags=re.S)
TAIL = TPL[TPL.index("</main>"):]
LK2 = between(TPL, "<!--fa-lk2-->", "<!--/fa-lk2-->")
TIM_LK = between(TPL, "<!--fa-tim-atas-->", "<!--/fa-tim-atas-->")
TIM_AUDIT = between(rd(P("/jasa-audit-laporan-keuangan-bpr/")), "<!--fa-tim-atas-->", "<!--/fa-tim-atas-->")
assert "Bali" in LK2 and "Bali" not in TIM_LK and "BPR" not in TIM_AUDIT.replace("laporan keuangan BPR", "")


def lk2(what, loc):
    """Kotak kontak KJA Farhani + KAP DHN. what: 'rumah sakit'; loc: '' atau 'Bali'."""
    b = LK2.replace("Kontak KJA Farhani dan KAP DHN &amp; Rekan di Bali", "Kontak KJA Farhani dan KAP DHN &amp; Rekan" + (f" di {E(loc)}" if loc else ""))
    di = f" di {loc}" if loc else ""
    msgs = [f"Halo Pak Ananta, saya ingin tanya penyusunan laporan keuangan {what}{di} oleh KJA Farhani.",
            f"Halo Pak Ananta, saya ingin tanya audit laporan keuangan {what}{di} oleh KAP DHN & Rekan."]
    it = iter(msgs)
    b = re.sub(r'href="https://wa\.me/6282245260121\?text=[^"]*"', lambda m: f'href="{wa(next(it))}"', b)
    assert "Bali" not in b or loc == "Bali"
    return b


# ---------------- provinsi dan kab/kota (dibaca dari halaman live) ----------------
PROV = []   # (pslug, nama, [(slug, nama kab/kota)])
for d in sorted(glob.glob(os.path.join(OUT, "laporan-keuangan-cafe-restoran", "provinsi-*"))):
    t = rd(os.path.join(d, "index.html"))
    nm = html.unescape(re.search(r'<p class="eyebrow">[^<]*· ([^<]+)</p>', t).group(1)).strip()
    seg = t[t.index('<h2 id="kabupaten-dan-kota-di-'):]
    seg = seg[:seg.index("</p>")]
    kab = [(a, html.unescape(b)) for a, b in re.findall(r'href="/jasa-penyusunan-laporan-keuangan/([^/"]+)/">([^<]+)</a>', seg)]
    PROV.append((os.path.basename(d), nm, kab))
# 4 provinsi baru Papua: keanggotaan kabupaten mengikuti shared/lokal.py (data wilayah lama masih memakai provinsi induk)
import lokal as _L
_AL = {"mimika": "timika"}
def _kslug(n):
    return [c for c in (sl(n), _AL.get(sl(n), ""), "kabupaten-" + sl(n), "kota-" + sl(n)) if c and os.path.exists(P(f"/jasa-penyusunan-laporan-keuangan/{c}/"))]
_PB = {}
for _pn, _lst in _L.PAPUA_BARU.items():
    _PB[_pn] = [(s, ("Timika" if s == "timika" else n if s == sl(n) else ("Kota " if s.startswith("kota-") else "Kabupaten ") + n)) for n in _lst for s in _kslug(n)]
_moved = {s for v in _PB.values() for s, _ in v}
PROV = [(ps, pn, [k for k in kab if k[0] not in _moved]) for ps, pn, kab in PROV if pn not in _PB]
PROV += [("provinsi-" + sl(pn), pn, sorted(v, key=lambda x: x[1])) for pn, v in _PB.items() if v]
PROV.sort(key=lambda x: x[1])
assert len(PROV) == 38 and all(k for _, _, k in PROV), (len(PROV), [p for p, _, k in PROV if not k])
LAMA = [("laporan-keuangan-cafe-restoran", "Cafe dan Restoran"), ("laporan-keuangan-klinik", "Klinik dan Apotek"),
        ("laporan-keuangan-perusahaan", "Perusahaan PT dan CV"), ("laporan-keuangan-kontraktor", "Kontraktor"),
        ("laporan-keuangan-koperasi", "Koperasi dan BUMDes"), ("laporan-keuangan-yayasan-sekolah", "Yayasan dan Sekolah"),
        ("laporan-keuangan-toko-distributor", "Toko dan Distributor"), ("laporan-keuangan-umkm", "UMKM")]
A = lambda i: "audit-laporan-keuangan-" + i["slug"]
K = lambda i: ("laporan-keuangan-" + i["slug"]) if i["lk"] else i["lk_lama"]
HUB = "/audit-laporan-keuangan-per-industri/"


def og_img(key, kicker, title):
    p = f"/img/og-page/{key}.jpg"
    if os.path.exists(os.path.join(OUT, p.strip("/"))): return p
    if DRY: return "/img/og-page/aplikasi-audit-kap.jpg"
    try:
        import share_all
        return share_all._poster("fa", kicker, title, key, OUT)
    except Exception as e:
        print("og fallback", key, repr(e)[:120]); return "/img/og-page/aplikasi-audit-kap.jpg"


def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
def links(items, sep=" · "): return '<p class="t">' + sep.join(f'<a href="{u}">{E(n)}</a>' for u, n in items) + "</p>"
def ul(items): return "<ul>" + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"


def page(path, eyebrow, h1, lead, watxt, back, top, intro, secs, faq, title, desc, svc, stype, crumb, og, mark):
    url = D + path
    assert len(title) <= 65, (len(title), title)
    nav, body = [], []
    for h, hh in secs:
        i = hid(h); nav.append(f'<li><a href="#{i}">{E(h)}</a></li>'); body.append(f'<h2 id="{i}">{E(h)}</h2>{hh}')
    pmap = f'<nav aria-label="Peta Isi" class="pf-map" id="pfmap"><b>Peta Isi</b><ol>{"".join(nav)}</ol></nav>'
    btn = f'<a class="btn solid" href="{wa(watxt)}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
    fq = ('<h2>Pertanyaan Umum</h2><div class="faq-acc">' + "".join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq) + "</div>")
    main = (f'<main id="top">{mark}\n<section class="block">\n<div class="wrap art">\n'
            f'<p class="eyebrow">{E(eyebrow)}</p>\n'
            f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{E(h1)}</h1><div class="tshare-top"><div class="share" data-lab="Bagikan" data-tool="{E(h1)}"></div></div>\n'
            f'<p class="t" style="max-width:62em">{E(lead)}</p>\n'
            f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px">{btn}<a class="btn line" href="{back[0]}">{E(back[1])}</a></div>'
            f'{top}\n<p>{E(intro)}</p>{pmap}' + "".join(body) + "\n" + fq
            + f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px">{btn}</div>\n</div>\n</section>\n')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": svc, "serviceType": stype,
         "provider": {"@type": "ProfessionalService", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"},
         "areaServed": {"@type": "Country", "name": "Indonesia"}, "url": url},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": D + u} for i, (n, u) in enumerate(crumb)]}]}
    head = HEAD
    title_, desc_ = E(title), E(cut(desc))
    n = [0]
    def sub(pat, rep, flags=0, count=0):
        nonlocal head
        head, k = re.subn(pat, rep, head, count=count, flags=flags); n[0] += 1
        assert k >= 1, pat
    sub(r"<title>.*?</title>", lambda m: f"<title>{title_}</title>", re.S, 1)
    sub(r'<meta content="[^"]*" (name="description"|property="og:description")/>', lambda m: f'<meta content="{desc_}" {m.group(1)}/>')
    sub(r'<meta content="[^"]*" property="og:title"/>', lambda m: f'<meta content="{title_}" property="og:title"/>')
    sub(r'<link href="[^"]*" rel="canonical"/>', lambda m: f'<link href="{url}" rel="canonical"/>')
    sub(r'<meta content="[^"]*" property="og:url"/>', lambda m: f'<meta content="{url}" property="og:url"/>')
    sub(r'(<meta content=")[^"]*(" (?:property="og:image"|name="twitter:image")/>)', lambda m: m.group(1) + D + og + m.group(2))
    sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", re.S, 1)
    head = re.sub(r'<meta content="[^"]*" name="twitter:(title|description)"/>', lambda m: f'<meta content="{title_ if m.group(1) == "title" else desc_}" name="twitter:{m.group(1)}"/>', head)
    old = rd(P(path)) if os.path.exists(P(path)) else ""
    uq = re.search(r"<!--uq-lokal-->.*?<!--/uq-lokal-->", old, re.S)   # blok uniq_lokal dipertahankan agar idempoten
    lkb = re.search(r"<!--fa-lk2-->.*?<!--/fa-lk2-->", old, re.S)       # kotak kontak yang sudah distandarkan fa_lead_lkaudit dipertahankan
    if lkb and "<!--fa-lk2-->" in main: main = re.sub(r"<!--fa-lk2-->.*?<!--/fa-lk2-->", lambda m: lkb.group(0), main, count=1, flags=re.S)
    if uq: main = main.replace("\n<h2>Pertanyaan Umum</h2>", "\n" + uq.group(0) + "<h2>Pertanyaan Umum</h2>", 1)
    t = head + main + TAIL
    assert "—" not in main
    wt(P(path), t)
    return path


URLS = []
MARK = "<!--fa-ind12-page-->"
OGA = og_img("audit-laporan-keuangan-per-industri", "Audit Laporan Keuangan", "Audit Laporan Keuangan per Industri oleh KAP Terdaftar OJK")
OGK = og_img("laporan-keuangan-per-industri", "Laporan Keuangan", "Jasa Laporan Keuangan per Industri")

FAQ_AUDIT = lambda i, di: [
    (f"Siapa yang mengaudit laporan keuangan {lw(i['nama'])}{di}?", "Audit dan opini dikerjakan KAP DHN & Rekan, Kantor Akuntan Publik berizin Menteri Keuangan dan terdaftar di OJK. FA Indonesia adalah pintu kontaknya: chat WhatsApp Anda dijawab Ananta W. Sasongko, CPA."),
    ("Berapa lama prosesnya?", "Tergantung kesiapan laporan keuangan dan dokumen pendukung. Jadwal disepakati setelah auditor melihat data awal. Kami tidak menjanjikan tanggal atau opini tertentu sebelum itu."),
    ("Laporan keuangan kami belum rapi, bagaimana?", "Laporan keuangan disusun lebih dulu oleh KJA Farhani K.N., lalu diaudit KAP DHN & Rekan. Untuk satu perusahaan, penyusun dan auditornya selalu kantor yang berbeda agar independensi terjaga.")]
FAQ_LK = lambda i, di: [
    (f"Siapa yang menyusun laporan keuangan {lw(i['nama'])}{di}?", "Penyusunan dikerjakan KJA Farhani K.N., Kantor Jasa Akuntansi berizin. FA Indonesia adalah pintu kontaknya: chat WhatsApp Anda dijawab Ananta W. Sasongko, CPA."),
    ("Standar apa yang dipakai?", "SAK EMKM, SAK EP, atau SAK Indonesia sesuai ukuran dan kebutuhan pemakai laporan. Pilihannya dibahas di awal karena menentukan isi laporan dan catatannya."),
    ("Bisakah sekaligus diaudit?", "Bisa, oleh kantor yang berbeda. Audit dikerjakan KAP DHN & Rekan yang terdaftar di OJK, setelah laporan keuangannya selesai disusun.")]


def other_ind(cur, fam, pslug=""):
    suf = f"{pslug}/" if pslug else ""
    its = []
    for j in IND:
        if j["slug"] == cur["slug"]: continue
        base = A(j) if fam == "audit" else K(j)
        its.append((f"/{base}/{suf}", j["pendek"]))
    return links(its)


for i in IND:
    nm, low = i["nama"], lw(i["nama"])
    # ---------- pilar audit ----------
    a = A(i)
    title = f"Audit Laporan Keuangan {i['pendek']} oleh KAP Terdaftar OJK"
    if len(title) > 60: title = f"Audit Laporan Keuangan {i['pendek']} oleh KAP"
    if len(title) > 60: title = f"Audit LK {i['pendek']} oleh KAP Terdaftar OJK"
    h1 = f"Audit Laporan Keuangan {nm} oleh KAP Terdaftar OJK"
    lead = f"Audit laporan keuangan (audit LK) untuk {i['who']}. Audit dan opini oleh KAP DHN & Rekan yang terdaftar di OJK. Satu chat WhatsApp, dijawab Ananta W. Sasongko, CPA."
    desc = f"Audit laporan keuangan {low} oleh KAP DHN & Rekan (terdaftar OJK): akun rawan, dokumen yang disiapkan, dan alurnya. Tanya dulu lewat WhatsApp."
    if len(E(desc)) > 158: desc = f"Audit laporan keuangan {lw(i['pendek'])} oleh KAP DHN & Rekan (terdaftar OJK): akun rawan, dokumen, dan alurnya. Tanya dulu lewat WhatsApp."
    watxt = f"Halo Pak Ananta, saya ingin tanya audit laporan keuangan {low}."
    lkurl = f"/{K(i)}/"
    secs = [(f"Kapan {nm} Perlu Audit", f"<p>{E(i['pemicu'])}</p><p>{E(UMUM_WAJIB)}</p>"),
            (f"Akun yang Paling Diperhatikan Auditor di {i['pendek']}", tbl(["Area", "Yang Diuji"], i["audit"])),
            ("Dokumen yang Perlu Disiapkan", ul(i["dok"]) + f'<p>Belum lengkap? Mulai dari laporan keuangan dan rekening koran. Bila laporan keuangannya belum ada, lihat <a href="{lkurl}">jasa laporan keuangan {E(low)}</a>.</p>'),
            ("Alur Audit", '<ol class="flow5"><li><b>Diskusi awal</b>Ruang lingkup, pemakai laporan, dan jadwal.</li><li><b>Perikatan</b>Surat perikatan dengan KAP DHN &amp; Rekan dan daftar dokumen.</li><li><b>Pekerjaan lapangan</b>Pengujian akun, konfirmasi, dan penghitungan fisik bila material.</li><li><b>Laporan auditor</b>Opini auditor independen dan surat kepada manajemen.</li></ol>'
                           '<p>Opini adalah keputusan independen auditor berdasarkan bukti. Untuk satu perusahaan, penyusun laporan keuangan dan auditornya selalu kantor yang berbeda.</p>'),
            (f"Audit {i['pendek']} per Provinsi", links([(f"/{a}/{ps}/", pn) for ps, pn, _ in PROV])),
            ("Audit untuk Industri Lain", other_ind(i, "audit") + f'<p><a href="{HUB}">Lihat semua industri</a> · <a href="/jasa-audit-laporan-keuangan/">Audit per kota dan kabupaten</a></p>')]
    faq = FAQ_AUDIT(i, "") + i["faq"]
    URLS.append(page(f"/{a}/", f"Audit Laporan Keuangan · {i['pendek']}", h1, lead, watxt, ("/jasa-audit-laporan-keuangan/", "Semua Layanan Audit"),
                     TIM_AUDIT, f"Setiap industri punya akun yang paling sering menjadi perhatian auditor. Untuk {i['who']}, berikut yang perlu disiapkan sebelum audit dimulai.",
                     secs, faq, title, desc, f"Audit Laporan Keuangan {nm}", "Financial statement audit",
                     [("FA Indonesia", "/"), ("Audit Laporan Keuangan", "/jasa-audit-laporan-keuangan/"), (i["pendek"], f"/{a}/")], OGA, MARK))
    # ---------- audit per provinsi ----------
    for ps, pn, kab in PROV:
        t2 = f"Audit Laporan Keuangan {i['pendek']} di {pn}"
        if len(t2) > 60: t2 = f"Audit LK {i['pendek']} di {pn}"
        if len(t2) > 60: t2 = f"Audit LK {i['pendek']} {pn}"
        d2 = f"Audit laporan keuangan {lw(i['pendek'])} di {pn} oleh KAP DHN & Rekan (terdaftar OJK), melayani {len(kab)} kabupaten dan kota. Tanya dulu lewat WhatsApp."
        w2 = f"Halo Pak Ananta, saya ingin tanya audit laporan keuangan {low} di {pn}."
        s2 = [(f"Akun yang Diperhatikan Auditor di {i['pendek']}", tbl(["Area", "Yang Diuji"], i["audit"])),
              ("Dokumen yang Perlu Disiapkan", ul(i["dok"])),
              (f"Kabupaten dan Kota di {pn}", links([(f"/jasa-audit-laporan-keuangan/{s}/", n) for s, n in kab if os.path.exists(P(f"/jasa-audit-laporan-keuangan/{s}/"))])),
              (f"Audit Industri Lain di {pn}", other_ind(i, "audit", ps))]
        f2 = [(f"Ada audit laporan keuangan {low} di {pn}?", f"Ada. KAP DHN & Rekan melayani {i['who']} di seluruh {pn}. Sebagian besar pengujian berjalan dari dokumen digital, dengan kunjungan lapangan terjadwal."),
              ] + FAQ_AUDIT(i, f" di {pn}")[:2] + i["faq"][:1]
        URLS.append(page(f"/{a}/{ps}/", f"Audit {i['pendek']} · {pn}", f"Audit Laporan Keuangan {nm} di {pn}",
                         f"Audit laporan keuangan (audit LK) untuk {i['who']} di {pn}. Audit dan opini oleh KAP DHN & Rekan yang terdaftar di OJK.",
                         w2, (f"/{a}/", f"Audit {i['pendek']}"), TIM_AUDIT,
                         f"Melayani {len(kab)} kabupaten dan kota di {pn}. Dokumen dikirim lewat Google Drive, pertemuan daring, dan kunjungan lapangan dijadwalkan untuk penghitungan fisik bila material.",
                         s2, f2, t2, d2, f"Audit Laporan Keuangan {nm} {pn}", "Financial statement audit",
                         [("FA Indonesia", "/"), ("Audit Laporan Keuangan", "/jasa-audit-laporan-keuangan/"), (i["pendek"], f"/{a}/"), (pn, f"/{a}/{ps}/")], OGA, MARK))
    # ---------- pilar LK baru ----------
    if not i["lk"]: continue
    k = K(i)
    title = f"Jasa Laporan Keuangan {i['pendek']}: Pembukuan sampai Siap Audit"
    if len(title) > 60: title = f"Jasa Laporan Keuangan {i['pendek']}"
    h1 = f"Jasa Laporan Keuangan {nm}: Pembukuan, Tutup Buku, dan Siap Audit"
    lead = f"Pembukuan dan penyusunan laporan keuangan untuk {i['who']}. Disusun KJA Farhani K.N., dan bila perlu diaudit KAP DHN & Rekan sebagai kantor yang berbeda."
    desc = f"Jasa laporan keuangan {lw(i['pendek'])}: pembukuan bulanan, tutup buku, laporan untuk bank dan investor, siap audit. Disusun KJA Farhani. Tanya lewat WhatsApp."
    watxt = f"Halo Pak Ananta, saya ingin tanya jasa laporan keuangan untuk {low}."
    DLV = [("Laporan keuangan lengkap", "Neraca, laba rugi, arus kas, perubahan ekuitas, CALK", "Bulanan atau tahunan"),
           ("Rekonsiliasi", "Bank, piutang, utang, persediaan, aset tetap", "Bulanan"),
           ("Penyesuaian pajak", "Selaras dengan SPT dan pelaporan pajak", "Bulanan dan tahunan"),
           ("Paket bank atau investor", "Laporan dan rasio yang dibaca analis", "Saat dibutuhkan")]
    secs = [(f"Yang Kami Kerjakan untuk {i['pendek']}", tbl(["Bagian", "Isi"], i["lk"])),
            ("Deliverables yang Anda Terima", tbl(["Deliverable", "Isi", "Waktu"], DLV)),
            ("Bila Laporan Akan Diaudit", f'<p>Laporan disusun dengan kertas kerja pendukung yang dibaca auditor. Audit dikerjakan kantor yang berbeda: <a href="/{a}/">audit laporan keuangan {E(low)}</a> oleh KAP DHN &amp; Rekan.</p>' + ul(i["dok"])),
            (f"Laporan Keuangan {i['pendek']} per Provinsi", links([(f"/{k}/{ps}/", pn) for ps, pn, _ in PROV])),
            ("Jenis Usaha Lain", links([(f"/{u}/", n) for u, n in LAMA] + [(f"/{K(j)}/", j["pendek"]) for j in IND if j["lk"] and j["slug"] != i["slug"]]))]
    URLS.append(page(f"/{k}/", f"Laporan Keuangan · {i['pendek']}", h1, lead, watxt, ("/jasa-penyusunan-laporan-keuangan/", "Penyusunan Laporan Keuangan"),
                     lk2(low, "") + TIM_LK, f"Setiap jenis usaha punya titik rawan sendiri dalam pembukuan. Untuk {i['who']}, berikut bagian yang paling menentukan kualitas laporannya.",
                     secs, FAQ_LK(i, "") + i["faq"][1:], title, desc, f"Jasa Laporan Keuangan {nm}", "Bookkeeping and financial statement preparation",
                     [("FA Indonesia", "/"), ("Penyusunan Laporan Keuangan", "/jasa-penyusunan-laporan-keuangan/"), (i["pendek"], f"/{k}/")], OGK, MARK))
    for ps, pn, kab in PROV:
        t2 = f"Jasa Laporan Keuangan {i['pendek']} di {pn}"
        if len(t2) > 60: t2 = f"Laporan Keuangan {i['pendek']} di {pn}"
        if len(t2) > 60: t2 = f"Laporan Keuangan {i['pendek']} {pn}"
        d2 = f"Jasa laporan keuangan {lw(i['pendek'])} di {pn}: pembukuan, tutup buku, siap bank dan audit. Disusun KJA Farhani, melayani {len(kab)} kabupaten dan kota."
        w2 = f"Halo Pak Ananta, saya ingin tanya jasa laporan keuangan untuk {low} di {pn}."
        s2 = [(f"Yang Kami Kerjakan untuk {i['pendek']}", tbl(["Bagian", "Isi"], i["lk"])),
              (f"Kabupaten dan Kota di {pn}", links([(f"/jasa-penyusunan-laporan-keuangan/{s}/", n) for s, n in kab])),
              ("Jenis Usaha Lain", links([(f"/{u}/{ps}/", n) for u, n in LAMA if os.path.exists(P(f"/{u}/{ps}/"))] + [(f"/{K(j)}/{ps}/", j["pendek"]) for j in IND if j["lk"] and j["slug"] != i["slug"]]))]
        f2 = [(f"Ada jasa laporan keuangan {low} di {pn}?", f"Ada. KJA Farhani K.N. melayani {i['who']} di seluruh {pn}, dengan dokumen digital dan pertemuan daring.")] + FAQ_LK(i, f" di {pn}")[1:]
        URLS.append(page(f"/{k}/{ps}/", f"Laporan Keuangan {i['pendek']} · {pn}", f"Jasa Laporan Keuangan {nm} di {pn}",
                         f"Pembukuan dan laporan keuangan untuk {i['who']} di {pn}. Disusun KJA Farhani K.N., siap dibaca bank, investor, dan auditor.",
                         w2, (f"/{k}/", f"Laporan Keuangan {i['pendek']}"), lk2(low, pn) + TIM_LK,
                         f"Melayani {len(kab)} kabupaten dan kota di {pn}. Dokumen dikirim lewat Google Drive, pertemuan daring, kunjungan dijadwalkan bila diperlukan.",
                         s2, f2, t2, d2, f"Jasa Laporan Keuangan {nm} {pn}", "Bookkeeping and financial statement preparation",
                         [("FA Indonesia", "/"), ("Penyusunan Laporan Keuangan", "/jasa-penyusunan-laporan-keuangan/"), (i["pendek"], f"/{k}/"), (pn, f"/{k}/{ps}/")], OGK, MARK))

# ---------- hub ----------
rows = [(f'<a href="/{A(i)}/">Audit {E(i["pendek"])}</a>', f'<a href="/{K(i)}/">Laporan Keuangan {E(i["pendek"])}</a>', E(i["who"][:1].upper() + i["who"][1:])) for i in IND]
hub_tbl = ('<div class="tblwrap"><table class="tbl"><thead><tr><th>Audit oleh KAP</th><th>Penyusunan Laporan Keuangan</th><th>Untuk</th></tr></thead><tbody>'
           + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
URLS.append(page(HUB, "Audit dan Laporan Keuangan · Per Industri", "Audit dan Laporan Keuangan per Industri",
                 "Audit oleh KAP DHN & Rekan yang terdaftar di OJK dan penyusunan laporan keuangan oleh KJA Farhani K.N., dengan perhatian pada akun yang khas di tiap industri.",
                 "Halo Pak Ananta, saya ingin tanya audit atau laporan keuangan untuk usaha saya.", ("/jasa-audit-laporan-keuangan/", "Audit per Kota dan Kabupaten"),
                 lk2("perusahaan", ""), f"Pilih industri Anda. Tiap halaman memuat akun yang paling diperhatikan auditor, dokumen yang perlu disiapkan, dan halaman per provinsi. {UMUM_WAJIB}",
                 [("Daftar Industri", hub_tbl),
                  ("Industri Anda Belum Ada", "<p>Daftar ini bertambah. Bila industri Anda belum tercantum, ceritakan jenis usahanya lewat WhatsApp. Lihat juga <a href=\"/jasa-audit-laporan-keuangan-bpr/\">audit BPR</a>, <a href=\"/jasa-audit-laporan-keuangan/\">audit per kota dan kabupaten</a>, dan <a href=\"/jasa-penyusunan-laporan-keuangan/\">penyusunan laporan keuangan per kota dan kabupaten</a>.</p>")],
                 [("Siapa yang mengaudit dan siapa yang menyusun?", "Audit dan opini oleh KAP DHN & Rekan (terdaftar OJK). Penyusunan laporan keuangan oleh KJA Farhani K.N. Untuk satu perusahaan, keduanya selalu kantor yang berbeda. FA Indonesia adalah pintu kontaknya."),
                  ("Apakah melayani seluruh Indonesia?", "Ya. Sebagian besar pekerjaan berjalan dari dokumen digital, dengan kunjungan lapangan terjadwal bila diperlukan."),
                  ("Bagaimana memulai?", "Kirim gambaran usaha dan tujuan laporan lewat WhatsApp. Dari sana ruang lingkup dan jadwalnya diusulkan.")],
                 "Audit dan Laporan Keuangan per Industri", "Audit dan laporan keuangan per industri: rumah sakit, restoran, cafe, hotel, manufaktur, data center, kontraktor, tambang, sawit, dan lainnya.",
                 "Audit dan Laporan Keuangan per Industri", "Financial statement audit",
                 [("FA Indonesia", "/"), ("Audit Laporan Keuangan", "/jasa-audit-laporan-keuangan/"), ("Per Industri", HUB)], OGA, MARK))

# ---------------- sisipan di halaman lama ----------------
def put(path, block, m0, before_pats):
    p = P(path)
    if not os.path.exists(p): print("lewat (tidak ada)", path); return 0
    t = rd(p); m1 = m0.replace("<!--", "<!--/")
    base = re.sub(re.escape(m0) + ".*?" + re.escape(m1), "", t, flags=re.S)
    b = m0 + block + m1
    for pat in before_pats:
        mm = re.search(pat, base)
        if mm: return wt(p, base[:mm.start()] + b + base[mm.start():])
    print("lewat (tanpa jangkar)", path); return 0

BEFORE = [r"<!--uq-lokal-->", r"<h2[^>]*>Pertanyaan Umum</h2>", r'<div class="faq-acc">']
ind_audit = '<h2 id="audit-per-industri">Audit Laporan Keuangan per Industri</h2>' + links([(f"/{A(i)}/", i["pendek"]) for i in IND]) + f'<p class="t"><a href="{HUB}">Lihat semua industri</a></p>'
ind_lk = '<h2 id="laporan-keuangan-per-industri">Laporan Keuangan per Industri</h2>' + links([(f"/{K(i)}/", i["pendek"]) for i in IND if i["lk"]] + [(f"/{u}/", n) for u, n in LAMA]) + f'<p class="t"><a href="{HUB}">Audit dan laporan keuangan per industri</a></p>'
n_ins = 0
n_ins += put("/jasa-audit-laporan-keuangan/", ind_audit, "<!--fa-ind12-->", BEFORE)
n_ins += put("/jasa-penyusunan-laporan-keuangan/", ind_lk, "<!--fa-ind12-->", BEFORE)
n_ins += put("/jasa-audit-laporan-keuangan-bpr/", ind_audit, "<!--fa-ind12-->", BEFORE)
for u, _ in LAMA: n_ins += put(f"/{u}/", ind_lk, "<!--fa-ind12-->", BEFORE)
rs = next(i for i in IND if i["slug"] == "rumah-sakit")
rs_line = (f'<p class="t"><b>Audit dan laporan keuangan rumah sakit:</b> <a href="/{A(rs)}/">Audit Laporan Keuangan Rumah Sakit oleh KAP</a> · '
           f'<a href="/{K(rs)}/">Jasa Laporan Keuangan Rumah Sakit</a> · <a href="/audit-laporan-keuangan-klinik/">Audit Klinik dan Apotek</a></p>')
for u in ("/konsultan-rumah-sakit/", "/konsultan-unit-cost-rumah-sakit/", "/konsultan-klinik/", "/konsultan-bpjs-rumah-sakit/"):
    n_ins += put(u, rs_line, "<!--fa-ind12-->", [r"<!--fa-rstim-->", r"<!--uq-lokal-->", r"<h2[^>]*>Pertanyaan Umum</h2>"])
# baris per kota/kabupaten/provinsi
top8 = ["rumah-sakit", "restoran-cafe", "hotel", "manufaktur", "kontraktor", "distributor", "koperasi", "yayasan", "data-center", "pma"]
x_audit = '<p class="t"><b>Audit per industri:</b> ' + " · ".join(f'<a href="/{A(i)}/">{E(i["pendek"])}</a>' for i in IND if i["slug"] in top8) + f' · <a href="{HUB}">Semua industri</a></p>'
x_lk = '<p class="t"><b>Laporan keuangan per industri:</b> ' + " · ".join(f'<a href="/{K(i)}/">{E(i["pendek"])}</a>' for i in IND if i["slug"] in top8) + f' · <a href="{HUB}">Semua industri</a></p>'
n_x = 0
for fam, blk in (("jasa-audit-laporan-keuangan", x_audit), ("jasa-penyusunan-laporan-keuangan", x_lk)):
    for p in glob.glob(os.path.join(OUT, fam, "*", "index.html")):
        rel = "/" + os.path.relpath(os.path.dirname(p), OUT).replace(os.sep, "/") + "/"
        n_x += put(rel, blk, "<!--fa-ind12x-->", BEFORE)

# ---------------- sitemap + llms ----------------
sm = os.path.join(OUT, "sitemap.xml"); s = rd(sm)
s = re.sub(r"<!--ind12-->.*?<!--/ind12-->\n?", "", s, flags=re.S)
blk = "<!--ind12-->" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in URLS) + "<!--/ind12-->\n"
wt(sm, s.replace("</urlset>", blk + "</urlset>"))
lp = os.path.join(OUT, "llms.txt"); l = rd(lp)
l = re.sub(r"\n<!--ind12-->.*?<!--/ind12-->", "", l, flags=re.S)
l = l.rstrip("\n") + ("\n<!--ind12-->\n\n## Audit dan Laporan Keuangan per Industri (12 Nov 2026)\n"
     f"- [Audit dan Laporan Keuangan per Industri]({D}{HUB}): daftar semua industri\n"
     + "".join(f"- [Audit Laporan Keuangan {i['nama']}]({D}/{A(i)}/): akun rawan, dokumen, alur; audit oleh KAP DHN & Rekan (terdaftar OJK)\n" for i in IND)
     + "".join(f"- [Jasa Laporan Keuangan {i['nama']}]({D}/{K(i)}/): pembukuan sampai siap audit; disusun KJA Farhani K.N.\n" for i in IND if i["lk"])
     + "<!--/ind12-->\n")
wt(lp, l)
print(f"industri: {len(IND)} | halaman: {len(URLS)} | sisipan pilar: {n_ins} | baris kota: {n_x} | file berubah: {len(CHANGED)}" + (" (dry)" if DRY else ""))
