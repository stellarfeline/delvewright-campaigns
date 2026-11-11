# Festival Day in Kelderby — generation record

## What the brief pinned, and what was invented

- Pinned: the owner's festival-day script (three acts, five soft-fail tasks A–E, the dusk fight, the night composed from six flags, the map it needs) and her notes on the town's pictures. The script is the design of record; `DESIGN.md` transcribes it and marks every line it authors.
- Invented: the order the clock jumps in, each task's window, which places are the fox's four hiding places and its den, the cast's lines, the classes, the farm district's layout.
- The script review (step 5b) does not apply: the story is the owner's, not the run's.

## Engine

- `delvec` 1.16.0, `dsl` 0.73.0, built from source in release profile from `stellarfeline/delvewright` `feature/festival-day` at `b4f61cd47` (cargo exit 0, 119 s, 4.0 GB peak). Earlier steps were authored at `eea5c7d997600bf19e5444a16081e58a3f96f647` (spec-0133, `dsl` 0.72.0) and `aa5484754` (spec-0134's first part). Dev mode; the skill page read is the revision's own.
- On the surfaces that have landed: the dusk waves scale with the party (`count {base, per_player}`); the castle's crossbows and starred rockets are handed out at dusk, sixteen or eight by the fireworks' fate; the keeper hands over her spyglass and the fox is first seen through it from the lamp room (`use-item`), which opens the chase; the key is taken off the fox at its den (`use-actor`, setting the flag the storeroom waits on); the cake is taken when a raider of either kind stands on the stage (`counts` over the stage, `body-enters`), and the ending reads it.
- Written but not emitted, on two engine defects of the `shot` surface: a `shot` trigger without a `prop` is refused (`DW1090`, "add a prop") and with one is refused (`DW0964`, "a shot has no cell to place a prop in"); and the target's station, which stands in the bell tower's opening where no body stands, is refused at detail (`DW0845`, which admits a no-body station only for a pit or a gate's answer). Task C (the clerk's bow, three hits, the bell rung, the bell's glow on the raiders at dusk) is in the author's source behind one switch and enters the documents when the pair agrees; the forecourt bell's station is placed.
- Not moved, though the surface has landed: the goats (task B): the census and `body-enters` are here, but the pen on the main street and the goats' three start points on the terraces are not yet built. The supply chests' food is task A's payoff and waits with A for boats.
- Also measured: the critical path's route proof does not cross a gap one cell wide at grade between two level floors (the lighthouse's broken stair); the same build with the stair whole walks every leg.
- Waiting on the branch: by-effect world edits (the night's lamps and bunting), the quorum, `give-item from` an actor (the key as an item), vehicles (task A's boats, the pig race).

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

## Build (step 8) — where it stands

The build of these documents refuses on two open items: the night's light (`DW0210`, above) and the lighthouse's broken stair (`DW0311`: the critical path's route proof does not cross a gap one cell wide even between two level floors). Every later gate was walked on a measurement copy of the same documents with the clock moved to the latest hour judged as day and the stair whole, each refusal fixed in these documents at its cause (`DW0921` pens, `DW0924` landings, `DW1033` and `DW0308` the ending's shots, `DW0430` the stair's treads, `DW0450` two townsfolk and the fox, `DW0478` the respawn, `DW0863` the storeroom). That copy now stops on `DW0807`, an engine defect: the PackTest templates for an `interact` and a `collect` objective that carries a `limit` assert an outcome whose gate reads the objective's expiry score, which the template never writes (`dw.x_light_the_lamp`, `dw.x_fetch_the_fireworks`). No ladder rung ran.
