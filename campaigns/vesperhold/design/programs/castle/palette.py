"""The site's shared materials. Parts that need their own add them where they
are used, through `grid.block` / `grid.stairs` / `grid.slab`."""
from .grid import PAL, state

R = PAL.role

BEDROCK = R("bedrock", "minecraft:stone")
EARTH = R("earth", "minecraft:dirt")
TURF = R("turf", [
    {"weight": 10, "block": "minecraft:grass_block[snowy=false]"},
    {"weight": 2, "block": "minecraft:moss_block"},
    {"weight": 2, "block": "minecraft:coarse_dirt"},
    {"weight": 1, "block": "minecraft:podzol[snowy=false]"},
])
ROCK = R("rock", [
    {"weight": 4, "block": "minecraft:tuff"},
    {"weight": 3, "block": "minecraft:deepslate[axis=y]"},
    {"weight": 2, "block": "minecraft:andesite"},
    {"weight": 2, "block": "minecraft:stone"},
    {"weight": 1, "block": "minecraft:cobbled_deepslate"},
])
ROCK_MOSS = R("rock_moss", [
    {"weight": 4, "block": "minecraft:tuff"},
    {"weight": 3, "block": "minecraft:moss_block"},
    {"weight": 2, "block": "minecraft:mossy_cobblestone"},
    {"weight": 2, "block": "minecraft:deepslate[axis=y]"},
])
ROAD = R("road", [
    {"weight": 4, "block": "minecraft:gravel"},
    {"weight": 3, "block": "minecraft:coarse_dirt"},
    {"weight": 2, "block": "minecraft:cobblestone"},
    {"weight": 1, "block": "minecraft:tuff"},
])
WALL = R("wall", [
    {"weight": 10, "block": "minecraft:stone_bricks"},
    {"weight": 3, "block": "minecraft:cracked_stone_bricks"},
    {"weight": 2, "block": "minecraft:mossy_stone_bricks"},
    {"weight": 1, "block": "minecraft:cobblestone"},
    {"weight": 1, "block": "minecraft:andesite"},
])
# the ruined top courses: the same stone with gaps in it
WALL_RUIN = R("wall_ruin", [
    {"weight": 6, "block": "minecraft:stone_bricks"},
    {"weight": 3, "block": "minecraft:cracked_stone_bricks"},
    {"weight": 2, "block": "minecraft:mossy_cobblestone"},
    {"weight": 4, "block": "minecraft:air"},
])
KEEP = R("keep", [
    {"weight": 8, "block": "minecraft:stone_bricks"},
    {"weight": 3, "block": "minecraft:tuff_bricks"},
    {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
    {"weight": 1, "block": "minecraft:polished_tuff"},
])
CHAPEL = R("chapel", [
    {"weight": 8, "block": "minecraft:tuff_bricks"},
    {"weight": 3, "block": "minecraft:stone_bricks"},
    {"weight": 2, "block": "minecraft:polished_tuff"},
    {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
])
TRIM = R("trim", "minecraft:chiseled_stone_bricks")
TRIM_TUFF = R("trim_tuff", "minecraft:chiseled_tuff_bricks")
PILLAR = R("pillar", "minecraft:polished_andesite")
QUOIN = R("quoin", "minecraft:polished_deepslate")
FLAG = R("flag", [
    {"weight": 8, "block": "minecraft:stone_bricks"},
    {"weight": 3, "block": "minecraft:cracked_stone_bricks"},
    {"weight": 2, "block": "minecraft:cobblestone"},
    {"weight": 2, "block": "minecraft:mossy_cobblestone"},
    {"weight": 1, "block": "minecraft:gravel"},
])
FLOOR = R("floor", [
    {"weight": 6, "block": "minecraft:polished_andesite"},
    {"weight": 3, "block": "minecraft:stone_bricks"},
    {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
])
FLOOR_HALL = R("floor_hall", [
    {"weight": 5, "block": "minecraft:polished_deepslate"},
    {"weight": 3, "block": "minecraft:deepslate_tiles"},
    {"weight": 1, "block": "minecraft:cracked_deepslate_tiles"},
])
PLANKS = R("planks", "minecraft:spruce_planks")
DARK_PLANKS = R("dark_planks", "minecraft:dark_oak_planks")
BEAM = R("beam_x", "minecraft:stripped_dark_oak_log[axis=x]")
BEAM_Z = R("beam_z", "minecraft:stripped_dark_oak_log[axis=z]")
POST = R("post", "minecraft:stripped_dark_oak_log[axis=y]")
HAY = R("hay", "minecraft:hay_block[axis=y]")
STRAW = R("straw", [
    {"weight": 4, "block": "minecraft:coarse_dirt"},
    {"weight": 3, "block": "minecraft:rooted_dirt"},
    {"weight": 2, "block": "minecraft:podzol[snowy=false]"},
    {"weight": 1, "block": "minecraft:gravel"},
])
GLASS = R("glass", "minecraft:gray_stained_glass")
GLASS_DARK = R("glass_dark", "minecraft:black_stained_glass")
ROSE_GLASS = R("rose_glass", [
    {"weight": 3, "block": "minecraft:red_stained_glass"},
    {"weight": 2, "block": "minecraft:blue_stained_glass"},
    {"weight": 2, "block": "minecraft:purple_stained_glass"},
    {"weight": 1, "block": "minecraft:yellow_stained_glass"},
])
BOOKS = R("books", "minecraft:bookshelf")
WATER = R("water", "minecraft:water[level=0]")
LANTERN = R("lantern", state("minecraft:lantern", hanging=False, waterlogged=False))
LANTERN_HANG = R("lantern_hang", state("minecraft:lantern", hanging=True, waterlogged=False))
SOUL_LANTERN = R("soul_lantern", state("minecraft:soul_lantern", hanging=False, waterlogged=False))
CHAIN = R("chain", state("minecraft:iron_chain", axis="y", waterlogged=False))
CANDLES = R("candles", state("minecraft:white_candle", candles=3, lit=True, waterlogged=False))
LOG = R("log", "minecraft:spruce_log[axis=y]")
LEAVES = R("leaves", state("minecraft:spruce_leaves", distance=1, persistent=True, waterlogged=False))
DARK_LEAVES = R("dark_leaves", state("minecraft:dark_oak_leaves", distance=1, persistent=True, waterlogged=False))
COBWEB = R("cobweb", "minecraft:cobweb")
BARS_X = R("bars_x", state("minecraft:iron_bars", east=True, north=False, south=False, waterlogged=False, west=True))
BARS_Z = R("bars_z", state("minecraft:iron_bars", east=False, north=True, south=True, waterlogged=False, west=False))
GATE_WOOD = R("gate_wood", "minecraft:dark_oak_planks")
PSALTER = R("psalter", "minecraft:bookshelf")
ROOF = R("roof", [
    {"weight": 8, "block": "minecraft:deepslate_tiles"},
    {"weight": 2, "block": "minecraft:cracked_deepslate_tiles"},
    {"weight": 1, "block": "minecraft:deepslate_bricks"},
])
ROOF_RUIN = R("roof_ruin", [
    {"weight": 6, "block": "minecraft:deepslate_tiles"},
    {"weight": 2, "block": "minecraft:cracked_deepslate_tiles"},
    {"weight": 3, "block": "minecraft:air"},
])
ROOF_MAT = "minecraft:deepslate_tile_stairs"
