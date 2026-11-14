(function(){"use strict";
const $=s=>document.querySelector(s);const $$=s=>[...document.querySelectorAll(s)];
const nf=new Intl.NumberFormat("id-ID",{maximumFractionDigits:0});
const nf2=new Intl.NumberFormat("id-ID",{maximumFractionDigits:2});
const rp=n=>"Rp"+(n<0?"("+nf.format(Math.round(-n))+")":nf.format(Math.round(n||0)));
const num=v=>{if(typeof v==="number")return v;let s=String(v??"").trim();if(!s)return 0;const neg=/^\(.*\)$/.test(s)||/^-/.test(s);s=s.replace(/[()\s-]|Rp/gi,"").replace(/[^0-9.,]/g,"");
 if(/,\d{1,2}$/.test(s))s=s.replace(/\./g,"").replace(",",".");else if(/^\d+\.\d{1,2}$/.test(s)){}else s=s.replace(/[.,]/g,"");const x=parseFloat(s)||0;return neg?-x:x};
const val=id=>num(document.getElementById(id).value);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function toast(m){const t=$("#toast");if(!t)return;t.textContent=m;t.hidden=false;clearTimeout(toast.t);toast.t=setTimeout(()=>t.hidden=true,2600)}
function money(el){el.addEventListener("blur",()=>{const x=num(el.value);if(el.value.trim()!=="")el.value=nf.format(x)})}
function kpi(label,value,sub){return `<div class="kpi"><small>${label}</small><b>${value}</b>${sub?`<span>${sub}</span>`:""}</div>`}
const JENIS=["Barang berwujud","Jasa","Bunga","Harta tidak berwujud","Lainnya"];
const BATAS=[20e9,5e9,5e9,5e9,5e9];
const FLD=["t_brg","t_jasa","t_bunga","t_htb","t_lain"];
const HUB=["Pemegang saham","Induk","Anak perusahaan","Sepengendali","Lainnya"];
const MET=["Harga pembanding tak terkendali (CUP)","Harga jual kembali (RPM)","Biaya-plus (CPM)","Pemisahan laba (PSM)","Margin bersih transaksional (TNMM)","Lainnya"];
let rows=[{pihak:"",negara:"",hub:HUB[0],jenis:1,nilai:0,metode:4}];
function addM(d,k){const y=d.getFullYear(),m=d.getMonth()+k,last=new Date(y,m+1,0).getDate();return new Date(y,m,Math.min(d.getDate(),last))}
const tgl=d=>d.toLocaleDateString("id-ID",{day:"numeric",month:"long",year:"numeric"});
function calc1(){
 const ada=$("#ada").value==="ya",bruto=val("bruto"),rendah=$("#rendah").value==="ya";
 const why=[];
 if(bruto>50e9)why.push("Peredaran bruto "+rp(bruto)+" melebihi Rp50 miliar.");
 FLD.forEach((f,i)=>{const v=val(f);if(v>BATAS[i])why.push("Transaksi afiliasi "+JENIS[i].toLowerCase()+" "+rp(v)+" melebihi "+rp(BATAS[i])+".")});
 if(rendah)why.push("Ada lawan transaksi di negara bertarif PPh lebih rendah dari tarif Pasal 17 UU PPh.");
 const wajib=ada&&why.length>0;
 const d=new Date($("#akhir").value||($("#th").value+"-12-31"));
 const ok=!isNaN(d);
 const induk=$("#induk").value==="ya",kons=val("konsol"),cb=induk&&kons>=11e12;
 let sub=!ada?"Tanpa transaksi afiliasi tahun berjalan, kewajiban tidak timbul.":wajib?why.length+" kriteria terpenuhi.":"Tidak ada kriteria yang terpenuhi.";
 $("#kpi").innerHTML=kpi("Master File dan Local File",`<span class="${wajib?"tp-no":"tp-ok"}">${wajib?"Wajib":"Tidak wajib"}</span>`,sub)
  +kpi("Tersedia paling lambat",wajib&&ok?tgl(addM(d,4)):"-","4 bulan setelah akhir tahun pajak")
  +kpi("Jika diminta DJP","1 bulan","batas penyampaian sejak permintaan")
  +kpi("CbCR",cb?`<span class="tp-no">Wajib</span>`:"Tidak wajib",cb&&ok?"tersedia paling lambat "+tgl(addM(d,12)):"hanya induk dengan konsolidasi minimal Rp11 triliun");
 $("#why").innerHTML=(wajib?why:ada?["Tidak wajib bukan berarti bebas: transaksi afiliasi tetap harus memenuhi prinsip kewajaran dan kelaziman usaha."]:[]).map(x=>`<li>${esc(x)}</li>`).join("");
}
function renderRows(){
 $("#tx tbody").innerHTML=rows.map((r,i)=>`<tr>
 <td><input data-i="${i}" data-k="pihak" value="${esc(r.pihak)}" aria-label="Pihak afiliasi"/></td>
 <td><input data-i="${i}" data-k="negara" value="${esc(r.negara)}" aria-label="Negara"/></td>
 <td><select data-i="${i}" data-k="hub" aria-label="Hubungan">${HUB.map(h=>`<option${h===r.hub?" selected":""}>${h}</option>`).join("")}</select></td>
 <td><select data-i="${i}" data-k="jenis" aria-label="Jenis">${JENIS.map((h,j)=>`<option value="${j}"${j===+r.jenis?" selected":""}>${h}</option>`).join("")}</select></td>
 <td class="num"><input data-i="${i}" data-k="nilai" value="${r.nilai?nf.format(r.nilai):""}" aria-label="Nilai"/></td>
 <td><select data-i="${i}" data-k="metode" aria-label="Metode">${MET.map((h,j)=>`<option value="${j}"${j===+r.metode?" selected":""}>${h}</option>`).join("")}</select></td>
 <td><button class="btn small" type="button" data-del="${i}" aria-label="Hapus baris">Hapus</button></td></tr>`).join("");
 calc2();
}
function totals(){const t=[0,0,0,0,0];rows.forEach(r=>{t[+r.jenis]+=num(r.nilai)});return t}
function calc2(){
 const t=totals();
 $("#sumx tbody").innerHTML=JENIS.map((j,i)=>`<tr><td>${j}</td><td class="num">${rp(t[i])}</td><td class="num">${rp(BATAS[i])}</td><td>${t[i]>BATAS[i]?'<span class="tp-no">Melebihi batas</span>':'<span class="tp-ok">Di bawah batas</span>'}</td></tr>`).join("");
 draft();
}
function q(a,p){const n=a.length;if(!n)return NaN;const pos=(n-1)*p,lo=Math.floor(pos),hi=Math.ceil(pos);return a[lo]+(a[hi]-a[lo])*(pos-lo)}
let IQR=null;
function calc3(){
 const m=parseFloat(String($("#mt").value).replace(",","."));
 const a=$("#comps").value.split(/[\n;]+/).map(x=>parseFloat(x.replace(/\s/g,"").replace("%","").replace(",","."))).filter(x=>isFinite(x)).sort((x,y)=>x-y);
 if(a.length<2||!isFinite(m)){IQR=null;$("#kpi3").innerHTML=kpi("Rentang interkuartil","-","Isi minimal 2 pembanding dan margin yang diuji");draft();return}
 const q1=q(a,.25),md=q(a,.5),q3=q(a,.75),inr=m>=q1&&m<=q3,base=val("mbase");
 const adj=inr?0:(md-m)/100*base;
 IQR={n:a.length,q1,md,q3,m,inr,adj,base};
 const f=x=>nf2.format(Math.round(x*100)/100)+"%";
 $("#kpi3").innerHTML=kpi("Kuartil 1",f(q1),a.length+" pembanding")+kpi("Median",f(md))+kpi("Kuartil 3",f(q3))
  +kpi("Margin diuji",f(m),`<span class="${inr?"tp-ok":"tp-no"}">${inr?"Dalam rentang wajar":"Di luar rentang"}</span>`)
  +(inr?"":kpi("Penyesuaian ke median",rp(adj),base?(adj>0?"menambah laba":"mengurangi laba"):"isi dasar penyesuaian"))
  +(a.length<4?kpi("Catatan","Pembanding sedikit","disarankan lebih banyak"):"");
 draft();
}
function ph(v,l){v=String(v||"").trim();return v?esc(v).replace(/\n/g,"<br>"):`<mark>[${esc(l)}]</mark>`}
function draftHTML(){
 const t=totals(),th=$("#th").value||"";
 const f=x=>nf2.format(Math.round(x*100)/100)+"%";
 const trs=rows.map(r=>`<tr><td>${ph(r.pihak,"pihak")}</td><td>${ph(r.negara,"negara")}</td><td>${esc(r.hub)}</td><td>${JENIS[+r.jenis]}</td><td style="text-align:right">${rp(num(r.nilai))}</td></tr>`).join("");
 const mets=[...new Set(rows.map(r=>MET[+r.metode]))].join("; ");
 let h=`<h4>Dokumen Lokal (Local File) Tahun Pajak ${esc(th)}</h4><p>${ph($("#nm").value,"nama wajib pajak")}</p>`;
 h+=`<h4>A. Informasi Wajib Pajak</h4><p><b>Kegiatan usaha, strategi, dan pesaing.</b><br>${ph($("#usaha").value,"uraikan kegiatan usaha, strategi, dan pesaing")}</p><p><b>Struktur grup dan posisi wajib pajak.</b><br>${ph($("#grup").value,"uraikan struktur grup dan posisi wajib pajak")}</p>`;
 h+=`<h4>B. Transaksi Afiliasi</h4><table><thead><tr><th>Pihak afiliasi</th><th>Negara</th><th>Hubungan</th><th>Jenis</th><th>Nilai</th></tr></thead><tbody>${trs}</tbody></table><p>Total per jenis: ${JENIS.map((j,i)=>t[i]?`${j} ${rp(t[i])}`:"").filter(Boolean).join("; ")||"-"}.</p>`;
 h+=`<h4>C. Analisis Kesebandingan</h4><p><b>Fungsi.</b><br>${ph($("#fungsi").value,"uraikan fungsi yang dijalankan")}</p><p><b>Aset.</b><br>${ph($("#aset").value,"uraikan aset yang digunakan")}</p><p><b>Risiko.</b><br>${ph($("#risiko").value,"uraikan risiko yang ditanggung")}</p>`;
 h+=`<h4>D. Pemilihan Metode</h4><p>Metode yang dipilih: ${esc(mets)}.</p><p>${ph($("#alasan").value,"jelaskan alasan pemilihan metode")}</p>`;
 h+=`<h4>E. Penerapan Metode dan Hasil Uji Kewajaran</h4>`;
 if(IQR){h+=`<p>Dari ${IQR.n} pembanding independen, rentang interkuartil berada pada ${f(IQR.q1)} sampai ${f(IQR.q3)} dengan median ${f(IQR.md)}. Margin pihak yang diuji sebesar ${f(IQR.m)} ${IQR.inr?"berada di dalam rentang tersebut":"berada di luar rentang tersebut"}.`+(IQR.inr?"":` Penyesuaian ke median sebesar ${rp(IQR.adj)}${IQR.base?"":" (dasar penyesuaian belum diisi)"}.`)+`</p>`}else{h+=`<p><mark>[isi hasil uji kewajaran: margin pembanding dan pihak yang diuji]</mark></p>`}
 h+=`<h4>F. Kesimpulan</h4><p>Berdasarkan analisis di atas, transaksi afiliasi wajib pajak ${IQR?(IQR.inr?"berada dalam rentang kewajaran":"berada di luar rentang kewajaran dan disesuaikan"):"<mark>[memenuhi / belum memenuhi]</mark>"} sesuai prinsip kewajaran dan kelaziman usaha.</p>`;
 h+=`<h4>G. Lampiran</h4><p>Perjanjian dengan pihak afiliasi; faktur dan bukti transaksi; laporan keuangan; daftar pembanding beserta sumber data.</p>`;
 return h;
}
function draft(){const el=$("#draft");if(el)el.innerHTML=draftHTML()}
function docWord(){
 const css="body{font-family:Calibri,Arial,sans-serif;font-size:11pt;line-height:1.5}h4{font-size:13pt;margin:16pt 0 4pt}table{border-collapse:collapse;width:100%}td,th{border:1px solid #999;padding:4pt 6pt;text-align:left;font-size:10pt}mark{background:#ffff66}";
 const html='<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><title>Local File</title><style>'+css+'</style></head><body>'+draftHTML()+'</body></html>';
 const b=new Blob(["﻿",html],{type:"application/msword"});const a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="Draf-Local-File-"+($("#th").value||"TP")+".doc";document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},500);
}
function jenisFrom(s){s=String(s).toLowerCase();if(/barang|berwujud/.test(s)&&!/tidak|tak/.test(s))return 0;if(/jasa/.test(s))return 1;if(/bunga|pinjam/.test(s))return 2;if(/tak berwujud|tidak berwujud|htb|royalti|intangible/.test(s))return 3;return 4}
function metFrom(s){s=String(s).toLowerCase();if(/cup|pembanding tak/.test(s))return 0;if(/rpm|jual kembali/.test(s))return 1;if(/cpm|biaya/.test(s))return 2;if(/psm|pemisahan|bagi laba/.test(s))return 3;if(/tnmm|margin/.test(s))return 4;return 5}
document.addEventListener("DOMContentLoaded",()=>{
 $$("input.m").forEach(money);
 $$("#kpi,.fields").length;
 $$(".sec input,.sec select").forEach(e=>{if(e.closest("#tx"))return;e.addEventListener("input",()=>{calc1();calc3();draft()});e.addEventListener("change",()=>{calc1();calc3();draft()})});
 $$(".sec textarea").forEach(e=>e.addEventListener("input",()=>{if(e.id==="comps"||e.id==="pasteTa"){if(e.id==="comps")calc3()}else draft()}));
 const tb=$("#tx tbody");
 tb.addEventListener("input",e=>{const t=e.target,i=+t.dataset.i,k=t.dataset.k;if(isNaN(i))return;rows[i][k]=(k==="nilai")?num(t.value):(k==="jenis"||k==="metode")?+t.value:t.value;calc2()});
 tb.addEventListener("blur",e=>{const t=e.target;if(t.dataset&&t.dataset.k==="nilai"&&t.value.trim()!=="")t.value=nf.format(num(t.value))},true);
 tb.addEventListener("click",e=>{const b=e.target.closest("[data-del]");if(!b)return;rows.splice(+b.dataset.del,1);if(!rows.length)rows=[{pihak:"",negara:"",hub:HUB[0],jenis:1,nilai:0,metode:4}];renderRows()});
 $("#addRow").onclick=()=>{rows.push({pihak:"",negara:"",hub:HUB[0],jenis:1,nilai:0,metode:4});renderRows()};
 $("#togglePaste").onclick=()=>{const b=$("#pasteBox");b.hidden=!b.hidden};
 $("#doPaste").onclick=()=>{const L=$("#pasteTa").value.split(/\r?\n/).map(x=>x.split("\t")).filter(c=>c.join("").trim());if(!L.length)return toast("Tidak ada baris untuk dimasukkan");
  const add=L.map(c=>({pihak:(c[0]||"").trim(),negara:(c[1]||"").trim(),hub:HUB.find(h=>h.toLowerCase()===String(c[2]||"").trim().toLowerCase())||HUB[4],jenis:jenisFrom(c[3]||""),nilai:num(c[4]||0),metode:metFrom(c[5]||"")}));
  if(rows.length===1&&!rows[0].pihak&&!rows[0].nilai)rows=[];rows=rows.concat(add);$("#pasteTa").value="";$("#pasteBox").hidden=true;renderRows();toast(add.length+" baris masuk")};
 $("#useSum").onclick=()=>{const t=totals();FLD.forEach((f,i)=>{$("#"+f).value=nf.format(t[i])});calc1();toast("Total masuk ke langkah 1")};
 $("#dl").onclick=docWord;
 $("#cpd").onclick=()=>{navigator.clipboard.writeText($("#draft").innerText).then(()=>toast("Draf disalin"),()=>toast("Gagal menyalin"))};
 renderRows();calc1();calc3();draft();
});
})();
