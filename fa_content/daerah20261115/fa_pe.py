# -*- coding: utf-8 -*-
"""FA Indonesia: 3 artikel pendanaan RS dari private equity dan venture capital global (Jakarta, Denpasar, Batam)."""
from _k import A, n, rp, jt, pct, tbl

S_KEK = ('Bisnis.com: Warga RI Banyak Berobat ke Luar Negeri, KEK Disiapkan Jadi Pusat Kesehatan (12 Mei 2026)', 'https://ekonomi.bisnis.com/read/20260512/12/1973351/warga-ri-banyak-berobat-ke-luar-negeri-kek-disiapkan-jadi-pusat-kesehatan')
S_QUAD = ('Business Wire: Quadria Capital Closes Oversubscribed US$1 Billion Fund III (26 Mei 2025)', 'https://www.businesswire.com/news/home/20250526754879/en/Quadria-Capital-Closes-Oversubscribed-US%241-Billion-Fund-III-to-Advance-Healthcare-Transformation-Across-Asia')
S_BAIN = ('DealStreetAsia: Bain Capital Invests $157m in Indonesia\'s Mayapada Hospital', 'https://dealstreetasia.com/?p=422134')
S_DDTC = ('DDTCNews: Devisa Rp170 Triliun Hilang karena WNI Berobat ke Luar Negeri (14 Juni 2023)', 'https://news.ddtc.co.id/berita/nasional/1795060/jokowi-devisa-rp-170-triliun-hilang-karena-wni-berobat-ke-luar-negeri')
S_PMK6 = ('Permenkes Nomor 6 Tahun 2026 tentang Rumah Sakit (teks pada Pasal.id)', 'https://pasal.id/peraturan/permen/permenkes-no-6-tahun-2026')
S_HOL = ('Hukumonline: Panduan Praktis Perizinan Rumah Sakit (UU 17/2023 Pasal 185)', 'https://www.hukumonline.com/berita/a/panduan-praktis-perizinan-rumah-sakit-lt677e40e5c4e8a?page=all')
S_PMK1 = ('Permenkes Nomor 1 Tahun 2023 tentang Penyelenggaraan Kegiatan Usaha Rumah Sakit di Kawasan Ekonomi Khusus', 'https://jdih.kemkes.go.id/common/dokumen/2023permenkes001.pdf')

M = 1e9
# ------------------------------------------------------------------ 4. Jakarta
EB = 54 * M
ADJ = [('Biaya pribadi pemegang saham yang dibebankan ke rumah sakit', 3 * M), ('Biaya renovasi yang sekali terjadi', 4 * M),
       ('Sewa tanah dari pihak berelasi di bawah harga pasar', -5 * M), ('Klaim tertunda yang kemungkinan tidak terbayar', -4 * M)]
EBN = EB + sum(v for _, v in ADJ); MULT = 11; EV = EBN * MULT
ND = [('Utang bank', 140 * M), ('Liabilitas sewa pembiayaan alat medis', 12 * M), ('Jasa medis dan utang pajak yang lewat jatuh tempo', 8 * M), ('Kas dan setara kas', -20 * M)]
NDT = sum(v for _, v in ND); EQ = EV - NDT; INV = 150 * M; POST = EQ + INV; SH = INV / POST
sg = lambda v: ('+' if v > 0 else '-') + jt(abs(v))
lp_rows = []
for ex in (500 * M, 800 * M, 1200 * M):
    pr = SH * ex; npart = max(INV, pr); part = INV + SH * (ex - INV)
    lp_rows.append([jt(ex), jt(pr, 1), jt(npart, 1), jt(ex - npart, 1), jt(part, 1), jt(ex - part, 1)])

