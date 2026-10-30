# Tab Materi UpdateSAK: studi kasus (HTML + PDF) dan paket PDF ringkas. Dipanggil prep.py setelah build_seo.py.
import os, re, json, html, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_seo as B
from seo_materi import K, CHEAT, CHECKLIST, PBC, G7CHECK
from seo_psak import P
esc = html.escape
SITE = B.SITE; BASE = B.BASE
PDFDIR = os.path.join(SITE, "materi", "pdf"); os.makedirs(PDFDIR, exist_ok=True)
NAV_OLD = '<a href="/eksplor/" aria-current="page">Eksplor</a><a href="/materi/">Materi</a>'
NAV_NEW = '<a href="/eksplor/">Eksplor</a><a href="/materi/" aria-current="page">Materi</a>'
HEAD = B.HEAD.replace(NAV_OLD, NAV_NEW)
LV = {"Auditor Junior": "aj", "Staf Akuntansi": "sa", "Manager Akuntansi": "ma", "Semua": "all"}
pages = []

# ---------- PDF ----------
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
F = os.path.join(HERE, "fonts")
# Gaya dokumen mengikuti format standar FA (NDA #1): kertas putih, Lora untuk isi, Poppins untuk label,
# header logo kiri + tagline miring kanan, garis tipis, footer merek + "Halaman X dari Y".
for _n, _f in [("Lora", "Lora-Regular.ttf"), ("LoraB", "Lora-Bold.ttf"), ("LoraI", "Lora-Italic.ttf"), ("LoraBI", "Lora-BoldItalic.ttf"),
               ("Pop", "Poppins-Light.ttf"), ("Qs", "Quicksand-Light.ttf"), ("PopM", "Poppins-Medium.ttf"), ("PopSB", "Poppins-SemiBold.ttf")]:
    pdfmetrics.registerFont(TTFont(_n, os.path.join(F, _f)))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Lora", normal="Lora", bold="LoraB", italic="LoraI", boldItalic="LoraBI")
INK, ACC, MUTED, LINE, SOFT, BRAND = colors.HexColor("#1E1E1E"), colors.HexColor("#00ABD6"), colors.HexColor("#6B6B6B"), colors.HexColor("#D9D9D9"), colors.HexColor("#F5F5F5"), colors.HexColor("#1F5BFF")
S = {
 "h1": ParagraphStyle("h1", fontName="LoraB", fontSize=18, leading=23, textColor=INK, spaceAfter=6),
 "h2": ParagraphStyle("h2", fontName="LoraB", fontSize=11.5, leading=15, textColor=INK, spaceBefore=12, spaceAfter=5),
 "kick": ParagraphStyle("k", fontName="PopM", fontSize=7.5, leading=11, textColor=ACC, spaceAfter=5),
 "p": ParagraphStyle("p", fontName="Lora", fontSize=9.8, leading=14.6, textColor=INK, spaceAfter=5, alignment=4),
 "li": ParagraphStyle("li", fontName="Lora", fontSize=9.8, leading=14.6, textColor=INK, leftIndent=14, bulletIndent=0, spaceAfter=3, bulletFontName="Lora"),
 "q": ParagraphStyle("q", fontName="LoraI", fontSize=9.8, leading=14.6, textColor=INK, backColor=SOFT, borderColor=ACC, borderWidth=0, borderPadding=(8, 10, 8, 10), leftIndent=6, rightIndent=6, spaceBefore=6, spaceAfter=10),
 "small": ParagraphStyle("s", fontName="Pop", fontSize=7.5, leading=10.5, textColor=MUTED),
 "cell": ParagraphStyle("c", fontName="Lora", fontSize=9, leading=12, textColor=INK),
 "cellb": ParagraphStyle("cb", fontName="LoraB", fontSize=9, leading=12, textColor=INK),
}
from reportlab.pdfgen import canvas as _cv
class _NumCanvas(_cv.Canvas):
    """Simpan semua halaman dulu supaya footer bisa menulis 'Halaman X dari Y'."""
    def __init__(self, *a, **k): super().__init__(*a, **k); self._pg = []
    def showPage(self): self._pg.append(dict(self.__dict__)); self._startPage()
    def save(self):
        n = len(self._pg)
        for st in self._pg:
            self.__dict__.update(st)
            self.setFont("Pop", 7); self.setFillColor(MUTED)
            self.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Halaman {self._pageNumber} dari {n}")
            super().showPage()
        super().save()
