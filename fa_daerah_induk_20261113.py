# -*- coding: utf-8 -*-
"""13 Nov 2026: halaman daerah FA ditata mengikuti halaman induk /jasa-audit-laporan-keuangan/,
langsung ke inti, TANPA membuat isinya mirip satu sama lain dan TANPA membuang SEO yang sudah ada.

Arahan Bos 13 Nov: "halaman daerah harusnya seperti halaman induk dengan tambahan SEO per daerah";
"Cek Izin gak perlu ada di halaman FA daerah, langsung to the point pakai blok biru dan orange untuk
Chat Ananta, CPA"; "intinya jaga masih gak mirip"; "jangan sampai kehilangan SEO yang sudah ada".

Bekerja di out/faindonesia (blok berpenanda, idempoten). Sumber kartu dan blok tim = halaman induk yang
sudah final di out/, jadi jalankan SETELAH fa_rendah_hati_20261112.py (aman diulang kapan saja).

Keluarga:
  A /jasa-audit-laporan-keuangan/<kota>/     B /wilayah/<kota>/
  C /wilayah/<kota>/kecamatan/<kec>/         D /wilayah/<kota>/<kawasan>/
Yang dilakukan:
  1. Dua kartu KAP DHN & Rekan (oranye) + KJA Farhani K.N. (biru), tombol Chat Ananta, CPA, tepat di bawah
     tombol hero (penanda fa-ik2). Menggantikan kotak kontak terlipat fa-lk2; kartu di atas footer dibuang
     supaya tidak dobel. Pesan WA memuat nama daerah.
  2. Blok "Tim Kami" tiga foto (Ananta, Farhani, Dwi) dari halaman induk.
  3. B: blok Cek Izin KAP, KJA, KJPP tidak lagi tampil di tengah halaman. Isinya (daftar kantor per kota,
     teks unik tiap kota, penting untuk kueri "kap <kota>") dipindah utuh ke akordeon tertutup di bawah
     blok data lokal (penanda fa-pkfold), butir Peta Isi-nya dibuang.
Tidak ada teks induk yang disalin ke halaman daerah (supaya antarhalaman tidak makin mirip).
Title, description, H1, JSON-LD, URL, dan seluruh isi lokal tidak diubah.
"""
import os, re, glob, html
from urllib.parse import quote

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "faindonesia")
PARENT = os.path.join(ROOT, "jasa-audit-laporan-keuangan", "index.html")

RX_TIM = re.compile(r"<!--fa-tim-atas-->.*?<!--/fa-tim-atas-->", re.S)
RX_LK2 = re.compile(r"<!--fa-lk2-->.*?<!--/fa-lk2-->", re.S)
RX_IK2 = re.compile(r"<!--fa-ik2-->.*?<!--/fa-ik2-->", re.S)
RX_IKD = re.compile(r"<!--fa-ikd-->.*?<!--/fa-ikd-->\n?", re.S)
RX_NAV = re.compile(r'<nav aria-label="Peta Isi" class="pf-map[^"]*" id="pfmap">.*?</nav>', re.S)
RX_PK = re.compile(r"<!--pk-->.*?<!--/pk-->", re.S)
RX_DHN2 = re.compile(r'<div class="dhn2"[^>]*>.*?</aside></div>', re.S)
RX_CBTNS = re.compile(r'<div class="cbtns"[^>]*>.*?</div>', re.S)
FOLD_CSS = ('<style id="pkfold-css">details.pkfold{margin:26px 0 8px;border-top:1px solid rgba(127,127,127,.28);'
            'border-bottom:1px solid rgba(127,127,127,.28)}details.pkfold>summary{cursor:pointer;list-style:none;'
            'padding:16px 34px 16px 0;font-weight:600;position:relative}details.pkfold>summary::-webkit-details-marker{display:none}'
            'details.pkfold>summary:after{content:"+";position:absolute;right:2px;top:50%;margin-top:-15px;font-size:24px;'
            'line-height:30px;font-weight:300;transition:transform .25s}details.pkfold[open]>summary:after{transform:rotate(45deg)}'
            'details.pkfold .pk{margin-top:4px}</style>')


def load_parent():
    t = open(PARENT, encoding="utf-8").read()
    tim = RX_TIM.search(t).group(0)
    assert "Tim Kami" in tim and tim.count("<img") == 3, "blok tim induk berubah"
    kartu = RX_DHN2.search(t).group(0)
    assert kartu.count("<aside") == 2 and kartu.count("Chat Ananta, CPA") == 2, "dua kartu induk berubah"
    css = "".join(re.search(r'<style id="%s">.*?</style>' % i, t, re.S).group(0) for i in ("dhn-css", "dhn2-css"))
    return tim, kartu, css


