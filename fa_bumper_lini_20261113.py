#!/usr/bin/env python3
"""Tiga video lini FA Consult, FA Digital, FA Edu di /layanan/, di bawah Klien dan Bank sebagai "Layanan Lain" (13 Nov 2026).
BEKERJA LANGSUNG DI out/faindonesia/layanan/index.html, idempoten (penanda <!--bmpl--> ... <!--/bmpl-->; dry run: --dry).
Blok disisipkan di dalam section#klien, tepat sebelum tombol Chat Ananta, CPA (div.lay12-cta) section itu.
Jalankan SETELAH fa_layanan_ringkas_20261112.py dan SEBELUM fa_rendah_hati_20261112.py.

Pemicu (Bos): "Apakah aman kalau 3 video ini juga dipasang di bawah logo klien dan bank sebagai Layanan lain" lalu "Ya deploy".
Video: gaya FA Saturn, aksen warna asli lini (Consult biru, Digital orange, Edu merah); tahap kerja meniru metodologi firma
global tanpa menyebut merek. Aset web: media/cara-kerja-fa-{consult,digital,edu}.mp4 (1080x1920, 30 detik, CRF 27, < 7 MB) + .jpg.
Master resolusi penuh untuk Reels tidak di repo.
"""
import os, re, shutil, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'FA-Indonesia_Website_SIAP-UPLOAD-v58', 'media')
OUT = os.path.join(ROOT, 'out', 'faindonesia')
P = os.path.join(OUT, 'layanan', 'index.html')
BASE = 'https://faindonesia.co.id'
ITEMS = [
    ('consult', 'FA Consult', 'Pendampingan M&amp;A dan valuasi, dari ruang lingkup tertulis, due diligence, sampai closing.'),
    ('digital', 'FA Digital', 'SIMRS dan sistem rumah sakit, dari pemetaan alur kerja dan desain sampai go-live dan serah terima.'),
    ('edu', 'FA Edu', 'Pelatihan akuntansi dan audit berbasis kasus, dari pemetaan kebutuhan sampai toolkit yang siap dipakai.'),
]

CSS = ('<style id="bmpl-css">'
       '.bmpl{margin:48px 0 8px;padding:44px 0 0;border-top:1px solid var(--line)}'
       '.bmpl h2{margin:8px 0 12px;font-size:clamp(26px,3.2vw,38px);line-height:1.15}'
       '.bmpl>p.lead{margin:0 0 28px;color:var(--muted);font-size:16px;line-height:1.65;max-width:62ch}'
       '.bmpl .g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}'
       '.bmpl .v{position:relative;aspect-ratio:9/16;background:#06080c;border-radius:14px;overflow:hidden}'
       '.bmpl video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}'
       '.bmpl h3{margin:16px 0 6px;font-size:20px;line-height:1.25}'
       '.bmpl .it p{margin:0;color:var(--muted);font-size:15px;line-height:1.6}'
       '.bmpl .sh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:14px}'
       '.bmpl .sh .fxs{margin:0}.bmpl .sh .fxs>span{display:none}'
       '.bmpl .vb{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;'
       'gap:7px;height:38px;padding:0 14px;border-radius:999px;border:1px solid rgba(127,127,127,.38);color:inherit;'
       'font:600 .84rem/1 inherit;font-family:inherit;opacity:.85;transition:background .2s,opacity .2s}'
       '.bmpl .vb:hover,.bmpl .vb:focus-visible{opacity:1;background:rgba(127,127,127,.14);border-color:rgba(127,127,127,.6)}'
       '.bmpl .vb svg{width:16px;height:16px;flex:none}'
       '.bmpl .ok{font-size:13px;color:var(--muted);margin:10px 0 0;min-height:18px}'
       '@media(max-width:860px){.bmpl .g{grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:min(72vw,300px);'
       'overflow-x:auto;scroll-snap-type:x mandatory;gap:18px;padding-bottom:8px;-webkit-overflow-scrolling:touch}'
       '.bmpl .it{scroll-snap-align:start}}'
       '</style>')


