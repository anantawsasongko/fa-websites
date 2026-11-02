# -*- coding: utf-8 -*-
"""Tiga lini bisnis baru FA (2 Nov 2026): FA Bankability Index, Audit Back-Office untuk KAP,
Bursa Komite Audit & Komisaris Independen. Halaman dibuat dari kerangka halaman komite-audit (header, footer, CSS situs).
Idempoten: menimpa halaman yang sama, marker <!--fa-trio-svc--> di Layanan dipasang sekali."""
import os, re, json
R = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(R, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
SITE = "https://faindonesia.co.id"
WA = "6282245260121"
TPL = open(os.path.join(B, "komite-audit-komisaris-independen", "index.html"), encoding="utf-8").read()

def wa(msg):
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (WA, quote(msg))

CSS = """<style>
.nx-hero{padding-top:8px}.nx-hero h1{margin:.15em 0 .35em;font-size:clamp(32px,4.6vw,56px);line-height:1.08;max-width:15em}
.nx-lede{font-size:clamp(16px,1.6vw,19px);color:var(--muted);max-width:40em;margin:0 0 26px}
.nx-btns{display:flex;gap:12px;flex-wrap:wrap}
.nx-sec{margin-top:64px}.nx-sec>h2{font-size:clamp(24px,2.8vw,34px);margin:0 0 22px;line-height:1.2}
.nx-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.nx-grid.g4{grid-template-columns:repeat(4,minmax(0,1fr))}
.nx-card{border:1px solid var(--line);background:var(--surface);border-radius:14px;padding:22px 20px;opacity:0;transform:translateY(14px);animation:nxUp .7s var(--ez) forwards}
.nx-card:nth-child(2){animation-delay:.08s}.nx-card:nth-child(3){animation-delay:.16s}.nx-card:nth-child(4){animation-delay:.24s}
.nx-card b{display:block;font-size:17px;line-height:1.3;margin-bottom:6px}.nx-card p{margin:0;color:var(--muted);font-size:14.5px;line-height:1.55}
.nx-card .nx-k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);margin-bottom:10px;display:block}
.nx-flow{display:grid;grid-template-columns:repeat(var(--n,4),minmax(0,1fr));gap:0;counter-reset:s;position:relative}
.nx-flow li{list-style:none;position:relative;padding:44px 14px 0 0;counter-increment:s;font-size:15px;line-height:1.45}
.nx-flow li:before{content:counter(s);position:absolute;top:0;left:0;width:30px;height:30px;border-radius:50%;border:1px solid #fff;display:grid;place-items:center;font-size:13px;background:var(--paper);z-index:1}
.nx-flow li:after{content:"";position:absolute;top:15px;left:30px;right:0;height:1px;background:rgba(255,255,255,.35);transform-origin:left;transform:scaleX(0);animation:nxLine 1s var(--ez) forwards}
.nx-flow li:last-child:after{display:none}.nx-flow li b{display:block;margin-bottom:4px}.nx-flow li span{color:var(--muted);font-size:14px}
.nx-flow{padding:0;margin:0}
.nx-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.nx-fact{border-top:1px solid #fff;padding-top:14px}.nx-fact b{display:block;font-size:clamp(26px,3vw,38px);line-height:1.1;font-weight:500}.nx-fact span{color:var(--muted);font-size:14px}
.nx-more{margin-top:18px}.nx-more summary{cursor:pointer;color:var(--muted);font-size:14px}.nx-more p{color:var(--muted);font-size:14px;max-width:52em}
.nx-src{font-size:12.5px;color:var(--muted);margin-top:14px}
@keyframes nxUp{to{opacity:1;transform:none}}@keyframes nxLine{to{transform:scaleX(1)}}
@media (max-width:900px){.nx-grid,.nx-grid.g4{grid-template-columns:repeat(2,minmax(0,1fr))}.nx-flow{grid-template-columns:1fr 1fr;row-gap:22px}.nx-flow li:after{display:none}}
@media (max-width:560px){.nx-grid,.nx-grid.g4,.nx-facts{grid-template-columns:1fr}.nx-flow{grid-template-columns:1fr}.nx-flow li{padding:4px 0 0 44px}.nx-sec{margin-top:48px}}
@media (prefers-reduced-motion:reduce){.nx-card{animation:none;opacity:1;transform:none}.nx-flow li:after{animation:none;transform:none}}
</style>"""

def cards(items, cls="nx-grid"):
    return '<div class="%s">' % cls + "".join('<div class="nx-card">%s<b>%s</b><p>%s</p></div>' % (('<span class="nx-k">%s</span>' % k) if k else "", t, d) for k, t, d in items) + "</div>"

def flow(items):
    return '<ol class="nx-flow" style="--n:%d">' % len(items) + "".join("<li><b>%s</b><span>%s</span></li>" % (t, d) for t, d in items) + "</ol>"

def page(slug, title, desc, main, faq):
    t = TPL
    old = "https://faindonesia.co.id/komite-audit-komisaris-independen/"
    t = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, t, 1, flags=re.S)
    t = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, t, 1)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, t, 1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + desc, t, 1)
    t = t.replace('<meta property="og:type" content="profile">', '<meta property="og:type" content="website">')
    t = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + title, t)
    t = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + desc, t)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": SITE + "/" + slug + "/", "url": SITE + "/" + slug + "/", "name": title, "description": desc,
         "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": SITE + "/"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), t, 1, flags=re.S)
    t = t.replace(old, SITE + "/" + slug + "/")
    faqh = '<section class="nx-sec"><h2>Pertanyaan Umum</h2>' + "".join('<details class="nx-more"><summary><b>%s</b></summary><p>%s</p></details>' % (q, a) for q, a in faq) + "</section>"
    newmain = '<main id="top">' + CSS + '<section class="block"><div class="wrap">' + main + faqh + "</div></section></main>"
    t = re.sub(r'<main id="top">.*?</main>', lambda m: newmain, t, 1, flags=re.S)
    os.makedirs(os.path.join(B, slug), exist_ok=True)
    open(os.path.join(B, slug, "index.html"), "w", encoding="utf-8").write(t)
    print("ok", slug, len(t))

