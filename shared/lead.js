/* Lead tracking FA Indonesia, CariAkuntan, KJA (26 Okt 2026)
   1) Simpan sumber kunjungan pertama (google, instagram, threads, linkedin, langsung) di sessionStorage.
   2) Setiap klik WhatsApp / email: kirim event GA4 generate_lead + tambah kode ref pendek di pesan WA. */
(function(){
  function src(){
    try{var s=sessionStorage.getItem('fa_src');if(s)return s}catch(e){}
    var q=new URLSearchParams(location.search),u=q.get('utm_source'),r=document.referrer,v='langsung';
    if(u)v=u;else if(q.get('gclid'))v='google-ads';else if(r){try{var h=new URL(r).hostname.replace(/^www\.|^l\.|^m\./,'');
      if(h.indexOf(location.hostname.replace(/^www\./,''))<0)v=h.split('.').slice(-2,-1)[0]||h}catch(e){}}
    try{sessionStorage.setItem('fa_src',v);sessionStorage.setItem('fa_land',location.pathname)}catch(e){}
    return v}
  var S=src();
  function land(){try{return sessionStorage.getItem('fa_land')||location.pathname}catch(e){return location.pathname}}
  document.addEventListener('click',function(ev){
    var a=ev.target&&ev.target.closest?ev.target.closest('a[href]'):null;if(!a)return;
    var h=a.getAttribute('href')||'',wa=/wa\.me\/|api\.whatsapp\.com/.test(h),ml=/^mailto:/i.test(h);
    if(!wa&&!ml)return;
    var path=location.pathname.replace(/\/$/,'')||'/beranda';
    try{if(window.gtag)gtag('event','generate_lead',{method:wa?'whatsapp':'email',lead_page:path,lead_source:S,landing_page:land(),link_text:(a.textContent||'').trim().slice(0,60)})}catch(e){}
    if(wa&&!a.dataset.refd){
      try{var U=new URL(h,location.href),t=U.searchParams.get('text')||'';
        var tag=' [ref: '+location.hostname.replace(/^www\./,'').split('.')[0]+path+' | '+S+']';
        if(t.indexOf('[ref:')<0){U.searchParams.delete('text');var b=U.toString();a.setAttribute('href',b+(b.indexOf('?')<0?'?':'&')+'text='+encodeURIComponent(t+tag))}
        a.dataset.refd='1'}catch(e){}}
  },true);
})();
