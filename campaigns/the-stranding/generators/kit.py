"""The detailing kit: a voxel model of one place, written as its detail program.

A place's program is computed from a few proportions in its own builder
(places_*.py). This module holds what every builder shares:

- the place's allocation, asked afresh of `delvec allocation` on every run
  (argv: the delvec binary and the prefab library), so a builder follows the
  plan and no number from the allocation is typed anywhere;
- a voxel grid of (block, claim) per cell, with box, column and wall helpers;
- the seams: every allocated opening is cut to air and claimed as a way to
  the exterior, and nothing else on the frame's faces is opened by the kit;
- the spatial contract (one space per place unless the builder declares
  more), the marks, `shown_faces` read off the boundary blocks, and the
  program document (version 1.9.0), run-length encoded along every axis.

Deterministic: no clock, no RNG, sorted iteration only.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.abspath(os.path.join(HERE, ".."))
DELVEC = os.environ.get("DELVEC_BIN") or "delvec"
PREFABS = os.environ.get("DELVEWRIGHT_PREFABS") or os.path.join(CAMP, "..", "..", "prefabs")


def allocation(stem):
    out = subprocess.run([DELVEC, "--prefabs", PREFABS, "allocation", CAMP, f"node/{stem}"],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def lit(v):
    return {"expr": "int", "value": v}


# ---- block-state spellings (every property written: DW0737) ----------------
def stair(mat, facing, half="bottom", shape="straight"):
    return f"minecraft:{mat}_stairs[facing={facing},half={half},shape={shape},waterlogged=false]"

def slab(mat, typ="bottom"):
    return f"minecraft:{mat}_slab[type={typ},waterlogged=false]"

def fence(mat, n=False, e=False, s=False, w=False):
    b = lambda v: "true" if v else "false"
    return f"minecraft:{mat}_fence[east={b(e)},north={b(n)},south={b(s)},waterlogged=false,west={b(w)}]"

def pane(mat, n=False, e=False, s=False, w=False):
    b = lambda v: "true" if v else "false"
    return f"minecraft:{mat}[east={b(e)},north={b(n)},south={b(s)},waterlogged=false,west={b(w)}]"

def wall(mat, n="none", e="none", s="none", w="none", up=True):
    return f"minecraft:{mat}_wall[east={e},north={n},south={s},up={'true' if up else 'false'},waterlogged=false,west={w}]"

def log(mat, axis="y"):
    return f"minecraft:{mat}[axis={axis}]"

def trapdoor(mat, facing, half="bottom", open_=False):
    return (f"minecraft:{mat}_trapdoor[facing={facing},half={half},open={'true' if open_ else 'false'},"
            f"powered=false,waterlogged=false]")

def candle(n=1, color="white", lit_=True):
    name = f"{color}_candle" if color else "candle"
    return f"minecraft:{name}[candles={n},lit={'true' if lit_ else 'false'},waterlogged=false]"

LANTERN_HANG = "minecraft:lantern[hanging=true,waterlogged=false]"
LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
SOUL_HANG = "minecraft:soul_lantern[hanging=true,waterlogged=false]"
SOUL = "minecraft:soul_lantern[hanging=false,waterlogged=false]"
BARREL = "minecraft:barrel[facing=up,open=false]"
def barrel(facing="up"):
    return f"minecraft:barrel[facing={facing},open=false]"
def chain(axis="y"):
    return f"minecraft:iron_chain[axis={axis},waterlogged=false]"
def ladder(facing):
    return f"minecraft:ladder[facing={facing},waterlogged=false]"
def lichen(down=False, up=False, n=False, s=False, e=False, w=False):
    b = lambda v: "true" if v else "false"
    return (f"minecraft:glow_lichen[down={b(down)},east={b(e)},north={b(n)},south={b(s)},up={b(up)},"
            f"waterlogged=false,west={b(w)}]")
def vine_plant(berries=True):
    return f"minecraft:cave_vines_plant[berries={'true' if berries else 'false'}]"
def vine_tip(berries=True):
    return f"minecraft:cave_vines[age=25,berries={'true' if berries else 'false'}]"
def pickle(n=4, wet=True):
    return f"minecraft:sea_pickle[pickles={n},waterlogged={'true' if wet else 'false'}]"
def bone(axis="y"):
    return f"minecraft:bone_block[axis={axis}]"
def hay(axis="y"):
    return f"minecraft:hay_block[axis={axis}]"
def wood(mat, axis="y"):
    return f"minecraft:{mat}[axis={axis}]"
WATER = "minecraft:water[level=0]"
AIR = None

FACE_DIRS = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


def is_solid(b):
    """A cell the contract and the faces read as standing material."""
    if b is None:
        return False
    if isinstance(b, dict):
        return True                      # a palette role is always a full block here
    for s in ("water", "lantern", "candle", "torch", "_fence", "_pane", "iron_bars", "chain",
              "ladder", "glow_lichen", "cave_vines", "sea_pickle", "carpet", "_slab", "_stairs",
              "_trapdoor", "_wall[", "flower_pot", "rail", "_button", "lever", "cobweb", "button",
              "end_rod", "lightning_rod", "pointed_dripstone", "sculk_vein", "_sign", "banner",
              "bell", "skull", "head", "kelp", "seagrass", "scaffolding", "_door"):
        if s in b:
            return False
    return True


def _cls(b):
    """The engine's collision class (crates/dsl/src/blockshape.rs), as far as this kit uses it."""
    if b is None:
        return "air"
    if isinstance(b, dict):
        return "full"
    if "water" in b and "waterlogged" not in b or "seagrass" in b or "kelp" in b:
        return "fluid"
    for t in ("candle", "carpet", "torch", "pressure_plate", "_button", "_sign", "banner", "flower_pot",
              "cobweb", "short_grass", "fern", "glow_lichen", "cave_vines", "rail", "sea_pickle", "skull",
              "moss_carpet", "lever", "vine", "dead_bush", "lily_pad", "leaf_litter", "sculk_vein",
              "red_mushroom[", "brown_mushroom[", "minecraft:red_mushroom", "minecraft:brown_mushroom"):
        if t in b and "mushroom_block" not in b:
            return "thin"
    if "_trapdoor" in b and "open=false" in b and "half=bottom" in b:
        return "thin"
    if "_fence_gate" in b:
        return "gate"
    if "_fence" in b or "_wall[" in b:
        return "barrier"
    if "_slab" in b and "type=bottom" in b:
        return "partial"
    if "lantern" in b or "_bed[" in b:
        return "partial"
    return "full"

