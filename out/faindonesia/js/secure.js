/* Segel keamanan data (FA Secure / CariAkuntan Secure / UpdateSAK Secure), 28 Okt 2026.
   Tampil seperti segel software pihak ketiga yang ditempel: kartu putih tetap (tidak ikut tema situs),
   font sistem + monospace (beda dari font situs), emblem perisai, status "Aktif", baris spesifikasi teknis.
   Dipasang prep.py (add_secure). Konfigurasi:
     window.FA_SECURE = {brand:'fa'|'ca'|'us', mode:'local'|'drive'|'send', at:[{sel:'css', pos:'beforebegin'|'afterbegin'|'afterend'|'beforeend', cls:'bar'}]}
   Klaim harus selalu benar terhadap kode halaman:
     local = tidak ada data yang dikirim; drive = disimpan ke Google Drive pengguna; send = dihitung di browser, terkirim hanya saat klik Kirim. */
(function () {
  var C = window.FA_SECURE || {};
  var BR = {
    fa: { name: 'FA', full: 'FA Indonesia', c1: '#1a1a1a', c2: '#3a3a3a', acc: '#16a34a' },
    ca: { name: 'CariAkuntan', full: 'CariAkuntan', c1: '#0f2e8a', c2: '#1F5BFF', acc: '#16a34a' },
    us: { name: 'UpdateSAK', full: 'UpdateSAK', c1: '#0B1F33', c2: '#1F5BFF', acc: '#16a34a' }
  }[C.brand || 'fa'];
  var M = C.mode || 'local';
  var L = (document.documentElement.lang || 'id').toLowerCase();
  L = L.indexOf('en') === 0 ? 'en' : (L.indexOf('zh') === 0 || L === 'nan') ? 'zh' : 'id';
  var O = BR.full;
  var T = {
    id: {
      on: 'Aktif', h: { local: 'Data Diproses di Perangkat Anda', drive: 'Data Tersimpan di Drive Anda Sendiri', send: 'Angka Keuangan Tetap di Perangkat Anda' },
      s: {
        local: 'Perhitungan berjalan di browser. Data perusahaan tidak dikirim ke server dan tidak disimpan oleh ' + O + '.',
        drive: 'Perhitungan berjalan di browser. Kalau disimpan, file masuk ke Google Drive Anda, bukan ke server ' + O + '.',
        send: 'Dihitung di browser dan tidak disimpan di server ' + O + '. Hasil hanya terkirim ke tim kami kalau Anda klik Kirim.'
      },
      spec: { local: ['HTTPS Terenkripsi', 'Proses di Browser', 'Tanpa Database', 'Tanpa Login'],
              drive: ['HTTPS Terenkripsi', 'Proses di Browser', 'Google Drive Milik Anda', 'Tanpa Database'],
              send: ['HTTPS Terenkripsi', 'Proses di Browser', 'Kirim Hanya Atas Izin Anda', 'Tanpa Database'] },
      more: 'Detail', less: 'Tutup',
      d: [C.brand === 'ca' ? 'Kalau berlanjut, data dilindungi NDA sebelum dibahas.' : C.brand === 'us' ? 'Kalkulator tidak mengumpulkan data apa pun dan tidak perlu akun.' : 'Tim CA dan CPA terikat kode etik kerahasiaan profesi.',
          'Hapus data kapan saja dengan menutup tab atau membersihkan data browser.',
          'Pertanyaan soal data: office@faindonesia.co.id.']
    },
    en: {
      on: 'Active', h: { local: 'Data Processed on Your Device', drive: 'Data Saved to Your Own Drive', send: 'Financial Figures Stay on Your Device' },
      s: {
        local: 'Calculations run in your browser. Company data is never sent to or stored by ' + O + '.',
        drive: 'Calculations run in your browser. If you save, files go to your own Google Drive, not to ' + O + ' servers.',
        send: 'Calculated in your browser and not stored on ' + O + ' servers. Results reach our team only if you click Send.'
      },
      spec: { local: ['HTTPS Encrypted', 'In-Browser Processing', 'No Database', 'No Login'],
              drive: ['HTTPS Encrypted', 'In-Browser Processing', 'Your Own Google Drive', 'No Database'],
              send: ['HTTPS Encrypted', 'In-Browser Processing', 'Sent Only With Your Consent', 'No Database'] },
      more: 'Details', less: 'Close',
      d: [C.brand === 'ca' ? 'If you proceed, your data is covered by an NDA before review.' : 'CA and CPA team bound by professional confidentiality.',
          'Clear your data anytime by closing the tab or clearing browser data.', 'Data questions: office@faindonesia.co.id.']
    },
    zh: {
      on: '已启用', h: { local: '数据在您的设备上处理', drive: '数据保存在您自己的云端硬盘', send: '财务数字保留在您的设备上' },
      s: {
        local: '计算在您的浏览器中进行。公司数据不会发送到 ' + O + '，也不会被保存。',
        drive: '计算在您的浏览器中进行。如需保存，文件存入您自己的 Google Drive，而不是 ' + O + ' 服务器。',
        send: '在浏览器中计算，不保存在 ' + O + ' 服务器。只有您点击发送后，结果才会发给我们的团队。'
      },
      spec: { local: ['HTTPS 加密', '浏览器内处理', '无数据库', '无需登录'],
              drive: ['HTTPS 加密', '浏览器内处理', '您自己的 Google Drive', '无数据库'],
              send: ['HTTPS 加密', '浏览器内处理', '经您同意才发送', '无数据库'] },
      more: '安全详情', less: '关闭',
      d: [C.brand === 'ca' ? '如继续合作，资料在审阅前受保密协议 (NDA) 保护。' : 'CA 与 CPA 团队受职业保密准则约束。',
          '关闭页面或清除浏览器数据即可删除数据。', '数据相关问题：office@faindonesia.co.id。']
    }
  }[L];

  var SYS = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
  var MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace';
  var css =
    '.faSeal{all:initial;box-sizing:border-box;display:block;width:100%;max-width:560px;margin:10px 0;font-family:' + SYS + ';-webkit-font-smoothing:antialiased}' +
    '.faSeal *{box-sizing:border-box;font-family:inherit;margin:0;padding:0;letter-spacing:normal;text-transform:none}' +
    '.faSeal .cd{display:flex;align-items:stretch;background:#fff;color:#1f2328;border:1px solid #d0d7de;border-radius:8px;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.06),0 6px 18px rgba(0,0,0,.08)}' +
    '.faSeal .em{flex:none;width:40px;display:flex;align-items:center;justify-content:center;padding:6px;color:#fff;background:linear-gradient(160deg,' + BR.c2 + ',' + BR.c1 + ')}' +
    '.faSeal .em svg{width:18px;height:21px;display:block}.faSeal .em i{display:none!important}' +
    '.faSeal .em i{font-style:normal;font:700 8.5px/1.15 ' + MONO + ';letter-spacing:.12em;text-align:center;text-transform:uppercase}' +
    '.faSeal .em i b{display:block;font-weight:700;letter-spacing:.08em;font-size:9.5px;max-width:78px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}' +
    '.faSeal .bd{min-width:0;flex:1;padding:7px 12px}' +
    '.faSeal .tp{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.faSeal .x{margin-top:6px;padding-top:6px;border-top:1px dashed #e4e7ec}.faSeal .x[hidden]{display:none}.faSeal .x .sp{border:0;margin-top:5px;padding-top:0}' +
    '.faSeal .h{font:600 12.5px/1.3 ' + SYS + ';color:#1f2328}' +
    '.faSeal .st{display:inline-flex;align-items:center;gap:5px;font:600 10px/1 ' + MONO + ';letter-spacing:.06em;text-transform:uppercase;color:' + BR.acc + ';background:#ecfdf3;border:1px solid #abefc6;border-radius:999px;padding:3px 7px}' +
    '.faSeal .st:before{content:"";width:6px;height:6px;border-radius:50%;background:' + BR.acc + ';box-shadow:0 0 0 3px rgba(22,163,74,.18)}' +
    '.faSeal .s{font:400 12.5px/1.5 ' + SYS + ';color:#475467}' +
    '.faSeal .sp{display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:7px;padding-top:7px;border-top:1px dashed #e4e7ec}' +
    '.faSeal .sp span{display:inline-flex;align-items:center;gap:4px;font:500 10.5px/1.4 ' + MONO + ';color:#344054}' +
    '.faSeal .sp span:before{content:"";width:10px;height:10px;flex:none;background:no-repeat center/10px url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3E%3Cpath d=%27M3 8.5l3 3 7-7%27 fill=%27none%27 stroke=%27%2316a34a%27 stroke-width=%272.4%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27/%3E%3C/svg%3E")}' +
    '.faSeal button{all:unset;cursor:pointer;font:500 11px/1.4 ' + SYS + ';color:#475467;text-decoration:underline;text-underline-offset:2px;margin-left:auto}' +
    '.faSeal button:hover{color:#1f2328}' +
    '.faSeal ul{list-style:disc;margin:6px 0 0 16px;font:400 12px/1.5 ' + SYS + ';color:#475467}.faSeal ul[hidden]{display:none}' +
    '.faSeal.bar{max-width:none;margin:0;padding:10px 16px;background:transparent}.faSeal.bar .cd{max-width:640px;margin:0 auto}' +
    '@media (max-width:520px){.faSeal .h{font-size:12px}.faSeal .s{font-size:12px}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var shield = '<svg viewBox="0 0 30 34" aria-hidden="true"><path d="M15 1.5 3 6v8.6c0 7.7 5.1 14.3 12 17 6.9-2.7 12-9.3 12-17V6L15 1.5z" fill="rgba(255,255,255,.14)" stroke="#fff" stroke-width="1.6"/>' +
    '<rect x="10" y="14.5" width="10" height="8" rx="1.4" fill="#fff"/><path d="M12 14.5v-2.2a3 3 0 0 1 6 0v2.2" fill="none" stroke="#fff" stroke-width="1.7"/><circle cx="15" cy="18.5" r="1.2" fill="' + BR.c1 + '"/></svg>';

  function make(extra) {
    var w = document.createElement('div'); w.className = 'faSeal' + (extra ? ' ' + extra : ''); w.setAttribute('role', 'note');
    w.setAttribute('aria-label', BR.name + ' Secure');
    w.innerHTML = '<div class="cd"><div class="em">' + shield + '<i><b>' + BR.name + '</b>Secure</i></div>' +
      '<div class="bd"><div class="tp"><span class="h">' + BR.name + ' Secure</span><span class="st">' + T.on + '</span><button type="button">' + T.more + '</button></div>' +
      '<div class="x" hidden><p class="s"><b style="color:#1f2328;font-weight:600">' + T.h[M] + '.</b> ' + T.s[M] + '</p>' +
      '<div class="sp">' + T.spec[M].map(function (x) { return '<span>' + x + '</span>'; }).join('') + '</div>' +
      '<ul>' + T.d.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul></div></div></div>';
    var bt = w.querySelector('button'), ul = w.querySelector('.x');
    bt.onclick = function () { ul.hidden = !ul.hidden; bt.textContent = ul.hidden ? T.more : T.less; };
    return w;
  }
  function run() {
    (C.at || []).forEach(function (a) {
      var el = document.querySelector(a.sel); if (!el || el.getAttribute('data-fasec')) return;
      el.setAttribute('data-fasec', '1'); el.insertAdjacentElement(a.pos || 'beforebegin', make(a.cls));
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
