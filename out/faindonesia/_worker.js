/* Pembayaran online FA Indonesia lewat Midtrans Snap (27 Okt 2026).
   Hanya route /api/* yang masuk ke sini (lihat _routes.json); halaman statis dilayani langsung oleh Pages,
   jadi _headers dan _redirects tetap berlaku.

   Environment variables di Cloudflare Pages project faindonesia-web (Settings > Variables and Secrets):
     MIDTRANS_SERVER_KEY   (Secret)  Server Key dari dashboard Midtrans
     MIDTRANS_CLIENT_KEY   (Text)    Client Key dari dashboard Midtrans
     MIDTRANS_PRODUCTION   (Text)    "true" untuk live, kosong/"false" untuk sandbox
   Selama MIDTRANS_SERVER_KEY belum diisi, tombol Bayar Online tidak tampil dan /bayar/ tetap pakai transfer manual.

   Endpoint:
     GET  /api/pay/config          -> {enabled, production, clientKey}
     POST /api/pay/create          -> {token, redirect_url, order_id}   (harga dihitung di server)
     GET  /api/pay/status?order_id -> status + akses (kode Audit Ready / info e-book) bila lunas
     POST /api/pay/notify          -> webhook Midtrans (Payment Notification URL), cek signature, log ke Google Sheet
*/
const PRODUCTS = {
  "ar-day":     { name: "FA Jupiter Audit Ready Day Pass", price: 39000,  kind: "lic", lic: "D" },
  "ar-year":    { name: "FA Jupiter Audit Ready Tahunan",  price: 249000, kind: "lic", lic: "Y" },
  "eb-psp":     { name: "E-book Prosedur Audit Substantif Primer", price: 129000, kind: "ebook" },
  "eb-auditee": { name: "E-book Audit untuk Auditee UMKM", price: 59000, kind: "ebook" },
  "eb-lkumkm":  { name: "E-book Menyusun Laporan Keuangan UMKM", price: 69000, kind: "ebook" },
  "eb-akmen":   { name: "E-book Akuntansi Manajemen untuk UMKM", price: 49000, kind: "ebook" },
  "eb-iso":     { name: "E-book Panduan ISO 22000", price: 59000, kind: "ebook" },
  "eb-makacua": { name: "E-book Social Responsibility Makacua", price: 39000, kind: "ebook" },
  "eb-paket":   { name: "Paket 6 E-book Penerbit FA", price: 299000, kind: "ebook" },
  "custom":     { name: "Layanan FA Indonesia", price: 0, kind: "service" }
};
const SITE = "https://faindonesia.co.id";
const SHEET = "https://script.google.com/macros/s/AKfycbzBAfPUXS1F9zcnRBz_Xg7-IhKRrLtyOtoNY9342G2gsXwgThcXwxcwq-VE3ywgK8Dniw/exec";
/* Sama persis dengan app Audit Ready (FA Jupiter): kode FAC-<D|Y><YYMMDD>-<4>-<cek4>. */
const LIC_SECRET = "fa-ar-7Qm2x9Lr-2026", ALPH = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const PAID = ["settlement", "capture"];

const enc = new TextEncoder();
const hex = (buf) => Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, "0")).join("");
async function sha(alg, s) { return crypto.subtle.digest(alg, enc.encode(s)); }
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" } });
}
function api(env) { return env.MIDTRANS_PRODUCTION === "true" ? "https://api.midtrans.com" : "https://api.sandbox.midtrans.com"; }
function snapApi(env) { return env.MIDTRANS_PRODUCTION === "true" ? "https://app.midtrans.com" : "https://app.sandbox.midtrans.com"; }
function auth(env) { return "Basic " + btoa(env.MIDTRANS_SERVER_KEY + ":"); }
function clean(s, n) { return String(s == null ? "" : s).replace(/[\u0000-\u001f<>]/g, " ").trim().slice(0, n); }
function rid(n) { const a = new Uint8Array(n); crypto.getRandomValues(a); return Array.from(a, (x) => ALPH[x % 32]).join(""); }
function jktDate(ms) { return new Date(ms + 7 * 36e5); }
function yymmdd(d) { return d.toISOString().slice(2, 10).replace(/-/g, ""); }

