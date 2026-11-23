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
nav.top{margin-left:auto}details.hmenu>summary{list-style:none;cursor:pointer;font-weight:700;font-size:16px;padding:10px 16px;border-radius:12px;background:var(--green);color:var(--on-green);box-shadow:0 2px 6px rgba(14,124,74,.25)}details.hmenu>summary::-webkit-details-marker{display:none}details.hmenu[open]>summary{background:var(--green-dark)}details.hmenu .paneel{position:absolute;left:0;right:0;top:100%;z-index:50;background:var(--surface);box-shadow:0 18px 40px rgba(20,40,28,.18);padding:18px max(16px,calc((100vw - 1140px)/2 + 16px)) 22px;display:grid;grid-template-columns:repeat(3,1fr);gap:6px 24px;max-height:calc(100vh - 70px);overflow:auto}details.hmenu .groep p{margin:10px 0 4px;font-weight:700;font-size:15px;color:var(--muted)}details.hmenu .groep a{display:block;text-align:left;border:0!important;margin:0!important;padding:8px 10px;border-radius:10px;text-decoration:none;font-weight:700;color:var(--ink)}details.hmenu .groep a:hover{background:var(--green-soft);color:var(--green-dark)}header.top{position:relative}header.top nav.top details.hmenu .groep a{display:block!important;text-align:left!important;border:0!important;min-width:0!important;padding:9px 10px!important;font-size:15.5px!important;line-height:1.3!important;white-space:normal!important;color:var(--ink)!important;border-radius:10px!important;background:none!important;text-decoration:none!important}header.top nav.top details.hmenu .groep a:hover{background:var(--green-soft)!important;color:var(--green-dark)!important;text-decoration:none!important}header.top nav.top details.hmenu .groep a+a{border-left:0!important}@media(max-width:820px){details.hmenu .paneel{grid-template-columns:1fr 1fr}}@media(max-width:520px){details.hmenu .paneel{grid-template-columns:1fr;padding-top:6px}details.hmenu .groep{display:grid;grid-template-columns:1fr 1fr;gap:0 6px}details.hmenu .groep p{grid-column:1/-1}details.hmenu .groep a{padding:9px 8px;font-size:15px}}
@media(max-width:420px){.logo{font-size:17px;gap:8px}.logo svg{width:32px;height:32px}}
.crumbs{font-size:14px;color:var(--muted);margin:16px 0 0}.crumbs a{color:var(--muted)}
h1{font:700 clamp(28px,4.6vw,40px)/1.12 var(--text);letter-spacing:-.015em;margin:14px 0 10px;text-wrap:balance}
h2{font:700 22px/1.25 var(--text);margin:30px 0 10px}h3{font-size:18px;margin:20px 0 6px}h1,h2,h3{overflow-wrap:break-word;hyphens:auto}
.lead{font-size:18px;color:var(--muted);margin:0 0 16px}
.kaart{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:18px;margin:14px 0}
.tegels .vu{display:inline-block;margin-top:8px;font-size:12.5px;font-weight:700;color:var(--green-dark);background:var(--green-soft);border-radius:999px;padding:2px 9px}
.uitklappen{display:grid;gap:10px;margin:16px 0 22px}details.uitklap{background:var(--surface);border-radius:var(--r);box-shadow:0 2px 4px rgba(20,40,28,.06),0 8px 20px rgba(20,40,28,.09)}details.uitklap>summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:10px;padding:16px 18px;font-weight:700;font-size:18px;line-height:1.3}details.uitklap>summary::-webkit-details-marker{display:none}details.uitklap>summary::after{content:"";margin-left:auto;flex:none;width:28px;height:28px;border-radius:50%;background:var(--green-soft) url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27 fill=%27none%27 stroke=%27%230a6239%27 stroke-width=%273%27%3E%3Cpath d=%27m6 9 6 6 6-6%27/%3E%3C/svg%3E") center/16px no-repeat;transition:transform .2s}details.uitklap[open]>summary::after{transform:rotate(180deg)}details.uitklap>.inh{padding:0 18px 16px}details.uitklap>.inh>:first-child{margin-top:0}h2.vgl{margin-top:26px}
.uitgelicht{display:flex;gap:16px;align-items:center;text-decoration:none;color:var(--on-green);background:linear-gradient(135deg,#0e7c4a,#0a6239);border-radius:18px;padding:18px 20px;margin:18px 0;box-shadow:0 6px 14px rgba(14,124,74,.28),0 18px 40px rgba(14,124,74,.24);position:relative;overflow:hidden}.uitgelicht:hover{color:var(--on-green);transform:translateY(-2px)}.uitgelicht .gr{flex:none;width:58px;height:58px;border-radius:50%;background:#fff;display:grid;place-items:center;font-size:30px;box-shadow:0 0 0 6px rgba(255,255,255,.18)}@media (max-width:520px){.uitgelicht{align-items:flex-start;padding:34px 16px 16px;gap:12px}.uitgelicht .gr{width:44px;height:44px;font-size:24px}.uitgelicht b{font-size:18px}}.uitgelicht b{display:block;font-size:20px;line-height:1.2}.uitgelicht small{display:block;font-size:15px;opacity:.92;margin-top:3px}.uitgelicht .lbl{position:absolute;top:10px;right:12px;background:#ffd43b;color:#1e2a22;font:700 12px var(--text);padding:2px 8px;border-radius:999px}.uitgelicht .knop{display:inline-block;margin-top:10px;background:#fff;color:#0a6239;font-weight:700;padding:8px 14px;border-radius:10px}
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
html{scroll-behavior:smooth}.plbl{scroll-margin-top:90px}.plbl:target{background:#fff3bf;border-radius:8px;padding:2px 8px;margin-left:-8px}.plbl:target+.pchips a{border:2px solid #ffd43b!important}
.tegels>.tegel.met-keuze{grid-column:1/-1;scroll-margin-top:90px}.tegels>.tegel.met-keuze:target,.tegels>.tegel.met-keuze.uitgelicht{border:3px solid #f2b705!important;background:#fffbea!important;box-shadow:0 0 0 6px rgba(255,212,59,.55),0 12px 26px rgba(0,0,0,.14)!important;animation:kiespuls 1.1s ease-in-out 3}.tegels>.tegel.met-keuze:target::before,.tegels>.tegel.met-keuze.uitgelicht.eerste::before{content:"👇 Kies hier je provider";display:block;background:#ffd43b;color:#1e2a22;font-weight:800;font-size:15px;padding:8px 14px}.tegels>.tegel.met-keuze.uitgelicht:not(.eerste)::before{content:"👇 Of kies hier";display:block;background:#ffd43b;color:#1e2a22;font-weight:800;font-size:15px;padding:8px 14px}@keyframes kiespuls{0%,100%{box-shadow:0 0 0 6px rgba(255,212,59,.55),0 12px 26px rgba(0,0,0,.14)}50%{box-shadow:0 0 0 14px rgba(255,212,59,.25),0 12px 26px rgba(0,0,0,.14)}}@media(prefers-reduced-motion:reduce){.tegels>.tegel.met-keuze:target,.tegels>.tegel.met-keuze.uitgelicht{animation:none}}.tegels .tegel .hoofd{display:block;padding:16px 14px 8px;position:relative;color:var(--ink)}.tegels .tchips{margin:0;padding:0 14px 14px}.tegels .tegel .tchips a{border:1px solid #a9d6bb!important;border-radius:999px!important;background:var(--green-soft)!important}
.widget{overflow:hidden}@media(max-width:440px){.widget [class*="__product__wrapper"]{grid-template-columns:minmax(0,1fr) auto!important}.widget [class*="__product__logo"] img{max-width:96px!important;height:auto}.widget [class*="__price__title"]{white-space:nowrap!important;font-size:13px!important}}.widget [class*="__price__big"]{font-size:clamp(20px,6.5vw,30px)!important}.widget [class*="__product__specification"]{display:flex!important;flex-wrap:wrap!important;gap:10px 18px}.widget [class*="__product__specification"]>*{flex:1 1 90px}.widget .dc-tool,.widget .dc-tool *{min-width:0!important;max-width:100%!important;box-sizing:border-box}.widget [class*="__product__title"],.widget [class*="__product__price"]{white-space:normal!important}
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
.tegels{gap:12px!important;border:0;background:none}
.tegels>a,.tegels>.tegel{background:var(--surface);border:2px solid var(--green)!important;border-radius:16px!important;box-shadow:0 3px 0 rgba(8,80,47,.28),0 8px 18px rgba(0,0,0,.08);transition:transform .12s,box-shadow .12s}
.tegels>a:hover,.tegels>.tegel:hover{transform:translateY(-2px);box-shadow:0 5px 0 rgba(8,80,47,.28),0 12px 22px rgba(0,0,0,.12)}
.tegels>a:active,.tegels>.tegel:active{transform:translateY(2px);box-shadow:0 1px 0 rgba(8,80,47,.28)}
.tegels .ic{border-radius:50%!important;background:var(--green)!important;color:#fff!important}
.tegels b{font-size:18px!important}
.tegels>.tegel{display:flex;flex-direction:column;overflow:hidden;padding:0}
.tegels .tegel a{border:0!important;border-radius:0!important;box-shadow:none!important}
.tegels .tegel a.hoofd{flex:1;display:block;padding:16px 14px;text-decoration:none;color:var(--ink);position:relative;background:none}
.tegels .tegel a.uitleg{display:block;padding:10px 14px;font-size:14px;font-weight:700;background:var(--green-soft);color:var(--green-dark);border-top:1px solid var(--line)!important;text-decoration:underline}
.direct-kop{margin-top:22px}
.intro{position:relative;overflow:hidden;margin:14px 0 4px;padding:22px 20px 20px;border-radius:22px;color:#fff;background:radial-gradient(120% 140% at 100% 0%,#17a061 0%,#0e7c4a 45%,#0a5a35 100%);box-shadow:0 4px 0 #08502f,0 12px 26px rgba(8,80,47,.25)}
.intro .euro{position:absolute;right:-18px;top:50%;transform:translateY(-50%) rotate(-12deg);font:800 210px/1 "Barlow Condensed",system-ui,sans-serif;color:#ffd43b;opacity:.22;pointer-events:none;text-shadow:0 0 40px rgba(255,212,59,.35)}
.intro>*{position:relative}
.intro .pill{display:inline-block;margin:0 0 10px;padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.16);font-size:13px;font-weight:700;letter-spacing:.01em}
.intro h1{color:#fff;margin:0 0 6px;font-size:clamp(28px,7.4vw,44px);line-height:1.05;max-width:13ch}
.intro .kort{margin:0 0 14px;font-size:16px;line-height:1.45;max-width:34ch;color:#e6f5ec}
.intro .maker2{margin:0 0 8px;font-size:14px;color:#e6f5ec}
.intro a{color:#fff;font-weight:700;text-decoration:underline;text-decoration-color:rgba(255,255,255,.5);text-underline-offset:3px}
.intro .bekend{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0;font-size:13px}
.intro .bekend span{color:#cfe9da;margin-right:2px}
.intro .bekend a{text-decoration:none;background:#ffd43b;color:#1e2a22;padding:4px 10px;border-radius:999px;font-weight:800}
@media(min-width:700px){.intro{padding:34px 34px 30px}.intro .euro{font-size:300px;right:10px}}
.tegels>a,.tegels>.tegel{border:2px solid #a9d6bb!important;box-shadow:0 4px 0 #cfe6d8,0 10px 20px rgba(8,80,47,.10)!important;background:#fff!important}.tegels>a:hover{border-color:#0e7c4a!important}
.tegels>a:hover,.tegels>.tegel:hover{box-shadow:0 8px 0 #08502f,0 18px 28px rgba(8,80,47,.28)!important}
.tegels>a:active,.tegels>.tegel:active{transform:translateY(4px);box-shadow:0 2px 0 #08502f!important}
.tegels{gap:16px!important}
.tegels .ic{width:52px!important;height:52px!important}.tegels .ic svg{width:28px!important;height:28px!important}
.tegels b{font-size:19px!important;color:#10261a}
.tegels a .pijl{width:30px;height:30px;border-radius:50%;background:#ffd43b;color:#1e2a22!important;display:grid;place-items:center;top:14px!important;right:12px!important}
.tegels a .pijl svg{width:18px;height:18px}
@media (prefers-color-scheme:dark){.tegels>a,.tegels>.tegel{background:#1a221c!important}.tegels b{color:#e9efe8}}
.intro{padding:12px 16px 12px!important;margin:10px 0 2px!important;border-radius:16px!important;box-shadow:0 3px 0 #08502f,0 8px 16px rgba(8,80,47,.2)!important}
.intro .euro{font-size:120px!important;right:-6px!important;opacity:.2!important}
.intro h1{font-size:clamp(21px,5.8vw,32px)!important;max-width:none!important;margin:0 0 2px!important}
.intro .kort{font-size:14px!important;margin:0 0 6px!important;max-width:30ch!important}
.intro .bekend{display:block!important;font-size:12.5px!important;line-height:1.9;color:#e6f5ec;max-width:34ch}
.intro .bekend a:not(.b){background:none!important;color:#fff!important;padding:0!important;font-weight:800;text-decoration:underline}
.intro .bekend a.b{text-decoration:none;background:#ffd43b;color:#1e2a22;padding:2px 8px;border-radius:999px;font-weight:800;white-space:nowrap}
.intro{text-align:center}.intro .kort,.intro .bekend{margin-left:auto!important;margin-right:auto!important}
h2:has(+ .tegels),h2:has(+ .agenda),h2:has(+ .bron + .tegels),h2:has(+ .bron + .tegels)+.bron{text-align:center}.partners-top .keuzes{margin:16px 0 4px;padding:6px 14px 4px;background:#fff;border:2px solid #a9d6bb;border-radius:18px;box-shadow:0 4px 0 #cfe6d8,0 10px 20px rgba(8,80,47,.10)}.partners-top .keuzes .pchips:last-child{margin-bottom:8px}@media(max-width:640px){header.top .wrap{gap:8px!important}.logo svg{width:40px!important;height:40px!important}nav.top{display:flex!important;flex-wrap:wrap!important;justify-content:center;flex:1;gap:3px 0!important;overflow:visible!important;margin-left:0!important}header.top nav.top a{flex:0 0 auto;padding:2px clamp(7px,2.6vw,12px)!important;font-size:clamp(14px,4.2vw,18px)!important;line-height:1.05!important;white-space:nowrap;text-align:center}}
header.top nav.top a{color:#0e7c4a!important;font-weight:700;text-decoration:none!important;border-radius:0!important;background:none!important;box-shadow:none!important;border:0!important}header.top nav.top a+a{border-left:2px solid #0e7c4a!important}.nbr{display:none}@media(max-width:640px){.nbr{display:block;flex-basis:100%;height:0}}@media(min-width:641px){header.top nav.top .nbr+a{border-left:2px solid #0e7c4a!important}}header.top nav.top a:hover{background:none!important;color:#0a5a35!important;text-decoration:underline!important}
@media(min-width:641px){nav.top{gap:6px!important}header.top nav.top a{min-width:96px;text-align:center;padding:5px 10px!important}}
.logo svg{filter:drop-shadow(0 5px 0 #08502f) drop-shadow(0 14px 16px rgba(8,80,47,.55)) drop-shadow(0 0 1px rgba(255,255,255,.6));transform:translateY(-4px) scale(1.14);transition:transform .15s}.logo:active svg{transform:translateY(0) scale(1.04)}
header.top nav.top a:active{transform:translateY(1px);box-shadow:none!important}
header.top nav.top a[aria-current],header.top nav.top a.actief{background:linear-gradient(180deg,#ffd43b,#f2c12e)!important;color:#1e2a22!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.5),0 3px 0 #b8901a!important}.agenda{list-style:none;padding:0;margin:0 0 8px;display:grid;gap:8px}.agenda li{display:grid;grid-template-columns:64px 1fr auto;gap:10px;align-items:center;background:#fff;border:2px solid #a9d6bb;border-radius:14px;padding:10px 12px;box-shadow:0 3px 0 #cfe6d8,0 8px 16px rgba(8,80,47,.08)}.agenda li b{background:#ffd43b;color:#1e2a22;border-radius:8px;text-align:center;padding:4px 2px;font-size:14px;white-space:nowrap}.agenda li span{font-weight:600;font-size:15px;line-height:1.3}.agenda li a{font-weight:700;font-size:14px;color:#0e7c4a;white-space:nowrap}.agenda li{grid-template-columns:64px 1fr auto!important}.ag-acties{display:flex;flex-direction:column;align-items:flex-end;gap:4px}.ag-add{position:relative}.ag-add summary{list-style:none;cursor:pointer;font-weight:700;font-size:13px;color:#0e7c4a;white-space:nowrap;background:#e7f4ec;border-radius:999px;padding:3px 9px}.ag-add summary::-webkit-details-marker{display:none}.ag-add[open]>a{display:block;margin-top:6px;font-size:14px;font-weight:700;color:#0e7c4a;white-space:nowrap;text-align:right}.ag-alles{text-align:center;margin:10px 0 4px;font-size:15px}.ag-alles a{font-weight:700;color:#0e7c4a}.ag-alles small{color:var(--muted)}.tegels small strong{font-weight:800;color:var(--ink,#1e2a22)}.intro .kort{font-weight:700;max-width:none!important}.intro .bekend{font-size:11px!important;line-height:1.8!important;opacity:.95}.intro .bekend a.b{padding:1px 7px!important}.intro h1{font-size:clamp(22px,7.3vw,48px)!important;white-space:nowrap;letter-spacing:-.02em!important;line-height:1.05!important;text-shadow:0 2px 0 #08502f,0 4px 14px rgba(0,0,0,.35)}
@media(min-width:700px){.intro{padding:18px 24px!important}.intro .euro{font-size:170px!important;right:20px!important}.intro .bekend{max-width:none}}
.tegels .tegel a.uitleg{padding:5px 12px!important;font-size:13px!important;line-height:1.3}
.tegels b{font-size:17px!important;overflow-wrap:anywhere;hyphens:auto}
@media(min-width:420px){.tegels b{font-size:19px!important}}
@media(max-width:420px){nav.top a{font-size:13.5px!important;padding:7px 4px!important}}@media(max-width:480px){header.top nav.top a{font-size:13px!important;padding:6px 5px!important}}
/* intro zonder groen blok, groene letters met duidelijke schaduw */
.intro{background:#fff!important;border:2px solid #a9d6bb!important;border-radius:16px!important;box-shadow:0 4px 0 #cfe6d8,0 10px 20px rgba(8,80,47,.10)!important;color:#0e7c4a!important;overflow:hidden!important;padding:16px 14px 14px!important;margin:12px 0 6px!important}
.intro .euro{color:#ffd43b!important;opacity:.85!important;text-shadow:3px 4px 0 #e0a800,0 6px 14px rgba(0,0,0,.2)!important}
.intro h1{color:#0a6239!important;text-shadow:2px 3px 0 #ffd43b,0 8px 16px rgba(0,0,0,.45)!important}
.intro .kort{color:#0a5a35!important}
.intro .bekend{color:#1e2a22!important}
.intro .bekend a:not(.b){color:#0e7c4a!important}
.foot .wrap{display:grid;gap:4px}
.foot .free{text-align:center;color:var(--muted);font-size:14px;font-weight:400;margin:0 auto 6px;max-width:52ch}
.foot .fkop{text-align:center;font-weight:800;color:var(--ink);font-size:13px;text-transform:uppercase;letter-spacing:.06em;margin:14px 0 2px}
.foot nav{display:grid!important;grid-template-columns:1fr 1fr;gap:0!important;max-width:520px;margin:0 auto!important;width:100%;border-top:1px solid var(--line)}
.foot nav a{display:block;text-align:center;padding:8px 6px;font-weight:600;font-size:14px;line-height:1.3;text-decoration:none;color:var(--green-dark);border-bottom:1px solid var(--line)}
.foot nav a:nth-child(even){border-left:1px solid var(--line)}
.foot nav a:hover{text-decoration:underline}
.foot nav a:last-child:nth-child(odd){grid-column:1/-1;border-left:0}
.foot .small{text-align:center;color:var(--muted);font-size:13px;margin:12px 0 0}
.foot .small.copy{margin-top:2px}
.foot .small a{color:var(--green-dark);font-weight:600}
.partners-top{margin:14px 0 22px}.partners-top .tegels{margin:0 0 10px}.partners-top .plbl{margin:10px 0 4px;font-weight:700;font-size:14px}
.tegels.direct>a:only-child{grid-column:1/-1}
.kaart.partner,.kaart.tool{border:2px solid var(--green)!important;border-radius:16px!important;box-shadow:0 3px 0 rgba(8,80,47,.28),0 8px 18px rgba(0,0,0,.08)}
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
    "tv": _svg('<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>'),
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
DAISYCON_GEKEURD = True
DC_MEDIA = 449774
WIDGETS = {  # naam: (script-slug, css-klasse, extra config)
    "energie": ("energy-nl", "dc-energy-tool", {}),
    "simonly": ("sim-only", "dc-sim-only-tool", {"limit": 3, "limitSplit": 3, "showFilters": False}),
    "budgetmobiel": ("sim-only", "dc-sim-only-tool", {"limit": 3, "limitSplit": 3, "showFilters": False, "filter": {"provider": {"value": ["2"]}}}),
    "telecom": ("all-in-one", "dc-all-in-one-tool", {"limit": 3, "limitSplit": 3, "showFilters": False}),
    "vakantie": ("vacation", "dc-vacation-tool", {"limit": 3, "limitSplit": 3, "showFilters": False}),
    "enquetes": ("market-research", "dc-market-research-tool", {"locale": "nl-NL", "limit": 25, "showFilters": True}),
}

def widget(naam, titel):
    if not DAISYCON_GEKEURD or naam not in WIDGETS:
        return ""
    slug, klasse, extra = WIDGETS[naam]
    cfg = {"mediaId": DC_MEDIA, "subId": "bespaarvriend-" + naam, "language": "nl", "filter": {}}
    cfg.update(extra)
    return (f'<section class="widget" id="w-{naam}" aria-label="{esc(titel)}"><h2>{esc(titel)}</h2><p class="ad">{"Advertentie. Meld je je via deze lijst aan bij een panel, dan krijgt Bespaarvriend een vergoeding. Jij betaalt niets." if naam == "enquetes" else "Advertentie. Sluit je via deze vergelijker iets af, dan krijgt Bespaarvriend een vergoeding. Jij betaalt niets extra."}</p>'
            f'<script src="https://daisycon.tools/{slug}/app.js" defer></script><div class="dc-tool {klasse}" data-config=\'{json.dumps(cfg)}\'></div></section>')

from urllib.parse import quote as _q
def awin(mid, ref, doel=None):
    u = f"https://www.awin1.com/cread.php?awinmid={mid}&amp;awinaffid=3152283&amp;clickref={ref}"
    return u + (f"&amp;ued={_q(doel, safe='')}" if doel else "")
def dc(host, si, li, ref, pad=""):
    return f"https://{host}/c/?si={si}&amp;li={li}&amp;wi=449774&amp;ws={ref}&amp;dl={_q(pad, safe='')}"
def dynamisch_blok(ref):
    return partner(dc("glp8.net", 19921, 1848248, ref, "nl"), "Dynamisch energiecontract afsluiten", "Een contract waarbij je per uur de actuele stroomprijs betaalt. Past als je je verbruik kunt verschuiven naar goedkope uren.", "Bekijk dynamisch contract",
                   [("Per uur afgerekend", dc("glp8.net", 19921, 1848248, ref, "nl")), ("Met inzicht-app", dc("d.energyzero.nl", 20943, 1892250, ref))])
def batterij_blok(ref):
    return partner(dc("glp8.net", 20779, 1881195, ref), "Plug-and-play thuisbatterij", "Een batterij die je zelf in het stopcontact steekt, zonder installateur. Slaat overdag zonnestroom op voor de avond.", "Bekijk thuisbatterijen",
                   [("Instapmodel", dc("glp8.net", 20779, 1881195, ref, "products/zendure-solarflow-1600-ac")), ("Ander merk", dc("glp8.net", 23136, 1970556, ref, "nl")), ("Slimme energiemeter", dc("partner.homewizard.com", 18407, 1795784, ref, "nl/"))])
def partner(url, titel, tekst, knop, artikelen=()):
    chips = ''.join((f'<a href="{u}">{esc(t)}</a>' if u.startswith('#') else f'<a href="{u}" rel="sponsored noopener" target="_blank">{esc(t)}</a>') for t, u in artikelen)
    return (f'<div class="kaart partner"><p class="ad">Advertentie</p><b>{titel}</b><p>{tekst}</p>'
            + (f'<div class="pchips">{chips}</div>' if chips else '') +
            f'<a class="btn" href="{url}" rel="sponsored noopener" target="_blank">{knop}{ICON["pijl"]}</a>'
            '<p class="bron">Sluit je via deze link iets af, dan krijgt Bespaarvriend een kleine vergoeding. Jij betaalt niets extra.</p></div>')

NAV = '<nav class="top" aria-label="Hoofdmenu"><details class="hmenu"><summary>☰ Menu</summary><div class="paneel"><div class="groep"><p>🩺 Zorg</p><a href="/zorgverzekering-2027/">Zorgverzekering 2027</a><a href="/zorgverzekering-overstappen/">Overstappen</a><a href="/aanvullende-verzekering-2027/">Aanvullende verzekering</a><a href="/tandartsverzekering-2027/">Tandartsverzekering</a><a href="/fysiotherapie-vergoeding-2027/">Fysiotherapie</a><a href="/eigen-risico-2027/">Eigen risico</a></div><div class="groep"><p>⚡ Energie en wonen</p><a href="/energie-2027/">Energie 2027</a><a href="/salderen-2027/">Einde salderen</a><a href="/energierekening-verlagen/">Energierekening verlagen</a><a href="/energiecontract-opzeggen/">Energiecontract opzeggen</a><a href="/huurverhoging-2027/">Huurverhoging 2027</a><a href="https://stroomwekker.eu/?bron=bespaarvriend">Stroomwekker (dynamisch contract)</a></div><div class="groep"><p>📱 Internet en mobiel</p><a href="/internet-en-mobiel/">Internet en mobiel</a><a href="/sim-only-overstappen/">Sim only overstappen</a><a href="/refurbished-telefoon-kopen/">Refurbished telefoon</a><a href="/abonnementen-opzeggen/">Abonnementen opzeggen</a></div><div class="groep"><p>🚗 Auto en reizen</p><a href="/auto-en-tanken/">Auto en tanken</a><a href="/autoverzekering-besparen/">Autoverzekering</a><a href="/wegenbelasting-2027/">Wegenbelasting 2027</a><a href="/vakantie-en-vliegen/">Vakantie en vliegen</a><a href="/goedkoop-vliegen/">Goedkoop vliegen</a><a href="/reisverzekering-doorlopend-of-kortlopend/">Reisverzekering</a></div><div class="groep"><p>💶 Toeslagen en geld terug</p><a href="/zorgtoeslag-2027/">Zorgtoeslag</a><a href="/huurtoeslag-2027/">Huurtoeslag</a><a href="/kindgebonden-budget-2027/">Kindgebonden budget</a><a href="/kinderbijslag-2027/">Kinderbijslag</a><a href="/kinderopvangtoeslag-2027/">Kinderopvangtoeslag</a><a href="/noodfonds-energie-2027/">Noodfonds Energie</a><a href="/isde-subsidie-2027/">ISDE subsidie</a><a href="/belastingen-2027/">Belastingen 2027</a><a href="/belastingaangifte-tips/">Belasting terug</a><a href="/bijverdienen-met-enquetes/">Bijverdienen met enquêtes</a></div><div class="groep"><p>🛒 Boodschappen en spullen</p><a href="/boodschappen/">Boodschappen</a><a href="/goedkoop-boodschappen-doen/">Goedkoop boodschappen doen</a><a href="/elektronica/">Elektronica en witgoed</a><a href="/administratie/">Vaste lasten op orde</a></div></div></details></nav>'
FOOT = f"""<footer class="foot"><div class="wrap">
<p class="free">Bespaarvriend helpt je besparen op je vaste lasten. Gratis en onafhankelijk uitgelegd. Wij geven geen persoonlijk financieel advies.</p>
<p class="fkop">Zorg</p><nav aria-label="Zorg"><a href="/zorgverzekering-2027/">Zorgverzekering 2027</a><a href="/zorgverzekering-overstappen/">Overstappen</a><a href="/aanvullende-verzekering-2027/">Aanvullende verzekering</a><a href="/tandartsverzekering-2027/">Tandartsverzekering</a><a href="/fysiotherapie-vergoeding-2027/">Fysiotherapie</a><a href="/eigen-risico-2027/">Eigen risico 2027</a><a href="/zorgtoeslag-2027/">Zorgtoeslag 2027</a><a href="/huurtoeslag-2027/">Huurtoeslag 2027</a><a href="/huurverhoging-2027/">Huurverhoging 2027</a><a href="/kindgebonden-budget-2027/">Kindgebonden budget 2027</a><a href="/kinderbijslag-2027/">Kinderbijslag 2027</a><a href="/kinderopvangtoeslag-2027/">Kinderopvangtoeslag 2027</a><a href="/belastingen-2027/">Belastingen 2027</a><a href="/belastingaangifte-tips/">Belastingaangifte tips</a><a href="/administratie/">Vaste lasten op orde</a></nav>
<p class="fkop">Energie, internet en mobiel</p><nav aria-label="Energie, internet en mobiel"><a href="/energie-2027/">Energie 2027</a><a href="/salderen-2027/">Einde salderen</a><a href="/energierekening-verlagen/">Energierekening verlagen</a><a href="/noodfonds-energie-2027/">Noodfonds Energie 2027</a><a href="/isde-subsidie-2027/">ISDE subsidie 2027</a><a href="/abonnementen-opzeggen/">Abonnementen opzeggen</a><a href="/goedkoop-boodschappen-doen/">Goedkoop boodschappen doen</a><a href="/energiecontract-opzeggen/">Contract opzeggen</a><a href="/internet-en-mobiel/">Internet en mobiel</a><a href="/sim-only-overstappen/">Sim only overstappen</a><a href="/refurbished-telefoon-kopen/">Refurbished telefoon</a><a href="/boodschappen/">Boodschappen</a></nav>
<p class="fkop">Reizen en auto</p><nav aria-label="Reizen en auto"><a href="/vakantie-en-vliegen/">Vakantie en vliegen</a><a href="/goedkoop-vliegen/">Goedkoop vliegen</a><a href="/reisverzekering-doorlopend-of-kortlopend/">Reisverzekering</a><a href="/auto-en-tanken/">Auto en tanken</a><a href="/wegenbelasting-2027/">Wegenbelasting 2027</a><a href="/autoverzekering-besparen/">Autoverzekering</a></nav>
<p class="fkop">Meer gratis hulpmiddelen van Erik</p><nav aria-label="Meer gratis hulpmiddelen van Erik"><a href="https://boodschappenvergelijk.nl/">Boodschappenvergelijk</a><a href="https://goedkopertanken.netlify.app/">Tankwijzer</a><a href="https://vluchtwijzer.netlify.app/">Vluchtwijzer</a><a href="https://vakantietoppers.netlify.app/">Vakantiewijzer</a><a href="https://salderingscheck-nl.netlify.app/">Salderingscheck</a><a href="https://stroomwekker.eu/">Stroomwekker</a><a href="https://euroroadrules.eu/">EuroRoadRules</a><a href="https://foutcodezoeker.nl/">Foutcodezoeker</a><a href="/elektronica/">Elektrovergelijk</a><a href="https://bonnenboek.netlify.app/">Bonnenboek</a><a href="https://allesoporde.netlify.app/">Alles op orde</a></nav>
<p class="fkop">Over</p><nav aria-label="Over"><a href="/over/">Over Bespaarvriend</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/gebruiksvoorwaarden/">Gebruiksvoorwaarden</a><a href="/sitemap.xml">Sitemap</a></nav>
<p class="small">Gemaakt door Erik, de maker van <a href="https://boodschappenvergelijk.nl/?bron=bespaarvriend">Boodschappenvergelijk.nl</a>. Bijgewerkt op {BIJGEWERKT}.</p><p class="small copy">© {datetime.date.today().year} Bespaarvriend – Erik Beltman. Alle rechten voorbehouden. <a href="/gebruiksvoorwaarden/">Auteursrecht en gebruiksvoorwaarden</a></p></div></footer>"""


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



import re as _re
def _blokken_naar_boven(body):
    """Zet betaalde blokken (partners en vergelijkers) bovenaan, direct na de titel en de inleiding."""
    gevonden = []
    def pak(start_tag, s):
        uit = ""
        while True:
            i = s.find(start_tag)
            if i < 0:
                return s, uit
            tag = start_tag.split()[0][1:]
            diepte, j = 0, i
            pat = _re.compile(r'<(/?)' + tag + r'\b[^>]*>')
            for m in pat.finditer(s, i):
                diepte += -1 if m.group(1) else 1
                if diepte == 0:
                    j = m.end(); break
            blok = s[i:j]
            # losse kop direct ervoor (zonder tekst ertussen) gaat mee weg
            voor = s[:i]
            mk = _re.search(r'<h2>[^<]*</h2>\s*$', voor)
            if mk:
                voor = voor[:mk.start()]
            gevonden.append(blok)
            s = voor + s[j:]
    for t in ('<section class="widget"', '<div class="kaart partner"'):
        body, _ = pak(t, body)
    if not gevonden:
        return body
    top = _als_tegels(gevonden)
    m = _re.search(r'<p class="lead">.*?</p>', body, _re.S)
    if m:
        return body[:m.end()] + top + body[m.end():]
    m = _re.search(r'</h1>(</div>)?', body)
    return body[:m.end()] + top + body[m.end():] if m else top + body


_KORT = {
    "Zorgverzekering kiezen met hulp": ("Zorgverzekering kiezen", "Hulp bij je keuze"),
    "Autoverzekeringen vergelijken": ("Autoverzekering vergelijken", "Veel verzekeraars"),
    "Alle zorgverzekeringen van 2027 naast elkaar": ("Zorgverzekering vergelijken", "Alle polissen van 2027"),
    "Zorgverzekering met collectieve korting": ("Zorgverzekering met korting", "Via een collectief"),
    "Autoverzekering met korting": ("Autoverzekering met korting", "Premie direct berekend"),
    "Banden kopen": ("Banden kopen", "Prijs per bandenmaat"),
    "Banden vergelijken": ("Banden vergelijken", "Ook met montage"),
    "Boodschappenbox van de boer": ("Box van de boer", "Vers, thuisbezorgd"),
    "Energiecontract vergelijken": ("Energiecontract vergelijken", "Alle grote leveranciers"),
    "Energiecontracten vergelijken": ("Energiecontract vergelijken", "Alle grote leveranciers"),
    "Huurauto inclusief verzekering": ("Huurauto", "Alle verzekeringen inbegrepen"),
    "Internet en tv met korting": ("Internet en tv", "Met korting via een collectief"),
    "Telefoon met abonnement": ("Telefoon met abonnement", "Kies je provider"),
    "Sim only": ("Sim only", "Kies je provider"),
    "Glasvezel en internet thuis": ("Glasvezel thuis", "Kies je provider"),
    "Internet en tv": ("Internet en tv", "Kies je provider"),
    "Korting op elke tankbeurt": ("Tankkorting", "Korting per liter"),
    "Maaltijdbox": ("Maaltijdbox", "Minder weggooien"),
    "Refurbished telefoon met garantie": ("Refurbished telefoons/iPads", "Met garantie"),
    "Reisverzekering": ("Reisverzekering", "Eén reis of het hele jaar"),
    "Sim only met een duidelijke maandprijs": ("Sim only", "Vaste prijs per maand"),
    "Snellere wifi in huis": ("Snellere wifi", "Router of mesh"),
    "Vliegtickets boeken": ("Vliegtickets", "800+ maatschappijen"),
    "eSIM voor buiten de EU": ("eSIM", "Internet buiten de EU"),
}

def _icoon_voor(t):
    t = t.lower()
    for woorden, ic in ((("zorg", "tand"), "zorg"), (("energie", "stroom", "gas"), "energie"), (("wifi", "router", "internet", "tv"), "internet"),
                        (("telefoon", "sim", "esim", "mobiel"), "mobiel"), (("vlieg",), "vlucht"), (("reis",), "koffer"),
                        (("huurauto", "auto", "band", "tank"), "tank"), (("boodschap", "maaltijd", "boer"), "boodschappen")):
        if any(w in t for w in woorden):
            return ic
    return "check"

_KIES = {"Telefoon met abonnement", "Sim only", "Glasvezel en internet thuis", "Internet en tv"}  # tegels die eerst de providerkeuze tonen

def _als_tegels(blokken):
    """Zet partnerblokken om naar tegels in de stijl van de startpagina, met keuzelinks eronder."""
    pijl = f'<span class="pijl">{ICON["pijl"]}</span>'
    tegels, extra, rest = [], [], []
    for b in blokken:
        if 'class="kaart partner"' not in b:
            rest.append(b); continue
        titel = _re.search(r'<b>(.*?)</b>', b, _re.S).group(1)
        tekst = _re.search(r'</b><p>(.*?)</p>', b, _re.S).group(1)
        url = _re.search(r'<a class="btn" href="([^"]+)"', b).group(1)
        naam, kort = _KORT.get(titel, (titel, _re.split(r'(?<=[.!?])\s', tekst)[0][:40]))
        chips = _re.search(r'<div class="pchips">(.*?)</div>', b, _re.S)
        ic = f'<span class="ic">{ICON[_icoon_voor(titel)]}</span>'
        if chips:  # keuzes staan op de tegel zelf
            if titel in _KIES:  # meerdere aanbieders: kop is geen link, kies onderaan
                kop = f'<div class="hoofd">{ic}<b>{naam}</b><small>{kort}</small></div>'
            else:
                kop = f'<a class="hoofd" href="{url}" rel="sponsored noopener" target="_blank">{ic}{pijl}<b>{naam}</b><small>{kort}</small></a>'
            anker = "kies-" + _re.sub(r'[^a-z0-9]+', '-', titel.lower()).strip('-')
            tegels.append(f'<div class="tegel met-keuze" id="{anker}">{kop}<div class="pchips tchips">{chips.group(1)}</div></div>')
        else:
            tegels.append(f'<a href="{url}" rel="sponsored noopener" target="_blank">{ic}{pijl}<b>{naam}</b><small>{kort}</small></a>')
    tegels = [t for t in tegels if not t.startswith('<div')] + [t for t in tegels if t.startswith('<div')]
    uit = '<div class="partners-top"><div class="tegels direct">' + "".join(tegels) + '</div>' + (('<div class="keuzes">' + "".join(extra) + '</div>') if extra else '')
    uit += ('<script>(function(){var g={"#internet":["kies-internet-en-tv","kies-glasvezel-en-internet-thuis"],"#mobiel":["kies-telefoon-met-abonnement","kies-sim-only"]}[location.hash];'
            'if(!g)return;g.forEach(function(id,i){var e=document.getElementById(id);if(!e)return;e.classList.add("uitgelicht");'
            'if(!i){e.classList.add("eerste");setTimeout(function(){e.scrollIntoView({block:"start"})},60)}})})()</script>')
    uit += '<p class="bron" style="margin-top:6px">Advertentie: deze tegels gaan naar partners. Sluit je iets af, dan krijgt Bespaarvriend een kleine vergoeding. Jij betaalt niets extra.</p></div>'
    if any("dc-energy-tool" in r for r in rest):  # energiepagina's: eerst de vergelijker, dan de tegels
        return "".join(rest) + uit
    return uit + "".join(rest)

def _bovenniveau(html):
    """Splits html in elementen op het hoogste niveau (tekst tussen tags gaat mee met het vorige element)."""
    stuk, diepte, start, uit = 0, 0, 0, []
    for m in _re.finditer(r'<(/?)(div|section|ul|ol|table|details|nav|script|h2|p|figure|blockquote)\b[^>]*>', html):
        sluit, tag = m.group(1), m.group(2)
        if not sluit:
            if diepte == 0 and m.start() > start and html[start:m.start()].strip():
                uit.append(html[start:m.start()])
            if diepte == 0: start = m.start()
            diepte += 1
        else:
            diepte -= 1
            if diepte == 0:
                uit.append(html[start:m.end()]); start = m.end()
    if html[start:].strip(): uit.append(html[start:])
    return uit

def _uitleg_dan_vergelijken(body):
    """Pagina-opbouw: titel en inleiding, dan de uitleg in uitklapblokken, dan de vergelijkers, dan vragen en bronnen."""
    paid = []
    def pak(start_tag, s):
        while True:
            i = s.find(start_tag)
            if i < 0: return s
            tag = start_tag.split()[0][1:]
            diepte, j = 0, i
            for m in _re.finditer(r'<(/?)' + tag + r'\b[^>]*>', s[i:]):
                diepte += -1 if m.group(1) else 1
                if diepte == 0: j = i + m.end(); break
            voor = s[:i]
            mk = _re.search(r'<h2>[^<]*</h2>\s*$', voor)
            if mk: voor = voor[:mk.start()]
            paid.append(s[i:j]); s = voor + s[j:]
    for t in ('<section class="widget"', '<div class="kaart partner"'):
        body = pak(t, body)
    m = _re.search(r'<p class="lead">.*?</p>', body, _re.S) or _re.search(r'</h1>(</div>)?', body)
    if not m: return _blokken_naar_boven(body)
    kop, rest = body[:m.end()], body[m.end():]
    els = _bovenniveau(rest)
    zichtbaar, secties, eind, huidig = [], [], [], None
    for e in els:
        st = e.lstrip()
        if st.startswith('<section class="faq"') or st.startswith('<p class="bron">Bron') or eind:
            eind.append(e); continue
        if st.startswith('<h2'):
            huidig = [_re.sub(r'<[^>]+>', '', st).strip(), []]; secties.append(huidig); continue
        if huidig is None:
            if 'class="kerncijfers"' in st[:60] or 'class="kaart reken"' in st[:60] or (st.startswith('<p class="bron"') and zichtbaar): zichtbaar.append(e)
            elif 'class="kaart tool"' in st[:60]: eind.insert(0, e) if False else zichtbaar.append(e)
            else:
                if not secties or secties[0][0] != 'Belangrijk om te weten': secties.insert(0, ['Belangrijk om te weten', []])
                secties[0][1].append(e)
        else:
            huidig[1].append(e)
    if not secties:
        return _blokken_naar_boven(body if not paid else kop + "".join(paid) + rest)
    tools = [e for e in zichtbaar if 'kaart tool' in e[:60]]
    zichtbaar = [e for e in zichtbaar if e not in tools]
    uitklap = '<div class="uitklappen">' + "".join(
        f'<details class="uitklap"><summary>{esc(t)}</summary><div class="inh">{"".join(c)}</div></details>' for t, c in secties if "".join(c).strip()) + '</div>'
    vgl = ('<h2 class="vgl">Vergelijk en bespaar</h2>' + _als_tegels(paid)) if paid else ''
    return kop + "".join(zichtbaar) + uitklap + vgl + "".join(tools) + "".join(eind)

def page(path, title, desc, body, ld=(), noindex=False, prio="0.8"):
    body = _re.sub(r'<table><tr><th></th>.*?</table>', lambda m: _re.sub(r'<tr><td>(.*?)</td>', r'<tr><th scope="row">\1</th>', m.group(0)).replace('<tr><th scope="row"></th>', '<tr><td></td>', 1), body, flags=_re.S)
    if path not in ("/", "/over/", "/contact/", "/privacy/", "/gebruiksvoorwaarden/", "/bedankt/", "/404.html") and not path.startswith("/elektronica"):
        body = _uitleg_dan_vergelijken(body)
    lds = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": BASE + path, "description": desc, "inLanguage": "nl-NL",
            "dateModified": VANDAAG, "publisher": {"@type": "Organization", "name": "Bespaarvriend", "url": BASE}}] + list(ld)
    doc = f"""<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{BASE}{path}">
{'<meta name="robots" content="noindex">' if noindex else ''}<meta name="theme-color" content="#0e7c4a"><meta name="google-site-verification" content="Isum4B2AiTVAS9A4twzJT8GNjJFXqbZ6UT36pKaBPHE">
{'<meta name="e0d5a73bd035a1c" content="277030417ea9ada19f69ae08c41fb74b">' if path == "/" else ''}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:locale" content="nl_NL"><meta property="og:image" content="{BASE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta property="og:site_name" content="Bespaarvriend">
<link rel="preload" href="/fonts/atkinson-hyperlegible-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/atkinson-hyperlegible-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/manifest.webmanifest"><meta name="theme-color" content="#0e7c4a"><script src="/installeer.js" defer></script>
<style>{CSS}</style>
{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in lds)}
<script data-goatcounter="https://bespaarvriend.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</head><body><header class="top"><div class="wrap"><a class="logo" href="/" aria-label="Bespaarvriend, naar de startpagina">{LOGO}<span>Bespaarvriend</span></a>{NAV}</div></header>
<main class="wrap">{body}</main>{FOOT}<script>document.addEventListener("click",function(e){{var m=document.querySelector("details.hmenu");if(m&&m.open&&!m.contains(e.target))m.open=false}});document.addEventListener("keydown",function(e){{if(e.key==="Escape"){{var m=document.querySelector("details.hmenu");if(m)m.open=false}}}});if("serviceWorker" in navigator)navigator.serviceWorker.register("/sw.js").catch(function(){{}})</script></body></html>"""
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
# Tweede zorgvergelijker (Awin 8601, aangesloten nov 2026): alleen de standaard landingspagina.
ZORG_VERGELIJKER += partner(awin(8601, "bespaarvriend-zorg2"),
    "Zorgverzekering kiezen met hulp",
    "Vergelijk polissen en aanvullende pakketten op wat jij belangrijk vindt, en stap direct over. Gratis.",
    "Bekijk de vergelijking")

# Tegels bovenaan de startpagina: direct naar goedgekeurde partners (geen namen van adverteerders).
DIRECT = [
    (awin(107738, "bespaarvriend-tegel", "https://www.poliswijzer.nl/zorgverzekering"), "zorg", "Zorgverzekering vergelijken", "Overstappen kan <strong>tot 31 december</strong>"),
    (awin(8520, "bespaarvriend-tegel", "https://www.gaslicht.com/energievergelijken"), "energie", "Energiecontract vergelijken", "Ook met tarieven voor 2027"),
    ("/internet-en-mobiel/#internet", "internet", "Internet vergelijken", "Glasvezel, internet en tv"),
    ("/internet-en-mobiel/#mobiel", "mobiel", "Mobiel abonnement vergelijken", "Sim only of met telefoon"),
    (awin(63484, "bespaarvriend-tegel", "https://www.vliegwinkel.nl/"), "vlucht", "Vliegtickets", "Meer dan 800 maatschappijen"),
    (awin(78144, "bespaarvriend-tegel", "https://www.hansemerkur.nl/reisverzekeringen"), "koffer", "Reisverzekering", "Eén reis of het hele jaar"),
]


def artikel(path, kruim, ic, h1, lead, kern, inhoud, partnerblok, verder, faq, bronnen, title, desc, prio="0.8"):
    """Standaard bespaarartikel: kop, kerncijfers, inhoud, partner, verder lezen, FAQ en bronnen."""
    ch, cld = crumbs(kruim, path)
    k = ('<div class="kerncijfers">' + "".join(f'<div><b>{a}</b><small>{b}</small></div>' for a, b in kern) + '</div>') if kern else ''
    v = '<h2>Verder lezen</h2><ul class="links">' + "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in verder) + '</ul>'
    br = ('<p class="bron">Bronnen: ' + ", ".join(f'<a href="{u}" rel="noopener">{t}</a>' for u, t in bronnen) + f'. Bijgewerkt op {BIJGEWERKT}.</p>') if bronnen else f'<p class="bron">Bijgewerkt op {BIJGEWERKT}.</p>'
    body = (ch + f'<div class="paginakop"><span class="ic">{ICON[ic]}</span><h1>{h1}</h1></div><p class="lead">{lead}</p>' + k + inhoud + partnerblok + v + faq_html(faq) + br)
    page(path, title, desc, body, [cld, faq_ld(faq)], prio=prio)


# ---------- Agenda: "Deze data niet missen" (homepage) + .ics-bestanden ----------
AGENDA = [
    ("2026-12-08", "vermogen", "Vermogen doorgeven voor zorgtoeslag en kindgebonden budget", "/kindgebonden-budget-2027/", "Geef je vermogen op 1 januari 2027 uiterlijk vandaag door in Mijn toeslagen, anders moet je later terugbetalen."),
    ("2026-12-16", "eerste-kamer", "Eerste Kamer stemt over de belastingen van 2027", "/belastingen-2027/", "Dan is duidelijk welke belastingplannen voor 2027 doorgaan."),
    ("2026-12-31", "zorg", "Laatste dag om je zorgverzekering op te zeggen", "/zorgverzekering-overstappen/", "Zeg vandaag op en sluit uiterlijk 31 januari een nieuwe verzekering af."),
    ("2026-12-31", "isde", "Warmtepomp kopen voor het hogere ISDE-bedrag", "/isde-subsidie-2027/", "Koop je lucht-waterwarmtepomp uiterlijk vandaag voor het hogere subsidiebedrag (overgangsregeling)."),
    ("2027-01-01", "salderen", "Salderen stopt voor zonnepanelen", "/salderen-2027/", "Vanaf vandaag wordt teruggeleverde stroom apart afgerekend."),
    ("2027-01-01", "camper", "Camper alleen nog half tarief met RDW-code SA", "/wegenbelasting-2027/", "Check met de RDW-kentekencheck of je camper als categorie M met code SA staat geregistreerd."),
    ("2027-01-04", "noodfonds", "Noodfonds Energie gaat open", "/noodfonds-energie-2027/", "Aanvragen kan van 4 januari tot en met 7 mei 2027: € 120 tot € 1.800 steun."),
    ("2027-03-01", "aangifte", "Belastingaangifte doen kan weer", "/belastingaangifte-tips/", "Doe je aangifte vóór 1 april, dan heb je je geld meestal vóór 1 juli."),
]
_MND = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
def _agenda_items():
    vandaag = datetime.date.today().isoformat()
    return sorted([a for a in AGENDA if a[0] >= vandaag], key=lambda a: a[0])
def _gcal(d, titel, tekst, url):
    from urllib.parse import quote
    d0 = d.replace("-", ""); d1 = (datetime.date.fromisoformat(d) + datetime.timedelta(days=1)).isoformat().replace("-", "")
    return ("https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + quote(titel) + "&dates=" + d0 + "/" + d1
            + "&details=" + quote(tekst + " Meer uitleg: " + BASE + url))
def agenda_html():
    rij = []
    for d, sid, titel, url, tekst in _agenda_items():
        dd = datetime.date.fromisoformat(d)
        rij.append(f'<li><b>{dd.day} {_MND[dd.month-1]}</b><span>{titel}</span><span class="ag-acties"><a href="{url}">Lees meer</a>'
                   f'<details class="ag-add"><summary>📅 In agenda</summary><a href="{esc(_gcal(d, titel, tekst, url))}" target="_blank" rel="noopener">Google Agenda</a>'
                   f'<a href="/agenda/{sid}.ics" download>iPhone / Outlook</a></details></span></li>')
    abon = BASE.replace("https://", "webcal://") + "/agenda/bespaarvriend.ics"
    from urllib.parse import quote as _q
    return ('<ol class="agenda">' + "".join(rij) + '</ol>'
            '<p class="ag-alles">📅 <b>Alle data automatisch in je agenda?</b> '
            f'<a href="https://calendar.google.com/calendar/r?cid={_q(abon, safe="")}" target="_blank" rel="noopener">Google Agenda</a> · '
            f'<a href="{abon}">iPhone / Outlook</a><br><small>Nieuwe data komen er vanzelf bij.</small></p>')
def _ics_event(d, sid, titel, url, tekst):
    d0 = d.replace("-", ""); d1 = (datetime.date.fromisoformat(d) + datetime.timedelta(days=1)).isoformat().replace("-", "")
    def e(x): return x.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;")
    return ("BEGIN:VEVENT\r\nUID:" + sid + "-" + d0 + "@bespaarvriend.nl\r\nDTSTAMP:" + datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            + "\r\nDTSTART;VALUE=DATE:" + d0 + "\r\nDTEND;VALUE=DATE:" + d1 + "\r\nSUMMARY:" + e(titel)
            + "\r\nDESCRIPTION:" + e(tekst + " Meer uitleg: " + BASE + url) + "\r\nURL:" + BASE + url
            + "\r\nBEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:" + e(titel) + "\r\nTRIGGER:-P1D\r\nEND:VALARM\r\nEND:VEVENT\r\n")
def schrijf_agenda():
    os.makedirs(os.path.join(OUT, "agenda"), exist_ok=True)
    kop = "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Bespaarvriend//NL\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\n"
    alles = kop + "X-WR-CALNAME:Bespaarvriend: data niet missen\r\nX-WR-TIMEZONE:Europe/Amsterdam\r\nREFRESH-INTERVAL;VALUE=DURATION:P1D\r\n"
    for a in AGENDA:
        ev = _ics_event(*a); alles += ev
        open(os.path.join(OUT, "agenda", a[1] + ".ics"), "w", newline="").write(kop + ev + "END:VCALENDAR\r\n")
    open(os.path.join(OUT, "agenda", "bespaarvriend.ics"), "w", newline="").write(alles + "END:VCALENDAR\r\n")

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
    def _tegel(u, ic, n, t, uitleg=None):
        hoofd = f'<span class="ic">{ICON[ic]}</span>{pijl}<b>{n}</b><small>{t}</small>'
        if not uitleg:
            if u.startswith("/"):  # eigen pagina met providerkeuze
                return f'<a href="{u}">{hoofd}</a>'
            return f'<a href="{u}" rel="sponsored noopener" target="_blank">{hoofd}</a>'
        return f'<div class="tegel"><a class="hoofd" href="{u}" rel="sponsored noopener" target="_blank">{hoofd}</a><a class="uitleg" href="{uitleg[0]}">{uitleg[1]}</a></div>'
    UITLEG = {"zorg": ("/zorgverzekering-2027/", "Uitleg →"), "energie": ("/energie-2027/", "Uitleg →")}
    direct = ('<div class="tegels direct" style="margin-top:20px" aria-label="Direct vergelijken">'
              + "".join(_tegel(u, ic, n, t, UITLEG.get(ic)) for u, ic, n, t in DIRECT)
              + '</div><p class="bron" style="margin-top:-6px">Advertentie: deze tegels gaan naar partners. Sluit je iets af, dan krijgt Bespaarvriend een kleine vergoeding. Jij betaalt niets extra.</p>')
    body = ('<section class="intro"><span class="euro" aria-hidden="true">€</span>'
            '<h1>Stop met te veel betalen</h1>'
            '<p class="kort">Meer overhouden, uitgelegd in gewone taal.</p>'
            '<p class="bekend">Van de maker van <a href="https://boodschappenvergelijk.nl/?bron=bespaarvriend">Boodschappenvergelijk.nl</a> · bekend van '
            '<a class="b" href="https://www.hartvannederland.nl/advies-en-tips/kopen-besparen/videos/goedkoop-boodschappen-doen-erik-bouwt-vergelijker" target="_blank" rel="noopener">Hart van Nederland</a> '
            '<a class="b" href="https://www.oost.nl/nieuws/3720144/rijssenaar-erik-beltman-rekent-af-met-dure-boodschappen-in-vergelijkingswebsite" target="_blank" rel="noopener">RTV Oost</a></p>'
            '</section>' + '<a class="uitgelicht" href="https://stroomwekker.eu/?bron=bespaarvriend"><span class="lbl">Nieuw · gratis</span><span class="gr" aria-hidden="true">⚡</span><span><b>Dynamisch contract? Je apparaten vanzelf aan als stroom goedkoop is</b><small>Stroomwekker zet je boiler, wasmachine, auto of thuisbatterij aan op de goedkoopste momenten.</small><span class="knop">Naar Stroomwekker →</span></span></a>' +
            '<h2>Waar wil je op besparen?</h2><p class="bron" style="margin-top:-4px">Per onderwerp: eerst kort uitgelegd, daarna direct vergelijken.</p><div class="tegels">'
            f'<a href="/zorgverzekering-2027/"><span class="ic">{ICON["zorg"]}</span>{pijl}<b>Zorgverzekering</b><small>Overstappen kan <strong>tot 31 december</strong></small><span class="vu">Uitleg + vergelijken</span></a>'
            f'<a href="/energie-2027/"><span class="ic">{ICON["energie"]}</span>{pijl}<b>Energie</b><small>Contract en tarieven voor 2027</small><span class="vu">Uitleg + vergelijken</span></a>'
            f'<a href="/internet-en-mobiel/"><span class="ic">{ICON["internet"]}</span>{pijl}<b>Internet en mobiel</b><small>Glasvezel, tv en sim only</small><span class="vu">Uitleg + vergelijken</span></a>'
            f'<a href="/vakantie-en-vliegen/"><span class="ic">{ICON["vlucht"]}</span>{pijl}<b>Vakantie en vliegen</b><small>Vluchten, reizen en reisverzekering</small><span class="vu">Uitleg + vergelijken</span></a>'
            f'<a href="/auto-en-tanken/"><span class="ic">{ICON["tank"]}</span>{pijl}<b>Auto en tanken</b><small>Verzekering, brandstof en banden</small><span class="vu">Uitleg + vergelijken</span></a>'
            f'<a href="/salderen-2027/"><span class="ic">{ICON["zon"]}</span>{pijl}<b>Zonnepanelen</b><small>Einde salderen: zo beperk je de schade</small><span class="vu">Uitleg + vergelijken</span></a>'
            f'<a href="/eigen-risico-2027/"><span class="ic">{ICON["risico"]}</span>{pijl}<b>Eigen risico</b><small>€ 400 in 2027, met rekenhulp</small></a>'
            f'<a href="/zorgtoeslag-2027/"><span class="ic">{ICON["toeslag"]}</span>{pijl}<b>Zorgtoeslag</b><small>Heb jij recht? Check het</small></a>'
            f'<a href="/boodschappen/"><span class="ic">{ICON["boodschappen"]}</span>{pijl}<b>Boodschappen</b><small>Vergelijken en bijhouden</small></a>'
            f'<a href="/administratie/"><span class="ic">{ICON["map"]}</span>{pijl}<b>Vaste lasten op orde</b><small>In 5 stappen overzicht</small></a>'
            '</div>'
            '<h2>Geld terug en toeslagen</h2><p class="bron" style="margin-top:-4px">Geld waar je misschien recht op hebt. Gratis, je moet het alleen aanvragen.</p><div class="tegels">'
            f'<a href="/noodfonds-energie-2027/"><span class="ic">{ICON["energie"]}</span>{pijl}<b>Noodfonds Energie</b><small>Tot € 1.800 steun</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/huurtoeslag-2027/"><span class="ic">{ICON["sleutel"]}</span>{pijl}<b>Huurtoeslag</b><small>Huur nooit meer te hoog</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/kindgebonden-budget-2027/"><span class="ic">{ICON["toeslag"]}</span>{pijl}<b>Kindgebonden budget</b><small>Check vóór 8 december</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/kinderopvangtoeslag-2027/"><span class="ic">{ICON["toeslag"]}</span>{pijl}<b>Kinderopvangtoeslag</b><small>96% tot ± € 72.000</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/isde-subsidie-2027/"><span class="ic">{ICON["zon"]}</span>{pijl}<b>ISDE subsidie</b><small>Isolatie en warmtepomp</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/belastingaangifte-tips/"><span class="ic">{ICON["bon"]}</span>{pijl}<b>Belasting terug</b><small>Aftrekposten niet vergeten</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="/bijverdienen-met-enquetes/"><span class="ic">{ICON["bon"]}</span>{pijl}<b>Bijverdienen met enquêtes</b><small>Geld of cadeaubonnen voor je mening</small><span class="nieuw">Nieuw</span></a>'
            '</div>'
            '<h2>Deze data niet missen</h2>' + agenda_html() + ''
            '<h2>Meer gratis hulpmiddelen</h2><p class="bron" style="margin-top:-4px">Ook gemaakt door Erik, net zo eerlijk en gratis.</p><div class="tegels tools">'
            f'<a href="https://stroomwekker.eu/?bron=bespaarvriend"><span class="ic">{ICON["energie"]}</span>{pijl}<b>Stroomwekker</b><small>Apparaten vanzelf aan als stroom goedkoop is</small><span class="nieuw">Nieuw</span></a>'
            f'<a href="https://allesoporde.netlify.app/"><span class="ic">{ICON["map"]}</span>{pijl}<b>Alles op orde</b><small>Al je vaste lasten en inkomsten op een rij</small></a>'
            f'<a href="https://bonnenboek.netlify.app/"><span class="ic">{ICON["bon"]}</span>{pijl}<b>Bonnenboek</b><small>Kassabonnen scannen en zien wat je uitgeeft</small></a>'
            f'<a href="https://goedkopertanken.netlify.app/"><span class="ic">{ICON["tank"]}</span>{pijl}<b>Tankwijzer</b><small>Goedkoper tanken in NL, België en Duitsland</small></a>'
            f'<a href="https://vluchtwijzer.netlify.app/"><span class="ic">{ICON["vlucht"]}</span>{pijl}<b>Vluchtwijzer</b><small>De goedkoopste vluchten vergelijken</small></a>'
            f'<a href="https://vakantietoppers.netlify.app/"><span class="ic">{ICON["koffer"]}</span>{pijl}<b>Vakantiewijzer</b><small>Pakketreizen, hotels en campings vergelijken</small></a>'
            f'<a href="https://salderingscheck-nl.netlify.app/"><span class="ic">{ICON["zon"]}</span>{pijl}<b>Salderingscheck</b><small>Wat kost het einde van salderen jou?</small></a>'
            f'<a href="https://euroroadrules.eu/"><span class="ic">{ICON["weg"]}</span>{pijl}<b>EuroRoadRules</b><small>Vignetten, tol en milieuzones in Europa</small></a>'
            f'<a href="https://foutcodezoeker.nl/"><span class="ic">{ICON["sleutel"]}</span>{pijl}<b>Foutcodezoeker</b><small>Zelf repareren in plaats van vervangen</small></a>'
            f'<a href="/elektronica/"><span class="ic">{ICON["tv"]}</span>{pijl}<b>Elektrovergelijk</b><small>Witgoed, tv\'s, laptops en telefoons vergelijken, mét verzendkosten</small><span class="nieuw">Nieuw</span></a>'
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
            f'<div class="kaart tool"><span class="ic">{ICON["energie"]}</span><div><b>Dynamisch contract? Laat het vanzelf gaan</b><p>Met <b>Stroomwekker</b> zie je de stroomprijs per kwartier en gaan je boiler, wasmachine of thuisbatterij vanzelf aan als stroom goedkoop is. Gratis, ook van de maker van Bespaarvriend.</p><a class="btn" href="https://stroomwekker.eu/?bron=bespaarvriend">Naar Stroomwekker{ICON["pijl"]}</a></div></div>'
            '<h2>Zo bespaar je in 4 stappen</h2><ol class="stappen">'
            '<li><b>Pak je jaarafrekening erbij.</b> Daarop staat je echte verbruik in kWh en m³. Vergelijken met een gemiddelde levert vaak een verkeerd beeld op.</li>'
            '<li><b>Kijk wanneer je contract afloopt.</b> Heb je een variabel contract, dan kun je altijd overstappen. Bij een vast contract kan eerder stoppen geld kosten.</li>'
            '<li><b>Vergelijk op de tarieven vanaf 2027.</b> Heb je zonnepanelen? Let dan vooral op de terugleververgoeding en de terugleverkosten vanaf 1 januari, niet alleen op de prijs per kWh.</li>'
            '<li><b>Verbruik slim.</b> Met zonnepanelen loont het om stroom te gebruiken als de zon schijnt: wasmachine, vaatwasser of auto opladen overdag.</li></ol>'
            + widget("energie", "Energie vergelijken") + dynamisch_blok("bespaarvriend-energie") + partner(awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/energievergelijken"), "Energiecontracten vergelijken", "Vergelijk contracten van alle grote leveranciers, inclusief de tarieven en terugleververgoeding vanaf 2027.", "Vergelijk energiecontracten", [("3 jaar vast", awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/energievergelijken/energiecontract-3-jaar-vast")), ("Dynamisch contract", awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/energievergelijken/dynamisch-energiecontract-vergelijken")), ("Aanbiedingen", awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/energievergelijken/energie-aanbiedingen")), ("Zonnepanelen en 2027", awin(8520, "bespaarvriend-energie", "https://www.gaslicht.com/zonnepanelen/afschaffen-salderingsregeling"))]) +
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
            +
            '<h2>Internet thuis</h2><ol class="stappen">'
            '<li><b>Zoek je einddatum op.</b> In je account of op je factuur staat wanneer je minimale looptijd afloopt. Daarna ben je maandelijks opzegbaar.</li>'
            '<li><b>Check welke snelheid je echt nodig hebt.</b> Voor streamen en thuiswerken met een paar mensen is vaak een lager pakket genoeg.</li>'
            '<li><b>Vraag je huidige provider om een beter aanbod.</b> Wie belt en zegt te willen overstappen, krijgt vaak een lagere prijs aangeboden.</li>'
            '<li><b>Stap over met de overstapservice.</b> Je nieuwe provider zegt je oude abonnement voor je op. Je kunt dit tot vier maanden voor het einde van je contract al regelen.</li></ol>'
            + widget("telecom", "Internet vergelijken") + widget("budgetmobiel", "Voordelige sim only") +
            partner(awin(8400, "bespaarvriend-internettv", "https://www.odido.nl/internet-en-tv"), "Internet en tv", "Internet en tv samen bij verschillende providers.", "Bekijk internet en tv", [("Odido", awin(8400, "bespaarvriend-internettv", "https://www.odido.nl/internet-en-tv")), ("UnitedConsumers", awin(8311, "bespaarvriend-internettv", "https://www.unitedconsumers.com/internet-en-tv/televisie"))]) +
            partner(awin(8400, "bespaarvriend-internet", "https://www.odido.nl/internet/aanbiedingen"), "Glasvezel en internet thuis", "Snel internet thuis bij verschillende providers.", "Bekijk internet thuis", [("Odido", awin(8400, "bespaarvriend-internet", "https://www.odido.nl/internet/aanbiedingen")), ("Simpel", awin(129565, "bespaarvriend-internet", "https://www.simpel.nl/internet/product/zelf-samenstellen"))]) +
            partner(awin(120541, "bespaarvriend-internet"), "Snellere wifi in huis", "Trage wifi ligt vaak aan je router, niet aan je abonnement. Een nieuwe router of mesh-systeem helpt vaak beter dan een duurder abonnement.", "Bekijk routers en mesh-wifi") +
            f'<h2>Mobiel</h2><div class="paginakop" style="margin-top:0"><span class="ic">{ICON["mobiel"]}</span><p style="margin:0">Werkt je telefoon nog goed? Dan is sim only bijna altijd de goedkoopste keuze.</p></div>'
            +
            '<div class="let"><b>Rekenvoorbeeld:</b> een nieuw-toestel-abonnement van € 45 per maand kost in 2 jaar € 1.080. Een refurbished toestel van € 350 plus 24 maanden sim only van € 8 kost € 542. Dat scheelt € 538.</div>'
            + partner(awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/"), "Refurbished telefoon met garantie", "Gebruikte telefoons, gecontroleerd en schoongemaakt, met garantie.", "Bekijk refurbished telefoons", [("iPhone 15", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/iphone-15")), ("iPhone 16", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/iphone-16")), ("iPhone 17", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/iphone-17")), ("Samsung", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/samsung")), ("iPad", awin(112024, "bespaarvriend-mobiel", "https://www.refurbished.nl/ipad"))]) +
            '<ul class="links"><li>Kijk in je account hoeveel data je echt gebruikt. Veel mensen betalen voor een bundel die ze niet halen.</li>'
            '<li>Maandelijks opzegbaar kost vaak € 1 tot € 4 per maand meer dan een jaarcontract.</li>'
            '<li>Reken met de gemiddelde prijs over de hele looptijd, niet met de actieprijs.</li></ul>'
            + partner(awin(8389, "bespaarvriend-toestel", "https://www.odido.nl/shop/alle-telefoons"), "Telefoon met abonnement", "Een nieuwe telefoon met abonnement, betaald per maand.", "Bekijk telefoons", [("Odido", awin(8389, "bespaarvriend-toestel", "https://www.odido.nl/shop/alle-telefoons")), ("Ben", awin(8313, "bespaarvriend-toestel", "https://www.ben.nl/telefoons"))])
            + partner(awin(8313, "bespaarvriend-simonly", "https://www.ben.nl/sim-only"), "Sim only", "Sim only bij verschillende providers: kies zelf je bundel en looptijd.", "Bekijk sim only", [("Ben", awin(8313, "bespaarvriend-simonly", "https://www.ben.nl/sim-only")), ("Odido", awin(8389, "bespaarvriend-simonly", "https://www.odido.nl/mobiel-abonnement/sim-only")), ("Simpel", awin(8424, "bespaarvriend-simonly", "https://www.simpel.nl/sim-only")), ("UnitedConsumers", awin(8311, "bespaarvriend-simonly", "https://www.unitedconsumers.com/mobiel")), ("Lycamobile", "https://bdt9.net/c/?si=19078&amp;li=1819944&amp;wi=449774&amp;ws=bespaarvriend-simonly&amp;dl=nl%2Fsim-only%2F"), ("Budget Thuis", "#w-budgetmobiel")])
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
            + partner(dc("glp8.net", 20811, 1881767, "bespaarvriend-vakantie"), "Vakantiehuis huren", "Vakantiehuizen, hotels en complete reizen op één plek, met prijsgarantie.", "Bekijk vakantiehuizen")
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
            '<div class="let"><b>Nieuw in 2027:</b> elektrische auto’s houden 30% korting op de wegenbelasting, en een camper krijgt het halve tarief alleen nog met de juiste RDW-registratie. <a href="/wegenbelasting-2027/">Lees wat je moet checken →</a></div>'
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
    body = (ch + '<h1>Privacy</h1><div class="kaart"><p style="margin-top:0">Bespaarvriend gebruikt geen cookies en geen trackers die je volgen. Sommige pagina’s hebben partnerlinks; die staan altijd als advertentie gemarkeerd. Klik je op zo’n link, dan gelden op de site van de partner hun eigen privacy- en cookieregels.</p>'
            '<p>Om te zien hoeveel mensen de site bezoeken, gebruiken we GoatCounter. Dat telt alleen paginabezoeken, zonder cookies en zonder je IP-adres op te slaan. We kunnen jou daarmee niet volgen of herkennen.</p>'
            '<p>De rekenhulpen werken helemaal in je eigen browser: wat je invult, wordt nergens naartoe gestuurd of bewaard.</p>'
            '<p>Stuur je een bericht via de contactpagina, dan bewaren we je bericht (en je naam en e-mailadres als je die invult) alleen om je te kunnen antwoorden. '
            'We delen het met niemand en verwijderen het als het niet meer nodig is.</p><p style="margin-bottom:0">De site draait bij Netlify. Netlify houdt voor de beveiliging korte tijd technische gegevens bij, zoals IP-adressen.</p></div>')
    page("/privacy/", "Privacy | Bespaarvriend", "Bespaarvriend gebruikt geen cookies en geen trackers die je volgen. Rekenhulpen werken in je eigen browser.", body, [cld], prio="0.2")

    # ---------- Auteursrecht en gebruiksvoorwaarden ----------
    ch, cld = crumbs("Gebruiksvoorwaarden", "/gebruiksvoorwaarden/")
    body = (ch + '<h1>Auteursrecht en gebruiksvoorwaarden</h1><p class="lead">Kort gezegd: citeren mag met bronvermelding en een link. Overnemen of hergebruiken alleen met toestemming. Bespaarvriend geeft uitleg, geen persoonlijk financieel advies.</p>'
            '<div class="kaart"><h2 style="margin-top:0">Auteursrecht</h2><p>Alle inhoud van deze website (teksten, rekenhulpen, overzichten, ontwerp en broncode) is beschermd door het auteursrecht en/of het databankenrecht. '
            'Niets mag zonder voorafgaande schriftelijke toestemming worden verveelvoudigd, openbaar gemaakt of hergebruikt, ook niet geautomatiseerd (scrapen). Citeren mag met bronvermelding en een link naar deze website.</p>'
            f'<p style="margin-bottom:0">© {datetime.date.today().year} Bespaarvriend – Erik Beltman. Alle rechten voorbehouden.</p></div>'
            '<h2>Toestemming vragen</h2><p>Wil je iets van deze site gebruiken of overnemen? Vraag het eerst via de <a href="/contact/">contactpagina</a>. Je krijgt zo snel mogelijk antwoord.</p>'
            '<h2>Geen persoonlijk financieel advies</h2><p>Bespaarvriend legt in gewone taal uit hoe regels, premies en tarieven werken, met bronnen. Dat is algemene informatie, geen persoonlijk advies over een financieel product. '
            'Bespaarvriend heeft geen vergunning van de AFM en bemiddelt niet in verzekeringen of andere financiële producten. Twijfel je over je eigen situatie? Vraag dan advies aan een onafhankelijk adviseur.</p>'
            '<h2>Partnerlinks en advertenties</h2><p>Sommige tegels en blokken gaan naar partners. Die staan altijd gemarkeerd als advertentie. Sluit je via zo’n link iets af, dan krijgt Bespaarvriend een kleine vergoeding van de partner. Jij betaalt daarvoor niets extra. '
            'Partners hebben geen invloed op de uitleg op deze site. Op de site van de partner gelden de voorwaarden en het privacybeleid van die partner.</p>'
            '<h2>Rekenhulpen</h2><p>De rekenhulpen geven een indicatie op basis van wat je zelf invult. De uitkomst is geen garantie en geen advies. Wat je invult, blijft in je eigen browser.</p>'
            '<h2>Geen garantie</h2><p>We doen ons best om alles juist en actueel te houden en vermelden steeds onze bronnen. Toch kunnen bedragen, regels of voorwaarden veranderen of kan er een fout in staan. '
            'De voorwaarden van je verzekeraar, leverancier of de overheid zijn altijd leidend. Aan de informatie op deze site kun je geen rechten ontlenen. Bespaarvriend is niet aansprakelijk voor schade door het gebruik van deze site of van sites waar we naar linken.</p>'
            '<h2>Links naar deze site</h2><p>Links naar Bespaarvriend zijn welkom, ook zonder toestemming.</p>')
    page("/gebruiksvoorwaarden/", "Auteursrecht en gebruiksvoorwaarden | Bespaarvriend", "Alle inhoud van Bespaarvriend is beschermd door het auteursrecht en het databankenrecht. Citeren mag met bronvermelding en een link. Geen persoonlijk financieel advies.", body, [cld], prio="0.2")

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
             ("Wanneer zijn de premies van de aanvullende verzekering 2027 bekend?", "Zorgverzekeraars maken de premies van de aanvullende verzekeringen sinds 19 november 2026 bekend, een week na de premies van de basisverzekering. Je kunt basis en aanvullend nu samen vergelijken."),
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
            '<div class="let"><b>De premies voor 2027 zijn bekend.</b> Je kunt basis en aanvullend nu samen vergelijken. Overstappen kan tot 31 december.</div>'
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

    # ---------- Tweede reeks artikelen ----------
    ZV = ZORG_VERGELIJKER
    artikel("/zorgverzekering-overstappen/", "Zorgverzekering overstappen", "zorg",
        "Zorgverzekering overstappen voor 2027: zo doe je het",
        "Overstappen kan nog tot 31 december. Je nieuwe verzekeraar regelt de opzegging meestal voor je. Zo pak je het in 5 stappen aan.",
        [("31 dec", "laatste dag opzeggen"), ("31 jan", "uiterlijk nieuwe verzekering afsluiten"), ("€ 649", "verschil laagste en hoogste premie per jaar"), ("1 jan", "nieuwe verzekering gaat in")],
        '<h2>Overstappen in 5 stappen</h2><ol class="stappen">'
        '<li><b>Bekijk je jaaroverzicht.</b> Welke zorg had je dit jaar en wat kreeg je vergoed? Dan weet je wat je nodig hebt.</li>'
        '<li><b>Kies natura of restitutie.</b> Een naturapolis is goedkoper, maar bij een zorgverlener zonder contract krijg je soms minder vergoed.</li>'
        '<li><b>Vergelijk basis en aanvullend samen.</b> De premies van de aanvullende verzekeringen voor 2027 zijn bekend.</li>'
        '<li><b>Sluit de nieuwe verzekering af</b> vóór 1 januari. Heb je zelf vóór 31 december opgezegd, dan heb je tot 31 januari de tijd.</li>'
        '<li><b>Controleer de bevestiging.</b> Meestal zegt je nieuwe verzekeraar je oude polis op. Staat dat er niet, zeg dan zelf op vóór 31 december.</li></ol>'
        '<div class="let"><b>Let op met een aanvullende verzekering.</b> Voor de basisverzekering word je altijd geaccepteerd. Voor een uitgebreid aanvullend pakket kan een verzekeraar een gezondheidsverklaring vragen. Zeg je oude polis pas op als je zeker bent dat je nieuwe aanvraag is goedgekeurd.</div>'
        '<h2>Hoeveel kun je besparen?</h2><p>Tussen de laagste en de hoogste premie voor de basisverzekering zit in 2027 € 649 per jaar, voor dezelfde basiszorg. Met z’n tweeën loopt dat op tot bijna € 1.300 per jaar. Kinderen tot 18 jaar zijn gratis meeverzekerd.</p>',
        ZV,
        [("/zorgverzekering-2027/", "Zorgverzekering 2027: premies en verschillen"), ("/aanvullende-verzekering-2027/", "Aanvullende verzekering 2027: nodig of niet?"), ("/tandartsverzekering-2027/", "Tandartsverzekering 2027"), ("/eigen-risico-2027/", "Eigen risico 2027")],
        [("Moet ik mijn oude zorgverzekering zelf opzeggen?", "Meestal niet. De nieuwe verzekeraar zegt je oude verzekering op via de overstapservice. Controleer dit in je bevestiging. Staat het er niet in, zeg dan zelf op vóór 31 december."),
         ("Tot wanneer kan ik overstappen van zorgverzekering?", "Zeg je huidige verzekering uiterlijk 31 december 2026 op. Sluit daarna uiterlijk 31 januari 2027 een nieuwe af; die gaat met terugwerkende kracht in op 1 januari 2027."),
         ("Kan ik geweigerd worden bij een nieuwe zorgverzekeraar?", "Voor de basisverzekering niet: iedere verzekeraar moet je accepteren. Voor een aanvullende verzekering kan een verzekeraar soms een gezondheidsverklaring vragen."),
         ("Moet ik mijn kinderen apart overzetten?", "Kinderen tot 18 jaar zijn gratis meeverzekerd bij een van de ouders. Stap je over, geef je kinderen dan mee op bij je nieuwe verzekeraar.")],
        [("https://www.overstappen.nl/nieuws/zorgpremies-2027-bekend-alle-polissen-duurder-premiekloof-stijgt-naar-649-euro-per-jaar/", "Overstappen.nl (premies 2027)"), ("https://www.overstappen.nl/zorgverzekering/zorgverzekering-2027/", "Overstappen.nl (data overstappen)"), ("https://www.rabobank.nl/particulieren/verzekering/zorgverzekering/tips-voor-je-zorgverzekering", "Rabobank (aanvullende premies 19 november)")],
        "Zorgverzekering overstappen 2027: stappenplan en deadlines", "Zorgverzekering overstappen voor 2027: opzeggen vóór 31 december, nieuwe polis uiterlijk 31 januari. Stappenplan, valkuilen en tot € 649 per jaar verschil.", prio="0.9")

    artikel("/fysiotherapie-vergoeding-2027/", "Fysiotherapie vergoeding 2027", "zorg",
        "Fysiotherapie vergoeding 2027: wat betaal je zelf?",
        "Voor volwassenen zit fysiotherapie meestal niet in de basisverzekering. Of je een aanvullende verzekering nodig hebt, hangt af van hoe vaak je gaat.",
        [("21e", "behandeling: vanaf dan basis, bij een chronische aandoening"), ("9", "behandelingen voor kinderen uit de basis (soms 9 extra)"), ("0", "vergoeding uit de basis na een ongeval (volwassenen)"), ("19 nov", "premies aanvullend 2027 bekend")],
        '<h2>Wat vergoedt de basisverzekering?</h2><table><tr><th>Situatie</th><th>Basisverzekering</th></tr>'
        '<tr><td>Volwassene, gewone klachten (rug, knie, schouder)</td><td>Geen vergoeding. Alleen via een aanvullende verzekering</td></tr>'
        '<tr><td>Volwassene met een aandoening op de chronische lijst</td><td>Vanaf de 21e behandeling. De eerste 20 betaal je zelf of via je aanvullende verzekering</td></tr>'
        '<tr><td>Kind tot 18 jaar</td><td>De eerste 9 behandelingen per aandoening, eventueel nog 9 extra</td></tr>'
        '<tr><td>Tijdens een ziekenhuisopname</td><td>Valt onder de ziekenhuiszorg</td></tr>'
        '<tr><td>Na een ongeval (volwassene)</td><td>Geen vergoeding uit de basis</td></tr></table>'
        '<h2>Loont een aanvullende verzekering met fysio?</h2><p>Eén behandeling kost al snel meer dan een maand premie. Ga je regelmatig, of herstel je van een blessure of operatie, dan kan een pakket met genoeg behandelingen lonen. '
        'Ga je bijna nooit, dan ben je vaak goedkoper uit als je een losse behandeling zelf betaalt.</p>'
        '<ul class="links"><li><b>Kijk naar het aantal behandelingen</b> per jaar, niet alleen naar de premie.</li><li><b>Kies een gecontracteerde fysiotherapeut.</b> Bij een therapeut zonder contract krijg je vaak maar een deel vergoed, bijvoorbeeld 75%.</li>'
        '<li><b>Ongebruikte behandelingen meenemen</b> naar volgend jaar kan bij sommige verzekeraars, als je dezelfde aanvullende verzekering houdt.</li></ul>',
        ZV,
        [("/aanvullende-verzekering-2027/", "Aanvullende verzekering 2027: rekenhulp"), ("/zorgverzekering-overstappen/", "Zorgverzekering overstappen: stappenplan"), ("/eigen-risico-2027/", "Eigen risico 2027")],
        [("Wordt fysiotherapie vergoed uit de basisverzekering in 2027?", "Voor volwassenen alleen bij een aandoening op de lijst met chronische aandoeningen, en dan vanaf de 21e behandeling. Andere fysiotherapie betaal je zelf of via een aanvullende verzekering."),
         ("Hoeveel fysiotherapie krijgen kinderen vergoed?", "Kinderen tot 18 jaar krijgen de eerste 9 behandelingen per aandoening vergoed uit de basisverzekering, en zo nodig nog 9 extra."),
         ("Gaat fysiotherapie af van mijn eigen risico?", "Fysiotherapie uit de basisverzekering valt voor volwassenen onder het eigen risico. Vergoeding uit een aanvullende verzekering gaat niet van je eigen risico af."),
         ("Kan ik ongebruikte fysiobehandelingen meenemen naar 2027?", "Bij sommige verzekeraars wel, als je in 2027 weer een aanvullende verzekering met fysiotherapie hebt. De voorwaarden verschillen per verzekeraar.")],
        [("https://www.rijksoverheid.nl/onderwerpen/zorgverzekering/vraag-en-antwoord/is-fysiotherapie-opgenomen-in-het-basispakket", "Rijksoverheid"), ("https://www.consumentenbond.nl/zorgverzekering/vergoedingen/fysiotherapie", "Consumentenbond"), ("https://www.overstappen.nl/zorgverzekering/vergoedingen/fysiotherapie-na-een-ongeval/", "Overstappen.nl (na een ongeval)"), ("https://www.zorgwijzer.nl/zorgverzekering-2026/ongebruikte-fysio-meenemen-naar-volgend-jaar-het-kan-bij-deze-verzekeraars", "Zorgwijzer (behandelingen meenemen)")],
        "Fysiotherapie vergoeding 2027: basis of aanvullend?", "Fysiotherapie 2027: volwassenen krijgen uit de basis alleen vergoeding bij een chronische aandoening, vanaf de 21e behandeling. Kinderen 9 behandelingen. Zo kies je.")

    reis = partner(awin(78144, "bespaarvriend-reis", "https://www.hansemerkur.nl/reisverzekeringen"), "Reisverzekering", "Een reisverzekering voor één reis of het hele jaar, ook voor wintersport en lange reizen.", "Bekijk reisverzekeringen",
                   [("Doorlopend", awin(78144, "bespaarvriend-reis", "https://www.hansemerkur.nl/reisverzekeringen/doorlopende-reisverzekering")), ("Eén reis", awin(78144, "bespaarvriend-reis", "https://www.hansemerkur.nl/reisverzekeringen/kortlopende-reisverzekering")), ("Wintersport", awin(78144, "bespaarvriend-reis", "https://www.hansemerkur.nl/reisverzekeringen/wintersportverzekering"))])
    artikel("/reisverzekering-doorlopend-of-kortlopend/", "Doorlopend of kortlopend", "koffer",
        "Doorlopende of kortlopende reisverzekering: wat is goedkoper?",
        "Ga je één keer per jaar weg, of vaker? Dat bepaalt grotendeels welke reisverzekering voordeliger is.",
        [("1×", "per jaar weg: kortlopend vaak voordeliger"), ("16–21", "dagen per jaar: vanaf daar meestal doorlopend"), ("Zelfde", "dekking bij beide soorten"), ("Poliskosten", "betaal je bij kortlopend elke keer")],
        '<h2>Het verschil</h2><table><tr><th></th><th>Kortlopend</th><th>Doorlopend</th></tr>'
        '<tr><td>Geldig</td><td>Voor één reis</td><td>Het hele jaar, voor elke reis</td></tr>'
        '<tr><td>Premie</td><td>Per reis, plus poliskosten</td><td>Per maand of per jaar</td></tr>'
        '<tr><td>Past bij</td><td>Eén vakantie per jaar, korter dan 2 à 3 weken</td><td>Meerdere reizen of weekendjes weg per jaar</td></tr>'
        '<tr><td>Opzeggen</td><td>Stopt vanzelf</td><td>Loopt door tot je opzegt</td></tr></table>'
        '<h2>Heb je wel een reisverzekering nodig?</h2><p>Je zorgverzekering vergoedt spoedeisende zorg in het buitenland, maar meestal tot het Nederlandse tarief. In landen waar zorg duurder is betaal je het verschil zelf. Een terugreis naar Nederland na een ongeluk (repatriëring) vergoedt de zorgverzekering niet. '
        'Een reisverzekering dekt daarnaast bagage en hulp onderweg.</p>'
        '<h2>Zo bespaar je op je reisverzekering</h2><ul class="links"><li><b>Voorkom dubbele dekking.</b> Zijn je spullen al via je inboedelverzekering verzekerd? Dan heb je misschien geen bagagedekking nodig.</li>'
        '<li><b>Kies het juiste gebied.</b> Europa-dekking is goedkoper dan werelddekking.</li>'
        '<li><b>Wintersport alleen als je gaat.</b> Een wintersportdekking kun je vaak per jaar aan- of uitzetten.</li>'
        '<li><b>Annulering apart afwegen.</b> Sluit je reis- en annuleringsverzekering tegelijk af bij dezelfde verzekeraar, dan betaal je vaak maar één keer poliskosten.</li></ul>',
        reis,
        [("/vakantie-en-vliegen/", "Goedkoper op vakantie en vliegen"), ("/goedkoop-vliegen/", "Goedkoop vliegen: 8 tips")],
        [("Vanaf hoeveel reisdagen is een doorlopende reisverzekering goedkoper?", "Als richtlijn vanaf ongeveer 16 tot 21 vakantiedagen per jaar. Ga je één keer per jaar korter dan 2 à 3 weken op reis, dan is kortlopend vaak voordeliger."),
         ("Is de dekking van een kortlopende reisverzekering anders?", "Nee, meestal is de dekking hetzelfde. Het verschil zit in de looptijd en de manier van betalen."),
         ("Tot wanneer kan ik een kortlopende reisverzekering afsluiten?", "Tot vlak voor vertrek, meestal nog tot de dag voordat je weggaat."),
         ("Vergoedt mijn zorgverzekering zorg in het buitenland?", "Spoedeisende zorg wel, meestal tot het Nederlandse tarief. Is zorg in het buitenland duurder, of moet je na een ongeluk naar huis worden vervoerd, dan heb je een reisverzekering nodig.")],
        [("https://www.consumentenbond.nl/reisverzekering/kortlopend-of-doorlopend", "Consumentenbond"), ("https://www.vanbruggen.nl/verzekeringen/reisverzekering-annuleringsverzekering", "Van Bruggen (16–21 dagen)"), ("https://www.unive.nl/reisverzekering/soorten-reisverzekering", "Univé (poliskosten)"), ("https://hellosafe.com/nl/travel-insurance/single-trip", "HelloSafe (zorg in het buitenland)")],
        "Doorlopende of kortlopende reisverzekering: wat is goedkoper?", "Doorlopend of kortlopend? Eén reis per jaar: vaak kortlopend. Vanaf zo’n 16 tot 21 vakantiedagen per jaar: meestal doorlopend. Plus tips om dubbele dekking te voorkomen.")

    vlieg = partner(awin(63484, "bespaarvriend-vliegen", "https://www.vliegwinkel.nl/"), "Vliegtickets boeken", "Vluchten van meer dan 800 luchtvaartmaatschappijen, ook als vlucht + hotel. Let op bagage en boekingskosten voordat je betaalt.", "Bekijk vliegtickets")
    artikel("/goedkoop-vliegen/", "Goedkoop vliegen", "vlucht",
        "Goedkoop vliegen: 8 tips die echt schelen",
        "De prijs van een vliegticket hangt af van je dag, je vliegveld en wat je allemaal meeneemt. Met deze tips betaal je minder.",
        [],
        '<h2>8 tips</h2><ol class="stappen">'
        '<li><b>Wees flexibel met je datum.</b> Een dag eerder of later vertrekken scheelt vaak meer dan je denkt. Kijk naar een paar dagen rond je gewenste datum.</li>'
        '<li><b>Vergelijk vliegvelden.</b> Eindhoven, Rotterdam, Brussel, Charleroi, Düsseldorf of Weeze zijn soms goedkoper dan Schiphol. Reken wel de reiskosten en het parkeren mee.</li>'
        '<li><b>Vermijd de schoolvakanties</b> als dat kan. In de vakantieweken zijn tickets duurder.</li>'
        '<li><b>Reken met de totaalprijs.</b> Ruimbagage, stoelkeuze en boekingskosten maken een goedkoop ticket soms duurder dan een ander.</li>'
        '<li><b>Reis met handbagage.</b> Wie alleen handbagage meeneemt, betaalt bij veel maatschappijen het minst.</li>'
        '<li><b>Boek niet te laat.</b> Voor populaire bestemmingen in het hoogseizoen lopen de prijzen vaak op naarmate de vertrekdatum nadert.</li>'
        '<li><b>Kijk naar enkele reizen.</b> Heen met de ene en terug met de andere maatschappij is soms goedkoper dan een retour.</li>'
        '<li><b>Let op extra kosten op de bestemming</b>, zoals een huurauto of mobiel internet buiten de EU. Regel die vooraf.</li></ol>'
        '<div class="kaart tool"><span class="ic">' + ICON["vlucht"] + '</span><div><b>Vergelijk vluchten met Vluchtwijzer</b><p>Gratis app die vluchten vanaf meerdere vliegvelden tegelijk vergelijkt.</p><a href="https://vluchtwijzer.netlify.app/">Open Vluchtwijzer →</a></div></div>',
        vlieg,
        [("/vakantie-en-vliegen/", "Goedkoper op vakantie en vliegen"), ("/reisverzekering-doorlopend-of-kortlopend/", "Doorlopende of kortlopende reisverzekering")],
        [("Op welke dag is vliegen het goedkoopst?", "Dat verschilt per route. Midden in de week en op minder populaire tijden is vliegen vaak goedkoper dan op vrijdag of zondag. Vergelijk daarom een paar dagen rond je gewenste datum."),
         ("Is vliegen vanaf Duitsland of België goedkoper?", "Soms wel. Vanaf Düsseldorf, Weeze, Brussel of Charleroi zijn tickets soms goedkoper dan vanaf Schiphol. Reken de reis naar het vliegveld en het parkeren mee voordat je kiest."),
         ("Waarom is mijn ticket bij het afrekenen duurder?", "Door extra’s zoals ruimbagage, stoelkeuze en boekingskosten. Vergelijk daarom altijd de totaalprijs met de bagage die je echt meeneemt.")],
        [("https://vluchtwijzer.netlify.app/", "Vluchtwijzer (vluchten vanaf meerdere vliegvelden vergelijken)")],
        "Goedkoop vliegen: 8 tips om minder te betalen voor je ticket", "Goedkoop vliegen: flexibel met je datum, vliegvelden in België en Duitsland vergelijken, reizen met handbagage en rekenen met de totaalprijs. 8 tips.")

    refurb = partner(awin(112024, "bespaarvriend-refurbished", "https://www.refurbished.nl/"), "Refurbished telefoon met garantie", "Gebruikte telefoons, gecontroleerd en schoongemaakt, met garantie.", "Bekijk refurbished telefoons",
                     [("iPhone", awin(112024, "bespaarvriend-refurbished", "https://www.refurbished.nl/iphone-13")), ("Samsung", awin(112024, "bespaarvriend-refurbished", "https://www.refurbished.nl/samsung")), ("iPad", awin(112024, "bespaarvriend-refurbished", "https://www.refurbished.nl/ipad"))])
    artikel("/refurbished-telefoon-kopen/", "Refurbished telefoon kopen", "mobiel",
        "Refurbished telefoon kopen: hier let je op",
        "Een refurbished telefoon is gebruikt, nagekeken en schoongemaakt, en kost een stuk minder dan nieuw. Maar 'refurbished' is geen beschermd begrip. Let daarom op deze punten.",
        [("6 mnd–3 jr", "garantie, verschilt per verkoper"), ("14 dagen", "bedenktijd bij online kopen"), ("Accu", "het onderdeel dat het eerst slijt"), ("Updates", "check tot wanneer het model ze krijgt")],
        '<h2>Waar let je op?</h2><ul class="links">'
        '<li><b>Garantie.</b> Die loopt per verkoper uiteen van zo’n 6 maanden tot 3 jaar. Daarnaast heb je altijd recht op de wettelijke garantie: een product moet doen wat je ervan mag verwachten.</li>'
        '<li><b>De accu.</b> Een goede verkoper vermeldt de conditie van de accu of vervangt hem. Vraag ernaar als het er niet bij staat.</li>'
        '<li><b>Software-updates.</b> Kijk tot wanneer het model nog updates krijgt. Een goedkoop oud toestel zonder updates is minder veilig.</li>'
        '<li><b>De staat.</b> Lees wat de verkoper bedoelt met termen als “als nieuw” of “zichtbaar gebruikt”.</li>'
        '<li><b>De prijs.</b> Vergelijk met de prijs van nieuw. Betaal nooit (bijna) de nieuwprijs voor een refurbished toestel.</li></ul>'
        '<h2>Refurbished of tweedehands van een particulier?</h2><p>Bij een particulier heb je meestal geen garantie en weet je niet of het toestel gebreken heeft. Bij een refurbished verkoper is het toestel gecontroleerd en heb je garantie en, als je online koopt, 14 dagen bedenktijd.</p>'
        '<div class="let"><b>Rekenvoorbeeld:</b> een nieuw-toestel-abonnement van € 45 per maand kost in 2 jaar € 1.080. Een refurbished toestel van € 350 plus 24 maanden sim only van € 8 kost samen € 542.</div>',
        refurb,
        [("/internet-en-mobiel/", "Internet en mobiel: stop met te veel betalen"), ("/sim-only-overstappen/", "Sim only overstappen met nummerbehoud")],
        [("Heb ik garantie op een refurbished telefoon?", "Ja. De verkoper geeft meestal een eigen garantie van 6 maanden tot 3 jaar. Daarnaast heb je recht op de wettelijke garantie, die afhangt van wat je redelijkerwijs van het toestel mag verwachten."),
         ("Mag ik een refurbished telefoon terugsturen?", "Koop je online bij een webshop, dan heb je 14 dagen bedenktijd. Je kunt het toestel dan zonder reden terugsturen."),
         ("Wat is het verschil tussen refurbished en tweedehands?", "Een refurbished toestel is door een bedrijf gecontroleerd, schoongemaakt en waar nodig gerepareerd, en wordt met garantie verkocht. Een tweedehands toestel van een particulier is dat meestal niet.")],
        [("https://www.consumentenbond.nl/tablet/kooptips-refurbished", "Consumentenbond (garantie)"), ("https://radar.avrotros.nl/hulp-tips/hulpartikelen/item/nieuwe-telefoon-nodig-zo-bespaar-je-geld/", "Radar (geen wettelijke definitie)"), ("https://www.bnnvara.nl/kassa/artikelen/wat-mag-je-verwachten-van-een-refurbished-artikel", "Kassa (bedenktijd)"), ("https://www.nieuwemobiel.nl/telefoons/keuzehulp/refurbished-of-nieuw", "NieuweMobiel (accu en updates)")],
        "Refurbished telefoon kopen: garantie, accu en waar je op let", "Refurbished telefoon kopen? Let op garantie (6 maanden tot 3 jaar), de accu, software-updates en de prijs. Met 14 dagen bedenktijd online. Zo koop je slim.")

    auto = partner(awin(8311, "bespaarvriend-autoverzekering", "https://www.unitedconsumers.com/autoverzekering"), "Autoverzekering met korting", "Een autoverzekering met collectieve korting op de premie. Vul je kenteken in en zie direct wat je betaalt.", "Bereken je premie") + partner(awin(8599, "bespaarvriend-autoverzekering2"), "Autoverzekeringen vergelijken", "Vergelijk de premies van veel autoverzekeraars naast elkaar, met de dekking die bij jouw auto past.", "Vergelijk autoverzekeringen")
    artikel("/autoverzekering-besparen/", "Autoverzekering besparen", "tank",
        "Besparen op je autoverzekering: past je dekking nog?",
        "Veel automobilisten houden te lang vast aan een allriskverzekering voor een auto die steeds minder waard wordt. Met de juiste dekking betaal je vaak flink minder.",
        [("WA", "wettelijk verplicht"), ("0–6 jr", "auto: allrisk gebruikelijk"), ("6–10 jr", "auto: beperkt casco"), ("10+ jr", "auto: vaak alleen WA")],
        '<h2>Welke dekking past bij je auto?</h2><table><tr><th>Dekking</th><th>Wat is verzekerd</th><th>Vaak gekozen bij</th></tr>'
        '<tr><td><b>WA</b></td><td>Schade die je anderen toebrengt</td><td>Auto van 10 jaar of ouder</td></tr>'
        '<tr><td><b>Beperkt casco (WA+)</b></td><td>Plus onder meer diefstal, brand, storm en ruitschade aan je eigen auto</td><td>Auto van 6 tot 10 jaar</td></tr>'
        '<tr><td><b>Allrisk</b></td><td>Plus schade aan je eigen auto die je zelf veroorzaakt</td><td>Nieuwe auto tot 6 jaar</td></tr></table>'
        '<h2>5 manieren om te besparen</h2><ol class="stappen">'
        '<li><b>Verlaag je dekking als je auto ouder wordt.</b> Kijk elk jaar of de premie nog in verhouding staat tot de waarde van je auto.</li>'
        '<li><b>Kies een hoger eigen risico</b> bij casco. Bij WA is er geen eigen risico.</li>'
        '<li><b>Geef je kilometers eerlijk op.</b> Rijd je minder dan vroeger, pas dat dan aan: dat kan de premie verlagen.</li>'
        '<li><b>Schrap overbodige extra’s</b>, zoals pechhulp als je die al via een ander abonnement hebt.</li>'
        '<li><b>Vergelijk elk jaar.</b> Let op: bij sommige verzekeraars kun je in het eerste jaar niet zomaar naar een lagere dekking.</li></ol>'
        '<div class="kaart tool"><span class="ic">' + ICON["tank"] + '</span><div><b>Ook besparen op tanken?</b><p>Tankwijzer vergelijkt brandstofprijzen in Nederland, België en Duitsland.</p><a href="https://goedkopertanken.netlify.app/">Open Tankwijzer →</a></div></div>',
        auto,
        [("/auto-en-tanken/", "Auto en tanken: brandstof en banden")],
        [("Wanneer stap ik over van allrisk naar beperkt casco?", "Als vuistregel bij een auto van ongeveer 6 jaar oud. Bij een auto van 10 jaar of ouder kiezen veel mensen voor alleen WA. Kijk vooral naar de waarde van je auto ten opzichte van de premie."),
         ("Heeft een WA-verzekering een eigen risico?", "Nee. Een eigen risico geldt alleen bij beperkt casco en allrisk."),
         ("Kan ik mijn autoverzekering tussentijds wijzigen?", "Vaak wel, maar bij sommige verzekeraars kun je in het eerste jaar niet van allrisk naar een lagere dekking. Kijk in je polisvoorwaarden.")],
        [("https://www.consumentenbond.nl/autoverzekering/beperkt-casco", "Consumentenbond (dekking per leeftijd auto)"), ("https://www.consumentenbond.nl/autoverzekering/tussentijds-wijzigen", "Consumentenbond (tussentijds wijzigen)"), ("https://www.overstappen.nl/autoverzekering/wijzigen/", "Overstappen.nl (eerste jaar)"), ("https://autorai.nl/autoverzekeringen-vergelijken-5-handige-tips", "AutoRAI (eigen risico)")],
        "Besparen op je autoverzekering: WA, beperkt casco of allrisk?", "Bespaar op je autoverzekering: tot 6 jaar allrisk, 6 tot 10 jaar beperkt casco, ouder vaak alleen WA. Plus 5 tips: eigen risico, kilometers en overbodige extra’s.")

    sim = widget("budgetmobiel", "Voordelige sim only") + partner(awin(8313, "bespaarvriend-simonly", "https://www.ben.nl/sim-only"), "Sim only", "Sim only bij verschillende providers: kies zelf je bundel en looptijd.", "Bekijk sim only", [("Ben", awin(8313, "bespaarvriend-simonly", "https://www.ben.nl/sim-only")), ("Odido", awin(8389, "bespaarvriend-simonly", "https://www.odido.nl/mobiel-abonnement/sim-only")), ("Simpel", awin(8424, "bespaarvriend-simonly", "https://www.simpel.nl/sim-only")), ("UnitedConsumers", awin(8311, "bespaarvriend-simonly", "https://www.unitedconsumers.com/mobiel")), ("Lycamobile", "https://bdt9.net/c/?si=19078&amp;li=1819944&amp;wi=449774&amp;ws=bespaarvriend-simonly&amp;dl=nl%2Fsim-only%2F"), ("Budget Thuis", "#w-budgetmobiel")])
    artikel("/belastingen-2027/", "Belastingen 2027", "bon",
        "Belastingen 2027: wat verandert er voor jou? Simpel uitgelegd",
        "Elk jaar veranderen er belastingen. Hier lees je in gewone woorden wat er in 2027 verandert voor je geld, je auto en je vakantie. En wat al zeker is, en wat nog niet.",
        [("Bijna zeker", "de Tweede Kamer zei al ja"), ("± 16 dec", "dan stemt de Eerste Kamer"), ("± € 60.280", "spaargeld zonder belasting, per persoon"), ("1 jan 2027", "dan gaat het meeste in")],
        '<h2>Is het al zeker?</h2>'
        '<p>Nog niet helemaal. Zo werkt het:</p><ol class="stappen">'
        '<li><b>De regering maakt een plan.</b> Dat heet het Belastingplan. Het werd op Prinsjesdag (september) gepresenteerd.</li>'
        '<li><b>De Tweede Kamer stemt.</b> Dat gebeurde op 12 november 2026. De Tweede Kamer zei ja.</li>'
        '<li><b>De Eerste Kamer stemt.</b> Dat gebeurt rond 16 december 2026. Meestal zegt de Eerste Kamer ook ja, maar dat is niet gegarandeerd.</li>'
        '<li><b>Daarna is het wet.</b> De meeste veranderingen gaan dan in op 1 januari 2027.</li></ol>'
        '<p>Op deze pagina zie je per onderwerp of het <b>al vaststaat</b> of <b>nog een plan</b> is. Na de stemming in december werken wij de pagina bij.</p>'
        '<h2>Spaargeld en beleggingen</h2><ul>'
        '<li><b>Wat verandert er?</b> Over spaargeld en beleggingen boven een bepaald bedrag betaal je belasting. In 2027 wordt dat bedrag iets hoger: ongeveer € 60.280 per persoon. Heb je een partner? Dan is het samen ongeveer het dubbele.</li>'
        '<li><b>Wat ging niet door?</b> In september was het plan om dat bedrag te halveren naar € 30.846. Dat plan is in november geschrapt. Daar hoef je je dus geen zorgen meer over te maken.</li>'
        '<li><b>Zeker?</b> Nog een plan, maar de Tweede Kamer zei al ja.</li></ul>'
        '<h2>Je loon en je inkomstenbelasting</h2><ul>'
        '<li><b>Wat verandert er?</b> Wie werkt, houdt iets meer over. Het plan is een hogere korting voor werkenden (de arbeidskorting, € 173 extra) en iets lagere tarieven. Ook de algemene korting die iedereen krijgt, gaat iets omhoog.</li>'
        '<li><b>Wat merk je ervan?</b> Meestal een paar euro per maand meer netto loon.</li>'
        '<li><b>Zeker?</b> Nog een plan.</li></ul>'
        '<h2>Tanken</h2><ul>'
        '<li><b>Wat verandert er?</b> Benzine en diesel hebben nu een korting op de belasting. Het plan is om die korting nog een jaar te houden, tot eind 2027. In 2028 wordt de korting kleiner en vanaf 2029 is hij weg.</li>'
        '<li><b>LPG:</b> daar stopt de korting wel. LPG wordt dus duurder.</li>'
        '<li><b>Zeker?</b> Nog een plan. Gaat het niet door, dan wordt benzine op 1 januari ongeveer 18 cent per liter duurder.</li></ul>'
        '<h2>Vliegen</h2><ul>'
        '<li><b>Wat verandert er?</b> Nu betaal je overal dezelfde vliegbelasting: € 30,25. Vanaf 2027 hangt het af van hoe ver je vliegt: dichtbij (zoals Spanje) ongeveer € 31, verder weg (zoals Turkije) ongeveer € 50, en heel ver (zoals Thailand) ongeveer € 59 per persoon.</li>'
        '<li><b>Zeker?</b> Dat het per afstand gaat, staat vast. Het precieze bedrag voor heel verre vluchten is nog een plan.</li></ul>'
        '<h2>Je auto</h2><ul>'
        '<li><b>Elektrische auto:</b> je houdt 30% korting op de wegenbelasting.</li>'
        '<li><b>Camper:</b> je krijgt het halve tarief alleen nog als je camper goed bij de RDW staat. Check dit vóór 1 januari. <a href="/wegenbelasting-2027/">Lees hoe</a>.</li></ul>'
        '<h2>Je huis en energie</h2><ul>'
        '<li><b>Zonnepanelen:</b> het salderen stopt op 1 januari 2027. Dat staat vast. <a href="/salderen-2027/">Lees wat het voor jou betekent</a>.</li>'
        '<li><b>Energierekening:</b> die wordt gemiddeld zo’n € 149 duurder, vooral door hogere netkosten. <a href="/energierekening-verlagen/">Zo bespaar je</a>.</li></ul>'
        '<h2>Kleine dingen</h2><ul>'
        '<li><b>Bloemen en planten</b> worden duurder: daar komt het hoge btw-tarief op.</li>'
        '<li><b>Alcohol</b> wordt elk jaar iets duurder: de belasting groeit voortaan mee met de prijzen.</li></ul>'
        '<div class="let"><b>Wat moet je nu doen?</b> Voor de meeste dingen niets: het gaat vanzelf. Alleen als je een camper of bestelauto hebt, of veel spaargeld en toeslagen, is het slim om vóór 1 januari even te checken. Kijk ook bij <a href="/">Deze data niet missen</a> op de homepage.</div>',
        '',
        [("/wegenbelasting-2027/", "Wegenbelasting 2027"), ("/salderen-2027/", "Einde salderen 2027"), ("/belastingaangifte-tips/", "Belastingaangifte tips"), ("/kindgebonden-budget-2027/", "Kindgebonden budget 2027")],
        [("Zijn de belastingplannen voor 2027 al zeker?", "Nog niet helemaal. De Tweede Kamer stemde op 12 november 2026 voor. De Eerste Kamer stemt rond 16 december 2026. Pas daarna is het wet."),
         ("Gaat het belastingvrije spaargeld omlaag in 2027?", "Nee. Het plan om het te halveren is geschrapt. Het bedrag gaat juist iets omhoog, naar ongeveer € 60.280 per persoon."),
         ("Wordt tanken duurder in 2027?", "Waarschijnlijk niet: het plan is om de korting op de belasting op benzine en diesel nog een jaar te houden. Alleen LPG wordt duurder."),
         ("Wordt vliegen duurder?", "Voor verre reizen wel. Vanaf 2027 hangt de vliegbelasting af van de afstand. Dichtbij blijft het ongeveer gelijk.")],
        [("https://box3wacht.nl/artikelen/heffingsvrij-vermogen-2027", "Box3Wacht"), ("https://nettonu.nl/heffingsvrij-vermogen-2027", "NettoNu"), ("https://www.accountant.nl/nieuws/2026/9/belastingplan-2027-kabinet-schrapt-fiscale-regelingen-en-past-heffingen-aan/", "Accountant.nl"), ("https://www.rijksoverheid.nl/themas/belastingen-uitkeringen-en-toeslagen/belastingplan/plannen-kabinet-voor-belasting-op-brandstof-vliegbelasting-en-reiskostenvergoeding", "Rijksoverheid (brandstof en vliegen)"), ("https://ondernemersplein.overheid.nl/verhoging-vliegbelasting-lange-vluchten/", "Ondernemersplein (vliegbelasting)"), ("https://www.autoreview.nl/nieuws/id/38497/accijns-benzine-2027-stemming-tweede-kamer", "Autoreview")],
        "Belastingen 2027: wat verandert er voor jou? Simpel uitgelegd", "Belastingen 2027 in gewone taal: spaargeld, loon, tanken, vliegen, auto en energie. Wat verandert er, en wat is al zeker en wat nog niet?")
    artikel("/wegenbelasting-2027/", "Wegenbelasting 2027", "tank",
        "Wegenbelasting 2027: wat verandert er voor elektrische auto’s, campers en bestelauto’s?",
        "Op 1 januari 2027 verandert er weer wat aan de motorrijtuigenbelasting. Rijd je elektrisch, heb je een camper of een bestelauto als particulier? Lees dan wat je moet weten en wat je vóór de jaarwisseling moet checken.",
        [("30%", "korting voor elektrische personenauto’s in 2027"), ("Half", "tarief voor campers, nu via de RDW"), ("SA", "code die je camper bij de RDW moet hebben"), ("4 jan", "rekenhulp mrb 2027 online")],
        '<h2>Elektrische auto</h2><ul>'
        '<li><b>Korting blijft 30%.</b> Voor een volledig elektrische personenauto (of waterstofauto) betaal je in 2027, net als in 2026, 70% van het normale tarief voor jouw gewicht en provincie.</li>'
        '<li><b>Daarna minder korting.</b> In 2028 blijft het 30%, in 2029 wordt het 25% en vanaf 2030 betaal je het volle tarief.</li>'
        '<li><b>Geen korting voor plug-inhybrides en elektrische bestelauto’s.</b> Die betalen sinds 2026 al het volle tarief.</li>'
        '<li><b>Let op:</b> de korting is een percentage. Stijgt het normale tarief of de provinciale opslag, dan kan je rekening toch omhoog gaan.</li></ul>'
        '<h2>Camper (kampeerauto)</h2><ul>'
        '<li><b>Half tarief.</b> Sinds 1 januari 2026 betaal je voor een camper de helft van de motorrijtuigenbelasting (daarvoor een kwart).</li>'
        '<li><b>Vanaf 2027 bepaalt de RDW het.</b> Staat je camper bij de RDW geregistreerd als categorie M met de code <b>SA</b> (speciale doeleinden), dan krijg je het kampeerautotarief automatisch. Zonder SA betaal je het gewone tarief.</li>'
        '<li><b>Niet meer aanvragen.</b> Na 2026 kun je het kampeerautotarief niet meer bij de Belastingdienst aanvragen.</li>'
        '<li><b>Geschorst?</b> Komt een camper zonder SA-registratie in 2027 uit de schorsing, dan geldt meteen het gewone tarief.</li></ul>'
        '<h2>Bestelauto van een particulier</h2><p>Ook hier telt vanaf 2027 de RDW-registratie: je bestelauto moet als <b>N1</b> staan geregistreerd. Anders betaal je het tarief van de categorie waarin hij wel staat.</p>'
        '<h2>Doe dit vóór 1 januari</h2><ol class="stappen">'
        '<li><b>Doe de kentekencheck</b> op ovi.rdw.nl en kijk welke categorie en code je voertuig heeft.</li>'
        '<li><b>Klopt het niet?</b> Laat je camper of bestelauto zo snel mogelijk (her)keuren bij de RDW. Voldoet hij, dan wordt de juiste registratie automatisch toegevoegd.</li>'
        '<li><b>Reken je nieuwe bedrag uit</b> met de rekenhulp van de Belastingdienst. Die staat vanaf 4 januari 2027 online.</li>'
        '<li><b>Gebruik je de camper maanden niet?</b> Overweeg schorsen bij de RDW. Dan betaal je in die periode geen wegenbelasting, maar je mag er ook niet mee op de openbare weg staan.</li></ol>',
        partner(awin(8311, "bespaarvriend-wegenbelasting", "https://www.unitedconsumers.com/autoverzekering"), "Bespaar op je autoverzekering", "Duurdere wegenbelasting? Haal het terug op je autoverzekering. Vergelijk premies in een paar minuten.", "Vergelijk autoverzekeringen"),
        [("/auto-en-tanken/", "Auto en tanken: besparen"), ("/autoverzekering-besparen/", "Autoverzekering besparen")],
        [("Hoeveel korting krijg ik in 2027 op de wegenbelasting voor mijn elektrische auto?", "30%, net als in 2026. Je betaalt dus 70% van het normale tarief voor jouw gewichtsklasse en provincie. In 2029 wordt de korting 25% en vanaf 2030 vervalt hij."),
         ("Krijgt een plug-inhybride korting?", "Nee. Plug-inhybrides en elektrische bestelauto’s betalen sinds 2026 het volle tarief."),
         ("Wat moet ik doen voor mijn camper?", "Controleer met de RDW-kentekencheck of je camper als categorie M met de code SA staat geregistreerd. Zo ja, dan krijg je het kampeerautotarief automatisch. Zo nee, laat hem dan zo snel mogelijk (her)keuren."),
         ("Wanneer betaal ik het nieuwe tarief?", "Vanaf het eerste tijdvak dat in 2027 begint. Loopt jouw tijdvak bijvoorbeeld van 25 oktober 2026 tot en met 24 januari 2027, dan geldt het nieuwe tarief vanaf 25 januari 2027.")],
        [("https://www.belastingdienst.nl/wps/wcm/connect/nl/auto-en-vervoer/content/veranderingen-vrijstellingen-bepaalde-tarieven-mrb-vanaf-januari-2027", "Belastingdienst (wijzigingen 2027)"), ("https://www.belastingdienst.nl/mrb-kampeerauto", "Belastingdienst (kampeerauto)"), ("https://www.athlon.com/nl/kennisbank/belastingplan-2027-autobelastingen-en-mobiliteit/", "Athlon (Belastingplan 2027)"), ("https://www.rijksoverheid.nl/onderwerpen/belastingen-op-auto-en-motor/belastingvoordelen-klimaat", "Rijksoverheid")],
        "Wegenbelasting 2027: elektrische auto, camper en bestelauto", "Wegenbelasting 2027: 30% korting voor elektrische auto’s, het kampeerautotarief nu automatisch via de RDW (code SA) en bestelauto’s alleen als N1. Check dit vóór 1 januari.")
    artikel("/noodfonds-energie-2027/", "Noodfonds Energie 2027", "energie",
        "Noodfonds Energie 2027: tot € 1.800 steun voor je energierekening",
        "Is je energierekening te hoog voor je inkomen? Dan kun je van 4 januari tot en met 7 mei 2027 steun aanvragen bij het Noodfonds Energie. Dit keer raakt het geld niet op.",
        [("€ 120 – € 1.800", "steun, verrekend met je energierekening"), ("4 jan", "aanvragen kan vanaf 4 januari 2027"), ("7 mei", "laatste dag om aan te vragen"), ("4–6 wkn", "daarna krijg je het geld")],
        '<h2>Heb jij recht op steun?</h2><ul>'
        '<li><b>Je inkomen is laag.</b> Het fonds is voor huishoudens met een bruto-inkomen tot 130% van het sociaal minimum.</li>'
        '<li><b>Je energierekening is hoog.</b> Je betaalt 8% of meer van je inkomen aan energie.</li>'
        '<li><b>Je krijgt een deel terug.</b> Het fonds betaalt een deel van de energiekosten boven die grens: minimaal € 120 en maximaal € 1.800.</li></ul>'
        '<h2>Zo vraag je het aan</h2><ol class="stappen">'
        '<li><b>Bereid je voor vanaf 1 december 2026.</b> Dan staat alle informatie online en kun je het Noodfonds bellen met vragen.</li>'
        '<li><b>Pak je gegevens erbij:</b> je DigiD, je inkomen en je termijnbedrag of jaarafrekening van je energieleverancier.</li>'
        '<li><b>Vraag aan tussen 4 januari en 7 mei 2027.</b> Dat kan online met DigiD of op papier.</li>'
        '<li><b>Wacht 4 tot 6 weken.</b> Daarna wordt het bedrag verrekend met je energierekening.</li></ol>'
        '<div class="let"><b>Geen recht?</b> Vraag bij je gemeente naar bijzondere bijstand of een energiefixer. En kijk of een <a href="/energierekening-verlagen/">goedkoper energiecontract</a> je helpt.</div>',
        widget("energie", "Energie vergelijken") + partner(awin(8520, "bespaarvriend-noodfonds", "https://www.gaslicht.com/energievergelijken"), "Ook besparen met een ander contract", "Ook zonder steun kan een ander contract veel schelen. Vergelijk energiecontracten met de tarieven voor 2027.", "Vergelijk energiecontracten"),
        [("/energierekening-verlagen/", "Energierekening verlagen: 8 tips"), ("/energie-2027/", "Energie 2027: alles wat verandert"), ("/huurtoeslag-2027/", "Huurtoeslag 2027")],
        [("Wanneer kan ik het Noodfonds Energie aanvragen?", "Van 4 januari tot en met 7 mei 2027. Vanaf 1 december 2026 kun je al terecht met vragen."),
         ("Hoeveel krijg ik uit het Noodfonds?", "Minimaal € 120 en maximaal € 1.800. Hoeveel precies hangt af van je inkomen en welk deel daarvan je aan energie kwijt bent."),
         ("Raakt het geld weer op?", "Volgens de overheid niet: iedereen die in de aanvraagperiode aanvraagt en aan de voorwaarden voldoet, krijgt steun."),
         ("Kan ik op papier aanvragen?", "Ja. Lukt online aanvragen niet, dan kun je een papieren formulier gebruiken.")],
        [("https://www.rijksoverheid.nl/onderwerpen/koopkracht/vraag-en-antwoord/hoe-krijg-ik-geld-terug-uit-het-noodfonds-energie", "Rijksoverheid"), ("https://www.rijksoverheid.nl/actueel/nieuws/2026/09/29/noodfonds-energie-gaat-open", "Rijksoverheid (voorwaarden)"), ("https://www.keuze.nl/nieuws/noodfonds-energie-opent-4-januari", "Keuze.nl")],
        "Noodfonds Energie 2027: tot € 1.800 steun, aanvragen vanaf 4 januari", "Noodfonds Energie 2027: van 4 januari tot en met 7 mei aanvragen, € 120 tot € 1.800 steun bij een laag inkomen en hoge energierekening. Zo vraag je het aan.")
    artikel("/isde-subsidie-2027/", "ISDE subsidie 2027", "zon",
        "ISDE subsidie 2027: zo krijg je geld terug voor isolatie en een warmtepomp",
        "Met de ISDE krijg je als huiseigenaar een vast bedrag terug als je isoleert of een warmtepomp neemt. In 2027 verandert er veel. Wie slim plant, krijgt honderden euro’s meer.",
        [("5 jan 2027", "nieuwe ISDE opent om 12.00 uur"), ("2x", "isolatiesubsidie bij 2 of meer maatregelen"), ("+ € 200", "extra voor een slimme warmtepomp"), ("31 dec", "warmtepomp vóór die datum kopen = oud tarief")],
        '<h2>Wat verandert er in 2027?</h2><ul>'
        '<li><b>Lucht-waterwarmtepomp: minder subsidie.</b> Het bedrag per kilowatt daalt in 2027 flink. Koop je de warmtepomp vóór of op 31 december 2026 en laat je hem in 2027 plaatsen, dan geldt nog het oude, hogere bedrag via een overgangsregeling.</li>'
        '<li><b>Extra voor een slimme warmtepomp.</b> Een warmtepomp die je slim kunt aansturen levert € 200 extra op.</li>'
        '<li><b>Drievoudig glas:</b> de subsidie voor triple glas met nieuwe kozijnen wordt verlaagd.</li>'
        '<li><b>Water-water- en grondwarmtepompen</b> houden hetzelfde bedrag per kilowatt.</li></ul>'
        '<h2>Zo haal je het meeste eruit</h2><ol class="stappen">'
        '<li><b>Combineer maatregelen.</b> Laat je twee isolatiemaatregelen doen, of isolatie samen met een warmtepomp of zonneboiler? Dan krijg je het dubbele bedrag voor isolatie.</li>'
        '<li><b>Check de meldcode.</b> Je warmtepomp, zonneboiler of isolatiemateriaal moet op de meldcodelijst van RVO staan. Vraag de installateur ernaar.</li>'
        '<li><b>Maak foto’s</b> tijdens het isoleren. RVO vraagt daarom bij de aanvraag.</li>'
        '<li><b>Vraag op tijd aan</b> via de website van RVO, na installatie. Bewaar je factuur en betaalbewijs.</li></ol>'
        '<div class="let"><b>Let op:</b> isolatiesubsidie is alleen voor particuliere woningeigenaren die er zelf wonen. Huur je? Vraag dan je verhuurder naar verduurzaming.</div>',
        widget("energie", "Energie vergelijken") + partner(awin(8520, "bespaarvriend-isde", "https://www.gaslicht.com/energievergelijken"), "Na het isoleren: kies het juiste contract", "Minder verbruik? Dan past misschien een ander contract. Vergelijk energiecontracten met de tarieven voor 2027.", "Vergelijk energiecontracten"),
        [("/energierekening-verlagen/", "Energierekening verlagen: 8 tips"), ("/salderen-2027/", "Einde salderen 2027"), ("/energie-2027/", "Energie 2027")],
        [("Wanneer opent de ISDE 2027?", "Op dinsdag 5 januari 2027 om 12.00 uur."),
         ("Krijg ik minder subsidie voor een warmtepomp in 2027?", "Voor een lucht-waterwarmtepomp wel. Koop je hem vóór of op 31 december 2026, dan geldt via een overgangsregeling nog het hogere bedrag, ook als hij pas in 2027 wordt geplaatst."),
         ("Hoe krijg ik meer subsidie voor isolatie?", "Combineer twee of meer isolatiemaatregelen, of isolatie met een warmtepomp, zonneboiler of warmtenet. Dan verdubbelt het bedrag voor isolatie."),
         ("Kan ik als huurder ISDE aanvragen?", "Voor isolatie niet: dat is alleen voor eigenaren die zelf in hun woning wonen.")],
        [("https://www.rvo.nl/subsidie-en-financieringswijzer/isde/woningeigenaren", "RVO"), ("https://solarmagazine.nl/nieuws-zonne-energie/i45146/overgangsregeling-beschermt-kopers-warmtepomp-tegen-halvering-van-subsidie", "Solar Magazine (overgangsregeling)"), ("https://solarmagazine.nl/nieuws-zonne-energie/i45014/200-euro-extra-subsidie-voor-slimme-warmtepomp-subsidie-voor-triple-glas-gehalveerd", "Solar Magazine (slimme warmtepomp)")],
        "ISDE subsidie 2027: isolatie en warmtepomp, wat verandert er", "ISDE subsidie 2027: opent 5 januari, € 200 extra voor een slimme warmtepomp, dubbele isolatiesubsidie bij 2 maatregelen. Koop vóór 31 december voor het oude tarief.")
    artikel("/kinderopvangtoeslag-2027/", "Kinderopvangtoeslag 2027", "toeslag",
        "Kinderopvangtoeslag 2027: meer ouders krijgen het maximum",
        "In 2027 krijgen werkende ouders met een gezamenlijk inkomen tot ongeveer € 72.000 het maximale vergoedingspercentage. Ook de maximum uurprijzen gaan omhoog.",
        [("96%", "maximale vergoeding"), ("± € 72.000", "inkomen tot waar je het maximum krijgt"), ("€ 11,60", "max. uurprijs dagopvang 2027"), ("€ 10,31", "max. uurprijs BSO 2027")],
        '<h2>Maximum uurprijzen</h2><p>De toeslag wordt berekend over het uurtarief tot deze maximum uurprijs. Vraagt je opvang meer, dan betaal je het verschil zelf.</p>'
        '<table><tr><th>Soort opvang</th><th>2026</th><th>2027</th></tr>'
        '<tr><td>Dagopvang</td><td>€ 11,23</td><td>€ 11,60</td></tr>'
        '<tr><td>Buitenschoolse opvang (BSO)</td><td>€ 9,98</td><td>€ 10,31</td></tr>'
        '<tr><td>Gastouderopvang</td><td>€ 8,49</td><td>€ 8,77</td></tr></table>'
        '<p>Dit zijn de voorlopige cijfers van de overheid.</p>'
        '<h2>Zo voorkom je verrassingen</h2><ol class="stappen">'
        '<li><b>Vraag je opvang naar het uurtarief voor 2027.</b> Ligt het boven de maximum uurprijs, reken dan uit wat je zelf bijbetaalt.</li>'
        '<li><b>Geef je inkomen goed door</b> in Mijn toeslagen. Een te laag geschat inkomen kan later tot terugbetalen leiden.</li>'
        '<li><b>Geef het aantal uren door</b> dat in je contract staat, en pas het aan als dat verandert.</li>'
        '<li><b>Promovendus?</b> Vanaf 2027 krijg je ook recht op kinderopvangtoeslag als je promoveert of onderzoeker bent aan een universiteit of academisch ziekenhuis.</li></ol>',
        partner(awin(107738, "bespaarvriend-kinderopvang", "https://www.poliswijzer.nl/zorgverzekering"), "Zorgverzekering voor het gezin vergelijken", "Kinderen tot 18 zijn gratis meeverzekerd. Overstappen kan nog tot 31 december.", "Vergelijk zorgverzekeringen"),
        [("/kindgebonden-budget-2027/", "Kindgebonden budget 2027"), ("/kinderbijslag-2027/", "Kinderbijslag 2027"), ("/zorgtoeslag-2027/", "Zorgtoeslag 2027")],
        [("Hoeveel kinderopvangtoeslag krijg ik in 2027?", "Met een gezamenlijk inkomen tot ongeveer € 72.000 krijg je het maximale percentage van 96%, berekend over het uurtarief tot de maximum uurprijs. Daarboven wordt het percentage geleidelijk lager."),
         ("Wat is de maximum uurprijs voor dagopvang in 2027?", "Voorlopig € 11,60 per uur. Voor BSO is dat € 10,31 en voor gastouderopvang € 8,77."),
         ("Mijn opvang is duurder dan de maximum uurprijs. Wat nu?", "Dan betaal je het verschil zelf. Vraag je opvang naar het tarief voor 2027 en reken uit wat je bijbetaalt."),
         ("Wanneer komt het nieuwe stelsel?", "Het kabinet werkt toe naar een nieuw financieringsstelsel waarin de opvang rechtstreeks wordt betaald. Dat is pas over een paar jaar.")],
        [("https://www.rijksoverheid.nl/actueel/nieuws/2026/09/21/kabinet-zet-belangrijke-stap-naar-nieuwe-financieringsstelsel-kinderopvang", "Rijksoverheid"), ("https://www.sra.nl/nieuws/259001/2026/02/plannen-verdere-verbetering-kinderopvangtoeslag-per-2027", "SRA")],
        "Kinderopvangtoeslag 2027: maximum uurprijzen en inkomensgrens", "Kinderopvangtoeslag 2027: het maximum van 96% tot een inkomen van ongeveer € 72.000, en een maximum uurprijs van € 11,60 voor dagopvang en € 10,31 voor BSO.")
    artikel("/belastingaangifte-tips/", "Belastingaangifte tips", "bon",
        "Belastingaangifte: zo haal je alles terug waar je recht op hebt",
        "Veel mensen laten bij hun aangifte geld liggen, omdat ze aftrekposten vergeten. Met deze checklist mis je niets, en heb je je teruggave zo snel mogelijk binnen.",
        [("1 maart", "aangifte doen kan vanaf"), ("1 mei", "uiterste datum, of vraag uitstel"), ("Vóór 1 april", "insturen = meestal bericht vóór 1 juli"), ("5 jaar", "terug kun je een vergeten aftrek nog regelen")],
        '<h2>Zo pak je het aan</h2><ol class="stappen">'
        '<li><b>Begin vroeg.</b> Vanaf 1 maart kun je aangifte doen. Stuur je hem vóór 1 april in, dan krijg je meestal vóór 1 juli bericht en je geld snel daarna.</li>'
        '<li><b>Controleer de vooraf ingevulde gegevens.</b> Loon, bankrekeningen en WOZ-waarde staan er al in, maar ze kloppen niet altijd. Vergelijk ze met je jaaropgaven.</li>'
        '<li><b>Loop de aftrekposten na.</b> Zie het lijstje hieronder. Die vult de Belastingdienst niet voor je in.</li>'
        '<li><b>Verdeel slim met je fiscale partner.</b> Zet aftrekposten zoals hypotheekrente bij de partner met het hoogste inkomen. Dat levert vaak meer op.</li>'
        '<li><b>Niet op tijd klaar?</b> Vraag vóór 1 mei uitstel aan via Mijn Belastingdienst. Dan heb je tot 1 september.</li></ol>'
        '<h2>Aftrekposten die vaak vergeten worden</h2><ul>'
        '<li><b>Specifieke zorgkosten</b> die je zelf betaalde, zoals bepaalde hulpmiddelen, dieetkosten op voorschrift en extra reiskosten voor ziekenbezoek.</li>'
        '<li><b>Giften</b> aan goede doelen met een ANBI-status, boven een drempel. Periodieke giften (vastgelegd voor 5 jaar) zijn zonder drempel aftrekbaar.</li>'
        '<li><b>Hypotheekrente en afsluitkosten</b>, zoals advies- en notariskosten in het jaar dat je een huis kocht.</li>'
        '<li><b>Lijfrentepremie</b> als je een pensioentekort hebt, bijvoorbeeld als zzp’er.</li>'
        '</ul>'
        '<div class="let"><b>Iets vergeten?</b> Je kunt een aftrekpost tot 5 jaar terug alsnog opgeven via een verzoek om ambtshalve vermindering.</div>',
        '',
        [("/zorgtoeslag-2027/", "Zorgtoeslag 2027"), ("/huurtoeslag-2027/", "Huurtoeslag 2027"), ("/administratie/", "Vaste lasten op orde")],
        [("Wanneer moet ik aangifte doen?", "Tussen 1 maart en 1 mei. Lukt dat niet, vraag dan vóór 1 mei uitstel aan; je krijgt dan tot 1 september."),
         ("Moet ik aangifte doen als ik geen brief kreeg?", "Alleen als je moet bijbetalen boven een klein drempelbedrag. Maar vaak krijg je juist geld terug, dus invullen loont meestal."),
         ("Wanneer krijg ik mijn geld terug?", "Doe je vóór 1 april aangifte, dan krijg je meestal vóór 1 juli bericht. Daarna volgt de uitbetaling binnen een paar dagen."),
         ("Kan ik een vergeten aftrekpost later nog opgeven?", "Ja, tot 5 jaar terug, met een verzoek om ambtshalve vermindering bij de Belastingdienst.")],
        [("https://www.consumentenbond.nl/belastingaangifte/checklist-belastingaangifte-doen", "Consumentenbond"), ("https://bieb.knab.nl/inkomsten-uitgaven/aangifte-inkomstenbelasting-wat-je-moet-weten", "Knab"), ("https://www.raisin.com/nl-nl/sparen/wanneer-belasting-terug/", "Raisin")],
        "Belastingaangifte tips: aftrekposten die je niet wilt missen", "Haal alles terug bij je belastingaangifte: begin vóór 1 april, controleer de vooraf ingevulde gegevens en vergeet zorgkosten, giften en afsluitkosten niet.")
    artikel("/kinderbijslag-2027/", "Kinderbijslag 2027", "toeslag",
        "Kinderbijslag 2027: bedragen, betaaldata en wat er verandert",
        "Kinderbijslag krijg je voor elk kind tot 18 jaar, ongeacht je inkomen. In 2027 gaat het bedrag licht omhoog. Hier zie je wat je krijgt en wanneer het op je rekening staat.",
        [("€ 298,40", "per kwartaal voor 0–5 jaar (sinds 1 juli 2026)"), ("4x", "per jaar, achteraf betaald"), ("2 jan 2027", "betaling over het 4e kwartaal 2026"), ("18 jaar", "tot die leeftijd krijg je het")],
        '<h2>Hoeveel krijg je?</h2><p>Het bedrag hangt af van de leeftijd van je kind op de eerste dag van het kwartaal. In het eerste halfjaar van 2026 was het per kind per kwartaal:</p>'
        '<table><tr><th>Leeftijd kind</th><th>Per kwartaal</th><th>Per jaar</th></tr><tr><td>0 t/m 5 jaar</td><td>€ 295,07</td><td>€ 1.180,28</td></tr><tr><td>6 t/m 11 jaar</td><td>€ 358,30</td><td>€ 1.433,20</td></tr><tr><td>12 t/m 17 jaar</td><td>€ 421,53</td><td>€ 1.686,12</td></tr></table>'
        '<p>Sinds 1 juli 2026 zijn de bedragen iets hoger; voor een kind tot 6 jaar is dat € 298,40 per kwartaal. Het kabinet verhoogt de kinderbijslag in 2027 licht. De nieuwe bedragen maakt de SVB eind december bekend.</p>'
        '<h2>Wat verandert er in 2027?</h2><ul>'
        '<li><b>Kinderbijslag iets omhoog</b> voor alle ouders, om meer zekerheid te geven.</li>'
        '<li><b>Kindgebonden budget omlaag</b> voor gezinnen met een inkomen boven ongeveer € 61.917. Lees <a href="/kindgebonden-budget-2027/">wat dat voor jou betekent</a>.</li>'
        '<li><b>Nieuwe kindregeling</b> pas later: het kabinet wil kinderbijslag en kindgebonden budget rond 2030 samenvoegen.</li></ul>'
        '<div class="let"><b>Let op:</b> de kinderbijslag stopt in het kwartaal nadat je kind 18 wordt. Gaat je kind eerder studeren met studiefinanciering, dan stopt hij ook eerder.</div>',
        '',
        [("/kindgebonden-budget-2027/", "Kindgebonden budget 2027"), ("/zorgtoeslag-2027/", "Zorgtoeslag 2027"), ("/administratie/", "Vaste lasten op orde")],
        [("Hoeveel kinderbijslag krijg ik in 2027?", "Iets meer dan in 2026. De precieze bedragen maakt de SVB eind december bekend. In 2026 was het € 295,07 tot € 421,53 per kwartaal, afhankelijk van de leeftijd."),
         ("Wanneer wordt de kinderbijslag betaald?", "Elk kwartaal achteraf: begin januari, april, juli en oktober. De betaling over het vierde kwartaal van 2026 komt op 2 januari 2027."),
         ("Hangt kinderbijslag af van mijn inkomen?", "Nee, iedereen krijgt hetzelfde bedrag per kind. Het kindgebonden budget hangt wel af van je inkomen."),
         ("Moet ik kinderbijslag aanvragen?", "Na de geboorte van je kind stuurt de SVB je meestal vanzelf een formulier. Aanvragen kan ook via mijn.svb.nl.")],
        [("https://rekenmachinepro.nl/blog/kinderbijslag-uitbetaaldata-2026/", "Rekenmachinepro"), ("https://www.welingelichtekringen.nl/economie/kinderbijslag-nederland-vlaanderen-duitsland", "Welingelichte Kringen"), ("https://www.eerstekamer.nl/nonav/behandeling/20260917/nota_van_wijziging_tweede_nota_van/document3/f=/vn0zmz4cg0yw.pdf", "Eerste Kamer"), ("https://www.oudersvannu.nl/baby/veiligheid/kinderbijslag-hier-heb-je-recht-op", "Ouders van Nu")],
        "Kinderbijslag 2027: bedragen, betaaldata en wijzigingen", "Kinderbijslag 2027: bedragen per leeftijd, betaaldata per kwartaal en wat er verandert. De betaling over het 4e kwartaal van 2026 komt op 2 januari 2027.")
    artikel("/huurverhoging-2027/", "Huurverhoging 2027", "sleutel",
        "Huurverhoging 2027: hoeveel mag je verhuurder vragen?",
        "Je huur mag één keer per jaar omhoog, maar niet onbeperkt. Hoeveel hangt af van het soort woning. Zo check je of je huurverhoging klopt, en wat je doet als hij te hoog is.",
        [("4,1%", "max. sociale huur (1 juli 2026 – 1 juli 2027)"), ("6,1%", "max. middenhuur in 2026"), ("4,4%", "max. vrije sector in 2026"), ("2 mnd", "vooraf moet je het voorstel krijgen")],
        '<h2>Hoeveel mag je huur omhoog?</h2><table><tr><th>Soort woning</th><th>Maximum</th><th>Ingang</th></tr>'
        '<tr><td>Sociale huur</td><td>4,1% (of € 25 bij huur onder € 350)</td><td>1 juli 2026 tot 1 juli 2027</td></tr>'
        '<tr><td>Middenhuur</td><td>6,1%</td><td>1 januari 2026 tot 1 januari 2027</td></tr>'
        '<tr><td>Vrije sector</td><td>4,4%</td><td>1 januari 2026 tot 1 januari 2027</td></tr></table>'
        '<p>De maxima voor sociale huur vanaf 1 juli 2027 maakt de overheid in december bekend. Bij middenhuur en vrije sector gelden nieuwe maxima vanaf 1 januari 2027. Staat er in je contract een lager percentage? Dan geldt dat lagere percentage.</p>'
        '<h2>Zo check je je huurverhoging</h2><ol class="stappen">'
        '<li><b>Kijk welk soort woning je hebt.</b> Sociale huur, middenhuur of vrije sector: dat staat in je contract of vraag je aan je verhuurder.</li>'
        '<li><b>Reken het percentage uit.</b> Nieuwe huur min oude huur, gedeeld door de oude huur. Is het hoger dan het maximum, dan klopt het niet.</li>'
        '<li><b>Let op de termijn.</b> Bij sociale huur moet je het voorstel minstens 2 maanden voor de ingangsdatum krijgen.</li>'
        '<li><b>Te hoog? Maak bezwaar.</b> Doe dat schriftelijk bij je verhuurder, vóór de ingangsdatum. Komen jullie er niet uit, dan kun je naar de Huurcommissie.</li></ol>'
        '<div class="let"><b>Tip:</b> kijk meteen of je recht hebt op <a href="/huurtoeslag-2027/">huurtoeslag</a>. Sinds 2026 is je huur daar nooit meer te hoog voor.</div>',
        partner(awin(8520, "bespaarvriend-huurverhoging", "https://www.gaslicht.com/energievergelijken"), "Bespaar op je woonlasten", "Hogere huur? Haal het terug op energie. Vergelijk energiecontracten met de tarieven voor 2027.", "Vergelijk energiecontracten"),
        [("/huurtoeslag-2027/", "Huurtoeslag 2027"), ("/energierekening-verlagen/", "Energierekening verlagen")],
        [("Hoeveel mag mijn sociale huur omhoog?", "Van 1 juli 2026 tot 1 juli 2027 maximaal 4,1%, of € 25 als je huur lager is dan € 350. Bij een hoger inkomen mag de verhuurder soms meer vragen."),
         ("Hoeveel mag de huur in de vrije sector omhoog?", "In 2026 maximaal 4,4%. Het maximum voor 2027 wordt eind 2026 bekendgemaakt. Staat er een lager percentage in je contract, dan geldt dat."),
         ("Wat als mijn huurverhoging te hoog is?", "Maak schriftelijk bezwaar bij je verhuurder, vóór de ingangsdatum. Lost dat niets op, dan kun je de Huurcommissie inschakelen."),
         ("Hoe vaak mag de huur omhoog?", "Eén keer per jaar. Bij sociale huur meestal op 1 juli.")],
        [("https://www.rijksoverheid.nl/onderwerpen/veranderingen/nieuws/2025/12/15/maximale-huurverhoging-2026-in-sociale-sector-41-middenhuur-61-en-vrije-sector-44", "Rijksoverheid"), ("https://www.volkshuisvestingnederland.nl/onderwerpen/huren-en-wonen/passende-huur/jaarlijkse-huurverhoging", "Volkshuisvesting Nederland"), ("https://aedes.nl/huurbeleid-en-betaalbaarheid/huurbeleid-2027", "Aedes"), ("https://www.cbs.nl/nl-nl/nieuws/2026/36/woninghuur-stijgt-gemiddeld-met-4-4-procent/maximaal-toegestane-reguliere-huurverhoging", "CBS")],
        "Huurverhoging 2027: hoeveel mag je verhuurder vragen?", "Huurverhoging: maximaal 4,1% bij sociale huur, 6,1% bij middenhuur en 4,4% in de vrije sector. Zo check je je huurverhoging en maak je bezwaar als hij te hoog is.")
    artikel("/abonnementen-opzeggen/", "Abonnementen opzeggen", "check",
        "Abonnementen opzeggen: zo stop je makkelijk en betaal je niet te veel",
        "De meeste mensen hebben meer dan tien abonnementen. Vaak loopt er eentje door die je niet meer gebruikt. Dit zijn je rechten, en zo zeg je zonder gedoe op.",
        [("1 maand", "maximale opzegtermijn na de eerste periode"), ("Online", "afgesloten = ook online opzeggen"), ("3 mnd", "max. verlenging bij kranten en tijdschriften"), ("Bewijs", "vraag altijd een bevestiging")],
        '<h2>Je rechten op een rij</h2><ul>'
        '<li><b>Na de eerste periode maandelijks opzegbaar.</b> Een abonnement mag automatisch doorlopen, maar dan moet je het daarna op elk moment kunnen opzeggen, met hoogstens 1 maand opzegtermijn.</li>'
        '<li><b>Zelfde manier als afsluiten.</b> Heb je online afgesloten, dan moet je ook online kunnen opzeggen, bijvoorbeeld per e-mail of via je account.</li>'
        '<li><b>Kranten en tijdschriften:</b> na de eerste periode mogen ze telkens verlengen voor maximaal 3 maanden, of voor onbepaalde tijd met 1 maand opzegtermijn.</li>'
        '<li><b>Internet, tv en mobiel:</b> na je contractperiode (meestal 1 of 2 jaar) zeg je op met hoogstens 1 maand opzegtermijn, die direct ingaat.</li></ul>'
        '<h2>Zo ruim je op in 4 stappen</h2><ol class="stappen">'
        '<li><b>Maak een lijstje.</b> Loop je bankafschriften van de laatste 3 maanden door en schrijf elke vaste afschrijving op. Handig: de gratis app <a href="https://allesoporde.netlify.app/">Alles op orde</a>.</li>'
        '<li><b>Streep door wat je niet gebruikt.</b> Denk aan de sportschool, een tweede streamingdienst, een app-abonnement of een krant die je niet leest.</li>'
        '<li><b>Zeg op en bewaar het bewijs.</b> Vraag altijd een bevestiging per mail of brief.</li>'
        '<li><b>Check het na een maand</b> op je bankafschrift. Wordt er nog afgeschreven, dan kun je een incasso binnen 8 weken laten terugboeken.</li></ol>'
        '<div class="let"><b>Tip:</b> streamingdiensten kun je om de beurt nemen. Eén maand de ene, dan een maand de andere. Dat scheelt al snel € 100 per jaar.</div>',
        sim,
        [("/internet-en-mobiel/", "Internet en mobiel: stop met te veel betalen"), ("/sim-only-overstappen/", "Sim only overstappen"), ("/energiecontract-opzeggen/", "Energiecontract opzeggen")],
        [("Hoe lang is de opzegtermijn van een abonnement?", "Na de eerste contractperiode hoogstens 1 maand. Je kunt dan op elk moment opzeggen."),
         ("Mag een bedrijf mij dwingen te bellen om op te zeggen?", "Nee. Heb je online afgesloten, dan moet je ook online kunnen opzeggen."),
         ("Kan ik een lopend contract eerder stoppen?", "Meestal niet zonder kosten. Soms betaal je een opzegvergoeding voor de resterende maanden. Vragen kan altijd."),
         ("Er wordt na opzeggen nog geld afgeschreven, wat nu?", "Laat de incasso binnen 8 weken terugboeken via je bank en stuur het bedrijf je opzegbevestiging.")],
        [("https://www.acm.nl/nl/onderwerpen/consumentenrecht/prijzen-en-overeenkomsten/regels-voor-het-verlengen-en-opzeggen-van-abonnementen/", "ACM"), ("https://www.consumentenbond.nl/juridisch-advies/opzeggen-abonnement", "Consumentenbond"), ("https://www.rijksoverheid.nl/vraag-en-antwoord/bescherming-van-consumenten/mogen-abonnementen-stilzwijgend-verlengd-worden", "Rijksoverheid")],
        "Abonnementen opzeggen: je rechten en zo stop je makkelijk", "Abonnementen opzeggen: na de eerste periode maandelijks opzegbaar met max. 1 maand opzegtermijn, en online afgesloten is online opzeggen. Zo ruim je op.")
    artikel("/goedkoop-boodschappen-doen/", "Goedkoop boodschappen doen", "boodschappen",
        "Goedkoop boodschappen doen: 10 tips die elke week schelen",
        "Boodschappen zijn voor veel huishoudens de grootste uitgave na huur en energie. Met deze 10 tips houd je elke week geld over, zonder dat je minder lekker eet.",
        [("12", "supermarkten vergeleken op Boodschappenvergelijk.nl"), ("Elke dag", "nieuwe prijzen"), ("Huismerk", "vaak de grootste besparing"), ("Gratis", "en zonder account")],
        '<h2>10 tips om minder uit te geven</h2><ol class="stappen">'
        '<li><b>Vergelijk je lijstje.</b> Op <a href="https://boodschappenvergelijk.nl/?bron=bespaarvriend">Boodschappenvergelijk.nl</a> zie je in één keer bij welke supermarkt jouw boodschappen het goedkoopst zijn.</li>'
        '<li><b>Kies vaker het huismerk.</b> Voor basisproducten als melk, pasta, rijst en schoonmaakmiddel is het verschil met een A-merk vaak groot.</li>'
        '<li><b>Plan je week.</b> Met een weekmenu koop je alleen wat je nodig hebt en gooi je minder weg.</li>'
        '<li><b>Kijk naar de prijs per kilo of liter,</b> niet naar de prijs per pak. Een grote verpakking is niet altijd voordeliger.</li>'
        '<li><b>Gebruik aanbiedingen slim.</b> Sla houdbare producten in als ze in de aanbieding zijn, maar koop niet wat je anders nooit zou kopen.</li>'
        '<li><b>Ga niet met honger.</b> Dan koop je meer, en vaker iets ongezonds.</li>'
        '<li><b>Koop seizoensgroente.</b> Wat nu groeit is goedkoper en lekkerder. Diepvriesgroente is een goed en voordelig alternatief.</li>'
        '<li><b>Kook een keer extra</b> en vries een portie in. Zo voorkom je een dure afhaalavond.</li>'
        '<li><b>Let op de onderste schappen.</b> De duurste producten staan vaak op ooghoogte.</li>'
        '<li><b>Houd bij wat je uitgeeft.</b> Met de gratis app <a href="https://bonnenboek.netlify.app/">Bonnenboek</a> scan je je kassabonnen en zie je waar je geld heen gaat.</li></ol>',
        '',
        [("/boodschappen/", "Besparen op boodschappen"), ("/abonnementen-opzeggen/", "Abonnementen opzeggen"), ("/energierekening-verlagen/", "Energierekening verlagen")],
        [("Welke supermarkt is het goedkoopst?", "Dat verschilt per boodschappenlijstje en per week, door aanbiedingen. Vergelijk je eigen lijstje op Boodschappenvergelijk.nl."),
         ("Zijn huismerken echt goedkoper?", "Meestal wel, en vaak scheelt het veel. De kwaliteit is bij basisproducten vaak vergelijkbaar."),
         ("Loont het om bij meerdere supermarkten te halen?", "Soms, als ze dicht bij elkaar liggen. Voor de meeste mensen levert één goedkope supermarkt kiezen het meest op met het minste gedoe."),
         ("Hoe houd ik mijn boodschappenuitgaven bij?", "Scan je kassabonnen met een app als Bonnenboek. Dan zie je per week en per maand wat je uitgeeft.")],
        [("https://boodschappenvergelijk.nl/", "Boodschappenvergelijk.nl"), ("https://www.nibud.nl/onderwerpen/uitgaven/kosten-boodschappen/", "Nibud")],
        "Goedkoop boodschappen doen: 10 tips die elke week schelen", "Goedkoop boodschappen doen met 10 tips: vergelijk je lijstje bij 12 supermarkten, kies vaker het huismerk, plan je week en let op de prijs per kilo.")
    artikel("/bijverdienen-met-enquetes/", "Bijverdienen met enquêtes", "bon",
        "Bijverdienen met enquêtes: zo werkt het en wat levert het op",
        "Bij een betaald panel vul je online vragenlijsten in en krijg je daar geld, punten of cadeaubonnen voor. Rijk word je er niet van, maar het is een makkelijke manier om iets bij te verdienen. Hieronder zie je panels waar je je gratis kunt aanmelden.",
        [],
        '<h2>Hoe werkt een enquêtepanel?</h2><ol class="stappen">'
        '<li><b>Meld je gratis aan</b> bij een of meer panels. Je vult een korte vragenlijst over jezelf in, zoals je leeftijd en woonplaats.</li>'
        '<li><b>Je krijgt uitnodigingen</b> voor onderzoeken die bij jou passen, per mail of in een app.</li>'
        '<li><b>Vul de vragenlijst in.</b> Daarvoor krijg je geld, punten of een cadeaubon. Bij sommige panels scan je ook je boodschappen.</li>'
        '<li><b>Wissel je tegoed in</b> zodra je de uitbetaalgrens hebt bereikt.</li></ol>'
        '<h2>Wat levert het op?</h2><p>Per vragenlijst is de beloning meestal klein. Het loont vooral als je bij een paar panels tegelijk zit en regelmatig meedoet. Zie het als een extraatje, niet als vast inkomen.</p>'
        '<h2>Tips</h2><ul>'
        '<li><b>Betaal nooit om mee te doen.</b> Een betrouwbaar panel is altijd gratis.</li>'
        '<li><b>Gebruik een apart e-mailadres</b>, dan houd je je gewone mailbox rustig.</li>'
        '<li><b>Let op de uitbetaalgrens.</b> Kijk vooraf vanaf welk bedrag je je tegoed kunt laten uitbetalen.</li>'
        '<li><b>Lees de privacyvoorwaarden</b> en geef alleen gegevens die nodig zijn.</li></ul>',
        widget("enquetes", "Betaalde enquêtepanels"),
        [("/goedkoop-boodschappen-doen/", "Goedkoop boodschappen doen"), ("/belastingaangifte-tips/", "Belasting terug"), ("/abonnementen-opzeggen/", "Abonnementen opzeggen")],
        [("Kost meedoen aan een enquêtepanel geld?", "Nee. Aanmelden en meedoen bij een betrouwbaar panel is gratis. Vraagt een panel om geld, doe dan niet mee."),
         ("Hoeveel kun je verdienen met enquêtes?", "Per vragenlijst meestal een klein bedrag. Wie bij meerdere panels meedoet, spaart er een leuk extraatje mee bij elkaar."),
         ("Hoe krijg je je geld?", "Dat verschilt per panel: via je bankrekening, als cadeaubon of als punten die je inwisselt. Meestal pas vanaf een bepaald bedrag.")],
        [],
        "Bijverdienen met enquêtes: betaalde panels vergelijken", "Bijverdienen met online enquêtes: zo werkt een betaald panel, wat het oplevert en bij welke panels je je gratis aanmeldt. Met tips om oplichting te voorkomen.")
    artikel("/huurtoeslag-2027/", "Huurtoeslag 2027", "sleutel",
        "Huurtoeslag 2027: wat verandert er en heb jij recht?",
        "Sinds 2026 is je huur nooit meer te hoog om huurtoeslag te krijgen. In 2027 verandert er weer iets: ook het vermogen van je toeslagpartner telt mee. Zo zie je snel of je recht hebt.",
        [("Geen", "maximale huur meer als voorwaarde (sinds 2026)"), ("€ 932,93", "huur waarover in 2026 toeslag wordt berekend"), ("1 jan 2027", "vermogen toeslagpartner telt mee"), ("Gratis", "aanvragen via toeslagen.nl")],
        '<h2>Wat verandert er in 2027?</h2><ul>'
        '<li><b>Vermogen van je partner telt mee.</b> Vanaf 1 januari 2027 kijkt Dienst Toeslagen ook naar het vermogen van je toeslagpartner. Hebben jullie samen te veel spaargeld of beleggingen, dan vervalt het recht.</li>'
        '<li><b>De huur is nooit meer te hoog.</b> Sinds 2026 mag je ook bij een hogere huur huurtoeslag aanvragen, zolang je inkomen en vermogen niet te hoog zijn en je in een zelfstandige woning woont. Over het deel boven de huurgrens krijg je geen toeslag.</li>'
        '<li><b>Nieuwe bedragen.</b> De precieze huurgrens en inkomensgrenzen voor 2027 maakt de overheid eind van het jaar bekend. In 2026 werd de toeslag berekend tot een huur van € 932,93; voor jongeren van 18 tot en met 20 jaar tot € 498,20.</li></ul>'
        '<h2>Zo regel je het in 4 stappen</h2><ol class="stappen">'
        '<li><b>Check je vermogen op 1 januari.</b> Heb je op 1 januari te veel vermogen, dan heb je het hele jaar geen recht. Ook niet als het later in het jaar minder wordt.</li>'
        '<li><b>Doe een proefberekening</b> op toeslagen.nl. Daar vul je je huur, inkomen en huishouden in.</li>'
        '<li><b>Vraag aan via Mijn toeslagen.</b> Dat kan met DigiD. Je kunt tot 1 september van het jaar erna aanvragen, maar hoe eerder, hoe sneller je geld krijgt.</li>'
        '<li><b>Geef wijzigingen direct door.</b> Ander inkomen, een nieuwe huisgenoot of een huurverhoging? Geef het snel door, dan hoef je achteraf niets terug te betalen.</li></ol>'
        '<div class="let"><b>Tip:</b> verdien je net te veel? Kijk dan ook of je recht hebt op <a href="/zorgtoeslag-2027/">zorgtoeslag</a> of <a href="/kindgebonden-budget-2027/">kindgebonden budget</a>. Die hebben andere grenzen.</div>',

        partner(awin(8520, "bespaarvriend-huurtoeslag", "https://www.gaslicht.com/energievergelijken"), "Ook als huurder besparen op energie", "Ook als huurder kies je zelf. Vergelijk energiecontracten met de tarieven voor 2027.", "Vergelijk energiecontracten", [("3 jaar vast", awin(8520, "bespaarvriend-huurtoeslag", "https://www.gaslicht.com/energievergelijken/energiecontract-3-jaar-vast")), ("Dynamisch contract", awin(8520, "bespaarvriend-huurtoeslag", "https://www.gaslicht.com/energievergelijken/dynamisch-energiecontract-vergelijken"))]),
        [("/zorgtoeslag-2027/", "Zorgtoeslag 2027"), ("/kindgebonden-budget-2027/", "Kindgebonden budget 2027"), ("/administratie/", "Vaste lasten op orde")],
        [("Is mijn huur te hoog voor huurtoeslag?", "Nee, sinds 2026 niet meer. Je kunt huurtoeslag krijgen bij elke huur, zolang je inkomen en vermogen niet te hoog zijn en je in een zelfstandige woning woont. Over het deel boven de huurgrens krijg je geen toeslag."),
         ("Telt het vermogen van mijn partner mee?", "Vanaf 1 januari 2027 wel. Dan kijkt Dienst Toeslagen naar het vermogen van jou en je toeslagpartner samen."),
         ("Wanneer zijn de bedragen voor 2027 bekend?", "De overheid maakt de huurgrens en inkomensgrenzen voor het nieuwe jaar meestal eind november of in december bekend. Wij werken deze pagina dan bij."),
         ("Waar vraag ik huurtoeslag aan?", "Via Mijn toeslagen op toeslagen.nl, met je DigiD. Aanvragen is gratis.")],
        [("https://www.rijksoverheid.nl/actueel/nieuws/2025/11/24/meer-mensen-in-aanmerking-huurtoeslag", "Rijksoverheid"), ("https://www.belastingdienst.nl/wps/wcm/connect/nl/huurtoeslag/content/maximaal-vermogen-huurtoeslag", "Belastingdienst (vermogen)"), ("https://aedes.nl/huurbeleid-en-betaalbaarheid/huurbeleid-2027", "Aedes (huurbeleid 2027)")],
        "Huurtoeslag 2027: wat verandert er en heb jij recht?", "Huurtoeslag 2027: je huur is nooit meer te hoog, en vanaf 1 januari telt ook het vermogen van je partner mee. Zo check je in 4 stappen of je recht hebt.")
    artikel("/kindgebonden-budget-2027/", "Kindgebonden budget 2027", "toeslag",
        "Kindgebonden budget 2027: minder bij een inkomen boven € 60.000",
        "Verdien je samen meer dan zo’n € 60.000? Dan krijg je vanaf 2027 minder kindgebonden budget, of helemaal niets meer. Ook de vermogensgrens gaat flink omlaag. Check het vóór 8 december.",
        [("12,35%", "afbouw boven het tweede inkomenspunt"), ("€ 61.917", "dat inkomenspunt in 2027"), ("€ 119.122", "vermogensgrens zonder partner"), ("8 dec", "uiterlijk wijzigingen doorgeven")],
        '<h2>Wat verandert er in 2027?</h2><ul>'
        '<li><b>Snellere afbouw bij hogere inkomens.</b> Boven een inkomen van € 61.917 gaat er 12,35% van elke extra euro van je kindgebonden budget af, tot het op is. Gezinnen die het raakt, krijgen gemiddeld zo’n € 670 per jaar minder.</li>'
        '<li><b>Lagere vermogensgrens.</b> Op 1 januari 2027 mag je zonder toeslagpartner maximaal € 119.122 vermogen hebben, met toeslagpartner € 158.748. In 2026 was dat nog € 146.011 en € 184.633.</li>'
        '<li><b>Kinderbijslag iets hoger.</b> Daar staat tegenover dat de kinderbijslag voor iedereen licht omhoog gaat.</li></ul>'
        '<h2>Zo voorkom je dat je moet terugbetalen</h2><ol class="stappen">'
        '<li><b>Tel je vermogen op 1 januari 2027.</b> Spaargeld, beleggingen en een tweede huis tellen mee, min je schulden.</li>'
        '<li><b>Schat je inkomen voor 2027.</b> Krijg je loonsverhoging of ga je meer werken? Dan kan je budget lager uitvallen.</li>'
        '<li><b>Pas het aan in Mijn toeslagen</b> op toeslagen.nl, uiterlijk 8 december 2026. Dan klopt je voorschot vanaf januari.</li>'
        '<li><b>Controleer je beschikking</b> die je eind december krijgt. Klopt er iets niet, geef het dan meteen door.</li></ol>'
        '<div class="let"><b>Let op:</b> kindgebonden budget hoef je niet apart aan te vragen als je kinderbijslag krijgt. Het wordt automatisch berekend, dus je gegevens moeten wel kloppen.</div>',

        partner(awin(107738, "bespaarvriend-kgb", "https://www.poliswijzer.nl/zorgverzekering"), "Zorgverzekering voor het gezin vergelijken", "Kinderen tot 18 zijn gratis meeverzekerd. Overstappen kan nog tot 31 december.", "Vergelijk zorgverzekeringen"),
        [("/zorgtoeslag-2027/", "Zorgtoeslag 2027"), ("/huurtoeslag-2027/", "Huurtoeslag 2027"), ("/administratie/", "Vaste lasten op orde")],
        [("Krijg ik in 2027 minder kindgebonden budget?", "Als jullie inkomen boven ongeveer € 61.917 ligt wel. Daarboven gaat 12,35% van elke extra euro van het budget af, tot het op is."),
         ("Wat is de vermogensgrens voor 2027?", "€ 119.122 zonder toeslagpartner en € 158.748 met toeslagpartner, gemeten op 1 januari 2027."),
         ("Moet ik kindgebonden budget aanvragen?", "Meestal niet. Krijg je kinderbijslag, dan berekent Dienst Toeslagen het automatisch. Je moet wel je inkomen en vermogen goed doorgeven."),
         ("Wat als ik te veel vermogen heb?", "Dan heb je dat hele jaar geen recht. Geef het uiterlijk 8 december 2026 door in Mijn toeslagen, anders moet je het voorschot later terugbetalen.")],
        [("https://www.rijksoverheid.nl/actueel/nieuws/2025/10/06/internetconsultatie-minder-kindgebonden-budget-voor-hogere-inkomens-in-2027", "Rijksoverheid"), ("https://www.eerstekamer.nl/nonav/behandeling/20260917/nota_van_wijziging_tweede_nota_van/document3/f=/vn0zmz4cg0yw.pdf", "Eerste Kamer (nota van wijziging)"), ("https://www.homefinance.nl/nieuws-blog/2026/deze-ouders-verliezen-in-januari-een-toeslag-waar-ze-jaren-recht-op-hadden-301972/", "HomeFinance")],
        "Kindgebonden budget 2027: minder bij inkomen boven € 60.000", "Kindgebonden budget 2027: boven € 61.917 inkomen gaat 12,35% af, en de vermogensgrens daalt naar € 119.122. Check het vóór 8 december en voorkom terugbetalen.")
    artikel("/energierekening-verlagen/", "Energierekening verlagen", "energie",
        "Energierekening verlagen in 2027: 8 tips die echt schelen",
        "In 2027 stijgt je energierekening met gemiddeld zo’n € 149, vooral door hogere netbeheerkosten. Met deze tips haal je dat er ruim uit, zonder in de kou te zitten.",
        [("+ € 149", "gemiddeld duurder in 2027"), ("€ 0,7457", "energiebelasting gas per m³"), ("€ 0,1065", "energiebelasting stroom per kWh"), ("€ 628,69", "vaste korting op je rekening")],
        '<h2>8 tips om minder te betalen</h2><ol class="stappen">'
        '<li><b>Vergelijk je contract.</b> Loopt je contract af of heb je een variabel tarief? Overstappen is vaak de grootste besparing in één keer.</li>'
        '<li><b>Zet de verwarming een graad lager.</b> Eén graad lager scheelt ongeveer 6% gas. Een slimme thermostaat helpt je dat vol te houden.</li>'
        '<li><b>Korter douchen.</b> Een paar minuten minder per dag scheelt al snel tientallen euro’s gas per jaar. Een waterbesparende douchekop helpt ook.</li>'
        '<li><b>Dicht de kieren.</b> Tochtstrips en een tochtrol onder de deur zijn goedkoop en houden de warmte binnen.</li>'
        '<li><b>Radiatorfolie achter de verwarming</b> aan een buitenmuur kaatst de warmte terug de kamer in.</li>'
        '<li><b>Sluipverbruik eruit.</b> Apparaten op stand-by verbruiken het hele jaar door stroom. Een stekkerdoos met schakelaar lost dat op.</li>'
        '<li><b>Wassen op 30 graden</b> en de droger laten staan als het kan. Dat scheelt veel stroom.</li>'
        '<li><b>Pas je termijnbedrag aan.</b> Te hoog betaal je voor niets vooruit, te laag geeft een naheffing. Kijk elk kwartaal even in de app van je leverancier.</li></ol>'
        '<div class="let"><b>Zonnepanelen?</b> Vanaf 1 januari 2027 stopt het salderen. Lees <a href="/salderen-2027/">wat het einde van salderen voor jou betekent</a>.</div>',
        widget("energie", "Energie vergelijken") + dynamisch_blok("bespaarvriend-energierekening") + partner(awin(8520, "bespaarvriend-energierekening", "https://www.gaslicht.com/energievergelijken"), "Energiecontracten vergelijken", "Vergelijk contracten van alle grote leveranciers, met de tarieven voor 2027.", "Vergelijk energiecontracten", [("3 jaar vast", awin(8520, "bespaarvriend-energierekening", "https://www.gaslicht.com/energievergelijken/energiecontract-3-jaar-vast")), ("Dynamisch contract", awin(8520, "bespaarvriend-energierekening", "https://www.gaslicht.com/energievergelijken/dynamisch-energiecontract-vergelijken"))]),
        [("/energie-2027/", "Energie 2027: alles wat verandert"), ("/salderen-2027/", "Einde salderen 2027"), ("/energiecontract-opzeggen/", "Energiecontract opzeggen")],
        [("Waarom wordt mijn energierekening duurder in 2027?", "Vooral door hogere netbeheerkosten. De energiebelasting op gas stijgt iets, die op stroom daalt iets. Per saldo betaalt een gemiddeld huishouden ongeveer € 149 per jaar meer."),
         ("Wat is de vermindering energiebelasting?", "Een vaste korting op je energierekening van € 628,69 in 2027 (inclusief btw). Je leverancier trekt die automatisch af."),
         ("Wat levert één graad lager op?", "Ongeveer 6% minder gas voor verwarming. Bij een gemiddeld verbruik is dat al snel tientallen euro’s per jaar."),
         ("Is overstappen de moeite waard?", "Vaak wel, vooral als je contract afloopt of je een duur variabel tarief hebt. Vergelijk op de tarieven voor 2027 en let bij zonnepanelen op de terugleververgoeding.")],
        [("https://www.keuze.nl/nieuws/energiebelasting-2027-stijgt-toch", "Keuze.nl"), ("https://www.rijksoverheid.nl/onderwerpen/energie-thuis/energierekening-van-huishoudens", "Rijksoverheid"), ("https://www.milieucentraal.nl/energie-besparen/", "Milieu Centraal")],
        "Energierekening verlagen in 2027: 8 tips die echt schelen", "Je energierekening stijgt in 2027 met zo’n € 149. Met deze 8 tips betaal je minder: contract vergelijken, een graad lager, kieren dichten en sluipverbruik eruit.")
    artikel("/salderen-2027/", "Einde salderen 2027", "zon",
        "Einde salderen in 2027: wat betekent het voor jouw zonnepanelen?",
        "Op 1 januari 2027 stopt de salderingsregeling in één keer. Stroom die je teruglevert, mag je dan niet meer wegstrepen tegen je verbruik. Zo zie je wat het jou kost en wat je eraan kunt doen.",
        [("1 jan 2027", "salderen stopt in één keer"), ("Min. 50%", "terugleververgoeding van de kale stroomprijs"), ("Tot 2030", "geldt die wettelijke ondergrens"), ("Gratis", "opzeggen als je leverancier de voorwaarden wijzigt")],
        f'<div class="kaart tool"><span class="ic">{ICON["zon"]}</span><div><b>Reken uit wat het jou kost</b><p>Met de gratis <b>Salderingscheck</b> zie je wat het einde van salderen jou per jaar kost, en of een thuisbatterij zich terugverdient. Ook gemaakt door Erik, de maker van Bespaarvriend.</p><a class="btn" href="https://salderingscheck-nl.netlify.app/?bron=bespaarvriend">Naar de Salderingscheck{ICON["pijl"]}</a></div></div>'
        '<h2>Wat verandert er op 1 januari 2027?</h2><ul>'
        '<li><b>Niet meer wegstrepen.</b> Je betaalt voor alle stroom die je van het net haalt, ook als je op andere momenten stroom hebt teruggeleverd.</li>'
        '<li><b>Terugleververgoeding.</b> Voor elke kWh die je teruglevert krijg je minimaal 50% van de kale leveringsprijs (zonder energiebelasting en btw). Die ondergrens geldt tot 2030. Leveranciers mogen meer bieden.</li>'
        '<li><b>Terugleverkosten blijven, maar lager.</b> Leveranciers mogen alleen nog de echte kosten rekenen, per teruggeleverde kWh op de factuur. Je moet er netto altijd iets aan overhouden.</li>'
        '<li><b>Kosteloos opzeggen.</b> Wijzigt je leverancier de voorwaarden per 1 januari 2027 en ben je het er niet mee eens? Dan mag je tussentijds gratis opzeggen.</li></ul>'
        '<h2>Zo beperk je de schade</h2><ol class="stappen">'
        '<li><b>Gebruik je eigen stroom.</b> Zet wasmachine, vaatwasser en droger aan als de zon schijnt, en laad de auto overdag. Elke kWh die je zelf gebruikt, hoef je niet duur in te kopen.</li>'
        '<li><b>Vergelijk op de tarieven vanaf 2027.</b> Kijk niet alleen naar de prijs per kWh, maar vooral naar de terugleververgoeding en de terugleverkosten.</li>'
        '<li><b>Reken een thuisbatterij eerst door.</b> Een batterij slaat overdag stroom op voor de avond. Of dat loont, hangt af van jouw verbruik en teruglevering. Reken het uit met de Salderingscheck.</li>'
        '<li><b>Overweeg een dynamisch contract.</b> Daarmee kun je stroom gebruiken als die goedkoop is. Dat past vooral als je je verbruik kunt verschuiven.</li></ol>',
        widget("energie", "Energie vergelijken") + batterij_blok("bespaarvriend-saldering") + dynamisch_blok("bespaarvriend-saldering") + partner(awin(8520, "bespaarvriend-saldering", "https://www.gaslicht.com/energievergelijken"), "Energiecontracten vergelijken", "Vergelijk contracten met de terugleververgoeding en terugleverkosten vanaf 2027.", "Vergelijk energiecontracten", [("3 jaar vast", awin(8520, "bespaarvriend-saldering", "https://www.gaslicht.com/energievergelijken/energiecontract-3-jaar-vast")), ("Dynamisch contract", awin(8520, "bespaarvriend-saldering", "https://www.gaslicht.com/energievergelijken/dynamisch-energiecontract-vergelijken"))]),
        [("/energie-2027/", "Energie 2027: alles wat verandert"), ("/energiecontract-opzeggen/", "Energiecontract opzeggen")],
        [("Stopt salderen echt op 1 januari 2027?", "Ja. De salderingsregeling stopt in één keer op 1 januari 2027, zonder geleidelijke afbouw. Tot en met 31 december 2026 saldeer je nog volledig."),
         ("Hoeveel krijg ik nog voor teruggeleverde stroom?", "Minimaal 50% van de kale leveringsprijs, dus zonder energiebelasting en btw. Die ondergrens geldt tot 2030. Sommige leveranciers bieden meer."),
         ("Loopt mijn contract door in 2027, wat dan?", "Dan geldt tot en met december 2026 nog volledig salderen. Vanaf januari 2027 rekent je leverancier verbruik en teruglevering apart af."),
         ("Loont een thuisbatterij nu wel?", "Dat hangt af van hoeveel stroom je teruglevert en wanneer je die zelf gebruikt. Met de Salderingscheck reken je het voor jouw situatie uit.")],
        [("https://www.keuze.nl/nieuws/salderingsregeling-zonnepanelen-definitief-van-de-baan-per-2027-dit-zijn-de-gevolgen", "Keuze.nl"), ("https://www.gaslicht.com/blog/salderingsregeling-afgeschaft-gevolgen/", "Gaslicht.com"), ("https://selectra.nl/energie/zonnepanelen/salderingsregeling", "Selectra"), ("https://solarmagazine.nl/nieuws-zonne-energie/i44687/eigenaren-zonnepanelen-weten-eindelijk-waar-ze-aan-toe-zijn-terugleverkosten-moeten-vanaf-2027-per-kilowattuur-op-factuur", "Solar Magazine")],
        "Einde salderen 2027: wat het kost en wat je kunt doen", "Salderen stopt op 1 januari 2027. Je krijgt minimaal 50% van de kale stroomprijs terug, tot 2030. Zo beperk je de schade, en reken uit wat het jou kost.")
    artikel("/sim-only-overstappen/", "Sim only overstappen", "mobiel",
        "Sim only overstappen met nummerbehoud: zo houd je je 06-nummer",
        "Overstappen naar een goedkoper sim only-abonnement is makkelijk, en je eigen nummer gaat gewoon mee. Zeg je oude abonnement alleen niet zelf op.",
        [("120 dagen", "voor einddatum kun je al overstappen"), ("Gratis", "nummerbehoud bij de meeste providers"), ("1 maand", "opzegtermijn na de contractperiode"), ("14 dagen", "bedenktijd bij online afsluiten")],
        '<h2>Zo stap je over</h2><ol class="stappen">'
        '<li><b>Kijk wanneer je contract afloopt.</b> Dat staat in je account bij je huidige provider.</li>'
        '<li><b>Kies een nieuw abonnement.</b> Kijk hoeveel data je echt gebruikt; veel mensen betalen voor een bundel die ze niet halen.</li>'
        '<li><b>Vraag nummerbehoud aan</b> bij je nieuwe provider. Dat kan bij veel providers al vanaf 120 dagen voor je einddatum.</li>'
        '<li><b>Zeg niet zelf op.</b> De nieuwe provider regelt de overstap en zegt je oude abonnement op. Zeg je zelf op, dan kun je je nummer kwijtraken.</li>'
        '<li><b>Wissel van simkaart</b> zodra je oude simkaart geen bereik meer heeft. Je nummer staat dan op je nieuwe simkaart.</li></ol>'
        '<div class="let"><b>Let op:</b> zit je nog midden in een contract? Dan betaal je bij eerder overstappen vaak de resterende maanden. Wacht dan tot het einde, of reken uit wat het scheelt.</div>',
        sim,
        [("/internet-en-mobiel/", "Internet en mobiel: stop met te veel betalen"), ("/refurbished-telefoon-kopen/", "Refurbished telefoon kopen")],
        [("Kan ik mijn nummer meenemen naar een andere provider?", "Ja, elke mobiele provider biedt nummerbehoud aan, ook als je van prepaid naar sim only gaat. Je vraagt het aan bij je nieuwe provider."),
         ("Moet ik mijn oude abonnement zelf opzeggen?", "Nee. Bij overstappen met nummerbehoud zegt de nieuwe provider je oude abonnement op. Zeg je zelf op, dan loop je het risico dat je nummer vervalt."),
         ("Hoe vroeg kan ik overstappen?", "Bij de meeste providers vanaf ongeveer 4 maanden (120 dagen) voor de einddatum van je contract. Het nieuwe abonnement gaat in als het oude afloopt.")],
        [("https://www.keuze.nl/telefoon-abonnement/informatie/nummerbehoud", "Keuze.nl"), ("https://www.belsimpel.nl/klantenservice/abonnementen/nummerbehoud", "Belsimpel (120 dagen)"), ("https://www.overstappen.nl/overstappen", "Overstappen.nl"), ("https://www.consuwijzer.nl/vergelijken-en-overstappen/telecom/telefoonnummer-meenemen", "ACM ConsuWijzer")],
        "Sim only overstappen met nummerbehoud: stappenplan", "Sim only overstappen en je 06-nummer houden: vraag nummerbehoud aan bij je nieuwe provider, tot 120 dagen voor je einddatum. Zeg je oude abonnement niet zelf op.")

    schrijf_agenda()
    # ---------- sitemap, robots, llms.txt ----------
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                + "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{VANDAAG}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES) + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/elektronica/sitemap.xml\n")
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(f"""# Bespaarvriend
> Gratis, onafhankelijke uitleg over besparen op vaste lasten in Nederland. Gemaakt door Erik Beltman (ook maker van boodschappenvergelijk.nl). Bijgewerkt op {BIJGEWERKT}.

- [Zorgverzekering 2027]({BASE}/zorgverzekering-2027/): gemiddelde premie € 173,13 per maand, laagste premie € 148,40, hoogste € 202,50, verschil € 649 per jaar; overstappen vóór 31 december 2026.
- [Eigen risico 2027]({BASE}/eigen-risico-2027/): verplicht eigen risico € 400 (2026: € 385), met rekenhulp vrijwillig eigen risico.
- [Zorgtoeslag 2027]({BASE}/zorgtoeslag-2027/): maximaal € 140 per maand (alleenstaand), inkomensgrens ± € 42.950, vermogensgrens € 119.122.
- [Belastingen 2027]({BASE}/belastingen-2027/): overzicht in gewone taal; Tweede Kamer stemde 12 november 2026, Eerste Kamer rond 16 december; halvering heffingsvrij vermogen geschrapt (± € 60.280 p.p.); accijnskorting benzine/diesel verlengd tot eind 2027 (voorstel), niet voor LPG; vliegbelasting per afstand.\n- [Wegenbelasting 2027]({BASE}/wegenbelasting-2027/): elektrische personenauto 30% korting in 2027 en 2028, 25% in 2029; camper halftarief alleen nog automatisch met RDW-registratie M + SA; bestelauto particulier moet N1 zijn.\n- [Noodfonds Energie 2027]({BASE}/noodfonds-energie-2027/): aanvragen 4 januari t/m 7 mei 2027; € 120 tot € 1.800 steun; inkomen tot 130% sociaal minimum en energiequote 8% of hoger.\n- [ISDE subsidie 2027]({BASE}/isde-subsidie-2027/): opent 5 januari 2027 12.00 uur; € 200 extra voor slimme warmtepomp; lucht-waterwarmtepomp vóór 31 december 2026 kopen = oud tarief.\n- [Kinderopvangtoeslag 2027]({BASE}/kinderopvangtoeslag-2027/): maximaal 96% tot ± € 72.000 inkomen; max. uurprijs dagopvang € 11,60, BSO € 10,31, gastouder € 8,77 (voorlopig).\n- [Belastingaangifte tips]({BASE}/belastingaangifte-tips/): aangifte 1 maart tot 1 mei (uitstel tot 1 september); vóór 1 april insturen geeft meestal bericht vóór 1 juli; vergeten aftrek tot 5 jaar terug.\n- [Kinderbijslag 2027]({BASE}/kinderbijslag-2027/): bedragen per leeftijd, betaling per kwartaal achteraf; Q4 2026 op 2 januari 2027; licht hoger in 2027.\n- [Huurverhoging 2027]({BASE}/huurverhoging-2027/): max. 4,1% sociale huur (1-7-2026 tot 1-7-2027), 6,1% middenhuur en 4,4% vrije sector (2026).\n- [Abonnementen opzeggen]({BASE}/abonnementen-opzeggen/): na de eerste periode max. 1 maand opzegtermijn; online afgesloten is online opzeggen.\n- [Goedkoop boodschappen doen]({BASE}/goedkoop-boodschappen-doen/): 10 tips, met vergelijking van 12 supermarkten op boodschappenvergelijk.nl.\n- [Huurtoeslag 2027]({BASE}/huurtoeslag-2027/): sinds 2026 geen maximale huur meer als voorwaarde; vanaf 1 januari 2027 telt het vermogen van de toeslagpartner mee.
- [Kindgebonden budget 2027]({BASE}/kindgebonden-budget-2027/): afbouw 12,35% boven € 61.917 inkomen; vermogensgrens € 119.122 (zonder partner) en € 158.748 (met partner); wijzigingen doorgeven vóór 8 december 2026.
- [Energierekening verlagen]({BASE}/energierekening-verlagen/): energierekening 2027 gemiddeld € 149 duurder; energiebelasting gas € 0,7457/m³, stroom € 0,1065/kWh, vermindering € 628,69; 8 bespaartips.
- [Einde salderen 2027]({BASE}/salderen-2027/): salderen stopt in één keer op 1 januari 2027; terugleververgoeding minimaal 50% van de kale leveringsprijs tot 2030; tips en rekenhulp.
- [Energie 2027]({BASE}/energie-2027/): salderen stopt 1 januari 2027; energiebelasting gas € 0,7457/m³, stroom € 0,1065/kWh, vermindering € 628,69; netbeheer gemiddeld + € 141.
- [Aanvullende verzekering 2027]({BASE}/aanvullende-verzekering-2027/): wanneer een aanvullende verzekering loont, met rekenhulp; premies 2027 bekend sinds 19 november 2026.
- [Tandartsverzekering 2027]({BASE}/tandartsverzekering-2027/): bij 102 van de 110 tandpakketten is de premie hoger dan de vergoeding bij gemiddelde kosten; rekenhulp.
- [Energiecontract opzeggen]({BASE}/energiecontract-opzeggen/): opzegtermijn maximaal 30 dagen, geen opzegvergoeding bij variabel; vergoeding bij vast hangt af van prijsverschil.
- [Zorgverzekering overstappen]({BASE}/zorgverzekering-overstappen/): stappenplan; opzeggen vóór 31 december 2026, nieuwe polis uiterlijk 31 januari 2027.
- [Fysiotherapie vergoeding 2027]({BASE}/fysiotherapie-vergoeding-2027/): volwassenen uit de basis alleen bij chronische aandoening vanaf de 21e behandeling; kinderen 9 (+9) behandelingen.
- [Reisverzekering doorlopend of kortlopend]({BASE}/reisverzekering-doorlopend-of-kortlopend/): één reis per jaar vaak kortlopend; vanaf ±16–21 reisdagen per jaar doorlopend.
- [Goedkoop vliegen]({BASE}/goedkoop-vliegen/): 8 tips, o.a. flexibele datum, andere vliegvelden en totaalprijs met bagage.
- [Refurbished telefoon kopen]({BASE}/refurbished-telefoon-kopen/): garantie 6 maanden tot 3 jaar, wettelijke garantie, 14 dagen bedenktijd, accu en updates.
- [Autoverzekering besparen]({BASE}/autoverzekering-besparen/): dekking per leeftijd auto (allrisk tot 6 jaar, beperkt casco 6–10, WA 10+).
- [Sim only overstappen]({BASE}/sim-only-overstappen/): nummerbehoud via nieuwe provider, tot 120 dagen voor einddatum; niet zelf opzeggen.
- [Internet en mobiel]({BASE}/internet-en-mobiel/): na de contractperiode maximaal 1 maand opzegtermijn; 79% van de internetabonnementen loopt al door na de contractperiode.
- [Alles op orde](https://allesoporde.netlify.app/): gratis overzicht van je vaste lasten en inkomsten.
- [Bonnenboek](https://bonnenboek.netlify.app/): gratis app om kassabonnen te scannen en boodschappenuitgaven bij te houden, samen met je huishouden.
- [Salderingscheck](https://salderingscheck-nl.netlify.app/): rekent uit wat het einde van salderen per jaar kost en of een thuisbatterij loont.
- [Tankwijzer](https://goedkopertanken.netlify.app/): brandstofprijzen vergelijken in Nederland, België en Duitsland.
- [Vluchtwijzer](https://vluchtwijzer.netlify.app/): goedkope vluchten vergelijken.
- [EuroRoadRules](https://euroroadrules.eu/): vignetten, tol en milieuzones in Europa.
- [Vakantiewijzer](https://vakantietoppers.netlify.app/): pakketreizen, hotels, vakantieparken en campings vergelijken.
- [Elektrovergelijk](https://bespaarvriend.nl/elektronica/): elektronica en witgoed vergelijken bij Nederlandse webwinkels, inclusief verzendkosten.
- [Foutcodezoeker](https://foutcodezoeker.nl/): foutcodes en reparatie-uitleg voor apparaten.
- [Boodschappen vergelijken](https://boodschappenvergelijk.nl/): dagelijkse prijzen van supermarkten.
""")
    print(f"klaar: {len(PAGES)} pagina's in {OUT}")


def bouw_elektronica():
    """Elektrovergelijk draait als onderdeel van Bespaarvriend onder /elektronica/."""
    import subprocess, sys
    hier = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, SITE_BASIS="/elektronica", SITE_DOMEIN=BASE + "/elektronica")
    subprocess.run([sys.executable, os.path.join(hier, "elektronica", "scripts", "build.py"), os.path.join(OUT, "elektronica")], env=env, check=True)

if __name__ == "__main__":
    bouw()
    bouw_elektronica()
