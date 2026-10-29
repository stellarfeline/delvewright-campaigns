#!/usr/bin/env python3
"""Emits programs/castle.json: Doune's own program (doune/, copied verbatim from
campaigns/doune-castle-tour/design/programs) seated in node/castle's frame.

Three changes, all at the seat, none to Doune's design:
  1. the frame starts at Doune's local y4 (the floor course under its deepest
     ditch), so the four rock courses under it are not carried;
  2. the ring's courses under the plateau's surface are the whole's fixed
     ground, so the program skips them;
  3. the whole site is claimed as one open space, `site`, the piece's contract.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "doune"))
import build_castle as bc  # noqa: E402

CUT = 4          # Doune courses under the frame
FIXED = 4        # the ring's fixed-ground courses (frame y0..3 = Doune y4..7)
X, Y, Z = bc.X, bc.Y, bc.Z


def sz(n):
    return {"size": "absolute", "blocks": {"expr": "int", "value": n}}


def trim(node, k, ring):
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
    return {"op": "split", "axis": "y", "sizes": [sz(n) for n, _ in out],
            "children": [c for _, c in out]}


def build():
    rows = []
    for z in range(Z):
        cols = [bc.column(x, z) for x in range(X)]
        rows.append([trim(bc.column_node(x, z, cols[x]), CUT, x in (0, X - 1) or z in (0, Z - 1))
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
    "palette": bc.PALETTE,
    "rules": {"site": [{"weight": 1, "body": {"op": "claim", "region": "site", "body": build()}}]},
    "contract": {"entry": "site", "spaces": {"site": {"envelope": "open"}}, "edges": []},
    "shown_faces": ["north", "south", "east", "west"],
}

if __name__ == "__main__":
    out = HERE.parent.parent / "programs" / "castle.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(PROGRAM, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes), {X}x{Y - CUT}x{Z}")
