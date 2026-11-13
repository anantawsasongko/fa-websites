#!/usr/bin/env python3
"""Tiga video "How FA Indonesia Works" (Jupiter, Saturn, Venus) di bagian Rekam Jejak /layanan/ (13 Nov 2026).
BEKERJA LANGSUNG DI out/faindonesia/layanan/index.html, idempoten (penanda <!--bmp3--> ... <!--/bmp3-->).
Jalankan SETELAH fa_bumper_rekam_20261112.py (blok disisipkan tepat setelah <!--/bmp10-->) dan SEBELUM fa_rendah_hati_20261112.py.

Pemicu (Bos): "Upload di web semua ya dan bisa di share." Tujuan video (Bos): bukan menjual apps, tetapi menunjukkan
bahwa hasil kerja FA kuantitatif dan didukung alat buatan sendiri. Karena itu blok ini tidak memuat ajakan mencoba apps.
Aset: media/cara-kerja-fa-{jupiter,saturn,venus}.mp4 (1080x1920, 30 detik, di bawah 24 MB) dan .jpg (poster).
"""
import os, re, shutil, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'FA-Indonesia_Website_SIAP-UPLOAD-v58', 'media')
OUT = os.path.join(ROOT, 'out', 'faindonesia')
P = os.path.join(OUT, 'layanan', 'index.html')
BASE = 'https://faindonesia.co.id'
ITEMS = [
    ('jupiter', 'FA Jupiter', 'Laporan keuangan disusun dari buku besar, baris demi baris.'),
    ('saturn', 'FA Saturn', 'Pekerjaan audit direncanakan, diuji, dan ditandatangani dalam satu jejak.'),
    ('venus', 'FA Venus', 'Valuasi, kredit, dan biaya dijawab dengan model hitung.'),
]

CSS = ('<style id="bmp3-css">'
       '.bmp3{margin:0 0 56px;padding:0 0 48px;border-bottom:1px solid var(--line)}'
       '.bmp3 h2{margin:8px 0 12px;font-size:clamp(26px,3.2vw,38px);line-height:1.15}'
       '.bmp3>p.lead{margin:0 0 28px;color:var(--muted);font-size:16px;line-height:1.65;max-width:62ch}'
       '.bmp3 .g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}'
       '.bmp3 .v{position:relative;aspect-ratio:9/16;background:#06080c;border-radius:14px;overflow:hidden}'
       '.bmp3 video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}'
       '.bmp3 h3{margin:16px 0 6px;font-size:20px;line-height:1.25}'
       '.bmp3 .it p{margin:0;color:var(--muted);font-size:15px;line-height:1.6}'
       '.bmp3 .sh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:14px}'
       '.bmp3 .sh .fxs{margin:0}.bmp3 .sh .fxs>span{display:none}'
       '.bmp3 .vb{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;'
       'gap:7px;height:38px;padding:0 14px;border-radius:999px;border:1px solid rgba(127,127,127,.38);color:inherit;'
       'font:600 .84rem/1 inherit;font-family:inherit;opacity:.85;transition:background .2s,opacity .2s}'
       '.bmp3 .vb:hover,.bmp3 .vb:focus-visible{opacity:1;background:rgba(127,127,127,.14);border-color:rgba(127,127,127,.6)}'
       '.bmp3 .vb svg{width:16px;height:16px;flex:none}'
       '.bmp3 .ok{font-size:13px;color:var(--muted);margin:10px 0 0;min-height:18px}'
       '@media(max-width:860px){.bmp3 .g{grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:min(72vw,300px);'
       'overflow-x:auto;scroll-snap-type:x mandatory;gap:18px;padding-bottom:8px;-webkit-overflow-scrolling:touch}'
       '.bmp3 .it{scroll-snap-align:start}}'
       '</style>')


