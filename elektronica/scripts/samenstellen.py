#!/usr/bin/env python3
"""Voegt de opgehaalde winkelprijzen samen tot data/prijzen.json.
Elke gevonden aanbieding wordt nog eens gecontroleerd: de productnaam bij de winkel moet
het typenummer/de uitvoering bevatten, anders telt hij niet mee."""
import json, os, re, unicodedata, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(ROOT, 'data', 'config.json')))

KLEUREN = {'zwart', 'blauw', 'grijs', 'zilver', 'groen'}
ACCESSOIRE = ['oorkussen', 'hoesje', 'opberghoes', 'beschermhoes', 'oplader', 'bandje', 'screenprotector', 'beschermfolie',
              'faceplate', 'opzetborstel', 'filterset', 'vervangingsfilter', 'stofzuigerzak', 'onderdelen', 'tamper', 'waterfilter',
              'inktcartridge', 'accessoire', 'discdrive', 'bundel', 'bundle', 'refurbished', 'refurb', 'gebruikt', 'tweedehands',
              'renewed', 'oordopjes tips', 'standaard voor', 'soundbar zwart tv']
EXTRA_UIT = {  # extra uitsluitingen per product (index)
    85: ['compact'], 88: ['plus', 'mac'], 157: ['pro'], 14: ['2024'], 20: ['kg5nl'], 66: ['drive'], 51: ['882826'], 64: ['system'],
}
APPARAAT = {'wasmachines', 'wasdrogers', 'koelkasten', 'vriezers', 'vaatwassers', 'ovens', 'kookplaten', 'magnetrons', 'koffie',
            'scheerapparaten', 'tandenborstels', 'airfryers', 'steelstofzuigers', 'robotstofzuigers', 'speakers', 'soundbars',
            'koptelefoons', 'oordopjes', 'muizen', 'toetsenborden', 'printers'}


def comp(s):
    s = unicodedata.normalize('NFD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', s)


def spaced(s):
    s = unicodedata.normalize('NFD', s or '').encode('ascii', 'ignore').decode().lower()
    return ' ' + re.sub(r'[^a-z0-9+]+', ' ', s) + ' '


def past(txt, item, idx):
    c, sp = comp(txt), spaced(txt)
    for t in item['i']:
        if t in KLEUREN:
            continue
        if comp(t) not in c:
            return False
    for x in item['x'] + EXTRA_UIT.get(idx, []):
        if x == '+':
            if '+' in txt:
                return False
            continue
        if (' ' + x.lower() + ' ') in sp or (len(x) > 4 and comp(x) in c):
            return False
    for a in ACCESSOIRE:
        if a in txt.lower():
            return False
    return True


def ander_typenummer(naam, item):
    """True als de naam een typenummer bevat dat niet bij dit product hoort (bv. EY905B i.p.v. EY9428)."""
    eigen = {comp(t) for t in item['i']}
    for w in re.findall(r'[A-Za-z]*\d[A-Za-z0-9./-]{3,}', naam):
        cw = comp(w)
        if len(cw) >= 5 and re.search(r'[a-z]', cw) and re.search(r'\d', cw) and not any(e in cw or cw in e for e in eigen):
            if not re.fullmatch(r'\d+(gb|tb|mm|cm|w|l|kg|hz|pa|db|inch)', cw):
                return True
    return False


# Productlijst uit de catalogus
items = []
for l in open(os.path.join(ROOT, 'raw', 'catalogus.txt')):
    if l.startswith('#') or not l.strip():
        continue
    p = l.rstrip('\n').split('|')
    cat, naam, prijs, cbid, q, inc = p[:6]
    exc = p[6] if len(p) > 6 else ''
    items.append({'cat': cat, 'naam': naam, 'cb': (float(prijs), cbid), 'i': inc.split(), 'x': [e[1:] for e in exc.split() if len(e) > 1]})


def lees(bestand):
    t = open(os.path.join(ROOT, 'raw', bestand)).read().strip()
    if ' ## ' in t:
        recs = t.split(' ## ')
    elif '\n' in t:
        recs = t.split('\n')
    else:
        recs = re.split(r' (?=\d{1,3}\|\d)', t)
    out = []
    for r in recs:
        f = r.split('|', 6)
        if len(f) < 7:
            continue
        out.append({'k': int(f[0]), 'p': float(f[1]), 'a': f[2], 'sel': f[3].strip(), 'v': f[4], 'u': f[5], 'n': f[6]})
    return out


BASIS = {'azerty': 'https://azerty.nl', 'mobiel': 'https://www.mobiel.nl', 'bcc': 'https://www.bcc.nl', 'mediamarkt': 'https://www.mediamarkt.nl/nl/product/_', 'bol': 'https://www.bol.com/nl/nl/p/',
         'amazon': 'https://www.amazon.nl', 'alternate': 'https://www.alternate.nl'}
EIGEN = {'mediamarkt': {'', 'mediamarkt'}, 'bol': {'bol', 'bol.com', ''}, 'amazon': {'', 'amazon', 'amazon.nl', 'amazon eu s.a r.l.'},
         'alternate': {'alternate', 'alternate computerversand nederland c.v.'}, 'azerty': {''}, 'mobiel': {''}, 'bcc': {''}}

aanb = {i: [] for i in range(len(items))}
log = []
for i, it in enumerate(items):
    p, cbid = it['cb']
    aanb[i].append({'winkel': 'coolblue', 'prijs': p, 'verzend': 0, 'url': f'https://www.coolblue.nl/product/{cbid}/'})

