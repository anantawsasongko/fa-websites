/* Intake kotak kontak (12 Nov 2026): keperluan + omzet ikut ke pesan WhatsApp. */
(function(){
  document.querySelectorAll('.lk2').forEach(function(box){
    var sel=box.querySelectorAll('.lk2-q select'); if(!sel.length) return;
    var links=[].slice.call(box.querySelectorAll('a[href*="wa.me"]'));
    links.forEach(function(a){ a.dataset.base=a.getAttribute('href'); });
    function upd(){
      var perlu=sel[0].value, omzet=sel[1]?sel[1].value:'';
      links.forEach(function(a){
        var u=a.dataset.base, i=u.indexOf('text='); if(i<0) return;
        var t=decodeURIComponent(u.slice(i+5));
        t=t.replace(/\s*Keperluan: bank \/ SABH \/ tender \/ investor\.?/,'');
        if(perlu) t+=' Keperluan: '+perlu+'.';
        if(omzet) t+=' Omzet setahun: '+omzet+'.';
        a.setAttribute('href',u.slice(0,i+5)+encodeURIComponent(t));
      });
    }
    [].forEach.call(sel,function(s){ s.addEventListener('change',upd); });
  });
})();
