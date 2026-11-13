# -*- coding: utf-8 -*-
"""13 Nov 2026. Semua file download berbayar lewat Midtrans (Bos: "Semua berbayar ya, gak ada yang gratis";
pilihan Bos: template Excel di apps ikut berbayar; brosur, sampel e-book, contoh laporan CA, dan hasil kalkulator tetap).

BEKERJA LANGSUNG DI out/ + shared/pay/_worker.js + sumber /bayar/. Idempoten (dry run: --dry).
Jalankan SETELAH us_kk_berbayar_20261113.py dan SEBELUM caus_rapi_20261113.py.

Produk baru (harga di server, tampil hanya di /bayar/):
  tpl-sabh     Template Laporan Tahunan PT untuk SABH (Word, PDF, Excel FA Jupiter)   Rp49.000
  psak118-kit  PSAK 118 Implementation Toolkit (Excel) + Panduan Implementasi (PDF)   Rp49.000
  us-materi    Paket Materi Studi Kasus UpdateSAK (15 PDF, ZIP)                       Rp99.000
  us-dosen     Paket Materi Ajar Dosen UpdateSAK (11 PDF, ZIP)                        Rp99.000
  saturn-kk    Pustaka Kertas Kerja FA Saturn (101 Excel, 6 industri, ZIP)            Rp199.000
  tpl-jupiter, tpl-rs-abc, tpl-rs-obat, tpl-rs-coding, tpl-rs-ai: buka tombol Download Template Excel di aplikasi  Rp25.000
Semua termasuk konsultasi lewat WhatsApp. kk-118/116/109/115/paket (us_kk_berbayar) ikut diubah ke skema file yang sama.

Mekanisme:
- File dipindah ke out/faindonesia/kkx/<grup>/ (akses langsung /kkx/* = 404 oleh worker). File lama di out/faindonesia/template/,
  out/faindonesia-apps/files/ (toolkit + panduan PSAK 118), out/updatesak/materi/pdf/, out/updatesak/dosen/pdf/,
  out/faindonesia-saturn/saturn/kk/ dihapus; _redirects /saturn/kk/* dibuang.
- Worker: kind "file" (GET /api/pay/file?order_id=&f=<nomor file atau path di bawah prefix>) dan kind "unlock"
  (GET /api/pay/check?order_id=&prod=). Keduanya hanya jalan bila Midtrans settlement/capture dan MIDTRANS_PRODUCTION=true.
- /js/fa-gate.js di /audit-ready/, /saturn/, 4 tool RS: tombol template (dan link pustaka Saturn) mengecek order tersimpan;
  belum ada = diarahkan ke /bayar/?produk=..&back=..; sesudah lunas /bayar/selesai/ memberi tombol "Kembali ke Aplikasi".
  Template di aplikasi dibuat di browser, jadi pengamannya cek order di server, bukan file privat.
- Semua link download di 3 situs diganti ke /bayar/?produk=..; kata "gratis" untuk file tersebut dibuang.
"""
import os, re, sys, shutil, zipfile, json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FA, CA, US = (os.path.join(OUT, x) for x in ("faindonesia", "cariakuntan", "updatesak"))
APPS, SAT = os.path.join(OUT, "faindonesia-apps"), os.path.join(OUT, "faindonesia-saturn")
SRC = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
KKX = os.path.join(FA, "kkx")
DRY = "--dry" in sys.argv
N = [0]
PAY = "https://faindonesia.co.id/bayar/?produk="


def rd(p): return open(p, encoding="utf-8").read()


def wt(p, t):
    if os.path.exists(p) and rd(p) == t: return
    N[0] += 1
    if not DRY: open(p, "w", encoding="utf-8").write(t)


def must(t, old, new, count=1):
    assert old in t, old[:100]
    return t.replace(old, new, count)


def mv(a, b):
    if not os.path.exists(a): return
    N[0] += 1
    if DRY: return
    os.makedirs(os.path.dirname(b), exist_ok=True)
    if os.path.exists(b): os.remove(a)
    else: shutil.move(a, b)


# ====================== 1. file ======================
SABH = ["template-laporan-tahunan-pt-sabh-fa-indonesia.docx", "template-laporan-tahunan-pt-sabh-fa-indonesia.pdf",
        "template-data-laporan-tahunan-sabh-fa-jupiter.xlsx"]
