#!/usr/bin/env python3
"""Draws each place of The Treehouse Camp and writes programs/<place>.json.

    python3 places.py <place-stem> [...]     (or `all`)

Every position comes from the place's handout, fetched at run time; the
design itself is in world coordinates, the same as DESIGN.md section 4.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import thlib  # noqa: E402
import lights  # noqa: E402

C = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PREFABS = os.environ.get("DELVEWRIGHT_PREFABS", "")
CAMPAIGN = "the-treehouse-camp"

# ---------------------------------------------------------------- materials
BARK = [(6, "mangrove_wood[axis=y]"), (3, "spruce_wood[axis=y]"), (1, "dark_oak_wood[axis=y]")]
BARK_X = [(6, "mangrove_wood[axis=x]"), (3, "spruce_wood[axis=x]")]
BARK_Z = [(6, "mangrove_wood[axis=z]"), (3, "spruce_wood[axis=z]")]
LEAVES = [(5, "oak_leaves[persistent=true]"), (3, "dark_oak_leaves[persistent=true]"), (1, "azalea_leaves[persistent=true]")]
BUSH = [(4, "azalea_leaves[persistent=true]"), (2, "oak_leaves[persistent=true]"), (1, "flowering_azalea_leaves[persistent=true]")]
FOREST_FLOOR = [(6, "moss_block"), (2, "podzol[snowy=false]"), (1, "coarse_dirt"), (1, "rooted_dirt")]
DECK = [(7, "oak_planks"), (2, "spruce_planks"), (1, "stripped_oak_wood[axis=y]")]
DECK_WORN = [(5, "oak_planks"), (3, "spruce_planks"), (2, "stripped_oak_wood[axis=y]"), (1, "mossy_cobblestone")]
RAIL = "oak_fence"
POST = "stripped_oak_log[axis=y]"
THATCH = "hay_block[axis=y]"
CABIN_WALL = [(4, "spruce_planks"), (1, "stripped_spruce_wood[axis=y]")]
LANTERN_HANG = "lantern[hanging=true]"
LANTERN_STAND = "lantern[hanging=false]"
CHAIN_Y = "iron_chain[axis=y]"


def P(m, x, y, z, choices, salt=0):
    m.set(x, y, z, m.pick(x, y, z, choices, salt))


def trunk_layer(m, cx, cz, r, y, choices=BARK, keep=None):
    for x, z in m.disc_cells(cx, cz, r):
        if keep and keep(x, z):
            continue
        P(m, x, y, z, choices)


def ladder(m, x, z0, z1, y0, y1, facing):
    for y in range(y0, y1 + 1):
        for z in range(z0, z1 + 1):
            m.set(x, y, z, f"ladder[facing={facing}]")


def root(m, cells, heights, base_y, salt=1):
    """A buttress root: a list of (x, z) cells and a height for each."""
    for (x, z), h in zip(cells, heights):
        for dy in range(h):
            P(m, x, base_y + dy, z, BARK, salt)
        top = base_y + h
        if m.get(x, top, z) is None and h >= 1:
            m.set(x, top, z, "moss_carpet")


def line_cells(x0, z0, x1, z1, thick=2):
    """Cells of a thick straight line, ordered from (x0, z0) outward."""
    n = max(abs(x1 - x0), abs(z1 - z0))
    out = []
    for i in range(n + 1):
        t = i / n if n else 0
        x = round(x0 + (x1 - x0) * t)
        z = round(z0 + (z1 - z0) * t)
        step = []
        for dx in range(thick):
            for dz in range(thick):
                step.append((x + dx, z + dz))
        out.append(step)
    return out


def hanging_lantern(m, x, z, y_top, drop):
    """A lantern on a chain hanging `drop` cells under the block at y_top + 1."""
    for y in range(y_top - drop + 2, y_top + 1):
        m.set(x, y, z, CHAIN_Y)
    m.set(x, y_top - drop + 1, z, LANTERN_HANG)


def light_marks(m, node):
    for anchor, n, (x, y, z), _ in lights.for_node(node):
        m.mark(anchor.split("/", 1)[1], x, y, z, "south")


def write(m, stem):
    prog = m.program(f"{CAMPAIGN}-{stem}")
    path = os.path.join(C, "programs", f"{stem}.json")
    json.dump(prog, open(path, "w"), indent=1)
    cells = len(m.cells)
    print(f"{stem}: {cells} blocks, {len(prog['rules'])} rules, {len(prog['palette'])} roles, "
          f"faces {prog['shown_faces']}, {os.path.getsize(path)} bytes")


# ---------------------------------------------------------------- the Hearth Tree
HEARTH = (36.0, 36.0)


def hearth_trunk_keep_ladder(x, z):
    # The west face beside the ladder (x 30, z 35..36) stays flat bark.
    return False


def root_glade():
    h = thlib.handout(C, "node/root-glade", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    floor = 72
    cx, cz = HEARTH
    # Ground of the glade: the handed level, y 71, inside the ring.
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            P(m, x, floor - 1, z, FOREST_FLOOR, 3)
    # The trunk, straight 10 across, flared at its foot except on the ladder face.
    for y in range(floor - 1, y1 + 1):
        trunk_layer(m, cx, cz, 5.0, y)
    for y in range(floor, floor + 3):
        trunk_layer(m, cx, cz, 6.0, y, keep=lambda x, z: x <= 31 and 33 <= z <= 38)
    # Buttress roots: tall walls of bark that end in one low knuckle, so no
    # body climbs them (a step of two from the knuckle to the root).
    roots = [
        (38, 29, 38, 27),   # north
        (41, 30, 43, 28),   # north-east
        (41, 37, 43, 37),   # east
        (33, 41, 33, 43),   # south
        (30, 41, 28, 43),   # south-west
    ]
    for rx0, rz0, rx1, rz1 in roots:
        steps = line_cells(rx0, rz0, rx1, rz1, 2)
        for i, step in enumerate(steps):
            hgt = 1 if i == len(steps) - 1 else max(3, 6 - i)
            for (x, z) in step:
                if (x - cx + 0.5) ** 2 + (z - cz + 0.5) ** 2 <= 25:
                    continue
                for dy in range(hgt):
                    P(m, x, floor + dy, z, BARK, 7)
                if m.get(x, floor + hgt, z) is None:
                    m.set(x, floor + hgt, z, "moss_carpet")
    # The hedge round the glade: fallen logs and bushes three high on the
    # ring, so the glade is a room with open sky-light above its walls.
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                for dy in range(3):
                    if dy < 2 and (x + z) % 7 in (0, 1, 2):
                        axis = "x" if z in (z0, z1) else "z"
                        m.set(x, floor + dy, z, f"mangrove_log[axis={axis}]")
                    else:
                        P(m, x, floor + dy, z, BUSH, 11)
    # Ferns along the inside of the hedge.
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            edge = x in (x0 + 1, x1 - 1) or z in (z0 + 1, z1 - 1)
            if edge and m.get(x, floor, z) is None and (x * 3 + z) % 4 != 0:
                m.set(x, floor, z, "fern")
    # The fire ring, south-east of the trunk, and two log seats.
    fx, fz = 42, 42
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx or dz:
                m.set(fx + dx, floor, fz + dz, "mossy_cobblestone_slab[type=bottom]")
    m.set(fx, floor, fz, "campfire[lit=true,facing=north]")
    for z in (40, 41):
        m.set(44, floor, z, "stripped_spruce_log[axis=z]")
    for x in (40, 41):
        m.set(x, floor, 44, "stripped_spruce_log[axis=x]")
    # The rope ladder up the bark to the Hearth House (its top rung is the house's).
    ladder(m, 30, 35, 36, floor, y1, "west")
    # Lanterns hanging on chains from the platform overhead, and two on posts.
    for (lx, lz) in ((28, 30), (43, 32), (28, 42), (37, 43)):
        hanging_lantern(m, lx, lz, y1, 6)
    for (lx, lz) in ((27, 33), (44, 35)):
        hanging_lantern(m, lx, lz, y1, 9)
    # Contract: the glade's floor, the ladder shaft above it, the top rung's cell.
    m.space("glade", "open", (x0 + 1, floor, z0 + 1, x1 - 1, floor + 2, z1 - 1),
            (30, floor + 3, 35, 30, y1 - 1, 36))
    m.via("glade-ladder", (30, y1, 35, 30, y1, 36))
    top = floor + 3
    m.nobody("over-the-glade", "the tops of the buttress roots, the hedge and the hanging lanterns: nobody climbs up here",
             (x0, top, z0, 29, y1, z1), (31, top, z0, x1, y1, z1),
             (30, top, z0, 30, y1, 34), (30, top, 37, 30, y1, z1))
    m.entry = "glade"
    m.edge(a="glade", b="exterior", **{"class": "walk", "via": "glade-ladder"})
    m.mark("spawn", 28, floor, 28, "south", role="entry")
    m.mark("node-root-glade", 28, floor, 38, "north")
    light_marks(m, "node/root-glade")
    write(m, "root-glade")


PLACES = {"root-glade": root_glade}

if __name__ == "__main__":
    names = sys.argv[1:]
    if names == ["all"]:
        names = list(PLACES)
    for n in names:
        PLACES[n]()
