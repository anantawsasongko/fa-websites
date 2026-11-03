# -*- coding: utf-8 -*-
"""Peta Pendanaan FA (3 Nov 2026): satu alat untuk dua muara FA, kredit bank (usaha menengah) dan investor/VC (UMKM tumbuh).
Hasil: skor, jalur, celah yang perlu ditutup + mitra penutupnya (KJA, KAP, KJPP, notaris, konsultan pajak, tim FA),
checklist data room yang bisa dicentang dan disimpan PDF, lalu kirim ke WA. Teks web dibuat seminimal mungkin; teks SEO dilipat.
Idempoten: halaman ditimpa, sisipan beranda/layanan/bankability memakai marker."""
import os, re, json
R = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(R, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
SITE = "https://faindonesia.co.id"
SLUG = "cek-kesiapan-pendanaan"
WA = "6282245260121"
TPL = open(os.path.join(B, "komite-audit-komisaris-independen", "index.html"), encoding="utf-8").read()

CSS = r"""<style>
.fp-hero{padding-top:8px}.fp-hero h1{margin:.15em 0 .35em;font-size:clamp(30px,4.4vw,54px);line-height:1.08;max-width:15em}
.fp-lede{font-size:clamp(16px,1.6vw,19px);color:var(--muted);max-width:38em;margin:0 0 24px}
.fp-trk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.fp-trk button{all:unset;box-sizing:border-box;cursor:pointer;border:1px solid var(--line);background:var(--surface);border-radius:16px;padding:20px 18px;display:flex;flex-direction:column;gap:6px;transition:border-color .25s,transform .25s var(--ez)}
.fp-trk button:hover{transform:translateY(-2px);border-color:#777}
.fp-trk button b{font-size:18px;line-height:1.25}.fp-trk button span{font-size:13.5px;color:var(--muted);line-height:1.45}
.fp-trk button i{font-style:normal;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
.fp-trk button.on{border-color:#fff;background:#262626}
.fp-trk button:focus-visible{outline:2px solid #fff;outline-offset:2px}
#fp{display:none;margin-top:18px;border:1px solid var(--line);background:var(--surface);border-radius:18px;padding:24px}
#fp.on{display:block;animation:fpUp .6s var(--ez) forwards}
.fp-q{padding:14px 0;border-top:1px solid var(--line)}.fp-q:first-child{border-top:0;padding-top:0}
.fp-q>p{margin:0 0 10px;font-size:15px;font-weight:600}
.fp-ch{display:flex;flex-wrap:wrap;gap:8px}
.fp-ch button{all:unset;box-sizing:border-box;cursor:pointer;border:1px solid #3a3a3a;background:var(--paper);color:#fff;border-radius:999px;padding:9px 14px;font-size:14px;line-height:1.3;transition:background .2s,color .2s,border-color .2s}
.fp-ch button:hover{border-color:#888}.fp-ch button.on{background:#fff;color:#111;border-color:#fff}
.fp-ch button:focus-visible{outline:2px solid #fff;outline-offset:2px}
.fp-go{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:18px}
.fp-cnt{font-size:13px;color:var(--muted)}.fp-err{color:#F08A82;font-size:14px}
#fpr{display:none;margin-top:22px;border:1px solid var(--line);border-radius:18px;padding:26px;background:linear-gradient(160deg,#222,#161616)}
#fpr.on{display:block;animation:fpUp .7s var(--ez) forwards}
.fp-top{display:grid;grid-template-columns:180px 1fr;gap:26px;align-items:center}
.fp-ring{position:relative;width:180px;height:180px}.fp-ring svg{transform:rotate(-90deg)}
.fp-ring circle{fill:none;stroke-width:11}.fp-ring .bg{stroke:#2f2f2f}.fp-ring .fg{stroke:#fff;stroke-linecap:round;transition:stroke-dashoffset 1.4s var(--ez)}
.fp-num{position:absolute;inset:0;display:grid;place-items:center;text-align:center}.fp-num b{font-size:50px;font-weight:500;line-height:1}.fp-num span{display:block;font-size:11px;color:var(--muted);letter-spacing:.12em;text-transform:uppercase;margin-top:4px}
.fp-grade{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
.fp-title{font-size:clamp(22px,2.5vw,30px);margin:.2em 0 .4em;line-height:1.2}
.fp-pills{display:flex;flex-wrap:wrap;gap:8px}.fp-pills span{border:1px solid #fff;border-radius:999px;padding:6px 13px;font-size:13.5px}
.fp-pills span.m{border-color:#555;color:var(--muted)}
.fp-note{border:1px solid #444;border-radius:12px;padding:14px 16px;margin-top:20px;font-size:14.5px;line-height:1.5}
.fp-note .btn{margin-top:10px}
.fp-h{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);margin:30px 0 12px;font-weight:500}
.fp-gaps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.fp-gap{border:1px solid var(--line);background:#1b1b1b;border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:8px;opacity:0;transform:translateY(10px);animation:fpUp .6s var(--ez) forwards}
.fp-gap .mt{display:flex;justify-content:space-between;gap:8px;align-items:center;font-size:12px;color:var(--muted)}
.fp-gap .mt em{font-style:normal;border:1px solid #fff;color:#fff;border-radius:999px;padding:3px 10px;font-size:12px;white-space:nowrap}
.fp-gap b{font-size:16px;line-height:1.3}.fp-gap p{margin:0;font-size:13.5px;color:var(--muted);line-height:1.5}
.fp-gap a{margin-top:auto;font-size:13.5px;color:#fff;text-decoration:none;border-top:1px solid var(--line);padding-top:10px}
.fp-gap a:hover{text-decoration:underline}
.fp-dr{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 18px;margin:0;padding:0;list-style:none}
.fp-dr label{display:flex;gap:10px;align-items:flex-start;font-size:14.5px;line-height:1.45;cursor:pointer;padding:6px 0}
.fp-dr input{width:18px;height:18px;flex:none;margin-top:1px;accent-color:#fff}
.fp-dr small{display:block;color:var(--muted);font-size:12px}
.fp-bar{display:flex;align-items:center;gap:12px;margin:0 0 12px;font-size:13.5px;color:var(--muted)}
.fp-bar i{flex:1;height:8px;border-radius:8px;background:#2f2f2f;overflow:hidden}.fp-bar s{display:block;height:100%;width:0;background:#fff;transition:width .6s var(--ez)}
.fp-act button.btn{background:transparent;color:#fff;border:1px solid #fff}@media print{.fp-gap .du{color:#333}}.fp-gap .du{font-size:12.5px;color:#cfcfcf}
.fp-act{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.fp-safe{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.fp-safe span{font-size:12.5px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:5px 11px}
.fp-sec{margin-top:60px}.fp-sec>h2{font-size:clamp(22px,2.6vw,32px);margin:0 0 18px;line-height:1.2}
.fp-pro{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.fp-pro a{border:1px solid var(--line);background:var(--surface);border-radius:14px;padding:16px 14px;text-decoration:none;color:#fff;display:flex;flex-direction:column;gap:4px;transition:border-color .2s}
.fp-pro a:hover{border-color:#888}.fp-pro b{font-size:15.5px}.fp-pro span{font-size:12.5px;color:var(--muted);line-height:1.4}
.fp-more{margin-top:12px}.fp-more summary{cursor:pointer;color:var(--muted);font-size:14px}.fp-more p{color:var(--muted);font-size:14px;max-width:52em;line-height:1.6}
@keyframes fpUp{to{opacity:1;transform:none}}
@media (max-width:900px){.fp-gaps{grid-template-columns:repeat(2,minmax(0,1fr))}.fp-pro{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.fp-trk{grid-template-columns:1fr}.fp-trk button{padding:16px}#fp,#fpr{padding:18px}.fp-top{grid-template-columns:1fr;justify-items:center;text-align:center}.fp-pills{justify-content:center}.fp-gaps,.fp-dr{grid-template-columns:1fr}.fp-sec{margin-top:46px}}
@media (prefers-reduced-motion:reduce){.fp-gap,#fp.on,#fpr.on{animation:none;opacity:1;transform:none}}
@media print{header,footer,nav,.fp-hero,.fp-trk,#fp,.fp-act,.fp-sec,.fp-safe,.fp-gap a,[class*="fapw"],[class*="fal-"],#fa-ai,.eco,.fasec{display:none!important}
 body,#fpr{background:#fff!important;color:#000!important}#fpr{display:block!important;border:0;padding:0}
 .fp-gap,.fp-ring .fg{border-color:#000;stroke:#000}.fp-gap{background:#fff;opacity:1;transform:none;break-inside:avoid}.fp-gap p,.fp-dr small,.fp-num span{color:#333}
 .fp-gap .mt em,.fp-pills span{border-color:#000;color:#000}.fp-dr input{accent-color:#000}.fp-gaps{grid-template-columns:1fr 1fr}.fp-dr{grid-template-columns:1fr 1fr}}
</style>"""

TRACKS = ('<div class="fp-trk" role="group" aria-label="Pilih Tujuan Dana">'
  '<button type="button" data-t="bank"><i>Usaha Menengah</i><b>Kredit Bank</b><span>Modal Kerja, Investasi, Take Over, Kredit Kontraktor</span></button>'
  '<button type="button" data-t="inv"><i>UMKM yang Tumbuh</i><b>Investor atau VC</b><span>Angel, Venture Capital, Private Equity, Investor Strategis</span></button>'
  '<button type="button" data-t="?"><i>Belum Yakin</i><b>Bantu Pilihkan</b><span>Satu Pertanyaan, Lalu Kami Arahkan</span></button></div>')

FORM = ('<form id="fp" onsubmit="return false" aria-live="polite"><div id="fp_qs"></div>'
  '<div class="fp-go"><button type="button" id="fp_go" class="btn solid">Lihat Peta Pendanaan</button><span class="fp-cnt" id="fp_cnt"></span><span class="fp-err" id="fp_err"></span></div></form>')

RES = ('<div id="fpr"><div class="fp-top"><div class="fp-ring"><svg width="180" height="180" viewBox="0 0 180 180"><circle class="bg" cx="90" cy="90" r="78"/>'
  '<circle class="fg" id="fp_arc" cx="90" cy="90" r="78" stroke-dasharray="490.09" stroke-dashoffset="490.09"/></svg><div class="fp-num"><div><b id="fp_n">0</b><span>Kesiapan</span></div></div></div>'
  '<div><div class="fp-grade" id="fp_g"></div><div class="fp-title" id="fp_t"></div><div class="fp-pills" id="fp_p"></div></div></div>'
  '<div id="fp_note"></div>'
  '<div class="fp-h">Celah yang Perlu Ditutup dan Siapa yang Menutupnya</div><div class="fp-gaps" id="fp_gaps"></div>'
  '<div class="fp-h">Checklist Data Room</div><div class="fp-bar"><span id="fp_drn"></span><i><s id="fp_drb"></s></i></div><ul class="fp-dr" id="fp_dr"></ul>'
  '<div class="fp-act"><a class="btn solid" id="fp_wa" target="_blank" rel="noopener" href="#">Kirim Peta ke WhatsApp</a>'
  '<button type="button" class="btn line" id="fp_pr">Simpan PDF</button><a class="btn line" id="fp_more" href="/bankability-index/">Skor Detail</a></div></div>')

SAFE = ('<div class="fp-safe"><span>Dihitung di Browser, Tidak Disimpan di Server</span><span>Skor Indikatif, Bukan Keputusan Bank atau Investor</span>'
  '<span>FA Tidak Menghimpun Dana Masyarakat</span><span>Penyusun Laporan dan Auditor Selalu Pihak Berbeda</span><span>Biaya Profesional Mitra Ditagih Langsung oleh Mitra</span></div>')

PRO = ('<section class="fp-sec"><h2>Untuk Profesional dan Pemberi Dana</h2><div class="fp-pro">'
  '<a href="/mitra-kap-kja/"><b>KAP dan KJA</b><span>Klien Datang dengan Celah yang Sudah Dipetakan</span></a>'
  '<a href="https://wa.me/%s?text=%s" target="_blank" rel="noopener"><b>KJPP</b><span>Penilaian Agunan dan Valuasi Usaha</span></a>'
  '<a href="/mitra-notaris/"><b>Notaris</b><span>Akta Perubahan, Pendirian PT, Saham</span></a>'
  '<a href="/mitra-rm-bank/"><b>RM Bank</b><span>Calon Debitur yang Sudah Dibenahi</span></a>'
  '<a href="/mitra-investor/"><b>Investor</b><span>Usaha dengan Data Room Siap</span></a></div></section>') % (
  WA, __import__("urllib.parse", fromlist=["quote"]).quote("Halo FA Indonesia, saya dari KJPP dan tertarik menjadi mitra Peta Pendanaan FA. Nama KJPP: ... Kota: ..."))

JS = r"""<script>
(function(){
var $=function(i){return document.getElementById(i)},WA='__WA__';
// [teks, poin, kode celah, kunci data room yang tercentang]
var Q={bank:[
 ['b_aset','Total Aset',[['Di Bawah Rp2,5 M',3,'',''],['Rp2,5 sampai 25 M',6,'',''],['Rp25 sampai 100 M',9,'',''],['Di Atas Rp100 M',10,'','']]],
 ['b_umur','Lama Usaha Berjalan',[['Kurang dari 2 Tahun',0,'umur',''],['2 sampai 3 Tahun',5,'',''],['Lebih dari 3 Tahun',10,'','']]],
 ['b_lk','Laporan Keuangan',[['Belum Ada',0,'lk',''],['Catatan Kas atau Excel',4,'lk',''],['Lengkap, Belum Diaudit',10,'audit?','lk'],['Diaudit KAP',15,'','lk,aud']]],
 ['b_pajak','SPT Dibanding Laporan Keuangan',[['SPT Belum Rutin',0,'pajak',''],['Rutin, Angkanya Beda',5,'pajak','spt'],['Rutin dan Selaras',12,'','spt']]],
 ['b_slik','Riwayat Kredit di SLIK',[['Lancar',12,'','slik'],['Belum Pernah Kredit',9,'','slik'],['Pernah Terlambat',6,'slik2',''],['Ada Tunggakan Berat',0,'slik','']]],
 ['b_dscr','Laba Usaha + Penyusutan Dibanding Cicilan Setahun',[['Di Atas 1,5 Kali',18,'','proy'],['1,25 sampai 1,5 Kali',13,'','proy'],['1 sampai 1,25 Kali',6,'dscr',''],['Di Bawah 1 Kali atau Belum Tahu',0,'dscr','']]],
 ['b_agunan','Nilai Agunan Dibanding Plafon',[['Di Atas 125%',13,'','agn'],['100% sampai 125%',9,'','agn'],['Di Bawah 100%',4,'agunan','agn'],['Belum Ada Agunan',0,'agunan','']]],
 ['b_kjpp','Laporan Penilaian Agunan',[['Masih Berlaku',5,'','kjpp'],['Kedaluwarsa atau Belum Ada',0,'kjpp','']]],
 ['b_legal','Akta, NIB, dan Izin Usaha',[['Lengkap dan Terbaru',10,'','akta,nib'],['Ada yang Belum Diperbarui',4,'legal','nib'],['Belum Lengkap',0,'legal','']]],
 ['b_rek','Rekening Usaha',[['Terpisah dari Pribadi',5,'','rk'],['Sebagian Masih Campur',2,'rek',''],['Masih Satu Rekening',0,'rek','']]]],
inv:[
 ['i_tahap','Tahap Usaha',[['Ide, Belum Ada Omzet',2,'',''],['Omzet Kurang dari 1 Tahun',5,'',''],['Omzet Tumbuh 1 sampai 3 Tahun',9,'',''],['Untung Stabil Lebih dari 3 Tahun',12,'','']]],
 ['i_tumbuh','Pertumbuhan Omzet per Tahun',[['Di Bawah 10%',2,'growth',''],['10% sampai 30%',6,'',''],['30% sampai 100%',12,'',''],['Di Atas 100%',15,'','']]],
 ['i_badan','Badan Usaha',[['Perorangan',0,'pt',''],['CV',3,'pt',''],['PT',10,'','akta']]],
 ['i_saham','Kepemilikan Saham',[['Tercatat Rapi di Akta',8,'','cap'],['Ada Janji Saham Lisan',3,'cap',''],['Belum Jelas',0,'cap','']]],
 ['i_lk','Laporan Keuangan',[['Belum Ada',0,'lk',''],['Catatan Kas atau Excel',3,'lk',''],['Lengkap Bulanan',10,'audit?','lk'],['Diaudit KAP',14,'','lk,aud']]],
 ['i_metrik','Metrik Bulanan (Omzet, Margin, Pelanggan, Kas)',[['Ada Dashboard Rutin',8,'','met'],['Ada, Tidak Rutin',4,'metrik',''],['Belum Ada',0,'metrik','']]],
 ['i_pribadi','Aset dan Biaya Pribadi Pemilik',[['Sudah Terpisah',8,'','asset'],['Masih Campur',2,'normal','']]],
 ['i_pajak','Kepatuhan Pajak',[['Rutin dan Selaras',10,'','spt'],['Ada Selisih atau Tunggakan',3,'pajak',''],['Belum Lapor',0,'pajak','']]],
 ['i_deck','Pitch Deck dan Proyeksi 3 Tahun',[['Sudah Ada',8,'','deck,proy'],['Draf Kasar',4,'deck',''],['Belum Ada',0,'deck','']]],
 ['i_val','Valuasi dan Dana yang Dicari',[['Sudah Dihitung',7,'','val'],['Angka Kira-Kira',3,'val',''],['Belum Tahu',0,'val','']]]]};
// kode: [judul, alasan, mitra, durasi]
var G={
 lk:['Susun Laporan Keuangan Lengkap','Neraca, laba rugi, dan arus kas minimal 2 tahun. Dasar semua penilaian.','KJA Farhani','1 sampai 2 Bulan'],
 audit:['Audit oleh KAP','Kredit komersial dan investor institusi umumnya meminta laporan audited.','KAP DHN & Rekan','1 sampai 2 Bulan'],
 pajak:['Selaraskan SPT dengan Laporan','Omzet di SPT, mutasi rekening, dan laporan dicocokkan satu sama lain.','Konsultan Pajak Mitra','2 sampai 6 Minggu'],
 slik:['Selesaikan Tunggakan di SLIK','Kolektibilitas 3 sampai 5 hampir selalu ditolak. Restrukturisasi atau lunasi dulu.','Tim FA','1 sampai 3 Bulan'],
 slik2:['Siapkan Penjelasan Riwayat Telat Bayar','Analis bertanya. Jawaban tertulis dengan bukti mempercepat proses.','Tim FA','1 Minggu'],
 dscr:['Naikkan DSCR di Atas 1,25 Kali','Atur ulang plafon dan tenor, atau perbaiki laba, sebelum mengajukan.','Tim FA','2 sampai 4 Minggu'],
 agunan:['Tambah Agunan atau Sesuaikan Plafon','Nilai agunan di bawah plafon membuat plafon dipotong analis.','Tim FA','2 sampai 4 Minggu'],
 kjpp:['Penilaian Agunan Terbaru','Bank meminta laporan penilaian yang masih berlaku dari KJPP rekanannya.','KJPP Mitra','2 sampai 3 Minggu'],
 legal:['Perbarui Akta dan Izin','Akta perubahan, NIB, dan izin sektor dicek sejak tahap awal.','Notaris Mitra','2 sampai 4 Minggu'],
 rek:['Pisahkan Rekening Usaha','Mutasi rekening usaha adalah bukti omzet yang paling dipercaya.','Tim FA','Mulai Bulan Ini'],
 umur:['Bangun Riwayat Usaha','Usaha di bawah 2 tahun lebih cocok KUR atau pembiayaan berbasis kontrak.','Tim FA','Bertahap'],
 pt:['Ubah ke PT','Investor masuk lewat kepemilikan saham, yang hanya ada di PT.','Notaris Mitra','2 sampai 4 Minggu'],
 cap:['Rapikan Kepemilikan Saham','Janji saham lisan jadi masalah saat due diligence. Catat di akta.','Notaris Mitra','2 sampai 4 Minggu'],
 metrik:['Dashboard Metrik Bulanan','Investor membaca tren bulanan, bukan satu angka tahunan.','Tim FA','2 Minggu'],
 normal:['Pisahkan Aset dan Biaya Pribadi','Investor menormalkan EBITDA. Lebih baik angka itu Anda yang hitung duluan.','KJA Farhani + Tim FA','1 Bulan'],
 deck:['Pitch Deck dan Proyeksi 3 Tahun','Cerita, angka, dan penggunaan dana dalam 12 sampai 15 slide.','Tim FA','2 sampai 3 Minggu'],
 val:['Hitung Valuasi dan Kebutuhan Dana','Tentukan berapa yang dicari dan berapa persen saham yang dilepas.','Tim FA / KJPP Mitra','2 Minggu'],
 growth:['Pertimbangkan Kredit atau Investor Strategis','Pertumbuhan di bawah 10% kurang menarik untuk VC. Kredit bank sering lebih murah.','Tim FA','Diskusi 30 Menit'],
 paket:['Siapkan Paket Pengajuan','Memo kredit, proyeksi, dan data pendukung agar analis cepat memproses.','Tim FA','2 Minggu'],
 room:['Susun Data Room dan Daftar Investor','Data room rapi dan daftar investor yang tesisnya cocok dengan usaha Anda.','Tim FA','2 sampai 4 Minggu']};
var DR={bank:[['akta','Akta Pendirian, Perubahan, dan SK Kemenkum'],['nib','NIB dan Izin Sektor'],['kp','KTP dan NPWP Pengurus'],['lk','Laporan Keuangan 2 Tahun Terakhir'],['aud','Laporan Keuangan Diaudit KAP'],['spt','SPT Tahunan 2 Tahun Terakhir'],['rk','Rekening Koran 6 sampai 12 Bulan'],['slik','Daftar Utang dan Hasil SLIK'],['agn','Daftar dan Dokumen Agunan'],['kjpp','Laporan Penilaian Agunan (KJPP)'],['spk','Daftar Kontrak atau SPK Berjalan'],['proy','Proyeksi Arus Kas dan Penggunaan Dana']],
 inv:[['akta','Akta PT dan Daftar Pemegang Saham'],['cap','Struktur Kepemilikan (Cap Table)'],['lk','Laporan Keuangan Sejak Berdiri'],['aud','Laporan Keuangan Diaudit KAP'],['met','Dashboard Metrik Bulanan'],['deck','Pitch Deck'],['proy','Proyeksi 3 sampai 5 Tahun'],['val','Model Valuasi dan Penggunaan Dana'],['spt','SPT dan Bukti Bayar Pajak'],['ktr','Kontrak Pelanggan dan Pemasok Utama'],['asset','Daftar Aset, Merek, dan HKI'],['tim','Struktur Organisasi dan Tim Inti']]};
var T=null,A={},last=null;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function ga(n,o){try{window.gtag&&gtag('event',n,o)}catch(e){}}
function cnt(){var n=T?Q[T].filter(function(q){return A[q[0]]!=null}).length:0;$('fp_cnt').textContent=T?n+' dari '+Q[T].length+' Terjawab':''}
function render(){
 if(T==='?'){$('fp_qs').innerHTML='<div class="fp-q"><p>Omzet Tumbuh di Atas 30% per Tahun dan Bersedia Berbagi Kepemilikan Saham?</p><div class="fp-ch">'
  +'<button type="button" data-r="inv">Ya, Siap Berbagi Saham</button><button type="button" data-r="bank">Tidak, Ingin Tetap Pegang Penuh</button></div></div>';$('fp_go').style.display='none';cnt();return}
 $('fp_go').style.display='';
 $('fp_qs').innerHTML=Q[T].map(function(q){return '<div class="fp-q"><p>'+q[1]+'</p><div class="fp-ch" data-q="'+q[0]+'">'+q[2].map(function(o,i){return '<button type="button" data-i="'+i+'"'+(A[q[0]]===i?' class="on"':'')+'>'+o[0]+'</button>'}).join('')+'</div></div>'}).join('');cnt()}
function pick(t){T=t;A={};[].forEach.call(document.querySelectorAll('.fp-trk button'),function(b){b.classList.toggle('on',b.getAttribute('data-t')===t)});
 $('fp').classList.add('on');$('fpr').classList.remove('on');$('fp_err').textContent='';render();ga('pendanaan_track',{track:t})}
document.querySelector('.fp-trk').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;pick(b.getAttribute('data-t'));setTimeout(function(){$('fp').scrollIntoView({behavior:'smooth',block:'start'})},60)});
$('fp_qs').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
 if(b.hasAttribute('data-r')){pick(b.getAttribute('data-r'));return}
 var g=b.parentNode,k=g.getAttribute('data-q');A[k]=+b.getAttribute('data-i');[].forEach.call(g.children,function(x){x.classList.toggle('on',x===b)});$('fp_err').textContent='';cnt()});
function drKey(){return 'fa_dr_'+T}
function drLoad(){try{return JSON.parse(localStorage.getItem(drKey())||'{}')}catch(e){return {}}}
function drSave(o){try{localStorage.setItem(drKey(),JSON.stringify(o))}catch(e){}}
function drUpd(){var c=document.querySelectorAll('#fp_dr input'),n=0;[].forEach.call(c,function(x){if(x.checked)n++});$('fp_drn').textContent=n+' dari '+c.length+' Siap';$('fp_drb').style.width=Math.round(n/c.length*100)+'%'}
$('fp_go').addEventListener('click',function(){
 var qs=Q[T];for(var k=0;k<qs.length;k++){if(A[qs[k][0]]==null){$('fp_err').textContent='Masih ada yang belum dipilih.';document.querySelector('[data-q="'+qs[k][0]+'"]').scrollIntoView({behavior:'smooth',block:'center'});return}}
 var tot=0,max=0,gaps=[],have={},ans=[];
 qs.forEach(function(q){var o=q[2][A[q[0]]];tot+=o[1];max+=Math.max.apply(null,q[2].map(function(x){return x[1]}));ans.push(q[1]+': '+o[0]);
  if(o[2])gaps.push(o[2]);if(o[3])o[3].split(',').forEach(function(d){have[d]=1})});
 var sc=Math.round(tot/max*100),bank=T==='bank',as=bank?A.b_aset:-1;
 if(bank&&A.b_slik===3)sc=Math.min(sc,35);
 gaps=gaps.filter(function(g){if(g!=='audit?')return true;return bank?as>=2:A.i_tahap>=2}).map(function(g){return g==='audit?'?'audit':g});
 if(bank&&A.b_kjpp===1&&A.b_agunan===3)gaps=gaps.filter(function(g){return g!=='kjpp'});
 var seen={};gaps=gaps.filter(function(g){if(seen[g])return false;seen[g]=1;return true});
 if(!gaps.length)gaps=[bank?'paket':'room'];
 var gr=sc>=80?['A','Siap Diajukan','Siap Sekarang']:sc>=65?['B','Hampir Siap','1 sampai 2 Bulan Lagi']:sc>=50?['C','Perlu Dibenahi','3 sampai 6 Bulan']:sc>=35?['D','Belum Siap','6 sampai 12 Bulan']:['E','Benahi Fondasi Dulu','Lebih dari 12 Bulan'];
 var jalur=bank?['Segmen Mikro dan KUR','Segmen SME dan Bisnis','Segmen Komersial','Segmen Komersial Besar'][as]:['Angel atau Inkubator','Angel atau Pre-Seed','Seed sampai Series A (VC)','Private Equity atau Investor Strategis'][A.i_tahap];
 if(!bank&&A.i_tumbuh===0&&A.i_tahap===3)jalur='Investor Strategis atau Kredit Bank';
 $('fp_g').textContent='Grade '+gr[0]+(bank?' · Kredit Bank':' · Investor');$('fp_t').textContent=gr[1];
 $('fp_p').innerHTML='<span>'+jalur+'</span><span class="m">Estimasi Siap: '+gr[2]+'</span>';
 var note='';
 if(bank&&as<=1)note='<div class="fp-note"><b>Aset di bawah Rp25 M: rapikan laporan dulu.</b> Paket pembukuan terima beres, Anda cukup upload bon ke Drive.<br><a class="btn line" href="https://cariakuntan.com/jasa-pembukuan/" target="_blank" rel="noopener">Lihat Paket Pembukuan</a></div>';
 if(!bank&&A.i_tahap===0)note='<div class="fp-note"><b>Belum ada omzet:</b> investor tahap ini menilai tim dan bukti pasar. Mulai dari pembukuan sederhana dan metrik pelanggan.</div>';
 $('fp_note').innerHTML=note;
 var biz='';try{var L=JSON.parse(localStorage.getItem('fa_lead')||'{}');biz=L.nama||L.usaha||''}catch(e){}
 $('fp_gaps').innerHTML=gaps.slice(0,6).map(function(g,i){var x=G[g],m='Halo FA Indonesia, dari Peta Pendanaan ('+(bank?'Kredit Bank':'Investor')+', skor '+sc+'), saya perlu bantuan: '+x[0]+' ('+x[2]+').';
  return '<div class="fp-gap" style="animation-delay:'+(i*.07)+'s"><div class="mt"><span>'+(i+1<10?'0':'')+(i+1)+'</span><em>'+esc(x[2])+'</em></div><b>'+x[0]+'</b><p>'+x[1]+'</p><span class="du">Durasi: '+x[3]+'</span><a href="https://wa.me/'+WA+'?text='+encodeURIComponent(m)+'" target="_blank" rel="noopener">Minta Bantuan</a></div>'}).join('');
 var saved=drLoad();
 $('fp_dr').innerHTML=DR[T].map(function(d){var on=saved[d[0]]!=null?saved[d[0]]:!!have[d[0]];return '<li><label><input type="checkbox" data-k="'+d[0]+'"'+(on?' checked':'')+'><span>'+d[1]+'</span></label></li>'}).join('');
 drUpd();
 var r=$('fpr');r.classList.add('on');$('fp_more').href=bank?'/bankability-index/':'/cek-kelayakan-ipo/';$('fp_more').textContent=bank?'Skor Kredit Detail':'Cek Kelayakan IPO';
 var t0=null;function an(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1300);$('fp_n').textContent=Math.round(sc*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(an)}requestAnimationFrame(an);
 setTimeout(function(){$('fp_arc').style.strokeDashoffset=490.09*(1-sc/100)},60);
 last={sc:sc,gr:gr,jalur:jalur,gaps:gaps,ans:ans,bank:bank};setWa();
 ga('pendanaan_score',{track:T,score:sc,grade:gr[0],jalur:jalur,gaps:gaps.join(',')});
 r.scrollIntoView({behavior:'smooth',block:'start'})});
function setWa(){if(!last)return;var miss=[];[].forEach.call(document.querySelectorAll('#fp_dr input'),function(x){if(!x.checked)miss.push(x.parentNode.textContent)});
 var m='Halo FA Indonesia, saya sudah cek Peta Pendanaan FA.\nTujuan: '+(last.bank?'Kredit Bank':'Investor / VC')+'\nSkor: '+last.sc+'/100 (Grade '+last.gr[0]+', '+last.gr[1]+')\nJalur: '+last.jalur+'\nCelah: '+last.gaps.map(function(g){return G[g][0]}).join('; ')+'\nDokumen belum siap: '+(miss.length?miss.join('; '):'-')+'\nSaya ingin diskusi langkah berikutnya.';
 $('fp_wa').href='https://wa.me/'+WA+'?text='+encodeURIComponent(m)}
$('fp_dr').addEventListener('change',function(e){var x=e.target;if(!x.getAttribute('data-k'))return;var o=drLoad();o[x.getAttribute('data-k')]=x.checked;drSave(o);drUpd();setWa()});
$('fp_pr').addEventListener('click',function(){ga('pendanaan_pdf',{track:T});window.print()});
$('fp_wa').addEventListener('click',function(){ga('pendanaan_wa',{track:T,score:last&&last.sc})});
var h=(location.hash||'').replace('#','');if(h==='bank'||h==='investor')pick(h==='bank'?'bank':'inv');
})();
</script>""".replace("__WA__", WA)

SEO = ('<section class="fp-sec"><details class="fp-more"><summary>Tentang Peta Pendanaan FA</summary>'
  '<p>Peta Pendanaan memetakan kesiapan usaha untuk dua jalur pendanaan: kredit bank (modal kerja, investasi, take over, kredit kontraktor) dan investor (angel, venture capital, private equity, investor strategis). '
  'Penilaiannya mengikuti cara analis kredit membaca laporan keuangan, SPT, SLIK OJK, DSCR, dan agunan, serta cara investor menilai pertumbuhan, kepemilikan saham, normalisasi EBITDA, dan data room.</p>'
  '<p>Setiap celah ditautkan ke profesional yang menutupnya: kantor jasa akuntansi untuk laporan keuangan, kantor akuntan publik untuk audit, KJPP untuk penilaian agunan dan valuasi, notaris untuk akta dan kepemilikan saham, serta konsultan pajak. '
  'Tim FA mendampingi sampai pengajuan ke bank atau presentasi ke investor.</p></details></section>')

FAQ = [("Apa bedanya dengan FA Bankability Index?", "Bankability Index menilai kredit bank secara rinci dengan angka keuangan. Peta Pendanaan lebih singkat, mencakup jalur bank dan investor, dan langsung menunjukkan siapa yang menutup tiap celah beserta checklist data room."),
       ("Apakah data saya disimpan?", "Tidak di server FA. Perhitungan dan centang checklist hanya tersimpan di browser Anda. Data terkirim hanya bila Anda menekan tombol WhatsApp."),
       ("Apakah FA menyalurkan dana atau menjamin kredit cair?", "Tidak. FA tidak menghimpun dana masyarakat dan tidak menjamin keputusan bank atau investor. FA menyiapkan dan mendampingi, keputusan tetap pada bank atau investor."),
       ("Bagaimana biaya profesional mitra?", "KJA, KAP, KJPP, notaris, dan konsultan pajak menagih langsung kepada klien sesuai penawaran masing-masing. Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak berbeda.")]

def page():
    t = TPL
    title = "Cek Kesiapan Pendanaan Usaha: Kredit Bank atau Investor | FA Indonesia"
    desc = "Cek kesiapan kredit bank atau investor dalam 2 menit: skor, jalur yang cocok, celah yang perlu ditutup beserta mitranya (KJA, KAP, KJPP, notaris), dan checklist data room."
    old = "https://faindonesia.co.id/komite-audit-komisaris-independen/"
    t = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, t, count=1, flags=re.S)
    for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        t = re.sub(r'(<meta %s content=")[^"]*' % re.escape(k), lambda m: m.group(1) + desc, t)
    for k in ('property="og:title"', 'name="twitter:title"'):
        t = re.sub(r'(<meta %s content=")[^"]*' % re.escape(k), lambda m: m.group(1) + title, t)
    t = t.replace('<meta property="og:type" content="profile">', '<meta property="og:type" content="website">')
    url = SITE + "/" + SLUG + "/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "@id": url + "#app", "name": "FA Venus · Peta Pendanaan", "url": url, "applicationCategory": "FinanceApplication",
         "operatingSystem": "Web", "description": desc, "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": SITE + "/"}},
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), t, count=1, flags=re.S)
    t = t.replace(old, url)
    faqh = '<section class="fp-sec"><h2>Pertanyaan Umum</h2>' + "".join('<details class="fp-more"><summary><b>%s</b></summary><p>%s</p></details>' % (q, a) for q, a in FAQ) + "</section>"
    main = ('<main id="top">' + CSS + '<section class="block"><div class="wrap">'
            '<div class="fp-hero"><p class="eyebrow">FA Venus · Peta Pendanaan</p><h1>Kredit Bank atau Investor: Seberapa Siap Usaha Anda?</h1>'
            '<p class="fp-lede">10 pertanyaan, 2 menit. Hasilnya skor, jalur yang cocok, celah beserta mitra yang menutupnya, dan checklist data room.</p></div>'
            + TRACKS + FORM + RES + SAFE + PRO + faqh + SEO + JS + '</div></section></main>')
    t = re.sub(r'<main id="top">.*?</main>', lambda m: main, t, count=1, flags=re.S)
    os.makedirs(os.path.join(B, SLUG), exist_ok=True)
    open(os.path.join(B, SLUG, "index.html"), "w", encoding="utf-8").write(t)
    print("ok", SLUG, len(t))

