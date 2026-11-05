(function(){var D=null,P=null;function q(s,r){return (r||document).querySelector(s)}function all(s,r){return [].slice.call((r||document).querySelectorAll(s))}
var LAB={kap:"KAP",ap:"Akuntan Publik",kja:"KJA",ab:"Akuntan Berpraktik",kjpp:"KJPP",penilai:"Penilai Publik",kp:"Konsultan Pajak"};
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function cls(s){s=(s||"").toLowerCase();return s==="aktif"?"ok":s.indexOf("aktif")===0?"warn":"off"}
function txt(s){return{"Non-Aktif(permohonan)":"Non-aktif (tutup)","Non-Aktif(tidak berlaku)":"Non-aktif","Non-Aktif(sanksi)":"Dicabut"}[s]||s||"-"}
function li(r,k){var sub=[];if(r.no)sub.push(esc(r.no));if(r.o)sub.push(esc(r.o));if(r.k)sub.push(esc(r.k));
 return '<li><span class="pk-n">'+esc(r.n)+'</span><span class="pk-m">'+LAB[k]+(sub.length?" · "+sub.join(" · "):"")+'</span><span class="pk-s '+cls(r.s)+'">'+esc(txt(r.s))+'</span>'+(r.u?'<a href="https://find-profkeu.kemenkeu.go.id'+esc(r.u)+'" target="_blank" rel="noopener nofollow">Registri Kemenkeu ↗</a>':"")+'</li>'}
function load(){if(P)return P;P=fetch("/data/izin.json").then(function(r){return r.json()}).then(function(j){D=j;return j});return P}
function norm(s){return String(s||"").toLowerCase().replace(/[^a-z0-9]+/g," ").trim()}
function search(box){var inp=q("input",box),sel=q("select",box),out=q(".pk-r",box),v=norm(inp.value),t=sel.value;
 if(v.length<2){out.hidden=true;out.innerHTML="";var cur=q(".pk-tabs button[aria-selected=true]",box);all(".pk-city",box).forEach(function(e){var t=e.getAttribute("data-t");e.hidden=!!(t&&cur&&t!==cur.getAttribute("data-t"))});return}
 out.hidden=false;out.innerHTML='<p class="pk-h">Mencari…</p>';
 load().then(function(d){var res=[],keys=t?[t]:["kap","kja","kjpp","ap","ab","kp","penilai"];
  keys.forEach(function(k){(d[k]||[]).forEach(function(r){var h=norm(r.n+" "+(r.no||"")+" "+(r.o||"")+" "+(r.k||""));if(h.indexOf(v)>=0)res.push([k,r])})});
  res.sort(function(a,b){var x=cls(a[1].s)==="ok"?0:1,y=cls(b[1].s)==="ok"?0:1;return x-y||String(a[1].n).localeCompare(String(b[1].n))});
  var n=res.length;all(".pk-city",box).forEach(function(e){e.hidden=true});
  out.innerHTML='<p class="pk-h">'+(n?n+" hasil"+(n>60?", ditampilkan 60 pertama":""):"Tidak ada yang cocok")+' untuk "'+esc(inp.value)+'" di registri PPPK (data '+esc(d.updated||"")+')</p><ul class="pk-l">'+res.slice(0,60).map(function(x){return li(x[1],x[0])}).join("")+"</ul>"}).catch(function(){out.innerHTML='<p class="pk-h">Data belum bisa dimuat. Coba lagi sebentar.</p>'})}
all(".pk").forEach(function(box){var inp=q("input",box),sel=q("select",box);if(!inp)return;var t;
 inp.addEventListener("focus",function(){load()});inp.addEventListener("input",function(){clearTimeout(t);t=setTimeout(function(){search(box)},180)});
 if(sel)sel.addEventListener("change",function(){search(box)});
 all(".pk-tabs button",box).forEach(function(b){b.addEventListener("click",function(){all(".pk-tabs button",box).forEach(function(x){x.setAttribute("aria-selected",x===b)});all(".pk-city",box).forEach(function(e){e.hidden=e.getAttribute("data-t")!==b.getAttribute("data-t")})})})});
})();