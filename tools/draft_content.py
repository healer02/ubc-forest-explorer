"""ONE-TIME DRAFT SOURCE. Do not re-run once you start verifying: data/species.json is now the source of truth.
Emit data/species.json from the drafted content below.
Every non-blank drafted field gets status "needs_check". Blank = not confident, left empty on purpose.
Feature tuples: (type, text). Look-alike tuples: (name, how to tell apart).
"""
import json, sys

S = []
def sp(id, common, botanical, group, native, origin, feats, looks, design, ecology, controversy, tour):
    S.append(dict(id=id, common=common, botanical=botanical, group=group, native=native, origin=origin,
                  feats=feats, looks=looks, design=design, ecology=ecology, controversy=controversy, tour=tour))

# ---------------- NATIVE ----------------
sp("thuja-plicata", "western redcedar", "Thuja plicata", "conifer", True,
   "Native to coastal BC",
   [("leaf", "Flat, fern-like sprays of tiny overlapping scale leaves; the undersides show whitish bow-tie or butterfly-shaped markings."),
    ("bark", "Reddish-brown to grey bark that is fibrous and strips off in long vertical ribbons."),
    ("form", "Branches droop then curve up at the tips like a J; the leader often droops slightly; the trunk base is flared and buttressed.")],
   [("yellow-cedar", "Yellow-cedar sprays hang limp like a wet dog, feel prickly when stroked backward, and lack the white bow-tie marks underneath."),
    ("eastern white cedar (Thuja occidentalis)", "Usually a hedge or small columnar tree; foliage undersides are yellow-green with little or no white marking.")],
   "A good shade-tolerant screen and character tree in moist sites; a poor choice for hot, paved, drought-prone spots where it struggles.",
   "Its wood contains natural fungicidal compounds (thujaplicins) that make it highly rot-resistant.",
   "Summer droughts and heat (e.g., the 2021 heat dome) have caused visible dieback and dead tops in redcedar across the region. Should we keep planting it in urban sites as the climate warms?",
   "BC's official tree and by far the most common tree on campus (about 1 in 8 identified trees, above the 10% single-species guideline often used for urban forests). A cultural keystone for Coast Salish peoples, including the Musqueam, on whose land UBC stands: bark, wood and roots for canoes, houses, clothing and baskets.")

sp("pseudotsuga-menziesii", "Douglas-fir", "Pseudotsuga menziesii", "conifer", True,
   "Native to coastal BC",
   [("fruit", "Hanging cones with three-pointed bracts sticking out between the scales, often described as the hind legs and tail of a mouse hiding in the cone."),
    ("leaf", "Soft, flat needles 2-3 cm long arranged all around the twig (bottle-brush), with sharp-pointed, shiny reddish-brown buds."),
    ("bark", "Mature bark is very thick, corky and deeply furrowed; young bark is smooth and grey with resin blisters.")],
   [("grand fir", "Grand fir needles lie flat in two rows with notched tips and white stripes underneath; its cones stand upright and fall apart on the tree, so you rarely find whole cones on the ground."),
    ("western hemlock", "Hemlock needles are short and of uneven length, its cones are tiny (about 2 cm), and the very top of the tree nods over.")],
   "A forest-grown tree left standing alone after its neighbours are cleared is more exposed to wind than it grew up with; retain groves rather than single trees where possible.",
   "Thick bark lets mature trees survive low-intensity fire; it is a pioneer that regenerates well after disturbance in the drier coastal forests.",
   "How much of BC's remaining coastal old-growth should be logged and how much protected is a long-running debate, highlighted by the 2020 Old Growth Strategic Review and the Fairy Creek blockades on Vancouver Island.",
   "Not a true fir, hence the hyphen: the genus name Pseudotsuga means 'false hemlock'. The species name honours Archibald Menzies; the common name honours David Douglas.")

