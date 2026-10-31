# -*- coding: utf-8 -*-
"""Rapikan halaman tab di 3 situs (31 Okt 2026, permintaan Bos):
1. Urutan section: yang terpenting (tombol, alat, grafik) di atas, yang panjang/lain-lain di bawah.
2. Minim tulisan: paragraf/daftar panjang dilipat ke tombol "Selengkapnya" (teks tetap ada di HTML untuk SEO).
3. Grid link yang panjang (mis. kartu artikel per topik) hanya tampil 4 kartu, sisanya "Lihat Semua (N)".
Dipanggil dari prep.py setelah Title Case. Idempoten (penanda data-tidy pada <main>).
"""
import os, re
from bs4 import BeautifulSoup, NavigableString

# urutan per halaman: TOP (urut), BOTTOM (urut); sisanya tetap urutan asli di tengah.
# matcher = id section, atau awalan teks judul h1/h2 (huruf kecil)
CONFIG = {
 "faindonesia/index.html": {
   "top": ["#mulai-cepat", "#jalur", "#angka", "#cek-kredit"],
   "bottom": ["#mulai", "#kontak"]},
 "faindonesia/layanan/index.html": {
   "top": ["layanan & rekam jejak", "#layanan", "rm bank", "implementasi psak 118", "rumah sakit dan klinik", "#fee", "#paket", "#rekam"],
   "bottom": ["#pendiri", "#afiliasi", "#arsip", "#grup", "#ekosistem", "#kontak"]},
 "faindonesia/apps/index.html": {"top": [], "bottom": []},
 "faindonesia/artikel/index.html": {"top": [], "bottom": []},
 "updatesak/index.html": {
   "top": ["#mulai-cepat", "#kalkulator", "#update-sak", "atau langsung pilih kebutuhan", "#jadwal"],
   "bottom": ["#standar-audit", "peta memilih", "linimasa", "struktur calk", "calk sudah jadi"]},
 "updatesak/eksplor/index.html": {
   "top": ["update sak terbaru", "#standar", "psak yang berlaku"],
   "bottom": ["kapan standar", "empat pilar", "#dosen", "#artikel", "#tanya"]},
 "updatesak/materi/index.html": {"top": [], "bottom": []},
 "updatesak/jadwal-ujian/index.html": {"top": [], "bottom": []},
 "cariakuntan/index.html": {
   "top": ["#mulai-cepat", "#screen", "screening menentukan", "#cek", "atau langsung pilih"],
   "bottom": ["cara kami mendampingi", "salah langkah", "#kami", "kirim laporan"]},
 "cariakuntan/artikel/index.html": {"top": [], "bottom": [], "no_grid": True, "clip": ["section.feed ul", "section.feed ol", "div.list"]},
}

LABEL = {"id": ("Selengkapnya", "Lihat Semua"), }
CSS = ('<style id="tidy-css">'
 'details.tidy{margin:6px 0 18px;grid-column:1/-1;flex-basis:100%}'
 'details.tidy>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:8px;'
 'padding:9px 16px;border:1px solid currentColor;border-radius:999px;font-size:13px;font-weight:600;opacity:.8;'
 'font-family:inherit;transition:opacity .2s,transform .2s;user-select:none}'
 'details.tidy>summary::-webkit-details-marker{display:none}'
 'details.tidy>summary:hover{opacity:1;transform:translateY(-1px)}'
 'details.tidy>summary:after{content:"";width:7px;height:7px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;'
 'transform:rotate(45deg) translateY(-2px);transition:transform .25s}'
 'details.tidy[open]>summary:after{transform:rotate(-135deg) translateY(-2px)}'
 'details.tidy[open]>summary{margin-bottom:14px}'
 'details.tidy>.tidy-body{animation:tidy-in .35s ease}'
 '@keyframes tidy-in{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}'
 '@media (prefers-reduced-motion:reduce){details.tidy>.tidy-body{animation:none}}'
 '.tcard{cursor:pointer;position:relative}'
 '.tcard .tc{display:none!important}'
 '.tcard.open .tc{display:block!important;animation:tidy-in .35s ease}'
 '.tcard:after{content:"+";position:absolute;top:8px;right:12px;font-size:20px;font-weight:300;opacity:.55;line-height:1;transition:transform .25s}'
 '.tcard.open:after{transform:rotate(45deg)}'
 '.tidy-tw{overflow-x:auto;max-width:100%;-webkit-overflow-scrolling:touch}.tblwrap{max-width:100%;overflow-x:auto}.wv,.wv section,.wv .wrap{min-width:0;max-width:100%}.wv .tblwrap{max-width:calc(100vw - 32px)}'
 '.tidy-clip{max-height:620px;overflow:hidden;position:relative;-webkit-mask-image:linear-gradient(#000 80%,transparent);mask-image:linear-gradient(#000 80%,transparent)}'
 '.tidy-clip.open{max-height:none;-webkit-mask-image:none;mask-image:none}'
 '.tidy-clipbtn{display:inline-flex;margin:10px 0 22px;padding:9px 16px;border:1px solid currentColor;border-radius:999px;background:none;color:inherit;font:600 13px/1 inherit;cursor:pointer;opacity:.8}'
 '.tidy-clipbtn:hover{opacity:1}'
 '.card2 span,.list a p,.list a span{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}'
 '</style>')

