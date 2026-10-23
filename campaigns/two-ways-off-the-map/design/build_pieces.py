#!/usr/bin/env python3
"""Write the three place programs of Two Ways Off the Map.

    delvec allocation campaigns/two-ways-off-the-map --all --prefabs prefabs > alloc.json
    python3 campaigns/two-ways-off-the-map/design/build_pieces.py alloc.json [--yard-as-found] [--jetty-as-found] [--sixth]

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place. Each piece is stated here as a cell grid in the frame's
own coordinates (x east, y up, z south, the frame's minimum corner at 0) and
written out as a grammar program: the grid is cut along x into runs of
identical slices, each slice along z, each column along y, so every leaf is one
material over one box, wrapped in the contract region it belongs to.

The allocation is read, never copied: the frame's extent, the voids, the walk
plane and every seam's handed cells come from it.

The three flags write the shapes the engine refused, kept so each refusal in
`GENERATION.md` can be reproduced: `--yard-as-found` puts the stone where a
sprint jump reaches the buttress from it; `--jetty-as-found` leaves out the
stair into the water; `--sixth` breaks the last platform with a gap of four
columns for the sixth jump. Without them the script writes the shipped level.
"""
import json
import pathlib
import sys

VERSION = "1.12.0"
SKIP = "__skip__"
SEA_TOP_WORLD_Y = 62  # the ocean horizon's top water course


class Piece:
    def __init__(self, alloc):
        self.sx, self.sy, self.sz = alloc["extent"]
        self.alloc = alloc
        self.block = {}
        self.claim = {}
        self.fixed = set()
        for v in alloc["voids"]:
            (a, b) = v["cells"]
            for c in box(a, b):
                self.block[c] = SKIP
                self.fixed.add(c)
        # The ground the whole hands this place: each column's blocks, laid
        # from the column's top down.
        for col in alloc["ground"]["columns"]:
            for i, b in enumerate(col["blocks"]):
                c = (col["x"], col["top"] - i, col["z"])
                if c not in self.fixed:
                    self.block[c] = GROUND[b]
        self.walk = alloc["space"][0][1]
        self.sea = SEA_TOP_WORLD_Y - alloc["world_min"][1]

    def seam(self, edge):
        for s in self.alloc["seams"]:
            if s["edge"] == edge:
                return s
        raise KeyError(edge)

    def put(self, lo, hi, role):
        for c in box(lo, hi):
            if c in self.fixed:
                continue
            if not (0 <= c[0] < self.sx and 0 <= c[1] < self.sy and 0 <= c[2] < self.sz):
                raise SystemExit(f"{c} is outside the frame {self.sx, self.sy, self.sz}")
            self.block[c] = role

    def get(self, c):
        return self.block.get(c)

    def claim_box(self, lo, hi, region, air_only=False):
        for c in box(lo, hi):
            if c in self.fixed or c in self.claim:
                continue
            if air_only and self.block.get(c) is not None:
                continue
            self.claim[c] = region

    def cell(self, x, y, z):
        return (self.block.get((x, y, z)), self.claim.get((x, y, z)))

    def connect(self, palette, kind="fence"):
        """Give every fence the connections its neighbours give it: another
        fence, or a full block."""
        def joins(c):
            r = self.block.get(c)
            if r in (None, SKIP):
                return False
            return r.startswith(kind) or palette.get(r, "").split("[")[0] in FULL
        for (x, y, z), r in sorted(self.block.items()):
            if r != kind:
                continue
            n, e, s, w = (joins((x, y, z - 1)), joins((x + 1, y, z)), joins((x, y, z + 1)), joins((x - 1, y, z)))
            name = f"{kind}-{'n' if n else ''}{'e' if e else ''}{'s' if s else ''}{'w' if w else ''}"
            b = lambda v: "true" if v else "false"
            palette[name] = f"minecraft:spruce_fence[east={b(e)},north={b(n)},south={b(s)},waterlogged=false,west={b(w)}]"
            self.block[(x, y, z)] = name

    @staticmethod
    def runs(keys):
        out = []
        for k in keys:
            if out and out[-1][0] == k:
                out[-1][1] += 1
            else:
                out.append([k, 1])
        return out

    @staticmethod
    def split(axis, runs, child):
        if len(runs) == 1:
            return child(runs[0])
        return {
            "axis": axis,
            "children": [child(r) for r in runs],
            "op": "split",
            "sizes": [{"blocks": {"expr": "int", "value": n}, "size": "absolute"} for _, n in runs],
        }

    @staticmethod
    def leaf(cell):
        role, region = cell
        if role == SKIP:
            body = {"op": "skip"}
        elif role is None:
            body = {"op": "void"}
        else:
            body = {"material": {"role": role}, "op": "fill"}
        if region is None:
            return body
        return {"body": body, "op": "claim", "region": region}

    def body(self):
        def column(x, z):
            cells = [self.cell(x, y, z) for y in range(self.sy)]
            return self.split("y", self.runs(cells), lambda r: self.leaf(r[0]))

        def slab(x):
            cols = [tuple(self.cell(x, y, z) for y in range(self.sy)) for z in range(self.sz)]
            starts, z = [], 0
            for key, n in self.runs(cols):
                starts.append((key, n, z))
                z += n
            return self.split("z", [[(k, z0), n] for k, n, z0 in starts],
                              lambda r: column(x, r[0][1]))

        slabs = [tuple(tuple(self.cell(x, y, z) for y in range(self.sy)) for z in range(self.sz))
                 for x in range(self.sx)]
        starts, x = [], 0
        for key, n in self.runs(slabs):
            starts.append((key, n, x))
            x += n
        return self.split("x", [[(k, x0), n] for k, n, x0 in starts], lambda r: slab(r[0][1]))


