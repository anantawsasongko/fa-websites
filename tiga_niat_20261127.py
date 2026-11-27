#!/usr/bin/env python3
"""27 Nov 2026: Tiga situs, tiga niat pencarian (langkah B dan C dari keputusan Bos 26 Nov).

FA = jasa. CA = direktori kantor berizin + alat. US = belajar standar + kertas kerja.
Bekerja di out/cariakuntan dan out/updatesak. Idempoten, --dry.
JALANKAN PALING AKHIR untuk CA dan US (sesudah caus_mandiri_20261126.py), lalu
`python3 shared/thin_noindex.py out cariakuntan` (daftar pilar jasa CA yang di-noindex ada di sana).

CA
1. /kota/<kota>/{kap,kja,kjpp}/: H1 = title "Daftar ...", pembuka dan isi bernada direktori (bukan "kami pilihkan").
2. /kota/<kota>/: pembuka direktori. /kota/: title, H1, description, kalimat per pulau.
3. Daftar kecamatan/desa dilipat. Sebutan FA Indonesia di luar beranda dibuang.
4. Semua pesan WA memuat sumber cariakuntan.com.
US
5. Judul "Dikerjakan/Dibantu Tim FA Indonesia" jadi Tim UpdateSAK; publisher JSON-LD = UpdateSAK.
6. Blok bantuan (fa-cta2) berisi penerapan standar, bukan daftar jasa FA.
7. Isi unik 11 halaman PSAK/SA prioritas (fa_content/us_ck_20261127.py), penanda <!--us-ck27-->.
8. Semua pesan WA memuat sumber updatesak.com.
"""
import glob, html, os, re, sys
from urllib.parse import quote, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "fa_content"))
from us_ck_20261127 import CK  # noqa: E402

DRY = "--dry" in sys.argv
WA = "https://wa.me/6282245260121?text="
stat = {}


def bump(k, n=1):
    stat[k] = stat.get(k, 0) + n


def sub(pat, rep, s, key, flags=0, count=0):
    s2, n = re.subn(pat, rep, s, count=count, flags=flags)
    if n:
        bump(key, n)
    return s2


def wa_src(s, dom):
    """Pesan WA tanpa nama domain diberi sumber, supaya lead bisa dibedakan per situs."""
    def fix(m):
        raw = m.group(2)
        t = unquote(raw.replace("+", " "))
        if dom in t or not t.strip():
            return m.group(0)
        mm = re.match(r"((?:Halo|Selamat (?:pagi|siang|sore|malam))(?: Pak Ananta)?),\s*(.*)$", t, re.S)
        if mm:
            rest = mm.group(2)
            t2 = "%s, saya dari %s. %s" % (mm.group(1), dom, rest[:1].upper() + rest[1:])
        else:
            t2 = "[%s] %s" % (dom, t)
        bump(dom + " wa bersumber")
        return m.group(1) + quote(t2, safe="/") + m.group(3)
    return re.sub(r'(href="https://wa\.me/6282245260121\?text=)([^"]*)(")', fix, s)


# ---------------------------------------------------------------- CariAkuntan
NAMA = {"kap": "kantor akuntan publik (KAP)", "kja": "Kantor Jasa Akuntansi (KJA)", "kjpp": "Kantor Jasa Penilai Publik (KJPP)"}
EKOR = {"kap": "Cek izinnya dulu, lalu cocokkan dengan kelas yang diminta bank, regulator, atau investor Anda.",
        "kja": "KJA menyusun pembukuan dan laporan keuangan tanpa memberi opini audit, jadi cocok sebagai langkah sebelum diaudit KAP.",
        "kjpp": "Cek izinnya dulu, lalu pastikan kantor itu diterima bank tujuan Anda."}
PAKAI = ("<h2>Cara Memakai Daftar Ini</h2><p>1. Tanyakan ke bank, regulator, atau panitia tender jenis dan kelas kantor yang diminta. "
         "2. Saring daftar di halaman ini dan cek status izinnya di registri Kemenkeu. "
         "3. Minta penawaran tertulis dari dua atau tiga kantor, lalu bandingkan ruang lingkup dan jadwalnya, bukan hanya harganya. "
         "4. Bila butuh pendapat kedua sebelum memutuskan, tanyakan lewat WhatsApp.</p>")
