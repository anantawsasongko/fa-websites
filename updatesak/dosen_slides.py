# Bahan ajar dosen UpdateSAK: PDF slide 16:9, maksimal 8 slide per topik. Dipanggil build_dosen.py.
# Angka contoh adalah data ilustrasi dan dihitung di sini supaya selalu konsisten.
import os
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, Frame
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, "fonts")
for n, f in [("Plex", "IBMPlexSans-Regular.ttf"), ("PlexSB", "IBMPlexSans-SemiBold.ttf"), ("Serif", "SourceSerif4-Semibold.ttf"), ("Qs", "Quicksand-Light.ttf")]:
    try: pdfmetrics.registerFont(TTFont(n, os.path.join(F, f)))
    except Exception: pass
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Plex", normal="Plex", bold="PlexSB", italic="Plex", boldItalic="PlexSB")

W, H = 960, 540
NAVY, BLUE, INK, MUTED, LINE, PANEL = (colors.HexColor(c) for c in ("#0B1F33", "#1F5BFF", "#1A2332", "#5B6576", "#D5DBE5", "#F3F6FB"))
UPD = "31 Oktober 2026"
ST = dict(
    b=ParagraphStyle("b", fontName="Plex", fontSize=17, leading=24, textColor=INK, leftIndent=20, bulletIndent=2, spaceAfter=9, bulletFontName="PlexSB", bulletColor=BLUE),
    p=ParagraphStyle("p", fontName="Plex", fontSize=17, leading=24, textColor=INK, spaceAfter=9),
    small=ParagraphStyle("s", fontName="Plex", fontSize=15, leading=21, textColor=INK, leftIndent=18, bulletIndent=2, spaceAfter=6, bulletFontName="PlexSB", bulletColor=BLUE),
    note=ParagraphStyle("n", fontName="Plex", fontSize=14.5, leading=20, textColor=NAVY),
    cell=ParagraphStyle("c", fontName="Plex", fontSize=12.5, leading=16, textColor=INK),
    cellb=ParagraphStyle("cb", fontName="PlexSB", fontSize=12.5, leading=16, textColor=INK),
    th=ParagraphStyle("th", fontName="PlexSB", fontSize=11, leading=14, textColor=colors.white),
)


def rp(x, d=0):
    """Format angka gaya Indonesia: titik ribuan, koma desimal, kurung untuk negatif."""
    s = f"{abs(x):,.{d}f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return f"({s})" if x < 0 else s


def logo(c, x, y, h, col=BLUE):
    k = h / 40.0
    c.saveState(); c.setStrokeColor(col); c.setLineCap(1); c.setLineJoin(1)
    c.setLineWidth(1.2 * k); c.rect(x + .6 * k, y + .6 * k, 28.8 * k, 38.8 * k, stroke=1, fill=0)
    P = lambda X, Y: (x + X * k, y + (40 - Y) * k)
    c.setLineWidth(1.3 * k); p = c.beginPath(); p.moveTo(*P(6.5, 8)); p.lineTo(*P(6.5, 14.2))
    p.arcTo(x + 6.5 * k, y + (40 - 17.4) * k, x + 12.9 * k, y + (40 - 11.0) * k, startAng=180, extent=180); p.lineTo(*P(12.9, 8)); c.drawPath(p, stroke=1, fill=0)
    p = c.beginPath(); p.moveTo(*P(24.2, 24.4)); p.curveTo(*P(23.3, 23.2), *P(18.6, 22.8), *P(18.6, 25.8))
    p.curveTo(*P(18.6, 28.7), *P(24.7, 27.4), *P(24.7, 30.4)); p.curveTo(*P(24.7, 33.5), *P(19.4, 33.2), *P(18.1, 31.6))
    c.drawPath(p, stroke=1, fill=0); c.restoreState()


def wordmark(c, x, y, size, dark=False):
    c.setFont("Qs", size); c.setFillColor(colors.white if dark else NAVY); c.drawString(x, y, "Update")
    c.setFillColor(colors.HexColor("#8FB2FF") if dark else BLUE); c.drawString(x + c.stringWidth("Update", "Qs", size), y, "SAK")


def chrome(c, deck, i, n):
    c.setFillColor(colors.white); c.rect(0, 0, W, H, stroke=0, fill=1)
    logo(c, 48, 498, 22); wordmark(c, 70, 503, 13)
    c.setFont("Plex", 10.5); c.setFillColor(MUTED); c.drawRightString(W - 48, 505, "Bahan Ajar · " + deck["short"])
    c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(48, 488, W - 48, 488); c.line(48, 44, W - 48, 44)
    c.setFont("Plex", 10); c.drawString(48, 26, "updatesak.com/dosen/bahan-ajar/  ·  Boleh dipakai untuk perkuliahan dengan mencantumkan sumber")
    c.setFont("PlexSB", 10); c.drawRightString(W - 48, 26, f"{i} / {n}")


def title(c, t, kick=None):
    y = 448
    if kick:
        c.setFont("PlexSB", 10.5); c.setFillColor(BLUE); c.drawString(48, 462, kick.upper())
        y = 436
    c.setFont("Serif", 27); c.setFillColor(NAVY); c.drawString(48, y, t)
    c.setFillColor(BLUE); c.rect(48, y - 14, 44, 3, stroke=0, fill=1)
    return y - 30


