#!/usr/bin/env python3
"""Bouwt Bespaarvriend.nl: een kleine, snelle statische site over slim besparen op vaste lasten.
Uitvoer in public/. Draait op Netlify (zie netlify.toml) en lokaal met: python3 build.py"""
import html, json, os, shutil, datetime

BASE = "https://bespaarvriend.nl"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
VANDAAG = datetime.date.today().isoformat()
BIJGEWERKT = "19 november 2026"
esc = html.escape

CSS = """
@font-face{font-family:"Atkinson Hyperlegible";font-weight:400;font-display:swap;src:url(/fonts/atkinson-hyperlegible-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Atkinson Hyperlegible";font-weight:700;font-display:swap;src:url(/fonts/atkinson-hyperlegible-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"Barlow Condensed";font-weight:700;font-display:swap;src:url(/fonts/barlow-condensed-latin-700-normal.woff2) format("woff2")}
:root{--page:#f4f7f1;--surface:#fff;--ink:#1e2a22;--muted:#5d6a61;--line:#e1e7dc;--soft:#eef3ea;--green:#0e7c4a;--green-dark:#0a6239;--green-soft:#e2f2e8;--on-green:#fff;--tag:#ffd43b;--tag-ink:#1e2a22;--tag-soft:#fff6cc;
--text:"Atkinson Hyperlegible",system-ui,-apple-system,"Segoe UI",sans-serif;--num:"Barlow Condensed","Arial Narrow",system-ui,sans-serif;--r:14px;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--page:#121813;--surface:#1a221c;--ink:#e9efe8;--muted:#a3b0a6;--line:#2b362e;--soft:#202a23;--green:#3fbf7f;--green-dark:#5ad093;--green-soft:#1d3326;--on-green:#0f1a13;--tag-soft:#3a3315;color-scheme:dark}}
*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--page);color:var(--ink);font:17px/1.5 var(--text)}
a{color:var(--green-dark);text-underline-offset:3px;text-decoration-thickness:1px}a:hover{color:var(--green)}img{max-width:100%}
:focus-visible{outline:3px solid var(--green);outline-offset:2px;border-radius:6px}
.wrap{max-width:820px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left,0px))}
header.top{background:var(--surface);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;gap:12px;padding-block:12px;max-width:1140px}
.logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:19px;color:var(--ink);text-decoration:none}
nav.top{margin-left:auto;display:flex;gap:4px}nav.top a{text-decoration:none;font-weight:700;font-size:15px;padding:8px 10px;border-radius:10px;color:var(--ink)}
nav.top a:hover{background:var(--green-soft);color:var(--green-dark)}
@media(max-width:420px){.logo{font-size:17px;gap:8px}.logo svg{width:32px;height:32px}nav.top{gap:0}nav.top a{font-size:14px;padding:7px 6px}}
.crumbs{font-size:14px;color:var(--muted);margin:16px 0 0}.crumbs a{color:var(--muted)}
h1{font:700 clamp(28px,4.6vw,40px)/1.12 var(--text);letter-spacing:-.015em;margin:14px 0 10px;text-wrap:balance}
h2{font:700 22px/1.25 var(--text);margin:30px 0 10px}h3{font-size:18px;margin:20px 0 6px}h1,h2,h3{overflow-wrap:break-word;hyphens:auto}
.lead{font-size:18px;color:var(--muted);margin:0 0 16px}
.kaart{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:18px;margin:14px 0}
.kerncijfers{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:16px 0}
.kerncijfers div{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px}
.kerncijfers b{display:inline-block;background:var(--tag);color:var(--tag-ink);font:700 26px/1 var(--num);padding:5px 9px 4px;border-radius:5px;box-shadow:inset 0 -3px 0 rgba(0,0,0,.08);font-variant-numeric:tabular-nums;margin-bottom:6px}
.kerncijfers small{display:block;color:var(--muted);font-size:14px}
.tegels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:16px 0}
.tegels a{display:block;padding:16px 14px;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:var(--r);transition:border-color .15s}
.tegels a:hover{border-color:var(--green)}
.tegels .ic{font-size:26px;display:block}.tegels b{display:block;font-size:17px;margin-top:4px}.tegels small{color:var(--muted);font-size:14px}
.let{background:var(--tag-soft);border:1px solid var(--line);border-left:5px solid var(--tag);border-radius:var(--r);padding:12px 14px;margin:14px 0}
.btn{display:inline-block;background:var(--green);color:var(--on-green);font:700 16px var(--text);padding:12px 18px;border:0;border-radius:12px;text-decoration:none;cursor:pointer}
.btn:hover{background:var(--green-dark);color:var(--on-green)}
ol.stappen{counter-reset:s;list-style:none;padding:0;margin:12px 0}
ol.stappen li{counter-increment:s;position:relative;padding:12px 0 12px 46px;border-bottom:1px solid var(--line)}
ol.stappen li:before{content:counter(s);position:absolute;left:0;top:10px;width:32px;height:32px;border-radius:50%;background:var(--green);color:var(--on-green);font:700 18px var(--num);display:grid;place-items:center}
table{width:100%;border-collapse:separate;border-spacing:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;margin:10px 0;font-size:16px}
th,td{padding:11px 14px;text-align:left;border-top:1px solid var(--line)}tr:first-child th,tr:first-child td{border-top:0}th{background:var(--soft);font-size:14px;color:var(--muted)}
td.r,th.r{text-align:right;white-space:nowrap;font-family:var(--num);font-size:18px}
.faq details{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);margin:8px 0}.faq summary{cursor:pointer;padding:13px 16px;font-weight:700}.faq details p{margin:0;padding:0 16px 14px}
.reken label{display:block;font-weight:700;margin:12px 0 4px}.reken input,.reken select{width:100%;padding:11px 12px;font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:12px}
.reken .uit{margin-top:14px;padding:14px;background:var(--green-soft);border-radius:12px;font-weight:700;min-height:1em}
.bron{font-size:14px;color:var(--muted)}.links li{margin:4px 0}
.widget{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:12px;margin:14px 0;min-height:200px}
.ad{font-size:13px;color:var(--muted);margin:0 0 6px}
footer{margin-top:40px;background:var(--surface);border-top:1px solid var(--line);padding:24px 0 30px;font-size:15px;color:var(--muted)}
footer p:first-child{color:var(--ink);font-weight:700}
footer nav{display:flex;flex-wrap:wrap;gap:6px 18px;margin:10px 0}footer nav a{font-weight:700;text-decoration:none;color:var(--green-dark)}footer nav a:hover{text-decoration:underline}
form.contact label{display:block;font-weight:700;margin:12px 0 4px}form.contact input,form.contact select,form.contact textarea{width:100%;padding:11px 12px;font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:12px}
.hp{position:absolute;left:-9999px}
@media(min-width:700px){.kerncijfers,.tegels{grid-template-columns:repeat(4,minmax(0,1fr))}}
.logo svg{flex:none;display:block}
.hero{position:relative;margin:18px 0 8px;padding:26px 22px 24px;border-radius:22px;background:linear-gradient(135deg,var(--green-soft),var(--surface) 70%);border:1px solid var(--line);overflow:hidden}
.hero:after{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--tag) 45%,transparent),transparent 70%);pointer-events:none}
.hero h1{margin-top:6px;max-width:16ch}.hero .lead{max-width:46ch}
.kicker{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:14px;color:var(--green-dark);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:5px 12px}
.knoppen{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.btn-line{display:inline-block;background:var(--surface);color:var(--ink);border:2px solid var(--line);font:700 16px var(--text);padding:10px 16px;border-radius:12px;text-decoration:none}
.btn-line:hover{border-color:var(--green);color:var(--green-dark)}
.btn svg,.btn-line svg{width:18px;height:18px;vertical-align:-3px;margin-left:6px}
.vertrouwen{display:flex;flex-wrap:wrap;gap:8px 18px;list-style:none;padding:0;margin:18px 0 0;font-size:15px;font-weight:700;color:var(--muted)}
.vertrouwen li{display:flex;align-items:center;gap:6px}.vertrouwen svg{width:18px;height:18px;color:var(--green)}
.tegels .ic{display:inline-grid;place-items:center;width:44px;height:44px;border-radius:12px;background:var(--green-soft);color:var(--green-dark);font-size:0}
.tegels .ic svg{width:24px;height:24px}
.tegels a{position:relative}.tegels.tools a:last-child:nth-child(odd){grid-column:span 2}.tegels a .pijl{position:absolute;right:14px;top:18px;color:var(--muted)}.tegels a .pijl svg{width:18px;height:18px}
.tegels a:hover .pijl{color:var(--green)}
.tegels .nieuw{position:absolute;right:38px;top:16px;font-size:12px;font-weight:700;background:var(--tag);color:var(--tag-ink);border-radius:999px;padding:2px 8px}
.let .icl{display:inline-flex;vertical-align:-4px;margin-right:4px;color:var(--tag-ink)}.let .icl svg{width:20px;height:20px}
.drie{display:grid;gap:10px;margin:14px 0;counter-reset:d}
.drie div{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px 16px 16px 60px;position:relative;counter-increment:d}
.drie div:before{content:counter(d);position:absolute;left:16px;top:16px;width:30px;height:30px;border-radius:50%;background:var(--green);color:var(--on-green);font:700 18px var(--num);display:grid;place-items:center}
.drie b{display:block}.drie p{margin:2px 0 0;color:var(--muted);font-size:15px}
.media{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 0}.media span{font-size:13px;font-weight:700;border:1px solid var(--line);border-radius:999px;padding:4px 10px;color:var(--muted)}
.paginakop{display:flex;align-items:center;gap:12px;margin-top:14px}.paginakop .ic{flex:none;display:grid;place-items:center;width:48px;height:48px;border-radius:14px;background:var(--green-soft);color:var(--green-dark)}
.paginakop h1{margin:0}
.wijzigt{list-style:none;padding:0;margin:12px 0;display:grid;gap:10px}
.wijzigt li{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px}
.wijzigt li b{display:block}.wijzigt .bedrag{float:right;font:700 20px var(--num);margin-left:10px}.wijzigt .op{color:#b42318}.wijzigt .af{color:var(--green)}
@media(min-width:700px){.tegels{grid-template-columns:repeat(3,minmax(0,1fr))}.tegels.tien{grid-template-columns:repeat(3,minmax(0,1fr))}.tegels.tools{grid-template-columns:repeat(4,minmax(0,1fr))}.drie{grid-template-columns:repeat(3,minmax(0,1fr))}.hero{padding:40px 36px 34px}.wijzigt{grid-template-columns:repeat(2,minmax(0,1fr))}}
.partner .ad{margin:0 0 4px;font-size:13px;color:var(--muted)}.partner b{display:block;font-size:18px}.partner p{margin:4px 0 12px}.partner .bron{margin:10px 0 0}.pchips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}.pchips a{border:1px solid var(--line);border-radius:999px;padding:6px 12px;font-weight:700;font-size:14px;text-decoration:none;color:var(--green-dark);background:var(--green-soft)}.pchips a:hover{border-color:var(--green)}
.tool{display:flex;gap:14px;align-items:flex-start;border-color:var(--green);background:linear-gradient(135deg,var(--green-soft),var(--surface) 75%)}.tool .ic{flex:none;display:grid;place-items:center;width:48px;height:48px;border-radius:14px;background:var(--tag);color:var(--tag-ink)}.tool p{margin:4px 0 12px}
@media(max-width:640px){header.top .wrap{flex-wrap:wrap;row-gap:4px}nav.top{margin-left:0;width:100%;overflow-x:auto;scrollbar-width:none}nav.top a{white-space:nowrap}}@media(max-width:400px){.logo span{font-size:17px}}

/* gbstijl:start */
:root{--r:4px}
.hero{background:none!important;border:0!important;border-radius:0!important;padding:18px 0 6px!important;margin:0!important;text-align:center;overflow:visible!important}
.hero:after{display:none!important}
.hero h1{max-width:none!important;margin:0 0 4px!important;font-size:clamp(24px,6.6vw,42px)!important;letter-spacing:-.015em}
.hero .lead{max-width:none!important;color:var(--muted);font-size:16px;margin:0 auto 4px}
.maker{font-size:13px;color:var(--muted);margin:0 0 6px}
.maker a{color:var(--ink);font-weight:700;text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:3px}
.hero .knoppen{justify-content:center;display:flex;gap:8px;flex-wrap:nowrap}.hero .knoppen a{padding:11px 14px!important;font-size:15px!important;white-space:nowrap}
.hero .vertrouwen{justify-content:center;display:flex;flex-wrap:wrap;gap:2px 12px;padding:0;margin:10px 0 0;font-size:13px}.hero .vertrouwen li{display:flex;align-items:center;gap:4px}.hero .vertrouwen svg{width:15px;height:15px}
.stapjes{list-style:none;display:flex;margin:14px auto 12px;padding:0;max-width:640px;background:var(--surface);border:1px solid var(--line)}
.stapjes li{flex:1;display:flex;align-items:center;justify-content:center;gap:7px;padding:10px 4px;font-size:14px;font-weight:700;border-left:1px solid var(--line)}
.stapjes li:first-child{border-left:0}
.stapjes .n{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-size:13px;background:#f5c400;color:#1e2a22;flex:none}
.btn{background:linear-gradient(180deg,#17a061 0%,#0e7c4a 55%,#0b6a3f 100%)!important;color:#fff!important;border-radius:10px!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.28),0 3px 0 #08502f,0 5px 10px rgba(8,80,47,.28)!important}
.btn:active{transform:translateY(2px)}
.btn-line{border-radius:10px!important}
.tegels{gap:0!important;border:1px solid var(--line);background:var(--surface)}
.tegels a{border:0!important;border-radius:0!important;border-right:1px solid var(--line)!important;border-bottom:1px solid var(--line)!important}
.tegels .ic{border-radius:50%!important}
@media(max-width:640px){header.top .wrap{flex-wrap:nowrap!important;gap:6px}nav.top{width:auto!important;margin-left:auto!important}.logo span{display:none}nav.top{overflow-x:auto;scrollbar-width:none;flex-wrap:nowrap}nav.top::-webkit-scrollbar{display:none}nav.top a{white-space:nowrap}}
/* gbstijl:end */
"""

