/* QRIS donasi sukarela untuk layanan gratis FA Indonesia & CariAkuntan.
   Konfigurasi: window.FA_DONASI = {accent:'#fff', guards:[{sel:'css selector', key:'nama', skip:function(){return false}}]}
   Alur: klik tombol hasil -> popup QRIS (Sudah Donasi / Lewati) -> hasil muncul -> pill "Tampilkan QRIS" tetap ada. */
(function () {
  var C = window.FA_DONASI || {};
  var IMG = C.img || '/img/qris-fa-indonesia.jpg';
  var ACC = C.accent || '#ffffff';
  var ACC_INK = C.accentInk || '#171717';
  var L = (document.documentElement.lang || 'id').toLowerCase();
  L = L.indexOf('en') === 0 ? 'en' : (L.indexOf('zh') === 0 || L === 'nan') ? 'zh' : 'id';
  var T = {
    id: { t: 'Layanan ini gratis', s: 'Kalau bermanfaat, Anda bisa berdonasi lewat QRIS sebesar <b>Rp19.001</b>. Sepenuhnya opsional, boleh dilewati.',
          done: 'Sudah Donasi, Lanjutkan', skip: 'Lewati, Lanjutkan', save: 'Simpan Gambar QRIS', thanks: 'Terima kasih',
          s2: 'Scan QRIS dengan aplikasi bank atau e-wallet apa saja, lalu isi nominal <b>Rp19.001</b>.', close: 'Tutup',
          pill: 'Puas dengan hasilnya? Donasi via QRIS', short: 'Donasi via QRIS', x: 'Tutup' },
    en: { t: 'This service is free', s: 'If it helps, you can donate via QRIS: <b>Rp19,001</b>. Entirely optional, you may skip.',
          done: 'I Have Donated, Continue', skip: 'Skip and Continue', save: 'Save QRIS Image', thanks: 'Thank you',
          s2: 'Scan the QRIS with any Indonesian bank or e-wallet app and enter <b>Rp19,001</b>.', close: 'Close',
          pill: 'Happy with the result? Donate via QRIS', short: 'Donate via QRIS', x: 'Close' },
    zh: { t: '本服务免费', s: '如果对您有帮助，可通过 QRIS 捐赠 <b>Rp19.001</b>。完全自愿，可直接跳过。',
          done: '已捐赠，继续', skip: '跳过，继续', save: '保存 QRIS 图片', thanks: '谢谢',
          s2: '使用任意印尼银行或电子钱包扫描 QRIS，金额 <b>Rp19.001</b>。', close: '关闭',
          pill: '对结果满意？通过 QRIS 捐赠', short: 'QRIS 捐赠', x: '关闭' }
  }[L];

  var css = '#faDon{position:fixed;inset:0;z-index:2147483000;background:rgba(0,0,0,.72);display:flex;align-items:center;justify-content:center;padding:16px;font-family:Poppins,Inter,system-ui,sans-serif}' +
    '#faDon[hidden]{display:none}#faDon .fd{position:relative;background:#1b1b1b;color:#fff;border:1px solid #333;border-radius:14px;max-width:380px;width:100%;max-height:94vh;overflow:auto;padding:22px 20px;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,.5)}' +
    '#faDon h3{all:unset;display:block;font:500 22px/1.25 "EB Garamond",Georgia,serif;margin:0 0 6px;color:#fff;text-transform:none;letter-spacing:0}#faDon h3::before,#faDon h3::after{content:none!important;display:none!important}#faDon p{color:#b5b5b5;font-size:13px;line-height:1.6;margin:0 0 14px}#faDon p b{color:#fff}' +
    '#faDon img{width:100%;max-width:250px;height:auto;border-radius:10px;background:#fff;display:block;margin:0 auto}' +
    '#faDon .fb{display:grid;gap:8px;margin-top:16px}#faDon button,#faDon a.fs{all:unset;box-sizing:border-box;cursor:pointer;display:block;text-align:center;padding:11px 14px;border-radius:8px;font:500 14px Poppins,Inter,system-ui,sans-serif}' +
    '#faDon .p1{background:' + ACC + ';color:' + ACC_INK + '}#faDon .p2{border:1px solid #444;color:#fff}#faDon .p2:hover{border-color:#fff}#faDon a.fs{font-size:12px;color:#b5b5b5;text-decoration:underline;padding:4px}' +
    '#faDon .fx{position:absolute;right:8px;top:4px;padding:6px 10px!important;font-size:24px!important;line-height:1;color:#fff}' +
    '#faDonPill{position:fixed;left:14px;bottom:14px;z-index:2147482999;display:flex;align-items:center;gap:6px;background:#1b1b1b;color:#fff;border:1px solid #3a3a3a;border-radius:999px;padding:4px 4px 4px 14px;font:500 12.5px Poppins,Inter,system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.35);max-width:calc(100vw - 100px)}' +
    '#faDonPill[hidden]{display:none}#faDonPill a{color:#fff;text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}#faDonPill a:hover{text-decoration:underline}#faDonPill i{font-style:normal;color:' + (ACC === '#ffffff' ? '#ff6b6b' : ACC) + '}' +
    '#faDonPill .sh{display:none}@media (max-width:720px){#faDonPill{bottom:84px}#faDonPill .lg{display:none}#faDonPill .sh{display:inline}}' +
    '#faDonPill button{all:unset;cursor:pointer;width:26px;height:26px;display:grid;place-items:center;border-radius:50%;color:#aaa;font-size:16px}#faDonPill button:hover{background:#2a2a2a;color:#fff}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var m = document.createElement('div'); m.id = 'faDon'; m.hidden = true; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true');
  m.innerHTML = '<div class="fd"><button type="button" class="fx" aria-label="' + T.x + '">&times;</button><h3></h3><p class="fsub"></p>' +
    '<img src="' + IMG + '" width="720" height="1014" alt="QRIS FA Indonesia" loading="lazy">' +
    '<div class="fb"><button type="button" class="p1"></button><button type="button" class="p2"></button>' +
    '<a class="fs" href="' + IMG + '" download="QRIS-FA-Indonesia.jpg">' + T.save + '</a></div></div>';
  var pill = document.createElement('div'); pill.id = 'faDonPill'; pill.hidden = true;
  pill.innerHTML = '<i>&#9829;</i><a href="#" role="button"><span class="lg">' + T.pill + '</span><span class="sh">' + T.short + '</span></a><button type="button" aria-label="' + T.x + '">&times;</button>';
  function mount() { document.body.appendChild(m); document.body.appendChild(pill); }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);

  var cont = null;
  function ev(n, p) { try { if (window.gtag) gtag('event', n, p || {}); } catch (e) {} }
  function open(mode, cb) {
    cont = cb || null;
    m.querySelector('h3').textContent = mode === 'gate' ? T.t : T.thanks;
    m.querySelector('.fsub').innerHTML = mode === 'gate' ? T.s : T.s2;
    var b1 = m.querySelector('.p1'), b2 = m.querySelector('.p2');
    b1.textContent = mode === 'gate' ? T.done : T.close; b2.textContent = T.skip; b2.style.display = mode === 'gate' ? '' : 'none';
    m.hidden = false;
  }
  function finish(how) {
    m.hidden = true;
    if (cont) { var c = cont; cont = null; ev('qris_' + how); pill.hidden = false; c(); }
  }
  m.querySelector('.p1').onclick = function () { finish('donated'); };
  m.querySelector('.p2').onclick = function () { finish('skipped'); };
  m.querySelector('.fx').onclick = function () { m.hidden = true; cont = null; };
  m.addEventListener('click', function (e) { if (e.target === m) { m.hidden = true; cont = null; } });
  pill.querySelector('a').onclick = function (e) { e.preventDefault(); ev('qris_reopen'); open('info'); };
  pill.querySelector('button').onclick = function () { pill.hidden = true; };

  function passed(k) { try { return sessionStorage.getItem('fa-don-' + k) === '1'; } catch (e) { return false; } }
  function mark(k) { try { sessionStorage.setItem('fa-don-' + k, '1'); } catch (e) {} }

  var guards = C.guards || [];
  window.addEventListener('click', function (e) {
    for (var i = 0; i < guards.length; i++) {
      var g = guards[i], el = e.target.closest && e.target.closest(g.sel);
      if (!el) continue;
      if (el.__faDonPass) { el.__faDonPass = false; return; }
      if (g.skip && g.skip()) return;
      if (passed(g.key)) { pill.hidden = false; return; }
      e.preventDefault(); e.stopImmediatePropagation();
      ev('qris_gate', { tool: g.key });
      open('gate', function () { mark(g.key); el.__faDonPass = true; el.click(); });
      return;
    }
  }, true);
  window.FADonasi = { show: function () { open('info'); }, gate: function (k, cb) { if (passed(k)) { pill.hidden = false; cb(); return; } open('gate', function () { mark(k); cb(); }); } };
})();
