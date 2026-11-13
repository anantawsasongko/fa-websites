# -*- coding: utf-8 -*-
"""13 Nov 2026: halaman daerah mengikuti halaman induk /jasa-audit-laporan-keuangan/.
Bos: "per daerah sampai desa, kecamatan, kota, harusnya halamannya persis ini dengan tambahan SEO per daerah".

Bekerja di out/faindonesia (pola blok berpenanda, idempoten). Sumber isi = halaman induk yang sudah final
di out/, jadi jalankan SETELAH fa_rendah_hati_20261112.py (aman dijalankan ulang kapan saja).

Keluarga yang disentuh:
  A /jasa-audit-laporan-keuangan/<kota>/        (blok tim sudah tiga orang)
  B /wilayah/<kota>/                            (tim satu kartu -> tiga orang)
  C /wilayah/<kota>/kecamatan/<kec>/            (tim satu kartu -> tiga orang)
  D /wilayah/<kota>/<kawasan>/                  (belum ada kotak kontak dan tim -> ditambah)
Yang dipasang: blok Tim Kami induk (tiga foto), lalu inti halaman induk (Kapan Butuh Audit, Audit Hemat,
Alur Kerja, KAP yang Mengaudit, Industri, Data Awal, Bacaan Terkait) dengan judul bernama daerah,
tepat setelah Peta Isi dan sebelum isi lokal. Title, description, H1, JSON-LD, dan isi lokal tidak diubah.
Keluarga B juga: blok Cek Izin KAP, KJA, KJPP dibuang; dua kartu KAP DHN + KJA Farhani (Chat Ananta, CPA)
dipindah dari atas footer ke bawah judul "Siapa yang Mengerjakan di <kota>".
"""
import os, re, glob, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "faindonesia")
PARENT = os.path.join(ROOT, "jasa-audit-laporan-keuangan", "index.html")

RX_TIM = re.compile(r"<!--fa-tim-atas-->.*?<!--/fa-tim-atas-->", re.S)
RX_LK2 = re.compile(r"<!--fa-lk2-->.*?<!--/fa-lk2-->", re.S)
RX_IND = re.compile(r"<!--fa-induk-->.*?<!--/fa-induk-->", re.S)
RX_NAV = re.compile(r'<nav aria-label="Peta Isi" class="pf-map[^"]*" id="pfmap">.*?</nav>', re.S)
RX_LI_IK = re.compile(r'<li data-ik="1">.*?</li>', re.S)
RX_BTN = re.compile(r'<button aria-expanded="false" class="pf-more" data-for="pfmap"[^>]*>[^<]*</button>')
LK2D_CSS = ('<style id="lk2d-css">.lk2>summary{list-style:none;cursor:pointer;position:relative;padding-right:34px;line-height:1.4}'
            '.lk2>summary::-webkit-details-marker{display:none}'
            '.lk2>summary:after{content:"+";position:absolute;right:2px;top:50%;margin-top:-15px;font-size:24px;line-height:30px;font-weight:300;transition:transform .25s}'
            '.lk2[open]>summary:after{transform:rotate(45deg)}</style>')


RX_PK = re.compile(r"<!--pk-->.*?<!--/pk-->", re.S)
RX_DHN2 = re.compile(r'<!--dhn-->(<div class="dhn2">.*?</aside></div>)<!--/dhn-->', re.S)
RX_SIAPA = re.compile(r'<h2 id="siapa-yang-mengerjakan-di-[^"]*">.*?</h2>', re.S)


def buang_cek_izin(t):
    """Keluarga B: blok Cek Izin KAP/KJA/KJPP (daftar kantor lain) dibuang, diganti dua kartu
    KAP DHN (oranye) dan KJA Farhani (biru) bertombol Chat Ananta, CPA. Bos 13 Nov 2026."""
    pk = RX_PK.search(t)
    if pk:
        pos = pk.start()
        t = t[:pos] + t[pk.end():]
        nav = RX_NAV.search(t)
        if nav:
            n0 = nav.group(0)
            n1, k = re.subn(r'<li(?: data-ik="1")?><a href="#cek-izin-kap[^"]*">.*?</a></li>', "", n0, flags=re.S)
            def dec(m):
                return "%s%d%s" % (m.group(1), max(int(m.group(2)) - 1, 0), m.group(3))
            if 'data-ik0="' in n1:
                n1 = re.sub(r'(data-ik0=")(\d+)(")', dec, n1, count=1)
            else:
                n1 = re.sub(r'(Lihat Semua \()(\d+)(\))', dec, n1)
            t = t.replace(n0, n1, 1)
        t = re.sub(r'<style id="pk-css">.*?</style>', "", t, count=1, flags=re.S)
        t = re.sub(r'<script defer(?:="")? src="/js/izin\.js"></script>', "", t, count=1)
    if "<!--fa-ikpk-->" not in t:
        d = RX_DHN2.search(t)
        h = RX_SIAPA.search(t)
        if d and h and h.end() < d.start():
            kartu = d.group(1).replace('<div class="dhn2">', '<div class="dhn2" style="width:100%;margin:22px 0 26px">', 1)
            t = t[:d.start()] + "<!--dhn--><!--/dhn-->" + t[d.end():]
            t = t[:h.end()] + "<!--fa-ikpk-->" + kartu + "<!--/fa-ikpk-->" + t[h.end():]
    return t


def load_parent():
    t = open(PARENT, encoding="utf-8").read()
    tim = RX_TIM.search(t).group(0)
    lk2 = RX_LK2.search(t).group(0)
    a = t.index('<h2 id="kapan-perusahaan-butuh-audit">')
    b = t.index("<!--fanas-hub-->")
    core = t[a:b].strip()
    assert "Tim Kami" in tim and tim.count("<img") == 3, "blok tim induk berubah"
    assert core.count("<h2") == 7, "inti halaman induk berubah (%d h2)" % core.count("<h2")
    return tim, lk2, core


