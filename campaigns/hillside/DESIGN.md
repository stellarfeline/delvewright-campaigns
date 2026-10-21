# Saltstair — the hillside town built two ways

**What this is for: one hillside town, built twice from this one brief, to see which cut reads better** — the stepping of the levels, the joins between buildings, and how the town meets the ground. Variant **A** (`campaigns/hillside-a`) gives every building and every connector its own site-plan box. Variant **B** (`campaigns/hillside-b`) cuts the town into two boxes, an upper town and a lower town, and each box's one program draws everything inside it. Both are built from this file, the same heightmap (`terrain/peninsula.png`), the same reference image (`design/reference/view1-from-the-sea.jpg`), the same engine revision and the same judging set (§6). Everything in §4 is in world coordinates and is the authority on size and position; the image is the authority on look alone.

A short showcase: 1–4 players, 10 minutes, no combat. The party arrives on the square at the top of the town and walks the main street down to the quay. One quest, one objective (reach the quay); a cast is optional and identical in both variants if either has one.

## 1. The fiction

Saltstair is a fishing town on the seaward end of a long green peninsula. One street climbs from the quay to a square at the top, in five terraces, each a flight of stone steps above the last; the houses stand on the terraces, so from the sea their roofs step up the hill like the street does. The name is what the fishermen call the street. Nothing here is hostile; the town is at its afternoon work.

## 2. The peninsula (the owner's method)

All land is an island. The world's horizon is `ocean` (sea level y 62) with a `boundary` of margin 8. The island is one `fill: open` heightmap over the whole region; the town stands on its seaward (south) end, and the rest of the island — the mainland, green hills running north — is never played: a body that walks onto it is returned by the boundary clock, and so is a body that swims out past the quay.

Where the boundary falls is a derived fact, not a declaration: the engine inflates the union of the plan's **placed pieces** — every box's shell and every `volumes[]` entry — by `margin`; the fill is laid into the region's mass and is not a placed piece, so **the island beyond the boxes is outside the boundary** (`crates/delvec/src/compiler/emit/boundary.rs`, `playable_region`, over `plan.areas`, whose pieces the blockout lists in `crates/delvec/src/compiler/blockout.rs`). Measured on the feasibility fixtures of §7, which carry the numbers.

| Fact | Value |
|---|---|
| Region | min `[0, 40, 0]`, extent `[144, 96, 224]`; x runs east, z runs south; north is the land side |
| Heightmap | `terrain/peninsula.png`, 144 × 224, `base_y` 48, `range` 51 — surface `48 + value / 5`, written by `terrain/peninsula.py` from the tables below; `terrain/peninsula.txt` is a contour picture of it |
| Land | surface ≥ 62: 17 350 columns, x 10..138, z 7..204; the shore is the 62-contour |
| Heights | sea bed 54 at the rim; the town 63..83 (surface); the mainland's hills 76, 76 and 84 (surface), at (48, 76), (98, 70) and (72, 52) |
| Ground | the upper envelope of pads and hills falling half a block a column: no two open-ground columns differ by more than one block, and the surface has no pit (`terrain/heightfield.py`) |
| Fill | `surface` grass, `below` dirt |
| Harbour | the harbour floor in front of the quay wall is 60 (two blocks of water against the wall); a beach at 62 (walk plane 63) west of the quay, x 50..56, z 194..203, is where a swimmer climbs out |
| Sea | surface 61 and under is water; the nav model refuses water (spec-0038): no route touches it, and the sea is scenery the boundary returns a body from |

## 3. The town in words

The **main street** runs due south down the hill, six blocks wide, from the square at the top (walk plane 84) to the quay (64): a fall of 20 over 104 blocks of street, in five flat terraces four blocks apart, each joined to the next by a flight of four steps. Each flight is its own place (a stair box, six wide and six long, whose floor is the lower terrace and whose treads rise to the upper at its north end); each terrace is a flat street segment. The **quay** is a straight stone wall 32 wide at the water, walk plane 64, with the sea two blocks deep against it; the beach is west of it.

