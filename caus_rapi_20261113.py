# -*- coding: utf-8 -*-
"""13 Nov 2026. CariAkuntan dan UpdateSAK dirapikan selevel FA (Bos: "audit mendalam website dan tampilan US dan CA,
selevel FA kerapihannya, max 4 tab, US untuk orang cari edukasi lalu hire FA, CA untuk pemilik bisnis cari kantor lalu
pilih rekanan FA; simpelkan, lebih profesional, tulisan dilipat tanpa mengurangi SEO, banyak bagan dan sistematis").

BEKERJA LANGSUNG DI out/cariakuntan dan out/updatesak. Idempoten (dry run: --dry). Jalankan PALING AKHIR untuk CA dan US
(setelah ca_ananta, ca_kw3, us_lead, us_kw3, us_dupfix, us_kertas_kerja, uniq_lokal, blue_ocean, dhn_dua_kartu).

Isi:
1. Menu atas 4 tab di semua halaman.
   CA: Cek Kebutuhan, Cari Kantor, Cek Izin, Wawasan.   US: Standar, Kertas Kerja, Kalkulator, Dibantu Tim FA.
   Beranda lewat logo. Magang dan Toko (CA), Materi, Sertifikasi, Toko (US) hanya di footer. Magang tidak lagi ditaut dari US
   (Bos 13 Nov: terlalu banyak chat menanyakan magang).
2. /css/rx13.css di semua halaman: pita alur 4 langkah sebelum footer (<!--rx13f-->) yang berujung ke FA Indonesia,
   menu rapi di HP, dan di CA satu lebar kolom 880px untuk halaman dalam (sebelumnya teks 640px, tabel 1008px).
3. Beranda CA dan US dibangun ulang (<!--rx13-home-->): bagan alur, peta profesi, tangga belajar, pohon keputusan,
   linimasa, kartu rekanan; teks panjang masuk akordeon tertutup. Semua teks, link, H1, title, description, dan JSON-LD
   lama tetap ada di HTML (script berhenti bila ada link lama yang hilang).
Beranda versi EN/ZH/Hokkien CA hanya ikut menu 4 tab.
"""
import os, re, sys, html, hashlib, urllib.parse
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
CA = os.path.join(HERE, "out", "cariakuntan"); US = os.path.join(HERE, "out", "updatesak")
DRY = "--dry" in sys.argv
N = {"ca": 0, "us": 0}
E = html.escape


def rd(p): return open(p, encoding="utf-8").read()


def wt(p, t, k):
    if os.path.exists(p) and rd(p) == t: return
    N[k] += 1
    if DRY: return
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(t)


def wa(txt): return "https://wa.me/6282245260121?text=" + urllib.parse.quote(txt, safe="")


# ====================== CSS semua halaman ======================
CSS_ALL = """/* rx13 (13 Nov 2026): menu 4 tab, pita alur ke FA Indonesia, kolom halaman dalam. Sumber: caus_rapi_20261113.py */
.rxf{border-top:1px solid var(--line);background:var(--panel);padding:34px 16px 38px;margin-top:48px}
.rxf .in{max-width:1008px;margin:0 auto}
.rxf .t{display:flex;align-items:center;gap:12px;margin:0 0 20px;font:600 11.5px/1.2 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.rxf .t:before{content:"";width:28px;height:1px;background:currentColor}
.rxf ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr)}
.rxf li{position:relative;margin:0;padding:0 16px 0 0}
.rxf li:before{content:"";position:absolute;left:34px;right:0;top:17px;height:1px;background:var(--ink);opacity:.25}
.rxf li:last-child:before{display:none}
.rxf a{display:block;text-decoration:none;color:var(--ink)}
.rxf i{position:relative;z-index:1;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;border:1px solid var(--ink);background:var(--paper);font:600 12px/1 var(--body);font-style:normal}
.rxf b{display:block;margin-top:12px;font:600 1.04rem/1.25 var(--display)}
.rxf small{display:block;margin-top:5px;color:var(--muted);font-size:.86rem;line-height:1.45;max-width:25ch}
.rxf li.end i{background:var(--accent);border-color:var(--accent);color:#fff}
.rxf li.end b{color:var(--accent)}
.rxf a:hover b{text-decoration:underline;text-underline-offset:4px}
main+.rxf{margin-top:0}
@media(max-width:760px){.rxf{padding:28px 16px 30px}.rxf ol{grid-template-columns:1fr;gap:16px}.rxf li{padding:0}
.rxf li:before{left:17px;right:auto;top:34px;bottom:-16px;width:1px;height:auto}
.rxf a{display:grid;grid-template-columns:34px 1fr;column-gap:14px;align-items:start}.rxf i{grid-row:span 2}.rxf b{margin-top:1px}.rxf small{max-width:none}}
@media(max-width:860px){header.top .wrap{flex-wrap:wrap;row-gap:0;padding-bottom:0}
header.top .tabs{width:100%;margin-left:0;justify-content:space-between;order:5}
header.top .tabs{display:flex!important;flex-wrap:nowrap;gap:0}
header.top .tabs a{white-space:nowrap;font-size:.86rem;padding:8px 4px;flex:0 1 auto}}
@media(max-width:360px){header.top .tabs a{font-size:.8rem;padding:8px 2px}}
"""
CSS_CA = """main.wrap.art{max-width:880px}
main.wrap.art .prose{max-width:none}
main.wrap.art>.sub,main.wrap.art>p.sub{max-width:none}
body:has(main.wrap.art) .dhns{width:min(848px,calc(100% - 32px))!important}
main.wrap.art~.dhn2{width:min(848px,calc(100% - 32px))}
main.wrap.art+.rxf .in{max-width:848px}
main.wrap.art>h2{margin-top:40px;margin-bottom:12px}
main.wrap.art>h2+p{margin-top:8px}
main.wrap.art>p{margin-bottom:14px}
main.wrap.art>p.crumb,main.wrap.art>p.label{margin-bottom:0}
main.wrap.art .tx{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:14px 0 24px;border:1px solid var(--line);border-radius:0}
main.wrap.art .tx table{border-collapse:collapse;width:100%;margin:0;font-size:.95rem;line-height:1.5}
main.wrap.art .tx th,main.wrap.art .tx td{padding:12px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
main.wrap.art .tx thead th{background:var(--ink);color:#fff;font:600 11px/1.3 var(--body);letter-spacing:.16em;text-transform:uppercase}
main.wrap.art .tx tr:last-child td{border-bottom:0}
main.wrap.art .tx td:first-child{font-weight:600}
main.wrap.art .faq-acc,main.wrap.art>details{margin-top:8px}
"""

