"""Acts 2-4 on the far side: the body's bank, the inside of the body, and its back.

Inside: every place is cut out of the body form whole, so its piece draws the
body's flesh itself — a cavity of red-brown flesh with ribs of bone, lit by what
grows in it (glow lichen on the walls, glow berries hanging from the vault,
shroomlight set into the vault where the flesh is thin) and by the lamps earlier
visitors left, each recessed behind a slab so the light shows and the fixture
does not (docs/reference/interior-lighting.md §7). Outside: the places on the
back are slices of the sculpted piece, with only what stands in its air added.
"""

import math

import mapmodel as M
import body as B
from kit import Piece, AIR, boxcells, ground, seam_box, INWARD
from blocks import S, stairs, slab, is_full
import arch
from common import (leftovers_no_body, space_claim, node_mark, station_mark, stations, wall_seams,
                    shell_box, lantern_post, standable)
from places_town import rng, mix, COBBLE, STONE, MOSSY, PLANK, DARK, FENCE, DFENCE, PACKED
from places_flat import MUD, WET, ledge_ring, stake, WATER

FLESH = [(S("minecraft:nether_wart_block"), 5), (S("minecraft:red_nether_bricks"), 2),
         (S("minecraft:red_terracotta"), 2), (S("minecraft:brown_terracotta"), 1),
         (S("minecraft:crimson_hyphae", axis="y"), 1)]
DARK_FLESH = [(S("minecraft:red_terracotta"), 2), (S("minecraft:brown_terracotta"), 2),
              (S("minecraft:nether_wart_block"), 2), (S("minecraft:mud_bricks"), 1)]
HIDE = [(S("minecraft:tuff"), 2), (S("minecraft:cobbled_deepslate"), 2), (S("minecraft:deepslate"), 1)]
BONE_Y = S("minecraft:bone_block", axis="y")
BONE_X = S("minecraft:bone_block", axis="x")
BONE_Z = S("minecraft:bone_block", axis="z")
SHROOM = S("minecraft:shroomlight")


def glow_lichen(face_toward):
    """lichen on the face of the block in direction `face_toward` from its cell"""
    props = {d: "false" for d in ("down", "east", "north", "south", "up", "west")}
    props[face_toward] = "true"
    return S("minecraft:glow_lichen", **props, waterlogged=False)


def cave_vine(berries=True, tip=False):
    if tip:
        return S("minecraft:cave_vines", age=25, berries=berries)
    return S("minecraft:cave_vines_plant", berries=berries)


# -- a flesh room -----------------------------------------------------------
def flesh_fill(pc, r, palette=FLESH):
    for c in boxcells((0, 0, 0), (pc.X - 1, pc.Y - 1, pc.Z - 1)):
        if pc.owned(c):
            pc.set(*c, mix(r, palette))


def carve(pc, cells):
    for c in cells:
        if pc.owned(c):
            pc.set(*c, AIR)


def dome_cells(pc, box=None, y_floor=None, height=None, inset=0):
    """the cavity of a dome over the play space: an ellipsoid whose equator is
    the floor, so its walls rise sheer and close overhead"""
    (sx0, sy0, sz0), (sx1, sy1, sz1) = box or pc.space
    yf = pc.dy if y_floor is None else y_floor
    h = (sy1 - yf + 1) if height is None else height
    cx, cz = (sx0 + sx1) / 2.0, (sz0 + sz1) / 2.0
    rx, rz = (sx1 - sx0) / 2.0 + 0.5 - inset, (sz1 - sz0) / 2.0 + 0.5 - inset
    out = []
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            for y in range(yf, yf + h):
                v = ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2 + ((y - yf + 0.5) / (h + 0.25)) ** 2
                if v <= 1.0:
                    out.append((x, y, z))
    return out


