"""Building helpers for the upper street's plots drawn on the skill starter's
`Model` (the plots built before it stay on plotlib.py): full block states,
written with every property, and a few shapes a builder reaches for. Each
helper draws into a `Model` through its `set`/`get`; nothing here decides
where a body goes.
"""

AIR = "~air"


def mc(name: str) -> str:
    return name if name.startswith("minecraft:") else f"minecraft:{name}"


def stairs(mat, facing, half="bottom", shape="straight"):
    return f"{mc(mat)}_stairs[facing={facing},half={half},shape={shape},waterlogged=false]"


def slab(mat, kind="bottom"):
    return f"{mc(mat)}_slab[type={kind},waterlogged=false]"


def log(mat, axis="y"):
    return f"{mc(mat)}[axis={axis}]"


def door(mat, facing, half, hinge="left"):
    return f"{mc(mat)}_door[facing={facing},half={half},hinge={hinge},open=false,powered=false]"


def trapdoor(mat, facing, half="bottom", open_=False):
    return f"{mc(mat)}_trapdoor[facing={facing},half={half},open={'true' if open_ else 'false'},powered=false,waterlogged=false]"


def fence(mat):
    return f"{mc(mat)}_fence[east=false,north=false,south=false,waterlogged=false,west=false]"


def wall(mat):
    return f"{mc(mat)}_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]"


def pane(mat):
    return f"{mc(mat)}[east=false,north=false,south=false,waterlogged=false,west=false]"


def lantern(hanging=False):
    return f"minecraft:lantern[hanging={'true' if hanging else 'false'},waterlogged=false]"


def leaves(mat):
    return f"{mc(mat)}_leaves[distance=1,persistent=true,waterlogged=false]"


def bed(colour, facing, part):
    return f"minecraft:{colour}_bed[facing={facing},occupied=false,part={part}]"


def candle(n=1, colour="white"):
    return f"minecraft:{colour}_candle[candles={n},lit=true,waterlogged=false]"


def wall_torch(facing):
    return f"minecraft:wall_torch[facing={facing}]"


def campfire(facing="north"):
    return f"minecraft:campfire[facing={facing},lit=true,signal_fire=false,waterlogged=false]"


def ring(x0, x1, z0, z1):
    """The cells of a rectangle's outline, inclusive."""
    return [(x, z) for x in range(x0, x1 + 1) for z in (z0, z1)] + \
           [(x, z) for z in range(z0 + 1, z1) for x in (x0, x1)]


def window(m, x, z, glass, y0=2, h=2):
    for y in range(y0, y0 + h):
        m.set(x, y, z, glass)


def door2(m, x, z, mat, facing, hinge="left"):
    m.set(x, 1, z, door(mat, facing, "lower", hinge))
    m.set(x, 2, z, door(mat, facing, "upper", hinge))


def bed2(m, x, z, colour, facing):
    """A bed whose head lies toward `facing` from (x, z)."""
    dx, dz = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}[facing]
    m.set(x, 1, z, bed(colour, facing, "foot"))
    m.set(x + dx, 1, z + dz, bed(colour, facing, "head"))


def bed_of(m, cells, flowers, soil="minecraft:grass_block[snowy=false]"):
    """A flower bed: soil at the ground course, a bloom on each cell in turn."""
    for i, (x, z) in enumerate(cells):
        m.set(x, 0, z, soil)
        m.set(x, 1, z, flowers[i % len(flowers)])


def gable_roof(m, x0, x1, z0, z1, head, along, mat, fill=None, overhang=1, ridge=None):
    """A pitched roof over walls x0..x1, z0..z1 (inclusive) whose heads stand
    at course `head`: its first course sits beside the wall heads (the eave,
    `overhang` out), each course one in and one up, so the slope rests on the
    walls and the space under it is closed. The ridge runs along `along`
    ('x' or 'z'); the gable ends are filled with `fill` under the slope. An
    odd span is capped with a slab course (or `ridge`). Returns the top course."""
    if along == "x":
        a0, a1, b0, b1 = x0 - overhang, x1 + overhang, z0 - overhang, z1 + overhang
        w0, w1, ends = z0, z1, (x0, x1)

        def put(a, y, b, s):
            m.set(a, y, b, s)
    else:
        a0, a1, b0, b1 = z0 - overhang, z1 + overhang, x0 - overhang, x1 + overhang
        w0, w1, ends = x0, x1, (z0, z1)

        def put(a, y, b, s):
            m.set(b, y, a, s)
    f_lo, f_hi = ("south", "north") if along == "x" else ("east", "west")
    width = b1 - b0 + 1
    y0 = head - (overhang - 1) if overhang >= 1 else head + 1
    top = y0
    for i in range(width // 2):
        y = y0 + i
        top = y
        for a in range(a0, a1 + 1):
            put(a, y, b0 + i, stairs(mat, f_lo))
            put(a, y, b1 - i, stairs(mat, f_hi))
        if fill is not None:
            for b in range(max(b0 + i + 1, w0), min(b1 - i - 1, w1) + 1):
                for a in ends:
                    put(a, y, b, fill)
    if width % 2 == 1:
        y = y0 + width // 2
        for a in range(a0, a1 + 1):
            put(a, y, b0 + width // 2, ridge or slab(mat))
        top = y
    return top