# ====================== CSS beranda (dipakai CA dan US) ======================
CSS_HOME = """
.rx-s{padding-block:clamp(48px,6.4vw,76px);border-top:1px solid var(--line)}
.rx-s.alt{background:var(--panel)}
.rx-ey{display:flex;align-items:center;gap:12px;margin:0 0 14px;font:600 11.5px/1.2 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.rx-ey:before{content:"";width:28px;height:1px;background:currentColor}
h2.rx-ey{font-family:var(--body)}h2.rx-ey:after{display:none!important}
.rx-h{font:600 clamp(1.55rem,3.3vw,2.1rem)/1.14 var(--display);letter-spacing:-.005em;max-width:24ch;margin:0;padding:0}
.rx-h:after,.rx-acc h2:after,.rx-acc h3:after{display:none!important}
.rx-lead{color:var(--muted);max-width:62ch;margin-top:12px;font-size:1.02rem}
.rx-hd{margin-bottom:30px}
/* hero gelap ala FA */
main>.hero{background:radial-gradient(1000px 520px at 88% -10%,color-mix(in srgb,var(--accent) 46%,transparent),transparent 62%),radial-gradient(700px 420px at -10% 120%,color-mix(in srgb,var(--accent) 18%,transparent),transparent 60%),linear-gradient(180deg,#0A0C10 0%,var(--deep) 100%)!important;color:#fff;border-bottom:1px solid #000}
main>.hero::before{opacity:.22}
main>.hero h1{color:#fff}
main>.hero h1 em{font-style:italic;font-weight:500;color:rgba(255,255,255,.74)}
main>.hero .label{display:flex;align-items:center;gap:12px;color:rgba(255,255,255,.72);letter-spacing:.22em;font-size:.7rem}
main>.hero .label:before{content:"";width:34px;height:1px;background:currentColor;flex:none}
main>.hero .sub{color:rgba(255,255,255,.74)}
main>.hero .cta .btn{background:#fff;color:var(--deep);border:1px solid #fff}
main>.hero .cta .btn.btn-line,main>.hero .cta .btn.btn-ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.5)}
main>.hero .cta .btn.btn-line:hover,main>.hero .cta .btn.btn-ghost:hover{background:rgba(255,255,255,.1);border-color:#fff}
main>.hero .rx-link{color:#fff}
main>.hero .stats{border-top-color:rgba(255,255,255,.22)}
main>.hero .stats span{color:rgba(255,255,255,.62)}
main>.hero .rx-path{box-shadow:0 40px 80px -40px rgba(0,0,0,.8);border-color:transparent}
main>.hero .viz{background:#fff;padding:18px;box-shadow:0 40px 80px -40px rgba(0,0,0,.8)}
/* hero dua kolom + alur */
.hero .rx-hg{display:grid;grid-template-columns:1.2fr .8fr;gap:56px;align-items:center}
.rx-path{background:var(--paper);border:1px solid var(--line);padding:24px 24px 20px;box-shadow:0 30px 60px -44px rgba(11,31,51,.5)}
.rx-path>b{display:block;font:600 11.5px/1.2 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:16px}
.rx-path ol{list-style:none;margin:0;padding:0;display:grid}
.rx-path li{position:relative;margin:0;padding:0 0 18px}
.rx-path li:last-child{padding-bottom:0}
.rx-path li:before{content:"";position:absolute;left:16px;top:34px;bottom:0;width:1px;background:var(--ink);opacity:.22}
.rx-path li:last-child:before{display:none}
.rx-path a{display:grid;grid-template-columns:34px 1fr;column-gap:14px;text-decoration:none;color:var(--ink)}
.rx-path i{grid-row:span 2;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;border:1px solid var(--ink);background:var(--paper);font:600 12px/1 var(--body);font-style:normal;position:relative;z-index:1}
.rx-path a b{font:600 1.04rem/1.25 var(--display);margin-top:1px}
.rx-path a small{color:var(--muted);font-size:.86rem;line-height:1.4;margin-top:3px}
.rx-path li.end i{background:var(--accent);border-color:var(--accent);color:#fff}
.rx-path li.end a b{color:var(--accent)}
.rx-path a:hover b{text-decoration:underline;text-underline-offset:4px}
.rx-link{display:inline-block;margin-top:16px;font-weight:600;font-size:.95rem;color:var(--ink);text-underline-offset:5px}
/* peta profesi (matriks) */
.rx-mx{border:1px solid var(--line);background:var(--paper)}
.rx-mx .r{display:grid;grid-template-columns:1.25fr 1.15fr 1fr 1.1fr;border-top:1px solid var(--line);text-decoration:none;color:var(--ink);transition:background .15s ease}
.rx-mx .r:first-child{border-top:0}
.rx-mx a.r:hover{background:var(--soft)}
.rx-mx .r>span{position:relative;padding:16px 26px 16px 18px;font-size:.95rem;line-height:1.4;min-width:0}
.rx-mx .r>span+span:before{content:"";position:absolute;left:-7px;top:50%;width:9px;height:9px;border-top:1.5px solid var(--ink);border-right:1.5px solid var(--ink);transform:translateY(-50%) rotate(45deg);opacity:.35}
.rx-mx .hd{background:var(--ink);color:#fff}
.rx-mx .hd>span{font:600 11px/1.3 var(--body);letter-spacing:.16em;text-transform:uppercase;padding-block:13px}
.rx-mx .hd>span+span:before{display:none}
.rx-mx .r b{display:block;font:600 1.04rem/1.25 var(--display)}
.rx-mx .r small{display:block;color:var(--muted);font-size:.84rem;margin-top:3px}
.rx-mx .r .k{font-weight:600}
.rx-mx .r>span:last-child{background:color-mix(in srgb,var(--accent) 7%,transparent);font-weight:600;color:var(--accent)}
.rx-mx .hd>span:last-child{background:var(--accent);color:#fff}
.rx-mx .r>span[data-l]:after{content:none}
/* cabang (hasil screening) */
.rx-br{margin-top:34px}
.rx-br .root{display:table;margin:0 auto;padding:10px 20px;border-radius:999px;background:var(--accent);color:#fff;font-weight:600;font-size:.95rem;text-align:center}
.rx-br .root small{display:block;font-weight:400;font-size:.8rem;opacity:.85}
.rx-br .stem{width:1px;height:22px;background:var(--ink);opacity:.3;margin:0 auto}
.rx-br .g{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;position:relative;padding-top:22px}
.rx-br .g:before{content:"";position:absolute;left:12.5%;right:12.5%;top:0;height:1px;background:var(--ink);opacity:.3}
.rx-br .g a{position:relative;display:block;padding:14px 16px;border:1px solid var(--line);background:var(--paper);text-decoration:none;color:var(--ink);text-align:center}
.rx-br .g a:before{content:"";position:absolute;left:50%;top:-23px;width:1px;height:22px;background:var(--ink);opacity:.3}
.rx-br .g a b{display:block;font:600 1.02rem/1.25 var(--display)}
.rx-br .g a small{display:block;color:var(--muted);font-size:.84rem;margin-top:3px}
.rx-br .g a:hover{border-color:var(--accent)}
/* kartu rekanan */
.rx-rk{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.rx-rk .c{display:flex;flex-direction:column;gap:8px;padding:24px 22px 22px;border:1px solid var(--line);background:var(--paper);border-top:3px solid var(--ink)}
.rx-rk .c.main{border-top-color:var(--accent)}
.rx-rk .c .m{display:flex;align-items:center;gap:10px;min-height:30px;font:600 11px/1.3 var(--body);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.rx-rk .c .m img{height:26px;width:auto}
.rx-rk .c b{font:600 1.22rem/1.2 var(--display)}
.rx-rk .c .i{font-size:.86rem;color:var(--muted)}
.rx-rk .c p{font-size:.95rem;line-height:1.5;margin:4px 0 10px}
.rx-rk .c a.go{margin-top:auto;align-self:flex-start;font-weight:600;font-size:.93rem;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--ink);padding-bottom:2px}
.rx-rk .c a.go:after{content:" \\2192"}
.rx-rk .c a.go:hover{color:var(--accent);border-color:var(--accent)}
.rx-after{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin-top:26px}
.rx-after span{color:var(--muted);font-size:.93rem}
/* akordeon */
.rx-acc{border-bottom:1px solid var(--line)}
.rx-acc>details{border-top:1px solid var(--line);border-bottom:0;max-width:none;padding-block:0;margin:0}
.rx-acc>details>summary{list-style:none;cursor:pointer;position:relative;padding:20px 44px 20px 0;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px}
.rx-acc>details>summary::-webkit-details-marker{display:none}
.rx-acc>details>summary h2,.rx-acc>details>summary h3{font:600 1.22rem/1.25 var(--display);margin:0;padding:0}
.rx-acc>details>summary small{color:var(--muted);font:400 .88rem/1.4 var(--body)}
.rx-acc>details>summary{justify-content:flex-start}
.rx-acc .bd p{max-width:68ch}
.rx-acc>details>summary:after{content:"+";position:absolute;right:6px;top:14px;font:300 26px/1 var(--body);transition:transform .25s}
.rx-acc>details[open]>summary:after{transform:rotate(45deg)}
.rx-acc>details>summary:hover h2,.rx-acc>details>summary:hover h3{color:var(--accent)}
.rx-acc .bd{padding:2px 0 28px}
.rx-acc .bd>p{color:var(--muted);max-width:68ch;margin:0 0 16px}
.rx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,225px),1fr));gap:12px}
.rx-grid>*{display:grid;gap:5px;align-content:start;padding:16px 16px 18px;border:1px solid var(--line);background:var(--paper);text-decoration:none;color:var(--ink);min-width:0}
.rx-grid>a:hover{border-color:var(--accent)}
.rx-grid b{font:600 1.02rem/1.25 var(--display)}
.rx-grid small{color:var(--muted);font-size:.86rem;line-height:1.45}
.rx-grid em{font-style:normal;font-weight:600;font-size:.84rem;color:var(--accent);margin-top:4px}
.rx-grid .n{font:600 11px/1 var(--body);letter-spacing:.14em;color:var(--muted);text-transform:uppercase}
.rx-grid .ok{font-style:normal;font-weight:600;font-size:.84rem;color:#0B7A5A;border-top:1px dashed var(--line);padding-top:8px;margin-top:4px}
.rx-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,1fr)}
.rx-steps li{position:relative;margin:0;padding:0 14px 0 0}
.rx-steps li:before{content:"";position:absolute;left:34px;right:0;top:17px;height:1px;background:var(--ink);opacity:.25}
.rx-steps li:last-child:before{display:none}
.rx-steps i{position:relative;z-index:1;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;border:1px solid var(--ink);background:var(--paper);font:600 12px/1 var(--body);font-style:normal}
.rx-steps li:last-child i{background:var(--accent);border-color:var(--accent);color:#fff}
.rx-steps b{display:block;margin-top:12px;font:600 1.02rem/1.25 var(--display)}
.rx-steps small{display:block;margin-top:4px;color:var(--muted);font-size:.86rem;line-height:1.45}
.rx-note{margin-top:18px;font-weight:600}
.rx-tb{border:1px solid var(--line);background:var(--paper);overflow-x:auto}
.rx-tb table{width:100%;border-collapse:collapse;font-size:.94rem}
.rx-tb th,.rx-tb td{padding:12px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
.rx-tb tr:last-child th,.rx-tb tr:last-child td{border-bottom:0}
.rx-tb th{width:190px;font-weight:600;background:var(--panel)}
.want .in{max-width:1008px}
@media(min-width:861px){.want .g:has(a:nth-child(5)){grid-template-columns:repeat(5,1fr)}}
main[data-tidy]~.dhns{display:none}
/* tangga (US) */
.rx-st{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-items:end}
.rx-st .c{position:relative;display:flex;flex-direction:column;padding:24px 22px 22px;border:1px solid var(--line);background:var(--paper);border-top:3px solid var(--ink)}
.rx-st .c:nth-child(1){min-height:292px}.rx-st .c:nth-child(2){min-height:328px}.rx-st .c:nth-child(3){min-height:364px}
.rx-st .c .n{font:600 11px/1 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.rx-st .c b.h{display:block;font:600 1.3rem/1.2 var(--display);margin:12px 0 8px}
.rx-st .c p{font-size:.95rem;color:var(--muted);line-height:1.5;margin:0 0 16px}
.rx-st .c ul{list-style:none;margin:auto 0 0;padding:0;display:grid}
.rx-st .c li{margin:0;border-top:1px solid var(--line)}
.rx-st .c li a{display:flex;justify-content:space-between;gap:10px;padding:11px 0;text-decoration:none;color:var(--ink);font-weight:600;font-size:.95rem}
.rx-st .c li a:after{content:"\\2192";opacity:.5}
.rx-st .c li a:hover{color:var(--accent)}
.rx-st .c.end{background:var(--deep);border-color:var(--deep);border-top-color:var(--accent);color:#fff}
.rx-st .c.end .n,.rx-st .c.end p{color:rgba(255,255,255,.72)}
.rx-st .c.end li{border-top-color:rgba(255,255,255,.18)}
.rx-st .c.end li a{color:#fff}
.rx-st .c.end li a:hover{color:#fff;text-decoration:underline;text-underline-offset:4px}
/* pohon keputusan + linimasa (US) */
.rx-two{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.rx-dt{display:grid;gap:0;max-width:440px}
.rx-dt .q{padding:14px 16px;border:1.5px solid var(--ink);background:var(--paper);font-weight:600;line-height:1.35}
.rx-dt .row{display:grid;grid-template-columns:86px 1fr;align-items:center;min-height:20px}
.rx-dt .row .lb{position:relative;font:600 11px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding-left:26px}
.rx-dt .row .lb:before{content:"";position:absolute;left:0;top:50%;width:20px;height:1px;background:var(--ink);opacity:.4}
.rx-dt .ans{display:grid;grid-template-columns:1fr;border-left:1px solid color-mix(in srgb,var(--ink) 40%,transparent);margin-left:24px;padding:12px 0;gap:10px}
.rx-dt .res{padding:10px 14px;color:#fff;font-weight:600;font-size:.95rem}
.rx-dt .down{margin-left:24px;border-left:1px solid color-mix(in srgb,var(--ink) 40%,transparent);height:14px}
.rx-tl{list-style:none;margin:0;padding:0;display:grid}
.rx-tl li{position:relative;margin:0;padding:0 0 22px 30px}
.rx-tl li:last-child{padding-bottom:0}
.rx-tl li:before{content:"";position:absolute;left:5px;top:16px;bottom:-4px;width:1px;background:var(--ink);opacity:.25}
.rx-tl li:last-child:before{display:none}
.rx-tl li:after{content:"";position:absolute;left:0;top:6px;width:11px;height:11px;border-radius:50%;border:1.5px solid var(--ink);background:var(--paper)}
.rx-tl li.now:after{background:var(--accent);border-color:var(--accent);box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 18%,transparent)}
.rx-tl time{font:600 1.2rem/1.2 var(--display)}
.rx-tl li.now time:after{content:"Tahun Buku Berjalan";margin-left:10px;font:600 10.5px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--accent);vertical-align:middle}
.rx-tl .tg{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.rx-tl .tg span{padding:5px 10px;border:1px solid var(--line);background:var(--paper);font-size:.84rem;font-weight:500}
.rx-sub{font:600 1.18rem/1.25 var(--display);margin:0 0 18px;padding:0}
.rx-sub:after{display:none!important}
.rx-src{margin-top:18px;color:var(--muted);font-size:.84rem}
.rx-more{margin-top:20px}
.rx-share{margin-top:26px;padding-top:20px;border-top:1px solid var(--line)}
@media(max-width:900px){.hero .rx-hg{grid-template-columns:1fr;gap:34px}.rx-two{grid-template-columns:1fr;gap:40px}
.rx-rk,.rx-st{grid-template-columns:1fr}.rx-st .c{min-height:0!important}
.rx-steps{grid-template-columns:1fr;gap:16px}.rx-steps li{display:grid;grid-template-columns:34px 1fr;column-gap:14px;padding:0}
.rx-steps li:before{left:17px;right:auto;top:34px;bottom:-16px;width:1px;height:auto}.rx-steps i{grid-row:span 2}.rx-steps b{margin-top:1px}
.rx-br .g{grid-template-columns:1fr 1fr}.rx-br .g:before,.rx-br .g a:before{display:none}.rx-br .g{padding-top:0}.rx-br .stem{height:16px}}
@media(max-width:760px){.rx-mx .hd{display:none}.rx-mx .r{grid-template-columns:1fr;padding:14px 0 12px}
.rx-mx .r>span{padding:3px 16px}.rx-mx .r>span+span:before{display:none}
.rx-mx .r>span[data-l]:before{content:attr(data-l) ": ";display:inline;position:static;border:0;transform:none;width:auto;height:auto;opacity:1;font:600 10.5px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.rx-mx .r>span:last-child{background:none;margin-top:4px}.rx-tb th{width:120px}}
@media(max-width:520px){.rx-br .g{grid-template-columns:1fr}}
"""


