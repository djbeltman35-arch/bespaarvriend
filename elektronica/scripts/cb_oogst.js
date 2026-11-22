// Coolblue-oogst: draai in een coolblue.nl-tab (Claude in Chrome).
// Zet eerst window.__K = '<dump-sleutel>' en window.__C = { '<onze-cat>': '<coolblue-pad>', ... }.
// Per categorie: /<pad>/filter pagina 1 en 2, daarna elke productpagina (JSON-LD + spec-tabel) → dump 'cb_<cat>'.
// Voortgang: window.__hst.
window.__hst = { done: 0, cats: 0, err: 0, cur: '' };
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  async function prod(u) {
    const h = await (await fetch(u)).text();
    const d = new DOMParser().parseFromString(h, 'text/html');
    const ld = [...d.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { return JSON.parse(s.textContent); } catch (e) {} }).flat().filter(Boolean);
    const P = ld.find(o => o['@type'] === 'Product');
    if (!P) return null;
    const sp = {};
    for (const th of d.querySelectorAll('th')) {
      const v = th.nextElementSibling; if (!v) continue;
      const k = th.textContent.trim().replace(/\s+/g, ' ');
      let val = v.textContent.trim().replace(/\s+/g, ' ');
      if (!val) { const a = v.querySelector('[aria-label]'); val = a ? a.getAttribute('aria-label') : ''; }
      if (k && val && k.length < 60 && !(k in sp)) sp[k] = val.slice(0, 120);
    }
    const o = Array.isArray(P.offers) ? P.offers[0] : P.offers || {};
    const id = +(u.match(/\/product\/(\d+)/) || [])[1];
    return { id, n: P.name, p: +o.price, a: (o.availability || '').split('/').pop(), b: P.brand && (P.brand.name || P.brand), mpn: sp['Fabrikantcode'] || P.mpn || '', sp };
  }
  for (const [cat, path] of Object.entries(window.__C)) {
    __hst.cur = cat;
    const urls = [];
    for (const pg of [1, 2]) {
      try {
        const t = await (await fetch('/' + path + '/filter' + (pg > 1 ? '?pagina=' + pg : ''))).text();
        for (const m of (t.match(/\/product\/\d+\/[^"'?#\s]+\.html/g) || [])) if (!urls.some(x => x.split('/')[2] === m.split('/')[2])) urls.push(m);
      } catch (e) {}
    }
    const res = [];
    for (let i = 0; i < urls.length; i += 3) {
      const r = await Promise.all(urls.slice(i, i + 3).map(u => prod(u).catch(() => { __hst.err++; return null; })));
      for (const x of r) if (x && x.p) res.push(x);
      __hst.done += 3; await sleep(250);
    }
    await fetch('https://elektrovergelijk.netlify.app/api/dump?k=' + __K + '&n=cb_' + cat, { method: 'POST', body: JSON.stringify(res) });
    __hst.cats++; __hst['n_' + cat] = res.length;
  }
  __hst.cur = 'KLAAR';
})();
