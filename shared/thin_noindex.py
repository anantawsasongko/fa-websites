"""Noindex halaman programatik tipis + keluarkan dari sitemap (4 Nov 2026).

Aturan:
- cariakuntan: /kdmp/<prov>/<kab>/<desa>/ (level 3) dan /kota/<kota>/kecamatan/<kec>/ -> noindex,follow
- faindonesia: /wilayah/<kota>/kecamatan/<kec>/ -> noindex,follow; sitemap-kecamatan.xml tidak diiklankan
Hub (provinsi, kabupaten, kota, kota x layanan) tetap index.
Idempoten. Dipanggil dari prep.py setelah semua build.
"""
import os, re

META = '<meta name="robots" content="noindex,follow">'
RULES = {
    "cariakuntan": [re.compile(r"^kdmp/[^/]+/[^/]+/[^/]+/index\.html$"),
                    re.compile(r"^kota/[^/]+/kecamatan/[^/]+/index\.html$")],
    "faindonesia": [re.compile(r"^wilayah/[^/]+/kecamatan/[^/]+/index\.html$")],
}
DOMAIN = {"cariakuntan": "https://cariakuntan.com", "faindonesia": "https://faindonesia.co.id"}


def _url(site, rel):
    return DOMAIN[site] + "/" + rel[: -len("index.html")]


def run(out_root):
    stats = {}
    for site, pats in RULES.items():
        root = os.path.join(out_root, site)
        if not os.path.isdir(root):
            continue
        urls, n = set(), 0
        for d, _, fs in os.walk(root):
            if "index.html" not in fs:
                continue
            p = os.path.join(d, "index.html")
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            if not any(r.match(rel) for r in pats):
                continue
            urls.add(_url(site, rel))
            h = open(p, encoding="utf-8").read()
            h2 = re.sub(r'<meta name="robots"[^>]*>', META, h)
            if META not in h2:
                h2 = h2.replace("<head>", "<head>" + META, 1) if "<head>" in h2 else re.sub(r"(<head[^>]*>)", r"\1" + META, h2, 1)
            if h2 != h:
                open(p, "w", encoding="utf-8").write(h2)
                n += 1
        # sitemap utama: buang URL yang noindex
        removed = 0
        for sm in ("sitemap.xml",):
            sp = os.path.join(root, sm)
            if os.path.exists(sp):
                s = open(sp, encoding="utf-8").read()
                parts = re.split(r"(?=\s*<url>)", s)
                keep = []
                for part in parts:
                    m = re.search(r"<loc>([^<]+)</loc>", part)
                    if m and m.group(1) in urls:
                        removed += 1
                        continue
                    keep.append(part)
                s2 = "".join(keep)
                if "</urlset>" not in s2:
                    s2 = s2.rstrip() + "\n</urlset>\n"
                open(sp, "w", encoding="utf-8").write(s2)
        # sitemap-kecamatan: hapus file dan barisnya di robots.txt
        for extra in ("sitemap-kecamatan.xml",):
            ep = os.path.join(root, extra)
            if os.path.exists(ep):
                os.remove(ep)
        rp = os.path.join(root, "robots.txt")
        if os.path.exists(rp):
            r = open(rp, encoding="utf-8").read()
            r2 = re.sub(r"(?m)^Sitemap: \S*sitemap-kecamatan\.xml\s*\n?", "", r)
            if r2 != r:
                open(rp, "w", encoding="utf-8").write(r2)
        stats[site] = {"noindex_pages": len(urls), "changed": n, "removed_from_sitemap": removed}
    return stats


if __name__ == "__main__":
    import sys, json
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "out"), indent=1))


GA_SITE = {"cariakuntan": "G-ST6NBQ1D77", "updatesak": "G-ZFJDEKN947"}  # FA tetap G-09VZKH3JRJ


def ga_split(out_root, old="G-09VZKH3JRJ"):
    st = {}
    for site, new in GA_SITE.items():
        n = 0
        for d, _, fs in os.walk(os.path.join(out_root, site)):
            for f in fs:
                if f.endswith((".html", ".js")):
                    p = os.path.join(d, f)
                    try:
                        h = open(p, encoding="utf-8").read()
                    except UnicodeDecodeError:
                        continue
                    if old in h:
                        open(p, "w", encoding="utf-8").write(h.replace(old, new)); n += 1
        st[site] = n
    return st
