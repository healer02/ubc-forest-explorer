// Species page: photos, ID features, look-alikes, stories, campus locations,
// and a "Needs check / Verified" button on every drafted item.
import { checkItems, verifiedMap, isVerified, toggleVerified, featureLabel, GROUP_LABEL, largestText, fingerprint } from './content.js';
import { esc, checkChip, toast } from './ui.js';

const ROLE_LABEL = { leaf: 'Leaf', bark: 'Bark', form: 'Form', flower: 'Flower', fruit: 'Fruit', seasonal: 'Seasonal' };

export async function speciesView(root, content, id, section) {
  const s = content.byId.get(id);
  if (!s) {
    root.innerHTML = `<p class="empty">That species isn’t in the list. <a href="#/progress">See all species</a></p>`;
    return;
  }
  const loc = content.locations[s.id] || { count: 0, spots: [] };
  const photos = content.photos[s.id] || [];
  const items = checkItems(s, content.locations);
  const byPath = new Map(items.map((i) => [i.key.split('|')[1], i]));
  const vmap = await verifiedMap();

  const vbtn = (path) => {
    const item = byPath.get(path);
    if (!item) return '';
    const v = isVerified(vmap, item);
    return `<button class="vbtn" type="button" data-key="${esc(item.key)}" aria-pressed="${v}" aria-label="${v ? 'Verified. Tap to mark as needs check' : 'Needs check. Tap to mark verified'}">${checkChip(v)}</button>`;
  };
  const story = (path, title, f, anchor) => `
    <div class="vitem" ${anchor ? `id="${anchor}"` : ''}>
      <h3>${title}</h3>
      ${f.text ? `<p>${esc(f.text)}</p>${vbtn(path)}` : '<p class="muted">Left blank: no confident fact yet.</p>'}
    </div>`;

  const slides = photos.map((p) => `
    <figure class="slide">
      <img src="${esc(p.file)}" alt="${esc(s.common)}: ${esc(ROLE_LABEL[p.role] || p.role)}" loading="lazy">
      <span class="role">${esc(ROLE_LABEL[p.role] || p.role)}</span>
      <figcaption><a href="${esc(p.link)}" target="_blank" rel="noopener">${esc(p.credit === 'no rights reserved' ? 'CC0' : p.credit)} · ${esc(p.source)}</a></figcaption>
    </figure>`).join('');

  root.innerHTML = `
    <a class="back" href="#/progress">‹ All species</a>
    ${photos.length ? `<div class="carousel-wrap"><div class="carousel" tabindex="0" aria-label="Photos of ${esc(s.common)}">${slides}</div><span class="counter" aria-hidden="true">1 / ${photos.length}</span></div>` : ''}

    <header class="sp-head">
      <h1>${esc(s.common)}</h1>
      <p class="latin">${esc(s.botanical)}</p>
      <div class="tags">
        <span class="tag ${s.native.value ? 'native' : 'nonnative'}">${s.native.value ? 'Native' : 'Non-native'}</span>
        <span class="tag">${esc(GROUP_LABEL[s.group] || s.group)}</span>
        <span class="tag">${loc.count} on campus</span>
      </div>
    </header>

    <div class="verify-summary" aria-live="polite"></div>

    <section class="block">
      <div class="vitem"><h3>Status</h3><p>${esc(s.native.text)}</p>${vbtn('native')}</div>
    </section>

    <section class="block">
      <h2>How to identify it</h2>
      ${s.id_features.map((f, i) => `
        <div class="vitem feature">
          <h3>${esc(featureLabel(f.type, s.group))}</h3>
          <p>${esc(f.text)}</p>${vbtn(`id_features.${i}`)}
        </div>`).join('')}
    </section>

    <section class="block">
      <h2>Look-alikes</h2>
      ${s.lookalikes.length ? s.lookalikes.map((l, i) => `
        <div class="vitem">
          <h3>${esc(l.name)}</h3>
          <p>${esc(l.text)}</p>${vbtn(`lookalikes.${i}`)}
        </div>`).join('') : '<p class="muted">None listed.</p>'}
    </section>

    <section class="block">
      <h2>Stories</h2>
      ${story('design', 'Design use or misuse', s.design)}
      ${story('ecology', 'Ecology', s.ecology)}
      ${story('controversy', 'Controversy', s.controversy, 'controversy')}
      ${story('tour_point', 'Tour talking point', s.tour_point)}
    </section>

    <section class="block">
      <h2>On campus</h2>
      <p>${loc.count} trees in the UBC inventory. Most are at:</p>
      <ol class="spots">${loc.spots.map((p) => `<li><span>${esc(p.label)}</span><b>${p.count}</b></li>`).join('')}</ol>
      ${loc.largest_needs_check ? `<div class="vitem"><p>${esc(largestText(loc.largest_needs_check))}</p>${vbtn('largest')}</div>` : ''}
    </section>
  `;

  const summary = root.querySelector('.verify-summary');
  const updateSummary = () => {
    const done = items.filter((i) => isVerified(vmap, i)).length;
    summary.innerHTML = `<div class="meter" role="img" aria-label="${done} of ${items.length} verified"><span style="width:${(100 * done) / items.length}%"></span></div>
      <p><b>${done} of ${items.length}</b> items verified</p>`;
  };
  updateSummary();

  root.addEventListener('click', async (e) => {
    const btn = e.target.closest('.vbtn');
    if (!btn) return;
    const item = items.find((i) => i.key === btn.dataset.key);
    const now = await toggleVerified(item);
    if (now) vmap.set(item.key, { key: item.key, fp: fingerprint(item.text) });
    else vmap.delete(item.key);
    btn.setAttribute('aria-pressed', String(now));
    btn.setAttribute('aria-label', now ? 'Verified. Tap to mark as needs check' : 'Needs check. Tap to mark verified');
    btn.innerHTML = checkChip(now);
    updateSummary();
    toast(now ? 'Marked verified' : 'Marked as needs check');
  });

  const carousel = root.querySelector('.carousel');
  if (carousel) {
    const counter = root.querySelector('.counter');
    carousel.addEventListener('scroll', () => {
      const i = Math.round(carousel.scrollLeft / carousel.clientWidth);
      counter.textContent = `${i + 1} / ${photos.length}`;
    }, { passive: true });
  }

  if (section) {
    const target = root.querySelector(`#${CSS.escape(section)}`);
    if (target) requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  }
}
