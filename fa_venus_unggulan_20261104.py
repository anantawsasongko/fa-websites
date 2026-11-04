# -*- coding: utf-8 -*-
"""4 Nov 2026 malam (permintaan Bos): Kalkulator Valuasi Rumah Sakit jadi aplikasi unggulan FA Venus.
- /apps/: ringkasan FA Venus diawali Valuasi Rumah Sakit, kotak "Unggulan FA Venus" di atas daftar, kartu RS pindah ke depan + badge Unggulan.
- /galaxy/: seksi #venus diganti panduan Valuasi Rumah Sakit; Konversi PSAK 118 pindah ke #venus-psak118.
- /toko/: tag "Unggulan FA Venus", kartu dipindah ke urutan pertama aplikasi.
- Halaman kalkulator: eyebrow "Unggulan FA Venus". Homepage hs42, /layanan/, llms.txt.
Idempoten (marker). Jalankan setelah fa_rsval_20261104.py dan fa_kw_20261104.py."""
import os, re
R = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(R, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
U = "/kalkulator-valuasi-rumah-sakit/"
def rw(rel, fn):
    p = os.path.join(B, rel)
    if not os.path.exists(p): print("skip", rel); return
    t = open(p, encoding="utf-8").read(); n = fn(t)
    if n != t: open(p, "w", encoding="utf-8").write(n); print("patch", rel)
    else: print("tetap", rel)

FEAT = ('<!--fa-venus-top--><section class="sec" id="venus-unggulan"><div class="vu">'
        '<div class="cta vu-a"><h3>Unggulan FA Venus</h3><h2>Valuasi Rumah Sakit: Harga Jual Before dan After</h2>'
        '<p class="lead">Untuk pemilik RS, RSIA, dan RS khusus yang ingin menjual atau mencari investor. Hitung harga apa adanya, lalu harga setelah dibenahi: kerja sama BPJS, unit cost, okupansi, audit, dan data room.</p>'
        '<ul><li>EBITDA x multiple 5 sampai 8x, disesuaikan kelas, akreditasi, BPJS, BOR, dan status gedung</li>'
        '<li>Nilai aset dari appraisal KJPP atau benchmark per tempat tidur sebagai batas bawah</li>'
        '<li>Dikurangi utang bank, dikali porsi saham yang dijual, plus checklist data untuk calon pembeli</li></ul>'
        f'<div class="vu-b"><a class="btn solid" href="{U}">Buka Valuasi Rumah Sakit</a><a class="btn" href="/rumah-sakit-dijual/">RS Dijual</a><a class="btn" href="/konsultan-rumah-sakit/">Konsultan RS</a></div></div>'
        '<div class="meta vu-k"><b>Rp49 rb</b><span>bayar QRIS di aplikasi</span><b>4 langkah</b><span>profil, keuangan, aset dan utang, treatment</span><b>Laporan</b><span>siap dibawa ke calon pembeli</span></div>'
        '</div></section>'
        '<style>.vu{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,.7fr);gap:22px;border:1px solid #fff;border-radius:12px;padding:26px;background:var(--panel)}'
        '.vu ul{margin:12px 0 18px;padding-left:18px;color:var(--muted);font-size:14.5px}.vu-b{display:flex;gap:10px;flex-wrap:wrap}'
        '.vu .vu-k{display:grid;grid-template-columns:auto 1fr;gap:6px 12px;align-content:start;border-left:1px solid var(--line);padding-left:20px}'
        '.vu-k b{font-family:var(--f-display);font-weight:400;font-size:22px}.vu-k span{font-size:12.5px;color:var(--muted);align-self:center}'
        '.badge.top{background:#fff;color:#000}@media(max-width:760px){.vu{grid-template-columns:1fr;padding:20px}.vu-k{border-left:0;border-top:1px solid var(--line);padding:14px 0 0}}</style><!--/fa-venus-top-->')

def apps(t):
    t = re.sub(r"<!--fa-venus-top-->.*?<!--/fa-venus-top-->", "", t, flags=re.S)
    t = t.replace("<span>Kalkulator pajak, kredit, valuasi, PSAK</span>", "<span>Unggulan: Valuasi Rumah Sakit. Plus kalkulator pajak, kredit, valuasi, PSAK</span>")
    t = t.replace("kalkulator FA Venus (PPh 21 TER", "kalkulator FA Venus (unggulan Valuasi Rumah Sakit, PPh 21 TER")
    k = t.find('<section class="sec">', t.find("FA Galaxy</b>"))
    if k > 0: t = t[:k] + FEAT + t[k:]
    m = re.search(r'<a class="card" data-c="dana" data-q="fa venus · valuasi rumah sakit.*?</a>', t, re.S)
    if m:
        card = m.group(0)
        if 'badge top' not in card: card = card.replace('<span class="badge">Live</span>', '<span class="badge top">Unggulan</span><span class="badge">Live</span>', 1)
        t = t[:m.start()] + t[m.end():]
        f = t.find('<a class="card" data-c=', t.find("venus-unggulan"))
        t = t[:f] + card + t[f:]
    return t
rw("apps/index.html", apps)

GX = ('<article class="gx-sec" id="venus"><div class="id"><p class="kick eyebrow">Unggulan FA Venus</p><h2>FA Venus · Valuasi Rumah Sakit</h2></div><div class="body">'
      '<p class="intro">Banyak RS dijual lama tidak laku karena harga dipatok dari nilai gedung, sementara pembeli menghitung dari EBITDA, status BPJS, dan utang bank. Kalkulator ini menunjukkan harga apa adanya dan harga setelah RS dibenahi.</p>'
      '<ol class="steps"><li><div><h3>Isi Profil Rumah Sakit</h3><p>Jenis RS, kelas, akreditasi, jumlah tempat tidur, BOR, dan status kerja sama BPJS.</p></div></li>'
      '<li><div><h3>Isi Keuangan Setahun Terakhir</h3><p>Pendapatan, EBITDA, dan porsi pasien BPJS. Angka dari laporan internal cukup untuk estimasi awal.</p></div></li>'
      '<li><div><h3>Isi Aset, Utang, dan Saham</h3><p>Nilai appraisal bila ada, sisa utang bank, dan persentase saham yang akan dijual.</p></div></li>'
      '<li><div><h3>Pilih Treatment Sebelum Dijual</h3><p>Lihat dampak pembenahan BPJS, unit cost, okupansi, audit KAP, dan data room ke harga, lalu unduh laporannya.</p></div></li></ol>'
      f'<a class="btn solid" href="{U}" style="justify-self:start">Buka Valuasi Rumah Sakit</a></div></article>\n')
def galaxy(t):
    t = re.sub(r'<article class="gx-sec" id="venus"><div class="id"><p class="kick eyebrow">Unggulan FA Venus</p>.*?</article>\n', "", t, flags=re.S)
    t = t.replace('<article class="gx-sec" id="venus">', '<article class="gx-sec" id="venus-psak118">', 1)
    k = t.find('<article class="gx-sec" id="venus-psak118">')
    if k > 0: t = t[:k] + GX + t[k:]
    t = re.sub(r"<title>FA Galaxy: Panduan FA Jupiter · Laporan Keuangan - Audit Ready, FA Saturn &amp; FA Venus · Konversi PL PSAK 118",
               "<title>FA Galaxy: Panduan FA Jupiter, FA Saturn &amp; FA Venus · Valuasi Rumah Sakit", t, count=1)
    return t
rw("galaxy/index.html", galaxy)

def toko(t):
    m = re.search(r'<article class="it" data-cat="app" data-for="ca" id="p-venus-rsval">.*?</article>', t, re.S)
    if not m: return t
    art = m.group(0).replace('<span class="tg">Aplikasi · Rumah Sakit</span>', '<span class="tg">Unggulan FA Venus · Rumah Sakit</span>')
    t = t[:m.start()] + t[m.end():]
    f = t.find('<article class="it" data-cat="app"')
    return t[:f] + art + t[f:] if f > 0 else t[:m.start()] + art + t[m.start():]
rw("toko/index.html", toko)

rw("kalkulator-valuasi-rumah-sakit/index.html", lambda t: t.replace('<p class="eyebrow">FA Venus · Valuasi Rumah Sakit</p>', '<p class="eyebrow">Unggulan FA Venus · Valuasi Rumah Sakit</p>'))
rw("index.html", lambda t: t.replace('"hs42": "FA Jupiter, FA Saturn, FA Venus"', '"hs42": "FA Jupiter, FA Saturn, FA Venus Valuasi Rumah Sakit"')
                           .replace('"hs42": "FA Jupiter、FA Saturn、FA Venus"', '"hs42": "FA Jupiter、FA Saturn、FA Venus 医院估值"'))

def layanan(t):
    t = re.sub(r"<!--fa-venus-lay-->.*?<!--/fa-venus-lay-->", "", t, flags=re.S)
    a = '<a class="btn line" href="/konsultan-unit-cost-rumah-sakit/">Unit Cost Rumah Sakit</a>'
    return t.replace(a, a + f'<!--fa-venus-lay--><a class="btn line" href="{U}">Valuasi RS (FA Venus)</a><!--/fa-venus-lay-->', 1)
rw("layanan/index.html", layanan)

def llms(t):
    line = f"- Aplikasi unggulan FA Venus: Valuasi Rumah Sakit (harga jual RS before dan after) → https://faindonesia.co.id{U}\n"
    t = t.replace(line, "")
    return t.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + line, 1) if "\n## Layanan Spesifik\n" in t else t.rstrip("\n") + "\n" + line
rw("llms.txt", llms)
