#!/usr/bin/env python3
"""FA Apps /apps/ ala halaman produk SaaS (14 Nov 2026).

Bos: "tampilan apps di FA selain untuk penunjang konsultasi, tampilannya standar orang jualan apps
seperti Mekari dan Accurate, SEO-nya juga."

Yang dikerjakan di out/faindonesia/apps/index.html (idempoten, penanda <!--fa-saas--> dan <!--fa-saas2-->):
- hero produk (H1 baru berkata kunci, dua tombol, deret fakta, mockup jendela aplikasi berdata dummy)
- bagian fitur, cara kerja 3 langkah, untuk siapa, akses (tanpa harga), FAQ + JSON-LD FAQPage dan SoftwareApplication
- title, description, og/twitter ditulis ulang; H1 lama diturunkan jadi H2 (teks tetap)
Tidak ada blok lama yang dihapus. Aturan: tanpa harga, tanpa kata "bayar", tanpa nama Ananta di kalimat narasi.
Urutan bila build ulang: setelah fa_empat_apps_20261114.py, sebelum teks_rapi_20261113.py.
Pakai --dry untuk uji tanpa menulis.
"""
import os, re, sys, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
P = os.path.join(ROOT, "out", "faindonesia", "apps", "index.html")
B = "https://faindonesia.co.id"
WA = "https://wa.me/6282245260121?text=Halo%20Pak%20Ananta%2C%20saya%20ingin%20bertanya%20tentang%20FA%20Apps."

TITLE = "FA Apps: Aplikasi Akuntansi, Audit, Valuasi, dan Kalkulator Pajak"
DESC = ("Aplikasi akuntansi dan audit buatan FA Consult: laporan keuangan siap audit, kertas kerja KAP, "
        "valuasi, kredit, dan kalkulator pajak. Coba gratis.")

FAQ = [
    ("Apa itu FA Apps?",
     "FA Apps adalah kumpulan aplikasi web buatan FA Indonesia untuk pekerjaan akuntansi, audit, pajak, dan keuangan. "
     "Ada empat aplikasi utama: FA Jupiter untuk laporan keuangan siap audit, FA Saturn untuk audit KAP, "
     "FA Venus untuk valuasi, kredit, dan strategi keuangan, serta FA Galaxy untuk belajar standar dan membaca hasil."),
    ("Apakah FA Apps bisa dicoba gratis?",
     "Bisa. Hasil ringkas dan kalkulator dapat dicoba langsung di browser. File yang diunduh, seperti laporan lengkap, "
     "template Excel, dan kertas kerja, memiliki ketentuan sendiri yang tampil di halaman masing-masing."),
    ("Apa bedanya FA Jupiter, FA Saturn, FA Venus, dan FA Galaxy?",
     "FA Jupiter menyusun atau merapikan laporan keuangan sampai siap audit. FA Saturn menjalankan alur audit dari perencanaan "
     "sampai pelaporan. FA Venus menjawab pertanyaan keputusan seperti nilai usaha, plafon kredit, dan unit cost rumah sakit. "
     "FA Galaxy adalah tempat belajar standar akuntansi dan audit serta panduan memakai tiga aplikasi lainnya."),
    ("Apakah hasil dari aplikasi menggantikan auditor atau konsultan?",
     "Tidak. Aplikasi membantu menghitung, merapikan, dan menelusuri angka. Opini audit tetap diterbitkan oleh KAP, "
     "dan hasil kalkulator adalah estimasi yang perlu ditinjau sebelum dipakai untuk keputusan atau pelaporan resmi."),
    ("Standar apa yang diikuti FA Apps?",
     "FA Jupiter menyajikan laporan keuangan mengikuti PSAK dan SAK EMKM. FA Saturn mengikuti alur Standar Audit (SA) IAPI "
     "yang merujuk ISA. FA Galaxy memuat rujukan SAK dan standar audit, termasuk materi dari Update SAK."),
    ("Bisakah tim FA mengerjakan langsung kalau laporan keuangan saya belum rapi?",
     "Bisa. Tim FA Indonesia dapat menyusun laporan keuangan, mendampingi audit, dan menyiapkan dokumen kredit atau investor. "
     "Cukup mulai dari konsultasi lewat WhatsApp."),
]