for f in SABH: mv(os.path.join(FA, "template", f), os.path.join(KKX, "sabh", f))
if not DRY and os.path.isdir(os.path.join(FA, "template")) and not os.listdir(os.path.join(FA, "template")):
    os.rmdir(os.path.join(FA, "template"))
P118 = ["fa-psak118-implementation-toolkit.xlsx", "fa-psak118-panduan-implementasi.pdf"]
for f in P118: mv(os.path.join(APPS, "files", f), os.path.join(KKX, "psak118", f))
for grp, d in (("us-materi", os.path.join(US, "materi", "pdf")), ("us-dosen", os.path.join(US, "dosen", "pdf"))):
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)): mv(os.path.join(d, f), os.path.join(KKX, grp, f))
        if not DRY and not os.listdir(d): os.rmdir(d)
satkk = os.path.join(SAT, "saturn", "kk")
if os.path.isdir(satkk):
    for dd, _, fs in os.walk(satkk):
        for f in fs:
            a = os.path.join(dd, f); mv(a, os.path.join(KKX, "saturn", os.path.relpath(a, satkk)))
    if not DRY: shutil.rmtree(satkk, ignore_errors=True)


def zipdir(src, dst, arc):
    if DRY or not os.path.isdir(src): return
    files = sorted(os.path.join(r, f) for r, _, fs in os.walk(src) for f in fs if not f.endswith(".zip"))
    sig = "|".join("%s:%d" % (os.path.relpath(f, src), os.path.getsize(f)) for f in files)
    stamp = dst + ".sig"
    if os.path.exists(dst) and os.path.exists(stamp) and open(stamp).read() == sig: return
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files: z.write(f, os.path.join(arc, os.path.relpath(f, src)))
    open(stamp, "w").write(sig); N[0] += 1


ZIPS = {"us-materi": ("us-materi", "paket-materi-studi-kasus-updatesak.zip", "Materi Studi Kasus UpdateSAK"),
        "us-dosen": ("us-dosen", "paket-materi-ajar-dosen-updatesak.zip", "Materi Ajar Dosen UpdateSAK"),
        "saturn-kk": ("saturn", "pustaka-kertas-kerja-fa-saturn.zip", "Pustaka Kertas Kerja FA Saturn")}
for k, (d, z, arc) in ZIPS.items():
    if not DRY: os.makedirs(os.path.join(KKX, "zip"), exist_ok=True)
    zipdir(os.path.join(KKX, d), os.path.join(KKX, "zip", z), arc)
n_sat = sum(len(fs) for _, _, fs in os.walk(os.path.join(KKX, "saturn"))) if os.path.isdir(os.path.join(KKX, "saturn")) else 0

