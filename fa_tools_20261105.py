# -*- coding: utf-8 -*-
"""5 Nov 2026: keunggulan layanan FA (non-apps) = semua dikerjakan dengan tools buatan FA sendiri
(FA Jupiter, FA Saturn, FA Venus) yang dibangun mengikuti standar kertas kerja KAP (SA/SPAP IAPI)
dan metodologi advisory firma Big Four. Dipasang di semua halaman layanan FA sebagai:
  1. blok "Dikerjakan dengan Tools Buatan FA Sendiri" (3 kartu tool sesuai jenis layanan) sebelum
     blok tim (fa-wajah) atau sebelum Pertanyaan Umum;
  2. satu butir FAQ + Question di schema FAQPage;
  3. meta description yang > 160 karakter dipendekkan (agar tidak terpotong di Google).
Idempoten (penanda fa-tools). Jalankan setelah fa_venus_unggulan_20261104.py, sebelum kja_kota_20261101.py."""
import os, re, glob, json
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FA-Indonesia_Website_SIAP-UPLOAD-v58")

CSS = ('<style id="fa-tools-css">.ftl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:14px 0 12px}'
 '.ftl a{display:block;padding:14px 16px 15px;border:1px solid #333;border-radius:12px;background:#1b1b1b;color:inherit;text-decoration:none}'
 '.ftl a:hover{border-color:#777}.ftl small{display:block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;opacity:.65;margin-bottom:5px}'
 '.ftl b{display:block;font-size:15px;line-height:1.3;font-weight:600}.ftl span{display:block;font-size:12.5px;line-height:1.5;opacity:.78;margin-top:5px}'
 '.ftl-std{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 18px;margin:12px 0 6px;padding:0;list-style:none}'
 '.ftl-std li{font-size:14px;line-height:1.5;padding-left:16px;position:relative}.ftl-std li:before{content:"";position:absolute;left:0;top:.6em;width:7px;height:7px;border-radius:50%;background:#9c8f6c}'
 '@media(max-width:620px){.ftl,.ftl-std{grid-template-columns:1fr}}</style>')

# tool = (url, label kecil, nama, keterangan)
JUP = ("/audit-ready/", "FA Jupiter", "Laporan Keuangan Audit Ready", "Neraca saldo menjadi laporan keuangan lengkap dengan CALK format auditor, untuk SAK Indonesia, SAK EP, dan SAK EMKM.")
SAT = ("/saturn/", "FA Saturn", "Audit Workspace Standar KAP", "Kertas kerja audit mengikuti Standar Audit IAPI: materialitas, penilaian risiko per asersi, prosedur substantif, dan sign-off berjenjang.")
VEN_K = ("/cek-kapasitas-kredit/", "FA Venus", "Cek Kapasitas Kredit", "Plafon menurut DSCR, Utang/EBITDA, DER, dan agunan, memakai cara pandang analis kredit bank.")
VEN_DSCR = ("/kalkulator-dscr/", "FA Venus", "Kalkulator DSCR dan Rasio", "Rasio yang dibaca bank dihitung lebih dulu, sebelum berkas diajukan.")
VEN_P = ("/cek-psak-118/", "FA Venus", "Cek PSAK 118", "Simulasi penyajian laba rugi format baru yang wajib mulai tahun buku 2027.")
VEN_IPO = ("/cek-kelayakan-ipo/", "FA Venus", "Cek Kelayakan IPO", "Uji syarat papan utama, pengembangan, dan akselerasi BEI dari angka laporan keuangan.")
VEN_DCF = ("/kalkulator-valuasi-dcf/", "FA Venus", "Valuasi DCF", "Nilai usaha dengan arus kas terdiskonto, cara yang dipakai investor dan penilai.")
VEN_RS = ("/kalkulator-valuasi-rumah-sakit/", "FA Venus", "Valuasi Rumah Sakit", "Harga jual rumah sakit sebelum dan sesudah dirapikan, dari EBITDA dan tempat tidur.")
VEN_BI = ("/bankability-index/", "FA Venus", "Bankability Index", "Skor kesiapan perusahaan di mata bank, dari rasio dan kualitas laporan.")
VEN_TAX = ("/kalkulator-pph-badan/", "FA Venus", "Kalkulator PPh Badan", "Rekonsiliasi fiskal dan PPh Badan dihitung dari laporan keuangan yang sama.")