def flow(c, items, x, top, w, h, style="b"):
    fr = Frame(x, 60, w, top - 60, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    st = ST[style]
    paras = [Paragraph(t, st, bulletText="•" if style in ("b", "small") else None) for t in items]
    fr.addFromList(paras, c)


def table(c, head, rows, widths, x, top, bold_rows=(), align_right=None):
    compact = len(rows) > 11
    pad = 3 if compact else 5
    data = [[Paragraph(h, ST["th"]) for h in head]]
    for r_i, r in enumerate(rows):
        stl = ST["cellb"] if r_i in bold_rows else ST["cell"]
        if compact: stl = ParagraphStyle("cc", parent=stl, fontSize=11.5, leading=14)
        data.append([Paragraph(str(v), stl) for v in r])
    t = Table(data, colWidths=widths)
    sty = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
           ("LINEBELOW", (0, 1), (-1, -1), .5, LINE), ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]
    for r_i in bold_rows: sty.append(("BACKGROUND", (0, r_i + 1), (-1, r_i + 1), PANEL))
    t.setStyle(TableStyle(sty))
    if align_right:
        for col in align_right:
            for row in data[1:]:
                row[col].style = ParagraphStyle("r", parent=row[col].style, alignment=2)
            data[0][col].style = ParagraphStyle("rh", parent=ST["th"], alignment=2)
        t = Table(data, colWidths=widths); t.setStyle(TableStyle(sty))
    tw, th = t.wrap(sum(widths), 400)
    t.drawOn(c, x, top - th)
    return top - th


def note(c, text, x, y_top, w, label="Catatan"):
    p = Paragraph(f"<font name='PlexSB'>{label}.</font> {text}", ST["note"])
    pw, ph = p.wrap(w - 28, 300)
    c.setFillColor(PANEL); c.rect(x, y_top - ph - 20, w, ph + 20, stroke=0, fill=1)
    c.setFillColor(BLUE); c.rect(x, y_top - ph - 20, 4, ph + 20, stroke=0, fill=1)
    p.drawOn(c, x + 16, y_top - ph - 10)
    return y_top - ph - 20


def cover(c, deck, n):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#14304D"))
    for gx in range(0, W, 24):
        for gy in range(0, H, 24): c.circle(gx, gy, .9, stroke=0, fill=1)
    logo(c, 60, 450, 40, colors.HexColor("#8FB2FF")); wordmark(c, 100, 462, 22, dark=True)
    c.setFont("PlexSB", 12); c.setFillColor(colors.HexColor("#8FB2FF")); c.drawString(60, 360, deck["kick"].upper())
    y = 318
    for line in deck["cover"]:
        c.setFont("Serif", 40); c.setFillColor(colors.white); c.drawString(60, y, line); y -= 48
    c.setFillColor(BLUE); c.rect(60, y + 18, 56, 4, stroke=0, fill=1)
    c.setFont("Plex", 16); c.setFillColor(colors.HexColor("#C9D6EA")); c.drawString(60, y - 14, deck["sub"])
    c.setFont("Plex", 11); c.setFillColor(colors.HexColor("#9FB0C5"))
    c.drawString(60, 52, f"{n} slide  ·  Tim UpdateSAK  ·  Diperbarui {UPD}  ·  updatesak.com")
    c.drawString(60, 34, "Bebas dipakai dan dibagikan untuk perkuliahan dengan mencantumkan sumber updatesak.com. Angka contoh adalah data ilustrasi.")


def closing(c, deck, i, n):
    chrome(c, deck, i, n)
    top = title(c, "Rangkuman dan Bahan Lanjutan", "Penutup")
    flow(c, deck["ringkas"], 48, top, 560, 300)
    url = deck["url"]
    w = qr.QrCodeWidget(url); b = w.getBounds(); s = 170
    d = Drawing(s, s, transform=[s / (b[2] - b[0]), 0, 0, s / (b[3] - b[1]), 0, 0]); d.add(w)
    c.setFillColor(PANEL); c.rect(660, 150, 252, 290, stroke=0, fill=1)
    renderPDF.draw(d, c, 701, 250)
    c.setFont("PlexSB", 12.5); c.setFillColor(NAVY); c.drawCentredString(786, 222, "Ringkasan, contoh CALK,")
    c.drawCentredString(786, 204, "dan latihan gratis")
    c.setFont("Plex", 11.5); c.setFillColor(BLUE); c.drawCentredString(786, 176, url.replace("https://", ""))


def render(deck, path):
    slides = deck["slides"]; n = len(slides) + 2
    assert n <= 8, deck["slug"]
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle(deck["judul"]); c.setAuthor("Tim UpdateSAK"); c.setSubject("Bahan ajar akuntansi, updatesak.com"); c.setCreator("updatesak.com")
    cover(c, deck, n); c.showPage()
    for k, sl in enumerate(slides, start=2):
        chrome(c, deck, k, n)
        top = title(c, sl["t"], sl.get("k"))
        sl["draw"](c, top) if "draw" in sl else flow(c, sl["b"], 48, top, 864, 300)
        c.showPage()
    closing(c, deck, n, n); c.showPage(); c.save()
    return n


# ======================= ISI =======================
def two(left, right, lt=None, rt=None):
    def d(c, top):
        y = top
        if lt: c.setFont("PlexSB", 13); c.setFillColor(BLUE); c.drawString(48, top, lt.upper()); c.drawString(500, top, rt.upper()); y = top - 22
        flow(c, left, 48, y, 410, 300, "small"); flow(c, right, 500, y, 412, 300, "small")
    return d


# ---------- 1. PSAK 118 ----------
LR = [("Pendapatan", 10000, "Operasi"), ("Beban pokok pendapatan", -6500, "Operasi"), ("Beban penjualan", -900, "Operasi"),
      ("Beban umum dan administrasi", -1100, "Operasi")]
