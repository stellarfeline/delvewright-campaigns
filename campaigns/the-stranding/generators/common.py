"""Shared place helpers: the space claim, marks, seams answered, roofs."""

import mapmodel as M
from kit import Piece, AIR, boxcells, answer_wall_seam, ground, ring_cells, INWARD
from blocks import S, stairs, slab, is_full
import arch


def opening_top(pc):
    """the highest course any wall seam's opening reaches"""
    t = pc.dy + 1
    for s in pc.seams:
        if s["face"] in ("up", "down"):
            continue
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        t = max(t, y0, y1)
    return t


def space_claim(pc, name="room", envelope="enclosed", box=None, only_free=True, cap=None):
    """Claim every cell a body can be in (non-full) in the play space (or `box`)
    that no opening, landing or flight has claimed already. `cap` limits the
    claim's height (open places); it never falls under the openings' tops."""
    (sx0, sy0, sz0), (sx1, sy1, sz1) = box or pc.space
    if cap is not None:
        sy1 = min(sy1, max(cap, opening_top(pc)))
    pc.space_decl(name, envelope)
    for c in boxcells((sx0, sy0, sz0), (sx1, sy1, sz1)):
        if not pc.owned(c) or c in pc.prog.region:
            continue
        if is_full(pc.prog.get(*c)):
            continue
        pc.prog.region[c] = name


PASSABLE = ("torch", "carpet", "short_grass", "tall_grass", "fern", "vine", "vines", "vines_plant",
            "_sign", "_banner", "_button", "lever", "pressure_plate", "rail", "cobweb", "lichen",
            "sculk_vein", "snow", "flower", "dandelion", "poppy", "tulip", "orchid", "allium",
            "bluet", "daisy", "cornflower", "lily_of_the_valley", "petals", "wildflowers", "leaf_litter",
            "dead_bush", "seagrass", "kelp", "kelp_plant", "sugar_cane", "sapling", "mushroom",
            "hanging_roots", "spore_blossom", "nether_sprouts", "_roots")


def passable(st):
    n = st.split("[")[0]
    if n in ("minecraft:air", "minecraft:cave_air"):
        return True
    if "mushroom_block" in n or n.endswith("mushroom_stem"):
        return False
    return any(n.endswith(t) for t in PASSABLE)


def standable(pc, c):
    x, y, z = c
    a = pc.prog.get(x, y, z)
    b = pc.prog.get(x, y - 1, z)
    h = pc.prog.get(x, y + 1, z)
    if not pc.owned(c):
        return False
    room = passable(a) or "_slab" in a or "_stairs" in a or "carpet" in a
    head = passable(h) or "structure_void" in h
    bn = b.split("[")[0]
    sup = (bn not in ("minecraft:structure_void", "minecraft:water", "minecraft:lava") and not passable(b)) \
        or "_slab" in a or "_stairs" in a
    return room and head and sup


def node_mark(pc, prefer=None):
    """the place's own anchor at its floor centre; if a stair or a block stands
    there, the nearest standable cell of its space"""
    want = prefer or pc.L(*M.node_anchor(pc.node))
    name = "node-" + pc.node.split("/")[1]
    best = None
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    def rname(c):
        r = pc.prog.region.get(c)
        return r[0] if isinstance(r, tuple) else r
    if standable(pc, want) and rname(want) is not None and not rname(want).startswith(("flight", "door", "landing", "seam")):
        best = want
    else:
        cands = []
        for c in boxcells((sx0, sy0, sz0), (sx1, sy1, sz1)):
            r = rname(c)
            if r is None or r.startswith(("flight", "door", "landing", "seam")):
                continue
            if pc.no_body and r in pc.no_body:
                continue
            if standable(pc, c):
                d = abs(c[0] - want[0]) + abs(c[1] - want[1]) * 3 + abs(c[2] - want[2])
                cands.append((d, c))
        if cands:
            best = min(cands)[1]
    if best is None:
        raise SystemExit("%s: no standable cell for its node anchor" % pc.node)
    pc.mark(name, best)
    pc.node_cell = best
    return best


def leftovers_no_body(pc, name="tops", reason="the tops of walls, banks and roofs, which nobody walks"):
    """every standable cell no space or edge accounts for goes into one
    out-of-walk region, whose kind the contract computes from the blocks
    (into the roof's region when the place has one)"""
    if "roof" in pc.no_body:
        name = "roof"
    n = 0
    for c in boxcells((0, 0, 0), (pc.X - 1, pc.Y - 1, pc.Z - 1)):
        if c in pc.prog.region or not pc.owned(c):
            continue
        if standable(pc, c):
            pc.prog.region[c] = name
            n += 1
    if n and name not in pc.no_body:
        pc.no_body[name] = {"reason": reason}
    if n and not pc.majority_ack:
        pc.majority_ack = ("the place owns its outside: roofs, wall tops and banks are more standable "
                           "surface than its floor, and nobody walks them")
    return n


def station_mark(pc, aid, clear=True):
    c, f = pc.station(aid)
    if clear and pc.owned(c):
        pc.set(*c, AIR)
    pc.mark(aid.split("/")[1], c, facing=f)
    return c


def stations(pc):
    for st in M.P[pc.node]["stations"]:
        station_mark(pc, st["anchor"])


def wall_seams(pc, space="room", tread_fam="stone_brick", fill=None, threshold=None, bar_block=None, skip=()):
    fill = fill or S("minecraft:stone_bricks")
    out = {}
    for s in pc.seams:
        if s["face"] in ("up", "down") or s["edge"] in skip:
            continue
        out[s["edge"]] = answer_wall_seam(
            pc, s, space, tread=lambda f, fam=tread_fam: stairs(fam, f), fill=fill,
            threshold=threshold, bar_block=bar_block or S("minecraft:iron_bars"))
    return out


def shell_box(pc):
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    return sx0 - 1, sz0 - 1, sx1 + 1, sz1 + 1


def roof(pc, kind, axis, fam, gable_block, eaves=None):
    """the roof the plan reserves, drawn over the shell grown by its eaves"""
    r = pc.roof
    e = r["eaves"] if eaves is None else eaves
    x0, z0, x1, z1 = shell_box(pc)
    if kind == "gable":
        arch.gable(pc, x0 - e, z0 - e, x1 + e, z1 + e, r["lid_y"], axis, fam, gable_block,
                   max_courses=r["courses"] + 1)
    else:
        arch.hipped(pc, x0 - e, z0 - e, x1 + e, z1 + e, r["lid_y"], fam, gable_block,
                    max_courses=r["courses"] + 1)


def roof_no_body(pc):
    if pc.roof:
        pc.roof_no_body(pc.roof["lid_y"] + 1)


def chimney(pc, x, z, block, top=None):
    top = pc.Y - 1 if top is None else top
    for y in range(pc.dy, top + 1):
        pc.set(x, y, z, block)


def lantern_post(pc, x, z, y=None, post=None, lantern=None):
    y = pc.dy if y is None else y
    post = post or S("minecraft:spruce_fence")
    pc.set(x, y, z, post)
    pc.set(x, y + 1, z, post)
    pc.set(x, y + 2, z, lantern or arch.lantern(False))
