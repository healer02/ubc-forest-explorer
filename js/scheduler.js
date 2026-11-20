// Spaced-repetition scheduler: a simple SM-2 variant (the method Anki is built on).
//
// Each species has two cards:
//   photo   - see a leaf, bark or form photo, name the tree
//   reverse - see the name, recall the 3 key ID features
// The reverse card is added the day after you first pass the photo card.
//
// Ratings: Again (forgot), Hard, Good, Easy. New and forgotten cards go through
// short "learning" steps (1 min, 10 min) inside the session, then move to day
// intervals that grow by the card's ease factor (starts at 2.5).

import { getAll, getMeta, setMeta } from './db.js';
import { dayNumber } from './content.js';

export const NEW_SPECIES_PER_DAY = 2;  // new species introduced per day
export const SESSION_MAX = 20;         // cards per session (about 5 minutes)
export const MASTERED_DAYS = 21;       // both cards spaced 3+ weeks apart = mastered
export const FAMILIAR_DAYS = 7;

const MIN = 60 * 1000;
const DAY = 24 * 60 * MIN;

export function newCard(speciesId, kind, now = Date.now()) {
  return { id: `${speciesId}:${kind}`, speciesId, kind, state: 'learning', step: 0,
           due: now, interval: 0, ease: 2.5, reps: 0, lapses: 0, created: now };
}

// Cards due on a given day become due at 3 am local time, so they are ready all day.
function dueOnDay(now, days) {
  const d = new Date(now);
  d.setHours(3, 0, 0, 0);
  d.setDate(d.getDate() + days);
  return d.getTime();
}

function setReview(c, days, now, fuzz) {
  let d = Math.min(365, days);
  if (fuzz && d >= 3) d *= 1 + (Math.random() * 0.1 - 0.05); // spread cards out a little
  c.state = 'review';
  c.step = 0;
  c.interval = Math.max(1, Math.round(d));
  c.due = dueOnDay(now, c.interval);
}

export function schedule(card, rating, now = Date.now(), fuzz = true) {
  const c = { ...card, reps: card.reps + 1, lastReview: now };
  if (c.state === 'learning') {
    if (rating === 'again') { c.step = 0; c.due = now + 1 * MIN; }
    else if (rating === 'hard') { c.due = now + (c.step === 0 ? 5 : 10) * MIN; }
    else if (rating === 'good') {
      if (c.step === 0) { c.step = 1; c.due = now + 10 * MIN; }
      else setReview(c, Math.max(1, c.interval), now, fuzz);
    } else setReview(c, Math.max(4, Math.round(c.interval * 1.5)), now, fuzz);  // easy
    return c;
  }
  const ivl = c.interval;
  const late = Math.max(0, (now - card.due) / DAY);
  if (rating === 'again') {
    c.lapses += 1;
    c.ease = Math.max(1.3, c.ease - 0.2);
    c.interval = Math.max(1, Math.round(ivl * 0.5)); // used when it graduates again
    c.state = 'learning'; c.step = 0; c.due = now + 1 * MIN;
  } else {
    // keep Hard < Good < Easy, each at least one day longer than the last
    const hard = Math.max(ivl + 1, Math.round(ivl * 1.2));
    const good = Math.max(hard + 1, Math.round((ivl + late / 2) * c.ease));
    const easy = Math.max(good + 1, Math.round((ivl + late) * (c.ease + 0.15) * 1.3));
    if (rating === 'hard') c.ease = Math.max(1.3, c.ease - 0.15);
    if (rating === 'easy') c.ease += 0.15;
    setReview(c, { hard, good, easy }[rating], now, fuzz);
  }
  return c;
}

export function intervalLabel(card, rating, now = Date.now()) {
  const next = schedule(card, rating, now, false);
  const mins = Math.round((next.due - now) / MIN);
  if (next.state === 'learning') return `${Math.max(1, mins)} min`;
  const days = next.interval;
  if (days < 30) return `${days} ${days === 1 ? 'day' : 'days'}`;
  if (days < 365) return `${(days / 30).toFixed(days < 60 ? 1 : 0)} mo`;
  return '1 yr';
}

// ---------- mastery ----------
export const LEVELS = {
  new: 'Not started', learning: 'Learning', familiar: 'Familiar', mastered: 'Mastered',
};

export function masteryLevel(cards) {
  if (!cards || !cards.length) return 'new';
  const minIvl = Math.min(...cards.map((c) => (c.state === 'review' ? c.interval : 0)));
  const both = cards.length >= 2;
  if (both && minIvl >= MASTERED_DAYS) return 'mastered';
  if (both && minIvl >= FAMILIAR_DAYS) return 'familiar';
  return 'learning';
}

export function cardsBySpecies(cards) {
  const m = new Map();
  for (const c of cards) {
    if (!m.has(c.speciesId)) m.set(c.speciesId, []);
    m.get(c.speciesId).push(c);
  }
  return m;
}

// ---------- what to study today ----------
// New species come in a fixed teaching order: natives and non-natives
// alternate, most abundant on campus first.
export function introductionOrder(content) {
  const n = (s) => (content.locations[s.id] || {}).count || 0;
  const natives = content.species.filter((s) => s.native.value).sort((a, b) => n(b) - n(a));
  const others = content.species.filter((s) => !s.native.value).sort((a, b) => n(b) - n(a));
  const out = [];
  for (let i = 0; i < Math.max(natives.length, others.length); i++) {
    if (natives[i]) out.push(natives[i]);
    if (others[i]) out.push(others[i]);
  }
  return out;
}

export async function newSlotsToday() {
  const rec = await getMeta('introduced', null);
  const used = rec && rec.day === dayNumber() ? rec.count : 0;
  return Math.max(0, NEW_SPECIES_PER_DAY - used);
}

export async function countIntroduced() {
  const today = dayNumber();
  const rec = await getMeta('introduced', null);
  const count = rec && rec.day === today ? rec.count + 1 : 1;
  await setMeta('introduced', { day: today, count });
}

export async function studyPlan(content, now = Date.now()) {
  const cards = await getAll('cards');
  const started = new Set(cards.map((c) => c.speciesId));
  const due = cards.filter((c) => c.due <= now).sort((a, b) => a.due - b.due);
  const slots = await newSlotsToday();
  const fresh = introductionOrder(content).filter((s) => !started.has(s.id)).slice(0, slots);
  const nextDue = cards.filter((c) => c.due > now).reduce((m, c) => Math.min(m, c.due), Infinity);
  return { cards, due, fresh, nextDue, total: Math.min(SESSION_MAX, due.length + fresh.length) };
}