# =============== 1. FA Bankability Index ===============
BI_CSS = """<style>
#bi{border:1px solid var(--line);background:var(--surface);border-radius:18px;padding:26px;margin-top:8px}
#bi .q{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 22px}
#bi label{display:block;font-size:13px;color:var(--muted);margin-bottom:6px}
#bi select,#bi input{width:100%;box-sizing:border-box;background:var(--paper);color:#fff;border:1px solid #3a3a3a;border-radius:10px;padding:11px 12px;font:inherit;font-size:15px}
#bi select:focus,#bi input:focus{outline:2px solid #fff;outline-offset:1px}
#bi h3{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);margin:26px 0 12px;font-weight:500}
#bi h3:first-child{margin-top:0}
#bi .hint{font-size:12.5px;color:var(--muted);margin-top:6px}
#bi .go{margin-top:24px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
#bi .err{color:#F08A82;font-size:14px}
#bres{display:none;margin-top:22px;border:1px solid var(--line);border-radius:18px;padding:26px;background:linear-gradient(160deg,#222,#161616)}
#bres.on{display:block;animation:nxUp .7s var(--ez) forwards}
.br-top{display:grid;grid-template-columns:200px 1fr;gap:28px;align-items:center}
.br-ring{position:relative;width:200px;height:200px}.br-ring svg{transform:rotate(-90deg)}
.br-ring circle{fill:none;stroke-width:12}.br-ring .bg{stroke:#2f2f2f}.br-ring .fg{stroke:#fff;stroke-linecap:round;transition:stroke-dashoffset 1.4s var(--ez)}
.br-num{position:absolute;inset:0;display:grid;place-items:center;text-align:center}.br-num b{font-size:54px;font-weight:500;line-height:1}.br-num span{display:block;font-size:12px;color:var(--muted);letter-spacing:.12em;text-transform:uppercase;margin-top:4px}
.br-grade{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
.br-title{font-size:clamp(24px,2.6vw,32px);margin:.2em 0 .3em;line-height:1.2}
.br-seg{display:inline-block;border:1px solid #fff;border-radius:999px;padding:6px 14px;font-size:14px;margin-top:6px}
.br-bars{display:grid;gap:10px;margin-top:26px}
.br-bar{display:grid;grid-template-columns:200px 1fr 46px;gap:12px;align-items:center;font-size:14px}
.br-bar i{display:block;height:8px;border-radius:8px;background:#2f2f2f;overflow:hidden}.br-bar i s{display:block;height:100%;background:#fff;width:0;transition:width 1.1s var(--ez)}
.br-bar em{font-style:normal;color:var(--muted);text-align:right}
.br-gaps{margin:26px 0 0;padding:0;list-style:none;display:grid;gap:10px}
.br-gaps li{border-left:2px solid #F08A82;padding:4px 0 4px 14px;font-size:15px}.br-gaps li b{display:block}.br-gaps li span{color:var(--muted);font-size:14px}
.br-note{font-size:12.5px;color:var(--muted);margin-top:18px}
@media (max-width:700px){#bi{padding:18px}#bi .q{grid-template-columns:1fr}.br-top{grid-template-columns:1fr;justify-items:center;text-align:center}.br-bar{grid-template-columns:1fr 46px}.br-bar i{grid-column:1/-1;order:3}#bres{padding:18px}}
</style>"""

