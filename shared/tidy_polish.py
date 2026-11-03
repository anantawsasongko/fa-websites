# -*- coding: utf-8 -*-
"""Poles kerapian 3 situs (3 Nov 2026, permintaan Bos: rapi, margin, ukuran font, sistematis,
sedikit tulisan terbuka, SEO tetap maksimal, lebih banyak bagan).

Untuk halaman konten (artikel, halaman kota/wilayah, halaman jasa, PSAK):
1. "Peta Isi": bagan alur bernomor dari judul H2 di bawah pembuka, tiap node link ke bagiannya.
2. Tiap bagian H2 hanya menampilkan paragraf pertama + semua elemen visual (tabel, bagan, gambar, tombol).
   Sisa teks bagian itu dilipat ke tombol "Baca Selengkapnya". Teks tetap ada di HTML (terindeks Google).
Untuk semua halaman 3 situs:
3. Paragraf yang sangat panjang (>420 karakter) dipotong 4 baris + "Selengkapnya".
4. Batas bawah ukuran huruf 12px (label, badge, keterangan) dan jarak tepi minimal 16px di HP.
Dipanggil prep.py paling akhir sebelum zip. Idempoten (penanda data-polish)."""
import os, re
from bs4 import BeautifulSoup, NavigableString, Tag

SITES = ("faindonesia", "cariakuntan", "updatesak")
CONTENT = [r"^artikel/[^/]+/index\.html$", r"^kota/[^/]+/index\.html$", r"^layanan/[^/]+/index\.html$",
           r"^wilayah/[^/]+/index\.html$", r"^jasa-[^/]+/index\.html$", r"^konsultan-[^/]+/index\.html$",
           r"^psak/[^/]+/index\.html$", r"^update-[^/]+/index\.html$", r"^kap-murah/index\.html$",
           r"^jasa-pembukuan/index\.html$", r"^laporan-[^/]+/index\.html$", r"^cfo-[^/]+/index\.html$",
           r"^audit-[^/]+/index\.html$", r"^pendampingan-gcg/index\.html$", r"^penomoran-psak-baru/index\.html$"]
SKIP_H2 = ("artikel lainnya", "baca juga", "bacaan terkait", "pertanyaan umum", "faq", "artikel terkait", "kabar", "berita",
           "bagikan", "bermanfaat", "kontak", "hubungi", "mitra", "kap dhn", "kja farhani", "tim ", "sumber", "referensi", "tanya jawab", "daftar pustaka")
BAD_ANC = ("footer", "nav", "aside", "header", "form", "details")
BAD_CLS = ("dhns", "dhnc", "eco", "tshare", "related", "feedsec", "pf-map", "want", "cards2", "chips2", "gallery", "ft-more")
TEXT = ("p", "ul", "ol", "h3", "h4", "blockquote", "dl")

CSS = ('<style id="tidy-polish">'
       # peta isi
       '.pf-map{margin:22px 0 30px;padding:18px 18px 14px;border:1px solid rgba(127,127,127,.28);border-radius:14px}'
       '.pf-map>b{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.7;margin-bottom:12px;font-weight:600}'
       '.pf-map ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;counter-reset:pf}'
       '.pf-map li{counter-increment:pf;margin:0!important;position:relative}'
       '.pf-map a{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-radius:10px;background:rgba(127,127,127,.08);'
       'text-decoration:none!important;color:inherit;font-size:14px;line-height:1.35;min-height:44px;box-sizing:border-box;transition:background .2s}'
       '.pf-map a:hover{background:rgba(127,127,127,.16)}'
       '.pf-map.many li:nth-child(n+7){display:none}.pf-map.many.on li{display:block}.pf-map .pf-more{margin:12px 0 0}'
       '.pf-map a:before{content:counter(pf);flex:none;width:24px;height:24px;border-radius:50%;border:1px solid currentColor;'
       'display:grid;place-items:center;font-size:12px;font-weight:600;opacity:.85}'
       # lipat bagian
       '.pf-fold{display:none}.pf-fold.on{display:block;animation:pfin .35s ease}'
       '@keyframes pfin{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}'
       '.pf-more{display:inline-flex;align-items:center;gap:6px;margin:2px 0 18px;padding:8px 14px;min-height:36px;border-radius:999px;'
       'border:1px solid rgba(127,127,127,.45);background:transparent;color:inherit;font:inherit;font-size:13px;font-weight:600;cursor:pointer}'
       '.pf-more:hover{border-color:currentColor}.pf-more:after{content:"";width:6px;height:6px;border-right:1.5px solid;border-bottom:1.5px solid;transform:rotate(45deg) translateY(-2px)}'
       '.pf-more.on:after{transform:rotate(-135deg) translateY(-1px)}'
       # paragraf panjang
       '.pf-clamp{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}'
       '.pf-clamp.on{display:block}'
       # judul rapi + gutter HP
       'h1,h2,h3{text-wrap:balance}p,li{text-wrap:pretty}'
       '@media (max-width:600px){main p,main li,main h1,main h2,main h3{overflow-wrap:anywhere}}'
       '</style>'
       '<noscript><style>.pf-fold{display:block}.pf-more{display:none}.pf-clamp{display:block}</style></noscript>')

