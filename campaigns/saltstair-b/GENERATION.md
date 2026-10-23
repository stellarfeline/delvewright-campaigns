# Saltstair, cut B — generation record

## What the brief pinned, and what was invented

Pinned: the whole of `campaigns/hillside/DESIGN.md` §2–§6, built as cut B — two large boxes, `node/upper-town` (x 54..94 × z 96..149, floor 76, open 20) and `node/lower-town` (x 54..94 × z 151..200, floor 64, open 14), each drawn whole by one program, buildings not boxes; the junction an open `walk` contact over the whole front, as §5.2 now states it; the campaign id; `demo_level: true`; the walk from the square to the quay; light placed with each place.

Ruled at the design gate, the same for both cuts: `time: noon`; `demo_level: true` kept, with no `design.json`, and the staging gate's `DEMO-UNQUEUED` refusal accepted; English only; `views[]` empty, the six §6 cameras at their exact float coordinates, drawn at `day` (as built: the poses are in `design/judging-cameras.json`, not `design/cameras.json`, and the frames show the world's `noon` — see *Tool issues*); step 9 entered with `DW0210` as the only red, each house lit while it is detailed and no temporary lighting declaration.

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

- **The drop off the front, as built.** The two sides meet at one walk level, 76, over **x 57..58 and x 71..80 — the 12 columns the battery measures crossable**; the merchant's house's south wall stands on z 149 across x 59..70, so the merchant's side does not cross. Over x 81..93 the lower town's lane stands at 76 too, and the plane z 150 between the two edges is a one-cell trench in the fixed ground, falling from walk 74 to walk 69; at x 54..56 the plane stands at 73..74 between the same two edges. A body that steps off either edge there falls up to **7 blocks (x 91..93), `ceil(7 − 3)` = 4 of 20 health**, inside the unarmoured survivable 22. **No check proves it survivable**: `DW0831` judges only `drop` seams, by the floor difference, and nothing measures a fall off a `walk` contact's columns. `DW0921` does prove the trench is not a trap: 0 of 31 973 reachable cells cannot be left.

## Order change

The junction is proven at the **first build after `node/lower-town`'s program draws its ground up to 76 at z 151**, not before the rest is built: a stand-in build of the two boxes refuses it (below), because the lower town's stand-in is massed at its floor, 64, twelve under the front.

## Refusals, in order

