#!/usr/bin/env python3
"""28 Nov 2026: CA dan US mudah di-reach + jualan sendiri (konsultasi, audit, penyusunan LK).

Bos 28 Nov: gaya konsultan dan KAP pada umumnya susah di-reach (konsultasi awal berbayar, estimasi biaya
profesi lain baru muncul belakangan). FA, CA, US kebalikannya. "Tanpa banyak omong. Pake tabel dan animasi."
Lalu: "CA dan US belum optimal per kota per kecamatan. Dengan produknya sendiri. Tidak perlu selalu nyambung
dengan FA. Tapi sama, jualan konsultasi, audit, penyusunan LK."

Bekerja di out/cariakuntan dan out/updatesak. Idempoten, --dry.
JALANKAN PALING AKHIR untuk CA dan US (sesudah tiga_niat_20261127.py dan fa_drc_ananta_20261127.py),
lalu `python3 shared/thin_noindex.py out cariakuntan`.

1. /css/rx28.css di dua situs + <link id="rx28-css"> di halaman yang memuat blok.
2. Pita <!--rx28s--> (4 langkah beranimasi: chat WA, diskusi awal tanpa biaya, estimasi total tertulis,
   mulai bila cocok) tepat di bawah header halaman.
3. Tabel <!--rx28--> tiga produk (konsultasi, audit, susun LK) dengan tombol WA per baris. Pesan WA memuat
   domain, lokasi/halaman, dan produk (atribut data-rx28).
   CA: semua /kota/** (kota, daftar KAP/KJA/KJPP, layanan per kota, kecamatan, kawasan), /kota/,
       /akuntan-<segmen>/, pilar jasa, beranda. Artikel CA hanya pita.
   US: beranda (pita + tabel di bawah hero), halaman dalam (pita di bawah header, tabel sebelum blok bantuan).
4. CA /kota/<kota>/jasa-laporan-keuangan/ (113) dibuka lagi untuk indeks dengan sudut produk CA sendiri:
   title + H1 "Susun Laporan Keuangan di <Kota> oleh KJA Berizin", description baru, masuk sitemap.
   (shared/thin_noindex.py: jasa-laporan-keuangan dikeluarkan dari CA_JASA.)
Tanpa harga, tanpa janji waktu atau opini, tanpa kalimat yang menonjolkan nama orang, tanpa perbandingan
dengan kantor lain.
"""
import html, os, re, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
DRY = "--dry" in sys.argv
WA = "https://wa.me/6282245260121?text="
VER = "20261128"
stat = {}


def bump(k, n=1):
    stat[k] = stat.get(k, 0) + n


