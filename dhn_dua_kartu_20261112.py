#!/usr/bin/env python3
"""Dua kartu kantor berdampingan: KAP DHN & Rekan (oranye) + KJA Farhani K.N. (biru) (12 Nov 2026).
BEKERJA LANGSUNG DI out/faindonesia, out/cariakuntan, out/updatesak. Idempoten. Jalankan PALING AKHIR
(setelah fa_rapi_kolom_20261112.py).

Permintaan Bos: di semua halaman yang punya kartu KAP DHN dan di semua halaman layanan daerah FA harus ada
dua kartu, KAP dan KJA. Kartu KJA Farhani K.N. memakai logo birunya, ukuran sama dengan kartu KAP, dan
kedua tombol tetap ke WhatsApp Bos.

1. Setiap <aside class="dhnc"> (kartu KAP) dibungkus <div class="dhn2"> bersama kartu KJA (aside.dhnc.kja).
   Strip "dhns kja" yang menempel di kartu dibuang karena sudah digantikan kartu.
2. Halaman layanan daerah FA (berblok fanas-x) yang belum punya kartu: dua kartu disisipkan sebelum footer.
3. CSS <style id="dhn2-css">: grid dua kolom sama lebar dan sama tinggi, satu kolom di HP.
"""
import os, re, sys
from urllib.parse import quote

M = os.path.dirname(os.path.abspath(__file__))
DRY = '--dry' in sys.argv
WA = '6282245260121'

CSS = ('<style id="dhn2-css">'
       '.dhn2{box-sizing:border-box;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;align-items:stretch;'
       'width:min(1008px,calc(100% - 32px));margin:34px auto}'
       '.dhn2>.dhnc{width:auto!important;margin:0!important;height:100%}'
       '.dhn2>.dhnc>div{display:flex;flex-direction:column;flex:1;min-width:0;height:100%}'
       '.dhn2>.dhnc p{flex:1}'
       '.dhn2>.dhnc img{width:46px;height:54px;flex:0 0 46px;object-fit:contain}'
       '.dhnc.kja{border-color:rgba(37,99,235,.6);background:rgba(37,99,235,.07)}'
       '.dhnc.kja small{color:#3B82F6}'
       '.dhnc.kja .dhnb{background:#2563EB}'
       '.dhn2 .dhnb{min-width:150px;text-align:center;box-sizing:border-box}'
       'main:has(.fnx)~.dhn2{width:min(820px,calc(100% - 2*clamp(16px,4vw,40px)));'
       'margin-left:max(clamp(16px,4vw,40px),calc((100% - 1000px)/2 + clamp(16px,4vw,40px)));margin-right:auto}'
       '@media(max-width:760px){.dhn2{grid-template-columns:1fr;grid-auto-rows:1fr;gap:12px}}'
       '@media print{.dhn2{display:none}}'
       '</style>')

# CSS dasar kartu (salinan shared/dhn/dhn.py) untuk halaman yang belum pernah memuatnya
import importlib.util
_sp = importlib.util.spec_from_file_location('dhn', os.path.join(M, 'shared', 'dhn', 'dhn.py'))
_dhn = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_dhn)

KJA = {
    'id': dict(lab='Kantor Jasa Akuntansi',
               desc='Izin Menteri Keuangan No. 232/KM.1PPPK/2020. Pembukuan dan penyusunan laporan keuangan sesuai SAK EMKM, '
                    'SAK EP, atau PSAK, serta pajak, siap dipakai bank dan auditor, untuk perusahaan di seluruh Indonesia.',
               msg='Halo Pak Ananta, saya ingin tanya jasa pembukuan, laporan keuangan, dan pajak di KJA Farhani K.N.'),
    'en': dict(lab='Accounting Services Firm',
               desc='Licensed by the Minister of Finance (No. 232/KM.1PPPK/2020). Bookkeeping and financial statements under '
                    'SAK EMKM, SAK EP, or PSAK, plus tax, ready for banks and auditors, across Indonesia.',
               msg='Hello Pak Ananta, I would like to ask about bookkeeping, financial statements, and tax with KJA Farhani K.N.'),
}
ASIDE = re.compile(r'<aside\b(?=[^>]*class="dhnc")[^>]*>.*?</aside>', re.S)
STRIP = re.compile(r'\s*<div class="dhns kja">.*?</div>', re.S)


def kja_card(L, label):
    t = KJA[L]
    wa = 'https://wa.me/%s?text=%s' % (WA, quote(t['msg']))
    return ('<aside aria-label="KJA Farhani K.N." class="dhnc kja"><img alt="Logo KJA Farhani K.N." height="54" loading="lazy" '
            'src="/img/kja-farhani-mark.png" width="46"/><div><small>%s</small><b class="n">KJA Farhani K.N.</b><p>%s</p>'
            '<div class="bt"><a class="dhnb" href="%s" rel="noopener" target="_blank">%s</a></div></div></aside>'
            % (t['lab'], t['desc'], wa, label))


def process(t, rel, site):
    o = t
    L = 'en' if re.match(r'(en|zh|hokkien|ja|ko)(/|$)', rel) else 'id'
    if 'class="dhn2"' not in t:
        m = ASIDE.search(t)
        if m:
            lab = re.search(r'<a class="dhnb"[^>]*>([^<]+)</a>', m.group(0))
            label = lab.group(1) if lab else 'Chat Ananta, CPA'
            end = m.end()
            s = STRIP.match(t, end)
            if s:
                end = s.end()
            t = t[:m.start()] + '<div class="dhn2">' + m.group(0) + kja_card(L, label) + '</div>' + t[end:]
        elif site == 'faindonesia' and '<section class="fnx">' in t and 'noindex' not in t[:4000]:
            k = _dhn._outside(t, r'<footer[\s>]')
            if k > 0:
                kap = _dhn.card(L, '/img/kap-dhn-mark.png', '/kap-dhn/')
                kap = re.sub(r'(<a class="dhnb"[^>]*>)[^<]+', r'\1Chat Ananta, CPA', kap)
                a = ASIDE.search(kap)
                blk = ('<!--dhn--><div class="dhn2">' + a.group(0) + kja_card(L, 'Chat Ananta, CPA') + '</div><!--/dhn-->')
                t = t[:k] + blk + t[k:]
    if 'class="dhn2"' in t:
        if 'dhn-css' not in t:
            t = t.replace('</head>', _dhn.CSS + '</head>', 1)
        if '<style id="dhn2-css">' in t:
            t = re.sub(r'<style id="dhn2-css">.*?</style>', lambda m: CSS, t, count=1, flags=re.S)
        else:
            t = t.replace('</head>', CSS + '</head>', 1)
    return t, t != o


def main():
    for site in ('faindonesia', 'cariakuntan', 'updatesak'):
        root = os.path.join(M, 'out', site); n = 0
        for d, _, fs in os.walk(root):
            for f in fs:
                if not f.endswith('.html'):
                    continue
                p = os.path.join(d, f)
                t = open(p, encoding='utf-8').read()
                if 'dhnc' not in t and 'class="fnx"' not in t:
                    continue
                t2, ch = process(t, os.path.relpath(p, root).replace(os.sep, '/'), site)
                if ch:
                    n += 1
                    if not DRY:
                        open(p, 'w', encoding='utf-8').write(t2)
        print('dua kartu', site, n, '(dry)' if DRY else '')


if __name__ == '__main__':
    main()
