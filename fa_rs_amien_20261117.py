#!/usr/bin/env python3
"""17 Nov 2026: dr. Amien Mujib Bahruddin, M.Kes masuk Tim Konsultan Rumah Sakit FA.

Bekerja di out/faindonesia (idempoten, aman diulang; jalankan lagi setiap kali
fa_rs_tim_20261105.py atau fa_rs_daerah_20261105.py dijalankan ulang).
1. Kartu ketiga di blok fa-rstim (Ananta, dr. Sigit, dr. Amien), grid 3 kolom.
2. Halaman profil /dr-amien-mujib-bahruddin/ (template dari /dr-sigit-riyarto/).
3. Kalimat pembagian peran di profil dr. Sigit dan bagian "Pengalaman Memimpin
   Rumah Sakit", link profil di baris Layanan RS lain, sitemap, llms.txt.
Pakai --dry untuk hitung saja.
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
DRY = '--dry' in sys.argv
SLUG = 'dr-amien-mujib-bahruddin'
URL = f'https://faindonesia.co.id/{SLUG}/'
NAMA = 'dr. Amien Mujib Bahruddin, M.Kes'
FOTO = '/img/dr-amien-mujib-bahruddin-mkes.jpg'

SIGIT_CARD_END = ('<div class="t"><b>dr. Sigit Riyarto</b><small>M.Kes, AAK · Medis, Marketing, '
                  'Operasional</small></div></a>')
AMIEN_CARD = (f'<a href="/{SLUG}/"><img alt="{NAMA}" decoding="async" height="875" loading="lazy" '
              f'src="{FOTO}" width="700"/><div class="t"><b>dr. Amien Mujib Bahruddin</b>'
              '<small>M.Kes · Akreditasi, Strategi, Digitalisasi</small></div></a>')
CSS_OLD = ('.rstb{margin:22px 0 26px;max-width:560px}', '.rst{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}')
CSS_NEW = ('.rstb{margin:22px 0 26px;max-width:780px}', '.rst{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}')
PENGALAMAN_OLD = 'Di FA Indonesia beliau memegang sisi medis, marketing, dan operasional.</p>'
PENGALAMAN_NEW = ('Di FA Indonesia beliau memegang sisi medis, marketing, dan operasional. Akreditasi, strategi, '
                  f'dan digitalisasi rumah sakit dipegang <a href="/{SLUG}/">{NAMA}</a>.</p>')
PROFIL_OLD = '<a href="/dr-sigit-riyarto/">Profil dr. Sigit Riyarto</a>'
PROFIL_NEW = PROFIL_OLD + f' · <a href="/{SLUG}/">Profil dr. Amien Mujib Bahruddin</a>'


def patch(s):
    n = s
    if 'class="rst"' in n and f'href="/{SLUG}/"><img' not in n and SIGIT_CARD_END in n:
        n = n.replace(SIGIT_CARD_END, SIGIT_CARD_END + AMIEN_CARD, 1)
    if f'href="/{SLUG}/"><img' in n:
        for o, w in zip(CSS_OLD, CSS_NEW):
            n = n.replace(o, w)
    if PENGALAMAN_OLD in n:
        n = n.replace(PENGALAMAN_OLD, PENGALAMAN_NEW)
    if PROFIL_OLD in n and f'Profil dr. Amien' not in n:
        n = n.replace(PROFIL_OLD, PROFIL_NEW)
    return n


WA = ('https://wa.me/6282245260121?text=Halo%20Pak%20Ananta%2C%20saya%20ingin%20konsultasi%20rumah%20sakit'
      '%20dengan%20dr.%20Amien.')
TITLE = 'dr. Amien Mujib Bahruddin: Akreditasi dan SIMRS | FA Indonesia'
DESC = ('Profil dr. Amien Mujib Bahruddin, M.Kes, tim konsultan rumah sakit FA Indonesia untuk akreditasi, '
        'strategi, dan digitalisasi rumah sakit.')
FAQ = [
    ('Apa bidang dr. Amien Mujib Bahruddin di FA Indonesia?',
     'Akreditasi, strategi, dan digitalisasi rumah sakit, bersama tim konsultan rumah sakit FA Indonesia.'),
    ('Bagaimana menghubungi dr. Amien?',
     'Lewat tombol WhatsApp Tim Rumah Sakit FA Indonesia di halaman ini.'),
]


def main_html():
    btn = (f'<a class="btn solid" href="{WA}" rel="noopener" target="_blank">Chat Ananta, CPA</a>')
    faq = ''.join(f'<details class="faq-i"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return (
        '<p class="eyebrow">Tim Konsultan Rumah Sakit</p>\n'
        f'<h1 style="margin:.2em 0 .5em;font-size:clamp(32px,4.4vw,54px);line-height:1.12">{NAMA}</h1>\n'
        '<p class="t" style="max-width:62em">Konsultan rumah sakit FA Indonesia untuk akreditasi, strategi, '
        'dan digitalisasi rumah sakit.</p>\n'
        f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px">{btn}'
        '<a class="btn line" href="/konsultan-rumah-sakit/">Konsultan Rumah Sakit</a></div>\n'
        f'<img alt="{NAMA}" class="sig-foto" height="875" src="{FOTO}" '
        'style="width:min(280px,70%);height:auto;border-radius:12px;margin:8px 0 18px" width="700"/>'
        f'<p>{NAMA} adalah dokter dengan latar magister kesehatan. Di tim konsultan rumah sakit FA Indonesia, '
        'dr. Amien memegang tiga bidang: persiapan akreditasi, strategi pengembangan rumah sakit, dan '
        'digitalisasi layanan serta sistem informasi rumah sakit.</p>'
        '<p>Sisi medis, marketing, dan operasional dipegang <a href="/dr-sigit-riyarto/">dr. Sigit Riyarto, '
        'M.Kes, AAK</a>. Sisi keuangan, valuasi, M&amp;A, dan seller side dipegang <a href="/ananta-w-sasongko/">'
        'Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP</a>.</p>'
        '<h2>Bidang yang Ditangani</h2>'
        '<h3>Akreditasi Rumah Sakit</h3><p>Pemetaan kesiapan terhadap standar, penyusunan dan penataan dokumen, '
        'telusur unit, sampai pendampingan menjelang survei. <a href="/konsultan-akreditasi-rumah-sakit/">'
        'Konsultan Akreditasi Rumah Sakit</a></p>'
        '<h3>Strategi Rumah Sakit</h3><p>Arah layanan unggulan, rencana pengembangan, dan urutan prioritas '
        'investasi yang selaras dengan kemampuan keuangan rumah sakit. <a href="/konsultan-rumah-sakit/">'
        'Konsultan Rumah Sakit</a></p>'
        '<h3>Digitalisasi Rumah Sakit</h3><p>Pemilihan dan penerapan SIMRS, alur data dari layanan sampai klaim, '
        'dan laporan manajemen yang bisa dipakai direksi. <a href="/konsultan-simrs/">Konsultan SIMRS</a></p>'
        '<h2>Bersama Tim Rumah Sakit</h2>'
        '<img alt="Tim Konsultan Rumah Sakit FA Indonesia" height="996" loading="lazy" '
        'src="/img/tim-konsultan-rumah-sakit-fa.jpg" style="width:min(560px,100%);height:auto;border-radius:12px;'
        'margin:6px 0 10px" width="900"/>'
        '<ul><li><a href="/konsultan-bpjs-rumah-sakit/">BPJS Rumah Sakit</a></li>'
        '<li><a href="/konsultan-unit-cost-rumah-sakit/">Unit Cost Rumah Sakit</a></li>'
        '<li><a href="/direktur-rumah-sakit/">Direktur Rumah Sakit</a></li>'
        '<li><a href="/pendanaan-rumah-sakit/">Pendanaan Rumah Sakit</a></li></ul>\n'
        f'<h2>Pertanyaan Umum</h2><div class="faq-acc">{faq}</div>'
        f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px">{btn}</div>\n'
    )


def ldjson():
    g = {"@context": "https://schema.org", "@graph": [
        {"@type": "Person", "@id": URL + "#person", "name": "Amien Mujib Bahruddin",
         "honorificPrefix": "dr.", "honorificSuffix": "M.Kes", "jobTitle": "Konsultan Rumah Sakit",
         "image": "https://faindonesia.co.id" + FOTO, "url": URL,
         "knowsAbout": ["Akreditasi rumah sakit", "Strategi rumah sakit", "Digitalisasi rumah sakit", "SIMRS"],
         "worksFor": {"@type": "ProfessionalService", "@id": "https://faindonesia.co.id/#org",
                      "name": "FA Indonesia", "url": "https://faindonesia.co.id/"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                                               "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "FA Indonesia", "item": "https://faindonesia.co.id/"},
            {"@type": "ListItem", "position": 2, "name": "Layanan", "item": "https://faindonesia.co.id/layanan/"},
            {"@type": "ListItem", "position": 3, "name": "dr. Amien Mujib Bahruddin", "item": URL}]}]}
    return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + '</script>'


def build_profile():
    s = open(os.path.join(ROOT, 'dr-sigit-riyarto', 'index.html'), encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta content=")[^"]*(" name="description"/>)', lambda m: m.group(1) + DESC + m.group(2), s)
    s = re.sub(r'(<meta content=")[^"]*(" (?:property|name)="(?:og|twitter):title"/>)',
               lambda m: m.group(1) + TITLE + m.group(2), s)
    s = re.sub(r'(<meta content=")[^"]*(" (?:property|name)="(?:og|twitter):description"/>)',
               lambda m: m.group(1) + DESC + m.group(2), s)
    s = s.replace('/img/og-page/dr-sigit-riyarto.jpg', f'/img/og-page/{SLUG}.jpg')
    s = s.replace('https://faindonesia.co.id/dr-sigit-riyarto/', URL)
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@graph": \[\{"@type": "Service".*?</script>',
               lambda m: ldjson(), s, count=1, flags=re.S)
    a = s.index('<p class="eyebrow">Tim Konsultan Rumah Sakit</p>')
    b = s.index('<div style="margin:44px 0 0')
    s = s[:a] + main_html() + s[b:]
    s = re.sub(r'<script id="sig-person" type="application/ld\+json">.*?</script>', '', s, flags=re.S)
    left = [m.start() for m in re.finditer('Sigit|sigit', s)]
    allowed = s.count('href="/dr-sigit-riyarto/">dr. Sigit Riyarto') * 2
    assert len(left) <= allowed,('sisa Sigit', len(left), [s[i-80:i+40] for i in left])
    return s


def main():
    changed = 0
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            s = open(p, encoding='utf-8').read()
            if 'sigit' not in s.lower():
                continue
            n = patch(s)
            if n != s:
                changed += 1
                if not DRY:
                    open(p, 'w', encoding='utf-8').write(n)
    # profil dr. Sigit: pembagian peran
    sp = os.path.join(ROOT, 'dr-sigit-riyarto', 'index.html')
    s = open(sp, encoding='utf-8').read()
    o = 'akreditasi, layanan unggulan, cost cutting, dan manajemen.'
    w = ('layanan unggulan, cost cutting, dan manajemen. Akreditasi, strategi, dan digitalisasi rumah sakit '
         f'dipegang <a href="/{SLUG}/">{NAMA}</a>.')
    if o in s and not DRY:
        open(sp, 'w', encoding='utf-8').write(s.replace(o, w))
    prof = build_profile()
    pp = os.path.join(ROOT, SLUG, 'index.html')
    if not DRY:
        os.makedirs(os.path.dirname(pp), exist_ok=True)
        open(pp, 'w', encoding='utf-8').write(prof)
    # sitemap + llms
    sm = os.path.join(ROOT, 'sitemap.xml')
    t = open(sm, encoding='utf-8').read()
    if URL not in t and not DRY:
        line = '<url><loc>https://faindonesia.co.id/dr-sigit-riyarto/</loc>'
        i = t.index(line)
        j = t.index('</url>', i) + len('</url>')
        t = t[:j] + f'\n<url><loc>{URL}</loc><lastmod>2026-11-17</lastmod><priority>0.9</priority></url>' + t[j:]
        open(sm, 'w', encoding='utf-8').write(t)
    ll = os.path.join(ROOT, 'llms.txt')
    t = open(ll, encoding='utf-8').read()
    if URL not in t and not DRY:
        k = 'https://faindonesia.co.id/dr-sigit-riyarto/\n'
        t = t.replace(k, k + f'- {NAMA} (tim RS FA: akreditasi, strategi, digitalisasi rumah sakit) → {URL}\n', 1)
        open(ll, 'w', encoding='utf-8').write(t)
    print('halaman berubah:', changed, '| profil:', pp, '| dry' if DRY else '')


if __name__ == '__main__':
    main()
