#!/usr/bin/env python3
"""14 Nov 2026 (Bos): hero /apps/ diganti gaya noir FA (EB Garamond Italic + Poppins Light, logo asli, garis tipis).
Poin: dirancang akuntan lama di bisnis dan audit, CFO Fractional, migrasi Excel/single entry, sheet A-VD, Google Drive, SIMRS.
Tombol WA tidak lagi memakai nama dan gelar. Idempoten (penanda <!--fa-hero-noir-->), --dry."""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "out/faindonesia/apps/index.html"
DRY = "--dry" in sys.argv
WA = "https://wa.me/6282245260121?text=Halo%20FA%20Indonesia%2C%20saya%20ingin%20bertanya%20tentang%20FA%20Apps."

PTS = [
 ("Dirancang akuntan yang lama di bisnis dan audit.", "Alurnya otomatis dan mudah diikuti."),
 ("Ada CFO Fractional.", "Tanpa perlu training panjang."),
 ("Migrasi praktis lewat Excel,", "bahkan dari catatan single entry."),
 ("Sheet kode A sampai VD tersistemasi.", "Rapi dan siap diaudit."),
 ("Nyambung ke Google Drive.", "Satu folder bersama untuk seluruh tim."),
 ("Kuat sampai SIMRS.", "Sistem informasi paling kompleks pun kami kerjakan."),
]
pts = "".join(f'<li><i>{n:02d}</i><span><b>{a}</b> {b}</span></li>' for n,(a,b) in enumerate(PTS,1))

CSS = """<style id="fh-css">
.fh{position:relative;margin:0 0 40px;border:1px solid #2F2F2F;border-radius:6px;overflow:hidden;background:#04060B;color:#fff}
.fh:before{content:"";position:absolute;right:-12%;top:-45%;width:75%;height:140%;background:radial-gradient(closest-side,rgba(20,64,130,.55),rgba(4,6,11,0));pointer-events:none}
.fh:after{content:"";position:absolute;left:-14%;bottom:-40%;width:55%;height:100%;background:radial-gradient(closest-side,rgba(120,18,32,.32),rgba(4,6,11,0));pointer-events:none}
.fh .gr{position:absolute;inset:0;width:100%;height:100%;opacity:.08;mix-blend-mode:screen;pointer-events:none;z-index:1}
.fh-in{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.02fr);gap:44px;align-items:center;padding:52px 48px}
.fh-eb{margin:0 0 20px;font-size:11px;font-weight:300;letter-spacing:.28em;color:#9AA3B5;text-transform:uppercase}
.fh h1{margin:0 0 26px;font-family:"EB Garamond",Garamond,Georgia,serif;font-style:italic;font-weight:400;font-size:clamp(34px,4.6vw,58px);line-height:1.06;letter-spacing:-.005em;text-transform:none;color:#fff}
.fh ul{list-style:none;margin:0 0 28px;padding:0}
.fh li{display:flex;gap:16px;align-items:baseline;padding:11px 0;border-top:1px solid #2F2F2F;font-size:14.5px;line-height:1.55;font-weight:300;color:#C4CBDA}
.fh li:last-child{border-bottom:1px solid #2F2F2F}
.fh li i{flex:none;width:26px;font-style:normal;font-size:11px;letter-spacing:.14em;color:#00AAD6}
.fh li b{font-weight:500;color:#fff}
.fh-cta{display:flex;flex-wrap:wrap;gap:12px}
.fh-cta a{display:inline-flex;align-items:center;justify-content:center;height:46px;padding:0 24px;border-radius:3px;font-size:13px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;text-decoration:none}
.fh-cta .p{background:#fff;color:#04060B}
.fh-cta .w{border:1px solid #4A5163;color:#fff}
.fh-cta a:hover{opacity:.88}
.fh-win{background:#080B12;border:1px solid #2F2F2F;border-radius:4px;box-shadow:0 40px 90px rgba(0,0,0,.7),0 0 70px rgba(0,120,220,.12);overflow:hidden}
.fh-bar{display:flex;align-items:center;gap:7px;padding:10px 14px;border-bottom:1px solid #2F2F2F}
.fh-bar i{width:8px;height:8px;border-radius:50%;border:1px solid #4A5163}
.fh-bar span{margin-left:12px;font-size:10px;font-weight:300;letter-spacing:.1em;color:#9AA3B5}
.fh-body{display:flex;min-height:0}
.fh-side{width:128px;flex:none;border-right:1px solid #2F2F2F;padding:18px 14px;display:flex;flex-direction:column;gap:12px}
.fh-side img{height:44px;width:auto;align-self:flex-start;margin-bottom:10px}
.fh-side span{font-size:10px;font-weight:300;letter-spacing:.2em;color:#9AA3B5;text-transform:uppercase}
.fh-side span.on{font-weight:500;color:#fff;padding-bottom:8px;border-bottom:1px solid #00AAD6}
.fh-main{flex:1;min-width:0;padding:20px 22px;display:flex;flex-direction:column;gap:14px}
.fh-main small{display:block;font-size:9px;font-weight:300;letter-spacing:.18em;color:#9AA3B5;text-transform:uppercase}
.fh-t{font-family:"EB Garamond",Garamond,Georgia,serif;font-style:italic;font-size:26px;line-height:1.1;margin-top:4px;color:#fff}
.fh-k{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.fh-k small{letter-spacing:.06em;font-size:8.5px;overflow-wrap:anywhere}
.fh-k div,.fh-f,.fh-r{border:1px solid #2F2F2F}
.fh-k div{padding:11px 10px}
.fh-k b{display:block;margin-top:6px;font-size:21px;font-weight:300;color:#fff}
.fh-f{padding:12px 14px}
.fh-fs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-top:10px}
.fh-fs u{display:block;height:3px;text-decoration:none}
.fh-fs span{display:block;margin-top:6px;font-size:9px;font-weight:300;color:#C4CBDA}
.fh-r div{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-top:1px solid #2F2F2F;font-size:12px;font-weight:300;color:#fff}
.fh-r div:first-child{border-top:0}
.fh-r em{font-style:normal;padding:3px 12px;font-size:10px;font-weight:500;letter-spacing:.1em;text-transform:uppercase}
.fh-note{margin:12px 0 0;font-size:11px;font-weight:300;color:#7F889B;text-align:center}
@media(max-width:900px){.fh-in{grid-template-columns:1fr;padding:34px 20px;gap:30px}.fh-side{display:none}.fh-cta a{width:100%}}
</style>"""

