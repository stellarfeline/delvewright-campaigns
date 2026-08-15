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

**All eight zones pass every gate.** The drowned ward's `fluid-contained` red
(`DW0800`: 380 ways out of a 2304-cell body of water) was the design answer it
looked like, and §Z3 below records what that answer turned out to be: the ward's
water is walled at every internal boundary and open only where it leaves the
piece, because it is the sea rather than a pool. The zone now binds 3728 fluid
cells with nothing open beside or below any of them.

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
audit totals **149** fills resolved out of a scope's own frame across those five.
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
| Z3 drowned ward | `concept/z3-drowned-ward.jpg` | `programs/z3-drowned-ward.json` | **produced, awaiting owner review** — expands at 40x10x60 and ships as 2 tiles; review set in `review/z3/` — see below |
| Z4 chapel ward | `concept/z4-chapel-ward.jpg` | `programs/z4-chapel-ward.json` | **produced, awaiting owner review** — see below |
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

## Z3 drowned ward

**Scene** (fixed before any tool ran, per the procedure's §1): the player comes
out of the gate onto a raised stone spine crossing a ward whose floor is under
the sea, two arcades standing in the water either side of it, heaped weed
narrowing the walk at two points, sunken boats out in the water off the left,
and at the far end a water-gate tower on its own base whose ground door is
barred from the inside — so the way in is up a fallen bay onto the arcade, along
it at shutter height, and down through the tower.

**The tide decides everything here** (`tide.md`). One plane, whole-world, and
this zone's water is a piece of it: no bounded basin, no air pocket under the
plane, no flowing water. The program is written so that below the waterline
every cell is either water or stone — there is no third case in any rule — and
the causeway's mass rises through the water rather than being a lane cut into
it. That is the whole of the answer, and it is why the spine is walkable at the
standing tide and the ward is not.

**Expansion** — `delve-grammar expand --file design/programs/z3-drowned-ward.json
--region 40x10x60 --seed 1 --traversable`. Every gate passes with a non-zero
binding: `blocks-exist` 20, `shape-complete` 20, `states-complete` 20,
`oriented-fills` 296, `non-empty` 24000, `traversable` 72 (32 standable cells at
the approach face, 40 at the exit face). 9036 filled cells of 24000, 20 distinct
states, 2695 standable, 28 anchors, silhouette complexity 1.02. `delve-admit
audit` passes over 24000 blocks (0 forbidden, 0 non-allowlisted, 0 unknown, 0
under-specified). The zone is past the 48-per-axis cap, so it ships as 2 tiles
and one manifest, and has no lighting step: the profile is `unmeasured`.

**The water, and the instrument that established it.** The recorded `DW0800`
red was real and reproduces exactly. `fluid-contained` is newer than the pinned
engine the campaign audit runs, so at that pin the zone reported passing and the
red could not be reproduced by the campaign's own gate — a green that proves
nothing rather than a refutation. Three independent methods agree on the same
number: read off the old program's rules by hand (252 cells beside the causeway
lane, which was an air trench cut through the water, plus 128 beside the guard
station), an independent reader over the shipped `.nbt`, and the gate itself on
a later engine. All three say 380 ways out of 2304.

Against the zone as built, the same three say: **3728 fluid cells, every one a
source, none with an open cell beside or below it, and 0 internal escapes.** 344
run directions leave the piece's own outer faces and are counted rather than
judged — what is beyond a face is not in these bytes, and here what is beyond
them is the sea. The old program also held 3519 air cells under its own water
plane; this one holds none, which is `tide.md`'s rule stated as a property of
the blocks.

**Provenance** — program
`sha256:14cc79961cfd27811f2013a0ea467674db848432eeadb5784b76b80f76a77aee`, seed
1, region 40x10x60; re-expanding those inputs reproduces all four files byte for
byte. Verified twice over, by `cmp` and by sha256 taken over each file's
**content** alone — hashing a listing of `shasum` output would have hashed the
output directory's name along with the bytes and called two identical runs
different. A third build tree at a later engine reproduces both `.nbt` and the
metadata identically; only the gate report differs, because that engine runs two
gates more.

**Artifacts** — `prefabs/z3-drowned-ward.json` (the manifest, and the only file
that describes the zone) + `prefabs/z3-drowned-ward.x0y0z0.nbt` and
`.x0y0z1.nbt`; review shots and what each camera did in `design/review/z3/`.

**Every beat owes a rule**, and every beat has one:

