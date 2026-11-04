# -*- coding: utf-8 -*-
"""Kalkulator Valuasi Rumah Sakit (4 Nov 2026), FA Venus, gratis (tanpa paywall: alat lead-gen sell side RS).
Dua pendekatan: EBITDA x multiple (5 sampai 8x, disesuaikan kelas, akreditasi, BPJS, BOR, gedung) dan nilai aset
(appraisal KJPP/bank atau benchmark per TT). Aset jadi batas bawah, dikurangi utang bank, dikali porsi saham dijual.
Tombol WA lewat lead.js (form Nama Usaha, Bentuk Usaha, Kota + tag ref otomatis).
Gaya mengikuti Peta Pendanaan (fa_pendanaan_20261103.py). Idempoten: halaman ditimpa, sisipan memakai marker."""
import os, re, json
R = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(R, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
SITE = "https://faindonesia.co.id"
SLUG = "kalkulator-valuasi-rumah-sakit"
WA = "6282245260121"
TPL = open(os.path.join(B, "komite-audit-komisaris-independen", "index.html"), encoding="utf-8").read()

CSS = r"""<style>
.rv-hero{padding-top:8px}.rv-hero h1{margin:.15em 0 .35em;font-size:clamp(30px,4.4vw,54px);line-height:1.08;max-width:15em}
.rv-lede{font-size:clamp(16px,1.6vw,19px);color:var(--muted);max-width:38em;margin:0 0 24px}
.rv-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:18px;align-items:start}
.rv-card{border:1px solid var(--line);background:var(--surface);border-radius:18px;padding:24px}
.rv-h{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);margin:0 0 12px;font-weight:500}
.rv-blk{padding:16px 0;border-top:1px solid var(--line)}.rv-blk:first-of-type{border-top:0;padding-top:0}
.rv-f{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 14px}
.rv-f label{display:flex;flex-direction:column;gap:6px;font-size:14px;font-weight:600;line-height:1.35}
.rv-f label small{font-weight:400;color:var(--muted);font-size:12.5px}
.rv-f input,.rv-f select{all:unset;box-sizing:border-box;width:100%;border:1px solid #3a3a3a;background:var(--paper);color:#fff;border-radius:10px;padding:11px 13px;font-size:15px;font-family:var(--body);font-weight:400;transition:border-color .2s}
.rv-f select{background-image:linear-gradient(45deg,transparent 50%,#aaa 50%),linear-gradient(135deg,#aaa 50%,transparent 50%);background-position:calc(100% - 18px) 50%,calc(100% - 13px) 50%;background-size:5px 5px;background-repeat:no-repeat;padding-right:34px;cursor:pointer}
.rv-f select option{background:#1e1e1e;color:#fff}
.rv-f input:focus,.rv-f select:focus{border-color:#fff}
.rv-f input::placeholder{color:#6f6f6f}
.rv-u{position:relative}.rv-u input{padding-right:58px}.rv-u:after{content:attr(data-u);position:absolute;right:13px;top:50%;transform:translateY(-50%);font-size:12.5px;color:var(--muted);pointer-events:none}
.rv-note{font-size:13px;color:var(--muted);margin:0 0 14px;line-height:1.5}
#rvr{position:sticky;top:84px;border:1px solid var(--line);border-radius:18px;padding:24px;background:linear-gradient(160deg,#222,#161616)}
.rv-k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.rv-big{font-size:clamp(28px,3.4vw,40px);font-weight:500;line-height:1.1;margin:6px 0 16px;font-variant-numeric:tabular-nums}
.rv-row{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-top:1px solid var(--line);font-size:14.5px}
.rv-row span{color:var(--muted)}.rv-row b{font-weight:500;text-align:right;font-variant-numeric:tabular-nums}
.rv-stk{border:1px solid #fff;border-radius:14px;padding:16px;margin:16px 0 4px}
.rv-stk .rv-big{margin:4px 0 0;font-size:clamp(24px,2.8vw,32px)}
.rv-fl{list-style:none;margin:14px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}
.rv-fl li{font-size:13.5px;line-height:1.5;padding:10px 12px;border-radius:10px;background:#1b1b1b;border:1px solid var(--line);display:flex;gap:10px}
.rv-fl li i{font-style:normal;flex:none;width:18px;height:18px;border-radius:50%;display:grid;place-items:center;font-size:11px;margin-top:1px}
.rv-fl li.up i{background:#fff;color:#111}.rv-fl li.dn i{border:1px solid #F08A82;color:#F08A82}.rv-fl li.in i{border:1px solid #888;color:#bbb}
.rv-act{display:flex;flex-direction:column;gap:10px;margin-top:18px}.rv-act .btn{justify-content:center}
.rv-sm{font-size:12px;color:var(--muted);line-height:1.5;margin:12px 0 0}
.rv-safe{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.rv-safe span{font-size:12.5px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:5px 11px}
.rv-sec{margin-top:60px}.rv-sec>h2{font-size:clamp(22px,2.6vw,32px);margin:0 0 18px;line-height:1.2}
.rv-3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.rv-3 div{border:1px solid var(--line);background:#1b1b1b;border-radius:14px;padding:18px}
.rv-3 em{font-style:normal;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
.rv-3 b{display:block;font-size:17px;margin:6px 0}.rv-3 p{margin:0;font-size:14px;color:var(--muted);line-height:1.55}
.rv-tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px}
.rv-t{width:100%;border-collapse:collapse;font-size:14.5px;min-width:560px}
.rv-t th,.rv-t td{padding:12px 16px;text-align:left;border-top:1px solid var(--line);vertical-align:top;line-height:1.5}
.rv-t th{border-top:0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:500;background:#1b1b1b}
.rv-t td:nth-child(3){color:var(--muted)}
.rv-t .pu{white-space:nowrap}.rv-t .pd{white-space:nowrap;color:#F08A82}
.rv-cta{border:1px solid #fff;border-radius:18px;padding:26px;display:flex;flex-wrap:wrap;gap:16px 24px;align-items:center;justify-content:space-between;background:linear-gradient(160deg,#222,#161616)}
.rv-cta h2{margin:0 0 6px;font-size:clamp(22px,2.4vw,28px)}.rv-cta p{margin:0;color:var(--muted);max-width:40em}
.rv-cta .bt{display:flex;gap:10px;flex-wrap:wrap}
.rv-more{margin-top:12px}.rv-more summary{cursor:pointer;color:var(--muted);font-size:14px}.rv-more summary b{color:#fff;font-weight:500;font-size:15.5px}
.rv-more p{color:var(--muted);font-size:14px;max-width:52em;line-height:1.6}
@media (max-width:900px){.rv-grid{grid-template-columns:1fr}#rvr{position:static}.rv-3{grid-template-columns:1fr}}
@media (max-width:560px){.rv-f{grid-template-columns:1fr}.rv-card,#rvr{padding:18px}}
@media print{.rv-card,.rv-act,.rv-safe,.rv-sec,.ecobar,header,footer,.dhns{display:none!important}#rvr{background:#fff;color:#111;border-color:#999}}
</style>"""

def sel(i, label, opts, sm=""):
    o = "".join('<option value="%s"%s>%s</option>' % (v, ' selected' if s else '', t) for v, t, s in opts)
    return '<label>%s%s<select id="%s">%s</select></label>' % (label, (' <small>%s</small>' % sm) if sm else '', i, o)

def inp(i, label, val="", unit="", sm="", ph="", typ="text"):
    box = '<input id="%s" inputmode="decimal" type="%s" value="%s"%s>' % (i, typ, val, (' placeholder="%s"' % ph) if ph else '')
    if unit: box = '<span class="rv-u" data-u="%s">%s</span>' % (unit, box)
    return '<label>%s%s%s</label>' % (label, (' <small>%s</small>' % sm) if sm else '', box)

FORM = ('<form class="rv-card" id="rvf" onsubmit="return false">'
  '<p class="rv-note">Angka perkiraan juga boleh. Nilai uang dalam Rp miliar, contoh 2,5 berarti Rp2,5 miliar.</p>'
  '<div class="rv-blk"><p class="rv-h">Profil Rumah Sakit</p><div class="rv-f">'
  + sel("jenis", "Jenis RS", [("rsu", "RS Umum", False), ("rsia", "RS Ibu dan Anak (RSIA)", True), ("rsk", "RS Khusus Lain (Bedah, Mata, dll)", False)])
  + sel("kelas", "Kelas", [("b", "B", False), ("c", "C", True), ("d", "D", False)])
  + inp("tt", "Jumlah Tempat Tidur", "80", "TT")
  + inp("bor", "BOR Rata-Rata", "60", "%")
  + sel("akr", "Akreditasi", [("1.06", "Paripurna", False), ("1.0", "Utama", True), ("0.95", "Madya atau Dasar", False), ("0.85", "Belum Terakreditasi", False)])
  + sel("bpjs", "Kerja Sama BPJS", [("aktif", "Aktif", True), ("proses", "Sedang Perpanjangan", False), ("putus", "Diputus atau Kena Sanksi", False), ("non", "Tidak Kerja Sama", False)])
  + '</div></div><div class="rv-blk"><p class="rv-h">Keuangan Setahun Terakhir</p><div class="rv-f">'
  + inp("rev", "Pendapatan", "40", "miliar")
  + inp("ebitda", "EBITDA", "6", "miliar", "laba sebelum bunga, pajak, penyusutan")
  + '</div></div><div class="rv-blk"><p class="rv-h">Aset, Utang, dan Saham</p><div class="rv-f">'
  + sel("lahan", "Lahan dan Gedung", [("milik", "Milik Sendiri", True), ("sewa", "Sewa", False)])
  + inp("umur", "Umur Gedung", "6", "tahun")
  + inp("apr", "Nilai Appraisal KJPP atau Bank", "", "miliar", "opsional", "jika ada")
  + inp("utang", "Utang Bank", "10", "miliar")
  + inp("porsi", "Porsi Saham yang Dijual", "100", "%")
  + '</div></div></form>')

RES = ('<aside id="rvr" aria-live="polite">'
  '<div class="rv-k">Estimasi Nilai Perusahaan (EV)</div><div class="rv-big" id="rv_ev">-</div>'
  '<div class="rv-row"><span>Pendekatan Pendapatan</span><b id="rv_inc">-</b></div>'
  '<div class="rv-row"><span>Pendekatan Aset</span><b id="rv_ast">-</b></div>'
  '<div class="rv-row"><span>Dikurangi Utang Bank</span><b id="rv_dbt">-</b></div>'
  '<div class="rv-row"><span>Nilai 100%% Saham</span><b id="rv_eq">-</b></div>'
  '<div class="rv-stk"><div class="rv-k">Estimasi Harga Saham yang Dijual</div><div class="rv-big" id="rv_stk">-</div></div>'
  '<ul class="rv-fl" id="rv_fl"></ul>'
  '<div class="rv-act"><a class="btn solid" href="https://wa.me/%s" id="rv_wa" rel="noopener" target="_blank">Diskusikan Hasil via WhatsApp</a>'
  '<a class="btn line" href="/rumah-sakit-dijual/">Lihat Listing RS Dijual</a></div>'
  '<p class="rv-sm">Estimasi indikatif dari benchmark transaksi RS swasta di Indonesia. Harga akhir ditentukan due diligence, penilaian KJPP, dan negosiasi dengan pembeli.</p>'
  '</aside>') % WA

SAFE = ('<div class="rv-safe"><span>Dihitung di Browser, Tidak Disimpan di Server</span><span>Estimasi Indikatif, Bukan Laporan Penilaian KJPP</span>'
  '<span>Data RS Dibuka ke Investor Hanya Setelah NDA</span><span>Termasuk RS yang Kerja Sama BPJS-nya Bermasalah</span></div>')

HOW = ('<section class="rv-sec"><h2>Cara Kalkulator Ini Menghitung</h2><div class="rv-3">'
  '<div><em>Langkah 1</em><b>Pendekatan Pendapatan</b><p>EBITDA dikali multiple transaksi RS swasta (5 sampai 8 kali), disesuaikan dengan kelas, akreditasi, status BPJS, BOR, dan kepemilikan gedung.</p></div>'
  '<div><em>Langkah 2</em><b>Pendekatan Aset</b><p>Memakai appraisal KJPP atau bank bila ada. Bila belum, diestimasi dari nilai aset per tempat tidur, disusutkan sesuai umur gedung, dan didiskon bila arus pasien terganggu.</p></div>'
  '<div><em>Langkah 3</em><b>Nilai Saham</b><p>Nilai tertinggi dari dua pendekatan dikurangi utang bank, lalu dikali porsi saham yang dijual. Angka inilah yang dinegosiasikan dengan pembeli.</p></div>'
  '</div></section>')

TBL = ('<section class="rv-sec"><h2>Faktor yang Menaikkan dan Menurunkan Harga RS</h2><div class="rv-tw"><table class="rv-t">'
  '<thead><tr><th>Faktor</th><th>Pengaruh</th><th>Catatan</th></tr></thead><tbody>'
  '<tr><td>Kerja sama BPJS aktif</td><td class="pu">Naik</td><td>Volume pasien terjamin. Sebagian besar pembeli RS di Indonesia mencari RS BPJS.</td></tr>'
  '<tr><td>Kerja sama BPJS diputus</td><td class="pd">Turun tajam</td><td>Harga bergeser ke nilai aset. Isi temuan audit dan kewajiban pengembalian klaim sangat menentukan.</td></tr>'
  '<tr><td>Akreditasi Paripurna</td><td class="pu">Naik</td><td>Mempercepat perizinan dan kerja sama asuransi bagi pembeli.</td></tr>'
  '<tr><td>Lahan dan gedung milik sendiri</td><td class="pu">Naik</td><td>Ada nilai lantai dari aset fisik.</td></tr>'
  '<tr><td>BOR di bawah 50%</td><td class="pu">Netral sampai naik</td><td>Kapasitas menganggur bisa jadi peluang bagi pembeli strategis yang punya jaringan rujukan.</td></tr>'
  '<tr><td>Laporan keuangan belum diaudit</td><td class="pd">Diskon risiko</td><td>Bisa ditutup dengan audit KAP atau financial due diligence sebelum ditawarkan.</td></tr>'
  '</tbody></table></div></section>')

CTA = ('<section class="rv-sec"><div class="rv-cta"><div><h2>Mau Jual RS atau Cari Investor?</h2>'
  '<p>FA Indonesia mendampingi pemilik RS dari sisi penjual: valuasi, teaser dan data room, penawaran ke investor, due diligence, sampai closing. Identitas RS hanya dibuka setelah NDA.</p></div>'
  '<div class="bt"><a class="btn solid" href="https://wa.me/%s?text=%s" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
  '<a class="btn line" href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a></div></div></section>') % (
  WA, "Halo%2C%20saya%20ingin%20konsultasi%20penjualan%20rumah%20sakit.")

FAQ = [("Bagaimana cara menghitung harga jual rumah sakit?", "Dengan dua pendekatan: pendekatan pendapatan (EBITDA dikali multiple transaksi) dan pendekatan aset (tanah, gedung, alat kesehatan). Nilai perusahaan dikurangi utang bank menjadi nilai saham. Status BPJS, akreditasi, BOR, dan kepemilikan gedung menaikkan atau menurunkan multiple."),
       ("Apakah RS yang kerja sama BPJS-nya diputus masih bisa dijual?", "Bisa. Harganya biasanya bergeser mendekati nilai aset, dan struktur transaksinya perlu diatur, misalnya jual aset atau jual saham dengan klausul jaminan, tergantung isi temuan audit BPJS dan kewajiban klaim yang masih terbuka."),
       ("Apakah laporan keuangan harus sudah diaudit?", "Tidak untuk tahap awal. Laporan keuangan internal cukup untuk estimasi dan penjajakan investor. Audit KAP dan penilaian KJPP biasanya dibutuhkan saat due diligence."),
       ("Berapa lama proses menjual rumah sakit?", "Umumnya 4 sampai 9 bulan: persiapan data, penawaran ke investor, due diligence, negosiasi, sampai penandatanganan jual beli saham atau aset."),
       ("Siapa saja pembeli rumah sakit di Indonesia?", "Grup RS swasta yang sedang ekspansi, private equity, perusahaan yang ingin masuk bisnis kesehatan, kelompok dokter spesialis, dan pengusaha daerah."),
       ("Apakah data RS saya aman?", "Kalkulator berjalan di browser Anda dan tidak menyimpan data di server FA. Data hanya terkirim bila Anda menekan tombol WhatsApp, dan informasi RS baru ditawarkan ke calon investor setelah NDA ditandatangani.")]

SEO = ('<section class="rv-sec"><details class="rv-more"><summary>Tentang Kalkulator Valuasi Rumah Sakit FA</summary>'
  '<p>Kalkulator ini membantu pemilik rumah sakit umum, rumah sakit ibu dan anak (RSIA), dan rumah sakit khusus memperkirakan harga jual RS sebelum bicara dengan calon pembeli atau investor. '
  'Valuasi rumah sakit dihitung seperti cara pembeli menilai: kemampuan menghasilkan EBITDA, nilai aset tanah, gedung, dan alat kesehatan, lalu dikurangi utang bank.</p>'
  '<p>Untuk rumah sakit yang sedang bermasalah dengan BPJS, misalnya kerja sama diputus atau kena sanksi setelah audit, harga biasanya mendekati nilai aset. '
  'FA Indonesia mendampingi penjualan rumah sakit dan pencarian investor rumah sakit dari sisi penjual sampai closing, bersama KAP dan KJPP mitra untuk audit dan penilaian.</p></details></section>')

JS = r"""<script>
(function(){
var WA="__WA__",$=function(i){return document.getElementById(i)};
function num(i){var v=($(i).value||"").toString().trim().replace(/\./g,"").replace(",",".");if(v==="")return null;v=parseFloat(v);return isNaN(v)?null:v}
function fmt(v){if(v===null||!isFinite(v))return"-";var a=Math.abs(v),s=a<10?a.toFixed(1):Math.round(a).toString();return(v<0?"-":"")+"Rp"+s.replace(".",",")+" M"}
function rng(a,b){if(a===null||b===null)return"-";if(Math.abs(a-b)<0.05)return fmt(a);if(a>=0&&b>=0)return fmt(a).replace(" M","")+" sampai "+fmt(b).replace("Rp","");return fmt(a)+" sampai "+fmt(b)}
var perTT={rsu:1.0,rsia:0.8,rsk:0.9},kelasAdj={b:1.1,c:1.0,d:0.9},bpjsAdj={aktif:1.0,proses:0.85,putus:0.55,non:0.8},
lbl={rsu:"RS Umum",rsia:"RSIA",rsk:"RS Khusus"},bt={aktif:"Aktif",proses:"Sedang perpanjangan",putus:"Diputus / sanksi",non:"Tidak kerja sama"},last={};
function calc(){
 var jenis=$("jenis").value,kelas=$("kelas").value,tt=num("tt")||0,bor=num("bor"),akr=parseFloat($("akr").value),bpjs=$("bpjs").value,
 rev=num("rev"),eb=num("ebitda"),lahan=$("lahan").value,umur=num("umur")||0,apr=num("apr"),utang=num("utang")||0,po=Math.min(100,Math.max(1,num("porsi")||100))/100;
 var adj=kelasAdj[kelas]*akr*bpjsAdj[bpjs]*(lahan==="sewa"?0.9:1);if(bor!==null&&bor>=75)adj*=1.05;
 var iL=null,iH=null;if(eb!==null&&eb>0){iL=eb*5*adj;iH=eb*8*adj}
 var base,ap=false;if(apr!==null&&apr>0){base=apr;ap=true}else{base=tt*perTT[jenis]*Math.max(0.5,1-0.025*umur);if(lahan==="sewa")base*=0.3}
 var ec=0.6+0.4*bpjsAdj[bpjs],aH=base*ec,aL=base*0.7*ec;
 var eL=Math.max(iL||0,aL),eH=Math.max(iH||0,aH),qL=eL-utang,qH=eH-utang,sL=qL*po,sH=qH*po;
 $("rv_ev").textContent=rng(eL,eH);
 $("rv_inc").textContent=iL===null?"Tidak relevan (EBITDA negatif)":rng(iL,iH);
 $("rv_ast").textContent=rng(aL,aH)+(ap?" (appraisal)":"");
 $("rv_dbt").textContent=utang?"- "+fmt(utang):"Rp0";
 $("rv_eq").textContent=rng(qL,qH);
 $("rv_stk").textContent=rng(sL,sH)+(po<1?" ("+Math.round(po*100)+"%)":"");
 var f=[];
 if(bpjs==="putus")f.push(["dn","Kerja sama BPJS diputus: pembeli menawar mendekati nilai aset. Struktur transaksi (jual aset atau saham) jadi kunci."]);
 if(bpjs==="proses")f.push(["in","Perpanjangan BPJS belum final: pembeli biasanya minta closing setelah kontrak baru terbit."]);
 if(bpjs==="aktif")f.push(["up","BPJS aktif: daya tarik utama bagi grup RS yang sedang ekspansi."]);
 if(akr>=1.06)f.push(["up","Akreditasi Paripurna menambah nilai jual."]);
 if(bor!==null&&bor<50)f.push(["in","BOR di bawah 50%: kapasitas menganggur, peluang bagi pembeli yang punya jaringan rujukan."]);
 if(eb!==null&&eb<=0)f.push(["dn","EBITDA negatif: valuasi bertumpu pada aset. Perbaikan margin sebelum dijual bisa menaikkan harga."]);
 if(rev&&eb&&eb>0){var m=eb/rev*100;if(m<10)f.push(["in","Margin EBITDA "+m.toFixed(0)+"%: di bawah rata-rata RS swasta, ada ruang efisiensi."]);else if(m>=20)f.push(["up","Margin EBITDA "+m.toFixed(0)+"%: di atas rata-rata RS swasta."])}
 if(lahan==="sewa")f.push(["in","Gedung sewa: sisa masa sewa dan opsi perpanjangan akan diperiksa pembeli."]);
 if(qL<0)f.push(["dn","Utang bank lebih besar dari nilai bawah perusahaan: perlu skema restrukturisasi atau pelunasan saat closing."]);
 if(!ap)f.push(["in","Belum ada appraisal: nilai aset diestimasi dari benchmark per tempat tidur. Laporan KJPP mempertajam angka ini."]);
 var ic={up:"+",dn:"!",in:"i"};
 $("rv_fl").innerHTML=f.slice(0,5).map(function(x){return'<li class="'+x[0]+'"><i>'+ic[x[0]]+'</i><span>'+x[1]+'</span></li>'}).join("");
 last={jenis:jenis,kelas:kelas,tt:tt,bor:bor,akr:$("akr").options[$("akr").selectedIndex].text,bpjs:bpjs,rev:rev,eb:eb,lahan:lahan,utang:utang,po:po,sL:sL,sH:sH};
 var l=last,msg="Halo, saya ingin konsultasi penjualan rumah sakit.\n\n"+
  "Jenis: "+lbl[l.jenis]+" kelas "+l.kelas.toUpperCase()+" | TT: "+l.tt+" | BOR: "+(l.bor===null?"-":l.bor)+"%\n"+
  "Akreditasi: "+l.akr+" | BPJS: "+bt[l.bpjs]+"\n"+
  "Pendapatan: Rp"+(l.rev===null?"-":l.rev)+" M | EBITDA: Rp"+(l.eb===null?"-":l.eb)+" M\n"+
  "Lahan dan gedung: "+(l.lahan==="milik"?"Milik sendiri":"Sewa")+" | Utang bank: Rp"+l.utang+" M\n"+
  "Porsi dijual: "+Math.round(l.po*100)+"%\nHasil kalkulator: "+rng(l.sL,l.sH);
 $("rv_wa").href="https://wa.me/"+WA+"?text="+encodeURIComponent(msg);
 try{$("rv_wa").removeAttribute("data-refd")}catch(e){}
}
var t0=0;function track(){if(t0)return;t0=1;try{if(window.gtag)gtag("event","rsval_calc",{jenis:$("jenis").value,bpjs:$("bpjs").value})}catch(e){}}
var els=document.querySelectorAll("#rvf input,#rvf select");for(var i=0;i<els.length;i++){els[i].addEventListener("input",function(){calc();track()});els[i].addEventListener("change",calc)}
$("rv_wa").addEventListener("click",function(){try{if(window.gtag)gtag("event","rsval_wa",{jenis:$("jenis").value,bpjs:$("bpjs").value})}catch(e){}},true);
calc();
})();
</script>""".replace("__WA__", WA)

def page():
    t = TPL
    title = "Kalkulator Valuasi Rumah Sakit: Estimasi Harga Jual RS dan RSIA | FA Indonesia"
    desc = "Hitung estimasi harga jual rumah sakit, RSIA, atau RS khusus dalam 2 menit: pendekatan EBITDA dan aset, dikurangi utang bank. Gratis, termasuk RS yang kerja sama BPJS-nya bermasalah."
    old = "https://faindonesia.co.id/komite-audit-komisaris-independen/"
    t = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, t, count=1, flags=re.S)
    for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        t = re.sub(r'(<meta %s content=")[^"]*' % re.escape(k), lambda m: m.group(1) + desc, t)
    for k in ('property="og:title"', 'name="twitter:title"'):
        t = re.sub(r'(<meta %s content=")[^"]*' % re.escape(k), lambda m: m.group(1) + title, t)
    t = t.replace('<meta property="og:type" content="profile">', '<meta property="og:type" content="website">')
    url = SITE + "/" + SLUG + "/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "@id": url + "#app", "name": "FA Venus · Kalkulator Valuasi Rumah Sakit", "url": url, "applicationCategory": "FinanceApplication",
         "operatingSystem": "Web", "description": desc, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR"},
         "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": SITE + "/"}},
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), t, count=1, flags=re.S)
    t = t.replace(old, url)
    faqh = '<section class="rv-sec"><h2>Pertanyaan Umum Pemilik RS</h2>' + "".join('<details class="rv-more"><summary><b>%s</b></summary><p>%s</p></details>' % (q, a) for q, a in FAQ) + "</section>"
    main = ('<main id="top">' + CSS + '<section class="block"><div class="wrap">'
            '<div class="rv-hero"><p class="eyebrow">FA Venus · Valuasi Rumah Sakit</p><h1>Berapa Harga Jual Rumah Sakit Anda?</h1>'
            '<p class="rv-lede">Isi data RS, RSIA, atau RS khusus. Estimasi nilai perusahaan dan harga saham langsung muncul, termasuk untuk RS yang kerja sama BPJS-nya bermasalah.</p></div>'
            '<div class="rv-grid">' + FORM + RES + '</div>' + SAFE + HOW + TBL + CTA + faqh + SEO + JS + '</div></section></main>')
    t = re.sub(r'<main id="top">.*?</main>', lambda m: main, t, count=1, flags=re.S)
    os.makedirs(os.path.join(B, SLUG), exist_ok=True)
    open(os.path.join(B, SLUG, "index.html"), "w", encoding="utf-8").write(t)
    print("ok", SLUG, len(t))

