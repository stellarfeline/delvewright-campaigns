# Halgrave as one map program — the composition record

What `design/programs/map.json` does, why each decision was taken, and what the
machine refused. spec-0040 is the method; this is the record of applying it to
this campaign's eight zone programs as they stand.

The headline, stated first because everything below is evidence for it:

> **The map program composes, expands and is deterministic. It is red on six
> contract gates, and every one of the six is the same fact: five of the eight
> zone programs declare no spatial contract, so the whole has nothing to bind
> its obligations to over 15 879 standable cells, 130 anchors and five of the
> ten seams.** No workaround supplies what the parts do not declare, and the
> three that were tried are recorded in §5 with the diagnostics that refused
> them.

---

## 1. The composition, in numbers

| | |
|---|---|
| document version | `1.5.0` — the program-level `include` list |
| region | 79 × 72 × 436 = 2 479 968 cells |
| seed | 1 |
| composed | 8 zone documents, under prefixes `z0`…`z7` |
| after composition | 628 rules, 275 params, 109 palette roles |
| expansion | 2.5 s |
| anchors | 184, of which 130 land in nothing the contract declares |
| verdict | **fail** — 10 gates pass, 6 red |

```
delve-grammar expand --file design/programs/map.json \
    --region 79x72x436 --seed 1 --id halgrave-map -o out/
```

### The site plan

World axes: `+X` east, `+Y` up, `+Z` south. The site steps up south to north,
so the player's travel runs toward `Z`-min, which is also the direction every
§5b rule calls its own local `Z`-min.

Lanes, west to east: `lane_sea` 8 · `lane_road` 16 · `lane_core` 41 ·
`lane_east` 14.
Bands, north to south: `band_crown` 125 · `band_hall` 76 · `band_cloister` 33 ·
`band_ward` 60 · `band_gate` 56 · `band_apron` 6 · `band_flat` 80.

| zone | box (as `zones.json` declares it) | where | box floor (map course) | datum |
|---|---|---|---|---|
| Z0 barrow shore | 40 × 18 × 80 | flat band, core | 5 | flat −1 |
| Z1 cliff road | 16 × 24 × 72 | road lane, `z` 280–352 | 1 | road +4 |
| Z2 gate ward | 25 × 18 × 56 | gate band, core `x` 8–33 | 8 | passage +2 |
| Z3 drowned ward | 40 × 10 × 60 | ward band, core `x` 0–40 | 6 | causeway top 0 |
| Z4 chapel ward | 27 × 12 × 33 | cloister band, core `x` 7–34 | 14 | cloister +9 |
| Z5 hall keep | 11 × 11 × 76 | hall band, core `x` 26–37 | 17 | hall +12 |
| Z6 cistern deep | 40 × 10 × 100 | crown band, beneath Z7 | 6 | cistern 0 |
| Z7 bell tower | 41 × 48 × 125 | crown band, over Z6 | 17 | tower foot +14 |

Every zone is handed **exactly its declared region in the world frame**, with no
`reorient` at the call site. That is a decision, and its reason is in §2 clause 2.

---

## 2. Per clause of the brief

### Clause: compose the whole of Halgrave as one map program, `map.json`, `1.5.0`

**Decision.** One document at `1.5.0` with an eight-entry `include` list, each
zone allocated its box by nested `split`, called by its own qualified `start`
symbol (`z0/barrow_shore`, `z1/cliff_road`, `z2/gate_ward`, `z3/drowned_ward`,
`z4/chapel_ward`, `z5/keep`, `z6/cistern_deep`, `z7/zone`).

**Reason.** The document-level `include` surface exists in this toolchain and is
fenced at exactly `1.5.0`. spec-0040 §6.2 lists it as a capability the map
program requires and does not have; it has since landed, and `check` reports it
with a binding count. Two of the eight `start` rules are not named after their
files (`z5` is `keep`, `z7` is `zone`), which is only discoverable by reading the
documents.

**What was hard.** Nothing here. The include resolved first time and reported
each composed document by prefix, path and program name.

### Clause: include all eight; allocate each a box by `split`; bind params and palette roles at the call site; do not edit any zone's rule bodies

**Decision.** No zone program was opened for editing. Every zone gets exactly
its `zones.json` region, in the world frame, with no reorientation at the call
site. Palette rebinds happen at one `bind` node wrapping the whole core.

**Reason for the world frame, which was a real choice.** Every §5b rule opens
with `z(Largest)`, so a zone normalises its own frame from whatever box it is
handed. Handing Z5 a transposed 76 × 11 × 11 box would give the same local
geometry with the hall's long axis running east–west, which is what
`map-zones.md` says Z5's massing wants. It was **not** done: `grammar.md` §4e
records that Z2 expanded at its transposed region is refused by `DW0736` on four
world-frame `iron_bars` runs, and reports `DW0742` (undecided) at its declared
one. Transposing a zone is therefore a change to what the zone builds, not a
placement, and the brief calls the zones as they stand. The cost is recorded as
part debt in §4: **Z5's long axis runs north–south in the composition and
`map-zones.md` says east–west.**

### Clause: bind the palette roles per call site — the map is the material authority

**Decision.** One `bind` node over the whole core rebinds sixteen structural
roles onto two map roles:

- `stone/ashlar` ← `z1/wall/ashlar`, `z2/gate/ashlar`, `z3/tower/wall`,
  `z4/arcade`, `z4/vault_stone`, `z5/hall/stone`, `z5/gallery/stone`,
  `z5/motif/stone`, `z5/stores/stone`, `z5/door/stone`, `z7/tower/ashlar`
