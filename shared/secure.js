/* Lencana keamanan data (FA Secure / CariAkuntan Secure / UpdateSAK Secure), 27 Okt 2026.
   Dipasang prep.py (add_secure) pada alat yang meminta data perusahaan.
   Konfigurasi: window.FA_SECURE = {brand:'fa'|'ca'|'us', mode:'local'|'drive'|'send', theme:'dark'|'light',
                                    at:[{sel:'css', pos:'beforebegin'|'afterbegin'|'afterend'|'beforeend'}]}
   Klaim harus selalu benar terhadap kode halaman:
   local = tidak ada data yang dikirim; drive = disimpan ke Google Drive pengguna sendiri;
   send  = dihitung di browser, hasil hanya terkirim saat pengguna klik Kirim. */
(function () {
  var C = window.FA_SECURE || {};
  var B = { fa: ['FA Secure', 'FA Indonesia'], ca: ['CariAkuntan Secure', 'CariAkuntan'], us: ['UpdateSAK Secure', 'UpdateSAK'] }[C.brand || 'fa'];
  var L = (document.documentElement.lang || 'id').toLowerCase();
  L = L.indexOf('en') === 0 ? 'en' : (L.indexOf('zh') === 0 || L === 'nan') ? 'zh' : 'id';
  var O = B[1], M = C.mode || 'local';
  var T = {
    id: {
      local: 'Diproses di browser Anda. Data perusahaan tidak dikirim ke server dan tidak disimpan oleh ' + O + '.',
      drive: 'Diproses di browser Anda. Kalau disimpan, file masuk ke Google Drive Anda sendiri, bukan ke server ' + O + '.',
      send: 'Angka keuangan dihitung di browser Anda dan tidak disimpan di server ' + O + '. Hasil hanya terkirim ke tim kami kalau Anda klik Kirim.',
      more: 'Detail', less: 'Tutup',
      b: ['Koneksi terenkripsi HTTPS.', 'Tanpa akun dan tanpa database data keuangan di sisi kami.',
          C.brand === 'fa' ? 'Tim CA dan CPA terikat kode etik kerahasiaan profesi.' : C.brand === 'ca' ? 'Kalau berlanjut, data dilindungi NDA sebelum dibahas.' : 'Tidak perlu login, tidak ada data yang dikumpulkan dari kalkulator.']
    },
    en: {
      local: 'Processed in your browser. Company data is never sent to or stored on ' + O + ' servers.',
      drive: 'Processed in your browser. If you save, files go to your own Google Drive, not to ' + O + ' servers.',
      send: 'Figures are calculated in your browser and not stored on ' + O + ' servers. Results reach our team only if you click Send.',
      more: 'Details', less: 'Close',
      b: ['Encrypted HTTPS connection.', 'No account and no financial-data database on our side.',
          C.brand === 'ca' ? 'If you proceed, your data is covered by an NDA before review.' : 'CA and CPA team bound by professional confidentiality.']
    },
    zh: {
      local: '在您的浏览器中处理。公司数据不会发送到 ' + O + ' 服务器，也不会被保存。',
      drive: '在您的浏览器中处理。如需保存，文件存入您自己的 Google Drive，而不是 ' + O + ' 服务器。',
      send: '财务数字在您的浏览器中计算，不保存在 ' + O + ' 服务器。只有您点击发送后，结果才会发给我们的团队。',
      more: '详情', less: '关闭',
      b: ['HTTPS 加密连接。', '无需账户，我们不建立财务数据库。',
          C.brand === 'ca' ? '如继续合作，资料在审阅前受保密协议 (NDA) 保护。' : 'CA 与 CPA 团队受职业保密准则约束。']
    }
  }[L];
  var dark = C.theme !== 'light';
  var css = '.faSec{all:initial;box-sizing:border-box;display:flex;gap:12px;align-items:flex-start;max-width:100%;margin:12px 0;padding:11px 14px;border-radius:10px;font:400 13px/1.55 Poppins,Inter,system-ui,sans-serif;' +
    (dark ? 'background:rgba(127,209,166,.08);border:1px solid rgba(127,209,166,.35);color:#d9efe3' : 'background:#effaf4;border:1px solid #b7e4cb;color:#1d4733') + '}' +
    '.faSec *{box-sizing:border-box}.faSec svg{flex:none;width:30px;height:34px;margin-top:1px}.faSec .t{min-width:0;flex:1}' +
    '.faSec b{display:inline-block;font-weight:600;letter-spacing:.02em;margin-right:6px;color:' + (dark ? '#7fd1a6' : '#137a46') + '}' +
    '.faSec button{all:unset;cursor:pointer;font-weight:500;text-decoration:underline;margin-left:4px;color:inherit}' +
    '.faSec ul{margin:6px 0 0;padding-left:18px}.faSec li{margin:2px 0}.faSec ul[hidden]{display:none}' +
    '.faSec.bar{margin:0;border-radius:0;border-left:0;border-right:0;padding:8px 16px;justify-content:center}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var ic = '<svg viewBox="0 0 30 34" aria-hidden="true"><path d="M15 1 2 6v9c0 8.3 5.6 15.4 13 18 7.4-2.6 13-9.7 13-18V6L15 1z" fill="' + (dark ? 'rgba(127,209,166,.18)' : '#d6f2e2') + '" stroke="' + (dark ? '#7fd1a6' : '#137a46') + '" stroke-width="1.6"/><path d="M10 17.5l3.6 3.6L20.5 13" fill="none" stroke="' + (dark ? '#7fd1a6' : '#137a46') + '" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function make(extra) {
    var d = document.createElement('div'); d.className = 'faSec' + (extra ? ' ' + extra : ''); d.setAttribute('role', 'note');
    d.innerHTML = ic + '<div class="t"><b>' + B[0] + '</b>' + T[M] + '<button type="button">' + T.more + '</button><ul hidden>' + T.b.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul></div>';
    var bt = d.querySelector('button'), ul = d.querySelector('ul');
    bt.onclick = function () { ul.hidden = !ul.hidden; bt.textContent = ul.hidden ? T.more : T.less; };
    return d;
  }
  function run() {
    (C.at || []).forEach(function (a) {
      var el = document.querySelector(a.sel); if (!el || el.getAttribute('data-fasec')) return;
      el.setAttribute('data-fasec', '1'); el.insertAdjacentElement(a.pos || 'beforebegin', make(a.cls));
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
