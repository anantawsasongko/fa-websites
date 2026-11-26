#!/usr/bin/env python3
"""26 Nov 2026 (4): penyapu harga dan kata "mitra" (keputusan Bos 26 Nov: "Ya" untuk dua-duanya).

1. Stat "KAP Mitra" di halaman audit daerah + pendampingan audit jadi "KAP OJK" (tanpa kata mitra).
2. Harga dibuang dari /jasa-penyusunan-laporan-keuangan/, /laporan-keuangan-umkm/ (termasuk title dan H1),
   /kja-farhani/, /konsultan-kredit-bank/ (retainer + success fee), 2 artikel, kotak fa-pb di semua
   halaman, dan JSON-LD (offers.price, priceRange). "Kantor Jasa Akuntan mitra" jadi "KJA Farhani K.N.".
Aturan 21 Nov: situs FA tanpa harga; biaya lewat penawaran tertulis. JALANKAN PALING AKHIR (generator
lama masih menulis harga). Idempoten, --dry.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(ROOT, "out", "faindonesia")
DRY = "--dry" in sys.argv
changed = []
TAWAR = "disampaikan dalam penawaran tertulis setelah diskusi awal"


def write(path, new, old):
    if new != old:
        changed.append(os.path.relpath(path, ROOT))
        if not DRY:
            open(path, "w").write(new)


# ---- umum, semua halaman FA
GLOBAL = [
    ("<b>KAP Mitra</b><span>Audit lebih lancar lewat KAP mitra terdaftar OJK, karena data sudah siap sebelum auditor datang</span>",
     "<b>KAP OJK</b><span>Audit oleh KAP terdaftar OJK berjalan lebih lancar, karena data sudah siap sebelum auditor datang</span>"),
    (" UMKM mulai Rp900 ribu, PT dan CV mulai Rp2 juta per bulan.", ""),
    (" Paket jasa pembukuan UMKM mulai Rp900 ribu per bulan, PT dan CV mulai Rp2 juta per bulan; perapian beberapa tahun dihitung setelah melihat data.", ""),
    ("Paket jasa pembukuan UMKM mulai Rp900 ribu per bulan, PT dan CV mulai Rp2 juta per bulan; perapian beberapa tahun dihitung setelah melihat data.",
     "Biaya mengikuti volume transaksi dan kondisi pembukuan, dan disampaikan dalam penawaran tertulis setelah diskusi awal."),
    ("Pembukuan UMKM mulai Rp900 ribu per bulan, PT dan CV mulai Rp2 juta per bulan. ", "Biaya pembukuan mengikuti volume transaksi dan disampaikan dalam penawaran tertulis. "),
    ("oleh KJA mulai Rp900 ribu per bulan.", "oleh KJA."),
    ("Jasa Pembuatan Laporan Keuangan Bulanan Terima Beres, Mulai Rp900 Ribu", "Jasa Pembuatan Laporan Keuangan Bulanan Terima Beres"),
    (" UMKM mulai Rp900 ribu, PT/CV mulai Rp2 juta.", ""),
    ('<th>Untuk</th><th>Mulai</th>', '<th>Untuk</th>'),
    ('<td data-l="Mulai">Rp900 ribu per bulan</td>', ""), ('<td data-l="Mulai">Rp2 juta per bulan</td>', ""), ('<td data-l="Mulai">Rp3 juta</td>', ""),
    ('href="https://cariakuntan.com/jasa-pembukuan/">Lihat Paket dan Harga</a>', 'href="https://cariakuntan.com/jasa-pembukuan/">Lihat Paket</a>'),
]
# ---- per halaman (urutan penting: kalimat panjang dulu)
B_LK = f"Biaya mengikuti volume transaksi dan kondisi pembukuan, dan {TAWAR}."
PAGE = {
    "jasa-penyusunan-laporan-keuangan": [
        ("Retainer mulai Rp2,5 juta per bulan, kontrak minimal 1 tahun untuk laporan keuangan bulanan.", B_LK),
        ("Mulai Rp2,5 juta per bulan untuk laporan keuangan bulanan dengan kontrak minimal 1 tahun.", B_LK),
        (", mulai Rp2,5 juta per bulan.", "."),
        (" Mulai Rp2,5 juta per bulan.", ""),
        ("Dikerjakan bersama Kantor Jasa Akuntan mitra.", "Dikerjakan bersama KJA Farhani K.N."),
    ],
    "laporan-keuangan-umkm": [
        ("Jasa Laporan Keuangan UMKM Biaya Terjangkau, Mulai Rp2,5 Juta", "Jasa Laporan Keuangan UMKM Terima Beres untuk KUR dan Bank"),
        ("Jasa Laporan Keuangan UMKM dengan Biaya Terjangkau", "Jasa Laporan Keuangan UMKM Terima Beres untuk KUR dan Bank"),
        ("Jasa pembuatan laporan keuangan UMKM dengan biaya terjangkau, mulai Rp2,5 juta per bulan.",
         "Jasa pembuatan laporan keuangan UMKM terima beres: data seadanya dirapikan tim FA Indonesia."),
        ("FA Indonesia bersama Kantor Jasa Akuntan mitra yang dipimpin Farhani Kautsar Nugraha, CA menyusun laporan keuangan UMKM mulai Rp2,5 juta per bulan.",
         "FA Indonesia bersama KJA Farhani K.N. menyusun laporan keuangan UMKM dari data seadanya."),
        ("menyusun laporan keuangan UMKM mulai Rp2,5 juta per bulan bersama Kantor Jasa Akuntan mitra, diawasi CPA,",
         "menyusun laporan keuangan UMKM bersama KJA Farhani K.N., diawasi CPA,"),
        ("Disusun dengan FA Jupiter, mulai Rp2,5 juta per bulan.", "Disusun dengan FA Jupiter."),
        ("Mulai Rp2,5 juta per bulan untuk laporan keuangan bulanan dengan kontrak minimal 1 tahun.", B_LK),
        ("Laporan keuangan yang rapi tidak harus mahal. ", ""),
    ],
    "kja-farhani": [
        ("Retainer penyusunan laporan keuangan mulai Rp2,5 juta per bulan dengan kontrak minimal satu tahun; untuk usaha kecil tersedia paket putus sampai laporan terbit.",
         f"Untuk usaha kecil tersedia paket putus sampai laporan terbit. Angkanya {TAWAR}."),
        ('<div class="tblwrap"><table class="twr-s"><tr class="twr-h"><th>Paket</th><th>Mulai</th></tr><tr><td>Pembukuan UMKM dan perorangan</td><td data-l="Mulai">Rp900 ribu/bulan</td></tr><tr><td>Pembukuan PT dan CV</td><td data-l="Mulai">Rp2 juta/bulan</td></tr><tr><td>Laporan tahunan PT (SABH)</td><td data-l="Mulai">Rp3 juta, belum termasuk notaris</td></tr><tr><td>SPT Tahunan Badan</td><td data-l="Mulai">Rp3 juta</td></tr></table></div>',
         "<ul><li>Pembukuan UMKM dan perorangan</li><li>Pembukuan PT dan CV</li><li>Laporan tahunan PT (SABH)</li><li>SPT Tahunan Badan</li></ul>"
         f"<p>Biaya tiap paket mengikuti volume transaksi dan {TAWAR}.</p>"),
    ],
    "konsultan-kredit-bank": [
        ("Retainer mulai Rp2,5 juta per bulan ditambah success fee 1-3% dari nilai kredit yang dicairkan.",
         f"Biaya mengikuti lingkup pekerjaan dan besar fasilitas, dan {TAWAR}."),
        ("Retainer mulai Rp2,5 juta per bulan ditambah success fee 1-3% dari kredit yang cair.",
         f"Biaya mengikuti lingkup pekerjaan dan besar fasilitas, dan {TAWAR}."),
    ],
    "artikel/contoh-laporan-keuangan-umkm": [
        ("FA Indonesia menyusun laporan keuangan UMKM mulai Rp2,5 juta per bulan, diawasi CPA.",
         "FA Indonesia menyusun laporan keuangan UMKM, diawasi CPA."),
    ],
    "artikel/biaya-jasa-penyusunan-laporan-keuangan": [
        ("Di FA Indonesia mulai Rp2,5 juta per bulan untuk laporan bulanan dengan kontrak minimal 1 tahun.",
         f"Di FA Indonesia biayanya {TAWAR}."),
        ("Penyusunan laporan keuangan bulanan dimulai dari Rp2,5 juta per bulan dengan kontrak minimal satu tahun.",
         f"Biaya penyusunan laporan keuangan bulanan mengikuti volume transaksi dan kondisi pembukuan, dan {TAWAR}."),
        ("Kisaran Biaya di FA Indonesia", "Biaya di FA Indonesia"),
    ],
}


def ld_clean(s):
    def fix(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        hit = [False]

        def walk(o):
            if isinstance(o, dict):
                if "priceRange" in o:
                    del o["priceRange"]; hit[0] = True
                off = o.get("offers")
                if isinstance(off, dict) and ("price" in off or "Rp" in json.dumps(off, ensure_ascii=False)):
                    del o["offers"]; hit[0] = True
                for v in list(o.values()):
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(d)
        return ('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>") if hit[0] else m.group(0)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)


for f in glob.glob(os.path.join(FA, "**", "index.html"), recursive=True):
    old = open(f).read()
    if "Mitra</b>" not in old and "Rp900" not in old and "Paket dan Harga" not in old:
        continue
    s = old
    for a, b in GLOBAL:
        s = s.replace(a, b)
    write(f, s, old)
for slug, reps in PAGE.items():
    f = os.path.join(FA, slug, "index.html")
    old = open(f).read()
    s = old
    for a, b in reps:
        s = s.replace(a, b)
    s = s.replace("Kantor Jasa Akuntan mitra yang dipimpin Farhani Kautsar Nugraha, CA", "KJA Farhani K.N.")
    s = s.replace("Kantor Jasa Akuntan mitra", "KJA Farhani K.N.")
    s = re.sub(r"Penyusunan laporan keuangan bulanan dimulai dari\s*(?:<[^>]+>\s*)*Rp2,5 juta per bulan\s*(?:</[^>]+>\s*)*dengan kontrak minimal satu tahun\.",
               f"Biaya penyusunan laporan keuangan bulanan mengikuti volume transaksi dan kondisi pembukuan, dan {TAWAR}.", s)
    s = ld_clean(s)
    write(f, s, old)
print(("DRY " if DRY else "") + f"{len(set(changed))} file berubah")
