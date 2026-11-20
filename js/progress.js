// Progress: species list (mastery levels arrive with the quiz in Step 3;
// your photos and the campus map arrive in Step 5).
import { checkItems, verifiedMap, isVerified } from './content.js';
import { esc, firstPhoto } from './ui.js';
import { APP_VERSION } from './ui.js';

export async function progressView(root, content) {
  const vmap = await verifiedMap();
  let done = 0, total = 0;
  const row = (s) => {
    const items = checkItems(s, content.locations);
    const v = items.filter((i) => isVerified(vmap, i)).length;
    done += v; total += items.length;
    const p = firstPhoto(content, s.id, 'leaf');
    return `<li><a href="#/species/${esc(s.id)}">
      ${p ? `<img src="${esc(p.file)}" alt="" loading="lazy">` : '<span class="noimg"></span>'}
      <span class="names"><b>${esc(s.common)}</b><i>${esc(s.botanical)}</i></span>
      <span class="vcount ${v === items.length ? 'all' : ''}" title="Verified items">${v}/${items.length}</span>
    </a></li>`;
  };
  const natives = content.species.filter((s) => s.native.value);
  const others = content.species.filter((s) => !s.native.value);
  const lists = `
    <section class="block flush">
      <h2 class="group-h">Native <span>${natives.length}</span></h2>
      <ul class="splist">${natives.map(row).join('')}</ul>
    </section>
    <section class="block flush">
      <h2 class="group-h">Non-native <span>${others.length}</span></h2>
      <ul class="splist">${others.map(row).join('')}</ul>
    </section>`;

  let storage = 'unknown';
  try { storage = (await navigator.storage?.persisted?.()) ? 'kept on this phone' : 'may be cleared by iOS if space runs low'; } catch (e) { /* ignore */ }

  root.innerHTML = `
    <header class="page-head">
      <h1>Progress</h1>
      <p class="sub">${content.species.length} species · <b>${done} of ${total}</b> content items verified</p>
    </header>
    ${lists}
    <section class="block about">
      <h2>Coming next</h2>
      <p>Mastery level for each species arrives with the quiz (Step 3). Your photos and the campus map arrive in Step 5.</p>
      <p class="small">Version ${APP_VERSION} · Your data is ${esc(storage)}. Backup export arrives in Step 6.</p>
      <p class="small">Seed photos: iNaturalist and Wikimedia Commons contributors (CC0, CC BY, public domain); credits on each photo. Tree locations: UBC campus tree inventory.</p>
    </section>
  `;
}
