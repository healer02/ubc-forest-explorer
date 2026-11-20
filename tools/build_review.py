"""Build tools/content-review.html: a read-only page for checking the drafted species content,
campus locations and seed photos before they go into the app.
Run from the project folder:  python3 tools/build_review.py
"""
import json, os, html

ROOT = os.path.join(os.path.dirname(__file__), "..")
sp = json.load(open(os.path.join(ROOT, "data", "species.json")))
loc = json.load(open(os.path.join(ROOT, "data", "locations.json")))
ph = json.load(open(os.path.join(ROOT, "data", "photos.json")))["photos"]
e = html.escape

def badge(f):
    s = f["status"]
    return {"needs_check": '<span class="b nc">needs check</span>',
            "verified": '<span class="b ok">verified</span>',
            "blank": '<span class="b bl">left blank</span>'}[s]

def para(label, f):
    body = e(f["text"]) if f["text"] else '<em class="muted">No confident fact, so left empty.</em>'
    return f'<div class="row"><div class="lab">{label} {badge(f)}</div><div>{body}</div></div>'

cards, toc = [], []
for i, s in enumerate(sp["species"], 1):
    L = loc[s["id"]]
    native = "Native" if s["native"]["value"] else "Non-native"
    toc.append(f'<a href="#{s["id"]}">{i}. {e(s["common"])}</a>')
    feats = "".join(f'<li><b>{e(f["type"])}</b>: {e(f["text"])} {badge(f)}</li>' for f in s["id_features"])
    looks = "".join(f'<li><b>{e(l["name"])}</b>: {e(l["text"])} {badge(l)}</li>' for l in s["lookalikes"]) \
        or '<li><em class="muted">None listed.</em></li>'
    spots = "".join(f'<li>{e(x["label"])}: {x["count"]}</li>' for x in L["spots"])
    big = L.get("largest_needs_check")
    bigtxt = (f'Largest recorded DBH: {big["dbh_cm"]} cm{(", " + str(big["height_m"]) + " m tall") if big["height_m"] else ""}, {e(big["label"])} '
              f'<span class="b nc">needs check</span>') if big else ""
    photos = "".join(
        f'<figure><img loading="lazy" src="../{e(p["file"])}" alt="{e(s["common"])} {e(p["role"])}">'
        f'<figcaption><b>{e(p["role"])}</b> · <a href="{e(p["link"])}">{e(p["source"])}</a><br>{e(p["credit"])}</figcaption></figure>'
        for p in ph.get(s["id"], []))
    cards.append(f'''
<section id="{s["id"]}">
  <h2>{i}. {e(s["common"])} <i>{e(s["botanical"])}</i></h2>
  <p class="meta">{e(s["group"])} · {native}: {e(s["native"]["text"])} {badge(s["native"])} · <b>{L["count"]}</b> trees in the inventory</p>
  <div class="photos">{photos}</div>
  <h3>Key ID features</h3><ul>{feats}</ul>
  <h3>Look-alikes</h3><ul>{looks}</ul>
  {para("Design use / misuse", s["design"])}
  {para("Ecology", s["ecology"])}
  {para("Controversy", s["controversy"])}
  {para("Tour talking point", s["tour_point"])}
  <h3>Where on campus (from the inventory)</h3><ul>{spots}</ul><p class="small">{bigtxt}</p>
</section>''')

nc = sum(1 for s in sp["species"] for k in ("design", "ecology", "controversy", "tour_point") if s[k]["status"] == "needs_check") \
   + sum(len(s["id_features"]) + len(s["lookalikes"]) + 1 for s in sp["species"])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Species Content Review</title>
<style>
:root{{--bg:#f6f5f1;--card:#fff;--ink:#1f2a24;--muted:#66706a;--line:#dcdcd4;--accent:#2f6b4f;--warn:#9a5b00;--warnbg:#fff1d6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151a17;--card:#1d2420;--ink:#e8ece9;--muted:#9aa49e;--line:#2e3832;--accent:#7cc4a0;--warn:#f0b45a;--warnbg:#3a2c12}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,system-ui,sans-serif}}
main{{max-width:900px;margin:auto;padding:16px}}
header p{{color:var(--muted)}} nav{{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px;margin:12px 0 24px}}
a{{color:var(--accent)}} section{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:0 0 20px}}
h2{{margin:0 0 4px;font-size:22px}} h2 i{{font-weight:400;color:var(--muted)}} h3{{font-size:15px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin:16px 0 4px}}
.meta{{margin:0 0 10px;color:var(--muted)}} ul{{margin:0;padding-left:20px}} li{{margin:4px 0}}
.row{{margin:12px 0}} .lab{{font-weight:600}} .muted{{color:var(--muted)}} .small{{font-size:14px;color:var(--muted)}}
.b{{display:inline-block;font-size:11px;font-weight:600;padding:1px 7px;border-radius:99px;vertical-align:middle;white-space:nowrap}}
.nc{{background:var(--warnbg);color:var(--warn)}} .ok{{background:#d9f0e3;color:#1d5c3d}} .bl{{background:var(--line);color:var(--muted)}}
.photos{{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px}} figure{{margin:0;flex:0 0 170px}}
figure img{{width:170px;height:170px;object-fit:cover;border-radius:10px;display:block}} figcaption{{font-size:11px;color:var(--muted);line-height:1.3;margin-top:4px}}
</style></head><body><main>
<header><h1>UBC Urban Forest Explorer: species content review</h1>
<p>Draft content for the 26 approved species. Every drafted item is flagged <span class="b nc">needs check</span>
until you verify it in the app. Fields marked <span class="b bl">left blank</span> are empty on purpose. Native = native to coastal BC (default).
Locations and counts come from the UBC inventory (removed and dead trees excluded). {sum(len(v) for v in ph.values())} seed photos, all CC0, CC BY or public domain.</p></header>
<nav>{"".join(toc)}</nav>
{"".join(cards)}
</main></body></html>'''
open(os.path.join(ROOT, "tools", "content-review.html"), "w").write(page)
print("wrote tools/content-review.html;", nc, "items flagged needs_check")
