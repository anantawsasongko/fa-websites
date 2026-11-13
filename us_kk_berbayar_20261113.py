# -*- coding: utf-8 -*-
"""13 Nov 2026. Kertas Kerja PSAK (Excel) UpdateSAK tidak lagi gratis (Bos: "kok banyak contoh kertas kerja yang bisa
download gratis excel, saya gak mau, suruh bayar midtrans semua dan termasuk gratis konsultasi via WA").

BEKERJA LANGSUNG DI out/ + sumber worker/halaman bayar. Idempoten (dry run: --dry).
Jalankan SETELAH us_kertas_kerja_20261112.py dan SEBELUM caus_rapi_20261113.py.

Isi:
1. File xlsx dipindah dari out/updatesak/kertas-kerja/ ke out/faindonesia/kkx/ (tidak bisa dibuka langsung: /kkx/* lewat
   worker dan dijawab 404). File hanya keluar lewat /api/pay/file?order_id=..&f=.. setelah Midtrans menyatakan lunas.
2. Worker (shared/pay/_worker.js, disalin ke out/faindonesia/_worker.js): produk kk-118, kk-116, kk-109, kk-115
   (Rp25.000 per file, sama dengan aturan harga kalkulator UpdateSAK) dan kk-paket (4 file, Rp75.000), kind "kk".
   _routes.json: tambah /kkx/*.
3. /bayar/: 5 pilihan produk baru. /bayar/selesai/: setelah lunas tampil tombol download tiap file + tombol
   "Chat Ananta, CPA" (konsultasi gratis via WhatsApp, pesan berisi nomor order).
4. UpdateSAK: tombol download di /kertas-kerja/ dan kotak us-kk di /psak/118|116|109|115/ diarahkan ke
   faindonesia.co.id/bayar/?produk=kk-..; kata "gratis" untuk kertas kerja dibuang (title, description, label, llms).
   Sesuai aturan apps: tidak ada harga di halaman UpdateSAK, harga tampil di halaman pembayaran.
5. CariAkuntan /cek-kebutuhan/: "kertas kerja PSAK gratis" jadi "kertas kerja PSAK".
CATATAN: /api/pay/config live 13 Nov masih production:false (sandbox). Tombol Bayar Online baru muncul setelah Bos mengisi
MIDTRANS_PRODUCTION=true + key produksi di Cloudflare faindonesia-web. Sebelum itu /bayar/ memberi invoice transfer bank,
dan file dikirim manual lewat WhatsApp setelah bukti transfer.
"""
import os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(HERE, "out", "faindonesia"); US = os.path.join(HERE, "out", "updatesak"); CA = os.path.join(HERE, "out", "cariakuntan")
SRC = os.path.join(HERE, "FA-Indonesia_Website_SIAP-UPLOAD-v58")
DRY = "--dry" in sys.argv
N = [0]
PSAK = ["118", "116", "109", "115"]
PRICE, PAKET = 25000, 75000


def rd(p): return open(p, encoding="utf-8").read()


def wt(p, t):
    if os.path.exists(p) and rd(p) == t: return
    N[0] += 1
    if not DRY: open(p, "w", encoding="utf-8").write(t)


def must(t, old, new, count=1):
    assert old in t, old[:90]
    return t.replace(old, new, count)


# ---------- 1. file ----------
os.makedirs(os.path.join(FA, "kkx"), exist_ok=True)
for n in PSAK:
    f = "kertas-kerja-psak-%s-updatesak.xlsx" % n
    a = os.path.join(US, "kertas-kerja", f); b = os.path.join(FA, "kkx", f)
    if os.path.exists(a):
        N[0] += 1
        if not DRY: shutil.move(a, b)
    assert DRY or os.path.exists(b), f

