/* FA Paywall QRIS v2 (1 Nov 2026). Tidak ada akses gratis tanpa data:
   1) "Saya sudah bayar": isi nama, WA, nama usaha, dan referensi transaksi QRIS, lalu terbuka di perangkat ini.
   2) "Coba dulu 7 hari": isi nama, WA, nama usaha, bentuk usaha, kota, lalu terbuka 7 hari.
   Data dikirim ke Google Sheet lead (Apps Script) yang sama dengan Cek Kredit.
   Pakai: window.FA_PAY={app,name,price,guard?} lalu <script src="/js/fa-paywall.js" defer>,
   atau atribut data-app, data-name, data-price, data-guard pada tag script.
   guard = selector tombol: modal baru muncul saat tombol itu diklik (untuk halaman yang juga berisi artikel). */
(function(){
"use strict";
var S=document.currentScript||{},C=window.FA_PAY||{},ds=(S.dataset||{});
var app=C.app||ds.app||location.pathname.replace(/\W+/g,"-")||"app";
var name=C.name||ds.name||document.title.split("|")[0].trim();
var price=+(C.price||ds.price||25000);
/* 4 Nov 2026: semua aplikasi bebas dipakai. Yang berbayar hanya unduhan hasil lengkap (PDF, Excel, Word, export, salin).
   Selektor tombol berbayar: C.full / data-full, default DEF. Konfigurasi guard lama (tombol hitung) diabaikan. */
var DEF='[data-fa-full],#btnXlsx,#cp,#cpY,#fp_pr,[data-act="calkdoc"],[data-action="c-export"]';
var guard=C.full||ds.full||DEF;
var GS="__GS__",QR="__QR__",TRIAL_DAYS=7;
var KP="fa_akses_"+app,KT="fa_trial_"+app,KD="fa_pay_data";
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function open_(){if(ls(KP)||(C.skipKey&&ls(C.skipKey)))return true;var t=+ls(KT);return !!(t&&Date.now()-t<TRIAL_DAYS*864e5)}
var rp=function(n){return "Rp"+new Intl.NumberFormat("id-ID").format(n)};
var css="#fapw{position:fixed;inset:0;z-index:9999;background:rgba(10,10,10,.84);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);display:flex;align-items:flex-start;justify-content:center;overflow:auto;padding:max(16px,env(safe-area-inset-top)) 16px 24px;font-family:Poppins,system-ui,-apple-system,'Segoe UI',sans-serif;color:#fff;text-align:left}"+
"#fapw *{box-sizing:border-box}"+
"#fapw .bx{width:100%;max-width:410px;margin:auto;background:#1E1E1E;border:1px solid #2F2F2F;border-radius:10px;padding:22px 20px 16px;box-shadow:0 30px 80px -20px rgba(0,0,0,.9);animation:fapwIn .45s cubic-bezier(.2,.7,.2,1) both}"+
"@keyframes fapwIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}"+
"#fapw small{display:block;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#A8A8A8}"+
"#fapw h2{font-family:'EB Garamond',Georgia,serif;font-weight:400;font-size:24px;line-height:1.2;margin:6px 0 2px;color:#fff}"+
"#fapw .pr{font-size:30px;font-weight:300;margin:6px 0 2px;font-variant-numeric:tabular-nums}"+
"#fapw .pr span{font-size:12.5px;color:#A8A8A8;margin-left:6px}"+
"#fapw .qr{background:#fff;border-radius:8px;padding:10px;margin:14px 0 12px;text-align:center}"+
"#fapw .qr img{width:100%;max-width:280px;height:auto;display:block;margin:0 auto}"+
"#fapw ol{margin:0 0 14px;padding-left:18px;font-size:13px;color:#D8D8D8;line-height:1.55}"+
"#fapw ol b{color:#fff;font-weight:500}"+
"#fapw .go{display:block;width:100%;border:0;border-radius:999px;background:#fff;color:#171717;font:500 14px Poppins,system-ui,sans-serif;padding:12px 18px;cursor:pointer;margin-top:8px}"+
"#fapw .go:hover{background:#E8E8E8}"+
"#fapw .alt{display:block;width:100%;border:1px solid rgba(255,255,255,.35);border-radius:999px;background:transparent;color:#fff;font:500 13.5px Poppins,system-ui,sans-serif;padding:11px 18px;cursor:pointer;margin-top:8px}"+
"#fapw .alt:hover{border-color:#fff}"+
"#fapw .lk{background:none;border:0;color:#A8A8A8;font:inherit;font-size:12.5px;cursor:pointer;padding:6px 0;text-decoration:underline;text-underline-offset:3px}"+
"#fapw label{display:block;font-size:12px;color:#A8A8A8;margin:10px 0 4px}"+
"#fapw input,#fapw select{width:100%;background:#262626;border:1px solid #4A4A4A;border-radius:6px;color:#fff;font:14px Poppins,system-ui,sans-serif;padding:10px 12px}"+
"#fapw input:focus,#fapw select:focus{outline:none;border-color:#fff}"+
"#fapw .er{color:#F08A7E;font-size:12px;min-height:16px;margin-top:8px}"+
"#fapw .ft{margin-top:12px;font-size:11px;color:#7a7a7a;line-height:1.5}"+
"#fapw [hidden]{display:none!important}"+
"html.fapw-on,html.fapw-on body{overflow:hidden}";
var st,d,after=null;
function field(id,lab,ph,type,extra){return '<label for="'+id+'">'+lab+'</label><input id="'+id+'" type="'+(type||"text")+'" placeholder="'+(ph||"")+'" '+(extra||"")+'>'}
function build(){
 if(!st){st=document.createElement("style");st.textContent=css;document.head.appendChild(st)}
 d=document.createElement("div");d.id="fapw";d.setAttribute("role","dialog");d.setAttribute("aria-modal","true");d.setAttribute("aria-label","Akses "+name);
 d.innerHTML='<div class="bx"><small>Unduh hasil lengkap</small><h2></h2>'+
  '<div data-v="pay"><p class="ft" style="margin:4px 0 0;color:#D8D8D8;font-size:14px;line-height:1.6">Aplikasi tetap gratis dipakai. Untuk mengunduh hasil lengkap dan strategi, bayar sekali:</p>'+
  '<div class="pr">'+rp(price)+'<span>termasuk PPN · per aplikasi</span></div>'+
  '<div class="qr"><img alt="QRIS CV FA Indonesia" src="'+QR+'"></div>'+
  '<ol><li>Scan QRIS dengan m-banking atau e-wallet, bayar <b>'+rp(price)+'</b>.</li><li>Tekan <b>Saya sudah bayar</b> dan isi nomor referensi.</li><li>Unduhan langsung terbuka di perangkat ini.</li></ol>'+
  '<button class="go" type="button" data-to="paid">Saya sudah bayar</button><button class="lk" type="button" data-x>Nanti saja</button></div>'+
'<form data-v="paid" hidden novalidate><p class="ft" style="margin:4px 0 0;color:#D8D8D8;font-size:13px">Konfirmasi pembayaran '+rp(price)+'. Kami cocokkan dengan mutasi QRIS dan menghubungi Anda bila ada yang belum sesuai.</p>'+
  field("fp_nm","Nama","Nama lengkap")+field("fp_wa","Nomor WhatsApp","08xxxxxxxxxx","tel",'inputmode="tel"')+field("fp_us","Nama usaha atau instansi","PT, CV, toko, kampus, dll.")+
  field("fp_ref","Nomor referensi transaksi QRIS","Lihat di bukti bayar m-banking")+
  '<div class="er" aria-live="polite"></div><button class="go" type="submit">Buka unduhan</button><button class="lk" type="button" data-to="pay">Kembali ke QRIS</button></form>'+
  '<form data-v="trial" hidden novalidate><p class="ft" style="margin:4px 0 0;color:#D8D8D8;font-size:13px">Akses penuh '+TRIAL_DAYS+' hari di perangkat ini. Pembelian akses penuh segera tersedia lewat pembayaran online.</p>'+
  field("ft_nm","Nama","Nama lengkap")+field("ft_wa","Nomor WhatsApp","08xxxxxxxxxx","tel",'inputmode="tel"')+field("ft_us","Nama usaha atau instansi","PT, CV, toko, kampus, dll.")+
  '<label for="ft_bt">Bentuk usaha</label><select id="ft_bt"><option value="">Pilih</option><option>Perorangan</option><option>CV</option><option>PT</option><option>Koperasi atau Yayasan</option><option>Instansi atau Kampus</option><option>Mahasiswa</option><option>Lainnya</option></select>'+
  field("ft_kt","Kota","Kota domisili usaha")+
  '<div class="er" aria-live="polite"></div><button class="go" type="submit">Mulai coba</button><button class="lk" type="button" data-to="pay">Kembali</button></form>'+
  '<p class="ft">CV FA Indonesia. Data hanya dipakai untuk konfirmasi akses dan tindak lanjut layanan, tidak dibagikan ke pihak lain.</p></div>';
 d.querySelector("h2").textContent=name;
 document.body.appendChild(d);document.documentElement.classList.add("fapw-on");
 var prev={};try{prev=JSON.parse(ls(KD)||"{}")}catch(e){}
 ["fp_nm","ft_nm"].forEach(function(i){d.querySelector("#"+i).value=prev.nm||""});["fp_wa","ft_wa"].forEach(function(i){d.querySelector("#"+i).value=prev.wa||""});
 ["fp_us","ft_us"].forEach(function(i){d.querySelector("#"+i).value=prev.us||""});d.querySelector("#ft_kt").value=prev.kt||"";d.querySelector("#ft_bt").value=prev.bt||"";
 function show(v){[].forEach.call(d.querySelectorAll("[data-v]"),function(x){x.hidden=x.getAttribute("data-v")!==v});var f=d.querySelector('[data-v="'+v+'"] input,[data-v="'+v+'"] .go');if(f)setTimeout(function(){f.focus()},30)}
 [].forEach.call(d.querySelectorAll("[data-to]"),function(b){b.onclick=function(){show(b.getAttribute("data-to"))}});
 function val(i){return (d.querySelector("#"+i).value||"").trim()}
 function ok(form,ids){var er=form.querySelector(".er"),nm=val(ids[0]),wa=val(ids[1]).replace(/[^\d+]/g,""),us=val(ids[2]);
  if(nm.length<2){er.textContent="Isi nama Anda.";return false}
  if(!/^(\+?62|0)8\d{7,12}$/.test(wa)){er.textContent="Isi nomor WhatsApp yang aktif, contoh 081234567890.";return false}
  if(us.length<2){er.textContent="Isi nama usaha atau instansi.";return false}
  for(var k=3;k<ids.length;k++){if(!val(ids[k])){er.textContent="Lengkapi semua isian.";return false}}
  er.textContent="";return {nm:nm,wa:wa,us:us}}
 function send(kind,o,extra){ls(KD,JSON.stringify({nm:o.nm,wa:o.wa,us:o.us,kt:extra.kt||prev.kt||"",bt:extra.bt||prev.bt||""}));
  try{var p=new URLSearchParams();p.append("pt",o.us);p.append("email","");p.append("goal",(kind==="paid"?"Bayar QRIS ":"Coba 7 hari ")+name+" ("+rp(price)+")");
   p.append("unit",extra.bt||"");p.append("nama",o.nm);p.append("wa","'"+o.wa);p.append("lang","id");p.append("page",location.host+location.pathname+" (paywall "+kind+")");
   p.append("summary",kind==="paid"?"Konfirmasi bayar QRIS "+rp(price)+", referensi: "+extra.ref:"Coba "+TRIAL_DAYS+" hari. Bentuk usaha: "+(extra.bt||"-")+", kota: "+(extra.kt||"-"));
   if(!(navigator.sendBeacon&&navigator.sendBeacon(GS,p)))fetch(GS,{method:"POST",mode:"no-cors",body:p,keepalive:true})}catch(e){}
  try{window.gtag&&gtag("event",kind==="paid"?"qris_paid":"trial_start",{app:app,value:kind==="paid"?price:0,currency:"IDR"});window.gtag&&gtag("event","generate_lead",{method:"paywall_"+kind,app:app})}catch(e){}}
 d.querySelector('[data-v="paid"]').onsubmit=function(e){e.preventDefault();var o=ok(this,["fp_nm","fp_wa","fp_us","fp_ref"]);if(!o)return;send("paid",o,{ref:val("fp_ref")});ls(KP,new Date().toISOString());done()};
 d.querySelector('[data-v="trial"]').onsubmit=function(e){e.preventDefault();var o=ok(this,["ft_nm","ft_wa","ft_us","ft_bt","ft_kt"]);if(!o)return;send("trial",o,{bt:val("ft_bt"),kt:val("ft_kt")});ls(KT,String(Date.now()));done()};
 var x=d.querySelector("[data-x]");if(x)x.onclick=function(){after=null;done()};
 d.addEventListener("click",function(e){if(e.target===d){after=null;done()}});
 setTimeout(function(){d.querySelector('[data-to="paid"]').focus()},50);
}
function done(){if(d){d.remove();d=null}document.documentElement.classList.remove("fapw-on");if(after){var b=after;after=null;setTimeout(function(){b.click()},30)}}
function start(){
 document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(guard);if(!b||open_()||d)return;e.preventDefault();e.stopImmediatePropagation();after=b;build()},true);
}
if(document.body)start();else document.addEventListener("DOMContentLoaded",start);
})();
