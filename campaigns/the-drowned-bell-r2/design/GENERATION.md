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
it: all eight pass `oriented-fills`, six of them carry local roles, and the
audit totals **62** fills resolved out of a scope's own frame across those six.
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
| Z4 chapel ward | `concept/z4-chapel-ward.jpg` | `programs/z4-chapel-ward.json` | **produced, awaiting owner review** — see below |
| Z5 hall keep | `concept/z5-hall-keep.jpg` | `programs/z5-hall-keep.json` | **produced, awaiting owner review** — expands at 11x11x76 and ships as 2 tiles; review set in `review/z5/` — see below |
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

## Z5 hall keep

**Scene** (fixed before any tool ran, per the procedure's §1): the player enters
an intact great hall — timber-beamed ceiling on, ashlar walls dry, floor swept —
walks its length past a gallery perch and a store lane of standing barrels, and
leaves down a descent that does not climb back. It is the first room in the delve
that is not a ruin, and the only one the sea has never entered.

**It is a one-way descent, and that is the design.** The route enters at the hall
floor and ends on the lower landing; nothing climbs back. So the piece cannot
satisfy `--reachable-floor` and does not claim it — a red gate writes no `.nbt`,
so claiming it would ship nothing rather than ship a known red. The always-on
reachability line is read instead, and the lower keep appears there as an
unreachable sheltered pocket. **That pocket is the descent, not a room with no way
in**, and this sentence is what tells a later reader which it is.

**Expansion** — `delve-grammar expand --file design/programs/z5-hall-keep.json
--region 11x11x76 --seed 1 --traversable --allow-falls`. All six gates pass with a
non-zero binding: `blocks-exist` 11, `shape-complete` 11, `states-complete` 11,
`oriented-fills` 106, `non-empty` 9196, `traversable` 18 (9 standable cells at the
approach end, 9 at the exit end). 6126 filled cells, 11 distinct states, 697
standable, 14 anchors, silhouette complexity 1.50, and 29 local-frame fills — the
last is a measurement the corpus audit rolls up across programs, not a gate on
this zone.
`delve-admit audit` passes over 9196 blocks (0 forbidden, 0 non-allowlisted, 0
unknown, 0 pre-pin unknown, 0 under-specified).

**It ships as a tile set.** 76 is past the 48-per-axis structure-template cap, so
the expansion is written as 2 tiles in a 1x1x2 grid plus one manifest, cut
deterministically at z=48. Every gate above judged the whole zone, and
`delve-render piece` reassembles the tiles before placing a camera, so the review
set frames one building and no shot is cut at the packaging plane. The
consequence to know: `delve-admit lighting` takes one structure template and
refuses a manifest (`DW0732`), so **this zone has no lighting step and carries
`"profile": "unmeasured"`**. Running `lighting` on a single tile would succeed and
write a second metadata document describing one slice of the building, which is a
number about nothing; the tiles are left alone.

**Provenance** — program
`sha256:3db9ce6916603b68d3bde669e2c67cc601c978a283b753f7f3108e261a715a2d`, seed 1,
region 11x11x76; re-expanding those inputs reproduces both tiles and the manifest
byte for byte (verified by direct comparison against the shipped files, and again
by hashing each file's contents alone — a hash taken over a listing would have
compared the file paths as well as the bytes). The hash is over the **effective**
program, so it is not the hash of the file's own text. Every value this zone ships
at lives in the program's own `params`, so the file plus the manifest row is the
whole recipe and no remembered flag is needed.

**Artifacts** — `prefabs/z5-hall-keep.json` (the tile-set manifest) with
`prefabs/z5-hall-keep.x0y0z0.nbt` and `prefabs/z5-hall-keep.x0y0z1.nbt` beside it,
in the repo's flat prefab library; review shots and what each camera answers in
`design/review/z5/`.

**Palette** — measured, never named from memory. Material colours are patch means
over crops of the concept image, verified by drawing the crops back onto the image
and looking at where they landed; candidates come from `tools/block-appearance.py`
over the measured targets, and the mixes were read as a swatch sheet before
binding.

The concept is a dark, atmospheric painting, and every masonry patch in it
measures with a very wide value range — the hall's ashlar runs from `#262829` in
shadow through `#3b3d3e` to `#5e676b` in the light shafts, a spread of 73 out of
255. **A near-neutral wide-range measurement is a mix, not a block**: bound to one
block the hall reads as a flat panel that no measurement of the mean would object
to, which is exactly what it did before this pass. The value the mix is anchored on
is the **lit** share rather than the whole-patch mean, because the lit share is
where the material is revealed and the shadow is the painting's lighting rather
than the stone's colour.

| Role | Mix | Measured | Concept sample |
|---|---|---|---|
| `hall/stone`, `gallery/stone`, `motif/stone`, `door/stone`, `stores/stone` | `tuff_bricks` 60% · `polished_tuff` 20% · `chiseled_tuff_bricks` 10% · `deepslate_tiles` 10% | `#5e635d` | `#5e676b` lit hall ashlar — the chimney breast and the wall piers where the light shafts cross them |
| `duct/rock` | `minecraft:cobbled_deepslate` | `#4d4d51` | the service duct is not the hall, and is bound to the same stone Z4's chute is |
| `gallery/pedestal` | `minecraft:chiseled_tuff_bricks` | `#696d65` | the stand in the gallery — the wall mix's own loud member, used whole so the object reads against the wall it stands on |
| `hall/timber`, `gallery/timber` | `minecraft:dark_oak_wood[axis=y]` | `#3c2f1a` | `#282626` lit roof truss — the nearest wood on the shelf; the concept's timber is darker because it is the deepest shadow in the frame |
| `motif/curtain` | `minecraft:iron_chain[axis=y,waterlogged=false]` | — | the hanging strands across the hall's far opening |
| `stores/barrel`, `stores/barrel_unbanded` | `minecraft:barrel[facing=up,open=false]`, `minecraft:spruce_log[axis=y]` | — | the store lane's standing casks, banded and plain |
| `margin` | `minecraft:deepslate[axis=y]` | — | inert mass, no player-visible face |

The five keep-interior stone roles take **one** mix, so the hall, the gallery, the
motif wall, the doorway and the stores read as one building — the rule that the
interior belongs to the same theme as the outside, applied inside. `tuff_bricks`
is also Z4's ashlar: the chapel ward is reached through this keep's own duct, and
two rooms of one building are not two materials. `deepslate_tiles` is the dark
member at 10%, which is the craft rule the numbers serve — the flat dark panels
read as deliberate repair, where a rubbly dark member read as ruin on the swatch
sheet and this hall is explicitly not one.

**Every orientation-carrying role is written in the scope's own axis frame.** The
six roles that carry a direction — both timbers, the margin, the curtain and both
barrel roles — are `{"local": …}` paints, and the program declares `1.4.0`, the
version the local frame is fenced behind. 29 of 29 orientation-carrying fills now
resolve through the scope that fills them, where **0 did before**.

The reason this is not decoration here is worth stating, because the zone passed
every gate without it. The hall is entered through `reorient {y: world_y, z:
largest}`, and at *this* region 76 is already the largest axis — so the frame is
the identity, and a bare state lands correctly. The safety was a property of the
region, not of the program: a grammar program is region-polymorphic, and at any
region where x exceeded z the same bare states would land turned, with every gate
still green. Two of the program's nine reorientations (`door/alcove_air`,
`stores/tell_cell`) are genuine quarter-turns that only leave these states alone
because all six are stated about the vertical, which no turn about the vertical
moves. Wrapping them was proved to emit **byte-identical** blocks at this region,
so it cost the shipped piece nothing and bought it correctness everywhere else.

