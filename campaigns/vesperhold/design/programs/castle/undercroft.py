"""Under the rock: the Crypt of Wardens, the passage, and the Undertide Pool."""
from . import layout as L
from .grid import PAL, hsh, stairs, slab, block, rail, state, AIR
from .palette import (ROCK, ROCK_MOSS, FLOOR, PILLAR, TRIM, CHAPEL, WATER, CANDLES,
                      SOUL_LANTERN, LANTERN, COBWEB, BARS_Z, CHAIN, GLASS_DARK)

U = L.UNDER
VAULT = None
# the Undertide over the pool's floor: bottom slabs standing in their own water
WET_FLOOR = PAL.role("pool_floor_wet", [
    {"weight": 4, "block": state("minecraft:tuff_slab", type="bottom", waterlogged=True)},
    {"weight": 3, "block": state("minecraft:cobbled_deepslate_slab", type="bottom", waterlogged=True)},
    {"weight": 2, "block": state("minecraft:mossy_cobblestone_slab", type="bottom", waterlogged=True)},
])

# the same flags without the water, where a cut in the floor must stay dry;
# drawn with the wet flags' weights so the site's other draws keep their order
DRY_FLOOR = PAL.role("pool_floor_dry", [
    {"weight": 4, "block": state("minecraft:tuff_slab", type="bottom", waterlogged=False)},
    {"weight": 3, "block": state("minecraft:cobbled_deepslate_slab", type="bottom", waterlogged=False)},
    {"weight": 2, "block": state("minecraft:mossy_cobblestone_slab", type="bottom", waterlogged=False)},
])


def vaulted(g, x0, x1, z0, z1, height, wall, floor, bay=6):
    """A room cut into rock with a ribbed vault: the walls and the ceiling
    are masonry, the corners of each bay stepped in."""
    top = U + height
    g.box(x0 - 1, x1 + 1, U - 1, top, z0 - 1, z1 + 1, wall)
    g.box(x0, x1, U - 1, U - 1, z0, z1, floor)
    g.clear(x0, x1, U, top - 1, z0, z1)
    # ribs: every bay a transverse arch stepping down from the ceiling
    for x in range(x0 + bay - 1, x1, bay):
        g.box(x, x, top - 1, top - 1, z0, z1, wall)
        g.box(x, x, top - 2, top - 2, z0, z0 + 1, wall)
        g.box(x, x, top - 2, top - 2, z1 - 1, z1, wall)
        g.box(x, x, U, top - 3, z0, z0, PILLAR)
        g.box(x, x, U, top - 3, z1, z1, PILLAR)


def crypt(g):
    p = L.P["crypt-of-wardens"]
    x0, x1, z0, z1 = p.box
    stone = block("minecraft:polished_deepslate")
    vaulted(g, x0, x1, z0, z1, p.height, block("minecraft:deepslate_bricks"), FLOOR)
    # tombs in two rows, each lid carved with a bell
    for x in range(x0 + 2, x1 - 1, 6):
        for z in (z0 + 3, z1 - 5):
            g.box(x, x + 2, U, U, z, z + 2, stone)
            g.set(x + 1, U + 1, z + 1, block("minecraft:chiseled_deepslate"))
            if hsh(x, z, 151) < .5:
                g.set(x, U + 1, z, CANDLES)
    # the kneeling knight's dais at the far end
    g.box(x1 - 4, x1, U, U, 113, 118, stone)
    g.clear(x1 - 3, x1 - 1, U + 1, U + 3, 114, 117)
    # the way in (from the psalter stair, west), the way on (north, to the pool)
    g.clear(x0 - 1, x0 - 1, U, U + 2, 125, 127)
    g.clear(30, 33, U, U + 3, z0 - 1, z0 - 1)
    for (lx, lz) in ((x0, z0), (x1, z0), (x0, z1 - 3), (x1, z1), (x0 + 11, z0 + 11)):
        g.set(lx, U, lz, SOUL_LANTERN)
    g.set(x0 + 5, U + p.height - 2, z0 + 3, COBWEB)
    g.mark("crypt-of-wardens", 38, U, 122, "north")
    g.mark("warden-knight", x1 - 2, U + 1, 115, "west")
    g.mark("crypt-drop", 38, U, 110, "north")


def passage(g):
    g.box(29, 34, U - 1, U + 4, 92, 103, block("minecraft:deepslate_bricks"))
    g.clear(30, 33, U, U + 3, 92, 103)
    g.box(30, 33, U - 1, U - 1, 92, 103, FLOOR)
    g.set(30, U, 97, SOUL_LANTERN)


