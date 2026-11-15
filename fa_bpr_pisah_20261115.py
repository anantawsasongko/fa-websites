#!/usr/bin/env python3
"""Pisahkan konsultan dan seller side BPR dari rumah sakit (15 Nov 2026).

Bos: "Konsultan dan seller side BPR dan RS harusnya dipisah. Konsultan BPR itu
tim Ananta dan Ko Dwi, berpengalaman audit dan konsultasi 70+ BPR dan 5+
seller side yang berhasil close."

Bekerja langsung di out/faindonesia (lihat PERINGATAN BUILD). Idempoten.
 - /bpr-dijual/: blok Tim Konsultan BPR (Ananta + Dwi) di bawah hero, bagian
   "Konsultan BPR dan BPRS", tombol hero RS dibuang, "medis" di due diligence
   diganti kepatuhan dan TI.
 - /rumah-sakit-dijual/: baris BPR dibuang dari tabel pipeline, judul dan Peta
   Isi tanpa BPR, tombol hero BPR dibuang (link teks ke /bpr-dijual/ tetap).
 - /layanan/: kelompok baru "BPR dan BPRS" (06 kelompok, grid 2 kolom rata),
   RS hanya "Jual Beli Rumah Sakit", rekam jejak RS dan BPR dipisah (ID/EN/ZH).
"""
import re, sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out" / "faindonesia"
WA = "https://wa.me/6282245260121?text="
DRY = "--dry" in sys.argv
changed = []


def sub1(t, old, new, label):
    if new in t:
        return t
    if old not in t:
        sys.exit(f"[GAGAL] tidak ketemu: {label}")
    if t.count(old) != 1:
        sys.exit(f"[GAGAL] tidak unik ({t.count(old)}x): {label}")
    return t.replace(old, new)


def save(p, t0, t):
    if t != t0:
        changed.append(str(p.relative_to(OUT)))
        if not DRY:
            p.write_text(t, encoding="utf-8")


# ---------- /bpr-dijual/ ----------
p = OUT / "bpr-dijual" / "index.html"
t0 = t = p.read_text(encoding="utf-8")

css = ('<style id="fa-rstim-css">.rstb{margin:22px 0 26px;max-width:560px}.rstb h2{margin:0 0 12px}'
       '.rst{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.rst>*{display:block;'
       'border:1px solid #333;border-radius:12px;overflow:hidden;background:#1e1e1e;color:inherit;'
       'text-decoration:none}.rst a:hover{border-color:#777}.rst img{display:block;width:100%;height:auto;'
       'aspect-ratio:4/5;object-fit:cover;background:#d9d9d9}.rst .t{padding:10px 12px 12px}.rst b{display:'
       'block;font-size:14px;line-height:1.3;font-weight:600}.rst small{display:block;font-size:11.5px;'
       'line-height:1.4;opacity:.72;margin-top:3px}.rstb .wa{display:flex;align-items:center;justify-content:'
       'center;gap:8px;margin-top:12px;padding:13px 16px;border-radius:10px;background:#25d366;color:#0b1f12;'
       'font-weight:600;font-size:15px;text-decoration:none}.rstb .wa:hover{filter:brightness(1.05)}'
       '@media(max-width:620px){.rst{gap:8px}.rst b{font-size:12.5px}.rst small{font-size:10.5px}'
       '.rst .t{padding:8px 9px 10px}}.rstb .ps{margin:0 0 14px;font-size:15px;line-height:1.6;opacity:.85}</style>')
if 'id="fa-rstim-css"' not in t:
    t = sub1(t, "</head>", css + "</head>", "head bpr")

