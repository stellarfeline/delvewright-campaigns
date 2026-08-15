# The eight zones inside the whole

Where each zone sits in Halgrave's massing, at what height against the single sea
plane, and which of its faces is exterior and therefore in the silhouette. This
is the document a composition program is written from.

It **states where a zone sits; it does not adjudicate whether it fits.** Where
placing a zone needed a judgement, the fact that forced the judgement is written
down at the end and the judgement is left out.

Heights are metres against the **standing tide**, `0.0`, the datum `tide.md`
fixes. Compass: the mainland and the causeway are **south**; the sheer seaward
cliff is **west**; the rock's crown and the tower are **north**; the ward's
breached sea-wall is **east**.

## The zones

| zone | what it is in the massing | where on the rock | floor | exterior faces |
|---|---|---|---|---|
| **Z0 冢泽潮滩** Barrow Shore | the ground the rock stands out of | the tidal sand south and south-west of the crag, running off-site south as the causeway | −1.2 | all of it — Z0 is open sky and open sea, and it is the standpoint the front elevation is drawn from |
| **Z1 崖道** Cliff Road | a cut line across the rock's seaward face | the west cliff, climbing north from the flat's north-west shelf and bending east into the rock | +4.0 main ledge; +2.0 at the K2 gap | the whole west elevation. Read at distance as one thin horizontal scratch on an otherwise unbroken dark cliff |
| **Z2 门楼** Gatehouse | a squat wide block built into the rock's south foot | at the causeway head, dead ahead of a player standing on the flat | +2.5 passage; +1.8 channel invert | the south gate front, the flanking wall the breach is in, and the roof. The gate front is the second band of the silhouette |
| **Z3 下沉外庭** Drowned Ward | a basin sunk into the rock's low eastern lobe | behind (north of) the gatehouse, filling the east lobe; open to the sea through the breached sea-wall on the east | −1.5 floor; +0.4 causeway top | roofless, so its curtain wall, its two arcade runs and the water-gate tower's peaked roof are all in the silhouette, standing over the gate front and behind it |
| **Z4 礼拜堂中庭** Chapel Ward | the priory's cloister, on the upper shelf | north-west of and above the ward; the banded door on its south side looks down over the ward and the gatehouse yard | +9 | roofless, so its four arcade ranges and their broken arch-heads are the fourth band. Its south range is the face seen from below |
| **Z5 大厅与主楼** Hall & Keep | the one intact roofed building | north of the cloister, higher, long axis east–west | +12 | the roof and gable, and the slit-windowed flanks. The only solid dark shape in the silhouette below the tower |
| **Z6 深蓄水池** Cistern Deep | a brick vault cut into the rock, under the upper half of the site | beneath the upper shelf and the ward's rock, running north-east; the well at its deep north end | −0.15 floor; −2.3 well silt bed; −2.6 supply-channel invert | none, except two apertures: the **collapse shaft**, a hole in the paving of the upper ward, which is on the site plan and not on any elevation; and the **grille (S4)**, in the ward's rock face |
| **Z7 钟塔** Bell Tower | the crown, and the whole top of the silhouette | at the head of the cobbled ramp on the rock's north crown, standing clear of everything | +14 ramp and tower foot; +30 belfry floor | all four faces, from the ramp head up. The belfry is open on all four and the sky shows through it |

## Two things about the silhouette that are placements, not description

- **The tower stands clear.** Z0 to Z5 step upward south to north; Z7 does not
  step, it rises. The contrast is what makes the rock recognisable from the shore
  at a distance where no detail survives, and it is a fact about where Z7 is put:
  set back north of Z5, on higher ground, not abutting it.
- **Everything must be visible from the belfry.** `tide.md` gives Z7 the view of
  the whole rock at the Dead Ebb — every zone the player has crossed, visible and
  changed. That places Z0, Z1, Z2, Z3, Z4, Z5 and Z6's collapse shaft inside one
  downward view from +30: the site is a compact stepped mass, not a chain.

## The seams between zones

Where one zone hands the player to the next, and at what height.

