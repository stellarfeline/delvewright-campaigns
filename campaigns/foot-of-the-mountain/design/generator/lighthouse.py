#!/usr/bin/env python3
"""The starter generator for ONE place: an empty-but-correct program, read off its allocation.

`scripts/handout.py` copies this file beside every handout, with the place's
allocation saved next to it, so a place's author starts from a program that
already passes `delvec detail --check` and builds the place into it — never
from research. Run it as the handout prints it:

    "$DELVEWRIGHT_PYTHON" starter.py --allocation allocation.json --out <campaign>/programs/<stem>.json

It runs no binary and names no path: it reads the allocation `delvec allocation
<campaign> <place>` printed and writes the program. What it emits, for any
allocation the engine hands:

- the ground: a ground place's floor drawn down to the bottom of its claim; an
  aloft place's one floor course under its walk plane and nothing beneath;
- a wall on every cell of the one-cell ring, from the walk plane up — a cell a
  neighbour or the whole owns is a void the verb replaces, so painting it is
  harmless and nothing depends on it — except on a side the place declares
  open, whose ring run (its two corners excluded) is left open from the walk
  plane up with the floor course running across it, claimed as the region a
  `walk` edge to `exterior` goes `via`;
- a lid over a roofed place (at the plan's `roof/lid-y` where it declares a
  roof, at the frame's top course otherwise), and the declared roof zone above
  it claimed as a region no body walks;
- every seam answered: its handed cells claimed as the region its contract
  edge goes `via`, or — where this place owns the bar — filled with the bar's
  block inside a `barred` edge over exactly those cells;
- every owed name answered by a `mark` of its stem on walkable floor: `spawn`
  with the `entry` role, `unlock-<edge>` beside its bar, the rest along the
  room's middle;
- on a plot, every handed part laid as a region of exactly its declared
  cells, named for the part with `part`: the columns beside every opening,
  ladder, landing and gate, and the middle of every open side, stay the room; a walked part is a space
  (a walk edge joins every two walked spaces that touch); a part seen and
  never entered is an out-of-walk region over the floor that no edge reaches,
  laid only where the walked floor stays one piece — what keeps a body off it
  (a hedge, a crop, a fence) is yours to build. Where each part stands is this starter's
  choice; its count is the plan's;
- a sconce every four cells of wall a course above the floor, and on a roofed
  place a lamp every four cells of the lid, so the light probe has something
  to measure.

Every handed value it uses is declared as a `handed/…` parameter with the
allocation's value as its default, and the body reads it only through that
parameter (`references/detail.md`, *The program's contract*). A number that is
not handed — where a mark stands, how far apart the lamps are — is this
starter's choice and yours to change.

The building is yours. The places to put it are marked `# ── BUILD HERE`, each
naming the idiom of `docs/reference/grammar.md` §2c it reaches for and the step
of `references/new-pieces.md` that says how. Edit a copy under
`<campaign>/design/generator/<stem>.py`, re-run it, and check after every edit:
`delvec --prefabs "$DELVEWRIGHT_PREFABS" detail --check <campaign> <place>`.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys

LAMP_PERIOD = 4  # one sconce (and one ceiling lamp) in four cells; yours to change

# ── BUILD HERE: the palette. Every role below is a name the rules paint; bind
# each to the material the design names (references/new-pieces.md step 2 —
# measure a block's colour, never guess it). A role the whole's palette names
# (`role/<stem>` in detail-plan.json) is rebound to it by `delvec detail`.
PALETTE = {
    "floor": "minecraft:stone_bricks",
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:sea_lantern",
}


# ---- the grammar's expression and operation vocabulary (grammar.md §2) ----


def num(v: int) -> dict:
    return {"expr": "int", "value": v}


def par(name: str) -> dict:
    return {"expr": "param", "name": name}


def arith(lhs: dict, op: str, rhs: dict) -> dict:
    return {"expr": "arith", "lhs": lhs, "op": op, "rhs": rhs}


def fill(role: str) -> dict:
    return {"material": {"role": role}, "op": "fill"}


VOID = {"op": "void"}


def claim(region: str, body: dict) -> dict:
    return {"body": body, "op": "claim", "region": region}


# ---- a value the program reads: a handed parameter, or this starter's literal ----


class Bound:
    """A coordinate on one axis: its value now, and how the program spells it."""

    def __init__(self, value: int, expr: dict, handed: bool) -> None:
        self.value, self.expr, self.handed = value, expr, handed

    def plus(self, n: int) -> "Bound":
        if n == 0:
            return self
        if self.expr.get("expr") == "int":
            return lit(self.value + n)
        return Bound(self.value + n, arith(self.expr, "add" if n > 0 else "sub", num(abs(n))), self.handed)


def lit(v: int) -> Bound:
    return Bound(v, num(v), False)


class Handed:
    """The handed values this program declares — each read only through its parameter."""

    def __init__(self) -> None:
        self.params: dict[str, int] = {}

    def __call__(self, name: str, value: int) -> Bound:
        key = f"handed/{name}"
        self.params[key] = value
        return Bound(value, par(key), True)


# ---- the place, read off the allocation ----


FACES = {"west": (0, -1), "east": (0, 1), "down": (1, -1), "up": (1, 1), "north": (2, -1), "south": (2, 1)}


class Place:
    def __init__(self, a: dict) -> None:
        self.a = a
        self.h = Handed()
        self.n = list(a["extent"])
        self.ex, self.ey, self.ez = self.n
        self.space = a["space"]
        self.datum = self.h("datum-y", a["datum_y"])
        self.aloft = isinstance(a["ground"].get("base"), dict)
        roof = a.get("roof")
        self.roofed = roof is not None or a.get("brief", {}).get("kind") == "roofed"
        if roof is not None:
            self.lid = self.h("roof/lid-y", roof["lid_y"])
        elif self.roofed:
            self.lid = lit(self.ey - 1)
        else:
            self.lid = None
        # The walls stand on the cells just outside the play space, from the
        # walk plane to the lid — or, open to the sky, to the top of the play
        # space. Outside them (the eaves the plan reserves) is air.
        self.wall_top = self.lid if self.lid is not None else lit(self.space[1][1] + 1)
        self.seams = []
        for s in a["seams"]:
            stem = s["edge"].removeprefix("edge/")
            (x0, y0, z0), (x1, y1, z1) = s["cells"]
            lo = [self.h(f"seam/{stem}/{k}", v) for k, v in (("x0", x0), ("y0", y0), ("z0", z0))]
            hi = [self.h(f"seam/{stem}/{k}", v).plus(1) for k, v in (("x1", x1), ("y1", y1), ("z1", z1))]
            axis, sign = FACES[s["face"]]
            bar = None
            if s.get("bar") is not None:
                (bx0, by0, bz0), (bx1, by1, bz1) = s["bar"]
                bar = ([bx0, by0, bz0], [bx1 + 1, by1 + 1, bz1 + 1])
            seam = {"stem": stem, "lo": lo, "hi": hi, "seam": s, "bar": bar, "axis": axis, "approach": None}
            seam["approach"] = self.approach(seam, sign)
            self.seams.append(seam)
        # Every side the place declares open (spec-0123 §5.3): its ring run at
        # the walk plane, corners excluded, piece-local and inclusive.
        self.sides = []
        for s in a.get("sides", []) or []:
            (sx0, _, sz0), (sx1, _, sz1) = s["cells"]
            self.sides.append({"face": s["face"], "lo": (sx0, sz0), "hi": (sx1, sz1)})
        self.scenery = a.get("brief", {}).get("reached") is False
        # A station of kind `gate` is a volume that seals and clears, so it is
        # answered by a region, never a mark: a grille of bars in front of a
        # one-cell alcove against the play space's north wall, joined to the
        # room by a `barred` edge whose bar is that region.
        self.gates: list[dict] = []
        for st in a.get("brief", {}).get("stations", []) or []:
            name, _, kind = st.partition(" (")
            if kind.rstrip(")") != "gate":
                continue
            self.gates.append(self.place_gate(name.removeprefix("anchor/")))
        # A plot's parts (spec-0125 §5.1): the allocation's `parts`, each laid
        # as a region of its declared cells, named for the part.
        self.parts: list[dict] = []
        self.col_part: dict[tuple[int, int], dict] = {}
        self.lay_parts(a.get("parts", []) or [])

    def approach(self, seam: dict, sign: int) -> dict | None:
        """How a body reaches an opening above the walk plane, or None.

        A sideways opening whose sill stands above the floor, or a hole in the
        lid, is reached from a pillar of masonry under it: one course high it is
        a step, higher it carries a landing (its own space) and a ladder up its
        side, joined to the room by a `climb` edge. A hole in the floor needs
        nothing: a body drops through it.
        """
        s, lo, hi, axis = seam["seam"], seam["lo"], seam["hi"], seam["axis"]
        d = self.datum.value
        if axis == 1:
            if sign < 0:
                return None
            sill = lo[1].plus(-1)
            plo, phi = [lo[0], None, lo[2]], [hi[0], None, hi[2]]
            top = lo[1]
            # the ladder stands on the pillar's side toward the room's middle
            cx = (self.space[0][0] + self.space[1][0]) // 2
            lax, ldir = 0, (1 if cx >= lo[0].value else -1)
        else:
            if lo[1].value <= d:
                return None
            sill = lo[1]
            inward = -sign
            plo, phi = list(lo), list(hi)
            if inward > 0:
                plo[axis] = lo[axis].plus(1) if s["owns_plane"] else lo[axis]
                phi[axis] = plo[axis].plus(2)
            else:
                phi[axis] = hi[axis].plus(-1) if s["owns_plane"] else hi[axis]
                plo[axis] = phi[axis].plus(-2)
            top = hi[1]
            lax, ldir = axis, inward
        rise = sill.value - d
        if rise <= 0:
            return None
        out = {"plo": plo, "phi": phi, "sill": sill, "top": top, "rise": rise, "ladder": None}
        if rise > 1:
            other = 2 if lax == 0 else 0
            mid = (plo[other].value + phi[other].value - 1) // 2
            at = (phi[lax].value if ldir > 0 else plo[lax].value - 1)
            facing = {(0, 1): "east", (0, -1): "west", (2, 1): "south", (2, -1): "north"}[(lax, ldir)]
            cell_lo, cell_hi = [0, 0, 0], [0, 0, 0]
            cell_lo[lax], cell_hi[lax] = at, at + 1
            cell_lo[other], cell_hi[other] = mid, mid + 1
            out["ladder"] = {"lo": cell_lo, "hi": cell_hi, "facing": facing}
        return out

    def place_gate(self, stem: str) -> dict:
        lo, hi = self.space
        d = self.datum.value
        z = lo[2]
        for x in range(hi[0] - 1, lo[0], -1):
            cells = [(x2, y, zz) for x2 in (x - 1, x, x + 1) for y in (d, d + 1) for zz in (z, z + 1, z + 2)]
            if all(self.cell(*c) == ("claim", "room", None) for c in cells):
                g = {"stem": stem, "lo": [x, d, z], "hi": [x + 1, d + 2, z + 2], "x": x, "z": z}
                return g
        sys.exit(f"starter.py: no room against the north wall for the gate station `{stem}`; place it by hand")

    def lay_parts(self, parts: list[dict]) -> None:
        """Lay each part as a region of exactly its declared cells.

        The columns beside every opening, ladder, landing and gate, and the
        middle of every open side, stay the `room`, so every edge the room declares keeps its cells; the
        rest of the play space is walked in rows, a part a body walks taking
        the next run of its `cells` columns and a part seen and never entered
        taking columns from the far end, an out-of-walk region over the floor
        no edge reaches, only where the walked floor stays one piece. Where
        the parts stand is this starter's choice and yours to change; the
        counts are the plan's.
        """
        if not parts:
            return
        lo, hi = self.space
        d = self.datum.value
        top = self.lid.value if self.lid is not None else self.wall_top.value
        plain = {("claim", "room", None), ("claim", "roof", None), ("fill", "floor"), ("fill", "wall"), ("fill", "lid"), ("fill", "lamp"), ("void",)}
        special = set()
        for x in range(lo[0] - 1, hi[0] + 2):
            for z in range(lo[2] - 1, hi[2] + 2):
                kinds = {self.cell(x, y, z) for y in range(d - 1, top + 1)} - plain
                # An open side's run is a way out along a whole side: the room
                # keeps the column inside its middle cell, and the parts may
                # stand along the rest of it.
                if kinds and not all(k[0] == "claim" and k[1].startswith("side-") for k in kinds):
                    special.add((x, z))
        room = ("claim", "room", None)
        floor = {
            (x, z)
            for x in range(lo[0], hi[0] + 1)
            for z in range(lo[2], hi[2] + 1)
            if self.cell(x, d, z) == room and self.cell(x, d + 1, z) == room
        }
        # A pillar, a ladder, an alcove: a column of the play space that is
        # not open floor is as special as an opening.
        special |= {(x, z) for x in range(lo[0], hi[0] + 1) for z in range(lo[2], hi[2] + 1)} - floor
        keep = set()
        for sd in self.sides:
            mx, mz = (sd["lo"][0] + sd["hi"][0]) // 2, (sd["lo"][1] + sd["hi"][1]) // 2
            keep.add((min(max(mx, lo[0]), hi[0]), min(max(mz, lo[2]), hi[2])))
        free = []
        for x in range(lo[0], hi[0] + 1):
            zs = range(lo[2], hi[2] + 1) if (x - lo[0]) % 2 == 0 else range(hi[2], lo[2] - 1, -1)
            for z in zs:
                if (x, z) not in floor:
                    continue
                if (x, z) in keep or any(n in special for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1))):
                    keep.add((x, z))
                else:
                    free.append((x, z))
        if not keep and free:
            keep.add(free.pop(len(free) // 2))
        need = sum(p["cells"] for p in parts)
        if need > len(free):
            targets = [max(-(-3 * p["cells"] // 4), p["cells"] * len(free) // need) for p in parts]
        else:
            targets = [p["cells"] for p in parts]
        if sum(targets) > len(free):
            sys.exit(
                f"starter.py: the play space beside the openings holds {len(free)} column(s) and the parts "
                f"need at least {sum(targets)}; lay them by hand"
            )
        walked = (keep & floor) | set(free)
        beside_sides = {
            (min(max(x, lo[0]), hi[0]), min(max(z, lo[2]), hi[2]))
            for sd in self.sides
            for x in range(sd["lo"][0], sd["hi"][0] + 1)
            for z in range(sd["lo"][1], sd["hi"][1] + 1)
        }

        def whole(cells: set) -> bool:
            if not cells:
                return True
            start = next(iter(cells))
            seen, todo = {start}, [start]
            while todo:
                x, z = todo.pop()
                for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                    if n in cells and n not in seen:
                        seen.add(n)
                        todo.append(n)
            return len(seen) == len(cells)

        for p, n in zip(parts, targets):
            stem = p["id"].removeprefix("part/")
            entry = {"part": p, "region": f"part-{stem}", "walked": p.get("reached", True), "cols": []}
            self.parts.append(entry)
            if entry["walked"]:
                continue
            for c in reversed(free):
                if len(entry["cols"]) == n:
                    break
                if c in beside_sides:
                    continue
                if whole(walked - {c}):
                    walked.discard(c)
                    entry["cols"].append(c)
            if len(entry["cols"]) < n:
                sys.exit(f"starter.py: no room for the seen part `{p['id']}` that leaves the walked floor one piece; lay it by hand")
            free = [c for c in free if c not in set(entry["cols"])]
        for e, n in zip(self.parts, targets):
            if e["walked"]:
                e["cols"], free = free[:n], free[n:]
        for e in self.parts:
            for c in e["cols"]:
                self.col_part[c] = e

    def in_space_xz(self, x: int, z: int) -> bool:
        lo, hi = self.space
        return lo[0] <= x <= hi[0] and lo[2] <= z <= hi[2]

    def open_side(self, x: int, z: int) -> str | None:
        """The face of the open side whose ring run holds column `(x, z)`."""
        for s in self.sides:
            if s["lo"][0] <= x <= s["hi"][0] and s["lo"][1] <= z <= s["hi"][1]:
                return s["face"]
        return None

    def wall_ring(self, x: int, z: int) -> bool:
        lo, hi = self.space
        return (lo[0] - 1 <= x <= hi[0] + 1 and lo[2] - 1 <= z <= hi[2] + 1) and not self.in_space_xz(x, z)

    # -- what one cell is, by the rules above --
    def cell(self, x: int, y: int, z: int) -> tuple:
        kind = self.base_cell(x, y, z)
        if kind[0] == "claim" and kind[1].startswith("side-") and getattr(self, "col_part", None):
            # An open side's cell is the way out of the space inside it.
            space = self.side_space(x, z)
            return kind if space == "room" else ("claim", f"{kind[1]}-{space}", None)
        part = getattr(self, "col_part", {}).get((x, z))
        if part is None or kind != ("claim", "room", None):
            return kind
        return ("claim", part["region"], None)

    def side_space(self, x: int, z: int) -> str:
        """The walked space whose column stands inside an open side's cell."""
        lo, hi = self.space
        inner = (min(max(x, lo[0]), hi[0]), min(max(z, lo[2]), hi[2]))
        e = self.col_part.get(inner)
        return e["region"] if e is not None and e["walked"] else "room"

    def walkable(self, kind: tuple) -> bool:
        """A cell of a space a body walks: the room, or a walked part."""
        return kind == ("claim", "room", None) or any(kind == ("claim", e["region"], None) for e in self.parts if e["walked"])

    def base_cell(self, x: int, y: int, z: int) -> tuple:
        c = (x, y, z)
        for s in self.seams:
            if s["bar"] is not None and all(s["bar"][0][i] <= c[i] < s["bar"][1][i] for i in range(3)):
                return ("claim", f"seam-{s['stem']}", f"bar-{s['stem']}")
        for s in self.seams:
            if all(s["lo"][i].value <= c[i] < s["hi"][i].value for i in range(3)):
                return ("claim", f"{s['stem']}-way", None)
        d = self.datum.value
        for g in getattr(self, "gates", []):
            # the alcove and its grille, two courses high, walled at both
            # sides and capped with wall to the lid, so the bar is the only way
            # between the alcove and the room
            if d <= y < self.wall_top.value and ((x == g["x"] and z in (g["z"], g["z"] + 1)) or (abs(x - g["x"]) == 1 and z == g["z"])):
                if x != g["x"] or y >= d + 2:
                    return ("fill", "wall")
                if z == g["z"]:
                    return ("claim", f"{g['stem']}-alcove", None)
                return ("claim", g["stem"], f"bar-{g['stem']}")
        for s in self.seams:
            ap = s["approach"]
            if ap is None:
                continue
            lad = ap["ladder"]
            if lad is not None and lad["lo"][0] <= x < lad["hi"][0] and lad["lo"][2] <= z < lad["hi"][2] and d <= y <= ap["sill"].value:
                # the ladder up to the sill, and the cell beside the landing
                # open, so the climb abuts both the room and the landing
                return ("claim", f"{s['stem']}-ladder", f"ladder-{lad['facing']}" if y < ap["sill"].value else None)
            xz = all(ap["plo"][i].value <= c[i] < ap["phi"][i].value for i in (0, 2))
            if xz and d <= y < ap["sill"].value:
                return ("fill", "floor")
            if xz and lad is not None and ap["sill"].value <= y < ap["top"].value:
                return ("claim", f"{s['stem']}-landing", None)
        d = self.datum.value
        if y < d:
            if self.aloft and y < d - 1:
                return ("void",)
            return ("fill", "floor")
        if self.lid is not None and y == self.lid.value:
            if self.in_space_xz(x, z) and (x % LAMP_PERIOD, z % LAMP_PERIOD) == (2, 2):
                return ("fill", "lamp")
            return ("fill", "lid")
        if self.lid is not None and y > self.lid.value:
            return ("claim", "roof", None)
        side = self.open_side(x, z)
        if side is not None and d <= y < self.wall_top.value:
            # An open side stands no wall: its ring cells are open from the
            # walk plane up, and the floor course below runs across them.
            return ("claim", f"side-{side}", None)
        if self.wall_ring(x, z) and y < self.wall_top.value:
            lo, hi = self.space
            along, a0, a1 = (z, lo[2], hi[2]) if x in (lo[0] - 1, hi[0] + 1) else (x, lo[0], hi[0])
            if y == d + 1 and along % LAMP_PERIOD == 2 and a0 <= along <= a1:
                return ("fill", "lamp")
            return ("fill", "wall")
        if self.in_space_xz(x, z) and y < self.wall_top.value:
            return ("claim", "room", None)
        return ("void",)

    def cuts(self, axis: int) -> list[Bound]:
        """Every coordinate on `axis` where what a cell is can change."""
        n = self.n[axis]
        lo, hi = self.space
        out = [lit(0), lit(n)]
        for s in self.seams:
            out += [s["lo"][axis], s["hi"][axis]]
            if s["bar"] is not None:
                out += [lit(s["bar"][0][axis]), lit(s["bar"][1][axis])]
            ap = s["approach"]
            if ap is not None:
                if axis == 1:
                    out += [ap["sill"], ap["top"]]
                else:
                    out += [ap["plo"][axis], ap["phi"][axis]]
                if ap["ladder"] is not None and axis != 1:
                    out += [lit(ap["ladder"]["lo"][axis]), lit(ap["ladder"]["hi"][axis])]
                if ap["ladder"] is not None and axis == 1:
                    out += [ap["sill"].plus(1)]
        for s in self.sides:
            if axis != 1:
                i = 0 if axis == 0 else 1
                out += [lit(s["lo"][i]), lit(s["hi"][i] + 1)]
        for g in self.gates:
            out += [lit(g["lo"][axis]), lit(g["hi"][axis])]
            if axis == 0:
                out += [lit(g["x"] - 1), lit(g["x"] + 2)]
        if axis == 1:
            out += [self.datum.plus(-1), self.datum, self.datum.plus(1), self.datum.plus(2), self.wall_top]
            if self.lid is not None:
                out += [self.lid, self.lid.plus(1)]
        else:
            out += [lit(lo[axis] - 1), lit(lo[axis]), lit(hi[axis] + 1), lit(hi[axis] + 2)]
            if self.parts:
                out += [lit(v) for v in range(lo[axis], hi[axis] + 2)]
            out += [lit(v) for v in range(0, n, LAMP_PERIOD)] + [lit(v) for v in range(2, n, LAMP_PERIOD)] + [lit(v + 1) for v in range(2, n, LAMP_PERIOD)]
        best: dict[int, Bound] = {}
        for b in out:
            if 0 <= b.value <= n and (b.value not in best or (b.handed and not best[b.value].handed)):
                best[b.value] = b
        best[0] = lit(0)
        return [best[v] for v in sorted(best) if v < n]


