# -*- coding: utf-8 -*-
"""13 Nov 2026 (Bos): "https://www.smecfo.asia tiru semua untuk produk Fractional CFO kalau perlu bikin halaman dan anak anaknya
sendiri. Keunggulannya adalah dikerjakan oleh CFO yang sangat paham Indonesia dan punya kredensial jadi CFO di Singapura
sehingga paham ekspektasi Global."
Yang ditiru: ARSITEKTUR halaman (home, cara kerja, harga, health check, grup regional, repatriasi laba, fundraising, due
diligence, kepatuhan, interim, untuk CFO grup, tim, FAQ). TEKS TIDAK DISALIN; semua isi ditulis sendiri untuk konteks Indonesia.
Halaman bilingual EN + ID di /fractional-cfo/ (home menggantikan hub lokasi) dan /fractional-cfo/<topik>/.
Template dan perangkat: fa_content/fcfo_kit.py. Data lokasi: fa_content/fcfo_lokal_map.json (dari fa_fcfo_lokal_20261113.py).
Jalankan SETELAH fa_fcfo_lokal_20261113.py. Idempoten. Sitemap <!--fcfop-->, llms.txt.
Aturan: tanpa janji hasil, tanpa klaim terbaik, tanpa em dash, nama Ananta hanya di kartu profil, tim, dan tombol.
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "fa_content"))
from fcfo_kit import *  # noqa: F401,F403
from fcfo_kit import E, D, TODAY, NAME, rd, P, wt, wa, profil, PRICE, LOCAL, page, OUT

MAP = json.load(open(os.path.join(HERE, "fa_content", "fcfo_lokal_map.json")))
PROVN = {"51": "Bali", "52": "Nusa Tenggara Barat (Lombok, Sumbawa)", "53": "Nusa Tenggara Timur (Flores, Sumba, Timor)"}

def bi(en, idn, el="EN", il="ID"):
    return (f'<div class="fcl-bi"><div><small>{el}</small>{en}</div><div lang="id"><small>{il}</small>{idn}</div></div>')
def ul(xs): return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"
def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
def steps(xs):
    return '<div class="fcl-st">' + "".join(f"<div><i>{i + 1:02d}</i><b>{a}</b><span>{b}</span></div>" for i, (a, b) in enumerate(xs)) + "</div>"
def faqblock(F): return '<div class="faq-acc">' + "".join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in F) + "</div>"
def btn(W, extra=""): return f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px"><a class="btn solid" href="{W}" rel="noopener" target="_blank">Chat Ananta, CPA</a>{extra}</div>'
def h2(i, t): return f'<h2 id="{i}">{t}</h2>'

EDGE_EN = ("Indonesian ground truth, global expectations. Our CFO has run finance from Indonesia to Singapore, so he knows what a parent board, "
           "a regional investor, or an international auditor expects, and how to get there with Indonesian banks, KAP, KJPP, the tax office, and OSS.")
EDGE_ID = ("Paham lapangan Indonesia, paham ekspektasi global. CFO kami pernah memimpin keuangan dari Indonesia hingga Singapura, jadi tahu apa yang "
           "diharapkan direksi induk, investor regional, dan auditor internasional, serta cara mencapainya bersama bank, KAP, KJPP, kantor pajak, dan OSS di Indonesia.")

TEAM = ('<div class="fcl-tm"><a href="/ananta-w-sasongko/"><img alt="' + E(NAME) + '" loading="lazy" src="/img/ananta-w-sasongko-cpa-rs.jpg"/><div><b>' + E(NAME) + '</b>'
        '<span>Fractional CFO · FA Indonesia. CPA (IAPI), FMVA, FPAP; EY; Finance Director and Group CFO from Indonesia to Singapore</span></div></a>'
        '<a href="/kja-farhani/"><img alt="Farhani Kautsar Nugraha, S.E., M.S.A., Ak., CA" loading="lazy" src="/img/farhani-k-nugraha-fa-indonesia.jpg"/><div><b>Farhani Kautsar Nugraha, S.E., M.S.A., Ak., CA</b>'
        '<span>KJA Farhani K.N. · Bookkeeping and financial statements / pembukuan dan laporan keuangan</span></div></a>'
        '<a href="/kap-dhn/"><img alt="Dr. (C) Dwi Haryadi Nugraha, SST, MSi, Ak, CA, BKP, ASEAN CPA, CPA, CFI" loading="lazy" src="/img/dwi-haryadi-nugraha-kap-dhn-v2.jpg"/><div><b>Dr. (C) Dwi Haryadi Nugraha, SST, MSi, Ak, CA, BKP, ASEAN CPA, CPA, CFI</b>'
        '<span>KAP DHN &amp; Rekan · Statutory audit, registered with OJK / audit, terdaftar OJK</span></div></a></div>')

def loc_block():
    out = ""
    for p in ("51", "52", "53"):
        out += f"<h3>{E(PROVN[p])}</h3>" + '<div class="fcl-k">' + "".join(f'<a href="{u}">{E(l)}</a>' for u, l, c in MAP[p]) + "</div>"
    return out + ('<p class="t">Elsewhere in Indonesia (Jakarta, Batam, Surabaya, and other cities) we work remotely with scheduled visits / '
                  '<span lang="id">di kota lain di Indonesia kami bekerja jarak jauh dengan kunjungan terjadwal</span>: <a href="/en/fractional-cfo-indonesia/">Fractional CFO in Indonesia</a> · <a href="/cfo-paruh-waktu/">CFO Paruh Waktu</a></p>')

W0 = wa("Hello Pak Ananta, I would like to discuss fractional CFO support. Company: ... Location: ... Main issue: ...")
PAGES = []

# ---------------------------------------------------------------- HOME
body = (bi(f"<p>Senior finance leadership for foreign-owned companies (PT PMA), regional groups, and growing Indonesian businesses, for a few days a month. {E(EDGE_EN)}</p>",
           f"<p>Kepemimpinan keuangan senior untuk PT PMA, grup regional, dan usaha Indonesia yang tumbuh, beberapa hari dalam sebulan. {E(EDGE_ID)}</p>")
        + profil(W0)
        + h2("signs", "When Companies Call Us · Kapan Perusahaan Menghubungi Kami")
        + bi(ul(["Management accounts arrive weeks late, or not at all", "Profit on paper, but cash is always short", "Nobody can say which outlet, product, or customer makes money",
                 "A bank, investor, buyer, or auditor is about to look closely", "The parent asks for reports Indonesia cannot produce", "The CFO has left and hiring will take months"]),
             ul(["Laporan manajemen terlambat berminggu-minggu atau tidak ada", "Untung di atas kertas, kas selalu kurang", "Tidak ada yang tahu outlet, produk, atau pelanggan mana yang menghasilkan",
                 "Bank, investor, pembeli, atau auditor akan memeriksa", "Induk meminta laporan yang belum bisa disiapkan tim di Indonesia", "CFO keluar dan rekrutmen butuh berbulan-bulan"]))
        + h2("function", "Bookkeeping Is Not a Finance Function · Pembukuan Bukan Fungsi Keuangan")
        + tbl(["Bookkeeping / Pembukuan", "Finance function / Fungsi keuangan"], [
            ["Records what happened", "Explains why it happened and what to decide next"], ["Tax returns filed", "Tax planned, withholding on payments abroad controlled, LKPM consistent with the books"],
            ["Year-end figures", "Monthly management accounts, 13-week cash flow, budget versus actual"], ["Bank statements", "Bank relationships, covenants, financing, and refinancing"],
            ["Spreadsheets", "Controls, approval limits, audit trail, and systems that scale"]])
        + h2("scope", "What the CFO Covers · Lingkup Kerja CFO")
        + steps([("Reporting and close", "Monthly close in English and rupiah, parent reporting packs"), ("Cash and working capital", "Daily cash control, 13-week forecast, receivables and stock"),
                 ("Budget and scenarios", "Annual budget, project and capex budgets, what-if scenarios"), ("Margin and pricing", "Profit per outlet, product, project, or customer"),
                 ("Tax and compliance", "Tax calendar, withholding, transfer pricing files, LKPM"), ("Audit readiness", "Closing files and schedules for KAP DHN &amp; Rekan or your group auditor"),
                 ("Banks and investors", "Financial model, data room, bank and investor pack, valuation through KJPP"), ("Team and systems", "Hiring, training, Accurate, Jurnal, Xero, or Odoo setup")])
        + h2("steps", "How It Starts · Cara Memulai")
        + steps([("Conversation", "30 minutes on WhatsApp or video call. Free."), ("Health check", "A short review of books, cash, tax, and LKPM with a priority list."),
                 ("Monthly rhythm", "Agreed days per month, remote work, scheduled visits."), ("Handover", "When you are ready for a full-time finance manager or CFO.")])
        + f'<p class="t"><a href="/fractional-cfo/how-we-work/">How we work in detail</a> · <a href="/fractional-cfo/health-check/">Take the health check</a></p>'
        + h2("who", "Who We Work With · Siapa yang Kami Dampingi")
        + bi(ul(["<b>Owners</b> running a PT PMA from abroad", "<b>Regional groups</b> with an Indonesian subsidiary", "<b>Group CFOs</b> who need eyes and hands in Indonesia",
                 "<b>Indonesian companies</b> preparing for bank financing, investors, or IPO"]),
             ul(["<b>Pemilik</b> yang mengelola PT PMA dari luar negeri", "<b>Grup regional</b> dengan anak usaha di Indonesia", "<b>CFO grup</b> yang butuh perpanjangan tangan di Indonesia",
                 "<b>Perusahaan Indonesia</b> yang bersiap kredit bank, investor, atau IPO"]))
        + h2("where", "Where We Work · Wilayah")
        + bi("<p>Bali, West Nusa Tenggara, and East Nusa Tenggara by regency and district, plus remote support across Indonesia.</p>",
             "<p>Bali, NTB, dan NTT per kabupaten dan kecamatan, serta dukungan jarak jauh di seluruh Indonesia.</p>") + loc_block()
        + h2("pricing", "Pricing · Biaya") + PRICE + LOCAL + '<p class="t"><a href="/fractional-cfo/pricing/">Pricing details / rincian biaya</a></p>'
        + h2("team", "Team · Tim") + TEAM
        + h2("faq", "FAQ · Pertanyaan Umum"))
F_HOME = [("What is a fractional CFO?", "A senior finance leader who works for your company part-time, a set number of days per month, owning reporting, cash, budgeting, compliance, and the relationship with banks, auditors, and investors."),
          ("Apa itu fractional CFO?", "CFO senior yang bekerja paruh waktu untuk perusahaan Anda, beberapa hari per bulan, memegang laporan, kas, anggaran, kepatuhan, serta hubungan dengan bank, auditor, dan investor."),
          ("Why a CFO who knows Indonesia?", "Most problems of a PT PMA are solved on the Indonesian side: the tax office, OSS and LKPM, local banks, the KAP, and the KJPP. Our CFO works there every day and has also run finance in Singapore, so reports meet global expectations."),
          ("How much does it cost?", "CFO Advisory from USD 2,000 per month; Full Team from USD 5,000 per month, invoiced in rupiah.")]
PAGES.append(("/fractional-cfo/", "Fractional CFO Indonesia for PT PMA and SMEs | FA Indonesia",
              "Fractional CFO in Indonesia for PT PMA and SMEs: reporting, cash, tax and LKPM, audit, banks, IPO. A CFO with experience from Indonesia to Singapore.",
              "Fractional CFO in Indonesia · CFO Paruh Waktu", "Fractional CFO · Indonesia · Bilingual", body + faqblock(F_HOME) + btn(W0), F_HOME))

# ---------------------------------------------------------------- HOW WE WORK
body = (bi("<p>Four stages. You can stop after the first two with a clear picture of your finance function and no obligation.</p>",
           "<p>Empat tahap. Anda bisa berhenti setelah dua tahap pertama dengan gambaran fungsi keuangan yang jelas, tanpa kewajiban.</p>")
        + h2("s1", "1. First Conversation · Percakapan Awal")
        + bi("<p>30 minutes on WhatsApp or video call: your structure, shareholders, the reports you need, and what is not working. Free.</p>",
             "<p>30 menit lewat WhatsApp atau video call: struktur, pemegang saham, laporan yang dibutuhkan, dan apa yang belum berjalan. Gratis.</p>")
        + h2("s2", "2. Health Check · Pemeriksaan Awal")
        + bi(ul(["Trial balance and last year-end", "Bank reconciliations and cash", "Tax filings and withholding", "LKPM and OSS data", "Shareholder loans and capital", "Written priority list"]),
             ul(["Neraca saldo dan tutup buku terakhir", "Rekonsiliasi bank dan kas", "SPT dan pemotongan pajak", "Data LKPM dan OSS", "Pinjaman pemegang saham dan modal", "Daftar prioritas tertulis"]))
        + '<p class="t">Start with the <a href="/fractional-cfo/health-check/">10-question self-check</a>.</p>'
        + h2("s3", "3. Monthly Rhythm · Ritme Bulanan")
        + tbl(["When / Kapan", "What / Apa"], [["Week 1", "Close, reconciliations, management accounts in English and rupiah"], ["Week 2", "Review with owners or parent: results, cash, decisions"],
                                              ["Week 3", "Tax, withholding, LKPM in the quarter month, bank and covenant reporting"], ["Week 4", "Forecast update, projects: financing, audit, systems, hiring"]])
        + h2("s4", "4. Handover · Serah Terima")
        + bi("<p>When the company is ready, we help hire and train a full-time finance manager or CFO and hand over the files, controls, and calendar.</p>",
             "<p>Saat perusahaan siap, kami membantu merekrut dan melatih manajer keuangan atau CFO penuh waktu, lalu menyerahkan berkas, pengendalian, dan kalender kerja.</p>")
        + h2("tools", "How the Work Is Documented · Dokumentasi Kerja")
        + bi("<p>Work runs through a shared folder with a clear trail from source documents to reports, using tools FA built for itself: FA Jupiter for audit-ready statements, FA Saturn for audit-standard work papers, FA Venus for credit and valuation models.</p>",
             '<p>Pekerjaan berjalan lewat folder bersama dengan jejak dari dokumen sumber sampai laporan, memakai tools buatan FA: FA Jupiter, FA Saturn, dan FA Venus. Lihat <a href="/apps/">FA Apps</a>.</p>')
        + btn(W0, '<a class="btn line" href="/fractional-cfo/pricing/">Pricing</a>'))
PAGES.append(("/fractional-cfo/how-we-work/", "How Our Fractional CFO Works | FA Indonesia",
              "How a fractional CFO engagement runs in Indonesia: free first call, health check, monthly rhythm, and handover. Bilingual English and Indonesian.",
              "How We Work · Cara Kerja", "Fractional CFO · Process", body, []))

# ---------------------------------------------------------------- PRICING
body = (PRICE
        + h2("drivers", "What Drives the Fee · Yang Menentukan Biaya")
        + bi(ul(["Number of entities and consolidation", "State of the books at the start", "Reporting language and frequency for the parent", "Days per month on site", "Projects: financing, due diligence, IPO readiness"]),
             ul(["Jumlah entitas dan konsolidasi", "Kondisi pembukuan di awal", "Bahasa dan frekuensi laporan ke induk", "Hari kunjungan per bulan", "Proyek: pembiayaan, due diligence, kesiapan IPO"]))
        + h2("compare", "Compared With a Full-Time CFO · Dibanding CFO Penuh Waktu")
        + tbl(["", "Fractional CFO", "Full-time CFO"], [["Commitment", "Monthly, adjustable", "Employment contract, severance obligations"],
                                                        ["Time to start", "Days after the health check", "Typically months of search"], ["Team behind", "Bookkeeping, audit coordination, valuation network", "One person, team built over time"]])
        + h2("billing", "Billing · Penagihan")
        + bi("<p>Fees are quoted in USD for reference and invoiced in rupiah, as Indonesian currency law requires for transactions in Indonesia. The statutory audit (KAP) and valuation report (KJPP) are separate engagements signed directly with those licensed firms, which keeps their independence.</p>",
             "<p>Harga ditulis dalam USD sebagai acuan dan ditagih dalam rupiah sesuai UU Mata Uang. Audit (KAP) dan laporan penilaian (KJPP) adalah perikatan terpisah yang ditandatangani langsung dengan kantor berizin tersebut, supaya independensinya terjaga.</p>")
        + btn(W0, '<a class="btn line" href="/fractional-cfo/health-check/">Health Check</a>'))
PAGES.append(("/fractional-cfo/pricing/", "Fractional CFO Pricing in Indonesia | FA Indonesia",
              "Fractional CFO pricing in Indonesia: CFO Advisory from USD 2,000 per month, Full Team from USD 5,000 per month, invoiced in rupiah. What drives the fee.",
              "Fractional CFO Pricing · Biaya", "Fractional CFO · Pricing", body,
              [("How much is a fractional CFO in Indonesia?", "From USD 2,000 per month for CFO Advisory and from USD 5,000 per month for the Full Team package, invoiced in rupiah.")]))

# ---------------------------------------------------------------- HEALTH CHECK (interaktif)
Q = [("Management accounts are ready within 15 days of month-end", "Laporan manajemen siap paling lambat 15 hari setelah akhir bulan"),
     ("Every bank account is reconciled monthly", "Semua rekening bank direkonsiliasi tiap bulan"),
     ("You have a 13-week cash forecast", "Ada proyeksi kas 13 minggu"),
     ("You know the margin per outlet, product, or project", "Margin per outlet, produk, atau proyek diketahui"),
     ("Tax, withholding on payments abroad, and VAT are filed on time", "Pajak, pemotongan atas pembayaran ke luar negeri, dan PPN dilaporkan tepat waktu"),
     ("LKPM figures match the books", "Angka LKPM sesuai dengan pembukuan"),
     ("Shareholder loans and capital injections are documented and booked correctly", "Pinjaman pemegang saham dan setoran modal terdokumentasi dan tercatat benar"),
     ("Last year's statements were audited without major adjustments", "Laporan tahun lalu diaudit tanpa koreksi besar"),
     ("Payments need approval above a set limit", "Pembayaran di atas batas tertentu perlu persetujuan"),
     ("Someone besides the owner can explain the numbers to a bank", "Ada orang selain pemilik yang bisa menjelaskan angka ke bank")]
qhtml = "".join(f'<label class="hcq"><input type="checkbox" data-hc="1"/><span><b>{E(a)}</b><i lang="id">{E(b)}</i></span></label>' for a, b in Q)
HC = ('<style id="hc-css">.hcq{display:flex;gap:12px;align-items:flex-start;border:1px solid #333;border-radius:10px;padding:11px 13px;margin:8px 0;background:#1b1b1b;cursor:pointer}'
      '.hcq input{margin-top:4px;width:18px;height:18px;accent-color:#e9b949}.hcq b{display:block;font-weight:500}.hcq i{display:block;font-style:normal;font-size:13px;opacity:.7}'
      '.hcr{border:1px solid #e9b949;border-radius:12px;padding:16px;margin:16px 0}.hcr .sc{font-size:30px;font-weight:600}.hcbar{height:6px;background:#2b2b2b;border-radius:3px;overflow:hidden;margin:8px 0}'
      '.hcbar i{display:block;height:100%;width:0;background:#e9b949;transition:width .4s}</style>'
      f'<div id="hc">{qhtml}<div class="hcr" aria-live="polite"><div class="sc"><span id="hcs">0</span> / 10</div><div class="hcbar"><i id="hcb"></i></div>'
      '<p id="hct">Tick what is true today. / Centang yang sudah berjalan.</p><a class="btn solid" id="hcw" href="#" rel="noopener" target="_blank">Send my result on WhatsApp</a></div></div>'
      '<script>(function(){var c=document.querySelectorAll("[data-hc]"),s=document.getElementById("hcs"),b=document.getElementById("hcb"),t=document.getElementById("hct"),w=document.getElementById("hcw");'
      'function u(){var n=0;c.forEach(function(x){if(x.checked)n++});s.textContent=n;b.style.width=(n*10)+"%";'
      't.textContent=n>=8?"Solid basics. A fractional CFO adds forecasting, financing, and investor readiness. / Fondasi kuat.":n>=5?"Gaps that banks and auditors will notice. Worth a review. / Ada celah yang akan terlihat bank dan auditor.":"The finance function needs rebuilding before growth, financing, or audit. / Fungsi keuangan perlu dibenahi dulu.";'
      'w.href="https://wa.me/6282245260121?text="+encodeURIComponent("Hello Pak Ananta, my fractional CFO health check score is "+n+"/10. Company: ... Location: ...");'
      'if(window.gtag)gtag("event","fcfo_hc",{score:n});}c.forEach(function(x){x.addEventListener("change",u)});u();})();</script>')
body = (bi("<p>Ten questions, one minute. A low score is not a failure; it shows where a fractional CFO would start.</p>",
           "<p>Sepuluh pertanyaan, satu menit. Skor rendah bukan kegagalan; skor menunjukkan dari mana fractional CFO akan mulai.</p>")
        + HC + h2("next", "After the Check · Setelah Pemeriksaan")
        + bi("<p>Send your score on WhatsApp. The first conversation is free; if useful, we follow with a short review of your books, cash, tax, and LKPM and a written priority list.</p>",
             "<p>Kirim skor Anda lewat WhatsApp. Percakapan pertama gratis; bila bermanfaat, dilanjutkan reviu singkat pembukuan, kas, pajak, dan LKPM dengan daftar prioritas tertulis.</p>"))
PAGES.append(("/fractional-cfo/health-check/", "Finance Health Check for PT PMA and SMEs | FA Indonesia",
              "Free one-minute finance health check for PT PMA and SMEs in Indonesia: reporting, cash, tax, LKPM, audit, and controls. Send your score on WhatsApp.",
              "Finance Health Check · Cek Kesehatan Keuangan", "Fractional CFO · Health Check", body, []))

# ---------------------------------------------------------------- PT PMA & GROUPS
body = (bi(f"<p>An Indonesian subsidiary has to satisfy two masters: Indonesian rules and the group. {E(EDGE_EN)}</p>",
           f"<p>Anak usaha di Indonesia harus memenuhi dua pihak: aturan Indonesia dan grup. {E(EDGE_ID)}</p>")
        + h2("both", "Two Sets of Requirements · Dua Set Kewajiban")
        + tbl(["Indonesia", "The group / Grup"], [["Books in rupiah and Indonesian, statements under SAK", "Reporting pack in English, often under IFRS, in the group currency"],
                                                ["Monthly tax, withholding on payments abroad, annual corporate return", "Group tax provision and transfer pricing policy"],
                                                ["Quarterly LKPM through OSS", "Capital plan and investment tracking"], ["Statutory audit by an Indonesian KAP when required", "Group audit instructions and deadlines"]])
        + h2("issues", "Where It Usually Goes Wrong · Masalah yang Sering Terjadi")
        + bi(ul(["Intercompany balances that do not agree with the parent", "Management fees and royalties without documentation or withholding", "Shareholder loans above the debt-to-equity limit for interest deduction",
                 "Capital injections that differ between deed, LKPM, and bank", "Late group reporting because the local close is slow"]),
             ul(["Saldo antarperusahaan tidak cocok dengan induk", "Management fee dan royalti tanpa dokumen atau pemotongan pajak", "Pinjaman pemegang saham melebihi batas rasio utang terhadap modal",
                 "Setoran modal berbeda antara akta, LKPM, dan bank", "Laporan ke grup terlambat karena tutup buku lokal lambat"]))
        + h2("what", "What We Do · Yang Kami Kerjakan")
        + ul(["Monthly group reporting pack and PSAK to IFRS bridge", "Intercompany reconciliation and transfer pricing documentation (PMK 172/2023)", "Withholding and VAT on cross-border services",
              "LKPM and OSS data consistent with the books", "Audit coordination with the group auditor or KAP DHN &amp; Rekan"])
        + '<p class="t">See also <a href="/fractional-cfo/profit-repatriation/">profit repatriation</a>, <a href="/fractional-cfo/lkpm-compliance/">LKPM and compliance</a>, and <a href="/en/pt-pma-audit-requirements-indonesia/">PT PMA audit requirements</a>.</p>'
        + btn(W0))
PAGES.append(("/fractional-cfo/pt-pma-groups/", "Fractional CFO for PT PMA and Regional Groups | FA Indonesia",
              "Fractional CFO for PT PMA and regional groups: group reporting in English, PSAK to IFRS, intercompany, transfer pricing, withholding, LKPM, audit.",
              "PT PMA and Regional Groups · Grup Regional", "Fractional CFO · PT PMA", body, []))

# ---------------------------------------------------------------- REPATRIATION
body = (bi("<p>Getting profit out of Indonesia is legal and routine, but it needs the right order of steps. Most delays come from the balance sheet, not the bank.</p>",
           "<p>Membawa laba keluar dari Indonesia itu sah dan biasa, tetapi urutannya harus benar. Hambatan biasanya ada di neraca, bukan di bank.</p>")
        + h2("routes", "Common Routes · Jalur yang Umum")
        + tbl(["Route / Jalur", "Key points / Catatan"], [
            ["Dividends", "Only from positive retained earnings; a reserve must be set aside until it reaches 20% of issued and paid-up capital (Company Law Articles 70 and 71). Withholding tax 20% for non-residents, reduced under a tax treaty with valid treaty documentation."],
            ["Interest on shareholder loans", "Withholding tax on interest paid abroad; interest deduction limited by the debt-to-equity rule (generally 4:1)."],
            ["Management fees and royalties", "Need an agreement, evidence of the service, arm's length pricing, withholding tax, and self-assessed VAT on imported services."],
            ["Capital reduction", "Corporate approvals, creditor protection steps, and updates to the deed and OSS."]])
        + h2("order", "The Order That Works · Urutan yang Berjalan")
        + steps([("Clean balance sheet", "Retained earnings, reserve, and intercompany agreed"), ("Tax position", "Corporate tax settled, treaty documents ready"),
                 ("Approvals", "GMS resolution and board decision"), ("Payment", "Withholding paid and reported, transfer executed")])
        + bi("<p>This page is general information, not tax advice. Rates and documents depend on the treaty and the facts of your company.</p>",
             "<p>Halaman ini informasi umum, bukan nasihat pajak. Tarif dan dokumen tergantung perjanjian pajak dan fakta perusahaan Anda.</p>")
        + btn(W0))
PAGES.append(("/fractional-cfo/profit-repatriation/", "Profit Repatriation From Indonesia for PT PMA | FA Indonesia",
              "How a PT PMA repatriates profit from Indonesia: dividends, reserve rules, withholding tax and treaties, shareholder loan interest, management fees.",
              "Profit Repatriation · Repatriasi Laba", "Fractional CFO · PT PMA", body,
              [("Can a PT PMA pay dividends with accumulated losses?", "No. Dividends can only be paid from positive retained earnings, after setting aside the statutory reserve.")]))

# ---------------------------------------------------------------- FUNDRAISING
body = (bi("<p>Banks and investors fund numbers they can trust and a story that holds under questions. We prepare both, and we know how Indonesian credit analysts read a file.</p>",
           "<p>Bank dan investor mendanai angka yang bisa dipercaya dan cerita yang tahan pertanyaan. Kami menyiapkan keduanya, dan kami tahu cara analis kredit bank Indonesia membaca berkas.</p>")
        + h2("bank", "Bank Financing · Pembiayaan Bank")
        + ul(["Audited or reviewed statements, debt service coverage, and covenant headroom", "Collateral valuation by a KJPP the bank accepts", "Refinancing and restructuring of existing facilities"])
        + h2("investor", "Investors · Investor")
        + ul(["Financial model and business plan", "Data room and quality of earnings preparation", "Valuation support and negotiation preparation"])
        + h2("ipo", "IPO Readiness · Kesiapan IPO")
        + ul(["Audited history under SAK, governance organs, and internal audit", "Working with underwriters, KAP, legal counsel, and KJPP", 'Self-check: <a href="/cek-kelayakan-ipo/">IPO eligibility calculator</a>'])
        + btn(W0, '<a class="btn line" href="/cek-kapasitas-kredit/">Credit capacity check</a>'))
PAGES.append(("/fractional-cfo/fundraising/", "Fundraising, Bank Financing and IPO Readiness | FA Indonesia",
              "Fractional CFO support for bank financing, investors, and IPO readiness in Indonesia: models, data room, KJPP valuation, covenants, underwriter coordination.",
              "Fundraising and Financing · Pendanaan", "Fractional CFO · Funding", body, []))

# ---------------------------------------------------------------- DUE DILIGENCE
body = (bi("<p>Buying, selling, or investing in an Indonesian company? Due diligence finds what the statements do not show: cash quality, tax exposure, related parties, and licences.</p>",
           "<p>Membeli, menjual, atau berinvestasi di perusahaan Indonesia? Due diligence menemukan yang tidak terlihat di laporan: kualitas kas, risiko pajak, pihak berelasi, dan izin.</p>")
        + h2("scope", "Scope · Lingkup")
        + tbl(["Area", "What we look at / Yang diperiksa"], [["Earnings", "Normalised EBITDA, one-offs, revenue cut-off"], ["Cash and working capital", "Cash conversion, receivables ageing, stock"],
                                                          ["Tax", "Open years, withholding, VAT, transfer pricing"], ["Related parties", "Owner transactions, intercompany, guarantees"],
                                                          ["Licences and OSS", "Business licences, KBLI, LKPM history"]])
        + h2("sell", "Sell-Side Preparation · Persiapan Penjual")
        + bi("<p>For owners preparing a sale, vendor due diligence and a clean data room shorten the process and protect the price.</p>",
             "<p>Untuk pemilik yang akan menjual, vendor due diligence dan data room yang rapi mempercepat proses dan menjaga harga.</p>")
        + btn(W0))
PAGES.append(("/fractional-cfo/due-diligence/", "Financial Due Diligence in Indonesia | FA Indonesia",
              "Financial due diligence in Indonesia for buyers, sellers, and investors: earnings quality, cash, tax exposure, related parties, licences and LKPM history.",
              "Due Diligence", "Fractional CFO · Transactions", body, []))

# ---------------------------------------------------------------- LKPM & COMPLIANCE
body = (bi("<p>Foreign-owned companies carry a compliance calendar on top of normal tax. Missed filings rarely stop the business on day one, but they surface at the worst time: a licence change, a bank review, or a sale.</p>",
           "<p>Perusahaan PMA punya kalender kepatuhan di atas pajak biasa. Laporan yang terlewat jarang langsung menghentikan usaha, tetapi muncul di saat paling tidak tepat: perubahan izin, reviu bank, atau penjualan.</p>")
        + h2("calendar", "The Calendar · Kalender Kepatuhan")
        + tbl(["Item", "Frequency / Frekuensi", "Note / Catatan"], [
            ["LKPM (investment activity report, OSS)", "Quarterly", "Due by the 10th of the month after each quarter; must agree with the books and capital"],
            ["Monthly tax and withholding", "Monthly", "Including withholding on payments abroad and VAT on imported services"],
            ["Annual corporate tax return", "Annual", "With financial statements; audited statements when required"],
            ["Transfer pricing documentation", "Annual", "When thresholds under PMK 172/2023 are met"],
            ["Statutory audit", "Annual, when required", "Company Law Article 68 and lender or parent requirements"],
            ["Minimum investment and paid-up capital", "On setup and changes", "Rules set by the Investment Ministry/BKPM changed recently; check your position"]])
        + bi("<p>We keep the calendar, prepare or review each filing, and make sure the figures agree across OSS, tax, and the books.</p>",
             "<p>Kami memegang kalender, menyiapkan atau mereviu setiap laporan, dan memastikan angkanya konsisten antara OSS, pajak, dan pembukuan.</p>")
        + btn(W0))
PAGES.append(("/fractional-cfo/lkpm-compliance/", "LKPM and PT PMA Compliance Calendar | FA Indonesia",
              "PT PMA compliance in Indonesia: quarterly LKPM through OSS, monthly tax and withholding, transfer pricing, statutory audit, capital rules. Bilingual guide.",
              "LKPM and Compliance · Kepatuhan PT PMA", "Fractional CFO · Compliance", body, []))

# ---------------------------------------------------------------- INTERIM CFO
body = (bi("<p>When a CFO or finance manager leaves suddenly, the close, the bank, and the auditor do not wait. An interim CFO keeps the function running while you hire.</p>",
           "<p>Saat CFO atau manajer keuangan keluar mendadak, tutup buku, bank, dan auditor tidak menunggu. Interim CFO menjaga fungsi keuangan berjalan selama Anda merekrut.</p>")
        + h2("first", "The First 30 Days · 30 Hari Pertama")
        + steps([("Week 1", "Access, cash position, payment approvals"), ("Week 2", "Close the month, open issues list"), ("Week 3", "Banks, tax deadlines, auditor"), ("Week 4", "Plan, hiring profile, handover path")])
        + bi("<p>We can also run the search: job profile, interviews, technical test, and onboarding of the permanent hire.</p>",
             "<p>Kami juga bisa membantu rekrutmen: profil jabatan, wawancara, tes teknis, dan orientasi pejabat tetap.</p>")
        + btn(W0))
PAGES.append(("/fractional-cfo/interim-cfo/", "Interim CFO in Indonesia | FA Indonesia",
              "Interim CFO in Indonesia when your CFO or finance manager leaves: cash control, month-end close, banks, tax, auditor, and hiring the permanent replacement.",
              "Interim CFO", "Fractional CFO · Interim", body, []))

# ---------------------------------------------------------------- FOR GROUP CFOs
body = (bi(f"<p>You run finance for a group and Indonesia is the subsidiary that reports late and surprises you. You need someone senior on the ground who speaks your language and the local one. {E(EDGE_EN)}</p>",
           f"<p>Anda memimpin keuangan grup dan Indonesia adalah anak usaha yang laporannya terlambat dan sering mengejutkan. Anda butuh orang senior di lapangan yang paham bahasa grup dan bahasa lokal. {E(EDGE_ID)}</p>")
        + h2("you-get", "What You Get · Yang Anda Dapat")
        + ul(["Reporting pack on the group calendar, in English, reconciled to local books", "Early warning on tax, licence, and bank issues", "A senior counterpart for the local team, auditor, and banks",
              "Subsidiary review: controls, people, and systems, with a written report"])
        + btn(W0))
PAGES.append(("/fractional-cfo/for-cfos/", "For Group CFOs With an Indonesian Subsidiary | FA Indonesia",
              "For group CFOs with an Indonesian subsidiary: on-the-ground senior finance support, group reporting on time, subsidiary review, tax and bank early warning.",
              "For Group CFOs · Untuk CFO Grup", "Fractional CFO · Groups", body, []))

# ---------------------------------------------------------------- TEAM
body = (bi(f"<p>You get a team, not a single contractor: a fractional CFO, a licensed accounting services firm for the books, and a public accounting firm registered with OJK for the audit, which is always a separate engagement. {E(EDGE_EN)}</p>",
           f"<p>Anda mendapat tim, bukan satu orang: fractional CFO, kantor jasa akuntansi berizin untuk pembukuan, dan kantor akuntan publik terdaftar OJK untuk audit, yang selalu perikatan terpisah. {E(EDGE_ID)}</p>")
        + TEAM + profil(W0) + btn(W0))
PAGES.append(("/fractional-cfo/team/", "Fractional CFO Team: CFO, KJA, KAP | FA Indonesia",
              "The FA Indonesia fractional CFO team: a CFO with experience from Indonesia to Singapore, KJA Farhani K.N. for the books, and KAP DHN & Rekan for the audit.",
              "Team · Tim", "Fractional CFO · Team", body, []))

# ---------------------------------------------------------------- FAQ
F_ALL = F_HOME + [
    ("How is that different from an accountant?", "An accountant records and reports. A CFO uses the numbers to manage cash, margins, risk, and funding, and owns the relationship with banks, auditors, and investors."),
    ("How many days a month do companies need?", "Most start with two to four days a month, more during a financing, audit, or due diligence."),
    ("Do you replace our finance team?", "No. We lead and develop it. If there is no team yet, bookkeeping can be done by KJA Farhani K.N."),
    ("Do you work in English?", "Yes. Reports, meetings, and documents in English; books and filings in Indonesian as the law requires."),
    ("Where do you work?", "Bali, NTB, and NTT on site by regency and district; elsewhere in Indonesia remotely with scheduled visits."),
    ("Apakah bisa untuk perusahaan lokal, bukan PMA?", "Bisa. Untuk perusahaan lokal lihat juga halaman CFO Paruh Waktu."),
]
body = faqblock(F_ALL) + btn(W0)
PAGES.append(("/fractional-cfo/faq/", "Fractional CFO FAQ Indonesia | FA Indonesia",
              "Questions about fractional CFO services in Indonesia: what it is, cost, days per month, English reporting, audit independence, and locations.",
              "Fractional CFO FAQ · Pertanyaan Umum", "Fractional CFO · FAQ", body, F_ALL))

n = 0; URLS = []
for path, title, desc, h1t, eyebrow, body, F in PAGES:
    crumbs = [("/fractional-cfo/", "Fractional CFO")] + ([(path, h1t.split(" · ")[0])] if path != "/fractional-cfo/" else [])
    if len(title) > 65 or len(desc) > 158: print('PANJANG', len(title), len(desc), path)
    n += page(path, title, desc, h1t, eyebrow, body, W0, F, crumbs, cur=path)
    URLS.append(path)

sm = os.path.join(OUT, "sitemap.xml"); x = rd(sm); x = re.sub(r"<!--fcfop-->.*?<!--/fcfop-->\n?", "", x, flags=re.S)
wt(sm, x.replace("</urlset>", "<!--fcfop-->" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in URLS if u != "/fractional-cfo/") + "<!--/fcfop-->\n</urlset>"))
lp = os.path.join(OUT, "llms.txt"); l = rd(lp); l = re.sub(r"\n<!--fcfop-->.*?<!--/fcfop-->", "", l, flags=re.S)
wt(lp, l.rstrip("\n") + "\n<!--fcfop-->\n\n## Fractional CFO (produk, bilingual, 13 Nov 2026)\n" + "".join(f"- [{t}]({D}{u}): {d}\n" for u, t, d, *_ in PAGES) + "<!--/fcfop-->\n")
print("halaman", n)
