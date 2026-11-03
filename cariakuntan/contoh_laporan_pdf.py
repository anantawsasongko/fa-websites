# -*- coding: utf-8 -*-
"""PDF contoh laporan bulanan jasa pembukuan, format output FA Jupiter (dua bahasa, kolom pembanding,
rujukan catatan, CALK). Perusahaan dan angka dummy. Versi 3 Nov 2026 malam (ganti versi reportlab).
Butuh Playwright + Chromium dan font Liberation Sans (metrik Arial)."""
import os, asyncio, html
from playwright.async_api import async_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site", "files", "contoh-laporan-keuangan-bulanan-jasa-pembukuan.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
CO = "CV Contoh Sejahtera Abadi"

def rp(n):
    if n == 0: return "-"
    s = "{:,.0f}".format(abs(n)).replace(",", ".")
    return f"({s})" if n < 0 else s

# ---- data dummy (Rupiah) ----
OKT = dict(kas=212_640_000, piu=148_900_000, sed=265_400_000, at=318_750_000,
           uu=96_300_000, kur=180_000_000, up=2_432_500, mod=400_000_000, ld=266_957_500)
SEP = dict(kas=184_100_000, piu=142_196_000, sed=249_800_000, at=325_000_000,
           uu=88_200_000, kur=185_000_000, up=2_261_000, mod=400_000_000, ld=225_635_000)
PL_O = dict(pen=486_500_000, hpp=-355_145_000, gaji=-42_000_000, sewa=-12_500_000, bbm=-14_830_000,
            util=-4_120_000, susut=-6_250_000, lain=-3_400_000, pph=-2_432_500)
PL_S = dict(pen=452_200_000, hpp=-332_817_000, gaji=-42_000_000, sewa=-12_500_000, bbm=-13_210_000,
            util=-3_980_000, susut=-6_250_000, lain=-1_560_000, pph=-2_261_000)
PRIVE = -4_500_000

def tot_a(b): return b["kas"] + b["piu"] + b["sed"] + b["at"]
def tot_l(b): return b["uu"] + b["kur"] + b["up"]
def lr(p):
    lk = p["pen"] + p["hpp"]; beban = p["gaji"] + p["sewa"] + p["bbm"] + p["util"] + p["susut"] + p["lain"]
    lu = lk + beban; return lk, beban, lu, lu + p["pph"]
LK_O, BB_O, LU_O, LB_O = lr(PL_O); LK_S, BB_S, LU_S, LB_S = lr(PL_S)
assert tot_a(OKT) == tot_l(OKT) + OKT["mod"] + OKT["ld"]
assert tot_a(SEP) == tot_l(SEP) + SEP["mod"] + SEP["ld"]
assert OKT["ld"] == SEP["ld"] + LB_O + PRIVE

d = lambda k: OKT[k] - SEP[k]
CFO = LB_O + 6_250_000 - d("piu") - d("sed") + d("uu") + d("up")
CFF = d("kur") + PRIVE
assert SEP["kas"] + CFO + CFF == OKT["kas"]

