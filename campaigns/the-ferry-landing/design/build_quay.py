#!/usr/bin/env python3
"""Write world-edits.json for The Ferry Landing.

Every block of the quay comes from this script's edit script; nothing is
hand-placed in a world. Coordinates below are world coordinates; the script
turns them into boxes relative to `anchor/node-landing`, which the site plan
derives at (8207, 64, 8191).

    python3 campaigns/the-ferry-landing/design/build_quay.py

The places (site-plan.json):
  landing stage  x 8200..8215, z 8188..8195, walk y 64 (deck block y 63)
  quay top       x 8200..8215, z 8197..8204, walk y 68 (paving y 67)
  quay wall face z 8196, y 63..67, between them
"""
import json
import pathlib

ANCHOR = (8207, 64, 8191)
FRAME = {"anchor": "anchor/node-landing", "kind": "anchor-relative"}

STONE = [
    {"block": "minecraft:stone_bricks", "weight": 6},
    {"block": "minecraft:mossy_stone_bricks", "weight": 2},
    {"block": "minecraft:cracked_stone_bricks", "weight": 1},
]
WET_STONE = [
    {"block": "minecraft:mossy_stone_bricks", "weight": 3},
    {"block": "minecraft:stone_bricks", "weight": 2},
    {"block": "minecraft:mossy_cobblestone", "weight": 1},
]
PAVING = [
    {"block": "minecraft:stone_bricks", "weight": 3},
    {"block": "minecraft:polished_andesite", "weight": 2},
    {"block": "minecraft:andesite", "weight": 1},
]
DECK = [
    {"block": "minecraft:spruce_planks", "weight": 6},
    {"block": "minecraft:dark_oak_planks", "weight": 1},
]


class Batch:
    def __init__(self, bid, note):
        self.bid, self.note, self.edits, self.n = bid, note, [], 0

    def box(self, lo, hi):
        """Select a world-coordinate box; returns the region id."""
        self.n += 1
        name = f"region/r{self.n:03d}"
        rel = lambda p: [p[i] - ANCHOR[i] for i in range(3)]
        mn = [min(a, b) for a, b in zip(lo, hi)]
        mx = [max(a, b) for a, b in zip(lo, hi)]
        self.edits.append({"name": name, "shape": {"frame": FRAME, "kind": "box",
                                                   "min": rel(mn), "max": rel(mx)},
                           "verb": "select"})
        return name

    def fill(self, lo, hi, blocks, scale=None):
        r = self.box(lo, hi)
        recipe = {"blocks": blocks if isinstance(blocks, list)
                  else [{"block": blocks, "weight": 1}]}
        if scale:
            recipe["scale"] = scale
        self.edits.append({"recipe": recipe, "region": r, "verb": "fill"})

    def carve(self, lo, hi):
        self.edits.append({"region": self.box(lo, hi), "verb": "carve"})

    def doc(self):
        return {"area": "area/site", "edits": self.edits, "id": self.bid, "note": self.note}


def masonry():
    b = Batch("batch/quay-wall",
              "The stone quay: a solid body of stone brick from the sea floor up to the "
              "quay top, its face standing four courses over the landing stage, paved on "
              "top, with a parapet on its two sides.")
    # The quay body, sea floor (y 55) to the paving course; its north face is the wall.
    b.fill((8199, 55, 8196), (8216, 62, 8205), WET_STONE)
    b.fill((8199, 63, 8196), (8216, 66, 8205), STONE)
    b.fill((8200, 67, 8197), (8215, 67, 8204), PAVING, scale=0.6)
    b.fill((8199, 67, 8196), (8216, 67, 8196), "minecraft:smooth_stone")
    b.fill((8199, 67, 8197), (8199, 67, 8205), "minecraft:smooth_stone")
    b.fill((8216, 67, 8197), (8216, 67, 8205), "minecraft:smooth_stone")
    b.fill((8200, 67, 8205), (8215, 67, 8205), "minecraft:smooth_stone")
    # Clear the derived shell above the quay top, then the parapet: sides and back.
    b.carve((8199, 68, 8196), (8216, 72, 8205))
    b.fill((8199, 68, 8196), (8199, 68, 8205), "minecraft:stone_brick_wall")
    b.fill((8216, 68, 8196), (8216, 68, 8205), "minecraft:stone_brick_wall")
    # The head of the steps is a gateway through the wall: two piers and a lintel.
    # East of it, from x 8206, the quay edge is open over the landing.
    b.fill((8200, 68, 8196), (8200, 71, 8196), STONE)
    b.fill((8203, 68, 8196), (8205, 71, 8196), STONE)
    b.fill((8201, 71, 8196), (8202, 71, 8196), "minecraft:stone_brick_slab[type=top]")
    return b


