#!/usr/bin/env python3
"""22 Nov 2026: Klien dan Bank di /layanan/ FA.
Bos: "Update logo klien, tapi jangan Lixicon. GPMS, Inni Joa, RS seller side, dll. Bank juga baru UOB, CCB"
dan "klien yang tulisan atau tanpa logo dibuat gak masuk SEO dan picture (gak bisa di copas)".
- Baris "Klien lainnya" dan baris baru "Bank lainnya" dirender jadi gambar teks (alt kosong, tidak bisa dipilih/copas,
  nama file netral), jadi nama klien tidak terbaca Google.
- RS seller side tetap anonim (keputusan 19 Nov).
- Logo asli GPMS, UOB, CCB menyusul bila file logo ada: taruh di img/clients/ atau img/banks/, ganti item di NAMA/BANK.
Idempoten, --dry. Penanda <!--kb22-->.
"""
import sys, re, hashlib, os
from PIL import Image, ImageDraw, ImageFont
DRY='--dry' in sys.argv
KLIEN=["PT GPMS","PT Inni Joa","Rumah sakit swasta di Jawa Barat dan Banten (seller side)",
       "PT Semesta Cipta Lab Indonesia","PT Rinda Setya Renjana","PT Akazaya Sinergi Indonesia",
       "PT Odo Multi Aero","PT Garuda Lintas Cakrawala"]
BANK=["Bank UOB Indonesia","Bank China Construction Bank Indonesia"]
FONT='/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'
S=3; PX=13*S; COL=(168,168,168,255); TRACK=0.04*PX
IMG='out/faindonesia/img/clients/x'
def render(t):
    f=ImageFont.truetype(FONT,PX)
    w=int(sum(f.getlength(c)+TRACK for c in t))+2; h=int(PX*1.5)
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im); x=0
    for c in t:
        d.text((x,int(PX*0.18)),c,font=f,fill=COL); x+=f.getlength(c)+TRACK
    name=hashlib.sha1(t.encode()).hexdigest()[:10]+'.png'
    return im,name
def items(lst):
    out=[]
    for t in lst:
        im,name=render(t)
        if not DRY:
            os.makedirs(IMG,exist_ok=True); im.save(f'{IMG}/{name}',optimize=True)
        out.append(f'<img src="/img/clients/x/{name}" alt="" aria-hidden="true" draggable="false" loading="lazy" width="{im.width//S}" height="{im.height//S}">')
    return '<span class="kb22d">·</span>'.join(out)
CSS=('<style id="kb22-css">.kb22{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;margin:26px 0 0;'
     'user-select:none;-webkit-user-select:none}.kb22 .lb{text-transform:uppercase;letter-spacing:.14em;font-size:11px;'
     'color:var(--muted);font-family:var(--body);margin-right:4px}.kb22 img{display:block;height:19.5px;width:auto;'
     'pointer-events:none;-webkit-user-drag:none}.kb22d{color:var(--muted);font-size:13px}'
     '.lenders .kb22.bk{margin-top:22px}</style>')
def build():
    k=('<!--kb22--><div class="kb22" oncontextmenu="return false"><span class="lb" data-i18n="k294">Klien lainnya:</span>'
       +items(KLIEN)+'</div><!--/kb22-->')
    b=('<!--kb22b--><div class="kb22 bk" oncontextmenu="return false"><span class="lb">Bank lainnya:</span>'
       +items(BANK)+'</div><!--/kb22b-->')
    return k,b
def apply(p):
    s=open(p,encoding='utf-8').read(); o=s
    k,b=build()
    s=re.sub(r'<!--kb22-->.*?<!--/kb22-->',k,s,flags=re.S)
    s=re.sub(r'<p class="others"><span data-i18n="k294">Klien lainnya:</span>.*?</p>',k,s,count=1,flags=re.S)
    s=re.sub(r'<!--kb22b-->.*?<!--/kb22b-->','',s,flags=re.S)
    i=s.find('data-i18n="k266"')
    if i>0:
        j=s.find('</ul>',i)+5; s=s[:j]+b+s[j:]
    if 'id="kb22-css"' not in s: s=s.replace('</head>',CSS+'</head>',1)
    if s!=o:
        print('ubah',p)
        if not DRY: open(p,'w',encoding='utf-8').write(s)
    else: print('sama',p)
for p in ['out/faindonesia/layanan/index.html','FA-Indonesia_Website_SIAP-UPLOAD-v58/layanan/index.html']:
    apply(p)
