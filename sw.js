// Service worker: makes the app open and work offline on campus.
// Bump VERSION whenever app files change so phones pick up the update.
const VERSION = '0.2.0';
const SHELL = `ufe-shell-${VERSION}`;
const PHOTOS = 'ufe-photos-v1';
const SHELL_FILES = [
  './', 'index.html', 'manifest.webmanifest', 'css/app.css',
  'js/app.js', 'js/db.js', 'js/content.js', 'js/ui.js', 'js/today.js', 'js/species.js', 'js/progress.js',
  'data/species.json', 'data/photos.json', 'data/locations.json',
  'icons/icon-180.png', 'icons/icon-192.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL);
    await cache.addAll(SHELL_FILES.map((u) => new Request(u, { cache: 'reload' })));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) {
      if (key.startsWith('ufe-shell-') && key !== SHELL) await caches.delete(key);
    }
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;

  if (req.mode === 'navigate') {
    event.respondWith(caches.match('index.html', { ignoreSearch: true }).then((r) => r || fetch(req)));
    return;
  }
  if (url.pathname.includes('/photos/')) {
    event.respondWith(cacheFirst(req, PHOTOS));
    return;
  }
  if (url.pathname.includes('/data/')) {
    event.respondWith(staleWhileRevalidate(req, SHELL));
    return;
  }
  event.respondWith(cacheFirst(req, SHELL));
});

async function cacheFirst(req, name) {
  const cache = await caches.open(name);
  const hit = await cache.match(req, { ignoreSearch: true });
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok) cache.put(req, res.clone());
  return res;
}

async function staleWhileRevalidate(req, name) {
  const cache = await caches.open(name);
  const hit = await cache.match(req, { ignoreSearch: true });
  const fresh = fetch(req).then((res) => { if (res.ok) cache.put(req, res.clone()); return res; }).catch(() => null);
  return hit || (await fresh) || new Response('offline', { status: 503 });
}

// The page sends the list of seed photos once it has loaded, so they are all
// available offline even before you have looked at them.
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'cache-photos') {
    event.waitUntil(cachePhotos(event.data.urls || []));
  }
});

async function cachePhotos(urls) {
  const cache = await caches.open(PHOTOS);
  for (const u of urls) {
    const full = new URL(u, self.registration.scope).href;
    if (await cache.match(full)) continue;
    try {
      const res = await fetch(full);
      if (res.ok) await cache.put(full, res);
    } catch (e) { /* offline: try again next launch */ }
  }
}