page()

# ---------- integrasi ----------
def patch(rel, marker, find, block, before=False):
    p = os.path.join(B, rel)
    if not os.path.exists(p): print("skip", rel); return
    t = open(p, encoding="utf-8").read()
    if marker in t: print("ada", rel); return
    if find not in t: print("TIDAK KETEMU", rel); return
    t = t.replace(find, (block + find) if before else (find + block), 1)
    open(p, "w", encoding="utf-8").write(t); print("patch", rel)

BAN = ('<!--fa-peta-pendanaan--><div class="cta peta-cta" style="margin:22px 0 4px;border:1px solid currentColor;padding:18px 20px;display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between">'
       '<div><b style="display:block;font-size:17px">Belum Yakin Jalurnya?</b><span style="opacity:.75;font-size:14px">Peta Pendanaan: Skor, Celah, Mitra, dan Checklist Data Room dalam 2 Menit</span></div>'
       '<a class="btn red" href="/%s/">Cek Kesiapan Pendanaan</a></div><!--/fa-peta-pendanaan-->' % SLUG)
# beranda: di bawah catatan Pilih Jalur
patch("index.html", "<!--fa-peta-pendanaan-->", '<div class="jl2">', BAN, before=True)
# bankability: tombol ke peta pendanaan di hasil
patch("bankability-index/index.html", '/%s/#investor' % SLUG, '<a class="btn line" href="/cek-kapasitas-kredit/">Hitung Plafon Detail</a>',
      '<a class="btn line" href="/%s/#investor">Jalur Investor</a>' % SLUG)