def sel(id_, label, opts, hint=""):
    o = '<option value="">Pilih</option>' + "".join('<option value="%s">%s</option>' % (v, t) for v, t in opts)
    return '<div><label for="%s">%s</label><select id="%s" required>%s</select>%s</div>' % (id_, label, id_, o, ('<div class="hint">%s</div>' % hint) if hint else "")

def num(id_, label, hint=""):
    return '<div><label for="%s">%s</label><input id="%s" inputmode="decimal" placeholder="Rp juta, contoh 12.500" autocomplete="off">%s</div>' % (id_, label, id_, ('<div class="hint">%s</div>' % hint) if hint else "")

form = ('<form id="bi" onsubmit="return false">'
 '<h3>Profil Usaha</h3><div class="q">'
 + sel("b_bentuk", "Bentuk Usaha", [("2", "Perorangan"), ("5", "CV"), ("8", "PT")])
 + sel("b_umur", "Lama Beroperasi", [("0", "Kurang dari 2 Tahun"), ("4", "2 sampai 3 Tahun"), ("7", "3 sampai 5 Tahun"), ("10", "Lebih dari 5 Tahun")])
 + sel("b_legal", "Legalitas dan Izin Usaha", [("0", "Belum Lengkap"), ("3", "Sebagian (NIB atau Akta Saja)"), ("5", "Lengkap (Akta, NIB, Izin Sektor)")])
 + sel("b_cust", "Porsi Pelanggan Terbesar", [("0", "Lebih dari 50% Omzet"), ("3", "30% sampai 50%"), ("5", "Kurang dari 30%")])
 + '</div><h3>Kualitas Laporan</h3><div class="q">'
 + sel("b_lk", "Laporan Keuangan", [("0", "Belum Ada"), ("4", "Catatan Kas atau Excel Sederhana"), ("8", "Inhouse Lengkap (Neraca, Laba Rugi, Arus Kas)"), ("14", "Diaudit KAP")])
 + sel("b_pajak", "Laporan Pajak", [("0", "SPT Belum Rutin"), ("4", "SPT Rutin, Angka Beda dengan LK"), ("10", "SPT Rutin dan Selaras dengan LK")])
 + sel("b_slik", "Riwayat Kredit (SLIK)", [("10", "Lancar (Kolektibilitas 1)"), ("7", "Belum Pernah Kredit"), ("5", "Pernah Terlambat (Kol 2)"), ("x", "Ada Tunggakan Berat (Kol 3 sampai 5)")])
 + sel("b_rek", "Rekening Usaha Terpisah dari Pribadi", [("0", "Belum"), ("2", "Sebagian"), ("5", "Ya, Sepenuhnya")])
 + '</div><h3>Angka Keuangan (Rp Juta, Tahun Terakhir)</h3><div class="q">'
 + num("b_omzet", "Omzet Setahun") + num("b_aset", "Total Aset")
 + num("b_ebitda", "EBITDA Setahun", "Laba usaha ditambah penyusutan.") + num("b_ekuitas", "Total Ekuitas")
 + num("b_utang", "Utang Bank Termasuk Plafon yang Diincar") + num("b_agunan", "Nilai Pasar Agunan", "Tanah, bangunan, kendaraan, mesin yang bisa diikat.")
 + '</div><div class="go"><button type="button" id="bi_go" class="btn solid">Hitung Skor Saya</button><span class="err" id="b_err"></span></div></form>')

res = ('<div id="bres" aria-live="polite"><div class="br-top"><div class="br-ring"><svg width="200" height="200" viewBox="0 0 200 200"><circle class="bg" cx="100" cy="100" r="86"/>'
 '<circle class="fg" id="br_arc" cx="100" cy="100" r="86" stroke-dasharray="540.35" stroke-dashoffset="540.35"/></svg><div class="br-num"><div><b id="br_n">0</b><span>dari 100</span></div></div></div>'
 '<div><div class="br-grade" id="br_g"></div><div class="br-title" id="br_t"></div><div style="color:var(--muted)" id="br_d"></div><div class="br-seg" id="br_s"></div></div></div>'
 '<div class="br-bars" id="br_bars"></div><ul class="br-gaps" id="br_gaps"></ul>'
 '<div class="nx-btns" style="margin-top:24px"><a class="btn solid" id="br_wa" target="_blank" rel="noopener" href="#">Kirim Skor ke WhatsApp</a><a class="btn line" href="/cek-kapasitas-kredit/">Hitung Plafon Detail</a></div>'
 '<p class="br-note">Skor indikatif berdasarkan pola penilaian kredit bank umum, bukan keputusan bank. DSCR dihitung dengan asumsi bunga 11% dan tenor 5 tahun.</p></div>')

