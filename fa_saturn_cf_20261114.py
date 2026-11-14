# -*- coding: utf-8 -*-
"""Saturn: conditional formatting risiko di kertas kerja Excel (14 Nov 2026).
High/Tinggi merah, Moderate/Sedang kuning, Low/Rendah hijau, Minimal abu, SR merah tua.
Menyuntik <conditionalFormatting> + <dxf> langsung ke XML xlsx (isi sel, rumus, validasi tidak disentuh).
Target: out/faindonesia/kkx/saturn/** dan sumber FA-Saturn_SIAP-UPLOAD-v4/saturn/kk/**, lalu ZIP pustaka dibangun ulang.
Idempoten (penanda: dxf unik FA-CF di styles.xml). Dry run: --dry."""
import os, re, sys, zipfile, shutil, io

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = "--dry" in sys.argv
DIRS = [os.path.join(ROOT, "out", "faindonesia", "kkx", "saturn"),
        os.path.join(ROOT, "FA-Saturn_SIAP-UPLOAD-v4", "saturn", "kk")]
ZIPDIR = os.path.join(ROOT, "out", "faindonesia", "kkx", "zip")

# (nama, fill, font, bold) ; urutan dxf = urutan di DXF_XML
STY = [("high", "FFC7CE", "9C0006"), ("mod", "FFEB9C", "7F6000"), ("low", "C6EFCE", "006100"),
       ("min", "EDEDED", "595959"), ("sr", "C00000", "FFFFFF"), ("na", "F7F7F7", "A6A6A6")]


def dxf(fill, font):
    return ('<dxf><font><b/><color rgb="FF%s"/></font><fill><patternFill patternType="solid">'
            '<fgColor rgb="FF%s"/><bgColor rgb="FF%s"/></patternFill></fill></dxf>') % (font, fill, fill)


MARK = 'FA-CF'  # ditulis sebagai atribut count? tidak ada; penanda = dxf SR (fill C00000 + font FFFFFF)
MARK_XML = dxf("C00000", "FFFFFF")

IR_LIST = '"R,S,T,SR,n/a"'
CR_LIST = '"Minimal,Rendah,Sedang,Tinggi"'


def rules(kind, base_dxf, prio):
    """kind ir -> R/S/T/SR/n/a ; cr -> teks. kembalikan (xml, prio_berikut)"""
    d = {n: base_dxf + i for i, (n, _, _) in enumerate(STY)}
    if kind == "ir":
        order = [("SR", "sr"), ("T", "high"), ("S", "mod"), ("R", "low"), ("n/a", "na")]
    else:
        order = [("Tinggi", "high"), ("Sedang", "mod"), ("Rendah", "low"), ("Minimal", "min"), ("n/a", "na")]
    out = []
    for val, nm in order:
        out.append('<cfRule type="cellIs" dxfId="%d" priority="%d" operator="equal"><formula>"%s"</formula></cfRule>' % (d[nm], prio, val))
        prio += 1
    return "".join(out), prio


def patch_styles(x):
    if MARK_XML in x: return None, None
    m = re.search(r'<dxfs count="(\d+)"\s*/>', x)
    add = "".join(dxf(f, c) for _, f, c in STY)
    if m:
        base = int(m.group(1))
        x = x.replace(m.group(0), '<dxfs count="%d">%s</dxfs>' % (base + len(STY), add), 1)
        return x, base
    m = re.search(r'<dxfs count="(\d+)">', x)
    if m:
        base = int(m.group(1))
        x = x.replace(m.group(0), '<dxfs count="%d">' % (base + len(STY)), 1)
        x = x.replace("</dxfs>", add + "</dxfs>", 1)
        return x, base
    if "<dxfs" not in x:
        blk = '<dxfs count="%d">%s</dxfs>' % (len(STY), add)
        if "<tableStyles" in x: x = x.replace("<tableStyles", blk + "<tableStyles", 1)
        elif "</styleSheet>" in x: x = x.replace("</styleSheet>", blk + "</styleSheet>", 1)
        else: return None, None
        return x, 0
    return None, None


def expand(sq):
    return sq.strip()


def patch_sheet(x, base):
    """x = xml sheet. return xml baru atau None bila tak ada target."""
    dvs = re.findall(r'<dataValidation\b[^>]*?sqref="([^"]+)"[^>]*>.*?<formula1>(.*?)</formula1>', x, re.S)
    ir, cr = [], []
    for sq, f1 in dvs:
        f1 = f1.replace("&quot;", '"')
        if f1 == IR_LIST: ir.append(sq)
        elif f1 == CR_LIST: cr.append(sq)
    if not ir and not cr: return None
    # B-8: kolom CR K:P mengikuti baris IR
    for sq in list(ir):
        for part in sq.split():
            m = re.match(r'^E(\d+):I(\d+)$', part)
            if m: cr.append("K%s:P%s" % (m.group(1), m.group(2)))
    existing = [int(p) for p in re.findall(r'<cfRule\b[^>]*priority="(\d+)"', x)]
    prio = (max(existing) if existing else 0) + 1
    blocks = []
    if ir:
        r, prio = rules("ir", base, prio)
        blocks.append('<conditionalFormatting sqref="%s">%s</conditionalFormatting>' % (" ".join(ir), r))
    if cr:
        r, prio = rules("cr", base, prio)
        blocks.append('<conditionalFormatting sqref="%s">%s</conditionalFormatting>' % (" ".join(cr), r))
    ins = "".join(blocks)
    i = x.find("<dataValidations")
    if i < 0: return None
    return x[:i] + ins + x[i:]


def process(path):
    zin = zipfile.ZipFile(path)
    names = zin.namelist()
    data = {n: zin.read(n) for n in names}
    infos = {i.filename: i for i in zin.infolist()}
    zin.close()
    st = data.get("xl/styles.xml")
    if st is None: return "skip"
    sx, base = patch_styles(st.decode("utf-8"))
    if sx is None: return "sudah"
    changed = 0
    for n in names:
        if n.startswith("xl/worksheets/sheet") and n.endswith(".xml"):
            nx = patch_sheet(data[n].decode("utf-8"), base)
            if nx: data[n] = nx.encode("utf-8"); changed += 1
    if not changed: return "tanpa-target"
    data["xl/styles.xml"] = sx.encode("utf-8")
    if DRY: return "ubah"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(infos[n], data[n], compress_type=zipfile.ZIP_DEFLATED)
    open(path, "wb").write(buf.getvalue())
    return "ubah"


def zipdir(src, dst, arc):
    files = sorted(os.path.join(r, f) for r, _, fs in os.walk(src) for f in fs if not f.endswith(".zip"))
    sig = "|".join("%s:%d" % (os.path.relpath(f, src), os.path.getsize(f)) for f in files)
    stamp = dst + ".sig"
    if os.path.exists(dst) and os.path.exists(stamp) and open(stamp).read() == sig: return False
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files: z.write(f, os.path.join(arc, os.path.relpath(f, src)))
    open(stamp, "w").write(sig); return True


if __name__ == "__main__":
    tot = {}
    for D in DIRS:
        if not os.path.isdir(D): continue
        for r, _, fs in os.walk(D):
            for f in fs:
                if f.endswith(".xlsx"):
                    s = process(os.path.join(r, f)); tot[s] = tot.get(s, 0) + 1
    print(tot)
    if not DRY:
        z = zipdir(DIRS[0], os.path.join(ZIPDIR, "pustaka-kertas-kerja-fa-saturn.zip"), "Pustaka Kertas Kerja FA Saturn")
        print("zip dibangun ulang:", z)