# ====================== 2. produk + worker ======================
WA_NOTE = " + Konsultasi WhatsApp"
PRODUCTS = [
    ("kk-118", "Kertas Kerja PSAK 118 (Excel)" + WA_NOTE, 25000, "file", [["Kertas Kerja PSAK 118 (Excel)", "kertas-kerja-psak-118-updatesak.xlsx"]], None, None),
    ("kk-116", "Kertas Kerja PSAK 116 (Excel)" + WA_NOTE, 25000, "file", [["Kertas Kerja PSAK 116 (Excel)", "kertas-kerja-psak-116-updatesak.xlsx"]], None, None),
    ("kk-109", "Kertas Kerja PSAK 109 (Excel)" + WA_NOTE, 25000, "file", [["Kertas Kerja PSAK 109 (Excel)", "kertas-kerja-psak-109-updatesak.xlsx"]], None, None),
    ("kk-115", "Kertas Kerja PSAK 115 (Excel)" + WA_NOTE, 25000, "file", [["Kertas Kerja PSAK 115 (Excel)", "kertas-kerja-psak-115-updatesak.xlsx"]], None, None),
    ("kk-paket", "Paket 4 Kertas Kerja PSAK (Excel)" + WA_NOTE, 75000, "file",
     [["Kertas Kerja PSAK %s (Excel)" % n, "kertas-kerja-psak-%s-updatesak.xlsx" % n] for n in ("118", "116", "109", "115")], None, None),
    ("tpl-sabh", "Template Laporan Tahunan PT untuk SABH (Word, PDF, Excel)" + WA_NOTE, 49000, "file",
     [["Template Word", "sabh/" + SABH[0]], ["Contoh PDF", "sabh/" + SABH[1]], ["Excel Format FA Jupiter", "sabh/" + SABH[2]]], None, None),
    ("psak118-kit", "PSAK 118 Implementation Toolkit (Excel) dan Panduan (PDF)" + WA_NOTE, 49000, "file",
     [["Toolkit Excel PSAK 118", "psak118/" + P118[0]], ["Panduan Implementasi (PDF)", "psak118/" + P118[1]]], None, None),
    ("us-materi", "Paket Materi Studi Kasus UpdateSAK (PDF)" + WA_NOTE, 99000, "file",
     [["Paket Materi (ZIP)", "zip/" + ZIPS["us-materi"][1]]], "us-materi/", None),
    ("us-dosen", "Paket Materi Ajar Dosen UpdateSAK (PDF)" + WA_NOTE, 99000, "file",
     [["Paket Materi Ajar (ZIP)", "zip/" + ZIPS["us-dosen"][1]]], "us-dosen/", None),
    ("saturn-kk", "Pustaka Kertas Kerja FA Saturn (Excel, 6 industri)" + WA_NOTE, 199000, "file",
     [["Pustaka Kertas Kerja (ZIP)", "zip/" + ZIPS["saturn-kk"][1]]], "saturn/", "/saturn/"),
    ("tpl-jupiter", "Template Excel FA Jupiter" + WA_NOTE, 25000, "unlock", None, None, "/audit-ready/"),
    ("tpl-rs-abc", "Template Excel Unit Cost RS (FA Venus)" + WA_NOTE, 25000, "unlock", None, None, "/kalkulator-unit-cost-rumah-sakit/"),
    ("tpl-rs-obat", "Template Excel ABC-VEN Obat RS (FA Venus)" + WA_NOTE, 25000, "unlock", None, None, "/analisis-abc-ven-obat-rumah-sakit/"),
    ("tpl-rs-coding", "Template Excel Cek Koding BPJS (FA Venus)" + WA_NOTE, 25000, "unlock", None, None, "/cek-koding-bpjs-ina-cbg/"),
    ("tpl-rs-ai", "Template Excel Analis AI RS (FA Venus)" + WA_NOTE, 25000, "unlock", None, None, "/analis-ai-rumah-sakit/"),
]
for k, name, price, kind, files, prefix, back in PRODUCTS:
    for lab, path in (files or []): assert DRY or os.path.exists(os.path.join(KKX, path)), path
    assert len(name) <= 80, k

js_prod = "  /* PAID13:start (fa_semua_berbayar_20261113.py) */\n" + "".join(
    '  "%s": %s,\n' % (k, json.dumps(dict([("name", name), ("price", price), ("kind", kind)]
                                          + ([("files", files)] if files else []) + ([("prefix", prefix)] if prefix else [])
                                          + ([("back", back)] if back else [])), ensure_ascii=False))
    for k, name, price, kind, files, prefix, back in PRODUCTS) + "  /* PAID13:end */\n"

WFILE = r'''/* PAIDFN13:start File berbayar dan buka template aplikasi (fa_semua_berbayar_20261113.py). */
const FILE_TYPES = { xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document", pdf: "application/pdf", zip: "application/zip" };
async function paidOrder(env, id, kind) {
  if (!/^FA-\d{6}-[a-z0-9-]+-[A-Z2-9]{8}$/.test(id)) return { err: json({ error: "Nomor order tidak valid" }, 400) };
  const key = prodFromOrder(id), p = key && PRODUCTS[key];
  if (!p || p.kind !== kind) return { err: json({ error: "Order ini bukan untuk produk tersebut" }, 403) };
  if (env.MIDTRANS_PRODUCTION !== "true") return { err: json({ error: "Mode uji: tidak diterbitkan" }, 403) };
  const st = await midStatus(env, id);
  const paid = st && PAID.indexOf(st.transaction_status) >= 0 && st.fraud_status !== "deny" && st.fraud_status !== "challenge";
  if (!paid) return { err: json({ error: "Pembayaran belum lunas" }, 402) };
  return { key, p };
}
async function paidFile(url, env) {
  const r0 = await paidOrder(env, url.searchParams.get("order_id") || "", "file"); if (r0.err) return r0.err;
  const p = r0.p, f = url.searchParams.get("f") || "";
  let path = null;
  if (/^\d+$/.test(f) && p.files[+f]) path = p.files[+f][1];
  else if (p.prefix && f.startsWith(p.prefix) && !f.includes("..") && /^[A-Za-z0-9._\/-]+\.(xlsx|pdf|docx)$/.test(f)) path = f;
  if (!path) return json({ error: "File tidak termasuk order ini" }, 403);
  const r = await env.ASSETS.fetch(new Request(new URL("/kkx/" + path, url).toString()));
  if (!r.ok) return json({ error: "File tidak ditemukan" }, 404);
  const name = path.split("/").pop(), ext = name.split(".").pop();
  return new Response(r.body, { headers: { "content-type": FILE_TYPES[ext] || "application/octet-stream",
    "content-disposition": 'attachment; filename="' + name + '"', "cache-control": "no-store", "x-robots-tag": "noindex" } });
}
async function paidCheck(url, env) {
  const r0 = await paidOrder(env, url.searchParams.get("order_id") || "", "unlock"); if (r0.err) return r0.err;
  if (r0.key !== (url.searchParams.get("prod") || "")) return json({ ok: false, error: "Order ini untuk aplikasi lain" }, 403);
  return json({ ok: true, prod: r0.key });
}
/* PAIDFN13:end */
'''