OP = sum(v for _, v, _ in LR)
INV = [("Bagian laba entitas asosiasi", 120, "Investasi"), ("Penghasilan bunga deposito", 80, "Investasi")]
LSPP = OP + sum(v for _, v, _ in INV)
FIN = [("Beban bunga pinjaman bank", -300, "Pendanaan"), ("Beban bunga liabilitas sewa", -50, "Pendanaan")]
LSP = LSPP + sum(v for _, v, _ in FIN)
TAX = -round(LSP * 0.22)
NET = LSP + TAX


def lr118(c, top):
    rows = [(a, k, rp(v)) for a, v, k in LR] + [("Laba operasi", "Subtotal wajib", rp(OP))] + \
           [(a, k, rp(v)) for a, v, k in INV] + [("Laba sebelum pendanaan dan pajak penghasilan", "Subtotal wajib", rp(LSPP))] + \
           [(a, k, rp(v)) for a, v, k in FIN] + [("Laba sebelum pajak penghasilan", "", rp(LSP)), ("Beban pajak penghasilan (22%)", "Pajak", rp(TAX)), ("Laba tahun berjalan", "", rp(NET))]
    bold = [i for i, r in enumerate(rows) if r[1] == "Subtotal wajib" or r[0] == "Laba tahun berjalan"]
    table(c, ["Pos (dalam Rp juta, data ilustrasi)", "Kategori", "2027"], rows, [400, 140, 110], 48, top, bold, align_right=[2])
    note(c, "Bagian laba entitas asosiasi tidak lagi masuk laba operasi. Bunga liabilitas sewa masuk kategori pendanaan. Beban pajak = 22% × laba sebelum pajak.", 722, top, 190, "Perhatikan")


D118 = dict(slug="psak-118-penyajian-laporan-keuangan", short="PSAK 118", kick="Akuntansi Keuangan · Standar Baru 2027",
            judul="PSAK 118 Penyajian dan Pengungkapan dalam Laporan Keuangan", cover=["PSAK 118: Penyajian dan", "Pengungkapan Laporan Keuangan"],
            sub="Struktur laba rugi baru yang berlaku 1 Januari 2027", url="https://updatesak.com/psak/118/", psak=118,
            desk="Kategori laba rugi, subtotal wajib, ukuran kinerja manajemen (MPM), dan contoh angka.",
            slides=[
    dict(t="Latar Belakang dan Tanggal Berlaku", k="Konteks", draw=two(
        ["PSAK 118 adalah adopsi IFRS 18 oleh DSAK IAI.", "Menggantikan PSAK 201 Penyajian Laporan Keuangan.",
         "Berlaku untuk periode yang dimulai pada atau setelah 1 Januari 2027.", "Diterapkan retrospektif: angka komparatif 2026 disajikan ulang dalam format baru."],
        ["Laba rugi antarperusahaan sulit dibandingkan karena subtotal berbeda-beda.", "Angka seperti EBITDA atau laba disesuaikan tidak diatur dan tidak direkonsiliasi.",
         "Pos 'lain-lain' sering terlalu besar sehingga informasi hilang.", "PSAK 118 menjawab tiga masalah ini."],
        "Apa yang berubah", "Mengapa diubah")),
    dict(t="Lima Kategori Laba Rugi", k="Inti standar", draw=lambda c, top: table(c, ["Kategori", "Isi utama (entitas umum)", "Contoh pos"], [
        ("Operasi", "Kategori sisa: semua yang tidak masuk kategori lain, termasuk kegiatan usaha utama", "Pendapatan, beban pokok, beban usaha, penurunan nilai piutang"),
        ("Investasi", "Hasil dari aset yang menghasilkan imbal hasil secara terpisah dari sumber daya lain", "Bagian laba entitas asosiasi dan ventura bersama, bunga deposito, dividen"),
        ("Pendanaan", "Hasil liabilitas dari transaksi penggalangan dana, serta bunga atas liabilitas lain", "Bunga pinjaman bank dan obligasi, bunga liabilitas sewa"),
        ("Pajak penghasilan", "Beban atau penghasilan pajak sesuai PSAK 212", "Pajak kini dan pajak tangguhan"),
        ("Operasi dihentikan", "Sesuai PSAK 105", "Laba rugi operasi yang dihentikan")], [150, 380, 334], 48, top)),
    dict(t="Contoh Laporan Laba Rugi Format PSAK 118", k="Ilustrasi angka", draw=lr118),
    dict(t="Ukuran Kinerja yang Ditetapkan Manajemen", k="MPM", draw=two(
        ["Subtotal penghasilan dan beban yang dipakai manajemen di komunikasi publik di luar laporan keuangan.",
         "Mencerminkan pandangan manajemen atas kinerja dan tidak ditetapkan oleh standar.",
         "Contoh yang perlu dievaluasi: 'laba operasi disesuaikan' atau EBITDA versi perusahaan di rilis dan prospektus."],
        ["Diungkapkan dalam satu catatan di CALK.", "Direkonsiliasi ke subtotal paling mirip yang diatur PSAK.",
         "Dampak pajak dan kepentingan nonpengendali untuk tiap pos rekonsiliasi.", "Penjelasan mengapa ukuran itu berguna dan bagaimana dihitung."],
        "Definisi", "Kewajiban pengungkapan")),
    dict(t="Agregasi, Disagregasi, dan Arus Kas", k="Perubahan lain", draw=two(
        ["Pos dikelompokkan berdasarkan karakteristik yang sama; dipisah bila karakteristiknya berbeda.",
         "Label 'lain-lain' hanya boleh bila tidak ada label yang lebih informatif.",
         "Beban operasi yang disajikan per fungsi wajib dilengkapi rincian per sifat tertentu di CALK."],
        ["Metode tidak langsung dimulai dari laba operasi.", "Bunga dan dividen dibayar masuk arus kas pendanaan.",
         "Bunga dan dividen diterima masuk arus kas investasi.", "Berlaku untuk entitas yang kegiatan utamanya bukan investasi atau pembiayaan."],
        "Laporan keuangan dan CALK", "Laporan arus kas (PSAK 207)")),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "PT A memiliki pinjaman bank dan liabilitas sewa gedung. Ke kategori mana masing-masing beban bunganya, dan mengapa?",
        "Direksi menyebut 'EBITDA disesuaikan' di paparan publik. Apa saja yang wajib diungkapkan di CALK?",
        "Susun ulang laba rugi 2026 sebuah emiten di BEI ke format PSAK 118. Subtotal apa yang berubah dibanding laporan aslinya?"]),
], ringkas=["PSAK 118 berlaku 1 Januari 2027, retrospektif, menggantikan PSAK 201.",
            "Lima kategori: operasi, investasi, pendanaan, pajak penghasilan, operasi dihentikan.",
            "Dua subtotal wajib: laba operasi serta laba sebelum pendanaan dan pajak penghasilan.",
            "MPM diungkapkan dan direkonsiliasi di satu catatan CALK."])

