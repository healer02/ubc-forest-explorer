"""Build data/trees.json and data/locations.json from the UBC inventory.

Run from the project folder:
  python3 tools/build_trees.py "../ubc github"
Keeps only the 26 starter species, drops removed/dead trees and every
editor/metadata field (they contain personal email addresses).
"""
import json, sys, re, math, collections, os

SRC = sys.argv[1] if len(sys.argv) > 1 else "../ubc github"
OUT = os.path.join(os.path.dirname(__file__), "..", "data")

SPECIES = {  # inventory taxon -> app species id
    "Thuja plicata": "thuja-plicata", "Pseudotsuga menziesii": "pseudotsuga-menziesii",
    "Tsuga heterophylla": "tsuga-heterophylla", "Abies grandis": "abies-grandis",
    "Callitropsis nootkatensis": "callitropsis-nootkatensis", "Acer circinatum": "acer-circinatum",
    "Acer macrophyllum": "acer-macrophyllum", "Cornus nuttallii": "cornus-nuttallii",
    "Alnus rubra": "alnus-rubra", "Arbutus menziesii": "arbutus-menziesii",
    "Quercus garryana": "quercus-garryana", "Pinus nigra": "pinus-nigra",
    "Cedrus deodara": "cedrus-deodara", "Sequoiadendron giganteum": "sequoiadendron-giganteum",
    "Metasequoia glyptostroboides": "metasequoia-glyptostroboides", "Ginkgo biloba": "ginkgo-biloba",
    "Acer platanoides": "acer-platanoides", "Acer palmatum": "acer-palmatum",
    "Acer x freemanii": "acer-x-freemanii", "Prunus serrulata": "prunus-serrulata",
    "Quercus rubra": "quercus-rubra", "Cercidiphyllum japonicum": "cercidiphyllum-japonicum",
    "Cornus kousa": "cornus-kousa", "Liquidambar styraciflua": "liquidambar-styraciflua",
    "Platanus x hispanica": "platanus-x-hispanica", "Ilex aquifolium": "ilex-aquifolium",
}
ALIAS = {"Acer macrophylla": "Acer macrophyllum", "Chamaecyparis nootkatensis": "Callitropsis nootkatensis",
         "Xanthocyparis nootkatensis": "Callitropsis nootkatensis", "Platanus x acerifolia": "Platanus x hispanica"}
# trees with no TAXA but a usable common name
COMMON_ONLY = {"douglas fir": "Pseudotsuga menziesii", "douglas-fir": "Pseudotsuga menziesii",
               "western red cedar": "Thuja plicata", "coastal hemlock": "Tsuga heterophylla",
               "western hemlock": "Tsuga heterophylla", "kousa dogwood": "Cornus kousa",
               "vine maple": "Acer circinatum", "norway maple": "Acer platanoides"}
GONE_NAMES = {"removed", "dead", "dead standing tree", "standing dead tree"}

def norm_taxon(t):
    t = re.sub(r"\s+", " ", t.replace("\xa0", " ").strip())
    parts = re.split(r"[\'\"‘’“”]", t, maxsplit=1)
    base = parts[0].strip()
    cultivar = re.sub(r"[\'\"‘’“”]", "", parts[1]).strip() if len(parts) > 1 else ""
    w = base.split(" ")
    if len(w) >= 3 and w[1].lower() in ("x", "×"):
        name = f"{w[0].capitalize()} x {w[2].lower()}"
    elif len(w) >= 2:
        name = f"{w[0].capitalize()} {w[1].lower()}"
    else:
        return None, ""
    return ALIAS.get(name, name), cultivar.title()

# --- simple planar geometry in metres around campus ---
LAT0 = 49.262
KX, KY = 111320 * math.cos(math.radians(LAT0)), 110540
def xy(lon, lat): return (lon * KX, lat * KY)

def rings(geom):
    if geom["type"] == "Polygon": return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon": return geom["coordinates"]
    return []

def inside(pt, poly):  # poly = list of rings in xy
    x, y = pt; c = False
    for ring in poly:
        for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c

def seg_dist(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)

def load_shapes(fname, namefn):
    out = []
    for f in json.load(open(os.path.join(SRC, fname)))["features"]:
        g = f["geometry"]; name = namefn(f["properties"])
        if not g or not name: continue
        if g["type"] in ("Polygon", "MultiPolygon"):
            polys = [[[xy(*c[:2]) for c in ring] for ring in poly] for poly in rings(g)]
            segs = [(a, b) for poly in polys for ring in poly for a, b in zip(ring, ring[1:])]
        elif g["type"] in ("LineString", "MultiLineString"):
            lines = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
            polys = []
            segs = [(xy(*a[:2]), xy(*b[:2])) for line in lines for a, b in zip(line, line[1:])]
        else: continue
        xs = [p[0] for s in segs for p in s]; ys = [p[1] for s in segs for p in s]
        out.append(dict(name=name.strip(), polys=polys, segs=segs, bbox=(min(xs), min(ys), max(xs), max(ys))))
    return out