PULAU = {
    r"Jaringan mitra kami menangani klien di berbagai kota Sumatera, dari usaha keluarga hingga grup perkebunan\.":
        "Daftar kantor berizin di kota-kota Sumatera, dari Banda Aceh sampai Bandar Lampung, bersumber dari registri PPPK Kementerian Keuangan.",
    r"Mitra kami berpengalaman dengan BPR, koperasi, dan usaha pariwisata di Bali dan Nusa Tenggara\.":
        "Di Bali dan Nusa Tenggara, daftar ini paling sering dibuka pemilik usaha pariwisata, BPR, dan koperasi yang diminta laporan oleh bank atau investor.",
    r"Untuk Kalimantan, pekerjaan lapangan dijadwalkan per kunjungan, sementara sebagian besar proses berjalan daring\.":
        "Di Kalimantan jumlah kantor per kota lebih sedikit, jadi cek juga daftar kota terdekat dan kantor yang melayani secara daring.",
    r"Jarak bukan hambatan\. Mitra kami pernah menangani pekerjaan hingga Indonesia timur, dengan kunjungan lapangan terjadwal dan proses daring\.":
        "Di Indonesia timur kantor berizin terpusat di beberapa kota. Daftar per kota membantu melihat pilihan terdekat sebelum mencari ke luar pulau.",
}


def ca_kota(rel, s):
    parts = rel.split("/")
    kind = parts[2] if len(parts) == 4 else None  # kota/<kota>/<kind>/index.html
    m = re.search(r'data-city="([^"]+)"', s)
    city = m.group(1) if m else None
    if kind in NAMA and city:
        t = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
        if t.startswith("Daftar "):
            h1 = re.search(r"<h1>(.*?)</h1>", s, re.S)
            if h1 and h1.group(1) != t:
                old = h1.group(1)
                s = s.replace("<h1>%s</h1>" % old, "<h1>%s</h1>" % t, 1)
                s = s.replace('data-tool="%s"' % old, 'data-tool="%s"' % t)
                bump("ca h1 daftar")
        s = sub(r'<p class="sub">Cari [^<]*?Ceritakan kebutuhan Anda, kami pilihkan kantor[^<]*</p>',
                '<p class="sub">Daftar %s di %s menurut registri PPPK Kementerian Keuangan, lengkap dengan nomor izin dan statusnya. %s</p>'
                % (NAMA[kind], city, EKOR[kind]), s, "ca sub daftar")
        s = sub(r"(?<=\. )Dipilihkan sesuai syarat bank, regulator, atau investor\. Chat Ananta, CPA, konsultasi awal gratis\.",
                "Daftar dari registri PPPK Kementerian Keuangan, lengkap dengan status izin.", s, "ca jsonld desc")
    if kind is None:
        s = sub(r"Kami menghubungkan perusahaan di ([^<]+?) dengan kantor akuntan publik \(KAP\), KJPP, konsultan pajak, dan Kantor Jasa Akuntansi yang memenuhi persyaratan bank, regulator, atau investor\.",
                r"Halaman ini memuat daftar KAP, KJA, dan KJPP berizin aktif di \1 menurut registri PPPK Kementerian Keuangan, untuk dicek sebelum Anda memilih kantor.",
                s, "ca sub hub")
    s = sub(r"(Di [^<.;]+?), yang paling sering menghubungi kami adalah ", r"\1, kebutuhan ini umumnya datang dari ", s, "ca umumnya")
    s = sub(r"Selain kota ([^<,]+), kami juga melayani ", r"Wilayah sekitar \1 yang juga sering dicari adalah ", s, "ca sekitar")
    s = s.replace("yang juga sering dicari: ", "yang juga sering dicari adalah ")
    s = sub(r"Kawasan yang sering kami layani di ", "Kawasan bisnis di ", s, "ca kawasan")
    s = sub(r"<h2>Cara Kami Memilihkan (KAP|KJA|KJPP) untuk ", r"<h2>Cara Memilih \1 di ", s, "ca h2 memilih")
    s = sub(r"Kami cocokkan KAP untuk perusahaan di [^<.]+? dengan kelas yang diminta bank Anda, sehingga laporan audited tidak ditolak\.",
            "Cocokkan kelas KAP dengan yang diminta bank Anda sebelum menandatangani perikatan, supaya laporan audited tidak ditolak.", s, "ca cocokkan")
    s = sub(r"Kami hubungkan dengan KJA dan akuntan berpraktik yang terbiasa dengan SAK EMKM, SAK EP, dan PSAK, dan bisa memakai software akuntansi apa pun atau template Excel\.",
            "Pilih KJA yang terbiasa dengan kerangka yang Anda pakai (SAK EMKM, SAK EP, atau PSAK) dan bisa bekerja dengan software akuntansi atau template Excel Anda.", s, "ca kja pilih")
    s = sub(r"Kami carikan KJPP yang sudah menjadi rekanan bank tujuan Anda dan bisa menjadwalkan",
            "Tanyakan dulu daftar rekanan bank tujuan Anda, lalu cocokkan dengan KJPP berizin aktif yang bisa menjadwalkan", s, "ca kjpp cocok")
    s = sub(r"Kami carikan KJPP rekanan bank tujuan Anda yang bisa menjadwalkan",
            "Pilih KJPP berizin aktif yang menjadi rekanan bank tujuan Anda dan bisa menjadwalkan", s, "ca kjpp faq")
    s = sub(r"<h2>Alurnya</h2><p>1\. Anda chat[^<]*?kami dampingi sampai selesai\.</p>", PAKAI, s, "ca cara pakai")
    s = sub(r"Ceritakan kebutuhan Anda melalui WhatsApp ke Ananta, CPA di cariakuntan\.com\. Kami pilihkan KAP yang sesuai kelas rekanan bank, skala usaha, dan jadwal Anda di ([^.<\"]+)\. Konsultasi awal gratis\.",
            r"Daftar KAP berizin di \1 ada di halaman ini, bersumber dari registri PPPK Kementerian Keuangan. Saring menurut kelas rekanan bank, skala usaha, dan jadwal Anda, lalu cek status izinnya. Bila perlu pendapat kedua, tanyakan lewat WhatsApp.",
            s, "ca faq kap")
    s = sub(r"Kami sampaikan kisaran biaya setelah melihat data Anda, sebelum Anda berkomitmen\.",
            "Minta penawaran tertulis setelah kantor melihat data Anda, sebelum Anda berkomitmen.", s, "ca faq biaya")
    s = sub(r"kami bantu rekomendasikan notaris rekanan\.", "tanyakan lewat WhatsApp bila butuh rujukan notaris.", s, "ca notaris")
    s = sub(r"<h2>Area Layanan di ", "<h2>Cakupan Wilayah ", s, "ca h2 cakupan")
    s = sub(r"Kami melayani KAP, KJA, konsultan pajak, dan KJPP untuk perusahaan, yayasan, koperasi, dan rumah sakit di seluruh ([^<]+?), termasuk kecamatan dan desa/kelurahan berikut\. Pertemuan bisa di lokasi Anda atau daring\.",
            r"Daftar ini mencakup kantor yang tercatat di seluruh \1, termasuk kecamatan dan desa/kelurahan berikut.", s, "ca cakupan")
    s = sub(r'(<section class="arl"[^>]*>.*?)<details open>', r"\1<details>", s, "ca lipat kecamatan", flags=re.S)
    return s