# ---------- 2. Penomoran PSAK ----------
from seo_psak import P as _P
MAP = [(p[0], p[3], p[1]) for p in _P if p[3]]


def maptab(lo, hi, extra=()):
    rows = [(f"PSAK {o.replace('PSAK ', '')}", f"PSAK {n}", t) for n, o, t in MAP if lo <= n < hi] + list(extra)
    return lambda c, top: table(c, ["Nomor lama", "Nomor baru", "Judul standar"], rows, [130, 130, 604], 48, top)


MAP1 = [m for m in MAP if 100 <= m[0] < 200]; MAP2 = [m for m in MAP if 200 <= m[0] < 300]
half = (len(MAP2) + 1) // 2
D_NUM = dict(slug="penomoran-psak-baru", short="Penomoran PSAK", kick="Akuntansi Keuangan · Dasar Standar",
             judul="Penomoran PSAK Baru: Seri 100 sampai 400 dan Tabel Konversi", cover=["Penomoran PSAK Baru:", "Seri 100 sampai 400"],
             sub="Membaca nomor PSAK 3 digit dan padanan nomor lamanya", url="https://updatesak.com/penomoran-psak-baru/", psak=None,
             desk="Logika seri 1xx, 2xx, 3xx, 4xx dan tabel konversi nomor lama ke nomor baru.",
             slides=[
    dict(t="Mengapa Nomor PSAK Berubah", k="Konteks", b=[
        "Sejak 1 Januari 2024 DSAK IAI memakai penomoran 3 digit untuk PSAK.",
        "Isi standar tidak berubah karena penomoran; yang berubah hanya nomor rujukannya.",
        "Nomor baru langsung menunjukkan sumber standar: IFRS, IAS, atau khusus Indonesia.",
        "Soal ujian CA dan CPA serta laporan auditor kini memakai nomor baru."]),
    dict(t="Logika Empat Seri", k="Aturan dasar", draw=lambda c, top: table(c, ["Seri", "Sumber", "Pola", "Contoh"], [
        ("1xx", "IFRS", "100 + nomor IFRS", "IFRS 15 menjadi PSAK 115"),
        ("2xx", "IAS", "200 + nomor IAS", "IAS 16 menjadi PSAK 216"),
        ("3xx", "Khusus Indonesia (non-IFRS)", "Nomor tersendiri", "PSAK 338 Kombinasi Bisnis Entitas Sepengendali"),
        ("4xx", "Akuntansi syariah", "Seri 400", "PSAK 401 Penyajian Laporan Keuangan Syariah")], [90, 240, 210, 324], 48, top)),
    dict(t="Konversi Seri 100 (Berbasis IFRS)", k="Tabel 1", draw=maptab(100, 200)),
    dict(t="Konversi Seri 200 (Berbasis IAS), Bagian 1", k="Tabel 2", draw=lambda c, top: table(c, ["Nomor lama", "Nomor baru", "Judul standar"],
         [(o, f"PSAK {n}", t) for n, o, t in MAP2[:half]], [130, 130, 604], 48, top)),
    dict(t="Konversi Seri 200 Bagian 2 dan Seri 300", k="Tabel 3", draw=lambda c, top: table(c, ["Nomor lama", "Nomor baru", "Judul standar"],
         [(o, f"PSAK {n}", t) for n, o, t in MAP2[half:]] + [(o, f"PSAK {n}", t) for n, o, t in MAP if n >= 300], [130, 130, 604], 48, top)),
    dict(t="Latihan Cepat", k="Kuis kelas", b=[
        "IAS 37 Provisi, Liabilitas Kontinjensi, dan Aset Kontinjensi menjadi PSAK nomor berapa?",
        "Mahasiswa menulis 'PSAK 73 Sewa' di tugas tahun 2026. Bagaimana menuliskan yang benar?",
        "Sebutkan seri untuk standar yang tidak punya padanan IFRS. Beri satu contoh.",
        "Kunci: PSAK 237; PSAK 116 Sewa (dahulu PSAK 73); seri 3xx, misalnya PSAK 338."]),
], ringkas=["Penomoran 3 digit berlaku sejak 1 Januari 2024; isi standar tetap.",
            "1xx = IFRS, 2xx = IAS, 3xx = khusus Indonesia, 4xx = syariah.",
            "Gunakan nomor baru di tugas, skripsi, dan soal; sebut nomor lama dalam kurung bila perlu."])