def light_surfaces(pc, r, cavity, every=5, shroom_every=11, vine_every=9):
    """natural light set into the surface: lichen on walls and vault, berries
    hanging from the vault, shroomlight embedded where the vault is thin"""
    cav = set(cavity)
    k = 0
    for (x, y, z) in sorted(cav):
        if (x, y, z) in pc.prog.region:
            continue
        k += 1
        h = (x * 73856093 ^ y * 19349663 ^ z * 83492791) & 0xFFFF
        # the vault over this cell
        if (x, y + 1, z) not in cav and pc.owned((x, y + 1, z)) and is_full(pc.get(x, y + 1, z)):
            if h % shroom_every == 0 and y > pc.dy + 3:
                pc.set(x, y + 1, z, SHROOM)
            elif h % vine_every == 1 and y > pc.dy + 4 and (x, y - 1, z) in cav:
                pc.set(x, y, z, cave_vine(True, tip=False))
                if (x, y - 1, z) in cav and y - 1 > pc.dy + 2:
                    pc.set(x, y - 1, z, cave_vine(True, tip=True))
                else:
                    pc.set(x, y, z, cave_vine(True, tip=True))
            elif h % every == 2:
                pc.set(x, y, z, glow_lichen("up"))
            continue
        for d, (dx, dz) in (("north", (0, -1)), ("south", (0, 1)), ("west", (-1, 0)), ("east", (1, 0))):
            n = (x + dx, y, z + dz)
            if n not in cav and pc.owned(n) and is_full(pc.get(*n)) and pc.get(x, y, z) == AIR:
                if h % every == 3 and y > pc.dy:
                    pc.set(x, y, z, glow_lichen(d))
                break


def recessed_lamp(pc, wall_cell, room_dir, lamp=None, fam="red_nether_brick"):
    """a lamp one block behind the surface, a slab of the flesh in front, the
    slot beside it letting the light out"""
    x, y, z = wall_cell
    dx, dz = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}[room_dir]
    pc.set(x - dx, y, z - dz, lamp or arch.lantern(False))
    pc.set(x, y, z, slab(fam, "top"))
    pc.set(x, y - 1, z, AIR) if False else None


def ribs(pc, cavity, axis, positions, thick=1):
    """arcs of bone set into the flesh skin round the cavity, across `axis` at
    each position: the rib is the wall's own surface, so it makes no ledge"""
    cav = set(cavity)
    for (x, y, z) in list(cav):
        if (z if axis == "z" else x) not in [q + t for q in positions for t in range(thick)]:
            continue
        nbrs = ((1, 0, 0), (-1, 0, 0), (0, 1, 0)) if axis == "z" else ((0, 0, 1), (0, 0, -1), (0, 1, 0))
        for dx, dy, dz in nbrs:
            n = (x + dx, y + dy, z + dz)
            if n not in cav and pc.owned(n) and is_full(pc.get(*n)) and n not in pc.prog.region and n[1] >= pc.dy:
                pc.set(*n, BONE_Y if dy == 0 else (BONE_X if axis == "z" else BONE_Z))


def tunnels(pc, depth=4):
    """the way in from each wall seam carried into the room: its cells cut
    straight in, `depth` deep, so every opening meets the cavity"""
    out = []
    for sm in pc.seams:
        if sm["face"] in ("up", "down") or sm.get("rise", 0) != 0:
            continue
        (x0, y0, z0), (x1, y1, z1) = sm["cells"]
        ix, _, iz = INWARD[sm["face"]]
        for d in range(0, depth + 1):
            for c in boxcells((x0 + ix * d, y0, z0 + iz * d), (x1 + ix * d, y1, z1 + iz * d)):
                if pc.owned(c) and c not in pc.prog.region:
                    pc.set(*c, AIR)
                    out.append(c)
        # the floor under the tunnel
        for d in range(0, depth + 1):
            for c in boxcells((x0 + ix * d, y0 - 1, z0 + iz * d), (x1 + ix * d, y0 - 1, z1 + iz * d)):
                if pc.owned(c) and not is_full(pc.get(*c)):
                    pc.set(*c, S("minecraft:nether_wart_block"))
    return out


def claim_room(pc, name="room", envelope="enclosed"):
    space_claim(pc, name, envelope)
    node_mark(pc)
    stations(pc)
    leftovers_no_body(pc, reason="ledges of flesh and bone a body could climb to and nobody walks")


