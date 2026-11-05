# -*- coding: utf-8 -*-
"""5 Nov 2026 (aturan Bos): di semua FA Apps tidak ada kata "bayar" dan tidak ada harga yang diumumkan di muka.
Semua aplikasi dan hasil ringkasnya gratis, ajak orang mencoba. Yang gratis bilang gratis + QRIS donasi.
Pembayaran (Mayar atau QRIS) hanya muncul saat pengguna mau mengunduh laporan hasil lengkap.
Script ini membersihkan teks sumber (Jupiter, Galaxy, /apps/, /toko/, kalkulator Venus). Idempoten.
Jalankan sebelum prep.py (setelah fa_venus_unggulan_20261104.py)."""
import os, re, json
M = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(M, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
JUP = os.path.join(M, "FA-Jupiter_SIAP-UPLOAD-v6", "audit-ready", "index.html")
MAYAR_DAY = "https://fa-indonesia-14404.myr.id/pl/fa-jupiter-audit-ready-day-pass-1-hari"
MAYAR_YEAR = "https://fa-indonesia-14404.myr.id/pl/fa-jupiter-audit-ready-tahunan-1-tahun"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t): open(p, "w", encoding="utf-8").write(t)
def rep(t, pairs, label):
    n = 0
    for a, b in pairs:
        if a in t: t = t.replace(a, b); n += 1
    print(f"  {label}: {n}/{len(pairs)} pola diganti")
    return t

# ---------- FA Jupiter ----------
t = rd(JUP)
t = rep(t, [
    ('["pay","Bayar akses","Day pass Rp39.000 atau tahunan Rp249.000.",`<a class="btn small" href="/bayar/?produk=ar-year">Bayar</a>`]',
     '["pay","Unduh hasil lengkap","Excel, Word CALK, dan file proyek. Pilih akses saat klik Download.",`<button class="btn small" data-tab="lk">Lihat Laporan</button>`]'),
    ('<p>Coba dulu dengan data contoh. Bayar kalau sudah yakin.</p>', '<p>Coba dulu dengan data contoh. Semua hasil tampil gratis, tanpa daftar.</p>'),
    ('<th>Fitur</th><th>Gratis</th><th>Berbayar</th>', '<th>Fitur</th><th>Gratis</th><th>Akses Penuh</th>'),
    ('<button class="btn small primary" data-tab="mulai">Harga &amp; aktivasi</button>', '<button class="btn small primary" data-tab="mulai">Aktivasi</button>'),
    ('Penyimpanan otomatis, file proyek, dan Download Excel tersedia dengan akses berbayar.', 'Penyimpanan otomatis, file proyek, dan Download Excel terbuka dengan kode akses.'),
    ('gate("Download Word CALK tersedia setelah akses diaktifkan.")', 'gate("Tempel kode akses untuk membuka Download Word CALK.")'),
    ('gate("Download Excel tersedia setelah akses diaktifkan.")', 'gate("Tempel kode akses untuk membuka Download Excel.")'),
    ('gate("Simpan file proyek tersedia setelah akses diaktifkan.")', 'gate("Tempel kode akses untuk membuka file proyek.")'),
], "jupiter teks")
# kotak aktivasi: tanpa harga; pilihan akses lewat tombol Download (paywall v4)
t = re.sub(r'<p class="note">Beli kode akses: <a href="[^"]*day-pass[^"]*"[^>]*>[^<]*</a> atau <a href="[^"]*tahunan[^"]*"[^>]*>[^<]*</a> \(termasuk PPN\)\. Kode tampil otomatis setelah pembayaran\. Semua fitur tetap bisa dicoba gratis\.</p>',
           '<p class="note">Belum punya kode? Klik <b>Download Excel</b> atau <b>Download Word CALK</b>, pilih masa akses, kode tampil otomatis setelah selesai. Semua fitur tetap bisa dicoba gratis.</p>', t)
assert "Rp39.000" not in t and "Rp249.000" not in t, "harga Jupiter masih ada"
wr(JUP, t)

