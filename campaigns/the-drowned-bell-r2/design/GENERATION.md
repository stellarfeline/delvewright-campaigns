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

**All eight zones pass every gate, and no gate withholds a verdict.** One call
judges this campaign's eight programs and the engine's 35-program rule library
together: every gate green with a non-zero binding, nothing undecided anywhere,
and one library program held to the red its record says it must fail with
(`library/causeway`, `DW0800`) rather than skipped.

`fluid-contained` binds **3728** cells, every one of them in the drowned ward —
the only zone in the campaign carrying fluid at all — each a source with nothing
open beside or below it. That water is walled at every internal boundary and
open only where it leaves the piece, because it is the sea rather than a pool.

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
it: all eight pass `oriented-fills`, every one of them carries local roles, and
the audit totals **705** fills resolved out of a scope's own frame across the set.

The pass is a **decided** one, which is a stronger claim than a green. The
pinned engine's `oriented-fills` has a third answer, `DW0742` — *this region
cannot decide it* — for a frame-sensitive state that stands in an identity frame
and is therefore never read; a two-valued gate reports those as passes and
cannot tell a judged fill from an unjudged one. Across the eight zones the gate
returns that third answer **0** times.

Z1 is the worked case for the *state*, and it shows why the frame is not
decoration: the corpse is authored as `rotation=8`, facing out of its own recess,
and lands in the world as `rotation=4`. Z7 is the worked case for the *rule* —
one wall rule builds all four faces of a tower by naming its thin axis
`smallest`, so two of the four calls run under a turned frame, and it contributes
125 of the 705 by itself.

Z0 is the other kind of case, and it is the one a green hides. Its root asks for
`z: largest` over a box already longest along Z, so the frame it stands in is the
**identity** — and a world-frame literal under an identity frame is not judged at
all, which is a different fact from being judged and found sound. The engine now
splits those two with a third verdict, *this region cannot decide it*, and the
way not to depend on which one a green means is to write the state in the scope's
own frame in the first place.

Z6 is the case that shows what the wrap costs when it is *not* needed, which is
the reason to write it anyway. Its own frame is `z(largest)` over a region whose
largest axis is world `Z`, so the frame is the identity and every local paint
resolves to itself: the wrap moves nothing. Held against the same program with
its two local roles written bare, the shipped region is **green on every gate**,
`oriented-fills` included, which reports `0` fills resolved out of a scope's own
frame and calls that a pass. Expanded into a region whose largest axis is world
`X`, the wrapped program writes the grate's bars as `east`/`west` from the one
binding, and the bare program is refused by `DW0736`. A region where the frame
happens to be the identity is therefore not evidence that a bare state is
correct — it is the one region where nothing can tell.


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
| Z0 barrow shore | `concept/z0-barrow-shore.jpg` | `programs/z0-barrow-shore.json` | **produced, awaiting owner review** — expands at 40x18x80 as a 2-tile set; declares a spatial contract, so it is judged by 15 gates where a zone without one carries 6; review set in `review/z0/` — see below |
| Z1 cliff road | `concept/z1-cliff-road.jpg` | `programs/z1-cliff-road.json` | **produced, awaiting owner review** — expands at 16x24x72 as a 2-tile set; the second zone with a spatial contract, so it is judged by 14 gates where a zone without one carries 6; review set in `review/z1/` — see below |
| Z2 gate ward | `concept/z2-gatehouse.jpg` | `programs/z2-gate-ward.json` | **produced, awaiting owner review** — expands at 25x18x56 as a 2-tile set; review set in `review/z2/` — see below |
| Z3 drowned ward | `concept/z3-drowned-ward.jpg` | `programs/z3-drowned-ward.json` | **produced, awaiting owner review** — expands at 40x10x60 and ships as 2 tiles; declares no spatial contract, so it is judged by 7 gates where a zone with one carries 16. The contract is written and is not yet in the program: it was refused at this piece's own seed by a single cell the ruin mix seals inside a pier, and the engine now computes the out-of-walk kind per cell, which is what that cell needed. Declaring it is an open authoring item; the whole account is below. Review set in `review/z3/` — see below |
| Z4 chapel ward | `concept/z4-chapel-ward.jpg` | `programs/z4-chapel-ward.json` | **produced, awaiting owner review** — expands at 27x12x33; the campaign's first zone with a spatial contract, so it is judged by 14 gates where a zone without one carries 6; review set in `review/z4/` — see below |
| Z5 hall keep | `concept/z5-hall-keep.jpg` | `programs/z5-hall-keep.json` | **produced, awaiting owner review** — expands at 11x11x76 and ships as 2 tiles; declares a spatial contract, so it is judged by 15 gates where a zone without one carries 6; review set in `review/z5/` — see below |
| Z6 cistern deep | `concept/z6-cistern-deep.jpg` | `programs/z6-cistern-deep.json` | **produced, awaiting owner review** — expands at 40x10x100 into a 3-tile set; declares a spatial contract, so it is judged by 14 gates where a zone without one carries 6 — the fifteenth is withheld by name, every cell of this building being play space; review set in `review/z6/` — see below |
| Z7 bell tower | `concept/z7-bell-tower.jpg` | `programs/z7-bell-tower.json` | **produced, awaiting owner review** — expands at 41x48x125 into a 3-tile set; declares a spatial contract at document version `1.7.0`, and its broken flight is a contingent edge, so it is judged by 15 gates where a zone without one carries 6; review set in `review/z7/` — see below |

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
`states-complete` 12, `oriented-fills` 383, `non-empty` 57600, `traversable` 2,
`contract-well-formed` 16, `contract-coverage` 2854, `contract-closure` 11408,
`contract-edge-proof` 4, `contract-no-body` 5, `contract-reachability` 2014,
`contract-anchors` 37, `contract-exterior-faces` 2, `contract-no-body-majority`
2854. 19 067 filled cells of 57 600, 12 distinct states (11 of them not air), 2854
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

- **The piece declares a spatial contract, and every contract gate passes.** Five
  spaces, five out-of-walk regions and six edges: the sand flat, the mire one
  course under it, the lamp shelf, and the two ends of the cut ledge. Bindings —
  well-formed 16, coverage 2854 with nothing left over, closure 11 408, edge
  proof 4, no-body 5, reachability 2014 (every cell of every space reached),
  anchors 37, exterior faces 2, majority 2854. The five out-of-walk regions are
  the cairn field, the mire heaps, the tide-stake tops, the crag's batter and the
  shelf coping, and each earns its kind from the blocks, computed per standable
  cell. Four are `facade` throughout — the mire heaps 100 cells, the crag's
  batter 116, the tide-stake tops 3, the shelf coping 6. The cairn field is
  `mixed`: 72 of its 615 cells are `posted`, the floor the three readable graves
  stand on, and the other 543 are `facade`.
