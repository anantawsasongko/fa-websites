/* Cek layout sebelum push (wajib, 5 Nov 2026): cari elemen konten di <main> yang nempel tepi kiri (di luar .wrap)
   atau bikin scroll horizontal. Pakai: python3 -m http.server 8801 -d out/faindonesia & python3 -m http.server 8802 -d out/cariakuntan &
   lalu node tools/layout_check.js [jumlah_sampel=200]. Harus keluar "LAYOUT OK". */
const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const N=+process.argv[2]||200;
function pages(site){const out=[];(function walk(d){for(const f of fs.readdirSync(d)){const p=path.join(d,f);const s=fs.statSync(p);if(s.isDirectory())walk(p);else if(f==='index.html')out.push('/'+path.relative(`out/${site}`,d).split(path.sep).join('/')+(d===`out/${site}`?'':'/'))}})(`out/${site}`);
 const fixed=out.filter(u=>u.split('/').length<=3);const rest=out.filter(u=>u.split('/').length>3).sort(()=>Math.random()-.5).slice(0,N);return [...new Set(fixed.slice(0,150).concat(rest))].map(u=>u.replace('//','/'))}
(async()=>{const b=await chromium.launch();const bad=[];
for(const [site,port] of [['faindonesia',8801],['cariakuntan',8802]])for(const w of [1280,375]){const ctx=await b.newContext({viewport:{width:w,height:900}});
 for(const u of pages(site)){const p=await ctx.newPage();try{await p.goto(`http://localhost:${port}${u}`,{waitUntil:'domcontentloaded',timeout:15000});
  const r=await p.evaluate(w=>{const o=[];document.querySelectorAll('main p,main h2,main h3,main ul,main details,main a.btn,main form').forEach(e=>{if(getComputedStyle(e).display==='none'||e.closest('header,footer,nav'))return;const r=e.getBoundingClientRect();if(r.width<40||r.height<5||!(e.innerText||'').trim())return;if(r.left<(w>600?12:6))o.push(e.tagName+': '+e.innerText.trim().slice(0,50))});return [document.documentElement.scrollWidth,o]},w);
  if(r[1].length)bad.push(`${site}${u} @${w} nempel kiri: ${r[1][0]}`);if(r[0]>w+2)bad.push(`${site}${u} @${w} scroll horizontal ${r[0]}px`)}catch(e){}await p.close()}await ctx.close()}
console.log(bad.length?bad.slice(0,40).join('\n')+`\nLAYOUT GAGAL: ${bad.length}`:'LAYOUT OK');await b.close();process.exit(bad.length?1:0)})();