# ---------- 3. PSAK 116 ----------
PAY, R, N = 100_000_000, 0.10, 5
PV = sum(PAY / (1 + R) ** t for t in range(1, N + 1))
SCHED = []
o = PV
for t in range(1, N + 1):
    i_ = o * R; cl = o + i_ - PAY; SCHED.append((t, o, i_, PAY, max(cl, 0))); o = cl
DEP = PV / N


def sewa_tab(c, top):
    rows = [(f"Tahun {t}", rp(a), rp(b), rp(-p), rp(d)) for t, a, b, p, d in SCHED]
    y = table(c, ["Tahun", "Saldo awal", "Bunga 10%", "Pembayaran", "Saldo akhir"], rows, [130, 190, 170, 180, 194], 48, top, align_right=[1, 2, 3, 4])
    note(c, f"Penyusutan aset hak guna per tahun = {rp(PV)} / 5 = {rp(DEP)}. Beban tahun 1 = bunga {rp(SCHED[0][2])} + penyusutan {rp(DEP)}.", 48, y - 14, 864, "Penyusutan")


D116 = dict(slug="psak-116-sewa-penyewa", short="PSAK 116", kick="Akuntansi Keuangan · Sewa",
            judul="PSAK 116 Sewa: Akuntansi Penyewa", cover=["PSAK 116 Sewa:", "Akuntansi Penyewa"],
            sub="Aset hak guna, liabilitas sewa, dan tabel amortisasi", url="https://updatesak.com/psak/116/", psak=116,
            desk="Pengakuan aset hak guna dan liabilitas sewa, pengecualian, dan contoh perhitungan 5 tahun.",
            slides=[
    dict(t="Tujuan Pembelajaran", k="Pertemuan ini", b=[
        "Menjelaskan model tunggal akuntansi penyewa dalam PSAK 116 (dahulu PSAK 73, adopsi IFRS 16).",
        "Mengukur liabilitas sewa pada nilai kini pembayaran sewa.",
        "Menyusun tabel amortisasi liabilitas sewa dan menghitung penyusutan aset hak guna.",
        "Menerapkan pengecualian sewa jangka pendek dan aset bernilai rendah."]),
    dict(t="Model Penyewa", k="Konsep", draw=two(
        ["Aset hak guna: hak menggunakan aset selama masa sewa.", "Liabilitas sewa: kewajiban membayar sewa.",
         "Diukur awal pada nilai kini pembayaran sewa yang belum dibayar.", "Tingkat diskonto: suku bunga implisit, atau suku bunga pinjaman inkremental penyewa."],
        ["Sewa jangka pendek: masa sewa 12 bulan atau kurang.", "Sewa aset bernilai rendah, misalnya laptop dan perabot kecil.",
         "Untuk keduanya penyewa boleh membebankan pembayaran secara garis lurus.", "Pesewa tetap membedakan sewa pembiayaan dan sewa operasi."],
        "Yang diakui di neraca", "Pengecualian")),
    dict(t="Kasus: Sewa Gudang 5 Tahun", k="Data ilustrasi", b=[
        f"PT Contoh menyewa gudang 5 tahun, sewa Rp{rp(PAY)} dibayar setiap akhir tahun.",
        "Suku bunga pinjaman inkremental 10% per tahun; tidak ada biaya langsung awal.",
        f"Nilai kini = Rp{rp(PAY)} × faktor anuitas 5 tahun 10% ({(1 - 1.1 ** -5) / 0.1:.4f}) = <b>Rp{rp(PV)}</b>.",
        f"Jurnal awal: Dr Aset Hak Guna Rp{rp(PV)} / Cr Liabilitas Sewa Rp{rp(PV)}."]),
    dict(t="Tabel Amortisasi Liabilitas Sewa", k="Perhitungan", draw=sewa_tab),
    dict(t="Jurnal Tahun Pertama", k="Pencatatan", draw=lambda c, top: table(c, ["Transaksi", "Debit", "Kredit", "Jumlah (Rp)"], [
        ("Pengakuan awal", "Aset hak guna", "Liabilitas sewa", rp(PV)),
        ("Bunga tahun 1", "Beban bunga", "Liabilitas sewa", rp(SCHED[0][2])),
        ("Pembayaran sewa", "Liabilitas sewa", "Kas", rp(PAY)),
        ("Penyusutan tahun 1", "Beban penyusutan", "Akumulasi penyusutan aset hak guna", rp(DEP))], [210, 200, 290, 164], 48, top, align_right=[3])),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "Sewa ruko 3 tahun dibayar di muka sekaligus. Bagaimana pencatatan menurut PSAK 116 dibanding mencatat sebagai biaya dibayar di muka?",
        "Kontrak memberi opsi perpanjangan 2 tahun yang hampir pasti dipakai. Apa dampaknya pada liabilitas sewa?",
        "Bandingkan beban di laba rugi tahun 1 dan tahun 5 pada kasus gudang. Mengapa polanya menurun?"]),
], ringkas=["Penyewa mengakui aset hak guna dan liabilitas sewa untuk hampir semua sewa.",
            "Liabilitas = nilai kini pembayaran; bunga menurun seiring saldo turun.",
            "Aset hak guna disusutkan; pengecualian untuk jangka pendek dan bernilai rendah.",
            "Opsi perpanjangan yang cukup pasti ikut diperhitungkan."])

# ---------- 4. PSAK 115 ----------
SSP = [("Mesin", 100_000_000), ("Instalasi", 10_000_000), ("Servis 2 tahun", 20_000_000)]
PRICE = 120_000_000
TOT = sum(v for _, v in SSP)
ALLOC = [(a, v, PRICE * v / TOT) for a, v in SSP]


