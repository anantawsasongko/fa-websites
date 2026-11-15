"""Template bersama modul FA Indonesia (A4, cover foto gradasi)."""
import os
A = 'file:///home/claude/ebook/assets/'
WA = 'https://wa.me/6282245260121'

CSS = """
@font-face{font-family:'Newsreader';src:url('%(A)sNewsreader-normal.ttf');font-style:normal;font-weight:200 800}
@font-face{font-family:'Newsreader';src:url('%(A)sNewsreader-italic.ttf');font-style:italic;font-weight:200 800}
:root{--d:%(dark)s;--a:%(acc)s;--ink:#1d1d1f;--mut:#5f6368;--line:#dcdcdc}
@page{size:A4;margin:21mm 19mm 19mm 19mm;
  @bottom-left{content:"FA Indonesia  |  %(foot)s";font:400 7.5pt Poppins;color:#8a8a8a;letter-spacing:.06em}
  @bottom-right{content:counter(page);font:500 8pt Poppins;color:#8a8a8a}}
@page cover{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font:400 10pt/1.62 Inter,sans-serif;color:var(--ink)}
.cover{page:cover;width:210mm;height:297mm;position:relative;overflow:hidden;
  background:url('%(A)scover-%(key)s.jpg') center/cover no-repeat;break-after:page}
.back{page:cover;width:210mm;height:297mm;position:relative;overflow:hidden;
  background:url('%(A)sback-%(key)s.jpg') center/cover no-repeat;break-before:page}
.cv-logo{position:absolute;left:20mm;top:18mm;height:8.5mm}
.cv-lab{position:absolute;right:20mm;top:20mm;font:500 7.5pt Poppins;letter-spacing:.22em;color:rgba(255,255,255,.85);text-transform:uppercase}
.cv-body{position:absolute;left:20mm;right:24mm;top:58mm;color:#fff;text-shadow:0 1px 18px rgba(0,0,0,.25)}
.cv-no{font:500 8pt Poppins;letter-spacing:.3em;text-transform:uppercase;color:rgba(255,255,255,.9);margin-bottom:7mm;display:flex;align-items:center;gap:4mm}
.cv-no:after{content:"";display:block;width:22mm;height:.5mm;background:var(--a)}
.cv-t{font:500 36pt/1.08 Newsreader,serif;margin:0 0 6mm;letter-spacing:-.01em}
.cv-t i{font-weight:400;color:#fff}
.cv-s{font:300 11.5pt/1.55 Poppins;max-width:150mm;color:rgba(255,255,255,.92)}
.cv-firms{position:absolute;left:20mm;right:20mm;bottom:52mm;font:500 8pt Poppins;letter-spacing:.16em;text-transform:uppercase;color:#2b2b2b;display:flex;flex-wrap:wrap;gap:2mm 6mm}
.cv-foot{position:absolute;left:20mm;right:20mm;bottom:20mm;display:flex;justify-content:space-between;align-items:flex-end;border-top:.3mm solid #1d1d1f;padding-top:4mm;color:#1d1d1f;font:400 8.5pt Poppins}
.cv-foot b{font-weight:500}
.cv-foot .by{font:500 7pt Poppins;letter-spacing:.2em;text-transform:uppercase;color:#6b6b6b}
.auth{display:grid;grid-template-columns:22mm 1fr;gap:5mm;margin-top:8mm;padding-top:5mm;border-top:.25mm solid var(--line);break-inside:avoid}
.auth img{width:22mm;height:29mm;object-fit:cover;object-position:center 20%%}
.auth b{font:600 10pt Poppins;color:var(--d)}
.auth p{font-size:9pt;color:#444;margin:1.5mm 0 0}
h1,h2,h3{break-after:avoid}
.ch{margin-top:13mm}
.toc+.ch{margin-top:0}
.kick,.rule,.lead{break-after:avoid}
.lead,p{break-inside:avoid}
.ch>h3,.two>div>h3{break-after:avoid}
.kick{font:500 7.5pt Poppins;letter-spacing:.24em;text-transform:uppercase;color:var(--a);margin:0 0 2mm}
h2{font:500 22pt/1.15 Newsreader,serif;margin:0 0 5mm;color:var(--d);letter-spacing:-.005em}
h3{font:600 11pt/1.35 Poppins;margin:6mm 0 2mm;color:var(--ink)}
p{margin:0 0 3mm}
.lead{font:400 12pt/1.6 Newsreader,serif;color:#333;margin-bottom:5mm}
.rule{height:.4mm;width:16mm;background:var(--a);margin:0 0 6mm}
ul,ol{margin:0 0 3mm;padding-left:5mm}
li{margin-bottom:1.4mm}
table{width:100%%;border-collapse:collapse;margin:2mm 0 5mm;font-size:8.8pt;line-height:1.45;break-inside:auto}
th{font:500 7.5pt Poppins;letter-spacing:.08em;text-transform:uppercase;text-align:left;color:var(--d);border-bottom:.5mm solid var(--d);padding:2mm 2.5mm 2mm 0;vertical-align:bottom}
td{border-bottom:.25mm solid var(--line);padding:2mm 2.5mm 2mm 0;vertical-align:top}
tr{break-inside:avoid}
td.n,th.n{text-align:right;white-space:nowrap}
tr.tot td{font-weight:600;border-top:.4mm solid var(--ink);border-bottom:none}
.step{display:grid;grid-template-columns:13mm 1fr;gap:0 4mm;padding:4mm 0 3mm;border-top:.25mm solid var(--line);break-inside:avoid}
.step .no{font:400 22pt/1 Newsreader,serif;color:var(--a)}
.step h3{margin:0 0 1.5mm}
.step .row{display:grid;grid-template-columns:27mm 1fr;gap:3mm;font-size:9.2pt;margin-bottom:1mm}
.step .row b{font:500 7pt/1.9 Poppins;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.note{border-left:.8mm solid var(--a);padding:1mm 0 1mm 5mm;margin:4mm 0 5mm;font:400 11pt/1.55 Newsreader,serif;color:#333;break-inside:avoid}
.keep{break-inside:avoid}
.two{display:grid;grid-template-columns:1fr 1fr;gap:0 8mm}
.firm{break-inside:avoid;padding:2.5mm 0;border-top:.25mm solid var(--line)}
.firm b{font:600 9.5pt Poppins;color:var(--d)}
.firm span{display:block;font-size:9pt;color:#333}
.chk li{list-style:none;position:relative;padding-left:6mm}
.chk li:before{content:"";position:absolute;left:0;top:1.6mm;width:2.6mm;height:2.6mm;border:.3mm solid var(--d)}
.toc{break-after:page}
.toc ol{list-style:none;padding:0;margin:4mm 0 10mm;counter-reset:t}
.toc li{counter-increment:t;display:grid;grid-template-columns:12mm 1fr;padding:2.6mm 0;border-bottom:.25mm solid var(--line);font:400 12pt Newsreader,serif}
.toc li:before{content:counter(t,decimal-leading-zero);font:500 8pt/2 Poppins;color:var(--a);letter-spacing:.1em}
.small{font-size:8.3pt;color:var(--mut);line-height:1.5}
.ref li{font-size:8.6pt;margin-bottom:1mm}
.bk-body{position:absolute;left:20mm;right:24mm;top:52mm;color:#fff}
.bk-body h2{color:#fff;font-size:26pt;margin-bottom:6mm}
.bk-body p{font:300 11pt/1.6 Poppins;color:rgba(255,255,255,.92);max-width:150mm}
.btn{display:inline-block;margin-top:6mm;background:var(--a);color:#fff;text-decoration:none;font:500 9.5pt Poppins;letter-spacing:.06em;padding:3.2mm 7mm;border-radius:10mm}
.btn2{display:inline-block;margin:6mm 0 0 4mm;color:#fff;text-decoration:none;font:500 9.5pt Poppins;letter-spacing:.06em;padding:3mm 7mm;border:.35mm solid rgba(255,255,255,.8);border-radius:10mm}
.bk-foot{position:absolute;left:20mm;right:20mm;bottom:20mm;display:flex;justify-content:space-between;align-items:flex-end;border-top:.3mm solid #1d1d1f;padding-top:4mm;font:400 8pt Poppins;color:#1d1d1f}
.bk-foot img{height:7mm}
"""

