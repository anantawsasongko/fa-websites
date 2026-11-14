#!/usr/bin/env python3
"""Hero produk + screenshot app asli di tiga hub FA Apps dan screenshot asli di /apps/ (14 Nov 2026).

Bos: "tambahin screenshot app asli", "hub app", "SEO".
- /apps/saturn/, /apps/jupiter/, /apps/venus/: hero ala SaaS (H1 berkata kunci, tombol, deret fakta, screenshot asli),
  FAQ 3 butir + JSON-LD FAQPage dan SoftwareApplication, title/description/og ditulis ulang. H1 lama jadi H2 (teks tetap).
- /apps/: mockup dummy di hero diganti galeri tab screenshot asli (Jupiter, Saturn, Venus, Galaxy).
Data SEO (GSC 90 hari s.d. 10 Nov): query "aplikasi" hanya 5 impresi; yang nyata kalkulator penyusutan fiskal (3 klik, 17 impresi),
kalkulator penyusutan 28, PPh 23 dan gross up. Karena itu hub Jupiter memuat kata penyusutan dan PPh di title dan FAQ.
Gambar: out/faindonesia/img/apps/fa-<app>-app.webp (screenshot app dengan data contoh, tanpa data klien).
Urutan bila build ulang: setelah fa_apps_saas_20261114.py, sebelum teks_rapi_20261113.py. Idempoten, --dry.
"""
import os, re, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fa_apps_saas_20261114 as S

ROOT = S.ROOT
DRY = "--dry" in sys.argv
B = S.B
esc = S.esc

HUBS = {
    "saturn": dict(
        n="FA Saturn", c="#4f8cff", alt="Tampilan dashboard FA Saturn: alur engagement audit, materialitas, rekap asersi, dan kesiapan LAI dengan klien dummy",
        h1="FA Saturn: Aplikasi Audit untuk KAP, dari Planning sampai Sign-off",
        sub="Satu tempat untuk seluruh siklus audit KAP: planning, penilaian risiko, respons risiko, dan pelaporan. Tingkat risiko berwarna dan setiap kesimpulan punya jejak ke kertas kerjanya.",
        cta=("Coba Demo FA Saturn", "/saturn/"),
        facts=[("4", "Tahap Audit"), ("5", "Tingkat Sign-off"), ("SA", "Standar Audit IAPI")],
        title="FA Saturn: Aplikasi Audit KAP, Kertas Kerja dan Sign-off",
        desc="Aplikasi audit untuk KAP: planning, penilaian risiko berwarna, kertas kerja Excel, dan sign-off berjenjang. Coba demo gratis dengan data dummy.",
        faq=[("Apa itu FA Saturn?", "FA Saturn adalah aplikasi web untuk menjalankan audit di KAP: perencanaan, penilaian risiko, respons risiko, sampai pelaporan, lengkap dengan kertas kerja, review note, dan sign-off berjenjang. Alur kerjanya mengikuti Standar Audit (SA) IAPI yang merujuk ISA."),
             ("Apakah FA Saturn bisa dicoba?", "Bisa. Tersedia demo dengan klien dummy, sehingga Anda dapat melihat seluruh alur dari planning sampai tanda tangan laporan auditor tanpa memasukkan data sendiri."),
             ("Apakah FA Saturn menggantikan penilaian auditor?", "Tidak. Aplikasi merapikan alur, kertas kerja, dan jejak review. Pertimbangan profesional dan opini audit tetap menjadi tanggung jawab KAP.")]),
    "jupiter": dict(
        n="FA Jupiter", c="#f2994a", alt="Tampilan ringkasan FA Jupiter: status kontrol tied up, total aset, pendapatan, dan laba neto dengan data dummy",
        h1="FA Jupiter: Aplikasi Laporan Keuangan Siap Audit, Penyusutan, dan PPh",
        sub="Dari buku besar jadi laporan keuangan PSAK atau SAK EMKM dengan lead schedule dan checklist PBC. Kalkulator penyusutan fiskal, PPh 21, PPh Badan, dan PPh 23 membantu menutup angka akhir tahun.",
        cta=("Buka FA Jupiter", "/audit-ready/"),
        facts=[("4", "Kalkulator Pajak"), ("PSAK", "dan SAK EMKM"), ("Excel", "Upload dan Download")],
        title="FA Jupiter: Laporan Keuangan Siap Audit, Penyusutan dan PPh",
        desc="Susun laporan keuangan PSAK atau SAK EMKM sampai siap audit, plus kalkulator penyusutan fiskal, PPh 21, PPh Badan, dan PPh 23. Coba gratis.",
        faq=[("Apa itu FA Jupiter?", "FA Jupiter adalah aplikasi web untuk menyusun laporan keuangan dari COA dan buku besar sampai siap diaudit, atau merapikan laporan keuangan yang berantakan menjadi paket yang diminta auditor."),
             ("Kalkulator pajak apa saja yang ada di FA Jupiter?", "Penyusutan fiskal dan pajak tangguhan, PPh 21 dengan tarif efektif rata-rata (TER), PPh Badan dan tarif final UMKM, serta pemotongan atau pemungutan PPh (termasuk PPh 23) dan PPN."),
             ("Laporan keuangan mengikuti standar apa?", "Penyajian mengikuti PSAK dan SAK EMKM, dilengkapi kontrol tied up, jurnal penyesuaian, trial balance, lead schedule, dan CALK.")]),
    "venus": dict(
        n="FA Venus", c="#e86fb0", alt="Tampilan kalkulator valuasi rumah sakit FA Venus: estimasi harga before dan after dengan input profil dan keuangan rumah sakit",
        h1="FA Venus: Aplikasi Valuasi, Kredit, dan Keputusan Keuangan",
        sub="Seberapa bernilai usaha, seberapa besar kredit yang masuk akal, dan di mana rumah sakit kehilangan margin. Isi angka usaha Anda, hasil langsung keluar di browser.",
        cta=("Lihat Semua Alat FA Venus", "#alat"),
        facts=[("15", "Alat di FA Venus"), ("DCF", "WACC, DSCR, Kredit"), ("RS", "Toolkit Rumah Sakit")],
        title="FA Venus: Aplikasi Valuasi, Kredit, DSCR, dan Toolkit RS",
        desc="Hitung valuasi usaha dan rumah sakit, kapasitas kredit, DSCR, dan unit cost ABC. Isi angka, hasil langsung keluar di browser. Coba gratis.",
        faq=[("Apa itu FA Venus?", "FA Venus adalah kumpulan alat bantu keputusan manajemen: valuasi usaha dan rumah sakit, DCF dan WACC, kapasitas kredit, DSCR, bankability, kesiapan pendanaan, dan toolkit rumah sakit."),
             ("Apakah hasil valuasi dan kapasitas kredit sudah pasti?", "Tidak. Hasilnya estimasi dari angka yang Anda masukkan, berguna untuk gambaran awal. Keputusan pendanaan atau transaksi tetap perlu ditinjau oleh profesional dan pihak pemberi dana."),
             ("Alat apa saja untuk rumah sakit?", "Valuasi rumah sakit before dan after, unit cost berbasis ABC, analisis ABC-VEN obat, cek koding INA-CBG, dan AI Analis Keuangan RS.")]),
}