CAT = {
 "lk":    (JUP, VEN_P, SAT),
 "psak":  (JUP, VEN_P, SAT),
 "audit": (SAT, JUP, VEN_DSCR),
 "kredit":(VEN_K, VEN_DSCR, JUP),
 "ipo":   (VEN_IPO, JUP, SAT),
 "val":   (VEN_DCF, JUP, VEN_RS),
 "rs":    (VEN_RS, JUP, VEN_K),
 "umum":  (JUP, SAT, VEN_K),
}
def cat_of(rel):
    r = rel.lower()
    if r.startswith(("konsultan-rumah-sakit", "konsultan-unit-cost-rumah-sakit", "rumah-sakit-dijual")): return "rs"
    if "psak" in r or "sak-ep" in r or "konsolidasi" in r: return "psak"
    if "audit" in r or "komite" in r or "gcg" in r or "sppg" in r or "koperasi" in r or "kampanye" in r or "statutory" in r: return "audit"
    if "kredit" in r or "bankability" in r or "konsultan-keuangan" in r or "akuntan-terdekat" in r: return "kredit"
    if "ipo" in r or "cfo" in r: return "ipo"
    if "valuasi" in r or "dijual" in r: return "val"
    if "laporan" in r or "pembukuan" in r: return "lk"
    return "umum"

STD = ('<ul class="ftl-std">'
 '<li><b>Standar kertas kerja KAP:</b> FA Saturn disusun dari Standar Audit (SA) dan SPAP IAPI, dengan tahapan perencanaan, materialitas, dan review berjenjang seperti di kantor akuntan publik.</li>'
 '<li><b>Metodologi advisory firma Big Four:</b> alur kerja FA mengikuti pola yang dipelajari tim saat berkarier di Ernst &amp; Young: hipotesis dulu, data kemudian, lalu dokumentasi yang bisa ditelusuri.</li>'
 '<li><b>Dibangun dan dipakai sendiri:</b> tools ini dibuat tim FA dari pengalaman menyusun laporan keuangan, mengawal kredit, dan mendampingi audit, lalu dipakai di setiap penugasan.</li>'
 '<li><b>Bisa Anda coba dulu:</b> sebagian besar tools terbuka gratis di <a href="/apps/">FA Apps</a>, jadi Anda melihat cara kerja kami sebelum memutuskan.</li></ul>')

def block(rel, h="h2"):
    tools = CAT[cat_of(rel)]
    cards = "".join(f'<a href="{u}"><small>{l}</small><b>{n}</b><span>{d}</span></a>' for u, l, n, d in tools)
    return (f'<!--fa-tools--><{h}>Dikerjakan dengan Tools Buatan FA Sendiri</{h}>'
            '<p>Setiap penugasan FA Indonesia dikerjakan dengan perangkat yang kami bangun sendiri, bukan template umum. '
            'Hasilnya konsisten dari satu klien ke klien lain, dan angkanya bisa ditelusuri sampai ke sumbernya.</p>'
            f'<div class="ftl">{cards}</div>{STD}<!--/fa-tools-->')

FAQ_Q = "Tools apa yang dipakai FA Indonesia dalam mengerjakan layanan ini?"
FAQ_A = ("Tools buatan FA sendiri: FA Jupiter untuk laporan keuangan audit ready, FA Saturn untuk kertas kerja audit berstandar KAP (SA/SPAP IAPI), "
         "dan kalkulator FA Venus untuk kredit, PSAK 118, IPO, dan valuasi. Alur kerjanya mengikuti metodologi advisory firma Big Four, "
         "tempat tim FA pernah berkarier, dan sebagian besar tools bisa dicoba gratis di faindonesia.co.id/apps/.")
FAQ_HTML = f'<p style="margin:0 0 18px" data-fa-tools-faq><b>{FAQ_Q}</b><br>{FAQ_A}</p>'

def add_faq(t):
    t = re.sub(r'<p style="margin:0 0 18px" data-fa-tools-faq>.*?</p>\n?', "", t, flags=re.S)
    m = re.search(r"<h2>Pertanyaan Umum</h2>(</div>)?\n?", t)
    if not m: return t, False
    t = t[:m.end()] + FAQ_HTML + "\n" + t[m.end():]
    # schema FAQPage
    def fix(mm):
        try: d = json.loads(mm.group(1))
        except Exception: return mm.group(0)
        g = d.get("@graph", [d])
        for x in g:
            if x.get("@type") == "FAQPage":
                x["mainEntity"] = [q for q in x.get("mainEntity", []) if q.get("name") != FAQ_Q]
                x["mainEntity"].append({"@type": "Question", "name": FAQ_Q, "acceptedAnswer": {"@type": "Answer", "text": FAQ_A}})
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"
    t = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, t, count=1, flags=re.S)
    return t, True