APPS = [
    ("FA Jupiter", "Laporan Keuangan Siap Audit", "/apps/jupiter/", "#f2994a",
     "Dari buku besar jadi laporan keuangan PSAK atau SAK EMKM, lengkap dengan lead schedule dan checklist PBC."),
    ("FA Saturn", "Audit dan KAP", "/apps/saturn/", "#4f8cff",
     "Perencanaan, penilaian risiko, respons risiko, dan pelaporan dalam satu alur dengan sign-off berjenjang."),
    ("FA Venus", "Valuasi, Kredit, dan Strategi", "/apps/venus/", "#e86fb0",
     "Valuasi, DCF, kapasitas kredit, DSCR, bankability, dan toolkit unit cost rumah sakit."),
    ("FA Galaxy", "Belajar dan Panduan", "/galaxy/", "#19b5a5",
     "Standar akuntansi dan audit, tutorial tiga aplikasi lain, dan Cek PSAK 118."),
]

ICON = {
    "upload": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4M7 9l5-5 5 5M4 20h16"/></svg>',
    "std": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/></svg>',
    "trail": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h10M4 18h6"/><circle cx="18" cy="16" r="3"/><path d="M20.2 18.2L22 20"/></svg>',
    "risk": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17v.5"/></svg>',
    "bank": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10l9-6 9 6M5 10v8M10 10v8M14 10v8M19 10v8M3 20h18"/></svg>',
    "team": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5.2a3.2 3.2 0 010 5.6M18 14.3c1.8.8 3 2.6 3 4.7"/></svg>',
}

FEATURES = [
    ("upload", "Upload Excel, Hasil Langsung", "Isi atau upload data dari Excel, hasil analisis langsung tampil di browser tanpa instalasi."),
    ("std", "Format Mengikuti Standar", "Laporan keuangan mengikuti PSAK dan SAK EMKM, alur audit mengikuti Standar Audit (SA) IAPI."),
    ("trail", "Jejak Angka yang Bisa Ditelusuri", "Neraca saldo, jurnal penyesuaian, lead schedule, dan kertas kerja saling terhubung sampai ke sumber angka."),
    ("risk", "Risiko Terbaca Sekali Lihat", "Tingkat risiko audit berwarna: Tinggi merah, Sedang kuning, Rendah hijau, di aplikasi dan di kertas kerja Excel."),
    ("bank", "Siap untuk Bank dan Investor", "DSCR, kapasitas kredit, bankability, dan kesiapan pendanaan dihitung dari angka usaha Anda."),
    ("team", "Dibantu Tim Bila Perlu", "Kalau hasilnya perlu dikerjakan sampai beres, tim FA Indonesia siap menyusun, mendampingi, dan menyiapkan dokumen."),
]

STEPS = [
    ("1", "Pilih Aplikasi", "Pilih FA Jupiter, Saturn, Venus, atau Galaxy sesuai pekerjaan Anda."),
    ("2", "Isi atau Upload Data", "Masukkan angka atau upload Excel. Hasil ringkas langsung tampil dan gratis dicoba."),
    ("3", "Unduh atau Minta Dikerjakan", "Unduh laporan lengkap, atau minta tim FA mengerjakannya sampai beres."),
]

AUD = [
    ("Pemilik Usaha dan Bagian Keuangan", "Susun dan rapikan laporan keuangan sampai siap audit, hitung pajak dan penyusutan.", "/apps/jupiter/", "FA Jupiter"),
    ("Auditor dan KAP", "Jalankan perencanaan, penilaian risiko, kertas kerja, dan sign-off dalam satu alur.", "/apps/saturn/", "FA Saturn"),
    ("Direksi, CFO, dan Tim Kredit", "Hitung nilai usaha, kapasitas kredit, DSCR, dan kesiapan pendanaan.", "/apps/venus/", "FA Venus"),
    ("Rumah Sakit dan Klinik", "Unit cost ABC, analisis obat, cek koding INA-CBG, dan valuasi rumah sakit.", "/fa-venus-rumah-sakit/", "Toolkit Rumah Sakit"),
    ("Mahasiswa, Dosen, dan Staf Akuntansi", "Pelajari PSAK, standar audit, dan cara membaca hasil aplikasi.", "/galaxy/", "FA Galaxy"),
]