JS = r"""<script>
(function(){
var $=function(i){return document.getElementById(i)};
function n(i){var v=($(i).value||'').replace(/\./g,'').replace(',','.');var x=parseFloat(v);return isNaN(x)?null:x}
var LBL={profil:'Profil dan Legalitas',lap:'Kualitas Laporan',kredit:'Riwayat Kredit',kemampuan:'Kemampuan Bayar (DSCR)',struktur:'Struktur Modal dan Agunan'};
$('bi_go').addEventListener('click',function(){
 var ids=['b_bentuk','b_umur','b_legal','b_cust','b_lk','b_pajak','b_slik','b_rek'],e=$('b_err');e.textContent='';
 for(var k=0;k<ids.length;k++){if(!$(ids[k]).value){e.textContent='Lengkapi semua pilihan dulu.';$(ids[k]).focus();return}}
 var om=n('b_omzet'),as=n('b_aset'),eb=n('b_ebitda'),eq=n('b_ekuitas'),ut=n('b_utang'),ag=n('b_agunan');
 if([om,as,eb,eq,ut,ag].some(function(v){return v===null})){e.textContent='Isi semua angka keuangan (boleh 0).';return}
 var v=function(i){return +$(i).value}, slikBad=$('b_slik').value==='x';
 var ds=ut>0?eb/(ut*0.31):9, der=eq>0?ut/eq:9, cov=ut>0?ag/ut:2, de=eb>0?ut/eb:9;
 var pDs=ds>=1.5?15:ds>=1.25?11:ds>=1?5:0, pDer=der<=1?8:der<=2?6:der<=3?3:0, pCov=cov>=1.25?10:cov>=1?7:cov>=.7?4:0, pDe=de<=3?5:de<=4?3:0;
 var g={profil:[v('b_bentuk')+v('b_umur')+v('b_legal')+v('b_cust'),28],lap:[v('b_lk')+v('b_pajak')+v('b_rek'),29],kredit:[slikBad?0:v('b_slik'),10],kemampuan:[pDs+pDe,20],struktur:[pDer+pCov,18]};
 var tot=0,max=0;for(var x in g){tot+=g[x][0];max+=g[x][1]}
 var sc=Math.round(tot/max*100); if(slikBad)sc=Math.min(sc,35); if(eb<=0)sc=Math.min(sc,40);
 var gr=sc>=80?['A','Siap Diajukan ke Bank','Berkas dan angka sudah di level yang biasanya lolos analis kredit.']:sc>=65?['B','Hampir Siap','Satu atau dua celah perlu ditutup supaya plafon dan bunga optimal.']:sc>=50?['C','Perlu Perbaikan 3 sampai 6 Bulan','Rapikan laporan dan struktur utang sebelum mengajukan, agar tidak ditolak dan tercatat di SLIK.']:sc>=35?['D','Belum Siap','Fokus membenahi laporan keuangan dan pajak dulu, baru bicara plafon.']:['E','Benahi Fondasi Dulu','Ada faktor yang biasanya membuat bank langsung menolak. Selesaikan itu lebih dulu.'];
 var seg=as<2500?'Segmen Mikro dan KUR':as<25000?'Segmen SME dan Bisnis Ritel':as<500000?'Segmen Komersial':'Segmen Korporasi';
 var gaps=[];
 if(slikBad)gaps.push(['Selesaikan Tunggakan di SLIK','Kolektibilitas 3 sampai 5 hampir selalu ditolak. Restrukturisasi atau lunasi dulu.',0]);
 if(v('b_lk')<8)gaps.push(['Susun Laporan Keuangan Lengkap','Bank menilai dari neraca, laba rugi, dan arus kas minimal 2 tahun.',1]);
 if(v('b_lk')<14&&as>=25000)gaps.push(['Siapkan Laporan Diaudit KAP','Untuk segmen komersial, laporan diaudit biasanya jadi syarat.',2]);
 if(v('b_pajak')<10)gaps.push(['Selaraskan SPT dengan Laporan Keuangan','Analis membandingkan omzet SPT, mutasi rekening, dan laporan.',3]);
 if(pDs<11)gaps.push(['Naikkan DSCR di Atas 1,25','Perpanjang tenor, turunkan plafon, atau perbaiki EBITDA sebelum mengajukan.',4]);
 if(pCov<7)gaps.push(['Tambah Agunan atau Turunkan Plafon','Nilai agunan di bawah utang membuat plafon dipotong.',5]);
 if(pDer<6)gaps.push(['Perkuat Ekuitas','Utang lebih dari 2 kali ekuitas menekan penilaian struktur modal.',6]);
 if(v('b_rek')<5)gaps.push(['Pisahkan Rekening Usaha','Mutasi rekening usaha adalah bukti omzet yang paling dipercaya bank.',7]);
 if(v('b_cust')<3)gaps.push(['Kurangi Ketergantungan pada Satu Pelanggan','Konsentrasi di atas 50% dianggap risiko tinggi.',8]);
 if(v('b_legal')<5)gaps.push(['Lengkapi Legalitas dan Izin','Akta, NIB, dan izin sektor dicek sejak tahap awal.',9]);
 if(!gaps.length)gaps.push(['Siapkan Paket Pengajuan','Proyeksi, memo kredit, dan data pendukung agar analis cepat memproses.',10]);
 gaps=gaps.slice(0,3);
 var r=$('bres');r.classList.add('on');
 $('br_g').textContent='Grade '+gr[0];$('br_t').textContent=gr[1];$('br_d').textContent=gr[2];$('br_s').textContent=seg+' (Indikatif)';
 var c=0,t0=null;function anim(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1300);c=Math.round(sc*(1-Math.pow(1-p,3)));$('br_n').textContent=c;if(p<1)requestAnimationFrame(anim)}requestAnimationFrame(anim);
 setTimeout(function(){$('br_arc').style.strokeDashoffset=540.35*(1-sc/100)},60);
 var h='';for(var x in g){var pc=Math.round(g[x][0]/g[x][1]*100);h+='<div class="br-bar"><span>'+LBL[x]+'</span><i><s data-w="'+pc+'"></s></i><em>'+pc+'%</em></div>'}$('br_bars').innerHTML=h;
 setTimeout(function(){[].forEach.call(document.querySelectorAll('.br-bar s'),function(s){s.style.width=s.getAttribute('data-w')+'%'})},80);
 $('br_gaps').innerHTML=gaps.map(function(a){return '<li><b>'+a[0]+'</b><span>'+a[1]+'</span></li>'}).join('');
 var msg='Halo FA Indonesia, saya sudah cek FA Bankability Index.\nSkor: '+sc+'/100 (Grade '+gr[0]+', '+gr[1]+')\n'+seg+'\nCelah utama: '+gaps.map(function(a){return a[0]}).join('; ')+'\nSaya ingin diskusi langkah berikutnya.';
 $('br_wa').href='https://wa.me/__WA__?text='+encodeURIComponent(msg);
 try{gtag('event','bankability_score',{score:sc,grade:gr[0],segmen:seg,dscr:Math.round(ds*100)/100,lk:$('b_lk').value})}catch(_){}
 r.scrollIntoView({behavior:'smooth',block:'start'});
});
})();
</script>""".replace("__WA__", WA)

