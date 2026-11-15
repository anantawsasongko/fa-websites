# -*- coding: utf-8 -*-
"""Poster artikel daerah (15 Nov 2026, Bos: "poster gaya FA, foto gradasi, pakai yang jas berdasi").
Dua ukuran: feed 1080x1350 (LinkedIn/IG) dan og 1200x630 (og:image halaman).
Gaya: noir FA (latar gelap bergradasi warna topik, foto stok di-blur + grain), foto Bos jas navy dasi kuning
memudar ke gradasi, judul Newsreader, teks Poppins Light. Logo asli (FA wordmark, lockup CA/US), bukan tulisan.
Tanpa emoji, tanpa em dash, tanpa nomor HP."""
import os, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
AS = os.path.join(HERE, 'assets')
BG = os.path.join(REPO, 'shared', 'share-bg')
UF = os.path.join(REPO, 'updatesak', 'fonts')

BRAND = {
    'fa': dict(dom='faindonesia.co.id', logo=os.path.join(REPO, 'out', 'faindonesia', 'img', 'brand', 'wm-light.png'), lh=44,
               tag='Spirit & Hope. Since 2016'),
    'ca': dict(dom='cariakuntan.com', logo=os.path.join(REPO, 'shared', 'logo', 'ca-lockup-dark.png'), lh=70,
               tag='KAP, KJA, KJPP, dan Konsultan Pajak'),
    'us': dict(dom='updatesak.com', logo=os.path.join(REPO, 'shared', 'logo', 'us-lockup-dark.png'), lh=70,
               tag='Standar, Kertas Kerja, Kalkulator'),
    'ks': dict(dom='Kompasiana', logo=None, lh=0, tag='Catatan Praktik Keuangan'),
}
# warna per brand x topik: (warna gradasi, warna aksen)
PAL = {
    ('fa', 'abc'): ((13, 92, 99), (126, 224, 214)),      # teal
    ('fa', 'pe'): ((52, 36, 110), (190, 178, 255)),      # indigo
    ('fa', 'cfo'): ((126, 54, 22), (255, 196, 140)),     # terracotta
    ('ca', 'abc'): ((20, 70, 190), (150, 190, 255)),     # biru CA
    ('ca', 'pe'): ((20, 52, 130), (140, 210, 255)),
    ('ca', 'cfo'): ((36, 60, 160), (255, 214, 130)),
    ('us', 'abc'): ((10, 104, 86), (126, 224, 195)),     # hijau US
    ('us', 'pe'): ((8, 84, 96), (150, 230, 220)),
    ('us', 'cfo'): ((30, 98, 60), (214, 236, 150)),
    ('ks', 'abc'): ((96, 30, 46), (255, 176, 176)),      # marun
    ('ks', 'pe'): ((70, 34, 96), (226, 180, 250)),       # plum
    ('ks', 'cfo'): ((104, 76, 14), (252, 216, 110)),     # amber
}
TOPIK_OG = {'abc': 'Unit Cost · Activity Based Costing', 'pe': 'Pendanaan RS · PE & VC', 'cfo': 'Fractional CFO'}
TOPIK = {'abc': 'Unit Cost · Activity Based Costing', 'pe': 'Pendanaan RS · Private Equity & Venture Capital', 'cfo': 'Fractional CFO'}


