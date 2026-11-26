#!/usr/bin/env python3
"""26 Nov 2026 (5): CA dan US berdiri sendiri (keputusan Bos 26 Nov 16.00).

Putus corong ke FA di out/cariakuntan dan out/updatesak. Idempoten, --dry, --sisa (cetak pola link FA tersisa).
JALANKAN PALING AKHIR untuk CA dan US (sesudah caus_ramping_20261120.py dan ca_lk_siap_bank_20261120.py).
1. Strip KAP DHN / KJA Farhani (kelas dhnb, data-fa-out): tombol jadi WA langsung dengan pesan bersumber.
2. Lipatan "Butuh Pendampingan sampai Dana Cair?" (daftar link FA) dibuang.
3. Link FA lain di isi: anchor dilepas (teks tetap) atau blok dibuang, lihat aturan di bawah.
TETAP: link Kebijakan Privasi (nofollow), link pembayaran/produk US ke faindonesia.co.id (/bayar/, /api/pay, kkx, data-us-kk, kelas dl).
"""
import collections, glob, html, os, re, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
SISA = "--sisa" in sys.argv
WA = "https://wa.me/6282245260121?text="
FAH = r"https://(?:www\.)?faindonesia\.co\.id"
changed = 0
left = collections.Counter()
ex = {}


def title(s):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    t = re.sub(r"<[^>]+>", "", m.group(1)) if m else re.search(r"<title>(.*?)</title>", s).group(1)
    return html.unescape(re.sub(r"\s+", " ", t)).strip()[:70]


def keep(tag, href):
    return ("/kebijakan-privasi" in href or "/bayar" in href or "/api/pay" in href or "/kkx" in href
            or "data-us-kk" in tag or re.search(r'class="[^"]*\bdl\b', tag) or "/syarat-ketentuan" in href
            or "/kebijakan-refund" in href)


for site, dom in (("cariakuntan", "cariakuntan.com"), ("updatesak", "updatesak.com")):
    for f in glob.glob(os.path.join(ROOT, "out", site, "**", "*.html"), recursive=True):
        old = open(f).read()
        if "faindonesia.co.id" not in old and "Pencarian Populer" not in old and "Rinciannya di" not in old:
            continue
        s = old
        t = title(s)

        def dhn(m):
            kind = m.group(2)
            if kind == "audit":
                msg, lab = f"Halo, saya dari {dom} ({t}). Mau tanya audit laporan keuangan.", "Tanya Audit via WhatsApp"
            else:
                msg, lab = f"Halo, saya dari {dom} ({t}). Mau tanya penyusunan laporan keuangan.", "Tanya Laporan Keuangan via WhatsApp"
            return (f'<a class="dhnb" href="{WA}{quote(msg)}" target="_blank" rel="noopener" data-wa-out="{kind}">{lab}</a>')
        s = re.sub(r'<a class="dhnb" href="' + FAH + r'([^"]*)" data-fa-out="(audit|lk)">[^<]*</a>', dhn, s)
        s = re.sub(r'<details class="fold"><summary>Butuh Pendampingan sampai Dana Cair\?</summary>.*?</details>\s*', "", s, flags=re.S)
        s = re.sub(r' · <a href="' + FAH + r'/audit-koperasi-desa-merah-putih/">Laporan Keuangan dan Audit KDMP</a>', "", s)

        # footer US, pita alur, CTA, bagian kota di halaman segmen US
        s = re.sub(r' · <a href="' + FAH + r'/">FA Indonesia</a></span>', "</span>", s)
        s = s.replace("Masih Bingung? Serahkan ke Tim FA Indonesia", "Masih Bingung? Serahkan ke Tim Kami")
        s = re.sub(r'<a class="l" href="' + FAH + r'[^"]*"[^>]*>.*?</a>', "", s, flags=re.S)
        s = re.sub(r'<h2 id="bantuan-di-kota-anda">.*?</h2><p>.*?</p><details>.*?</details>', "", s, flags=re.S)
        s = re.sub(r'\s*<a class="btn" href="' + FAH + r'[^"]*"[^>]*>Detail Layanan</a>', "", s)
        if f.endswith(os.path.join("cariakuntan", "kota", "index.html")):
            s = re.sub(r'<h2 style="margin-top:28px">Pencarian Populer</h2>(<div class="citylist">.*?</div>)',
                       r'<style>.ppfold{margin:28px 0 8px;border:1px solid rgba(127,127,127,.35);border-radius:10px;padding:12px 16px}.ppfold summary{cursor:pointer;font-weight:600;font-size:1.15rem}.ppfold .citylist{margin-top:12px}</style><details class="ppfold"><summary>Pencarian Populer</summary>\1</details>', s, count=1, flags=re.S)

        def unwrap(m):
            tag, href, inner = m.group(0), m.group(1), m.group(2)
            return tag if keep(tag[:tag.find(">") + 1], href) else inner
        if not SISA:
            s = re.sub(r'<a\b[^>]*?href="' + FAH + r'([^"]*)"[^>]*>(.*?)</a>', unwrap, s, flags=re.S)

        s = re.sub(r" Rinciannya di [^<]*?\.(?= Untuk membandingkan)", "", s)

        def gen(m):
            tag, href, inner = m.group(0), m.group(1), m.group(2)
            if keep(tag[:tag.find(">") + 1], href):
                return tag
            if SISA:
                pre = s[max(0, m.start() - 2500):m.start()]
                mk = re.findall(r"<!--([a-z0-9/_-]+)-->", pre)
                cls = re.search(r'class="([^"]*)"', tag[:tag.find(">")])
                key = (cls.group(1) if cls else "", mk[-1] if mk else "-", re.sub(r"<[^>]+>", "", inner)[:34])
                left[(site,) + key] += 1
                ex.setdefault((site,) + key, f)
            return tag
        if SISA:
            re.sub(r'<a\b[^>]*?href="' + FAH + r'([^"]*)"[^>]*>(.*?)</a>', gen, s, flags=re.S)
        if s != old:
            changed += 1
            if not DRY and not SISA:
                open(f, "w").write(s)
print(("DRY " if DRY or SISA else "") + f"{changed} file berubah")
if SISA:
    print("link FA tersisa:", sum(left.values()), "pola:", len(left))
    for k, v in left.most_common(45):
        print(v, k, ex[k].split("/out/")[1][:70])
