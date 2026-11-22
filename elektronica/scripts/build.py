#!/usr/bin/env python3
"""Bouwt de statische site uit data/prijzen.json naar de map public/ (of het opgegeven pad)."""
import json, os, re, sys, shutil, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else 'public')
SITE = 'Elektrovergelijk'
DOMEIN = os.environ.get('SITE_DOMEIN', 'https://elektrovergelijk.netlify.app')
B = os.environ.get('SITE_BASIS', '').rstrip('/')  # bv. /elektronica als de vergelijker onder Bespaarvriend draait
MAIL = os.environ.get('CONTACT_MAIL', '')  # contactadres via omgevingsvariabele (Netlify)

data = json.load(open(os.path.join(ROOT, 'data', 'prijzen.json')))
WINKELS = data['winkels']
CATS = data['categorieen']
GROEPEN = data['groepen']
PRODUCTEN = data['producten']
JAAR = datetime.date.today().year
BIJGEWERKT = data['bijgewerkt']
SUBS = data.get('subcategorieen', {})


def _subs_van(p):
    n = p['naam'].lower()
    best = min(o['prijs'] + (o['verzend'] or 0) for o in p['aanbiedingen'])
    uit = []
    for slug_, naam_, woorden in SUBS.get(p['cat'], []):
        for w in woorden:
            if w.startswith('@merk:'):
                if p['merk'].lower() == w[6:]:
                    uit.append(slug_); break
                continue
            if w.startswith('@spec:'):  # @spec:Kenmerk=deel van waarde  of  @spec:Kenmerk==exacte waarde
                k_, _, v_ = w[6:].partition('=')
                waarde = str(p.get('kenmerken', {}).get(k_, '')).lower()
                ok_ = waarde == v_[1:].lower() if v_.startswith('=') else (v_.lower() in waarde and waarde != '')
                if ok_:
                    uit.append(slug_); break
                continue
            if w == '@alles' or (w.startswith('@max') and best <= float(w[4:])) or (not w.startswith('@') and w in n):
                uit.append(slug_); break
    return uit


HANDMATIG_INCH = {'Samsung Galaxy Tab A11 Plus': '11', 'Samsung Galaxy Tab S10 FE': '10,9', '34U650A': '34', 'U32G4U': '31,5',
                  '27UP850K': '27', '346E2CUAE': '34', '27GX704A': '26,5', 'Q27G4ZDR': '26,5'}
INCH_CATS = {'televisies', 'monitoren', 'tablets', 'laptops'}
OPSLAG_CATS = {'smartphones', 'tablets', 'ssd', 'laptops'}


def _kenmerken(p):
    n = p['naam']
    k = {}
    if p['cat'] in INCH_CATS:
        m = re.search(r'(?<!\d)(\d{2,3}(?:[,.]\d)?)\s*(?:"|inch\b)', n)
        val = m.group(1).replace('.', ',') if m else next((v for key, v in HANDMATIG_INCH.items() if key in n), None)
        if val:
            k['Schermformaat'] = val + ' inch'
    if p['cat'] in OPSLAG_CATS:
        m = re.findall(r'(\d+)\s*(GB|TB)', n)
        if m:
            num, eh = m[-1]
            k['Opslag'] = f'{num} {eh}'
    if p['cat'] == 'smartwatches':
        m = re.search(r'(\d{2})\s*mm', n)
        if m:
            k['Kastmaat'] = m.group(1) + ' mm'
    return k


FILTERS = ['Schermtype', 'Scherpte', 'Paneeltype', 'Verversingssnelheid', 'Beeldverhouding', 'Smart platform', 'Type SSD',
           'Afdruktechnologie', 'Type printer', 'Type verbinding', 'Type ergonomie', 'Type vaatwasser', 'Droogtechniek', 'Type wasdroger',
           'Maximaal vulgewicht drogen', 'Verwarming kookplaat', 'Aansluiting op aantal fasen in Nederland', 'Plaatsing apparaat',
           'Type oven / magnetron', 'Reinigingsmethode', 'Aantal lades', 'Bedieningsmogelijkheden', 'Melkopschuimmethode', 'Poetstechniek tandenborstel',
           'Type oorkussen', 'IP-certificering', 'Internetverbinding opties', 'Compatibel met besturingssysteem', 'Processor', 'Intern werkgeheugen (RAM)',
           'Dweilfunctie', 'Reinigingsstation', 'Type koffiezetapparaat', 'Type koffie/vulling', 'Model koelkast/vriezer', 'Anti-ijsvorming', 'Type wasmachine',
           'Vulgewicht', 'Toerental centrifugeren', 'Noise cancelling', 'Multipoint pairing', 'Waterdichtheid', 'Wifi ingebouwd', 'Multiroom audio',
           'Formaat draadloze speaker', 'Losse subwoofer', 'Dolby Atmos', 'Local dimming', 'Besturingssysteem', 'Geschikt voor gaming', 'Verlicht toetsenbord',
           'Geografische toetsenbordindeling', 'Type inkt', 'Fotoprinter', 'Scheerkop', 'Aantal couverts', 'Bestekvoorziening', 'Compatibel met smartphone / apps',
           'Uitschakelbaar draaiplateau', 'Volledig draadloze oordopjes', 'Met heatsink']
LABEL = {'Aansluiting op aantal fasen in Nederland': 'Aansluiting', 'Maximaal vulgewicht drogen': 'Vulgewicht', 'Poetstechniek tandenborstel': 'Poetstechniek',
         'Compatibel met besturingssysteem': 'Werkt met', 'Internetverbinding opties': 'Verbinding', 'Intern werkgeheugen (RAM)': 'Werkgeheugen',
         'Type oven / magnetron': 'Type', 'Totale opslagcapaciteit': 'Opslag', 'Schermdiagonaal': 'Schermformaat'}