def _svg(d, extra=""):
    return f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{d}</svg>'
ICON = {
    "zorg": _svg('<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/><path d="M3.2 12h4.3l1.5-3 3 6 1.5-3h7.3"/>'),
    "risico": _svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="M14.5 9.5a3 3 0 1 0 0 5M8.5 11h5M8.5 13h5"/>'),
    "toeslag": _svg('<path d="M4 2v20l2.5-1.5L9 22l3-1.5 3 1.5 2.5-1.5L20 22V2l-2.5 1.5L15 2l-3 1.5L9 2 6.5 3.5Z"/><path d="M8 8h8M8 12h8M8 16h5"/>'),
    "energie": _svg('<path d="M13 2 4 14h7l-1 8 9-12h-7Z"/>'),
    "internet": _svg('<path d="M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M2 9a15 15 0 0 1 20 0"/><circle cx="12" cy="19.5" r="1"/>'),
    "mobiel": _svg('<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/>'),
    "boodschappen": _svg('<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>'),
    "check": _svg('<path d="M20 6 9 17l-5-5"/>'),
    "klok": _svg('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>'),
    "bron": _svg('<path d="M4 19.5V4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>'),
    "pijl": _svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "tank": _svg('<path d="M3 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18M2 22h14M7 7h4"/><path d="M15 9h2a2 2 0 0 1 2 2v6a1.5 1.5 0 0 0 3 0V8l-3-3"/>'),
    "vlucht": _svg('<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>'),
    "weg": _svg('<path d="M4 22 9 2M20 22 15 2M12 4v3M12 11v3M12 18v3"/>'),
    "koffer": _svg('<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M8 11v6M16 11v6"/>'),
    "sleutel": _svg('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>'),
    "map": _svg('<path d="M4 20h16a1 1 0 0 0 1-1V8a1 1 0 0 0-1-1h-7.9a1 1 0 0 1-.8-.4L10.5 5.4A1 1 0 0 0 9.7 5H4a1 1 0 0 0-1 1v13a1 1 0 0 0 1 1Z"/><path d="m9 13 2 2 4-4"/>'),
    "bon": _svg('<path d="M6 2h12v20l-3-2-3 2-3-2-3 2Z"/><path d="M9 7h6M9 11h6M9 15h3"/>'),
    "zon": _svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
}
LOGO = ('<svg viewBox="0 0 40 40" width="36" height="36" aria-hidden="true"><rect width="40" height="40" rx="11" fill="var(--green)"/>'
        '<path d="M26.5 12.6a8.6 8.6 0 1 0 0 14.8" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>'
        '<path d="M10.5 18h11M10.5 22.5h9.5" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
        '<circle cx="31" cy="9" r="5" fill="var(--tag)" stroke="var(--surface)" stroke-width="2"/></svg>')

# Daisycon-vergelijkers. Zet GEKEURD op True zodra Daisycon de media Bespaarvriend (449774) heeft gekeurd;
# tot die tijd vallen kliks terug op een Daisycon-overzicht en tonen we de blokken niet.
DAISYCON_GEKEURD = False
DC_MEDIA = 449774
WIDGETS = {  # naam: (script-slug, css-klasse, extra config)
    "energie": ("energy-nl", "dc-energy-tool", {}),
    "simonly": ("sim-only", "dc-sim-only-tool", {"limit": 6, "limitSplit": 6, "showFilters": False}),
    "telecom": ("all-in-one", "dc-all-in-one-tool", {"limit": 6, "limitSplit": 6, "showFilters": False}),
    "vakantie": ("vacation", "dc-vacation-tool", {"limit": 6, "limitSplit": 6, "showFilters": False}),
}

def widget(naam, titel):
    if not DAISYCON_GEKEURD or naam not in WIDGETS:
        return ""
    slug, klasse, extra = WIDGETS[naam]
    cfg = {"mediaId": DC_MEDIA, "subId": "bespaarvriend-" + naam, "language": "nl", "filter": {}}
    cfg.update(extra)
    return (f'<section class="widget" aria-label="{esc(titel)}"><h2>{esc(titel)}</h2><p class="ad">Advertentie. Sluit je via deze vergelijker iets af, dan krijgt Bespaarvriend een vergoeding. Jij betaalt niets extra.</p>'
            f'<script src="https://daisycon.tools/{slug}/app.js" defer></script><div class="dc-tool {klasse}" data-config=\'{json.dumps(cfg)}\'></div></section>')

from urllib.parse import quote as _q
def awin(mid, ref, doel=None):
    u = f"https://www.awin1.com/cread.php?awinmid={mid}&amp;awinaffid=3152283&amp;clickref={ref}"
    return u + (f"&amp;ued={_q(doel, safe='')}" if doel else "")
def partner(url, titel, tekst, knop, artikelen=()):
    chips = ''.join(f'<a href="{u}" rel="sponsored noopener" target="_blank">{esc(t)}</a>' for t, u in artikelen)
    return (f'<div class="kaart partner"><p class="ad">Advertentie</p><b>{titel}</b><p>{tekst}</p>'
            + (f'<div class="pchips">{chips}</div>' if chips else '') +
            f'<a class="btn" href="{url}" rel="sponsored noopener" target="_blank">{knop}{ICON["pijl"]}</a>'
            '<p class="bron">Sluit je via deze link iets af, dan krijgt Bespaarvriend een kleine vergoeding. Jij betaalt niets extra.</p></div>')

NAV = '<nav class="top" aria-label="Hoofdmenu"><a href="/zorgverzekering-2027/">Zorg</a><a href="/energie-2027/">Energie</a><a href="/internet-en-mobiel/">Internet</a><a href="/vakantie-en-vliegen/">Vakantie</a><a href="/auto-en-tanken/" class="wide">Auto</a></nav>'
FOOT = f"""<footer><div class="wrap">
<p><b>Bespaarvriend</b> helpt je eenvoudig besparen op je vaste lasten. Onafhankelijk uitgelegd, zonder verkooppraatjes. Wij geven geen persoonlijk financieel advies.</p>
<nav aria-label="Over"><a href="/zorgverzekering-2027/">Zorgverzekering 2027</a><a href="/eigen-risico-2027/">Eigen risico 2027</a><a href="/zorgtoeslag-2027/">Zorgtoeslag 2027</a><a href="/aanvullende-verzekering-2027/">Aanvullende verzekering 2027</a><a href="/tandartsverzekering-2027/">Tandartsverzekering 2027</a><a href="/energie-2027/">Energie 2027</a><a href="/energiecontract-opzeggen/">Energiecontract opzeggen</a><a href="/internet-en-mobiel/">Internet en mobiel</a><a href="/vakantie-en-vliegen/">Vakantie en vliegen</a><a href="/auto-en-tanken/">Auto en tanken</a><a href="/boodschappen/">Boodschappen</a><a href="/administratie/">Administratie</a><a href="https://allesoporde.netlify.app/">Alles op orde</a><a href="https://bonnenboek.netlify.app/">Bonnenboek</a><a href="https://salderingscheck-nl.netlify.app/">Salderingscheck</a><a href="https://goedkopertanken.netlify.app/">Tankwijzer</a><a href="https://vluchtwijzer.netlify.app/">Vluchtwijzer</a><a href="https://vakantietoppers.netlify.app/">Vakantiewijzer</a><a href="https://euroroadrules.eu/">EuroRoadRules</a><a href="https://foutcodezoeker.nl/">Foutcodezoeker</a><a href="https://boodschappenvergelijk.nl/">Boodschappen vergelijken</a><a href="/over/">Over Bespaarvriend</a><a href="/privacy/">Privacy</a><a href="/contact/">Contact</a></nav>
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
{'<meta name="robots" content="noindex">' if noindex else ''}<meta name="theme-color" content="#0e7c4a">
{'<meta name="e0d5a73bd035a1c" content="277030417ea9ada19f69ae08c41fb74b">' if path == "/" else ''}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:locale" content="nl_NL"><meta property="og:image" content="{BASE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta property="og:site_name" content="Bespaarvriend">
<link rel="preload" href="/fonts/atkinson-hyperlegible-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/manifest.webmanifest"><meta name="theme-color" content="#0e7c4a"><script src="/installeer.js" defer></script>
<style>{CSS}</style>
{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in lds)}
</head><body><header class="top"><div class="wrap"><a class="logo" href="/" aria-label="Bespaarvriend, naar de startpagina">{LOGO}<span>Bespaarvriend</span></a>{NAV}</div></header>
<main class="wrap">{body}</main>{FOOT}<script>if("serviceWorker" in navigator)navigator.serviceWorker.register("/sw.js").catch(function(){{}})</script></body></html>"""
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


# Zorgvergelijker (Awin 107738). Voorwaarden: alleen naar de landingspagina linken (geen formulier- of resultatenpagina),
# geen merknamen van de vergelijker of verzekeraars, geen iframes/pop-ups. Provisie alleen op zorgoverstappers.
ZORG_VERGELIJKER = partner(awin(107738, "bespaarvriend-zorg", "https://www.poliswijzer.nl/zorgverzekering"),
    "Alle zorgverzekeringen van 2027 naast elkaar",
    "Vergelijk de premies en vergoedingen van alle zorgverzekeringen in één overzicht. Gratis en zonder verplichtingen.",
    "Vergelijk zorgverzekeringen")

# Tegels bovenaan de startpagina: direct naar goedgekeurde partners (geen namen van adverteerders).
DIRECT = [
    (awin(107738, "bespaarvriend-tegel", "https://www.poliswijzer.nl/zorgverzekering"), "zorg", "Zorgverzekering vergelijken", "Overstappen kan tot 31 december"),
    (awin(8520, "bespaarvriend-tegel", "https://www.gaslicht.com/energievergelijken"), "energie", "Energiecontract vergelijken", "Ook met tarieven voor 2027"),
    (awin(8311, "bespaarvriend-tegel", "https://www.unitedconsumers.com/internet-en-tv"), "internet", "Internet en tv met korting", "Via een collectief"),
    (awin(8311, "bespaarvriend-tegel", "https://www.unitedconsumers.com/mobiel"), "mobiel", "Sim only", "Vaste prijs, maandelijks opzegbaar"),
    (awin(63484, "bespaarvriend-tegel", "https://www.vliegwinkel.nl/"), "vlucht", "Vliegtickets", "Meer dan 800 maatschappijen"),
    (awin(78144, "bespaarvriend-tegel", "https://www.hansemerkur.nl/reisverzekeringen"), "koffer", "Reisverzekering", "Eén reis of het hele jaar"),
]