sp("tsuga-heterophylla", "western hemlock", "Tsuga heterophylla", "conifer", True,
   "Native to coastal BC",
   [("form", "The leader (very top) droops or nods over, and branch tips are soft and drooping, giving a feathery look."),
    ("leaf", "Short, flat needles of mixed lengths (hence 'heterophylla', different leaves) with two whitish bands underneath, in flattened sprays."),
    ("fruit", "Small cones about 2-3 cm long hanging from the branch tips.")],
   [("Douglas-fir", "Douglas-fir has longer, even needles all around the twig, pointed buds, an upright leader and larger cones with three-pointed bracts."),
    ("western redcedar", "Redcedar also has a slightly drooping leader, but its foliage is scale leaves, not needles.")],
   "Thrives in shade beneath other conifers; a poor choice for hot, dry, exposed sites.",
   "Very shade tolerant; seedlings often establish on rotting logs and stumps (nurse logs).",
   "",
   "Look for the nodding top: a quick way to pick hemlock out of a skyline of conifers. Washington's state tree.")

sp("abies-grandis", "grand fir", "Abies grandis", "conifer", True,
   "Native to coastal BC",
   [("leaf", "Glossy, flat needles of two lengths spread flat in two rows like a comb, with notched tips and two white bands underneath; citrus scent when crushed."),
    ("fruit", "Cones stand upright near the top of the tree and fall apart there; you find loose scales, not whole cones, on the ground."),
    ("bark", "Young bark is smooth and grey with raised resin blisters.")],
   [("Douglas-fir", "Douglas-fir needles go all around the twig, its buds are sharp-pointed, and its cones hang down with three-pointed bracts.")],
   "",
   "As a true fir (Abies) it is attacked by the introduced balsam woolly adelgid in the Pacific Northwest.",
   "",
   "Pair it with Douglas-fir: same 'fir' name, different genus. Crush a needle and smell the citrus.")

sp("callitropsis-nootkatensis", "yellow-cedar", "Callitropsis nootkatensis", "conifer", True,
   "Native to coastal BC",
   [("leaf", "Scale leaves in limp, hanging sprays that feel prickly when stroked backward; no white markings underneath."),
    ("fruit", "Small round cones about 1 cm across with 4-6 scales, each with a pointed knob; they take two years to mature."),
    ("form", "Branchlets hang vertically, giving a shaggy, weeping look; the leader droops.")],
   [("western redcedar", "Redcedar sprays are flatter and smooth to the touch, show white bow-tie marks underneath, and have small egg-shaped cones with overlapping scales.")],
   "The weeping form ('Pendula') is a popular ornamental; the inventory lists several 'weeping Alaskan yellow-cedar' on campus.",
   "Yellow-cedar decline: widespread dieback along the coast of Alaska and northern BC has been linked to reduced snowpack, which leaves shallow roots exposed to freezing.",
   "Its scientific name keeps changing (Chamaecyparis, Xanthocyparis, Callitropsis, Cupressus nootkatensis) and botanists still disagree on which genus is right.",
   "Hands-on test: stroke the foliage backward. Redcedar feels smooth, yellow-cedar feels prickly. Then ask the group which genus name they would put on the sign.")

sp("acer-circinatum", "vine maple", "Acer circinatum", "broadleaf", True,
   "Native to coastal BC",
   [("leaf", "Nearly round leaves with 7-9 shallow, toothed lobes, arranged opposite."),
    ("fruit", "Paired winged seeds (samaras) spread almost straight out to each side, often red-tinged in summer."),
    ("form", "Multi-stemmed small tree or large shrub with crooked, sprawling stems that can root where they touch the ground.")],
   [("Japanese maple", "Japanese maple leaves are deeply cut into 5-9 narrow, pointed lobes; vine maple leaves are rounder with shallow lobes.")],
   "An excellent native small tree for shady or tight spaces; fall colour is orange-red in sun and yellow in shade.",
   "An understory specialist: in deep shade it grows sprawling and vine-like; in sun it is more compact.",
   "",
   "The most-planted native broadleaf on campus (about 415 trees). 'Circinatum' refers to the rounded leaves. Ask: why use this instead of a Japanese maple?")