# ---------- Galaxy ----------
p = os.path.join(FA, "galaxy", "index.html"); t = rd(p)
t = rep(t, [
    ('<h3 data-i18n="j7">Gratis dan Berbayar</h3>', '<h3 data-i18n="j7">Gratis dan Akses Penuh</h3>'),
    ('<li data-i18n="jr2"><b>Akses berbayar:</b> simpan otomatis, file proyek untuk dibuka lagi, dan download Excel. Data tetap di laptop Anda.</li>',
     '<li data-i18n="jr2"><b>Akses penuh:</b> simpan otomatis, file proyek untuk dibuka lagi, dan download Excel serta Word CALK. Pilihan akses muncul saat klik Download. Data tetap di laptop Anda.</li>'),
    ('"j7": "Free and Paid"', '"j7": "Free and Full Access"'),
    ('"jr2": "<b>Paid access:</b> autosave, project files you can reopen, and Excel download. Your data stays on your laptop."',
     '"jr2": "<b>Full access:</b> autosave, project files you can reopen, and Excel and Word downloads. Access options appear when you click Download. Your data stays on your laptop."'),
    ('"j7": "免费与付费"', '"j7": "免费与完整版"'),
    ('"jr2": "<b>付费开通：</b>自动保存、可再次打开的项目文件，以及 Excel 下载。数据仍保存在您的电脑上。"',
     '"jr2": "<b>完整版：</b>自动保存、可再次打开的项目文件，以及 Excel 和 Word 下载。点击下载时会显示访问选项。数据仍保存在您的电脑上。"'),
], "galaxy")
wr(p, t)

# ---------- /apps/ ----------
p = os.path.join(FA, "apps", "index.html"); t = rd(p)
n = len(re.findall(r'<span class="cat">Rp\d+ rb</span>', t))
t = re.sub(r'<span class="cat">Rp\d+ rb</span>', '<span class="cat">Coba Gratis</span>', t)
t = rep(t, [
    ('<p class="lead">Bayar sekali per aplikasi lewat QRIS, akses tersimpan di perangkat Anda. Kalkulator memberi angka cepat.',
     '<p class="lead">Semua aplikasi gratis dicoba, hasil ringkas langsung tampil di layar. Kalkulator memberi angka cepat.'),
    ('<div class="meta vu-k"><b>Rp49 rb</b><span>bayar QRIS di aplikasi</span>', '<div class="meta vu-k"><b>Gratis</b><span>coba langsung, laporan lengkap via WhatsApp</span>'),
], "apps")
print(f"  apps: {n} badge harga -> Coba Gratis")
wr(p, t)

# ---------- /toko/ (halaman jualan: harga produk tetap, tapi tanpa kata bayar di kartu aplikasi) ----------
p = os.path.join(FA, "toko", "index.html")
if os.path.exists(p):
    t = rd(p)
    t = rep(t, [("termasuk PPN · bayar QRIS di aplikasi", "termasuk PPN · unduh laporan lengkap di aplikasi"), ("Termasuk PPN · Bayar QRIS di Aplikasi", "Termasuk PPN · Unduh laporan lengkap di aplikasi")], "toko")
    wr(p, t)

# ---------- kalkulator FA Venus: 6 kalkulator gratis (hapus FA_PAY), DCF dapat tombol unduh laporan ----------
FREE = ["kalkulator-pph-21", "kalkulator-pph-badan", "kalkulator-potput-ppn", "kalkulator-penyusutan-fiskal", "kalkulator-cicilan-pinjaman", "kalkulator-rasio-keuangan"]
for s in FREE:
    p = os.path.join(FA, s, "index.html"); t = rd(p)
    t2 = re.sub(r'<script>window\.FA_PAY=\{[^<]*\}\s*;?\s*</script>\s*<script src="/js/fa-paywall\.js"[^>]*></script>', "", t)
    if t2 != t: wr(p, t2); print(f"  {s}: FA_PAY dihapus (gratis)")