**Open against this piece**

- **The lower landing is bare floor.** The descent ends on it and there is nothing
  on it — no fitting, no cover, no object; `review/z5/eye-landing.png` is a frame
  containing a floor and the background. A big empty room is a small building that
  costs more to walk across, and this is one. The program exposes no rule that
  furnishes the landing, so what goes there arrives as campaign-bound content on
  the declared anchors, or as a rule this program does not have.
- **46.0% of the piece is `margin`**, the inert mass around and below the hall. The
  `anchor/hatch` anchor stands inside it, so its eye camera looks into solid rock
  (`review/z5/eye-hatch.png`) — an anchor aimed at nothing in this piece.
- Lighting is `unmeasured` and cannot be otherwise: a tiled zone has no lighting
  step (above). No rule in this zone exposes a light-emitting role either, so the
  hall's light — the shafts through the slit windows that beat 5.1 is built on —
  has to arrive as campaign-bound content on the declared anchors.
- **The hearth, the tapestries and the far arch have no role and no rule in this
  program.** They are three of the zone's beats: the cold laid hearth, the priory's
  own account of itself panel by panel, and the arched doorway to the chamber the
  prior sits in. The hanging strands stand in for the third; the first two are
  design work this production did not do.
- The concept's roof is an open truss with rafters and light between them. Here the
  span beams read as a beamed ceiling rather than an open truss, because the truss
  band's course above the beam is the piece's top and there is nothing to see
  through it to. At playable scale the ceiling carries the recognition; the
  rafter-by-rafter detail it was never going to have is not a defect.
- The piece declares no spatial contract, so every contract obligation examined
  nothing and `traversable`'s binding counts standable cells on two region faces
  rather than declared ways in.
- Judge it from the eye shots. A roofed interior photographs as a closed box from
  outside, so the exterior orbit cameras are the weakest shots in the set;
  `review/z5/README.md` says which camera answers which question.
- **This is the first tiled zone in the flat prefab library, and the prefab
  palette audit cannot yet read one.** That job globs `prefabs/*.nbt` and audits
  each file alone, which a tile set does not answer to in either direction: the
  manifest is the only file that describes the zone and a `*.nbt` glob never
  reaches it, while a per-tile verdict is one the current engine deliberately
  **refuses** to give (`DW0732`) on the ground that a verdict over one file reads
  as a verdict over the zone. Separately, the engine that job pins predates
  `minecraft:iron_chain` in the palette allowlist, so it reds one tile with
  `DW0730` — reproduced identically against this zone's pre-production expansion,
  so it is a property of the pinned allowlist and of this zone's palette, not of
  this production pass. Z1 and Z4 pass at that pin because neither ships the
  block. The zone itself audits clean as a zone: `delve-admit audit` over the
  manifest passes on 9196 blocks with zero findings.
