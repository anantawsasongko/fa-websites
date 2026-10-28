const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();
for(const n of ['ca','us'])for(const s of [512,192,180,48,32]){const p=await b.newPage({viewport:{width:s,height:s}});
await p.setContent(`<html><body style="margin:0;background:transparent">${fs.readFileSync(n+'.svg','utf8').replace('<svg ',`<svg width="${s}" height="${s}" `)}</body></html>`);
await p.screenshot({path:`${n}-${s}.png`,omitBackground:true});await p.close();}await b.close()})();