p = os.path.join(HERE, "shared", "pay", "_worker.js"); t = rd(p)
t = re.sub(r'  "kk-[a-z0-9]+":\s*\{ name: [^\n]*\n', "", t)                       # baris lama us_kk_berbayar
if "PAID13:start" in t: t = re.sub(r'  /\* PAID13:start.*?PAID13:end \*/\n', lambda m: js_prod, t, flags=re.S)
else: t = must(t, '  "custom":     { name: "Layanan FA Indonesia", price: 0, kind: "service" }', js_prod + '  "custom":     { name: "Layanan FA Indonesia", price: 0, kind: "service" }')
t = re.sub(r'/\* Kertas kerja Excel berbayar: file di /kkx/.*?\n}\n\n', "", t, flags=re.S)   # kkFile lama
if "PAIDFN13:start" in t: t = re.sub(r'/\* PAIDFN13:start.*?/\* PAIDFN13:end \*/\n', lambda m: WFILE, t, flags=re.S)
else: t = must(t, "async function notify(req, env, ctx) {", WFILE + "\nasync function notify(req, env, ctx) {")
t = t.replace('  if (p.kind === "kk") return { kind: "kk", product: p.name, files: p.files };\n', "")
if 'p.kind === "file"' not in t:
    t = must(t, '  return { kind: p.kind, product: p.name };\n}',
             '  if (p.kind === "file") return { kind: "file", product: p.name, files: p.files.map(function (x, i) { return { l: x[0], i: i }; }) };\n'
             '  if (p.kind === "unlock") return { kind: "unlock", product: p.name, prod: key, back: p.back };\n'
             '  return { kind: p.kind, product: p.name };\n}')
t = t.replace('acc && acc.kind === "kk" ? "Kertas kerja Excel: pembeli download sendiri di halaman status, termasuk konsultasi WA"',
              'acc && (acc.kind === "file" || acc.kind === "unlock") ? "File/template: pembeli download sendiri di halaman status, termasuk konsultasi WA"')
if 'acc.kind === "file"' not in t:
    t = must(t, 'acc && acc.kind === "ebook" ? "Kirim PDF + password e-book ke pembeli"',
             'acc && (acc.kind === "file" || acc.kind === "unlock") ? "File/template: pembeli download sendiri di halaman status, termasuk konsultasi WA" : acc && acc.kind === "ebook" ? "Kirim PDF + password e-book ke pembeli"')
t = t.replace('      if (url.pathname === "/api/pay/file" && req.method === "GET") return await kkFile(url, env);\n',
              '      if (url.pathname === "/api/pay/file" && req.method === "GET") return await paidFile(url, env);\n')
if "/api/pay/check" not in t:
    t = must(t, '      if (url.pathname === "/api/pay/file" && req.method === "GET") return await paidFile(url, env);\n',
             '      if (url.pathname === "/api/pay/file" && req.method === "GET") return await paidFile(url, env);\n'
             '      if (url.pathname === "/api/pay/check" && req.method === "GET") return await paidCheck(url, env);\n')
if 'url.pathname.startsWith("/files/fa-psak118-")' not in t:
    t = must(t, '    if (url.pathname.startsWith("/kkx/")) return',
             '    if (url.pathname.startsWith("/files/fa-psak118-")) return new Response("Tidak ditemukan", { status: 404, headers: { "x-robots-tag": "noindex" } });\n'
             '    if (url.pathname.startsWith("/kkx/")) return')
