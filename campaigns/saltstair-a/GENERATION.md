# Saltstair, variant A — generation record

## Toolchain

- `/new-delve` plugin 1.14.0; engine release `delvec--v1.14.0` (`e51f8bbef8c3a3b58caea451b5f9898b15b00509`); `delvec 1.14.0, dsl 0.56.0, mc 1.21.11`, the release archive `delvec-v1.14.0-x86_64-unknown-linux-gnu.tar.gz` (sha256 `8dad85c5fc80f1cc8cc0dba4e2cee6523e73a3aee36eecfcd8bd2af996130db3`).
- Prefab library: this clone's `prefabs/`, at the revision that carries this directory; the engine's `[content].sha` is `3d8b343dbcb9f44c267da77fa2a31f1c47e8957e`, an ancestor of it.
- The engine constitution's operating half, `CLAUDE.local.md`, was not available to this run; the run decides nothing about dispatch, review, merge or staging.

## What the brief pinned, and what this campaign invented

Pinned, verbatim from `campaigns/hillside/DESIGN.md` §2–§6: the region, the heightmap and its fill, the horizon and boundary, the nineteen places and their extents, floors, headroom and roofs, the eighteen seams, the materials, the light rule, the six cameras, the walk and the five numbers. Pinned by the run's brief: cut A, the id `saltstair-a`, `demo_level: true`, one program per box, the six cameras drawn at day.

Invented: the seed (`20261022`), the title line, the horizon's music (silence — the design states none), the quest's wording.

## Posture note

Three axes off the default, for a ten-minute walk with one objective: the text addresses the player directly ("You stand on the square…"); it states no point about the town — the street is the whole of what is said; and it ends on the fact of arrival, with no reflection after it.

## Rulings at the design gate

The design was approved as written (`campaigns/hillside/DESIGN.md`), on the reference image `view1-from-the-sea` and the design's tables; no concept set was drawn. Rulings, the same for both variants:

- `world.time` is `noon`. The design's "late afternoon" has no DSL spelling: the sky vocabulary has no sun position between `high` and `setting` (the disc on the western horizon). The six §6 frames are drawn at `day`.
- `demo_level: true` stays; the staging gate's `DEMO-UNQUEUED` refusal (no row of the pinned engine's demo queue names `campaigns/saltstair-a`) is accepted, and the gate's full report is recorded with every other row judged. No `design.json`.
- English only.
- `site-plan.json` `views[]` stays empty: it takes whole numbers and §6's cameras stand at half blocks. The exact camera coordinates live in `judging/cameras.json` — first written to `design/cameras.json`, moved after refusal 8: every row there must answer a `design.json` row, which the campaign does not carry by ruling, and `detail` refuses the record (`DW0721`) on every run. Moved by the owner's delegation to the run's judgement. The frames are drawn with `delvec frames --campaign --camera` at the rows' exact poses, which draws the world's sky (`noon`); `day` frames are drawn from a scratch copy that differs only in `world.time: day`, and are labelled so.
- The step-8 build goes on to step 9 with `DW0210` as its only red (the stand-in houses are dark); each house is lit as it is detailed. No `lighting` declaration, temporary or otherwise.

## Findings

