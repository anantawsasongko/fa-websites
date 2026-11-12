# -*- coding: utf-8 -*-
"""12 Nov 2026. UpdateSAK: Kertas Kerja siap pakai (strategi Blue Ocean, langkah 4).
BEKERJA LANGSUNG DI out/updatesak. Idempoten.
1. Template Excel berisi data contoh: /kertas-kerja/kertas-kerja-psak-<n>-updatesak.xlsx untuk PSAK 118, 116, 109, 115
   (sheet Petunjuk, Checklist, Kertas Kerja berumus, Contoh Jurnal). Angka contoh PT Contoh Sejahtera, tanpa em dash.
2. Halaman hub /kertas-kerja/.
3. Kotak <!--us-kk--> di /psak/118/, /psak/116/, /psak/109/, /psak/115/; hero beranda (us-hero12); footer since 2016;
   sitemap <!--uskk-->; llms.
Jalankan setelah us_dupfix_20261109.py."""
import os, re, sys, html, glob, urllib.parse, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "updatesak")
D = "https://updatesak.com"
TODAY = "2026-11-12"
E = html.escape
def rd(p): return open(p, encoding="utf-8").read()
def wt(p, t):
    if os.path.exists(p) and rd(p) == t: return 0
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(t); return 1
def wa(txt): return "https://wa.me/6282245260121?text=" + urllib.parse.quote(txt, safe="")

# ---------------- Excel ----------------
GREEN = "0E7C66"
H = Font(bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor=GREEN)
B = Font(bold=True); INP = PatternFill("solid", fgColor="FFF7D6"); TOT = PatternFill("solid", fgColor="E7F3F0")
thin = Side(style="thin", color="BBBBBB"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
RP = '#,##0;(#,##0);"-"'; PC = "0.00%"


def head(ws, row, cols):
    for j, c in enumerate(cols, 1):
        x = ws.cell(row=row, column=j, value=c); x.font = H; x.fill = HF; x.border = BOX
        x.alignment = Alignment(wrap_text=True, vertical="center")
def widths(ws, ws_):
    for j, w in enumerate(ws_, 1): ws.column_dimensions[get_column_letter(j)].width = w
def title(ws, t, sub):
    ws["A1"] = t; ws["A1"].font = Font(bold=True, size=14, color=GREEN)
    ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="666666")
def petunjuk(wb, no, nama, langkah):
    ws = wb.active; ws.title = "Petunjuk"
    title(ws, f"Kertas Kerja PSAK {no} {nama}", "UpdateSAK (updatesak.com), bagian dari FA Indonesia. Gratis dipakai dan diubah.")
    r = 4
    for t in ["Cara pakai:"] + [f"{i}. {s}" for i, s in enumerate(langkah, 1)] + [
            "", "Sel berwarna kuning adalah isian. Sel lain berisi rumus, jangan ditimpa.",
            "Angka yang ada adalah contoh PT Contoh Sejahtera. Ganti dengan angka perusahaan Anda.",
            "Kertas kerja ini alat bantu, bukan pengganti teks standar dan pertimbangan profesional.",
            "Pertanyaan soal kasus perusahaan Anda: tombol Tanya Ananta, CPA di updatesak.com.",
            "Laporan keuangan lengkap dan CALK: FA Jupiter di faindonesia.co.id/audit-ready/"]:
        ws.cell(row=r, column=1, value=t).font = B if t.endswith(":") else Font()
        r += 1
    widths(ws, [110])
def checklist(wb, items):
    ws = wb.create_sheet("Checklist")
    title(ws, "Checklist Penerapan", "Isi kolom Status dengan Sudah, Belum, atau Tidak Berlaku.")
    head(ws, 4, ["No", "Yang Dicek", "Status", "Catatan dan Referensi Dokumen"])
    for i, t in enumerate(items, 1):
        ws.cell(row=4 + i, column=1, value=i).border = BOX
        c = ws.cell(row=4 + i, column=2, value=t); c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = BOX
        s = ws.cell(row=4 + i, column=3, value="Belum"); s.fill = INP; s.border = BOX
        ws.cell(row=4 + i, column=4).fill = INP; ws.cell(row=4 + i, column=4).border = BOX
    n = 4 + len(items)
    ws.cell(row=n + 2, column=2, value="Jumlah Sudah").font = B
    ws.cell(row=n + 2, column=3, value=f'=COUNTIF(C5:C{n},"Sudah")')
    ws.cell(row=n + 3, column=2, value="Jumlah Belum").font = B
    ws.cell(row=n + 3, column=3, value=f'=COUNTIF(C5:C{n},"Belum")')
    widths(ws, [6, 78, 16, 46])
