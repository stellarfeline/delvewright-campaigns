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
audit totals **32** fills resolved out of a scope's own frame across those five.
Z1 is the worked case, and it shows why the frame is not decoration: the corpse
is authored as `rotation=8`, facing out of its own recess, and lands in the world
as `rotation=4`.

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
| Z0 barrow shore | `concept/z0-barrow-shore.jpg` | tidal-keep generator (pre-procedure; measured-palette pass 2026-08-11, engine PR #397) | owner-reviewed, accepted with the shoreline-edge correction applied |
| Z1 cliff road | `concept/z1-cliff-road.jpg` | `programs/z1-cliff-road.json` | **produced, awaiting owner review** — expands at 10x28x44; review set in `review/z1/` — see below |
| Z2 gate ward | `concept/z2-gatehouse.jpg` | `programs/z2-gate-ward.json` | **awaiting owner review** — expands at 20x10x84; interior review set in `review/z2/` (largest program: 101 rules) |
| Z3 drowned ward | `concept/z3-drowned-ward.jpg` | `programs/z3-drowned-ward.json` | program exported, unproduced |
| Z4 chapel ward | `concept/z4-chapel-ward.jpg` | `programs/z4-chapel-ward.json` | **produced, awaiting owner review** — see below |
| Z5 hall keep | `concept/z5-hall-keep.jpg` | `programs/z5-hall-keep.json` | program exported, unproduced |
| Z6 cistern deep | `concept/z6-cistern-deep.jpg` | `programs/z6-cistern-deep.json` | **produced, awaiting owner review** — expands at 40x10x100 into a 3-tile set; review set in `review/z6/` — see below |
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
527, `non-empty` 40000, `traversable` 12 (4 standable cells at the approach face
— which are the duct and nothing else, the rest of that face being solid — and 8
at the exit face, where the aisle's last arch is). 26463 filled cells of 40000,
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
- **The piece declares no spatial contract**, so every contract obligation
  examined nothing and `traversable`'s binding counts standable cells on two
  region faces rather than declared ways in. It would say something real here —
  the zone has one entry, one interior route and two openings that are not on the
  same axis — and it is the largest single thing left undone against this piece.
- **`tools/block-appearance.py --program` does not read a `local` paint.** Over
  this seven-role palette it reports `binding: 5 paint(s) examined` and skips
  `render` and `grate` in silence; their numbers in the table above came from
  `--mix` and `--id` instead. The binding count is the only tell, and a palette
  written entirely in the scope's own frame would measure as zero paints and
  print no error.