- `stone/rubble` ← `z0/cairn/stone`, `z2/gate/rubble`, `z4/rubble`,
  `z4/collapse`, `z6/rubble`

**Reason.** spec-0040 §4: "the same stone is one binding read eight times, not
eight measurements that happen to agree." Sixteen sites, two bindings.

**The limit, and it is a part-debt finding.** Only **world-frame** roles are
rebound. A `{"local": …}` role carries the scope's own axis frame, and pushing a
plain paint down over it would strip the frame that `DW0736` exists to protect.
The zones' most characteristic materials are `local` — `z1/crag`, `z1/path/rock`,
`z2/gate/crag`, `z3/ward/deck`, `z3/ward/seabed`, `z5/margin`, `z6/render`,
`z7/ramp/cobble`, `z7/ruin/rubble`, `z7/margin` — so the map is the authority
over the dressed stone and is not the authority over the rock any of these zones
is cut from. **The whole cannot restyle a part's framed role from the call site;
the DSL has no framed-role rebind.**

### Clause: the map writes the rock, the connective pieces, the curtain, the roofscape, the ground and the one sea

**Decision.** The map's own rules are `cliff_mass` (the west cliff, 26 courses),
`ground` / `ground_crag` (one rule, height pushed by `bind`, called at four
sites), `shelf_ground` (the upper shelf, which the cloister's north door is
handed on to), `strand` (the wet strand at the cliff foot), `tidal_apron` and
`causeway` (the map's own arrival ground), `curtain` + `merlons` (the ward's
toothed wall-head, a `repeat` split), `open_water` and `sea_wall` (the sea).

**The one sea is one param.** `sea_y` = 10 is the first air course above the
standing tide; every floor whose datum is `d` stands at `sea_y + d`. Both sea
bodies read it, and so does every zone box placement.

**What was hard: the sea does not stay in its own box.** The first expansion was
red with

```
fluid-contained FAIL  bound 174728 DW0800: 117 way(s) out of a body of 174728
fluid cell(s) — 8,1,415 runs into 8,1,414 (minecraft:air); 8,2,415 runs into
8,2,414 (minecraft:air); … (+111 more)
```

The map's shore water abutted Z1's box on a plane where Z1 leaves air. A split
partitions, so the map cannot reach into a zone's box to wall it; the wall has
to be a map-owned cell **allocated in advance**. Two things were changed: the
map's water bodies were reduced to the two flank seas, each walled by its own
`sea_wall` column on its inward side, and the tidal apron's water sheet was
deleted outright rather than shelled. That last is not a weakened check — the
apron's sheet was geometry invented for this composition that was wrong, and Z0
writes no water at all (`fluid_cells: 0` in its own report), so a second sheet
over the same flat would have been the map overwriting a part's business.
`fluid-contained` now passes at 82 208 cells with 0 ways out.

### Clause: every seam becomes a declared contract edge, with its class and rise

**Decision.** Six of the ten rows of `map-zones.md`'s seam table are declared
edges. Four are **undeclarable**, and that word is used precisely: a contract
edge's endpoint must be a declared space or the reserved name `exterior`, and
for these four neither end supplies one.

| # | seam (`map-zones.md`) | treatment | verdict |
|---|---|---|---|
| 1 | Z0 → Z1, flat → ledge | `map/arrival --walk-- z1/foot` via `z1/shore-mouth`, rise 0 | **proved** |
| 2 | Z1 → Z2, the fall through the breach | `z1/landing --drop-- z2/gate/passage` via `z1/breach`, rise −3 | red |
| 3 | Z2 → Z3, passage → causeway top | undeclarable | — |
| 4 | Z3 → Z4, ward → cloister | `map/causeway --stair-- z4/walk` via `z4/west-door`, rise 9 | red |
| 5 | Z4 → Z5, cloister → hall | `z4/terrace --walk-- map/shelf` via `z4/north-door`, rise 0 | **proved** |
| 6 | Z5 → Z6, hall → cistern | undeclarable | — |
| 7 | Z6 → Z3, the grille | undeclarable | — |
| 8 | Z3/Z4 → Z7, the ramp | undeclarable | — |
| 9 | Z2 ↔ Z0, S1 the portcullis | `z2/gate/mouth --walk-- map/causeway`, rise −1 | **proved** |
| 10 | Z4 → Z2, S3 the banded door | `z4/stoop --drop-- z2/gate/yard`, rise −7 | red |

**Seam 9 is stated at its measured class, not the seam table's.** The table calls
it a drop onto the sand. The resolved boxes measure one course, and the checker
reported *"a drop is one-way, and a body can walk back up from map/causeway to
z2/gate/mouth"*. It is a walk of rise −1, and that is what the contract says.
Seams 2, 4 and 10 likewise carry the **measured** rise, not the table's; the
table's figures were −2, 9 and −8 against measured −3, 9 and −7.

**Seam 5 is a rise of 0, not the table's 3.** The three-course climb the table
gives Z4 → Z5 is Z4's *own* north flight, which Z4 already declares as
`walk --stair-- terrace, rise 3`. Across the seam plane the terrace and the map's
upper shelf stand on one course, `sea_y + hall_datum` = 22, and the identity is
guarded. Stating the table's 3 at the seam would have double-counted it.

**Why the four are undeclarable, and it is one fact.** Z3, Z5, Z6 and Z7 declare
no contract, so they declare no space; and a `split` gives two boxes exactly one
shared plane with no map-owned cell between them, so the map cannot interpose a
region of its own. There is no near side and no far side to name.

