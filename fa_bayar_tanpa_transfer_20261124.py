# -*- coding: utf-8 -*-
"""Bayar tanpa transfer (24 Nov 2026, permintaan Bos).
Pemicu: pembeli produk kecil masih transfer BRI lalu kirim bukti lewat WA, padahal sudah ada Mayar dan Midtrans.
Aturan baru di /bayar/:
- E-book dan FA Jupiter: hanya Bayar Online, tombol membuka checkout Mayar (sama dengan /toko/).
- Produk lain (kertas kerja, template, Paket AI): hanya Bayar Online lewat Midtrans.
  Bila Midtrans belum mode produksi (/api/pay/config production:false), invoice transfer tampil sebagai cadangan
  supaya produk tetap bisa dibeli. Begitu produksi aktif, transfer hilang otomatis.
- Layanan lain sesuai penawaran: Bayar Online (bila Midtrans aktif) atau invoice dan transfer bank.
Juga: S&K pasal 3.2 dan FAQ /buku/ disamakan dengan kondisi ini.
Idempoten. Mengedit sumber v58 dan out/ sekaligus (jangan commit out/ hasil prep penuh, lihat README-DEPLOY)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS = [os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58"), os.path.join(HERE, "out", "faindonesia")]
MARK = "<!--bayar-nt-20261124-->"

LEAD = ('<p class="lead">Pilih produk dan isi data Anda, lalu klik Bayar Online (QRIS, e-wallet, atau virtual account). '
        'Akses dan file langsung tersedia setelah lunas, tanpa kirim bukti bayar. '
        'Invoice dan transfer bank hanya untuk layanan sesuai surat penawaran.</p>')
DESC = "Bayar FA Apps, e-book, dan kertas kerja FA Indonesia secara online (QRIS, e-wallet, virtual account). Invoice dan transfer bank khusus layanan sesuai surat penawaran."

BLOCK = MARK + '''<div class="btns"><button class="btn blue" id="paynow" style="display:none">Bayar Online</button>
<button class="btn solid tf" id="mk" style="display:none">Buat Invoice Transfer Bank</button><button class="btn tf" id="cp" style="display:none">Salin Rekening BRI</button></div>
<p class="hint" id="payhint" style="display:none">Bayar Online diproses payment gateway berizin: QRIS, e-wallet, dan virtual account. Kode akses dan file tersedia otomatis setelah pembayaran lunas, tanpa kirim bukti bayar.</p>
<p class="hint" id="gwnote" style="display:none">Pembayaran online untuk produk ini sedang diaktifkan. Sementara ini gunakan invoice di bawah.</p>
<p class="hint tf" style="display:none">Invoice dan transfer bank khusus layanan sesuai surat penawaran. Rekening atas nama CV FA Indonesia (BRI). Tombol salin menyalin nomor rekening ke clipboard.</p>
<p class="hint">Butuh diskusi dulu? <a href="https://wa.me/6282245260121?text=Halo%20Pak%20Ananta%2C%20saya%20ingin%20konsultasi%20sebelum%20membeli.">Chat Ananta, CPA</a>.</p>
<section class="card" style="margin:18px 0"><h2>Langkah</h2><ol class="steps"><li class="ol-on" style="display:none"><b>Bayar Online:</b> klik Bayar Online, pilih metode, selesaikan pembayaran. Kode akses dan link unduh langsung tampil, juga dikirim ke email.</li>
<li class="tf" style="display:none">Transfer bank: buat invoice, lalu simpan sebagai PDF (tombol Simpan PDF).</li><li class="tf" style="display:none">Transfer sesuai total ke rekening BRI CV FA Indonesia. Tulis nomor invoice di berita transfer.</li><li class="tf" style="display:none">Kirim invoice dan bukti transfer lewat tombol Chat Ananta, CPA atau email.</li><li class="tf" style="display:none">Jadwal layanan atau akses dikirim setelah pembayaran dikonfirmasi.</li></ol></section>
'''

# JS: pemetaan Mayar harus sama dengan shared/pay_mayar.py
MODE_JS = '''/*nt24*/var MY={"eb-psp":"e-book-prosedur-audit-substantif-primer","eb-auditee":"e-book-audit-untuk-auditee-umkm","eb-lkumkm":"e-book-menyusun-laporan-keuangan-umkm","eb-akmen":"e-book-akuntansi-manajemen-untuk-umkm","eb-iso":"e-book-panduan-iso-22000-sistem-manajemen-keamanan-pangan","eb-makacua":"e-book-social-responsibility-dalam-budaya-makacua-nelayan-bugis","eb-paket":"paket-hemat-6-e-book-penerbit-fa","ar-day":"fa-jupiter-audit-ready-day-pass-1-hari","ar-year":"fa-jupiter-audit-ready-tahunan-1-tahun"};
window.FA_MAYAR=function(v){return MY[v]?'https://fa-indonesia-14404.myr.id/pl/'+MY[v]:''};
function show(sel,on){[].forEach.call(document.querySelectorAll(sel),function(e){e.style.display=on?'':'none'})}
function mode(){var v=$('prod').value,my=!!MY[v],cu=v==='custom',gw=!!window.FA_GW,on=my||gw,tf=cu||(!my&&!gw);
  show('#paynow,#payhint,.ol-on',on);show('.tf',tf);show('#gwnote',!my&&!cu&&!gw);if(!tf)$('inv').style.display='none'}
window.FA_mode=mode;
function sync(){$('customBox').style.display=$('prod').value==='custom'?'block':'none';mode()}$('prod').onchange=sync;sync();/*/nt24*/'''
OLD_SYNC = "function sync(){$('customBox').style.display=$('prod').value==='custom'?'block':'none'}$('prod').onchange=sync;sync();"
OLD_ONLOAD = "s.onload=function(){$('paynow').style.display='';$('payhint').style.display='';\n    [].forEach.call(document.querySelectorAll('.ol-on'),function(e){e.style.display=''})};"
NEW_ONLOAD = "s.onload=function(){window.FA_GW=true;if(window.FA_mode)window.FA_mode()};"
OLD_CLICK = "var b=$('paynow'),o=$('prod').selectedOptions[0],custom=o.value==='custom';"
NEW_CLICK = (OLD_CLICK + "\n  var mu=window.FA_MAYAR?window.FA_MAYAR(o.value):'';"
             "if(mu){if(window.gtag)gtag('event','begin_checkout',{currency:'IDR',items:[{item_id:o.value}]});window.open(mu,'_blank','noopener');return}"
             "\n  if(!window.snap){toast('Pembayaran online belum siap, muat ulang halaman');return}")
TOAST = [("toast(x.error||'Gagal membuat pembayaran, coba transfer bank')", "toast(x.error||'Gagal membuat pembayaran, coba lagi atau Chat Ananta, CPA')"),
         ("toast('Pembayaran gagal. Coba metode lain atau transfer bank.')", "toast('Pembayaran gagal. Coba metode lain atau Chat Ananta, CPA.')")]

SK_OLD = re.compile(r'<li>Pembayaran dilakukan secara online lewat Midtrans \(PT Midtrans, payment gateway berizin Bank Indonesia\) di <a[^>]*>faindonesia\.co\.id/bayar/</a>\.')
SK_NEW = ('<li>Pembayaran produk digital (FA Apps, e-book, kertas kerja, dan paket lain di situs ini) dilakukan secara online lewat payment gateway berizin Bank Indonesia, '
          'yaitu Mayar dan Midtrans, dari tombol Beli atau halaman <a href="/bayar/">faindonesia.co.id/bayar/</a>. '
          'Invoice dan transfer bank hanya untuk layanan profesional sesuai surat penawaran.')
BK_OLD = "Pembelian online sedang disiapkan. Begitu dibuka, klik Beli pada buku yang Anda pilih dan bayar lewat payment gateway resmi. Sementara itu, sampel setiap buku bisa dibaca gratis."
BK_NEW = "Klik Beli pada buku yang Anda pilih, halaman pembayaran terbuka di tab baru. Bayar lewat QRIS, virtual account, atau e-wallet, lalu file PDF langsung bisa diunduh. Sampel setiap buku tetap bisa dibaca gratis."

def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t): open(p, "w", encoding="utf-8").write(t)
def one(t, a, b, what):
    if t.count(a) != 1: sys.exit(f"GAGAL: '{what}' ditemukan {t.count(a)} kali")
    return t.replace(a, b)

def bayar(p):
    t = rd(p)
    if MARK in t: return "sudah"
    t, n = re.subn(r'<p class="lead">.*?</p>', LEAD, t, count=1, flags=re.S); assert n == 1
    t, n = re.subn(r'(<meta content=")[^"]*(" name="description"/?>)|(<meta name="description" content=")[^"]*(">)',
                   lambda m: (m.group(1) or m.group(3)) + DESC + (m.group(2) or m.group(4)), t, count=1); assert n == 1
    i = t.index('<div class="btns">'); j = t.index('<p class="hint" style="margin-bottom:40px">')
    t = t[:i] + BLOCK + t[j:]
    t = one(t, OLD_SYNC, MODE_JS, "sync")
    t = one(t, OLD_ONLOAD, NEW_ONLOAD, "onload")
    t = one(t, OLD_CLICK, NEW_CLICK, "click")
    for a, b in TOAST: t = one(t, a, b, a[:30])
    wr(p, t); return "diubah"

def swap(p, fn):
    t = rd(p); u = fn(t)
    if u != t: wr(p, u); return "diubah"
    return "sudah"

for R in ROOTS:
    print(os.path.relpath(R, HERE))
    print("  bayar:", bayar(os.path.join(R, "bayar", "index.html")))
    print("  syarat-ketentuan:", swap(os.path.join(R, "syarat-ketentuan", "index.html"), lambda t: SK_OLD.sub(SK_NEW, t)))
    print("  buku:", swap(os.path.join(R, "buku", "index.html"), lambda t: t.replace(BK_OLD, BK_NEW)))
