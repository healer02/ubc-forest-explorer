// Review session: photo cards (name the tree) and reverse cards (recall its
// 3 ID features), rated Again / Hard / Good / Easy.
import { get, put } from './db.js';
import { featureLabel, GROUP_LABEL } from './content.js';
import { studyPlan, newCard, schedule, intervalLabel, countIntroduced, SESSION_MAX } from './scheduler.js';
import { esc } from './ui.js';

const QUIZ_ROLES = ['leaf', 'bark', 'form'];
const ROLE_LABEL = { leaf: 'Leaf', bark: 'Bark', form: 'Form', flower: 'Flower', fruit: 'Fruit', seasonal: 'Seasonal' };
const RATINGS = [
  ['again', 'Again'], ['hard', 'Hard'], ['good', 'Good'], ['easy', 'Easy'],
];

// ---------- answer checking ----------
const norm = (s) => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/×/g, 'x').replace(/[^a-z]/g, '');

function acceptedNames(s) {
  const names = [s.common, s.botanical];
  const m = s.common.match(/^(.*?)\s*\((.*?)\)\s*(.*)$/); // "Austrian (black) pine", "arbutus (Pacific madrone)"
  if (m) {
    names.push(`${m[1]} ${m[3]}`, `${m[2]} ${m[3]}`);
    if (!m[3]) names.push(m[2]);
  }
  return names.map(norm).filter(Boolean);
}

function distance(a, b) {
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
  for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    }
  }
  return d[a.length][b.length];
}

// Returns the species the typed text best matches (allowing small typos), or null.
function matchTyped(text, content) {
  const t = norm(text);
  if (t.length < 3) return null;
  let best = null, bestD = Infinity;
  for (const s of content.species) {
    for (const name of acceptedNames(s)) {
      const dd = distance(t, name);
      const allowed = name.length <= 6 ? 1 : name.length <= 12 ? 2 : 3;
      if (dd <= allowed && dd < bestD) { best = s; bestD = dd; }
    }
  }
  return best;
}

// ---------- multiple choice ----------
function lookalikeIds(s, content) {
  const ids = [];
  for (const l of s.lookalikes) {
    const ln = norm(l.name);
    const hit = content.species.find((o) => o.id !== s.id && acceptedNames(o).some((n) => ln.includes(n) || n.includes(ln)));
    if (hit && !ids.includes(hit.id)) ids.push(hit.id);
  }
  return ids;
}

const shuffle = (arr) => {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
};

function choicesFor(s, content) {
  const picks = new Set();
  for (const id of shuffle(lookalikeIds(s, content))) if (picks.size < 2) picks.add(id);
  for (const o of shuffle(content.species.filter((o) => o.group === s.group && o.id !== s.id))) if (picks.size < 3) picks.add(o.id);
  for (const o of shuffle(content.species.filter((o) => o.id !== s.id))) if (picks.size < 3) picks.add(o.id);
  return shuffle([s.id, ...picks]).map((id) => content.byId.get(id));
}

function pickPhoto(content, card) {
  const all = content.photos[card.speciesId] || [];
  const quiz = all.filter((p) => QUIZ_ROLES.includes(p.role));
  const pool = quiz.length ? quiz : all;
  // rotate leaf -> bark -> form across reviews, then pick a random photo of that role
  const roles = QUIZ_ROLES.filter((r) => pool.some((p) => p.role === r));
  const role = roles.length ? roles[card.reps % roles.length] : null;
  const options = pool.filter((p) => !role || p.role === role).filter((p) => p.file !== card.lastPhoto);
  const list = options.length ? options : pool;
  return list[Math.floor(Math.random() * list.length)];
}