# ---------- 2. worker ----------
p = os.path.join(HERE, "shared", "pay", "_worker.js"); t = rd(p)
if '"kk-118"' not in t:
    t = must(t, '  "custom":     { name: "Layanan FA Indonesia", price: 0, kind: "service" }',
             "".join('  "kk-%s":     { name: "Kertas Kerja PSAK %s (Excel) + Konsultasi WhatsApp", price: %d, kind: "kk", files: ["%s"] },\n' % (n, n, PRICE, n) for n in PSAK)
             + '  "kk-paket":   { name: "Paket 4 Kertas Kerja PSAK (Excel) + Konsultasi WhatsApp", price: %d, kind: "kk", files: %s },\n' % (PAKET, str(PSAK).replace("'", '"'))
             + '  "custom":     { name: "Layanan FA Indonesia", price: 0, kind: "service" }')
    t = must(t, '  return { kind: p.kind, product: p.name };\n}',
             '  if (p.kind === "kk") return { kind: "kk", product: p.name, files: p.files };\n  return { kind: p.kind, product: p.name };\n}')
    t = must(t, 'acc && acc.kind === "ebook" ? "Kirim PDF + password e-book ke pembeli"',
             'acc && acc.kind === "kk" ? "Kertas kerja Excel: pembeli download sendiri di halaman status, termasuk konsultasi WA" : acc && acc.kind === "ebook" ? "Kirim PDF + password e-book ke pembeli"')
    t = must(t, "async function notify(req, env, ctx) {", '''/* Kertas kerja Excel berbayar: file di /kkx/ hanya keluar lewat sini setelah Midtrans menyatakan lunas. */
async function kkFile(url, env) {
  const id = url.searchParams.get("order_id") || "", f = url.searchParams.get("f") || "";
  if (!/^FA-\\d{6}-[a-z0-9-]+-[A-Z2-9]{8}$/.test(id)) return json({ error: "Nomor order tidak valid" }, 400);
  const key = prodFromOrder(id), p = key && PRODUCTS[key];
  if (!p || p.kind !== "kk" || p.files.indexOf(f) < 0) return json({ error: "File tidak termasuk order ini" }, 403);
  if (env.MIDTRANS_PRODUCTION !== "true") return json({ error: "Mode uji: file tidak diterbitkan" }, 403);
  const st = await midStatus(env, id);
  const paid = st && PAID.indexOf(st.transaction_status) >= 0 && st.fraud_status !== "deny" && st.fraud_status !== "challenge";
  if (!paid) return json({ error: "Pembayaran belum lunas" }, 402);
  const name = "kertas-kerja-psak-" + f + "-updatesak.xlsx";
  const r = await env.ASSETS.fetch(new Request(new URL("/kkx/" + name, url).toString()));
  if (!r.ok) return json({ error: "File tidak ditemukan" }, 404);
  return new Response(r.body, { headers: { "content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "content-disposition": 'attachment; filename="' + name + '"', "cache-control": "no-store", "x-robots-tag": "noindex" } });
}

async function notify(req, env, ctx) {''')
    t = must(t, '    if (!url.pathname.startsWith("/api/pay/")) return env.ASSETS.fetch(req);',
             '    if (url.pathname.startsWith("/kkx/")) return new Response("Tidak ditemukan", { status: 404, headers: { "x-robots-tag": "noindex" } });\n'
             '    if (!url.pathname.startsWith("/api/pay/")) return env.ASSETS.fetch(req);')
    t = must(t, '      if (url.pathname === "/api/pay/status" && req.method === "GET") return await status(url, env);',
             '      if (url.pathname === "/api/pay/status" && req.method === "GET") return await status(url, env);\n'
             '      if (url.pathname === "/api/pay/file" && req.method === "GET") return await kkFile(url, env);')
wt(p, t); wt(os.path.join(FA, "_worker.js"), t)
for p in (os.path.join(HERE, "shared", "pay", "_routes.json"), os.path.join(FA, "_routes.json")):
    r = rd(p)
    if "/kkx/*" not in r: r = must(r, '"include": ["/api/*"]', '"include": ["/api/*", "/kkx/*"]')
    wt(p, r)

