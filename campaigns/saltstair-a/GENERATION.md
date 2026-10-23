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

- **DEPARTURE — an open street front cannot be built under cut A as written.** §3 makes the smithy "open-fronted toward the street" (and the rope walk "open along its street side"); §5.1 gives each exactly one `door` seam. Every open cell of a house wall that is not an allocated seam is an undeclared way out, refused by the piece's closure and coverage gates, so the open front is not authorable without changing the plan (a `contact` seam along the street face instead of a `door`), which the brief forbids. The smithy's author built the closest authorable thing: a three-wide forge window filled with iron bars over a counter, beside the door.
- **The weaver's "cloth on the upper floor" is a closed loft.** The plan gives the house clearance 4 and a 5-course roof; a second storey a body reaches would need a climb into the roof zone, above the handed play space. The cloth is there, as wool on the loft floor under the roof; nobody can walk up to it.
- **The retaining walls between terraces stand only where a flight's frame reaches.** Under cut A a street's frame begins at its paving course, so the four-course drop at a terrace's downhill end is below it; the flight's frame (floor the lower terrace) is the one place that can face it, six wide, and the drop beside the street, outside every box, is the commons hillside at the heightmap's half-block grade. §3's "every terrace stands above the next behind a retaining wall the place draws" is therefore met six wide at each flight and not across the town — a property of the cut, reported by the upper street's author.
- **A `stair` contract edge to `exterior` cannot carry a rise** ("no resolved box on the far side"), reported by flight 3's author: a flight whose whole climb is its seam's rise is two spaces joined by an interior `stair` edge, with a rise-0 edge at the seam. Authorable; recorded as the engine's shape, not a gap that blocked anything. Flights 3 and 5's authors add that the contract's `rise` takes only a literal integer, so each flight's generator copies it from the allocation's handed seam rise rather than binding `handed/seam/<edge>/rise`.
- **Detail authors stepped outside their handout**, each recorded on its row of the Detail table: several ran a read-only `git status`, and the upper street's author read the start of `programs/flight-1.json` before writing, stopped, and reports building nothing from it. No attempt was discarded for it: every piece passes its own gates, and every confirming run moved no byte.
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
