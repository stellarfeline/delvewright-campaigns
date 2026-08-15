# Beat audit — the four zones produced before the current round

`reconciliation.md` part three asks, of the zones produced in the current round,
whether the program exported as a zone's artifact of record builds the zone it
names. In all of those it did not. **This document asks the same question of the
four zones produced earlier — Z0 barrow shore, Z1 cliff road, Z2 gate ward, Z4
chapel ward — beat by beat.** They came from the same export and nobody had asked
it of them.

The unit is the beat. `beats.md` states what each zone must stage; a beat is
either built by a rule of that zone's program or it is not.

## Method

- The subject is the **program**, not the zone's own record. `design/programs/z*.json`
  are the artifacts of record; `programs/zones.json` gives each its region and seed.
  Where a record and its program disagree, the disagreement is named below.
- Programs were expanded with `delve-grammar` built from the engine commit
  `zone-audit.yml` carries in `GRAMMAR_REF`, at the region and seed `zones.json`
  declares, with the optional gates it claims. Every one passed every gate.
- **Verdicts are traced to rules.** A rule that merely occupies the part of the
  region a beat happens in is not credited. Where reading the rules settles the
  question the verdict is by reading; where it does not, the zone was expanded and
  the shot or the measurement that settled it is named.
- Adjudication: **built** = the program has rules producing the scene the beat
  stages, including the geometry a campaign would bind its actors and items to.
  **Partially built** = the beat's mechanism or its named image element is
  produced but a stated, load-bearing part of the beat is not. **Absent** = no
  rule produces it.

Reproducing every verdict below:

```sh
# engine at the pin zone-audit.yml carries in GRAMMAR_REF
cargo build -p delvewright-grammar --release
delve-grammar expand --file design/programs/z0-barrow-shore.json --region 19x6x24  --seed 1 --traversable                                   --id z0 -o out/
delve-grammar expand --file design/programs/z1-cliff-road.json   --region 10x28x44 --seed 1 --traversable --reachable-floor                 --id z1 -o out/
delve-grammar expand --file design/programs/z2-gate-ward.json    --region 20x10x84 --seed 1 --traversable --allow-falls                     --id z2 -o out/
delve-grammar expand --file design/programs/z4-chapel-ward.json  --region 16x9x26  --seed 1 --traversable --allow-falls                     --id z4 -o out/
delve-render piece out/z<n>.nbt -o shots/ --size 900     # out/z2.json for the tiled zone
```

The renderer at this pin has no author-aimed camera, so an interior shot is aimed
by an anchor. Where a beat lies away from every declared anchor — Z2's ported wall,
its drain and the view back at its gateway — a review standpoint was added to the
expansion's metadata before rendering, the same device Z2's review set uses:
`look-gate-out` at 14,5,68 facing south; `look-ports` at 16,5,76 facing west;
`look-drain` at 14,5,77 facing east. Nothing was added to any program.

Every count stated below was taken twice by unrelated means — once from the
expander's own report and once by reading the `.nbt` palettes and block lists
directly.

Zone totals, measured off the expansions:

| zone | region | filled cells | distinct block states | standable | open to the sky | anchors |
|---|---|---|---|---|---|---|
| Z0 | 19×6×24 | 1 422 | **2** | 438 | 0 | 1 |
| Z1 | 10×28×44 | 5 490 | 7 | 50 | 44 | 12 |
| Z2 | 20×10×84 | 14 404 | 17 | 655 | 0 | 16 |
| Z4 | 16×9×26 | 3 045 | 7 | 165 | 0 | 6 |

---

## Z0 冢泽潮滩 — Barrow Shore

**Z0 is the special case, and it is not the case the round's status table
describes.** `GENERATION.md` credits Z0 to a tileset generator, pre-procedure,
and lists it as reviewed and accepted. That generator's shore piece is a 48×14×40
lit beach
with burial mounds, driftwood and a fire ring; it belongs to a six-piece delve of
its own, it is not in this campaign's tree, and `zones.json` does not name it. The
artifact `zones.json` **does** name, and that CI expands and judges on every push,
is `programs/z0-barrow-shore.json`.