def localize(core, name, ids_on_page):
    c = core
    c = c.replace(">Kapan Perusahaan Butuh Audit</h2>", ">Kapan Perusahaan di %s Butuh Audit</h2>" % name)
    c = c.replace(">Alur Kerja</h2>", ">Alur Kerja Audit di %s</h2>" % name)
    c = c.replace("<h2>Bacaan Terkait</h2>", "<h2>Bacaan Terkait Audit</h2>")
    toc = []
    def fix(m):
        i = m.group(1)
        if i in ids_on_page:
            i = i + "-audit"
        toc.append((i, re.sub(r"<[^>]+>", "", m.group(2))))
        return '<h2 id="%s">%s</h2>' % (i, m.group(2))
    c = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', fix, c)
    return c, toc


def place_name(t, fam):
    m = re.search(r"<summary><b[^>]*>Kontak KJA Farhani dan KAP DHN &amp; Rekan di (.*?)</b></summary>", t)
    if m:
        return m.group(1).strip()
    if fam == "D":
        m = re.search(r"<h2[^>]*>Persiapan Audit KAP di (.*?)</h2>", t)
        if m:
            return m.group(1).strip()
    return None


def do(path, fam, tim, lk2, core):
    t = open(path, encoding="utf-8").read()
    o = t
    # bersihkan hasil lama (idempoten)
    t = RX_IND.sub("", t)
    nav = RX_NAV.search(t)
    if not nav:
        return "nonav"
    n0 = nav.group(0)
    n1 = RX_LI_IK.sub("", n0)
    if 'data-ikb="1"' in n1:
        n1 = re.sub(r'<button aria-expanded="false" class="pf-more" data-for="pfmap" data-ikb="1"[^>]*>[^<]*</button>', "", n1)
        n1 = n1.replace('class="pf-map many"', 'class="pf-map"', 1)
    t = t.replace(n0, n1, 1)
    if fam == "D":
        t = re.sub(r"<!--fa-ikd-->.*?<!--/fa-ikd-->\n?", "", t, flags=re.S)

    name = place_name(t, fam)
    if not name:
        return "noname"
    if fam == "B":
        t = buang_cek_izin(t)

    # 1. blok tim tiga orang
    if RX_TIM.search(t):
        t = RX_TIM.sub(lambda m: tim, t, count=1)
    elif fam == "D":
        box = lk2.replace("Kontak KJA Farhani dan KAP DHN &amp; Rekan</b>", "Kontak KJA Farhani dan KAP DHN &amp; Rekan di %s</b>" % name, 1)
        box = re.sub(r'<div class="lk2-q">.*?</div>', "", box, count=1, flags=re.S)
        css = "" if "lk2d-css" in t else LK2D_CSS
        css += '<style id="ikd-css">.art table{border-collapse:collapse;width:100%}.art th,.art td{border:1px solid #333;padding:9px 10px;text-align:left;vertical-align:top}</style>'
        nav = RX_NAV.search(t)
        t = t[:nav.start()] + "<!--fa-ikd-->" + css + box + tim + "<!--/fa-ikd-->\n" + t[nav.start():]
    else:
        return "notim"

    # 2. inti halaman induk setelah Peta Isi
    nav = RX_NAV.search(t)
    rest = t[:nav.start()] + t[nav.end():]
    ids = set(re.findall(r'\sid="([^"]+)"', rest))
    c, toc = localize(core, name, ids)
    block = "<!--fa-induk-->" + c + "<!--/fa-induk-->"
    # 3. Peta Isi: enam butir induk di depan
    n0 = nav.group(0)
    lis = "".join('<li data-ik="1"><a href="#%s">%s</a></li>' % (i, lab) for i, lab in toc)
    n1 = n0.replace("<ol>", "<ol>" + lis, 1)
    btn = RX_BTN.search(n1)
    if btn:
        m = re.search(r"Lihat Semua \((\d+)\)", btn.group(0))
        old = int(m.group(1)) if m else n1.count("<li")
        base = btn.group(0)
        # simpan angka asli supaya jalan ulang tidak menumpuk
        mo = re.search(r'data-ik0="(\d+)"', base)
        orig = int(mo.group(1)) if mo else old
        tot = orig + len(toc)
        nb = ('<button aria-expanded="false" class="pf-more" data-for="pfmap" data-ik0="%d" data-l="Lihat Semua (%d)" type="button">Lihat Semua (%d) </button>'
              % (orig, tot, tot))
        n1 = n1.replace(base, nb, 1)
    else:
        tot = n1.count("<li")
        n1 = n1.replace('class="pf-map"', 'class="pf-map many"', 1)
        n1 = n1.replace("</ol>", '</ol><button aria-expanded="false" class="pf-more" data-for="pfmap" data-ikb="1" data-l="Lihat Semua (%d)" type="button">Lihat Semua (%d) </button>' % (tot, tot), 1)
    t = t[:nav.start()] + n1 + block + t[nav.end():]
    if t != o:
        open(path, "w", encoding="utf-8").write(t)
        return "ok"
    return "same"


def main():
    tim, lk2, core = load_parent()
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
            r = do(p, fam, tim, lk2, core)
            res[r] = res.get(r, 0) + 1
            if r not in ("ok", "same"):
                bad.append((r, os.path.relpath(p, ROOT)))
        print(fam, len(fams[fam]), res)
        for b in bad[:10]:
            print("   ", b)


if __name__ == "__main__":
    main()