def R(k, i, n, c, p, e): return (k, i, n, c if isinstance(c, str) else rp(c), p if isinstance(p, str) else rp(p), e)
SFP = [
 R("grp","ASET","","","","ASSETS"),
 R("sub","Aset Lancar","","","","Current Assets"),
 R("row","Kas dan bank","2c,3",OKT["kas"],SEP["kas"],"Cash and banks"),
 R("row","Piutang usaha","2d,4",OKT["piu"],SEP["piu"],"Trade receivables"),
 R("row","Persediaan","2e",OKT["sed"],SEP["sed"],"Inventories"),
 R("tot","Jumlah aset lancar","",OKT["kas"]+OKT["piu"]+OKT["sed"],SEP["kas"]+SEP["piu"]+SEP["sed"],"Total current assets"),
 R("sub","Aset Tidak Lancar","","","","Non-current Assets"),
 R("row","Aset tetap, neto","2f",OKT["at"],SEP["at"],"Fixed assets, net"),
 R("tot","Jumlah aset tidak lancar","",OKT["at"],SEP["at"],"Total non-current assets"),
 R("gt","JUMLAH ASET","",tot_a(OKT),tot_a(SEP),"TOTAL ASSETS"),
 R("grp","LIABILITAS DAN EKUITAS","","","","LIABILITIES AND EQUITY"),
 R("sub","Liabilitas","","","","Liabilities"),
 R("row","Utang usaha","",OKT["uu"],SEP["uu"],"Trade payables"),
 R("row","Utang bank (KUR)","5",OKT["kur"],SEP["kur"],"Bank loan (KUR)"),
 R("row","Utang pajak","2g",OKT["up"],SEP["up"],"Taxes payable"),
 R("tot","Jumlah liabilitas","",tot_l(OKT),tot_l(SEP),"Total liabilities"),
 R("sub","Ekuitas","","","","Equity"),
 R("row","Modal","",OKT["mod"],SEP["mod"],"Capital"),
 R("row","Saldo laba","",OKT["ld"],SEP["ld"],"Retained earnings"),
 R("tot","Jumlah ekuitas","",OKT["mod"]+OKT["ld"],SEP["mod"]+SEP["ld"],"Total equity"),
 R("gt","JUMLAH LIABILITAS DAN EKUITAS","",tot_l(OKT)+OKT["mod"]+OKT["ld"],tot_l(SEP)+SEP["mod"]+SEP["ld"],"TOTAL LIABILITIES AND EQUITY"),
]
PL = [
 R("row","Penjualan","2g",PL_O["pen"],PL_S["pen"],"Sales"),
 R("row","Harga pokok penjualan","",PL_O["hpp"],PL_S["hpp"],"Cost of goods sold"),
 R("tot","LABA KOTOR","",LK_O,LK_S,"GROSS PROFIT"),
 R("row","Gaji dan upah","",PL_O["gaji"],PL_S["gaji"],"Salaries and wages"),
 R("row","Sewa gudang","",PL_O["sewa"],PL_S["sewa"],"Warehouse rent"),
 R("row","Transportasi dan BBM","",PL_O["bbm"],PL_S["bbm"],"Transportation and fuel"),
 R("row","Listrik, air, dan internet","",PL_O["util"],PL_S["util"],"Utilities and internet"),
 R("row","Penyusutan aset tetap","2f",PL_O["susut"],PL_S["susut"],"Depreciation of fixed assets"),
 R("row","Beban lain-lain","",PL_O["lain"],PL_S["lain"],"Other expenses"),
 R("tot","LABA SEBELUM PAJAK","",LU_O,LU_S,"PROFIT BEFORE TAX"),
 R("row","Pajak penghasilan final 0,5%","2g",PL_O["pph"],PL_S["pph"],"Final income tax 0.5%"),
 R("gt","LABA BERSIH","",LB_O,LB_S,"NET PROFIT"),
]
CF = [
 R("grp","ARUS KAS DARI AKTIVITAS OPERASI","","","","CASH FLOWS FROM OPERATING ACTIVITIES"),
 R("row","Laba bersih","",LB_O,"","Net profit"),
 R("row","Penyusutan aset tetap","2f",6_250_000,"","Depreciation of fixed assets"),
 R("row","Kenaikan piutang usaha","4",-d("piu"),"","Increase in trade receivables"),
 R("row","Kenaikan persediaan","",-d("sed"),"","Increase in inventories"),
 R("row","Kenaikan utang usaha","",d("uu"),"","Increase in trade payables"),
 R("row","Kenaikan utang pajak","",d("up"),"","Increase in taxes payable"),
 R("tot","Arus kas neto dari aktivitas operasi","",CFO,"","Net cash flows from operating activities"),
 R("grp","ARUS KAS DARI AKTIVITAS PENDANAAN","","","","CASH FLOWS FROM FINANCING ACTIVITIES"),
 R("row","Pembayaran pokok KUR","5",d("kur"),"","Repayment of KUR principal"),
 R("row","Pengambilan pribadi pemilik (prive)","",PRIVE,"","Owner's drawings"),
 R("tot","Arus kas neto dari aktivitas pendanaan","",CFF,"","Net cash flows from financing activities"),
 R("gt","KENAIKAN NETO KAS DAN BANK","",CFO+CFF,"","NET INCREASE IN CASH AND BANKS"),
 R("row","Kas dan bank awal bulan","3",SEP["kas"],"","Cash and banks at beginning of month"),
 R("gt","KAS DAN BANK AKHIR BULAN","3",OKT["kas"],"","CASH AND BANKS AT END OF MONTH"),
]

