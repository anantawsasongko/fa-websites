# -*- coding: utf-8 -*-
"""13 Nov 2026: isi halaman daerah FA dilipat per bagian supaya rapi (Bos: "isi halaman daerah itu dilipat ya,
sehingga gak nampak berantakan"). SEO tetap: semua teks, link, id, dan H2 tetap ada di HTML; H2 pindah ke dalam
<summary> (judul tetap terlihat dan terbaca Google), isinya di dalam <details> tertutup.

Jalankan SETELAH fa_daerah_induk_20261113.py. Idempoten: lipatan lama (details.dfold) dibuka dulu, lalu dilipat
ulang, jadi aman dijalankan berkali-kali dan aman bila generator lama menambah isi.

Keluarga: /jasa-audit-laporan-keuangan/<kota>/, /wilayah/<kota>/, /wilayah/<kota>/kecamatan/<kec>/,
/wilayah/<kota>/<kawasan>/.
Aturan:
- Yang dilipat: setiap H2 tingkat atas di kolom isi (setelah Peta Isi) beserta isinya sampai H2 berikutnya.
- Section ber-H2 (Area Layanan, Layanan Lain) ikut dilipat: H2-nya ke summary, section utuh di dalam lipatan
  (details data-in="1", saat dibuka H2 kembali ke dalam section).
- Tidak dilipat: hero, dua kartu, Tim Kami, Peta Isi; akordeon Cek Izin (pkfold), akordeon rg; Pertanyaan Umum yang sudah berbentuk faq-acc;
  ekor halaman setelah Pertanyaan Umum (tombol, blok fa-pb).
- Klik butir Peta Isi atau buka URL dengan #anchor: lipatan terkait otomatis terbuka (script kecil df-js).
- Penanda komentar generator lama (<!--fa-tools-->...<!--/fa-tools--> dst.) bisa melintasi batas lipatan.
  Karena itu SEBELUM menjalankan ulang generator lama mana pun pada out/, jalankan dulu
  `python3 fa_daerah_lipat_20261113.py --buka` (semua lipatan dibuka kembali, struktur datar seperti semula),
  lalu di akhir build jalankan lagi tanpa --buka.
"""
import os, re, glob, sys
from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "faindonesia")
CSS = ('<style id="df-css">details.dfold{border-top:1px solid rgba(255,255,255,.12);margin:0}'
       'details.dfold:last-of-type{border-bottom:1px solid rgba(255,255,255,.12)}'
       'details.dfold>summary{list-style:none;cursor:pointer;position:relative;padding:20px 40px 20px 0}'
       'details.dfold>summary::-webkit-details-marker{display:none}'
       'details.dfold>summary:after{content:"+";position:absolute;right:4px;top:50%;margin-top:-16px;font-size:26px;'
       'line-height:32px;font-weight:300;opacity:.8;transition:transform .25s}'
       'details.dfold[open]>summary:after{transform:rotate(45deg)}'
       '.art details.dfold>summary>h2{margin:0!important;padding:0!important;border:0!important;'
       'font-size:clamp(20px,2.1vw,26px)!important;line-height:1.3}'
       'details.dfold>summary:hover>h2{opacity:.85}'
       'details.dfold>.dfb{padding:0 0 26px}'
       'details.dfold>.dfb>:first-child{margin-top:0}'
       '.wrap.art>nav.pf-map+details.dfold,.wrap.art>details.dfold:first-of-type{margin-top:34px}'
       '</style>')
JS = ('<script id="df-js">(function(){function o(h){if(!h)return;var e=document.getElementById(decodeURIComponent(h.slice(1)));'
      'if(!e)return;var d=e.closest("details.dfold");if(d&&!d.open){d.open=true;setTimeout(function(){e.scrollIntoView()},0)}}'
      'document.addEventListener("click",function(v){var a=v.target.closest&&v.target.closest("a[href^=\'#\']");if(a)o(a.getAttribute("href"))});'
      'window.addEventListener("hashchange",function(){o(location.hash)});'
      'if(document.readyState!="loading")o(location.hash);else document.addEventListener("DOMContentLoaded",function(){o(location.hash)})})();</script>')

RX_WRAP = re.compile(r'<div class="wrap art">')
MARK = re.compile(r"^(/?)([a-z0-9][a-z0-9-]*)$")


def wrap_bounds(t):
    m = RX_WRAP.search(t)
    if not m:
        return None
    i = m.end()
    depth, j = 1, i
    for x in re.finditer(r"<(/?)div\b[^>]*>", t[i:]):
        depth += -1 if x.group(1) else 1
        if depth == 0:
            j = i + x.start()
            break
    return i, j


def unfold(soup):
    for d in soup.find_all("details", class_="dfold", recursive=False):
        h2 = d.summary.find("h2")
        body = d.find("div", class_="dfb", recursive=False)
        items = list(body.contents) if body else []
        if d.get("data-in"):
            sec = next(x for x in items if isinstance(x, Tag))
            sec.insert(0, h2.extract())
        else:
            items = [h2] + items
        for it in items:
            d.insert_before(it.extract())
        d.decompose()