assert "kkFile" not in t and "paidFile(url, env)" in t
wt(p, t); wt(os.path.join(FA, "_worker.js"), t)

for p in (os.path.join(HERE, "shared", "pay", "_routes.json"), os.path.join(FA, "_routes.json")):
    r = rd(p)
    if "/files/fa-psak118-*" not in r: r = must(r, '"/kkx/*"]', '"/kkx/*", "/files/fa-psak118-*"]')
    wt(p, r)
p = os.path.join(FA, "_redirects"); t = rd(p)
t = re.sub(r'\n/saturn/kk/\*[^\n]*', "", t)
if "/files/fa-psak118-*" not in t:   # _redirects dibaca sebelum worker; arahkan link lama ke halaman pembayaran
    t = must(t, "\n/files/*", "\n/files/fa-psak118-*  /bayar/?produk=psak118-kit  302\n/files/*")
wt(p, t)

# ====================== 3. /bayar/ dan /bayar/selesai/ ======================
OPTS = "<!--paid13-->" + "".join('<option data-ppn="1" data-price="%d" value="%s">%s</option>\n' % (price, k, name)
                                for k, name, price, kind, files, prefix, back in PRODUCTS) + "<!--/paid13-->"
SEL_JS = ("}else if(a.kind==='file'||a.kind==='unlock'){var wam='https://wa.me/6282245260121?text='+encodeURIComponent('Halo Pak Ananta, saya sudah membeli '+a.product+' (order '+x.order_id+'). Mau konsultasi: ');"
          "$('acc').innerHTML='<p style=\"margin:0\">'+esc(a.product)+'. '+(a.kind==='file'?'File siap di-download.':'Tombol Download Template Excel di aplikasi sudah terbuka di perangkat ini.')+' Pembelian ini termasuk konsultasi lewat WhatsApp, sebutkan nomor order saat chat.</p><p class=\"hint\" style=\"margin:8px 0 0\">Halaman ini bisa dibuka lagi kapan saja dari link yang sama.</p>';"
          "if(a.kind==='unlock'){try{localStorage.setItem('fa_pay_'+a.prod,x.order_id)}catch(e){}}"
          "act((a.kind==='file'?(a.files||[]).map(function(f){return '<a class=\"btn solid\" href=\"/api/pay/file?order_id='+encodeURIComponent(x.order_id)+'&f='+f.i+'\">Download '+esc(f.l)+'</a>'}).join(''):'<a class=\"btn solid\" href=\"'+esc(a.back)+'?order_id='+encodeURIComponent(x.order_id)+'\">Kembali ke Aplikasi</a>')+"
          "(a.back&&a.kind==='file'?'<a class=\"btn\" href=\"'+esc(a.back)+'?order_id='+encodeURIComponent(x.order_id)+'\">Kembali ke Aplikasi</a>':'')+"
          "'<a class=\"btn\" target=\"_blank\" rel=\"noopener\" href=\"'+wam+'\">Chat Ananta, CPA</a>');\n"
          "    }else if(a.kind==='ebook'){")
for root in (SRC, FA):
    p = os.path.join(root, "bayar", "index.html"); t = rd(p)
    t = re.sub(r'<option data-ppn="1" data-price="\d+" value="kk-[a-z0-9]+">[^<]*</option>\n', "", t)
    if "<!--paid13-->" in t: t = re.sub(r"<!--paid13-->.*?<!--/paid13-->", lambda m: OPTS, t, flags=re.S)
    else:
        m = re.search(r'<option [^>]*value="custom"[^>]*>', t); assert m
        t = t[:m.start()] + OPTS + "\n" + t[m.start():]
    if "fa_back" not in t:   # simpan ?back= supaya selesai tahu jalan pulang (cadangan bila produk tanpa back)
        t = must(t, "var q=new URLSearchParams(location.search).get('produk');",
                 "try{var bk=new URLSearchParams(location.search).get('back');if(bk&&/^\\/[a-z0-9\\-\\/]*$/.test(bk))sessionStorage.setItem('fa_back',bk)}catch(e){}\nvar q=new URLSearchParams(location.search).get('produk');")
    wt(p, t)
    p = os.path.join(root, "bayar", "selesai", "index.html"); t = rd(p)
    t = re.sub(r"\}else if\(a\.kind==='kk'\)\{.*?\n    \}else if\(a\.kind==='ebook'\)\{", lambda m: SEL_JS, t, flags=re.S)
    t = re.sub(r"\}else if\(a\.kind==='file'\|\|a\.kind==='unlock'\)\{.*?\n    \}else if\(a\.kind==='ebook'\)\{", lambda m: SEL_JS, t, flags=re.S)
    if "a.kind==='file'" not in t: t = must(t, "}else if(a.kind==='ebook'){", SEL_JS)
    wt(p, t)

