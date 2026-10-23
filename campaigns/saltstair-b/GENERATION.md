# Saltstair, cut B — generation record

## What the brief pinned, and what was invented

Pinned: the whole of `campaigns/hillside/DESIGN.md` §2–§6, built as cut B — two large boxes, `node/upper-town` (x 54..94 × z 96..149, floor 76, open 20) and `node/lower-town` (x 54..94 × z 151..200, floor 64, open 14), each drawn whole by one program, buildings not boxes; the junction an open `walk` contact over the whole front, as §5.2 now states it; the campaign id; `demo_level: true`; the walk from the square to the quay; light placed with each place.

Ruled at the design gate, the same for both cuts: `time: noon`; `demo_level: true` kept, with no `design.json`, and the staging gate's `DEMO-UNQUEUED` refusal accepted; English only; `views[]` empty, the six §6 cameras at their exact float coordinates in `design/cameras.json`, drawn at `day`; step 9 entered with `DW0210` as the only red, each house lit while it is detailed and no temporary lighting declaration.

Invented: the ground music (silent), the world seed, and the title and premise lines.

## Posture note

Three axes off the default, for the few lines this walk has: **thematic explicitness** — no line states what the town means, the street and the sea say it; **resolution** — the delve ends on arrival at the quay, with no epilogue and no understanding reached; **address** — the journal line speaks to the player as the one walking, in the imperative, not about a protagonist.

## Toolchain

- Plugin `delvewright` 1.14.0; engine release `delvec--v1.14.0` (`e51f8bbef8c3a3b58caea451b5f9898b15b00509`); `delvec 1.14.0, dsl 0.56.0, mc 1.21.11`, the release archive (`delvec-v1.14.0-x86_64-unknown-linux-gnu.tar.gz`, sha256 `8dad85c5fc80f1cc8cc0dba4e2cee6523e73a3aee36eecfcd8bd2af996130db3`).
- Library: this content clone's `prefabs/`, at the revision this branch stands on; the engine's `[content].sha` names `3d8b343dbcb9f44c267da77fa2a31f1c47e8957e`, a different revision, named and not corrected.
- Every build writes to `$DELVEWRIGHT_ENGINE/validation/delve-output-saltstair-b` and every ladder run is pointed at it with `--output`: the engine's default tree is shared with another build on the same toolchain, and a ladder that boots another campaign's tree judges the wrong world.

## Decisions

- **The hour.** The design states "late afternoon", which has **no DSL spelling**: the engine's clock is six keywords (`day`, `noon`, `dusk`, `night`, `midnight`, `dawn`) and six positions of a body's arc, none of them a late afternoon. `noon` is the ruling, the same in both cuts so the comparison stays fair.
- **The heightmap** is a byte copy (`sha256 455d5a93e32cc8c9e009fe2e3a27683edba289d8d71a83463c63078ef66944fb`) of the design's, because a site plan reads its heightmap from inside the campaign.

## Unproven points

- **The drop off the front.** Along the contact at z 150 the two sides meet at walk 76 over x 59..78 only; at x 54..58 and x 79..94 the upper town's edge stands 1 to 7 blocks above the fixed ground (walk 73..75 west, 75 → 69 east). The deepest fall is 7 blocks, `ceil(7 − 3)` = 4 of 20 health, inside the unarmoured survivable 22 of the metrics table. **No check proves it survivable**: `DW0831` judges only `drop` seams, by the floor difference, and nothing measures a fall off a `walk` contact's columns.

## Order change

The junction is proven at the **first build after `node/lower-town`'s program draws its ground up to 76 at z 151**, not before the rest is built: a stand-in build of the two boxes refuses it (below), because the lower town's stand-in is massed at its floor, 64, twelve under the front.

## Refusals, in order

| # | Run | Code | What it said | Repair |
|---|---|---|---|---|
| 1 | stand-in `build` of the two-box junction probe | `DW0877` | 0 of the front's 41 columns (x 54..94, y 76..77, z 150) crossable | none in the plan: the junction is proven once the lower town's piece draws its ground to the front (*Order change*) |
| 2 | same run | `DW0837` | no body reaches `node/lower-town` (2050 standable cells, none reachable) | the same: the lower town is reached over the front its piece draws |
| 3 | `validate`, placement written, story stubbed | `DW0150` | the planned quest has no stage-5 expansion | none at step 2: the expected state until `quests.json` is written at step 5 |
| 4 | same run | `DW0818` | the beat names `quest/to-the-quay`, which no quest document declares | the same: cleared by step 5 |
| 5 | `build` at step 8, stand-ins | `DW0837` | no body reaches `node/lower-town` | none at step 8: the junction's order change — cleared by the lower town's piece |
| 6 | same run | `DW0877` | 0 of the front's 41 columns crossable | the same; the battery stops here, so `DW0210` is not yet measured, and step 8b's cameras wait for the first build that exits 0 |
| 7 | `detail node/upper-town`, attempt 1 (the whole's battery) | `DW0837` | no body reaches `node/lower-town` | none in the upper town: its piece is written and every gate of its own green; the junction's order change, cleared by the lower town's piece |
| 8 | same run | `DW0877` | 0 of the front's 41 columns crossable | the same |

## Detail

Handouts are regenerable files under `campaigns/saltstair-b/.out/handouts/` (gitignored). Refusals an attempt repaired are the codes it was handed; the codes the author met and repaired inside its own attempt are listed beside them.

| Place | Attempt | Handout | Agent tokens | Duration | Refusal repaired | Repaired inside the attempt | `delvec detail` exit confirmed |
|---|---|---|---|---|---|---|---|
| `node/upper-town` | 1 | `upper-town/handout-1.md` | 266 554 | 20 min 23 s | none (first authoring) | `DW0990` (an eave over the plot edge), `DW0730` (a lava cauldron off the allowlist, now a magma-block forge), an empty `no_body` region over the ring | 3 — the piece written, the whole refused only at the junction (`DW0837`, `DW0877`, rows 7–8) |

Departures the upper town's author recorded: doors are open 1 x 2 doorways under a timber lintel (the engine's walk treats a door block as solid, so no passable door exists); the weaver's cloth is on the ground floor (clearance 4 holds one floor); the chapel's and inn's outer walls stand on the frame's first layer and eaves are omitted where the frame or plot edge forbids them; the smithy's and merchant's roofs end in a flat top four wide at the stated course counts.
