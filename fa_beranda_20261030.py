# -*- coding: utf-8 -*-
"""Beranda FA disederhanakan lagi (30 Okt 2026), jalankan SETELAH fa_rapi_20261027.py.
Urutan beranda: Hero -> Pilih Jalur (aset < Rp35 M ke CariAkuntan untuk penyiapan; >= Rp35 M ke Cek Kredit/Investor/IPO)
-> Cek Kredit -> Rekam Jejak (angka) -> Cara Mulai -> Kontak.
Dibuang dari beranda: peta, pendekatan, siapa, jelajahi (isinya sudah ada di tab Layanan/Eksplor).
Cek Kredit: kalau Total Aset < Rp35 miliar, hasil menampilkan arahan ke CariAkuntan (penyiapan dulu, bukan cari pendanaan).
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
#jalur .jl2{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:26px}
#jalur .jc{border:1px solid rgba(128,128,128,.35);padding:26px 26px 22px;display:flex;flex-direction:column;gap:12px;position:relative}
#jalur .jc .tg{font-size:12px;letter-spacing:.22em;text-transform:uppercase;opacity:.75}
#jalur .jc h3{font-family:inherit;font-size:clamp(1.25rem,2.4vw,1.6rem);line-height:1.25;margin:0;font-weight:500}
#jalur .jc ul{margin:2px 0 6px;padding:0;list-style:none;display:grid;gap:8px}
#jalur .jc li{display:flex;gap:10px;align-items:flex-start;font-size:15px;line-height:1.5;opacity:.9}
#jalur .jc li:before{content:"";flex:none;width:7px;height:7px;margin-top:8px;border-radius:50%;background:currentColor;opacity:.55}
#jalur .jc .ac{display:flex;flex-wrap:wrap;gap:10px;margin-top:auto}
#jalur .jc.hi{border-color:currentColor}
#jalur .jn{font-size:13px;opacity:.65;margin-top:16px;line-height:1.55}
@media(max-width:760px){#jalur .jl2{grid-template-columns:1fr}#jalur .jc{padding:22px 18px}}
.kk-jl{border:1px solid rgba(128,128,128,.45);padding:16px 18px;margin:0 0 18px;line-height:1.55}
.kk-jl b{display:block;font-size:16px;margin-bottom:4px}.kk-jl .ac{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
</style>"""
wa1 = WA + quote("Halo Pak Ananta, aset perusahaan kami di bawah Rp35 miliar. Kami ingin merapikan laporan keuangan dan dokumen dulu sebelum mengajukan kredit.")
wa2 = WA + quote("Halo Pak Ananta, aset perusahaan kami di atas Rp35 miliar. Kami ingin diskusi kredit bank, investor, atau IPO.")
JALUR = f"""<!--fa-jalur-->
<section class="block alt hs" id="jalur">
<div class="wrap">
<div class="head"><p class="eyebrow" data-i18n="jl1">Mulai dari Sini</p><h2 class="aph" data-i18n="jl2">Pilih jalur sesuai <em>total aset.</em></h2></div>
<div class="jl2">
<div class="jc">
<span class="tg" data-i18n="jl3">Aset di Bawah Rp35 Miliar</span>
<h3 data-i18n="jl4">Rapikan Dulu, Siap Diajukan Nanti</h3>
<ul><li data-i18n="jl5">Laporan keuangan, audit KAP, dan pajak dibereskan lebih dulu</li><li data-i18n="jl6">KAP, KJA, dan konsultan pajak berizin lewat CariAkuntan</li><li data-i18n="jl7">Tim FA tetap membantu penyiapan berkas dan rasio</li></ul>
<div class="ac"><a class="btn red" data-i18n="jl8" href="https://cariakuntan.com/screening/" target="_blank" rel="noopener">Mulai di CariAkuntan</a><a class="btn line" data-i18n="jl9" href="{wa1}" target="_blank" rel="noopener">Tanya Penyiapan</a></div>
</div>
<div class="jc hi">
<span class="tg" data-i18n="jl10">Aset Rp35 Miliar ke Atas</span>
<h3 data-i18n="jl11">Kredit Bank, Investor, atau IPO</h3>
<ul><li data-i18n="jl12">Hitung plafon dan kemampuan bayar dalam 3 menit</li><li data-i18n="jl13">Pendampingan due diligence sampai dana cair</li><li data-i18n="jl14">Pencarian investor, M&amp;A, dan persiapan IPO</li></ul>
<div class="ac"><a class="btn red" data-i18n="jl15" href="#cek-kredit">Cek Kredit Gratis</a><a class="btn line" data-i18n="jl16" href="{wa2}" target="_blank" rel="noopener">Chat Ananta, CPA</a></div>
</div>
</div>
<p class="jn" data-i18n="jl17">Rp35 miliar adalah gambaran umum agunan minimum segmen kredit komersial bank. Kebijakan tiap bank berbeda.</p>
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
var a=ta==null?null:ta*u;if(a==null||a>=35000){if(ex)ex.remove();return}if(ex)return;
var d=document.createElement('div');d.className='kk-jl';d.id='kk_jl';
d.innerHTML='<b>Total aset di bawah Rp35 miliar: fokus penyiapan dulu.</b>Segmen kredit komersial bank umumnya meminta agunan sekitar Rp35 miliar ke atas. Langkah paling cepat saat ini adalah merapikan laporan keuangan, audit, dan pajak. Tim FA tetap bisa membantu penyiapannya.<div class="ac"><a class="btn red" href="https://cariakuntan.com/screening/" target="_blank" rel="noopener">Mulai di CariAkuntan</a><a class="btn line" href="https://wa.me/6282245260121?text='+encodeURIComponent('Halo Pak Ananta, total aset kami di bawah Rp35 miliar. Kami ingin bantuan penyiapan laporan keuangan dan berkas kredit.')+'" target="_blank" rel="noopener">Tanya Penyiapan</a></div>';
o.insertBefore(d,o.firstChild)}
new MutationObserver(run).observe(o,{attributes:true,attributeFilter:['style'],childList:true});document.addEventListener('input',function(e){if(e.target&&(e.target.id==='kk_ta'||e.target.id==='kk_unit'))setTimeout(run,50)});})();</script><!--/fa-jalur-js-->"""
s = re.sub(r"<!--fa-jalur-js-->.*?<!--/fa-jalur-js-->", "", s, flags=re.S)
s = s.replace("</body>", JS + "</body>", 1)