def head(it, et, ip, ep):
    return (f'<div class=hd><div><b>{CO}</b><br><b>{it}</b><br>{ip}<br><i class=sm>(Dinyatakan dalam Rupiah, kecuali dinyatakan lain)</i></div>'
            f'<div class=en><b>{CO}</b><br><b>{et}</b><br>{ep}<br><i class=sm>(Expressed in Rupiah, unless otherwise stated)</i></div></div>')

def table(rows, two=True, h1=("31 Okt 2026", "Oct 31, 2026"), h2=("30 Sep 2026", "Sep 30, 2026")):
    th = f"<th class=n>Catatan/<br><i>Notes</i></th><th class=a>{h1[0]}/<br><i>{h1[1]}</i></th>" + (f"<th class=a>{h2[0]}/<br><i>{h2[1]}</i></th>" if two else "")
    cols = f"<col style='width:{31 if two else 36}%'><col style='width:7%'><col style='width:15%'>" + ("<col style='width:15%'>" if two else "") + "<col>"
    out = [f"<table class=st><colgroup>{cols}</colgroup><thead><tr><th></th>{th}<th></th></tr></thead><tbody>"]
    for k, i, n, c, p, e in rows:
        out.append(f"<tr class={k}><td>{html.escape(i)}</td><td class=n>{n}</td><td class=a>{c}</td>" + (f"<td class=a>{p}</td>" if two else "") + f"<td class=en>{html.escape(e)}</td></tr>")
    return "".join(out) + "</tbody></table>"

def bi(a, b): return f"<div class=bi><div>{a}</div><div class=en>{b}</div></div>"
def nt(rows, h=("31 Okt 2026", "30 Sep 2026")):
    r = "".join(f"<tr class={k}><td>{a}</td><td class=a>{b}</td><td class=a>{c}</td><td class=en>{e}</td></tr>" for k, a, b, c, e in rows)
    return f"<table class=nt><thead><tr><th></th><th class=a>{h[0]}</th><th class=a>{h[1]}</th><th></th></tr></thead><tbody>{r}</tbody></table>"

PI, PE = "31 Oktober 2026 dan 30 September 2026", "October 31, 2026 and September 30, 2026"
MI, ME = "Untuk Bulan yang Berakhir pada Tanggal 31 Oktober 2026", "For the Month Ended October 31, 2026"
FOOT = ('<p class=ft>Catatan atas laporan keuangan terlampir merupakan bagian yang tidak terpisahkan dari laporan keuangan secara keseluruhan.'
        '<br><i>The accompanying notes to the financial statements form an integral part of these financial statements taken as a whole.</i></p>')

cover = f"""<section class="pg cover"><div class=mark>F<br>&nbsp;&nbsp;&#923;</div>
<p class=kick>CONTOH LAPORAN KEUANGAN BULANAN</p><h1>{CO}</h1>
<p class=big>Laporan Keuangan<br><i>Financial Statements</i></p><p>{PI}<br><i>{PE}</i></p>
<table class=toc>
<tr><td>Laporan Posisi Keuangan</td><td class=en>Statement of Financial Position</td><td class=a>2</td></tr>
<tr><td>Laporan Laba Rugi</td><td class=en>Statement of Profit or Loss</td><td class=a>3</td></tr>
<tr><td>Laporan Arus Kas</td><td class=en>Statement of Cash Flows</td><td class=a>4</td></tr>
<tr><td>Catatan atas Laporan Keuangan</td><td class=en>Notes to the Financial Statements</td><td class=a>5</td></tr>
<tr><td>Lampiran: Catatan Akuntan dan Status Bon</td><td class=en>Appendix: Accountant's Notes and Receipt Status</td><td class=a>7</td></tr>
</table>
<div class=box><b>Contoh hasil jasa pembukuan bulanan.</b> Format ini adalah output FA Jupiter: laporan keuangan dua bahasa dengan kolom pembanding bulan lalu, rujukan catatan, dan CALK. Laporan dikirim 5 sampai 10 hari kerja setelah bon dan mutasi rekening bulan berjalan lengkap di folder Drive klien. Nama perusahaan dan seluruh angka adalah data dummy.</div></section>"""

