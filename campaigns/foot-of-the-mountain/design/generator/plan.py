#!/usr/bin/env python3
"""The town at the foot of the mountain: the whole plan, generated.

Writes world.json, layout-graph.json, site-plan.json, geometry-brief.json,
quest-plan.json, quests.json and terrain/island.png into the campaign
directory. Stdlib only. Deterministic: no clock, no unseeded randomness.

Axes: +x east, +z south. The sea is south; the mountain is north. The main
street runs north to south from the square at the mountain's foot down to the
quay. Every box but the square is placed by the seam packing; this script
mirrors that packing to shape the terrain under each box.
"""
import json
import math
import os
import struct
import sys
import zlib

CAMPAIGN = "foot-of-the-mountain"
DSL = "0.69.0"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

RX, RZ = 320, 512          # the island's frame (saltstair-a: 144 x 224; 5.08x); the region reaches past it
RY0, RYN = 40, 176         # region y span
BASE_Y, RANGE = 40, 168    # heightmap: y = 40 + v * 168 // 255
SEA = 62

boxes = []                 # site-plan boxes, in order
seams = []
nodes = []
edges = []
pos = {}                   # node -> (x0, z0, dx, dz, floor)


def box(node, extent, floor, ceiling, intent, note, holds=None, way=None,
        roof=None, pin=None):
    b = {"node": node, "extent": list(extent), "floor": {"y": floor},
         "ceiling": ceiling}
    if way:
        b["way"] = way
    if roof:
        b["roof"] = roof
    if pin:
        b["min"] = list(pin)
        pos[node] = (pin[0], pin[1], extent[0], extent[1], floor)
    boxes.append(b)
    n = {"id": node, "intent": intent, "note": note}
    if holds:
        n["holds"] = holds
    if node in REFS:
        n["references"] = REFS[node]
    elif node.split("/")[1].split("-")[0] in ("street", "flight", "lane", "square"):
        n["references"] = STREET_REFS
    nodes.append(n)
    return b


def ext(node):
    for b in boxes:
        if b["node"] == node:
            return b["extent"], b["floor"]["y"]
    raise KeyError(node)


def seam(a, b, face, at, meets, kind, form, span=None):
    """Join a to b on a's `face`; place b by the packing rule. A contact
    with a `span` (width, height) meets only over that run, from `at`/`meets`."""
    eid = "edge/" + a.split("/")[1] + "-to-" + b.split("/")[1]
    s = {"edge": eid, "face": face, "at": at, "meets": meets, "form": form}
    cls = "walk"
    if kind == "contact":
        s["contact"] = {"extent": list(span)} if span else {}
    elif kind == "stair":   # a is the upper place, b the flight below it
        (bdx, bdz), _ = ext(b)
        w = bdx if face in ("north", "south") else bdz
        s["opening"] = {"width": w, "height": 4}
        s["stair_in"] = b
        cls = "stair"
    seams.append(s)
    edges.append({"a": a, "b": b, "class": cls, "id": eid})
    ax, az, adx, adz, _ = pos[a]
    (bdx, bdz), bf = ext(b)
    # the packing leaves the one shared ring cell between two boxes
    if face == "south":
        p = (ax + at - meets, az + adz + 1)
    elif face == "north":
        p = (ax + at - meets, az - bdz - 1)
    elif face == "east":
        p = (ax + adx + 1, az + at - meets)
    else:
        p = (ax - bdx - 1, az + at - meets)
    pos[b] = (p[0], p[1], bdx, bdz, bf)
    return eid


OPEN = lambda n: {"open": n}

# Community and historical reference builds per plot: looked at for form and
# room layout, never copied (an unlicensed or non-commercial source is ideas only).
# The streets, flights, lanes and the square share one set: the medieval
# cobbled street with its central kennel, and the stepped street of a harbour town.
STREET_REFS = [
    {"url": "https://oxmag.co.uk/articles/brasenose-lane",
     "shows": "Brasenose Lane, Oxford: a cobbled lane whose kennel runs down the middle of the road, the cobbles falling to it rather than cambered to either side; such gutters once ran down every thoroughfare.",
     "terms": "none stated for the text (images © Morris Oxford); ideas only"},
    {"url": "https://en.wikipedia.org/wiki/Cobblestone",
     "shows": "Medieval cobbles: rounded field and river stones set in sand or mortar, the surface moving with the ground; pitched paving and setts for the dressed parts.",
     "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    {"url": "https://en.wikipedia.org/wiki/The_Shambles",
     "shows": "York's Shambles at eye level: a narrow street of timber-framed shops whose upper storeys overhang it, shopfronts with their hooks and display shelves to the street, runnels for the rain.",
     "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    {"url": "https://en.wikipedia.org/wiki/Market_town",
     "shows": "The medieval market place: a wide main street or a square where stalls and booths stand on market day, a market cross at its middle, a market hall beside it.",
     "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    {"url": "https://en.wikipedia.org/wiki/Clovelly",
     "shows": "Clovelly: a steep, pedestrian, cobbled main street of terraced houses falling to the pier, goods moved by sledge and donkey, broken by side alleys.",
     "terms": "CC BY-SA 4.0 (Wikipedia text)"},
]