CSS2 = """<style id="sx-hub-css">.sx-shot{display:block;position:relative}.sx-shot img{display:block;width:100%;height:auto;background:#121212}
.sx-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}.sx-tabs button{appearance:none;border:1px solid var(--line);background:rgba(127,127,127,.08);color:var(--muted);padding:7px 14px;border-radius:999px;font:600 12.5px var(--f-ui,sans-serif);cursor:pointer}
.sx-tabs button[aria-selected=true]{background:#fff;color:#111;border-color:#fff}.sx-pane[hidden]{display:none}
.sx-hubhero .sx-win{margin:0}.sx-cap{margin:8px 14px 12px;font-size:10.5px;color:var(--muted)}</style>"""


def facts_html(f):
    return "".join("<li><b>%s</b>%s</li>" % (esc(a), esc(b)) for a, b in f)


NOIR_CSS = re.search(r'CSS = """(<style id="fh-css">.*?</style>)"""', open(os.path.join(ROOT, "fa_hero_noir_20261114.py"), encoding="utf-8").read(), re.S).group(1)
FOLD_CSS = """<style id="fh-fold-css">.fh-fold{margin:0 0 26px;border-top:1px solid #2F2F2F;border-bottom:1px solid #2F2F2F}.fh-fold summary{cursor:pointer;list-style:none;padding:13px 0;font-size:12px;font-weight:400;letter-spacing:.2em;text-transform:uppercase;color:#C4CBDA}.fh-fold summary::-webkit-details-marker{display:none}.fh-fold summary:after{content:"+";float:right;color:#00AAD6;font-size:16px;line-height:1}.fh-fold[open] summary:after{content:"\\2212"}.fh-fold ul{margin:0 0 6px!important}.fh-fold li:first-child{border-top:0}.fh-fold p{margin:0 0 14px;font-size:14.5px;line-height:1.6;font-weight:300;color:#C4CBDA}.fh-1c .fh-in{grid-template-columns:minmax(0,760px);padding:60px 48px}.fh-shots{margin:0 0 44px}.fh-shots h2{margin:0 0 6px}.fh-shots>p{margin:0 0 16px;color:var(--muted)}</style>"""