sp("acer-macrophyllum", "bigleaf maple", "Acer macrophyllum", "broadleaf", True,
   "Native to coastal BC",
   [("leaf", "Very large opposite leaves, often 15-30 cm across, with 5 deep lobes."),
    ("fruit", "Paired samaras with hairy seed cases, joined in a V and hanging in clusters."),
    ("bark", "Grey-brown, furrowed bark that is often thickly covered with mosses and licorice ferns.")],
   [("Norway maple", "Norway maple leaves are smaller, the broken leaf stalk oozes milky sap, and its samaras spread almost flat."),
    ("London plane", "London plane leaves are alternate (not opposite) and its bark flakes in camouflage patches.")],
   "A large, fast-growing shade tree best suited to parks and natural areas where it has room.",
   "Its bark carries heavy loads of mosses and ferns, and the tree can grow roots from its branches into these canopy soil mats.",
   "Bigleaf maple dieback has been reported in the Pacific Northwest over the past decade, with drought and heat suspected as drivers.",
   "Often said to have the largest leaves of any maple. Its sap can be tapped for syrup.")

sp("cornus-nuttallii", "Pacific dogwood", "Cornus nuttallii", "broadleaf", True,
   "Native to coastal BC",
   [("flower", "In spring, 4-7 (often 6) large white bracts surround a button of tiny greenish flowers; it sometimes blooms again in late summer."),
    ("fruit", "Clusters of shiny red-orange berry-like fruits in fall."),
    ("leaf", "Opposite oval leaves with veins that curve toward the tip; tear a leaf gently and stretchy threads hold the halves together.")],
   [("kousa dogwood", "Kousa has 4 pointed bracts, blooms about a month later after its leaves are out, and has a single raspberry-like fruit on a long stalk."),
    ("eastern flowering dogwood (Cornus florida)", "Usually 4 bracts with notched tips, and a smaller tree."),
    ("'Eddie's White Wonder'", "A hybrid of Pacific and eastern flowering dogwood; intermediate features, so check the label or bract count.")],
   "Hard to establish in urban sites; prefers well-drained soil in partial shade beneath taller trees.",
   "Dogwood anthracnose, a fungal disease (Discula destructiva) first noticed in the late 1970s, has killed many Pacific dogwoods.",
   "Should campus keep planting the native dogwood despite anthracnose, or switch to disease-resistant kousa and hybrids?",
   "BC's floral emblem. What look like petals are bracts: count them and compare with a kousa dogwood nearby.")

sp("alnus-rubra", "red alder", "Alnus rubra", "broadleaf", True,
   "Native to coastal BC",
   [("leaf", "Oval, alternate leaves with coarse double teeth; the leaf edge rolls under slightly."),
    ("bark", "Smooth, light grey bark often blotched white with lichens; scraped inner bark turns orange-red."),
    ("fruit", "Small woody cone-like catkins (about 2 cm) that stay on the tree through winter; long male catkins in early spring.")],
   [("paper birch", "Paper birch has white bark that peels in papery strips, and its leaf edges do not roll under.")],
   "A fast-growing, short-lived pioneer good for quick cover and restoration; its weak wood makes it a poor long-term street tree.",
   "Fixes nitrogen through root nodules with Frankia bacteria, enriching soils after disturbance.",
   "Long treated as a weed in conifer plantations and cut or sprayed with herbicide; now increasingly valued for soil building and as a hardwood.",
   "Scratch test: the inner bark turns orange, the 'red' in red alder. Its wood is a traditional choice for smoking salmon.")