def _logo(c, x, ytop, h):
    """Logo UpdateSAK terbaru (sama dengan favicon/header situs): kotak garis tipis, U kiri atas, S kanan bawah."""
    k = h / 40.0; P = lambda X, Y: (x + X * k, ytop - Y * k)
    c.saveState(); c.setStrokeColor(BRAND); c.setLineCap(1); c.setLineJoin(1)
    c.setLineWidth(1.2 * k); c.rect(x + .6 * k, ytop - 39.4 * k, 28.8 * k, 38.8 * k, stroke=1, fill=0)
    c.setLineWidth(1.3 * k); p = c.beginPath()
    p.moveTo(*P(6.5, 8)); p.lineTo(*P(6.5, 14.2))
    p.arcTo(x + 6.5 * k, ytop - 17.4 * k, x + 12.9 * k, ytop - 11.0 * k, startAng=180, extent=180)
    p.lineTo(*P(12.9, 8)); c.drawPath(p, stroke=1, fill=0)
    p = c.beginPath(); p.moveTo(*P(24.2, 24.4))
    p.curveTo(*P(23.3, 23.2), *P(18.6, 22.8), *P(18.6, 25.8))
    p.curveTo(*P(18.6, 28.7), *P(24.7, 27.4), *P(24.7, 30.4))
    p.curveTo(*P(24.7, 33.5), *P(19.4, 33.2), *P(18.1, 31.6))
    c.drawPath(p, stroke=1, fill=0); c.restoreState()
def _page(c, d):
    W, H = A4; c.saveState()
    # header: logo US + wordmark (kiri), tagline miring + label kecil berjarak (kanan), garis tipis
    _logo(c, 18 * mm, H - 10 * mm, 9.6 * mm)
    c.setFont("Qs", 16); c.setFillColor(colors.HexColor("#0B1F33")); c.drawString(26.5 * mm, H - 17.2 * mm, "Update")
    c.setFillColor(BRAND); c.drawString(26.5 * mm + c.stringWidth("Update", "Qs", 16), H - 17.2 * mm, "SAK")
    c.setFont("LoraI", 9); c.setFillColor(MUTED); c.drawRightString(W - 18 * mm, H - 13.4 * mm, "Materi Latihan Akuntansi & Audit")
    c.setFont("PopM", 6.3); c.setFillColor(ACC)
    _t = "UPDATESAK.COM  ·  DATA DUMMY"; _w = c.stringWidth(_t, "PopM", 6.3) + 1.1 * (len(_t) - 1)
    _o = c.beginText(W - 18 * mm - _w, H - 17.6 * mm); _o.setFont("PopM", 6.3); _o.setCharSpace(1.1); _o.textOut(_t); _o.setCharSpace(0); c.drawText(_o)
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(18 * mm, H - 22 * mm, W - 18 * mm, H - 22 * mm)
    # footer: merek tebal + keterangan (kiri), judul dokumen (kanan); nomor halaman diisi _NumCanvas
    c.setStrokeColor(LINE); c.line(18 * mm, 18 * mm, W - 18 * mm, 18 * mm)
    c.setFillColor(INK); c.setFont("Qs", 8.5); c.drawString(18 * mm, 13.6 * mm, "Update"); c.setFillColor(BRAND); c.drawString(18 * mm + c.stringWidth("Update", "Qs", 8.5), 13.6 * mm, "SAK"); c.setFillColor(INK)
    c.setFillColor(MUTED); c.setFont("LoraI", 7.5); c.drawString(18 * mm + c.stringWidth("UpdateSAK", "Qs", 8.5) + 2 * mm, 13.6 * mm, "Materi Latihan Akuntansi & Audit")
    c.setFont("Pop", 6.5); c.drawString(18 * mm, 10 * mm, "www.updatesak.com  |  Data dummy untuk latihan  |  PSAK sesuai SAK Online IAI")
    _tt = (getattr(d, "title", "") or ""); _tt = _tt if len(_tt) <= 52 else _tt[:50].rsplit(" ", 1)[0] + " ..."
    c.setFont("LoraI", 7.3); c.drawRightString(W - 18 * mm, 13.6 * mm, _tt)
    c.restoreState()
def doc(path, title):
    d = BaseDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=28 * mm, bottomMargin=24 * mm, title=title, author="UpdateSAK", subject="Materi latihan akuntansi")
    d.addPageTemplates([PageTemplate(id="p", frames=[Frame(d.leftMargin, d.bottomMargin, d.width, d.height, id="f")], onPage=_page)])
    _b = d.build
    d.build = lambda st: _b(st, canvasmaker=_NumCanvas)
    return d