main1 = (BI_CSS + '<div class="nx-hero"><p class="eyebrow">FA Venus · Bankability Index</p>'
 '<h1>Seberapa Siap Usaha Anda Dibiayai Bank?</h1>'
 '<p class="nx-lede">14 pertanyaan, sekitar 2 menit. Hasilnya skor 0 sampai 100, segmen bank yang cocok, dan 3 celah yang perlu ditutup sebelum mengajukan.</p></div>'
 + form + res +
 '<section class="nx-sec"><h2>Yang Dinilai</h2>' + cards([
   ("27%", "Profil dan Legalitas", "Bentuk usaha, umur, izin, dan konsentrasi pelanggan."),
   ("28%", "Kualitas Laporan", "Laporan keuangan, kepatuhan SPT, dan pemisahan rekening."),
   ("10%", "Riwayat Kredit", "Kolektibilitas di SLIK OJK."),
   ("35%", "Kemampuan Bayar dan Agunan", "DSCR, utang terhadap EBITDA, DER, dan rasio agunan.")], "nx-grid g4") + '</section>'
 '<section class="nx-sec"><h2>Setelah Skor Keluar</h2>' + flow([
   ("Kirim Skor", "Lewat tombol WhatsApp, tanpa mengisi ulang."),
   ("Diagnosis Singkat", "Tim FA membaca laporan dan mutasi rekening."),
   ("Tutup Celah", "Laporan, pajak, dan struktur utang dibenahi."),
   ("Ajukan ke Bank", "Paket pengajuan lengkap, didampingi sampai cair.")]) + '</section>'
 '<section class="nx-sec"><h2>Untuk RM Bank</h2><p class="nx-lede" style="margin-bottom:18px">Calon debitur yang sudah diskor dan dibenahi kami rujuk ke RM yang segmennya cocok, tanpa biaya untuk bank.</p>'
 '<div class="nx-btns"><a class="btn line" href="/mitra-rm-bank/">Program Mitra RM Bank</a></div></section>' + JS)