def item(slug, name, cap):
    vid = '/media/cara-kerja-fa-%s.mp4' % slug; pos = '/media/cara-kerja-fa-%s.jpg' % slug
    url = BASE + '/layanan/#layanan-lain-' + slug; title = 'Cara Kerja ' + name
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'VideoObject', 'name': title,
                     'description': cap.replace('&amp;', '&'), 'thumbnailUrl': BASE + pos, 'contentUrl': BASE + vid,
                     'uploadDate': '2026-11-13', 'duration': 'PT30S', 'inLanguage': 'en',
                     'publisher': {'@type': 'Organization', 'name': 'FA Indonesia', 'url': BASE + '/'}}, ensure_ascii=False)
    return ('<div class="it" id="layanan-lain-%s"><div class="v"><video controls playsinline preload="none" poster="%s" '
            'aria-label="Video %s"><source src="%s" type="video/mp4"/></video></div>'
            '<h3>%s</h3><p>%s</p>'
            '<div class="sh"><div class="share" data-url="%s" data-tool="%s" data-kick="FA Indonesia" data-lab="Bagikan">'
            '<span data-story="%s" data-title="%s" hidden></span></div>'
            '<button type="button" class="vb" data-bmpl="%s" data-name="cara-kerja-fa-%s.mp4" data-title="%s" '
            'title="Bagikan file video" aria-label="Bagikan file video %s">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="13" height="12" rx="2"/>'
            '<path d="M16 10l5-3v10l-5-3z"/></svg><span>Video</span></button></div>'
            '<script type="application/ld+json">%s</script></div>'
            % (slug, pos, title, vid, name, cap, url, title, pos, title, vid, slug, title, name, ld))


JS = ('<script>(function(){var ok=document.getElementById("bmpl-ok");function say(m){if(ok)ok.textContent=m}'
      'document.querySelectorAll("[data-bmpl]").forEach(function(b){b.addEventListener("click",function(){'
      'var v=b.getAttribute("data-bmpl"),n=b.getAttribute("data-name"),t=b.getAttribute("data-title"),'
      'u=location.origin+"/layanan/#"+b.closest(".it").id;say("Menyiapkan video...");'
      'fetch(v).then(function(r){return r.blob()}).then(function(bl){var f=new File([bl],n,{type:"video/mp4"});'
      'if(navigator.canShare&&navigator.canShare({files:[f]})){say("");'
      'return navigator.share({files:[f],title:t,text:t+" "+u}).catch(function(){})}'
      'var o=URL.createObjectURL(bl),a=document.createElement("a");a.href=o;a.download=n;document.body.appendChild(a);'
      'a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(o)},4000);'
      'say("Video sudah di-download. Upload ke Reels atau Story dari galeri.")})'
      '.catch(function(){window.open(v,"_blank")})})})})();</script>')

BLOCK = ('<!--bmpl-->' + CSS + '<div class="bmpl" id="layanan-lain"><p class="eyebrow">Layanan Lain</p>'
         '<h2>Konsultasi, Sistem, dan Pelatihan</h2>'
         '<p class="lead">Selain laporan keuangan dan pendanaan, tim FA Indonesia juga mengerjakan tiga lini ini. '
         'Semuanya berjalan bertahap dengan cara kerja yang tertulis, dari kesepakatan ruang lingkup sampai hasil akhir diserahkan.</p>'
         '<div class="g">' + ''.join(item(*x) for x in ITEMS) + '</div>'
         '<p class="ok" id="bmpl-ok" aria-live="polite"></p></div>' + JS + '<!--/bmpl-->\n')


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
    new = re.sub(r'<!--bmpl-->.*?<!--/bmpl-->\n?', '', h, flags=re.S)
    i = new.find('<section class="block" id="klien">')
    if i < 0:
        sys.exit('section#klien tidak ditemukan; jalankan fa_layanan_ringkas_20261112.py dulu')
    j = new.find('<div class="lay12-cta"', i)
    k = new.find('</section>', i)
    if j < 0 or j > k:
        sys.exit('tombol lay12-cta di section#klien tidak ditemukan')
    new = new[:j] + BLOCK + new[j:]
    changed = new != h
    if changed and not dry:
        open(P, 'w', encoding='utf-8').write(new)
    print('bmpl:', 'berubah' if changed else 'tidak berubah', '(dry run)' if dry else '')


if __name__ == '__main__':
    main('--dry' in sys.argv)