sp("arbutus-menziesii", "arbutus (Pacific madrone)", "Arbutus menziesii", "broadleaf", True,
   "Native to coastal BC",
   [("bark", "Smooth orange-red to cinnamon bark that peels in thin papery curls in summer, revealing greenish-yellow bark beneath."),
    ("leaf", "Thick, glossy, evergreen oval leaves, dark green above and pale beneath."),
    ("flower", "Clusters of small white urn-shaped flowers in spring, followed by orange-red berries in fall.")],
   [("strawberry tree (Arbutus unedo)", "Smaller and shrubbier, with smaller leaves with toothed edges; it flowers in autumn while last year's fruit ripens.")],
   "Notoriously hard to transplant; needs sharp drainage and dislikes summer irrigation and root disturbance.",
   "A tree of dry, rocky coastal sites in the Strait of Georgia region.",
   "",
   "Often described as Canada's only native broadleaf evergreen tree. Invite people to touch the cool, smooth bark.")

sp("quercus-garryana", "Garry oak", "Quercus garryana", "broadleaf", True,
   "Native to BC (mainly SE Vancouver Island and the Gulf Islands)",
   [("leaf", "Leathery, glossy dark green leaves with 5-7 deep, rounded lobes, paler beneath."),
    ("bark", "Thick, grey, deeply furrowed bark."),
    ("form", "On open sites, a broad spreading crown with gnarled, twisting branches.")],
   [("English oak", "English oak leaves have very short stalks and small ear-like lobes at the base, and its acorns hang on long stalks; Garry oak acorns sit almost directly on the twig.")],
   "Slow-growing; summer watering of established trees is often discouraged because it can promote root disease.",
   "Garry oak ecosystems are among the most endangered in Canada; only a small fraction remains in near-natural condition.",
   "Native where? Garry oak is BC's only native oak, but its natural range is mostly SE Vancouver Island and the Gulf Islands. On Point Grey it is planted. Does that count as a native planting?",
   "BC's only native oak. South Commons holds 17 of the 21 on campus.")

# ---------------- NON-NATIVE ----------------
sp("pinus-nigra", "Austrian (black) pine", "Pinus nigra", "conifer", False,
   "Non-native: southern Europe, Turkey and North Africa",
   [("leaf", "Stiff, dark green needles 8-15 cm long, in bundles of 2."),
    ("bark", "Dark grey-brown bark broken into deep fissures and flat, scaly plates."),
    ("form", "Dense, dark, broad crown; older trees often become flat-topped.")],
   [("Scots pine", "Scots pine has shorter (3-7 cm), twisted, blue-green needles and orange, flaky bark on the upper trunk."),
    ("shore (lodgepole) pine", "Shore pine has short (3-7 cm), twisted, yellow-green needles and small cones that stay on the branches for years.")],
   "Tolerant of wind, salt and urban stress, which is why it was widely planted for shelter.",
   "Prone to Diplodia tip blight, a common fungal disease of planted Austrian pines.",
   "",
   "Count needles per bundle: 2 (Austrian, Scots, shore pine), 3 (ponderosa), 5 (western white pine). The most common non-native conifer on campus.")

sp("cedrus-deodara", "deodar cedar", "Cedrus deodara", "conifer", False,
   "Non-native: western Himalaya",
   [("leaf", "Needles 2.5-5 cm long in dense tufts on short spur shoots, single on new long shoots."),
    ("form", "Branch tips and the leader droop gracefully; broadly conical crown."),
    ("fruit", "Barrel-shaped cones sit upright on the branches and break apart on the tree.")],
   [("Atlas cedar", "Atlas cedar has shorter needles (under 2.5 cm), often blue-grey, and stiffer, upswept branches."),
    ("larch", "Larch also has needles in tufts, but they are soft, deciduous (turn gold and drop in fall), and its cones are small.")],
   "A large specimen tree for open lawns; its sweeping lower branches need room.",
   "The national tree of Pakistan.",
   "Which trees deserve the name 'cedar'? Only Cedrus is a true cedar; western redcedar, yellow-cedar and incense-cedar are in the cypress family, which is why careful usage writes their names as one word or with a hyphen.",
   "Meet a true cedar, then walk to a western redcedar and compare. 'Deodar' comes from Sanskrit 'devadaru', timber of the gods.")