| seam | from | to | the move |
|---|---|---|---|
| Z0 → Z1 | flat, −1.2 | ledge, up to +4.0 | the flat ends at cliff and one cut ledge starts up it |
| Z1 → Z2 | ledge, +4.0 | passage, +2.5 | a **fall** through the breach in the gatehouse's outer wall. `zones.json` declares Z2 `allow_falls` |
| Z2 → Z3 | passage, +2.5 | causeway top, +0.4 | down, inward, onto the raised spine across the water |
| Z3 → Z4 | ward, −1.5 / arcade top | cloister, +9 | up the ruined arcade into the water-gate tower at shutter height, down inside it, and up through the rock |
| Z4 → Z5 | cloister, +9 | hall, +12 | up, north, out of the cloister's north range |
| Z5 → Z6 | hall, +12 | cistern, −0.15 | the descent stair. `TIDE-3` fires on it |
| Z6 → Z3 | cistern, −0.15 | ward floor, −1.5 | **S4**, the grille broken outward, its sill about 1.35 above the ward's bare floor |
| Z3/Z4 → Z7 | cloister, +9 | tower foot, +14 | the cobbled ramp, climbing north-east between the collapsed low buildings of the upper ward |
| Z2 ↔ Z0 | passage, +2.5 | flat, −1.2 | **S1**, the portcullis: the gate becomes the front door and opens straight down onto the sand |
| Z4 → Z2 | cloister, +9 | gatehouse yard, ~+2.5 | **S3**, the banded door, opened from the chapel side |

## Facts that forced a judgement, recorded without the judgement

These are the places where writing down a zone's position required deciding
something this document is not the right place to decide. Each is stated as the
measurement or the quotation that forced it.

1. **Z7's declared extent against its declared heights.** `tide.md` puts the
   tower approach at +14 and the belfry floor at +30, a rise of 16. `zones.json`
   declares Z7's region as **41 x 14 x 125** — fourteen high and a hundred and
   twenty-five long. The program's `climb` parameter is `9`; its palette carries
   `door`, `flight`, `hearth`, `loft`, `margin`, `plinth`, `ring`, `shaft` and
   `tee` roles and no bell and no belfry; its start rule expands
   `tower → tower_plan → upper_chain → upper_storey`.

2. **Z0's declared extent against its written content.** `beats.md` gives Z0 a
   half-mile of open flat, a cairn field of one heap per recovered body, a
   tide-stake line, and at the Dead Ebb several hundred of the answered standing
   in the silt below that line. `zones.json` declares Z0's region as
   **19 x 6 x 24**.

3. **Z2's upper storeys.** `beats.md` requires the murder-hole floor above the
   passage as a real reachable storey, and the gatehouse roof above that as the
   ground the Gatewright is fought on. `zones.json` declares Z2 as
   **20 x 10 x 84**; the program's `gate/head` is `4` and `gate/haunch` is `2`.

4. **The descent from Z5 to Z6.** The hall floor is +12 and the cistern floor is
   −0.15, a descent of 12.15 that `quests.md` places at CP-15 and `tide.md` binds
   `TIDE-3` to. Measured from their own declared floors, Z5's region
   (**11 x 11 x 76**) reaches +23 and Z6's (**40 x 10 x 100**) reaches +9.85.

5. **S3's drop.** `beats.md` says the banded door, opened from the chapel side,
   "drops the player straight back into the gatehouse yard", and that the view
   through it as it swings is the drowned ward below going under. The chapel ward
   is +9 and the gate passage is +2.5.

6. **Z3's water.** The ward floor is −1.5 and the gate sill that admits it is
   +2.5. `tide.md` requires that nothing hold a level of its own and that every
   wet volume be the sea reached through a broken wall. `GENERATION.md` records
   Z3 as the campaign's one open machine finding: `fluid-contained` reds with
   `DW0800`, 380 ways out of a 2304-cell body of water, and states the answer is
   a design answer about where the ward's water is walled and where it spills.

7. **Z4's produced topology against its position here.** This document places Z4
   as a roofless cloister on the upper shelf, from `beats.md` and the concept
   image. `GENERATION.md` records the produced piece as an enclosed hub, states
   that the divergence from the concept's open cloister is deliberate and the
   topology fixed, and records 47.9% of the piece as inert `margin`.

8. **Z1's seaward elevation.** This document puts Z1's cut ledge in the west
   elevation as the rock's only broken line. `GENERATION.md` records that the
   produced ledge does not overhang — the walking surface is flush with the rock
   below it and the seaward face is a flat plane with a seam — and that the
   concept's iron stanchions and chain rail have no role and no rule in the
   program.