/* Kode akses Audit Ready, deterministik per order (refresh halaman = kode sama). */
async function licCode(orderId, type, paidAtMs) {
  const d = jktDate(paidAtMs);
  if (type === "Y") d.setUTCFullYear(d.getUTCFullYear() + 1); else d.setUTCDate(d.getUTCDate() + 1);
  const exp = yymmdd(d);
  const h = new Uint8Array(await sha("SHA-256", LIC_SECRET + "|order|" + orderId));
  const mid = Array.from(h.slice(0, 4), (x) => ALPH[x % 32]).join("");
  const body = type + exp + "-" + mid;
  const c = new Uint8Array(await sha("SHA-256", LIC_SECRET + "|" + body));
  const chk = Array.from(c.slice(0, 4), (x) => ALPH[x % 32]).join("");
  return { code: "FAC-" + body + "-" + chk, exp: exp.slice(4, 6) + "/" + exp.slice(2, 4) + "/20" + exp.slice(0, 2) };
}
/* order_id: FA-<YYMMDD>-<produk>-<acak>; produk dibaca balik dari order_id. */
function prodFromOrder(id) { const m = /^FA-\d{6}-([a-z0-9-]+?)-[A-Z2-9]{8}$/.exec(id || ""); return m && PRODUCTS[m[1]] ? m[1] : null; }
function paidMs(st) {
  const t = st.settlement_time || st.transaction_time;
  const ms = t ? Date.parse(t.replace(" ", "T") + "+07:00") : NaN;
  return isNaN(ms) ? Date.now() : ms;
}
async function access(st) {
  const key = prodFromOrder(st.order_id); if (!key) return null;
  const p = PRODUCTS[key];
  if (p.kind === "lic") { const l = await licCode(st.order_id, p.lic, paidMs(st)); return { kind: "lic", product: p.name, code: l.code, exp: l.exp }; }
  return { kind: p.kind, product: p.name };
}
async function logSheet(st, acc, extra) {
  try {
    const p = new URLSearchParams();
    p.append("pt", extra.company || "-");
    p.append("email", st.customer_details && st.customer_details.email || extra.email || "");
    p.append("nama", st.customer_details && st.customer_details.first_name || extra.name || "");
    p.append("wa", extra.phone ? "'" + extra.phone : "");
    p.append("goal", "FA Pembayaran Midtrans: " + st.transaction_status + " | " + (acc ? acc.product : st.order_id));
    p.append("unit", "Rp " + st.gross_amount);
    p.append("lang", "id");
    p.append("page", "faindonesia.co.id/bayar/ (" + st.payment_type + ")");
    p.append("summary", ["Order " + st.order_id, "Status " + st.transaction_status + (st.fraud_status ? " / fraud " + st.fraud_status : ""),
      "Metode " + st.payment_type, "Nominal Rp " + st.gross_amount, "Waktu " + (st.settlement_time || st.transaction_time || "-"),
      acc && acc.code ? "Kode Audit Ready: " + acc.code + " (s.d. " + acc.exp + ")" : acc && acc.kind === "ebook" ? "Kirim PDF + password e-book ke pembeli" : "Layanan: tindak lanjut manual"].join("\n"));
    await fetch(SHEET, { method: "POST", body: p, redirect: "manual" });
  } catch (e) {}
}
async function midStatus(env, id) {
  const r = await fetch(api(env) + "/v2/" + encodeURIComponent(id) + "/status", { headers: { authorization: auth(env), accept: "application/json" } });
  return r.json();
}