sp("sequoiadendron-giganteum", "giant sequoia", "Sequoiadendron giganteum", "conifer", False,
   "Non-native: Sierra Nevada, California",
   [("leaf", "Awl-shaped, scale-like needles that clasp the twig and overlap all around it, making shoots look like ropes."),
    ("bark", "Very thick, soft, spongy, fibrous red-brown bark: you can press into it without hurting your hand."),
    ("form", "Massive columnar trunk with strong taper and a dense, conical crown; branch tips turn upward.")],
   [("coast redwood", "Coast redwood has flat needles in two rows on most shoots (like a yew), with white bands beneath, and smaller cones (about 2 cm vs 5-7 cm)."),
    ("Japanese cedar (Cryptomeria)", "Cryptomeria also has awl-shaped needles, but they curve forward, and its bark is thinner and stringy.")],
   "A dramatic specimen for large open spaces; its eventual size makes it unsuitable close to buildings or utilities.",
   "Fire-adapted: thick bark protects the trunk and heat helps open the cones to release seed.",
   "Severe wildfires in 2020-2021 killed a substantial share of the world's large giant sequoias. Should we plant them well outside their native range as a kind of insurance?",
   "The largest tree on Earth by volume. Press the spongy bark. Campus's biggest recorded is near the First Nations Garden.")

sp("metasequoia-glyptostroboides", "dawn redwood", "Metasequoia glyptostroboides", "conifer", False,
   "Non-native: central China",
   [("leaf", "Soft, flat, feathery needles arranged opposite each other on short shoots that drop with the needles."),
    ("seasonal", "A deciduous conifer: needles turn russet-orange in fall and drop; the tree is bare in winter."),
    ("bark", "Reddish, fibrous bark on a fluted, buttressed trunk, with 'armpit' hollows beneath the branches.")],
   [("bald cypress (Taxodium distichum)", "Bald cypress needles and branchlets are alternate, not opposite."),
    ("coast redwood", "Coast redwood is evergreen and its needles are stiffer and alternate.")],
   "Fast-growing and tolerant of wet soils; a striking avenue or pond-edge tree that needs space.",
   "Described from fossils in 1941 before living trees were found in China in the 1940s; seed sent out in 1948 spread it to gardens worldwide.",
   "Listed as Endangered in the wild, yet planted widely around the world. Does abundance in gardens help conservation of the wild populations?",
   "A 'living fossil' and a conifer that drops its needles every fall. Point to the armpits under the branches.")

sp("ginkgo-biloba", "ginkgo", "Ginkgo biloba", "ginkgo", False,
   "Non-native: China",
   [("leaf", "Fan-shaped leaves with fine parallel veins that fork, often with a notch in the middle splitting the fan into two lobes."),
    ("form", "Leaves grow in clusters on short, knobby spur shoots along the branches."),
    ("seasonal", "Leaves turn bright butter-yellow in fall and often drop almost all at once.")],
   [],
   "A very tough urban street tree, tolerant of pollution and compaction. Male trees are usually planted to avoid the female trees' foul-smelling seeds.",
   "The only living species of an ancient lineage of seed plants; several ginkgos survived the Hiroshima atomic bombing near the hypocentre.",
   "Planting only male trees avoids the smelly seeds but adds pollen; some critics call this 'botanical sexism', while others dispute how much it matters for allergies.",
   "Neither a conifer nor a flowering tree. The campus inventory even mislabels it 'Angiosperm' on several records, which makes a nice data-quality story.")

