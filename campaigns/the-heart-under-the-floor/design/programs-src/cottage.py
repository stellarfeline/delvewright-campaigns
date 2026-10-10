"""The two place programs (the cottage and its doorstep), drawn as voxels from
each place's handout.

The handout (`delvec allocation <campaign> node/cottage`) is read at run time
and nothing from it is typed here: the frame's extent, the play space, the
seam's cells, the roof zone and the voids all come from it. The cottage is
drawn cell by cell in the frame's own coordinates, then compiled into a
box-split grammar program: the frame is cut along the contract's claimed
regions (each region one `claim` scope), and every other box is cut into
y layers, x columns and z runs. A cell another owner holds is `skip`.

Run from the campaign directory with `delvec` on PATH:

    python3 design/programs-src/cottage.py

It writes `programs/cottage.json` and `programs/doorstep.json`. No randomness: the same handout writes the
same bytes.
"""
import json
import os
import subprocess

CAMPAIGN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PREFABS = os.environ.get("DELVEWRIGHT_PREFABS", "")
SKIP = "<skip>"

COBBLE = "minecraft:cobblestone"
PLASTER = "minecraft:calcite"
POST = "minecraft:stripped_spruce_log[axis=y]"
BRICK = "minecraft:bricks"
PLANK = "minecraft:spruce_planks"
KITCHEN_FLOOR = "minecraft:stone_bricks"
BOARDS = "minecraft:spruce_planks"
RIDGE = "minecraft:dark_oak_planks"
HEARTHSTONE = "minecraft:smooth_stone_slab[type=bottom,waterlogged=false]"
HEART_BOX = "minecraft:barrel[facing=up,open=false]"
FIRE = "minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]"
LANTERN = "minecraft:lantern[hanging=true,waterlogged=false]"
TABLE = "minecraft:spruce_slab[type=top,waterlogged=false]"
CARPET = "minecraft:red_carpet"
SHELF = "minecraft:bookshelf"
CAULDRON = "minecraft:cauldron"


def stair(block, facing):
    return f"minecraft:{block}[facing={facing},half=bottom,shape=straight,waterlogged=false]"


def pane(axis):
    if axis == "x":  # a pane in a wall that runs along x
        return "minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]"
    return "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]"


def handout(place):
    cmd = ["delvec"] + (["--prefabs", PREFABS] if PREFABS else []) + ["allocation", CAMPAIGN, place]
    return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)


