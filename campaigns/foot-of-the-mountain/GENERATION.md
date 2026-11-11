# Festival Day in Kelderby — generation record

## What the brief pinned, and what was invented

- Pinned: the owner's festival-day script (three acts, five soft-fail tasks A–E, the dusk fight, the night composed from six flags, the map it needs) and her notes on the town's pictures. The script is the design of record; `DESIGN.md` transcribes it and marks every line it authors.
- Invented: the order the clock jumps in, each task's window, which places are the fox's four hiding places and its den, the cast's lines, the classes, the farm district's layout.
- The script review (step 5b) does not apply: the story is the owner's, not the run's.

## Engine

- `delvec` 1.16.0, `dsl` 0.72.0, built from source in release profile from `stellarfeline/delvewright` `feature/festival-day` at `eea5c7d997600bf19e5444a16081e58a3f96f647` (spec-0133, the timed beat). Dev mode; the skill page read is that revision's.
- Waiting on the branch: spec-0134 (small surfaces) and spec-0135 (vehicles). What each one carries for this delve is listed in `DESIGN.md`, *What the build carries now, and what waits*.

## The design record

The approved pictures of the replaced story showed it at late afternoon and at sunset; this day is played at 07:00, 10:00, noon, 18:00 and midnight. A picture approves the hour it was drawn at, so the old set cannot stand as this delve's approval and is removed with its record and its showcase cameras. The festival day's own design walkthrough has not been approved: the record is empty, which validation states as a zero and the staging gate refuses. The camera poses of the old set, with the owner's keep / drop / reframe notes, are in `design/generator/shots.json` for drawing pictures to look at.

## Placement (step 2)

- The farm district on the empty flank east of the town: a farm track off the end of lane 5 and six plots off it (wheat field, orchard, sheep fold, duck pond, cattle pen, barn), each a contact on the track. Drawn by `design/generator/farm.py`.
- The lighthouse gains the station `anchor/lamp-room`.
- The engine refuses crops in a piece (`DW0730`: farmland and wheat change after the proofs judged them), so the wheat field is drawn cut, its sheaves stood in stooks of hay.

## Content (step 5)

- Every objective is bound to the place it happens in (`layout-graph.json` `beats[]`), and the authored critical path is re-derived as the walk through those places in order.
- Windows: the lamp, 6000 ticks from reaching the lamp room's climb; the fireworks, 9600 ticks from the fox's first flight. Each is an expiry world the ladder waits out.

## Languages

`world.json` declares `zh-cn`. The sidecar is written in this run from the English documents through `delvec l10n-apply` (146 of 146 rows); no translation provider was configured.

## Light at night (step 8)

The night act is judged at the darkest sky the world reaches (effective 4). The build refuses (`DW0210`): 4634 of 74006 reachable cells of the island's ground outside every place stand below light 3, in some three hundred pockets under the island's tree cover (the fill's oak, birch and spruce strata), plus 39 cells in 24 places, each a cell or two under an eave or a canopy. Filling the empty flank with the farm district moved the first figure from 5070 of 78902 to 4634 of 74006: the dark ground is the woods, not the open land. The repair is a design choice between the woods and the night (`DESIGN.md` has no line for it yet), and is open.