- **Each gate masked the next.** The build stops at its first refusal, so the gates surfaced one layer at a time — `DW0210` (the ruled darkness) hid the battery, the battery hid the exposure gate (`DW0885`), and the exposure gate hid the leave-proof (`DW0921`).
- **The ruled-for `DW0210` masked the blockout battery for eighteen places.** The build stops at the first refusal and `DW0210` comes before the battery, so while any stand-in house was dark no `detail` run measured built rises or the brief's identities. Flight 4 was laid with its foot one course high (three risers, rise 3) at its first authoring and passed every gate of its own; the battery first ran when the warehouse lit the last dark cells, and refused it (refusals 11–13).
- **DEPARTURE — an open street front cannot be built under cut A as written.** §3 makes the smithy "open-fronted toward the street" (and the rope walk "open along its street side"); §5.1 gives each exactly one `door` seam. Every open cell of a house wall that is not an allocated seam is an undeclared way out, refused by the piece's closure and coverage gates, so the open front is not authorable without changing the plan (a `contact` seam along the street face instead of a `door`), which the brief forbids. The smithy's author built the closest authorable thing: a three-wide forge window filled with iron bars over a counter, beside the door. The rope walk's author met the same wall and gave the street side a run of windows; its door lantern hangs just inside, because the door's outer cells are the lower street's (whose own kerb-post lantern stands opposite the door).
- **The weaver's "cloth on the upper floor" is a closed loft.** The plan gives the house clearance 4 and a 5-course roof; a second storey a body reaches would need a climb into the roof zone, above the handed play space. The cloth is there, as wool on the loft floor under the roof; nobody can walk up to it.
- **The retaining walls between terraces stand only where a flight's frame reaches.** Under cut A a street's frame begins at its paving course, so the four-course drop at a terrace's downhill end is below it; the flight's frame (floor the lower terrace) is the one place that can face it, six wide, and the drop beside the street, outside every box, is the commons hillside at the heightmap's half-block grade. §3's "every terrace stands above the next behind a retaining wall the place draws" is therefore met six wide at each flight and not across the town — a property of the cut, reported by the upper street's author.
- **A `stair` contract edge to `exterior` cannot carry a rise** ("no resolved box on the far side"), reported by flight 3's author: a flight whose whole climb is its seam's rise is two spaces joined by an interior `stair` edge, with a rise-0 edge at the seam. Authorable; recorded as the engine's shape, not a gap that blocked anything. Flights 3 and 5's authors add that the contract's `rise` takes only a literal integer, so each flight's generator copies it from the allocation's handed seam rise rather than binding `handed/seam/<edge>/rise`.
- **Detail authors stepped outside their handout**, each recorded on its row of the Detail table: several ran a read-only `git status`, and the upper street's author read the start of `programs/flight-1.json` before writing, stopped, and reports building nothing from it. No attempt was discarded for it: every piece passes its own gates, and every confirming run moved no byte.
- **Three generator scripts named `delvec` by an absolute home path** (flight 2, flight 5, the upper street); the orchestrating session rewrote that one line to the same location through `~`, which changes no emitted byte (re-run: flight 2 identical, flight 5 identical after `delvec fmt`). The upper street's script does not emit its program of record: its repair author added `shown_faces: ["west"]` to the JSON alone, so re-running the script drops that line — the JSON is the artifact of record and stands.
- **`delvec detail` writes the piece and the plan row when the only refusal is the whole's `DW0210`**: the page's `detail.md` says the verb runs every gate before any file is written; observed on every place so far, a place whose own gates pass is written and the run then exits 2 on the whole's darkness. Recorded as observed, not judged.

## Refusals, in order

Every `DW` refusal `delvec` printed during authoring, with its repair. Refusals a detail author met inside its own iteration (`grammar expand`, its own `detail` runs) are seen only through its report, and are recorded here as reported.