# 5. terjemahan EN/ZH
EN = {"jl0": "For companies of every size: tidy financial statements first, then bank credit, investors, and IPO.", "jl1": "Start Here", "jl2": "Choose your route by <em>total assets.</em>",
      "jl3": "Assets Below Rp35 Billion", "jl4": "Get Ready First, Apply Later", "jl5": "Sort out financial statements, KAP audit, and tax first", "jl6": "Licensed KAP, KJA, and tax consultants via CariAkuntan",
      "jl7": "The FA team still helps prepare files and ratios", "jl8": "Start at CariAkuntan", "jl9": "Ask About Preparation", "jl10": "Assets Rp35 Billion and Above", "jl11": "Bank Credit, Investors, or IPO",
      "jl12": "Estimate credit limit and repayment capacity in 3 minutes", "jl13": "Due diligence support until funds are disbursed", "jl14": "Investor search, M&amp;A, and IPO preparation",
      "jl15": "Free Credit Check", "jl16": "Chat Ananta, CPA", "jl17": "Rp35 billion is a general picture of minimum collateral in banks' commercial lending segment. Each bank's policy differs."}
ZH = {"jl0": "适用于各种规模的企业：先整理财务报表，再对接银行贷款、投资者与上市。", "jl1": "从这里开始", "jl2": "按 <em>总资产</em> 选择路径。", "jl3": "资产低于 350 亿印尼盾", "jl4": "先做准备，再申请",
      "jl5": "先完成财务报表、审计与税务", "jl6": "通过 CariAkuntan 找持牌会计师事务所与税务顾问", "jl7": "FA 团队仍协助准备文件与比率", "jl8": "前往 CariAkuntan", "jl9": "咨询准备工作",
      "jl10": "资产 350 亿印尼盾及以上", "jl11": "银行贷款、投资者或上市", "jl12": "3 分钟估算贷款额度与还款能力", "jl13": "尽职调查陪同直至放款", "jl14": "寻找投资者、并购与上市准备",
      "jl15": "免费贷款检测", "jl16": "联系 Ananta, CPA", "jl17": "350 亿印尼盾是银行商业贷款板块最低抵押的一般参考，各银行政策不同。"}
import json
for lang, D in (("en", EN), ("zh", ZH)):
    tag = '"%s": {' % lang
    if tag in s:
        i = s.find(tag) + len(tag)
        body = "".join('%s: %s, ' % (json.dumps(k), json.dumps(v, ensure_ascii=False)) for k, v in D.items() if '"%s":' % k not in s[i:i + 400000])
        s = s[:i] + body + s[i:]
open(P, "w", encoding="utf-8").write(s)
print("beranda FA: jalur ok,", s.count("<section"), "section")
