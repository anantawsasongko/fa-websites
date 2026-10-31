# Halaman kata kunci UpdateSAK (31 Okt 2026): /update-sak-emkm/, /update-sak-ep/, /update-psak-terbaru/, /update-sak-syariah-terbaru/,
# /update-isak-terbaru/, /update-sak-2027/, /penomoran-psak-baru/ dari updatesak/landing_data.json. Blok beranda + Eksplor, sitemap, llms.
# Dijalankan prep.py setelah build_sa.py, sebelum build_jadwal.py.
import os, re, sys, json, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_seo as B
esc = html.escape
SITE = B.SITE; BASE = B.BASE
UPD_ISO = "2026-10-31"; UPD = "31 Oktober 2026"
L = json.load(open(os.path.join(HERE, "landing_data.json"), encoding="utf-8"))

def page(a):
    url = f"{BASE}/{a['slug']}/"; k = "lp-" + a["slug"]; img = f"{BASE}/img/share/{k}-og.jpg"
    faq = [tuple(x) for x in a["faq"]]
    ld = json.loads(B.ld_graph(url, a["h1"], a["desc"], [("UpdateSAK", BASE + "/"), (a["kw"], url)], faq, img))
    for g in ld["@graph"]:
        if g["@type"] == "Article": g["datePublished"] = g["dateModified"] = UPD_ISO
    body = re.sub(r'<table>', '<div class="scroll"><table class="tbl">', a["body"]).replace("</table>", "</table></div>")
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in a.get("sources", []))
    others = "".join(f'<a href="/{x["slug"]}/"><b>{esc(x["kw"])}</b><small>{esc(x["desc"][:100])}…</small></a>' for x in L if x["slug"] != a["slug"])
    out = f'''<article class="art"><div class="wrap">
<nav class="crumb"><a href="/">Beranda</a> / {esc(a["kw"])}</nav>
<p class="label">Update SAK · Diperbarui {UPD}</p>
<h1>{esc(a["h1"])}</h1>
<p class="lede">{esc(a["lede"])}</p>
<p class="upd">Tim UpdateSAK · Diperbarui {UPD}</p>
{B.share(url, a["h1"], k)}
<div class="prose">{body}</div>
{B.cta("Cek Standar yang Berlaku untuk Perusahaan Anda")}
{B.faq_html(faq)}
<h2>Update SAK Lainnya</h2><div class="reads">{others}</div>
{('<h2>Sumber</h2><ul>' + src + '</ul>') if src else ""}
{B.wa_box("Laporan Keuangan")}
</div></article>
'''
    title = a["title"] if "UpdateSAK" in a["title"] else a["title"] + " | UpdateSAK"
    B.write(a["slug"], B.HEAD.format(title=esc(title), desc=esc(a["desc"]), url=url, ogt=esc(a["h1"]), img=img, ld=json.dumps(ld, ensure_ascii=False)) + out + B.FOOT)
    B.make_images(k, "Update SAK", a["h1"])
    return url

def wire(urls):
    links = "".join(f'<a class="need" href="/{a["slug"]}/"><b>{esc(a["kw"])}</b><small>{esc(a["lede"][:70])}…</small><em>Baca</em></a>' for a in L)
    blk = f'''<!--lp:start-->
<section id="update-sak"><div class="wrap">
  <div class="head"><h2>Update SAK Terbaru</h2><p>Update SAK EMKM, SAK EP, PSAK, ISAK, dan SAK Syariah dalam satu tempat. Diperbarui {UPD}.</p></div>
  <div class="needs">{links}</div>
</div></section>
<!--lp:end-->'''
    p = os.path.join(SITE, "index.html"); s = open(p, encoding="utf-8").read()
    if "<!--lp:start-->" in s: s = re.sub(r"<!--lp:start-->.*?<!--lp:end-->", lambda m: blk, s, flags=re.S)
    else:
        i = s.find("<!--sa:start-->")
        if i < 0: i = s.find('<section class="final">')
        s = s[:i] + blk + "\n\n" + s[i:]
    open(p, "w", encoding="utf-8").write(s)
    p = os.path.join(SITE, "eksplor", "index.html"); s = open(p, encoding="utf-8").read()
    s = re.sub(r"<!--lp-eks-->.*?<!--/lp-eks-->", "", s, flags=re.S)
    k = s.find("<!--seo:start-->")
    if k > 0:
        s = s[:k] + '<!--lp-eks--><section><div class="wrap"><div class="head"><h2>Update SAK Terbaru</h2></div><div class="reads">' + "".join(f'<a href="/{a["slug"]}/"><b>{esc(a["h1"])}</b><small>{esc(a["desc"][:110])}…</small></a>' for a in L) + '</div></div></section><!--/lp-eks-->' + s[k:]
    open(p, "w", encoding="utf-8").write(s)
    p = os.path.join(SITE, "sitemap.xml"); s = re.sub(r"<!--lp-->.*?<!--/lp-->\n?", "", open(p).read(), flags=re.S)
    s = s.replace("</urlset>", "<!--lp-->\n" + "".join(f"<url><loc>{u}</loc><lastmod>{UPD_ISO}</lastmod><priority>0.9</priority></url>\n" for u in urls) + "<!--/lp-->\n</urlset>")
    open(p, "w").write(s)
    p = os.path.join(SITE, "llms.txt"); s = open(p, encoding="utf-8").read().split("\n## Update SAK Terbaru")[0].rstrip()
    s += "\n\n## Update SAK Terbaru\n" + "".join(f"- [{a['h1']}]({BASE}/{a['slug']}/): {a['desc']}\n" for a in L)
    open(p, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    urls = [page(a) for a in L]; wire(urls); print("landing update sak:", len(urls))
