/* FA Asisten AI (2 Nov 2026).
   Tombol "Asisten AI" hanya muncul bila /api/ai/status menjawab enabled:true
   (ANTHROPIC_API_KEY dan KV FA_AI sudah dipasang di Cloudflare Pages faindonesia-web).
   Gratis 3 pertanyaan per perangkat, setelah itu kode kredit (Paket AI 50 = Rp25.000, 300 = Rp99.000)
   lewat QRIS yang hanya muncul setelah paket dipilih (5 Nov 2026), konfirmasi masuk ke Google Sheet lead, kode diterbitkan dari /ai-admin/.
   Pakai: window.FA_AI={app:"..."} (opsional; default ikut window.FA_PAY.app) lalu <script src="/js/fa-ai.js" defer>. */
(function(){
"use strict";
var C=window.FA_AI||{},P=window.FA_PAY||{};
var app=C.app||P.app||location.pathname.replace(/\W+/g,"-")||"app";
var GS="__GS__",QR="__QR__",WA="6282245260121";
var host=location.hostname.replace(/^www\./,"");
var API=(host==="faindonesia.co.id"||C.local)?"":"https://faindonesia.co.id";
var PACKS=[{id:"ai-50",n:50,p:25000},{id:"ai-300",n:300,p:99000}];
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);if(v===null)localStorage.removeItem(k);else localStorage.setItem(k,v)}catch(e){return null}}
function dev(){var d=ls("fa_ai_dev");if(!d){d="d"+Date.now().toString(36)+Math.random().toString(36).slice(2,12);ls("fa_ai_dev",d)}return d}
var rp=function(n){return "Rp"+new Intl.NumberFormat("id-ID").format(n)};
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function md(s){return esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").split(/\n{2,}/).map(function(b){
  if(/^\s*([-*]|\d+[.)])\s/m.test(b)){var it=b.split(/\n/).filter(Boolean).map(function(l){return "<li>"+l.replace(/^\s*([-*]|\d+[.)])\s+/,"")+"</li>"}).join("");return (/^\s*\d/.test(b)?"<ol>":"<ul>")+it+(/^\s*\d/.test(b)?"</ol>":"</ul>")}
  return "<p>"+b.replace(/\n/g,"<br>")+"</p>"}).join("")}
function ga(e,p){try{window.gtag&&gtag("event",e,p||{})}catch(x){}}
function beacon(o){try{var q=Object.keys(o).map(function(k){return k+"="+encodeURIComponent(o[k]||"")}).join("&");
  if(navigator.sendBeacon)navigator.sendBeacon(GS+"?"+q);else fetch(GS+"?"+q,{mode:"no-cors"})}catch(e){}}

function context(){
  var out=[],seen={};
  document.querySelectorAll("input,select,textarea").forEach(function(el){
    if(el.closest("#faai,#fapw")||el.type==="hidden"||el.type==="password"||el.offsetParent===null)return;
    var v=el.type==="checkbox"||el.type==="radio"?(el.checked?"ya":""):(el.tagName==="SELECT"?(el.options[el.selectedIndex]||{}).text:el.value);
    if(!v)return;
    var l=(el.id&&document.querySelector('label[for="'+el.id+'"]'))||el.closest("label");
    var lt="";if(l){var lc=l.cloneNode(true);lc.querySelectorAll("select,input,textarea,option").forEach(function(x){x.remove()});lt=lc.innerText||lc.textContent||""}
    var t=(lt.trim()||el.getAttribute("aria-label")||el.placeholder||el.name||el.id||"").replace(/\s+/g," ").trim().slice(0,80);
    var k=t+"="+v;if(seen[k])return;seen[k]=1;out.push("- "+t+": "+String(v).slice(0,120));
  });
  var m=document.querySelector("main")||document.body,txt="";
  try{var cl=m.cloneNode(true);cl.querySelectorAll("script,style,nav,footer,header,#faai,#fapw,.fxs,.fxrel,.fa-cta,.eco,svg").forEach(function(x){x.remove()});txt=(cl.innerText||cl.textContent||"")}catch(e){txt=m.innerText||""}
  txt=txt.replace(/[ \t]+/g," ").replace(/\n\s*\n+/g,"\n").trim();
  return ("INPUT PENGGUNA:\n"+(out.join("\n")||"(belum ada)")+"\n\nISI DAN HASIL DI HALAMAN:\n"+txt).slice(0,6800);
}

