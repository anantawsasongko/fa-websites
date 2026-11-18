#!/usr/bin/env python3
"""Redesign section #jalur beranda FA (18 Nov 2026).

Bekerja di out/faindonesia/index.html, idempoten, --dry.
Isi teks, link, dan kunci data-i18n jl3..jl24 tetap; hanya tata letak.
Bagan tangga 3 tahap (01/02/03) satu panel, poin tampil terbuka,
tombol utama + link sekunder, strip "Belum Yakin Jalurnya?" di kaki panel.
Jalankan PALING AKHIR untuk beranda FA (setelah fa_pendanaan dan tidy_tabs/prep).
"""
import re, sys

F = "out/faindonesia/index.html"
DRY = "--dry" in sys.argv
M0, M1 = "<!--fa-jalur18-->", "<!--/fa-jalur18-->"
C0, C1 = "<!--fa-jalur18-css-->", "<!--/fa-jalur18-css-->"

WA = "https://wa.me/6282245260121?text="
COLS = [
    dict(n="01", h=24, hi=False, tg=("jl3", "Aset di Bawah Rp25 Miliar"), t=("jl4", "Rapikan Laporan Keuangan Dulu"),
         li=[("jl5", "Laporan Keuangan, Audit KAP, dan Pajak Dibereskan Lebih Dulu"),
             ("jl6", "KAP, KJA, dan Konsultan Pajak Berizin Lewat CariAkuntan"),
             ("jl7", "Tim FA Membantu Penyiapan sampai Siap Diajukan")],
         a1=("jl8", "Mulai di CariAkuntan", "https://cariakuntan.com/screening/", True),
         a2=("jl9", "Tanya Penyiapan", WA + "Halo%20Pak%20Ananta%2C%20aset%20perusahaan%20kami%20di%20bawah%20Rp25%20miliar.%20Kami%20ingin%20merapikan%20laporan%20keuangan%20dan%20dokumen%20dulu.", True)),
    dict(n="02", h=48, hi=True, tg=("jl10", "Aset Rp25 Miliar ke Atas"), t=("jl11", "Kredit Komersial Bank"),
         li=[("jl12", "Hitung Plafon dan Kemampuan Bayar dalam 3 Menit"),
             ("jl13", "Berkas Kredit Disiapkan Sesuai Cara Analis Bank Membaca"),
             ("jl14", "Pendampingan Due Diligence sampai Dana Cair")],
         a1=("jl15", "Cek Kredit Gratis", "#cek-kredit", False),
         a2=("jl16", "Chat Ananta, CPA", WA + "Halo%20Pak%20Ananta%2C%20aset%20perusahaan%20kami%20di%20atas%20Rp25%20miliar.%20Kami%20ingin%20diskusi%20pengajuan%20kredit%20bank.", True)),
    dict(n="03", h=72, hi=False, tg=("jl18", "Aset Bersih di Atas Rp50 Miliar"), t=("jl19", "Investor Institusi dan IPO"),
         li=[("jl20", "Aset Bersih di Atas Rp50 Miliar, Berturut-turut"),
             ("jl21", "Private Equity, Family Office, dan Pembeli Strategis"),
             ("jl22", "Persiapan IPO Bursa Efek Indonesia")],
         a1=("jl23", "Untuk Investor", "/mitra-investor/", False),
         a2=("jl24", "Diskusi IPO", WA + "Halo%20Pak%20Ananta%2C%20aset%20bersih%20perusahaan%20kami%20di%20atas%20Rp50%20miliar.%20Kami%20ingin%20diskusi%20investor%20institusi%20atau%20IPO.", True)),
]

def a(k, txt, href, ext, cls):
    x = ' rel="noopener" target="_blank"' if ext else ""
    return f'<a class="{cls}" data-i18n="{k}" href="{href}"{x}>{txt}</a>'