def place_name(t, fam):
    for rx in (r"<summary><b[^>]*>Kontak KJA Farhani dan KAP DHN &amp; Rekan di (.*?)</b></summary>",
               r'<div class="dhn2" data-n="([^"]*)"',
               r"<h2[^>]*>Persiapan Audit KAP di (.*?)</h2>"):
        m = re.search(rx, t)
        if m:
            return html.unescape(m.group(1)).strip()
    return None


def kartu_lokal(kartu, name):
    q = quote(name)
    k = kartu.replace("saya%20ingin%20tanya", "saya%20dari%20" + q + "%20ingin%20tanya")
    k = re.sub(r'<div class="dhn2"[^>]*>',
               '<div class="dhn2" data-n="%s" style="width:100%%;margin:24px 0 6px">' % html.escape(name, quote=True), k, count=1)
    return k


def pindah_cek_izin(t, name):
    """B: section.pk keluar dari tengah halaman, masuk akordeon tertutup setelah blok uq-lokal."""
    if "<!--fa-pkfold-->" in t:
        return t
    pk = RX_PK.search(t)
    if not pk:
        return t
    isi = pk.group(0)
    t = t[:pk.start()] + t[pk.end():]
    nav = RX_NAV.search(t)
    if nav:
        n0 = nav.group(0)
        n1, k = re.subn(r'<li><a href="#cek-izin-kap[^"]*">.*?</a></li>', "", n0, flags=re.S)
        if k:
            n1 = re.sub(r"Lihat Semua \((\d+)\)", lambda m: "Lihat Semua (%d)" % max(int(m.group(1)) - 1, 0), n1)
            t = t.replace(n0, n1, 1)
    fold = ('<!--fa-pkfold-->' + FOLD_CSS + '<details class="pkfold"><summary>Daftar KAP, KJA, dan KJPP Terdaftar di %s</summary>'
            % html.escape(name) + isi + '</details><!--/fa-pkfold-->')
    k = t.find("<!--/uq-lokal-->")
    if k >= 0:
        k += len("<!--/uq-lokal-->")
    else:
        k = t.find("<h2>Pertanyaan Umum</h2>")
        if k < 0:
            k = t.rfind("</main>")
    return t[:k] + fold + t[k:]


def do(path, fam, tim, kartu, css):
    t = open(path, encoding="utf-8").read()
    o = t
    name = place_name(t, fam)
    if not name:
        return "noname"
    # bersihkan hasil sebelumnya
    t = RX_IKD.sub("", t)
    if fam == "B":
        t = pindah_cek_izin(t, name)
    # kartu lama (atas footer / hasil lama) dibuang, kecuali yang ada di dalam blok fa-ik2
    ik2 = RX_IK2.search(t)
    if ik2:
        t = t[:ik2.start()] + "\x00IK2\x00" + t[ik2.end():]
    t = RX_DHN2.sub("", t)
    blok = "<!--fa-ik2-->" + ("" if "dhn2-css" in t else css) + kartu_lokal(kartu, name) + "<!--/fa-ik2-->"
    # 1. dua kartu di bawah tombol hero
    if "\x00IK2\x00" in t:
        t = t.replace("\x00IK2\x00", blok, 1)
    elif RX_LK2.search(t):
        t = RX_LK2.sub(lambda m: blok, t, count=1)
    else:
        cb = RX_CBTNS.search(t)
        if not cb:
            return "nohero"
        t = t[:cb.end()] + blok + t[cb.end():]
    # 2. blok tim tiga orang
    if RX_TIM.search(t):
        t = RX_TIM.sub(lambda m: tim, t, count=1)
    else:
        e = t.index("<!--/fa-ik2-->") + len("<!--/fa-ik2-->")
        t = t[:e] + "<!--fa-ikd-->" + tim + "<!--/fa-ikd-->\n" + t[e:]
    if t != o:
        open(path, "w", encoding="utf-8").write(t)
        return "ok"
    return "same"


def main():
    tim, kartu, css = load_parent()
    fams = {
        "A": glob.glob(os.path.join(ROOT, "jasa-audit-laporan-keuangan", "*", "index.html")),
        "B": glob.glob(os.path.join(ROOT, "wilayah", "*", "index.html")),
        "C": glob.glob(os.path.join(ROOT, "wilayah", "*", "kecamatan", "*", "index.html")),
        "D": [p for p in glob.glob(os.path.join(ROOT, "wilayah", "*", "*", "index.html")) if os.sep + "kecamatan" + os.sep not in p],
    }
    for fam in "ABCD":
        res = {}
        bad = []
        for p in sorted(fams[fam]):
            r = do(p, fam, tim, kartu, css)
            res[r] = res.get(r, 0) + 1
            if r not in ("ok", "same"):
                bad.append((r, os.path.relpath(p, ROOT)))
        print(fam, len(fams[fam]), res)
        for b in bad[:10]:
            print("   ", b)


if __name__ == "__main__":
    main()
