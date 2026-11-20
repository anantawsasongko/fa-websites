#!/usr/bin/env python3
"""Rampingkan link silang FA/CA/US dan tombol WA di CA/US (20 Nov 2026).

Pemicu (Bos, 20 Nov): CA dan US gagal jadi penunjang lead; keduanya tenggelam di Google sejak 9 Nov.
Keputusan: tiga situs jangan saling membebani. Link silang massal dilepas, CA dan US cukup satu tombol WA
utama per halaman, daftar registri CA naik ke atas, dan kartu KAP/KJA di CA/US mengarah ke halaman layanan FA.

BEKERJA LANGSUNG DI out/ (faindonesia, cariakuntan, updatesak). Idempoten. Jalankan PALING AKHIR
(setelah semua generator FA, CA, US), lalu `python3 shared/thin_noindex.py out cariakuntan`.

  python3 caus_ramping_20261120.py [--dry]

Yang dikerjakan:
1. Tiga situs: baris "Ekosistem FA" (ecobar) di atas header dibuang.
2. FA: link footer Cari Akuntan dan Update SAK dibuang di semua halaman kecuali beranda.
3. CA: footer tanpa Toko dan Update SAK; "dikelola oleh FA Indonesia" tetap tertulis tetapi hanya jadi link di
   beranda (ID/EN/ZH/Hokkien); Kebijakan Privasi rel="nofollow"; link artikel UpdateSAK di halaman /kdmp/ dibuang.
   Kotak ca-tanya (3 chip WA) dan pk-cta dibuang. Di /kota/<kota>/ dan /kota/<kota>/{kap,kja,kjpp}/ daftar
   registri (blok pk) dipindah ke tepat di bawah hero. Tombol kartu KAP DHN dan KJA Farhani jadi link ke
   halaman audit / penyusunan LK FA (versi kota bila ada).
4. US: footer tanpa CariAkuntan dan Toko. Kotak us-tanya dibuang. Di halaman yang punya blok fa-cta2,
   tombol WA hero dan kotak cta-box gelap dibuang (WA cukup di fa-cta2). Strip KAP/KJA jadi link ke FA.
Tidak mengubah title, description, H1, canonical, JSON-LD, URL, atau isi artikel.
"""
import os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DRY = "--dry" in sys.argv

ECO = re.compile(r'<div class="ecobar"[^>]*>.*?</div></div>\s?', re.S)
FA_AUDIT = "https://faindonesia.co.id/jasa-audit-laporan-keuangan/"
FA_LK = "https://faindonesia.co.id/jasa-penyusunan-laporan-keuangan/"
LBL_AUDIT = "Lihat Layanan Audit"
LBL_LK = "Lihat Layanan Laporan Keuangan"

st = collections.Counter()


def footer_sub(h, pats, key):
    """Hapus link tertentu hanya di dalam <footer>."""
    i = h.rfind("<footer")
    if i < 0:
        return h
    j = h.find("</footer>", i)
    if j < 0:
        return h
    f = h[i:j]
    f2 = f
    for p in pats:
        f2, n = p.subn("", f2)
        st[key] += n
    return h[:i] + f2 + h[j:] if f2 != f else h


DHN = re.compile(r"<!--dhn-->.*?<!--/dhn-->", re.S)
DHNB = re.compile(r'<a class="dhnb"[^>]*>[^<]*</a>')


def dhn_to_fa(h, city=None):
    def fix(m):
        b = m.group(0)
        k = re.search(r'class="dhn[cs] kja"|aria-label="KJA', b)
        cut = k.start() if k else len(b)

        def rep(a):
            if "wa.me" not in a.group(0):
                return a.group(0)
            lk = a.start() >= cut
            base, lbl, fam = (FA_LK, LBL_LK, "jasa-penyusunan-laporan-keuangan") if lk else (FA_AUDIT, LBL_AUDIT, "jasa-audit-laporan-keuangan")
            url = base
            if city and os.path.exists(os.path.join(OUT, "faindonesia", fam, city, "index.html")):
                url = base + city + "/"
            st["dhn_link"] += 1
            return '<a class="dhnb" href="%s" data-fa-out="%s">%s</a>' % (url, "lk" if lk else "audit", lbl)

        return DHNB.sub(rep, b)

    return DHN.sub(fix, h)


# ---------- FA ----------
FA_FOOT = [re.compile(r'<li><a href="https://cariakuntan\.com/">Cari Akuntan</a></li>'),
           re.compile(r'<li><a href="https://updatesak\.com/">Update SAK</a></li>')]


def do_fa(rel, h):
    h, n = ECO.subn("", h)
    st["fa_ecobar"] += n
    if rel != "index.html":
        h = footer_sub(h, FA_FOOT, "fa_footer")
    return h


