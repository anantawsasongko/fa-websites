"""UpdateSAK: bereskan GSC "Duplicate without user-selected canonical" (PDF www/apex) dan 404 /cdn-cgi/ (9 Nov 2026).
Idempoten, jalankan setelah prep.py + us_lead + us_kw3.
- PDF tidak bisa punya <link rel=canonical>, jadi canonical dikirim lewat header Link di _headers.
  PDF yang punya halaman HTML kembaran (/materi/<slug>/) -> canonical ke halaman itu; sisanya -> URL PDF apex.
  Berlaku juga saat diakses lewat www.updatesak.com (pola path, tanpa host).
- robots.txt: Disallow /cdn-cgi/ (link email-protection Cloudflare yang 404).
Catatan: www -> apex 301 hanya bisa lewat Redirect Rule di zone updatesak.com (dashboard Cloudflare), seperti FA.
"""
import os, re
R = os.path.dirname(os.path.abspath(__file__))
U = os.path.join(R, "out", "updatesak")
SITE = "https://updatesak.com"
M1, M2 = "# us-pdfcanon-start", "# us-pdfcanon-end"

lines = [M1]
n = 0
for sub in ("materi/pdf", "dosen/pdf"):
    d = os.path.join(U, sub)
    for f in sorted(os.listdir(d)):
        if not f.endswith(".pdf"):
            continue
        slug = f[:-4]
        twin = os.path.join(U, "materi", slug, "index.html") if sub == "materi/pdf" else None
        target = f"{SITE}/materi/{slug}/" if twin and os.path.exists(twin) else f"{SITE}/{sub}/{f}"
        lines += [f"/{sub}/{f}", f'  Link: <{target}>; rel="canonical"']
        n += 1
lines.append(M2)
block = "\n".join(lines)

h = os.path.join(U, "_headers")
s = open(h).read()
s = re.sub(re.escape(M1) + r".*?" + re.escape(M2), "", s, flags=re.S).rstrip()
open(h, "w").write(s + "\n\n" + block + "\n")

rb = os.path.join(U, "robots.txt")
t = open(rb).read()
if "Disallow: /cdn-cgi/" not in t:
    t = t.replace("Allow: /\n", "Allow: /\nDisallow: /cdn-cgi/\n", 1)
    open(rb, "w").write(t)
print("us_dupfix: canonical PDF", n, "| robots", "Disallow: /cdn-cgi/" in t)
