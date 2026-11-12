#!/usr/bin/env python3
"""Video "Ten Years" (bumper 10 tahun) di bagian Rekam Jejak /layanan/ (12 Nov 2026 malam).
BEKERJA LANGSUNG DI out/faindonesia/layanan/index.html, idempoten (penanda <!--bmp10--> ... <!--/bmp10-->).
Jalankan SETELAH fa_layanan_ringkas_20261112.py dan SEBELUM fa_rendah_hati_20261112.py.

Pemicu (Bos): "Pasang di web aja lah dan captionnya ya dan bisa di share. Di bagian rekam jejak."
Caption berfokus pada menjaga kepercayaan klien, bukan pada ulang tahun. Atas nama Tim FA Indonesia,
tanpa nama pribadi, tanpa angka.

Aset: media/sepuluh-tahun-fa-indonesia.mp4 (1080x1920, 30 detik, di bawah batas 25 MB Cloudflare Pages)
dan media/sepuluh-tahun-fa-indonesia.jpg (poster). Disalin dari folder sumber ke out/ oleh script ini.
Panduan gaya video: project doc claude/gaya-bumper-fa.md.
"""
import os, re, shutil, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'FA-Indonesia_Website_SIAP-UPLOAD-v58', 'media')
OUT = os.path.join(ROOT, 'out', 'faindonesia')
P = os.path.join(OUT, 'layanan', 'index.html')
URL = 'https://faindonesia.co.id/layanan/#sepuluh-tahun'
VID = '/media/sepuluh-tahun-fa-indonesia.mp4'
POS = '/media/sepuluh-tahun-fa-indonesia.jpg'
TXT = 'Sepuluh tahun FA Indonesia: yang kami jaga adalah kepercayaan. Spirit & Hope.'

CSS = ('<style id="bmp10-css">'
       '.bmp10{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:40px;align-items:center;'
       'margin:0 0 56px;padding:0 0 48px;border-bottom:1px solid var(--line)}'
       '.bmp10 .v{position:relative;aspect-ratio:9/16;background:#06080c;border-radius:14px;overflow:hidden}'
       '.bmp10 video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}'
       '.bmp10 h2{margin:8px 0 16px;font-size:clamp(26px,3.2vw,38px);line-height:1.15}'
       '.bmp10 .c p{margin:0 0 12px;color:var(--muted);font-size:16px;line-height:1.65;max-width:56ch}'
       '.bmp10 .c p.sig{color:inherit;font-weight:600;margin-top:16px}'
       '.bmp10 .sh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:22px}'
       '.bmp10 .sh .fxs{margin:0}'
       '.bmp10 .vb{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;'
       'gap:7px;height:38px;padding:0 14px;border-radius:999px;border:1px solid rgba(127,127,127,.38);color:inherit;'
       'font:600 .84rem/1 inherit;font-family:inherit;opacity:.85;transition:background .2s,opacity .2s}'
       '.bmp10 .vb:hover,.bmp10 .vb:focus-visible{opacity:1;background:rgba(127,127,127,.14);border-color:rgba(127,127,127,.6)}'
       '.bmp10 .vb svg{width:16px;height:16px;flex:none}'
       '.bmp10 .ok{font-size:13px;color:var(--muted);margin:10px 0 0;min-height:18px}'
       '@media(max-width:760px){.bmp10{grid-template-columns:minmax(0,1fr);gap:24px;margin-bottom:40px;padding-bottom:36px}'
       '.bmp10 .v{max-width:300px;width:100%;margin:0 auto}}'
       '</style>')


LD = json.dumps({
    '@context': 'https://schema.org', '@type': 'VideoObject',
    'name': 'Sepuluh Tahun FA Indonesia: Menjaga Kepercayaan',
    'description': 'Perjalanan FA Indonesia 2016 sampai 2026 dalam 30 detik. Spirit & Hope.',
    'thumbnailUrl': 'https://faindonesia.co.id' + POS, 'contentUrl': 'https://faindonesia.co.id' + VID,
    'uploadDate': '2026-11-12', 'duration': 'PT30S', 'inLanguage': 'en',
    'publisher': {'@type': 'Organization', 'name': 'FA Indonesia', 'url': 'https://faindonesia.co.id/'}},
    ensure_ascii=False)

