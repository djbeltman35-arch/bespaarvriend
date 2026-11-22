#!/usr/bin/env python3
"""Versie 2: bouwt data/prijzen.json uit de Coolblue-oogst (raw/v2/cb_<cat>.json) en de winkelresultaten
(raw/v2/<winkel>_*.json) van matcher v2 (tools/m2.js). Een winkelresultaat telt alleen als de fabrikantcode
op de productpagina stond (vlag 'm') of, bij telefoons/tablets/audio, alle naamwoorden klopten (vlag 't').

Producten uit de oude catalogus (samenstellen.py) die niet in de nieuwe oogst zitten, blijven behouden.
Gebruik: python3 scripts/samenstellen2.py"""
import json, os, re, glob, unicodedata, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = os.path.join(ROOT, 'raw', 'v2')
cfg = json.load(open(os.path.join(ROOT, 'data', 'config.json')))
_ob = os.path.join(ROOT, 'raw', 'prijzen_basis.json')  # vaste basis met de oude producten (v1)
oud = json.load(open(_ob if os.path.exists(_ob) else os.path.join(ROOT, 'data', 'prijzen.json')))

WINKEL = {'mm': 'mediamarkt', 'amz': 'amazon', 'alt': 'alternate', 'az': 'azerty', 'bol': 'bol', 'mob': 'mobiel', 'bcc': 'bcc'}
BASIS = {'mediamarkt': 'https://www.mediamarkt.nl', 'amazon': 'https://www.amazon.nl', 'alternate': 'https://www.alternate.nl',
         'azerty': 'https://azerty.nl', 'bol': 'https://www.bol.com', 'mobiel': 'https://www.mobiel.nl', 'bcc': 'https://www.bcc.nl'}
EIGEN = {'mediamarkt': {'', 'mediamarkt', 'media markt'}, 'bol': {'bol', 'bol.com', ''}, 'amazon': {'', 'amazon', 'amazon.nl', 'amazon eu s.a r.l.'}}
ACCESSOIRE = ['oorkussen', 'hoesje', 'opberghoes', 'beschermhoes', 'bandje', 'screenprotector', 'beschermfolie', 'opzetborstel',
              'vervangingsfilter', 'stofzuigerzak', 'onderdeel', 'inktcartridge', 'bundel', 'bundle', 'refurbished', 'refurb',
              'gebruikt', 'tweedehands', 'renewed', 'b-grade', 'demo']
OK_BESCHIKBAAR = {'', 'InStock', 'LimitedAvailability', 'PreOrder', 'OnlineOnly', 'BackOrder'}
KLEUR = r'\s+(Zwart|Blauw|Grijs|Zilver|Groen|Wit|Roze|Paars|Oranje|Rood|Geel|Goud|Beige|Bruin|Titanium|Bordeaux Rood|Donkerblauw|Lichtblauw|Mint|Lavendel|Crème|Creme|Antraciet|Zand)\b.*$'
SPEC_KEYS = {k for p in oud['producten'] for k in p.get('kenmerken', {})} | {'Schermdiagonaal', 'Totale opslagcapaciteit', 'Energieklasse',
             'Inhoud', 'Toerental centrifugeren', 'Vulgewicht', 'Processor', 'Intern werkgeheugen (RAM)', 'Videokaart chipset', 'Noise cancelling'}
log = []