def landing():
    b = Batch("batch/landing-stage",
              "The landing stage: a spruce deck on log piles over the water at the foot of "
              "the quay wall, railed on its three water sides, with stone steps up the "
              "wall face to the quay top.")
    # Everything the derivation built above the deck goes: its roof and walls.
    b.carve((8199, 64, 8187), (8216, 72, 8195))
    b.fill((8199, 63, 8187), (8216, 63, 8195), DECK, scale=0.5)
    # Piles down to the sea floor.
    for x in (8199, 8205, 8210, 8216):
        b.fill((x, 55, 8187), (x, 62, 8187), "minecraft:spruce_log")
    for z in (8191, 8195):
        b.fill((8199, 55, z), (8199, 62, z), "minecraft:spruce_log")
        b.fill((8216, 55, z), (8216, 62, z), "minecraft:spruce_log")
    # The rail on the water sides.
    b.fill((8199, 64, 8187), (8216, 64, 8187), "minecraft:spruce_fence")
    b.fill((8199, 64, 8188), (8199, 64, 8195), "minecraft:spruce_fence")
    b.fill((8216, 64, 8188), (8216, 64, 8195), "minecraft:spruce_fence")
    # The steps: a two-wide flight against the wall face, rising west to a head at
    # x 8201..8203 that opens south onto the quay top through the wall.
    b.fill((8201, 64, 8194), (8203, 67, 8195), STONE)
    for x, top in ((8206, 64), (8205, 65), (8204, 66)):
        if top > 64:
            b.fill((x, 64, 8194), (x, top - 1, 8195), STONE)
        b.fill((x, top, 8194), (x, top, 8195), "minecraft:stone_brick_stairs[facing=west]")
    # A low balustrade along the foot of the flight, so the bottom tread is taken
    # from the east, the way it climbs.
    b.fill((8201, 64, 8193), (8206, 64, 8193), "minecraft:stone_brick_wall")
    return b


def lamps_and_furniture():
    b = Batch("batch/lamps",
              "Lamps and the things on a quay: lantern posts at the rail, bracket lamps on "
              "the wall face, lantern bollards along the quay edge, lamp standards at the back, "
              "barrels and a bench where people wait.")
    # Lantern posts on the deck, at the rail.
    for x in (8200, 8207, 8215):
        b.fill((x, 64, 8188), (x, 65, 8188), "minecraft:spruce_fence")
        b.fill((x, 66, 8188), (x, 66, 8188), "minecraft:lantern")
    # Bracket lamps on the wall face: a fence arm out of the wall, a lantern under it.
    for x in (8200, 8209, 8213):
        b.fill((x, 67, 8195), (x, 67, 8195), "minecraft:spruce_fence")
        b.fill((x, 66, 8195), (x, 66, 8195), "minecraft:lantern[hanging=true]")
    # Bollards along the open quay edge; the outer two carry lanterns.
    for x in (8207, 8211, 8214):
        b.fill((x, 68, 8196), (x, 68, 8196), "minecraft:polished_blackstone_wall")
    for x in (8207, 8214):
        b.fill((x, 69, 8196), (x, 69, 8196), "minecraft:lantern")
    # A lantern on each pier of the gateway at the head of the steps.
    for x in (8200, 8203):
        b.fill((x, 72, 8196), (x, 72, 8196), "minecraft:lantern")
    # Lamp standards along the back of the quay, in front of the buildings.
    for x in (8202, 8209, 8215):
        b.fill((x, 68, 8204), (x, 69, 8204), "minecraft:polished_blackstone_wall")
        b.fill((x, 70, 8204), (x, 70, 8204), "minecraft:lantern")
    # A bench facing the water and a few barrels, both stood off the parapet so
    # neither is a step up onto it.
    b.fill((8205, 68, 8202), (8207, 68, 8202), "minecraft:spruce_stairs[facing=south]")
    b.fill((8212, 68, 8201), (8213, 68, 8202), "minecraft:barrel[facing=up]")
    return b