sp("acer-platanoides", "Norway maple", "Acer platanoides", "broadleaf", False,
   "Non-native: Europe and western Asia",
   [("leaf", "Broad leaves with 5 lobes and a few long pointed teeth; snap the leaf stalk and it oozes milky sap."),
    ("fruit", "Paired samaras spread almost flat, like a straight line."),
    ("flower", "Bright yellow-green flower clusters appear before the leaves in early spring.")],
   [("sugar maple", "Sugar maple sap is clear and its samaras form a U shape."),
    ("sycamore maple", "Sycamore maple leaves are thicker with coarse rounded teeth, the sap is clear, and samaras meet at about a right angle."),
    ("bigleaf maple", "Bigleaf maple leaves are much larger, often wider than 15 cm.")],
   "A very tough street tree, but it casts dense shade and has shallow roots that suppress grass. Purple cultivars such as 'Royal Red' are on campus.",
   "In eastern North American forests its dense shade and abundant seedlings can crowd out native understory plants.",
   "Listed as invasive and banned from sale in some US states, yet still a common street tree. Should campus stop planting it?",
   "Snap a leaf stalk: milky sap. The most common non-native broadleaf on campus (about 406 trees).")

sp("acer-palmatum", "Japanese maple", "Acer palmatum", "broadleaf", False,
   "Non-native: East Asia (Japan, Korea, China)",
   [("leaf", "Small, deeply cut palm-shaped leaves with 5-9 pointed, toothed lobes, arranged opposite."),
    ("form", "Low, layered crown with graceful horizontal branches, often multi-stemmed."),
    ("seasonal", "Brilliant red, orange or yellow fall colour; many cultivars have red or purple leaves all season.")],
   [("vine maple", "Vine maple leaves are rounder with 7-9 shallow lobes rather than deeply cut ones.")],
   "An excellent small-scale accent tree; leaves scorch in hot, reflective sites.",
   "Cultivated in Japan for centuries, with hundreds of named cultivars.",
   "Should native vine maple replace Japanese maple in campus plantings where a similar form is wanted?",
   "Campus has red-leaved 'Atropurpureum', lace-leaf 'Dissectum' and coral-bark 'Sangokaku', all one species.")

sp("acer-x-freemanii", "Freeman maple", "Acer × freemanii", "broadleaf", False,
   "Non-native hybrid of two eastern North American maples (red × silver)",
   [("leaf", "Opposite leaves with 3-5 lobes, more deeply cut than red maple but less than silver maple."),
    ("seasonal", "Bright red to orange fall colour in cultivars such as 'Autumn Blaze'."),
    ("form", "Vigorous, upright to oval crown.")],
   [("red maple", "Red maple leaves usually have 3 shallow lobes and red leaf stalks; hybrids can be hard to separate."),
    ("silver maple", "Silver maple leaves are very deeply cut with silvery undersides.")],
   "Heavily planted as a street tree because it combines silver maple's vigour with red maple's fall colour.",
   "The cross also occurs naturally where the two parent species overlap.",
   "Maple overload: maples (Acer) make up about 22% of identified campus trees, above the 20% per-genus guideline often used for urban forest diversity. What happens if a maple pest arrives?",
   "A hybrid of two eastern maples. Use it to introduce the 10-20-30 diversity guideline with real UBC numbers.")

sp("prunus-serrulata", "Japanese flowering cherry", "Prunus serrulata", "broadleaf", False,
   "Non-native: East Asia (mostly garden cultivars)",
   [("flower", "Showy clusters of pink or white flowers, often double, in April, with or just before reddish-bronze new leaves."),
    ("bark", "Shiny reddish-brown bark with prominent horizontal stripes (lenticels)."),
    ("leaf", "Oval leaves with finely toothed, bristle-tipped edges.")],
   [("Yoshino cherry (Prunus × yedoensis)", "Single, pale pink-white flowers that open before the leaves, usually earlier than Kanzan-type cherries; 'Akebono' is on campus."),
    ("cherry plum (Prunus cerasifera)", "Smaller, earlier single flowers, and usually purple leaves.")],
   "A spectacular two-week spring show from a short-lived tree prone to diseases such as bacterial canker.",
   "Most campus trees are grafted garden cultivars (the Sato-zakura group); double-flowered ones such as 'Kanzan' rarely set fruit.",
   "Is two weeks of blossom worth the street space of a short-lived, disease-prone tree?",
   "Read the bark: horizontal lenticel stripes identify cherries year-round, even in winter.")