| # | Run | Code | What it said | Repair |
|---|---|---|---|---|
| 1 | stand-in `build` of the two-box junction probe (scratch) | `DW0877` | 0 of the front's 41 columns (x 54..94, y 76..77, z 150) crossable | none in the plan: the junction is proven once the lower town's piece draws its ground to the front (*Order change*) |
| 2 | same run | `DW0837` | no body reaches `node/lower-town` (2050 standable cells, none reachable) | the same: the lower town is reached over the front its piece draws |
| 3 | `validate`, placement written, story stubbed (step 2) | `DW0150` | the planned quest has no stage-5 expansion | none: the expected state until `quests.json` (step 5) |
| 4 | same run | `DW0818` | the beat names `quest/to-the-quay`, which no quest document declares | the same |
| 5 | `validate`, step 3 | `DW0150` | the same | the same |
| 6 | same run | `DW0818` | the same | the same |
| 7 | `validate`, the gate's rulings applied | `DW0150` | the same | cleared at step 5 by `quests.json` |
| 8 | same run | `DW0818` | the same | cleared at step 5 |
| 9 | `build` at step 8, stand-ins | `DW0837` | no body reaches `node/lower-town` | the junction's order change — cleared by the lower town's piece |
| 10 | same run | `DW0877` | 0 of the front's 41 columns crossable | the same; the battery stops here, so `DW0210` is not yet measured, and step 8b's cameras wait for the first build that exits 0 |
| 11–21 | inside `detail node/upper-town` attempt 1 (the author's runs, consecutive repeats collapsed) | `DW0730`, `DW0837`, `DW0990`, `DW0877`, `DW0837`, `DW0990`, `DW0877`, `DW0837`, `DW0877`, `DW0837`, `DW0877` | a lava cauldron off the block allowlist; an eave over the plot edge (twice); the junction (each run) | magma-block forge; eaves dropped at the plot edge; the junction by the order change |
| 22 | my confirming `detail node/upper-town` | `DW0837` | no body reaches `node/lower-town` | the order change |
| 23 | same run | `DW0877` | 0 of 41 crossable | the same |
| 24–26 | inside `detail node/lower-town` attempt 2 | `DW0838`, `DW0344`, `DW0885` | lower ground in front of the contact was an unallocated crossing; the stand-in's sea level, then the quay's water row; the upper town's open sides | the lane level at 76 across the front; the quay's ring row filled to walk 63 and no water painted; `DW0885` handed on |
| 27 | my confirming `detail node/lower-town` | `DW0885` | the upper town's piece: its north side (13 cells, first [63, 83, 95]) stands in open air, `shown_faces: ["up"]` | a fresh author for the upper town, handed the refusal |
| 28 | same run | `DW0885` | its east side (20 cells, first [95, 69, 147]) | the same |
| 29 | same run | `DW0885` | its west side (16 cells, first [53, 72, 150]) | the same |
| 30–31 | inside `detail node/upper-town` attempt 2 | `DW0885` (as handed), `DW0921` | the open sides; then a pit in the lower town | `shown_faces` east, north, up, west; `DW0921` handed on |
| 32 | my confirming `detail node/upper-town` | `DW0921` | a body falls 2 from [77, 70, 187] into [77, 68, 186], east of flight 5, and cannot get out | a fresh author for the lower town, handed the refusal |
| 33 | inside `detail node/lower-town` attempt 3 | `DW0921` (as handed) | the same | kerb posts and bollards count as street when the hillside is fenced |
| 34 | `place-camera` on a scratch copy, step 8b | `DW0721` | `design.json`: no such file | none: the record cannot be written without `design.json` (*Tool issues*) |
| 35 | `build` of a scratch copy carrying a hand-placed `design/cameras.json` | `DW0721` | camera `from-the-sea` answers `view/from-the-sea`, which is not a row of `design.json` | `design/cameras.json` not committed; the poses go to `design/judging-cameras.json` |

Refusals per code over the run: `DW0837` 7, `DW0877` 7, `DW0150` 3, `DW0818` 3, `DW0885` 5, `DW0921` 3, `DW0990` 2, `DW0721` 2, `DW0730` 1, `DW0838` 1, `DW0344` 1 — 35 in all. Codes inside an author's attempt are those its runs printed, consecutive repeats collapsed, and include at the head of a repair the refusal its handout quoted.

## Detail

Handouts are regenerable files under `campaigns/saltstair-b/.out/handouts/` (gitignored). Refusals an attempt repaired are the codes it was handed; the codes the author met and repaired inside its own attempt are listed beside them.

| Place | Attempt | Handout | Agent tokens | Duration | Refusal repaired | Repaired inside the attempt | `delvec detail` exit confirmed |
|---|---|---|---|---|---|---|---|
| `node/upper-town` | 1 | `upper-town/handout-1.md` | 266 554 | 20 min 23 s | none (first authoring) | `DW0990` (an eave over the plot edge), `DW0730` (a lava cauldron off the allowlist, now a magma-block forge), an empty `no_body` region over the ring | 3 — the piece written, the whole refused only at the junction (`DW0837`, `DW0877`, rows 22–23) |
| `node/lower-town` | 1 | `lower-town/handout-1.md` | 58 439 | 30 s | none (first authoring) | — | not run: the author stopped before writing, reading this repository's `CLAUDE.md` ("without the constitution … ask before improvising") as binding on authoring, since `CLAUDE.local.md` is absent on this machine; no program written |
| `node/lower-town` | 2 | `lower-town/handout-1.md` (relaunched; the prompt carried one added line naming the engine `CLAUDE.md` and stating `CLAUDE.local.md` absent and not binding on a place program) | 278 751 | 23 min 30 s | none (first authoring) | `DW0838` (lower ground in front of the contact, outside its y 76..77 span), `DW0344` (the stand-in's sea level, then the quay's water row) | 3 — the piece written; the whole's junction now holds (12 crossable columns, no `DW0877`/`DW0837`), and refuses `DW0885` ×3 on the upper town's piece (rows 27–29) |
| `node/upper-town` | 2 | `upper-town/handout-2.md` | 120 478 | 3 min 23 s | `DW0885` ×3 | — | 3 — `DW0885` cleared by declaring the north, east and west sides shown (`shown_faces` east, north, up, west; no block changed: the exposed cells are the whole's fixed ring turf one course over the commons, which the piece may not write — the declaration rests on that turf, not on anything the piece built); the whole then refuses `DW0921` in the lower town (row 32) |
| `node/lower-town` | 3 | `lower-town/handout-2.md` | 76 591 | 1 min 22 s | `DW0921` | — | 0 — kerb posts and bollards now count as street when the hillside is fenced, so the cell beside the shore street's east post is walled; the whole builds |

Departures the upper town's author recorded: doors are open 1 x 2 doorways under a timber lintel (the engine's walk treats a door block as solid, so no passable door exists); the weaver's cloth is on the ground floor (clearance 4 holds one floor); the chapel's and inn's outer walls stand on the frame's first layer and eaves are omitted where the frame or plot edge forbids them; the smithy's and merchant's roofs end in a flat top four wide at the stated course counts.

Departures the lower town's author recorded: **the front lane is level at walk 76 across the whole width** (x 54..94 at z 151), not only over x 59..78 — lower ground in front of the contact was refused as an unallocated crossing (`DW0838`), because the contact's span is y 76..77; so where the fixed ground on the plane z 150 is under 76 (x 54..58, x 79..94) the front is a one-cell gap between two walk-76 edges rather than the drop onto lower ground that §5.2 describes. Roofs follow ceil((W - 1) / 2) under the frame's top course, which brings the rope walk's walls down to 2 courses (clearance 4 stated); the quay's ring row at the water is filled to walk 63 (`DW0344`) and no water is painted in the piece; doors are open 1 x 2 doorways in spruce frames.

## The detailed build

`delvec detail --all` exit 0; `validate` 0; `analyze` 0; `build` 0 into `validation/delve-output-saltstair-b`. Blockout: 2 places, both detailed, **0 massed by the derivation (0 stand-ins)**; 1621 fixed ring ground cells laid. Battery: 1 contact proven, **12 crossable columns** of the front's 41, 2 places reached, 0 cracks. `DW0921`: 31 973 reachable cells, 0 a body cannot leave. `DW1002`: 145 attached blocks, all held. `DW0210` raised nothing (world `noon`, sky light 15; every house lit by its own piece). Pacing (`DW0822`): 57 blocks of route measured over the built map, about 1 minute against `target_minutes` 10 — the design's street length; nothing added. Advisory `DW0781`: zero abutting piece faces examined.

## The judging frames (step 8b)

The six §6 cameras, at their exact eye coordinates (yaw and pitch derived from each `look_at`, fov 70), are recorded in `design/judging-cameras.json` and drawn by `delvec frames --campaign campaigns/saltstair-b --camera x,y,z,yaw,pitch,70` (lumenwright 0.3.0, CPU backend, quick mode, 1024 × 1024, the load world at `noon`) to `review/frames/<camera>.png`, each with its manifest. The storybook image is the review frame `pov/leg0/wp1`, from the square down the first flight.

## The machine ladder (step 10)

- PackTest (`validation/packtest-run.sh --project dw-saltstair-b-r1 --output ./delve-output-saltstair-b`): **exit 0, 17 of 17 required tests passed**.
- The bot (`validation/bot-run.sh`, same project and tree): **exit 0; `critical-path` passed** — class chosen on the square, then down the main street to `anchor/quay`. `die-retry`, `death-loop` and `crush-death` not run: the build declares no combat, no lethal volume and no crush gate. Run report: `$DELVEWRIGHT_ENGINE/validation/run-out/dw-saltstair-b-r1/run-report.json`, build `manifest_sha256` `2b44c33f9add25174c2705e11d8e7e6a7e2ecaef5695068a315b1ef73eb61eba`.
- Written world (`world-save.sh`, `delvec written-world`, `check-written-world.py`): **exit 0** — 70 684 non-air cells compared, the server's at every one outside the named classes (147 re-derived).
- No `branch_points`, so no branch runs and no chronicle (step 11).

## The five numbers (§6)

Read from the server-saved world (`delve-output-saltstair-b/world`) with the engine's `tools/lib/anvil.py` at the pinned engine, and cross-read from the engine-written world (`delvec written-world`) by the same rule — the two agree on every figure. A cell is standable when the block under it holds a body (not air, fluid, a fence, a wall, a pane, bars or a lantern) and it and the cell over it are passable.

| Number | B |
|---|---|
| Distinct floor levels on the centre line (x 73, 74; z 96..200) | **21** — every walk plane 64..84: the six datums and the fifteen tread levels of the five flights (207 of 210 columns carry a standable cell) |
| Ring cells where a box's ground and the outside terrain differ | **372** plot-edge columns examined (the battery's own count; **0 cracks**, `DW0990`); **110** of them faced — inside ground more than one block from the ring's terrain (upper town 59 of 190, lower town 51 of 182; the largest difference 10) |
| Refusals per code | 35: `DW0837` 7, `DW0877` 7, `DW0885` 5, `DW0150` 3, `DW0818` 3, `DW0921` 3, `DW0990` 2, `DW0721` 2, `DW0730` 1, `DW0838` 1, `DW0344` 1 (*Refusals, in order*) |
| Author tokens and time | the five place authors: **800 813 tokens, 49 min 08 s** (table *Detail*); the orchestrating session's own token count is in no record this run can read; wall clock from the pin repair at Init to the staging gate about 1 h 16 min, both hand-overs included |
| Build and bot status | `build` 0; PackTest 0 (17/17); bot critical path passed; staging gate **REFUSED on `DEMO-UNQUEUED` alone** (below) |

