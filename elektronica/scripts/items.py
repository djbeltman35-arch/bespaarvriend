"""Maakt de zoeklijst voor matcher v2 uit de Coolblue-oogst (cb_<cat>) en zet hem in de dump als 'items'."""
import json, re, sys, urllib.request
K = open('/home/claude/.dumpkey').read().strip()
API = f'https://elektrovergelijk.netlify.app/api/dump?k={K}&n='
CATS = sys.argv[1].split(',') if len(sys.argv) > 1 else None
LOOSE = {'smartphones', 'tablets', 'smartwatches', 'koptelefoons', 'oordopjes', 'speakers', 'spelcomputers'}
VAR = ['pro', 'max', 'plus', 'ultra', 'mini', 'fe', 'lite', 'air', 'se', 'neo', 'edge', 'xl']
STOP = {'gb', 'tb', 'inch', 'met', 'en', 'de', 'het', 'wifi', 'wi', 'fi', 'zwart'}
def get(n):
    return urllib.request.urlopen(API + n).read().decode()
def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())
def tokens(name):
    w = re.findall(r'[a-z0-9+]+', name.lower().replace('(', ' ').replace(')', ' '))
    t = [x for x in w if (x not in STOP or x == 'zwart') and not re.fullmatch(r'20\d\d', x) and x not in ('5g', 'inch')][:8]
    return t
def build(cats):
    items = []
    for c in cats:
        raw = get('cb_' + c)
        if not raw: continue
        for x in json.loads(raw):
            if not x.get('p'): continue
            m = norm(x.get('mpn') or '')
            loose = c.split('__')[0] in LOOSE
            name = x['n']
            t = tokens(name)
            xs = [v for v in VAR if v not in t] + (['cellular', '5g', 'lte', '4g'] if c.split('__')[0] == 'tablets' and not {'5g', 'cellular', 'lte'} & set(name.lower().split()) else [])
            q = name if (loose or len(m) < 5) else x['mpn']
            items.append({'k': x['id'], 'c': c.split('__')[0], 'q': q, 'm': m if len(m) >= 5 else '', 'p': x['p'], 't': t, 'x': xs, 'loose': loose or len(m) < 5})
    return items
if __name__ == '__main__':
    cats = CATS or [l for l in get('').split() if l.startswith('cb_')]
    cats = [c.replace('cb_', '') for c in cats]
    items = build(cats)
    req = urllib.request.Request(API + (sys.argv[2] if len(sys.argv) > 2 else 'items'), data=json.dumps(items).encode(), method='POST')
    print(urllib.request.urlopen(req).read().decode(), len(items), 'items')
