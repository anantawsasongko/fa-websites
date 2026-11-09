"""Ukur kemiripan teks utama antarhalaman sejenis (9 Nov 2026).
Pemakaian: python3 tools/similarity.py out/faindonesia jasa-audit-laporan-keuangan konsultan-klinik ...
Untuk tiap keluarga: ambil maks 30 halaman (urut nama, deterministik), teks di <main> (atau <body>),
shingle 5 kata, rata-rata Jaccard semua pasangan. Juga "unik%": porsi shingle halaman yang tidak ada di halaman lain sampel.
"""
import os, re, sys, itertools, json

def text(p):
    s = open(p, encoding="utf-8", errors="ignore").read()
    m = re.search(r"(?s)<main[^>]*>(.*)</main>", s)
    s = m.group(1) if m else s
    s = re.sub(r"(?s)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = re.sub(r"&[a-z#0-9]+;", " ", s).lower()
    return re.findall(r"[a-z0-9]+", s)

def sh(w, k=5):
    return {" ".join(w[i:i + k]) for i in range(max(0, len(w) - k + 1))}

def family(root, fam, n=30, depth1=True):
    import glob
    pat = fam if "*" in fam else fam + "/*"
    subs = sorted(os.path.dirname(f) for f in glob.glob(os.path.join(root, pat, "index.html")))
    if len(subs) > n:  # sebar sampel merata
        step = len(subs) / n
        subs = [subs[int(i * step)] for i in range(n)]
    S = [sh(text(os.path.join(x, "index.html"))) for x in subs]
    pairs = [len(a & b) / max(1, len(a | b)) for a, b in itertools.combinations(S, 2)]
    uniq = []
    for i, a in enumerate(S):
        others = set().union(*(S[j] for j in range(len(S)) if j != i))
        uniq.append(len(a - others) / max(1, len(a)))
    return dict(n=len(S), jaccard=round(sum(pairs) / max(1, len(pairs)), 3), unik=round(sum(uniq) / len(uniq), 3),
                words=int(sum(len(a) for a in S) / len(S)))

if __name__ == "__main__":
    root = sys.argv[1]
    out = {}
    for fam in sys.argv[2:]:
        r = family(root, fam)
        out[fam] = r
        print(f"{fam:45s} n={r['n']:3d} jaccard={r['jaccard']:.3f} unik={r['unik']:.3f} shingle={r['words']}")
    if os.environ.get("SIMJSON"):
        json.dump(out, open(os.environ["SIMJSON"], "w"), indent=1)