FULL = {
    "minecraft:stone_bricks", "minecraft:mossy_stone_bricks", "minecraft:cracked_stone_bricks",
    "minecraft:cobblestone", "minecraft:mossy_cobblestone", "minecraft:stone", "minecraft:andesite",
    "minecraft:spruce_planks", "minecraft:stripped_spruce_log", "minecraft:deepslate_tiles",
    "minecraft:polished_andesite", "minecraft:grass_block", "minecraft:dirt",
}


def box(a, b):
    return [(x, y, z)
            for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1)
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1)
            for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1)]


def program(name, piece, palette, contract, marks, shown):
    body = piece.body()
    for m in marks:
        stem, pos, facing = m[0], m[1], m[2]
        mark = {
            "anchor": stem, "at": "offset", "facing": facing,
            "x": {"expr": "int", "value": pos[0]},
            "y": {"expr": "int", "value": pos[1]},
            "z": {"expr": "int", "value": pos[2]},
        }
        if len(m) > 3:
            mark["role"] = m[3]
        body = {"body": body, "mark": mark, "op": "mark"}
    used = {r for r in piece.block.values() if r not in (None, SKIP)}
    return {
        "contract": contract,
        "name": name,
        "palette": {k: v for k, v in sorted(palette.items()) if k in used},
        "params": {},
        "rules": {"place": [{"body": body, "weight": 1}]},
        "shown_faces": shown,
        "start": "place",
        "version": VERSION,
    }


GROUND = {"minecraft:gravel": "gravel"}

BASE = {
    "cobble": "minecraft:cobblestone",
    "deck": "minecraft:spruce_planks",
    "dirt": "minecraft:dirt",
    "grass": "minecraft:grass_block[snowy=false]",
    "glass": "minecraft:white_stained_glass",
    "gravel": "minecraft:gravel",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lid": "minecraft:deepslate_tiles",
    "log": "minecraft:stripped_spruce_log[axis=y]",
    "mossy": "minecraft:mossy_stone_bricks",
    "plank": "minecraft:spruce_planks",
    "rock": "minecraft:stone",
    "stone": "minecraft:mossy_cobblestone",
    "wall": "minecraft:stone_bricks",
    "water": "minecraft:water[level=0]",
}