| Beat | The rules that build it |
|---|---|
| 3.1 the ward, the arcades, the spine above the water | `lower_ward_plan` places two `arcade_run`s either side of the spine; `open_water`; `causeway_run` + `causeway_mass` carry the deck one course clear of the water top; `kerb_column`. `anchor/causeway-head` |
| 3.2 waders in the flooded ward, slow to climb the spine | `flat_run` + `wader_post` (12 `anchor/wader-*`); the causeway's four-course rise out of the seabed is what they cannot climb quickly |
| 3.3 weed heaped at two points on the causeway | `lane_run`, `weed_pinch`, `weed_pinch_far` (the same rule handed its own reflection), `weed_heap`. `anchor/weed-pinch-1`, `-2` |
| 3.4 the wrecks off the causeway's left | `wreck_reach`, `wreck_hull`, `hull_section` — three hulls flooded to the gunwale. `anchor/wreck-1..3` |
| 3.5 the water-gate tower, barred from the causeway side | `water_tower`, `tower_plinth` / `plinth_mass` / `plinth_water` (the base standing in the sea, the storey oversailing it), `tower_face` (the shuttered windows), the roof course, `ground_near_wall` + `barred_door` + `bar_or_open` |
| 3.6 over the arcade, in at shutter height, down inside | `crossing_ramp` + `ramp_low` / `ramp_mid` / `ramp_high`; the arcade deck course; `upper_east_wall`'s opening; `tower_midfloor` + `midfloor_well` + `stair_lower` + `tread_low`. `anchor/arcade-climb`, `arcade-walk`, `shutter`, `tower-upper`, `descent` |
| 3.7 shortcut S2, the barred door | `bar_or_open` on the `unbarred` parameter, which ships at 0. `anchor/barred-door` |
| 3.8 the ward at the Dead Ebb | No geometry of its own, by design — it is the same zone with the plane lowered. What makes the floor worth walking is `ward/seabed`, a mix carrying weed over old paving, with the wrecks and the arcade footings standing on it. `anchor/grate-landing` is where `S4` arrives |

The route the `traversable` gate proves is the designed one, not a shortcut
through the door: the causeway is walled by the bars at the tower's near face,
so the only walk from the approach face to the exit face is up the fallen bay,
along the arcade, in through the shutter and down the well.

**Palette** — measured, never named from memory. Material colours are patch
means over crops of the concept image, verified by looking at the crops drawn
back onto the image; every mix was read as a swatch sheet before binding. The
whole image is near-neutral — saturation runs 3 to 13 of 255 across every
sample — so the palette separates by **value**, not by hue, and every structural
role is a mix.

