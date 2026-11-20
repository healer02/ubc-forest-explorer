// Species content, photos and campus locations, plus the "needs check" logic.
import { getAll, get, put, del } from './db.js';

let cache;

export async function loadContent() {
  if (cache) return cache;
  const load = async (name) => {
    const res = await fetch(`data/${name}.json`);
    if (!res.ok) throw new Error(`Could not load ${name} (${res.status}).`);
    return res.json();
  };
  const [species, photos, locations] = await Promise.all([load('species'), load('photos'), load('locations')]);
  const ROLE_ORDER = ['leaf', 'bark', 'form', 'flower', 'fruit', 'seasonal'];
  for (const list of Object.values(photos.photos)) {
    list.sort((a, b) => ROLE_ORDER.indexOf(a.role) - ROLE_ORDER.indexOf(b.role));
  }
  cache = {
    meta: species,
    species: species.species,
    byId: new Map(species.species.map((s) => [s.id, s])),
    photos: photos.photos,
    locations,
  };
  return cache;
}

// ---------- labels ----------
export const GROUP_LABEL = { conifer: 'Conifer', broadleaf: 'Broadleaf', ginkgo: 'Ginkgo (neither)' };

export function featureLabel(type, group) {
  if (type === 'fruit') return group === 'conifer' ? 'Cone' : 'Fruit';
  return { leaf: 'Leaf', bark: 'Bark', form: 'Form', flower: 'Flower', seasonal: 'Seasonal cue' }[type] || type;
}

export function largestText(big) {
  if (!big) return '';
  const h = big.height_m ? `, ${big.height_m} m tall` : '';
  return `Largest recorded: ${big.dbh_cm} cm DBH${h}, ${big.label} (inventory value)`;
}

// ---------- verification ----------
// Every drafted item has a key such as "thuja-plicata|id_features.0".
// A verification is stored with a fingerprint of the text you checked; if the
// text is later changed, the item goes back to "needs check" automatically.
export function checkItems(s, locations) {
  const items = [];
  const add = (path, text) => { if (text) items.push({ key: `${s.id}|${path}`, text }); };
  add('native', s.native.text);
  s.id_features.forEach((f, i) => add(`id_features.${i}`, f.text));
  s.lookalikes.forEach((l, i) => add(`lookalikes.${i}`, `${l.name}: ${l.text}`));
  for (const k of ['design', 'ecology', 'controversy', 'tour_point']) add(k, s[k].text);
  const big = locations && locations[s.id] && locations[s.id].largest_needs_check;
  if (big) add('largest', largestText(big));
  return items;
}

export function fingerprint(text) {
  let h = 5381;
  for (let i = 0; i < text.length; i++) h = ((h << 5) + h + text.charCodeAt(i)) | 0;
  return (h >>> 0).toString(36);
}

export async function verifiedMap() {
  const recs = await getAll('verify');
  return new Map(recs.map((r) => [r.key, r]));
}

export const isVerified = (vmap, item) => {
  const r = vmap.get(item.key);
  return !!r && r.fp === fingerprint(item.text);
};

export async function toggleVerified(item) {
  const r = await get('verify', item.key);
  if (r && r.fp === fingerprint(item.text)) {
    await del('verify', item.key);
    return false;
  }
  await put('verify', { key: item.key, fp: fingerprint(item.text), at: new Date().toISOString() });
  return true;
}

// ---------- daily picks ----------
export function dayNumber(d = new Date()) {
  return Math.floor((d.getTime() - d.getTimezoneOffset() * 60000) / 86400000);
}

// A fixed shuffle, so every species comes up once every 26 days in a varied order.
function fixedOrder(n, seed) {
  const idx = [...Array(n).keys()];
  let x = seed;
  for (let i = n - 1; i > 0; i--) {
    x = (Math.imul(x, 1103515245) + 12345) & 0x7fffffff;
    const j = x % (i + 1);
    [idx[i], idx[j]] = [idx[j], idx[i]];
  }
  return idx;
}

export function speciesOfDay(content, day = dayNumber()) {
  const order = fixedOrder(content.species.length, 2027);
  return content.species[order[day % order.length]];
}

export function controversyOfDay(content, day = dayNumber()) {
  const pool = content.species.filter((s) => s.controversy.text);
  const order = fixedOrder(pool.length, 444);
  let pick = pool[order[day % order.length]];
  if (pick.id === speciesOfDay(content, day).id) pick = pool[order[(day + 1) % order.length]];
  return pick;
}