def masonry(x, y, z):
    """A deterministic weathering of the walls: mossy here and there."""
    return "mossy" if (x * 7 + y * 13 + z * 5) % 9 == 0 else "wall"


def yard(a, as_found, stone_at=None):
    """The chapel yard (spec-0113's Bell yard, rebuilt). Its inner yard is
    walled three high; the stone stands one high near the buttress, which
    stands two high against the east wall; past the east wall is the old
    burying ground, walled five high on every side."""
    p = Piece(a)
    W = p.walk
    sx, sz = p.sx, p.sz
    # The rock under everything, the grass on top.
    p.put((0, 1, 0), (sx - 1, W - 4, sz - 1), "rock")
    p.put((0, W - 3, 0), (sx - 1, W - 2, sz - 1), "dirt")
    p.put((0, W - 1, 0), (sx - 1, W - 1, sz - 1), "grass")
    east = 14  # the inner yard's east wall
    # The inner yard's walls, three high: west and south on the ring, east at x 14.
    for z in range(0, sz):
        for y in range(W, W + 3):
            p.put((0, y, z), (0, y, z), masonry(0, y, z))
            p.put((east, y, z), (east, y, z), masonry(east, y, z))
    # The south wall is the cistern's north wall too, and stands six high
    # over the whole of the cistern's open height.
    for x in range(0, sx):
        for y in range(W, W + 6):
            p.put((x, y, sz - 1), (x, y, sz - 1), masonry(x, y, sz - 1))
    # The chapel's south wall is the yard's north side, roofless and ruined,
    # its gable stepping up over the middle, two glazed lancets high in it.
    for x in range(0, east + 1):
        top = W + 6
        if 2 <= x <= east - 2:
            top = W + 7
        if 4 <= x <= east - 4:
            top = W + 8
        if 6 <= x <= east - 6:
            top = W + 9
        p.put((x, W, 0), (x, top, 0), "wall")
    for x in (4, east - 4):
        p.put((x, W + 3, 0), (x, W + 5, 0), "glass")
    # The burying ground: the strip past the east wall, walled five high.
    for z in range(0, sz):
        p.put((sx - 1, W, z), (sx - 1, W + 4, z), "wall")
    for x in range(east + 1, sx):
        p.put((x, W, 0), (x, W + 4, 0), "wall")
    # The gate onto the wall-walk: the seam's cells, open.
    s = p.seam("edge/yard-gate")
    (g0, g1) = s["cells"]
    p.put(g0, g1, None)
    p.claim_box(g0, g1, "yard-gate")
    # The buttress, two high, against the east wall; and the stone.
    p.put((12, W, 12), (13, W + 1, 12), "wall")
    stone = (10, W, 10) if as_found else (9, W, 10)
    if stone_at is not None:
        stone = (stone_at[0], W, stone_at[1])
    p.put(stone, stone, "stone")
    # The other standing stones, well away from the walls and the buttress.
    for (x, z) in ((4, 6), (6, 11), (7, 4), (3, 9)):
        p.put((x, W, z), (x, W, z), "stone")
    # A gravel path from the gate in.
    for z in range(9, sz - 1):
        for x in (3, 4, 5):
            if p.get((x, W, z)) is None:
                p.put((x, W - 1, z), (x, W - 1, z), "gravel")
    # Contract regions: the yard, the buttress's top, the burying ground, and
    # the tops of the walls.
    p.claim_box((12, W + 2, 12), (13, p.sy - 1, 12), "buttress-top", air_only=True)
    p.claim_box((1, W, 1), (east - 1, p.sy - 1, sz - 2), "yard", air_only=True)
    p.claim_box((east + 1, W, 1), (sx - 2, p.sy - 1, sz - 2), "burying-ground", air_only=True)
    p.claim_box((0, W, 0), (sx - 1, p.sy - 1, sz - 1), "wall-top", air_only=True)
    contract = {
        "edges": [{"a": "yard", "b": "exterior", "class": "walk", "via": "yard-gate"}],
        "entry": "yard",
        "no_body": {
            "buttress-top": {"reason": "the top of the buttress against the yard's east wall; nobody is meant to stand on it"},
            "burying-ground": {"reason": "the old burying ground past the yard's east wall, walled five high on every side; nobody is meant to get in"},
            "wall-top": {"reason": "the tops of the yard's walls and of the chapel's ruined south wall; nobody is meant to get up there"},
        },
        "spaces": {"yard": {"envelope": "open"}},
    }
    marks = [
        ("spawn", (4, W, 3), "south", "entry"),
        ("node-yard", (6, W, 8), "south"),
    ]
    return program("two-ways-off-the-map-yard", p, dict(BASE), contract, marks, ["east", "north", "south", "up", "west"])