page()

# ---------- integrasi: tombol dari halaman RS dan valuasi ----------
for rel in ("rumah-sakit-dijual/index.html", "konsultan-rumah-sakit/index.html", "jasa-valuasi-usaha/index.html"):
    p = os.path.join(B, rel)
    if not os.path.exists(p): continue
    t = open(p, encoding="utf-8").read()
    if 'href="/%s/"' % SLUG in t: print("ada", rel); continue
    m = re.search(r'Chat Ananta, CPA</a>', t)
    if not m: print("no-btn", rel); continue
    t = t[:m.end()] + '<a class="btn line" href="/%s/">Kalkulator Valuasi RS</a>' % SLUG + t[m.end():]
    open(p, "w", encoding="utf-8").write(t); print("link", rel)

sp = os.path.join(B, "sitemap.xml"); t = open(sp, encoding="utf-8").read(); u = SITE + "/" + SLUG + "/"
if u not in t: open(sp, "w", encoding="utf-8").write(t.replace("</urlset>", "<url><loc>%s</loc><lastmod>2026-11-04</lastmod></url></urlset>" % u))
lp = os.path.join(B, "llms.txt"); t = open(lp, encoding="utf-8").read()
if SLUG not in t:
    open(lp, "a", encoding="utf-8").write("\n- [Kalkulator Valuasi Rumah Sakit](%s): estimasi harga jual RS, RSIA, dan RS khusus (EBITDA x multiple dan nilai aset, dikurangi utang bank), termasuk RS dengan masalah kerja sama BPJS; pendampingan sell side sampai closing.\n" % u)

