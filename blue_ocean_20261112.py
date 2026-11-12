# -*- coding: utf-8 -*-
"""12 Nov 2026. Eksekusi strategi Blue Ocean (dokumen 8 Nov) untuk beranda FA dan CariAkuntan.
Bos: "selesaikan semuanya", "no 4 kamu yang urus, tapi semua tetap ada tombol WA saya".
BEKERJA LANGSUNG DI out/. Idempoten. Jalankan setelah semua script beranda lain.

FA (out/faindonesia/index.html):
- Hero: "Siapkan Keuangan Usaha Sebelum Bertemu Bank, Investor, atau Pembeli." (ID, EN, ZH), tombol "Cek Kapasitas Kredit"
  + "Chat Ananta, CPA".
- Blok "Mulai dari Tujuan Anda" (pengganti menu layanan di beranda): Ke Bank, Cari Investor, Jual Usaha, Rumah Sakit dan
  Klinik, Audit dan Laporan Keuangan, Tim dan Izin, FA Apps, Tanya Langsung (WA). Nav atas TIDAK diubah (muat 360 px).
CariAkuntan (out/cariakuntan):
- Hero: "Sebelum Bayar Akuntan, Pastikan Dulu Jasa yang Anda Butuhkan." tombol "Mulai Cek Kebutuhan", "Cek Izin Praktik",
  "Tanya Ananta, CPA".
- Halaman baru /cek-kebutuhan/: kuis 5 pertanyaan, hasil jenis jasa + dokumen + perkiraan waktu kerja (tanpa angka tarif)
  + tombol WA berisi ringkasan jawaban. Dihitung di browser, tidak ada data terkirim.
- Kartu "Cek Kebutuhan" di blok Saya Butuh, sitemap <!--cakb-->, llms."""
import os, re, sys, json, html, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(HERE, "out", "faindonesia"); CA = os.path.join(HERE, "out", "cariakuntan")
TODAY = "2026-11-12"
E = html.escape
N = [0]
def rd(p): return open(p, encoding="utf-8").read()
def wt(p, t):
    if os.path.exists(p) and rd(p) == t: return
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(t); N[0] += 1
def wa(txt): return "https://wa.me/6282245260121?text=" + urllib.parse.quote(txt, safe="")
def must(t, old, new, count=1):
    assert old in t, old[:80]
    return t.replace(old, new, count)

# ====================== FA beranda ======================
p = os.path.join(FA, "index.html"); t = rd(p)
if "<!--bo12-hero-->" not in t:
    t = must(t, '<h1 data-i18n="k318">Dari Laporan Keuangan<br/>sampai <em>Dana Cair.</em></h1>',
             '<!--bo12-hero--><h1 data-i18n="k318">Siapkan Keuangan Usaha Sebelum Bertemu <em>Bank, Investor, atau Pembeli.</em></h1>')
    t = must(t, 'data-tool="Dari Laporan Keuangan sampai Dana Cair."', 'data-tool="Siapkan Keuangan Usaha Sebelum Bertemu Bank, Investor, atau Pembeli."')
    t = must(t, '<p class="lede" data-i18n="jl0">Untuk semua skala perusahaan: merapikan laporan keuangan, lalu kredit bank, investor, sampai IPO.</p>',
             '<p class="lede" data-i18n="jl0">Cek posisi usaha Anda lewat FA Apps, gratis. Bila perlu pendampingan, Anda bicara langsung dengan Ananta W. Sasongko, CPA.</p>')
    t = must(t, '<a class="btn line" data-i18n="k11" href="/layanan/#rekam">Lihat Rekam Jejak</a>', '<a class="btn line" data-i18n="k11" href="#cek-kredit">Cek Kapasitas Kredit</a>')
    for old, new in (('"k318": "From Financial Statements<br>to <em>Funds Disbursed.</em>"', '"k318": "Get Your Finances Ready Before Meeting <em>Banks, Investors, or Buyers.</em>"'),
                     ('"k318": "从财务报表<br>到<em>资金到位。</em>"', '"k318": "在面对<em>银行、投资者或买家</em>之前，先把财务准备好。"'),
                     ('"k11": "View Track Record"', '"k11": "Check Credit Capacity"'), ('"k11": "查看业绩"', '"k11": "测算贷款额度"')):
        t = must(t, old, new)
    t = re.sub(r'("jl0": ")For companies of every size: tidy financial statements first, then bank credit, investors, and IPO\.(")',
               r'\1Check where your business stands with FA Apps, free. When you need hands-on support, you talk directly with Ananta W. Sasongko, CPA.\2', t)
    t = re.sub(r'("jl0": ")适用于各种规模的企业：先整理财务报表，再对接银行贷款、投资者与上市。(")', r'\1先用 FA Apps 免费了解企业现状；需要协助时，直接与 Ananta W. Sasongko, CPA 沟通。\2', t)
