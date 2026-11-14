# -*- coding: utf-8 -*-
"""Konsolidasi FA Apps jadi 4 aplikasi utama (14 Nov 2026): Saturn, Jupiter, Venus, Galaxy.
Bekerja di out/faindonesia (BUKAN prep penuh), hanya blok berpenanda + 3 halaman hub baru. Idempoten. --dry
- /apps/: blok 4 kartu besar (penanda fa4-hub), URL tool lama TIDAK berubah
- /apps/saturn|jupiter|venus/: hub per app baru; /galaxy/: blok hub + Cek PSAK 118 + materi UpdateSAK
- breadcrumb JSON-LD semua tool: Home > Apps > <App induk> > Tool ; breadcrumb terlihat di halaman statis
- sitemap.xml + llms.txt
"""
import os, re, sys, json, html
ROOT = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(ROOT, "out", "faindonesia")
DRY = "--dry" in sys.argv
B = "https://faindonesia.co.id"
U = "https://updatesak.com"

APPS = {
 "saturn": dict(n="FA Saturn", c="#4f8cff", hub="/apps/saturn/", k="Audit dan KAP",
   tag="Audit rapi dari perencanaan sampai sign-off",
   who="Untuk KAP, tim audit internal, dan akuntan yang menyusun kertas kerja audit.",
   desc="FA Saturn: aplikasi audit untuk KAP. Perencanaan, penilaian risiko berwarna (Tinggi merah, Sedang kuning, Rendah hijau), kertas kerja Excel, dan sign-off berjenjang.",
   lead="Satu tempat untuk seluruh siklus audit KAP: Planning, Penilaian Risiko, Respons Risiko, sampai Pelaporan. Tingkat risiko dibaca sekali lihat: Tinggi merah, Sedang kuning, Rendah hijau, baik di aplikasi web maupun di kertas kerja Excel.",
   tools=[("FA Saturn Workspace", "/saturn/", "Materialitas, CRA per akun dan asersi, program audit, review note, sign-off lima tingkat."),
          ("Metodologi FA Saturn", "/saturn/metodologi/", "Logika audit di balik tiap tahap, rujukan SA, dan cara membaca hasilnya."),
          ("Aplikasi Audit untuk KAP", "/aplikasi-audit-kap/", "Gambaran fitur, alur kerja, dan cara memulai untuk KAP.")],
   stages=[("1 Planning", "#4f8cff"), ("2 Penilaian Risiko", "#b07cf5"), ("3 Respons Risiko", "#19b5a5"), ("4 Pelaporan", "#ef7fb5")]),
 "jupiter": dict(n="FA Jupiter", c="#f2994a", hub="/apps/jupiter/", k="Laporan Keuangan Siap Audit",
   tag="Dari buku besar jadi laporan keuangan siap audit",
   who="Untuk perusahaan, bagian akuntansi, dan konsultan yang menyusun atau merapikan laporan keuangan.",
   desc="FA Jupiter: susun laporan keuangan PSAK atau SAK EMKM sampai siap audit, rapikan laporan keuangan berantakan, plus penyusutan, PPh 21, PPh Badan, dan potput PPN.",
   lead="Menyusun laporan keuangan PSAK atau SAK EMKM sampai siap audit, dan mengubah laporan keuangan yang berantakan jadi paket yang diminta auditor. Kalkulator pajak dan penyusutan di bawahnya membantu menutup angka akhir tahun.",
   tools=[("FA Jupiter Audit Ready", "/audit-ready/", "Upload COA dan buku besar, neraca saldo, jurnal penyesuaian, laporan keuangan PSAK atau SAK EMKM, lead schedule, dan checklist PBC."),
          ("Penyusutan Fiskal dan Pajak Tangguhan", "/kalkulator-penyusutan-fiskal/", "Hitung penyusutan komersial dan fiskal serta pajak tangguhan."),
          ("Kalkulator PPh 21 TER", "/kalkulator-pph-21/", "PPh 21 dengan tarif efektif rata-rata dan penyesuaian Desember."),
          ("Kalkulator PPh Badan dan UMKM", "/kalkulator-pph-badan/", "Estimasi PPh Badan, tarif final UMKM, dan fasilitas."),
          ("Kalkulator PPh Potput dan PPN", "/kalkulator-potput-ppn/", "Pemotongan atau pemungutan PPh dan perhitungan PPN.")]),
 "venus": dict(n="FA Venus", c="#e86fb0", hub="/apps/venus/", k="Akuntansi Manajemen dan Strategi",
   tag="Valuasi, kredit, dan keputusan keuangan terjawab dalam hitungan menit",
   who="Untuk pemilik usaha, direksi, CFO, dan manajemen rumah sakit yang mengambil keputusan pendanaan dan strategi.",
   desc="FA Venus: valuasi, DCF, kapasitas kredit, DSCR, cicilan, rasio, bankability, kesiapan pendanaan, dan toolkit rumah sakit (unit cost ABC, ABC-VEN obat, koding BPJS).",
   lead="Alat bantu keputusan manajemen: seberapa bernilai usaha, seberapa besar kredit yang masuk akal, apakah laporan keuangan terbaca bankable, dan di mana rumah sakit kehilangan margin. Isi angka usaha Anda, hasil langsung keluar di browser.",
   tools=[("Valuasi Rumah Sakit", "/kalkulator-valuasi-rumah-sakit/", "Harga jual RS sebelum dan sesudah dibenahi: EBITDA x multiple, nilai aset, utang bank."),
          ("Valuasi DCF dan WACC", "/kalkulator-valuasi-dcf/", "Nilai usaha dari arus kas diskonto."),
          ("Cek Kapasitas Kredit", "/cek-kapasitas-kredit/", "Perkiraan plafon kredit yang masuk akal dari arus kas dan agunan."),
          ("Kalkulator DSCR", "/kalkulator-dscr/", "Debt service coverage ratio dan ruang cicilan."),
          ("Kalkulator Cicilan dan Biaya Kredit", "/kalkulator-cicilan-pinjaman/", "Cicilan, bunga efektif, dan total biaya kredit."),
          ("Cek Kesehatan Keuangan dan Altman Z", "/kalkulator-rasio-keuangan/", "Rasio keuangan dan skor Altman Z."),
          ("Bankability Index", "/bankability-index/", "Seberapa layak laporan keuangan Anda di mata bank."),
          ("Cek Kesiapan Pendanaan", "/cek-kesiapan-pendanaan/", "Daftar periksa kesiapan sebelum mengajukan pendanaan."),
          ("Simulasi Plafon Kredit Usaha", "/simulasi-plafon-kredit-usaha/", "Simulasi plafon kredit usaha dari data keuangan."),
          ("Cek Kelayakan IPO", "/cek-kelayakan-ipo/", "Penyaringan awal kesiapan IPO."),
          ("Unit Cost RS Berbasis ABC", "/kalkulator-unit-cost-rumah-sakit/", "Unit cost per layanan dan layanan rugi tersembunyi."),
          ("Analisis ABC-VEN Obat RS", "/analisis-abc-ven-obat-rumah-sakit/", "EOQ, titik pesan ulang, kas terkunci, kedaluwarsa."),
          ("Cek Koding INA-CBG", "/cek-koding-bpjs-ina-cbg/", "Under-coding, pending klaim, dan dispute."),
          ("AI Analis Keuangan RS", "/analis-ai-rumah-sakit/", "Indikator Barber-Johnson dan analisis AI."),
          ("Hub Toolkit Rumah Sakit", "/fa-venus-rumah-sakit/", "Semua alat FA Venus untuk rumah sakit dan klinik.")]),
 "galaxy": dict(n="FA Galaxy", c="#19b5a5", hub="/galaxy/", k="Belajar, Legenda, dan Kamus",
   tag="Tempat belajar standar, membaca hasil, dan memakai tiga aplikasi lain",
   who="Untuk mahasiswa, staf akuntansi, auditor, dan siapa saja yang ingin paham logika di balik angka.",
   desc="FA Galaxy: tempat belajar SAK dan standar audit, tutorial FA Saturn, Jupiter, Venus, dan Cek PSAK 118. Materi standar mengambil dari Update SAK.",
   lead="Pintu belajar di ekosistem FA. Galaxy merangkum cara pakai Saturn, Jupiter, dan Venus, memuat Cek PSAK 118, dan menautkan materi standar dari Update SAK yang tetap berdiri sendiri.",
   tools=[("Panduan dan Metodologi FA Galaxy", "/galaxy/", "Cara pakai dan logika di balik FA Jupiter, Saturn, dan Venus."),
          ("Cek PSAK 118", "/cek-psak-118/", "Konversi laporan laba rugi ke PSAK 118: kategori, subtotal, dan ukuran kinerja."),
          ("Update PSAK Terbaru", U + "/update-psak-terbaru/", "Daftar PSAK dan ISAK terbaru dari Update SAK."),
          ("SAK EMKM", U + "/update-sak-emkm/", "Standar untuk entitas mikro, kecil, dan menengah."),
          ("SAK EP", U + "/update-sak-ep/", "Standar untuk entitas privat."),
          ("Standar Audit (SA)", U + "/standar-audit/", "Ringkasan SA dan kerangka asurans."),
          ("Penerapan PSAK", U + "/penerapan-psak/", "Langkah penerapan PSAK di perusahaan."),
          ("Menghadapi Auditor", U + "/menghadapi-auditor/", "Persiapan dokumen dan komunikasi dengan auditor."),
          ("Jadwal Ujian Profesi", U + "/jadwal-ujian/", "Jadwal ujian profesi akuntan.")],
   soon=["IFRS", "US GAAP", "Kamus Istilah"]),
}

