"""Kontak satu pintu (2 Nov 2026, permintaan Bos): section "Mari Berdiskusi" (#kontak) dihapus dari FA,
semua email alias tampil sebagai satu alamat ananta@faindonesia.co.id, Gmail pribadi tidak tampil,
nomor telepon tidak tampil sebagai teks (cukup tombol WhatsApp). Email tetap ada di footer FA."""
import os, re
MAIL = "ananta@faindonesia.co.id"
SEC = re.compile(r'<section class="block( alt)?" id="kontak">.*?</section>\s*', re.S)
def clean(t, site):
    o = t
    t = SEC.sub("", t)
    t = t.replace('href="#kontak"', 'href="https://wa.me/6282245260121" target="_blank" rel="noopener"').replace('href="/#kontak"', 'href="https://wa.me/6282245260121" target="_blank" rel="noopener"')
    t = t.replace("?cc=ananta.w.sasongko@gmail.com&amp;", "?").replace("?cc=ananta.w.sasongko@gmail.com&", "?").replace("?cc=ananta.w.sasongko@gmail.com", "")
    t = re.sub(r'<li><a href="mailto:(ananta\.w\.sasongko|farhanikn)@gmail\.com">[^<]*</a></li>', "", t)
    t = re.sub(r'<div class="cline">(?:(?!</div>).)*?c-gmail.*?</div>', "", t, flags=re.S)
    t = t.replace("ananta.w.sasongko@gmail.com", MAIL).replace("office@faindonesia.co.id", MAIL).replace("info@faindonesia.co.id", MAIL)
    t = re.sub(r'<a href="https://wa\.me/(\d+)">0\d{2,3}[ -]?\d{3,4}[ -]?\d{3,4}</a>', r'<a href="https://wa.me/\1" target="_blank" rel="noopener">Chat WhatsApp</a>', t)
    t = re.sub(r'\s*\(0\d{2,3}[ -]?\d{3,4}[ -]?\d{3,4}\)', "", t)
    if site == "faindonesia" and 'class="flegal"' in t and "fa-mail-ft" not in t:
        t = re.sub(r'(<span class="flegal"[^>]*>)', r'\1<a class="fa-mail-ft" href="mailto:' + MAIL + '" style="color:inherit">' + MAIL + '</a> · ', t, count=1)
    return t if t != o else None
def run(OUT):
    n = 0
    for site in ("faindonesia", "cariakuntan", "updatesak", "kja-farhani"):
        root = os.path.join(OUT, site)
        if not os.path.isdir(root): continue
        for d, _, fs in os.walk(root):
            for f in fs:
                if not f.endswith(".html"): continue
                p = os.path.join(d, f); t = open(p, encoding="utf-8").read()
                r = clean(t, site)
                if r: open(p, "w", encoding="utf-8").write(r); n += 1
    return n
