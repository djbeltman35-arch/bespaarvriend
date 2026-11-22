// Zoekt producten in de bol Marketing Catalog API. De sleutel staat alleen in Netlify (BOL_CLIENT_ID / BOL_CLIENT_SECRET).
const KEY_HASH = "4238cb78390f495e3626ee61089d4f95b1d2f8b58b878e173e4be1d466ef4f51";
async function sha(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
let tok = null, tokExp = 0;
async function token() {
  if (tok && Date.now() < tokExp) return tok;
  const id = (Netlify.env.get("BOL_CLIENT_ID") || "").trim(), sec = (Netlify.env.get("BOL_CLIENT_SECRET") || "").trim();
  if (!id || !sec) throw new Error("BOL_CLIENT_ID/BOL_CLIENT_SECRET ontbreken");
  const r = await fetch("https://login.bol.com/token?grant_type=client_credentials", { method: "POST", headers: { Authorization: "Basic " + btoa(id + ":" + sec), Accept: "application/json" } });
  const j = await r.json(); if (!j.access_token) throw new Error("token: " + r.status);
  tok = j.access_token; tokExp = Date.now() + (j.expires_in - 30) * 1000; return tok;
}
export default async (req) => {
  const u = new URL(req.url);
  if ((await sha(u.searchParams.get("k") || "")) !== KEY_HASH) return new Response("nee", { status: 403 });
  if (u.searchParams.get("diag")) { const i = (Netlify.env.get("BOL_CLIENT_ID") || ""), s = (Netlify.env.get("BOL_CLIENT_SECRET") || ""); return new Response(JSON.stringify({ namen: Object.keys(process.env).filter(x => /bol/i.test(x)), idLengte: i.length, idVorm: i.replace(/[0-9a-f]/gi, "x"), geheimLengte: s.length, spaties: /\s/.test(i + s) })); }
  try {
    const t = await token();
    const ean = u.searchParams.get("ean"), q = u.searchParams.get("q");
    const api = ean
      ? `https://api.bol.com/marketing/catalog/v1/products/${encodeURIComponent(ean)}?country-code=NL&include-offer=true&include-specifications=false`
      : `https://api.bol.com/marketing/catalog/v1/products/search?search-term=${encodeURIComponent(q)}&country-code=NL&include-offer=true&page-size=${u.searchParams.get("n") || 6}`;
    const r = await fetch(api, { headers: { Authorization: "Bearer " + t, Accept: "application/json", "Accept-Language": "nl" } });
    return new Response(await r.text(), { status: r.status, headers: { "Content-Type": "application/json" } });
  } catch (e) { return new Response(JSON.stringify({ fout: String(e) }), { status: 500 }); }
};
export const config = { path: "/api/bol" };