| # | Run | Code | What it said | Repair |
|---|---|---|---|---|
| 1 | step 1, validate | DW0874 | classes.json, quest-plan.json, quests.json absent | stubbed the three |
| 2 | step 1, validate | DW0112 | `quest-plan` names `area/site` and the campaign has no placement authority yet | step 2 writes the site-plan pipeline, whose one area is `area/site` |
| 3 | step 1, validate | DW0150 | the planned quest has no stage-5 expansion | the ordinary state until step 5; `quests.json` expands it |
| 4 | step 2, validate | DW0818 | the layout graph's beat names `quest/down-to-the-quay`, which stage 5 does not declare yet | clears with step 5's `quests.json` (DW0150 still standing, same cause) |
| — | step 3, validate | DW0150, DW0818 | still standing, the step-3 state | step 5 |
| 5 | step 3, scratch probe build (a copy outside the campaign with a throwaway quest; not the campaign) | DW0210 | the 19 stand-ins measure 144 of 1698 reachable cells dark, the stand-in houses' interiors | not repaired in the campaign; the probe alone took a site-plan `lighting` to see past it — see the open items |
| 6 | step 3, scratch probe build | DW0863 | the throwaway quest's objective is 97 blocks from spawn with no `hint` | owed by step 5's quest |
| — | step 5, validate | none | `quests.json` written; DW0150 and DW0818 cleared; exit 0 | — |
| — | step 7, analyze | none | exit 0 | — |
| 7 | step 8, build | DW0210 | 144 of 1698 reachable cells dark under the 19 stand-ins, darkest at [54, 84, 98] (the chapel's stand-in) | by ruling, carried into step 9: each house is lit as it is detailed; no `lighting` declaration |
| — | step 8b, validate | DW0900 (notice, not a refusal) | the six cameras in `design/cameras.json` name rows no `design.json` holds — by ruling there is none; each names the §6 view it answers | none owed; `delvec cameras` refuses to draw without `design.json` (DW0721 on a scratch copy), so the frames are drawn with `delvec frames` |
| 8 | step 9, `detail node/square` | DW0721 | `design/cameras.json`: camera `view-from-the-sea` answers `view/from-the-sea`, which is not a row of design.json (rows: none) — refused on every `detail` run while the record stands without a `design.json` | the camera record moved to `judging/cameras.json`, which no engine verb reads; `detail node/square` then exits 2 on `DW0210` alone |
| 9 | step 9, the chapel's author, `grammar expand` | DW0730 | `minecraft:candle` is outside the admission allowlist | the altar is bare stone; the nave is lit by four hanging lanterns (a lantern on the altar would be a third standable level) |
| 10 | step 9, the smithy's author, `grammar expand` | DW0730 | a lava cauldron (the forge) is outside the admission allowlist | two lit campfires under a masonry hood at the chimney foot |
| 11 | step 9, `detail node/warehouse` (the whole's battery) | DW0836 | `edge/flight-4-shore-street`: built climb −1 where the plan says 0 — feet at y 69 in `node/flight-4`, 68 in `node/shore-street` | flight 4 re-authored by a fresh agent (attempt 2), the refusal in its handout |
| 12 | same run | DW0833 | `fact/shore-walk-plane` measures 69 in the built world; the brief asks 68 (flight 4 stands on `datum/shore`) | same repair |
| 13 | same run | DW0836 | `edge/lower-street-flight-4`: built climb −3 where the plan says −4 — feet at y 72 and y 69 | same repair |
| 14 | step 9, flight 4's repair author, `detail node/flight-4` | DW0885 | once the battery passed, flight 4's east and west kerb sides stand in open air the party can be in, and the piece declares no `shown_faces` | the author declared `shown_faces: ["east", "west"]` — finished stone kerb faces meant to be seen |
| 15 | step 9, `detail node/flight-4` (attempt 2) | DW0885 ×8 | the same for flight 1 (east, west), the upper street (west), flight 2 (east, west), flight 3 (east, west), the shore street (east): kerb sides in the open hillside air, no `shown_faces`; the `ocean` horizon offers no ground above y 62 to bury them | each place re-authored by a fresh agent with the refusal in its handout |
| 16 | step 9, `detail node/shore-street` (attempt 2) | DW0921 | a soft-lock: 6 cells around [78, 65, 191] — a body gets in from [77, 67, 191] (flight 5's east kerb, in its ring) by a fall of 2 into the one-cell commons gap between that kerb and the warehouse's west wall, and nothing leads back to the route | flight 5 re-authored by a fresh agent (attempt 2), the refusal in its handout |
| 17 | step 9, flight 5's repair author, its own `detail` | DW0838 | its first fix opened both ring columns, and a body could walk through the south ring cells into `node/quay` — a crossing the plan did not allocate | piers two courses above the turf close the flight's south plane beside the quay opening; the ring columns stay open over the turf, so a body that steps off the flight can step back |

## Detail

One row per attempt. Handouts are regenerable files under `campaigns/saltstair-a/.out/handouts/<place>/` (gitignored). Before the first handout every node's `note` in `layout-graph.json` was given its rows of `campaigns/hillside/DESIGN.md` §3 and §5.1 — what the place is, what its program draws, its materials and its light — because the handout quotes the note and nothing of the hillside record.

| Place | Attempt | Handout | Agent tokens | Duration | Codes repaired | `delvec detail` exit |
|---|---|---|---|---|---|---|
| `node/square` | 1 | `square/handout-1.md` | 141 282 | 260 s | none (first authoring) | 3 — the place passes (3 faces for 3 seams, 2 of 2 owed names, light `lit` over 316 cells); the run refuses `DW0721` on `design/cameras.json` (six cameras answer rows of a `design.json` the campaign does not have). On a scratch copy without `cameras.json` the same run exits 2 on `DW0210` alone (the 144 dark stand-in cells) |
| `node/flight-1` | 1 | `flight-1/handout-1.md` | 141 614 | 299 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame |
| `node/upper-street` | 1 | `upper-street/handout-1.md` | 123 057 | 277 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame; the author read the start of another place's program (see Findings) |
| `node/flight-2` | 1 | `flight-2/handout-1.md` | 129 827 | 355 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame |
| `node/middle-street` | 1 | `middle-street/handout-1.md` | 126 964 | 259 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame |
| `node/flight-3` | 1 | `flight-3/handout-1.md` | 123 724 | 325 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame; the author ran a read-only git status (see Findings) |
| `node/lower-street` | 1 | `lower-street/handout-1.md` | 106 939 | 208 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame; the author ran a read-only git status (see Findings) |
| `node/flight-4` | 1 | `flight-4/handout-1.md` | 152 522 | 352 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame; the author ran a read-only git status |
| `node/shore-street` | 1 | `shore-street/handout-1.md` | 118 046 | 254 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame |
| `node/flight-5` | 1 | `flight-5/handout-1.md` | 145 697 | 374 s | none (first authoring) | 2 — DW0210 alone, 144 dark cells, none in this frame |
| `node/quay` | 1 | `quay/handout-1.md` | 154 943 | 344 s | none (first authoring) | 2 — DW0210 alone, still 144 dark cells, none in this frame; the author read the engine CLAUDE.md, outside its handout's reading list |
| `node/chapel` | 1 | `chapel/handout-1.md` | 156 030 | 470 s | none (first authoring) | 2 — DW0210 alone, 124 dark cells (from 144), none in this frame; the author met DW0730 on candles (refusal 9) |
| `node/inn` | 1 | `inn/handout-1.md` | 165 943 | 544 s | none (first authoring) | 2 — DW0210 alone, 83 dark cells (from 124), none in this frame |
| `node/smithy` | 1 | `smithy/handout-1.md` | 167 467 | 539 s | none (first authoring) | 2 — DW0210 alone, 79 dark cells (from 83), none in this frame; the open front is a recorded departure (Findings); the author met DW0730 (refusal 10) |
| `node/weaver` | 1 | `weaver/handout-1.md` | 155 095 | 436 s | none (first authoring) | 2 — DW0210 alone, 73 dark cells (from 79), none in this frame; the author ran a read-only git status |
| `node/merchant` | 1 | `merchant/handout-1.md` | 150 386 | 367 s | none (first authoring) | 2 — DW0210 alone, 48 dark cells (from 73), none in this frame |
| `node/ropewalk` | 1 | `ropewalk/handout-1.md` | 145 751 | 361 s | none (first authoring) | 2 — DW0210 alone, 39 dark cells (from 48), none in this frame; the open street side is a recorded departure (Findings) |
| `node/harbourmaster` | 1 | `harbourmaster/handout-1.md` | 146 606 | 390 s | none (first authoring) | 2 — DW0210 alone, 35 dark cells (from 39), all in the warehouse's stand-in |
| `node/warehouse` | 1 | `warehouse/handout-1.md` | 154 414 | 423 s | none (first authoring) | 3 — the place passes (light lit over 113 cells); DW0210 cleared for the whole; the battery then refuses flight 4 (refusals 11–13) |
| `node/flight-4` | 2 | `flight-4/handout-2.md` | 87 876 | 204 s | DW0836 ×2, DW0833 (refusals 11–13) | 3 — the place's refusals cleared (foot at 68, four risers, rise from the handed value); DW0885 ×8 stands on five other places (refusal 15) |
| `node/flight-1` | 2 | `flight-1/handout-2.md` | 70 712 | 58 s | DW0885 ×2 (refusal 15) | 3 — its own refusals cleared; DW0885 ×6 stands on four other places |
| `node/upper-street` | 2 | `upper-street/handout-2.md` | 68 730 | 56 s | DW0885 ×1 (refusal 15) | 3 — its own refusal cleared; DW0885 ×5 stands on three other places. The author edited the JSON and not its generator script, which no longer emits it exactly |
| `node/flight-2` | 2 | `flight-2/handout-2.md` | 69 700 | 68 s | DW0885 ×2 (refusal 15) | 3 — its own refusals cleared; DW0885 ×3 stands on two other places |
| `node/flight-3` | 2 | `flight-3/handout-2.md` | 65 058 | 85 s | DW0885 ×2 (refusal 15) | 3 — its own refusals cleared; DW0885 ×1 stands on the shore street |
| `node/shore-street` | 2 | `shore-street/handout-2.md` | 66 872 | 50 s | DW0885 ×1 (refusal 15) | 3 — its own refusal cleared, all DW0885 gone; the leave-proof then refuses a pocket by flight 5 (DW0921, refusal 16) |
| `node/flight-5` | 2 | `flight-5/handout-2.md` | 85 652 | 215 s | DW0921 (refusal 16) | 0 — the whole builds with every place detailed; 0 of 32 164 reachable cells a body cannot leave; the author met DW0838 on the way (refusal 17) |

## Step 9 closed, the build that ships

`delvec detail --all` 0 (19 of 19 places detailed; the run moved no byte); `validate` 0; `analyze` 0; `build` 0 into the engine's `validation/delve-output`. Blockout: 19 places massed, 19 detailed, 0 by the derivation — **0 stand-ins**. Battery: 18 seams proven (5 contacts, 13 portals), 19 places reached, 0 cracks. Leave-proof: 0 of 32 164 reachable cells a body cannot leave. Advisories standing: `DW0822` — the critical path measures 115 blocks over 10 legs, about 2 minutes at the metrics table's rate, against `target_minutes` 10 (the design's own walk is the street and back, then the hillside and the beach; the number is reported, not acted on); `DW0813` (provisional metrics); `DW0781` (the piece-mating check examined zero abutting faces: in cut A no two pieces touch — every neighbour is one ring cell away).

## Step 10, the machine ladder

On the build that ships (`manifest.json` sha256 `f25e01a7c9f6b9b453fb2b8c9ce35ee04263e0e6c5b8f575a769eeff11ce673b`):

- PackTest (`packtest-run.sh --project dw-saltstair-a-r1`): exit 0, all 17 required tests passed.
- Bot (`bot-run.sh --project dw-saltstair-a-r1`): exit 0, the critical path passed — spawn on the square at [74, 84, 97], down the main street, the `reach-anchor` objective on the quay; 3 steps; 2 of 2 owed cues arrived. Stages not run, each with the build's reason: die-retry (no mandatory combat), death-loop (no lethal volume), crush-death (no crush gate) — advisories, not passes.
- No `validation/branch-plan.json` was emitted, so there are no branch runs; step 11 does not apply (the plan declares no `branch_points`).
- Written world (`world-save.sh`, `delvec written-world`, `check-written-world.py`): each exit 0 — the server's world is the engine's model.

## Step 12, visual review

`delvec frames` on the build that ships: `renderer: lumenwright 0.3.0, backend cpu (16 threads) (auto: fell back to cpu — no usable GPU (only a software Gpu adapter is available))`; 63 of 63 shots, all at the world's clock (`noon`). The POV sequence, square to quay, read in route order against `campaigns/hillside/design/reference/view1-from-the-sea.jpg` (no concept set exists): the street is the place the image shows — cobbled terraces between stone-brick kerbs, stone-brick flights between stepped kerbs, lanterns on kerb posts at every flight and door, timber-framed calcite houses with deepslate and dark-oak roofs, the stone quay with spruce-log bollards. Findings, document-level, not repaired:

- **A row of turf crosses the paved street at each of the five flight-foot contacts.** The contact's ring row is the whole's fixed ground; under cut A no place owns it, so neither the flight nor the street paves it.
- **The open fronts** (smithy, rope walk) are windows — the departure under Findings.
- **No house interior is on a POV frame**: no house is on the critical path; each house's own light probe reads `lit`.

## The six §6 cameras

`judging/cameras.json` holds the six rows at §6's exact eyes; yaw and pitch are derived from §6's `look_at`, fov 70. Drawn three ways, all into `judging/frames/` (local, not committed — renders are regenerable from the build):

- `noon/` — `delvec frames --campaign campaigns/saltstair-a --camera <x,y,z,yaw,pitch,70> --size 1536`, the campaign's own sky.
- `day/` — the same command on a scratch copy that differs from the campaign only in `world.time: day` (diffed: one line).
- `cameras-day/` — `delvec cameras` (path traced, 1920 × 1080, 256 samples, sky `day` stated per camera) on a scratch copy that adds a one-row `design.json` naming the reference image, which `delvec cameras` requires; the campaign carries none, by ruling.

Every manifest's camera position equals the row's exactly; the aim is within 0.0005° of §6's `look_at` (the manifests round to three decimals). Read against §6:

- `view/up-the-street`, `view/from-the-south-east`, `view/the-merchants-terrace` show what §6 says they judge.
- `view/down-the-street` is mostly the square's paving and its south parapet: from 1.6 above the square the flights fall below the parapet line.
- `view/the-first-flight` stands inside the smithy: §6's eye [68.5, 81.6, 120.5] is within the smithy's footprint (x 62..69, z 119..126, floor 80, §4.2), so the frame is the smithy's inner wall and a window. A property of the design's coordinates; not moved.
- **Instrument limit**: neither `delvec frames --campaign` nor `delvec cameras` draws the `ocean` horizon beyond the site plan's region. A camera standing past it (`view/from-the-sea`, z 232.5 against the region's last row z 223) or seeing past it (`view/from-the-south-east`) shows the region's cut face — dirt to the sea bed under the water slab — where the game shows open sea.

## The five numbers (DESIGN.md §6)

1. **Distinct floor levels**: 21 — every `y` from 64 to 84 — over 210 of 210 columns on the centre line (x 73 and 74, z 96..200), read from the server-saved world (`world-save.sh`) through `tools/lib/anvil.py`; a cell is standable when it and the cell above are passable and the cell below supports. The 6 datums and the 15 tread levels of the five four-tread flights.
2. **Ring cells**: the battery examines 700 plot-edge columns (`blockout battery binding: … 700 plot-edge column(s) examined, 0 crack(s)`); read from the same saved world over the same 700 (each footprint-edge column paired with the ring column outside it), 96 stand more than one block from the ring's surface — faced edges, every one held by a solid face (0 cracks) — and 329 offer no standable surface to compare (a house wall on the ring, mostly). Per box: square 8, flights 4/4/4/5/2, upper street 20, middle 13, lower 23, shore 10, quay 3, every house 0.
3. **Refusals per code**, from the table above (24 in all): `DW0885` 9, `DW0210` 2, `DW0730` 2, `DW0836` 2, `DW0112` 1, `DW0150` 1, `DW0721` 1, `DW0818` 1, `DW0833` 1, `DW0838` 1, `DW0863` 1, `DW0874` 1, `DW0921` 1. Counted by logged row; `DW0210` was also printed by each of the eighteen confirming `detail` runs it was ruled to stand through, and refusals inside an author's iteration count only as reported.
4. **Author tokens and time**: the 26 detail-author attempts used 3 220 907 tokens and 7 573 s, from the Agent tool's completion records; the orchestrating session's own tokens are not in a record this run can read. Wall clock from the first campaign commit to the green ladder: 2 h 33 min, including the pause at the design gate.
5. **Build and bot status**: `delvec build` 0; PackTest passed (17 of 17); the bot's critical path passed; the staging gate refused on `DEMO-UNQUEUED` alone, by ruling.

## Step 13, the staging gate

`staging-gate.py` over the build that ships, with the ladder's run report and the written-world record: **REFUSED — 1 of 148 findings**, `DEMO-UNQUEUED` (no row of the pinned engine's demo queue names `campaigns/saltstair-a`), accepted by ruling and not overridden. Every other row judged: `BOUND` 21, `INAPPLICABLE` 99, `DECLARED-UNCOVERABLE` 27, `NO-SOURCE` 0, `NO-GENERAL-FORM` 0, `MISSING-CHECK` 0, `UNBOUND` 0. The full report is `judging/staging-gate.md`. Storybook marker: `check-storybook-version.py` OK on this campaign (the repository-wide run fails on other campaigns' storybooks only).