# ---------- 3. /bayar/ dan /bayar/selesai/ ----------
for root in (SRC, FA):
    p = os.path.join(root, "bayar", "index.html"); t = rd(p)
    if 'value="kk-118"' not in t:
        m = re.search(r'<option [^>]*value="custom"[^>]*>', t); assert m
        opts = "".join('<option data-ppn="1" data-price="%d" value="kk-%s">Kertas Kerja PSAK %s (Excel) + Konsultasi WhatsApp</option>\n' % (PRICE, n, n) for n in PSAK)
        opts += '<option data-ppn="1" data-price="%d" value="kk-paket">Paket 4 Kertas Kerja PSAK (Excel) + Konsultasi WhatsApp</option>\n' % PAKET
        t = t[:m.start()] + opts + t[m.start():]
    wt(p, t)
    p = os.path.join(root, "bayar", "selesai", "index.html"); t = rd(p)
    if "a.kind==='kk'" not in t:
        t = must(t, "}else if(a.kind==='ebook'){",
                 "}else if(a.kind==='kk'){$('acc').innerHTML='<p style=\"margin:0\">'+esc(a.product)+'. File Excel siap di-download. Pembelian ini termasuk konsultasi lewat WhatsApp untuk kasus perusahaan Anda, sebutkan nomor order saat chat.</p><p class=\"hint\" style=\"margin:8px 0 0\">Halaman ini bisa dibuka lagi kapan saja dari link yang sama.</p>';"
                 "act((a.files||[]).map(function(f){return '<a class=\"btn solid\" href=\"/api/pay/file?order_id='+encodeURIComponent(x.order_id)+'&f='+encodeURIComponent(f)+'\">Download Kertas Kerja PSAK '+esc(f)+'</a>'}).join('')+"
                 "'<a class=\"btn\" target=\"_blank\" rel=\"noopener\" href=\"https://wa.me/6282245260121?text='+encodeURIComponent('Halo Pak Ananta, saya sudah membeli '+a.product+' (order '+x.order_id+'). Mau konsultasi: ')+'\">Chat Ananta, CPA</a>');\n"
                 "    }else if(a.kind==='ebook'){")
    wt(p, t)

# ---------- 4. UpdateSAK ----------
def pay(n): return "https://faindonesia.co.id/bayar/?produk=kk-%s" % n


p = os.path.join(US, "kertas-kerja", "index.html"); t = rd(p)
for n in PSAK:
    t = t.replace('<a class="btn arrow" href="/kertas-kerja/kertas-kerja-psak-%s-updatesak.xlsx" download data-us-kk="%s">Download Excel PSAK %s</a>' % (n, n, n),
                  '<a class="btn arrow" href="%s" data-us-kk="%s">Dapatkan Kertas Kerja PSAK %s</a>' % (pay(n), n, n))
for a, b in [
    ("<title>Kertas Kerja PSAK Gratis: Template Excel Siap Pakai</title>", "<title>Kertas Kerja PSAK: Template Excel Siap Pakai</title>"),
    ("Kertas kerja PSAK gratis dalam Excel: PSAK 118, 116, 109, dan 115. Berisi contoh, checklist, rumus, dan jurnal. Download, ganti angka, langsung dipakai.",
     "Kertas kerja PSAK dalam Excel: PSAK 118, 116, 109, dan 115. Berisi contoh, checklist, rumus, dan jurnal, termasuk konsultasi lewat WhatsApp."),
    ("Kertas Kerja PSAK Gratis: Template Excel Siap Pakai", "Kertas Kerja PSAK: Template Excel Siap Pakai"),
    ('<p class="label">Template Excel · Gratis · Tanpa Daftar</p>', '<p class="label">Template Excel · Termasuk Konsultasi WhatsApp</p>'),
    ("kertas kerja berumus dengan data contoh, dan contoh jurnal. Download, ganti angkanya dengan angka perusahaan Anda.",
     "kertas kerja berumus dengan data contoh, dan contoh jurnal. Setiap file sudah termasuk konsultasi lewat WhatsApp untuk kasus perusahaan Anda."),
    ("<li>Download file Excel PSAK yang Anda perlukan.</li>", "<li>Pilih PSAK yang Anda perlukan, selesaikan pemesanan, lalu download file Excel di halaman status order.</li>"),
    ("Tanyakan langsung. Gratis, dijawab lewat WhatsApp.", "Konsultasi lewat WhatsApp sudah termasuk di setiap kertas kerja."),
]:
    t = t.replace(a, b)
