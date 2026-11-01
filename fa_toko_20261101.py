# -*- coding: utf-8 -*-
"""Toko FA (1 Nov 2026): satu toko pusat di faindonesia.co.id/toko/ untuk semua produk berbayar
(e-book Penerbit FA, paket hemat, aplikasi FA Jupiter Audit Ready) yang dibayar lewat /bayar/ (QRIS, GoPay, VA via Midtrans, atau transfer BRI).
Harga sama persis dengan PRODUCTS di shared/pay/_worker.js. Tab "Toko" dipasang di nav FA, CariAkuntan, UpdateSAK oleh prep.py.
?dari=cariakuntan atau ?dari=updatesak menampilkan rekomendasi yang cocok. Idempoten (menulis ulang toko/index.html).
"""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_mitra_20261027.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. MITRA RM BANK")]
_src = _src.replace('TODAY = "2026-10-27"', 'TODAY = "2026-11-01"').replace("27 Oktober 2026", "1 November 2026")
exec(compile(_src, "fa_mitra_helpers", "exec"))

URL = D + "/toko/"
def rp(n): return "Rp" + f"{n:,}".replace(",", ".")

# (id, slug cover, kategori, judul, deskripsi singkat, harga, catatan, untuk, link detail, label detail)
BOOKS = [
 ("eb-psp", "prosedur-audit-substantif-primer", "Audit", "Prosedur Audit Substantif Primer", "Prosedur substantif per akun: asersi, konfirmasi bank, pisah batas, sampai valuasi. PDF 282 halaman.", 129000, "us ca"),
 ("eb-auditee", "audit-untuk-auditee-umkm", "Audit", "Audit untuk Auditee UMKM", "Apa yang diminta auditor dan apa yang harus disiapkan perusahaan sebelum audit pertama. PDF 88 halaman.", 59000, "ca"),
 ("eb-lkumkm", "menyusun-laporan-keuangan-umkm", "Laporan Keuangan", "Menyusun Laporan Keuangan UMKM", "Dari double entry, COA, jurnal, sampai laporan keuangan sesuai SAK EMKM. PDF 93 halaman.", 69000, "ca us"),
 ("eb-akmen", "akuntansi-manajemen-umkm", "Manajemen", "Akuntansi Manajemen untuk UMKM", "Biaya, harga pokok, titik impas, dan anggaran untuk keputusan pemilik usaha.", 49000, ""),
 ("eb-iso", "panduan-iso-22000", "Sistem Mutu", "Panduan ISO 22000", "Sistem manajemen keamanan pangan untuk usaha makanan dan minuman.", 59000, ""),
 ("eb-makacua", "social-responsibility-makacua", "Riset", "Social Responsibility Makacua", "Tanggung jawab sosial dalam budaya Makacua nelayan Bugis.", 39000, ""),
]
NORMAL = sum(b[5] for b in BOOKS); PAKET = 299000

