# Halgrave — the site plan, and where the eight parts stand against it

`../programs/map.json` is Halgrave's site plan: the map program of spec-0040 §3,
whose top-level splits are the plan, whose `params` are the whole-map datums, and
whose `include` list is which zones it composes. This page is the derivation of
every number in it, fact by fact against `map-brief.md`, so the plan can be
checked without re-deriving it — spec-0040 §3c link 1 names that reading as the
design gate's, because it is the one link no machine can take.

The eight zones predate the plan, so this is §3c's transitional class: **the plan
is derived from the whole's brief and never from the parts' extents, and every
pre-existing part confronts its allocation at the map's first expansion.** The
confrontation is the last section, and it is the honest output of a correct plan
meeting parts that were sized before it existed.

Compass, as `map-zones.md` fixes it: the causeway and the mainland are **south**,
the sheer seaward cliff is **west**, the crown and the tower are **north**, the
ward's breached sea-wall is **east**. So the region's `X` runs west to east, its
`Z` runs south to north, and heights are metres against the standing tide, `0.0`.

---

## 1. The region: 70 × 44 × 150

### Z = 150 = `flat_run` 80 + `rock_run` 70

`flat_run` is the brief's own figure of record, quoted:

> **The figure of record: the flat's long axis is 80 blocks**, from the wake
> point to the gatehouse's foot.

`rock_run` is derived from two of the brief's own sentences, in the brief's own
idiom. The sentence that makes it a constraint rather than a taste:

> That is a constraint on the plan, not a piece of prose: **the site is a compact
> stepped mass, not a chain.**

and the reading rule the brief already uses to turn "reads as one object" into a
number:

> A building is read as one whole object, rather than as detail or as landscape,
> when it subtends about **27°** in the vertical. … the same reading is
> conventionally written `D/H = 2`.

