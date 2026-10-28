# Blok "Artikel Lainnya" bergambar (gaya kartu media: sampul, kategori, tanggal, judul, tombol Baca).
# Dipanggil prep.py untuk out/faindonesia, out/cariakuntan, out/updatesak. Idempoten (penanda fxrel).
# Sampul dibuat dari CSS + SVG (tanpa foto pihak ketiga), warna per kategori, ikon per topik.
import os, re, html, json, hashlib

BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
STOP = set("dan di ke dari yang untuk atau dengan pada dalam ini itu apa cara bagi agar tidak bisa lebih jadi sudah oleh serta tahun terbaru 2025 2026 2027 vs the a of".split())

ICONS = {
    "bank": '<path d="M4 10h16M5 10v8m4-8v8m6-8v8m4-8v8M3 20h18M12 3l9 5H3z"/>',
    "pajak": '<path d="M7 3h10l2 3v15l-3-2-2 2-2-2-2 2-2-2-3 2V6z"/><path d="M9 9h6M9 13h6"/>',
    "audit": '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M8.5 11l2 2 3.5-4"/>',
    "psak": '<path d="M5 4h11l3 3v13H5z"/><path d="M8 9h8M8 13h8M8 17h5"/>',
    "investor": '<path d="M4 19h16M6 16l4-5 3 3 5-7"/><path d="M15 7h3v3"/>',
    "legal": '<path d="M12 3v18M5 7h14M7 7l-3 7h6zM17 7l-3 7h6z"/>',
    "rs": '<path d="M4 20V8l8-4 8 4v12H4z"/><path d="M12 10v6M9 13h6"/>',
    "rasio": '<path d="M4 20h16"/><rect x="6" y="11" width="3" height="7"/><rect x="11" y="7" width="3" height="11"/><rect x="16" y="13" width="3" height="5"/>',
    "dokumen": '<path d="M9 4h6v3H9z"/><path d="M7 5H5v16h14V5h-2"/><path d="M8 12l2 2 4-4M8 17h8"/>',
    "proyek": '<path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6"/>',
    "uang": '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 9v.01M18 15v.01"/>',
    "tanya": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5V14M12 17v.01"/>',
    "umum": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 9h8M8 13h8M8 17h4"/>',
}
TOPIC = [("rasio", "dscr rasio leverage ratio ebitda margin"), ("dokumen", "dokumen checklist syarat persyaratan berkas"),
         ("proyek", "kontraktor spk proyek konstruksi properti gudang"), ("uang", "pencairan undisbursed modal dana biaya fee harga gaji tarif"),
         ("tanya", "alasan kenapa mengapa ditolak gagal salah"), ("pajak", "pajak spt coretax pph ppn fiskal"), ("bank", "kredit bank kur pinjaman debitur dscr kmk plafon pencairan undisbursed"),
         ("audit", "audit kap auditor opini akuntan publik"), ("investor", "investor ipo akuisisi valuasi saham equity term"),
         ("legal", "pt nib oss izin akta notaris legal kjpp"), ("rs", "rumah sakit klinik bpr"),
         ("psak", "psak sak calk laporan keuangan ifrs standar jurnal ekuitas arus kas")]
PAL = {"fa": [("#2a2a2a", "#161616")], "ca": [("#0B1F33", "#17345f")], "us": [("#0B1F33", "#17345f")]}
ACC = {"fa": "#B91C1C", "ca": "#1F5BFF", "us": "#1F5BFF"}
LBL = {"fa": ("Artikel Lainnya", "Baca Selengkapnya"), "ca": ("Artikel Lainnya", "Baca Selengkapnya"), "us": ("Artikel Lainnya", "Baca Selengkapnya")}


def _meta(path, url):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    if not m: return None
    title = html.unescape(re.split(r"\s+\|\s+", m.group(1).strip())[0])
    d = re.search(r'"datePublished"\s*:\s*"(\d{4})-(\d{2})-(\d{2})', t)
    date = d.groups() if d else None
    cat = None
    for pat in (r'class="eyebrow"><a[^>]*>Eksplor · ([^<]+)<', r'<p class="label"[^>]*>([^<]{2,40})</p>', r'"articleSection"\s*:\s*"([^"]+)"'):
        c = re.search(pat, t)
        if c: cat = html.unescape(c.group(1)).strip(); break
    if not re.search(r'"@type"\s*:\s*"(Article|BlogPosting|NewsArticle)"', t): return None
    return dict(url=url, title=title, date=date, cat=cat or "Artikel", words=set(w for w in re.findall(r"[a-z0-9]+", title.lower()) if w not in STOP and len(w) > 2))


def _topic(a):
    for s in (a["title"].lower(), a["cat"].lower()):
        ws = set(re.findall(r"[a-z0-9]+", s))
        for k, kw in TOPIC:
            if ws & set(kw.split()): return k
    return "umum"


def _card(a, brand, i, btn):
    h = int(hashlib.md5(a["url"].encode()).hexdigest(), 16)
    c1, c2 = PAL[brand][h % len(PAL[brand])]
    ang = (h >> 8) % 4 * 45 + 115
    ic = ICONS[_topic(a)]
    dt = f'{int(a["date"][2])} {BULAN[int(a["date"][1]) - 1]} {a["date"][0]}' if a["date"] else ""
    return (f'<a class="fxr-c" href="{a["url"]}" style="--d:{i * 90}ms">'
            f'<span class="fxr-img" style="background:linear-gradient({ang}deg,{c1},{c2})" aria-hidden="true">'
            f'<svg class="fxr-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{ic}</svg>'
            f'</span>'
            f'<span class="fxr-x"><span class="fxr-m"><b>{html.escape(a["cat"])}</b><time>{dt}</time></span>'
            f'<span class="fxr-t">{html.escape(a["title"])}</span>'
            f'<span class="fxr-b">{btn}</span></span></a>')