# ====================== 4. gerbang template di aplikasi ======================
GATE = r'''/* fa-gate.js (13 Nov 2026, fa_semua_berbayar_20261113.py): template Excel dan pustaka kertas kerja berbayar via Midtrans. */
(function(){var C=window.FA_GATE;if(!C)return;var P=C.prod,K='fa_pay_'+P,ok=false,oid=null;
try{var q=new URLSearchParams(location.search).get('order_id');if(q&&/^FA-\d{6}-[a-z0-9-]+-[A-Z2-9]{8}$/.test(q)){localStorage.setItem(K,q);history.replaceState(null,'',location.pathname+location.hash)}oid=localStorage.getItem(K)}catch(e){}
function go(){location.href='/bayar/?produk='+encodeURIComponent(P)+'&back='+encodeURIComponent(location.pathname)}
if(oid){var u=C.file?'/api/pay/status?order_id='+encodeURIComponent(oid):'/api/pay/check?order_id='+encodeURIComponent(oid)+'&prod='+encodeURIComponent(P);
 fetch(u,{cache:'no-store'}).then(function(r){return r.json()}).then(function(x){ok=C.file?!!(x&&x.paid&&x.access&&x.access.kind==='file'):!!(x&&x.ok)}).catch(function(){})}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest(C.sel);if(!a)return;
 if(C.file){e.preventDefault();e.stopImmediatePropagation();if(!ok){go();return}
  var m=(a.getAttribute('href')||'').match(/\/saturn\/kk\/(.+)$/);if(!m){go();return}
  location.href='/api/pay/file?order_id='+encodeURIComponent(oid)+'&f='+encodeURIComponent('saturn/'+decodeURIComponent(m[1]));return}
 if(ok)return;e.preventDefault();e.stopImmediatePropagation();go()},true)})();
'''
wt(os.path.join(FA, "js", "fa-gate.js"), GATE)
GATES = {"audit-ready": ("tpl-jupiter", '[data-act="tpl"]', False), "saturn": ("saturn-kk", 'a[href*="/saturn/kk/"]', True),
         "saturn/metodologi": ("saturn-kk", 'a[href*="/saturn/kk/"]', True),
         "kalkulator-unit-cost-rumah-sakit": ("tpl-rs-abc", "#xl_dl", False), "analisis-abc-ven-obat-rumah-sakit": ("tpl-rs-obat", "#xl_dl", False),
         "cek-koding-bpjs-ina-cbg": ("tpl-rs-coding", "#xl_dl", False), "analis-ai-rumah-sakit": ("tpl-rs-ai", "#xl_dl", False)}
for d, (prod, sel, isfile) in GATES.items():
    p = os.path.join(FA, d, "index.html"); t = rd(p)
    tag = ('<!--fagate--><script>window.FA_GATE={prod:%s,sel:%s,file:%s}</script><script src="/js/fa-gate.js?v=20261113"></script><!--/fagate-->'
           % (json.dumps(prod), json.dumps(sel), "true" if isfile else "false"))
    t = re.sub(r"<!--fagate-->.*?<!--/fagate-->", "", t, flags=re.S)
    t = t.replace("</head>", tag + "</head>", 1)
    if d.startswith("saturn"):
        t = t.replace("Demo dan semua template bisa dicoba gratis di browser.", "Demo bisa dicoba gratis di browser. Pustaka kertas kerja Excel tersedia berbayar, termasuk konsultasi WhatsApp.")
    wt(p, t)

