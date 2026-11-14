/* 14 Nov 2026 (Bos: "bahasa Inggris dan Mandarinnya kalau buka dari layanan masih indo aja").
   Pilihan bahasa ID / EN / 中文 berlaku di SEMUA halaman FA, bukan hanya beranda dan /layanan/.
   Urutan: (1) bila halaman punya versi resmi bahasa itu (link hreflang), pindah ke sana;
           (2) bila tidak, terjemahan otomatis Google di browser pengunjung (tidak memengaruhi SEO).
   Halaman berbahasa Inggris tidak pernah diterjemahkan ke bahasa Indonesia secara otomatis.
   Tidak pernah aktif bila pengunjung belum memilih bahasa. Dipasang oleh fa_lang_global_20261114.py. */
(function () {
  if (window.__faLang) return; window.__faLang = 1;
  var KEY = 'fa-lang', pick = null;
  try { pick = localStorage.getItem(KEY); } catch (e) {}
  var src = (document.documentElement.lang || 'id').slice(0, 2).toLowerCase();
  var GT = { id: 'id', en: 'en', zh: 'zh-CN' };

  function alt(l) {
    var a = document.querySelector('link[rel="alternate"][hreflang="' + l + '"]') ||
            (l === 'zh' && document.querySelector('link[rel="alternate"][hreflang^="zh"]'));
    if (!a) return null;
    try { var u = new URL(a.href, location.href); return u.pathname === location.pathname ? null : u.href; } catch (e) { return null; }
  }
  function cookie(v) {
    var host = location.hostname, base = host.replace(/^www\./, '');
    var exp = v ? '' : ';expires=Thu, 01 Jan 1970 00:00:00 GMT';
    ['', ';domain=' + host, ';domain=.' + base].forEach(function (d) {
      document.cookie = 'googtrans=' + (v || '') + ';path=/' + d + exp;
    });
  }
  function target(l) {
    if (!l || l === src) return null;
    if (l === 'id' && src === 'en') return null;      // halaman Inggris tetap Inggris
    return '/' + src + '/' + GT[l];
  }
  function loadGT() {
    if (document.getElementById('fa-gt-js')) return;
    var st = document.createElement('style');
    st.textContent = '.goog-te-banner-frame,.skiptranslate>iframe,iframe.skiptranslate,#goog-gt-tt,.goog-te-balloon-frame,.VIpgJd-ZVi9od-ORHb-OEVmcd,.VIpgJd-ZVi9od-aZ2wEe-wOHMyf{display:none!important;visibility:hidden!important}' +
      'body{top:0!important;position:static!important}.goog-text-highlight{background:none!important;box-shadow:none!important}#fa-gt{display:none}';
    document.head.appendChild(st);
    var d = document.createElement('div'); d.id = 'fa-gt'; document.body.appendChild(d);
    window.faGtInit = function () {
      try { new google.translate.TranslateElement({ pageLanguage: src, autoDisplay: false }, 'fa-gt'); } catch (e) {}
    };
    var s = document.createElement('script'); s.id = 'fa-gt-js'; s.async = true;
    s.src = 'https://translate.google.com/translate_a/element.js?cb=faGtInit';
    document.body.appendChild(s);
  }
  function go(l) {
    try { localStorage.setItem(KEY, l); } catch (e) {}
    var a = alt(l); if (a) { location.href = a; return; }
    var t = target(l); cookie(t); location.reload();
  }

  // tombol bahasa di header (halaman yang belum punya)
  var hr = document.querySelector('header .hright');
  if (hr && !hr.querySelector('.lang')) {
    var g = document.createElement('div'); g.className = 'lang notranslate'; g.setAttribute('role', 'group');
    g.setAttribute('aria-label', 'Bahasa / Language'); g.setAttribute('translate', 'no');
    [['id', 'ID'], ['en', 'EN'], ['zh', '中文']].forEach(function (x) {
      var b = document.createElement('button'); b.type = 'button'; b.dataset.lang = x[0]; b.textContent = x[1];
      b.addEventListener('click', function () { go(x[0]); });
      g.appendChild(b);
    });
    hr.appendChild(g);
  }
  var cur = pick || src;
  document.querySelectorAll('header .lang button').forEach(function (b) {
    b.setAttribute('aria-pressed', b.dataset.lang === (pick ? pick : src) ? 'true' : 'false');
  });
  document.querySelectorAll('.brand,.fx-fig figcaption b,.fcp .nm').forEach(function (e) { e.classList.add('notranslate'); });

  if (!pick) return;                         // pengunjung belum memilih: tampil apa adanya
  var a = alt(pick);
  if (a && pick !== src) { location.replace(a); return; }
  var t = target(pick);
  if (t) { cookie(t); loadGT(); } else if (/googtrans=/.test(document.cookie)) { cookie(null); }
})();