def col(c):
    li = "".join(f'<li data-i18n="{k}">{v}</li>' for k, v in c["li"])
    k2, t2, h2, e2 = c["a2"]
    ext = ' rel="noopener" target="_blank"' if e2 else ""
    sec = (f'<a class="jr-lk" href="{h2}"{ext}>'
           f'<span data-i18n="{k2}">{t2}</span><i aria-hidden="true">&#8594;</i></a>')
    return (f'<div class="jr-c{" jr-hi" if c["hi"] else ""}">'
            f'<div class="jr-st" aria-hidden="true"><b>{c["n"]}</b><i style="--h:{c["h"]}px;--f:{round(c["h"]/72,2)}"></i></div>'
            f'<span class="jr-tg" data-i18n="{c["tg"][0]}">{c["tg"][1]}</span>'
            f'<h3 data-i18n="{c["t"][0]}">{c["t"][1]}</h3>'
            f'<ul>{li}</ul>'
            f'<div class="jr-ac">{a(c["a1"][0], c["a1"][1], c["a1"][2], c["a1"][3], "btn red")}{sec}</div></div>')

BODY = (M0 + '<div class="jr" id="jalur-peta"><div class="jr-grid">' + "".join(col(c) for c in COLS) + '</div>'
        '<!--fa-peta-pendanaan--><div class="jr-ft"><div><b>Belum Yakin Jalurnya?</b>'
        '<span>Peta Pendanaan: Skor, Celah, Mitra, dan Checklist Data Room dalam 2 Menit</span></div>'
        '<a class="jr-ftb" href="/cek-kesiapan-pendanaan/">Cek Kesiapan Pendanaan<i aria-hidden="true">&#8594;</i></a></div><!--/fa-peta-pendanaan-->'
        '</div><p class="jr-note" data-i18n="jl17">Batas di atas adalah gambaran umum: Rp25 miliar untuk pengajuan ke segmen kredit komersial bank, '
        'aset bersih Rp50 miliar untuk investor institusi dan IPO. Kebijakan tiap bank dan investor berbeda.</p>' + M1)

