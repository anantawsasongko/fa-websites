# -*- coding: utf-8 -*-
"""12 Nov 2026 sore. Bos: untuk pencarian audit PT PMA, FA masih kalah dari panduan panjang berbahasa Inggris milik pesaing.
Halaman EN FA yang ada (/en/statutory-audit-indonesia/) hanya ±430 kata dan sebagian masih berbahasa Indonesia.
BEKERJA LANGSUNG DI out/faindonesia. Idempoten. Jalankan setelah fa_industri_20261112.py.
1. Panduan panjang EN: /en/pt-pma-audit-requirements-indonesia/ (seluruhnya bahasa Inggris, termasuk blok tim).
2. Link berpenanda <!--fa-enpma--> dari /en/statutory-audit-indonesia/, /en/accountant-indonesia/, /audit-laporan-keuangan-pma/,
   /laporan-keuangan-pma/, /artikel/audit-laporan-keuangan-pt-pma-persiapan/; sitemap <!--enpma-->; llms.
Dasar hukum yang dipakai: UU 40/2007 Pasal 66 dan 68; PP 24/1998 jo. PP 64/1999 (Permendag 25/2020 sudah dicabut Permendag 26/2025,
jadi TIDAK dirujuk sebagai dasar); UU 5/2011 Akuntan Publik. Tanpa angka tarif, tanpa janji waktu atau opini."""
import os, re, json, html, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faindonesia")
D = "https://faindonesia.co.id"; TODAY = "2026-11-12"
E = html.escape
N = [0]
def rd(p): return open(p, encoding="utf-8").read()
def P(path): return os.path.join(OUT, *[x for x in path.strip("/").split("/") if x], "index.html")
def wt(p, t):
    if os.path.exists(p) and rd(p) == t: return
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(t); N[0] += 1
WA = "https://wa.me/6282245260121?text=" + urllib.parse.quote("Hello Pak Ananta, we are a PT PMA and would like to discuss our audit. Financial year: ... Purpose of the audit: ...", safe="")
PATH = "/en/pt-pma-audit-requirements-indonesia/"; URL = D + PATH
TITLE = "PT PMA Audit Requirements in Indonesia 2026: When, Who, How"
DESC = "When a PT PMA must be audited in Indonesia, who is allowed to sign the audit, how the process runs, what documents to prepare, and what drives the fee."
H1 = "PT PMA Audit Requirements in Indonesia (2026): When It Is Required, Who Can Audit, and How It Works"
assert len(TITLE) <= 65 and len(DESC) <= 158

