/* Helper bersama FA Venus Advanced Hospital Toolkit (7 Nov 2026). Disisipkan inline ke tiap halaman. */
var WA="6282245260121",$=function(i){return document.getElementById(i)};
function pn(v){v=(v==null?"":String(v)).trim().replace(/\s/g,"").replace(/\./g,"").replace(",",".");if(v==="")return 0;v=parseFloat(v);return isNaN(v)?0:v}
function f0(v){return isFinite(v)?Math.round(v).toLocaleString("id-ID"):"-"}
function f1(v){return isFinite(v)?(Math.round(v*10)/10).toLocaleString("id-ID",{minimumFractionDigits:1,maximumFractionDigits:1}):"-"}
function pc(v){return isFinite(v)?f1(v*100)+"%":"-"}
function jt(v){if(!isFinite(v))return"-";var a=Math.abs(v),s=v<0?"-":"";return a>=1000?s+"Rp"+(a/1000).toLocaleString("id-ID",{minimumFractionDigits:a>=10000?1:2,maximumFractionDigits:a>=10000?1:2})+" M":s+"Rp"+f0(a)+" jt"}
function rp(v){return isFinite(v)?(v<0?"-":"")+"Rp"+f0(Math.abs(v)):"-"}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function ga(e,p){try{if(window.gtag)gtag("event",e,p||{})}catch(x){}}
function tag(c,t){return '<span class="ra-tag '+c+'">'+t+'</span>'}
function today(){return new Date().toLocaleDateString("id-ID",{day:"numeric",month:"long",year:"numeric"})}
function printRep(html){var rp=$("ra_rep");if(rp.parentNode!==document.body)document.body.appendChild(rp);rp.innerHTML=html;setTimeout(function(){window.print()},400)}
function waHref(t){return "https://wa.me/"+WA+"?text="+encodeURIComponent(t)}
