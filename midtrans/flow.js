// Ambil screenshot alur transaksi FA Indonesia sampai checkout Midtrans (sandbox) untuk dokumen onboarding Midtrans.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 860 }, deviceScaleFactor: 1 });
  const shot = async (n) => { await p.waitForTimeout(1200); await p.screenshot({ path: `midtrans/shots/${n}.png` }); console.log('shot', n); };
  fs.mkdirSync('midtrans/shots', { recursive: true });
  await p.goto('https://faindonesia.co.id/', { waitUntil: 'networkidle' }); await shot('01-beranda');
  await p.goto('https://faindonesia.co.id/toko/uji/', { waitUntil: 'networkidle' }); await shot('02-toko');
  const buy = p.locator('a[href*="bayar/uji/?produk=ar-year"], a[href*="bayar/uji/?produk="]').first();
  await buy.scrollIntoViewIfNeeded(); await p.evaluate(() => window.scrollBy(0, -200)); await shot('03-pilih-produk');
  await buy.click(); await p.waitForLoadState('networkidle'); await shot('04-halaman-bayar');
  await p.fill('#nm', 'Budi Santoso'); await p.fill('#co', 'PT Contoh Sukses Abadi'); await p.fill('#em', 'budi@contoh.co.id'); await p.fill('#ph', '081234567890');
  await p.check('#agree');
  await p.waitForSelector('#paynow', { state: 'visible', timeout: 20000 });
  await p.locator('#paynow').scrollIntoViewIfNeeded(); await shot('05-isi-data');
  const log = [];
  p.on('console', m => log.push('console ' + m.text())); p.on('response', async r => { if (r.url().includes('/api/pay/create')) { try { log.push('create ' + r.status() + ' ' + (await r.text()).slice(0, 300)); } catch (e) {} } });
  await p.click('#paynow');
  let f = null;
  try { await p.waitForSelector('#snap-midtrans', { timeout: 25000 }); await p.waitForTimeout(6000); f = p.frameLocator('#snap-midtrans'); }
  catch (e) {
    log.push('iframe tidak muncul, pakai redirect_url');
    const x = await p.evaluate(async () => (await fetch('/api/pay/create', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ prod: 'eb-paket', qty: '1', nm: 'Budi Santoso', co: 'PT Contoh Sukses Abadi', em: 'budi@contoh.co.id', ph: '081234567890', nt: '', desc: '', amt: '', agree: true, src: '' }) })).json());
    log.push(JSON.stringify(x).slice(0, 300));
    await p.goto(x.redirect_url, { waitUntil: 'networkidle' }); await p.waitForTimeout(5000);
    f = p;
  }
  fs.writeFileSync('midtrans/shots/log.txt', log.join('\n'));
  await shot('06-snap-metode');
  for (const t of ['Virtual account', 'Bank transfer', 'Transfer bank']) { try { await f.getByText(t, { exact: false }).first().click({ timeout: 4000 }); break; } catch (e) {} }
  await p.waitForTimeout(3000); await shot('07-snap-va');
  for (const t of ['BCA', 'BNI', 'Mandiri', 'BRI', 'Permata']) { try { await f.getByText(t, { exact: true }).first().click({ timeout: 3000 }); break; } catch (e) {} }
  await p.waitForTimeout(4000); await shot('08-snap-instruksi');
  fs.writeFileSync('midtrans/shots/log.txt', (fs.existsSync('midtrans/shots/log.txt')?fs.readFileSync('midtrans/shots/log.txt','utf8'):'')+'\nselesai');
  await b.close();
})().catch(e => { console.error(e); process.exit(0); });
