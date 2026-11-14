#!/usr/bin/env python3
"""FA: tab RFP menggantikan tab Eksplor + halaman /rfp/ (14 Nov 2026).

Pemicu (Bos, contoh KPMG "Submit RFP"): "Harusnya ada tab RFP, daripada
tab Eksplor. Backlink di Eksplor gak hilang kalau tabnya diganti RFP resmi by
email kan? Tapi tombol WA tetep banyak tersebar."

- Menu atas semua halaman FA: <a data-i18n="kwws" href="/artikel/">Eksplor</a>
  diganti <a data-i18n="krfp" href="/rfp/">RFP</a>. Halaman /artikel/ dan
  semua artikel TIDAK berubah (URL, sitemap, link footer "Artikel" tetap),
  jadi indeks dan backlink aman. Kamus I18N: krfp EN "RFP", ZH "RFP".
- Halaman baru /rfp/ (kerangka dari /mitra-notaris/): form RFP resmi yang
  menyusun email terstruktur ke ananta@faindonesia.co.id (mailto, lampiran
  ditambahkan di aplikasi email). Tombol WA lain di situs tidak disentuh.
- sitemap.xml dan llms.txt.
Idempoten, --dry.
"""
import os, re, sys, json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, 'out', 'faindonesia')
DRY = '--dry' in sys.argv
EMAIL = 'ananta@faindonesia.co.id'
URL = 'https://faindonesia.co.id/rfp/'
TITLE = 'Ajukan Request for Proposal (RFP) | FA Indonesia'
DESC = ('Kirim Request for Proposal resmi ke FA Indonesia untuk kredit bank, investor, M&A, IPO, '
        'valuasi, audit, laporan keuangan, dan konsultasi rumah sakit.')

NAV_OLD = re.compile(r'<a (?:data-i18n="kwws" )?href="/artikel/">Eksplor</a>')
NAV_NEW = '<a data-i18n="krfp" href="/rfp/">RFP</a>'

LAYANAN = [
    'Kredit bank dan pembiayaan',
    'Investor, M&A, atau IPO',
    'Valuasi usaha',
    'Audit laporan keuangan (KAP DHN & Rekan)',
    'Penyusunan laporan keuangan (KJA Farhani K.N.)',
    'Konsultasi rumah sakit dan klinik',
    'Fractional CFO',
    'Penerapan PSAK',
    'Lainnya',
]
ANGGARAN = ['Belum ditentukan', 'Di bawah Rp50 juta', 'Rp50 sampai 250 juta',
            'Rp250 juta sampai Rp1 miliar', 'Di atas Rp1 miliar']

