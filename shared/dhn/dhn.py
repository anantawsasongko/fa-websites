# -*- coding: utf-8 -*-
"""Identitas KAP DHN & Rekan + KJA Farhani K.N. (strip biru, 2 Nov 2026) di semua situs (2 Nov 2026, permintaan Bos: logo + nama KAP DHN di semua tempat + nomor Bos).
- Halaman bertema audit/KAP: kartu besar (logo, nama, izin, layanan, kontak audit Ananta, CPA + nomor + tombol WA)
- Semua halaman lain: strip ringkas di atas footer
Dipanggil dari prep.py di akhir (setelah related cards). Idempoten (penanda <!--dhn-->)."""
import os, re, shutil
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__))
WA = "6282245260121"; TEL_TXT = "0822 4526 0121"; TEL = "+6282245260121"
SITE_DHN = "https://kap.akuntan-dhnr.com/"
CSS = ("<style id=\"dhn-css\">"
 ".dhnc{box-sizing:border-box;width:min(1008px,calc(100% - 32px));margin:34px auto;display:flex;gap:18px;align-items:flex-start;padding:20px 22px;border:1px solid rgba(232,115,12,.55);border-radius:12px;background:rgba(232,115,12,.06);font-family:inherit;text-align:left}"
 ".dhnc img{width:46px;height:auto;flex:0 0 46px;margin-top:2px}"
 ".dhnc small{display:block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#E8730C;font-weight:600}"
 ".dhnc b.n{display:block;font-size:20px;line-height:1.25;margin:2px 0 6px;font-weight:600}"
 ".dhnc p{margin:0 0 8px;font-size:14px;line-height:1.55;opacity:.9}"
 ".dhnc .k{font-size:14px;margin:0 0 12px;opacity:1}.dhnc .k a{color:inherit;font-weight:600;text-decoration:none;white-space:nowrap}"
 ".dhnc .bt{display:flex;gap:10px;flex-wrap:wrap}"
 ".dhnb{display:inline-block;background:#E8730C;color:#fff!important;border-radius:999px;padding:9px 18px;font-size:14px;font-weight:600;text-decoration:none!important;line-height:1.3}"
 ".dhnl{display:inline-block;border:1px solid rgba(128,128,128,.5);color:inherit!important;border-radius:999px;padding:8px 16px;font-size:13.5px;text-decoration:none!important;line-height:1.3}"
 ".dhns{box-sizing:border-box;width:min(1008px,calc(100% - 32px));margin:26px auto 18px;display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;padding:12px 16px;border:1px solid rgba(128,128,128,.32);border-radius:10px;font-size:13.5px;line-height:1.45;text-align:left;font-family:inherit}"
 ".dhns img{width:24px;height:auto}.dhns b{font-weight:600}.dhns .s{opacity:.8}.dhns a.t{color:inherit;font-weight:600;text-decoration:none;white-space:nowrap}"
 ".dhns .dhnb{padding:7px 14px;font-size:13px;margin-left:auto}"
 ".dhns+.dhns{margin-top:-8px}.dhns.kja{border-color:rgba(37,99,235,.38)}.dhns.kja img{width:15px;margin:0 4px}.dhns.kja .dhnb{background:#2563EB}.dhns a.nm{color:inherit;text-decoration:none}"
 "@media(max-width:600px){.dhnc{flex-direction:column;gap:10px;padding:18px}.dhns .dhnb{margin-left:0}}"
 "@media print{.dhnc,.dhns{display:none}}"
 "</style>")
T = {
 "id": dict(lab="Kantor Akuntan Publik Mitra", reg="Terdaftar OJK", desc="Izin Menteri Keuangan KMK No. 592/KM.1/2023, terdaftar OJK, anggota jaringan PA Global. Audit umum, audit untuk kredit bank dan laporan tahunan PT (SABH), reviu, dan prosedur yang disepakati untuk perusahaan di seluruh Indonesia.",
           kon="Kontak audit", wa="Chat WhatsApp", web="Profil KAP DHN", msg="Halo Pak Ananta, saya ingin tanya jasa audit di KAP DHN & Rekan."),
 "en": dict(lab="Partner Public Accounting Firm", reg="Registered with OJK", desc="Licensed by the Minister of Finance (KMK No. 592/KM.1/2023), registered with OJK, member of the PA Global network. Statutory audits, audits for bank loans and annual reports, reviews, and agreed-upon procedures across Indonesia.",
           kon="Audit contact", wa="Chat on WhatsApp", web="About KAP DHN", msg="Hello Pak Ananta, I would like to ask about an audit with KAP DHN & Rekan."),
}
TK = {
 "id": dict(lab="Kantor Jasa Akuntansi", reg="Izin 232/KM.1PPPK/2020", kon="Kontak KJA", wa="Chat WhatsApp",
           msg="Halo Pak Ananta, saya ingin tanya jasa pembukuan, laporan keuangan, dan pajak di KJA Farhani K.N."),
 "en": dict(lab="Accounting Services Firm", reg="License 232/KM.1PPPK/2020", kon="KJA contact", wa="Chat on WhatsApp",
           msg="Hello Pak Ananta, I would like to ask about bookkeeping, financial statements, and tax with KJA Farhani K.N."),
}
def strip_kja(L, mark, prof):
    t = TK[L]; wa = f"https://wa.me/{WA}?text={quote(t['msg'])}"
    return (f'<div class="dhns kja"><img src="{mark}" alt="Logo KJA Farhani K.N." width="15" height="28" loading="lazy">'
            f'<span><a class="nm" href="{prof}"><b>KJA Farhani K.N.</b></a> <span class="s">· {t["lab"]}, {t["reg"]}</span></span>'
            f'<span>{t["kon"]}: Ananta, CPA · <a class="t" href="tel:{TEL}">{TEL_TXT}</a></span>'
            f'<a class="dhnb" href="{wa}" target="_blank" rel="noopener">{t["wa"]}</a></div>')