// ---------- the session ----------
export async function reviewView(root, content) {
  const plan = await studyPlan(content);
  const queue = plan.due.map((card) => ({ card, isNew: false }));
  for (const s of plan.fresh) queue.push({ card: newCard(s.id, 'photo'), isNew: true });
  queue.splice(SESSION_MAX);
  const tally = { done: 0, photoAsked: 0, photoRight: 0, newNames: [] };

  if (!queue.length) return caughtUp(root, plan.nextDue);

  const next = () => {
    if (!queue.length) return finished(root, content, tally);
    const item = queue.shift();
    const s = content.byId.get(item.card.speciesId);
    if (!s) return next();
    const pos = `${tally.done + 1} of ${tally.done + queue.length + 1}`;
    if (item.card.kind === 'reverse') showReverse(root, content, s, item, onRated, pos);
    else showPhoto(root, content, s, item, onRated, pos);
    window.scrollTo(0, 0);
  };

  const onRated = async (item, rating, extra) => {
    const now = Date.now();
    const before = item.card;
    const after = schedule(before, rating, now);
    if (extra.photo) after.lastPhoto = extra.photo;
    await put('cards', after);
    await put('reviews', {
      cardId: after.id, speciesId: after.speciesId, kind: after.kind, rating,
      correct: extra.correct ?? null, answer: extra.answer ?? null, mode: extra.mode ?? null,
      photo: extra.photo ?? null, intervalBefore: before.interval, intervalAfter: after.interval,
      at: new Date(now).toISOString(),
    });
    if (item.isNew) {
      await countIntroduced();
      tally.newNames.push(content.byId.get(after.speciesId).common);
    }
    // Add the reverse card the day after the photo card is first passed.
    if (after.kind === 'photo' && after.state === 'review' && !(await get('cards', `${after.speciesId}:reverse`))) {
      const rev = newCard(after.speciesId, 'reverse', now);
      const d = new Date(now); d.setHours(3, 0, 0, 0); d.setDate(d.getDate() + 1);
      rev.due = d.getTime();
      await put('cards', rev);
    }
    tally.done++;
    if (after.kind === 'photo' && typeof extra.correct === 'boolean') {
      tally.photoAsked++;
      if (extra.correct) tally.photoRight++;
    }
    // Cards still in learning come back later in this session.
    if (after.state === 'learning' && after.due - now < 20 * 60 * 1000) {
      queue.push({ card: after, isNew: false });
    }
    next();
  };

  next();
}

function header(item, label, pos) {
  return `<div class="quiz-top">
    <span class="eyebrow">${esc(label)}${item.isNew ? ' · <span class="new-badge">New species</span>' : ''}</span>
    <span class="quiz-pos">${esc(pos)}</span>
    <a class="quiz-end" href="#/today" aria-label="End session">End</a>
  </div>`;
}

function ratingBar(card) {
  return `<div class="rate-bar" role="group" aria-label="How well did you know it?">
    ${RATINGS.map(([r, label]) => `<button type="button" class="rate rate-${r}" data-rate="${r}">
      <b>${label}</b><small>${esc(intervalLabel(card, r))}</small></button>`).join('')}
  </div>`;
}

function featuresList(s) {
  return `<ul class="feat-list">${s.id_features.map((f) => `
    <li><b>${esc(featureLabel(f.type, s.group))}</b> ${esc(f.text)}</li>`).join('')}</ul>`;
}

function bindRating(root, item, onRated, extra, suggested) {
  const bar = root.querySelector('.rate-bar');
  if (suggested) bar.querySelector(`[data-rate="${suggested}"]`)?.classList.add('suggested');
  bar.addEventListener('click', (e) => {
    const b = e.target.closest('[data-rate]');
    if (!b) return;
    bar.querySelectorAll('button').forEach((x) => { x.disabled = true; });
    onRated(item, b.dataset.rate, extra);
  });
}

