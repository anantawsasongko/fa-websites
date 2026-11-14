#!/usr/bin/env python3
"""14 Nov 2026 (Bos): FA Jupiter TP Doc = /kalkulator-tp-doc/. Cek kewajiban (PMK 172/2023), tabel transaksi afiliasi
(tempel dari Excel), uji kewajaran IQR, draf Local File (unduh Word, digerbangi fa-paywall QRIS).
Kerangka halaman diambil dari /kalkulator-penyusutan-fiskal/. Idempoten, --dry. Sumber: /tmp/tp tidak dipakai; HTML dan JS ada di fa_tpdoc_src/."""
import re, sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
FA = ROOT / "out/faindonesia"
SRC = ROOT / "fa_tpdoc_src"
DRY = "--dry" in sys.argv
B = "https://faindonesia.co.id"
SLUG = "kalkulator-tp-doc"
URL = f"{B}/{SLUG}/"
TITLE = "Aplikasi TP Doc: Cek Kewajiban Transfer Pricing dan Draf Local File | FA Jupiter"
DESC = "Cek wajib Master File dan Local File menurut PMK 172/2023, uji kewajaran rentang interkuartil, dan draf Local File siap disunting dari data transaksi afiliasi."

tpl = (FA / "kalkulator-penyusutan-fiskal/index.html").read_text(encoding="utf-8")
t = tpl
def sub1(pat, rep, s):
    n = re.subn(pat, lambda m: rep, s, count=1, flags=re.S)
    assert n[1] == 1, pat
    return n[0]