CSS = """<style id="tk-css">
.tk{--tk-a:#fca5a5;--tk-card:#1e1e1e;--tk-l:#2f2f2f}
.tk *{min-width:0}
.tk .tkh{display:grid;grid-template-columns:1.25fr .9fr;gap:40px;align-items:center}
.tk h1{font-family:"Times New Roman",Times,serif;font-size:clamp(32px,4vw,50px);line-height:1.1;margin:.2em 0 .35em}
.tk .lede{color:#bdbdbd;max-width:56ch;font-size:17px}
.tk .pay{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0}
.tk .pay span{border:1px solid #3a3a3a;border-radius:999px;padding:6px 13px;font-size:13px;color:#e5e5e5;background:#1b1b1b;white-space:nowrap}
.tk .pay span b{color:#fff}
.tk .trust{display:grid;gap:12px}
.tk .trust div{display:flex;gap:14px;align-items:flex-start;border:1px solid var(--tk-l);background:linear-gradient(135deg,#1f1f1f,#191919);border-radius:14px;padding:16px 18px}
.tk .trust i{flex:0 0 34px;height:34px;border-radius:10px;background:#2a1515;color:var(--tk-a);display:grid;place-items:center;font-style:normal;font-weight:600}
.tk .trust b{display:block;font-size:15px}.tk .trust span{color:#a8a8a8;font-size:13.5px;line-height:1.5}
.tk .chips{display:flex;flex-wrap:wrap;gap:8px;margin:38px 0 22px;border-bottom:1px solid var(--tk-l);padding-bottom:18px}
.tk .chips button{font:inherit;font-size:14px;cursor:pointer;border:1px solid #3a3a3a;background:transparent;color:#e5e5e5;border-radius:999px;padding:8px 16px}
.tk .chips button[aria-pressed="true"]{background:#fff;color:#111;border-color:#fff}
.tk .chips small{opacity:.6;margin-left:4px}
.tk .rec{display:none;border:1px solid #5b2a2a;background:#231616;border-radius:12px;padding:12px 16px;margin:0 0 18px;font-size:14.5px;color:#f3d6d6}
.tk .rec.on{display:block}
.tk .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}
.tk .it{display:flex;flex-direction:column;border:1px solid var(--tk-l);background:var(--tk-card);border-radius:16px;overflow:hidden;transition:transform .2s,border-color .2s}
.tk .it:hover{transform:translateY(-3px);border-color:#4a4a4a}
.tk .it[hidden]{display:none}
.tk .cv{position:relative;display:block;aspect-ratio:4/3;background:radial-gradient(circle at 30% 20%,#2b2b2b,#141414);overflow:hidden}
.tk .cv img{position:absolute;left:50%;top:14px;transform:translateX(-50%);height:calc(100% - 28px);width:auto;max-width:none;border-radius:4px;box-shadow:0 12px 26px rgba(0,0,0,.55)}
.tk .cv .rb{position:absolute;left:12px;top:12px;background:var(--tk-a);color:#2a0c0c;font-size:11.5px;font-weight:600;letter-spacing:.04em;border-radius:999px;padding:3px 10px;display:none}
.tk .it.pick .cv .rb{display:block}
.tk .app{display:grid;place-items:center;background:linear-gradient(135deg,#3b0f0f,#111 70%)}
.tk .app .ic{width:46%;aspect-ratio:1;border-radius:22%;background:linear-gradient(140deg,#7f1d1d,#1a1a1a);border:1px solid #5a2a2a;display:grid;place-items:center;box-shadow:0 14px 30px rgba(0,0,0,.5)}
.tk .app .ic svg{width:56%;height:56%}
.tk .app em{position:absolute;bottom:12px;left:0;right:0;text-align:center;font-style:normal;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#d4d4d4}
.tk .in{display:flex;flex-direction:column;gap:6px;padding:16px 16px 18px;flex:1}
.tk .tg{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--tk-a)}
.tk .in h3{font-family:"Times New Roman",Times,serif;font-size:20px;line-height:1.2;margin:0}
.tk .in p{color:#a8a8a8;font-size:14px;line-height:1.5;margin:0}
.tk .pr{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin-top:auto;padding-top:10px}
.tk .pr b{font-size:20px}.tk .pr small{color:#8f8f8f;font-size:12.5px}
.tk .ac{display:flex;gap:8px;margin-top:10px}
.tk .ac a{flex:1;text-align:center;border-radius:10px;padding:10px 8px;font-size:14px;text-decoration:none;white-space:nowrap}
.tk .ac .b{background:#fff;color:#111;font-weight:600}
.tk .ac .s{border:1px solid #444;color:#e5e5e5}
.tk .pk{grid-column:1/-1;display:grid;grid-template-columns:1.1fr 1fr;gap:0;border:1px solid #6b2b2b;background:linear-gradient(120deg,#2a1212,#1a1a1a 60%);border-radius:18px;overflow:hidden}
.tk .pk .fan{position:relative;min-height:250px}
.tk .pk .fan img{position:absolute;bottom:22px;width:24%;height:auto;max-width:none;border-radius:4px;box-shadow:0 14px 28px rgba(0,0,0,.6);transform-origin:bottom center}
.tk .pk .in{padding:28px 28px 26px;justify-content:center}
.tk .pk h3{font-size:clamp(24px,2.6vw,32px)}
.tk .pk .pr s{color:#8f8f8f;font-size:15px}.tk .pk .pr b{font-size:28px}
.tk .pk .save{display:inline-block;background:var(--tk-a);color:#2a0c0c;font-weight:600;font-size:13px;border-radius:999px;padding:4px 12px}
.tk .pk .ac{max-width:420px}
.tk .flow{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:56px 0 0;counter-reset:s}
.tk .flow div{border-top:2px solid #fff;padding-top:14px}
.tk .flow div:before{counter-increment:s;content:"0" counter(s);font-size:13px;letter-spacing:.14em;color:var(--tk-a)}
.tk .flow b{display:block;font-size:17px;margin:4px 0}.tk .flow span{color:#a8a8a8;font-size:14px}
.tk .free{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.tk .free a{display:block;border:1px dashed #444;border-radius:14px;padding:16px 18px;text-decoration:none}
.tk .free a b{display:block;font-size:16px}.tk .free a span{color:#a8a8a8;font-size:13.5px}
.tk h2.h{font-family:"Times New Roman",Times,serif;font-size:clamp(26px,3vw,36px);margin:56px 0 16px}
.tk .faq details{border-bottom:1px solid var(--tk-l);padding:14px 0}
.tk .faq summary{cursor:pointer;font-size:16px}.tk .faq p{color:#a8a8a8;margin-top:8px;font-size:14.5px}
@media (max-width:900px){.tk .tkh{grid-template-columns:1fr;gap:26px}.tk .pk{grid-template-columns:1fr}.tk .pk .fan{min-height:200px}.tk .free{grid-template-columns:1fr}}
@media (max-width:620px){.tk .grid{grid-template-columns:1fr 1fr;gap:12px}.tk .in{padding:12px 12px 14px}.tk .in h3{font-size:16.5px}.tk .in p{font-size:13px}
 .tk .pr b{font-size:17px}.tk .ac{flex-direction:column}.tk .ac a{padding:9px 6px;font-size:13.5px}.tk .flow{grid-template-columns:1fr}.tk .chips button{padding:7px 13px;font-size:13.5px}
 .tk .pk .in{padding:20px 18px}.tk .pk .ac{flex-direction:row}
 .tk .cv .rb{left:8px;top:8px;font-size:10.5px;padding:2px 8px}.tk .app .ic{width:36%;margin-top:6px}.tk .app em{display:none}.tk .cv img{top:34px;height:calc(100% - 42px)}.tk .it:not(.pick) .cv img{top:12px;height:calc(100% - 24px)}}
@media (max-width:360px){.tk .grid{grid-template-columns:1fr}}
</style>"""