def hub_hero(k, a):
    facts = "".join("<li><i>%02d</i><span><b>%s</b> %s</span></li>" % (i, esc(x), esc(y)) for i, (x, y) in enumerate(a["facts"], 1))
    body = (
        '<section class="fh fh-1c" aria-label="%s"><svg class="gr" aria-hidden="true"><filter id="fhg"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
        '<feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0"/></filter><rect width="100%%" height="100%%" filter="url(#fhg)"/></svg>'
        '<div class="fh-in"><div><p class="fh-eb">FA Apps / %s</p><h1>%s</h1>'
        '<details class="fh-fold"><summary>Selengkapnya</summary><p>%s</p><ul>%s</ul></details>'
        '<div class="fh-cta"><a class="p" href="%s">%s</a><a class="w" href="%s" rel="noopener" target="_blank">Chat via WhatsApp</a></div></div></div></section>'
        '<section class="fh-shots" aria-label="Tampilan aplikasi"><p class="kick">Tampilan</p><h2>%s dalam Tampilan Nyata</h2><p>Data contoh, bukan data klien.</p>'
        '<div class="sx-win sx-shot"><div class="sx-bar"><i></i><i></i><i></i><span>%s</span></div><img src="/img/apps/fa-%s-app.webp" width="1100" height="%d" alt="%s" loading="lazy" decoding="async"></div></section>') % (
        esc(a["n"]), esc(a["n"]), esc(a["h1"]), esc(a["sub"]), facts, a["cta"][1], esc(a["cta"][0]), S.WA,
        esc(a["n"]), esc(a["n"]), k, 653 if k in ("saturn", "venus") else 627, esc(a["alt"]))
    return '<!--fa-saas-hub-->' + S.CSS1 + CSS2 + NOIR_CSS + FOLD_CSS + body + '<!--/fa-saas-hub-->'


def hub_tail(k, a):
    faq = "".join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else "", esc(q), esc(t)) for i, (q, t) in enumerate(a["faq"]))
    ld1 = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in a["faq"]]}, ensure_ascii=False)
    ld2 = json.dumps({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": a["n"], "url": B + "/apps/%s/" % k,
                      "applicationCategory": "BusinessApplication", "operatingSystem": "Web", "description": a["desc"], "inLanguage": "id",
                      "image": B + "/img/apps/fa-%s-app.webp" % k, "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": B + "/"}}, ensure_ascii=False)
    return ('<!--fa-saas-hub2--><section class="sx-sec sx-faq" id="faq-app" aria-label="Pertanyaan umum"><p class="kick">FAQ</p><h2>Pertanyaan tentang %s</h2>%s</section>'
            '<script type="application/ld+json">%s</script><script type="application/ld+json">%s</script><!--/fa-saas-hub2-->') % (esc(a["n"]), faq, ld1, ld2)


def set_meta(h, title, desc):
    assert len(title) <= 65 and len(desc) <= 158, (title, len(title), len(desc))
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % esc(title), h, count=1, flags=re.S)
    for pat in (r'(<meta[^>]*?(?:name|property)="(?:og:title|twitter:title)"[^>]*?content=")[^"]*(")',
                r'(<meta[^>]*?content=")[^"]*("[^>]*?(?:name|property)="(?:og:title|twitter:title)")'):
        h = re.sub(pat, lambda m: m.group(1) + esc(title) + m.group(2), h)
    for pat in (r'(<meta[^>]*?(?:name|property)="(?:description|og:description|twitter:description)"[^>]*?content=")[^"]*(")',
                r'(<meta[^>]*?content=")[^"]*("[^>]*?(?:name|property)="(?:description|og:description|twitter:description)")'):
        h = re.sub(pat, lambda m: m.group(1) + esc(desc) + m.group(2), h)
    return h


def do_hub(k, a):
    p = os.path.join(ROOT, "out", "faindonesia", "apps", k, "index.html")
    h = open(p, encoding="utf-8").read()
    h = re.sub(r'<!--fa-saas-hub-->.*?<!--/fa-saas-hub-->', '', h, flags=re.S)
    h = re.sub(r'<!--fa-saas-hub2-->.*?<!--/fa-saas-hub2-->', '', h, flags=re.S)
    # H1 lama jadi H2 (hanya yang di luar hero)
    m = re.search(r'<h1([^>]*)>(.*?)</h1>', h, re.S)
    if m:
        h = h.replace(m.group(0), '<h2%s>%s</h2>' % (m.group(1), m.group(2)), 1)
    key = '<section class="sec fa4'
    assert key in h, k + ": penanda section fa4 tidak ada"
    h = h.replace(key, hub_hero(k, a) + key, 1)
    ck = '<!--dhn-->'
    assert ck in h, k + ": penanda dhn tidak ada"
    h = h.replace(ck, hub_tail(k, a) + ck, 1)
    h = set_meta(h, a["title"], a["desc"])
    if not DRY:
        open(p, "w", encoding="utf-8").write(h)
    print(k, "OK" if not DRY else "DRY", len(h), len(a["title"]), len(a["desc"]), h.count("<h1"))


