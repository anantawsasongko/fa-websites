# -*- coding: utf-8 -*-
"""Sederhanakan beranda faindonesia.co.id (gaya cariakuntan.com: singkat, banyak bagan).
Section detail dipindah ke tab yang sesuai:
  /layanan/  : layanan, paket, fee, rekam jejak, arsip, galeri, pendiri, grup, ekosistem, afiliasi
  /unduhan/  : materi gratis (unduhan), publikasi, kabar kanal FA  (ditautkan dari tab E-Book)
Sumber asli disimpan di backup/index-v58-full-20261025.html. Script idempoten: selalu membangun ulang dari backup.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
SRC = os.path.join(HERE, "backup", "index-v58-full-20261025.html")
h = open(SRC, encoding="utf-8").read()

def sec(id_):
    m = re.search(r'<section class="block[^"]*"[^>]*id="%s"[^>]*>.*?</section>\n?' % id_, h, re.S)
    return m.group(0)

i_main = h.find('<main id="top">')
i_mend = h.find('</main>')
HEAD = h[:i_main]                      # head + header (nav)
TAIL = h[i_mend:]                      # </main> footer scripts
main = h[i_main:i_mend]
hero_end = main.find('<section class="block" id="pendekatan">')
HERO = main[len('<main id="top">'):hero_end]
PEND = sec("pendekatan")
KONTAK = sec("kontak")

MOVE_L = ["layanan", "paket", "fee", "rekam", "arsip", "pendiri", "grup", "ekosistem", "afiliasi"]
MOVE_B = ["unduhan", "publikasi"]
MOVE_E = ["galeri", "kabar"]
WHERE = {k: "/layanan/" for k in MOVE_L}
WHERE.update({k: "/buku/" for k in MOVE_B})
WHERE.update({k: "/artikel/" for k in MOVE_E})

def set_alt(blocks):
    out = []
    for n, b in enumerate(blocks):
        b = re.sub(r'<section class="block( alt)?( feedsec)?"', lambda m: '<section class="block%s%s"' % (" alt" if n % 2 else "", m.group(2) or ""), b, count=1)
        out.append(b)
    return "".join(out)

# ---------------- teks baru (ID / EN / ZH) ----------------
T = {
 "hs01": ("Peta Layanan", "Service Map", "服务地图"),
 "hs02": ("Satu pintu, tiga jalur <em>uang masuk.</em>", "One door, three routes to <em>funding.</em>", "一个入口，三条<em>资金</em>路径。"),
 "hs03": ("Perusahaan Anda", "Your Company", "您的公司"),
 "hs04": ("Dari UMKM sampai calon Tbk", "From small businesses to IPO candidates", "从小微企业到上市候选公司"),
 "hs05": ("Kredit Bank", "Bank Credit", "银行贷款"),
 "hs06": ("Due diligence sampai pencairan", "Due diligence to disbursement", "从尽职调查到放款"),
 "hs07": ("Investor &amp; IPO", "Investors &amp; IPO", "投资者与 IPO"),
 "hs08": ("Pencarian investor, M&amp;A, jalur IPO", "Investor search, M&amp;A, IPO path", "寻找投资者、并购、IPO 路径"),
 "hs09": ("GCG &amp; Laporan Keuangan", "GCG &amp; Financial Statements", "治理与财务报表"),
 "hs10": ("Fondasi yang membuat dua jalur di atas lolos", "The foundation that gets both routes approved", "让前两条路径通过的基础"),
 "hs11": ("Dana Masuk", "Funds In", "资金到位"),
 "hs12": ("Kredit cair, investor masuk, atau transaksi tuntas", "Loan disbursed, investor in, or deal closed", "贷款发放、投资者入股或交易完成"),
 "hs13": ("Rekam Jejak", "Track Record", "业绩"),
 "hs14": ("Kredit perbankan yang <em>sudah cair.</em>", "Bank credit <em>already disbursed.</em>", "<em>已发放</em>的银行贷款。"),
 "hs15": ("Kumulatif per jenis bank, dalam Rp miliar", "Cumulative by bank type, in Rp billion", "按银行类型累计，单位：十亿印尼盾"),
 "hs16": ("Ditambah BPD, BPR, dan kredit sindikasi, serta pendanaan investor hingga US$3 juta. Total mendekati Rp1 triliun.", "Plus regional banks, rural banks and syndicated loans, and investor funding up to US$3 million. Close to Rp1 trillion in total.", "另有地方银行、农村银行及银团贷款，以及最高 300 万美元的投资者资金。合计接近 1 万亿印尼盾。"),
 "hs17": ("Lihat Rekam Jejak Lengkap", "See Full Track Record", "查看完整业绩"),
 "hs18": ("Untuk Siapa", "Who It Is For", "服务对象"),
 "hs19": ("Semua skala perusahaan, <em>satu standar.</em>", "Every company size, <em>one standard.</em>", "各种规模的企业，<em>同一标准。</em>"),
 "hs20": ("Dari usaha kecil sampai calon emiten, kebutuhannya berbeda, standar kerjanya sama", "From small businesses to IPO candidates: different needs, the same working standard", "从小企业到上市候选公司：需求不同，标准一致"),
 "hs21": ("Setiap klien ditangani langsung oleh Ananta, CPA", "Every client is handled personally by Ananta, CPA", "每位客户均由 Ananta, CPA 亲自负责"),
 "hs60": ("UMKM", "Small Business", "小微企业"), "hs61": ("LK SAK EMKM, siap kredit", "SAK EMKM statements, loan-ready", "小微准则报表，可申请贷款"),
 "hs62": ("Menengah", "Mid-Sized", "中型企业"), "hs63": ("Audit, kredit bank, GCG", "Audit, bank credit, governance", "审计、银行贷款、治理"),
 "hs64": ("Besar &amp; Grup", "Large &amp; Groups", "大型企业与集团"), "hs65": ("Sindikasi, investor, M&amp;A", "Syndication, investors, M&amp;A", "银团贷款、投资者、并购"),
 "hs66": ("Calon Tbk &amp; BUMN", "IPO Candidates &amp; SOEs", "上市候选与国企"), "hs67": ("IPO, komite audit, pelaporan", "IPO, audit committee, reporting", "IPO、审计委员会、报告"),
 "hs68": ("Klien penugasan penuh per tahun, semua skala perusahaan", "Full engagements per year, every company size", "每年全程服务客户，覆盖各种规模"),
 "hs22": ("Rumah Sakit", "Hospitals", "医院"), "hs23": ("BPR", "Rural Banks (BPR)", "农村银行"),
 "hs24": ("Kontraktor", "Contractors", "承包商"), "hs25": ("Logistik &amp; Kargo", "Logistics &amp; Cargo", "物流与货运"),
 "hs26": ("Farmasi &amp; Kimia", "Pharma &amp; Chemicals", "制药与化工"), "hs27": ("Klinik &amp; Kecantikan", "Clinics &amp; Beauty", "诊所与美容"),
 "hs28": ("Cara Mulai", "How to Start", "如何开始"),
 "hs29": ("Empat langkah, <em>satu orang.</em>", "Four steps, <em>one person.</em>", "四个步骤，<em>一位负责人。</em>"),
 "hs30": ("Chat", "Chat", "沟通"), "hs31": ("Ceritakan kebutuhan lewat WhatsApp atau email", "Tell us what you need via WhatsApp or email", "通过 WhatsApp 或邮件说明需求"),
 "hs32": ("Diagnosis", "Diagnosis", "诊断"), "hs33": ("Baca laporan terakhir, petakan rasio dan jalur yang realistis", "Read your latest reports, map ratios and a realistic route", "阅读最新报表，梳理比率与可行路径"),
 "hs34": ("NDA &amp; Kontrak", "NDA &amp; Engagement", "保密协议与合同"), "hs35": ("Retainer bulanan plus success fee saat dana masuk", "Monthly retainer plus success fee when funds arrive", "月度顾问费加资金到位后的成功费"),
 "hs36": ("Eksekusi", "Execution", "执行"), "hs37": ("Dikawal sampai laporan terbit atau dana cair", "Guided until reports are issued or funds are disbursed", "全程陪同至报表出具或资金到位"),
 "hs38": ("Jelajahi", "Explore", "浏览"),
 "hs39": ("Layanan &amp; Rekam Jejak", "Services &amp; Track Record", "服务与业绩"), "hs40": ("Paket, fee, penugasan, dan profil tim", "Packages, fees, engagements and team", "套餐、费用、项目与团队"),
 "hs41": ("Apps", "Apps", "应用"), "hs42": ("FA Jupiter, FA Saturn, FA Venus", "FA Jupiter, FA Saturn, FA Venus", "FA Jupiter、FA Saturn、FA Venus"),
 "hs43": ("E-Book &amp; Materi", "E-Books &amp; Materials", "电子书与资料"), "hs44": ("Buku Penerbit FA, materi gratis, dan publikasi", "Penerbit FA books, free materials and publications", "Penerbit FA 图书、免费资料与出版物"),
 "hs45": ("Eksplor", "Explore", "探索"), "hs46": ("Berita, artikel, dan galeri foto", "News, articles and photo gallery", "新闻、文章与图库"),
 "hs47": ("Butuh KAP, KJPP, atau konsultan pajak?", "Need an audit firm, valuer or tax consultant?", "需要会计师事务所、评估师或税务顾问？"),
 "hs48": ("Cek Dulu di CariAkuntan", "Screen First at CariAkuntan", "先在 CariAkuntan 筛选"),
 "hs49": ("Layanan &amp; Rekam Jejak", "Services &amp; Track Record", "服务与业绩"),
 "hs50": ("Materi &amp; Publikasi", "Materials &amp; Publications", "资料与出版物"),
 "hs51": ("Kembali ke Beranda", "Back to Home", "返回首页"),
 "hs52": ("E-Book berbayar ada di Toko Buku Penerbit FA", "Paid e-books are in the Penerbit FA Bookstore", "付费电子书请见 Penerbit FA 书店"),
}
def t(k, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-i18n="{k}">{T[k][0]}</{tag}>'

WA = "https://wa.me/6282245260121"

CSS = r'''<style id="home-simple">
.hs .wrap{max-width:1120px}
.hs h2.aph{margin-bottom:6px}
.hs .sub{color:var(--muted);font-size:.9rem;margin:0 0 28px}
/* peta layanan */
.map3{display:grid;grid-template-columns:1fr 1.25fr 1fr;align-items:center;gap:0;position:relative;margin-top:18px}
.map3 .node{border:1px solid var(--line);background:var(--surface);border-radius:12px;padding:18px 18px;position:relative;z-index:1}
.map3 .node b{display:block;font-family:var(--serif);font-weight:400;font-size:1.35rem;line-height:1.2}
.map3 .node span{display:block;color:var(--muted);font-size:.78rem;margin-top:4px}
.map3 .node.start,.map3 .node.end{text-align:center}
.map3 .node.end{background:#fff;color:#171717;border-color:#fff}
.map3 .node.end span{color:#555}
.map3 .mid{display:grid;gap:14px;padding:0 46px;position:relative}
.map3 .mid .node{padding:14px 16px}
.map3 .mid .node b{font-size:1.15rem}
.map3 .mid .node .no{position:absolute;right:14px;top:12px;font-size:.7rem;color:var(--muted);letter-spacing:.1em}
.map3 svg.wires{position:absolute;inset:0;width:100%;height:100%;z-index:0;overflow:visible}
.map3 svg.wires path{fill:none;stroke:rgba(255,255,255,.35);stroke-width:1.4;stroke-dasharray:5 7;vector-effect:non-scaling-stroke;animation:flow 1.6s linear infinite}
@keyframes flow{to{stroke-dashoffset:-24}}
.map3 a.node{color:inherit;text-decoration:none;transition:border-color .25s,background .25s}
.map3 a.node:hover{border-color:#fff;background:#262626}
@media (max-width:820px){
 .map3{grid-template-columns:1fr;gap:26px}
 .map3 .mid{padding:0}
 .map3 svg.wires{display:none}
 .map3 .mid::before,.map3 .mid::after{content:"";position:absolute;left:50%;width:0;height:26px;border-left:1.4px dashed rgba(255,255,255,.4)}
 .map3 .mid::before{top:-26px}.map3 .mid::after{bottom:-26px}
}
/* bar chart */
.bars{display:grid;gap:12px;margin-top:8px;max-width:820px}
.bar{display:grid;grid-template-columns:120px 1fr 64px;align-items:center;gap:14px;font-size:.86rem}
.bar .tr{height:14px;background:#232323;border-radius:7px;overflow:hidden}
.bar .tr i{display:block;height:100%;width:0;background:linear-gradient(90deg,#8a8a8a,#fff);border-radius:7px;transition:width 1.4s cubic-bezier(.2,.7,.2,1)}
.bars.on .bar .tr i{width:var(--w)}
.bar .v{text-align:right;font-variant-numeric:tabular-nums;color:#fff}
.bar .n{color:var(--muted)}
.chartnote{color:var(--muted);font-size:.8rem;max-width:820px;margin:18px 0 0;line-height:1.6}
.total{display:inline-flex;align-items:baseline;gap:10px;border:1px solid var(--line);border-radius:999px;padding:8px 16px;margin:0 0 22px}
.total b{font-family:var(--serif);font-weight:400;font-size:1.6rem;white-space:nowrap}
@media (max-width:480px){.total{flex-direction:column;align-items:flex-start;gap:2px;border-radius:12px}}
.total span{color:var(--muted);font-size:.78rem}
.morelink{display:inline-block;margin-top:20px;color:#fff;font-size:.86rem;border-bottom:1px solid rgba(255,255,255,.4);text-decoration:none}
/* rentang aset */
.scale{position:relative;margin:34px 0 12px;max-width:820px}
.scale .axis{height:2px;background:#333;position:relative}
.scale .band{position:absolute;top:-9px;height:20px;left:0;width:0;border-radius:10px;background:linear-gradient(90deg,rgba(255,255,255,.25),#fff);transition:width 1.4s cubic-bezier(.2,.7,.2,1)}
.scale.on .band{width:92%}
.scale .tk{position:absolute;top:18px;transform:translateX(-50%);font-size:.72rem;color:var(--muted);white-space:nowrap}
.scale .tk::before{content:"";position:absolute;top:-22px;left:50%;height:10px;border-left:1px solid #555}
.scale .tk:first-of-type{transform:none}.scale .tk:first-of-type::before{left:0}
.tiers{position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:30px 0 8px;padding-top:30px}
.tiers .tband{position:absolute;top:8px;left:0;height:6px;width:0;border-radius:3px;background:linear-gradient(90deg,rgba(255,255,255,.2),#fff);transition:width 1.6s cubic-bezier(.2,.7,.2,1)}
.tiers.on .tband{width:100%}
.tiers>div{position:relative;padding-right:14px}
.tiers i{position:absolute;top:-28px;left:0;width:14px;height:14px;border-radius:50%;background:var(--paper);border:1.5px solid #fff}
.tiers>div:last-of-type i{background:#fff}
.tiers b{display:block;font-family:var(--serif);font-weight:400;font-size:1.25rem}
.tiers span{display:block;color:var(--muted);font-size:.78rem;margin-top:4px;line-height:1.5}
@media (max-width:720px){.tiers{grid-template-columns:1fr;gap:18px;padding:0 0 0 30px}
 .tiers .tband{top:0;left:6px;width:2px!important;height:0;background:linear-gradient(180deg,rgba(255,255,255,.2),#fff);transition:height 1.6s cubic-bezier(.2,.7,.2,1)}
 .tiers.on .tband{height:100%}.tiers i{top:4px;left:-30px}}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:40px}
.chips span{border:1px solid var(--line);border-radius:999px;padding:6px 12px;font-size:.78rem;color:#ddd}
.who{margin-top:16px;font-size:.86rem;color:#ddd}
/* langkah */
.steps4{list-style:none;margin:20px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:0;position:relative}
.steps4::before{content:"";position:absolute;top:22px;left:12%;right:12%;height:1px;background:linear-gradient(90deg,#555,#fff)}
.steps4 li{text-align:center;padding:0 10px;position:relative}
.steps4 .c{width:44px;height:44px;border-radius:50%;border:1px solid #fff;background:var(--paper);display:grid;place-items:center;margin:0 auto 14px;font-size:.8rem;position:relative;z-index:1}
.steps4 li:last-child .c{background:#fff;color:#171717}
.steps4 b{display:block;font-family:var(--serif);font-weight:400;font-size:1.2rem}
.steps4 span{display:block;color:var(--muted);font-size:.78rem;margin-top:4px;line-height:1.5}
@media (max-width:820px){
 .steps4{grid-template-columns:1fr;gap:18px}
 .steps4::before{top:22px;bottom:22px;left:22px;right:auto;width:1px;height:auto;background:linear-gradient(180deg,#555,#fff)}
 .steps4 li{display:grid;grid-template-columns:44px 1fr;gap:14px;text-align:left;padding:0}
 .steps4 .c{margin:0}
}
/* jelajahi */
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:18px}
.tiles a{border:1px solid var(--line);background:var(--surface);border-radius:12px;padding:18px;color:inherit;text-decoration:none;display:block;transition:border-color .25s,transform .25s}
.tiles a:hover{border-color:#fff;transform:translateY(-2px)}
.tiles svg{width:26px;height:26px;stroke:#fff;fill:none;stroke-width:1.5;margin-bottom:12px}
.tiles b{display:block;font-family:var(--serif);font-weight:400;font-size:1.2rem}
.tiles span{display:block;color:var(--muted);font-size:.78rem;margin-top:4px}
.tiles a::after{content:"\2192";display:block;margin-top:10px;font-size:.9rem}
.cabar{margin-top:18px;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;justify-content:space-between;border:1px dashed var(--line);border-radius:12px;padding:14px 18px;font-size:.86rem}
.cabar a{color:#fff}
@media (max-width:900px){.tiles{grid-template-columns:1fr 1fr}}
@media (max-width:480px){.tiles{grid-template-columns:1fr}.bar{grid-template-columns:92px 1fr 48px;gap:10px}}
/* pendekatan diringkas */
#pendekatan .svcintro{display:none}
.subhero{padding:120px 0 40px}
.subhero h1{font-family:var(--serif);font-weight:400;font-size:clamp(2rem,5vw,3.2rem);margin:0 0 8px}
.subhero a{color:var(--muted);font-size:.84rem}
</style>'''

ICON = {
 "lay": '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 14h8"/></svg>',
 "app": '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><rect x="14" y="14" width="6" height="6" rx="1"/></svg>',
 "book": '<svg viewBox="0 0 24 24"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5"/></svg>',
 "ins": '<svg viewBox="0 0 24 24"><path d="M4 19h16M6 16l4-5 3 3 5-7"/></svg>',
}

BANKS = [("Bank BUMN", 440, "440+"), ("Bank Syariah", 90, "90+"), ("Bank Swasta", 85, "85+")]
bars = "".join(f'<div class="bar"><span class="n">{n}</span><span class="tr"><i style="--w:{v/440*100:.0f}%"></i></span><span class="v">{lbl}</span></div>' for n, v, lbl in BANKS)

PETA = f'''<section class="block alt hs" id="peta">
<div class="wrap">
<div class="head"><p class="eyebrow" data-i18n="hs01">{T["hs01"][0]}</p><h2 class="aph" data-i18n="hs02">{T["hs02"][0]}</h2></div>
<div class="map3">
<svg class="wires" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
<path d="M29 50 C34 50 34 17 39 17"/><path d="M29 50 L39 50"/><path d="M29 50 C34 50 34 83 39 83"/>
<path d="M71 17 C76 17 76 50 81 50"/><path d="M71 50 L81 50"/><path d="M71 83 C76 83 76 50 81 50"/>
</svg>
<div class="node start">{t("hs03","b")}{t("hs04")}</div>
<div class="mid">
<a class="node" href="/konsultan-kredit-bank/"><em class="no">01</em>{t("hs05","b")}{t("hs06")}</a>
<a class="node" href="/konsultan-persiapan-ipo/"><em class="no">02</em>{t("hs07","b")}{t("hs08")}</a>
<a class="node" href="/pendampingan-gcg/"><em class="no">03</em>{t("hs09","b")}{t("hs10")}</a>
</div>
<div class="node end">{t("hs11","b")}{t("hs12")}</div>
</div>
</div>
</section>
'''

REKAM = f'''<section class="block hs" id="angka">
<div class="wrap">
<div class="head"><p class="eyebrow" data-i18n="hs13">{T["hs13"][0]}</p><h2 class="aph" data-i18n="hs14">{T["hs14"][0]}</h2></div>
<div class="total"><b>±Rp1 T</b>{t("hs15")}</div>
<div class="bars" data-on>{bars}</div>
<p class="chartnote" data-i18n="hs16">{T["hs16"][0]}</p>
<a class="morelink" href="/layanan/#rekam" data-i18n="hs17">{T["hs17"][0]}</a>
</div>
</section>
'''

SIAPA = f'''<section class="block alt hs" id="siapa">
<div class="wrap">
<div class="head"><p class="eyebrow" data-i18n="hs18">{T["hs18"][0]}</p><h2 class="aph" data-i18n="hs19">{T["hs19"][0]}</h2></div>
<p class="sub" data-i18n="hs20">{T["hs20"][0]}</p>
<div class="tiers" data-on><span class="tband" aria-hidden="true"></span>
<div><i></i>{t("hs60","b")}{t("hs61")}</div><div><i></i>{t("hs62","b")}{t("hs63")}</div><div><i></i>{t("hs64","b")}{t("hs65")}</div><div><i></i>{t("hs66","b")}{t("hs67")}</div>
</div>
<div class="chips">{"".join(t(k) for k in ["hs22","hs23","hs24","hs25","hs26","hs27"])}</div>
<p class="who" data-i18n="hs21">{T["hs21"][0]}</p>
</div>
</section>
'''

LANGKAH = f'''<section class="block hs" id="mulai">
<div class="wrap">
<div class="head"><p class="eyebrow" data-i18n="hs28">{T["hs28"][0]}</p><h2 class="aph" data-i18n="hs29">{T["hs29"][0]}</h2></div>
<ol class="steps4">
<li><span class="c">01</span><div>{t("hs30","b")}{t("hs31")}</div></li>
<li><span class="c">02</span><div>{t("hs32","b")}{t("hs33")}</div></li>
<li><span class="c">03</span><div>{t("hs34","b")}{t("hs35")}</div></li>
<li><span class="c">04</span><div>{t("hs36","b")}{t("hs37")}</div></li>
</ol>
</div>
</section>
'''

JELAJAH = f'''<section class="block alt hs" id="jelajahi">
<div class="wrap">
<div class="head"><p class="eyebrow" data-i18n="hs38">{T["hs38"][0]}</p></div>
<div class="tiles">
<a href="/layanan/">{ICON["lay"]}{t("hs39","b")}{t("hs40")}</a>
<a href="/apps/">{ICON["app"]}{t("hs41","b")}{t("hs42")}</a>
<a href="/buku/">{ICON["book"]}{t("hs43","b")}{t("hs44")}</a>
<a href="/artikel/">{ICON["ins"]}{t("hs45","b")}{t("hs46")}</a>
</div>
<div class="cabar"><span data-i18n="hs47">{T["hs47"][0]}</span><a href="https://cariakuntan.com/" target="_blank" rel="noopener" data-i18n="hs48">{T["hs48"][0]} &#8594;</a></div>
</div>
</section>
'''

ANIM = '''<script>(function(){var e=document.querySelectorAll('[data-on]');if(!('IntersectionObserver' in window)){e.forEach(function(x){x.classList.add('on')});return}
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('on');io.unobserve(x.target)}})},{threshold:.3});e.forEach(function(x){io.observe(x)})})();</script>'''

REDIR = '<script>(function(){var m={%s},h=location.hash.slice(1);if(m[h])location.replace(m[h]+"#"+h)})();</script>' % ",".join(f'"{k}":"{v}"' for k, v in WHERE.items())

def add_i18n(s):
    en = ", ".join(f'"{k}": "{v[1]}"' for k, v in T.items())
    zh = ", ".join(f'"{k}": "{v[2]}"' for k, v in T.items())
    a = s.find('var I18N={"en": {')
    assert a > 0
    s = s[:a] + 'var I18N={"en": {' + en + ", " + s[a + len('var I18N={"en": {'):]
    z = s.find('"zh": {', a)
    s = s[:z] + '"zh": {' + zh + ", " + s[z + len('"zh": {'):]
    return s

def fix_links(s, here):
    """here: path page ini ('/', '/layanan/', '/unduhan/')"""
    def rep(m):
        attr, id_ = m.group(1), m.group(2)
        tgt = WHERE.get(id_, "/")
        if tgt == here: return f'{attr}="#{id_}"'
        return f'{attr}="{tgt}#{id_}"'
    s = re.sub(r'(href)="/?#([a-z0-9-]+)"', rep, s)
    return s

# kotak ke-4 Lini Usaha: CariAkuntan (pendampingan)
CA_CARD = ('<a class="eco-ca" href="https://cariakuntan.com/" target="_blank" rel="noopener">'
           '<span class="lgbox ca-lg" aria-label="CariAkuntan"><span class="cabox">C<i>A</i></span><span class="caw">Cari<b>Akuntan</b></span></span>'
           '<span data-i18n="hs53">Pendampingan cari KAP, KJPP, dan profesi penunjang</span></a>')
T["hs53"] = ("Pendampingan cari KAP, KJPP, dan profesi penunjang", "Guidance to find audit firms, valuers and other professionals", "协助寻找会计师事务所、评估师及其他专业服务")
CSS = CSS.replace("</style>", """.eco a.eco-ca{background:var(--paper);padding:20px;min-width:0;display:grid;gap:10px;align-content:start;color:inherit;text-decoration:none;transition:background .25s}
.eco a.eco-ca:hover{background:#222}
.ca-lg{display:inline-flex;align-items:center;gap:10px;height:30px}
.eco .ca-lg .cabox{width:28px;height:30px;border:1.5px solid #fff;display:grid;place-items:center;font-family:Poppins,sans-serif;font-size:10px;line-height:1;letter-spacing:.04em;font-weight:500;padding-top:1px;color:#fff;text-align:center}
.eco .ca-lg .cabox i{font-style:normal;color:#1F5BFF}
.eco .ca-lg .caw{white-space:nowrap;display:inline;margin:0;font-family:Poppins,sans-serif;font-weight:600;font-size:21px;letter-spacing:-.01em;color:#fff}
.eco .ca-lg .caw b{display:inline;margin:0;font-weight:600;color:#1F5BFF}
@media (max-width:600px){.eco .ca-lg{gap:7px}.eco .ca-lg .caw{font-size:16px}.eco .ca-lg .cabox{width:24px;height:26px;font-size:9px}}
:root[data-theme="light"] .cabox{border-color:#171717}:root[data-theme="light"] .caw{color:#171717}
</style>""", 1)
_eco_old = sec("ekosistem")
_eco_new = _eco_old.replace('</div>\n<p class="note"', CA_CARD + '</div>\n<p class="note"', 1)
assert _eco_new != _eco_old
_orig_sec = sec
def sec(id_):
    return _eco_new if id_ == "ekosistem" else _orig_sec(id_)

# ---------------- BERANDA ----------------
hero = HERO.replace('href="#rekam"', 'href="/layanan/#rekam"').replace('<span data-i18n="k16">Klien baru per tahun, beraset Rp1–500 miliar</span>', '<span data-i18n="hs68">' + T['hs68'][0] + '</span>')
home = HEAD + '<main id="top">' + hero + PETA + REKAM + PEND.replace('class="block"', 'class="block hs"', 1) + SIAPA + LANGKAH + JELAJAH + KONTAK.replace('class="block alt"', 'class="block"', 1) + TAIL
home = home.replace("</head>", CSS + "</head>", 1)
home = home.replace("</body>", ANIM + REDIR + "</body>", 1)
home = add_i18n(home)
home = fix_links(home, "/")
open(os.path.join(FA, "index.html"), "w", encoding="utf-8").write(home)

# ---------------- halaman tab ----------------
def subpage(path, title, desc, h1key, ids):
    head = HEAD
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head, count=1)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', head, count=1)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', head, count=1)
    head = head.replace('<link rel="canonical" href="https://faindonesia.co.id/">', f'<link rel="canonical" href="https://faindonesia.co.id{path}">')
    head = head.replace('<meta property="og:url" content="https://faindonesia.co.id/">', f'<meta property="og:url" content="https://faindonesia.co.id{path}">')
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    bc = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
          '{"@type":"ListItem","position":1,"name":"Beranda","item":"https://faindonesia.co.id/"},'
          f'{{"@type":"ListItem","position":2,"name":"{title.split(" | ")[0]}","item":"https://faindonesia.co.id{path}"}}]}}</script>')
    head = head.replace("</head>", bc + CSS + "</head>", 1)
    top = (f'<section class="block subhero hs"><div class="wrap"><p class="eyebrow">FA Indonesia</p>'
           f'<h1 data-i18n="{h1key}">{T[h1key][0]}</h1><a href="/" data-i18n="hs51">{T["hs51"][0]}</a></div></section>\n')
    extra = ""
    if path == "/unduhan/":
        extra = f'<div class="wrap" style="padding-top:0"><p class="cabar"><span data-i18n="hs52">{T["hs52"][0]}</span><a href="/buku/">/buku/ &#8594;</a></p></div>'
    body = set_alt([sec(i) for i in ids] + [KONTAK])
    s = head + '<main id="top">' + top + extra + body + TAIL
    s = s.replace("</body>", ANIM + "</body>", 1)
    s = add_i18n(s)
    s = fix_links(s, path)
    # path relatif -> absolut
    s = re.sub(r'(src|href|data-full|srcset)="(?!https?:|/|#|mailto:|tel:|data:|javascript:)([^"]+)"', r'\1="/\2"', s)
    s = s.replace('href="/#top"', 'href="#top"').replace('url("img/', 'url("/img/')
    d = os.path.join(FA, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(s)

subpage("/layanan/", "Layanan, Paket, Fee dan Rekam Jejak | FA Indonesia",
        "Layanan FA Indonesia: pendampingan kredit bank, investor, M&amp;A, IPO dan GCG. Paket, model fee, rekam jejak pendanaan, galeri, dan profil tim Ananta W. Sasongko, CPA.",
        "hs49", MOVE_L)

# ---------------- link di halaman lain + sitemap ----------------
for root, _, files in os.walk(FA):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f)
        if p in (os.path.join(FA, "index.html"), os.path.join(FA, "layanan", "index.html")): continue
        s = open(p, encoding="utf-8").read()
        s2 = re.sub(r'href="/#(%s)"' % "|".join(WHERE), lambda m: f'href="{WHERE[m.group(1)]}#{m.group(1)}"', s)
        if s2 != s: open(p, "w", encoding="utf-8").write(s2)

import shutil
TAILRAW = h[h.find('</footer>'):]
def grab(pat):
    m = re.search(pat, TAILRAW, re.S); assert m, pat; return m.group(0)
SH_TOAST = grab(r'<div class="shtoast" id="shtoast".*?</script>')
LEAD = grab(r'<div id="leadModal".*?</div>\s*<script>\(function\(\)\{var G=.*?</script>')
LIGHT = grab(r"<script>\s*\(function\(\)\{var d=document.getElementById\('lightbox'\).*?</script>")
FEEDJS = grab(r'<script id="feed-js">.*?</script>')
HOMECSS = absol_css = "".join(re.findall(r'<style[^>]*>(.*?)</style>', h[:h.find('</head>')], re.S)).replace('url("img/', 'url("/img/')
def absol(x):
    x = re.sub(r'(src|href|data-full|srcset|data-story)="(?!https?:|/|#|mailto:|tel:|data:|javascript:)([^"]+)"', r'\1="/\2"', x)
    return x.replace('url("img/', 'url("/img/')
def inject(rel, blocks, tail, css="", subs=(), mid=(), jump=""):
    pth = os.path.join(FA, rel)
    b = open(pth, encoding="utf-8").read()
    b = re.sub(r'<div id="ke-unduhan".*?</div>\n?', '', b, flags=re.S)
    b = re.sub(r'<!--fa-inj-->.*?<!--/fa-inj-->\n?', '', b, flags=re.S)
    b = re.sub(r'<!--fa-injt-->.*?<!--/fa-injt-->\n?', '', b, flags=re.S)
    b = re.sub(r'<style id="fa-injc">.*?</style>', '', b, flags=re.S)
    for a, c in subs: b = b.replace(a, c)
    b = re.sub(r'<!--fa-jump-->.*?<!--/fa-jump-->', '', b, flags=re.S)
    body = absol(fix_links(set_alt(blocks), "/" + rel.split("/")[0] + "/"))
    i = b.rfind("<footer")
    b = b[:i] + "<!--fa-inj-->" + body + "<!--/fa-inj-->\n" + b[i:]
    for marker, blk in mid:
        k = b.find(marker); assert k > 0, marker
        b = b[:k] + "<!--fa-inj-->" + absol(fix_links(blk, "/" + rel.split("/")[0] + "/")) + "<!--/fa-inj-->" + b[k:]
    if jump:
        k = b.find('<div class="bk-grid">'); b = b[:k] + "<!--fa-jump-->" + jump + "<!--/fa-jump-->" + b[k:]
    b = b.replace("</body>", "<!--fa-injt-->" + absol(tail) + "<!--/fa-injt-->\n</body>", 1)
    b = re.sub(r'<style id="fa-injbase">.*?</style>', '', b, flags=re.S)
    b = b.replace('<meta charset="utf-8">', '<meta charset="utf-8"><style id="fa-injbase">' + HOMECSS + "</style>", 1)
    if css: b = b.replace("</head>", '<style id="fa-injc">' + css + "</style></head>", 1)
    open(pth, "w", encoding="utf-8").write(b)

BK_CSS = (".bk-steps li{position:relative;padding:18px 18px 18px 58px!important;line-height:1.6}"
          ".bk-steps li:before{position:absolute;left:18px;top:17px;margin:0!important;width:28px!important;height:28px!important}"
          "#unduhan,#publikasi{border-top:1px solid var(--line)}")
UND = sec("unduhan").replace('<p class="eyebrow" data-i18n="k272">Unduhan</p><h2 data-i18n="k273">Materi untuk Anda</h2>',
                             '<p class="eyebrow">Unduhan Gratis</p><h2>Materi Gratis</h2><p class="lede" style="margin-top:8px">Brosur, panduan, dan toolkit Excel. Isi nama dan email sekali, file langsung terunduh.</p>')
UND = UND.replace('<section class="block" id="unduhan">', '<section class="block alt" id="unduhan">', 1)
QRIS_BOX = ('<div class="qris-box" id="donasi"><img src="/img/qris-fa-indonesia.jpg" width="720" height="1014" loading="lazy" alt="QRIS FA Indonesia - Book &amp; Stationery">'
            '<div><p class="eyebrow">Donasi Sukarela</p><h3>Materi ini gratis. Kalau bermanfaat, dukung lewat QRIS.</h3>'
            '<p>Scan QRIS dengan aplikasi bank atau e-wallet apa saja. Nominal donasi Rp10.001, sepenuhnya opsional. Dana dipakai untuk menyusun materi dan toolkit berikutnya.</p>'
            '<a class="btn line" href="/img/qris-fa-indonesia.jpg" download="QRIS-FA-Indonesia.jpg">Simpan Gambar QRIS</a></div></div>')
k = UND.rfind('</div>\n</div>\n</section>')
UND = UND[:k] + '</div>\n' + QRIS_BOX + '\n</div>\n</section>'
QRIS_MODAL = ('<div id="qrisModal" role="dialog" aria-modal="true" aria-labelledby="qrisTtl" hidden>'
              '<div class="qm"><button type="button" class="qx" aria-label="Tutup">&times;</button>'
              '<p id="qrisTtl" class="qt">Terima kasih sudah mengunduh</p>'
              '<p class="qs">Materinya gratis. Kalau bermanfaat, Anda bisa berdonasi lewat QRIS, minimal Rp10.000. Sepenuhnya opsional.</p>'
              '<img src="/img/qris-fa-indonesia.jpg" width="720" height="1014" alt="QRIS FA Indonesia">'
              '<div class="qb"><a class="btn solid" href="/img/qris-fa-indonesia.jpg" download="QRIS-FA-Indonesia.jpg">Simpan QRIS</a><button type="button" class="btn line qx2">Nanti Saja</button></div></div></div>'
              '<script>(function(){var m=document.getElementById("qrisModal");if(!m)return;var shown=false;'
              'function open_(){if(shown)return;try{if(sessionStorage.getItem("fa-qris"))return;sessionStorage.setItem("fa-qris","1")}catch(e){}shown=true;m.hidden=false;if(window.gtag)gtag("event","qris_prompt")}'
              'function close_(){m.hidden=true}m.querySelector(".qx").onclick=close_;m.querySelector(".qx2").onclick=close_;m.addEventListener("click",function(e){if(e.target===m)close_()});'
              'document.addEventListener("click",function(e){var a=e.target.closest("#unduhan a.dl, #unduhan a[download], #unduhan .dl a");if(!a||a.closest(".qris-box"))return;'
              'var t=setInterval(function(){var lm=document.getElementById("leadModal");if(!lm||lm.style.display!=="flex"){clearInterval(t);setTimeout(open_,900)}},400)},true)})();</script>')
BK_CSS += (".qris-box{display:grid;grid-template-columns:200px 1fr;gap:28px;align-items:center;margin-top:36px;padding:22px;border:1px solid var(--line);border-radius:14px;background:var(--surface)}"
           ".qris-box img{width:100%;height:auto;border-radius:10px;background:#fff}.qris-box h3{font-family:var(--serif);font-weight:400;font-size:1.5rem;margin:4px 0 8px}.qris-box p{color:var(--muted);font-size:14px;margin:0 0 14px}"
           "@media (max-width:640px){.qris-box{grid-template-columns:1fr;text-align:left}.qris-box img{max-width:220px}}"
           "#qrisModal{position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.75);display:flex;align-items:center;justify-content:center;padding:16px}#qrisModal[hidden]{display:none}"
           "#qrisModal .qm{position:relative;background:#1b1b1b;border:1px solid #333;border-radius:14px;max-width:380px;width:100%;max-height:92vh;overflow:auto;padding:22px;text-align:center;font-family:Poppins,sans-serif;color:#fff}"
           "#qrisModal .qt{font:500 22px 'EB Garamond',serif;margin:0 0 6px}#qrisModal .qs{color:#a3a3a3;font-size:13px;margin:0 0 14px;line-height:1.6}"
           "#qrisModal img{width:100%;max-width:260px;height:auto;border-radius:10px;background:#fff}#qrisModal .qb{display:flex;gap:10px;justify-content:center;margin-top:14px;flex-wrap:wrap}"
           "#qrisModal .qx{position:absolute;right:10px;top:6px;background:none;border:0;color:#fff;font-size:26px;cursor:pointer}")
JUMP = ('<nav class="bk-jump" aria-label="Isi halaman"><a href="#paket">E-Book Berbayar</a><a href="#unduhan" class="on">Materi Gratis &#8595;</a><a href="#publikasi">Publikasi</a></nav>')
BK_CSS += (".bk-jump{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 6px}.bk-jump a{border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:13px;color:#fff;text-decoration:none}"
           ".bk-jump a.on{background:#fff;color:#171717;border-color:#fff;font-weight:500}.bk-jump a:hover{border-color:#fff}html{scroll-behavior:smooth}#unduhan,#publikasi,#paket{scroll-margin-top:80px}")
inject("buku/index.html", [sec("publikasi").replace('class="block alt"', 'class="block"', 1)], SH_TOAST + LEAD, BK_CSS,
       mid=[('<h2 style="margin-top:40px">Cara Membeli</h2>', '</div></section>' + UND + '<section class="block"><div class="wrap">')], jump=JUMP,
       subs=[('Cara membeli</h2>', 'Cara Membeli</h2>'), ('Pertanyaan umum</h2>', 'Pertanyaan Umum</h2>'), ('>Beli paket<', '>Beli Paket<'), ('Paket 6 E-book Penerbit FA</h2>', 'Paket 6 E-Book Penerbit FA</h2>')])
inject("artikel/index.html", [sec("galeri"), sec("kabar")], LIGHT + FEEDJS,
       subs=[('<p class="eyebrow">Wawasan</p>', '<p class="eyebrow">Eksplor</p>'),
             ('Wawasan: Artikel dan Berita Keuangan</h1>', 'Eksplor: Berita, Artikel, dan Galeri</h1>')])
ud = os.path.join(FA, "unduhan")
if os.path.isdir(ud): shutil.rmtree(ud)
rd = os.path.join(FA, "_redirects"); r = open(rd, encoding="utf-8").read()
if "/unduhan/" not in r:
    open(rd, "a", encoding="utf-8").write("\n/unduhan/*  /buku/#unduhan  301\n")

sm = os.path.join(FA, "sitemap.xml")
x = open(sm, encoding="utf-8").read()
x = x.replace("<url><loc>https://faindonesia.co.id/unduhan/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n", "")
for u in ["https://faindonesia.co.id/layanan/"]:
    if u not in x:
        x = x.replace("</urlset>", f"<url><loc>{u}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>")
open(sm, "w", encoding="utf-8").write(x)
print("ok")
