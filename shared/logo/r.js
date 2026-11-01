const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();
for(const n of ['ca-lockup-dark','us-lockup-dark','ca-lockup-light','us-lockup-light']){const sv=fs.readFileSync(n+'.svg','utf8');const w=+sv.match(/width="(\d+)"/)[1];
const p=await b.newPage({viewport:{width:w*3,height:74*3}});await p.setContent(`<html><body style="margin:0;background:transparent">${sv.replace(/width="\d+" height="74"/,`width="${w*3}" height="${74*3}"`)}</body></html>`);
await p.screenshot({path:n+'.png',omitBackground:true});await p.close();}await b.close()})();
