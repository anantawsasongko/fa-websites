"""Noindex halaman programatik tipis + keluarkan dari sitemap (4 Nov 2026).

Aturan:
- cariakuntan: /kdmp/<prov>/<kab>/<desa>/ (level 3) dan /kota/<kota>/kecamatan/<kec>/ -> noindex,follow
- faindonesia: /wilayah/<kota>/kecamatan/<kec>/ -> noindex,follow; sitemap-kecamatan.xml tidak diiklankan
Hub (provinsi, kabupaten, kota, kota x layanan) tetap index.
17 Nov 2026 (Bos: "noindex halaman tipis CA, sisakan kota, cek izin, artikel"): cariakuntan sekarang juga noindex,follow
untuk SEMUA /kdmp/ (beranda, provinsi, kabupaten, desa), hub /kota/<kota>/kecamatan/, dan semua kawasan bisnis
(/kota/<kota>/<kawasan>/ + 4 halaman layanannya). Kawasan dikenali dari struktur folder (punya anak kap/ atau kjpp/).
20 Nov 2026 (Bos setuju CA diciutkan jadi alat/direktori): cariakuntan juga noindex,follow untuk 9 halaman
layanan per kota yang isinya penawaran jasa tanpa data registri (CA_JASA di bawah, niatnya sama dengan halaman FA),
dan /kota/<kota>/{kap,kja,kjpp}/ yang daftar registrinya kosong (0 kantor aktif jenis itu di kota tersebut).
Yang tetap index: /kota/<kota>/ dan /kota/<kota>/{kap,kja,kjpp}/ yang punya daftar kantor aktif.
27 Nov 2026 (Bos: "tidak berbenturan di google"): 10 halaman pilar jasa CA (CA_PILAR) ikut noindex,follow; kueri jasa milik FA.
Idempoten. Dipanggil dari prep.py setelah semua build. Mode lokal: python3 shared/thin_noindex.py out cariakuntan [--dry]
"""
import os, re

META = '<meta name="robots" content="noindex,follow">'
CA_JASA = ("jasa-laporan-keuangan|kap-murah|konsultan-rumah-sakit|laporan-tahunan-pt|konsultan-psak|"
           "jasa-buku-besar|pendampingan-audit|akuntan-forensik|konsultan-pajak")
# 27 Nov 2026 (tiga situs, tiga niat): pilar jasa CA yang kuerinya milik FA -> noindex,follow.
CA_PILAR = ("konsultan-rumah-sakit|konsultan-psak|jasa-buku-besar|pendampingan-audit|akuntan-forensik|"
            "laporan-keuangan-sabh|jasa-pembukuan(?:/[^/]+)?|layanan/jasa-laporan-keuangan|layanan/laporan-tahunan-pt")
CA_REG = re.compile(r"^kota/[^/]+/(kap|kja|kjpp)/index\.html$")
RULES = {
    "cariakuntan": [re.compile(r"^kdmp/(?:[^/]+/)*index\.html$"),
                    re.compile(r"^kota/[^/]+/kecamatan/(?:[^/]+/)?index\.html$"),
                    re.compile(r"^kota/[^/]+/(?:%s)/index\.html$" % CA_JASA),
                    re.compile(r"^(?:%s)/index\.html$" % CA_PILAR)],
    "faindonesia": [re.compile(r"^wilayah/[^/]+/kecamatan/[^/]+/index\.html$")],
}
DOMAIN = {"cariakuntan": "https://cariakuntan.com", "faindonesia": "https://faindonesia.co.id"}


def _url(site, rel):
    return DOMAIN[site] + "/" + rel[: -len("index.html")]


def _kawasan_prefixes(root):
    """kota/<kota>/<kawasan>/ = folder yang punya anak kap/ atau kjpp/ (folder layanan tingkat kota tidak punya)."""
    kroot = os.path.join(root, "kota")
    res = set()
    if not os.path.isdir(kroot):
        return res
    for city in os.listdir(kroot):
        cp = os.path.join(kroot, city)
        if not os.path.isdir(cp):
            continue
        for s in os.listdir(cp):
            sp = os.path.join(cp, s)
            if os.path.isdir(sp) and (os.path.exists(os.path.join(sp, "kap", "index.html")) or os.path.exists(os.path.join(sp, "kjpp", "index.html"))):
                res.add("kota/%s/%s/" % (city, s))
    return res


def _reg_kosong(path, jenis):
    """True bila halaman /kota/<kota>/<jenis>/ tidak punya kantor aktif jenis itu di blok registri (pk-sum)."""
    h = open(path, encoding="utf-8").read()
    m = re.search(r'<div class="pk-sum">(.*?)</div>', h, re.S)
    if not m:
        return True
    a = re.search(r"<b>%s \d+</b> \((\d+) aktif\)" % jenis.upper(), m.group(1))
    return not a or int(a.group(1)) == 0


def run(out_root, sites=None, dry=False):
    stats = {}
    for site, pats in RULES.items():
        if sites and site not in sites:
            continue
        root = os.path.join(out_root, site)
        if not os.path.isdir(root):
            continue
        kaw = _kawasan_prefixes(root) if site == "cariakuntan" else set()
        urls, n = set(), 0
        for d, _, fs in os.walk(root):
            if "index.html" not in fs:
                continue
            p = os.path.join(d, "index.html")
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            hit = any(r.match(rel) for r in pats) or (kaw and any(rel.startswith(k) for k in kaw))
            if not hit and site == "cariakuntan":
                mr = CA_REG.match(rel)
                hit = bool(mr) and _reg_kosong(p, mr.group(1))
            if not hit:
                continue
            urls.add(_url(site, rel))
            h = open(p, encoding="utf-8").read()
            h2 = re.sub(r'<meta name="robots"[^>]*>', META, h)
            if META not in h2:
                h2 = h2.replace("<head>", "<head>" + META, 1) if "<head>" in h2 else re.sub(r"(<head[^>]*>)", r"\1" + META, h2, 1)
            if h2 != h:
                if not dry:
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
                if not dry:
                    open(sp, "w", encoding="utf-8").write(s2)
        # sitemap-kecamatan: hapus file dan barisnya di robots.txt
        for extra in ("sitemap-kecamatan.xml",):
            ep = os.path.join(root, extra)
            if os.path.exists(ep) and not dry:
                os.remove(ep)
        rp = os.path.join(root, "robots.txt")
        if os.path.exists(rp):
            r = open(rp, encoding="utf-8").read()
            r2 = re.sub(r"(?m)^Sitemap: \S*sitemap-kecamatan\.xml\s*\n?", "", r)
            if r2 != r and not dry:
                open(rp, "w", encoding="utf-8").write(r2)
        stats[site] = {"noindex_pages": len(urls), "changed": n, "removed_from_sitemap": removed}
    return stats


if __name__ == "__main__":
    import sys, json
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    print(json.dumps(run(a[0] if a else "out", a[1:] or None, "--dry" in sys.argv), indent=1))


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
