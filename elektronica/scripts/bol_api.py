"""Haalt bol-prijzen op via de Marketing Catalog API (serverfunctie op bespaarvriend.nl/api/bol).
Eerst per product op EAN (uit de MediaMarkt/Alternate/Azerty-resultaten), anders zoeken op naam + controle op naamwoorden.
Schrijft raw/v2/bol_api.json in hetzelfde formaat als matcher v2: {cbid: [prijs, beschikbaar, verkoper, verzend, url, naam, ean, vlag]}"""
import json, os, re, sys, glob, time, urllib.request, urllib.parse
K = open('/home/claude/.dumpkey').read().strip()
F = 'https://bespaarvriend.nl/api/bol?k=' + K
V2 = '/home/claude/bespaarvriend/elektronica/raw/v2'
DUMP = f'https://elektrovergelijk.netlify.app/api/dump?k={K}&n='


def get(url):
    for i in range(3):
        try:
            return json.loads(urllib.request.urlopen(url, timeout=30).read().decode() or '{}')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {}
            time.sleep(2)
        except Exception:
            time.sleep(2)
    return {}


def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def offer(p):
    o = p.get('offer') or (p.get('offers') or [None])[0] or {}
    prijs = o.get('price') or (o.get('pricing') or {}).get('price')
    return prijs, o


items = []
for naam in (sys.argv[1].split(',') if len(sys.argv) > 1 else ['items', 'items2']):
    items += json.loads(urllib.request.urlopen(DUMP + naam).read() or '[]')
print(len(items), 'items', flush=True)
eans = {}
for f in glob.glob(os.path.join(V2, '*_*.json')):
    if os.path.basename(f).startswith(('cb_', 'bol_')):
        continue
    try:
        for k, r in json.load(open(f)).items():
            g = (r + [None] * 8)[6]
            if g and re.fullmatch(r'\d{12,14}', str(g)):
                eans.setdefault(k, str(g).zfill(13))
    except Exception:
        pass
res, voorbeeld = {}, None
for it in items:
    k = str(it['k'])
    p = None
    if k in eans:
        d = get(F + '&ean=' + eans[k])
        p = d if d.get('ean') or d.get('title') else None
    if not p:
        d = get(F + '&n=5&q=' + urllib.parse.quote(it['q']))
        for c in d.get('results', d.get('products', [])) or []:
            c = c.get('product', c)
            t = norm(c.get('title', ''))
            if (it.get('m') and it['m'] in t) or (it.get('loose') and all(norm(w) in t for w in it['t'] if w not in ('zwart', 'wit', 'blauw', 'grijs', 'zilver'))):
                p = c; break
    if not p:
        continue
    voorbeeld = voorbeeld or p
    prijs, o = offer(p)
    if not prijs:
        continue
    ratio = float(prijs) / it['p']
    if ratio < 0.55 or ratio > 1.8:
        continue
    lev = (o.get('deliveryDescription') or '').lower()
    if 'niet leverbaar' in lev or 'tijdelijk' in lev:
        continue
    url = p.get('url', '')
    res[k] = [float(prijs), 'InStock', 'bol', None, url, p.get('title', '')[:120], p.get('ean', ''), 'e' if k in eans else 't']
    if len(res) % 100 == 0:
        print(len(res), flush=True)
json.dump(res, open(os.path.join(V2, os.environ.get('UIT', 'bol_api') + '.json'), 'w'))
print(len(res), 'bol-prijzen; voorbeeld:', json.dumps(voorbeeld)[:600] if voorbeeld else None)
