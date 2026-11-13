/* 13 Nov 2026: video pratinjau tools FA diputar hanya saat terlihat (hemat kuota data). Dipasang oleh fa_tools_anim_20261113.py. */
(function(){
  var vs=document.querySelectorAll('.ftv video[data-src]');if(!vs.length)return;
  function on(v){if(!v.src){v.src=v.getAttribute('data-src');}var p=v.play();if(p&&p.catch)p.catch(function(){});}
  if(!('IntersectionObserver' in window)){vs.forEach(on);return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting&&e.intersectionRatio>=.35){on(v);}else if(v.src){v.pause();}});},{threshold:[0,.35,.7]});
  vs.forEach(function(v){io.observe(v);});
})();