HTML = f"""<!--fa-hero-noir-->{CSS}<section class="fh" aria-label="FA Apps"><svg class="gr" aria-hidden="true"><filter id="fhg"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0"/></filter><rect width="100%" height="100%" filter="url(#fhg)"/></svg><div class="fh-in"><div><p class="fh-eb">FA Apps · Since 2016</p><h1>Laporan keuangan yang siap diaudit, tersusun rapi sejak awal.</h1><ul>{pts}</ul><div class="fh-cta"><a class="p" href="#empat-app">Coba Gratis</a><a class="w" href="{WA}" rel="noopener" target="_blank">Chat via WhatsApp</a></div></div><div aria-hidden="true"><div class="fh-win"><div class="fh-bar"><i></i><i></i><i></i><span>faindonesia.co.id/saturn</span></div><div class="fh-body"><div class="fh-side"><img src="/img/brand/mark-hero.png" alt=""><span class="on">Saturn</span><span>Jupiter</span><span>Venus</span><span>Galaxy</span></div><div class="fh-main"><div><small>Penugasan audit · TB 2026</small><div class="fh-t">PT Contoh Jaya Tbk</div></div><div class="fh-k"><div><small>Materialitas</small><b>250 jt</b></div><div><small>Akun diuji</small><b>18</b></div><div><small>Sign-off</small><b>3 / 5</b></div></div><div class="fh-f"><small>Alur audit</small><div class="fh-fs"><div><u style="background:#4F8CFF"></u><span>01 Planning</span></div><div><u style="background:#B07CF5"></u><span>02 Risiko</span></div><div><u style="background:#19B5A5"></u><span>03 Respons</span></div><div><u style="background:#2F2F2F"></u><span>04 Pelaporan</span></div></div></div><div class="fh-r"><div>Pendapatan<em style="background:#E03A3E;color:#fff">Tinggi</em></div><div>Persediaan<em style="background:#F2C230;color:#1a1400">Sedang</em></div><div>Kas dan Bank<em style="background:#1F9D55;color:#fff">Rendah</em></div></div></div></div></div><p class="fh-note">Contoh tampilan dengan data dummy.</p></div></div></section><!--/fa-hero-noir-->"""

t = F.read_text(encoding="utf-8")
if "<!--fa-hero-noir-->" in t:
    new = re.sub(r"<!--fa-hero-noir-->.*?<!--/fa-hero-noir-->", lambda m: HTML, t, flags=re.S)
else:
    new, n = re.subn(r'<section class="sx-hero".*?</section>', lambda m: HTML, t, count=1, flags=re.S)
    assert n == 1, "hero lama tidak ketemu"
new = new.replace(">Chat Ananta, CPA<", ">Chat via WhatsApp<")
print("berubah" if new != t else "tidak berubah (sudah)")
if not DRY and new != t:
    F.write_text(new, encoding="utf-8")