class Frame:
    def __init__(self, h):
        self.h = h
        self.ext = h["extent"]
        X, Y, Z = self.ext
        self.cells = {(x, y, z): None for x in range(X) for y in range(Y) for z in range(Z)}
        for v in h["voids"]:
            (x0, y0, z0), (x1, y1, z1) = v["cells"]
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    for z in range(z0, z1 + 1):
                        self.cells[(x, y, z)] = SKIP
        self.regions = {}
        self.marks = []

    def mine(self, x, y, z):
        return self.cells.get((x, y, z), SKIP) is not SKIP

    def set(self, x, y, z, block):
        if self.mine(x, y, z):
            self.cells[(x, y, z)] = block

    def box(self, a, b, block):
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                    self.set(x, y, z, block)

    def claim(self, name, a, b):
        self.regions.setdefault(name, []).append(
            tuple(min(a[i], b[i]) for i in range(3)) + tuple(max(a[i], b[i]) for i in range(3)))

    def mark(self, stem, x, y, z, facing):
        self.marks.append((stem, x, y, z, facing))

    def program(self, name, contract, shown):
        roles = {}

        def role(state):
            if state not in roles:
                base = state.split(":")[1].split("[")[0].replace("_", "-")
                n = sum(1 for r in roles.values() if r == base or r.startswith(base + "-"))
                roles[state] = base if n == 0 else f"{base}-{n + 1}"
            return roles[state]

        def ab(n):
            return {"size": "absolute", "blocks": {"expr": "int", "value": n}}

        def split(axis, runs):
            if len(runs) == 1:
                return runs[0][1]
            return {"op": "split", "axis": axis, "sizes": [ab(n) for n, _ in runs], "children": [c for _, c in runs]}

        def leaf(s):
            if s is SKIP:
                return {"op": "skip"}
            if s is None:
                return {"op": "void"}
            return {"op": "fill", "material": {"role": role(s)}}

        def runs_of(keys, make):
            out = []
            for k, arg in keys:
                if out and out[-1][0] == k:
                    out[-1][1] += 1
                else:
                    out.append([k, 1, arg])
            return [(n, make(arg)) for _, n, arg in out]

        def voxel(bx):
            x0, y0, z0, x1, y1, z1 = bx

            def column(x, y):
                return split("z", runs_of([(self.cells[(x, y, z)], z) for z in range(z0, z1 + 1)],
                                          lambda z, x=x, y=y: leaf(self.cells[(x, y, z)])))

            def layer(y):
                keys = [(tuple(self.cells[(x, y, z)] for z in range(z0, z1 + 1)), x) for x in range(x0, x1 + 1)]
                return split("x", runs_of(keys, lambda x, y=y: column(x, y)))

            keys = [(tuple(self.cells[(x, y, z)] for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)), y)
                    for y in range(y0, y1 + 1)]
            return split("y", runs_of(keys, layer))

        def inside(b, bx):
            return all(bx[i] <= b[i] and b[i + 3] <= bx[i + 3] for i in range(3))

        def scope(bx, rs):
            if not rs:
                return voxel(bx)
            if len(rs) == 1 and rs[0][1] == bx:
                return {"op": "claim", "region": rs[0][0], "body": voxel(bx)}
            for ai, axis in enumerate("xyz"):
                for p in sorted({p for _, b in rs for p in (b[ai], b[ai + 3] + 1) if bx[ai] < p <= bx[ai + 3]}):
                    if any(b[ai] < p <= b[ai + 3] for _, b in rs):
                        continue
                    lo = list(bx); lo[ai + 3] = p - 1
                    hi = list(bx); hi[ai] = p
                    rl = [r for r in rs if inside(r[1], tuple(lo))]
                    rh = [r for r in rs if inside(r[1], tuple(hi))]
                    return split(axis, [(p - bx[ai], scope(tuple(lo), rl)), (bx[ai + 3] - p + 1, scope(tuple(hi), rh))])
            raise SystemExit(f"{name}: regions inside {bx} are not guillotine-separable: {[r[0] for r in rs]}")

        X, Y, Z = self.ext
        regs = [(n, b) for n, bs in sorted(self.regions.items()) for b in bs]
        body = scope((0, 0, 0, X - 1, Y - 1, Z - 1), regs)
        for stem, x, y, z, facing, *role in reversed(self.marks):
            m = {"anchor": stem, "at": "offset", "facing": facing,
                 "x": {"expr": "int", "value": x}, "y": {"expr": "int", "value": y}, "z": {"expr": "int", "value": z}}
            if role:
                m["role"] = role[0]
            body = {"op": "mark", "mark": m, "body": body}
        return {
            "version": "1.10.0",
            "name": name,
            "start": "place",
            "params": {},
            "palette": {r: s for s, r in sorted(roles.items(), key=lambda kv: kv[1])},
            "rules": {"place": [{"weight": 1, "body": body}]},
            "contract": contract,
            "shown_faces": shown,
        }