JS_HOME = ('<script id="rx13-js">(function(){function o(){var h=location.hash;if(!h||h.length<2)return;var e;try{e=document.querySelector(h)}catch(x){return}'
           'if(!e)return;var d=e.tagName==="DETAILS"?e:e.closest&&e.closest("details");if(d&&!d.open){d.open=true;e.scrollIntoView()}}'
           'window.addEventListener("hashchange",o);if(document.readyState!=="loading")o();else document.addEventListener("DOMContentLoaded",o)})();</script>')

def ver(s): return hashlib.md5(s.encode()).hexdigest()[:8]


# ====================== pita alur ======================
def band(title, steps):
    li = "".join('<li%s><a href="%s"><i>%02d</i><b>%s</b><small>%s</small></a></li>' % (
        ' class="end"' if i == len(steps) - 1 else "", E(u), i + 1, E(b), E(s)) for i, (b, s, u) in enumerate(steps))
    return '<!--rx13f--><div class="rxf"><div class="in"><p class="t">%s</p><ol>%s</ol></div></div><!--/rx13f-->' % (E(title), li)


BAND_CA = band("Alur Memilih Kantor", [
    ("Cek Kebutuhan", "Audit, review, kompilasi, atau cukup pembukuan.", "/cek-kebutuhan/"),
    ("Cek Izin", "Registri Kemenkeu, IAPI, dan OJK.", "/cek-izin/"),
    ("Bandingkan di Kota Anda", "KAP, KJA, KJPP, dan konsultan pajak per kota.", "/kota/"),
    ("Dikerjakan Rekanan FA Indonesia", "KAP DHN & Rekan dan KJA Farhani K.N.", "/#rekanan"),
])
BAND_US = band("Dari Belajar sampai Selesai", [
    ("Pelajari Standarnya", "Ringkasan PSAK, SAK EP, SAK EMKM, dan Standar Audit.", "/eksplor/"),
    ("Kerjakan dengan Kertas Kerja", "Template Excel berumus, termasuk konsultasi.", "/kertas-kerja/"),
    ("Cek dengan Kalkulator", "Kerangka SAK, laporan keuangan, dan CALK.", "/#kalkulator"),
    ("Masih Bingung? Serahkan ke Tim FA Indonesia", "Penerapan PSAK, laporan keuangan, sampai audit.", "/#dibantu"),
])

