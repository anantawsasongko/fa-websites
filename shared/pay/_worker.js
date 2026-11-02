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
  "ai-50":      { name: "Paket Asisten AI 50 Pertanyaan", price: 25000, kind: "ai", credits: 50 },
  "ai-300":     { name: "Paket Asisten AI 300 Pertanyaan", price: 99000, kind: "ai", credits: 300 },
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
async function access(st, env) {
  const key = prodFromOrder(st.order_id); if (!key) return null;
  const p = PRODUCTS[key];
  /* Sandbox: transaksi uji, kode lisensi asli tidak pernah diterbitkan */
  if (env && env.MIDTRANS_PRODUCTION !== "true") return { kind: "test", product: p.name, code: "MODE UJI: KODE TIDAK BERLAKU", exp: "" };
  if (p.kind === "lic") { const l = await licCode(st.order_id, p.lic, paidMs(st)); return { kind: "lic", product: p.name, code: l.code, exp: l.exp }; }
  if (p.kind === "ai") { const c = await aiCodeForOrder(env, st.order_id, p.credits); return { kind: "ai", product: p.name, code: c || "Kode AI dikirim via WhatsApp", exp: "" }; }
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
      acc && acc.kind === "ai" ? "Kode Asisten AI: " + acc.code : acc && acc.code ? "Kode Audit Ready: " + acc.code + " (s.d. " + acc.exp + ")" : acc && acc.kind === "ebook" ? "Kirim PDF + password e-book ke pembeli" : "Layanan: tindak lanjut manual"].join("\n"));
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
  if (paid) out.access = await access(st, env);
  return json(out);
}

async function notify(req, env, ctx) {
  let b; try { b = await req.json(); } catch (e) { return json({ ok: false }, 400); }
  const sig = hex(await sha("SHA-512", String(b.order_id) + String(b.status_code) + String(b.gross_amount) + env.MIDTRANS_SERVER_KEY));
  if (sig !== b.signature_key) return json({ ok: false, error: "signature" }, 403);
  /* Jangan percaya isi webhook mentah: ambil status resmi dari API. */
  const st = await midStatus(env, b.order_id);
  const paid = PAID.indexOf(st.transaction_status) >= 0 && st.fraud_status !== "deny";
  const acc = paid ? await access(st, env) : null;
  if (paid || ["expire", "cancel", "deny", "refund"].indexOf(st.transaction_status) >= 0) ctx.waitUntil(logSheet(st, acc, { company: st.custom_field1 }));
  return json({ ok: true });
}

/* ===================== Asisten AI (2 Nov 2026) =====================
   Aktif hanya bila kedua hal ini ada di Cloudflare Pages project faindonesia-web:
     ANTHROPIC_API_KEY  (Secret)  API key dari console.anthropic.com
     AI_ADMIN_KEY       (Secret)  kata sandi bebas untuk halaman /ai-admin/ (menerbitkan kode kredit dari pembayaran QRIS)
     AI_MODEL           (Text, opsional) default claude-haiku-5-5
     KV binding FA_AI   (Settings > Bindings > KV namespace) untuk saldo kredit dan kuota gratis
   Endpoint:
     GET  /api/ai/status            -> {enabled}
     GET  /api/ai/credit?code=      -> {credits}
     POST /api/ai/ask               -> {answer, credits|free}
     POST /api/ai/admin/new         -> {code}     (header x-admin: AI_ADMIN_KEY)
   Kuota gratis: 3 pertanyaan per perangkat dan 10 per IP per hari. Setelah itu wajib kode kredit (Paket AI). */
