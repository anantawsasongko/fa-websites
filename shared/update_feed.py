"""Updater otomatis "Berita Terkini" (dijalankan GitHub Actions .github/workflows/berita.yml).

1. Ambil RSS media bisnis nasional, saring topik bisnis/pajak/bank/pasar modal.
2. Tulis cariakuntan/feed.json (format [tanggal, judul, link, sumber], terbaru di atas).
3. Ganti daftar <li> di blok berita halaman yang sudah jadi di out/ (FA /artikel/,
   CariAkuntan beranda + /artikel/, UpdateSAK /eksplor/), jumlah item per blok tetap.
Kalau semua sumber gagal atau hasil < 5 berita, tidak ada yang diubah (situs tetap pakai daftar lama).
"""
import html, json, os, re, sys, urllib.request
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED_PATH = os.path.join(ROOT, "cariakuntan", "feed.json")
OUT = os.path.join(ROOT, "out")
WIB = timezone(timedelta(hours=7))

SOURCES = [
    ("CNBC Indonesia", "https://www.cnbcindonesia.com/market/rss"),
    ("CNBC Indonesia", "https://www.cnbcindonesia.com/news/rss"),
    ("Antara", "https://www.antaranews.com/rss/ekonomi-finansial.xml"),
    ("Antara", "https://www.antaranews.com/rss/ekonomi-bursa.xml"),
    ("Antara", "https://www.antaranews.com/rss/ekonomi.xml"),
    ("Kontan", "https://rss.kontan.co.id/news/keuangan"),
    ("Kontan", "https://rss.kontan.co.id/news/investasi"),
    ("Bisnis.com", "https://www.bisnis.com/rss"),
    ("CNN Indonesia", "https://www.cnnindonesia.com/ekonomi/rss"),
]
KEEP = re.compile(r"\b(pajak|djp|coretax|spt|ppn|pph|bank|kredit|bunga|ojk|bi rate|bank indonesia|bei|ihsg|saham|emiten|ipo|obligasi|sbn|sukuk|"
                  r"rupiah|dolar|laba|rugi|dividen|buyback|right issue|audit|akuntan|laporan keuangan|umkm|investasi|investor|"
                  r"pasar modal|reksa ?dana|fintech|pinjol|asuransi|bumn|danantara|apbn|inflasi|ekspor|impor|tbk|merger|akuisisi|"
                  r"npl|likuiditas|deposito|valas|suku bunga|fed|fomc)\b", re.I)
DROP = re.compile(r"^(video|foto|infografis|podcast)\b|\b(penyadap\w*|polri|kapolri|pilkada|pemilu|selebriti|artis|zodiak|resep|aki mobil)\b", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; FA-Indonesia-NewsBot/1.0)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def clean(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()
    return re.sub(r"\s+", " ", t)


def parse(name, raw):
    out = []
    root = ET.fromstring(raw)
    for it in root.iter("item"):
        title = clean(it.findtext("title"))
        link = clean(it.findtext("link")) or clean(it.findtext("guid"))
        pub = it.findtext("pubDate") or ""
        if not title or not link.startswith("http"):
            continue
        try:
            dt = parsedate_to_datetime(pub).astimezone(WIB)
        except Exception:
            continue
        out.append((dt, title, link, name))
    return out


def collect():
    items, ok = [], []
    for name, url in SOURCES:
        try:
            got = parse(name, fetch(url))
            items += got
            ok.append(f"{name} {len(got)}")
        except Exception as e:
            print(f"lewati {url}: {e}", file=sys.stderr)
    print("sumber:", ", ".join(ok) or "tidak ada")
    now = datetime.now(WIB)
    seen, res = set(), []
    for dt, t, l, s in sorted(items, key=lambda x: x[0], reverse=True):
        if dt > now + timedelta(hours=1) or dt < now - timedelta(days=4):
            continue
        if DROP.search(t) or not KEEP.search(t):
            continue
        key = re.sub(r"\W+", "", t.lower())[:60]
        if key in seen or l in seen:
            continue
        seen.update([key, l])
        res.append([dt.strftime("%Y-%m-%d"), t, l, s])
    # campur sumber: maks 14 berita dari satu sumber
    mixed, counts = [], {}
    for r in res:
        counts[r[3]] = counts.get(r[3], 0) + 1
        if counts[r[3]] <= 14:
            mixed.append(r)
    return mixed[:30]


def li_fa(d, t, l, s):
    return f'<li><a href="{html.escape(l)}" target="_blank" rel="noopener nofollow">{html.escape(t)}</a><span>{html.escape(s)} · {d}</span></li>'


li_ca = li_fa  # format sama, judul di-escape agar tanda & atau < tidak merusak halaman


def patch_out(feed):
    changed = 0
    pat = re.compile(r'(<section\b[^>]*\bclass="(ca-feed|feed)"[^>]*>.*?<ul[^>]*>)(.*?)(</ul>)', re.S)
    for root, _, files in os.walk(OUT):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            s = open(p, encoding="utf-8").read()
            if 'class="ca-feed"' not in s and 'class="feed"' not in s:
                continue

            def rep(m):
                n = max(m.group(3).count("<li>"), 1)
                mk = li_fa if m.group(2) == "ca-feed" else li_ca
                return m.group(1) + "".join(mk(*x) for x in feed[:n]) + m.group(4)

            t = pat.sub(rep, s)
            if t != s:
                open(p, "w", encoding="utf-8").write(t)
                changed += 1
                print("update", os.path.relpath(p, ROOT))
    return changed


def main():
    feed = collect()
    if len(feed) < 5:
        print(f"hanya {len(feed)} berita lolos saring, feed lama dipertahankan")
        return
    old = json.load(open(FEED_PATH)) if os.path.exists(FEED_PATH) else []
    if feed == old:
        print("tidak ada berita baru")
        return
    json.dump(feed, open(FEED_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"feed.json: {len(feed)} berita, terbaru {feed[0][0]} {feed[0][1]}")
    print("halaman diperbarui:", patch_out(feed))


if __name__ == "__main__":
    main()