APP_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M7 15l3-3 3 2 4-5"/><path d="M7 7h4"/></svg>')

def card(pid, cat, tag, title, desc, price, note, cover_html, sec_href, sec_lbl, forr="", cls="", buy="Beli"):
    return (f'<article class="it{cls}" data-cat="{cat}" data-for="{forr}" id="p-{pid}">{cover_html}<div class="in"><span class="tg">{E(tag)}</span>'
            f'<h3>{E(title)}</h3><p>{E(desc)}</p><div class="pr"><b>{rp(price)}</b><small>{E(note)}</small></div>'
            f'<div class="ac"><a class="b" href="/bayar/?produk={pid}" data-buy="{pid}">{buy}</a><a class="s" href="{sec_href}">{E(sec_lbl)}</a></div></div></article>')

items = []
# paket di depan, satu baris penuh
fan = "".join(f'<img src="/img/buku/{b[1]}.jpg" width="600" height="891" loading="lazy" decoding="async" alt="" style="left:{6 + i * 13}%;transform:rotate({(i - 2.5) * 5:.1f}deg);z-index:{i}">' for i, b in enumerate(BOOKS))
items.append(f'<article class="pk it" data-cat="paket" data-for="ca us" id="p-eb-paket"><div class="fan" aria-hidden="true">{fan}</div><div class="in">'
             f'<span class="tg">Paket Hemat · 6 E-Book</span><h3>Semua E-Book Penerbit FA</h3>'
             f'<p>Enam buku audit, laporan keuangan, akuntansi manajemen, dan riset dalam satu pembelian. Cocok untuk tim keuangan, kantor akuntan, dan perpustakaan kampus.</p>'
             f'<div class="pr"><s>{rp(NORMAL)}</s><b>{rp(PAKET)}</b><span class="save">Hemat {rp(NORMAL - PAKET)}</span></div>'
             f'<div class="ac"><a class="b" href="/bayar/?produk=eb-paket" data-buy="eb-paket">Beli Paket</a><a class="s" href="/buku/#paket">Lihat Isi Paket</a></div></div></article>')
