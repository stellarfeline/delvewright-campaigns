# Festival Day in Kelderby — generation record

## What the brief pinned, and what was invented

- Pinned: the owner's festival-day script (three acts, five soft-fail tasks A–E, the dusk fight, the night composed from six flags, the map it needs) and her notes on the town's pictures. The script is the design of record; `DESIGN.md` transcribes it and marks every line it authors.
- Invented: the order the clock jumps in, each task's window, which places are the fox's four hiding places and its den, the cast's lines, the classes, the farm district's layout.
- The script review (step 5b) does not apply: the story is the owner's, not the run's.

## Engine

- `delvec` 1.16.0, built from source in release profile from `stellarfeline/delvewright` `feature/festival-day` at `d54e27128f52f12b3657390a2f39dae8c6cd9255` (cargo exit 0, 92 s, 4.8 GB peak; the build before it at `735fdeb89565f73f3790c90695a55467fc2474ac`, 248 s, 3.3 GB peak); `dsl` 0.75.0. Earlier steps were authored at `eea5c7d99` (spec-0133), `aa5484754`, `b4f61cd47`, `0f0f9db12`, `2da9bc544`, `db82a1115` and `f2b19478`. Dev mode; the skill page read is the revision's own.
- Every surface the script needs is on this engine and every task is emitted: the dusk waves scale with the party; the castle's crossbows and starred rockets at dusk; the spyglass that spots the fox (`use-item`); the key taken from the fox's mouth (`use-actor`, `give-item from`); three hits on the belfry target (`shot`); the cake taken by a raider on the stage (`counts`, `body-enters`); the goats counted into their pen (`counts` over the pen, judged by its census, `DW0879`); the boats rowed to the crates (`vehicles`, `ride`); the night's bunting and lamps applied by the festival's beat (`apply-edits`) and the woods' lanterns set at build; the crowd's moves under the show (spec-0136: `face`, `hold`, `hop`, `pose`, `particle` and `play-sound` at bodies, each with `repeat` and `stagger_ticks`).
- Two engine defects stand. (1) The build stops at the critical path's leg to the belfry shot (`DW0311`, from [124, 82, 268] to [149, 108, 238], floor [150, 106, 240]): with the boats' rides on the critical path no stance is fixed for the shot, and the leg is routed to the target in the tower's opening. The same documents with task A held (`WITH_CARGO=0` in the author's source, every other part as written) pass that leg. Reported to the engine. (2) The food in the three defence lines' supply chests: a starter mark on a container's own cell lands in no element of the piece's contract (`contract-anchors`), so no drawn chest can carry the anchor a `loot` fill names. The chests stand drawn; the fills are in the author's source behind one switch.

## The design record

The approved pictures of the replaced story showed it at late afternoon and at sunset; this day is played at 07:00, 10:00, noon, 18:00 and midnight. A picture approves the hour it was drawn at, so the old set cannot stand as this delve's approval and is removed with its record and its showcase cameras. The festival day's own design walkthrough has not been approved: the record is empty, which validation states as a zero and the staging gate refuses. The camera poses of the old set, with the owner's keep / drop / reframe notes, are in `design/generator/shots.json` for drawing pictures to look at.

## Placement (step 2)