## The staging gate (step 13)

`tools/creator/staging-gate.py --campaign campaigns/saltstair-b --build … --run-report … --written-world .out/written-world.json`: **REFUSED — exit 1, one red row, `DEMO-UNQUEUED`** (the demo declaration with no queue row naming `campaigns/saltstair-b`), accepted at the design gate. Every other row is judged: **22 BOUND, 27 DECLARED-UNCOVERABLE, 98 INAPPLICABLE; 0 UNBOUND, 0 MISSING-CHECK, 0 NO-SOURCE, 0 NO-GENERAL-FORM**. The full report is `review/staging-gate.md`.

## Tool issues

1. **Init I1's skill-root lookup** refused on a second install of the plugin scoped to a different project (`2 installed delvewright plugin(s)`); resolved by removing the stale install.
2. **`~/.delvewright/` is one toolchain shared by every session on the machine**: a concurrent session rewrote `env.sh`'s `DELVEWRIGHT_PREFABS` to its own clone, and `validation/delve-output` is one tree. This run set the library per command and built to its own tree.
3. **`delvec validate` with no `--prefabs`** stopped with `internal error: cannot read prefabs dir campaigns/prefabs` (exit 10, no DW code) in a directory without `campaigns/prefabs`.
4. **A stand-in cannot meet a contact between places on different floors**: the derivation masses the lower box at its floor, so the junction is unprovable until the lower piece exists (`DW0877`'s own text: "the repair is in the compiler").
5. **The step-9 handout quotes only the campaign's documents** (node `note`, seam `form`, box, facts); a design kept in `DESIGN.md` reaches the author only once it is copied into the notes, which this run did.
6. **A place author stopped on this repository's `CLAUDE.md` constitution rule**, the absent `CLAUDE.local.md`; the relaunch carried one added prompt line, a departure from the page's "nothing is added".
7. **A camera record needs `design.json`**: `place-camera` and `build` both refuse (`DW0721`) a `design/cameras.json` whose rows answer no approved image, so a demo level cannot carry showcase cameras.
8. **`delvec frames --campaign` and `delvec panorama` draw only the load model's chunks**: the island, the mainland and the open sea that the server's world holds (checked in the save: the hills at surface 84 and 76, the sea at 62) are absent from every frame, and a camera standing past them sees the model's cut face. `frames --campaign` takes no sky, so the `day` ruling could not be applied: the frames show the world's `noon`.
9. **No passable door** in the contract's walk: every door is an open doorway (both authors).
10. The `check-storybook-version.py` sweep over `campaigns/` fails on other campaigns' missing storybooks; run over this campaign alone it passes.

## Conformance review, against `campaigns/hillside/DESIGN.md`

Drift nobody asked for, reported rather than kept silently:

- **§5.2 (restated) — the front.** Built: the two sides meet at walk 76 over 12 columns (x 57..58, x 71..80), not over x 59..78: the merchant's south wall closes x 59..70. Beyond them the lower town's lane is at 76 across the whole width and the drop is into a one-cell trench in the plane's fixed ground (to walk 69), not onto lower ground. Forced by `DW0838` (the contact's span is y 76..77). A body does **not** cross "anywhere along" the front.
- **§3/§4.2 — doors** are open 1 × 2 doorways, not door blocks; **eaves** are dropped where a frame or plot edge forbids them (the chapel's and inn's outer walls, the edge houses); the **smithy's and merchant's roofs** end in a flat top; the **weaver's cloth** is on the ground floor; the **rope walk's walls** are two courses under its roof, not its clearance of 4.
- **§2 — the island and the hour**: the island is in the world; the hour is `noon` by ruling, not late afternoon.
- **§6 — the cameras** are drawn from `design/judging-cameras.json`, not `design/cameras.json`, under `noon`, not `day`; `views[]` is empty by ruling.