def jurnal(wb, rows, note=""):
    """rows: (keterangan, akun, debit, kredit); debit/kredit boleh rumus."""
    ws = wb.create_sheet("Contoh Jurnal")
    title(ws, "Contoh Jurnal", note or "Angka mengambil dari sheet Kertas Kerja.")
    head(ws, 4, ["Keterangan", "Akun", "Debit", "Kredit"])
    for i, (k, a, d, c) in enumerate(rows, 5):
        ws.cell(row=i, column=1, value=k).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=i, column=2, value=a)
        for col, v in ((3, d), (4, c)):
            x = ws.cell(row=i, column=col, value=v); x.number_format = RP
        for col in range(1, 5): ws.cell(row=i, column=col).border = BOX
    n = 4 + len(rows)
    ws.cell(row=n + 1, column=2, value="Jumlah").font = B
    for col in (3, 4):
        x = ws.cell(row=n + 1, column=col, value=f"=SUM({get_column_letter(col)}5:{get_column_letter(col)}{n})"); x.number_format = RP; x.font = B; x.fill = TOT
    ws.cell(row=n + 2, column=2, value="Cek balance (harus 0)").font = B
    x = ws.cell(row=n + 2, column=3, value=f"=C{n+1}-D{n+1}"); x.number_format = RP
    widths(ws, [44, 44, 20, 20])
def inp(ws, ref, v, fmt=RP):
    ws[ref] = v; ws[ref].fill = INP; ws[ref].number_format = fmt; ws[ref].border = BOX


def psak116():
    wb = Workbook()
    petunjuk(wb, 116, "Sewa", ["Daftar semua kontrak sewa di sheet Checklist dan tentukan mana yang memakai pengecualian.",
                              "Isi pembayaran sewa per tahun, suku bunga pinjaman inkremental, dan masa sewa di sheet Kertas Kerja.",
                              "Baca liabilitas sewa awal, jadwal bunga dan pokok, serta penyusutan aset hak guna.",
                              "Salin jurnal dari sheet Contoh Jurnal ke pembukuan."])
    checklist(wb, ["Semua kontrak sewa gedung, gudang, kendaraan, dan alat sudah didaftar",
                   "Kontrak jasa yang mengandung aset teridentifikasi sudah dinilai apakah mengandung sewa",
                   "Sewa jangka pendek (12 bulan atau kurang) dan aset bernilai rendah sudah dipisah",
                   "Masa sewa sudah memperhitungkan opsi perpanjangan yang cukup pasti dieksekusi",
                   "Suku bunga pinjaman inkremental ditetapkan dan didokumentasikan sumbernya",
                   "Pembayaran di muka, biaya langsung awal, dan insentif sewa masuk ke aset hak guna",
                   "Liabilitas sewa dipisah bagian lancar dan tidak lancar",
                   "Dampak ke rasio utang dalam perjanjian kredit sudah dihitung dan dibahas dengan bank",
                   "Pengungkapan di CALK: analisis jatuh tempo, beban bunga, beban penyusutan, arus kas keluar sewa"])
    ws = wb.create_sheet("Kertas Kerja")
    title(ws, "Liabilitas Sewa dan Aset Hak Guna", "Pembayaran tahunan di akhir tahun, masa sewa sampai 10 tahun.")
    ws["A4"] = "Pembayaran sewa per tahun"; inp(ws, "B4", 240000000)
    ws["A5"] = "Suku bunga pinjaman inkremental per tahun"; inp(ws, "B5", 0.10, PC)
    ws["A6"] = "Masa sewa (tahun, maksimal 10)"; inp(ws, "B6", 5, "0")
    ws["A7"] = "Biaya langsung awal dan pembayaran di muka"; inp(ws, "B7", 0)
    ws["A9"] = "Liabilitas sewa awal (nilai kini)"; ws["B9"] = "=B4*(1-(1+B5)^-B6)/B5"; ws["B9"].number_format = RP; ws["B9"].font = B; ws["B9"].fill = TOT
    ws["A10"] = "Aset hak guna awal"; ws["B10"] = "=B9+B7"; ws["B10"].number_format = RP; ws["B10"].font = B; ws["B10"].fill = TOT
    ws["A11"] = "Penyusutan aset hak guna per tahun"; ws["B11"] = "=B10/B6"; ws["B11"].number_format = RP
    head(ws, 13, ["Tahun", "Liabilitas Awal", "Beban Bunga", "Pembayaran", "Pokok", "Liabilitas Akhir", "Penyusutan", "Aset Hak Guna Akhir"])
    for k in range(1, 11):
        r = 13 + k
        ws.cell(row=r, column=1, value=k)
        ws.cell(row=r, column=2, value="=IF(A14<=$B$6,$B$9,0)" if k == 1 else f"=IF(A{r}<=$B$6,F{r-1},0)")
        ws.cell(row=r, column=3, value=f"=B{r}*$B$5")
        ws.cell(row=r, column=4, value=f"=IF(A{r}<=$B$6,$B$4,0)")
        ws.cell(row=r, column=5, value=f"=D{r}-C{r}")
        ws.cell(row=r, column=6, value=f"=B{r}-E{r}")
        ws.cell(row=r, column=7, value=f"=IF(A{r}<=$B$6,$B$11,0)")
        ws.cell(row=r, column=8, value=f"=$B$10-SUM($G$14:G{r})" if True else None)
        for c in range(2, 9): ws.cell(row=r, column=c).number_format = RP
        for c in range(1, 9): ws.cell(row=r, column=c).border = BOX
    ws["A25"] = "Jumlah"; ws["A25"].font = B
    for c in (3, 4, 5, 7):
        L = get_column_letter(c); x = ws.cell(row=25, column=c, value=f"={L}14+{L}15+{L}16+{L}17+{L}18+{L}19+{L}20+{L}21+{L}22+{L}23"); x.number_format = RP; x.font = B; x.fill = TOT
    ws["A27"] = "Cek: jumlah pokok dikurangi liabilitas awal (harus 0)"; ws["E27"] = "=ROUND(E25-B9,0)"; ws["E27"].number_format = RP
    widths(ws, [46, 20, 18, 18, 18, 20, 18, 22])
    jurnal(wb, [("Tanggal permulaan sewa", "Aset hak guna", "='Kertas Kerja'!B10", None),
                ("", "    Liabilitas sewa", None, "='Kertas Kerja'!B9"),
                ("", "    Kas (biaya langsung awal)", None, "='Kertas Kerja'!B7"),
                ("Akhir tahun 1: pembayaran sewa", "Beban bunga", "='Kertas Kerja'!C14", None),
                ("", "Liabilitas sewa", "='Kertas Kerja'!E14", None),
                ("", "    Kas", None, "='Kertas Kerja'!D14"),
                ("Akhir tahun 1: penyusutan", "Beban penyusutan aset hak guna", "='Kertas Kerja'!G14", None),
                ("", "    Akumulasi penyusutan aset hak guna", None, "='Kertas Kerja'!G14")])
    return wb