# ---------- CA ----------
CA_FOOT = [re.compile(r'\s*·\s*<a href="https://faindonesia\.co\.id/toko/[^"]*">[^<]*</a>'),
           re.compile(r'\s*·\s*<a href="https://updatesak\.com/">[^<]*</a>')]
CA_TANYA = re.compile(r"<!--ca-tanya-->.*?<!--/ca-tanya-->", re.S)
PK = re.compile(r"<!--pk-->.*?<!--/pk-->", re.S)
PK_CTA = re.compile(r'<div class="pk-cta">.*?</div>', re.S)
HERO_END = "<!--/rx17s--></header>"
KOTA = re.compile(r"^kota/([^/]+)/(?:(kap|kja|kjpp)/)?index\.html$")
KOTA_ANY = re.compile(r"^kota/([^/]+)/")
CA_HOME = ("index.html", "en/index.html", "zh/index.html", "hokkien/index.html")
CA_OWN = [re.compile(r'<a href="https://faindonesia\.co\.id/">(FA Indonesia)</a>')]
CA_PRIV = re.compile(r'<a href="https://faindonesia\.co\.id/kebijakan-privasi/">')
CA_KDMP_US = re.compile(r'\s*·\s*<a href="https://updatesak\.com/artikel/sak-untuk-kdkmp[^"]*">[^<]*</a>')


def footer_unlink(h, pats, key):
    i = h.rfind("<footer")
    j = h.find("</footer>", i) if i >= 0 else -1
    if j < 0:
        return h
    f = h[i:j]
    f2 = f
    for p in pats:
        f2, n = p.subn(r"\1", f2)
        st[key] += n
    return h[:i] + f2 + h[j:] if f2 != f else h


def do_ca(rel, h):
    h, n = ECO.subn("", h)
    st["ca_ecobar"] += n
    h = footer_sub(h, CA_FOOT, "ca_footer")
    if rel not in CA_HOME:
        h = footer_unlink(h, CA_OWN, "ca_footer_pemilik")
    h, n = CA_PRIV.subn('<a href="https://faindonesia.co.id/kebijakan-privasi/" rel="nofollow">', h)
    st["ca_privasi_nofollow"] += n
    if rel.startswith("kdmp/"):
        h, n = CA_KDMP_US.subn("", h)
        st["ca_kdmp_us"] += n
    h, n = CA_TANYA.subn("", h)
    st["ca_tanya"] += n
    h, n = PK_CTA.subn("", h)
    st["ca_pkcta"] += n
    if KOTA.match(rel) and HERO_END in h:
        m = PK.search(h)
        if m:
            blk = m.group(0)
            rest = h[:m.start()] + h[m.end():]
            i = rest.find(HERO_END) + len(HERO_END)
            h2 = rest[:i] + blk + rest[i:]
            if h2 != h:
                st["ca_pk_naik"] += 1
            h = h2
    c = KOTA_ANY.match(rel)
    h = dhn_to_fa(h, c.group(1) if c else None)
    return h


# ---------- US ----------
US_FOOT = [re.compile(r'\s*·\s*<a href="https://cariakuntan\.com/">[^<]*</a>'),
           re.compile(r'<a href="https://faindonesia\.co\.id/toko/[^"]*">[^<]*</a>\s*·\s*')]
US_TANYA = re.compile(r"<!--us-tanya-->.*?<!--/us-tanya-->", re.S)
US_HERO_WA = re.compile(r'<a class="btn" href="https://wa\.me/[^"]*"[^>]*data-us-q="hero"[^>]*>[^<]*</a>')
US_CTABOX = re.compile(r'<aside class="cta-box dark">(?:(?!</aside>).)*?wa\.me(?:(?!</aside>).)*?</aside>\s?', re.S)


def do_us(rel, h):
    h, n = ECO.subn("", h)
    st["us_ecobar"] += n
    h = footer_sub(h, US_FOOT, "us_footer")
    h, n = US_TANYA.subn("", h)
    st["us_tanya"] += n
    if 'class="fa-cta2"' in h:
        h, n = US_HERO_WA.subn("", h)
        st["us_hero_wa"] += n
        h, n = US_CTABOX.subn("", h)
        st["us_ctabox"] += n
    h = dhn_to_fa(h)
    return h


def walk(site, fn):
    root = os.path.join(OUT, site)
    ch = 0
    for d, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith(".html"):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            try:
                h = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            h2 = fn(rel, h)
            if h2 != h:
                ch += 1
                if not DRY:
                    open(p, "w", encoding="utf-8").write(h2)
    st[site + "_files"] = ch


if __name__ == "__main__":
    walk("faindonesia", do_fa)
    walk("cariakuntan", do_ca)
    walk("updatesak", do_us)
    for k in sorted(st):
        print(k, st[k])
    print("DRY" if DRY else "DITULIS")
