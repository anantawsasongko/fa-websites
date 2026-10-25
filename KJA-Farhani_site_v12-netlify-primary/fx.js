/* KJA Farhani K.N. — motion layer. Content is fully visible without JS. */
(function(){
  var d=document,root=d.documentElement;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO='IntersectionObserver' in window;

  /* header shadow + reading progress */
  var top=d.querySelector('.top'),bar=d.createElement('div');bar.className='progress';d.body.appendChild(bar);
  var ticking=false;
  function onScroll(){
    var y=window.scrollY||0,h=root.scrollHeight-innerHeight;
    if(top)top.classList.toggle('scrolled',y>8);
    bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';ticking=false;
  }
  addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});onScroll();

  if(!hasIO||reduce){d.querySelectorAll('.eyebrow,.route,.track,.cal,[data-count]').forEach(function(e){e.classList.add('in')});return}

  /* auto-tag reveal targets with a stagger per parent */
  var sel=['section h2','section .intro','.svc > div','.rel > div','.dl-list > div','.people > .person','section details',
    '.stats > div','.tabs','.calwrap','.route','.track','table.seg','.article h2','.article .box','.list-art','.booklet','.addr'];
  d.querySelectorAll(sel.join(',')).forEach(function(el){
    if(el.closest('.hero'))return;
    el.setAttribute('data-rv','');
    var i=Array.prototype.indexOf.call(el.parentNode.children,el);
    el.style.setProperty('--d',Math.min(i,8)*0.07+'s');
  });
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return;var t=e.target;t.classList.add('in');io.unobserve(t);
    if(t.hasAttribute('data-count'))count(t);
    t.querySelectorAll&&t.querySelectorAll('[data-count]').forEach(count);
  })},{rootMargin:'0px 0px -12% 0px',threshold:.12});
  d.querySelectorAll('[data-rv],.eyebrow,.route,.track,.cal,.stats').forEach(function(e){io.observe(e)});

  /* count-up numbers */
  function count(el){
    if(el._done)return;el._done=true;
    var to=parseFloat(el.getAttribute('data-count')),dur=1400,t0=null,dec=(el.getAttribute('data-count').split('.')[1]||'').length;
    function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/dur),v=to*(1-Math.pow(1-p,3));
      el.textContent=dec?v.toFixed(dec).replace('.',','):Math.round(v).toString();if(p<1)requestAnimationFrame(step)}
    requestAnimationFrame(step);
  }
})();

/* tabs (works with or without the motion layer) */
(function(){
  document.querySelectorAll('.tabs').forEach(function(w){
    var tabs=w.querySelectorAll('[role=tab]'),panels=w.querySelectorAll('[role=tabpanel]'),ind=w.querySelector('.tab-ind');
    if(!tabs.length)return;w.classList.add('on');
    function sel(i,focus){
      tabs.forEach(function(t,j){t.setAttribute('aria-selected',j===i);t.tabIndex=j===i?0:-1});
      panels.forEach(function(p,j){p.hidden=j!==i;if(j===i){p.classList.remove('show');void p.offsetWidth;p.classList.add('show')}});
      if(ind){ind.style.width=tabs[i].offsetWidth+'px';ind.style.transform='translateX('+tabs[i].offsetLeft+'px)'}
      if(focus)tabs[i].focus();
    }
    tabs.forEach(function(t,i){
      t.addEventListener('click',function(){sel(i)});
      t.addEventListener('keydown',function(e){var k=e.key,n=tabs.length;
        if(k==='ArrowRight'||k==='ArrowLeft'){e.preventDefault();sel((i+(k==='ArrowRight'?1:n-1))%n,true)}});
    });
    sel(0);addEventListener('resize',function(){var a=w.querySelector('[aria-selected=true]');if(a&&ind){ind.style.width=a.offsetWidth+'px';ind.style.transform='translateX('+a.offsetLeft+'px)'}});
  });
  /* compliance calendar: mark the current month */
  var cal=document.querySelector('.cal');
  if(cal){var m=new Date().getMonth();cal.style.setProperty('--now',m);cal.classList.add('has-now');
    var lab=cal.querySelectorAll('.cal-m .plot span')[m];if(lab)lab.classList.add('now');
    var now=cal.querySelector('.cal-now');if(now)now.setAttribute('aria-label','Bulan ini')}
})();