def psak109():
    wb = Workbook()
    petunjuk(wb, 109, "Instrumen Keuangan: Cadangan Kerugian Piutang Usaha", [
        "Kelompokkan piutang usaha menurut umur di sheet Kertas Kerja.",
        "Isi tingkat kerugian historis per kelompok umur dari data penagihan 2 sampai 3 tahun terakhir.",
        "Tambahkan penyesuaian kondisi ke depan bila ada alasan yang dapat didukung.",
        "Bandingkan cadangan yang diperlukan dengan saldo cadangan di buku, lalu catat selisihnya."])
    checklist(wb, ["Daftar umur piutang cocok dengan buku besar dan sub buku besar",
                   "Piutang dikelompokkan menurut karakteristik risiko yang serupa (jenis pelanggan, wilayah, jaminan)",
                   "Tingkat kerugian historis dihitung dari data penagihan sendiri dan didokumentasikan",
                   "Penyesuaian kondisi ke depan punya dasar yang dapat dijelaskan",
                   "Piutang yang dinilai individual (sengketa, pailit) dipisah dari matriks",
                   "Piutang pihak berelasi dinilai tersendiri",
                   "Penghapusan piutang mengikuti kebijakan dan persetujuan yang berwenang",
                   "Pengungkapan di CALK: mutasi cadangan, matriks provisi, dan kebijakan penghapusan"])
    ws = wb.create_sheet("Kertas Kerja")
    title(ws, "Matriks Provisi Piutang Usaha (Pendekatan yang Disederhanakan)", "Kerugian kredit ekspektasian sepanjang umur piutang.")
    head(ws, 4, ["Kelompok Umur", "Saldo Piutang", "Tingkat Kerugian Historis", "Penyesuaian Ke Depan", "Tingkat Dipakai", "Cadangan Diperlukan"])
    data = [("Belum jatuh tempo", 1850000000, 0.005, 0.002), ("1 sampai 30 hari", 620000000, 0.015, 0.003), ("31 sampai 60 hari", 310000000, 0.04, 0.005),
            ("61 sampai 90 hari", 140000000, 0.10, 0.01), ("91 sampai 180 hari", 95000000, 0.25, 0.02), ("Lebih dari 180 hari", 60000000, 0.60, 0.05)]
    for i, (k, s, h_, a) in enumerate(data, 5):
        ws.cell(row=i, column=1, value=k); inp(ws, f"B{i}", s); inp(ws, f"C{i}", h_, PC); inp(ws, f"D{i}", a, PC)
        ws.cell(row=i, column=5, value=f"=C{i}+D{i}").number_format = PC
        ws.cell(row=i, column=6, value=f"=B{i}*E{i}").number_format = RP
        for c in (1, 5, 6): ws.cell(row=i, column=c).border = BOX
    ws["A11"] = "Jumlah"; ws["A11"].font = B
    ws["B11"] = "=SUM(B5:B10)"; ws["F11"] = "=SUM(F5:F10)"
    for r in ("B11", "F11"): ws[r].number_format = RP; ws[r].font = B; ws[r].fill = TOT
    ws["A13"] = "Piutang dinilai individual: cadangan"; inp(ws, "F13", 35000000)
    ws["A14"] = "Total cadangan diperlukan"; ws["F14"] = "=F11+F13"; ws["F14"].number_format = RP; ws["F14"].font = B; ws["F14"].fill = TOT
    ws["A15"] = "Saldo cadangan di buku sebelum penyesuaian"; inp(ws, "F15", 98000000)
    ws["A16"] = "Penambahan (pemulihan) cadangan periode ini"; ws["F16"] = "=F14-F15"; ws["F16"].number_format = RP; ws["F16"].font = B
    ws["A17"] = "Cadangan terhadap saldo piutang"; ws["F17"] = "=F14/B11"; ws["F17"].number_format = PC
    widths(ws, [44, 20, 24, 22, 18, 22])
    jurnal(wb, [("Penambahan cadangan (bila hasil positif)", "Beban kerugian penurunan nilai piutang", "=MAX('Kertas Kerja'!F16,0)", None),
                ("", "    Cadangan kerugian penurunan nilai piutang", None, "=MAX('Kertas Kerja'!F16,0)"),
                ("Pemulihan cadangan (bila hasil negatif)", "Cadangan kerugian penurunan nilai piutang", "=MAX(-'Kertas Kerja'!F16,0)", None),
                ("", "    Pemulihan kerugian penurunan nilai piutang", None, "=MAX(-'Kertas Kerja'!F16,0)")])
    return wb