async function create(req, env) {
  let b; try { b = await req.json(); } catch (e) { return json({ error: "Data tidak terbaca" }, 400); }
  const key = String(b.prod || ""); const p = PRODUCTS[key];
  if (!p) return json({ error: "Produk tidak dikenal" }, 400);
  if (!b.agree) return json({ error: "Centang persetujuan Syarat & Ketentuan dulu" }, 400);
  const nm = clean(b.nm, 60), em = clean(b.em, 80), ph = clean(b.ph, 20).replace(/[^\d+]/g, ""), co = clean(b.co, 80), nt = clean(b.nt, 200);
  if (!nm || !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(em)) return json({ error: "Isi nama dan email yang valid" }, 400);
  let qty = Math.max(1, Math.min(p.kind === "lic" ? 1 : 20, parseInt(b.qty, 10) || 1));
  let price = p.price, name = p.name;
  if (key === "custom") {
    price = Math.round(Number(String(b.amt || "").replace(/\D/g, "")));
    name = clean(b.desc, 50) || p.name; qty = 1;
    if (!(price >= 10000 && price <= 500000000)) return json({ error: "Nominal layanan Rp10.000 sampai Rp500 juta" }, 400);
  }
  const id = "FA-" + yymmdd(jktDate(Date.now())) + "-" + key + "-" + rid(8);
  const payload = {
    transaction_details: { order_id: id, gross_amount: price * qty },
    item_details: [{ id: key, price, quantity: qty, name: name.slice(0, 50), merchant_name: "CV FA Indonesia" }],
    customer_details: { first_name: nm, email: em, phone: ph || undefined, billing_address: co ? { first_name: nm, address: co.slice(0, 200) } : undefined },
    custom_field1: co.slice(0, 255), custom_field2: nt.slice(0, 255), custom_field3: clean(b.src, 60),
    callbacks: { finish: SITE + "/bayar/selesai/" },
    expiry: { unit: "hours", duration: 24 }
  };
  const r = await fetch(snapApi(env) + "/snap/v1/transactions", {
    method: "POST", headers: { authorization: auth(env), "content-type": "application/json", accept: "application/json" }, body: JSON.stringify(payload)
  });
  const out = await r.json().catch(() => ({}));
  if (!r.ok || !out.token) return json({ error: "Gateway menolak: " + ((out.error_messages || []).join("; ") || r.status) }, 502);
  return json({ token: out.token, redirect_url: out.redirect_url, order_id: id, amount: price * qty });
}

async function status(url, env) {
  const id = url.searchParams.get("order_id") || "";
  if (!/^FA-\d{6}-[a-z0-9-]+-[A-Z2-9]{8}$/.test(id)) return json({ error: "Nomor order tidak valid" }, 400);
  const st = await midStatus(env, id);
  if (!st || !st.transaction_status) return json({ order_id: id, transaction_status: "not_found" });
  const out = { order_id: id, transaction_status: st.transaction_status, payment_type: st.payment_type, gross_amount: st.gross_amount, expiry_time: st.expiry_time || null };
  const paid = PAID.indexOf(st.transaction_status) >= 0 && st.fraud_status !== "deny" && st.fraud_status !== "challenge";
  out.paid = paid;
  if (paid) out.access = await access(st);
  return json(out);
}

async function notify(req, env, ctx) {
  let b; try { b = await req.json(); } catch (e) { return json({ ok: false }, 400); }
  const sig = hex(await sha("SHA-512", String(b.order_id) + String(b.status_code) + String(b.gross_amount) + env.MIDTRANS_SERVER_KEY));
  if (sig !== b.signature_key) return json({ ok: false, error: "signature" }, 403);
  /* Jangan percaya isi webhook mentah: ambil status resmi dari API. */
  const st = await midStatus(env, b.order_id);
  const paid = PAID.indexOf(st.transaction_status) >= 0 && st.fraud_status !== "deny";
  const acc = paid ? await access(st) : null;
  if (paid || ["expire", "cancel", "deny", "refund"].indexOf(st.transaction_status) >= 0) ctx.waitUntil(logSheet(st, acc, { company: st.custom_field1 }));
  return json({ ok: true });
}

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    if (!url.pathname.startsWith("/api/pay/")) return env.ASSETS.fetch(req);
    const ck = env.MIDTRANS_CLIENT_KEY || "";
    /* Pengaman: jangan pernah kirim Server Key ke browser walau salah diisi di variabel Client Key. */
    const ckOk = !!ck && ck !== env.MIDTRANS_SERVER_KEY && !/server/i.test(ck);
    const on = !!env.MIDTRANS_SERVER_KEY && !/client/i.test(env.MIDTRANS_SERVER_KEY);
    try {
      if (url.pathname === "/api/pay/config") return json({ enabled: on && ckOk, production: env.MIDTRANS_PRODUCTION === "true", clientKey: on && ckOk ? ck : "", ...(on && !ckOk ? { note: "Client Key belum benar" } : {}) });
      if (!on) return json({ error: "Pembayaran online belum aktif. Silakan pakai transfer bank." }, 503);
      if (url.pathname === "/api/pay/create" && req.method === "POST") return await create(req, env);
      if (url.pathname === "/api/pay/status" && req.method === "GET") return await status(url, env);
      if (url.pathname === "/api/pay/notify" && req.method === "POST") return await notify(req, env, ctx);
      return json({ error: "Tidak ditemukan" }, 404);
    } catch (e) {
      return json({ error: "Gangguan sementara, coba lagi atau pakai transfer bank." }, 500);
    }
  }
};