tim = ('<!--fa-bprtim--><div style="margin:30px 0 8px"><div class="rstb"><h2>Tim Konsultan BPR</h2>'
       '<p class="ps">Berpengalaman dalam audit dan konsultasi lebih dari 70 BPR dan BPRS, serta mendampingi '
       '5+ transaksi seller side BPR sampai closing.</p><div class="rst">'
       '<a href="/ananta-w-sasongko/"><img alt="Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP" '
       'decoding="async" height="875" loading="lazy" src="/img/ananta-w-sasongko-cpa-rs.jpg" width="700"/>'
       '<div class="t"><b>Ananta W. Sasongko</b><small>CPA · Keuangan, Valuasi, Seller Side BPR</small></div></a>'
       '<a href="/kap-dhn/"><img alt="Dr. (C) Dwi Haryadi Nugraha, SST, MSi, Ak, CA, BKP, ASEAN CPA, CPA, CFI" '
       'decoding="async" height="1050" loading="lazy" src="/img/dwi-haryadi-nugraha-kap-dhn-v2.jpg" width="700"/>'
       '<div class="t"><b>Dwi Haryadi Nugraha</b><small>CA, CPA, CFI · Audit dan Konsultasi BPR</small></div></a>'
       '</div><a class="wa" href="' + WA + 'Halo%20Pak%20Ananta%2C%20saya%20ingin%20konsultasi%20untuk%20BPR%20atau%20BPRS." '
       'rel="noopener" target="_blank">Chat Tim BPR via WhatsApp</a></div></div><!--/fa-bprtim-->')
btn_rs = '<a class="btn line" href="/rumah-sakit-dijual/">Rumah Sakit Dijual</a></div>\n'
if "<!--fa-bprtim-->" not in t:
    t = sub1(t, btn_rs, "</div>\n" + tim + "\n", "hero bpr")

kons = ('<!--fa-bprkons--><h2 id="konsultan-bpr-dan-bprs">Konsultan BPR dan BPRS</h2>'
        '<p>Selain jual beli, tim yang sama mendampingi BPR dan BPRS dalam urusan keuangan sehari-hari sampai '
        'aksi korporasi.</p><ul>'
        '<li>Penyusunan laporan keuangan dan CKPN sesuai PSAK 109: <a href="/jasa-penyusunan-laporan-keuangan-bpr/">penyusunan laporan keuangan BPR</a>.</li>'
        '<li>Persiapan dan pelaksanaan audit untuk laporan tahunan OJK: <a href="/jasa-audit-laporan-keuangan-bpr/">audit BPR dan BPRS</a>.</li>'
        '<li>Pemenuhan modal inti: penambahan modal, masuknya pemegang saham baru, merger, atau konsolidasi antar-BPR.</li>'
        '<li>Valuasi saham, teaser, information memorandum, data room, sampai persetujuan OJK dan closing.</li>'
        '</ul><!--/fa-bprkons-->')
h_pipe = '<h2 id="pipeline-bpr-dan-bprs">'
if "<!--fa-bprkons-->" not in t:
    t = sub1(t, "</nav>" + h_pipe, "</nav>" + kons + h_pipe, "konsultan bpr")
    t = sub1(t, '<ol><li><a href="#pipeline-bpr-dan-bprs">',
             '<ol><li><a href="#konsultan-bpr-dan-bprs">Konsultan BPR dan BPRS</a></li><li><a href="#pipeline-bpr-dan-bprs">',
             "peta isi bpr")
t = t.replace("<b>Due Diligence</b>Keuangan, legal, pajak, dan medis lewat data room.",
              "<b>Due Diligence</b>Keuangan, legal, pajak, kepatuhan, dan TI lewat data room.")
t = sub1(t, "<p>Kami membantu valuasi, information memorandum, pencarian pembeli, dan koordinasi dengan KAP dan konsultan hukum untuk proses persetujuan OJK.</p>",
         "<p>Kami membantu valuasi, information memorandum, pencarian pembeli, dan koordinasi dengan KAP dan konsultan hukum untuk proses persetujuan OJK. Laporan keuangan dan CKPN dirapikan lebih dulu, supaya harga tidak tergerus temuan due diligence.</p>",
         "ingin menjual bpr")
