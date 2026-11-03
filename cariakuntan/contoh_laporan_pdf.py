# -*- coding: utf-8 -*-
"""PDF contoh laporan bulanan jasa pembukuan (perusahaan fiktif, berlabel CONTOH). 3 Nov 2026."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site", "files", "contoh-laporan-keuangan-bulanan-jasa-pembukuan.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
INK = colors.HexColor("#141414"); ACC = colors.HexColor("#1F5BFF"); MUT = colors.HexColor("#6B6B6B"); LINE = colors.HexColor("#D9D9D9")
H1 = ParagraphStyle("h1", fontName="Times-Roman", fontSize=20, leading=24, textColor=INK, spaceAfter=4)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=10, spaceAfter=6)
P = ParagraphStyle("p", fontName="Helvetica", fontSize=9, leading=13, textColor=INK)
S = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=11, textColor=MUT)
def rp(n): return ("(" if n < 0 else "") + "{:,.0f}".format(abs(n)).replace(",", ".") + (")" if n < 0 else "")
def tbl(rows, widths, bold=(), total=(), left=()):
    t = Table(rows, colWidths=widths)
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
          ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK), ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TEXTCOLOR", (0, 0), (-1, -1), INK)]
    for c_ in left: st.append(("ALIGN", (c_, 0), (c_, -1), "LEFT"))
    for r in bold: st.append(("FONT", (0, r), (-1, r), "Helvetica-Bold", 8.5))
    for r in total: st += [("LINEABOVE", (0, r), (-1, r), 0.6, INK), ("FONT", (0, r), (-1, r), "Helvetica-Bold", 8.5)]
    t.setStyle(TableStyle(st)); return t
def deco(c, d):
    c.saveState(); c.setFillColor(ACC); c.rect(0, A4[1] - 6, A4[0], 6, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(colors.HexColor("#C0392B")); c.drawRightString(A4[0] - 18 * mm, A4[1] - 14 * mm, "CONTOH - PERUSAHAAN FIKTIF")
    c.setFont("Helvetica", 7.5); c.setFillColor(MUT)
    c.drawString(18 * mm, 10 * mm, "cariakuntan.com · Jasa Pembukuan dan Laporan Keuangan Terima Beres · dikerjakan KJA Farhani")
    c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Halaman {d.page}"); c.restoreState()
W = A4[0] - 36 * mm
s = []
s += [Paragraph("CV Contoh Sejahtera Abadi", H1), Paragraph("Laporan Keuangan Bulanan · Oktober 2026 · Disusun sesuai SAK EMKM", S), Spacer(1, 8),
      Paragraph("Dokumen ini adalah contoh format laporan yang diterima klien jasa pembukuan setiap bulan. Nama perusahaan dan seluruh angka fiktif. Laporan dikirim 5 sampai 10 hari kerja setelah bon dan mutasi rekening bulan berjalan lengkap di folder Drive klien.", P), Spacer(1, 6)]
s += [Paragraph("Ringkasan Bulan Ini", H2), tbl([["Indikator", "Oktober 2026", "September 2026"],
      ["Penjualan", rp(486_500_000), rp(452_200_000)], ["Laba kotor", rp(131_355_000), rp(119_383_000)], ["Margin laba kotor", "27,0%", "26,4%"],
      ["Laba bersih", rp(45_822_500), rp(37_622_000)], ["Saldo kas dan bank akhir", rp(212_640_000), rp(184_100_000)], ["Piutang usaha lewat 60 hari", rp(18_400_000), rp(9_750_000)]], [W * .5, W * .25, W * .25])]
s += [Paragraph("Catatan Penting dari Akuntan", H2),
      Paragraph("1. Piutang lewat 60 hari naik menjadi Rp18,4 juta (dua pelanggan). Disarankan penagihan sebelum akhir November.<br/>2. Tiga bon pembelian solar tanpa nota (total Rp1,35 juta) dicatat berdasarkan mutasi rekening; mohon foto nota diunggah ke folder 'Bon Oktober'.<br/>3. Pembayaran pribadi pemilik Rp4,5 juta dari rekening usaha dicatat sebagai prive, bukan biaya.", P)]
s += [PageBreak(), Paragraph("Laporan Laba Rugi", H2), tbl([["Keterangan", "Okt 2026", "Sep 2026", "Jan s.d. Okt 2026"],
      ["Penjualan", rp(486_500_000), rp(452_200_000), rp(4_412_800_000)], ["Harga pokok penjualan", rp(-355_145_000), rp(-332_817_000), rp(-3_235_600_000)],
      ["Laba kotor", rp(131_355_000), rp(119_383_000), rp(1_177_200_000)], ["Gaji dan upah", rp(-42_000_000), rp(-42_000_000), rp(-410_000_000)],
      ["Sewa gudang", rp(-12_500_000), rp(-12_500_000), rp(-125_000_000)], ["Transportasi dan BBM", rp(-14_830_000), rp(-13_210_000), rp(-139_400_000)],
      ["Listrik, air, internet", rp(-4_120_000), rp(-3_980_000), rp(-40_300_000)], ["Penyusutan", rp(-6_250_000), rp(-6_250_000), rp(-62_500_000)],
      ["Beban lain-lain", rp(-3_400_000), rp(-1_560_000), rp(-27_900_000)], ["Laba sebelum pajak", rp(48_255_000), rp(39_883_000), rp(372_100_000)],
      ["Pajak penghasilan final 0,5%", rp(-2_432_500), rp(-2_261_000), rp(-22_064_000)], ["Laba bersih", rp(45_822_500), rp(37_622_000), rp(350_036_000)]],
      [W * .4, W * .2, W * .2, W * .2], total=(3, 10, 12))]
s += [Paragraph("Laporan Posisi Keuangan per 31 Oktober 2026", H2), tbl([["Aset", "Rp", "Liabilitas dan Ekuitas", "Rp"],
      ["Kas dan bank", rp(212_640_000), "Utang usaha", rp(96_300_000)], ["Piutang usaha", rp(148_900_000), "Utang bank (KUR)", rp(180_000_000)],
      ["Persediaan", rp(265_400_000), "Utang pajak", rp(2_432_500)], ["Aset tetap bersih", rp(318_750_000), "Modal", rp(400_000_000)],
      ["", "", "Laba ditahan", rp(266_957_500)], ["Jumlah aset", rp(945_690_000), "Jumlah liabilitas dan ekuitas", rp(945_690_000)]],
      [W * .3, W * .2, W * .3, W * .2], total=(6,), left=(2,))]
s += [PageBreak(), Paragraph("Rekonsiliasi Bank dan Status Bon", H2), tbl([["Rekening", "Saldo buku", "Saldo bank", "Selisih"],
      ["Bank operasional", rp(187_240_000), rp(187_240_000), "0"], ["Bank penerimaan", rp(25_400_000), rp(25_400_000), "0"]], [W * .4, W * .2, W * .2, W * .2]), Spacer(1, 8),
      tbl([["Folder Drive", "Jumlah file", "Status"], ["Bon pembelian", "142", "Lengkap"], ["Nota penjualan", "318", "Lengkap"], ["Bon biaya operasional", "57", "3 nota menyusul"], ["Mutasi rekening (PDF)", "2", "Lengkap"]], [W * .5, W * .2, W * .3], left=(2,))]
s += [Paragraph("Cara Kerja Layanan", H2), Paragraph("1. Klien mengunggah foto bon, nota, catatan single entry, dan mutasi rekening ke folder Drive yang kami siapkan.<br/>2. Tim KJA Farhani menginput, mengklasifikasi, dan merekonsiliasi.<br/>3. Laporan bulanan dikirim 5 sampai 10 hari kerja setelah bukti lengkap, beserta catatan tindak lanjut.<br/>4. Di akhir tahun, laporan dipakai untuk SPT Tahunan, laporan tahunan PT, pengajuan kredit, atau audit KAP (dilaksanakan pihak terpisah).", P), Spacer(1, 10),
      Paragraph("Contoh ini dibuat untuk ilustrasi format. Tidak menggambarkan klien nyata.", S)]
SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=22 * mm, bottomMargin=18 * mm,
                  title="Contoh Laporan Keuangan Bulanan Jasa Pembukuan", author="cariakuntan.com").build(s, onFirstPage=deco, onLaterPages=deco)
print(OUT, os.path.getsize(OUT))