def passable(b):
    return _cls(b) in ("air", "thin", "gate")

def floor_block(b):
    return _cls(b) in ("partial", "full")

def standable(p, c):
    x, y, z = c
    if y < 1:
        return False
    if not floor_block(p.g.get((x, y - 1, z))):
        return False
    if not passable(p.g.get(c)):
        return False
    up = (x, y + 1, z)
    return p.inb(*up) and passable(p.g.get(up))

def components(cells):
    cells = set(cells); out = []
    while cells:
        seed = cells.pop(); comp = {seed}; st = [seed]
        while st:
            x, y, z = st.pop()
            for d in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                n = (x+d[0], y+d[1], z+d[2])
                if n in cells:
                    cells.remove(n); comp.add(n); st.append(n)
        out.append(comp)
    return out


class Place:
    def __init__(self, stem, envelope=None):
        self.stem = stem
        a = allocation(stem)
        self.alloc = a
        self.W, self.H, self.L = a["extent"]
        self.datum = a["datum_y"]
        self.wmin = a["world_min"]
        self.g = {}
        self.cl = {}
        self.struct = set()
        self.marks = []
        self.palette = {}
        self.extra_spaces = {}
        self.extra_edges = []
        self.no_body = {}
        self.envelope = envelope
        self.main = "room"
        self.seams = a["seams"]
        self.owed = [o.split("/", 1)[-1] for o in a["owed_anchors"]]

    # -- grid --------------------------------------------------------------
    def inb(self, x, y, z):
        return 0 <= x < self.W and 0 <= y < self.H and 0 <= z < self.L

    def put(self, x, y, z, b, struct=None, claim=None):
        if not self.inb(x, y, z):
            return
        self.g[(x, y, z)] = b
        if struct is None:
            struct = is_solid(b)
        if struct:
            self.struct.add((x, y, z))
        else:
            self.struct.discard((x, y, z))
        if claim is not None:
            self.cl[(x, y, z)] = claim
        elif not passable(b):
            self.cl.pop((x, y, z), None)

    def get(self, x, y, z):
        return self.g.get((x, y, z))

    def box(self, x0, y0, z0, x1, y1, z1, b, struct=None, claim=None):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.put(x, y, z, b(x, y, z) if callable(b) else b, struct, claim)

    def clear(self, x0, y0, z0, x1, y1, z1):
        self.box(x0, y0, z0, x1, y1, z1, None, struct=False)

    def role(self, name, paint):
        self.palette[name] = paint
        return {"role": name}

    def mark(self, stem, pos, facing=None):
        self.marks.append((stem, tuple(pos), facing))

    # -- seams -------------------------------------------------------------
    def seam_cells(self, s):
        """The allocation hands a seam as its corner cells; the opening is the box between."""
        cs = s["cells"]
        lo = [min(c[i] for c in cs) for i in range(3)]; hi = [max(c[i] for c in cs) for i in range(3)]
        return [(x, y, z) for x in range(lo[0], hi[0] + 1) for y in range(lo[1], hi[1] + 1)
                for z in range(lo[2], hi[2] + 1)]

    def seam_box(self, s):
        cs = self.seam_cells(s)
        return ([min(c[i] for c in cs) for i in range(3)], [max(c[i] for c in cs) for i in range(3)])

    def seam(self, edge_stem):
        for s in self.seams:
            if s["edge"].split("/", 1)[1] == edge_stem:
                return s
        raise KeyError(edge_stem)

    def cut_seams(self, floor=None):
        """Open every allocated way: its cells air, claimed as the way; the cell under the lowest
        course of each is made floor if the builder left it open."""
        for s in self.seams:
            name = "way-" + s["edge"].split("/", 1)[1]
            lo, hi = self.seam_box(s)
            dx, dz = {"north": (0, 1), "south": (0, -1), "west": (1, 0), "east": (-1, 0)}[s["face"]]
            for (x, y, z) in self.seam_cells(s):
                self.put(x, y, z, None, struct=False, claim=name)
                if y == lo[1] and floor is not None:
                    below = self.get(x, y - 1, z)
                    if below is None or not is_solid(below):
                        self.put(x, y - 1, z, floor, struct=True)
                # the cell just inside the opening is kept clear, so the way meets the room
                ix, iz = x + dx, z + dz
                if self.inb(ix, y, iz) and not passable(self.get(ix, y, iz)):
                    self.put(ix, y, iz, None, struct=False)

    def way_names(self):
        return ["way-" + s["edge"].split("/", 1)[1] for s in self.seams]

    # -- contract ----------------------------------------------------------
    def space(self, name, envelope):
        self.extra_spaces[name] = {"envelope": envelope}

    def claim(self, name, x0, y0, z0, x1, y1, z1, envelope=None):
        """Claim every passable cell of the box for `name` (a space when `envelope` is given),
        leaving the ways' cells alone."""
        if envelope:
            self.space(name, envelope)
        ways = set(self.way_names())
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    if self.inb(x, y, z) and passable(self.g.get((x, y, z))) and self.cl.get((x, y, z)) not in ways:
                        self.cl[(x, y, z)] = name

    def stair_edge(self, via, lower, upper):
        self.transits = getattr(self, "transits", {})
        self.transits[via] = (lower, upper)

    def default_claims(self):
        """Every passable cell above the floor course that no builder claimed belongs to the
        main space."""
        for x in range(self.W):
            for y in range(1, self.H):
                for z in range(self.L):
                    if (x, y, z) in self.cl:
                        continue
                    if passable(self.g.get((x, y, z))):
                        self.cl[(x, y, z)] = self.main

    def fold_strays(self):
        """Air left to the main space that does not join its floor (a pocket over a door's
        head, a cell over a flight) belongs to whatever region it touches."""
        main = {c for c, r in self.cl.items() if r == self.main}
        if not main:
            return
        st = self.standables()
        comps = components(main)
        keep = [c for c in comps if c & st]
        if not keep:
            return
        ways = set(self.way_names())
        for comp in comps:
            if comp in keep:
                continue
            votes = {}
            for (x, y, z) in comp:
                for d in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                    r = self.cl.get((x+d[0], y+d[1], z+d[2]))
                    if r and r != self.main and r not in ways:
                        votes[r] = votes.get(r, 0) + 1
            if votes:
                r = sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
                for c in comp:
                    self.cl[c] = r

    def standables(self):
        out = set()
        for x in range(self.W):
            for z in range(self.L):
                for y in range(1, self.H):
                    if standable(self, (x, y, z)):
                        out.add((x, y, z))
        return out

    def settle_contract(self):
        """Read the claims back as the engine will: split an open space's roofed cells into
        their own closed spaces, give the tops of lamps and walls nobody stands on to an
        out-of-walk region, and report every space whose floor spans more than two levels."""
        spaces = {self.main: self.envelope}
        spaces.update({k: v["envelope"] for k, v in self.extra_spaces.items()})
        st = self.standables()
        self.problems = []
        under_n = 0
        for name, env in list(spaces.items()):
            cells = {c for c, r in self.cl.items() if r == name}
            if not cells:
                continue
            if env in ("open", "open_top"):
                covered = {c for c in cells
                           if any(self.g.get((c[0], yy, c[2])) is not None for yy in range(c[1] + 1, self.H))}
                comps = components(covered)
                for comp in comps:
                    if not (comp & st):
                        continue                # roofed air nobody stands in stays open
                    under_n += 1
                    nm = f"{name}-under-{under_n}"
                    self.extra_spaces[nm] = {"envelope": "enclosed"}
                    for c in comp:
                        self.cl[c] = nm
                    self.extra_edges.append({"a": name, "b": nm, "class": "walk", "rise": "auto"})
                cells = {c for c, r in self.cl.items() if r == name}
                sts = sorted(c for c in cells if c in st)
                if sts:
                    f = min(c[1] for c in sts)
                    for c in sts:
                        if c[1] > f + 1 and all(passable(self.g.get((c[0], yy, c[2]))) for yy in range(c[1], self.H)):
                            self.cl[c] = "tops"
                            self.no_body["tops"] = {"reason": "the tops of posts, lamps, walls and banks, which nobody stands on"}
        # every space: one floor
        allsp = {self.main: self.envelope}
        allsp.update({k: v["envelope"] for k, v in self.extra_spaces.items()})
        for name in allsp:
            sts = [c for c, r in self.cl.items() if r == name and c in st]
            if sts:
                lv = sorted({c[1] for c in sts})
                if lv[-1] - lv[0] > 1:
                    hi = [c for c in sts if c[1] > lv[0] + 1][:6]
                    self.problems.append(f"space {name}: standable levels {lv}; e.g. {hi}")
        unc = sorted(c for c in st if c not in self.cl)
        if unc:
            self.problems.append(f"unclaimed standable cells: {len(unc)} e.g. {unc[:6]}")

    def min_y(self, name):
        ys = [c[1] for c, r in self.cl.items() if r == name]
        return min(ys) if ys else 0

    def contract(self):
        spaces = {self.main: {"envelope": self.envelope}}
        spaces.update(self.extra_spaces)
        edges = []
        seam_space = getattr(self, "seam_space", {})
        for s in self.seams:
            name = "way-" + s["edge"].split("/", 1)[1]
            edges.append({"a": "exterior", "b": seam_space.get(name, self.main), "class": "walk", "via": name})
        for e in self.extra_edges:
            e = dict(e)
            if e.get("rise") == "auto":
                e["rise"] = self.min_y(e["b"]) - self.min_y(e["a"])
            edges.append(e)
        for via, (lo, up) in sorted(getattr(self, "transits", {}).items()):
            edges.append({"a": lo, "b": up, "class": "stair", "rise": self.min_y(up) - self.min_y(lo), "via": via})
        entry = getattr(self, "entry", self.main)
        return {"entry": entry, "spaces": spaces, "no_body": self.no_body, "edges": edges}

    def shown_faces(self):
        W, H, L = self.W, self.H, self.L
        sides = {
            "north": [(x, y, 0) for x in range(W) for y in range(H)],
            "south": [(x, y, L - 1) for x in range(W) for y in range(H)],
            "west": [(0, y, z) for y in range(H) for z in range(L)],
            "east": [(W - 1, y, z) for y in range(H) for z in range(L)],
            "up": [(x, H - 1, z) for x in range(W) for z in range(L)],
            "down": [(x, 0, z) for x in range(W) for z in range(L)],
        }
        return [k for k in ("north", "south", "east", "west", "up", "down")
                if any(is_solid(self.g.get(c)) for c in sides[k])]

    # -- emission ----------------------------------------------------------
    def cell(self, x, y, z):
        return (self.g.get((x, y, z)), self.cl.get((x, y, z)))

    def program(self):
        if self.envelope is None:
            raise ValueError("envelope unset")
        self.default_claims()
        self.fold_strays()
        self.settle_contract()
        for pr in self.problems:
            print(f"  CONTRACT {self.stem}: {pr}")
        body = encode(self)
        for stem, (x, y, z), facing in sorted(self.marks, reverse=True):
            m = {"anchor": stem, "at": "offset", "x": lit(x), "y": lit(y), "z": lit(z)}
            if facing:
                m["facing"] = facing
            body = {"op": "mark", "mark": m, "body": body}
        return {
            "version": "1.9.0", "name": self.stem, "start": "place", "params": {},
            "palette": self.palette,
            "rules": {"place": [{"weight": 1, "body": body}]},
            "contract": self.contract(),
            "shown_faces": self.shown_faces(),
        }

    def write(self):
        prog = self.program()
        path = os.path.join(CAMP, "programs", f"{self.stem}.json")
        with open(path, "w") as f:
            json.dump(prog, f, indent=1, sort_keys=True)
            f.write("\n")
        return path


