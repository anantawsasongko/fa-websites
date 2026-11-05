/* FA Paywall v4 (5 Nov 2026, aturan Bos): aplikasi dan hasil ringkas selalu gratis, tidak ada kata "bayar" dan tidak ada harga
   yang diumumkan di muka. Pembayaran hanya muncul saat pengguna mau mengunduh laporan hasil lengkap (Excel, Word, PDF, export).
   Pakai: window.FA_PAY={app,name,what,full?,skipKey?,pay:{type:"mayar",items:[{label,url}],code?:true}
                                                      |{type:"qris",amount}} lalu <script src="/js/fa-paywall.js" defer>.
   - type mayar: tombol pilihan akses membuka halaman Mayar (tab baru, harga tampil di sana); kode akses dimasukkan di aplikasi.
   - type qris : QRIS dengan nominal muncul di langkah ini saja, lalu konfirmasi referensi -> unduhan terbuka di perangkat ini.
   Selektor tombol hasil lengkap: C.full / data-full, default DEF. Data konfirmasi ke Google Sheet lead (Apps Script). */
(function(){
"use strict";
var S=document.currentScript||{},C=window.FA_PAY||{},ds=(S.dataset||{});
var app=C.app||ds.app||location.pathname.replace(/\W+/g,"-")||"app";
var name=C.name||ds.name||document.title.split("|")[0].trim();
var what=C.what||ds.what||"laporan lengkap";
var PAY=C.pay||{type:"qris",amount:+(C.price||ds.price||25000)};
var DEF='[data-fa-full],#btnXlsx,#cp,#cpY,#fp_pr,[data-act="calkdoc"],[data-action="c-export"]';
var guard=C.full||ds.full||DEF;
var GS="__GS__",QR="__QR__";
var KP="fa_akses_"+app,KD="fa_pay_data";
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function open_(){return !!(ls(KP)||(C.skipKey&&ls(C.skipKey)))}
var rp=function(n){return "Rp"+new Intl.NumberFormat("id-ID").format(n)};
var css="#fapw{position:fixed;inset:0;z-index:9999;background:rgba(10,10,10,.84);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);display:flex;align-items:flex-start;justify-content:center;overflow:auto;padding:max(16px,env(safe-area-inset-top)) 16px 24px;font-family:Poppins,system-ui,-apple-system,'Segoe UI',sans-serif;color:#fff;text-align:left}"+
"#fapw *{box-sizing:border-box}"+
"#fapw .bx{width:100%;max-width:410px;margin:auto;background:#1E1E1E;border:1px solid #2F2F2F;border-radius:10px;padding:22px 20px 16px;box-shadow:0 30px 80px -20px rgba(0,0,0,.9);animation:fapwIn .45s cubic-bezier(.2,.7,.2,1) both}"+
"@keyframes fapwIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}"+
"#fapw small{display:block;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#A8A8A8}"+
"#fapw h2{font-family:'EB Garamond',Georgia,serif;font-weight:400;font-size:24px;line-height:1.2;margin:6px 0 2px;color:#fff}"+
"#fapw p{margin:8px 0 0;color:#D8D8D8;font-size:14px;line-height:1.6}"+
"#fapw ul.ok{margin:10px 0 0;padding:0;list-style:none;font-size:13.5px;color:#D8D8D8;line-height:1.6}#fapw ul.ok li{padding-left:22px;position:relative}#fapw ul.ok li:before{content:'✓';position:absolute;left:0;color:#7CD992}"+
"#fapw .pr{font-size:30px;font-weight:300;margin:10px 0 2px;font-variant-numeric:tabular-nums}"+
"#fapw .pr span{font-size:12.5px;color:#A8A8A8;margin-left:6px}"+
"#fapw .qr{background:#fff;border-radius:8px;padding:10px;margin:12px 0;text-align:center}"+
"#fapw .qr img{width:100%;max-width:260px;height:auto;display:block;margin:0 auto}"+
"#fapw ol{margin:0 0 10px;padding-left:18px;font-size:13px;color:#D8D8D8;line-height:1.55}"+
"#fapw ol b{color:#fff;font-weight:500}"+
"#fapw .go,#fapw a.go{display:block;width:100%;border:0;border-radius:999px;background:#fff;color:#171717;font:500 14px Poppins,system-ui,sans-serif;padding:12px 18px;cursor:pointer;margin-top:10px;text-align:center;text-decoration:none}"+
"#fapw .go:hover{background:#E8E8E8}"+
"#fapw .alt,#fapw a.alt{display:block;width:100%;border:1px solid rgba(255,255,255,.35);border-radius:999px;background:transparent;color:#fff;font:500 13.5px Poppins,system-ui,sans-serif;padding:11px 18px;cursor:pointer;margin-top:8px;text-align:center;text-decoration:none}"+
"#fapw .alt:hover{border-color:#fff}"+
"#fapw .lk{background:none;border:0;color:#A8A8A8;font:inherit;font-size:12.5px;cursor:pointer;padding:8px 0 0;text-decoration:underline;text-underline-offset:3px;display:block;width:100%;text-align:center}"+
"#fapw label{display:block;font-size:12px;color:#A8A8A8;margin:10px 0 4px}"+
"#fapw input{width:100%;background:#262626;border:1px solid #4A4A4A;border-radius:6px;color:#fff;font:14px Poppins,system-ui,sans-serif;padding:10px 12px}"+
"#fapw input:focus{outline:none;border-color:#fff}"+
"#fapw .er{color:#F08A7E;font-size:12px;min-height:16px;margin-top:8px}"+
"#fapw .ft{margin-top:12px;font-size:11px;color:#7a7a7a;line-height:1.5}"+
"#fapw [hidden]{display:none!important}"+
"html.fapw-on,html.fapw-on body{overflow:hidden}";
var st,d,after=null;
function field(id,lab,ph,type,extra){return '<label for="'+id+'">'+lab+'</label><input id="'+id+'" type="'+(type||"text")+'" placeholder="'+(ph||"")+'" '+(extra||"")+'>'}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function build(){
 if(!st){st=document.createElement("style");st.textContent=css;document.head.appendChild(st)}
 d=document.createElement("div");d.id="fapw";d.setAttribute("role","dialog");d.setAttribute("aria-modal","true");d.setAttribute("aria-label",name);
 var isM=PAY.type==="mayar";
 var intro='<div data-v="intro"><p>Hasil ringkas di layar gratis dan bisa dipakai sepuasnya. Kalau hasilnya cocok, '+esc(what)+' siap diunduh.</p>'+
  '<ul class="ok"><li>Hasil lengkap dalam file yang bisa dibuka di laptop</li><li>Siap dibawa ke auditor, bank, atau calon pembeli</li><li>'+(isM?"Kode akses tampil otomatis, berlaku sesuai pilihan":"Terbuka langsung di perangkat ini")+'</li></ul>'+
  '<button class="go" type="button" data-to="pay">Lanjutkan</button><button class="lk" type="button" data-x>Nanti saja, lanjut pakai gratis</button></div>';
 var pay;
 if(isM){
  pay='<div data-v="pay" hidden><p>Pilih masa akses. Halaman berikutnya terbuka di tab baru; setelah selesai, kode akses tampil otomatis dan tinggal ditempel di aplikasi.</p>'+
   (PAY.items||[]).map(function(it){return '<a class="go" target="_blank" rel="noopener" href="'+esc(it.url)+'" data-mayar="'+esc(it.label)+'">'+esc(it.label)+'</a>'}).join("")+
   '<button class="alt" type="button" data-code>Saya sudah punya kode akses</button><button class="lk" type="button" data-to="intro">Kembali</button></div>';
 }else{
  var amt=+PAY.amount||25000;
  pay='<div data-v="pay" hidden><div class="pr">'+rp(amt)+'<span>termasuk PPN · sekali untuk perangkat ini</span></div>'+
   '<div class="qr"><img alt="QRIS CV FA Indonesia" src="'+QR+'"></div>'+
   '<ol><li>Scan QRIS dengan m-banking atau e-wallet, isi nominal <b>'+rp(amt)+'</b>.</li><li>Tekan <b>Sudah, lanjutkan</b> dan isi nomor referensi dari bukti transaksi.</li><li>Unduhan langsung terbuka.</li></ol>'+
   '<button class="go" type="button" data-to="paid">Sudah, lanjutkan</button><button class="lk" type="button" data-to="intro">Kembali</button></div>'+
   '<form data-v="paid" hidden novalidate><p style="font-size:13px">Konfirmasi '+rp(amt)+'. Kami cocokkan dengan mutasi QRIS dan menghubungi Anda bila ada yang belum sesuai.</p>'+
   field("fp_nm","Nama","Nama lengkap")+field("fp_wa","Nomor WhatsApp","08xxxxxxxxxx","tel",'inputmode="tel"')+field("fp_us","Nama usaha atau instansi","PT, CV, toko, kampus, dll.")+
   field("fp_ref","Nomor referensi transaksi QRIS","Lihat di bukti transaksi m-banking")+
   '<div class="er" aria-live="polite"></div><button class="go" type="submit">Buka unduhan</button><button class="lk" type="button" data-to="pay">Kembali ke QRIS</button></form>';
 }
 d.innerHTML='<div class="bx"><small>'+esc(what)+'</small><h2>'+esc(name)+'</h2>'+intro+pay+'<p class="ft">CV FA Indonesia. Data hanya dipakai untuk konfirmasi akses dan tindak lanjut layanan, tidak dibagikan ke pihak lain.</p></div>';
 document.body.appendChild(d);document.documentElement.classList.add("fapw-on");
 var prev={};try{prev=JSON.parse(ls(KD)||"{}")}catch(e){}
 ["fp_nm","fp_wa","fp_us"].forEach(function(i){var el=d.querySelector("#"+i);if(el)el.value=prev[i.slice(3)]||""});
 function show(v){[].forEach.call(d.querySelectorAll("[data-v]"),function(x){x.hidden=x.getAttribute("data-v")!==v});var f=d.querySelector('[data-v="'+v+'"] input,[data-v="'+v+'"] .go');if(f)setTimeout(function(){f.focus()},30);
  try{window.gtag&&gtag("event","paywall_"+v,{app:app})}catch(e){}}
 [].forEach.call(d.querySelectorAll("[data-to]"),function(b){b.onclick=function(){show(b.getAttribute("data-to"))}});
 [].forEach.call(d.querySelectorAll("[data-mayar]"),function(a){a.addEventListener("click",function(){try{window.gtag&&gtag("event","mayar_open",{app:app,item:a.getAttribute("data-mayar")})}catch(e){}})});
 var cb=d.querySelector("[data-code]");if(cb)cb.onclick=function(){after=null;done();if(typeof C.onCode==="function")C.onCode();else{var t=document.querySelector(C.codeSel||"#lic-code");if(t){var tab=document.querySelector('[data-tab="mulai"]');if(tab)tab.click();setTimeout(function(){var i=document.querySelector(C.codeSel||"#lic-code");if(i){if(i.scrollIntoView)i.scrollIntoView({block:"center"});i.focus()}},80)}}};
 function val(i){var el=d.querySelector("#"+i);return el?(el.value||"").trim():""}
 var pf=d.querySelector('[data-v="paid"]');
 if(pf)pf.onsubmit=function(e){e.preventDefault();var er=pf.querySelector(".er"),nm=val("fp_nm"),wa=val("fp_wa").replace(/[^\d+]/g,""),us=val("fp_us"),ref=val("fp_ref");
  if(nm.length<2){er.textContent="Isi nama Anda.";return}
  if(!/^(\+?62|0)8\d{7,12}$/.test(wa)){er.textContent="Isi nomor WhatsApp yang aktif, contoh 081234567890.";return}
  if(us.length<2){er.textContent="Isi nama usaha atau instansi.";return}
  if(!ref){er.textContent="Isi nomor referensi transaksi.";return}
  er.textContent="";ls(KD,JSON.stringify({nm:nm,wa:wa,us:us}));
  try{var p=new URLSearchParams();p.append("pt",us);p.append("email","");p.append("goal","Konfirmasi QRIS "+name+" ("+rp(PAY.amount)+")");p.append("unit","");p.append("nama",nm);p.append("wa","'"+wa);p.append("lang","id");
   p.append("page",location.host+location.pathname+" (paywall qris)");p.append("summary","Konfirmasi QRIS "+rp(PAY.amount)+", referensi: "+ref);
   if(!(navigator.sendBeacon&&navigator.sendBeacon(GS,p)))fetch(GS,{method:"POST",mode:"no-cors",body:p,keepalive:true})}catch(x){}
  try{window.gtag&&gtag("event","qris_paid",{app:app,value:PAY.amount,currency:"IDR"});window.gtag&&gtag("event","generate_lead",{method:"paywall_qris",app:app})}catch(x){}
  ls(KP,new Date().toISOString());done()};
 var x=d.querySelector("[data-x]");if(x)x.onclick=function(){after=null;done()};
 d.addEventListener("click",function(e){if(e.target===d){after=null;done()}});
 setTimeout(function(){var b=d.querySelector('[data-v="intro"] .go');if(b)b.focus()},50);
}
function done(){if(d){d.remove();d=null}document.documentElement.classList.remove("fapw-on");if(after){var b=after;after=null;setTimeout(function(){b.click()},30)}}
function start(){
 document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(guard);if(!b||open_()||d)return;e.preventDefault();e.stopImmediatePropagation();after=b;build()},true);
}
if(document.body)start();else document.addEventListener("DOMContentLoaded",start);
window.FAPaywall={open:function(){if(!d)build()},unlocked:open_};
})();