CSS = """/* rx28 (28 Nov 2026): pita mudah di-reach + tabel tiga produk. Dibuat caus_reach_20261128.py */
.rx28s{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;margin:22px 0 0;padding:0;list-style:none;border:1px solid var(--line,#e4e4e0);border-radius:3px;background:#fff;position:relative;overflow:hidden;counter-reset:rx28}
.rx28s li{position:relative;margin:0;padding:14px 16px 14px 46px;font:500 .92rem/1.3 var(--body,inherit);color:var(--ink,#141414);counter-increment:rx28;opacity:0;transform:translateY(6px);animation:rx28in .5s ease forwards}
.rx28s li+li{border-left:1px solid var(--line,#e4e4e0)}
.rx28s li:nth-child(2){animation-delay:.25s}.rx28s li:nth-child(3){animation-delay:.5s}.rx28s li:nth-child(4){animation-delay:.75s}
.rx28s li::before{content:counter(rx28);position:absolute;left:14px;top:50%;width:22px;height:22px;margin-top:-11px;border-radius:50%;background:#141414;color:#fff;font:600 .72rem/22px var(--body,inherit);text-align:center;animation:rx28step 6s linear infinite}
.rx28s li:nth-child(2)::before{animation-delay:1.5s}.rx28s li:nth-child(3)::before{animation-delay:3s}.rx28s li:nth-child(4)::before{animation-delay:4.5s}
.rx28s li small{display:block;margin-top:2px;font-weight:400;font-size:.78rem;color:var(--muted,#6b6b66)}
.rx28s::after{content:"";position:absolute;left:0;bottom:0;height:2px;width:25%;background:#1fa855;animation:rx28run 6s linear infinite}
.rx28{margin:26px 0 8px}
.rx28 h2{margin:0 0 12px;font:500 clamp(1.25rem,2.2vw,1.6rem)/1.2 var(--rx-serif,Georgia,serif);color:var(--ink,#141414);border:0;padding:0}
.rx28 h2 i{display:inline-block;width:9px;height:9px;margin-right:10px;border-radius:50%;background:#1fa855;vertical-align:middle;animation:rx28pulse 1.8s ease-out infinite}
.rx28 table{width:100%;border-collapse:collapse;margin:0;font-size:.93rem;background:#fff;border:1px solid var(--line,#e4e4e0)}
.rx28 th{background:#141414;color:#fff;font:600 .72rem/1.2 var(--body,inherit);letter-spacing:.08em;text-transform:uppercase;text-align:left;padding:11px 14px}
.rx28 td{padding:13px 14px;border-top:1px solid var(--line,#e4e4e0);vertical-align:middle;color:var(--ink,#141414);line-height:1.35}
.rx28 td b{display:block;font:500 1.05rem/1.2 var(--rx-serif,Georgia,serif)}
.rx28 td span{display:block;font-size:.8rem;color:var(--muted,#6b6b66);margin-top:2px}
.rx28 tbody tr{opacity:0;transform:translateY(8px);animation:rx28in .5s ease forwards;transition:background .2s}
.rx28 tbody tr:nth-child(1){animation-delay:.3s}.rx28 tbody tr:nth-child(2){animation-delay:.5s}.rx28 tbody tr:nth-child(3){animation-delay:.7s}
.rx28 tbody tr:hover{background:#f6f6f2}
.rx28 a.rx28w{display:inline-block;white-space:nowrap;padding:9px 14px;border-radius:2px;background:#141414;color:#fff!important;font:600 .82rem/1 var(--body,inherit);text-decoration:none!important;transition:background .2s,transform .2s}
.rx28 a.rx28w::before{content:"";display:inline-block;width:7px;height:7px;margin-right:8px;border-radius:50%;background:#1fa855;vertical-align:1px}
.rx28 a.rx28w:hover{background:#1fa855;transform:translateX(2px)}
.rx28 a.rx28w:hover::before{background:#fff}
@keyframes rx28in{to{opacity:1;transform:none}}
@keyframes rx28run{0%{left:0}25%{left:25%}50%{left:50%}75%{left:75%}100%{left:100%}}
@keyframes rx28step{0%,20%{background:#1fa855}25%,100%{background:#141414}}
@keyframes rx28pulse{0%{box-shadow:0 0 0 0 rgba(31,168,85,.55)}100%{box-shadow:0 0 0 10px rgba(31,168,85,0)}}
@media(max-width:760px){
.rx28s{grid-template-columns:repeat(2,minmax(0,1fr))}
.rx28s li{padding:12px 10px 12px 40px;font-size:.84rem}
.rx28s li::before{left:10px}
.rx28s li:nth-child(3){border-left:0}
.rx28s li:nth-child(n+3){border-top:1px solid var(--line,#e4e4e0)}
.rx28s::after{display:none}
.rx28 table,.rx28 tbody,.rx28 tr,.rx28 td{display:block;width:auto}
.rx28 thead{position:absolute;left:-9999px}
.rx28 table{border:0;background:none}
.rx28 tbody tr{border:1px solid var(--line,#e4e4e0);background:#fff;margin:0 0 10px;padding:12px 14px}
.rx28 td{border:0;padding:3px 0}
.rx28 td[data-l]::before{content:attr(data-l) ": ";font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted,#6b6b66)}
.rx28 td:last-child{padding-top:10px}
}
@media(prefers-reduced-motion:reduce){.rx28s li,.rx28 tbody tr{animation:none;opacity:1;transform:none}.rx28s::after,.rx28s li::before,.rx28 h2 i{animation:none}}
"""

STRIP = ('<!--rx28s--><ol class="rx28s" aria-label="Cara menghubungi kami">'
         '<li>Chat WhatsApp<small>Tanpa form, tanpa janji temu</small></li>'
         '<li>Diskusi Awal<small>Tanpa biaya</small></li>'
         '<li>Estimasi Total Tertulis<small>Termasuk biaya profesi lain</small></li>'
         '<li>Mulai Bila Cocok<small>Tanpa ikatan sebelum setuju</small></li>'
         '</ol><!--/rx28s-->')

