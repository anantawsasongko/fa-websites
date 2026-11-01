/* Lead tracking FA Indonesia, CariAkuntan, KJA (26 Okt 2026; form singkat 1 Nov 2026)
   1) Simpan sumber kunjungan pertama (google, instagram, threads, linkedin, langsung) di sessionStorage.
   2) Klik tombol WhatsApp ke nomor bisnis: tampilkan form singkat (Nama Usaha, Bentuk Usaha, Kota),
      lalu buka WA dengan pesan yang sudah memuat data itu + kode ref. Link share WA (tanpa nomor) tidak diubah.
   3) Event GA4: lead_form_open saat form muncul, generate_lead saat lanjut ke WA / klik email. */
(function(){
  var NUM=/wa\.me\/(6282245260121|6287872558626)|api\.whatsapp\.com\/send\?phone=(6282245260121|6287872558626)/;
  function src(){
    try{var s=sessionStorage.getItem('fa_src');if(s)return s}catch(e){}
    var q=new URLSearchParams(location.search),u=q.get('utm_source'),r=document.referrer,v='langsung';
    if(u)v=u;else if(q.get('gclid'))v='google-ads';else if(r){try{var h=new URL(r).hostname.replace(/^www\.|^l\.|^m\./,'');
      if(h.indexOf(location.hostname.replace(/^www\./,''))<0)v=h.split('.').slice(-2,-1)[0]||h}catch(e){}}
    try{sessionStorage.setItem('fa_src',v);sessionStorage.setItem('fa_land',location.pathname)}catch(e){}
    return v}
  var S=src();
  function land(){try{return sessionStorage.getItem('fa_land')||location.pathname}catch(e){return location.pathname}}
  function path(){return location.pathname.replace(/\/$/,'')||'/beranda'}
  function ga(n,o){try{if(window.gtag)gtag('event',n,o)}catch(e){}}
  function tag(){return ' [ref: '+location.hostname.replace(/^www\./,'').split('.')[0]+path()+' | '+S+']'}
  function load(){try{return JSON.parse(localStorage.getItem('fa_lead')||'{}')}catch(e){return {}}}
  function save(d){try{localStorage.setItem('fa_lead',JSON.stringify(d))}catch(e){}}
  function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}

  var css='.fal-ov{position:fixed;inset:0;z-index:2147483000;background:rgba(10,10,10,.55);display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box;font-family:var(--body,system-ui,-apple-system,Segoe UI,Roboto,sans-serif)}'
  +'.fal-box{background:#fff;color:#171717;width:100%;max-width:400px;border-radius:16px;padding:22px 20px 18px;box-sizing:border-box;box-shadow:0 20px 60px rgba(0,0,0,.3);max-height:calc(100vh - 32px);overflow-y:auto}'
  +'.fal-box h3{margin:0 0 4px;font-size:19px;line-height:1.3;font-family:var(--display,inherit);color:#171717}'
  +'.fal-box p.fal-sub{margin:0 0 16px;font-size:13.5px;line-height:1.45;color:#5c5c5c}'
  +'.fal-box label{display:block;font-size:12.5px;font-weight:600;margin:0 0 6px;color:#2f2f2f;letter-spacing:.2px}'
  +'.fal-box input[type=text]{display:block;width:100%;box-sizing:border-box;font-size:16px;padding:11px 12px;border:1.5px solid #d4d4d4;border-radius:10px;margin:0 0 14px;color:#171717;background:#fff;font-family:inherit}'
  +'.fal-box input[type=text]:focus{outline:none;border-color:#25D366}'
  +'.fal-seg{display:grid;grid-template-columns:1.5fr 1fr 1fr 1.3fr;gap:6px;margin:0 0 14px}'
  +'.fal-seg button{font-size:13px;font-weight:500;padding:10px 2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border:1.5px solid #d4d4d4;border-radius:10px;background:#fff;color:#2f2f2f;cursor:pointer;font-family:inherit;min-width:0}'
  +'.fal-seg button.on{border-color:#171717;background:#171717;color:#fff}'
  +'.fal-err{color:#c0392b;font-size:12.5px;margin:-6px 0 10px;min-height:0}'
  +'.fal-go{display:block;width:100%;border:0;border-radius:12px;background:#25D366;color:#fff;font-size:15.5px;font-weight:700;padding:13px;cursor:pointer;font-family:inherit}'
  +'.fal-x{display:block;width:100%;border:0;background:none;color:#7a7a7a;font-size:13px;padding:10px 0 0;cursor:pointer;font-family:inherit}'
  +'.fal-sec{display:flex;align-items:center;gap:6px;justify-content:center;font-size:11.5px;color:#7a7a7a;margin-top:6px}';

  function form(a,h){
    if(document.querySelector('.fal-ov'))return;
    if(!document.getElementById('fal-css')){var st=document.createElement('style');st.id='fal-css';st.textContent=css;document.head.appendChild(st)}
    var d=load(),ov=document.createElement('div');ov.className='fal-ov';
    ov.innerHTML='<div class="fal-box" role="dialog" aria-modal="true" aria-label="Data Singkat Sebelum Chat">'
      +'<h3>Sedikit Info Sebelum Chat</h3><p class="fal-sub">Supaya tim kami bisa langsung menyapa dengan benar dan memberi estimasi yang pas.</p>'
      +'<label for="fal-n">Nama Usaha</label><input type="text" id="fal-n" autocomplete="organization" placeholder="Contoh: Toko Maju Jaya" value="'+esc(d.n)+'">'
      +'<label>Bentuk Usaha</label><div class="fal-seg">'
      +['Perorangan','CV','PT','Lainnya'].map(function(x){return '<button type="button" data-v="'+x+'"'+(d.b===x?' class="on"':'')+'>'+x+'</button>'}).join('')+'</div>'
      +'<label for="fal-k">Kota</label><input type="text" id="fal-k" autocomplete="address-level2" placeholder="Contoh: Malang" value="'+esc(d.k)+'">'
      +'<div class="fal-err"></div>'
      +'<button type="button" class="fal-go">Lanjut Ke WhatsApp</button><button type="button" class="fal-x">Batal</button></div>';
    document.body.appendChild(ov);
    var b=d.b||'',err=ov.querySelector('.fal-err'),n=ov.querySelector('#fal-n'),k=ov.querySelector('#fal-k');
    ov.querySelectorAll('.fal-seg button').forEach(function(x){x.addEventListener('click',function(){
      ov.querySelectorAll('.fal-seg button').forEach(function(y){y.classList.remove('on')});x.classList.add('on');b=x.getAttribute('data-v')})});
    function close(){ov.remove();document.removeEventListener('keydown',kd)}
    function kd(e){if(e.key==='Escape')close()}
    document.addEventListener('keydown',kd);
    ov.addEventListener('click',function(e){if(e.target===ov)close()});
    ov.querySelector('.fal-x').addEventListener('click',close);
    ov.querySelector('.fal-go').addEventListener('click',function(){
      var nv=n.value.trim(),kv=k.value.trim();
      if(!nv||!b||!kv){err.textContent='Mohon isi Nama Usaha, Bentuk Usaha, dan Kota.';(!nv?n:!kv&&b?k:n).focus();return}
      save({n:nv,b:b,k:kv});
      var U=new URL(h,location.href),t=(U.searchParams.get('text')||'').replace(/\s*\[ref:[^\]]*\]\s*$/,'');
      t=(t||'Halo, saya ingin konsultasi.')+'\n\nNama usaha: '+nv+'\nBentuk usaha: '+b+'\nKota: '+kv+'\n'+tag().trim();
      U.searchParams.delete('text');var base=U.toString(),url=base+(base.indexOf('?')<0?'?':'&')+'text='+encodeURIComponent(t);
      ga('generate_lead',{method:'whatsapp',lead_page:path(),lead_source:S,landing_page:land(),link_text:(a.textContent||'').trim().slice(0,60),bentuk_usaha:b,kota:kv});
      close();
      var w=null;if(a.target==='_blank'){try{w=window.open(url,'_blank','noopener')}catch(e){}}
      if(!w)location.href=url;
    });
    setTimeout(function(){(d.n?k:n).focus()},50);
  }

  document.addEventListener('click',function(ev){
    var a=ev.target&&ev.target.closest?ev.target.closest('a[href]'):null;if(!a)return;
    var h=a.getAttribute('href')||'',wa=/wa\.me\/|api\.whatsapp\.com/.test(h),ml=/^mailto:/i.test(h);
    if(!wa&&!ml)return;
    if(ml){ga('generate_lead',{method:'email',lead_page:path(),lead_source:S,landing_page:land(),link_text:(a.textContent||'').trim().slice(0,60)});return}
    if(NUM.test(h)&&!a.hasAttribute('data-noform')){
      ev.preventDefault();ev.stopPropagation();
      ga('lead_form_open',{lead_page:path(),lead_source:S});
      form(a,h);return}
    if(!a.dataset.refd){
      try{var U=new URL(h,location.href),t=U.searchParams.get('text')||'';
        if(/wa\.me\/\d|phone=\d/.test(h)&&t.indexOf('[ref:')<0){U.searchParams.delete('text');var b=U.toString();a.setAttribute('href',b+(b.indexOf('?')<0?'?':'&')+'text='+encodeURIComponent(t+tag()))}
        a.dataset.refd='1'}catch(e){}}
  },true);
})();