def item(slug, name, cap):
    vid = '/media/cara-kerja-fa-%s.mp4' % slug; pos = '/media/cara-kerja-fa-%s.jpg' % slug
    url = BASE + '/layanan/#cara-kerja-' + slug; title = 'Cara Kerja FA Indonesia: ' + name
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'VideoObject', 'name': title, 'description': cap,
                     'thumbnailUrl': BASE + pos, 'contentUrl': BASE + vid, 'uploadDate': '2026-11-13', 'duration': 'PT30S',
                     'inLanguage': 'en', 'publisher': {'@type': 'Organization', 'name': 'FA Indonesia', 'url': BASE + '/'}},
                    ensure_ascii=False)
    return ('<div class="it" id="cara-kerja-%s"><div class="v"><video controls playsinline preload="none" poster="%s" '
            'aria-label="Video %s"><source src="%s" type="video/mp4"/></video></div>'
            '<h3>%s</h3><p>%s</p>'
            '<div class="sh"><div class="share" data-url="%s" data-tool="%s" data-kick="FA Indonesia" data-lab="Bagikan">'
            '<span data-story="%s" data-title="%s" hidden></span></div>'
            '<button type="button" class="vb" data-bmp3="%s" data-name="cara-kerja-fa-%s.mp4" data-title="%s" '
            'title="Bagikan file video" aria-label="Bagikan file video %s">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="13" height="12" rx="2"/>'
            '<path d="M16 10l5-3v10l-5-3z"/></svg><span>Video</span></button></div>'
            '<script type="application/ld+json">%s</script></div>'
            % (slug, pos, title, vid, name, cap, url, title, pos, title, vid, slug, title, name, ld))


JS = ('<script>(function(){var ok=document.getElementById("bmp3-ok");function say(m){if(ok)ok.textContent=m}'
      'document.querySelectorAll("[data-bmp3]").forEach(function(b){b.addEventListener("click",function(){'
      'var v=b.getAttribute("data-bmp3"),n=b.getAttribute("data-name"),t=b.getAttribute("data-title"),'
      'u=location.origin+"/layanan/#"+b.closest(".it").id;say("Menyiapkan video...");'
      'fetch(v).then(function(r){return r.blob()}).then(function(bl){var f=new File([bl],n,{type:"video/mp4"});'
      'if(navigator.canShare&&navigator.canShare({files:[f]})){say("");'
      'return navigator.share({files:[f],title:t,text:t+" "+u}).catch(function(){})}'
      'var o=URL.createObjectURL(bl),a=document.createElement("a");a.href=o;a.download=n;document.body.appendChild(a);'
      'a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(o)},4000);'
      'say("Video sudah di-download. Upload ke Reels atau Story dari galeri.")})'
      '.catch(function(){window.open(v,"_blank")})})})})();</script>')

BLOCK = ('<!--bmp3-->' + CSS + '<div class="bmp3" id="cara-kerja"><p class="eyebrow">Cara Kerja Kami</p>'
         '<h2>Angka yang Bisa Ditelusuri</h2>'
         '<p class="lead">Tiga video pendek tentang cara tim FA Indonesia bekerja. Setiap hasil kerja kami berangkat dari data '
         'dan perhitungan, dikerjakan dengan alat yang kami bangun sendiri, sehingga setiap angka bisa ditelusuri asalnya.</p>'
         '<div class="g">' + ''.join(item(*x) for x in ITEMS) + '</div>'
         '<p class="ok" id="bmp3-ok" aria-live="polite"></p></div>' + JS + '<!--/bmp3-->')
ANCHOR = '<!--/bmp10-->\n'


def main(dry=False):
    os.makedirs(os.path.join(OUT, 'media'), exist_ok=True)
    for slug, _, _ in ITEMS:
        for ext in ('mp4', 'jpg'):
            n = 'cara-kerja-fa-%s.%s' % (slug, ext); s = os.path.join(SRC, n)
            if not os.path.exists(s):
                sys.exit('aset tidak ada: ' + s)
            if os.path.getsize(s) > 24 * 1024 * 1024:
                sys.exit('aset di atas 24 MB (batas Cloudflare Pages 25 MB): ' + n)
            if not dry:
                shutil.copy2(s, os.path.join(OUT, 'media', n))
    h = open(P, encoding='utf-8').read()
    new = re.sub(r'<!--bmp3-->.*?<!--/bmp3-->\n?', '', h, flags=re.S)
    if ANCHOR not in new:
        sys.exit('penanda <!--/bmp10--> tidak ditemukan; jalankan fa_bumper_rekam_20261112.py dulu')
    new = new.replace(ANCHOR, ANCHOR + BLOCK + '\n', 1)
    changed = new != h
    if changed and not dry:
        open(P, 'w', encoding='utf-8').write(new)
    print('bmp3:', 'berubah' if changed else 'tidak berubah', '(dry run)' if dry else '')


if __name__ == '__main__':
    main('--dry' in sys.argv)
