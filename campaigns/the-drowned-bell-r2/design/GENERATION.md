# The Drowned Bell r2 — prefab generation record

This campaign's prefabs are produced by the engine's prefab procedure
(`docs/reference/prefab-procedure.md` in the pipeline repo): scene description
first, palette by measurement, grammar program as JSON, machine gates at
expansion, render before believing, admission. The scene-type route table in
that document decides the back end; every zone below is a grammar zone.

## The programs are campaign files

`design/programs/z*.json` are the **artifacts of record** (ADR-0018: the IR is
the artifact; a zone belongs to its campaign, not to the engine's library).
Exported 2026-08-12 from the engine library `bell::` module at engine commit
`4be4a12` — the engine copies are slated for removal once this campaign's
pipeline consumes only these files. Vocabulary is inlined at export, so each
file is self-contained and expands via `delve-grammar expand --file`.

`programs/zones.json` says at what size and seed this campaign builds each of
them, and which optional gates each zone claims. Without it a program file
cannot be expanded at all — a grammar program fits any region, so nothing but
the campaign knows which one is this zone. It is a bijection with the directory:
a program file it does not name is a finding, and so is an entry naming a file
that is not there.

`delve-grammar audit --campaign-root <this repo>` expands every zone declared
here and runs every machine gate over it, stating what each gate examined. CI
runs it on every pull request and every push, and the pipeline repo runs the
same command against its pinned copy of this repo.

An expansion's provenance (program hash, region, seed) is recorded in the
metadata the expander writes beside every `.nbt`; the same inputs regenerate
the same bytes. The hash is taken over the **effective** program — parameters
and role overrides applied — so it identifies what was expanded rather than what
the file said before the command line touched it, and a zone whose shipped values
live in its own `params` needs no remembered flags to be reproduced.

**Seven of the eight zones pass every gate; Z3 does not.** `fluid-contained` reds
on the drowned ward with `DW0800`: 380 ways out of a 2304-cell body of water, so
the ward renders as still water in every tool here and runs on the first tick in
the world. It reproduces from Z3's program alone, in a corpus holding nothing
else, and it is a *design* answer — where the ward's water is walled and where it
is meant to spill — not a palette or a version matter.

## An oriented block state is a palette role, written in the scope's own frame

A connection, facing or rotation property names a direction, and a direction is
only meaningful against a frame. Written bare, a state is in the **world** frame
and a reorientation does not rewrite it — so a bar or a skull bound to a plain
role lands turned however the scope was turned, and the piece ships facing the
wrong way with every gate green. Wrapped as `{"local": …}` the state is in the
**scope's own** frame and is resolved into the world's at fill time, which is
what lets an orientation-dependent block stay a role a campaign can restyle
without knowing which way the piece was laid.

Every such role in this campaign is written that way, so no zone is held back by
it: all eight pass `oriented-fills`, five of them carry local roles, and the
audit totals **33** fills resolved out of a scope's own frame across those five.
Z1 is the worked case, and it shows why the frame is not decoration: the corpse
is authored as `rotation=8`, facing out of its own recess, and lands in the world
as `rotation=4`.

Two shapes the frame cannot resolve, and both are refusals rather than guesses: a
16-step `rotation` and a handedness are stated against a fixed vertical *and* a
fixed handedness, so under anything but a pure turn about the vertical they have
no image (`DW0738`); and a state written bare under a turned frame is refused
outright (`DW0736`).

## Zone status

One prefab per zone (owner decision, 2026-08-12 — no candidate sweeps until
the zone set is complete).

| Zone | Concept | Program | Status |
|---|---|---|---|
| Z0 barrow shore | `concept/z0-barrow-shore.jpg` | tidal-keep generator (pre-procedure; measured-palette pass 2026-08-11, engine PR #397) | owner-reviewed, accepted with the shoreline-edge correction applied |
| Z1 cliff road | `concept/z1-cliff-road.jpg` | `programs/z1-cliff-road.json` | **produced, awaiting owner review** — expands at 10x28x44; review set in `review/z1/` — see below |
| Z2 gate ward | `concept/z2-gatehouse.jpg` | `programs/z2-gate-ward.json` | **awaiting owner review** — expands at 20x10x84; interior review set in `review/z2/` (largest program: 101 rules) |
| Z3 drowned ward | `concept/z3-drowned-ward.jpg` | `programs/z3-drowned-ward.json` | program exported, unproduced |
| Z4 chapel ward | `concept/z4-chapel-ward.jpg` | `programs/z4-chapel-ward.json` | **produced, awaiting owner review** — expands at 27x12x33; the campaign's first zone with a spatial contract, so it is judged by 14 gates where the others carry 6; review set in `review/z4/` — see below |
| Z5 hall keep | `concept/z5-hall-keep.jpg` | `programs/z5-hall-keep.json` | program exported, unproduced |
| Z6 cistern deep | `concept/z6-cistern-deep.jpg` | `programs/z6-cistern-deep.json` | program exported, unproduced |
| Z7 bell tower | `concept/z7-bell-tower.jpg` | `programs/z7-bell-tower.json` | program exported, unproduced |

Zone order of production is by complexity, hardest first (owner decision,
2026-08-12): the most complex zone is produced and owner-reviewed before the
rest, so a workflow defect is found on the zone most likely to expose it.

## Z1 cliff road

**Scene** (fixed before any tool ran, per the procedure's §1): the player walks a
one-block ledge cut into a sea cliff, the rock wall close on the landward hand
and an open drop to the water on the seaward one, past shallow recesses in the
wall — some empty enough to stand back into, two holding the skull of somebody
who did not make the traverse.

**Expansion** — `delve-grammar expand --file design/programs/z1-cliff-road.json
--region 10x28x44 --seed 1 --traversable --reachable-floor`. Every gate passes
with a non-zero binding: `blocks-exist` 7, `shape-complete` 7, `states-complete`
7, `oriented-fills` 27, `non-empty` 12320, `traversable` 3, `reachable-floor` 6.
5490 filled cells, 7 distinct states, 50 standable cells all reachable on foot,
12 anchors, silhouette complexity 1.65. `delve-admit audit` passes over 12320
blocks (0 forbidden, 0 non-allowlisted, 0 unknown, 0 under-specified).

**Provenance** — program
`sha256:67c441bc329fdd1517740c8d6fe8c765ed885b9ee11f4f4e52672894a71ad2fb`, seed
1, region 10x28x44; re-expanding those inputs reproduces the `.nbt`, the metadata
and the report byte for byte. Both of this zone's tuned values — `fall` 12 and
`sea` 5, a drop that reads as lethal and a gulf wide enough to see down — live in
the program's own `params`, so the file plus the manifest row is the whole recipe.

**Artifacts** — `prefabs/z1-cliff-road.nbt` + `prefabs/z1-cliff-road.json`;
review shots and what each camera did in `design/review/z1/`.

**Palette** — measured, never named from memory. Material colours are patch means
over crops of the concept image, verified by looking at the crops drawn back onto
the image; candidates come from `tools/block-appearance.py --screen` over the
measured shelf, and the mixes were read as a swatch sheet before binding. The
near cliff measures as a near-neutral dark grey of very wide value range (mean
`#3f3e3a`, luminance p05 30 and p95 101 out of 255, saturation 6/255), which is a
*mix* rather than a block: bound to one block the wall reads as a flat panel that
no measurement of the mean would object to.

| Role | Mix | Measured | Concept sample |
|---|---|---|---|
| `crag` | `cobbled_deepslate` 50% · `smooth_basalt` 30% · `blackstone` 10% · `deepslate[axis=y]` 10% | `#49484d` | `#3f3e3a` near cliff face — the untouched sea-cliff mass below and behind the road |
| `path/rock` | `cobbled_deepslate` 60% · `deepslate[axis=y]` 20% · `tuff` 10% · `blackstone` 10% | `#4e4e50` | `#464742` the cut ledge and its wall — same rock, a shade lighter and drier where it is worked |
| `path/corpse` | `skeleton_skull[powered=false,rotation=8]` | — | the remains in the wall recesses |

`blackstone` is the loud member of both mixes and holds 10% of the area, which is
the craft rule the numbers serve; the near-black patches are the concept's deep
crevices. `deepslate[axis=y]` carries the vertical grain the cliff face is
striated with.

**Every role is written in the scope's own axis frame.** The palette's three
entries are `{"local": …}` paints, so each resolves its directions through the
scope that fills it: `deepslate`'s `axis` and the skull's `rotation` follow the
piece instead of the world. This is not decoration. The recesses are reached
through a `reorient` that names the across-path axis as local `Z`, so the corpse
is authored as `rotation=8` — facing out of its own recess — and the expander
writes `rotation=4` into the world. Written bare, the same value is the world's
own yaw: the skull would face along the road into the side wall of its recess,
and every gate would still be green. 27 of 27 orientation-carrying fills resolve
this way.

**Open against this piece**

- Lighting profile is `dark` (`DW0751`, min light 0 over the 4 roofed walkable
  cells). The road itself is open to the sky; the dark cells are the recesses,
  and no rule in this zone exposes a light-emitting role, so a lantern in a
  recess arrives as campaign-bound content on the declared anchors.
- **The ledge does not overhang, and the program cannot make it.** The concept's
  road projects from the cliff on a lip with the drop undercut beneath it; here
  the walking surface is flush with the rock below, so the seaward elevation is a
  flat plane with a seam. The one lever is `ledge_shelf`, which lays its course
  across the *whole* gulf width, so the lip's projection and the drop's width are
  the same number: `sea=3` gives 182 standable cells and `sea=5` gives 269,
  against 50 shipped, and `sea=2` is refused by `road_plan`'s own guard. A narrow
  lip over a wide drop is not expressible, and the zone ships at `ledge_shelf=0`
  — a one-block ledge, which is the exposure the scene is about.
- The concept's rusted iron stanchions and their chain rail have no role and no
  rule in this program. They are the element that reads the road as *made* rather
  than found, and adding them is design work this production did not do.
- The piece declares no spatial contract, so every contract obligation examined
  nothing and `traversable`'s binding counts standable cells on two region faces
  rather than declared ways in.
- Judge it from the eye shots. A cliff section is solid rock with a groove in it,
  so its exterior orbit cameras photograph a slab and cannot show the road at
  all; `review/z1/README.md` says which camera answers which question.

## Z4 chapel ward

**Scene** (fixed before any tool ran, per the procedure's §1): the player comes up
through the rock into the west range of a cloister whose roof is gone — arcades on
all four sides, sky over all of it, moss standing in the joints of the paving.
Fallen masonry is heaped along the west walk with bodies lying in it. The garth is
open ground with a collapsed canopy across its north-west corner; the two north
corners of the walk are down, so the ward cannot be crossed around whatever is
standing in it. Three chiselled plinths mark the stations of an hour-round. In the
paving there is a grate to look down through and a stair to go down by, and under
the whole garth is the hour-vault, behind a gate that opens from the crypt side.
The one intact door on the rock is in the south range, oak and iron-banded, with a
broken traceried bay beside it that the drowned ward is seen through. The way on is
north, up three steps to the terrace of the north range.

### The two documents that disagreed about this zone, and which one this piece follows

**Where Z4 sits in the delve.** `beats.md` places the chapel ward between the
drowned ward and the hall, entered from below and left upward; the production
record's earlier scene for this zone had the player drop out of the keep's kitchen
duct into it, and the earlier program was built that way — a duct descent, a
one-way fall, no way back. Beats 4.6 and 4.7 both need Emeric to arrive here after
the shortcut opens, which the reversed order cannot stage.

This piece follows **`beats.md`**, and the site plan and section in
`reference/` agree with it: Z4 is the cloister on the upper shelf at +9, entered
from the drowned ward's side, left north and up into the hall at +12, with the
banded door on its south side looking down over the ward and the gatehouse yard.
The document that was wrong is **this one** — the production record's own scene —
and the paragraph above replaces it. The zone has no duct, no fall and no
one-way descent; it is walked into and walked out of.

**The roof.** The earlier record called the roof "a decision, not an omission",
against a concept image of an open cloister. Measured against `beats.md` it was
five absent beats, because sky is what four of them are staged in. **There is no
roof.** Of 927 standable cells, 632 are open to the sky; the 295 that are
sheltered are the hour-vault, the crypt stair and the cells under the arcades'
own arch heads.

### The seven beats, and the rule that builds each

| # | beat | rule(s) that build it | anchors |
|---|---|---|---|
| 4.1 | a cloister with its roof gone: arcade on all four sides, sky above, grass in the paving | `ward_band` → `arcade_cross_row` / `garth_row` → `arcade_screen` → `arcade_pier_col` + `arcade_bay_col` → `arcade_bay_body` (4 bays a side, head narrowed to one cell); `paving_band` → `slab_floor` (`paving`, whose `moss_block` member is the growth in the joints) | `ward` |
| 4.2 | K4 the fallen: bodies among rubble piles, one of them not scenery | `west_walk_lane` → `heap_row` → `rubble_heap` → `heap_body` (three heaps of `rubble` and `collapse`, each carrying a `corpse`, each two of the walk's three cells wide so the walk is squeezed and not sealed) | `fallen-1`, `fallen-2`, `fallen-3` |
| 4.3 | the Two Sextons, fought where the ward cannot be crossed around them; the collapsed canopy | `garth_body` → `garth_centre_row` → `sexton_col` (the ground) + `garth_canopy_row` → `canopy_mass` → `canopy_body` (the fallen canopy, 5×5, as cover); `north_walk_row` → `corner_collapse` (both north corners of the round filled to head height, so the north range is reached only across the garth) | `sexton-1`, `sexton-2`, `canopy` |
| 4.4 | Sister Ide walks the cloister round with a hand-bell; the plinth is her turning-point | the round is the four walks and the garth's own perimeter (`west_walk_lane`, `north_walk_row`, `south_walk_row`, `arcade_cross_row`); `station_col_turn` → `plinth_cell_turn` → `plinth_body_turn` is the plinth she turns on | `plinth` |
| 4.5 | G2 the rite: three marked stations of her round; completing it opens the hour-vault below | `plinth_cell` / `plinth_cell_turn` → `plinth_body` (three plinths, and the only chiselled stone in the zone); `undercroft_band` → `vault_core` → `hour_wall` → `hour_run` → `hour_niche_col` (seven recesses), `vault_hall` → `vault_room` → `vault_air` → `vault_pier_row`; reached by `crypt_flight` → `crypt_treads` and shut by `vault_gate`; seen before it is earned through `slab_oculus_row`'s grate | `station-1..3`, `hour-1..7`, `vault-gate`, `crypt-head` |
| 4.6 | S3 the banded door — oak, iron-banded, ring handle, barred on the chapel side; the ward visible below through the arcade gap | `south_wall` → `banded_door` → `door_leaf` (two leaves, four states, in an arch with a transom); `stoop_row` → `stoop_cell` is the sill beyond it; `arcade_gap_wall` is the broken bay beside it and the tracery left in it | `gate`, `stoop` |
| 4.7 | Emeric comes this far and no further; he sets the lamp on the chapel step | `slab_step_row` lays the step's own flag in front of the door; `south_walk_row` → `chapel_step_lane` → `chapel_step_body` declares the cell he stands on | `lamp-step` |

**7 of 7 built.** Every beat has a named rule and the anchors a campaign binds to.
What each shot in `review/z4/` answers is in that directory's README.

**Expansion** — `delve-grammar expand --file design/programs/z4-chapel-ward.json
--region 27x12x33 --seed 1`. **Fourteen gates, every one passing with a non-zero
binding**: `blocks-exist` 24, `shape-complete` 24, `states-complete` 24,
`oriented-fills` 258, `non-empty` 10692, `contract-well-formed` 18,
`contract-coverage` 927, `contract-closure` 2750, `contract-edge-proof` 5,
`contract-no-body` 3, `contract-reachability` 887, `contract-anchors` 26,
`contract-exterior-faces` 3, `contract-no-body-majority` 927. 5191 filled cells,
24 distinct states, 927 standable, 26 anchors, silhouette complexity 1.02.
`delve-admit audit` passes over the whole model (0 forbidden, 0 non-allowlisted,
0 unknown, 0 under-specified).

**The zone declares a spatial contract, and that is what it is judged by.** Six
spaces (`garth`, `walk`, `terrace`, `stoop`, `crypt-foot`, `vault`), three
out-of-walk regions (`rubble`, `canopy`, `stations`, every one earning `posted`
from the anchors in it) and nine edges. The contract proves what a face-count
cannot: that the arcade's openings are the only way between the walk and the
garth, that the crypt stair really descends four and connects through its own
treads, that both bars bar — the reachability walk names them, `space stoop:
door-leaf` and `space vault: vault-door` — and that every one of the 26 anchors
lands somewhere the contract classifies.

**Why the zone claims neither `traversable` nor `reachable-floor`.** Both were
tried and both are the wrong claim for this piece, for one reason each, and the
contract gate that replaces them is stronger than either. `traversable` requires a
walk between **every pair** of declared exterior traversal edges; S3 ships barred,
so the sill beyond it is severed from the way in by construction, and the gate can
neither be told about a bar nor pass with one standing. `contract-reachability`
is the gate that can: it walks from the entry through declared edges only, then
re-walks with bars opened and names the spaces that needed it.
`reachable-floor` turns "every roofed floor is walkable to" into a verdict, and
the hour-vault's floor is deliberately not walkable to until the rite is done.
Both facts are in the always-on reachability line rather than hidden: 698 of 927
standable cells are reachable on foot with the bars standing, and the 227
sheltered cells it cannot reach are one pocket, `x 2..24 y 1..1 z 7..17`, which is
the hour-vault.

**Provenance** — program
`sha256:67b2323217aba1008904c7bcf1b3c5c0f7f30c9d776139ed661eb71c8719bd59`, seed 1,
region 27x12x33. Reproduction was checked from a **second instrument sharing no
working directory and no build tree with the first**: a separate checkout of the
pinned engine, built on its own, run from a different directory and writing to a
different one. The two `.nbt` files hash alike —
`12526f1306c0e8b2796ad4799071df7b7df211ffaf8414eb06a93ed2270d6c33`, taken over
**stdin**, so no path enters the digest — and the cross-check does not hash at
all: both files were parsed and compared cell by cell, 10692 of 10692 identical,
with the metadata and the report equal object for object.

**Artifacts** — `prefabs/z4-chapel-ward.nbt` + `prefabs/z4-chapel-ward.json`;
review shots and what each camera answers in `design/review/z4/`.

**Palette** — measured from the concept image, never named from memory. Material
colours are patch means over crops, and the crops were drawn back onto the image
and looked at before any of them was used. The near stone of the concept has a
very wide value range (the lit pier and voussoir measure `#5f6362` with luminance
running 32 to 184 out of 255), which is a *mix* rather than a block: bound to one
block the ward reads as a flat panel that no measurement of the mean would object
to.

| Role | Mix | Measured | Concept sample |
|---|---|---|---|
| `arcade` | `tuff_bricks` 55% · `polished_tuff` 25% · `mossy_stone_bricks` 10% · `cobbled_deepslate` 10% | `#61665f` | `#5f6362` lit pier and voussoir |
| `wall` | `deepslate_bricks` 30% · `cobbled_deepslate` 25% · `tuff_bricks` 20% · `polished_deepslate` 15% · `mossy_stone_bricks` 10% | `#525452` | `#4c5147` / `#424844` range-wall ashlar, lit and shaded |
| `paving` | `tuff` 30% · `cracked_stone_bricks` 25% · `cobbled_deepslate` 25% · `mossy_stone_bricks` 12% · `moss_block` 8% | `#676b60` | `#687375` the flagstones, and `#353733` the growth in their joints |
| `crest` | `tuff_bricks` 30% · `cobbled_deepslate` 20% · `mossy_stone_bricks` 10% · **air 40%** | `#464747` | the broken roofline over every wall and pier |
| `rubble` | `cobbled_deepslate` 30% · `cracked_deepslate_tiles` 20% · `chiseled_deepslate` 10% · `tuff_bricks` 10% · **air 30%** | `#464747` | `#323536` the heaps along the left arcade |
| `collapse` | `cobbled_deepslate` 40% · `cracked_deepslate_tiles` 25% · `tuff_bricks` 25% · `mossy_stone_bricks` 10% | `#515350` | the same fall where it has to stop a body, so no air member |
| `vault_stone` | `polished_tuff` 50% · `tuff_bricks` 30% · `cobbled_deepslate` 20% | `#5e625e` | the undercroft: the ward's stone, plainer |
| `timber` | `dark_oak_wood` 50% · `dark_oak_log` 25% · `muddy_mangrove_roots` 15% · **air 10%** | `#3f311d` | `#17191c` the collapsed canopy at the back left |
| `plinth` | `chiseled_tuff` | `#5b6059` | the standing plinth at the left of the ward |
| `bedrock` | `deepslate[axis=y]` | `#545456` | inert mass, no player-visible face |
| `corpse` | `skeleton_skull` | `#513e33` | what is lying in the heaps |
| `grate`, `tracery`, `vault_bar` | `iron_bars` | `#898b88` | the grate over the oculus, the tracery in the broken bay, the hour-vault's gate |
| `door_low_a/b`, `door_high_a/b` | `dark_oak_door` | `#493118` | the closed iron-banded double door with the ring handle |

The loudest member of every stone mix holds 10% of the area or less
(`mossy_stone_bricks` in three of them, `moss_block` at 8% in the paving), which
is the craft rule the numbers serve. `timber` is the exception and is stated
rather than hidden: it is 75% chromatic area, because dark oak is, and it is 50
cells of the 5191.

**The palette tool reports a binding that is not the whole palette, and the number
it prints reads as a pass.** `block-appearance.py --program` over this file says
*"binding: 8 paint(s) examined"*. The program declares **18** roles. The ten it
did not see are exactly the ten written in the scope's own axis frame: a `local`
paint is skipped in silence and does not appear in the count, so a palette that
is mostly oriented roles is reported as fully measured. Handing the same ten to
`--mix` does not recover them either — the flag splits its argument on `=`, so a
block state with a property in it is refused (`'y]=1' is not a weight`). **The real
binding for the table above is 18 of 18 roles**: eight through `--program`, and
ten through `--mix` with the state's properties stripped, which measures the
block's own texture and is the right number for a colour anyway. Both halves are
stated here so the shortfall is not carried forward as a pass.

**Every orientation-carrying role is written in the scope's own axis frame, and
this region cannot decide whether that mattered.** `oriented-fills` reports 258
fills examined, 20 carrying block-state properties, and **20 of those 20 resolved
out of the scope's own frame** — there is no world-frame literal left for the gate
to bite on. That is the strongest form of the claim, and it is worth being plain
about why it was worth making here: the zone's outermost frame is the identity,
and a world-frame literal under the identity frame is licensed by the gate and
lands correctly. A green on that branch would have proved nothing about this
palette. What does prove something is the arcade: the north and south screens are
the same rule as the east and west ones under a `z: world_x` transposition, and
every state inside them resolves through it.

**How much of this is mass nobody touches.** Measured by rebinding each role in
turn to a marker block and counting the marker, which is the only way to ask the
question — one block serves several roles, so a block census cannot answer it. The
measurement variant has the contract and its claims stripped so a rebind that
changes passability cannot be refused by a contract gate, and the run asserts what
that costs: **10692 of 10692 cells identical to the shipped model**, because a
claim writes no blocks.

| what | cells | of the region | of the filled blocks |
|---|---|---|---|
| `bedrock` — the role that exists only as mass | 2148 | 20.1% | 41.4% |
| stone with no air beside it and no outer face — mass nothing can look at | 1742 | 16.3% | 33.6% |
| everything else | 3449 | 32.3% | 66.4% |

The 2148 was taken twice by unrelated means: by counting the marker in a rebind
expansion, and by adding up the layout's own bands on paper. Both give 2148. The
1742 reconciles the other way: summed per role from the marker runs it is 1742, and
scanned cell by cell over the shipped model for stone with no air neighbour it is
also 1742.

**Open against this piece**

- **The hour-vault is a room and not yet a reason.** Seven recesses, two pier
  ranks and a gate the rite opens — the geometry G2 needs — but what is *in* the
  recesses is campaign-bound content that does not exist yet. Until it does, the
  optional gate leads to an empty undercroft.
- **The zone has no light-emitting role and does not need one above ground.** The
  ward is roofless, so 632 of its 927 standable cells are open to the sky and it
  is the first zone of this campaign that is lit at all. The hour-vault is not:
  its only daylight is the oculus grate over the middle of it, and whether that
  is enough is a measurement `delve-admit lighting --write` takes, not something
  expansion can know.
- **A sightline through tracery cannot be declared, only built.** Beat 4.6 wants
  the drowned ward visible through the broken bay. It is: the bay's opening
  carries iron-bar tracery, which a body cannot pass and an eye can. The contract
  cannot say so — an `exterior` opening must be cells the air outside the piece
  reaches, so a `vision` edge over the tracery is refused, and a `vision` edge
  over an air opening would be an opening a body walks out of. The zone chose the
  geometry that is right and left the claim unstated; nothing downstream knows the
  bay is a window rather than a wall.
- **A cloister's own image asks for scatter the walk model treats as a wall.**
  The growth in the paving joints is `moss_block` set into the flags rather than
  the concept's tufts standing proud of them, because the navigation predicate
  admits only air and skulls: a `short_grass` on a walked floor is read as a
  barrier, and the contract's coverage and reachability gates would red over a
  floor a player can in fact cross. The same rule keeps every torch, lantern and
  candle off the ground.
- **Two of the three station plinths cannot be climbed, and that is the plinth
  being a plinth**; the reachability measurement reports them as two cells of
  unreachable floor open to the sky, which is a number and not a finding.
- **The corner collapse is the pinch, and a player who breaks it breaks the
  fight.** Beat 4.3's "the ward cannot be crossed around them" is built as two
  head-high fills of `collapse` in the north corners of the walk. In adventure
  mode nothing can mine them; in any other mode the pinch is a two-block dig.