p = os.path.join(FA, "kalkulator-valuasi-dcf", "index.html"); t = rd(p)
t = re.sub(r'<script>window\.FA_PAY=\{[^<]*\}\s*;?\s*</script>\s*<script src="/js/fa-paywall\.js"[^>]*></script>', "", t)
if 'id="dcf_pdf"' not in t and 'id="dcf_wa"' not in t:
    t = t.replace('<p class="note">Baris = WACC, kolom = pertumbuhan terminal.',
                  '<p style="margin:14px 0 0"><button class="btn primary" id="dcf_pdf" type="button" data-fa-full="">Unduh Laporan Lengkap (PDF)</button></p>\n  <p class="note">Baris = WACC, kolom = pertumbuhan terminal.', 1)
    t = t.replace("calc();\n\n})();", 'calc();\n$("#dcf_pdf").addEventListener("click",()=>{calc();window.print()});\n\n})();', 1)
    t = t.replace("</style>", "@media print{header,nav,footer,.toast,#fapw,#faDon,#faDonPill,#faai-b,#faai,.fa-share,#dcf_pdf{display:none!important}body{background:#fff;color:#000}.sec{break-inside:avoid}}\n</style>", 1) if "@media print{header,nav,footer" not in t else t
    print("  dcf: tombol Unduh Laporan Lengkap (PDF) ditambah")
wr(p, t)
print("fa_harga_20261105 selesai")