Applied to the belfry's view of the rock, which is the view the compactness
sentence is about. A standing eye on the belfry floor is at `+30 + 1.62 = +31.62`
(the brief's own eye height), and the lowest ground it looks down on is the ward
floor at `−1.5`, so `H = 33.12`. Then `33.12 / tan 27° = 65.0` and
`2 × 33.12 = 66.24` — **two methods 1.9 % apart**, which is what says neither is
a units error, and the same 1.9 % the brief's own standoff got. The figure of
record rounds up to the next round number exactly as the brief rounds 75.7/77.2
to 80: **`rock_run` = 70**.

Checked against a bound the brief derives by a different rule at a different
angle, so its failure mode is unrelated:

> The belfry has to see the flat's far end in one downward look, and a 31.2 m
> drop at 10° of depression reaches **177 m**.

Tower to wake point is 150, and `150 ≤ 177`.

### X = 70

> An oval crag, **long axis south-west to north-east**.

A long axis at 45° to the grid projects equally onto `X` and `Z`, so the crag's
axis-aligned plan box is **square**. That is the numeric form of "a compact
stepped mass, not a chain": the mass's plan aspect is **1 : 1**, against the
1 : 5.5 the first composed citadel measured. The flat's played band is 40 wide —

> **The cross axis is 40 blocks.**

— and lies inside it, pushed against the west edge, so that the flat is "south
and south-west of the crag" and its north-west corner meets the cliff where the
cut road begins. The 30 east of it is the open sea the ward's torn east wall
opens onto, which is why the ward "holds sea rather than a pool".

### Y = 44 = `crown_y` 39 − `invert_y` (−3) + `base_course` 1 + 1

> the crown is at **+39**.

is the top. The bottom is the deepest plane the brief names, the cistern's
supply-channel invert at `−2.6`, transcribed to whole blocks as `−3`; and one
course of rock beneath it, because

> a brick cistern is **cut into the rock**

and a vault cut into rock has rock under its invert.

### The vertical datums

Every plane of the brief's massing table is a `param` of the plan, transcribed to
whole blocks by rounding half away from zero. `tide_y` = 4 is the region-local
`Y` of the standing tide, so a plane at `+h` is the local layer `tide_y + h`.

| brief | metres | param | local Y |
|---|---|---|---|
| supply-channel invert | −2.6 | `invert_y` | 1 |
| well's silt bed | −2.3 | `well_bed_y` | 2 |
| the drowned ward's floor | −1.5 | `ward_floor_y` | 2 |
| the tidal sand | −1.2 | `flat_floor_y` | 3 |
| the cistern's floor | −0.15 | `cistern_y` | 4 |
| **the standing tide** | 0.0 | `tide_y` | 4 |
| the causeway top | +0.4 | `causeway_y` | 4 |
| the gate passage | +2.5 | `gate_y` | 7 |
| the cut ledge | +4.0 | `road_y` | 8 |
| the cloister's paving | +9 | `cloister_y` | 13 |
| the keep's floor | +12 | `hall_y` | 16 |
| the upper ward, the tower foot | +14 | `upper_ward_y` | 18 |
| the belfry floor | +30 | `belfry_y` | 34 |
| the crown | +39 | `crown_y` | 43 |

---

## 2. What is an identity and what is a distribution

The brief fixes the whole's outer extent and every height. It fixes **no interior
plan dimension of the rock**. Those are two different kinds of number and the plan
never mixes them silently:

- An **identity** is a brief fact. It is a `param` and it is guarded by a `cmp`
  over the map's own region or a top-level split, so a plan that violates it
  refuses at expansion naming both numbers. The rules `halgrave`,
  `brief_plan_is_square` and `brief_vertical_range` are one identity each, so a
  refusal names the fact that failed rather than a compound guard that names
  nothing.
- A **distribution** is the plan sharing out a brief-fixed total the brief does
  not divide. It is written as an expression over the box being split, so it
  cannot sum past what the brief fixed — a `split` partitions.

The gap is named rather than papered over: **the absolute plan size of the rock's
three lobes and of its spine's Z bands is not in the design of record.** The plan
distributes them; revising that distribution is a §3c plan revision, which is one
visible diff line and re-runs the identities. Fixing them as brief facts is a
design-gate decision about the whole, and it is the one thing this page asks for.

Every band's height follows one rule, stated once and obeyed everywhere: **a
band runs from the region's base to the plane of the ground that stands above or
behind it.** The flat is bounded by the cut road at +4.0, "above and outside
everything"; the seaward face by the crown's ground at +14; the gatehouse, the
drowned ward and the cistern by the cloister's paving at +9, which is why the gate
front is the silhouette's second band under the cloister's fourth, and why the
cistern's vault crown lies under the paving it collapses through.

---

## 3. The plan

```
region 70 x 44 x 150                       X west→east · Y base(−4)→crown(+39) · Z south→north

split Z  [ 80 flat_run | 70 rock_run ]
├── THE FLAT ................................................ 70 x 44 x  80
│   split X  [ 40 flat_cross | 30 ]
│   ├── the flat's band ..................................... 40 x 44 x  80
│   │   split Y  [ 8 = tide_y + road_y | 36 ]
│   │   ├── Z0  barrow shore ............................ ▣ 40 x  8 x  80
│   │   └── sky
│   └── the open sea ....................................... 30 x 44 x  80
│       seabed to the flat's floor, water to the standing tide, air above
└── THE ROCK ................................................ 70 x 44 x  70   (square in plan)
    split X  [ 17 | 36 | 17 ]                    the brief's own three lobes
    ├── THE SEAWARD FACE .................................... 17 x 44 x  70
    │   split Y  [ 18 = tide_y + upper_ward_y | 26 ]
    │   ├── Z1  cliff road .............................. ▣ 17 x 18 x  70
    │   └── sky
    ├── THE SPINE .......................................... 36 x 44 x  70
    │   split Z  [ 35 | 35 ]              "under the UPPER HALF of the site"
    │   ├── the south foot ................................. 36 x 44 x  35
    │   │   split Y  [ 13 = tide_y + cloister_y | 31 ]
    │   │   ├── Z2  gatehouse ........................... ▣ 36 x 13 x  35
    │   │   └── sky
    │   └── the upper half ................................. 36 x 44 x  35
    │       split Y  [ 13 = tide_y + cloister_y | 31 ]
    │       ├── Z6  cistern deep ........................ ▣ 36 x 13 x  35
    │       └── the upper ground ........................... 36 x 31 x  35
    │           split Z  [ 17 | 18 ]
    │           ├── Z4  chapel ward ..................... ▣ 36 x 31 x  17
    │           └── the crown .............................. 36 x 31 x  18
    │               split Z  [ 9 | 9 ]
    │               ├── Z5  hall & keep ................. ▣ 36 x 31 x   9
    │               └── Z7  bell tower .................. ▣ 36 x 31 x   9
    └── THE EAST LOBE ...................................... 17 x 44 x  70
        split Y  [ 13 = tide_y + cloister_y | 31 ]
        ├── Z3  drowned ward ............................ ▣ 17 x 13 x  70
        └── sky
```

Where each split comes from:

| split | the sentence it comes from |
|---|---|
| flat ǀ rock | "The figure of record: the flat's long axis is 80 blocks, from the wake point to the gatehouse's foot" |
| the flat's band ǀ the open sea | "The cross axis is 40 blocks" · "the tidal sand south and south-west of the crag" · "the sea is ONE flat plane at height 0.0 everywhere" |
| the rock's three lobes | "**West and south-west**: sheer cliff to open sea … **East**: the low lobe of the rock … **North**: the crown, highest ground, and the tower" |
| the south foot ǀ the upper half | "a brick cistern is cut into the rock" **under the upper half of the site** |
| the cistern beneath ǀ the ground above | "**The cistern is beneath, not beside.**" |
| the shelf ǀ the crown | "the cloister on the shelf above the ward" · "the hall north of the cloister, higher" |
| the hall ǀ the tower | "**The tower stands clear.** … set back north of Z5, on higher ground, not abutting it" |
| every band's height | "Seven stacked ground planes, and they are not one plane. **A composition that lays these out at a single level has not built Halgrave.**" |

---

## 4. The three facts a plan drawn from boxes loses

`map-brief.md` names three, and each is a thing the plan has to keep rather than
a thing it can describe. Where the plan keeps it:

1. **The ward is a hole, not a floor.** The plan does not put the ward and the
   gate on one plane: the drowned ward is its own lobe, its floor at
   `ward_floor_y` = −2 and the gate sill that admits it at `gate_y` = +3, four
   metres above it. Both are `param`s of the map, so the drop is one subtraction
   over two map-owned numbers and not two zone constants that happen to differ.
2. **The cistern is beneath, not beside.** The cistern's box is the under-croft
   of the spine's upper half — a `Y` split of the same footprint the cloister,
   the hall and the crown stand on, not a `Z` band beside them. It is the one
   split on this plan that the brief states in those words.
   **What the plan does not yet keep:** the collapse shaft. The shaft is one
   continuous void from the cistern's vault at +8 to the upper ward's paving at
   +14, and a split tree partitions, so the shaft crosses two boxes and belongs
   wholly to neither. Under spec-0040 §4 its upper length is the map's own
   connective work, declared as a seam edge with its `via` cells — which is
   §5's owed work, not a defect of the split.
3. **The tower is a climb, not a room.** The tower's band runs from the
   cloister's plane at +9 to the crown at +39 — 31 courses, the whole of the
   16 m climb from the ramp head at +14 to the belfry floor at +30 with the
   belfry storey above it. The plan guards it: the crown's band refuses unless
   `dim(y) ≥ crown_y − cloister_y + 1`.

---

## 5. Where the eight parts stand against the plan

Measured, at the pinned engine, over the plan as written. The allocated box is
the engine's own reading of the plan's splits, not arithmetic done beside it.
Every row is a `DW0806` debt: the row and the allocation are two claims about how
big one part is, and where they disagree the box a part was reviewed in is not
the box it is built in.

| zone | its row | the plan allocates | ΔX | ΔY | ΔZ | at its allocation |
|---|---|---|---|---|---|---|
| Z0 barrow shore | 40 × 18 × 80 | 40 × 8 × 80 | 0 | −10 | 0 | refuses: needs `y ≥ 14` |
| Z1 cliff road | 16 × 24 × 72 | 17 × 18 × 70 | +1 | −6 | −2 | **builds** |
| Z2 gatehouse | 25 × 18 × 56 | 36 × 13 × 35 | +11 | −5 | −21 | refuses: needs `z ≥ 48`, `y ≥ 18` |
| Z3 drowned ward | 40 × 10 × 60 | 17 × 13 × 70 | −23 | +3 | +10 | refuses: needs `x ≥ 23` |
| Z4 chapel ward | 27 × 12 × 33 | 36 × 31 × 17 | +9 | +19 | −16 | refuses: its undercroft split needs 33 along z |
| Z5 hall & keep | 11 × 11 × 76 | 36 × 31 × 9 | +25 | +20 | −67 | refuses: its five ranges need `z > x + 60`, and it reads 36 × 9 |
| Z6 cistern deep | 40 × 10 × 100 | 36 × 13 × 35 | −4 | +3 | −65 | refuses: needs `x ≥ 36`, `z ≥ 92`; it reads 35 × 36 |
| Z7 bell tower | 41 × 48 × 125 | 36 × 31 × 9 | −5 | −17 | −116 | refuses: needs `x ≥ 25`, `y ≥ 48`, `z ≥ 113` |

Two things to read off it rather than around it.

**The deficits are in `Z`, and they are one shape.** The eight rows' depths sum
to 602 against a site 150 deep. Every §5b rule opens with `z(Largest)`, so a part
turns its length onto the longer horizontal axis of whatever box it is handed
(`grammar.md` §5c) — which is why Z2, Z5, Z6 and Z7 each report `dim:z = 36` at
their failure site, reading the 36 × 35 box turned. The parts were authored as
long runs because nothing had allocated them a box; **that is the same extent-
flowing-up shape the first composed citadel measured, arriving one level down.**
The remedy is each part's own revision under its own zone review, and it is a
round of content design with its own brief. It is not this page's to take.

**Z0 fits in plan and misses in section, and that is the plan working.** Its
40 × 80 is exact, because those two numbers are the brief's own and Z0 has
already been revised to them. Its height is not a brief fact at all — the brief
fixes no ceiling for the flat — so the plan bounds it by the one rule it bounds
every band by, and Z0 refuses. The repair is one of the two §3c moves and neither
is free: revise Z0, or add the flat's vertical extent to the whole's design of
record and re-derive.

---

## 6. What the design of record does not say, and one place it contradicts itself

Each of these is a design-gate item, not something the plan may settle for itself.

1. **No plan dimension of the rock is written down.** `map-brief.md` fixes the
   flat exactly, every height exactly, and a 177 m ceiling on the site's length.
   It fixes no width, depth or footprint for the crag or for anything on it. §1
   derives the rock's 70 × 70 in the brief's own idiom because a plan cannot be
   authored without it, and §2 keeps the interior shares visibly a distribution
   — but the derivation is a reading, and a reading is not a fact of record.
   Adding the rock's plan extent to the brief is what makes this plan checkable
   by someone who did not write it.
2. **`map-prompt.md` says the crag is not a grammar program.** Its triage list
   reads: *"The crag is in-house generator work or a surround layer, and it is
   not a grammar program. It is the largest single thing in the reference and it
   belongs to no zone."* spec-0040 §3b decides the other way — designed ground is
   content and is written in the DSL, and a landform of stepped axis-aligned
   masses reads as rock at playable scale. The plan follows the spec, and the
   triage line is stale against it.
3. **The map owes a massif and it has none yet.** Under this plan every rock cell
   falls inside some part's box, and the map's own writing is the sea, the seabed
   and the sky. The mass between and around the boxes — spec-0040 §4's "the mass
   no piece can know about" — has nothing to occupy while the parts are in debt,
   because connective geometry built across boxes that are about to move is
   invention. It lands with the whitebox, after the parts have been revised to
   their allocations.
4. **The parts' own contracts are restated here by hand.** `include` carries a
   composed document's claims but not its `contract`, and the destination must
   classify every claimed region or `validate` refuses — so `map.json` carries
   47 spaces, 23 out-of-walk regions and 59 edges copied under their prefixes.
   spec-0040 §4 names that restatement as the shell defect one level down and
   specifies contract adoption under `include` to end it; until that lands, this
   is what a composed map can be read at all. It also drags the map's own
   document version up to the highest any part's contract surface uses, which is
   how this document declares `1.7.0` while composing seven parts that declare
   `1.4.0`.