def cottage():
    h = handout("node/cottage")
    f = Frame(h)
    X, Y, Z = f.ext
    (sx0, sy0, sz0), (sx1, sy1, sz1) = h["space"]
    lid = h["roof"]["lid_y"]
    top = h["roof"]["top_y"]
    fy = sy0 - 1  # the floor course
    wx0, wx1, wz0, wz1 = sx0 - 1, sx1 + 1, sz0 - 1, sz1 + 1  # the ring the walls stand on
    width = sx1 - sx0 + 1
    room = (width - 2) // 3  # three rooms, two inner walls
    kitchen = (sx0, sx0 + room - 1)
    wall_a = kitchen[1] + 1
    parlour = (wall_a + 1, wall_a + room)
    wall_b = parlour[1] + 1
    front = (wall_b + 1, sx1)
    assert front[1] - front[0] + 1 == room, (kitchen, parlour, front)
    mz = (sz0 + sz1) // 2

    # Floor course: flagstones in the kitchen, boards elsewhere.
    f.box((sx0, fy, sz0), (sx1, fy, sz1), BOARDS)
    f.box((kitchen[0], fy, sz0), (kitchen[1], fy, sz1), KITCHEN_FLOOR)
    # Outer walls on the ring: a cobble course, plaster above, spruce posts at the corners.
    for y in range(sy0, sy1 + 1):
        blk = COBBLE if y == sy0 else PLASTER
        f.box((wx0, y, wz0), (wx1, y, wz0), blk)
        f.box((wx0, y, wz1), (wx1, y, wz1), blk)
        f.box((wx0, y, wz0), (wx0, y, wz1), blk)
        f.box((wx1, y, wz0), (wx1, y, wz1), blk)
        for x, z in ((wx0, wz0), (wx0, wz1), (wx1, wz0), (wx1, wz1), (wall_a, wz0), (wall_a, wz1), (wall_b, wz0), (wall_b, wz1)):
            f.set(x, y, z, POST)
    # Inner walls, plaster on boards, each with a doorway in its middle.
    for wx in (wall_a, wall_b):
        f.box((wx, sy0, sz0), (wx, sy1, sz1), PLASTER)
    # Windows: two panes high, in the long walls and the east gable.
    for x in ((kitchen[0] + kitchen[1]) // 2, (parlour[0] + parlour[1]) // 2):
        f.box((x, sy0 + 1, wz0), (x, sy0 + 2, wz0), pane("x"))
        f.box((x, sy0 + 1, wz1), (x, sy0 + 2, wz1), pane("x"))
    f.box(((front[0] + front[1]) // 2, sy0 + 1, wz0), ((front[0] + front[1]) // 2, sy0 + 2, wz0), pane("x"))
    f.box((wx1, sy0 + 1, mz), (wx1, sy0 + 2, mz), pane("z"))
    # The fireplace in the west wall: a brick breast, a campfire in a one-high recess.
    f.box((wx0, sy0, mz - 1), (wx0, sy1, mz + 1), BRICK)
    f.set(wx0, sy0, mz, FIRE)
    # The hearth: bricks in the floor before the fire, and the hearthstone on the
    # middle one, over the little barrel set into the floor course.
    f.box((sx0, fy, mz - 1), (sx0 + 1, fy, mz + 1), BRICK)
    hx, hz = sx0, mz
    f.set(hx, fy, hz, HEART_BOX)
    f.set(hx, sy0, hz, HEARTHSTONE)
    # Furniture: kitchen table and stools, a cauldron; parlour shelves and a rug;
    # front-room table and bench.
    kx = kitchen[0] + 4
    f.box((kx, sy0, mz - 1), (kx, sy0, mz + 1), TABLE)
    f.set(kx + 1, sy0, mz - 1, stair("spruce_stairs", "east"))
    f.set(kx + 1, sy0, mz + 1, stair("spruce_stairs", "east"))
    f.set(kitchen[1], sy0, sz0, CAULDRON)
    f.box((parlour[0] + 1, sy0, sz0), (parlour[1] - 1, sy0 + 2, sz0), SHELF)
    f.box((parlour[0] + 2, sy0, mz - 1), (parlour[1] - 2, sy0, mz + 1), CARPET)
    f.box((front[0] + 2, sy0, sz0 + 1), (front[1] - 2, sy0, sz0 + 1), TABLE)
    f.box((front[0] + 2, sy0, sz0 + 2), (front[1] - 2, sy0, sz0 + 2), stair("spruce_stairs", "south"))
    # A lantern hung from the middle of every room's ceiling.
    for a, b in (kitchen, parlour, front):
        f.set((a + b) // 2, sy1, mz, LANTERN)
    # Ceiling course and roof: a gable whose ridge runs east-west, spruce stairs
    # on both slopes, the attic under it solid.
    f.box((wx0, lid, wz0), (wx1, lid, wz1), PLANK)
    roof_air = []
    zr0, zr1 = 0, Z - 1
    half = (zr1 - zr0) // 2
    for z in range(zr0, zr1 + 1):
        c = min(z - zr0, zr1 - z)
        y = lid + c
        if y > top:
            continue
        for x in range(0, X):
            if z - zr0 < half:
                f.set(x, y, z, stair("spruce_stairs", "south"))
            elif zr1 - z < half:
                f.set(x, y, z, stair("spruce_stairs", "north"))
            else:
                f.set(x, y, z, RIDGE)
            if wx0 <= x <= wx1 and wz0 <= z <= wz1:
                for yy in range(lid, y):
                    f.set(x, yy, z, PLANK)
        if y + 1 <= top:
            roof_air.append(((0, y + 1, z), (X - 1, top, z)))
    # The chimney: the fireplace's brick breast carried up through the roof in
    # the west gable to the ridge.
    f.box((wx0, lid, mz - 1), (wx0, top, mz + 1), BRICK)
    # The front doorway: the handed cells, open.
    seam = h["seams"][0]
    (dx0, dy0, dz0), (dx1, dy1, dz1) = seam["cells"]
    f.box((dx0, dy0, dz0), (dx1, dy1, dz1), None)
    f.claim("front-door", (dx0, dy0, dz0), (dx1, dy1, dz1))
    # Inner doorways.
    for wx, nm in ((wall_a, "kitchen-door"), (wall_b, "parlour-door")):
        f.box((wx, sy0, mz), (wx, sy0 + 1, mz), None)
        f.claim(nm, (wx, sy0, mz), (wx, sy0 + 1, mz))
    # Spaces.
    # Each room's space takes in its own floor course, so the barrel set into
    # the kitchen floor under the hearthstone lies in the kitchen.
    f.claim("kitchen", (kitchen[0], fy, sz0), (kitchen[1], sy1, sz1))
    f.claim("parlour", (parlour[0], fy, sz0), (parlour[1], sy1, sz1))
    f.claim("front-room", (front[0], fy, sz0), (front[1], sy1, sz1))
    for a, b in roof_air:
        f.claim("roof", a, b)
    # Marks: every owed name.
    f.mark("hearth", hx, sy0, hz, "west")
    f.mark("heart", hx, fy, hz, "west")
    f.mark("front-room", (front[0] + front[1]) // 2, sy0, mz, "north")
    f.mark("parlour", (parlour[0] + parlour[1]) // 2, sy0, mz, "west")
    f.mark("node-cottage", (parlour[0] + parlour[1]) // 2, sy0, mz, "west")
    contract = {
        "entry": "front-room",
        "spaces": {"kitchen": {"envelope": "enclosed"}, "parlour": {"envelope": "enclosed"},
                   "front-room": {"envelope": "enclosed"}},
        "no_body": {"roof": {"reason": "the outer slopes of the roof; nobody is meant to get up there"}},
        "no_body_majority_ack": "the roof's two slopes carry more cells a body could stand on than the three rooms do, and every one of them is open to the sky",
        "edges": [
            {"a": "exterior", "b": "front-room", "class": "walk", "via": "front-door"},
            {"a": "front-room", "b": "parlour", "class": "walk", "via": "parlour-door"},
            {"a": "parlour", "b": "kitchen", "class": "walk", "via": "kitchen-door"},
        ],
    }
    # Every side of the cottage stands in the open and is meant to be seen.
    return f.program("the-heart-under-the-floor-cottage", contract, ["east", "north", "south", "up", "west"])


def subtract(box, holes):
    """Disjoint boxes covering `box` minus `holes`, cut along the holes' faces."""
    for hole in holes:
        if all(box[i] <= hole[i + 3] and hole[i] <= box[i + 3] for i in range(3)):
            break
    else:
        return [box]
    out = []
    lo, hi = list(box[:3]), list(box[3:])
    for i in range(3):
        if lo[i] < hole[i]:
            piece = lo[:] + hi[:]; piece[i + 3] = hole[i] - 1
            out.append(tuple(piece)); lo[i] = hole[i]
        if hi[i] > hole[i + 3]:
            piece = lo[:] + hi[:]; piece[i] = hole[i + 3] + 1
            out.append(tuple(piece)); hi[i] = hole[i + 3]
    rest = [o for o in holes if o is not hole]
    return [b for p in out for b in subtract(p, rest)]


GROUND_LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
FLAG = "minecraft:polished_andesite"
PATH = "minecraft:gravel"
TURF = "minecraft:grass_block[snowy=false]"
HEDGE = "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]"


def doorstep():
    h = handout("node/doorstep")
    f = Frame(h)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = h["space"]
    fy = sy0 - 1
    seam = h["seams"][0]
    (dx0, dy0, dz0), (dx1, dy1, dz1) = seam["cells"]
    # Turf, a worn path from the lane to the door, and two flags before the door.
    f.box((sx0, fy, sz0), (sx1, fy, sz1), TURF)
    f.box((dx0 - 1, fy, sz0), (dx1 + 1, fy, sz1), PATH)
    f.box((dx0 - 1, fy, dz0), (dx1 + 1, fy, dz0 + 1), FLAG)
    # A hedge two high round the garden on the plot's ring, closing it against
    # the cottage's front wall: the garden is the only outside the party has.
    X, Y, Z = f.ext
    for y in (sy0, sy0 + 1):
        f.box((sx0 - 1, y, sz0), (sx0 - 1, y, Z - 1), HEDGE)
        f.box((sx1 + 1, y, sz0), (sx1 + 1, y, Z - 1), HEDGE)
        f.box((sx0 - 1, y, Z - 1), (sx1 + 1, y, Z - 1), HEDGE)
    f.claim("hedge-top", (sx0 - 1, sy0 + 2, sz0), (sx0 - 1, sy0 + 2, Z - 2))
    f.claim("hedge-top", (sx1 + 1, sy0 + 2, sz0), (sx1 + 1, sy0 + 2, Z - 2))
    f.claim("hedge-top", (sx0 - 1, sy0 + 2, Z - 1), (sx1 + 1, sy0 + 2, Z - 1))
    # Two lanterns on the flags either side of the door.
    f.set(dx0 - 2, sy0, dz0, GROUND_LANTERN)
    f.set(dx1 + 2, sy0, dz0, GROUND_LANTERN)
    f.box((dx0, dy0, dz0), (dx1, dy1, dz1), None)
    f.claim("front-door", (dx0, dy0, dz0), (dx1, dy1, dz1))
    for b in subtract((sx0, sy0, sz0, sx1, sy1, sz1), [(dx0, dy0, dz0, dx1, dy1, dz1)]):
        f.claim("doorstep", b[:3], b[3:])
    cx = dx0
    f.mark("spawn", cx, sy0, sz1 - 1, "north")
    f.marks[-1] = f.marks[-1] + ("entry",)
    f.mark("node-doorstep", cx, sy0, sz1 - 1, "north")
    contract = {
        "entry": "doorstep",
        "spaces": {"doorstep": {"envelope": "open"}},
        "no_body": {"hedge-top": {"reason": "the top of the garden hedge, two blocks up; nobody is meant to stand on it"}},
        "edges": [{"a": "exterior", "b": "doorstep", "class": "walk", "via": "front-door"}],
    }
    # The hedge's three outer sides are finished faces, seen from the lane.
    return f.program("the-heart-under-the-floor-doorstep", contract, ["east", "south", "west"])


def main():
    os.makedirs(os.path.join(CAMPAIGN, "programs"), exist_ok=True)
    for stem, make in (("cottage", cottage), ("doorstep", doorstep)):
        path = os.path.join(CAMPAIGN, "programs", f"{stem}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(make(), fh, indent=2)
            fh.write("\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