That program is `elite_ground` alone — nine rules, one palette role. Expanded at
its declared region and seed it is **two block states**: stone bricks and air. A
floor slab, a roof slab, three courses of air between them, one declared anchor at
the centre. There is no sea, no mud, no cliff, no tide line, no prop and no light.
The engine's own rule index states the scope plainly: `elite_ground` is the whole
of Z0.

So the question has an answer, and the generator does not change it: the audited
artifact of record for Z0 stages none of Z0's seven beats, and the reviewed
artifact it is confused with is a different production of a different design.

| # | beat | rule(s) that build it | verdict |
|---|---|---|---|
| 0.1 | wakes on wet flat, a heap of stones a few metres away | — | **absent** |
| 0.2 | the cairn field, readable, thinning inland | — | **absent** |
| 0.3 | first enemy pushes out of the mud beside a cairn | — | **absent** |
| 0.4 | K1 the tide-stakes: three iron posts, lethal outside the line | — | **absent** |
| 0.5 | Emeric on the last dry shelf, shore-lamp lit | — | **absent** |
| 0.6 | the flat ends at cliff; one cut ledge starts up it | — | **absent** |
| 0.7 | the Dead Ebb return, the answered standing in the silt | — | **absent** |

**7 of 7 absent.** All by reading; confirmed by looking (the exterior orbit and the
eye shot from `anchor/elite` show an empty stone-brick sandwich) and by the block
census (2 states, 0 fittings, 0 light).

What the program *does* build is an open arena with a body position and two proven
flank lanes — the staging an optional elite needs. Z0's beat list has no such
beat; the optional elite appears only in the budget table. **The program is not a
failed attempt at the zone. It is a correct build of something the beat sheet does
not ask for.**

---

## Z1 崖道 — Cliff Road

Program: a `sea`-wide void gulf 12 courses deep, and above it `cliff_path` — a
one-wide lane with 1-deep recesses cut into the inner wall, some holding a corpse
prop.

| # | beat | rule(s) that build it | verdict |
|---|---|---|---|
| 1.1 | the ledge is single-file, met head-on | `shelf` → `path/cliff_path` → `path/cliff_courses` → `path/wall_lane` (`abs 1` void lane against `path/rock`) | **built** |
| 1.2 | a row of iron brackets at hand height — the anchors of a gone rope handrail | — | **absent** |
| 1.3 | K2 the fallen ledge: the shelf has gone into the sea, a gap round a blind bend | — | **absent** |
| 1.4 | a shover — one of the answered on the ledge that puts the player over the edge | `path/niche_band` → `path/niche_run` → `path/recess_teach` / `_test` / `_twist` → `path/niche_empty` / `path/niche_corpse` (6 recesses, 6 `anchor/niche-<i>` + 6 `anchor/niche-watch-<i>`), over `gulf` → `open_gulf` | **built** |
| 1.5 | the road goes *through* the rock — a rope store between two cave mouths, holding the Z1 rope | — | **absent** |
| 1.6 | the road reaches a breach in the gatehouse's outer wall | — | **absent** |

**4 of 6 absent.**

Evidence:

- **1.1 built, by reading and by measurement.** `wall_lane` splits the width into
  one void column and rock; 50 standable cells in a 44-long zone, 44 of them the
  lane and 6 the recesses.
- **1.2 absent, by census.** Z1's palette is three roles — `crag`, `path/rock`,
  `path/corpse`. Seven block states in the expansion, five of them rock, two
  skeleton skulls. No iron anywhere. The zone's own record says so: the concept's
  stanchions and chain rail "have no role and no rule in this program".
- **1.3 absent, by measurement.** The lane column was walked cell by cell: the
  floor beneath it is solid at **all 44** cells and the two cells above it are open
  at all 44. There is no gap, and no rule in the program can produce one — the
  zone's own gate ("the ledge is the only route") is written to refuse exactly
  that. The tide beat that depends on it (the sea rising into this one gap and no
  other) has nothing to rise into.