def tbl(head, rows, widths, num_cols=()):
    tot = sum(widths); widths = [w * (174 * mm) / tot for w in widths] if tot > 174 * mm else widths
    data = [[Paragraph(esc(h), S["cellb"]) for h in head]] + [[Paragraph(esc(str(x)), S["cell"]) for x in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), SOFT), ("LINEABOVE", (0, 0), (-1, 0), 0.8, INK), ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
          ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    for c in num_cols:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
        for r in range(len(data)): data[r][c].style = ParagraphStyle("r", parent=data[r][c].style, alignment=2)
    t.setStyle(TableStyle(st)); return t
def bullets(items, numbered=False):
    return [Paragraph(esc(x), S["li"], bulletText=(f"{i+1}." if numbered else "•")) for i, x in enumerate(items)]

def case_story(k, with_head=True):
    st = []
    if with_head:
        st += [Paragraph(" · ".join(k["level"]).upper() + "  |  " + " · ".join(f"PSAK {n}" for n in k["psak"]), S["kick"]), Paragraph(esc(k["judul"]), S["h1"]), Paragraph(esc(k["ringkas"]), S["p"])]
    st += [Paragraph("Bagian A · Fakta Kasus", S["h2"])] + bullets(k["fakta"])
    if k.get("tabel_fakta"):
        h, r = k["tabel_fakta"]; w = 174 * mm
        st += [Spacer(1, 4), tbl(h, r, [w * .55] + [w * .45 / (len(h) - 1)] * (len(h) - 1), num_cols=range(1, len(h)))]
    st += [Paragraph("Pertanyaan", S["h2"])] + bullets(k["pertanyaan"], True)
    st += [PageBreak(), Paragraph("Bagian B · Pembahasan", S["kick"]), Paragraph(esc(k["judul"]), S["h2"]), Paragraph("Analisis", S["h2"])] + [Paragraph(esc(x), S["p"]) for x in k["analisis"]]
    st += [Paragraph("Jurnal Penyesuaian (Rp juta)", S["h2"]), tbl(["Akun", "Debit", "Kredit"], [[("      " if len(j) > 3 else "") + j[0], j[1], j[2]] for j in k["jurnal"]], [110 * mm, 35 * mm, 35 * mm], (1, 2))]
    st += [Paragraph("Dampak ke Laporan Keuangan", S["h2"]), tbl(["Pos", "Sebelum", "Sesudah"], [list(d) for d in k["dampak"]], [100 * mm, 40 * mm, 40 * mm], (1, 2))]
    st += [Paragraph("Kalimat CALK", S["h2"]), Paragraph(esc(k["calk"]), S["q"])]
    st += [Paragraph("Prosedur Auditor", S["h2"])] + bullets(k["prosedur"])
    st += [Paragraph("Catatan untuk Manager Akuntansi", S["h2"])] + bullets(k["manager"])
    return st

def pdf_case(k):
    p = os.path.join(PDFDIR, k["slug"] + ".pdf")
    d = doc(p, k["judul"]); d.build(case_story(k))
def pdf_all():
    p = os.path.join(PDFDIR, "kumpulan-studi-kasus-updatesak.pdf")
    d = doc(p, "Kumpulan Studi Kasus Akuntansi dan Audit UpdateSAK")
    st = [Paragraph("KUMPULAN STUDI KASUS", S["kick"]), Paragraph(f"{len(K)} Studi Kasus Akuntansi dan Audit untuk Profesional", S["h1"]),
          Paragraph("Untuk auditor junior, staf akuntansi, dan manager akuntansi. Setiap kasus berisi fakta, pertanyaan, pembahasan, jurnal penyesuaian, dampak laporan keuangan, kalimat CALK, prosedur auditor, dan catatan manager.", S["p"]),
          tbl(["No", "Studi Kasus", "Untuk", "PSAK"], [[i + 1, k["judul"], ", ".join(k["level"]), ", ".join(map(str, k["psak"]))] for i, k in enumerate(K)], [10 * mm, 95 * mm, 45 * mm, 30 * mm]), PageBreak()]
    for i, k in enumerate(K):
        st += case_story(k) + ([PageBreak()] if i < len(K) - 1 else [])
    d.build(st)