def ca_page(rel, s):
    home = rel in ("index.html", "en/index.html", "zh/index.html", "hokkien/index.html")
    if re.match(r"kota/[^/]+/(?:(?:kap|kja|kjpp)/)?index\.html$", rel):
        s = ca_kota(rel, s)
    if rel == "kota/index.html":
        s = sub(r"<title>KAP, KJPP, Konsultan Pajak &amp; Jasa Laporan Keuangan di 113 Kota Indonesia</title>",
                "<title>Direktori KAP, KJA, dan KJPP Berizin di 113 Kota Indonesia</title>", s, "ca /kota/ title")
        s = sub(r"<h1>KAP, KJPP, Konsultan Pajak, dan Jasa Laporan Keuangan dari Aceh hingga Papua</h1>",
                "<h1>Direktori KAP, KJA, dan KJPP Berizin dari Aceh hingga Papua</h1>", s, "ca /kota/ h1")
        s = sub(r'content="Cari KAP, KJPP, konsultan pajak, dan jasa penyusunan laporan keuangan di 113 kota: [^"]*"',
                'content="Direktori KAP, KJA, dan KJPP berizin aktif di 113 kota menurut registri PPPK Kementerian Keuangan. Pilih kota, lihat daftar kantor, cek status izinnya."',
                s, "ca /kota/ desc")
        s = sub(r"(<p class=\"sub\">113 kota dengan aktivitas bisnis terbesar di Indonesia\.) Pekerjaan lapangan dijadwalkan per kunjungan, sebagian besar proses berjalan daring\.</p>",
                r"\1 Pilih kota untuk melihat daftar kantor berizin aktif beserta nomor izinnya.</p>", s, "ca /kota/ sub")
    if rel.startswith("kota/"):
        for a, b in PULAU.items():
            s = sub(a, b, s, "ca pulau")
    if not home:
        s = sub(r" · dikelola oleh FA Indonesia \(CV FA Indonesia, NIB \d+\)", "", s, "ca footer pengelola")
    s = sub(r"<b>Dikerjakan Rekanan FA Indonesia</b>", "<b>Dikerjakan Kantor Berizin</b>", s, "ca pita 04")
    s = sub(r"dikerjakan rekanan kami, tim FA Indonesia, bersama", "dikerjakan rekanan kami bersama", s, "ca artikel rekanan")
    s = sub(r"Lihat layanan [^,<.]+, daftar kantor di ", "Lihat daftar kantor di ", s, "ca artikel lihat")
    s = sub(r" Lihat Akuntan Forensik FA Indonesia\.", "", s, "ca lihat forensik")
    s = sub(r", dengan FA Indonesia sebagai pintu kontaknya\.", ".", s, "ca pintu kontak")
    s = sub(r" Rincian: [^<]*?\.(?= Ingin paham dulu)", "", s, "ca rincian")
    s = s.replace('base="https://wa.me/6282245260121?text=Selamat%20siang%20Pak%20Ananta%2C%20tolong%20bantu',
                  'base="https://wa.me/6282245260121?text=Selamat%20siang%20Pak%20Ananta%2C%20saya%20dari%20cariakuntan.com.%20Tolong%20bantu')
    s = s.replace('base="https://wa.me/6282245260121?text=Hello%20Pak%20Ananta%2C%20please',
                  'base="https://wa.me/6282245260121?text=Hello%20Pak%20Ananta%2C%20I%20am%20writing%20from%20cariakuntan.com.%20Please')
    s = wa_src(s, "cariakuntan.com")
    return s


