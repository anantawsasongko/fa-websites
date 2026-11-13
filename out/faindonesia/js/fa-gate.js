/* fa-gate.js (13 Nov 2026, fa_semua_berbayar_20261113.py): template Excel dan pustaka kertas kerja berbayar via Midtrans. */
(function(){var C=window.FA_GATE;if(!C)return;var P=C.prod,K='fa_pay_'+P,ok=false,oid=null;
try{var q=new URLSearchParams(location.search).get('order_id');if(q&&/^FA-\d{6}-[a-z0-9-]+-[A-Z2-9]{8}$/.test(q)){localStorage.setItem(K,q);history.replaceState(null,'',location.pathname+location.hash)}oid=localStorage.getItem(K)}catch(e){}
function go(){location.href='/bayar/?produk='+encodeURIComponent(P)+'&back='+encodeURIComponent(location.pathname)}
if(oid){var u=C.file?'/api/pay/status?order_id='+encodeURIComponent(oid):'/api/pay/check?order_id='+encodeURIComponent(oid)+'&prod='+encodeURIComponent(P);
 fetch(u,{cache:'no-store'}).then(function(r){return r.json()}).then(function(x){ok=C.file?!!(x&&x.paid&&x.access&&x.access.kind==='file'):!!(x&&x.ok)}).catch(function(){})}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest(C.sel);if(!a)return;
 if(C.file){e.preventDefault();e.stopImmediatePropagation();if(!ok){go();return}
  var m=(a.getAttribute('href')||'').match(/\/saturn\/kk\/(.+)$/);if(!m){go();return}
  location.href='/api/pay/file?order_id='+encodeURIComponent(oid)+'&f='+encodeURIComponent('saturn/'+decodeURIComponent(m[1]));return}
 if(ok)return;e.preventDefault();e.stopImmediatePropagation();go()},true)})();