# blok tujuan
IC = {"bank": '<path d="M3 10h18M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18M12 3l9 5H3z"></path>',
      "up": '<path d="M3 17l6-6 4 4 8-8"></path><path d="M15 7h6v6"></path>',
      "tag": '<path d="M3 12V4h8l10 10-8 8z"></path><path d="M7.5 7.5h.01"></path>',
      "plus": '<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"></path>',
      "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"></path><path d="M14 3v5h5M9 13h6M9 17h6"></path>',
      "id": '<path d="M3 6h18v12H3z"></path><path d="M7 10h4M7 14h6M16 10.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"></path>',
      "grid": '<path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"></path>',
      "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"></path>'}
GOALS = [("Ke Bank", "Kredit baru, top up, atau take over: hitung plafon yang realistis dulu.", "/konsultan-kredit-bank/", "bank", True),
         ("Cari Investor atau IPO", "Kesiapan pendanaan, valuasi, dan persiapan uji tuntas.", "/mitra-investor/", "up", False),
         ("Jual Usaha", "Valuasi dan penyiapan sebelum bertemu pembeli.", "/jasa-valuasi-usaha/", "tag", False),
         ("Rumah Sakit dan Klinik", "Unit cost, klaim BPJS, dan keuangan rumah sakit.", "/konsultan-rumah-sakit/", "plus", False),
         ("Audit dan Laporan Keuangan", "Per industri dan per daerah, oleh KAP DHN & Rekan dan KJA Farhani.", "/audit-laporan-keuangan-per-industri/", "doc", False),
         ("Tim dan Izin", "Siapa yang mengerjakan dan izin praktiknya.", "/mitra-kap-kja/", "id", False),
         ("FA Apps", "Kalkulator dan aplikasi gratis, hasil langsung keluar.", "/apps/", "grid", False),
         ("Tanya Langsung", "Ceritakan kondisi usaha Anda lewat WhatsApp.", wa("Halo Pak Ananta, saya ingin konsultasi soal usaha saya."), "chat", False)]
def card(lbl, tip, href, ic, main):
    ext = ' rel="noopener" target="_blank"' if href.startswith("http") else ""
    return (f'<a class="w{" main" if main else ""}" href="{href}"{ext} title="{E(tip)}"><span class="ic"><svg aria-hidden="true" viewbox="0 0 24 24">{IC[ic]}</svg></span>'
            f'<b>{E(lbl)}</b><i>→</i></a>')
a = t.index('<section class="want" id="mulai-cepat"'); b = t.index("</section>", a) + len("</section>")
sec = t[a:b]
style = re.search(r'<section class="want" id="mulai-cepat" style="[^"]*">', sec).group(0)
new = (style + '<!--bo12-tujuan--><div class="in"><div class="hd"><h2>Mulai dari Tujuan Anda</h2></div><div class="g">'
       + "".join(card(*g) for g in GOALS) + "</div></div></section>")
t = t[:a] + new + t[b:]
if 'id="bo12-css"' not in t:
    t = t.replace("</head>", '<style id="bo12-css">.want a.w:nth-child(n+5){animation-delay:.28s}</style></head>', 1)
wt(p, t)

# ====================== CariAkuntan ======================
p = os.path.join(CA, "index.html"); t = rd(p)
if "<!--bo12-hero-->" not in t:
    a = t.index('<p class="label">Screening Awal'); b = t.index("</div></section>", a)
    hero = ('<!--bo12-hero--><p class="label">Cek Kebutuhan · Cek Izin · Screening</p>\n'
            '<h1>Sebelum Bayar Akuntan, Pastikan Dulu Jasa yang Anda Butuhkan.</h1><div class="tshare-top"><div class="share" data-lab="Bagikan" data-tool="Sebelum Bayar Akuntan, Pastikan Dulu Jasa yang Anda Butuhkan."></div></div>\n'
            '<p class="sub">Audit, review, kompilasi, atau cukup pembukuan? Jawab 5 pertanyaan, lihat jasa yang pas dan dokumen yang perlu disiapkan. Cek juga izin praktiknya di registri resmi. Gratis, tanpa daftar.</p>\n'
            '<div class="cta"><a class="btn btn-wa arrow" href="/cek-kebutuhan/">Mulai Cek Kebutuhan</a><a class="btn btn-line" href="/cek-izin/">Cek Izin Praktik</a>'
            f'<a class="btn btn-line" href="{wa("Halo Pak Ananta, saya ingin tanya dulu jasa akuntan apa yang pas untuk usaha saya.")}" rel="noopener" target="_blank">Tanya Ananta, CPA</a></div>\n')
    t = t[:a] + hero + t[b:]
# kartu Cek Kebutuhan sebagai kartu pertama blok Saya Butuh
if "<!--bo12-kb-->" not in t:
    a = t.index('<section class="want" id="mulai-cepat"'); g = t.index('<div class="g">', a) + len('<div class="g">')
    c = ('<!--bo12-kb--><a class="w main" href="/cek-kebutuhan/" title="Jawab 5 pertanyaan, lihat jasa yang pas."><span class="ic"><svg aria-hidden="true" viewbox="0 0 24 24">'
         '<path d="M9 11l3 3 8-8"></path><path d="M20 12v7a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h11"></path></svg></span><b>Cek Kebutuhan Jasa</b><i>→</i></a><!--/bo12-kb-->')
    seg_end = t.index("</section>", a)
    seg = t[g:seg_end].replace('class="w main"', 'class="w"', 1)
    t = t[:g] + c + seg + t[seg_end:]
    if 'id="bo12-css"' not in t:
        t = t.replace("</head>", '<style id="bo12-css">@media(min-width:861px){#mulai-cepat .g{grid-template-columns:repeat(5,1fr)}}@media(max-width:860px){#mulai-cepat .g a.w:first-of-type{grid-column:1/-1;min-height:92px}}</style></head>', 1)
wt(p, t)

# ---------- halaman /cek-kebutuhan/ ----------
T = rd(os.path.join(CA, "cek-izin", "index.html"))
head, tail = T[:T.index("<main")], T[T.index("</main>"):]
URL = "https://cariakuntan.com/cek-kebutuhan/"
TITLE = "Cek Kebutuhan Jasa Akuntan: Audit, Review, atau Pembukuan?"
DESC = "Jawab 5 pertanyaan, lihat jasa akuntan yang pas: audit KAP, review, kompilasi, atau pembukuan, plus dokumen yang disiapkan. Gratis, tanpa daftar."
assert len(TITLE) <= 65 and len(DESC) <= 158
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, count=1, flags=re.S)
head = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description")/>', lambda m: f'<meta content="{DESC}" {m.group(1)}/>', head)
head = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{TITLE}" property="og:title"/>', head)
head = re.sub(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{URL}" rel="canonical"/>', head)
head = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{URL}" property="og:url"/>', head)
FAQ = [("Apa beda audit, review, dan kompilasi?", "Audit memberi keyakinan memadai dan menghasilkan opini auditor independen, dikerjakan Kantor Akuntan Publik. Review memberi keyakinan terbatas. Kompilasi adalah penyusunan laporan keuangan dari data perusahaan tanpa memberi keyakinan, umumnya dikerjakan Kantor Jasa Akuntansi."),
       ("Kapan perusahaan wajib diaudit?", "UU Perseroan Terbatas Pasal 68 mewajibkan audit antara lain bila perseroan menghimpun dana masyarakat, menerbitkan surat pengakuan utang kepada masyarakat, berstatus terbuka, atau memiliki aset dan/atau peredaran usaha paling sedikit Rp50 miliar. Di luar itu, audit sering diminta bank, pemberi kerja tender, dan investor."),
       ("Apakah hasil cek ini mengikat?", "Tidak. Hasilnya arahan awal dari jawaban Anda. Kebutuhan sebenarnya ditentukan pihak yang meminta laporan, misalnya bank atau panitia tender. Karena itu ada tombol untuk menanyakannya langsung ke Ananta, CPA."),
       ("Apakah data saya disimpan?", "Tidak. Jawaban dihitung di browser Anda dan tidak dikirim ke server. Ringkasan baru terkirim bila Anda sendiri menekan tombol WhatsApp."),
       ("Kenapa tidak ada angka tarif?", "Biaya bergantung pada ukuran usaha, kelengkapan data, dan ruang lingkup. Angka yang jujur baru bisa diberikan setelah data awal dilihat.")]
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebApplication", "name": "Cek Kebutuhan Jasa Akuntan", "url": URL, "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR"}, "inLanguage": "id"},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": "https://cariakuntan.com/"},
                                                    {"@type": "ListItem", "position": 2, "name": "Cek Kebutuhan", "item": URL}]}]}