BUKTI = {
 "saturn": "Dibuat sendiri oleh FA. Alur audit mengikuti Standar Audit (SA) IAPI yang merujuk ISA, dengan pendekatan berbasis risiko seperti praktik firma audit global.",
 "jupiter": "Dibuat sendiri oleh FA. Penyajian mengikuti PSAK dan SAK EMKM, dengan kontrol tied-up dan lead schedule seperti yang diminta auditor.",
 "venus": "Dibuat sendiri oleh FA. Metodenya lazim di praktik advisory global: DCF, WACC, multiple, dan DSCR.",
 "galaxy": "Dibuat sendiri oleh FA. Materi mengacu pada SAK IAI, standar audit, dan rujukan IFRS.",
}
# slug halaman tool -> (app, nama tool)
TOOLMAP = {}
for ak, a in APPS.items():
    for nm, url, _ in a["tools"]:
        if url.startswith("/") and ak != "galaxy" or url in ("/cek-psak-118/", "/galaxy/"):
            TOOLMAP[url.strip("/")] = (ak, nm)
TOOLMAP["kalkulator-pajak"] = ("jupiter", "Hub Kalkulator Pajak")
TOOLMAP.pop("fa-venus-rumah-sakit", None); TOOLMAP["fa-venus-rumah-sakit"] = ("venus", "Hub Toolkit Rumah Sakit")
TOOLMAP.pop("galaxy", None)
TOOLMAP.pop("kalkulator-pajak", None)