# produk sendiri per situs: (kunci, kebutuhan, nama produk, anda kirim, anda terima, kalimat WA)
PROD = {
    "cariakuntan.com": [
        ("konsul", "Konsultasi", "Pilih Kantor 15 Menit", "Cerita singkat kebutuhan Anda",
         "Jalur yang tepat: KAP, KJA, KJPP, atau konsultan pajak", "Mau konsultasi pilih kantor."),
        ("audit", "Audit", "Audit oleh KAP Berizin", "Neraca dan laba rugi seadanya",
         "Laporan auditor independen dari KAP terdaftar", "Mau tanya audit laporan keuangan."),
        ("lk", "Susun LK", "Laporan Keuangan oleh KJA Berizin", "Rekening koran atau catatan usaha",
         "Laporan keuangan lengkap dengan CALK", "Mau tanya penyusunan laporan keuangan."),
    ],
    "updatesak.com": [
        ("konsul", "Konsultasi", "Klinik PSAK", "Transaksi atau pertanyaan Anda",
         "Jurnal, perhitungan, dan rujukan standarnya", "Mau konsultasi penerapan PSAK."),
        ("audit", "Audit", "Audit Sesuai Standar Audit Terbaru", "Neraca saldo atau draf laporan",
         "Laporan auditor independen dari KAP terdaftar", "Mau tanya audit laporan keuangan."),
        ("lk", "Susun LK", "Laporan Keuangan Sesuai SAK Terbaru", "Data seadanya",
         "Laporan keuangan dan CALK sesuai SAK yang berlaku", "Mau tanya penyusunan laporan keuangan."),
    ],
}


def table(dom, where, lokasi=None):
    """where = keterangan sumber di pesan WA; lokasi = nama daerah untuk judul (CA)."""
    judul = "Konsultasi, Audit, dan Penyusunan Laporan Keuangan"
    if lokasi:
        judul += " di " + lokasi
    rows = []
    for key, need, name, kirim, terima, ask in PROD[dom]:
        msg = "Halo, saya dari %s (%s). %s" % (dom, where, ask)
        rows.append(
            '<tr><td data-l="Kebutuhan">%s</td><td><b>%s</b></td><td data-l="Anda kirim">%s</td>'
            '<td data-l="Anda terima">%s</td><td><a class="rx28w" data-rx28="%s" href="%s%s" rel="noopener" '
            'target="_blank">Chat WhatsApp</a></td></tr>'
            % (need, html.escape(name), html.escape(kirim), html.escape(terima), key, WA, quote(msg, safe="/")))
    return ('<!--rx28--><section class="rx28" id="mulai-chat" aria-label="Layanan dan cara menghubungi">'
            '<h2><i aria-hidden="true"></i>%s</h2>'
            '<table><thead><tr><th>Kebutuhan</th><th>Layanan</th><th>Anda Kirim</th><th>Anda Terima</th>'
            '<th>Mulai</th></tr></thead><tbody>%s</tbody></table></section><!--/rx28-->'
            % (html.escape(judul), "".join(rows)))


RX_S = re.compile(r"<!--rx28s-->.*?<!--/rx28s-->", re.S)
RX_T = re.compile(r"<!--rx28-->.*?<!--/rx28-->", re.S)
LINK = '<link href="/css/rx28.css?v=%s" id="rx28-css" rel="stylesheet"/>' % VER


def strip_old(s):
    s = re.sub(r'<div class="rx28wrap"[^>]*>(?:<!--rx28s-->.*?<!--/rx28s-->)?(?:<!--rx28-->.*?<!--/rx28-->)?</div>', "", s, flags=re.S)
    s = RX_S.sub("", s)
    s = RX_T.sub("", s)
    s = re.sub(r'<link href="/css/rx28\.css[^>]*>', "", s)
    return s


def add_css(s):
    return s.replace("</head>", LINK + "</head>", 1)


def after_rxh(s, block):
    """Sisipkan tepat sesudah </header> milik <header class="rxh">."""
    i = s.find('<header class="rxh">')
    if i < 0:
        return s, False
    j = s.find("</header>", i)
    if j < 0:
        return s, False
    j += len("</header>")
    return s[:j] + block + s[j:], True