DESC = {
 "bpr-dijual": "BPR dijual: daftar BPR yang ditawarkan FA Indonesia untuk investor, dengan data keuangan, NPL, dan struktur harga. Ditangani sampai persetujuan OJK.",
 "cfo-direktur-keuangan-ipo": "CFO dan Direktur Keuangan berpengalaman IPO di BEI: tata kelola Tbk, audit historis, financial model, dan kredit bank lebih dari Rp1 triliun. Tim ex EY.",
 "cfo-paruh-waktu": "CFO paruh waktu (fractional CFO) untuk perusahaan yang belum perlu Direktur Keuangan penuh waktu: laporan keuangan, pajak, bank, investor, dan tata kelola.",
 "jasa-audit-laporan-keuangan": "Jasa audit laporan keuangan lewat KAP mitra terdaftar OJK untuk SABH, bank, investor, dan tender. Siap audit dengan tools FA Jupiter dan FA Saturn.",
 "jasa-transisi-sak-ep-ke-psak": "Pendampingan transisi SAK EP ke PSAK (SAK Indonesia): pemetaan perbedaan, penyajian kembali saldo awal, CALK, dan laporan siap audit dengan FA Jupiter.",
 "jasa-valuasi-usaha": "Valuasi usaha untuk UMKM dan usaha perorangan: normalisasi laba, DCF, multiple, nilai aset, sampai bahan negosiasi investor. Dihitung dengan tools FA Venus.",
 "komite-audit-komisaris-independen": "Ananta W. Sasongko, CPA terbuka untuk peran Komite Audit dan Komisaris Independen perusahaan Tbk, pra-IPO, BUMN/BUMD, dan rumah sakit. Latar EY dan CFO.",
 "konsultan-keuangan": "Konsultan keuangan untuk perusahaan menengah: laporan keuangan, kredit bank, investor, dan tata kelola, dikerjakan dengan tools FA berstandar KAP dan Big Four.",
 "konsultan-kredit-bank": "Pendampingan pengajuan kredit bank hingga cair: financial model, paket kredit, due diligence, komite kredit. Kumulatif lebih dari Rp1,1 triliun, tools FA Venus.",
 "konsultan-kredit-distributor-importir": "Konsultan kredit bank untuk distributor dan importir: plafon modal kerja dari siklus kas, DSCR, LC dan SKBDN, laporan keuangan yang dibaca analis kredit.",
 "konsultan-persiapan-ipo": "Pendampingan persiapan IPO di BEI dari sisi perusahaan: tata kelola, audit laporan keuangan historis, financial model, data room, koordinasi penjamin emisi.",
 "konsultan-rumah-sakit": "Konsultan keuangan rumah sakit swasta: studi kelayakan, kredit bank, akuisisi dan divestasi, investor, unit cost dan tarif. Tools valuasi rumah sakit buatan FA.",
 "laporan-keuangan-audit-sppg": "Laporan keuangan dan audit SPPG (dapur MBG): pembukuan dana, laporan pertanggungjawaban, dan audit oleh KAP mitra, disiapkan dengan tools FA berstandar KAP.",
 "laporan-keuangan-umkm": "Jasa laporan keuangan UMKM sesuai SAK EMKM dan SAK EP, siap pajak, kredit bank, dan audit. Disusun dengan FA Jupiter, mulai Rp2,5 juta per bulan.",
 "laporan-tahunan-pt": "Laporan tahunan PT untuk RUPS dan pelaporan AHU: laporan keuangan, laporan direksi, dan catatan sesuai UU PT, disusun dengan tools FA berstandar auditor.",
 "layanan": "Layanan FA Indonesia: laporan keuangan, audit lewat KAP mitra, kredit bank, investor, IPO, valuasi, GCG. Dikerjakan dengan tools FA berstandar KAP dan Big Four.",
 "pendampingan-gcg": "Pendampingan GCG untuk perusahaan pra-IPO, BUMD, dan rumah sakit: organ perseroan, Komite Audit, SOP, dan audit internal, dengan kertas kerja standar KAP.",
 "rumah-sakit-dijual": "Rumah sakit dijual: daftar RS swasta yang ditawarkan FA Indonesia untuk investor, dengan data tempat tidur, EBITDA, dan rentang harga. Valuasi dengan tools FA.",
}
def shorten_desc(t, rel=""):
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    if not m: return t
    d = m.group(1)
    if rel in DESC: cut = DESC[rel]
    elif len(d) <= 160: return t
    else:
        cut = d[:158]
        k = max(cut.rfind(". "), cut.rfind(", "))
        cut = (cut[:k] if k > 90 else cut.rsplit(" ", 1)[0]).rstrip(" ,;:") + "."
    if cut == d: return t
    t = t.replace(m.group(0), f'<meta name="description" content="{cut}"', 1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda mm: mm.group(1) + cut + mm.group(2), t, count=1)
    return t

