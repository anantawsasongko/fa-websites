# -*- coding: utf-8 -*-
"""Beranda FA disederhanakan lagi (30 Okt 2026), jalankan SETELAH fa_rapi_20261027.py.
Urutan beranda: Hero -> Pilih Jalur (aset < Rp25 M ke CariAkuntan (rapikan LK); >= Rp25 M kredit komersial bank; aset bersih > Rp50 M investor institusi/IPO)
-> Cek Kredit -> Rekam Jejak (angka) -> Cara Mulai -> Kontak.
Dibuang dari beranda: peta, pendekatan, siapa, jelajahi (isinya sudah ada di tab Layanan/Eksplor).
Cek Kredit: kalau Total Aset < Rp25 miliar, hasil menampilkan arahan ke CariAkuntan (penyiapan dulu, bukan cari pendanaan).
Idempoten (penanda fa-jalur / fa-jalur-js)."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58", "index.html")
s = open(P, encoding="utf-8").read()
WA = "https://wa.me/6282245260121?text="
from urllib.parse import quote

# 1. buang section yang membuat ruwet
for sid in ("peta", "pendekatan", "siapa", "jelajahi"):
    s = re.sub(r'<section[^>]*\bid="%s"[^>]*>.*?</section>\s*' % sid, "", s, flags=re.S)

# 2. teks hero dan fakta: semua skala, bahasa tim
s = re.sub(r'<p class="lede" data-i18n="k9">.*?</p>',
           '<p class="lede" data-i18n="jl0">Untuk semua skala perusahaan: merapikan laporan keuangan, lalu kredit bank, investor, sampai IPO.</p>', s, flags=re.S)
s = re.sub(r'<span data-i18n="k16">[^<]*</span>', '<span data-i18n="k16">Klien Pendanaan Baru per Tahun, Agar Fokus</span>', s)
s = s.replace('Empat langkah, <em>satu orang.</em>', 'Empat langkah, <em>sampai dana cair.</em>')

# 3. section Pilih Jalur
CSS = """<style id="fa-jalur-css">
#jalur .jl2{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px}
#jalur .jc{border:1px solid rgba(128,128,128,.35);padding:26px 26px 22px;display:flex;flex-direction:column;gap:12px;position:relative}
#jalur .jc .tg{font-size:12px;letter-spacing:.22em;text-transform:uppercase;opacity:.75}
#jalur .jc h3{font-family:inherit;font-size:clamp(1.25rem,2.4vw,1.6rem);line-height:1.25;margin:0;font-weight:500}
#jalur .jc ul{margin:2px 0 6px;padding:0;list-style:none;display:grid;gap:8px}
#jalur .jc li{display:flex;gap:10px;align-items:flex-start;font-size:15px;line-height:1.5;opacity:.9}
#jalur .jc li:before{content:"";flex:none;width:7px;height:7px;margin-top:8px;border-radius:50%;background:currentColor;opacity:.55}
#jalur .jc .ac{display:grid;grid-template-columns:1fr;gap:10px;margin-top:auto}#jalur .jc .ac .btn{text-align:center;justify-content:center}
#jalur .jc.hi{border-color:currentColor}
#jalur .jn{font-size:13px;opacity:.65;margin-top:16px;line-height:1.55}
@media(max-width:980px){#jalur .jl2{grid-template-columns:1fr}#jalur .jc{padding:22px 18px}}
.kk-jl{border:1px solid rgba(128,128,128,.45);padding:16px 18px;margin:0 0 18px;line-height:1.55}
.kk-jl b{display:block;font-size:16px;margin-bottom:4px}.kk-jl .ac{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
</style>"""
wa1 = WA + quote("Halo Pak Ananta, aset perusahaan kami di bawah Rp25 miliar. Kami ingin merapikan laporan keuangan dan dokumen dulu.")
wa2 = WA + quote("Halo Pak Ananta, aset perusahaan kami di atas Rp25 miliar. Kami ingin diskusi pengajuan kredit bank.")
wa3 = WA + quote("Halo Pak Ananta, aset bersih perusahaan kami di atas Rp50 miliar. Kami ingin diskusi investor institusi atau IPO.")
def card(cls, tg, ktg, h, kh, items, b1, b2):
    li = "".join(f'<li data-i18n="{k}">{t}</li>' for k, t in items)
    return (f'<div class="jc{cls}"><span class="tg" data-i18n="{ktg}">{tg}</span><h3 data-i18n="{kh}">{h}</h3><ul>{li}</ul>'
            f'<div class="ac"><a class="btn red" data-i18n="{b1[0]}" href="{b1[2]}"{b1[3]}>{b1[1]}</a><a class="btn line" data-i18n="{b2[0]}" href="{b2[2]}" target="_blank" rel="noopener">{b2[1]}</a></div></div>')
NB = ' target="_blank" rel="noopener"'
JALUR = f"""<!--fa-jalur-->
<section class="block alt hs" id="jalur">
<div class="wrap">
<div class="head"><p class="eyebrow" data-i18n="jl1">Mulai dari Sini</p><h2 class="aph" data-i18n="jl2">Pilih jalur sesuai <em>skala perusahaan.</em></h2></div>
<div class="jl2">
{card("", "Aset di Bawah Rp25 Miliar", "jl3", "Rapikan Laporan Keuangan Dulu", "jl4", [("jl5", "Laporan Keuangan, Audit KAP, dan Pajak Dibereskan Lebih Dulu"), ("jl6", "KAP, KJA, dan Konsultan Pajak Berizin Lewat CariAkuntan"), ("jl7", "Tim FA Membantu Penyiapan sampai Siap Diajukan")], ("jl8", "Mulai di CariAkuntan", "https://cariakuntan.com/screening/", NB), ("jl9", "Tanya Penyiapan", wa1))}
{card(" hi", "Aset Rp25 Miliar ke Atas", "jl10", "Kredit Komersial Bank", "jl11", [("jl12", "Hitung Plafon dan Kemampuan Bayar dalam 3 Menit"), ("jl13", "Berkas Kredit Disiapkan Sesuai Cara Analis Bank Membaca"), ("jl14", "Pendampingan Due Diligence sampai Dana Cair")], ("jl15", "Cek Kredit Gratis", "#cek-kredit", ""), ("jl16", "Chat Ananta, CPA", wa2))}
{card("", "Aset Bersih di Atas Rp50 Miliar", "jl18", "Investor Institusi dan IPO", "jl19", [("jl20", "Aset Bersih di Atas Rp50 Miliar, Berturut-turut"), ("jl21", "Private Equity, Family Office, dan Pembeli Strategis"), ("jl22", "Persiapan IPO Bursa Efek Indonesia")], ("jl23", "Untuk Investor", "/mitra-investor/", ""), ("jl24", "Diskusi IPO", wa3))}
</div>
<p class="jn" data-i18n="jl17">Batas di atas adalah gambaran umum: Rp25 miliar untuk pengajuan ke segmen kredit komersial bank, aset bersih Rp50 miliar untuk investor institusi dan IPO. Kebijakan tiap bank dan investor berbeda.</p>
</div>
</section>
<!--/fa-jalur-->
"""
s = re.sub(r"<!--fa-jalur-->.*?<!--/fa-jalur-->\s*", "", s, flags=re.S)
s = re.sub(r'<style id="fa-jalur-css">.*?</style>', "", s, flags=re.S)
s = s.replace("</head>", CSS + "</head>", 1)
k = s.find("<!--fa-kk-home-->")
if k < 0: k = s.find('<section class="block" id="cek-kredit">')
s = s[:k] + JALUR + s[k:]

# 4. Cek Kredit: arahan aset < Rp35 M
JS = """<!--fa-jalur-js--><script>(function(){var o=document.getElementById('kk_out');if(!o)return;
function num(id){var e=document.getElementById(id);if(!e)return null;var v=(e.value||'').trim();if(!v)return null;v=v.replace(/\\./g,'').replace(',','.').replace(/[^0-9.\\-]/g,'');var n=parseFloat(v);return isNaN(n)?null:n}
function run(){if(o.style.display==='none')return;var ex=document.getElementById('kk_jl');var ta=num('kk_ta'),u=+((document.getElementById('kk_unit')||{}).value||1);
var a=ta==null?null:ta*u;if(a==null||a>=25000){if(ex)ex.remove();return}if(ex)return;
var d=document.createElement('div');d.className='kk-jl';d.id='kk_jl';
d.innerHTML='<b>Total aset di bawah Rp25 miliar: rapikan laporan keuangan dulu.</b>Pengajuan ke segmen kredit komersial bank umumnya dimulai dari aset sekitar Rp25 miliar. Langkah paling cepat saat ini adalah merapikan laporan keuangan, audit, dan pajak. Tim FA tetap bisa membantu penyiapannya.<div class="ac"><a class="btn red" href="https://cariakuntan.com/screening/" target="_blank" rel="noopener">Mulai di CariAkuntan</a><a class="btn line" href="https://wa.me/6282245260121?text='+encodeURIComponent('Halo Pak Ananta, total aset kami di bawah Rp25 miliar. Kami ingin bantuan penyiapan laporan keuangan dan berkas kredit.')+'" target="_blank" rel="noopener">Tanya Penyiapan</a></div>';
o.insertBefore(d,o.firstChild)}
new MutationObserver(run).observe(o,{attributes:true,attributeFilter:['style'],childList:true});document.addEventListener('input',function(e){if(e.target&&(e.target.id==='kk_ta'||e.target.id==='kk_unit'))setTimeout(run,50)});})();</script><!--/fa-jalur-js-->"""
s = re.sub(r"<!--fa-jalur-js-->.*?<!--/fa-jalur-js-->", "", s, flags=re.S)
s = s.replace("</body>", JS + "</body>", 1)

# 5. terjemahan EN/ZH
EN = {"jl0": "For companies of every size: tidy financial statements first, then bank credit, investors, and IPO.", "jl1": "Start Here", "jl2": "Choose your route by <em>company size.</em>",
      "jl3": "Assets Below Rp25 Billion", "jl4": "Tidy Financial Statements First", "jl5": "Sort out financial statements, KAP audit, and tax first", "jl6": "Licensed KAP, KJA, and tax consultants via CariAkuntan",
      "jl7": "The FA team helps prepare until ready to apply", "jl8": "Start at CariAkuntan", "jl9": "Ask About Preparation", "jl10": "Assets Rp25 Billion and Above", "jl11": "Commercial Bank Credit",
      "jl12": "Estimate credit limit and repayment capacity in 3 minutes", "jl13": "Credit files prepared the way bank analysts read them", "jl14": "Due diligence support until funds are disbursed",
      "jl15": "Free Credit Check", "jl16": "Chat Ananta, CPA", "jl18": "Net Assets Above Rp50 Billion", "jl19": "Institutional Investors and IPO", "jl20": "Net assets above Rp50 billion, consecutively",
      "jl21": "Private equity, family offices, and strategic buyers", "jl22": "Indonesia Stock Exchange IPO preparation", "jl23": "For Investors", "jl24": "Discuss IPO",
      "jl17": "These are general guides: Rp25 billion for banks' commercial lending segment, Rp50 billion net assets for institutional investors and IPO. Each bank's and investor's policy differs."}
ZH = {"jl0": "适用于各种规模的企业：先整理财务报表，再对接银行贷款、投资者与上市。", "jl1": "从这里开始", "jl2": "按 <em>企业规模</em> 选择路径。", "jl3": "资产低于 250 亿印尼盾", "jl4": "先整理财务报表",
      "jl5": "先完成财务报表、审计与税务", "jl6": "通过 CariAkuntan 找持牌会计师事务所与税务顾问", "jl7": "FA 团队协助准备直至可以申请", "jl8": "前往 CariAkuntan", "jl9": "咨询准备工作",
      "jl10": "资产 250 亿印尼盾及以上", "jl11": "银行商业贷款", "jl12": "3 分钟估算贷款额度与还款能力", "jl13": "按银行分析师的视角准备贷款文件", "jl14": "尽职调查陪同直至放款",
      "jl15": "免费贷款检测", "jl16": "联系 Ananta, CPA", "jl18": "净资产超过 500 亿印尼盾", "jl19": "机构投资者与上市", "jl20": "净资产连续超过 500 亿印尼盾", "jl21": "私募股权、家族办公室与战略买家",
      "jl22": "印尼证券交易所上市准备", "jl23": "投资者入口", "jl24": "讨论上市", "jl17": "以上为一般参考：250 亿印尼盾对应银行商业贷款板块，500 亿印尼盾净资产对应机构投资者与上市。各银行与投资者政策不同。"}
import json
for lang, D in (("en", EN), ("zh", ZH)):
    tag = '"%s": {' % lang
    if tag in s:
        i = s.find(tag) + len(tag)
        body = "".join('%s: %s, ' % (json.dumps(k), json.dumps(v, ensure_ascii=False)) for k, v in D.items())
        s = s[:i] + body + s[i:]
open(P, "w", encoding="utf-8").write(s)
print("beranda FA: jalur ok,", s.count("<section"), "section")