JS = ('<script id="tidy-polish-js">(function(){'
      'document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(".pf-more");if(!b)return;'
      'var t=b.getAttribute("data-for"),f=t?document.getElementById(t):b.previousElementSibling;if(!f)return;'
      'var on=f.classList.toggle("on");b.classList.toggle("on",on);b.setAttribute("aria-expanded",on);'
      'b.firstChild.nodeValue=on?"Tutup ":(b.getAttribute("data-l")||"Baca Selengkapnya")+" ";});'
      'function run(){'
      # paragraf panjang di <main>
      'var m=document.querySelector("main")||document.body;'
      '[].forEach.call(m.querySelectorAll("p"),function(p){if(p.closest(".pf-fold,details,form,footer,nav,.pf-map,label,button,td,th"))return;'
      'var n=(p.textContent||"").replace(/\\s+/g," ").trim().length;if(n<420||p.classList.contains("pf-clamp"))return;var nx=p.nextElementSibling;if(nx&&(nx.classList.contains("pf-fold")||nx.classList.contains("pf-more")))return;'
      'p.classList.add("pf-clamp");var b=document.createElement("button");b.type="button";b.className="pf-more";b.setAttribute("data-l","Selengkapnya");'
      'b.appendChild(document.createTextNode("Selengkapnya "));p.parentNode.insertBefore(b,p.nextSibling);'
      'b.addEventListener("click",function(ev){ev.stopPropagation();var on=p.classList.toggle("on");b.classList.toggle("on",on);b.firstChild.nodeValue=on?"Tutup ":"Selengkapnya ";});});'
      # ukuran huruf minimal 12px
      'var W=innerWidth;[].forEach.call(document.querySelectorAll("body *"),function(e){if(e.closest("svg,canvas,.pf-noscale"))return;'
      'var has=false;for(var i=0;i<e.childNodes.length;i++){var c=e.childNodes[i];if(c.nodeType==3&&c.textContent.trim().length>1){has=true;break}}'
      'if(!has)return;var fs=parseFloat(getComputedStyle(e).fontSize);if(fs&&fs<12)e.style.fontSize="12px";});}'
      'if(document.readyState=="loading")document.addEventListener("DOMContentLoaded",run);else run();'
      '})();</script>')


SITE_CSS = {
 "faindonesia": '<style id="tidy-polish-fa">@media (max-width:600px){nav.links a{font-size:12px!important}}</style>',
 "updatesak": '<style id="tidy-polish-us">@media (max-width:480px){nav.tabs{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr));row-gap:2px}nav.tabs a{text-align:center}}</style>',
}


def _bad(el):
    for a in el.parents:
        if not isinstance(a, Tag): continue
        if a.name in BAD_ANC: return True
        cls = " ".join(a.get("class") or [])
        if any(c in cls for c in BAD_CLS): return True
    return False


def _slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60] or "bagian"


def _txt(el):
    return re.sub(r"\s+", " ", el.get_text(" ")).strip()