CSS = C0 + '<style id="fa-jalur18">' + (
    "#jalur .jr{margin-top:34px;border:1px solid rgba(255,255,255,.16);background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.01))}"
    "#jalur .jr-grid{display:grid;grid-template-columns:repeat(3,1fr)}"
    "#jalur .jr-c{position:relative;display:flex;flex-direction:column;padding:0 30px 30px;border-left:1px solid rgba(255,255,255,.12);transition:background .3s}"
    "#jalur .jr-c:first-child{border-left:0}"
    "#jalur .jr-c:hover{background:rgba(255,255,255,.025)}"
    "#jalur .jr-hi{background:rgba(255,255,255,.055)}"
    "#jalur .jr-hi:hover{background:rgba(255,255,255,.07)}"
    "#jalur .jr-hi:before{content:'';position:absolute;top:-1px;left:-1px;right:-1px;height:2px;background:#fff;z-index:2}"
    "#jalur .jr-st{position:relative;height:122px;margin:0 -30px 26px;display:flex;align-items:flex-end;border-bottom:1px solid rgba(255,255,255,.28)}"
    "#jalur .jr-st i{display:block;width:100%;height:var(--h);background:linear-gradient(180deg,rgba(255,255,255,.13),rgba(255,255,255,.03));border-top:1px solid rgba(255,255,255,.55)}#jalur .jr-hi .jr-st i{background:linear-gradient(180deg,rgba(255,255,255,.24),rgba(255,255,255,.05));border-top:2px solid #fff}"
    "#jalur .jr-st b{position:absolute;top:22px;left:30px;font:400 15px/1 'Times New Roman',Times,serif;letter-spacing:.22em;color:rgba(255,255,255,.6)}"
    "#jalur .jr-hi .jr-st b{color:#fff}"
    "#jalur .jr-tg{font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:12px}"
    "#jalur .jr-c h3{font-weight:400;font-size:clamp(1.6rem,2.4vw,2.05rem);line-height:1.18;margin:0 0 18px;color:#fff}"
    "#jalur .jr-c ul{list-style:none;margin:0 0 26px;padding:0;display:grid;gap:11px}"
    "#jalur .jr-c li{position:relative;padding-left:20px;font-size:14.5px;line-height:1.55;color:rgba(255,255,255,.78)}"
    "#jalur .jr-c li:before{content:'';position:absolute;left:0;top:.72em;width:9px;height:1px;background:rgba(255,255,255,.55)}"
    "#jalur .jr-ac{margin-top:auto;display:flex;flex-direction:column;gap:14px;align-items:stretch}"
    "#jalur .jr-ac .btn{justify-content:center;text-align:center;padding:13px 18px}"
    "#jalur .jr-lk{display:inline-flex;align-items:center;justify-content:center;gap:10px;font-size:14px;font-weight:500;color:rgba(255,255,255,.85);text-decoration:none;padding:4px 0}"
    "#jalur .jr-lk span{border-bottom:1px solid rgba(255,255,255,.35);padding-bottom:2px;transition:border-color .25s}"
    "#jalur .jr-lk i,#jalur .jr-ftb i{font-style:normal;transition:transform .25s}"
    "#jalur .jr-lk:hover span{border-color:#fff}#jalur .jr-lk:hover i,#jalur .jr-ftb:hover i{transform:translateX(4px)}"
    "#jalur .jr-ft{display:flex;flex-wrap:wrap;gap:14px 28px;align-items:center;justify-content:space-between;padding:22px 30px;border-top:1px solid rgba(255,255,255,.12);background:rgba(0,0,0,.18)}"
    "#jalur .jr-ft b{display:block;font-size:16px;font-weight:600;color:#fff;margin-bottom:3px}"
    "#jalur .jr-ft span{font-size:14px;color:rgba(255,255,255,.65)}"
    "#jalur .jr-ftb{display:inline-flex;align-items:center;gap:12px;padding:12px 22px;border:1px solid rgba(255,255,255,.55);border-radius:2px;color:#fff;font-size:14px;font-weight:500;text-decoration:none;white-space:nowrap;transition:background .25s,color .25s}"
    "#jalur .jr-ftb:hover{background:#fff;color:#111}"
    "#jalur .jr-note{margin:14px 0 0;font-size:12.5px;line-height:1.6;color:rgba(255,255,255,.5);max-width:820px}"
    "@media(max-width:860px){#jalur .jr-grid{grid-template-columns:1fr}"
    "#jalur .jr-c{border-left:0;border-top:1px solid rgba(255,255,255,.12);padding:0 22px 26px}#jalur .jr-c:first-child{border-top:0}"
    "#jalur .jr-st{height:auto;margin:0 0 18px;padding-top:24px;border-bottom:0;align-items:center;gap:16px}#jalur .jr-st b{position:static;flex:none}#jalur .jr-st i,#jalur .jr-hi .jr-st i{flex:none;width:calc((100% - 40px)*var(--f));height:2px;border:0;background:rgba(255,255,255,.45)}#jalur .jr-hi .jr-st i{background:#fff}"
    "#jalur .jr-ft{padding:20px 22px}#jalur .jr-ftb{width:100%;justify-content:center;white-space:normal}}"
) + "</style>" + C1

def main():
    s = open(F, encoding="utf-8").read()
    o = s
    if M0 in s:
        s = re.sub(re.escape(M0) + r".*?" + re.escape(M1), lambda m: BODY, s, count=1, flags=re.S)
    else:
        i = s.find('id="jalur"')
        assert i > 0, "section #jalur tidak ditemukan"
        a0 = s.find("<!--fa-peta-pendanaan-->", i)
        hd = s.find('<div class="head">', i)
        hd_end = s.find("</div>", hd) + len("</div>")
        start = hd_end
        end = s.find("</details>", start)
        assert 0 < end < s.find("</section>", i), "struktur #jalur berubah"
        end += len("</details>")
        assert a0 == -1 or s[start:a0].strip() == "", "posisi peta-pendanaan tidak terduga"
        s = s[:start] + "\n" + BODY + "\n" + s[end:]
    if C0 in s:
        s = re.sub(re.escape(C0) + r".*?" + re.escape(C1), lambda m: CSS, s, count=1, flags=re.S)
    else:
        s = s.replace("</head>", CSS + "</head>", 1)
    ch = s != o
    print("berubah" if ch else "0 perubahan", F)
    if ch and not DRY:
        open(F, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    main()