def pool(g):
    p = L.P["undertide-pool"]
    x0, x1, z0, z1 = p.box
    top = U + p.height
    # a rough cavern, its walls rock rather than masonry
    g.box(x0 - 2, x1 + 2, U - 3, top, z0 - 2, z1 + 2, ROCK)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            h = p.height - (1 if hsh(x, z, 161) < .25 else 0) - (1 if hsh(x, z, 162) < .1 else 0)
            g.clear(x, x, U, U + h - 1, z, z)
            g.set(x, U - 1, z, ROCK_MOSS if hsh(x, z, 163) < .3 else FLOOR)
    # the well at the centre: grey water behind a curb nothing walks over,
    # and under it a shaft to the bottom, where the Undertide takes whatever
    # reaches it
    cx, cz = 36, 80
    curb = rail("minecraft:polished_deepslate_wall")
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 5, cz + 6):
            d2 = (x - cx) ** 2 + (z - cz) ** 2
            if d2 <= 16:
                g.box(x, x, U - 4, U - 2, z, z, WATER)
                g.set(x, U - 1, z, WATER)
            elif d2 <= 26:
                g.set(x, U, z, slab("minecraft:polished_deepslate_slab"))
    g.box(cx - 5, cx + 5, U - 5, U - 5, cz - 5, cz + 5, ROCK)
    # the curb: every cell that touches the water, one wall block high — a
    # block and a half, over the lift of a blow and under a player's eye
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 5, cz + 6):
            d2 = (x - cx) ** 2 + (z - cz) ** 2
            if d2 > 16 and any((x + dx - cx) ** 2 + (z + dz - cz) ** 2 <= 16
                               for dx in (-1, 0, 1) for dz in (-1, 0, 1)):
                g.set(x, U - 1, z, block("minecraft:polished_deepslate"))
                g.set(x, U, z, curb)
    # one opening in the curb, on the well's west side, between two gateposts
    # two blocks high: a body in the water climbs out onto its sill, whose top is
    # a step above the water, and a body on the floor comes in by jumping the dry
    # cut in front of it. The choir never can: it does not jump a gap, a body in
    # the cut is a block and a half under the sill, and there is nothing a body
    # can leave open. (A gate stood here; a player who opened it and walked on,
    # or died in the well, left the choir a way to walk in and drown.)
    g.set(cx - 5, U, cz, AIR)
    # the gateposts and the sill are the cavern's own rock: rock is drawn from
    # a mix, and the cut takes three wet flags out of the floor, so the three
    # rock cells here keep the site's weighted draws in step and nothing else in
    # the castle changes its stone
    g.set(cx - 5, U - 1, cz, ROCK)
    for dz in (-1, 1):
        g.set(cx - 5, U, cz + dz, ROCK)
        g.set(cx - 5, U + 1, cz + dz, block("minecraft:polished_deepslate"))
    for dz in (-1, 0, 1):
        g.set(cx - 6, U - 1, cz + dz, AIR)
        g.set(cx - 6, U - 2, cz + dz, DRY_FLOOR)
    # the floor round the cut stays dry, so that no water pours into it and a
    # body in the cut cannot swim up to the sill (in water it rose to 68.67
    # from the cut's floor at 66.5): the three flags on its west side are dry
    # slabs at the floor's height, the floor a body climbs out of the cut onto, and the four
    # corners beside them are whole rock, because a dry slab with two wet
    # flags beside it is wetted again by the next fluid tick (measured on the
    # pinned server); each of the three dry flags has one wet neighbour
    for dz in (-1, 0, 1):
        g.set(cx - 7, U - 1, cz + dz, DRY_FLOOR)
    for (dx, dz) in ((-7, -2), (-7, 2), (-6, -2), (-6, 2)):
        g.set(cx + dx, U - 1, cz + dz, ROCK)
    # the shaft under the well's heart, five deeper, rock all round it
    g.box(cx - 2, cx + 2, U - 11, U - 5, cz - 2, cz + 2, ROCK)
    g.box(cx - 1, cx + 1, U - 10, U - 5, cz - 1, cz + 1, WATER)
    for (lx, lz) in ((cx, cz - 5), (cx, cz + 5), (cx + 5, cz)):
        g.set(lx, U + 1, lz, SOUL_LANTERN)
    # the west lantern stands on the north gatepost: a lantern on the floor
    # against the curb is a step half a block up from the wet flags, and from
    # its top a drowned jumps onto the curb and walks along it into the well
    g.set(cx - 5, U + 2, cz - 1, SOUL_LANTERN)
    # choir stalls round the well, and the fallen tongue at its lip
    for (sx, sz) in ((cx - 8, cz), (cx + 8, cz), (cx, cz - 8), (cx, cz + 8)):
        g.set(sx, U, sz, stairs("minecraft:polished_deepslate_stairs", "south"))
    g.box(cx + 6, cx + 8, U, U, cz - 7, cz - 7, block("minecraft:iron_block"))
    g.set(cx + 6, U + 1, cz - 7, block("minecraft:iron_block"))
    # openings to the passage (south) and the well stair (west)
    g.clear(30, 33, U, U + 3, z1 + 1, z1 + 2)
    g.clear(x0 - 2, x0 - 1, U, U + 2, 76, 79)
    # barred windows through the crag's west face would be here if the pool
    # reached it; instead a light shaft from the garth drips in
    g.box(cx - 1, cx + 1, top, L.CASTLE - 2, cz - 1, cz + 1, AIR)
    g.box(cx - 1, cx + 1, L.CASTLE - 1, L.CASTLE - 1, cz - 1, cz + 1,
          block("minecraft:iron_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]"))
    for (lx, lz) in ((x0, z0), (x1, z0), (x0, z1), (x1, z1), (x0 + 4, 78), (x1 - 2, 70)):
        g.set(lx, U, lz, SOUL_LANTERN)
    # the Undertide has risen over the cavern floor: every flag outside the
    # well's ring stands in a skin of grey water, so a body fighting the choir
    # stands in it -- a drowned will not quarrel with anyone on dry ground while
    # the sky is light, and here there is no dry ground to leave them on. The
    # water is each slab's own, so it spreads nowhere; the flags under the stalls,
    # the lanterns and the fallen tongue stay whole, since a lantern will not
    # stand on a half block.
    wet = 0
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if ((x - cx) ** 2 + (z - cz) ** 2 > 26 and g.get(x, U, z) == AIR
                    and g.get(x, U - 1, z) in (ROCK_MOSS, FLOOR)):
                g.set(x, U - 1, z, WET_FLOOR)
                wet += 1
    assert wet > 0, "the pool floor took no water"
    g.mark("undertide-pool", 36, U, 90, "north")
    g.mark("drowned-choir", 36, U, 70, "south")
    g.mark("bell-tongue", 42, U, 74, "west")
    g.mark("undertide-well", 36, U - 9, 80, "north", stand=False)


def build(g):
    crypt(g)
    passage(g)
    pool(g)
