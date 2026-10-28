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
    th: function () { ga('threads'); window.open('https://www.threads.com/intent/post?text=' + encodeURIComponent(text), '_blank', 'noopener'); },
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
  var BRAND = { ig: ['M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077', 'radial-gradient(circle at 30% 107%,#fdf497 0%,#fdf497 5%,#fd5949 45%,#d6249f 60%,#285AEB 90%)'], th: ['M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 0 1 3.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.79-1.548 7.158-1.85 1.81-4.094 2.628-7.277 2.65Zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 0 0-2.215-.221z', '#000'], li: ['M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z', '#0A66C2'], wa: ['M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z', '#25D366'] };
  var LB = { all: 'Bagikan', ig: 'Instagram', th: 'Threads', li: 'LinkedIn', wa: 'WhatsApp', cp: 'Salin Link' };
  var css = '.fxs{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:18px 0 22px;font-family:inherit}.fxs>span{font-size:.8rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.7;margin-right:4px}' +
    '.fxs button{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:7px;padding:8px 12px;border-radius:999px;border:1px solid rgba(127,127,127,.35);font:600 .84rem/1 inherit;font-family:inherit;transition:background .2s,transform .2s}' +
    '.fxs button:hover{transform:translateY(-1px);background:rgba(127,127,127,.12)}.fxs button svg{width:17px;height:17px;flex:none}.fxs button.p{background:' + B.c2 + ';border-color:' + B.c2 + ';color:#fff}.fxs button.br{width:40px;height:40px;padding:0;justify-content:center;border:0;border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,.18)}.fxs button.br svg{width:20px;height:20px}.fxs button.br:hover{transform:translateY(-2px) scale(1.06);background-blend-mode:normal;filter:brightness(1.08)}' +
    '.fxs-toast{position:fixed;left:50%;bottom:90px;transform:translate(-50%,20px);max-width:min(92vw,460px);background:#111827;color:#fff;padding:12px 16px;border-radius:10px;font:500 .9rem/1.45 system-ui,sans-serif;box-shadow:0 12px 30px rgba(0,0,0,.3);opacity:0;pointer-events:none;transition:.3s;z-index:9999}.fxs-toast.on{opacity:1;transform:translate(-50%,0)}' +
    '.fxs button.br{box-shadow:0 0 0 1px rgba(127,127,127,.35),0 2px 6px rgba(0,0,0,.18)}@media (max-width:520px){.fxs{gap:7px}.fxs>span{display:none}.fxs button.p,.fxs button.cp{width:40px;height:40px;padding:0;justify-content:center;border-radius:50%}.fxs button.p span,.fxs button.cp span{display:none}}';
  function bar() {
    var d = document.createElement('div'); d.className = 'fxs'; d.setAttribute('aria-label', 'Bagikan halaman ini');
    var show = navigator.share ? ['ig', 'th', 'li', 'wa', 'all', 'cp'] : ['ig', 'th', 'li', 'wa', 'cp'];
    d.innerHTML = '<span>Bagikan</span>' + show.map(function (k) {
      if (BRAND[k]) return '<button type="button" data-a="' + k + '" class="br" title="Bagikan ke ' + LB[k] + '" aria-label="Bagikan ke ' + LB[k] + '" style="background:' + BRAND[k][1] + '"><svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="' + BRAND[k][0] + '"/></svg></button>';
      return '<button type="button" data-a="' + k + '" class="' + (k === 'all' ? 'p' : k) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + IC[k] + '</svg><span>' + LB[k] + '</span></button>'; }).join('');
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