# ================= 5 Nov 2026 siang (permintaan Bos): laporan lengkap lewat WhatsApp, bukan unduh/QRIS =================
# Valuasi RS dan DCF: tombol "Minta Laporan Lengkap via WhatsApp" (lead.js: form + Sheet + email, lalu chat WA berisi semua data
# dan link prefill). Bos buka link prefill (?laporan=1) untuk cetak PDF dan mengirimkannya lewat WA. Rumus RS dirapikan:
# ekuitas tidak pernah negatif (utang melebihi nilai = Rp0 + catatan), multiple before 4,5-6x, after 6-7,5x (+0,5 proses kompetitif, maks 8x).
RS = os.path.join(FA, "kalkulator-valuasi-rumah-sakit", "index.html"); t = rd(RS)
if "RSV2" not in t:
    s = t.index("<script>\n(function(){\nvar WA=\"6282245260121\""); e = t.index("</script>", s)
    old = t[s:e]
    new = old
    # tombol: a href WA (lead.js menangani form + Sheet + email)
    t = t.replace('<button class="btn line" type="button" id="rv_pdf" data-fa-full>Unduh Laporan Lengkap dan Strategi</button>',
                  '<a class="btn line" id="rv_pdf" href="https://wa.me/6282245260121" rel="noopener" target="_blank">Minta Laporan Lengkap dan Strategi via WhatsApp</a>')
    t = t.replace('<p class="rv-sm">Estimasi indikatif. Kolom After',
                  '<p class="rv-sm">Laporan lengkap (PDF) berisi rincian perhitungan, temuan, dan strategi treatment, dikirim tim FA Indonesia lewat WhatsApp. Estimasi indikatif. Kolom After')
    new = new.replace('var LAST=null;', '/*RSV2*/var LAST=null;\nfunction eqc(ev,u){return Math.max(0,ev-u)}')
    new = new.replace('var bL=Math.max(pL,iL||0)-utang,bH=Math.max(pH,iH||0)-utang;',
                      'var evbL=Math.max(pL,iL||0),evbH=Math.max(pH,iH||0),bL=eqc(evbL,utang),bH=eqc(evbH,utang);')
    new = new.replace('if(eb!==null&&eb>0){iL=eb*4*adjN;iH=eb*6*adjN}', 'if(eb!==null&&eb>0){iL=eb*4.5*adjN;iH=eb*6*adjN}')
    new = new.replace('var mL=4.5+(tA?0.5:0)+(tP?0.5:0),mH=6.5+(tA?0.5:0)+(tP?1:0),aiL=null,aiH=null;',
                      'var mL=Math.min(8,6+(tP?0.5:0)),mH=Math.min(8,7.5+(tP?0.5:0)),aiL=null,aiH=null;')
    new = new.replace('var aL=Math.max(gL,aiL||0)-utang,aH=Math.max(gH,aiH||0)-utang;',
                      'var evaL=Math.max(gL,aiL||0),evaH=Math.max(gH,aiH||0),aL=eqc(evaL,utang),aH=eqc(evaH,utang);')
    new = new.replace('$("rv_up").textContent=up>0.05?"+"+fmt(up):"Rp0";',
                      '$("rv_up").textContent=up>0.05?"+"+fmt(up):"Rp0";var gapB=utang-evbH,gapA=utang-evaH;')
    new = new.replace('$("rv_upx").textContent=(up>0.05&&bm>0.1)?"Sekitar "+(am/bm).toFixed(1).replace(".",",")+" kali harga before (nilai tengah)":(bm<=0.1&&up>0.05?"Before belum menutup utang bank":"Pilih treatment untuk melihat selisih");',
                      '$("rv_upx").textContent=(up>0.05&&bm>0.1)?"Sekitar "+(am/bm).toFixed(1).replace(".",",")+" kali harga before (nilai tengah)":(bm<=0.1&&up>0.05?"Before: utang bank melebihi nilai RS sekitar "+fmt(gapB)+", pemilik tidak menerima apa pun":(am<=0.1?"Utang bank melebihi nilai RS bahkan setelah treatment (kurang "+fmt(gapA)+"); perlu restrukturisasi utang":"Pilih treatment untuk melihat selisih"));')
    new = new.replace('$("rv_dbt").textContent=utang?"- "+fmt(utang):"Rp0";',
                      '$("rv_dbt").textContent=utang?"- "+fmt(utang)+(gapB>0?" (melebihi nilai before)":""):"Rp0";')
    new = new.replace('if(bL<0)f.push(["dn","Harga before belum menutup utang bank: tanpa treatment, penjualan berisiko tidak menghasilkan apa pun bagi pemilik."]);',
                      'if(gapB>0)f.push(["dn","Utang bank "+fmt(utang)+" melebihi nilai RS saat ini ("+rng(evbL,evbH)+"): dijual apa adanya, pemilik tidak menerima apa pun. Treatment plus restrukturisasi utang menentukan hasilnya."]);')
    # pesan WA untuk laporan lengkap + link prefill
    new = new.replace('$("rv_wa").href="https://wa.me/"+WA+"?text="+encodeURIComponent(msg);',
                      '$("rv_wa").href="https://wa.me/"+WA+"?text="+encodeURIComponent(msg);\n'
                      ' var qp=["jenis","kelas","tt","bor","akr","bpjs","rev","ebitda","aud","lahan","umur","apr","utang","porsi"].map(function(i){return i+"="+encodeURIComponent($(i).value)}).join("&")+["t_bpjs","t_mrg","t_bor","t_aud","t_prs"].map(function(i){return "&"+i+"="+(ck(i)?1:0)}).join("");\n'
                      ' var rep="Halo, saya ingin minta Laporan Lengkap dan Strategi Penjualan RS (PDF) dari kalkulator FA.\\n\\n"+msg.replace("Halo, saya ingin konsultasi penjualan rumah sakit.\\n\\n","")+"\\n\\nLink data: https://faindonesia.co.id/kalkulator-valuasi-rumah-sakit/?"+qp+"&laporan=1";\n'
                      ' $("rv_pdf").href="https://wa.me/"+WA+"?text="+encodeURIComponent(rep);')
    new = new.replace('$("rv_pdf").addEventListener("click",function(){calc();report(LAST);try{if(window.gtag)gtag("event","rsval_pdf",{jenis:$("jenis").value})}catch(e){}setTimeout(function(){window.print()},80)});',
                      '$("rv_pdf").addEventListener("click",function(){calc();try{if(window.gtag)gtag("event","rsval_pdf",{jenis:$("jenis").value})}catch(e){}},true);\n'
                      '(function(){var q=new URLSearchParams(location.search);if(!q.has("laporan")&&!q.has("tt"))return;q.forEach(function(v,k){var el=$(k);if(!el)return;if(el.type==="checkbox")el.checked=v==="1";else el.value=v});calc();if(q.get("laporan")==="1"){report(LAST);setTimeout(function(){window.print()},400)}})();')
    assert new.count("RSV2") == 1 and "eqc(evbL" in new and "laporan=1" in new and 'rv_pdf").href' in new, "patch RS gagal"
    t = t.replace(old, new)
    t = t.replace('"offers": {"@type": "Offer", "price": "49000", "priceCurrency": "IDR", "description": "Kalkulator gratis; laporan lengkap dan strategi berbayar"}',
                  '"offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR", "description": "Kalkulator gratis; laporan lengkap dan strategi dikirim lewat WhatsApp"}')
    t = t.replace("@media print{body>*:not(#rv_rep){disp", "@media print{#fapw,#faDon,#faDonPill,#faai-b,#faai{display:none!important}body>*:not(#rv_rep){disp", 1)
    wr(RS, t); print("  valuasi RS: rumus v2 + laporan via WA + prefill ?laporan=1")