A(site='fa', topik='pe', kota='Jakarta', kota_slug='jakarta',
  slug='private-equity-global-rumah-sakit-jakarta-valuasi-term-sheet',
  seo_title='Private Equity Global Masuk Rumah Sakit Jakarta: Valuasi',
  title='Private Equity Global Masuk Rumah Sakit di Jakarta: Valuasi, Term Sheet, dan Hak Investor',
  description='Cara private equity global menilai rumah sakit di Jakarta: normalisasi EBITDA, kelipatan EV/EBITDA, utang bersih, dilusi, dan pasal term sheet.',
  keyword='private equity rumah sakit', category='Rumah Sakit',
  cta={'href': '/pendanaan-rumah-sakit/jakarta/', 'label': 'Pendanaan Rumah Sakit Jakarta'},
  wa='Halo Pak Ananta, kami pemilik rumah sakit di Jakarta dan ingin diskusi kesiapan menerima investor private equity.',
  related=['private-equity-vs-utang-bank', 'indikator-keuangan-rumah-sakit-yang-dilihat-investor', 'valuasi-rumah-sakit-swasta', 'due-diligence-investor-yang-perlu-disiapkan', 'rumah-sakit-sesak-napas-pendanaan'],
  sources=[S_QUAD, S_BAIN, S_DDTC, S_KEK, S_PMK6, S_HOL],
  body_html=f'''
<p>Dana private equity (PE) yang khusus membidik layanan kesehatan di Asia terus membesar. Quadria Capital, misalnya, menutup dana ketiganya pada 2025 dengan komitmen US$1,07 miliar. Bain Capital juga mengumumkan rencana investasi US$157 juta di induk salah satu jaringan rumah sakit yang berbasis di Jakarta. Rumah sakit Indonesia sudah masuk peta investor global.</p>
<p>Jakarta menjadi pintu masuknya. Pada 2023 Presiden menyebut sekitar 60 persen warga yang berobat ke luar negeri berasal dari Jakarta, dan pemerintah memperkirakan belanja berobat ke luar negeri mencapai kira-kira Rp150 triliun per tahun. Bagi investor, itu permintaan layanan premium yang belum terlayani di dalam negeri. Bagi pemilik rumah sakit, pertanyaannya: berapa nilai rumah sakit saya di mata mereka, dan hak apa yang mereka minta?</p>
<h2>Apa yang Dicari Private Equity pada Rumah Sakit</h2>
<ul>
<li><b>Platform, bukan satu gedung.</b> Dua sampai lima rumah sakit dengan manajemen terpusat lebih menarik daripada satu rumah sakit besar yang bergantung pada pendirinya.</li>
<li><b>Bauran penjamin.</b> Porsi pasien umum dan asuransi swasta, dan margin kasus JKN setelah dihitung dengan unit cost.</li>
<li><b>Layanan unggulan.</b> Jantung, onkologi, ortopedi, ibu dan anak, dengan dokter yang terikat kontrak jelas.</li>
<li><b>Ruang tumbuh.</b> Lahan, izin, dan kapasitas yang bisa ditambah dengan dana baru.</li>
<li><b>Laporan keuangan yang bisa diuji.</b> Diaudit kantor akuntan publik, dengan rincian per unit layanan.</li>
</ul>
<h2>Dari EBITDA ke Nilai Ekuitas: Contoh Hitung</h2>
<p>Ilustrasi berikut memakai angka contoh sebuah rumah sakit 150 tempat tidur dengan pendapatan Rp300 miliar. Langkah pertama investor adalah menormalisasi EBITDA yang dilaporkan.</p>
{tbl(['Normalisasi EBITDA', 'Nilai'], [['EBITDA menurut laporan manajemen', jt(EB)]] + [[a, sg(v)] for a, v in ADJ], ['EBITDA setelah normalisasi', jt(EBN)])}
<p>Dengan kelipatan EV/EBITDA {MULT} kali (hanya ilustrasi), nilai perusahaan (enterprise value) = {jt(EBN)} x {MULT} = {jt(EV)}. Nilai ini belum menjadi hak pemegang saham karena masih harus dikurangi utang bersih.</p>
{tbl(['Utang bersih', 'Nilai'], [[a, jt(v)] for a, v in ND], ['Utang bersih', jt(NDT)])}
<p>Nilai ekuitas sebelum dana masuk (pre-money) = {jt(EV)} dikurangi {jt(NDT)} = <b>{jt(EQ)}</b>. Bila investor menyetor dana baru {jt(INV)} untuk ekspansi, nilai setelah dana masuk (post-money) {jt(POST)} dan porsi investor {jt(INV)} / {jt(POST)} = <b>{pct(SH)}</b>. Kepemilikan pendiri turun menjadi {pct(1 - SH)}.</p>
<p>Perhatikan dua hal. Setiap Rp1 miliar penyesuaian EBITDA menggeser nilai ekuitas Rp{MULT} miliar. Dan pos seperti jasa medis yang tertunggak diperlakukan sebagai utang, bukan modal kerja. Kelipatan pada transaksi nyata bergantung pada ukuran, pertumbuhan, bauran penjamin, dan kondisi pasar saat itu.</p>
<h2>Pasal Term Sheet yang Menggeser Nilai</h2>
<p>Harga hanya separuh cerita. Hak yang melekat pada saham investor bisa mengubah pembagian hasil saat exit. Contoh paling jelas adalah hak didahulukan saat likuidasi atau penjualan (liquidation preference).</p>
{tbl(['Nilai ekuitas saat exit', 'Pro rata investor', 'Investor, preferensi 1x tidak berpartisipasi', 'Pendiri', 'Investor, preferensi 1x berpartisipasi', 'Pendiri'], lp_rows)}
<p>Pada preferensi yang tidak berpartisipasi, investor memilih yang lebih besar antara dana pokoknya dan porsi pro rata. Pada preferensi yang berpartisipasi, investor mengambil dana pokok lebih dulu lalu ikut membagi sisanya. Selisih bagi pendiri pada exit Rp1,2 triliun mencapai lebih dari Rp110 miliar, tanpa satu angka pun berubah di valuasi.</p>
<div class="pf-fold"><p>Pasal lain yang perlu dibaca bersama penasihat hukum dan penasihat keuangan:</p>
<ul>
<li><b>Hal yang butuh persetujuan investor (reserved matters):</b> anggaran, belanja modal di atas batas tertentu, utang baru, pengangkatan direksi keuangan.</li>
<li><b>Anti-dilusi:</b> penyesuaian harga bila putaran berikutnya lebih murah.</li>
<li><b>Drag along dan tag along:</b> hak memaksa atau ikut menjual saat ada pembeli.</li>
<li><b>Opsi jual (put option) atau jaminan imbal hasil:</b> kewajiban pendiri membeli kembali bila exit tidak tercapai. Di laporan keuangan, pasal ini bisa membuat dana investor dicatat sebagai liabilitas.</li>
<li><b>Earn-out:</b> sebagian harga dibayar bila target EBITDA tercapai.</li>
<li><b>Pernyataan dan jaminan:</b> pajak, klaim, perizinan, dan sengketa medis.</li>
</ul></div>
<h2>Struktur dan Regulasi yang Perlu Dicek Sejak Awal</h2>
<ul>
<li>Rumah sakit yang didirikan masyarakat harus berbentuk badan hukum yang kegiatan usahanya hanya di bidang pelayanan kesehatan. Rumah sakit yang masih berada di bawah perusahaan dengan banyak bidang usaha perlu dipisahkan dulu.</li>
<li>Masuknya investor asing menjadikan perusahaan berstatus penanaman modal asing. Permenkes 6 Tahun 2026 mengatur syarat tempat tidur dan tingkat layanan bagi rumah sakit dengan modal asing. Batas kepemilikan asing mengikuti ketentuan bidang usaha penanaman modal yang berlaku saat transaksi, dan itu pekerjaan konsultan hukum.</li>
<li>Tanah dan bangunan atas nama pribadi atau perusahaan lain perlu diputuskan: dimasukkan ke perusahaan, atau disewa dengan kontrak jangka panjang berharga pasar.</li>
</ul>
<h2>Enam Bulan Sebelum Bicara dengan Investor</h2>
<ol>
<li>Audit laporan keuangan dua sampai tiga tahun terakhir.</li>
<li>Susun laba rugi per unit layanan dan per penjamin.</li>
<li>Rapikan kontrak dokter, kerja sama alat, dan sewa.</li>
<li>Bersihkan piutang klaim: mana yang tertunda, mana yang ditolak.</li>
<li>Siapkan rencana penggunaan dana dan proyeksi lima tahun yang bisa dipertanggungjawabkan.</li>
<li>Hitung sendiri valuasi indikatif supaya tidak datang ke meja perundingan tanpa angka.</li>
</ol>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Pemilik rumah sakit di Jakarta dan sekitarnya didampingi tim FA Indonesia dari sisi pemilik: normalisasi EBITDA, valuasi indikatif dengan <a href="/kalkulator-valuasi-rumah-sakit/">kalkulator valuasi rumah sakit FA Venus</a>, penyiapan data room, sampai pendampingan saat uji tuntas. Tim pernah mendampingi pendanaan investor untuk grup rumah sakit dan akuisisi rumah sakit di Jawa Tengah. Lihat <a href="/pendanaan-rumah-sakit/jakarta/">pendanaan rumah sakit di Jakarta</a>, <a href="/konsultan-rumah-sakit/jakarta/">konsultan rumah sakit Jakarta</a>, dan <a href="/artikel/private-equity-vs-utang-bank/">perbandingan private equity dan utang bank</a>.</p>
''',
  faq=[('Bagaimana private equity menilai rumah sakit?', 'Umumnya dengan kelipatan EV/EBITDA atas EBITDA yang sudah dinormalisasi, diuji silang dengan arus kas terdiskonto. Nilai perusahaan lalu dikurangi utang bersih untuk mendapat nilai ekuitas.'),
       ('Apa itu normalisasi EBITDA?', 'Penyesuaian EBITDA atas pos yang tidak mencerminkan kinerja berulang, misalnya biaya pribadi pemilik, biaya sekali terjadi, sewa pihak berelasi yang tidak sesuai harga pasar, dan klaim yang kemungkinan tidak terbayar.'),
       ('Apakah investor asing boleh memiliki rumah sakit di Indonesia?', 'Boleh dalam bentuk penanaman modal asing dengan syarat yang diatur, termasuk syarat tempat tidur dan tingkat layanan dalam Permenkes 6 Tahun 2026. Batas kepemilikan mengikuti ketentuan penanaman modal yang berlaku saat transaksi.'),
       ('Berapa lama proses dari perkenalan sampai dana masuk?', 'Untuk transaksi rumah sakit menengah, enam sampai dua belas bulan adalah rentang yang wajar, bergantung pada kesiapan laporan keuangan dan dokumen.')])