sp("quercus-rubra", "northern red oak", "Quercus rubra", "broadleaf", False,
   "Non-native: eastern North America",
   [("leaf", "Leaves with 7-11 pointed, bristle-tipped lobes; the gaps between lobes reach about halfway to the midrib."),
    ("bark", "Ridged bark with smooth, flat, shiny stripes running down the ridges ('ski tracks') on mature trunks."),
    ("fruit", "Large acorns (2-3 cm) with a shallow, beret-like cap; they take two years to mature.")],
   [("pin oak", "Pin oak leaves are smaller with deep C-shaped gaps, lower branches droop, and acorns are small."),
    ("Garry oak", "Garry oak leaves have rounded lobes with no bristle tips (white oak group).")],
   "One of the faster-growing oaks; a large, long-lived shade tree for wide boulevards.",
   "Red oak group oaks have bristle-tipped lobes and acorns that take two years to mature; white oak group oaks (Garry, English) have rounded lobes and one-year acorns.",
   "",
   "Bristle tips mean red oak group. Walk from a red oak to a Garry oak to compare the two groups.")

sp("cercidiphyllum-japonicum", "katsura", "Cercidiphyllum japonicum", "broadleaf", False,
   "Non-native: Japan and China",
   [("leaf", "Rounded to heart-shaped leaves with scalloped edges, opposite on long shoots; new leaves emerge reddish-purple."),
    ("seasonal", "Fall leaves turn yellow, apricot and pink and smell like burnt sugar or cotton candy."),
    ("bark", "Often multi-stemmed, with shaggy, shredding bark on older trunks.")],
   [("redbud (Cercis)", "Redbud also has heart-shaped leaves, but they are alternate with smooth edges, and it has pink pea-like flowers on bare branches in spring.")],
   "Needs steady moisture; leaves scorch and drop early in drought and heat.",
   "The sweet smell comes from maltol, a compound released as the fallen leaves break down.",
   "",
   "The name means 'Cercis-leaf'. In October, sniff the fallen leaves for burnt sugar. University Boulevard is lined with them.")

sp("cornus-kousa", "kousa dogwood", "Cornus kousa", "broadleaf", False,
   "Non-native: Japan, Korea and China",
   [("flower", "Four pointed, creamy-white bracts in early summer, after the leaves are out."),
    ("fruit", "Round, bumpy, pinkish-red fruit like a raspberry on a long stalk in late summer; edible."),
    ("bark", "Mottled bark that flakes in patches of tan, grey and brown on older trees.")],
   [("Pacific dogwood", "Pacific dogwood usually shows 4-7 rounded bracts, blooms earlier in spring, and has clusters of separate red fruits."),
    ("eastern flowering dogwood", "Its 4 bracts have notched tips, it blooms before the leaves, and its fruits are in clusters.")],
   "Widely planted as an alternative to native dogwoods because it is more resistant to dogwood anthracnose.",
   "The fruit is eaten by birds and people, though it is seedy.",
   "Does replacing native Pacific dogwood with disease-resistant kousa make sense for wildlife and local identity?",
   "Taste test in September: the fruit is edible. The biggest campus cluster is near MacMillan.")

sp("liquidambar-styraciflua", "sweetgum", "Liquidambar styraciflua", "broadleaf", False,
   "Non-native: southeastern US to Central America",
   [("leaf", "Glossy, star-shaped leaves with 5-7 pointed lobes, arranged alternate (maples are opposite)."),
    ("fruit", "Spiky, woody 'gumballs' hanging on long stalks, persisting into winter."),
    ("bark", "Deeply furrowed grey-brown bark; twigs on some trees have corky wings.")],
   [("maples", "Maples have opposite leaves and winged samaras; sweetgum has alternate leaves and spiky balls.")],
   "Brilliant, long-lasting fall colour, but the spiky gumballs are a slip and litter nuisance on paths; the fruitless cultivar 'Rotundiloba' avoids them.",
   "The name Liquidambar ('liquid amber') refers to its fragrant resin.",
   "Fruitless cultivars solve the litter problem but remove seeds that some birds eat. Who should the tree serve?",
   "Opposite or alternate? A star-shaped 'maple' with alternate leaves is a sweetgum. The inventory also calls it 'alligator-wood'.")

