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
        # an open place's space reaches as high as its openings, but its floor
        # is the walk: a stake's or a wreck's top higher up is left to `tops`
        if cap is not None and c[1] > pc.dy + 1 and standable(pc, c):
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
                   max_courses=r["courses"] + 1, inset=min(e, 1))
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


def close_fronts(pc, fill):
    """Between two open places the wall a seam pierces is the whole shared
    front, up to the lower of their skies, and nothing walls an open place's
    sky but what its piece builds: so where this place owns the plane of a
    doorway or stair seam to another open place, the plane outside the hole is
    built solid, from the lower floor to the lower sky (DW0836)."""
    me = M.P[pc.node]
    if me["ceiling"][0] != "open":
        return
    for s in pc.seams:
        if s["face"] in ("up", "down") or not s.get("owns_plane"):
            continue
        e = next(e for e in M.E if e["id"] == s["edge"])
        other = M.P[e["b"] if e["a"] == pc.node else e["a"]]
        if other["ceiling"][0] != "open" or M.S[s["edge"]]["contact"] is not None:
            continue
        y0 = min(M.fy(me), M.fy(other))
        y1 = min(M.fy(me) + me["ceiling"][1], M.fy(other) + other["ceiling"][1]) - 1
        (cx0, cy0, cz0), (cx1, cy1, cz1) = s["cells"]
        if s["face"] in ("north", "south"):
            lo, hi = max(me["x"], other["x"]), min(M.x1(me), M.x1(other))
            cols = [(x, None) for x in range(lo, hi + 1)]
        else:
            lo, hi = max(me["z"], other["z"]), min(M.z1(me), M.z1(other))
            cols = [(None, z) for z in range(lo, hi + 1)]
        for (wx, wz) in cols:
            for wy in range(y0, y1 + 1):
                lx, ly, lz = pc.L(wx if wx is not None else 0, wy, wz if wz is not None else 0)
                c = (lx if wx is not None else cx0, ly, lz if wz is not None else cz0)
                if pc.owned(c) and c not in pc.prog.region and not is_full(pc.get(*c)):
                    pc.set(*c, fill(c))


def _claim_xz(p):
    return (p["x"] - 1, p["z"] - 1, M.x1(p) + 1, M.z1(p) + 1)


def close_rings(pc, block):
    """An open place's ring is ground, and where it touches another place's
    claim outside a seam a body walks from one place into the other along
    rings nothing allocated (DW0838). Each such ring cell gets a post: from
    the ring's own floor to two over the walk."""
    me = M.P[pc.node]
    if me["ceiling"][0] != "open":
        return
    mx0, mz0, mx1, mz1 = _claim_xz(me)

    def inside(a, b):
        return b[0] <= a[0] and b[1] <= a[1] and a[2] <= b[2] and a[3] <= b[3]

    mine = (mx0, mz0, mx1, mz1)
    # a platform standing over another place, and the place under it, are not
    # walked into from each other's rings
    if any(inside(mine, _claim_xz(p)) for n, p in M.P.items() if n != pc.node):
        return
    others = [(n, _claim_xz(p)) for n, p in M.P.items()
              if n != pc.node and not inside(_claim_xz(p), mine)]
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ring = [(x, sz0 - 1) for x in range(sx0 - 1, sx1 + 2)] + [(x, sz1 + 1) for x in range(sx0 - 1, sx1 + 2)]
    ring += [(sx0 - 1, z) for z in range(sz0, sz1 + 1)] + [(sx1 + 1, z) for z in range(sz0, sz1 + 1)]
    for (x, z) in ring:
        if any((x, y, z) in pc.prog.region for y in range(fy - 1, fy + 2)):
            continue
        wx, _, wz = pc.W(x, 0, z)
        touch = False
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)):
            nx, nz = wx + dx, wz + dz
            if (dx, dz) != (0, 0) and mx0 <= nx <= mx1 and mz0 <= nz <= mz1:
                continue
            for n, (ox0, oz0, ox1, oz1) in others:
                if ox0 <= nx <= ox1 and oz0 <= nz <= oz1:
                    # where two rings lie side by side, one of them carries
                    # the posts: two rows of posts side by side are a path
                    # along their tops from one place into the other
                    if (dx, dz) == (0, 0) or not (ox0 <= wx <= ox1 and oz0 <= wz <= oz1) and pc.node < n:
                        touch = True
                        break
            if touch:
                break
        if not touch:
            continue
        y0 = fy - 1 if not is_full(pc.get(x, fy - 1, z)) else fy
        for y in range(y0, fy + 2):
            c = (x, y, z)
            if pc.owned(c) and c not in pc.prog.region and not is_full(pc.get(*c)):
                pc.set(*c, block(c))
