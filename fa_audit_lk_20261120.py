#!/usr/bin/env python3
"""20 Nov 2026: frasa "audit LK" di 543 halaman audit daerah FA.

Bekerja di out/ (pola blok berpenanda). Idempoten. --dry hanya menghitung.
FA  : title, og/twitter title, description (bila muat <=158), eyebrow, kalimat pembuka hero.
      H1, URL, JSON-LD, isi lain tidak diubah. Penanda <!--fa-alk--> di head.
CA  : TIDAK disentuh (keputusan 20 Nov: tidak menambah link silang massal di CA/US;
      kartu CA sudah menaut ke halaman audit FA kota yang sama lewat caus_ramping_20261120.py).
Jalankan PALING AKHIR (sesudah fa_ctr_daerah, fa_audit_stat, caus_*), karena generator lama
menulis title lama.
"""
import glob, html, os, re, sys

DRY = "--dry" in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(ROOT, "out", "faindonesia", "jasa-audit-laporan-keuangan")
MARK = "<!--fa-alk-->"


def new_title(old):
    m = re.match(r"(?:Jasa )?Audit Laporan Keuangan (.+?)(?::.*)?$", old)
    if not m:
        return None
    nama = m.group(1).strip()
    for t in (
        f"Jasa Audit LK {nama}: Audit Laporan Keuangan KAP OJK",
        f"Jasa Audit LK {nama}: KAP Terdaftar OJK",
        f"Jasa Audit LK {nama}: KAP OJK",
        f"Jasa Audit LK {nama}",
    ):
        if len(t) <= 60:
            return t
    return f"Jasa Audit LK {nama}"


def new_desc(old):
    raw = html.unescape(old)
    for a, b in (
        ("Jasa audit di ", "Jasa audit LK di "),
        ("Audit laporan keuangan ", "Audit LK (laporan keuangan) "),
        ("Butuh laporan keuangan audited di ", "Butuh audit LK di "),
    ):
        if raw.startswith(a):
            cand = b + raw[len(a):]
            if len(cand) <= 158:
                return html.escape(cand, quote=True)
    return None


def set_meta(s, key, val):
    """Ganti content pada <meta ... name|property="key" ...> apa pun urutan atributnya."""
    def rep(m):
        return re.sub(r'content="[^"]*"', lambda _: f'content="{val}"', m.group(0), count=1)
    return re.sub(r'<meta[^>]*(?:name|property)="%s"[^>]*>' % re.escape(key), rep, s)


def do_fa():
    n = dict(file=0, title=0, desc=0, eyebrow=0, hero=0, skip=0)
    names = {}
    for f in sorted(glob.glob(os.path.join(FA, "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(f))
        s = open(f, encoding="utf8").read()
        m = re.search(r'<p class="eyebrow">[^<]*?·\s*([^<]+)</p>', s)
        if m:
            names[slug] = html.unescape(m.group(1)).strip()
        if MARK in s:
            n["skip"] += 1
            continue
        o = s
        mt = re.search(r"<title>(.*?)</title>", s)
        t = new_title(html.unescape(mt.group(1))) if mt else None
        if t:
            te = html.escape(t, quote=True)
            s = s.replace(mt.group(0), f"<title>{te}</title>{MARK}", 1)
            s = set_meta(s, "og:title", te)
            s = set_meta(s, "twitter:title", te)
            n["title"] += 1
        md = re.search(r'<meta[^>]*name="description"[^>]*>', s)
        if md:
            old = re.search(r'content="([^"]*)"', md.group(0)).group(1)
            d = new_desc(old)
            if d:
                for k in ("description", "og:description", "twitter:description"):
                    s = set_meta(s, k, d)
                n["desc"] += 1
        s2 = s.replace('<p class="eyebrow">Audit · ', '<p class="eyebrow">Audit LK · ', 1)
        s2 = s2.replace('<p class="eyebrow">Audit Laporan Keuangan (KAP) · ', '<p class="eyebrow">Audit LK (KAP) · ', 1)
        if s2 != s:
            n["eyebrow"] += 1
            s = s2
        i = s.find("</h1>")
        if i > 0:
            head, tail = s[:i], s[i:]
            t2 = re.sub(r'(<p class="t"[^>]*>)Audit laporan keuangan ', r"\1Audit LK (laporan keuangan) ", tail, count=1)
            if t2 != tail:
                n["hero"] += 1
                s = head + t2
        if s != o:
            n["file"] += 1
            if not DRY:
                open(f, "w", encoding="utf8").write(s)
    return n, names


if __name__ == "__main__":
    a, names = do_fa()
    print("FA", a)