def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t):
    if DRY: return
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(t)
def esc(s): return html.escape(s, quote=True)
def full(u): return u if u.startswith("http") else B + u

CSS = """<style id="fa4-css">
.fa4{margin:0 0 44px}.fa4 h2{margin:6px 0 8px;font-size:clamp(26px,3.2vw,38px);line-height:1.15}
.fa4 .lead{margin:0 0 22px;color:var(--muted);font-size:16px;line-height:1.6;max-width:66ch}
.fa4 .g4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.fa4 .c4{display:flex;flex-direction:column;gap:10px;padding:22px 22px 20px;border:1px solid var(--line);border-top:5px solid var(--ac);border-radius:10px;background:linear-gradient(180deg,color-mix(in srgb,var(--ac) 10%,var(--panel,#1a1a1a)),var(--panel,#1a1a1a) 55%);color:var(--ink)}
.fa4 .c4 .kk{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ac);font-weight:600}
.fa4 .c4 h3{margin:0;font-family:var(--f-display,serif);font-weight:400;font-size:30px;line-height:1.15;letter-spacing:0;text-transform:none;color:var(--ink)}.fa4 .c4 h3::before{content:none;display:none}
.fa4 .c4 p{margin:0;color:var(--muted);font-size:14.5px;line-height:1.55}
.fa4 .bk{margin:0;padding:9px 12px;border-left:3px solid var(--ac);background:rgba(127,127,127,.08);border-radius:0 6px 6px 0;font-size:13px;color:var(--muted);line-height:1.5}.fa4 .bk b{color:var(--ink);font-weight:600}
.fa4 .chips{display:flex;flex-wrap:wrap;gap:7px;margin:4px 0 6px}
.fa4 .chips a,.fa4 .chips span{font-size:12.5px;line-height:1;padding:7px 10px;border-radius:999px;border:1px solid var(--line);color:var(--ink);text-decoration:none;background:rgba(127,127,127,.08)}
.fa4 .chips a:hover{border-color:var(--ac)}.fa4 .chips .soon{color:var(--muted);border-style:dashed}
.fa4 .go{align-self:flex-start;margin-top:auto;display:inline-flex;align-items:center;height:40px;padding:0 18px;border-radius:999px;background:var(--ac);color:#111;font-weight:600;font-size:14px;text-decoration:none}
.fa4 .go:hover{opacity:.9}
.fa4 .stg{display:flex;flex-wrap:wrap;gap:6px;margin:2px 0}.fa4 .stg span{font-size:11.5px;font-weight:600;padding:5px 9px;border-radius:999px;color:#10131a}
.fa4 .tg{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}
.fa4 .t4{display:flex;flex-direction:column;gap:6px;padding:16px 18px;border:1px solid var(--line);border-left:4px solid var(--ac);border-radius:8px;background:var(--panel,#1a1a1a);color:var(--ink);text-decoration:none}
.fa4 .t4:hover{border-color:var(--ac)}.fa4 .t4 b{font-family:var(--f-display,serif);font-weight:400;font-size:19px;line-height:1.25}
.fa4 .t4 span{color:var(--muted);font-size:13.5px;line-height:1.5}
.fa4 .sib{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}.fa4 .sib a{padding:9px 14px;border-radius:999px;border:1px solid var(--line);color:var(--ink);text-decoration:none;font-size:13.5px}
.fa4 .sib a.on{background:var(--ac);color:#111;border-color:var(--ac);font-weight:600}
.fa4-bc{margin:6px 0 14px;font-size:12.5px;color:var(--muted)}.fa4-bc a{color:var(--muted);text-decoration:none}.fa4-bc a:hover{color:var(--ink)}.fa4-bc b{color:var(--ink);font-weight:500}
@media(max-width:760px){.fa4 .g4{grid-template-columns:1fr}}
</style>"""