# ---------- 4 Nov pagi: masuk daftar aplikasi berbayar Rp49.000 (paywall QRIS dipasang prep.py: app venus-rsval) ----------
def _rw(rel, fn):
    p = os.path.join(B, rel)
    if not os.path.exists(p): print("skip", rel); return
    t = open(p, encoding="utf-8").read(); n = fn(t)
    if n != t: open(p, "w", encoding="utf-8").write(n); print("patch", rel)
    else: print("tetap", rel)

def _apps(t):
    if 'href="/%s/"' % SLUG in t: return t
    m = re.search(r'<a class="card" data-c="dana" data-q="fa venus · valuasi dcf.*?</a>', t, flags=re.S)
    if not m: print("dcf card tidak ketemu"); return t
    card = ('<a class="card" data-c="dana" data-q="fa venus · valuasi rumah sakit harga jual rs rsia, ebitda, nilai aset, bpjs, utang bank, investor rumah sakit. pendanaan" href="/%s/">'
            '<b>FA Venus · Valuasi Rumah Sakit</b><p>Estimasi harga jual RS, RSIA, dan RS khusus: EBITDA x multiple, nilai aset, utang bank, dan dampak status BPJS.</p>'
            '<div class="meta"><span class="badge">Live</span><span class="cat">Rp49 rb</span><span class="cat">Pendanaan</span><span class="src">FA Indonesia</span></div></a>') % SLUG
    return t[:m.end()] + card + t[m.end():]
