#!/usr/bin/env python3
"""Bouwt Bespaarvriend.nl: een kleine, snelle statische site over slim besparen op vaste lasten.
Uitvoer in public/. Draait op Netlify (zie netlify.toml) en lokaal met: python3 build.py"""
import html, json, os, shutil, datetime

BASE = "https://bespaarvriend.nl"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
VANDAAG = datetime.date.today().isoformat()
BIJGEWERKT = "18 november 2026"
esc = html.escape

CSS = """
:root{--g:#0b6a3f;--g2:#17a061;--ink:#1d2a22;--mut:#5b6b62;--line:#dde5df;--bg:#f4f7f3;--soft:#e8f3ec;--geel:#fff6d6}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:17px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--g)}img{max-width:100%}
.wrap{max-width:760px;margin:0 auto;padding:0 16px}
header.top{background:#fff;border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:60px}
.logo{display:flex;align-items:center;gap:8px;font-weight:800;font-size:1.2rem;color:var(--ink);text-decoration:none}
.logo span.ic{display:inline-grid;place-items:center;width:34px;height:34px;background:var(--g);color:#fff;font-size:1.1rem}
nav.top{display:flex;gap:12px;font-weight:700;font-size:.92rem}@media(max-width:400px){.logo{font-size:1.05rem}.logo span.ic{width:30px;height:30px}nav.top{gap:10px;font-size:.88rem}}nav.top a{text-decoration:none}
.crumbs{font-size:.85rem;color:var(--mut);margin:14px 0 0}.crumbs a{color:var(--mut)}
h1{font-size:1.9rem;line-height:1.15;margin:14px 0 8px}h2{font-size:1.35rem;margin:28px 0 10px}h3{font-size:1.08rem;margin:18px 0 6px}
.lead{font-size:1.1rem;color:var(--mut);margin:0 0 16px}
.kaart{background:#fff;border:1px solid var(--line);padding:16px 18px;margin:14px 0;box-shadow:0 3px 6px rgba(20,40,28,.08)}
.kerncijfers{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0;margin:14px 0;border:1px solid var(--line);background:#fff}
.kerncijfers div{padding:14px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.kerncijfers div:nth-child(2n){border-right:0}.kerncijfers div:nth-last-child(-n+2){border-bottom:0}
.kerncijfers b{display:block;font-size:1.45rem;color:var(--g)}.kerncijfers small{color:var(--mut);font-size:.88rem}
.tegels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0;border:1px solid var(--line);background:#fff;margin:16px 0}
.tegels a{display:block;padding:16px 14px;text-decoration:none;color:var(--ink);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.tegels a:nth-child(2n){border-right:0}.tegels a:nth-last-child(-n+2){border-bottom:0}
.tegels .ic{font-size:1.6rem;display:block}.tegels b{display:block;font-size:1.05rem}.tegels small{color:var(--mut)}
.let{background:var(--geel);border:1px solid #f0e2a8;padding:12px 14px;margin:14px 0}
.btn{display:inline-block;background:linear-gradient(#17a061,#0b6a3f);color:#fff;font-weight:800;padding:12px 18px;border:0;border-radius:10px;text-decoration:none;box-shadow:inset 0 1px 0 rgba(255,255,255,.25),0 3px 0 #08502f;cursor:pointer;font-size:1rem}
.btn:active{transform:translateY(2px);box-shadow:0 1px 0 #08502f}
ol.stappen{counter-reset:s;list-style:none;padding:0;margin:12px 0}
ol.stappen li{counter-increment:s;position:relative;padding:10px 0 10px 44px;border-bottom:1px solid var(--line)}
ol.stappen li:before{content:counter(s);position:absolute;left:0;top:9px;width:30px;height:30px;border-radius:50%;background:var(--g);color:#fff;font-weight:800;display:grid;place-items:center}
table{border-collapse:collapse;width:100%;background:#fff;margin:10px 0;font-size:.95rem}th,td{border:1px solid var(--line);padding:8px 10px;text-align:left}th{background:var(--soft)}
td.r,th.r{text-align:right;white-space:nowrap}
.faq details{background:#fff;border:1px solid var(--line);margin:8px 0}.faq summary{cursor:pointer;padding:12px 14px;font-weight:700}.faq details p{margin:0;padding:0 14px 12px}
.reken label{display:block;font-weight:700;margin:10px 0 4px}.reken input,.reken select{width:100%;padding:11px;font:inherit;border:1px solid var(--line);background:#fbfdfb}
.reken .uit{margin-top:12px;padding:12px;background:var(--soft);font-weight:600;min-height:1em}
.bron{font-size:.85rem;color:var(--mut)}
.links li{margin:4px 0}
footer{margin-top:40px;background:#fff;border-top:1px solid var(--line);padding:20px 0;font-size:.92rem;color:var(--mut)}
footer nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 16px;margin:10px 0}footer nav a{font-weight:700;text-decoration:none}
form.contact label{display:block;font-weight:700;margin:10px 0 4px}form.contact input,form.contact select,form.contact textarea{width:100%;padding:11px;font:inherit;border:1px solid var(--line)}
.hp{position:absolute;left:-9999px}
@media(min-width:700px){h1{font-size:2.3rem}.kerncijfers,.tegels{grid-template-columns:repeat(4,minmax(0,1fr))}.kerncijfers div,.tegels a{border-bottom:0;border-right:1px solid var(--line)!important}.kerncijfers div:last-child,.tegels a:last-child{border-right:0!important}}
"""

