#!/usr/bin/env python3
"""8 Nov 2026 (permintaan Bos): FA jangan terasa makelar. Klien langsung berurusan
dengan Ananta W. Sasongko, CPA.

BEKERJA LANGSUNG DI out/faindonesia (lihat PERINGATAN BUILD di README-DEPLOY).
Jalankan SETELAH prep.py dan script out/ lain. Idempoten.

1. Blok fa-wajah ("Tiga Orang di Balik FA, KJA, dan KAP" / "Tim yang Menangani")
   diganti blok fa-langsung "Ditangani Langsung, Bukan Diteruskan" (kartu Ananta,
   tanpa kartu kalau halaman sudah memuat tim RS Ananta + dr. Sigit).
2. Strip <!--dhn--> KAP DHN / KJA Farhani: hanya di halaman audit (path berisi
   "audit", segmen "kap", /kap-dhn/, /mitra-kap-kja/, /saturn/), dan hanya bagian
   KAP, tanpa kata "Mitra". Halaman lain: strip dikosongkan (penanda tetap).
3. Kalimat mitra / jaringan mitra / dicarikan / menghubungkan diganti kalimat langsung.
4. Tombol WA ke nomor Bos: "Chat WhatsApp", "Chat Tim FA Indonesia", dst. jadi
   "Chat Ananta, CPA" (EN: "Chat with Ananta, CPA"). Tombol tim RS (Ananta + dr. Sigit)
   tidak diubah. Pesan WA "Halo FA Indonesia," jadi "Halo Pak Ananta,".
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'faindonesia')
WA = 'https://wa.me/6282245260121'

# (lama, baru) plain string, diterapkan untuk versi &amp; (HTML) dan & (JSON-LD)
PLAIN = [
    ('Bisa diarahkan ke KAP mitra yang terdaftar OJK.', 'Bisa, oleh KAP DHN &amp; Rekan yang terdaftar OJK.'),
    ('Audit oleh KAP mitra untuk', 'Audit oleh KAP DHN &amp; Rekan (terdaftar OJK) untuk'),
    ('KAP DHN &amp; Rekan, mitra FA yang terdaftar OJK, untuk perusahaan di', 'KAP DHN &amp; Rekan (terdaftar OJK) untuk perusahaan di'),
    ('Hubungi kami lewat WhatsApp untuk diskusi awal.', 'Diskusi awalnya langsung dengan Ananta W. Sasongko, CPA lewat WhatsApp.'),
    ('Audit dilakukan KAP mitra yang terdaftar OJK.', 'Audit dilakukan KAP DHN &amp; Rekan yang terdaftar OJK.'),
    ('audit lewat KAP mitra,', 'audit oleh KAP terdaftar OJK,'),
    ('Audit dilaksanakan KAP mitra terdaftar OJK;', 'Audit dilaksanakan KAP DHN &amp; Rekan (terdaftar OJK);'),
    ('jasa audit laporan keuangan lewat KAP mitra,', 'jasa audit laporan keuangan oleh KAP terdaftar OJK,'),
    ('bersama KAP mitra terdaftar OJK', 'oleh KAP terdaftar OJK'),
    (', kantor akuntan publik mitra yang terdaftar OJK', ', kantor akuntan publik yang terdaftar OJK'),
    ('Audit lewat KAP mitra terdaftar OJK', 'Audit oleh KAP DHN &amp; Rekan (terdaftar OJK)'),
    ('lalu audit dilaksanakan KAP mitra yang terdaftar OJK', 'lalu audit dilaksanakan KAP DHN &amp; Rekan yang terdaftar OJK'),
    ('KAP mitra yang terdaftar OJK', 'KAP DHN &amp; Rekan yang terdaftar OJK'),
    ('KAP mitra terdaftar OJK', 'KAP DHN &amp; Rekan (terdaftar OJK)'),
    ('Jaringan mitra kami menangani', 'Kami menangani'),
    ('Mitra kami pernah menangani', 'Kami pernah menangani'),
    ('Mitra kami berpengalaman', 'Kami berpengalaman'),
    ('Audit tetap dilakukan KAP independen; bila dibutuhkan, kami bantu menghubungkan dengan KAP berizin yang sesuai.',
     'Audit tetap dilakukan KAP independen yang terdaftar OJK, terpisah dari penyusun laporan keuangan.'),
    ('Ditangani tim Chartered Accountant dan CPA yang mengikuti SAK terbaru',
     'Anda berdiskusi langsung dengan Ananta W. Sasongko, CPA, yang mengikuti SAK terbaru'),
    ('>KAP Mitra FA</a>', '>KAP DHN &amp; Rekan</a>'),
    ('KAP Mitra dan Pilihan Lain', 'KAP yang Mengaudit dan Pilihan Lain'),
    (', dikerjakan bersama KJA mitra.', ', dikerjakan langsung bersama Ananta W. Sasongko, CPA.'),
    ('KJA mitra kami bisa membantu sebelum audit dimulai.', 'Kami bisa membantu merapikannya sebelum audit dimulai.'),
    ('<a href="/kap-dhn/">KAP mitra FA yang terdaftar OJK</a>', '<a href="/kap-dhn/">KAP DHN &amp; Rekan yang terdaftar OJK</a>'),
    ('</a>, KAP mitra di jaringan FA.', '</a>, KAP yang terdaftar OJK.'),
    ('misalnya KAP mitra di jaringan FA Indonesia.', 'misalnya KAP DHN &amp; Rekan.'),
    ('<td>Koordinator: Dr. (C) Ananta', '<td>Ditangani langsung: Dr. (C) Ananta'),
    ('Kami membantu menyiapkan laporan dan menghubungkan dengan KAP yang sesuai.',
     'Kami menyiapkan laporannya; auditnya oleh KAP DHN &amp; Rekan yang terdaftar OJK, atau KAP rekanan bank Anda.'),
    ('Untuk kebutuhan audit atau reviu, kami membantu menghubungkan dengan KAP berizin yang sesuai tanpa konflik kepentingan.',
     'Audit atau reviu tetap dilakukan KAP independen yang terdaftar OJK, terpisah dari penyusun laporan keuangan.'),
    ('kami bisa menyiapkan data dan menghubungkan dengan KJPP yang sesuai.', 'kami menyiapkan datanya untuk KJPP yang Anda atau bank pilih.'),
    ('FA Indonesia bekerja dengan jaringan mitra lengkap, sehingga pembukuan, pajak, audit, sampai kredit bank dan investor bisa diurus dari satu pintu.',
     'Anda cukup bicara dengan Ananta W. Sasongko, CPA: pembukuan, pajak, persiapan audit, sampai kredit bank dan investor dibahas langsung, sementara audit tetap dilakukan KAP DHN &amp; Rekan yang independen.'),
    ('<p class="eyebrow">Partner</p><h2>Tiga Orang di Balik FA, KJA, dan KAP</h2>', '<p class="eyebrow">Tim</p><h2>Ditangani Langsung, Bukan Diteruskan</h2>'),
    ('<h2 data-i18n="k197">Mitra Profesional</h2>', '<h2 data-i18n="k197">Kantor Berizin Terafiliasi</h2>'),
    ('Kantor Akuntan Publik Mitra, Terdaftar OJK', 'Kantor Akuntan Publik, Terdaftar OJK'),
    ('<small>Kantor Akuntan Publik Mitra</small>', '<small>Kantor Akuntan Publik</small>'),
    ('Kantor Akuntan Publik Mitra', 'Kantor Akuntan Publik'),
    ('Koordinator, Kredit, Investor, dan Pendampingan Audit', 'Laporan Keuangan, Kredit, Investor, dan Pendampingan Audit'),
    ('langsung chat tim kami', 'langsung chat Ananta, CPA'),
    ('kami bantu rekomendasikan notaris rekanan', 'kami bantu cek notaris yang Anda pilih'),
]

RX = [
    # FAQ wilayah: "Tim FA Indonesia bersama KJA mitra melayani"
    (re.compile(r'Tim FA ([A-Z][\w\- ]*?) bersama KJA mitra melayani'), r'Ananta W. Sasongko, CPA dan tim FA \1 melayani'),
    (re.compile(r'KAP-nya bisa dicarikan di cariakuntan\.com/[^<."]*\.'), 'Auditnya oleh KAP DHN &amp; Rekan yang terdaftar OJK.'),
    (re.compile(r'>Minta rekomendasi di [^<]+</a>'), '>Tanya Ananta, CPA</a>'),
]

# /wilayah/<kota>/: "KAP, KJA, dan Konsultan Pajak Mitra FA untuk X"
RX_MITRA_H2 = re.compile(r'<h2 id="kap-kja-dan-konsultan-pajak-mitra-fa-untuk-([\w\-]+)">KAP, KJA, dan Konsultan Pajak Mitra FA untuk ([^<]+)</h2><p>.*?</p>', re.S)
RX_MITRA_TOC = re.compile(r'<li><a href="#kap-kja-dan-konsultan-pajak-mitra-fa-untuk-([\w\-]+)">KAP, KJA, dan Konsultan Pajak Mitra FA untuk ([^<]+)</a></li>')

def mitra_h2(m):
    return ('<h2 id="siapa-yang-mengerjakan-di-%s">Siapa yang Mengerjakan di %s</h2><p>Anda berdiskusi langsung dengan '
            '<a href="/ananta-w-sasongko/">Ananta W. Sasongko, CPA</a> sejak chat pertama: ia membaca dokumen Anda, menyusun '
            'rencana kerja, dan memeriksa hasilnya sebelum diserahkan. Audit laporan keuangan dilakukan '
            '<a href="/kap-dhn/">KAP DHN &amp; Rekan</a> yang terdaftar OJK, karena penyusun dan auditor harus pihak yang berbeda.</p>'
            % (m.group(1), m.group(2)))

RX_WAJAH = re.compile(r'<!--fa-wajah-->.*?<!--/fa-wajah-->', re.S)
RX_LAYTIM = re.compile(r'<!--fa-lay-tim-->.*?<!--/fa-lay-tim-->', re.S)
RX_TOC_WAJAH = re.compile(r'<li><a href="#(tiga-orang-di-balik-fa-kja-dan-kap|tim-yang-menangani)">[^<]*</a></li>')
RX_DHN = re.compile(r'<!--dhn-->(.*?)<!--/dhn-->', re.S)

CARD = ('<a class="fl-card" href="/ananta-w-sasongko/" style="display:grid;grid-template-columns:120px minmax(0,1fr);gap:16px;'
        'align-items:center;border:1px solid #333;border-radius:12px;overflow:hidden;background:#1e1e1e;color:inherit;'
        'text-decoration:none;margin:14px 0 12px;max-width:640px"><img alt="Ananta W. Sasongko, CPA" decoding="async" '
        'height="150" loading="lazy" src="/img/ananta-w-sasongko-cpa.jpg" style="display:block;width:120px;height:150px;'
        'object-fit:cover;object-position:50% 18%" width="120"/><div style="padding:12px 14px 12px 0"><small style="display:block;'
        'font-size:11px;letter-spacing:.16em;text-transform:uppercase;opacity:.7;margin-bottom:4px">Kontak Anda Sejak Awal</small>'
        '<b style="display:block;font-size:16px;line-height:1.3;font-weight:600">Ananta W. Sasongko, CPA</b><span style="display:block;'
        'font-size:13px;line-height:1.5;opacity:.78;margin-top:4px">Pernah berkarir di EY, lalu direktur keuangan dan group CFO '
        'di beberapa rumah sakit dan perusahaan. Kandidat doktor ilmu akuntansi.</span></div></a>')

def is_audit(rel):
    p = rel.replace('\\', '/').lower()
    segs = p.split('/')
    if 'audit' in p or 'saturn' in p:
        return True
    if segs[0] in ('kap-dhn', 'mitra-kap-kja'):
        return True
    return any(re.search(r'(^|-)kap(-|$)', s) for s in segs)

def langsung_block(audit, has_rs_team):
    p = ('Sejak chat pertama Anda bicara langsung dengan Ananta W. Sasongko, CPA. Ia yang membaca dokumen Anda, '
         'menyusun rencana kerja, dan memeriksa hasilnya sebelum diserahkan, supaya siap dipakai bank, auditor, dan investor.')
    if audit:
        p += (' Diskusi awal, ruang lingkup, dan persiapan dokumen Anda bicarakan langsung dengannya; audit dan opininya '
              'dilakukan KAP DHN &amp; Rekan yang terdaftar OJK.')
    p += ' Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda.'
    return ('<!--fa-langsung--><h2 id="ditangani-langsung-bukan-diteruskan">Ditangani Langsung, Bukan Diteruskan</h2>'
            + ('' if has_rs_team else CARD) + '<p>' + p + '</p><!--/fa-langsung-->')

def new_dhn(m, audit):
    body = m.group(1)
    if not audit:
        return '<!--dhn--><!--/dhn-->'
    # sisakan elemen KAP saja (strip .dhns tanpa kelas kja, atau kartu aside.dhnc)
    keep = ''
    a = re.search(r'<aside[^>]*class="dhnc".*?</aside>', body, re.S)
    if a:
        keep = a.group(0)
    else:
        for d in re.finditer(r'<div class="dhns">.*?</a></div>', body, re.S):
            keep = d.group(0); break
    return '<!--dhn-->' + keep + '<!--/dhn-->'

LABELS_ID = ('Chat WhatsApp', 'Chat Tim FA Indonesia', 'Diskusikan dengan Tim FA Indonesia')
RX_WA_A = re.compile(r'(<a [^>]*href="' + re.escape(WA) + r'(?:\?text=[^"]*)?"[^>]*>)([^<]*)(</a>)')

def fix_wa(m):
    lab = m.group(2).strip()
    if lab in LABELS_ID:
        return m.group(1) + 'Chat Ananta, CPA' + m.group(3)
    if lab == 'Chat on WhatsApp':
        return m.group(1) + 'Chat with Ananta, CPA' + m.group(3)
    return m.group(0)


# ---- Tahap 2 (8 Nov 2026 pagi, Bos): blok foto tim di PALING ATAS, tepat di bawah tombol hero "Chat Ananta, CPA".
# Halaman RS: blok Tim Konsultan Rumah Sakit (fa-rstim) dipindah ke atas. Halaman audit: 3 orang (Ananta, Farhani, Dwi).
# Halaman lain yang punya fa-langsung: blok itu dipindah ke atas.
WJ_CSS = ('<style>.wj{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:14px 0 10px}'
          '.wj a{display:block;border:1px solid #333;border-radius:12px;overflow:hidden;background:#1e1e1e;color:inherit;text-decoration:none}'
          '.wj a:hover{border-color:#777}.wj img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 18%}'
          '.wj div{padding:12px 14px 14px}.wj small{display:block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;opacity:.7;margin-bottom:4px}'
          '.wj b{display:block;font-size:15.5px;line-height:1.3;font-weight:600}.wj span{display:block;font-size:12.5px;line-height:1.45;opacity:.75;margin-top:4px}'
          '@media(max-width:720px){.wj{grid-template-columns:1fr;gap:10px}.wj a{display:grid;grid-template-columns:96px 1fr;align-items:center}}</style>')

TIGA = (WJ_CSS + '<h2 id="tim-yang-menangani-audit-anda">Tim yang Menangani Audit Anda</h2><div class="wj">'
        '<a href="/ananta-w-sasongko/"><img alt="Ananta W. Sasongko, CPA" decoding="async" height="1050" loading="lazy" src="/img/ananta-w-sasongko-cpa.jpg" width="700"/>'
        '<div><small>FA Indonesia</small><b>Ananta W. Sasongko, CPA</b><span>Kontak Anda Sejak Awal, Persiapan Audit dan Laporan Keuangan</span></div></a>'
        '<a href="/kja-farhani/"><img alt="Farhani Kautsar Nugraha, S.E., M.S.A., Ak., CA" decoding="async" height="1050" loading="lazy" src="/img/farhani-k-nugraha-fa-indonesia.jpg" width="700"/>'
        '<div><small>KJA Farhani</small><b>Farhani Kautsar Nugraha, S.E., M.S.A., Ak., CA</b><span>Pembukuan dan Penyusunan Laporan Keuangan</span></div></a>'
        '<a href="/kap-dhn/"><img alt="Dr. (C) Dwi Haryadi Nugraha, SST, MSi, Ak, CA, BKP, ASEAN CPA, CPA, CFI" decoding="async" height="1050" loading="lazy" src="/img/dwi-haryadi-nugraha-kap-dhn-v2.jpg" width="700"/>'
        '<div><small>KAP DHN &amp; Rekan</small><b>Dr. (C) Dwi Haryadi Nugraha, SST, MSi, Ak, CA, BKP, ASEAN CPA, CPA, CFI</b><span>Pemimpin Rekan, Audit Laporan Keuangan</span></div></a></div>'
        '<p>Sejak chat pertama Anda bicara langsung dengan Ananta W. Sasongko, CPA. Audit dan opininya dilakukan KAP DHN &amp; Rekan yang terdaftar OJK. '
        'Untuk satu entitas, penyusun laporan keuangan dan auditornya selalu pihak yang berbeda.</p>')

RX_RSTIM = re.compile(r'<!--fa-rstim--><div class="rstb">.*?<!--/fa-rstim-->', re.S)
RX_LANG = re.compile(r'<!--fa-langsung-->.*?<!--/fa-langsung-->', re.S)
RX_HERO = re.compile(r'<div class="cbtns"[^>]*>.*?</div>', re.S)
RX_TOC_ANY = re.compile(r'<li><a href="#(ditangani-langsung-bukan-diteruskan|tim-yang-menangani-audit-anda)">[^<]*</a></li>')

def tim_atas(rel, t):
    if '<!--fa-tim-atas-->' in t:
        return t
    h = t.find('<h1')
    if h < 0:
        return t
    m = RX_HERO.search(t, h)
    if not m or 'Chat Ananta, CPA' not in m.group(0):
        return t
    block = None
    rs = RX_RSTIM.search(t)
    if rs:
        block = rs.group(0)
        t = t[:rs.start()] + t[rs.end():]
        t = RX_LANG.sub('', t)
    elif is_audit(rel):
        block = TIGA
        t = RX_LANG.sub('', t)
    else:
        lg = RX_LANG.search(t)
        if lg:
            block = lg.group(0)
            t = t[:lg.start()] + t[lg.end():]
    if not block:
        return t
    t = RX_TOC_ANY.sub('', t)
    m = RX_HERO.search(t, t.find('<h1'))
    ins = '<!--fa-tim-atas--><div style="margin:30px 0 8px">' + block + '</div><!--/fa-tim-atas-->'
    return t[:m.end()] + ins + t[m.end():]

def process(rel, t):
    o = t
    audit = is_audit(rel)
    for a, b in PLAIN:
        t = t.replace(a, b)
        if '&amp;' in a or '&amp;' in b:
            t = t.replace(a.replace('&amp;', '&'), b.replace('&amp;', '&'))
    for rx, rep in RX:
        t = rx.sub(rep, t)
    t = RX_MITRA_H2.sub(mitra_h2, t)
    t = RX_MITRA_TOC.sub(lambda m: '<li><a href="#siapa-yang-mengerjakan-di-%s">Siapa yang Mengerjakan di %s</a></li>' % (m.group(1), m.group(2)), t)
    if '<!--fa-wajah-->' in t:
        rs = 'dr-sigit-riyarto-mkes-aak.jpg' in t
        t = RX_WAJAH.sub(lambda m: langsung_block(audit, rs), t)
        t = RX_TOC_WAJAH.sub('<li><a href="#ditangani-langsung-bukan-diteruskan">Ditangani Langsung, Bukan Diteruskan</a></li>', t)
    if '<!--fa-lay-tim-->' in t:
        t = RX_LAYTIM.sub(lambda m: '<!--fa-lay-tim-->' + CARD + '<p>Sejak chat pertama Anda bicara langsung dengan Ananta W. Sasongko, CPA. Ia yang membaca dokumen Anda, menyusun rencana kerja, dan memeriksa hasilnya sebelum diserahkan. Audit laporan keuangan dilakukan KAP DHN &amp; Rekan yang terdaftar OJK, terpisah dari penyusun laporan keuangan.</p><!--/fa-lay-tim-->', t)
    t = RX_DHN.sub(lambda m: new_dhn(m, audit), t)
    t = RX_WA_A.sub(fix_wa, t)
    t = t.replace(WA + '?text=Halo%20FA%20Indonesia%2C', WA + '?text=Halo%20Pak%20Ananta%2C')
    t = t.replace(WA + '?text=Halo%20Tim%20FA%20Indonesia%2C', WA + '?text=Halo%20Pak%20Ananta%2C')
    t = t.replace(WA + '?text=Hello%20FA%20Indonesia%2C', WA + '?text=Hello%20Pak%20Ananta%2C')
    t = tim_atas(rel, t)
    return t, t != o

def main():
    dry = '--dry' in sys.argv
    n = 0
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT)
            with open(p, encoding='utf-8') as h:
                t = h.read()
            t2, ch = process(rel, t)
            if ch:
                n += 1
                if not dry:
                    with open(p, 'w', encoding='utf-8') as h:
                        h.write(t2)
    print(('[dry] ' if dry else '') + 'fa_langsung: %d file berubah' % n)

if __name__ == '__main__':
    main()