for winkel, bestand in [('mediamarkt', 'mediamarkt.txt'), ('bol', 'bol.txt'), ('amazon', 'amazon.txt'), ('alternate', 'alternate.txt'), ('azerty', 'azerty.txt'), ('mobiel', 'mobiel.txt'), ('bcc', 'bcc.txt')]:
    if not os.path.exists(os.path.join(ROOT, 'raw', bestand)):
        continue
    ok = nee = 0
    for r in lees(bestand):
        it = items[r['k']]
        if r['a'] and r['a'] not in ('InStock', 'LimitedAvailability', 'PreOrder', 'OnlineOnly'):
            nee += 1; log.append(f'{winkel} {r["k"]} niet op voorraad'); continue
        goed = past(r['n'], it, r['k'])
        if not goed and it['cat'] in APPARAAT and past(re.sub(r'\d{5,}', '', r['u']).replace('-', ' '), it, r['k']) and not ander_typenummer(r['n'], it):
            goed = True
        if not goed:
            nee += 1; log.append(f'{winkel} {r["k"]} afgekeurd: {r["n"][:70]}'); continue
        prijs = r['p']
        # Ongeloofwaardige prijs (meer dan 60% goedkoper of 2,5x duurder dan Coolblue): waarschijnlijk ander product
        ref = it['cb'][0]
        lo, hi = (0.75, 1.5) if winkel == 'amazon' else (0.4, 2.5)
        if prijs < ref * lo or prijs > ref * hi:
            nee += 1; log.append(f'{winkel} {r["k"]} prijs onwaarschijnlijk {prijs} vs {ref}'); continue
        sel = r['sel']
        eigen = sel.lower() in EIGEN[winkel]
        if not eigen and prijs < ref * 0.65:
            nee += 1; log.append(f'{winkel} {r["k"]} verdacht goedkope partner {prijs} vs {ref}'); continue
        if winkel == 'mediamarkt':
            if prijs < 50:
                nee += 1; continue  # verzendkosten onder € 50 onbekend
            verzend = 0
        elif winkel == 'bol':
            verzend = 2.99 if (eigen and prijs < 25) else 0
        elif winkel == 'amazon':
            verzend = 2.99 if prijs < 20 else 0
        elif winkel == 'mobiel':
            verzend = 0
        elif winkel == 'azerty':
            v_ = float(r['v'] or 0)
            verzend = round(v_ * 1.21, 2) if v_ else 0  # Azerty geeft verzendkosten excl. btw
        else:
            verzend = float(r['v']) if r['v'] not in ('', 'None', 'null') else None
            if verzend is None:
                nee += 1; continue
        url = BASIS[winkel] + r['u'] if winkel in ('mediamarkt', 'bol') else BASIS[winkel] + r['u']
        aanb[r['k']].append({'winkel': winkel, 'prijs': prijs, 'verzend': verzend, 'url': url,
                             'verkoper': '' if eigen or winkel in ('alternate', 'amazon', 'azerty', 'mobiel', 'bcc') else sel})
        ok += 1
    log.append(f'== {winkel}: {ok} goed, {nee} afgekeurd/overgeslagen')


def slug(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower().replace('+', ' plus ').replace('"', ' inch ')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


producten = []
for i, it in enumerate(items):
    of = aanb[i]
    # per winkel alleen de goedkoopste
    beste = {}
    for o in of:
        t = o['prijs'] + (o['verzend'] or 0)
        if o['winkel'] not in beste or t < beste[o['winkel']]['prijs'] + (beste[o['winkel']]['verzend'] or 0):
            beste[o['winkel']] = o
    naam = re.sub(r'\s+(Zwart|Blauw|Grijs|Zilver|Groen|Wit)\b', '', it['naam'])
    producten.append({'slug': slug(naam), 'naam': naam, 'cat': it['cat'], 'merk': naam.split()[0].replace("De'Longhi", "De'Longhi"),
                      'aanbiedingen': list(beste.values())})

specs = {}
_sp = os.path.join(ROOT, 'raw', 'specs.txt')
if os.path.exists(_sp):
    for rec in open(_sp).read().strip().split(' ## '):
        idx, _, rest = rec.partition('|')
        specs[idx.strip()] = dict(kv.split('=', 1) for kv in rest.split(';') if '=' in kv)
_sp2 = os.path.join(ROOT, 'raw', 'specs2.txt')
if os.path.exists(_sp2):
    for line in open(_sp2):
        idx, _, rest = line.strip().partition('|')
        if idx:
            specs.setdefault(idx, {}).update(dict(kv.split('=', 1) for kv in rest.split(';') if '=' in kv))
for i, p in enumerate(producten):
    p['kenmerken'] = specs.get(items[i]['cb'][1], {})
producten = [p for p in producten if len(p['aanbiedingen']) >= 2]
data = dict(cfg)
data['producten'] = producten
data['bijgewerkt'] = datetime.date.today().strftime('%-d %B %Y').replace('November', 'november').replace('December', 'december')
data['versie'] = datetime.datetime.now().strftime('%Y%m%d%H%M')
json.dump(data, open(os.path.join(ROOT, 'data', 'prijzen.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ROOT, 'raw', 'controle.log'), 'w').write('\n'.join(log))
n = [len(p['aanbiedingen']) for p in producten]
print(len(producten), 'producten; gemiddeld', round(sum(n) / len(n), 2), 'winkels; met >=2 winkels:', sum(1 for x in n if x >= 2))
print('\n'.join(l for l in log if l.startswith('==')))
