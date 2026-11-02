// Susun PDF flow transaksi dari screenshot.
const { chromium } = require('playwright'); const fs = require('fs');
const S = [
 ['01-beranda', 'Pengunjung membuka faindonesia.co.id. Produk berbayar (aplikasi FA Jupiter dan e-book Penerbit FA) ada di menu Toko.'],
 ['02-toko', 'Halaman Toko menampilkan daftar produk, harga, dan metode pembayaran online lewat Midtrans.'],
 ['03-pilih-produk', 'Pembeli memilih produk dan menekan tombol Beli.'],
 ['04-halaman-bayar', 'Halaman Pembayaran terbuka dengan produk terpilih. Pembeli dapat mengubah produk dan jumlah.'],
 ['05-isi-data', 'Pembeli mengisi nama, email, dan nomor WhatsApp, menyetujui Syarat & Ketentuan, Kebijakan Privasi, dan Kebijakan Refund, lalu menekan Bayar Online.'],
 ['06-snap-metode', 'Jendela pembayaran Midtrans Snap terbuka. Pembeli memilih metode pembayaran.'],
 ['07-snap-va', 'Pembeli memilih bank virtual account, lalu Midtrans menampilkan nomor virtual account dan instruksi pembayaran. Setelah lunas, notifikasi Midtrans diterima server kami (faindonesia.co.id/api/pay/notify), kode akses aplikasi tampil di halaman konfirmasi dan e-book dikirim ke email pembeli.'],
];
(async () => {
  const items = S.filter(s => fs.existsSync(`midtrans/shots/${s[0]}.png`));
  const html = `<html><head><meta charset="utf-8"><style>body{font-family:Arial,sans-serif;color:#111;margin:0}
  .pg{page-break-after:always;padding:28px 34px}h1{font-size:22px;margin:0 0 6px}h2{font-size:15px;margin:0 0 8px}p{font-size:12.5px;line-height:1.5;margin:0 0 12px;color:#333}
  img{width:100%;border:1px solid #ccc}.meta{font-size:12px;color:#555}</style></head><body>
  <div class="pg"><h1>Alur Transaksi Pembelian Produk</h1><p class="meta">CV FA Indonesia · faindonesia.co.id · NIB 0208001900096<br>Dokumen flow transaksi untuk aktivasi Midtrans, dari pemilihan produk sampai checkout.</p>
  <p>Produk: aplikasi FA Jupiter · Laporan Keuangan - Audit Ready (day pass Rp39.000, tahunan Rp249.000, termasuk PPN) dan e-book Penerbit FA (PDF, Rp39.000 sampai Rp299.000). Pembayaran diproses Midtrans Snap. Screenshot diambil dari lingkungan sandbox.</p>
  <ol style="font-size:12.5px;line-height:1.6">${items.map(s => `<li>${s[1].split('.')[0]}.</li>`).join('')}</ol></div>
  ${items.map((s, i) => `<div class="pg"><h2>Langkah ${i + 1}</h2><p>${s[1]}</p><img src="file://${process.cwd()}/midtrans/shots/${s[0]}.png"></div>`).join('')}
  </body></html>`;
  fs.writeFileSync('midtrans/flow.html', html);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + process.cwd() + '/midtrans/flow.html'); await p.waitForTimeout(800);
  await p.pdf({ path: 'midtrans/Flow Transaksi CV FA Indonesia - Midtrans.pdf', format: 'A4', printBackground: true });
  await b.close(); console.log('pdf ok', items.length);
})();
