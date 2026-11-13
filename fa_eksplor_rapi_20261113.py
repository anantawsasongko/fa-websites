#!/usr/bin/env python3
"""Tata ulang halaman Eksplor FA (/artikel/) supaya sistematis, TANPA mengurangi SEO (13 Nov 2026).
BEKERJA LANGSUNG DI out/faindonesia/artikel/index.html, idempoten. Membangun ulang isi di antara
<!--fa-seo-cards--> ... <!--/fa-seo-cards--> dari SEMUA kartu <a class="card2"> yang ada di blok itu.

Pemicu (Bos): "Halaman eksplor masih jelek dan gak sistematis di FA. Tata ulang. Tanpa mengurangi SEO."
Masalah lama: 30 artikel lead + 4 artikel WTP menumpuk di topik Rumah Sakit (audit, kredit, forensik, valuasi ikut
di situ), satu kolom, tinggi halaman 16 ribu px (desktop) dan 21 ribu px (mobile).

Yang dijaga (SEO): H1, paragraf pembuka, semua URL kartu, judul dan deskripsi kartu (teks sama persis), id anchor
topik lama (#t-rumah-sakit dst.), semua link chip lama. Tidak ada link yang dibuang; script berhenti bila jumlah
URL unik sesudah tidak sama dengan sebelum.

Yang berubah: kartu dipindah ke topik yang benar (+ topik baru Forensik dan Kerugian), grid 3 kolom (2 di tablet,
1 di mobile), tiap topik tampil 6 kartu + "Lihat Semua (n)" (kartu sisanya tetap ada di HTML), navigasi topik
dengan jumlah artikel, kotak cari judul, dan baris lompat ke Galeri / Berita Terkini.

URUTAN: jalankan SETELAH semua generator yang menyisipkan kartu Eksplor (fa_seo, fa_seo20, fa_artikel_wtp,
fa_artikel_lead, dst.) dan SEBELUM fa_rendah_hati_20261112.py. Kartu baru yang disisipkan generator lain di topik
pertama akan otomatis dipilah oleh script ini (MOVE lalu aturan kata kunci). Dry run: --dry.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, 'out', 'faindonesia', 'artikel', 'index.html')
A, B = '<!--fa-seo-cards-->', '<!--/fa-seo-cards-->'
SHOW = 6

# urutan tampil: (id, judul, keterangan singkat)
TOPICS = [
    ('t-rumah-sakit', 'Rumah Sakit', 'Unit cost, klaim BPJS, iDRG, valuasi, dan jual beli rumah sakit.'),
    ('t-kredit-bank', 'Kredit Bank', 'Syarat, dokumen, rasio, dan cara bank membaca usaha Anda.'),
    ('t-laporan-keuangan', 'Laporan Keuangan', 'Menyusun dan merapikan laporan keuangan sesuai standar.'),
    ('t-audit-kap', 'Audit &amp; KAP', 'Kapan wajib audit, memilih KAP, opini, dan persiapannya.'),
    ('t-penilaian-kjpp', 'Penilaian &amp; KJPP', 'Valuasi usaha, penilaian aset, dan studi kelayakan.'),
    ('t-investor-ipo', 'Investor &amp; IPO', 'Mencari investor, menjual saham, dan persiapan IPO.'),
    ('t-forensik', 'Forensik &amp; Kerugian', 'Penghitungan kerugian dan peran akuntan dalam sengketa.'),
    ('t-pajak', 'Pajak', 'Cara hitung PPh, PPN, dan pajak tangguhan.'),
    ('t-cfo-tata-kelola', 'CFO &amp; Tata Kelola', 'Peran CFO, komite audit, dan komisaris independen.'),
    ('t-psak', 'PSAK &amp; SAK Terbaru', 'Standar baru dan amendemen yang berlaku 2026 sampai 2027.'),
]
TID = [t[0] for t in TOPICS]

# pindah eksplisit: slug -> id topik
MOVE = {}
for tid, slugs in {
    't-audit-kap': ['audit-laporan-keuangan-perusahaan-tambang-kontraktor-kalimantan', 'audit-laporan-keuangan-pt-pma-persiapan',
                    'audit-selesai-sebelum-akhir-tahun-target-realistis', 'cara-membaca-surat-penawaran-audit-kap',
                    'laporan-keuangan-audited-untuk-tender-migas-bumn', 'dari-opini-wdp-ke-wtp',
                    'opini-tidak-menyatakan-pendapat-disclaimer', 'laporan-audit-lama-keluar'],
    't-laporan-keuangan': ['keaslian-data-laporan-keuangan-untuk-bank', 'laporan-keuangan-bank-dan-pajak-harus-sejalan',
                           'laporan-keuangan-usaha-pariwisata-bali', 'menyusun-laporan-keuangan-dari-rekening-koran',
                           'pertanyaan-sebelum-menyusun-laporan-keuangan-pt', 'laporan-keuangan-bankable-investor-ready'],
    't-kredit-bank': ['kredit-konstruksi-developer-perumahan-dokumen', 'laporan-keuangan-interim-triwulan-untuk-kredit',
                      'penjualan-tunai-dan-money-changer-dibaca-bank', 'perpanjangan-prk-sambil-mengajukan-ke-bank-lain',
                      'rencana-kerja-3-bulan-sebelum-mengajukan-kredit', 'kredit-bank-klinik-dental-kecantikan-cabang-baru'],
    't-forensik': ['ahli-akuntansi-di-penyidikan-dan-persidangan', 'dokumen-menghitung-kerugian-penggelapan',
                   'kerja-sama-kuasa-hukum-pembuktian-kerugian', 'laporan-penghitungan-kerugian-proyek-akuntan-publik',
                   'metode-menghitung-kerugian-keuangan'],
    't-penilaian-kjpp': ['studi-kelayakan-proyek-wisata-pemegang-saham', 'valuasi-indikatif-vs-valuasi-lengkap',
                         'valuasi-usaha-umkm-penjualan-marketplace', 'valuasi-perusahaan-swasta-dcf-multiple-ebitda',
                         'cara-menghitung-wacc-dan-valuasi-dcf-perusahaan-indonesia'],
    't-investor-ipo': ['menawarkan-usaha-kecil-ke-investor-langkah', 'menentukan-harga-saham-usaha-keluarga-partner-baru'],
}.items():
    for s in slugs:
        MOVE[s] = tid

RS_KEY = ('rumah-sakit', 'rsia', 'klinik', 'idrg', 'unit-cost', 'bpjs', 'permenkes')
# untuk kartu baru yang nyasar ke topik pertama (generator menyisipkan di depan kartu pertama)
RULES = [
    ('t-forensik', ('kerugian', 'forensik', 'penggelapan', 'persidangan')),
    ('t-audit-kap', ('audit', 'opini', 'kap-')),
    ('t-kredit-bank', ('kredit', 'prk', 'pinjaman', 'agunan')),
    ('t-penilaian-kjpp', ('valuasi', 'penilaian', 'kjpp', 'kelayakan')),
    ('t-investor-ipo', ('investor', 'ipo', 'saham')),
    ('t-pajak', ('pajak', 'pph', 'ppn', 'coretax')),
    ('t-psak', ('psak', 'isak')),
    ('t-laporan-keuangan', ('laporan-keuangan', 'pembukuan')),
]

CSS = ('<style id="eks-css">'
       '.eks-jump{display:flex;flex-wrap:wrap;gap:8px 18px;margin:0 0 26px;font-size:14px;color:var(--muted)}'
       '.eks-jump a{color:#fff;text-decoration:none;border-bottom:1px solid #555;padding-bottom:1px}'
       '.eks-jump a:hover{border-color:#fff}'
       '.eks-bar{position:sticky;top:var(--eks-top,58px);z-index:5;margin:0 calc(-1*clamp(16px,4vw,40px));padding:12px clamp(16px,4vw,40px) 10px;'
       'background:rgba(18,18,18,.94);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-bottom:1px solid #2c2c2c}'
       '.eks-bar .chips2{margin:0;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}'
       '.eks-bar .chips2::-webkit-scrollbar{display:none}'
       '.eks-bar .chips2 a{white-space:nowrap;flex:none}'
       '.eks-bar .chips2 a i{font-style:normal;font-weight:400;color:var(--muted);margin-left:6px}'
       '.eks-top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 24px;margin:26px 0 0}'
       '.eks-top p{margin:0;color:var(--muted);font-size:14px}'
       '.eks-q{flex:1 1 260px;max-width:380px}'
       '.eks-q input{width:100%;box-sizing:border-box;height:42px;padding:0 14px;border:1px solid #3a3a3a;border-radius:2px;'
       'background:#161616;color:#fff;font:inherit;font-size:14px}'
       '.eks-q input:focus{outline:none;border-color:#fff}'
       '#eks .topic{margin:44px 0 0;scroll-margin-top:calc(var(--eks-top,58px) + 70px)}'
       '#eks .topic-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;margin:0 0 16px;padding:0 0 12px;'
       'border-bottom:1px solid #2c2c2c}'
       '#eks .topic-h h2{margin:0}'
       '#eks .topic-h .n{font-size:13px;color:var(--muted);letter-spacing:.04em}'
       '#eks .topic-h p{flex:1 1 100%;margin:0;color:var(--muted);font-size:14px}'
       '#eks .cards2{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;max-width:none}'
       '#eks .card2{display:flex;flex-direction:column;height:100%;box-sizing:border-box;padding:18px 20px;'
       'transition:border-color .2s,transform .2s}'
       '#eks .card2:hover{border-color:#fff;transform:translateY(-2px)}'
       '#eks .card2 b{font-size:18px;line-height:1.3;margin-bottom:8px}'
       '#eks .card2 span{line-height:1.55}'
       '#eks details.eks-more{margin:14px 0 0}'
       '#eks details.eks-more>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:8px;'
       'padding:9px 16px;border:1px solid #555;border-radius:999px;font-size:13px;font-weight:600;color:#fff;user-select:none}'
       '#eks details.eks-more>summary::-webkit-details-marker{display:none}'
       '#eks details.eks-more>summary:hover{border-color:#fff}'
       '#eks details.eks-more>summary:after{content:"";width:7px;height:7px;border-right:1.5px solid currentColor;'
       'border-bottom:1.5px solid currentColor;transform:rotate(45deg) translateY(-2px)}'
       '#eks details.eks-more[open]>summary:after{transform:rotate(-135deg) translateY(-2px)}'
       '#eks details.eks-more[open]>summary{margin-bottom:14px}'
       '#eks.q details.eks-more>summary{display:none}'
       '#eks .eks-none{display:none;margin:28px 0 0;color:var(--muted)}'
       '#eks [hidden]{display:none!important}'
       '@media(max-width:980px){#eks .cards2{grid-template-columns:repeat(2,minmax(0,1fr))}}'
       '@media(max-width:620px){#eks .cards2{grid-template-columns:minmax(0,1fr);gap:10px}'
       '#eks .card2{padding:14px 16px}#eks .card2 b{font-size:17px;margin-bottom:4px}'
       '#eks .card2 span{-webkit-line-clamp:1;font-size:13px}#eks .topic{margin-top:36px}}'
       '</style>')

JS = ('<script>(function(){var r=document.getElementById("eks"),q=document.getElementById("eks-q");if(!r||!q)return;'
      'var hd=document.querySelector("header.top");function st(){if(hd)r.style.setProperty("--eks-top",hd.offsetHeight+"px")}'
      'st();window.addEventListener("resize",st);'
      'var cs=[].slice.call(r.querySelectorAll("a.card2")),ts=[].slice.call(r.querySelectorAll(".topic")),'
      'ds=[].slice.call(r.querySelectorAll("details.eks-more")),no=r.querySelector(".eks-none"),was=null;'
      'q.addEventListener("input",function(){var v=q.value.trim().toLowerCase(),on=v.length>1;'
      'if(on&&was===null){was=ds.map(function(d){return d.open});ds.forEach(function(d){d.open=true})}'
      'if(!on&&was!==null){ds.forEach(function(d,i){d.open=was[i]});was=null}'
      'r.classList.toggle("q",on);var tot=0;'
      'cs.forEach(function(c){var ok=!on||c.textContent.toLowerCase().indexOf(v)>-1;c.hidden=!ok;if(ok)tot++});'
      'ts.forEach(function(t){t.hidden=on&&!t.querySelector("a.card2:not([hidden])")});'
      'if(no)no.style.display=on&&!tot?"block":"none"});'
      'if(location.hash){var t=document.getElementById(location.hash.slice(1));'
      'if(t&&t.classList.contains("topic")){var d=t.querySelector("details.eks-more");if(d)d.open=true}}'
      '})();</script>')


def slug_of(href):
    m = re.match(r'/artikel/([^/]+)/', href)
    return m.group(1) if m else href


def classify(slug, cur):
    if slug in MOVE:
        return MOVE[slug]
    if cur == 't-rumah-sakit' and not any(k in slug for k in RS_KEY):
        for tid, keys in RULES:
            if any(k in slug for k in keys):
                return tid
    return cur if cur in TID else 't-laporan-keuangan'


def main(dry=False):
    h = open(P, encoding='utf-8').read()
    a, b = h.find(A), h.find(B)
    if a < 0 or b < 0:
        sys.exit('penanda fa-seo-cards tidak ditemukan')
    blk = h[a + len(A):b]
    before = set(re.findall(r'href="([^"]+)"', blk))
    # chip lama yang bukan anchor topik (E-Book, Cari Akuntan, Update SAK, Per Kota) dipertahankan
    ext = []
    for m in re.finditer(r'<a href="([^"#][^"]*)"([^>]*)>([^<]+)</a>', blk):
        if 'class="card2"' in m.group(0):
            continue
        if m.group(1) not in [e[0] for e in ext]:
            ext.append((m.group(1), m.group(2), m.group(3)))
    # kartu, urut dokumen, dengan topik asalnya
    buckets = {t: [] for t in TID}
    seen = set()
    tok = re.compile(r'<div class="topic" id="([^"]+)"|(<a class="card2" href="([^"]+)"[^>]*>.*?</a>)', re.S)
    cur = TID[0]
    for m in tok.finditer(blk):
        if m.group(1):
            cur = m.group(1); continue
        href = m.group(3)
        if href in seen:
            continue
        seen.add(href)
        card = re.sub(r'\s+hidden(="")?', '', m.group(2))
        buckets[classify(slug_of(href), cur)].append(card)
    total = sum(len(v) for v in buckets.values())
    used = [t for t in TOPICS if buckets[t[0]]]

    chips = ''.join('<a href="#%s">%s<i>%d</i></a>' % (tid, name, len(buckets[tid])) for tid, name, _ in used)
    jump = ('<p class="eks-jump"><span>Di halaman ini:</span><a href="#eks">Artikel per Topik</a><a href="#galeri">Galeri</a>'
            '<a href="#berita">Berita Terkini</a>'
            + ''.join('<a href="%s"%s>%s</a>' % e for e in ext) + '</p>')
    out = [CSS, jump, '<div id="eks">',
           '<div class="eks-bar"><div class="chips2" aria-label="Topik artikel">', chips, '</div></div>',
           '<div class="eks-top"><p>%d artikel dalam %d topik.</p><label class="eks-q"><input id="eks-q" type="search" '
           'placeholder="Cari judul artikel, misal kredit modal kerja" aria-label="Cari artikel"/></label></div>'
           % (total, len(used))]
    for tid, name, desc in used:
        cards = buckets[tid]
        out.append('<div class="topic" id="%s"><div class="topic-h"><h2>%s</h2><span class="n">%d artikel</span><p>%s</p></div>'
                   '<div class="cards2">%s</div>' % (tid, name, len(cards), desc, ''.join(cards[:SHOW])))
        if len(cards) > SHOW:
            out.append('<details class="eks-more"><summary>Lihat %d Artikel Lainnya</summary><div class="cards2">%s</div></details>'
                       % (len(cards) - SHOW, ''.join(cards[SHOW:])))
        out.append('</div>')
    out.append('<p class="eks-none">Belum ada artikel dengan kata itu. Coba kata lain.</p></div>' + JS)
    new_blk = ''.join(out)
    after = set(re.findall(r'href="([^"]+)"', new_blk))
    lost = {x for x in before if not x.startswith('#')} - after
    if lost:
        sys.exit('BATAL, link hilang: %s' % sorted(lost))
    new = h[:a + len(A)] + new_blk + h[b:]
    # anchor #berita tepat sebelum blok Berita Terkini (section-nya sendiri tidak disentuh, dipakai update_feed.py)
    if 'id="berita"' not in new:
        new = new.replace('<section aria-label="Berita Terkini" class="ca-feed"',
                          '<span id="berita" style="display:block;scroll-margin-top:72px"></span>'
                          '<section aria-label="Berita Terkini" class="ca-feed"', 1)
    changed = new != h
    if changed and not dry:
        open(P, 'w', encoding='utf-8').write(new)
    print('eksplor:', 'berubah' if changed else 'tidak berubah', '| kartu', total, '|',
          ', '.join('%s %d' % (t[0][2:], len(buckets[t[0]])) for t in used), '(dry run)' if dry else '')


if __name__ == '__main__':
    main('--dry' in sys.argv)