def _is_text(el):
    if not isinstance(el, Tag) or el.name not in TEXT: return False
    if el.find(["table", "img", "svg", "canvas", "form", "iframe", "details", "button"]): return False
    if el.find("a", class_=re.compile(r"\bbtn\b")): return False
    return True


def polish_content(soup, fid):
    main = soup.find("main") or soup.body
    if not main: return 0
    h2s = [h for h in main.find_all("h2") if not _bad(h) and not any(_txt(h).lower().startswith(k) for k in SKIP_H2)]
    folds = 0
    # 1. peta isi
    if 3 <= len(h2s) <= 14 and not soup.select_one(".pf-map"):
        items = []
        used = set()
        for h in h2s:
            if not h.get("id"):
                base = _slug(_txt(h)); hid = base; k = 2
                while hid in used or soup.find(id=hid): hid = "%s-%d" % (base, k); k += 1
                h["id"] = hid
            used.add(h["id"])
            items.append('<li><a href="#%s">%s</a></li>' % (h["id"], _esc(_txt(h))))
        many = len(items) > 6
        more = ('<button type="button" class="pf-more" data-for="pfmap" data-l="Lihat Semua (%d)" aria-expanded="false">Lihat Semua (%d) </button>' % (len(items), len(items))) if many else ""
        nav = BeautifulSoup('<nav class="pf-map%s" id="pfmap" aria-label="Peta Isi"><b>Peta Isi</b><ol>%s</ol>%s</nav>' % (" many" if many else "", "".join(items), more), "html.parser")
        h2s[0].insert_before(nav)
    # 2. lipat teks per bagian
    for h in h2s:
        sib = []
        for s in h.next_siblings:
            if isinstance(s, NavigableString):
                if s.strip(): sib = []; break
                continue
            if s.name in ("h1", "h2") or (s.find("h2") if isinstance(s, Tag) else None): break
            sib.append(s)
        if not sib: continue
        first_p = next((i for i, s in enumerate(sib) if s.name == "p"), None)
        if first_p is None: continue
        run = []
        def flush(run):
            nonlocal folds
            if not run or sum(len(_txt(x)) for x in run) < 160: return
            fid[0] += 1; idf = "pf%d" % fid[0]
            wrap = soup.new_tag("div", attrs={"class": "pf-fold", "id": idf})
            run[0].insert_before(wrap)
            for x in run: wrap.append(x.extract())
            btn = soup.new_tag("button", attrs={"type": "button", "class": "pf-more", "data-for": idf, "aria-expanded": "false", "aria-controls": idf})
            btn.string = "Baca Selengkapnya "
            wrap.insert_after(btn); folds += 1
        for s in sib[first_p + 1:]:
            if _is_text(s): run.append(s)
            else: flush(run); run = []
        flush(run)
    return folds


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def run(OUT):
    n_all = n_content = n_fold = 0
    for site in SITES:
        root = os.path.join(OUT, site)
        if not os.path.isdir(root): continue
        for d, _, fs in os.walk(root):
            for f in fs:
                if not f.endswith(".html"): continue
                p = os.path.join(d, f); rel = os.path.relpath(p, root).replace(os.sep, "/")
                t = open(p, encoding="utf-8").read()
                if 'id="tidy-polish"' in t or "</head>" not in t or "</body>" not in t: continue
                if 'http-equiv="refresh"' in t or "noindex" in t and rel.startswith("toko/uji"): continue
                is_content = any(re.search(rx, rel) for rx in CONTENT) and not rel.startswith(("en/", "zh/", "hokkien/", "ja/"))
                if not is_content and site == "faindonesia" and 'class="wrap art"' in t and not rel.startswith(("en/", "zh/", "hokkien/", "ja/", "ko/")): is_content = True
                if is_content:
                    soup = BeautifulSoup(t, "html.parser"); fid = [0]
                    k = polish_content(soup, fid); n_fold += k; n_content += 1
                    t = str(soup)
                t = t.replace("</head>", CSS + SITE_CSS.get(site, "") + "</head>", 1).replace("</body>", JS + "</body>", 1)
                open(p, "w", encoding="utf-8").write(t); n_all += 1
    return {"halaman": n_all, "konten": n_content, "lipatan": n_fold}
