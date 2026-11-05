# -*- coding: utf-8 -*-
"""Blok "Cek Izin" dari registri PPPK Kemenkeu (5 Nov 2026, permintaan Bos).
Sumber data: shared/pppk/registry.json (dibuat workflow .github/workflows/pppk.yml dari find-profkeu.kemenkeu.go.id).

Dipasang ke halaman yang sudah di-build (dipanggil prep.py sebelum dhn, atau langsung `python3 shared/pppk/izin.py out`):
- cariakuntan: /kota/<kota>/ dan /kota/<kota>/{kap,kja,kjpp,konsultan-pajak,jasa-laporan-keuangan}/ -> blok sebelum kotak screening (ca-scr)
- faindonesia: /wilayah/<kota>/ -> blok setelah paragraf "Cari KAP, KJPP, dan Konsultan Pajak di <Kota>"
- halaman hub cariakuntan.com/cek-izin/ (pencarian seluruh Indonesia), masuk sitemap dan llms.txt
- /data/izin.json + /js/izin.js di kedua situs (pencarian di browser, dimuat saat kolom cari dipakai)
Isi blok: daftar KAP, KJA, KJPP yang terdaftar di kota itu (semua status, badge Aktif/Non-aktif), link ke halaman detail registri,
kolom cari nasional (KAP, AP, KJA, AB, KJPP, Penilai, Konsultan Pajak), catatan notaris, dan SATU kontak: tombol WA Bos.
Telepon/email kantor lain tidak pernah ditampilkan. Idempoten (penanda <!--pk--> ... <!--/pk-->)."""
import os, re, json, sys, html, unicodedata
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REG = os.path.join(HERE, "registry.json")
WA = "6282245260121"
BASE = "https://find-profkeu.kemenkeu.go.id"
SETS = [("kap", "KAP", "Kantor Akuntan Publik"), ("ap", "AP", "Akuntan Publik"), ("kja", "KJA", "Kantor Jasa Akuntansi"),
        ("ab", "AB", "Akuntan Berpraktik"), ("kjpp", "KJPP", "Kantor Jasa Penilai Publik"), ("penilai", "Penilai", "Penilai Publik"),
        ("kp", "Konsultan Pajak", "Konsultan Pajak")]
CITY_SETS = ("kap", "kja", "kjpp")
LABEL = {k: v for k, v, _ in SETS}
LONG = {k: v for k, _, v in SETS}
PRE = {"kap": "kap", "kja": "kja", "kjpp": "kjpp", "konsultan-pajak": "kp", "jasa-laporan-keuangan": "kja"}

def E(t): return html.escape(str(t or ""), quote=True)

def slug(t):
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def norm_city(v):
    v = " ".join(str(v or "").split()).lower()
    v = re.sub(r"^(kota adm\.?|kota administrasi|kota|kab\.|kabupaten|kab)\s+", "", v)
    v = re.sub(r"^jakarta\s+(selatan|pusat|utara|barat|timur)$", "jakarta", v)
    if v in ("null", "none", "-", ""): return ""
    return v

def load():
    if not os.path.exists(REG): return None
    return json.load(open(REG, encoding="utf-8"))

def st_cls(s):
    s = (s or "").strip().lower()
    if s == "aktif": return "ok"
    if s.startswith("aktif"): return "warn"
    return "off"

def st_txt(s):
    s = (s or "").strip()
    return {"Non-Aktif(permohonan)": "Non-aktif (tutup)", "Non-Aktif(tidak berlaku)": "Non-aktif", "Non-Aktif(sanksi)": "Dicabut"}.get(s, s or "-")

def city_index(reg):
    idx = {k: {} for k in CITY_SETS}
    for k in CITY_SETS:
        for r in reg["sets"].get(k, []):
            idx[k].setdefault(norm_city(r.get("k")), []).append(r)
    return idx