ACCESS = [
    ("Coba Gratis", ["Hasil ringkas dan kalkulator di browser", "Tanpa instalasi dan tanpa akun", "Konsultasi awal lewat WhatsApp"]),
    ("Laporan Lengkap", ["Unduh laporan, template Excel, dan kertas kerja", "Ketentuan tampil di halaman tiap aplikasi", "Konsultasi lewat WhatsApp tetap gratis"]),
    ("Didampingi Tim FA", ["Penyusunan laporan keuangan siap audit", "Pendampingan audit dan laporan tahunan PT", "Persiapan kredit bank dan investor"]),
]

CSS1 = """<style id="sx-css">
.sx-hero{position:relative;margin:0 0 40px;padding:44px 40px 40px;border:1px solid var(--line);border-radius:18px;overflow:hidden;background:radial-gradient(900px 380px at 88% -10%,rgba(79,140,255,.20),transparent 60%),radial-gradient(700px 360px at 4% 110%,rgba(242,153,74,.16),transparent 60%),var(--panel,#1e1e1e)}
.sx-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:36px;align-items:center}
.sx-eb{display:inline-flex;align-items:center;gap:8px;margin:0 0 14px;padding:6px 12px;border:1px solid var(--line);border-radius:999px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:rgba(127,127,127,.08)}
.sx-eb i{width:7px;height:7px;border-radius:50%;background:#6FCF97;display:inline-block}
.sx-hero h1{margin:0 0 16px;font-family:var(--f-display,serif);font-weight:400;font-size:clamp(32px,4.6vw,54px);line-height:1.08;letter-spacing:0;color:var(--ink);text-transform:none}
.sx-sub{margin:0 0 24px;color:var(--muted);font-size:17px;line-height:1.6;max-width:56ch}
.sx-cta{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 26px}
.sx-cta a{display:inline-flex;align-items:center;justify-content:center;height:48px;padding:0 24px;border-radius:999px;font-weight:600;font-size:15px;text-decoration:none}
.sx-cta .p{background:#fff;color:#111}.sx-cta .p:hover{opacity:.92}
.sx-cta .w{background:#25D366;color:#06301a}.sx-cta .w:hover{opacity:.92}
.sx-facts{display:flex;flex-wrap:wrap;gap:10px 28px;margin:0;padding:18px 0 0;border-top:1px solid var(--line);list-style:none}
.sx-facts li{display:flex;flex-direction:column;gap:2px;font-size:12.5px;color:var(--muted)}
.sx-facts b{font-family:var(--f-display,serif);font-weight:400;font-size:26px;line-height:1;color:var(--ink)}
.sx-win{border:1px solid var(--line);border-radius:14px;background:#121212;box-shadow:0 30px 70px -30px rgba(0,0,0,.9);overflow:hidden}
.sx-bar{display:flex;align-items:center;gap:6px;padding:10px 14px;border-bottom:1px solid var(--line);background:#181818}
.sx-bar i{width:9px;height:9px;border-radius:50%;background:#3a3a3a;display:inline-block}
.sx-bar span{margin-left:10px;font-size:11.5px;color:var(--muted)}
.sx-body{display:grid;grid-template-columns:104px minmax(0,1fr);min-height:292px}
.sx-side{padding:12px 10px;border-right:1px solid var(--line);display:flex;flex-direction:column;gap:6px}
.sx-side span{display:block;padding:7px 9px;border-radius:7px;font-size:11.5px;color:var(--muted)}
.sx-side span.on{background:rgba(255,255,255,.08);color:var(--ink);font-weight:600}
.sx-main{padding:14px;display:flex;flex-direction:column;gap:12px}
.sx-tiles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.sx-tiles div{padding:9px 10px;border:1px solid var(--line);border-radius:8px;background:#1a1a1a}
.sx-tiles small{display:block;font-size:10.5px;color:var(--muted)}.sx-tiles b{display:block;margin-top:3px;font-size:16px;font-weight:600;color:var(--ink)}
.sx-chart{display:flex;align-items:flex-end;gap:7px;height:78px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#1a1a1a}
.sx-chart u{flex:1;border-radius:3px 3px 0 0;background:linear-gradient(180deg,#4f8cff,#2b5bbf);display:block}
.sx-rows{display:flex;flex-direction:column;gap:6px}
.sx-rows div{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:7px 10px;border:1px solid var(--line);border-radius:7px;background:#1a1a1a;font-size:11.5px;color:var(--ink)}
.sx-rows em{font-style:normal;font-size:10.5px;font-weight:600;padding:3px 8px;border-radius:999px;color:#10131a}
.sx-note{margin:8px 14px 12px;font-size:10.5px;color:var(--muted)}
.sx-sec{margin:0 0 46px}.sx-sec h2{margin:6px 0 8px;font-size:clamp(26px,3.2vw,38px);line-height:1.15}
.sx-sec .lead{margin:0 0 24px;color:var(--muted);font-size:16px;line-height:1.6;max-width:66ch}
.sx-f{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.sx-f div{padding:22px;border:1px solid var(--line);border-radius:12px;background:var(--panel,#1e1e1e)}
.sx-f svg{display:block;margin:0 0 14px;color:#fff}
.sx-f h3{margin:0 0 6px;font-family:var(--f-display,serif);font-weight:400;font-size:22px;line-height:1.2;text-transform:none;letter-spacing:0;color:var(--ink)}.sx-f h3::before{content:none;display:none}
.sx-f p{margin:0;color:var(--muted);font-size:14.5px;line-height:1.55}
.sx-st{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;counter-reset:s}
.sx-st div{position:relative;padding:24px 22px 22px;border:1px solid var(--line);border-radius:12px;background:var(--soft,#242424)}
.sx-st b.n{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;margin:0 0 12px;border-radius:50%;background:#fff;color:#111;font-size:15px}
.sx-st h3{margin:0 0 6px;font-family:var(--f-display,serif);font-weight:400;font-size:22px;text-transform:none;letter-spacing:0;color:var(--ink)}.sx-st h3::before{content:none;display:none}
.sx-st p{margin:0;color:var(--muted);font-size:14.5px;line-height:1.55}
.sx-au{display:grid;grid-template-columns:repeat(auto-fit,minmax(214px,1fr));gap:14px}
.sx-au a{display:flex;flex-direction:column;gap:8px;padding:20px;border:1px solid var(--line);border-radius:12px;background:var(--panel,#1e1e1e);color:var(--ink);text-decoration:none}
.sx-au a:hover{border-color:#fff}.sx-au b{font-family:var(--f-display,serif);font-weight:400;font-size:21px;line-height:1.2}
.sx-au span{color:var(--muted);font-size:14px;line-height:1.5}.sx-au em{margin-top:auto;font-style:normal;font-size:13px;font-weight:600;color:var(--ink)}
.sx-ac{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.sx-ac div{padding:24px;border:1px solid var(--line);border-radius:12px;background:var(--panel,#1e1e1e)}
.sx-ac div.hl{border-color:#fff;background:linear-gradient(180deg,rgba(255,255,255,.07),var(--panel,#1e1e1e))}
.sx-ac h3{margin:0 0 12px;font-family:var(--f-display,serif);font-weight:400;font-size:24px;text-transform:none;letter-spacing:0;color:var(--ink)}.sx-ac h3::before{content:none;display:none}
.sx-ac ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:9px}
.sx-ac li{position:relative;padding-left:22px;font-size:14.5px;line-height:1.5;color:var(--muted)}
.sx-ac li::before{content:"";position:absolute;left:0;top:.45em;width:12px;height:7px;border-left:2px solid #6FCF97;border-bottom:2px solid #6FCF97;transform:rotate(-45deg)}
.sx-faq details{border:1px solid var(--line);border-radius:10px;background:var(--panel,#1e1e1e);margin:0 0 10px}
.sx-faq summary{cursor:pointer;list-style:none;padding:16px 18px;font-weight:600;font-size:15.5px;color:var(--ink);display:flex;justify-content:space-between;gap:12px}
.sx-faq summary::-webkit-details-marker{display:none}.sx-faq summary::after{content:"+";font-size:20px;line-height:1;color:var(--muted)}
.sx-faq details[open] summary::after{content:"\\2212"}
.sx-faq details p{margin:0;padding:0 18px 18px;color:var(--muted);font-size:14.5px;line-height:1.65}
@media(max-width:900px){.sx-grid{grid-template-columns:1fr}.sx-f,.sx-st,.sx-ac{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.sx-hero{padding:26px 18px 24px;border-radius:14px}.sx-f,.sx-st,.sx-ac{grid-template-columns:1fr}.sx-cta a{width:100%}.sx-body{grid-template-columns:78px minmax(0,1fr)}.sx-side span{padding:6px 6px;font-size:10.5px}}
</style>"""