### Clause: guard identities so a drifting floor refuses at expansion naming both numbers

**Decision.** Twenty-eight identities, in one `all` guard on the `halgrave` start
rule with **no `otherwise` arm**, so any drift is a `NoApplicableRule` refusal at
the outermost scope, and `grammar.md` §4 makes that refusal print every failed
conjunct at once with both operands as evaluated.

They are of four kinds:

- **the region is the site plan** — `dim(x)`, `dim(y)`, `dim(z)` against the lane
  and band sums, so the region on the command line cannot disagree with the plan;
- **the sea plane** — the causeway top read from both ends of the Z2/Z3 seam and
  against `sea_y + head_datum`; the ward floor and the belfry floor against
  `sea_y + ward_datum` / `sea_y + belfry_datum`;
- **the seams** — Z0/Z1 on one course; Z1 → Z2 strictly a fall; Z4 → Z5 on one
  course; Z4 → Z5 climbs; Z5 → Z6 descends by more than one course; the grille
  above the ward's bare floor; the cistern beneath the tower with the map's own
  lid between; the belfry over the hall's box top;
- **the plan** — the road's south face must land inside the apron band, or the
  strand and the arrival flat are two disjoint pieces of ground; the cloister's
  north door must face the map's shelf and not the hall's box; and every box must
  fit the lane and band it is handed.

**The two the parts made fire, and what they say.** Two identities taken straight
from `map-brief.md` refuse:

- `sea_y + ward_datum == z3_base + z3_ward_off` with `ward_datum = −2` (the
  brief's −1.5). Z3's program fixes its causeway head three courses above its
  ward floor (`anchor/causeway-head` local `y` 4, `anchor/wader-*` local `y` 1);
  the brief wants 1.9. The composition places Z3 by the causeway seam, which is
  the traversal fact, and the ward floor lands at **−3**. `ward_datum` is
  declared −3 so the identity holds and states the truth.
- `sea_y + belfry_datum == z7_base + z7_belfry_off` with `belfry_datum = 30` (the
  brief's belfry floor). Z7's program puts the belfry floor **25** courses above
  the tower foot (`anchor/tower-foot` local `y` 7, `anchor/bell-walk` local
  `y` 32); `tide.md` wants 16. The composition places Z7 by the tower foot at
  +14, so its belfry floor is at **+39** — which is, exactly, the crown height
  `map-brief.md` derives for the shore standoff. `belfry_datum` is declared 39.

Both are part debt, in §4. Both are now guarded, so a future edit that moves
either number refuses instead of drifting.

### Clause: the map's entry is the flat at the causeway head, and reachability must carry a body to the belfry floor

**Decision.** `contract.entry` is `map/arrival` — the map's own tidal ground at
the causeway head, which unions with the strand at the cliff foot so the entry
space is one floor and one connected piece. Reachability from it reaches 3 411 of
6 578 standable cells in declared space: the whole arrival, the causeway, the
whole of Z1 (foot, road, store, landing) and the whole of Z2 (passage, mouth
behind its bar, chamber, roof, yard, head). What it does not reach is Z4's six
spaces and the map's own upper shelf — 3 167 cells, every one of them behind
seam 4, which is the seam Z3 cannot supply a near side for.

**The belfry cannot be reached, and it is not a layout failure.** Z7 declares no
contract, so the belfry floor is not a declared space, so no edge can end there
and no walk can be asked to arrive. The map cannot supply the space: a `claim`
takes the scope's whole box, and the box handed to `z7/zone` is the whole tower,
48 courses of it. §5 records what the machine says when that is tried anyway.

### Clause: `map-zones.md`'s six ground planes against the standing tide at one level

**Note on a number.** `map-brief.md`'s massing table has **seven** stages, not
six: the flat, the ward, the gate, the road, the cloister, the hall, and the
ramp-and-belfry. All seven are placed and all seven are guarded against `sea_y`.

### Clause: the five reference views are rank-only reference, never targets

Honoured. No view was reproduced and no geometry was drawn from an image. The
geometry of record is `map-brief.md` and `map-zones.md`, and where a written fact
and a produced zone disagreed the produced zone won and the disagreement is
written down (§4).

---

## 3. The corpus search — what was looked for before anything was written

`prefab-procedure.md` §3 sends an author to the corpus rather than the schema, so
the corpus is the language. This is what was there.

| looked for | found |
|---|---|
| any example of `include` in the corpus | **none.** `delve-grammar list` names 35 programs and no program in it writes an `include` list. The only example of the surface anywhere reachable is the six-line JSON fragment in `grammar.md` §5c. |
| `include` in the demonstration-coverage report | **absent from the table entirely.** `delve-grammar coverage --json` returns 22 constructs and the string `include` appears **zero** times in the file. spec-0040 AC8 requires `coverage` to count the include surface with a binding count and a corpus program to demonstrate it; in this build it counts neither. |
| an example of `claim` / `contract` | **one.** `node:claim bound 4, 4 use(s) in spatial-contract` — a single corpus program, two rooms, a barred door and a corbel. Every contract idiom used at map scale had to be generalised from that one example plus `grammar.md` §2d. |
| an example of `bind` | **two.** `node:bind bound 2, 2 use(s) in idiom-arguments`, both of them a palette rebind of one role. The map performs a sixteen-role rebind at one site; nothing in the corpus shows that shape. |
| how a zone composes vocabulary | eight worked examples, in `grammar.md` §5c's tables, and the eight zone documents themselves. This was the richest source and the one actually used. |
| a `compose`/`map` CLI verb | **none.** `delve-grammar` has six subcommands and none of them composes; composition is a document surface only. |
| how the map is bound to CI | `audit --campaign-root`, and it walks `zones.json`'s `zones` list. See §7. |

**The distinction the search was for.** For the map's geometry the answer was
consistently *nobody had said it this way* — every construct the map program uses
is demonstrated somewhere, and the eight zones are a rich model for box
allocation, guarded arithmetic and margin mass. For the map's **contract** the
answer was closer to *the language cannot say this*: there is one corpus example
of `claim`, it is a two-room piece, and nothing anywhere demonstrates a contract
that takes on regions from a composed document. Everything in §5 was discovered
by refusal rather than by example.

---

## 4. What each part fails to owe the whole

spec-0040 §4 lists five things a part owes. Measured against the eight programs
as they stand.

### The one that dominates: five of eight declare no spatial contract

| zone | contract | claims | standable cells | anchors |
|---|---|---|---|---|
| Z0 barrow shore | **absent** | 0 | 2 854 | 37 |
| Z1 cliff road | present | 11 | 163 | 11 |
| Z2 gate ward | present | 13 | 1 787 | 17 |
| Z3 drowned ward | **absent** | 0 | 2 695 | 28 |
| Z4 chapel ward | present | 19 | 927 | 26 |
| Z5 hall keep | **absent** | 0 | 697 | 14 |
| Z6 cistern deep | **absent** | 0 | 3 168 | 14 |
| Z7 bell tower | **absent** | 0 | 6 312 | 37 |

Each of the five prints its own finding when expanded alone:

```
finding: this piece declares no spatial contract: no space, edge or envelope is
claimed, so every contract obligation examined nothing. What the building IS
remains unstated, and nothing downstream can check that a placed piece fits its
neighbours
```

The whole's red list is that sentence, cashed:

- `contract-coverage` — **15 855 of 41 412 standable cells** are in nothing the
  contract declares. The five zones' own standalone standable counts sum to
  15 726; composition adds the remainder at the boxes' own floors.
- `contract-anchors` — **130 of 184 anchors** land in nothing the contract
  declares. 37 + 28 + 14 + 14 + 37 = **130 exactly**, and the list is
  `anchor/bell-walk`, `anchor/ringing-floor`, `anchor/boss`, `anchor/wake`,
  `anchor/well`, `anchor/hall-door` and the rest of the five zones' anchors.
- five of the ten seams are undeclarable (§2).
- `contract-closure` — 21 boundary cells of `z2/gate/head` open north into Z3's
  box. Z2's opening and Z3's air are both real and the seam is physically
  happening; because Z3 declares nothing, the checker cannot account for it.

**The reduced probe proves the attribution.** Removing the four red seam edges
and leaving everything else identical leaves coverage at 15 879 and anchors at
130, unchanged. The debt is the missing contracts, not the seams.

### Per zone, in the fixed formula

**Z0 cannot supply the whole's arrival ground.** Its program lacks a spatial
contract and therefore any declared space; the map cannot claim part of Z0's box
because a `claim` takes the whole scope. The map's arrival ground therefore has
to be somewhere Z0 is not, which is a band between the flat and the gate, and
every block of that band pushes the wake point further from the tower than the
standoff `map-brief.md` derives. The nearest workaround is a zero-deep apron,
which leaves the map with no entry space at all.

**Z0 cannot supply the flat's water.** Its program lacks any water role — the
palette is `shore/bed`, `shore/sand`, `shore/silt` and no fluid — and its report
measures `fluid_cells: 0`. `map-brief.md` says that at the standing tide the flat
is under. The nearest workaround is a map-owned sheet over Z0's box, which the
map cannot write because splits partition.

**Z1 cannot supply both of its ends to the map's ground.** Its program declares
two `exterior` faces, north and south, 72 cells apart; the map's shore must
reach the south one and the map's cliff mass the north one, and the road lane is
one Z partition. Placing Z1 so its south face lands in the apron band (which is
what makes the arrival space one connected floor) puts its north face 70 blocks
from Z2's west opening. The nearest workaround is a map-built corridor from Z1's
north face through the cliff mass into the gate band's west strip — buildable,
about 60 cells of tunnel, and it proves one seam.

**Z1 cannot mate with Z2 by declared faces at all.** Z1 declares its way out on
its **north** face; Z2 declares its way in on its **west** face. A `split` gives
two boxes exactly one shared plane, and no plane is both a `Z`-face of one and an
`X`-face of the other. This is independent of layout. The nearest workaround is
the map-built corridor above, which is a `via` volume and not a mating of faces.

**Z2's face contract does not survive composition.** Its program declares two
`exterior` edges, west and north. Inside the map neither is on the piece's outer
face, and the checker refuses the claim by name (§5, R11 — demonstrated on Z4,
which fails identically). `exterior` is relative to the piece, and composition
changes which piece that is. The nearest workaround is to restate each as an
interior edge to a map space, which is what the map does for the three seams it
proves and cannot do where the far side is contractless.

**Z3 cannot supply a ward floor 1.9 below its causeway top.** Its program fixes
the causeway head three courses above the ward floor and exposes no param for
that offset (`quay_h`, `deck_h`, `kerb_h` and `water_depth` are all inside the
ward, none of them the head-to-floor rise). The nearest workaround is to place Z3
by its causeway seam and declare the ward datum at −3, which is what the map does
and what the guard now asserts.

**Z3 cannot supply a near side for the Z2 → Z3 or the Z3 → Z4 seam.** Its program
lacks a spatial contract. The nearest workaround is to route the Z3 → Z4 seam
through the map's own causeway, which the map does — and which is red, because
the map's causeway and Z4's west door are 200 blocks apart.

**Z4's own contract is the only one whose interior survived intact.** Nothing is
owed. Its nine interior edges, six spaces and three out-of-walk regions were
taken on unchanged under the `z4` prefix, and every one of them holds in the
composition.

**Z5 cannot supply either end of the two seams it is on.** Its program lacks a
spatial contract. Physically it is very close to right: its hall door is 9 cells
on its south face at local `y` 5, which lands at map course 22 — the same course
as Z4's terrace and as the map's upper shelf. The seam is one flat step and
nothing can say so. The nearest workaround is a map-owned shelf beside Z5's box,
which the map builds and which proves the seam *up to* Z4's terrace and stops
there.

**Z5's long axis cannot be turned without changing what Z5 builds.** Its
program's root reorients by `z(Largest)`, so a 76 × 11 × 11 box would give the
hall an east–west axis as `map-zones.md` asks — and would re-frame every
world-frame fill in it, which is the class `DW0736` refuses and `DW0742` reports
undecided. The nearest workaround is to accept the north–south axis, which the
map does.

**Z6 cannot supply the grille seam.** Its program lacks a spatial contract, so
`anchor/grille` (local `y` 5, its east face) has nothing to be an edge from. The
map guards that the grille comes out above Z3's bare floor and can prove nothing
further.

**Z7 cannot supply both `tide.md`'s tower foot and its belfry floor.** Its
program puts the belfry floor 25 courses above the tower foot where the brief
requires 16, and no param separates them (`storey` 6 × `storeys` 24 and
`base_height` 7 are the tower's own arithmetic, and the brief calls the zones as
they stand). The nearest workaround is to place Z7 by the tower foot at +14 and
declare the belfry at +39 — which is the number `map-brief.md` independently
derives for the crown, so the two documents agree after all.

**Z7 cannot supply the belfry as a place a body can be proved to reach.** Its
program lacks a spatial contract. Nothing the map can do supplies it: the map's
only reach into Z7 is a `claim` over the whole 41 × 48 × 125 box, and §5 records
what the checker says about that.

### The three obligations the parts mostly do keep

- **Refusal, not accommodation** — kept. Every zone refuses a box it cannot build
  in; none of them silently degraded at any point in this composition.
- **Renameable anchor stems** — kept, and needed. Six stems collide across the
  eight zones: `breach` (Z1, Z2, Z6), `causeway-head` (Z2, Z3), `gate` (Z2, Z4),
  `lampman` (Z0, Z2), `landing` (Z5, Z6), `stair-head` (Z2, Z7). All six are
  resolved by `rename_anchors` at the include site, on both sides, so no surviving
  name is ambiguous. 94 distinct stems, 184 anchors, no collision.
- **Datums as params** — **not** kept, and this is the quiet one. No zone declares
  its own floor offset as a param the map could bind and guard. The map's twelve
  `*_off` params are **measurements**, taken from the exported anchor map and
  cross-checked against the block grid (§6). A guard against a measured constant
  refuses a drifting *box*, and cannot refuse a drifting *zone interior*: if a
  zone's own rules move its floor, the map's identity still holds and the seam
  silently breaks. That is the residual, and it is stated rather than solved.

---

## 5. Every machine refusal, verbatim

Grouped by what was being attempted. Nothing here is paraphrased.

### R1 — a map that composes a contract-bearing zone cannot omit a contract

Attempt: expand the map with no `contract` block.

```
error: map: rule "z1/breach_hole" claims the region "z1/breach", which the contract never classifies as a space, an out-of-walk region or an edge's own volume. A claim the contract does not name resolves boxes that belong to nothing
```

Then, after classifying that one:

```
error: map: rule "z1/shore_walk" claims the region "z1/shore-mouth", which the contract never classifies as a space, an out-of-walk region or an edge's own volume. A claim the contract does not name resolves boxes that belong to nothing
```

This is a `validate` refusal, before any region or seed. All 43 regions claimed
by Z1, Z2 and Z4 had to be classified in the map's own contract before the
program would expand at all. **The map has no option to say nothing.**

### R2 — declining to declare a seam does not free the map from the opening

Attempt: drop the four red seam edges.

```
error: probe-noseams: invalid program: rule "z1/breach_hole" claims the region "z1/breach", which the contract never classifies as a space, an out-of-walk region or an edge's own volume.
```

Dropping the Z1 → Z2 edge orphans `z1/breach`, which is Z1's own claimed opening.
The map must classify it as something — a space, an out-of-walk region, or
another edge's volume — so a composition cannot quietly decline to have an
opinion about a part's declared way out.

### R3 — an edge class carries exactly the fields it means

```
error: parse …/map-cover.json: missing field `via` at line 188 column 7
```

A `stair` without treads is not writable.

### R4 — the map's own sea, unwalled

```
fluid-contained FAIL  bound 174728 DW0800: 117 way(s) out of a body of 174728 fluid cell(s) — 8,1,415 runs into 8,1,414 (minecraft:air); 8,2,415 runs into 8,2,414 (minecraft:air); 8,3,415 runs into 8,3,414 (minecraft:air); 8,4,415 runs into 8,4,414 (minecraft:air); 8,5,415 runs into 8,5,414 (minecraft:air); 8,6,415 runs into 8,6,414 (minecraft:air) (+111 more). A body of fluid is saturated and walled by construction: every cell a source, and nothing open beside or below it. This piece renders as still water in every tool here and runs on the first tick in the world
```

### R5 — a claim over a full-height column makes `rise` meaningless

```
contract-edge-proof FAIL  edge map/arrival--walk--map/causeway: declares rise 1 but the resolved boxes measure 0 (min_y(map/causeway) - min_y(map/arrival))
```

Both claims wrapped the whole `y` split, so both resolved to `min_y` 0. `rise` is
computed from the resolved boxes, so a map space must claim its **walkable band**
and not its column. Fixed by splitting the fill off and claiming only the band
above it.

### R6 — a seam whose two ends are not adjacent

```
contract-well-formed FAIL  edge z1/landing--drop--z2/gate/passage: its transit volume does not touch "z2/gate/passage" — a transit volume abuts both endpoints
contract-well-formed FAIL  edge map/causeway--stair--z4/walk: its transit volume does not touch "map/causeway" — a transit volume abuts both endpoints
contract-edge-proof FAIL  edge z1/landing--drop--z2/gate/passage: nothing falls from z1/landing to z2/gate/passage
contract-edge-proof FAIL  edge z4/stoop--drop--z2/gate/yard: nothing falls from z4/stoop to z2/gate/yard
contract-edge-proof FAIL  edge map/causeway--stair--z4/walk: the climb does not connect its two ends through its own treads
```

### R7 — an `exterior` edge does not survive composition

```
contract-exterior-faces FAIL  bound 2  edge z4/terrace--walk--exterior claims a way into the piece, but no cell of "z4/terrace" reaches the piece's outer face and it declares no opening that does — the face contract it exports is empty, so nothing downstream can mate with it
```

The map's first contract re-declared Z4's own `terrace → exterior` edge, because
that is what Z4 declares. Inside the map, Z4 is buried. **A part's ways in and
out are stated relative to the part, and composition is exactly the operation
that makes that statement false.** There is no construct for "this face now
abuts a neighbour" other than an interior edge to a declared space, which is why
the five contractless seams are undeclarable rather than merely unproved.

### R8 — the coverage and anchor debt

```
contract-coverage FAIL  bound 41412  15879 of 41412 standable cell(s) are in NOTHING the contract declares — floor the piece does not account for: [24,8,427] [24,8,428] [24,8,429] … (15879 in all)
contract-anchors FAIL  bound 184  130 anchor(s) land in nothing the contract declares — a campaign would bind content to a place the piece does not account for: "anchor/alcove" at [54,22,178], … "anchor/bell-walk" at [38,49,94], "anchor/boss" at [46,42,94], … "anchor/wake" at [44,9,432], …
```

### R9 — the closure the parts cannot close

```
contract-closure FAIL  bound 6636  space "z2/gate/head" is declared `open_top` but 21 of its boundary cell(s) are open air that no declared opening, neighbouring space or out-of-walk region accounts for: [34,13,293] [35,12,293] [35,13,293] [36,13,293] [37,10,293] [37,11,293] [38,10,293] [38,11,293] … (21 in all)
```

### R10 — the majority gate, and the acknowledgement it offers

```
contract-no-body-majority FAIL  bound 53034  28403 of 53034 standable cell(s) are out of walk — most of this piece is not play space. Say so in `no_body_majority_ack` if that is what it is, which does not weaken any region's own proof
```

Acknowledged. A whole map is mostly outer surface: the majority is `map/skyline`,
which the checker computes as `facade` — the air outside the piece reaches it —
and none of it is `posted`. The narrowing `grammar.md` §2d describes is exactly
what makes the acknowledgement legitimate here rather than a hatch.

### R11 — the whole-box claim, which is the obvious workaround and does not work

Attempt: claim each contractless zone's whole box as a map space, so
`contract-coverage` and `contract-anchors` bind. Four independent refusals, any
one of which closes it:

```
contract-well-formed FAIL  space "map/crown" has standable floor at y 18..60, which is 43 levels — a space is ONE floor (at most two consecutive levels, for a dais). Two levels are two places and a transition, and a transition is an edge that owes a `rise`
contract-well-formed FAIL  space "map/cistern" has standable floor at y 7..13, which is 7 levels — …
contract-well-formed FAIL  space "map/flat" has standable floor at y 8..20, which is 13 levels — …
contract-well-formed FAIL  space "map/gate" has standable floor at y 10..25, which is 16 levels — …
contract-well-formed FAIL  space "map/hall" has standable floor at y 18..26, which is 9 levels — …
contract-well-formed FAIL  space "map/ward" has standable floor at y 9..13, which is 5 levels — …
contract-well-formed FAIL  space "map/road-plinth" has standable floor at y 9..14, which is 6 levels — …
```

```
contract-well-formed FAIL  spaces "map/gate" and "z2/gate/passage" overlap on 1617 cell(s): [32,12,344] [32,12,345] [32,12,346] … (1617 in all)
contract-well-formed FAIL  spaces "map/road-plinth" and "z1/store" overlap on 100 cell(s): …
contract-well-formed FAIL  edge z1/foot--stair--z1/road: its transit volume overlaps space "map/road-plinth" on 14 cell(s) … A stair's treads and a drop's column belong to the edge, not to either end
contract-well-formed FAIL  edge map/arrival--walk--z1/foot: its opening claims cells that are inside space "map/road-plinth". An opening is a hole through a boundary, not a piece of the room it opens
```

```
contract-closure FAIL  space "map/cistern" is declared `open` but 3166 of its standable cell(s) have this piece's own blocks overhead ([26,7,48] [26,7,49] …) — a roofed room cannot be downgraded out of closure
```

```
contract-no-body FAIL  out-of-walk region "z1/teeth" (1704) qualifies for NOTHING: its own boundary is not closed (not `sealed`), it holds no anchor covering its cells (not `posted`), and the air outside the piece does not reach it or it nests inside a space (not `facade`). The author's reason was "the rock teeth in the surf at the cliff's foot -- what the drop ends on, and never ground the road offers a body"
contract-no-body FAIL  out-of-walk region "z2/gate/wall-head" (576) qualifies for NOTHING: …
```

That last pair is worth its own sentence. **A part's out-of-walk classification
does not survive composition either.** `z1/teeth` and `z2/gate/wall-head` both
earn `facade` when their zones are expanded alone, because the air outside the
piece reaches them. Inside the map they are buried, the kind they earned
evaporates, and the region qualifies for nothing — with the author's own reason
quoted back. Nothing in spec-0040 anticipates this.

### R12 — the escape hatch, and how far it gets

Attempt: declare each contractless zone's whole box an **out-of-walk region**
instead of a space — "no body goes here" over the bell tower, the hall, the
cistern, the ward and the shore. This is the cheapest possible green and it is
exactly the shape a review is supposed to catch, so it was run to see whether the
checker can.

It passes four gates:

```
contract-no-body pass  bound 13  13 out-of-walk region(s), every one earning a computed kind: 2182165 cell(s) facade, 293 cell(s) posted, 40000 cell(s) sealed
contract-anchors pass  bound 184  184 anchor(s), every one landing in a contract element: 3 in a bar, 143 in a no_body, 29 in a space, 9 in a via
contract-closure pass  bound 6636  6636 boundary cell(s) examined; every one is accounted for
contract-no-body-majority pass  bound 41412  34698 of 41412 standable cell(s) are out of walk, acknowledged
```

The 40 000 sealed cells are Z6's whole box: the cistern is buried, so its union
**is** closed, so it earns `sealed` for free — and being unreachable is the
property that made it a finding. The `facade` cells are Z0, Z3 and Z7's boxes:
they are open to the sky, so the air outside reaches them, for free.

**Taken all the way — every space but the entry reclassified, every edge dropped
— the hatch closes**, and it closes on the one box that is neither buried nor
open:

```
contract-no-body FAIL  bound 53  out-of-walk region "map/gate" (25200) qualifies for NOTHING: its own boundary is not closed (not `sealed`), it holds no anchor covering its cells (not `posted`), and the air outside the piece does not reach it or it nests inside a space (not `facade`). The author's reason was "PROBE: blanket out-of-walk"
contract-closure FAIL  bound 0  no space declares an envelope this gate can examine — nothing is `enclosed` or `open_top`, so closure proved nothing
```

So the answer to *could the defect itself produce the opt-out's proof* is
**partly yes, and the machine says which part**. A fully buried box supplies
`sealed` for free; a fully open box supplies `facade` for free; a box that is
half cut into rock supplies neither, and that is what refuses. The zero-binding
rule fires correctly alongside it: closure reports `bound 0` and calls it a fail
rather than a pass.

### R13 — the render layer's own refusals, both of which said what to do next

```
DW0721 [error] …/z4-chapel-ward.json is a single-template prefab's metadata, not a tile-set manifest — render it by passing the `.nbt` beside it
DW0721 [error] view `cutaway=x`: use true or false
```

### R14 — the audit's binding refusal

```
error: …/design/programs/map.json: no entry in zones.json names it and no zone program composes it, so it is a program nothing expands and nothing checks
```

---

## 6. The measurements, and how each was cross-checked

**The twelve per-zone floor offsets are the load-bearing measurement of this
composition** — every box's vertical placement is computed from them — so they
were taken twice by unrelated instruments.

- *Method A*, which was used to place the boxes: the `anchors` map of each zone's
  exported prefab metadata, read as JSON.
- *Method B*: the standable-cell `y` histogram recomputed from the `.nbt` block
  grid by a parser written for this run (`nbtread.py`, in scratch), which shares
  no code with the toolchain and reads the gzipped NBT directly.

Every offset agrees. The busiest floor level in each zone is exactly the anchor
level Method A used: Z0 `y` 4 (1 611 cells), Z1 `y` 13 (115) and `y` 8 (13),
Z2 `y` 4 (581) and `y` 2 (126), Z3 `y` 1 (1 864) and `y` 4 (229), Z4 `y` 5 (530),
Z5 `y` 5 (600), Z6 `y` 4 (3 001), Z7 `y` 7 (2 180).

The two methods' **totals** do not agree exactly, and the disagreement is stated
rather than smoothed: Method B counts 697 and 6 312 for Z5 and Z7 — exact matches
— and over-counts the other six by 0.1 % to 9.5 %, because its passability
heuristic treats bars, fences, carpets and doors as passable where the engine's
`standable` does not. The measurement being relied on is the floor **level**, on
which the two agree cell for cell.

### Determinism

Two expansions of the massing composition, in two processes, into two
differently-named directories, compared three ways:

| method | result |
|---|---|
| `cmp` on each of the 42 output files | 42 byte-identical, 0 differing |
| `sha256` of the concatenated 40 tile files, hashing **contents** and never paths | `9809ee0679cb9418df2d066f27478e44bff74407e9c8f8f5f36d44cfee76fe11` both runs |
| the independent NBT parser, cell by cell over the reassembled model | 2 479 968 cells, **0 differ** |

The map program of record is red and writes no prefab, so its determinism can
only be checked on the expansion report: byte-identical across two processes,
`sha256:91ec8a20…` both runs. That is the weaker check and it is labelled as such.

### The standoff

`map-brief.md` derives the viewing distance twice — `38.58 / tan 27° = 75.7 m`
and `D/H = 2 → 77.2 m`, 1.9 % apart — and calls 80 blocks the figure of record.
Measured on the composition, from `anchor/wake` to `anchor/bell-walk`:

| distance | rise | subtends |
|---|---|---|
| wake → gate front, 83 blocks | 38.4 | 24.8° |
| wake → belfry, 338 blocks | 40 | **6.7°** |

The apron band was cut from 50 to 6 to bring the first figure inside the brief's
range. The second figure cannot be moved: the zone boxes between the flat and the
crown are 56 + 60 + 33 + 76 + 125 = **350 blocks** of `Z` along the route, a
`split` partitions, and the two zones that could be nested side by side (Z4 at 27
wide, Z5 at 11) still leave 317. **The whole cannot be seen as one object from
its own standpoint at these part sizes, and no layout fixes it.**

---

## 7. What the toolchain was like to use

**Where a document told the truth.** `grammar.md` is the reason this composition
exists at all. §5c's `include` section, §2d's contract tables and §2's "the order
of the splits" are each written as though someone had already made the mistake
they prevent, and all three held. The corpus tables in §5c — every zone's params,
anchors and what it composes — were the working reference throughout. §2's item 4
(a world-frame role does not turn when `largest` turns the scope) is what stopped
the transposed-Z5 idea before it cost anything.

**Where a document misled, and it is one specific line.** spec-0040 §3 says the
composition manifest is a `composition` block in `zones.json`, and AC1 says
`delve-grammar audit --campaign-root` expands the map at that block's region and
seed. It does not. Adding the block changes nothing: the audit still reports
`map.json` as "a program nothing expands and nothing checks". What **does** bind
it is an ordinary entry in the `zones` list, which makes the audit expand the map
inside its composition, judge it with the same gates, and total the include
surface (`include bound 8 over 1 campaign program(s)`). Both are now in
`zones.json`, and the `zones` entry is the one that invokes anything. This is
the UNRUN shape exactly: the mechanism named as making composition impossible to
skip is the one that is not there, and adding the artifact it names would have
looked like compliance while binding nothing.

The same spec's AC8 — `coverage` counts the include surface with a binding count
and a corpus program demonstrates it — is also unmet: `include` appears zero
times in the coverage report, and no library program writes one.

**Where a refusal said what to do next.** Almost everywhere, and this is the
strongest thing about the toolchain. `DW0721` on a tile-set manifest names the
file to pass instead. The claim-classification refusal names the rule, the region
and what a contract may classify it as. `contract-well-formed` does not say "a
space is wrong", it says *"has standable floor at y 18..60, which is 43 levels —
a space is ONE floor … and a transition is an edge that owes a `rise`"* — the
verdict, the number, and the construct to reach for. `contract-edge-proof` prints
`min_y(b) - min_y(a)` with both operands, which is what turned four wrong
declared rises into four right ones in one pass. `contract-no-body` quotes the
author's own reason back at them when the region qualifies for nothing, which is
the difference between an error and an argument.

**Where a refusal did not.** Two.

- `contract-coverage` names a count and the first eight cells of 15 879. There is
  no way to ask *which regions those cells are in* — the attribution to the five
  contractless zones had to be established by arithmetic on their standalone
  counts and confirmed by re-running with the whole-box claims on and watching
  the number fall. A per-space or per-included-prefix breakdown would have
  replaced an afternoon with a line.
- The **absence** of a refusal in one place. `exterior` edges are checked for
  having cells on the piece's outer face — but a composition that inherits a
  part's `exterior` edge is doing something categorically wrong, and it is caught
  as an empty face rather than as "this edge came from a document you composed".

**A flag that is recorded as applied and does nothing.** `--view
name=…,cutaway=true` on the composed map produced a PNG byte-identical to the
same view without it, while `shots.json` records `"cutaway": true`. Three
controls bound it: the same flag on the same face visibly cuts a single-template
zone (Z4, 27 × 12 × 33), a two-tile zone rendered from its manifest (Z2), and a
2 × 2 × 2 tile grid (Z0 expanded at 60 × 56 × 60). No mechanism is claimed here.
What is claimed is that the shot manifest asserts something the bytes do not
support, which is a claim nothing downstream re-checks.

**A self-caught error, recorded because the method is the point.** The first
reading of the above was "cutaway is inert" — a toolchain finding, from one
observation. The cross-check on a subject with a known interior reversed it
within a minute. The rule that saved it is the project's own: when a measurement
is the deliverable, take it a second way before reporting it. The same rule
caught a second one earlier the same run — an NBT parser that misparsed silently
because `d[read_name()] = read_payload()` evaluates the payload first in Python.
Both were plausible wrong answers rather than errors, which is the class that
gets reported.

**Speed is not a constraint, as spec-0040 §1.3 says.** 2.5 s to expand 2.5 M
cells with eight zones composed and every gate run; 46 s to render 271 shots of
the whole map.