def hub_block():
    out = ['<!--fa4-hub-->', CSS, '<section class="sec fa4" id="empat-app" aria-label="Empat aplikasi utama FA"><p class="kick">FA Apps</p>',
           '<h2>Empat Aplikasi Utama FA</h2>',
           '<p class="lead">Semua alat FA dikelompokkan jadi empat aplikasi. Pilih sesuai pekerjaan Anda; alamat tiap alat tetap sama.</p><div class="g4">']
    for ak in ("jupiter", "saturn", "venus", "galaxy"):
        a = APPS[ak]
        chips = "".join('<a href="%s">%s</a>' % (esc(u), esc(nm)) for nm, u, _ in a["tools"][:6])
        more = len(a["tools"]) - 6
        if more > 0: chips += '<a href="%s">+%d lainnya</a>' % (a["hub"], more)
        for s in a.get("soon", []): chips += '<span class="soon">%s (segera)</span>' % esc(s)
        stg = ""
        if a.get("stages"):
            stg = '<div class="stg">' + "".join('<span style="background:%s">%s</span>' % (c, esc(n)) for n, c in a["stages"]) + "</div>"
        out.append('<article class="c4" style="--ac:%s"><span class="kk">%s</span><h3>%s</h3><p><b>%s.</b> %s</p>%s<p class="bk">%s</p><div class="chips">%s</div><a class="go" href="%s" data-fa4="%s">Buka %s</a></article>'
                   % (a["c"], esc(a["k"]), esc(a["n"]), esc(a["tag"]), esc(a["who"]), stg, esc(BUKTI[ak]), chips, a["hub"], ak, esc(a["n"])))
    out.append("</div></section><!--/fa4-hub-->")
    return "".join(out)