pages = [cover,
 f"<section class=pg>{head('LAPORAN POSISI KEUANGAN','STATEMENT OF FINANCIAL POSITION',PI,PE)}{table(SFP)}{FOOT}</section>",
 f"<section class=pg>{head('LAPORAN LABA RUGI','STATEMENT OF PROFIT OR LOSS',MI,ME)}{table(PL, h1=('Okt 2026','Oct 2026'), h2=('Sep 2026','Sep 2026'))}{FOOT}</section>",
 f"<section class=pg>{head('LAPORAN ARUS KAS','STATEMENT OF CASH FLOWS',MI,ME)}{table(CF, two=False, h1=('Okt 2026','Oct 2026'))}<p class=sm2>Metode tidak langsung. <i>Indirect method.</i></p>{FOOT}</section>",
 f"""<section class=pg>{head('CATATAN ATAS LAPORAN KEUANGAN','NOTES TO THE FINANCIAL STATEMENTS',MI,ME)}
{bi('<h3>1. UMUM</h3>','<h3>1. GENERAL</h3>')}
{bi(f'<p>{CO} ("Perusahaan") adalah persekutuan komanditer yang bergerak di bidang perdagangan besar dan distribusi barang kebutuhan pokok. Perusahaan berkedudukan di Malang, Jawa Timur.</p>',
    f'<p>{CO} (the "Company") is a limited partnership engaged in wholesale trading and distribution of staple goods. The Company is domiciled in Malang, East Java.</p>')}
{bi('<h3>2. IKHTISAR KEBIJAKAN AKUNTANSI MATERIAL</h3>','<h3>2. SUMMARY OF MATERIAL ACCOUNTING POLICIES</h3>')}
{bi('<h4>a. Pernyataan Kepatuhan</h4><p>Laporan keuangan disusun sesuai dengan Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM) yang diterbitkan oleh Dewan Standar Akuntansi Keuangan Ikatan Akuntan Indonesia.</p>',
    '<h4>a. Statement of Compliance</h4><p>The financial statements have been prepared in accordance with the Financial Accounting Standards for Micro, Small and Medium Entities (SAK EMKM) issued by the Financial Accounting Standards Board of the Institute of Indonesia Chartered Accountants.</p>')}
{bi('<h4>b. Dasar Penyusunan</h4><p>Laporan keuangan disusun dengan dasar akrual dan konsep biaya historis. Laporan bulanan ini menyajikan pembanding posisi keuangan dan hasil usaha bulan sebelumnya.</p>',
    '<h4>b. Basis of Preparation</h4><p>The financial statements have been prepared on the accrual basis using the historical cost concept. This monthly report presents the financial position and results of the previous month as comparatives.</p>')}
{bi('<h4>c. Kas dan Bank</h4><p>Kas dan bank terdiri dari saldo rekening bank yang tidak dibatasi penggunaannya.</p>','<h4>c. Cash and Banks</h4><p>Cash and banks consist of unrestricted bank balances.</p>')}
{bi('<h4>d. Piutang Usaha</h4><p>Piutang usaha dicatat sebesar jumlah tagihan. Piutang yang lewat jatuh tempo lebih dari 60 hari dipantau dan dilaporkan kepada pemilik setiap bulan.</p>','<h4>d. Trade Receivables</h4><p>Trade receivables are stated at invoiced amounts. Receivables more than 60 days past due are monitored and reported to the owner every month.</p>')}
{bi('<h4>e. Persediaan</h4><p>Persediaan dinyatakan sebesar biaya perolehan dengan metode rata-rata tertimbang.</p>','<h4>e. Inventories</h4><p>Inventories are stated at cost using the weighted average method.</p>')}
{bi('<h4>f. Aset Tetap</h4><p>Aset tetap dinyatakan sebesar biaya perolehan dikurangi akumulasi penyusutan, disusutkan dengan metode garis lurus.</p>','<h4>f. Fixed Assets</h4><p>Fixed assets are stated at cost less accumulated depreciation, depreciated using the straight-line method.</p>')}
{bi('<h4>g. Pendapatan dan Pajak</h4><p>Penjualan diakui pada saat barang diserahkan kepada pelanggan. Perusahaan dikenakan pajak penghasilan final 0,5% dari peredaran bruto.</p>','<h4>g. Revenue and Tax</h4><p>Sales are recognized when goods are delivered to customers. The Company is subject to final income tax of 0.5% of gross turnover.</p>')}
</section>""",
 f"""<section class=pg>{head('CATATAN ATAS LAPORAN KEUANGAN','NOTES TO THE FINANCIAL STATEMENTS',MI,ME)}
{bi('<h3>3. KAS DAN BANK</h3>','<h3>3. CASH AND BANKS</h3>')}
{nt([("row","Bank operasional",rp(187_240_000),rp(161_350_000),"Operating bank account"),("row","Bank penerimaan",rp(25_400_000),rp(22_750_000),"Collection bank account"),("tot","Jumlah",rp(OKT['kas']),rp(SEP['kas']),"Total")])}
{bi('<p>Saldo buku seluruh rekening telah direkonsiliasi dengan rekening koran per 31 Oktober 2026 tanpa selisih.</p>','<p>The book balances of all accounts have been reconciled to the bank statements as of October 31, 2026 with no differences.</p>')}
{bi('<h3>4. PIUTANG USAHA</h3>','<h3>4. TRADE RECEIVABLES</h3>')}
{nt([("row","Belum jatuh tempo",rp(98_300_000),rp(104_446_000),"Not yet due"),("row","Lewat 1 sampai 60 hari",rp(32_200_000),rp(28_000_000),"1 to 60 days past due"),("row","Lewat lebih dari 60 hari",rp(18_400_000),rp(9_750_000),"More than 60 days past due"),("tot","Jumlah",rp(OKT['piu']),rp(SEP['piu']),"Total")])}
{bi('<p>Seluruh piutang usaha berasal dari pihak ketiga dan dalam mata uang Rupiah.</p>','<p>All trade receivables are from third parties and denominated in Rupiah.</p>')}
{bi('<h3>5. UTANG BANK (KUR)</h3>','<h3>5. BANK LOAN (KUR)</h3>')}
{bi('<p>Utang bank merupakan fasilitas Kredit Usaha Rakyat dengan angsuran pokok Rp5.000.000 per bulan. Saldo per 31 Oktober 2026 sebesar Rp180.000.000.</p>','<p>The bank loan is a Kredit Usaha Rakyat (KUR) facility with monthly principal instalments of Rp5,000,000. The balance as of October 31, 2026 was Rp180,000,000.</p>')}
</section>""",
 f"""<section class=pg>{head('LAMPIRAN: CATATAN AKUNTAN DAN STATUS BON','APPENDIX: ACCOUNTANT\'S NOTES AND RECEIPT STATUS',MI,ME)}
{bi('<h3>Catatan Akuntan</h3>','<h3>Accountant\'s Notes</h3>')}
{bi('<p>1. Piutang lewat 60 hari naik menjadi Rp18,4 juta (dua pelanggan). Disarankan penagihan sebelum akhir November.</p><p>2. Tiga bon pembelian solar tanpa nota (total Rp1,35 juta) dicatat berdasarkan mutasi rekening; mohon foto nota di-upload ke folder Bon Oktober.</p><p>3. Pembayaran pribadi pemilik Rp4,5 juta dari rekening usaha dicatat sebagai prive, bukan biaya.</p>',
    '<p>1. Receivables more than 60 days past due rose to Rp18.4 million (two customers). Collection before the end of November is recommended.</p><p>2. Three fuel purchases without receipts (total Rp1.35 million) were recorded from bank statements; please upload photos of the receipts to the October folder.</p><p>3. Personal payments of Rp4.5 million from the business account were recorded as owner\'s drawings, not expenses.</p>')}
{bi('<h3>Status Bon di Folder Drive</h3>','<h3>Receipt Status in Drive Folder</h3>')}
<table class=nt><thead><tr><th>Folder</th><th class=a>Jumlah file</th><th>Status</th><th></th></tr></thead><tbody>
<tr><td>Bon pembelian</td><td class=a>142</td><td>Lengkap</td><td class=en>Purchase receipts: complete</td></tr>
<tr><td>Nota penjualan</td><td class=a>318</td><td>Lengkap</td><td class=en>Sales invoices: complete</td></tr>
<tr><td>Bon biaya operasional</td><td class=a>57</td><td>3 nota menyusul</td><td class=en>Operating expense receipts: 3 pending</td></tr>
<tr><td>Mutasi rekening (PDF)</td><td class=a>2</td><td>Lengkap</td><td class=en>Bank statements: complete</td></tr></tbody></table>
</section>"""]