# ---- run-length encoding to a split tree ------------------------------------
def leaf(cell):
    block, claim = cell
    body = {"op": "void"} if block is None else {"op": "fill", "material": block}
    if claim:
        body = {"op": "claim", "region": claim, "body": body}
    return body

def runs(items):
    out = []
    for it in items:
        k = json.dumps(it, sort_keys=True)
        if out and out[-1][0] == k:
            out[-1][2] += 1
        else:
            out.append([k, it, 1])
    return [(it, n) for _, it, n in out]

def split(axis, items):
    rs = runs(items)
    if len(rs) == 1:
        return rs[0][0]
    return {"op": "split", "axis": axis,
            "sizes": [{"size": "absolute", "blocks": lit(n)} for _, n in rs],
            "children": [it for it, _ in rs]}

def encode(p):
    def col(x, z):
        return split("y", [leaf(p.cell(x, y, z)) for y in range(p.H)])
    def row(z):
        return split("x", [col(x, z) for x in range(p.W)])
    return split("z", [row(z) for z in range(p.L)])


def main(builders):
    """argv: delvec binary, prefab library, place stems (default: every builder)."""
    global DELVEC, PREFABS
    if len(sys.argv) >= 3:
        DELVEC, PREFABS = sys.argv[1], sys.argv[2]
    stems = sys.argv[3:] or sorted(builders)
    for stem in stems:
        p = builders[stem]()
        print("wrote", os.path.relpath(p.write(), CAMP))
        light_report(p)