def is_start(c):
    return isinstance(c, Tag) and c.name == "h2"


def is_barrier(c):
    if not isinstance(c, Tag):
        return False
    cls = c.get("class") or []
    if c.name == "details" and ("pkfold" in cls or "rg" in cls):
        return True
    if c.name == "style":
        return False
    return False


def markers_ok(nodes):
    st = []
    for n in nodes:
        if isinstance(n, Comment):
            m = MARK.match(n.strip())
            if not m:
                continue
            if m.group(1):
                if st and st[-1] == m.group(2):
                    st.pop()
                else:
                    return False
            else:
                st.append(m.group(2))
    return not st


def fold(soup):
    kids = list(soup.contents)
    nav = soup.find("nav", class_="pf-map", recursive=False)
    if nav is not None:
        start_idx = kids.index(nav) + 1
        start_idx = kids.index(nav) + 1
    else:
        tim = soup.find("div", class_="wj")
        if tim is None:
            return "nostart"
        top = tim
        while top.parent is not soup:
            top = top.parent
        start_idx = kids.index(top) + 1
    groups, cur = [], None
    for c in kids[start_idx:]:
        if isinstance(c, Tag) and c.name == "section" and c.find("h2", recursive=False):
            cur = {"h2": c.find("h2", recursive=False), "body": [c], "faq": False, "in": True}
            groups.append(cur)
            cur = None
            continue
        if is_start(c):
            txt = c.get_text(" ", strip=True)
            if txt == "Pertanyaan Umum":
                cur = {"h2": c, "body": [], "faq": True}
            else:
                cur = {"h2": c, "body": [], "faq": False}
            groups.append(cur)
            continue
        if is_barrier(c):
            cur = None
            continue
        if cur is None:
            continue
        if cur["faq"]:
            if isinstance(c, Comment) or (isinstance(c, Tag) and (c.name == "div" and ("cbtns" in (c.get("class") or []) or not c.get("class")))):
                cur["stop"] = True
            if cur.get("stop"):
                continue
        cur["body"].append(c)
    n = 0
    for g in groups:
        body = g["body"]
        while body and isinstance(body[-1], NavigableString) and not isinstance(body[-1], Comment) and not body[-1].strip():
            body.pop()
        if g["faq"] and any(isinstance(b, Tag) and (b.get("class") and "faq-acc" in b.get("class") or b.find(class_="faq-acc")) for b in body):
            continue
        if not any(isinstance(b, Tag) or (isinstance(b, NavigableString) and b.strip() and not isinstance(b, Comment)) for b in body):
            continue
        h2 = g["h2"]
        d = soup.new_tag("details", attrs={"class": "dfold"})
        if g.get("in"):
            d["data-in"] = "1"
        s = soup.new_tag("summary")
        bx = soup.new_tag("div", attrs={"class": "dfb"})
        (body[0] if g.get("in") else h2).insert_before(d)
        s.append(h2.extract())
        d.append(s)
        d.append(bx)
        for b in body:
            bx.append(b.extract())
        n += 1
    return n


def do(path, buka=False):
    t = open(path, encoding="utf-8").read()
    b = wrap_bounds(t)
    if not b:
        return "nowrap"
    i, j = b
    inner = t[i:j]
    soup = BeautifulSoup(inner, "html.parser")
    unfold(soup)
    if not buka:
        r = fold(soup)
        if not isinstance(r, int):
            return r
    new_inner = str(soup)
    nt = t[:i] + new_inner + t[j:]
    if buka:
        nt = re.sub(r'<style id="df-css">.*?</style>', "", nt, count=1, flags=re.S)
        nt = re.sub(r'<script id="df-js">.*?</script>', "", nt, count=1, flags=re.S)
    elif "df-css" not in nt:
        nt = nt.replace("</head>", CSS + "</head>", 1)
    if not buka and "df-js" not in nt:
        nt = nt.replace("</body>", JS + "</body>", 1)
    if nt != t:
        open(path, "w", encoding="utf-8").write(nt)
        return "ok"
    return "same"


def files():
    R = ROOT
    out = glob.glob(os.path.join(R, "jasa-audit-laporan-keuangan", "*", "index.html"))
    out += glob.glob(os.path.join(R, "wilayah", "*", "index.html"))
    out += glob.glob(os.path.join(R, "wilayah", "*", "kecamatan", "*", "index.html"))
    out += [p for p in glob.glob(os.path.join(R, "wilayah", "*", "*", "index.html")) if os.sep + "kecamatan" + os.sep not in p]
    return sorted(out)


if __name__ == "__main__":
    buka = "--buka" in sys.argv
    fs = [a for a in sys.argv[1:] if a != "--buka"] or files()
    res, bad = {}, []
    for p in fs:
        r = do(p, buka)
        res[r] = res.get(r, 0) + 1
        if r not in ("ok", "same"):
            bad.append((r, os.path.relpath(p, ROOT)))
    print(len(fs), res)
    for x in bad[:15]:
        print("  ", x)