t = sub1(r"<title>.*?</title>", f"<title>{TITLE}</title>", t)
t = sub1(r'<meta content="[^"]*" name="description"/>', f'<meta content="{DESC}" name="description"/>', t)
t = sub1(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{URL}" rel="canonical"/>', t)
t = sub1(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{TITLE}" property="og:title"/>', t)
t = sub1(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{DESC}" property="og:description"/>', t)
t = sub1(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{URL}" property="og:url"/>', t)

faq = [
 ("Siapa yang wajib menyusun Master File dan Local File?", "Wajib pajak yang melakukan transaksi afiliasi pada tahun berjalan dan memenuhi salah satu kriteria tahun pajak sebelumnya: peredaran bruto lebih dari Rp50 miliar, transaksi afiliasi barang berwujud lebih dari Rp20 miliar, atau jasa, bunga, harta tidak berwujud, dan transaksi lainnya masing-masing lebih dari Rp5 miliar, atau transaksi dengan afiliasi di negara bertarif PPh lebih rendah."),
 ("Kapan Local File harus tersedia?", "Paling lambat 4 bulan setelah akhir tahun pajak, yaitu 30 April untuk tahun buku Januari sampai Desember. Bila Direktur Jenderal Pajak meminta, dokumen disampaikan paling lama 1 bulan sejak permintaan."),
 ("Apakah draf ini langsung bisa dipakai?", "Draf menyusun kerangka dan angka dari data yang Anda isi. Analisis kesebandingan, set pembanding, dan dokumen pendukung perlu dilengkapi dan direview sebelum dipakai."),
]
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": ["WebApplication", "SoftwareApplication"], "@id": URL + "#app", "name": "FA Jupiter TP Doc", "url": URL, "description": DESC,
   "applicationCategory": "FinanceApplication", "operatingSystem": "Web (browser)", "inLanguage": "id",
   "publisher": {"@type": "Organization", "@id": B + "/#org", "name": "FA Indonesia", "url": B + "/"}},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
  {"@type": "BreadcrumbList", "itemListElement": [
     {"@type": "ListItem", "position": 1, "name": "FA Indonesia", "item": B + "/"},
     {"@type": "ListItem", "position": 2, "name": "FA Apps", "item": B + "/apps/"},
     {"@type": "ListItem", "position": 3, "name": "FA Jupiter", "item": B + "/apps/jupiter/"},
     {"@type": "ListItem", "position": 4, "name": "TP Doc", "item": URL}]}]}
t = sub1(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", t)

body = (SRC / "body.html").read_text(encoding="utf-8")
js = (SRC / "app.js").read_text(encoding="utf-8")
t = sub1(r"<main.*?</main>", body, t)
m = [x for x in re.finditer(r"<script>(?!window.dataLayer).*?</script>", t, flags=re.S) if "calc()" in x.group(0)]
assert len(m) == 1
t = t[:m[0].start()] + "<script>" + js + "</script>" + t[m[0].end():]
pay = ('<script>window.FA_PAY={app:"tp-doc",name:"Draf Local File TP Doc",what:"draf Local File (Word)",pay:{type:"qris",amount:25000},full:"[data-fa-full]"};</script>'
       '<script src="/js/fa-paywall.js" defer></script>')
k = t.rfind("</body>"); t = t[:k] + pay + t[k:]
t = t.replace("FA Venus · Kalkulator Penyusutan Fiskal &amp; Pajak Tangguhan", "FA Jupiter · TP Doc").replace("Kalkulator Penyusutan Fiskal & Pajak Tangguhan", "TP Doc: Cek Kewajiban dan Draf Local File")
t = t.replace("/img/og-page/kalkulator-penyusutan-fiskal.jpg", "/img/og-page/apps.jpg")
t = re.sub(r'(<p class="note">Lanjut: .*?</p>)', lambda m: m.group(1), t, flags=re.S)
assert "Pajak Tangguhan" not in t and "pajak tangguhan" not in t

out = FA / SLUG / "index.html"
cur = out.read_text(encoding="utf-8") if out.exists() else ""
print("halaman:", "berubah" if cur != t else "sudah sama")
changed = cur != t

sp = FA / "sitemap.xml"; S = sp.read_text(encoding="utf-8")
if URL not in S:
    S = S.replace("</urlset>", f"<url><loc>{URL}</loc><lastmod>2026-11-14</lastmod><priority>0.7</priority></url>\n</urlset>", 1); changed = True; print("sitemap +1")
    if not DRY: sp.write_text(S, encoding="utf-8")
lp = FA / "llms.txt"; L = lp.read_text(encoding="utf-8")
if URL not in L:
    L = L.rstrip("\n") + f"\n- FA Jupiter TP Doc: cek kewajiban Master File dan Local File (PMK 172/2023), uji kewajaran, draf Local File → {URL}\n"; print("llms +1")
    if not DRY: lp.write_text(L, encoding="utf-8")
if not DRY and cur != t:
    out.parent.mkdir(exist_ok=True); out.write_text(t, encoding="utf-8")

# kartu di grid /apps/ (setelah kartu Penyusutan Fiskal), idempoten
ap = FA / "apps/index.html"; A = ap.read_text(encoding="utf-8")
if 'href="/kalkulator-tp-doc/"' not in A.split('id="video"')[-1] and 'data-c="pajak"' in A:
    card = ('<a class="card" data-c="pajak" data-q="fa jupiter · tp doc cek kewajiban master file local file pmk 172 uji kewajaran draf local file transfer pricing. pajak" href="/kalkulator-tp-doc/">'
            '<b>FA Jupiter · TP Doc</b><p>Cek wajib Master File dan Local File, uji kewajaran rentang interkuartil, dan draf Local File dari transaksi afiliasi.</p>'
            '<div class="meta"><span class="badge">Live</span><span class="cat">Coba Gratis</span><span class="cat">Pajak</span><span class="src">FA Indonesia</span></div></a>')
    k = A.find('href="/kalkulator-penyusutan-fiskal/"><b>FA Venus')
    assert k > 0
    e = A.find("</a>", k) + 4
    A = A[:e] + card + A[e:]
    print("kartu /apps/ +1")
    if not DRY: ap.write_text(A, encoding="utf-8")
