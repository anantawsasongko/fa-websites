# -*- coding: utf-8 -*-
"""13 Nov 2026 (Bos): "Jualan Fractional CFO di Bali, NTT, NTB untuk PT PMA ya, jadi halamannya yang bagus dengan foto dan
gelar lengkap saya." Foto dan gelar lengkap tampil di kartu profil (tempat yang memang dibolehkan aturan rendah hati);
tidak ada kalimat "ditangani langsung" dan sejenisnya.

Halaman (out/faindonesia, template live /en/pt-pma-audit-requirements-indonesia/, idempoten):
  EN: /en/fractional-cfo-bali/, /en/fractional-cfo-lombok-ntb/, /en/fractional-cfo-labuan-bajo-ntt/
  ID: /fractional-cfo-pt-pma-bali/, /fractional-cfo-pt-pma-ntb/, /fractional-cfo-pt-pma-ntt/  (pasangan hreflang)
Link masuk (blok berpenanda <!--fa-fcfo-->): /cfo-paruh-waktu/, /en/pt-pma-audit-requirements-indonesia/,
/audit-laporan-keuangan-pma/provinsi-{bali,nusa-tenggara-barat,nusa-tenggara-timur}/; baris di halaman daerah tiga provinsi
dipasang oleh fa_industri_lokal_20261113.py; sitemap <!--fcfo-->; llms.txt.
Tanpa janji harga atau hasil, tanpa angka pencapaian, tanpa em dash.
"""
import os, re, json, html, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faindonesia")
E = html.escape; D = "https://faindonesia.co.id"; TODAY = "2026-11-13"
NAME = "Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP"
def rd(p): return open(p, encoding="utf-8").read()
def P(u): return os.path.join(OUT, *[x for x in u.strip("/").split("/") if x], "index.html")
def wt(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and rd(p) == t: return 0
    open(p, "w", encoding="utf-8").write(t); return 1
def wa(t): return "https://wa.me/6282245260121?text=" + urllib.parse.quote(t, safe="")
def tbl(head, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

CSS = ('<style id="fcfo-css">.fcp{display:grid;grid-template-columns:260px 1fr;gap:28px;align-items:center;border:1px solid #333;'
       'border-radius:16px;background:#1b1b1b;padding:22px;margin:26px 0 30px}.fcp img{display:block;width:100%;aspect-ratio:4/5;'
       'object-fit:cover;object-position:50% 20%;border-radius:12px}.fcp small{display:block;font-size:11px;letter-spacing:.18em;'
       'text-transform:uppercase;opacity:.7;margin-bottom:8px}.fcp .nm{display:block;font-size:clamp(19px,2.2vw,24px);line-height:1.3;'
       'font-weight:600;margin:0 0 6px}.fcp .rl{display:block;opacity:.8;margin:0 0 14px}.fcp ul{margin:0 0 16px;padding-left:1.1em}'
       '.fcp li{margin:4px 0;line-height:1.5}.fcp .cbtns{margin:0!important}@media(max-width:720px){.fcp{grid-template-columns:1fr;'
       'gap:16px;padding:16px}.fcp img{max-width:240px}}</style>')

def profil(L):
    if L == "en":
        sm, rl = "Fractional CFO · FA Indonesia", "Fractional CFO and finance advisor for foreign-owned companies"
        li = ["Certified Public Accountant (CPA), Indonesian Institute of Certified Public Accountants (IAPI)",
              "FMVA and FPAP, Corporate Finance Institute",
              "Audit and assurance at Ernst &amp; Young (EY)",
              "Finance Director and Group CFO roles from Indonesia to Singapore: consolidation, acquisitions, bank financing, investor funding",
              "Prepared a private company for IPO on the Indonesia Stock Exchange; doctoral candidate in accounting"]
        b1, b2 = "Chat Ananta, CPA", "Full Profile"
    else:
        sm, rl = "Fractional CFO · FA Indonesia", "Fractional CFO dan penasihat keuangan untuk perusahaan PMA"
        li = ["Certified Public Accountant (CPA), Institut Akuntan Publik Indonesia (IAPI)",
              "FMVA dan FPAP, Corporate Finance Institute",
              "Audit dan assurance di Ernst &amp; Young (EY)",
              "Direktur Keuangan dan Group CFO dari Indonesia hingga Singapura: konsolidasi, akuisisi, pembiayaan bank, pendanaan investor",
              "Menyiapkan perusahaan swasta menuju IPO di Bursa Efek Indonesia; kandidat doktor akuntansi"]
        b1, b2 = "Chat Ananta, CPA", "Profil Lengkap"
    return (f'<div class="fcp"><img alt="{E(NAME)}" decoding="async" height="875" src="/img/ananta-w-sasongko-cpa-rs.jpg" width="700"/><div>'
            f'<small>{sm}</small><b class="nm">{E(NAME)}</b><span class="rl">{rl}</span><ul>' + "".join(f"<li>{x}</li>" for x in li) + "</ul>"
            '<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap">'
            f'<a class="btn solid" href="{{WA}}" rel="noopener" target="_blank">{b1}</a><a class="btn line" href="/ananta-w-sasongko/">{b2}</a></div></div></div>')

# ------------------------------------------------------------------ konten per wilayah
R = {
 "indonesia": dict(en="/en/fractional-cfo-indonesia/", id="/cfo-paruh-waktu/", prov=None, en_only=True,
   en_place="Indonesia", id_place="Indonesia",
   en_title="Fractional CFO in Indonesia for PT PMA | FA Indonesia",
   en_desc="Fractional CFO for foreign-owned companies (PT PMA) across Indonesia: monthly reporting, cash control, tax and LKPM oversight, audit readiness, and financing.",
   en_ctx="Foreign-owned companies in Indonesia usually reach the same point: the business has grown, the parent or investors want reliable reports in English, tax and LKPM deadlines keep coming, and a bank or auditor starts asking questions, yet a full-time CFO is not justified yet. Jakarta and Batam groups, Bali hospitality, and project companies in eastern Indonesia all face it.",
   ind=[("pma", "Trading, services, and holding PT PMA", ""), ("manufaktur", "Manufacturing", ""), ("hotel", "Hotels and resorts", ""),
        ("restoran-cafe", "Restaurants and cafes", ""), ("developer-properti", "Property", ""), ("pertambangan", "Mining services", "")]),
 "bali": dict(en="/en/fractional-cfo-bali/", id="/fractional-cfo-pt-pma-bali/", prov="provinsi-bali",
   en_place="Bali", id_place="Bali",
   en_title="Fractional CFO for PT PMA in Bali | FA Indonesia",
   en_desc="Fractional CFO for foreign-owned companies (PT PMA) in Bali: monthly reporting, cash control, tax and LKPM oversight, audit readiness, and bank financing.",
   id_title="Fractional CFO PT PMA di Bali: CFO Paruh Waktu | FA Indonesia",
   id_desc="Fractional CFO untuk PT PMA di Bali: laporan bulanan, kendali kas, pengawasan pajak dan LKPM, kesiapan audit, sampai pembiayaan bank. Diskusi awal via WA.",
   en_ctx="Most PT PMA in Bali run villas and resorts, restaurants and beach clubs, property projects, wellness, or creative businesses. Owners often live abroad, cash is collected at many outlets and through booking platforms, and the parent or investors want reports in English. That is where a part-time CFO pays off before a full-time hire makes sense.",
   id_ctx="Sebagian besar PT PMA di Bali mengelola vila dan resor, restoran dan beach club, proyek properti, wellness, atau usaha kreatif. Pemilik sering tinggal di luar negeri, kas masuk dari banyak outlet dan platform pemesanan, dan induk atau investor meminta laporan dalam bahasa Inggris. Di titik itulah CFO paruh waktu terasa manfaatnya sebelum merekrut CFO penuh waktu.",
   ind=[("hotel", "Hotels, villas, and resorts", "Hotel, vila, dan resor"), ("restoran-cafe", "Restaurants, cafes, and beach clubs", "Restoran, cafe, dan beach club"),
        ("developer-properti", "Property development and leasing", "Pengembangan dan sewa properti"), ("pma", "Trading, services, and holding PT PMA", "PT PMA dagang, jasa, dan holding")]),
 "ntb": dict(en="/en/fractional-cfo-lombok-ntb/", id="/fractional-cfo-pt-pma-ntb/", prov="provinsi-nusa-tenggara-barat",
   en_place="Lombok and NTB", id_place="NTB dan Lombok",
   en_title="Fractional CFO for PT PMA in Lombok and NTB | FA Indonesia",
   en_desc="Fractional CFO for PT PMA in Lombok, the Gili Islands, Mandalika, and Sumbawa: reporting, project budgets, tax and LKPM oversight, audit readiness, financing.",
   id_title="Fractional CFO PT PMA di NTB dan Lombok | FA Indonesia",
   id_desc="Fractional CFO untuk PT PMA di Lombok, Gili, Mandalika, dan Sumbawa: laporan bulanan, anggaran proyek, pengawasan pajak dan LKPM, kesiapan audit, pembiayaan.",
   en_ctx="Foreign investment in West Nusa Tenggara is concentrated in hospitality on Lombok and the Gili Islands, projects around the Mandalika special economic zone, and mining and its services on Sumbawa. Many are still in the build or ramp-up phase, so the finance questions are about project budgets, capital calls, and keeping the investment plan reported through LKPM consistent with the books.",
   id_ctx="Investasi asing di Nusa Tenggara Barat banyak berada di perhotelan Lombok dan Gili, proyek di sekitar KEK Mandalika, serta pertambangan dan jasa penunjangnya di Sumbawa. Banyak yang masih tahap pembangunan atau awal operasi, jadi pertanyaan keuangannya soal anggaran proyek, setoran modal, dan menjaga rencana investasi di LKPM tetap konsisten dengan pembukuan.",
   ind=[("hotel", "Hotels, villas, and dive resorts", "Hotel, vila, dan resor selam"), ("developer-properti", "Property and tourism projects", "Proyek properti dan pariwisata"),
        ("pertambangan", "Mining services and suppliers", "Jasa dan pemasok pertambangan"), ("restoran-cafe", "Restaurants and cafes", "Restoran dan cafe")]),
 "ntt": dict(en="/en/fractional-cfo-labuan-bajo-ntt/", id="/fractional-cfo-pt-pma-ntt/", prov="provinsi-nusa-tenggara-timur",
   en_place="Labuan Bajo and NTT", id_place="NTT dan Labuan Bajo",
   en_title="Fractional CFO for PT PMA in Labuan Bajo and NTT | FA Indonesia",
   en_desc="Fractional CFO for PT PMA in Labuan Bajo, Flores, Sumba, and Kupang: reporting, boat and resort cash control, tax and LKPM oversight, audit readiness.",
   id_title="Fractional CFO PT PMA di NTT dan Labuan Bajo | FA Indonesia",
   id_desc="Fractional CFO untuk PT PMA di Labuan Bajo, Flores, Sumba, dan Kupang: laporan bulanan, kendali kas kapal dan resor, pajak dan LKPM, kesiapan audit.",
   en_ctx="In East Nusa Tenggara, foreign-owned businesses cluster around Labuan Bajo and Komodo (resorts, liveaboard and phinisi boats, dive operators), resorts on Sumba, and trade and fisheries around Kupang. Revenue is seasonal and often paid in foreign currency through agents, while costs are local and in cash, so cash control and currency are usually the first things to fix.",
   id_ctx="Di Nusa Tenggara Timur, usaha milik asing banyak berada di sekitar Labuan Bajo dan Komodo (resor, kapal liveaboard dan phinisi, operator selam), resor di Sumba, serta perdagangan dan perikanan di sekitar Kupang. Pendapatannya musiman dan sering dibayar dalam valuta asing lewat agen, sementara biayanya lokal dan tunai, sehingga kendali kas dan kurs biasanya yang pertama dibenahi.",
   ind=[("hotel", "Resorts, liveaboards, and dive operators", "Resor, kapal liveaboard, dan operator selam"), ("restoran-cafe", "Restaurants and cafes", "Restoran dan cafe"),
        ("agribisnis", "Fisheries and agribusiness", "Perikanan dan agribisnis"), ("pma", "Trading and services PT PMA", "PT PMA dagang dan jasa")]),
}

def isi(k, L):
    r = R[k]; pl = r[L + "_place"]
    if L == "en":
        S = [("why", f"Why PT PMA in {pl} Use a Fractional CFO", f"<p>{r['en_ctx']}</p><p>A fractional CFO gives you senior finance leadership for a few days a month: someone who owns the numbers, answers to the board and the parent, and keeps the accountant, tax consultant, and auditor working to one plan.</p>"),
             ("what", "What the Fractional CFO Does", tbl(["Area", "What you get"], [
                 ["Monthly close and reporting", "Management accounts in English, in rupiah and, where needed, the parent's currency, with a short commentary"],
                 ["Cash and controls", "Daily cash and bank control across outlets, booking platforms, and agents; approval limits; petty cash"],
                 ["Budget and forecast", "Annual budget, 13-week cash flow, project or capex budget, and variance review"],
                 ["Tax and regulatory oversight", "Calendar and review of monthly and annual tax, withholding on payments abroad, and quarterly LKPM through OSS, working with your tax consultant"],
                 ["Shareholder funding", "Capital injections and shareholder loans documented and booked consistently with the deed, LKPM, and debt-to-equity limits"],
                 ["Audit readiness", "Closing files and schedules so the statutory audit runs on time"],
                 ["Banks and investors", "Financial model, information pack, and covenant reporting"]])),
             ("local", "Why a Local Fractional CFO", "<p>Many fractional CFO services in Indonesia are run from abroad and see the company from the group side. The work that decides whether a PT PMA runs smoothly happens on the Indonesian side: the public accounting firm (KAP) that signs the audit, the licensed valuer (KJPP) the bank accepts, the credit analyst at a local bank, the tax office, OSS and LKPM, and the notary for the deed.</p>"
                 "<p>Our team works on that side every day: Indonesian CPA, audit work under Indonesian Standards on Auditing, bank financing for multi-entity groups, and preparation of a private company for IPO on the Indonesia Stock Exchange. Reports still come to you in English.</p>"),
             ("pricing", "Pricing", tbl(["Package", "From", "What is included"], [
                 ["CFO Advisory", "USD 2,000 / month", "Fractional CFO for an agreed number of days per month: monthly reporting review, budget and cash, tax and LKPM oversight, reporting to owners and parent"],
                 ["Full Team", "USD 5,000 / month", "Everything in CFO Advisory, plus bookkeeping and financial statements (KJA Farhani K.N.), audit readiness and coordination with KAP DHN &amp; Rekan, valuation through a licensed KJPP, bank financing and refinancing, investor and financing pack, IPO readiness"]])
                 + "<p>Prices are indicative and confirmed in writing after the diagnostic, depending on the number of entities and the clean-up needed. Quoted in USD for reference; invoiced in rupiah, as Indonesian currency law requires for transactions in Indonesia. The statutory audit opinion and the KJPP valuation report are separate engagements signed directly with the licensed firms, so their independence is kept.</p>"),
             ("how", "How It Works", "<ol><li><b>First conversation</b> on WhatsApp or video call: your structure, owners, and the reports you need.</li>"
                 "<li><b>Diagnostic</b> of the books, cash, tax position, and LKPM, with a written list of priorities.</li>"
                 "<li><b>Monthly engagement</b>: an agreed number of days per month, remote work through a shared folder, and scheduled site visits.</li>"
                 "<li><b>Handover</b> when you are ready for a full-time finance manager or CFO, including help with the hiring.</li></ol>"),
             ("industries", f"Businesses We Support in {pl}", "<ul>" + "".join(
                 f'<li><a href="/audit-laporan-keuangan-{s}/' + (r["prov"] + "/" if r["prov"] else "") + f'">{e}</a></li>' for s, e, i in r["ind"]) + "</ul>"
                 "<p>Linked pages are in Indonesian and cover audit and financial statements for each industry" + (" in the province." if r["prov"] else ".") + "</p>"
                 + ("" if r["prov"] else '<p class="t"><b>Regional pages:</b> <a href="/en/fractional-cfo-bali/">Bali</a> · <a href="/en/fractional-cfo-lombok-ntb/">Lombok and NTB</a> · <a href="/en/fractional-cfo-labuan-bajo-ntt/">Labuan Bajo and NTT</a></p>')),
             ("team", "Who You Will Work With", tbl(["Role", "Who"], [
                 ["Fractional CFO", "Ananta W. Sasongko, CPA, FA Indonesia"],
                 ["Bookkeeping and financial statements", "KJA Farhani K.N., licensed accounting services firm"],
                 ["Statutory audit", "KAP DHN &amp; Rekan, public accounting firm licensed by the Minister of Finance and registered with OJK"]])
                 + "<p>The CFO role is part of management. The audit is always done by a separate firm.</p>")]
        F = [("What does a fractional CFO cost?", "CFO Advisory starts from USD 2,000 per month and the Full Team package, from bookkeeping to audit coordination, valuation, bank financing, and IPO readiness, from USD 5,000 per month. The final fee depends on the number of entities and the clean-up needed, and is confirmed in writing after the diagnostic. Invoices are in rupiah."),
             ("Do you need to be on site?", f"Most of the work runs remotely through a shared folder and regular calls. Site visits in {pl} are scheduled when they add value, for example at year-end, for a bank meeting, or for a stock count."),
             ("Will this replace our accountant or tax consultant?", "No. The fractional CFO directs and reviews their work and owns the reporting to the owners. If you have no accountant yet, bookkeeping can be done by KJA Farhani K.N."),
             ("Can you help with the statutory audit?", "Yes, by preparing the closing and the schedules. The audit itself and the opinion are by a separate licensed firm, such as KAP DHN &amp; Rekan."),
             ("Can reports be in English and in our parent's currency?", "Yes. Management reports are prepared in English, in rupiah and in the parent's currency where needed. Statutory books follow Indonesian rules unless the tax office has approved otherwise.")]
        rel = (('' if not r["prov"] else '<p class="t">All regions: <a href="/en/fractional-cfo-indonesia/">Fractional CFO in Indonesia</a></p>') + f'<p class="t">Related: <a href="/en/pt-pma-audit-requirements-indonesia/">PT PMA Audit Requirements in Indonesia</a> · '
               f'<a href="/en/statutory-audit-indonesia/">Statutory Audit in Indonesia</a> · <a href="{r["id"]}">Versi Bahasa Indonesia</a></p>')
    else:
        S = [("mengapa", f"Mengapa PT PMA di {pl} Memakai Fractional CFO", f"<p>{r['id_ctx']}</p><p>Fractional CFO memberi kepemimpinan keuangan senior beberapa hari dalam sebulan: ada yang memegang angka, melapor ke direksi dan induk, serta menjaga akuntan, konsultan pajak, dan auditor bekerja dalam satu rencana.</p>"),
             ("lingkup", "Yang Dikerjakan Fractional CFO", tbl(["Bidang", "Yang Anda Dapat"], [
                 ["Tutup buku dan laporan bulanan", "Laporan manajemen dalam bahasa Inggris dan Indonesia, dalam rupiah dan bila perlu mata uang induk, dengan ulasan singkat"],
                 ["Kas dan pengendalian", "Kendali kas dan bank harian di semua outlet, platform pemesanan, dan agen; batas persetujuan; kas kecil"],
                 ["Anggaran dan proyeksi", "Anggaran tahunan, arus kas 13 minggu, anggaran proyek atau belanja modal, dan analisis selisih"],
                 ["Pengawasan pajak dan regulasi", "Kalender dan reviu pajak bulanan dan tahunan, pemotongan atas pembayaran ke luar negeri, serta LKPM triwulanan di OSS, bersama konsultan pajak Anda"],
                 ["Pendanaan pemegang saham", "Setoran modal dan pinjaman pemegang saham didokumentasikan dan dicatat konsisten dengan akta, LKPM, dan batas rasio utang terhadap modal"],
                 ["Kesiapan audit", "Berkas tutup buku dan rincian akun supaya audit tahunan selesai tepat waktu"],
                 ["Bank dan investor", "Model keuangan, paket informasi, dan laporan covenant"]])),
             ("lokal", "Mengapa CFO Lokal", "<p>Banyak layanan fractional CFO di Indonesia dijalankan dari luar negeri dan melihat perusahaan dari sisi grup. Padahal yang menentukan lancar tidaknya PT PMA ada di sisi Indonesia: KAP yang menandatangani audit, KJPP yang diterima bank, analis kredit bank lokal, kantor pajak, OSS dan LKPM, serta notaris untuk akta.</p>"
                 "<p>Tim kami bekerja di sisi itu setiap hari: CPA Indonesia, audit berdasarkan Standar Audit IAPI, pembiayaan bank untuk grup multi-entitas, dan persiapan perusahaan swasta menuju IPO di Bursa Efek Indonesia. Laporan tetap tersedia dalam bahasa Inggris untuk induk dan investor.</p>"),
             ("biaya", "Biaya", tbl(["Paket", "Mulai dari", "Yang Termasuk"], [
                 ["CFO Advisory", "USD 2.000 per bulan", "Fractional CFO dengan jumlah hari per bulan yang disepakati: reviu laporan bulanan, anggaran dan kas, pengawasan pajak dan LKPM, pelaporan ke pemilik dan induk"],
                 ["Tim Lengkap", "USD 5.000 per bulan", "Semua di CFO Advisory, ditambah pembukuan dan laporan keuangan (KJA Farhani K.N.), kesiapan dan koordinasi audit dengan KAP DHN &amp; Rekan, penilaian lewat KJPP berizin, pembiayaan dan refinancing bank, paket investor dan pendanaan, kesiapan IPO"]])
                 + "<p>Harga bersifat indikatif dan dikonfirmasi tertulis setelah diagnostik, tergantung jumlah entitas dan pembenahan yang dibutuhkan. Ditulis dalam USD sebagai acuan; tagihan dalam rupiah sesuai UU Mata Uang. Opini audit dan laporan penilaian KJPP adalah perikatan terpisah yang ditandatangani langsung dengan kantornya, supaya independensinya terjaga.</p>"),
             ("alur", "Alur Kerja Sama", "<ol><li><b>Percakapan awal</b> lewat WhatsApp atau video call: struktur, pemilik, dan laporan yang dibutuhkan.</li>"
                 "<li><b>Diagnostik</b> pembukuan, kas, posisi pajak, dan LKPM, dengan daftar prioritas tertulis.</li>"
                 "<li><b>Perikatan bulanan</b>: jumlah hari per bulan yang disepakati, kerja jarak jauh lewat folder bersama, dan kunjungan terjadwal.</li>"
                 "<li><b>Serah terima</b> saat Anda siap merekrut manajer keuangan atau CFO penuh waktu, termasuk membantu rekrutmennya.</li></ol>"),
             ("industri", f"Usaha yang Kami Dampingi di {pl}", "<ul>" + "".join(
                 f'<li><a href="/audit-laporan-keuangan-{s}/{r["prov"]}/">{i}</a></li>' for s, e, i in r["ind"]) + "</ul>"),
             ("tim", "Tim Kami", tbl(["Peran", "Siapa"], [
                 ["Fractional CFO", "Ananta W. Sasongko, CPA, FA Indonesia"],
                 ["Pembukuan dan penyusunan laporan keuangan", "KJA Farhani K.N., Kantor Jasa Akuntansi berizin"],
                 ["Audit laporan keuangan", "KAP DHN &amp; Rekan, Kantor Akuntan Publik berizin Menteri Keuangan dan terdaftar OJK"]])
                 + "<p>Peran CFO adalah bagian dari manajemen. Audit selalu dilakukan kantor yang berbeda.</p>")]
        F = [("Berapa biaya fractional CFO?", "CFO Advisory mulai USD 2.000 per bulan dan paket Tim Lengkap, dari pembukuan sampai koordinasi audit, valuasi, pembiayaan bank, dan kesiapan IPO, mulai USD 5.000 per bulan. Biaya akhir tergantung jumlah entitas dan pembenahan yang dibutuhkan, dikonfirmasi tertulis setelah diagnostik. Tagihan dalam rupiah."),
             ("Apakah harus hadir di lokasi?", f"Sebagian besar pekerjaan berjalan jarak jauh lewat folder bersama dan rapat rutin. Kunjungan ke {pl} dijadwalkan saat memberi nilai, misalnya tutup buku akhir tahun, rapat dengan bank, atau stok opname."),
             ("Apakah menggantikan akuntan atau konsultan pajak kami?", "Tidak. Fractional CFO mengarahkan dan mereviu pekerjaan mereka serta memegang pelaporan ke pemilik. Bila belum punya akuntan, pembukuan bisa dikerjakan KJA Farhani K.N."),
             ("Bisa membantu audit tahunan?", "Bisa, dengan menyiapkan tutup buku dan rincian akun. Audit dan opininya dilakukan kantor akuntan publik yang terpisah, seperti KAP DHN &amp; Rekan."),
             ("Laporan bisa dalam bahasa Inggris dan mata uang induk?", "Bisa. Laporan manajemen disusun dalam bahasa Inggris, dalam rupiah dan mata uang induk bila perlu. Pembukuan resmi mengikuti aturan Indonesia kecuali sudah ada izin dari kantor pajak.")]
        rel = (f'<p class="t">Terkait: <a href="/cfo-paruh-waktu/">Fractional CFO dan CFO Paruh Waktu</a> · <a href="/audit-laporan-keuangan-pma/{r["prov"]}/">Audit Laporan Keuangan PT PMA di {E(pl.split(" dan ")[0])}</a> · '
               f'<a href="{r["en"]}">English Version</a></p>')
    return S, F, rel

T = rd(P("/en/pt-pma-audit-requirements-indonesia/"))
DHN_ID = ('<!--dhn--><div class="dhn2"><aside class="dhnc" aria-label="KAP DHN &amp; Rekan"><img src="/img/kap-dhn-mark.png" alt="Logo KAP DHN &amp; Rekan" width="46" height="54" loading="lazy"><div><small>Kantor Akuntan Publik</small><b class="n">KAP DHN &amp; Rekan</b><p>Izin Menteri Keuangan KMK No. 592/KM.1/2023, terdaftar OJK, anggota jaringan PA Global. Audit umum, audit untuk kredit bank dan laporan tahunan PT, reviu, dan prosedur yang disepakati untuk perusahaan di seluruh Indonesia.</p><div class="bt"><a class="dhnb" href="'
          + wa("Halo Pak Ananta, saya ingin tanya jasa audit di KAP DHN & Rekan.") + '" target="_blank" rel="noopener">Chat Ananta, CPA</a></div></div></aside><aside aria-label="KJA Farhani K.N." class="dhnc kja"><img alt="Logo KJA Farhani K.N." height="54" loading="lazy" src="/img/kja-farhani-mark.png" width="46"/><div><small>Kantor Jasa Akuntansi</small><b class="n">KJA Farhani K.N.</b><p>Izin Menteri Keuangan No. 232/KM.1PPPK/2020. Pembukuan dan penyusunan laporan keuangan sesuai SAK EMKM, SAK EP, atau PSAK, serta pajak, siap dipakai bank dan auditor, untuk perusahaan di seluruh Indonesia.</p><div class="bt"><a class="dhnb" href="'
          + wa("Halo Pak Ananta, saya ingin tanya jasa pembukuan, laporan keuangan, dan pajak di KJA Farhani K.N.") + '" rel="noopener" target="_blank">Chat Ananta, CPA</a></div></div></aside></div><!--/dhn-->')

n = 0; URLS = []
for k, r in R.items():
    for L in (("en",) if r.get("en_only") else ("en", "id")):
        url_path = r[L]; url = D + url_path; URLS.append(url_path)
        pl = r[L + "_place"]; S, F, rel = isi(k, L)
        h1 = f"Fractional CFO for PT PMA in {pl}" if L == "en" else f"Fractional CFO untuk PT PMA di {pl}"
        eb = f"Fractional CFO · Foreign Investment · {pl}" if L == "en" else f"Fractional CFO · PMA · {pl}"
        lead = (f"Senior finance leadership for foreign-owned companies in {pl}, a few days a month: reporting your owners can trust, cash under control, tax and LKPM on schedule, and books ready for the auditor and the bank."
                if L == "en" else f"Kepemimpinan keuangan senior untuk perusahaan PMA di {pl}, beberapa hari dalam sebulan: laporan yang dipercaya pemilik, kas terkendali, pajak dan LKPM tepat waktu, serta pembukuan siap untuk auditor dan bank.")
        wtxt = (f"Hello Pak Ananta, we are a PT PMA in {pl} and would like to discuss fractional CFO support. Business: ... Number of entities: ..."
                if L == "en" else f"Halo Pak Ananta, kami PT PMA di {pl} dan ingin diskusi soal fractional CFO. Usaha: ... Jumlah entitas: ...")
        W = wa(wtxt)
        meta = (f'<p class="meta">By <a href="/ananta-w-sasongko/">Ananta W. Sasongko, CPA</a> · Updated 13 November 2026</p>' if L == "en"
                else f'<p class="meta">Oleh <a href="/ananta-w-sasongko/">Ananta W. Sasongko, CPA</a> · Diperbarui 13 November 2026</p>')
        cont = "Contents" if L == "en" else "Peta Isi"
        faqh = ("faq", "Frequently Asked Questions" if L == "en" else "Pertanyaan Umum")
        nav = f'<nav aria-label="{cont}" class="pf-map" id="pfmap"><b>{cont}</b><ol>' + "".join(f'<li><a href="#{a}">{E(b)}</a></li>' for a, b, _ in S) + f'<li><a href="#faq">{faqh[1]}</a></li></ol></nav>'
        body = "".join(f'<h2 id="{a}">{E(b)}</h2>{c}' for a, b, c in S)
        faq = (f'<h2 id="faq">{faqh[1]}</h2><div class="faq-acc">' + "".join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{a}</p></details>' for q, a in F) + "</div>")
        btn = f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px"><a class="btn solid" href="{W}" rel="noopener" target="_blank">Chat Ananta, CPA</a></div>'
        main = (f'<main id="top"><!--fa-fcfo-page-->{CSS}\n<section class="block">\n<div class="wrap art">\n<p class="eyebrow">{E(eb)}</p>\n'
                f'<h1 style="margin:.2em 0 .5em;font-size:clamp(30px,4.2vw,50px);line-height:1.12">{E(h1)}</h1>\n{meta}\n'
                f'<p class="t" style="max-width:62em">{E(lead)}</p>\n' + profil(L).replace("{WA}", W) + nav + body + faq + rel + btn + "\n</div>\n</section>\n</main>")
        t = re.sub(r'<main id="top">.*?</main>', lambda m: main, T, count=1, flags=re.S)
        if L == "id":
            t = t.replace('<html lang="en">', '<html lang="id">', 1)
            t = re.sub(r"<!--dhn-->.*?<!--/dhn-->", lambda m: DHN_ID, t, count=1, flags=re.S)
        ti, de = r[L + "_title"], r[L + "_desc"]
        t = re.sub(r"<title>.*?</title>", f"<title>{E(ti)}</title>", t, count=1, flags=re.S)
        for prop in ("og:title",): t = re.sub(rf'<meta content="[^"]*" property="{prop}"/>', f'<meta content="{E(ti)}" property="{prop}"/>', t, count=1)
        t = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{E(de)}" name="description"/>', t, count=1)
        t = re.sub(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{E(de)}" property="og:description"/>', t, count=1)
        t = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{url}" property="og:url"/>', t, count=1)
        t = re.sub(r'<meta content="[^"]*" property="og:image"/>', f'<meta content="{D}/img/ananta-w-sasongko-cpa-rs.jpg" property="og:image"/>', t, count=1)
        t = t.replace('<meta content="1200" property="og:image:width"/><meta content="630" property="og:image:height"/>', '<meta content="700" property="og:image:width"/><meta content="875" property="og:image:height"/>', 1)
        t = re.sub(r'<meta content="[^"]*" property="og:locale"/>', f'<meta content="{"en_US" if L == "en" else "id_ID"}" property="og:locale"/>', t, count=1)
        t = re.sub(r'<link href="[^"]*" rel="canonical"/><link href="[^"]*" hreflang="en" rel="alternate"/><link href="[^"]*" hreflang="id" rel="alternate"/>',
                   f'<link href="{url}" rel="canonical"/><link href="{D}{r["en"]}" hreflang="en" rel="alternate"/><link href="{D}{r["id"]}" hreflang="id" rel="alternate"/>', t, count=1)
        g = {"@context": "https://schema.org", "@graph": [
            {"@type": "ProfessionalService", "name": h1, "description": de, "url": url, "areaServed": {"@type": "AdministrativeArea", "name": pl},
             "provider": {"@type": "Organization", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"},
             "employee": {"@type": "Person", "name": NAME, "jobTitle": "Fractional CFO", "image": D + "/img/ananta-w-sasongko-cpa-rs.jpg", "url": D + "/ananta-w-sasongko/"},
             "inLanguage": L},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in F]}]}
        t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + "</script>", t, count=1, flags=re.S)
        _old = rd(P(url_path)) if os.path.exists(P(url_path)) else ""
        _blk = re.search(r"<!--fa-fcfol-->.*?<!--/fa-fcfol-->", _old, re.S)   # blok kabupaten dari fa_fcfo_lokal dipertahankan
        if _blk and '<h2 id="faq">' in t: t = t.replace('<h2 id="faq">', _blk.group(0) + '<h2 id="faq">', 1)
        n += wt(P(url_path), t)

# ------------------------------------------------------------------ link masuk
def put(u, blk, anchors, after=False):
    p = P(u)
    if not os.path.exists(p): print("tidak ada", u); return 0
    t = rd(p); base = re.sub(r"<!--fa-fcfo-->.*?<!--/fa-fcfo-->", "", t, flags=re.S)
    for a in anchors:
        m = re.search(a, base)
        if m: return wt(p, base[:m.start()] + blk + base[m.start():])
    print("tanpa jangkar", u); return 0
def fl(items, lab): return f'<!--fa-fcfo--><p class="t"><b>{lab}</b> ' + " · ".join(f'<a href="{u}">{E(x)}</a>' for u, x in items) + "</p><!--/fa-fcfo-->"
nl = 0
_p = P("/cfo-paruh-waktu/"); _t = rd(_p); wt(_p, re.sub(r"<!--fa-fcfo-->.*?<!--/fa-fcfo-->", "", _t, flags=re.S))   # diganti blok penuh fa-cfopw
nl += put("/en/pt-pma-audit-requirements-indonesia/", fl([(R[k]["en"], R[k]["en_place"]) for k in R], "Fractional CFO for PT PMA:"), [r'<h2 id="sources">'])
for k in [x for x in R if R[x]["prov"]]:
    nl += put(f"/audit-laporan-keuangan-pma/{R[k]['prov']}/", fl([(R[k]["id"], f"Fractional CFO PT PMA di {R[k]['id_place']}"), (R[k]["en"], "English")], "Butuh pendampingan rutin?"),
              [r"<h2[^>]*>Pertanyaan Umum</h2>", r'<div class="faq-acc">'])

sm = os.path.join(OUT, "sitemap.xml"); x = rd(sm); x = re.sub(r"<!--fcfo-->.*?<!--/fcfo-->\n?", "", x, flags=re.S)
wt(sm, x.replace("</urlset>", "<!--fcfo-->" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in URLS) + "<!--/fcfo-->\n</urlset>"))
lp = os.path.join(OUT, "llms.txt"); l = rd(lp); l = re.sub(r"\n<!--fcfo-->.*?<!--/fcfo-->", "", l, flags=re.S)
wt(lp, l.rstrip("\n") + "\n<!--fcfo-->\n\n## Fractional CFO untuk PT PMA (13 Nov 2026)\n" + "".join(f"- [{R[k][L + '_title']}]({D}{R[k][L]})\n" for k in R for L in (("en",) if R[k].get("en_only") else ("en", "id"))) + "<!--/fcfo-->\n")
print("halaman", n, "link masuk", nl)