# ====================== menu ======================
NAV_CA = [("/cek-kebutuhan/", "Cek Kebutuhan", ("cek-kebutuhan",)),
          ("/kota/", "Cari Kantor", ("kota", "layanan", "kap-murah", "kdmp")),
          ("/cek-izin/", "Cek Izin", ("cek-izin", "screening")),
          ("/artikel/", "Wawasan", ("artikel",))]
NAV_CA_L = {"en": ["Needs Check", "Find a Firm", "License Check", "Insights"],
            "zh": ["需求检查", "找事务所", "执照查询", "见解"],
            "hokkien": ["需求檢查", "揣事務所", "執照查詢", "文章"]}
NAV_US = [("/eksplor/", "Standar", ("eksplor", "psak", "standar-audit", "update-psak-2026", "update-psak-terbaru",
                                    "update-isak-terbaru", "update-sak-2027", "update-sak-emkm", "update-sak-ep",
                                    "update-sak-syariah-terbaru", "penomoran-psak-baru", "artikel")),
          ("/kertas-kerja/", "Kertas Kerja", ("kertas-kerja",)),
          ("/#kalkulator", "Kalkulator", ()),
          ("/#dibantu", "Dibantu Tim FA", ())]
RX_NAV = re.compile(r'(<nav[^>]*class="tabs"[^>]*>)(.*?)(</nav>)', re.S)


def nav_html(items, rel, labels=None):
    top = rel.split("/")[0] if rel else ""
    out = []
    for i, (u, lab, keys) in enumerate(items):
        cur = ' aria-current="page"' if top and top in keys else ""
        out.append('<a%s href="%s">%s</a>' % (cur, u, labels[i] if labels else lab))
    return "".join(out)


def common(t, rel, site):
    """menu, link css, pita alur, footer. rel = path folder relatif ('' untuk beranda)."""
    if 'class="tabs"' not in t: return t
    is_ca = site == "ca"
    lang = rel.split("/")[0] if is_ca and rel in ("en", "zh", "hokkien") else None
    items = NAV_CA if is_ca else NAV_US
    t = RX_NAV.sub(lambda m: m.group(1) + nav_html(items, rel, NAV_CA_L.get(lang)) + m.group(3), t, count=1)
    # css
    link = '<link href="/css/rx13.css?v=%s" id="rx13-css" rel="stylesheet"/>' % (VCA if is_ca else VUS)
    t = re.sub(r'<link href="/css/rx13\.css\?v=[0-9a-f]+" id="rx13-css" rel="stylesheet"/>\n?', "", t)
    t = t.replace("</head>", link + "\n</head>", 1)
    # pita alur (bukan di beranda)
    t = re.sub(r'<!--rx13f-->.*?<!--/rx13f-->', "", t, flags=re.S)
    if rel != "" and not lang and "</main>" in t:
        i = t.rindex("</main>") + len("</main>")
        t = t[:i] + (BAND_CA if is_ca else BAND_US) + t[i:]
    # footer: menu yang keluar dari tab tetap tertaut
    if is_ca:
        if "<!--rx13n-->" not in t:
            add = ('<!--rx13n--> · <a href="/magang/">Magang</a> · <a href="https://faindonesia.co.id/toko/?dari=cariakuntan">Toko</a>'
                   ' · <a href="/cek-kebutuhan/">Cek Kebutuhan</a>')
            k = ' · <a href="https://updatesak.com/">Update SAK</a>'
            j = t.rfind(k, t.rfind("<footer"))
            if j > 0: t = t[:j] + add + t[j:]
    else:
        t = t.replace(' · <a href="https://cariakuntan.com/magang/?dari=updatesak">Magang</a> · <a href="https://faindonesia.co.id/toko/', ' · <a href="https://faindonesia.co.id/toko/')
        if "<!--rx13n-->" not in t:
            add = ('<!--rx13n--><a href="/kertas-kerja/">Kertas Kerja</a> · <a href="https://faindonesia.co.id/toko/?dari=updatesak">Toko</a> · ')
            f = t.rfind("<footer")
            j = t.find('<a href="mailto:', f)
            if f > 0 and j > 0: t = t[:j] + add + t[j:]
    return t