CSS = '''<style id="rfp-css">
.rfp-steps{list-style:none;padding:0!important;margin:1.4em 0 2em!important;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-top:1px solid rgba(255,255,255,.16);border-bottom:1px solid rgba(255,255,255,.16)}
.rfp-steps li{margin:0!important;padding:18px 18px 16px 0}
.rfp-steps li+li{padding-left:18px;border-left:1px solid rgba(255,255,255,.12)}
.rfp-steps b{display:block;font-family:var(--fa-serif,'Newsreader',serif);font-weight:400;font-size:30px;line-height:1;color:#fff;margin-bottom:8px}
.rfp-steps span{display:block;font-size:14px;line-height:1.5;color:rgba(255,255,255,.72)}
@media(max-width:640px){.rfp-steps{grid-template-columns:1fr}.rfp-steps li,.rfp-steps li+li{padding:14px 0;border-left:0}.rfp-steps li+li{border-top:1px solid rgba(255,255,255,.12)}}
form.rfp{margin:1.2em 0 2em;padding:28px;border:1px solid rgba(255,255,255,.14);border-top:2px solid #fff;border-radius:3px;background:rgba(255,255,255,.025)}
form.rfp fieldset{border:0;margin:0 0 22px;padding:0}
form.rfp legend{font-family:var(--fa-serif,'Newsreader',serif);font-size:22px;font-weight:400;color:#fff;margin:0 0 12px;padding:0}
form.rfp .g{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 16px}
form.rfp .g .w{grid-column:1/-1}
form.rfp label{display:block;font-size:13px;font-weight:600;letter-spacing:.02em;color:rgba(255,255,255,.8)}
form.rfp label em{color:#fff;font-style:normal}
form.rfp input,form.rfp select,form.rfp textarea{display:block;width:100%;box-sizing:border-box;margin-top:6px;padding:11px 12px;font:inherit;font-size:15px;color:#fff;background:#121212;border:1px solid rgba(255,255,255,.22);border-radius:2px;outline:none}
form.rfp textarea{min-height:140px;resize:vertical;line-height:1.55}
form.rfp input:focus,form.rfp select:focus,form.rfp textarea:focus{border-color:#fff}
form.rfp .ck{display:flex;gap:10px;align-items:flex-start;font-weight:400;font-size:14px;line-height:1.5;color:rgba(255,255,255,.78)}
form.rfp .ck input{width:auto;margin:3px 0 0}
form.rfp .ck a{color:#fff}
form.rfp .act{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:20px}
form.rfp button{cursor:pointer;padding:13px 22px;font:inherit;font-weight:600;font-size:15px;border-radius:2px;border:1px solid #fff;background:#fff;color:#111}
form.rfp button.ln{background:transparent;color:#fff;border-color:rgba(255,255,255,.4)}
form.rfp .note{font-size:13px;line-height:1.55;color:rgba(255,255,255,.6);margin:14px 0 0!important}
form.rfp .err{color:#ff9b8a;font-size:13px;margin:10px 0 0!important;display:none}
.rfp-ok{display:none;margin:1em 0 2em;padding:20px 22px;border:1px solid rgba(255,255,255,.2);border-left:2px solid #fff}
.rfp-ok pre{white-space:pre-wrap;font:13px/1.55 ui-monospace,Menlo,monospace;color:rgba(255,255,255,.8);background:#101010;padding:14px;max-height:260px;overflow:auto;margin:12px 0 0}
@media(max-width:640px){form.rfp{padding:20px 16px}form.rfp .g{grid-template-columns:1fr}}
</style>'''


def opts(xs, ph):
    return '<option value="">%s</option>' % ph + ''.join('<option>%s</option>' % x.replace('&', '&amp;') for x in xs)