def psak115():
    wb = Workbook()
    petunjuk(wb, 115, "Pendapatan dari Kontrak dengan Pelanggan", [
        "Baca kontrak dengan lima langkah di sheet Checklist.",
        "Isi harga transaksi dan harga jual berdiri sendiri tiap kewajiban pelaksanaan di sheet Kertas Kerja.",
        "Isi persentase pemenuhan tiap kewajiban sampai tanggal laporan.",
        "Baca pendapatan yang diakui, lalu bandingkan dengan tagihan untuk mendapat aset atau liabilitas kontrak."])
    checklist(wb, ["Langkah 1: kontrak dengan pelanggan teridentifikasi (disetujui, hak dan syarat pembayaran jelas, kolektibilitas mungkin)",
                   "Langkah 2: kewajiban pelaksanaan yang dapat dibedakan sudah didaftar",
                   "Langkah 3: harga transaksi ditentukan, termasuk imbalan variabel dan komponen pendanaan signifikan",
                   "Langkah 4: harga transaksi dialokasikan berdasarkan harga jual berdiri sendiri",
                   "Langkah 5: tiap kewajiban dinilai dipenuhi sepanjang waktu atau pada suatu waktu",
                   "Metode pengukuran kemajuan (input atau output) konsisten dan didokumentasikan",
                   "Modifikasi kontrak dan adendum sudah dinilai perlakuannya",
                   "Prinsipal atau agen sudah dinilai untuk barang atau jasa pihak ketiga",
                   "Biaya perolehan kontrak (komisi) dinilai untuk dikapitalisasi",
                   "Pengungkapan di CALK: pemilahan pendapatan, saldo kontrak, kewajiban pelaksanaan tersisa"])
    ws = wb.create_sheet("Kertas Kerja")
    title(ws, "Alokasi Harga Transaksi dan Pengakuan Pendapatan", "Contoh: kontrak penjualan mesin, pemasangan, dan pemeliharaan 2 tahun.")
    ws["A4"] = "Harga transaksi kontrak"; inp(ws, "B4", 1200000000)
    head(ws, 6, ["Kewajiban Pelaksanaan", "Harga Jual Berdiri Sendiri", "Porsi", "Harga Dialokasikan", "Pemenuhan sampai Tanggal Laporan", "Pendapatan Diakui"])
    data = [("Mesin (pada suatu waktu)", 1000000000, 1.0), ("Pemasangan (pada suatu waktu)", 100000000, 1.0), ("Pemeliharaan 24 bulan (sepanjang waktu)", 200000000, 0.25)]
    for i, (k, s, p) in enumerate(data, 7):
        inp(ws, f"A{i}", k, "General"); inp(ws, f"B{i}", s)
        ws.cell(row=i, column=3, value=f"=B{i}/$B$10").number_format = PC
        ws.cell(row=i, column=4, value=f"=$B$4*C{i}").number_format = RP
        inp(ws, f"E{i}", p, PC)
        ws.cell(row=i, column=6, value=f"=D{i}*E{i}").number_format = RP
        for c in (3, 4, 6): ws.cell(row=i, column=c).border = BOX
    ws["A10"] = "Jumlah"; ws["A10"].font = B
    for c in ("B", "D", "F"): ws[f"{c}10"] = f"=SUM({c}7:{c}9)"; ws[f"{c}10"].number_format = RP; ws[f"{c}10"].font = B; ws[f"{c}10"].fill = TOT
    ws["C10"] = "=SUM(C7:C9)"; ws["C10"].number_format = PC
    ws["A12"] = "Sudah ditagih ke pelanggan sampai tanggal laporan"; inp(ws, "B12", 1200000000)
    ws["A13"] = "Liabilitas kontrak (bila tagihan melebihi pendapatan)"; ws["B13"] = "=MAX(B12-F10,0)"; ws["B13"].number_format = RP; ws["B13"].font = B
    ws["A14"] = "Aset kontrak (bila pendapatan melebihi tagihan)"; ws["B14"] = "=MAX(F10-B12,0)"; ws["B14"].number_format = RP; ws["B14"].font = B
    ws["A15"] = "Cek: alokasi dikurangi harga transaksi (harus 0)"; ws["B15"] = "=ROUND(D10-B4,0)"; ws["B15"].number_format = RP
    widths(ws, [50, 24, 12, 22, 30, 22])
    jurnal(wb, [("Penagihan ke pelanggan", "Piutang usaha", "='Kertas Kerja'!B12", None),
                ("", "    Pendapatan", None, "='Kertas Kerja'!F10"),
                ("", "    Liabilitas kontrak", None, "='Kertas Kerja'!B13"),
                ("", "Aset kontrak", "='Kertas Kerja'!B14", None),
                ("", "", None, None)],
           "Angka mengambil dari sheet Kertas Kerja. Sesuaikan baris bila yang timbul aset kontrak.")
    # seimbangkan: bila aset kontrak timbul, pendapatan = tagihan + aset kontrak (debit piutang + aset kontrak = kredit pendapatan)
    return wb