faq1 = [("Apa itu FA Bankability Index?", "Skor 0 sampai 100 yang mengukur kesiapan usaha mengajukan kredit bank, dari kualitas laporan, kepatuhan pajak, riwayat SLIK, kemampuan bayar (DSCR), sampai agunan. Disusun dari pola penilaian analis kredit bank umum."),
        ("Apakah skor ini keputusan bank?", "Bukan. Skor bersifat indikatif untuk memetakan celah sebelum mengajukan. Keputusan tetap pada analis dan komite kredit bank."),
        ("Apakah data saya disimpan?", "Tidak. Perhitungan berjalan di browser. Data hanya terkirim bila Anda menekan tombol Kirim Skor ke WhatsApp."),
        ("Berapa skor yang biasanya siap diajukan?", "Di atas 80 umumnya siap. Skor 65 sampai 79 biasanya cukup menutup satu atau dua celah dulu agar plafon dan bunga optimal.")]
page("bankability-index", "FA Bankability Index: Cek Kesiapan Kredit Bank | FA Indonesia",
     "Cek kesiapan usaha mengajukan kredit bank dalam 2 menit: skor 0 sampai 100, segmen bank yang cocok, dan 3 celah yang perlu ditutup. Data dihitung di browser.", main1, faq1)

# =============== 2. Audit Back-Office untuk KAP ===============
wa2 = wa("Halo FA Indonesia, saya dari KAP dan ingin diskusi Audit Back-Office (FA Saturn dan tim kertas kerja).")
main2 = ('<div class="nx-hero"><p class="eyebrow">Untuk KAP · FA Saturn</p>'
 '<h1>Kapasitas Audit Tambahan, Tanpa Menambah Staf Tetap</h1>'
 '<p class="nx-lede">Workspace audit FA Saturn ditambah tim pendukung yang menyiapkan kertas kerja mengikuti metodologi KAP Anda. Opini dan tanggung jawab tetap pada Partner.</p>'
 '<div class="nx-btns"><a class="btn solid" href="%s" target="_blank" rel="noopener">Diskusi Kapasitas</a><a class="btn line" href="/saturn/">Coba FA Saturn</a></div></div>' % wa2 +
 '<section class="nx-sec"><h2>Masalah yang Kami Selesaikan</h2>' + cards([
   ("Musim Audit", "Januari sampai April Menumpuk", "Perikatan datang bersamaan, staf tidak bertambah, tenggat RUPS dan bank tetap jalan."),
   ("SDM", "Staf Junior Cepat Keluar", "Setiap musim melatih orang baru dari nol, kualitas kertas kerja naik turun."),
   ("Review", "Waktu Partner Habis untuk Merapikan", "Review seharusnya soal pertimbangan, bukan memperbaiki format dan tickmark.")]) + '</section>'
 '<section class="nx-sec"><h2>Paket</h2>' + cards([
   ("Workspace", "FA Saturn", "Engagement per klien, Combined Risk Assessment, materialitas, sign-off berjenjang, review note. Data di Google Drive KAP."),
   ("Workspace + Tim", "Tim Kertas Kerja per Perikatan", "Lead schedule, KK anak, dan uji substantif disiapkan tim, lalu direview staf KAP di FA Saturn."),
   ("Musiman", "Peak Season Squad", "Tim 2 sampai 4 orang dikontrak khusus Januari sampai April untuk perikatan yang menumpuk.")]) + '</section>'
 '<section class="nx-sec"><h2>Alur Kerja</h2>' + flow([
   ("Partner Menetapkan Arah", "Risiko, materialitas, dan program audit."),
   ("Tim FA Menyiapkan KK", "Lead schedule, KK anak, uji substantif primer."),
   ("Review oleh KAP", "Senior dan Manager KAP review di FA Saturn."),
   ("Partner Sign-Off", "Opini dan LAI sepenuhnya oleh KAP.")]) + '</section>'
 '<section class="nx-sec"><h2>Batas Mutu dan Independensi</h2>' + cards([
   ("SMM 1", "Di Bawah Sistem Mutu KAP", "Tim bekerja atas arahan dan supervisi Partner, mengikuti kebijakan manajemen mutu KAP."),
   ("Independensi", "Tidak untuk Klien yang LK-nya Kami Susun", "Perikatan audit atas laporan yang disusun FA atau KJA mitra tidak kami kerjakan."),
   ("Kerahasiaan", "NDA per Perikatan, Data di Drive KAP", "Kertas kerja tersimpan di Google Drive milik KAP, bukan server FA.")]) + '</section>')