def pdf_cheat(slug, title, desc):
    p = os.path.join(PDFDIR, slug + ".pdf"); d = doc(p, title)
    st = [Paragraph("PAKET RINGKAS UPDATESAK", S["kick"]), Paragraph(esc(title), S["h1"]), Paragraph(esc(desc), S["p"])]
    if slug == "checklist-tutup-buku-akhir-tahun":
        for g, items in CHECKLIST:
            st.append(KeepTogether([Paragraph(esc(g), S["h2"]), tbl(["", "Langkah", "PIC", "Selesai"], [["[  ]", x, "", ""] for x in items], [10 * mm, 120 * mm, 25 * mm, 25 * mm])]))
    elif slug == "daftar-pbc-audit":
        for g, items in PBC:
            st.append(KeepTogether([Paragraph(esc(g), S["h2"]), tbl(["", "Dokumen", "Status", "Catatan"], [["[  ]", x, "", ""] for x in items], [10 * mm, 110 * mm, 25 * mm, 35 * mm])]))
    elif slug == "checklist-pengungkapan-viii-g7":
        st.append(Paragraph("Dasar: Keputusan Ketua Bapepam-LK Nomor KEP-347/BL/2012 tanggal 25 Juni 2012 (Peraturan VIII.G.7). Ketentuan A.4: bila SAK berubah, emiten mengikuti SAK terkini.", S["p"]))
        for g, items in G7CHECK:
            st.append(Paragraph(esc(g), S["h2"])); st.append(tbl(["", "Ketentuan", "Ada", "Catatan"], [["[  ]", x, "", ""] for x in items], [10 * mm, 120 * mm, 18 * mm, 32 * mm]))
    elif slug == "peta-psak-2026":
        st.append(tbl(["PSAK", "Judul", "Padanan", "Inti Pengaturan"], [[q[0], q[1], q[2] or "Khusus Indonesia", q[4]] for q in P], [14 * mm, 45 * mm, 22 * mm, 99 * mm]))
    else:
        for q in P:
            st.append(KeepTogether([Paragraph(f"PSAK {q[0]} {esc(q[1])}", S["h2"]), Paragraph(esc(q[6]), S["q"])]))
    d.build(st)

# ---------- HTML ----------
def tags(levels):
    return "".join(f'<span class="tag t-{LV.get(l, "all")}">{esc(l)}</span>' for l in levels)
def dl(href, label="Download PDF"):
    return f'<a class="btn btn-sm dl" href="{href}" download>{esc(label)}</a>'

