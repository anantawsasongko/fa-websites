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
  await p.click('#paynow');
  await p.waitForSelector('#snap-midtrans', { timeout: 30000 }); await p.waitForTimeout(6000); await shot('06-snap-metode');
  const f = p.frameLocator('#snap-midtrans');
  for (const t of ['Virtual account', 'Bank transfer', 'Transfer bank']) { try { await f.getByText(t, { exact: false }).first().click({ timeout: 4000 }); break; } catch (e) {} }
  await p.waitForTimeout(3000); await shot('07-snap-va');
  for (const t of ['BCA', 'BNI', 'Mandiri', 'BRI', 'Permata']) { try { await f.getByText(t, { exact: true }).first().click({ timeout: 3000 }); break; } catch (e) {} }
  await p.waitForTimeout(4000); await shot('08-snap-instruksi');
  await b.close();
})().catch(e => { console.error(e); process.exit(0); });