| Role | Mix | Measured | Concept sample |
|---|---|---|---|
| `ward/sea` | `water[level=0]` | — | `#23282b` near water, `#42494d` far. Biome-tinted, so no measurement of the block predicts it |
| `ward/seabed` | `mud` 40% · `deepslate_tiles` 25% · `cobbled_deepslate` 25% · `muddy_mangrove_roots[axis=y]` 10% | `#403e3f` | the ground the Dead Ebb uncovers — silt over the ward's old paving, weed lying in it |
| `ward/quay` | `deepslate_tiles` 40% · `cobbled_deepslate` 30% · `polished_blackstone_bricks` 20% · `blackstone` 10% | `#3b393c` | `#2f3332` the causeway's wet flank |
| `ward/deck` | `deepslate[axis=y]` 35% · `cobbled_deepslate` 30% · `polished_deepslate` 25% · `stone_bricks` 10% | `#535355` | `#54585b` the wet flagstone walking course |
| `ward/kerb` | `tuff_bricks` 35% · `polished_tuff` 30% · `deepslate[axis=y]` 25% · `stone_bricks` 10% | `#616461` | `#5a6063` the raised kerb, which catches what light there is |
| `ward/weed` | `muddy_mangrove_roots[axis=y]` 30% · `black_concrete` 30% · `blackstone` 25% · `polished_blackstone_bricks` 15% | `#292424` | `#282c2d` the black weed heaped on the deck and hanging on the tower base |
| `arcade/footing`, `tower/base` | `deepslate_tiles` 35% · `cobbled_deepslate` 30% · `polished_blackstone_bricks` 25% · `muddy_mangrove_roots[axis=y]` 10% | `#3d3b3d` | `#3a3c38` masonry standing in the water, fouled with weed |
| `arcade/pier_stone`, `arcade/arch_stone` | `tuff_bricks` 30% · `polished_tuff` 25% · `cobbled_deepslate` 20% · `chiseled_tuff` 15% · `blackstone` 10% | `#575a57` | `#5c6164` the arch voussoirs, the palest stone in the image |
| `arcade/deck_stone` | `tuff_bricks` 30% · `cobbled_deepslate` 25% · `polished_tuff` 20% · `deepslate_tiles` 15% · `blackstone` 10% | `#515351` | `#3f4345` the arcade walk |
| `ruin/*` | the three arcade roles again, each with `air` at 15% / 30% / 20% | — | the west arcade, as the sea has left it |
| `tower/wall` | `tuff_bricks` 30% · `cobbled_deepslate` 30% · `chiseled_tuff` 15% · `deepslate_tiles` 15% · `blackstone` 10% | `#4f504e` | `#4e504f` the oversailing storey |
| `tower/roof` | `polished_basalt[axis=x]` 40% · `deepslate[axis=y]` 25% · `polished_deepslate` 25% · `stone_bricks` 10% | `#59595a` | `#5c6268` the metal roof; `polished_basalt`'s stripe is what reads as standing seams |
| `tower/shutter` | `dark_oak_trapdoor[facing=north,half=bottom,open=true,…]` | — | `#3a3b37` the shuttered windows. Stood open so it is a shutter rather than a floor hatch |
| `shortcut/bar` | `iron_bars[…]` | — | the tower's ground door. See-through, so the far side of a shortcut can be read before it opens |
| `wreck/hull` | `deepslate_tiles` 30% · `stripped_dark_oak_log[axis=z]` 25% · `cobbled_deepslate` 20% · `dark_oak_planks` 15% · `muddy_mangrove_roots[axis=y]` 10% | `#423930` | `#5a6267` the sunken boats |

`blackstone` is the loud member of every dressed-stone mix and holds 10% of the
area, which is the craft rule the numbers serve.

Two departures from the nearest colour match, both for role fitness. The
**wreck** measures as a pale bleached grey in the image; it is built from timber
half rotted into the silt, because that reading is aerial perspective at thirty
metres and a grey hull at arm's length reads as masonry. The **weed** is
`muddy_mangrove_roots` and not the nearer-measuring `dried_kelp_block`, which
the swatch sheet settled: kelp's mean is a dark olive but its texture is a
bright green lattice, and it is the only chromatic thing in a monochrome world.

**Every orientation-carrying role is written in the scope's own axis frame.**
Nine of the fifteen roles are `{"local": …}` paints, so an `axis`, a `facing` or
a bar's connection set follows the piece rather than the world: 117 of 296 fills
resolve out of a scope's own frame. It is not decoration here — `tower_face` is
one rule called for the tower's side walls in their own frame and again through
`cross_face`, which hands it a frame where the wall's run is the local X, and the
shutters stand correctly in both without a second rule.

**Open against this piece**

- **The region cannot hold the tower the beats describe.** `beats.md` asks for
  three storeys and `concept/z3-drowned-ward.jpg` for a peaked roof; at the
  manifest's ten courses the vertical budget is one course of ward floor, two of
  water, three of arch, one of arcade deck, two of storey and one of roof, and
  three storeys with a pitch needs thirteen. Two storeys and a single-course cap
  are built, and the oversailing upper storey — the silhouette's strongest
  element — is what carries the recognition instead. Raising the region is a
  manifest change and a design decision, so it is recorded rather than taken.
- **Only one of the two arcades is climbable.** `beats.md`'s *what fills it*
  column asks for two arcades climbable end to end. The east arcade is the upper
  route and has the fallen bay that reaches it; the west is a ruin with a holed
  deck and no way up, which is what makes it read as the wrecked one. A second
  climb is a design decision about whether the upper route should branch.
- **The zone declares no `waterline_y`.** The prefab metadata has the field and
  `DW0344` checks it against the campaign's ocean datum, but the grammar exporter
  writes `None` unconditionally, so a zone whose water *is* the campaign's tide
  plane cannot state where that plane sits from its own program. It is 2 in this
  piece's local frame. Hand-editing it into the metadata was not done: it would
  make the byte-reproduction claim above false. This is a missing engine surface,
  not a defect in the zone.
- The piece declares no spatial contract, so every contract obligation examined
  nothing and `traversable`'s binding counts standable cells on two region faces
  rather than declared ways in — the same gap Z1 carries.