def after_hero(s, block):
    i = s.find('<section class="hero"')
    if i < 0:
        return s, False
    j = s.find("</section>", i)
    if j < 0:
        return s, False
    j += len("</section>")
    return s[:j] + '<div class="rx28wrap" style="max-width:1100px;margin:0 auto;padding:0 20px">' + block + "</div>" + s[j:], True


def h1_text(s):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""


def write(p, old, new, key):
    if new != old:
        bump(key)
        if not DRY:
            open(p, "w", encoding="utf-8").write(new)


def walk(site):
    root = os.path.join(OUT, site)
    for d, _, fs in os.walk(root):
        if "index.html" in fs:
            p = os.path.join(d, "index.html")
            yield p, os.path.relpath(p, root).replace(os.sep, "/")


# ---------- CariAkuntan ----------
CA_PILAR = re.compile(r"^(?:akuntan-[^/]+|konsultan-[^/]+|jasa-[^/]+(?:/[^/]+)?|pendampingan-audit|laporan-keuangan-sabh|"
                      r"layanan/[^/]+|kap-murah|akuntan-forensik|cek-kebutuhan|lk-siap-bank)/index\.html$")
CITY = {}


def ca_cities():
    kroot = os.path.join(OUT, "cariakuntan", "kota")
    for slug in sorted(os.listdir(kroot)):
        p = os.path.join(kroot, slug, "index.html")
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        m = re.search(r'data-city="([^"]+)"', s)
        name = html.unescape(m.group(1)) if m else slug.replace("-", " ").title()
        kja = re.search(r"<b>(\d+)</b><span>KJA berizin aktif", s)
        CITY[slug] = (name, int(kja.group(1)) if kja else 0)


def ca_lokasi(rel, s):
    """Nama daerah untuk judul tabel dan pesan WA."""
    parts = rel.split("/")
    if parts[0] != "kota" or len(parts) < 3:
        return None
    city = CITY.get(parts[1], (parts[1].replace("-", " ").title(), 0))[0]
    if len(parts) >= 5 and parts[2] == "kecamatan":
        m = re.search(r'<p class="label"[^>]*>Kecamatan ([^·<]+)', s)
        kec = html.unescape(m.group(1)).strip() if m else parts[3].replace("-", " ").title()
        return "Kecamatan %s, %s" % (kec, city)
    return city


