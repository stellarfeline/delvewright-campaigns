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
it: all eight pass `oriented-fills`, six of them carry local roles, and the audit
totals **193** fills resolved out of a scope's own frame across those six.
Z1 is the worked case, and it shows why the frame is not decoration: the corpse
is authored as `rotation=8`, facing out of its own recess, and lands in the world
as `rotation=4`.

Z0 is the other kind of case, and it is the one a green hides. Its root asks for
`z: largest` over a box already longest along Z, so the frame it stands in is the
**identity** — and a world-frame literal under an identity frame is not judged at
all, which is a different fact from being judged and found sound. The engine now
splits those two with a third verdict, *this region cannot decide it*, and the
way not to depend on which one a green means is to write the state in the scope's
own frame in the first place.

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
| Z0 barrow shore | `concept/z0-barrow-shore.jpg` | `programs/z0-barrow-shore.json` | **produced, awaiting owner review** — expands at 40x18x80 as a 2-tile set; review set in `review/z0/` — see below |
| Z1 cliff road | `concept/z1-cliff-road.jpg` | `programs/z1-cliff-road.json` | **produced, awaiting owner review** — expands at 10x28x44; review set in `review/z1/` — see below |
| Z2 gate ward | `concept/z2-gatehouse.jpg` | `programs/z2-gate-ward.json` | **produced, awaiting owner review** — expands at 25x18x56 as a 2-tile set; review set in `review/z2/` — see below |
| Z3 drowned ward | `concept/z3-drowned-ward.jpg` | `programs/z3-drowned-ward.json` | program exported, unproduced |
| Z4 chapel ward | `concept/z4-chapel-ward.jpg` | `programs/z4-chapel-ward.json` | **produced, awaiting owner review** — see below |
| Z5 hall keep | `concept/z5-hall-keep.jpg` | `programs/z5-hall-keep.json` | program exported, unproduced |
| Z6 cistern deep | `concept/z6-cistern-deep.jpg` | `programs/z6-cistern-deep.json` | program exported, unproduced |
| Z7 bell tower | `concept/z7-bell-tower.jpg` | `programs/z7-bell-tower.json` | program exported, unproduced |

Zone order of production is by complexity, hardest first (owner decision,
2026-08-12): the most complex zone is produced and owner-reviewed before the
rest, so a workflow defect is found on the zone most likely to expose it.

## Z0 barrow shore

