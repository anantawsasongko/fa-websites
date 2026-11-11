import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extra1 import X as X1
from extra2 import X as X2
X = {**X1, **X2}
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'articles')
PEN = ['<h2>Kontak Audit lewat FA Indonesia</h2>', '<h2>Penyusunan Laporan Keuangan lewat FA Indonesia</h2>',
       '<h2>Diskusi dengan FA Indonesia</h2>', '<h2>Konsultasi Penghitungan Kerugian</h2>']
for slug, ex in X.items():
    p = os.path.join(ART, slug + '.json'); d = json.load(open(p, encoding='utf-8'))
    assert '—' not in ex and '–' not in ex, slug
    b = d['body_html']
    blk = ex.strip()
    if blk[:60] in b: continue
    k = min([b.find(x) for x in PEN if x in b] or [len(b)])
    d['body_html'] = b[:k] + '\n' + blk + '\n' + b[k:]
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(X))