def css(brand):
    a = ACC[brand]
    return ("<style>.fxrel{width:min(" + ("1080" if brand == "fa" else "1008") + "px,calc(100% - 32px));border:0;margin:28px auto 0;padding:0 0 8px;font-family:inherit}"
            ".fxrel h2{border:0;padding-top:0;font-size:clamp(1.4rem,3vw,1.9rem);margin:0 0 18px;line-height:1.2}"
            ".fxr-g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}"
            ".fxr-c{display:flex;flex-direction:column;text-decoration:none;color:var(--ink,#111827);background:var(--surface,#fff);border:1px solid var(--line,rgba(0,0,0,.1));border-radius:8px;overflow:hidden;"
            "transition:transform .25s ease,box-shadow .25s ease;opacity:0;animation:fxrUp .5s ease forwards;animation-delay:var(--d)}"
            ".fxr-c:hover{transform:translateY(-3px);border-color:rgba(127,127,127,.5)}"
            ".fxr-img{position:relative;aspect-ratio:16/10;display:block;overflow:hidden;color:rgba(255,255,255,.28)}"
            ".fxr-img:before{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1px);background-size:14px 14px;opacity:.35}"
            ".fxr-ic{position:absolute;right:8%;top:50%;transform:translateY(-50%);width:34%;height:auto;opacity:1;transition:transform .4s ease}"
            ".fxr-c:hover .fxr-ic{transform:translateY(-50%) scale(1.05)}"
            ".fxr-tag{position:absolute;left:12px;top:12px;font:600 .68rem/1 system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);padding:5px 8px;border-radius:99px;max-width:80%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"
            f".fxr-m{{display:flex;justify-content:space-between;gap:8px;padding:12px 14px 0;font-size:.74rem;letter-spacing:.04em;text-transform:uppercase}}.fxr-m b{{color:var(--muted,#6b7280);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.fxr-m time{{color:var(--muted,#6b7280);text-transform:none;letter-spacing:0;white-space:nowrap}}"
            ".fxr-t{padding:6px 14px 0;font-weight:600;line-height:1.35;font-size:.98rem;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}"
            f".fxr-b{{margin:12px 14px 14px;margin-top:auto;padding-top:12px;font-weight:600;font-size:.85rem;color:var(--ink,#111827);opacity:.8}}.fxr-b:after{{content:' →';transition:margin .2s}}.fxr-c:hover .fxr-b:after{{margin-left:4px}}"
            "@keyframes fxrUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"
            "@media (max-width:900px){.fxr-g{grid-template-columns:repeat(2,minmax(0,1fr))}}"
            ".fxr-x{display:flex;flex-direction:column;flex:1;min-width:0}"
            "@media (max-width:520px){.fxr-g{grid-template-columns:1fr;gap:12px}.fxr-c{flex-direction:row}.fxr-img{aspect-ratio:auto;width:32%;min-height:104px;flex:none}.fxr-tag{display:none}.fxr-ic{width:44%;right:28%}.fxr-c:hover .fxr-ic{transform:translateY(-50%) scale(1.06)}.fxr-m{padding:10px 12px 0}.fxr-t{padding:4px 12px 0;font-size:.92rem;-webkit-line-clamp:3}.fxr-b{margin:8px 12px 10px;padding-top:6px}}"
            "@media (prefers-reduced-motion:reduce){.fxr-c{animation:none;opacity:1}}</style>")


def add_related(root, brand, extra_dirs=()):
    arts = []
    dirs = [os.path.join(root, "artikel", d) for d in sorted(os.listdir(os.path.join(root, "artikel"))) if os.path.isdir(os.path.join(root, "artikel", d))]
    dirs += [os.path.join(root, d) for d in extra_dirs]
    for d in dirs:
        p = os.path.join(d, "index.html")
        if not os.path.exists(p): continue
        url = "/" + os.path.relpath(d, root).replace(os.sep, "/") + "/"
        m = _meta(p, url)
        if m: m["path"] = p; arts.append(m)
    head, btn = LBL[brand]
    n = 0
    for a in arts:
        def score(b):
            s = len(a["words"] & b["words"]) * 3 + (4 if b["cat"] == a["cat"] else 0) + (2 if _topic(b) == _topic(a) else 0)
            return (s, b["date"] or ("0",))
        rel = sorted((b for b in arts if b["url"] != a["url"]), key=score, reverse=True)[:4]
        if len(rel) < 2: continue
        cards = "".join(_card(b, brand, i, btn) for i, b in enumerate(rel))
        block = f'<!--fxrel--><section class="fxrel" aria-label="{head}">{css(brand)}<h2>{head}</h2><div class="fxr-g">{cards}</div></section><!--/fxrel-->'
        t = open(a["path"], encoding="utf-8").read()
        t = re.sub(r"<!--fxrel-->.*?<!--/fxrel-->", "", t, flags=re.S)
        k = t.rfind("<footer")
        if k < 0: k = t.rfind("</body>")
        t = t[:k] + block + "\n" + t[k:]
        open(a["path"], "w", encoding="utf-8").write(t); n += 1
    return n