def psak118():
    wb = Workbook()
    petunjuk(wb, 118, "Penyajian dan Pengungkapan dalam Laporan Keuangan", [
        "PSAK 118 berlaku untuk tahun buku yang dimulai 1 Januari 2027 dan menggantikan PSAK 201.",
        "Di sheet Kertas Kerja, isi pos laba rugi dan pilih kategorinya: Operasi, Investasi, Pendanaan, Pajak, atau Dihentikan.",
        "Baca subtotal baru: laba operasi dan laba sebelum pendanaan dan pajak penghasilan.",
        "Pakai sheet Checklist untuk ukuran kinerja yang ditetapkan manajemen dan penyajian komparatif.",
        "Cek awal lebih cepat: Cek PSAK 118 di faindonesia.co.id/cek-psak-118/"])
    checklist(wb, ["Kegiatan usaha utama sudah dinilai (apakah berinvestasi pada aset atau memberi pembiayaan ke pelanggan sebagai usaha utama)",
                   "Tiap pos penghasilan dan beban dipetakan ke kategori operasi, investasi, pendanaan, pajak penghasilan, atau operasi dihentikan",
                   "Subtotal laba operasi disajikan",
                   "Subtotal laba sebelum pendanaan dan pajak penghasilan disajikan",
                   "Selisih kurs diklasifikasikan mengikuti kategori pos yang menimbulkannya",
                   "Beban operasi disajikan menurut sifat atau fungsi dengan dasar yang paling berguna",
                   "Ukuran kinerja yang ditetapkan manajemen diidentifikasi dan direkonsiliasi di satu catatan",
                   "Prinsip agregasi dan disagregasi diterapkan, label pos lain-lain dikurangi",
                   "Laporan arus kas metode tidak langsung dimulai dari laba operasi",
                   "Informasi komparatif disajikan kembali dan rekonsiliasinya disiapkan"])
    ws = wb.create_sheet("Kertas Kerja")
    title(ws, "Pemetaan Pos Laba Rugi ke Kategori PSAK 118", "Penghasilan positif, beban negatif. Ubah kategori di kolom C.")
    head(ws, 4, ["Pos Laba Rugi", "Jumlah", "Kategori"])
    data = [("Pendapatan", 48500000000, "Operasi"), ("Beban pokok pendapatan", -33200000000, "Operasi"), ("Beban penjualan", -3100000000, "Operasi"),
            ("Beban umum dan administrasi", -5400000000, "Operasi"), ("Penghasilan (beban) operasi lain", 150000000, "Operasi"),
            ("Bagian laba entitas asosiasi", 420000000, "Investasi"), ("Penghasilan bunga deposito", 180000000, "Investasi"),
            ("Laba penjualan properti investasi", 260000000, "Investasi"), ("Beban bunga pinjaman bank", -1900000000, "Pendanaan"),
            ("Beban bunga liabilitas sewa", -240000000, "Pendanaan"), ("Beban pajak penghasilan", -1250000000, "Pajak"),
            ("Laba (rugi) operasi dihentikan", 0, "Dihentikan")]
    for i, (k, v, c) in enumerate(data, 5):
        inp(ws, f"A{i}", k, "General"); inp(ws, f"B{i}", v); inp(ws, f"C{i}", c, "General")
    last = 4 + len(data) + 4      # sisakan 4 baris kosong untuk pos tambahan
    for i in range(5 + len(data), last + 1):
        inp(ws, f"A{i}", None, "General"); inp(ws, f"B{i}", None); inp(ws, f"C{i}", None, "General")
    r = last + 2
    def line(lbl, f, bold=True):
        nonlocal r
        ws.cell(row=r, column=1, value=lbl).font = B if bold else Font()
        x = ws.cell(row=r, column=2, value=f); x.number_format = RP
        if bold: x.font = B; x.fill = TOT
        r += 1; return r - 1
    S = lambda k: f'SUMIF($C$5:$C${last},"{k}",$B$5:$B${last})'
    op = line("Laba operasi", "=" + S("Operasi"))
    line("Kategori investasi", "=" + S("Investasi"), False)
    sb = line("Laba sebelum pendanaan dan pajak penghasilan", f"=B{op}+B{op+1}")
    line("Kategori pendanaan", "=" + S("Pendanaan"), False)
    bt = line("Laba sebelum pajak penghasilan", f"=B{sb}+B{sb+1}")
    line("Pajak penghasilan", "=" + S("Pajak"), False)
    ct = line("Laba dari operasi yang dilanjutkan", f"=B{bt}+B{bt+1}")
    line("Operasi dihentikan", "=" + S("Dihentikan"), False)
    nt = line("Laba tahun berjalan", f"=B{ct}+B{ct+1}")
    r += 1
    ws.cell(row=r, column=1, value="Cek: laba tahun berjalan dikurangi jumlah semua pos (harus 0)")
    ws.cell(row=r, column=2, value=f"=ROUND(B{nt}-SUM(B5:B{last}),0)").number_format = RP
    ws.cell(row=r + 1, column=1, value="Bila cek tidak 0, ada pos yang kategorinya kosong atau salah eja.").font = Font(italic=True, color="666666")
    widths(ws, [56, 24, 18])
    ws2 = wb.create_sheet("Ukuran Kinerja Manajemen")
    title(ws2, "Rekonsiliasi Ukuran Kinerja yang Ditetapkan Manajemen", "Contoh: laba operasi disesuaikan. Hapus bila perusahaan tidak mengomunikasikan ukuran seperti ini.")
    head(ws2, 4, ["Uraian", "Jumlah", "Dampak Pajak", "Alasan Penyesuaian"])
    ws2["A5"] = "Laba operasi (subtotal PSAK 118)"; ws2["B5"] = f"='Kertas Kerja'!B{op}"; ws2["B5"].number_format = RP
    for i, (k, v, t, a) in enumerate([("Biaya restrukturisasi", 350000000, -77000000, "Tidak berulang, penutupan satu cabang"),
                                      ("Kerugian penurunan nilai aset", 120000000, -26400000, "Tidak mencerminkan kinerja berjalan")], 6):
        inp(ws2, f"A{i}", k, "General"); inp(ws2, f"B{i}", v); inp(ws2, f"C{i}", t); inp(ws2, f"D{i}", a, "General")
    ws2["A8"] = "Laba operasi disesuaikan"; ws2["A8"].font = B; ws2["B8"] = "=SUM(B5:B7)"; ws2["B8"].number_format = RP; ws2["B8"].font = B; ws2["B8"].fill = TOT
    widths(ws2, [44, 22, 20, 50])
    return wb