def alloc_tab(c, top):
    rows = [(a, rp(v), f"{v / TOT * 100:.2f}%".replace(".", ","), rp(x)) for a, v, x in ALLOC] + [("Total", rp(TOT), "100%", rp(PRICE))]
    y = table(c, ["Kewajiban pelaksanaan", "Harga jual berdiri sendiri", "Porsi", "Alokasi harga transaksi"], rows, [250, 230, 120, 264], 48, top, bold_rows=[3], align_right=[1, 2, 3])
    note(c, f"Mesin dan instalasi diakui saat serah terima dan instalasi selesai. Servis Rp{rp(ALLOC[2][2])} diakui sepanjang 24 bulan, sekitar Rp{rp(ALLOC[2][2] / 24)} per bulan.", 48, y - 14, 864, "Pengakuan")


D115 = dict(slug="psak-115-pendapatan-lima-langkah", short="PSAK 115", kick="Akuntansi Keuangan · Pendapatan",
            judul="PSAK 115 Pendapatan dari Kontrak dengan Pelanggan", cover=["PSAK 115: Pendapatan dari", "Kontrak dengan Pelanggan"],
            sub="Model lima langkah dan alokasi harga transaksi", url="https://updatesak.com/psak/115/", psak=115,
            desk="Model lima langkah, pengakuan pada titik waktu atau sepanjang waktu, dan contoh alokasi harga.",
            slides=[
    dict(t="Tujuan Pembelajaran", k="Pertemuan ini", b=[
        "Menerapkan model lima langkah PSAK 115 (dahulu PSAK 72, adopsi IFRS 15).",
        "Mengidentifikasi kewajiban pelaksanaan dalam satu kontrak.",
        "Mengalokasikan harga transaksi berdasarkan harga jual berdiri sendiri.",
        "Membedakan pengakuan pada titik waktu dan sepanjang waktu."]),
    dict(t="Model Lima Langkah", k="Kerangka", draw=lambda c, top: table(c, ["Langkah", "Pertanyaan kunci"], [
        ("1. Identifikasi kontrak", "Apakah ada kontrak yang menimbulkan hak dan kewajiban yang dapat dipaksakan?"),
        ("2. Identifikasi kewajiban pelaksanaan", "Barang atau jasa apa saja yang dijanjikan dan dapat dibedakan?"),
        ("3. Tentukan harga transaksi", "Berapa imbalan yang diharapkan, termasuk imbalan variabel yang dibatasi?"),
        ("4. Alokasikan harga transaksi", "Berapa porsi harga untuk tiap kewajiban pelaksanaan?"),
        ("5. Akui pendapatan", "Kapan kendali beralih: pada titik waktu atau sepanjang waktu?")], [300, 564], 48, top)),
    dict(t="Kasus: Paket Mesin, Instalasi, dan Servis", k="Data ilustrasi", b=[
        f"PT Contoh menjual paket seharga Rp{rp(PRICE)}: mesin, instalasi, dan servis 2 tahun.",
        "Ketiganya dapat dibedakan: pelanggan bisa memakai mesin dan membeli instalasi atau servis dari pihak lain.",
        "Maka ada tiga kewajiban pelaksanaan.",
        f"Harga jual berdiri sendiri: mesin Rp{rp(SSP[0][1])}, instalasi Rp{rp(SSP[1][1])}, servis Rp{rp(SSP[2][1])}. Total Rp{rp(TOT)}, ada diskon paket Rp{rp(TOT - PRICE)}."]),
    dict(t="Alokasi Harga Transaksi", k="Perhitungan", draw=alloc_tab),
    dict(t="Titik Waktu atau Sepanjang Waktu", k="Langkah 5", draw=two(
        ["Pelanggan menerima dan memakai manfaat saat entitas melaksanakan, misalnya jasa servis.",
         "Pekerjaan entitas menciptakan atau meningkatkan aset yang dikendalikan pelanggan.",
         "Aset tidak punya penggunaan alternatif dan entitas berhak atas pembayaran atas pekerjaan yang telah selesai, contohnya kontrak konstruksi."],
        ["Bila tidak ada kriteria sepanjang waktu yang terpenuhi, pendapatan diakui pada titik waktu.",
         "Indikator: hak atas pembayaran, kepemilikan legal, penguasaan fisik, risiko dan manfaat, penerimaan pelanggan.",
         "Aset kontrak dan liabilitas kontrak disajikan terpisah dari piutang."],
        "Sepanjang waktu bila", "Pada titik waktu")),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "Kontraktor menagih sesuai termin, padahal progres fisik sudah 60%. Berapa pendapatan yang seharusnya diakui?",
        "Penjual memberi diskon volume bila pelanggan membeli di atas target tahunan. Bagaimana perlakuan imbalan variabelnya?",
        "Pada kasus paket mesin, berapa liabilitas kontrak per akhir tahun pertama bila seluruh harga diterima di awal?"]),
], ringkas=["Lima langkah: kontrak, kewajiban pelaksanaan, harga, alokasi, pengakuan.",
            "Harga dialokasikan berdasarkan harga jual berdiri sendiri, termasuk diskon paket.",
            "Pendapatan diakui saat kendali beralih, pada titik waktu atau sepanjang waktu.",
            "Aset kontrak dan liabilitas kontrak disajikan terpisah dari piutang."])

# ---------- 5. PSAK 109 ECL ----------
AG = [("Belum jatuh tempo", 800, 0.005), ("Lewat 1 sampai 30 hari", 300, 0.02), ("Lewat 31 sampai 60 hari", 150, 0.05),
      ("Lewat 61 sampai 90 hari", 80, 0.12), ("Lewat lebih dari 90 hari", 70, 0.40)]