def sort_rows(rows):
    return sorted(rows, key=lambda r: ({"ok": 0, "warn": 1, "off": 2}[st_cls(r.get("s"))], (r.get("n") or "").lower()))

def li(r, k):
    u = r.get("u")
    link = f'<a href="{BASE}{E(u)}" target="_blank" rel="noopener nofollow">Registri Kemenkeu ↗</a>' if u else ""
    sub = []
    if r.get("no"): sub.append(E(r["no"]))
    if k in ("ap", "ab") and r.get("o"): sub.append(E(r["o"]))
    if k == "kjpp" and r.get("o"): sub.append(E(r["o"]))
    if k not in CITY_SETS and r.get("k"): sub.append(E(r["k"]))
    return (f'<li><span class="pk-n">{E(r.get("n"))}</span><span class="pk-m">{" · ".join(sub)}</span>'
            f'<span class="pk-s {st_cls(r.get("s"))}">{E(st_txt(r.get("s")))}</span>{link}</li>')

CSS = ("<style id=\"pk-css\">"
 ".pk{box-sizing:border-box;margin:30px 0;padding:22px 22px 18px;border:1px solid var(--line,#444);border-radius:12px;background:var(--panel,rgba(127,127,127,.08))}"
 ".pk h2,.pk h3{margin:0 0 6px}.pk h3{font-size:1.05em;margin-top:18px}.pk .pk-sub{margin:0 0 14px;opacity:.85;font-size:.95em;line-height:1.55}"
 ".pk-f{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;margin:0 0 10px}@media(max-width:560px){.pk-f{grid-template-columns:1fr}}"
 ".pk-f input,.pk-f select{box-sizing:border-box;width:100%;font:inherit;font-size:16px;padding:11px 12px;border:1px solid var(--line,#555);border-radius:8px;background:var(--bg,transparent);color:inherit;min-height:44px}"
 ".pk-sum{font-size:.95em;margin:8px 0 10px}.pk-sum b{font-weight:600}"
 ".pk-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 10px}.pk-tabs button{font:inherit;font-size:14px;padding:7px 14px;border:1px solid var(--line,#555);border-radius:999px;background:transparent;color:inherit;cursor:pointer}"
 ".pk-tabs button[aria-selected=true]{border-color:currentColor;background:rgba(127,127,127,.2);font-weight:600;box-shadow:inset 0 0 0 1px currentColor}"
 ".pk-l{list-style:none;margin:0;padding:0}.pk-l li{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:4px 12px;align-items:center;padding:9px 0;border-top:1px solid var(--line,#444);font-size:.95em}"
 ".pk-l li:first-child{border-top:0}.pk-n{font-weight:600;grid-column:1}.pk-m{grid-column:1;font-size:.86em;opacity:.75}.pk-l li a{grid-column:3;grid-row:1/3;font-size:.86em;white-space:nowrap;text-decoration:underline;color:inherit}"
 ".pk-s{grid-column:2;grid-row:1/3;font-size:.78em;letter-spacing:.04em;padding:3px 9px;border-radius:999px;white-space:nowrap;border:1px solid}"
 ".pk-s.ok{color:#15803d;border-color:#15803d;background:rgba(21,128,61,.1)}.pk-s.warn{color:#b45309;border-color:#b45309}.pk-s.off{opacity:.6}"
 "@media(max-width:560px){.pk-l li{grid-template-columns:minmax(0,1fr) auto}.pk-l li a{grid-column:1/3;grid-row:auto}}"
 ".pk details{margin:6px 0 0}.pk summary{cursor:pointer;font-size:.92em;padding:6px 0;opacity:.85}.pk [hidden]{display:none!important}"
 ".pk-r{margin:0 0 8px}.pk-r .pk-h{font-size:.9em;opacity:.8;margin:4px 0 6px}"
 ".pk-note{font-size:.9em;opacity:.8;line-height:1.55;margin:14px 0 0}"
 ".pk-cta{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:14px 0 0;padding-top:14px;border-top:1px solid var(--line,#444)}"
 ".pk-cta a.pk-wa{display:inline-block;background:#25D366;color:#fff!important;border-radius:999px;padding:11px 20px;font-weight:600;text-decoration:none!important;font-size:15px}"
 ".pk-cta span{font-size:.9em;opacity:.85;flex:1 1 260px}"
 "@media print{.pk-f,.pk-cta{display:none}}</style>")

