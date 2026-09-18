"""The valley floor, the crag, the two shelves cut into its faces, and trees."""
from . import layout as L
from .grid import hsh, AIR, rail
from .palette import BEDROCK, EARTH, TURF, ROCK, ROCK_MOSS, LOG, LEAVES, WALL, ROAD

GROUND = L.VALLEY - 1          # the surface course


def valley(g):
    g.box(0, L.X - 1, 0, GROUND - 3, 0, L.Z - 1, BEDROCK)
    g.box(0, L.X - 1, GROUND - 2, GROUND - 1, 0, L.Z - 1, EARTH)
    g.box(0, L.X - 1, GROUND, GROUND, 0, L.Z - 1, TURF)


def crag(g):
    """The rock: sheer where the castle's curtain stands on it, with a broken
    skirt at its foot so it reads as a rock and not a plinth."""
    top = L.CASTLE - 1
    x0, x1, z0, z1 = L.CRAG
    g.box(x0, x1, GROUND, top, z0, z1, ROCK)
    # the skirt: boulders and scree around the foot, never under the shelves
    for x in range(x0 - 6, x1 + 7):
        for z in range(z0 - 6, z1 + 7):
            if x0 <= x <= x1 and z0 <= z <= z1:
                continue
            dx = max(x0 - x, 0, x - x1)
            dz = max(z0 - z, 0, z - z1)
            d = max(dx, dz)
            h = int((7 - d) * 1.6 * hsh(x // 2, z // 2, 11)) - 1
            if h > 0 and not on_approach(x, z):
                g.box(x, x, GROUND, GROUND + h, z, z, ROCK_MOSS if hsh(x, z, 12) < .4 else ROCK)
    # the crag's own face: buttresses of rock standing out of it
    def outcrop(x, z, dx, dz):
        h = int((top - GROUND + 2) * (0.45 + 0.6 * hsh(x // 2, z // 2, 17)))
        d = 1 + int(4 * hsh(x // 2, z // 2, 18))
        for k in range(1, d + 1):
            hh = min(h - 2 * (k - 1), top - GROUND)
            if hh > 0 and not on_approach(x + dx * k, z + dz * k):
                g.box(x + dx * k, x + dx * k, GROUND, GROUND + hh, z + dz * k, z + dz * k,
                      ROCK_MOSS if hsh(x, z, k) < .35 else ROCK)
    for x in range(x0, x1 + 1):
        outcrop(x, z0, 0, -1)
        if not 4 <= x <= 105:
            outcrop(x, z1, 0, 1)
    for z in range(z0, z1 + 1):
        outcrop(x1, z, 1, 0)
        if z < 120:
            outcrop(x0, z, -1, 0)
    # no scree pockets along the south foot east of the gate
    g.clear(100, L.X - 2, GROUND + 1, top, z1 + 1, z1 + 14)
    # the crag's own face: moss bands and a few overhanging courses
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            if hsh(x, z, 13) < .3:
                g.box(x, x, GROUND + 3, GROUND + 3 + int(6 * hsh(x, z, 14)), z, z, ROCK_MOSS)
    for z in range(z0, z1 + 1):
        for x in (x0, x1):
            if hsh(x, z, 15) < .3:
                g.box(x, x, GROUND + 3, GROUND + 3 + int(6 * hsh(x, z, 16)), z, z, ROCK_MOSS)


def on_approach(x, z):
    """The road, the causeway's foot and the shrine keep their ground clear."""
    return 74 <= x <= 101 and z >= 172


def shelves(g):
    """The side route's ground: rock cut out from the crag's south and west
    faces at castle height, with a parapet on the drop side and a sheer fall
    below it."""
    top = L.CASTLE - 1
    # the fall below the shelves is sheer: no scree against it
    g.clear(0, 82, GROUND + 1, L.CASTLE + 6, 178, 186)
    g.clear(0, 3, GROUND + 1, L.CASTLE + 6, 120, 186)
    for (sx0, sx1, sz0, sz1) in (L.SHELF_SOUTH, L.SHELF_WEST):
        g.box(sx0, sx1, GROUND, top, sz0, sz1, ROCK)
    # the west shelf's blind north end, one course of rock for its parapet
    g.box(4, 11, GROUND, top, L.SHELF_WEST[2] - 1, L.SHELF_WEST[2] - 1, ROCK)
    g.box(5, 75, top, top, 172, 176, ROAD)
    g.box(5, 9, top, top, 128, 176, ROAD)
    # east of the shelf's end, under the gate towers, open air to the valley
    g.clear(76, 83, GROUND + 1, L.CASTLE + 6, 176, 186)


RAIL = [(6, "minecraft:stone_brick_wall"), (3, "minecraft:mossy_stone_brick_wall"),
        (2, "minecraft:cobblestone_wall"), (2, "minecraft:mossy_cobblestone_wall")]


def rail_material(x, z):
    """The parapet's stone, mixed by position: the same stone as the curtain
    over it, weathered unevenly."""
    t = hsh(x, z, 21) * sum(w for w, _ in RAIL)
    for w, m in RAIL:
        if t < w:
            return m
        t -= w
    return RAIL[-1][1]


def parapets(g):
    """The shelves' parapet, laid after every part so it reads what stands.

    One unbroken course of wall blocks along every open edge of the side
    route — the south shelf's lip, the west shelf's lip and its blind north
    end. A wall block stands a block and a half, over the height a blow can
    lift a body (a knockback rises about a block and a quarter) and under the
    eye (a block and five eighths), so nothing fought on the shelf goes over
    it and the valley stays in view. Every so often the course steps up into
    a stub of the old parapet, a stone with a post on it."""
    top = L.CASTLE - 1
    line = ([(x, 177) for x in range(4, 76)] + [(4, z) for z in range(L.SHELF_WEST[2], 177)]
            + [(x, L.SHELF_WEST[2] - 1) for x in range(4, 12)])
    for x, z in line:
        if g.get(x, L.CASTLE, z) != AIR or g.get(x, top, z) == AIR:
            continue
        if hsh(x, z, 23) < .1:
            g.set(x, L.CASTLE, z, WALL)
            g.set(x, L.CASTLE + 1, z, rail(rail_material(x, z)))
        else:
            g.set(x, L.CASTLE, z, rail(rail_material(x, z)))


def tree(g, x, z, h):
    g.box(x, x, L.VALLEY, L.VALLEY + h, z, z, LOG)
    for k in range(3, h + 2):
        r = max(0, (h + 2 - k) // 2 - (k % 2))
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) <= r + 1 and (dx or dz) and g.get(x + dx, L.VALLEY + k, z + dz) == AIR:
                    g.set(x + dx, L.VALLEY + k, z + dz, LEAVES)
    g.set(x, L.VALLEY + h + 1, z, LEAVES)
    g.set(x, L.VALLEY + h + 2, z, LEAVES)


def trees(g):
    for z in range(3, L.Z - 3, 5):
        for x in range(3, L.X - 3, 5):
            jx = x + int(4 * hsh(x, z, 31)); jz = z + int(4 * hsh(x, z, 32))
            x0, x1, z0, z1 = L.CRAG
            if x0 - 9 <= jx <= x1 + 9 and z0 - 9 <= jz <= z1 + 9:
                continue
            if 55 <= jx <= 120 and jz >= 170:
                continue
            if 45 <= jx <= 130 and jz >= 170 and hsh(jx, jz, 35) < .6:
                continue
            if hsh(jx, jz, 33) < .35 and g.get(jx, L.VALLEY, jz) == AIR:
                tree(g, jx, jz, 5 + int(5 * hsh(jx, jz, 34)))


def field_wall(g):
    """A dry-stone wall round the whole valley field, two courses high, so the
    party's world ends where the piece does."""
    for x in range(L.X):
        for z in (0, L.Z - 1):
            g.box(x, x, L.VALLEY, L.VALLEY + 1, z, z, ROCK_MOSS)
    for z in range(L.Z):
        for x in (0, L.X - 1):
            g.box(x, x, L.VALLEY, L.VALLEY + 1, z, z, ROCK_MOSS)


def build(g):
    valley(g)
    crag(g)
    shelves(g)
    trees(g)
    field_wall(g)