KK = [(118, "Penyajian dan Pengungkapan dalam Laporan Keuangan", psak118, "Pemetaan pos laba rugi ke lima kategori, subtotal laba operasi, dan rekonsiliasi ukuran kinerja manajemen"),
      (116, "Sewa", psak116, "Nilai kini liabilitas sewa, jadwal bunga dan pokok, penyusutan aset hak guna, dan jurnalnya"),
      (109, "Instrumen Keuangan", psak109, "Matriks provisi piutang usaha: umur piutang, tingkat kerugian, cadangan yang diperlukan, dan jurnalnya"),
      (115, "Pendapatan dari Kontrak dengan Pelanggan", psak115, "Alokasi harga transaksi ke kewajiban pelaksanaan, pendapatan diakui, aset dan liabilitas kontrak")]
FN = lambda no: f"kertas-kerja-psak-{no}-updatesak.xlsx"


def build_xlsx():
    d = os.path.join(OUT, "kertas-kerja"); os.makedirs(d, exist_ok=True)
    for no, nama, fn, _ in KK:
        p = os.path.join(d, FN(no))
        if os.path.exists(p) and "--xlsx" not in sys.argv: continue   # file biner: buat ulang hanya bila diminta
        wb = fn()
        if no == 115:   # jurnal 115 dibuat seimbang untuk dua arah (aset atau liabilitas kontrak)
            ws = wb["Contoh Jurnal"]
            ws["D9"] = None; ws["B9"] = None
            ws["C5"] = "='Kertas Kerja'!B12"; ws["D6"] = "='Kertas Kerja'!F10"; ws["D7"] = "='Kertas Kerja'!B13"; ws["C8"] = "='Kertas Kerja'!B14"
        wb.properties.creator = "UpdateSAK, FA Indonesia"; wb.properties.title = f"Kertas Kerja PSAK {no} {nama}"
        wb.save(p); print("xlsx", os.path.basename(p))


