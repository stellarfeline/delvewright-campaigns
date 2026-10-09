"""Acts 3 and 4 — inside the body, on its head and back, and the Run: detail builders.

    python3 generators/places_act34.py "$(command -v delvec)" "$DELVEWRIGHT_PREFABS" [stem ...]

The body's own tones are the sculpt form's (generators/body_form.py): hide in grey,
flesh in red-brown, bone white. Inside, a room's walls and vault are flesh
shaped as a height field over its floor, so every surface over a body faces down
and nobody stands on a ledge of it; bone shows as ribs through the vault. Light
inside follows interior-lighting.md §7 and the owner's rules: natural light set
in the surface (glow lichen on the walls, cave vines with glow berries hung from
the vault), and the lamps earlier visitors brought set into niches under a lip
of bone, staggered, never a grid.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *  # noqa: F401,F403
import kit
from places_act1 import hang, flight, stair_head, landing
from places_act2 import h, stake, low_lamp, mud_floor, litter, BANKMUD

FLESH = [{"weight": 4, "block": "minecraft:red_terracotta"}, {"weight": 2, "block": "minecraft:brown_terracotta"},
         {"weight": 1, "block": "minecraft:pink_terracotta"}, {"weight": 1, "block": "minecraft:nether_wart_block"}]
TONGUE = [{"weight": 4, "block": "minecraft:pink_terracotta"}, {"weight": 2, "block": "minecraft:red_terracotta"},
          {"weight": 1, "block": "minecraft:nether_wart_block"}]
GUT = [{"weight": 3, "block": "minecraft:brown_terracotta"}, {"weight": 2, "block": "minecraft:red_terracotta"},
       {"weight": 1, "block": "minecraft:black_terracotta"}, {"weight": 1, "block": "minecraft:mud"}]
HEARTWALL = [{"weight": 3, "block": "minecraft:nether_wart_block"}, {"weight": 2, "block": "minecraft:red_terracotta"},
             {"weight": 1, "block": "minecraft:crimson_hyphae[axis=y]"}, {"weight": 1, "block": "minecraft:black_terracotta"}]
HIDE = [{"weight": 6, "block": "minecraft:gray_concrete"}, {"weight": 2, "block": "minecraft:gray_terracotta"},
        {"weight": 1, "block": "minecraft:light_gray_concrete"}]
BONE = [{"weight": 6, "block": "minecraft:bone_block[axis=y]"}, {"weight": 1, "block": "minecraft:calcite"}]


def body_room(p, floor, wall, top, ribs_every=0, rib_axis="z", salt=0, wall_lining=None, cap=None):
    """A chamber of the body: its floor, and over it a vault of flesh as a height field —
    air from the floor up to c(x, z), flesh above — high in the middle and falling to the
    walls, so the room's every overhead surface faces down. Ribs of bone run through the
    vault every `ribs_every` cells along `rib_axis`."""
    W, H, L = p.W, p.H, p.L
    p.box(0, 0, 0, W - 1, H - 1, L - 1, wall)
    for x in range(W):
        for z in range(L):
            p.put(x, 0, z, floor)
    cx, cz = (W - 1) / 2, (L - 1) / 2
    for x in range(W):
        for z in range(L):
            if x in (0, W - 1) or z in (0, L - 1):
                continue
            u = abs(x - cx) / max(0.5, (W - 1) / 2)
            v = abs(z - cz) / max(0.5, (L - 1) / 2)
            m = max(u, v) ** 3
            f = math.sqrt(max(0.0, 1 - m))
            c = 3 + int(round((top - 3) * f)) + (1 if h(x, z, salt) % 5 == 0 else 0)
            c = min(c, H - 2 if cap is None else cap)
            for y in range(1, c + 1):
                p.put(x, y, z, None)
    if ribs_every:
        for x in range(W):
            for z in range(L):
                k = z if rib_axis == "z" else x
                if k % ribs_every:
                    continue
                for y in range(1, H):
                    if p.get(x, y, z) is not None and p.get(x, y - 1, z) is None and y > 2:
                        p.put(x, y, z, bone("x" if rib_axis == "z" else "z"))
                        break
                for xx in (0, W - 1) if rib_axis == "z" else ():
                    pass


def air_neighbour(p, x, y, z):
    for d, n in (("north", (0, 0, -1)), ("south", (0, 0, 1)), ("west", (-1, 0, 0)), ("east", (1, 0, 0))):
        c = (x + n[0], y + n[1], z + n[2])
        if p.inb(*c) and p.get(*c) is None:
            return d, c
    return None, None


def body_lights(p, salt, n_niche=8, n_vine=10, n_lichen=30, soul=False, vine_floor=4, vine_len=3):
    """Staggered light: lamps in niches of the wall under a lip, vines with glow berries
    hung from the vault, glow lichen on the walls low and high."""
    W, H, L = p.W, p.H, p.L
    walls = []
    for x in range(W):
        for z in range(L):
            for y in range(1, H - 1):
                b = p.get(x, y, z)
                if b is None or (x, y, z) in p.cl:
                    continue
                d, c = air_neighbour(p, x, y, z)
                if d:
                    walls.append((x, y, z, d, c))
    walls.sort()
    placed = 0
    i = 0
    while placed < n_niche and walls and i < 4000:
        i += 1
        x, y, z, d, c = walls[h(i, salt, 5) % len(walls)]
        if not (2 <= y <= 5) or p.get(x, y + 1, z) is None or p.get(x, y - 1, z) is None:
            continue
        p.put(x, y, z, SOUL if soul else LANTERN)
        facing = {"north": "south", "south": "north", "west": "east", "east": "west"}[d]
        p.put(x, y + 1, z, stair("polished_granite", OPP[facing] if False else facing, "top"))
        placed += 1
    # vines from the vault
    tops = []
    for x in range(1, W - 1):
        for z in range(1, L - 1):
            col = [y for y in range(1, H) if p.get(x, y, z) is None]
            if not col:
                continue
            ty = max(col)
            if ty >= 5 and p.get(x, ty + 1, z) is not None:
                tops.append((x, ty, z))
    tops.sort()
    placed = 0; i = 0
    while placed < n_vine and tops and i < 4000:
        i += 1
        x, ty, z = tops[h(i, salt, 7) % len(tops)]
        if p.get(x, ty, z) is not None:
            continue
        ln = 1 + h(i, salt, 8) % vine_len
        bottom = max(vine_floor, ty - ln)
        for y in range(bottom + 1, ty + 1):
            p.put(x, y, z, vine_plant(h(y, x, z) % 2 == 0))
        p.put(x, bottom, z, vine_tip(True))
        placed += 1
    # lichen on the walls
    placed = 0; i = 0
    while placed < n_lichen and walls and i < 8000:
        i += 1
        x, y, z, d, c = walls[h(i, salt, 9) % len(walls)]
        if p.get(*c) is not None or c in p.cl:
            continue
        face = {"north": "s", "south": "n", "west": "e", "east": "w"}[d]
        p.put(c[0], c[1], c[2], lichen(**{face: True}))
        placed += 1


# =============================================================================
def mouth():
    """The mouth: through the teeth onto the tongue; a vault of palate ridged with bone over
    a floor of tongue, the teeth standing in a row along the jaw's edge either side of the way
    in; Marrack's lamps set in the cheek."""
    p = Place("mouth", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    flesh = p.role("flesh", FLESH)
    tongue = p.role("tongue", TONGUE)
    body_room(p, tongue, flesh, H - 3, ribs_every=3, rib_axis="z", salt=11)
    n = p.seam("jaw-to-mouth"); nlo, nhi = p.seam_box(n)
    for x in range(1, W - 1):
        if nlo[0] - 1 <= x <= nhi[0] + 1:
            continue
        if x % 2 == 0:
            y = 1
            while p.inb(x, y, 1) and p.get(x, y, 1) is None:
                p.put(x, y, 1, bone()); y += 1
    for z in range(3, L - 2, 2):
        p.put(1, 1, z, bone()); p.put(W - 2, 1, z, bone())
    body_lights(p, 11, n_niche=10, n_vine=12, n_lichen=30, vine_len=5)
    p.cut_seams(floor=tongue)
    p.mark("node-mouth", (7, 1, 7), "south")
    return p


def throat():
    """The throat: a corridor of ribs, every six blocks the same, flesh between; one rib broken
    and set wrong; earlier visitors' chalk-marked lamps in its walls."""
    p = Place("throat", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    flesh = p.role("flesh", FLESH)
    p.box(0, 0, 0, W - 1, H - 1, L - 1, flesh)
    p.box(0, 0, 0, W - 1, 0, L - 1, "minecraft:pink_terracotta")
    for z in range(L):
        for x in range(0, 3):
            for y in range(1, 4 + (1 if x == 1 else 0)):
                p.put(x, y, z, None)
    for z in range(2, L, 6):
        for y in range(1, 6):
            p.put(3, y, z, bone())
        for x in range(0, 3):
            top = 5 if x == 1 else 4
            p.put(x, top, z, bone("x"))
        p.put(0, 1, z, stair("polished_granite", "east", "top")) if False else None
    for z in range(5, L, 6):
        p.put(3, 3, z, LANTERN); p.put(3, 4, z, stair("polished_granite", "west", "top"))
    for z in range(0, L, 3):
        p.put(1, 4, z, lichen(up=True)) if p.get(1, 5, z) is not None and p.get(1, 4, z) is None else None
    p.cut_seams(floor="minecraft:pink_terracotta")
    p.mark("node-throat", (1, 1, 13), "south")
    p.mark("wrong-rib", (0, 1, 14), "east")
    return p


def rib_cathedral():
    """The rib cathedral: the chest, a vault of flesh near forty high with the ribs standing
    through it in white arcs across the way; lice-holes in the walls; the diaphragm, a wall of
    membrane, closing the way down at the south."""
    p = Place("rib-cathedral", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    flesh = p.role("flesh", FLESH)
    gut = p.role("gut", GUT)
    # the vault keeps the brief's height (fact/cathedral-height): its crown reaches the frame's top
    body_room(p, gut, flesh, H - 1, ribs_every=4, rib_axis="z", salt=21, cap=H - 1)
    # the ribs come down the walls to the floor as pilasters of bone
    for z in range(0, L, 4):
        for x in range(W):
            col = [y for y in range(1, H) if p.get(x, y, z) is None]
            if not col:
                continue
            if x in (1, W - 2) or (p.get(x - 1, 1, z) is not None or p.get(x + 1, 1, z) is not None):
                for y in range(1, max(col) + 2):
                    if p.get(x, y, z) is not None:
                        p.put(x, y, z, bone("y"))
    # the diaphragm: a membrane wall across the south end
    d = p.seam("diaphragm"); dlo, dhi = p.seam_box(d)
    for x in range(1, W - 1):
        for y in range(1, H - 1):
            if p.get(x, y, L - 2) is None:
                p.put(x, y, L - 2, "minecraft:nether_wart_block" if (x + y) % 3 else "minecraft:pink_terracotta")
    for x in range(dlo[0], dhi[0] + 1):
        for y in range(1, dhi[1] + 1):
            p.put(x, y, L - 2, None)
    # the arcade: columns of bone and flesh from floor to vault either side of the way, each
    # carrying a lamp in a niche under a lip of bone and lichen on its faces
    for k, z in enumerate(range(4, L - 3, 6)):
        for x in (9, 21):
            for y in range(1, H - 1):
                if p.get(x, y, z) is not None and y > 2:
                    break
                p.put(x, y, z, bone("y") if (y + k) % 5 else "minecraft:red_terracotta")
            ly = 3 + (k + x) % 3
            p.put(x, ly, z, LANTERN)
            p.put(x, ly + 1, z, stair("polished_granite", "south" if k % 2 else "north", "top"))
            for (dx, dz, f) in ((1, 0, "w"), (-1, 0, "e"), (0, 1, "n"), (0, -1, "s")):
                yy = 2 + (k * 3 + dx + dz) % 6
                c = (x + dx, yy, z + dz)
                if p.get(*c) is None:
                    p.put(*c, lichen(**{f: True}))
    # lice holes low in the walls
    for (x, z) in ((1, 7), (W - 2, 13), (1, 21), (W - 2, 27), (1, 30)):
        p.put(x, 1, z, "minecraft:mud")
    body_lights(p, 21, n_niche=24, n_vine=60, n_lichen=120, vine_floor=7, vine_len=26)
    p.cut_seams(floor=gut)
    p.mark("node-rib-cathedral", (15, 1, 17), "south")
    p.mark("diaphragm", (dhi[0] + 1, 1, L - 3), "south")
    p.mark("unlock-diaphragm", (dlo[0] + 2, 1, L - 3), "south")
    p.mark("cathedral-west-landing", (5, 1, 14), "south")
    p.mark("cathedral-east-landing", (25, 1, 14), "south")
    return p


def stomach():
    """The stomach: a black pool behind a curb of bone, and on its shore what earlier visitors
    left — the crew's lamps, a boot, a coil of rope, the sleepers' coats."""
    p = Place("stomach", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    flesh = p.role("flesh", GUT)
    body_room(p, "minecraft:brown_terracotta", flesh, H - 3, ribs_every=5, rib_axis="x", salt=31)
    # the pool: a basin of black water behind a curb of bone, east half
    for x in range(11, W - 2):
        for z in range(4, L - 4):
            p.put(x, 0, z, WATER)
            p.put(x, 1, z, WATER)
    for x in range(10, W - 1):
        for z in (3, L - 4):
            p.put(x, 1, z, bone("x"))
    for z in range(3, L - 3):
        p.put(10, 1, z, bone("z"))
        p.put(W - 2, 1, z, bone("z"))
    # what was left on the shore
    p.put(7, 1, 9, "minecraft:white_carpet"); p.put(6, 1, 10, "minecraft:gray_carpet")
    p.put(5, 1, 8, barrel("up"))
    p.put(8, 1, 11, chain("x")) if False else None
    p.put(4, 1, 12, LANTERN); p.put(9, 1, 6, LANTERN)
    p.put(12, 1, 2, "minecraft:leather_boots") if False else None
    body_lights(p, 31, n_niche=6, n_vine=10, n_lichen=30)
    p.cut_seams(floor="minecraft:brown_terracotta")
    p.mark("node-stomach", (8, 1, 13), "south")
    p.mark("stomach-shore", (8, 1, 9), "east")
    return p


def heart_chamber():
    """The heart chamber: the heart itself, a mass of muscle and vessel from floor to vault in
    the east half, its three valves in its west face; dark growth over the bone of the walls;
    the lamps Davey's dream did not put out."""
    p = Place("heart-chamber", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    wall = p.role("wall", HEARTWALL)
    body_room(p, "minecraft:black_terracotta", wall, H - 3, ribs_every=4, rib_axis="x", salt=41)
    # the heart: a mass from floor to vault, x 11..15, z 5..14, with its three valves on the west face
    for x in range(11, 16):
        for z in range(5, 15):
            r = ((x - 13) / 2.6) ** 2 + ((z - 9.5) / 5.2) ** 2
            if r <= 1.0:
                for y in range(1, H - 1):
                    p.put(x, y, z, "minecraft:nether_wart_block" if (x + y + z) % 4 else "minecraft:crimson_hyphae[axis=y]")
    for (x, z) in ((12, 4), (14, 15), (16, 9), (10, 12)):
        for y in range(1, H - 1):
            if p.get(x, y, z) is None:
                p.put(x, y, z, "minecraft:crimson_stem[axis=y]")
    # dark growth over the floor near the heart
    for x in range(2, W - 2):
        for z in range(2, L - 2):
            if h(x, z, 43) % 4 == 0 and p.get(x, 0, z) is not None:
                p.put(x, 0, z, "minecraft:cyan_terracotta")
    body_lights(p, 41, n_niche=10, n_vine=16, n_lichen=40)
    p.cut_seams(floor="minecraft:black_terracotta")
    p.mark("node-heart-chamber", (9, 1, 9), "east")
    p.mark("davey-heart", (9, 1, 12), "east")
    for i, nm in enumerate(("valve-west", "valve-middle", "valve-east")):
        z = 8 + i
        xs = [x for x in range(16) if p.get(x, 1, z) is not None and x >= 9]
        p.mark(nm, (min(xs) - 1, 1, z), "east")
    p.mark("unlock-heart-to-spine", (W - 2, 1, 9), "east")
    return p


def breach():
    """The breach: a short ragged tunnel out through a wound in the flank, flesh walls and
    the ends of ribs, from the heart to the spotter's ridge."""
    p = Place("breach", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    flesh = p.role("flesh", FLESH)
    p.box(0, 0, 0, W - 1, H - 1, L - 1, flesh)
    p.box(0, 0, 0, W - 1, 0, L - 1, "minecraft:red_terracotta")
    for x in range(W):
        for z in range(0, 3):
            for y in range(1, 4):
                p.put(x, y, z, None)
    for x in (2, 5, 8):
        p.put(x, 3, 2, bone("x")); p.put(x, 4, 1, bone("z"))
    for x in (3, 9):
        p.put(x, 2, 3, LANTERN); p.put(x, 3, 3, stair("polished_granite", "north", "top"))
    p.put(6, 3, 0, lichen(down=False, s=True)) if False else None
    p.cut_seams(floor="minecraft:red_terracotta")
    p.mark("node-breach", (5, 1, 1), "west")
    return p


def spine_stair():
    """The spine stair: up the inside of the neck on the vertebrae; a lane of flesh from the
    heart's door along the foot of the climb, then the flight of vertebra steps rising back
    the length of the neck to the blowhole, walled from the lane by the spine's own bone."""
    p = Place("spine-stair", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    flesh = p.role("flesh", FLESH)
    p.box(0, 0, 0, W - 1, H - 1, L - 1, flesh)
    d = p.seam("heart-to-spine"); dlo, dhi = p.seam_box(d)
    t = p.seam("spine-to-crown"); tlo, thi = p.seam_box(t)
    top = tlo[1]
    # the lane along x 0 from the heart's door to the stair's foot at the far end
    for z in range(dlo[2], L - 1):
        p.put(0, 0, z, "minecraft:pink_terracotta")
        for y in range(1, 4):
            p.put(0, y, z, None)
    # the foot: the lane turns into the flight at the south end
    for x in range(0, W):
        for y in range(1, 4):
            p.put(x, y, L - 2, None)
        p.put(x, 0, L - 2, "minecraft:pink_terracotta")
    xs = [2, 3]
    run = list(range(L - 3, 1, -1))       # from the foot northward to the top landing
    zs_top_first = list(reversed(run))
    flight(p, xs, zs_top_first, top, 1, "polished_granite", flesh, via="flight")
    for z in run:
        lvl = max([y for y in range(H) if (2, y, z) in p.struct and p.get(2, y, z) is not None and passable(p.get(2, y + 1, z))] + [0]) + 1
        for x in xs:
            for y in range(lvl, min(H - 1, lvl + 4)):
                p.put(x, y, z, None)
                if (x, y, z) not in p.cl and y >= lvl + 2:
                    p.cl[(x, y, z)] = "flight"
        for y in range(1, lvl + 3):
            p.put(1, y, z, bone() if z % 4 == 0 else flesh)
    stair_head(p, "top", 1, 1, 3, 1, top, "enclosed", flesh, top=top + 2)
    for x in (1, 2, 3):
        for y in range(top, top + 3):
            p.put(x, y, 1, None); p.put(x, y, 0, None)
    p.claim("top", 1, top, 1, 3, top + 2, 1)
    # vertebra rings: bone across the vault over the flight every fourth cell
    for z in range(2, L - 2, 4):
        for x in xs:
            col = [y for y in range(1, H) if p.get(x, y, z) is None]
            if col:
                p.put(x, max(col) + 1, z, bone("x"))
    for z in range(4, L - 3, 7):
        lvl = max([y for y in range(H) if p.get(3, y, z) is None] + [3])
        if p.get(3, lvl, z) is None and lvl - 1 >= 2:
            pass
        wy = lvl - 1
        if p.inb(3, wy, z) and p.get(3, wy, z) is None:
            pass
    for z in range(6, L - 3, 6):
        # a lamp in the outer wall beside the flight, its lip of bone over it
        col = [y for y in range(1, H) if p.get(3, y, z) is None]
        if col:
            y = min(col) + 1
            p.put(W - 1, y, z, LANTERN) if W - 1 > 3 else None
    for z in range(dlo[2] + 3, L - 2, 8):
        p.put(1, 2, z, LANTERN)
    for z in range(3, L - 3, 4):
        col = [y for y in range(1, H - 1) if p.get(2, y, z) is None]
        if col:
            ly = min(col) + 1
            p.put(1, ly, z, LANTERN)
    p.stair_edge("flight", "room", "top")
    p.seam_space = {"way-spine-to-crown": "top"}
    p.cut_seams(floor=flesh)
    p.mark("node-spine-stair", (0, 1, 28), "south")
    return p


def hide_floor(p, role, salt):
    W, L = p.W, p.L
    for x in range(W):
        for z in range(L):
            p.put(x, 0, z, role)
            if h(x, z, salt) % 23 == 0:
                p.put(x, 0, z, "minecraft:light_gray_concrete")


def wound(p, x0, z0, w, l, salt):
    """A wound in the hide: red flesh in a hollow, ribs standing out of it, a crew lamp set in
    its lip, one rib arched over the hollow's end."""
    for x in range(x0, x0 + w):
        for z in range(z0, z0 + l):
            p.put(x, 0, z, "minecraft:red_terracotta" if h(x, z, salt) % 3 else "minecraft:nether_wart_block")
    for i, x in enumerate(range(x0, x0 + w, 2)):
        ht = 2 + (i % 2)
        for y in range(1, ht + 1):
            p.put(x, y, z0, bone())
    for x in range(x0, x0 + w):
        p.put(x, 4, z0 + l - 1, bone("x"))
    for y in range(1, 4):
        p.put(x0, y, z0 + l - 1, bone()); p.put(x0 + w - 1, y, z0 + l - 1, bone())
    p.put(x0 + w // 2, 1, z0 + 1, LANTERN)


def back_place(stem, salt, mud=False):
    """A stretch of the back: wrinkled grey hide falling a step at a time toward the tail,
    the line of knuckles along the spine ridge beside the way, sloughed skin, a wound with
    its ribs; the stair down from the step above at the north door."""
    def build():
        p = Place(stem, envelope="open")
        W, H, L = p.W, p.H, p.L
        if mud:
            role = p.role("mud", BANKMUD)
            # no standing pools: the tail bank runs past the end of the far bank's ground,
            # and a pool there would drain into the sea (DW0322)
            mud_floor(p, role, 0.0, salt)
        else:
            role = p.role("hide", HIDE)
            hide_floor(p, role, salt)
        n = p.seam([s["edge"].split("/", 1)[1] for s in p.seams if s["face"] == "north"][0])
        nlo, nhi = p.seam_box(n)
        if nlo[1] > 1:
            xs = list(range(nlo[0], nhi[0] + 1))
            q = nlo[1]
            stair_head(p, "head", xs[0], 1, xs[-1], 1, q, "open", role)
            run = list(range(2, 2 + q))
            flight(p, xs, run, q, 1, "polished_andesite" if not mud else "blackstone", role, via="steps")
            for z in range(0, 2 + q):
                for x in (xs[0] - 1, xs[-1] + 1):
                    lv = max([y for y in range(H) if (xs[0], y, z) in p.struct] + [0])
                    for y in range(1, lv + 1):
                        p.put(x, y, z, role)
            # the step the back falls by: the hide stands up behind the stair to its head
            for x in range(W):
                if xs[0] - 1 <= x <= xs[-1] + 1:
                    continue
                for y in range(1, q):
                    p.put(x, y, 0, role)
            p.stair_edge("steps", "room", "head")
            p.seam_space = {"way-" + n["edge"].split("/", 1)[1]: "head"}
        if not mud:
            # knuckles of the spine ridge along the east side of the way
            for z in range(4, L - 2, 5):
                for y in range(1, 3):
                    p.put(22, y, z, "minecraft:gray_terracotta")
                p.put(22, 3, z, bone("y")) if z % 10 == 4 else None
            for (x, z) in ((5, 8), (9, 20), (26, 25)):
                for dx in range(3):
                    for dz in range(2):
                        p.put(x + dx, 0, z + dz, "minecraft:light_gray_concrete")
        wound(p, 3 + salt % 4, 12 + salt % 5, 5, 5, salt)
        for (x, z) in ((10, 4), (20, 9), (12, 26), (24, 20), (4, 28), (27, 4), (8, 16), (18, 16), (28, 13), (14, 9), (2, 4)):
            low_lamp(p, x, z)
        p.cut_seams(floor=role)
        p.mark(f"node-{stem}", (14, 1, 16), "south")
        return p
    return build


def crown():
    """The Crown: the top of the head, wrinkled hide forty blocks over the flat, the blowhole's
    lip where the spine stair comes up, sloughed skin; the town's lights to the north; the
    tentacles stand out of the wounds round it, the way to the Brow passing between them."""
    p = Place("crown", envelope="open")
    W, H, L = p.W, p.H, p.L
    hide = p.role("hide", HIDE)
    hide_floor(p, hide, 51)
    s = p.seam("spine-to-crown"); slo, shi = p.seam_box(s)
    # the blowhole's lip: a ridge of hide round the spine's mouth, a hood of it over the way out
    for x in range(slo[0] - 1, shi[0] + 2):
        for z in (L - 4, L - 3):
            if not (slo[0] <= x <= shi[0]):
                for y in (1, 2):
                    p.put(x, y, z, "minecraft:gray_terracotta")
    for x in range(slo[0] - 1, shi[0] + 2):
        p.put(x, 3, L - 4, slab("polished_blackstone", "top"))
    for x in (slo[0] - 1, shi[0] + 1):
        p.put(x, 1, L - 4, "minecraft:gray_terracotta"); p.put(x, 2, L - 4, "minecraft:gray_terracotta")
    # three wounds round the top, ribs out of them
    for (x0, z0) in ((0, 2), (11, 10), (0, 18)):
        for x in range(x0, x0 + 4):
            for z in range(z0, z0 + 3):
                p.put(x, 0, z, "minecraft:red_terracotta")
        p.put(x0, 1, z0, bone()); p.put(x0, 2, z0, bone()); p.put(x0 + 3, 1, z0 + 2, bone())
    for (x, z) in ((5, 2), (10, 3), (5, 9), (9, 15), (13, 20), (6, 21), (1, 17), (14, 14)):
        low_lamp(p, x, z)
    p.cut_seams(floor=hide)
    p.mark("node-crown", (7, 1, 11), "north")
    p.mark("crown-landing-1", (2, 1, 9), "north")
    p.mark("crown-landing-2", (13, 1, 4), "north")
    p.mark("crown-landing-3", (2, 1, 13), "north")
    return p


def brow():
    """The Brow: the front of the head, and driven into it the Brow Stone, a tall pale carved
    tablet standing up out of the hide at the forehead's edge; the pictures on its face."""
    p = Place("brow", envelope="open")
    W, H, L = p.W, p.H, p.L
    hide = p.role("hide", HIDE)
    hide_floor(p, hide, 61)
    # the tablet: quartz and calcite, carved, three wide, rising out of the hide at the north edge
    for x in range(3, 9):
        for y in range(1, H - 1):
            p.put(x, y, 0, "minecraft:quartz_bricks" if (x + y) % 3 else "minecraft:chiseled_quartz_block")
        p.put(x, H - 1, 0, slab("smooth_quartz")) if False else None
    for x in (3, 8):
        for y in range(1, H - 1):
            p.put(x, y, 0, "minecraft:quartz_pillar[axis=y]")
    for x in range(4, 8):
        p.put(x, 1, 1, "minecraft:calcite")
    p.put(5, 1, 1, None); p.put(6, 1, 1, None)
    # a lip of hide folded over the tablet's west foot
    p.put(1, 3, 1, slab("polished_blackstone", "top")); p.put(1, 3, 2, slab("polished_blackstone", "top"))
    p.put(0, 1, 1, "minecraft:gray_terracotta"); p.put(0, 2, 1, "minecraft:gray_terracotta")
    p.put(0, 1, 2, "minecraft:gray_terracotta"); p.put(0, 2, 2, "minecraft:gray_terracotta")
    for (x, z) in ((2, 5), (9, 5), (5, 9), (10, 1)):
        low_lamp(p, x, z)
    p.cut_seams(floor=hide)
    p.mark("node-brow", (6, 1, 5), "north")
    p.mark("brow-stone", (5, 1, 1), "north")
    return p


def tail_road():
    """The road behind the tail: a strip of the bank from behind the flukes out to the east,
    the crew's lamp stakes along it, a lean-to of theirs."""
    p = Place("tail-road", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", BANKMUD)
    mud_floor(p, mud, 0.03, 81)
    for x in range(4, W - 2, 8):
        stake(p, x, 0 if (x // 8) % 2 else L - 1)
    for x in range(20, 24):
        p.put(x, 3, L - 1, slab("spruce", "top")); p.put(x, 3, L - 2, slab("spruce", "top"))
    p.put(21, 2, L - 1, LANTERN_HANG)
    for y in (1, 2):
        p.put(20, y, L - 1, fence("spruce")); p.put(23, y, L - 1, fence("spruce"))
    p.cut_seams(floor=mud)
    p.mark("node-tail-road", (23, 1, 3), "east")
    return p


def run_bank():
    """The run bank: the long bank east of the body down to the landing, Marrack's crew's lamp
    stakes along it; halfway, their tarp over a cache."""
    p = Place("run-bank", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", BANKMUD)
    mud_floor(p, mud, 0.03, 91)
    for z in range(6, L - 2, 12):
        stake(p, 0 if (z // 12) % 2 else W - 1, z)
    for z in range(134, 142):
        for x in range(4, W):
            p.put(x, 0, z, mud)
    for z in range(136, 140):
        p.put(W - 1, 3, z, slab("spruce", "top")); p.put(W - 2, 3, z, slab("spruce", "top"))
    for y in (1, 2):
        p.put(W - 1, y, 136, fence("spruce")); p.put(W - 1, y, 139, fence("spruce"))
    litter(p, 1, 2, W - 2, L - 3, 97, 30, keep={(x, z) for x in range(4, W) for z in range(133, 143)})
    p.cut_seams(floor=mud)
    p.mark("node-run-bank", (3, 1, 137), "north")
    return p


BUILDERS = {
    "mouth": mouth, "throat": throat, "rib-cathedral": rib_cathedral, "stomach": stomach,
    "heart-chamber": heart_chamber, "breach": breach, "spine-stair": spine_stair,
    "crown": crown, "brow": brow,
    "back-upper": back_place("back-upper", 3), "back-middle": back_place("back-middle", 5),
    "back-lower": back_place("back-lower", 7), "tail-flank": back_place("tail-flank", 9),
    "tail-bank": back_place("tail-bank", 11, mud=True), "tail-road": tail_road, "run-bank": run_bank,
}

if __name__ == "__main__":
    kit.main(BUILDERS)
