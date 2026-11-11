"""The three place programs of The Thing Across the Water — the jetty, the
harbour hall and the sea-stack — drawn as voxels from each place's handout.

The handout (`delvec allocation <campaign> <place>`) is read at run time and
nothing from it is typed here: the frame's extent, the play space, the seam's
cells, the roof zone and the voids all come from it. Each place is drawn cell by
cell in its frame's own coordinates and then written out as a box-split grammar
program: the frame is cut along the contract's claimed regions (each region one
`claim` scope), and every other box is cut into y layers, x columns and z runs.
A cell another owner holds is `skip`; an unset cell is `void` (air).

Everything below the sea's surface inside a frame is solid masonry or rock, so
no frame cell holds water and no cell of the sea is replaced by air.

Run from anywhere with `delvec` on PATH (and `DELVEWRIGHT_PREFABS` naming the
library):

    python3 campaigns/the-thing-across-the-water/design/programs-src/bay.py

It writes `programs/jetty.json`, `programs/hall.json` and `programs/stack.json`.
No randomness: the same handouts write the same bytes.
"""
import json
import os
import subprocess

CAMPAIGN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PREFABS = os.environ.get("DELVEWRIGHT_PREFABS", "")
SKIP = "<skip>"
SEA_TOP_WORLD_Y = 62  # the ocean horizon's sea surface (compiler.md, horizon)

STONE_BRICK = "minecraft:stone_bricks"
MOSSY_BRICK = "minecraft:mossy_stone_bricks"
CRACKED_BRICK = "minecraft:cracked_stone_bricks"
COBBLE = "minecraft:cobblestone"
MOSSY_COBBLE = "minecraft:mossy_cobblestone"
DECK = "minecraft:spruce_planks"
KERB = "minecraft:polished_andesite"
LOG = "minecraft:stripped_spruce_log[axis=y]"
PLANK = "minecraft:spruce_planks"
DARK_PLANK = "minecraft:dark_oak_planks"
LANTERN_UP = "minecraft:lantern[hanging=false,waterlogged=false]"
LANTERN_HUNG = "minecraft:lantern[hanging=true,waterlogged=false]"
BARREL = "minecraft:barrel[facing=up,open=false]"
KELP = "minecraft:dried_kelp_block"
SHELF = "minecraft:bookshelf"
DESK = "minecraft:spruce_slab[type=top,waterlogged=false]"
ROCK = ["minecraft:stone", "minecraft:andesite", "minecraft:tuff", "minecraft:cobblestone"]
ROCK_TOP = "minecraft:mossy_cobblestone"


def handout(place):
    cmd = ["delvec"] + (["--prefabs", PREFABS] if PREFABS else []) + ["allocation", CAMPAIGN, place]
    return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)


def fence(n, e, s, w):
    b = lambda v: "true" if v else "false"
    return f"minecraft:spruce_fence[east={b(e)},north={b(n)},south={b(s)},waterlogged=false,west={b(w)}]"


def pane(n, e, s, w):
    b = lambda v: "true" if v else "false"
    return f"minecraft:glass_pane[east={b(e)},north={b(n)},south={b(s)},waterlogged=false,west={b(w)}]"


def stair(block, facing, half="bottom"):
    return f"minecraft:{block}[facing={facing},half={half},shape=straight,waterlogged=false]"


def slab(block, kind):
    return f"minecraft:{block}_slab[type={kind},waterlogged=false]"


def full(state):
    """A block a fence or a pane connects to: a full opaque cube."""
    if state in (None, SKIP):
        return False
    name = state.split("[")[0]
    return not any(t in name for t in ("fence", "pane", "lantern", "slab", "stairs", "bell", "wall", "cobweb", "carpet"))


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
        # world y of local y 0
        self.y0 = h["world_min"][1]

    def mine(self, x, y, z):
        return self.cells.get((x, y, z), SKIP) is not SKIP

    def get(self, x, y, z):
        return self.cells.get((x, y, z), SKIP)

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

    def mark(self, stem, x, y, z, facing, role=None):
        self.marks.append((stem, x, y, z, facing, role))

    def connect(self, kind):
        """Give every fence or pane the connections its neighbours give it."""
        for (x, y, z), s in list(self.cells.items()):
            if s in (None, SKIP) or kind not in s:
                continue
            def joins(dx, dz):
                n = self.cells.get((x + dx, y, z + dz))
                return n not in (None, SKIP) and (kind in n or full(n))
            make = fence if kind == "fence" else pane
            self.cells[(x, y, z)] = make(joins(0, -1), joins(1, 0), joins(0, 1), joins(-1, 0))

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
        for stem, x, y, z, facing, mrole in reversed(self.marks):
            mk = {"anchor": stem, "at": "offset", "facing": facing,
                  "x": {"expr": "int", "value": x}, "y": {"expr": "int", "value": y}, "z": {"expr": "int", "value": z}}
            if mrole:
                mk["role"] = mrole
            body = {"op": "mark", "mark": mk, "body": body}
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