def lang_of(rel):
    return "en" if re.match(r"(en|zh|hokkien)(/|$)", rel) else "id"
def card(L, mark, prof):
    t = T[L]; wa = f"https://wa.me/{WA}?text={quote(t['msg'])}"
    return (f'<!--dhn--><aside class="dhnc" aria-label="KAP DHN &amp; Rekan"><img src="{mark}" alt="Logo KAP DHN &amp; Rekan" width="46" height="54" loading="lazy">'
            f'<div><small>{t["lab"]}</small><b class="n">KAP DHN &amp; Rekan</b><p>{t["desc"]}</p>'
            f'<p class="k">{t["kon"]}: Ananta, CPA · <a href="tel:{TEL}">{TEL_TXT}</a></p>'
            f'<div class="bt"><a class="dhnb" href="{wa}" target="_blank" rel="noopener">{t["wa"]}</a><a class="dhnl" href="{prof}" target="_blank" rel="noopener">{t["web"]}</a></div></div></aside><!--/dhn-->')
def strip(L, mark):
    t = T[L]; wa = f"https://wa.me/{WA}?text={quote(t['msg'])}"
    return (f'<!--dhn--><div class="dhns"><img src="{mark}" alt="Logo KAP DHN &amp; Rekan" width="24" height="28" loading="lazy">'
            f'<span><b>KAP DHN &amp; Rekan</b> <span class="s">· {t["lab"]}, {t["reg"]}</span></span>'
            f'<span>{t["kon"]}: Ananta, CPA · <a class="t" href="tel:{TEL}">{TEL_TXT}</a></span>'
            f'<a class="dhnb" href="{wa}" target="_blank" rel="noopener">{t["wa"]}</a></div><!--/dhn-->')

AUDIT = re.compile(r"(audit|(^|/)kap(-|/|$)|kap-murah|opini|laporan-tahunan|nirlaba|sabh|mitra-kap|kja|standar-audit|saldo-awal|ganti-kap|wilayah/|^kota/[^/]+/(index\.html)?$|jasa-penyusunan|laporan-keuangan-umkm)")

def _outside(t, pat):
    for m in re.finditer(pat, t):
        i = m.start(); so = t.rfind("<script", 0, i); sc = t.rfind("</script>", 0, i)
        if so <= sc: return i
    return -1

def add_dhn(site_root, site, prof):
    os.makedirs(os.path.join(site_root, "img"), exist_ok=True)
    shutil.copy2(os.path.join(HERE, "kap-dhn-mark.png"), os.path.join(site_root, "img", "kap-dhn-mark.png"))
    shutil.copy2(os.path.join(HERE, "kja-farhani-mark.png"), os.path.join(site_root, "img", "kja-farhani-mark.png"))
    mark = "/img/kap-dhn-mark.png"; nc = ns = 0
    kprof = "/kja-farhani/" if site == "fa" else "https://faindonesia.co.id/kja-farhani/"
    for d, _, fs in os.walk(site_root):
        if "index.html" not in fs: continue
        p = os.path.join(d, "index.html"); rel = os.path.relpath(p, site_root).replace(os.sep, "/")
        if rel.split("/")[0] in ("ai-admin", "bayar", "404.html") or "/uji/" in rel: continue
        t = open(p, encoding="utf-8").read()
        if "noindex" in t[:4000] and "robots" in t[:4000]: continue
        t = re.sub(r"<!--dhn-->.*?<!--/dhn-->", "", t, flags=re.S)
        L = lang_of(rel)
        big = bool(AUDIT.search(rel)) and site != "us" or (site == "us" and rel.startswith("standar-audit"))
        blk = card(L, mark, prof) if big else strip(L, mark)
        blk = blk.replace("<!--/dhn-->", strip_kja(L, "/img/kja-farhani-mark.png", kprof) + "<!--/dhn-->")
        k = -1
        if big:
            k = _outside(t, r'<(section|div) class="fxrel')
        if k < 0: k = _outside(t, r"<footer[\s>]")
        if k < 0: k = t.rfind("</body>")
        if k < 0: continue
        t = t[:k] + blk + t[k:]
        if "dhn-css" not in t: t = t.replace("</head>", CSS + "</head>", 1)
        open(p, "w", encoding="utf-8").write(t)
        if big: nc += 1
        else: ns += 1
    return nc, ns