faq2 = [("Siapa yang menandatangani opini audit?", "Selalu Partner KAP. Tim FA hanya menyiapkan kertas kerja di bawah supervisi KAP, sesuai kebijakan manajemen mutu KAP."),
        ("Apakah bisa dipakai tanpa tim, hanya software?", "Bisa. FA Saturn dapat dilisensikan sendiri. Coba semua fitur di faindonesia.co.id/saturn sebelum mengaktifkan lisensi."),
        ("Bagaimana dengan independensi?", "Tim tidak mengerjakan perikatan audit atas laporan keuangan yang disusun FA Indonesia atau KJA mitra, dan setiap anggota tim menandatangani pernyataan independensi per perikatan."),
        ("Bagaimana biaya tim kertas kerja dihitung?", "Per perikatan, berdasarkan jumlah akun signifikan dan kompleksitas entitas. Estimasi diberikan setelah melihat neraca saldo klien.")]
page("audit-back-office-kap", "Audit Back-Office untuk KAP: FA Saturn dan Tim Kertas Kerja | FA Indonesia",
     "Kapasitas audit tambahan untuk KAP: workspace FA Saturn dan tim pendukung kertas kerja di bawah supervisi Partner. Cocok untuk musim audit Januari sampai April.", main2, faq2)

# =============== 3. Bursa Komite Audit & Komisaris Independen ===============
wa3a = wa("Halo FA Indonesia, perusahaan kami mencari anggota Komite Audit / Komisaris Independen. Nama perusahaan: ... Status: Tbk / pra-IPO / lainnya.")
wa3b = wa("Halo FA Indonesia, saya ingin mendaftar ke Bursa Komite Audit dan Komisaris Independen. Latar belakang: ...")
main3 = ('<div class="nx-hero"><p class="eyebrow">Tata Kelola · Bursa Independen</p>'
 '<h1>Anggota Komite Audit dan Komisaris Independen untuk Emiten dan Calon Emiten</h1>'
 '<p class="nx-lede">Kami mempertemukan perusahaan Tbk, pra-IPO, BUMD, dan grup rumah sakit dengan profesional independen yang memenuhi syarat OJK.</p>'
 '<div class="nx-btns"><a class="btn solid" href="%s" target="_blank" rel="noopener">Saya Perusahaan</a><a class="btn line" href="%s" target="_blank" rel="noopener">Saya Profesional</a></div></div>' % (wa3a, wa3b) +
 '<section class="nx-sec"><h2>Syarat Utama Komite Audit</h2><div class="nx-facts">'
 '<div class="nx-fact"><b>3 Orang</b><span>Minimal anggota, dari Komisaris Independen dan pihak luar</span></div>'
 '<div class="nx-fact"><b>Ketua</b><span>Dijabat Komisaris Independen</span></div>'
 '<div class="nx-fact"><b>1 Akuntansi</b><span>Minimal satu anggota berlatar akuntansi dan keuangan</span></div></div>'
 '<p class="nx-src">Dasar: POJK 55/POJK.04/2015 tentang Komite Audit dan POJK 33/POJK.04/2014 tentang Direksi dan Dewan Komisaris Emiten atau Perusahaan Publik.</p></section>'
 '<section class="nx-sec"><h2>Profil di Bursa</h2>' + cards([
   ("Akuntansi", "CPA dan Akuntan Publik", "Pernah memimpin atau mereview audit laporan keuangan."),
   ("Akademik", "Doktor dan Kandidat Doktor Akuntansi", "Dosen dan peneliti audit, pengungkapan, dan tata kelola."),
   ("Manajemen", "Mantan CFO dan Direktur Keuangan", "Paham kredit bank, IPO, dan pengendalian internal dari sisi manajemen."),
   ("Risiko", "Praktisi Hukum dan Manajemen Risiko", "Untuk Komite Pemantau Risiko dan kepatuhan.")], "nx-grid g4") + '</section>'
 '<section class="nx-sec"><h2>Alur untuk Perusahaan</h2>' + flow([
   ("Profil Kebutuhan", "Status perusahaan, industri, dan posisi yang kosong."),
   ("Shortlist 3 Kandidat", "Lengkap dengan uji independensi dan rangkap jabatan."),
   ("Wawancara", "Bersama Dewan Komisaris dan Direksi."),
   ("Pengangkatan", "Keputusan Dewan Komisaris atau RUPS, lalu onboarding piagam komite.")]) + '</section>'
 '<section class="nx-sec"><h2>Untuk Profesional</h2><p class="nx-lede" style="margin-bottom:18px">Kirim CV, sertifikasi, dan daftar jabatan saat ini. Profil yang memenuhi syarat masuk bursa dan dihubungi saat ada kebutuhan yang cocok.</p>'
 '<div class="nx-btns"><a class="btn line" href="mailto:ananta@faindonesia.co.id?subject=Daftar%20Bursa%20Komite%20Audit">Kirim CV via Email</a><a class="btn line" href="/konsultan-persiapan-ipo/">Persiapan IPO</a></div></section>')
