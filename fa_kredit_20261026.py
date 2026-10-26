# -*- coding: utf-8 -*-
"""FA Venus · Cek Kapasitas Kredit (26 Okt 2026).
Screening gratis kemampuan pengajuan kredit baru / top up / take over:
repayment capacity (DSCR), plafon maksimal per batas (DSCR, Debt/EBITDA, DER, agunan, siklus modal kerja),
matriks plafon per suku bunga x tenor, bunga maksimal untuk plafon incaran, langkah lanjut.
QRIS donasi Rp10.001 dipasang prep.py (add_donasi). Lead ke Google Sheet yang sama dengan CariAkuntan.
Idempoten. Jalankan setelah fa_psak_20261026.py, sebelum prep.py.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
exec(_src[:_src.index("# ================= 1.")])  # P, rd, wtxt, set_head, set_main, faq_html, faq_ld, crumbs, E, D, TODAY, TPL_SVC, AUTHOR_BOX, wa

GS_URL = "https://script.google.com/macros/s/AKfycbzBAfPUXS1F9zcnRBz_Xg7-IhKRrLtyOtoNY9342G2gsXwgThcXwxcwq-VE3ywgK8Dniw/exec"
PATH = "/cek-kapasitas-kredit/"
URL = D + PATH
WA_NO = "6282245260121"
MAIL = "office@faindonesia.co.id"

CSS = r"""<style id="kk-css">
.kk{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);border:1px solid var(--line);background:var(--surface);margin:26px 0 34px}
.kk *{box-sizing:border-box}.kk-f{padding:26px 24px;min-width:0}.kk-r{padding:26px 24px;background:linear-gradient(160deg,#262626,#111);border-left:1px solid var(--line);position:relative;min-width:0}
.kk-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:20px}.kk-steps button{all:unset;cursor:pointer;font:500 12.5px/1.3 Poppins,sans-serif;color:var(--muted);border-top:3px solid #3a3a3a;padding-top:9px}
.kk-steps button.on{color:#fff;border-top-color:#fff}
.kk-p{display:none}.kk-p.on{display:block;animation:kkin .35s ease}@keyframes kkin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.kk label{display:block;font:500 13.5px/1.4 Poppins,sans-serif;margin:14px 0 6px}.kk label em{color:#ff8a8a;font-style:normal;margin-left:3px}.kk label small{color:var(--muted);font-weight:400;margin-left:6px}
.kk input,.kk select{width:100%;min-width:0;font:400 15px/1.3 Poppins,sans-serif;color:#fff;background:#121212;border:1px solid #3a3a3a;padding:11px 12px;border-radius:0}
.kk input:focus,.kk select:focus{outline:2px solid #fff;outline-offset:0}.kk input.miss{border-color:#ff8a8a}
.kk-row{display:grid;grid-template-columns:1fr 1fr;gap:0 12px}
.kk-chips{display:flex;flex-wrap:wrap;gap:8px}.kk-chips button{all:unset;cursor:pointer;font:500 13.5px/1 Poppins,sans-serif;padding:11px 14px;border:1px solid #444;color:#ddd}.kk-chips button.on{background:#fff;color:#171717;border-color:#fff}
.kk-nav{display:flex;justify-content:space-between;gap:10px;margin-top:22px;flex-wrap:wrap}
.kk .err{color:#ff8a8a;font-size:13px;min-height:1.2em;margin:10px 0 0}
.kk-hint{font-size:12.5px;color:var(--muted);margin:6px 0 0;line-height:1.5}
.kk-r h3{margin:0 0 14px;font-size:22px}
.kk-lock{position:absolute;inset:70px 24px auto 24px;z-index:2;border:1px solid #444;background:rgba(23,23,23,.92);padding:26px 18px;text-align:center;font:500 15px/1.5 Poppins,sans-serif}
.kk-res.blur{filter:blur(6px);pointer-events:none;user-select:none}
.kk-big{border:1px solid #444;padding:16px;margin-bottom:12px}.kk-big small{display:block;color:var(--muted);font-size:12.5px}.kk-big b{display:block;font:600 clamp(24px,3.4vw,34px)/1.15 Poppins,sans-serif;margin:4px 0}.kk-big i{font-style:normal;font-size:12.5px;color:#cfcfcf}
.kk-cap{display:grid;grid-template-columns:1fr auto;gap:6px 10px;font-size:13.5px;margin:0 0 14px;padding:0}.kk-cap span{color:#cfcfcf}.kk-cap b{font-weight:500;text-align:right;white-space:nowrap}.kk-cap .bind{color:#fff;font-weight:600}
.kk-bar{height:6px;background:#2c2c2c;margin:2px 0 10px;grid-column:1/-1}.kk-bar i{display:block;height:100%;background:#fff;width:0;transition:width .6s ease}
.kk-k{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:0 0 14px}.kk-k div{border:1px solid #3a3a3a;padding:10px}.kk-k small{display:block;font-size:11.5px;color:var(--muted)}.kk-k b{font-weight:600;font-size:16px}
.g2{color:#8fe3b0}.g1{color:#ffd27a}.g0{color:#ff8a8a}
.kk-note{font-size:12px;color:var(--muted);line-height:1.5;margin:12px 0 0}
.kk-out{margin:8px 0 34px}.kk-out h2{margin-top:28px}
.kk-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:10px 0 18px}.kk-tw table{min-width:520px;border-collapse:collapse;width:100%}
.kk-tw th,.kk-tw td{border:1px solid #333;padding:9px 10px;text-align:right;white-space:nowrap;font-size:14px}.kk-tw th:first-child,.kk-tw td:first-child{text-align:left}.kk-tw td.hl{background:#fff;color:#171717;font-weight:600}
.kk-next{list-style:none;padding:0;margin:10px 0;display:grid;gap:10px}.kk-next li{border:1px solid #333;padding:14px 16px;background:#1e1e1e;font-size:14.5px;line-height:1.55}.kk-next li b{display:block;font-weight:600;margin-bottom:2px}
@media (max-width:820px){.kk{grid-template-columns:1fr}.kk-r{border-left:0;border-top:1px solid var(--line)}.kk-lock{inset:64px 16px auto 16px}.kk-f,.kk-r{padding:22px 16px}}
@media (max-width:420px){.kk-row{grid-template-columns:1fr}.kk-k{grid-template-columns:1fr 1fr}}
</style>"""

def inp(id_, label, req=False, hint="", ph="0", val="", im="decimal"):
    r = '<em>*</em>' if req else '<small>opsional</small>'
    h = f'<p class="kk-hint">{hint}</p>' if hint else ""
    v = f' value="{val}"' if val else ""
    return f'<div><label for="{id_}">{label}{r}</label><input id="{id_}" inputmode="{im}" placeholder="{ph}"{v} autocomplete="off">{h}</div>'

FORM = f"""
<div class="kk" id="kk">
 <div class="kk-f">
  <div class="kk-steps" role="tablist"><button type="button" data-s="0" class="on">1 · Perusahaan</button><button type="button" data-s="1">2 · Angka Keuangan</button><button type="button" data-s="2">3 · Fasilitas</button></div>
  <div class="kk-p on" data-p="0">
   <div><label for="kk_pt">Nama PT<em>*</em></label><input id="kk_pt" placeholder="PT Contoh Sukses Abadi" autocomplete="organization"></div>
   <div><label for="kk_em">Email<em>*</em></label><input id="kk_em" type="email" inputmode="email" placeholder="nama@perusahaan.com" autocomplete="email"></div>
   <label>Tujuan</label><div class="kk-chips" id="kk_goal"><button type="button" class="on">Kredit Baru</button><button type="button">Top Up Kredit Eksisting</button><button type="button">Take Over Bank Lain</button><button type="button">Investor / IPO</button><button type="button">Belum Tahu</button></div>
   <label for="kk_unit">Satuan Angka</label><select id="kk_unit"><option value="1">Rupiah Juta</option><option value="1000">Rupiah Miliar</option></select>
   <p class="err" id="kk_e0"></p>
   <div class="kk-nav"><span></span><a class="btn solid" href="#kk" data-go="1">Lanjut →</a></div>
  </div>
  <div class="kk-p" data-p="1">
   <p class="kk-hint" style="margin-top:0">Pakai angka laporan keuangan tahun terakhir (audited atau inhouse). Titik ribuan boleh, contoh 12.500.</p>
   <div class="kk-row">{inp("kk_rev","Pendapatan Setahun",True)}{inp("kk_ebit","Laba Usaha (EBIT)",True,"Laba sebelum bunga dan pajak.")}</div>
   <div class="kk-row">{inp("kk_da","Penyusutan dan Amortisasi",True)}{inp("kk_tax","Pajak Penghasilan Dibayar")}</div>
   <div class="kk-row">{inp("kk_eq","Total Ekuitas",True)}{inp("kk_os","Sisa Utang Bank Saat Ini",True,"Semua fasilitas, isi 0 bila belum ada.")}</div>
   <div class="kk-row">{inp("kk_ds","Angsuran Bank per Bulan",True,"Pokok + bunga semua fasilitas berjalan.")}{inp("kk_col","Nilai Pasar Agunan Tambahan",False,"Agunan yang belum diikat bank.")}</div>
   <div class="kk-row">{inp("kk_ar","Piutang Usaha")}{inp("kk_inv","Persediaan")}</div>
   <div class="kk-row">{inp("kk_ap","Utang Usaha")}{inp("kk_ta","Total Aset",False,"Untuk cek jalur IPO dan investor.")}</div>
   <div class="kk-row">{inp("kk_pbt","Laba Sebelum Pajak Tahun Terakhir")}{inp("kk_pbt0","Laba Sebelum Pajak Tahun Sebelumnya")}</div>
   <div class="kk-row">{inp("kk_ita","Aset Tak Berwujud",False,"Goodwill, lisensi, software. Untuk menghitung NTA.")}{inp("kk_age","Lama Beroperasi (Tahun)",False,"","0","","numeric")}</div>
   <p class="err" id="kk_e1"></p>
   <div class="kk-nav"><a class="btn line" href="#kk" data-go="0">← Kembali</a><a class="btn solid" href="#kk" data-go="2">Lanjut →</a></div>
  </div>
  <div class="kk-p" data-p="2">
   <label>Jenis Fasilitas</label><div class="kk-chips" id="kk_type"><button type="button" class="on" data-t="ki">Kredit Investasi / Term Loan</button><button type="button" data-t="kmk">KMK Revolving</button></div>
   <div class="kk-row">{inp("kk_rate","Suku Bunga per Tahun (%)",True,"",'11',"11")}{inp("kk_ten","Tenor (Tahun)",True,"KMK revolving: bunga saja, diperpanjang tahunan.",'5',"5")}</div>
   <div class="kk-row">{inp("kk_want","Plafon yang Diincar","","Untuk menghitung bunga maksimal yang masih aman.")}{inp("kk_dscr","Target DSCR Bank",False,"Umumnya 1,2 sampai 1,5.",'1,25',"1,25")}</div>
   <div class="kk-row">{inp("kk_lev","Maks. Utang / EBITDA (x)",False,"",'3,5',"3,5")}{inp("kk_der","Maks. DER (x)",False,"",'2,5',"2,5")}</div>
   <div><label for="kk_nm">Nama Anda<small>opsional</small></label><input id="kk_nm" autocomplete="name"></div>
   <div><label for="kk_wa">Nomor WhatsApp<small>opsional</small></label><input id="kk_wa" inputmode="tel" autocomplete="tel"></div>
   <p class="err" id="kk_e2"></p>
   <div class="kk-nav"><a class="btn line" href="#kk" data-go="1">← Kembali</a><button type="button" class="btn solid" id="kk_go">Hitung Kredit &amp; Pendanaan</button></div>
  </div>
 </div>
 <div class="kk-r">
  <h3>Indikasi Kredit &amp; Pendanaan</h3>
  <div class="kk-lock" id="kk_lock">🔒<br>Isi data lalu tekan <b>Hitung Kredit &amp; Pendanaan</b> untuk melihat hasil.</div>
  <div class="kk-res blur" id="kk_res">
   <div class="kk-big"><small id="kk_lbl">Tambahan Plafon Indikatif</small><b id="kk_cap">Rp -</b><i id="kk_bind">Pembatas utama: -</i></div>
   <div class="kk-k"><div><small>DSCR Saat Ini</small><b id="kk_k1">-</b></div><div><small>Utang / EBITDA</small><b id="kk_k2">-</b></div><div><small>DER</small><b id="kk_k3">-</b></div></div>
   <div class="kk-cap" id="kk_caps"></div>
   <div class="kk-big" id="kk_ipobox"><small>Jalur IPO Indikatif</small><b id="kk_ipo" style="font-size:clamp(19px,2.4vw,24px)">-</b><i id="kk_ipot"></i></div>
   <div class="kk-big" id="kk_wantbox" style="display:none"><small>Bunga Maksimal untuk Plafon Incaran</small><b id="kk_maxr">-</b><i id="kk_wantt"></i></div>
  </div>
  <p class="kk-note">Indikasi otomatis dari angka yang Anda isi, bukan keputusan bank. Setiap bank memakai kebijakan, agunan, dan analisis industri sendiri.</p>
 </div>
</div>
<div class="kk-out" id="kk_out" style="display:none">
 <h2>Kemampuan Bayar per Suku Bunga dan Tenor</h2>
 <p class="t">Pinjaman yang sanggup dibayar dari arus kas pada target DSCR Anda, untuk tiap kombinasi bunga dan tenor. Sel yang disorot adalah asumsi Anda.</p>
 <div class="kk-tw"><table id="kk_mx"></table></div><p class="kk-note" id="kk_mxn"></p>
 <h2>Jalur Pendanaan Ekuitas dan IPO</h2>
 <p class="t">Uji cepat terhadap syarat keuangan pencatatan saham di Bursa Efek Indonesia. Syarat lengkap (free float, jumlah pemegang saham, opini audit, tata kelola) dinilai saat persiapan.</p>
 <div class="kk-tw"><table id="kk_ipotb"></table></div><p class="kk-note">Acuan: Peraturan BEI Nomor I-A (opsi keuangan Papan Utama), perubahan yang berlaku 4 Februari 2026 (masa operasi dan free float), dan POJK 53/2017 untuk emiten aset skala kecil dan menengah. Bukan nasihat investasi.</p>
 <h2>Langkah Selanjutnya</h2>
 <ol class="kk-next" id="kk_next"></ol>
 <div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:18px 0 6px"><a class="btn solid" id="kk_wa_btn" href="#" target="_blank" rel="noopener">Kirim Hasil ke Ananta, CPA</a><a class="btn line" id="kk_mail" href="#">Kirim via Email</a></div>
 <p class="kk-note" id="kk_done" style="display:none">Terima kasih. Data Anda sudah kami terima dan hanya dipakai untuk menindaklanjuti screening ini.</p>
</div>
"""

JS = r"""<script>(function(){
var D=__D__,R=document.getElementById("kk"),$=function(i){return document.getElementById(i)};
function num(v){if(v==null)return null;v=String(v).trim().replace(/\s/g,"").replace(/^rp/i,"");if(!v)return null;if(/,\d{1,2}$/.test(v))v=v.replace(/\./g,"").replace(",",".");else if(/^\d{1,3}(\.\d{3})+$/.test(v))v=v.replace(/\./g,"");else v=v.replace(/,/g,"");var n=parseFloat(v);return isFinite(n)?n:null}
function g(i){return num($(i).value)}
var U=function(){return +$("kk_unit").value};
function rp(x){if(x==null||!isFinite(x))return "-";var j=x*U();var neg=j<0;j=Math.abs(j);var s=j>=1000?(Math.round(j/10)/100).toLocaleString("id-ID",{maximumFractionDigits:2})+" miliar":Math.round(j).toLocaleString("id-ID")+" juta";return (neg?"-":"")+"Rp"+s}
function x1(v){return v==null||!isFinite(v)?"-":v.toLocaleString("id-ID",{maximumFractionDigits:2})+"x"}
var goal="Kredit Baru",type="ki";
function chips(id,cb){$(id).addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;[].forEach.call(this.children,function(c){c.classList.remove("on")});b.classList.add("on");cb(b)})}
chips("kk_goal",function(b){goal=b.textContent});
chips("kk_type",function(b){type=b.dataset.t;if(type==="kmk"&&g("kk_ten")>1)$("kk_ten").value="1";if(type==="ki"&&g("kk_ten")<=1)$("kk_ten").value="5"});
function show(s){R.querySelectorAll(".kk-p").forEach(function(p){p.classList.toggle("on",+p.dataset.p===s)});R.querySelectorAll(".kk-steps button").forEach(function(b){b.classList.toggle("on",+b.dataset.s<=s)})}
function v0(){var pt=$("kk_pt").value.trim(),em=$("kk_em").value.trim();return pt.length>2&&/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(em)}
var REQ=[["kk_rev","Pendapatan"],["kk_ebit","Laba Usaha"],["kk_da","Penyusutan"],["kk_eq","Ekuitas"],["kk_os","Sisa Utang Bank"],["kk_ds","Angsuran per Bulan"]];
function v1(){var m=[];REQ.forEach(function(r){var e=$(r[0]);var ok=num(e.value)!=null;e.classList.toggle("miss",!ok);if(!ok)m.push(r[1])});$("kk_e1").textContent=m.length?"Lengkapi: "+m.join(", "):"";return !m.length}
function v2(){var ok=g("kk_rate")>0&&g("kk_ten")>0;$("kk_e2").textContent=ok?"":"Isi suku bunga dan tenor.";return ok}
function go(s){if(s>=1&&!v0()){$("kk_e0").textContent="Isi nama PT dan email yang valid.";show(0);return}$("kk_e0").textContent="";if(s>=2&&!v1()){show(1);return}show(s)}
R.addEventListener("click",function(e){var a=e.target.closest("[data-go]");if(a){e.preventDefault();go(+a.dataset.go)}var b=e.target.closest(".kk-steps button");if(b)go(+b.dataset.s)});
function annF(r,n){var i=r/12,m=Math.round(n*12);return i>0?(1-Math.pow(1+i,-m))/i:m}
function model(rate,ten){var rev=g("kk_rev"),ebit=g("kk_ebit"),da=g("kk_da")||0,tax=g("kk_tax")||0,eq=g("kk_eq"),os=g("kk_os")||0,ds=(g("kk_ds")||0)*12,col=g("kk_col"),ar=g("kk_ar"),inv=g("kk_inv"),ap=g("kk_ap")||0;
 var dscr=(num($("kk_dscr").value)||1.25),lev=(num($("kk_lev").value)||3.5),derM=(num($("kk_der").value)||2.5);
 var ebitda=ebit+da,cfads=ebitda-tax,r=rate/100,roomDS=cfads/dscr-ds;
 var capD=roomDS<=0?0:(type==="kmk"?roomDS/r:roomDS/12*annF(r,ten));
 var caps=[["Kemampuan Bayar (DSCR "+dscr.toLocaleString("id-ID")+"x)",capD,"dscr"],["Batas Utang / EBITDA "+lev.toLocaleString("id-ID")+"x",Math.max(0,lev*ebitda-os),"lev"],["Batas DER "+derM.toLocaleString("id-ID")+"x",eq>0?Math.max(0,derM*eq-os):0,"der"]];
 if(col!=null&&col>0)caps.push(["Agunan Tambahan (LTV 70%)",col*0.7,"col"]);
 if(type==="kmk"&&(ar!=null||inv!=null)){var wc=(ar||0)+(inv||0)-ap;caps.push(["Siklus Modal Kerja (75% dari piutang + persediaan - utang usaha)",Math.max(0,wc*0.75),"wc"])}
 var b=caps[0];caps.forEach(function(c){if(c[1]<b[1])b=c});
 return {rev:rev,ebitda:ebitda,cfads:cfads,ds:ds,os:os,eq:eq,dscrNow:ds>0?cfads/ds:null,levNow:ebitda>0?os/ebitda:null,derNow:eq>0?os/eq:null,caps:caps,bind:b,cap:Math.max(0,b[1]),dscrT:dscr,lev:lev,derM:derM,r:r,ten:ten}}
function maxRate(want,ten){var lo=0.001,hi=0.6,M=model(11,ten);var room=M.cfads/M.dscrT-M.ds;if(room<=0)return null;
 function need(r){return type==="kmk"?want*r:want/annF(r,ten)*12}
 if(need(lo)>room)return 0;if(need(hi)<=room)return hi*100;for(var k=0;k<60;k++){var m=(lo+hi)/2;if(need(m)<=room)lo=m;else hi=m}return lo*100}
function ipoCheck(){var J=function(i){var v=g(i);return v==null?null:v*U()},eq=J("kk_eq"),ita=J("kk_ita")||0,ta=J("kk_ta"),pb=J("kk_pbt"),pb0=J("kk_pbt0"),rv=J("kk_rev"),age=g("kk_age"),nta=eq==null?null:eq-ita;
 var B=function(x){return x==null?"Data Belum Diisi":x?"Memenuhi":"Belum"},T=[];
 var o1=nta==null||pb==null?null:(nta>=250000&&pb>0),o2=pb==null||pb0==null?null:(pb+pb0>=100000),o3=rv==null?null:rv>=800000,o4=ta==null?null:ta>=2000000,ag3=age==null?null:age>=3,ag2=age==null?null:age>=2;
 T.push(["Papan Utama, Opsi 1","Aset berwujud bersih (NTA) min. Rp250 miliar dan laba sebelum pajak tahun terakhir positif",B(o1)]);
 T.push(["Papan Utama, Opsi 2","Laba sebelum pajak kumulatif 2 tahun min. Rp100 miliar, kapitalisasi pasar min. Rp1 triliun saat IPO",B(o2)]);
 T.push(["Papan Utama, Opsi 3","Pendapatan tahun terakhir min. Rp800 miliar, kapitalisasi pasar min. Rp8 triliun",B(o3)]);
 T.push(["Papan Utama, Opsi 4","Total aset min. Rp2 triliun, kapitalisasi pasar min. Rp4 triliun",B(o4)]);
 T.push(["Masa Operasi Papan Utama","Usaha utama berjalan komersial min. 36 bulan, ada pendapatan 3 tahun buku terakhir",B(ag3)]);
 T.push(["Papan Pengembangan","Masa operasi min. 24 bulan; opsi keuangan lebih ringan dari Papan Utama, dicek detail saat persiapan",B(ag2)]);
 T.push(["Papan Akselerasi","Emiten aset skala kecil atau menengah: total aset sampai Rp250 miliar",B(ta==null?null:ta<=250000)]);
 var utama=(o1||o2||o3||o4)&&ag3!==false,head,sub;
 if(utama){head="Kandidat Papan Utama";sub="Free float min. 25% bila kapitalisasi pasar di bawah Rp5 triliun, min. 300 juta saham, 10.000 pemegang saham."}
 else if(ta!=null&&ta<=250000){head="Kandidat Papan Akselerasi";sub="Aset skala kecil atau menengah. Papan Pengembangan juga bisa dijajaki."}
 else if(ag2){head="Kandidat Papan Pengembangan";sub="Belum masuk opsi Papan Utama. Investor strategis atau PE bisa menjadi jembatan."}
 else if(ta==null&&pb==null){head="Isi Total Aset dan Laba";sub="Lengkapi untuk melihat jalur IPO."}
 else{head="Investor Privat Dulu";sub="Bangun rekam jejak 2 sampai 3 tahun dengan laporan audit, lalu siapkan IPO."}
 var tb="<thead><tr><th>Jalur</th><th>Syarat Keuangan</th><th>Status</th></tr></thead><tbody>"+T.map(function(r){return "<tr><td>"+r[0]+"</td><td style=\"white-space:normal;min-width:260px;text-align:left\">"+r[1]+"</td><td class=\""+(r[2]==="Memenuhi"?"g2":r[2]==="Belum"?"g0":"")+"\">"+r[2]+"</td></tr>"}).join("")+"</tbody>";
 return {head:head,sub:sub,tbl:tb,utama:utama,any:head.indexOf("Kandidat")===0}}
function cls(v,good,ok,lowGood){if(v==null)return "";return lowGood?(v<=good?"g2":v<=ok?"g1":"g0"):(v>=good?"g2":v>=ok?"g1":"g0")}
var last=null;
function calc(){if(!v0()){go(0);return false}if(!v1()){show(1);return false}if(!v2())return false;
 var rate=g("kk_rate"),ten=g("kk_ten"),M=model(rate,ten);last=M;
 $("kk_lock").style.display="none";$("kk_res").classList.remove("blur");
 $("kk_lbl").textContent=goal.indexOf("Top Up")===0?"Ruang Top Up Indikatif":goal.indexOf("Take Over")===0?"Tambahan Plafon di Luar Take Over":"Tambahan Plafon Indikatif";
 $("kk_cap").textContent=rp(M.cap);$("kk_bind").textContent="Pembatas utama: "+M.bind[0];
 var k1=$("kk_k1"),k2=$("kk_k2"),k3=$("kk_k3");k1.textContent=M.dscrNow==null?"Belum Ada Utang":x1(M.dscrNow);k1.className=cls(M.dscrNow,1.5,1.2);k2.textContent=x1(M.levNow);k2.className=cls(M.levNow,2.5,3.5,1);k3.textContent=x1(M.derNow);k3.className=cls(M.derNow,1.5,2.5,1);
 var mx=Math.max.apply(null,M.caps.map(function(c){return c[1]}))||1;
 $("kk_caps").innerHTML=M.caps.map(function(c){return '<span'+(c===M.bind?' class="bind"':'')+'>'+c[0]+'</span><b'+(c===M.bind?' class="bind"':'')+'>'+rp(c[1])+'</b><div class="kk-bar"><i style="width:'+Math.max(2,c[1]/mx*100)+'%"></i></div>'}).join("");
 var want=g("kk_want");if(want&&want>0){var mr=maxRate(want,ten);$("kk_wantbox").style.display="block";var mt=null;if(mr==null||mr===0){var rm=M.cfads/M.dscrT-M.ds;if(rm>0&&type!=="kmk")for(var tt=1;tt<=20;tt++){if(want/annF(rate/100,tt)*12<=rm){mt=tt;break}}}$("kk_maxr").textContent=mr==null||mr===0?(mt?"Perlu Tenor Minimal "+mt+" Tahun di Bunga "+rate+"%":"Belum Terjangkau, Turunkan Plafon"):mr>=60?"Aman di Semua Bunga Wajar":mr.toLocaleString("id-ID",{maximumFractionDigits:2})+"% per tahun";
  var nonD=Math.min.apply(null,M.caps.filter(function(c){return c[2]!=="dscr"}).map(function(c){return c[1]}));
  $("kk_wantt").textContent="Plafon "+rp(want)+", tenor "+ten+" tahun"+(want>nonD?". Catatan: melebihi batas "+M.caps.filter(function(c){return c[2]!=="dscr"&&c[1]<want}).map(function(c){return c[0].split(" (")[0]}).join(", "):"")}else $("kk_wantbox").style.display="none";
 var rates=[];for(var d=-3;d<=3;d++){var rr=Math.round((rate+d)*10)/10;if(rr>0)rates.push(rr)}
 var tens=type==="kmk"?[1]:[3,5,7,10];if(type!=="kmk"&&tens.indexOf(ten)<0){tens.push(ten);tens.sort(function(a,b){return a-b})}
 var h="<thead><tr><th>Bunga / Tenor</th>"+tens.map(function(t){return "<th>"+(type==="kmk"?"Revolving":t+" Tahun")+"</th>"}).join("")+"</tr></thead><tbody>";
 rates.forEach(function(r){h+="<tr><td>"+r.toLocaleString("id-ID")+"%</td>"+tens.map(function(t){var m=model(r,t),cd=m.caps[0][1],lim=Math.min.apply(null,m.caps.slice(1).map(function(c){return c[1]}));return '<td'+(r===rate&&(type==="kmk"||t===ten)?' class="hl"':'')+'>'+rp(cd)+(cd>lim?" *":"")+"</td>"}).join("")+"</tr>"});
 $("kk_mx").innerHTML=h+"</tbody>";var bnd=M.caps.slice(1).reduce(function(a,c){return c[1]<a[1]?c:a});$("kk_mxn").textContent="* Melebihi "+bnd[0]+" sebesar "+rp(bnd[1])+". Bagian di atas batas ini perlu agunan, ekuitas, atau struktur fasilitas tambahan.";
 var ipo=ipoCheck();$("kk_ipo").textContent=ipo.head;$("kk_ipot").textContent=ipo.sub;$("kk_ipotb").innerHTML=ipo.tbl;
 var N=[];
 if(M.cfads<=0)N.push(["Perbaiki Arus Kas Operasi Dulu","EBITDA setelah pajak belum positif. Bank akan menolak tambahan kredit sebelum ada perbaikan laba atau restrukturisasi biaya."]);
 if(M.bind[2]==="dscr"&&M.cfads>0)N.push(["Perpanjang Tenor atau Restrukturisasi Angsuran","Batas utama ada di kemampuan bayar. Tenor lebih panjang, grace period, atau take over ke bunga lebih rendah bisa menaikkan plafon tanpa menambah agunan."]);
 if(M.bind[2]==="lev")N.push(["Naikkan EBITDA yang Diakui Bank","Rapikan pos biaya nonrutin, pisahkan biaya pemilik, dan pastikan laporan keuangan mencerminkan laba operasi yang sebenarnya, idealnya diaudit KAP rekanan bank."]);
 if(M.bind[2]==="der")N.push(["Perkuat Ekuitas","Opsi: setoran modal, konversi pinjaman pemegang saham menjadi modal, atau revaluasi aset tetap sesuai PSAK 216 dengan penilaian KJPP."]);
 if(M.bind[2]==="col")N.push(["Tambah atau Nilai Ulang Agunan","Penilaian KJPP yang tepat, agunan tambahan, atau struktur berbasis transaksi seperti invoice financing dan trust receipt."]);
 if(M.bind[2]==="wc")N.push(["Data Piutang dan Persediaan","Plafon KMK mengikuti siklus modal kerja. Siapkan umur piutang dan perputaran persediaan yang rapi agar bank bisa menghitung borrowing base."]);
 if(M.dscrNow!=null&&M.dscrNow<1.2)N.push(["DSCR Saat Ini Masih Tipis","Fokuskan top up untuk refinancing yang menurunkan angsuran, bukan tambahan utang baru."]);
 if(ipo.any||goal.indexOf("IPO")>=0){N.push(["Jalur IPO: Audit 3 Tahun dan SAK Indonesia","Laporan keuangan diaudit KAP terdaftar OJK dengan SAK Indonesia. Bila masih SAK EP, mulai <a href=\"/jasa-transisi-sak-ep-ke-psak/\">transisi ke PSAK</a> dari sekarang."]);N.push(["Tata Kelola Sebelum IPO","Komisaris independen, komite audit, dan sekretaris perusahaan. Lihat <a href=\"/komite-audit-komisaris-independen/\">komite audit dan komisaris independen</a> serta <a href=\"/konsultan-persiapan-ipo/\">persiapan IPO</a>."])}
 N.push(["Siapkan Paket Pengajuan","Laporan keuangan 3 tahun dengan CALK, rekening koran 6 sampai 12 bulan, proyeksi arus kas, dan memo penggunaan dana. Kami bantu susun sampai siap komite kredit."]);
 N.push(["Diskusi Awal Gratis","Kirim hasil ini ke Ananta, CPA. Kami baca dulu sebelum Anda mendatangi bank, supaya pengajuan pertama tidak ditolak."]);
 $("kk_next").innerHTML=N.map(function(n){return "<li><b>"+n[0]+"</b>"+n[1]+"</li>"}).join("");
 $("kk_out").style.display="block";
 var s=summary();$("kk_wa_btn").href="https://wa.me/"+D.wa+"?text="+encodeURIComponent(s);$("kk_mail").href="mailto:"+D.mail+"?subject="+encodeURIComponent("Cek Kapasitas Kredit - "+$("kk_pt").value)+"&body="+encodeURIComponent(s);
 sheet("hitung");try{if(window.gtag)gtag("event","generate_lead",{method:"calculator",form:"cek-kapasitas-kredit"})}catch(x){}
 return true}
function summary(){var M=last,L=["Halo Pak Ananta, saya sudah cek kredit dan pendanaan di faindonesia.co.id:","","PT: "+$("kk_pt").value,"Tujuan: "+goal,"Fasilitas: "+(type==="kmk"?"KMK Revolving":"Kredit Investasi / Term Loan"),"Bunga "+g("kk_rate")+"%, tenor "+g("kk_ten")+" tahun",""];
 [["Total Aset","kk_ta"],["Laba Sebelum Pajak","kk_pbt"],["Laba Sebelum Pajak Th Sebelumnya","kk_pbt0"],["Aset Tak Berwujud","kk_ita"],["Pendapatan","kk_rev"],["Laba Usaha","kk_ebit"],["Penyusutan","kk_da"],["Pajak","kk_tax"],["Ekuitas","kk_eq"],["Sisa Utang Bank","kk_os"],["Angsuran/Bulan","kk_ds"],["Agunan Tambahan","kk_col"],["Piutang","kk_ar"],["Persediaan","kk_inv"],["Utang Usaha","kk_ap"],["Plafon Diincar","kk_want"]].forEach(function(r){var v=g(r[1]);if(v!=null)L.push(r[0]+": "+rp(v))});
 L.push("","DSCR saat ini: "+(M.dscrNow==null?"-":x1(M.dscrNow)),"Utang/EBITDA: "+x1(M.levNow),"DER: "+x1(M.derNow),"Plafon indikatif: "+rp(M.cap)+" (pembatas: "+M.bind[0]+")");
 L.push("Jalur IPO indikatif: "+$("kk_ipo").textContent);
 if($("kk_wantbox").style.display!=="none")L.push("Bunga maksimal plafon incaran: "+$("kk_maxr").textContent);
 L.push("","Nama: "+($("kk_nm").value||"-"),"Email: "+$("kk_em").value,"WA: "+($("kk_wa").value||"-"));return L.join("\n")}
function sheet(m){try{var p=new URLSearchParams();p.append("pt",$("kk_pt").value);p.append("email",$("kk_em").value);p.append("goal","FA Cek Kredit & Pendanaan: "+goal);p.append("unit",$("kk_unit").options[$("kk_unit").selectedIndex].text);
 p.append("nama",$("kk_nm").value);p.append("wa",$("kk_wa").value?"'"+$("kk_wa").value:"");p.append("lang","id");p.append("page","faindonesia.co.id"+location.pathname+" ("+m+")");p.append("summary",summary());
 if(navigator.sendBeacon&&navigator.sendBeacon(D.gs,p))return;fetch(D.gs,{method:"POST",mode:"no-cors",body:p,keepalive:true})}catch(x){}}
$("kk_go").addEventListener("click",function(){if(calc())setTimeout(function(){$("kk_res").scrollIntoView({behavior:"smooth",block:"start"})},60)});
["kk_wa_btn","kk_mail"].forEach(function(i){$(i).addEventListener("click",function(){$("kk_done").style.display="block"})});
})();</script>"""
JS = JS.replace("__D__", json.dumps({"wa": WA_NO, "mail": MAIL, "gs": GS_URL}))

ABOUT = (
 "<h2>Cara Bank Menghitung Kemampuan Bayar</h2>"
 "<p>Analis kredit membaca arus kas yang tersedia untuk membayar utang, yaitu EBITDA dikurangi pajak, lalu membandingkannya dengan seluruh angsuran pokok dan bunga. "
 "Rasio ini disebut DSCR. Bank umumnya meminta DSCR minimal sekitar 1,2 sampai 1,5 kali. Plafon akhir juga dibatasi rasio utang terhadap EBITDA, DER, nilai agunan, dan untuk KMK, kebutuhan modal kerja dari siklus piutang dan persediaan. Kalkulator ini menghitung semua batas itu lalu mengambil yang paling kecil.</p>"
 "<h2>Pertanyaan Umum</h2>")
FAQ = [
 ("Apakah hasil kalkulator ini sama dengan keputusan bank?", "Tidak. Ini indikasi awal dari angka yang Anda isi. Bank juga menilai karakter, industri, riwayat SLIK, agunan, dan kebijakan internalnya."),
 ("Berapa DSCR yang aman?", "Banyak bank memakai batas minimal sekitar 1,2 sampai 1,5 kali. Semakin tinggi DSCR, semakin besar ruang tambahan kredit dan posisi tawar bunga."),
 ("Apa beda kredit investasi dan KMK revolving dalam perhitungan ini?", "Kredit investasi dihitung dengan angsuran pokok plus bunga selama tenor. KMK revolving dihitung bunga saja karena pokok umumnya diperpanjang tahunan, tetapi dibatasi kebutuhan modal kerja."),
 ("Apakah data saya disimpan?", "Data yang Anda kirim dipakai hanya untuk menindaklanjuti screening ini. Detail laporan keuangan lengkap baru kami minta setelah NDA."),
 ("Benarkah gratis?", "Ya. Di akhir ada pilihan donasi sukarela lewat QRIS sebesar Rp10.001 yang boleh dilewati."),
]
main = (f'<section class="block">\n<div class="wrap art">\n<p class="eyebrow">FA Venus · Kalkulator Gratis</p>\n'
        f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">Cek Kredit dan Pendanaan: Berapa Plafon yang Sanggup Ditanggung, dan Sudah Layak IPO?</h1>\n'
        f'<p class="t" style="max-width:62em">Untuk kredit baru, top up kredit eksisting, take over, sampai investor dan IPO. Isi angka ringkas laporan keuangan, lalu lihat repayment capacity (DSCR), plafon indikatif per suku bunga dan tenor, bunga maksimal yang masih aman, jalur papan BEI yang mungkin, dan langkah selanjutnya. Gratis.</p>\n'
        f'{FORM}\n{ABOUT}{faq_html(FAQ)}\n'
        f'<p class="t">Butuh pendampingan sampai cair? Lihat <a href="/konsultan-kredit-bank/">Konsultan Kredit Bank</a> atau <a href="/konsultan-kredit-distributor-importir/">Kredit Distributor dan Importir</a>.</p>\n'
        f'{AUTHOR_BOX}\n</div>\n</section>')
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebApplication", "name": "FA Venus · Cek Kredit dan Pendanaan", "url": URL, "applicationCategory": "FinanceApplication", "operatingSystem": "Web",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR"}, "provider": PROVIDER, "inLanguage": "id"},
    faq_ld(FAQ), crumbs([("FA Indonesia", D + "/"), ("Apps", D + "/apps/"), ("Cek Kredit dan Pendanaan", URL)])]}
title = "Cek Kredit & Pendanaan Gratis: DSCR, Plafon, Kelayakan IPO | FA Indonesia"
desc = "Kalkulator gratis kredit dan pendanaan: repayment capacity (DSCR), plafon per bunga dan tenor, bunga maksimal, dan uji cepat syarat IPO Papan Utama, Pengembangan, Akselerasi BEI."
page = set_main(set_head(TPL_SVC, title, desc, URL, ld), main).replace("</head>", CSS + "</head>", 1).replace("</body>", JS + "</body>", 1)
p = P("cek-kapasitas-kredit", "index.html"); os.makedirs(os.path.dirname(p), exist_ok=True); wtxt(p, page)

# ---------- CTA di halaman kredit ----------
def box(title, text):
    return (f'<!--fa-kk--><div style="margin:26px 0;padding:20px 22px;border:1px solid #444;border-radius:12px;background:#1e1e1e">'
            f'<p style="margin:0 0 6px;font-weight:600">{E(title)}</p><p style="margin:0 0 12px">{E(text)}</p>'
            f'<a class="btn solid" href="{PATH}">Cek Kredit &amp; Pendanaan Gratis</a></div><!--/fa-kk-->')
INJ = {
 ("konsultan-kredit-bank",): box("Berapa Plafon yang Realistis?", "Hitung repayment capacity, plafon per suku bunga dan tenor, serta bunga maksimal yang masih aman. Gratis, 3 menit."),
 ("konsultan-kredit-distributor-importir",): box("Cek Dulu Ruang Plafon Anda", "Kalkulator gratis untuk kredit baru, top up, atau take over, termasuk batas siklus modal kerja untuk KMK."),
 ("artikel", "rasio-keuangan-yang-dilihat-bank"): box("Hitung Rasio Anda Sekarang", "DSCR, utang terhadap EBITDA, dan DER langsung terhitung, lengkap dengan plafon indikatif."),
 ("artikel", "kmk-vs-kredit-investasi"): box("Bandingkan KMK dan Kredit Investasi", "Lihat plafon indikatif untuk kedua jenis fasilitas dengan angka perusahaan Anda."),
 ("artikel", "alasan-kredit-bank-ditolak"): box("Cek Sebelum Mengajukan", "Ketahui batas mana yang paling menahan plafon Anda sebelum bertemu bank."),
}
for parts, b in INJ.items():
    q = P(*parts, "index.html")
    if not os.path.exists(q): print("skip", q); continue
    t = re.sub(r"<!--fa-kk-->.*?<!--/fa-kk-->", "", rd(q), flags=re.S)
    k = t.find('<div style="margin:44px 0 0;padding:22px 24px;border:1px solid #333')
    if k < 0: k = t.find("</main>")
    wtxt(q, t[:k] + b + t[k:])

# /layanan/ tombol
lp = P("layanan", "index.html"); t = re.sub(r"<!--fa-kk-->.*?<!--/fa-kk-->", "", rd(lp), flags=re.S)
anchor = '<a class="btn line" href="/konsultan-kredit-distributor-importir/">'
if anchor in t: t = t.replace(anchor, f'<!--fa-kk--><a class="btn line" href="{PATH}">Cek Kredit &amp; Pendanaan</a><!--/fa-kk-->' + anchor, 1)
wtxt(lp, t)

# sitemap & llms
sm = re.sub(r"<!--fa-kk-->.*?<!--/fa-kk-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", f"<!--fa-kk-->\n<url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><priority>0.9</priority></url>\n<!--/fa-kk-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = re.sub(r"\n## Kalkulator Kredit.*?(?=\n## |\Z)", "", rd(P("llms.txt")), flags=re.S)
ll = ll.rstrip("\n") + f"\n\n## Kalkulator Kredit\n- FA Venus Cek Kredit dan Pendanaan (gratis): repayment capacity/DSCR, plafon indikatif per bunga dan tenor, bunga maksimal, uji cepat syarat IPO Papan Utama/Pengembangan/Akselerasi BEI, kredit baru/top up/take over/investor → {URL}\n"
wtxt(P("llms.txt"), ll)
print("ok", PATH)

# /apps/ kartu FA Venus baru (setelah kartu PSAK 118)
ap = P("apps", "index.html"); t = re.sub(r"<!--fa-kk-->.*?<!--/fa-kk-->", "", rd(ap), flags=re.S)
card = ('<!--fa-kk--><div class="ap-app"><div class="nm"><b>FA Venus · Cek Kredit &amp; Pendanaan</b><span class="chip on">Gratis</span></div>'
        '<p>Hitung repayment capacity (DSCR), plafon per suku bunga dan tenor, bunga maksimal yang masih aman, dan uji cepat syarat IPO di BEI.</p>'
        f'<a class="btn solid sm" href="{PATH}">Buka FA Venus</a></div><!--/fa-kk-->')
m = re.search(r'<div class="ap-app"><div class="nm"><b>FA Venus · Konversi PL PSAK 118</b>.*?</a></div>', t, re.S)
if m: t = t[:m.end()] + card + t[m.end():]
else: print("apps card anchor not found")
wtxt(ap, t)

# ---------- Beranda: kalkulator tepat di bawah hero (26 Okt 2026 malam) ----------
hp = P("index.html"); t = rd(hp)
t = re.sub(r"<!--fa-kk-home-->.*?<!--/fa-kk-home-->", "", t, flags=re.S)
home_sec = ('<!--fa-kk-home--><section class="block" id="cek-kredit"><div class="wrap">'
            '<div class="head"><p class="eyebrow">FA Venus · Gratis</p><h2 class="aph">Cek Kredit &amp; Pendanaan, <em>3 Menit.</em></h2></div>'
            '<p class="t" style="max-width:62em">Kredit baru, top up, take over, sampai investor dan IPO. Lihat repayment capacity, plafon yang sanggup ditanggung di tiap suku bunga, jalur papan BEI yang mungkin, dan langkah selanjutnya.</p>'
            + FORM + '</div></section>' + CSS + JS + '<!--/fa-kk-home-->')
anchor = '<section class="block alt hs" id="peta">'
assert anchor in t, "anchor beranda tidak ketemu"
t = t.replace(anchor, home_sec + anchor, 1)
wtxt(hp, t)
print("home ok")