# ====================== 5. link di 3 situs ======================
RX_SABH = re.compile(r'<a ([^>]*?)href="(?:https://faindonesia\.co\.id)?/template/(template-[^"]+)"([^>]*)>([^<]*)</a>')
RX_118 = re.compile(r'<a ([^>]*?)href="(?:https://faindonesia\.co\.id)?/files/fa-psak118-[^"]+"([^>]*)>')
RX_US = re.compile(r'<a ([^>]*?)href="/(materi|dosen)/pdf/[^"]+"([^>]*)>([^<]*)</a>')
LAB = {"Download Template Word": "Dapatkan Template Word", "Lihat Contoh PDF": "Template PDF",
       "Download PDF Soal dan Pembahasan": "Dapatkan PDF Soal dan Pembahasan", "Download PDF": "Dapatkan PDF",
       "Download Paket PDF": "Dapatkan Paket PDF", "PDF": "PDF", "Download Slide Pelatihan (PDF)": "Dapatkan Slide Pelatihan (PDF)",
       "Download Template Excel": "Dapatkan Template Excel"}


def clean_attrs(a):
    a = re.sub(r'\s*download(="[^"]*")?(?=\s|$)', "", a)
    a = re.sub(r'\s*target="_blank"', "", a); a = re.sub(r'\s*rel="noopener"', "", a)
    return a.strip()


def fix_links(t, site):
    o = t
    def s1(m):
        a1, a3 = clean_attrs(m.group(1)), clean_attrs(m.group(3))
        return '<a %shref="%s"%s>%s</a>' % ((a1 + " ") if a1 else "", PAY + "tpl-sabh", (" " + a3) if a3 else "", LAB.get(m.group(4), m.group(4)))
    t = RX_SABH.sub(s1, t)
    t = RX_118.sub(lambda m: '<a %shref="%s"%s>' % ((clean_attrs(m.group(1)) + " ") if clean_attrs(m.group(1)) else "", PAY + "psak118-kit",
                                                    (" " + clean_attrs(m.group(2))) if clean_attrs(m.group(2)) else ""), t)
    def s3(m):
        a1, a3 = clean_attrs(m.group(1)), clean_attrs(m.group(3))
        return '<a %shref="%s"%s>%s</a>' % ((a1 + " ") if a1 else "", PAY + ("us-materi" if m.group(2) == "materi" else "us-dosen"),
                                         (" " + a3) if a3 else "", LAB.get(m.group(4), m.group(4)))
    t = RX_US.sub(s3, t)
    # sisa URL mentah (JSON-LD, data-*): arahkan ke halaman pembayaran
    t = re.sub(r'(?:https://faindonesia\.co\.id)?/template/template-[A-Za-z0-9._-]+', PAY + "tpl-sabh", t)
    t = re.sub(r'(?:https://faindonesia\.co\.id)?/files/fa-psak118-[A-Za-z0-9._-]+', PAY + "psak118-kit", t)
    t = re.sub(r'(?:https://updatesak\.com)?/materi/pdf/[A-Za-z0-9._-]+', PAY + "us-materi", t)
    t = re.sub(r'(?:https://updatesak\.com)?/dosen/pdf/[A-Za-z0-9._-]+', PAY + "us-dosen", t)
    if t == o: return t
    for a, b in [("Template Gratis untuk Notaris dan Direksi", "Template untuk Notaris dan Direksi"),
                 ('id="template-gratis-untuk-notaris-dan-direksi"', 'id="template-untuk-notaris-dan-direksi"'),
                 ("#template-gratis-untuk-notaris-dan-direksi", "#template-untuk-notaris-dan-direksi"),
                 ("Template Gratis: Laporan Tahunan PT untuk SABH", "Template Laporan Tahunan PT untuk SABH"),
                 ("Panduan SABH · Template Gratis", "Panduan SABH · Template"),
                 (">Template Gratis<", ">Template<"),
                 ("Studi Kasus dan PDF Gratis", "Studi Kasus dan PDF"), ("Download Gratis →", "Lihat Materi Ajar →"),
                 ("Angkanya bisa dihasilkan dari FA Jupiter.</p>", "Angkanya bisa dihasilkan dari FA Jupiter. Termasuk konsultasi lewat WhatsApp.</p>")]:
        t = t.replace(a, b)
    return t


for root, site in ((FA, "fa"), (CA, "ca"), (US, "us")):
    for dd, _, fs in os.walk(root):
        if "/kkx" in dd: continue
        for f in fs:
            if not f.endswith(".html"): continue
            q = os.path.join(dd, f); t = rd(q)
            if "/template/template-" in t or "/files/fa-psak118-" in t or "/materi/pdf/" in t or "/dosen/pdf/" in t or "Template Gratis" in t:
                n = fix_links(t, site)
                assert "/template/template-" not in n and "/files/fa-psak118-" not in n and "/materi/pdf/" not in n and "/dosen/pdf/" not in n, q
                if n != t: wt(q, n)

