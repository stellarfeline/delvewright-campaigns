#!/usr/bin/env python3
"""Emits programs/castle.json: Doune's own program (doune/, copied verbatim from
campaigns/doune-castle-tour/design/programs) seated in node/castle's frame.

The seat changes nothing of Doune's design:
  1. the frame starts at Doune's local y4 (the floor course under its deepest
     ditch), so the four rock courses under it are not carried;
  2. the ring's courses under the plateau's surface are the whole's fixed
     ground, so the program skips them;
  3. the whole site is claimed as one open space, `site`, the piece's contract,
     entered from the road where Doune's approach road leaves the plot's north
     edge (`road-mouth`, the seam's contact).
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "doune"))
import build_castle as bc  # noqa: E402

CUT = 4          # Doune courses under the frame
FIXED = 4        # the ring's fixed-ground courses (frame y0..3 = Doune y4..7)
X, Y, Z = bc.X, bc.Y, bc.Z
ROAD_X, ROAD_W = 75, 5   # Doune's approach road where it leaves the plot's north edge
MOUTH_H = 6              # the contact's height over the walk plane: the road place's open courses


FIXES = {}
# Two posts flank Doune's approach road where it leaves the plot, so the plot's
# open north edge meets the road place only across the road's own width.
for _y in range(8, 14):
    FIXES[(ROAD_X - 1, _y, 0)] = "wall"
    FIXES[(ROAD_X + ROAD_W, _y, 0)] = "wall"
# The two names the site plan owes this place, marked beside Doune's own:
# where the party spawns (a step behind Doune's arrival, facing the castle) and
# the place's own name (in the courtyard, beside the guide's stop).
bc.ANCHORS[(77, bc.WALK, 2)] = ("spawn", None)
bc.ANCHORS[(46, bc.WALK, 63)] = ("node-castle", None)
bc.FACING["spawn"] = "south"
bc.FACING["node-castle"] = "north"
PALETTE = bc.PALETTE


def fixed_column(x, z):
    col = bc.column(x, z)
    cells = {y: r for (fx, y, fz), r in FIXES.items() if (fx, fz) == (x, z)}
    if not cells:
        return col
    flat = [r for r, n in col.spans for _ in range(n)]
    for y, r in cells.items():
        flat[y] = r
    spans = []
    for r in flat:
        if spans and spans[-1][0] == r:
            spans[-1] = (r, spans[-1][1] + 1)
        else:
            spans.append((r, 1))
    col.spans = spans
    return col


def sz(n):
    return {"size": "absolute", "blocks": {"expr": "int", "value": n}}


def trim(node, k, ring, mouth=False, here=None):
    """Drop k bottom courses of a column node; on the ring, skip the next FIXED."""
    assert node.get("op") == "split" and node["axis"] == "y", node.get("op")
    spans = [(s["blocks"]["value"], c) for s, c in zip(node["sizes"], node["children"])]
    assert sum(n for n, _ in spans) == Y
    out, drop = [], k
    for n, c in spans:
        if drop >= n:
            drop -= n
            continue
        if drop:
            assert c.get("op") != "mark", "a mark under the cut"
            n -= drop
            drop = 0
        out.append((n, c))
    if ring:
        rest, skip = [], FIXED
        for n, c in out:
            if skip >= n:
                assert c.get("op") != "mark"
                skip -= n
                continue
            if skip:
                n -= skip
                skip = 0
            rest.append((n, c))
        out = [(FIXED, {"op": "skip"})] + rest
    assert sum(n for n, _ in out) == Y - k
    out = crowns(out)
    for y in UNWALKED.get(here, ()):
        out = claim_band(out, y, y + 1, "unwalked")
    if mouth:
        out = claim_band(out, FIXED, FIXED + MOUTH_H, "road-mouth")
    if any(c.get("op") == "claim" for _, c in out):
        out = [(n, c if c.get("op") == "claim" else {"op": "claim", "region": "site", "body": c})
               for n, c in out]
        return {"op": "split", "axis": "y", "sizes": [sz(n) for n, _ in out],
                "children": [c for _, c in out]}
    return {"op": "claim", "region": "site",
            "body": {"op": "split", "axis": "y", "sizes": [sz(n) for n, _ in out],
                     "children": [c for _, c in out]}}


UNWALKED = {}
for _line in (HERE / "unwalked.txt").read_text().splitlines():
    if _line and not _line.startswith("#"):
        _x, _y, _z = map(int, _line.split(","))
        UNWALKED.setdefault((_x, _z), []).append(_y)


LEAVES = {"yard/oak_leaf", "yard/spruce_leaf"}


def role_of(c):
    while c.get("op") == "mark":
        c = c["body"]
    return c.get("material", {}).get("role") if c.get("op") == "fill" else None


def crowns(spans):
    """The course over a tree's crown is out of walk: nobody climbs the trees."""
    out, after_leaf = [], False
    for n, c in spans:
        if after_leaf and role_of(c) is None and c.get("op") == "void":
            out.append((1, {"op": "claim", "region": "crowns", "body": c}))
            if n > 1:
                out.append((n - 1, c))
        else:
            out.append((n, c))
        after_leaf = role_of(c) in LEAVES
    return out


