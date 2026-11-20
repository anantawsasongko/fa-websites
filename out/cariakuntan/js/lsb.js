/* lsb.js: LK Siap Bank (CariAkuntan, 20 Nov 2026). Sumber: fa_content/lsb20261120/lsb.js, dipasang oleh ca_lk_siap_bank_20261120.py.
   Semua diolah di browser. Tidak ada data mutasi atau angka yang dikirim ke server. */
(function () {
  'use strict';
  var root = document.getElementById('lsb'); if (!root) return;
  var XLSX_URL = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
  var WA = '6282245260121';
  var $ = function (s, r) { return (r || root).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || root).querySelectorAll(s)); };
  function ev(n, p) { try { if (window.gtag) gtag('event', n, p || {}); } catch (e) {} }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---------- angka dan tanggal ---------- */
  function num(v) {
    if (typeof v === 'number') return isFinite(v) ? v : NaN;
    if (v == null) return NaN;
    var s = String(v).trim(); if (!s) return NaN;
    var neg = /^\(.*\)$/.test(s) || /^-/.test(s) || /-$/.test(s);
    s = s.replace(/[^0-9.,]/g, ''); if (!/\d/.test(s)) return NaN;
    var ld = s.lastIndexOf('.'), lc = s.lastIndexOf(','), dec = -1;
    if (ld > -1 && lc > -1) dec = Math.max(ld, lc);
    else { var i = Math.max(ld, lc); if (i > -1) { var after = s.length - i - 1, cnt = s.split(i === ld ? '.' : ',').length - 1; if (cnt === 1 && after !== 3) dec = i; } }
    var ip = dec > -1 ? s.slice(0, dec) : s, fp = dec > -1 ? s.slice(dec + 1) : '';
    var n = parseFloat(ip.replace(/[.,]/g, '') + (fp ? '.' + fp : ''));
    return isNaN(n) ? NaN : (neg ? -n : n);
  }
  function rp(n, short) {
    if (n == null || !isFinite(n)) return '-';
    var a = Math.abs(n), s;
    if (short) {
      if (a >= 1e12) s = (a / 1e12).toFixed(2).replace('.', ',') + ' triliun';
      else if (a >= 1e9) s = (a / 1e9).toFixed(2).replace('.', ',') + ' miliar';
      else if (a >= 1e6) s = (a / 1e6).toFixed(1).replace('.', ',') + ' juta';
      else s = Math.round(a).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    } else s = Math.round(a).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return (n < 0 ? '(' : '') + 'Rp' + s + (n < 0 ? ')' : '');
  }
  function tb(n) { if (!isFinite(n)) return '-'; var s = Math.round(Math.abs(n)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.'); return n < 0 ? '(' + s + ')' : s; }
  var BLN = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
  var BL3 = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
  var MON = { jan: 1, feb: 2, mar: 3, apr: 4, mei: 5, may: 5, jun: 6, jul: 7, agu: 8, agt: 8, ags: 8, aug: 8, sep: 9, okt: 10, oct: 10, nov: 11, nop: 11, des: 12, dec: 12 };
  function mkd(y, m, d) { if (y < 100) y += 2000; if (m < 1 || m > 12 || d < 1 || d > 31 || y < 2000 || y > 2100) return null; return { y: y, m: m, d: d }; }
  function pdate(v, cy) {
    if (v instanceof Date && !isNaN(v)) return mkd(v.getFullYear(), v.getMonth() + 1, v.getDate());
    if (typeof v === 'number') { if (v > 36000 && v < 80000) { var t = new Date(Math.round((v - 25569) * 864e5)); return mkd(t.getUTCFullYear(), t.getUTCMonth() + 1, t.getUTCDate()); } return null; }
    if (v == null) return null;
    var s = String(v).trim().replace(/^'+/, ''); if (!s) return null;
    var m;
    if ((m = /^(\d{4})[-\/.](\d{1,2})[-\/.](\d{1,2})/.exec(s))) return mkd(+m[1], +m[2], +m[3]);
    if ((m = /^(\d{1,2})[-\/.](\d{1,2})[-\/.](\d{2,4})(?!\d)/.exec(s))) { var a = +m[1], b = +m[2]; if (b > 12 && a <= 12) { var x = a; a = b; b = x; } return mkd(+m[3], b, a); }
    if ((m = /^(\d{1,2})[-\/ ]([A-Za-z]{3})[A-Za-z]*[-\/ ,]+(\d{2,4})/.exec(s))) { var mo = MON[m[2].toLowerCase()]; return mo ? mkd(+m[3], mo, +m[1]) : null; }
    if ((m = /^(\d{1,2})[-\/ ]([A-Za-z]{3})[A-Za-z]*$/.exec(s))) { var mo2 = MON[m[2].toLowerCase()]; return mo2 && cy ? mkd(cy, mo2, +m[1]) : null; }
    if ((m = /^(\d{1,2})[\/-](\d{1,2})$/.exec(s))) return cy ? mkd(cy, +m[2], +m[1]) : null;
    return null;
  }
  function dnum(o) { return Date.UTC(o.y, o.m - 1, o.d) / 864e5; }
  function dstr(o) { return o.d + ' ' + BLN[o.m - 1] + ' ' + o.y; }

  /* ---------- kategori ---------- */
  var CIN = { jual: 'Penerimaan usaha', bunga: 'Bunga dan pendapatan lain', pinjam: 'Pencairan pinjaman', pindah: 'Pindah buku atau setoran pemilik' };
  var COUT = { beli: 'Pembelian dan operasional', gaji: 'Gaji dan upah', sewa: 'Sewa', util: 'Listrik, air, internet', pajak: 'Pajak dan iuran', bank: 'Biaya bank', angs: 'Angsuran pinjaman', tunai: 'Tarik tunai', prive: 'Keperluan pribadi', pindah: 'Pindah buku ke rekening sendiri' };
  var KIN = ['jual', 'bunga', 'pinjam', 'pindah'], KOUT = ['beli', 'gaji', 'sewa', 'util', 'pajak', 'bank', 'angs', 'tunai', 'prive', 'pindah'];
  function catOf(desc, isIn) {
    var s = ' ' + String(desc || '').toLowerCase() + ' ';
    if (isIn) {
      if (/bunga|interest|jasa giro|bagi hasil|nisbah/.test(s)) return 'bunga';
      if (/pencairan|dropping|realisasi (kredit|pinjaman)|loan disb/.test(s)) return 'pinjam';
      if (/pindah buku|overbook|pemindahbukuan|setoran modal/.test(s)) return 'pindah';
      return 'jual';
    }
    if (/biaya adm|by adm|\badm\b|administrasi|biaya transfer|biaya trf|\bfee\b|pajak bunga|materai|meterai|biaya kartu/.test(s)) return 'bank';
    if (/gaji|salary|payroll|\bthr\b|upah|honor/.test(s)) return 'gaji';
    if (/\bsewa\b|\brent\b|kontrak ruko/.test(s)) return 'sewa';
    if (/\bpln\b|listrik|pdam|telkom|indihome|internet|telepon|pulsa|token|wifi/.test(s)) return 'util';
    if (/pajak|\bdjp\b|\bmpn\b|\bpph\b|\bppn\b|\bpbb\b|bpjs|kode billing/.test(s)) return 'pajak';
    if (/angsuran|cicilan|pinjaman|\bloan\b|leasing|\bkpr\b|installment|pembayaran kredit|byr kredit|multifinance|\bfinance\b/.test(s)) return 'angs';
    if (/tarik tunai|tarikan tunai|\batm\b|penarikan|cash withdrawal|\btarik\b/.test(s)) return 'tunai';
    if (/pribadi|\bprive\b/.test(s)) return 'prive';
    if (/pindah buku|overbook|pemindahbukuan/.test(s)) return 'pindah';
    return 'beli';
  }

  /* ---------- baca file ---------- */
  function csvRows(text) {
    text = text.replace(/^﻿/, '');
    var head = text.slice(0, 4000), best = ',', bc = -1;
    [',', ';', '\t', '|'].forEach(function (d) { var c = head.split(d).length; if (c > bc) { bc = c; best = d; } });
    var rows = [], row = [], cur = '', q = false, i, ch;
    for (i = 0; i < text.length; i++) {
      ch = text[i];
      if (q) { if (ch === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += ch; }
      else if (ch === '"') q = true;
      else if (ch === best) { row.push(cur); cur = ''; }
      else if (ch === '\n') { row.push(cur); rows.push(row); row = []; cur = ''; }
      else if (ch !== '\r') cur += ch;
    }
    if (cur !== '' || row.length) { row.push(cur); rows.push(row); }
    return rows;
  }
  var xlsxP = null;
  function loadXLSX() {
    if (window.XLSX) return Promise.resolve();
    if (!xlsxP) xlsxP = new Promise(function (ok, no) { var s = document.createElement('script'); s.src = XLSX_URL; s.onload = function () { ok(); }; s.onerror = function () { xlsxP = null; no(new Error('Pustaka pembaca Excel gagal dimuat. Periksa koneksi lalu coba lagi.')); }; document.head.appendChild(s); });
    return xlsxP;
  }
  function readFile(f) {
    var name = f.name.toLowerCase();
    if (/\.pdf$/.test(name)) return Promise.reject(new Error('File PDF belum bisa dibaca otomatis. Unduh mutasi dalam format CSV atau Excel dari internet banking, atau kirim PDF-nya lewat WhatsApp untuk kami bantu.'));
    return new Promise(function (ok, no) {
      var r = new FileReader();
      r.onerror = function () { no(new Error('File tidak bisa dibaca.')); };
      if (/\.(csv|txt)$/.test(name)) { r.onload = function () { ok(csvRows(String(r.result))); }; r.readAsText(f); }
      else if (/\.(xlsx|xls)$/.test(name)) {
        r.onload = function () {
          loadXLSX().then(function () {
            try {
              var wb = XLSX.read(new Uint8Array(r.result), { type: 'array', cellDates: true }), all = [];
              wb.SheetNames.forEach(function (n) { all = all.concat(XLSX.utils.sheet_to_json(wb.Sheets[n], { header: 1, raw: true, defval: '' })); });
              ok(all);
            } catch (e) { no(new Error('File Excel tidak bisa dibuka.')); }
          }, no);
        };
        r.readAsArrayBuffer(f);
      } else no(new Error('Format file belum didukung. Pakai CSV, XLS, atau XLSX.'));
    });
  }
  var HK = {
    date: /^(tanggal|tgl|date|posting date|trx date|transaction date|tanggal transaksi|waktu)/i,
    desc: /(keterangan|uraian|deskripsi|description|remark|rincian|berita|narrative|detail|transaksi)/i,
    out: /(debit|debet|keluar|withdrawal|pengeluaran|^db$)/i,
    inn: /(kredit|credit|masuk|deposit|penerimaan|^cr$|setoran)/i,
    amt: /(jumlah|amount|nominal|mutasi|nilai)/i,
    typ: /(^jenis|^type|^tipe|d\/k|db\/cr|^dk$)/i,
    bal: /(saldo|balance)/i
  };
  function detect(rows) {
    var map = { date: -1, desc: -1, out: -1, inn: -1, amt: -1, typ: -1, bal: -1 }, hrow = -1, i, j;
    for (i = 0; i < Math.min(rows.length, 60) && hrow < 0; i++) {
      var r = rows[i], m = { date: -1, desc: -1, out: -1, inn: -1, amt: -1, typ: -1, bal: -1 }, hit = 0;
      for (j = 0; j < r.length; j++) {
        var c = String(r[j] == null ? '' : r[j]).trim(); if (!c || c.length > 40) continue;
        if (m.date < 0 && HK.date.test(c)) { m.date = j; hit++; }
        else if (m.bal < 0 && HK.bal.test(c)) { m.bal = j; hit++; }
        else if (m.out < 0 && HK.out.test(c)) { m.out = j; hit++; }
        else if (m.inn < 0 && HK.inn.test(c)) { m.inn = j; hit++; }
        else if (m.typ < 0 && HK.typ.test(c)) { m.typ = j; hit++; }
        else if (m.amt < 0 && HK.amt.test(c)) { m.amt = j; hit++; }
        else if (m.desc < 0 && HK.desc.test(c)) { m.desc = j; hit++; }
      }
      if (m.date > -1 && hit >= 3) { map = m; hrow = i; }
    }
    if (hrow < 0) {
      /* tanpa judul kolom: tebak dari isi */
      var n = 0, st = []; rows.slice(0, 80).forEach(function (r) { n = Math.max(n, r.length); });
      for (j = 0; j < n; j++) st.push({ d: 0, n: 0, t: 0, len: 0 });
      rows.slice(0, 80).forEach(function (r) { for (var k = 0; k < n; k++) { var v = r[k]; if (v === '' || v == null) continue; if (pdate(v, 2026)) st[k].d++; else if (!isNaN(num(v)) && !/[a-z]{3}/i.test(String(v))) st[k].n++; else { st[k].t++; st[k].len += String(v).length; } } });
      var bd = -1, bt = -1;
      st.forEach(function (s, k) { if (s.d > 3 && (bd < 0 || s.d > st[bd].d)) bd = k; if (s.t > 3 && (bt < 0 || s.len > st[bt].len)) bt = k; });
      var nums = []; st.forEach(function (s, k) { if (k !== bd && s.n > 3) nums.push(k); });
      map.date = bd; map.desc = bt;
      if (nums.length >= 3) { map.out = nums[0]; map.inn = nums[1]; map.bal = nums[nums.length - 1]; }
      else if (nums.length === 2) { map.amt = nums[0]; map.bal = nums[1]; }
      else if (nums.length === 1) map.amt = nums[0];
    }
    if (map.desc < 0 && map.date > -1) map.desc = map.date + 1;
    return { map: map, hrow: hrow };
  }
  function parseRows(rows, map, hrow) {
    var cy = 0, i, tx = [], pre = rows.slice(0, Math.max(hrow, 0) + 1).map(function (r) { return r.join(' '); }).join(' '), my = /(20\d\d)/.exec(pre);
    cy = my ? +my[1] : new Date().getFullYear();
    var last = null;
    for (i = hrow + 1; i < rows.length; i++) {
      var r = rows[i]; if (!r || !r.length) continue;
      var d = pdate(r[map.date], cy); if (!d) continue;
      if (last && d.y === last.y && d.m < last.m - 6 && !/\d{4}/.test(String(r[map.date]))) { cy++; d.y = cy; }
      var desc = String(r[map.desc] == null ? '' : r[map.desc]).replace(/\s+/g, ' ').trim();
      var inn = 0, out = 0;
      if (map.out > -1 || map.inn > -1) {
        out = Math.abs(num(r[map.out])) || 0; inn = Math.abs(num(r[map.inn])) || 0;
      } else if (map.amt > -1) {
        var raw = String(r[map.amt] == null ? '' : r[map.amt]), a = num(raw), flag = '';
        if (map.typ > -1) flag = String(r[map.typ] || '');
        if (!flag) { var mm = /\b(DB|CR|D|K|C)\b\s*$/i.exec(raw.trim()); if (mm) flag = mm[1]; }
        if (!flag) { var nx = String(r[map.amt + 1] == null ? '' : r[map.amt + 1]).trim(); if (/^(DB|CR|D|K|C|DEBIT|DEBET|KREDIT|CREDIT)$/i.test(nx)) flag = nx; }
        if (isNaN(a)) continue;
        if (flag) { if (/^(DB|D|DEBIT|DEBET)/i.test(flag.trim())) out = Math.abs(a); else inn = Math.abs(a); }
        else if (a < 0) out = -a; else inn = a;
      }
      if (!inn && !out) continue;
      if (/saldo awal|opening balance|saldo akhir/i.test(desc)) continue;
      var bal = map.bal > -1 ? num(r[map.bal]) : NaN;
      tx.push({ y: d.y, m: d.m, d: d.d, desc: desc, inn: inn, out: out, bal: bal, cat: catOf(desc, inn > 0) });
      last = d;
    }
    /* mutasi tanpa tahun: jangan sampai jatuh di masa depan */
    if (tx.length && !my) { var now = new Date(), mx = tx[tx.length - 1]; if (Date.UTC(mx.y, mx.m - 1, mx.d) > now.getTime() + 40 * 864e5) tx.forEach(function (t) { t.y--; }); }
    return tx;
  }

  /* ---------- data contoh (dummy) ---------- */
  function contoh() {
    var seed = 20261120, tx = []; function rnd() { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }
    var now = new Date(), ey = now.getFullYear(), em = now.getMonth(); if (em === 0) { em = 12; ey--; }
    var musim = [0.55, 0.65, 0.9, 1.15, 1.4, 1.05, 0.85, 1.2, 1.5, 1.25, 0.9, 0.6], bal = 46e6, k, i;
    for (k = 11; k >= 0; k--) {
      var m = em - k, y = ey; while (m < 1) { m += 12; y--; }
      var f = musim[m - 1], list = [];
      for (i = 0; i < 26; i++) list.push([1 + Math.floor(rnd() * 28), ['TRSF E-BANKING CR PEMBAYARAN INV', 'SETORAN TUNAI TOKO', 'TRSF CR QRIS SETTLEMENT', 'TRSF E-BANKING CR CV MITRA BANGUN'][Math.floor(rnd() * 4)] + ' ' + (1000 + Math.floor(rnd() * 8999)), Math.round((3.2e6 + rnd() * 9.5e6) * f / 1000) * 1000, 0]);
      for (i = 0; i < 12; i++) list.push([2 + Math.floor(rnd() * 26), ['TRSF E-BANKING DB PT SEMEN DISTRIBUSI', 'TRSF E-BANKING DB UD BAJA RINGAN', 'TRSF DB CV CAT WARNA', 'TRSF E-BANKING DB PT KERAMIK NUSA'][Math.floor(rnd() * 4)], 0, Math.round((6.5e6 + rnd() * 9e6) * f / 1000) * 1000]);
      list.push([25, 'PAYROLL GAJI KARYAWAN', 0, 18500000]); list.push([5, 'SEWA GUDANG BULANAN', 0, 6500000]);
      list.push([12, 'PEMBAYARAN PLN POSTPAID', 0, 1150000 + Math.round(rnd() * 300) * 1000]); list.push([12, 'INDIHOME INTERNET', 0, 420000]);
      list.push([15, 'KODE BILLING PAJAK PPH FINAL', 0, Math.round(0.005 * 190e6 * f / 1000) * 1000]);
      list.push([10, 'ANGSURAN KREDIT KENDARAAN LEASING', 0, 4850000]); list.push([28, 'BIAYA ADM', 0, 15000]);
      list.push([8, 'TARIK TUNAI ATM', 0, 12000000]); list.push([20, 'TARIK TUNAI ATM', 0, 10000000 + Math.round(rnd() * 4) * 1e6]); list.push([27, 'TRSF E-BANKING DB KE REKENING PRIBADI', 0, 10000000]);
      list.push([28, 'BUNGA', Math.round(bal * 0.0008), 0]);
      list.sort(function (a, b) { return a[0] - b[0]; });
      list.forEach(function (t) { bal += t[2] - t[3]; tx.push({ y: y, m: m, d: t[0], desc: t[1], inn: t[2], out: t[3], bal: bal, cat: catOf(t[1], t[2] > 0) }); });
    }
    return tx;
  }

  /* ---------- hitung ---------- */
  var S = { src: '', tx: [], months: [], from: null, to: null, saldo: NaN, files: 0, ref: '' };
  function z(keys) { var o = {}; keys.forEach(function (k) { o[k] = 0; }); return o; }
  function aggregate() {
    var by = {}, tx = S.tx;
    tx.forEach(function (t) { var k = t.y * 12 + (t.m - 1); if (!by[k]) by[k] = { k: k, inn: z(KIN), out: z(KOUT), n: 0 }; if (t.inn) by[k].inn[t.cat in by[k].inn ? t.cat : 'jual'] += t.inn; if (t.out) by[k].out[t.cat in by[k].out ? t.cat : 'beli'] += t.out; by[k].n++; });
    var ks = Object.keys(by).map(Number).sort(function (a, b) { return a - b; });
    if (ks.length > 12) ks = ks.slice(ks.length - 12);
    S.months = ks.map(function (k) { return by[k]; });
    var keep = {}; ks.forEach(function (k) { keep[k] = 1; });
    var inRange = tx.filter(function (t) { return keep[t.y * 12 + (t.m - 1)]; });
    inRange.sort(function (a, b) { return dnum(a) - dnum(b); });
    S.from = inRange.length ? { y: inRange[0].y, m: inRange[0].m, d: inRange[0].d } : null;
    S.to = inRange.length ? { y: inRange[inRange.length - 1].y, m: inRange[inRange.length - 1].m, d: inRange[inRange.length - 1].d } : null;
    var lb = NaN; for (var i = inRange.length - 1; i >= 0; i--) if (isFinite(inRange[i].bal)) { lb = inRange[i].bal; break; }
    S.saldo = lb;
  }
  function pmt(p, ratePct, n) { if (!p || !n) return 0; var r = ratePct / 1200; return r ? p * r / (1 - Math.pow(1 + r, -n)) : p / n; }
  function pv(a, ratePct, n) { if (a <= 0 || !n) return 0; var r = ratePct / 1200; return r ? a * (1 - Math.pow(1 + r, -n)) / r : a * n; }
  function compute(D) {
    var T = { inn: z(KIN), out: z(KOUT) }, f = D.f, R = { T: T };
    D.months.forEach(function (m) { KIN.forEach(function (k) { T.inn[k] += m.inn[k] || 0; }); KOUT.forEach(function (k) { T.out[k] += m.out[k] || 0; }); });
    var days = D.days || D.months.length * 30.4, nm = Math.max(D.months.length, 1), af = nm >= 12 ? 1 : days >= 28 ? 365 / days : 12 / nm; if (af < 1) af = 1;
    R.days = days; R.nm = nm; R.af = af;
    var p = Math.min(Math.max(f.tunaiPct, 0), 100) / 100;
    R.pend = T.inn.jual; R.lain = T.inn.bunga;
    R.b = { beli: T.out.beli + T.out.tunai * (1 - p), gaji: T.out.gaji, sewa: T.out.sewa, util: T.out.util, pajak: T.out.pajak, bank: T.out.bank };
    R.beban = R.b.beli + R.b.gaji + R.b.sewa + R.b.util + R.b.pajak + R.b.bank;
    R.prive = T.out.prive + T.out.tunai * p;
    R.labaKas = R.pend + R.lain - R.beban;
    R.susut = f.umur > 0 ? f.aset / f.umur * (days / 365) : 0;
    R.bunga = f.ubank * (f.bungaLama / 100) * (days / 365); if (T.out.angs > 0) R.bunga = Math.min(R.bunga, T.out.angs);
    R.laba = R.labaKas - R.susut - R.bunga;
    R.pendTh = R.pend * af; R.labaTh = R.laba * af;
    R.kas = (isFinite(D.saldo) ? D.saldo : 0) + f.kas;
    R.aset = R.kas + f.piutang + f.sedia + f.aset;
    R.liab = f.uutang + f.ubank;
    R.ekuitas = R.aset - R.liab;
    R.angsLama = f.angs; R.angsBaru = pmt(f.ajukan, f.rate, f.tenor);
    R.kasBln = (R.labaKas - R.prive) * af / 12;
    var den = R.angsLama + R.angsBaru; R.dscr = den > 0 ? R.kasBln / den : null;
    R.der = R.ekuitas > 0 ? (R.liab + f.ajukan) / R.ekuitas : null;
    R.margin = R.pend > 0 ? R.laba / R.pend : 0;
    var full = D.months.map(function (m) { return m.inn.jual; });
    if (D.partial) { if (D.partial[0] && full.length > 3) full = full.slice(1); if (D.partial[1] && full.length > 3) full = full.slice(0, -1); }
    var mean = full.reduce(function (a, b) { return a + b; }, 0) / Math.max(full.length, 1), sd = Math.sqrt(full.reduce(function (a, b) { return a + (b - mean) * (b - mean); }, 0) / Math.max(full.length, 1));
    R.cv = mean > 0 ? sd / mean : 9;
    R.pisah = R.pend > 0 ? (T.out.tunai + T.out.prive) / R.pend : 1;
    var maxA = R.kasBln / 1.25 - R.angsLama; R.plafon = maxA > 0 ? Math.floor(pv(maxA, f.rate, f.tenor) / 1e6) * 1e6 : 0;
    /* skor */
    var I = [];
    var bl = nm, pt;
    if (D.src === 'manual') { pt = 5; I.push({ k: 'Lama dan sumber data', p: pt, max: 15, v: 'Isian sendiri', n: 'Angka diisi sendiri. Bank akan meminta mutasi rekening minimal 6 sampai 12 bulan sebagai bukti.' }); }
    else { pt = bl >= 12 ? 15 : bl >= 6 ? 10 : bl >= 3 ? 5 : 0; I.push({ k: 'Lama dan sumber data', p: pt, max: 15, v: bl + ' bulan mutasi', n: bl >= 12 ? 'Mutasi 12 bulan sudah cukup untuk dibaca analis.' : 'Lengkapi mutasi sampai 12 bulan supaya musim ramai dan sepi terlihat.' }); }
    pt = R.cv <= 0.25 ? 15 : R.cv <= 0.5 ? 10 : R.cv <= 0.8 ? 5 : 0;
    I.push({ k: 'Kestabilan omzet', p: pt, max: 15, v: 'Naik turun ' + Math.round(R.cv * 100) + '%', n: pt >= 10 ? 'Penerimaan bulanan cukup stabil.' : 'Penerimaan bulanan naik turun tajam. Siapkan penjelasan musim dan kontrak yang sedang berjalan.' });
    pt = R.margin >= 0.10 ? 15 : R.margin >= 0.05 ? 10 : R.margin > 0 ? 5 : 0;
    I.push({ k: 'Margin laba bersih', p: pt, max: 15, v: (R.margin * 100).toFixed(1).replace('.', ',') + '%', n: pt >= 10 ? 'Usaha menghasilkan laba yang cukup tebal.' : R.margin > 0 ? 'Laba tipis. Periksa lagi pos pembelian dan pengeluaran yang belum dikelompokkan.' : 'Usaha tercatat rugi pada periode ini. Periksa pengelompokan transaksi sebelum mengajukan.' });
    if (R.dscr == null) { pt = 15; I.push({ k: 'Kemampuan bayar angsuran', p: pt, max: 25, v: 'Belum ada angsuran', n: 'Isi rencana pinjaman supaya kemampuan bayar bisa dihitung.' }); }
    else { pt = R.dscr >= 1.5 ? 25 : R.dscr >= 1.25 ? 20 : R.dscr >= 1 ? 10 : 0; I.push({ k: 'Kemampuan bayar angsuran', p: pt, max: 25, v: R.dscr.toFixed(2).replace('.', ',') + ' kali', n: pt >= 20 ? 'Arus kas usaha menutup angsuran dengan ruang yang longgar.' : pt === 10 ? 'Arus kas hanya pas menutup angsuran. Pertimbangkan plafon lebih kecil atau tenor lebih panjang.' : 'Arus kas belum menutup angsuran. Turunkan plafon atau benahi pengeluaran dulu.' }); }
    if (R.der == null) { pt = 0; I.push({ k: 'Utang dibanding modal', p: pt, max: 15, v: R.aset > 0 ? 'Modal negatif' : 'Aset belum diisi', n: R.aset > 0 ? 'Aset lebih kecil dari utang. Lengkapi dulu daftar aset usaha Anda.' : 'Isi saldo rekening, persediaan, dan aset tetap supaya modal usaha bisa dihitung.' }); }
    else { pt = R.der <= 1 ? 15 : R.der <= 2 ? 10 : R.der <= 3 ? 5 : 0; I.push({ k: 'Utang dibanding modal', p: pt, max: 15, v: R.der.toFixed(2).replace('.', ',') + ' kali', n: pt >= 10 ? 'Porsi utang masih wajar dibanding modal sendiri.' : 'Utang sudah besar dibanding modal. Bank biasanya meminta agunan atau setoran modal tambahan.' }); }
    pt = R.pisah <= 0.10 ? 15 : R.pisah <= 0.25 ? 10 : R.pisah <= 0.40 ? 5 : 0;
    I.push({ k: 'Pemisahan uang usaha dan pribadi', p: pt, max: 15, v: Math.round(R.pisah * 100) + '% dari omzet', n: pt >= 10 ? 'Tarik tunai dan keperluan pribadi terkendali.' : 'Tarik tunai dan keperluan pribadi besar. Pisahkan rekening usaha dan pribadi mulai bulan ini.' });
    R.ind = I; R.skor = I.reduce(function (a, b) { return a + b.p; }, 0);
    R.label = R.skor >= 80 ? 'Kuat' : R.skor >= 60 ? 'Layak dengan Catatan' : R.skor >= 40 ? 'Perlu Dibenahi' : 'Belum Siap';
    return R;
  }

  /* ---------- kode data untuk link laporan ---------- */
  function b64e(s) { return btoa(unescape(encodeURIComponent(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
  function b64d(s) { s = s.replace(/-/g, '+').replace(/_/g, '/'); while (s.length % 4) s += '='; return decodeURIComponent(escape(atob(s))); }
  function pack(D) {
    var f = D.f, k = function (v) { return Math.round((v || 0) / 1000); };
    return b64e(JSON.stringify({ v: 1, s: D.src, n: D.nama, r: D.ref || '', d: Math.round(D.days), p: D.partial || [0, 0], fr: D.from ? [D.from.y, D.from.m, D.from.d] : 0, to: D.to ? [D.to.y, D.to.m, D.to.d] : 0, sa: isFinite(D.saldo) ? k(D.saldo) : null,
      m: D.months.map(function (m) { return [m.k].concat(KIN.map(function (c) { return k(m.inn[c]); }), KOUT.map(function (c) { return k(m.out[c]); })); }),
      f: [k(f.kas), k(f.piutang), k(f.sedia), k(f.aset), f.umur, k(f.uutang), k(f.ubank), k(f.angs), f.bungaLama, f.tunaiPct, k(f.ajukan), f.tenor, f.rate] }));
  }
  function unpack(code) {
    var o = JSON.parse(b64d(code)), a = o.f, K = 1000;
    return { src: o.s, nama: o.n, ref: o.r, days: o.d, partial: o.p, from: o.fr ? { y: o.fr[0], m: o.fr[1], d: o.fr[2] } : null, to: o.to ? { y: o.to[0], m: o.to[1], d: o.to[2] } : null, saldo: o.sa == null ? NaN : o.sa * K,
      months: o.m.map(function (r) { var mm = { k: r[0], inn: {}, out: {} }; KIN.forEach(function (c, i) { mm.inn[c] = r[1 + i] * K; }); KOUT.forEach(function (c, i) { mm.out[c] = r[1 + KIN.length + i] * K; }); return mm; }),
      f: { kas: a[0] * K, piutang: a[1] * K, sedia: a[2] * K, aset: a[3] * K, umur: a[4], uutang: a[5] * K, ubank: a[6] * K, angs: a[7] * K, bungaLama: a[8], tunaiPct: a[9], ajukan: a[10] * K, tenor: a[11], rate: a[12] } };
  }

  /* ---------- tampilan: tabel laporan ---------- */
  function periode(D) { return D.from && D.to ? dstr(D.from) + ' sampai ' + dstr(D.to) : D.months.length + ' bulan'; }
  function row(l, v, c) { return '<tr' + (c ? ' class="' + c + '"' : '') + '><td>' + l + '</td><td>' + (v === '' ? '' : tb(v)) + '</td></tr>'; }
  function tLR(R) {
    return '<table class="lsb-t"><tbody>' + row('Pendapatan usaha', R.pend) + (R.lain ? row('Bunga dan pendapatan lain', R.lain) : '') + row('Jumlah pendapatan', R.pend + R.lain, 'sum')
      + row('Pembelian dan beban operasional', -R.b.beli) + (R.b.gaji ? row('Gaji dan upah', -R.b.gaji) : '') + (R.b.sewa ? row('Sewa', -R.b.sewa) : '') + (R.b.util ? row('Listrik, air, internet', -R.b.util) : '') + (R.b.pajak ? row('Pajak dan iuran', -R.b.pajak) : '') + (R.b.bank ? row('Biaya bank', -R.b.bank) : '')
      + row('Laba usaha sebelum penyusutan dan bunga', R.labaKas, 'sum') + row('Penyusutan aset tetap', -R.susut) + row('Bunga pinjaman', -R.bunga) + row('Laba bersih', R.laba, 'tot') + '</tbody></table>';
  }
  function tPK(R, f) {
    return '<table class="lsb-t"><tbody><tr class="hd"><td colspan="2">Aset</td></tr>' + row('Kas dan bank', R.kas) + row('Piutang usaha', f.piutang) + row('Persediaan', f.sedia) + row('Aset tetap', f.aset) + row('Jumlah aset', R.aset, 'tot')
      + '<tr class="hd"><td colspan="2">Liabilitas dan Ekuitas</td></tr>' + row('Utang usaha', f.uutang) + row('Utang bank dan leasing', f.ubank) + row('Jumlah liabilitas', R.liab, 'sum') + row('Ekuitas pemilik', R.ekuitas) + row('Jumlah liabilitas dan ekuitas', R.aset, 'tot') + '</tbody></table>';
  }
  function chart(D) {
    var ms = D.months, W = 640, H = 200, pad = 28, n = ms.length, mx = 1, i;
    var a = ms.map(function (m) { var o = 0, k; for (k in m.out) if (k !== 'pindah') o += m.out[k]; return [m.inn.jual + m.inn.bunga, o]; });
    a.forEach(function (v) { mx = Math.max(mx, v[0], v[1]); });
    var bw = (W - pad * 2) / n, s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Grafik uang masuk dan keluar per bulan"><line x1="' + pad + '" x2="' + (W - pad) + '" y1="' + (H - 24) + '" y2="' + (H - 24) + '" class="ax"/>';
    for (i = 0; i < n; i++) {
      var x = pad + i * bw, h1 = (H - 44) * a[i][0] / mx, h2 = (H - 44) * a[i][1] / mx, w = Math.max(Math.min(bw * 0.34, 18), 3), mo = ms[i].k % 12;
      s += '<rect class="bi" x="' + (x + bw / 2 - w - 1).toFixed(1) + '" y="' + (H - 24 - h1).toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h1.toFixed(1) + '"/><rect class="bo" x="' + (x + bw / 2 + 1).toFixed(1) + '" y="' + (H - 24 - h2).toFixed(1) + '" width="' + w.toFixed(1) + '" height="' + h2.toFixed(1) + '"/><text x="' + (x + bw / 2).toFixed(1) + '" y="' + (H - 8) + '">' + BL3[mo] + '</text>';
    }
    return s + '</svg><p class="lsb-leg"><span class="i"></span>Uang masuk<span class="o"></span>Uang keluar</p>';
  }
  function ring(sk) {
    var c = 2 * Math.PI * 52, off = c * (1 - sk / 100);
    return '<svg class="lsb-ring" viewBox="0 0 120 120" role="img" aria-label="Skor ' + sk + ' dari 100"><circle cx="60" cy="60" r="52" class="bg"/><circle cx="60" cy="60" r="52" class="fg" stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '" transform="rotate(-90 60 60)"/><text x="60" y="66" class="n">' + sk + '</text><text x="60" y="84" class="s">dari 100</text></svg>';
  }

  /* ---------- langkah 1: sumber data ---------- */
  var elMsg = $('#lsb-msg'), elSum = $('#lsb-sum'), elForm = $('#lsb-form'), elRes = $('#lsb-res'), fileIn = $('#lsb-file');
  var lastRows = null, lastDet = null;
  function msg(t, bad) { elMsg.textContent = t || ''; elMsg.className = 'lsb-msg' + (bad ? ' bad' : ''); }
  function show(el, on) { el.hidden = !on; }
  function setMode(m) { $$('.lsb-tab').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-m') === m); b.setAttribute('aria-selected', b.getAttribute('data-m') === m ? 'true' : 'false'); }); $$('.lsb-pane').forEach(function (p) { p.hidden = p.getAttribute('data-p') !== m; }); }
  $$('.lsb-tab').forEach(function (b) { b.addEventListener('click', function () { var m = b.getAttribute('data-m'); setMode(m); if (m === 'contoh') startContoh(); if (m === 'manual') startManual(); }); });

  function afterTx(src) {
    S.src = src; aggregate();
    if (!S.months.length) { msg('Belum ada transaksi yang terbaca. Coba atur kolom di bawah, atau pakai tab Isi Angka Sendiri.', true); show(elSum, !!lastRows); renderMap(); return; }
    var first = S.months[0], lastM = S.months[S.months.length - 1];
    S.partial = [S.from && S.from.d > 7 ? 1 : 0, S.to && S.to.d < 22 ? 1 : 0];
    S.days = S.from && S.to ? dnum(S.to) - dnum(S.from) + 1 : S.months.length * 30.4;
    msg(''); renderSum(); show(elSum, true); prefill(); show(elForm, true); show(elRes, false);
    ev('lsb_data', { sumber: src, bulan: S.months.length });
  }
  function renderMap() {
    var box = $('#lsb-map'); if (!lastRows) { box.innerHTML = ''; return; }
    var n = 0; lastRows.slice(0, 80).forEach(function (r) { n = Math.max(n, r.length); });
    var hd = lastDet.hrow > -1 ? lastRows[lastDet.hrow] : [], opts = '<option value="-1">(tidak ada)</option>', j;
    for (j = 0; j < n; j++) opts += '<option value="' + j + '">Kolom ' + (j + 1) + (hd[j] ? ': ' + esc(String(hd[j]).slice(0, 22)) : '') + '</option>';
    var L = { date: 'Tanggal', desc: 'Keterangan', inn: 'Uang masuk (kredit)', out: 'Uang keluar (debit)', amt: 'Jumlah (satu kolom)', typ: 'Penanda DB/CR', bal: 'Saldo' }, h = '';
    Object.keys(L).forEach(function (k) { h += '<label>' + L[k] + '<select data-k="' + k + '">' + opts + '</select></label>'; });
    box.innerHTML = '<details' + (S.months.length ? '' : ' open') + '><summary>Atur kolom file (bila hasil baca belum pas)</summary><div class="lsb-mapg">' + h + '</div></details>';
    $$('select', box).forEach(function (s) { s.value = String(lastDet.map[s.getAttribute('data-k')]); s.addEventListener('change', function () { lastDet.map[s.getAttribute('data-k')] = +s.value; S.tx = parseRows(lastRows, lastDet.map, lastDet.hrow); afterTx('mutasi'); }); });
  }
  function renderSum() {
    var T = { inn: z(KIN), out: z(KOUT) };
    S.months.forEach(function (m) { KIN.forEach(function (k) { T.inn[k] += m.inn[k]; }); KOUT.forEach(function (k) { T.out[k] += m.out[k]; }); });
    var h = '<p class="lsb-ok"><b>' + (S.src === 'contoh' ? 'Data contoh (dummy) dimuat: ' : 'Terbaca: ') + S.tx.length + ' transaksi, ' + S.months.length + ' bulan</b> (' + (S.from ? dstr(S.from) + ' sampai ' + dstr(S.to) : '') + ').' + (S.tx.length && S.months.length > 12 ? '' : '') + '</p>';
    h += '<div class="lsb-two"><table class="lsb-t sm"><tbody><tr class="hd"><td colspan="2">Uang Masuk</td></tr>' + KIN.filter(function (k) { return T.inn[k]; }).map(function (k) { return row(CIN[k], T.inn[k]); }).join('') + '</tbody></table>';
    h += '<table class="lsb-t sm"><tbody><tr class="hd"><td colspan="2">Uang Keluar</td></tr>' + KOUT.filter(function (k) { return T.out[k]; }).map(function (k) { return row(COUT[k], T.out[k]); }).join('') + '</tbody></table></div>';
    /* transaksi terbesar: bisa dipindah kelompok */
    var keep = {}; S.months.forEach(function (m) { keep[m.k] = 1; });
    var inR = S.tx.filter(function (t) { return keep[t.y * 12 + t.m - 1]; });
    function grp(isIn) {
      var g = {}; inR.forEach(function (t, i) { var v = isIn ? t.inn : t.out; if (!v) return; var key = t.desc.toLowerCase().replace(/[0-9]+/g, '').replace(/\s+/g, ' ').trim().slice(0, 26) || '(tanpa keterangan)'; if (!g[key]) g[key] = { key: key, label: t.desc.replace(/\s*\d{3,}\s*$/, '') || '(tanpa keterangan)', sum: 0, n: 0, cat: t.cat }; g[key].sum += v; g[key].n++; });
      return Object.keys(g).map(function (k) { return g[k]; }).sort(function (a, b) { return b.sum - a.sum; }).slice(0, 7);
    }
    function list(isIn) {
      var names = isIn ? CIN : COUT, keys = isIn ? KIN : KOUT;
      return grp(isIn).map(function (g) { return '<tr><td>' + esc(g.label.slice(0, 44)) + '<small>' + g.n + ' transaksi</small></td><td>' + tb(g.sum) + '</td><td><select data-in="' + (isIn ? 1 : 0) + '" data-key="' + esc(g.key) + '">' + keys.map(function (k) { return '<option value="' + k + '"' + (k === g.cat ? ' selected' : '') + '>' + names[k] + '</option>'; }).join('') + '</select></td></tr>'; }).join('');
    }
    h += '<details class="lsb-fix"><summary>Periksa pengelompokan transaksi terbesar</summary><p>Mesin mengelompokkan dari kata di kolom keterangan. Betulkan bila ada yang keliru, misalnya transfer dari rekening sendiri yang terbaca sebagai penjualan.</p><div class="lsb-scroll"><table class="lsb-t sm fx"><tbody><tr class="hd"><td colspan="3">Masuk</td></tr>' + list(true) + '<tr class="hd"><td colspan="3">Keluar</td></tr>' + list(false) + '</tbody></table></div></details>';
    $('#lsb-sumbody').innerHTML = h;
    $$('select[data-key]', elSum).forEach(function (s) { s.addEventListener('change', function () { var isIn = s.getAttribute('data-in') === '1', key = s.getAttribute('data-key'); S.tx.forEach(function (t) { if ((isIn ? t.inn : t.out) && (t.desc.toLowerCase().replace(/[0-9]+/g, '').replace(/\s+/g, ' ').trim().slice(0, 26) || '(tanpa keterangan)') === key) t.cat = s.value; }); aggregate(); renderSum(); prefill(true); if (!elRes.hidden) hasil(); }); });
    renderMap();
  }
  function handleFiles(files) {
    if (!files || !files.length) return;
    msg('Membaca file...'); var all = [], rowsAll = [], det = null, i = 0, list = Array.prototype.slice.call(files);
    (function next() {
      if (i >= list.length) {
        if (!rowsAll.length) return;
        S.keep = false; lastRows = rowsAll; lastDet = det; S.files = list.length;
        var seen = {}; S.tx = all.filter(function (t) { var k = [t.y, t.m, t.d, t.desc, t.inn, t.out, isFinite(t.bal) ? t.bal : Math.random()].join('|'); if (seen[k]) return false; seen[k] = 1; return true; });
        afterTx('mutasi'); return;
      }
      readFile(list[i++]).then(function (rows) { var d = detect(rows); if (!det) { det = d; rowsAll = rows; } all = all.concat(parseRows(rows, d.map, d.hrow)); next(); }, function (e) { msg(e.message, true); });
    })();
  }
  fileIn.addEventListener('change', function () { handleFiles(fileIn.files); });
  var drop = $('#lsb-drop');
  ['dragenter', 'dragover'].forEach(function (n) { drop.addEventListener(n, function (e) { e.preventDefault(); drop.classList.add('over'); }); });
  ['dragleave', 'drop'].forEach(function (n) { drop.addEventListener(n, function (e) { e.preventDefault(); drop.classList.remove('over'); }); });
  drop.addEventListener('drop', function (e) { if (e.dataTransfer && e.dataTransfer.files) handleFiles(e.dataTransfer.files); });
  function startContoh() { S.keep = false; lastRows = null; S.tx = contoh(); afterTx('contoh'); var n = $('#lsb-nama'); if (!n.value) n.value = 'Toko Bangunan Contoh (data dummy)'; setv('sedia', 145e6); setv('piutang', 38e6); setv('aset', 310e6); setv('uutang', 52e6); setv('ubank', 96e6); setv('ajukan', 250e6); hasil(); }
  function startManual() { S.keep = false; lastRows = null; show(elSum, false); show(elForm, true); show(elRes, false); S.src = 'manual'; msg(''); $$('.lsb-only-mutasi').forEach(function (e) { e.hidden = true; }); }

  /* ---------- langkah 2: form ---------- */
  function fmtIn(el) { var n = num(el.value); el.value = isNaN(n) || !n ? '' : Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  $$('input[data-rp]').forEach(function (el) { el.addEventListener('blur', function () { fmtIn(el); }); el.addEventListener('focus', function () { el.select && el.select(); }); });
  function g(id) { var el = $('#lsb-' + id); if (!el) return 0; var n = num(el.value); return isNaN(n) ? 0 : n; }
  function setv(id, v, soft) { var el = $('#lsb-' + id); if (!el) return; if (soft && el.value && el.getAttribute('data-auto') !== '1') return; el.value = v ? Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') : ''; if (soft) el.setAttribute('data-auto', '1'); }
  $$('input[data-rp]').forEach(function (el) { el.addEventListener('input', function () { el.removeAttribute('data-auto'); }); });
  function prefill() {
    $$('.lsb-only-mutasi').forEach(function (e) { e.hidden = false; });
    var a = 0; S.months.forEach(function (m) { a += m.out.angs; });
    setv('angs', S.months.length ? Math.round(a / S.months.length / 1000) * 1000 : 0, true);
    setv('saldo', isFinite(S.saldo) ? S.saldo : 0, true);
  }
  function collect() {
    var D = { src: S.src, nama: ($('#lsb-nama').value || '').trim().slice(0, 60), ref: S.ref, f: { kas: g('kas'), piutang: g('piutang'), sedia: g('sedia'), aset: g('aset'), umur: g('umur') || 8, uutang: g('uutang'), ubank: g('ubank'), angs: g('angs'), bungaLama: g('bungalama') || 0, tunaiPct: +$('#lsb-tunai').value, ajukan: g('ajukan'), tenor: g('tenor') || 36, rate: g('rate') } };
    if (S.src === 'manual' && !S.keep) {
      var om = g('m-omzet'), lo = g('m-sepi') || om, hi = Math.max(2 * om - lo, om), base = { beli: g('m-beli'), gaji: g('m-gaji'), sewa: g('m-sewa'), util: 0, pajak: g('m-pajak'), bank: 0, angs: D.f.angs, tunai: 0, prive: g('m-prive'), pindah: 0 };
      var now = new Date(), k0 = now.getFullYear() * 12 + now.getMonth() - 12; D.months = [];
      for (var i = 0; i < 12; i++) { var o = {}; KOUT.forEach(function (k) { o[k] = base[k]; }); o.beli = base.beli * ([lo, om, hi][i % 3] / (om || 1)) + g('m-lain'); D.months.push({ k: k0 + i, inn: { jual: [lo, om, hi][i % 3], bunga: 0, pinjam: 0, pindah: 0 }, out: o }); }
      D.days = 365; D.partial = [0, 0]; D.from = null; D.to = null; D.saldo = g('saldo'); D.f.tunaiPct = 100;
    } else { D.months = S.months; D.days = S.days; D.partial = S.partial; D.from = S.from; D.to = S.to; D.saldo = g('saldo') || (isFinite(S.saldo) ? S.saldo : 0); }
    return D;
  }

  /* ---------- langkah 3: hasil ---------- */
  var CUR = null;
  function waLink(D, R) {
    var L = ['Halo Pak Ananta, saya sudah mencoba LK Siap Bank di cariakuntan.com dan ingin minta laporan keuangan lengkapnya.', '', 'Usaha: ' + (D.nama || '(belum diisi)'), 'Sumber data: ' + (D.src === 'manual' ? 'isian sendiri' : D.src === 'contoh' ? 'data contoh' : 'mutasi rekening ' + D.months.length + ' bulan'), 'Omzet setahun: ' + rp(R.pendTh, true), 'Skor Siap Bank: ' + R.skor + ' (' + R.label + ')'];
    if (D.f.ajukan) L.push('Rencana pinjaman: ' + rp(D.f.ajukan, true) + ', ' + D.f.tenor + ' bulan');
    if (D.ref) L.push('Dirujuk oleh: ' + D.ref);
    L.push('', 'Data ringkas: https://cariakuntan.com/lk-siap-bank/#lap=' + pack(D));
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(L.join('\n'));
  }
  function hasil(pre) {
    var D = pre && pre.months ? pre : collect();
    if (!D.months.length || !(D.months.reduce(function (a, m) { return a + m.inn.jual; }, 0) > 0)) { msg(S.src === 'manual' ? 'Isi dulu omzet rata-rata per bulan.' : 'Belum ada penerimaan usaha yang terbaca.', true); $('#lsb-msg').scrollIntoView({ block: 'center' }); return; }
    msg('');
    var R = compute(D), f = D.f; CUR = { D: D, R: R };
    var sah = R.pend > 0 && isFinite(R.laba);
    var tiles = [['Omzet Setahun', rp(R.pendTh, true), R.af > 1.02 ? 'disetahunkan dari ' + R.nm + ' bulan' : periodeS(D)], ['Laba Bersih Setahun', rp(R.labaTh, true), 'margin ' + (R.margin * 100).toFixed(1).replace('.', ',') + '%'], ['Kemampuan Bayar', R.dscr == null ? '-' : R.dscr.toFixed(2).replace('.', ',') + ' kali', R.dscr == null ? 'isi rencana pinjaman' : 'arus kas dibanding angsuran'], ['Plafon yang Masih Aman', rp(R.plafon, true), f.tenor + ' bulan, bunga ' + String(f.rate).replace('.', ',') + '%']];
    var notes = R.ind.filter(function (i) { return i.p < i.max * 0.6; }).map(function (i) { return '<li><b>' + i.k + '.</b> ' + i.n + '</li>'; });
    if (D.src !== 'manual' && R.T.out.tunai > 0.15 * R.pend) notes.push('<li><b>Tarik tunai.</b> Siapkan catatan pemakaian tarik tunai, karena analis tidak bisa membacanya dari mutasi.</li>');
    if (f.ajukan && R.plafon && f.ajukan > R.plafon * 1.05) notes.push('<li><b>Plafon.</b> Rencana pinjaman ' + rp(f.ajukan, true) + ' lebih besar dari plafon yang masih aman ' + rp(R.plafon, true) + '.</li>');
    if (!notes.length) notes.push('<li>Tidak ada catatan besar. Lengkapi dokumen legalitas dan siapkan penjelasan rencana pemakaian dana.</li>');
    var h = '<div class="lsb-rh"><div><p class="lsb-ey">Hasil</p><h2>' + esc(D.nama || 'Usaha Anda') + '</h2><p class="lsb-per">' + (D.src === 'manual' ? 'Berdasarkan angka isian sendiri, disetahunkan' : 'Periode ' + periode(D)) + (D.src === 'contoh' ? ' · data dummy untuk contoh' : '') + '</p></div></div>';
    h += '<div class="lsb-score"><div class="lsb-sc1">' + ring(R.skor) + '<p class="lsb-lab">Skor Siap Bank</p><p class="lsb-lv">' + R.label + '</p></div><div class="lsb-sc2">' + R.ind.map(function (i) { return '<div class="lsb-ind"><div><b>' + i.k + '</b><span>' + i.v + '</span></div><div class="lsb-bar"><i style="width:' + Math.round(i.p / i.max * 100) + '%"></i></div><em>' + i.p + '/' + i.max + '</em></div>'; }).join('') + '</div></div>';
    h += '<div class="lsb-tiles">' + tiles.map(function (t) { return '<div><span>' + t[0] + '</span><b>' + t[1] + '</b><small>' + t[2] + '</small></div>'; }).join('') + '</div>';
    if (D.src !== 'manual') h += '<div class="lsb-card"><h3>Uang Masuk dan Keluar per Bulan</h3>' + chart(D) + '</div>';
    h += '<div class="lsb-two"><div class="lsb-card"><h3>Laba Rugi</h3><p class="lsb-cap">' + (D.src === 'manual' ? '12 bulan, dari angka isian' : periode(D)) + ', dalam rupiah</p>' + tLR(R) + '</div><div class="lsb-card"><h3>Posisi Keuangan</h3><p class="lsb-cap">Per ' + (D.to ? dstr(D.to) : 'hari ini') + ', dalam rupiah</p>' + tPK(R, f) + '</div></div>';
    h += '<div class="lsb-card"><h3>Yang Perlu Dibenahi Sebelum ke Bank</h3><ul class="lsb-notes">' + notes.join('') + '</ul><p class="lsb-fine">Skor ini indikasi awal dari data yang Anda masukkan, disusun dari cara analis kredit membaca usaha. Keputusan dan kebijakan tiap bank berbeda. Ruang aman dihitung dengan arus kas 1,25 kali angsuran.</p></div>';
    h += '<div class="lsb-cta"><div><h3>Butuh Laporan Lengkap untuk Diserahkan ke Bank?</h3><p>Laba rugi, posisi keuangan, dan catatan atas laporan keuangan dalam format SAK EMKM, dirapikan tim dari data ini. Kirim hasilnya lewat WhatsApp, kami lanjutkan dari sana.</p></div><div class="lsb-btns"><a class="btn btn-wa arrow" id="lsb-wa" rel="noopener" target="_blank" href="' + waLink(D, R) + '">Minta LK Lengkap via WhatsApp</a><button type="button" class="btn btn-line" id="lsb-edit">Ubah Angka</button></div></div>';
    elRes.innerHTML = h; show(elRes, true);
    $('#lsb-edit').addEventListener('click', function () { elForm.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
    $('#lsb-wa').addEventListener('click', function () { ev('lsb_wa', { skor: R.skor, sumber: D.src }); });
    var up = $('#lsb-up'); if (up) up.hidden = false;
    elRes.scrollIntoView({ behavior: 'smooth', block: 'start' });
    ev('lsb_hasil', { skor: R.skor, sumber: D.src });
  }
  function periodeS(D) { return D.from && D.to ? BL3[D.from.m - 1] + ' ' + D.from.y + ' sampai ' + BL3[D.to.m - 1] + ' ' + D.to.y : '12 bulan'; }
  $('#lsb-go').addEventListener('click', function () { hasil(); });

  /* ---------- mode laporan (dibuka tim dari link di WhatsApp) ---------- */
  function laporan(code) {
    var D; try { D = unpack(code); } catch (e) { return false; }
    var R = compute(D), f = D.f, per = D.src === 'manual' ? 'Untuk periode 12 bulan (angka isian pemilik)' : 'Untuk periode ' + periode(D), T = R.T;
    var doc = document.createElement('div'); doc.className = 'lsb-doc'; doc.id = 'lsb-doc';
    var h = '<div class="lsb-docbar"><button type="button" class="btn btn-wa" id="lsb-print">Cetak atau Simpan PDF</button><button type="button" class="btn btn-line" id="lsb-ce">Edit Teks</button><span>Mode laporan untuk tim. Periksa pengelompokan sebelum dikirim ke klien.</span></div>';
    h += '<article class="lsb-paper"><header><p class="k">Laporan Keuangan</p><h1>' + esc(D.nama || 'Nama Usaha') + '</h1><p>' + per + '</p><p class="k2">Disusun dari mutasi rekening dan data pemilik usaha, mengacu pada format SAK EMKM. Belum diaudit.</p></header>';
    h += '<section><h2>Laporan Laba Rugi</h2><p class="cap">' + per + ' · dalam rupiah</p>' + tLR(R) + '</section>';
    h += '<section><h2>Laporan Posisi Keuangan</h2><p class="cap">Per ' + (D.to ? dstr(D.to) : 'tanggal laporan') + ' · dalam rupiah</p>' + tPK(R, f) + '</section>';
    h += '<section class="brk"><h2>Catatan atas Laporan Keuangan</h2><h3>1. Umum</h3><p>' + esc(D.nama || 'Usaha ini') + ' adalah usaha milik perorangan atau badan usaha yang kegiatan dan alamat lengkapnya dilengkapi oleh pemilik.</p>'
      + '<h3>2. Dasar Penyusunan</h3><p>Laporan keuangan ini disusun dengan mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM). Pendapatan dan beban diambil dari mutasi rekening bank pada periode laporan, lalu disesuaikan dengan saldo piutang, persediaan, aset tetap, dan utang yang disampaikan pemilik. Ekuitas pemilik disajikan sebagai selisih antara aset dan liabilitas.</p>'
      + '<h3>3. Kas dan Bank</h3><table class="lsb-t"><tbody>' + row('Saldo rekening bank', isFinite(D.saldo) ? D.saldo : 0) + row('Kas tunai', f.kas) + row('Jumlah', R.kas, 'tot') + '</tbody></table>'
      + '<h3>4. Aset Tetap</h3><p>Aset tetap dicatat sebesar ' + rp(f.aset) + ' dan disusutkan dengan metode garis lurus selama ' + f.umur + ' tahun. Beban penyusutan periode ini ' + rp(R.susut) + '.</p>'
      + '<h3>5. Utang Bank dan Leasing</h3><p>Sisa pokok pinjaman ' + rp(f.ubank) + ' dengan angsuran sekitar ' + rp(f.angs) + ' per bulan. Bunga yang dibebankan pada periode ini ' + rp(R.bunga) + (f.bungaLama ? ' (perkiraan ' + String(f.bungaLama).replace('.', ',') + '% per tahun dari sisa pokok).' : '.') + '</p>'
      + '<h3>6. Rincian Uang Keluar yang Tidak Masuk Beban Usaha</h3><table class="lsb-t"><tbody>' + row('Angsuran pinjaman', T.out.angs) + row('Tarik tunai untuk keperluan pribadi (' + f.tunaiPct + '%)', T.out.tunai * f.tunaiPct / 100) + row('Keperluan pribadi lain', T.out.prive) + row('Pindah buku ke rekening sendiri', T.out.pindah) + '</tbody></table>'
      + '<h3>7. Penerimaan di Luar Pendapatan Usaha</h3><table class="lsb-t"><tbody>' + row('Pencairan pinjaman', T.inn.pinjam) + row('Pindah buku atau setoran pemilik', T.inn.pindah) + '</tbody></table></section>';
    h += '<section class="brk"><h2>Lampiran: Analisis Kesiapan Kredit</h2><p class="cap">Skor Siap Bank ' + R.skor + ' dari 100 (' + R.label + ')' + (f.ajukan ? ' · rencana pinjaman ' + rp(f.ajukan) + ', ' + f.tenor + ' bulan, bunga ' + String(f.rate).replace('.', ',') + '% per tahun' : '') + '</p><table class="lsb-t ind"><tbody><tr class="hd"><td>Indikator</td><td>Hasil</td><td>Nilai</td></tr>' + R.ind.map(function (i) { return '<tr><td><b>' + i.k + '</b><br>' + i.n + '</td><td>' + i.v + '</td><td>' + i.p + '/' + i.max + '</td></tr>'; }).join('') + '</tbody></table>'
      + '<table class="lsb-t"><tbody>' + row('Omzet setahun (disetahunkan)', R.pendTh) + row('Laba bersih setahun (disetahunkan)', R.labaTh) + row('Arus kas tersedia untuk angsuran per bulan', R.kasBln) + row('Angsuran berjalan per bulan', R.angsLama) + row('Angsuran pinjaman baru per bulan', R.angsBaru) + row('Plafon yang masih aman', R.plafon, 'tot') + '</tbody></table>'
      + (D.src !== 'manual' ? '<div class="lsb-card">' + chart(D) + '</div>' : '') + '</section>';
    h += '<footer><p>Disiapkan melalui LK Siap Bank, cariakuntan.com' + (D.ref ? ' · rujukan: ' + esc(D.ref) : '') + '</p></footer></article>';
    doc.innerHTML = h;
    var main = root.closest('main') || document.body; main.innerHTML = ''; main.appendChild(doc); document.body.classList.add('lsb-lapmode');
    doc.querySelector('#lsb-print').addEventListener('click', function () { window.print(); });
    doc.querySelector('#lsb-ce').addEventListener('click', function () { var p = doc.querySelector('.lsb-paper'), on = p.getAttribute('contenteditable') === 'true'; p.setAttribute('contenteditable', on ? 'false' : 'true'); this.textContent = on ? 'Edit Teks' : 'Selesai Edit'; });
    window.scrollTo(0, 0);
    return true;
  }

  /* ---------- mulai ---------- */
  try { var q = new URLSearchParams(location.search), rf = q.get('ref'); if (rf) { rf = rf.replace(/[^\w .&-]/g, '').slice(0, 40); sessionStorage.setItem('lsb_ref', rf); } S.ref = sessionStorage.getItem('lsb_ref') || ''; } catch (e) {}
  var TIM = '1947b5cc48a42d838980e1cd8b419c212a4c70ab2890b7161feb9a9304c57ffc';
  function sha(t) { return crypto.subtle.digest('SHA-256', new TextEncoder().encode(t)).then(function (b) { return Array.prototype.map.call(new Uint8Array(b), function (x) { return ('0' + x.toString(16)).slice(-2); }).join(''); }); }
  function pulih(code) {
    var D; try { D = unpack(code); } catch (e) { return; }
    if (!D.months || !D.months.length) return;
    S.keep = true; S.src = D.src; S.months = D.months; S.days = D.days; S.partial = D.partial; S.from = D.from; S.to = D.to; S.saldo = D.saldo; if (D.ref) S.ref = D.ref;
    var f = D.f; $('#lsb-nama').value = D.nama || '';
    ['kas', 'piutang', 'sedia', 'aset', 'uutang', 'ubank', 'angs', 'ajukan'].forEach(function (k) { setv(k, f[k]); }); setv('saldo', isFinite(D.saldo) ? D.saldo : 0);
    $('#lsb-umur').value = f.umur; $('#lsb-bungalama').value = f.bungaLama; $('#lsb-tenor').value = f.tenor; $('#lsb-rate').value = f.rate; $('#lsb-tunai').value = String(f.tunaiPct);
    show(elForm, true); hasil(D);
    var bar = document.createElement('p'); bar.className = 'lsb-tim';
    bar.innerHTML = '<button type="button">Akses tim penyusun</button>'; elRes.appendChild(bar);
    function buka() { laporan(code); }
    var saved = ''; try { saved = localStorage.getItem('lsb_tim') || ''; } catch (e) {}
    if (saved === TIM) { bar.firstChild.textContent = 'Buka mode laporan (tim)'; }
    bar.firstChild.addEventListener('click', function () {
      if (saved === TIM) return buka();
      var k = window.prompt('Kode tim penyusun:'); if (!k || !window.crypto || !crypto.subtle) return;
      sha(k.trim()).then(function (hx) { if (hx === TIM) { try { localStorage.setItem('lsb_tim', TIM); } catch (e) {} buka(); } else window.alert('Kode tidak cocok.'); });
    });
  }
  if (S.ref) { var rb = $('#lsb-refnote'); if (rb) { rb.textContent = 'Anda dirujuk oleh ' + S.ref + '. Nama perujuk ikut tercantum saat Anda mengirim hasil.'; rb.hidden = false; } }
  /* pembuat link untuk RM bank */
  var rn = document.getElementById('lsb-rmname'), ro = document.getElementById('lsb-rmlink'), rc = document.getElementById('lsb-rmcopy');
  if (rn && ro) {
    var mk = function () { var v = rn.value.replace(/[^\w .&-]/g, '').trim().slice(0, 40); ro.value = 'https://cariakuntan.com/lk-siap-bank/' + (v ? '?ref=' + encodeURIComponent(v).replace(/%20/g, '+') : ''); };
    rn.addEventListener('input', mk); mk();
    rc.addEventListener('click', function () { ro.select(); try { navigator.clipboard.writeText(ro.value); } catch (e) { try { document.execCommand('copy'); } catch (e2) {} } rc.textContent = 'Tersalin'; setTimeout(function () { rc.textContent = 'Salin Link'; }, 1600); ev('lsb_rm_link'); });
  }
  var hm = /[#&]lap=([A-Za-z0-9_-]+)/.exec(location.hash);
  if (hm) pulih(hm[1]);
  else if (/[?&]contoh=1/.test(location.search)) { setMode('contoh'); startContoh(); }
  window.LSB = { num: num, pdate: pdate, csvRows: csvRows, detect: detect, parseRows: parseRows, compute: compute, pack: pack, unpack: unpack, catOf: catOf };
})();