# ------------------------------------------------------------------ UpdateSAK
US_PUB = '"publisher": {"@type": "Organization", "name": "UpdateSAK", "url": "https://updatesak.com/"}'
US_UL = ("<ul><li>Jurnal penyesuaian dan perhitungan untuk penerapan standar</li>"
         "<li>Kebijakan akuntansi dan catatan atas laporan keuangan (CALK)</li>"
         "<li>Jawaban atas pertanyaan auditor tentang standar ini</li></ul>")
CSS27 = ('<style id="us-ck27">.us-ck27 table th,.us-ck27 table td{border:1px solid rgba(127,127,127,.35);padding:7px 10px;text-align:left;vertical-align:top}'
         ".us-ck27 table th{font-weight:600}.us-ck27 ul{margin:8px 0 18px;padding-left:20px}.us-ck27 li{margin:5px 0}</style>")


def us_ck(rel, s):
    key = rel[: -len("/index.html")]
    if key not in CK:
        return s
    judul, isi, salah = CK[key]
    kode = re.search(r"<h1[^>]*>((?:PSAK|SA|SPA|SJT) \d+)", s).group(1)
    blok = ('<!--us-ck27--><div class="us-ck27">%s<h2 id="contoh-27">%s</h2>%s<h2 id="kesalahan-27">Kesalahan yang Sering Terjadi</h2><ul>%s</ul>'
            '<p class="note">Angka di atas adalah ilustrasi yang disusun tim UpdateSAK, bukan kutipan teks standar. Kasus Anda berbeda? '
            '<a href="%s" target="_blank" rel="noopener" data-us-q="ck27">Tanyakan penerapan %s lewat WhatsApp</a>.</p></div><!--/us-ck27-->'
            % (CSS27, judul, isi, "".join("<li>%s</li>" % x for x in salah),
               WA + quote("Halo, saya dari updatesak.com (%s). Mau tanya penerapannya di perusahaan kami: " % kode, safe="/"), kode))
    s0 = re.sub(r"<!--us-ck27-->.*?<!--/us-ck27-->", "", s, flags=re.S)
    s0 = s0.replace('<li><a href="#contoh-27">Contoh Angka</a></li><li><a href="#kesalahan-27">Kesalahan yang Sering Terjadi</a></li>', "")
    # sisipkan sebelum "Standar Terkait" (PSAK), "PSAK Terkait" (SA), atau "Tanya Jawab"
    for anchor in (r'<h2 id="standar-terkait">', r"<h2>PSAK Terkait</h2>", r"<h2>Tanya Jawab</h2>"):
        m = re.search(anchor, s0)
        if m:
            s0 = s0[: m.start()] + blok + s0[m.start():]
            break
    else:
        raise SystemExit("anchor us-ck27 tidak ketemu: " + rel)
    s0 = s0.replace('<li><a href="#standar-terkait">Standar Terkait</a></li>',
                    '<li><a href="#contoh-27">Contoh Angka</a></li><li><a href="#kesalahan-27">Kesalahan yang Sering Terjadi</a></li><li><a href="#standar-terkait">Standar Terkait</a></li>', 1)
    if s0 != s:
        bump("us isi unik")
    return s0