def nearest(pt, shapes, maxd):
    best, bd = None, maxd
    for s in shapes:
        x0, y0, x1, y1 = s["bbox"]
        if pt[0] < x0 - bd or pt[0] > x1 + bd or pt[1] < y0 - bd or pt[1] > y1 + bd: continue
        if s["polys"] and any(inside(pt, poly) for poly in s["polys"]): return s, 0
        d = min(seg_dist(pt, a, b) for a, b in s["segs"])
        if d < bd: best, bd = s, d
    return best, bd

ROAD_FIX = {"Blvd": "Boulevard", "Rd": "Road", "Ave": "Avenue", "Cres": "Crescent", "Pl": "Place", "Dr": "Drive"}
def road_name(p):
    n = p.get("ROADNAME") or p.get("NAME")
    if not n: return None
    return " ".join(ROAD_FIX.get(w, w) for w in n.replace("W ", "West ").split())

features = load_shapes("ubcv_landscape_features.geojson", lambda p: p.get("NAME"))
def bldg_name(p):
    short, full = p.get("SHORTNAME"), p.get("NAME")
    if not short or re.match(r"^(Building \d|[A-Z]$|Tower \d)", short): return full or short
    return short
buildings = load_shapes("ubcv_buildings.geojson", bldg_name)
roads = load_shapes("ubcv_roads_simple.geojson", road_name)

def place_label(lon, lat):
    pt = xy(lon, lat)
    for f in features:
        if any(inside(pt, poly) for poly in f["polys"]): return f["name"]
    r, _ = nearest(pt, roads, 20)
    b, _ = nearest(pt, buildings, 80)
    parts = ([r["name"]] if r else []) + ([f"near {b['name']}"] if b else [])
    return " · ".join(parts) if parts else "open area"

# --- build ---
trees, skipped = [], collections.Counter()
for f in json.load(open(os.path.join(SRC, "ubcv_campus_trees.geojson")))["features"]:
    p = f["properties"]
    cn = (p.get("COMMON_NAME") or "").strip().lower()
    status = (p.get("TREE_STATUS") or "").lower()
    if p.get("LIVE_TREE") == "Dead" or cn in GONE_NAMES or status.startswith(("removed", "dead", "missing")):
        skipped["removed/dead"] += 1; continue
    taxon, cultivar = norm_taxon(p["TAXA"]) if p.get("TAXA") else (COMMON_ONLY.get(cn), "")
    if taxon not in SPECIES: skipped["other species / unnamed"] += 1; continue
    lon, lat = f["geometry"]["coordinates"][:2]
    dbh = p.get("DBH"); h = p.get("THEIGHT")
    dbh = dbh if isinstance(dbh, (int, float)) and 1 <= dbh <= 300 else None
    h = round(h, 1) if isinstance(h, (int, float)) and 0.5 <= h <= 90 else None
    trees.append(dict(oid=p["OBJECTID"], sp=SPECIES[taxon], lat=round(lat, 6), lon=round(lon, 6),
                      cv=cultivar, dbh=dbh, h=h, near=place_label(lon, lat)))

cols = ["oid", "sp", "lat", "lon", "cv", "dbh", "h", "near"]
json.dump({"source": "UBC Campus + Community Planning tree inventory (ubcv_campus_trees.geojson)",
           "note": "Cleaned subset for the 26 starter species. Removed/dead trees and editor fields dropped. dbh in cm, h in m; implausible values blanked.",
           "columns": cols, "rows": [[t[c] for c in cols] for t in trees]},
          open(os.path.join(OUT, "trees.json"), "w"), separators=(",", ":"), ensure_ascii=False)

loc = {}
for sp in SPECIES.values():
    ts = [t for t in trees if t["sp"] == sp]
    groups = collections.defaultdict(list)
    for t in ts: groups[t["near"]].append(t)
    top = sorted(groups.items(), key=lambda kv: -len(kv[1]))[:5]
    big = max((t for t in ts if t["dbh"]), key=lambda t: t["dbh"], default=None)
    loc[sp] = {"count": len(ts),
               "spots": [{"label": k, "count": len(v), "lat": round(sum(t["lat"] for t in v) / len(v), 6),
                          "lon": round(sum(t["lon"] for t in v) / len(v), 6)} for k, v in top],
               "largest_needs_check": ({"oid": big["oid"], "dbh_cm": big["dbh"], "height_m": big["h"], "label": big["near"],
                            "lat": big["lat"], "lon": big["lon"]} if big else None)}
json.dump(loc, open(os.path.join(OUT, "locations.json"), "w"), indent=1, ensure_ascii=False)
print(len(trees), "trees written;", dict(skipped))
for sp, v in loc.items():
    print(f"{v['count']:5d} {sp:30s} {[ (s['label'], s['count']) for s in v['spots'][:3]]}  largest={v['largest_needs_check'] and (v['largest_needs_check']['dbh_cm'], v['largest_needs_check']['label'])}")