# ---- /apps/: mockup dummy -> galeri screenshot asli
TABS = [("jupiter", "FA Jupiter", 627), ("saturn", "FA Saturn", 653), ("venus", "FA Venus", 653), ("galaxy", "FA Galaxy", 627)]
ALT = {"jupiter": HUBS["jupiter"]["alt"], "saturn": HUBS["saturn"]["alt"], "venus": HUBS["venus"]["alt"],
       "galaxy": "Tampilan FA Galaxy Konversi PL PSAK 118: laba usaha versi lama, laba usaha PSAK 118, dan subtotal wajib baru dengan data contoh"}


def shot_block():
    tabs = "".join('<button type="button" role="tab" aria-selected="%s" data-t="%s">%s</button>' % ("true" if i == 0 else "false", k, n) for i, (k, n, _) in enumerate(TABS))
    panes = "".join('<div class="sx-pane" role="tabpanel" data-p="%s"%s><img src="/img/apps/fa-%s-app.webp" width="1100" height="%d" alt="%s" decoding="async"%s></div>' % (
        k, "" if i == 0 else " hidden", k, hh, esc(ALT[k]), "" if i == 0 else ' loading="lazy"') for i, (k, n, hh) in enumerate(TABS))
    js = ("<script>(function(){var r=document.currentScript.parentNode;r.addEventListener('click',function(e){var b=e.target.closest('button[data-t]');if(!b)return;"
          "r.querySelectorAll('button[data-t]').forEach(function(x){x.setAttribute('aria-selected',x===b?'true':'false')});"
          "r.querySelectorAll('.sx-pane').forEach(function(p){p.hidden=p.getAttribute('data-p')!==b.getAttribute('data-t')})})})();</script>")
    return ('<!--fa-saas-shot--><div class="sx-shotbox"><div class="sx-tabs" role="tablist">%s</div>'
            '<div class="sx-win sx-shot"><div class="sx-bar"><i></i><i></i><i></i><span>FA Apps</span></div>%s</div>'
            '<p class="sx-cap">Tampilan aplikasi dengan data contoh.</p>%s</div><!--/fa-saas-shot-->') % (tabs, panes, js)


def do_apps():
    p = os.path.join(ROOT, "out", "faindonesia", "apps", "index.html")
    h = open(p, encoding="utf-8").read()
    h = re.sub(r'<!--fa-saas-shot-->.*?<!--/fa-saas-shot-->', '', h, flags=re.S)
    if "sx-hub-css" not in h:
        h = h.replace('<!--/fa-saas-->', CSS2 + '<!--/fa-saas-->', 1)
    # hero noir tetap (minim tulisan): poin dilipat, galeri screenshot asli di bawah hero. Jalankan SETELAH fa_hero_noir_20261114.py
    h = re.sub(r'<!--fa-saas-shot-->.*?<!--/fa-saas-shot-->', '', h, flags=re.S)
    h = re.sub(r'<section class="fh-shots".*?</section>', '', h, flags=re.S)
    if "fh-fold-css" not in h:
        h = h.replace('<!--/fa-hero-noir-->', FOLD_CSS + '<!--/fa-hero-noir-->', 1)
    if '<details class="fh-fold">' not in h:
        h = h.replace('<ul><li><i>01</i>', '<details class="fh-fold"><summary>Keunggulan</summary><ul><li><i>01</i>', 1)
        h = h.replace('</li></ul><div class="fh-cta">', '</li></ul></details><div class="fh-cta">', 1)
    sec = '<section class="fh-shots" aria-label="Tampilan aplikasi"><p class="kick">Tampilan</p><h2>FA Apps dalam Tampilan Nyata</h2><p>Data contoh, bukan data klien.</p>' + shot_block() + '</section>'
    h = h.replace('<!--/fa-hero-noir-->', '<!--/fa-hero-noir-->' + sec, 1) if False else h.replace('<!--/fa-saas-->', '<!--/fa-saas-->' + sec, 1)
    if not DRY:
        open(p, "w", encoding="utf-8").write(h)
    print("apps", "OK" if not DRY else "DRY", len(h), "galeri", h.count("fa-saas-shot-->"))


if __name__ == "__main__":
    for k, a in HUBS.items():
        do_hub(k, a)
    do_apps()