# ====================== beranda CA ======================
def inner(tag): return tag.decode_contents()


def links_of(htmltext):
    return sorted(set(html.unescape(u) for u in re.findall(r'href="([^"#][^"]*)"', htmltext)))


def home_ca(t):
    if "<!--rx13-home-->" in t: return t
    soup = BeautifulSoup(t, "html.parser")
    main = soup.find("main")
    old_main = str(main)
    secs = main.find_all("section", recursive=False)
    by = {}
    for s in secs:
        h = s.find("h2") or s.find("h1")
        by[h.get_text(" ", strip=True)] = s
    hero = main.find("section", class_="hero")
    want = main.find("section", id="mulai-cepat")
    screen = main.find("section", id="screen")
    cek = main.find("section", id="cek")
    tree = by["Screening Menentukan Jalur Anda"]
    needs = by["Atau Langsung Pilih Kebutuhan"]
    damp = by["Cara Kami Mendampingi"]
    salah = by["Salah Langkah yang Paling Mahal"]
    kami = main.find("section", id="kami")
    final = main.find("section", class_="final")
    pb = re.search(r'<!--pb-box-->.*?<!--/pb-box-->', old_main, re.S).group(0)

    # hero
    hw = hero.find("div", class_="wrap")
    label = str(hw.find("p", class_="label")); h1 = str(hw.find("h1")); sub = str(hw.find("p", class_="sub"))
    share = str(hw.find("div", class_="tshare-top"))
    cta = hw.find("div", class_="cta"); cta_a = cta.find_all("a")
    path = ('<div class="rx-path"><b>Alur Memilih Kantor</b><ol>'
            '<li><a href="/cek-kebutuhan/"><i>01</i><b>Cek Kebutuhan</b><small>Audit, review, kompilasi, atau cukup pembukuan.</small></a></li>'
            '<li><a href="/cek-izin/"><i>02</i><b>Cek Izin</b><small>Registri Kemenkeu, IAPI, dan OJK.</small></a></li>'
            '<li><a href="/kota/"><i>03</i><b>Bandingkan di Kota Anda</b><small>KAP, KJA, KJPP, dan konsultan pajak per kota.</small></a></li>'
            '<li class="end"><a href="#rekanan"><i>04</i><b>Dikerjakan Rekanan FA Indonesia</b><small>KAP DHN &amp; Rekan dan KJA Farhani K.N.</small></a></li>'
            '</ol></div>')
    hero_h = ('<section class="hero"><div class="wrap rx-hg"><div><!--bo12-hero-->%s\n%s\n%s\n'
              '<div class="cta">%s%s</div><a class="rx-link" href="%s" rel="noopener" target="_blank">%s</a></div>%s</div></section>'
              % (label, h1, sub, str(cta_a[0]), str(cta_a[1]), E(cta_a[2]["href"]), E(cta_a[2].get_text(strip=True)), path))

    # peta profesi
    rows = [("Audit Laporan Keuangan", "Untuk bank, tender, investor, atau wajib audit", "KAP", "Kantor Akuntan Publik",
             "Kemenkeu (PPPK) dan OJK", "KAP DHN & Rekan", "/layanan/kap/"),
            ("Pembukuan dan Laporan Keuangan", "Bulanan, tutup buku, siap bank", "KJA", "Kantor Jasa Akuntansi",
             "Kemenkeu (PPPK)", "KJA Farhani K.N.", "/layanan/jasa-laporan-keuangan/"),
            ("Urusan Pajak", "SPT, Coretax, pemeriksaan", "Konsultan Pajak", "Berizin praktik",
             "Kemenkeu", "Dipilihkan Tim FA Indonesia", "/layanan/konsultan-pajak/"),
            ("Penilaian Aset", "Agunan kredit dan revaluasi", "KJPP", "Kantor Jasa Penilai Publik",
             "Kemenkeu (PPPK)", "Dipilihkan Tim FA Indonesia", "/layanan/kjpp/"),
            ("Kredit Bank, Investor, IPO", "Dari laporan keuangan sampai dana cair", "Penasihat Keuangan", "Financial advisor",
             "NIB badan usaha", "FA Indonesia", "https://faindonesia.co.id/")]
    mx = ('<div class="rx-mx"><div class="r hd"><span>Kebutuhan Anda</span><span>Jenis Kantor</span><span>Izin Dicek di</span>'
          '<span>Rekanan FA Indonesia</span></div>')
    for a, a2, b, b2, c, d, u in rows:
        mx += ('<a class="r" href="%s"><span><b>%s</b><small>%s</small></span><span data-l="Jenis kantor"><span class="k">%s</span>'
               '<small>%s</small></span><span data-l="Izin dicek di">%s</span><span data-l="Rekanan">%s</span></a>'
               % (u, E(a), E(a2), E(b), E(b2), E(c), E(d)))
    mx += "</div>"
    peta = ('<section class="rx-s" id="peta"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Peta Profesi</p>'
            '<h2 class="rx-h">Siapa Mengerjakan Apa</h2><p class="rx-lead">Satu kebutuhan, satu jenis kantor berizin. '
            'Kolom terakhir menunjukkan siapa yang mengerjakannya bila Anda memilih rekanan FA Indonesia.</p></div>%s'
            '<p class="rx-more"><a class="btn btn-wa arrow" href="/cek-kebutuhan/">Belum Yakin? Mulai Cek Kebutuhan</a></p></div></section>' % mx)

    # screening + cabang
    sw = screen.find("div", class_="wrap")
    sh2 = sw.find("h2"); ssub = sw.find("p", class_="sub")
    sh2_txt = sh2.get_text(strip=True); ssub_txt = ssub.get_text(strip=True)
    sh2.extract(); ssub.extract()
    tm = tree.find("div", class_="tree-m")
    root = tm.find("div", class_="c")
    br = ('<div class="rx-br"><h3 class="rx-sub" style="text-align:center">%s</h3><div class="root">%s<small>%s</small></div>'
          '<div class="stem"></div><div class="g">%s</div></div>'
          % (E(by_title(tree)), E(root.find("b").get_text(strip=True)), E(root.find("small").get_text(strip=True)),
             "".join('<a href="%s" rel="noopener" target="_blank"><b>%s</b><small>%s</small></a>'
                     % (E(a["href"]), E(a.find("b").get_text(strip=True)), E(a.find("small").get_text(strip=True)))
                     for a in tm.find_all("a"))))
    screen_h = ('<section class="rx-s alt" id="screen"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Alat Gratis 1</p>'
                '<h2 class="rx-h">%s</h2><p class="rx-lead">%s</p></div>%s%s</div></section>'
                % (E(sh2_txt), E(ssub_txt), inner(sw), br))

    # cek izin
    cw = cek.find("div", class_="wrap")
    ch2 = cw.find("h2"); csub = cw.find("p", class_="sub")
    ch2_txt = ch2.get_text(strip=True); csub_txt = csub.get_text(strip=True)
    ch2.extract(); csub.extract()
    cek_h = ('<section class="rx-s" id="cek"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Alat Gratis 2</p>'
             '<h2 class="rx-h">%s</h2><p class="rx-lead">%s</p></div>%s'
             '<p class="rx-more"><a class="btn btn-line" href="/cek-izin/">Cari semua KAP, KJA, KJPP, dan konsultan pajak berizin di Indonesia</a></p>'
             '</div></section>' % (E(ch2_txt), E(csub_txt), inner(cw)))

    # rekanan
    wa_rek = wa("Halo Pak Ananta, saya dari cariakuntan.com. Kebutuhan saya sudah jelas, mau tanya pengerjaannya oleh rekanan FA Indonesia.")
    rek = ('<section class="rx-s alt" id="rekanan"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Rekanan FA Indonesia</p>'
           '<h2 class="rx-h">Setelah Kebutuhan Jelas, Ini yang Mengerjakan</h2><p class="rx-lead">CariAkuntan dikelola FA Indonesia. '
           'Anda bebas memakai kantor mana pun yang izinnya aktif. Bila ingin langsung dikerjakan, tiga pintu ini yang kami pakai sendiri.</p></div>'
           '<div class="rx-rk">'
           '<div class="c"><span class="m"><img alt="Logo KAP DHN &amp; Rekan" height="28" loading="lazy" src="/img/kap-dhn-mark.png" width="24"/>Audit</span>'
           '<b>KAP DHN &amp; Rekan</b><span class="i">Kantor Akuntan Publik, Terdaftar OJK</span>'
           '<p>Audit laporan keuangan, review, dan prosedur yang disepakati untuk bank, tender, investor, dan laporan tahunan PT.</p>'
           '<a class="go" href="https://faindonesia.co.id/jasa-audit-laporan-keuangan/">Lihat Jasa Audit</a></div>'
           '<div class="c"><span class="m"><img alt="Logo KJA Farhani K.N." height="28" loading="lazy" src="/img/kja-farhani-mark.png" width="15"/>Laporan Keuangan</span>'
           '<b>KJA Farhani K.N.</b><span class="i">Kantor Jasa Akuntansi, Izin 232/KM.1/PPPK/2020</span>'
           '<p>Pembukuan bulanan dan penyusunan laporan keuangan sesuai SAK EMKM, SAK EP, atau PSAK.</p>'
           '<a class="go" href="https://faindonesia.co.id/jasa-penyusunan-laporan-keuangan/">Lihat Jasa Penyusunan</a></div>'
           '<div class="c main"><span class="m">Pendanaan</span>'
           '<b>FA Indonesia</b><span class="i">Financial Advisory, Since 2016</span>'
           '<p>Kredit bank, investor, IPO, dan pendampingan keuangan rumah sakit, setelah laporan keuangan rapi.</p>'
           '<a class="go" href="https://faindonesia.co.id/">Buka FA Indonesia</a></div>'
           '</div><div class="rx-after"><a class="btn btn-wa" href="%s" rel="noopener" target="_blank">Tanya Ananta, CPA</a>'
           '<span>Diskusi awal tanpa biaya.</span></div></div></section>' % E(wa_rek))

    # akordeon
    need_a = needs.find_all("a", class_="need")
    g_need = '<div class="rx-grid">%s</div>' % "".join(
        '<a href="%s" rel="noopener" target="_blank"><b>%s</b><small>%s</small><em>%s</em></a>'
        % (E(a["href"]), E(a.find("b").get_text(strip=True)), E(a.find("small").get_text(strip=True)),
           E(a.find("em").get_text(strip=True))) for a in need_a)
    st = damp.find_all("div", class_="s")
    g_damp = '<ol class="rx-steps">%s</ol>' % "".join(
        '<li><i>%s</i><b>%s</b><small>%s</small></li>' % (E(s.find("i").get_text(strip=True)), E(s.find("b").get_text(strip=True)),
                                                         E(s.find("small").get_text(strip=True))) for s in st)
    csub2 = salah.find("p", class_="c-sub").get_text(strip=True)
    figc = salah.find("figcaption").get_text(strip=True)
    fix = salah.find("p", class_="fixline").get_text(" ", strip=True).replace("✓", "").strip()
    g_salah = '<p>%s</p><div class="rx-grid">%s</div><p class="rx-note">%s</p><p style="margin-top:8px;font-size:.84rem">%s</p>' % (
        E(csub2), "".join('<div><span class="n">%s</span><b>%s</b><small>%s</small><span class="ok">%s</span></div>' % (
            E(c.find("span", class_="n").get_text(strip=True).zfill(2)), E(c.find("b").get_text(strip=True)),
            E(c.find_all("span")[1].get_text(strip=True)), E(c.find("em").get_text(strip=True)))
            for c in salah.find_all("div", class_="cause")), E(fix), E(figc))
    kn = kami.find_all("div", class_="need")
    g_kami = '<div class="rx-grid">%s</div>' % "".join(
        '<div><b>%s</b><small>%s</small></div>' % (E(k.find("b").get_text(strip=True)), E(k.find("small").get_text(strip=True))) for k in kn)
    kh3 = kami.find("h3").get_text(strip=True)
    trs = []
    for tr in kami.find("table").find_all("tr"):
        th = tr.find("th").get_text(strip=True); td = inner(tr.find("td"))
        if th == "Contoh Mitra KAP": th = "KAP Rekanan"
        if th == "Contoh Mitra KJA": th = "KJA Rekanan"
        td = td.replace(", dipimpin Akuntan Berpraktik izin AB.715", "")
        trs.append('<tr><th scope="row">%s</th><td>%s</td></tr>' % (E(th), td))
    g_kred = '<div class="rx-tb"><table><tbody>%s</tbody></table></div>' % "".join(trs)

    def det(title, note, body, tag="h2"):
        return '<details><summary><%s>%s</%s><small>%s</small></summary><div class="bd">%s</div></details>' % (tag, E(title), tag, E(note), body)
    acc = ('<section class="rx-s" id="kami"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Selengkapnya</p>'
           '<p class="rx-h">Yang Sering Ditanyakan Sebelum Memilih</p></div><div class="rx-acc">%s%s%s%s%s</div>%s</div></section>'
           % (det(by_title(needs), "%d kebutuhan, langsung chat" % len(need_a), g_need),
              det(by_title(damp), "%d langkah" % len(st), g_damp),
              det(by_title(salah), "5 titik bocor", g_salah),
              det(by_title(kami), "Bukan KAP, izin dicek, biaya terbuka, NDA", g_kami),
              det(kh3, "Nomor izin dan registri", g_kred, "h3"),
              '<div class="rx-share">%s</div>' % share))

    pb_h = '<div class="wrap" style="padding-bottom:8px">%s</div>' % pb
    new_inner = ("\n<!--rx13-home-->" + hero_h + str(want) + peta + screen_h + cek_h + rek + acc + str(final) + JS_HOME + "\n" + pb_h + "\n")
    lost = [u for u in links_of(old_main) if u not in links_of(new_inner)]
    assert not lost, "CA: link hilang %s" % lost[:5]
    # ganti isi main
    m = re.search(r'(<main[^>]*>)', t)
    i = m.end(); j = t.rindex("</main>")
    t = t[:i] + new_inner + t[j:]
    t = t.replace("</head>", '<style id="rx13-home">%s</style>\n</head>' % CSS_HOME.replace("\n", ""), 1)
    return t


