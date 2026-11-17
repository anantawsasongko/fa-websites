# -*- coding: utf-8 -*-
"""Foto Ananta untuk poster artikel CA, US, Kompasiana, dan artikel daerah (17 Nov 2026, Bos: "pakenya foto
yang itu itu saja", "di CA dan US sama sekali gak ada foto saya").
Sumber: Drive "1. Foto Profesional/Raw (belum dipilih)" (IMG_3217, 3219, 3222, Foto 2, 7599) + foto jas navy lama + foto BG Hijau (16 Nov).
Latar sudah dipotong (PNG transparan) di shared/ananta/. Foto KPMG tidak dipakai (logo firma lain).
pick(key) memilih foto secara tetap per artikel (hash), sehingga foto menyebar merata dan tidak berganti tiap build."""
import os, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "ananta")
# nama file -> (tinggi relatif di poster, posisi geser horizontal relatif lebar foto)
POOL = {
    "ananta-navy.png": (1.00, 0.00),
    "ananta-noir.png": (0.92, 0.04),
    "ananta-kursi-hitam.png": (0.96, 0.10),
    "ananta-tigapotong.png": (1.00, 0.02),
    "ananta-abu.png": (0.92, 0.04),
    "ananta-kursi-putih.png": (0.96, 0.10),
    "ananta-hijau.png": (0.98, 0.02),
}
NAMES = list(POOL)


_ASSIGN = None


def _assign():
    """shared/ananta/assign.json: judul -> foto, dibagi bergiliran per kelompok (caus_poster_foto_20261117.py)
    supaya sebaran merata. Judul yang belum tercatat memakai hash."""
    global _ASSIGN
    if _ASSIGN is None:
        import json
        f = os.path.join(DIR, "assign.json")
        _ASSIGN = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    return _ASSIGN


def pick(key):
    n = _assign().get(key or "")
    if n in POOL: return n
    return NAMES[int(hashlib.md5(("foto" + (key or "")).encode()).hexdigest(), 16) % len(NAMES)]


def paste(im, key, right, bottom, height, c2, fade_left=.14, fade_bottom=.22, name=None):
    """Tempel foto (dipilih dari key) dengan tepi kanan di `right` dan dasar di `bottom`.
    Bawah dan kiri memudar ke gradasi, bayangan didinginkan dengan warna topik, ada cahaya tepi tipis."""
    name = name or pick(key)
    rel, shift = POOL[name]
    p = Image.open(os.path.join(DIR, name)).convert("RGBA")
    h = int(height * rel); w = int(p.width * h / p.height)
    p = p.resize((w, h), Image.LANCZOS)
    x = int(right - w + w * shift); y = int(bottom - h)
    a = np.asarray(p, "float32")
    rgb, al = a[..., :3], a[..., 3] / 255
    lum = rgb.mean(-1, keepdims=True) / 255
    rgb = rgb * (.90 + .06 * lum) + np.array(c2, "float32") * .06 * (1 - lum)
    yy, xx = np.mgrid[0:h, 0:w].astype("float32")
    fb = np.clip((h - yy) / (h * fade_bottom), 0, 1) if fade_bottom else 1
    fl = np.clip(xx / (w * fade_left), 0, 1) if fade_left else 1
    al = al * fb * fl
    halo = Image.new("L", im.size, 0)
    ImageDraw.Draw(halo).ellipse([x + w * .15, y + h * .0, x + w * .85, y + h * .70], fill=64)
    halo = halo.filter(ImageFilter.GaussianBlur(max(8, h / 7)))
    glow = Image.new("RGB", im.size, tuple(int(min(255, v * 1.5 + 60)) for v in c2))
    im.paste(glow, (0, 0), halo)
    out = Image.fromarray(np.dstack([rgb.clip(0, 255), al * 255]).astype("uint8"), "RGBA")
    im.paste(out, (x, y), out)
    return x


def grain(im, key, sigma=7.0):
    """Noise film merata (gaya noir)."""
    rng = np.random.default_rng(int(hashlib.md5(("grain" + (key or "")).encode()).hexdigest()[:8], 16))
    a = np.asarray(im.convert("RGB"), "float32")
    a += rng.normal(0, sigma, a.shape[:2])[..., None]
    return Image.fromarray(a.clip(0, 255).astype("uint8"), "RGB")