def case_page(k):
    url = f"{BASE}/materi/{k['slug']}/"; key = "mat-" + k["slug"]; img = f"{BASE}/img/share/{key}-og.jpg"
    pdf = f"/materi/pdf/{k['slug']}.pdf"
    tf = ""
    if k.get("tabel_fakta"):
        h, r = k["tabel_fakta"]
        tf = '<div class="scroll"><table class="tbl"><thead><tr>' + "".join(f'<th{" class=r" if i else ""}>{esc(x)}</th>' for i, x in enumerate(h)) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f'<td{" class=r" if i else ""}>{esc(c)}</td>' for i, c in enumerate(row)) + "</tr>" for row in r) + "</tbody></table></div>"
    jr = "".join(f'<tr><td{" class=i" if len(j) > 3 else ""}>{esc(j[0])}</td><td class="r">{esc(j[1])}</td><td class="r">{esc(j[2])}</td></tr>' for j in k["jurnal"])
    dp = "".join(f'<tr><td>{esc(a)}</td><td class="r">{esc(b)}</td><td class="r">{esc(c)}</td></tr>' for a, b, c in k["dampak"])
    body = f'''<article class="art"><div class="wrap">
<nav class="crumb"><a href="/">Beranda</a> / <a href="/materi/">Materi</a> / Studi Kasus</nav>
<div class="tags">{tags(k["level"])}</div>
<h1>{esc(k["judul"])}</h1>
<p class="lede">{esc(k["ringkas"])}</p>
<div class="actions">{dl(pdf, "Download PDF Soal dan Pembahasan")}</div>
{B.share(url, k["judul"], key)}
<h2>Fakta Kasus</h2>
<ul class="facts">{"".join(f"<li>{esc(x)}</li>" for x in k["fakta"])}</ul>
{tf}
<h2>Pertanyaan</h2>
<ol class="qs">{"".join(f"<li>{esc(x)}</li>" for x in k["pertanyaan"])}</ol>
<details class="solve"><summary>Lihat Pembahasan</summary>
<h3>Analisis</h3>{"".join(f"<p>{esc(x)}</p>" for x in k["analisis"])}
<h3>Jurnal Penyesuaian (Rp juta)</h3><div class="scroll"><table class="tbl"><thead><tr><th>Akun</th><th class="r">Debit</th><th class="r">Kredit</th></tr></thead><tbody>{jr}</tbody></table></div>
<h3>Dampak ke Laporan Keuangan</h3><div class="scroll"><table class="tbl"><thead><tr><th>Pos</th><th class="r">Sebelum</th><th class="r">Sesudah</th></tr></thead><tbody>{dp}</tbody></table></div>
<h3>Kalimat CALK</h3><blockquote class="calk">{esc(k["calk"])}</blockquote>
<div class="two"><div><h3>Prosedur Auditor</h3><ul class="flags ok">{"".join(f"<li>{esc(x)}</li>" for x in k["prosedur"])}</ul></div>
<div><h3>Catatan Manager Akuntansi</h3><ul class="flags ok">{"".join(f"<li>{esc(x)}</li>" for x in k["manager"])}</ul></div></div>
</details>
<h2>Standar Terkait</h2><div class="pchips">{"".join(B.chip(n) for n in k["psak"])}</div>
{B.cta("Cek Kasus Serupa di Perusahaan Anda")}
{B.wa_box("Pelatihan dan Review Laporan Keuangan")}
</div></article>
'''
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "LearningResource", "name": k["judul"], "description": k["ringkas"], "url": url, "inLanguage": "id", "learningResourceType": "Studi Kasus",
         "educationalLevel": ", ".join(k["level"]), "isAccessibleForFree": True, "image": img, "about": [f"PSAK {n}" for n in k["psak"]],
         "provider": {"@type": "Organization", "name": "UpdateSAK", "url": BASE + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "UpdateSAK", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": "Materi", "item": BASE + "/materi/"}, {"@type": "ListItem", "position": 3, "name": k["judul"], "item": url}]}]}, ensure_ascii=False)
    title = k["judul"] + " | Studi Kasus UpdateSAK"
    B.write(f"materi/{k['slug']}", HEAD.format(title=esc(title), desc=esc(k["ringkas"]), url=url, ogt=esc(k["judul"]), img=img, ld=ld) + body + B.FOOT)
    B.make_images(key, "Studi Kasus · " + " · ".join(f"PSAK {n}" for n in k["psak"][:2]), k["judul"])
    pages.append(url)

def hub():
    url = BASE + "/materi/"
    cards = "".join(f'''<article class="mcard" data-lv="{" ".join(LV[l] for l in k["level"])}">
<div class="tags">{tags(k["level"])}</div><h3><a href="/materi/{k["slug"]}/">{esc(k["judul"])}</a></h3><p>{esc(k["ringkas"])}</p>
<div class="psaks">{"".join(f'<a href="/psak/{n}/">PSAK {n}</a>' for n in k["psak"])}</div>
<div class="row"><a class="btn btn-sm btn-ghost" href="/materi/{k["slug"]}/">Baca Studi Kasus</a>{dl(f"/materi/pdf/{k['slug']}.pdf", "PDF")}</div></article>''' for k in K)
    cheats = "".join(f'''<article class="mcard pdf" data-lv="{" ".join(LV[l] for l in lv)}"><div class="pdfic">PDF</div><div class="tags">{tags(lv)}</div><h3>{esc(t)}</h3><p>{esc(d)}</p><div class="row">{dl(f"/materi/pdf/{s}.pdf")}</div></article>''' for s, t, d, lv in CHEAT)
    n_aj = sum("Auditor Junior" in k["level"] for k in K); n_sa = sum("Staf Akuntansi" in k["level"] for k in K); n_ma = sum("Manager Akuntansi" in k["level"] for k in K)
    body = f'''<section class="hero mhero"><div class="wrap">
<p class="label">Materi · Studi Kasus dan PDF Gratis</p>
<h1>Belajar Dari Kasus Nyata Tutup Buku dan Audit</h1>
<p class="sub">Untuk auditor junior, staf, dan manager akuntansi. Setiap kasus lengkap dengan jurnal, dampak laporan keuangan, kalimat CALK, dan prosedur auditor.</p>
<div class="stats"><div><b>{len(K)}</b><span>Studi Kasus</span></div><div><b>{len(K) + len(CHEAT) + 1}</b><span>PDF Siap Download</span></div><div><b>{len(P)}</b><span>PSAK Terhubung</span></div></div>
</div></section>
<section class="alt"><div class="wrap">
<div class="head"><h2>Pilih Sesuai Peran</h2></div>
<div class="roles">
<button type="button" class="role on" data-f="all"><b>Semua</b><span>{len(K) + len(CHEAT)} materi</span></button>
<button type="button" class="role" data-f="aj"><b>Auditor Junior</b><span>{n_aj} studi kasus</span></button>
<button type="button" class="role" data-f="sa"><b>Staf Akuntansi</b><span>{n_sa} studi kasus</span></button>
<button type="button" class="role" data-f="ma"><b>Manager Akuntansi</b><span>{n_ma} studi kasus</span></button>
</div>
<div class="pack"><div><b>Paket Lengkap {len(K)} Studi Kasus</b><span>Satu PDF berisi seluruh soal dan pembahasan, cocok untuk pelatihan tim.</span></div>{dl("/materi/pdf/kumpulan-studi-kasus-updatesak.pdf", "Download Paket PDF")}</div>
<h3 class="gh">Studi Kasus</h3><div class="mgrid">{cards}</div>
<h3 class="gh">Paket Ringkas</h3><div class="mgrid">{cheats}</div>
</div></section>
<section class="final"><div class="wrap center"><h2>Butuh Pelatihan In-House untuk Tim Akuntansi?</h2><p>Studi kasus disesuaikan dengan industri dan sistem perusahaan Anda.</p><a class="btn arrow" target="_blank" rel="noopener" href="https://wa.me/6282245260121?text=Halo%20tim%20UpdateSAK%2C%20kami%20tertarik%20pelatihan%20in-house%20untuk%20tim%20akuntansi.">Chat Ananta, CPA</a></div></section>
<script>document.querySelectorAll('.role').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.role').forEach(x=>x.classList.toggle('on',x===b));const f=b.dataset.f;document.querySelectorAll('.mcard').forEach(c=>{{c.hidden=!(f==='all'||c.dataset.lv.split(' ').some(v=>v===f||v==='all'))}})}}));</script>
'''
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Materi UpdateSAK", "url": url, "inLanguage": "id",
                     "hasPart": [{"@type": "LearningResource", "name": k["judul"], "url": f"{BASE}/materi/{k['slug']}/"} for k in K]}, ensure_ascii=False)
    html_ = HEAD.format(title="Materi Akuntansi dan Audit: Studi Kasus dan PDF Gratis | UpdateSAK",
                        desc=esc("Studi kasus akuntansi dan audit untuk auditor junior, staf, dan manager akuntansi: piutang ECL, PSAK 115, PSAK 116, persediaan, imbalan kerja, pajak tangguhan, covenant kredit. Download PDF gratis."),
                        url=url, ogt="Materi Akuntansi dan Audit UpdateSAK", img=f"{BASE}/img/share/mat-hub-og.jpg", ld=ld).replace('<main>\n', '<main>\n', 1) + body + B.FOOT
    B.write("materi", html_)
    B.make_images("mat-hub", "Materi Gratis", "Studi Kasus Akuntansi dan Audit untuk Profesional")
    pages.append(url)

def sitemap_llms():
    p = os.path.join(SITE, "sitemap.xml"); s = open(p).read()
    s = re.sub(r"<url><loc>https://updatesak\.com/materi/[^<]*</loc>.*?</url>\n", "", s)
    s = s.replace("</urlset>", "".join(f"<url><loc>{u}</loc><lastmod>{B.TODAY}</lastmod></url>\n" for u in pages) + "</urlset>")
    open(p, "w").write(s)
    p = os.path.join(SITE, "llms.txt"); s = open(p, encoding="utf-8").read().split("\n## Materi")[0].rstrip()
    s += "\n\n## Materi (Studi Kasus dan PDF Gratis)\n" + "".join(f"- [{k['judul']}]({BASE}/materi/{k['slug']}/): {k['ringkas']} Untuk {', '.join(k['level'])}.\n" for k in K)
    open(p, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    for k in K: pdf_case(k); case_page(k)
    pdf_all()
    for s_, t, d, _ in CHEAT: pdf_cheat(s_, t, d)
    hub(); sitemap_llms()
    print("materi pages", len(pages), "pdf", len(os.listdir(PDFDIR)))