for pid, slug, tag, title, desc, price, forr in BOOKS:
    cov = (f'<a class="cv" href="/buku/#{slug}" aria-label="Detail {E(title)}"><span class="rb">Rekomendasi</span>'
           f'<img src="/img/buku/{slug}.jpg" width="600" height="891" loading="lazy" decoding="async" alt="Sampul {E(title)}"></a>')
    items.append(card(pid, "ebook", "E-Book · " + tag, title, desc, price, "bebas PPN · PDF", cov, f"/buku/#{slug}", "Baca Sampel", forr))
for pid, title, desc, price, note in [
    ("ar-day", "FA Jupiter Audit Ready: Day Pass", "Upload COA dan GL dari Xero, Accurate, atau Jurnal. Jadi trial balance, laporan keuangan, lead schedule, dan checklist PBC.", 39000, "termasuk PPN · berlaku sampai besok"),
    ("ar-year", "FA Jupiter Audit Ready: Tahunan", "Akses penuh satu tahun untuk menyiapkan laporan keuangan audit ready setiap periode, termasuk kalkulator industri.", 249000, "termasuk PPN · berlaku 1 tahun"),
]:
    cov = (f'<a class="cv app" href="/audit-ready/" aria-label="Buka {E(title)}"><span class="rb">Rekomendasi</span><span class="ic">{APP_SVG}</span><em>FA Jupiter</em></a>')
    items.append(card(pid, "app", "Aplikasi · FA Jupiter", title, desc, price, note, cov, "/audit-ready/", "Coba Aplikasi", "ca us" if pid == "ar-day" else "ca"))

n_eb, n_app = len(BOOKS), 2
chips = (f'<div class="chips" role="toolbar" aria-label="Kategori produk">'
         f'<button type="button" data-f="all" aria-pressed="true">Semua<small>{n_eb + n_app + 1}</small></button>'
         f'<button type="button" data-f="ebook" aria-pressed="false">E-Book<small>{n_eb}</small></button>'
         f'<button type="button" data-f="app" aria-pressed="false">Aplikasi<small>{n_app}</small></button>'
         f'<button type="button" data-f="paket" aria-pressed="false">Paket Hemat<small>1</small></button>'
         f'<button type="button" data-f="free" aria-pressed="false">Gratis</button></div>')

FAQ = [
 ("Metode pembayaran apa saja?", "QRIS (semua e-wallet dan m-banking), GoPay, dan virtual account semua bank lewat Midtrans. Bisa juga transfer ke rekening BRI CV FA Indonesia dengan invoice otomatis dari halaman bayar."),
 ("Kapan produk saya terima?", "Kode akses aplikasi FA Jupiter tampil otomatis setelah pembayaran lunas. File PDF e-book dan password dikirim ke email atau WhatsApp setelah pembayaran dikonfirmasi, biasanya di hari yang sama pada jam kerja."),
 ("Apakah harga sudah termasuk pajak?", "E-book dibebaskan dari PPN, jadi harga yang tertera adalah harga akhir. Harga aplikasi sudah termasuk PPN dan faktur pajak dapat diminta dengan mengirim data NPWP atau NIK."),
 ("Bisa minta invoice atas nama perusahaan?", "Bisa. Isi nama perusahaan di halaman bayar, invoice dibuat otomatis dan bisa diunduh atau dicetak."),
 ("Bagaimana dengan refund?", "E-book yang password-nya sudah dikirim tidak dapat di-refund kecuali file rusak dan tidak bisa kami ganti. Detail ada di Kebijakan Refund."),
 ("Bisa beli banyak untuk kantor atau kampus?", "Bisa. Untuk 10 lisensi atau lebih, gunakan tombol Chat Ananta, CPA untuk harga khusus."),
]
faq_block = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)

