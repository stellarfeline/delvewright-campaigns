# Festival Day in Kelderby — generation record

## What the brief pinned, and what was invented

- Pinned: the owner's festival-day script (three acts, five soft-fail tasks A–E, the dusk fight, the night composed from six flags, the map it needs) and her notes on the town's pictures. The script is the design of record; `DESIGN.md` transcribes it and marks every line it authors.
- Invented: the order the clock jumps in, each task's window, which places are the fox's four hiding places and its den, the cast's lines, the classes, the farm district's layout.
- The script review (step 5b) does not apply: the story is the owner's, not the run's.

## Engine

- `delvec` 1.16.0, `dsl` 0.73.0, built from source in release profile from `stellarfeline/delvewright` `feature/festival-day` at `2da9bc5444a16288e24b4ddd17898060363191f3` (cargo exit 0, 125 s, 3.9 GB peak). Earlier steps were authored at `eea5c7d997600bf19e5444a16081e58a3f96f647` (spec-0133, `dsl` 0.72.0), `aa5484754` (spec-0134's first part), `b4f61cd47` and `0f0f9db12`. Dev mode; the skill page read is the revision's own.
- On the surfaces that have landed: the dusk waves scale with the party (`count {base, per_player}`); the castle's crossbows and starred rockets are handed out at dusk, sixteen or eight by the fireworks' fate; the keeper hands over her spyglass and the fox is first seen through it from the lamp room (`use-item`), which opens the chase; the key is taken off the fox at its den (`use-actor`) and handed over from its mouth (`give-item from {actor, slot}`); the clerk's bow and three hits on the belfry's target (`shot`, its prop `minecraft:target`, its station in the tower's opening); the cake is taken off its table when a raider of either kind stands on the stage (`counts` over the stage, `body-enters`), and the ending reads it.
- Two engine defects stop the documents. (1) `DW0879` dates a loop's count as moved by bodies but not a census (`counts`), so a gate on a census is judged against the path's writes, which a census never has: task B's latch (`requires_state` on the three goats' censuses) is refused. B is in the author's source behind one switch; on a copy of `delvec` that dates a census as it dates a loop's count, B validates and its three goats' seats are proven to reach the pen (`census binding (DW1089): 5 counted datum(s); 3 body seat(s) proven`). (2) `DW0807`: the PackTest template for a limited objective's expiry (`limit_o_<obj>_expires`) does not write the data the objective's `requires_state` reads — `dw.s_belfry_hits` for the bell, the three censuses for the goats — so the build of these documents is refused once the bell is in them. Both stand at `2da9bc544`.
- Written but not emitted, on an engine limit: the night's bunting and lanterns over the main street, a `by-effect` batch the festival's beat applies (`apply-edits`). With it the build's darkness survey after the batch passes the engine's reach budget (`DW1042`: 240350413 launch states against a ceiling of 200000000, "a build the engine cannot yet afford").

## The design record

The approved pictures of the replaced story showed it at late afternoon and at sunset; this day is played at 07:00, 10:00, noon, 18:00 and midnight. A picture approves the hour it was drawn at, so the old set cannot stand as this delve's approval and is removed with its record and its showcase cameras. The festival day's own design walkthrough has not been approved: the record is empty, which validation states as a zero and the staging gate refuses. The camera poses of the old set, with the owner's keep / drop / reframe notes, are in `design/generator/shots.json` for drawing pictures to look at.

## Placement (step 2)

- The farm district on the empty flank east of the town: a farm track off the end of lane 5 and six plots off it (wheat field, orchard, sheep fold, duck pond, cattle pen, barn), each a contact on the track. Drawn by `design/generator/farm.py`.
- The goat pen, hung off stretch 5's east face between the tavern and lane 5 (its box held to nine cells deep by the tavern's and the lane's rings), its gate on the stretch of the seam; the station `anchor/goat-pen-gate`. Drawn by `farm.py`.
- The net green west of the cliff path and the beacon point east of it, each the full length of its contact with the path. Drawn by `farm.py`.
- The lighthouse gains the station `anchor/lamp-room`, on the newel head's south-east cell; the cathedral `anchor/belfry-target` in the bell tower's west opening and `anchor/forecourt-bell` on the close; the square `anchor/cake-table` on the stage's deck.
- The engine refuses crops in a piece (`DW0730`: farmland and wheat change after the proofs judged them), so the wheat field is drawn cut, its sheaves stood in stooks of hay; it refuses a cake for the same reason, so the cake is set on its table by the opening.
- Not placed: the gap beside the guildhall. A yard hung off flight 5 is refused three ways (`DW1057` the flight's steps fill the seam's columns, `DW0844` a seam on the landing alone falls on the yard's corner, `DW0827` a deeper yard meets stretch 5's ring); the gap needs the flight or the neighbouring plots moved in the plan. Nor the grid of streets west of the main street: the slope falls two courses every stretch, so a back street needs its own flights and a re-laid west half of the plan.

## Content (step 5)

- Every objective is bound to the place it happens in (`layout-graph.json` `beats[]`), and the authored critical path is re-derived as the walk through those places in order.
- Windows: the lamp, 6000 ticks from reaching the lamp room's climb; the bell, 6000 ticks from its activation; the fireworks, 9600 ticks from the fox's first flight; the goats (held), 12000 ticks from Kettil's ask. Each is an expiry world the ladder waits out.
- Task B is a fork the plan declares (`branch-point/goats`): the goats home or astray, both leading to the festival, because the night stages three goats on the stage when they are astray.

## Languages

`world.json` declares `zh-cn`. The sidecar is written in this run from the English documents through `delvec l10n-apply` (178 of 178 rows; 197 with task B); no translation provider was configured.

## Light at night (step 8)

The night act is judged at the darkest sky the world reaches (effective 4). The build refuses (`DW0210`): 4590 of 73355 reachable cells of the island's ground outside every place stand below light 3, in some three hundred pockets under the island's tree cover (the fill's oak, birch and spruce strata), plus 39 cells in 24 places, each a cell or two under an eave or a canopy. The farm district, the goat pen, the net green and the beacon point measure no dark cell; the belfry, a floor the measured world now reaches, is lit by the ringers' four lanterns. The repair is a design choice between the woods and the night, put to the owner and open; the woods are left as they are.

## Build (step 8) — where it stands

The build of these documents refuses on the night's light (`DW0210`, above) and on the bell's window template (`DW0807`, an engine defect). Every later gate was walked on measurement copies of the same documents with the dusk and the night clocked to the latest hours judged as day, each named below by what else it changes.

- Copy with the bell's window dropped (the bell otherwise as written): builds; the critical-path bot stops at step 3, the bell, because the exported critical path carries no step that shoots the belfry target (the shot trigger the bell's `requires_state` reads), so the three hits never land — an engine defect, measured at `0f0f9db12` and again at `2da9bc544`.
- Copy with the bell held back and the beach landing at once, at `2da9bc544` (build exit 0, 596 s, 4.0 GB peak):
  - PackTest: 104 tests, 91 passed, 13 failed, all in the engine's templates: 12 read a wave scaled with the party (`count {base, per_player}`) against `base` while the batch's server holds more players (`#dock_landing dw.wave` 6 for 3), and 1 reads the window score of a limit opened `from` an objective (`limit_o_fetch_the_fireworks_expires`: `#lim_open_fetch_the_fireworks` has no score at tick 9601).
  - The critical-path bot: passed, 18 steps, 6 scripted deaths survived, die-retry passed. The landing is moved to the dusk's first beat on this copy because the bot musters a `kill` step's wave when the step opens, and the documents land the beach wave thirty seconds after the lighthouse's warning (the script's early warning): the muster read no body (an engine-side defect of the harness).
  - The written world: 5037034 cells compared; 8 differ in no class the server's physics explains (`DW0955`): four `dirt_path` the server turns to `dirt` under the wheat field's stooks, and four sugar canes by the duck pond aged by a random tick. The engine's model is wrong at those cells.
  - Branch runs: BRANCHLINE
  - The staging gate: refused on 4 of 160 rows — `drill3-01`/`drill3-03` (no design record: the reference sheet could not be drawn, the image provider's prepaid credit is spent) and `isl-33`/`isl-53` (the fireworks are fetched from a chest the compiler stamps, not from a container the castle's storeroom holds).
- The earlier run of the ending, on the same kind of copy, found the party restored twenty blocks over the main street after the ending's second shot; fixed in these documents (one cutscene of three shots).