# DCF: tombol WA (lead) + prefill + cetak oleh Bos
p = os.path.join(FA, "kalkulator-valuasi-dcf", "index.html"); t = rd(p)
if 'id="dcf_wa"' not in t:
    t = re.sub(r'<p style="margin:14px 0 0"><button class="btn primary" id="dcf_pdf"[^>]*>[^<]*</button></p>\n  ', '', t)
    t = t.replace('<p class="note">Baris = WACC, kolom = pertumbuhan terminal.',
                  '<p style="margin:14px 0 0"><a class="btn primary" id="dcf_wa" href="https://wa.me/6282245260121" rel="noopener" target="_blank">Minta Laporan Valuasi Lengkap via WhatsApp</a></p>\n  <p class="note">Laporan lengkap (PDF: asumsi, WACC, proyeksi, sensitivitas, dan catatan tim FA) dikirim lewat WhatsApp. Baris = WACC, kolom = pertumbuhan terminal.', 1)
    t = t.replace('$("#dcf_pdf").addEventListener("click",()=>{calc();window.print()});\n', '')
    t = t.replace("calc();\n\n})();",
                  'const DIDS=["fcf","g1","g2","gt","rf","beta","erp","sp","kd","tx","dw","debt","cash","dlom","sh"];\n'
                  'function waRep(){const W=wacc(),v=value(W.w,pv("gt"));const qp=DIDS.map(i=>i+"="+encodeURIComponent($("#"+i).value)).join("&");\n'
                  ' const m="Halo, saya ingin minta Laporan Valuasi DCF lengkap (PDF) dari kalkulator FA.\\n\\nFCFF: "+rp(val("fcf"))+" | g 1-3 thn: "+$("#g1").value+"% | g 4-5 thn: "+$("#g2").value+"% | g terminal: "+$("#gt").value+"%\\nWACC: "+pct(W.w)+" (Ke "+pct(W.ke)+", Kd "+pct(W.kd)+")\\nEnterprise value: "+rp(v.ev)+"\\nNilai ekuitas: "+rp(v.eq)+"\\n\\nLink data: https://faindonesia.co.id/kalkulator-valuasi-dcf/?"+qp+"&laporan=1";\n'
                  ' $("#dcf_wa").href="https://wa.me/6282245260121?text="+encodeURIComponent(m)}\n'
                  '(function(){const q=new URLSearchParams(location.search);if(!q.has("laporan")&&!q.has("fcf"))return;q.forEach((v,k)=>{const el=document.getElementById(k);if(el&&DIDS.includes(k))el.value=v});})();\n'
                  'calc();waRep();$$("input,select").forEach(e=>{e.addEventListener("input",waRep);e.addEventListener("change",waRep)});\n'
                  'if(new URLSearchParams(location.search).get("laporan")==="1")setTimeout(()=>window.print(),400);\n\n})();', 1)
    t = t.replace('"offers": {"@type": "Offer", "price": "99000", "priceCurrency": "IDR"}', '"offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR"}')
    t = t.replace("#faai-b,#faai,.fa-share,#dcf_pdf{display:none!important}", "#faai-b,#faai,.fa-share,#dcf_wa{display:none!important}")
    assert 'id="dcf_wa"' in t and "waRep()" in t, "patch DCF gagal"
    wr(p, t); print("  valuasi DCF: laporan via WA + prefill ?laporan=1")

# toko: kartu Valuasi RS jadi gratis (laporan lengkap via WA)
p = os.path.join(FA, "toko", "index.html")
if os.path.exists(p):
    t = rd(p)
    t = rep(t, [('<div class="pr"><b>Rp49.000</b><small>termasuk PPN · unduh laporan lengkap di aplikasi</small></div>', '<div class="pr"><b>Gratis</b><small>laporan lengkap dan strategi via WhatsApp</small></div>'),
                ('<article class="it" data-cat="app" data-for="ca" id="p-venus-rsval">', '<article class="it" data-cat="app" data-free="1" data-for="ca" id="p-venus-rsval">')], "toko RS gratis")
    wr(p, t)
print("fa_harga_20261105 (siang) selesai")