NAV = '<nav class="top" aria-label="Hoofdmenu"><a href="/zorgverzekering-2027/">Zorg</a><a href="/zorgtoeslag-2027/">Toeslag</a><a href="/contact/">Contact</a></nav>'
FOOT = f"""<footer><div class="wrap">
<p><b>Bespaarvriend</b> helpt je eenvoudig besparen op je vaste lasten. Onafhankelijk uitgelegd, zonder verkooppraatjes. Wij geven geen persoonlijk financieel advies.</p>
<nav aria-label="Over"><a href="/zorgverzekering-2027/">Zorgverzekering 2027</a><a href="/eigen-risico-2027/">Eigen risico 2027</a><a href="/zorgtoeslag-2027/">Zorgtoeslag 2027</a><a href="https://boodschappenvergelijk.nl/">Boodschappen vergelijken</a><a href="/over/">Over Bespaarvriend</a><a href="/privacy/">Privacy</a><a href="/contact/">Contact</a></nav>
<p>© {datetime.date.today().year} Bespaarvriend – Erik Beltman. Bijgewerkt op {BIJGEWERKT}.</p></div></footer>"""


def faq_html(faq):
    return '<section class="faq"><h2>Veelgestelde vragen</h2>' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</section>"


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def crumbs(naam, path):
    h = f'<p class="crumbs"><a href="/">Home</a> › {esc(naam)}</p>'
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": naam, "item": BASE + path}]}
    return h, ld


PAGES = []


def page(path, title, desc, body, ld=(), noindex=False, prio="0.8"):
    lds = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": BASE + path, "description": desc, "inLanguage": "nl-NL",
            "dateModified": VANDAAG, "publisher": {"@type": "Organization", "name": "Bespaarvriend", "url": BASE}}] + list(ld)
    doc = f"""<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{BASE}{path}">
{'<meta name="robots" content="noindex">' if noindex else ''}<meta name="theme-color" content="#0b6a3f">
{'<meta name="e0d5a73bd035a1c" content="277030417ea9ada19f69ae08c41fb74b">' if path == "/" else ''}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:locale" content="nl_NL"><meta property="og:site_name" content="Bespaarvriend">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%230b6a3f'/%3E%3Ctext x='50' y='70' font-size='62' text-anchor='middle' fill='white' font-family='Arial' font-weight='bold'%3E€%3C/text%3E%3C/svg%3E">
<style>{CSS}</style>
{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in lds)}
</head><body><header class="top"><div class="wrap"><a class="logo" href="/"><span class="ic">€</span>Bespaarvriend</a>{NAV}</div></header>
<main class="wrap">{body}</main>{FOOT}</body></html>"""
    doc = doc.replace("€ ", "€\u00a0").replace("+ €", "+\u00a0€")
    if path.endswith("/"):
        d = os.path.join(OUT, path.strip("/")); os.makedirs(d, exist_ok=True); fn = os.path.join(d, "index.html")
    else:
        fn = os.path.join(OUT, path.lstrip("/"))
    with open(fn, "w") as f:
        f.write(doc)
    if not noindex:
        PAGES.append((path, prio))


