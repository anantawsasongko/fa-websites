import sys, importlib, asyncio
from tpl import page
from playwright.async_api import async_playwright
MODS={'m1_ma':'FA-Modul-01_Merger-dan-Akuisisi.pdf','m2_tp':'FA-Modul-02_Transfer-Pricing.pdf','m3_fd':'FA-Modul-03_Pendanaan-dan-Investor.pdf'}
async def main(keys):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page()
        for k in keys:
            m=importlib.import_module(k).M
            html=page(m); open(f'out/{k}.html','w').write(html)
            await pg.goto(f'file:///home/claude/ebook/out/{k}.html'); await pg.wait_for_load_state('networkidle')
            await pg.pdf(path='out/'+MODS[k],prefer_css_page_size=True,print_background=True)
            from pypdf import PdfReader, PdfWriter
            r=PdfReader('out/'+MODS[k]); w=PdfWriter(clone_from=r)
            w.add_metadata({'/Title':m['title_plain']+' | Modul FA Indonesia','/Author':'Dr. (C) Ananta W. Sasongko, S.E., M.S.A., Ak., CPA, CTT, FMVA, FPAP','/Subject':m['sub'],'/Creator':'FA Indonesia'})
            w.write('out/'+MODS[k])
            print('ok',MODS[k])
        await b.close()
asyncio.run(main(sys.argv[1:]))
