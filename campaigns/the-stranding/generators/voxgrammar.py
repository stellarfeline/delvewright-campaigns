"""Shared helper: a voxel model (block + claim per cell) written as a box-split grammar program.

The campaign's detail programs for its boats are computed from a few
proportions (see ferry_house.py and its README notes). This module turns the
computed model into the engine's program surface: a split along one axis into
one-cell slices, each slice into one-cell columns, each column into runs of
equal (block, claim), and every run a `fill`/`void` wrapped in its `claim`.
Deterministic: no clock, no RNG, sorted iteration only.
"""

def lit(v):
    return {"expr": "int", "value": v}

def run_node(block, claim):
    body = {"op": "void"} if block is None else {"op": "fill", "material": block}
    if claim:
        body = {"op": "claim", "region": claim, "body": body}
    return body

def column(cells):
    """cells: list over y of (block, claim). Returns a split along y."""
    runs = []
    for c in cells:
        if runs and runs[-1][0] == c:
            runs[-1][1] += 1
        else:
            runs.append([c, 1])
    if len(runs) == 1:
        return run_node(*runs[0][0])
    return {"op": "split", "axis": "y",
            "sizes": [{"size": "absolute", "blocks": lit(n)} for _, n in runs],
            "children": [run_node(*c) for c, _ in runs]}

def slab_x(model, xs, ys, z):
    """One z-row: a split along x of columns."""
    cols = [column([model(x, y, z) for y in ys]) for x in xs]
    if len(set(map(repr, cols))) == 1:
        return cols[0]
    return {"op": "split", "axis": "x",
            "sizes": [{"size": "absolute", "blocks": lit(1)} for _ in xs],
            "children": cols}

def rows_z(model, xs, ys, zs):
    rows = [slab_x(model, xs, ys, z) for z in zs]
    return {"op": "split", "axis": "z",
            "sizes": [{"size": "absolute", "blocks": lit(1)} for _ in zs],
            "children": rows}

def marked(body, marks):
    """marks: list of (stem, (x,y,z), facing) offsets from the frame's minimum corner."""
    for stem, (x, y, z), facing in sorted(marks, reverse=True):
        m = {"anchor": stem, "at": "offset", "x": lit(x), "y": lit(y), "z": lit(z)}
        if facing:
            m["facing"] = facing
        body = {"op": "mark", "mark": m, "body": body}
    return body

def fence(wood, n=False, e=False, s=False, w=False):
    b = lambda v: "true" if v else "false"
    return f"minecraft:{wood}_fence[east={b(e)},north={b(n)},south={b(s)},waterlogged=false,west={b(w)}]"