# ---------------------------------------------------------------------------
def mouth(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    flesh_fill(pc, r)
    cav = dome_cells(pc)
    carve(pc, cav)
    cav += tunnels(pc)
    # the tongue: a long low swell of flesh down the middle of the floor
    for x in range(sx0 + 6, sx1 - 5):
        for z in range(sz0 + 3, sz1 - 2):
            pc.set(x, fy - 1, z, S("minecraft:nether_wart_block"))
    for z in range(sz0 + 5, sz1 - 3):
        for x in range(sx0 + 8, sx1 - 7):
            if pc.get(x, fy, z) == AIR:
                pc.set(x, fy, z, slab("red_nether_brick", "bottom"))
    built = wall_seams(pc, "room", fill=S("minecraft:nether_wart_block"))
    # teeth like posts round the way in, on the outside face
    door = [c for b in built.values() for c in b["cells"] if c[2] == 0]
    xs = sorted({c[0] for c in door})
    ys = sorted({c[1] for c in door})
    for x in range(xs[0] - 3, xs[-1] + 4, 2):
        for y in (ys[-1] + 1, ys[-1] + 2):
            if pc.owned((x, y, 0)) and (x, y, 0) not in pc.prog.region:
                pc.set(x, y, 0, BONE_Y)
    for x in (xs[0] - 1, xs[-1] + 1):
        for y in ys:
            pc.set(x, y, 0, BONE_Y)
    # teeth inside the lip, down both sides of the tongue
    for z in range(sz0 + 1, sz0 + 6, 2):
        for x in (sx0 + 3, sx1 - 3):
            if (x, fy, z) in set(cav):
                pc.set(x, fy, z, BONE_Y)
    light_surfaces(pc, r, cav)
    for (wx, wz, d) in [(sx0 + 2, sz1 - 3, "east"), (sx1 - 2, sz1 - 4, "west")]:
        if pc.get(wx, fy + 1, wz) == AIR:
            pass
    claim_room(pc)
    return pc.finish("room")


def throat(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    flesh_fill(pc, r)
    cx = (sx0 + sx1) / 2.0
    cav = []
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            for y in range(fy, sy1 + 1):
                dx = (x - cx) / ((sx1 - sx0) / 2.0 + 0.5)
                dy = (y - fy + 0.5) / (sy1 - fy + 1.25)
                if dx * dx + dy * dy <= 1.0:
                    cav.append((x, y, z))
    carve(pc, cav)
    cav += tunnels(pc)
    # a corridor of ribs, every six blocks the same
    ribs(pc, cav, "z", list(range(sz0 + 2, sz1, 6)))
    light_surfaces(pc, r, cav, every=4, shroom_every=97, vine_every=97)
    # Marrack's chalk-marked lanterns, set back into the flesh between the ribs
    for z in range(sz0 + 5, sz1, 6):
        for x, d in ((sx0, "east"), (sx1, "west")):
            wall = (x - 1, fy + 1, z) if d == "east" else (x + 1, fy + 1, z)
            if pc.owned(wall):
                pc.set(*wall, S("minecraft:red_nether_brick_slab", type="top", waterlogged=False)) if False else None
    wall_seams(pc, "room", fill=S("minecraft:nether_wart_block"))
    claim_room(pc)
    return pc.finish("room")


def rib_cathedral(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    flesh_fill(pc, r)
    cav = dome_cells(pc)
    carve(pc, cav)
    cav += tunnels(pc)
    # the vault of ribs
    ribs(pc, cav, "z", list(range(sz0 + 3, sz1 - 2, 5)), thick=1)
    # the two roof wounds: holes torn up through the vault to the sky
    for (wx, wz) in B.ROOF_WOUNDS:
        lx, _, lz = pc.L(wx, 0, wz)
        for x in range(lx - 3, lx + 4):
            for z in range(lz - 3, lz + 4):
                if (x - lx) ** 2 + (z - lz) ** 2 <= 9:
                    for y in range(fy + 1, pc.Y):
                        if pc.owned((x, y, z)) and pc.get(x, y - 1, z) == AIR and pc.get(x, y, z) != AIR:
                            pc.set(x, y, z, AIR)
                            cav.append((x, y, z))
    built = wall_seams(pc, "room", fill=S("minecraft:nether_wart_block"),
                       bar_block=S("minecraft:nether_wart_block"))
    light_surfaces(pc, r, cav, every=4, shroom_every=9, vine_every=7)
    claim_room(pc, envelope="open")
    return pc.finish("room")


def stomach(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    flesh_fill(pc, r, DARK_FLESH)
    cav = dome_cells(pc)
    carve(pc, cav)
    cav += tunnels(pc)
    # the black pool behind a curb of bone, in the chamber's east part
    px0, px1, pz0, pz1 = sx1 - 9, sx1 - 2, sz0 + 4, sz1 - 4
    for x in range(px0, px1 + 1):
        for z in range(pz0, pz1 + 1):
            edge = x in (px0, px1) or z in (pz0, pz1)
            if (x, fy, z) not in set(cav):
                continue
            if edge:
                pc.set(x, fy, z, BONE_Y)
            else:
                pc.set(x, fy - 1, z, WATER)
    # what earlier visitors left on its shore
    shore = pc.L(*M.STATIONS["anchor/stomach-shore"][:3])
    for (x, z, b) in [(sx0 + 3, sz0 + 6, arch.lantern(False)), (sx0 + 5, sz0 + 8, S("minecraft:brown_carpet")),
                      (sx0 + 4, sz0 + 10, S("minecraft:gray_carpet")), (sx0 + 7, sz0 + 12, S("minecraft:cobweb")),
                      (sx0 + 9, sz0 + 5, BARREL_OPEN)]:
        if (x, fy, z) in set(cav):
            pc.set(x, fy, z, b)
    built = wall_seams(pc, "room", fill=S("minecraft:nether_wart_block"))
    light_surfaces(pc, r, cav, every=4, shroom_every=8, vine_every=8)
    claim_room(pc)
    return pc.finish("room")


BARREL_OPEN = S("minecraft:barrel", facing="up", open=True)


def heart_chamber(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    flesh_fill(pc, r)
    cav = dome_cells(pc)
    carve(pc, cav)
    cav += tunnels(pc)
    cavs = set(cav)
    # sculk grown over bone like flesh: the floor, veins up the walls
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            if (x, fy, z) in cavs:
                pc.set(x, fy - 1, z, S("minecraft:sculk"))
    # the heart against the south wall, three valves in its face
    hz0 = sz1 - 4
    for x in range(sx0 - 1, sx1 + 2):
        for z in range(hz0, sz1 + 2):
            for y in range(fy, fy + 8):
                if (x, y, z) not in cavs and pc.owned((x, y, z)) and ((x - (sx0 + sx1) / 2) ** 2 / 30 + (y - fy - 3) ** 2 / 14 + (z - sz1) ** 2 / 20) <= 1.6:
                    pc.set(x, y, z, mix(r, [(S("minecraft:nether_wart_block"), 3), (S("minecraft:red_mushroom_block", down=True, east=True, north=True, south=True, up=True, west=True), 1), (S("minecraft:crimson_hyphae", axis="y"), 1)]))
    # sensors at every few steps across the floor, the shrieker in the dark
    for (dx, dz) in [(2, 3), (5, 6), (8, 4), (3, 9), (9, 9), (6, 12)]:
        x, z = sx0 + dx, sz0 + dz
        if (x, fy, z) in cavs and pc.get(x, fy, z) == AIR:
            pc.set(x, fy, z, S("minecraft:sculk_sensor", power=0, sculk_sensor_phase="inactive", waterlogged=False))
    sx_, sz_ = sx0 + 1, sz0 + 1
    if (sx_, fy, sz_) in cavs:
        pc.set(sx_, fy, sz_, S("minecraft:sculk_shrieker", can_summon=False, shrieking=False, waterlogged=False))
    built = wall_seams(pc, "room", fill=S("minecraft:nether_wart_block"), bar_block=S("minecraft:bone_block", axis="y"))
    light_surfaces(pc, r, cav, every=4, shroom_every=9, vine_every=9)
    # the lanterns Davey's dream did not put out
    for (x, z) in [(sx0, sz0 + 6), (sx1, sz0 + 3)]:
        if (x, fy, z) in cavs:
            pc.set(x, fy, z, arch.lantern(False))
    claim_room(pc)
    return pc.finish("room")


def breach(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    flesh_fill(pc, r, FLESH)
    # outside the body the tunnel's walls are the torn hide hanging off the wound
    for c in boxcells((0, 0, 0), (pc.X - 1, pc.Y - 1, pc.Z - 1)):
        wx, wy, wz = pc.W(*c)
        if wx < 150 and pc.owned(c) and c[1] > 0:
            pc.set(*c, mix(r, HIDE))
    cav = []
    for x in range(sx0, sx1 + 1):
        for z in range(sz0 + 1, sz1):
            for y in range(fy, fy + 3):
                cav.append((x, y, z))
    carve(pc, cav)
    cav += tunnels(pc)
    for x in range(sx0, sx1 + 1):
        for z in range(sz0 + 1, sz1):
            pc.set(x, fy - 1, z, S("minecraft:mud") if pc.W(x, 0, 0)[0] < 150 else S("minecraft:nether_wart_block"))
    wall_seams(pc, "room", fill=S("minecraft:nether_wart_block"))
    light_surfaces(pc, r, cav, every=3, shroom_every=97, vine_every=97)
    pc.set(sx0 + 7, fy + 2, sz0 + 1, SHROOM) if False else None
    claim_room(pc)
    return pc.finish("room")


def spine_stair(node):
    """the lower neck: a tall slot of flesh from the heart's door, the vertebra
    stair climbing its north end into the upper neck"""
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    flesh_fill(pc, r)
    cav = []
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            for y in range(fy, sy1 + 1):
                cav.append((x, y, z))
    carve(pc, cav)
    ribs(pc, cav, "z", list(range(sz0 + 2, sz1, 4)))
    wall_seams(pc, "room", tread_fam="polished_diorite", fill=S("minecraft:bone_block", axis="y"))
    cav += tunnels(pc)
    light_surfaces(pc, r, cav, every=3, shroom_every=11, vine_every=97)
    claim_room(pc)
    return pc.finish("room")


def spine_top(node):
    """the upper neck: the vertebra stair climbs north to the first course under
    the blowhole, where a body arrives in the hole and steps up onto the crown"""
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    flesh_fill(pc, r)
    up = [s for s in pc.seams if s["face"] == "up"][0]
    (ax, ay, az), (bx, by, bz) = up["cells"]
    top = ay
    hz0, hz1 = min(az, bz), max(az, bz)
    hx0, hx1 = min(ax, bx), max(ax, bx)
    cav = [c for c in boxcells((sx0, fy, sz0), (sx1, sy1, sz1))]
    carve(pc, cav)
    # the treads climb north, the top one in the blowhole's north row
    rows = {hz0 + k: top - k for k in range(0, top - fy + 1)}
    for z in range(sz0, hz0):
        for x in range(sx0, sx1 + 1):
            for y in range(fy, sy1 + 1):
                pc.set(x, y, z, mix(r, FLESH))
    for z, ty in rows.items():
        for x in range(sx0, sx1 + 1):
            pc.set(x, ty, z, stairs("polished_diorite", "north"))
            for yy in range(fy - 1, ty):
                pc.set(x, yy, z, mix(r, FLESH))
    hole = set((x, top, z) for x in range(hx0, hx1 + 1) for z in range(hz0, hz1 + 1))
    opening, landing, flight = sorted(hole), [], []
    for z, ty in rows.items():
        for x in range(sx0, sx1 + 1):
            if ty == top:
                if (x, ty, z) not in hole:
                    landing.append((x, ty, z))
            elif ty >= top - 2:
                landing += [c for c in [(x, yy, z) for yy in range(ty, top + 1)] if c not in hole]
            elif ty >= fy + 1:
                flight += [(x, yy, z) for yy in range(ty, min(ty + 4, sy1 + 1))]
    pc.claim(opening, "door-spine-to-crown")
    pc.claim(landing, "landing-spine-to-crown")
    pc.claim([c for c in flight if c not in landing and c not in hole], "flight-spine-to-crown")
    pc.space_decl("landing-spine-to-crown", "open")
    pc.edge(a="room", b="landing-spine-to-crown", **{"class": "stair"}, rise=(top - 2) - fy,
            via="flight-spine-to-crown")
    pc.edge(a="landing-spine-to-crown", b="exterior", **{"class": "stair"}, rise=0, via="door-spine-to-crown")
    wall_seams(pc, "room", fill=S("minecraft:nether_wart_block"))
    cav += tunnels(pc)
    light_surfaces(pc, r, [c for c in cav if pc.get(*c) == AIR], every=3, shroom_every=11, vine_every=97)
    space_claim(pc, "room", "enclosed")
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("room")


# -- the bank ---------------------------------------------------------------
def bank_place(node, extra=None, sides=None, stakes=None):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, WET), lambda x, z: PACKED)
    wall_seams(pc, "bank", fill=PACKED)
    if sides:
        ledge_ring(pc, r, sides=sides)
    if extra:
        extra(pc, r)
    stations(pc)
    space_claim(pc, "bank", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc, reason="the tops of the crew's lamp stakes and what lies on the bank")
    return pc.finish("bank", shown_faces=["north", "south", "east", "west"])


def far_landing(node):
    def extra(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        for (x, z) in [(sx0 + 4, sz0 + 3), (sx1 - 3, sz0 + 6), (sx0 + 10, sz1 - 2)]:
            stake(pc, x, z)
    return bank_place(node, extra, sides=("west",))


def jaw_bank(node):
    def extra(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        # the tentacles' pits either side of the mouth, holes of black water
        for aid in ("anchor/jaw-west-pit", "anchor/jaw-east-pit"):
            px, py, pz = pc.L(*M.STATIONS[aid][:3])
            for x in range(px - 2, px + 3):
                for z in range(pz - 2, pz + 3):
                    if abs(x - px) + abs(z - pz) <= 3 and (x, fy, z) not in pc.prog.region:
                        pc.set(x, fy - 1, z, WATER)
                        pc.set(x, fy - 2, z, MUD)
        # the lower jaw slung under the head, lying open on the mud, its peg teeth
        jx0, jx1 = pc.L(172, 0, 0)[0], pc.L(183, 0, 0)[0]
        for z in range(sz1 - 12, sz1 + 1):
            for x in (jx0, jx1):
                pc.set(x, fy - 1, z, mix(r, [(S("minecraft:nether_wart_block"), 2), (S("minecraft:red_terracotta"), 1)]))
                if z % 3 == 0:
                    pc.set(x, fy, z, BONE_Y)
        # the crew's lamps on the bank
        for (x, z) in [(sx0 + 3, sz0 + 2), (sx0 + 22, sz0 + 3), (sx1 - 4, sz0 + 9)]:
            stake(pc, x, z)
    return bank_place(node, extra)


def flank_ridge(node):
    def extra(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        # a low ridge of mud: a course higher down its spine
        for z in range(sz0 + 1, sz1):
            for x in range(sx0 + 3, sx1 - 2):
                pc.set(x, fy - 1, z, mix(r, [(MUD, 3), (PACKED, 1)]))
        for z in range(sz0 + 8, sz1, 24):
            stake(pc, sx0 + 1, z)
    return bank_place(node, extra, sides=("west",))


def run_bank(node):
    def extra(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        # Marrack's crew's lamp stakes along the bank: the markers the Run passes
        for z in range(sz0 + 6, sz1, 16):
            stake(pc, sx1, z)
    return bank_place(node, extra, sides=("east",))


def tail_bank(node):
    return bank_place(node, None, sides=("south",))


def tail_road(node):
    return bank_place(node, None, sides=("south", "east"))


# -- on the body ------------------------------------------------------------
def body_slice(pc):
    """the sculpted body's own blocks in this place's frame (air where it has none)"""
    cells = B.cells()
    for c in boxcells((0, 0, 0), (pc.X - 1, pc.Y - 1, pc.Z - 1)):
        if pc.owned(c):
            pc.set(*c, cells.get(pc.W(*c), AIR))


def on_body(node, extra=None):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    body_slice(pc)
    # the walk plane is the hide's own: where the body's top dips, a course of hide
    for x in range(sx0 - 1, sx1 + 2):
        for z in range(sz0 - 1, sz1 + 2):
            if pc.owned((x, fy - 1, z)) and not is_full(pc.get(x, fy - 1, z)):
                pc.set(x, fy - 1, z, mix(r, HIDE))
            for y in range(fy, pc.Y):
                if pc.owned((x, y, z)) and pc.get(x, y, z) != AIR and (x, y, z) not in pc.prog.region:
                    pc.set(x, y, z, AIR)
    wall_seams(pc, "back", tread_fam="cobbled_deepslate", fill=S("minecraft:cobbled_deepslate"))
    if extra:
        extra(pc, r)
    stations(pc)
    space_claim(pc, "back", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc, reason="the hide's ridges and the tops of the steps")
    return pc.finish("back", shown_faces=["north", "south", "east", "west", "up"])


def crown(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    body_slice(pc)
    for x in range(0, pc.X):
        for z in range(0, pc.Z):
            if pc.owned((x, fy - 1, z)):
                pc.set(x, fy - 1, z, pc.get(x, fy - 1, z) if is_full(pc.get(x, fy - 1, z)) else mix(r, HIDE))
            for y in range(fy, pc.Y):
                if pc.owned((x, y, z)):
                    pc.set(x, y, z, AIR)
    # the blowhole: the hole the spine stair comes up through, and the well
    # the climber's head passes under its rim
    for s in pc.seams:
        if s["face"] == "down":
            (ax, ay, az), (bx, by, bz) = s["cells"]
            cells = list(boxcells((ax, ay, az), (bx, by, bz)))
            zs = sorted({c[2] for c in cells})
            well = [(x, y, z + k) for (x, y, z) in cells if z == zs[-1] for k in (1, 2)]
            for c in cells + well:
                pc.set(*c, AIR)
            pc.claim(cells, "door-spine-to-crown")
            pc.claim(well, "crown")
            pc.edge(a="crown", b="exterior", **{"class": "walk"}, via="door-spine-to-crown")
            # a ragged rim round the blowhole
            for (x, y, z) in cells + well:
                for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    n = (x + dx, fy, z + dz)
                    if pc.owned(n) and n not in pc.prog.region and (x + dx, y, z + dz) not in cells + well:
                        pc.set(*n, slab("cobbled_deepslate", "bottom")) if (x + z) % 2 else None
    wall_seams(pc, "crown", tread_fam="cobbled_deepslate", fill=S("minecraft:cobbled_deepslate"))
    stations(pc)
    space_claim(pc, "crown", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc, reason="the rim of the blowhole and the hide's ridges")
    return pc.finish("crown", shown_faces=["north", "south", "east", "west", "up"])


def brow(node):
    def extra(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        # the Brow Stone: a tall pale carved tablet driven into the forehead,
        # its top standing out of the brow at the forehead's edge
        bx, by, bz = pc.L(*M.STATIONS["anchor/brow-stone"][:3])
        for x in range(bx - 1, bx + 3):
            for y in range(fy, fy + 6):
                if (x, y, bz) == (bx, by, bz):
                    continue
                pc.set(x, y, bz, S("minecraft:chiseled_quartz_block") if (x + y) % 2 else S("minecraft:quartz_block"))
            pc.set(x, fy - 1, bz, S("minecraft:quartz_block"))
        # the lip of the forehead over the jaw bank
        for x in range(sx0 - 1, sx1 + 2):
            if pc.owned((x, fy - 1, sz0)) and not is_full(pc.get(x, fy - 1, sz0)):
                pc.set(x, fy - 1, sz0, mix(r, HIDE))
    return on_body(node, extra)


BUILDERS = {
    "node/mouth": mouth,
    "node/throat": throat,
    "node/rib-cathedral": rib_cathedral,
    "node/stomach": stomach,
    "node/heart-chamber": heart_chamber,
    "node/breach": breach,
    "node/spine-stair": spine_stair,
    "node/spine-top": spine_top,
    "node/far-landing": far_landing,
    "node/jaw-bank": jaw_bank,
    "node/flank-ridge": flank_ridge,
    "node/run-bank": run_bank,
    "node/tail-bank": tail_bank,
    "node/tail-road": tail_road,
    "node/crown": crown,
    "node/brow": brow,
    "node/back-upper": on_body,
    "node/back-middle": on_body,
    "node/back-lower": on_body,
    "node/tail-flank": on_body,
}