BRONNEN_ZORG = ('<p class="bron">Bronnen: <a href="https://www.overstappen.nl/nieuws/zorgpremies-2027-bekend-alle-polissen-duurder-premiekloof-stijgt-naar-649-euro-per-jaar/" rel="noopener">Overstappen.nl (premies 2027)</a>, '
                '<a href="https://www.consumentenbond.nl/zorgverzekering/zorgverzekeringen-2027-zorgpremies-stijgen-fors" rel="noopener">Consumentenbond</a>, '
                '<a href="https://www.rabobank.nl/particulieren/verzekering/zorgverzekering/zorgverzekering-2027" rel="noopener">Rabobank (eigen risico en data)</a>. '
                f'Bijgewerkt op {BIJGEWERKT}.</p>')

VERGELIJKERS = ('<ul class="links"><li><a href="https://www.zorgwijzer.nl/" rel="noopener">Zorgwijzer</a> – alle polissen en premies op een rij</li>'
                '<li><a href="https://www.independer.nl/zorgverzekering/" rel="noopener">Independer</a> – vergelijken met je eigen wensen</li>'
                '<li><a href="https://www.consumentenbond.nl/zorgverzekering" rel="noopener">Consumentenbond</a> – onafhankelijke vergelijker (deels voor leden)</li></ul>'
                '<p class="bron">Wij krijgen niets voor deze links. Komt dat ooit wel, dan staat het er duidelijk bij.</p>')