def ca_lk_page(rel, s):
    """/kota/<kota>/jasa-laporan-keuangan/: sudut produk CA sendiri + buka indeks."""
    slug = rel.split("/")[1]
    name, kja = CITY.get(slug, (slug.title(), 0))
    title = "Susun Laporan Keuangan di %s oleh KJA Berizin" % name
    if len(title) > 60:
        title = "Susun Laporan Keuangan %s oleh KJA Berizin" % name
    h1 = "Susun Laporan Keuangan di %s oleh KJA Berizin" % name
    if kja:
        desc = ("Penyusunan laporan keuangan di %s oleh Kantor Jasa Akuntan berizin: %d KJA aktif di registri "
                "PPPK. Kirim data seadanya, diskusi awal tanpa biaya." % (name, kja))
    else:
        desc = ("Penyusunan laporan keuangan di %s oleh Kantor Jasa Akuntan berizin, dikerjakan jarak jauh. "
                "Kirim data seadanya, diskusi awal tanpa biaya." % name)
    if len(desc) > 158:
        desc = ("Penyusunan laporan keuangan di %s oleh Kantor Jasa Akuntan berizin. Kirim data seadanya, "
                "diskusi awal tanpa biaya." % name)
    e = html.escape
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % e(title), s, count=1, flags=re.S)
    s = re.sub(r'(<meta[^>]+name="description"[^>]+content=")[^"]*(")', lambda m: m.group(1) + e(desc) + m.group(2), s, count=1)
    s = re.sub(r'(<meta[^>]+content=")[^"]*("[^>]+name="description")', lambda m: m.group(1) + e(desc) + m.group(2), s, count=1)
    for prop in ("og:title", "twitter:title"):
        s = re.sub(r'(<meta[^>]+(?:property|name)="%s"[^>]+content=")[^"]*(")' % prop, lambda m: m.group(1) + e(title) + m.group(2), s)
        s = re.sub(r'(<meta[^>]+content=")[^"]*("[^>]+(?:property|name)="%s")' % prop, lambda m: m.group(1) + e(title) + m.group(2), s)
    for prop in ("og:description", "twitter:description"):
        s = re.sub(r'(<meta[^>]+(?:property|name)="%s"[^>]+content=")[^"]*(")' % prop, lambda m: m.group(1) + e(desc) + m.group(2), s)
        s = re.sub(r'(<meta[^>]+content=")[^"]*("[^>]+(?:property|name)="%s")' % prop, lambda m: m.group(1) + e(desc) + m.group(2), s)
    s = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1) + e(h1) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(data-tool=")[^"]*(")', lambda m: m.group(1) + e(h1) + m.group(2), s, count=1)
    s = re.sub(r'<meta name="robots" content="noindex,follow">', "", s)
    return s


def ca():
    ca_cities()
    lk_urls = []
    for p, rel in walk("cariakuntan"):
        top = rel.split("/")[0]
        if top in ("en", "zh", "hokkien", "kdmp", "magang", "screening", "files", "bayar"):
            continue
        old = open(p, encoding="utf-8").read()
        s = strip_old(old)
        if rel == "index.html":
            s, ok = after_hero(s, STRIP + table("cariakuntan.com", "beranda"))
            if ok:
                s = add_css(s)
            write(p, old, s, "CA beranda")
            continue
        if top == "artikel":
            s, ok = after_rxh(s, STRIP)
            if ok:
                s = add_css(s)
            write(p, old, s, "CA artikel (pita)")
            continue
        is_kota = top == "kota"
        if not (is_kota or CA_PILAR.match(rel)):
            continue
        if re.match(r"^kota/[^/]+/jasa-laporan-keuangan/index\.html$", rel):
            s = ca_lk_page(rel, s)
            lk_urls.append("https://cariakuntan.com/" + rel[:-len("index.html")])
        lokasi = ca_lokasi(rel, s) if is_kota else None
        where = lokasi or h1_text(s) or "cariakuntan.com"
        s, ok = after_rxh(s, STRIP + table("cariakuntan.com", where, lokasi))
        if ok:
            s = add_css(s)
        write(p, old, s, "CA kota" if is_kota else "CA pilar/segmen")
    # sitemap: 113 halaman susun LK per kota masuk lagi
    sp = os.path.join(OUT, "cariakuntan", "sitemap.xml")
    sm = open(sp, encoding="utf-8").read()
    add = ["  <url><loc>%s</loc><lastmod>2026-11-28</lastmod></url>\n" % u for u in sorted(lk_urls) if "<loc>%s</loc>" % u not in sm]
    if add:
        sm2 = sm.replace("</urlset>", "".join(add) + "</urlset>")
        bump("CA sitemap +URL", len(add))
        if not DRY:
            open(sp, "w", encoding="utf-8").write(sm2)


# ---------- UpdateSAK ----------
def us():
    for p, rel in walk("updatesak"):
        top = rel.split("/")[0]
        if top in ("bayar", "dosen"):
            continue
        old = open(p, encoding="utf-8").read()
        s = strip_old(old)
        if rel == "index.html":
            s, ok = after_hero(s, STRIP + table("updatesak.com", "beranda"))
            if ok:
                s = add_css(s)
            write(p, old, s, "US beranda")
            continue
        where = h1_text(s) or "updatesak.com"
        s, ok = after_rxh(s, STRIP)
        if not ok:
            continue
        t = table("updatesak.com", where)
        i = s.find('<section aria-label="Bantuan Tim" class="fa-cta2">')
        if i < 0:
            i = s.find("<!--rx13f-->")
        if i < 0:
            i = s.find("<footer")
        if i >= 0:
            s = s[:i] + t + s[i:]
        s = add_css(s)
        write(p, old, s, "US halaman dalam")


def main():
    for site in ("cariakuntan", "updatesak"):
        cp = os.path.join(OUT, site, "css", "rx28.css")
        cur = open(cp, encoding="utf-8").read() if os.path.exists(cp) else ""
        if cur != CSS:
            bump(site + " css")
            if not DRY:
                open(cp, "w", encoding="utf-8").write(CSS)
    ca()
    us()
    for k in sorted(stat):
        print("%-28s %d" % (k, stat[k]))
    if not stat:
        print("0 perubahan")


if __name__ == "__main__":
    main()
