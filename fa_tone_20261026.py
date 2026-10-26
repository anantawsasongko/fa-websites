# -*- coding: utf-8 -*-
"""Hapus klaim "ditangani langsung oleh Ananta W. Sasongko, CPA" (permintaan Bos 26 Okt 2026: terlalu sombong).
Diganti bahasa tim. Berlaku ke semua sumber (FA, apps, KJA, CariAkuntan, generator, spec konten). Idempoten."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {"out", "zips", ".git", "__pycache__", "netlify-redirect"}
A = r"Ananta W\. Sasongko, CPA"
RULES = [
 (rf"Ditangani langsung oleh {A}, bersama tim Chartered Accountant dan CPA", "Ditangani tim Chartered Accountant dan CPA"),
 (rf"Ditangani langsung oleh {A}, mantan Group CFO rumah sakit\.", "Ditangani tim yang berpengalaman di keuangan rumah sakit."),
 (r"Ditangani langsung oleh mantan Group CFO rumah sakit", "Ditangani tim yang berpengalaman di keuangan rumah sakit"),
 (rf"Ditangani langsung oleh {A}\.", "Dikerjakan bersama tim CA dan CPA FA Indonesia."),
 (rf"Ditangani langsung {A}\. Konsultasi gratis\.", "Tim CA dan CPA FA Indonesia. Konsultasi gratis."),
 (rf", dan setiap klien ditangani langsung oleh {A}\.", "."),
 (rf"(Setiap klien|Klien|Setiap mandat) ditangani langsung oleh (?:{A}|Ananta, CPA)(?:, [^.<\"]*)?\.", "Setiap klien didampingi tim FA Indonesia."),
 (rf"(Setiap klien|Klien|Setiap mandat) ditangani langsung oleh (?:{A}|Ananta, CPA)", "Setiap klien didampingi tim FA Indonesia"),
 (rf"Penugasan diawasi langsung oleh {A}, bersama Kantor Jasa Akuntan mitra", "Penugasan dikerjakan bersama Kantor Jasa Akuntan mitra"),
 (rf" dan diawasi langsung oleh {A}\.", "."),
 (r"dikerjakan langsung oleh Ananta, CPA dan Farhani, Ak\., CA", "dikerjakan tim akuntan FA Indonesia"),
 (r"agar setiap penugasan ditangani langsung oleh partner\.", "agar setiap penugasan mendapat perhatian penuh."),
 (r"agar setiap penugasan ditangani langsung", "agar setiap penugasan mendapat perhatian penuh"),
 (r"Dikerjakan langsung, bukan dioper ke tim lain\.", "Dikerjakan tim FA Indonesia bersama mitra profesional sesuai kebutuhan."),
 (r"Every client is handled personally by Ananta, CPA", "Every client works with our CA and CPA team"),
 (r"每位客户均由 Ananta, CPA 亲自负责", "每位客户均由我们的 CA 与 CPA 团队负责"),
 (r"确保每个项目均由合伙人亲自负责", "确保每个项目都得到充分关注"),
 (r"每项委托均由合伙人亲自负责", "每项委托都得到充分关注"),
 (r"(?:Ananta W\. )?Sasongko, CPA 将亲自回复", "我们将尽快回复"),
 (rf"menyebut bahwa klien ditangani langsung oleh {A}", "menyebut bahwa klien didampingi tim FA Indonesia (jangan pernah menulis ditangani langsung oleh Ananta)"),
]
RULES = [(re.compile(p), r) for p, r in RULES]
RULES += [(re.compile(a), b) for a, b in [
 (r" di Mandiri, BRI, BSI, BCA dan bank lain", " di bank BUMN, bank syariah, bank swasta, BPD, dan BPR"),
 (r" \(Bank Mandiri, BRI, BSI, BCA, OCBC, CIMB Niaga, BPD Jateng, BPD DIY, BPR\)", " (bank BUMN, bank syariah, bank swasta, BPD, dan BPR)"),
 (r" bersama Bank Mandiri, BRI, BSI, BCA, OCBC, CIMB Niaga, dan bank lainnya", " bersama bank BUMN, bank syariah, dan bank swasta"),
 (r" bersama Bank Mandiri, BRI, BSI, BCA, OCBC, CIMB Niaga, BPD, dan BPR", " bersama bank BUMN, bank syariah, bank swasta, BPD, dan BPR"),
 (r"mendekati Rp ?1 triliun", "lebih dari Rp1,1 triliun"),
 (r"±Rp1 triliun", "lebih dari Rp1,1 triliun"),
 (r"累计银行融资接近1万亿印尼盾", "累计银行融资超过1.1万亿印尼盾"),
 (r", bersama Bank Mandiri, BRI, BSI, BCA, OCBC, BPD Jateng, CIMB Niaga dan bank lainnya,", ", bersama bank BUMN, bank syariah, bank swasta, dan BPD,"),
 (r"Antara lain Bank Mandiri, BRI, BSI, BCA, OCBC, CIMB Niaga, BPD Jateng, BPD DIY, dan beberapa BPR\.", "Bank BUMN, bank syariah nasional, bank swasta nasional dan asing, BPD, serta beberapa BPR."),
 (r"(?i)close to (Rp|IDR) ?1 trillion", r"more than \1 1.1 trillion"),
]]
n_files = n_hits = 0
for root, dirs, files in os.walk(HERE):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        if not f.endswith((".html", ".py", ".json", ".txt", ".js", ".md", ".xml")) or f == "fa_tone_20261026.py": continue
        p = os.path.join(root, f)
        try: s = open(p, encoding="utf-8").read()
        except Exception: continue
        t = s; k = 0
        for rx, rep in RULES:
            t, c = rx.subn(rep, t); k += c
        if k: open(p, "w", encoding="utf-8").write(t); n_files += 1; n_hits += k
print("files", n_files, "replacements", n_hits)