KAART_SPECS = {'televisies': ['Schermtype', 'Scherpte', 'Verversingssnelheid'], 'monitoren': ['Scherpte', 'Paneeltype', 'Verversingssnelheid'],
               'ssd': ['Type SSD', 'Maximale leessnelheid'], 'wasdrogers': ['Maximaal vulgewicht drogen', 'Maximaal geluidsniveau'],
               'vaatwassers': ['Type vaatwasser', 'Maximaal geluidsniveau'], 'kookplaten': ['Verwarming kookplaat', 'Aansluiting op aantal fasen in Nederland'],
               'printers': ['Afdruktechnologie', 'Type printer'], 'speakers': ['Maximale accu/batterijduur', 'IP-certificering'],
               'oordopjes': ['Gemiddelde accuduur'], 'smartwatches': ['Accuduur in tijdmodus'], 'airfryers': ['Aantal lades', 'Vermogen'],
               'laptops': ['Processor', 'Intern werkgeheugen (RAM)'], 'magnetrons': ['Type oven / magnetron', 'Magnetronvermogen'],
               'koffie': ['Type koffiezetapparaat', 'Melkopschuimmethode'], 'steelstofzuigers': ['Maximale accu/batterijduur', 'Maximaal geluidsniveau'],
               'robotstofzuigers': ['Zuigkracht', 'Dweilfunctie'], 'koelkasten': ['Model koelkast/vriezer', 'Netto inhoud'], 'vriezers': ['Netto inhoud'],
               'wasmachines': ['Vulgewicht', 'Toerental centrifugeren'], 'koptelefoons': ['Gewicht in gram'], 'scheerapparaten': ['Scheerkop'], 'tandenborstels': ['Poetstechniek tandenborstel'], 'soundbars': ['Breedte']}
PRIJSKLASSEN = [(50, 'Tot € 50'), (100, '€ 50 – 100'), (250, '€ 100 – 250'), (500, '€ 250 – 500'), (1000, '€ 500 – 1.000'), (10 ** 9, 'Vanaf € 1.000')]


def _sortwaarde(v):
    if v.startswith('Tot €'):
        return -1
    if v.startswith('€') or v.startswith('Vanaf €'):
        return float(re.sub(r'[^\d]', '', v.split('–')[0]) or 0)
    m = re.match(r'([\d,]+)\s*(\w+)', v)
    if not m:
        return hash(v) % 1000 / 1000 + 10 ** 6
    x = float(m.group(1).replace(',', '.'))
    return x * 1000 if m.group(2) == 'TB' else x


def spec_slug(v):
    return re.sub(r'[^a-z0-9]+', '-', v.lower().replace(',', '-')).strip('-')


# Automatische subcategorieën (zoals bij de grote webwinkels): per merk en per belangrijk kenmerk.
_GEEN = {'Artikelnummer', 'Afhandeling van je defect', 'Oude apparaat gratis retour', 'Hoogte', 'Breedte', 'Diepte', 'Gewicht',
         'Introductiejaar', 'Fabrikantcode', 'Kleur', 'Merk', 'Garantie', 'Productnaam', 'Bluetooth', 'Smart TV', 'Kleurdiepte',
         'HDR ondersteuning', 'Energieklasse'}


def _auto_subs():
    from collections import Counter, defaultdict
    per = defaultdict(list)
    for p in PRODUCTEN:
        per[p['cat']].append(p)
    for cat, ps in per.items():
        bestaand = SUBS.setdefault(cat, [])
        slugs = {s[0] for s in bestaand}
        namen = {s[1].lower() for s in bestaand}
        _nm = lambda x: re.sub(r'[^a-z0-9]', '', x.lower())
        kern = [_nm(s[1]) for s in bestaand]
        dubbel = lambda v: any(c.startswith(_nm(v)) for c in kern if _nm(v))
        # kenmerken: 2 sleutels met 2-8 waarden die elk bij minstens 3 producten voorkomen
        kandidaten = []
        for k in {k for p in ps for k in p.get('kenmerken', {})} - _GEEN:
            if k.startswith('Garantie') or not re.search(r'type|soort|systeem|installatie|plaatsing|uitvoering|technologie', k, re.I) or re.search(r'etui|sluiting|aansluiting|connector|stroom|voeding|processor|batterij|accu|accessoire|pakket|ergonom|hdr|bediening|motor|verbinding|besturing|kabel|geheugenkaart|filter|lade', k, re.I):
                continue
            c = Counter(p['kenmerken'][k] for p in ps if k in p['kenmerken'])
            goed = [(v, n) for v, n in c.items() if n >= 3 and len(v) <= 30 and ',' not in v and not re.fullmatch(r'[\d.,\s]+[a-zA-Z]{0,3}', v) and v.lower() not in ('ja', 'nee', 'geen', 'gedeeltelijk', 'onbekend', 'basis', 'uitgebreid', 'standaard', 'overig', 'anders')]
            if 2 <= len(goed) <= 8 and sum(n for _, n in goed) >= len(ps) * 0.5:
                kandidaten.append((sum(n for _, n in goed), k, goed))
        for _, k, goed in sorted(kandidaten, reverse=True)[:2]:
            for v, n in sorted(goed, key=lambda x: -x[1]):
                sl = spec_slug(v)
                if sl and sl not in slugs and v.lower() not in namen and not dubbel(v) and not sl.endswith('-inch'):
                    bestaand.append([sl, v, [f'@spec:{k}=={v}']]); slugs.add(sl); namen.add(v.lower())
        # merken met minstens 3 producten
        for m, n in Counter(p['merk'] for p in ps).most_common(10):
            sl = spec_slug(m)
            if n >= 3 and sl and sl not in slugs and m.lower() not in namen and not dubbel(m):
                bestaand.append([sl, m, ['@merk:' + m.lower()]]); slugs.add(sl); namen.add(m.lower())


_auto_subs()

for _p in PRODUCTEN:
    _p['subs'] = _subs_van(_p)
    _p['spec'] = _kenmerken(_p)
    _km = _p.get('kenmerken', {})
    if 'Opslag' not in _p['spec'] and _km.get('Totale opslagcapaciteit') and _p['cat'] in OPSLAG_CATS:
        _p['spec']['Opslag'] = _km['Totale opslagcapaciteit']
    if 'Schermformaat' not in _p['spec'] and _km.get('Schermdiagonaal') and _p['cat'] in INCH_CATS:
        _p['spec']['Schermformaat'] = _km['Schermdiagonaal']
    for _k in FILTERS:
        if _km.get(_k):
            _p['spec'][LABEL.get(_k, _k)] = _km[_k]
    _b = min(o['prijs'] + (o['verzend'] or 0) for o in _p['aanbiedingen'])
    _p['spec']['Prijsklasse'] = next(n for g_, n in PRIJSKLASSEN if _b < g_)
    _p['kaartspec'] = [v for v in [_p['spec'].get('Schermformaat'), _p['spec'].get('Opslag'), _p['spec'].get('Kastmaat')] if v] + \
                      [_km[k] for k in KAART_SPECS.get(_p['cat'], []) if _km.get(k)]
    _p['merk'] = _p['naam'].split()[0]