FIRMS = ['McKinsey', 'BCG', 'Bain', 'EY', 'KPMG', 'PwC', 'Deloitte']


def page(m):
    css = CSS % dict(A=A, dark=m['dark'], acc=m['acc'], key=m['key'], foot=m['foot'])
    toc = ''.join(f'<li>{t}</li>' for t in m['toc'])
    firms = ''.join(f'<span>{f}</span>' for f in FIRMS)
    return f"""<!doctype html><html lang="id"><head><meta charset="utf-8"><title>{m['title_plain']}</title><style>{css}</style></head><body>
<section class="cover">
 <img class="cv-logo" src="{A}wm-light.png" alt="FA Indonesia">
 <div class="cv-lab">Modul FA Indonesia</div>
 <div class="cv-body"><div class="cv-no">Modul {m['no']}</div>
 <h1 class="cv-t">{m['title']}</h1><div class="cv-s">{m['sub']}</div></div>
 <div class="cv-foot"><div><span class="by">Penulis</span><br><b>Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP</b><br>Tim FA Indonesia, Edisi November 2026</div><div>faindonesia.co.id</div></div>
</section>
<section class="toc"><div class="kick">Isi Modul</div><h2>Daftar Isi</h2><div class="rule"></div>
<ol>{toc}</ol>
<h3>Cara Memakai Modul Ini</h3>{m['howto']}
<div class="auth"><img src="{A}ananta-w-sasongko-cpa.jpg" alt=""><div><div class="kick" style="margin-bottom:1mm">Penulis</div><b>Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP</b><p>CFO dan Direktur Keuangan, ex-EY. Certified Public Accountant (IAPI), FMVA dan FPAP (CFI). Kandidat doktor ilmu akuntansi. Menulis modul ini bersama Tim FA Indonesia sebagai metode dasar setiap penugasan FA Indonesia.</p></div></div>
<p class="small" style="margin-top:6mm">Modul ini bahan belajar umum, bukan nasihat hukum, pajak, atau investasi untuk kasus tertentu. Nama firma disebut sebagai rujukan praktik yang dipublikasikan secara umum; FA Indonesia tidak berafiliasi dengan firma tersebut, dan nama unit layanan firma dapat berubah dari waktu ke waktu. Angka dalam contoh adalah ilustrasi.</p>
</section>
{m['body']}
<section class="back">
 <img class="cv-logo" src="{A}wm-light.png" alt="FA Indonesia">
 <div class="bk-body"><div class="cv-no">Langkah Berikutnya</div><h2>{m['back_t']}</h2><p>{m['back_p']}</p>
 <a class="btn" href="{WA}">Chat Ananta, CPA</a><a class="btn2" href="https://faindonesia.co.id">faindonesia.co.id</a></div>
 <div class="bk-foot"><div>FA Indonesia<br>Spirit &amp; Hope. Since 2016</div><img src="{A}wm-dark.png" alt="FA Indonesia"></div>
</section>
</body></html>"""