- **1.4 built, by looking.** The eye shot from `anchor/niche-watch-3` shows the
  one-wide ledge, the recess mouth beside the walking line and the open drop; the
  program's own gate binds the gulf beside 36 ledge cells over 3 seeds. What is
  absent is only the beat's named image element at the bottom of the drop — surf
  and rock teeth — which is 12 courses below a player who is falling.
  The surplus is worth naming: the beat sheet wants **one** shover; the program
  declares **six** occupant positions.
- **1.5 absent, by measurement.** Six sheltered standable cells in the whole zone,
  one per recess, each one deep. There is no chamber, no second mouth and no
  branch off the lane. The road passes nothing.
- **1.6 absent, by reading.** The lane runs off the region face. No rule writes a
  wall at either end, so there is nothing for a breach to be a hole in.

---

## Z2 门楼 — Gate Ward

The largest program of the four, and the only one that writes fabric of its own
rather than composing the vocabulary alone: a vaulted gate passage with
springers, a kerbed drain channel, a ported wall and a grille. Everything behind
the passage is stock vocabulary.

Mainline in travel order from the approach face: `gate/gate_passage` (a `watch_bay`
elaborated into a gatehouse), `door/threshold` (`ambush_door`),
`stand/disarm_stand`, `stair/boulder_stair`, `tee/passage`, `motif/threshold_motif`,
then off the end into `shaft/drop_shaft`. The shortcut hangs off the tee in the
side strip as `sally/threshold` (`far_side_bar`).

| # | beat | rule(s) that build it | verdict |
|---|---|---|---|
| 2.1 | entry through the breach, inside a **lowered** portcullis, the shore visible through its bars | — | **absent** |
| 2.2 | K3 the murder-holes: round openings in the vault, a killing drop on the centre line, safe edges, a floor above with something on it | `gate/port_wall` → `gate/port_row` (5 openings); hazard span `gate/hazard_span` → `gate/span_run` → `gate/span_column` (`anchor/gate`), observed from `gate/bay_zone` → `gate/bay_room` (`anchor/watch`) | **partially built** |
| 2.3 | the drain: a cut channel, still water at the plane's height, out under the gate | `gate/channel_column`, `gate/kerb_west` / `gate/kerb_east` / `gate/springer_kerb_column`, `gate/drain` → `gate/spur_column` + `gate/grate_wall_column` | **built** |
| 2.4 | G1 the guardroom: a grated embrasure, ledger leaves on the sill and floor, the bound ledger inside | — | **absent** |
| 2.5 | the Gatewright on the gatehouse roof above the murder-holes, working a winch; roof stair off the critical path | — | **absent** |
| 2.6 | S1 the portcullis, raised from a winch on the passage's inner side | `gate/span_grille` → `gate/grille_column` + `gate/kerb_west_grille_column` + `gate/channel_grille_column` (the grille); `sally/threshold` → `sally/bar_or_open` + `sally/far_room` (`anchor/sally-gate`, `anchor/unlock`) | **partially built** |
| 2.7 | Emeric moves up to the gate passage and stays; the lamp goes with him | `gate/corridor` → `gate/corridor_column` (dry roofed passage); `gate/bay_room` (a roofed pocket off the lane) | **partially built** |

**3 of 7 absent, 3 partial, 1 built.**

Evidence:

- **2.3 built, by looking and by census.** The eye view back down the passage at
  the gateway shows the channel running the length of the flags with mitred stair
  kerbs both sides, under a bar grille hung in the vault: 14 water source blocks,
  23 straight kerb stairs and 2 mitred corners, plus a spur and a grate set in the
  outer wall. The one divergence is position — the channel runs down one side, not
  the centre — and it terminates at the passage's inner wall rather than passing
  out under the gate.
