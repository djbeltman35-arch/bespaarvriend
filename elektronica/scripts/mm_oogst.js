// MediaMarkt-oogst: draai in een mediamarkt.nl-tab. Zet window.__K (dump-sleutel); de categoriekaart staat in de dump als 'mm_map'
// ({onze-cat: ['/nl/category/...html', ...]}). Per categorie pagina 1-4 van elke MediaMarkt-categorie, dan elke productpagina
// (JSON-LD: naam, merk, EAN, prijs, verkoper) → dump 'mmb_<cat>'. Voortgang: window.__mst.
window.__mst = { cats: 0, cur: '', n: 0 };
(async () => {
  const K = window.__K, API = 'https://elektrovergelijk.netlify.app/api/dump?k=' + K + '&n=';
  const MAP = window.__MAP || JSON.parse(await (await fetch(API + 'mm_map')).text());
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const lds = d => [...d.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { return JSON.parse(s.textContent); } catch (e) { return null; } }).filter(Boolean);
  async function prod(u) {
    const d = new DOMParser().parseFromString(await (await fetch(u)).text(), 'text/html');
    let P = null;
    for (const o of lds(d)) { const x = o['@type'] === 'BuyAction' ? o.object : o; if (x && (x['@type'] === 'Product' || x['@type'] === 'ProductGroup')) { P = x; break; } }
    if (!P) return null;
    if (P['@type'] === 'ProductGroup' && P.hasVariant) P = P.hasVariant.find(v => (v.url || '') === u) || P.hasVariant[0];
    const o = [].concat(P.offers || [])[0] || {};
    return { id: 'mm' + (P.sku || (u.match(/-(\d+)\.html/) || [])[1]), n: P.name, p: +o.price, a: (o.availability || '').split('/').pop(), b: P.brand && (P.brand.name || P.brand), gtin: P.gtin13 || P.gtin || '', mpn: P.mpn || '', sel: (o.seller && o.seller.name) || '', url: u.replace('https://www.mediamarkt.nl', ''), sp: {} };
  }
  for (const [cat, urls] of Object.entries(MAP)) {
    __mst.cur = cat;
    const links = [];
    for (const cu of urls) for (let pg = 1; pg <= 4; pg++) {
      try {
        const d = new DOMParser().parseFromString(await (await fetch(cu + (pg > 1 ? '?page=' + pg : ''))).text(), 'text/html');
        const il = lds(d).find(o => o['@type'] === 'ItemList');
        const nieuw = (il ? il.itemListElement : []).map(e => e.item && e.item.url).filter(x => x && !links.includes(x));
        if (!nieuw.length) break;
        links.push(...nieuw);
      } catch (e) { break; }
      await sleep(150);
    }
    const res = [];
    for (let i = 0; i < links.length; i += 3) {
      const r = await Promise.all(links.slice(i, i + 3).map(u => prod(u).catch(() => null)));
      for (const x of r) if (x && x.p) res.push(x);
      await sleep(200);
    }
    await fetch(API + 'mmb_' + cat, { method: 'POST', body: JSON.stringify(res) });
    __mst.cats++; __mst.n += res.length; __mst['n_' + cat] = res.length;
  }
  __mst.cur = 'KLAAR';
})();
