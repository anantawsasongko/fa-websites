#!/usr/bin/env python3
"""Tab Layanan diringkas (12 Nov 2026 malam). BEKERJA LANGSUNG DI out/faindonesia/layanan/index.html,
idempoten (penanda <!--lay12-->), jalankan setelah semua script lain yang menyentuh /layanan/.

Pemicu (Bos): "tab Layanan urutannya masih berantakan. Masih ada apps. Masih ada yang ruwet ruwet.
Rapikan, layanannya apa, dan rekam jejak, dan klien. Tombol Chat Ananta, CPA. Udah."

Isi halaman sekarang hanya: (0) Galeri paling atas (Bos: "harusnya di atas sendiri"), (1) Layanan, lima kelompok berurutan dari yang paling sering dicari,
(2) Rekam Jejak (daftar lama, tanpa lipatan; "Penugasan Lainnya" dilipat), (3) Klien dan bank,
(4) tombol Chat Ananta, CPA. Dibuang dari halaman ini: apps dan kalkulator, tools buatan FA, Untuk Mitra,
Skema Kerja Sama, Paket Fractional, blok tim, afiliasi, badan usaha, lini usaha.
Halaman tujuan link-link itu sendiri tidak dihapus.
"""
import os, re, sys

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia', 'layanan', 'index.html')
WA = ('https://wa.me/6282245260121?text=Halo%20Pak%20Ananta%2C%20saya%20ingin%20tanya%20layanan%20FA%20Indonesia.')
BTN = f'<a class="btn solid" href="{WA}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'

GROUPS = [
    ('Laporan Keuangan dan Audit',
     'Penyusunan oleh KJA Farhani K.N., audit oleh KAP DHN &amp; Rekan yang terdaftar OJK. Untuk bank, laporan tahunan PT, tender, dan investor.',
     [('/jasa-penyusunan-laporan-keuangan/', 'Penyusunan Laporan Keuangan'),
      ('/jasa-audit-laporan-keuangan/', 'Audit Laporan Keuangan'),
      ('/laporan-keuangan-umkm/', 'Laporan Keuangan UMKM'),
      ('/jasa-laporan-keuangan-bulanan/', 'Pembukuan dan Laporan Bulanan'),
      ('/laporan-tahunan-pt/', 'Laporan Tahunan PT (SABH)'),
      ('/jasa-pendampingan-audit/', 'Pendampingan Audit'),
      ('/jasa-implementasi-psak/', 'Penerapan PSAK'),
      ('/audit-laporan-keuangan-per-industri/', 'Audit per Industri')]),
    ('Kredit Bank dan Pendanaan',
     'Menyiapkan laporan, proyeksi, dan dokumen pengajuan sampai fasilitas cair atau investor masuk.',
     [('/konsultan-kredit-bank/', 'Pendampingan Kredit Bank'),
      ('/konsultan-kredit-distributor-importir/', 'Kredit Distributor dan Importir'),
      ('/jasa-valuasi-usaha/', 'Valuasi Usaha'),
      ('/konsultan-persiapan-ipo/', 'Persiapan IPO')]),
    ('Rumah Sakit dan Klinik',
     'Keuangan, unit cost, tarif, pendanaan, serta jual beli rumah sakit dan klinik.',
     [('/konsultan-rumah-sakit/', 'Konsultan Rumah Sakit'),
      ('/konsultan-unit-cost-rumah-sakit/', 'Unit Cost Rumah Sakit'),
      ('/konsultan-klinik/', 'Konsultan Klinik'),
      ('/rumah-sakit-dijual/', 'Jual Beli Rumah Sakit dan BPR')]),
    ('CFO dan Tata Kelola',
     'Fungsi keuangan yang dijalankan dari luar, pengendalian internal, dan penghitungan kerugian.',
     [('/cfo-paruh-waktu/', 'CFO Paruh Waktu'),
      ('/pendampingan-gcg/', 'Pendampingan GCG'),
      ('/komite-audit-komisaris-independen/', 'Komite Audit dan Komisaris Independen'),
      ('/akuntan-forensik/', 'Akuntan Forensik')]),
    ('Sektor Khusus',
     'Laporan dan audit dengan aturan tersendiri.',
     [('/jasa-audit-laporan-keuangan-bpr/', 'Audit BPR dan BPRS'),
      ('/audit-koperasi-desa-merah-putih/', 'Koperasi Desa Merah Putih'),
      ('/laporan-keuangan-audit-sppg/', 'Laporan dan Audit SPPG'),
      ('/audit-dana-kampanye/', 'Audit Dana Kampanye')]),
]

