# Pusat belajar Standar Audit IAPI edisi 2025 di UpdateSAK: /standar-audit/ (hub) + /standar-audit/<slug>/ per standar.
# Data ringkasan (parafrase, bukan teks standar) di updatesak/sa_data/part_*.json. Dijalankan prep.py SETELAH build_jadwal.py.
import os, re, sys, json, html, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_seo as B
esc = html.escape
SITE = B.SITE; BASE = B.BASE
UPD_ISO = "2026-10-30"; UPD = "30 Oktober 2026"
SRC_IAPI = [("IAPI: Standar Audit 2025", "https://iapi.or.id/standar-audit-2025/"), ("IAPI: SPR, SPA, SJT 2025", "https://iapi.or.id/spr-spa-sjt-2025/"),
            ("IAPI: SA 600 dan SJT 4400", "https://iapi.or.id/sa-600-dan-sjt-4400/"), ("IAPI: Standar Profesional Akuntan Publik", "https://iapi.or.id/standar-profesional-akuntan-publik/")]
ORDER = ["Manajemen Mutu", "SA 200-299 Prinsip Umum dan Tanggung Jawab", "SA 300-499 Penilaian Risiko dan Respons", "SA 500-599 Bukti Audit",
         "SA 600-699 Menggunakan Pekerjaan Pihak Lain", "SA 700-799 Kesimpulan dan Pelaporan", "SA 800-899 Area Khusus", "Reviu, Asurans, dan Jasa Terkait"]
WARNA = dict(zip(ORDER, ["#7C3AED", "#1F5BFF", "#12A39A", "#0EA5E9", "#F59E0B", "#E11D48", "#0B1F33", "#16A34A"]))

S = []
for f in sorted(glob.glob(os.path.join(HERE, "sa_data", "part_*.json"))):
    S += json.load(open(f, encoding="utf-8"))
for s in S:
    s["judul"] = re.sub(r"\s*\(judul perlu dicek\)", "", s["judul"]).strip()
    if s["seri"] not in ORDER: s["seri"] = ORDER[-1]
def key(s):
    m = re.search(r"(\d+)", s["kode"]); n = int(m.group(1)) if m else 0
    return (ORDER.index(s["seri"]), 0 if s["kode"].startswith("SMM") else 1, n)
S.sort(key=key)

CSS = """<style>
.sagrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:14px 0 30px}
.sacard{display:flex;flex-direction:column;gap:5px;border:1px solid #d5dbe5;border-left:4px solid var(--c);padding:14px 16px;text-decoration:none;color:inherit;background:#fff}
.sacard b{font-size:15px;letter-spacing:.02em;color:var(--c)}.sacard span{font-size:14.5px;line-height:1.45;color:#0B1F33}.sacard small{font-size:12.5px;color:#5b6576}
.sanav{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 8px}.sanav a{border:1px solid #d5dbe5;padding:7px 13px;border-radius:999px;font-weight:600;font-size:13.5px;text-decoration:none;color:inherit}
.sabox{border-left:4px solid var(--c);background:#f5f7fb;padding:12px 16px;margin:14px 0}
.sanew{border:1px solid #F59E0B;background:#fff8eb;padding:12px 16px;margin:14px 0;color:#0B1F33}
.saprev{display:flex;justify-content:space-between;gap:12px;margin:28px 0 8px;flex-wrap:wrap}.saprev a{font-weight:600}
@media (prefers-color-scheme:dark){.sacard{background:#0f1a28;border-color:#26364a}.sacard span{color:#e8edf5}.sacard small{color:#9fb0c5}.sanav a{border-color:#26364a}.sabox{background:#0f1a28;color:#e8edf5}.sanew{background:#2a2112;color:#f3e6cc}}
</style>"""

def card(s, base=""):
    return (f'<a class="sacard" href="{base}/standar-audit/{s["slug"]}/" style="--c:{WARNA[s["seri"]]}"><b>{esc(s["kode"])}</b>'
            f'<span>{esc(s["judul"])}</span><small>{esc(s["judul_en"])}</small></a>')

def li(xs): return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in xs) + "</ul>"