ECL = sum(a * r for _, a, r in AG); OLD = 30.0


def ecl_tab(c, top):
    rows = [(k, rp(a), f"{r * 100:.1f}%".replace(".", ","), rp(a * r, 1)) for k, a, r in AG] + [("Total", rp(sum(a for _, a, _ in AG)), "", rp(ECL, 1))]
    y = table(c, ["Umur piutang", "Saldo (Rp juta)", "Tingkat kerugian", "Cadangan ECL (Rp juta)"], rows, [300, 190, 170, 204], 48, top, bold_rows=[5], align_right=[1, 2, 3])
    note(c, f"Saldo cadangan awal Rp{rp(OLD)} juta, kebutuhan Rp{rp(ECL, 1)} juta. Jurnal: Dr Beban Kerugian Penurunan Nilai Rp{rp(ECL - OLD, 1)} juta / Cr Cadangan Kerugian Penurunan Nilai Rp{rp(ECL - OLD, 1)} juta.", 48, y - 14, 864, "Penyesuaian")


D109 = dict(slug="psak-109-ecl-matriks-provisi", short="PSAK 109", kick="Akuntansi Keuangan · Instrumen Keuangan",
            judul="PSAK 109 Kerugian Kredit Ekspektasian dan Matriks Provisi", cover=["PSAK 109: Kerugian Kredit", "Ekspektasian (ECL)"],
            sub="Tiga tahap ECL dan matriks provisi piutang usaha", url="https://updatesak.com/psak/109/", psak=109,
            desk="Konsep ECL tiga tahap, pendekatan sederhana untuk piutang usaha, dan contoh matriks provisi.",
            slides=[
    dict(t="Tujuan Pembelajaran", k="Pertemuan ini", b=[
        "Menjelaskan perubahan dari model kerugian terjadi ke kerugian kredit ekspektasian (PSAK 109, dahulu PSAK 71, adopsi IFRS 9).",
        "Membedakan tiga tahap ECL dalam pendekatan umum.",
        "Menyusun matriks provisi untuk piutang usaha dengan pendekatan sederhana.",
        "Mencatat jurnal penyesuaian cadangan kerugian penurunan nilai."]),
    dict(t="Pendekatan Umum: Tiga Tahap", k="Konsep", draw=lambda c, top: table(c, ["Tahap", "Kondisi risiko kredit", "ECL yang diakui", "Dasar bunga"], [
        ("Tahap 1", "Tidak meningkat signifikan sejak pengakuan awal", "ECL 12 bulan", "Jumlah tercatat bruto"),
        ("Tahap 2", "Meningkat signifikan sejak pengakuan awal", "ECL sepanjang umur", "Jumlah tercatat bruto"),
        ("Tahap 3", "Mengalami penurunan nilai kredit", "ECL sepanjang umur", "Biaya perolehan diamortisasi (neto)")], [110, 330, 200, 224], 48, top)),
    dict(t="Pendekatan Sederhana untuk Piutang Usaha", k="Praktik", b=[
        "Untuk piutang usaha dan aset kontrak tanpa komponen pendanaan signifikan, entitas mengakui ECL sepanjang umur sejak awal.",
        "Tidak perlu menilai perpindahan tahap.",
        "Alat praktis yang umum: matriks provisi berdasarkan umur piutang.",
        "Tingkat kerugian historis disesuaikan dengan informasi masa depan, misalnya proyeksi ekonomi sektor pelanggan."]),
    dict(t="Contoh Matriks Provisi", k="Data ilustrasi", draw=ecl_tab),
    dict(t="Temuan Auditor yang Sering Muncul", k="Praktik audit", b=[
        "Cadangan dihitung dengan persentase tetap tanpa data historis dan informasi masa depan.",
        "Tingkat kerugian tidak diperbarui bertahun-tahun.",
        "Piutang pihak berelasi tanpa bunga tidak diukur pada nilai kini.",
        "Pengungkapan risiko kredit di CALK (PSAK 107) tidak memadai."]),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "Bila tingkat kerugian kelompok lewat lebih dari 90 hari naik menjadi 50%, berapa tambahan cadangan pada contoh?",
        "Informasi masa depan apa yang relevan bagi distributor yang pelanggannya kontraktor?",
        "Kapan piutang dihapusbukukan dan bagaimana jurnalnya terhadap cadangan?"]),
], ringkas=["ECL melihat ke depan: kerugian diakui sebelum gagal bayar terjadi.",
            "Pendekatan umum tiga tahap; piutang usaha boleh pendekatan sederhana.",
            "Matriks provisi: saldo per umur × tingkat kerugian yang disesuaikan.",
            "Selisih dengan saldo cadangan dicatat sebagai beban penurunan nilai."])

# ---------- 6. Arus kas ----------
CF_OP = [("Laba sebelum pajak", 500), ("Penyusutan", 120), ("Beban bunga", 40), ("Kenaikan piutang usaha", -80),
         ("Kenaikan persediaan", -50), ("Kenaikan utang usaha", 30)]
KAS_OP = sum(v for _, v in CF_OP)
CF_OP2 = [("Bunga dibayar", -40), ("Pajak penghasilan dibayar", -110)]
NET_OP = KAS_OP + sum(v for _, v in CF_OP2)
CF_INV = [("Pembelian aset tetap", -300), ("Penjualan aset tetap", 20)]
CF_FIN = [("Penerimaan pinjaman bank", 200), ("Pembayaran pinjaman bank", -150), ("Dividen dibayar", -60)]
NI, NF = sum(v for _, v in CF_INV), sum(v for _, v in CF_FIN)
KAS0 = 230; CHG = NET_OP + NI + NF; KAS1 = KAS0 + CHG


