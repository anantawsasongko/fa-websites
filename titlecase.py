# Title Case untuk judul dan poin di semua halaman (dipanggil dari prep.py).
# Aturan Bos: huruf pertama tiap kata kapital untuk judul (title, h1-h6) dan poin pendek
# (item list, label, tombol, chip, label SVG). Kata sambung tetap kecil kecuali di awal.
# Kalimat panjang / paragraf tidak disentuh.
import os, re, json
from bs4 import BeautifulSoup, NavigableString, Comment

MINOR = {"dan","di","ke","dari","untuk","yang","atau","hingga","sampai","dengan","pada","oleh","bagi",
         "tentang","dalam","per","serta","tetapi","karena","agar","saat","tanpa","jadi","&","vs","via",
         "terhadap","antara","kepada","daripada","sebagai","lewat","melalui","akan","pun",
         "a","an","the","and","or","but","nor","of","on","in","at","to","by","from","with","as","for","into"}
UNITS = {"jt","juta","rb","ribu","miliar","triliun"}
KEEP = re.compile(r"[@/]|\.\w|cariakuntan|faindonesia|https?:", re.I)

def tc(t, first=True):
    out = []
    words = t.split(" ")
    seen = not first
    for w in words:
        if not w:
            out.append(w); continue
        core = w.strip("(),:;?!\"'“”‘’.")
        if KEEP.search(w) or not core:
            out.append(w); seen = seen or bool(core); continue
        if core.islower() and core.lower() in UNITS and out and re.search(r"\d", " ".join(out[-1:])+w):
            out.append(w); seen = True; continue
        if core in ("ribu","juta","miliar","triliun","jt","rb"):
            out.append(w); seen = True; continue
        if seen and core.lower() in MINOR and core.islower():
            out.append(w); continue
        j = next((k for k, ch in enumerate(w) if ch.isalpha()), None)
        seen = True
        if j is None or not w[j].islower():
            out.append(w); continue
        out.append(w[:j] + w[j].upper() + w[j+1:])
    return " ".join(out)

HEAD = {"h1","h2","h3","h4","h5","h6","title"}
SHORT = {"li","span","small","b","strong","a","button","label","figcaption","dt","th","summary","legend","text","tspan","div","em"}
SKIP_ANC = {"p","td","blockquote","script","style","textarea","select","code","pre","noscript"}
INLINE = {"span","b","strong","i","em","br","small","a","sup","sub","svg","img","u"}

def words(s): return [w for w in re.split(r"\s+", s.strip()) if w]

def short_ok(s):
    s = s.strip()
    if not s or not re.search(r"[a-z]", s): return False
    if s[-1] in ".!?…": return False
    n = len(words(s))
    return 1 <= n <= 7

def textnodes(el):
    return [x for x in el.descendants if isinstance(x, NavigableString) and not isinstance(x, Comment)
            and x.parent.name not in ("script","style")]

def apply(el):
    changed = False
    first = True
    for x in textnodes(el):
        s = str(x)
        if not s.strip(): continue
        n = tc(s, first)
        first = False
        if n != s:
            x.replace_with(NavigableString(n)); changed = True
    return changed

def branded(el):
    for a in [el] + list(el.parents):
        c = " ".join(a.get("class", []) or []) if hasattr(a, "get") else ""
        if re.search(r"logo|brand|wordmark", c, re.I): return True
    return False

def qualifies(el):
    if branded(el): return False
    if el.name in HEAD: return True
    if el.name not in SHORT: return False
    if any(a.name in SKIP_ANC or a.name in HEAD for a in el.parents): return False
    if any(getattr(c, "name", None) and c.name not in INLINE for c in el.children): return False
    if el.name in ("span","b","strong","a","em","small") and el.parent is not None and el.parent.name in ("li","div") :
        # bagian dari kalimat yang lebih panjang? cek teks induk
        pt = el.parent.get_text(" ", strip=True)
        if not short_ok(pt) and len(words(pt)) > len(words(el.get_text(" ", strip=True))) + 2: return False
    return short_ok(el.get_text(" ", strip=True))

def fix_i18n(html, keys):
    m = re.search(r"var I18N=", html)
    if not m or not keys: return html
    start = m.end()
    try:
        obj, end = json.JSONDecoder().raw_decode(html[start:])
    except Exception:
        return html
    for lang in ("id", "en"):
        d = obj.get(lang)
        if not isinstance(d, dict): continue
        for k, kind in keys.items():
            v = d.get(k)
            if not isinstance(v, str): continue
            plain = re.sub(r"<[^>]+>", " ", v)
            if kind == "head" or short_ok(plain):
                if "<" in v:
                    parts = re.split(r"(<[^>]+>)", v); first = True
                    for i, part in enumerate(parts):
                        if part.startswith("<") or not part.strip(): continue
                        parts[i] = tc(part, first); first = False
                    d[k] = "".join(parts)
                else:
                    d[k] = tc(v)
    return html[:start] + json.dumps(obj, ensure_ascii=False) + html[start+end:]

def process_file(p):
    raw = open(p, encoding="utf-8").read()
    soup = BeautifulSoup(raw, "html.parser")
    keys = {}
    changed = False
    done = set()
    for el in soup.find_all(list(HEAD | SHORT)):
        if any(id(a) in done for a in el.parents): continue
        if not qualifies(el): continue
        done.add(id(el))
        if apply(el): changed = True
        k = el.get("data-i18n")
        if k: keys[k] = "head" if el.name in HEAD else "short"
    if not changed and not keys: return False
    out = str(soup)
    out = fix_i18n(out, keys)
    if out != raw:
        open(p, "w", encoding="utf-8").write(out)
        return True
    return False

def run(root):
    n = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".html") and process_file(os.path.join(dp, f)): n += 1
    return n

if __name__ == "__main__":
    import sys
    for r in sys.argv[1:]: print(r, run(r))