SKIP = ("artikel/", "en/", "ja/", "ko/", "zh/", "toko", "buku", "apps", "galaxy", "bayar", "kebijakan", "syarat", "mitra-", "kap-dhn",
        "kja", "files", "img", "404", "audit-ready", "saturn", "cek-", "simulasi", "kalkulator", "bankability", "unduhan", "ananta-w-sasongko", "seller", "bursa-komite-audit")
n = f = d = 0
for p in sorted(glob.glob(os.path.join(B, "**", "index.html"), recursive=True)):
    rel = os.path.relpath(p, B)[:-10].rstrip("/")
    if rel == "." or any(rel.startswith(s) for s in SKIP): continue
    t = open(p, encoding="utf-8").read()
    if "<h2>Pertanyaan Umum</h2>" not in t and "fa-wajah" not in t: continue
    t = re.sub(r"<!--fa-tools-->.*?<!--/fa-tools-->", "", t, flags=re.S)
    k = t.find("<!--fa-wajah-->")
    if k < 0: k = t.find("<h2>Pertanyaan Umum</h2>")
    if k < 0: continue
    t = t[:k] + block(rel) + t[k:]
    if "fa-tools-css" not in t: t = t.replace("</head>", CSS + "</head>", 1)
    t, ok = add_faq(t); f += ok
    t2 = shorten_desc(t, rel); d += (t2 != t); t = t2
    open(p, "w", encoding="utf-8").write(t); n += 1

# /layanan/: blok di atas "Tiga Orang" (sudah ada fa-lay-tim) sebagai section sendiri
p = os.path.join(B, "layanan", "index.html"); t = open(p, encoding="utf-8").read()
t = re.sub(r"<!--fa-tools-sec-->.*?<!--/fa-tools-sec-->", "", t, flags=re.S)
sec = ('<!--fa-tools-sec--><section class="block alt" id="tools-fa"><div class="wrap">' + block("umum").replace("<!--fa-tools-->", "").replace("<!--/fa-tools-->", "") + '</div></section><!--/fa-tools-sec-->')
k = t.find("<!--fa-lay-tim-->")
if k < 0: k = t.find('id="badan-usaha"'); k = t.rfind("<section", 0, k) if k > 0 else t.rfind("</main>")
t = t[:k] + sec + t[k:]
if "fa-tools-css" not in t: t = t.replace("</head>", CSS + "</head>", 1)
t = shorten_desc(t, "layanan")
open(p, "w", encoding="utf-8").write(t)

# beranda: satu kalimat di bawah Pendekatan/Pilih Jalur kalau belum ada
p = os.path.join(B, "index.html"); t = open(p, encoding="utf-8").read()
t = re.sub(r"<!--fa-tools-home-->.*?<!--/fa-tools-home-->", "", t, flags=re.S)
home = ('<!--fa-tools-home--><div class="wrap" style="padding-top:8px;padding-bottom:28px"><p style="margin:0;font-size:15px;line-height:1.6;opacity:.85">Semua layanan dikerjakan dengan tools buatan FA sendiri '
        '(<a href="/audit-ready/">FA Jupiter</a>, <a href="/saturn/">FA Saturn</a>, <a href="/cek-kapasitas-kredit/">FA Venus</a>), '
        'dibangun mengikuti standar kertas kerja KAP dan metodologi advisory firma Big Four. <a href="/layanan/#tools-fa">Lihat caranya</a>.</p></div><!--/fa-tools-home-->')
k = t.find("<!--fa-wajah-->")
if k < 0:
    m = re.search(r'id="cara-mulai"', t); k = t.rfind("<section", 0, m.start()) if m else t.rfind("</main>")
t = t[:k] + home + t[k:]
open(p, "w", encoding="utf-8").write(t)

# llms.txt
p = os.path.join(B, "llms.txt")
if os.path.exists(p):
    t = open(p, encoding="utf-8").read()
    line = "\n## Cara kerja\n- Semua layanan dikerjakan dengan tools buatan FA sendiri: FA Jupiter (laporan keuangan audit ready), FA Saturn (kertas kerja audit standar SA/SPAP IAPI), FA Venus (kalkulator kredit, PSAK 118, IPO, valuasi). Metodologi mengikuti praktik advisory firma Big Four; sebagian besar tools gratis di https://faindonesia.co.id/apps/\n"
    if "tools buatan FA sendiri" not in t: open(p, "w", encoding="utf-8").write(t.rstrip() + "\n" + line)
print("fa_tools: halaman", n, "| faq", f, "| desc dipendekkan", d)