JS = r"""(function(){var D=null,P=null;function q(s,r){return (r||document).querySelector(s)}function all(s,r){return [].slice.call((r||document).querySelectorAll(s))}
var LAB={kap:"KAP",ap:"Akuntan Publik",kja:"KJA",ab:"Akuntan Berpraktik",kjpp:"KJPP",penilai:"Penilai Publik",kp:"Konsultan Pajak"};
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function cls(s){s=(s||"").toLowerCase();return s==="aktif"?"ok":s.indexOf("aktif")===0?"warn":"off"}
function txt(s){return{"Non-Aktif(permohonan)":"Non-aktif (tutup)","Non-Aktif(tidak berlaku)":"Non-aktif","Non-Aktif(sanksi)":"Dicabut"}[s]||s||"-"}
function li(r,k){var sub=[];if(r.no)sub.push(esc(r.no));if(r.o)sub.push(esc(r.o));if(r.k)sub.push(esc(r.k));
 return '<li><span class="pk-n">'+esc(r.n)+'</span><span class="pk-m">'+LAB[k]+(sub.length?" · "+sub.join(" · "):"")+'</span><span class="pk-s '+cls(r.s)+'">'+esc(txt(r.s))+'</span>'+(r.u?'<a href="https://find-profkeu.kemenkeu.go.id'+esc(r.u)+'" target="_blank" rel="noopener nofollow">Registri Kemenkeu ↗</a>':"")+'</li>'}
function load(){if(P)return P;P=fetch("/data/izin.json").then(function(r){return r.json()}).then(function(j){D=j;return j});return P}
function norm(s){return String(s||"").toLowerCase().replace(/[^a-z0-9]+/g," ").trim()}
function search(box){var inp=q("input",box),sel=q("select",box),out=q(".pk-r",box),v=norm(inp.value),t=sel.value;
 if(v.length<2){out.hidden=true;out.innerHTML="";var cur=q(".pk-tabs button[aria-selected=true]",box);all(".pk-city",box).forEach(function(e){var t=e.getAttribute("data-t");e.hidden=!!(t&&cur&&t!==cur.getAttribute("data-t"))});return}
 out.hidden=false;out.innerHTML='<p class="pk-h">Mencari…</p>';
 load().then(function(d){var res=[],keys=t?[t]:["kap","kja","kjpp","ap","ab","kp","penilai"];
  keys.forEach(function(k){(d[k]||[]).forEach(function(r){var h=norm(r.n+" "+(r.no||"")+" "+(r.o||"")+" "+(r.k||""));if(h.indexOf(v)>=0)res.push([k,r])})});
  res.sort(function(a,b){var x=cls(a[1].s)==="ok"?0:1,y=cls(b[1].s)==="ok"?0:1;return x-y||String(a[1].n).localeCompare(String(b[1].n))});
  var n=res.length;all(".pk-city",box).forEach(function(e){e.hidden=true});
  out.innerHTML='<p class="pk-h">'+(n?n+" hasil"+(n>60?", ditampilkan 60 pertama":""):"Tidak ada yang cocok")+' untuk "'+esc(inp.value)+'" di registri PPPK (data '+esc(d.updated||"")+')</p><ul class="pk-l">'+res.slice(0,60).map(function(x){return li(x[1],x[0])}).join("")+"</ul>"}).catch(function(){out.innerHTML='<p class="pk-h">Data belum bisa dimuat. Coba lagi sebentar.</p>'})}
all(".pk").forEach(function(box){var inp=q("input",box),sel=q("select",box);if(!inp)return;var t;
 inp.addEventListener("focus",function(){load()});inp.addEventListener("input",function(){clearTimeout(t);t=setTimeout(function(){search(box)},180)});
 if(sel)sel.addEventListener("change",function(){search(box)});
 all(".pk-tabs button",box).forEach(function(b){b.addEventListener("click",function(){all(".pk-tabs button",box).forEach(function(x){x.setAttribute("aria-selected",x===b)});all(".pk-city",box).forEach(function(e){e.hidden=e.getAttribute("data-t")!==b.getAttribute("data-t")})})})});
})();"""