const AI_ORIGINS = ["https://faindonesia.co.id", "https://cariakuntan.com", "https://updatesak.com", "https://www.faindonesia.co.id", "https://www.cariakuntan.com", "https://www.updatesak.com"];
const AI_FREE_DEVICE = 3, AI_FREE_IP_DAY = 10, AI_MAX_CTX = 7000, AI_MAX_Q = 600;
const AI_APPS = {
  "kalkulator-pph-21": "Kalkulator PPh 21 TER (PP 58/2023, PMK 168/2023): tarif efektif rata-rata kategori A/B/C, perhitungan Desember pakai tarif Pasal 17, BPJS, gross-up.",
  "kalkulator-pph-badan": "Kalkulator PPh Badan: tarif umum 22%, fasilitas Pasal 31E, PPh final UMKM 0,5% (PP 55/2022), angsuran PPh 25.",
  "kalkulator-potput-ppn": "Kalkulator PPh potong pungut (23, 4 ayat 2, 26, 22 impor) dan PPN 12% dengan DPP nilai lain 11/12.",
  "kalkulator-penyusutan-fiskal": "Penyusutan fiskal (PMK 72/2023) vs komersial, beda temporer, pajak tangguhan PSAK 212.",
  "kalkulator-cicilan-pinjaman": "Simulasi cicilan pinjaman anuitas/efektif/flat, bunga efektif, DSCR, plafon maksimal.",
  "kalkulator-valuasi-dcf": "Valuasi DCF 5 tahun, WACC dengan CAPM, nilai terminal, sensitivitas.",
  "kalkulator-rasio-keuangan": "Rasio keuangan, siklus konversi kas, Altman Z'' untuk perusahaan privat.",
  "venus-kredit": "Cek kapasitas kredit dan pendanaan: DSCR, utang/EBITDA, DER, plafon indikatif, jalur IPO indikatif. Batas umum praktik bank (bukan regulasi): DSCR minimal sekitar 1,25x, utang/EBITDA sekitar 3,5x.",
  "cek-psak-118": "Konversi laba rugi ke format PSAK 118 (berlaku 1 Januari 2027): kategori operasi, investasi, pendanaan, pajak, operasi dihentikan; subtotal laba operasi dan laba sebelum pendanaan dan pajak.",
  "audit-ready": "FA Jupiter: penyusunan laporan keuangan dan CALK siap audit dari buku besar.",
  "saturn": "FA Saturn: kertas kerja audit KAP (materialitas, walkthrough, uji substantif, temuan).",
  "us-kalkulator": "Kalkulator UpdateSAK: menentukan kerangka SAK (SAK Indonesia, SAK EP, SAK EMKM, SAK Syariah), daftar PSAK per akun, kewajiban audit, dan penyusunan CALK."
};
function aiSystem(app) {
  return "Anda adalah Asisten AI FA Indonesia untuk akuntansi, perpajakan, kredit, dan standar akuntansi Indonesia. " +
    "Konteks aplikasi: " + (AI_APPS[app] || "aplikasi keuangan FA Indonesia.") + "\n" +
    "Aturan: jawab dalam Bahasa Indonesia yang mudah dipahami pemilik usaha, maksimal sekitar 250 kata. " +
    "Gunakan angka dari DATA HALAMAN bila ada dan sebutkan asumsi yang Anda pakai. " +
    "Jangan mengarang nomor peraturan, tarif, atau angka yang tidak ada di data; bila tidak yakin, katakan perlu dicek ke peraturan terbaru atau konsultan. " +
    "Jangan memakai tanda pisah panjang. Tutup dengan 1 sampai 3 langkah praktis. " +
    "Ini bukan pendapat profesional resmi; untuk keputusan penting sarankan diskusi dengan tim FA Indonesia.";
}
function aiHeaders(req) {
  const o = req.headers.get("origin") || "";
  const h = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex", "vary": "origin" };
  if (AI_ORIGINS.indexOf(o) >= 0) { h["access-control-allow-origin"] = o; h["access-control-allow-headers"] = "content-type, x-admin"; h["access-control-allow-methods"] = "GET, POST, OPTIONS"; }
  return h;
}
function aj(req, obj, status = 200) { return new Response(JSON.stringify(obj), { status, headers: aiHeaders(req) }); }
function aiOn(env) { return !!(env.ANTHROPIC_API_KEY && env.FA_AI); }
function aiNewCode() { return "FAI-" + rid(4) + "-" + rid(4) + "-" + rid(4); }
async function aiCodeForOrder(env, orderId, credits) {
  if (!env.FA_AI) return null;
  const k = "order:" + orderId; let c = await env.FA_AI.get(k);
  if (c) return c;
  c = aiNewCode(); await env.FA_AI.put("c:" + c, JSON.stringify({ credits, total: credits, order: orderId, at: Date.now() }));
  await env.FA_AI.put(k, c); return c;
}
async function aiAsk(req, env) {
  let b; try { b = await req.json(); } catch (e) { return aj(req, { error: "Data tidak terbaca" }, 400); }
  const app = clean(b.app, 60), device = clean(b.device, 64), code = clean(b.code, 30).toUpperCase();
  const q = clean(b.question, AI_MAX_Q), ctx = String(b.context == null ? "" : b.context).replace(/[\u0000-\u0008\u000b-\u001f]/g, " ").slice(0, AI_MAX_CTX);
  if (!q) return aj(req, { error: "Pertanyaan kosong" }, 400);
  if (!/^[A-Za-z0-9_-]{8,64}$/.test(device)) return aj(req, { error: "Perangkat tidak dikenali" }, 400);
  const ip = req.headers.get("cf-connecting-ip") || "0", day = new Date().toISOString().slice(0, 10);
  let rec = null, freeLeft = null;
  if (code) {
    rec = JSON.parse(await env.FA_AI.get("c:" + code) || "null");
    if (!rec) return aj(req, { error: "Kode kredit AI tidak dikenal", need: "code" }, 402);
    if (rec.credits <= 0) return aj(req, { error: "Kredit AI habis. Silakan beli paket baru.", need: "buy", credits: 0 }, 402);
  } else {
    const fd = +(await env.FA_AI.get("f:" + device) || 0), fi = +(await env.FA_AI.get("fi:" + ip + ":" + day) || 0);
    if (fd >= AI_FREE_DEVICE || fi >= AI_FREE_IP_DAY) return aj(req, { error: "Pertanyaan gratis sudah terpakai. Masukkan kode kredit AI atau beli paket.", need: "buy", free: 0 }, 402);
    freeLeft = AI_FREE_DEVICE - fd - 1;
    await env.FA_AI.put("f:" + device, String(fd + 1)); await env.FA_AI.put("fi:" + ip + ":" + day, String(fi + 1), { expirationTtl: 172800 });
  }
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model: env.AI_MODEL || "claude-haiku-5-5", max_tokens: 900, system: aiSystem(app),
      messages: [{ role: "user", content: "DATA HALAMAN (" + clean(b.page, 120) + "):\n" + (ctx || "(tidak ada)") + "\n\nPERTANYAAN:\n" + q }] })
  });
  const out = await r.json().catch(() => ({}));
  if (!r.ok) return aj(req, { error: "Asisten AI sedang sibuk, coba lagi sebentar lagi." }, 502);
  const answer = (out.content || []).filter((x) => x.type === "text").map((x) => x.text).join("\n").trim();
  if (rec) { rec.credits -= 1; rec.last = Date.now(); await env.FA_AI.put("c:" + code, JSON.stringify(rec)); return aj(req, { answer, credits: rec.credits }); }
  return aj(req, { answer, free: Math.max(0, freeLeft) });
}
async function aiRoute(req, env, url) {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: aiHeaders(req) });
  try {
    if (url.pathname === "/api/ai/status") return aj(req, { enabled: aiOn(env), free: AI_FREE_DEVICE });
    if (!aiOn(env)) return aj(req, { error: "Asisten AI belum aktif" }, 503);
    if (url.pathname === "/api/ai/credit") {
      const rec = JSON.parse(await env.FA_AI.get("c:" + clean(url.searchParams.get("code"), 30).toUpperCase()) || "null");
      return rec ? aj(req, { credits: rec.credits, total: rec.total }) : aj(req, { error: "Kode tidak dikenal" }, 404);
    }
    if (url.pathname === "/api/ai/ask" && req.method === "POST") return await aiAsk(req, env);
    if (url.pathname === "/api/ai/admin/new" && req.method === "POST") {
      if (!env.AI_ADMIN_KEY || req.headers.get("x-admin") !== env.AI_ADMIN_KEY) return aj(req, { error: "Tidak diizinkan" }, 403);
      let b; try { b = await req.json(); } catch (e) { b = {}; }
      const credits = Math.max(1, Math.min(5000, parseInt(b.credits, 10) || 50)), c = aiNewCode();
      await env.FA_AI.put("c:" + c, JSON.stringify({ credits, total: credits, note: clean(b.note, 200), at: Date.now() }));
      return aj(req, { code: c, credits });
    }
    return aj(req, { error: "Tidak ditemukan" }, 404);
  } catch (e) { return aj(req, { error: "Gangguan sementara" }, 500); }
}

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    if (url.pathname.startsWith("/api/ai/")) return aiRoute(req, env, url);
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