def gpad(cat):
    return f"/{CATS[cat]['groep']}/{cat}/"


def actieve_subs(cat):
    return [(s_, n_) for s_, n_, _ in SUBS.get(cat, []) if any(s_ in p['subs'] for p in PRODUCTEN)]


def maak_menu():
    delen = []
    for g in GROEPEN:
        cats = [c for c, v in CATS.items() if v['groep'] == g['slug'] and any(p['cat'] == c for p in PRODUCTEN)]
        if not cats:
            continue
        li = ''
        for c in cats:
            sub = ''.join(f'<a class="msub" href="{gpad(c)}{s_}/">{e(n_)}</a>' for s_, n_ in actieve_subs(c))
            li += f'<li><a class="mcat" href="{gpad(c)}">{e(CATS[c]["naam"])}</a>{sub}</li>'
        delen.append(f'<details class="mgroep"><summary>{g["ico"]} {e(g["naam"])}</summary><a class="malles" href="/{g["slug"]}/">Alles in {e(g["naam"])} →</a><ul>{li}</ul></details>')
    return ('<details class="menu" id="menu"><summary class="menuknop">☰ Categorieën</summary><div class="menupaneel" role="navigation" aria-label="Categorieën">'
            + ''.join(delen) + '</div></details>')


def kruimel(*stukken):
    items = [('/', 'Home')] + list(stukken)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMEIN + u} for i, (u, n) in enumerate(items)]}
    html_ = ' <span aria-hidden="true">›</span> '.join(
        (f'<a href="{u}">{e(n)}</a>' if i < len(items) - 1 else f'<span aria-current="page">{e(n)}</span>') for i, (u, n) in enumerate(items))
    return f'<nav class="kruimel" aria-label="Kruimelpad">{html_}</nav><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
e = html.escape


def euro(v):
    s = f"{v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return s[:-3] + ',-' if s.endswith(',00') else s


def totaal(o):
    return round(o['prijs'] + (o['verzend'] or 0), 2)


def kop(titel, beschrijving, pad, extra_head=''):
    MENU = maak_menu()
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschrijving)}">
<link rel="canonical" href="{DOMEIN}{pad}">
<meta name="theme-color" content="#0e7c4a">
<link rel="icon" href="/favicon.ico" sizes="32x32"><link rel="icon" href="/icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="preload" href="/fonts/atkinson-hyperlegible-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/stijl.css?v={data['versie']}">
<meta property="og:title" content="{e(titel)}"><meta property="og:description" content="{e(beschrijving)}">
<meta property="og:type" content="website"><meta property="og:url" content="{DOMEIN}{pad}"><meta property="og:image" content="{DOMEIN}/icons/icon-512.png">
{extra_head}
</head>
<body>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="{SITE}, naar de startpagina"><img src="/icons/icon.svg" alt="" width="32" height="32"><span>{SITE}</span></a>
    <nav class="nav" aria-label="Menu">
      {MENU}
      <a class="lnk" href="/zo-vergelijken-wij/">Zo vergelijken wij</a>
      <button class="installeer" id="installeer" type="button" hidden>📲 Installeer app</button>
    </nav>
  </div>
</header>
<main>
'''


VOET = f'''</main>
<footer class="foot">
  <div class="wrap">
    <p class="free">{SITE} vergelijkt elektronica bij Nederlandse webwinkels, inclusief verzendkosten. Gratis en onafhankelijk.</p>
    <nav aria-label="Over"><a href="/">Alle producten</a><a href="/zo-vergelijken-wij/">Zo vergelijken wij</a><a href="/winkels/">Winkels en verzendkosten</a><a href="/over/">Over deze site</a><a href="/privacy/">Privacy</a><a href="/contact/">Contact</a><a href="#" id="installeer2">📲 Installeer als app</a></nav>
    <p class="small">Prijzen bijgewerkt op {e(BIJGEWERKT)}. Prijzen kunnen bij de winkel inmiddels anders zijn; de prijs in de webwinkel is altijd leidend.</p>
    <p class="small">© {JAAR} {SITE} – Erik Beltman. Alle rechten voorbehouden. <a href="/gebruiksvoorwaarden/">Gebruiksvoorwaarden</a></p>
  </div>
