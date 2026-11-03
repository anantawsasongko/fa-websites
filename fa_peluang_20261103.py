# -*- coding: utf-8 -*-
"""3 Nov 2026: /mitra-notaris/ dan halaman audit PMA multibahasa (EN, ZH, JA, KO).
Pakai helper fa_lead_20261026.py. Idempoten. Jalankan setelah fa_kec_20261102.py."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "fa_lead_20261026.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ================= 1. JASA IMPLEMENTASI PSAK 118")]
_src = _src.replace('TODAY = "2026-10-26"', 'TODAY = "2026-11-03"')
exec(compile(_src, "fa_lead_helpers", "exec"))
URLS = []

# ================= MITRA NOTARIS =================
PN = "/mitra-notaris/"
bn = ("<h2>Masalah di Meja Notaris Sejak Permenkum 49/2025</h2>"
 "<p>Persetujuan laporan tahunan PT kini dituangkan dalam akta notaris lalu disampaikan lewat SABH. Banyak klien datang tanpa laporan keuangan, dengan laporan yang belum lengkap, atau padahal wajib audit. Akta tertunda, klien terancam teguran Desember 2026 dan blokir SABH mulai 2 Januari 2027.</p>"
 "<h2>Yang Bisa Dirujuk</h2>"
 + tbl(["Kondisi Klien", "Kami Kerjakan", "Oleh"], [
   ("Belum punya laporan keuangan", "Penyusunan laporan keuangan dan CALK", "KJA Farhani"),
   ("Wajib audit (aset atau omzet minimal Rp50 miliar)", "Audit laporan keuangan", "KAP DHN & Rekan, terdaftar OJK"),
   ("Laporan ada tetapi belum lengkap", "Perbaikan CALK dan isi minimal laporan tahunan", "Tim FA"),
   ("Laporan beberapa tahun tertinggal", "Penyusunan ulang dan prioritas tahun yang diminta", "KJA Farhani dan tim FA")])
 + "<h2>Alur Kerja Sama</h2>" + flow([
   ("Rujuk", "Notaris mengirim kontak klien lewat WhatsApp."),
   ("Diskusi klien", "Kami menghubungi klien, menyepakati ruang lingkup dan biaya langsung dengan klien."),
   ("Kerjakan", "Laporan keuangan atau audit diselesaikan sesuai tenggat akta."),
   ("Serahkan", "Laporan dikirim ke klien dan salinannya ke notaris untuk RUPS dan akta.")])
 + "<h2>Komitmen untuk Notaris</h2><ul><li>Klien tetap klien notaris; kami tidak menawarkan jasa kenotariatan.</li><li>Status pengerjaan dikabarkan ke notaris sampai laporan siap.</li><li>Untuk satu klien, penyusun laporan keuangan dan auditornya pihak yang berbeda.</li></ul>"
 "<p>Bacaan untuk klien: <a href=\"/laporan-tahunan-pt/\">Jasa Laporan Tahunan PT</a> dan <a href=\"/jasa-audit-laporan-keuangan/\">Jasa Audit Laporan Keuangan</a>.</p>")
FN = [("Apakah notaris dikenakan biaya untuk merujuk klien?", "Tidak. Biaya disepakati langsung dengan klien sebelum pekerjaan dimulai."),
      ("Berapa lama laporan keuangan atau audit selesai?", "Penyusunan laporan keuangan dengan data lengkap umumnya 1 sampai 2 minggu; audit umumnya 4 sampai 6 minggu sejak dokumen lengkap."),
      ("Apakah melayani klien notaris di luar Jawa?", "Ya. Pekerjaan dilakukan daring, kunjungan lapangan dijadwalkan bila audit memerlukan observasi.")]
svc_page(PN, "Mitra · Notaris", "Mitra Notaris: Laporan Keuangan dan Audit untuk Laporan Tahunan PT Klien Anda",
  "Untuk notaris yang menangani akta persetujuan laporan tahunan PT. Klien yang belum punya laporan keuangan atau wajib audit bisa dirujuk ke tim kami: KJA Farhani untuk penyusunan laporan, KAP DHN & Rekan untuk audit.",
  bn, FN, "Mitra Notaris: Laporan Keuangan dan Audit Laporan Tahunan PT (SABH) | FA Indonesia",
  "Program kerja sama untuk notaris: klien PT tanpa laporan keuangan atau wajib audit untuk laporan tahunan SABH dirujuk ke KJA Farhani dan KAP DHN & Rekan.",
  "Mitra Notaris", "Accounting partner for notaries", "/laporan-tahunan-pt/", "Laporan Tahunan PT",
  "Halo FA Indonesia, saya notaris dan ingin kerja sama untuk laporan keuangan/audit klien PT.", "Mitra Notaris")
URLS.append(PN)
mp = P("mitra-kap-kja", "index.html")
if os.path.exists(mp):
    t = re.sub(r"<!--fa-notaris-->.*?<!--/fa-notaris-->", "", rd(mp), flags=re.S)
    b = '<!--fa-notaris--><p><b>Notaris?</b> Lihat <a href="/mitra-notaris/">Program Mitra Notaris</a> untuk laporan keuangan dan audit klien PT.</p><!--/fa-notaris-->'
    k = t.find("<h2>Pertanyaan Umum</h2>"); k = k if k > 0 else t.find("</main>")
    wtxt(mp, t[:k] + b + t[k:])

# ================= AUDIT PMA MULTIBAHASA =================
L = {
"en": dict(path="/en/statutory-audit-indonesia/", lang="en", eb="Services · Foreign Investment",
  h1="Statutory Audit and Accounting for PT PMA in Indonesia",
  lead="Audit, bookkeeping, and annual reporting for foreign-owned companies (PT PMA) in Jakarta, Batam, Bali, Karawang, Surabaya, Morowali, and across Indonesia. Coordinated in English, Mandarin on request.",
  title="Statutory Audit for PT PMA in Indonesia: Audit, Bookkeeping, Annual Report | FA Indonesia",
  desc="Statutory audit by an OJK-registered public accounting firm, bookkeeping, and annual report filing (SABH) for PT PMA in Indonesia. Free first discussion.",
  wa="Hello FA Indonesia, we are a PT PMA and need an audit / accounting services in Indonesia.", crumb="Statutory Audit (EN)",
  body=("<h2>When a PT PMA Needs an Audit</h2><ul><li>Required by Article 68 of the Company Law when assets or revenue reach IDR 50 billion, or for regulated activities.</li><li>Required by the parent company for group consolidation.</li><li>Requested by banks, investors, or tender committees.</li><li>Supporting the annual report that must be approved by the GMS, notarised, and filed through SABH (Permenkum 49/2025).</li></ul>"
   "<h2>Our Team</h2><div class=\"tblwrap\"><table><tr><th>Role</th><th>Who</th></tr><tr><td>Coordinator</td><td><a href=\"/ananta-w-sasongko/\">Ananta W. Sasongko, CPA</a></td></tr><tr><td>Bookkeeping and financial statements</td><td><a href=\"/kja-farhani/\">KJA Farhani</a>, licensed accounting services firm</td></tr><tr><td>Statutory audit</td><td><a href=\"/kap-dhn/\">KAP DHN &amp; Rekan</a>, licensed by the Minister of Finance, registered with OJK, member of PA Global</td></tr></table></div>"
   "<p>For the same company, the preparer of the financial statements and the auditor are always separate parties.</p>"
   "<h2>How We Work</h2><ol><li>Short call to define scope, reporting framework, and deadline.</li><li>Documents shared through a secure folder; field visit only for inventory and asset observation.</li><li>Fixed fee agreed upfront in the engagement letter.</li></ol>"),
  faq=[("Is every PT PMA required to be audited?", "Not automatically. The Company Law requires an audit when assets or revenue reach IDR 50 billion or for certain activities, but parents, banks, and investors often require one regardless."),
       ("Can you report in English?", "Yes. Financial statements and audit reports can be issued in Indonesian and English."),
       ("Do you serve companies outside Jakarta?", "Yes. We serve clients across Indonesia remotely, with scheduled field visits.")]),
"zh": dict(path="/zh/statutory-audit-indonesia/", lang="zh", eb="服务 · 外资企业",
  h1="印尼外资公司 (PT PMA) 法定审计与会计服务",
  lead="为雅加达、巴淡、巴厘、加拉横、泗水、莫罗瓦利及印尼各地的外资公司提供审计、记账与年度报告服务。可用中文沟通。",
  title="印尼外资公司法定审计与会计服务 | FA Indonesia",
  desc="由在OJK注册的会计师事务所提供法定审计，另有记账及年度报告 (SABH) 服务，适用于印尼外资公司。首次咨询免费。",
  wa="Hello FA Indonesia, we are a PT PMA and need an audit / accounting services in Indonesia. (中文)", crumb="法定审计 (ZH)",
  body=("<h2>外资公司何时需要审计</h2><ul><li>根据公司法第68条，资产或营业额达到500亿印尼盾时必须审计。</li><li>母公司合并报表需要。</li><li>银行、投资者或招标方要求。</li><li>年度报告须经股东大会批准、公证并通过SABH提交 (Permenkum 49/2025)。</li></ul>"
   "<h2>团队</h2><div class=\"tblwrap\"><table><tr><th>角色</th><th>负责方</th></tr><tr><td>项目协调</td><td><a href=\"/ananta-w-sasongko/\">Ananta W. Sasongko, CPA</a></td></tr><tr><td>记账与财务报表</td><td><a href=\"/kja-farhani/\">KJA Farhani</a></td></tr><tr><td>法定审计</td><td><a href=\"/kap-dhn/\">KAP DHN &amp; Rekan</a>，财政部许可，OJK注册，PA Global成员</td></tr></table></div>"
   "<p>同一家公司的财务报表编制方与审计方始终分开。</p>"),
  faq=[("所有外资公司都必须审计吗？", "不一定。公司法规定资产或营业额达到500亿印尼盾时须审计，但母公司、银行和投资者通常也会要求。"),
       ("可以出具英文报告吗？", "可以，财务报表和审计报告可提供印尼文和英文版本。")]),
"ja": dict(path="/ja/statutory-audit-indonesia/", lang="ja", eb="サービス · 外資企業",
  h1="インドネシア外資企業 (PT PMA) の法定監査・会計サービス",
  lead="ジャカルタ、バタム、バリ、カラワン、スラバヤ、モロワリなどインドネシア全土の外資企業向けに、監査、記帳、年次報告をサポートします。英語で対応します。",
  title="インドネシア外資企業 (PT PMA) 法定監査・会計 | FA Indonesia",
  desc="OJK登録の会計事務所による法定監査、記帳、年次報告 (SABH) をインドネシアの外資企業に提供。初回相談無料。",
  wa="Hello FA Indonesia, we are a PT PMA (Japanese-owned) and need an audit / accounting services in Indonesia.", crumb="法定監査 (JA)",
  body=("<h2>外資企業に監査が必要な場合</h2><ul><li>会社法第68条により、資産または売上高が500億ルピアに達した場合。</li><li>親会社の連結決算のため。</li><li>銀行、投資家、入札委員会からの要求。</li><li>年次報告は株主総会の承認、公証、SABHでの提出が必要です (Permenkum 49/2025)。</li></ul>"
   "<h2>チーム</h2><div class=\"tblwrap\"><table><tr><th>役割</th><th>担当</th></tr><tr><td>コーディネーター</td><td><a href=\"/ananta-w-sasongko/\">Ananta W. Sasongko, CPA</a></td></tr><tr><td>記帳・財務諸表作成</td><td><a href=\"/kja-farhani/\">KJA Farhani</a></td></tr><tr><td>法定監査</td><td><a href=\"/kap-dhn/\">KAP DHN &amp; Rekan</a>（財務大臣認可、OJK登録、PA Global加盟）</td></tr></table></div>"
   "<p>同一企業について、財務諸表の作成者と監査人は常に別の主体です。</p>"),
  faq=[("すべての外資企業に監査義務がありますか？", "必ずしもそうではありません。資産または売上高が500億ルピア以上の場合は義務ですが、親会社や銀行が求めることも多くあります。"),
       ("英語の報告書は作成できますか？", "はい。インドネシア語と英語で作成できます。")]),
"ko": dict(path="/ko/statutory-audit-indonesia/", lang="ko", eb="서비스 · 외국인투자기업",
  h1="인도네시아 외국인투자기업 (PT PMA) 법정감사 및 회계 서비스",
  lead="자카르타, 바탐, 발리, 카라왕, 수라바야, 모로왈리 등 인도네시아 전역의 외국인투자기업을 위한 감사, 기장, 연차보고 서비스. 영어로 진행합니다.",
  title="인도네시아 외국인투자기업 (PT PMA) 법정감사 및 회계 | FA Indonesia",
  desc="OJK 등록 회계법인의 법정감사, 기장, 연차보고 (SABH) 서비스를 인도네시아 외국인투자기업에 제공합니다. 첫 상담 무료.",
  wa="Hello FA Indonesia, we are a PT PMA (Korean-owned) and need an audit / accounting services in Indonesia.", crumb="법정감사 (KO)",
  body=("<h2>외국인투자기업에 감사가 필요한 경우</h2><ul><li>회사법 제68조에 따라 자산 또는 매출이 500억 루피아에 도달한 경우.</li><li>모회사 연결재무제표 작성.</li><li>은행, 투자자, 입찰기관의 요구.</li><li>연차보고서는 주주총회 승인, 공증, SABH 제출이 필요합니다 (Permenkum 49/2025).</li></ul>"
   "<h2>팀</h2><div class=\"tblwrap\"><table><tr><th>역할</th><th>담당</th></tr><tr><td>코디네이터</td><td><a href=\"/ananta-w-sasongko/\">Ananta W. Sasongko, CPA</a></td></tr><tr><td>기장 및 재무제표 작성</td><td><a href=\"/kja-farhani/\">KJA Farhani</a></td></tr><tr><td>법정감사</td><td><a href=\"/kap-dhn/\">KAP DHN &amp; Rekan</a> (재무부 인가, OJK 등록, PA Global 회원)</td></tr></table></div>"
   "<p>동일 기업에 대해 재무제표 작성자와 감사인은 항상 분리됩니다.</p>"),
  faq=[("모든 외국인투자기업이 감사 대상입니까?", "반드시 그렇지는 않습니다. 자산 또는 매출이 500억 루피아 이상이면 의무이며, 모회사나 은행이 요구하는 경우도 많습니다."),
       ("영문 보고서가 가능합니까?", "네. 인도네시아어와 영어로 작성할 수 있습니다.")]),
}
alt = "".join(f'<link rel="alternate" hreflang="{v["lang"]}" href="{D}{v["path"]}">' for v in L.values())
for k, v in L.items():
    svc_page(v["path"], v["eb"], v["h1"], E(v["lead"]), v["body"], v["faq"], v["title"], v["desc"],
             "Statutory Audit PT PMA", "Statutory audit and accounting", "/kap-dhn/", "KAP DHN & Rekan", v["wa"], v["crumb"])
    p = P(*v["path"].strip("/").split("/"), "index.html"); t = rd(p)
    t = re.sub(r'<html lang="[^"]*"', f'<html lang="{v["lang"]}"', t, count=1)
    if 'hreflang="ko"' not in t: t = t.replace("</head>", alt + "</head>", 1)
    others = " · ".join(f'<a href="{x["path"]}">{x["lang"].upper()}</a>' for kk, x in L.items() if kk != k)
    t = t.replace("<h2>", f'<p class="t" style="margin:6px 0 18px">{others} · <a href="/jasa-audit-laporan-keuangan/">ID</a></p><h2>', 1)
    wtxt(p, t); URLS.append(v["path"])

sm = re.sub(r"<!--fa-peluang-->.*?<!--/fa-peluang-->\n?", "", rd(P("sitemap.xml")), flags=re.S)
sm = sm.replace("</urlset>", "<!--fa-peluang-->\n" + "".join(f"<url><loc>{D}{u}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n" for u in URLS) + "<!--/fa-peluang-->\n</urlset>")
wtxt(P("sitemap.xml"), sm)
ll = rd(P("llms.txt"))
for u, l in [(PN, "Mitra notaris: laporan keuangan dan audit untuk laporan tahunan PT klien (SABH)"), ("/en/statutory-audit-indonesia/", "Statutory audit and accounting for PT PMA (English, Chinese, Japanese, Korean pages)")]:
    line = f"- {l} → {D}{u}\n"; ll = ll.replace(line, "")
    ll = ll.replace("\n## Layanan Spesifik\n", "\n## Layanan Spesifik\n" + line, 1)
wtxt(P("llms.txt"), ll)
print("fa_peluang ok", URLS)