def size_of(lo: Bound, hi: Bound | None) -> dict:
    if hi is None:
        return {"size": "relative", "weight": num(1)}
    if lo.expr.get("expr") == "int" and hi.expr.get("expr") == "int":
        return {"blocks": num(hi.value - lo.value), "size": "absolute"}
    if lo.value == 0 and lo.expr.get("expr") == "int":
        return {"blocks": hi.expr, "size": "absolute"}
    return {"blocks": arith(hi.expr, "sub", lo.expr), "size": "absolute"}


class Rules:
    """Rules, each body stated once and called by name wherever it recurs."""

    def __init__(self) -> None:
        self.rules: dict[str, list] = {}
        self.names: dict[str, str] = {}

    def name(self, body: dict, hint: str) -> dict:
        key = json.dumps(body, sort_keys=True)
        if key not in self.names:
            name = f"{hint}_{len(self.names)}"
            self.names[key] = name
            self.rules[name] = [{"body": body, "weight": 1}]
        return {"op": "call", "symbol": self.names[key]}


def leaf(kind: tuple) -> dict:
    if kind[0] == "fill":
        return fill(kind[1])
    if kind[0] == "void":
        return VOID
    _, region, role = kind
    return claim(region, fill(role) if role else VOID)


def split(axis: str, cuts: list[Bound], children: list[dict]) -> dict:
    if len(children) == 1:
        return children[0]
    sizes = [size_of(cuts[i], cuts[i + 1] if i + 1 < len(cuts) else None) for i in range(len(cuts))]
    return {"axis": axis, "children": children, "op": "split", "sizes": sizes}