def wa_url(city, prof=None):
    p = {"kap": "KAP", "kja": "KJA", "kjpp": "KJPP", "kp": "konsultan pajak"}.get(prof or "", "KAP / KJA / KJPP")
    return f"https://wa.me/{WA}?text=" + quote(f"Halo Pak Ananta, saya butuh rekomendasi {p} di {city}." if city else f"Halo Pak Ananta, saya butuh rekomendasi {p}.")

def block(reg, idx, city, pre=None, site="ca", hub=False):
    nc = norm_city(city) if city else ""
    upd = reg.get("updated", "")
    have = {k for k, _, _ in SETS if reg["sets"].get(k)}
    sel = "".join(f'<option value="{k}"{" selected" if pre == k else ""}>{E(LONG[k])}</option>' for k, _, _ in SETS if k in have)
    kp_ok = "kp" in have
    head = (("Cek Izin KAP, KJA, KJPP, Konsultan Pajak, dan Penilai Publik" if kp_ok else "Cek Izin KAP, Akuntan Publik, KJA, KJPP, dan Penilai Publik") if hub else
            (f"Cek Izin KAP, KJA, KJPP, dan Konsultan Pajak di {E(city)}" if kp_ok else f"Cek Izin KAP, KJA, dan KJPP di {E(city)}"))
    sub = ("Data registri resmi PPPK Kementerian Keuangan (find-profkeu.kemenkeu.go.id), diperbarui otomatis tiap bulan, terakhir " + E(upd) +
           ". Ketik nama kantor, nama akuntan, atau nomor izin. Hasil ringkas tampil langsung di sini, lengkap dengan link ke halaman registri.")
    out = [f'<!--pk--><section class="pk" id="cek-izin" data-city="{E(city)}"><h2>{head}</h2><p class="pk-sub">{sub}</p>',
           f'<form class="pk-f" role="search" onsubmit="return false"><input type="search" placeholder="Nama kantor, akuntan, atau nomor izin" aria-label="Cari izin profesi keuangan" autocomplete="off"><select aria-label="Profesi"><option value="">Semua profesi</option>{sel}</select></form>',
           '<div class="pk-r" hidden></div>']
    if nc:
        rows = {k: sort_rows(idx[k].get(nc, [])) for k in CITY_SETS}
        act = {k: sum(1 for r in rows[k] if st_cls(r.get("s")) == "ok") for k in CITY_SETS}
        tot = sum(len(v) for v in rows.values())
        if tot:
            out.append('<div class="pk-city"><div class="pk-sum">Terdaftar di ' + E(city) + ": " +
                       " · ".join(f'<b>{LABEL[k]} {len(rows[k])}</b> ({act[k]} aktif)' for k in CITY_SETS if rows[k]) + "</div>")
            first = pre if pre in CITY_SETS and rows.get(pre) else next(k for k in CITY_SETS if rows[k])
            out.append('<div class="pk-tabs" role="tablist">' + "".join(
                f'<button type="button" role="tab" data-t="{k}" aria-selected="{"true" if k == first else "false"}"><span>{LABEL[k]} ({len(rows[k])})</span></button>'
                for k in CITY_SETS if rows[k]) + "</div>")
            for k in CITY_SETS:
                if not rows[k]: continue
                hid = "" if k == first else " hidden"
                ok = [r for r in rows[k] if st_cls(r.get("s")) != "off"]; off = [r for r in rows[k] if st_cls(r.get("s")) == "off"]
                part = f'<div class="pk-city" data-t="{k}"{hid}>'
                if ok:
                    part += '<ul class="pk-l">' + "".join(li(r, k) for r in ok[:12]) + "</ul>"
                    if len(ok) > 12:
                        part += f'<details><summary>Tampilkan {len(ok) - 12} {LABEL[k]} aktif lainnya</summary><ul class="pk-l">' + "".join(li(r, k) for r in ok[12:]) + "</ul></details>"
                else:
                    part += f'<p class="pk-note" style="margin-top:4px">Belum ada {LABEL[k]} berstatus aktif yang tercatat di {E(city)}.</p>'
                if off:
                    part += f'<details><summary>{len(off)} {LABEL[k]} non-aktif atau sudah tutup</summary><ul class="pk-l">' + "".join(li(r, k) for r in off) + "</ul></details>"
                out.append(part + "</div>")
            out.append("</div>")
        else:
            # kota tanpa kantor terdaftar: tunjukkan kota terdekat di provinsi yang sama
            prov = ""
            for k in CITY_SETS:
                for r in reg["sets"].get(k, []):
                    if norm_city(r.get("k")) == nc and r.get("p"): prov = r["p"]; break
                if prov: break
            out.append(f'<div class="pk-city"><p class="pk-note" style="margin-top:0">Belum ada KAP, KJA, atau KJPP yang beralamat di {E(city)} menurut registri. '
                       f'Kantor terdekat biasanya di ibu kota provinsi; gunakan kolom cari di atas, atau minta kami carikan yang mau datang ke {E(city)}.</p></div>')
    if hub:
        n = {k: len(reg["sets"].get(k, [])) for k, _, _ in SETS}
        a = {k: sum(1 for r in reg["sets"].get(k, []) if st_cls(r.get("s")) == "ok") for k, _, _ in SETS}
        out.append('<div class="pk-city"><div class="pk-sum">Isi registri: ' + " · ".join(
            f'<b>{LABEL[k]} {n[k]:,}</b>'.replace(",", ".") + (f" ({a[k]:,} aktif)".replace(",", ".") if k != "penilai" else "") for k, _, _ in SETS if n[k]) + "</div></div>")
    out.append('<p class="pk-note">' + ('Konsultan pajak, penilai publik' if kp_ok else 'Penilai publik') + ', akuntan publik, dan akuntan berpraktik tidak dicatat per kota oleh registri, jadi carilah lewat nama. '
               + ('' if kp_ok else 'Daftar konsultan pajak di registri Kemenkeu sedang tidak bisa diakses dan akan muncul otomatis begitu tersedia; sementara itu kami bantu cek izin konsultan pajak Anda. ')
               + 
               'Notaris tidak masuk registri Kemenkeu; pencarian profil notaris di AHU Kemenkumham sedang tidak tersedia untuk publik, kami bantu rekomendasikan notaris rekanan. '
               'Telepon dan email kantor lain tidak kami tampilkan; kontak resminya ada di halaman registri masing-masing.</p>')
    out.append(f'<div class="pk-cta"><a class="pk-wa" href="{wa_url(city, pre)}" target="_blank" rel="noopener">Minta rekomendasi{(" di " + E(city)) if city else ""}</a>'
               '<span>Bingung memilih yang cocok dengan bank, tender, atau RUPS Anda? Chat Ananta, CPA. Kami cek izin, kelas rekanan bank, dan jadwalnya, gratis.</span></div>')
    out.append("</section><!--/pk-->")
    return "".join(out)