T = rd(P("/en/statutory-audit-indonesia/"))
head, tail = T[:T.index("<main")], T[T.index("</main>"):]
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, count=1, flags=re.S)
head = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description"|name="twitter:description")/>', lambda m: f'<meta content="{DESC}" {m.group(1)}/>', head)
head = re.sub(r'<meta content="[^"]*" (property="og:title"|name="twitter:title")/>', lambda m: f'<meta content="{TITLE}" {m.group(1)}/>', head)
head = re.sub(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{URL}" rel="canonical"/>', head)
head = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{URL}" property="og:url"/>', head)
head = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>\s*', "", head)
head = head.replace(f'<link href="{URL}" rel="canonical"/>', f'<link href="{URL}" rel="canonical"/><link href="{URL}" hreflang="en" rel="alternate"/><link href="{D}/audit-laporan-keuangan-pma/" hreflang="id" rel="alternate"/>', 1)
assert 'lang="en"' in head

FAQ = [
 ("Is every PT PMA required to have a statutory audit?",
  "Not by the Company Law alone. Article 68 of Law 40/2007 requires an audit for specific cases, including companies with assets and/or turnover of at least IDR 50 billion. Separately, the regulation on annual corporate financial information (Government Regulation 24/1998 as amended by Government Regulation 64/1999) covers, among others, companies with total assets of at least IDR 25 billion, bank debtors whose lender requires audited statements, and foreign companies operating in Indonesia. In practice most PT PMA are audited anyway because the parent company, a bank, or a counterparty asks for it."),
 ("Is LKPM the same as an audit?",
  "No. LKPM is the periodic investment activity report submitted through the OSS system. It reports investment realisation and is prepared by the company. An audit is an independent examination of the annual financial statements by a licensed public accountant."),
 ("Who is allowed to audit a PT PMA?",
  "A Public Accountant licensed by the Minister of Finance, practising through a registered public accounting firm (Kantor Akuntan Publik, KAP). A tax consultant, a bookkeeping firm, or an overseas auditor without an Indonesian licence cannot sign an Indonesian statutory audit report."),
 ("Can the same firm keep our books and audit them?",
  "No. Independence rules do not allow the auditor to audit financial statements that the same party prepared. For our clients, bookkeeping and preparation are done by KJA Farhani and the audit by KAP DHN & Rekan, which are separate firms."),
 ("Can the financial statements and audit report be in English?",
  "Yes. Bilingual Indonesian and English statements are common for PT PMA. Keeping the underlying books in English or in US dollars for tax purposes requires prior approval from the tax authority."),
 ("How long does a PT PMA audit take?",
  "It depends mostly on how ready the books are. A company with reconciled accounts and complete documents moves much faster than one that still has to rebuild its ledgers. We agree a timetable after reviewing the trial balance and do not promise a date before that."),
 ("How much does it cost?",
  "The fee follows the work: size and complexity of the company, number of locations, quality of the books, whether it is a first-year audit, and the reporting deadline. We quote after seeing the trial balance, and the fee is fixed in the engagement letter."),
 ("We have never been audited. Can prior years be audited now?",
  "Often yes, but the auditor needs sufficient evidence on opening balances, and inventory that was never counted in prior years can limit what the auditor is able to conclude. Tell us the situation first so the scope is realistic."),
]

def tbl(head_, rows):
    return ('<div class="tblwrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head_) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
def ul(items, tag="ul"): return f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>"

SECS = [
 ("The Short Answer",
  "<p>A PT PMA is not audited simply because it is foreign-owned. It is audited when the law requires it, or when someone who relies on the numbers requires it. For most PT PMA at least one of these applies within the first two or three years.</p>"
  + ul(["<b>By law:</b> assets and/or turnover of at least IDR 50 billion, or one of the other cases in Article 68 of the Company Law.",
        "<b>By filing rules:</b> companies that fall under the annual corporate financial information regulation must file audited statements.",
        "<b>By the people you report to:</b> the parent company, a bank, an investor, a tender committee, or a major customer.",
        "<b>Who signs:</b> an Indonesian Public Accountant practising through a licensed KAP. The firm that prepares the books cannot be the auditor."])),
 ("When an Audit Is Required by Law",
  "<p><b>Company Law (Law 40/2007), Article 68.</b> The board of directors must submit the financial statements to a public accountant for audit when the company:</p>"
  + ul(["collects or manages public funds;", "issues debt acknowledgment instruments to the public;", "is a public (listed) company;",
        "is a state-owned limited company (Persero);", "has assets and/or business turnover of at least IDR 50 billion; or", "is required to do so by other regulations."])
  + "<p>Unaudited statements of a company that falls under Article 68 cannot be validly approved by the General Meeting of Shareholders.</p>"
  "<p><b>Annual corporate financial information.</b> Government Regulation 24/1998, as amended by Government Regulation 64/1999, requires certain companies to submit audited annual financial statements to the Minister of Trade. The scope includes limited liability companies with total assets of at least IDR 25 billion, bank debtors whose lender requires audited statements, and foreign companies domiciled and operating in Indonesia, including branches and representatives. The ministerial regulation that set out the filing procedure (Minister of Trade Regulation 25/2020) was revoked in 2025, so confirm the current filing channel before you submit.</p>"
  "<p><b>Annual report.</b> Under Article 66, the directors present the annual report, which includes the financial statements, to the General Meeting of Shareholders within six months after the financial year ends. If your company is audited, plan the audit so the report is signed before that meeting.</p>"),
 ("When an Audit Is Required in Practice",
  tbl(["Who asks", "Why", "What they usually look at"],
      [("Parent company", "Group consolidation and group audit instructions", "Reporting package, related party balances, deadline set by the group auditor"),
       ("Bank or lender", "Credit approval and annual covenant review", "Opinion, debt classification, covenant ratios"),
       ("Investor or buyer", "Due diligence before investing or acquiring", "Quality of earnings, working capital, tax exposure"),
       ("Tender committee or major customer", "Vendor qualification", "Audited statements for the last one to three years"),
       ("Tax office", "If the statements are audited, the audit report is attached to the annual corporate income tax return", "Consistency between audited figures and the tax return")])
  + "<p>This is why the first question we ask is who will read the audit report. The answer decides the reporting framework, the language, the deadline, and how deep the work has to go.</p>"),
 ("What an Audit Is Not",
  ul(["<b>LKPM</b> is the investment activity report filed through OSS. It is not an audit.",
      "<b>The annual corporate income tax return</b> is filed within four months after the financial year ends. It is not an audit either, although audited figures feed into it.",
      "<b>Bookkeeping or compilation</b> produces the financial statements. An audit is an independent opinion on them.",
      "<b>A review engagement</b> gives limited assurance and is not a substitute when a law, bank, or parent asks for an audit."])),
 ("Who Can Audit a PT PMA",
  "<p>Only a Public Accountant licensed by the Minister of Finance may sign an audit report in Indonesia, and the accountant must practise through a registered KAP (Law 5/2011 on Public Accountants). Before you sign an engagement letter, check three things:</p>"
  + ul(["The KAP and the signing partner hold a valid licence. The Ministry of Finance keeps a public register.",
        "If your reader is in the financial sector or the capital market, the KAP and the partner are also registered with OJK.",
        "The auditor did not prepare your books. Preparer and auditor must be separate firms."], "ol")
  + "<p>A group auditor overseas can issue instructions and rely on the local auditor's work, but cannot replace the Indonesian statutory audit report.</p>"),
 ("Reporting Framework, Language, and Currency",
  ul(["<b>Framework.</b> SAK Indonesia, which is substantially converged with IFRS, or SAK EP for private entities without public accountability. Subsidiaries of IFRS groups usually choose SAK Indonesia to keep reconciling items small.",
      "<b>Functional currency.</b> Determined from the economics of the business, not from where the shareholder is. A PT PMA that sells and buys mostly in US dollars may have a US dollar functional currency under PSAK 221.",
      "<b>Language.</b> Statements are prepared in Indonesian and are commonly issued bilingual. Bookkeeping in English or in US dollars for tax purposes needs approval from the tax authority beforehand.",
      "<b>Group reporting.</b> Differences in effective dates between SAK Indonesia and IFRS are handled in the group reporting package, not by changing the statutory statements."])),
 ("How the Audit Works, Step by Step",
  '<ol class="flow5"><li><b>Scoping call</b>Purpose of the audit, readers, framework, deadline, and a first look at the trial balance.</li>'
  "<li><b>Engagement letter</b>Signed with the KAP. Scope, timetable, and fee are fixed here.</li>"
  "<li><b>Planning and document request</b>Risk assessment and a document list. Year-end inventory counts are scheduled.</li>"
  "<li><b>Fieldwork</b>Testing of balances and transactions, bank and third-party confirmations, review of related party agreements.</li>"
  "<li><b>Adjustments and draft</b>Proposed adjustments are discussed with management, then the draft statements and notes are agreed.</li>"
  "<li><b>Signing</b>Management representation letter, independent auditor's report, and management letter.</li></ol>"
  "<p>The opinion is the auditor's independent decision based on evidence. Nobody can promise an unqualified opinion in advance, and you should be cautious of anyone who does.</p>"),
 ("What Auditors Look at First in a PT PMA",
  tbl(["Area", "What is tested"],
      [("Related party transactions", "Sales, purchases, management fees, and royalties with the group, and their disclosure (PSAK 224)"),
       ("Shareholder loans", "Agreements, interest, exchange rates, and classification as debt or equity"),
       ("Functional currency and foreign exchange", "The functional currency assessment and the resulting exchange differences (PSAK 221)"),
       ("Revenue", "Contracts, performance obligations, and cut-off around year end (PSAK 115)"),
       ("Taxes", "Current and deferred tax, withholding on cross-border payments, and transfer pricing documentation (PSAK 212)"),
       ("Going concern", "Parent support letter where equity is negative or losses are recurring"),
       ("Paid-up capital", "Capital injections against the deed, bank records, and the investment plan")])),
 ("Documents to Prepare",
  ul(["Trial balance, general ledger, and draft financial statements", "Bank statements and reconciliations for all accounts", "Deed of establishment, amendments, business licences (NIB), and shareholder register",
      "Intercompany agreements, shareholder loan agreements, and balance confirmations with the group", "Fixed asset register, inventory count sheets, receivable and payable ageing",
      "Major customer and supplier contracts, lease agreements, and loan agreements", "Tax returns, tax payment slips, and transfer pricing documentation", "Group reporting package and instructions from the group auditor, if any"])
  + '<p>If the books are not ready, they are prepared first. See <a href="/laporan-keuangan-pma/">financial statement preparation for PT PMA</a> (in Indonesian) or ask us in English on WhatsApp.</p>'),
 ("What Drives the Fee",
  "<p>We do not publish a price list because a number without the facts would be wrong for most readers. These are the factors that move the fee, in order of weight:</p>"
  + ul(["<b>Condition of the books.</b> Reconciled, documented ledgers cost far less to audit than ledgers that need rebuilding.",
        "<b>Size and complexity.</b> Transaction volume, number of entities and locations, inventory, and foreign currency exposure.",
        "<b>First-year audit.</b> Opening balances need extra work when prior years were unaudited or audited by another firm.",
        "<b>Reporting requirements.</b> Bilingual statements, a group reporting package, or a full IFRS reconciliation.",
        "<b>Deadline.</b> A group deadline in January or February means more people on the job at the busiest time of the year."], "ol")
  + "<p>Send the trial balance and tell us who will read the report. You get a fixed fee in the engagement letter, not an estimate that grows later.</p>"),
 ("Common Mistakes That Delay a PT PMA Audit",
  ul(["Appointing the auditor after year end, so nobody observed the inventory count.", "Intercompany balances that do not agree with the parent's records.",
      "Shareholder loans without a written agreement or agreed interest terms.", "Expenses paid by the parent on the company's behalf and never recorded locally.",
      "Capital injections that do not match the deed or the bank statement.", "Using the tax return as the financial statements, without notes or proper accruals."])),
]
nav = "".join(f'<li><a href="#s{i}">{E(h)}</a></li>' for i, (h, _) in enumerate(SECS, 1))
body = "".join(f'<h2 id="s{i}">{E(h)}</h2>{b}' for i, (h, b) in enumerate(SECS, 1))
TEAM = ('<h2 id="team">Who You Will Work With</h2>'
        + tbl(["Role", "Who"], [("Your contact from the first message", "Ananta W. Sasongko, CPA, FA Indonesia"),
                                ("Bookkeeping and financial statement preparation", "KJA Farhani K.N., licensed accounting services firm"),
                                ("Statutory audit and opinion", "KAP DHN & Rekan, public accounting firm licensed by the Minister of Finance and registered with OJK")])
        + '<p>FA Indonesia is the contact point. Your WhatsApp message is answered by Ananta directly. Profiles: <a href="/ananta-w-sasongko/">Ananta W. Sasongko</a> · <a href="/kja-farhani/">KJA Farhani</a> · <a href="/kap-dhn/">KAP DHN &amp; Rekan</a>. We serve PT PMA across Indonesia, with documents shared through a secure folder and scheduled site visits.</p>')
btn = f'<a class="btn solid" href="{WA}" rel="noopener" target="_blank">Chat Ananta, CPA</a>'
main = ('<main id="top"><!--fa-enpma-page-->\n<section class="block">\n<div class="wrap art">\n'
        '<p class="eyebrow">Guide · Foreign Investment · Audit</p>\n'
        f'<h1 style="margin:.2em 0 .5em;font-size:clamp(30px,4.2vw,50px);line-height:1.12">{E(H1)}</h1>\n'
        '<p class="meta">By <a href="/ananta-w-sasongko/">Ananta W. Sasongko, CPA</a> · Updated 12 November 2026 · 9 min read</p>\n'
        '<p class="t" style="max-width:62em">A practical guide for directors, finance managers, and regional controllers of foreign-owned companies in Indonesia: the legal triggers, who is allowed to sign, how the work runs, and what to prepare.</p>\n'
        f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 8px">{btn}<a class="btn line" href="/en/statutory-audit-indonesia/">Our PT PMA Services</a></div>\n'
        f'<nav aria-label="Contents" class="pf-map" id="pfmap"><b>Contents</b><ol>{nav}<li><a href="#team">Who You Will Work With</a></li><li><a href="#faq">Frequently Asked Questions</a></li></ol></nav>'
        + body + TEAM
        + '<h2 id="faq">Frequently Asked Questions</h2><div class="faq-acc">' + "".join(f'<details class="faq-i"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ) + "</div>"
        + '<h2 id="sources">Sources</h2>' + ul(["Law 40/2007 on Limited Liability Companies, Articles 66 and 68", "Government Regulation 24/1998 on Annual Corporate Financial Information, as amended by Government Regulation 64/1999",
                                                "Law 5/2011 on Public Accountants", "Indonesian Financial Accounting Standards (SAK Indonesia) issued by DSAK IAI"])
        + '<p class="t">This guide is general information, not legal advice. Regulations change, so confirm the position for your company before acting. Related, in Indonesian: <a href="/audit-laporan-keuangan-pma/">Audit Laporan Keuangan PT PMA</a> · <a href="/artikel/audit-laporan-keuangan-pt-pma-persiapan/">Persiapan Audit PT PMA</a> · <a href="/audit-laporan-keuangan-per-industri/">Audit per Industri</a>.</p>'
        + f'<div class="cbtns" style="display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px">{btn}</div>\n</div>\n</section>\n')
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Article", "headline": H1, "description": DESC, "inLanguage": "en", "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": URL,
     "author": {"@type": "Person", "name": "Ananta W. Sasongko", "url": D + "/ananta-w-sasongko/"},
     "publisher": {"@type": "Organization", "@id": D + "/#org", "name": "FA Indonesia", "url": D + "/"}},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "FA Indonesia", "item": D + "/"},
                                                    {"@type": "ListItem", "position": 2, "name": "PT PMA Services", "item": D + "/en/statutory-audit-indonesia/"},
                                                    {"@type": "ListItem", "position": 3, "name": "PT PMA Audit Requirements", "item": URL}]}]}