- The farm district on the empty flank east of the town: a farm track off the end of lane 5 and six plots off it (wheat field, orchard, sheep fold, duck pond, cattle pen, barn), each a contact on the track. Drawn by `design/generator/farm.py`.
- The goat pen, hung off stretch 5's east face between the tavern and lane 5 (its box held to nine cells deep by the tavern's and the lane's rings), its gate on the stretch of the seam; the station `anchor/goat-pen-gate`. Drawn by `farm.py`.
- The net green west of the cliff path and the beacon point east of it, each the full length of its contact with the path. Drawn by `farm.py`.
- The lighthouse gains the station `anchor/lamp-room`, on the newel head's south-east cell; the cathedral `anchor/belfry-target` in the bell tower's west opening and `anchor/forecourt-bell` on the close; the square `anchor/cake-table` on the stage's deck.
- The engine refuses crops in a piece (`DW0730`: farmland and wheat change after the proofs judged them), so the wheat field is drawn cut, its sheaves stood in stooks of hay; it refuses a cake for the same reason, so the cake is set on its table by the opening.
- Not placed: the gap beside the guildhall. A yard hung off flight 5 is refused three ways (`DW1057` the flight's steps fill the seam's columns, `DW0844` a seam on the landing alone falls on the yard's corner, `DW0827` a deeper yard meets stretch 5's ring); the gap needs the flight or the neighbouring plots moved in the plan. Nor the grid of streets west of the main street: the slope falls two courses every stretch, so a back street needs its own flights and a re-laid west half of the plan.

- The bay below the quay (task A): clear water over sand, shoals breaking the surface, a bar across its mouth with a channel at the east end, the six crates' points (two past the bar) and the two boats' slips in open water; its `part/shoals` declares the 150 cells the drawing builds (`DW1074`), and the quay answers its seam (`DW0844`). Drawn by `farm.py`.
- The owner's second map note (the ground round the town still read empty from the sea), each a place a player walks into, drawn by `farm.py`: on the west terraces the west track off the quay's west end, the archery butts with the bow stall, the allotments, a croft and the bonfire green on the shore, and above them the terrace track off the back of the fishmonger's yard with the terrace orchard, a cottage, the sheep terrace and the kitchen garden; on the east meadow behind the beach the meadow track off the cliff path, the festival fair field (a maypole, a ring of striped stalls, a tent, then trestle tables, a bonfire and a dance floor toward the beach), the bee meadow and the dune cottage; in the town the games yard above the harbour house and the lantern-makers' yard between the houses, both off lane 8, and the cathedral garden on the terrace below its south side. The quay, lane 8, the cliff path, the fishmonger's and the cathedral are re-detailed to answer the new seams.
- A supply chest with a hay bale for cover at each of the three defence lines: on the quay beside the salt-fish barrels, on the street side of the goat pen's fence, at the stage's north foot.

## Content (step 5)

- Every objective is bound to the place it happens in (`layout-graph.json` `beats[]`), and the authored critical path is re-derived as the walk through those places in order.
- Windows: the lamp, 6000 ticks from reaching the lamp room's climb; the bell, 6000 ticks from its activation; the fireworks, 9600 ticks from the fox's first flight; the goats, 12000 ticks from Kettil's ask; each crate, 12000 ticks from Sverre's ask. Each is an expiry world the ladder waits out.
- Task B is a fork the plan declares (`branch-point/goats`): the goats home or astray, both leading to the festival, because the night stages three goats on the stage when they are astray.

## Languages

`world.json` declares `zh-cn`. The sidecar is written in this run from the English documents through `delvec l10n-apply` (249 of 249 rows); no translation provider was configured.

## Light at night (step 8)

The night act is judged at the darkest sky the world reaches (effective 4), and it measures lit: no reachable cell of the island below light 3 after the woods' batch and after the night's. Placed while each place was designed (the owner's ruling for the woods; light is placed, never derived): festival lanterns on the ground under the woods' crowns, six cells apart over the whole island, every place and two cells round it kept clear, and three set by hand in hollows the spacing misses; lanterns hung on chains under the square's two trees; a torch in the inn's passage and a lamp post under its yard oak; lanterns under the castle's two south bartizans and one hung in the great hall's east embrasure; a lamp in the lighthouse yard; a lamp at each turning end of the castle road's legs that a seam keeps clear, and a lantern in a niche at the foot of each climbing leg's embankment, where the turn below the next leg was dark.

## Build (step 8) — where it stands

The build of these documents stops at the belfry shot's leg (`DW0311`, the engine defect above), after the night's light, the vehicles' seats and every earlier gate pass; build wall time 352 s and 3.6 GB peak at `d54e27128` on this Mac. The ladder (step 10) waits on the engine.