def sibs(cur):
    s = '<div class="sib">'
    for ak in ("jupiter", "saturn", "venus", "galaxy"):
        s += '<a%s href="%s">%s</a>' % (' class="on"' if ak == cur else "", APPS[ak]["hub"], esc(APPS[ak]["n"]))
    return s + '<a href="/apps/">Semua FA Apps</a></div>'


def hub_main(ak):
    a = APPS[ak]
    stg = ""
    if a.get("stages"):
        stg = '<div class="stg" style="margin:0 0 20px">' + "".join('<span style="background:%s">%s</span>' % (c, esc(n)) for n, c in a["stages"]) + "</div>"
    cards = "".join('<a class="t4" href="%s"><b>%s</b><span>%s</span></a>' % (esc(u), esc(nm), esc(d)) for nm, u, d in a["tools"])
    return ('<main data-tidy="1" id="top"><div class="wrap">' + CSS + '<section class="sec fa4" style="--ac:%s">' % a["c"] +
            '<nav class="fa4-bc" aria-label="Breadcrumb"><a href="/">FA Indonesia</a> › <a href="/apps/">FA Apps</a> › <b>%s</b></nav>' % esc(a["n"]) +
            '<p class="kick" style="color:%s">%s</p><h1 style="font-family:var(--f-display,serif);font-weight:400;font-size:clamp(34px,5vw,58px);line-height:1.1;margin:6px 0 12px">%s: %s</h1>' % (a["c"], esc(a["n"]), esc(a["n"]), esc(a["k"])) +
            '<p class="lead">%s</p><p class="bk" style="max-width:66ch;margin:0 0 18px">%s</p>%s<h2 style="font-size:clamp(22px,2.6vw,30px)">Alat di %s</h2><div class="tg">%s</div>' % (esc(a["lead"]), esc(BUKTI[ak]), stg, esc(a["n"]), cards) +
            (('<p class="lead" style="margin-top:18px">Segera hadir: %s.</p>' % ", ".join(a["soon"])) if a.get("soon") else "") +
            sibs(ak) + '</section></div></main>')