# ---- a light estimate, for the builder's own loop (the engine's probe is the verdict) ----
EMIT = (("soul_lantern", 10), ("lantern", 15), ("soul_torch", 10), ("torch", 14), ("sea_lantern", 15),
        ("shroomlight", 15), ("froglight", 15), ("glowstone", 15), ("campfire", 15),
        ("glow_lichen", 7), ("crying_obsidian", 10), ("magma_block", 3), ("end_rod", 14),
        ("redstone_lamp[lit=true", 15), ("copper_bulb[lit=true", 15), ("jack_o_lantern", 15))

def emission(b):
    if not isinstance(b, str):
        return 0
    if "cave_vines" in b:
        return 14 if "berries=true" in b else 0
    if "sea_pickle" in b:
        n = int(b.split("pickles=")[1][0])
        return 3 + 3 * n if "waterlogged=true" in b else 0
    if "candle" in b and "lit=true" in b:
        return 3 * int(b.split("candles=")[1][0])
    for k, v in EMIT:
        if k in b:
            return v
    return 0

def opaque(b):
    if b is None or isinstance(b, dict):
        return b is not None
    if emission(b):
        return False
    return is_solid(b) and "glass" not in b and "leaves" not in b and "barrel" not in b

def light_report(p, floor_ok=None, quiet=False):
    """Block light at every standable cell (body cell air-ish, below solid, head clear); prints
    the count under 7 and the darkest few."""
    import collections
    lvl = {}
    q = collections.deque()
    for c, b in p.g.items():
        e = emission(b)
        if e:
            lvl[c] = e; q.append(c)
    while q:
        c = q.popleft(); v = lvl[c] - 1
        if v <= 0:
            continue
        x, y, z = c
        for d in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            n = (x+d[0], y+d[1], z+d[2])
            if not p.inb(*n) or opaque(p.g.get(n)):
                continue
            if lvl.get(n, 0) < v:
                lvl[n] = v; q.append(n)
    stand = []
    for x in range(p.W):
        for z in range(p.L):
            for y in range(1, p.H):
                b, below, head = p.g.get((x, y, z)), p.g.get((x, y-1, z)), p.g.get((x, y+1, z))
                if is_solid(b) or not (is_solid(below) or (isinstance(below, str) and ("_slab" in below or "_stairs" in below))):
                    continue
                if isinstance(b, str) and "water" in b:
                    continue
                if y + 1 < p.H and is_solid(head):
                    continue
                stand.append(((x, y, z), lvl.get((x, y, z), 0)))
    # keep only what a body reaches from the ways in (up one, down three)
    ss = {c for c, _ in stand}
    seeds = [c for c in ss if any(c in p.seam_cells(s) for s in p.seams)]
    if not seeds:
        seeds = [c for c in ss if any(abs(c[0]-x)+abs(c[2]-z) <= 1 and abs(c[1]-y) <= 1
                                      for s in p.seams for (x, y, z) in p.seam_cells(s))]
    reach = set(seeds); q2 = collections.deque(seeds)
    while q2:
        x, y, z = q2.popleft()
        for dx, dz in ((1,0),(-1,0),(0,1),(0,-1)):
            for dy in (1, 0, -1, -2, -3):
                n = (x+dx, y+dy, z+dz)
                if n in ss and n not in reach:
                    reach.add(n); q2.append(n); break
    stand = [s for s in stand if s[0] in reach]
    dark = sorted([s for s in stand if s[1] < 7], key=lambda s: s[1])
    if not quiet:
        print(f"  light estimate {p.stem}: {len(stand)} standable, {len(dark)} under 7"
              + (f"; darkest {dark[:6]}" if dark else ""))
    return dark