MAIN = '''<main id="top">
<section class="block">
<div class="wrap art">
<p class="eyebrow">Request for Proposal</p>
<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">Ajukan Request for Proposal (RFP)</h1>
<p class="t" style="max-width:62em">Untuk perusahaan, rumah sakit, yayasan, dan investor yang membutuhkan proposal resmi dari FA Indonesia. Isi ringkasan kebutuhan Anda; form ini menyusun email RFP yang rapi ke tim kami, lengkap dengan ruang lingkup dan tenggat proposal.</p>
<ol class="rfp-steps">
<li><b>01</b><span>Isi form dan kirim email RFP. Dokumen pendukung dilampirkan di email.</span></li>
<li><b>02</b><span>Tim FA Indonesia mengonfirmasi penerimaan dan, bila perlu, mengirim NDA sebelum data dibuka.</span></li>
<li><b>03</b><span>Proposal resmi berisi ruang lingkup, tim, jadwal, dan skema kerja sama dikirim ke email Anda.</span></li>
</ol>
<form class="rfp" id="rfp" novalidate>
<fieldset><legend>Data Kontak</legend><div class="g">
<label>Nama Lengkap <em>*</em><input name="nama" required autocomplete="name"/></label>
<label>Jabatan <em>*</em><input name="jabatan" required autocomplete="organization-title"/></label>
<label>Nama Perusahaan atau Institusi <em>*</em><input name="perusahaan" required autocomplete="organization"/></label>
<label>Email Kantor <em>*</em><input name="email" type="email" required autocomplete="email"/></label>
<label>Telepon atau WhatsApp<input name="telepon" type="tel" autocomplete="tel"/></label>
<label>Kota<input name="kota" autocomplete="address-level2"/></label>
</div></fieldset>
<fieldset><legend>Kebutuhan</legend><div class="g">
<label>Layanan <em>*</em><select name="layanan" required>%(layanan)s</select></label>
<label>Industri<input name="industri" placeholder="Contoh: rumah sakit, manufaktur, distribusi"/></label>
<label class="w">Latar Belakang dan Ruang Lingkup <em>*</em><textarea name="lingkup" required placeholder="Tujuan, kondisi saat ini, periode laporan, jumlah entitas, pihak yang akan memakai hasilnya (bank, investor, regulator)."></textarea></label>
<label>Batas Waktu Proposal<input name="tenggat" type="date"/></label>
<label>Anggaran Indikatif<select name="anggaran">%(anggaran)s</select></label>
</div></fieldset>
<label class="ck"><input type="checkbox" name="setuju" required/> <span>Saya setuju data ini dipakai untuk menyusun proposal sesuai <a href="/kebijakan-privasi/">Kebijakan Privasi</a> FA Indonesia.</span></label>
<p class="err" id="rfp-err">Lengkapi kolom bertanda * dan centang persetujuan.</p>
<div class="act"><button type="submit">Kirim RFP via Email</button><button class="ln" type="button" id="rfp-copy">Salin Teks RFP</button></div>
<p class="note">Tombol kirim membuka aplikasi email Anda dengan RFP yang sudah tersusun ke %(email)s. Lampirkan dokumen pendukung (laporan keuangan, TOR, atau dokumen tender) sebelum mengirim.</p>
</form>
<div class="rfp-ok" id="rfp-ok"><b>Email RFP sudah disiapkan.</b><p style="margin:.4em 0 0">Bila aplikasi email tidak terbuka, salin teks di bawah dan kirim ke <a href="mailto:%(email)s">%(email)s</a>.</p><pre id="rfp-txt"></pre></div>
<h2 id="kerahasiaan">Kerahasiaan</h2>
<p>Informasi dalam RFP hanya dipakai untuk menyusun proposal. Bila data keuangan atau dokumen transaksi perlu dibuka, NDA ditandatangani lebih dulu. Untuk audit, penyusun laporan keuangan dan auditor selalu pihak yang berbeda.</p>
<h2 id="tanpa-form">Tanpa Form</h2>
<p>RFP atau undangan tender dari bank, BUMN, rumah sakit, dan yayasan juga bisa dikirim langsung ke <a href="mailto:%(email)s?subject=RFP%%20untuk%%20FA%%20Indonesia">%(email)s</a>. Untuk pertanyaan singkat sebelum mengirim RFP, gunakan tombol WhatsApp di halaman ini.</p>
<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px"><a class="btn line" href="https://wa.me/6282245260121?text=Halo%%20Pak%%20Ananta%%2C%%20saya%%20ingin%%20bertanya%%20sebelum%%20mengirim%%20RFP." rel="noopener" target="_blank">Chat Ananta, CPA</a><a class="btn line" href="/layanan/">Lihat Layanan</a></div>
</div>
</section>
</main>'''