- **2.2 partial, by looking and by measurement.** The ported wall is real: five
  square openings, evenly spaced, and the eye shot facing it shows them. But they
  are in a **side wall at chest height**, not in the vault; the cells behind them
  are the inert margin the zone's side strip is filled with, so nothing can look or
  drop through; and the standable floor levels in the whole zone are exactly two —
  the ward at one height and the drop-shaft landing at the bottom. **There is no
  storey above the passage**, so the half of the beat that is a map ("there is a
  floor above, and something on it") has nothing to be a map of. The hazard span
  the campaign would bind the drop to covers the full three-wide lane, so the
  beat's safe edges do not exist either.
- **2.4 absent, by reading.** No rule in the program produces a grate over a sill,
  a container, or a sealed room in the gate passage. The nearest thing is the
  watch bay — a 2×2 pocket walled on three sides — and it is not credited: it is
  open by construction, its gate is a sightline to the hazard span, and G1 is an
  optional *gated* room whose content is the thing it exists for. Crediting the bay
  would be crediting a rule that occupies the same part of the region.
- **2.5 absent, by measurement.** Same two floor levels. There is no roof storey,
  no stair to one, and no rule that could put a body above the passage.
- **2.6 partial, by looking.** A grille is built across the passage and it reads
  well — but it hangs in the top two courses with two clear courses of walk beneath
  it, i.e. permanently **raised**, and it carries no anchor, so nothing can open or
  shut it. The shortcut mechanism that *does* exist is 46 blocks away in the side
  strip: a barred opening with `anchor/sally-gate` and `anchor/unlock` behind it,
  proven unreachable from the near side. The beat's arrangement — the shortcut IS
  the portcullis, and the winch that raises it is beside it — is not built. There
  is a mechanism block in the program (`anchor/release`, one polished blackstone),
  but it belongs to the disarm stand 16 blocks further in and governs the hazard
  lane, not the gate.
- **2.7 partial, by looking.** The passage is dry, roofed and the first shelter,
  which is the beat's named image element, and there is a roofed pocket off the
  lane a station could bind to. There is no lamp: **no program of the four exposes
  a light-emitting role and no expansion contains one block that emits light.**
- **2.1 absent.** Three elements, none built: no breach (the approach face is the
  bare region face), no shut gate, and the grille the player would look through is
  ahead of them on the route rather than behind them.

**The surplus is larger here than the shortfall.** Four of the six pieces on Z2's
mainline — the boss-door bell-rope curtain, the worn-tread boulder lane and its
side pockets, the hazard release stand and the blind corner alcove — correspond to
**no beat of Z2 at all**, and neither does the one-way drop shaft the zone leaves
by. Z2's beats
name a portcullis, murder-holes, a drain, a guardroom, a roof elite, a shortcut and
an NPC station. The drop shaft additionally contradicts the beat sheet's own
topology: Z3's first beat has the gate opening onto the ward, and this program
leaves Z2 by falling four blocks with no way back.

---

## Z4 礼拜堂中庭 — Chapel Ward

Program: the box is split into a 9-deep side strip and a 7-wide mainline. The strip
holds `shortcut/threshold` (`far_side_bar`) and 18 further cells of inert margin.
The mainline is three corridor segments end to end: `junction/passage`
(`tee_passage`), `hearth/hearth_ward`, `chute/dumbwaiter`. Seven block states, six
anchors, 47.9% inert margin.

| # | beat | rule(s) that build it | verdict |
|---|---|---|---|
| 4.1 | a cloister with its roof gone: arcade on all four sides, sky above, grass in the paving | — | **absent** |
| 4.2 | K4 the fallen: bodies among rubble piles, one of them not scenery | — | **absent** |
| 4.3 | the Two Sextons, fought where the ward cannot be crossed around them; the collapsed canopy | — | **absent** |
| 4.4 | Sister Ide walks the cloister round with a hand-bell; the plinth is her turning-point | — | **absent** |
| 4.5 | G2 the rite: three marked stations of her round; completing it opens the hour-vault below | — | **absent** |
| 4.6 | S3 the banded door — oak, iron-banded, ring handle, barred on the chapel side; the ward visible below through the arcade gap | `shortcut/threshold` → `shortcut/threshold_plan` → `shortcut/wall` → `shortcut/door_column` → `shortcut/bar_or_open` (`anchor/gate`), `shortcut/far_room` (`anchor/unlock`), reached through `junction/branch_door` | **partially built** |
| 4.7 | Emeric comes this far and no further; he sets the lamp on the chapel step | `hearth/nook_band` → `hearth/nook_column` → `hearth/nook_room` → `hearth/nook_air` (`anchor/hearth`, `hearth/hearth_floor`) | **partially built** |

**5 of 7 absent, 2 partial, 0 built.**

Evidence:

- **4.1 absent, by measurement and by looking.** Of 165 standable cells, **165 are
  sheltered and 0 are open to the sky**. `hearth/lane_column` fills four courses of
  rock over the lane along its whole length; the exterior shot is a solid block and
  the eye shot from the hearth nook is an unlit stone tunnel. There is no arcade
  rule anywhere in the program: every cross-lane split terminates in a solid
  `fill`, never a repeated pier-and-opening.
- **4.2 absent, by census.** No corpse role, no rubble role. Z4's palette is seven
  entries and every one of them is structural stone, inert margin, a paving, or
  the shortcut's bars. The capability is not the obstacle — Z1's program binds a corpse prop in
  the same document version.
- **4.3 absent, by reading.** No arena rule. The lane is five wide, narrowing to
  two at the nook. Nothing in the program produces open ground, a canopy, or a
  fight the ward cannot be crossed around.
- **4.4 absent, by reading.** The mainline is a straight 26-long corridor; there is
  no round to walk and no plinth. `anchor/hearth` is not credited here: it is a
  rest-point focus in a nook off the lane, reachable only as a detour, which is the
  opposite of an NPC circling the middle of an arena.
- **4.5 absent, by measurement.** No three stations, and the only floor below the
  ward is the duct landing — the zone's own exit by falling, not a vault under a
  chapel.
- **4.6 partial, by looking and by reading.** The mechanism is genuinely built:
  18 iron bars in a wall across a side branch, `anchor/gate` on the opening,
  `anchor/unlock` in the far room, the far room proven unreachable from the near
  side through one doorway. Absent: the oak leaf, the ironwork, the ring handle
  (the zone's record states the substitution and its reason), the arcade gap, the
  view of the ward below, and the drop into the gatehouse yard — the far room is a
  24-cell pocket opening on the zone's own outer face.
- **4.7 partial, by reading.** The rest nook is the mechanism a stationary NPC
  needs — off the road, one way in, a declared focus cell on its own paved floor.
  Absent: the chapel step, the arch, and the lamp; the zone's minimum floor light is
  zero over all 165 walkable cells and no rule exposes a light role.

**Two documents disagree about where Z4 sits in the delve.** `beats.md` places the
chapel ward before the hall and keep, entered from the drowned ward and left up the
keep stair. The production record's scene for this zone has the player **drop out
of the keep's kitchen duct** into it, and the program is built that way — a duct
descent at the approach end, a one-way fall, no way back up. The engine's zone index
calls Z4 a hub. Beats 4.6 and 4.7 both depend on Emeric arriving here after the
shortcut opens, which the reversed order makes impossible to stage.

---

## The count

| zone | beats | built | partially built | **absent** |
|---|---|---|---|---|
| Z0 barrow shore | 7 | 0 | 0 | **7** |
| Z1 cliff road | 6 | 2 | 0 | **4** |
| Z2 gate ward | 7 | 1 | 3 | **3** |
| Z4 chapel ward | 7 | 0 | 2 | **5** |
| **total** | **27** | **3** | **5** | **19** |

**19 of 27 beats are absent. 3 are built.** Every one of the four programs passed
every machine gate with a non-zero binding, at the region and seed the campaign
declares, at the pinned engine.

The worst zone by count is **Z0**, at 7 of 7 — but its program never claimed to be
the shore, and the engine's own index says so. The worst zone by consequence is
**Z4**: 5 of 7 absent and nothing built outright, in a zone the production record
lists as produced and awaiting review, whose one structural decision — a roof —
deletes five beats on its own while the palette and the proportions converge on the
image and every gate stays green.

## The shape of the absences

`reconciliation.md` finds that the omissions across the zones are all one
omission — the made-by-hands layer, fittings and light and ornament. Held against
27 beats, that finding is **confirmed as a universal fact and refuted as the shape
of the absences.**

Confirmed, and more strongly than the original evidence put it. Across the four
zones there are **24 361 filled cells and not one block that emits light.**
Fittings, props and fluids together are 0 blocks in Z0 (0.00%), 2 in Z1 (0.04%),
81 in Z2 (0.56%) and 18 in Z4 (0.59%). Z0's entire palette is one block. Nothing in
any of the four was *put there* rather than cut from the rock, except a portcullis,
a drain, two skulls and three doorways' worth of bars.

Refuted as the shape, because the beats say what the block census cannot. Sorting
the 19 absent beats by what would have to change to build them:

| what the beat needs that the program does not have | beats |
|---|---|
| a fitting or a light, in a room the program already builds | **1** — Z1's bracket line |
| a fitting **and** a different room | **4** — the cairn field, Emeric's shelf, the guardroom's grate and ledger, the corpse ambush |
| a **different room**: massing or topology | **14** |

Fourteen of nineteen are absent because the program builds a different building:
sky where there is a roof, a second storey where there is none, a gap in a floor
that is continuous by gate, a chamber off a route that has no branch, an arena
where there is a corridor, a round where there is a straight line, a vault where
there is a drain shaft, a breach where there is a bare region face. **Only one of
nineteen would be fixed by binding a fitting.**

Why the earlier finding landed where it did is visible in its own method: it was
written from the zones' "Open against this piece" lists, and those are written by
comparing the built zone against its **concept image**. That comparison catches
missing ornament, because ornament is what differs when the palette and the
proportion already agree — and it structurally cannot catch a missing beat,
because the beat sheet is not one of its inputs. Z4 is the proof: its record
records the roof honestly and then classifies it as a decision rather than an
omission, and the reconciliation carries that classification forward. Measured
against the beat sheet it is not a stylistic decision. It is five beats.

So the refinement is: **the made-by-hands layer is missing everywhere and is the
smaller half of the problem.** Eight correctly-massed volumes with no fittings read
as a quarry; these four are not correctly massed either.

There is a second shape the beat count exposes that no image comparison can, and it
runs the other way. **Seven composed pieces across the four programs stage nothing
the beat sheet asks of their zone** — Z0's arena, Z2's boss-door curtain, boulder
lane, release stand, blind alcove and drop shaft, and Z4's duct. In Z2 that is four
of the six pieces on its mainline, plus the shaft it leaves by. The programs are not thin versions of their
zones. They are the staging vocabulary laid out end to end, with the zone's name on
the file. The vocabulary chose what the zone stages, and the beat sheet was not
consulted at either end.

## What the campaign's own documents assert that the programs do not

Named because each cost time to run down, and each would mislead the next reader.

- The audit workflow's own comment about its pin is wrong in both directions: it
  says the pin is a feature-branch commit and that the job is red until a bump is
  made. The pin it carries is a merge commit on the engine repo's main and the
  bump has already happened. The commit that made the bump says so.
- Both review READMEs give reproduction commands the pinned renderer cannot run:
  an author-aimed `--view` flag it does not have, and a global option placed before
  the subcommand. Z2's review set is additionally reproduced at a seed the campaign
  does not build that zone at.
- The production record credits Z0 to a tileset generator and lists it as
  reviewed and accepted. The artifact the manifest names and CI audits is a different thing
  entirely, and the tileset named belongs to a six-piece delve of its own design —
  which the campaign's own design README declares is not a source for anything here.
- The production record and the beat sheet place Z4 on opposite sides of the hall
  and keep, and the program implements the record's order.
- The production record has full sections for two of these four zones. Z2's only
  record is its review README; Z0's is one table cell. A reader told to work from
  the produced zones' records finds half of them.
