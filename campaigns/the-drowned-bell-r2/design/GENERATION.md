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
it: all eight pass `oriented-fills`, seven of them carry local roles, and the
audit totals **501** fills resolved out of a scope's own frame across those seven.
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
| Z1 cliff road | `concept/z1-cliff-road.jpg` | `programs/z1-cliff-road.json` | **produced, awaiting owner review** — expands at 16x24x72 as a 2-tile set; the second zone with a spatial contract, so it is judged by 14 gates where the others carry 6; review set in `review/z1/` — see below |
| Z2 gate ward | `concept/z2-gatehouse.jpg` | `programs/z2-gate-ward.json` | **awaiting owner review** — expands at 20x10x84; interior review set in `review/z2/` (largest program: 101 rules) |
| Z3 drowned ward | `concept/z3-drowned-ward.jpg` | `programs/z3-drowned-ward.json` | **produced, awaiting owner review** — expands at 40x10x60 and ships as 2 tiles; review set in `review/z3/` — see below |
| Z4 chapel ward | `concept/z4-chapel-ward.jpg` | `programs/z4-chapel-ward.json` | **produced, awaiting owner review** — expands at 27x12x33; the campaign's first zone with a spatial contract, so it is judged by 14 gates where the others carry 6; review set in `review/z4/` — see below |
| Z5 hall keep | `concept/z5-hall-keep.jpg` | `programs/z5-hall-keep.json` | **produced, awaiting owner review** — expands at 11x11x76 and ships as 2 tiles; review set in `review/z5/` — see below |
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
