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
function cv(v){return typeof v=="number"?v:pn(v)}
function xlMsg(t,ok){var m=$("ra_xmsg");if(m){m.textContent=t;m.className=ok?"ok":"bad"}}
function xlLib(cb){if(window.XLSX)return cb();xlMsg("Memuat modul Excel...",true);var s=document.createElement("script");s.src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js";s.onload=function(){xlMsg("",true);cb()};s.onerror=function(){xlMsg("Modul Excel gagal dimuat. Periksa koneksi lalu coba lagi.",false)};document.head.appendChild(s)}
function xlDown(fn,sheets){xlLib(function(){var wb=XLSX.utils.book_new();sheets.forEach(function(s){var ws=XLSX.utils.aoa_to_sheet(s[1]);ws["!cols"]=s[1][0].map(function(_,i){return {wch:i==0?42:20}});XLSX.utils.book_append_sheet(wb,ws,s[0])});XLSX.writeFile(wb,fn);xlMsg("Template terunduh. Isi di Excel, simpan, lalu klik Upload Excel.",true)})}
function xlUp(cb){var i=document.createElement("input");i.type="file";i.accept=".xlsx,.xls,.xlsm,.csv";i.onchange=function(){var f=i.files[0];if(!f)return;xlLib(function(){var r=new FileReader();r.onload=function(e){var o={};try{var wb=XLSX.read(new Uint8Array(e.target.result),{type:"array"});wb.SheetNames.forEach(function(n){o[n.toLowerCase().trim()]=XLSX.utils.sheet_to_json(wb.Sheets[n],{header:1,blankrows:false,defval:""})})}catch(x){return xlMsg("File tidak terbaca. Pakai file dari tombol Download Template Excel.",false)}cb(o)};r.readAsArrayBuffer(f)})};i.click()}
function rowsOf(t){return (t||[]).slice(1).filter(function(r){return String(r[0]).trim()!==""})}
function xlWire(fname,toX,fromX,ev){$("xl_dl").onclick=function(){xlDown(fname,toX());ga(ev+"_template")};$("xl_up").onclick=function(){xlUp(function(o){var e;try{e=fromX(o)}catch(x){e="Isi file tidak sesuai template."}if(e)return xlMsg(e+" Pakai file dari tombol Download Template Excel.",false);xlMsg("Data Excel terbaca. Hasil sudah diperbarui.",true);ga(ev+"_upload");var r=document.querySelector(".ra-res")||$("rvr");if(r)r.scrollIntoView({behavior:"smooth",block:"start"})})}}
function kvSheet(title,ids,labels){return [title,[["Data","Nilai"]].concat(ids.map(function(id,i){return [labels[i],cv($(id).value)]}))]}
function kvLoad(t,ids){var r=rowsOf(t);if(r.length<ids.length)return false;ids.forEach(function(id,i){var v=r[i][1];if(v!==""&&v!=null)$(id).value=String(cv(v)).replace(".",",")});return true}
