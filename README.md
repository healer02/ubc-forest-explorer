# UBC Urban Forest Explorer

A personal, phone-first web app for learning UBC Vancouver campus trees through spaced repetition, your own photos and stories, in preparation for a 45-minute campus tree walking tour.

The app is a static site (no server, no accounts). All personal data (quiz progress, observations, photos, verification marks) is stored only on the phone, in the browser's IndexedDB.

## What's here

| Path | What it is |
|---|---|
| `index.html`, `css/`, `js/`, `sw.js`, `manifest.webmanifest`, `icons/` | The app |
| `data/species.json` | Species content for the 26 starter species. AI-drafted items carry `"status": "needs_check"` until verified. |
| `data/trees.json`, `data/locations.json` | Cleaned subset of the UBC campus tree inventory (26 species, removed/dead trees and editor fields dropped) |
| `data/photos.json`, `photos/seed/` | Seed quiz photos (CC0, CC BY or public domain) with credits |
| `tools/` | Scripts that rebuild the data, and `content-review.html` for reading all content at once |

## Updating the tree data

```bash
python3 tools/build_trees.py "../ubc github"
```

After changing any app file, bump `VERSION` in `sw.js` and `APP_VERSION` in `js/ui.js` so phones pick up the update.

## Credits

- Tree locations: UBC campus tree inventory (UBC Campus + Community Planning geospatial data).
- Seed photos: iNaturalist and Wikimedia Commons contributors; each photo's credit and licence are in `data/photos.json` and shown in the app.
