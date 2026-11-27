#!/usr/bin/env python3
"""27 Nov 2026: nama tampil "Ananta W. Sasongko, CPA" jadi "Dr. (C) Ananta W. Sasongko, CPA".

Bos (melihat blok Tim Kami): "Saya juga Dr (C) lho ubah semua." Berlaku untuk nama yang TAMPIL:
kartu Tim Kami, kartu Tim Rumah Sakit, byline ("Oleh"/"By"), baris "Ditinjau" UpdateSAK, dan sel tabel. Tidak mengubah
tombol "Chat Ananta, CPA", atribut alt, maupun JSON-LD. Bekerja di out/ semua situs. Idempoten, --dry.
Jalankan PALING AKHIR (generator lama masih menulis nama tanpa Dr. (C)).
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
PAT = re.compile(r"(>|Ditinjau )Ananta W\. Sasongko(?=, CPA[<,]|</b><small>CPA)")
for site in sorted(os.listdir(os.path.join(ROOT, "out"))):
    n = k = 0
    for f in glob.glob(os.path.join(ROOT, "out", site, "**", "*.html"), recursive=True):
        s = open(f, encoding="utf-8", errors="ignore").read()
        s2, c = PAT.subn(r"\1Dr. (C) Ananta W. Sasongko", s)
        if c:
            n += 1; k += c
            if not DRY:
                open(f, "w", encoding="utf-8").write(s2)
    if n:
        print("%-20s file %5d, nama %5d%s" % (site, n, k, " (dry)" if DRY else ""))