# The wall-walk's platforms, west to east: (x0, x1, walk rise over the grade).
def platforms(sixth):
    last = [(45, 51, 0), (56, 58, 0)] if sixth else [(45, 58, 0)]
    # The last platform widens to the cistern's full width at its far end,
    # where the far stair comes up out of the cistern onto it.
    return [(1, 9, 0), (11, 16, 0), (19, 24, 0), (28, 33, 0), (36, 41, 1)] + last


def course(a, sixth):
    """The broken wall-walk over a dry cistern: platforms three wide in a row
    down the cistern's middle, gaps of one, two, three, two (up one) and three
    (down one, under the lid) columns between them, the cistern's floor three
    below, and a stair at each end back up out of it. The raised fourth
    platform is reached only by the four leaps before it, and left only by the
    fifth, under the lid."""
    p = Piece(a)
    W = p.walk
    sx, sz = p.sx, p.sz
    pit = W - 3
    top = W + 3  # the cistern walls' top course
    p.put((0, 1, 0), (sx - 1, pit - 1, sz - 1), "rock")
    # The cistern walls on the ring, up to four over the grade.
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                for y in range(pit, top + 1):
                    p.put((x, y, z), (x, y, z), masonry(x, y, z))
    # The first platform: the whole width, the gate onto it from the yard.
    plats = platforms(sixth)
    x0, x1, _ = plats[0]
    p.put((x0, pit, 1), (x1, W - 1, sz - 2), "wall")
    # The others: the middle three cells of the width.
    for (x0, x1, rise) in plats[1:]:
        p.put((x0, pit, 3), (x1, W - 1 + rise, 5), "wall")
        p.put((x0, W - 1 + rise, 3), (x1, W - 1 + rise, 5), "cobble")
    # The last platform's far end, the whole width.
    fx0 = plats[-1][1] - 2
    p.put((fx0, pit, 1), (plats[-1][1], W - 1, sz - 2), "wall")
    # The stairs up out of the cistern: against the south wall at the near
    # end, rising west onto the first platform; against the north wall at the
    # far end, rising east onto the last.
    near = [(10, W - 1), (11, W - 2), (12, W - 3)]
    far = [(fx0 - 1, W - 1), (fx0 - 2, W - 2), (fx0 - 3, W - 3)]
    for (x, t) in near:
        p.put((x, pit, sz - 2), (x, t, sz - 2), "wall")
    for (x, t) in far:
        p.put((x, pit, 1), (x, t, 1), "wall")
    # The lid: a course of stone laid across the cistern's walls over the fifth
    # leap, three cells over the fourth platform's top.
    lid_y = W + 1 + 3
    p.put((37, lid_y, 0), (46, lid_y, sz - 1), "lid")
    # The seams: the gate from the yard (the first platform's cells, open) and
    # the gap in the east wall onto the jetty.
    for edge, region in (("edge/yard-gate", "yard-gate"), ("edge/jetty-foot", "jetty-foot")):
        (c0, c1) = p.seam(edge)["cells"]
        p.put(c0, c1, None)
        p.claim_box(c0, c1, region)
    # Contract regions.
    for (x, t) in near:
        p.claim_box((x, t + 1, sz - 2), (x, t + 3, sz - 2), "near-stair")
    for (x, t) in far:
        p.claim_box((x, t + 1, 1), (x, t + 3, 1), "far-stair")
    for (x0, x1, rise) in plats:
        p.claim_box((x0, W + rise, 3), (x1, p.sy - 1, 5), "wall-walk", air_only=True)
    p.claim_box((1, W, 1), (plats[0][1], p.sy - 1, sz - 2), "wall-walk", air_only=True)
    p.claim_box((fx0, W, 1), (plats[-1][1], p.sy - 1, sz - 2), "wall-walk", air_only=True)
    p.claim_box((1, pit, 1), (sx - 2, p.sy - 1, sz - 2), "cistern", air_only=True)
    p.claim_box((0, pit, 0), (sx - 1, p.sy - 1, sz - 1), "wall-top", air_only=True)
    contract = {
        "edges": [
            {"a": "wall-walk", "b": "exterior", "class": "walk", "via": "yard-gate"},
            {"a": "wall-walk", "b": "exterior", "class": "walk", "via": "jetty-foot"},
            {"a": "cistern", "b": "wall-walk", "class": "stair", "rise": 3, "via": "near-stair"},
            {"a": "cistern", "b": "wall-walk", "class": "stair", "rise": 3, "via": "far-stair"},
        ],
        "entry": "wall-walk",
        "no_body": {
            "wall-top": {"reason": "the tops of the cistern's walls and of the stone lid laid across them; nobody is meant to get up there"},
        },
        "no_body_majority_ack": "the cistern's walls stand four high round the whole wall-walk and the lid lies across them, so their tops, open to the sky and out of walk, outnumber the platforms a body crosses",
        "spaces": {"cistern": {"envelope": "open"}, "wall-walk": {"envelope": "open"}},
    }
    marks = [("node-course", (5, W, 4), "east")]
    launches = [(x1, rise) for (_, x1, rise) in plats[:-1]]
    lands = [(x0, rise) for (x0, _, rise) in plats[1:]]
    for k, ((lx, lr), (dx, dr)) in enumerate(zip(launches, lands), start=1):
        marks.append((f"launch-{k}", (lx, W + lr, 4), "east"))
        marks.append((f"land-{k}", (dx, W + dr, 4), "east"))
    hx0, hx1, hr = plats[4]
    marks.append(("high-platform", ((hx0 + hx1) // 2, W + hr, 4), "east"))
    return program("two-ways-off-the-map-course", p, dict(BASE), contract, marks, ["east", "north", "south", "up", "west"])


def jetty(a, as_found):
    """A plank jetty on spruce piles over the open sea, railed along both
    sides and across its head; the plank stands against the north rail, and a
    stair goes down off the south side into the water near the head."""
    p = Piece(a)
    W = p.walk
    sx, sz = p.sx, p.sz
    sea = p.sea
    # The sea under and round the deck, to its top course.
    p.put((0, 1, 0), (sx - 1, sea, sz - 1), "water")
    # The piles.
    for x in (2, 7, 12, 17, 21):
        for z in (1, sz - 2):
            p.put((x, 1, z), (x, W - 2, z), "log")
    # The deck, five wide, and the rails on its two edges and across its head.
    p.put((0, W - 1, 1), (sx - 2, W - 1, sz - 2), "deck")
    for x in range(0, sx - 1):
        p.put((x, W, 1), (x, W, 1), "fence")
        p.put((x, W, sz - 2), (x, W, sz - 2), "fence")
    for z in range(1, sz - 1):
        p.put((sx - 2, W, z), (sx - 2, W, z), "fence")
    # Lanterns on the head's corner posts.
    p.put((sx - 2, W + 1, 1), (sx - 2, W + 1, 1), "lantern")
    p.put((sx - 2, W + 1, sz - 2), (sx - 2, W + 1, sz - 2), "lantern")
    # The plank: a block of planks left against the north rail.
    plank = (10, W, 2)
    p.put(plank, plank, "plank")
    stair_cells = []
    landing = []
    if not as_found:
        # The stair into the water: a gap in the south rail at x 16, and steps
        # down eastward off the deck's south edge to below the water's top.
        p.put((16, W, sz - 2), (16, W, sz - 2), None)
        for i, x in enumerate(range(16, 22)):
            t = max(W - 2 - i, sea)  # the step's top block; the last two land at the water's top
            p.put((x, 1, sz - 1), (x, t - 1, sz - 1), "rock")
            p.put((x, t, sz - 1), (x, t, sz - 1), "plank")
            for y in range(t + 1, t + 4):
                p.put((x, y, sz - 1), (x, y, sz - 1), "water" if y <= sea else None)
            (landing if t == sea else stair_cells).append((x, t + 1, sz - 1))
        stair_cells.append((16, W, sz - 2))
    p.connect(BASE_JETTY)
    # The seam: the wall-walk's last platform, onto the deck.
    (c0, c1) = p.seam("edge/jetty-foot")["cells"]
    p.put(c0, c1, None)
    p.claim_box(c0, c1, "jetty-foot")
    for (x, y, z) in stair_cells:
        p.claim_box((x, y, z), (x, y + 2, z), "water-stair")
    for (x, y, z) in landing:
        p.claim_box((x, y, z), (x, y + 2, z), "landing")
    p.claim_box((plank[0], W + 1, plank[2]), (plank[0], p.sy - 1, plank[2]), "plank-top")
    p.claim_box((0, W, 2), (sx - 3, p.sy - 1, sz - 3), "deck", air_only=True)
    p.claim_box((0, W, 0), (sx - 1, p.sy - 1, sz - 1), "rail-top", air_only=True)
    edges = [{"a": "deck", "b": "exterior", "class": "walk", "via": "jetty-foot"}]
    if not as_found:
        edges.append({"a": "landing", "b": "deck", "class": "stair", "rise": 5, "via": "water-stair"})
    contract = {
        "edges": edges,
        "entry": "deck",
        "no_body": {
            "plank-top": {"reason": "the top of the plank left against the north rail; nobody is meant to stand on it"},
            "rail-top": {"reason": "the tops of the jetty's rails and of the lanterns on its head; nobody is meant to stand on them"},
        },
        "spaces": dict({"deck": {"envelope": "open"}}, **({} if as_found else {"landing": {"envelope": "open"}})),
    }
    marks = [
        ("node-jetty", (3, W, 3), "east"),
        ("jetty-head", (sx - 4, W, 3), "east"),
    ]
    return program("two-ways-off-the-map-jetty", p, BASE_JETTY, contract, marks, ["east", "north", "south", "west"])


BASE_JETTY = dict(BASE)


def main():
    args = sys.argv[1:]
    flags = {a for a in args if a.startswith("--")}
    # `--stone=X,Z` stands the stone at another cell of the yard (a probe of
    # where a sprint jump still reaches the buttress from it).
    stone_at = next((tuple(int(v) for v in a.split("=", 1)[1].split(",")) for a in flags if a.startswith("--stone=")), None)
    files = [a for a in args if not a.startswith("--")]
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(files[0]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    builds = (
        ("yard", lambda h: yard(h, "--yard-as-found" in flags, stone_at)),
        ("course", lambda h: course(h, "--sixth" in flags)),
        ("jetty", lambda h: jetty(h, "--jetty-as-found" in flags)),
    )
    for stem, build in builds:
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