def slug(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower().replace('+', ' plus ').replace('"', ' inch ')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def lees(pad):
    try:
        t = open(pad).read().strip()
        return json.loads(t) if t else {}
    except Exception:
        return {}


# 1. Coolblue-basis
basis = {}
for f in sorted(glob.glob(os.path.join(V2, 'cb_*.json'))):
    cat = os.path.basename(f)[3:-5].split('__')[0]
    for x in lees(f) or []:
        if not x.get('p') or x.get('a') not in ('InStock', 'LimitedAvailability', 'PreOrder', 'OnlineOnly', ''):
            continue
        if any(a in x['n'].lower() for a in ACCESSOIRE):
            continue
        basis[str(x['id'])] = dict(x, cat=cat)

# 2. Winkelresultaten (meerdere bestanden per winkel mogelijk: mm_1, mm_2, ...)
aanb = {k: [{'winkel': 'coolblue', 'prijs': float(x['p']), 'verzend': 0, 'url': f'https://www.coolblue.nl/product/{k}/'}] for k, x in basis.items()}
for f in sorted(glob.glob(os.path.join(V2, '*_*.json'))):
    naam = os.path.basename(f)[:-5]
    pre = naam.split('_')[0]
    if pre == 'cb' or pre not in WINKEL:
        continue
    winkel = WINKEL[pre]
    goed = nee = 0
    for k, r in (lees(f) or {}).items():
        if k not in basis:
            continue
        prijs, besch, sel, ship, url, pnaam, gtin, vlag = (r + [None] * 8)[:8]
        ref = float(basis[k]['p'])
        if besch not in OK_BESCHIKBAAR:
            nee += 1; continue
        if any(a in (pnaam or '').lower() for a in ACCESSOIRE):
            nee += 1; continue
        lo, hi = (0.7, 1.5) if winkel == 'amazon' else (0.55, 1.8)
        if not prijs or prijs < ref * lo or prijs > ref * hi:
            nee += 1; log.append(f'{winkel} {k} prijs {prijs} vs {ref}'); continue
        sel = (sel or '').strip()
        eigen = sel.lower() in EIGEN.get(winkel, {''}) or winkel not in EIGEN
        if not eigen and prijs < ref * 0.65:
            nee += 1; continue
        if winkel == 'mediamarkt':
            if prijs < 50:
                nee += 1; continue
            verzend = 0
        elif winkel == 'bol':
            verzend = 2.99 if (sel.lower() in ('bol', 'bol.com') and prijs < 25) else 0
        elif winkel == 'amazon':
            verzend = 2.99 if prijs < 20 else 0
        elif winkel == 'azerty':
            verzend = round(float(ship) * 1.21, 2) if ship else 0
        elif winkel == 'alternate':
            if ship is None:
                nee += 1; continue
            verzend = float(ship)
        else:
            verzend = 0
        if not url.startswith('http'):
            url = BASIS[winkel] + url
        aanb[k].append({'winkel': winkel, 'prijs': float(prijs), 'verzend': verzend, 'url': url, 'verkoper': '' if eigen else sel})
        goed += 1
    log.append(f'== {naam}: {goed} goed, {nee} afgekeurd')

# 2b. Oude aanbiedingen (bv. bol, Mobiel.nl) behouden voor winkels die deze keer niet opnieuw zijn opgehaald
opgehaald = {WINKEL[os.path.basename(f).split('_')[0]] for f in glob.glob(os.path.join(V2, '*_*.json')) if os.path.basename(f).split('_')[0] in WINKEL and not os.path.basename(f).startswith('cb_')}
for p in oud['producten']:
    cbid = next((re.search(r'/product/(\d+)/', o['url']).group(1) for o in p['aanbiedingen'] if o['winkel'] == 'coolblue'), None)
    if cbid in aanb:
        for o in p['aanbiedingen']:
            if o['winkel'] != 'coolblue' and not any(x['winkel'] == o['winkel'] for x in aanb[cbid]):
                aanb[cbid].append(o)

# 2c. Per categorie de meest voorkomende kenmerken toestaan (voor nieuwe categorieën)
from collections import Counter as _C
_SKIP = {'Fabrikantcode', 'Breedte', 'Hoogte', 'Diepte', 'Gewicht', 'Kleur', 'Garantie', 'Materiaal', 'Merk', 'Productnaam', 'Gewicht in gram'}
CAT_KEYS = {}
for _cat in {x['cat'] for x in basis.values()}:
    _c = _C(k for x in basis.values() if x['cat'] == _cat for k in (x.get('sp') or {}) if k not in _SKIP and not k.startswith('Garantie'))
    CAT_KEYS[_cat] = {k for k, _ in _c.most_common(14)}

# 3. Samenvoegen per productnaam zonder kleur (kleurvarianten worden één product)
per = {}
for k, x in basis.items():
    naam = re.sub(KLEUR, '', x['n']).strip()
    naam = re.sub(r'\s+(5G|4G)$', '', naam)
    s = slug(naam)
    p = per.setdefault(s, {'slug': s, 'naam': naam, 'cat': x['cat'], 'merk': (x.get('b') or naam.split()[0]), 'aanbiedingen': [], 'kenmerken': {}})
    p['aanbiedingen'] += aanb[k]
    for kk, vv in (x.get('sp') or {}).items():
        if (kk in SPEC_KEYS or kk in CAT_KEYS.get(x['cat'], ())) and kk not in p['kenmerken']:
            p['kenmerken'][kk] = vv
producten = []
for p in per.values():
    beste = {}
    for o in p['aanbiedingen']:
        t = o['prijs'] + (o['verzend'] or 0)
        if o['winkel'] not in beste or t < beste[o['winkel']]['prijs'] + (beste[o['winkel']]['verzend'] or 0):
            beste[o['winkel']] = o
    cb = beste.get('coolblue', {}).get('prijs')
    p['aanbiedingen'] = [o for o in beste.values() if not cb or 0.55 * cb <= o['prijs'] <= 1.6 * cb]
    if len(p['aanbiedingen']) >= 2:
        producten.append(p)

# 4. Oude producten die niet in de nieuwe oogst zitten behouden
nieuw = {p['slug'] for p in producten}
cb_nieuw = set(basis)
for p in oud['producten']:
    cbid = next((re.search(r'/product/(\d+)/', o['url']).group(1) for o in p['aanbiedingen'] if o['winkel'] == 'coolblue'), None)
    if p['slug'] not in nieuw and cbid not in cb_nieuw:
        producten.append(p)

def _schoon(p):
    cb = next((o['prijs'] for o in p['aanbiedingen'] if o['winkel'] == 'coolblue'), None)
    p['aanbiedingen'] = [o for o in p['aanbiedingen'] if not cb or 0.55 * cb <= o['prijs'] <= 1.6 * cb]
    return len(p['aanbiedingen']) >= 2
producten = [p for p in producten if _schoon(p)]

data = dict(cfg)
data['producten'] = producten
data['bijgewerkt'] = datetime.date.today().strftime('%-d %B %Y').replace('November', 'november').replace('December', 'december').replace('January', 'januari')
data['versie'] = datetime.datetime.now().strftime('%Y%m%d%H%M')
json.dump(data, open(os.path.join(ROOT, 'data', 'prijzen.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ROOT, 'raw', 'controle2.log'), 'w').write('\n'.join(log))
n = [len(p['aanbiedingen']) for p in producten]
from collections import Counter
print(len(producten), 'producten; gemiddeld', round(sum(n) / len(n), 2), 'winkels')
print(Counter(p['cat'] for p in producten).most_common())
print('\n'.join(l for l in log if l.startswith('==')))
