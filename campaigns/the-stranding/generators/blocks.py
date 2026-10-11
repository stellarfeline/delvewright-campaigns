"""Block states, every property written (the grammar's states-complete gate).

Defaults come from the engine's pinned registry (`crates/dsl/data/
block-defaults-1.21.11.json` in `$DELVEWRIGHT_ENGINE`), so a state is written
from the game's own property list and never from memory. `derive()` sets the
properties vanilla computes from neighbours (stair shapes, fence/pane/wall
connections) over a finished model.
"""

import json
import os

_DEF = None


def defaults():
    global _DEF
    if _DEF is None:
        p = os.path.join(os.environ["DELVEWRIGHT_ENGINE"], "crates/dsl/data/block-defaults-1.21.11.json")
        _DEF = json.load(open(p))
    return _DEF


def parse(state):
    if "[" in state:
        name, rest = state.split("[", 1)
        props = dict(kv.split("=") for kv in rest.rstrip("]").split(",") if kv)
    else:
        name, props = state, {}
    if ":" not in name:
        name = "minecraft:" + name
    return name, props


def fmt(name, props):
    if not props:
        return name
    return name + "[" + ",".join("%s=%s" % (k, props[k]) for k in sorted(props)) + "]"


def complete(state):
    name, props = parse(state)
    d = defaults().get(name)
    if d:
        full = dict(d)
        for k, v in props.items():
            if k not in full:
                raise ValueError("%s has no property %s" % (name, k))
            full[k] = v
        return fmt(name, full)
    if props:
        raise ValueError("%s takes no properties" % name)
    return name


def S(state, **kw):
    """A state with keyword properties, completed."""
    name, props = parse(state)
    props.update({k: str(v).lower() for k, v in kw.items()})
    return complete(fmt(name, props))


def stairs(fam, facing, half="bottom"):
    return S("minecraft:%s_stairs" % fam, facing=facing, half=half)


def slab(fam, type_="bottom"):
    return S("minecraft:%s_slab" % fam, type=type_)


def name_of(state):
    return parse(state)[0]


# -- what vanilla derives from the neighbours ---------------------------------
CCW = {"north": "west", "west": "south", "south": "east", "east": "north"}
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
STEP = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0)}

NOT_FULL_SUFFIX = ("_stairs", "_slab", "_fence", "_pane", "_wall", "_door", "_trapdoor", "lantern",
                   "torch", "_sign", "_banner", "carpet", "candle", "_button", "lever", "_chain",
                   "iron_bars", "ladder", "vine", "vines", "vines_plant", "_bed", "flower_pot", "_head",
                   "_skull", "rail", "pressure_plate", "scaffolding", "_gate", "end_rod", "bell",
                   "campfire", "cobweb", "lichen", "_roots", "sapling", "short_grass", "tall_grass",
                   "seagrass", "fern", "_bush", "bush", "kelp", "kelp_plant", "sea_pickle", "copper_bulb",
                   "lily_pad", "_coral", "_coral_fan", "pointed_dripstone", "amethyst_cluster", "_bud",
                   "water", "lava", "air", "structure_void", "snow", "hopper", "cauldron", "anvil", "chest",
                   "brewing_stand", "grindstone", "lectern", "composter", "cake", "conduit", "decorated_pot",
                   "sculk_vein", "sculk_sensor", "sculk_shrieker", "_wall_fan", "mushroom", "flower",
                   "dandelion", "poppy", "tulip", "orchid", "allium", "bluet", "daisy", "cornflower",
                   "lily_of_the_valley", "rose", "lilac", "peony", "sunflower", "petals", "wildflowers",
                   "leaf_litter", "dead_bush", "sugar_cane", "bamboo", "cactus", "spore_blossom",
                   "hanging_roots", "dripleaf", "dripleaf_stem", "azalea", "nether_sprouts", "fungus",
                   "stonecutter", "enchanting_table", "daylight_detector", "sculk_catalyst_never",
                   "iron_chain", "heavy_core", "frogspawn", "turtle_egg", "sniffer_egg", "egg")