def us_page(rel, s):
    home = rel == "index.html"
    s = sub(r'<h2 id="(?:dikerjakan|dibantu)-tim-fa-indonesia">(?:Dikerjakan|Dibantu) Tim FA Indonesia</h2>',
            '<h2 id="dibantu-tim-updatesak">Dibantu Tim UpdateSAK</h2>', s, "us h2 tim")
    s = sub(r'<li><a href="#(?:dikerjakan|dibantu)-tim-fa-indonesia">(?:Dikerjakan|Dibantu) Tim FA Indonesia</a></li>',
            '<li><a href="#dibantu-tim-updatesak">Dibantu Tim UpdateSAK</a></li>', s, "us toc tim")
    s = sub(r'<li><a href="#bantuan-di-kota-anda">[^<]*</a></li>', "", s, "us toc kota")
    s = sub(r"Tim FA Indonesia bisa mengerjakannya:", "tim kami bisa mengerjakannya:", s, "us tim kami")
    s = sub(r"dikerjakan tim FA Indonesia untuk perusahaan di ([^<.]+?) dan kota lain\. Lihat [^<]*?\.",
            lambda m: 'juga kami kerjakan untuk perusahaan di %s dan kota lain. <a href="%s" target="_blank" rel="noopener" data-us-q="artikel">Tanyakan lewat WhatsApp</a>.'
            % (m.group(1), WA + quote("Halo, saya dari updatesak.com. Mau tanya perhitungan seperti di artikel untuk perusahaan kami di %s: " % m.group(1), safe="/")),
            s, "us artikel tim")
    s = sub(r'(<a class="btn rxg" href="/#dibantu">)Dikerjakan Tim FA(</a>)', r"\1Minta Dibantu Tim UpdateSAK\2", s, "us tombol hero")
    s = sub(r">Dibantu Tim FA</a>", ">Dibantu Tim</a>", s, "us menu")
    s = sub(r'(<p class="rx-h">)Dikerjakan Tim FA Indonesia(</p>)', r"\1Dibantu Tim UpdateSAK\2", s, "us beranda judul")
    s = s.replace("ingin%20dibantu%20tim%20FA%20Indonesia%20untuk%20penerapannya", "ingin%20dibantu%20untuk%20penerapannya")
    if not home:
        s = sub(r'"publisher": \{"@type": "Organization", "name": "FA Indonesia", "url": "https://faindonesia\.co\.id/"\}', US_PUB, s, "us publisher")
    s = sub(r"<ul><li>Pembukuan dan laporan keuangan siap audit, UMKM sampai PT</li><li>Pendampingan Audit KAP dan Laporan Tahunan PT</li><li>Persiapan Kredit Bank dan Investor</li></ul>",
            US_UL, s, "us cta isi")
    s = sub(r"Bila perlu, kami bantu dari jurnal penyesuaian, CALK, sampai pendampingan KAP\.",
            "Bila perlu, tim UpdateSAK membantu sampai angkanya masuk ke laporan keuangan.", s, "us cta kalimat")
    s = us_ck(rel, s)
    s = wa_src(s, "updatesak.com")
    return s


def run():
    changed = {}
    for site, fn in (("cariakuntan", ca_page), ("updatesak", us_page)):
        root = os.path.join(ROOT, "out", site)
        n = 0
        for f in glob.glob(os.path.join(root, "**", "*.html"), recursive=True):
            rel = os.path.relpath(f, root).replace(os.sep, "/")
            old = open(f, encoding="utf-8").read()
            new = fn(rel, old)
            if new != old:
                n += 1
                if not DRY:
                    open(f, "w", encoding="utf-8").write(new)
        changed[site] = n
    print("file berubah:", changed, "(dry)" if DRY else "")
    for k in sorted(stat):
        print("  %-28s %d" % (k, stat[k]))


if __name__ == "__main__":
    run()
