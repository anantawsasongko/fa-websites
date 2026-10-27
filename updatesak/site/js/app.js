/* UpdateSAK: Kalkulator Standar dan Kalkulator CALK. Semua hitungan di browser, tanpa server. */
(() => {
"use strict";
const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

/* ---------- Baris input ---------- */
// [id, label, kelompok, tanda]  tanda: 1 tambah, -1 kurang (diisi positif), 0 bebas (±)
const ROWS = [
  ["#", "Aset Lancar"],
  ["kas", "Kas dan Setara Kas", "AL", 1],
  ["piu3", "Piutang Usaha: Pihak Ketiga (Bruto)", "AL", 1],
  ["piurel", "Piutang Usaha: Pihak Berelasi", "AL", 1],
  ["cke", "Dikurangi Cadangan Kerugian Penurunan Nilai Piutang", "AL", -1],
  ["piulain", "Piutang Lain-Lain", "AL", 1],
  ["asetkontrak", "Aset Kontrak", "AL", 1],
  ["persediaan", "Persediaan", "AL", 1],
  ["uangmuka", "Uang Muka dan Biaya Dibayar di Muka", "AL", 1],
  ["pajakdm", "Pajak Dibayar di Muka", "AL", 1],
  ["=AL", "Jumlah Aset Lancar"],
  ["#", "Aset Tidak Lancar"],
  ["atbiaya", "Aset Tetap: Biaya Perolehan", "ATL", 1],
  ["atakum", "Dikurangi Akumulasi Penyusutan Aset Tetap", "ATL", -1],
  ["rou", "Aset Hak Guna (Neto)", "ATL", 1],
  ["propinv", "Properti Investasi", "ATL", 1],
  ["atb", "Aset Takberwujud (Neto)", "ATL", 1],
  ["invasos", "Investasi pada Entitas Asosiasi dan Ventura Bersama", "ATL", 1],
  ["apt", "Aset Pajak Tangguhan", "ATL", 1],
  ["atllain", "Aset Tidak Lancar Lainnya", "ATL", 1],
  ["=ATL", "Jumlah Aset Tidak Lancar"],
  ["=ASET", "Jumlah Aset"],
  ["#", "Liabilitas Jangka Pendek"],
  ["ubpendek", "Utang Bank Jangka Pendek", "LPD", 1],
  ["uu3", "Utang Usaha: Pihak Ketiga", "LPD", 1],
  ["uurel", "Utang Usaha: Pihak Berelasi", "LPD", 1],
  ["ul", "Utang Lain-Lain", "LPD", 1],
  ["akrual", "Beban Akrual", "LPD", 1],
  ["utangpajak", "Utang Pajak", "LPD", 1],
  ["liabkontrak", "Liabilitas Kontrak / Uang Muka Pelanggan", "LPD", 1],
  ["ublancar", "Bagian Lancar Utang Bank Jangka Panjang", "LPD", 1],
  ["sewalancar", "Bagian Lancar Liabilitas Sewa", "LPD", 1],
  ["=LPD", "Jumlah Liabilitas Jangka Pendek"],
  ["#", "Liabilitas Jangka Panjang"],
  ["ubpanjang", "Utang Bank Jangka Panjang, Setelah Dikurangi Bagian Lancar", "LPJ", 1],
  ["sewapanjang", "Liabilitas Sewa, Setelah Dikurangi Bagian Lancar", "LPJ", 1],
  ["imbalan", "Liabilitas Imbalan Kerja", "LPJ", 1],
  ["lpt", "Liabilitas Pajak Tangguhan", "LPJ", 1],
  ["utangrel", "Utang Pihak Berelasi Jangka Panjang", "LPJ", 1],
  ["=LPJ", "Jumlah Liabilitas Jangka Panjang"],
  ["=LIAB", "Jumlah Liabilitas"],
  ["#", "Ekuitas"],
  ["modal", "Modal Saham", "EK", 1],
  ["tmd", "Tambahan Modal Disetor", "EK", 1],
  ["saldolaba", "Saldo Laba (±)", "EK", 0],
  ["ociek", "Penghasilan Komprehensif Lain Akumulasian (±)", "EK", 0],
  ["=EK", "Jumlah Ekuitas"],
  ["=LE", "Jumlah Liabilitas dan Ekuitas"],
  ["#", "Laba Rugi dan Penghasilan Komprehensif Lain"],
  ["pendapatan", "Pendapatan", "PL", 1],
  ["hpp", "Beban Pokok Pendapatan", "PL", -1],
  ["=LK", "Laba Bruto"],
  ["bjual", "Beban Penjualan", "PL", -1],
  ["bumum", "Beban Umum dan Administrasi", "PL", -1],
  ["lain", "Pendapatan (Beban) Lain-Lain, Neto (±)", "PL", 0],
  ["=LU", "Laba Usaha"],
  ["pkeu", "Pendapatan Keuangan", "PL", 1],
  ["bkeu", "Beban Keuangan", "PL", -1],
  ["=LSBP", "Laba Sebelum Pajak Penghasilan"],
  ["pajakkini", "Beban Pajak Kini", "PL", -1],
  ["pajaktgh", "Beban (Manfaat) Pajak Tangguhan (±)", "PL", 0],
  ["=LB", "Laba Tahun Berjalan"],
  ["oci", "Penghasilan Komprehensif Lain Tahun Berjalan (±)", "PL", 0],
  ["=TCI", "Jumlah Penghasilan Komprehensif Tahun Berjalan"]
];
const IDS = ROWS.filter(r => r[2]).map(r => r[0]);

/* ---------- Format angka ---------- */
const parse = s => {
  s = String(s ?? "").trim(); if (!s) return 0;
  const neg = /^\(.*\)$/.test(s) || /^-/.test(s);
  const n = Number(s.replace(/[^\d]/g, "")) || 0;
  return neg ? -n : n;
};
const idn = n => Math.round(Math.abs(n)).toLocaleString("id-ID");
const fmtIn = n => n ? (n < 0 ? "-" : "") + idn(n) : "";
const fmt = n => !Math.round(n) ? "-" : (n < 0 ? "(" + idn(n) + ")" : idn(n));
const jt = n => (n / 1e9).toLocaleString("id-ID", {maximumFractionDigits: 1}) + " M";

/* ---------- Bangun tabel input ---------- */
const rowHtml = ([id, lab]) => {
  if (id === "#") return `<tr class="sec"><td colspan="3">${lab}</td></tr>`;
  if (id[0] === "=") return `<tr class="tot"><td>${lab}</td><td class="num" data-t="${id.slice(1)}" data-y="1">-</td><td class="num" data-t="${id.slice(1)}" data-y="0">-</td></tr>`;
  return `<tr><td>${lab}</td><td><input inputmode="decimal" data-id="${id}" data-y="1" aria-label="${lab} tahun berjalan"></td><td><input inputmode="decimal" data-id="${id}" data-y="0" aria-label="${lab} tahun lalu"></td></tr>`;
};
const cut = ROWS.findIndex(r => r[0] === "#" && r[1].startsWith("Laba Rugi"));
$("#finBS tbody").innerHTML = ROWS.slice(0, cut).map(rowHtml).join("");
$("#finPL tbody").innerHTML = ROWS.slice(cut + 1).map(rowHtml).join("");

function read() {
  const v = {}; IDS.forEach(id => v[id] = [0, 0]);
  $$(".finx input").forEach(i => v[i.dataset.id][+i.dataset.y] = parse(i.value));
  const f = Object.fromEntries(new FormData($("#form")).entries());
  $$("#flags input").forEach(c => f[c.name] = c.checked);
  return {v, f, t: totals(v)};
}
function totals(v) {
  const t = {};
  for (const y of [0, 1]) {
    const sum = k => ROWS.filter(r => r[2] === k).reduce((s, r) => s + (r[3] === -1 ? -Math.abs(v[r[0]][y]) : v[r[0]][y]), 0);
    const T = {};
    T.AL = sum("AL"); T.ATL = sum("ATL"); T.ASET = T.AL + T.ATL;
    T.LPD = sum("LPD"); T.LPJ = sum("LPJ"); T.LIAB = T.LPD + T.LPJ;
    T.EK = sum("EK"); T.LE = T.LIAB + T.EK;
    const a = id => v[id][y];
    T.LK = a("pendapatan") - Math.abs(a("hpp"));
    T.LU = T.LK - Math.abs(a("bjual")) - Math.abs(a("bumum")) + a("lain");
    T.LSBP = T.LU + a("pkeu") - Math.abs(a("bkeu"));
    T.PAJAK = Math.abs(a("pajakkini")) + a("pajaktgh");
    T.LB = T.LSBP - T.PAJAK;
    T.TCI = T.LB + a("oci");
    T.BANK = a("ubpendek") + a("ublancar") + a("ubpanjang");
    T.SEWA = a("sewalancar") + a("sewapanjang");
    T.PIU = a("piu3") + a("piurel") - Math.abs(a("cke"));
    T.AT = a("atbiaya") - Math.abs(a("atakum"));
    t[y] = T;
  }
  return t;
}
function refresh() {
  live();
  const {v, t} = read();
  $$(".finx td[data-t]").forEach(td => td.textContent = fmt(t[+td.dataset.y][td.dataset.t]));
  const any = IDS.some(id => v[id][1]);
  const el = $("#cek");
  if (!any) { el.className = "chk"; el.textContent = "⚖️ Cek Balance: isi angka, nanti terlihat apakah Total Aset sudah sama dengan Liabilitas + Ekuitas."; return; }
  const msg = [];
  for (const y of [1, 0]) {
    if (y === 0 && !IDS.some(id => v[id][0])) continue;
    const d = t[y].ASET - t[y].LE;
    msg.push((y ? "Tahun berjalan: " : "Tahun lalu: ") + (Math.abs(d) < 1 ? "✅ Balance" : "❌ Belum balance, selisih Rp" + idn(d) + (d > 0 ? " (aset lebih besar)" : " (liabilitas + ekuitas lebih besar)")));
  }
  const bad = msg.some(m => m.includes("selisih"));
  el.className = "chk" + (bad ? " bad" : "");
  el.textContent = msg.join(" · ") + (bad ? ". Hasil tetap bisa dibuat, tapi cek lagi angkanya." : "");
}
$$(".finx").forEach(tb => tb.addEventListener("input", refresh));
$$(".finx").forEach(tb => tb.addEventListener("focusout", e => { if (e.target.matches("input")) { e.target.value = fmtIn(parse(e.target.value)); refresh(); } }));

/* ---------- Mode ---------- */
let mode = "std";
function setMode(m) {
  mode = m;
  $$(".modes button").forEach(b => b.setAttribute("aria-pressed", b.dataset.mode === m));
  $$(".stepnav .calk-only").forEach(e => e.hidden = m !== "calk");
  $("#go").textContent = m === "calk" ? "Susun CALK" : "Cek Standar";
  if (m !== "calk" && step > 2) goStep(2); else goStep(step);
}
let step = 0;
function lastStep() { return mode === "calk" ? 3 : 2; }
function goStep(n) {
  step = Math.max(0, Math.min(n, lastStep()));
  $$(".stepnav button").forEach(b => b.setAttribute("aria-selected", +b.dataset.step === step));
  $$(".pane").forEach(p => p.classList.toggle("on", +p.dataset.pane === step));
  $("#prev").hidden = step === 0;
  $("#next").hidden = step === lastStep();
  $("#go").hidden = step !== lastStep();
}
$$(".stepnav button").forEach(b => b.onclick = () => goStep(+b.dataset.step));
$("#next").onclick = () => goStep(step + 1);
$("#prev").onclick = () => goStep(step - 1);
$$(".modes button").forEach(b => b.onclick = () => setMode(b.dataset.mode));
$$(".need[data-mode]").forEach(a => a.addEventListener("click", () => setMode(a.dataset.mode)));
const yearLabels = () => { const y = +($("[name=tahun]").value || 2026); $$("#finBS .th1").forEach(e => e.textContent = "31 Des " + y); $$("#finBS .th0").forEach(e => e.textContent = "31 Des " + (y - 1)); $$("#finPL .th1").forEach(e => e.textContent = y); $$("#finPL .th0").forEach(e => e.textContent = y - 1); };
$("[name=tahun]").addEventListener("change", yearLabels); yearLabels();

/* ---------- Mesin standar ---------- */
const PP7 = [ // PP 7/2021: kriteria hasil penjualan tahunan
  [2e9, "Usaha Mikro"], [15e9, "Usaha Kecil"], [50e9, "Usaha Menengah"]
];
function analyze(d) {
  const {v, f, t} = d, T = t[1], has = id => v[id][1] || v[id][0];
  const rev = v.pendapatan[1], aset = T.ASET, eq = T.EK;
  const st = f.status;
  const r = {reasons: [], items: [], news: [], audit: [], umkm: null};
  const kelas = PP7.find(([lim]) => rev <= lim);
  r.umkm = kelas ? kelas[1] : "Usaha Besar (di atas kriteria UMKM)";
  // Kerangka
  if (["tbk", "ipo", "lk"].includes(st) || f.f_obligasi) {
    r.fw = "sak"; r.fwName = "SAK Indonesia"; r.wajib = true;
    r.reasons.push(st === "tbk" ? "Perusahaan Terbuka memiliki akuntabilitas publik dan wajib memakai SAK Indonesia." :
      st === "ipo" ? "Entitas yang sedang mengajukan pernyataan pendaftaran ke OJK diperlakukan memiliki akuntabilitas publik, sehingga laporan keuangan untuk prospektus disusun dengan SAK Indonesia." :
      st === "lk" ? "Bank, asuransi, dana pensiun, dan lembaga yang menghimpun dana masyarakat memiliki akuntabilitas publik." :
      "Penerbitan efek utang kepada publik menimbulkan akuntabilitas publik.");
  } else if (st === "anak") {
    r.fw = "sak"; r.fwName = "SAK Indonesia"; r.wajib = false;
    r.reasons.push("Sebagai entitas anak, angka Anda dikonsolidasikan ke induk yang memakai SAK Indonesia. Memakai kerangka yang sama menghindari penyesuaian ganda saat konsolidasi.");
    r.reasons.push("Mulai 1 Januari 2027 PSAK 119 mengizinkan pengungkapan yang lebih ringkas bagi entitas anak tanpa akuntabilitas publik.");
  } else if (st === "bumn") {
    r.fw = "sak"; r.fwName = "SAK Indonesia"; r.wajib = true;
    r.reasons.push("Praktik pelaporan BUMN/BUMD dan ketentuan kementerian pembina umumnya mensyaratkan SAK Indonesia.");
  } else if (kelas && !f.f_kredit && !f.f_anak && aset <= 10e9) {
    r.fw = "emkm"; r.fwName = "SAK EMKM"; r.wajib = false;
    r.reasons.push(`Hasil penjualan Rp${jt(rev)} masuk kriteria ${kelas[1]} (PP 7/2021), sehingga SAK EMKM dapat dipakai.`);
    r.reasons.push("Jika perusahaan berencana mengajukan kredit bank atau tumbuh di atas kriteria UMKM, siapkan migrasi ke SAK EP.");
  } else {
    r.fw = "ep"; r.fwName = "SAK EP"; r.wajib = false;
    r.reasons.push("Perusahaan tidak memiliki akuntabilitas publik, sehingga dapat memakai SAK Indonesia untuk Entitas Privat (berlaku sejak 1 Januari 2025, menggantikan SAK ETAP).");
    if (kelas) r.reasons.push(`Hasil penjualan masuk kriteria ${kelas[1]}, tetapi ${f.f_kredit ? "fasilitas kredit bank" : f.f_anak ? "kewajiban konsolidasi" : "skala aset"} membuat SAK EP lebih tepat dibanding SAK EMKM.`);
    r.reasons.push("Jika ada rencana IPO dalam 2 sampai 3 tahun, pertimbangkan langsung memakai SAK Indonesia agar tidak perlu menyajikan ulang angka historis.");
  }
  if (st === "nonlaba") r.reasons.push("Untuk entitas berorientasi nonlaba, penyajian mengikuti ISAK 335 (diamendemen 1 Januari 2027 seiring PSAK 118) bila memakai SAK Indonesia.");
  if (f.f_syariah) r.reasons.push("Transaksi berbasis akad syariah juga tunduk pada SAK Syariah (PSAK 4xx dan ISAK 4xx).");

  const S = r.fw === "sak";
  const add = (psak, topik, why, fokus, cond = true) => { if (cond) r.items.push({psak, topik, why, fokus}); };
  // Umum
  add(r.fwName === "SAK Indonesia" ? "PSAK 201" : "Penyajian LK", "Penyajian Laporan Keuangan", "Berlaku untuk semua entitas. Menentukan komponen laporan, klasifikasi lancar/tidak lancar, dan pengungkapan kebijakan akuntansi material.", S ? "Diganti PSAK 118 mulai 1 Januari 2027." : "Konsistensi klasifikasi dan komparatif.");
  add(S ? "PSAK 207" : "Arus Kas", "Laporan Arus Kas", "Wajib disajikan.", "Klasifikasi bunga dan dividen, transaksi nonkas, rekonsiliasi liabilitas pendanaan.", r.fw !== "emkm");
  add(S ? "PSAK 208" : "Kebijakan Akuntansi", "Kebijakan Akuntansi, Perubahan Estimasi, dan Kesalahan", "Dasar penyajian ulang bila ada koreksi tahun lalu.", "Koreksi kesalahan material wajib disajikan ulang secara retrospektif.");
  add(S ? "PSAK 210" : "Peristiwa Setelah Periode", "Peristiwa setelah Periode Pelaporan", "Semua entitas.", "Kejadian sampai tanggal otorisasi laporan keuangan.");
  add(S ? "PSAK 224" : "Pihak Berelasi", "Pengungkapan Pihak-Pihak Berelasi", "Ada saldo atau transaksi dengan pihak berelasi.", "Kelengkapan daftar pihak berelasi dan kompensasi manajemen kunci.", has("piurel") || has("uurel") || has("utangrel") || r.fw !== "emkm");
  // Instrumen keuangan
  const fi = has("kas") || has("piu3") || has("uu3") || T.BANK;
  add(S ? "PSAK 109" : "Instrumen Keuangan Dasar", "Instrumen Keuangan: Klasifikasi, Pengukuran, Penurunan Nilai", "Kas, piutang, utang usaha, dan pinjaman bank adalah instrumen keuangan.", S ? "Model kerugian kredit ekspektasian (ECL) untuk piutang; biaya perolehan diamortisasi dengan suku bunga efektif untuk pinjaman." : "Penurunan nilai piutang dan pengukuran pinjaman.", fi);
  add("PSAK 107", "Instrumen Keuangan: Pengungkapan", "Pengungkapan risiko kredit, likuiditas, dan pasar.", "Tabel jatuh tempo liabilitas keuangan dan eksposur risiko kredit.", fi && S);
  add("PSAK 232", "Instrumen Keuangan: Penyajian", "Klasifikasi utang vs ekuitas dan saling hapus.", "Pinjaman pemegang saham dan instrumen campuran.", fi && S);
  add(S ? "PSAK 113" : "Nilai Wajar", "Pengukuran Nilai Wajar", "Dipakai bila ada aset/liabilitas yang diukur atau diungkapkan pada nilai wajar.", "Hierarki nilai wajar dan teknik penilaian.", S && (has("propinv") || f.f_obligasi || f.f_valas));
  // Pendapatan
  add(S ? "PSAK 115" : "Pendapatan", "Pendapatan dari Kontrak dengan Pelanggan", f.f_kontrak ? "Pendapatan proyek diakui sepanjang waktu berdasarkan progres." : "Pendapatan diakui saat pengendalian barang/jasa beralih.", f.f_kontrak ? "Metode pengukuran progres, aset dan liabilitas kontrak, kontrak merugi, retensi." : "Pisahkan kewajiban pelaksanaan, diskon, dan retur.", has("pendapatan"));
  // Persediaan dsb
  add(S ? "PSAK 202" : "Persediaan", "Persediaan", "Ada saldo persediaan.", "Nilai realisasi neto, persediaan usang, dan metode biaya (FIFO/rata-rata).", has("persediaan"));
  add(S ? "PSAK 216" : "Properti, Pabrik, dan Peralatan", "Aset Tetap", "Ada aset tetap.", "Umur manfaat, komponen signifikan, model biaya vs revaluasi, aset dijaminkan.", has("atbiaya"));
  add(S ? "PSAK 236" : "Penurunan Nilai Aset", "Penurunan Nilai Aset", "Aset nonkeuangan wajib diuji bila ada indikasi penurunan nilai.", "Indikasi penurunan nilai dan perhitungan jumlah terpulihkan.", has("atbiaya") || has("atb") || has("invasos"));
  add(S ? "PSAK 116" : "Sewa", "Sewa", "Ada aset hak guna atau liabilitas sewa.", S ? "Pengakuan aset hak guna dan liabilitas sewa, pengecualian sewa jangka pendek dan aset bernilai rendah." : "Sewa pembiayaan vs sewa operasi.", has("rou") || T.SEWA);
  add(S ? "PSAK 240" : "Properti Investasi", "Properti Investasi", "Ada properti yang disewakan atau dimiliki untuk kenaikan nilai.", "Pilihan model biaya atau nilai wajar.", has("propinv"));
  add(S ? "PSAK 238" : "Aset Takberwujud", "Aset Takberwujud", "Ada perangkat lunak, lisensi, atau aset takberwujud lain.", "Kapitalisasi biaya pengembangan dan umur manfaat.", has("atb"));
  add(S ? "PSAK 228" : "Investasi pada Entitas Asosiasi", "Investasi pada Entitas Asosiasi dan Ventura Bersama", "Ada investasi dengan pengaruh signifikan.", "Metode ekuitas; amendemen opsi nilai wajar berlaku bersamaan PSAK 118.", has("invasos"));
  add(S ? "PSAK 223" : "Biaya Pinjaman", "Biaya Pinjaman", "Ada pinjaman bank.", "Kapitalisasi bunga ke aset kualifikasian (proyek/gedung dalam pembangunan).", T.BANK > 0);
  add(S ? "PSAK 219" : "Imbalan Kerja", "Imbalan Kerja", "Ada liabilitas imbalan pascakerja (UU 6/2023 dan PP 35/2021).", "Laporan aktuaris, asumsi diskonto dan kenaikan gaji, pengukuran kembali di penghasilan komprehensif lain.", has("imbalan") || r.fw !== "emkm");
  add(S ? "PSAK 212" : "Pajak Penghasilan", "Pajak Penghasilan", "Ada beban pajak, utang pajak, atau pajak tangguhan.", S ? "Rekonsiliasi tarif efektif, pajak tangguhan, posisi pajak tidak pasti (ISAK 123)." : "Rekonsiliasi fiskal dan pajak tangguhan.", has("pajakkini") || has("utangpajak") || has("apt") || has("lpt"));
  add(S ? "PSAK 237" : "Provisi", "Provisi, Liabilitas Kontinjensi, dan Aset Kontinjensi", "Garansi, sengketa pajak, atau kasus hukum.", "Kelengkapan provisi dan pengungkapan kontinjensi.");
  // Flag
  add(S ? "PSAK 221" : "Transaksi Valuta Asing", "Pengaruh Perubahan Kurs Valuta Asing", "Ada transaksi atau saldo valuta asing.", "Kurs penjabaran akhir periode (JISDOR) dan selisih kurs di laba rugi.", f.f_valas);
  add("PSAK 110 · 112 · 227", "Konsolidasi dan Pengungkapan Kepentingan pada Entitas Lain", "Ada entitas anak.", "Analisis pengendalian, eliminasi transaksi antarperusahaan, kepentingan nonpengendali.", f.f_anak && S);
  add(S ? "PSAK 220" : "Hibah Pemerintah", "Akuntansi Hibah Pemerintah", "Menerima hibah atau bantuan pemerintah.", "Pengakuan pendapatan tangguhan dan syarat hibah.", f.f_hibah);
  add("PSAK 102", "Pembayaran Berbasis Saham", "Ada program saham/opsi karyawan.", "Nilai wajar pada tanggal pemberian dan periode vesting.", f.f_saham && S);
  add("PSAK 103 · 338", "Kombinasi Bisnis dan Kombinasi Bisnis Entitas Sepengendali", "Ada akuisisi atau merger.", "Alokasi harga beli, goodwill, atau metode penyatuan kepemilikan bila sepengendali.", f.f_akuisisi && S);
  add("PSAK 233 · 108 · 234", "Laba per Saham, Segmen Operasi, Laporan Interim", "Perusahaan terbuka atau sedang IPO.", "Laba per saham dasar/dilusian dan informasi segmen.", ["tbk", "ipo"].includes(st));
  add(S ? "PSAK 241" : "Agrikultur", "Agrikultur", "Ada aset biologis.", "Nilai wajar dikurangi biaya untuk menjual.", $("[name=industri]").value === "agri");
  add("PSAK 106 · ISAK 101", "Eksplorasi Mineral dan Liabilitas Restorasi", "Usaha pertambangan.", "Kapitalisasi biaya eksplorasi dan provisi reklamasi.", $("[name=industri]").value === "tambang" && S);
  add("PSAK 402 · 405 · 406 · 407", "SAK Syariah: Murabahah, Mudharabah, Musyarakah, Ijarah", "Ada akad syariah.", "Pilih PSAK syariah sesuai akad; PSAK 401 berlaku 1 Januari 2027.", f.f_syariah);
  add("ISAK 335", "Penyajian Laporan Keuangan Entitas Berorientasi Nonlaba", "Entitas nonlaba.", "Aset neto dengan dan tanpa pembatasan.", st === "nonlaba");

  // Standar baru
  const nw = (eff, psak, judul, dampak, cond = true) => { if (cond) r.news.push({eff, psak, judul, dampak}); };
  if (S) {
    nw("1 Jan 2026", "Amendemen PSAK 109 & PSAK 107", "Klasifikasi dan Pengukuran Instrumen Keuangan", "Penghentian pengakuan liabilitas yang dibayar via transfer elektronik dan pengungkapan instrumen berfitur ESG.", fi);
    nw("1 Jan 2026", "Penyesuaian Tahunan 2024", "PSAK 107, PSAK 109, PSAK 110, PSAK 207", "Perbaikan redaksional; umumnya tidak berdampak material.");
    nw("1 Jan 2027", "PSAK 118", "Penyajian dan Pengungkapan dalam Laporan Keuangan", "Dampak tinggi: laba rugi dibagi kategori operasi, investasi, pendanaan; subtotal laba operasi; ukuran kinerja manajemen; komparatif 2026 disajikan ulang.");
    nw("1 Jan 2027", "PSAK 119", "Entitas Anak tanpa Akuntabilitas Publik: Pengungkapan", "Opsi pengungkapan ringkas untuk entitas anak.", st === "anak");
    nw("1 Jan 2027", "Amendemen PSAK 221", "Penjabaran ke Mata Uang Penyajian Hiperinflasi", "Relevan bila ada kegiatan usaha luar negeri.", f.f_valas);
    nw("Bersama PSAK 118", "Amendemen PSAK 228", "Opsi Nilai Wajar untuk Investasi pada Entitas Asosiasi", "Opsi pengukuran investasi asosiasi.", has("invasos"));
    nw("1 Jan 2027", "Amendemen ISAK 335", "Penyajian Laporan Keuangan Entitas Nonlaba", "Menyesuaikan dengan PSAK 118.", st === "nonlaba");
    nw("1 Jan 2029", "PSAK 120", "Aset Regulatori dan Liabilitas Regulatori", "Untuk usaha dengan tarif diatur regulator.", f.f_regulasi);
  } else {
    nw("1 Jan 2025", r.fwName, r.fw === "ep" ? "SAK Indonesia untuk Entitas Privat menggantikan SAK ETAP" : "SAK EMKM tetap berlaku", r.fw === "ep" ? "Bila laporan 2024 masih SAK ETAP, laporan 2025 menyajikan penerapan pertama SAK EP." : "Pantau batas kriteria UMKM setiap tahun.");
    nw("1 Jan 2027", "ISAK 403", "Komponen Laporan Keuangan Entitas Syariah yang Menerapkan SAK EP dan SAK EMKM", "Untuk entitas dengan transaksi syariah.", f.f_syariah);
  }
  nw("1 Jan 2027", "PSAK 401", "Penyajian dan Pengungkapan dalam Laporan Keuangan Syariah", "Pengganti standar penyajian syariah sebelumnya.", f.f_syariah && S);

  // Kewajiban audit UU 40/2007 Pasal 68
  if (aset >= 50e9) r.audit.push(`Jumlah aset Rp${jt(aset)} (≥ Rp50 M)`);
  if (rev >= 50e9) r.audit.push(`Peredaran usaha Rp${jt(rev)} (≥ Rp50 M)`);
  if (st === "tbk" || st === "ipo") r.audit.push("Perusahaan Terbuka / proses penawaran umum");
  if (st === "lk") r.audit.push("Menghimpun atau mengelola dana masyarakat");
  if (st === "bumn") r.audit.push("Persero / BUMN");
  if (f.f_obligasi) r.audit.push("Menerbitkan surat pengakuan utang kepada masyarakat");
  r.kreditNote = f.f_kredit;
  r.ratios = {der: eq ? T.BANK / eq : null, cr: T.LPD ? T.AL / T.LPD : null};
  return r;
}

function renderStd(d, r) {
  const nama = esc(d.f.nama || "Perusahaan Anda");
  const yr = d.f.tahun;
  const rows = r.items.map(i => `<tr><td>${esc(i.psak)}</td><td>${esc(i.topik)}</td><td>${esc(i.why)}</td><td>${esc(i.fokus)}</td></tr>`).join("");
  
  const rt = r.ratios;
  return `<div class="res">
  <h3>Hasil Kalkulator Standar: ${nama}, Tahun Buku ${esc(yr)}</h3>
  <div class="verdict"><span class="pill${r.wajib ? " r" : ""}">${r.wajib ? "Wajib" : "Disarankan"}</span><div><b>${esc(r.fwName)}${d.f.f_syariah ? " + SAK Syariah" : ""}</b><p>${r.reasons.map(esc).join(" ")}</p></div></div>
  <div class="catbars">
    <div><b>${r.items.length}</b><span>PSAK Relevan</span><i></i></div>
    <div><b style="font-size:1.15rem">${esc(r.umkm.replace(" (di atas kriteria UMKM)", ""))}</b><span>Skala Usaha (PP 7/2021)</span><i style="animation-delay:.15s"></i></div>
    <div><b>${rt.cr ? rt.cr.toFixed(2) + "x" : "-"}</b><span>Rasio Lancar</span><i style="animation-delay:.3s"></i></div>
    <div><b>${rt.der != null ? rt.der.toFixed(2) + "x" : "-"}</b><span>Utang Bank / Ekuitas</span><i style="animation-delay:.45s"></i></div>
  </div>
  <h3>Kewajiban Audit Akuntan Publik</h3>
  ${r.audit.length ? `<p><span class="pill r">Wajib Audit</span>Laporan keuangan wajib diaudit akuntan publik menurut Pasal 68 UU 40/2007 tentang Perseroan Terbatas karena: ${r.audit.map(esc).join("; ")}.</p>` : `<p><span class="pill">Belum Wajib</span>Belum memenuhi kriteria wajib audit Pasal 68 UU 40/2007. ${r.kreditNote ? "Namun bank umumnya meminta laporan keuangan audit untuk plafon kredit menengah ke atas." : "Audit sukarela tetap membantu saat mengajukan kredit atau mencari investor."}</p>`}
  <h3>Standar yang Berlaku (${r.items.length})</h3>
  <div class="chipgrid">${r.items.map((i, k) => `<div style="animation-delay:${k * .04}s"><b>${esc(i.psak)}</b><span>${esc(i.topik)}</span></div>`).join("")}</div>
  <details class="more"><summary>Lihat Alasan dan Fokus Auditor per Standar</summary>
  <div class="scroll" style="margin-top:12px"><table class="std"><thead><tr><th>${r.fw === "sak" ? "PSAK/ISAK" : "Topik " + esc(r.fwName)}</th><th>Topik</th><th>Mengapa Berlaku</th><th>Fokus Auditor</th></tr></thead><tbody>${rows}</tbody></table></div></details>
  ${r.fw !== "sak" ? `<p class="lock">Topik ditulis menurut ${esc(r.fwName)}. Nomor PSAK hanya tampil untuk SAK Indonesia.</p>` : ""}
  <h3>Standar Baru yang Berdampak</h3>
  <div class="tl">${r.news.map((n, i) => `<div style="animation-delay:${i * .12}s"><time>${esc(n.eff)}</time><b>${esc(n.psak)}</b><p>${esc(n.dampak)}</p></div>`).join("")}</div>
  <div class="actions" style="margin-top:20px"><button type="button" class="btn" id="toCalk">Lanjut Susun CALK</button><a class="btn btn-ghost" target="_blank" rel="noopener" href="https://wa.me/6282245260121?text=${encodeURIComponent("Halo tim UpdateSAK, hasil kalkulator untuk " + (d.f.nama || "perusahaan kami") + " menunjukkan " + r.fwName + ". Kami ingin diskusi penerapannya.")}">Diskusikan Hasil Ini</a></div>
  </div>`;
}

/* ---------- Penyusun CALK ---------- */
function buildCalk(d, r) {
  const {v, f, t} = d;
  const fw = f.kerangka && f.kerangka !== "auto" ? f.kerangka : r.fw;
  const S = fw === "sak";
  const fwFull = fw === "sak" ? "Standar Akuntansi Keuangan di Indonesia (\"SAK Indonesia\")" : fw === "ep" ? "Standar Akuntansi Keuangan Indonesia untuk Entitas Privat (\"SAK EP\")" : "Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (\"SAK EMKM\")";
  const ref = p => S ? ` ("${p}")` : "";
  const Y1 = +f.tahun, Y0 = Y1 - 1;
  const d1 = `31 Desember ${Y1}`, d0 = `31 Desember ${Y0}`;
  const nama = esc(f.nama || "PT [Nama Perusahaan]");
  const P = s => `<span style="background:#FFF2A8">[${esc(s)}]</span>`;
  const val = (x, ph) => x ? esc(x) : P(ph);
  const a = (id, y) => v[id][y];
  const has = id => a(id, 1) || a(id, 0);
  const prior = IDS.some(id => a(id, 0));

  const TB = "border-collapse:collapse;width:100%;font-family:'Times New Roman',serif;font-size:10.5pt;margin:6px 0 10px";
  const TH = "border-bottom:1px solid #000;padding:3px 6px;text-align:right;font-weight:bold";
  const TD = "padding:2px 6px;text-align:right;white-space:nowrap";
  const TL = "padding:2px 6px;text-align:left";
  // rows: [label, v1, v0, style] ; style 'b' bold total, 'h' heading
  const table = (rows, opt = {}) => {
    const cols = opt.cols || [d1, d0];
    let h = `<table style="${TB}"><tr><th style="${TH};text-align:left">${opt.head || ""}</th>${opt.note ? `<th style="${TH};text-align:center">Catatan</th>` : ""}${cols.map(c => `<th style="${TH}">${c}</th>`).join("")}</tr>`;
    for (const rw of rows) {
      const [lab, x1, x0, s, nt] = rw;
      if (s === "h") { h += `<tr><td style="${TL};font-weight:bold;padding-top:8px" colspan="${cols.length + 1 + (opt.note ? 1 : 0)}">${lab}</td></tr>`; continue; }
      const bt = s === "b" ? ";border-top:1px solid #000;font-weight:bold" : s === "bb" ? ";border-top:1px solid #000;border-bottom:3px double #000;font-weight:bold" : "";
      const cell = x => typeof x === "string" ? x : fmt(x);
      h += `<tr><td style="${TL}${s === "b" || s === "bb" ? ";font-weight:bold" : ""}${s === "i" ? ";padding-left:22px" : ""}">${lab}</td>${opt.note ? `<td style="${TD};text-align:center">${nt || ""}</td>` : ""}<td style="${TD}${bt}">${cell(x1)}</td>${cols.length > 1 ? `<td style="${TD}${bt}">${cell(x0)}</td>` : ""}</tr>`;
    }
    return h + "</table>";
  };
  const p = s => `<p style="margin:0 0 8px;text-align:justify">${s}</p>`;
  const H1 = (n, s) => `<h3 style="font-family:'Times New Roman',serif;font-size:11pt;margin:18px 0 8px;font-weight:bold">${n}. ${s.toUpperCase()}</h3>`;
  const H2 = (n, s) => `<p style="margin:12px 0 6px;font-weight:bold">${n}. ${s}</p>`;
  const lines = s => String(s || "").split(/\n+/).map(l => l.trim()).filter(Boolean).map(l => { const [j, ...nm] = l.split(":"); return [j.trim(), nm.join(":").trim()]; });

  /* Penomoran catatan akun */
  const order = [
    ["kas", has("kas")], ["piu", has("piu3") || has("piurel")], ["piulain", has("piulain")], ["kontrak", has("asetkontrak") || has("liabkontrak")],
    ["persediaan", has("persediaan")], ["uangmuka", has("uangmuka")], ["pajak", has("pajakdm") || has("utangpajak") || has("pajakkini") || has("apt") || has("lpt")],
    ["at", has("atbiaya")], ["sewa", has("rou") || has("sewalancar") || has("sewapanjang")], ["propinv", has("propinv")], ["atb", has("atb")],
    ["invasos", has("invasos")], ["atllain", has("atllain")], ["bank", t[1].BANK || t[0].BANK], ["uu", has("uu3") || has("uurel")],
    ["ul", has("ul")], ["akrual", has("akrual")], ["imbalan", has("imbalan")], ["modal", has("modal")], ["tmd", has("tmd")],
    ["saldolaba", true], ["pend", has("pendapatan")], ["hpp", has("hpp")], ["busaha", has("bjual") || has("bumum")],
    ["lain", has("lain")], ["keu", has("pkeu") || has("bkeu")], ["rel", true], ["risiko", S || fw === "ep"], ["modalmgmt", S],
    ["baru", S], ["peristiwa", true]
  ];
  const N = {}; let n = 4;
  for (const [k, on] of order) if (on) N[k] = n++;
  const c = k => N[k] ? String(N[k]) : "";

  /* Laporan posisi keuangan dan laba rugi */
  const ln = (lab, id, k, sgn = 1) => has(id) ? [[lab, sgn * a(id, 1), sgn * a(id, 0), "", c(k)]] : [];
  const T1 = t[1], T0 = t[0];
  const bs = [
    ["ASET LANCAR", 0, 0, "h"],
    ...ln("Kas dan setara kas", "kas", "kas"),
    ...(has("piu3") || has("piurel") ? [["Piutang usaha, neto", T1.PIU, T0.PIU, "", c("piu")]] : []),
    ...ln("Piutang lain-lain", "piulain", "piulain"), ...ln("Aset kontrak", "asetkontrak", "kontrak"),
    ...ln("Persediaan", "persediaan", "persediaan"), ...ln("Uang muka dan biaya dibayar di muka", "uangmuka", "uangmuka"),
    ...ln("Pajak dibayar di muka", "pajakdm", "pajak"),
    ["Jumlah Aset Lancar", T1.AL, T0.AL, "b"],
    ["ASET TIDAK LANCAR", 0, 0, "h"],
    ...(has("atbiaya") ? [["Aset tetap, neto", T1.AT, T0.AT, "", c("at")]] : []),
    ...ln("Aset hak guna, neto", "rou", "sewa"), ...ln("Properti investasi", "propinv", "propinv"),
    ...ln("Aset takberwujud, neto", "atb", "atb"), ...ln("Investasi pada entitas asosiasi", "invasos", "invasos"),
    ...ln("Aset pajak tangguhan", "apt", "pajak"), ...ln("Aset tidak lancar lainnya", "atllain", "atllain"),
    ["Jumlah Aset Tidak Lancar", T1.ATL, T0.ATL, "b"],
    ["JUMLAH ASET", T1.ASET, T0.ASET, "bb"],
    ["LIABILITAS JANGKA PENDEK", 0, 0, "h"],
    ...ln("Utang bank jangka pendek", "ubpendek", "bank"), ...ln("Utang usaha: pihak ketiga", "uu3", "uu"), ...ln("Utang usaha: pihak berelasi", "uurel", "uu"),
    ...ln("Utang lain-lain", "ul", "ul"), ...ln("Beban akrual", "akrual", "akrual"), ...ln("Utang pajak", "utangpajak", "pajak"),
    ...ln("Liabilitas kontrak", "liabkontrak", "kontrak"), ...ln("Bagian lancar utang bank jangka panjang", "ublancar", "bank"),
    ...ln("Bagian lancar liabilitas sewa", "sewalancar", "sewa"),
    ["Jumlah Liabilitas Jangka Pendek", T1.LPD, T0.LPD, "b"],
    ["LIABILITAS JANGKA PANJANG", 0, 0, "h"],
    ...ln("Utang bank jangka panjang, setelah dikurangi bagian lancar", "ubpanjang", "bank"),
    ...ln("Liabilitas sewa, setelah dikurangi bagian lancar", "sewapanjang", "sewa"),
    ...ln("Liabilitas imbalan kerja", "imbalan", "imbalan"), ...ln("Liabilitas pajak tangguhan", "lpt", "pajak"),
    ...ln("Utang pihak berelasi", "utangrel", "rel"),
    ["Jumlah Liabilitas Jangka Panjang", T1.LPJ, T0.LPJ, "b"],
    ["JUMLAH LIABILITAS", T1.LIAB, T0.LIAB, "b"],
    ["EKUITAS", 0, 0, "h"],
    ...ln("Modal saham", "modal", "modal"), ...ln("Tambahan modal disetor", "tmd", "tmd"),
    ["Saldo laba", a("saldolaba", 1), a("saldolaba", 0), "", c("saldolaba")],
    ...ln("Penghasilan komprehensif lain", "ociek", "imbalan"),
    ["JUMLAH EKUITAS", T1.EK, T0.EK, "b"],
    ["JUMLAH LIABILITAS DAN EKUITAS", T1.LE, T0.LE, "bb"]
  ];
  const pl = [
    ...ln("Pendapatan", "pendapatan", "pend"), ...ln("Beban pokok pendapatan", "hpp", "hpp", -1),
    ["LABA BRUTO", T1.LK, T0.LK, "b"],
    ...ln("Beban penjualan", "bjual", "busaha", -1), ...ln("Beban umum dan administrasi", "bumum", "busaha", -1),
    ...ln("Pendapatan (beban) lain-lain, neto", "lain", "lain"),
    ["LABA USAHA", T1.LU, T0.LU, "b"],
    ...ln("Pendapatan keuangan", "pkeu", "keu"), ...ln("Beban keuangan", "bkeu", "keu", -1),
    ["LABA SEBELUM PAJAK PENGHASILAN", T1.LSBP, T0.LSBP, "b"],
    ["Beban pajak penghasilan, neto", -T1.PAJAK, -T0.PAJAK, "", c("pajak")],
    ["LABA TAHUN BERJALAN", T1.LB, T0.LB, "b"],
    ["PENGHASILAN KOMPREHENSIF LAIN", 0, 0, "h"],
    ["Pos yang tidak akan direklasifikasi ke laba rugi: pengukuran kembali liabilitas imbalan kerja, setelah pajak", a("oci", 1), a("oci", 0), "", c("imbalan")],
    ["JUMLAH PENGHASILAN KOMPREHENSIF TAHUN BERJALAN", T1.TCI, T0.TCI, "bb"]
  ];

  let H = `<div style="font-family:'Times New Roman',serif;font-size:11pt;color:#000">`;
  H += `<p style="text-align:center;font-weight:bold;margin:0">${nama.toUpperCase()}</p><p style="text-align:center;font-weight:bold;margin:0">LAPORAN POSISI KEUANGAN</p><p style="text-align:center;margin:0 0 6px">Tanggal ${d1}<br>(Disajikan dalam Rupiah, kecuali dinyatakan lain)</p>`;
  H += table(bs, {note: true});
  H += `<p style="text-align:center;font-weight:bold;margin:18px 0 0">LAPORAN LABA RUGI DAN PENGHASILAN KOMPREHENSIF LAIN</p><p style="text-align:center;margin:0 0 6px">Untuk Tahun yang Berakhir pada Tanggal ${d1}<br>(Disajikan dalam Rupiah, kecuali dinyatakan lain)</p>`;
  H += table(pl, {note: true});
  H += `<p style="font-style:italic;font-size:10pt">Catatan atas laporan keuangan terlampir merupakan bagian yang tidak terpisahkan dari laporan keuangan secara keseluruhan.</p>`;
  H += `<br style="page-break-before:always"><p style="text-align:center;font-weight:bold;margin:12px 0 0">${nama.toUpperCase()}</p><p style="text-align:center;font-weight:bold;margin:0">CATATAN ATAS LAPORAN KEUANGAN</p><p style="text-align:center;margin:0 0 8px">Tanggal ${d1} dan untuk Tahun yang Berakhir pada Tanggal Tersebut<br>(Disajikan dalam Rupiah, kecuali dinyatakan lain)</p>`;

  /* Catatan 1 */
  H += H1(1, "Umum");
  H += H2("a", "Pendirian dan Informasi Umum");
  H += p(`${nama} ("Perusahaan") didirikan berdasarkan Akta Notaris No. ${val(f.akta_no, "nomor")} tanggal ${val(f.akta_tgl, "tanggal akta")} dari ${val(f.notaris, "nama notaris")}. Akta pendirian tersebut telah memperoleh pengesahan dari Menteri Hukum melalui Surat Keputusan No. ${val(f.sk, "nomor SK AHU")}. Anggaran Dasar Perusahaan telah beberapa kali mengalami perubahan, terakhir dengan ${val(f.akta_ubah, "akta perubahan terakhir, nomor, tanggal, dan pokok perubahan")}.`);
  H += p(`Sesuai dengan Pasal 3 Anggaran Dasar, ruang lingkup kegiatan Perusahaan meliputi ${val(f.kegiatan, "kegiatan usaha sesuai anggaran dasar dan KBLI")}. Perusahaan mulai beroperasi secara komersial pada tahun ${val(f.mulai, "tahun")}. Kantor pusat Perusahaan berkedudukan di ${val(f.alamat || f.kota, "alamat kantor pusat")}.`);
  if (f.induk) H += p(`Entitas induk Perusahaan adalah ${esc(f.induk)}.`);
  H += H2("b", "Dewan Komisaris, Direksi, dan Karyawan");
  H += p(`Susunan Dewan Komisaris dan Direksi Perusahaan pada tanggal ${d1} adalah sebagai berikut:`);
  const kom = lines(f.komisaris), dir = lines(f.direksi);
  const ppl = (arr, def) => (arr.length ? arr : def.map(j => [j, ""])).map(([j, nm]) => `<tr><td style="${TL};width:45%">${esc(j)}</td><td style="${TL}">: ${nm ? esc(nm) : P("nama")}</td></tr>`).join("");
  H += `<table style="${TB}"><tr><td style="${TL};font-weight:bold" colspan="2">Dewan Komisaris</td></tr>${ppl(kom, ["Komisaris Utama", "Komisaris"])}<tr><td style="${TL};font-weight:bold;padding-top:6px" colspan="2">Direksi</td></tr>${ppl(dir, ["Direktur Utama", "Direktur"])}</table>`;
  H += p(`Pada tanggal ${d1}, Perusahaan memiliki ${val(f.karyawan, "jumlah")} karyawan tetap${prior ? ` (${d0}: ${P("jumlah")} karyawan)` : ""}.`);
  H += H2("c", "Penyelesaian Laporan Keuangan");
  H += p(`Manajemen Perusahaan bertanggung jawab atas penyusunan dan penyajian wajar laporan keuangan ini yang telah diselesaikan dan diotorisasi untuk terbit oleh Direksi pada tanggal ${val(f.otorisasi, "tanggal otorisasi")}.`);

  /* Catatan 2 */
  let s2 = "a".charCodeAt(0);
  const sub = () => String.fromCharCode(s2++);
  H += H1(2, "Ikhtisar Informasi Kebijakan Akuntansi Material");
  H += p(`Kebijakan akuntansi material yang diterapkan dalam penyusunan laporan keuangan Perusahaan adalah sebagai berikut:`);
  H += H2(sub(), "Dasar Penyusunan Laporan Keuangan");
  H += p(`Laporan keuangan telah disusun dan disajikan sesuai dengan ${fwFull} yang diterbitkan oleh Dewan Standar Akuntansi Keuangan Ikatan Akuntan Indonesia.`);
  H += p(`Laporan keuangan disusun berdasarkan konsep akrual, kecuali laporan arus kas, dengan menggunakan konsep biaya historis, kecuali beberapa akun tertentu yang diukur berdasarkan pengukuran lain sebagaimana dijelaskan dalam kebijakan akuntansi masing-masing akun. Laporan arus kas disusun dengan metode tidak langsung dan mengelompokkan arus kas ke dalam aktivitas operasi, investasi, dan pendanaan.`);
  H += p(`Mata uang penyajian yang digunakan dalam laporan keuangan adalah Rupiah, yang juga merupakan mata uang fungsional Perusahaan.`);
  if (S) {
    H += H2(sub(), "Perubahan Kebijakan Akuntansi");
    H += p(Y1 >= 2026
      ? `Perusahaan menerapkan amendemen standar yang berlaku efektif sejak 1 Januari ${Y1}, yaitu Amendemen PSAK 109 dan PSAK 107 tentang Klasifikasi dan Pengukuran Instrumen Keuangan, Amendemen PSAK 109 dan PSAK 107 tentang Kontrak yang Mengacu pada Listrik Bergantung Alam, serta Penyesuaian Tahunan 2024 atas PSAK 107, PSAK 109, PSAK 110, dan PSAK 207. Penerapan amendemen tersebut tidak menimbulkan perubahan material atas kebijakan akuntansi Perusahaan dan tidak berdampak material terhadap jumlah yang dilaporkan.`
      : `Perusahaan menerapkan amendemen standar yang berlaku efektif sejak 1 Januari ${Y1}, termasuk Amendemen PSAK 221 tentang Kekurangan Ketertukaran. Penerapan amendemen tersebut tidak berdampak material terhadap laporan keuangan Perusahaan.`);
  }
  H += H2(sub(), "Klasifikasi Lancar dan Tidak Lancar");
  H += p(`Perusahaan menyajikan aset dan liabilitas dalam laporan posisi keuangan berdasarkan klasifikasi lancar dan tidak lancar. Aset diklasifikasikan lancar jika diperkirakan akan direalisasi, dimaksudkan untuk dijual atau digunakan dalam siklus operasi normal, dimiliki untuk diperdagangkan, atau diperkirakan direalisasi dalam jangka waktu dua belas bulan setelah periode pelaporan. Liabilitas diklasifikasikan lancar jika diperkirakan akan diselesaikan dalam siklus operasi normal, dimiliki untuk diperdagangkan, jatuh tempo dalam dua belas bulan setelah periode pelaporan, atau Perusahaan tidak memiliki hak pada akhir periode pelaporan untuk menangguhkan penyelesaian liabilitas paling sedikit dua belas bulan setelah periode pelaporan. Seluruh aset dan liabilitas lainnya diklasifikasikan tidak lancar.`);
  H += H2(sub(), "Kas dan Setara Kas");
  H += p(`Kas dan setara kas terdiri dari kas, kas di bank, dan deposito berjangka dengan jangka waktu tiga bulan atau kurang sejak tanggal penempatan dan tidak dijaminkan atau dibatasi penggunaannya.`);
  H += H2(sub(), "Instrumen Keuangan");
  H += p(S
    ? `Perusahaan menerapkan PSAK 109, "Instrumen Keuangan". Aset keuangan diklasifikasikan pada pengakuan awal sebagai diukur pada biaya perolehan diamortisasi, nilai wajar melalui penghasilan komprehensif lain, atau nilai wajar melalui laba rugi, berdasarkan model bisnis Perusahaan dalam mengelola aset keuangan dan karakteristik arus kas kontraktualnya. Aset keuangan Perusahaan yang terdiri dari kas dan setara kas, piutang usaha, dan piutang lain-lain diklasifikasikan sebagai aset keuangan yang diukur pada biaya perolehan diamortisasi.`
    : `Aset keuangan dasar (kas, piutang usaha, dan piutang lain-lain) dan liabilitas keuangan dasar (utang usaha, utang lain-lain, dan pinjaman) diakui pada harga transaksi dan selanjutnya diukur pada biaya perolehan diamortisasi.`);
  H += p(S
    ? `Perusahaan mengakui cadangan kerugian kredit ekspektasian ("KKE"). Untuk piutang usaha dan aset kontrak, Perusahaan menerapkan pendekatan yang disederhanakan dan mengakui cadangan kerugian berdasarkan KKE sepanjang umur menggunakan matriks provisi yang didasarkan pada pengalaman kerugian kredit historis dan disesuaikan dengan faktor perkiraan masa depan yang spesifik terhadap debitur dan lingkungan ekonomi.`
    : `Pada setiap akhir periode pelaporan, Perusahaan menilai apakah terdapat bukti objektif penurunan nilai atas aset keuangan dan mengakui kerugian penurunan nilai di laba rugi.`);
  H += p(`Liabilitas keuangan Perusahaan yang terdiri dari ${[has("ubpendek") || has("ubpanjang") || has("ublancar") ? "utang bank" : "", has("uu3") || has("uurel") ? "utang usaha" : "", has("ul") ? "utang lain-lain" : "", has("akrual") ? "beban akrual" : "", T1.SEWA || T0.SEWA ? "liabilitas sewa" : ""].filter(Boolean).join(", ") || "utang usaha dan utang lain-lain"} diklasifikasikan sebagai liabilitas keuangan yang diukur pada biaya perolehan diamortisasi menggunakan metode suku bunga efektif.`);
  if (has("persediaan")) { H += H2(sub(), "Persediaan"); H += p(`Persediaan dinyatakan sebesar nilai terendah antara biaya perolehan dan nilai realisasi neto. Biaya perolehan ditentukan dengan metode ${P("rata-rata tertimbang / FIFO")}. Nilai realisasi neto adalah estimasi harga jual dalam kegiatan usaha normal dikurangi estimasi biaya penyelesaian dan biaya yang diperlukan untuk melaksanakan penjualan. Penyisihan persediaan usang dan penurunan nilai ditentukan berdasarkan penelaahan atas kondisi persediaan pada akhir periode.`); }
  if (has("atbiaya")) {
    H += H2(sub(), "Aset Tetap");
    H += p(`Aset tetap dinyatakan sebesar biaya perolehan dikurangi akumulasi penyusutan dan akumulasi rugi penurunan nilai, jika ada. Tanah tidak disusutkan. Penyusutan aset tetap lainnya dihitung dengan metode garis lurus berdasarkan taksiran masa manfaat ekonomis sebagai berikut:`);
    H += `<table style="${TB};width:60%"><tr><th style="${TH};text-align:left">Kelompok Aset</th><th style="${TH}">Tahun</th></tr>${[["Bangunan dan prasarana", "20"], ["Mesin dan peralatan", "4 - 8"], ["Kendaraan", "4 - 8"], ["Peralatan kantor", "4"]].map(([k, y]) => `<tr><td style="${TL}">${k}</td><td style="${TD}">${P(y)}</td></tr>`).join("")}</table>`;
    H += p(`Biaya pemeliharaan dan perbaikan dibebankan ke laba rugi pada saat terjadinya. Pemugaran dan penambahan dalam jumlah signifikan dikapitalisasi. Nilai residu, umur manfaat, dan metode penyusutan ditelaah setiap akhir tahun dan disesuaikan secara prospektif jika diperlukan.${S ? ` Aset dalam penyelesaian dinyatakan sebesar biaya perolehan, termasuk biaya pinjaman yang dapat diatribusikan sesuai PSAK 223, dan direklasifikasi ke aset tetap terkait pada saat siap digunakan.` : ""}`);
  }
  if (has("rou") || T1.SEWA || T0.SEWA) { H += H2(sub(), "Sewa"); H += p(S ? `Pada tanggal insepsi kontrak, Perusahaan menilai apakah kontrak merupakan, atau mengandung, sewa. Sebagai penyewa, Perusahaan mengakui aset hak guna dan liabilitas sewa pada tanggal permulaan sewa. Aset hak guna disusutkan dengan metode garis lurus selama periode yang lebih pendek antara masa sewa dan umur manfaat aset. Liabilitas sewa diukur pada nilai kini pembayaran sewa yang belum dibayar, didiskontokan dengan suku bunga pinjaman inkremental Perusahaan. Perusahaan memilih untuk tidak mengakui aset hak guna dan liabilitas sewa untuk sewa jangka pendek (12 bulan atau kurang) dan sewa aset bernilai rendah; pembayarannya diakui sebagai beban dengan metode garis lurus.` : `Sewa diklasifikasikan sebagai sewa pembiayaan jika sewa tersebut mengalihkan secara substansial seluruh risiko dan manfaat yang terkait dengan kepemilikan aset. Sewa lainnya diklasifikasikan sebagai sewa operasi dan pembayarannya diakui sebagai beban dengan metode garis lurus.`); }
  if (has("propinv")) { H += H2(sub(), "Properti Investasi"); H += p(`Properti investasi adalah properti yang dikuasai untuk menghasilkan sewa atau untuk kenaikan nilai, atau keduanya. Perusahaan memilih ${P("model biaya / model nilai wajar")} untuk pengukuran setelah pengakuan awal.`); }
  if (has("atb")) { H += H2(sub(), "Aset Takberwujud"); H += p(`Aset takberwujud, terutama perangkat lunak, dinyatakan sebesar biaya perolehan dikurangi akumulasi amortisasi dan diamortisasi dengan metode garis lurus selama ${P("4")} tahun.`); }
  if (has("invasos")) { H += H2(sub(), "Investasi pada Entitas Asosiasi"); H += p(`Entitas asosiasi adalah entitas di mana Perusahaan memiliki pengaruh signifikan. Investasi pada entitas asosiasi dicatat dengan metode ekuitas.`); }
  H += H2(sub(), "Penurunan Nilai Aset Nonkeuangan");
  H += p(`Pada setiap tanggal pelaporan, Perusahaan menilai apakah terdapat indikasi aset nonkeuangan mengalami penurunan nilai. Jika terdapat indikasi tersebut, Perusahaan mengestimasi jumlah terpulihkan aset, yaitu nilai tertinggi antara nilai wajar dikurangi biaya pelepasan dan nilai pakainya. Jika jumlah tercatat aset melebihi jumlah terpulihkannya, aset tersebut dianggap mengalami penurunan nilai dan diturunkan menjadi sebesar jumlah terpulihkannya.`);
  H += H2(sub(), "Pengakuan Pendapatan dan Beban");
  H += p(S
    ? `Perusahaan mengakui pendapatan dari kontrak dengan pelanggan sesuai PSAK 115 dengan menerapkan lima langkah: (i) identifikasi kontrak dengan pelanggan; (ii) identifikasi kewajiban pelaksanaan; (iii) penentuan harga transaksi; (iv) alokasi harga transaksi ke setiap kewajiban pelaksanaan; dan (v) pengakuan pendapatan ketika (atau selama) Perusahaan memenuhi kewajiban pelaksanaan.`
    : `Pendapatan diukur pada nilai wajar imbalan yang diterima atau dapat diterima, setelah dikurangi diskon dan retur.`);
  H += p(d.f.f_kontrak
    ? `Pendapatan dari kontrak proyek diakui sepanjang waktu berdasarkan tingkat penyelesaian, yang diukur dengan ${P("metode input: biaya yang terjadi dibandingkan estimasi total biaya / metode output: survei progres fisik")}. Selisih antara pendapatan yang diakui dan tagihan kepada pelanggan disajikan sebagai aset kontrak atau liabilitas kontrak. Jika kemungkinan besar total biaya kontrak melebihi total pendapatan kontrak, taksiran kerugian segera diakui sebagai beban.`
    : `Pendapatan dari penjualan barang diakui pada titik waktu ketika pengendalian atas barang telah dialihkan kepada pelanggan, umumnya pada saat barang diserahkan. Pendapatan jasa diakui pada saat jasa diberikan.`);
  H += p(`Beban diakui pada saat terjadinya dengan dasar akrual.`);
  if (has("imbalan") || fw !== "emkm") { H += H2(sub(), "Imbalan Kerja"); H += p(`Perusahaan mengakui liabilitas imbalan pascakerja sesuai dengan Undang-Undang No. 6 Tahun 2023 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang No. 2 Tahun 2022 tentang Cipta Kerja dan Peraturan Pemerintah No. 35 Tahun 2021. ${S ? `Liabilitas imbalan pascakerja dihitung oleh aktuaris independen menggunakan metode projected unit credit sesuai PSAK 219. ` : ``}Pengukuran kembali, yang terdiri dari keuntungan dan kerugian aktuarial, diakui segera dalam penghasilan komprehensif lain dan tidak direklasifikasi ke laba rugi pada periode berikutnya. Biaya jasa lalu diakui di laba rugi pada tanggal yang lebih awal antara amendemen atau kurtailmen program dan pengakuan biaya restrukturisasi terkait.`); }
  H += H2(sub(), "Pajak Penghasilan");
  H += p(`Beban pajak kini ditentukan berdasarkan laba kena pajak periode berjalan yang dihitung berdasarkan tarif pajak yang berlaku. Aset dan liabilitas pajak tangguhan diakui atas perbedaan temporer antara dasar pengenaan pajak aset dan liabilitas dengan jumlah tercatatnya pada setiap tanggal pelaporan, diukur dengan tarif pajak yang diharapkan berlaku pada periode realisasi aset atau penyelesaian liabilitas. Aset pajak tangguhan diakui sepanjang kemungkinan besar laba kena pajak tersedia untuk dimanfaatkan dengan perbedaan temporer tersebut.${S ? ` Perusahaan menerapkan ISAK 123 dalam menilai ketidakpastian perlakuan pajak penghasilan.` : ""}`);
  H += p(`Koreksi atas liabilitas perpajakan diakui pada saat surat ketetapan pajak diterima atau, jika Perusahaan mengajukan keberatan atau banding, pada saat keputusan atas keberatan atau banding tersebut telah ditetapkan.`);
  if (d.f.f_valas) { H += H2(sub(), "Transaksi dan Saldo dalam Mata Uang Asing"); H += p(`Transaksi dalam mata uang asing dicatat dalam Rupiah berdasarkan kurs pada tanggal transaksi. Pada tanggal pelaporan, aset dan liabilitas moneter dalam mata uang asing dijabarkan ke dalam Rupiah menggunakan kurs tengah Bank Indonesia pada tanggal tersebut. Keuntungan atau kerugian kurs yang timbul dikreditkan atau dibebankan pada laba rugi tahun berjalan. Kurs yang digunakan pada tanggal ${d1} adalah ${P("Rp... per USD 1")}${prior ? ` (${d0}: ${P("Rp...")})` : ""}.`); }
  H += H2(sub(), "Transaksi dengan Pihak-Pihak Berelasi");
  H += p(`Perusahaan melakukan transaksi dengan pihak-pihak berelasi sebagaimana didefinisikan dalam ${S ? "PSAK 224, \"Pengungkapan Pihak-Pihak Berelasi\"" : fwFull}. Seluruh transaksi dan saldo yang signifikan dengan pihak berelasi diungkapkan dalam catatan atas laporan keuangan.`);
  H += H2(sub(), "Provisi");
  H += p(`Provisi diakui jika Perusahaan memiliki kewajiban kini (baik bersifat hukum maupun konstruktif) sebagai akibat peristiwa masa lalu, kemungkinan besar penyelesaian kewajiban tersebut mengakibatkan arus keluar sumber daya, dan estimasi yang andal mengenai jumlah kewajiban tersebut dapat dibuat.`);
  H += H2(sub(), "Peristiwa setelah Periode Pelaporan");
  H += p(`Peristiwa setelah periode pelaporan yang memberikan informasi tambahan tentang posisi keuangan Perusahaan pada tanggal pelaporan (peristiwa penyesuai) tercermin dalam laporan keuangan. Peristiwa setelah periode pelaporan yang bukan merupakan peristiwa penyesuai diungkapkan dalam catatan atas laporan keuangan jika material.`);

  /* Catatan 3 */
  H += H1(3, "Pertimbangan, Estimasi, dan Asumsi Akuntansi yang Signifikan");
  H += p(`Penyusunan laporan keuangan mengharuskan manajemen membuat pertimbangan, estimasi, dan asumsi yang memengaruhi jumlah pendapatan, beban, aset, dan liabilitas yang dilaporkan, serta pengungkapan atas liabilitas kontinjensi pada akhir periode pelaporan. Ketidakpastian mengenai asumsi dan estimasi tersebut dapat mengakibatkan penyesuaian material terhadap nilai tercatat aset dan liabilitas dalam periode pelaporan berikutnya.`);
  H += H2("a", "Pertimbangan");
  H += p(`<i>Penentuan mata uang fungsional.</i> Mata uang fungsional Perusahaan adalah mata uang dari lingkungan ekonomi primer di mana Perusahaan beroperasi, yaitu mata uang yang paling memengaruhi harga jual barang dan jasa serta biaya Perusahaan. Berdasarkan penilaian manajemen, mata uang fungsional Perusahaan adalah Rupiah.`);
  if (S) H += p(`<i>Klasifikasi aset dan liabilitas keuangan.</i> Perusahaan menetapkan klasifikasi atas aset dan liabilitas tertentu sebagai aset keuangan dan liabilitas keuangan dengan mempertimbangkan apakah definisi yang ditetapkan PSAK 109 dipenuhi.`);
  if (d.f.f_kontrak) H += p(`<i>Pengakuan pendapatan sepanjang waktu.</i> Manajemen menilai bahwa kewajiban pelaksanaan atas kontrak proyek dipenuhi sepanjang waktu karena pelanggan mengendalikan aset selama aset tersebut dibangun.`);
  if (T1.SEWA || T0.SEWA) H += p(`<i>Penentuan masa sewa.</i> Dalam menentukan masa sewa, manajemen mempertimbangkan seluruh fakta dan keadaan yang menimbulkan insentif ekonomik untuk mengeksekusi opsi perpanjangan atau tidak mengeksekusi opsi penghentian.`);
  H += H2("b", "Estimasi dan Asumsi");
  if (has("piu3") || has("piurel")) H += p(`<i>Cadangan kerugian penurunan nilai piutang usaha.</i> Perusahaan menggunakan matriks provisi berdasarkan pengalaman kerugian historis yang disesuaikan dengan informasi perkiraan masa depan. Jumlah tercatat piutang usaha sebelum cadangan pada tanggal ${d1} adalah sebesar Rp${idn(a("piu3", 1) + a("piurel", 1))}.`);
  if (has("atbiaya")) H += p(`<i>Penyusutan aset tetap.</i> Biaya perolehan aset tetap disusutkan dengan metode garis lurus berdasarkan taksiran masa manfaat ekonomisnya. Perubahan tingkat pemakaian dan perkembangan teknologi dapat memengaruhi masa manfaat dan nilai sisa aset, sehingga beban penyusutan masa depan dapat direvisi. Nilai tercatat neto aset tetap pada tanggal ${d1} adalah sebesar Rp${idn(T1.AT)}.`);
  if (has("imbalan")) H += p(`<i>Liabilitas imbalan kerja.</i> Penentuan liabilitas imbalan kerja bergantung pada asumsi aktuarial, antara lain tingkat diskonto, tingkat kenaikan gaji, tingkat pengunduran diri, dan tingkat kematian. Perbedaan hasil aktual dengan asumsi diakui sebagai pengukuran kembali dalam penghasilan komprehensif lain. Nilai tercatat liabilitas imbalan kerja pada tanggal ${d1} adalah sebesar Rp${idn(a("imbalan", 1))}.`);
  if (has("persediaan")) H += p(`<i>Penyisihan persediaan usang.</i> Penyisihan ditentukan berdasarkan estimasi harga jual dan kondisi fisik persediaan yang ditelaah secara berkala.`);
  H += p(`<i>Pajak penghasilan.</i> Pertimbangan signifikan diperlukan dalam menentukan provisi pajak penghasilan. Perusahaan mengakui liabilitas atas pemeriksaan pajak berdasarkan estimasi apakah akan terdapat tambahan pajak.`);

  /* Catatan akun */
  const NT = (k, title) => H1(N[k], title);
  const pr = prior;
  const tb2 = (rows) => table(rows, pr ? {} : {cols: [d1]});
  if (N.kas) { H += NT("kas", "Kas dan Setara Kas"); H += tb2([["Kas", P("kas tunai"), P("..."), "i"], ["Bank: Rupiah", P("rincian per bank"), P("..."), "i"], ["Deposito berjangka", P("..."), P("..."), "i"], ["Jumlah", a("kas", 1), a("kas", 0), "bb"]]); H += p(`Rincian saldo bank: ${P("nama bank dan saldo masing-masing")}. Suku bunga tahunan deposito berjangka berkisar antara ${P("...%")} sampai ${P("...%")}. Pada tanggal ${d1}${pr ? ` dan ${Y0}` : ""}, tidak terdapat kas dan setara kas yang dijaminkan atau dibatasi penggunaannya.`); }
  if (N.piu) {
    H += NT("piu", "Piutang Usaha");
    H += tb2([["Pihak ketiga", a("piu3", 1), a("piu3", 0), "i"], ["Pihak berelasi (Catatan " + c("rel") + ")", a("piurel", 1), a("piurel", 0), "i"], ["Jumlah", a("piu3", 1) + a("piurel", 1), a("piu3", 0) + a("piurel", 0), "b"], ["Dikurangi cadangan kerugian penurunan nilai", -Math.abs(a("cke", 1)), -Math.abs(a("cke", 0)), ""], ["Neto", T1.PIU, T0.PIU, "bb"]]);
    H += p(`Analisis umur piutang usaha berdasarkan tanggal faktur adalah sebagai berikut:`);
    H += tb2([["Belum jatuh tempo", P("..."), P("..."), "i"], ["Lewat jatuh tempo 1 - 30 hari", P("..."), P("..."), "i"], ["Lewat jatuh tempo 31 - 60 hari", P("..."), P("..."), "i"], ["Lewat jatuh tempo 61 - 90 hari", P("..."), P("..."), "i"], ["Lewat jatuh tempo lebih dari 90 hari", P("..."), P("..."), "i"], ["Jumlah", a("piu3", 1) + a("piurel", 1), a("piu3", 0) + a("piurel", 0), "bb"]]);
    if (has("cke")) { const awal = Math.abs(a("cke", 0)), akh = Math.abs(a("cke", 1)); H += p(`Mutasi cadangan kerugian penurunan nilai piutang usaha adalah sebagai berikut:`); H += table([["Saldo awal tahun", awal, "", "i"], ["Penyisihan (pemulihan) tahun berjalan", akh - awal, "", "i"], ["Penghapusan", P("..."), "", "i"], ["Saldo akhir tahun", akh, "", "bb"]], {cols: [String(Y1)]}); }
    H += p(`Manajemen berpendapat bahwa cadangan kerugian penurunan nilai piutang usaha telah memadai untuk menutup kemungkinan kerugian atas tidak tertagihnya piutang usaha.${T1.BANK ? ` Piutang usaha sebesar ${P("Rp...")} dijadikan jaminan atas utang bank (Catatan ${c("bank")}).` : ""}`);
  }
  if (N.piulain) { H += NT("piulain", "Piutang Lain-Lain"); H += tb2([["Piutang karyawan", P("..."), P("..."), "i"], ["Lain-lain", P("..."), P("..."), "i"], ["Jumlah", a("piulain", 1), a("piulain", 0), "bb"]]); }
  if (N.kontrak) { H += NT("kontrak", "Aset Kontrak dan Liabilitas Kontrak"); H += tb2([["Aset kontrak", a("asetkontrak", 1), a("asetkontrak", 0), "i"], ["Liabilitas kontrak", a("liabkontrak", 1), a("liabkontrak", 0), "i"]]); H += p(`Aset kontrak merupakan hak Perusahaan atas imbalan untuk pekerjaan yang telah diselesaikan tetapi belum ditagih pada tanggal pelaporan. Liabilitas kontrak merupakan uang muka yang diterima dari pelanggan atas pekerjaan yang belum dilaksanakan. Pendapatan yang diakui pada tahun ${Y1} yang berasal dari saldo liabilitas kontrak awal tahun adalah sebesar ${P("Rp...")}.`); }
  if (N.persediaan) { H += NT("persediaan", "Persediaan"); H += tb2([["Barang jadi / barang dagangan", P("..."), P("..."), "i"], ["Bahan baku dan pembantu", P("..."), P("..."), "i"], ["Jumlah", a("persediaan", 1), a("persediaan", 0), "bb"]]); H += p(`Manajemen berpendapat bahwa nilai tercatat persediaan tidak melebihi nilai realisasi netonya, sehingga tidak diperlukan penyisihan penurunan nilai persediaan. Persediaan diasuransikan terhadap risiko kebakaran dan risiko lainnya dengan nilai pertanggungan sebesar ${P("Rp...")}, yang menurut manajemen memadai untuk menutup kemungkinan kerugian atas risiko tersebut.${T1.BANK ? ` Persediaan sebesar ${P("Rp...")} dijadikan jaminan atas utang bank (Catatan ${c("bank")}).` : ""}`); }
  if (N.uangmuka) { H += NT("uangmuka", "Uang Muka dan Biaya Dibayar di Muka"); H += tb2([["Uang muka pembelian", P("..."), P("..."), "i"], ["Asuransi dibayar di muka", P("..."), P("..."), "i"], ["Lain-lain", P("..."), P("..."), "i"], ["Jumlah", a("uangmuka", 1), a("uangmuka", 0), "bb"]]); }
  if (N.pajak) {
    H += NT("pajak", "Perpajakan");
    let s = 97; const ps = () => String.fromCharCode(s++);
    if (has("pajakdm")) { H += H2(ps(), "Pajak Dibayar di Muka"); H += tb2([["Pajak Pertambahan Nilai", P("..."), P("..."), "i"], ["Pajak Penghasilan Pasal 28A", P("..."), P("..."), "i"], ["Jumlah", a("pajakdm", 1), a("pajakdm", 0), "bb"]]); }
    if (has("utangpajak")) { H += H2(ps(), "Utang Pajak"); H += tb2([["Pajak Penghasilan Pasal 21", P("..."), P("..."), "i"], ["Pajak Penghasilan Pasal 23 dan 4(2)", P("..."), P("..."), "i"], ["Pajak Penghasilan Pasal 29", P("..."), P("..."), "i"], ["Pajak Pertambahan Nilai", P("..."), P("..."), "i"], ["Jumlah", a("utangpajak", 1), a("utangpajak", 0), "bb"]]); }
    H += H2(ps(), "Beban Pajak Penghasilan");
    H += tb2([["Kini", Math.abs(a("pajakkini", 1)), Math.abs(a("pajakkini", 0)), "i"], ["Tangguhan", a("pajaktgh", 1), a("pajaktgh", 0), "i"], ["Beban pajak penghasilan, neto", T1.PAJAK, T0.PAJAK, "bb"]]);
    H += p(`Rekonsiliasi antara beban pajak penghasilan yang dihitung dengan menerapkan tarif pajak yang berlaku sebesar 22% atas laba sebelum pajak penghasilan dengan beban pajak penghasilan sebagaimana disajikan dalam laba rugi adalah sebagai berikut:`);
    const e1 = T1.LSBP * .22, e0 = T0.LSBP * .22;
    H += tb2([["Laba sebelum pajak penghasilan", T1.LSBP, T0.LSBP, ""], ["Beban pajak dengan tarif yang berlaku (22%)", Math.round(e1), Math.round(e0), "i"], ["Pengaruh pajak atas beda tetap dan lainnya", Math.round(T1.PAJAK - e1), Math.round(T0.PAJAK - e0), "i"], ["Beban pajak penghasilan, neto", T1.PAJAK, T0.PAJAK, "bb"]]);
    if (has("apt") || has("lpt")) { H += H2(ps(), "Aset (Liabilitas) Pajak Tangguhan"); H += tb2([["Liabilitas imbalan kerja", P("..."), P("..."), "i"], ["Cadangan kerugian penurunan nilai piutang", P("..."), P("..."), "i"], ["Aset tetap", P("..."), P("..."), "i"], ["Aset (liabilitas) pajak tangguhan, neto", a("apt", 1) - a("lpt", 1), a("apt", 0) - a("lpt", 0), "bb"]]); }
    H += H2(ps(), "Administrasi");
    H += p(`Berdasarkan Undang-Undang Perpajakan yang berlaku di Indonesia, Perusahaan menghitung, menetapkan, dan membayar sendiri jumlah pajak yang terutang (self-assessment). Direktur Jenderal Pajak dapat menetapkan atau mengubah liabilitas pajak dalam batas waktu lima tahun sejak saat terutangnya pajak.`);
  }
  if (N.at) {
    H += NT("at", "Aset Tetap");
    H += tb2([["Biaya perolehan", a("atbiaya", 1), a("atbiaya", 0), "i"], ["Akumulasi penyusutan", -Math.abs(a("atakum", 1)), -Math.abs(a("atakum", 0)), "i"], ["Nilai tercatat", T1.AT, T0.AT, "bb"]]);
    H += p(`Mutasi aset tetap per kelompok untuk tahun ${Y1}:`);
    H += table([["Biaya perolehan", "", "", "h"], ...["Tanah", "Bangunan dan prasarana", "Mesin dan peralatan", "Kendaraan", "Peralatan kantor"].map(k => [k, P("saldo awal"), P("penambahan"), "i"]), ["Jumlah biaya perolehan", Math.abs(a("atbiaya", 0)), Math.abs(a("atbiaya", 1)), "b"], ["Akumulasi penyusutan", Math.abs(a("atakum", 0)), Math.abs(a("atakum", 1)), "b"], ["Nilai tercatat", T0.AT, T1.AT, "bb"]], {cols: ["1 Januari " + Y1, d1]});
    H += p(`Beban penyusutan dialokasikan ke beban pokok pendapatan sebesar ${P("Rp...")} dan beban umum dan administrasi sebesar ${P("Rp...")}. Aset tetap, kecuali tanah, diasuransikan terhadap risiko kebakaran, pencurian, dan risiko lainnya dengan nilai pertanggungan sebesar ${P("Rp...")}, yang menurut manajemen memadai. Manajemen berpendapat bahwa tidak terdapat indikasi penurunan nilai aset tetap pada tanggal ${d1}.${T1.BANK ? ` Aset tetap berupa ${P("tanah dan bangunan / mesin")} dijadikan jaminan atas utang bank (Catatan ${c("bank")}).` : ""}`);
  }
  if (N.sewa) {
    H += NT("sewa", "Sewa");
    H += p(`Perusahaan menyewa ${P("gedung kantor / gudang / kendaraan")} dengan masa sewa ${P("...")} tahun.`);
    H += tb2([["Aset hak guna, neto", a("rou", 1), a("rou", 0), ""], ["Liabilitas sewa", T1.SEWA, T0.SEWA, ""], ["Dikurangi bagian lancar", -a("sewalancar", 1), -a("sewalancar", 0), "i"], ["Bagian jangka panjang", a("sewapanjang", 1), a("sewapanjang", 0), "bb"]]);
    H += p(`Beban penyusutan aset hak guna tahun ${Y1} sebesar ${P("Rp...")}, beban bunga atas liabilitas sewa sebesar ${P("Rp...")}, dan beban sewa jangka pendek sebesar ${P("Rp...")}.`);
  }
  if (N.propinv) { H += NT("propinv", "Properti Investasi"); H += tb2([["Properti investasi", a("propinv", 1), a("propinv", 0), "bb"]]); H += p(`Pendapatan sewa dari properti investasi tahun ${Y1} sebesar ${P("Rp...")}. Nilai wajar properti investasi berdasarkan penilaian ${P("KJPP ...")} adalah sebesar ${P("Rp...")}.`); }
  if (N.atb) { H += NT("atb", "Aset Takberwujud"); H += tb2([["Perangkat lunak, neto", a("atb", 1), a("atb", 0), "bb"]]); }
  if (N.invasos) { H += NT("invasos", "Investasi pada Entitas Asosiasi"); H += tb2([[P("nama entitas asosiasi, persentase kepemilikan"), a("invasos", 1), a("invasos", 0), "bb"]]); }
  if (N.atllain) { H += NT("atllain", "Aset Tidak Lancar Lainnya"); H += tb2([["Uang jaminan", P("..."), P("..."), "i"], ["Lain-lain", P("..."), P("..."), "i"], ["Jumlah", a("atllain", 1), a("atllain", 0), "bb"]]); }
  if (N.bank) {
    H += NT("bank", "Utang Bank");
    H += tb2([["Utang bank jangka pendek", a("ubpendek", 1), a("ubpendek", 0), ""], ["Utang bank jangka panjang", a("ublancar", 1) + a("ubpanjang", 1), a("ublancar", 0) + a("ubpanjang", 0), ""], ["Dikurangi bagian lancar", -a("ublancar", 1), -a("ublancar", 0), "i"], ["Bagian jangka panjang", a("ubpanjang", 1), a("ubpanjang", 0), "bb"]]);
    H += p(`Perusahaan memperoleh fasilitas kredit dari ${P("nama bank")} berupa ${P("Kredit Modal Kerja / Kredit Investasi")} dengan batas maksimum ${P("Rp...")}. Fasilitas ini dikenakan suku bunga tahunan ${P("...%")} dan jatuh tempo pada ${P("tanggal")}. Fasilitas dijamin dengan ${P("piutang usaha, persediaan, dan aset tetap")} (Catatan ${[c("piu"), c("persediaan"), c("at")].filter(Boolean).join(", ")}).`);
    H += p(`Perjanjian kredit mensyaratkan Perusahaan memenuhi rasio keuangan tertentu, antara lain ${P("rasio utang terhadap ekuitas maksimal ...x dan Debt Service Coverage Ratio minimal ...x")}, serta memperoleh persetujuan tertulis bank untuk tindakan tertentu. Pada tanggal ${d1}, Perusahaan telah memenuhi seluruh persyaratan tersebut.`);
  }
  if (N.uu) { H += NT("uu", "Utang Usaha"); H += tb2([["Pihak ketiga", a("uu3", 1), a("uu3", 0), "i"], ["Pihak berelasi (Catatan " + c("rel") + ")", a("uurel", 1), a("uurel", 0), "i"], ["Jumlah", a("uu3", 1) + a("uurel", 1), a("uu3", 0) + a("uurel", 0), "bb"]]); H += p(`Utang usaha timbul dari pembelian barang dan jasa dengan jangka waktu kredit ${P("30 - 60")} hari, tidak dikenakan bunga, dan tidak dijamin.${d.f.f_valas ? ` Utang usaha dalam mata uang asing sebesar ${P("USD ...")}.` : ""}`); }
  if (N.ul) { H += NT("ul", "Utang Lain-Lain"); H += tb2([["Utang lain-lain", a("ul", 1), a("ul", 0), "bb"]]); }
  if (N.akrual) { H += NT("akrual", "Beban Akrual"); H += tb2([["Gaji dan tunjangan", P("..."), P("..."), "i"], ["Bunga", P("..."), P("..."), "i"], ["Jasa profesional", P("..."), P("..."), "i"], ["Lain-lain", P("..."), P("..."), "i"], ["Jumlah", a("akrual", 1), a("akrual", 0), "bb"]]); }
  if (N.imbalan) {
    H += NT("imbalan", "Liabilitas Imbalan Kerja");
    H += p(`Liabilitas imbalan kerja pada tanggal ${d1}${pr ? ` dan ${Y0}` : ""} dihitung oleh ${P("nama aktuaris independen")} dalam laporannya tanggal ${P("tanggal")} menggunakan metode projected unit credit dengan asumsi utama sebagai berikut:`);
    H += tb2([["Tingkat diskonto per tahun", P("...%"), P("...%"), "i"], ["Tingkat kenaikan gaji per tahun", P("...%"), P("...%"), "i"], ["Tingkat mortalitas", "TMI IV", "TMI IV", "i"], ["Usia pensiun normal", P("... tahun"), P("... tahun"), "i"]]);
    H += tb2([["Liabilitas imbalan kerja", a("imbalan", 1), a("imbalan", 0), "bb"], ["Pengukuran kembali di penghasilan komprehensif lain, setelah pajak", a("oci", 1), a("oci", 0), ""]]);
    H += p(`Analisis sensitivitas: kenaikan (penurunan) tingkat diskonto sebesar 1% akan menurunkan (menaikkan) liabilitas imbalan kerja sebesar ${P("Rp...")}.`);
  }
  if (N.modal) {
    H += NT("modal", "Modal Saham");
    H += p(`Susunan pemegang saham Perusahaan pada tanggal ${d1} adalah sebagai berikut:`);
    H += table([[P("Nama pemegang saham 1"), P("jumlah saham"), P("...%"), "i"], [P("Nama pemegang saham 2"), P("jumlah saham"), P("...%"), "i"], ["Jumlah modal ditempatkan dan disetor penuh: Rp" + idn(a("modal", 1)), P("jumlah saham"), "100%", "bb"]], {cols: ["Jumlah Saham", "Persentase"]});
    if (pr && a("modal", 1) !== a("modal", 0)) H += p(`Perubahan modal ditempatkan dan disetor dari Rp${idn(a("modal", 0))} menjadi Rp${idn(a("modal", 1))} dilakukan berdasarkan ${P("akta dan keputusan RUPS")}.`);
  }
  if (N.tmd) { H += NT("tmd", "Tambahan Modal Disetor"); H += tb2([["Tambahan modal disetor", a("tmd", 1), a("tmd", 0), "bb"]]); }
  if (N.saldolaba) {
    H += NT("saldolaba", "Saldo Laba");
    const div = a("saldolaba", 0) + T1.LB - a("saldolaba", 1);
    if (pr) { H += table([["Saldo awal tahun", a("saldolaba", 0), "", "i"], ["Laba tahun berjalan", T1.LB, "", "i"], ["Dividen dan lain-lain", -div, "", "i"], ["Saldo akhir tahun", a("saldolaba", 1), "", "bb"]], {cols: [String(Y1)]}); }
    H += p(`Sesuai Pasal 70 Undang-Undang No. 40 Tahun 2007 tentang Perseroan Terbatas, Perusahaan wajib menyisihkan jumlah tertentu dari laba bersih setiap tahun buku untuk cadangan sampai cadangan tersebut mencapai paling sedikit 20% dari jumlah modal ditempatkan dan disetor. ${pr && Math.round(div) ? `Berdasarkan ${P("keputusan RUPS tanggal ...")}, pemegang saham menyetujui pembagian dividen tunai sebesar Rp${idn(div)}.` : `Pada tahun ${Y1} tidak terdapat pembagian dividen.`}`);
  }
  if (N.pend) { H += NT("pend", "Pendapatan"); H += tb2([[P("Jenis pendapatan 1"), P("..."), P("..."), "i"], [P("Jenis pendapatan 2"), P("..."), P("..."), "i"], ["Jumlah", a("pendapatan", 1), a("pendapatan", 0), "bb"]]); H += p(`Berdasarkan waktu pengakuan: ${d.f.f_kontrak ? `sepanjang waktu ${P("Rp...")} dan pada titik waktu ${P("Rp...")}` : `seluruh pendapatan diakui pada titik waktu`}. Pendapatan dari pelanggan yang melebihi 10% dari jumlah pendapatan: ${P("nama pelanggan dan jumlah, atau tidak ada")}.`); }
  if (N.hpp) { H += NT("hpp", "Beban Pokok Pendapatan"); H += tb2([["Bahan baku / pembelian", P("..."), P("..."), "i"], ["Upah langsung", P("..."), P("..."), "i"], ["Beban overhead", P("..."), P("..."), "i"], ["Jumlah", Math.abs(a("hpp", 1)), Math.abs(a("hpp", 0)), "bb"]]); H += p(`Pembelian dari pemasok yang melebihi 10% dari jumlah pendapatan: ${P("nama pemasok dan jumlah, atau tidak ada")}.`); }
  if (N.busaha) { H += NT("busaha", "Beban Usaha"); H += tb2([["Beban penjualan", Math.abs(a("bjual", 1)), Math.abs(a("bjual", 0)), ""], ["Beban umum dan administrasi", "", "", "h"], ["Gaji dan tunjangan", P("..."), P("..."), "i"], ["Penyusutan", P("..."), P("..."), "i"], ["Jasa profesional", P("..."), P("..."), "i"], ["Lain-lain", P("..."), P("..."), "i"], ["Jumlah beban umum dan administrasi", Math.abs(a("bumum", 1)), Math.abs(a("bumum", 0)), "b"], ["Jumlah beban usaha", Math.abs(a("bjual", 1)) + Math.abs(a("bumum", 1)), Math.abs(a("bjual", 0)) + Math.abs(a("bumum", 0)), "bb"]]); }
  if (N.lain) { H += NT("lain", "Pendapatan (Beban) Lain-Lain"); H += tb2([[d.f.f_valas ? "Laba (rugi) selisih kurs, neto" : "Laba penjualan aset tetap", P("..."), P("..."), "i"], ["Lain-lain", P("..."), P("..."), "i"], ["Neto", a("lain", 1), a("lain", 0), "bb"]]); }
  if (N.keu) { H += NT("keu", "Pendapatan dan Beban Keuangan"); H += tb2([["Pendapatan bunga jasa giro dan deposito", a("pkeu", 1), a("pkeu", 0), ""], ["Beban bunga utang bank", P("..."), P("..."), "i"], ["Beban bunga liabilitas sewa", P("..."), P("..."), "i"], ["Jumlah beban keuangan", Math.abs(a("bkeu", 1)), Math.abs(a("bkeu", 0)), "bb"]]); }
  if (N.rel) {
    H += NT("rel", "Saldo dan Transaksi dengan Pihak-Pihak Berelasi");
    H += p(`Sifat hubungan dengan pihak berelasi:`);
    H += table([[P("Nama pihak berelasi"), P("Entitas sepengendali / pemegang saham"), P("Penjualan / pembelian / pinjaman"), ""]], {head: "Pihak Berelasi", cols: ["Sifat Hubungan", "Transaksi"]});
    const relRows = [["Piutang usaha", a("piurel", 1), a("piurel", 0), "i"], ["Utang usaha", a("uurel", 1), a("uurel", 0), "i"], ["Utang pihak berelasi jangka panjang", a("utangrel", 1), a("utangrel", 0), "i"]].filter(x => x[1] || x[2]);
    if (relRows.length) H += tb2(relRows);
    H += p(`Kompensasi yang diberikan kepada Dewan Komisaris dan Direksi sebagai personel manajemen kunci berupa imbalan kerja jangka pendek sebesar ${P("Rp...")} pada tahun ${Y1}.`);
  }
  if (N.risiko) {
    H += NT("risiko", "Tujuan dan Kebijakan Manajemen Risiko Keuangan");
    H += p(`Risiko utama yang timbul dari instrumen keuangan Perusahaan adalah risiko kredit, risiko likuiditas, dan risiko pasar${T1.BANK ? " (risiko suku bunga)" : ""}${d.f.f_valas ? " termasuk risiko mata uang asing" : ""}. Direksi menelaah dan menyetujui kebijakan untuk mengelola risiko-risiko tersebut.`);
    H += p(`<i>Risiko kredit.</i> Risiko kredit terutama berasal dari piutang usaha. Perusahaan mengelola risiko ini dengan menetapkan batas kredit pelanggan dan memantau saldo piutang secara berkelanjutan. Eksposur maksimum risiko kredit adalah sebesar nilai tercatat aset keuangan, yaitu Rp${idn(a("kas", 1) + T1.PIU + a("piulain", 1))} pada tanggal ${d1}.`);
    H += p(`<i>Risiko likuiditas.</i> Perusahaan mengelola risiko likuiditas dengan memantau proyeksi arus kas dan menjaga ketersediaan fasilitas kredit. Liabilitas keuangan jangka pendek pada tanggal ${d1} sebesar Rp${idn(T1.LPD - a("utangpajak", 1) - a("liabkontrak", 1))} jatuh tempo dalam satu tahun.`);
    if (T1.BANK) H += p(`<i>Risiko suku bunga.</i> Eksposur Perusahaan terhadap risiko perubahan suku bunga pasar terutama terkait dengan utang bank dengan suku bunga mengambang sebesar Rp${idn(T1.BANK)}. Kenaikan suku bunga sebesar 100 basis poin akan menurunkan laba sebelum pajak sekitar Rp${idn(T1.BANK * .01)}.`);
    if (d.f.f_valas) H += p(`<i>Risiko mata uang asing.</i> Perusahaan terekspos risiko mata uang asing atas transaksi dalam ${P("USD")}. Aset dan liabilitas moneter dalam mata uang asing: ${P("rincian")}.`);
  }
  if (N.modalmgmt) {
    H += NT("modalmgmt", "Manajemen Permodalan");
    H += p(`Tujuan utama pengelolaan modal Perusahaan adalah memastikan dipertahankannya rasio modal yang sehat untuk mendukung usaha dan memaksimalkan nilai pemegang saham. Perusahaan memantau modal menggunakan rasio utang terhadap ekuitas sebagai berikut:`);
    H += tb2([["Jumlah utang bank dan liabilitas sewa", T1.BANK + T1.SEWA, T0.BANK + T0.SEWA, ""], ["Jumlah ekuitas", T1.EK, T0.EK, ""], ["Rasio utang terhadap ekuitas", T1.EK ? ((T1.BANK + T1.SEWA) / T1.EK).toFixed(2) + "x" : "-", T0.EK ? ((T0.BANK + T0.SEWA) / T0.EK).toFixed(2) + "x" : "-", "bb"]]);
  }
  if (N.baru) {
    H += NT("baru", "Standar Akuntansi yang Telah Diterbitkan namun Belum Berlaku Efektif");
    H += p(`Standar dan amendemen yang telah diterbitkan Dewan Standar Akuntansi Keuangan Ikatan Akuntan Indonesia namun belum berlaku efektif untuk tahun buku ${Y1} adalah sebagai berikut:`);
    const L = [["1 Januari 2027", "PSAK 118, \"Penyajian dan Pengungkapan dalam Laporan Keuangan\", menggantikan PSAK 201"], ["1 Januari 2027", "PSAK 119, \"Entitas Anak tanpa Akuntabilitas Publik: Pengungkapan\""], ["1 Januari 2027", "Amendemen PSAK 221, \"Penjabaran ke Mata Uang Penyajian Hiperinflasi\""], ["1 Januari 2027", "Amendemen PSAK 228, \"Opsi Nilai Wajar untuk Investasi pada Entitas Asosiasi dan Ventura Bersama\""], ["1 Januari 2029", "PSAK 120, \"Aset Regulatori dan Liabilitas Regulatori\""]];
    if (Y1 < 2026) L.unshift(["1 Januari 2026", "Amendemen PSAK 109 dan PSAK 107, \"Klasifikasi dan Pengukuran Instrumen Keuangan\""]);
    H += `<table style="${TB}"><tr><th style="${TH};text-align:left">Berlaku Efektif</th><th style="${TH};text-align:left">Standar</th></tr>${L.map(([e, s]) => `<tr><td style="${TL};white-space:nowrap">${e}</td><td style="${TL}">${s}</td></tr>`).join("")}</table>`;
    H += p(`Perusahaan sedang mengevaluasi dampak penerapan standar dan amendemen tersebut. PSAK 118 diperkirakan berdampak pada penyajian laporan laba rugi, yaitu pengelompokan penghasilan dan beban ke dalam kategori operasi, investasi, dan pendanaan, serta pengungkapan ukuran kinerja yang ditetapkan manajemen. Angka komparatif tahun ${Y1} akan disajikan kembali pada saat penerapan.`);
  }
  if (N.peristiwa) { H += NT("peristiwa", "Peristiwa setelah Periode Pelaporan"); H += p(`${P("Uraikan peristiwa material setelah " + d1 + " sampai tanggal otorisasi laporan keuangan, atau tulis: Tidak terdapat peristiwa material setelah periode pelaporan yang memerlukan penyesuaian atau pengungkapan dalam laporan keuangan.")}`); }
  H += `</div>`;
  return {html: H, fw, notes: n - 1};
}

function renderCalk(d, r) {
  const out = buildCalk(d, r);
  const fwn = {sak: "SAK Indonesia", ep: "SAK EP", emkm: "SAK EMKM"}[out.fw];
  return `<div class="res">
  <h3>Draf CALK: ${esc(d.f.nama || "Perusahaan Anda")} (${fwn}, ${out.notes} Catatan)</h3>
  <p class="lock">Bagian bertanda kuning wajib dilengkapi. Tombol Salin ke Word menyalin tabel dan format sekaligus; tempel di Word dengan Ctrl+V.</p>
  <div class="actions" style="margin:12px 0 16px"><button type="button" class="btn" id="copy">Salin ke Word</button><button type="button" class="btn btn-ghost" id="dl">Download .doc</button><a class="btn btn-ghost" target="_blank" rel="noopener" href="https://wa.me/6282245260121?text=${encodeURIComponent("Halo tim UpdateSAK, kami sudah membuat draf CALK " + (d.f.nama || "") + " dan ingin dibantu finalisasi sebelum audit.")}">Minta Review Tim</a></div>
  <div class="calk-doc" id="calkDoc">${out.html}</div>
  </div>`;
}


/* ---------- Panel indikasi langsung ---------- */
function live() {
  const box = $("#live"); if (!box) return;
  const d = read();
  const ok = (d.f.nama || "").trim().length > 2;
  box.classList.toggle("ready", ok);
  const r = analyze(d), T = d.t[1];
  $("#lvFw").textContent = r.fwName + (d.f.f_syariah ? " + Syariah" : "");
  const au = $("#lvAudit"); au.textContent = r.audit.length ? "Wajib Audit" : "Belum Wajib Audit"; au.className = r.audit.length ? "w" : "";
  $("#lvPsak").textContent = r.items.length;
  $("#lvNew").textContent = r.news.length;
  $("#lvKelas").textContent = d.v.pendapatan[1] ? r.umkm.replace("Usaha ", "").replace(" (di atas kriteria UMKM)", "") : "-";
  const tot = Math.abs(T.ASET) || 1;
  for (const k of ["AL", "ATL", "LIAB", "EK"]) {
    const p = T.ASET ? Math.max(0, Math.min(100, T[k] / tot * 100)) : 0;
    $(`[data-b="${k}"]`).style.width = p + "%"; $(`[data-p="${k}"]`).textContent = Math.round(p) + "%";
  }
  const g = (id, val, max, lab) => { const f = val == null || !isFinite(val) ? 0 : Math.max(0, Math.min(1, val / max)); $(id).style.strokeDashoffset = 126 * (1 - f); return val == null || !isFinite(val) ? "-" : val.toFixed(2) + "x"; };
  $("#lvCr").textContent = g("#gCr", T.LPD ? T.AL / T.LPD : null, 3);
  $("#lvDer").textContent = g("#gDer", T.EK ? T.BANK / T.EK : null, 3);
}
$("#form").addEventListener("input", e => { if (!e.target.closest(".finx")) live(); });
$("#form").addEventListener("change", live);

/* ---------- Aksi ---------- */
function run() {
  const d = read();
  if (!IDS.some(id => d.v[id][1])) { $("#cek").className = "chk bad"; $("#cek").textContent = "Isi minimal angka tahun berjalan terlebih dahulu."; $("#cek").scrollIntoView({behavior: "smooth", block: "center"}); return; }
  const r = analyze(d);
  const box = $("#hasil");
  box.innerHTML = mode === "calk" ? renderCalk(d, r) : renderStd(d, r);
  box.hidden = false;
  box.scrollIntoView({behavior: "smooth", block: "start"});
  const tc = $("#toCalk"); if (tc) tc.onclick = () => { setMode("calk"); goStep(3); $("#kalkulator").scrollIntoView({behavior: "smooth", block: "start"}); };
  const cp = $("#copy"); if (cp) cp.onclick = copyDoc;
  const dl = $("#dl"); if (dl) dl.onclick = () => downloadDoc(d.f.nama);
}
async function copyDoc() {
  const el = $("#calkDoc"), html = el.innerHTML, btn = $("#copy");
  try {
    await navigator.clipboard.write([new ClipboardItem({"text/html": new Blob([html], {type: "text/html"}), "text/plain": new Blob([el.innerText], {type: "text/plain"})})]);
  } catch (e) {
    const rg = document.createRange(); rg.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(rg);
    try { document.execCommand("copy"); } catch (_) {} s.removeAllRanges();
  }
  btn.textContent = "Tersalin"; setTimeout(() => btn.textContent = "Salin ke Word", 2200);
}
function downloadDoc(nama) {
  const html = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><title>CALK</title><style>@page{size:A4;margin:2.5cm 2cm}body{font-family:'Times New Roman';font-size:11pt}</style></head><body>${$("#calkDoc").innerHTML}</body></html>`;
  const b = new Blob(["﻿", html], {type: "application/msword"});
  const u = URL.createObjectURL(b), x = document.createElement("a");
  x.href = u; x.download = "CALK " + (nama || "Perusahaan").replace(/[^\w .-]/g, "") + ".doc"; document.body.appendChild(x); x.click(); x.remove(); setTimeout(() => URL.revokeObjectURL(u), 1000);
}
$("#go").onclick = run;
$("#reset").onclick = () => { $("#form").reset(); $$(".finx input").forEach(i => i.value = ""); $("#hasil").hidden = true; refresh(); yearLabels(); };

const SAMPLE = {
  nama: "PT Contoh Karya Nusantara", kota: "Batam", industri: "dagang", status: "privat",
  akta_no: "12", akta_tgl: "14 Maret 2012", kegiatan: "perdagangan besar bahan bangunan dan peralatan konstruksi", mulai: "2012",
  komisaris: "Komisaris Utama: Budi Santoso\nKomisaris: Rina Kartika", direksi: "Direktur Utama: Andi Wijaya\nDirektur: Sari Lestari", karyawan: "85", otorisasi: "20 Maret 2027",
  flags: ["f_valas", "f_kredit"],
  v: { // juta Rupiah: [tahun berjalan, tahun lalu]
    kas: [4850, 3900], piu3: [12400, 10800], piurel: [1150, 900], cke: [620, 510], piulain: [380, 300], persediaan: [9700, 8900], uangmuka: [760, 650], pajakdm: [540, 480],
    atbiaya: [18500, 16900], atakum: [6300, 5100], rou: [1200, 1500], atb: [240, 280], apt: [410, 360], atllain: [300, 260],
    ubpendek: [6000, 4330], uu3: [7800, 7100], uurel: [650, 500], ul: [420, 380], akrual: [530, 470], utangpajak: [610, 560], liabkontrak: [900, 700], ublancar: [1200, 1200], sewalancar: [380, 360],
    ubpanjang: [3600, 4800], sewapanjang: [760, 1120], imbalan: [1450, 1250],
    modal: [10000, 10000], saldolaba: [9420, 7000], ociek: [-210, -150],
    pendapatan: [61500, 54200], hpp: [47800, 42600], bjual: [2900, 2500], bumum: [5600, 5100], lain: [150, 80], pkeu: [90, 70], bkeu: [1050, 1120], pajakkini: [1010, 700], pajaktgh: [-40, -20], oci: [-60, -40]
  }
};
$("#contoh").onclick = () => {
  const F = $("#form");
  for (const k of ["nama", "kota", "industri", "status", "akta_no", "akta_tgl", "kegiatan", "mulai", "komisaris", "direksi", "karyawan", "otorisasi"]) if (F.elements[k]) F.elements[k].value = SAMPLE[k];
  $$("#flags input").forEach(c => c.checked = SAMPLE.flags.includes(c.name));
  $$(".finx input").forEach(i => { const x = SAMPLE.v[i.dataset.id]; i.value = x ? fmtIn(x[i.dataset.y === "1" ? 0 : 1] * 1e6) : ""; });
  refresh(); live();
};

/* Animasi saat terlihat */
const io = "IntersectionObserver" in window ? new IntersectionObserver((es, o) => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("on"); o.unobserve(e.target); } }), {threshold: .25}) : null;
["#tree", "#rail", "#pages", "#doc"].forEach(sel => { const el = $(sel); if (el) io ? io.observe(el) : el.classList.add("on"); });
$$("#pages div").forEach((e, i) => e.style.transitionDelay = (i * .12) + "s");
$$("[data-count]").forEach(el => { const n = +el.dataset.count; if (!n) return; let c = 0; const st = performance.now(); const tick = t => { c = Math.min(1, (t - st) / 1200); el.textContent = Math.round(n * (1 - Math.pow(1 - c, 3))); if (c < 1) requestAnimationFrame(tick); }; requestAnimationFrame(tick); });
if (window.SAK_DATA && $("#sakUpd")) $("#sakUpd").textContent = "Sumber SAK Online IAI, dicek " + SAK_DATA.updated + ".";
goStep(0); live();
})();