def claim_band(spans, y0, y1, region):
    """Wrap frame courses y0..y1-1 of a column's spans in a `claim`."""
    out, y = [], 0
    for n, c in spans:
        lo, hi = max(y, y0), min(y + n, y1)
        if lo >= hi:
            out.append((n, c))
        else:
            assert c.get("op") != "mark", "a mark in the mouth"
            if lo > y:
                out.append((lo - y, c))
            out.append((hi - lo, {"op": "claim", "region": region, "body": c}))
            if y + n > hi:
                out.append((y + n - hi, c))
        y += n
    return out


def build():
    rows = []
    for z in range(Z):
        cols = [fixed_column(x, z) for x in range(X)]
        rows.append([trim(bc.column_node(x, z, cols[x]), CUT, x in (0, X - 1) or z in (0, Z - 1),
                          z == 0 and ROAD_X <= x < ROAD_X + ROAD_W, (x, z))
                     for x in range(X)])

    def merge(items):
        """Equal neighbours merge into one span (the original emitter's partition)."""
        out = []
        for it in items:
            if out and out[-1][1] == it:
                out[-1][0] += 1
            else:
                out.append([1, it])
        return out
    z_nodes = []
    for row in rows:
        xs = merge([json.dumps(c, sort_keys=True) for c in row])
        z_nodes.append(json.dumps({"op": "split", "axis": "x", "sizes": [sz(n) for n, _ in xs],
                                   "children": [json.loads(c) for _, c in xs]}, sort_keys=True))
    zs = merge(z_nodes)
    return {"op": "split", "axis": "z", "sizes": [sz(n) for n, _ in zs],
            "children": [json.loads(c) for _, c in zs]}


PROGRAM = {
    "version": "1.9.0",
    "name": "doune_castle_plot",
    "start": "site",
    "params": {},
    "palette": PALETTE,
    "rules": {"site": [{"weight": 1, "body": build()}]},
    "contract": {"entry": "site", "spaces": {"site": {"envelope": "open"}},
                 "no_body": {"crowns": {"reason": "the tops of the trees on the grounds: nothing anybody climbs"},
                             "unwalked": {"reason": "window embrasures open only to the outside, wall heads, the cloth of estate and the high table, the well beam and the approach's marker posts: seen, never stood on"}},
                 "edges": [{"a": "site", "b": "exterior", "class": "walk", "via": "road-mouth"}]},
    "shown_faces": ["north", "south", "east", "west"],
}

if not UNWALKED:
    del PROGRAM["contract"]["no_body"]["unwalked"]

if __name__ == "__main__":
    out = HERE.parent.parent / "programs" / "castle.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(PROGRAM, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes), {X}x{Y - CUT}x{Z}")