var css="#faai-b{position:fixed;right:18px;bottom:20px;z-index:9990;display:flex;align-items:center;gap:8px;border:1px solid rgba(255,255,255,.22);border-radius:999px;background:#171717;color:#fff;font:500 13.5px Poppins,system-ui,sans-serif;padding:11px 16px 11px 13px;cursor:pointer;box-shadow:0 12px 34px -12px rgba(0,0,0,.6)}"+
"#faai-b:hover{background:#262626}#faai-b svg{width:19px;height:19px;color:#E8916B}#faai-b{border-color:rgba(217,119,87,.7)}"+
"#faai-b .t{display:flex;flex-direction:column;line-height:1.15;text-align:left}#faai-b em{font-style:normal;font-size:10.5px;letter-spacing:.04em;color:#E8916B;font-weight:600}"+
"#faai .pb{display:flex;width:fit-content;align-items:center;gap:6px;margin-top:6px;padding:3px 9px;border:1px solid rgba(217,119,87,.6);border-radius:999px;font-size:11px;font-weight:600;letter-spacing:.03em;color:#E8916B;background:rgba(217,119,87,.08)}#faai .pb i{width:7px;height:7px;border-radius:50%;background:#D97757}"+
"#faai{position:fixed;right:18px;bottom:20px;z-index:9991;width:min(400px,calc(100vw - 24px));max-height:min(640px,calc(100vh - 40px));display:none;flex-direction:column;background:#1E1E1E;color:#fff;border:1px solid #2F2F2F;border-radius:12px;box-shadow:0 30px 80px -20px rgba(0,0,0,.85);font:14px/1.55 Poppins,system-ui,-apple-system,'Segoe UI',sans-serif;text-align:left;overflow:hidden}"+
"#faai.on{display:flex}#faai *{box-sizing:border-box}"+
"#faai .hd{display:flex;align-items:center;justify-content:space-between;padding:14px 16px 10px;border-bottom:1px solid #2F2F2F}"+
"#faai .hd small{display:block;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:#A8A8A8}"+
"#faai .hd b{font-family:'EB Garamond',Georgia,serif;font-weight:400;font-size:20px}"+
"#faai .x{background:none;border:0;color:#A8A8A8;font-size:22px;line-height:1;cursor:pointer;padding:4px 6px}"+
"#faai .bd{flex:1;overflow:auto;padding:12px 16px}"+
"#faai .ft{border-top:1px solid #2F2F2F;padding:10px 12px 12px}"+
"#faai .msg{margin:0 0 12px;font-size:13.5px;color:#E6E6E6}#faai .msg p{margin:0 0 8px}#faai .msg ul,#faai .msg ol{margin:0 0 8px;padding-left:18px}"+
"#faai .q{background:#2A2A2A;border-radius:10px;padding:8px 11px;margin:0 0 10px auto;max-width:88%;width:fit-content;font-size:13px;color:#fff}"+
"#faai .hint{font-size:12.5px;color:#A8A8A8;margin:0 0 10px}"+
"#faai .chip{display:block;width:100%;text-align:left;background:transparent;border:1px solid #3A3A3A;border-radius:8px;color:#fff;font:13px Poppins,system-ui,sans-serif;padding:9px 11px;margin:0 0 7px;cursor:pointer}"+
"#faai .chip:hover{border-color:#fff}"+
"#faai .row{display:flex;gap:8px;align-items:flex-end}#faai .row textarea{flex:1;min-width:0;width:auto}"+
"#faai textarea,#faai input,#faai select{width:100%;background:#262626;border:1px solid #4A4A4A;border-radius:8px;color:#fff;font:13.5px Poppins,system-ui,sans-serif;padding:9px 11px;resize:none}"+
"#faai textarea:focus,#faai input:focus,#faai select:focus{outline:none;border-color:#fff}"+
"#faai .go{border:0;border-radius:999px;background:#fff;color:#171717;font:500 13.5px Poppins,system-ui,sans-serif;padding:10px 16px;cursor:pointer;white-space:nowrap}"+
"#faai .go:disabled{opacity:.5;cursor:default}#faai .go.w{display:block;width:100%;margin-top:10px}"+
"#faai .alt{display:block;width:100%;text-align:center;border:1px solid rgba(255,255,255,.35);border-radius:999px;background:transparent;color:#fff;font:500 13px Poppins,system-ui,sans-serif;padding:9px 14px;cursor:pointer;margin-top:8px;text-decoration:none}"+
"#faai .lk{background:none;border:0;color:#A8A8A8;font:inherit;font-size:12px;cursor:pointer;padding:4px 0;text-decoration:underline;text-underline-offset:3px}"+
"#faai .meta{display:flex;justify-content:space-between;align-items:center;font-size:11.5px;color:#A8A8A8;margin-top:7px}"+
"#faai label{display:block;font-size:12px;color:#A8A8A8;margin:9px 0 4px}"+
"#faai .er{color:#F08A7E;font-size:12px;min-height:15px;margin-top:6px}"+
"#faai .pk{display:flex;gap:8px;margin:8px 0}#faai .pk button{flex:1;background:transparent;border:1px solid #3A3A3A;border-radius:8px;color:#fff;font:13px Poppins,system-ui,sans-serif;padding:10px 6px;cursor:pointer}#faai .pk button.on{border-color:#fff;background:#262626}#faai .pk b{display:block;font-size:16px;font-weight:500}"+
"#faai .qr{background:#fff;border-radius:8px;padding:8px;margin:8px 0;text-align:center}#faai .qr img{width:100%;max-width:230px;display:block;margin:0 auto}"+
"#faai .dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#A8A8A8;margin-right:4px;animation:faaiP 1s infinite alternate}#faai .dot:nth-child(2){animation-delay:.2s}#faai .dot:nth-child(3){animation-delay:.4s}"+
"@keyframes faaiP{to{opacity:.2}}"+
"@media(max-width:760px){#faai-b{bottom:calc(78px + env(safe-area-inset-bottom));right:12px;padding:10px 14px 10px 12px}#faai{right:12px;bottom:calc(12px + env(safe-area-inset-bottom));max-height:calc(100vh - 90px)}}"+
"@media print{#faai,#faai-b{display:none!important}}";