head = re.sub(r'<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
CSS = ('<style id="kb-css">.kb{border:1px solid #dde3ee;border-radius:14px;padding:20px;background:#fff;margin:22px 0}.kb fieldset{border:0;padding:0;margin:0 0 18px}'
       '.kb legend{font-weight:600;font-size:16.5px;margin-bottom:8px;padding:0}.kb .o{display:flex;flex-wrap:wrap;gap:8px}'
       '.kb label{display:inline-flex;align-items:center;border:1px solid #cfd8e6;border-radius:999px;padding:8px 14px;cursor:pointer;font-size:14.5px;line-height:1.3;background:#f7f9fd}'
       '.kb input{position:absolute;opacity:0;pointer-events:none}.kb label:has(input:checked){background:#1F5BFF;border-color:#1F5BFF;color:#fff}'
       '.kb label:has(input:focus-visible){outline:2px solid #0B1F33;outline-offset:2px}.kb-r{border:1px solid #1F5BFF;border-radius:14px;padding:20px;background:#f3f6ff;margin:22px 0}'
       '.kb-r h2{margin-top:0}.kb-r ol,.kb-r ul{padding-left:20px}.kb-r .svc{border-top:1px solid #d5ddf0;padding-top:12px;margin-top:12px}.kb-r .svc b{font-size:16px}'
       '.kb-r .btn{margin:6px 8px 0 0}.kb-n{font-size:13.5px;opacity:.75}.kb-p{font-size:14px;margin:0 0 14px;opacity:.8}</style>')
head = head.replace("</head>", CSS + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script></head>", 1)
Q = [("tujuan", "1. Laporan keuangan ini untuk apa?", [("bank", "Kredit bank"), ("tender", "Tender atau prakualifikasi"), ("investor", "Investor atau jual usaha"),
                                                      ("sabh", "Laporan tahunan PT (SABH)"), ("pajak", "Pajak: SPT, SP2DK, pemeriksaan"), ("aset", "Nilai aset atau agunan"), ("rapi", "Belum ada yang minta, ingin rapi")]),
     ("bentuk", "2. Bentuk usahanya?", [("pt", "PT"), ("cv", "CV atau firma"), ("perorangan", "Perorangan atau UMKM"), ("nirlaba", "Yayasan atau koperasi")]),
     ("skala", "3. Aset atau omzet setahun kira-kira?", [("kecil", "Di bawah Rp5 miliar"), ("menengah", "Rp5 sampai 50 miliar"), ("besar", "Rp50 miliar ke atas")]),
     ("buku", "4. Kondisi pembukuan sekarang?", [("belum", "Belum ada pembukuan"), ("sebagian", "Ada catatan, belum jadi laporan"), ("lengkap", "Sudah ada laporan keuangan lengkap")]),
     ("minta", "5. Apakah pihak yang meminta menyebut kata diaudit atau audited?", [("ya", "Ya"), ("tidak", "Tidak"), ("taktahu", "Belum tahu")])]
form = "".join(f'<fieldset><legend>{E(l)}</legend><div class="o">' + "".join(f'<label><input type="radio" name="{k}" value="{v}"/>{E(tx)}</label>' for v, tx in opts) + "</div></fieldset>" for k, l, opts in Q)
LBL = {k: dict(opts) for k, _, opts in Q}
JS = r"""<script id="kb-js">(function(){
var L=%s,f=document.getElementById('kb'),r=document.getElementById('kb-r');
var S={
 susun:{n:'Penyusunan laporan keuangan (kompilasi)',w:'Kantor Jasa Akuntansi (KJA)',t:'Umumnya 2 sampai 6 minggu, tergantung kelengkapan data dan jumlah transaksi.',d:['Rekening koran semua rekening usaha','Nota atau rekap penjualan dan pembelian','Daftar aset tetap dan tahun perolehannya','Daftar utang, piutang, dan stok akhir periode','Akta, NIB, dan NPWP']},
 buku:{n:'Pembukuan bulanan',w:'Kantor Jasa Akuntansi (KJA)',t:'Berjalan tiap bulan. Bulan pertama biasanya lebih lama karena menata saldo awal.',d:['Rekening koran bulanan','Nota penjualan, pembelian, dan biaya','Daftar gaji','Akses aplikasi kasir atau lokapasar bila ada']},
 audit:{n:'Audit laporan keuangan',w:'Kantor Akuntan Publik (KAP)',t:'Umumnya 4 sampai 8 minggu setelah laporan keuangan siap, tergantung ukuran usaha dan kesiapan dokumen.',d:['Laporan keuangan dan neraca saldo','Buku besar dan rekening koran','Daftar aset tetap, piutang, utang, dan persediaan','Perjanjian kredit dan kontrak penting','Akta dan perizinan']},
 review:{n:'Review laporan keuangan (keyakinan terbatas)',w:'Kantor Akuntan Publik (KAP)',t:'Umumnya lebih singkat daripada audit karena prosedurnya terbatas pada analitis dan permintaan keterangan.',d:['Laporan keuangan dan neraca saldo','Buku besar','Penjelasan manajemen atas pos yang berubah besar']},
 pajak:{n:'Jasa perpajakan',w:'Konsultan pajak berizin (KKP)',t:'Tergantung jenis urusannya. Surat dari kantor pajak punya batas waktu jawab, jadi jangan ditunda.',d:['Surat dari kantor pajak (bila ada)','SPT Masa dan SPT Tahunan terakhir','Laporan keuangan atau rekap omzet','Bukti potong dan faktur pajak']},
 nilai:{n:'Penilaian aset',w:'Kantor Jasa Penilai Publik (KJPP)',t:'Umumnya 1 sampai 3 minggu setelah survei lokasi, tergantung jenis dan jumlah aset.',d:['Sertifikat tanah dan IMB atau PBG','PBB terakhir','Daftar mesin atau kendaraan dan bukti kepemilikannya','Surat permintaan bank bila untuk agunan']}};
function val(k){var e=f.querySelector('input[name="'+k+'"]:checked');return e?e.value:''}
function go(){var a={},ok=true;['tujuan','bentuk','skala','buku','minta'].forEach(function(k){a[k]=val(k);if(!a[k])ok=false});
 if(!ok){r.hidden=true;return}
 var list=[],why=[];
 if(a.tujuan==='pajak'){list.push('pajak');why.push('Urusan pajak ditangani konsultan pajak berizin.')}
 if(a.tujuan==='aset'){list.push('nilai');why.push('Nilai aset untuk agunan atau transaksi ditetapkan penilai publik, bukan akuntan.')}
 if(a.buku!=='lengkap'&&a.tujuan!=='aset'){list.push('susun');why.push('Laporan keuangan belum lengkap, jadi harus disusun dulu sebelum dipakai atau diaudit.')}
 var wajib=a.bentuk==='pt'&&a.skala==='besar';
 var audit=a.minta==='ya'||wajib||a.tujuan==='tender'||a.tujuan==='investor';
 if(a.tujuan==='pajak'||a.tujuan==='aset')audit=a.minta==='ya'||wajib;
 if(audit){list.push('audit');
  if(wajib)why.push('PT dengan aset atau omzet Rp50 miliar ke atas termasuk yang wajib diaudit menurut UU Perseroan Terbatas Pasal 68.');
  else if(a.minta==='ya')why.push('Pihak yang meminta menyebut laporan audited, jadi diperlukan audit oleh KAP.');
  else why.push('Untuk tender dan investor, laporan audited hampir selalu diminta. Pastikan di dokumen persyaratannya.')}
 else if(a.tujuan==='bank'&&a.minta==='taktahu'){if(a.buku==='lengkap')list.push('review');why.push('Tanyakan ke bank apakah laporan harus audited. Banyak bank memintanya di atas plafon tertentu. Bila tidak, laporan yang disusun KJA atau review bisa cukup.')}
 else if(a.tujuan==='sabh'){why.push('Laporan tahunan PT memerlukan laporan keuangan. Audit diperlukan bila perseroan memenuhi kriteria wajib audit.')}
 if(a.tujuan==='rapi'&&a.buku!=='lengkap'){list.push('buku');why.push('Agar tidak menumpuk lagi, pembukuan dilanjutkan bulanan.')}
 if(!list.length){list.push('buku');why.push('Laporan sudah ada dan belum ada pihak yang meminta audit. Yang dijaga tinggal pembukuan rutinnya.')}
 var seen={},h='<h2>Hasil: Jasa yang Anda Butuhkan</h2><ol>';
 list=list.filter(function(x){if(seen[x])return false;seen[x]=1;return true});
 why.forEach(function(w){h+='<li>'+w+'</li>'});h+='</ol>';
 list.forEach(function(k,i){var s=S[k];h+='<div class="svc"><b>'+(i+1)+'. '+s.n+'</b><p>Dikerjakan: '+s.w+'.<br>Perkiraan waktu kerja: '+s.t+'</p><p><b>Dokumen yang disiapkan:</b></p><ul>'+s.d.map(function(x){return'<li>'+x+'</li>'}).join('')+'</ul></div>'});
 if(seen.susun&&seen.audit)h+='<p class="kb-n">Untuk satu perusahaan, penyusun laporan keuangan dan auditornya harus kantor yang berbeda agar independensi terjaga.</p>';
 var msg='Halo Pak Ananta, saya sudah isi Cek Kebutuhan di cariakuntan.com. Tujuan: '+L.tujuan[a.tujuan]+'. Bentuk usaha: '+L.bentuk[a.bentuk]+'. Skala: '+L.skala[a.skala]+'. Pembukuan: '+L.buku[a.buku]+'. Diminta audited: '+L.minta[a.minta]+'. Hasil: '+list.map(function(k){return S[k].n}).join(', ')+'. Mohon arahannya.';
 h+='<p style="margin-top:14px"><a class="btn btn-wa arrow" target="_blank" rel="noopener" data-ca-q="kebutuhan" href="https://wa.me/6282245260121?text='+encodeURIComponent(msg)+'">Tanya Ananta, CPA soal Hasil Ini</a><a class="btn btn-line" href="/cek-izin/">Cek Izin Praktik</a></p>';
 h+='<p class="kb-n">Perkiraan waktu adalah gambaran umum, bukan janji. Arahan ini dari jawaban Anda dan bukan opini profesional. Tidak ada data yang dikirim ke server.</p>';
 r.innerHTML=h;r.hidden=false;if(window.gtag)gtag('event','kb_hasil',{jasa:list.join('+')});
 r.scrollIntoView({behavior:'smooth',block:'nearest'})}
f.addEventListener('change',go)})();</script>""" % json.dumps(LBL, ensure_ascii=False)
tbl = ('<div class="tx"><table><thead><tr><th>Kebutuhan</th><th>Jasa</th><th>Dikerjakan</th></tr></thead><tbody>'
       '<tr><td>Bank, tender, atau investor meminta laporan audited</td><td>Audit laporan keuangan</td><td><a href="/layanan/kap/">KAP</a></td></tr>'
       '<tr><td>Belum punya laporan keuangan</td><td>Penyusunan laporan keuangan (kompilasi)</td><td><a href="/layanan/kja/">KJA</a></td></tr>'
       '<tr><td>Pembukuan menumpuk tiap bulan</td><td>Pembukuan bulanan</td><td><a href="/jasa-pembukuan/">KJA</a></td></tr>'
       '<tr><td>Laporan tahunan PT untuk SABH</td><td>Laporan keuangan, dan audit bila memenuhi kriteria</td><td><a href="/laporan-keuangan-sabh/">KJA dan KAP</a></td></tr>'
       '<tr><td>SPT, SP2DK, atau pemeriksaan pajak</td><td>Jasa perpajakan</td><td><a href="/layanan/konsultan-pajak/">Konsultan pajak</a></td></tr>'
       '<tr><td>Nilai agunan atau revaluasi aset</td><td>Penilaian aset</td><td><a href="/layanan/kjpp/">KJPP</a></td></tr></tbody></table></div>')
for u in ("/layanan/kja/", "/jasa-pembukuan/", "/laporan-keuangan-sabh/", "/layanan/kap/", "/layanan/konsultan-pajak/", "/layanan/kjpp/"):
    if not os.path.exists(os.path.join(CA, u.strip("/"), "index.html")): tbl = tbl.replace(f'<a href="{u}">', "<a>").replace("<a>", "<span>").replace("</a>", "</a>")
main = ('<main class="wrap art"><p class="crumb"><a href="/">Beranda</a> / Cek Kebutuhan</p><p class="label">Gratis · Tanpa Daftar · 1 Menit</p>'
        '<h1>Cek Kebutuhan: Jasa Akuntan Apa yang Sebenarnya Anda Perlukan?</h1>'
        '<p class="sub">Banyak pemilik usaha membayar jasa yang salah: minta audit padahal laporannya belum ada, atau menyusun laporan padahal bank meminta audited. Jawab 5 pertanyaan, hasilnya langsung tampil.</p>'
        f'<form class="kb" id="kb" onsubmit="return false"><p class="kb-p">Pilih satu jawaban di tiap pertanyaan. Hasil muncul setelah kelimanya terisi.</p>{form}</form>'
        '<div class="kb-r" id="kb-r" hidden aria-live="polite"></div>'
        f'<noscript><p>Aktifkan JavaScript untuk memakai kuis ini, atau langsung <a href="{wa("Halo Pak Ananta, saya ingin tanya jasa akuntan apa yang pas untuk usaha saya.")}">tanya Ananta, CPA</a>.</p></noscript>'
        '<h2>Ringkasnya: Kebutuhan dan Jasanya</h2>' + tbl +
        '<p>Sudah tahu jasanya? Lanjut <a href="/cek-izin/">cek izin praktik</a> kantor yang akan Anda tunjuk, atau lihat <a href="/kota/">daftar per kota</a>. '
        'Untuk akun yang khas di tiap industri, lihat <a href="https://faindonesia.co.id/audit-laporan-keuangan-per-industri/?dari=cariakuntan">audit dan laporan keuangan per industri</a> di FA Indonesia. '
        'Ingin menyusun sendiri dulu? Ada <a href="https://updatesak.com/kertas-kerja/?dari=cariakuntan">kertas kerja PSAK gratis</a> di UpdateSAK.</p>'
        '<h2>Pertanyaan Umum</h2>' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)
        + f'<p style="margin-top:20px"><a class="btn btn-wa arrow" href="{wa("Halo Pak Ananta, saya ingin tanya jasa akuntan apa yang pas untuk usaha saya.")}" rel="noopener" target="_blank">Tanya Ananta, CPA</a></p>')
tail2 = tail.replace('data-tool="Screening Instan Kebutuhan Akuntan"', 'data-tool="Cek Kebutuhan Jasa Akuntan"')
tail2 = re.sub(r"<script[^>]*>[^<]*izin[^<]*</script>|<script[^>]*src=\"/js/izin\.js[^\"]*\"[^>]*></script>", "", tail2)
tail2 = tail2.replace("</body>", JS + "</body>", 1)
wt(os.path.join(CA, "cek-kebutuhan", "index.html"), head + main + tail2)
sm = os.path.join(CA, "sitemap.xml"); s = re.sub(r"<!--cakb-->.*?<!--/cakb-->\n?", "", rd(sm), flags=re.S)
wt(sm, s.replace("</urlset>", f"<!--cakb--><url><loc>{URL}</loc><lastmod>{TODAY}</lastmod></url><!--/cakb-->\n</urlset>"))
for fn in ("llms.txt",):
    lp = os.path.join(CA, fn)
    if os.path.exists(lp):
        l = re.sub(r"\n<!--cakb-->.*?<!--/cakb-->", "", rd(lp), flags=re.S).rstrip("\n")
        wt(lp, l + f"\n<!--cakb-->\n\n## Cek Kebutuhan (12 Nov 2026)\n- [Cek Kebutuhan Jasa Akuntan]({URL}): kuis 5 pertanyaan, hasil jenis jasa (audit, review, kompilasi, pembukuan, pajak, penilaian), dokumen, dan perkiraan waktu\n<!--/cakb-->\n")
print("blue ocean: file berubah", N[0])