def bouw():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)),'static'), OUT, dirs_exist_ok=True)
    import time as _t
    _sw=os.path.join(OUT,'sw.js'); _swt=open(_sw).read(); open(_sw,'w').write(_swt.replace('__BOUW__', _t.strftime('%Y%m%d%H%M%S')))

    # ---------- Home ----------
    faq_h = [("Wat is Bespaarvriend?", "Een gratis site die in gewone taal uitlegt hoe je bespaart op je vaste lasten en grote uitgaven, zoals je zorgverzekering, energie, internet, vakantie, auto en boodschappen. Wij verkopen zelf niets."),
             ("Geven jullie persoonlijk advies?", "Nee. We leggen uit hoe het zit en verwijzen naar onafhankelijke vergelijkers en officiële bronnen. De keuze maak je zelf."),
             ("Tot wanneer kan ik overstappen van zorgverzekering?", "Zeg je huidige zorgverzekering uiterlijk 31 december 2026 op. Je hebt daarna tot en met 31 januari 2027 om een nieuwe af te sluiten; die gaat in per 1 januari 2027.")]
    pijl = f'<span class="pijl">{ICON["pijl"]}</span>'
    body = ('<section class="hero"><p class="maker">Van de maker van <a href="https://boodschappenvergelijk.nl/?bron=bespaarvriend">Boodschappenvergelijk.nl</a>, bekend van <a href="https://www.hartvannederland.nl/advies-en-tips/kopen-besparen/videos/goedkoop-boodschappen-doen-erik-bouwt-vergelijker" target="_blank" rel="noopener">Hart van Nederland</a> en <a href="https://www.oost.nl/nieuws/3720144/rijssenaar-erik-beltman-rekent-af-met-dure-boodschappen-in-vergelijkingswebsite" target="_blank" rel="noopener">RTV Oost</a></p>'
            '<h1>Besparen op je vaste lasten</h1>'
            '<p class="lead">Gratis en onafhankelijk uitgelegd</p>'
            '<ol class="stapjes" aria-label="Zo werkt het"><li><span class="n">1</span>Kies</li><li><span class="n">2</span>Vergelijk</li><li><span class="n">3</span>Bespaar</li></ol>'
            f'<div class="knoppen"><a class="btn" href="/zorgverzekering-2027/">Bespaar op je zorgpremie{ICON["pijl"]}</a><a class="btn-line" href="/energie-2027/">Energie 2027</a></div>'
            f'<ul class="vertrouwen"><li>{ICON["check"]}Altijd met bronnen</li><li>{ICON["check"]}Geen cookies of trackers</li><li>{ICON["check"]}Rekenhulpen in je eigen browser</li></ul></section>'
            '<h2>Direct vergelijken</h2><div class="tegels direct">'
            + "".join(f'<a href="{u}" rel="sponsored noopener" target="_blank"><span class="ic">{ICON[ic]}</span>{pijl}<b>{n}</b><small>{t}</small></a>' for u, ic, n, t in DIRECT)
            + '</div><p class="bron" style="margin-top:-6px">Advertentie: deze tegels gaan naar partners. Sluit je iets af, dan krijgt Bespaarvriend een kleine vergoeding. Jij betaalt niets extra.</p>'
            f'<div class="let"><span class="icl">{ICON["klok"]}</span><b>Overstappen kan nog tot 31 december.</b> Tussen de laagste en hoogste premie voor de basisverzekering zit in 2027 € 649 per jaar, voor dezelfde basiszorg. <a href="/zorgverzekering-2027/">Zo stap je over →</a></div>'
            '<h2>Waar wil je op besparen?</h2><div class="tegels">'
            f'<a href="/zorgverzekering-2027/"><span class="ic">{ICON["zorg"]}</span>{pijl}<b>Zorgverzekering</b><small>Premies 2027 en overstappen</small></a>'
            f'<a href="/eigen-risico-2027/"><span class="ic">{ICON["risico"]}</span>{pijl}<b>Eigen risico</b><small>€ 400 in 2027, met rekenhulp</small></a>'
            f'<a href="/zorgtoeslag-2027/"><span class="ic">{ICON["toeslag"]}</span>{pijl}<b>Zorgtoeslag</b><small>Heb jij recht? Check het</small></a>'
            f'<a href="/energie-2027/"><span class="ic">{ICON["energie"]}</span>{pijl}<b>Energie</b><small>Wat verandert er in 2027</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/internet-en-mobiel/"><span class="ic">{ICON["internet"]}</span>{pijl}<b>Internet en mobiel</b><small>Stop met te veel betalen</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/vakantie-en-vliegen/"><span class="ic">{ICON["vlucht"]}</span>{pijl}<b>Vakantie en vliegen</b><small>Goedkoper weg, met vergelijkers</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/auto-en-tanken/"><span class="ic">{ICON["tank"]}</span>{pijl}<b>Auto en tanken</b><small>Brandstof en banden</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/boodschappen/"><span class="ic">{ICON["boodschappen"]}</span>{pijl}<b>Boodschappen</b><small>Vergelijken en bijhouden</small></a>'
            f'<a href="/administratie/"><span class="ic">{ICON["map"]}</span>{pijl}<b>Vaste lasten op orde</b><small>In 5 stappen overzicht</small></a>'
            '</div>'
            '<h2>Meer gratis hulpmiddelen</h2><p class="bron" style="margin-top:-4px">Ook gemaakt door Erik, net zo eerlijk en gratis.</p><div class="tegels tools">'
            f'<a href="https://allesoporde.netlify.app/"><span class="ic">{ICON["map"]}</span>{pijl}<b>Alles op orde</b><small>Al je vaste lasten en inkomsten op een rij</small></a>'
            f'<a href="https://bonnenboek.netlify.app/"><span class="ic">{ICON["bon"]}</span>{pijl}<b>Bonnenboek</b><small>Kassabonnen scannen en zien wat je uitgeeft</small></a>'
            f'<a href="https://goedkopertanken.netlify.app/"><span class="ic">{ICON["tank"]}</span>{pijl}<b>Tankwijzer</b><small>Goedkoper tanken in NL, België en Duitsland</small></a>'
            f'<a href="https://vluchtwijzer.netlify.app/"><span class="ic">{ICON["vlucht"]}</span>{pijl}<b>Vluchtwijzer</b><small>De goedkoopste vluchten vergelijken</small></a>'
            f'<a href="https://vakantietoppers.netlify.app/"><span class="ic">{ICON["koffer"]}</span>{pijl}<b>Vakantiewijzer</b><small>Pakketreizen, hotels en campings vergelijken</small></a>'
            f'<a href="https://salderingscheck-nl.netlify.app/"><span class="ic">{ICON["zon"]}</span>{pijl}<b>Salderingscheck</b><small>Wat kost het einde van salderen jou?</small></a>'
            f'<a href="https://euroroadrules.eu/"><span class="ic">{ICON["weg"]}</span>{pijl}<b>EuroRoadRules</b><small>Vignetten, tol en milieuzones in Europa</small></a>'
            f'<a href="https://foutcodezoeker.nl/"><span class="ic">{ICON["sleutel"]}</span>{pijl}<b>Foutcodezoeker</b><small>Zelf repareren in plaats van vervangen</small></a>'
            '</div>'
            '<h2>Zo werkt het</h2><div class="drie">'
            '<div><b>Kies je vaste last</b><p>Elke gids begint met de bedragen die er nu toe doen.</p></div>'
            '<div><b>Reken het na</b><p>Met de rekenhulpen zie je wat het voor jou betekent.</p></div>'
            '<div><b>Stap zelf over</b><p>Stap voor stap uitgelegd. De keuze maak jij.</p></div></div>'
            '<h2>Waarom Bespaarvriend?</h2><div class="kaart"><p style="margin-top:0">Ik ben Erik, de maker van <a href="https://boodschappenvergelijk.nl/">Goedkope Boodschappen</a>. '
            'Met Bespaarvriend wil ik mensen op dezelfde manier helpen met hun andere vaste lasten: duidelijk, eerlijk en gratis.</p>'
            '<p style="margin-bottom:0">Elke pagina noemt zijn bronnen en de datum waarop hij is bijgewerkt. Zo weet je precies waar je aan toe bent.</p>'
            '<div class="media"><span>Bekend van Hart van Nederland</span><span>RTV Oost</span></div></div>'
            + faq_html(faq_h))
    page("/", "Bespaarvriend – slim besparen op je vaste lasten", "Gratis en eerlijk uitgelegd: besparen op je zorgverzekering, energie, internet, vakantie, auto en boodschappen. Met bronnen, vergelijkers en rekenhulpen.",
         body, [faq_ld(faq_h), {"@context": "https://schema.org", "@type": "WebSite", "name": "Bespaarvriend", "url": BASE + "/", "inLanguage": "nl-NL"}], prio="1.0")

    # ---------- Zorgverzekering 2027 ----------
    ch, cld = crumbs("Zorgverzekering 2027", "/zorgverzekering-2027/")
    faq_z = [("Hoeveel kost de zorgverzekering in 2027?", "De gemiddelde basisverzekering kost in 2027 € 173,13 per maand, € 14,83 meer dan in 2026. De laagste premie is € 148,40 per maand, de hoogste € 202,50."),
             ("Is de basisverzekering overal hetzelfde?", "Wat er in het basispakket zit, bepaalt de overheid. Dat is bij elke verzekeraar gelijk. Het verschil zit vooral in de vrije keuze van zorgverlener: bij een goedkope naturapolis krijg je bij een zorgverlener zonder contract soms minder vergoed."),
             ("Tot wanneer kan ik overstappen?", "Zeg je huidige verzekering uiterlijk 31 december 2026 op. Sluit daarna uiterlijk 31 januari 2027 een nieuwe af; die gaat met terugwerkende kracht in op 1 januari 2027. Vaak zegt je nieuwe verzekeraar de oude voor je op."),
             ("Moet ik mijn aanvullende verzekering ook opzeggen?", "Niet per se. Kijk of je de aanvullende verzekering het afgelopen jaar echt hebt gebruikt. Wie weinig naar tandarts of fysio gaat, betaalt vaak meer premie dan hij terugkrijgt."),
             ("Kan ik geweigerd worden?", "Voor de basisverzekering niet: iedere verzekeraar moet je accepteren. Voor een aanvullende verzekering mag een verzekeraar soms wel een gezondheidsverklaring vragen.")]
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["zorg"]}</span><h1>Zorgverzekering 2027: dit betaal je en zo stap je over</h1></div><p class="lead">Alle zorgverzekeringen worden duurder. Maar het verschil tussen goedkoop en duur is groter dan ooit.</p>'
            '<div class="kerncijfers"><div><b>€ 173,13</b><small>gemiddeld per maand</small></div><div><b>+ € 14,83</b><small>per maand t.o.v. 2026</small></div>'
            '<div><b>€ 148,40</b><small>laagste premie</small></div><div><b>€ 202,50</b><small>hoogste premie</small></div></div>'
            '<div class="let"><b>Verschil laagste en hoogste premie: € 649 per jaar</b>, voor dezelfde basiszorg. Met z\'n tweeën kan dat oplopen tot bijna € 1.300 per jaar.</div>'
            '<h2>Zo stap je over in 4 stappen</h2><ol class="stappen">'
            '<li><b>Kijk wat je echt gebruikt.</b> Pak je jaaroverzicht erbij: welke zorg had je, en had je die aanvullende verzekering nodig?</li>'
            '<li><b>Vergelijk de premies.</b> Gebruik een onafhankelijke vergelijker (zie hieronder). Let op: naturapolis of restitutiepolis.</li>'
            '<li><b>Sluit de nieuwe verzekering af</b> vóór 1 januari, of uiterlijk 31 januari 2027 als je vóór 31 december hebt opgezegd.</li>'
            '<li><b>Je oude verzekering wordt opgezegd.</b> Meestal doet je nieuwe verzekeraar dat voor je. Controleer het in de bevestiging.</li></ol>'
            '<h2>Naturapolis of restitutiepolis?</h2><table><tr><th></th><th>Naturapolis</th><th>Restitutiepolis</th></tr>'
            '<tr><td>Premie</td><td>Lager</td><td>Hoger</td></tr><tr><td>Zorgverlener met contract</td><td>Volledig vergoed</td><td>Volledig vergoed</td></tr>'
            '<tr><td>Zorgverlener zonder contract</td><td>Vaak deels vergoed</td><td>Meestal volledig (tot marktconform tarief)</td></tr>'
            '<tr><td>Voor wie</td><td>Wie geen vaste voorkeur heeft voor een ziekenhuis of therapeut</td><td>Wie zeker een eigen zorgverlener wil houden</td></tr></table>'
            '<h2>Zorgverzekeringen vergelijken</h2>' + ZORG_VERGELIJKER
            + partner(awin(8311, "bespaarvriend-zorg", "https://www.unitedconsumers.com/zorgverzekering"), "Zorgverzekering met collectieve korting", "Via een groot collectief krijg je korting op de premie, bij bekende verzekeraars. Handig als je al weet welke polis je wilt.", "Bekijk de collectieve korting")
            + '<h2>Meer besparen op je zorgkosten</h2><ul class="links"><li><a href="/aanvullende-verzekering-2027/">Aanvullende verzekering 2027: nodig of niet?</a></li><li><a href="/tandartsverzekering-2027/">Tandartsverzekering 2027: loont het nog?</a></li><li><a href="/eigen-risico-2027/">Eigen risico 2027: loont een vrijwillig eigen risico?</a></li><li><a href="/zorgtoeslag-2027/">Zorgtoeslag 2027: heb jij recht?</a></li></ul>'
            + faq_html(faq_z) + BRONNEN_ZORG)
    page("/zorgverzekering-2027/", "Zorgverzekering 2027: premies, verschillen en overstappen", "De zorgpremie 2027 is gemiddeld € 173,13 per maand. Laagste premie € 148,40, hoogste € 202,50: € 649 per jaar verschil. Zo stap je vóór 31 december over.",
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
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["risico"]}</span><h1>Eigen risico 2027: € 400</h1></div>' + '<p class="lead">Het verplichte eigen risico stijgt in 2027 van € 385 naar € 400. Wat betekent dat, en loont een hoger vrijwillig eigen risico?</p>'
            '<div class="kerncijfers"><div><b>€ 400</b><small>verplicht eigen risico 2027</small></div><div><b>€ 385</b><small>in 2026</small></div><div><b>+ € 500</b><small>max. vrijwillig extra</small></div><div><b>€ 900</b><small>max. totaal</small></div></div>'
            + reken +
            '<h2>Wanneer betaal je eigen risico?</h2><p>Je betaalt eigen risico voor zorg uit de basisverzekering, zoals ziekenhuiszorg, medicijnen en bloedonderzoek. '
            'Een bezoek aan de huisarts valt erbuiten, en kinderen onder de 18 hebben geen eigen risico.</p>'
            '<h2>Tip: krap bij kas? Spreid je betaling</h2><p>Weet je dat je je eigen risico toch opmaakt, bijvoorbeeld door vaste medicijnen? Bij veel verzekeraars kun je het dan in termijnen betalen. Zo krijg je geen grote rekening in één keer.</p>'
            + ZORG_VERGELIJKER + faq_html(faq_e) + BRONNEN_ZORG)
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
             '<label for="ink">Verwacht bruto jaarinkomen 2027 (samen, als je een partner hebt)</label><small class="bron" style="display:block;margin:-2px 0 6px">Bruto: vóór belasting. De Belastingdienst kijkt naar je toetsingsinkomen, voor de meeste mensen het verzamelinkomen van je aangifte. Vakantiegeld en een dertiende maand tellen mee.</small><input id="ink" type="number" inputmode="numeric" min="0" step="500" value="30000">'
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
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["toeslag"]}</span><h1>Zorgtoeslag 2027: hogere toeslag, lagere vermogensgrens</h1></div>' + '<p class="lead">De maximale zorgtoeslag gaat omhoog. Maar wie spaargeld heeft, kan zijn toeslag juist kwijtraken.</p>'
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

    # ---------- Energie 2027 ----------
    ch, cld = crumbs("Energie 2027", "/energie-2027/")
    faq_e = [("Stopt de salderingsregeling echt op 1 januari 2027?", "Ja. De salderingsregeling stopt in één keer op 1 januari 2027, ook voor lopende contracten. Teruggeleverde stroom streep je dan niet meer weg tegen je verbruik. Je krijgt er een terugleververgoeding voor: tot 2030 minimaal 50% van de kale leveringsprijs."),
             ("Wordt mijn energierekening duurder in 2027?", "Voor de meeste huishoudens wel. De netbeheerkosten stijgen volgens de prognose van de ACM met gemiddeld zo’n € 141 per jaar. De belasting op gas gaat iets omhoog, die op stroom iets omlaag. Wat je uiteindelijk betaalt, hangt vooral af van je contract."),
             ("Kan ik zomaar overstappen van energieleverancier?", "Met een variabel contract kun je altijd overstappen, met een opzegtermijn van maximaal 30 dagen en zonder boete. Bij een vast contract kan je leverancier een opzegvergoeding rekenen als je eerder stopt. Kijk daarom eerst wanneer je contract afloopt."),
             ("Vast, variabel of dynamisch: wat is het verschil?", "Bij vast staat je prijs voor de looptijd vast. Bij variabel kan de leverancier de prijs tussentijds aanpassen. Bij dynamisch betaal je per uur of kwartier de beursprijs. Wat het beste past, hangt af van hoeveel zekerheid je wilt en hoe flexibel je verbruik is.")]
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["energie"]}</span><h1>Energie 2027: dit verandert er en zo bespaar je</h1></div>'
            '<p class="lead">Op 1 januari 2027 verandert er veel op je energierekening. Met zonnepanelen nog meer. Hier lees je wat er verandert en wat je nu al kunt doen.</p>'
            '<div class="kerncijfers"><div><b>€ 0,7457</b><small>energiebelasting gas per m³ (2026: € 0,7268)</small></div>'
            '<div><b>€ 0,1065</b><small>energiebelasting stroom per kWh (2026: € 0,1108)</small></div>'
            '<div><b>€ 628,69</b><small>belastingvermindering per jaar</small></div>'
            '<div><b>+ € 141</b><small>netbeheerkosten per jaar, gemiddeld</small></div></div>'
            '<p class="bron">Belastingbedragen inclusief 21% btw, voor normaal huishoudelijk verbruik.</p>'
            '<h2>Wat verandert er op 1 januari 2027?</h2><ul class="wijzigt">'
            '<li><b>Salderen stopt</b>Teruggeleverde stroom wordt apart afgerekend. Je krijgt een terugleververgoeding van minimaal 50% van de kale stroomprijs (tot 2030). Terugleverkosten moeten per kWh op je factuur staan.</li>'
            '<li><span class="bedrag op">+ € 141</span><b>Netbeheer duurder</b>De kosten voor het transport van stroom en gas stijgen volgens de ACM-prognose fors. Dat zijn vaste kosten: elk huishouden betaalt ongeveer hetzelfde bedrag extra.</li>'
            '<li><b>Gas zwaarder belast, stroom lichter</b>De energiebelasting op gas stijgt met 2,6%, die op stroom daalt met 3,9%. Netto scheelt dat bij gemiddeld verbruik maar een paar euro.</li>'
            '<li><b>Groen gas bijmengen</b>Leveranciers moeten een deel van het gas vervangen door duurder groen gas. Die meerprijs komt in je gastarief terecht. De CO₂-heffing op gas is uitgesteld tot 2028.</li></ul>'
            f'<div class="kaart tool"><span class="ic">{ICON["zon"]}</span><div><b>Zonnepanelen? Reken het zelf uit</b><p>Met de <b>Salderingscheck</b> zie je wat het einde van salderen jou per jaar kost, en of een thuisbatterij zich terugverdient. Gratis, ook van de maker van Bespaarvriend.</p><a class="btn" href="https://salderingscheck-nl.netlify.app/">Naar de Salderingscheck{ICON["pijl"]}</a></div></div>'
            '<h2>Zo bespaar je in 4 stappen</h2><ol class="stappen">'
            '<li><b>Pak je jaarafrekening erbij.</b> Daarop staat je echte verbruik in kWh en m³. Vergelijken met een gemiddelde levert vaak een verkeerd beeld op.</li>'
            '<li><b>Kijk wanneer je contract afloopt.</b> Heb je een variabel contract, dan kun je altijd overstappen. Bij een vast contract kan eerder stoppen geld kosten.</li>'
            '<li><b>Vergelijk op de tarieven vanaf 2027.</b> Heb je zonnepanelen? Let dan vooral op de terugleververgoeding en de terugleverkosten vanaf 1 januari, niet alleen op de prijs per kWh.</li>'
            '<li><b>Verbruik slim.</b> Met zonnepanelen loont het om stroom te gebruiken als de zon schijnt: wasmachine, vaatwasser of auto opladen overdag.</li></ol>'
            + widget("energie", "Energie vergelijken") + partner(awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/energievergelijken"), "Energiecontracten vergelijken", "Vergelijk contracten van alle grote leveranciers, inclusief de tarieven en terugleververgoeding vanaf 2027.", "Vergelijk energiecontracten", [("3 jaar vast", awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/energievergelijken/energiecontract-3-jaar-vast")), ("Dynamisch contract", awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/energievergelijken/dynamisch-energiecontract-vergelijken")), ("Aanbiedingen", awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/energievergelijken/energie-aanbiedingen")), ("Zonnepanelen en 2027", awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/zonnepanelen/afschaffen-salderingsregeling"))]) +
            '<h2>Vast, variabel of dynamisch?</h2><table><tr><th>Contract</th><th>Prijs</th><th>Past bij</th></tr>'
            '<tr><td><b>Vast</b></td><td>Staat vast voor 1, 2 of 3 jaar</td><td>Wie zekerheid wil over het maandbedrag</td></tr>'
            '<tr><td><b>Variabel</b></td><td>Kan tussentijds wijzigen</td><td>Wie flexibel wil blijven en wil kunnen overstappen</td></tr>'
            '<tr><td><b>Dynamisch</b></td><td>Beursprijs per uur of kwartier</td><td>Wie verbruik kan verschuiven, zoals met een thuisbatterij of elektrische auto</td></tr></table>'
            '<p class="bron">Stroom en gas hoeven niet bij dezelfde leverancier. Een vast gascontract naast een dynamisch stroomcontract kan ook.</p>'
            + faq_html(faq_e) +
            '<p class="bron">Bronnen: <a href="https://www.overstappen.nl/nieuws/gasbelasting-stijgt-stroombelasting-daalt-energierekening-euro-180-hoger-in-2027/" rel="noopener">Overstappen.nl (energiebelasting 2027)</a>, '
            '<a href="https://www.energievergelijk.nl/nieuws/meer-belasting-op-gas-minder-op-stroom-energierekening-stijgt-in-2027" rel="noopener">Energievergelijk.nl</a>, '
            '<a href="https://www.overstappen.nl/nieuws/prinsjesdag-2026-dit-zijn-de-gevolgen-voor-je-energierekening/" rel="noopener">Overstappen.nl (netbeheerkosten, ACM-prognose)</a>, '
            '<a href="https://selectra.nl/energie/zonnepanelen/salderingsregeling" rel="noopener">Selectra (einde salderen)</a>, '
            '<a href="https://solarmagazine.nl/nieuws-zonne-energie/i44687/eigenaren-zonnepanelen-weten-eindelijk-waar-ze-aan-toe-zijn-terugleverkosten-moeten-vanaf-2027-per-kilowattuur-op-factuur" rel="noopener">Solar Magazine (terugleverkosten)</a>. '
            f'Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/energie-2027/", "Energie 2027: einde salderen, energiebelasting en besparen", "Wat verandert er op je energierekening in 2027? Einde salderingsregeling, energiebelasting gas € 0,7457 en stroom € 0,1065, netbeheer + € 141. Zo bespaar je.",
         body, [cld, faq_ld(faq_e)], prio="0.9")

    # ---------- Internet en mobiel ----------
    ch, cld = crumbs("Internet en mobiel", "/internet-en-mobiel/")
    faq_i = [("Wanneer kan ik mijn internetabonnement opzeggen?", "Na de vaste looptijd (meestal 1 of 2 jaar) mag je altijd kosteloos opzeggen. De opzegtermijn is dan maximaal één maand en gaat in op de dag dat je opzegt."),
             ("Moet ik zelf mijn oude abonnement opzeggen?", "Meestal niet. Bij internet regelt de overstapservice van je nieuwe provider de opzegging. Bij mobiel zegt je nieuwe provider je oude abonnement op als je nummerbehoud aanvraagt."),
             ("Houd ik mijn 06-nummer als ik overstap?", "Ja. Vraag bij je nieuwe provider nummerbehoud aan. Overstappen duurt meestal 5 tot 10 werkdagen en is gratis."),
             ("Is een telefoon met abonnement goedkoper?", "Meestal niet. Een toestel los kopen en een sim only nemen is vaak honderden euro’s goedkoper over twee jaar. Reken altijd met de gemiddelde maandprijs over de hele looptijd, niet met de actieprijs van de eerste maanden.")]
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["internet"]}</span><h1>Internet en mobiel: stop met te veel betalen</h1></div>'
            '<p class="lead">Na je contractperiode loopt je abonnement gewoon door, vaak tegen een hogere prijs dan nieuwe klanten betalen. Overstappen is makkelijker dan je denkt.</p>'
            '<div class="kerncijfers"><div><b>79%</b><small>van de internetabonnementen loopt al na de contractperiode door</small></div>'
            '<div><b>± 5 mln</b><small>huishoudens laten geld liggen met een slapend contract</small></div>'
            '<div><b>1 maand</b><small>maximale opzegtermijn na je contract</small></div>'
            '<div><b>€ 7,50</b><small>sim only met 10 GB kan al voor ongeveer dit per maand</small></div></div>'
            '<h2>Internet thuis</h2><ol class="stappen">'
            '<li><b>Zoek je einddatum op.</b> In je account of op je factuur staat wanneer je minimale looptijd afloopt. Daarna ben je maandelijks opzegbaar.</li>'
            '<li><b>Check welke snelheid je echt nodig hebt.</b> Voor streamen en thuiswerken met een paar mensen is vaak een lager pakket genoeg.</li>'
            '<li><b>Vraag je huidige provider om een beter aanbod.</b> Wie belt en zegt te willen overstappen, krijgt vaak een lagere prijs aangeboden.</li>'
            '<li><b>Stap over met de overstapservice.</b> Je nieuwe provider zegt je oude abonnement voor je op. Je kunt dit tot vier maanden voor het einde van je contract al regelen.</li></ol>'
            + widget("telecom", "Internet vergelijken") +
            partner(awin(8311, "bespaarvriend-internet", "https://www.unitedconsumers.com/internet-en-tv"), "Internet en tv met korting", "Een internet- en tv-abonnement met extra korting via een collectief, bij de bekende providers.", "Bekijk internet en tv", [("Alleen internet", awin(8311, "bespaarvriend-internet", "https://www.unitedconsumers.com/internet-en-tv/internet")), ("Internet en tv", awin(8311, "bespaarvriend-internet", "https://www.unitedconsumers.com/internet-en-tv/televisie"))]) +
            partner(awin(120541, "bespaarvriend-internet"), "Snellere wifi in huis", "Trage wifi ligt vaak aan je router, niet aan je abonnement. Een nieuwe router of mesh-systeem helpt vaak beter dan een duurder abonnement.", "Bekijk routers en mesh-wifi") +
            f'<h2>Mobiel</h2><div class="paginakop" style="margin-top:0"><span class="ic">{ICON["mobiel"]}</span><p style="margin:0">Werkt je telefoon nog goed? Dan is sim only bijna altijd de goedkoopste keuze.</p></div>'
            '<div class="let"><b>Rekenvoorbeeld:</b> een nieuw-toestel-abonnement van € 45 per maand kost in 2 jaar € 1.080. Een refurbished toestel van € 350 plus 24 maanden sim only van € 8 kost € 542. Dat scheelt € 538.</div>'
            + partner(awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/"), "Refurbished telefoon met garantie", "Gebruikte telefoons, gecontroleerd en schoongemaakt, met garantie.", "Bekijk refurbished telefoons", [("iPhone 13", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/iphone-13")), ("iPhone 14", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/iphone-14")), ("iPhone 15", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/iphone-15")), ("Samsung", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/samsung")), ("iPad", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/ipad"))]) +
            '<ul class="links"><li>Kijk in je account hoeveel data je echt gebruikt. Veel mensen betalen voor een bundel die ze niet halen.</li>'
            '<li>Maandelijks opzegbaar kost vaak € 1 tot € 4 per maand meer dan een jaarcontract.</li>'
            '<li>Reken met de gemiddelde prijs over de hele looptijd, niet met de actieprijs.</li></ul>'
            + widget("simonly", "Sim only vergelijken")
            + partner(awin(8311, "bespaarvriend-mobiel", "https://www.unitedconsumers.com/mobiel"), "Sim only met een duidelijke maandprijs", "Sim only zonder kleine lettertjes: één vaste prijs per maand, maandelijks opzegbaar.", "Bekijk sim only")
            + faq_html(faq_i) +
            '<p class="bron">Bronnen: <a href="https://www.acm.nl/nl/publicaties/acm-telecomaanbieders-moeten-consumenten-duidelijker-en-transparanter-voorlichten-over-vast-internet" rel="noopener">ACM (vast internet)</a>, '
            '<a href="https://nos.nl/l/2601599" rel="noopener">NOS</a>, '
            '<a href="https://www.overstappen.nl/internet/opzeggen/" rel="noopener">Overstappen.nl (opzeggen)</a>, '
            '<a href="https://www.providers.nl/mobiel/mobiel-abonnement/" rel="noopener">Providers.nl (rekenvoorbeeld)</a>, '
            '<a href="https://www.keuze.nl/sim-only/goedkoopste" rel="noopener">Keuze.nl (sim only-prijzen)</a>. '
            f'Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/internet-en-mobiel/", "Internet en mobiel: opzeggen, overstappen en besparen", "79% van de internetabonnementen loopt na de contractperiode door, vaak te duur. Zo zeg je op, stap je over en bespaar je met sim only.",
         body, [cld, faq_ld(faq_i)], prio="0.9")

    # ---------- Vakantie en vliegen ----------
    def tool(url, ic, naam, tekst):
        return f'<a class="kaart tool" href="{url}" style="text-decoration:none;color:inherit;margin:0"><span class="ic">{ICON[ic]}</span><span><b>{naam}</b><p style="margin:4px 0 0">{tekst}</p></span></a>'
    LANDEN = [("Spanje", "spanje"), ("Frankrijk", "frankrijk"), ("Italië", "italie"), ("Portugal", "portugal"), ("Griekenland", "griekenland"), ("Kroatië", "kroatie"), ("Oostenrijk", "oostenrijk")]
    ESIM = [("Turkije", "turkey"), ("Zwitserland", "switzerland"), ("Engeland", "united-kingdom"), ("Egypte", "egypt"), ("Marokko", "morocco")]
    ch, cld = crumbs("Vakantie en vliegen", "/vakantie-en-vliegen/")
    faq_v = [("Wanneer is op vakantie gaan het goedkoopst?", "Buiten de schoolvakanties. Dan zijn vluchten, pakketreizen, vakantieparken en campings meestal een stuk goedkoper. Ben je aan schoolvakanties gebonden, boek dan vroeg en vergelijk ook vertrek vanaf een ander vliegveld."),
             ("Is een pakketreis goedkoper dan los boeken?", "Soms wel, soms niet. Reken vlucht en hotel ook los uit en vergelijk de totaalprijs, inclusief bagage, transfers en toeristenbelasting. Een pakketreis geeft wel extra zekerheid als er iets misgaat."),
             ("Kan ik in het buitenland mijn eigen bundel gebruiken?", "In de EU, Noorwegen, IJsland en Liechtenstein bel en internet je tegen dezelfde voorwaarden als thuis. Buiten die landen, zoals in Zwitserland, Turkije of Engeland, kan het flink duurder zijn. Kijk vooraf wat je provider rekent of neem een eSIM met data."),
             ("Waarom een huurauto met alle verzekeringen?", "Bij een goedkope huurauto zit vaak een hoog eigen risico. Aan de balie wordt dan een dure extra verzekering aangeboden. Een huurprijs waarin de verzekeringen al zitten, is achteraf vaak goedkoper en geeft geen verrassingen.")]
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["vlucht"]}</span><h1>Goedkoper op vakantie en vliegen</h1></div>'
            '<p class="lead">Een vakantie is voor veel mensen de grootste uitgave van het jaar. Met slim vergelijken, flexibele data en een paar trucs houd je meer over.</p>'
            '<h2>Vergelijk met je eigen apps</h2><div class="tegels" style="grid-template-columns:1fr">'
            + tool("https://vluchtwijzer.netlify.app/", "vlucht", "Vluchtwijzer", "Vul je reis één keer in en zie direct waar je de goedkoopste vlucht vindt, ook vanaf vliegvelden over de grens.")
            + tool("https://vakantietoppers.netlify.app/", "koffer", "Vakantiewijzer", "Pakketreizen, hotels, vakantieparken en campings vergelijken in één keer.")
            + tool("https://euroroadrules.eu/", "weg", "EuroRoadRules", "Met de auto op vakantie? Vignetten, tol en milieuzones per land.")
            + '</div>'
            '<h2>Zo bespaar je op je vakantie</h2><ol class="stappen">'
            '<li><b>Reis buiten de schoolvakanties</b> als dat kan. Dat scheelt vaak het meest.</li>'
            '<li><b>Vergelijk totaalprijzen.</b> Tel bagage, stoelreservering, transfers en toeristenbelasting mee. Een lage advertentieprijs is niet altijd de goedkoopste reis.</li>'
            '<li><b>Kijk ook naar andere vliegvelden.</b> Vanaf Weeze, Düsseldorf of Brussel is dezelfde bestemming soms goedkoper.</li>'
            '<li><b>Reken vlucht en hotel ook los uit.</b> Soms is dat goedkoper dan een pakketreis.</li>'
            '<li><b>Huur een auto met alle verzekeringen erbij.</b> Dan betaal je aan de balie niets extra.</li>'
            '<li><b>Regel mobiel internet vooraf</b> als je buiten de EU reist.</li></ol>'
            + widget("vakantie", "Actuele vakantie-aanbiedingen")
            + partner(awin(63484, "bespaarvriend-vakantie", "https://www.vliegwinkel.nl/"), "Vliegtickets boeken", "Vluchten van meer dan 800 luchtvaartmaatschappijen naar bestemmingen over de hele wereld, ook als vlucht + hotel. Let op bagage en boekingskosten voordat je betaalt.", "Bekijk vliegtickets")
            + partner(awin(128671, "bespaarvriend-vakantie"), "Huurauto inclusief verzekering", "Een huurauto waarbij alle verzekeringen al in de prijs zitten. Kies het land van je vakantie.", "Bekijk huurauto's",
                      [(n, awin(128671, "bespaarvriend-vakantie", f"https://www.sunnycars.nl/auto-huren/{sl}/")) for n, sl in LANDEN])
            + partner(awin(128623, "bespaarvriend-vakantie"), "eSIM voor buiten de EU", "Mobiel internet zonder dure roaming. Je zet de eSIM vooraf op je telefoon en hebt direct data bij aankomst.", "Bekijk eSIM's",
                      [(n, awin(128623, "bespaarvriend-vakantie", f"https://saily.com/nl/esim-{sl}/")) for n, sl in ESIM])
            + partner(awin(78144, "bespaarvriend-vakantie", "https://www.hansemerkur.nl/reisverzekeringen"), "Reisverzekering", "Een reisverzekering voor één reis of het hele jaar, ook voor wintersport en lange reizen.", "Bekijk reisverzekeringen", [("Doorlopend", awin(78144, "bespaarvriend-vakantie", "https://www.hansemerkur.nl/reisverzekeringen/doorlopende-reisverzekering")), ("Eén reis", awin(78144, "bespaarvriend-vakantie", "https://www.hansemerkur.nl/reisverzekeringen/kortlopende-reisverzekering")), ("Wintersport", awin(78144, "bespaarvriend-vakantie", "https://www.hansemerkur.nl/reisverzekeringen/wintersportverzekering")), ("Lang op reis", awin(78144, "bespaarvriend-vakantie", "https://www.hansemerkur.nl/lang-op-reisverzekeringen"))])
            + faq_html(faq_v) +
            '<p class="bron">Bronnen: <a href="https://europa.eu/youreurope/citizens/consumers/internet-telecoms/mobile-roaming-costs/index_nl.htm" rel="noopener">Your Europe (roamen in de EU)</a>, '
            '<a href="https://vakantietoppers.netlify.app/gids/goedkoop-op-vakantie-tips.html" rel="noopener">Vakantiewijzer: 10 tips</a>. '
            f'Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/vakantie-en-vliegen/", "Goedkoper op vakantie en vliegen: tips en vergelijkers", "Zo ga je goedkoper op vakantie: buiten de schoolvakanties, totaalprijzen vergelijken, vertrekken vanaf een ander vliegveld en een huurauto met alle verzekeringen.",
         body, [cld, faq_ld(faq_v)], prio="0.8")

    # ---------- Auto en tanken ----------
    def banden_abm(w, h, d, s): return awin(8671, "bespaarvriend-auto", f"https://www.autobandenmarkt.nl/search?vehicleTypes=PKW&width={w}&profile={h}&size={d}&season={s}&type=tyre")
    def banden_bnl(w, h, d, s): return awin(12717, "bespaarvriend-auto", f"https://www.banden.nl/banden/auto/{s}/{w}-{h}-{d}/200+201+202")
    ch, cld = crumbs("Auto en tanken", "/auto-en-tanken/")
    faq_a = [("Is tanken in België of Duitsland goedkoper?", "Vaak wel. Benzine en diesel zijn in België en Duitsland meestal goedkoper dan in Nederland. Of omrijden loont, hangt af van hoeveel je tankt en hoe ver je moet rijden. Tankwijzer rekent het voor je uit."),
             ("Scheelt de bandenspanning echt brandstof?", "Ja. Met te zachte banden rij je minder zuinig en slijten je banden sneller. Controleer de spanning ongeveer eens per maand; de juiste waarde staat in het instructieboekje of in de deurstijl."),
             ("Zomer-, winter- of all-seasonbanden?", "In Nederland zijn winterbanden niet verplicht. Met all-seasonbanden hoef je niet twee keer per jaar te wisselen. Rijd je veel in Duitsland of de Alpen in de winter, kijk dan naar de regels per land."),
             ("Wat betekent een storingslampje?", "Een brandend lampje of een foutcode betekent niet altijd een dure reparatie. Zoek de code eerst op, zodat je weet wat er aan de hand is voordat je naar de garage gaat.")]
    MATEN = [("205/55 R16", 205, 55, 16), ("195/65 R15", 195, 65, 15), ("225/45 R17", 225, 45, 17), ("215/55 R17", 215, 55, 17)]
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["tank"]}</span><h1>Besparen op je auto en tanken</h1></div>'
            '<p class="lead">Brandstof, banden en onderhoud: met een paar slimme keuzes rijd je voor minder geld.</p>'
            '<h2>Je eigen hulpmiddelen</h2><div class="tegels" style="grid-template-columns:1fr">'
            + tool("https://goedkopertanken.netlify.app/", "tank", "Tankwijzer", "Live brandstofprijzen in Nederland, België en Duitsland, en of omrijden voor jou loont.")
            + tool("https://foutcodezoeker.nl/", "sleutel", "Foutcodezoeker", "Zoek foutcodes en storingen op voordat je naar de garage gaat.")
            + tool("https://euroroadrules.eu/", "weg", "EuroRoadRules", "Vignetten, tol en milieuzones in heel Europa.")
            + '</div>'
            '<h2>Zo bespaar je op je auto</h2><ol class="stappen">'
            '<li><b>Vergelijk brandstofprijzen.</b> Het verschil tussen tankstations kan flink oplopen, zeker langs de snelweg.</li>'
            '<li><b>Tank over de grens</b> als je toch in de buurt bent.</li>'
            '<li><b>Houd je banden op spanning.</b> Dat is zuiniger en je banden gaan langer mee.</li>'
            '<li><b>Rijd rustig.</b> Op tijd opschakelen en gelijkmatig rijden scheelt brandstof.</li>'
            '<li><b>Vergelijk bandenprijzen</b> voordat je bij de garage nieuwe banden laat zetten.</li></ol>'
            + partner(banden_abm(205, 55, 16, "so"), "Banden kopen", "Kies je bandenmaat en zie direct de prijzen. De maat staat op de zijkant van je band, bijvoorbeeld 205/55 R16.", "Bekijk banden",
                      [(f"{n} zomer", banden_abm(w, h, d, "so")) for n, w, h, d in MATEN] + [("205/55 R16 winter", banden_abm(205, 55, 16, "wi")), ("205/55 R16 all-season", banden_abm(205, 55, 16, "gan"))])
            + partner(banden_bnl(205, 55, 16, "zomer-banden"), "Banden vergelijken", "Vergelijk banden van verschillende winkels, ook met montage bij je in de buurt.", "Vergelijk banden",
                      [(f"{n} zomer", banden_bnl(w, h, d, "zomer-banden")) for n, w, h, d in MATEN] + [("205/55 R16 all-season", banden_bnl(205, 55, 16, "all-season-banden"))])
            + partner(awin(8311, "bespaarvriend-auto", "https://www.unitedconsumers.com/autoverzekering"), "Autoverzekering met korting", "Een autoverzekering met collectieve korting op de premie. Vul je kenteken in en zie direct wat je betaalt.", "Bereken je premie")
            + partner(awin(8311, "bespaarvriend-auto", "https://www.unitedconsumers.com/tanken"), "Korting op elke tankbeurt", "Met een tankpas van een collectief krijg je korting per liter bij veel tankstations in Nederland.", "Bekijk de tankkorting")
            + faq_html(faq_a) +
            f'<p class="bron">Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/auto-en-tanken/", "Besparen op je auto: goedkoper tanken en banden", "Zo bespaar je op je auto: brandstofprijzen vergelijken, tanken over de grens, banden op spanning en bandenprijzen vergelijken.",
         body, [cld, faq_ld(faq_a)], prio="0.8")

    # ---------- Boodschappen ----------
    ch, cld = crumbs("Boodschappen", "/boodschappen/")
    faq_b = [("Welke supermarkt is het goedkoopst?", "Dat verschilt per product en per week. Vergelijk daarom de producten die jij echt koopt. Goedkope Boodschappen laat per product zien waar het het goedkoopst is."),
             ("Zijn huismerken echt goedkoper?", "Meestal wel, en vaak is de kwaliteit vergelijkbaar. Probeer bij producten die je vaak koopt eens het huismerk."),
             ("Helpt een boodschappenlijstje?", "Ja. Met een lijstje en een weekmenu koop je minder op impuls en gooi je minder weg.")]
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["boodschappen"]}</span><h1>Besparen op je boodschappen</h1></div>'
            '<p class="lead">Boodschappen zijn een van de grootste vaste uitgaven. Met vergelijken en een beetje planning houd je elke maand geld over.</p>'
            '<h2>Je eigen hulpmiddelen</h2><div class="tegels" style="grid-template-columns:1fr">'
            + tool("https://boodschappenvergelijk.nl/", "boodschappen", "Goedkope Boodschappen", "Vergelijk de prijzen van 12 supermarkten per product.")
            + tool("https://bonnenboek.netlify.app/", "bon", "Bonnenboek", "Scan je kassabonnen en zie per maand waar je geld naartoe gaat.")
            + '</div>'
            '<h2>Zo bespaar je op je boodschappen</h2><ol class="stappen">'
            '<li><b>Maak een weekmenu en een lijstje.</b> Je koopt minder op impuls en gooit minder weg.</li>'
            '<li><b>Vergelijk de producten die je echt koopt.</b> De goedkoopste supermarkt verschilt per product.</li>'
            '<li><b>Kies vaker het huismerk.</b></li>'
            '<li><b>Koop aanbiedingen alleen als je het toch nodig hebt.</b> Twee halen, één betalen is geen besparing als je het weggooit.</li>'
            '<li><b>Houd bij wat je uitgeeft.</b> Wie het ziet, geeft vaak vanzelf minder uit.</li></ol>'
            + partner(awin(82075, "bespaarvriend-boodschappen"), "Boodschappenbox van de boer", "Verse producten van Nederlandse boeren, thuisbezorgd.", "Bekijk de boxen",
                      [("Kies je box", awin(82075, "bespaarvriend-boodschappen", "https://www.boerschappen.nl/kies-je-box/")), ("Maaltijdboxen", awin(82075, "bespaarvriend-boodschappen", "https://www.boerschappen.nl/maaltijdboxen/")), ("Specials", awin(82075, "bespaarvriend-boodschappen", "https://www.boerschappen.nl/specials/"))])
            + partner(awin(8591, "bespaarvriend-boodschappen"), "Maaltijdbox", "Precies genoeg ingrediënten voor je recepten, dus minder weggooien.", "Bekijk de maaltijdbox",
                      [("Menu van deze week", awin(8591, "bespaarvriend-boodschappen", "https://marleyspoon.nl/menu")), ("Kies je plan", awin(8591, "bespaarvriend-boodschappen", "https://marleyspoon.nl/select-plan"))])
            + faq_html(faq_b) + f'<p class="bron">Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/boodschappen/", "Besparen op boodschappen: vergelijken en bijhouden", "Zo bespaar je op je boodschappen: weekmenu, prijzen per product vergelijken, huismerken en bijhouden wat je uitgeeft.",
         body, [cld, faq_ld(faq_b)], prio="0.8")

    # ---------- Administratie ----------
    ch, cld = crumbs("Administratie", "/administratie/")
    faq_d = [("Hoe vaak moet ik mijn vaste lasten nalopen?", "Minstens één keer per jaar. Een goed moment is het einde van het jaar, als je ook je zorgverzekering kunt vergelijken."),
             ("Welke abonnementen vergeten mensen vaak?", "Streamingdiensten, sportscholen, apps en tijdschriften die je niet meer gebruikt. Kijk je bankafschriften van de afgelopen drie maanden door op terugkerende afschrijvingen."),
             ("Moet ik toeslagen zelf aanvragen?", "Ja. Toeslagen krijg je niet vanzelf. Check elk jaar of je recht hebt, bijvoorbeeld op zorgtoeslag, en geef wijzigingen in je inkomen op tijd door.")]
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["map"]}</span><h1>Je vaste lasten en administratie op orde</h1></div>'
            '<p class="lead">Wie weet wat er elke maand afgaat, ziet ook waar het goedkoper kan. Zo krijg je in een uurtje overzicht.</p>'
            '<h2>Je eigen hulpmiddelen</h2><div class="tegels" style="grid-template-columns:1fr">'
            + tool("https://allesoporde.netlify.app/", "map", "Alles op orde", "Al je vaste lasten en inkomsten op een rij, met einddata van contracten.")
            + tool("https://salderingscheck-nl.netlify.app/", "zon", "Salderingscheck", "Zonnepanelen? Reken uit wat het einde van salderen in 2027 jou kost.")
            + tool("https://bonnenboek.netlify.app/", "bon", "Bonnenboek", "Je boodschappen en tankbeurten bijhouden met een foto van de bon.")
            + '</div>'
            '<h2>In 5 stappen overzicht</h2><ol class="stappen">'
            '<li><b>Zet al je vaste lasten op een rij.</b> Huur of hypotheek, energie, zorg, internet, mobiel, verzekeringen en abonnementen.</li>'
            '<li><b>Zoek de einddatum van elk contract op.</b> Na de looptijd kun je vaak maandelijks opzeggen en overstappen.</li>'
            '<li><b>Zeg op wat je niet gebruikt.</b> Kijk je bankafschriften door op terugkerende afschrijvingen.</li>'
            '<li><b>Vergelijk de grote posten.</b> Begin met <a href="/zorgverzekering-2027/">zorg</a>, <a href="/energie-2027/">energie</a> en <a href="/internet-en-mobiel/">internet en mobiel</a>.</li>'
            '<li><b>Check je toeslagen.</b> Bijvoorbeeld met de <a href="/zorgtoeslag-2027/">zorgtoeslag-check</a>.</li></ol>'
            + partner(awin(8520, "bespaarvriend-administratie", "https://www.gaslicht.com/energievergelijken"), "Energiecontract vergelijken", "Loopt je energiecontract af? Vergelijk de tarieven van alle grote leveranciers.", "Vergelijk energiecontracten")
            + faq_html(faq_d) + f'<p class="bron">Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/administratie/", "Vaste lasten op orde: in 5 stappen overzicht", "Zo krijg je overzicht in je vaste lasten: alles op een rij, einddata van contracten, abonnementen opzeggen, grote posten vergelijken en toeslagen checken.",
         body, [cld, faq_ld(faq_d)], prio="0.7")

    # ---------- Privacy ----------
    ch, cld = crumbs("Privacy", "/privacy/")
    body = (ch + '<h1>Privacy</h1><div class="kaart"><p style="margin-top:0">Bespaarvriend gebruikt geen cookies en geen trackers die je volgen. Sommige pagina’s hebben partnerlinks; die staan altijd als advertentie gemarkeerd.</p>'
            '<p>De rekenhulpen werken helemaal in je eigen browser: wat je invult, wordt nergens naartoe gestuurd of bewaard.</p>'
            '<p>Stuur je een bericht via de contactpagina, dan bewaren we je bericht (en je naam en e-mailadres als je die invult) alleen om je te kunnen antwoorden. '
            'We delen het met niemand en verwijderen het als het niet meer nodig is.</p><p style="margin-bottom:0">De site draait bij Netlify. Netlify houdt voor de beveiliging korte tijd technische gegevens bij, zoals IP-adressen.</p></div>')
    page("/privacy/", "Privacy | Bespaarvriend", "Bespaarvriend gebruikt geen cookies en geen trackers. Rekenhulpen werken in je eigen browser.", body, [cld], prio="0.2")

    # ---------- Contact (Netlify Forms, geen e-mailadres op de site) ----------
    ch, cld = crumbs("Contact", "/contact/")
    body = (ch + '<h1>Contact</h1><p class="lead">Een vraag, een fout gezien of een tip? Laat het weten.</p>'
            '<div class="let"><b>Let op:</b> Bespaarvriend heeft geen vergunning voor financieel advies. Vragen over je persoonlijke situatie of over specifieke verzekeringen en financiële producten kunnen en mogen we niet beantwoorden. Daarvoor kun je terecht bij je verzekeraar of een erkend adviseur.</div>'
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

    # ---------- Aanvullende verzekering 2027 ----------
    ch, cld = crumbs("Aanvullende verzekering 2027", "/aanvullende-verzekering-2027/")
    faq_a = [("Is een aanvullende verzekering verplicht?", "Nee. Alleen de basisverzekering is verplicht. Een aanvullende verzekering kies je zelf, voor zorg die niet of maar deels in het basispakket zit, zoals fysiotherapie, tandarts of een bril."),
             ("Wanneer zijn de premies van de aanvullende verzekering 2027 bekend?", "Zorgverzekeraars maken de premies van de aanvullende verzekeringen uiterlijk 19 november bekend, een week na de premies van de basisverzekering."),
             ("Moet mijn aanvullende verzekering bij dezelfde verzekeraar als mijn basisverzekering?", "Meestal wel. Bij veel verzekeraars kun je een aanvullende verzekering alleen afsluiten in combinatie met hun eigen basisverzekering. Kijk dus naar de totaalprijs van basis plus aanvullend."),
             ("Kan een verzekeraar mij weigeren voor een aanvullende verzekering?", "Voor de basisverzekering niet. Voor een aanvullende verzekering mag een verzekeraar soms een gezondheidsverklaring vragen of je weigeren, vooral bij uitgebreide pakketten."),
             ("Tot wanneer kan ik overstappen?", "Zeg je huidige verzekering uiterlijk 31 december 2026 op. Je hebt daarna tot en met 31 januari 2027 om een nieuwe af te sluiten; die gaat in per 1 januari 2027.")]
    reken_a = ('<div class="kaart reken" id="rekenhulp"><h2 style="margin-top:0">Rekenhulp: verdien je je aanvullende verzekering terug?</h2>'
               '<label for="ap">Premie aanvullende verzekering per maand</label><input id="ap" type="number" inputmode="decimal" min="0" step="0.5" value="25">'
               '<label for="ak">Wat kreeg je vorig jaar vergoed uit je aanvullende verzekering? (zie je jaaroverzicht)</label><input id="ak" type="number" inputmode="decimal" min="0" step="10" value="150">'
               '<div class="uit" id="auit" role="status" aria-live="polite"></div>'
               '<p class="bron">Je jaaroverzicht staat in de app of op de site van je zorgverzekeraar. Dit is een indicatie, geen advies.</p></div>'
               """<script>
(function(){var p=document.getElementById('ap'),k=document.getElementById('ak'),u=document.getElementById('auit');
function n(x){return Math.max(0,parseFloat(String(x.value).replace(',','.'))||0)}
function eur(x){return '€ '+Math.round(x).toLocaleString('nl-NL')}
function r(){var jaar=n(p)*12,terug=n(k),s=terug-jaar;
u.textContent='Je betaalt '+eur(jaar)+' per jaar aan premie. '+(s>=0?('Je kreeg '+eur(s)+' meer terug dan je betaalde: het pakket leverde je vorig jaar geld op.'):('Je betaalde '+eur(-s)+' meer dan je terugkreeg. Kijk of een kleiner pakket of geen aanvullende verzekering beter past.'))}
p.addEventListener('input',r);k.addEventListener('input',r);r()})();
</script>""")
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["zorg"]}</span><h1>Aanvullende verzekering 2027: heb je het echt nodig?</h1></div>'
            '<p class="lead">Ruim 80% van de Nederlanders heeft een aanvullende verzekering. Toch betalen veel mensen voor zorg die ze nooit gebruiken.</p>'
            '<div class="let"><b>Premies 2027 bekend uiterlijk 19 november.</b> Daarna kun je basis en aanvullend samen vergelijken. Overstappen kan tot 31 december.</div>'
            + reken_a +
            '<h2>Wanneer is een aanvullende verzekering zinvol?</h2><ul class="links">'
            '<li><b>Je gaat regelmatig naar de fysiotherapeut.</b> Eén behandeling kost al snel meer dan een maand premie.</li>'
            '<li><b>Je kind krijgt een beugel.</b> Orthodontie voor kinderen zit niet in de basisverzekering.</li>'
            '<li><b>Je verwacht een dure behandeling</b>, zoals een kroon of implantaat. Vraag dan eerst een begroting.</li></ul>'
            '<h2>Wanneer kun je zonder?</h2><p>Ben je gezond, verwacht je weinig zorgkosten en heb je een buffer voor onverwachte rekeningen? Dan is een aanvullende verzekering vaak duurder dan wat je terugkrijgt. '
            'Bij voorspelbare kosten, zoals een jaarlijkse tandartscontrole, is een pakket eigenlijk een manier van gespreid betalen: je krijgt een deel van je eigen premie terug.</p>'
            '<h2>Zo kies je in 4 stappen</h2><ol class="stappen">'
            '<li><b>Pak je jaaroverzicht erbij.</b> Wat kreeg je vorig jaar vergoed, en waarvoor?</li>'
            '<li><b>Schrap wat je niet gebruikt.</b> Brillen, alternatieve zorg of extra fysio: alleen houden als je het echt nodig hebt.</li>'
            '<li><b>Vergelijk de totaalprijs.</b> Basis plus aanvullend, want je kunt ze meestal niet los bij verschillende verzekeraars nemen.</li>'
            '<li><b>Let op wachttijden en gezondheidsverklaringen</b> bij uitgebreide pakketten.</li></ol>'
            + ZORG_VERGELIJKER +
            '<h2>Meer over je zorgkosten</h2><ul class="links"><li><a href="/tandartsverzekering-2027/">Tandartsverzekering 2027: loont het nog?</a></li><li><a href="/zorgverzekering-2027/">Zorgverzekering 2027: premies en overstappen</a></li><li><a href="/eigen-risico-2027/">Eigen risico 2027</a></li><li><a href="/zorgtoeslag-2027/">Zorgtoeslag 2027</a></li></ul>'
            + faq_html(faq_a) +
            '<p class="bron">Bronnen: <a href="https://www.zorgwijzer.nl/zorgverzekering-2027/zoveel-duurder-wordt-je-zorgverzekering-in-2027-de-optelsom" rel="noopener">Zorgwijzer (aanvullende verzekering 2027)</a>, '
            '<a href="https://www.rabobank.nl/particulieren/verzekering/zorgverzekering/tips-voor-je-zorgverzekering" rel="noopener">Rabobank (premies aanvullend uiterlijk 19 november)</a>, '
            '<a href="https://www.overstappen.nl/nieuws/tandarts-3-procent-duurder-in-2027-102-van-de-110-tandpakketten-loont-met-deze-kosten-niet/" rel="noopener">Overstappen.nl</a>. '
            f'Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/aanvullende-verzekering-2027/", "Aanvullende verzekering 2027: nodig of niet? Met rekenhulp", "Heb je een aanvullende zorgverzekering echt nodig in 2027? Reken uit of je je premie terugverdient, en lees wanneer je beter zonder kunt.",
         body, [cld, faq_ld(faq_a)], prio="0.9")

    # ---------- Tandartsverzekering 2027 ----------
    ch, cld = crumbs("Tandartsverzekering 2027", "/tandartsverzekering-2027/")
    faq_t = [("Zit de tandarts in de basisverzekering?", "Voor kinderen tot 18 jaar wordt de meeste tandartszorg vergoed, maar niet bijvoorbeeld orthodontie, kronen en bruggen. Voor volwassenen vergoedt de basisverzekering alleen enkele dingen, zoals chirurgische tandheelkunde, röntgenonderzoek en een uitneembaar kunstgebit. Controles en vullingen betaal je zelf of via een tandartsverzekering."),
             ("Loont een tandartsverzekering in 2027?", "Bij een gezond gebit meestal niet. Uit onderzoek van Overstappen.nl blijkt dat bij 102 van de 110 tandpakketten de premie hoger is dan de vergoeding als je gemiddelde tandartskosten hebt (ongeveer € 175 per jaar)."),
             ("Wordt de tandarts duurder in 2027?", "Ja. De tandartstarieven stijgen in 2027 met ongeveer 3%. De maximale vergoedingen van de meeste tandpakketten blijven gelijk."),
             ("Wat als ik een grote behandeling verwacht?", "Vraag je tandarts om een begroting. Zet de verwachte kosten naast de premie, het vergoedingspercentage en de maximale vergoeding van het pakket. Let ook op wachttijden of een maximum in het eerste jaar.")]
    reken_t = ('<div class="kaart reken" id="rekenhulp"><h2 style="margin-top:0">Rekenhulp: loont een tandartsverzekering voor jou?</h2>'
               '<label for="tk">Wat betaal je per jaar aan de tandarts? (controles, vullingen, mondhygiënist)</label><input id="tk" type="number" inputmode="decimal" min="0" step="10" value="175">'
               '<label for="tp">Premie van het tandpakket per maand</label><input id="tp" type="number" inputmode="decimal" min="0" step="0.5" value="15">'
               '<label for="tv">Vergoedingspercentage</label><select id="tv"><option value="75">75%</option><option value="80">80%</option><option value="100">100%</option></select>'
               '<label for="tm">Maximale vergoeding per jaar</label><select id="tm"><option value="250">€ 250</option><option value="500">€ 500</option><option value="750">€ 750</option><option value="1000">€ 1.000</option></select>'
               '<div class="uit" id="tuit" role="status" aria-live="polite"></div>'
               '<p class="bron">De premie en voorwaarden verschillen per verzekeraar. Dit is een indicatie, geen advies.</p></div>'
               """<script>
(function(){var k=document.getElementById('tk'),p=document.getElementById('tp'),v=document.getElementById('tv'),m=document.getElementById('tm'),u=document.getElementById('tuit');
function n(x){return Math.max(0,parseFloat(String(x.value).replace(',','.'))||0)}
function eur(x){return '€ '+Math.round(x).toLocaleString('nl-NL')}
function r(){var kost=n(k),prem=n(p)*12,verg=Math.min(kost*(+v.value)/100,+m.value),met=prem+kost-verg,zonder=kost;
u.textContent='Zonder verzekering betaal je '+eur(zonder)+'. Met dit pakket betaal je '+eur(met)+' (premie '+eur(prem)+' plus wat je zelf betaalt). '+(met<zonder?('Het pakket scheelt je ongeveer '+eur(zonder-met)+' per jaar.'):('Zonder pakket ben je ongeveer '+eur(met-zonder)+' per jaar goedkoper uit.'))}
[k,p].forEach(function(e){e.addEventListener('input',r)});[v,m].forEach(function(e){e.addEventListener('change',r)});r()})();
</script>""")
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["zorg"]}</span><h1>Tandartsverzekering 2027: loont het nog?</h1></div>'
            '<p class="lead">De tandarts wordt in 2027 ongeveer 3% duurder, maar de vergoedingen van de meeste tandpakketten blijven gelijk. Voor veel mensen kost een tandartsverzekering meer dan hij oplevert.</p>'
            '<div class="kerncijfers"><div><b>102 van 110</b><small>tandpakketten: premie hoger dan vergoeding*</small></div><div><b>± € 175</b><small>gemiddelde tandartskosten per jaar</small></div>'
            '<div><b>+ 3%</b><small>tandartstarieven 2027</small></div><div><b>31 dec</b><small>laatste dag overstappen</small></div></div>'
            '<p class="bron">* Bij gemiddelde tandartskosten. Bron: Overstappen.nl, november 2026.</p>'
            + reken_t +
            '<h2>Wanneer is een tandartsverzekering wél zinvol?</h2><ul class="links">'
            '<li>Je verwacht een <b>grote behandeling</b>, zoals een kroon, brug of implantaat. Vraag eerst een begroting aan je tandarts.</li>'
            '<li>Je kind heeft <b>orthodontie</b> nodig. Die zit niet in de basisverzekering.</li>'
            '<li>Je hebt een <b>gevoelig gebit</b> en elk jaar hoge kosten.</li></ul>'
            '<h2>Wanneer kun je beter zonder?</h2><p>Ben je per jaar zo’n € 100 tot € 150 kwijt aan controles? Dan betaal je met een standaard tandpakket al snel evenveel of meer aan premie dan je terugkrijgt. '
            'Zet het geld van de premie dan liever opzij voor de tandarts. Bij kinderen tot 18 jaar zit de meeste tandartszorg al in de basisverzekering.</p>'
            '<h2>Waar let je op bij een tandpakket?</h2><ul class="links"><li><b>Vergoedingspercentage:</b> 75% of 100% van de kosten.</li><li><b>Maximale vergoeding</b> per jaar.</li><li><b>Welke behandelingen</b> vallen eronder: niet elk pakket vergoedt kronen en bruggen.</li><li><b>Wachttijd of maximum</b> in het eerste jaar.</li></ul>'
            + ZORG_VERGELIJKER +
            '<h2>Meer over je zorgkosten</h2><ul class="links"><li><a href="/aanvullende-verzekering-2027/">Aanvullende verzekering 2027: nodig of niet?</a></li><li><a href="/zorgverzekering-2027/">Zorgverzekering 2027: premies en overstappen</a></li><li><a href="/eigen-risico-2027/">Eigen risico 2027</a></li></ul>'
            + faq_html(faq_t) +
            '<p class="bron">Bronnen: <a href="https://www.overstappen.nl/nieuws/tandarts-3-procent-duurder-in-2027-102-van-de-110-tandpakketten-loont-met-deze-kosten-niet/" rel="noopener">Overstappen.nl (tandpakketten 2027)</a>, '
            '<a href="https://www.consumentenbond.nl/zorgverzekering/vergoedingen/tandarts" rel="noopener">Consumentenbond (tandarts in de basisverzekering)</a>, '
            '<a href="https://www.zorgwijzer.nl/vergoeding/tandarts" rel="noopener">Zorgwijzer (vergoeding kinderen)</a>, '
            '<a href="https://www.bnnvara.nl/kassa/artikelen/sluit-je-wel-of-geen-aanvullende-tandartsverzekering-af-voor-2026-maak-in-vijf-stappen-de-keuze" rel="noopener">Kassa</a>. '
            f'Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/tandartsverzekering-2027/", "Tandartsverzekering 2027: loont het nog? Met rekenhulp", "Bij 102 van de 110 tandpakketten is de premie hoger dan de vergoeding bij gemiddelde kosten. Reken uit of een tandartsverzekering in 2027 voor jou loont.",
         body, [cld, faq_ld(faq_t)], prio="0.9")

    # ---------- Energiecontract opzeggen ----------
    ch, cld = crumbs("Energiecontract opzeggen", "/energiecontract-opzeggen/")
    faq_o = [("Moet ik mijn energiecontract zelf opzeggen als ik overstap?", "Nee. Stap je over naar een andere leverancier, dan regelt je nieuwe leverancier de overstap en zegt hij je oude contract op. Zelf opzeggen moet je alleen als je bijvoorbeeld emigreert."),
             ("Hoe lang is de opzegtermijn van een energiecontract?", "Maximaal 30 dagen, voor elk type contract. Steeds meer leveranciers hanteren een kortere opzegtermijn, bijvoorbeeld 5 dagen."),
             ("Betaal ik een boete als ik een variabel contract opzeg?", "Nee. Een contract voor onbepaalde tijd, zoals een variabel contract, kun je altijd zonder opzegvergoeding opzeggen."),
             ("Hoe hoog is de opzegvergoeding bij een vast contract?", "Die hangt af van hoeveel energie je nog zou verbruiken tot het einde van je contract en van het prijsverschil tussen jouw tarief en het huidige tarief voor hetzelfde contract. Is energie sindsdien duurder geworden, dan betaal je niets. Vraag je leverancier om een schatting; die moet hij geven en uitleggen."),
             ("Mijn vaste contract is van vóór de zomer van 2023. Welke regels gelden dan?", "Voor vaste contracten van vóór de nieuwe regels uit de zomer van 2023 geldt nog een vast bedrag per aansluiting, afhankelijk van hoe lang je contract nog loopt: € 50 bij minder dan 1,5 jaar, oplopend tot € 125 bij meer dan 2,5 jaar. Stroom en gas tellen apart.")]
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON["energie"]}</span><h1>Energiecontract opzeggen: zo voorkom je een boete</h1></div>'
            '<p class="lead">Overstappen van energieleverancier kan veel schelen. Maar bij een vast contract kan te vroeg stoppen geld kosten. Zo weet je vooraf waar je aan toe bent.</p>'
            '<div class="kerncijfers"><div><b>30 dagen</b><small>maximale opzegtermijn</small></div><div><b>€ 0</b><small>opzegvergoeding bij een variabel contract</small></div>'
            '<div><b>Vast</b><small>contract: vergoeding hangt af van prijsverschil</small></div><div><b>1 jan</b><small>2026: nieuwe Energiewet</small></div></div>'
            '<h2>Welk contract heb je?</h2><table><tr><th>Contract</th><th>Opzeggen</th></tr>'
            '<tr><td><b>Variabel</b> (onbepaalde tijd)</td><td>Altijd, zonder opzegvergoeding, met een opzegtermijn van maximaal 30 dagen</td></tr>'
            '<tr><td><b>Dynamisch</b></td><td>Meestal net als variabel: zonder opzegvergoeding</td></tr>'
            '<tr><td><b>Vast</b>, voor de einddatum</td><td>Er kan een opzegvergoeding gelden, afhankelijk van het prijsverschil en je resterende verbruik</td></tr>'
            '<tr><td><b>Vast</b>, na de einddatum</td><td>Je contract loopt meestal door als variabel contract. Dan kun je zonder opzegvergoeding weg</td></tr></table>'
            '<h2>Zo stap je over zonder verrassingen</h2><ol class="stappen">'
            '<li><b>Kijk in je contract</b> wat voor contract je hebt en wanneer het afloopt.</li>'
            '<li><b>Heb je een vast contract?</b> Vraag je leverancier om een schatting van de opzegvergoeding. Die moet hij geven en uitleggen.</li>'
            '<li><b>Vergelijk</b> de besparing bij een nieuw contract met die opzegvergoeding.</li>'
            '<li><b>Sluit het nieuwe contract af.</b> Je nieuwe leverancier zegt je oude contract voor je op.</li></ol>'
            '<div class="let"><b>Let op:</b> past je leverancier zijn voorwaarden aan, bijvoorbeeld door de nieuwe Energiewet? Dan mag je vaak zonder opzegvergoeding overstappen. Lees de brief of e-mail daarover goed.</div>'
            + partner(awin(8520, "bespaarvriend-opzeggen", "https://www.gaslicht.com/energievergelijken"), "Energiecontracten vergelijken", "Vergelijk contracten van alle grote leveranciers. Bij de productvoorwaarden zie je ook de opzegtermijn.", "Vergelijk energiecontracten", [("Variabel en dynamisch", awin(8520, "bespaarvriend-opzeggen", "https://www.gaslicht.com/energievergelijken/dynamisch-energiecontract-vergelijken")), ("3 jaar vast", awin(8520, "bespaarvriend-opzeggen", "https://www.gaslicht.com/energievergelijken/energiecontract-3-jaar-vast"))]) +
            '<h2>Meer over energie</h2><ul class="links"><li><a href="/energie-2027/">Energie 2027: einde salderen en energiebelasting</a></li><li><a href="https://salderingscheck-nl.netlify.app/">Salderingscheck: wat kost het einde van salderen jou?</a></li></ul>'
            + faq_html(faq_o) +
            '<p class="bron">Bronnen: <a href="https://www.acm.nl/nl/publicaties/acm-publiceert-nieuwe-regels-voor-opzeggen-vaste-energiecontracten" rel="noopener">ACM (regels opzegvergoeding)</a>, '
            '<a href="https://www.gaslicht.com/nieuws/overstappen-zonder-boete" rel="noopener">Gaslicht.com (opzegtermijn)</a>, '
            '<a href="https://www.anwb.nl/huis/energie/opzegboete-energie" rel="noopener">ANWB (oude vaste bedragen)</a>, '
            '<a href="https://www.keuze.nl/nieuws/energie-boetevrij-opzeggen-of-nieuwe-voorwaarden-accepteren-dit-kun-je-doen" rel="noopener">Keuze.nl (Energiewet 2026)</a>. '
            f'Bijgewerkt op {BIJGEWERKT}.</p>')
    page("/energiecontract-opzeggen/", "Energiecontract opzeggen: opzegtermijn en opzegvergoeding", "Energiecontract opzeggen zonder boete: maximaal 30 dagen opzegtermijn, geen opzegvergoeding bij variabel. Zo bereken je de vergoeding bij een vast contract.",
         body, [cld, faq_ld(faq_o)], prio="0.8")

    # ---------- sitemap, robots, llms.txt ----------
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                + "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{VANDAAG}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES) + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(f"""# Bespaarvriend
> Gratis, onafhankelijke uitleg over besparen op vaste lasten in Nederland. Gemaakt door Erik Beltman (ook maker van boodschappenvergelijk.nl). Bijgewerkt op {BIJGEWERKT}.