def page(i, s):
    path = f"standar-audit/{s['slug']}"; url = f"{BASE}/{path}/"; k = "sa-" + s["slug"]
    img = f"{BASE}/img/share/{k}-og.jpg"
    title = f"{s['kode']} {s['judul']}: Ringkasan dan Poin Kunci"
    desc = (f"{s['kode']} {s['judul']}: ringkasan, poin kunci, praktik kertas kerja, dan temuan reviu mutu. Catatan belajar edisi 2025.")[:300]
    crumbs = [("UpdateSAK", BASE + "/"), ("Standar Audit", BASE + "/standar-audit/"), (s["kode"], url)]
    faq = [tuple(x) for x in s.get("faq", [])]
    ld = json.loads(B.ld_graph(url, title, desc, crumbs, faq, img))
    for g in ld["@graph"]:
        if g["@type"] == "Article": g["datePublished"] = g["dateModified"] = UPD_ISO
    prev = S[i - 1] if i > 0 else None; nxt = S[i + 1] if i + 1 < len(S) else None
    rel = [x for x in S if x["seri"] == s["seri"] and x["slug"] != s["slug"]][:6]
    psak = "".join(B.chip(n) for n in s.get("psak", []))
    out = f'''{CSS}<article class="art"><div class="wrap">
<nav class="crumb"><a href="/">Beranda</a> / <a href="/standar-audit/">Standar Audit</a> / {esc(s["kode"])}</nav>
<p class="label">{esc(s["seri"])}</p>
<h1>{esc(s["kode"])} {esc(s["judul"])}</h1>
<p class="lede">{esc(s["ringkas"])}</p>
<p class="upd">Tim UpdateSAK · Catatan belajar edisi 2025 · Diperbarui {UPD} · Padanan: {esc(s["judul_en"])}</p>
{B.share(url, s["kode"] + " " + s["judul"], k)}
<div class="prose">
<div class="sabox" style="--c:{WARNA[s["seri"]]}"><b>Tujuan Auditor:</b> {esc(s["tujuan"])}</div>
{f'<div class="sanew"><b>Yang Baru di Edisi 2025:</b> {esc(s["baru2025"])}</div>' if s.get("baru2025") else ""}
<h2>Poin Kunci</h2>{li(s["poin"])}
<h2>Praktik di Kertas Kerja</h2>{li(s["praktik"])}
<h2>Temuan Reviu Mutu yang Sering Muncul</h2>{li(s["temuan"])}
<p><i>Catatan ini adalah ringkasan untuk belajar, bukan pengganti teks standar. Untuk pekerjaan perikatan, rujuk dokumen resmi IAPI di <a href="https://iapi.or.id/standar-audit-2025/" target="_blank" rel="noopener">iapi.or.id</a>.</i></p>
</div>
{('<h2>PSAK Terkait</h2><div class="pchips">' + psak + '</div>') if psak else ""}
{B.faq_html(faq)}
<div class="saprev">{f'<a href="/standar-audit/{prev["slug"]}/">← {esc(prev["kode"])}</a>' if prev else "<span></span>"}<a href="/standar-audit/">Semua Standar</a>{f'<a href="/standar-audit/{nxt["slug"]}/">{esc(nxt["kode"])} →</a>' if nxt else "<span></span>"}</div>
{('<h2>Standar Lain di Kelompok Ini</h2><div class="sagrid">' + "".join(card(x) for x in rel) + "</div>") if rel else ""}
{B.cta("Latihan Menyusun Laporan Keuangan dan CALK")}
</div></article>
'''
    B.write(path, B.HEAD.format(title=esc(title + " | UpdateSAK"), desc=esc(desc), url=url, ogt=esc(title), img=img, ld=json.dumps(ld, ensure_ascii=False)) + out + B.FOOT)
    B.make_images(k, s["kode"], s["judul"])
    return url