def body(p: Place, rules: Rules) -> dict:
    """The place, cut into boxes on x, then y, then z, each box one kind of cell."""
    xs, ys, zs = p.cuts(0), p.cuts(1), p.cuts(2)
    columns = []
    for x in xs:
        courses = []
        for y in ys:
            row = [leaf(p.cell(x.value, y.value, z.value)) for z in zs]
            courses.append(rules.name(split("z", zs, row), "row"))
        columns.append(rules.name(split("y", ys, courses), "column"))
    return split("x", xs, columns)


def marks(p: Place, inner: dict) -> dict:
    """Every owed name, answered by a `mark` of its stem on walkable floor."""
    lo, hi = p.a["space"]
    cx, cz = (lo[0] + hi[0]) // 2, (lo[2] + hi[2]) // 2
    taken: set[tuple[int, int]] = set()

    def free(x: int, z: int) -> tuple[int, int]:
        for dz in range(0, max(p.ex, p.ez)):
            for x2, z2 in ((x, z + dz), (x, z - dz), (x + dz, z), (x - dz, z)):
                if lo[0] <= x2 <= hi[0] and lo[2] <= z2 <= hi[2] and (x2, z2) not in taken:
                    if p.walkable(p.cell(x2, p.datum.value, z2)) and p.walkable(p.cell(x2, p.datum.value + 1, z2)) and p.cell(x2, p.datum.value - 1, z2) == ("fill", "floor"):
                        taken.add((x2, z2))
                        return x2, z2
        sys.exit("starter.py: no free floor cell for a mark; the play space is full")

    out = inner
    for name in reversed(p.a["owed_anchors"]):
        stem = name.removeprefix("anchor/")
        if stem.startswith("seam-") or any(g["stem"] == stem for g in p.gates):
            continue  # answered by a barred edge's region, never a mark
        mark = {"anchor": stem, "at": "offset", "facing": "south", "y": p.datum.expr}
        if stem == "spawn":
            mark["role"] = "entry"
        target = (cx, cz)
        if stem.startswith("unlock-"):
            s = next((s for s in p.seams if f"unlock-{s['stem']}" == stem), None)
            if s is not None:
                (x0, _, z0), (x1, _, z1) = s["seam"]["cells"]
                target = (min(max((x0 + x1) // 2, lo[0]), hi[0]), min(max((z0 + z1) // 2, lo[2]), hi[2]))
        x, z = free(*target)
        mark["x"], mark["z"] = num(x), num(z)
        out = {"body": out, "mark": mark, "op": "mark"}
    return out


def contract(p: Place) -> dict:
    """The spatial contract: the room, a landing under each raised opening, an
    edge per seam, the roof zone no body walks."""
    spaces = {"room": {"envelope": "enclosed" if p.lid is not None else "open"}}
    edges = []
    for s in p.seams:
        seam = s["seam"]
        space = p.seam_space(s)
        ap = s["approach"]
        if ap is not None and ap["ladder"] is not None:
            space = f"{s['stem']}-landing"
            spaces[space] = {"envelope": "open"}
            edges.append({"a": "room", "b": space, "class": "climb", "rise": ap["rise"], "via": f"{s['stem']}-ladder"})
        if s["bar"] is not None:
            edge = {"a": space, "b": "exterior", "bar": {"block": f"bar-{s['stem']}", "region": f"seam-{s['stem']}"}, "class": "barred"}
            if s["bar"] != ([v.value for v in s["lo"]], [v.value for v in s["hi"]]):
                edge["via"] = f"{s['stem']}-way"  # the opening the bar closes
            edges.append(edge)
            continue
        answers = [c for c in seam["answer_with"] if c != "barred"]
        cls = "walk" if "walk" in answers else answers[0]
        edge = {"a": space, "b": "exterior", "class": cls, "via": f"{s['stem']}-way"}
        if cls in ("stair", "drop", "climb"):
            edge["rise"] = 0  # the level beyond is the neighbour's to measure
        edges.append(edge)
    for s in p.sides:
        # A frontage a body crosses: the open side's cells are the way out
        # (spec-0123 §5.4). A counter a body does not cross stands at the play
        # space's edge, inside, and the side stays this edge's. On a plot the
        # run is one way out per walked space standing inside it.
        spaces_in = []
        for x in range(s["lo"][0], s["hi"][0] + 1):
            for z in range(s["lo"][1], s["hi"][1] + 1):
                sp = p.side_space(x, z) if p.col_part else "room"
                if sp not in spaces_in:
                    spaces_in.append(sp)
        for sp in sorted(spaces_in):
            via = f"side-{s['face']}" if sp == "room" else f"side-{s['face']}-{sp}"
            edges.append({"a": sp, "b": "exterior", "class": "walk", "via": via})
    no_body = {}
    pairs = set()
    for e in p.parts:
        if not e["walked"]:
            no_body[e["region"]] = {"part": e["part"]["id"], "reason": f"{e['part']['use']}: seen, never entered"}
            continue
        spaces[e["region"]] = {"envelope": spaces["room"]["envelope"], "part": e["part"]["id"]}
    # A walk edge between every two walked spaces whose columns touch.
    for (x, z), e in p.col_part.items():
        if not e["walked"]:
            continue
        for n in ((x + 1, z), (x, z + 1), (x - 1, z), (x, z - 1)):
            if not p.in_space_xz(*n):
                continue
            o = p.col_part.get(n)
            other = "room" if o is None else (o["region"] if o["walked"] else None)
            if other is not None and other != e["region"]:
                pairs.add(tuple(sorted((e["region"], other))))
    for a_, b_ in sorted(pairs):
        edges.append({"a": a_, "b": b_, "class": "walk"})
    for g in p.gates:
        spaces[f"{g['stem']}-alcove"] = {"envelope": "open"}
        edges.append({"a": "room", "b": f"{g['stem']}-alcove", "bar": {"block": f"bar-{g['stem']}", "region": g["stem"]}, "class": "barred"})
    out = {
        "edges": edges,
        "entry": "room",
        # ── BUILD HERE: the spaces. A room a body walks around inside walls and
        # under a lid is `enclosed`; a street, a deck or a court open to the sky
        # is `open`. A second floor is a second space and a `climb` or `stair`
        # edge between them — a landing below is reached that way
        # (grammar.md §2d; references/detail.md, the program's contract).
        "spaces": spaces,
    }
    if p.lid is not None and p.lid.value + 1 < p.ey:
        no_body["roof"] = {"reason": "the roof zone over the lid, which no one is meant to walk"}
        out["no_body_majority_ack"] = "the roof zone the plan reserves over the lid is left for the roof the author builds; nobody walks it"
    if no_body:
        out["no_body"] = no_body
    return out


# A handed block named with no state, written out as the gates require
# (`DW0735`, `DW0737`): every property, the block's own default where the
# design says nothing.
BARE_STATES = {
    "minecraft:iron_bars": "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]",
}


def full_state(block: str) -> str:
    return BARE_STATES.get(block, block)


def program(a: dict) -> dict:
    p = Lighthouse(a)
    rules = Rules()
    # ── BUILD HERE: the building. The body below is the empty place — floor,
    # ring wall, lid, openings, sconces. Replace the `room` boxes with the
    # rooms the design draws, starting from the idioms (grammar.md §2c: 1
    # repetition for a colonnade or a run of bays, 3 shape for an arch or a
    # gable, 7 symmetry for a front, 9 light for where the lamps stand) and the
    # procedure (references/new-pieces.md step 3, the program; step 4, the
    # gates). Keep every seam's region and every mark; they are what binds.
    start = marks(p, body(p, rules))
    rules.rules["place"] = [{"body": start, "weight": 1}]
    palette = dict(PALETTE)
    for s in p.seams:
        if s["bar"] is not None:
            palette[f"bar-{s['stem']}"] = full_state(s["seam"]["bar_block"])
        ap = s["approach"]
        if ap is not None and ap["ladder"] is not None:
            f = ap["ladder"]["facing"]
            palette[f"ladder-{f}"] = f"minecraft:ladder[facing={f},waterlogged=false]"
    for g in p.gates:
        palette[f"bar-{g['stem']}"] = full_state("minecraft:iron_bars")
    climbs = any(e.get("class") == "climb" for e in contract(p)["edges"])
    return {
        "contract": contract(p),
        "name": f"{a['place'].removeprefix('node/')}-starter",
        "palette": palette,
        "params": dict(sorted(p.h.params.items())),
        "rules": rules.rules,
        # ── BUILD HERE: the faces the piece shows the world (grammar.md §2f).
        # Derived from what this skeleton draws: a declared side must hold a
        # block (`DW0885`), and a side over open air must be declared.
        "shown_faces": shown_faces(p),
        "start": "place",
        "version": "1.14.0" if p.parts else ("1.10.0" if climbs else "1.9.0"),
    }


def shown_faces(p) -> list[str]:
    """The sides this skeleton finishes: the four walls; the top course where
    the lid stands at it, or the walls reach it under an open sky (a lid under a
    declared roof zone leaves the top course to the roof the author builds, so
    `up` is the author's to add with the roof); and the underside of an aloft
    place, which stands over air the party can be in."""
    faces = ["east", "north", "south", "west"]
    if (p.lid is not None and p.lid.value == p.ey - 1) or (p.lid is None and p.wall_top.value >= p.ey):
        faces.append("up")
    if p.aloft:
        faces.append("down")
    return sorted(faces)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--allocation", required=True, help="`delvec allocation <campaign> <place>`, saved")
    ap.add_argument("--out", required=True, help="where the program is written")
    args = ap.parse_args(argv)
    with open(args.allocation, encoding="utf-8") as f:
        allocation = json.load(f)
    text = json.dumps(program(allocation), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text)
    return 0


# ===================================================================== the lighthouse
#
# Everything above is the starter, which binds the handing (datum, the lane's
# seam, the four open sides, the owed name, the three parts). Everything below
# is the place: a voxel model of the lighthouse, the keeper's cottage and the
# walled yard, which the place's cell() reads.
#
# After the community's lighthouse builds (madexc's big-lighthouse and
# lighthouse, CC BY 4.0; l4ziness's Quay and Lighthouse, no licence stated;
# all ideas only): an octagonal white tower on a dark stone base, narrowing
# once below the top; a corbelled gallery with a railing round a glazed
# lantern room; a dark cap stepping to a finial. Inside, a stair turns round a
# solid newel in four flights a revolution, with landings at the corners, up
# to the lantern room's floor and its great lamp. The keeper's cottage stands
# against the tower's north face and opens into it by a door; the yard lies
# west and south of the tower inside a low wall, a gate on the cliff path.
#
# Axes are piece-local: +x east, +z south; y 0 is the ground course, y 1 the
# walk plane. The lane is west.

AIR = "~air"

PALETTE = {
    "floor": "minecraft:stone_bricks",
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    # the ground
    "turf": "minecraft:grass_block[snowy=false]",
    "path": "minecraft:gravel",
    "flags": [{"weight": 5, "block": "minecraft:stone_bricks"},
              {"weight": 2, "block": "minecraft:andesite"},
              {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    # the tower
    "base": [{"weight": 6, "block": "minecraft:stone_bricks"},
             {"weight": 2, "block": "minecraft:cobblestone"},
             {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "white": "minecraft:white_concrete",
    "band": "minecraft:red_terracotta",
    "corbel": "minecraft:polished_andesite",
    "dark": "minecraft:polished_deepslate",
    "newel": "minecraft:stone_bricks",
    "step_e": "minecraft:stone_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "step_s": "minecraft:stone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
    "step_w": "minecraft:stone_brick_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
    "step_n": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "landing": "minecraft:polished_andesite",
    "slit": "minecraft:light_gray_stained_glass",
    "lamp_glass": "minecraft:glass",
    "mullion": "minecraft:polished_deepslate",
    "lamp_floor": "minecraft:polished_andesite",
    "great_lamp": "minecraft:sea_lantern",
    "newel_lamp": "minecraft:sea_lantern",
    "plinth_ring": "minecraft:polished_andesite",
    "cone_n": "minecraft:deepslate_tile_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "cone_s": "minecraft:deepslate_tile_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
    "cone_e": "minecraft:deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "cone_w": "minecraft:deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
    "rail": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "gallery": "minecraft:polished_andesite_slab[type=top,waterlogged=false]",
    "cap": "minecraft:deepslate_tiles",
    "finial": "minecraft:lightning_rod[facing=up,powered=false,waterlogged=false]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    # the cottage
    "stone": [{"weight": 8, "block": "minecraft:stone_bricks"},
              {"weight": 3, "block": "minecraft:cobblestone"},
              {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "plaster": "minecraft:white_terracotta",
    "post": "minecraft:dark_oak_log[axis=y]",
    "beam_x": "minecraft:dark_oak_log[axis=x]",
    "beam_z": "minecraft:dark_oak_log[axis=z]",
    "boards": "minecraft:spruce_planks",
    "floorb": "minecraft:spruce_planks",
    "glass": "minecraft:light_gray_stained_glass",
    "roof": "minecraft:deepslate_tiles",
    "roof_n": "minecraft:deepslate_tile_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "roof_s": "minecraft:deepslate_tile_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "chimney": "minecraft:bricks",
    "hearth": "minecraft:furnace[facing=south,lit=false]",
    "table": "minecraft:spruce_slab[type=top,waterlogged=false]",
    "chair": "minecraft:spruce_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "shelf": "minecraft:bookshelf",
    "candles": "minecraft:white_candle[candles=2,lit=true,waterlogged=false]",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "pot_a": "minecraft:potted_red_tulip",
    "pot_b": "minecraft:potted_cornflower",
    "pot_c": "minecraft:potted_oxeye_daisy",
    # the yard
    "ywall": [{"weight": 4, "block": "minecraft:cobblestone"},
              {"weight": 2, "block": "minecraft:mossy_cobblestone"},
              {"weight": 1, "block": "minecraft:stone_bricks"}],
    "ycap": "minecraft:stone_brick_slab[type=bottom,waterlogged=false]",
    "bench": "minecraft:spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "trough": "minecraft:cauldron",
    "woodpile": "minecraft:spruce_log[axis=x]",
    "lamp_post": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "bush": "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]",
    "rose": "minecraft:rose_bush[half=lower]",
    "rose_top": "minecraft:rose_bush[half=upper]",
    "tuft": "minecraft:short_grass",
    "daisy": "minecraft:oxeye_daisy",
}

class Model:
    def __init__(self):
        self.v = {}
        self.region = {}

    def set(self, x, y, z, role):
        self.v[(x, y, z)] = role

    def box(self, x0, x1, y0, y1, z0, z1, role):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.v[(x, y, z)] = role

    def get(self, x, y, z):
        return self.v.get((x, y, z))


CX = CZ = 13.5               # the tower's axis, between four cells
R_BASE, R_TOP = 5.25, 4.1    # the shaft's outer radius at its foot and at its head: it tapers
R_IN = 2.25                  # the shaft's inside: the newel and the stair's lane round it
R_PART = 4.25                # the tower's claimed columns: its inside and the wall's inner half
LAMP_FLOOR = 26              # the lantern room's floor course, the gallery's walk
LAMP_TOP = 30                # the last glazed course
R_LAMP = 3.4                 # the lantern room's polygon
R_GALLERY = 5.6              # the gallery's outer edge
COTTAGE = (2, 14, 2, 8)      # walls inclusive (x0, x1, z0, z1)
C_TOP = 5                    # the cottage's wall head
# the stair's lane: the ring of twelve cells round the 2x2 newel, clockwise from the north-west
RING = [(12, 12), (13, 12), (14, 12), (15, 12), (15, 13), (15, 14), (15, 15), (14, 15), (13, 15),
        (12, 15), (12, 14), (12, 13)]
RING0 = 3                    # the ring cell the first step stands on
NEWEL = [(13, 13), (14, 13), (13, 14), (14, 14)]
FACING = {(1, 0): "e", (-1, 0): "w", (0, 1): "s", (0, -1): "n"}


def dist(x, z):
    return ((x - CX) ** 2 + (z - CZ) ** 2) ** 0.5


def r_at(y):
    """The shaft's outer radius at course y."""
    if y <= 3:
        return R_BASE
    t = min(1.0, (y - 3) / (LAMP_FLOOR - 4))
    return R_BASE + (R_TOP - R_BASE) * t


def tower_wall(x, z, y=1):
    return R_IN < dist(x, z) <= r_at(y)


def tower_inside(x, z):
    return dist(x, z) <= R_IN


def stair_path():
    """The stair's steps, bottom to top: (x, z, y, role). One step a ring cell, a
    course a step, twelve courses a revolution, up to the lantern room's floor."""
    out = []
    for k in range(LAMP_FLOOR):
        i = (RING0 + k) % 12
        x, z = RING[i]
        nx, nz = RING[(i + 1) % 12]
        d = FACING[(nx - x, nz - z)] if (nx - x, nz - z) in FACING else "e"
        out.append((x, z, k + 1, "step_" + d))
    return out


def polygon_ring(m, y, r, role, fill_role=None):
    """An octagon of radius r at course y: its rim cells `role`, its inside `fill_role`."""
    for x in range(int(CX - r) - 1, int(CX + r) + 2):
        for z in range(int(CZ - r) - 1, int(CZ + r) + 2):
            dx, dz = abs(x - CX), abs(z - CZ)
            inside = max(dx, dz) <= r and dx + dz <= r * 1.42
            if not inside:
                continue
            rim = not (max(dx + 1, dz) <= r and dx + 1 + dz <= r * 1.42
                       and max(dx, dz + 1) <= r and dx + dz + 1 <= r * 1.42)
            if rim:
                m.set(x, y, z, role)
            elif fill_role:
                m.set(x, y, z, fill_role)


def build_tower(m):
    # ---------- the shaft: round, tapering, a stone foot, white with two red bands
    for x in range(1, 21):
        for z in range(1, 21):
            d = dist(x, z)
            if d <= R_IN:
                m.set(x, 0, z, "flags")
            for y in range(1, LAMP_FLOOR):
                if R_IN < d <= r_at(y):
                    role = "base" if y <= 3 else "white"
                    if y in (11, 12, 19, 20):
                        role = "band"
                    m.set(x, y, z, role)
                    m.set(x, 0, z, "base")
    # a plinth course round the foot
    for x in range(1, 21):
        for z in range(1, 21):
            if R_BASE < dist(x, z) <= R_BASE + 0.8 and m.get(x, 1, z) is None:
                m.set(x, 1, z, "plinth_ring")
    # the newel, solid to the lantern room's floor, a lamp let into it every four courses
    for (x, z) in NEWEL:
        m.box(x, x, 1, LAMP_FLOOR - 1, z, z, "newel")
    for j, y in enumerate(range(3, LAMP_FLOOR, 4)):
        x, z = NEWEL[j % 4]
        m.set(x, y, z, "newel_lamp")
    # the stair
    path = stair_path()
    for (x, z, y, role) in path:
        m.set(x, y, z, role)
    # slits up the stair: a window in the wall beside every third step
    for (x, z, y, role) in path[2::3]:
        ox, oz = x - CX, z - CZ
        wx = x + (1 if ox > 0 else -1) * (abs(ox) >= abs(oz))
        wz = z + (1 if oz > 0 else -1) * (abs(oz) > abs(ox))
        if tower_wall(wx, wz, y + 2) and 4 < y + 2 < LAMP_FLOOR - 1:
            m.set(wx, y + 2, wz, "slit")
            m.set(wx, y + 3, wz, "slit")
    # the door onto the yard (west) and the passage from the cottage (north)
    for x in range(8, 12):
        for z in (13, 14):
            if tower_wall(x, z) or x == 11:
                m.box(x, x, 1, 3, z, z, AIR)
                m.set(x, 0, z, "flags")
    for z in range(9, 12):
        for x in (13, 14):
            m.box(x, x, 1, 3, z, z, AIR)
            m.set(x, 0, z, "flags")
    # the lantern room's floor, the stairwell left open over the last steps
    well = {(x, z) for (x, z, y, r) in path if LAMP_FLOOR - 3 <= y < LAMP_FLOOR}
    for x in range(1, 21):
        for z in range(1, 21):
            if dist(x, z) <= R_LAMP + 0.6 and (x, z) not in well and not str(m.get(x, LAMP_FLOOR, z)).startswith("step"):
                m.set(x, LAMP_FLOOR, z, "lamp_floor")
    # the gallery: slabs on a corbel course round the lantern room, railed
    for x in range(1, 21):
        for z in range(1, 21):
            d = dist(x, z)
            if R_LAMP + 0.6 < d <= R_GALLERY:
                m.set(x, LAMP_FLOOR, z, "gallery")
                if d > r_at(LAMP_FLOOR - 1):
                    m.set(x, LAMP_FLOOR - 1, z, "corbel")
                if d > R_GALLERY - 1:
                    m.set(x, LAMP_FLOOR + 1, z, "rail")
    # the lantern room: an octagon of glass between dark mullions
    for y in range(LAMP_FLOOR + 1, LAMP_TOP + 1):
        polygon_ring(m, y, R_LAMP, "lamp_glass")
    for x in range(1, 21):
        for z in range(1, 21):
            if m.get(x, LAMP_FLOOR + 1, z) == "lamp_glass":
                dx, dz = abs(x - CX), abs(z - CZ)
                if abs(dx - dz) < 1.1 or min(dx, dz) < 0.6:
                    for y in range(LAMP_FLOOR + 1, LAMP_TOP + 1):
                        m.set(x, y, z, "mullion")
    # a door onto the gallery, on the west
    for z in (13, 14):
        for x in range(9, 12):
            if m.get(x, LAMP_FLOOR + 1, z) in ("lamp_glass", "mullion"):
                m.box(x, x, LAMP_FLOOR + 1, LAMP_FLOOR + 2, z, z, AIR)
    # the great lamp on the newel's head
    for (x, z) in NEWEL:
        m.box(x, x, LAMP_FLOOR + 1, LAMP_FLOOR + 2, z, z, "great_lamp")
    # the cap: a dark cornice, then a cone of tile stairs stepping in to a finial
    polygon_ring(m, LAMP_TOP + 1, R_LAMP + 0.7, "dark", "cap")
    for k, r in enumerate((R_LAMP - 0.4, R_LAMP - 1.4, R_LAMP - 2.4)):
        y = LAMP_TOP + 2 + k
        polygon_ring(m, y, r, "cone", "cap")
    for x in range(1, 21):
        for z in range(1, 21):
            for y in range(LAMP_TOP + 2, LAMP_TOP + 5):
                if m.get(x, y, z) == "cone":
                    ox, oz = x - CX, z - CZ
                    d = ("w" if ox > 0 else "e") if abs(ox) >= abs(oz) else ("n" if oz > 0 else "s")
                    m.set(x, y, z, "cone_" + d)
    m.set(13, LAMP_TOP + 4, 13, "finial")
    return path


def build_model():
    m = Model()
    for x in range(1, 21):
        for z in range(1, 21):
            m.set(x, 0, z, "turf")

    path = build_tower(m)

    # ---------- the keeper's cottage, against the tower's north face
    x0, x1, z0, z1 = COTTAGE
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            m.set(x, 0, z, "stone" if edge else "floorb")
            if not edge:
                continue
            corner = x in (x0, x1) and z in (z0, z1)
            m.box(x, x, 1, 2, z, z, "stone")
            post = corner or ((x - x0) % 3 == 0 if z in (z0, z1) else (z - z0) % 3 == 0)
            for y in range(3, C_TOP + 1):
                m.set(x, y, z, "post" if post else "plaster")
            m.set(x, C_TOP, z, "beam_x" if z in (z0, z1) else "beam_z")
    m.box(x0 + 1, x1 - 1, C_TOP, C_TOP, z0 + 1, z1 - 1, "boards")
    lo, hi, k = z0, z1, 0
    while lo <= hi:
        y = C_TOP + 1 + k
        if lo == hi:
            m.box(x0, x1, y, y, lo, lo, "ridge")
        else:
            m.box(x0, x1, y, y, lo, lo, "roof_s")
            m.box(x0, x1, y, y, hi, hi, "roof_n")
            for x in (x0, x1):
                m.box(x, x, y, y, lo + 1, hi - 1, "boards" if k else "beam_z")
            for x in range(x0 + 1, x1):
                m.box(x, x, y, y, lo + 1, hi - 1, "roof")
        lo, hi, k = lo + 1, hi - 1, k + 1
    # the door through to the tower (south wall, into the tower's north-west landing)
    m.box(13, 14, 1, 3, z1, z1, AIR)
    for x in (13, 14):
        m.set(x, 0, z1, "floorb")
    # the front door onto the lane's side of the yard (west wall)
    m.box(x0, x0, 1, 3, 5, 6, AIR)
    m.set(x0, 0, 5, "floorb")
    m.set(x0, 0, 6, "floorb")
    # windows
    for (x, z) in ((5, z0), (8, z0), (11, z0), (5, z1)):
        m.set(x, 3, z, "glass")
        m.set(x, 4, z, "glass")
    m.set(x0, 3, 3, "glass")
    m.set(x1, 3, 5, "glass")
    m.set(x1, 4, 5, "glass")
    # the chimney and the hearth on the east gable
    m.box(x1 - 1, x1 - 1, 1, C_TOP + 6, z0 + 3, z0 + 3, "chimney")
    m.set(x1 - 2, 1, z0 + 3, "hearth")
    # inside: a table and chairs, shelves, the keeper's log on the table, a lamp
    m.set(6, 1, 4, "table")
    m.set(7, 1, 4, "table")
    m.set(5, 1, 4, "chair")
    m.set(6, 2, 4, "candles")
    m.box(3, 3, 1, 2, 7, 7, "shelf")
    m.set(4, 1, 7, "barrel")
    m.set(8, C_TOP - 1, 5, "lantern_h")
    m.set(12, 1, 3, "pot_a")

    # ---------- the yard: a low wall west and south, a gate on the cliff path
    for z in range(15, 20):
        m.set(2, 1, z, "ywall")
        m.set(2, 2, z, "ycap")
    for x in range(2, 10):
        m.set(x, 1, 19, "ywall")
        m.set(x, 2, 19, "ycap")
    for x in (4, 5):                                    # the gate onto the cliff path
        m.set(x, 1, 19, AIR)
        m.set(x, 2, 19, AIR)
    # the path: the lane to the cottage door and the tower door, and out to the cliff
    for x in range(1, 10):
        m.set(x, 0, 13, "path")
        m.set(x, 0, 14, "path")
    for z in range(9, 14):
        m.set(1, 0, z, "path")
    for z in range(5, 9):
        m.set(1, 0, z, "path")
    for z in range(14, 21):
        m.set(4, 0, z, "path")
        m.set(5, 0, z, "path")
    # life in the yard: a bench, a trough, a woodpile, barrels, flowers, lamps
    m.set(6, 1, 11, "bench")
    m.set(7, 1, 11, "bench")
    m.set(7, 1, 17, "trough")
    m.box(3, 3, 1, 1, 16, 18, "woodpile")
    m.set(3, 2, 17, "woodpile")
    m.set(8, 1, 16, "barrel")
    m.set(8, 1, 15, "barrel")
    for (x, z, r) in ((3, 11, "pot_b"), (3, 12, "pot_c"), (6, 18, "rose"), (7, 18, "rose")):
        m.set(x, 1, z, r)
        if r == "rose":
            m.set(x, 2, z, "rose_top")
    for (x, z) in ((3, 15), (6, 15), (6, 16), (7, 12), (16, 3), (18, 6)):
        if m.get(x, 1, z) is None:
            m.set(x, 1, z, "tuft" if (x + z) % 2 else "daisy")
    for (x, z) in ((16, 8), (3, 9), (19, 5)):
        m.set(x, 1, z, "lamp_post")
        m.set(x, 2, z, "lantern")
    # the east garden behind the cottage: a hedge of bushes, a bench
    for x in range(16, 20):
        m.set(x, 1, 2, "bush")
    m.set(17, 1, 4, "bench")

    # ---------- the parts: which columns are which
    for x in range(1, 21):
        for z in range(1, 21):
            if dist(x, z) <= R_PART:
                m.region[(x, z)] = "tower"
            elif x0 < x < x1 and z0 < z < z1:
                m.region[(x, z)] = "cottage"
            elif (x <= 8 and z >= 9) or (x == 1 and z >= COTTAGE[3] - 1) or (x >= 15 and z <= 7):
                m.region[(x, z)] = "yard"
    return m


DIRS = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
CCW = {"north": "west", "west": "south", "south": "east", "east": "north"}


def stair_shapes(m):
    """Write every stair's `shape` as the game derives it from its neighbours
    (StairBlock.getStairsShape), so the written world is the world the server keeps."""
    def props(role):
        b = PALETTE.get(role)
        if not isinstance(b, str) or "_stairs[" not in b:
            return None
        kv = dict(p.split("=") for p in b[b.index("[") + 1:-1].split(","))
        return kv["facing"], kv["half"]

    def at(x, y, z):
        r = m.v.get((x, y, z))
        return props(r) if r else None

    new = {}
    for (x, y, z), r in list(m.v.items()):
        st = props(r)
        if st is None:
            continue
        f, h = st

        def take(face):
            dx, dz = DIRS[face]
            n = at(x + dx, y, z + dz)
            return n is None or n[0] != f or n[1] != h
        shape = "straight"
        dx, dz = DIRS[f]
        front = at(x + dx, y, z + dz)
        if front and front[1] == h:
            d = front[0]
            if (d in ("north", "south")) != (f in ("north", "south")) and take(OPP[d]):
                shape = "outer_left" if d == CCW[f] else "outer_right"
        if shape == "straight":
            back = at(x - dx, y, z - dz)
            if back and back[1] == h:
                d = back[0]
                if (d in ("north", "south")) != (f in ("north", "south")) and take(d):
                    shape = "inner_left" if d == CCW[f] else "inner_right"
        if shape != "straight":
            name = f"{r}~{shape}"
            if name not in PALETTE:
                PALETTE[name] = PALETTE[r].replace("shape=straight", f"shape={shape}")
                LOW.add(name)
            new[(x, y, z)] = name
    m.v.update(new)


OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


class Lighthouse(Place):
    """The starter's place, with the lighthouse's model in place of the empty room."""

    def lay_parts(self, parts):
        self.shift = self.datum.value - 1        # the model is drawn with its walk plane at course 1
        self.model = build_model()
        by_stem = {p["id"].removeprefix("part/"): p for p in parts}
        self.parts = []
        self.col_part = {}
        for stem, p in by_stem.items():
            e = {"part": p, "region": f"part-{stem}", "walked": p.get("reached", True), "cols": []}
            self.parts.append(e)
            for c, st in self.model.region.items():
                if st == stem:
                    e["cols"].append(c)
                    self.col_part[c] = e
        self.reach()
        # the air over the water under the quay's walk plane: nobody stands in it
        for (x, y, z), r in self.model.v.items():
            if r == AIR and y + self.shift < self.datum.value:
                self.unwalked.add((x, y + self.shift, z))

    def seam_space(self, s):
        (x0, _, z0), (x1, _, z1) = s["seam"]["cells"]
        e = self.col_part.get(((x0 + x1) // 2, (z0 + z1) // 2))
        return e["region"] if e is not None and e["walked"] else "room"

    def base_cell(self, x, y, z):
        kind = Place.base_cell(self, x, y, z)
        # the ring's four corners: nothing stands there, so no post marks the plot;
        # their ground course is the room's to walk
        if not self.in_space_xz(x, z) and kind == ("fill", "wall"):
            return ("claim", "room", None)
        if not self.in_space_xz(x, z):
            return kind
        if kind[0] == "claim" and kind[1].endswith("-way"):
            return kind          # a seam's opening is the connection's, kept clear
        r = self.model.get(x, y - self.shift, z)
        if r is None or r == AIR:
            if (x, y, z) in self.unwalked:
                return ("claim", "unwalked", None)
            if y < self.datum.value:
                return ("fill", "turf")
            return kind if kind[0] == "claim" else ("claim", "room", None)
        if r in FULL:
            return ("fill", r)
        # a block a body stands in or on: inside the space its column is
        if (x, y, z) in self.unwalked:
            return ("claim", "unwalked", r)
        if (x, y, z) not in self.reached:
            return ("fill", r)
        e = self.col_part.get((x, z))
        return ("claim", e["region"] if e is not None else "room", r)

    def reach(self):
        """Every standable cell a body cannot walk to from the plot's edges: the
        roof spaces, the wall heads, the aisle roofs. Claimed as `unwalked`."""
        self.unwalked = set()
        role = lambda x, y, z: self.model.get(x, y - self.shift, z)
        lo, hi = self.space

        def kind(x, y, z):
            if not (lo[0] <= x <= hi[0] and lo[2] <= z <= hi[2]) or y < 0 or y > hi[1] + 1:
                return "pass"
            r = role(x, y, z)
            if r == "water":
                return "water"
            if r is None or r == AIR:
                return "full" if y < self.datum.value else "pass"
            if r in FULL:
                return "full"
            if r in TALL:
                return "tall"
            if r in LOW:
                return "low"
            return "pass"

        def standable(x, y, z):
            k = kind(x, y, z)
            if k not in ("pass", "low") or kind(x, y + 1, z) != "pass":
                return False
            return k == "low" or kind(x, y - 1, z) in ("full", "low", "tall")

        cols = {(x, z) for x in range(lo[0], hi[0] + 1) for z in range(lo[2], hi[2] + 1)}
        cells = {(x, y, z) for (x, z) in cols for y in range(1, hi[1] + 1) if standable(x, y, z)}
        crowns = {c for c in cells if role(c[0], c[1] - 1, c[2]) in ("yew", "bush", "yew_log")}
        walk = cells - crowns
        start = [(x, y, z) for (x, y, z) in walk if y == self.datum.value and (x in (lo[0], hi[0]) or z in (lo[2], hi[2]))]
        seen, todo = set(start), list(start)
        while todo:
            x, y, z = todo.pop()
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, nz = x + dx, z + dz
                def floor_h(cx, cy, cz):
                    # a low block's top is half a course up; a wall or fence's is half a course over its cell
                    return cy + (0.5 if kind(cx, cy, cz) == "low" or kind(cx, cy - 1, cz) == "tall" else 0)
                h0 = floor_h(x, y, z)
                for ny in (y, y + 1):
                    if floor_h(nx, ny, nz) - h0 > 1:
                        continue
                    if (nx, ny, nz) in walk and (nx, ny, nz) not in seen:
                        seen.add((nx, ny, nz))
                        todo.append((nx, ny, nz))
                        break
                else:
                    ny = y - 1
                    while ny >= 1 and kind(nx, ny, nz) == "pass" and (nx, ny, nz) not in cells:
                        ny -= 1
                    if (nx, ny, nz) in walk and (nx, ny, nz) not in seen and kind(nx, y, nz) == "pass":
                        seen.add((nx, ny, nz))
                        todo.append((nx, ny, nz))
        for c in cells - seen:
            e = self.col_part.get((c[0], c[2]))
            if e is None or e["walked"]:
                self.unwalked.add(c)
        # A cavity sealed from the sky and the ground (the roof space over a
        # vault): every cell of its air is out of walk, not only its floor.
        self.reached = seen
        air = lambda c: role(*c) in (None, AIR) and lo[0] <= c[0] <= hi[0] and lo[2] <= c[2] <= hi[2] and 1 <= c[1] <= hi[1]
        done = set()
        for c0 in sorted(self.unwalked):
            if c0 in done:
                continue
            comp, todo, open_ = {c0}, [c0], False
            while todo:
                x, y, z = todo.pop()
                for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    n = (x + d[0], y + d[1], z + d[2])
                    if n in comp:
                        continue
                    if not air(n):
                        inside = lo[0] <= n[0] <= hi[0] and lo[2] <= n[2] <= hi[2] and 1 <= n[1] <= hi[1]
                        if not inside:
                            open_ = True      # it runs out of the piece: the sky or the ring
                        continue
                    if n in seen:
                        open_ = True
                        continue
                    comp.add(n)
                    todo.append(n)
                if open_ or len(comp) > 20000:
                    open_ = True
                    break
            done |= comp
            if not open_:
                for c in comp:
                    e = self.col_part.get((c[0], c[2]))
                    if e is None or e["walked"]:
                        self.unwalked.add(c)

    def cuts(self, axis):
        n = self.n[axis]
        out = super().cuts(axis)
        best = {b.value: b for b in out}
        for v in range(n):
            best.setdefault(v, lit(v))
        return [best[v] for v in sorted(best)]


def body(p, rules):
    """The place, cut on x, then y, then z; equal neighbours merged into one span."""
    xs, ys, zs = p.cuts(0), p.cuts(1), p.cuts(2)

    def runs(cuts, items):
        out_c, out_i = [], []
        for c, it in zip(cuts, items):
            if out_i and json.dumps(out_i[-1], sort_keys=True) == json.dumps(it, sort_keys=True):
                continue
            out_c.append(c)
            out_i.append(it)
        return out_c, out_i

    columns = []
    for x in xs:
        courses = []
        for y in ys:
            row = [leaf(p.cell(x.value, y.value, z.value)) for z in zs]
            cz, rz = runs(zs, row)
            courses.append(rules.name(split("z", cz, rz), "row"))
        cy, ry = runs(ys, courses)
        columns.append(rules.name(split("y", cy, ry), "column"))
    cx, rx = runs(xs, columns)
    return split("x", cx, rx)


FULL = {"floor", "wall", "lid", "turf", "path", "flags", "base", "white", "band", "corbel", "dark", "newel",
        "landing", "slit", "lamp_glass", "mullion", "lamp_floor", "great_lamp", "cap", "stone", "plaster", "post",
        "beam_x", "beam_z", "boards", "floorb", "glass", "roof", "chimney", "hearth", "shelf", "barrel", "ywall",
        "trough", "woodpile", "bush", "gallery", "table", "newel_lamp", "plinth_ring"}
TALL = {"rail", "finial", "lamp_post"}
LOW = {"step_e", "step_s", "step_w", "step_n", "lantern", "roof_n", "roof_s", "ridge", "chair", "candles",
       "pot_a", "pot_b", "pot_c", "ycap", "bench", "cone_n", "cone_s", "cone_e", "cone_w"}

_starter_contract = contract


def contract(p):
    out = _starter_contract(p)
    if p.unwalked:
        out.setdefault("no_body", {})["unwalked"] = {
            "reason": "the roofs, the wall heads, the lantern room's cap and the gallery's rail: seen, never stood on"}
    return out


def shown_faces(p):
    """The four sides; the top course is open sky."""
    return ["east", "north", "south", "west"]


MARK_AT = {"node-lighthouse": (8, 6, "west")}   # in the keeper's cottage, facing its front door


def marks(p, inner):
    """Every owed name, marked where the lighthouse puts it."""
    out = inner
    for name in reversed(p.a["owed_anchors"]):
        stem = name.removeprefix("anchor/")
        x, z, facing = MARK_AT[stem]
        assert p.walkable(p.cell(x, p.datum.value, z)), stem
        mark = {"anchor": stem, "at": "offset", "facing": facing, "y": p.datum.expr, "x": num(x), "z": num(z)}
        out = {"body": out, "mark": mark, "op": "mark"}
    return out


if __name__ == "__main__":
    raise SystemExit(main())