CSS = """
@page{size:A4;margin:18mm 16mm 16mm;@bottom-left{content:'Contoh dari FA Jupiter \\00B7  data dummy \\00B7  cariakuntan.com';font:7.5pt 'Liberation Sans';color:#8a8a8a}@bottom-right{content:counter(page);font:8pt 'Liberation Sans';color:#555}}
*{box-sizing:border-box}body{margin:0;font:9pt/1.45 'Liberation Sans',Arial,sans-serif;color:#1a1a1a}
.pg{page-break-after:always}.pg:last-child{page-break-after:auto}i,.en{font-style:italic}.en{color:#333}
.hd{display:grid;grid-template-columns:1fr 1fr;gap:18px;border-bottom:1.2pt solid #1a1a1a;padding-bottom:7px;margin-bottom:12px;font-size:9.2pt;line-height:1.4}
.sm{font-size:7.8pt}.sm2{font-size:8pt;margin:6px 0 0}
table.st{width:100%;border-collapse:collapse;font-size:8.6pt}
table.st th{font-weight:700;font-size:7.6pt;text-align:left;padding:3px 4px 5px;border-bottom:.8pt solid #1a1a1a;vertical-align:bottom;line-height:1.25}
table.st th.a{text-align:right}table.st th.n{text-align:center}table.st td{padding:3px 4px;vertical-align:top}table.st td.en{padding-left:16px}
.a{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}.n{text-align:center;color:#444;font-size:7.8pt}
tr.grp td{font-weight:700;padding-top:9px}tr.sub td{font-weight:700;padding-top:6px}
tr.row td:first-child{padding-left:12px}table.st tr.row td.en{padding-left:24px}
tr.tot td,tr.gt td{font-weight:700}tr.tot td.a{border-top:.6pt solid #1a1a1a}tr.gt td.a{border-top:.6pt solid #1a1a1a;border-bottom:2pt double #1a1a1a}
.ft{margin-top:16px;padding-top:6px;border-top:.5pt solid #bbb;font-size:7.6pt;color:#555}
.bi{display:grid;grid-template-columns:1fr 1fr;gap:20px}.bi p{margin:0 0 7px;text-align:justify}
h3{font-size:9.4pt;margin:12px 0 6px}h4{font-size:9pt;margin:8px 0 4px}.bi .en h3,.bi .en h4{font-style:italic}
table.nt{width:100%;border-collapse:collapse;font-size:8.6pt;margin:2px 0 8px}table.nt th{font-size:7.8pt;border-bottom:.8pt solid #1a1a1a;padding:3px 4px;text-align:left}table.nt th.a{text-align:right}
table.nt td{padding:3px 4px}table.nt td:first-child{width:34%}table.nt td.en{padding-left:16px}
.cover{padding-top:60px}.mark{width:46px;height:58px;border:1.2pt solid #1a1a1a;font:13pt/1.3 'Liberation Serif',serif;padding:7px 9px;margin-bottom:46px}
.kick{letter-spacing:.2em;font-size:8pt;color:#666;margin:0 0 10px}.cover h1{font:700 22pt/1.2 'Liberation Sans';margin:0 0 18px}
.big{font-size:13pt;margin:0 0 10px}.cover p{font-size:10pt}
table.toc{width:100%;border-collapse:collapse;margin:40px 0 50px;font-size:9.4pt}table.toc td{padding:8px 4px;border-bottom:.5pt solid #ccc}
.box{border-left:3pt solid #1a1a1a;background:#f5f5f3;padding:12px 14px;font-size:9pt;line-height:1.5}
"""
DOC = f"<!doctype html><html lang=id><head><meta charset=utf-8><title>Contoh Laporan Keuangan Bulanan Jasa Pembukuan</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"

async def _main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(DOC); await pg.pdf(path=OUT, format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(_main())
print(OUT, os.path.getsize(OUT))