CSS = ('<style id="lay12">'
       '.lay12{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 48px;margin-top:26px}'
       '.lay12 article{padding:26px 0;border-top:1px solid var(--line)}'
       '.lay12 .no{font-family:var(--mono);font-size:13px;color:var(--red)}'
       '.lay12 h3{margin:6px 0 8px;font-size:22px;line-height:1.25}'
       '.lay12 p{margin:0 0 14px;color:var(--muted);font-size:15px;line-height:1.6;max-width:46ch}'
       '.lay12 ul{list-style:none;margin:0;padding:0}'
       '.lay12 li{border-top:1px solid var(--line)}'
       '.lay12 li a{display:flex;justify-content:space-between;gap:12px;padding:11px 0;color:inherit;text-decoration:none;font-size:15.5px}'
       '.lay12 li a:after{content:"\\2192";opacity:.5}'
       '.lay12 li a:hover:after{opacity:1}'
       '.lay12-kota{margin:22px 0 0;font-size:15px}'
       '.lay12-cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}'
       '#rekam details.lay12-d{margin-top:22px;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}'
       '#rekam details.lay12-d>summary{cursor:pointer;padding:16px 0;font-weight:600;list-style:none;display:flex;justify-content:space-between}'
       '#rekam details.lay12-d>summary::-webkit-details-marker{display:none}'
       '#rekam details.lay12-d>summary:after{content:"+";font-size:22px;font-weight:300;line-height:1}'
       '#rekam details.lay12-d[open]>summary:after{content:"\\2212"}'
       '#rekam details.lay12-d h3{margin:18px 0 6px;font-size:17px}'
       '@media(max-width:760px){.lay12{grid-template-columns:1fr}.lay12 h3{font-size:20px}}'
       '</style>')


def section(m, sid):
    a = m.find(f'id="{sid}"')
    if a < 0:
        raise SystemExit(f'section {sid} tidak ditemukan')
    a = m.rfind('<section', 0, a)
    b = m.find('</section>', a) + len('</section>')
    return m[a:b]


def inner(s, start_pat, end_pat):
    a = re.search(start_pat, s, re.S)
    b = s.find(end_pat, a.end())
    return s[a.start():b + len(end_pat)]


def main():
    t = open(P, encoding='utf-8').read()
    if '<!--lay12-->' in t:
        print('sudah ringkas, tidak diubah')
        return
    i = t.index('<main')
    i2 = t.index('>', i) + 1
    j = t.index('</main>')
    m = t[i2:j]

    rekam = section(m, 'rekam')
    log = inner(rekam, r'<ul class="log">', '</ul>')
    note = re.search(r'<p class="note"[^>]*>.*?</p>', rekam[rekam.find('</ul>'):], re.S)
    note = note.group(0) if note else ''
    bank = inner(rekam, r'<div class="lenders">', '</ul>') + '\n</div>'
    klien = rekam[rekam.find('<div class="lenders clients">'):]
    klien = klien[:klien.find('</p>', klien.find('class="others"')) + 4] + '\n</div>'
    klien = klien.replace('<p class="eyebrow" data-i18n="k285">Klien</p>', '')
    galeri = section(m, 'galeri-layanan')
    arsip = section(m, 'arsip')
    arsip_body = arsip[arsip.find('</h2>') + 5:arsip.rfind('</div>')]
    arsip_body = re.sub(r'^\s*</div>', '', arsip_body.strip())

    cards = []
    for n, (title, desc, links) in enumerate(GROUPS, 1):
        li = ''.join(f'<li><a href="{u}">{x}</a></li>' for u, x in links)
        cards.append(f'<article><span class="no">{n:02d}</span><h3>{title}</h3><p>{desc}</p><ul>{li}</ul></article>')

    new = f'''<!--lay12-->
<section class="block subhero hs"><div class="wrap"><p class="eyebrow">FA Indonesia</p><h1 data-i18n="hs49">Layanan &amp; Rekam Jejak</h1><div class="lay12-cta">{BTN}</div></div></section>
{galeri}
<section class="block" id="layanan">
<div class="wrap">
<div class="head"><p class="eyebrow">Layanan</p><h2>Yang Kami Kerjakan</h2></div>
<div class="lay12">{''.join(cards)}</div>
<p class="lay12-kota">Melayani seluruh Indonesia. <a href="/wilayah/">Lihat layanan per kota</a>.</p>
</div>
</section>
<section class="block alt" id="rekam">
<div class="wrap">
<div class="head"><p class="eyebrow" data-i18n="k104">Rekam Jejak</p><h2 data-i18n="k105">Penugasan Pilihan</h2></div>
{log}
{note}
<details class="lay12-d"><summary>Penugasan Lainnya Sejak 2016</summary><div>{arsip_body}</div></details>
</div>
</section>
<section class="block" id="klien">
<div class="wrap">
<div class="head"><p class="eyebrow">Klien</p><h2>Klien dan Bank</h2></div>
{klien}
{bank}
<div class="lay12-cta" style="margin-top:36px">{BTN}</div>
</div>
</section>
<!--/lay12-->'''
    main_open = t[i:i2]
    t = t[:i] + main_open + new + t[j:]
    if 'id="lay12"' not in t:
        t = t.replace('</head>', CSS + '</head>', 1)
    if '--dry' not in sys.argv:
        open(P, 'w', encoding='utf-8').write(t)
    print('layanan diringkas:', len(m), '->', len(new), 'karakter isi')


if __name__ == '__main__':
    main()
