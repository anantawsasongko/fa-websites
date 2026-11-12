#!/usr/bin/env python3
"""Rapi kolom halaman daerah + intake "Audit untuk Apa" (12 Nov 2026).
BEKERJA LANGSUNG DI out/faindonesia, idempoten, jalankan PALING AKHIR (setelah blue_ocean_20261112.py).

Pemicu (Bos): halaman daerah (contoh /jasa-audit-laporan-keuangan/makassar/) tidak serapi landing:
margin dan lebar blok berbeda-beda, "Layanan Lain" berupa deretan link panjang yang tidak terlipat,
tabel terpotong di HP. Dari calon klien yang masuk: 40% butuh audit, 10% all in, 20% RS bermasalah,
30% terlalu kecil atau tidak jelas, jadi setiap kotak kontak audit/LK sekarang menanyakan keperluan
dan omzet sebelum chat (pesan WhatsApp ikut terisi) supaya lead tersaring sejak pesan pertama.

Isi:
1. Halaman berblok fanas-x (6.110): satu lebar kolom 820px untuk paragraf, kotak kontak, tim, peta isi,
   tabel, FAQ; kartu KAP DHN sejajar kolom; tabel 2 sampai 3 kolom membungkus di HP (tidak terpotong).
2. "Layanan Lain di <Kota>" + baris fa-kw3x dan fa-ind12x: tiap kelompok jadi akordeon tertutup
   (details.rg) berisi chip link. Penanda komentar lama tidak disentuh.
3. Kotak fa-lk2 (4.393 halaman): dua pilihan (keperluan, omzet setahun) di atas tombol; /js/fa-intake.js
   menyisipkan jawabannya ke pesan WhatsApp. Tanpa JS tombol tetap berfungsi seperti semula.
4. "&amp;amp;" (ampersand ganda) dibetulkan.
5. Daftar "Semua Kecamatan dan Desa di <Kota>" (1.531 halaman) yang terbuka sejak awal jadi terlipat.
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv

CSS = ('<style id="rapi12">'
       # satu kolom
       '.wrap.art:has(.fnx)>p,.wrap.art:has(.fnx)>p.t,.wrap.art:has(.fnx)>.lk2,.wrap.art:has(.fnx)>div,'
       '.wrap.art:has(.fnx)>nav,.wrap.art:has(.fnx)>section,.wrap.art:has(.fnx)>.faq-acc,.wrap.art:has(.fnx)>.tblwrap'
       '{max-width:820px!important;box-sizing:border-box}'
       '.wrap.art:has(.fnx)>h1{max-width:900px}.wrap.art:has(.fnx) h2{max-width:820px;box-sizing:border-box}'
       '.wrap.art:has(.fnx) .tblwrap table,.wrap.art:has(.fnx)>div>table{width:100%}'
       '.wrap.art:has(.fnx)>.lk2{margin:26px 0 0!important;padding:20px 22px!important}'
       '.wrap.art:has(.fnx)>.cbtns{margin:24px 0 0!important}'
       '.wrap.art:has(.fnx)>p{margin:0 0 14px}'
       '.wrap.art:has(.fnx)>.pf-map{margin:28px 0 8px}'
       '.wrap.art:has(.fnx) .faq-acc{margin:6px 0 22px}'
       '.wrap.art:has(.fnx)>div>table th,.wrap.art:has(.fnx)>div>table td{padding:10px 12px}'
       'main:has(.fnx)~.dhnc,main:has(.fnx)~.dhns{width:min(820px,calc(100% - 2*clamp(16px,4vw,40px)))!important;'
       'margin-left:max(clamp(16px,4vw,40px),calc((100% - 1000px)/2 + clamp(16px,4vw,40px)))!important;margin-right:auto!important}'
       # akordeon layanan lain
       '.fnx h2{margin-bottom:6px!important}'
       'details.rg{border-bottom:1px solid #333;max-width:820px}'
       '.fnx>details.rg:first-of-type{border-top:1px solid #333}'
       'details.rg>summary{list-style:none;cursor:pointer;padding:15px 36px 15px 0;position:relative;font-weight:600;'
       'font-size:16.5px;line-height:1.45;display:flex;gap:10px;align-items:baseline}'
       'details.rg>summary::-webkit-details-marker{display:none}'
       'details.rg>summary:after{content:"+";position:absolute;right:4px;top:10px;font-size:22px;font-weight:300;transition:transform .25s}'
       'details.rg[open]>summary:after{transform:rotate(45deg)}'
       'details.rg>summary i{font-style:normal;font-weight:400;font-size:13px;opacity:.6}'
       '.rg-l{display:flex;flex-wrap:wrap;gap:8px;padding:2px 0 18px}'
       '.rg-l a{display:inline-block;padding:7px 13px;border:1px solid rgba(127,127,127,.4);border-radius:999px;'
       'font-size:14px;line-height:1.3;text-decoration:none!important;color:inherit}'
       '.rg-l a:hover{border-color:currentColor}'
       # intake
       '.lk2-q{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:14px 0 4px}'
       '.lk2-q label{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;opacity:.75;font-weight:600}'
       '.lk2-q select{display:block;width:100%;margin-top:6px;padding:10px 12px;border-radius:8px;border:1px solid rgba(127,127,127,.5);'
       'background:#161616;color:#fff;font:inherit;font-size:15px;letter-spacing:0;text-transform:none;font-weight:400}'
       '@media(max-width:640px){.lk2-q{grid-template-columns:1fr}'
       'main table:not(:has(th:nth-child(4))){min-width:0!important;width:100%}'
       'main table:not(:has(th:nth-child(4))) th,main table:not(:has(th:nth-child(4))) td{min-width:0!important;width:auto!important;'
       'max-width:none!important;white-space:normal!important;overflow-wrap:break-word;word-break:normal;padding:9px 10px}'
       'main table:has(th:nth-child(3)):not(:has(th:nth-child(4))){table-layout:fixed}'
       'main table:has(th:nth-child(3)):not(:has(th:nth-child(4))) th,main table:has(th:nth-child(3)):not(:has(th:nth-child(4))) td'
       '{font-size:14px!important;line-height:1.5!important;padding:8px!important;overflow-wrap:anywhere}'
       '.wrap.art:has(.fnx)>.lk2{padding:16px!important}}'
       '</style>')

INTAKE = ('<div class="lk2-q"><label>Untuk Keperluan Apa<select data-q="perlu" aria-label="Untuk keperluan apa">'
          '<option value="">Pilih keperluan</option><option>Kredit bank</option><option>Investor atau jual usaha</option>'
          '<option>Tender atau mitra usaha</option><option>Laporan tahunan PT (SABH)</option><option>Pajak</option>'
          '<option>Persiapan IPO</option><option>Belum tahu, ingin tanya dulu</option></select></label>'
          '<label>Omzet Setahun<select data-q="omzet" aria-label="Omzet setahun">'
          '<option value="">Pilih kisaran</option><option>Di bawah Rp5 miliar</option><option>Rp5 sampai 50 miliar</option>'
          '<option>Rp50 sampai 500 miliar</option><option>Di atas Rp500 miliar</option></select></label></div>')

JS = r"""/* Intake kotak kontak (12 Nov 2026): keperluan + omzet ikut ke pesan WhatsApp. */
(function(){
  document.querySelectorAll('.lk2').forEach(function(box){
    var sel=box.querySelectorAll('.lk2-q select'); if(!sel.length) return;
    var links=[].slice.call(box.querySelectorAll('a[href*="wa.me"]'));
    links.forEach(function(a){ a.dataset.base=a.getAttribute('href'); });
    function upd(){
      var perlu=sel[0].value, omzet=sel[1]?sel[1].value:'';
      links.forEach(function(a){
        var u=a.dataset.base, i=u.indexOf('text='); if(i<0) return;
        var t=decodeURIComponent(u.slice(i+5));
        t=t.replace(/\s*Keperluan: bank \/ SABH \/ tender \/ investor\.?/,'');
        if(perlu) t+=' Keperluan: '+perlu+'.';
        if(omzet) t+=' Omzet setahun: '+omzet+'.';
        a.setAttribute('href',u.slice(0,i+5)+encodeURIComponent(t));
      });
    }
    [].forEach.call(sel,function(s){ s.addEventListener('change',upd); });
  });
})();
"""
JSTAG = '<script defer src="/js/fa-intake.js"></script>'

GRP = re.compile(r'<p class="t"><b>([^<:]+):</b>\s*((?:<a [^>]*>[^<]*</a>(?:\s*·\s*)?)+)</p>')


def fold_groups(seg):
    def rep(m):
        links = re.findall(r'<a [^>]*>[^<]*</a>', m.group(2))
        return ('<details class="rg"><summary>%s <i>%d</i></summary><div class="rg-l">%s</div></details>'
                % (m.group(1).strip(), len(links), ''.join(links)))
    return GRP.sub(rep, seg)


def process(t):
    o = t
    t = t.replace('&amp;amp;', '&amp;')
    t = re.sub(r'<details open=""><summary>(Semua [Kk]ecamatan)', r'<details><summary>\1', t)
    has_fnx = '<section class="fnx">' in t
    has_lk2 = '<!--fa-lk2-->' in t
    if has_fnx:
        i = t.index('<section class="fnx">')
        j = t.find('<h2', t.index('</section>', i))
        if j < 0:
            j = t.find('</main>', i)
        t = t[:i] + fold_groups(t[i:j]) + t[j:]
    if has_lk2 and 'class="lk2-q"' not in t:
        i = t.index('<!--fa-lk2-->'); j = t.index('<!--/fa-lk2-->', i)
        b = t[i:j]
        k = b.find('</p>')
        if k > 0 and b.count('wa.me') >= 1:
            b = b[:k + 4] + INTAKE + b[k + 4:]
            t = t[:i] + b + t[j:]
    if 'class="lk2-q"' in t and JSTAG not in t:
        t = t.replace('</body>', JSTAG + '</body>', 1)
    if has_fnx or has_lk2:
        t = re.sub(r'<style id="rapi12">.*?</style>', '', t, flags=re.S)
        t = t.replace('</head>', CSS + '</head>', 1)
    return t, t != o


def main():
    n = 0
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            if not f.endswith('.html'):
                continue
            p = os.path.join(d, f)
            t = open(p, encoding='utf-8').read()
            t2, ch = process(t)
            if ch:
                n += 1
                if not DRY:
                    open(p, 'w', encoding='utf-8').write(t2)
    jp = os.path.join(ROOT, 'js', 'fa-intake.js')
    if not DRY and (not os.path.exists(jp) or open(jp, encoding='utf-8').read() != JS):
        open(jp, 'w', encoding='utf-8').write(JS)
    print('rapi kolom:', n, 'file', '(dry)' if DRY else '')


if __name__ == '__main__':
    main()