**Eight buildings**, four each side, every one on its own terrace with its door at grade on the street:

| # | Building | Side | Terrace | Use | Door |
|---|---|---|---|---|---|
| 1 | The chapel | west of the square | 84 | a small stone chapel with a short tower; the first thing seen from the square | east, onto the square |
| 2 | The inn | east of the square | 84 | the Lantern: a wide timber-framed inn, lit windows | west, onto the square |
| 3 | The smithy | west | 80 | a forge with a chimney, open-fronted toward the street | east |
| 4 | The weaver's house | east | 80 | a narrow house, cloth on the upper floor | west |
| 5 | The merchant's house | west | 76 | the tallest house, a steep roof, a counting room | east |
| 6 | The rope walk | east | 72 | a long low shed open along its street side | west |
| 7 | The harbourmaster's house | west | 68 | a narrow house with a lamp in its gable | east |
| 8 | The warehouse | east end of the quay | 64 | a long stone store with a slate roof, doors onto the quay | south, onto the quay |

**Materials** (one hand across the town; the reference image is the colour authority): walls — stone bricks and cobblestone ground floors, spruce timber framing with white (calcite or quartz) infill above; roofs — deepslate tiles (slate) on the chapel, inn, merchant's house and warehouse, dark oak stairs (shingles) on the rest, every roof with one block of eaves; street — cobblestone paving with stone-brick kerbs and stone-brick stairs at the flights; retaining walls between terraces — stone bricks with mossy courses at the foot; quay — stone bricks and polished andesite with spruce-log bollards; light — lanterns on the street's kerb posts at every flight and at every door, windows lit from inside. Roof courses are chosen against `docs/reference/roof-and-facade-craft.md` §2 and §4 (45° stairs over a span `W`: `⌈(W − 1) / 2⌉` courses).

