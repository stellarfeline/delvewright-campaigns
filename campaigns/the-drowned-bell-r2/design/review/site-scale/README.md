# Halgrave at scale — is there room to play in it?

`../../reference/map-site-plan.md` derives the site plan's every number from the
brief, and one of them is not a brief fact: **the rock's plan size.** The brief
fixes the flat exactly, every height exactly, and a 177 m ceiling on the site's
length; it fixes no width or depth for the crag. The plan's 70 × 70 is a reading
of the compactness sentence, and a derivation can show a number is faithful to
the brief without saying anything about whether it leaves room to play.

That question is answered by looking, not by arithmetic. These are the drawings
that make it answerable: **to scale, with a body on them, showing the contents
rather than the boxes.**

## The sheets

| sheet | what it shows |
|---|---|
| `01-site-plan.svg` | the whole region in plan at 1 block = 6 px — the box the plan hands each part, what that part declares laid in that box at true scale, the order of arrival, and a party of four standing on the sand. Every box carries the comparison of declared against offered — height, and the footprint whichever way round fits best — so the axis each part misses on is on the page |
| `02-parts-at-scale.svg` | the eight parts as the engine actually builds them, at the same scale: each part's own floor plan measured off an expansion at the region `zones.json` declares, with its allocated box laid over it and the engine's own words when it is expanded there |
| `03-section.svg` | the south–north section: the fourteen planes of the brief's massing table at the region-local layer `map.json` puts each at, the sixteen-block climb, and the tower zone's measured long section laid against the whole site's height and depth |
| `04-how-big-is-the-rock.svg` | the ruler. The same plan re-evaluated at `rock_run` = 70, 90, 97 and 110, with every part expanded at the box each size gives it |
| `05-a-body-in-it.svg` | six rooms at the storey their own anchors stand at, each with the party standing in it — the ledge, the causeway, the cloister, the hall, the cistern and the belfry, plus the unit: one player, four abreast, a door, a walk |

Why 90, 97 and 110 rather than a round ladder: 90 is the mid-point, **97 is where
the brief's own belfry sightline runs out** (`80 + 97 = 177 m`, and the same 18°
reading gives 102), and 110 is past it and is drawn so that being past it is
visible rather than described.

## How they are made

Three files, each with one job, and nothing on any sheet is typed in by hand:

- `alloc.py` evaluates `../../programs/map.json`'s split tree to the box each
  zone is allocated. It walks the rules the site plan declares, so a plan
  revision moves the boxes without anything here being edited.
- `measured.json` is what the engine measured: for every zone, the plan
  silhouette, a long section, a floor plan at each storey a declared space
  stands at, what is over a standing head there, the anchors, and the verdict
  when the zone is expanded at its allocated box. It is committed so the
  drawings regenerate without an engine.
- `draw.py` draws. `svgkit.py` holds the block grid, the scale bar and the
  body; `zonefacts.py` holds the strings transcribed from `beats.md`,
  `map-brief.md` and `map-zones.md`.

```
python3 draw.py                          # redraw the five sheets
rsvg-convert 01-site-plan.svg -o 01-site-plan.png    # and each raster beside it
```

Each sheet is committed twice: the `.svg` is the drawing, and the `.png` beside
it is the same drawing rastered at its natural size, so a reviewer opens a
picture the way the other review sets in this campaign are opened.

To rebuild the records — needs `delve-grammar`:

```
python3 measure.py measured.json <engine revision>    # expands + measures
python3 sweep.py                                      # rock_run 70..140
```

The records in this directory were measured with `delve-grammar` built from
engine revision **`f369ee5713651285dfc191a5df37b72467a144ec`**, named literally
because a version string is not an instrument name.

Every measured number was taken twice by methods that do not share a
calibration: the plan areas were read out of the NBT by `measure.py` and
compared against the engine's own `footprint_area` gate measurement (all eight
agree); the allocations were derived by `alloc.py` and compared against the
engine-measured table in `map-site-plan.md` §5 (all eight agree); the sweep's
result was re-derived by arithmetic on the plan's own vertical identity, which
runs no engine at all.

## What the sheets show

A reading, offered as one — the sheets are the instrument and this is not part
of it.

**Which way a part turns in its box is not asserted anywhere here.** It is a
property of the rule that opens on the scope rather than of the zone: §5 of the
site plan's derivation records four parts reading their box turned, and the
engine's own refusal for the flat names its 40 × 8 × 80 with `x → world x`,
untuned. So every comparison on these sheets is made in whichever orientation
fits best, which needs no assumption and is still decisive — where the best case
fails, no turn saves it.

**The rock's size is not what is stopping anything.** Sheet 4 expands every part
at the box every rock size from 70 to 140 gives it, and the set that builds does
not change: it is the cliff road, at every size, and nothing else. The plan
halves the rock's depth, halves it again, and halves it again, so the hall and
the tower each get an eighth of it — 9 blocks at rock 70, 18 at rock 140,
against a tower that declares 125. Growing the rock grows an eighth of it. And
the flat's box never moves at all, because both its plan numbers are brief facts
and its height is `tide_y + road_y`; it refuses on height, and the rock cannot
reach it.

The first refusal the site plan reaches is the flat's, at a box 8 blocks high
against a zone declaring 18, and that is what the zone-program audit reports
when it expands `map-halgrave` at 70 × 44 × 150. Sheet 1 puts the same three
numbers beside the same box.

**The parts are not too big for the site.** Their declared volumes sum to
440,336 blocks against a site of 462,000 — 95.3 % of it. They are the wrong
shape for the boxes the plan cuts, which is a different finding with a different
repair.

**One part is the size of the site.** Z7 declares 41 × 48 × 125 = 246,000
blocks, 53 % of the whole site on its own, and it is **taller than the site is**:
48 against a region height of 44 that `brief_vertical_range` pins to a brief
fact. Sheet 3 draws that as the four courses standing above the site's own
crown. No rock size reaches it, because the region's height does not depend on
the rock.

**Where there is room, and where there is not.** At the storeys the parts
themselves build, the belfry is a 15 × 15 room of standable floor — 201 cells —
with the bell hung in the middle of it: seven blocks across its lip, tapering to
three, nine courses of oxidised copper, with four courses of clear headroom
beneath. Its lip measures the `bell_side` its program declares and the clearance
measures `under_bell`, so "walked around, not sat on" is built and measures
right. The cistern carries 3,004 standable cells on one floor, 38 blocks across
between its walls, with its piers ranked over them. The hall's floor is 9 across
between its walls, so four abreast fits with five to spare. The cliff road's
walk is 2 wide, and a party of four goes down it in single file — which is that
zone's own design and reads correctly on sheet 5.

So the parts, at the storeys they build, are not short of room. What has no room
is the box the plan hands them.