- [Zorgverzekering 2027]({BASE}/zorgverzekering-2027/): gemiddelde premie € 173,13 per maand, laagste premie € 148,40, hoogste € 202,50, verschil € 649 per jaar; overstappen vóór 31 december 2026.
- [Eigen risico 2027]({BASE}/eigen-risico-2027/): verplicht eigen risico € 400 (2026: € 385), met rekenhulp vrijwillig eigen risico.
- [Zorgtoeslag 2027]({BASE}/zorgtoeslag-2027/): maximaal € 140 per maand (alleenstaand), inkomensgrens ± € 42.950, vermogensgrens € 119.122.
- [Energie 2027]({BASE}/energie-2027/): salderen stopt 1 januari 2027; energiebelasting gas € 0,7457/m³, stroom € 0,1065/kWh, vermindering € 628,69; netbeheer gemiddeld + € 141.
- [Aanvullende verzekering 2027]({BASE}/aanvullende-verzekering-2027/): wanneer een aanvullende verzekering loont, met rekenhulp; premies bekend uiterlijk 19 november.
- [Tandartsverzekering 2027]({BASE}/tandartsverzekering-2027/): bij 102 van de 110 tandpakketten is de premie hoger dan de vergoeding bij gemiddelde kosten; rekenhulp.
- [Energiecontract opzeggen]({BASE}/energiecontract-opzeggen/): opzegtermijn maximaal 30 dagen, geen opzegvergoeding bij variabel; vergoeding bij vast hangt af van prijsverschil.
- [Internet en mobiel]({BASE}/internet-en-mobiel/): na de contractperiode maximaal 1 maand opzegtermijn; 79% van de internetabonnementen loopt al door na de contractperiode.
- [Alles op orde](https://allesoporde.netlify.app/): gratis overzicht van je vaste lasten en inkomsten.
- [Bonnenboek](https://bonnenboek.netlify.app/): gratis app om kassabonnen te scannen en boodschappenuitgaven bij te houden, samen met je huishouden.
- [Salderingscheck](https://salderingscheck-nl.netlify.app/): rekent uit wat het einde van salderen per jaar kost en of een thuisbatterij loont.
- [Tankwijzer](https://goedkopertanken.netlify.app/): brandstofprijzen vergelijken in Nederland, België en Duitsland.
- [Vluchtwijzer](https://vluchtwijzer.netlify.app/): goedkope vluchten vergelijken.
- [EuroRoadRules](https://euroroadrules.eu/): vignetten, tol en milieuzones in Europa.
- [Vakantiewijzer](https://vakantietoppers.netlify.app/): pakketreizen, hotels, vakantieparken en campings vergelijken.
- [Foutcodezoeker](https://foutcodezoeker.nl/): foutcodes en reparatie-uitleg voor apparaten.
- [Boodschappen vergelijken](https://boodschappenvergelijk.nl/): dagelijkse prijzen van supermarkten.
""")
    print(f"klaar: {len(PAGES)} pagina's in {OUT}")


if __name__ == "__main__":
    bouw()