def roof(b, x0, x1, z0, z1, y0, stair, ridge):
    """A gable roof over x0..x1, z0..z1 (ridge along x), eaves at y0.

    The gable ends are filled with planks; the slopes are stairs ascending to
    the ridge from both sides, overhanging the gable ends by one block.
    """
    depth = z1 - z0 + 1
    half = (depth - 1) // 2
    for i in range(half):
        y = y0 + i
        if z0 + i + 1 <= z1 - i - 1:
            b.fill((x0, y, z0 + i + 1), (x1, y, z1 - i - 1), ridge)
        b.fill((x0 - 1, y, z0 + i), (x1 + 1, y, z0 + i), f"{stair}[facing=south]")
        b.fill((x0 - 1, y, z1 - i), (x1 + 1, y, z1 - i), f"{stair}[facing=north]")
    if depth % 2 == 1:
        b.fill((x0 - 1, y0 + half, z0 + half), (x1 + 1, y0 + half, z0 + half),
               ridge.replace("_planks", "_slab"))
    elif depth % 2 == 0:
        b.fill((x0 - 1, y0 + half, z0 + half), (x1 + 1, y0 + half, z0 + half + 1),
               ridge.replace("_planks", "_slab"))


def harbour_front():
    b = Batch("batch/harbour-front",
              "The shore the quay stands out from, and the backs of the quay: a stone toll "
              "house and a timber warehouse facing the water, a grass bank either side "
              "with a few trees.")
    # The shore: a bank of earth on a stone footing, grassed at the quay's height.
    b.fill((8186, 55, 8206), (8229, 62, 8214), [
        {"block": "minecraft:stone", "weight": 3},
        {"block": "minecraft:andesite", "weight": 2},
        {"block": "minecraft:cobblestone", "weight": 1},
    ])
    b.fill((8186, 63, 8206), (8229, 66, 8214), [
        {"block": "minecraft:dirt", "weight": 4},
        {"block": "minecraft:coarse_dirt", "weight": 1},
    ])
    b.fill((8186, 67, 8206), (8229, 67, 8214), [
        {"block": "minecraft:grass_block", "weight": 5},
        {"block": "minecraft:coarse_dirt", "weight": 1},
    ], scale=0.5)
    # The toll house: stone, two windows onto the quay, a spruce roof.
    b.fill((8199, 63, 8205), (8207, 71, 8211), STONE)
    # The party wall between the two buildings closes the alley off the quay.
    b.fill((8207, 63, 8212), (8207, 71, 8212), STONE)
    for x in (8201, 8204):
        b.fill((x, 69, 8205), (x, 70, 8205), "minecraft:glass_pane")
    roof(b, 8199, 8206, 8205, 8211, 72, "minecraft:spruce_stairs", "minecraft:spruce_planks")
    b.fill((8207, 72, 8205), (8207, 72, 8212), STONE)
    # The warehouse: a stone plinth, spruce boards on a log frame, a dark roof.
    b.fill((8208, 63, 8205), (8216, 68, 8212), "minecraft:cobblestone")
    b.fill((8208, 69, 8205), (8216, 72, 8212), [
        {"block": "minecraft:spruce_planks", "weight": 5},
        {"block": "minecraft:stripped_spruce_wood", "weight": 1},
    ], scale=0.8)
    for x in (8208, 8216):
        b.fill((x, 69, 8205), (x, 72, 8205), "minecraft:stripped_spruce_log")
    for x in (8210, 8214):
        b.fill((x, 70, 8205), (x, 71, 8205), "minecraft:glass_pane")
    roof(b, 8208, 8216, 8205, 8212, 73, "minecraft:dark_oak_stairs", "minecraft:dark_oak_planks")
    # Trees on the bank, clear of the quay.
    west = b.box((8186, 68, 8207), (8194, 68, 8214))
    b.edits.append({"count": 2, "region": west, "spacing": 5, "tree": "oak", "verb": "plant"})
    east = b.box((8221, 68, 8207), (8229, 68, 8214))
    b.edits.append({"count": 2, "region": east, "spacing": 5, "tree": "oak", "verb": "plant"})
    return b


def main():
    here = pathlib.Path(__file__).resolve().parent.parent
    # One batch: the lighting invariant re-proves after every batch, and the quay is
    # only lit once its lamps stand, so the masonry, the landing stage and the lamps
    # land together.
    whole = Batch("batch/the-quay",
                  "The whole landing: the stone quay with its parapet, the spruce landing "
                  "stage railed over the water with steps up the wall, the lamps and "
                  "furniture of a working quay, and the shore and buildings behind it.")
    for part in (masonry(), landing(), lamps_and_furniture(), harbour_front()):
        for e in part.edits:
            whole.n += 1
            if e["verb"] == "select":
                old = e["name"]
                e["name"] = f"region/r{whole.n:03d}"
                ren = {old: e["name"]}
            elif "region" in e:
                e["region"] = ren[e["region"]]
                whole.n -= 1
            whole.edits.append(e)
    doc = {"campaign_id": "the-ferry-landing",
           "content": {"batches": [whole.doc()]},
           "dsl_version": "0.35.1", "stage": "world-edits"}
    out = here / "world-edits.json"
    out.write_text(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
