/* Tombol share universal FA Indonesia, CariAkuntan, UpdateSAK (28 Okt 2026).
   - Bagikan: share sheet HP berisi poster story + judul + link (pilih IG, Threads, LinkedIn, WA, dll.).
   - Instagram: link otomatis tersalin, poster dibuka di share sheet (atau di-download di desktop), tinggal tempel di sticker Link.
   - Threads / LinkedIn / WhatsApp: composer terbuka dengan judul + link terisi; kartu pratinjau memakai og:image.
   - Salin Link.
   Poster story dibuat di browser (canvas) kalau tidak ada gambar story siap pakai. Tidak ada data yang dikirim ke server kami. */
(function () {
  if (window.__faShare) return; window.__faShare = 1;
  var H = location.hostname.replace(/^www\./, '');
  var B = /cariakuntan/.test(H) ? { l: 'C', n: 'cariakuntan.com', c1: '#0B1F33', c2: '#1F5BFF', ac: '#8FB2FF', tag: 'KAP, KJPP, Pajak, Laporan Keuangan' }
        : /updatesak/.test(H) ? { l: 'U', n: 'updatesak.com', c1: '#0B1F33', c2: '#1F5BFF', ac: '#8FB2FF', tag: 'Kalkulator PSAK dan CALK' }
        : { l: 'F', n: 'faindonesia.co.id', c1: '#0a0a0a', c2: '#7f1d1d', ac: '#fca5a5', tag: 'Kredit Bank, Investor, IPO' };
  var canon = (document.querySelector('link[rel=canonical]') || {}).href || location.href.split('#')[0];
  var h1 = document.querySelector('main h1, h1');
  var title = ((h1 && h1.innerText) || document.title.split(' | ')[0]).trim().replace(/\s+/g, ' ');
  var kick = '';
  var k = document.querySelector('.label, .eyebrow, .crumb + .label');
  if (k) kick = k.innerText.replace(/^Eksplor\s*·\s*/i, '').trim();

  function ga(m) { try { if (window.gtag) gtag('event', 'share', { method: m, item_id: canon }); } catch (e) {} }
  var toastEl;
  function toast(m) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'fxs-toast'; toastEl.setAttribute('role', 'status'); document.body.appendChild(toastEl); }
    toastEl.textContent = m; toastEl.classList.add('on'); clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove('on'); }, 6500);
  }
  function copy(t) {
    try { if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(t).then(function () { return true; }, function () { return fb(); }); } catch (e) {}
    return Promise.resolve(fb());
    function fb() { var a = document.createElement('textarea'); a.value = t; a.style.position = 'fixed'; a.style.opacity = '0'; document.body.appendChild(a); a.select(); var ok = false; try { ok = document.execCommand('copy'); } catch (e) {} a.remove(); return ok; }
  }

  var ready = null;
  function storyUrl() {
    var d = document.querySelector('[data-story]'); if (d) return d.getAttribute('data-story');
    var a = document.querySelector('a[href*="-story.jpg"]'); if (a) return a.getAttribute('href');
    return null;
  }
  function wrap(ctx, text, maxw) {
    var w = text.split(' '), lines = [], cur = '';
    w.forEach(function (x) { var t = (cur + ' ' + x).trim(); if (ctx.measureText(t).width <= maxw) cur = t; else { if (cur) lines.push(cur); cur = x; } });
    if (cur) lines.push(cur); return lines;
  }
  function makePoster() {
    if (ready) return ready;
    var su = storyUrl();
    if (su) { ready = fetch(su).then(function (r) { if (!r.ok) throw 0; return r.blob(); }).catch(function () { return draw(); }); return ready; }
    ready = draw(); return ready;
  }
  function draw() {
    return new Promise(function (res) {
      var W = 1080, Hh = 1920, c = document.createElement('canvas'); c.width = W; c.height = Hh;
      var x = c.getContext('2d');
      var g = x.createLinearGradient(0, 0, W, Hh); g.addColorStop(0, B.c1); g.addColorStop(1, B.c2); x.fillStyle = g; x.fillRect(0, 0, W, Hh);
      x.fillStyle = 'rgba(255,255,255,.10)'; for (var i = 0; i < W; i += 28) for (var j = 0; j < Hh; j += 28) x.fillRect(i, j, 2, 2);
      var serif = getComputedStyle(h1 || document.body).fontFamily || 'Georgia, serif';
      var sans = getComputedStyle(document.body).fontFamily || 'system-ui, sans-serif';
      var m = 96;
      x.strokeStyle = '#fff'; x.lineWidth = 3; x.strokeRect(m, m, 54, 72); x.fillStyle = '#fff'; x.font = '400 22px ' + sans; x.textBaseline = 'middle'; x.fillText(B.l, m + 9, m + 20); x.lineWidth = 2.5; x.beginPath(); if (B.l === 'U') { x.moveTo(m + 32, m + 46); x.quadraticCurveTo(m + 36, m + 40, m + 40, m + 46); x.quadraticCurveTo(m + 44, m + 52, m + 40, m + 58); x.quadraticCurveTo(m + 36, m + 64, m + 32, m + 60); } else { x.moveTo(m + 30, m + 62); x.lineTo(m + 37, m + 44); x.lineTo(m + 44, m + 62); } x.stroke();
      x.fillStyle = '#fff'; x.font = '600 40px ' + sans; x.textBaseline = 'middle'; x.fillText(B.n, m + 80, m + 36);
      var y = 560;
      if (kick) { x.fillStyle = B.ac; x.font = '600 38px ' + sans; x.fillText(kick.toUpperCase(), m, y); y += 90; }
      var size = 92, lines;
      do { x.font = '600 ' + size + 'px ' + serif; lines = wrap(x, title, W - 2 * m); size -= 6; } while (lines.length > 7 && size > 50);
      size += 6; x.fillStyle = '#fff'; x.textBaseline = 'top';
      lines.forEach(function (l) { x.fillText(l, m, y); y += size * 1.2; });
      x.fillStyle = B.ac; x.fillRect(m, y + 30, 90, 8);
      x.fillStyle = 'rgba(255,255,255,.85)'; x.font = '400 38px ' + sans; x.fillText(B.tag, m, Hh - 330);
      x.fillStyle = '#fff'; x.fillRect(m, Hh - 250, W - 2 * m, 120);
      x.fillStyle = B.c1; x.font = '600 40px ' + sans; x.textBaseline = 'middle';
      var u = canon.replace(/^https?:\/\//, ''); if (x.measureText(u).width > W - 2 * m - 60) u = B.n;
      x.fillText('Baca: ' + u, m + 30, Hh - 190);
      c.toBlob(function (b) { res(b); }, 'image/jpeg', .88);
    });
  }
  function fileOf(b) { var slug = (canon.split('/').filter(Boolean).pop() || 'artikel').slice(0, 60); return new File([b], slug + '-story.jpg', { type: 'image/jpeg' }); }
  function download(b) { var u = URL.createObjectURL(b), a = document.createElement('a'); a.href = u; a.download = fileOf(b).name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(u); }, 4000); }
  var text = title + '\n\n' + canon;

  function nativeShare(withFile) {
    return makePoster().then(function (b) {
      var f = fileOf(b);
      if (withFile && navigator.canShare && navigator.canShare({ files: [f] })) return navigator.share({ files: [f], title: title, text: text }).then(function () { return 'ok'; }, function (e) { return e && e.name === 'AbortError' ? 'abort' : 'fail'; });
      if (!withFile && navigator.share) return navigator.share({ title: title, text: title, url: canon }).then(function () { return 'ok'; }, function (e) { return e && e.name === 'AbortError' ? 'abort' : 'fail'; });
      return 'none';
    });
  }
  var ACT = {
    all: function () { ga('native'); nativeShare(true).then(function (r) { if (r === 'none') nativeShare(false).then(function (r2) { if (r2 === 'none') copy(canon).then(function () { toast('Link tersalin. Tempel di aplikasi mana saja.'); }); }); }); },
    ig: function () {
      ga('instagram');
      copy(canon).then(function () {
        nativeShare(true).then(function (r) {
          if (r === 'ok' || r === 'abort') { toast('Link sudah tersalin. Di Instagram pilih Story, tambahkan sticker Link, lalu tempel.'); return; }
          makePoster().then(download); toast('Poster di-download dan link sudah tersalin. Upload poster ke Instagram Story, tambahkan sticker Link, lalu tempel.');
        });
      });
    },
    th: function () { ga('threads'); window.open('https://www.threads.net/intent/post?text=' + encodeURIComponent(text), '_blank', 'noopener'); },
    li: function () { ga('linkedin'); copy(canon); window.open('https://www.linkedin.com/feed/?shareActive=true&text=' + encodeURIComponent(text), '_blank', 'noopener'); },
    wa: function () { ga('whatsapp'); window.open('https://wa.me/?text=' + encodeURIComponent(text), '_blank', 'noopener'); },
    cp: function (b) { ga('copy'); copy(canon).then(function () { var o = b.lastChild.textContent; b.lastChild.textContent = 'Tersalin'; setTimeout(function () { b.lastChild.textContent = o; }, 2000); }); }
  };
  var IC = {
    all: '<path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>',
    ig: '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".9" fill="currentColor"/>',
    th: '<path d="M16.5 11.2c-.3-2.6-2-3.9-4.4-3.9-2.6 0-4.3 1.8-4.3 4.7s1.7 4.8 4.4 4.8c2.2 0 3.6-1.1 3.6-2.8 0-1.5-1.2-2.4-3.2-2.4-1.7 0-2.6.8-2.6 1.9M12 21c-5 0-8.5-3.4-8.5-9S7 3 12 3c4 0 6.8 2 7.9 5.5"/>',
    li: '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/>',
    wa: '<path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c.5 2 2.5 4 4.5 4.5l1-1 2 1"/>',
    cp: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>'
  };
  var LB = { all: 'Bagikan', ig: 'Instagram', th: 'Threads', li: 'LinkedIn', wa: 'WhatsApp', cp: 'Salin Link' };
  var css = '.fxs{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:18px 0 22px;font-family:inherit}.fxs>span{font-size:.8rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.7;margin-right:4px}' +
    '.fxs button{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:7px;padding:8px 12px;border-radius:999px;border:1px solid rgba(127,127,127,.35);font:600 .84rem/1 inherit;font-family:inherit;transition:background .2s,transform .2s}' +
    '.fxs button:hover{transform:translateY(-1px);background:rgba(127,127,127,.12)}.fxs button svg{width:17px;height:17px;flex:none}.fxs button.p{background:' + B.c2 + ';border-color:' + B.c2 + ';color:#fff}' +
    '.fxs-toast{position:fixed;left:50%;bottom:90px;transform:translate(-50%,20px);max-width:min(92vw,460px);background:#111827;color:#fff;padding:12px 16px;border-radius:10px;font:500 .9rem/1.45 system-ui,sans-serif;box-shadow:0 12px 30px rgba(0,0,0,.3);opacity:0;pointer-events:none;transition:.3s;z-index:9999}.fxs-toast.on{opacity:1;transform:translate(-50%,0)}' +
    '@media (max-width:520px){.fxs button{padding:8px 10px}.fxs button span{display:none}.fxs button.p span,.fxs button.ig span{display:inline}}';
  function bar() {
    var d = document.createElement('div'); d.className = 'fxs'; d.setAttribute('aria-label', 'Bagikan halaman ini');
    var show = navigator.share ? ['all', 'ig', 'th', 'li', 'wa', 'cp'] : ['ig', 'th', 'li', 'wa', 'cp'];
    d.innerHTML = '<span>Bagikan</span>' + show.map(function (k) { return '<button type="button" data-a="' + k + '" class="' + (k === 'all' ? 'p' : k) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + IC[k] + '</svg><span>' + LB[k] + '</span></button>'; }).join('');
    d.addEventListener('click', function (e) { var b = e.target.closest('button[data-a]'); if (b) ACT[b.getAttribute('data-a')](b); });
    return d;
  }
  function isArticle() {
    return [].some.call(document.querySelectorAll('script[type="application/ld+json"]'), function (s) { return /"@type"\s*:\s*"(Article|NewsArticle|BlogPosting)"/.test(s.textContent); });
  }
  function run() {
    if (!isArticle()) return;
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var olds = document.querySelectorAll('main .share, .art .share, article .share');
    if (olds.length) { [].forEach.call(olds, function (o) { o.replaceWith(bar()); }); return; }
    var main = document.querySelector('main') || document.body;
    var anchor = main.querySelector('.meta, .meta-line, .upd, .sub') || (h1 && h1.nextElementSibling) || h1;
    if (anchor) anchor.insertAdjacentElement('afterend', bar());
    var end = document.querySelector('.fxrel');
    if (end) end.insertAdjacentElement('beforebegin', bar());
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