# ---------------- halaman ----------------
def box(no, nama, isi):
    f = FN(no)
    return ('<!--us-kk--><aside class="us-kk" style="border:1px solid #0E7C66;border-radius:10px;padding:16px 18px;margin:22px 0;background:rgba(14,124,102,.06)">'
            f'<b style="display:block;font-size:17px">Kertas Kerja PSAK {no} (Excel, Gratis)</b>'
            f'<p style="margin:.4em 0 .8em">{E(isi)}. Berisi data contoh, checklist, dan rumus. Download, ganti angkanya, langsung dipakai.</p>'
            f'<a class="btn arrow" href="/kertas-kerja/{f}" download data-us-kk="{no}">Download Kertas Kerja PSAK {no}</a> '
            f'<a class="btn btn-ghost" href="/kertas-kerja/">Semua Kertas Kerja</a>'
            '<p style="margin:.8em 0 0;font-size:13.5px;opacity:.8">Butuh laporan keuangan lengkap dan CALK? <a href="https://faindonesia.co.id/audit-ready/?dari=updatesak">FA Jupiter</a>. '
            'Cek dampak PSAK 118: <a href="https://faindonesia.co.id/cek-psak-118/?dari=updatesak">Cek PSAK 118</a>.</p></aside><!--/us-kk-->')