def esc(s):
    return html.escape(s, quote=True)


def hero():
    chart = "".join('<u style="height:%d%%"></u>' % h for h in (38, 52, 44, 66, 58, 82, 74))
    facts = [("4", "Aplikasi Utama"), ("23", "Aplikasi Live"), ("PSAK, SAK EMKM, SA", "Standar yang Diikuti")]
    fl = "".join("<li><b>%s</b>%s</li>" % (esc(a), esc(b)) for a, b in facts)
    body = (
        '<section class="sx-hero" aria-label="FA Apps"><div class="sx-grid"><div>'
        '<p class="sx-eb"><i></i>FA Apps oleh FA Consult</p>'
        '<h1>FA Apps: Aplikasi Akuntansi, Audit, dan Valuasi untuk Bisnis di Indonesia</h1>'
        '<p class="sx-sub">Susun laporan keuangan siap audit, jalankan audit berbasis risiko, dan hitung valuasi serta kapasitas kredit. '
        'Upload Excel, hasilnya langsung keluar di browser. Dibuat oleh tim yang setiap hari mengerjakan laporan keuangan, audit, dan pendanaan.</p>'
        '<div class="sx-cta"><a class="p" href="#empat-app">Coba Gratis</a>'
        '<a class="w" href="%s" rel="noopener" target="_blank">Chat Ananta, CPA</a></div>'
        '<ul class="sx-facts">%s</ul></div>'
        '<div aria-hidden="true"><div class="sx-win"><div class="sx-bar"><i></i><i></i><i></i><span>FA Apps</span></div>'
        '<div class="sx-body"><div class="sx-side"><span class="on">Saturn</span><span>Jupiter</span><span>Venus</span><span>Galaxy</span></div>'
        '<div class="sx-main"><div class="sx-tiles"><div><small>Materialitas</small><b>250 jt</b></div><div><small>Akun diuji</small><b>18</b></div><div><small>Sign-off</small><b>3 / 5</b></div></div>'
        '<div class="sx-chart">%s</div>'
        '<div class="sx-rows"><div>Pendapatan<em style="background:#F08A7E">Tinggi</em></div><div>Persediaan<em style="background:#E6B85C">Sedang</em></div><div>Kas dan Bank<em style="background:#6FCF97">Rendah</em></div></div>'
        '</div></div><p class="sx-note">Contoh tampilan dengan data dummy.</p></div></div></div></section>'
    ) % (WA, fl, chart)
    return '<!--fa-saas-->' + CSS1 + body + '<!--/fa-saas-->'