**Scene** (fixed before any tool ran, per the procedure's §1): the player wakes
face-down on a causeway of wet grey sand running north across a half-mile of
tidal flat, walks up through a line of three rusted stakes into a field of
drystone graves that thins as the ground rises inland, and reaches a shelf of
worked stone under the rock's foot where a lamp is burning in daylight and one
cut ledge starts up the cliff. Below the stake line the ground drops a course
into soft dark mire, which the sea covers at every state of the tide but the
lowest.

### Every beat, and the rule that builds it

`beats.md` is what this zone must stage. A beat with no rule beside it is absent,
and none is.

| # | beat | rule(s) that build it | anchors |
|---|---|---|---|
| 0.1 | wakes face-down on wet flat, a heap of stones a few metres away | `causeway/spine` → `causeway/wake_row` → `causeway/wake_post`; the heaps it wakes among are `mud/plan` → `mud/cairn_row` → `mud/mound`, and the nearest is 7 blocks up-causeway | `wake` (north) |
| 0.2 | the cairn field, readable, thinning inland | `cairn/field` → `cairn/row` → `cairn/mound` → `cairn/heap` → `cairn/inset_x` / `cairn/inset_z`; `flat/inner` and `flat/outer` call the one field rule under a `bind` that rebinds `cairn/gap` and `cairn/row_gap`, and that binding **is** the density gradient. The three readable graves are `cairn/grave_row` → `cairn/grave` | `grave-1..3` (north) |
| 0.3 | first enemy pushes up out of the mud beside a cairn, walking landward | `flat/outer` → `flat/first_row` → `flat/answered_post`, one cell east of a `cairn/mound` on the last row of flat before the line | `first-answered` (north, i.e. landward) |
| 0.4 | K1 the tide-stakes: three iron posts, lethal outside the line | `stake/band` → `stake/line` → `stake/post` for the posts; the boundary itself is `ground/flat` meeting `ground/mire` — one course down and a visibly different paint — and the graves crowding it are `cairn/grave_row` plus `cairn/row` under a tighter `bind` | `stake-1..3` (north), and `mire-1..2` for the hazard box |
| 0.5 | Emeric on the last dry shelf, shore-lamp lit in full daylight | `cliff/shelf_lane` → `shelf/plate` → `shelf/furnish` → `shelf/stand` for the standing cell, `shelf/front_wall` → `shelf/wall_course` for the low walling and `shelf/lamp_cell` for the lamp on it | `lampman` (south) |
| 0.6 | the flat ends at a wall of cliff; one cut ledge starts up it | `cliff/band` → `cliff/crag` → `cliff/crag_face` → `cliff/batter` for the face, `cliff/cut` → `ledge/start` → `ledge/run` and `ledge/foot_tread` for the ledge | `ledge-foot` (north) |
| 0.7 | the Dead Ebb return: the answered standing in the silt, facing the rock | `mud/band` → `mud/field` → `mud/plan` → `mud/figure_field` → `mud/figure_row` → `mud/figure_post`, on `ground/mire` a course below the flat | `silt-1..24` (north, i.e. facing the rock) |

**7 of 7 built.** Beats 0.4 and 0.7 are built as far as a grammar program reaches
— the ground, the boundary and the positions — and each needs one campaign-level
declaration to finish: a hazard on `anchor/mire-1..2`, and bodies on
`anchor/silt-*`. Neither is geometry and neither is expressible here.

**Expansion** — `delve-grammar expand --file design/programs/z0-barrow-shore.json
--region 40x18x80 --seed 1 --traversable --id z0-barrow-shore -o out/`. Every
gate passes with a non-zero binding: `blocks-exist` 12, `shape-complete` 12,
`states-complete` 12, `oriented-fills` 383, `non-empty` 57600, `traversable` 44.
19 067 filled cells of 57 600, 12 distinct states (11 of them not air), 2854
standable cells, footprint 3200 columns, perimeter 240, silhouette complexity
1.06, 37 anchors. Reachability: 2764 of 2854 standable cells reached on foot from
135 grade entry cells; **0 sheltered**, so the piece is open to the sky end to
end, and the 90 unreached cells are the crag's own batter ledges and the tops of
the three stakes — floor open to the sky, which the report states as a number and
never as a finding. `delve-admit audit` passes over 57 600 blocks (0 forbidden, 0
non-allowlisted, 0 unknown, 0 pre-pin unknown, 0 under-specified, 0 findings),
with a per-tile verdict for both tiles.

**Provenance** — program
`sha256:be06fc468d1b5fafa15bba95a649cdaa96d3e93d46cf1249ca312c88363b17c9`, seed
1, region 40x18x80. Every tuned value lives in the program's own `params`, so the
file plus the manifest row is the whole recipe and no remembered flag is part of
it.

Reproduction was taken from a **second instrument**: a separate worktree at the
same engine commit, its own cargo target tree, its own working directory and its
own output directory. Three methods, none of which hashes a file path — `cmp`
over the bytes, `shasum` fed from **stdin** so no name reaches the digest, and a
cell-by-cell diff through a structure-template reader written for the check
rather than by the expander. 3 of 3 files identical, 57 600 of 57 600 cells
equal, 0 differing, 37 anchors identical, program hash equal. The two release
builds of the pinned commit are themselves byte-identical.

**Artifacts** — `prefabs/z0-barrow-shore.x0y0z0.nbt`,
`prefabs/z0-barrow-shore.x0y0z1.nbt` and `prefabs/z0-barrow-shore.json` in the
repo's flat prefab library. The zone is past the 48-per-axis structure-template
cap on its long axis, so it ships as a tile set in a 1×1×2 grid and **the
manifest is the only file that describes the zone**: the gates, the render and
the admission audit all take it and treat the tiles as one thing. Review shots and
what each camera answers: `design/review/z0/`.

**Palette** — measured, never named from memory. Material colours are patch means
over crops of the concept image, verified by drawing the crops back onto it and
looking; candidates come from `tools/block-appearance.py --near` over the measured
shelf, and every mix was read as a render before it was believed.

| Role | Mix | Measured | Concept sample |
|---|---|---|---|
| `shore/sand` | `cobbled_deepslate` 30% · `mud` 22% · `tuff` 20% · `deepslate[axis=y]` 18% · `blackstone` 10% | `#4d4c4e` | `#545c60` the open wet flat mid-frame; p05 51, p95 128 out of 255, so a **mix** and not a block — bound to one block the flat reads as a floor |
| `shore/silt` | `mud` 55% · `cobbled_deepslate` 20% · `deepslate[axis=y]` 15% · `blackstone` 10% | `#413f43` | `#4b5254` the nearer, wetter flat. Held against `shore/sand` it is the whole of beat 0.4's tell: the ground below the line is a different colour, at every tide and from any distance |
| `cairn/stone` | `cobblestone` 42% · `andesite` 18% · `cobbled_deepslate` 18% · `blackstone` 12% · `mossy_cobblestone` 10% | `#6c6c6b` | `#3e4444` the big foreground-left cairn, p95 128 — pale rounded stones in a dark matrix, which is a mix and not a mean |
| `cliff/rock` | `cobbled_deepslate` 50% · `smooth_basalt` 30% · `blackstone` 10% · `deepslate[axis=y]` 10% | `#49484d` | `#3c4348` the near cliff face. **Z1's `crag`, unchanged** — Z0's crag and Z1's cliff are the same rock, and two mixes would put a seam in it |
| `ledge/rock` | `cobbled_deepslate` 60% · `deepslate[axis=y]` 20% · `tuff` 10% · `blackstone` 10% | `#4e4e50` | Z1's `path/rock`, unchanged, for the same reason: the cut ledge here is the road there |
| `shelf/stone` | `cobblestone` 48% · `tuff` 22% · `cobbled_deepslate` 20% · `mossy_cobblestone` 10% | `#70706e` | `#3b3f3e` the drystone walling right of frame — the same family as the graves, a shade lighter where it is worked |
| `shore/bed` | `cobbled_deepslate` | `#4d4d51` | inert mass under every surface; no player-visible face except the region's own sides |
| `stake/iron` | `dark_oak_fence` | `#432b14` | `#201b16` the right-hand post, saturation 10.8 — warm and very dark |
| `shelf/lamp` | `lantern[hanging=false,waterlogged=false]` | `#6b5c55` | the shore-lamp |

Every mix's loudest chromatic member sits at 10% of area or less, which is the
craft rule the numbers serve. **The binding is 9 of 9 roles**, and it had to be
taken a role at a time with `--mix`: `block-appearance.py --program` reads a
paint only when it is a string or a list, so a paint written in the scope's own
axis frame is a `dict` and is skipped by both arms in silence. Pointed at this
program it prints `binding: 4 paint(s) examined` over a program that declares
nine, having missed all five local ones — including `cliff/rock` and
`shore/sand`, which write 50.3% of the zone's blocks between them. The line reads
as a pass.

**What each role actually writes**, measured rather than inferred from the block
census: the two are different questions, since one block serves several roles.
Each role was rebound to a marker block in turn and the marker counted off the
expansion, which moves no geometry — and the nine come to 19 067 cells exactly,
i.e. they partition the filled zone, which is the check that the method is
reading what it thinks it is.

| Role | cells | share of filled |
|---|---|---|
| `cliff/rock` | 7446 | 39.1% |
| `shore/bed` | 7430 | 39.0% |
| `shore/sand` | 2150 | 11.3% |
| `cairn/stone` | 997 | 5.2% |
| `shore/silt` | 490 | 2.6% |
| `ledge/rock` | 328 | 1.7% |
| `shelf/stone` | 216 | 1.1% |
| `stake/iron` | 9 | 0.05% |
| `shelf/lamp` | 1 | 0.01% |

Two substitutions, both deliberate and neither a colour match:

- **The stakes are a fence, not iron.** Vanilla has no thin rusted-iron post.
  What carries "iron stake" at played scale is the silhouette — a 4/16 post reads
  as a stake where a full block reads as a pillar — plus the measured warm-dark
  value against the flat's cool grey. `iron_bars` is the right material and the
  wrong colour (`#898b88`, lighter than the ground it stands in); `dark_oak_fence`
  is the right colour and the wrong material, and the silhouette is the half that
  survives at 1 m per block.
- **The black weed is the dark member of the ground and cairn mixes, not a block
  of its own.** `dried_kelp_block` is the thematically exact choice and its mean
  (`#2e3724`) is almost the concept's weed (`#2e3234`) — and it renders as
  saturated green with cream borders, loud at 10% of area across a whole flat.
  `sculk` was tried next and renders as bright cyan speckle. Both were caught by
  looking, not by measuring; a mean cannot see a texture. `blackstone` is what the
  weed reads as at played scale: a near-black smear on grey.

**Every orientation-carrying role is written in the scope's own axis frame.** Five
of the nine roles are `{"local": …}` paints and 160 of the 161 fills that carry
block-state properties resolve through the scope that filled them; the one that
does not is the lantern, whose two properties name no direction. That matters
here for a reason this zone would otherwise have hidden: its root asks for
`z: largest` and its box is already longest along Z, so **the frame is the
identity and a world-frame literal would have passed every gate at this region
and landed wrong at any other**. Checked rather than assumed — the same program
was expanded at an engine carrying the third verdict for that gate, which reports
`this region cannot decide it` exactly where a green means "never judged", and
`oriented-fills` comes back `pass` and not `undecided`. The two engines produce
byte-identical output over all 57 600 cells.

**The fog band, and what closes the shore.** Beyond the played flat the shore is
closed by fiction, not by a gradient, and neither half of it is geometry:

- a **`boundary`** declaration (`{margin, message}`) derives the playable region
  from the placed pieces and runs a 1 s clock that returns a player outside it to
  the last checkpoint with an actionbar line and a soft sound, taking no damage
  and no item. The line is the narration hook and is already inventoried for
  translation as `world.boundary.message`;
- a **`give-effect`** with an `in` box centred on an anchor is the fog itself — a
  status effect scoped to a coordinate box, the same box model a stealth zone and
  a lethal volume use.

The zone's part is to make the band mean something rather than merely hide a
wall. `anchor/crossing` sits on the causeway's own mouth at the region's south
face, facing south, and it is the cell the narration binds to: what lies that way
is the crossing, which the player has already made. `map-brief.md` fixes the
words. The anchor renders as an empty frame and is kept in the review set for
that — it faces out of the piece, which is exactly what it is for.

**Open against this piece**

- **The piece declares no spatial contract**, so every contract obligation
  examined nothing, and `traversable`'s binding of 44 counts standable cells on
  two faces of the region rather than declared ways in. The zone has four real
  ones — the causeway's mouth south, the ledge north, and the open flat running
  off east and west into the fog — and stating them would turn that 44 into 4
  doors and put the mire, the shelf and the ledge into named spaces with proven
  edges between them. It is the largest single thing still owed here.
- **The crag's batter is regular.** The face steps back one cell every three
  courses, which makes it a cliff rather than a staircase (a one-course riser
  would be a step, and the way on would stop being the only way on) and gives the
  silhouette the receding ledges the concept's cliffs have. What it cannot do is
  vary: the language has no positional index, so every bay of the face steps at
  the same height, and the concept's face does not.
- **`delve-admit lighting` cannot measure a tiled zone, and does not say so.**
  Handed the manifest it fails with `DW0732 gzip decode: invalid gzip header`,
  having tried to read the JSON as NBT. Handed one tile of the set it returns a
  verdict — `profile: dark`, 1574 floor cells, min light 0 — over 48 of the zone's
  80 blocks of length, i.e. 1574 of its 2854 standable cells, with no indication
  that it is looking at half a zone. `delve-admit audit` refuses that same lone
  tile by name and points at the manifest, and so does `delve-render`; the guard
  exists in two of the three doors. So no lighting profile was written, and the
  metadata still says `"profile": "unmeasured"`, which is a positive statement
  that a measurement is owed rather than a missing field.
- **The number would be wrong here in a second way even if it could be taken.**
  The probe measures block light, and this zone is open to the sky over all 2854
  of its standable cells; the one light it carries is Emeric's lamp. An open
  beach at noon reports `dark`.
- **A mire that is lethal at one tide and safe at another is not a
  `lethal_volumes[]`.** That surface has no state gate, so a volume declared over
  the mire would kill the answered standing in it at the Dead Ebb — and
  `DW0511` forbids posting a body inside one, which is exactly what
  `anchor/silt-*` does. The expressible form is a `trigger` carrying
  `damage-players {amount, in: {anchor: mire-<i>, extent}}` under `requires_state`
  on the tide, which is gateable at all 35 sites. Recorded because the obvious
  reading of beat 0.4 reaches for the wrong verb.
- **Mass the player never touches is 78.0% of the zone.** `shore/bed` is 39.0%
  — the courses under every surface, with no visible face but the region's own
  sides — and `cliff/rock` is 39.1%, nearly all of it solid rock behind a face
  seen only from the south. Both are doing work beat 0.6 asks for, and both are
  still mass nobody walks in; the eight roles a player can actually see total
  22.0%. So when the §4 palette budget lands as a diagnostic, this zone's claim
  has to be scoped to reachable mass or it will be a judgement about the inside
  of a cliff — the same risk `grammar.md` §5c records for Z6's margin, at twice
  the share.
- **The shore is drawn against `reference/map-brief.md`, which is not on this
  branch** and was read from its own. `beat-audit.md`, the document that found
  this zone staged none of its beats, has since landed here — and every Z0 row in
  it describes the program this one replaces. It states Z0 at 19×6×24, 1422
  filled cells, two block states, one anchor and 7 of 7 beats absent; it gives a
  reproduction command at a region `zones.json` no longer declares; and its
  campaign-wide finding that there is **not one block that emits light** across
  the produced zones, which `reconciliation.md` carries too, now has this zone's
  lamp as its counter-example. The audit is a record of what was found, not a
  claim about what is here now, and nothing in it should be quietly rewritten —
  but a reader who lands on it first will read live claims about a file that no
  longer builds any of what it describes.

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

## Z2 gate ward

**Scene** (fixed before any tool ran, per the procedure's §1): the cliff road
ends at a hole the sea has torn through the gatehouse's seaward wall, and the
player steps out of it into a vaulted stone passage with a gutter cut down the
middle of its flags. Two paces ahead the portcullis is down, and the
flat they woke on is on the other side of it. Behind them the passage runs
inward under a row of openings in its crown; a grated embrasure in the west wall
shows a porter's lodge with a ledger still on its stand; the winch that would
raise the gate is at the far, inner end. A stair off the passage's east side
climbs past the floor those openings belong to and comes out on the leads, where
a second winch has had nothing to lift for fifty-one years. The way on is
through an arch in the gatehouse's inner wall, across a yard, and off a lip on
to the drowned ward's causeway two courses below.

### Every beat, and the rule that builds it

`beats.md` is what this zone must stage. A beat with no rule beside it is
absent, and none is.

| # | beat | rule(s) that build it | anchors |
|---|---|---|---|
| 2.1 | entry through the breach, inside a **lowered** portcullis, the shore visible through its bars | `breach/skin` → `breach/outer` / `breach/inner` — the hole goes through both leaves of the seaward skin and the passage reaches its own outer face through it — then `breach/lane` → `breach/room` → `breach/stand`. The gate itself is `grille/band` → `grille/plane` → `grille/bars` + `grille/threshold`, the bar standing from the flags to the springing | `breach` (south), `gate` (on the bar) |
| 2.2 | **K3 the murder-holes**: openings in the vault, a killing drop on the centre line, safe edges, and a floor above with something on it | `pass/crown` → `shaft/crown_row` → `shaft/hole` and `pass/soffit` → `shaft/floor_row` → `shaft/floor_hole` cut one cell through both courses every `shaft_period`; `gate/paving` puts the gutter on the centre line with a mitred kerb each side and two flags of safe outside each kerb; the storey is `pass/lane` → `chamber/room` → `chamber/watch`, and what is on its floor is `winch/lane` → `chamber/store` → `chamber/gear` | `murder-hole-1..4` (in the openings), `murder-watch` |
| 2.3 | the drain: a cut channel, still water at the plane's height or a dry gutter, out under the gate | `gate/paving` (the gutter one course below the flags, `gate/kerb_west` / `gate/kerb_east` mitred against it), `grille/threshold` (the outfall through the portcullis's own bars), `mouth/paving` (the gutter running on through the arch to the region face) | — |
| 2.4 | **G1 the guardroom**: a grated embrasure, ledger leaves on the sill and floor, the bound ledger inside | `lodge/band` → `lodge/room` → `lodge/air` → `lodge/fitout` → `lodge/litter` → `lodge/desk`; the embrasure is `lodge/face` → `lodge/embrasure` → `lodge/sill` + `lodge/grate` → `lodge/grate_leaf`. The lodge is declared **out of the walk** and earns the `posted` kind | `ledger` (east), `embrasure` (west) |
| 2.5 | **optional elite — the Gatewright**, on the roof above the murder-holes, working a winch; roof stair off the critical path | the leads are `top_gear` → `roof/leads` → `roof/winch` → `roof/frame` / `roof/drum` / `roof/stand`, with `roof/spall` heaping fallen coping along them; the climb is `stair/band` → `stair/well` → `stair/foot_landing` / `stair/lower` / `stair/mid_landing` / `stair/upper` / `stair/head_landing`, over `stair/run` and its reflection | `gatewright`, `stair-foot`, `stair-head` |
| 2.6 | **S1 the portcullis**, raised from a winch on the passage's inner side | `grille/bars` is the bar region the contract's `barred` edge is proved against; the winch is `winch/band` → `winch/lane` → `winch/room` → `winch/gear` → `winch/frame` / `winch/post` / `winch/drum`, and the cell it is worked from is `winch/stand` | `gate` (on the bar), `winch` (south, i.e. down the passage at the gate) |
| 2.7 | Emeric moves up to the gate passage and stays; the lamp goes with him | `lodge/band` → `lamp/niche` → `lamp/air` → `lamp/fitout` → `lamp/bracket` — a pocket off the lane, one way in through `lamp/mouth`, its own floor, and a lantern set in its wall | `lampman` (east, out of the niche) |

**7 of 7 built.** Beats 2.2 and 2.5 are built as far as a grammar program
reaches — the openings, the storey they belong to, the ground the elite is
fought on — and each needs one campaign-level declaration to finish: a hazard
bound to `anchor/murder-hole-*`, and a body on `anchor/gatewright`. Neither is
geometry and neither is expressible here.

**Three of those beats are proved by machine, not asserted.** The contract's
`barred` edge is beat 2.6: the walk from the passage does **not** reach the gate
arch while the bar stands, and does with the bar voided — 21 bar cells, 10 cells
of arch beyond them. The `stair` edges are the reachable storey beat 2.2 calls a
map and the roof beat 2.5 puts a man on: `contract-reachability` reaches all
1690 standable cells in declared space from the entry, one of them only once
that bar is opened, and names which bar. And the lodge is beat 2.4's *gate*: it
is declared out of the walk and earns `posted` — 25 standable cells, every one
within two of a declared anchor — rather than being a room that happens to have
no door.

**The stair is beside the route, measured rather than argued.** Cut its doorway
column (56 standable cells at `x = 16`) and the breach face still reaches the
causeway head; the stair well is then unreachable, and the zone still crosses.
Taken from the shipped bytes by the second instrument, not from the expander.

**Expansion** — `delve-grammar expand --file design/programs/z2-gate-ward.json
--region 25x18x56 --seed 1 --traversable --allow-falls --id z2-gate-ward -o
out/`. **Fifteen gates, every one passing with a non-zero binding**:
`blocks-exist` 28, `shape-complete` 28, `states-complete` 28, `oriented-fills`
386, `non-empty` 25200, `traversable` **2 declared ways in or out** (not face
cells — the piece declares a contract), `contract-well-formed` 16,
`contract-coverage` 1787, `contract-closure` 3714, `contract-edge-proof` 6,
`contract-no-body` 2, `contract-reachability` 1690, `contract-anchors` 17,
`contract-exterior-faces` 2, `contract-no-body-majority` 1787. 14 959 filled
cells of 25 200, 28 distinct states (27 of them not air), 1787 standable cells,
footprint 1400 columns, perimeter 162, silhouette complexity 1.08, 17 anchors.
`delve-admit audit` passes over 25 200 blocks (0 forbidden, 0 non-allowlisted, 0
unknown, 0 pre-pin unknown, 0 under-specified, 0 findings), with a per-tile
verdict for both tiles.

**The always-on reachability line reads 136 of 1787, and that is the zone's
topology rather than a defect.** That walk starts at *grade* — the lowest side
face a body stands on, which here is the causeway head, two courses below
everything else — and a two-course lip cannot be climbed. The instrument that
answers the question this zone actually makes is `contract-reachability`, which
starts at the declared entry and reaches every one of the 1690 cells in declared
space. `grammar.md` §4d records exactly this: on a piece whose design is a
one-way descent, `--reachable-floor` is a gate to leave off rather than to
satisfy, and the zone declares `allow_falls` for the same reason. It is left off
here for a second reason as well: the porter's lodge is sheltered floor that is
*meant* to be unreachable, and that flag cannot be told about a room a key
opens.

**Provenance** — program
`sha256:1475b3303cb13af33f8b10dde74acb8524561decabb9e9b2d14f43ae662a0888`, seed
1, region 25×18×56. Every tuned value lives in the program's own `params`, so
the file plus the manifest row is the whole recipe and no remembered flag is
part of it.

Reproduction was taken from a **second instrument**: a separate worktree at the
same engine commit, its own cargo target tree, its own working directory, its
own copy of the program and its own output directory. Two methods, neither of
which hashes a file path — `cmp` over the bytes, and `shasum` fed from **stdin**
so no name reaches the digest. 3 of 3 files identical, both tile digests equal.

**Artifacts** — `prefabs/z2-gate-ward.x0y0z0.nbt`,
`prefabs/z2-gate-ward.x0y0z1.nbt` and `prefabs/z2-gate-ward.json` in the repo's
flat prefab library. The zone is past the 48-per-axis structure-template cap on
its long axis, so it ships as a tile set in a 1×1×2 grid and **the manifest is
the only file that describes the zone**: the gates, the render and the admission
audit all take it and treat the tiles as one thing. Review shots and what each
camera answers: `design/review/z2/`.

**Palette** — measured, never named from memory. Targets are patch means over
crops of the concept image and of `reference/map-v1-front-elevation.jpg`, taken
at the lit 90th percentile because a painting's shadow is not a block's albedo;
candidates come from `tools/block-appearance.py --near` over the measured shelf,
and every mix was read back with `--mix` before it was believed.

| Role | Mix | Measured | Sample it answers |
|---|---|---|---|
| `gate/ashlar` | `stone_bricks` 44% · `smooth_stone` 14% · `cracked_stone_bricks` 14% · `tuff` 12% · `cobblestone` 10% · `mossy_stone_bricks` 6% | `#7d7e7c` | `#84837f`, the lit face of the gate front in the front elevation. The gatehouse is the second band of the silhouette and it has to read **pale against the crag**: the two image samples stand at 2.11x in luminance and the two mixes at 1.73x, so the contrast survives the translation |
| `gate/flag` | `stone` 30% · `polished_andesite` 24% · `andesite` 18% · `polished_diorite` 10% · `cobblestone` 10% · `cobbled_deepslate` 8% | `#848585` | `#78878e`, the lit flags of the concept's passage floor — wet and cool. Dominant hue 233°, which is as blue as 1.21.11's full-cube shelf goes; there is no pale blue-grey stone in it that is not an ore |
| `gate/crag` | `cobbled_deepslate` 50% · `smooth_basalt` 30% · `blackstone` 10% · `deepslate[axis=y]` 10% | `#49484d` | `#3a3f42`, the crag in the front elevation. **Z0's `cliff/rock`, unchanged** — the rock this gate is cut into is the rock the shore stands under, and two mixes would put a seam in it |
| `gate/crenel` | `stone_bricks` 60% · `cracked_stone_bricks` 22% · `cobblestone` 18% | `#7a7a7a` | the parapet's merlons, which is the part of this zone the shore actually resolves |
| `gate/rubble` | `cobblestone` 30% · `mossy_cobblestone` 14% · `stone_bricks` 10% · `cracked_stone_bricks` 10% · `gravel` 10% · **`air` 26%** | `#7b7b77` | fallen masonry in the yard and spall on the leads. Its loudest member is 14% of area, over the 10% accent ceiling — it is 17 cells and the overrun is recorded rather than tuned away |
| `gate/leaf` | `white_carpet` 5 · `light_gray_carpet` 3 · **`air` 8** | `#c8c9c7` | the crossing-ledger's loose leaves. Half the paint is not there, which is what makes it scatter rather than carpet |
| `gate/lamp` | `lantern[hanging=false,waterlogged=false]` | `#6b5c55` | the one block in this zone that emits light |
| `gate/bar` | `iron_bars`, in the scope's own axes | `#898b88` | the portcullis and the embrasure's grate. **The colour is wrong and the reason is recorded below** |
| `gate/kerb_west` / `gate/kerb_east` | `stone_brick_stairs`, mitred, in the scope's own axes | — | the two kerbs the concept's gutter runs between |
| `gate/drum` · `gate/post` · `gate/chain` | `spruce_log` · `cobblestone_wall` · `iron_chain`, all in the scope's own axes | — | a winch is a drum on two posts with a chain off it. No vanilla block is a winch, and the beat turns on the object, so it is built out of blocks |
| `gate/ledger` | `lectern[has_book=true]`, in the scope's own axes | — | the bound ledger on its stand |
| `gate/mechanism` | `polished_blackstone` | `#353139` | the one block a campaign hangs S1's release on |

**The palette tool's binding here is 7 of 16, and the line reads as a pass.**
`block-appearance.py --program` reads a paint only when it is a string or a
list, so a paint written in the scope's own axis frame is a `dict` and is
skipped by both arms in silence. Pointed at this program it prints `binding: 7
paint(s) examined` over a program that declares sixteen roles, having missed all
nine local ones — `gate/crag` among them, which paints 13.7% of the zone. The
numbers above were therefore taken a role at a time with `--mix`.

**What each role actually writes**, measured rather than inferred from the block
census: the two are different questions, since one block serves several roles —
`stone_bricks` is in four of these mixes. Each role was rebound to a marker
block in turn and the marker counted off the expansion, which moves no
geometry. The sixteen come to 14 979 cells against 14 959 solid; the difference
is exactly the air members inside `gate/rubble` and `gate/leaf`, which is the
check that the method is reading what it thinks it is.

| Role | cells | share of the region |
|---|---|---|
| `gate/ashlar` | 10 485 | 41.6% |
| `gate/crag` | 3441 | 13.7% |
| `gate/flag` | 719 | 2.9% |
| `gate/crenel` | 194 | 0.8% |
| `gate/kerb_east` · `gate/kerb_west` | 29 · 29 | 0.1% each |
| `gate/leaf` | 24 | 0.1% |
| `gate/bar` | 21 | 0.1% |
| `gate/rubble` | 17 | 0.1% |
| `gate/post` | 8 | 0.03% |
| `gate/grate` | 6 | 0.02% |
| `gate/drum` | 2 | 0.01% |
| `gate/chain` · `gate/lamp` · `gate/ledger` · `gate/mechanism` | 1 each | — |

**Mass the player never touches is 43.6% of the zone** — 10 975 cells of the
14 959 that are solid, i.e. 73.4% of the stone. It is measured rather than
estimated: flood the air from outside the piece and from every standable cell
inside it, and a solid cell is *touched* when it is next to that air. Where it
sits: 6783 cells (26.9% of the region) are the gatehouse's own walls, piers and
vault, which is what a three-storey fortified gate block is made of; 3884
(15.4%) are the footing under every floor, which a zone must sit on; and 308
(1.2%) are the yard's ground and the causeway head's. When the §4 palette budget
lands as a diagnostic, this zone's claim has to be scoped to reachable mass or
it will be a judgement about the inside of a wall — the same risk `grammar.md`
§5c records for Z6's margin.

**The channel is dry, and that is `tide.md` rather than a simplification.** The
concept paints a running stream down the flags. The sea is one whole-world plane
and this campaign forbids both a bounded basin and a flow, so the zone paints no
water at all: it builds the gutter one course below the flags, kerbed both
sides, running out under the gate, and the plane does the rest — a dry gutter at
the ebbs, brimming at the flood. **The zone contains zero water blocks**, read
off the shipped bytes by block id rather than asserted. (Grepping the state
strings for `water` answers 95, because every bar, stair and chain carries
`waterlogged=false`; the number that means something is the one taken over block
ids.)

**Every orientation-carrying role is written in the scope's own axis frame,
and the gate that can tell says so.** Nine of the sixteen roles are
`{"local": …}` paints and 81 of the 82 fills that carry block-state properties
resolve through the scope that filled them; the one that does not is the
lantern, whose two properties name no direction.

The program this replaces wrote four bar runs as **world-frame literals**, and
at this campaign's own region that is invisible to the pinned engine: the root
asks for `z: largest`, the box is already longest along Z, so the frame is the
identity, the mismatch test short-circuits before it reads the state, and
`oriented-fills` returns `pass` over four fills it never judged. Two
instruments separate that green from a real one, and both were run.

- **The third verdict.** `oriented-fills` has a third answer, `DW0742` —
  *undecided*, which is neither a pass nor a fail and refuses nothing. Over the
  old program at 20x10x84 it reads **UNDECIDED**: 211 fills examined, 1
  resolved through a local frame, **and 4 this region cannot decide**, naming
  `gate/channel_grille_column`, `gate/grate_wall_column`, `gate/grille_column`
  and `gate/kerb_west_grille_column` and the frame request each stands under.
  Over this program at 25x18x56 it reads **pass**: 386 fills, 81 resolved
  through the local frame, nothing undecided. That verdict is 32 commits newer
  than the engine `zone-audit.yml` pins, so it was read from that engine as a
  *measurement*; the shipped bytes are the pinned engine's and the pin is not
  moved.
- **The transposed region.** At `56x18x25` the same four literals in the old
  program are refused outright with `DW0736`. This program passes there too,
  with the same 386 fills and the same 81 resolved — which is the check
  available at the pin itself.

**Open against this piece**

- **The gate front declares no exterior face, because it is shut.** A face is
  exported from an `exterior` edge's *passable* cells on the region's own plane,
  and the portcullis is not passable — so declaring the gateway as a walk out
  would either red `contract-exterior-faces` or, if the bars were moved off the
  face, red `traversable`, whose walk model knows nothing about bars. What is
  declared instead is the gate arch as its own enclosed space behind a `barred`
  edge, which is what proves S1 opens; the consequence is that **Z2 exports two
  faces, west and north, and none south**, so world assembly has nothing to mate
  the shore to at the gate. The general shape is that `traversable` and
  `contract-edge-proof` disagree about what a bar means, and only one of them is
  told.
- **The concept's ironwork is rust and this ships grey.** The concept's grate
  reads `#62544b` at its lit 90th percentile — warm brown, r > g > b.
  `iron_bars` measures `#898b88`, a neutral grey with g > r > b: the wrong hue
  family, not merely the wrong value. 1.21.11 has the block that carries it,
  `exposed_copper_bars` at `#866c59`, and the admission allowlist does not carry
  the copper **bar** family — it carries `copper_grate`, `copper_bulb` and the
  whole cut-copper family, so the omission is a list written before those blocks
  existed rather than a policy. `delve-admit audit` refuses the piece by name
  (`DW0730`) and its own message says not to bypass the list to admit an asset;
  the lever that exists, `--allowlist <file>`, *replaces* the default, which is
  the bypass rather than a fix. So the piece ships in iron and the gate is not
  weakened. Widening the allowlist to the copper bar and chain families is an
  engine change and is left where it belongs.
- **No image in the review set shows the murder-holes from underneath.** That is
  the beat's own composition — a player walking the centre line looks up — and
  the pinned renderer's eye camera is level and cannot. The openings are shown
  from above instead, from the chamber floor, and counted from the plan. The
  same limit hides the Gatewright from the yard, which is where beat 2.5 says
  the player sees him before committing.
- **The leaves are behind the grate, not across the sill.** Beat 2.4 blows them
  "out across the sill and floor"; the embrasure's sill is one course thick with
  the grate laid straight on it, so there is no cell for a leaf to lie in on the
  sill, and none reach the passage's own flags. The lodge's floor carries eight
  of them, which is what the grate frames.
- **`anchor/gateway` is inside the arch, not outside it.** It is where a body
  arriving off the flat stands once S1 is raised, and until then it is behind
  the bar — reachable only in the "with bars opened" half of the reachability
  verdict. A campaign binding an arrival to it has to know that.
- **The leads are open ground.** 21 × 33 of flags with a winch, two spall heaps
  and a parapet: that is a fight's ground rather than a room, and it is the one
  volume in this zone whose density argument rests on the elite standing in it.
  If the Gatewright is cut, the roof is a big empty space and should shrink with
  him.
- **The stair well is open to the sky over its top flight**, because the head
  landing has to be roof for a body to get out on to the leads. It reads as a
  roofed stair that becomes a trench, and nothing in the beat sheet asked for
  either.
- **`beat-audit.md` describes the program this one replaces.** Its Z2 rows state
  20×10×84, 14 404 filled cells, 655 standable, 3 of 7 beats absent and 3
  partial, and they name a boss-door bell-rope curtain, a boulder lane, a
  release stand, a blind alcove and a one-way drop shaft — none of which is in
  this file. The audit is a record of what was found and nothing in it should be
  quietly rewritten, but a reader who lands on it first will read live claims
  about a file that no longer builds any of what it describes. The same is true
  of `reconciliation.md`'s campaign-wide finding that no produced zone contains
  one block that emits light: this zone's lantern is now its second
  counter-example.
- **This zone's production record used to live in `review/z2/README.md` and now
  lives here**, where Z0's, Z1's and Z4's are. The review directory keeps what a
  review directory is for: which camera answers which question.
- **This document's own header says the engine has a third `oriented-fills`
  verdict, and the engine CI pins does not.** `DW0742` landed 32 commits after
  `zone-audit.yml`'s `GRAMMAR_REF`, so a reader who takes the header at its word
  and runs the pinned binary gets a two-valued gate and no way to tell a judged
  green from an unjudged one. Both facts are true and neither sentence carries
  the other; what the header is missing is which engine it is describing. The
  same applies to `review/z1/README.md` and `review/z2/README.md`'s old
  reproduction commands, which name a renderer flag the pinned build does not
  have.

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