_rw("apps/index.html", _apps)

def _toko(t):
    if 'id="p-venus-rsval"' in t: return t
    m = re.search(r'<article class="it" data-cat="app" data-free="1" data-for="ca" id="p-venus-dcf">(.*?)</article>', t, flags=re.S)
    k = t.find('id="p-ar-year"')
    if not m or k < 0: print("toko anchor tidak ketemu"); return t
    cov = re.search(r'<a class="cv app".*?</a>', m.group(1), flags=re.S).group(0)
    cov = (cov.replace("/kalkulator-valuasi-dcf/", "/%s/" % SLUG).replace("Buka FA Venus Valuasi DCF", "Buka FA Venus Valuasi Rumah Sakit")
              .replace("venus-dcf", "venus-rsval").replace("<small>Valuasi DCF</small>", "<small>Valuasi RS</small>").replace("app-9.jpg", "app-2.jpg"))
    art = ('<article class="it" data-cat="app" data-for="ca" id="p-venus-rsval">' + cov +
           '<div class="in"><span class="tg">Aplikasi · Rumah Sakit</span><h3>FA Venus: Valuasi Rumah Sakit</h3>'
           '<p>Estimasi harga jual RS dan RSIA dari EBITDA, nilai aset, utang bank, dan status BPJS, lengkap dengan faktor penaik dan penurun harga.</p>'
           '<div class="pr"><b>Rp49.000</b><small>termasuk PPN · bayar QRIS di aplikasi</small></div>'
           '<div class="ac"><a class="b" href="/%s/">Buka Aplikasi</a><a class="s" href="/artikel/harga-jual-rumah-sakit-cara-menghitung/">Cara Hitung</a></div></div></article>') % SLUG
    e = t.find("</article>", k) + len("</article>")
    t = t[:e] + art + t[e:]
    t = re.sub(r'(data-f="app" aria-pressed="false">Aplikasi<small>)(\d+)', lambda x: x.group(1) + str(int(x.group(2)) + 1), t, count=1)
    t = re.sub(r'(data-f="all" aria-pressed="true">Semua<small>)(\d+)', lambda x: x.group(1) + str(int(x.group(2)) + 1), t, count=1)
    return t
_rw("toko/index.html", _toko)

# kotak CTA di artikel RS lama
BOX = ('<!--rsval-cta--><div class="cta" style="margin:24px 0;border:1px solid currentColor;padding:18px 20px;display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between">'
       '<div><b style="display:block;font-size:17px">Berapa Harga Jual RS Anda?</b><span style="opacity:.75;font-size:14px">Kalkulator Valuasi Rumah Sakit: EBITDA, Nilai Aset, Utang Bank, dan Status BPJS</span></div>'
       '<a class="btn red" href="/%s/">Hitung Harga Jual RS</a></div><!--/rsval-cta-->') % SLUG
for rel in ("artikel/valuasi-rumah-sakit-swasta/index.html", "artikel/menjual-rumah-sakit-persiapan-sisi-penjual/index.html",
            "artikel/due-diligence-akuisisi-rumah-sakit-swasta/index.html", "artikel/indikator-keuangan-rumah-sakit-yang-dilihat-investor/index.html"):
    def _box(t):
        if "<!--rsval-cta-->" in t: return t
        k = t.find("<h2", t.find("<h1"))
        if k < 0: print("no h2", rel); return t
        return t[:k] + BOX + t[k:]
    _rw(rel, _box)