# artikel PSAK 118 + /buku/ + llms
p = os.path.join(FA, "artikel", "panduan-implementasi-psak-118", "index.html")
if os.path.exists(p):
    t = rd(p)
    for a, b in [("Panduan Implementasi PSAK 118 + Template Excel Gratis", "Panduan Implementasi PSAK 118 + Template Excel"),
                 ("Roadmap, Contoh Laba Rugi, dan Template Excel Gratis", "Roadmap, Contoh Laba Rugi, dan Template Excel"),
                 ("template Excel PSAK 118 yang bisa di-download gratis.", "template Excel PSAK 118, termasuk konsultasi lewat WhatsApp."),
                 ("Download gratis ", ""),
                 ("Apakah template Excel PSAK 118 ini gratis?", "Bagaimana mendapatkan template Excel PSAK 118 ini?"),
                 ('"https://faindonesia.co.id/files/fa-psak118-panduan-implementasi.pdf"', '"https://faindonesia.co.id/bayar/?produk=psak118-kit"'),
                 ('"https://faindonesia.co.id/files/fa-psak118-implementation-toolkit.xlsx"', '"https://faindonesia.co.id/bayar/?produk=psak118-kit"')]:
        t = t.replace(a, b)
    t = re.sub(r'(Bagaimana mendapatkan template Excel PSAK 118 ini\?(?:</summary>|"[^}]*?"text":\s*"|[^<]*?<p>))Gratis\.',
               r"\1Lewat halaman pembayaran FA Indonesia, termasuk konsultasi WhatsApp.", t)
    t = t.replace("Bagaimana mendapatkan template Excel PSAK 118 ini?\", \"acceptedAnswer\": {\"@type\": \"Answer\", \"text\": \"Gratis.",
                  "Bagaimana mendapatkan template Excel PSAK 118 ini?\", \"acceptedAnswer\": {\"@type\": \"Answer\", \"text\": \"Lewat halaman pembayaran FA Indonesia, termasuk konsultasi WhatsApp.")
    wt(p, t)
p = os.path.join(FA, "buku", "index.html"); t = rd(p)
t = t.replace("""window.FA_DONASI={guards:[{sel:'#unduhan a.dl:not([href*="fa-consult-"])',key:'materi'}]}""",
              """window.FA_DONASI={guards:[{sel:'#unduhan a.dl:not([href*="fa-consult-"]):not([href*="/bayar/"])',key:'materi'}]}""")
t = re.sub(r'(<a class="dl" href="https://faindonesia\.co\.id/bayar/\?produk=psak118-kit"[^>]*>(?:(?!</a>).)*?)Unduh Gratis', r"\1Dapatkan", t, flags=re.S)
t = t.replace('data-title="Panduan gratis: Implementasi PSAK 118"', 'data-title="Panduan: Implementasi PSAK 118"')
t = t.replace("Brosur, panduan, dan toolkit Excel.", "Brosur dan panduan.")
wt(p, t)
for p, rules in [(os.path.join(FA, "llms.txt"), [
        ("- [Panduan Implementasi PSAK 118 (PDF)](https://faindonesia.co.id/files/fa-psak118-panduan-implementasi.pdf)\n", ""),
        ("- [PSAK 118 Implementation Toolkit (Excel)](https://faindonesia.co.id/files/fa-psak118-implementation-toolkit.xlsx)\n",
         "- [PSAK 118 Implementation Toolkit (Excel) dan Panduan (PDF)](https://faindonesia.co.id/bayar/?produk=psak118-kit): berbayar, termasuk konsultasi WhatsApp\n")]),
        (os.path.join(US, "llms.txt"), [])]:
    t = rd(p)
    for a, b in rules: t = t.replace(a, b)
    t = re.sub(r"\(https://updatesak\.com/(materi|dosen)/pdf/[^)]+\)", lambda m: "(" + PAY + ("us-materi" if m.group(1) == "materi" else "us-dosen") + ")", t)
    wt(p, t)

print("fa_semua_berbayar_20261113: %d perubahan, pustaka Saturn %d file%s" % (N[0], n_sat, " (dry)" if DRY else ""))