save(p, t0, t)

# ---------- /rumah-sakit-dijual/ ----------
p = OUT / "rumah-sakit-dijual" / "index.html"
t0 = t = p.read_text(encoding="utf-8")
t = t.replace('<a class="btn line" href="/bpr-dijual/">BPR dan BPRS Dijual</a></div><!--fa-tim-atas-->', '</div><!--fa-tim-atas-->')
t = t.replace('<tr><td>BPR Konvensional</td><td data-l="Gambaran">2 BPR di Jawa Tengah dan DI Yogyakarta</td><td data-l="Indikasi Harga">Setelah NDA</td></tr>'
              '<tr><td>BPR Syariah (BPRS)</td><td data-l="Gambaran">1 BPRS dengan LOI akuisisi saham yang sudah berjalan</td><td data-l="Indikasi Harga">Setelah NDA</td></tr>', '')
t = t.replace('<p>Untuk BPR dan BPRS, lihat <a href="/bpr-dijual/">BPR dan BPRS dijual</a>.</p>',
              '<p>BPR dan BPRS ditangani tim tersendiri, lihat <a href="/bpr-dijual/">BPR dan BPRS dijual</a>.</p>')
for a, b in [('pipeline-lain-rs-bpr-dan-bprs">Pipeline Lain: RS, BPR, dan BPRS', 'pipeline-rumah-sakit-lain">Pipeline Rumah Sakit Lain'),
             ('punya-rs-klinik-atau-bpr-yang-ingin-dijual">Punya RS, Klinik, atau BPR yang Ingin Dijual?', 'punya-rs-atau-klinik-yang-ingin-dijual">Punya RS atau Klinik yang Ingin Dijual?')]:
    t = t.replace('href="#' + a, 'href="#' + b).replace('id="' + a, 'id="' + b)
if "BPR Konvensional" in t or "RS, BPR, dan BPRS" in t or "Klinik, atau BPR" in t:
    sys.exit("[GAGAL] sisa BPR di rumah-sakit-dijual")
save(p, t0, t)

# ---------- /layanan/ ----------
p = OUT / "layanan" / "index.html"
t0 = t = p.read_text(encoding="utf-8")
t = t.replace('<li><a href="/rumah-sakit-dijual/">Jual Beli Rumah Sakit dan BPR</a></li>',
              '<li><a href="/rumah-sakit-dijual/">Jual Beli Rumah Sakit</a></li><li><a href="/menjual-rumah-sakit/">Menjual Rumah Sakit</a></li>')
old5 = ('<article><span class="no">05</span><h3>Sektor Khusus</h3><p>Laporan dan audit dengan aturan tersendiri.</p><ul>'
        '<li><a href="/jasa-audit-laporan-keuangan-bpr/">Audit BPR dan BPRS</a></li>')
new5 = ('<article><span class="no">05</span><h3>BPR dan BPRS</h3><p>Tim tersendiri yang berpengalaman dalam audit dan konsultasi lebih dari 70 BPR, serta 5+ transaksi seller side BPR sampai closing.</p><ul>'
        '<li><a href="/jasa-penyusunan-laporan-keuangan-bpr/">Laporan Keuangan dan CKPN BPR</a></li>'
        '<li><a href="/jasa-audit-laporan-keuangan-bpr/">Audit BPR dan BPRS</a></li>'
        '<li><a href="/bpr-dijual/">Konsultan dan Jual Beli BPR</a></li></ul></article>'
        '<article><span class="no">06</span><h3>Sektor Khusus</h3><p>Laporan dan audit dengan aturan tersendiri.</p><ul>')
if "<h3>BPR dan BPRS</h3>" not in t:
    t = sub1(t, old5, new5, "layanan grup bpr")
t = t.replace("<p>Keuangan, unit cost, tarif, pendanaan, serta jual beli rumah sakit dan klinik.</p>",
              "<p>Bersama tim rumah sakit: keuangan, unit cost, tarif, pendanaan, serta jual beli rumah sakit dan klinik.</p>")
