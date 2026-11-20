// App start-up and navigation between the four tabs.
import { loadContent } from './content.js';
import { openDB } from './db.js';
import { todayView } from './today.js';
import { speciesView } from './species.js';
import { progressView } from './progress.js';
import { esc, toast } from './ui.js';

import { APP_VERSION } from './ui.js';
export { APP_VERSION };

const placeholder = (title, text) => async (root) => {
  root.innerHTML = `<header class="page-head"><h1>${esc(title)}</h1></header>
    <div class="placeholder"><p>${esc(text)}</p><a class="cta secondary" href="#/today">Back to Today</a></div>`;
};

const ROUTES = {
  today: { tab: 'today', view: todayView },
  review: { tab: 'review', view: placeholder('Review', 'The photo quiz with spaced repetition arrives in Step 3. For now, open a species from Today or Progress and read its ID features.') },
  add: { tab: 'add', view: placeholder('Add observation', 'Camera photo, species, GPS and a short note arrive in Step 4.') },
  progress: { tab: 'progress', view: progressView },
  species: { tab: 'progress', view: speciesView },
};

const main = document.getElementById('view');
let content;

function parseHash() {
  const parts = location.hash.replace(/^#\/?/, '').split('/').filter(Boolean).map(decodeURIComponent);
  const name = ROUTES[parts[0]] ? parts[0] : 'today';
  return { name, params: parts.slice(1) };
}

async function render() {
  const { name, params } = parseHash();
  const route = ROUTES[name];
  for (const a of document.querySelectorAll('.tabbar a')) {
    a.toggleAttribute('aria-current', a.dataset.tab === route.tab);
    if (a.dataset.tab === route.tab) a.setAttribute('aria-current', 'page');
  }
  const viewEl = document.createElement('div');
  viewEl.className = `screen screen-${name}`;
  try {
    await route.view(viewEl, content, ...params);
  } catch (err) {
    console.error(err);
    viewEl.innerHTML = `<p class="empty">Something went wrong showing this screen: ${esc(err.message)}. Pull down to reload, or go back to <a href="#/today">Today</a>.</p>`;
  }
  main.replaceChildren(viewEl);
  if (!params[1]) window.scrollTo(0, 0);
}

async function start() {
  try {
    await openDB();
    content = await loadContent();
  } catch (err) {
    main.innerHTML = `<p class="empty">The app couldn’t load its data: ${esc(err.message)}. Check your connection and reopen the app.</p>`;
    return;
  }
  window.addEventListener('hashchange', render);
  await render();
  setupOffline();
}

function setupOffline() {
  // Ask iOS to keep this app's data even when the phone is short of space.
  navigator.storage?.persist?.().catch(() => {});
  if (!('serviceWorker' in navigator)) return;
  const hadController = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.register('./sw.js').catch((e) => console.warn('Offline support unavailable', e));
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (hadController) toast('A new version is ready.', { label: 'Reload', run: () => location.reload() });
  });
  navigator.serviceWorker.ready.then((reg) => {
    if (!navigator.onLine || !reg.active) return;
    const urls = Object.values(content.photos).flat().map((p) => p.file);
    reg.active.postMessage({ type: 'cache-photos', urls });
  });
}

start();
