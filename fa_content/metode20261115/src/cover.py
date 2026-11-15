import numpy as np
from PIL import Image, ImageFilter
SRC='/home/claude/anantawsasongko/fa-websites/shared/unsplash/img/'
W,H=1654,2339  # A4 @200dpi
def hexrgb(h):h=h.lstrip('#');return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)
def make(src,out,dark,acc,focus=0.5,back=False):
    im=Image.open(SRC+src).convert('RGB')
    w,h=im.size; s=max(W/w,H/h); im=im.resize((int(w*s)+1,int(h*s)+1),Image.LANCZOS)
    x=int((im.width-W)*focus); im=im.crop((x,0,x+W,H))
    sharp=np.asarray(im.filter(ImageFilter.GaussianBlur(4)),float)
    blur=np.asarray(im.filter(ImageFilter.GaussianBlur(34)),float)
    yy=np.linspace(0,1,H)[:,None,None]
    # blur gradien: atas tajam sedikit, makin ke bawah makin blur
    mb=np.clip((yy-0.15)/0.55,0,1)
    img=sharp*(1-mb)+blur*mb
    # overexposure lembut
    g=img.mean(axis=2,keepdims=True)
    img=img*0.55+g*0.45
    img=np.clip(img*1.18+18,0,255)
    d=hexrgb(dark); a=hexrgb(acc)
    # duotone tint
    lum=img.mean(axis=2,keepdims=True)/255
    tint=d*(1-lum)+ (a*0.35+np.array([255,255,255])*0.65)*lum
    img=img*0.25+tint*0.75
    # overlay gelap atas -> memudar ke putih bawah
    if back:
        top=np.clip(1-yy/0.9,0,1)**0.8*0.85
        white=np.clip((yy-0.66)/0.20,0,1)**1.2
    else:
        top=0.30+np.clip(1-yy/0.58,0,1)**0.75*0.62
        white=np.clip((yy-0.58)/0.30,0,1)**1.3
    img=img*(1-top)+d*top
    img=img*(1-white)+255*white
    # vignette kiri halus
    xx=np.linspace(0,1,W)[None,:,None]
    v=np.clip(0.35-xx,0,1)*0.6*(1-white)
    img=img*(1-v)+d*v
    # noise
    rng=np.random.default_rng(7)
    n=rng.normal(0,9,(H,W,1))*(1-white*0.8)
    img=np.clip(img+n,0,255).astype('uint8')
    Image.fromarray(img).save(out,quality=88)
P=[('1521791136064-7986c2920216.jpg','ma','#141414','#E9B949',0.55),
   ('1554224155-6726b3ff858f.jpg','tp','#3E0D1A','#C8364F',0.45),
   ('1486406146926-c627a92ad1ab.jpg','fd','#0B3327','#2F9E74',0.5)]
for src,k,d,a,f in P:
    make(src,f'assets/cover-{k}.jpg',d,a,f)
    make(src,f'assets/back-{k}.jpg',d,a,1-f,back=True)