def _serif(size, wght=420, italic=False):
    f = ImageFont.truetype(os.path.join(AS, 'Newsreader-italic.ttf' if italic else 'Newsreader-normal.ttf'), size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f


def _sans(size, w='Light'):
    return ImageFont.truetype(os.path.join(UF, f'Poppins-{w}.ttf'), size)


def _wrap(dr, text, font, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if dr.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def _balance(dr, text, font, maxw):
    """Bungkus lalu seimbangkan panjang baris (tanpa baris yatim satu kata)."""
    lines = _wrap(dr, text, font, maxw)
    n = len(lines)
    if n <= 1: return lines
    lo, hi = max(dr.textlength(w, font=font) for w in text.split()), maxw
    best = lines
    for _ in range(18):
        mid = (lo + hi) / 2
        t = _wrap(dr, text, font, mid)
        if len(t) <= n: best, hi = t, mid
        else: lo = mid
    return best


def _bg(W, H, key, c2, photo_box):
    rng = np.random.default_rng(int(hashlib.md5(key.encode()).hexdigest()[:8], 16))
    yy, xx = np.mgrid[0:H, 0:W].astype('float32')
    # gradasi: warna topik dari kiri bawah, noir di kanan atas
    d = np.sqrt((xx / W) ** 2 + ((H - yy) / H) ** 2) / 1.3
    d = np.clip(d / .78, 0, 1)[..., None]
    c0 = np.array([6, 8, 14], 'float32'); cc = np.array(c2, 'float32')
    base = cc * .92 + (c0 - cc * .92) * d
    im = Image.fromarray(base.clip(0, 255).astype('uint8'), 'RGB')
    # foto stok di-blur, diberi warna, memudar
    fs = sorted(f for f in os.listdir(BG) if f.endswith('.jpg'))
    ph = Image.open(os.path.join(BG, fs[int(hashlib.md5(('bg' + key).encode()).hexdigest(), 16) % len(fs)])).convert('RGB')
    px, py, pw, phh = photo_box
    sc = max(pw / ph.width, phh / ph.height)
    ph = ph.resize((int(ph.width * sc) + 1, int(ph.height * sc) + 1), Image.LANCZOS)
    x0 = (ph.width - pw) // 2; y0 = (ph.height - phh) // 2
    ph = ph.crop((x0, y0, x0 + pw, y0 + phh)).filter(ImageFilter.GaussianBlur(max(W, H) / 60))
    g = np.asarray(ph.convert('L'), 'float32')[..., None] / 255
    tint = (g * 1.25).clip(0, 1) * (cc * .55 + 70) + (1 - g) * c0
    ph = Image.fromarray(tint.clip(0, 255).astype('uint8'), 'RGB')
    my, mx = np.mgrid[0:phh, 0:pw].astype('float32')
    m = np.clip(mx / pw / .55, 0, 1) * np.clip((phh - my) / phh / .35, 0, 1) * .62
    im.paste(ph, (px, py), Image.fromarray((m * 255).astype('uint8'), 'L'))
    a = np.asarray(im, 'float32')
    a += rng.normal(0, 5.5, a.shape[:2])[..., None]          # grain
    # vignette halus
    v = 1 - .22 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)[..., None] / 2
    return Image.fromarray((a * v).clip(0, 255).astype('uint8'), 'RGB')


def _person(im, box, c2, fade_left=.0, fade_bottom=.22):
    """Tempel foto potong (RGBA) di box=(x, y, tinggi). Bawah dan kiri memudar ke gradasi."""
    x, y, h = box
    p = Image.open(os.path.join(AS, 'ananta-jas.png')).convert('RGBA')
    w = int(p.width * h / p.height)
    p = p.resize((w, h), Image.LANCZOS)
    a = np.asarray(p, 'float32')
    rgb, al = a[..., :3], a[..., 3] / 255
    # sedikit turunkan eksposur dan dinginkan bayangan agar menyatu dengan noir
    lum = rgb.mean(-1, keepdims=True) / 255
    rgb = rgb * (.90 + .06 * lum) + np.array(c2, 'float32') * .05 * (1 - lum)
    yy, xx = np.mgrid[0:h, 0:w].astype('float32')
    fb = np.clip((h - yy) / (h * fade_bottom), 0, 1) if fade_bottom else 1
    fl = np.clip(xx / (w * fade_left), 0, 1) if fade_left else 1
    al = al * fb * fl
    # cahaya tepi tipis di belakang kepala
    halo = Image.new('L', im.size, 0)
    ImageDraw.Draw(halo).ellipse([x + w * .12, y + h * .02, x + w * .88, y + h * .78], fill=70)
    halo = halo.filter(ImageFilter.GaussianBlur(h / 7))
    glow = Image.new('RGB', im.size, tuple(int(min(255, v * 1.5 + 60)) for v in c2))
    im.paste(glow, (0, 0), halo)
    out = Image.fromarray(np.dstack([rgb.clip(0, 255), al * 255]).astype('uint8'), 'RGBA')
    im.paste(out, (x, y), out)


def _logo(im, dr, brand, x, y, s=1.0):
    b = BRAND[brand]
    if b['logo'] and os.path.exists(b['logo']):
        lg = Image.open(b['logo']).convert('RGBA'); hh = int(b['lh'] * s)
        lg = lg.resize((int(lg.width * hh / lg.height), hh), Image.LANCZOS)
        im.paste(lg, (x, y), lg); return hh
    f = _serif(int(40 * s), 480, italic=True)
    dr.text((x, y), 'Catatan Ananta W. Sasongko', font=f, fill='white')
    return int(46 * s)


def feed(brand, topik, kota, title, out, byline='Ananta W. Sasongko, CPA'):
    W, H = 1080, 1350; m = 84
    c2, ac = PAL[(brand, topik)]
    im = _bg(W, H, brand + topik + kota + title, c2, (W - 760, 0, 760, 820))
    ph = 770
    pw = int(700 * ph / 875)
    _person(im, (W - pw + 36, H - ph - 120, ph), c2, fade_left=.10, fade_bottom=.30)
    # gradasi gelap di bawah untuk pita info
    ov = np.zeros((H, W), 'float32'); yy = np.arange(H)[:, None]
    ov[:] = np.clip((yy - (H - 420)) / 300, 0, 1) * .93
    im.paste(Image.new('RGB', (W, H), (6, 8, 14)), (0, 0), Image.fromarray((ov * 255).astype('uint8'), 'L'))
    dr = ImageDraw.Draw(im)
    lh = _logo(im, dr, brand, m, m - 6)
    # garis tipis + kicker
    y = m + lh + 54
    dr.text((m, y), TOPIK[topik].upper(), font=_sans(23, 'Medium'), fill=ac)
    y += 50
    size = 78
    while True:
        f = _serif(size, 400); lines = _balance(dr, title, f, W - 2 * m - 20)
        if len(lines) * int(size * 1.12) <= 262 or size <= 48: break
        size -= 2
    for ln in lines:
        dr.text((m, y), ln, font=f, fill='white'); y += int(size * 1.12)
    dr.rectangle([m, y + 22, m + 96, y + 26], fill=ac)
    # kota (italic serif) di kiri bawah
    dr.text((m, H - 316), kota, font=_serif(60, 380, italic=True), fill='white')
    dr.text((m, H - 240), 'Artikel untuk pemilik usaha dan direksi di daerah', font=_sans(23), fill=(214, 220, 228))
    # pita bawah
    dr.line([(m, H - 150), (W - m, H - 150)], fill=(255, 255, 255, 90), width=1)
    dr.text((m, H - 112), ('Baca di ' if brand == 'ks' else 'Baca: ') + BRAND[brand]['dom'], font=_sans(27, 'Medium'), fill='white')
    dr.text((m, H - 72), BRAND[brand]['tag'], font=_sans(21), fill=(190, 198, 208))
    if byline:
        dr.text((W - m, H - 112), byline, font=_sans(23, 'Medium'), fill='white', anchor='ra')
        dr.text((W - m, H - 72), 'Penulis', font=_sans(21), fill=(190, 198, 208), anchor='ra')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, 'JPEG', quality=88, optimize=True, progressive=True)