faq3 = [("Berapa minimal anggota Komite Audit perusahaan Tbk?", "Minimal tiga orang yang berasal dari Komisaris Independen dan pihak dari luar emiten, diketuai Komisaris Independen, sesuai POJK 55/POJK.04/2015."),
        ("Apakah anggota Komite Audit harus akuntan?", "Minimal satu anggota wajib berlatar belakang pendidikan dan keahlian di bidang akuntansi dan keuangan."),
        ("Kapan perusahaan pra-IPO perlu membentuk Komite Audit?", "Sebelum pernyataan pendaftaran efektif. Idealnya sejak tahap persiapan, agar piagam dan rapat komite sudah berjalan saat due diligence."),
        ("Apakah profesional dikenakan biaya untuk mendaftar?", "Tidak. Pendaftaran ke bursa tidak dipungut biaya.")]
page("bursa-komite-audit", "Bursa Komite Audit dan Komisaris Independen | FA Indonesia",
     "Cari anggota Komite Audit dan Komisaris Independen untuk perusahaan Tbk, pra-IPO, BUMD, dan rumah sakit: CPA, akademisi akuntansi, dan mantan CFO yang memenuhi syarat OJK.", main3, faq3)

# =============== Integrasi: Layanan, sitemap, llms ===============
lp = os.path.join(B, "layanan", "index.html"); t = open(lp, encoding="utf-8").read()
if "<!--fa-trio-svc-->" not in t:
    blk = ('<!--fa-trio-svc--><section class="block"><div class="wrap"><div class="head"><p class="eyebrow">Baru</p><h2>Skor Kredit, Back-Office KAP, dan Bursa Independen</h2></div>'
           '<p class="t" style="max-width:62em">Cek kesiapan kredit bank dalam 2 menit, tambah kapasitas audit KAP di musim sibuk, atau temukan anggota Komite Audit dan Komisaris Independen.</p>'
           '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn solid" href="/bankability-index/">FA Bankability Index</a>'
           '<a class="btn line" href="/audit-back-office-kap/">Audit Back-Office KAP</a><a class="btn line" href="/bursa-komite-audit/">Bursa Komite Audit</a></div></div></section><!--/fa-trio-svc-->')
    t = t.replace('<main id="top">', '<main id="top">' + blk, 1); open(lp, "w", encoding="utf-8").write(t)
sp = os.path.join(B, "sitemap.xml"); t = open(sp, encoding="utf-8").read()
for s in ("bankability-index", "audit-back-office-kap", "bursa-komite-audit"):
    u = SITE + "/" + s + "/"
    if u not in t: t = t.replace("</urlset>", "<url><loc>%s</loc><lastmod>2026-11-02</lastmod></url></urlset>" % u)
open(sp, "w", encoding="utf-8").write(t)
lp = os.path.join(B, "llms.txt"); t = open(lp, encoding="utf-8").read()
if "bankability-index" not in t:
    t += ("\n## Layanan Baru (Nov 2026)\n- [FA Bankability Index](%s/bankability-index/): skor 0 sampai 100 kesiapan kredit bank, segmen bank, dan 3 celah.\n"
          "- [Audit Back-Office untuk KAP](%s/audit-back-office-kap/): FA Saturn dan tim kertas kerja di bawah supervisi Partner KAP.\n"
          "- [Bursa Komite Audit dan Komisaris Independen](%s/bursa-komite-audit/): mempertemukan emiten dan calon emiten dengan profesional independen.\n") % (SITE, SITE, SITE)
    open(lp, "w", encoding="utf-8").write(t)
for f, href, label in (("mitra-rm-bank", "/bankability-index/", "FA Bankability Index"), ("mitra-kap-kja", "/audit-back-office-kap/", "Audit Back-Office untuk KAP")):
    p = os.path.join(B, f, "index.html"); t = open(p, encoding="utf-8").read()
    if href not in t:
        em = '<a class="btn line" href="mailto:ananta@faindonesia.co.id?subject=Kerja%20Sama%20Mitra%20FA%20Indonesia">Email Kerja Sama</a>'
        t = t.replace(em, em + '<a class="btn line" href="%s">%s</a>' % (href, label), 1)
        open(p, "w", encoding="utf-8").write(t); print("link", f, href in t)