def faq_ld():
    return json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]
    }, ensure_ascii=False)


def apps_ld():
    return json.dumps({
        "@context": "https://schema.org", "@graph": [
            {"@type": "SoftwareApplication", "name": n, "alternateName": k, "url": B + u,
             "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
             "description": d, "inLanguage": "id",
             "publisher": {"@type": "Organization", "name": "FA Indonesia", "url": B + "/"}}
            for n, k, u, c, d in APPS]
    }, ensure_ascii=False)


def lower():
    feats = "".join('<div>%s<h3>%s</h3><p>%s</p></div>' % (ICON[i], esc(t), esc(d)) for i, t, d in FEATURES)
    steps = "".join('<div><b class="n">%s</b><h3>%s</h3><p>%s</p></div>' % (n, esc(t), esc(d)) for n, t, d in STEPS)
    aud = "".join('<a href="%s"><b>%s</b><span>%s</span><em>Buka %s &rarr;</em></a>' % (u, esc(t), esc(d), esc(a)) for t, d, u, a in AUD)
    acc = "".join('<div%s><h3>%s</h3><ul>%s</ul></div>' % (' class="hl"' if i == 0 else "", esc(t), "".join("<li>%s</li>" % esc(x) for x in li))
                  for i, (t, li) in enumerate(ACCESS))
    faq = "".join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else "", esc(q), esc(a)) for i, (q, a) in enumerate(FAQ))
    return (
        '<!--fa-saas2-->'
        '<section class="sx-sec" id="fitur" aria-label="Fitur"><p class="kick">Kenapa FA Apps</p><h2>Dibuat untuk Pekerjaan Keuangan yang Sebenarnya</h2>'
        '<p class="lead">Setiap aplikasi lahir dari pekerjaan nyata menyusun laporan keuangan, mengaudit, dan menyiapkan pendanaan, bukan dari template umum.</p>'
        '<div class="sx-f">%s</div></section>'
        '<section class="sx-sec" id="cara-kerja-apps" aria-label="Cara kerja"><p class="kick">Cara Kerja</p><h2>Tiga Langkah dari Angka Mentah ke Hasil</h2><div class="sx-st">%s</div></section>'
        '<section class="sx-sec" id="untuk-siapa" aria-label="Untuk siapa"><p class="kick">Untuk Siapa</p><h2>Pilih Aplikasi Sesuai Peran Anda</h2><div class="sx-au">%s</div></section>'
        '<section class="sx-sec" id="akses" aria-label="Akses"><p class="kick">Cara Memakai</p><h2>Mulai Gratis, Lanjut Sesuai Kebutuhan</h2>'
        '<p class="lead">Coba dulu, lihat hasilnya, lalu putuskan apakah Anda butuh laporan lengkap atau pendampingan tim.</p><div class="sx-ac">%s</div></section>'
        '<section class="sx-sec sx-faq" id="faq-apps" aria-label="Pertanyaan umum"><p class="kick">FAQ</p><h2>Pertanyaan tentang FA Apps</h2>%s</section>'
        '<script type="application/ld+json">%s</script><script type="application/ld+json">%s</script><!--/fa-saas2-->'
    ) % (feats, steps, aud, acc, faq, faq_ld(), apps_ld())


