// IndexedDB on the phone. All stores for Phase 1 are created up front,
// so later steps (quiz, observations, backup) need no database upgrade.
const DB_NAME = 'ufe';
const DB_VERSION = 1;

let dbPromise;

export function openDB() {
  if (!dbPromise) {
    dbPromise = new Promise((resolve, reject) => {
      if (!('indexedDB' in self)) return reject(new Error('This browser has no IndexedDB.'));
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        const make = (name, opts, indexes = []) => {
          if (db.objectStoreNames.contains(name)) return;
          const store = db.createObjectStore(name, opts);
          for (const ix of indexes) store.createIndex(ix, ix);
        };
        make('cards', { keyPath: 'id' }, ['speciesId', 'due']);          // quiz scheduling (Step 3)
        make('reviews', { keyPath: 'id', autoIncrement: true }, ['at']);  // review log, streak (Step 3)
        make('observations', { keyPath: 'id' }, ['speciesId']);           // your field notes (Step 4)
        make('photos', { keyPath: 'id' });                                // your photo files (Step 4)
        make('verify', { keyPath: 'key' });                               // content you marked verified
        make('meta', { keyPath: 'key' });                                 // settings and bookkeeping
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }
  return dbPromise;
}

async function run(storeName, mode, fn) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const t = db.transaction(storeName, mode);
    const req = fn(t.objectStore(storeName));
    t.oncomplete = () => resolve(req ? req.result : undefined);
    t.onerror = () => reject(t.error);
    t.onabort = () => reject(t.error);
  });
}

export const get = (store, key) => run(store, 'readonly', (s) => s.get(key));
export const getAll = (store) => run(store, 'readonly', (s) => s.getAll());
export const count = (store) => run(store, 'readonly', (s) => s.count());
export const put = (store, value) => run(store, 'readwrite', (s) => s.put(value));
export const del = (store, key) => run(store, 'readwrite', (s) => s.delete(key));

export async function getMeta(key, fallback = null) {
  const rec = await get('meta', key);
  return rec ? rec.value : fallback;
}
export const setMeta = (key, value) => put('meta', { key, value });
