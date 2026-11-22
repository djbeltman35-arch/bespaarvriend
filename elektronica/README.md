# Elektronica-vergelijker (bespaarvriend.nl/elektronica/)

Prijsvergelijker voor witgoed, tv/audio, computers, telefoons enz. bij Nederlandse webwinkels, prijs mét en zónder verzendkosten. Alleen losse producten.
Wordt gebouwd door `../build.py` (Bespaarvriend) via `scripts/build.py` met SITE_BASIS=/elektronica.

## Bestanden
- `raw/catalogus.txt` – productlijst: `cat|naam|coolblue prijs|coolblue id|zoekterm|verplichte tokens|-uitsluitwoorden`
- `raw/<winkel>.txt` – opgehaalde aanbiedingen, records `k|prijs|beschikbaarheid|verkoper|verzend|url-pad|naam`, gescheiden door ` ## ` of nieuwe regels. `k` = regelnummer (0-based, zonder commentaarregels) in catalogus.txt.
- `raw/specs.txt`, `raw/specs2.txt` – specificaties van Coolblue per Coolblue-ID.
- `data/config.json` – groepen, categorieën, subcategorieën, winkels (+ verzendtekst), vaste pagina's.
- `scripts/samenstellen.py` – valideert matches (typenummer/tokens, prijsplausibiliteit, minimaal 2 winkels) → `data/prijzen.json`. Nieuwe winkel: toevoegen aan BASIS, EIGEN, de bestandenlijst en verzendregel in dit script én aan `winkels` in config.json.
- `scripts/build.py` – genereert de pagina's. `PARTNERS` (advertentietegels per categorie) en `winkellink()` (partnerlinks per winkel; bol via site-ID 1562371).
- `tools/m.js` – matcher die in Chrome op de site van een winkel draait (zie hieronder). Gehost op https://elektrovergelijk.netlify.app/tools/m.js (CORS *).

## Prijzen ophalen (Claude in Chrome)
1. Open de winkel in een tab. Zet `window.__S={search:'<zoek-URL met {q}>', link:'<regex voor productlinks>', wait:600, pricesel:'<css, optioneel>', eigen:'<regex eigen prijs, optioneel>'}`.
2. Laad m.js: `fetch('https://elektrovergelijk.netlify.app/tools/m.js').then(r=>r.text()).then(s=>(new Function(s))())`. `window.__ITEMS` in m.js moet dezelfde volgorde hebben als catalogus.txt (q=zoekterm, i=verplichte tokens, x=uitsluitwoorden). Na het uitbreiden van de catalogus m.js opnieuw genereren en (optioneel) op elektrovergelijk deployen, of __ITEMS zelf in de pagina zetten vóór het laden.
3. Voortgang: `window.__st`; resultaat: `window.__res[k]` met prijs, naam, url. Dump in delen (uitvoer wordt afgekapt; geen querystrings in de uitvoer) en zet om naar `raw/<winkel>.txt`.
4. Prijzen komen uit JSON-LD `offers.price`. Controleer altijd op de productnaam (varianten!). BCC is grotendeels zelf een vergelijker: alleen de eigen prijs ("€ X Bestel bij BCC") telt.
5. `python3 scripts/samenstellen.py` en daarna vanuit de repo-root `python3 build.py`.

## Verzendregels
Coolblue 0 · MediaMarkt gratis vanaf € 50 (onder € 50 niet opgenomen) · bol € 2,99 onder € 25 als bol zelf verkoopt, anders 0 · Amazon € 2,99 onder € 20 · Alternate per product uit JSON-LD shippingRate · Azerty uit JSON-LD (excl. btw → ×1,21) · Mobiel.nl losse telefoon gratis.

## Bekend
Wehkamp geeft 429 (bot-bescherming). Megekko, Expert en EP renderen zoekresultaten in de browser (fetch+DOMParser werkt niet; pagina zelf openen).

## Versie 2 (vanaf 22 nov 2026): matchen op fabrikantcode
1. Coolblue-oogst (`scripts/cb_oogst.js` in een coolblue.nl-tab): per categorie de populairste producten (filterpagina's, 2 pagina's) met prijs, fabrikantcode en specs → opslag `cb_<cat>`.
2. `scripts/items.py <cats>` maakt de zoeklijst `items` (zoekterm = fabrikantcode, of naam bij telefoons/tablets/audio).
3. `tools/m2.js` (gehost op elektrovergelijk.netlify.app/tools/m2.js) draait per winkel in Chrome: `window.__K=<sleutel>; window.__S={shop:'mm_2',search:'/nl/search.html?query={q}',link:'/nl/product/',wait:250,max:2}`. Een treffer telt alleen als de fabrikantcode op de productpagina staat (of alle naamwoorden kloppen bij telefoons/tablets/audio).
   Winkels: MediaMarkt (zie boven), Amazon (`/s?k={q}`, link `/dp/`, pricesel `#corePrice_feature_div .a-offscreen, .priceToPay .a-offscreen`), Alternate (`/listing.xhtml?q={q}`, `/html/product/`), Azerty (`/search?q={q}`, `/product/`).
   bol blokkeert externe verzoeken: gebruik `scripts/bol_api.py` (bol Marketing Catalog API via bespaarvriend.nl/api/bol; sleutel in Netlify-variabelen BOL_CLIENT_ID/BOL_CLIENT_SECRET).
4. `DUMPKEY=<sleutel> sh scripts/ophalen_v2.sh` → `raw/v2/`, daarna `python3 scripts/samenstellen2.py` (oude producten uit `raw/prijzen_basis.json` blijven behouden).
De opslagsleutel staat niet in deze repo.

## MediaMarkt als extra basis (vanaf 22 nov 2026)
Voor categorieën waar Coolblue weinig heeft: `scripts/mm_oogst.js` in een mediamarkt.nl-tab (kaart `mm_map` in de dump: onze categorie → MediaMarkt-categoriepagina's) → `mmb_<cat>`.
`python3 scripts/items.py mmb_a,mmb_b,... items_mm` (EAN gaat mee voor bol), daarna m2.js bij Coolblue (`cbm_*`, zoek `/zoeken?query={q}`), Amazon, EP en `bol_api.py items_mm`.
`samenstellen2.py` neemt alleen MediaMarkt-eigen producten vanaf € 50 en slaat producten over die al in de Coolblue-basis zitten (zelfde fabrikantcode).