def strip(h):
    h = re.sub(r'<!--fa-saas-->.*?<!--/fa-saas-->', '', h, flags=re.S)
    h = re.sub(r'<!--fa-saas2-->.*?<!--/fa-saas2-->', '', h, flags=re.S)
    return h


def main():
    h = open(P, encoding="utf-8").read()
    h = strip(h)
    old_h1 = re.search(r'<h1 style="font-family:var\(--f-display\);font-weight:400;font-size:clamp\(24px,3vw,30px\)[^>]*>(.*?)</h1>', h, re.S)
    if old_h1:
        h = h.replace(old_h1.group(0), old_h1.group(0).replace('<h1 ', '<h2 ', 1).replace('</h1>', '</h2>'))
    # hero sebelum blok video (bmp3a)
    assert '<!--bmp3a-->' in h, "penanda bmp3a tidak ada"
    h = h.replace('<!--bmp3a-->', hero() + '<!--bmp3a-->', 1)
    # bagian fitur dst sebelum katalog penuh
    key = '<section class="sec">\n<h3>FA Apps · 23 Aplikasi Live</h3>'
    assert key in h, "penanda katalog tidak ada"
    h = h.replace(key, lower() + key, 1)
    # title dan description
    assert 1 <= len(TITLE) <= 65 and len(DESC) <= 158, (len(TITLE), len(DESC))
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % esc(TITLE), h, count=1, flags=re.S)
    h = re.sub(r'(<meta[^>]*?(?:name|property)="(?:og:title|twitter:title)"[^>]*?content=")[^"]*(")', lambda m: m.group(1) + esc(TITLE) + m.group(2), h)
    h = re.sub(r'(<meta[^>]*?content=")[^"]*("[^>]*?(?:name|property)="(?:og:title|twitter:title)")', lambda m: m.group(1) + esc(TITLE) + m.group(2), h)
    h = re.sub(r'(<meta[^>]*?content=")[^"]*("[^>]*?(?:name|property)="(?:description|og:description|twitter:description)")', lambda m: m.group(1) + esc(DESC) + m.group(2), h)
    h = re.sub(r'(<meta[^>]*?(?:name|property)="(?:description|og:description|twitter:description)"[^>]*?content=")[^"]*(")', lambda m: m.group(1) + esc(DESC) + m.group(2), h)
    if not DRY:
        open(P, "w", encoding="utf-8").write(h)
    print("OK" if not DRY else "DRY", len(h), "title", len(TITLE), "desc", len(DESC))


if __name__ == "__main__":
    main()