inner = f"""{CSS}
<section class="block tk">
<div class="wrap">
<div class="tkh"><div>
<p class="eyebrow">Toko FA Indonesia</p>
<h1>E-Book dan Aplikasi Akuntansi, Bayar Pakai QRIS</h1>
<p class="lede">Semua produk FA Indonesia dalam satu tempat: e-book Penerbit FA, paket hemat, dan aplikasi FA Jupiter untuk menyiapkan laporan keuangan audit ready. Pilih produk, bayar, lalu terima di hari yang sama.</p>
<div class="pay" aria-label="Metode pembayaran"><span><b>QRIS</b></span><span><b>GoPay</b></span><span><b>Virtual Account</b> semua bank</span><span><b>Transfer BRI</b></span></div>
</div>
<div class="trust">
<div><i>1</i><p><b>Pembayaran Aman via Midtrans</b><span>Gateway berizin Bank Indonesia. Data kartu dan rekening tidak melewati server kami.</span></p></div>
<div><i>2</i><p><b>Invoice Otomatis</b><span>Atas nama pribadi atau perusahaan, siap untuk bukti biaya.</span></p></div>
<div><i>3</i><p><b>Kirim Cepat</b><span>Kode akses aplikasi tampil begitu lunas. PDF e-book dikirim ke email atau WhatsApp.</span></p></div>
</div></div>
{chips}
<p class="rec" id="tk-rec" role="status"></p>
<div class="grid" id="tk-grid">
{"".join(items)}
</div>
<div id="tk-free">
<h2 class="h" id="gratis">Gratis untuk Dicoba Dulu</h2>
<div class="free">
<a href="/buku/#unduhan"><b>Materi dan Template Gratis</b><span>Unduh materi pelatihan, template, dan sampel e-book Penerbit FA.</span></a>
<a href="/apps/"><b>Kalkulator dan Aplikasi Gratis</b><span>Cek kapasitas kredit, DSCR, kelayakan IPO, dan konverter PSAK.</span></a>
<a href="https://updatesak.com/materi/" target="_blank" rel="noopener"><b>Materi PSAK di UpdateSAK</b><span>Ringkasan standar, studi kasus, dan cheat sheet PDF.</span></a>
</div></div>
<div class="flow"><div><b>Pilih</b><span>Klik Beli pada produk. Halaman bayar terbuka dengan produk sudah terpilih.</span></div>
<div><b>Bayar</b><span>QRIS, GoPay, virtual account, atau transfer BRI. Invoice dibuat otomatis.</span></div>
<div><b>Terima</b><span>Kode akses aplikasi langsung tampil. E-book dikirim ke email atau WhatsApp.</span></div></div>
<h2 class="h">Pertanyaan Seputar Pembelian</h2>
<div class="faq">{faq_block}</div>
<p style="margin-top:26px;font-size:14px;color:#a8a8a8">Ketentuan: <a href="/syarat-ketentuan/">Syarat &amp; Ketentuan</a> · <a href="/kebijakan-refund/">Kebijakan Refund</a>.</p>
{btns("Halo FA Indonesia, saya ingin bertanya tentang produk di Toko FA.")}
</div>
</section>
<script>
(function(){{
var g=document.getElementById('tk-grid'),fr=document.getElementById('tk-free'),bs=document.querySelectorAll('.tk .chips button'),rec=document.getElementById('tk-rec');
function set(f){{bs.forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.f===f?'true':'false')}});
 if(f==='free'){{g.style.display='none';fr.scrollIntoView({{behavior:'smooth',block:'start'}});return}}
 g.style.display='';g.querySelectorAll('.it').forEach(function(it){{it.hidden=!(f==='all'||it.dataset.cat===f)}});}}
bs.forEach(function(b){{b.addEventListener('click',function(){{set(b.dataset.f);try{{history.replaceState(null,'',b.dataset.f==='all'?location.pathname+location.search:'#'+b.dataset.f)}}catch(e){{}}}})}});
var h=(location.hash||'').slice(1);if(['ebook','app','paket'].indexOf(h)>=0)set(h);
var d=(new URLSearchParams(location.search).get('dari')||'').toLowerCase(),k=d.indexOf('cari')===0?'ca':d.indexOf('update')===0?'us':'';
if(k){{rec.textContent=k==='ca'?'Dari CariAkuntan: produk bertanda Rekomendasi membantu perusahaan menyiapkan laporan keuangan dan dokumen sebelum diaudit KAP.':'Dari UpdateSAK: produk bertanda Rekomendasi melengkapi materi PSAK untuk praktik audit dan penyusunan laporan keuangan.';rec.classList.add('on');
 var first=g.querySelector('.it:not(.pk)');g.querySelectorAll('.it:not(.pk)').forEach(function(it){{if((' '+it.dataset.for+' ').indexOf(' '+k+' ')>=0){{it.classList.add('pick');g.insertBefore(it,first)}}}});}}
}})();
</script>"""

ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "@id": URL, "url": URL, "name": "Toko FA Indonesia", "inLanguage": "id", "isPartOf": {"@id": D + "/#website"},
     "description": "E-book Penerbit FA dan aplikasi FA Jupiter Audit Ready, bayar pakai QRIS, GoPay, virtual account, atau transfer."},
    crumbs([("Beranda", D + "/"), ("Toko", URL)]),
    {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Product", "name": n, "url": URL + "#p-" + pid,
        "brand": {"@type": "Brand", "name": "FA Indonesia"},
        "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "IDR", "availability": "https://schema.org/InStock", "url": D + "/bayar/?produk=" + pid}}}
        for i, (pid, n, p) in enumerate([("eb-paket", "Paket 6 E-book Penerbit FA", PAKET)] + [(b[0], "E-book " + b[3], b[5]) for b in BOOKS]
                                         + [("ar-day", "FA Jupiter Audit Ready Day Pass", 39000), ("ar-year", "FA Jupiter Audit Ready Tahunan", 249000)])]}]}