def masonry(x, y, z):
    """A deterministic weathering of the jetty's and the hall's stone below the deck."""
    k = (x * 7 + y * 13 + z * 5) % 11
    if k == 0:
        return MOSSY_BRICK
    if k == 4:
        return CRACKED_BRICK
    return STONE_BRICK


def jetty():
    h = handout("node/jetty")
    f = Frame(h)
    X, Y, Z = f.ext
    (sx0, sy0, sz0), (sx1, sy1, sz1) = h["space"]
    fy = sy0 - 1  # the deck course
    # The mole: solid masonry from the sea floor to the deck, the whole frame wide.
    for x in range(X):
        for z in range(Z):
            for y in range(1, fy):
                f.set(x, y, z, masonry(x, y, z))
    # The deck: planks between a stone kerb on both sides and at the seaward end.
    f.box((0, fy, 0), (X - 1, fy, Z - 1), KERB)
    f.box((sx0, fy, sz0), (sx1, fy, sz1), DECK)
    # The railing: spruce fence on the kerb, both sides and across the seaward end,
    # a post with a lantern on it every four blocks.
    rail_y = sy0
    for z in range(0, Z):
        f.set(0, rail_y, z, "fence")
        f.set(X - 1, rail_y, z, "fence")
    for x in range(0, X):
        f.set(x, rail_y, 0, "fence")
    lamps = []
    for z in range(0, sz1 + 1, 4):
        for x in (0, X - 1):
            if f.mine(x, rail_y, z):
                lamps.append((x, z))
    f.connect("fence")
    # The railing's last posts meet the hall's front wall, which stands one cell
    # beyond this frame on the face the handout names; the game joins a fence to
    # that wall, so the piece writes the join too.
    if any(n["face"] == "south" and n["kind"] == "roofed" for n in h["neighbours"]):
        for x in (0, X - 1):
            st = f.get(x, rail_y, Z - 1)
            if isinstance(st, str) and "fence" in st:
                f.cells[(x, rail_y, Z - 1)] = st.replace("south=false", "south=true")
    for x, z in lamps:
        f.set(x, rail_y + 1, z, LANTERN_UP)
    # The bell, at the very end of the jetty in the middle of the deck: the
    # objective's prop is placed on this cell by the engine.
    mx = (sx0 + sx1) // 2
    bell = (mx, sy0, sz0)
    # Two bollards flank the bell.
    f.set(mx - 2, sy0, sz0, "minecraft:andesite_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]")
    f.set(mx + 2, sy0, sz0, "minecraft:andesite_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]")
    # The seam: the hall's door, at the jetty's landward end. Left open.
    seam = h["seams"][0]
    (dx0, dy0, dz0), (dx1, dy1, dz1) = seam["cells"]
    f.box((dx0, dy0, dz0), (dx1, dy1, dz1), None)
    f.claim("hall-door", (dx0, dy0, dz0), (dx1, dy1, dz1))
    # Spaces: the deck, less the door cells.
    for b in subtract((sx0, sy0, sz0, sx1, sy1, sz1), [(dx0, dy0, dz0, dx1, dy1, dz1)]):
        f.claim("jetty", b[:3], b[3:])
    # The rail tops are not stood on.
    f.claim("rail-top", (0, sy0 + 1, 0), (0, sy1, Z - 1))
    f.claim("rail-top", (X - 1, sy0 + 1, 0), (X - 1, sy1, Z - 1))
    f.claim("rail-top", (1, sy0 + 1, 0), (X - 2, sy1, 0))
    # Marks.
    f.mark("bell", bell[0], bell[1], bell[2], "north")
    f.mark("jetty-end", mx, sy0, sz0 + 2, "north")
    f.mark("door-step", mx, sy0, sz1 - 3, "south")
    f.mark("node-jetty", mx, sy0, (sz0 + sz1) // 2, "south")
    f.mark("spawn", mx, sy0, (sz0 + sz1) // 2, "south", "entry")
    contract = {
        "entry": "jetty",
        "spaces": {"jetty": {"envelope": "open"}},
        "no_body": {"rail-top": {"reason": "the tops of the jetty's railing and its lantern posts; nobody is meant to stand on them"}},
        "edges": [{"a": "exterior", "b": "jetty", "class": "walk", "via": "hall-door"}],
    }
    return f.program("the-thing-across-the-water-jetty", contract, ["east", "north", "west"])


def hall():
    h = handout("node/hall")
    f = Frame(h)
    X, Y, Z = f.ext
    (sx0, sy0, sz0), (sx1, sy1, sz1) = h["space"]
    lid = h["roof"]["lid_y"]
    top = h["roof"]["top_y"]
    fy = sy0 - 1
    wx0, wx1, wz0, wz1 = sx0 - 1, sx1 + 1, sz0 - 1, sz1 + 1
    # The footing: masonry from the sea floor up to the floor course, under the
    # walls and the floor alike.
    for x in range(wx0, wx1 + 1):
        for z in range(wz0, wz1 + 1):
            for y in range(1, fy):
                f.set(x, y, z, masonry(x, y, z))
    f.box((wx0, fy, wz0), (wx1, fy, wz1), STONE_BRICK)
    f.box((sx0, fy, sz0), (sx1, fy, sz1), PLANK)
    # Walls: a stone-brick course, then stone bricks with spruce posts at the
    # corners and either side of the door.
    for y in range(sy0, sy1 + 1):
        f.box((wx0, y, wz0), (wx1, y, wz0), STONE_BRICK)
        f.box((wx0, y, wz1), (wx1, y, wz1), STONE_BRICK)
        f.box((wx0, y, wz0), (wx0, y, wz1), STONE_BRICK)
        f.box((wx1, y, wz0), (wx1, y, wz1), STONE_BRICK)
        for x, z in ((wx0, wz0), (wx1, wz0), (wx0, wz1), (wx1, wz1)):
            f.set(x, y, z, LOG)
    seam = h["seams"][0]
    (dx0, dy0, dz0), (dx1, dy1, dz1) = seam["cells"]
    for y in range(sy0, sy1 + 1):
        f.set(dx0 - 1, y, wz0, LOG)
        f.set(dx1 + 1, y, wz0, LOG)
    # Windows: two panes high in the east and west walls, and either side of the
    # keeper in the back wall.
    mz = (sz0 + sz1) // 2
    for z in (mz - 2, mz + 2):
        f.box((wx0, sy0 + 1, z), (wx0, sy0 + 2, z), "pane")
        f.box((wx1, sy0 + 1, z), (wx1, sy0 + 2, z), "pane")
    mx = (sx0 + sx1) // 2
    for x in (mx - 3, mx + 3):
        f.box((x, sy0 + 1, wz1), (x, sy0 + 2, wz1), "pane")
    # The door: the handed cells, open.
    f.box((dx0, dy0, dz0), (dx1, dy1, dz1), None)
    f.connect("pane")
    # The keeper's desk: a counter either side of where he stands, against the
    # back wall, so nothing stands between him and the door.
    kz = sz1 - 1
    f.box((mx - 3, sy0, kz), (mx - 1, sy0, kz), DESK)
    f.box((mx + 1, sy0, kz), (mx + 3, sy0, kz), DESK)
    # Shelves set into the back wall behind the counter.
    f.box((mx - 2, sy0, wz1), (mx - 1, sy0 + 1, wz1), SHELF)
    f.box((mx + 1, sy0, wz1), (mx + 2, sy0 + 1, wz1), SHELF)
    # Stores along the west wall: a barrel, then bales of dried kelp; a coil of
    # rope and nets along the east. Two barrels in the hall and no more: empty
    # containers stay few (scenery is capped per place).
    for z in range(sz0 + 1, sz1 - 1, 2):
        f.set(sx0, sy0, z, BARREL if z == sz0 + 1 else KELP)
    f.set(sx1, sy0, sz0 + 1, BARREL)
    f.set(sx1, sy0, sz0 + 3, "minecraft:cobweb")
    # Lanterns hung from the ceiling.
    for x in (sx0 + 2, sx1 - 2):
        for z in (sz0 + 1, sz1 - 1):
            f.set(x, sy1, z, LANTERN_HUNG)
    # The ceiling course, and a low-pitched roof of slabs: the ridge runs east to
    # west, each slope rising half a block a cell from the eaves, the attic under
    # it solid planks.
    f.box((wx0, lid, wz0), (wx1, lid, wz1), DARK_PLANK)
    roof_air = []
    for z in range(0, Z):
        c = min(z, Z - 1 - z)
        y = lid + c // 2
        kind = "bottom" if c % 2 == 0 else "top"
        if y > top:
            y, kind = top, "top"
        for x in range(0, X):
            if c == min(Z // 2, (Z - 1) // 2) and (Z - 1) % 2 == 0 and z == (Z - 1) // 2:
                f.set(x, y, z, DARK_PLANK)
            else:
                f.set(x, y, z, slab("spruce", kind))
            if wx0 <= x <= wx1 and wz0 <= z <= wz1:
                for yy in range(lid + 1, y):
                    f.set(x, yy, z, PLANK)
        if y + 1 <= top:
            roof_air.append(((0, y + 1, z), (X - 1, top, z)))
    # The gable ends: plank infill between the ceiling course and the slabs is
    # already solid; the eaves overhang open air.
    f.claim("hall-door", (dx0, dy0, dz0), (dx1, dy1, dz1))
    f.claim("hall", (sx0, fy, sz0), (sx1, sy1, sz1))
    for a, b in roof_air:
        f.claim("roof", a, b)
    f.mark("keeper", mx, sy0, kz, "north")
    f.mark("node-hall", mx, sy0, mz, "north")
    contract = {
        "entry": "hall",
        "spaces": {"hall": {"envelope": "enclosed"}},
        "no_body": {"roof": {"reason": "the outer slopes of the hall's roof; nobody is meant to get up there"}},
        "no_body_majority_ack": "the roof's two slopes carry more cells a body could stand on than the hall's floor does, and every one of them is open to the sky",
        "edges": [{"a": "exterior", "b": "hall", "class": "walk", "via": "hall-door"}],
    }
    return f.program("the-thing-across-the-water-hall", contract, ["east", "north", "south", "west"])


def stack():
    h = handout("node/stack")
    f = Frame(h)
    X, Y, Z = f.ext
    (sx0, sy0, sz0), (sx1, sy1, sz1) = h["space"]
    fy = sy0 - 1
    cx, cz = (sx0 + sx1) // 2, (sz0 + sz1) // 2
    sea = SEA_TOP_WORLD_Y - f.y0  # local y of the sea's top course
    # A rock stack from the sea floor: the frame's full width at the waterline,
    # stepping in as it rises to a seven-wide top. Each column stands to its own
    # height, so the flanks read as weathered rock, not a box; every column is
    # solid at least to the sea's top course, so no cell of the sea is emptied.
    top_r = 3
    for x in range(X):
        for z in range(Z):
            d = max(abs(x - cx), abs(z - cz))
            j = (x * 5 + z * 3) % 3
            if d <= top_r:
                height = fy
            elif d == top_r + 1:
                height = fy - 3 - j
            elif d == top_r + 2:
                height = fy - 8 - j
            else:
                height = sea + 2 - j
            height = max(height, sea)
            for y in range(1, height + 1):
                k = (x * 5 + y * 3 + z * 7) % len(ROCK)
                block = ROCK[k]
                if y == height and y > sea:
                    block = ROCK_TOP
                if sea - 1 <= y <= sea + 1 and (x + y + z) % 3 == 0:
                    block = "minecraft:mossy_cobblestone"
                f.set(x, y, z, block)
    # A broken crown of rock two courses high round the top's edge, so the middle
    # where the thing rises is a hollow, and the top is closed: nothing stood on
    # it could step off into the sea.
    for x in range(cx - top_r, cx + top_r + 1):
        for z in range(cz - top_r, cz + top_r + 1):
            if max(abs(x - cx), abs(z - cz)) != top_r:
                continue
            corner = abs(x - cx) == top_r and abs(z - cz) == top_r
            for y in (sy0, sy0 + 1):
                k = (x * 3 + y + z * 5) % len(ROCK)
                f.set(x, y, z, ROCK[k])
            if not corner and (x * 7 + z * 3) % 4 == 0:
                f.set(x, sy0 + 2, z, ROCK_TOP)
    r = top_r - 1
    f.claim("top", (cx - r, sy0, cz - r), (cx + r, Y - 1, cz + r))
    f.claim("crown", (0, sy0, 0), (cx - r - 1, Y - 1, Z - 1))
    f.claim("crown", (cx + r + 1, sy0, 0), (X - 1, Y - 1, Z - 1))
    f.claim("crown", (cx - r, sy0, 0), (cx + r, Y - 1, cz - r - 1))
    f.claim("crown", (cx - r, sy0, cz + r + 1), (cx + r, Y - 1, Z - 1))
    f.mark("stack-top", cx, sy0, cz, "south")
    contract = {
        "entry": "top",
        "spaces": {"top": {"envelope": "open"}},
        "edges": [],
        "no_body": {"crown": {"reason": "the stack's broken rock crown and its stepped flanks, seen from the jetty and never stood on"}},
        "no_body_majority_ack": "scenery: built to be seen from the jetty and never entered",
    }
    return f.program("the-thing-across-the-water-stack", contract, ["east", "north", "south", "west"])


def main():
    os.makedirs(os.path.join(CAMPAIGN, "programs"), exist_ok=True)
    for stem, make in (("jetty", jetty), ("hall", hall), ("stack", stack)):
        path = os.path.join(CAMPAIGN, "programs", f"{stem}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(make(), fh, indent=2)
            fh.write("\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