**Light is placed with the place** (the owner's rulings, as the planner hands them): every street segment and flight carries kerb lanterns, every house its door lantern and lit windows; the engine only checks the result, on the whole world and on each region (`DW0210`), never on a piece. **How the town meets the ground**: every terrace stands above the next behind a retaining wall the place draws; the hillside beside the street is the heightmap, stepped turf; a house's downhill wall stands on the heightmap's ring and the house's floor is level with its street.

## 4. The design brief: geometric facts

Interior footprints `x0..x1 × z0..z1` inclusive, world coordinates; a box's play space. Heights are walk planes (the surface block is one under). `terrain/peninsula.py`'s `TOWN` table is this table; the heightmap puts a flat pad at walk plane − 1 under every footprint and its one-cell ring (the higher pad wins a shared ring column).

### 4.1 The street

| Place | x | z | Walk plane | Kind | Headroom |
|---|---|---|---|---|---|
| the square | 65..82 (18) | 96..109 (14) | 84 | way | open 6 |
| flight 1 | 71..76 (6) | 111..116 (6) | 80, treads up to 84 at its north end | stair | open 8 |
| upper street | 71..76 | 118..129 (12) | 80 | way | open 6 |
| flight 2 | 71..76 | 131..136 | 76, treads up to 80 | stair | open 8 |
| middle street | 71..76 | 138..149 (12) | 76 | way | open 6 |
| flight 3 | 71..76 | 151..156 | 72, treads up to 76 | stair | open 8 |
| lower street | 71..76 | 158..169 (12) | 72 | way | open 6 |
| flight 4 | 71..76 | 171..176 | 68, treads up to 72 | stair | open 8 |
| shore street | 71..76 | 178..185 (8) | 68 | way | open 6 |
| flight 5 | 71..76 | 187..192 | 64, treads up to 68 | stair | open 8 |
| the quay | 58..89 (32) | 194..200 (7) | 64 | way | open 6 |

The street's centre line is x 73–74. The ring between two consecutive street places is one cell (z 110, 117, 130, 137, 150, 157, 170, 177, 186, 193).

### 4.2 The buildings

| # | Place | x | z | Floor | Clearance | Roof (courses, eaves) | Door face, cell |
|---|---|---|---|---|---|---|---|
| 1 | chapel | 54..63 (10) | 98..106 (9) | 84 | 6 | 6, 1 | east, z 102 |
| 2 | inn | 84..94 (11) | 97..107 (11) | 84 | 4 | 6, 1 | west, z 102 |
| 3 | smithy | 62..69 (8) | 119..126 (8) | 80 | 4 | 4, 1 | east, z 122 |
| 4 | weaver | 78..84 (7) | 118..128 (11) | 80 | 4 | 5, 1 | west, z 123 |
| 5 | merchant | 60..69 (10) | 139..148 (10) | 76 | 5 | 5, 1 | east, z 143 |
| 6 | ropewalk | 78..84 (7) | 158..169 (12) | 72 | 4 | 4, 1 | west, z 163 |
| 7 | harbourmaster | 62..69 (8) | 177..184 (8) | 68 | 4 | 4, 1 | east, z 180 |
| 8 | warehouse | 80..89 (10) | 182..192 (11) | 64 | 5 | 5, 1 | south, x 84 |

Every house stands one cell from its street (the shared cell is the house's facade: spec-0098 §2 rule 3b), and its door is a standard `door` (1 × 2) centred on its street face. Floors take six distinct values over the nineteen places: 84, 80, 76, 72, 68, 64.

### 4.3 Terrain under and around

Pads at walk plane − 1 under every place and its ring; between pads the ground falls half a block a column, so the hillside beside each flight steps the way the flight does, and a house's uphill ring stands on ground up to one block above its floor course and its downhill ring on ground at its floor course. The terrain inside a stair box rises from its floor course at its south end to the upper terrace at its north (the cones from the pad above), which is the ramp its treads climb. Outside the town the island falls at the same half-block grade to the shore on every side and climbs to the hills in the north. In A that half-block hillside is the commons and no contract reads it; in B the part of it inside a box is the piece's, and §5.2 says what the piece owes for it.

### 4.4 Heights at a glance

| Thing | y |
|---|---|
| sea | water top 62; harbour floor 60; beach 62 (walk 63) |
| quay, warehouse floor | 64 |
| shore street, harbourmaster floor | 68 |
| lower street, ropewalk floor | 72 |
| middle street, merchant floor | 76 |
| upper street, smithy and weaver floors | 80 |
| square, chapel and inn floors | 84 |
| inn roof ridge | 84 + 4 + 6 = 94 (the town's highest roof); chapel ridge 84 + 6 + 6 = 96 |
| mainland hills | 77, 77, 85 (walk planes) |

## 5. The two cuts, as site plans

Both plans share the region, the fill, the datums (`datum/square` 84, `datum/upper` 80, `datum/middle` 76, `datum/lower` 72, `datum/shore` 68, `datum/quay` 64), the identities (the region's span and depth; the six datums) and the views (§6's cameras as `views[]`). `world.json` in both: `horizon: "ocean"`, `boundary: {margin: 8}`, `time` late afternoon, `weather` clear. The entry is the square (A: `node/square`; B: `node/upper-town`), the goal the quay (A: `node/quay`; B: `node/lower-town`).

### 5.1 Variant A — one box per building and per connector

Nineteen boxes, the nineteen rows of §4.1 and §4.2, each with the extent, floor and headroom its row states; the square is pinned at `min: [65, 96]` and every other box is placed by its seam. Eighteen seams:

| Seam | a → b | Class | Face of a | `at` / `meets` | Opening or contact | `stair_in` |
|---|---|---|---|---|---|---|
| square → flight 1 | stair | south | 6 / 0 | `{width: 6, height: 4}` | flight 1 |
| flight 1 → upper street | walk | south | 0 / 0 | contact (whole face) | — |
| upper street → flight 2 | stair | south | 0 / 0 | `{width: 6, height: 4}` | flight 2 |
| flight 2 → middle street | walk | south | 0 / 0 | contact | — |
| middle street → flight 3 | stair | south | 0 / 0 | `{6, 4}` | flight 3 |
| flight 3 → lower street | walk | south | 0 / 0 | contact | — |
| lower street → flight 4 | stair | south | 0 / 0 | `{6, 4}` | flight 4 |
| flight 4 → shore street | walk | south | 0 / 0 | contact | — |
| shore street → flight 5 | stair | south | 0 / 0 | `{6, 4}` | flight 5 |
| flight 5 → quay | walk | south | 0 / 13 | contact | — |
| square → chapel | walk | west | 6 / 4 | `door` | — |
| square → inn | walk | east | 6 / 5 | `door` | — |
| upper street → smithy | walk | west | 4 / 3 | `door` | — |
| upper street → weaver | walk | east | 5 / 5 | `door` | — |
| middle street → merchant | walk | west | 5 / 4 | `door` | — |
| lower street → ropewalk | walk | east | 5 / 5 | `door` | — |
| shore street → harbourmaster | walk | west | 2 / 3 | `door` | — |
| quay → warehouse | walk | north | 26 / 4 | `door` | — |

Every seam's `form` names the thing: "the first flight: six wide, four up to the square, treads on the flight", "the chapel's east door onto the square". The layout graph has nineteen nodes and eighteen traversal edges; the critical path is the eleven street places from the square to the quay. The ground outside every box is the heightmap. Nineteen pieces at step 9, one program each (a flight's program draws its treads, its kerb walls and lanterns; a street's its paving, kerbs, retaining wall and lanterns; a house its whole outside and inside).

### 5.2 Variant B — two boxes, one seam

| Box | x | z | Floor | Headroom | Holds |
|---|---|---|---|---|---|
| `node/upper-town` | 54..94 (41) | 96..149 (54) | 76 (`datum/middle`, its south end) | open 20 (top 96, over the chapel's ridge) | the square, flights 1 and 2, the upper and middle streets, the chapel, the inn, the smithy, the weaver's and the merchant's houses |
| `node/lower-town` | 54..94 | 151..200 (50) | 64 (`datum/quay`, its south end) | open 14 (top 78, over the harbourmaster's ridge) | flights 3, 4 and 5, the lower and shore streets, the quay, the rope walk, the harbourmaster's house, the warehouse |

One seam: `upper-town → lower-town`, class `stair`, face south, `at` 17 / `meets` 17 (x 71..76), opening `{width: 6, height: 2}`, `stair_in: node/lower-town`, form "the main street: the lower town's street climbs twelve to the middle terrace, in three flights, and passes through the terrace parapet at grade". The seam's plane is z 150, which in A is the ring between the middle street and flight 3; the sill is 76. **The face the two boxes share — the overlap of their two play spaces, in x and in y — must be wall wherever the opening is not** (`DW0836` names every open cell of it, measured on the fixture of §7), and that face is the full 41 columns wide and, with the lower town's top at 77, two courses high (76..77), so B owes a parapet across the town at z 150 — two courses, a body's height, on the middle terrace's edge, with the street's six-wide, two-high gap in it. The lower town's headroom is chosen so the shared face is exactly that parapet. The layout graph has two nodes and one edge; the critical path is `upper-town, lower-town`. Within B a building is not a box: each program draws its own slope surface from the same heightmap function (`terrain/peninsula.py`'s tables), so its edge meets the fixed ring within a block; then the street, its flights, the retaining walls, the kerb lanterns and the houses, inside the box's play space. Two pieces at step 9. Two beats: the quest's objective sits in `node/lower-town`; a cast, if any, stands by station anchors the two nodes declare.

What B needs from the engine that A does not: nothing on `origin/main` — its box is a cuboid whose play space the piece fills freely (spec-0098 §2, §14 correction 3), terrain above the floor inside the footprint is the piece's to draw, the ring is fixed by the whole and the crack check judges the join (§2c). What B's programs owe that A's do not: **a piece's space is one floor** (at most two consecutive levels; `contract-well-formed`, spec-0098 departure 33), so every terrace is a space of its own, every flight a `stair` edge whose via is its treads, and every standable cell of the hillside inside the box is either the via of a stair edge between two terraces or is fenced off and declared `no_body` — a 0.5 slope that a body can walk is not a space (the fixture of §7 was refused with "7 levels" on its first shape). The Treehouse Camp's bridges climb the same way, a deck space, a landing space and a flight between. spec-0106's `base: {"owned": n}` (unmerged) would let B's pieces own their ring and bottom course too; B does not need it, and does not use it.

## 6. The judging set — fixed before either is built

**Cameras** (the same world coordinates in both; `design/cameras.json` in each variant, one row per view; rendered with Lumenwright after the machine ladder is green). `eye` and `look_at` in world coordinates; fov 70 unless stated.

| Id | Eye | Look at | What it judges |
|---|---|---|---|
| `view/from-the-sea` | `[73.5, 66.5, 232.5]` | `[73.5, 80, 150]` | the whole town from the water: the stepping of the roofs, the quay wall, the hill behind |
| `view/down-the-street` | `[73.5, 85.6, 97.5]` | `[73.5, 66, 200]` | the street from the square to the sea: the flights, the kerbs, the houses' facades |
| `view/up-the-street` | `[73.5, 65.6, 199.5]` | `[73.5, 84, 100]` | the street from the quay: how each terrace meets the next |
| `view/the-first-flight` | `[68.5, 81.6, 120.5]` | `[73.5, 83, 112]` | one join at eye height: flight 1 between the upper street and the square, with the smithy's corner |
| `view/the-merchants-terrace` | `[48.5, 80.6, 143.5]` | `[73.5, 76, 143.5]` | from the hillside west: how a house and its terrace meet the ground |
| `view/from-the-south-east` | `[120, 110, 215]` | `[74, 76, 150]` | the oblique whole, roofs and terraces |

**The walk**: spawn on the square; the critical path is the main street from the square to the quay; the bot's run is that walk (the objective completes on the quay). The owner's walk is the same, then back up, then off the street onto the hillside between two houses and down to the beach.

**The numbers**, each measured the same way on both builds, in each variant's `GENERATION.md`:

| Number | How it is measured |
|---|---|
| distinct floor levels | the number of distinct `y` of the standable cells on the street's centre line (x 73 and 74) from z 96 to z 200, read from the server-saved world of the build with `tools/lib/anvil.py` (the engine's own reader); A's expected 6 datums plus the flights' treads |
| ring cells where a box's ground and the outside terrain differ | for every box, the plot-edge columns the stage-5 battery examines (`blockout battery binding: … plot-edge column(s) examined, … crack(s)`), and beside it the count of those columns where the standable surface inside differs from the ring's terrain by more than one block (a faced edge), read from the same saved world |
| refusals per code | every `DW` code `delvec` printed during authoring, counted per code from the `GENERATION.md` log |
| author tokens and time | the round's token count and wall-clock from the task record, per variant |
| build and bot status | `delvec build` exit, PackTest, the bot's critical path (`validation/bot-run.sh`), the staging gate |

## 7. Feasibility, proven by building (phase 1)

Two small fixtures on the same heightfield module, built on engine `da769d0ed4499caed7bcd0c69dc12f476586ce82` (`origin/main`), `delvec 1.13.0, dsl 0.55.0`: `campaigns/hillside-feas-a` (two roofed houses four apart joined through a way box that hosts the treads) and `campaigns/hillside-feas-b` (one sky-open box whose piece draws a sloping street above its floor and meets the heightmap at its ring, over a stair seam to a landing). Each fixture's `GENERATION.md` carries its exit statuses, refusals and where the boundary fell.
