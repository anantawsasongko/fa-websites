# -*- coding: utf-8 -*-
"""9 Nov 2026 (Bos): template laporan tahunan + laporan keuangan untuk SABH (Permenkum 49/2025) yang diserahkan ke Notaris,
nyambung dengan FA Jupiter, logo FA, lembar penyusun ditandatangani Akuntan Berpraktik (kolom KOSONG, diisi penyusun sendiri;
FA tidak mengklaim siapa penandatangannya).

Hasil (dipakai halaman SABH di FA, CariAkuntan, UpdateSAK; file di-host di faindonesia.co.id/template/):
  out/faindonesia/template/template-laporan-tahunan-pt-sabh-fa-indonesia.docx
  out/faindonesia/template/template-data-laporan-tahunan-sabh-fa-jupiter.xlsx  (sheet COA + GL = format impor FA Jupiter)
Angka adalah ILUSTRASI (PT Contoh Sejahtera), seimbang dan saling cocok antar laporan. Idempoten."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.drawing.image import Image as XLImage

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, "out", "faindonesia", "template")
LOGO = os.path.join(HERE, "out", "faindonesia", "img", "brand", "wm-dark.png")
os.makedirs(OUTD, exist_ok=True)
DOCX = os.path.join(OUTD, "template-laporan-tahunan-pt-sabh-fa-indonesia.docx")
XLSX = os.path.join(OUTD, "template-data-laporan-tahunan-sabh-fa-jupiter.xlsx")
PT_ = "PT Contoh Sejahtera"
Y1, Y0 = "20X1", "20X0"


def rp(v):
    s = f"{abs(v):,.0f}".replace(",", ".")
    return f"({s})" if v < 0 else s


# ---------------- angka ilustrasi (seimbang) ----------------
NERACA = [
    ("ASET", None, None, None, True),
    ("Aset Lancar", None, None, None, True),
    ("Kas dan setara kas", "4", 412_500_000, 356_200_000, False),
    ("Piutang usaha", "5", 1_236_000_000, 1_104_500_000, False),
    ("Persediaan", "6", 865_300_000, 790_100_000, False),
    ("Uang muka dan biaya dibayar dimuka", "", 48_000_000, 52_000_000, False),
    ("Jumlah Aset Lancar", "", 2_561_800_000, 2_302_800_000, True),
    ("Aset Tidak Lancar", None, None, None, True),
    ("Aset tetap - harga perolehan", "7", 2_150_000_000, 1_980_000_000, False),
    ("Akumulasi penyusutan", "7", -735_000_000, -548_000_000, False),
    ("Jumlah Aset Tidak Lancar", "", 1_415_000_000, 1_432_000_000, True),
    ("JUMLAH ASET", "", 3_976_800_000, 3_734_800_000, True),
    ("LIABILITAS DAN EKUITAS", None, None, None, True),
    ("Liabilitas Jangka Pendek", None, None, None, True),
    ("Utang usaha", "8", 642_000_000, 598_300_000, False),
    ("Utang pajak", "9", 86_400_000, 74_900_000, False),
    ("Beban akrual", "", 55_200_000, 49_800_000, False),
    ("Bagian lancar utang bank jangka panjang", "10", 240_000_000, 240_000_000, False),
    ("Jumlah Liabilitas Jangka Pendek", "", 1_023_600_000, 963_000_000, True),
    ("Liabilitas Jangka Panjang", None, None, None, True),
    ("Utang bank jangka panjang", "10", 720_000_000, 960_000_000, False),
    ("Jumlah Liabilitas", "", 1_743_600_000, 1_923_000_000, True),
    ("Ekuitas", None, None, None, True),
    ("Modal saham", "11", 1_000_000_000, 1_000_000_000, False),
    ("Saldo laba", "", 1_233_200_000, 811_800_000, False),
    ("Jumlah Ekuitas", "", 2_233_200_000, 1_811_800_000, True),
    ("JUMLAH LIABILITAS DAN EKUITAS", "", 3_976_800_000, 3_734_800_000, True),
]
LR = [
    ("Pendapatan", "12", 6_840_000_000, 6_120_000_000, False),
    ("Beban pokok pendapatan", "13", -4_582_800_000, -4_162_000_000, False),
    ("LABA KOTOR", "", 2_257_200_000, 1_958_000_000, True),
    ("Beban penjualan", "", -412_000_000, -380_000_000, False),
    ("Beban umum dan administrasi", "14", -1_163_400_000, -1_090_500_000, False),
    ("LABA USAHA", "", 681_800_000, 487_500_000, True),
    ("Pendapatan lain-lain", "", 18_600_000, 15_200_000, False),
    ("Beban keuangan", "10", -139_200_000, -161_400_000, False),
    ("LABA SEBELUM PAJAK PENGHASILAN", "", 561_200_000, 341_300_000, True),
    ("Beban pajak penghasilan", "9", -139_800_000, -85_300_000, False),
    ("LABA TAHUN BERJALAN", "", 421_400_000, 256_000_000, True),
]
EKUITAS = [  # (keterangan, modal, saldo laba)
    (f"Saldo 1 Januari {Y0}", 1_000_000_000, 555_800_000, False),
    (f"Laba tahun {Y0}", 0, 256_000_000, False),
    (f"Saldo 31 Desember {Y0}", 1_000_000_000, 811_800_000, True),
    (f"Laba tahun {Y1}", 0, 421_400_000, False),
    (f"Saldo 31 Desember {Y1}", 1_000_000_000, 1_233_200_000, True),
]
ARUS = [
    ("ARUS KAS DARI AKTIVITAS OPERASI", None, True),
    ("Laba sebelum pajak penghasilan", 561_200_000, False),
    ("Penyesuaian: penyusutan aset tetap", 187_000_000, False),
    ("Kenaikan piutang usaha", -131_500_000, False),
    ("Kenaikan persediaan", -75_200_000, False),
    ("Penurunan uang muka dan biaya dibayar dimuka", 4_000_000, False),
    ("Kenaikan utang usaha", 43_700_000, False),
    ("Kenaikan beban akrual", 5_400_000, False),
    ("Pajak penghasilan dibayar", -128_300_000, False),
    ("Kas Neto dari Aktivitas Operasi", 466_300_000, True),
    ("ARUS KAS DARI AKTIVITAS INVESTASI", None, True),
    ("Perolehan aset tetap", -170_000_000, False),
    ("Kas Neto untuk Aktivitas Investasi", -170_000_000, True),
    ("ARUS KAS DARI AKTIVITAS PENDANAAN", None, True),
    ("Pembayaran utang bank", -240_000_000, False),
    ("Kas Neto untuk Aktivitas Pendanaan", -240_000_000, True),
    ("KENAIKAN NETO KAS DAN SETARA KAS", 56_300_000, True),
    (f"Kas dan setara kas awal tahun", 356_200_000, False),
    (f"KAS DAN SETARA KAS AKHIR TAHUN", 412_500_000, True),
]
# cek konsistensi angka ilustrasi
_n = {r[0]: r for r in NERACA}
assert _n["JUMLAH ASET"][2] == _n["JUMLAH LIABILITAS DAN EKUITAS"][2]
assert _n["JUMLAH ASET"][3] == _n["JUMLAH LIABILITAS DAN EKUITAS"][3]
assert sum(r[2] for r in LR if not r[4]) == 421_400_000 and sum(r[3] for r in LR if not r[4]) == 256_000_000
assert sum(v for k, v, b in ARUS[1:9]) == 466_300_000 and 466_300_000 - 170_000_000 - 240_000_000 == 56_300_000
assert 356_200_000 + 56_300_000 == 412_500_000 and 811_800_000 + 421_400_000 == 1_233_200_000

PENGURUS = [("Direktur Utama", "Nama Direktur Utama", 360_000_000, 30_000_000), ("Direktur", "Nama Direktur", 240_000_000, 20_000_000),
            ("Komisaris", "Nama Komisaris", 60_000_000, 0)]

# ---------------- DOCX ----------------
d = Document()
for s in d.sections:
    s.page_height, s.page_width = Cm(29.7), Cm(21)
    s.left_margin = s.right_margin = Cm(2.3); s.top_margin = Cm(2.2); s.bottom_margin = Cm(2)
st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
for h, sz in (("Heading 1", 16), ("Heading 2", 12.5)):
    hs = d.styles[h]; hs.font.name = "Cambria"; hs.font.size = Pt(sz); hs.font.bold = True; hs.font.color.rgb = RGBColor(0, 0, 0)

# header logo + footer nomor halaman
sec = d.sections[0]
hp = sec.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hp.add_run().add_picture(LOGO, width=Cm(3.4))
r = hp.add_run("\nFormat ilustrasi laporan tahunan untuk SABH"); r.font.size = Pt(7.5); r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
def _fld(p, code):
    r = p.add_run(); a = OxmlElement("w:fldChar"); a.set(qn("w:fldCharType"), "begin"); r._r.append(a)
    r2 = p.add_run(); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = code; r2._r.append(it)
    r3 = p.add_run(); b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "end"); r3._r.append(b)
fr = fp.add_run(f"{PT_} · Laporan Tahunan {Y1} · Halaman "); fr.font.size = Pt(8)
_fld(fp, "PAGE")


def P_(text="", bold=False, size=None, align=None, italic=False, space=4):
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(space)
    if align: p.alignment = align
    if text:
        r = p.add_run(text); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
    return p


def nlist(items):
    for i, s in enumerate(items, 1):
        p = d.add_paragraph(f"{i}. {s}"); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.first_line_indent = Cm(-0.6); p.paragraph_format.space_after = Pt(4)


def brk(): d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexc); tcPr.append(sh)


def table(head, rows, widths, num_cols=(), bold_rows=()):
    t = d.add_table(rows=1, cols=len(head)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]; c.text = ""; rr = c.paragraphs[0].add_run(h); rr.bold = True; rr.font.size = Pt(9.5); shade(c, "EDEDED")
        if i in num_cols: c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""; rr = cells[i].paragraphs[0].add_run(str(v)); rr.font.size = Pt(9.5); rr.bold = ri in bold_rows
            if i in num_cols: cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    t.autofit = False
    for i, w in enumerate(widths): t.columns[i].width = Cm(w)
    for row in t.rows:
        for i, w in enumerate(widths): row.cells[i].width = Cm(w)
    d.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def money_table(rows, cols=(Y1, Y0)):
    out, bold = [], []
    for i, (k, cat, a, b, isb) in enumerate(rows):
        out.append([k, cat or "", rp(a) if a is not None else "", rp(b) if b is not None else ""])
        if isb: bold.append(i)
    table(["Keterangan", "Catatan", f"31 Des {cols[0]}", f"31 Des {cols[1]}"], out, [8.4, 1.6, 3.2, 3.2], num_cols=(2, 3), bold_rows=bold)


# 0. Petunjuk (hapus sebelum dipakai)
P_("PETUNJUK PEMAKAIAN (hapus halaman ini sebelum diserahkan ke Notaris)", True, 12)
PET = []
for s in [
    "Template ini adalah contoh format laporan tahunan PT persekutuan modal yang persetujuan RUPS-nya dituangkan dalam akta notaris dan disampaikan melalui SABH (Permenkum 49/2025, Pasal 16). Semua nama dan angka adalah ILUSTRASI (PT Contoh Sejahtera), bukan data perusahaan nyata.",
    "Angka laporan keuangan bisa dihasilkan otomatis dari FA Jupiter (faindonesia.co.id/audit-ready/): isi sheet COA dan GL di file Excel pendamping (template-data-laporan-tahunan-sabh-fa-jupiter.xlsx), upload ke FA Jupiter, lalu salin hasil Neraca, Laba Rugi, Perubahan Ekuitas, Arus Kas, dan CALK ke bagian B dokumen ini.",
    "Bagian A (Laporan Tahunan) diisi Direksi dan ditelaah Dewan Komisaris. Bagian B (Laporan Keuangan) disusun oleh penyusun laporan keuangan. Bagian C berisi lampiran untuk Notaris.",
    "Lembar Penyusun ditandatangani oleh Akuntan Berpraktik atau Kantor Jasa Akuntansi yang menyusun laporan keuangan, dengan nama dan nomor izinnya sendiri. Bila PT wajib audit (Pasal 68 UU 40/2007, misalnya aset atau omzet paling sedikit Rp50 miliar), lampirkan Laporan Auditor Independen dari Kantor Akuntan Publik sebagai pengganti lembar ini. Untuk satu entitas, penyusun dan auditornya pihak yang berbeda.",
    "Template ini bukan nasihat hukum. Format akta, keputusan RUPS, dan cara penyampaian di SABH mengikuti arahan Notaris Anda.",
    "Butuh dibantu menyusun? Tanya lewat WhatsApp di faindonesia.co.id/laporan-keuangan-sabh/.",
]:
    PET.append(s)
nlist(PET)
brk()

# Sampul
for _ in range(5): P_()
P_(PT_.upper(), True, 22, WD_ALIGN_PARAGRAPH.CENTER)
P_("LAPORAN TAHUNAN", True, 16, WD_ALIGN_PARAGRAPH.CENTER)
P_(f"DAN LAPORAN KEUANGAN TAHUN BUKU {Y1}", True, 13, WD_ALIGN_PARAGRAPH.CENTER)
P_(f"Untuk tahun yang berakhir 31 Desember {Y1} dengan angka pembanding tahun {Y0}", False, 10.5, WD_ALIGN_PARAGRAPH.CENTER, italic=True)
for _ in range(6): P_()
P_("Disampaikan kepada Rapat Umum Pemegang Saham untuk mendapat persetujuan,", False, 10, WD_ALIGN_PARAGRAPH.CENTER)
P_("yang selanjutnya dituangkan dalam akta notaris dan disampaikan melalui SABH", False, 10, WD_ALIGN_PARAGRAPH.CENTER)
P_("sesuai Peraturan Menteri Hukum Nomor 49 Tahun 2025.", False, 10, WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(4): P_()
P_("[Alamat Perseroan] · [Kota]", False, 10, WD_ALIGN_PARAGRAPH.CENTER)
brk()

# Daftar isi
d.add_heading("Daftar Isi", 1)
for s in ["A. Laporan Tahunan", "   A.1 Laporan Kegiatan Perseroan", "   A.2 Pelaksanaan Tanggung Jawab Sosial dan Lingkungan",
          "   A.3 Permasalahan Selama Tahun Buku", "   A.4 Laporan Pengawasan Dewan Komisaris", "   A.5 Susunan Direksi dan Dewan Komisaris",
          "   A.6 Gaji, Honorarium, dan Tunjangan", "B. Laporan Keuangan", "   Surat Pernyataan Direksi", "   Lembar Penyusun Laporan Keuangan",
          "   Laporan Posisi Keuangan", "   Laporan Laba Rugi", "   Laporan Perubahan Ekuitas", "   Laporan Arus Kas", "   Catatan atas Laporan Keuangan",
          "C. Lampiran untuk Notaris", "   C.1 Daftar Dokumen yang Diserahkan", "   C.2 Ilustrasi Keputusan Pemegang Saham secara Sirkuler"]:
    P_(s, space=2)
brk()

# A. Laporan tahunan
d.add_heading("A. Laporan Tahunan", 1)
d.add_heading("A.1 Laporan Kegiatan Perseroan", 2)
P_(f"Selama tahun {Y1}, {PT_} menjalankan kegiatan usaha [uraikan bidang usaha sesuai KBLI dalam anggaran dasar]. Pendapatan naik 11,8% menjadi Rp6,84 miliar, terutama dari [produk/wilayah]. Laba tahun berjalan Rp421,4 juta (tahun {Y0}: Rp256,0 juta).")
P_("[Uraikan pencapaian utama, perubahan kegiatan usaha, investasi, dan rencana tahun berikutnya.]", italic=True)
d.add_heading("A.2 Pelaksanaan Tanggung Jawab Sosial dan Lingkungan", 2)
P_("[Uraikan program TJSL yang dijalankan, penerima manfaat, dan biayanya. Bila belum ada program, jelaskan kebijakan Perseroan.]", italic=True)
d.add_heading("A.3 Permasalahan Selama Tahun Buku", 2)
P_("[Uraikan masalah yang memengaruhi kegiatan usaha, misalnya keterlambatan pembayaran pelanggan, kenaikan harga bahan baku, atau sengketa, beserta langkah penanganannya.]", italic=True)
d.add_heading("A.4 Laporan Pengawasan Dewan Komisaris", 2)
P_(f"Dewan Komisaris telah melakukan pengawasan atas kebijakan pengurusan dan jalannya pengurusan Perseroan oleh Direksi selama tahun {Y1}, serta menelaah laporan tahunan ini sebelum disampaikan kepada RUPS. [Uraikan pokok pengawasan dan rekomendasi.]")
d.add_heading("A.5 Susunan Direksi dan Dewan Komisaris", 2)
table(["Jabatan", "Nama", "Masa Jabatan"], [[a, b, "[sesuai akta]"] for a, b, _, _ in PENGURUS], [5, 7, 4.4])
d.add_heading("A.6 Gaji, Honorarium, dan Tunjangan", 2)
table(["Jabatan", "Gaji / Honorarium (Rp)", "Tunjangan (Rp)", "Jumlah (Rp)"],
      [[a, rp(g), rp(t), rp(g + t)] for a, _, g, t in PENGURUS] + [["Jumlah", rp(sum(x[2] for x in PENGURUS)), rp(sum(x[3] for x in PENGURUS)), rp(sum(x[2] + x[3] for x in PENGURUS))]],
      [5, 4, 3.4, 4], num_cols=(1, 2, 3), bold_rows=(3,))
P_(f"[Kota], [tanggal] · Direksi {PT_}", space=2)
table(["Direktur Utama", "Direktur", "Komisaris (telah menelaah)"], [["\n\n\n( ................................ )", "\n\n\n( ................................ )", "\n\n\n( ................................ )"]], [5.4, 5.4, 5.6])
brk()

# B. Laporan keuangan
d.add_heading("B. Laporan Keuangan", 1)
d.add_heading("Surat Pernyataan Direksi tentang Tanggung Jawab atas Laporan Keuangan", 2)
P_(f"Kami yang bertanda tangan di bawah ini, Direksi {PT_}, menyatakan bahwa:")
LST = []
for s in [f"Kami bertanggung jawab atas penyusunan dan penyajian laporan keuangan {PT_} untuk tahun yang berakhir 31 Desember {Y1};",
          "Laporan keuangan telah disusun dan disajikan sesuai dengan [SAK EP / SAK EMKM / SAK Indonesia, pilih salah satu];",
          "Semua informasi dalam laporan keuangan telah dimuat secara lengkap dan benar, dan laporan keuangan tidak mengandung informasi atau fakta material yang tidak benar maupun menghilangkan informasi atau fakta material;",
          "Kami bertanggung jawab atas sistem pengendalian internal Perseroan."]:
    LST.append(s)
nlist(LST)
P_("Demikian pernyataan ini dibuat dengan sebenarnya.")
table(["Direktur Utama", "Direktur"], [["\n\n\n( ................................ )\nTanggal:", "\n\n\n( ................................ )\nTanggal:"]], [8.2, 8.2])
brk()

d.add_heading("Lembar Penyusun Laporan Keuangan", 2)
P_(f"Laporan keuangan {PT_} untuk tahun yang berakhir 31 Desember {Y1}, yang terdiri dari laporan posisi keuangan, laporan laba rugi, laporan perubahan ekuitas, laporan arus kas, dan catatan atas laporan keuangan, disusun berdasarkan informasi yang diberikan oleh manajemen Perseroan dalam suatu perikatan kompilasi. Penyusun tidak melakukan audit atau reviu atas informasi tersebut dan karena itu tidak menyatakan opini maupun kesimpulan atas laporan keuangan ini. Tanggung jawab atas laporan keuangan tetap berada pada Direksi Perseroan.")
table(["Data Penyusun", "Diisi oleh Akuntan Berpraktik / Kantor Jasa Akuntansi"],
      [["Nama Akuntan Berpraktik", ""], ["Nomor Izin Akuntan Berpraktik", ""], ["Nama Kantor Jasa Akuntansi (bila ada)", ""], ["Nomor Izin KJA", ""],
       ["Alamat kantor", ""], ["Tempat dan tanggal", ""], ["Tanda tangan dan cap", "\n\n\n\n"]], [6.4, 10])
P_("Catatan: bila Perseroan wajib audit, lembar ini diganti Laporan Auditor Independen yang ditandatangani Akuntan Publik dari Kantor Akuntan Publik. Untuk satu entitas, penyusun laporan keuangan dan auditornya pihak yang berbeda.", italic=True, size=9)
brk()

d.add_heading(f"{PT_}\nLaporan Posisi Keuangan\n31 Desember {Y1} dan {Y0} (dalam Rupiah)", 2)
money_table(NERACA)
brk()
d.add_heading(f"{PT_}\nLaporan Laba Rugi\nUntuk Tahun yang Berakhir 31 Desember {Y1} dan {Y0} (dalam Rupiah)", 2)
money_table(LR)
d.add_heading(f"Laporan Perubahan Ekuitas (dalam Rupiah)", 2)
table(["Keterangan", "Modal Saham", "Saldo Laba", "Jumlah Ekuitas"], [[k, rp(m), rp(s_), rp(m + s_)] for k, m, s_, _ in EKUITAS], [6.6, 3.2, 3.2, 3.4],
      num_cols=(1, 2, 3), bold_rows=tuple(i for i, r in enumerate(EKUITAS) if r[3]))
brk()
d.add_heading(f"{PT_}\nLaporan Arus Kas (Metode Tidak Langsung)\nUntuk Tahun yang Berakhir 31 Desember {Y1} (dalam Rupiah)", 2)
table(["Keterangan", f"{Y1}"], [[k, rp(v) if v is not None else ""] for k, v, _ in ARUS], [12.4, 4], num_cols=(1,), bold_rows=tuple(i for i, r in enumerate(ARUS) if r[2]))
brk()

d.add_heading("Catatan atas Laporan Keuangan", 2)
CALK = [
    ("1. Umum", f"{PT_} didirikan berdasarkan akta notaris [nama notaris] Nomor [..] tanggal [..], disahkan Menteri Hukum dengan keputusan Nomor [..]. Perseroan bergerak di bidang [..] dan berkedudukan di [kota]."),
    ("2. Dasar Penyusunan", "Laporan keuangan disusun sesuai [SAK EP / SAK EMKM / SAK Indonesia] berdasarkan konsep biaya historis dan dasar akrual, kecuali laporan arus kas. Mata uang penyajian adalah Rupiah."),
    ("3. Ikhtisar Kebijakan Akuntansi Penting", "Kas dan setara kas; piutang usaha dan cadangan kerugian; persediaan (biaya atau nilai realisasi neto, mana yang lebih rendah); aset tetap dan penyusutan garis lurus; pengakuan pendapatan; imbalan kerja; pajak penghasilan."),
    ("4. Kas dan Setara Kas", f"Kas Rp{rp(12_500_000)} dan bank Rp{rp(400_000_000)}. [Rinci per bank dan nomor rekening disamarkan.]"),
    ("5. Piutang Usaha", "Rincian umur piutang dan cadangan kerugian. [Tabel umur piutang dari FA Jupiter.]"),
    ("6. Persediaan", "Rincian barang jadi, barang dalam proses, bahan baku."),
    ("7. Aset Tetap", f"Mutasi harga perolehan dan akumulasi penyusutan. Penambahan tahun {Y1} Rp170.000.000; beban penyusutan Rp187.000.000."),
    ("8. Utang Usaha", "Rincian per pemasok utama dan umur utang."),
    ("9. Perpajakan", "Utang pajak, rekonsiliasi laba akuntansi ke laba fiskal, beban pajak kini dan tangguhan."),
    ("10. Utang Bank", "Nama bank, plafon, suku bunga, jaminan, jadwal angsuran (bagian lancar Rp240.000.000), dan persyaratan pinjaman (covenant)."),
    ("11. Modal Saham", "Susunan pemegang saham, jumlah saham, nilai nominal, dan persentase kepemilikan sesuai daftar pemegang saham."),
    ("12-14. Pendapatan dan Beban", "Rincian pendapatan per jenis, beban pokok, dan beban umum dan administrasi."),
    ("15. Peristiwa Setelah Periode Pelaporan", "[Uraikan bila ada; bila tidak, nyatakan tidak ada.]"),
]
for h, s in CALK:
    P_(h, True, 10.5, space=1); P_(s)
brk()

# C. Lampiran notaris
d.add_heading("C. Lampiran untuk Notaris", 1)
d.add_heading("C.1 Daftar Dokumen yang Diserahkan", 2)
table(["No", "Dokumen", "Ada"], [[str(i + 1), s, "☐"] for i, s in enumerate([
    "Laporan tahunan bagian A, ditandatangani Direksi dan ditelaah Dewan Komisaris",
    "Laporan keuangan bagian B dengan Lembar Penyusun, atau Laporan Auditor Independen bila wajib audit",
    "Surat Pernyataan Direksi atas laporan keuangan",
    "Undangan dan daftar hadir RUPS, atau keputusan pemegang saham secara sirkuler",
    "Akta pendirian dan perubahan terakhir, SK pengesahan, data pemegang saham terbaru",
    "Fotokopi identitas Direksi, Dewan Komisaris, dan pemegang saham sesuai permintaan Notaris",
    "NPWP Perseroan dan NIB",
])], [1.2, 13.4, 1.8], )
d.add_heading("C.2 Ilustrasi Keputusan Pemegang Saham secara Sirkuler", 2)
P_("(Ilustrasi. Bentuk final mengikuti anggaran dasar dan arahan Notaris.)", italic=True, size=9)
P_(f"Para pemegang saham {PT_} yang mewakili seluruh saham yang telah dikeluarkan Perseroan dengan ini mengambil keputusan di luar Rapat Umum Pemegang Saham sebagai berikut:")
LST = []
for s in [f"Menyetujui Laporan Tahunan Perseroan untuk tahun buku yang berakhir 31 Desember {Y1}, termasuk laporan tugas pengawasan Dewan Komisaris;",
          f"Mengesahkan Laporan Keuangan Perseroan untuk tahun buku yang berakhir 31 Desember {Y1};",
          "Memberikan pelunasan dan pembebasan tanggung jawab sepenuhnya (acquit et de charge) kepada Direksi dan Dewan Komisaris atas tindakan pengurusan dan pengawasan selama tahun buku tersebut, sepanjang tercermin dalam laporan tahunan;",
          "Menetapkan penggunaan laba tahun berjalan [dibukukan sebagai saldo laba / dibagikan sebagai dividen sebesar ..];",
          "Memberi kuasa kepada Direksi untuk menyatakan keputusan ini dalam akta notaris dan menyampaikannya melalui SABH."]:
    LST.append(s)
nlist(LST)
table(["Pemegang Saham", "Jumlah Saham", "Tanda Tangan"], [["[Nama pemegang saham 1]", "[..]", "\n\n"], ["[Nama pemegang saham 2]", "[..]", "\n\n"]], [7, 4, 5.4])
d.save(DOCX)

# ---------------- XLSX (format impor FA Jupiter) ----------------
wb = Workbook()
B = Font(bold=True); HF = PatternFill("solid", fgColor="EDEDED"); thin = Side(style="thin", color="BBBBBB")
def sheet(ws, rows, widths, money=()):
    for r in rows: ws.append(r)
    for c in ws[1]: c.font = B; c.fill = HF
    for i, w in enumerate(widths): ws.column_dimensions[chr(65 + i)].width = w
    for col in money:
        for c in ws[col][1:]: c.number_format = '#,##0;(#,##0)'
    ws.freeze_panes = "A2"

ws = wb.active; ws.title = "Petunjuk"
try:
    img = XLImage(LOGO); img.width, img.height = 216, 40; ws.add_image(img, "A1")
except Exception as e: print("logo xlsx", e)
for i, s in enumerate([
    "", "", "", "Template Data Laporan Tahunan PT untuk SABH (format FA Jupiter)",
    "1. Isi sheet COA (daftar akun + Pos LK + saldo tahun lalu) dan GL (jurnal setahun). Kolom dan urutannya jangan diubah: ini format impor FA Jupiter.",
    "2. Buka faindonesia.co.id/audit-ready/ (FA Jupiter), pilih Upload Excel, lalu unduh Neraca, Laba Rugi, Perubahan Ekuitas, Arus Kas, dan CALK.",
    "3. Salin hasilnya ke template Word (template-laporan-tahunan-pt-sabh-fa-indonesia.docx) bagian B.",
    "4. Isi sheet Pengurus (bagian A.5 dan A.6 laporan tahunan) dan cek sheet Checklist Notaris sebelum dokumen diserahkan ke Notaris.",
    "5. Lembar Penyusun ditandatangani Akuntan Berpraktik atau KJA yang menyusun, dengan nama dan nomor izinnya sendiri. Bila wajib audit, pakai Laporan Auditor Independen dari KAP.",
    "Data di file ini ILUSTRASI (PT Contoh Sejahtera). Hapus dan ganti dengan data perusahaan Anda.",
    "Perlu dibantu? faindonesia.co.id/laporan-keuangan-sabh/ (tombol WhatsApp).",
], start=1):
    ws.cell(row=i, column=1, value=s)
ws["A4"].font = Font(bold=True, size=13); ws.column_dimensions["A"].width = 120

COA = [["Kode Akun", "Nama Akun", "Pos LK", "Saldo Pembanding"],
       ["1101", "Kas kecil", "Kas dan setara kas", 10_000_000], ["1103", "Bank", "Kas dan setara kas", 346_200_000],
       ["1201", "Piutang usaha", "Piutang usaha", 1_104_500_000], ["1301", "Persediaan barang dagang", "Persediaan", 790_100_000],
       ["1401", "Biaya dibayar dimuka", "Uang muka dan biaya dibayar dimuka", 52_000_000],
       ["1501", "Aset tetap", "Aset tetap - harga perolehan", 1_980_000_000], ["1509", "Akumulasi penyusutan", "Akumulasi penyusutan aset tetap", -548_000_000],
       ["2101", "Utang usaha", "Utang usaha", -598_300_000], ["2201", "Utang PPh Badan", "Utang pajak", -74_900_000],
       ["2301", "Beban akrual", "Beban akrual", -49_800_000], ["2401", "Utang bank jangka panjang", "Utang bank jangka panjang", -1_200_000_000],
       ["3101", "Modal saham", "Modal saham", -1_000_000_000], ["3201", "Saldo laba", "Saldo laba", -811_800_000],
       ["4101", "Penjualan", "Pendapatan", 0], ["5101", "Harga pokok penjualan", "Beban pokok pendapatan", 0],
       ["6101", "Beban gaji kantor", "Beban umum dan administrasi", 0], ["6201", "Beban pemasaran", "Beban penjualan", 0],
       ["7101", "Beban bunga bank", "Beban keuangan", 0]]
assert sum(r[3] for r in COA[1:]) == 0
sheet(wb.create_sheet("COA"), COA, [12, 32, 36, 18], money=("D",))
GL = [["No Jurnal", "Tanggal", "Kode Akun", "Nama Akun", "Keterangan", "Debit", "Kredit"],
      ["JU-2601-0001", "20X1-01-05", "1201", "Piutang usaha", "Penjualan kredit (contoh)", 125_000_000, 0],
      ["JU-2601-0001", "20X1-01-05", "4101", "Penjualan", "Penjualan kredit (contoh)", 0, 125_000_000],
      ["JU-2601-0002", "20X1-01-20", "1103", "Bank", "Pelunasan piutang (contoh)", 98_000_000, 0],
      ["JU-2601-0002", "20X1-01-20", "1201", "Piutang usaha", "Pelunasan piutang (contoh)", 0, 98_000_000],
      ["JU-2601-0003", "20X1-01-31", "7101", "Beban bunga bank", "Bunga pinjaman Januari (contoh)", 12_000_000, 0],
      ["JU-2601-0003", "20X1-01-31", "1103", "Bank", "Bunga pinjaman Januari (contoh)", 0, 12_000_000]]
sheet(wb.create_sheet("GL"), GL, [14, 12, 10, 24, 34, 16, 16], money=("F", "G"))
POS = ["Kas dan setara kas", "Piutang usaha", "Cadangan kerugian kredit ekspektasian", "Piutang lain-lain", "Persediaan", "Uang muka dan biaya dibayar dimuka",
       "Pajak dibayar dimuka", "Aset lancar lainnya", "Aset tetap - harga perolehan", "Akumulasi penyusutan aset tetap", "Aset hak guna - neto",
       "Aset takberwujud dan aset lain-lain", "Aset pajak tangguhan", "Utang bank jangka pendek", "Utang usaha", "Utang lain-lain",
       "Uang muka pelanggan / liabilitas kontrak", "Beban akrual", "Utang pajak", "Bagian lancar utang jangka panjang", "Utang bank jangka panjang",
       "Liabilitas sewa", "Liabilitas imbalan kerja", "Liabilitas pajak tangguhan", "Modal saham", "Tambahan modal disetor", "Saldo laba",
       "Akumulasi penghasilan komprehensif lain", "Pendapatan", "Beban pokok pendapatan", "Beban penjualan", "Beban umum dan administrasi",
       "Pendapatan lain-lain", "Beban lain-lain", "Pendapatan keuangan", "Beban keuangan"]
sheet(wb.create_sheet("Pos LK"), [["Daftar Pos LK yang dikenali FA Jupiter"]] + [[p] for p in POS], [48])
sheet(wb.create_sheet("Pengurus"), [["Jabatan", "Nama", "Masa Jabatan", "Gaji / Honorarium", "Tunjangan"]] + [[a, b, "sesuai akta", g, t] for a, b, g, t in PENGURUS],
      [18, 28, 16, 18, 16], money=("D", "E"))
sheet(wb.create_sheet("Checklist Notaris"), [["Dokumen", "Ada (Ya/Belum)", "Catatan"]] + [[s, "", ""] for s in [
    "Laporan tahunan (kegiatan, TJSL, permasalahan, pengawasan Komisaris, pengurus, remunerasi)", "Laporan keuangan + CALK",
    "Lembar Penyusun (Akuntan Berpraktik/KJA) atau Laporan Auditor Independen (KAP) bila wajib audit", "Surat Pernyataan Direksi",
    "Undangan + daftar hadir RUPS atau keputusan sirkuler", "Akta pendirian, perubahan terakhir, SK pengesahan", "Data pemegang saham terbaru", "NPWP dan NIB"]],
      [70, 16, 30])
wb.save(XLSX)
print("ok", DOCX, XLSX)