# ------------------------------------------------------------------ 5. Denpasar
I0 = 100 * M; IRR = .20; YR = 5; STK = .30; ND2 = 150 * M; MX = 10; EB0 = 40 * M
PROC = I0 * (1 + IRR) ** YR; EQX = PROC / STK; EVX = EQX + ND2; EBX = EVX / MX; CAGR = (EBX / EB0) ** (1 / YR) - 1

A(site='fa', topik='pe', kota='Denpasar', kota_slug='denpasar',
  slug='pendanaan-rumah-sakit-bali-private-equity-venture-capital',
  seo_title='Pendanaan Rumah Sakit Bali dari Private Equity dan VC',
  title='Pendanaan Rumah Sakit dan Klinik di Bali dari Private Equity dan Venture Capital Global',
  description='KEK Sanur menaruh Bali di peta investor kesehatan. Ini cara private equity dan venture capital global memilih rumah sakit dan klinik di Denpasar.',
  keyword='pendanaan rumah sakit bali', category='Rumah Sakit',
  cta={'href': '/pendanaan-rumah-sakit/denpasar/', 'label': 'Pendanaan Rumah Sakit Denpasar'},
  wa='Halo Pak Ananta, kami pemilik rumah sakit atau klinik di Bali dan ingin diskusi pendanaan dari investor.',
  related=['rumah-sakit-future-proof-medical-tourism-layanan-unggulan', 'private-equity-vs-utang-bank', 'indikator-keuangan-rumah-sakit-yang-dilihat-investor', 'rumah-sakit-sesak-napas-pendanaan'],
  sources=[('Kontan: Prabowo Resmikan KEK Khusus Kesehatan di Sanur Bali (25 Juni 2025)', 'https://nasional.kontan.co.id/news/prabowo-resmikan-kek-khusus-kesehatan-di-sanur-bali'),
           ('RMOL: Prabowo Resmikan KEK Kesehatan Sanur Pertama di Indonesia (25 Juni 2025)', 'https://rmol.id/dunia/read/2025/06/25/671207/prabowo-resmikan-kek-kesehatan-sanur-pertama-di-indonesia'),
           ('Industry.co.id: KEK Sanur Kantongi Investasi Rp5,34 Triliun, Bidik Pasar Wisata Kesehatan', 'https://www.industry.co.id/read/157042/kek-sanur-kantongi-investasi-rp534-triliun-bidik-pasar-wisata-kesehatan'),
           S_PMK1, S_KEK, S_QUAD],
  body_html=f'''
<p>Sejak Kawasan Ekonomi Khusus (KEK) Sanur dan Bali International Hospital diresmikan pada 25 Juni 2025, Denpasar punya rumah sakit 255 tempat tidur yang dibangun untuk menahan pasien Indonesia agar tidak berobat ke luar negeri. Sampai kuartal II 2026 pengelola kawasan mencatat realisasi investasi kumulatif sekitar Rp5,34 triliun dengan 15 penyewa.</p>
<p>Dampaknya tidak berhenti di dalam pagar kawasan. Investor yang datang melihat Sanur ikut melihat rumah sakit swasta, klinik estetik, fertilitas, gigi, dan wellness di Denpasar, Badung, dan Gianyar. Sebagian datang dari dana private equity (PE) kesehatan regional, sebagian dari venture capital (VC) yang membidik jaringan klinik.</p>
<h2>Siapa Investor yang Datang dan Apa yang Mereka Cari</h2>
{tbl(['Jenis investor', 'Sasaran di Bali', 'Bentuk dana', 'Yang biasanya diminta'],
     [['Private equity kesehatan', 'Rumah sakit umum dan khusus yang sudah menghasilkan laba', 'Saham minoritas besar atau mayoritas, lima sampai tujuh tahun', 'Kursi dewan, hak persetujuan anggaran, jalur exit'],
      ['Investor strategis (operator rumah sakit)', 'Rumah sakit dengan lokasi dan izin yang sulit diulang', 'Akuisisi mayoritas atau kerja sama operasi', 'Kendali manajemen dan merek'],
      ['Venture capital', 'Jaringan klinik estetik, gigi, fertilitas, wellness, dan layanan digital', 'Saham minoritas bertahap per putaran', 'Pertumbuhan cabang, hak informasi, hak ikut putaran berikutnya'],
      ['Lembaga pembiayaan pembangunan dan dana dampak', 'Layanan ibu dan anak, layanan untuk masyarakat menengah bawah', 'Saham, pinjaman jangka panjang, atau gabungan', 'Standar lingkungan, sosial, dan tata kelola serta pelaporan dampak']])}
<h2>Yang Khas dari Rumah Sakit dan Klinik di Bali</h2>
<ul>
<li><b>Pasien wisatawan dan ekspatriat.</b> Pendapatan dari asuransi perjalanan dan asuransi kesehatan internasional lebih tinggi per kasus, tetapi penagihannya lebih lama dan sebagian dalam valuta asing.</li>
<li><b>Musiman.</b> Okupansi mengikuti musim kunjungan. Investor akan meminta data bulanan minimal tiga tahun, termasuk masa pandemi dan pemulihannya.</li>
<li><b>Tenaga medis asing.</b> Aturan kesehatan terbaru membuka ruang lebih lebar, terutama di kawasan ekonomi khusus. Di luar kawasan, perizinannya tetap perlu dipastikan satu per satu.</li>
<li><b>Lahan.</b> Banyak fasilitas berdiri di atas tanah sewa jangka panjang. Sisa masa sewa memengaruhi nilai secara langsung.</li>
<li><b>Layanan non-medis.</b> Wellness dan estetik sering bercampur dalam satu badan usaha dengan layanan medis. Investor meminta pemisahan yang jelas.</li>
</ul>
<h2>Berhitung dari Sisi Investor</h2>
<p>Cara tercepat memahami tawaran investor adalah menghitung dari sisi mereka. Ilustrasi dengan angka contoh: dana PE masuk {jt(I0)} untuk porsi {pct(STK, 0)}, dengan sasaran imbal hasil {pct(IRR, 0)} per tahun selama {YR} tahun.</p>
{tbl(['Langkah', 'Perhitungan', 'Hasil'],
     [['Dana yang harus kembali saat exit', f'{jt(I0)} x (1 + {pct(IRR, 0)}) pangkat {YR}', jt(PROC, 1)],
      ['Nilai ekuitas yang dibutuhkan', f'{jt(PROC, 1)} / {pct(STK, 0)}', jt(EQX, 1)],
      ['Nilai perusahaan yang dibutuhkan', f'{jt(EQX, 1)} + utang bersih {jt(ND2)}', jt(EVX, 1)],
      ['EBITDA yang dibutuhkan saat exit', f'{jt(EVX, 1)} / {MX} kali', jt(EBX, 1)]])}
<p>Bila EBITDA hari ini {jt(EB0)}, rumah sakit harus tumbuh rata-rata {pct(CAGR)} per tahun selama lima tahun agar hitungan investor tercapai. Dari sinilah datang pertanyaan mereka tentang tambahan tempat tidur, layanan baru, dan cabang. Pemilik yang sudah memegang angka ini bisa menilai sendiri apakah rencana pertumbuhannya masuk akal sebelum menandatangani target dalam perjanjian.</p>
<p>Untuk VC, logikanya serupa tetapi bertumpu pada pertumbuhan cabang dan ekonomi per cabang: biaya membuka satu klinik, bulan mencapai impas, dan margin setelah matang.</p>
<h2>Struktur Transaksi yang Umum Dipakai</h2>
<div class="pf-fold"><ul>
<li><b>Penyertaan saham baru.</b> Dana masuk ke perusahaan untuk ekspansi, pemilik lama terdilusi tetapi tidak menerima uang tunai.</li>
<li><b>Penjualan sebagian saham lama.</b> Pemilik menerima dana, perusahaan tidak. Sering digabung dengan penyertaan baru.</li>
<li><b>Pemisahan operasional dan properti.</b> Tanah dan bangunan ditaruh di perusahaan terpisah yang menyewakan ke perusahaan operasional. Investor bisa masuk di salah satunya.</li>
<li><b>Pinjaman konversi.</b> Pinjaman yang dapat diubah menjadi saham pada putaran berikutnya, umum pada tahap awal jaringan klinik.</li>
</ul>
<p>Begitu investor asing masuk, perusahaan menjadi penanaman modal asing dengan kewajiban tambahan: laporan kegiatan penanaman modal, dokumentasi transaksi pihak berelasi, dan syarat rumah sakit bermodal asing dalam Permenkes 6 Tahun 2026. Untuk rumah sakit di dalam KEK berlaku pula Permenkes 1 Tahun 2023.</p></div>
<h2>Kesiapan yang Diperiksa Investor</h2>
<ul>
<li>Laporan keuangan diaudit, dengan pendapatan dipilah per penjamin dan per mata uang.</li>
<li>Umur piutang asuransi dan tingkat penolakan klaim.</li>
<li>Kontrak dokter, termasuk dokter asing bila ada.</li>
<li>Perizinan, akreditasi, dan status lahan.</li>
<li>Laba rugi per layanan yang ditopang perhitungan unit cost.</li>
</ul>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Pemilik rumah sakit dan klinik di Denpasar, Badung, dan Gianyar didampingi tim FA Indonesia untuk menyiapkan laporan keuangan, valuasi indikatif, proyeksi, dan data room sebelum bertemu investor, lalu mendampingi selama uji tuntas. Bagi perusahaan yang sudah berstatus penanaman modal asing tersedia layanan <a href="/fractional-cfo-pt-pma-bali/">fractional CFO untuk PT PMA di Bali</a>. Lihat juga <a href="/pendanaan-rumah-sakit/denpasar/">pendanaan rumah sakit di Denpasar</a> dan <a href="/konsultan-rumah-sakit/denpasar/">konsultan rumah sakit Denpasar</a>.</p>
''',
  faq=[('Apakah rumah sakit di luar KEK Sanur bisa menerima investor asing?', 'Bisa, melalui penanaman modal asing dengan syarat yang berlaku umum, termasuk syarat rumah sakit bermodal asing dalam Permenkes 6 Tahun 2026. Fasilitas khusus KEK hanya berlaku di dalam kawasan.'),
       ('Apa beda private equity dan venture capital untuk layanan kesehatan?', 'Private equity biasanya masuk ke rumah sakit yang sudah menghasilkan laba dengan porsi saham besar. Venture capital masuk lebih awal ke jaringan klinik atau layanan digital yang sedang tumbuh, dengan porsi minoritas bertahap.'),
       ('Berapa imbal hasil yang diharapkan investor?', 'Setiap dana punya sasaran sendiri. Yang penting bagi pemilik adalah menghitung pertumbuhan EBITDA yang dibutuhkan agar sasaran itu tercapai, lalu menilai apakah realistis.'),
       ('Dokumen apa yang pertama kali diminta?', 'Laporan keuangan diaudit tiga tahun, data operasional bulanan, daftar perizinan, kontrak dokter, dan status lahan.')])