</footer>
<script>
let uitstel=null;const k1=document.getElementById('installeer'),k2=document.getElementById('installeer2');
const ios=/iphone|ipad|ipod/i.test(navigator.userAgent),los=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
addEventListener('beforeinstallprompt',ev=>{{ev.preventDefault();uitstel=ev;if(!los)k1.hidden=false;}});
if(ios&&!los)k1.hidden=false;
function installeer(ev){{ev&&ev.preventDefault();if(uitstel){{uitstel.prompt();uitstel=null;k1.hidden=true;}}else if(ios){{alert('Tik onderin Safari op het deel-icoon en kies "Zet op beginscherm".');}}else{{alert('Open het menu van je browser en kies "App installeren" of "Toevoegen aan startscherm".');}}}}
k1.addEventListener('click',installeer);k2&&k2.addEventListener('click',installeer);
if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('/sw.js'));
</script>
</body>
</html>
'''


def prijstabel(p):
    rijen = []
    for i, o in enumerate(sorted(p['aanbiedingen'], key=totaal)):
        w = WINKELS[o['winkel']]
        v = o['verzend']
        vtxt = '<span class="gratis">gratis</span>' if v == 0 else '€ ' + euro(v)
        sub = ['verkoop door ' + e(o['verkoper'])] if o.get('verkoper') else []
        subtxt = f'<small>{" · ".join(sub)}</small>' if sub else ''
        rijen.append(
            f'<tr class="{"top1" if i == 0 else ""}" data-p="{o["prijs"]}" data-v="{v}">'
            f'<td class="w">{e(w["naam"])}{subtxt}</td>'
            f'<td class="r prijs">€ {euro(o["prijs"])}</td>'
            f'<td class="r verb">{vtxt}</td>'
            f'<td class="r tot">€ {euro(totaal(o))}</td>'
            f'<td class="r"><a class="btn" href="{e(winkellink(o, p))}" target="_blank" rel="{"sponsored noopener" if o["winkel"] == "bol" else "noopener nofollow"}">Bekijk</a></td></tr>')
    return ('<table class="prijzen"><thead><tr><th>Winkel</th><th class="r">Prijs</th>'
            '<th class="r verb">Verzending</th><th class="r">Totaal</th><th></th></tr></thead><tbody>'
            + ''.join(rijen) + '</tbody></table>')


def kaart(p):
    offers = sorted(p['aanbiedingen'], key=totaal)
    best = offers[0]
    bespaar = totaal(offers[-1]) - totaal(best)
    besp = f'<span class="besparing">tot € {euro(bespaar)} verschil</span>' if bespaar >= 1 else '<span class="besparing" hidden></span>'
    cat = CATS[p['cat']]['naam']
    zoek = (p['naam'] + ' ' + cat + ' ' + p.get('zoek', '')).lower()
    return (f'<article class="kaart" data-cat="{p["cat"]}" data-groep="{CATS[p["cat"]]["groep"]}" data-z="{e(zoek)}" data-best="{totaal(best)}" data-bespaar="{bespaar:.2f}" data-sub=" {' '.join(p['subs'])} " data-merk="{e(p['merk'])}" data-spec="|{e('|'.join(k + '=' + v for k, v in p['spec'].items()))}|">'
            f'<span class="cat">{e(cat)}</span>'
            f'<h3><a href="/product/{p["slug"]}/">{e(p["naam"])}</a></h3>'
            + (f'<div class="specs">{" · ".join(e(v) for v in p["kaartspec"][:4])}</div>' if p['kaartspec'] else '') +
            f'<div class="prijsrij"><span class="kaartje">€ {euro(totaal(best))}</span>{besp}</div>'
            f'<div class="bij">Goedkoopst bij <b>{e(WINKELS[best["winkel"]]["naam"])}</b> · {len(offers)} winkel{"s" if len(offers) != 1 else ""} vergeleken</div>'
            f'<details class="winkels"><summary>Alle prijzen</summary>{prijstabel(p)}</details>'
            '</article>')


SCRIPT_LIJST = '''<script>
(()=>{const lijst=document.getElementById('lijst');if(!lijst)return;const kaarten=[...lijst.querySelectorAll('.kaart')];
const q=document.getElementById('q'),inc=document.getElementById('incl'),sort=document.getElementById('sort'),aantal=document.getElementById('aantal');
let groep=lijst.dataset.groep||'',cat=lijst.dataset.cat||'',sub=lijst.dataset.sub||'',merk='';const specf={};
const eur=v=>{let s=v.toFixed(2).replace('.',',').replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.');return s.endsWith(',00')?s.slice(0,-3)+',-':s};
function herreken(){const metV=!inc||inc.checked;
 kaarten.forEach(k=>{const rijen=[...k.querySelectorAll('tbody tr')];rijen.forEach(r=>{r._t=+r.dataset.p+(metV?+r.dataset.v:0);r.querySelector('.tot').textContent='€ '+eur(r._t)});
  rijen.sort((a,b)=>a._t-b._t);const tb=k.querySelector('tbody');rijen.forEach((r,i)=>{r.classList.toggle('top1',i==0);tb.appendChild(r)});
  const b=rijen[0];k.dataset.best=b._t;k.dataset.bespaar=(rijen[rijen.length-1]._t-b._t).toFixed(2);
  const kj=k.querySelector('.kaartje');if(kj)kj.textContent='€ '+eur(b._t);const bb=k.querySelector('.bij b');if(bb)bb.textContent=b.querySelector('.w').firstChild.textContent;
  const bs=k.querySelector('.besparing');if(bs){bs.hidden=+k.dataset.bespaar<1;bs.textContent='tot € '+eur(+k.dataset.bespaar)+' verschil';}});
 const pk=document.querySelector('.pkop .kaartje');if(pk&&kaarten[0])pk.textContent='€ '+eur(+kaarten[0].dataset.best);
 filter();}
function filter(){const t=(q&&q.value||'').toLowerCase().trim().split(/\\s+/).filter(Boolean);
 const zicht=kaarten.filter(k=>{const ok=(!groep||k.dataset.groep==groep)&&(!cat||k.dataset.cat==cat)&&(!sub||(k.dataset.sub||'').includes(' '+sub+' '))&&(!merk||k.dataset.merk==merk)&&Object.entries(specf).every(([a,b])=>!b||(k.dataset.spec||'').includes('|'+a+'='+b+'|'))&&t.every(w=>k.dataset.z.includes(w));k.hidden=!ok;return ok});
 const s=sort?sort.value:'pop';const volg=[...kaarten];
 if(s=='laag')volg.sort((a,b)=>a.dataset.best-b.dataset.best);else if(s=='hoog')volg.sort((a,b)=>b.dataset.best-a.dataset.best);else if(s=='verschil')volg.sort((a,b)=>b.dataset.bespaar-a.dataset.bespaar);
 if(sort)volg.forEach(k=>lijst.appendChild(k));if(aantal)aantal.textContent=zicht.length+' product'+(zicht.length==1?'':'en');
 const g=document.getElementById('geen');if(g&&sort)g.hidden=zicht.length>0;}
document.querySelectorAll('[data-kies]').forEach(b=>b.addEventListener('click',()=>{groep=b.dataset.kies;document.querySelectorAll('[data-kies]').forEach(x=>x.classList.toggle('aan',x==b));filter();}));
const fa=document.getElementById('factief');const telf=()=>{const n=(merk?1:0)+Object.values(specf).filter(Boolean).length;if(fa)fa.textContent=n?'('+n+')':'';document.querySelectorAll('select[data-spec-groep],select[data-merk-sel]').forEach(x=>x.classList.toggle('aan',!!x.value));};
document.querySelectorAll('select[data-merk-sel]').forEach(x=>x.addEventListener('change',()=>{merk=x.value;telf();filter();}));
document.querySelectorAll('select[data-spec-groep]').forEach(x=>x.addEventListener('change',()=>{specf[x.dataset.specGroep]=x.value;telf();filter();}));
const wis=document.getElementById('wis');wis&&wis.addEventListener('click',()=>{merk='';for(const k in specf)delete specf[k];document.querySelectorAll('select[data-spec-groep],select[data-merk-sel]').forEach(x=>x.value='');telf();filter();});
if(!matchMedia('(max-width:700px)').matches)document.querySelectorAll('details.filters').forEach(d=>d.open=true);
q&&q.addEventListener('input',filter);sort&&sort.addEventListener('change',filter);
inc&&inc.addEventListener('change',()=>{try{localStorage.setItem('incl',inc.checked?'1':'0')}catch(e){};herreken()});
try{if(inc&&localStorage.getItem('incl')==='0')inc.checked=false}catch(e){}
const u=new URLSearchParams(location.search);if(u.get('q')&&q)q.value=u.get('q');
herreken();})();
</script>'''


def spectabel(p):
    rijen = [('Merk', p['merk'])] + [(k, v) for k, v in p['spec'].items() if k != 'Prijsklasse']
    bekend = {k for k, _ in rijen} | set(LABEL.values())
    for k, v in p.get('kenmerken', {}).items():
        if LABEL.get(k, k) not in bekend and k not in bekend:
            rijen.append((k, v))
    if len(rijen) < 2:
        return ''
    return ('<div class="blok"><h2>Specificaties</h2><table class="spectab"><tbody>' +
            ''.join(f'<tr><th>{e(k)}</th><td>{e(v)}</td></tr>' for k, v in rijen) +
            '</tbody></table><p class="uitleg">Specificaties volgens de fabrikant en de winkels. Controleer ze altijd bij de winkel.</p></div>')


def merkknoppen(producten):
    merken = sorted({p['merk'] for p in producten}, key=str.lower)
    if len(merken) < 2:
        return ''
    return ('<label class="fsel"><span>Merk</span><select data-merk-sel><option value="">Alle merken</option>'
            + ''.join(f'<option value="{e(m)}">{e(m)}</option>' for m in merken) + '</select></label>')


def specknoppen(producten, alleen_prijs=False):
    """Filters als rustige keuzelijsten. Alleen kenmerken die bij de meeste producten bekend zijn en 2-12 waarden hebben."""
    tel = {}
    for p in producten:
        for k_ in p['spec']:
            tel[k_] = tel.get(k_, 0) + 1
    sleutels = sorted(tel, key=lambda k_: (k_ != 'Prijsklasse', -tel[k_]))
    uit = []
    for k_ in sleutels:
        if alleen_prijs and k_ != 'Prijsklasse':
            continue
        if k_ != 'Prijsklasse' and tel[k_] < max(3, len(producten) * 0.4):
            continue
        waarden = sorted({p['spec'][k_] for p in producten if k_ in p['spec']}, key=_sortwaarde)
        if not 2 <= len(waarden) <= 12:
            continue
        naam = 'Prijs' if k_ == 'Prijsklasse' else k_
        uit.append(f'<label class="fsel"><span>{e(naam)}</span><select data-spec-groep="{e(k_)}"><option value="">Alle</option>'
                   + ''.join(f'<option value="{e(v)}">{e(v)}</option>' for v in waarden) + '</select></label>')
    return uit


def lijstblok(producten, groep='', cat='', sub=''):
    sp = specknoppen(producten, alleen_prijs=not cat)
    m_ = merkknoppen(producten)
    velden = sp[:1] + ([m_] if m_ else []) + sp[1:]
    zicht, meer = velden[:6], velden[6:]
    f = ''.join(zicht) + (f'<details class="meer"><summary>Meer filters ({len(meer)})</summary><div class="fgrid">{"".join(meer)}</div></details>' if meer else '')
    fblok = (f'<details class="filters"><summary>Filteren <span id="factief"></span></summary><div class="fbody"><div class="fgrid">{f}</div>'
             '<button type="button" class="wis" id="wis">Wis filters</button></div></details>') if velden else ''
    return (f'''{fblok}<div class="balk"><span id="aantal"></span>
<label>Sorteer: <select id="sort"><option value="pop">Populair</option><option value="laag">Laagste prijs</option><option value="hoog">Hoogste prijs</option><option value="verschil">Grootste prijsverschil</option></select></label></div>
<div class="lijst" id="lijst" data-groep="{groep}" data-cat="{cat}" data-sub="{sub}">{''.join(kaart(p) for p in producten)}</div>
<p class="leeg" id="geen" hidden>Niets gevonden. Probeer een andere zoekterm.</p>''')


# Advertenties per categorie (Erik: geen naam van de adverteerder in de titel van een tegel)
from urllib.parse import quote as _q
def _awin(mid, ref, doel): return f'https://www.awin1.com/cread.php?awinmid={mid}&awinaffid=3152283&clickref={ref}&ued={_q(doel, safe="")}'
def _teufel(pad=''): return f'https://fr135.net/c/?si=15574&li=1673006&wi=449774&ws=bespaarvriend-elektronica&dl={_q(pad, safe="")}'
_REFURB = ('Liever refurbished?', 'Gebruikte toestellen, gecontroleerd en schoongemaakt, met garantie. Vaak flink goedkoper dan nieuw.')
PARTNERS = {
    'smartphones': [(*_REFURB, 'Bekijk refurbished telefoons', _awin(112024, 'bespaarvriend-elektronica', 'https://www.refurbished.nl/'),
                     [('iPhone 15', _awin(112024, 'bespaarvriend-elektronica', 'https://www.refurbished.nl/iphone-15')), ('iPhone 16', _awin(112024, 'bespaarvriend-elektronica', 'https://www.refurbished.nl/iphone-16')), ('Samsung', _awin(112024, 'bespaarvriend-elektronica', 'https://www.refurbished.nl/samsung'))])],
    'tablets': [(*_REFURB, 'Bekijk refurbished iPads', _awin(112024, 'bespaarvriend-elektronica', 'https://www.refurbished.nl/ipad'), [])],
    'laptops': [(*_REFURB, 'Bekijk refurbished laptops', _awin(112024, 'bespaarvriend-elektronica', 'https://www.refurbished.nl/laptops'),
                 [('MacBook', _awin(112024, 'bespaarvriend-elektronica', 'https://www.refurbished.nl/macbook'))])],
    'koptelefoons': [('Koptelefoons rechtstreeks van de Duitse maker', 'Een audiomerk uit Berlijn dat zelf verkoopt, zonder winkel ertussen.', 'Bekijk koptelefoons', _teufel('koptelefoons'), [])],
    'soundbars': [('Soundbars rechtstreeks van de Duitse maker', 'Een audiomerk uit Berlijn dat zelf verkoopt, zonder winkel ertussen.', 'Bekijk soundbars', _teufel('soundbars'), [])],
    'speakers': [('Speakers rechtstreeks van de Duitse maker', 'Een audiomerk uit Berlijn dat zelf verkoopt, zonder winkel ertussen.', 'Bekijk speakers', _teufel('speakers'), [])],
}


def partnerblok(c):
    out = ''
    for titel, tekst, knop, url, chips in PARTNERS.get(c, []):
        ch = ''.join(f'<a href="{e(u)}" rel="sponsored noopener" target="_blank">{e(t)}</a>' for t, u in chips)
        out += (f'<aside class="partner"><p class="ad">Advertentie</p><b>{e(titel)}</b><p>{e(tekst)}</p>'
                + (f'<div class="pchips">{ch}</div>' if ch else '')
                + f'<a class="btn" href="{e(url)}" rel="sponsored noopener" target="_blank">{e(knop)} →</a>'
                '<p class="bron">Koop je via deze link, dan krijgt Bespaarvriend een kleine vergoeding. Jij betaalt niets extra.</p></aside>')
    return out


BOL_SITE = os.environ.get('BOL_SITE', '1562371')  # bol affiliate site-ID van Bespaarvriend


def winkellink(o, p):
    """Partnerlink waar we een goedgekeurd programma hebben; anders de gewone productlink."""
    if o['winkel'] == 'bol' and BOL_SITE:
        from urllib.parse import quote
        return (f'https://partner.bol.com/click/click?p=2&t=url&s={BOL_SITE}&f=TXL'
                f'&url={quote(o["url"], safe="")}&name={quote(p["naam"][:60], safe="")}&subid=elektronica')
    return o['url']


def zoekblok():
    return '''<form class="zoek" role="search" onsubmit="return false"><input id="q" type="search" placeholder="Zoek een product, merk of type…" aria-label="Zoeken" autocomplete="off"></form>
<label class="schakel"><input type="checkbox" id="incl" checked> Inclusief verzendkosten</label>'''


def schrijf(pad, inhoud):
    f = os.path.join(OUT, pad.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(f), exist_ok=True)
    if B:
        inhoud = re.sub(r'((?:href|src|action)=["\'])/(?!/)', r'\1' + B + '/', inhoud).replace("register('/sw.js')", f"register('{B}/sw.js')")
        inhoud = inhoud.replace('<a class="brand"', '<a class="lnk bv" href="/" aria-label="Terug naar Bespaarvriend">←<span> Bespaarvriend</span></a><a class="brand"', 1)
    open(f, 'w').write(inhoud)


def bouw():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, 'site'), OUT)
    nwinkels = len({o['winkel'] for p in PRODUCTEN for o in p['aanbiedingen']})
    knoppen = '<button class="aan" data-kies="">Alles</button>' + ''.join(
        f'<button data-kies="{g["slug"]}">{g["ico"]} {e(g["naam"])}</button>' for g in GROEPEN if any(CATS[p['cat']]['groep'] == g['slug'] for p in PRODUCTEN))
    tegels = ''.join(f'<a class="groep" href="/{g["slug"]}/"><span class="ico">{g["ico"]}</span><b>{e(g["naam"])}</b><small>{e(g["tekst"])}</small></a>' for g in GROEPEN if any(CATS[p['cat']]['groep'] == g['slug'] for p in PRODUCTEN))
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": DOMEIN + "/",
          "potentialAction": {"@type": "SearchAction", "target": DOMEIN + "/?q={q}", "query-input": "required name=q"}}
    body = f'''<section class="wrap hero"><h1>Elektronica vergelijken</h1>
<p>Witgoed, tv's, laptops, smartphones en meer: de prijs bij {nwinkels} Nederlandse webwinkels, mét verzendkosten.</p>
{zoekblok()}</section>
<section class="wrap"><div class="groepen">{tegels}</div><div class="cats">{knoppen}</div>
{lijstblok(PRODUCTEN)}</section>'''
    schrijf('/', kop(f'{SITE} – elektronica vergelijken incl. verzendkosten',
                     'Vergelijk prijzen van witgoed, televisies, laptops, smartphones en meer bij Nederlandse webwinkels, inclusief verzendkosten.', '/',
                     f'<script type="application/ld+json">{json.dumps(ld)}</script>') + body + SCRIPT_LIJST + VOET)

    extra_urls = []
    for g in GROEPEN:
        prods = [p for p in PRODUCTEN if CATS[p['cat']]['groep'] == g['slug']]
        cats = [c for c, v in CATS.items() if v['groep'] == g['slug'] and any(p['cat'] == c for p in prods)]
        if not prods:
            continue
        ctegels = ''.join(f'<div class="groep"><a class="ckop" href="{gpad(c)}"><b>{e(CATS[c]["naam"])}</b><small>{sum(1 for p in prods if p["cat"] == c)} producten</small></a>'
                          + ''.join(f'<a class="csub" href="{gpad(c)}{s_}/">{e(n_)}</a>' for s_, n_ in actieve_subs(c)) + '</div>' for c in cats)
        body = f'''<section class="wrap">{kruimel((f"/{g['slug']}/", g["naam"]))}
<div class="hero"><h1>{g["ico"]} {e(g["naam"])}</h1><p>{e(g["tekst"])}. Prijzen inclusief verzendkosten bij Nederlandse webwinkels.</p>{zoekblok()}</div>
<div class="groepen ctegels">{ctegels}</div>{lijstblok(prods, g["slug"])}</section>'''
        schrijf(f'/{g["slug"]}/', kop(f'{g["naam"]} vergelijken incl. verzendkosten – {SITE}',
                                       f'{g["naam"]} vergelijken: {g["tekst"].lower()}. Zie waar het het goedkoopst is, inclusief verzendkosten.', f'/{g["slug"]}/') + body + SCRIPT_LIJST + VOET)
        for c in cats:
            cp = [p for p in prods if p['cat'] == c]
            naam = CATS[c]['naam']
            subs = actieve_subs(c)
            _maten = sorted({p['spec']['Schermformaat'] for p in cp if 'Schermformaat' in p['spec']}, key=_sortwaarde) if c in ('televisies', 'monitoren', 'tablets') else []
            matenchips = ('<div class="cats subs"><span class="lbl">Per formaat:</span>' + ''.join(f'<a href="{gpad(c)}{spec_slug(x)}/">{e(x)}</a>' for x in _maten) + '</div>') if len(_maten) > 1 else ''
            subchips = ('<div class="cats subs"><a class="aan" href="' + gpad(c) + '">Alle ' + e(naam.lower()) + '</a>' + ''.join(f'<a href="{gpad(c)}{s_}/">{e(n_)}</a>' for s_, n_ in subs) + '</div>') if subs else ''
            body = f'''<section class="wrap">{kruimel((f"/{g['slug']}/", g["naam"]), (gpad(c), naam))}
<div class="hero"><h1>{e(naam)} vergelijken</h1><p>{len(cp)} populaire {e(naam.lower())} bij Nederlandse webwinkels, inclusief verzendkosten.</p>{zoekblok()}</div>
{subchips}{matenchips}{partnerblok(c)}{lijstblok(cp, "", c)}</section>'''
            schrijf(f'/{g["slug"]}/{c}/', kop(f'{naam} vergelijken – goedkoopste prijs incl. verzending – {SITE}',
                                              f'Vergelijk de prijs van populaire {naam.lower()} bij Nederlandse webwinkels, inclusief verzendkosten.', f'/{g["slug"]}/{c}/') + body + SCRIPT_LIJST + VOET)

            maten = sorted({p['spec']['Schermformaat'] for p in cp if 'Schermformaat' in p['spec']}, key=_sortwaarde)
            if c in ('televisies', 'monitoren', 'tablets') and maten:
                for m_ in maten:
                    sl = spec_slug(m_)
                    mp = [p for p in cp if p['spec'].get('Schermformaat') == m_]
                    titel_ = f'{m_} {naam.lower()}'
                    mchips = '<div class="cats subs"><a href="' + gpad(c) + '">Alle maten</a>' + ''.join(f'<a class="{"aan" if x == m_ else ""}" href="{gpad(c)}{spec_slug(x)}/">{e(x)}</a>' for x in maten) + '</div>'
                    body = f'''<section class="wrap">{kruimel((f"/{g['slug']}/", g["naam"]), (gpad(c), naam), (gpad(c) + sl + "/", m_))}
<div class="hero"><h1>{e(titel_[0].upper() + titel_[1:])} vergelijken</h1><p>{len(mp)} {e(naam.lower())} van {e(m_)}, inclusief verzendkosten bij Nederlandse webwinkels.</p>{zoekblok()}</div>
{mchips}{partnerblok(c)}{lijstblok(mp, "", c)}</section>'''
                    schrijf(gpad(c) + sl + '/', kop(f'{titel_[0].upper() + titel_[1:]} vergelijken incl. verzending – {SITE}',
                                                  f'Vergelijk {naam.lower()} van {m_} bij Nederlandse webwinkels, inclusief verzendkosten.', gpad(c) + sl + '/') + body + SCRIPT_LIJST + VOET)
                    extra_urls.append(gpad(c) + sl + '/')
            for s_, n_ in subs:
                sp = [p for p in cp if s_ in p['subs']]
                chips2 = '<div class="cats subs"><a href="' + gpad(c) + '">Alle ' + e(naam.lower()) + '</a>' + ''.join(f'<a class="{"aan" if x == s_ else ""}" href="{gpad(c)}{x}/">{e(y)}</a>' for x, y in subs) + '</div>'
                body = f'''<section class="wrap">{kruimel((f"/{g['slug']}/", g["naam"]), (gpad(c), naam), (gpad(c) + s_ + "/", n_))}
<div class="hero"><h1>{e(n_)} vergelijken</h1><p>{len(sp)} {e(naam.lower())}: {e(n_.lower())}. Prijzen inclusief verzendkosten bij Nederlandse webwinkels.</p>{zoekblok()}</div>
{chips2}{partnerblok(c)}{lijstblok(sp, "", c, s_)}</section>'''
                schrijf(gpad(c) + s_ + '/', kop(f'{n_} – {naam} vergelijken incl. verzending – {SITE}',
                                               f'{n_}: vergelijk {naam.lower()} bij Nederlandse webwinkels, inclusief verzendkosten.', gpad(c) + s_ + '/') + body + SCRIPT_LIJST + VOET)

    for p in PRODUCTEN:
        offers = sorted(p['aanbiedingen'], key=totaal)
        best = offers[0]
        cat = CATS[p['cat']]
        g = next(x for x in GROEPEN if x['slug'] == cat['groep'])
        ld = {"@context": "https://schema.org", "@type": "Product", "name": p['naam'],
              "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": min(o['prijs'] for o in offers),
                         "highPrice": max(o['prijs'] for o in offers), "offerCount": len(offers)}}
        if p.get('merk'):
            ld['brand'] = {"@type": "Brand", "name": p['merk']}
        verschil = totaal(offers[-1]) - totaal(best)
        sublinks = ' · '.join(f'<a href="{gpad(p["cat"])}{s_}/">{e(n_)}</a>' for s_, n_ in actieve_subs(p['cat']) if s_ in p['subs'])
        body = f'''<section class="wrap">{kruimel((f"/{g['slug']}/", g["naam"]), (gpad(p["cat"]), cat["naam"]), (f"/product/{p['slug']}/", p["naam"]))}
<div class="pkop"><h1>{e(p["naam"])}</h1>
<p class="bij">Goedkoopst: <span class="kaartje">€ {euro(totaal(best))}</span> bij <b>{e(WINKELS[best["winkel"]]["naam"])}</b></p></div>
<label class="schakel"><input type="checkbox" id="incl" checked> Inclusief verzendkosten</label>
<div class="blok" id="lijst"><div class="kaart" style="box-shadow:none;border:0;padding:0" data-cat="{p["cat"]}" data-groep="{cat["groep"]}" data-z="" data-best="{totaal(best)}" data-bespaar="0">{prijstabel(p)}</div></div>
<p class="uitleg">We vergeleken {len(offers)} webwinkel{"s" if len(offers) != 1 else ""}. {"Het verschil tussen de goedkoopste en duurste winkel is € " + euro(verschil) + "." if verschil >= 1 else ""} Bij winkels met andere verkopers (zoals bol en Amazon) staat erbij wie het product verkoopt. Controleer altijd de actuele prijs bij de winkel.</p>
{spectabel(p)}{('<p class="uitleg">Ook in: ' + sublinks + '</p>') if sublinks else ''}
<p class="uitleg">Prijzen bijgewerkt op {e(BIJGEWERKT)}. <a href="/zo-vergelijken-wij/">Zo vergelijken wij</a> · <a href="/winkels/">Verzendkosten per winkel</a></p></section>'''
        schrijf(f'/product/{p["slug"]}/', kop(f'{p["naam"]} – prijzen vergelijken – {SITE}',
                                              f'{p["naam"]} vanaf € {euro(totaal(best))} inclusief verzendkosten. Vergelijk {len(offers)} Nederlandse webwinkels.',
                                              f'/product/{p["slug"]}/', f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>') + body + SCRIPT_LIJST + VOET)

    gebruikt = {o['winkel'] for p in PRODUCTEN for o in p['aanbiedingen']}
    rij = ''.join(f'<tr><td class="w">{e(w["naam"])}</td><td>{e(w["verzendtekst"])}</td></tr>' for k, w in WINKELS.items() if k in gebruikt)
    body = f'''<section class="wrap tekst"><a class="terug" href="/">← Alle producten</a><h1>Winkels en verzendkosten</h1>
<p>Dit zijn de webwinkels die we vergelijken, met de verzendkosten die we meetellen voor een bestelling van één product, thuisbezorgd in Nederland.</p>
<div class="blok"><table class="prijzen"><thead><tr><th>Winkel</th><th>Verzendkosten</th></tr></thead><tbody>{rij}</tbody></table></div>
<p class="uitleg">Extra's zoals een bezorgmoment kiezen, avondlevering, aansluiten of het meenemen van je oude apparaat tellen we niet mee. Bron: de klantenservice- en productpagina's van de winkels zelf, bekeken op {e(BIJGEWERKT)}.</p></section>'''
    schrijf('/winkels/', kop(f'Verzendkosten per webwinkel – {SITE}', 'Overzicht van de verzendkosten van Nederlandse elektronicawinkels.', '/winkels/') + body + VOET)

    contact = f'<p>Mail ons: <a href="mailto:{e(MAIL)}">{e(MAIL)}</a></p>' if MAIL else '<p>Het contactadres volgt binnenkort.</p>'
    for pad, titel, tekst in data['paginas']:
        tekst = tekst.replace('{CONTACT}', contact).replace('{SITE}', SITE)
        schrijf(pad, kop(f'{titel} – {SITE}', titel, pad) + f'<section class="wrap tekst"><a class="terug" href="/">← Alle producten</a><h1>{e(titel)}</h1>{tekst}</section>' + VOET)

    urls = ['/', '/winkels/'] + [p for p, _, _ in data['paginas']] + [f'/{g["slug"]}/' for g in GROEPEN] + \
           sorted({gpad(p["cat"]) for p in PRODUCTEN}) + sorted({gpad(p["cat"]) + x + '/' for p in PRODUCTEN for x in p['subs']}) + [f'/product/{p["slug"]}/' for p in PRODUCTEN] + extra_urls
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
                                                     ''.join(f'<url><loc>{DOMEIN}{u}</loc></url>' for u in urls) + '</urlset>\n')
    if B:  # onder Bespaarvriend: robots en redirects regelt de hoofdsite
        for x in ('_redirects', 'tools'):
            p_ = os.path.join(OUT, x); shutil.rmtree(p_) if os.path.isdir(p_) else os.path.exists(p_) and os.remove(p_)
    else:
      open(os.path.join(OUT, 'robots.txt'), 'w').write(
        'User-agent: *\nAllow: /\nDisallow: /tools/\n\n' + ''.join(f'User-agent: {b}\nDisallow: /\n\n' for b in ['GPTBot', 'CCBot', 'Google-Extended', 'anthropic-ai', 'ClaudeBot', 'PerplexityBot', 'Bytespider', 'meta-externalagent']) +
        f'Sitemap: {DOMEIN}/sitemap.xml\n')
    json.dump({"name": SITE, "short_name": SITE, "description": "Vergelijk elektronica bij Nederlandse webwinkels, inclusief verzendkosten.",
               "lang": "nl", "start_url": B + "/?bron=app", "scope": B + "/", "display": "standalone", "background_color": "#f4f7f1", "theme_color": "#0e7c4a",
               "icons": [{"src": B + "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": B + "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                         {"src": B + "/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
              open(os.path.join(OUT, 'manifest.webmanifest'), 'w'))
    open(os.path.join(OUT, 'sw.js'), 'w').write(f'''const V='ev-{data["versie"]}';
self.addEventListener('install',e=>{{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>c.addAll(['{B}/','{B}/stijl.css?v={data["versie"]}','{B}/icons/icon.svg'])))}});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{{if(e.request.method!=='GET'||new URL(e.request.url).origin!==location.origin)return;
e.respondWith(fetch(e.request).then(r=>{{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r}}).catch(()=>caches.match(e.request)))}});
''')
    print('Gebouwd:', len(PRODUCTEN), 'producten,', len(urls), 'pagina\'s naar', OUT)


bouw()