def cf_tab(c, top):
    rows = [(a, rp(v)) for a, v in CF_OP] + [("Kas dihasilkan dari operasi", rp(KAS_OP))] + [(a, rp(v)) for a, v in CF_OP2] + \
           [("Arus kas neto dari aktivitas operasi", rp(NET_OP))]
    b = [6, 9]
    table(c, ["Aktivitas operasi (Rp juta)", "2026"], rows, [330, 110], 48, top, bold_rows=b, align_right=[1])
    rows2 = [(a, rp(v)) for a, v in CF_INV] + [("Arus kas neto aktivitas investasi", rp(NI))] + [(a, rp(v)) for a, v in CF_FIN] + \
            [("Arus kas neto aktivitas pendanaan", rp(NF)), ("Kenaikan kas dan setara kas", rp(CHG)), ("Kas awal tahun", rp(KAS0)), ("Kas akhir tahun", rp(KAS1))]
    table(c, ["Investasi dan pendanaan", "2026"], rows2, [314, 110], 488, top, bold_rows=[2, 6, 7, 9], align_right=[1])


DCF = dict(slug="laporan-arus-kas-metode-tidak-langsung", short="PSAK 207", kick="Akuntansi Keuangan · Laporan Arus Kas",
           judul="Laporan Arus Kas Metode Tidak Langsung (PSAK 207)", cover=["Laporan Arus Kas Metode", "Tidak Langsung"],
           sub="Rekonsiliasi laba ke kas operasi dan perubahan karena PSAK 118", url="https://updatesak.com/psak/207/", psak=207,
           desk="Tiga aktivitas arus kas, penyesuaian nonkas dan modal kerja, contoh lengkap, dan dampak PSAK 118.",
           slides=[
    dict(t="Tujuan Pembelajaran", k="Pertemuan ini", b=[
        "Mengklasifikasikan arus kas ke aktivitas operasi, investasi, dan pendanaan (PSAK 207, dahulu PSAK 2, adopsi IAS 7).",
        "Menyusun arus kas operasi metode tidak langsung dari laba.",
        "Mengenali transaksi nonkas yang tidak masuk laporan arus kas.",
        "Memahami perubahan klasifikasi bunga dan dividen mulai 2027."]),
    dict(t="Langkah Metode Tidak Langsung", k="Prosedur", b=[
        "Mulai dari laba sebelum pajak (mulai 2027: dari laba operasi).",
        "Tambahkan kembali beban nonkas: penyusutan, amortisasi, penurunan nilai.",
        "Keluarkan pos yang bukan operasi, seperti beban bunga atau laba penjualan aset tetap.",
        "Sesuaikan perubahan modal kerja: kenaikan aset lancar mengurangi kas, kenaikan liabilitas lancar menambah kas.",
        "Kurangi bunga dan pajak yang dibayar sesuai kebijakan klasifikasi entitas."]),
    dict(t="Contoh Laporan Arus Kas", k="Data ilustrasi", draw=cf_tab),
    dict(t="Kesalahan yang Sering Ditemukan", k="Praktik audit", b=[
        "Kas akhir di laporan arus kas tidak sama dengan kas di neraca.",
        "Pembelian aset tetap secara utang dicatat sebagai arus kas keluar investasi; seharusnya diungkapkan sebagai transaksi nonkas.",
        "Rekonsiliasi liabilitas yang timbul dari aktivitas pendanaan tidak disajikan.",
        "Deposito jatuh tempo lebih dari tiga bulan dimasukkan ke setara kas."]),
    dict(t="Perubahan Mulai 2027 karena PSAK 118", k="Pembaruan", draw=two(
        ["Titik awal metode tidak langsung bisa dari laba sebelum pajak atau laba neto.",
         "Bunga dan dividen dibayar atau diterima boleh dipilih klasifikasinya, asalkan konsisten."],
        ["Titik awal metode tidak langsung adalah laba operasi.", "Bunga dan dividen dibayar masuk aktivitas pendanaan.",
         "Bunga dan dividen diterima masuk aktivitas investasi.", "Berlaku untuk entitas yang kegiatan utamanya bukan investasi atau pembiayaan."],
        "Sebelum (PSAK 207 saat ini)", "Mulai 1 Januari 2027")),
    dict(t="Soal Diskusi Kelas", k="Latihan", b=[
        "Pada contoh, perusahaan membeli mesin Rp100 juta secara kredit dari pemasok. Apakah arus kas investasi berubah? Bagaimana pengungkapannya?",
        "Susun ulang arus kas operasi contoh dengan titik awal laba operasi dan bunga dibayar di aktivitas pendanaan. Berapa arus kas operasi neto yang baru?",
        "Mengapa arus kas operasi bisa negatif padahal perusahaan membukukan laba?"]),
], ringkas=["Arus kas dikelompokkan ke aktivitas operasi, investasi, dan pendanaan.",
            "Metode tidak langsung merekonsiliasi laba ke kas dari operasi.",
            "Transaksi nonkas diungkapkan, bukan disajikan di arus kas.",
            "Mulai 2027 titik awal dan klasifikasi bunga serta dividen berubah mengikuti PSAK 118."])

DECKS = [D118, D_NUM, D116, D115, D109, DCF]


def build(outdir):
    os.makedirs(outdir, exist_ok=True); res = []
    for d in DECKS:
        p = os.path.join(outdir, d["slug"] + ".pdf"); n = render(d, p); res.append((d, n))
    return res


if __name__ == "__main__":
    import sys
    for d, n in build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/slides"): print(d["slug"], n)