def build_hub(ak, tpl):
    a = APPS[ak]
    url = B + a["hub"]
    title = "%s: %s | FA Indonesia" % (a["n"], a["k"])
    t = tpl
    t = re.sub(r"<title>.*?</title>", "<title>%s</title>" % esc(title), t, 1, flags=re.S)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', '<meta content="%s" name="description"/>' % esc(a["desc"]), t, 1)
    t = re.sub(r'<link href="[^"]*" rel="canonical"/>', '<link href="%s" rel="canonical"/>' % url, t, 1)
    t = re.sub(r'<meta content="[^"]*" property="og:title"/>', '<meta content="%s" property="og:title"/>' % esc(title), t, 1)
    t = re.sub(r'<meta content="[^"]*" property="og:description"/>', '<meta content="%s" property="og:description"/>' % esc(a["desc"]), t, 1)
    t = re.sub(r'<meta content="[^"]*" property="og:url"/>', '<meta content="%s" property="og:url"/>' % url, t, 1)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#page", "name": title, "url": url, "description": a["desc"], "isPartOf": {"@id": B + "/#website"} if False else {"@type": "WebSite", "url": B + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "FA Indonesia", "item": B + "/"},
            {"@type": "ListItem", "position": 2, "name": "FA Apps", "item": B + "/apps/"},
            {"@type": "ListItem", "position": 3, "name": a["n"], "item": url}]},
        {"@type": "ItemList", "name": "Alat di " + a["n"], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": nm, "url": full(u)} for i, (nm, u, _) in enumerate(a["tools"])]}]}
    ldx = '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False)
    # ganti JSON-LD ItemList apps dengan milik hub
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: ldx, t, 1, flags=re.S)
    i = t.find('<main data-tidy="1">'); j = t.find("</main>") + len("</main>")
    assert i > 0 and j > i
    t = t[:i] + hub_main(ak) + t[j:]
    # skrip filter grid /apps/ tidak relevan di hub (merujuk elemen yang tidak ada)
    t = re.sub(r'<script>\s*\(function\(\)\{"use strict";\s*const \$=s=>document\.querySelector.*?</script>', "", t, count=1, flags=re.S)
    # buang skrip filter khusus grid /apps/ yang merujuk elemen tidak ada tidak perlu; dibiarkan (dilindungi null-check dicek lewat browser)
    return t


changed = {"hub": 0, "apps": 0, "bc": 0, "galaxy": 0, "psak118": 0}

# ---------------- 1. /apps/ ----------------
ap = os.path.join(FA, "apps", "index.html"); T = rd(ap); tpl_apps = T
blk = hub_block()
if "<!--fa4-hub-->" in T:
    T2 = re.sub(r"<!--fa4-hub-->.*?<!--/fa4-hub-->", lambda m: blk, T, 1, flags=re.S)
else:
    k = T.find('<section class="sec" id="video"'); assert k > 0
    T2 = T[:k] + blk + T[k:]
if T2 != T: changed["apps"] += 1; wr(ap, T2)
tpl_for_hubs = T  # template tanpa efek blok (blok tidak dipakai di hub karena main diganti)

# ---------------- 2. halaman hub ----------------
for ak in ("saturn", "jupiter", "venus"):
    p = os.path.join(FA, "apps", ak, "index.html")
    new = build_hub(ak, tpl_for_hubs)
    if not os.path.exists(p) or rd(p) != new: changed["hub"] += 1; wr(p, new)

# ---------------- 3. breadcrumb tool ----------------
def patch_bc(slug, ak, nm):
    p = os.path.join(FA, slug, "index.html")
    if not os.path.exists(p): return
    t = rd(p); o = t; a = APPS[ak]
    hub = B + a["hub"]
    def fix(m):
        s = m.group(1)
        if "BreadcrumbList" not in s or hub in s: return m.group(0)
        d = json.loads(s)
        def walk(x):
            if isinstance(x, dict):
                if x.get("@type") == "BreadcrumbList":
                    its = x["itemListElement"]
                    idx = next((i for i, it in enumerate(its) if str(it.get("item", "")).rstrip("/") == B + "/apps"), None)
                    if idx is not None:
                        its.insert(idx + 1, {"@type": "ListItem", "position": 0, "name": a["n"], "item": hub})
                        for i, it in enumerate(its): it["position"] = i + 1
                for v in x.values(): walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
        walk(d)
        return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)
    t = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, t, flags=re.S)
    # breadcrumb terlihat: halaman statis dengan <main ...><div class="wrap"> atau <main id="top">
    if "fa4-bc" not in t and slug not in ("saturn", "audit-ready", "cek-psak-118"):
        bc = ('<nav class="fa4-bc fa4" aria-label="Breadcrumb" style="--ac:%s"><a href="/">FA Indonesia</a> › <a href="/apps/">FA Apps</a> › <a href="%s">%s</a> › <b>%s</b></nav>'
              % (a["c"], a["hub"], esc(a["n"]), esc(nm)))
        m = re.search(r"<main[^>]*>", t)
        if m:
            css = "" if 'id="fa4-css"' in t else CSS
            t = t[:m.end()] + '<div class="wrap" style="padding-top:10px">' + css + bc + "</div>" + t[m.end():]
    if t != o: changed["bc"] += 1; wr(p, t)