BLOCK = ('<!--bmp10-->' + CSS +
         '<div class="bmp10" id="sepuluh-tahun">'
         '<div class="v"><video controls playsinline preload="none" poster="' + POS + '" '
         'aria-label="Video Sepuluh Tahun FA Indonesia, 2016 sampai 2026">'
         '<source src="' + VID + '" type="video/mp4"/></video></div>'
         '<div class="c"><p class="eyebrow">2016 sampai 2026</p>'
         '<h2>Sepuluh Tahun Menjaga Kepercayaan</h2>'
         '<p>Sepuluh tahun bukan soal berapa lama kami ada. Yang kami jaga dari 2016 sampai hari ini cuma satu: '
         'kepercayaan orang yang menitipkan angkanya kepada kami.</p>'
         '<p>Dari katalog sebuah toko mebel, laporan tahunan, rumah sakit, kampus, sampai pendampingan pendanaan. '
         'Pekerjaannya berubah, cara kami memperlakukan kepercayaan itu tidak.</p>'
         '<p>Kepercayaan tidak dibangun dari satu proyek besar. Ia dijaga lewat hal kecil yang diulang terus: '
         'angka yang bisa dipertanggungjawabkan, janji yang ditepati, dan kabar yang jujur walau tidak enak didengar.</p>'
         '<p>Terima kasih untuk setiap klien dan rekan yang sudah berjalan bersama kami. Kami masih belajar.</p>'
         '<p class="sig">Spirit &amp; Hope. Tim FA Indonesia</p>'
         '<div class="sh">'
         '<div class="share" data-url="' + URL + '" data-tool="Sepuluh Tahun Menjaga Kepercayaan" '
         'data-kick="FA Indonesia" data-lab="Bagikan">'
         '<span data-story="' + POS + '" data-title="Sepuluh Tahun Menjaga Kepercayaan" hidden></span></div>'
         '<button type="button" class="vb" data-bmp="video" title="Bagikan file video" aria-label="Bagikan file video">'
         '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="13" height="12" rx="2"/>'
         '<path d="M16 10l5-3v10l-5-3z"/></svg><span>Video</span></button>'
         '</div><p class="ok" id="bmp10-ok" aria-live="polite"></p></div></div>'
         '<script type="application/ld+json">' + LD + '</script>'
         '<script>(function(){var u=' + json.dumps(URL) + ',t=' + json.dumps(TXT) + ',v=' + json.dumps(VID) + ','
         'ok=document.getElementById("bmp10-ok");function say(m){if(ok)ok.textContent=m}'
         'function dl(b){var o=URL.createObjectURL(b),a=document.createElement("a");a.href=o;'
         'a.download="sepuluh-tahun-fa-indonesia.mp4";document.body.appendChild(a);a.click();a.remove();'
         'setTimeout(function(){URL.revokeObjectURL(o)},4000);'
         'say("Video sudah di-download. Upload ke Reels atau Story dari galeri.")}'
         'document.querySelectorAll("[data-bmp]").forEach(function(b){b.addEventListener("click",function(){'
         'say("Menyiapkan video...");fetch(v).then(function(r){return r.blob()}).then(function(bl){'
         'var f=new File([bl],"sepuluh-tahun-fa-indonesia.mp4",{type:"video/mp4"});'
         'if(navigator.canShare&&navigator.canShare({files:[f]})){say("");'
         'return navigator.share({files:[f],title:t,text:t+" "+u}).catch(function(){})}dl(bl)})'
         '.catch(function(){window.open(v,"_blank")})})})})();</script>'
         '<!--/bmp10-->')

ANCHOR = '<section class="block alt" id="rekam">\n<div class="wrap">\n'


def main(dry=False):
    os.makedirs(os.path.join(OUT, 'media'), exist_ok=True)
    for n in ('sepuluh-tahun-fa-indonesia.mp4', 'sepuluh-tahun-fa-indonesia.jpg'):
        s = os.path.join(SRC, n)
        if not os.path.exists(s):
            sys.exit('aset tidak ada: ' + s)
        if os.path.getsize(s) > 24 * 1024 * 1024:
            sys.exit('aset di atas 24 MB (batas Cloudflare Pages 25 MB): ' + n)
        if not dry:
            shutil.copy2(s, os.path.join(OUT, 'media', n))
    h = open(P, encoding='utf-8').read()
    new = re.sub(r'<!--bmp10-->.*?<!--/bmp10-->\n?', '', h, flags=re.S)
    if ANCHOR not in new:
        sys.exit('anchor #rekam tidak ditemukan; jalankan fa_layanan_ringkas_20261112.py dulu')
    new = new.replace(ANCHOR, ANCHOR + BLOCK + '\n', 1)
    changed = new != h
    if changed and not dry:
        open(P, 'w', encoding='utf-8').write(new)
    print('bmp10:', 'berubah' if changed else 'tidak berubah', '(dry run)' if dry else '')


if __name__ == '__main__':
    main('--dry' in sys.argv)