FULL_EXCEPTIONS = ("minecraft:mushroom_stem", "minecraft:red_mushroom_block", "minecraft:brown_mushroom_block",
                   "minecraft:snow_block", "minecraft:azalea_leaves", "minecraft:flowering_azalea_leaves",
                   "minecraft:bamboo_block", "minecraft:stripped_bamboo_block", "minecraft:bamboo_planks",
                   "minecraft:bamboo_mosaic", "minecraft:dried_kelp_block")


def is_full(state):
    n = name_of(state)
    if n in FULL_EXCEPTIONS or n.endswith("_coral_block") or n.endswith("_planks") or n.endswith("_wool"):
        return True
    if n in ("minecraft:air", "minecraft:structure_void", "minecraft:water", "minecraft:mud", "minecraft:soul_sand",
             "minecraft:dirt_path", "minecraft:farmland", "minecraft:honey_block"):
        return False
    return not any(n.endswith(t) for t in NOT_FULL_SUFFIX)


def is_stairs(state):
    return name_of(state).endswith("_stairs")


def derive(cells):
    """cells: dict (x,y,z) -> state; rewrites derived properties in place."""
    get = lambda c: cells.get(c, "minecraft:air")
    out = {}
    for c, st in cells.items():
        name, props = parse(st)
        if name.endswith("_stairs"):
            f, h = props["facing"], props["half"]
            shape = "straight"
            dx, dy, dz = STEP[f]
            front = get((c[0] + dx, c[1], c[2] + dz))
            done = False
            if is_stairs(front):
                n2, p2 = parse(front)
                if p2["half"] == h:
                    f1 = p2["facing"]
                    if (f1 in ("east", "west")) != (f in ("east", "west")):
                        ox, _, oz = STEP[OPP[f1]]
                        side = get((c[0] + ox, c[1], c[2] + oz))
                        ok = not (is_stairs(side) and parse(side)[1]["facing"] == f and parse(side)[1]["half"] == h)
                        if ok:
                            shape = "outer_left" if f1 == CCW[f] else "outer_right"
                            done = True
            if not done:
                bx, _, bz = STEP[OPP[f]]
                back = get((c[0] + bx, c[1], c[2] + bz))
                if is_stairs(back):
                    n3, p3 = parse(back)
                    if p3["half"] == h:
                        f2 = p3["facing"]
                        if (f2 in ("east", "west")) != (f in ("east", "west")):
                            sx, _, sz = STEP[f2]
                            side = get((c[0] + sx, c[1], c[2] + sz))
                            ok = not (is_stairs(side) and parse(side)[1]["facing"] == f and parse(side)[1]["half"] == h)
                            if ok:
                                shape = "inner_left" if f2 == CCW[f] else "inner_right"
            props["shape"] = shape
            out[c] = fmt(name, props)
        elif name.endswith("_fence") or name.endswith("_pane") or name == "minecraft:iron_bars" or name == "minecraft:glass_pane":
            for d, (dx, _, dz) in STEP.items():
                nb = get((c[0] + dx, c[1], c[2] + dz))
                nn = name_of(nb)
                if name.endswith("_fence"):
                    con = is_full(nb) or nn.endswith("_fence") or nn.endswith("_fence_gate")
                else:
                    con = is_full(nb) or nn.endswith("_pane") or nn == "minecraft:iron_bars" or nn.endswith("_wall")
                props[d] = "true" if con else "false"
            out[c] = fmt(name, props)
        elif name.endswith("_wall") and name != "minecraft:wall_torch":
            anyc = []
            for d, (dx, _, dz) in STEP.items():
                nb = get((c[0] + dx, c[1], c[2] + dz))
                nn = name_of(nb)
                con = is_full(nb) or nn.endswith("_wall") or nn.endswith("_pane") or nn == "minecraft:iron_bars" or nn.endswith("_fence_gate")
                if con:
                    above = get((c[0], c[1] + 1, c[2]))
                    props[d] = "tall" if is_full(above) else "low"
                    anyc.append(d)
                else:
                    props[d] = "none"
            straight = sorted(anyc) in (["east", "west"], ["north", "south"])
            above = get((c[0], c[1] + 1, c[2]))
            props["up"] = "false" if (straight and not is_full(above)) else "true"
            out[c] = fmt(name, props)
    cells.update(out)