def by_title(sec):
    return (sec.find("h2")).get_text(" ", strip=True)


# ====================== beranda US ======================
def home_us(t):
    if "<!--rx13-home-->" in t: return t
    soup = BeautifulSoup(t, "html.parser")
    main = soup.find("main")
    old_main = str(main)
    by = {}
    for s in main.find_all("section", recursive=False):
        h = s.find("h2") or s.find("h1")
        by[h.get_text(" ", strip=True)] = s
    hero = main.find("section", class_="hero")
    want = main.find("section", id="mulai-cepat")
    kalk = main.find("section", id="kalkulator")
    upd = main.find("section", id="update-sak")
    needs = by["Atau Langsung Pilih Kebutuhan"]
    jad = main.find("section", id="jadwal")
    sa = main.find("section", id="standar-audit")
    peta = by["Peta Memilih Kerangka SAK"]
    lini = by["Linimasa Perubahan SAK"]
    calk = by["Struktur CALK Format Auditor"]
    final = main.find("section", class_="final")
    tail = old_main[old_main.index("<!--lp:start-->"):old_main.rindex("</main>")]
    wants = {a.find("b").get_text(strip=True): a for a in want.find_all("a")}
    wa_fa = wa("Halo Pak Ananta, saya dari updatesak.com. Sudah coba pelajari standarnya, tapi ingin dibantu tim FA Indonesia untuk penerapannya.")

    def li(a_or_txt, href=None):
        if href is None: return '<li><a href="%s">%s</a></li>' % (E(a_or_txt["href"]), E(a_or_txt.find("b").get_text(strip=True)))
        return '<li><a href="%s">%s</a></li>' % (E(href), E(a_or_txt))
    cek118 = [a for a in hero.find("div", class_="cta").find_all("a") if "cek-psak-118" in a["href"]][0]
    stair = ('<section class="rx-s alt" id="mulai-cepat"><div class="wrap"><div class="rx-hd"><h2 class="rx-ey">%s</h2>'
             '<p class="rx-h">Pelajari, Kerjakan Sendiri, atau Serahkan.</p><p class="rx-lead">Tiga tahap, makin ke kanan makin '
             'sedikit yang perlu Anda kerjakan sendiri.</p></div><div class="rx-st">'
             '<div class="c"><span class="n">Tahap 01</span><b class="h">Pelajari Standarnya</b><p>Ringkasan PSAK, SAK EP, SAK EMKM, '
             'dan Standar Audit, lengkap dengan contoh kalimat CALK.</p><ul>%s%s%s</ul></div>'
             '<div class="c"><span class="n">Tahap 02</span><b class="h">Kerjakan Sendiri</b><p>Kertas kerja Excel berumus dan kalkulator '
             'yang menyusun laporan keuangan serta CALK langsung di browser.</p><ul>%s%s%s</ul></div>'
             '<div class="c end"><span class="n">Tahap 03</span><b class="h">Masih Bingung? Serahkan ke Tim FA Indonesia</b>'
             '<p>Penerapan PSAK, penyusunan laporan keuangan, sampai audit dikerjakan tim CA dan CPA.</p><ul>%s%s%s</ul></div>'
             '</div></div></section>'
             % (E(by_title(want)), li(wants["Update SAK Terbaru"]), li("Daftar PSAK dan Panduan", "/eksplor/"), li(wants["Belajar Standar Audit"]),
                li("Kertas Kerja PSAK (Excel)", "/kertas-kerja/"), li(wants["Cek Standar Akuntansi Saya"]),
                li(cek118.get_text(strip=True), cek118["href"]),
                li("Lihat yang Bisa Dikerjakan Tim", "#dibantu"), li(wants["Cari Akuntan Berizin"]), li("Tanya Ananta, CPA", wa_fa)))

    # update sak: 7 kartu tanpa lipatan
    uh = upd.find("div", class_="head")
    g_upd = '<div class="rx-grid">%s</div>' % "".join(
        '<a href="%s"><b>%s</b><small>%s</small><em>%s</em></a>' % (E(a["href"]), E(a.find("b").get_text(strip=True)),
                                                                   E(a.find("small").get_text(strip=True)), E(a.find("em").get_text(strip=True)))
        for a in upd.find_all("a", class_="need"))
    upd_h = ('<section class="rx-s" id="update-sak"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Tahap 01 · Pelajari</p>'
             '<h2 class="rx-h">%s</h2><p class="rx-lead">%s</p></div>%s</div></section>'
             % (E(uh.find("h2").get_text(strip=True)), E(uh.find("p").get_text(strip=True)), g_upd))

    # pohon keputusan + linimasa
    tm = peta.find("div", class_="tree-m")
    tq = [q.get_text(strip=True) for q in tm.find_all("div", class_="tq")]
    tr = [(r.find("span").get_text(strip=True), r.find("b").get_text(strip=True), r.find("b")["style"]) for r in tm.find_all("div", class_="tr")]
    q2 = tq[1].split(":", 1)[1].strip() if ":" in tq[1] else tq[1]

    def res(r): return '<div class="row"><span class="lb">%s</span><span class="res" style="%s">%s</span></div>' % (E(r[0]), E(r[2]), E(r[1]))
    dt = ('<div aria-label="Diagram keputusan kerangka SAK" class="rx-dt" id="tree"><div class="q">%s</div><div class="ans">%s'
          '<div class="row"><span class="lb">Tidak</span><span></span></div></div><div class="q">%s</div><div class="ans">%s%s</div>'
          '<div class="q" style="border-style:dashed;font-weight:500">Ada Akad Syariah?</div><div class="ans" style="padding-bottom:0">%s</div></div>'
          % (E(tq[0]), res(tr[0]), E(q2), res(tr[1]), res(tr[2]), res(tr[3])))
    pts = lini.find_all("div", class_="pt")
    tl = '<ol class="rx-tl">%s</ol>' % "".join(
        '<li%s><time>%s</time><div class="tg">%s</div></li>' % (' class="now"' if "now" in (p.get("class") or []) else "",
                                                               E(p.find("time").get_text(strip=True)),
                                                               "".join("<span>%s</span>" % E(s.get_text(strip=True)) for s in p.find("div", class_="tags").find_all("span")))
        for p in pts)
    updp = lini.find("p", id="sakUpd")
    two = ('<section class="rx-s alt" id="peta"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Dua Bagan Ringkas</p>'
           '<p class="rx-h">Standar Mana, Berlaku Kapan</p></div><div class="rx-two"><div><h2 class="rx-sub">%s</h2>%s</div>'
           '<div><h2 class="rx-sub">%s</h2>%s<p class="rx-src" id="sakUpd">%s</p>'
           '<p class="rx-more"><a class="btn btn-ghost" href="/eksplor/">Linimasa Lengkap sampai 2029</a></p></div></div></div></section>'
           % (E(by_title(peta)), dt, E(by_title(lini)), tl, E(updp.get_text(strip=True))))

    # akordeon: standar audit, sertifikasi, struktur CALK
    sah = sa.find("div", class_="head")
    g_sa = '<p>%s</p><div class="rx-grid">%s</div><p class="rx-more"><a class="btn arrow" href="/standar-audit/">%s</a></p>' % (
        E(sah.find("p").get_text(strip=True)),
        "".join('<a href="%s"><span class="n">%s</span><b>%s</b><small>%s</small></a>' % (
            E(a["href"]), E(a.find("b").get_text(strip=True)), E(a.find("span").get_text(strip=True)), E(a.find("small").get_text(strip=True)))
            for a in sa.find_all("a", class_="sacard")), E(sa.find("a", class_="btn").get_text(strip=True)))
    jh = jad.find("div", class_="head")
    g_jad = '<p>%s</p><div class="rx-grid">%s</div><p class="rx-more"><a class="btn arrow" href="/jadwal-ujian/">%s</a></p>' % (
        E(jh.find("p").get_text(strip=True)),
        "".join('<a href="%s"><span class="n">%s</span><b>%s</b><small>%s</small><em>%s</em></a>' % (
            E(a["href"]), E(a.find("span", class_="st").get_text(strip=True)), E(a.find("b").get_text(strip=True)),
            E(a.find("small").get_text(strip=True)), E(a.find("em").get_text(strip=True))) for a in jad.find_all("a", class_="excard")),
        E(jad.find("a", class_="btn").get_text(strip=True)))
    pg = calk.find("div", class_="pages").find_all("div", recursive=False)
    g_calk = ('<div class="rx-grid">%s</div><p class="rx-more"><a class="btn arrow" data-mode="calk" href="#kalkulator">Coba Kalkulator CALK</a></p>'
              % "".join('<div><span class="n">%s</span><b>%s</b><small>%s</small></div>' % (
                  E(d.find("b").get_text(strip=True)), E(d.find("span").get_text(strip=True)), E(d.find("small").get_text(strip=True))) for d in pg))

    def det(title, note, body):
        return '<details><summary><h2>%s</h2><small>%s</small></summary><div class="bd">%s</div></details>' % (E(title), E(note), body)
    acc = ('<section class="rx-s"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Selengkapnya</p>'
           '<p class="rx-h">Untuk Auditor, Peserta Ujian, dan Penyusun CALK</p></div><div class="rx-acc">%s%s%s</div></div></section>'
           % ('<details id="standar-audit"><summary><h2>%s</h2><small>49 standar, 6 paling dicari</small></summary><div class="bd">%s</div></details>'
              % (E(by_title(sa)), g_sa),
              '<details id="jadwal"><summary><h2>%s</h2><small>CPA, CA, CPMA, BKP</small></summary><div class="bd">%s</div></details>'
              % (E(by_title(jad)), g_jad),
              det(by_title(calk), "5 bagian", g_calk)))

    # dibantu tim FA
    na = needs.find_all("a", class_="need")
    g_need = '<div class="rx-grid">%s</div>' % "".join(
        '<a href="%s"%s%s><b>%s</b><small>%s</small><em>%s</em></a>' % (
            E(a["href"]), ' data-mode="%s"' % a["data-mode"] if a.get("data-mode") else "",
            ' rel="noopener" target="_blank"' if a["href"].startswith("https://wa.me") else "",
            E(a.find("b").get_text(strip=True)), E(a.find("small").get_text(strip=True)), E(a.find("em").get_text(strip=True))) for a in na)
    dib = ('<section class="rx-s alt" id="dibantu"><div class="wrap"><div class="rx-hd"><p class="rx-ey">Tahap 03 · Serahkan</p>'
           '<p class="rx-h">Dikerjakan Tim FA Indonesia</p><p class="rx-lead">UpdateSAK dikelola FA Indonesia. Bila waktu Anda lebih '
           'berharga untuk mengurus usaha, tiga pekerjaan ini bisa langsung diserahkan.</p></div><div class="rx-rk">'
           '<div class="c main"><span class="m">Standar</span><b>Penerapan PSAK</b><span class="i">PSAK 109, 115, 116, 118, 219</span>'
           '<p>Pemetaan dampak, kebijakan akuntansi, jurnal transisi, sampai pengungkapan di CALK.</p>'
           '<a class="go" href="https://faindonesia.co.id/konsultan-penerapan-psak/">Lihat Penerapan PSAK</a></div>'
           '<div class="c"><span class="m"><img alt="Logo KJA Farhani K.N." height="28" loading="lazy" src="/img/kja-farhani-mark.png" width="15"/>Laporan Keuangan</span>'
           '<b>Penyusunan Laporan Keuangan</b><span class="i">Oleh KJA Farhani K.N.</span>'
           '<p>Laporan keuangan lengkap dengan arus kas dan CALK, siap dipakai bank, pajak, atau auditor.</p>'
           '<a class="go" href="https://faindonesia.co.id/jasa-penyusunan-laporan-keuangan/">Lihat Jasa Penyusunan</a></div>'
           '<div class="c"><span class="m"><img alt="Logo KAP DHN &amp; Rekan" height="28" loading="lazy" src="/img/kap-dhn-mark.png" width="24"/>Audit</span>'
           '<b>Audit Laporan Keuangan</b><span class="i">Oleh KAP DHN &amp; Rekan, Terdaftar OJK</span>'
           '<p>Audit umum untuk bank, tender, investor, dan laporan tahunan PT. Penyusun dan auditor selalu pihak berbeda.</p>'
           '<a class="go" href="https://faindonesia.co.id/jasa-audit-laporan-keuangan/">Lihat Jasa Audit</a></div>'
           '</div><div class="rx-acc" style="margin-top:30px"><details><summary><h2>%s</h2><small>%d pilihan</small></summary>'
           '<div class="bd">%s</div></details></div></div></section>' % (E(by_title(needs)), len(na), g_need))

    # hero tanpa perubahan isi; kalkulator apa adanya
    new_inner = ("\n<!--rx13-home-->" + str(hero) + stair + str(kalk) + upd_h + two + acc + dib + str(final) + JS_HOME + "\n" + tail + "\n")
    lost = [u for u in links_of(old_main) if u not in links_of(new_inner)]
    assert not lost, "US: link hilang %s" % lost[:5]
    m = re.search(r'(<main[^>]*>)', t)
    i = m.end(); j = t.rindex("</main>")
    t = t[:i] + new_inner + t[j:]
    t = t.replace("</head>", '<style id="rx13-home">%s</style>\n</head>' % CSS_HOME.replace("\n", ""), 1)
    return t