for rel in ("mitra-investor/index.html", "mitra-rm-bank/index.html", "mitra-notaris/index.html", "mitra-kap-kja/index.html", "jasa-valuasi-usaha/index.html", "konsultan-kredit-bank/index.html"):
    p = os.path.join(B, rel)
    if not os.path.exists(p): continue
    t = open(p, encoding="utf-8").read()
    if 'href="/%s/"' % SLUG in t: continue
    m = re.search(r'Chat Ananta, CPA</a>', t)
    if not m: print("no-btn", rel); continue
    t = t[:m.end()] + '<a class="btn line" href="/%s/">Cek Kesiapan Pendanaan</a>' % SLUG + t[m.end():]
    open(p, "w", encoding="utf-8").write(t); print("link", rel)

sp = os.path.join(B, "sitemap.xml"); t = open(sp, encoding="utf-8").read(); u = SITE + "/" + SLUG + "/"
if u not in t: open(sp, "w", encoding="utf-8").write(t.replace("</urlset>", "<url><loc>%s</loc><lastmod>2026-11-03</lastmod></url></urlset>" % u))
lp = os.path.join(B, "llms.txt"); t = open(lp, encoding="utf-8").read()
if SLUG not in t:
    open(lp, "a", encoding="utf-8").write("\n- [Peta Pendanaan FA](%s): cek kesiapan kredit bank atau investor, celah beserta mitra penutupnya (KJA, KAP, KJPP, notaris, konsultan pajak), dan checklist data room.\n" % u)