- **The cut ledge is a CLIMB, so it is an edge and not a space.** Its five treads
  union into one transit volume, and a `via` carries no one-floor rule — that
  rule governs spaces, which is why the ledge refused as one ("standable floor at
  y 4..8, which is 5 levels"). Both ends are separately nameable because the
  program gives each its own rule: the foot has `ledge/foot_tread`, and the head
  is the recursion's own base alternative. The `stair` edge between them proves,
  rise 4, and because it is INTERIOR it never meets the rule that an `exterior`
  endpoint has no box to measure a rise against.
- **Both exterior edges name their opening, because an open-air zone cannot let
  one be discovered.** An edge with no `via` exports the whole of its space's
  cells that sit on the piece's outer layer, and both of this zone's exterior
  spaces are open to the sky: their air runs to the top of the region, so the
  region's top plane is part of them and the derivation reads it as a way out.
  Six faces came out of two edges that way: four around the sides, and two of
  open sky. No walk reaches sky, so nine of the fifteen pairs the gate examines
  were severed, and a gate asking for a walk between every pair of declared ways
  is asking for something no building can supply. The declaration is the half
  that was wrong, and the repair is the one the surface is for: `causeway/mouth`
  is the walking width of the causeway where it meets the shore, `ledge/mouth`
  is the body-height slot the cut ledge ends in, and each is claimed out of the
  air its space would otherwise hold. Faces go from six to two — `north walk` 8
  cells, `south walk` 6 — and the piece's own bytes do not move: both tiles are
  identical before and after, because naming an opening says where a body leaves
  and places no block. The flanking course of the causeway stays `flat` on
  purpose: it is what the mire beside it is closed against, and an opening taken
  all the way to the mire's edge leaves those cells excused by nothing.
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

## Z1 崖道 cliff road

**Scene** (fixed before any tool ran, per the procedure's §1): the flat ends at a
wall of cliff, and one cut ledge starts up it. A stepped flight climbs five
courses off the last dry shelf onto a road one body wide, cut into the seaward
face with the rock close on the landward hand and an open drop to the surf on the
other. A line of iron brackets is driven into the wall at head height the whole
length of it — the anchors of a rope handrail the priory stopped replacing. Where
the brackets hang bent and then stop, the shelf beyond them has gone into the
sea; the road does not cross that gap, it goes **through** the rock, in at one
cave mouth and out at the next, past the store where the handrail was kept. Past
the store the ledge resumes and runs to a wall of dressed masonry with a hole
broken in it, which is the back of the gatehouse.

**The road is a stage of the route, not a detail of the gatehouse**
(`reference/map-brief.md`). It is the only way off the sand, so the piece is
built as the whole distance between them: it is entered at the shore's own level
and left through the breach, and both ends are declared ways in rather than
region faces that happen to have floor on them.

### The six beats, and the rule that builds each

`beats.md` is what this zone must stage. A beat with no rule beside it is absent,
and none is.

| # | beat | rule(s) that build it | anchors |
|---|---|---|---|
| 1.1 | the ledge is single-file, met head-on with no room to circle | `road_plan` → `rail_band` → `rail_courses` → `deck_band` (the road's own floor, seaward edge at `sea`) + `road_walk` (`abs 1` of void between the open air and `path/rock`); the same walk course under `warn_courses`, `road_wide_courses` at the bend and `landing_courses` past the store | `shover`, `shover-watch` |
| 1.2 | a row of iron brackets at hand height — the anchors of a gone rope handrail | `road_bay` / `landing_bay` → `road_bracket_slice` → `road_bracket_row` (`iron/bracket`, one driven into the wall face every `bracket_gap + 1` cells, over every stretch of open ledge) | — |
| 1.3 | K2 the fallen ledge: the shelf has gone into the sea, round a blind bend | the tell is `warn_walk` → `warn_bay` → `bent_slice` → `bent_row` (`iron/bent`) and then three cells with no bracket at all; the bend is `bend_band` → `road_courses` under a `bind` that narrows `sea`, so the wall bulges seaward for two cells and the line goes round it; the gap itself is `store_band` → `gap_courses` → `gap_deck`, which lays no deck on the walking line | `warn-watch`, `gap-brink` |
| 1.4 | a shover — one of the answered on the ledge that puts the player over the edge | `rail_walk` → `shover_bay` → `shover_slice` / `watch_slice` for the two positions, over the one-wide lane; the recesses a body presses into are `recess_pair` / `recess_pair_corpse` → `recess_cell` (one deep, two high, two long, out of the walk); the surf's rock teeth are `gulf_band` → `tooth_floor` → `tooth_field` → `tooth_col` → `tooth_tall` / `tooth_low`, twelve courses down | `shover`, `shover-watch`, `stand-back-1..3` |
| 1.5 | the road goes *through* the rock — a rope store between two cave mouths, holding the Z1 rope | `store_band` → `mouth_a_courses` / `mouth_b_courses` → `mouth_a_walk` / `mouth_b_walk` (the two mouths, each a claimed opening in the wall face) → `gap_courses` and `room_courses` → `room_body` → `rope_col` (the rope's own cell), `rack_col` (`store/timber`) and `room_lamp_col` (`store/lamp`) | `rope`, `store-out` |
| 1.6 | the road reaches a breach in the gatehouse's outer wall | `breach_band` → `breach_courses` → `breach_hole` + `breach_head` (`wall/ashlar`, a hole two wide and two high broken through it) and `reveal_courses` → `reveal_walk` (the wall's inner reveal) | `breach` |

**6 of 6 built.** Beat 1.4 is built as far as a grammar program reaches — the
ground, the positions and the drop — and needs one campaign-level declaration to
finish: a body on `anchor/shover`. Beat 1.5 needs the rope itself on
`anchor/rope`. Neither is geometry and neither is expressible here.

**The overhang is expressible, and it is built.** The previous production of this
zone recorded that the ledge could not project over an undercut drop, because its
one lever laid the lip's course across the *whole* gulf width — so the lip's
projection and the drop's width were the same number. Re-measured at the pin, that
finding reproduces exactly on that program: at `ledge_shelf=1` the zone comes out
with 182 standable cells at `sea=3`, 226 at `sea=4` and 269 at `sea=5` against 50
shipped, and `sea=2` is refused by the plan's own guard. **The limit was in the
decomposition, not in the grammar.** The gulf and the deck are siblings of a `y`
split, so they share their other two extents by construction and each cuts `x`
with its own number: the gulf's seaward void is `sea + lip` and the deck's is
`sea`, and `lip` is a parameter of its own. Measured off the shipped bytes by a
reader that shares no code with the expander: the deck stands over open air on
**all 50** rows of open ledge, **two cells** on every one of them, with **12
courses** of open air under the outer cell.

### Every claim, measured

Taken off the two `.nbt` tiles by a hand-written structure-template reader, not
from the expander's report. It agrees with the expander on the two numbers both
produce: 14 872 filled cells and 163 standable.

| beat | the claim | measured |
|---|---|---|
| 1.1 | single-file | the open ledge is **one cell wide on 45 of its 50 rows**; the five wider rows are the breach sill and the two cells the bend turns on. The recesses are out of the walk and are 6 cells more |
| 1.2 | a row of brackets | **7 driven into the wall** (z 4, 7, 10, 13 past the store; z 52, 54, 58 on the teaching run) and **3 hanging bent** (z 39, 42, 45), then three cells with none |
| 1.3 | the shelf has gone, once | the walking line has **no floor under it in exactly one run, of 10 cells**, and floor under it everywhere else |
| 1.3 | round a blind bend | the brink is in sight from **6 cells of road and from nowhere further up-path**: the buttress cuts the sightline, so a body that has not read the wall meets the gap with about a second of road left |
| 1.5 | the rope cannot be walked past | sealing the store's two mouths and re-walking from the shore reaches **0 of the 20** standable cells on the far side, against 20 of 20 with them open |
| 1.6 | a hole in a wall | 216 cells of `wall/ashlar` across the road, with a 2 × 2 opening claimed as the way out |

**Expansion** — `delve-grammar expand --file design/programs/z1-cliff-road.json
--region 16x24x72 --seed 1`. **Fourteen gates, every one passing with a non-zero
binding**: `blocks-exist` 18, `shape-complete` 18, `states-complete` 18,
`oriented-fills` 175, `non-empty` 27 648, `contract-well-formed` 11,
`contract-coverage` 163, `contract-closure` 172, `contract-edge-proof` 3,
`contract-no-body` 2, `contract-reachability` 125, `contract-anchors` 11,
`contract-exterior-faces` 2, `contract-no-body-majority` 163. 14 872 filled cells,
18 distinct states (17 of them not air), 163 standable, 11 anchors, silhouette complexity 1.92.
`delve-admit audit` passes over 27 648 blocks (0 forbidden, 0 non-allowlisted, 0
unknown, 0 under-specified), with a per-tile verdict for both tiles.

**The zone declares a spatial contract, and that is what it is judged by.** Four
spaces (`foot`, `road`, `store`, `landing`), two out-of-walk regions (`teeth`
earning `facade`, `stand-backs` earning `posted` from the three anchors in it) and
five edges. The contract proves what a face-count cannot: that the flight really
climbs **five** courses between two spaces one floor each and connects through its
own treads; that the store is `enclosed` and its 172 boundary cells are accounted
for by its two claimed mouths and nothing else; that the way in at the shore and
the way out at the breach are **doors** rather than the standable cells of a
region face; and that all 125 standable cells in a declared space are reached from
the shore through declared edges only.

**Why the zone claims neither `traversable` nor `reachable-floor`.** Both are
weaker than the contract here and one of them is the wrong claim. `traversable`
without a contract falls back to the region's `Z` faces and counts standable cells
on them, which is the number the previous production reported as 3; with the
contract it would count the two doors the contract already proves. `reachable-floor`
turns "every roofed floor is walkable to" into a verdict, and this zone has roofed
floor that is deliberately not walkable to: the tops of the rock teeth, twelve
courses down under an overhanging ledge. Both facts are in the always-on
reachability line rather than hidden: 131 of 163 standable cells are reachable on
foot from 3 grade entry cells, and the 32 it does not reach are the teeth — 8 of
them sheltered, which is the overhang doing exactly what an overhang does.

**Provenance** — program
`sha256:017d2b4bae8652e61faee8a933b4cddbc52a39a96e39250d44b8b36f43a411c0`, seed 1,
region 16x24x72. Reproduction was checked from a **second instrument sharing no
working directory and no build tree with the first**: a separate checkout of the
pinned engine, built on its own, run from a different directory and writing to a
different one. Three methods, none of which hashes a path — `cmp` over the bytes
(4 of 4 files identical), `shasum` fed from **stdin** so no name reaches the
digest (`fd4e8644…` and `dac927ae…`, equal both ways), and a cell-by-cell
comparison through the hand-written reader (**27 648 of 27 648 equal, 0
differing**), with the 11 anchors and the resolved contract equal object for
object. The two release builds of the pinned commit are themselves byte-identical.

**Artifacts** — `prefabs/z1-cliff-road.x0y0z0.nbt`,
`prefabs/z1-cliff-road.x0y0z1.nbt` and `prefabs/z1-cliff-road.json` in the repo's
flat prefab library. The zone is past the 48-per-axis structure-template cap on
its long axis, so it ships as a tile set in a 1×1×2 grid and **the manifest is the
only file that describes the zone**: the gates, the render and the admission audit
all take it and treat the tiles as one thing. Review shots and what each camera
answers: `design/review/z1/`.

**Palette** — measured from the concept image, never named from memory. Material
colours are patch means over crops, and every crop was drawn back onto the image
and looked at before it was used. The near cliff measures as a near-neutral dark
grey of very wide value range (`#494e51`, luminance p05 53 and p95 111 out of
255), which is a *mix* rather than a block: bound to one block the face reads as a
flat panel that no measurement of the mean would object to.

| Role | Mix | Measured | Concept sample |
|---|---|---|---|
| `crag` | `cobbled_deepslate` 50% · `smooth_basalt` 30% · `blackstone` 10% · `deepslate[axis=y]` 10% | `#49484d` | `#494e51` the untouched sea-cliff mass. Z0's `cliff/rock` unchanged — Z0's crag and this cliff are the same rock, and two mixes would put a seam in it |
| `path/rock` | `cobbled_deepslate` 60% · `deepslate[axis=y]` 20% · `tuff` 10% · `blackstone` 10% | `#4e4e50` | `#454541` the cut ledge and `#494a45` its wall — same rock, a shade lighter and drier where it is worked. Z0's `ledge/rock` unchanged |
| `wall/ashlar` | `tuff_bricks` 40% · `polished_tuff` 20% · `cracked_stone_bricks` 15% · `deepslate_bricks` 15% · `mossy_stone_bricks` 10% | `#636661` | `#5c5f5d` the gatehouse's broken wall-head in `concept/z2-gatehouse.jpg`, p05 33 p95 139 — dressed stone, and the only thing on this road that was built rather than cut |
| `teeth/rock` | `cobbled_deepslate` 40% · `smooth_basalt` 25% · `blackstone` 20% · `deepslate[axis=y]` 15% | `#464549` | `#677174` the dark rock standing in the surf, bottom-left of frame. The sample is contaminated by foam (p95 209), so the mix is bound darker than the mean and to the same family as the cliff it fell off |
| `iron/bracket` | `lightning_rod[facing=west,…]` | `#c56f53` | the line of rusted pitons in the rock face — see below |
| `iron/bent` | `lightning_rod[facing=down,…]` | `#c56f53` | the same bracket, bent down |
| `store/timber` | `dark_oak_wood[axis=z]` 55% · `dark_oak_log[axis=z]` 30% · `muddy_mangrove_roots[axis=z]` 15% | `#3f301d` | the rack the handrail was kept on |
| `store/lamp` | `lantern[hanging=true,waterlogged=false]` | `#6b5c55` | — |
| `path/corpse` | `skeleton_skull[powered=false,rotation=8]` | `#513e33` | the remains in one wall recess |

The loudest member of every stone mix holds 20% of the area or less and none of
them is chromatic at all (`chromatic_area 0.00` on all four), which is the craft
rule the numbers serve. `store/timber` is the exception and is stated rather than
hidden: 85% chromatic area, because dark oak is, and it is 4 cells of 14 872.

**The ironwork is admitted, and the divergence is a hue family.** The concept's
brackets and rings measure warm and dark — five tight crops over the pitons give
`#3d3b37`, `#34322e`, `#44413c`, `#383733` and `#2d2b27`, hue 36–46°, saturation
22–32 out of 255. Of the blocks the admission allowlist permits, the bar is
`iron_bars` at `#898b88` — hue 120°, saturation 6, which is not a dark warm iron
but a neutral grey — and the chain is `iron_chain` at `#333a4a`, hue 222°, the
right value and a **cool** family. The block that is the right family, 1.21.11's
`copper_bars` at `#9c5137`, is **not in the allowlist**, which was written before
that block existed. Nothing here was weakened to get round it. What this zone
ships instead is `lightning_rod` — allowlisted, `#c56f53`, hue 15°, the right
family and lighter than the concept's value — because the element beat 1.2 needs
is a **rod driven into a wall**, not a bar, and for a rod the warm family is
reachable inside the allowlist even though for a bar it is not. Two states of one
block carry the whole tell: `facing=west` is a bracket driven in, `facing=down` is
one bent down. It is brighter than the rock it is set into, and that is the half
of the substitution worth arguing with — but beat 1.2 says the brackets are the
zone's only navigation aid and its only warning, and a tell that cannot be seen at
walking distance is not one. In `review/z1/ext-nw.png` they are the only thing on
the face besides the road.

**The palette tool reports no binding at all over this program, and the output
reads like a measurement.** `block-appearance.py --program` over this file prints
**the whole block registry** and no `binding:` line, because every paint here is
written in the scope's own axis frame: a `local` paint is a `dict`, both of the
tool's arms want a string or a list, and neither says so. The count is **0 of 9**
and it does not appear. Handing the nine to `--mix` does not recover them either —
the flag splits its argument on `=`, so a block state with a property in it is
refused (`'y]=10' is not a weight`). **The real binding for the table above is 9 of
9 roles**, taken through `--mix` with the states' properties stripped, which
measures the block's own texture and is the right number for a colour anyway. Both
halves are stated here so the shortfall is not carried forward as a pass. Z4's
record found the same tool reporting 8 of 18; over a palette that is entirely
`local` the same defect reports nothing whatever.

**Every orientation-carrying role is written in the scope's own axis frame, and
this region cannot decide whether that mattered.** `oriented-fills` reports 175
fills examined, 171 carrying block-state properties, and **171 of those 171
resolved out of the scope's own frame** — there is no world-frame literal left for
the gate to bite on, which is the strongest form the claim has. It is worth being
plain about why it was worth making: this zone's outermost frame asks for
`z: largest` over a box already longest along `Z`, so the frame it stands in is the
**identity**, and a world-frame literal under an identity frame is licensed by the
gate and lands correctly at this region and wrongly at any other. A green on that
branch would have proved nothing. What does prove something is the recesses: each
is entered through a `reorient` that names the across-path axis as local `Z`, a
real transposition, and the corpse authored as `rotation=8` lands in the world as
`rotation=4`.

**The seed moves texture and nothing else.** This program makes no seeded choice
of geometry anywhere: every alternative is selected by a guard, and the only draws
from the stream are per-cell paint draws inside a mix. That is what makes a role
rebind a measurement rather than a perturbation — a rebind changes how many values
are drawn, and a program whose geometry depended on the draw would move under it.
It also means there is no seed to reroll: at any seed this is the same building.

**How much of this is mass nobody touches.** Measured by rebinding each role in
turn to a marker block and counting the marker, which is the only way to ask the
question — one block serves several roles, so a block census cannot answer it. The
measurement variant has the contract and its claims stripped so a rebind that
changes passability cannot be refused by a contract gate, and the run asserts what
that costs: **27 648 of 27 648 cells identical to the shipped model**, because a
claim writes no blocks. The nine roles come to 14 872 cells exactly and their
union is 14 872, i.e. they partition the filled zone, which is the check that the
method is reading what it thinks it is.

| Role | cells | share of filled |
|---|---|---|
| `crag` | 12 731 | 85.6% |
| `path/rock` | 1 860 | 12.5% |
| `wall/ashlar` | 216 | 1.45% |
| `teeth/rock` | 48 | 0.32% |
| `iron/bracket` | 7 | 0.05% |
| `store/timber` | 4 | 0.03% |
| `iron/bent` | 3 | 0.02% |
| `path/corpse` | 2 | 0.01% |
| `store/lamp` | 1 | 0.01% |

Read geometrically rather than by role, **9 901 cells — 66.6% of the filled zone —
have no air beside them and no face on the region's own outside**: mass nothing
can look at. The number was taken twice by unrelated means, once by scanning for a
passable neighbour and once by counting the complement, and both give 9 901. It
sits between Z0's 78.0% and Z4's 33.6%, and the reason is the same as Z0's: **this
zone is a line cut across a face, and what surrounds the line is rock rather than
enclosed air.** The rule the number serves is about volume a player is charged a
walk across, and by that reading this piece encloses almost nothing — 163
standable cells in all, of which the store is 45 and every other one is on a ledge
one body wide.

**Open against this piece**

- **The store is the only lit thing in the campaign, and it is one lantern.** No
  other zone of this campaign exposes a light-emitting role, and the reconciliation
  records that as a campaign-wide omission. This zone adds one, because the store
  is roofed rock fourteen cells long on the critical path holding a carried key
  item, and a room a player has to enter and cannot see is a defect the machine
  gates do not name. It is a deliberate addition beyond what any beat asks for, and
  it is one cell of 14 872.
- **`delve-admit lighting` cannot measure a tiled zone, and does not say so.**
  Handed the manifest it fails with `DW0732 gzip decode: invalid gzip header`,
  having tried to read the JSON as NBT. Handed one tile of the set it returns a
  verdict — `profile: dark`, 119 floor cells, min light 0 — over 48 of the zone's
  72 blocks of length, with no indication that it is looking at part of a zone.
  `delve-admit audit` refuses that same lone tile by name and points at the
  manifest, and so does `delve-render`; the guard exists in two of the three doors.
  So no lighting profile was written and the metadata still says
  `"profile": "unmeasured"`, which is a positive statement that a measurement is
  owed rather than a missing field. This is the second zone to hit it; Z0 recorded
  it first.
- **The number would be wrong here in a second way even if it could be taken.**
  98 of this zone's 163 standable cells are open to the sky. An open cliff road at
  noon reports `dark`.
- **The surf is not in this piece.** Beat 1.4's named image element is surf *and*
  rock teeth below the path; the teeth are built and the surf is the tide plane,
  which `tide.md` fixes as one moving sea the assembled world carries. A basin of
  water inside a piece open on three faces is a body of water with no walls, which
  is the shape of the campaign's one open machine finding on Z3, so this zone
  places none and says so rather than shipping a pond twelve courses down.
- **The teeth read as blocks rather than as spurs.** They are two-cell and
  one-cell stacks standing off the cliff's foot in a repeat, so at the distance the
  exterior orbits look from they are a rhythm of nubs. What they have to do — give
  the drop a bottom that is not flat, and give the overhang something to be over —
  they do; what they do not have is a silhouette that would survive being looked at
  from the sea.
- **The reference draws a chain still hanging between the first brackets, and this
  zone does not build one.** `reference/map-v2-west-elevation.jpg` draws the
  bracket line with a sagging rail over its southern third and bare posts after it;
  `beats.md` 1.2 says the handrail is "long gone" and the brackets are its anchors.
  The zone follows the beat sheet, and the divergence is named here rather than
  quietly split. Building the surviving stretch is one rule and is not hard; it was
  not done because a rail on the first third would give the road a second gradient
  competing with the sound → bent → gone one that beat 1.3's tell is read from.
- **The recesses are declared out of the walk, and that is a reading of them.**
  `contract-coverage` needs every standable cell accounted for, and a recess is
  roofed by the cliff over it, so a recess claimed as part of an `open` road is a
  roofed cell in a space that says it has no roof. They are declared as an
  out-of-walk region instead, which earns `posted` from the three anchors in them
  and is right for an ambusher's station — but a player who steps back into one to
  survive a shove is standing in a cell the contract says no body goes to. The
  distinction the checker can draw is roofed or not; the distinction the beat wants
  is *whose* body.
- **No standpoint in this piece can frame a recess.** It is one cell deep off a
  lane one cell wide, so a camera in the lane is half a block from the wall it is
  photographing. `review/z1/eye-recess_look.png` is the shot that shows why, and
  the measurement is what answers the question instead.
- **`beat-audit.md` describes the program this one replaces.** It is the document
  that found four of this zone's six beats absent, and every Z1 row in it is about
  a 10x28x44 expansion with 5490 filled cells, 7 block states, 50 standable cells,
  12 anchors and no ironwork. It states the ledge's want of an overhang as a
  property of the grammar, which this piece refutes with its own numbers. The audit
  is a record of what was found and nothing in it should be quietly rewritten — but
  a reader who lands on it first will read live claims about a file that no longer
  builds any of what it describes.
- **`review/z1/README.md`'s predecessor documented cameras the pinned renderer
  cannot produce** — an author-aimed `--view` flag it does not have, and a global
  option placed before the subcommand. It has been replaced rather than extended,
  and every camera in the new one was run at the pin before it was written down.

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
| 2.4 | **G1 the guardroom**: a grated embrasure, ledger leaves on the sill and floor, the bound ledger inside | `lodge/band` → `lodge/room` → `lodge/air` → `lodge/fitout` → `lodge/litter` → `lodge/desk`; the embrasure is `lodge/face` → `lodge/embrasure` → `lodge/sill` + `lodge/grate` → `lodge/grate_leaf`. The lodge is declared **out of the walk** and earns the `sealed` kind | `ledger` (east), `embrasure` (west) |
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
is declared out of the walk and earns `sealed` — 25 standable cells, the air
each of them stands in closed by this piece's own blocks and lying wholly inside
the declared out-of-walk cells — rather than being a room that happens to have
no door. The kind is computed per cell and strongest first, so `sealed` is what
these cells earn on the blocks and neither the ledger nor the embrasure anchor
posts any of them; the enumeration names both, and every gate passes. That is
the stronger of the two readings: `posted` is a kind an author secures by
placing something, and `sealed` is one the masonry has to supply.

**The stair is beside the route, measured rather than argued.** Cut its doorway
column (56 standable cells at `x = 16`) and the breach face still reaches the
causeway head; the stair well is then unreachable, and the zone still crosses.
Taken from the shipped bytes by the second instrument, not from the expander.

**Expansion** — `delve-grammar expand --file design/programs/z2-gate-ward.json
--region 25x18x56 --seed 1 --traversable --allow-falls --id z2-gate-ward -o
out/`. **Sixteen gates, every one passing with a non-zero binding**:
`blocks-exist` 28, `shape-complete` 28, `states-complete` 28, `oriented-fills`
386, `stair-shape` 58, `non-empty` 25200, `traversable` **2 declared ways in or
out** (not face cells — the piece declares a contract), `contract-well-formed` 16,
`contract-coverage` 1787, `contract-closure` 3714, `contract-edge-proof` 6,
`contract-no-body` 2, `contract-reachability` 1690, `contract-anchors` 17,
`contract-exterior-faces` 2, `contract-no-body-majority` 1787. `stair-shape` is
the zone's alone: no other program in the campaign writes a stair. 14 959 filled
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
at this campaign's own region that is invisible to a two-valued
`oriented-fills`: the root asks for `z: largest`, the box is already longest
along Z, so the frame is the identity, the mismatch test short-circuits before
it reads the state, and the gate returns `pass` over four fills it never judged.
Two instruments separate that green from a real one, and both were run.

- **The third verdict.** `oriented-fills` has a third answer, `DW0742` —
  *undecided*, which is neither a pass nor a fail and refuses nothing. Over the
  old program at 20x10x84 it reads **UNDECIDED**: 211 fills examined, 1
  resolved through a local frame, **and 4 this region cannot decide**, naming
  `gate/channel_grille_column`, `gate/grate_wall_column`, `gate/grille_column`
  and `gate/kerb_west_grille_column` and the frame request each stands under.
  Over this program at 25x18x56 it reads **pass**: 386 fills, 81 resolved
  through the local frame, nothing undecided. `zone-audit.yml` pins an engine
  that carries this verdict, so the campaign's own CI reads a decided pass here
  rather than a two-valued green. The shipped bytes are indifferent to which of
  the two engines writes them: every `.nbt` and every manifest of all eight
  zones is byte-identical across that pin, and only the gate reports differ.
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
- **The third `oriented-fills` verdict this document's header describes is the
  one the pinned engine has.** `DW0742` is what separates a judged green from an
  unjudged one, and `zone-audit.yml`'s `GRAMMAR_REF` names an engine carrying
  it, so a reader who takes the header at its word and runs the pinned binary
  gets the gate the header describes. `review/z1/README.md` and
  `review/z2/README.md`'s old reproduction commands are a separate matter: they
  name a renderer flag the pinned build does not have.

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
`oriented-fills` 296, `fluid-contained` 3728, `non-empty` 24000, `traversable`
72 (32 standable cells at the approach face, 40 at the exit face). 9036 filled
cells of 24000, 20 distinct states, 2695 standable, 28 anchors, silhouette
complexity 1.02. `delve-admit
audit` passes over 24000 blocks (0 forbidden, 0 non-allowlisted, 0 unknown, 0
under-specified). The zone is past the 48-per-axis cap, so it ships as 2 tiles
and one manifest, and has no lighting step: the profile is `unmeasured`.

**The water, and the instruments that establish it.** Two methods whose failure
modes are unrelated agree to the cell: `fluid-contained` at expansion, and a
reader of the shipped `.nbt` palettes and block lists that shares nothing with
the expander but the bytes on disk. Both say **3728 fluid cells, every one a
source, none with an open cell beside or below it, and 0 internal escapes.** 344
run directions leave the piece's own outer faces and are counted rather than
judged — what is beyond a face is not in these bytes, and here what is beyond
them is the sea, so whatever this zone is placed against decides where that
water goes. Below the waterline the zone holds no air at all, which is
`tide.md`'s rule stated as a property of the blocks rather than as an intention.

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
  writes `None` unconditionally — at both of its export sites, and still at the
  engine revision the zone audit pins — so a zone whose water *is* the campaign's
  tide plane cannot state where that plane sits from its own program. No program
  field and no flag reaches it. It is 2 in this piece's local frame. Hand-editing it into the metadata was not done: it would
  make the byte-reproduction claim above false. This is a missing engine surface,
  not a defect in the zone.
- **The two runs are nameable apart today, and the record that said otherwise was
  wrong.** Both the ruined twin of the arcade rule chain and the `include`
  restructure — lifting the run into its own document and composing it twice
  under an `east/` and a `west/` prefix — are withdrawn. `bind` is what already
  tells the two runs apart: the west call site rebinds three palette roles to
  `ruin/*`, and a `bind` carries **parameters** as well as roles. So one
  parameter pushed from that same call site, read by a rule whose two
  alternatives are guarded on it, chooses the region literal — the intact run's
  deck void claims `arcade/walk`, the ruined run's claims `arcade/ruin` — and the
  geometry stays in one place, where nothing can drift out of step. It is
  `bar_or_open`'s idiom, which this program already uses for the barred door,
  applied to a claim. A region name being a literal was never the obstacle:
  nothing requires a rule to reach a literal by only one path.
- **The five-level refusal was about the wrong box, not about the name.**
  "standable floor at y 3..7, which is 5 levels" is what a claim at the CALL SITE
  earns, and it earns it on the intact run as readily as the ruined one: an
  arcade column carries two floors five courses apart — the water surface inside
  the arches at y 3, and the deck walk at y 7. A space is the walked volume, so
  the claim belongs on the void course over the deck (`arcade_pier` and
  `arcade_bay`'s last child, y 7..9), where the intact run measures one floor and
  180 standable cells and `contract-well-formed` passes. Two mistakes were being
  read as one, and only the second was real.
- **The ward is not a walked space, and the claim that it is two is withdrawn.**
  `nav`'s `standable` calls any non-air cell a floor, so this zone's sea reads as
  1888 cells of walkable ground at y 3, and a contract declaring them a space —
  `ward/water` `open_top` beside an `enclosed` `ward/arches` — would go green
  while being false. That is the capability the audit's exclusions record already
  names against `library/causeway`, arriving here by the door that record
  predicted: the library rule floods to the ceiling *so that* its flanks are
  unwalkable and is red on containment for it; this zone took the repair that
  record calls the only one keeping the design, holds its water two courses deep
  and fully contained, and inherited the misreading in exchange. What is true is
  the sentence the zone was written around — the spine is walkable at the
  standing tide and the ward is not. So the whole water surface is ONE
  out-of-walk region, `ward/tide`, earning `facade` because the sea outside the
  piece reaches every cell of it, and the piece says it is mostly out of walk
  over an acknowledgement whose majority is `facade` and holds no `posted` cell.
- **The contract that follows is written, and this piece's own seed refuses it by
  one cell.** Four spaces, two out-of-walk regions, six edges, three transit
  volumes and a bar:

  | element | kind | claimed at |
  |---|---|---|
  | `causeway` | space, `open_top`, the entry | `causeway_over`, under a `y` split that keeps the top course out so the piece's up face is not a way in |
  | `arcade/walk` | space, `open_top` | the intact run's deck void |
  | `tower/hall` | space, `enclosed` | `ground_room` |
  | `tower/upper` | space, `enclosed` | `upper_room` |
  | `ward/tide` | out-of-walk, `facade` | `open_water`, `wreck_hull`, `plinth_water`, `arch_void`, and the oversail gap beside `ground_room` |
  | `arcade/ruin` | out-of-walk, `facade` | the ruined run's pier stone, deck course and deck void |
  | `crossing` | transit volume | `crossing_ramp` — the treads belong to the edge |
  | `tower/well` | transit volume | `midfloor_well` |
  | `tower/shutter-way` | transit volume | the opening in `upper_east_wall` |
  | `shortcut/s2-bar` | bar | `bar_or_open`, both arms |

  The edges are `exterior`–`causeway` walk, `causeway`–`arcade/walk` stair rise 3
  via `crossing`, `arcade/walk`–`tower/upper` walk via `tower/shutter-way`,
  `tower/hall`–`tower/upper` stair rise 3 via `tower/well`,
  `causeway`–`tower/hall` barred on `shortcut/s2-bar`, and `tower/hall`–
  `exterior` walk. Declaring it costs the building nothing: five rules of
  indirection and one `ruined` parameter defaulting to 0 leave both `.nbt` tiles
  and all 28 anchors byte-identical, checked by content hash and again by `cmp`.
  At a seed it is admitted at, every gate binds and passes —
  `contract-well-formed` 12, `contract-coverage` 2698, `contract-closure` 2096,
  `contract-edge-proof` 4, `contract-no-body` 2, `contract-reachability` 647,
  `contract-anchors` 28, `contract-exterior-faces` 2 and
  `contract-no-body-majority` 2698 — and the zone is judged by 16 gates where
  undeclared it is judged by 7, which is half what every other zone of this
  campaign is held to.
- **Seed 1 is the seed that refuses, and one cell is why.** Swept over sixteen
  seeds the contract is green at fifteen; the exception is the seed this piece
  ships at. `ruin/pier_stone` carries 15% air, and at this roll it seals a
  two-cell void inside the last pier of the ruined run, the lower cell of which
  (x11 y3 z58) a body could stand in. `arcade/ruin` then qualifies for nothing:
  `facade` asks that the air outside the piece reach every standable cell the
  region holds, and this one it does not reach; `sealed` asks that the region's
  own boundary be closed, and a pier standing in open water has no closed
  boundary at any box a rule can claim. Both demands are right and the cell meets
  neither. Rerolling is not a repair and was not taken — the sweep is a
  measurement of how the mix behaves, not a search for a green seed.
- **What that cell needed was a kind of its own, and the kind now belongs to the
  cell rather than to the region — the engine repair has landed and this zone is
  the one waiting on it.** `contract-no-body` used to compute one verdict per
  region, so a region holding 159 standable cells the outside air reaches and one
  it does not had no honest label although every cell in it had one. The property
  the sealed cell earns — *the piece's own blocks enclose it from the air outside
  the piece* — is a fact about the blocks, is already computed for `facade`, and
  is not one stranding can supply: floor that is merely unreachable but open to
  the sky is reached by that air and fails it. The gate now asks each demand of
  the standable cell, strongest first, and `sealed` per cell demands that the
  cell's whole passable component lie inside the declared out-of-walk cells and
  touch no cell of the model's outer layer — which is what a void the masonry
  closes meets and what stranding still cannot buy. Two regions elsewhere in this
  campaign re-verdicted under it with no artifact and no gate moving: Z0's cairn
  field, and Z2's lodge. So this zone's remaining work is the campaign's rather
  than the engine's: the contract tabled above is written, is not in the program,
  and declaring it is an open authoring item to be re-measured at the seed the
  piece ships at — not a wait. The alternative repair, a ruin eroded from its
  faces instead of mixed with air through its mass, is a change to what the zone
  builds and is not needed for the declaration to be admissible.
- **The head-to-floor rise is already a param, and the record that said otherwise
  was wrong.** It is `$water_depth + $quay_h`, and an exhaustive scan for
  param-free arithmetic finds only anchor-centring on X anywhere in the program.
  What the zone lacks is a *named datum* a composer can set: the offset is an
  emergent sum of two block thicknesses, retunable only by shallowing the sea or
  deleting the quay course. The written 1.9 is unreachable either way, because
  every rise in this grammar is an integer.
- Lighting is `unmeasured` and cannot be otherwise: `delve-admit lighting` takes
  one structure template and refuses a tile set, and running it on a single tile
  would write a second metadata document describing one slice of a building. No
  rule here exposes a light-emitting role, so light arrives as campaign-bound
  content on the declared anchors.
- 158 standable cells are unreachable but open to the sky: the ruined run's deck,
  which is scenery and is meant to have no way up. They are `arcade/ruin`'s
  `facade` cells, and being open to the sky is exactly what earns them that kind.
- `anchor/tower-gate` renders as an empty frame. It faces out of the exit face,
  so what it is about lives in the assembled world; it is kept in the review set
  rather than dropped so the gap is visible.

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
- **The piece declares a spatial contract.** Seven spaces, three out-of-walk
  regions and eight edges: the chain of rooms on one floor — hall, door
  threshold, stores, gallery, motif threshold — and the dumbwaiter duct down to
  the cistern, an entry floor and a landing four courses under it joined by a
  `drop`. `traversable` now binds 2 declared ways rather than 18 standable cells
  on two region faces. The bait perch and the two truss corbels earn `posted`;
  the roof timbers earn `facade`, every one of their 28 standable cells reached
  by the air over the piece's open top. `duct/drop` is the datum a composing
  whole binds, and the declared rise guards it: moved to 3, expansion refuses
  naming both numbers.
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

## Z6 cistern deep

**Scene** (fixed before any tool ran, per the procedure's §1): the player comes
out of a low duct high in the end wall and drops three courses into a brick
barrel vault that is the largest interior in the delve — a nave ranked by
transverse arches, an arcade down one side into a lower aisle, and one break in
the crown. Under the break a ridge of fallen vault is climbable terrain; across
the floor a supply channel is cut three courses down, spanning nave and aisle,
crossed only on the arcade's own continuous footing. In the aisle wall a hole is
smashed through to the ward beyond and barred. At the deep end, where the vault
ends in a wall, a dressed apron ring sinks two steps to a silt bed.

The zone is entered by falling and left through the hole in its side; the walk it
claims is duct to deep end, and `--allow-falls` is the entry.

**This program is not the engine export.** The exported one composed the staging
vocabulary — a drop shaft, a watch bay, a broken grate, an open arena, a junction
and a sealed door — and it passed every gate it was given, but it built a
nineteen-wide lane beside a twenty-one-wide slab of inert rock and none of the
scene: no vault, no piers, no break, no channel, no well. Two fifths of its
blocks were `margin` a body never sees, its interiors were three courses high
under six of solid mass, and six of the seven beats had no rule in it at all. It
was replaced by a program written against this zone's own concept and beats. What
survives is the shape of the plan — one run of named segments with a side strip
— and the id.

**Expansion** — `delve-grammar expand --file
design/programs/z6-cistern-deep.json --region 40x10x100 --seed 1 --traversable
--allow-falls --id z6-cistern-deep`. Every gate passes with a non-zero binding:
`blocks-exist` 12, `shape-complete` 12, `states-complete` 12, `oriented-fills`
527, `non-empty` 40000, `traversable` 2 (the two declared ways in or out — the
duct and the aisle's last arch — with a walk, falls allowed, between them),
`contract-well-formed` 13, `contract-coverage` 3168, `contract-closure` 9311,
`contract-edge-proof` 5, `contract-reachability` 3168, `contract-anchors` 14,
`contract-exterior-faces` 2, `contract-no-body-majority` 3168. 26463 filled
cells of 40000,
12 distinct states, 3168 standable, silhouette complexity 1.11, 14 anchors.
Reachability 3076 of 3168 standable cells (97.1%) from 8 grade entry cells, in 3
pockets, each of which is a design and is named below. `delve-admit audit` passes
over 40000 blocks across the 3 tiles (0 forbidden, 0 non-allowlisted, 0 unknown,
0 pre-pin unknown, 0 under-specified, no findings).

100 is past the 48-per-axis structure-template cap, so the zone ships as **three
tiles in a 1x1x3 grid plus a manifest**; `prefabs/z6-cistern-deep.json` is the
manifest and is the only file that describes the zone. Per the procedure's §7 a
tiled zone has no `lighting` step — `socket`, `anchor` and `lighting` take one
template and refuse a manifest — so this piece carries `"profile": "unmeasured"`
and means it.

**Provenance** — program
`sha256:104d2ccaf8372410db42f77aa6d2f6df44c8f7ab3b8b658c980f12b38f5f74b6`, seed
1, region 40x10x100. The hash is over the effective program, and it binds: the
same expansion with `--param hole=9` reports
`sha256:d60f6d00e5a84555a73e7e9b54a6e26fc5b8b189ca8f6618382d4fe7acd09416`, so a
matching hash is a statement about what was expanded and not only about which
file was named.

Reproduction is **verified by two methods whose configuration is not shared**,
because hashing a listing of `shasum` output hashes the file paths as well as the
bytes and would call two output directories different when nothing is. First: a
second expansion run from a different working directory through a relative input
path, compared with `cmp` — a byte comparator that never sees a name — giving 3
of 3 tiles and the manifest byte-identical. Second: an independent NBT reader
assembles both expansions into full 40x10x100 grids and compares cell by cell —
**40000 cells examined, 0 differing**, anchors and provenance row equal, and its
own count of filled cells (26463) equals the expander's.

**Artifacts** — `prefabs/z6-cistern-deep.json` (the manifest) +
`prefabs/z6-cistern-deep.x0y0z{0,1,2}.nbt`; review shots and what each camera
did in `design/review/z6/`.

**Palette** — measured, never named from memory. The concept image is a lit
render, so its patch means are the scene's darkness rather than the material: the
masonry crops mean `#272a2d` and the same pixels' lit decile means `#3e4345`,
over a value range of p05 20 to p95 70 at a saturation of 6 out of 255. A
near-neutral colour of that range is a **mix** and not a block — bound to one
block the vault reads as a flat panel — and the number the mixes are matched
against is the lit decile, because the only material fact in a rendered scene is
what the key light reaches.

| Role | Mix | Mix mean | Concept sample |
|---|---|---|---|
| `vault` | `deepslate_bricks` 50% · `cracked_deepslate_bricks` 20% · `deepslate_tiles` 20% · `chiseled_deepslate` 10% | `#414141` | `#3e4345` the lit masonry of crown and wall |
| `pier` | `polished_deepslate` 50% · `deepslate_bricks` 30% · `cobbled_deepslate` 10% · `chiseled_deepslate` 10% | `#464747` | `#4c5051` the lit rib — the same rock, worked smoother |
| `floor` | `deepslate_tiles` 50% · `cracked_deepslate_tiles` 30% · `cobbled_deepslate` 10% · `chiseled_deepslate` 10% | `#383839` | `#2e3234` the lit band of the water, which is what the floor is seen through |
| `render` | `deepslate[axis=y]` 50% · `polished_deepslate` 20% · `cobbled_deepslate` 20% · `basalt[axis=y]` 10% | `#505052` | `#4b5356` the pale broken face around the breach — lighter and cooler than the brick, and the highest saturation in the image |
| `rubble` | `cobbled_deepslate` 45% · `cracked_deepslate_bricks` 25% · `deepslate_tiles` 10% · `chiseled_deepslate` 10% · `air` 10% | `#454547` | fallen vault; a tenth of the paint is not there, which is what makes it rubble rather than a block of stone |
| `silt` | `mud` 60% · `cracked_deepslate_tiles` 30% · `deepslate_tiles` 10% | `#39383a` | not in the image — the bed is under water in every frame of it. Read as the cistern's own paving with fifty-one years over it |
| `grate` | `iron_bars`, local | `#898b88` | `#535a5c` the lit ironwork of the grille |

Two decisions the measurement made rather than confirmed. The first shortlist put
`polished_blackstone` and `polished_blackstone_bricks` in the vault, floor and
rubble as the loud member at the craft rule's 10%; both are warm-purple
(dominant hue 314 degrees) while every crop of the concept is cool — blue above
red in the lit decile of all four materials. They were swapped for
`chiseled_deepslate`, which is loud in value and neutral in hue, and the swatch
sheet is what settled it. The second was silt: the first mix carried `clay`,
which tiles as near-white blotches and reads as nothing the fiction has.

**Every role that carries a direction is written in the scope's own axis frame.**
`render` (through `deepslate` and `basalt`, both of which carry `axis`) and
`grate` are `{"local": …}` paints; `oriented-fills` reports 2 of 2
orientation-carrying fills resolved that way. Why this matters here even though
it changes nothing here is in the section above.

**Every beat has a rule.** `design/beats.md` §Z6, in order:

| beat | the rules that build it |
|---|---|
| 6.1 the ranked vault, ankle-deep | `deep_plan` (a 22-wide nave, a 2-wide arcade and a 12-wide aisle across 40), `bay_section` · `vault_head` · `vault_haunch` (the section), `ranked_run` · `pier_slab` · `pier_jamb` · `pier_arch` · `pier_head` · `pier_shoulder` (the transverse arches), `arcade_run` · `arcade_pier` (the second rank line). The water is not authored — see below. |
| 6.2 the daylight shaft through a collapse | `sky_crown` (the break and its rubble lip), `cone_side` (the vault gone to rubble around it), `rubble_ridge` · `ridge_step` · `ridge_cap` (the debris as climbable terrain), `cone_nave` · `cone_head` · `cone_run` · `cone_slot` |
| 6.3 K5, the supply channel | `chan_seg` · `chan_trench` · `trench_bay` · `trench_aisle` (the cut, three courses into a four-course sub-floor, spanning nave and aisle), and `bay_section` in the arcade lane, which is the crossing |
| 6.4 the Choir's side vault | `choir_seg` · `choir_aisle` · `choir_pair` · `choir_bay` (the vault), `choir_arcade` (the wide opening it is heard through), `choir_watch_bay` (the cell it is counted from) |
| 6.5 the Founder and the well head | `well_seg` · `well_end` · `well_nave` · `well_floor` · `apron_row` · `apron_slab` · `well_row` (the dressed apron), `well_shaft` · `well_step` · `well_pit` (the mouth), `well_jamb_band` (`anchor/founder`, `anchor/well`) |
| 6.6 the tongue in the silt | `well_pit`'s `silt` course and `anchor/tongue` on the bed above it |
| 6.7 S4, the grille | `breach_wall` · `breach_section` · `breach_opening` · `breach_mouth` · `grate_leaf` |

**The sea is the campaign's, and this piece authors none of it.** `design/tide.md`
is the design of record: one world-wide plane, no bounded basin, every wet volume
solid water, no flow. A cistern is the zone most likely to want a basin and this
one has none — the geometry is dry and the plane arrives from outside it, which
is the only construction that cannot re-flood from its own edges. What the piece
owes the tide is the **ordering of three heights**, and it carries it: the floor
is the top of a four-course sub-floor; the well's bed is one course above the
region's floor and the channel's bed is on it, so the channel's invert is one
course lower than the well's. That is the whole of the two rows `tide.md` says
carry the design — at the Dead Ebb the channel still holds water and the well's
silt clears the plane. Both cuts are open to the room above, so nothing under the
plane is a trapped pocket.

**Open against this piece**

- **The three unreachable pockets are three designs, and each is named.** 44
  cells at `x 2..23 y 1 z 48..49` and 24 at `x 26..37 y 1 z 48..49` are the
  channel's bed: a body that walks on to it cannot climb out, which is what beat
  6.3 asks of it, and in play it is under water at every state of the tide. 24 cells
  at `x 10..13 y 7 z 94..99` are the entry duct, which is a one-way descent —
  the case `prefab-procedure.md` §4 says to describe rather than gate, and the
  reason this zone does not claim `reachable-floor`. Nothing else is stranded.
- **The vault is segmental, not semicircular, and the region decides that.** A
  barrel over a 22-block span wants eleven courses of rise; the zone has ten
  courses in total and four of them are the sub-floor the channel and the well
  are cut into. The section that fits is 22 wide at the springing stepping to 14
  at the crown over five courses. Narrowing the nave would buy the profile at the
  cost of the one thing beat 6.1 is about, so the silhouette carries it and the
  arcade's arches carry the rest.
- **The wellhead is a dressed apron and a sunk mouth, not a built-up kerb.** A
  kerb standing proud of the floor has to come out of the head band, which starts
  the vault one course higher over the well than over its neighbours. The apron
  is the floor's own top course in `pier`, and it is flush.
- **The grate does not lean.** The concept's grille is half out of its hole,
  which is a diagonal, and the grammar has no diagonal (`grammar.md` §6). What is
  built is a flat leaf of bars in the wall's outer course over a fallen sill of
  `rubble`, with the pale `render` lip around it.
- **No rule in this zone exposes a light-emitting role**, so the piece is dark
  and the shaft of daylight the scene is composed around is a hole rather than a
  beam. Light arrives as campaign-bound content on the declared anchors.
- **The piece declares a spatial contract.** Six spaces and seven edges: the
  entry duct, the cistern, the two one-block steps to the well's silt bed, the
  debris platform under the collapse, and the supply channel's invert — declared
  a space behind a one-way `drop`, because a body does go there and no
  out-of-walk kind fits a cut that opens upward, holds no anchor, and is reached
  by outside air on only 14 of its 68 cells. This zone therefore declares no
  out-of-walk region at all, which is answered by the rule below rather than by
  inventing one. `drop` is the datum a whole binds, guarded by the declared rise.
- **One authority decides that zero, and this zone's emptiness proves itself.**
  Both doors onto the contract checker — `expand` and `audit` — take the
  same verdict from the same function, and the strict reading holds: a gate that
  examined nothing has proved nothing. What saves this zone is not an exemption
  it claims but a fact the checker computes about it. `contract-no-body` is
  withheld, by name and with its reason printed, when a contract declares no
  out-of-walk region **and does not need one** — every standable cell lying in a
  declared space or a traversal edge's transit volume. That is the whole of this
  building, so the gate is not emitted and the zone is judged by 14. The
  withholding is secured by something the defect cannot supply: deleting a
  region that qualifies for nothing does not delete its cells, and they must
  then sit in a space, where the walk has to reach every one of them and the
  boundary has to close around them — strictly more proof than any out-of-walk
  kind asks for. Inventing a region to turn the audit green would have been the
  vacuity the gate exists to catch, one layer out.
- **Two things this zone cannot say, each established by a refusal.** S4's
  grille stands in the piece's outer column rather than between the room and its
  niche, so a `barred` edge refuses — "the bar does not bar anything" — and an
  opening claimed across both columns refuses as well, because with the grille up
  no cell there is reached by the air outside. The niche is part of the cistern
  and S4 is a seam the composing map declares. Separately, the collapse shaft and
  the aisle arch at z=0 cannot both be declared: an exterior edge is a property of
  the space and not of a face, so one edge on `cistern` exported both at once and
  `traversable` asked for a walk between a hole in the ceiling and a doorway on
  the floor. The two declared ways are the duct and the arch.
- **`tools/block-appearance.py --program` does not read a `local` paint.** Over
  this seven-role palette it reports `binding: 5 paint(s) examined` and skips
  `render` and `grate` in silence; their numbers in the table above came from
  `--mix` and `--id` instead. The binding count is the only tell, and a palette
  written entirely in the scope's own frame would measure as zero paints and
  print no error.

## Z7 bell tower

**Scene** (fixed before any tool ran, per the procedure's §1): the player climbs a
cobbled ramp that steps up between the collapsed low buildings of the upper ward,
with the tower standing at its head; enters at the tower's foot through a small
arched door; finds the first flight of the belfry stair broken — its lower treads
gone, what is left climbing four courses and stopping — and above it a ringing
floor, a louvre stage and a stairhead, and over those an open belfry whose four
faces are arcade bays and whose middle is filled by **a bell built out of blocks**,
hung in a timber frame that is part of the building, with a walk-around lane wide
enough to circle it and headroom enough to stand under its mouth.

**The tower above the break is unreachable on foot, and that is the design.** The
household broke the first flight; the campaign closes the gap by laying
`anchor/tread-lower` and `anchor/tread-upper`, worked from `anchor/tread-stand` at
the head of the surviving flight, with the rope carried from Z1. So the expansion's
reachability line raises everything over the break as one unreachable sheltered
pocket, and this paragraph is the reader §4 asks for — the pocket is the design,
not rooms with no way in. The zone accordingly claims `traversable` and **not**
`reachable-floor`, which is also what its manifest row says.

**One pocket is the shape that says the stair is sound.** Above the break the
ringing floor, the louvre stage, the stairhead and the belfry deck are a single
connected component: the climb is walkable end to end, and the only severance in
the tower is the broken flight the household made. A tower whose storeys came out
as SEPARATE pockets would be saying the opposite — that each flight fails on its
own — and that is a defect rather than a design, whatever the first flight is
doing.

**The manifest region changed, and it is the one design decision in this
production.** The row read `41x14x125`. Fourteen courses is one storey: it cannot
hold a stair, a ringing floor, a stairhead and a belfry above them, and a bell
that a body stands under needs eleven of the fourteen by itself. The scene needs
41 courses above grade — 7 of foundation, 4 storeys of 6, and 17 of belfry — so
the row now reads `41x48x125`. The footprint the campaign chose is untouched, and
48 is still one tile on the vertical axis. A bell tower fourteen blocks tall would
have been the block that shares the object's name, laid where the object goes.

**Expansion** — `delve-grammar expand --file design/programs/z7-bell-tower.json
--region 41x48x125 --seed 1 --traversable --id z7-bell-tower`. Fifteen gates pass,
every one with a non-zero binding: `blocks-exist` 25, `shape-complete` 25,
`states-complete` 25, `oriented-fills` 272, `non-empty` 246000, `traversable` 6,
`contract-well-formed` 25, `contract-coverage` 6248, `contract-closure` 4876,
`contract-edge-proof` 8, `contract-no-body` 6, `contract-reachability` 5187,
`contract-anchors` 40, `contract-exterior-faces` 2, `contract-no-body-majority`
6248. `traversable` counts declared doors rather than standable cells on two
region faces, which is what having a contract buys it: 6 where the contractless
reading said 82. `contract-anchors` splits its 40 as 13 in a space, 25 in a via
and 2 in a way — the way pair being the two treads CP-20 lays, which is the
engine saying in the manifest that those anchors are the declared opening rather
than a private copy of it. 38317 filled cells, 25 distinct
states, 6248 standable, footprint 5125 columns, perimeter 332, silhouette
complexity 1.16, 40 anchors. Reachability: 4259 of 6248 standable cells reachable
on foot from 41 grade entries (68.2%), 1212 unreachable sheltered in 43 pockets —
the largest by far is the whole tower over the break at 1102 cells, and the next
two are the inside of the bell. `delve-admit audit` passes over 246000 blocks (0
forbidden, 0 non-allowlisted, 0 unknown, 0 pre-pin unknown, 0 under-specified);
the block-state set is the same 25 it has always been.

**Provenance** — program `sha256:c0e0a23554cb9e30a237f57e8747eec39cef59d507a7acd8650a9cff2ec2238a`
(the hash of the *effective* program, which is what regenerates the bytes and is
carried in the manifest's own `generated_by.program_hash`; the sha256 of the
committed file itself is
`08e595eb00c7deb0a314f458c36efb8aaac94caaad602674a39abc111f0449bf`), seed 1,
region 41x48x125. Re-expanding those inputs reproduces every shipped file byte for
byte — verified by comparing file **contents** on stdin, never a path, since
hashing a `shasum` line hashes the filename with it. The tile contents are
`0ad4f90e67495b9c6b472cf4e575be2fcd50c5d45589c6e6ebcc427fd039b333`,
`607a8e442993832ee2596023970a32bab2ad2d399c9904d0af855db5aef73ee3` and
`bf50ce1d43f2d7cff73c4cbf2d30fbd00f6bffd29f54347aab9c93ccbd3cc967`.

**The program hash moves and the building does not.** Declaring the three beat
anchors and renaming `stair/foot_flat` changes the effective program, so the
manifest's `program_hash` and provenance line move with it — and a `mark` places
no block and a rule name reaches no output, so the three tile contents above are
the same three strings they were before the edit, `cmp` agreeing file for file.
The manifest's own diff is the three anchors and the two hashes, and nothing else:
the resolved spatial contract compares equal object for object.

**The first tile is byte-identical to the tile before the stair was repaired, and
the other two are not.** The well is drawn after the approach in the seeded
stream, so re-shaping it re-rolls every weighted mix downstream of it: 10266
cells differ, of which 938 are the well and the deck opening themselves and 9328
are the same role drawing a different member. Only 98 of those 9328 change
whether a cell is solid, and every one is `ruin/rubble` against its own declared
5% of air. The change is confined to `z 84..124` — the tower block and the rear
ward — which is why tile `x0y0z0` does not move, and git agrees with the hash.

**Artifacts** — the zone is past the 48-per-axis structure-template cap, so it
ships as a **tile set**: `prefabs/z7-bell-tower.x0y0z0.nbt`,
`…x0y0z1.nbt`, `…x0y0z2.nbt` and the manifest `prefabs/z7-bell-tower.json`, which
is the only file that describes the zone. Review shots and what each camera did in
`design/review/z7/`.

**Palette** — measured, never named from memory. Material colours are patch means
over crops of the concept image, verified by drawing the crops back onto the image
and looking at them; candidates come from `tools/block-appearance.py --screen` and
`--near` over the measured shelf, and every mix was read as a swatch sheet before
binding. The tower's ashlar measures as a pale near-neutral of very wide value
range (lit `#8a8e8f`, shaded `#7e8285`, saturation 10–15 of 255, luminance p05–p95
spread 88), which is a *mix* rather than a block: bound to one block the shaft
reads as a flat panel that no measurement of the mean would object to.

| Role | Mix | Measured | Concept sample |
|---|---|---|---|
| `tower/ashlar` | `stone_bricks` 40% · `andesite` 25% · `cracked_stone_bricks` 15% · `smooth_stone` 10% · `tuff` 5% · `chiseled_stone_bricks` 5% | `#808080` | `#8a8e8f` sunlit shaft face / `#7e8285` the shaded face |
| `tower/base` | `tuff_bricks` 40% · `andesite` 20% · `cobblestone` 15% · `polished_tuff` 15% · `mossy_stone_bricks` 10% | `#70736e` | `#626463` the streaked, stained lower shaft |
| `tower/floor`, `stair/rock` | `andesite` 40% · `cobblestone` 30% · `stone_bricks` 20% · `tuff` 10% | `#808080` | plainer than the wall, so a tread reads against it |
| `belfry/timber` | `dark_oak_wood[axis=x]` 75% · `muddy_mangrove_roots[axis=x]` 25% | `#3e321f` | `#42464b` the belfry's head-frame |
| `bell/bronze` | `oxidized_cut_copper` 60% · `oxidized_copper` 25% · `weathered_cut_copper` 15% | `#559b7d` | `#202328` Mercy, in shade |
| `bell/chain` | `iron_chain[axis=y,waterlogged=false]` | — | the tongue's hanging and the rope's fall |
| `ramp/cobble` | `cobbled_deepslate` 50% · `deepslate_bricks` 20% · `basalt[axis=y]` 15% · `polished_deepslate` 10% · `smooth_basalt` 5% | `#4b4b4e` | `#404449` the cobbled way |
| `ruin/rubble` | `cobbled_deepslate` 40% · `deepslate[axis=y]` 20% · `basalt[axis=y]` 15% · `mossy_cobblestone` 10% · `cracked_deepslate_bricks` 10% · `air` 5% | `#515252` | `#414548` the collapsed low buildings |
| `margin` | `deepslate[axis=y]` | — | inert mass, no player-visible face |

The loud member holds 5–15% of every structural mix, which is the craft rule the
numbers serve; `ruin/rubble`'s 5% of `minecraft:air` is the collapse itself — a
material that is partly not there.

**Two deliberate departures from the nearest colour match**, both stated rather
than smoothed over. The belfry's frame measures as a *cool* dark grey-brown and
**every wood block in 1.21.11 is warm**: the mix matches the concept's value and
cannot match its hue, so the frame is a shade browner than the painting. And the
bell measures near-black (`#202328`) because in the concept it is a shaded object
seen against a bright sky; its material is named in the campaign's own text as
oxidised copper, and a bell bound to the measured shadow would be a black box. It
is bound to a copper mix that is near-uniform on purpose — a bell is one casting,
and a four-block mottle would read as damage rather than as patina.

**Every orientation-carrying role is written in the scope's own axis frame.** Six
of the ten roles are `{"local": …}` paints, and this is not decoration here: a
tower wall is the same 2-thick slab on all four faces, so **one** rule builds all
four by naming its thin axis `smallest` — which hands two of the four calls a
turned frame. A bare `axis=y` or `axis=x` under those calls is in the world's
frame, and the rubble grain, the deepslate bedding and the belfry beams would run
the wrong way on half the building with every gate green. The stair well
reflects its frame as well: alternate flights are the same rule under
`mirror: {z: true}`, which is half of what makes the climb a switchback — the
other half is that they stand in different legs of the well. 272 fills were
examined, 125 carry block-state properties, and **125 of 125 resolve out of a
scope's own frame**.

**The well carries two legs, and that is what lets the tower be climbed.** A
flight's first act is to cast a solid course under its whole run. Stack two
flights in one bay and that course lands one block over the flight below's
landing: the landing loses its headroom, and the next tread stands three courses
above the last one a body can reach. The walk steps ±1 and does not jump, so
every joint severs — and it severs at every joint at once, which is why the
storeys came out as separate pockets rather than as one. So `stair/well` splits
the bay in `x` into a near leg (`stair_leg`) and a far leg, and the flights
alternate between them: no flight's plinth is ever cast over the flight below
it, and each flight's landing is entered from the other leg one course up. Only
the far leg touches the storey floors, so a body leaves the stair onto each
storey and rejoins it on the other side.

**The last flight ends in a pier, not in open air.** The belfry deck sits two
courses over the shaft's top course, so a flight that finishes with a landing
finishes one course short of the deck's own floor. `stair/flight_head` therefore
ends its run against a `head_run` pier carried the full height of the flight:
the body walks the landing, steps up onto the pier through the deck's opening,
and steps again onto the deck. The opening is `stair_bay + tread` long so that it
clears the landing as well as the pier — sized to the pier alone it roofs the
last treads and severs the climb one course below the bell — and it now stops
short of the wall it used to hole.

**The declaration, and the break declared as a way**

Nine spaces, six out-of-walk regions and ten edges, all read off the program's
own splits. The route is the zone: the ramp's foot, the climb to its crest, the
ward the tower stands in, the door through the tower wall, the tower's foot
room, and above it the ringing floor, the louvre stage, the stairhead and the
belfry — each its own floor, each entered by a declared edge. The document
version moves `1.4.0` → `1.7.0`, which is the version that owns `way`; `1.6.0`
is reserved in the ledger and is refused, so the move is direct.

**The broken flight is one contingent edge, and the region it opens is six
cells.** `tower/foot --stair--> tower/ringing` carries
`way { laid, stair/broken-flight, stair/tread }`: two treads at the head of the
surviving flight — `x 12..14 y 11 z 87` and `x 12..14 y 12 z 86` — empty as
built, and filled when content lays them. Laid, they carry a body off the last
surviving tread, round the switchback and onto the landing of the flight above,
and the whole tower opens: the four storey spaces and both upper stair volumes
are named in the verdict as *reached only once `stair/broken-flight` is laid*.
The proof is held to both halves and the verdict says so — **closed on the bytes
as shipped, open on the single-delta copy** — so a break that opens nothing
could not have been declared here.

**The break is at the head of the flight, not at its foot, and the region says
so.** The scene has the lower treads gone and what is left "climbing four
courses and stopping"; the bytes agree exactly — the surviving treads climb from
y 8 to y 11 and stop three courses under the landing they should meet, while the
flat stretch where the lower treads were is bare floor a body walks across,
because the tower's own base fills the courses beneath it. So the cells that are
not there are the ones at the TOP, and a region carved at the foot would open
nothing: filling the whole lower gap moves the reachable count by two cells and
leaves the tower shut. The declaration names the cells that carry the climb. The
rule that makes that flat is `stair/foot_flat`, named for the floor it produces
rather than for a break, because the severance is at the head of the run and not
here.

**The beat stands on the last surviving tread, and that is not where the break is
photographed from.** `anchor/broken-flight` sits at `13,7,97`, on the flat where
the lower treads were — the place the break is *seen* from, four courses below
the cells that carry the climb and ten blocks along it. A beat that wrote blocks
at that anchor would close nothing, and the number says so: filling the whole of
that flat takes the reachable count from 4259 to 4261 and leaves the tower shut.
So the repair is declared where it happens. `anchor/tread-stand` at `13,11,88` is
the cell at the head of the surviving flight that the repair leaves alone, facing
the two courses that are gone; it is reached from the tower door before anything
is laid, and it is still standable afterwards, because nothing the way lays
touches it. The two
courses are `anchor/tread-lower` at `13,11,87` and `anchor/tread-upper` at
`13,12,86`, and the manifest resolves both to `way:stair/broken-flight` — the
anchors ARE the way rather than a second description of it that could drift from
it.

**The nearest-looking anchor is the one that stops existing.** `anchor/stair-head-1`
at `13,11,86` is the auto-indexed mark at the top of the run, and it is the obvious
thing to reach for: it is at the break, and its name says stair head. A body stands
in it as built and does not once the way is laid — `tread-upper` is the cell
directly over it, so the repair turns it into the riser of the new step. A beat
anchored there would put the party inside its own repair, and would do it silently.
`tread-stand` sits two cells back along the run at the same level, on the last
course of surviving tread the repair leaves clear, which is why it is a declared
name rather than an index.

**Both courses, or nothing, and the enclosing box is not the beat.** CP-20 is two
region fills, each an anchor-centred box of extent `1,0,0` on a tread anchor, and
together they are exactly the six cells the contract declares — set equality
against the manifest's own boxes, not a count. Neither half is a smaller version
of the beat: the lower course alone leaves the reachable count at 4259, the upper
course alone drops it to 4256, and only both together raise it to 5361 and put a
body in the belfry. Nor is one fill over the region's bounding box the beat: `x
12..14 y 11..12 z 86..87` covers every declared cell, and it walls the climb at
4253 — six cells BELOW doing nothing at all, while reading exactly like "fill the
region". A way that is a stair is not a box, and a campaign that restates a
declared way as boxes gets no help from anything when it restates it wrongly.

**An open space is the stratum a body walks, not the sky column over it.** This
is the first zone here whose spaces are mostly `open`, and the first draft
claimed each one all the way to the top of the region, because that is the shape
of the `void` scope the rules produce. Every such space then exported an
exterior face on the region's UP plane — the sky, declared as a way out of the
piece — and `traversable` red, correctly, because no walk connects a face at
y 47 to anything. An opening is claimed rather than discovered, and a claim that
reaches the sky discovers one. So the ramp's foot is claimed as deep as the
ruins beside it and the ward as deep as the low walls standing in it, both by
the program's own parameters rather than by a number chosen to make the gate
green; the air above each is claimed separately and out of walk. Six faces are
exported where the sky-reaching draft exported eight, and the two that went are
the two that were not doors. The cut is owed exactly where a space carries an
`exterior` edge, because that is the only kind of space a face is exported from:
`approach/crest` keeps its full column and is 6724 cells of mostly air, which
costs nothing and says nothing, because no exterior edge names it.

**A way is one material, so the tread it lays is one block.** `stair/rock` is a
four-member mix and is refused for a way under the same rule that refuses a mix
for a bar; `stair/tread` is bound to `minecraft:andesite`, the dominant member of
the rock the surviving treads are built from.

**The climb out of the foot owns its own transit volume.** A way lies inside its
own edge's volume and is disjoint from every other edge's — that disjointness is
what makes opening monotone. So the well carries two volumes: `tower/stair-well`
for the contingent climb, and `tower/stair-upper` for the three climbs above it,
which excludes the broken flight entirely.

**The building did not change, proved three ways**: the three `.nbt` tiles hash
identically to the pre-contract expansion when their **contents** are hashed on
stdin rather than a `shasum` line that would carry the filename with it; `cmp`
agrees file for file; and a voxel-by-voxel comparison of the assembled 41x48x125
model finds 0 of 246000 cells differing. The structural edits the carve needed
were demonstrated byte-neutral **on their own** first, in a draft that still
declares `1.4.0` and carries no `contract` at all: 92 split nodes where the
shipped program carries 84, six of the eight new ones inside a private copy of
the run chain for this one flight and two outside it, every one of them cutting
void into void. That draft expands to the same three tiles, which is also what
says the version move is owed by the declaration and by nothing else — the
structure compiles unchanged at the old version.

**Judged at the pin, and the pin is named by revision.** The content repo's zone
audit builds the engine at `5e0ad7fd46d3855796e1963ad2eb54269ec76622`. Built
from that revision in its own tree, `delve-grammar audit --library
--campaign-root . --exclusions …` exits 0 over 43 programs with this zone at
`pass 15 gate(s)`. Its output is identical line for line to the same audit run
from a build at `57025e1c91626b71ab055f9b8a336caf9dc2489f`, and that revision's
output was in turn identical to a build at
`7d7a1057748d8660ecb9334eed9bcbdb0ace3764`, whose `crates/grammar`,
`Cargo.lock`, `Cargo.toml` and `rust-toolchain.toml` are content-identical to
it. Every revision is written out rather than called "the current engine",
because that phrase is a value that moves and this one has moved twice. The
move that carries a behaviour is `33d1af8a6786c2d4c702c33556f79c008fffddd6`: it
computes the out-of-walk kind per standable cell instead of once per declared
region, which changes what the report says about two regions of this campaign —
neither of them in this zone — and changes no verdict, no binding count and no
byte anywhere.

**Open against this piece**

- **Lighting is `unmeasured`, and cannot be otherwise for this zone.**
  `delve-admit lighting` reads one structure template and refuses a tile-set
  manifest (`DW0732`, exit 2); the zone's own tiles are not a way round it,
  because a lighting number for one slice of a building is a number about
  nothing. No rule in this zone exposes a light-emitting role either, so light
  arrives as campaign-bound content on the declared anchors.
- **The cobbled way is declarable, and the claim that it was not is withdrawn.**
  A climb is an EDGE, not a space: the seven terraces union into one transit
  volume, and a `via` carries no one-floor rule. Modelled as the `via` of a
  `stair` edge from `ramp/foot` to `ramp/head_way` — both of which are their own
  rules and so their own names — it proves green, rise 6 as declared. The earlier
  refusal ("standable floor at y 1..7, which is 7 levels") was the answer to the
  wrong question.
- **The tower stair climbs, and the claim that it does not is withdrawn.** The
  four separate pockets of 264, 242, 260 and 397 cells were one defect seen four
  times, not four: every flight cast its plinth across the whole bay at the foot
  of its own storey slab, which is a ceiling over the flight below. Stood in
  alternating legs the flights connect, and the storeys, the belfry deck and the
  climb between them are now a single component of 1102 cells. Two instruments
  that share only the frozen bytes agree: the zone's own reachability line, and a
  walk over the exported tiles that finds a 38-step route from the ringing floor
  to the belfry deck whose largest single step is one course.
- **The gap the campaign closes is declarable, and the claim that no edge class
  can state it is withdrawn.** A `walk`, `stair` or `drop` carries a `way`, and
  `opens: laid` names a region that is empty as built and that opening fills with
  the way's block. That is Z7's break exactly — treads that are not there, which
  the rope carried from Z1 puts back — where `barred` could only ever state the
  dual, an obstruction voided away. The proof is held to both halves: the class's
  own connectivity must FAIL on the bytes as shipped, so a break that opens
  nothing cannot be declared, and must hold on a copy with the treads laid.
  `contract-reachability` then walks the ways shut and opens them cumulatively by
  name, so the storeys over the break are reached *once the flight is laid*
  rather than excused. Declaring them out of the walk was never available and
  still is not: it would be secured by the very unreachability that is the
  finding. The general form reaches well past this zone — every one-way shortcut
  opened from the far side, every lowered bridge, every placed ladder is the same
  shape, and all of them are now writable.
- **The DSL has no way to say "lay this declared way", so the campaign restates
  the cells.** The contract names the region and the block, the manifest carries
  the exact boxes, and a quest effect can reach neither: CP-20 has to spell the
  same six cells again as two anchor-centred fills, and nothing compares the two
  statements. The restatement is not hard to get wrong in a way that looks right
  — the region's bounding box is one fill, covers every declared cell, and leaves
  the tower shut with six fewer cells reachable than doing nothing. This is a
  capability gap in the engine, not a defect in this zone, and it is worth naming
  because the general shape is every repaired stair, lowered bridge and placed
  ladder the `way` surface was written for.
- **The review set predates the three beat anchors.** `shots.json` carries a
  camera per anchor and was taken before `tread-stand`, `tread-lower` and
  `tread-upper` were declared, so it is three cameras short; `review/z7/README.md`
  says which and what each would show. Re-rendering is owed at the next render
  pass and changes no geometry — the three `.nbt` tiles are byte-identical across
  this edit, `cmp` file for file.
- **The envelope vocabulary has no term for a roofed, open-sided space, and the
  belfry is one.** An arcade is `enclosed` only in the sense that a roof stands
  over it; its four faces are open bays a player walks round the bell in and
  looks out of. `open` and `open_top` are both refused over a roofed cell, and
  rightly — so `enclosed` is what the belfry declares, and its bay openings are
  excused the way any opening is: by the claimed air outside them,
  `ward/wall-tops`. That excuse is load-bearing rather than incidental, and it
  is worth naming that a wall which is simply missing would supply the same
  excuse a deliberate arcade does. Declaring the bays out of walk would have
  avoided the question and would have been false — a body walks them, and they
  are 180 standable cells of the belfry's play space. This is a capability
  observation, not a defect in this zone.
- **The rise range is a separate matter and does not block the contract.** The
  declared rises of 6, 6, 6 and 7 between the storeys are accepted as written —
  the edge proof judges the connection, never the numbers — so the
  contract can state this tower's geometry at any parameter value. What
  `4 x $storey + 1` against a guarded `$storey ge 5` rules out is the DESIGN
  plane: a foot-to-belfry rise of 16, which `map-zones.md` asks for, is
  unreachable at every parameter value. That is a rule change and a design
  question, and it is not what stops the declaration.
- The rise is `$storeys + 1` rather than a bare literal, but `storeys` has
  exactly one legal value at this region: `zone_plan` guards
  `dim.y ge base_height + storeys + belfry_run`, and 48 = 7 + 24 + 17 exactly.
- **`tools/block-appearance.py --program` does not see a `local` paint.** Run
  against this program it reports `binding: 4 paint(s) examined` where the palette
  has ten roles: the six wrapped in `{"local": …}` are skipped in silence, and the
  six include every mix in the piece that carries an `axis`. The procedure's §2
  makes that command the palette check, so on any program written at document
  version 1.4.0 the check is a binding of 4 out of 10 wearing a pass. The numbers
  in the table above were therefore taken with `--mix` per role instead.
- **The bell is a stepped silhouette, not a curve.** The grammar has no smooth
  curve by design, so Mercy flares 3 → 5 → 7 across in two visible steps rather
  than in a profile. At playable scale the silhouette carries it; a reviewer
  looking for a bell-shaped *curve* will not find one, and no seed will produce
  it.
- **The tower's top is a flat cap.** The concept's belfry finishes with a cornice
  and a shallow crown; here the head band is one course of ashlar and timber and
  the roof one course of ashlar above it. The mass is right and the profile of the
  finish is not.
- The concept's shaft carries far more staining and streaking than a six-member
  mix can place, because a mix has no gradient — the weathering is uniform up the
  whole shaft where the painting concentrates it under the openings and above the
  base. A graded band per storey would fix it and is authoring work this
  production did not do.
- `anchor/belfry-stairhead` and `anchor/stair-head-1` have no useful eye shot;
  `review/z7/README.md` says why for each, and which cameras answer those
  questions instead.
- **The `minecraft:iron_chain` red is closed, and this entry is what is left of
  it.** It was real: the prefab audit's pinned `delve-admit` predated the 1.21.11
  chain rename, its allowlist had no `iron_chain`, and the one chain block in the
  belfry tile was the only offender in the whole palette. The pin has since
  moved, and the job now audits this zone as a tiled unit — the manifest is the
  audited unit for a zone past the template cap, not the individual `.nbt` — and
  passes: 45 of 45 units over 54 in-scope files, `prefabs/z7-bell-tower.json`
  named among them, with 0 files disowned by git. Nothing about the piece
  changed; the checker caught up with the pinned game version, which is what the
  entry said would fix it. The same red was noted as latent in `z2-gate-ward` and
  `z5-hall-keep`, and it is closed for them by the same bump. What survives the
  closure is a `DW0734` warning on two hero prefabs that carry the pre-rename
  `minecraft:chain` at a DataVersion of 2975 and rely on load-time datafixing;
  those are not this zone and not this campaign.
