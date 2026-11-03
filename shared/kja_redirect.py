# -*- coding: utf-8 -*-
"""3 Nov 2026: KJA Farhani tidak lagi punya website terpisah. kja-farhani.pages.dev menjadi redirect 301 ke ekosistem FA
(halaman KJA Farhani di FA, jasa pembukuan di CariAkuntan, standar di UpdateSAK). Juga mengganti semua link pages.dev di situs lain."""
import os, shutil, re
FA = "https://faindonesia.co.id"; CA = "https://cariakuntan.com"; US = "https://updatesak.com"
HOME = FA + "/kja-farhani/"
MAP = [
 ("/kantor-jasa-akuntan-malang", CA + "/jasa-pembukuan/malang/"), ("/jasa-penyusunan-laporan-keuangan-malang", CA + "/jasa-pembukuan/malang/"),
 ("/artikel/jasa-pembukuan-malang", CA + "/jasa-pembukuan/malang/"), ("/artikel/jasa-laporan-keuangan-cafe-malang", CA + "/jasa-pembukuan/malang/"),
 ("/jasa-penyusunan-laporan-keuangan-surabaya", CA + "/kota/surabaya/kja/"),
] + [(f"/kantor-jasa-akuntan-{c}", f"{CA}/kota/{c}/kja/") for c in ("surabaya", "sidoarjo", "pasuruan", "batu", "kediri", "mojokerto", "tuban")] + [
 ("/lapor-umkm", CA + "/jasa-pembukuan/"), ("/lapor-resto", CA + "/jasa-pembukuan/"), ("/artikel/jasa-laporan-keuangan-toko-umkm-murah", CA + "/jasa-pembukuan/"),
 ("/artikel/laporan-keuangan-koperasi-kantin-kampus", CA + "/jasa-pembukuan/"),
 ("/jasa-lapor-pajak", CA + "/layanan/konsultan-pajak/"), ("/artikel/beda-kja-dan-kap", CA + "/artikel/kja-adalah-kantor-jasa-akuntansi/"),
 ("/artikel/ajukan-kur-belum-punya-laporan-keuangan", FA + "/laporan-keuangan-umkm/"), ("/artikel/laporan-keuangan-untuk-kredit-bank-kur", FA + "/laporan-keuangan-umkm/"),
 ("/artikel/dokumen-laporan-keuangan-tahunan", FA + "/laporan-tahunan-pt/"),
 ("/artikel/penomoran-baru-psak", US + "/penomoran-psak-baru/"), ("/artikel/update-psak-2026", US + "/update-psak-2026/"),
 ("/artikel/psak-118-penyajian-laporan-keuangan", US + "/"), ("/artikel/psak-119-entitas-anak-tanpa-akuntabilitas-publik", US + "/"), ("/artikel/sak-ep-pengganti-sak-etap", US + "/"),
 ("/apps", FA + "/apps/"),
]
def build(k):
    if os.path.exists(k): shutil.rmtree(k)
    os.makedirs(k)
    lines = []
    for src, dst in MAP: lines += [f"{src} {dst} 301", f"{src}/ {dst} 301", f"{src}/* {dst} 301"]
    lines += ["/ " + HOME + " 301", "/* " + HOME + " 301"]
    open(os.path.join(k, "_redirects"), "w").write("\n".join(lines) + "\n")
    open(os.path.join(k, "index.html"), "w").write(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={HOME}"><link rel="canonical" href="{HOME}"><title>KJA Farhani K.N.</title><a href="{HOME}">KJA Farhani K.N. di FA Indonesia</a>')
    return len(lines)
def relink(roots):
    n = 0
    for r in roots:
        for d, _, fs in os.walk(r):
            for f in fs:
                if not f.endswith((".html", ".xml", ".txt", ".js")): continue
                p = os.path.join(d, f); t = open(p, encoding="utf-8", errors="ignore").read()
                if "kja-farhani.pages.dev" not in t and "kja-farhani.netlify.app" not in t: continue
                t2 = re.sub(r"https?://kja-farhani\.(pages\.dev|netlify\.app)/?", HOME, t)
                open(p, "w", encoding="utf-8").write(t2); n += 1
    return n