# rekam jejak
old_li = ('<li><span class="yr" data-i18n="k109">2025-Kini</span><div><b data-i18n="k110">Mandat Sell-Side: 10+ Rumah Sakit dan 3 BPR</b>'
          '<span data-i18n="k111">Divestasi rumah sakit swasta serta BPR dan BPRS di Jawa Barat, Jawa Tengah, dan DIY. Valuasi, information memorandum, NDA, dan virtual data room. Proses penjajakan calon pembeli sedang berjalan.</span></div></li>')
new_li = ('<li><span class="yr" data-i18n="k109">2025-Kini</span><div><b data-i18n="k110">Mandat Sell-Side: 10+ Rumah Sakit</b>'
          '<span data-i18n="k111">Divestasi rumah sakit swasta di Jawa Barat, Jawa Tengah, dan DIY. Valuasi, information memorandum, NDA, dan virtual data room. Proses penjajakan calon pembeli sedang berjalan.</span></div></li>'
          '<li><span class="yr" data-i18n="kbpr0">Tim BPR</span><div><b data-i18n="kbpr1">BPR dan BPRS: 70+ Audit dan Konsultasi, 5+ Seller Side Closing</b>'
          '<span data-i18n="kbpr2">Audit dan konsultasi untuk lebih dari 70 BPR konvensional dan syariah, serta 5+ transaksi seller side BPR yang sudah closing. Tiga mandat BPR dan BPRS sedang berjalan.</span></div></li>')
if 'data-i18n="kbpr1"' not in t:
    t = sub1(t, old_li, new_li, "rekam jejak")
EN = ('"k110": "Sell-side mandates: 10+ hospitals and 3 rural banks", "k111": "Divestment of private hospitals and conventional and sharia rural banks (BPR/BPRS) in West Java, Central Java, and Yogyakarta. Valuation, information memorandum, NDA, and virtual data room. Buyer outreach is in progress."',
      '"k110": "Sell-side mandates: 10+ hospitals", "k111": "Divestment of private hospitals in West Java, Central Java, and Yogyakarta. Valuation, information memorandum, NDA, and virtual data room. Buyer outreach is in progress.", '
      '"kbpr0": "BPR Team", "kbpr1": "Rural banks (BPR/BPRS): 70+ audit and advisory engagements, 5+ sell-side deals closed", '
      '"kbpr2": "Audit and advisory for more than 70 conventional and sharia rural banks, and 5+ BPR sell-side transactions taken through to closing. Three BPR and BPRS mandates are in progress."')
ZH = ('"k110": "卖方委托：10余家医院及3家农村银行", "k111": "出售位于西爪哇、中爪哇及日惹的私立医院和农村银行（含伊斯兰农村银行）。估值、信息备忘录、保密协议及虚拟数据室。买方接洽正在进行中。"',
      '"k110": "卖方委托：10余家医院", "k111": "出售位于西爪哇、中爪哇及日惹的私立医院。估值、信息备忘录、保密协议及虚拟数据室。买方接洽正在进行中。", '
      '"kbpr0": "农村银行团队", "kbpr1": "农村银行（BPR/BPRS）：70余家审计与咨询，5宗以上卖方交易完成交割", '
      '"kbpr2": "为70余家传统及伊斯兰农村银行提供审计与咨询，并完成5宗以上农村银行卖方交易交割。另有3项BPR及BPRS委托正在进行中。"')
for old, new in (EN, ZH):
    if '"kbpr1"' not in t or old in t:
        t = t.replace(old, new)
if t.count('"kbpr1": ') != 2:
    sys.exit("[GAGAL] i18n kbpr tidak lengkap")
save(p, t0, t)

print(("DRY " if DRY else "") + f"berubah {len(changed)} file:", *changed, sep="\n  ")
