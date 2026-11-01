# Halaman /dosen/panduan-submit-scopus/ (1 Nov 2026). Dipanggil build_dosen.py: make(B, esc, CSS, UPD, crumb, head, cta_dosen).

P_FAQ = [("Bagaimana cara mengecek jurnal Scopus asli atau bajakan?", "Cari judul atau ISSN di Scopus Sources, lalu buka situs jurnal dari tautan di halaman sumber Scopus atau DOAJ. Jurnal bajakan biasanya memakai domain mirip, menjanjikan terbit cepat, dan meminta biaya sebelum review."),
         ("Berapa lama proses review jurnal Scopus akuntansi?", "Sangat bervariasi. Banyak jurnal memberi keputusan pertama dalam 1 sampai 4 bulan, dan total sampai terbit bisa 6 sampai 18 bulan. Cek data waktu proses di situs jurnal bila tersedia."),
         ("Apakah boleh memakai AI saat menulis naskah?", "Ikuti kebijakan penerbit. Umumnya AI tidak boleh menjadi penulis, dan penggunaannya untuk penyuntingan bahasa atau analisis wajib diungkapkan. Tanggung jawab isi tetap pada penulis."),
         ("Apa yang dilakukan bila naskah ditolak tanpa review (desk reject)?", "Baca alasan editor, perbaiki kecocokan dengan scope dan kejelasan kontribusi, lalu kirim ke jurnal lain yang lebih sesuai. Desk reject wajar dan sering terjadi.")]

COVER = """Kepada Yth. Editor-in-Chief [Nama Jurnal]

Dengan hormat, kami mengajukan naskah berjudul "[Judul]" untuk dipertimbangkan sebagai [research paper] di [Nama Jurnal].

Penelitian ini menjawab pertanyaan [pertanyaan riset dalam satu kalimat] dengan data [sumber data, periode, jumlah observasi]. Temuan utamanya adalah [temuan utama dalam satu kalimat].

Naskah ini sesuai dengan ruang lingkup jurnal karena [alasan], dan melanjutkan diskusi dalam [rujuk 1 sampai 2 artikel jurnal ini].

Kami menyatakan naskah ini orisinal, belum diterbitkan, dan tidak sedang dipertimbangkan di jurnal lain. Seluruh penulis menyetujui pengajuan ini dan tidak ada konflik kepentingan. [Pernyataan penggunaan alat AI bila ada.]

Hormat kami,
[Nama penulis korespondensi, afiliasi, email, ORCID]"""

RESP = [("Reviewer 1, Komentar 1", "[Kutip komentar reviewer]", "Terima kasih atas masukan ini. Kami [menambah uji ketahanan / memperjelas definisi variabel]. Perubahan ada di halaman 12, baris 240 sampai 255."),
        ("Reviewer 1, Komentar 2", "[Kutip komentar reviewer]", "Kami memahami pertimbangan Reviewer. Namun kami mempertahankan [pilihan metode] karena [argumen dan rujukan]. Sebagai jalan tengah, kami menambahkan [analisis tambahan] di Lampiran B."),
        ("Reviewer 2, Komentar 1", "[Kutip komentar reviewer]", "Kami setuju dan telah [merevisi bagian]. Lihat halaman 5, baris 88.")]