sp("platanus-x-hispanica", "London plane", "Platanus × hispanica", "broadleaf", False,
   "Non-native hybrid (oriental plane × American sycamore)",
   [("bark", "Camouflage-patterned bark that flakes off in patches of cream, olive and grey."),
    ("leaf", "Large, maple-like leaves with 3-5 lobes, arranged alternate; the hollow base of the leaf stalk hides the bud."),
    ("fruit", "Round, bristly seed balls on long stalks, usually two per stalk, hanging into winter.")],
   [("American sycamore", "Seed balls usually single, and the upper bark is whiter."),
    ("sycamore maple", "Despite the name, a maple: opposite leaves and winged samaras.")],
   "A classic tough urban tree that tolerates compaction, pollution and heavy pruning such as pollarding.",
   "Anthracnose, a fungal disease, causes spring leaf and shoot blight in cool, wet springs.",
   "Fine hairs shed from leaves and seed balls can irritate eyes and airways. Is it still the right default city tree?",
   "Pull off a leaf: the bud is hidden inside the hollow base of the stalk. A hybrid that became the street tree of many world cities.")

sp("ilex-aquifolium", "English holly", "Ilex aquifolium", "broadleaf", False,
   "Non-native: Europe, western Asia and North Africa",
   [("leaf", "Glossy, leathery, dark green evergreen leaves with wavy, spiny edges; upper leaves on older plants are often less spiny."),
    ("fruit", "Bright red berries in winter, on female plants only."),
    ("form", "Dense, pyramidal shrub or small tree with smooth grey bark.")],
   [("Oregon-grape (Berberis aquifolium)", "Spiny leaflets on compound leaves, and blue berries."),
    ("holly-leaved osmanthus", "Leaves are opposite; holly leaves are alternate.")],
   "A traditional hedge and festive greenery plant, but bird-spread seeds let it escape into nearby forests such as Pacific Spirit Regional Park.",
   "Birds eat the berries and spread the seeds; shade-tolerant seedlings form dense thickets in the forest understory.",
   "Holly is grown commercially for holiday greenery in the region while volunteers pull it out of forests. Plant it or pull it?",
   "Compare spiny lower leaves with smoother upper leaves; research suggests browsing pressure influences how prickly holly leaves are.")

# -------------- emit --------------
def field(text):
    return {"text": text, "status": "needs_check" if text else "blank"}

out = {"schema": 1,
       "status_legend": {"needs_check": "AI-drafted, not yet verified", "verified": "checked by the author", "blank": "left empty on purpose (no confident fact)"},
       "native_definition": "Native = native to coastal BC (default; confirm)",
       "species": []}
for s in S:
    assert len(s["feats"]) == 3, s["id"]
    out["species"].append({
        "id": s["id"], "common": s["common"], "botanical": s["botanical"], "group": s["group"],
        "native": {"value": s["native"], **field(s["origin"])},
        "id_features": [{"type": t, **field(x)} for t, x in s["feats"]],
        "lookalikes": [{"name": n, **field(h)} for n, h in s["looks"]],
        "design": field(s["design"]), "ecology": field(s["ecology"]),
        "controversy": field(s["controversy"]), "tour_point": field(s["tour"]),
    })
assert len(out["species"]) == 26
json.dump(out, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
blank = sum(1 for s in out["species"] for k in ("design", "ecology", "controversy", "tour_point") if s[k]["status"] == "blank")
print(len(out["species"]), "species written;", blank, "fields left blank;", sum(1 for s in out["species"] if not s["lookalikes"]), "with no look-alikes")
