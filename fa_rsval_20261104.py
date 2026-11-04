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
</style>"""

def sel(i, label, opts, sm=""):
    o = "".join('<option value="%s"%s>%s</option>' % (v, ' selected' if s else '', t) for v, t, s in opts)
    return '<label>%s%s<select id="%s">%s</select></label>' % (label, (' <small>%s</small>' % sm) if sm else '', i, o)

def inp(i, label, val="", unit="", sm="", ph="", typ="text"):
    box = '<input id="%s" inputmode="decimal" type="%s" value="%s"%s>' % (i, typ, val, (' placeholder="%s"' % ph) if ph else '')
    if unit: box = '<span class="rv-u" data-u="%s">%s</span>' % (unit, box)
    return '<label>%s%s%s</label>' % (label, (' <small>%s</small>' % sm) if sm else '', box)

CSS2 = r"""<style>
.rv-ck{display:flex;flex-direction:column;gap:8px}
.rv-ck label{display:flex;gap:12px;align-items:flex-start;cursor:pointer;border:1px solid #3a3a3a;background:var(--paper);border-radius:12px;padding:12px 14px;font-size:14.5px;line-height:1.4;transition:border-color .2s}
.rv-ck label:hover{border-color:#888}
.rv-ck input{width:18px;height:18px;flex:none;margin-top:1px;accent-color:#fff}
.rv-ck b{font-weight:600}.rv-ck small{display:block;color:var(--muted);font-size:12.5px;margin-top:2px}
.rv-ck label.na{opacity:.45}
.rv-ba{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:4px 0 14px}
.rv-ba>div{border:1px solid var(--line);border-radius:14px;padding:14px;background:#1b1b1b}
.rv-ba>div.af{border-color:#fff;background:#232323}
.rv-ba .rv-k{font-size:11px}.rv-ba small{display:block;color:var(--muted);font-size:12px;line-height:1.4;margin-top:2px}
.rv-ba .rv-big{font-size:clamp(19px,1.9vw,24px);margin:8px 0 0}
.rv-bar{margin:6px 0 4px}.rv-bar div{display:flex;align-items:center;gap:10px;font-size:12.5px;color:var(--muted);margin:6px 0}
.rv-bar span{width:58px;flex:none}.rv-bar i{flex:1;height:10px;border-radius:10px;background:#2a2a2a;overflow:hidden;display:block}
.rv-bar s{display:block;height:100%;width:0;border-radius:10px;transition:width .8s var(--ez)}
#rv_bb{background:#6f6f6f}#rv_ba{background:#fff}
.rv-up{border:1px solid #fff;border-radius:14px;padding:14px 16px;margin:12px 0 4px;text-align:center}
.rv-up .rv-big{margin:4px 0 2px;font-size:clamp(24px,2.8vw,32px)}
.rv-up small{color:var(--muted);font-size:12.5px}
.rv-det{margin-top:10px}.rv-det summary{cursor:pointer;color:var(--muted);font-size:13.5px}
@media (max-width:420px){.rv-ba{grid-template-columns:1fr}}
#rv_rep{display:none}
@media print{body>*:not(#rv_rep){display:none!important}html,body{background:#fff!important}#rv_rep{display:block!important;position:static;width:100%;background:#fff;color:#111;font:12.5px/1.5 'Source Sans 3',Arial,sans-serif;padding:0 6mm}#rv_rep h1{font:600 22px Georgia,serif;margin:0 0 4px}#rv_rep h2{font:600 15px Arial,sans-serif;margin:16px 0 6px;border-bottom:1px solid #999;padding-bottom:3px}#rv_rep table{width:100%;border-collapse:collapse;margin:4px 0}#rv_rep td,#rv_rep th{border:1px solid #bbb;padding:5px 7px;text-align:left;vertical-align:top}#rv_rep th{background:#eee}#rv_rep .s{color:#555;font-size:11px}#rv_rep .big{font-size:18px;font-weight:700}@page{margin:14mm}}
</style>"""

FORM = ('<form class="rv-card" id="rvf" onsubmit="return false">'
  '<p class="rv-note">Angka perkiraan juga boleh. Nilai uang dalam Rp miliar, contoh 2,5 berarti Rp2,5 miliar.</p>'
  '<div class="rv-blk"><p class="rv-h">1. Profil Rumah Sakit</p><div class="rv-f">'
  + sel("jenis", "Jenis RS", [("rsu", "RS Umum", False), ("rsia", "RS Ibu dan Anak (RSIA)", True), ("rsk", "RS Khusus Lain (Bedah, Mata, dll)", False)])
  + sel("kelas", "Kelas", [("b", "B", False), ("c", "C", True), ("d", "D", False)])
  + inp("tt", "Jumlah Tempat Tidur", "80", "TT")
  + inp("bor", "BOR Rata-Rata", "45", "%")
  + sel("akr", "Akreditasi", [("1.06", "Paripurna", False), ("1.0", "Utama", True), ("0.95", "Madya atau Dasar", False), ("0.85", "Belum atau Habis", False)])
  + sel("bpjs", "Kerja Sama BPJS", [("aktif", "Aktif", False), ("proses", "Sedang Perpanjangan", False), ("putus", "Diputus atau Kena Sanksi", True), ("non", "Tidak Kerja Sama", False)])
  + '</div></div><div class="rv-blk"><p class="rv-h">2. Keuangan Setahun Terakhir</p><div class="rv-f">'
  + inp("rev", "Pendapatan", "30", "miliar")
  + inp("ebitda", "EBITDA", "1,5", "miliar", "laba sebelum bunga, pajak, penyusutan")
  + sel("aud", "Laporan Keuangan", [("0", "Belum Diaudit", True), ("1", "Sudah Diaudit KAP", False)])
  + '</div></div><div class="rv-blk"><p class="rv-h">3. Aset, Utang, dan Saham</p><div class="rv-f">'
  + sel("lahan", "Lahan dan Gedung", [("milik", "Milik Sendiri", True), ("sewa", "Sewa", False)])
  + inp("umur", "Umur Gedung", "6", "tahun")
  + inp("apr", "Nilai Appraisal KJPP atau Bank", "", "miliar", "opsional", "jika ada")
  + inp("utang", "Utang Bank", "10", "miliar")
  + inp("porsi", "Porsi Saham yang Dijual", "100", "%")
  + '</div></div><div class="rv-blk"><p class="rv-h">4. Treatment FA Indonesia Sebelum Dijual</p>'
  '<p class="rv-note" style="margin-bottom:10px">Centang perbaikan yang ingin disimulasikan. Hasilnya menjadi kolom After.</p><div class="rv-ck">'
  '<label id="lb_bpjs"><input type="checkbox" id="t_bpjs" checked><span><b>Pulihkan Kerja Sama BPJS dan Akreditasi</b><small>Tutup temuan, perbarui izin dan akreditasi, ajukan kredensialing ulang</small></span></label>'
  '<label><input type="checkbox" id="t_mrg" checked><span><b>Efisiensi Biaya dan Unit Cost</b><small>Unit cost per layanan, tarif, belanja obat dan alkes, struktur SDM</small></span></label>'
  '<label id="lb_bor"><input type="checkbox" id="t_bor" checked><span><b>Naikkan Okupansi</b><small>Jejaring rujukan, dokter spesialis kunci, kerja sama asuransi dan perusahaan</small></span></label>'
  '<label id="lb_aud"><input type="checkbox" id="t_aud" checked><span><b>Audit KAP dan Data Room</b><small>Laporan keuangan audited, normalisasi EBITDA, teaser, data room siap due diligence</small></span></label>'
  '<label><input type="checkbox" id="t_prs" checked><span><b>Proses Penjualan Kompetitif</b><small>Ditawarkan ke beberapa grup RS dan investor sekaligus dengan NDA, bukan menunggu satu pembeli</small></span></label>'
  '</div></div></form>')

RES = ('<aside id="rvr" aria-live="polite">'
  '<div class="rv-k">Estimasi Harga Saham yang Dijual</div>'
  '<div class="rv-ba"><div><div class="rv-k">Before</div><small>Dijual apa adanya, dihitung sebagai properti</small><div class="rv-big" id="rv_b">-</div></div>'
  '<div class="af"><div class="rv-k">After</div><small>Setelah treatment FA Indonesia</small><div class="rv-big" id="rv_a">-</div></div></div>'
  '<div class="rv-bar"><div><span>Before</span><i><s id="rv_bb"></s></i></div><div><span>After</span><i><s id="rv_ba"></s></i></div></div>'
  '<div class="rv-up"><div class="rv-k">Potensi Kenaikan Harga</div><div class="rv-big" id="rv_up">-</div><small id="rv_upx"></small></div>'
  '<ul class="rv-fl" id="rv_fl"></ul>'
  '<details class="rv-det"><summary>Rincian Perhitungan</summary>'
  '<div class="rv-row"><span>Nilai sebagai properti</span><b id="rv_prop">-</b></div>'
  '<div class="rv-row"><span>Nilai usaha saat ini</span><b id="rv_inc">-</b></div>'
  '<div class="rv-row"><span>EBITDA after</span><b id="rv_eba">-</b></div>'
  '<div class="rv-row"><span>Nilai usaha after</span><b id="rv_inca">-</b></div>'
  '<div class="rv-row"><span>Dikurangi utang bank</span><b id="rv_dbt">-</b></div></details>'
  '<div class="rv-act"><a class="btn solid" href="https://wa.me/%s" id="rv_wa" rel="noopener" target="_blank">Diskusikan Treatment via WhatsApp</a>'
  '<button class="btn line" type="button" id="rv_pdf" data-fa-full>Unduh Laporan Lengkap dan Strategi</button></div>'
  '<p class="rv-sm">Estimasi indikatif. Kolom After adalah skenario setelah perbaikan 6 sampai 18 bulan, bukan jaminan harga. Harga akhir ditentukan due diligence, penilaian KJPP, dan negosiasi dengan pembeli.</p>'
  '</aside><div id="rv_rep" aria-hidden="true"></div>') % WA

SAFE = ('<div class="rv-safe"><span>Dihitung di Browser, Tidak Disimpan di Server</span><span>Estimasi Indikatif, Bukan Laporan Penilaian KJPP</span>'
  '<span>Data RS Dibuka ke Investor Hanya Setelah NDA</span><span>Untuk RS yang Sulit Laku atau Bermasalah dengan BPJS</span></div>')

HOW = ('<section class="rv-sec"><h2>Kenapa RS Sulit Laku, dan Apa yang Mengubah Harganya</h2><div class="rv-3">'
  '<div><em>Before</em><b>Dijual Apa Adanya</b><p>Kalau kinerja turun atau kerja sama BPJS putus, pembeli tidak membeli usaha. Mereka menghitung tanah, gedung, dan alat, lalu memberi diskon karena harus memulihkan RS sendiri.</p></div>'
  '<div><em>Treatment</em><b>Dibenahi Sebelum Ditawarkan</b><p>Pulihkan BPJS dan akreditasi, rapikan unit cost, naikkan okupansi, audit laporan keuangan, dan siapkan data room. Risiko yang tadinya ditanggung pembeli diselesaikan lebih dulu.</p></div>'
  '<div><em>After</em><b>Dijual Sebagai Usaha</b><p>RS dinilai dari EBITDA yang pulih dikali multiple transaksi, lalu ditawarkan ke beberapa pembeli sekaligus. Selisih before dan after adalah ruang yang bisa diperjuangkan pemilik.</p></div>'
  '</div></section>')

CTA = ('<section class="rv-sec"><div class="rv-cta"><div><h2>RS Belum Ketemu Pembeli?</h2>'
  '<p>FA Indonesia mendampingi pemilik RS dari sisi penjual: memetakan masalah, menjalankan treatment bersama tim RS, menyusun data room, lalu menawarkan ke grup RS dan investor setelah NDA sampai closing.</p></div>'
  '<div class="bt"><a class="btn solid" href="https://wa.me/%s?text=%s" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
  '<a class="btn line" href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a></div></div></section>') % (
  WA, "Halo%2C%20saya%20ingin%20konsultasi%20penjualan%20rumah%20sakit.")

FAQ = [("Kenapa rumah sakit saya dijual tapi tidak ada pembeli?", "Biasanya karena pembeli melihat risiko yang harus mereka tanggung sendiri: kerja sama BPJS putus, akreditasi habis, okupansi rendah, laporan keuangan belum diaudit, atau utang besar. Mereka lalu hanya mau membayar seharga properti. Risiko ini bisa dibenahi sebelum RS ditawarkan."),
       ("Apa beda harga before dan after di kalkulator ini?", "Before adalah harga bila RS dijual apa adanya, yang umumnya dihitung sebagai properti (tanah, gedung, alat) dengan diskon. After adalah skenario setelah treatment: BPJS dan akreditasi pulih, biaya efisien, okupansi naik, laporan diaudit, dan proses penjualan kompetitif, sehingga RS dinilai sebagai usaha dari EBITDA-nya."),
       ("Berapa lama treatment sebelum RS siap dijual?", "Umumnya 6 sampai 18 bulan, tergantung masalahnya. Pemulihan kerja sama BPJS dan akreditasi biasanya paling menentukan waktu."),
       ("Apakah RS yang kerja sama BPJS-nya diputus masih bisa dijual?", "Bisa. Dijual apa adanya, harganya mendekati nilai properti. Bila kerja sama dipulihkan dulu, RS bisa dinilai kembali sebagai usaha dengan harga yang jauh lebih baik."),
       ("Apakah harga After dijamin?", "Tidak. After adalah skenario indikatif. Hasil nyata bergantung pada keberhasilan perbaikan, kondisi pasar, due diligence, dan negosiasi dengan pembeli."),
       ("Apakah data RS saya aman?", "Kalkulator berjalan di browser Anda dan tidak menyimpan data di server FA. Data hanya terkirim bila Anda menekan tombol WhatsApp, dan informasi RS baru ditawarkan ke calon pembeli setelah NDA ditandatangani.")]

SEO = ('<section class="rv-sec"><details class="rv-more"><summary>Tentang Kalkulator Valuasi Rumah Sakit FA</summary>'
  '<p>Banyak pemilik rumah sakit swasta ingin menjual RS tetapi tidak ketemu pembeli atau investor, atau hanya ditawar seharga tanah dan gedung. Kalkulator ini membandingkan dua angka: harga jual rumah sakit bila dijual apa adanya, dan harga setelah RS dibenahi lebih dulu.</p>'
  '<p>Treatment yang disimulasikan mengikuti hal yang paling sering membuat pembeli mundur: kerja sama BPJS yang diputus, akreditasi habis, unit cost dan biaya yang tidak terkendali, okupansi rendah, laporan keuangan belum diaudit, dan penjualan yang hanya ditawarkan ke satu pihak. '
  'FA Indonesia mendampingi penjualan rumah sakit, RSIA, dan RS khusus dari sisi penjual sampai closing, bersama KAP dan KJPP mitra.</p></details></section>')

JS = r"""<script>
(function(){
var WA="__WA__",$=function(i){return document.getElementById(i)};
function num(i){var v=($(i).value||"").toString().trim().replace(/\./g,"").replace(",",".");if(v==="")return null;v=parseFloat(v);return isNaN(v)?null:v}
function fmt(v){if(v===null||!isFinite(v))return"-";var a=Math.abs(v),s=a<10?a.toFixed(1):Math.round(a).toString();return(v<0?"-":"")+"Rp"+s.replace(".",",")+" M"}
function rng(a,b){if(a===null||b===null)return"-";if(Math.abs(a-b)<0.05)return fmt(a);if(a>=0&&b>=0)return fmt(a).replace(" M","")+" sampai "+fmt(b).replace("Rp","");return fmt(a)+" sampai "+fmt(b)}
function ck(i){return $(i).checked}
var perTT={rsu:1.0,rsia:0.8,rsk:0.9},kelasAdj={b:1.1,c:1.0,d:0.9},bpjsAdj={aktif:1.0,proses:0.85,putus:0.55,non:0.8},
lbl={rsu:"RS Umum",rsia:"RSIA",rsk:"RS Khusus"},bt={aktif:"Aktif",proses:"Sedang perpanjangan",putus:"Diputus / sanksi",non:"Tidak kerja sama"};

var STR={
 bpjs:["Pulihkan Kerja Sama BPJS dan Akreditasi","3 sampai 9 bulan",["Petakan penyebab pemutusan atau sanksi dan hitung nilai kewajiban klaim yang masih terbuka.","Sepakati penyelesaian atau skema angsuran pengembalian klaim dengan BPJS Kesehatan.","Perbarui izin operasional dan akreditasi, minimal tingkat Utama.","Ajukan kredensialing ulang ke kantor cabang BPJS Kesehatan dengan dokumen yang sudah lengkap."]],
 mrg:["Efisiensi Biaya dan Unit Cost","3 sampai 6 bulan",["Hitung unit cost per layanan dan bandingkan dengan tarif INA-CBG dan tarif umum.","Renegosiasi pembelian obat, BMHP, dan alkes; tertibkan stok.","Tata ulang struktur SDM dan skema jasa medis sesuai volume.","Sesuaikan tarif umum dan paket layanan yang marginnya tipis."]],
 bor:["Naikkan Okupansi","6 sampai 12 bulan",["Kunci dokter spesialis utama dengan kontrak jangka panjang.","Bangun jejaring rujukan dari FKTP, bidan, dan klinik sekitar.","Perluas kerja sama asuransi dan perusahaan.","Tonjolkan satu atau dua layanan unggulan yang paling dicari di wilayah."]],
 aud:["Audit KAP dan Data Room","2 sampai 4 bulan",["Audit laporan keuangan oleh KAP mitra; penyusun dan auditor selalu pihak berbeda.","Normalisasi EBITDA: gaji pemilik, biaya pribadi, pos sekali terjadi.","Penilaian KJPP atas tanah, gedung, dan alat.","Data room: legalitas, izin, kontrak dokter dan BPJS, aset, utang, perkara."]],
 prs:["Proses Penjualan Kompetitif","3 sampai 6 bulan",["Teaser tanpa nama RS dan daftar panjang calon pembeli: grup RS, private equity, kelompok dokter, investor strategis.","NDA, lalu buka data room ke pembeli yang serius.","Kumpulkan penawaran awal, pilih yang terbaik untuk due diligence.","Negosiasi struktur (saham, aset, atau KSO) dan penandatanganan jual beli."]]};
function report(R){
 var h='<h1>Laporan Valuasi dan Strategi Penjualan Rumah Sakit</h1><div class="s">FA Venus · Valuasi Rumah Sakit · faindonesia.co.id · '+new Date().toLocaleDateString("id-ID",{day:"numeric",month:"long",year:"numeric"})+'</div>';
 h+='<h2>Ringkasan</h2><table><tr><th>Skenario</th><th>Harga saham dijual ('+R.porsi+'%)</th></tr><tr><td>Before: dijual apa adanya, dihitung sebagai properti</td><td class="big">'+R.b+'</td></tr><tr><td>After: setelah treatment FA Indonesia</td><td class="big">'+R.a+'</td></tr><tr><td>Potensi kenaikan (nilai tengah)</td><td class="big">'+R.up+'</td></tr></table>';
 h+='<h2>Profil dan Data yang Diisi</h2><table>'+R.rows.map(function(r){return'<tr><th style="width:38%">'+r[0]+'</th><td>'+r[1]+'</td></tr>'}).join("")+'</table>';
 h+='<h2>Rincian Perhitungan</h2><table>'+R.calc.map(function(r){return'<tr><th style="width:38%">'+r[0]+'</th><td>'+r[1]+'</td></tr>'}).join("")+'</table>';
 h+='<h2>Temuan Utama</h2><ul>'+R.flags.map(function(x){return'<li>'+x+'</li>'}).join("")+'</ul>';
 h+='<h2>Strategi Treatment Sebelum Dijual</h2>';
 R.tr.forEach(function(k,i){var s=STR[k];h+='<p><b>'+(i+1)+'. '+s[0]+'</b> <span class="s">(perkiraan '+s[1]+')</span></p><ol>'+s[2].map(function(x){return'<li>'+x+'</li>'}).join("")+'</ol>'});
 if(!R.tr.length)h+='<p>Belum ada treatment yang dipilih.</p>';
 h+='<h2>Checklist Data Awal untuk Calon Pembeli</h2><ol><li>Profil RS: kelas, tempat tidur, akreditasi, kerja sama BPJS, tahun berdiri.</li><li>Laporan keuangan 3 tahun terakhir dan tahun berjalan.</li><li>Data operasional: BOR, kunjungan, persalinan atau tindakan utama, porsi BPJS dan umum.</li><li>Struktur kepemilikan, porsi saham dijual, status lahan dan gedung, utang bank.</li><li>Surat dan hasil audit BPJS bila ada masalah kerja sama.</li><li>Laporan KJPP atau appraisal bank atas aset.</li></ol>';
 h+='<p class="s">Estimasi indikatif berdasarkan data yang diisi dan benchmark transaksi RS swasta di Indonesia. Skenario After bukan jaminan harga; hasil nyata ditentukan keberhasilan perbaikan, due diligence, penilaian KJPP, dan negosiasi. FA Indonesia tidak menghimpun dana masyarakat. Diskusi lanjutan: tim FA Indonesia via WhatsApp di faindonesia.co.id.</p>';
 var rp=$("rv_rep");if(rp.parentNode!==document.body)document.body.appendChild(rp);rp.innerHTML=h}
var LAST=null;
function calc(){
 var jenis=$("jenis").value,kelas=$("kelas").value,tt=num("tt")||0,bor=num("bor"),akr=parseFloat($("akr").value),bpjs=$("bpjs").value,
 rev=num("rev")||0,eb=num("ebitda"),aud=$("aud").value==="1",lahan=$("lahan").value,umur=num("umur")||0,apr=num("apr"),utang=num("utang")||0,
 po=Math.min(100,Math.max(1,num("porsi")||100))/100,sw=lahan==="sewa"?0.9:1;
 // nilai aset dasar
 var base,ap=false;if(apr!==null&&apr>0){base=apr;ap=true}else{base=tt*perTT[jenis]*Math.max(0.5,1-0.025*umur);if(lahan==="sewa")base*=0.3}
 // BEFORE: dijual apa adanya
 var pL=base*0.55,pH=base*0.75,adjN=kelasAdj[kelas]*akr*bpjsAdj[bpjs]*sw*(aud?1:0.85),iL=null,iH=null;
 if(eb!==null&&eb>0){iL=eb*4*adjN;iH=eb*6*adjN}
 var bL=Math.max(pL,iL||0)-utang,bH=Math.max(pH,iH||0)-utang;
 // AFTER: setelah treatment
 var tB=ck("t_bpjs"),tM=ck("t_mrg"),tO=ck("t_bor"),tA=ck("t_aud"),tP=ck("t_prs");
 var bpA=tB?"aktif":bpjs,akA=tB?Math.max(akr,1.0):akr,revA=rev;
 if(tB&&bpjs==="putus")revA*=1.25;else if(tB&&bpjs==="proses")revA*=1.1;else if(tB&&bpjs==="non")revA*=1.15;
 var borA=bor;if(tO&&bor!==null&&bor<65){revA*=Math.min(1.3,65/Math.max(bor,20));borA=65}
 var m=rev>0&&eb!==null?eb/rev:0,mA=m;if(tM)mA=m<=0?0.10:Math.max(m,Math.min(m+0.05,0.17));
 var ebA=revA*mA,audA=aud||tA,adjA=kelasAdj[kelas]*akA*bpjsAdj[bpA]*sw*(audA?1:0.85)*(borA!==null&&borA>=75?1.05:1);
 var mL=4.5+(tA?0.5:0)+(tP?0.5:0),mH=6.5+(tA?0.5:0)+(tP?1:0),aiL=null,aiH=null;
 if(ebA>0){aiL=ebA*mL*adjA;aiH=ebA*mH*adjA}
 var gL=base*(tP?0.85:0.75),gH=base*(tP?1:0.85);
 var aL=Math.max(gL,aiL||0)-utang,aH=Math.max(gH,aiH||0)-utang;
 if(aL<bL)aL=bL;if(aH<bH)aH=bH;
 var sbL=bL*po,sbH=bH*po,saL=aL*po,saH=aH*po;
 $("rv_b").textContent=rng(sbL,sbH);$("rv_a").textContent=rng(saL,saH);
 var bm=(sbL+sbH)/2,am=(saL+saH)/2,mx=Math.max(am,bm,0.1);
 $("rv_bb").style.width=Math.max(2,bm/mx*100)+"%";$("rv_ba").style.width=Math.max(2,am/mx*100)+"%";
 var up=am-bm;$("rv_up").textContent=up>0.05?"+"+fmt(up):"Rp0";
 $("rv_upx").textContent=(up>0.05&&bm>0.1)?"Sekitar "+(am/bm).toFixed(1).replace(".",",")+" kali harga before (nilai tengah)":(bm<=0.1&&up>0.05?"Before belum menutup utang bank":"Pilih treatment untuk melihat selisih");
 $("rv_prop").textContent=rng(pL,pH)+(ap?" (appraisal)":"");
 $("rv_inc").textContent=iL===null?"Tidak relevan (EBITDA negatif)":rng(iL,iH);
 $("rv_eba").textContent=fmt(ebA)+" (margin "+Math.round(mA*100)+"%)";
 $("rv_inca").textContent=aiL===null?"-":rng(aiL,aiH);
 $("rv_dbt").textContent=utang?"- "+fmt(utang):"Rp0";
 $("lb_bpjs").classList.toggle("na",bpjs==="aktif"&&akr>=1);
 $("lb_aud").classList.toggle("na",aud&&false);
 $("lb_bor").classList.toggle("na",bor!==null&&bor>=65);
 var f=[];
 if(bpjs==="putus")f.push(["dn","Kerja sama BPJS diputus: pembeli hanya menghitung properti. Pemulihan BPJS adalah pengungkit harga terbesar."]);
 if(bpjs==="proses")f.push(["in","Perpanjangan BPJS belum final: pembeli biasanya menunggu kontrak baru terbit."]);
 if(akr<1)f.push(["dn","Akreditasi belum Utama: perpanjangan dan peningkatan akreditasi membuka kembali kerja sama BPJS dan asuransi."]);
 if(bor!==null&&bor<50)f.push(["in","BOR "+bor+"%: kapasitas menganggur. Okupansi yang naik langsung menaikkan EBITDA."]);
 if(eb!==null&&eb<=0)f.push(["dn","EBITDA negatif: dijual apa adanya hanya laku seharga aset. Efisiensi biaya mengubah RS kembali menjadi usaha."]);
 else if(m>0&&m<0.12)f.push(["in","Margin EBITDA "+Math.round(m*100)+"%: di bawah RS swasta yang sehat, ruang efisiensi masih ada."]);
 if(!aud)f.push(["in","Laporan keuangan belum diaudit: pembeli memberi diskon risiko. Audit KAP menghapus diskon ini."]);
 if(bL<0)f.push(["dn","Harga before belum menutup utang bank: tanpa treatment, penjualan berisiko tidak menghasilkan apa pun bagi pemilik."]);
 if(!ap)f.push(["in","Belum ada appraisal: nilai aset diestimasi dari benchmark per tempat tidur."]);
 var ic={up:"+",dn:"!",in:"i"};
 $("rv_fl").innerHTML=f.slice(0,4).map(function(x){return'<li class="'+x[0]+'"><i>'+ic[x[0]]+'</i><span>'+x[1]+'</span></li>'}).join("");
 var tr=[];if(tB)tr.push("pulihkan BPJS/akreditasi");if(tM)tr.push("efisiensi biaya");if(tO)tr.push("naikkan okupansi");if(tA)tr.push("audit + data room");if(tP)tr.push("proses kompetitif");
 var msg="Halo, saya ingin konsultasi penjualan rumah sakit.\n\n"+
  "Jenis: "+lbl[jenis]+" kelas "+kelas.toUpperCase()+" | TT: "+tt+" | BOR: "+(bor===null?"-":bor)+"%\n"+
  "Akreditasi: "+$("akr").options[$("akr").selectedIndex].text+" | BPJS: "+bt[bpjs]+"\n"+
  "Pendapatan: Rp"+rev+" M | EBITDA: Rp"+(eb===null?"-":eb)+" M | LK: "+(aud?"audited":"belum audit")+"\n"+
  "Lahan dan gedung: "+(lahan==="milik"?"Milik sendiri":"Sewa")+" | Utang bank: Rp"+utang+" M | Porsi dijual: "+Math.round(po*100)+"%\n"+
  "Before (apa adanya): "+rng(sbL,sbH)+"\nAfter (treatment FA): "+rng(saL,saH)+"\nTreatment: "+(tr.join(", ")||"-");
 $("rv_wa").href="https://wa.me/"+WA+"?text="+encodeURIComponent(msg);
 var keys=[];if(tB)keys.push("bpjs");if(tM)keys.push("mrg");if(tO)keys.push("bor");if(tA)keys.push("aud");if(tP)keys.push("prs");
 LAST={b:rng(sbL,sbH),a:rng(saL,saH),up:up>0.05?"+"+fmt(up):"Rp0",porsi:Math.round(po*100),tr:keys,flags:f.map(function(x){return x[1]}),
  rows:[["Jenis dan kelas",lbl[jenis]+" kelas "+kelas.toUpperCase()],["Tempat tidur dan BOR",tt+" TT, BOR "+(bor===null?"-":bor+"%")],["Akreditasi",$("akr").options[$("akr").selectedIndex].text],["Kerja sama BPJS",bt[bpjs]],["Pendapatan dan EBITDA",fmt(rev)+" dan "+(eb===null?"-":fmt(eb))],["Laporan keuangan",aud?"Sudah diaudit KAP":"Belum diaudit"],["Lahan dan gedung",(lahan==="milik"?"Milik sendiri":"Sewa")+", umur "+umur+" tahun"],["Utang bank","Rp"+utang+" M"]],
  calc:[["Nilai sebagai properti",rng(pL,pH)+(ap?" (dari appraisal)":" (benchmark per TT)")],["Nilai usaha saat ini",iL===null?"Tidak relevan, EBITDA negatif":rng(iL,iH)],["Pendapatan after",fmt(revA)],["EBITDA after",fmt(ebA)+", margin "+Math.round(mA*100)+"%"],["Multiple after",mL.toFixed(1).replace(".",",")+" sampai "+mH.toFixed(1).replace(".",",")+" kali"],["Nilai usaha after",aiL===null?"-":rng(aiL,aiH)],["Utang bank dikurangkan","Rp"+utang+" M"]]};
}
var t0=0;function track(){if(t0)return;t0=1;try{if(window.gtag)gtag("event","rsval_calc",{jenis:$("jenis").value,bpjs:$("bpjs").value})}catch(e){}}
var els=document.querySelectorAll("#rvf input,#rvf select");for(var i=0;i<els.length;i++){els[i].addEventListener("input",function(){calc();track()});els[i].addEventListener("change",calc)}
$("rv_pdf").addEventListener("click",function(){calc();report(LAST);try{if(window.gtag)gtag("event","rsval_pdf",{jenis:$("jenis").value})}catch(e){}setTimeout(function(){window.print()},80)});
$("rv_wa").addEventListener("click",function(){try{if(window.gtag)gtag("event","rsval_wa",{jenis:$("jenis").value,bpjs:$("bpjs").value})}catch(e){}},true);
calc();
})();
</script>""".replace("__WA__", WA)

TBL = ('<section class="rv-sec"><h2>Faktor yang Menaikkan dan Menurunkan Harga RS</h2><div class="rv-tw"><table class="rv-t">'
  '<thead><tr><th>Faktor</th><th>Pengaruh</th><th>Catatan</th></tr></thead><tbody>'
  '<tr><td>Kerja sama BPJS aktif</td><td class="pu">Naik</td><td>Volume pasien terjamin. Sebagian besar pembeli RS di Indonesia mencari RS BPJS.</td></tr>'
  '<tr><td>Kerja sama BPJS diputus</td><td class="pd">Turun tajam</td><td>Harga bergeser ke nilai aset. Isi temuan audit dan kewajiban pengembalian klaim sangat menentukan.</td></tr>'
  '<tr><td>Akreditasi Paripurna</td><td class="pu">Naik</td><td>Mempercepat perizinan dan kerja sama asuransi bagi pembeli.</td></tr>'
  '<tr><td>Lahan dan gedung milik sendiri</td><td class="pu">Naik</td><td>Ada nilai lantai dari aset fisik.</td></tr>'
  '<tr><td>BOR di bawah 50%</td><td class="pu">Netral sampai naik</td><td>Kapasitas menganggur bisa jadi peluang bagi pembeli strategis yang punya jaringan rujukan.</td></tr>'
  '<tr><td>Laporan keuangan belum diaudit</td><td class="pd">Diskon risiko</td><td>Bisa ditutup dengan audit KAP atau financial due diligence sebelum ditawarkan.</td></tr>'
  '</tbody></table></div></section>')


def page():
    t = TPL
    title = "Kalkulator Harga Jual Rumah Sakit: Sebelum dan Sesudah Dibenahi | FA Indonesia"
    desc = "RS dijual tapi belum ada pembeli? Hitung harga jual rumah sakit, RSIA, atau RS khusus bila dijual apa adanya vs setelah dibenahi: BPJS, unit cost, okupansi, audit, data room."
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
         "operatingSystem": "Web", "description": desc, "offers": {"@type": "Offer", "price": "49000", "priceCurrency": "IDR", "description": "Kalkulator gratis; laporan lengkap dan strategi berbayar"},
         "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": SITE + "/"}},
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), t, count=1, flags=re.S)
    t = t.replace(old, url)
    faqh = '<section class="rv-sec"><h2>Pertanyaan Umum Pemilik RS</h2>' + "".join('<details class="rv-more"><summary><b>%s</b></summary><p>%s</p></details>' % (q, a) for q, a in FAQ) + "</section>"
    main = ('<main id="top">' + CSS + CSS2 + '<section class="block"><div class="wrap">'
            '<div class="rv-hero"><p class="eyebrow">FA Venus · Valuasi Rumah Sakit</p><h1>RS Dijual tapi Belum Ada Pembeli? Hitung Harga Before dan After</h1>'
            '<p class="rv-lede">Bandingkan harga RS bila dijual apa adanya dengan harga setelah dibenahi tim FA Indonesia: kerja sama BPJS, unit cost, okupansi, audit, dan data room. Gratis dipakai, hasil langsung muncul.</p></div>'
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