def hub():
    url = f"{BASE}/standar-audit/"; img = f"{BASE}/img/share/standar-audit-og.jpg"
    title = "Standar Audit IAPI 2025: Ringkasan SA, SMM, SPR, SPA, dan SJT"
    desc = "Catatan belajar Standar Audit IAPI edisi 2025: SA 200 sampai SA 810, manajemen mutu, reviu, asurans, dan jasa terkait. Poin kunci, kertas kerja, temuan reviu mutu."
    faq = [("Apa yang baru di Standar Audit IAPI 2025?", "Edisi 2025 mengacu Handbook IAASB 2023-2024: penyesuaian akibat standar manajemen mutu, SA 315 revisi 2019, SA 600 revisi untuk audit grup, amendemen terbatas SA 700 dan SA 260 terkait pengungkapan independensi entitas kepentingan publik, serta SJT 4400 revisi untuk prosedur yang disepakati."),
           ("Kapan SA 600 revisi berlaku?", "SA 600 revisi berlaku untuk audit laporan keuangan grup periode yang dimulai pada atau setelah 31 Desember 2025, dengan penerapan dini diizinkan."),
           ("Di mana mengunduh teks resmi Standar Audit?", "Teks resmi diterbitkan IAPI dan tersedia melalui halaman Standar Audit 2025 di iapi.or.id. Halaman UpdateSAK berisi ringkasan untuk belajar, bukan pengganti teks standar.")]
    crumbs = [("UpdateSAK", BASE + "/"), ("Standar Audit", url)]
    ld = json.loads(B.ld_graph(url, title, desc, crumbs, faq, img))
    for g in ld["@graph"]:
        if g["@type"] == "Article": g["datePublished"] = g["dateModified"] = UPD_ISO
    groups = [g for g in ORDER if any(s["seri"] == g for s in S)]
    gid = lambda g: re.sub(r"[^a-z0-9]+", "-", g.lower()).strip("-")
    body = "".join(f'<h2 id="{gid(g)}">{esc(g)}</h2><div class="sagrid">' + "".join(card(s) for s in S if s["seri"] == g) + "</div>" for g in groups)
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in SRC_IAPI)
    out = f'''{CSS}<article class="art"><div class="wrap">
<nav class="crumb"><a href="/">Beranda</a> / Standar Audit</nav>
<p class="label">Belajar Audit · Edisi 2025</p>
<h1>Standar Audit IAPI 2025: Ringkasan untuk Auditor</h1>
<p class="lede">{len(S)} standar dalam satu tempat: manajemen mutu, SA 200 sampai SA 810, reviu, asurans, dan jasa terkait. Setiap halaman berisi tujuan, poin kunci, praktik kertas kerja, dan temuan reviu mutu yang sering muncul.</p>
<p class="upd">Tim UpdateSAK · Diperbarui {UPD}</p>
{B.share(url, title, "standar-audit")}
<div class="sanew"><b>Yang Baru di Edisi 2025:</b> mengacu Handbook IAASB 2023-2024. Penyesuaian dari standar manajemen mutu, SA 315 revisi 2019, dan SA 600 revisi (audit grup, berlaku periode yang dimulai pada atau setelah 31 Desember 2025), amendemen terbatas SA 700 dan SA 260 tentang pengungkapan independensi entitas kepentingan publik, serta SJT 4400 revisi (prosedur yang disepakati).</div>
<div class="sanav">{"".join(f'<a href="#{gid(g)}">{esc(g.split(" ")[0] + " " + g.split(" ")[1] if g.startswith("SA ") else g)}</a>' for g in groups)}</div>
{body}
<h2>Cara Memakai Halaman Ini</h2>
<div class="prose"><ol>
<li><b>Belajar ujian CPA dan CA:</b> mulai dari SA 200, SA 315, SA 320, SA 330, SA 500, lalu SA 700 dan SA 705. Kelompok ini paling sering keluar di mata ujian Audit dan Asurans.</li>
<li><b>Auditor junior:</b> fokus pada Praktik di Kertas Kerja di setiap halaman untuk tahu apa yang perlu didokumentasikan.</li>
<li><b>Senior dan manajer:</b> cek bagian Temuan Reviu Mutu sebelum file perikatan ditutup.</li>
<li><b>Latihan angka:</b> pakai <a href="/#kalkulator">Kalkulator Standar Akuntansi</a> dan <a href="/materi/">Materi Studi Kasus</a> untuk menghubungkan standar audit dengan PSAK.</li>
</ol></div>
{B.faq_html(faq)}
<h2>Sumber Resmi</h2><ul class="exsrc">{src}</ul>
<p class="upd">Ringkasan disusun ulang dengan bahasa sendiri untuk tujuan belajar. Teks resmi dan judul baku mengikuti terbitan IAPI.</p>
{B.wa_box("Audit")}
</div></article>
'''
    B.write("standar-audit", B.HEAD.format(title=esc(title + " | UpdateSAK"), desc=esc(desc), url=url, ogt=esc(title), img=img, ld=json.dumps(ld, ensure_ascii=False)) + out + B.FOOT)
    B.make_images("standar-audit", "Belajar Audit 2025", "Standar Audit IAPI 2025: Ringkasan untuk Auditor")
    return url