def bouw():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    # ---------- Home ----------
    faq_h = [("Wat is Bespaarvriend?", "Een gratis site die in gewone taal uitlegt hoe je bespaart op je vaste lasten, zoals je zorgverzekering, zorgtoeslag en boodschappen. Wij verkopen zelf niets."),
             ("Geven jullie persoonlijk advies?", "Nee. We leggen uit hoe het zit en verwijzen naar onafhankelijke vergelijkers en officiële bronnen. De keuze maak je zelf."),
             ("Tot wanneer kan ik overstappen van zorgverzekering?", "Zeg je huidige zorgverzekering uiterlijk 31 december 2026 op. Je hebt daarna tot en met 31 januari 2027 om een nieuwe af te sluiten; die gaat in per 1 januari 2027.")]
    body = ('<h1>Slim besparen op je vaste lasten</h1><p class="lead">Eerlijk uitgelegd, zonder verkooppraatjes. Begin met de zorgverzekering: daar valt nu het meest te halen.</p>'
            '<div class="let"><b>⏰ Overstappen kan nog tot 31 december.</b> Tussen de goedkoopste en duurste basisverzekering zit in 2027 € 649 per jaar, voor dezelfde basiszorg. <a href="/zorgverzekering-2027/">Zo stap je over →</a></div>'
            '<div class="tegels">'
            '<a href="/zorgverzekering-2027/"><span class="ic">🩺</span><b>Zorgverzekering</b><small>Premies 2027 en overstappen</small></a>'
            '<a href="/eigen-risico-2027/"><span class="ic">💶</span><b>Eigen risico</b><small>€ 400 in 2027, rekenhulp</small></a>'
            '<a href="/zorgtoeslag-2027/"><span class="ic">🧾</span><b>Zorgtoeslag</b><small>Heb jij recht? Check</small></a>'
            '<a href="https://boodschappenvergelijk.nl/"><span class="ic">🛒</span><b>Boodschappen</b><small>11 supermarkten vergelijken</small></a>'
            '</div>'
            '<h2>Waarom Bespaarvriend?</h2><div class="kaart"><p style="margin-top:0">Ik ben Erik, de maker van <a href="https://boodschappenvergelijk.nl/">Goedkope Boodschappen</a>, bekend van Hart van Nederland en RTV Oost. '
            'Met Bespaarvriend wil ik mensen op dezelfde manier helpen met hun andere vaste lasten: duidelijk, eerlijk en gratis.</p>'
            '<p style="margin-bottom:0">Elke pagina noemt zijn bronnen en de datum waarop we hem hebben bijgewerkt. Zo weet je precies waar je aan toe bent.</p></div>'
            + faq_html(faq_h))
    page("/", "Bespaarvriend – slim besparen op je vaste lasten", "Gratis en eerlijk uitgelegd: besparen op je zorgverzekering 2027, eigen risico, zorgtoeslag en boodschappen. Met bronnen, rekenhulpen en zonder verkooppraatjes.",
         body, [faq_ld(faq_h), {"@context": "https://schema.org", "@type": "WebSite", "name": "Bespaarvriend", "url": BASE + "/", "inLanguage": "nl-NL"}], prio="1.0")

    # ---------- Zorgverzekering 2027 ----------
    ch, cld = crumbs("Zorgverzekering 2027", "/zorgverzekering-2027/")
    faq_z = [("Hoeveel kost de zorgverzekering in 2027?", "De gemiddelde basisverzekering kost in 2027 € 173,13 per maand, € 14,83 meer dan in 2026. De goedkoopste kost € 148,40 per maand, de duurste € 202,50."),
             ("Is de basisverzekering overal hetzelfde?", "Wat er in het basispakket zit, bepaalt de overheid. Dat is bij elke verzekeraar gelijk. Het verschil zit vooral in de vrije keuze van zorgverlener: bij een goedkope naturapolis krijg je bij een zorgverlener zonder contract soms minder vergoed."),
             ("Tot wanneer kan ik overstappen?", "Zeg je huidige verzekering uiterlijk 31 december 2026 op. Sluit daarna uiterlijk 31 januari 2027 een nieuwe af; die gaat met terugwerkende kracht in op 1 januari 2027. Vaak zegt je nieuwe verzekeraar de oude voor je op."),
             ("Moet ik mijn aanvullende verzekering ook opzeggen?", "Niet per se. Kijk of je de aanvullende verzekering het afgelopen jaar echt hebt gebruikt. Wie weinig naar tandarts of fysio gaat, betaalt vaak meer premie dan hij terugkrijgt."),
             ("Kan ik geweigerd worden?", "Voor de basisverzekering niet: iedere verzekeraar moet je accepteren. Voor een aanvullende verzekering mag een verzekeraar soms wel een gezondheidsverklaring vragen.")]
    body = (ch + '<h1>Zorgverzekering 2027: dit betaal je en zo stap je over</h1><p class="lead">Alle zorgverzekeringen worden duurder. Maar het verschil tussen goedkoop en duur is groter dan ooit.</p>'
            '<div class="kerncijfers"><div><b>€ 173,13</b><small>gemiddeld per maand</small></div><div><b>+ € 14,83</b><small>per maand t.o.v. 2026</small></div>'
            '<div><b>€ 148,40</b><small>goedkoopste (VinkVink)</small></div><div><b>€ 202,50</b><small>duurste (CZ Zorgvariatiepolis)</small></div></div>'
            '<div class="let"><b>Verschil goedkoopste en duurste: € 649 per jaar</b>, voor dezelfde basiszorg. Met z\'n tweeën kan dat oplopen tot bijna € 1.300 per jaar.</div>'
            '<h2>Zo stap je over in 4 stappen</h2><ol class="stappen">'
            '<li><b>Kijk wat je echt gebruikt.</b> Pak je jaaroverzicht erbij: welke zorg had je, en had je die aanvullende verzekering nodig?</li>'
            '<li><b>Vergelijk de premies.</b> Gebruik een onafhankelijke vergelijker (zie hieronder). Let op: naturapolis of restitutiepolis.</li>'
            '<li><b>Sluit de nieuwe verzekering af</b> vóór 1 januari, of uiterlijk 31 januari 2027 als je vóór 31 december hebt opgezegd.</li>'
            '<li><b>Je oude verzekering wordt opgezegd.</b> Meestal doet je nieuwe verzekeraar dat voor je. Controleer het in de bevestiging.</li></ol>'
            '<h2>Naturapolis of restitutiepolis?</h2><table><tr><th></th><th>Naturapolis</th><th>Restitutiepolis</th></tr>'
            '<tr><td>Premie</td><td>Lager</td><td>Hoger</td></tr><tr><td>Zorgverlener met contract</td><td>Volledig vergoed</td><td>Volledig vergoed</td></tr>'
            '<tr><td>Zorgverlener zonder contract</td><td>Vaak deels vergoed</td><td>Meestal volledig (tot marktconform tarief)</td></tr>'
            '<tr><td>Voor wie</td><td>Wie geen vaste voorkeur heeft voor een ziekenhuis of therapeut</td><td>Wie zeker een eigen zorgverlener wil houden</td></tr></table>'
            '<h2>Onafhankelijk vergelijken</h2>' + VERGELIJKERS
            + '<h2>Meer besparen op je zorgkosten</h2><ul class="links"><li><a href="/eigen-risico-2027/">Eigen risico 2027: loont een vrijwillig eigen risico?</a></li><li><a href="/zorgtoeslag-2027/">Zorgtoeslag 2027: heb jij recht?</a></li></ul>'
            + faq_html(faq_z) + BRONNEN_ZORG)
    page("/zorgverzekering-2027/", "Zorgverzekering 2027: premies, verschillen en overstappen", "De zorgpremie 2027 is gemiddeld € 173,13 per maand. Goedkoopste € 148,40, duurste € 202,50: € 649 per jaar verschil. Zo stap je vóór 31 december over.",
         body, [cld, faq_ld(faq_z)], prio="0.9")

    # ---------- Eigen risico 2027 ----------
    ch, cld = crumbs("Eigen risico 2027", "/eigen-risico-2027/")
    faq_e = [("Hoe hoog is het eigen risico in 2027?", "Het verplichte eigen risico is in 2027 € 400 per jaar. In 2026 was het nog € 385. Het is de eerste verhoging sinds 2016."),
             ("Waarvoor betaal ik geen eigen risico?", "De huisarts, zorg voor kinderen onder de 18 en een aantal andere vormen van zorg vallen buiten het eigen risico. Ziekenhuiszorg en medicijnen vallen er meestal wel onder."),
             ("Wat is een vrijwillig eigen risico?", "Je kunt je eigen risico vrijwillig verhogen, tot maximaal € 500 extra. In ruil daarvoor krijg je korting op je premie. Maak je zorgkosten, dan betaal je wel meer zelf."),
             ("Kan ik het eigen risico gespreid betalen?", "Bij veel zorgverzekeraars wel. Je betaalt het dan in termijnen in plaats van in één keer als je zorg nodig hebt.")]
    reken = ('<div class="kaart reken" id="rekenhulp"><h2 style="margin-top:0">Rekenhulp: loont een hoger eigen risico?</h2>'
             '<label for="korting">Premiekorting per maand bij € 500 extra eigen risico</label><input id="korting" type="number" inputmode="decimal" min="0" step="0.5" value="20">'
             '<label for="kosten">Hoeveel zorgkosten (onder het eigen risico) verwacht je per jaar?</label>'
             '<select id="kosten"><option value="0">Geen, ik ben bijna nooit ziek</option><option value="200">Een beetje (ongeveer € 200)</option><option value="600">Gemiddeld (ongeveer € 600)</option><option value="1500">Veel (meer dan € 900)</option></select>'
             '<div class="uit" id="uitkomst" role="status" aria-live="polite"></div>'
             '<p class="bron">De korting verschilt per verzekeraar; kijk in de vergelijker wat jouw verzekeraar geeft. Dit is een indicatie, geen advies.</p></div>'
             """<script>
(function(){var k=document.getElementById('korting'),c=document.getElementById('kosten'),u=document.getElementById('uitkomst');
function eur(x){return '€ '+Math.round(x).toLocaleString('nl-NL')}
function r(){var kort=Math.max(0,parseFloat(String(k.value).replace(',','.'))||0)*12,kost=+c.value;
var extra=Math.min(500,Math.max(0,kost-400)),saldo=kort-extra;
u.textContent=saldo>0?('Je houdt naar verwachting ongeveer '+eur(saldo)+' per jaar over. Zet wel € 500 apart voor als je toch zorg nodig hebt.'):('Een hoger eigen risico kost je naar verwachting ongeveer '+eur(-saldo)+' per jaar extra. Houd het bij € 400.')}
k.addEventListener('input',r);c.addEventListener('change',r);r()})();
</script>""")
    body = (ch + '<h1>Eigen risico 2027: € 400</h1><p class="lead">Het verplichte eigen risico stijgt in 2027 van € 385 naar € 400. Wat betekent dat, en loont een hoger vrijwillig eigen risico?</p>'
            '<div class="kerncijfers"><div><b>€ 400</b><small>verplicht eigen risico 2027</small></div><div><b>€ 385</b><small>in 2026</small></div><div><b>+ € 500</b><small>max. vrijwillig extra</small></div><div><b>€ 900</b><small>max. totaal</small></div></div>'
            + reken +
            '<h2>Wanneer betaal je eigen risico?</h2><p>Je betaalt eigen risico voor zorg uit de basisverzekering, zoals ziekenhuiszorg, medicijnen en bloedonderzoek. '
            'Een bezoek aan de huisarts valt erbuiten, en kinderen onder de 18 hebben geen eigen risico.</p>'
            '<h2>Tip: krap bij kas? Spreid je betaling</h2><p>Weet je dat je je eigen risico toch opmaakt, bijvoorbeeld door vaste medicijnen? Bij veel verzekeraars kun je het dan in termijnen betalen. Zo krijg je geen grote rekening in één keer.</p>'
            + faq_html(faq_e) + BRONNEN_ZORG)
    page("/eigen-risico-2027/", "Eigen risico 2027 is € 400: rekenhulp vrijwillig eigen risico", "Het eigen risico is in 2027 € 400 (was € 385). Reken uit of een hoger vrijwillig eigen risico voor jou loont, en wat er buiten het eigen risico valt.",
         body, [cld, faq_ld(faq_e)], prio="0.9")

    # ---------- Zorgtoeslag 2027 ----------
    ch, cld = crumbs("Zorgtoeslag 2027", "/zorgtoeslag-2027/")
    faq_t = [("Hoeveel zorgtoeslag krijg je maximaal in 2027?", "Naar verwachting maximaal € 140 per maand als alleenstaande en ongeveer € 268 per maand met een toeslagpartner. Hoeveel jij krijgt, hangt af van je inkomen."),
             ("Wat is de inkomensgrens voor zorgtoeslag in 2027?", "Naar verwachting ongeveer € 42.950 per jaar voor alleenstaanden en ongeveer € 54.150 samen met een toeslagpartner. De definitieve bedragen maakt Dienst Toeslagen bekend."),
             ("Wat is de vermogensgrens in 2027?", "€ 119.122 voor alleenstaanden en € 158.748 met een toeslagpartner, gemeten op 1 januari 2027. Dat is fors lager dan in 2026. Je eigen woning en pensioen tellen niet mee."),
             ("Ik zit net boven de vermogensgrens. Kan ik iets doen?", "Je vermogen wordt gemeten op 1 januari. Wie de zorgpremie voor heel 2027 vooruitbetaalt, heeft op die datum minder spaargeld. Laat je goed informeren voordat je iets doet."),
             ("Hoe vraag ik zorgtoeslag aan?", "Bij Dienst Toeslagen. Met een proefberekening zie je eerst of je recht hebt en hoeveel je ongeveer krijgt.")]
    check = ('<div class="kaart reken" id="check"><h2 style="margin-top:0">Snelle check: kom jij in aanmerking?</h2>'
             '<label for="sit">Je situatie</label><select id="sit"><option value="a">Alleenstaand</option><option value="p">Met toeslagpartner</option></select>'
             '<label for="ink">Verwacht jaarinkomen 2027 (samen, als je een partner hebt)</label><input id="ink" type="number" inputmode="numeric" min="0" step="500" value="30000">'
             '<label for="verm">Spaargeld en beleggingen op 1 januari 2027 (samen)</label><input id="verm" type="number" inputmode="numeric" min="0" step="1000" value="10000">'
             '<div class="uit" id="tuit" role="status" aria-live="polite"></div>'
             '<p class="bron">Gebaseerd op de verwachte grenzen voor 2027. Alleen een indicatie: doe voor zekerheid de <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/toeslagen/content/hulpmiddel-proefberekening-toeslagen" rel="noopener">proefberekening van Dienst Toeslagen</a>.</p></div>'
             """<script>
(function(){var G={a:[42950,119122,140],p:[54150,158748,268]},s=document.getElementById('sit'),i=document.getElementById('ink'),v=document.getElementById('verm'),u=document.getElementById('tuit');
function eur(x){return '€ '+Math.round(x).toLocaleString('nl-NL')}
function r(){var g=G[s.value],ink=+i.value||0,verm=+v.value||0;
if(verm>g[1])u.textContent='Je vermogen ligt boven de grens van '+eur(g[1])+'. Dan krijg je in 2027 waarschijnlijk geen zorgtoeslag.';
else if(ink>g[0])u.textContent='Je inkomen ligt boven de verwachte grens van ongeveer '+eur(g[0])+'. Dan krijg je waarschijnlijk geen zorgtoeslag.';
else u.textContent='Je komt waarschijnlijk in aanmerking. Hoe lager je inkomen, hoe meer je krijgt: maximaal '+eur(g[2])+' per maand. Doe de proefberekening voor het precieze bedrag.'}
[s,i,v].forEach(function(e){e.addEventListener('input',r);e.addEventListener('change',r)});r()})();
</script>""")
    body = (ch + '<h1>Zorgtoeslag 2027: hogere toeslag, lagere vermogensgrens</h1><p class="lead">De maximale zorgtoeslag gaat omhoog. Maar wie spaargeld heeft, kan zijn toeslag juist kwijtraken.</p>'
            '<table><tr><th></th><th class="r">Alleenstaand</th><th class="r">Met partner</th></tr>'
            '<tr><td>Maximale toeslag per maand</td><td class="r">€ 140</td><td class="r">± € 268</td></tr>'
            '<tr><td>Inkomensgrens (verwacht)</td><td class="r">± € 42.950</td><td class="r">± € 54.150</td></tr>'
            '<tr><td>Vermogensgrens op 1 januari</td><td class="r">€ 119.122</td><td class="r">€ 158.748</td></tr>'
            '<tr><td>Vermogensgrens in 2026</td><td class="r">€ 146.011</td><td class="r">€ 184.633</td></tr></table>'
            + check +
            '<h2>Let op de lagere vermogensgrens</h2><p>De vermogensgrens daalt in 2027 flink. Zit je op 1 januari 2027 boven de grens, dan vervalt je zorgtoeslag voor het hele jaar. '
            'Tot het vermogen horen spaargeld, beleggingen en bijvoorbeeld een tweede huis. Je eigen woning en je pensioen tellen niet mee.</p>'
            '<h2>Krijg je nu geen zorgtoeslag?</h2><p>De inkomensgrens gaat omhoog. Wie in 2026 net te veel verdiende, kan in 2027 misschien wel recht hebben. Je krijgt het niet vanzelf: je moet het zelf aanvragen.</p>'
            + faq_html(faq_t)
            + '<p class="bron">Bronnen: <a href="https://www.zorgwijzer.nl/zorgverzekering-2027/zorgtoeslag-stijgt-in-2027-zoveel-krijg-je-erbij" rel="noopener">Zorgwijzer</a>, '
              '<a href="https://www.hartvannederland.nl/economie/geld/artikelen/zorgtoeslag-2027-bedrag-inkomensgrens" rel="noopener">Hart van Nederland</a> (op basis van de begrotingen VWS en SZW 2027). '
              f'De inkomensgrenzen zijn een raming; Dienst Toeslagen maakt de definitieve bedragen bekend. Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/zorgtoeslag-2027/", "Zorgtoeslag 2027: bedragen, grenzen en snelle check", "Zorgtoeslag 2027: maximaal € 140 per maand (alleenstaand), inkomensgrens ± € 42.950 en een lagere vermogensgrens van € 119.122. Check of jij recht hebt.",
         body, [cld, faq_ld(faq_t)], prio="0.9")

    # ---------- Over ----------
    ch, cld = crumbs("Over Bespaarvriend", "/over/")
    body = (ch + '<h1>Over Bespaarvriend</h1><div class="kaart"><p style="margin-top:0">Bespaarvriend is gemaakt door Erik Beltman uit Rijssen, ook de maker van <a href="https://boodschappenvergelijk.nl/">Goedkope Boodschappen</a>. '
            'Het doel is simpel: mensen helpen besparen in deze dure tijd, met uitleg die iedereen begrijpt.</p>'
            '<p><b>Onafhankelijk.</b> We verkopen zelf geen verzekeringen of energiecontracten. Verdienen we ooit iets aan een link, dan staat dat er duidelijk bij en verandert het niets aan de uitleg.</p>'
            '<p><b>Geen advies.</b> We leggen uit en verwijzen naar officiële bronnen en onafhankelijke vergelijkers. We geven geen persoonlijk financieel advies.</p>'
            '<p style="margin-bottom:0"><b>Klopt er iets niet?</b> Laat het weten via de <a href="/contact/">contactpagina</a>. Dan pas ik het snel aan.</p></div>')
    page("/over/", "Over Bespaarvriend", "Bespaarvriend is gemaakt door Erik Beltman, ook de maker van Goedkope Boodschappen. Onafhankelijke uitleg over besparen, zonder verkooppraatjes.", body, [cld], prio="0.4")

    # ---------- Privacy ----------
    ch, cld = crumbs("Privacy", "/privacy/")
    body = (ch + '<h1>Privacy</h1><div class="kaart"><p style="margin-top:0">Bespaarvriend gebruikt geen cookies, geen advertenties en geen trackers die je volgen.</p>'
            '<p>De rekenhulpen werken helemaal in je eigen browser: wat je invult, wordt nergens naartoe gestuurd of bewaard.</p>'
            '<p>Stuur je een bericht via de contactpagina, dan bewaren we je bericht (en je naam en e-mailadres als je die invult) alleen om je te kunnen antwoorden. '
            'We delen het met niemand en verwijderen het als het niet meer nodig is.</p><p style="margin-bottom:0">De site draait bij Netlify. Netlify houdt voor de beveiliging korte tijd technische gegevens bij, zoals IP-adressen.</p></div>')
    page("/privacy/", "Privacy | Bespaarvriend", "Bespaarvriend gebruikt geen cookies en geen trackers. Rekenhulpen werken in je eigen browser.", body, [cld], prio="0.2")

    # ---------- Contact (Netlify Forms, geen e-mailadres op de site) ----------
    ch, cld = crumbs("Contact", "/contact/")
    body = (ch + '<h1>Contact</h1><p class="lead">Een vraag, een fout gezien of een tip? Laat het weten.</p>'
            '<form class="contact kaart" name="contact" method="POST" action="/bedankt/" data-netlify="true" netlify-honeypot="website">'
            '<input type="hidden" name="form-name" value="contact"><p class="hp"><label>Niet invullen <input name="website"></label></p>'
            '<label for="onderwerp">Onderwerp</label><select id="onderwerp" name="onderwerp" required><option value="">Kies een onderwerp</option><option>Vraag</option><option>Fout op de site</option><option>Tip of idee</option><option>Pers en media</option><option>Samenwerking</option><option>Privacy</option><option>Overig</option></select>'
            '<label for="bericht">Je bericht</label><textarea id="bericht" name="bericht" rows="6" maxlength="2000" required></textarea>'
            '<label for="naam">Naam <small>(mag leeg)</small></label><input id="naam" name="naam" maxlength="80" autocomplete="name">'
            '<label for="email">E-mail <small>(alleen als je antwoord wilt)</small></label><input id="email" name="email" type="email" maxlength="120" autocomplete="email">'
            '<p><button class="btn" type="submit">Versturen</button></p></form>')
    page("/contact/", "Contact | Bespaarvriend", "Neem contact op met Bespaarvriend: een vraag, een fout of een tip.", body, [cld], prio="0.3")
    page("/bedankt/", "Bedankt | Bespaarvriend", "Je bericht is verstuurd.", '<h1>Bedankt!</h1><p class="lead">Je bericht is verstuurd. Heb je je e-mailadres ingevuld, dan krijg je antwoord.</p><p><a class="btn" href="/">Terug naar home</a></p>', noindex=True)
    page("/404.html", "Pagina niet gevonden | Bespaarvriend", "Deze pagina bestaat niet.", '<h1>Pagina niet gevonden</h1><p>Deze pagina bestaat niet (meer). <a href="/">Naar de homepage</a></p>', noindex=True)

    # ---------- sitemap, robots, llms.txt ----------
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                + "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{VANDAAG}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES) + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(f"""# Bespaarvriend
> Gratis, onafhankelijke uitleg over besparen op vaste lasten in Nederland. Gemaakt door Erik Beltman (ook maker van boodschappenvergelijk.nl). Bijgewerkt op {BIJGEWERKT}.

- [Zorgverzekering 2027]({BASE}/zorgverzekering-2027/): gemiddelde premie € 173,13 per maand, goedkoopste € 148,40, duurste € 202,50, verschil € 649 per jaar; overstappen vóór 31 december 2026.
- [Eigen risico 2027]({BASE}/eigen-risico-2027/): verplicht eigen risico € 400 (2026: € 385), met rekenhulp vrijwillig eigen risico.
- [Zorgtoeslag 2027]({BASE}/zorgtoeslag-2027/): maximaal € 140 per maand (alleenstaand), inkomensgrens ± € 42.950, vermogensgrens € 119.122.
- [Boodschappen vergelijken](https://boodschappenvergelijk.nl/): dagelijkse prijzen van supermarkten.
""")
    print(f"klaar: {len(PAGES)} pagina's in {OUT}")


if __name__ == "__main__":
    bouw()
