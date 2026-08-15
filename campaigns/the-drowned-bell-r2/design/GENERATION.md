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
audit totals **158** fills resolved out of a scope's own frame across those six.
Z1 is the worked case for the *state*, and it shows why the frame is not
decoration: the corpse is authored as `rotation=8`, facing out of its own recess,
and lands in the world as `rotation=4`. Z7 is the worked case for the *rule* —
one wall rule builds all four faces of a tower by naming its thin axis
`smallest`, so two of the four calls run under a turned frame, and it contributes
125 of the 158 by itself.

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
| Z5 hall keep | `concept/z5-hall-keep.jpg` | `programs/z5-hall-keep.json` | program exported, unproduced |
| Z6 cistern deep | `concept/z6-cistern-deep.jpg` | `programs/z6-cistern-deep.json` | program exported, unproduced |
| Z7 bell tower | `concept/z7-bell-tower.jpg` | `programs/z7-bell-tower.json` | **produced, awaiting owner review** — expands at 41x48x125; review set in `review/z7/` — see below |

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
household broke the first flight; the campaign closes the gap on
`anchor/broken-flight` with the rope carried from Z1. So the expansion's
reachability line raises the storeys, the belfry and the inside of the bell as
unreachable sheltered pockets, and this paragraph is the reader §4 asks for — the
pockets are the design, not rooms with no way in. The zone accordingly claims
`traversable` and **not** `reachable-floor`, which is also what its manifest row
says.

**The manifest region changed, and it is the one design decision in this
production.** The row read `41x14x125`. Fourteen courses is one storey: it cannot
hold a stair, a ringing floor, a stairhead and a belfry above them, and a bell
that a body stands under needs eleven of the fourteen by itself. The scene needs
41 courses above grade — 7 of foundation, 4 storeys of 6, and 17 of belfry — so
the row now reads `41x48x125`. The footprint the campaign chose is untouched, and
48 is still one tile on the vertical axis. A bell tower fourteen blocks tall would
have been the block that shares the object's name, laid where the object goes.

**Expansion** — `delve-grammar expand --file design/programs/z7-bell-tower.json
--region 41x48x125 --seed 1 --traversable --id z7-bell-tower`. Every gate passes
with a non-zero binding: `blocks-exist` 25, `shape-complete` 25, `states-complete`
25, `oriented-fills` 268, `non-empty` 246000, `traversable` 82 (41 standable cells
on the approach face, 41 on the exit face). 38808 filled cells, 25 distinct
states, 6312 standable, footprint 5125 columns, perimeter 332, silhouette
complexity 1.16, 37 anchors. Reachability: 4259 of 6312 standable cells reachable
on foot from 41 grade entries (67.5%), 1276 unreachable sheltered in 43 pockets —
the four largest are the three upper storeys and the belfry deck, and the
smallest named one is the inside of the bell. `delve-admit audit` passes over
246000 blocks (0 forbidden, 0 non-allowlisted, 0 unknown, 0 pre-pin unknown, 0
under-specified).

**Provenance** — program `sha256:17a315185a211f743d8fbea314aec76e7b0dd82f6a866dfcc75b7cac5cee1945`
(the hash of the *effective* program, which is what regenerates the bytes; the
sha256 of the committed file itself is
`713c54d5993b71460702e1f720b03d149210272a3024ec1065507f318b92c52f`), seed 1,
region 41x48x125. Re-expanding those inputs reproduces every shipped file byte for
byte — verified by comparing file **contents**, and by three instruments that do
not share a working directory, an output path or a build tree, one of them a
different engine commit. The tile contents are
`0ad4f90e67495b9c6b472cf4e575be2fcd50c5d45589c6e6ebcc427fd039b333`,
`2e163c480be39b73758c6dab670cf5b0c276dababc1dc03d0dea9612a64034ef` and
`25305fb67a4d28e37447f43100c680f6e8532beb23b7340048e1e7e605ad5d96`.

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
`mirror: {z: true}`, which is what makes the climb a switchback. 268 fills were
examined, 125 carry block-state properties, and **125 of 125 resolve out of a
scope's own frame**.

**Open against this piece**

- **Lighting is `unmeasured`, and cannot be otherwise for this zone.**
  `delve-admit lighting` reads one structure template and refuses a tile-set
  manifest (`DW0732`, exit 2); the zone's own tiles are not a way round it,
  because a lighting number for one slice of a building is a number about
  nothing. No rule in this zone exposes a light-emitting role either, so light
  arrives as campaign-bound content on the declared anchors.
- The piece declares no spatial contract, so every contract obligation examined
  nothing and `traversable`'s binding counts standable cells on two region faces
  rather than declared ways in. This is true of every zone in the campaign.
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
- **`prefab-audit` reds on `minecraft:iron_chain`, and the piece is not what is
  wrong.** That job globs `prefabs/*.nbt` and audits each file with its own
  pinned `delve-admit`, which is older than the pin the zone audit uses and older
  than the 1.21.11 chain rename: its allowlist has no `iron_chain`, so the one
  chain block in the belfry tile is `DW0730`, one block of 94464 in that tile and
  the only offender in the whole palette. `iron_chain` is in the pinned 1.21.11
  registry and is allowlisted by the engine the zone audit runs, where the whole
  zone audits clean — 246000 blocks, 0 not-allowlisted. The fix is the same
  one-line pin bump the zone audit's own comment describes for its engine ref,
  and it is a reviewed decision rather than a content edit: dropping the chain
  would trade the tongue's hanging and the bell-rope's fall for a green from a
  checker that is wrong about the pinned game version. **This is not specific to
  Z7** — `z2-gate-ward` and `z5-hall-keep` also paint a chain, so the same red is
  latent in two more zones and Z7 is only the first of the three to be produced
  into the library.