for slug, (ak, nm) in TOOLMAP.items(): patch_bc(slug, ak, nm)
patch_bc("cek-psak-118", "galaxy", "Cek PSAK 118")
patch_bc("galaxy", "galaxy", "Panduan dan Metodologi") if False else None

# ---------------- 4. Galaxy: blok hub ----------------
gp = os.path.join(FA, "galaxy", "index.html"); G = rd(gp); a = APPS["galaxy"]
gb = ["<!--fa4-galaxy-->", CSS, '<section class="fa4" style="--ac:%s;padding:8px 0 28px"><div class="wrap"><h2 style="font-size:clamp(24px,3vw,34px)">Belajar, Legenda, dan Kamus</h2>' % a["c"],
      '<p class="lead">%s</p><div class="tg">' % esc(a["lead"])]
for nm, u, d in a["tools"][1:]:
    gb.append('<a class="t4" href="%s"%s><b>%s</b><span>%s</span></a>' % (esc(u), ' rel="noopener" target="_blank"' if u.startswith("http") else "", esc(nm), esc(d)))
gb.append('</div><p class="lead" style="margin-top:16px">Segera hadir: %s.</p>%s</div></section><!--/fa4-galaxy-->' % (", ".join(a["soon"]), sibs("galaxy")))
gb = "".join(gb)
if "<!--fa4-galaxy-->" in G:
    G2 = re.sub(r"<!--fa4-galaxy-->.*?<!--/fa4-galaxy-->", lambda m: gb, G, 1, flags=re.S)
else:
    k = G.find('<article class="gx-sec" id="jupiter">'); assert k > 0
    # sisip sebelum pembungkus gx-sec pertama: cari awal section/div induk terdekat tidak perlu; sisip langsung sebelum artikel
    G2 = G[:k] + gb + G[k:]
if G2 != G: changed["galaxy"] += 1; wr(gp, G2)

# ---------------- 5. sitemap + llms ----------------
sp = os.path.join(FA, "sitemap.xml"); S = rd(sp); add = ""
for ak in ("saturn", "jupiter", "venus"):
    loc = B + APPS[ak]["hub"]
    if loc not in S: add += '<url><loc>%s</loc><lastmod>2026-11-14</lastmod><priority>0.7</priority></url>\n' % loc
if add: wr(sp, S.replace("</urlset>", add + "</urlset>", 1)); changed["sitemap"] = add.count("<url>")
lp = os.path.join(FA, "llms.txt"); L = rd(lp)
if "/apps/saturn/" not in L:
    ins = ("\n## Empat Aplikasi Utama FA (14 Nov 2026)\n"
           + "".join("- %s: %s (%s%s)\n" % (APPS[k]["n"], APPS[k]["k"], B, APPS[k]["hub"]) for k in ("saturn", "jupiter", "venus", "galaxy")))
    wr(lp, L.rstrip("\n") + "\n" + ins); changed["llms"] = 1
# ---------------- 6. Cek PSAK 118 pindah label ke Galaxy ----------------
for rel in ("apps/index.html", "cek-psak-118/index.html"):
    fp = os.path.join(FA, rel); x = rd(fp); y = x.replace("FA Venus \u00b7 Konversi PL PSAK 118", "FA Galaxy \u00b7 Konversi PL PSAK 118").replace("FA Venus - Konversi PL PSAK 118", "FA Galaxy - Konversi PL PSAK 118")
    if y != x: changed["psak118"] += 1; wr(fp, y)
print(changed)