def run():
    build_xlsx()
    n = 0
    # kotak di halaman PSAK
    for no, nama, _, isi in KK:
        p = os.path.join(OUT, "psak", str(no), "index.html"); t = rd(p)
        base = re.sub(r"<!--us-kk-->.*?<!--/us-kk-->", "", t, flags=re.S)
        m = re.search(r'<nav aria-label="Peta Isi"', base) or re.search(r"<h2", base)
        n += wt(p, base[:m.start()] + box(no, nama, isi) + base[m.start():])
    # hub
    T = rd(os.path.join(OUT, "psak", "116", "index.html"))
    T = re.sub(r"<!--us-kk-->.*?<!--/us-kk-->", "", T, flags=re.S)
    headp, tail = T[:T.index("<main")], T[T.index("</main>"):]
    title_ = "Kertas Kerja PSAK Gratis: Template Excel Siap Pakai"
    desc = "Kertas kerja PSAK gratis dalam Excel: PSAK 118, 116, 109, dan 115. Berisi contoh, checklist, rumus, dan jurnal. Download, ganti angka, langsung dipakai."
    url = D + "/kertas-kerja/"
    headp = re.sub(r"<title>.*?</title>", f"<title>{title_}</title>", headp, count=1, flags=re.S)
    headp = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description"|name="twitter:description")/>', lambda m: f'<meta content="{E(desc)}" {m.group(1)}/>', headp)
    headp = re.sub(r'<meta content="[^"]*" (property="og:title"|name="twitter:title")/>', lambda m: f'<meta content="{title_}" {m.group(1)}/>', headp)
    headp = re.sub(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{url}" rel="canonical"/>', headp)
    headp = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{url}" property="og:url"/>', headp)
    import json
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": title_, "url": url, "description": desc, "inLanguage": "id",
         "publisher": {"@type": "Organization", "name": "UpdateSAK", "url": D + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Beranda", "item": D + "/"},
                                                        {"@type": "ListItem", "position": 2, "name": "Kertas Kerja", "item": url}]}]}
    headp = re.sub(r'<script type="application/ld\+json">.*?</script>', "", headp, flags=re.S)
    headp = headp.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script></head>", 1)
    cards = "".join(
        f'<h2 id="psak-{no}">Kertas Kerja PSAK {no} {E(nama)}</h2><p>{E(isi)}.</p>'
        f'<p><a class="btn arrow" href="/kertas-kerja/{FN(no)}" download data-us-kk="{no}">Download Excel PSAK {no}</a> <a class="btn btn-ghost" href="/psak/{no}/">Baca Ringkasan PSAK {no}</a></p>'
        for no, nama, _, isi in KK)
    watxt = "Halo Pak Ananta, saya pakai kertas kerja PSAK dari updatesak.com. Mau tanya kasus perusahaan kami: "
    main = ('<main>\n<article class="art"><div class="wrap">\n'
            '<nav class="crumb"><a href="/">Beranda</a> / Kertas Kerja</nav>\n<p class="label">Template Excel · Gratis · Tanpa Daftar</p>\n'
            '<h1>Kertas Kerja PSAK: Template Excel Siap Pakai</h1>\n'
            '<p class="lede">Standar akuntansi yang langsung bisa dikerjakan. Tiap file berisi petunjuk, checklist penerapan, kertas kerja berumus dengan data contoh, dan contoh jurnal. Download, ganti angkanya dengan angka perusahaan Anda.</p>\n'
            '<p class="upd">Diperbarui 12 November 2026 · Ditinjau Ananta W. Sasongko, CPA</p>\n'
            + cards +
            '<h2 id="cara-pakai">Cara Pakai</h2><ol class="us-steps"><li>Download file Excel PSAK yang Anda perlukan.</li><li>Baca sheet Petunjuk, lalu isi sel berwarna kuning dengan angka perusahaan.</li><li>Tandai sheet Checklist, salin jurnal dari sheet Contoh Jurnal, dan simpan sebagai kertas kerja pendukung untuk auditor.</li></ol>'
            '<p class="note">Kertas kerja ini alat bantu yang disusun tim UpdateSAK, bukan kutipan teks standar dan bukan pengganti pertimbangan profesional. PSAK lain menyusul.</p>'
            '<h2 id="lanjut">Setelah Kertas Kerja</h2><p>Laporan keuangan lengkap dan CALK: <a href="https://faindonesia.co.id/audit-ready/?dari=updatesak">FA Jupiter</a>. Cek dampak PSAK 118 ke laba rugi: <a href="https://faindonesia.co.id/cek-psak-118/?dari=updatesak">Cek PSAK 118</a>. '
            'Perlu penyusun atau auditor: <a href="https://faindonesia.co.id/audit-laporan-keuangan-per-industri/?dari=updatesak">audit dan laporan keuangan per industri</a> di FA Indonesia, atau <a href="https://cariakuntan.com/cek-kebutuhan/?dari=updatesak">cek kebutuhan jasa</a> di CariAkuntan.</p>'
            f'<section class="us-tanya" aria-label="Tanya Ananta, CPA"><b class="t">Tanya Ananta, CPA</b><p>Kasus perusahaan Anda tidak pas dengan contoh di kertas kerja? Tanyakan langsung. Gratis, dijawab lewat WhatsApp.</p><div class="q"><a class="w" href="{wa(watxt)}" target="_blank" rel="noopener" data-us-q="kk">Tanya kasus perusahaan saya</a></div></section>\n'
            '</div></article>\n')
    n += wt(os.path.join(OUT, "kertas-kerja", "index.html"), headp + main + tail)
    # beranda: hero
    p = os.path.join(OUT, "index.html"); t = rd(p)
    if "<!--us-hero12-->" not in t:
        a = t.index('<p class="label">Update SAK'); b = t.index('<div class="stats">', a)
        new = ('<!--us-hero12--><p class="label">Update SAK · Kertas Kerja · Kalkulator SAK</p>\n<h1>Standar Akuntansi yang Langsung Bisa Dikerjakan.</h1>\n'
               '<p class="sub">Ringkasan, checklist, contoh jurnal, dan template Excel untuk tiap PSAK. Plus kalkulator yang memetakan PSAK wajib dan menyusun CALK format auditor.</p>\n'
               '<div class="cta"><a class="btn arrow" href="/kertas-kerja/">Kertas Kerja PSAK</a><a class="btn btn-ghost" href="#kalkulator">Kalkulator SAK</a><a class="btn btn-ghost" href="https://faindonesia.co.id/cek-psak-118/?dari=updatesak">Cek PSAK 118</a></div>\n<!--/us-hero12-->')
        n += wt(p, t[:a] + new + t[b:])
    # footer since 2016 di semua halaman
    nf = 0
    for q in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True):
        t = rd(q)
        if "© 2026 UpdateSAK" in t: nf += wt(q, t.replace("© 2026 UpdateSAK", "© updatesak.com, since 2016"))
    # sitemap + llms
    sm = os.path.join(OUT, "sitemap.xml"); s = re.sub(r"<!--uskk-->.*?<!--/uskk-->\n?", "", rd(sm), flags=re.S)
    n += wt(sm, s.replace("</urlset>", f"<!--uskk--><url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url><!--/uskk-->\n</urlset>"))
    lp = os.path.join(OUT, "llms.txt")
    if os.path.exists(lp):
        l = re.sub(r"\n<!--uskk-->.*?<!--/uskk-->", "", rd(lp), flags=re.S).rstrip("\n")
        n += wt(lp, l + f"\n<!--uskk-->\n\n## Kertas Kerja PSAK (12 Nov 2026)\n- [Kertas Kerja PSAK Gratis]({url}): template Excel PSAK 118, 116, 109, 115 berisi contoh, checklist, rumus, dan jurnal\n<!--/uskk-->\n")
    print("us kertas kerja: file berubah", n, "| footer", nf)


if __name__ == "__main__":
    run()