def make(B, esc, CSS, UPD, crumb, head, cta_dosen):
    BASE = B.BASE
    path = "/dosen/panduan-submit-scopus/"
    title = "Panduan Submit Artikel ke Jurnal Scopus untuk Dosen Akuntansi"
    desc = "Langkah submit artikel akuntansi ke jurnal Scopus: memilih jurnal, cek jurnal bajakan, struktur naskah, template cover letter, tabel balasan reviewer, dan etika publikasi. Gratis untuk dosen."
    rows = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in RESP)
    key = "dosen-panduan-scopus"
    out = f'''{CSS}<article class="art"><div class="wrap">
{crumb("Panduan Submit Scopus")}
<p class="label">Ruang Dosen · Submit Scopus</p>
<h1>{esc(title)}</h1>
<p class="lede">Dari memilih jurnal sampai membalas reviewer, dalam urutan yang biasa dilalui dosen. Lengkap dengan template yang bisa langsung disalin.</p>
<p class="upd">Tim UpdateSAK · Diperbarui {UPD}</p>
{B.share(BASE + path, title, key)}
<div class="ds-grid">
<a class="ds-card" href="#pilih"><span class="k">Langkah 1</span><b>Pilih Jurnal</b><span>Scope, status Scopus, dan biaya.</span></a>
<a class="ds-card" href="#naskah"><span class="k">Langkah 2</span><b>Rapikan Naskah</b><span>Struktur dan kontribusi.</span></a>
<a class="ds-card" href="#cover"><span class="k">Langkah 3</span><b>Cover Letter</b><span>Template satu halaman.</span></a>
<a class="ds-card" href="#reviewer"><span class="k">Langkah 4</span><b>Balas Reviewer</b><span>Tabel respon.</span></a>
</div>
<h2 id="pilih">1. Memilih Jurnal</h2>
<div class="prose"><ol>
<li><b>Mulai dari daftar pustaka sendiri.</b> Jurnal yang paling sering Anda kutip biasanya paling cocok dengan topik naskah.</li>
<li><b>Cek status di Scopus Sources.</b> Pastikan aktif dan cakupannya sampai tahun berjalan.</li>
<li><b>Buka situs dari sumber resmi.</b> Ambil alamat situs dari halaman sumber Scopus atau DOAJ, bukan dari email undangan.</li>
<li><b>Baca biaya di author guidelines.</b> Biaya submit, APC, dan biaya open access opsional. Pilihan terjangkau ada di <a href="/dosen/jurnal-scopus-gratis/">Jurnal Scopus Gratis dan APC Rendah</a>.</li>
<li><b>Cek waktu proses.</b> Sesuaikan dengan tenggat angka kredit atau kelulusan mahasiswa. Tenggat edisi khusus ada di <a href="/dosen/call-for-paper/">Call for Paper</a>.</li>
</ol></div>
<h3>Tanda Jurnal Bajakan atau Predator</h3>
<div class="prose"><ul>
<li>Domain mirip tetapi berbeda dengan yang tercantum di Scopus.</li>
<li>Menjanjikan terbit dalam hitungan minggu, atau review tanpa komentar substantif.</li>
<li>Meminta pembayaran sebelum keputusan review.</li>
<li>Satu edisi memuat ratusan artikel di luar scope jurnal.</li>
</ul></div>
<h2 id="naskah">2. Merapikan Naskah</h2>
<div class="scroll"><table class="tbl"><thead><tr><th>Bagian</th><th>Pertanyaan yang Harus Dijawab</th></tr></thead><tbody>
<tr><td>Judul dan abstrak</td><td>Apa temuan utama dan mengapa penting? Ikuti format abstrak terstruktur bila diminta.</td></tr>
<tr><td>Pendahuluan</td><td>Celah riset apa yang diisi dan apa kontribusinya, dalam 3 sampai 4 paragraf.</td></tr>
<tr><td>Teori dan hipotesis</td><td>Teori apa yang dipakai dan bagaimana hipotesis diturunkan.</td></tr>
<tr><td>Metode</td><td>Data, sampel, model, dan uji ketahanan yang bisa direplikasi.</td></tr>
<tr><td>Hasil dan pembahasan</td><td>Apa artinya dibanding studi terdahulu, bukan mengulang angka tabel.</td></tr>
<tr><td>Kesimpulan</td><td>Implikasi bagi regulator, praktisi, dan peneliti, serta keterbatasan.</td></tr>
</tbody></table></div>
<p>Konteks kelembagaan Indonesia, seperti kepemilikan keluarga, BUMN, regulasi OJK, dan adopsi SAK, adalah nilai jual naskah bila dijelaskan sebagai alasan teoretis, bukan sekadar mengganti nama negara.</p>
<h2 id="cover">3. Template Cover Letter</h2>
<pre style="white-space:pre-wrap;word-break:break-word;border:1px solid var(--line);padding:16px;font-size:.9rem;line-height:1.55;font-family:inherit">{esc(COVER)}</pre>
<p><button class="btn btn-sm" type="button" data-copy="{esc(COVER)}">Salin Template</button></p>
<h2 id="reviewer">4. Tabel Balasan Reviewer</h2>
<div class="scroll"><table class="tbl"><thead><tr><th>No.</th><th>Komentar Reviewer</th><th>Tanggapan dan Lokasi Perubahan</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="prose"><ul>
<li>Jawab setiap komentar, termasuk yang kecil.</li>
<li>Bila tidak setuju, beri argumen dan rujukan, lalu tawarkan jalan tengah.</li>
<li>Tandai perubahan di naskah sesuai permintaan editor.</li>
</ul></div>
<h2>Etika Publikasi</h2>
<div class="prose"><ul>
<li>Satu naskah hanya dikirim ke satu jurnal pada satu waktu.</li>
<li>Cek similarity sebelum submit, termasuk terhadap tesis, disertasi, atau prosiding sendiri.</li>
<li>Kepengarangan sesuai kontribusi nyata.</li>
<li>Ungkapkan penggunaan alat AI sesuai kebijakan penerbit.</li>
</ul></div>
<p><a class="btn arrow" href="/dosen/pdf/menulis-dan-submit-artikel-jurnal-scopus.pdf" download>Download Slide Pelatihan (PDF)</a></p>
{B.faq_html(P_FAQ)}
{cta_dosen()}
</div></article>
'''
    B.write(path.strip("/"), head(path, title, desc, [("UpdateSAK", BASE + "/"), ("Ruang Dosen", BASE + "/dosen/"), ("Panduan Submit Scopus", BASE + path)], P_FAQ, key, "Ruang Dosen") + out + B.FOOT)
    return path, title, desc