REFS = {
    # the lower street's chandler and tannery (content demo/plots-lower @ e236131)
    "node/chandler": [
        {"url": "https://en.wikipedia.org/wiki/Sail_Loft_(Tenants_Harbor,_Maine)",
         "shows": "A harbour chandlery of 1860: the chandler's store on the ground floor with its counters and fixtures, a loft above, gable windows and an upper materials door in one end.",
         "terms": "CC BY-SA 4.0 (ideas only)"},
        {"url": "https://igg.org.uk/rail/12-linind/dockind.htm",
         "shows": "A dockside chandlery is warehouse-like, its upper doors served by cat-head hoists, stocking rope, blocks and tackle, sails, paint and stores.",
         "terms": "none stated (ideas only)"},
        {"url": "https://sketchfab.com/3d-models/medieval-port-city-e66255aa77c041ed9517426ee0926856",
         "shows": "A community-built Minecraft harbour town's wharf with storage warehouses beside the businesses that serve the harbour.",
         "terms": "CC BY 4.0 (ideas only)"},
    ],
    "node/tannery": [
        {"url": "https://sitelines.newcastle.gov.uk/SMR/2051",
         "shows": "A tannery's open yard of pits, oblong for soaking and liming, square for tanning, a row of small pits along one side, ringed by long buildings with drying lofts and a bark house.",
         "terms": "none stated (ideas only)"},
        {"url": "https://coflein.gov.uk/en/site/41220",
         "shows": "A traditional tannery: hides limed, scraped, then tanned in pits of oak-bark liquor in the yard; drying and currying lofts; a single-storey beam house where hides are defleshed; a bark barn.",
         "terms": "Non-commercial Government Licence (ideas only)"},
    ],
    # the lower street's rows (content demo/plots-lower @ b505915), carried here
    "node/boatwright": [
        {"url": "https://www.minecraft-guides.com/mod/alekis-nifty-ships/",
         "shows": "A Minecraft boat built in stages on land: the hull's frames laid in the hull pattern first and filled with planks frame by frame, and unfinished rowboats and sloops standing half-built on the shore.",
         "terms": "none stated (ideas only)"},
        {"url": "https://minecraft.how/blog/post/build-pirate-ship-minecraft",
         "shows": "A community ship-building guide: lay the keel first down the centre line, raise the frame from it angled outward, taper the hull toward bow and stern, and build on land.",
         "terms": "all rights reserved (ideas only)"},
        {"url": "https://her.cne-siar.gov.uk/Monument/MWE148761",
         "shows": "A small boatbuilding yard: a single-storey shed with its door to the slipway, the long plank steamer against an inside wall over a fire, clinker boats built inside.",
         "terms": "none stated (ideas only)"},
    ],
    "node/cooper": [
        {"url": "https://www.brothers-brick.com/2021/08/24/roll-out-the-barrel-with-this-medieval-coopers-workshop",
         "shows": "A community-built medieval cooper's workshop: the work floor at ground open on one side so the scorching of a barrel is seen, the family's rooms beside and above, beams over jagged stonework.",
         "terms": "none stated (ideas only)"},
        {"url": "https://museum.wales/collections/online/object/6761dd14-e787-3d33-87f2-6b3012da9b86",
         "shows": "A cooper's shaving horse, the bench he sits astride to hold and shape the staves for barrels: the working object of the cooperage floor.",
         "terms": "none stated; image by permission of the museum (ideas only)"},
    ],
    "node/cottages-2": [
        {"url": "https://en.wikipedia.org/wiki/True%27s_Yard_Fisherfolk_Museum",
         "shows": "Fisherfolk cottages of one room down and one up, a whole family in each, in a row off a shared yard.",
         "terms": "CC BY-SA 4.0 (ideas only)"},
        {"url": "https://charliecustard.com/downloads/waterway-cottage",
         "shows": "A community-built medieval waterside cottage on a stone foundation, small and tall, with balconies over the water.",
         "terms": "none stated; site terms of service (ideas only)"},
        {"url": "https://sketchfab.com/3d-models/medieval-port-city-e66255aa77c041ed9517426ee0926856",
         "shows": "A community-built Minecraft harbour town's fishermen's village: small cottages close together near the water.",
         "terms": "CC BY 4.0 (ideas only)"},
    ],
    "node/fishmonger": [
        {"url": "https://buildinghistory.org/buildings/shops.shtml",
         "shows": "How a medieval shop front was built: a wide unglazed opening whose upper shutter hooks up as an awning and whose lower one folds down as the counter, the living or working space behind.",
         "terms": "none stated (ideas only)"},
        {"url": "https://en.wikipedia.org/wiki/True%27s_Yard_Fisherfolk_Museum",
         "shows": "A fisher family's fishmonger's in the front room on the street, with the smokehouse at the rear of the house where the herring were hung and smoked.",
         "terms": "CC BY-SA 4.0 (ideas only)"},
        {"url": "https://sketchfab.com/3d-models/medieval-port-city-e66255aa77c041ed9517426ee0926856",
         "shows": "A community-built Minecraft harbour town whose north side holds an outer market and a fishermen's village beside the wharf.",
         "terms": "CC BY 4.0 (ideas only)"},
    ],
    "node/netloft": [
        {"url": "https://www.hastingshistory.net/hastings-net-shops",
         "shows": "The Hastings net shops: tall, narrow, tarred weatherboarded sheds of up to three storeys, a ladder through each floor, nets coiled and hung from the beams for storage and dried on the beach outside, rows of shops with capstans between them.",
         "terms": "none stated; copyright notice only (ideas only)"},
        {"url": "https://www.meer.com/en/42331-net-sheds",
         "shows": "Baltic net sheds set at right angles to the sea, each owner's row of net-drying beams starting at his shed door, the drying ground and the boat landing between the sheds.",
         "terms": "none stated"},
        {"url": "https://www.mc-mod.net/?p=538592",
         "shows": "A community fisherman's waterside house in stripped spruce and stone, 17 by 20 and 22 tall: the tall timber-on-stone massing of a harbour work building.",
         "terms": "none stated"},
    ],
    "node/smithy": [
        {"url": "https://minecraft.how/blog/post/build-blacksmith-shop-minecraft",
         "shows": "A blacksmith laid out along the material's path: the fire and smelting on one side, the anvils in the middle with room to work round them, the grindstone beside the anvils, storage opposite; dark masonry, chains and lanterns hung from the beams.",
         "terms": "none stated; page footer: all rights reserved (ideas only)"},
        {"url": "https://www.curseforge.com/minecraft/mc-mods/blacksmith-structures",
         "shows": "A vanilla-block village smithy whose interior and exterior pictures put the forge against a stone wall at one end of a timber building, the anvil before it and the work open to the yard.",
         "terms": "CC BY-NC 3.0 (ideas only)"},
    ],
    "node/tavern": [
        {"url": "https://www.hukins-hops.co.uk/our-story/news-press/brewery-in-minecraft",
         "shows": "Minecraft brewery and tavern builds: a rustic taproom with warm lighting, the brewing done apart at a stone counter with cauldrons of water beside it, a cellar below.",
         "terms": "none stated"},
        {"url": "https://www.profitableventure.com/beer-garden-design-ideas-layout-floor-plan/",
         "shows": "Beer-garden layouts: pergolas over the seating zones dressed in climbing greenery and lights, communal tables with benches, the garden edged with hedges and planting.",
         "terms": "none stated"},
    ],
    # the landmarks worker's rows (content demo/town-buildings @ a82f763), carried here
    "node/cathedral": [
        {"url": "https://minecraftonline.com/wiki/Cathedral",
         "shows": "A community cathedral at nearly this plot's scale (30 x 50 x 30): take the west front's three portals, each a pointed opening under archivolts that step inward in layers, and the nave vault built as stepped courses rising from every pier head to the crown.",
         "terms": "CC BY-NC-SA 3.0 (the wiki's stated licence): ideas only"},
        {"url": "https://store.abfielder.com/products/gothic-cathedral-with-interior",
         "shows": "A vanilla Gothic cathedral in deepslate, tuff and andesite: take the bay rhythm of a buttress pier between every pair of tall paired lancets, wall planes broken into two and three depths, clustered piers on broad bases down a chequered nave.",
         "terms": "none stated beyond the store's EULA and terms of sale: ideas only"},
        {"url": "https://minecraft.how/pt/blog/post/build-cathedral-minecraft",
         "shows": "A cathedral-building guide: take buttresses projecting two to three cells and tapering as they rise, a vault faked with upside-down stairs, pews of stairs, and light gathered at the altar rather than spread evenly.",
         "terms": "all rights reserved: ideas only"},
    ],
    "node/harbour": [
        {"url": "https://sketchfab.com/3d-models/medieval-port-city-e66255aa77c041ed9517426ee0926856",
         "shows": "A community-built harbour town (TheAvatar): take the harbour building standing on the quay with its front to the water, the paved waterfront between the buildings and the edge, and boats lying alongside it.",
         "terms": "CC BY 4.0 (stated on the page): ideas only"},
        {"url": "https://sketchfab.com/3d-models/harbor-village-f4b14a5ed28848efb78131a20217fca3",
         "shows": "A community-built harbour (madexc): take a stone quay edge lined by timber-framed buildings on a stone ground course, and a moored boat with its mast up and sails on the yard.",
         "terms": "CC BY 4.0 (stated on the page): ideas only"},
        {"url": "https://en.wikipedia.org/wiki/Lucarne",
         "shows": "The lucarne: a housing high on a store's wall, the roof run out past the gable on a strong ridge timber carrying the hoist over the loading doors of every floor beneath it.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    ],
    # the landmarks worker's lighthouse rows (content demo/town-buildings @ f4ae754)
    "node/lighthouse": [
        {"url": "https://sketchfab.com/3d-models/big-lighthouse-08bbb2483fe246dca8ff3c458b18047d",
         "shows": "A community lighthouse (madexc): take the shaft stepping in once below the top, a corbelled gallery ring and a fully glazed lantern room under a dark cap.",
         "terms": "CC BY 4.0 (stated on the page): ideas only"},
        {"url": "https://sketchfab.com/3d-models/lighthouse-874941099c94487eadef57c80f628271",
         "shows": "A community lighthouse (madexc): take an octagonal tower on a dark stone plinth, a projecting gallery with a railing, and the lantern room's roof rising to a finial.",
         "terms": "CC BY 4.0 (stated on the page): ideas only"},
        {"url": "https://sketchfab.com/3d-models/quay-and-lighthouse-0460777c48b040b7884c19a709d13287",
         "shows": "A community harbour lighthouse (l4ziness): take a banded masonry shaft with small windows up the stair, a timber gallery on corbels below a glazed lantern room, and the tower's foot meeting a walled quay.",
         "terms": "none stated: ideas only"},
    ],
    "node/bakery": [
        {"url": "https://en.wikipedia.org/wiki/Masonry_oven",
         "shows": "The bread oven: a brick or clay dome on a raised hearth, fired inside (a black oven), smoke out at the door or a flue over it, nearly always under a roof against the weather.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
        {"url": "https://www.planetminecraft.com/project/medieval-town-bakery/",
         "shows": "A Minecraft medieval town bakery (TheAvatar): two storeys, the shopfront below and the baker's rooms above, two small ovens out back (read from its listing; the page refuses an automated fetch).",
         "terms": "not read (the page refuses an automated fetch); ideas only"},
    ],
    "node/apothecary": [
        {"url": "https://en.wikipedia.org/wiki/Apothecary",
         "shows": "The apothecary's trade: remedies of herbs, minerals and animal matter prepared and dispensed over a counter, weighed small, shaped vessels for what is dangerous.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
        {"url": "https://en.wikipedia.org/wiki/Physic_garden",
         "shows": "The physic garden: the medieval garden's own section for medicinal plants, the hortus medicus, beside the house that uses them.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
        {"url": "https://www.planetminecraft.com/project/medieval-apothecary/",
         "shows": "A Minecraft medieval apothecary, its potion shop fully furnished with a brewing tower at the back (read from its listing; the page refuses an automated fetch).",
         "terms": "not read (the page refuses an automated fetch); ideas only"},
    ],
    "node/weaver": [
        {"url": "https://en.wikipedia.org/wiki/Weavers%27_cottage",
         "shows": "The weavers' cottage: a tall house whose loomshop is lit by a long row of many-light windows along one wall, the family below, storage beside the looms.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
        {"url": "https://en.wikipedia.org/wiki/Tenter",
         "shows": "The tenter: a large wooden frame the wet cloth is stretched on to dry without shrinking, its edges on tenterhooks; tentergrounds of them stood in the open wherever cloth was made.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    ],
    "node/potter": [
        {"url": "https://her.northamptonshire.gov.uk/Monument/MNN28914",
         "shows": "A late medieval pottery kiln and its workshop: a thick-walled kiln with opposed flues and a stoke pit, the workshop beside it, wasters thrown about.",
         "terms": "Northamptonshire HER terms of use (linked from the page); ideas only"},
        {"url": "https://en.wikipedia.org/wiki/Masonry_oven",
         "shows": "Fired brick built in courses closing to a dome, smoke out at a flue: the kiln's construction in the town's brick.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    ],
    "node/cottages": [
        {"url": "https://en.wikipedia.org/wiki/Cottage",
         "shows": "The cottage: modest, often semi-detached, low-ceilinged with its timbers showing, a garden enough to feed the family, built of the cheapest local stuff (rubble stone, whitewash, slate); the fisherman's one-roomed penty.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    ],
    "node/townhall": [
        {"url": "https://en.wikipedia.org/wiki/Market_house",
         "shows": "The market house: an arcade on the ground floor sheltering the traders and their goods, the upper floor for civic use, on the market square (Titchfield Market Hall, 1620s).",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
        {"url": "https://en.wikipedia.org/wiki/Guildhall",
         "shows": "The guildhall: market trading on its ground floor, the officers' offices and the board's meetings in it, the guild's arms on the facade; in Britain, the town hall.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    ],
    # the quay: the harbour's rows fit it
    "node/quay": [
        {"url": "https://sketchfab.com/3d-models/medieval-port-city-e66255aa77c041ed9517426ee0926856",
         "shows": "A community-built harbour town (TheAvatar): take the harbour building standing on the quay with its front to the water, the paved waterfront between the buildings and the edge, and boats lying alongside it.",
         "terms": "CC BY 4.0 (stated on the page): ideas only"},
        {"url": "https://sketchfab.com/3d-models/harbor-village-f4b14a5ed28848efb78131a20217fca3",
         "shows": "A community-built harbour (madexc): take a stone quay edge lined by timber-framed buildings on a stone ground course, and a moored boat with its mast up and sails on the yard.",
         "terms": "CC BY 4.0 (stated on the page): ideas only"},
        {"url": "https://en.wikipedia.org/wiki/Lucarne",
         "shows": "The lucarne: a housing high on a store's wall, the roof run out past the gable on a strong ridge timber carrying the hoist over the loading doors of every floor beneath it.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    ],
    "node/inn": [
        {"url": "https://store.abfielder.com/products/%F0%9F%90%8E-travelers-refuge",
         "shows": "A Minecraft inn and tavern: a common hall with a serving counter and a fireplace, the kitchen and pantry behind it, chambers over, an attached stable of eight stalls under a lofted hay balcony.",
         "terms": "the store's EULA and terms of service (a paid build); ideas only"},
        {"url": "https://en.wikipedia.org/wiki/The_George_Inn,_Southwark",
         "shows": "The last galleried coaching inn in London: a partly timber-framed range of connected bars on the ground floor, the bedrooms in the galleried storey over, a coach yard behind.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
        {"url": "https://en.wikipedia.org/wiki/Coaching_inn",
         "shows": "What a coaching inn holds: attached stables staffed by hostlers who changed a tired team for a fresh one, rooms for travellers over the bars.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    ],
    "node/merchant": [
        {"url": "https://www.shulkr.com/de/schematics/0XY7X8e3YicC",
         "shows": "A Minecraft U-shaped manor: two symmetrical wings round a central courtyard with covered walkways along both sides, dark timber over stone brick, tall gabled roofs with deep eaves.",
         "terms": "none stated on the page (site terms of use linked); ideas only"},
        {"url": "https://en.wikipedia.org/wiki/Medieval_Merchant%27s_House",
         "shows": "Southampton's merchant's house: a shop front on the street, the hall behind it with a side passage, a private inner room at the rear, a wine undercroft, chambers over; stone walls with a timber frontage.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
    ],
    "node/carpenter": [
        {"url": "https://en.wikipedia.org/wiki/Saw_pit",
         "shows": "The pit saw: a log laid across a pit (or on trestles before pits), a top and a bottom sawyer, often in a covered open-fronted shed with a rubble back wall, rubble corner piers and a slate roof.",
         "terms": "CC BY-SA 4.0 (Wikipedia text)"},
        {"url": "https://www.mc-mod.net/?p=538588",
         "shows": "A Minecraft medieval carpenter's house (24 x 22 x 20): stripped spruce framing over stone, spruce slab and trapdoor detailing.",
         "terms": "none stated on the page; ideas only"},
        {"url": "https://minecolonies.com/wiki/buildings/sawmill/",
         "shows": "The carpenter's workplace as a Minecraft colony building: wooden goods made to order from the yard's timber, so the shop takes commissions and the workroom makes them.",
         "terms": "none stated on the page; ideas only"},
    ],
}

# ---------------------------------------------------------------- the square
SQF = 84                     # the square, at the mountain's foot
SQ = (108, 230)
box("node/square", (30, 24), SQF, OPEN(8), "the square",
    "The square at the top of the town, at the mountain's foot: the cathedral's "
    "west front on its east side, the inn on its west, the castle road leaving "
    "north up the mountain and the main street leaving south down to the sea. "
    "Cobbled, with a well at its middle and benches under two trees.",
    pin=SQ)

# ------------------------------------------------------- the main street
# Ten short flights of two, so the street and the plots beside it follow the
# slope in small steps: neighbours differ by two at most.
STREET_W, SEG_L, FLIGHT_L, NFL = 7, 14, 6, 10
# A stretch is wider than its flights: its clear way stays five, centred, and
# the verge either side holds the street's own life (lamps, benches, carts,
# stalls) clear of the lots' fronts. At the guildhall the street widens into
# a market.
STRETCH_W = {k: 9 for k in range(1, NFL)}
# A stretch's own air is four courses over its walk: a lamp, a stall's
# awning; above that the air is the open sky, so a lot's upper storey may
# jetty out over the street's edge.
STREET_AIR = 4
# every stretch: a lot may front the street anywhere along it
AIR_STRETCHES = set(range(1, NFL))
STRETCH_W[4] = 11
segs = []
prev = "node/square"
prev_w = None
floor = SQF
for k in range(1, NFL + 1):
    fl = f"node/flight-{k}"
    floor -= 2
    # a flight below a stretch of four courses' air rises no higher than that
    # stretch's air, so no ring of its own stands over the stretch's edge
    fair = STREET_AIR + 2 if (k - 1) in AIR_STRETCHES else 10
    box(fl, (STREET_W, FLIGHT_L), floor, OPEN(fair), "a flight of the main street",
        f"Flight {k} of the main street: seven wide, two shallow steps down, "
        "between low kerbs.", way={"axis": "z", "clear": 5})
    at = 11 if prev == "node/square" else (prev_w - STREET_W) // 2
    seam(prev, fl, "south", at, 0, "stair", f"flight {k}: two down, the full width")
    if k == NFL:
        break
    sg = f"node/street-{k}"
    w = STRETCH_W[k]
    box(sg, (w, SEG_L), floor, OPEN(STREET_AIR if k in AIR_STRETCHES else 8), "a stretch of the main street",
        f"Stretch {k} of the main street, walk plane {floor}: cobbles with a "
        "kennel, the plots' fronts on both sides" + (", widening into the market before the guildhall." if k == 4 else "."),
        way={"axis": "z", "clear": 5})
    seam(fl, sg, "south", 0, (w - STREET_W) // 2, "contact", "the street runs on at grade")
    segs.append(sg)
    prev, prev_w = sg, w

# the quay at the foot of the street; the basin beyond it is the sea itself
box("node/quay", (60, 10), floor, OPEN(8), "the quay",
    f"The quay at the foot of the street: a long stone wharf at walk plane {floor}, "
    "bollards, stacked crates and nets, the open water of the harbour basin beyond.",
    way={"axis": "x", "clear": 8})
seam(f"node/flight-{NFL}", "node/quay", "south", 0, 27, "contact",
     "the last flight lands on the quay")
QUAYF = floor

# ------------------------------------------------------------- the cathedral
box("node/cathedral", (56, 38), SQF, OPEN(46), "the cathedral",
    "A large cathedral in the manner of Vesperhold's Chapel of Hours: a long "
    "nave running east from a west front on the square, aisles under flying "
    "buttresses, a transept, an apse at the east end and a tall bell tower at "
    "the north-west corner; a walled churchyard on the south side.",
    holds=[
        {"id": "part/church", "kind": "structure", "cells": 1100, "height": 28,
         "use": "the cathedral: nave, aisles, transept and apse, entered by the west door from the square"},
        {"id": "part/tower", "kind": "structure", "cells": 64, "height": 42,
         "reached": False,
         "use": "the bell tower at the north-west corner, its spire over the town"},
        {"id": "part/close", "kind": "ground", "cells": 300,
         "use": "the paved close before the west front, joining the square"},
        {"id": "part/churchyard", "kind": "ground", "cells": 380,
         "use": "the churchyard south of the nave, graves and yews inside a low wall"},
    ])
seam("node/square", "node/cathedral", "east", 0, 14, "contact",
     "the close before the west front opens onto the square")

# ------------------------------------------------------------------- the inn
box("node/inn", (28, 24), SQF, OPEN(16), "the inn",
    "The Bell, a large timber-framed coaching inn on the square's west side: "
    "an L of a taproom and a stable range around a cobbled yard.",
    holds=[
        {"id": "part/inn-house", "kind": "structure", "cells": 200, "height": 12,
         "use": "the inn: a taproom in front, a kitchen behind it, through a door"},
        {"id": "part/stables", "kind": "structure", "cells": 90, "height": 8,
         "use": "the stable range, open-fronted onto the yard"},
        {"id": "part/inn-yard", "kind": "ground", "cells": 160,
         "use": "the inn yard, a trough and a cart"},
    ])
seam("node/square", "node/inn", "west", 0, 0, "contact",
     "the inn's front yard opens onto the square")

# ----------------------------------------------------------- the castle road
# Doune's gate faces north. The road leaves the square northward and climbs
# the mountain's west flank in switchbacks: legs that follow the contour east
# and west, each turning north up a ramp at its end, then runs along the
# castle's north side to Doune's approach (a contact on the north face at 74).
ROAD_W, RAMP_L = 5, 10
CASTLE_WALK = 164            # Doune's grade walk, the castle box's floor: 80 over the square
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


def place_next(prev, node, face, align):
    """Put `node` beside `prev` across `face`, one ring cell apart; `align`
    is 'lo' or 'hi': which end of prev's face the 5-wide road continues at."""
    ax, az, adx, adz, _ = pos[prev]
    (bdx, bdz), bf = ext(node)
    if face in ("north", "south"):
        x = ax if align == "lo" else ax + adx - bdx
        z = az - bdz - 1 if face == "north" else az + adz + 1
    else:
        z = az if align == "lo" else az + adz - bdz
        x = ax - bdx - 1 if face == "west" else ax + adx + 1
    pos[node] = (x, z, bdx, bdz, bf)


def join(a, b, face, kind, form):
    """A seam between two placed boxes, `b` across `a`'s `face`; at/meets read
    off the placement. kind: 'contact', or 'stair' (a is the upper place)."""
    ax, az, adx, adz, _ = pos[a]
    bx, bz, bdx, bdz, _ = pos[b]
    if face in ("north", "south"):
        lo = max(ax, bx); at, meets = lo - ax, lo - bx
        w = min(ax + adx, bx + bdx) - lo
    else:
        lo = max(az, bz); at, meets = lo - az, lo - bz
        w = min(az + adz, bz + bdz) - lo
    eid = "edge/" + a.split("/")[1] + "-to-" + b.split("/")[1]
    s = {"edge": eid, "face": face, "at": at, "meets": meets, "form": form}
    if kind == "contact":
        s["contact"] = {}
        cls = "walk"
    else:
        s["opening"] = {"width": w, "height": 4}
        s["stair_in"] = b
        cls = "stair"
    seams.append(s)
    edges.append({"a": a, "b": b, "class": cls, "id": eid})


CLIMB_RUN = 12
# Four traverses along the contours of the castle hill's west shoulder, each
# climbing twelve, joined by climbs up the slope between them; each traverse
# stands some forty-five cells above the last, so the hillside between two
# legs is a natural slope, never a bank.
ROUTE = [  # (direction of travel, kind, length): kind run (level) or ramp (+4)
    ("north", "run", 4),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("west", "run", 8), ("west", "ramp", RAMP_L), ("west", "run", 8), ("west", "ramp", RAMP_L),
    ("west", "run", 8), ("west", "ramp", RAMP_L), ("west", "run", 8),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("east", "run", 8), ("east", "ramp", RAMP_L), ("east", "run", 8), ("east", "ramp", RAMP_L),
    ("east", "run", 8), ("east", "ramp", RAMP_L), ("east", "run", 8),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("west", "run", 8), ("west", "ramp", RAMP_L), ("west", "run", 8), ("west", "ramp", RAMP_L),
    ("west", "run", 8), ("west", "ramp", RAMP_L), ("west", "run", 8),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("east", "run", 8), ("east", "ramp", RAMP_L), ("east", "run", 8), ("east", "ramp", RAMP_L),
    ("east", "run", 8), ("east", "ramp", RAMP_L), ("east", "run", 8),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
]
prev, prev_dir, floor, rising = "node/square", "north", SQF, False
for k, (d, kind, L) in enumerate(ROUTE, 1):
    node = f"node/road-{k}"
    ext_ = (ROAD_W, L) if d in ("north", "south") else (L, ROAD_W)
    axis = "z" if d in ("north", "south") else "x"
    if kind == "ramp":
        box(node, ext_, floor, OPEN(10), "a ramp of the castle road",
            "A ramp of the castle road: a cobbled stair-road, one step every two "
            "cells, the hillside meeting it on both sides.", way={"axis": axis, "clear": 4})
    else:
        box(node, ext_, floor, OPEN(8), "the castle road",
            "The castle road along the mountain's flank, cobbled and level, the "
            "slope above it and below it running up to its edges.", way={"axis": axis, "clear": 4})
    if prev == "node/square":
        (sx, sz, sdx, sdz, _) = pos[prev]
        pos[node] = (sx + 13, sz - L - 1, ROAD_W, L, floor)
    else:
        # a turn joins at the end of the previous leg the road came along
        align = {"west": "lo", "east": "hi"}.get(prev_dir, "lo") if d == "north" else (
            "lo" if prev_dir == "north" else "lo")
        if d in ("west", "east") and prev_dir == "north":
            align = "lo"            # the turn leaves from the north end of a run up the slope
        place_next(prev, node, d, align)
    if rising:                      # prev was a ramp: node is the upper place
        join(node, prev, OPP[d], "stair", "the ramp climbs to the road")
    else:
        join(prev, node, d, "contact", "the road runs on")
    rising = kind == "ramp"
    if rising:
        floor += 4
        # the place after a ramp stands four higher
    prev, prev_dir = node, d
assert not rising and floor == CASTLE_WALK, floor

box("node/road-top", (10, ROAD_W), CASTLE_WALK, OPEN(8), "the castle road's last stretch",
    "The road's last stretch, level along the castle's north side to the head "
    "of Doune's approach.", way={"axis": "x", "clear": 4})
CASTLE_X0 = 170
rx = pos[prev][0]
L = CASTLE_X0 + 74 + ROAD_W - rx
boxes[-1]["extent"] = [L, ROAD_W]
place_next(prev, "node/road-top", "north", "lo")
join(prev, "node/road-top", "north", "contact", "the road turns east under the castle")
box("node/gate-road", (5, 8), CASTLE_WALK, OPEN(6), "the road onto Doune's approach",
    "The last stretch of the road from the town, arriving on the hilltop at the "
    "start of Doune's own approach road, five wide.", way={"axis": "z", "clear": 5})
place_next("node/road-top", "node/gate-road", "south", "hi")
join("node/road-top", "node/gate-road", "south", "contact",
     "the road turns south onto Doune's approach")
box("node/castle", (102, 118), CASTLE_WALK, OPEN(48), "the castle",
    "Doune Castle, copied whole as one plot: the gatehouse, the hall range, the "
    "kitchen tower, the courtyard, the curtain and the three ditches on the north "
    "approach.")
gx, gz = pos["node/gate-road"][0], pos["node/gate-road"][1]
pos["node/castle"] = (gx - 74, gz + 8 + 1, 102, 118, CASTLE_WALK)
seams.append({"edge": "edge/road-to-gate", "face": "north", "at": 74,
              "contact": {"extent": [5, 6]},
              "form": "Doune's approach road running on, level, onto the hilltop road: five wide, no wall across it"})
edges.append({"a": "node/castle", "b": "node/gate-road", "class": "walk",
              "id": "edge/road-to-gate"})

# --------------------------------------------------------------------- plots
THEMES = {
    "smithy": ("the smithy", "A blacksmith's yard: an open-walled forge shed under a deep roof, the smith's house behind it, a work yard with a quench trough.",
               [("structure", "house", 0.22, 9, "the smith's house: front room, back kitchen"),
                ("structure", "forge", 0.16, 7, "the open-walled forge: anvil, bellows, hearth under a hood"),
                ("ground", "work-yard", 0.22, None, "the work yard, a quench trough and stacked iron")]),
    "bakery": ("the bakery", "A baker's: a shop with a counter in front and the bake room behind it through a door, a domed oven house in the yard.",
               [("structure", "shop", 0.30, 10, "the shop in front and the bake room behind it, joined by a door"),
                ("structure", "oven", 0.06, 5, "a domed bread oven under a lean-to"),
                ("ground", "yard", 0.24, None, "the back yard, a woodpile and flour sacks")]),
    "weaver": ("the weaver's house", "A weaver's tall house with a loom room on the ground floor, a drying yard of cloth on lines and a dye shed.",
               [("structure", "house", 0.30, 12, "the weaver's house: loom room, stair up to the cloth store"),
                ("structure", "dye-shed", 0.08, 6, "an open dye shed with vats"),
                ("ground", "drying-yard", 0.22, None, "the drying yard, cloth hung on lines")]),
    "chandler": ("the chandler's", "A ship chandler's shop with a long store behind it, rope coils and barrels in the yard.",
                 [("structure", "shop", 0.34, 9, "the shop with its counter and the long store behind it through a door"),
                  ("ground", "yard", 0.26, None, "the yard, rope coils, barrels and a handcart")]),
    "cooper": ("the cooper's", "A cooper's workshop, open-fronted, with the family house beside it and barrels stacked in the yard.",
               [("structure", "workshop", 0.18, 7, "the open-fronted cooperage, staves and hoops"),
                ("structure", "house", 0.18, 9, "the cooper's house"),
                ("ground", "yard", 0.24, None, "the barrel yard")]),
    "apothecary": ("the apothecary", "An apothecary's narrow house with a physic garden behind it.",
                   [("structure", "house", 0.30, 11, "the shop with jars and a still room behind it"),
                    ("ground", "garden", 0.30, None, "the physic garden in raised beds")]),
    "merchant": ("the merchant's house", "A rich merchant's U-shaped stone house around a front court, a counting room by the door.",
                 [("structure", "house", 0.48, 13, "the merchant's house: the counting room and the cloth store in the north wing, the hall range"),
                  ("ground", "court", 0.22, None, "the front court with a fountain, walled on the south")]),
    "tavern": ("the tavern", "A low sailors' tavern with a beer garden under a vine pergola.",
               [("structure", "tavern", 0.32, 9, "the taproom and the cellar stair"),
                ("ground", "garden", 0.28, None, "the beer garden under a pergola")]),
    "fishmonger": ("the fishmonger's", "A fishmonger's open stall-front with the smokehouse behind it.",
                   [("structure", "stall", 0.20, 7, "the open stall-front with a slab counter"),
                    ("structure", "smokehouse", 0.12, 8, "the smokehouse"),
                    ("ground", "yard", 0.24, None, "the yard with drying racks")]),
    "netloft": ("the net loft", "A tall net loft over a boat store, nets drying on poles in the yard.",
                [("structure", "loft", 0.30, 12, "the net loft over the boat store"),
                 ("ground", "yard", 0.28, None, "the yard with net poles")]),
    "tannery": ("the tannery", "A tanner's long shed with pits in the yard and the tanner's cottage.",
                [("structure", "shed", 0.20, 7, "the long open shed with hides on racks"),
                 ("structure", "cottage", 0.14, 8, "the tanner's cottage"),
                 ("ground", "pits", 0.24, None, "the yard of tanning pits")]),
    "potter": ("the potter's", "A potter's workshop: the shop where the ware is sold in front, the throwing room behind it through a door, a brick kiln in the yard under a lean-to and the clay pit's heap.",
               [("structure", "workshop", 0.30, 9, "the shop in front and the throwing room behind it, joined by a door"),
                ("structure", "kiln", 0.06, 6, "the bottle kiln under its lean-to", "seen"),
                ("ground", "yard", 0.24, None, "the yard: clay heaps, ware drying on boards")]),
    "carpenter": ("the carpenter's", "A carpenter's workshop and timber yard with a saw pit.",
                  [("structure", "workshop", 0.26, 9, "the workshop and the house over it"),
                   ("ground", "timber-yard", 0.32, None, "the timber yard and the saw pit")]),
    "cottages": ("a pair of cottages", "Two small fishermen's cottages with front gardens and a shared back yard.",
                 [("structure", "cottage-a", 0.16, 8, "the first cottage"),
                  ("structure", "cottage-b", 0.16, 8, "the second cottage"),
                  ("ground", "gardens", 0.26, None, "front gardens and the shared yard")]),
    "boatwright": ("the boatwright's", "A boatwright's shed with a hull on the stocks, open to the lane.",
                   [("structure", "shed", 0.30, 10, "the open boat shed with a hull on the stocks"),
                    ("ground", "yard", 0.28, None, "the yard with timber and a winch")]),
    "townhall": ("the guildhall", "The guildhall: a hall on an open arcade, a clock over the door.",
                 [("structure", "hall", 0.42, 14, "the guildhall over its open arcade"),
                  ("ground", "forecourt", 0.20, None, "the forecourt")]),
    "harbour": ("the harbour", "The harbourmaster's house on the quay's east end, and the fishing boats moored along its edge as fixed builds.",
                [("structure", "harbourmaster", 0.22, 9, "the harbourmaster's house: an office facing the quay, a store behind"),
                 ("structure", "boats", 0.20, 6, "fishing boats moored along the quay's edge, masts and furled sails"),
                 ("ground", "quayside", 0.30, None, "the quayside: bollards, nets, crates")]),
    "lighthouse": ("the lighthouse", "A tall white lighthouse on the headland with the keeper's cottage and a walled yard.",
                   [("structure", "tower", 0.14, 30, "the lighthouse tower, a stair to the lantern room"),
                    ("structure", "cottage", 0.16, 8, "the keeper's cottage"),
                    ("ground", "yard", 0.30, None, "the walled yard and the cliff path")]),
}


# a holding sized by its place's author where the theme's share would not fit
# the room it builds: node -> {part stem: cells}
HOLD_CELLS = {"node/cottages-2": {"cottage-a": 36, "cottage-b": 36}}


def holds_for(theme, dx, dz, node=None):
    area = dx * dz
    out = []
    for kind, pid, share, h, use, *rest in THEMES[theme][2]:
        p = {"id": f"part/{pid}", "kind": kind, "use": use,
             "cells": max(4, int(area * share))}
        if h:
            p["height"] = h
        if rest and rest[0] == "seen":
            p["reached"] = False      # a structure seen and never entered
        if node in HOLD_CELLS and pid in HOLD_CELLS[node]:
            p["cells"] = HOLD_CELLS[node][pid]
        out.append(p)
    return out


# The trades whose fronts stand on the street, by the name their hanging sign
# carries; the street hangs the sign on its own bracket before the doorway
# (street.py marks the cell `sign-<stem>`), and the campaign writes the name.
TRADES = {"node/bakery": "Bakery", "node/apothecary": "Apothecary", "node/merchant": "Merchant",
          "node/weaver": "Weaver", "node/tavern": "Tavern", "node/smithy": "Smithy",
          "node/chandler": "Chandler", "node/fishmonger": "Fishmonger", "node/netloft": "Net Loft"}
SIGNED = []                 # (street, lot), in the order the lots are planned


def plot(name, theme, street, face, at, meets, dx, dz):
    theme = theme.split("-")[0]
    node = f"node/{name}"
    _, f = ext(street)
    intent, note, _ = THEMES[theme]
    box(node, (dx, dz), f, OPEN(16 if theme != "lighthouse" else 44), intent,
        note, holds=holds_for(theme, dx, dz, node))
    if node in FRONTS:
        # the lot fronts the street: its building's front stands on its box
        # edge and the lot meets the street only at its doorway
        zs, w, h, form = FRONTS[node]
        if node in TRADES:
            SIGNED.append((street, node))
        seam(street, node, face, at + zs - 1, meets + zs - 1, "contact", form, span=(w, h))
    else:
        seam(street, node, face, at, meets, "contact",
             f"the plot's front opens onto the street")
    return node


# Lots whose building fronts the street: (first row of the doorway, counted
# from 1 along the lot's street face; its width; its height; what it is).
# Every other cell of such a lot's street edge is its building's front wall
# or its yard wall, four courses high.
FRONTS = {
    "node/bakery": (6, 3, 3, "the bakery's open shop front onto the street"),
    "node/apothecary": (7, 3, 3, "the apothecary's doorway onto the street"),
    "node/weaver": (5, 3, 3, "the weaver's shop doorway onto the street"),
    "node/merchant": (7, 5, 3, "the merchant's court mouth under its arch, onto the street"),
}
# The lower street's lots that are to front it, each span the doorway its
# author builds its front round. Held apart until that front stands: a span
# cut before it leaves the lot's open frontage a crossing no seam allows.
# Set LOWER_FRONTS_READY to the nodes whose fronts stand.
LOWER_FRONTS = {
    "node/tavern": (5, 3, 3, "the tavern's door onto the market"),
    "node/smithy": (3, 4, 3, "the smithy's open forge front onto the street"),
    "node/chandler": (4, 3, 3, "the chandler's shop door onto the street"),
    "node/fishmonger": (3, 5, 3, "the fishmonger's open stall front onto the street"),
    "node/netloft": (4, 3, 3, "the net loft's boat-store doors onto the street"),
}
LOWER_FRONTS_READY = {"node/tavern", "node/smithy", "node/chandler", "node/fishmonger", "node/netloft"}
FRONTS.update({n: v for n, v in LOWER_FRONTS.items() if n in LOWER_FRONTS_READY})


def overlaps(a, b, gap=0):
    ax, az, adx, adz, _ = a
    bx, bz, bdx, bdz, _ = b
    return not (ax + adx + gap <= bx or bx + bdx + gap <= ax or
                az + adz + gap <= bz or bz + bdz + gap <= az)


# two places one cell apart ask to draw one wall (DW0827): any pair not joined
# by a seam keeps two cells between its footprints


# side streets: from street-2 west, street-4 east, street-6 east to the light
SIDE = {("node/street-3", "west"): 40, ("node/street-5", "east"): 40,
        ("node/street-8", "east"): 46}
for (sg, face), L in SIDE.items():
    k = sg.split("-")[1]
    sname = f"node/lane-{k}"
    _, f = ext(sg)
    box(sname, (L, 5), f, OPEN(8), "a side street",
        f"A side street off stretch {k}, cobbled, five wide, plots along it.",
        way={"axis": "x", "clear": 4})
    seam(sg, sname, face, 5, 0, "contact", "the side street leaves the main street")

MAIN = [  # (street, face, theme, dx, dz, at): a plot stays inside its stretch
    ("street-1", "west", "bakery", 22, 12, 1), ("street-1", "east", "apothecary", 18, 12, 1),
    ("street-2", "west", "cottages", 20, 12, 1), ("street-2", "east", "merchant", 26, 12, 1),
    ("street-3", "east", "weaver", 22, 12, 1),
    ("street-4", "west", "townhall", 24, 11, 2), ("street-4", "east", "tavern", 24, 12, 1),
    ("street-5", "west", "smithy", 24, 12, 1),
    ("street-6", "west", "chandler", 20, 10, 2), ("street-6", "east", "cooper", 22, 10, 2),
    ("street-7", "west", "fishmonger", 20, 10, 2), ("street-7", "east", "tannery", 22, 10, 2),
    ("street-8", "west", "netloft", 20, 10, 2),
]
LANE = [  # (lane, face, theme, at, dx, dz)
    ("lane-3", "north", "carpenter", 2, 16, 16), ("lane-3", "south", "potter", 2, 16, 11),
    ("lane-5", "north", "boatwright", 26, 14, 10), ("lane-5", "south", "cottages-2", 26, 14, 10),
]
for st, face, theme, dx, dz, at in MAIN:
    plot(theme, theme, f"node/{st}", face, at, 0, dx, dz)
for ln, face, theme, at, dx, dz in LANE:
    plot(theme, theme.split("-")[0], f"node/{ln}", face, at, 0, dx, dz)
# the cliff path: on from lane 8's east end, then south along the headland's
# spine to the lighthouse on its point, sea west (the harbour basin), east
# (the cove) and south
_, _lf = ext("node/lane-8")
box("node/cliff-path-1", (18, 5), _lf, OPEN(8), "the cliff path",
    "The cliff path leaving the end of lane 8 east toward the headland: trodden earth and rock, a low rail on its seaward side.",
    way={"axis": "x", "clear": 4})
seam("node/lane-8", "node/cliff-path-1", "east", 0, 0, "contact", "the lane runs on as the cliff path")
box("node/cliff-path-2", (5, 41), _lf, OPEN(8), "the cliff path",
    "The cliff path running south along the headland's spine to the lighthouse, the harbour basin below it on the west and the cove on the east.",
    way={"axis": "z", "clear": 4})
seam("node/cliff-path-1", "node/cliff-path-2", "south", 13, 0, "contact", "the path turns south onto the headland")
plot("lighthouse", "lighthouse", "node/cliff-path-2", "south", 0, 1, 20, 20)
# the harbour plot on the quay's east side, at the quay's floor; its south
# rows stand over the basin's water, so boats moor alongside its quay edge
plot("harbour", "harbour", "node/quay", "east", 0, 2, 24, 22)   # its last six rows over the basin

# ---------------------------------------------------------- consistency check
names = list(pos)
bad = []
for i, a in enumerate(names):
    for b in names[i + 1:]:
        joined = any({e["a"], e["b"]} == {a, b} for e in edges)
        if overlaps(pos[a], pos[b], 0 if joined else 2):
            bad.append((a, b))
for a, b in bad:
    print("OVERLAP", a, pos[a], b, pos[b], file=sys.stderr)
for n, (x, z, dx, dz, f) in pos.items():
    if x < 1 or z < 1 or x + dx > RX - 1 or z + dz > RZ - 1:
        print("OUTSIDE", n, pos[n], file=sys.stderr)
if bad:
    sys.exit(1)

# ------------------------------------------------------------------- terrain

# The world goes on past the island. The walk region is every box grown by the
# boundary's margin; from any cell in it a player sees as far as the server's
# view distance serves (ten chunks, plus the chunk the player stands in), so the
# region reaches that far past the walk region on every side and the land and
# sea run on to it. Nothing out there is reachable: the boundary returns a
# player at the walk region's edge.
MARGIN = 8                 # world.json boundary.margin
SEEN = 176                 # the view distance's reach, chunk-rounded: 16 * (10 + 1)
WALK = (min(p[0] for p in pos.values()) - MARGIN, max(p[0] + p[2] - 1 for p in pos.values()) + MARGIN,
        min(p[1] for p in pos.values()) - MARGIN, max(p[1] + p[3] - 1 for p in pos.values()) + MARGIN)
GX0, GZ0 = min(0, WALK[0] - SEEN), min(0, WALK[2] - SEEN)            # the region's corner
GX = max(RX, WALK[1] + SEEN + 1) - GX0                               # the region's footprint
GZ = max(RZ, WALK[3] + SEEN + 1) - GZ0


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def hash2(ix, iz, s):
    h = (ix * 374761393 + iz * 668265263 + s * 2147483647) & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


def vnoise(x, z, scale, s):
    gx, gz = x / scale, z / scale
    ix, iz = math.floor(gx), math.floor(gz)
    fx, fz = smooth(gx - ix), smooth(gz - iz)
    a = hash2(ix, iz, s); b = hash2(ix + 1, iz, s)
    c = hash2(ix, iz + 1, s); d = hash2(ix + 1, iz + 1, s)
    return (a + (b - a) * fx) * (1 - fz) + (c + (d - c) * fx) * fz


def ellipse(x, z, cx, cz, rx, rz):
    return math.hypot((x - cx) / rx, (z - cz) / rz)


def rounded_rect(x, z, x0, x1, z0, z1, r):
    """A normalised distance: < 1 inside a rectangle with corners rounded by r."""
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    hx, hz = (x1 - x0) / 2, (z1 - z0) / 2
    qx, qz = abs(x - cx) - (hx - r), abs(z - cz) - (hz - r)
    out = math.hypot(max(qx, 0), max(qz, 0)) + min(max(qx, qz), 0)
    return 1 + out / r


# The island: one land mass. The mountain rises behind the town with Doune
# near its summit; its broad lower slope falls south to an irregular coast of
# coves, rock and beach, and the town lies on that slope down to the harbour.
TOWN = (60, 216, 210, 500)     # the town's ground: x0, x1, z0, z1
TOWN_EAST = 184                # east of it the headland: wild rock, no brick, no lawn
CX, CZ = pos["node/castle"][0] + 51, pos["node/castle"][1] + 59   # Doune's centre


def fbm(x, z, scale, octaves, salt):
    v, amp, tot = 0.0, 1.0, 0.0
    for o in range(octaves):
        v += amp * vnoise(x, z, scale / (2 ** o), salt + o)
        tot += amp
        amp *= 0.5
    return v / tot


def ridged(x, z, scale, octaves, salt):
    v, amp, tot = 0.0, 1.0, 0.0
    for o in range(octaves):
        n = 1 - abs(vnoise(x, z, scale / (2 ** o), salt + o) * 2 - 1)
        v += amp * n * n
        tot += amp
        amp *= 0.5
    return v / tot


def coast_z(x):
    """The south coast's line: coves and points; the harbour inlet at the
    quay; a deep cove east of the lighthouse so it stands on its point."""
    z = 492 + (fbm(x, 0, 38, 3, 31) - 0.5) * 60
    z -= 30 * smooth(1 - abs(x - 122) / 40)          # the harbour inlet
    z -= 22 * smooth(1 - abs(x - 166) / 30)          # the basin the harbour plot moors its boats in
    z -= 66 * smooth(1 - abs(x - 222) / 22)          # the cove east of the lighthouse's headland
    z -= 48 * smooth(1 - abs(x - 38) / 30)           # a western cove
    return z


# North of the neck the island is the mainland's: there is no north coast, and
# the west and east coasts open out as they run north, so the land goes on
# toward a mainland on the far side and the sea runs to the horizon elsewhere.
Z_NECK = 40                # south of this row the island's frame is unchanged


def shores(z):
    """The west and east coast frame at row z: the island's frame south of the
    neck, opening out north of it."""
    k = max(0.0, Z_NECK - z)
    k = 0.9 * k + 0.004 * k * k
    return -k, RX - 1 + k


def mainland(x, z):
    """The mainland's hills behind the mountain: rising north to a range."""
    t = smooth((Z_NECK - 30 - z) / 150)
    r = ridged(x, z, 80, 4, 91)
    return min(198.0, 58 + t * (30 + 110 * r) + (fbm(x, z, 30, 3, 93) - 0.5) * 12)


# East and west the land runs on past the walk region and falls to the sea
# over LAND_FALL blocks, so from the walk region's edge the ground drops away
# in front of the player and the sea shows beyond it, rather than a cliff top
# against the sky; the coast frame stands COAST_OUT past the walk region.
COAST_OUT, LAND_FALL = 70, 55


def land_fall(z, side):
    """How far past the walk region the land runs before it is under the sea,
    along the east (side 1) or west (side 0) coast at row z: long where a
    headland runs out, short in a cove, never under FALL_MIN, so the shore
    stays clear of every box and its ring."""
    v = fbm(side * 997, z, 70, 3, 101 + side)          # the coast's long swing
    k = ridged(side * 991, z, 45, 2, 105 + side)       # a headland's point
    return FALL_MIN + (FALL_MAX - FALL_MIN) * smooth(v * 1.3 - 0.15) + 28 * k * k


FALL_MIN, FALL_MAX = 28, 96


def coast(z):
    """The coast frame at row z: the island's frame grown past the walk region
    east and west, as far as the land runs there, opening out north of the
    neck as the island's does."""
    lo, hi = shores(z)
    return (min(lo, WALK[0] - land_fall(z, 0) - 15), max(hi, WALK[1] + land_fall(z, 1) + 15))


def offshore(x, z):
    """How far a column lies out to sea past the island's coast or the
    mainland's; 0 inside them."""
    lo, hi = coast(z)
    return max(lo + 25 - x, x - (hi - 25), z - (RZ - 1), 0.0)


def land(x, z):
    """1 on land, 0 at sea; the south coast slopes gently to beaches."""
    wob = (fbm(x, z, 40, 3, 1) - 0.5) * 30
    lo, hi = shores(z)
    inset = min(x - lo, hi - x) + wob
    edge = smooth((inset - 10) / 14)                 # cliffs on the far coasts
    south = smooth((coast_z(x) - z + wob * 0.3) / 18)  # a gentle shore by the town
    return min(edge, south)


def mountain(x, z):
    """One mountain at the town's foot: its lower slope starts at the town's
    upper edge and rises along the castle road's shoulder to the summit
    plateau Doune stands on, the summit itself north-east of Doune; domain
    warped, ridged and broken into uneven ledges, so nothing is a cone."""
    wx = x + (fbm(x, z, 60, 2, 41) - 0.5) * 40
    wz = z + (fbm(x, z, 60, 2, 43) - 0.5) * 30
    top = SQ[1] - 18                                  # the town's upper edge
    # the shoulder the road climbs: rising north from the town's edge
    shoulder = 84 + 0.40 * (top - wz)               # falls away south of the town's edge too
    # the plateau round Doune, falling away on every side
    # south of Doune the ground falls evenly from its ring to the square's
    # level (about one in one, so grass and trees hold, not a cliff); north
    # it rounds off over the summit plateau
    if wz > CZ:
        d = math.hypot((wx - CX) / 150, (wz - CZ) / 105)
        t = max(0.0, min(1.0, (d - 0.56) / 0.67))
        plateau = 84 + (CASTLE_WALK - 84) * (1 - t) - 34 * max(0.0, d - 1.23)
    else:
        d = math.hypot((wx - CX) / 150, (wz - CZ) / 150)
        plateau = 50 + (CASTLE_WALK - 50) * (1 - smooth((d - 0.60) / 0.95))
    # the summit, north-east of Doune
    p = math.hypot((wx - (CX + 40)) / 80, (wz - (CZ - 55)) / 70)
    summit = CASTLE_WALK - 20 + 56 * (1 - smooth(p)) ** 1.3
    h = max(min(shoulder, CASTLE_WALK - 2), plateau, summit if p < 1 else 0)
    # fade the mountain into the island's low country east and west
    lo, hi = shores(z)
    fade = smooth((x - lo - 8) / 40) * smooth((hi + 1 - 8 - x) / 40)
    h = 50 + (h - 50) * fade
    # uneven ledges and broken rock, strongest where the ground is high
    up = smooth((h - 90) / 40)
    h += (ridged(x, z, 18, 3, 47) - 0.45) * 12 * up + (vnoise(x, z, 5, 49) - 0.5) * 3.5 * up
    hills = (12 + (fbm(x, z, 44, 3, 53) - 0.35) * 30) * smooth((300 - z) / 60) * (1 - up)
    return h + hills


def slope(x, z):
    """The mountain's lower slope under the town: the street's own fall."""
    z0, z1 = SQ[1] + 12, pos['node/quay'][1]
    y = SQF - (SQF - QUAYF) * (max(z, z0) - z0) / (z1 - z0) - 10 * smooth((z0 - z) / 80)
    return y + (fbm(x, z, 33, 2, 7) - 0.5) * 3


def base_height(x, z):
    """The land: the soft maximum of the mountain and its lower slope, cut by
    the shore so the waterline follows the coast's coves and points, falling
    to the sea floor; cliffs only on the far coasts."""
    wob = (fbm(x, z, 40, 3, 1) - 0.5) * 30
    lo, hi = coast(z)
    inset = min(x - lo, hi - x) + wob
    edge = smooth((inset - 10) / 14)
    h_m, h_s = mountain(x, z), max(slope(x, z), 64.5)
    k = 6.0                                          # a soft maximum: no crease
    h = k * math.log(math.exp(h_m / k) + math.exp(h_s / k))
    if z < Z_NECK:
        # behind the summit the mountain falls to a saddle, and past it the
        # mainland's hills rise to a range
        fall = smooth(1 - (Z_NECK - z) / 110)
        h = min(h, 66 + (h - 66) * fall)
        h = max(h, mainland(x, z))
    # past the walk region east and west the land falls to the sea; north of
    # the neck the mainland goes on
    out = max(WALK[0] - x, x - WALK[1], 0)
    if out > 0:
        lf = land_fall(z, 1 if x > WALK[1] else 0)
        drop = smooth(out / lf) * smooth((z - (Z_NECK - 80)) / 40)
        h -= (h - 58) * drop
    shore = 62.5 + 0.35 * (coast_z(x) + wob * 0.3 - z)   # a beach rising from the waterline
    # the seabed: as it was inside the frame, falling away out to sea
    sea_floor = max(41.0, 50 + (vnoise(x, z, 31, 4) - 0.5) * 4 - 9 * smooth(offshore(x, z) / 80))
    h = max(sea_floor, min(h, shore))
    return sea_floor + (h - sea_floor) * edge


# H[z - GZ0][x - GX0] is column (x, z); every loop below reads world x, z
H = [[base_height(x, z) for x in range(GX0, GX0 + GX)] for z in range(GZ0, GZ0 + GZ)]

# each box: its columns at floor - 1; the ground eases to the natural ground
# over a skirt. Doune's plot: inside the ring its ditch floor (walk - 4), the
# ring at its surface course (walk - 1), flat, then the summit's own rock.
rects = [(n, *pos[n]) for n in pos]
HARBOUR_WATER = 6           # rows of the harbour plot over water, and its depth
W = [[0.0] * GX for _ in range(GZ)]
T = [[0.0] * GX for _ in range(GZ)]
for n, x0, z0, dx, dz, f in rects:
    castle = n == "node/castle"
    road = n.startswith("node/road") or n == "node/gate-road"
    skirt = 1 if castle else (12 if road else (3 if n in ("node/quay", "node/lighthouse") else 12))
    for z in range(max(GZ0, z0 - 1 - skirt), min(GZ0 + GZ, z0 + dz + 1 + skirt)):
        for x in range(max(GX0, x0 - 1 - skirt), min(GX0 + GX, x0 + dx + 1 + skirt)):
            ddx = max(x0 - x, 0, x - (x0 + dx - 1))
            ddz = max(z0 - z, 0, z - (z0 + dz - 1))
            d = math.hypot(ddx, ddz)
            if castle:
                if d == 0:
                    target, w = f - 4, 1.0
                elif max(ddx, ddz) <= 1:
                    target, w = f - 1, 1.0
                else:
                    target, w = f - 1, smooth(1 - (d - 1) / skirt)
            else:
                # the footprint and its ring lie at the floor course, so the
                # ground meets the next place level across the seam
                target = f - 1
                w = 1.0 if max(ddx, ddz) <= 1 else smooth(1 - (d - 1) / skirt)
            if n == "node/harbour" and z >= z0 + dz - HARBOUR_WATER:
                # the harbour's south rows stand over the basin: sea floor,
                # HARBOUR_WATER deep at sea level, easing into the sea beyond
                target = SEA - HARBOUR_WATER
            gz, gx = z - GZ0, x - GX0
            if w > W[gz][gx] + 1e-9 or (abs(w - W[gz][gx]) < 1e-9 and target > T[gz][gx]):
                W[gz][gx] = w
                T[gz][gx] = target
for gz in range(GZ):
    for gx in range(GX):
        w = W[gz][gx]
        if w > 0:
            H[gz][gx] = H[gz][gx] * (1 - w) + T[gz][gx] * w

# Doune stands on the summit, not on a table: past its ring a lawn of a few
# cells, then the ground goes to the mountain's own in steps of rock, three
# courses each, the bank's edge wandering so no side of it is straight. The
# bank holds the ground to within its slope of the ring's course, up or down,
# and touches only ground no other place shapes; past where the mountain
# already lies within the bank it leaves the ground alone.
BANK_LAWN, BANK_SLOPE, BANK_LEDGE, BANK_REACH = 3, 1.3, 3, 90
BANK_TOUCHED = []          # skirt cells of another place the bank moved: (x, z, was, now)
_cx, _cz, _cdx, _cdz, _cf = pos["node/castle"]
# the terrace between the road's last stretch and the north wall stays level
_trx, _trz, _trdx, _trdz, _ = pos["node/road-top"]
_tx0, _tx1, _tz0, _tz1 = min(_trx, _cx) - 2, _cx + _cdx + 15, _trz + _trdz + 1, _cz - 2
for z in range(max(GZ0, _cz - 1 - BANK_REACH), min(GZ0 + GZ, _cz + _cdz + 1 + BANK_REACH)):
    for x in range(max(GX0, _cx - 1 - BANK_REACH), min(GX0 + GX, _cx + _cdx + 1 + BANK_REACH)):
        gz, gx = z - GZ0, x - GX0
        if W[gz][gx] >= 1.0:
            continue
        if _tx0 <= x <= _tx1 and _tz0 <= z <= _tz1:
            H[gz][gx] = _cf - 1             # the terrace under the north wall: level
            continue
        ddx = max(0, (_cx - 1) - x, x - (_cx + _cdx))
        ddz = max(0, (_cz - 1) - z, z - (_cz + _cdz))
        d = math.hypot(ddx, ddz) + (fbm(x, z, 26, 3, 111) - 0.5) * 26
        run = max(0.0, d - BANK_LAWN)
        step = BANK_LEDGE * math.floor(run * BANK_SLOPE / BANK_LEDGE + vnoise(x, z, 7, 113) * 0.6)
        lo, hi = (_cf - 1) - step, (_cf - 1) + step
        was = H[gz][gx]
        # in another place's skirt the bank only lowers: it never lifts the
        # ground a neighbour eases toward its own floor
        H[gz][gx] = min(was if W[gz][gx] > 0 else max(was, lo), hi)
        if W[gz][gx] > 0 and H[gz][gx] != was:
            BANK_TOUCHED.append((x, z, round(was), round(H[gz][gx])))

# Behind the cathedral (north) and past its apse (east) the mountain's lower
# terrace stands some thirty above the cathedral's floor. The ground falls from
# that terrace to the cathedral's ring as a hillside, never a bank: there the
# ground is capped by a slope rising from the ring course, one in one at its
# foot and steepening gently (BACK_BEND) until it meets the natural ground,
# which then runs on up to Doune untouched. The cap only lowers ground, and
# never inside another box's footprint or ring. West (the square and the
# castle road) and south (the town) keep their own shaping.
BACK_RISE, BACK_BEND, BACK_REACH, BACK_WEST = 1.0, 0.02, 44, 12
_bx, _bz, _bdx, _bdz, _bf = pos["node/cathedral"]
for z in range(max(GZ0, _bz - 1 - BACK_REACH), min(GZ0 + GZ, _bz + _bdz + 1 + BACK_REACH)):
    for x in range(_bx - BACK_WEST, min(GX0 + GX, _bx + _bdx + 1 + BACK_REACH)):
        ddw = max(0, (_bx - 1) - x)               # past the west ring: eased out
        ddx = max(0, x - (_bx + _bdx))            # past the east ring
        ddz = max(0, (_bz - 1) - z, z - (_bz + _bdz))
        if ddx == 0 and ddz == 0 or W[z - GZ0][x - GX0] >= 1.0:
            continue
        if z > _bz + _bdz and ddx == 0:
            continue                               # south of the cathedral: the town's
        d = math.hypot(ddx, ddz)
        cap = (_bf - 1) + BACK_RISE * d + BACK_BEND * d * d \
            + (vnoise(x, z, 6, 61) - 0.5) * 2.0 + 1.5 * ddw
        if H[z - GZ0][x - GX0] > cap:
            H[z - GZ0][x - GX0] = cap

# The inn backs onto the same slope: north of it (the mountain) and west of it
# the ground rose over a short skirt to a bank. It eases the same way,
# one in two at the inn's ring and steepening until it meets the natural ground; the
# square and the castle road east of it, and the street south, keep theirs.
_ix, _iz, _idx, _idz, _if = pos["node/inn"]
INN_RISE, INN_BEND = 0.6, 0.03    # gentler than the cathedral's: a lawn rising behind the yard
for z in range(max(GZ0, _iz - 1 - BACK_REACH), _iz + _idz + 1):
    for x in range(max(GX0, _ix - 1 - BACK_REACH), _ix + _idx + 1):
        ddw = max(0, (_ix - 1) - x)
        ddz = max(0, (_iz - 1) - z)
        if (ddw == 0 and ddz == 0) or W[z - GZ0][x - GX0] >= 1.0:
            continue
        d = math.hypot(ddw, ddz)
        cap = (_if - 1) + INN_RISE * d + INN_BEND * d * d + (vnoise(x, z, 6, 67) - 0.5) * 1.0
        if H[z - GZ0][x - GX0] > cap:
            H[z - GZ0][x - GX0] = cap

# The lighthouse's point falls to the sea as rock: west, south and east of its
# plot the ground drops in ledges, three or four a course, to the sea floor,
# steep enough that it weathers as the wild's stone, andesite and tuff, with
# the plot's own turf on top. The cliff path arrives from the north.
_lx, _lz, _ldx, _ldz, _lf = pos["node/lighthouse"]
for z in range(_lz - 1, min(GZ0 + GZ, _lz + _ldz + 1 + 14)):
    for x in range(max(GX0, _lx - 1 - 14), min(GX0 + GX, _lx + _ldx + 1 + 14)):
        ddx = max(0, (_lx - 1) - x, x - (_lx + _ldx))
        ddz = max(0, z - (_lz + _ldz))
        if (ddx == 0 and ddz == 0) or W[z - GZ0][x - GX0] >= 1.0:
            continue
        d = math.hypot(ddx, ddz)
        ledge = math.floor(d / 1.6) * 4 + (vnoise(x, z, 4, 71) - 0.5) * 3
        cap = (_lf - 1) - ledge
        if H[z - GZ0][x - GX0] > cap:
            H[z - GZ0][x - GX0] = max(cap, 50.0)

# No pit a body cannot climb out of: a priority flood from the sea and the
# region's rim raises every column to at least one under the column it is
# reached from, so from anywhere a walk of steps no higher than one leads to
# the shore. Cliffs stay: only hollows are filled.
import heapq
Q = [[int(round(H[z][x])) for x in range(GX)] for z in range(GZ)]
seen = [[False] * GX for _ in range(GZ)]
heap = []
for z in range(GZ):
    for x in range(GX):
        if Q[z][x] < SEA + 1 or x in (0, GX - 1) or z in (0, GZ - 1):
            seen[z][x] = True
            heapq.heappush(heap, (Q[z][x], x, z))
while heap:
    h, x, z = heapq.heappop(heap)
    for nx, nz in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
        if 0 <= nx < GX and 0 <= nz < GZ and not seen[nz][nx]:
            seen[nz][nx] = True
            if Q[nz][nx] < h - 1:
                Q[nz][nx] = h - 1
            heapq.heappush(heap, (Q[nz][nx], nx, nz))
H = [[float(Q[z][x]) for x in range(GX)] for z in range(GZ)]

pix = bytearray()
for z in range(GZ):
    pix.append(0)
    for x in range(GX):
        v = round((H[z][x] - BASE_Y) * 255 / RANGE)
        # y = BASE_Y + v * RANGE // 255 must land on the intended course
        want = int(round(H[z][x]))
        v = max(0, min(255, v))
        while v < 255 and BASE_Y + v * RANGE // 255 < want:
            v += 1
        while v > 0 and BASE_Y + v * RANGE // 255 > want:
            v -= 1
        pix.append(v)


def png(path, w, h, raw):
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n")
        fh.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0)))
        fh.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        fh.write(chunk(b"IEND", b""))


os.makedirs(os.path.join(ROOT, "terrain"), exist_ok=True)
png(os.path.join(ROOT, "terrain", "island.png"), GX, GZ, pix)

# ----------------------------------------------------------------- documents


TOWN_AREA = {"min": [TOWN[0], TOWN[2]], "max": [TOWN_EAST, TOWN[3]]}
BRICK_AREA = {"min": [TOWN[0], SQ[1] + 24], "max": [TOWN_EAST, TOWN[3]]}   # below the square: the mountain never takes a brick
_cx, _cz, _cdx, _cdz, _ = pos["node/castle"]
CASTLE_AREA = {"min": [_cx - 1, _cz - 1], "max": [_cx + _cdx, _cz + _cdz]}
P = lambda scale, mn, salt: {"scale": scale, "min": mn, "salt": salt}
# the terrace under Doune's north wall, between the castle road's last stretch
# and the castle's ring: level ground at the walk's grade, turfed, so from the
# wall it reads as a kept terrace, not a bare strip
_rx, _rz, _rdx, _rdz, _ = pos["node/road-top"]
TERRACE = {"min": [min(_rx, _cx) - 2, _rz + _rdz + 1], "max": [_cx + _cdx + 15, _cz - 2]}
_hx, _hz, _hdx, _hdz, _ = pos["node/lighthouse"]
HEADLAND = {"min": [max(_hx - 14, pos["node/harbour"][0] + pos["node/harbour"][2] + 2), _hz - 1],
            "max": [_hx + _hdx + 14, _hz + _hdz + 14]}
STRATA = [
    # the lighthouse's point: rock ledges to the water, never sand or brick
    {"when": {"area": HEADLAND, "steep": 3, "patch": P(4, 520, 81)}, "surface": "minecraft:andesite", "below": "minecraft:stone"},
    {"when": {"area": HEADLAND, "steep": 3, "patch": P(5, 540, 82)}, "surface": "minecraft:tuff", "below": "minecraft:stone"},
    {"when": {"area": HEADLAND, "steep": 3}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"area": HEADLAND, "y_max": 64, "patch": P(4, 560, 83)}, "surface": "minecraft:andesite", "below": "minecraft:stone"},
    {"when": {"area": HEADLAND, "y_max": 64}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    # the sea floor and the shore
    {"when": {"y_max": 56}, "surface": "minecraft:gravel", "below": "minecraft:stone"},
    {"when": {"y_max": 63}, "surface": "minecraft:sand", "below": "minecraft:sandstone"},
    # Doune's plot and its ring: Doune's own turf, which its plants stand on
    {"when": {"area": CASTLE_AREA}, "surface": "minecraft:grass_block", "below": "minecraft:dirt"},
    {"when": {"area": TERRACE}, "surface": "minecraft:grass_block", "below": "minecraft:dirt"},
    # the town: a step of two or more is a retaining wall a builder laid
    {"when": {"area": BRICK_AREA, "steep": 3, "patch": P(9, 600, 11)},
     "surface": "minecraft:mossy_stone_bricks", "below": "minecraft:mossy_stone_bricks"},
    {"when": {"area": BRICK_AREA, "steep": 3},
     "surface": "minecraft:stone_bricks", "below": "minecraft:stone_bricks"},
    {"when": {"area": TOWN_AREA, "patch": P(7, 780, 12)},
     "surface": "minecraft:coarse_dirt", "below": "minecraft:dirt"},
    {"when": {"area": TOWN_AREA}, "surface": "minecraft:grass_block", "below": "minecraft:dirt"},
    # the wild: rock as it weathers, never one smooth face. A real cliff only
    # where it is very steep; elsewhere stone, andesite, tuff and moss broken
    # by grass in the cracks, and scree high up.
    {"when": {"steep": 5, "patch": P(4, 520, 21)}, "surface": "minecraft:andesite", "below": "minecraft:andesite"},
    {"when": {"steep": 5, "patch": P(5, 560, 30)}, "surface": "minecraft:tuff", "below": "minecraft:stone"},
    {"when": {"steep": 5}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"steep": 3, "patch": P(3, 620, 31)}, "surface": "minecraft:moss_block", "below": "minecraft:stone"},
    {"when": {"steep": 3, "patch": P(4, 540, 32)}, "surface": "minecraft:grass_block", "below": "minecraft:dirt"},
    {"when": {"steep": 3, "patch": P(3, 500, 33)}, "surface": "minecraft:andesite", "below": "minecraft:stone"},
    {"when": {"steep": 3, "patch": P(4, 520, 34)}, "surface": "minecraft:tuff", "below": "minecraft:stone"},
    {"when": {"steep": 3}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"y_min": 178, "patch": P(5, 520, 35)}, "surface": "minecraft:gravel", "below": "minecraft:stone"},
    {"when": {"y_min": 178, "patch": P(4, 600, 36)}, "surface": "minecraft:moss_block", "below": "minecraft:stone"},
    {"when": {"y_min": 178}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    # outcrops breaking the slopes: small patches, mixed
    {"when": {"y_min": 100, "patch": P(7, 780, 28)}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"y_min": 95, "patch": P(6, 800, 29)}, "surface": "minecraft:andesite", "below": "minecraft:stone"},
    {"when": {"y_min": 110, "patch": P(5, 820, 37)}, "surface": "minecraft:mossy_cobblestone", "below": "minecraft:stone"},
    {"when": {"y_min": 92, "y_max": 176, "patch": P(30, 400, 23)},
     "surface": "minecraft:podzol", "below": "minecraft:dirt",
     "trees": {"per_mille": 70, "log": "minecraft:spruce_log",
               "leaves": "minecraft:spruce_leaves[persistent=true]", "height": [6, 9]}},
    {"when": {"y_min": 66, "y_max": 104, "patch": P(26, 470, 24)},
     "surface": "minecraft:grass_block", "below": "minecraft:dirt",
     "trees": {"per_mille": 55, "log": "minecraft:oak_log",
               "leaves": "minecraft:oak_leaves[persistent=true]", "height": [5, 7]}},
    {"when": {"y_min": 66, "patch": P(22, 620, 25)},
     "surface": "minecraft:grass_block", "below": "minecraft:dirt",
     "trees": {"per_mille": 30, "log": "minecraft:birch_log",
               "leaves": "minecraft:birch_leaves[persistent=true]", "height": [5, 7]}},
    {"when": {"patch": P(6, 800, 26)}, "surface": "minecraft:coarse_dirt", "below": "minecraft:dirt"},
]


def write(name, stage, content):
    doc = {"campaign_id": CAMPAIGN, "content": content, "dsl_version": DSL,
           "stage": stage}
    with open(os.path.join(ROOT, name), "w") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")


# each sign is a station of the street it hangs over, and a `signs` entry
# writes its trade's name, front and back
SIGNS = []
for street, lot in sorted(SIGNED, key=lambda sl: list(TRADES).index(sl[1])):
    stem = lot.removeprefix("node/")
    sn = next(n for n in nodes if n["id"] == street)
    sn.setdefault("stations", []).append({
        "anchor": f"anchor/sign-{stem}", "kind": "point",
        "note": f"the {TRADES[lot].lower()}'s hanging sign, on the street's bracket before its doorway"})
    SIGNS.append({"anchor": f"anchor/sign-{stem}", "back": ["", TRADES[lot]], "front": ["", TRADES[lot]],
                  "id": f"sign/{stem}"})

main_path = ["node/square"]
for k in range(1, NFL + 1):
    main_path.append(f"node/flight-{k}")
    if k < NFL:
        main_path.append(f"node/street-{k}")
main_path.append("node/quay")

write("world.json", "world", {
    "areas": [],
    "boundary": {"margin": 8},
    "test_level": True,
    "horizon": {"attributes": {"audio/background_music": {}}, "base": "ocean"},
    "premise": "The party arrives on the square at the foot of the mountain and walks the main street down through the town to the harbour.",
    "seed": 20261028,
    "target_minutes": 20,
    "theme": "A harbour town on the slope below a castle mountain: one main street from the cathedral square down to the quays, side streets off it, a lighthouse on the headland.",
    "time": "noon",
    "title": "The Town at the Foot of the Mountain",
    "weather": "clear",
})
write("layout-graph.json", "layout-graph", {
    "beats": [{"node": "node/quay", "objective": "obj/reach-the-quay",
               "quest": "quest/down-to-the-harbour"}],
    "critical_path": main_path,
    "edges": edges,
    "entry": "node/square",
    "goal": "node/quay",
    "nodes": nodes,
})
write("site-plan.json", "site-plan", {
    "boxes": boxes,
    "datums": [],
    "fill": {"below": "minecraft:dirt", "kind": "open",
             "surface": "minecraft:grass_block", "strata": STRATA,
             "terrain": {"base_y": BASE_Y, "heightmap": "terrain/island.png",
                         "kind": "heightmap", "range": RANGE}},
    "identities": [
        {"cmp": "eq", "fact": "fact/region-span", "measure": {"axis": "x", "of": "region-extent"}},
        {"cmp": "eq", "fact": "fact/region-depth", "measure": {"axis": "z", "of": "region-extent"}},
    ],
    "region": {"extent": [GX, RYN, GZ], "min": [GX0, RY0, GZ0]},
    "seams": seams,
    "views": [],
    "volumes": [],
})
write("geometry-brief.json", "geometry-brief", {"facts": [
    {"id": "fact/region-span", "note": "The region east to west.", "unit": "blocks", "value": float(GX)},
    {"id": "fact/region-depth", "note": "The region north to south.", "unit": "blocks", "value": float(GZ)},
]})
write("quest-plan.json", "quest-plan", {
    "finale": "quest/down-to-the-harbour",
    "quests": [{"act": 1, "area": "area/site", "depends_on": [],
                "goal": "Walk the town from the square down to the harbour.",
                "id": "quest/down-to-the-harbour", "mandatory": True, "npcs": []}],
})
write("quests.json", "quests", {
    # the town's barrels and cupboards are its people's, scenery the player
    # looks at: every container no fill and no device claims is decoration
    "containers": {"decoration_notice": {
        "style": "chat",
        "text": "The barrels, crates and cupboards of the town hold their owners' goods: look all you like, but they are not yours to open."}},
    "quests": [{
    "happening": {"text": "You stand on the square at the foot of the mountain, the cathedral on one side and the inn on the other.", "verb": "arrives"},
    "id": "quest/down-to-the-harbour",
    "objectives": [{
        "anchor": "anchor/node-quay",
        "happening": {"text": "You reach the quay at the foot of the street.", "verb": "arrives"},
        "hint": "Down the main street from the square, past the side streets, to the stone quay at the harbour.",
        "id": "obj/reach-the-quay", "radius": 1, "title": "Go down to the harbour",
        "type": "reach-anchor"}],
    "on_complete": [{"happening": {"text": "The town is walked, square to harbour.", "verb": "departs"}, "type": "campaign-complete"}],
    "trigger": {"type": "campaign-start"},
}], "signs": SIGNS})

print(f"boxes {len(boxes)}  seams {len(seams)}  plots {sum(1 for n in nodes if 'holds' in n)}")
for n in ("node/square", "node/castle", "node/quay", "node/cathedral", "node/lighthouse"):
    print(n, pos[n])
if os.environ.get("POS_OUT"):
    with open(os.environ["POS_OUT"], "w") as fh:
        json.dump(pos, fh)