JS = '''<script id="rfp-js">(function(){var f=document.getElementById('rfp');if(!f)return;var E='%s';
function v(n){var e=f.elements[n];return e?(e.value||'').trim():''}
function txt(){var L=[['Nama',v('nama')],['Jabatan',v('jabatan')],['Perusahaan',v('perusahaan')],['Email',v('email')],['Telepon/WA',v('telepon')],['Kota',v('kota')],['Layanan',v('layanan')],['Industri',v('industri')],['Batas waktu proposal',v('tenggat')],['Anggaran indikatif',v('anggaran')]];
var s='Kepada Tim FA Indonesia,\\n\\nBersama ini kami mengajukan Request for Proposal (RFP).\\n\\n';L.forEach(function(x){if(x[1])s+=x[0]+': '+x[1]+'\\n'});
s+='\\nLatar belakang dan ruang lingkup:\\n'+v('lingkup')+'\\n\\nDokumen pendukung terlampir (bila ada).\\n\\nHormat kami,\\n'+v('nama')+'\\n'+v('jabatan')+', '+v('perusahaan');return s}
function subj(){return 'RFP '+v('layanan')+' - '+v('perusahaan')}
function ok(){var r=['nama','jabatan','perusahaan','email','layanan','lingkup'].every(function(n){return v(n)})&&/@/.test(v('email'))&&f.elements.setuju.checked;document.getElementById('rfp-err').style.display=r?'none':'block';return r}
function show(){var o=document.getElementById('rfp-ok');document.getElementById('rfp-txt').textContent='Kepada: '+E+'\\nSubjek: '+subj()+'\\n\\n'+txt();o.style.display='block'}
f.addEventListener('submit',function(e){e.preventDefault();if(!ok())return;show();try{gtag('event','generate_lead',{method:'rfp_email',service:v('layanan')})}catch(x){}
location.href='mailto:'+E+'?subject='+encodeURIComponent(subj())+'&body='+encodeURIComponent(txt())});
document.getElementById('rfp-copy').addEventListener('click',function(){if(!ok())return;show();var t='Kepada: '+E+'\\nSubjek: '+subj()+'\\n\\n'+txt();try{navigator.clipboard.writeText(t);this.textContent='Tersalin'}catch(x){}try{gtag('event','generate_lead',{method:'rfp_copy',service:v('layanan')})}catch(x){}});
})();</script>''' % EMAIL

LD = {"@context": "https://schema.org", "@graph": [
    {"@type": "ContactPage", "@id": URL + "#page", "url": URL, "name": "Ajukan Request for Proposal (RFP)",
     "description": DESC, "inLanguage": "id-ID",
     "about": {"@type": "ProfessionalService", "@id": "https://faindonesia.co.id/#org", "name": "FA Indonesia",
               "url": "https://faindonesia.co.id/", "email": EMAIL}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Beranda", "item": "https://faindonesia.co.id/"},
        {"@type": "ListItem", "position": 2, "name": "RFP", "item": URL}]}]}


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def build_page():
    h = open(os.path.join(ROOT, 'mitra-notaris', 'index.html'), encoding='utf-8').read()
    old_title = re.search(r'<title>([^<]*)</title>', h).group(1)
    old_desc = re.search(r'<meta content="([^"]*)" name="description"/>', h).group(1)
    h = h.replace('<title>%s</title>' % old_title, '<title>%s</title>' % TITLE.replace('&', '&amp;'))
    h = h.replace('content="%s"' % old_title, 'content="%s"' % esc(TITLE))
    h = h.replace('content="%s"' % old_desc, 'content="%s"' % esc(DESC))
    h = h.replace('https://faindonesia.co.id/mitra-notaris/', URL)
    h = h.replace('/img/og-page/mitra-notaris.jpg', '/img/og-page/layanan.jpg')
    h = h.replace('content="profile" property="og:type"', 'content="website" property="og:type"')
    h = re.sub(r'<script type="application/ld\+json">.*?</script>',
               lambda _: '<script type="application/ld+json">%s</script>' % json.dumps(LD, ensure_ascii=False),
               h, count=1, flags=re.S)
    i, j = h.find('<main'), h.find('</main>') + len('</main>')
    main = MAIN % {'layanan': opts(LAYANAN, 'Pilih layanan'), 'anggaran': opts(ANGGARAN, 'Pilih kisaran'),
                   'email': EMAIL}
    h = h[:i] + main + h[j:]
    h = h.replace('</head>', CSS + '</head>', 1) if 'id="rfp-css"' not in h else h
    h = h.replace('</body>', JS + '</body>', 1)
    h = NAV_OLD.sub(NAV_NEW, h)
    assert 'mitra-notaris/"' not in h.split('<main')[0], 'sisa URL lama di head'
    return h