def ensure_assets(site_root, reg):
    os.makedirs(os.path.join(site_root, "data"), exist_ok=True); os.makedirs(os.path.join(site_root, "js"), exist_ok=True)
    slim = {"updated": reg.get("updated", "")}
    for k, _, _ in SETS:
        slim[k] = [{a: b for a, b in r.items() if a in ("n", "no", "o", "k", "s", "u")} for r in reg["sets"].get(k, [])]
    json.dump(slim, open(os.path.join(site_root, "data", "izin.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    open(os.path.join(site_root, "js", "izin.js"), "w", encoding="utf-8").write(JS)

def inject(path, blk, where):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<!--pk-->.*?<!--/pk-->", "", s, flags=re.S)
    s = s.replace(CSS, "").replace('<script src="/js/izin.js" defer></script>', "")
    k = -1
    if where == "ca-scr":
        k = s.find("<!--ca-scr-->")
        if k < 0: k = s.rfind("</main>")
    elif where == "fa-cari":
        m = re.search(r"<h2>Cari KAP, KJPP, dan Konsultan Pajak di [^<]*</h2>\s*<p>.*?</p>", s, re.S)
        if m: k = m.end()
        else:
            m = re.search(r"<!--fa-kk-all-->", s); k = m.start() if m else s.rfind("</main>")
    if k < 0: return False
    s = s[:k] + blk + s[k:]
    s = s.replace("</head>", CSS + "</head>", 1).replace("</body>", '<script src="/js/izin.js" defer></script></body>', 1)
    open(path, "w", encoding="utf-8").write(s); return True

def city_names():
    try:
        sys.path.insert(0, os.path.join(ROOT, "cariakuntan")); import cities as _c
        return {slug(c[0]): c[0] for c in _c.CITIES}
    except Exception:
        return {}

def hub_page(site_root, reg, idx, names):
    tpl = os.path.join(site_root, "screening", "index.html")
    if not os.path.exists(tpl): return False
    s = open(tpl, encoding="utf-8").read()
    s = re.sub(r"<!--ca-scr-->.*?<!--/ca-scr-->", "", s, flags=re.S)
    s = re.sub(r"<!--pk-->.*?<!--/pk-->", "", s, flags=re.S)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', "", s, flags=re.S)
    title = "Cek Izin KAP, KJA, KJPP, Konsultan Pajak, dan Penilai Publik Seluruh Indonesia | cariakuntan.com"
    desc = ("Cari nama kantor atau nomor izin di registri resmi PPPK Kementerian Keuangan: KAP, akuntan publik, KJA, akuntan berpraktik, KJPP, penilai publik, dan konsultan pajak. "
            "Status aktif atau non-aktif, link ke halaman registri, diperbarui tiap bulan.")
    s = re.sub(r"<title>.*?</title>", "<title>" + E(title) + "</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://cariakuntan.com/cek-izin/">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(desc)}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="https://cariakuntan.com/cek-izin/">', s, count=1)
    s = re.sub(r'<meta property="og:image"[^>]*>', "", s)
    s = s.replace(' aria-current="page"', "")
    # tabel provinsi
    prov = {}
    for k in CITY_SETS:
        for r in reg["sets"].get(k, []):
            p = (r.get("p") or "").strip()
            if not p: continue
            d = prov.setdefault(p, {"kap": 0, "kja": 0, "kjpp": 0, "cities": {}})
            d[k] += 1
            c = norm_city(r.get("k"))
            if c: d["cities"][c] = d["cities"].get(c, 0) + 1
    rows = []
    for p in sorted(prov):
        d = prov[p]
        top = sorted(d["cities"].items(), key=lambda x: -x[1])[:6]
        links = []
        for c, n in top:
            sl = slug(c)
            if sl in names: links.append(f'<a href="/kota/{sl}/">{E(names[sl])}</a> ({n})')
            else: links.append(f"{E(c.title())} ({n})")
        rows.append(f"<tr><th scope=\"row\">{E(p)}</th><td>{d['kap']}</td><td>{d['kja']}</td><td>{d['kjpp']}</td><td>{', '.join(links)}</td></tr>")
    table = ('<div class="tblwrap"><table class="tbl"><thead><tr><th>Provinsi</th><th>KAP</th><th>KJA</th><th>KJPP</th><th>Kota terbanyak (link ke halaman kota)</th></tr></thead><tbody>'
             + "".join(rows) + "</tbody></table></div>")
    faq = [("Apakah data ini resmi?", "Ya. Seluruh daftar diambil dari registri publik Pusat Pembinaan Profesi Keuangan (PPPK) Kementerian Keuangan dan diperbarui otomatis tiap awal bulan. Untuk keputusan penting, buka link \"Registri Kemenkeu\" pada tiap baris untuk melihat kondisi terkini, termasuk KMK izin, rekan, dan cabang."),
           ("Kenapa tidak ada nomor telepon kantornya?", "Kami hanya menampilkan nama, nomor izin, kota, dan status. Alamat dan kontak resmi tiap kantor ada di halaman registri Kemenkeu. Kalau Anda butuh rekomendasi yang cocok dengan bank atau kebutuhan Anda, hubungi kami lewat tombol WhatsApp."),
           ("Apa arti status non-aktif?", "Non-aktif (tutup) berarti kantor sudah mengajukan penutupan; non-aktif tidak berlaku biasanya karena pemimpin meninggal dunia; dicabut berarti dikenai sanksi pencabutan izin. Hanya kantor berstatus Aktif yang boleh memberikan jasa."),
           ("Bagaimana dengan notaris?", "Notaris bukan profesi keuangan, jadi tidak ada di registri PPPK. Pencarian profil notaris di AHU Kemenkumham saat ini belum tersedia untuk publik. Kami bisa merekomendasikan notaris rekanan di kota Anda, terutama untuk akta RUPS laporan tahunan PT.")]
    faqh = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": "Cek Izin Profesi Keuangan", "url": "https://cariakuntan.com/cek-izin/", "applicationCategory": "FinanceApplication", "operatingSystem": "Web",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR"}, "inLanguage": "id", "isBasedOn": BASE},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    main = ('<main class="wrap art"><p class="crumb"><a href="/">Beranda</a> / Cek Izin</p><p class="label">Registri Resmi</p>'
            '<h1>Cek Izin KAP, KJA, KJPP, Konsultan Pajak, dan Penilai Publik</h1>'
            '<p class="sub">Sebelum menunjuk kantor akuntan publik, kantor jasa akuntansi, kantor jasa penilai publik, atau konsultan pajak, pastikan izinnya masih aktif di registri Kementerian Keuangan. Gratis, tanpa daftar.</p>'
            + block(reg, idx, "", None, "ca", hub=True) +
            '<h2 style="margin-top:30px">Sebaran Kantor Berizin per Provinsi</h2><p>Jumlah kantor yang tercatat (semua status). Klik nama kota untuk halaman KAP, KJA, KJPP, dan konsultan pajak di kota itu, lengkap dengan daftar kantor terdaftar.</p>'
            + table + '<h2 style="margin-top:30px">Tanya Jawab</h2>' + faqh + "</main>")
    s = re.sub(r"<main.*?</main>", lambda m: main, s, count=1, flags=re.S)
    s = s.replace("</head>", CSS + f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>', 1)
    s = s.replace("</body>", '<script src="/js/izin.js" defer></script></body>', 1)
    os.makedirs(os.path.join(site_root, "cek-izin"), exist_ok=True)
    open(os.path.join(site_root, "cek-izin", "index.html"), "w", encoding="utf-8").write(s)
    sm = os.path.join(site_root, "sitemap.xml")
    if os.path.exists(sm):
        t = open(sm, encoding="utf-8").read()
        if "/cek-izin/" not in t:
            t = t.replace("</urlset>", "<url><loc>https://cariakuntan.com/cek-izin/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>")
            open(sm, "w", encoding="utf-8").write(t)
    for fn in ("llms.txt", "llms-full.txt"):
        lp = os.path.join(site_root, fn)
        if os.path.exists(lp):
            t = open(lp, encoding="utf-8").read()
            if "/cek-izin/" not in t:
                t = t.rstrip("\n") + "\n\n## Cek izin profesi keuangan\n- [Cek Izin KAP, KJA, KJPP, Konsultan Pajak, Penilai Publik](https://cariakuntan.com/cek-izin/): pencarian nama dan nomor izin dari registri PPPK Kemenkeu, diperbarui tiap bulan; daftar per kota ada di tiap halaman /kota/<kota>/.\n"
                open(lp, "w", encoding="utf-8").write(t)
    return True

def link_home(site_root):
    """Tambah link /cek-izin/ di tabel kredensial beranda CariAkuntan (4 bahasa) dan link cek izin di blok beranda."""
    n = 0
    for rel in ("index.html", "en/index.html", "zh/index.html", "hokkien/index.html"):
        p = os.path.join(site_root, rel)
        if not os.path.exists(p): continue
        s = open(p, encoding="utf-8").read()
        if "/cek-izin/" in s: continue
        lab = {"index.html": "Cari semua KAP, KJA, KJPP, dan konsultan pajak berizin di Indonesia", "en/index.html": "Search every licensed KAP, KJA, KJPP, and tax consultant in Indonesia"}.get(rel, "Cari semua KAP, KJA, KJPP, dan konsultan pajak berizin di Indonesia")
        s2 = s.replace('href="https://find-profkeu.kemenkeu.go.id/Ap/PeriksaKap" target="_blank" rel="noopener nofollow">',
                       'href="/cek-izin/">', 1) if 'href="https://find-profkeu.kemenkeu.go.id/Ap/PeriksaKap" target="_blank" rel="noopener nofollow">' in s else s
        if s2 == s:
            k = s.rfind("</main>")
            if k < 0: continue
            s2 = s[:k] + f'<p style="margin:18px 0 0"><a class="btn btn-line" href="/cek-izin/">{E(lab)}</a></p>' + s[k:]
        open(p, "w", encoding="utf-8").write(s2); n += 1
    return n

def apply(out_dir):
    reg = load()
    if not reg:
        print("izin: registry.json belum ada, dilewati"); return 0
    idx = city_index(reg); names = city_names(); n = 0
    ca = os.path.join(out_dir, "cariakuntan")
    if os.path.isdir(ca):
        ensure_assets(ca, reg)
        kota = os.path.join(ca, "kota")
        for sl in sorted(os.listdir(kota)) if os.path.isdir(kota) else []:
            d = os.path.join(kota, sl)
            if not os.path.isdir(d): continue
            city = names.get(sl) or " ".join(w.capitalize() for w in sl.split("-"))
            if os.path.exists(os.path.join(d, "index.html")) and inject(os.path.join(d, "index.html"), block(reg, idx, city, None, "ca"), "ca-scr"): n += 1
            for sub, pre in PRE.items():
                p = os.path.join(d, sub, "index.html")
                if os.path.exists(p) and inject(p, block(reg, idx, city, pre, "ca"), "ca-scr"): n += 1
        hub_page(ca, reg, idx, names); link_home(ca)
    fa = os.path.join(out_dir, "faindonesia")
    if os.path.isdir(fa):
        ensure_assets(fa, reg)
        wil = os.path.join(fa, "wilayah")
        for sl in sorted(os.listdir(wil)) if os.path.isdir(wil) else []:
            p = os.path.join(wil, sl, "index.html")
            if not os.path.exists(p): continue
            city = names.get(sl) or " ".join(w.capitalize() for w in sl.split("-"))
            if inject(p, block(reg, idx, city, None, "fa"), "fa-cari"): n += 1
    print("izin: blok cek izin di", n, "halaman; registri", reg.get("updated"))
    return n

if __name__ == "__main__":
    apply(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "out"))