s = set_head(TPL_SVC, "Toko FA Indonesia: E-Book Akuntansi dan Aplikasi, Bayar QRIS",
             "Beli e-book Penerbit FA dan aplikasi FA Jupiter Audit Ready. Bayar pakai QRIS, GoPay, virtual account, atau transfer BRI. Invoice otomatis, kirim di hari yang sama.",
             URL, ld)
s = set_main(s, inner)
os.makedirs(P("toko"), exist_ok=True)
wtxt(P("toko", "index.html"), s)

def strip_t(t): return re.sub(r"<!--fa-toko-->.*?<!--/fa-toko-->\n?", "", t, flags=re.S)
sm = strip_t(rd(P("sitemap.xml")))
wtxt(P("sitemap.xml"), sm.replace("</urlset>", f"<!--fa-toko-->\n<url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><priority>0.9</priority></url>\n<!--/fa-toko-->\n</urlset>"))
ll = re.sub(r"\n- \[Toko FA\].*", "", rd(P("llms.txt")))
wtxt(P("llms.txt"), ll.rstrip("\n") + f"\n- [Toko FA]({URL}): e-book Penerbit FA dan aplikasi FA Jupiter Audit Ready, bayar QRIS, GoPay, VA, transfer BRI\n")
print("toko:", URL, len(items), "produk")