var root,bd,ft,busy=false,lastQ="",lastA="",pack=PACKS[0];
function credit(){return ls("fa_ai_code")||""}
function meta(t){var m=root.querySelector(".meta span");if(m)m.textContent=t}
function status(){var c=credit(),r=ls("fa_ai_left");return c?("Kode "+c.slice(-4)+(r!==null?" · sisa "+r+" pertanyaan":"")):("Gratis "+(ls("fa_ai_free")===null?3:ls("fa_ai_free"))+" pertanyaan di perangkat ini")}

function build(){
  var st=document.createElement("style");st.textContent=css;document.head.appendChild(st);
  var b=document.createElement("button");b.id="faai-b";b.type="button";b.setAttribute("aria-label","Buka Asisten AI");
  b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></svg><span class="t">Asisten AI<em>Powered by Claude</em></span>';
  b.onclick=function(){root.classList.add("on");b.style.display="none";ga("ai_open",{app:app})};
  root=document.createElement("div");root.id="faai";root.setAttribute("role","dialog");root.setAttribute("aria-label","Asisten AI FA Indonesia");
  root.innerHTML='<div class="hd"><div><small>FA Indonesia</small><b>Asisten AI</b><span class="pb"><i></i>Powered by Claude · Anthropic</span></div><button class="x" type="button" aria-label="Tutup">&times;</button></div><div class="bd"></div><div class="ft"></div>';
  root.querySelector(".x").onclick=function(){root.classList.remove("on");b.style.display=""};
  document.body.appendChild(b);document.body.appendChild(root);
  bd=root.querySelector(".bd");ft=root.querySelector(".ft");home();
}
function home(){
  bd.innerHTML='<p class="hint">Asisten ini memakai Claude, model AI dari Anthropic. Asisten membaca angka dan hasil di halaman ini, lalu menjelaskannya dengan bahasa sederhana.</p>'+
   '<button class="chip" data-q="Jelaskan hasil perhitungan di halaman ini dan apa artinya untuk usaha saya.">Jelaskan hasil di halaman ini</button>'+
   '<button class="chip" data-q="Apa risiko atau hal yang perlu saya perhatikan dari angka di halaman ini?">Apa risiko dari angka ini?</button>'+
   '<button class="chip" data-q="Apa 3 langkah praktis untuk memperbaiki hasil ini?">Langkah perbaikan</button>';
  bd.querySelectorAll(".chip").forEach(function(c){c.onclick=function(){ask(c.getAttribute("data-q"))}});
  footer();
}
function footer(){
  ft.innerHTML='<div class="row"><textarea rows="2" maxlength="600" placeholder="Tulis pertanyaan Anda"></textarea><button class="go" type="button">Kirim</button></div>'+
   '<div class="meta"><span></span><button class="lk" type="button">'+(credit()?"Ganti kode":"Punya kode kredit?")+'</button></div>';
  var ta=ft.querySelector("textarea"),g=ft.querySelector(".go");
  g.onclick=function(){var v=ta.value.trim();if(v){ta.value="";ask(v)}};
  ta.onkeydown=function(e){if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();g.onclick()}};
  ft.querySelector(".lk").onclick=codeView;meta(status());
}
function ask(q){
  if(busy)return;busy=true;lastQ=q;
  if(bd.querySelector(".chip")){bd.innerHTML=""}
  var qe=document.createElement("div");qe.className="q";qe.textContent=q;bd.appendChild(qe);
  var a=document.createElement("div");a.className="msg";a.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span>';bd.appendChild(a);bd.scrollTop=bd.scrollHeight;
  ga("ai_ask",{app:app});
  fetch(API+"/api/ai/ask",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({app:app,device:dev(),code:credit(),question:q,context:context(),page:location.pathname})})
  .then(function(r){return r.json().then(function(j){j._s=r.status;return j})})
  .then(function(j){busy=false;
    if(j.answer){lastA=j.answer;a.innerHTML=md(j.answer)+'<a class="alt" target="_blank" rel="noopener" href="'+waLink()+'">Diskusikan hasil ini via WhatsApp</a>';
      if(j.credits!=null)ls("fa_ai_left",String(j.credits));if(j.free!=null)ls("fa_ai_free",String(j.free));meta(status());ga("ai_answer",{app:app})}
    else if(j.need==="buy"||j.need==="code"){a.innerHTML="<p>"+esc(j.error)+"</p>";if(j.need==="code")ls("fa_ai_code",null);if(j.free===0)ls("fa_ai_free","0");buyView(a)}
    else a.innerHTML="<p>"+esc(j.error||"Asisten belum bisa menjawab. Coba lagi.")+"</p>";
    bd.scrollTop=bd.scrollHeight})
  .catch(function(){busy=false;a.innerHTML="<p>Koneksi terputus. Coba lagi sebentar lagi.</p>"});
}
function waLink(){var t="Halo FA Indonesia, saya memakai "+document.title.split("|")[0].trim()+" ("+location.href.split("#")[0]+").\n\nPertanyaan saya: "+lastQ+"\n\nSaya ingin mendiskusikan hasilnya.";return "https://wa.me/"+WA+"?text="+encodeURIComponent(t)}
function codeView(){
  bd.innerHTML='<p class="hint">Masukkan kode paket Asisten AI yang Anda terima lewat WhatsApp.</p><label for="faai-c">Kode kredit</label><input id="faai-c" placeholder="FAI-XXXX-XXXX-XXXX" value="'+esc(credit())+'" autocomplete="off"><div class="er"></div><button class="go w" type="button">Simpan kode</button><button class="alt" type="button">Ambil paket pertanyaan</button><button class="lk" type="button">Kembali</button>';
  var i=bd.querySelector("input"),er=bd.querySelector(".er");
  bd.querySelector(".go").onclick=function(){var c=i.value.trim().toUpperCase();if(!/^FAI-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(c)){er.textContent="Format kode belum sesuai.";return}
    er.textContent="Memeriksa kode...";fetch(API+"/api/ai/credit?code="+encodeURIComponent(c)).then(function(r){return r.json()}).then(function(j){
      if(j.credits==null){er.textContent=j.error||"Kode tidak dikenal.";return}ls("fa_ai_code",c);ls("fa_ai_left",String(j.credits));home()}).catch(function(){er.textContent="Koneksi terputus."})};
  bd.querySelector(".alt").onclick=function(){bd.innerHTML="";buyView(bd)};bd.querySelector(".lk").onclick=home;
}
function buyView(box){
  /* 6 Nov 2026: paket dibayar online lewat Midtrans di /bayar/?produk=ai-50|ai-300. Kode tampil di /bayar/selesai/ setelah lunas. */
  var PK=[{id:"ai-50",n:50,amt:25000,l:"50 pertanyaan"},{id:"ai-300",n:300,amt:99000,l:"300 pertanyaan"}];
  var w=document.createElement("div");
  function pick(){w.innerHTML='<p class="hint" style="margin-top:6px">Kuota gratis di perangkat ini sudah terpakai. Lanjutkan dengan paket pertanyaan, kodenya berlaku di semua aplikasi FA.</p>'+
    PK.map(function(k,i){return '<button class="chip" type="button" data-i="'+i+'">Paket '+k.l+' · '+rp(k.amt)+'</button>'}).join("")+
    '<a class="alt" target="_blank" rel="noopener" href="'+waLink()+'">Diskusi via WhatsApp saja</a><button class="lk" type="button">Sudah punya kode</button>';
    w.querySelectorAll(".chip").forEach(function(c){c.onclick=function(){bayar(PK[+c.getAttribute("data-i")])}});w.querySelector(".lk").onclick=codeView}
  function bayar(k){ga("ai_pack_pick",{app:app,pack:k.n});
    w.innerHTML='<p class="hint" style="margin-top:6px">Paket '+k.l+' · <b style="color:#fff">'+rp(k.amt)+'</b> termasuk PPN. Bayar online lewat Midtrans, lalu kode paket tampil di halaman status pembayaran.</p>'+
     '<a class="go w" target="_blank" rel="noopener" href="/bayar/?produk='+k.id+'" style="display:block;text-align:center;text-decoration:none">Bayar Online</a>'+
     '<button class="lk" type="button">Kembali</button><button class="cd" type="button">Sudah punya kode</button>';
    w.querySelector(".lk").onclick=pick;w.querySelector(".cd").onclick=codeView}
  box.appendChild(w);pick();
}

function rp(n){return "Rp"+new Intl.NumberFormat("id-ID").format(n)}
function init(){
  fetch(API+"/api/ai/status").then(function(r){return r.ok?r.json():{}}).then(function(j){if(j&&j.enabled)build()}).catch(function(){});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