def og(brand, topik, kota, title, out):
    W, H = 1200, 630; m = 64
    c2, ac = PAL[(brand, topik)]
    im = _bg(W, H, brand + topik + kota + title, c2, (W - 700, 0, 700, H))
    ph = 640; pw = int(700 * ph / 875)
    _person(im, (W - pw - 6, H - ph + 30, ph), c2, fade_left=.12, fade_bottom=.16)
    dr = ImageDraw.Draw(im)
    lh = _logo(im, dr, brand, m, m - 8, .8)
    y = m + lh + 44
    dr.text((m, y), (TOPIK_OG[topik] + ' · ' + kota).upper(), font=_sans(18, 'Medium'), fill=ac)
    y += 40
    size = 54; maxw = 640
    while True:
        f = _serif(size, 400); lines = _balance(dr, title, f, maxw)
        if len(lines) <= 5 or size <= 34: break
        size -= 2
    for ln in lines:
        dr.text((m, y), ln, font=f, fill='white'); y += int(size * 1.13)
    dr.rectangle([m, y + 16, m + 72, y + 19], fill=ac)
    dr.text((m, H - m + 4), BRAND[brand]['dom'], font=_sans(21, 'Medium'), fill='white', anchor='ls')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, 'JPEG', quality=84, optimize=True, progressive=True)


if __name__ == '__main__':
    import sys
    o = sys.argv[1] if len(sys.argv) > 1 else '/tmp/poster-test'
    T = 'Unit Cost Rumah Sakit di Surabaya: Activity Based Costing dari Pool Biaya sampai Tarif'
    for b in ('fa', 'ca', 'us', 'ks'):
        feed(b, 'abc', 'Surabaya', T, f'{o}/{b}-feed.jpg'); og(b, 'abc', 'Surabaya', T, f'{o}/{b}-og.jpg')
    feed('fa', 'pe', 'Denpasar', 'Private Equity Global Melirik Rumah Sakit di Bali: Cara Membaca Term Sheet', f'{o}/fa-pe.jpg')
    feed('fa', 'cfo', 'Bekasi', 'Fractional CFO untuk Pabrik di Bekasi', f'{o}/fa-cfo.jpg')