if "<!--kk-paket-->" not in t:
    t = must(t, '<h2 id="cara-pakai">', '<!--kk-paket--><p><a class="btn btn-ghost" href="%s" data-us-kk="paket">Dapatkan Paket 4 Kertas Kerja</a></p><!--/kk-paket--><h2 id="cara-pakai">' % pay("paket"))
t = re.sub(r'"isAccessibleForFree"\s*:\s*true', '"isAccessibleForFree":false', t)
t = re.sub(r'("offers"\s*:\s*\{[^{}]*"price"\s*:\s*)"?0"?', r'\g<1>"%d"' % PRICE, t)
assert ".xlsx" not in t, "masih ada link xlsx di /kertas-kerja/"
wt(p, t)
for n in PSAK:
    p = os.path.join(US, "psak", n, "index.html"); t = rd(p)
    t = t.replace("Kertas Kerja PSAK %s (Excel, Gratis)" % n, "Kertas Kerja PSAK %s (Excel)" % n)
    t = t.replace("Berisi data contoh, checklist, dan rumus. Download, ganti angkanya, langsung dipakai.",
                  "Berisi data contoh, checklist, dan rumus, termasuk konsultasi lewat WhatsApp.")
    t = t.replace('<a class="btn arrow" href="/kertas-kerja/kertas-kerja-psak-%s-updatesak.xlsx" download data-us-kk="%s">Download Kertas Kerja PSAK %s</a>' % (n, n, n),
                  '<a class="btn arrow" href="%s" data-us-kk="%s">Dapatkan Kertas Kerja PSAK %s</a>' % (pay(n), n, n))
    assert "updatesak.xlsx" not in t, n
    wt(p, t)
p = os.path.join(US, "llms.txt"); t = rd(p)
t = t.replace("- [Kertas Kerja PSAK Gratis](https://updatesak.com/kertas-kerja/): template Excel PSAK 118, 116, 109, 115 berisi contoh, checklist, rumus, dan jurnal",
              "- [Kertas Kerja PSAK](https://updatesak.com/kertas-kerja/): template Excel PSAK 118, 116, 109, 115 berisi contoh, checklist, rumus, dan jurnal, termasuk konsultasi WhatsApp")
wt(p, t)
for d, _, fs in os.walk(US):
    for f in fs:
        if f.endswith(".html"):
            q = os.path.join(d, f); t = rd(q)
            if "updatesak.xlsx" in t or "Template Excel berumus, gratis." in t or "kertas kerja PSAK gratis" in t.lower():
                o = t
                t = t.replace("Template Excel berumus, gratis.", "Template Excel berumus, termasuk konsultasi.")
                t = re.sub(r"(?i)(kertas kerja PSAK) gratis", r"\1", t)
                assert "updatesak.xlsx" not in t, q
                if t != o: wt(q, t)

# ---------- 5. CariAkuntan ----------
p = os.path.join(CA, "cek-kebutuhan", "index.html"); t = rd(p)
t = t.replace("kertas kerja PSAK gratis", "kertas kerja PSAK")
wt(p, t)

print("us_kk_berbayar_20261113: %d file%s" % (N[0], " (dry)" if DRY else ""))