H1_EM = [("<h1>Sebelum Bayar Akuntan, Pastikan Dulu Jasa yang Anda Butuhkan.</h1>",
          "<h1>Sebelum Bayar Akuntan, <em>Pastikan Dulu Jasa yang Anda Butuhkan.</em></h1>"),
         ("<h1>Standar Akuntansi yang Langsung Bisa Dikerjakan.</h1>",
          "<h1>Standar Akuntansi yang <em>Langsung Bisa Dikerjakan.</em></h1>")]


def magang(t):
    """Bos 13 Nov: halaman magang diarahkan ke email, tidak ada tombol WhatsApp."""
    m = re.search(r'href="(mailto:ananta@faindonesia\.co\.id\?subject=Magang[^"]*)"', t)
    if not m: return t
    mail = m.group(1)
    t = re.sub(r'<a class="btn btn-wa btn-sm" href="https://wa\.me/[^"]*"[^>]*>[^<]*</a>',
               '<a class="btn btn-wa btn-sm" href="%s">Kirim Lamaran via Email</a>' % mail, t)
    t = re.sub(r'<!--dhn-->.*?<!--/dhn-->', '<!--dhn--><!--/dhn-->', t, flags=re.S)
    t = re.sub(r'<!--rx13f-->.*?<!--/rx13f-->', '', t, flags=re.S)
    return t


# ====================== jalan ======================
VCA = ver(CSS_ALL + CSS_CA); VUS = ver(CSS_ALL)


def run(root, site):
    wt(os.path.join(root, "css", "rx13.css"), CSS_ALL + (CSS_CA if site == "ca" else ""), site)
    for d, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith(".html"): continue
            p = os.path.join(d, f)
            rel = os.path.relpath(d, root).replace(os.sep, "/")
            rel = "" if rel == "." else rel
            if f != "index.html": rel = rel or f
            t = rd(p); o = t
            if rel == "" and f == "index.html":
                t = home_ca(t) if site == "ca" else home_us(t)
                t = re.sub(r'<style id="rx13-home">.*?</style>', lambda m: '<style id="rx13-home">%s</style>' % CSS_HOME.replace("\n", ""), t, count=1, flags=re.S)
                for a, b in H1_EM: t = t.replace(a, b)
            t = common(t, rel, site)
            if site == "ca" and rel == "magang": t = magang(t)
            if t != o: wt(p, t, site)


if __name__ == "__main__":
    run(CA, "ca"); run(US, "us")
    print("caus_rapi_20261113: CA %d file, US %d file%s" % (N["ca"], N["us"], " (dry)" if DRY else ""))
