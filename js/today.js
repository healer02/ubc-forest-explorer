// Today: dashboard, species of the day, today's controversy, Start review.
import { getAll, count } from './db.js';
import { speciesOfDay, controversyOfDay, checkItems, verifiedMap, isVerified, dayNumber } from './content.js';
import { esc, checkChip, firstPhoto } from './ui.js';

const MASTERED_DAYS = 21; // a species counts as mastered when all its cards are spaced 3+ weeks apart

export async function dashboardStats(content) {
  const [cards, reviews, observations] = await Promise.all([getAll('cards'), getAll('reviews'), count('observations')]);
  const now = Date.now();
  const bySpecies = new Map();
  for (const c of cards) {
    if (!bySpecies.has(c.speciesId)) bySpecies.set(c.speciesId, []);
    bySpecies.get(c.speciesId).push(c);
  }
  let mastered = 0;
  for (const list of bySpecies.values()) if (list.every((c) => (c.interval || 0) >= MASTERED_DAYS)) mastered++;
  const due = cards.filter((c) => c.due <= now).length;

  const days = new Set(reviews.map((r) => dayNumber(new Date(r.at))));
  let d = dayNumber();
  if (!days.has(d)) d -= 1; // today's review not done yet: the streak is still alive
  let streak = 0;
  while (days.has(d)) { streak++; d--; }

  return { mastered, total: content.species.length, due, observations, streak, hasCards: cards.length > 0 };
}

export async function todayView(root, content) {
  const st = await dashboardStats(content);
  const sp = speciesOfDay(content);
  const cv = controversyOfDay(content);
  const vmap = await verifiedMap();
  const cvItem = checkItems(cv, content.locations).find((i) => i.key.endsWith('|controversy'));
  const photo = firstPhoto(content, sp.id, 'leaf');
  const dateLabel = new Date().toLocaleDateString('en-CA', { weekday: 'long', day: 'numeric', month: 'long' });
  const blurb = sp.tour_point.text || sp.ecology.text || '';

  root.innerHTML = `
    <header class="page-head">
      <p class="eyebrow">${esc(dateLabel)}</p>
      <h1>Today</h1>
    </header>

    <section class="stats" aria-label="Your progress">
      <div class="stat"><b>${st.mastered}</b><span>Mastered</span><small>of ${st.total} species</small></div>
      <div class="stat"><b>${st.due}</b><span>Due</span><small>cards to review</small></div>
      <div class="stat"><b>${st.observations}</b><span>Observations</span><small>your field notes</small></div>
      <div class="stat"><b>${st.streak}</b><span>Day streak</span><small>${st.streak === 1 ? 'day' : 'days'} in a row</small></div>
    </section>

    <a class="card sotd" href="#/species/${esc(sp.id)}">
      ${photo ? `<img src="${esc(photo.file)}" alt="${esc(sp.common)}, ${esc(photo.role)}" loading="lazy">` : ''}
      <div class="sotd-body">
        <p class="eyebrow">Species of the day</p>
        <h2>${esc(sp.common)}</h2>
        <p class="latin">${esc(sp.botanical)}</p>
        <p class="clamp">${esc(blurb)}</p>
      </div>
    </a>

    <a class="card cv" href="#/species/${esc(cv.id)}/controversy">
      <p class="eyebrow">Today's controversy · ${esc(cv.common)}</p>
      <p class="cv-text">${esc(cv.controversy.text)}</p>
      ${cvItem ? checkChip(isVerified(vmap, cvItem)) : ''}
    </a>

    <div class="cta-wrap">
      <a class="cta" href="#/review">Start review${st.hasCards ? '' : '<small>Quiz arrives in Step 3</small>'}</a>
    </div>
  `;
}
