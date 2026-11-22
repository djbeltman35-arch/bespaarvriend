// Matcher v2: zoekt per product (op fabrikantcode of naam) in de winkel waar deze tab op staat,
// controleert de productpagina en stuurt de resultaten naar /api/dump.
// Gebruik: window.__S={shop:'bol',search:'/nl/nl/s/?searchtext={q}',link:'/nl/nl/p/',wait:500,max:4}; window.__K='<sleutel>'; laad dit script.
(async () => {
  const S = window.__S, K = window.__K;
  const API = 'https://elektrovergelijk.netlify.app/api/dump?k=' + K + '&n=';
  const sl = ms => new Promise(r => setTimeout(r, ms));
  const P = h => new DOMParser().parseFromString(h, 'text/html');
  const norm = s => (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');
  const SYN = { zwart: ['zwart', 'black', 'midnight', 'middernacht', 'graphite', 'grafiet', 'space'], wit: ['wit', 'white', 'cloud'], blauw: ['blauw', 'blue', 'navy'], grijs: ['grijs', 'grey', 'gray', 'titanium', 'graphite', 'grafiet'], zilver: ['zilver', 'silver'], groen: ['groen', 'green', 'sage'], roze: ['roze', 'pink'], paars: ['paars', 'purple', 'lavender'] };
  const BAD = /refurb|gebruikt|tweedehands|hoesje|hoes |case|cover|screenprotector|bundel|bundle|renewed|sleeve|onderdeel|filter voor|vervang/i;
  const items = window.__ITEMS || JSON.parse(await (await fetch(API + 'items')).text());
  window.__m2 = { done: 0, tot: items.length, hit: 0, err: 0 };
  const res = {};
  function ld(d, html) {
    let o = null;
    d.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
      try {
        const walk = x => {
          if (!x || typeof x !== 'object' || o) return;
          if (Array.isArray(x)) return x.forEach(walk);
          const t = [].concat(x['@type'] || []);
          if ((t.includes('Product') || t.includes('ProductGroup')) && x.offers) {
            const of = [].concat(x.offers)[0];
            if (of['@type'] === 'AggregateOffer' && !S.agg) return;
            const ship = [].concat(of.shippingDetails || [])[0];
            o = { p: +(of.price ?? of.lowPrice), n: x.name || '', a: (of.availability || '').split('/').pop(), sel: (of.seller && of.seller.name) || '',
                  v: ship && ship.shippingRate ? +ship.shippingRate.value : null, g: x.gtin13 || x.gtin || x.ean || '', m: x.mpn || '' };
            return;
          }
          for (const k in x) if (typeof x[k] === 'object') walk(x[k]);
        };
        walk(JSON.parse(s.textContent));
      } catch (e) {}
    });
    if (!o && S.pricesel) {
      const el = d.querySelector(S.pricesel);
      if (el) {
        const t = el.textContent.replace(/\s/g, ''); const mm = t.match(/(\d{1,3}(?:\.\d{3})*|\d+)(?:,(\d{2}))?/);
        if (mm) o = { p: parseFloat(mm[1].replace(/\./g, '') + '.' + (mm[2] || '00')), n: ((S.namesel && d.querySelector(S.namesel)) || { textContent: d.title }).textContent.trim(), a: '',
                      sel: ((S.selsel && d.querySelector(S.selsel)) || { textContent: '' }).textContent.trim().slice(0, 40), v: null, g: '', m: '' };
      }
    }
    if (S.eigen) { const m = html.match(new RegExp(S.eigen)); o = m ? { ...(o || { n: d.title }), p: parseFloat(m[1].replace(/\./g, '').replace(',', '.')) } : null; }
    return o;
  }
  function tokensOk(it, txt) {
    const t = norm(txt);
    for (const w of it.t) { const alts = SYN[w] || (/^\d+gb$/.test(w) ? [w, w.replace('gb', 'go')] : [w]); if (!alts.some(a => t.includes(norm(a)))) return false; }
    const words = new Set((txt || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').split(/[^a-z0-9+]+/));
    for (const w of it.x || []) if (words.has(w)) return false;
    return true;
  }
  for (const it of items) {
    try {
      const q = it.q;
      const r = await fetch(S.search.replace('{q}', encodeURIComponent(q)), { credentials: 'include' });
      const h = await r.text(); const d = P(h);
      let links = [...new Set([...d.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(u => u && u.includes(S.link)).map(u => new URL(u, location.origin).pathname))];
      if (r.url && new URL(r.url).pathname.includes(S.link)) links.unshift(new URL(r.url).pathname);
      if (it.loose) { const f = links.filter(u => tokensOk({ t: it.t.filter(w => !SYN[w]), x: it.x }, decodeURIComponent(u))); links = f.length ? f : links.slice(0, 1); }
      links = links.slice(0, S.max || 2);
      for (const u of links) {
        await sl(S.wait || 500);
        const ph = await (await fetch(u, { credentials: 'include' })).text();
        const pd = P(ph); const o = ld(pd, ph);
        if (!o || !(o.p > 0)) continue;
        const name = o.n || pd.title;
        if (BAD.test(name) || BAD.test(u)) continue;
        const ratio = o.p / it.p;
        if (ratio < 0.55 || ratio > 1.8) continue;
        const mpnOk = it.m && it.m.length >= 5 && (norm(o.m) === it.m || norm(ph.replace(/<script[\s\S]*?<\/script>/gi, ' ')).includes(it.m) || norm(name + u).includes(it.m));
        const tokOk = !it.m || it.loose ? tokensOk(it, name + ' ' + u) : false;
        if (mpnOk || tokOk) { res[it.k] = [o.p, o.a, o.sel, o.v, u, name.slice(0, 120), o.g, mpnOk ? 'm' : 't']; window.__m2.hit++; break; }
      }
    } catch (e) { window.__m2.err++; }
    window.__m2.done++;
    if (window.__m2.done % 40 === 0) await fetch(API + S.shop, { method: 'POST', body: JSON.stringify(res) });
    await sl(S.wait || 500);
  }
  await fetch(API + S.shop, { method: 'POST', body: JSON.stringify(res) });
  window.__m2.klaar = 1;
})();