JS = ('<script id="tidy-js">document.addEventListener("click",function(e){var c=e.target.closest(".tcard");'
      'var b=e.target.closest(".tidy-clipbtn");if(b){var l=b.previousElementSibling;l.classList.add("open");b.remove();return}'
      'if(e.target.closest(".chips,.chips2")){document.querySelectorAll(".tidy-clip").forEach(function(l){l.classList.add("open");var n=l.nextElementSibling;if(n&&n.classList.contains("tidy-clipbtn"))n.remove()})}'
      'if(!c||e.target.closest("a,button,input,select,textarea,summary"))return;c.classList.toggle("open")});</script>')

KEEP_CLS = re.compile(r"step|bars|flow|chart(?!note)|timeline|orbit|diagram|peta|eyebrow|label|meta|^t$|^sub$|cnt|\bhead\b|cbtns|\bbtns\b|\bchips2?\b|\bactions\b|\bcta\b", re.I)
INTERACTIVE = ("input", "select", "textarea", "form", "canvas")

def words(el): return len(el.get_text(" ", strip=True).split())

def heading_text(sec):
    h = sec.find(["h1", "h2"])
    return h.get_text(" ", strip=True).lower() if h else ""

def match(sec, key):
    if key.startswith("#"): return sec.get("id") == key[1:]
    return heading_text(sec).startswith(key)

def container(sec):
    w = sec
    while True:
        k = [c for c in w.children if getattr(c, "name", None) and c.name not in ("style", "script")]
        if len(k) == 1 and k[0].name in ("div", "article", "section"): w = k[0]
        else: return w

def link_ratio(el):
    tw = words(el)
    if not tw: return 0
    return sum(words(a) for a in el.find_all(["a", "button"])) / tw

TITLE = ("h3", "h4", "h5", "b", "strong")
def card_items(el):
    """Anak langsung yang berbentuk kartu (punya judul pendek di awal)."""
    kids = [x for x in el.children if getattr(x, "name", None) in ("div", "li", "article", "a", "section")]
    if len(kids) < 2: return []
    ok = 0
    for k in kids:
        t = k.find(TITLE) or k.find(class_=re.compile(r"tit|name|tg"))
        if t is not None and words(t) <= 14: ok += 1
    return kids if ok >= max(2, .6 * len(kids)) else []

def is_cards(el):
    if el.name in ("table",): return False
    items = card_items(el)
    if not items: return False
    body = sum(words(x) for i in items for x in i.find_all(["p", "ul", "ol"]) if x.find_parent(["p", "ul", "ol"]) is None)
    return body >= 30

def kind(el):
    if not getattr(el, "name", None): return "keep"
    if el.name in ("style", "script", "noscript", "details", "summary"): return "keep"
    if el.name in ("h1", "h2", "h3", "h4"): return "keep"
    if KEEP_CLS.search(" ".join(el.get("class") or [])): return "keep"
    if el.find(INTERACTIVE) is not None or el.name in INTERACTIVE: return "keep"
    w = words(el)
    if w and el.find(["a", "button"]) is not None and link_ratio(el) >= .7: return "grid"
    if el.get("id") or el.find(id=True): return "keep"           # target JS
    if el.name in ("svg", "img", "figure", "canvas", "iframe", "video"): return "keep"
    if el.name == "table" or (el.name == "div" and "tblwrap" in (el.get("class") or [])): return "keep"
    if is_cards(el): return "cards"
    sub = [x for x in el.children if getattr(x, "name", None)]
    if len(sub) == 1 and is_cards(sub[0]): return "cards"
    if el.find(["svg", "img", "canvas", "iframe", "video"]) is not None and w < 60: return "keep"
    if w == 0: return "keep"
    if len(el.select("a.btn, button, .btn")) >= 2: return "keep"
    if w >= 15: return "fold"
    return "keep"

def mark_cards(el):
    g = el if card_items(el) else [x for x in el.children if getattr(x, "name", None)][0]
    for c in card_items(g):
        hit = False
        for x in c.find_all(["p", "ul", "ol"]):
            if x.find_parent(["p", "ul", "ol"]) is not None: continue
            if x.find(["a", "button", "input"]) is not None and link_ratio(x) > .5: continue
            if words(x) >= 8:
                x["class"] = (x.get("class") or []) + ["tc"]; hit = True
        if hit: c["class"] = (c.get("class") or []) + ["tcard"]

def mk_details(soup, label, nodes, n=None):
    d = soup.new_tag("details", attrs={"class": "tidy"})
    s = soup.new_tag("summary"); s.string = label + (f" ({n})" if n else ""); d.append(s)
    body = soup.new_tag("div", attrs={"class": "tidy-body"}); d.append(body)
    for x in nodes: body.append(x.extract())
    return d

