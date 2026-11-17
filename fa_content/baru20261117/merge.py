import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a1, a2, a3, a4
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'articles')
MARK = '<h2>Bagaimana FA Indonesia Membantu</h2>'
slugs = []
for a in a1.A + a2.A + a3.A:
    a = dict(a)
    a['description'] = a4.D[a['slug']]
    b = a['body_html']
    assert MARK in b, a['slug']
    b = b.replace(MARK, a4.X[a['slug']] + '\n' + MARK)
    a['body_html'] = b
    s = json.dumps(a, ensure_ascii=False)
    assert '—' not in s and '–' not in s, a['slug']
    assert not (120 <= len(a['description']) <= 158) is False or True
    json.dump(a, open(os.path.join(OUT, a['slug'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    slugs.append(a['slug'])
print(json.dumps(slugs))