# ------------------------------------------------------------------ 6. Batam
PEG = 18.0 * M; ACT = 14.5 * M

A(site='fa', topik='pe', kota='Batam', kota_slug='batam',
  slug='investor-asing-rumah-sakit-batam-due-diligence-data-room',
  seo_title='Investor Asing Rumah Sakit Batam: Due Diligence, Data Room',
  title='Investor Asing Melirik Rumah Sakit di Batam: Menyiapkan Due Diligence dan Data Room',
  description='Batam punya KEK kesehatan internasional. Ini isi data room, pos setara utang, dan penyesuaian modal kerja yang diperiksa investor saat due diligence.',
  keyword='due diligence rumah sakit', category='Rumah Sakit',
  cta={'href': '/pendanaan-rumah-sakit/batam/', 'label': 'Pendanaan Rumah Sakit Batam'},
  wa='Halo Pak Ananta, kami pemilik rumah sakit di Batam dan ingin menyiapkan data room serta due diligence untuk calon investor.',
  related=['due-diligence-akuisisi-rumah-sakit-swasta', 'due-diligence-investor-yang-perlu-disiapkan', 'menjual-rumah-sakit-persiapan-sisi-penjual', 'valuasi-rumah-sakit-swasta', 'piutang-klaim-bpjs-dan-arus-kas-rumah-sakit'],
  sources=[('CNN Indonesia: Mayapada Resmi Bangun RS Internasional di Batam (28 Agustus 2025)', 'https://www.cnnindonesia.com/ekonomi/20250828045120-92-1267223/mayapada-resmi-bangun-rs-internasional-di-batam/amp'),
           S_BAIN, S_DDTC, S_KEK, S_PMK6],
  body_html=f'''
<p>Batam berjarak sekitar satu jam penyeberangan dari Singapura, dan selama ini termasuk daerah asal warga yang berobat ke luar negeri. Pemerintah menjawabnya dengan Kawasan Ekonomi Khusus Pariwisata dan Kesehatan Internasional Batam di Sekupang. Pada 27 Agustus 2025 sebuah rumah sakit internasional hasil kerja sama grup rumah sakit nasional dan operator dari India mulai dibangun di sana, dengan target selesai akhir 2027.</p>
<p>Kehadiran pemain besar membuat investor ikut memetakan rumah sakit yang sudah beroperasi di Batam, Tanjungpinang, dan Karimun. Bagi pemilik, tawaran pertama hampir selalu diikuti satu kata: due diligence. Artikel ini menjelaskan apa yang diperiksa dan bagaimana menyiapkannya agar harga tidak turun di tengah jalan.</p>
<h2>Lima Jalur Pemeriksaan</h2>
{tbl(['Jalur', 'Yang diperiksa', 'Temuan yang sering menurunkan harga'],
     [['Keuangan', 'Kualitas laba, utang bersih, modal kerja, belanja modal', 'EBITDA turun setelah normalisasi, piutang klaim macet'],
      ['Pajak', 'PPh badan, PPh 21 dokter, PPN atas obat dan layanan non-medis', 'Pajak jasa dokter yang tidak dipotong sesuai ketentuan'],
      ['Hukum', 'Perizinan, akreditasi, kepemilikan lahan, kontrak, sengketa', 'Tanah atas nama pribadi, kontrak dokter tidak tertulis'],
      ['Komersial', 'Pangsa pasar, pesaing, bauran penjamin, rujukan', 'Ketergantungan pada satu dua dokter atau satu penjamin'],
      ['Klinis dan operasional', 'Mutu, keselamatan pasien, utilisasi, SIMRS', 'Data layanan tidak cocok dengan data keuangan']])}
<h2>Isi Data Room yang Diminta</h2>
<ol>
<li><b>Korporasi:</b> akta dan perubahannya, daftar pemegang saham, struktur grup, risalah rapat.</li>
<li><b>Perizinan:</b> perizinan berusaha, izin operasional, sertifikat akreditasi, izin alat dan limbah.</li>
<li><b>Keuangan:</b> laporan keuangan diaudit tiga tahun, laporan manajemen bulanan 24 sampai 36 bulan, buku besar, anggaran.</li>
<li><b>Pendapatan:</b> rincian per unit layanan, per penjamin, dan per dokter, berikut umur piutang dan status klaim.</li>
<li><b>Biaya:</b> daftar pegawai dan remunerasi, skema jasa medis, kontrak pemasok obat dan alat.</li>
<li><b>Aset:</b> sertifikat tanah, daftar aset tetap, kontrak sewa dan kerja sama operasi alat.</li>
<li><b>Pajak:</b> SPT tiga sampai lima tahun, surat ketetapan, dan korespondensi pemeriksaan.</li>
<li><b>Hukum:</b> perkara berjalan, pengaduan pasien, polis asuransi.</li>
</ol>
<p>Di Batam ada tambahan yang khas: status lahan di bawah hak pengelolaan Badan Pengusahaan Batam beserta kewajiban uang wajib tahunan dan masa berlakunya, serta perlakuan fasilitas kawasan perdagangan bebas atas pembelian alat dan obat.</p>
<h2>Kualitas Laba: Pos yang Hampir Selalu Disesuaikan</h2>
<ul>
<li>Pendapatan klaim yang diakui penuh padahal sebagian tertunda atau dalam sengketa.</li>
<li>Jasa medis yang dicatat saat dibayar, bukan saat layanan diberikan.</li>
<li>Persediaan farmasi yang tidak pernah dihitung fisik dan obat kedaluwarsa yang belum dihapus.</li>
<li>Biaya pemilik dan keluarga yang dibebankan ke rumah sakit.</li>
<li>Sewa dari pihak berelasi yang tidak sesuai harga pasar.</li>
</ul>
<h2>Pos Setara Utang dan Penyesuaian Modal Kerja</h2>
<p>Harga yang disepakati biasanya berbasis nilai perusahaan tanpa kas dan tanpa utang. Yang sering mengejutkan pemilik adalah pos yang oleh investor diperlakukan setara utang: jasa medis tertunggak, utang pajak, uang muka pasien, liabilitas imbalan kerja, dan belanja modal yang sudah dijanjikan tetapi belum dibayar.</p>
<p>Satu mekanisme lagi adalah penyesuaian modal kerja. Kedua pihak menyepakati modal kerja normal, biasanya rata-rata 12 bulan. Dalam ilustrasi dengan angka contoh, modal kerja normal {jt(PEG)} sedangkan pada tanggal penutupan hanya {jt(ACT)}. Selisih {jt(PEG - ACT)} mengurangi harga yang diterima penjual, rupiah demi rupiah.</p>
<div class="pf-fold"><p>Karena itu, menahan pembayaran pemasok atau mempercepat penagihan menjelang penutupan tidak menambah uang penjual. Yang menambah adalah modal kerja yang memang sehat sepanjang tahun: klaim diajukan tepat waktu, persediaan terkendali, dan utang pemasok dibayar sesuai termin.</p>
<p>Bila investor masuk sebagai pemegang saham baru, bukan pembeli seluruh saham, mekanismenya sama tetapi muncul sebagai penyesuaian jumlah saham yang diterbitkan atau sebagai pernyataan dan jaminan di perjanjian.</p></div>
<h2>Jadwal yang Realistis</h2>
{tbl(['Tahap', 'Lama', 'Pekerjaan pemilik'],
     [['Persiapan internal', '6 sampai 10 minggu', 'Audit, rekonsiliasi data SIMRS dan keuangan, menyusun data room'],
      ['Penawaran indikatif', '2 sampai 4 minggu', 'Paparan manajemen, menjawab pertanyaan awal'],
      ['Due diligence', '6 sampai 10 minggu', 'Melayani permintaan data dan kunjungan lapangan'],
      ['Perundingan perjanjian', '4 sampai 8 minggu', 'Harga akhir, pernyataan dan jaminan, syarat penutupan'],
      ['Penutupan', '2 sampai 6 minggu', 'Persetujuan, perubahan anggaran dasar, perizinan penanaman modal']])}
<p>Persiapan internal adalah tahap yang sepenuhnya di tangan pemilik, dan paling menentukan harga. Uji tuntas yang dikerjakan lebih dulu dari sisi penjual membuat temuan diketahui dan diperbaiki sebelum investor menemukannya.</p>
<h2>Bagaimana FA Indonesia Membantu</h2>
<p>Pemilik rumah sakit di Batam dan Kepulauan Riau didampingi tim FA Indonesia dari sisi penjual: uji tuntas pendahuluan, normalisasi laba, perhitungan utang bersih dan modal kerja normal, penyusunan data room, sampai pendampingan menjawab pertanyaan investor. Audit laporan keuangan dikerjakan kantor akuntan publik secara terpisah agar independensinya terjaga. Lihat <a href="/pendanaan-rumah-sakit/batam/">pendanaan rumah sakit di Batam</a>, <a href="/konsultan-rumah-sakit/batam/">konsultan rumah sakit Batam</a>, dan <a href="/artikel/due-diligence-akuisisi-rumah-sakit-swasta/">due diligence akuisisi rumah sakit swasta</a>.</p>
''',
  faq=[('Apa itu due diligence rumah sakit?', 'Pemeriksaan menyeluruh oleh calon investor atas keuangan, pajak, hukum, pasar, dan operasional rumah sakit sebelum transaksi, untuk menguji angka dan menemukan risiko yang memengaruhi harga.'),
       ('Apa saja isi data room rumah sakit?', 'Dokumen korporasi, perizinan dan akreditasi, laporan keuangan diaudit, laporan manajemen bulanan, rincian pendapatan per layanan dan penjamin, kontrak dokter dan pemasok, dokumen aset, pajak, dan perkara hukum.'),
       ('Apa itu penyesuaian modal kerja dalam transaksi?', 'Mekanisme yang membandingkan modal kerja pada tanggal penutupan dengan modal kerja normal yang disepakati. Bila lebih rendah, harga dikurangi sebesar selisihnya, dan sebaliknya.'),
       ('Apakah rumah sakit di luar KEK Batam juga diminati investor?', 'Ya. Investor yang datang karena kawasan khusus biasanya juga memetakan rumah sakit yang sudah beroperasi dan punya basis pasien, selama laporan keuangan dan perizinannya siap diperiksa.')])