HOME = '''<!--sa:start-->
<section class="alt" id="standar-audit"><div class="wrap">
  <div class="head"><h2>Belajar Standar Audit IAPI 2025</h2><p>{n} standar: SA 200 sampai SA 810, manajemen mutu, reviu, asurans, dan jasa terkait. Ringkasan, poin kunci, kertas kerja, dan temuan reviu mutu.</p></div>
  <div class="sagrid">{cards}</div>
  <p><a class="btn arrow" href="/standar-audit/">Lihat Semua Standar Audit</a></p>
</div></section>
<!--sa:end-->'''

def wire(urls):
    p = os.path.join(SITE, "index.html"); s = open(p, encoding="utf-8").read()
    pick = [x for x in S if x["kode"] in ("SA 315", "SA 320", "SA 540", "SA 600", "SA 701", "SA 705")]
    blk = HOME.format(n=len(S), cards="".join(card(x) for x in pick))
    s = re.sub(r'<style id="sacss">.*?</style>', "", s, flags=re.S)
    s = s.replace("</head>", CSS.replace("<style>", '<style id="sacss">') + "</head>", 1)
    if "<!--sa:start-->" in s: s = re.sub(r"<!--sa:start-->.*?<!--sa:end-->", lambda m: blk, s, flags=re.S)
    else:
        i = s.find("<!--jadwal:start-->")
        if i < 0: i = s.find('<section class="final">')
        s = s[:i] + blk + "\n\n" + s[i:]
    if '/standar-audit/">Standar Audit</a>' not in s:
        s = s.replace('<a href="/jadwal-ujian/">Jadwal Ujian</a> · <a href="mailto:', '<a href="/jadwal-ujian/">Jadwal Ujian</a> · <a href="/standar-audit/">Standar Audit</a> · <a href="mailto:', 1)
    open(p, "w", encoding="utf-8").write(s)
    # Eksplor: tautan di atas
    p = os.path.join(SITE, "eksplor", "index.html"); s = open(p, encoding="utf-8").read()
    s = re.sub(r"<!--sa-eks-->.*?<!--/sa-eks-->", "", s, flags=re.S)
    k = s.find("<!--seo:start-->")
    if k > 0:
        s = s[:k] + f'<!--sa-eks--><section><div class="wrap"><aside class="cta-box"><div><b>Baru: Standar Audit IAPI 2025</b><span>{len(S)} ringkasan standar untuk auditor dan peserta ujian CPA/CA.</span></div><a class="btn arrow" href="/standar-audit/">Buka Standar Audit</a></aside></div></section><!--/sa-eks-->' + s[k:]
    open(p, "w", encoding="utf-8").write(s)
    p = os.path.join(SITE, "sitemap.xml"); s = re.sub(r"<!--sa-->.*?<!--/sa-->\n?", "", open(p).read(), flags=re.S)
    s = s.replace("</urlset>", "<!--sa-->\n" + "".join(f"<url><loc>{u}</loc><lastmod>{UPD_ISO}</lastmod></url>\n" for u in urls) + "<!--/sa-->\n</urlset>")
    open(p, "w").write(s)
    p = os.path.join(SITE, "llms.txt"); s = open(p, encoding="utf-8").read().split("\n## Standar Audit IAPI 2025")[0].rstrip()
    s += "\n\n## Standar Audit IAPI 2025\n" + f"- [Standar Audit IAPI 2025: Ringkasan untuk Auditor]({BASE}/standar-audit/)\n" + "".join(f"- [{x['kode']} {x['judul']}]({BASE}/standar-audit/{x['slug']}/): {x['ringkas']}\n" for x in S)
    open(p, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    urls = [hub()] + [page(i, s) for i, s in enumerate(S)]
    wire(urls); print("standar audit:", len(S), "halaman")