LAY_CTA = ('<div class="lay12-cta"><a class="btn solid" href="/rfp/">Ajukan RFP</a>'
           '<a class="btn line" href="https://wa.me/6282245260121?text=Halo%20Pak%20Ananta%2C%20saya%20ingin%20tanya%20layanan%20FA%20Indonesia." '
           'rel="noopener" target="_blank">Chat Ananta, CPA</a></div>')
LAY_CSS = ('<style id="lay-hero">main>.subhero{position:relative;isolation:isolate;padding:140px 0 72px!important}'
           'main>.subhero::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;'
           'background:linear-gradient(180deg,rgba(18,18,18,.35) 0%,rgba(18,18,18,.7) 60%,rgba(18,18,18,1) 100%),'
           'url(/img/fa/landscape.jpg) center 35%/cover no-repeat;filter:grayscale(1)}'
           'main>.subhero h1{font-family:"Newsreader","Times New Roman",serif!important;font-weight:400!important;letter-spacing:-.015em;font-size:clamp(40px,5.2vw,72px)!important;line-height:1.04!important;margin:.15em 0 .5em!important}'
           '.lay12-cta{display:flex;gap:12px;flex-wrap:wrap;align-items:center}'
           '.lay12-cta .btn{display:inline-flex!important;justify-content:center;align-items:center;border-radius:2px!important;font-weight:600;min-width:170px;text-align:center;box-sizing:border-box}'
           '</style>')


def layanan():
    p = os.path.join(ROOT, 'layanan', 'index.html')
    h = open(p, encoding='utf-8').read()
    o = h
    h = re.sub(r'<div class="lay12-cta">.*?</div>', lambda _: LAY_CTA, h, count=1, flags=re.S)
    if 'id="lay-hero"' in h:
        h = re.sub(r'<style id="lay-hero">.*?</style>', lambda _: LAY_CSS, h, count=1, flags=re.S)
    else:
        h = h.replace('</head>', LAY_CSS + '</head>', 1)
    if h != o and not DRY:
        open(p, 'w', encoding='utf-8').write(h)
    return int(h != o)


def main():
    n = layanan()
    page = build_page()
    out = os.path.join(ROOT, 'rfp', 'index.html')
    if not os.path.exists(out) or open(out, encoding='utf-8').read() != page:
        n += 1
        if not DRY:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(page)
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            p = os.path.join(root, fn)
            h = open(p, encoding='utf-8', errors='surrogateescape').read()
            o = h
            h = NAV_OLD.sub(NAV_NEW, h)
            h = h.replace('"kwws": "Explore", "ktoko"', '"kwws": "Explore", "krfp": "RFP", "ktoko"')
            h = h.replace('"kwws": "探索", "ktoko"', '"kwws": "探索", "krfp": "RFP", "ktoko"')
            if h != o:
                n += 1
                if not DRY:
                    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(h)
    sm = os.path.join(ROOT, 'sitemap.xml')
    s = open(sm, encoding='utf-8').read()
    if URL not in s:
        s = s.replace('</urlset>', '<url><loc>%s</loc><lastmod>2026-11-14</lastmod><priority>0.8</priority></url>\n</urlset>' % URL)
        n += 1
        if not DRY:
            open(sm, 'w', encoding='utf-8').write(s)
    ll = os.path.join(ROOT, 'llms.txt')
    t = open(ll, encoding='utf-8').read()
    if URL not in t:
        t = t.rstrip('\n') + '\n- Ajukan Request for Proposal (RFP) resmi via email → %s\n' % URL
        n += 1
        if not DRY:
            open(ll, 'w', encoding='utf-8').write(t)
    print(('DRY ' if DRY else '') + 'berubah: %d file' % n)


if __name__ == '__main__':
    main()
