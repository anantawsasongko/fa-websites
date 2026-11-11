"""Helper artikel lead 11 Nov 2026: tulis JSON ke fa_content/articles/."""
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'articles')
ALL = []


def A(slug, seo_title, title, description, keyword, category, minutes, cta, wa, sources, related, body_html, faq):
    assert len(seo_title) <= 65, (slug, len(seo_title))
    assert len(description) <= 158, (slug, len(description))
    for t in (seo_title, title, description, body_html, wa) + tuple(x for f in faq for x in f):
        assert '—' not in t and '–' not in t, slug
    d = dict(slug=slug, seo_title=seo_title, title=title, description=description, keyword=keyword,
             category=category, minutes=minutes, cta=dict(href=cta[0], label=cta[1]), wa=wa,
             sources=[list(s) for s in sources], related=related, body_html=body_html.strip(), faq=[list(f) for f in faq])
    json.dump(d, open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ALL.append(slug)