def fold_container(soup, c, no_grid):
    kids = [x for x in c.children if getattr(x, "name", None)]
    group = []
    def flush():
        if not group: return
        if sum(words(g) for g in group) >= 15:
            ph = soup.new_tag("i"); group[0].insert_before(ph)
            ph.replace_with(mk_details(soup, "Selengkapnya", list(group)))
        group.clear()
    for k in kids:
        t = kind(k)
        if t == "fold": group.append(k); continue
        flush()
        if t == "cards": mark_cards(k); continue
        if t == "grid" and not no_grid:
            items = [x for x in k.children if getattr(x, "name", None) in ("a", "div", "li", "article")]
            if len(items) > 6:
                rest = items[4:]
                k.append(mk_details(soup, "Lihat Semua", [], n=len(items)))
                det = k.find_all("details", class_="tidy")[-1]
                body = det.find("div", class_="tidy-body")
                body["class"] = body.get("class", []) + [" ".join(k.get("class") or [])]
                for r in rest: body.append(r.extract())
            # grid bertingkat (topic > cards2)
            elif len(items) <= 3:
                for inner in k.find_all(["div", "ul"], recursive=False):
                    if kind(inner) == "grid": fold_container(soup, k, no_grid); break
    flush()

def tidy(path, cfg):
    t = open(path, encoding="utf-8").read()
    if "data-tidy" in t or "<main" not in t: return False
    soup = BeautifulSoup(t, "html.parser")
    main = soup.find("main")
    # 1. reorder
    secs = [c for c in main.children if getattr(c, "name", None) == "section"]
    if secs and (cfg["top"] or cfg["bottom"]):
        used = set(); top = []; bot = []
        for key in cfg["top"]:
            for s in secs:
                if id(s) not in used and match(s, key): top.append(s); used.add(id(s)); break
        for key in cfg["bottom"]:
            for s in secs:
                if id(s) not in used and match(s, key): bot.append(s); used.add(id(s)); break
        hero = [s for s in secs if re.search(r"hero", " ".join(s.get("class") or [])) and id(s) not in used]
        for h in hero: used.add(id(h))
        mid = [s for s in secs if id(s) not in used]
        order = hero + top + mid + bot
        anchor = secs[0]
        marker = soup.new_tag("i"); anchor.insert_before(marker)
        for s in order: s.extract()
        for s in order: marker.insert_before(s)
        marker.decompose()
        # facts di beranda FA tetap tepat di bawah hero
        facts = main.find("div", class_="facts", recursive=False)
        if facts and hero: hero[-1].insert_after(facts.extract())
    # 2. lipat tulisan panjang
    secs = [c for c in main.find_all("section") if c.find_parent("details") is None]
    blocks = secs if secs else [main]
    if main.find("article") and not secs: blocks = [main.find("article")]
    for s in blocks:
        cls = " ".join(s.get("class") or [])
        if re.search(r"hero", cls): continue
        c = container(s)
        fold_container(soup, c, cfg.get("no_grid"))
    if not secs:
        fold_container(soup, container(main), cfg.get("no_grid"))
    for s in blocks:
        if re.search(r"hero", " ".join(s.get("class") or [])): continue
        for p_ in s.find_all("p"):
            if words(p_) < 35 or p_.get("id") or p_.find(id=True): continue
            if p_.find_parent(["details", "form", "label", "a", "button"]) is not None: continue
            if p_.find_parent(class_=re.compile(r"\btcard\b|hero")) is not None: continue
            ph = soup.new_tag("i"); p_.insert_before(ph)
            ph.replace_with(mk_details(soup, "Selengkapnya", [p_]))
    # tabel lebar: gulir di kotaknya sendiri
    for tb in main.find_all("table"):
        if tb.find_parent(class_=re.compile(r"tblwrap|tidy-tw")) is None:
            w_ = soup.new_tag("div", attrs={"class": "tidy-tw"}); tb.wrap(w_)
    # daftar panjang ber-filter JS: dipotong tinggi, tombol Lihat Semua
    for sel in cfg.get("clip", []):
        for el in main.select(sel):
            n_ = len([x for x in el.children if getattr(x, "name", None)])
            if n_ <= 6 or "tidy-clip" in (el.get("class") or []): continue
            el["class"] = (el.get("class") or []) + ["tidy-clip"]
            b_ = soup.new_tag("button", attrs={"class": "tidy-clipbtn", "type": "button"}); b_.string = f"Lihat Semua ({n_})"
            el.insert_after(b_)
    main["data-tidy"] = "1"
    head = soup.find("head")
    if head and not soup.find("style", id="tidy-css"):
        head.append(BeautifulSoup(CSS, "html.parser"))
    if (soup.find(class_="tcard") is not None or soup.find(class_="tidy-clip") is not None) and not soup.find("script", id="tidy-js"):
        soup.body.append(BeautifulSoup(JS, "html.parser"))
    open(path, "w", encoding="utf-8").write(str(soup))
    return True

def run(out_root):
    n = 0
    for rel, cfg in CONFIG.items():
        p = os.path.join(out_root, rel)
        if os.path.exists(p) and tidy(p, cfg): n += 1
    return n