// ----- photo card -----
function showPhoto(root, content, s, item, onRated, pos) {
  const photo = pickPhoto(content, item.card);
  const choices = choicesFor(s, content);
  root.innerHTML = `
    ${header(item, 'Name this tree', pos)}
    <figure class="quiz-photo">
      ${photo ? `<img src="${esc(photo.file)}" alt="Quiz photo: ${esc(ROLE_LABEL[photo.role] || photo.role)}">
      <span class="role">${esc(ROLE_LABEL[photo.role] || photo.role)}</span>` : '<div class="nophoto">No photo yet</div>'}
    </figure>
    <div class="answer-area">
      <div class="choices">
        ${choices.map((c) => `<button type="button" class="choice" data-id="${esc(c.id)}">${esc(c.common)}</button>`).join('')}
      </div>
      <button type="button" class="linkish" data-act="type">Type the name instead</button>
    </div>
  `;
  const area = root.querySelector('.answer-area');
  const reveal = (picked, mode, typedText) => {
    const correct = picked && picked.id === s.id;
    const tell = picked && !correct
      ? s.lookalikes.find((l) => acceptedNames(picked).some((n) => norm(l.name).includes(n) || n.includes(norm(l.name))))
      : null;
    const yours = mode === 'type' ? (typedText || '') : (picked ? picked.common : '');
    area.innerHTML = `
      <div class="result ${correct ? 'right' : 'wrong'}">
        <p class="verdict">${correct ? '✓ Correct' : `✗ Not quite${yours ? `: you said “${esc(yours)}”` : ''}`}</p>
        <h2>${esc(s.common)}</h2>
        <p class="latin">${esc(s.botanical)}</p>
      </div>
      ${tell ? `<div class="tell"><h3>Telling it from ${esc(picked.common)}</h3><p>${esc(tell.text)}</p></div>` : ''}
      <div class="reveal"><h3>Key ID features</h3>${featuresList(s)}</div>
      ${photo ? `<p class="credit">Photo: ${esc(photo.credit === 'no rights reserved' ? 'CC0' : photo.credit)} · ${esc(photo.source)}</p>` : ''}
      ${ratingBar(item.card)}
    `;
    bindRating(root, item, onRated,
      { correct, answer: yours || null, mode, photo: photo && photo.file },
      correct ? 'good' : 'again');
    area.querySelector('.result').scrollIntoView({ block: 'start', behavior: 'smooth' });
  };

  area.addEventListener('click', (e) => {
    const choice = e.target.closest('.choice');
    if (choice) {
      area.querySelectorAll('.choice').forEach((b) => { b.disabled = true; });
      reveal(content.byId.get(choice.dataset.id), 'pick');
      return;
    }
    if (e.target.closest('[data-act="type"]')) {
      area.innerHTML = `
        <form class="type-form" autocomplete="off">
          <label for="typed">Common or botanical name</label>
          <input id="typed" name="typed" type="text" autocapitalize="none" autocorrect="off" spellcheck="false" enterkeyhint="done">
          <div class="type-actions">
            <button type="submit" class="cta small">Check</button>
            <button type="button" class="linkish" data-act="dontknow">I don’t know</button>
          </div>
        </form>`;
      const form = area.querySelector('form');
      const input = form.querySelector('input');
      input.focus();
      form.addEventListener('submit', (ev) => {
        ev.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        input.blur();
        reveal(matchTyped(text, content), 'type', text);
      });
      form.querySelector('[data-act="dontknow"]').addEventListener('click', () => reveal(null, 'type', ''));
    }
  });
}

// ----- reverse card -----
function showReverse(root, content, s, item, onRated, pos) {
  root.innerHTML = `
    ${header(item, 'Recall the 3 features', pos)}
    <div class="reverse-card">
      <h2>${esc(s.common)}</h2>
      <p class="latin">${esc(s.botanical)}</p>
      <p class="tags"><span class="tag">${esc(GROUP_LABEL[s.group] || s.group)}</span></p>
      <p class="prompt">Say them out loud or in your head. Think leaf, bark, form, flower or fruit, and a seasonal cue.</p>
    </div>
    <div class="answer-area">
      <button type="button" class="cta" data-act="show">Show the features</button>
    </div>`;
  const area = root.querySelector('.answer-area');
  area.querySelector('[data-act="show"]').addEventListener('click', () => {
    const photo = (content.photos[s.id] || [])[0];
    area.innerHTML = `
      <div class="reveal">${featuresList(s)}</div>
      ${photo ? `<img class="reveal-photo" src="${esc(photo.file)}" alt="${esc(s.common)}">` : ''}
      ${ratingBar(item.card)}`;
    bindRating(root, item, onRated, { mode: 'recall' }, null);
  });
}

// ----- end states -----
function caughtUp(root, nextDue) {
  const when = Number.isFinite(nextDue)
    ? new Date(nextDue).toLocaleString('en-CA', { weekday: 'long', hour: 'numeric', minute: '2-digit' })
    : null;
  root.innerHTML = `
    <header class="page-head"><h1>All caught up</h1></header>
    <div class="placeholder">
      <p>No cards are due and today’s new species are done.${when ? ` Next review: ${esc(when)}.` : ''}</p>
      <a class="cta secondary" href="#/today">Back to Today</a>
    </div>`;
}

function finished(root, content, tally) {
  root.innerHTML = `
    <header class="page-head"><p class="eyebrow">Session complete</p><h1>Done for today</h1></header>
    <div class="placeholder">
      <p><b>${tally.done}</b> ${tally.done === 1 ? 'card' : 'cards'} reviewed.</p>
      ${tally.photoAsked ? `<p>Named <b>${tally.photoRight} of ${tally.photoAsked}</b> photos correctly.</p>` : ''}
      ${tally.newNames.length ? `<p>New today: ${tally.newNames.map(esc).join(', ')}.</p>` : ''}
      <a class="cta" href="#/today">Back to Today</a>
    </div>`;
}