head = re.sub(r'<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
head = head.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script></head>", 1)
# buang blok penulis berbahasa Indonesia di ekor template bila ada di dalam main; tail dimulai dari </main>
assert "—" not in main
wt(P(PATH), head + main + tail)

# ---------- link dari halaman lain ----------
def put(path, block, pats):
    p = P(path)
    if not os.path.exists(p): print("lewat", path); return
    t = rd(p); base = re.sub(r"<!--fa-enpma-->.*?<!--/fa-enpma-->", "", t, flags=re.S)
    for pat in pats:
        m = re.search(pat, base)
        if m: wt(p, base[:m.start()] + "<!--fa-enpma-->" + block + "<!--/fa-enpma-->" + base[m.start():]); return
    print("tanpa jangkar", path)
en_line = f'<p class="t" style="margin:6px 0 18px"><b>Guide:</b> <a href="{PATH}">PT PMA Audit Requirements in Indonesia (2026): When, Who, and How</a></p>'
id_line = f'<p class="t"><b>In English:</b> <a href="{PATH}">PT PMA Audit Requirements in Indonesia (2026)</a>, panduan untuk induk usaha dan manajemen asing.</p>'
put("/en/statutory-audit-indonesia/", en_line, [r"<h2>When a PT PMA Needs an Audit</h2>", r"<h2"])
put("/en/accountant-indonesia/", en_line, [r"<h2"])
for u in ("/audit-laporan-keuangan-pma/", "/laporan-keuangan-pma/", "/artikel/audit-laporan-keuangan-pt-pma-persiapan/"):
    put(u, id_line, [r'<nav aria-label="Peta Isi"', r"<h2"])
sm = os.path.join(OUT, "sitemap.xml"); s = re.sub(r"<!--enpma-->.*?<!--/enpma-->\n?", "", rd(sm), flags=re.S)
wt(sm, s.replace("</urlset>", f"<!--enpma--><url><loc>{URL}</loc><lastmod>{TODAY}</lastmod></url><!--/enpma-->\n</urlset>"))
lp = os.path.join(OUT, "llms.txt"); l = re.sub(r"\n<!--enpma-->.*?<!--/enpma-->", "", rd(lp), flags=re.S).rstrip("\n")
wt(lp, l + f"\n<!--enpma-->\n\n## English Guide (12 Nov 2026)\n- [PT PMA Audit Requirements in Indonesia 2026]({URL}): when a foreign-owned company must be audited, who can sign, process, documents, fee drivers\n<!--/enpma-->\n")
print("en pma: file berubah", N[0])