- Lighting is `unmeasured` and cannot be otherwise: `delve-admit lighting` takes
  one structure template and refuses a tile set, and running it on a single tile
  would write a second metadata document describing one slice of a building. No
  rule here exposes a light-emitting role, so light arrives as campaign-bound
  content on the declared anchors.
- One standable cell under a roof has no walking route (x11 y3 z58) and 158 more
  are unreachable but open to the sky. Both are the west arcade: the first is a
  gap inside a ruined pier, the second is its deck, which is scenery and is meant
  to have no way up.
- `anchor/tower-gate` renders as an empty frame. It faces out of the exit face,
  so what it is about lives in the assembled world; it is kept in the review set
  rather than dropped so the gap is visible.

## Z4 chapel ward

**Scene** (fixed before any tool ran, per the procedure's §1): the player drops
out of the keep's kitchen duct onto the floor of a walled chapel ward of pale
grey-green ashlar, steps aside into a low paved nook to rest, and walks the
lane out past a side doorway — behind which a barred grate holds the sealed half
of a shortcut that only opens from the far side.

**Expansion** — `delve-grammar expand --file design/programs/z4-chapel-ward.json
--region 16x9x26 --seed 1 --traversable --allow-falls`. All gates pass with
non-zero bindings: `blocks-exist` 7, `non-empty` 3744, `traversable` 10 (5
standable cells at the approach end, 5 at the exit end, 165 in all; the entry is
a fall, hence `--allow-falls`). 3045 filled cells, 7 distinct states, 6 anchors,
silhouette complexity 1.03. `delve-admit audit` passes (0 forbidden, 0
non-allowlisted, 0 unknown).

**Provenance** — program `sha256:eb6b39ddd66c20ff4657767635a91269118b8d6cd494090988d7b90571435540`,
seed 1, region 16x9x26; re-expanding those inputs reproduces the `.nbt` byte for
byte (verified: `sha256:ac11c68d2eb97eca5f5218fbeb11df9dbb9a49eefb4bdfaaed0b8f67aecf6019`).
It is recorded here as well as in the metadata because `delve-admit lighting
--write` rewrites the metadata without the machine-readable `license.generated_by`
block.

**Artifacts** — `prefabs/z4-chapel-ward.nbt` + `prefabs/z4-chapel-ward.json`
(the repo's flat prefab library, where every other campaign's pieces live);
review shots in `design/review/z4/`.

**Palette** — measured, never named from memory: material colours sampled from
the concept image (patch means over verified crops), then blocks taken from
`tools/block-appearance.py --near` ranked lists, full-cube for everything
structural.

| Role | Block | Measured | Concept sample |
|---|---|---|---|
| `junction/rock` | `minecraft:tuff_bricks` | `#62675f` | `#626863` lit arcade ashlar |
| `hearth/rock` | `minecraft:tuff_bricks` | `#62675f` | `#626863` — same stone as the junction, so the lane reads as one building |
| `shortcut/rock` | `minecraft:polished_tuff` | `#626864` | `#5c6160` far-wall arch stone; smooth, for the plainer sealed chamber |
| `chute/rock` | `minecraft:cobbled_deepslate` | `#4d4d51` | `#4f554b` shadowed lower masonry — the service duct is not the ward |
| `hearth/hearth_floor` | `minecraft:polished_andesite` | `#848786` | `#7b8789` lit flagstone — the rest plate |
| `margin` | `minecraft:deepslate` | `#545456` | inert mass, no player-visible face |
| `shortcut/bar` | `minecraft:iron_bars` | `#898b88` | `#262e31` door ironwork |

The bar is the one deliberate departure from the nearest colour match. The
concept's barrier is a timber door leaf, but the rule seals a 6-wide by 3-high
partition opening, which is a portcullis and not a leaf; a see-through grate is
also what lets the player read the far side of a shortcut before it opens.

**Open against this piece**

- Lighting profile is `dark` (`DW0751`, min floor light 0 over 165 walkable
  cells). No rule in this zone exposes a light-emitting role, so the piece
  cannot be lit from its palette: light has to arrive as campaign-bound content
  on the declared anchors, or as a light role added to the library rules.
- The concept image is an open, roofless cloister; the zone's design intent and
  topology are an enclosed hub. The palette and proportions converge on the
  concept's material and tone, and the composition does not — deliberately, the
  topology is fixed.
- 47.9% of the piece is `margin`, the inert mass behind the shortcut rooms.
