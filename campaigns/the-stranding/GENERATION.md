# The Stranding — generation record

The campaign's own decisions, as its author records them. `DESIGN.md` is the design of record; this file says which of its lines were pinned by the brief, which were invented, and what the toolchain was.

## Toolchain

- Engine release `delvec--v1.8.1` (commit `ff6bd4929a499d4eb7a1e55372912ea1ab2301fd`), binary `delvec 1.8.1, dsl 0.35.1, mc 1.21.11`, from the release archive `delvec-v1.8.1-aarch64-apple-darwin.tar.gz` (sha256 `f4074a8d0d20264155fb1bf856cab5be77384e4e79c99efa17809bdd6c22b671`).
- Every document carries `dsl_version` `0.35.1`.
- Prefab library: this content clone's own `prefabs/`; no prefab changed between the engine's pinned `[content].sha` `ff73411a1d7feabad57a4537e1384402a2b096d0` and the branch head the run started from.
- Reference images: `gemini-native`, model `gemini-3.1-flash-image`, series anchored with `--chain-from` on map view 1, style contract in `--style-note`.
- The engine's other half of its constitution (`CLAUDE.local.md`) is not available to this run; nothing here concerns dispatch, review, merge or staging.

## What the brief pinned

`DESIGN.md` is a detailed brief, so it is honoured exactly and nothing is showcased beyond it: four acts and thirty-six places in the order it gives, the cast of four, the four classes and their kits, the fights and tentacle counts, twelve cutscenes, the two endings, the danger model, the light plan, the hour (`night`, `clear`, full moon) and the site-plan placement model.

## Decisions made here

- **Placement model: a site plan.** The thing the delve is named after (the stranded body, and the town on its terraces) has an exterior silhouette the player reads from the town and the flat; no prefab is either. `DESIGN.md` pins this too.
- **Horizon: `ocean`.** `DESIGN.md` made `ocean` conditional on the library's sea pieces carrying `waterline_y`. The step-1 query found that the two sea-facing pieces do (`cave-shore` in `pool/cave-shore`, `island-beach-camp` in `pool/island`) and the rest of those pools, which are interiors, do not. A site plan places no pool piece, and it has no water surface of its own: the plan reads sea level from `horizon: ocean` (y 62), which is exactly the sea level `DESIGN.md` gives under the flat (mud at y 64 over water at y 62). A `void` horizon would leave the plan with no way to put the sea in the map, so the conditional's other branch is not buildable. `boundary` carries a message either way, as the brief asks.
- **Seed** `1919`. **Difficulty** `normal`, which the brief's tuning line names.
- **Atmospheres declared at step 1**: `wrong-place` (olive sky, close yellow fog, red clouds, no music), `inside-body` (dark red, close fog, no music), `red-night` (the body, the bank and the flat after the cut), `sea-fog` (the endings). The colours are first values, to be judged against the design images.

## Posture

`DESIGN.md` § Posture is the posture note: escalation is uneven, people name their fear, and the ending does not explain itself. Every line written at step 5 is held to it.

## Step 2 — the site plan

- **The map's reference** is five views under one style contract (`design/reference/style-contract.txt`), view 1 from the prompt alone and every later view chained on view 1: from above the coach road, a plan, a west elevation, the body from the Narrows, and from above the tail looking north. The plan view was drawn twice: the first return laid the body east-west, against the plan; the second, with the orientation stated, is the one kept. Reference images are style authority only; the geometry is `geometry-brief.json` and `site-plan.json`.
- **The body lies north-south, head to the north**, facing the town across the black water, with the Flank Ridge along its west side. `DESIGN.md` does not state the heading; this one puts the mouth at the Jaw Bank where the crossing lands and the flank wounds in sight from the ridge and, obliquely, from the Narrows.
- **Covered stairs.** A stair seam's opening has to lie inside both places' headroom, and a sky-open place claims only its size class's minimum headroom (a road six courses, a hall eight, an arena twelve). So every stair with a rise of eight is hosted in a roofed place: a covered flight of cliff steps between the coach road and the high street (a place `DESIGN.md` does not list), the harbour office, a covered fish market hall, the chapel crypt and the rope shed. The net lofts sit three courses above the seawall and the mast platform four above the launch's deck so that their open hosts can carry the stair.
- **The Run's descent is four broad steps.** Forty blocks from the back to the bank cannot be one open-air stair under that rule, so the back falls in four arenas of eight courses each (`back-upper`, `back-middle`, `back-lower`, `tail-flank`) to the bank behind the tail, which lengthens the tail beyond the brief's 140 blocks. Recorded as a capability limit, not a design choice.
- **No massif for the body.** A whole-owned volume may not contain a place, and the body's inside is places, so the blockout has no outer body mass. Its exterior shape is the sculpted form's (`delvec sculpt`), bound at step 13.
- **Two placement components**: the town and the flat (pinned at the coach road) and the far bank with the body (pinned at the far landing), joined only by the `carry` crossing and the two ferry bells.
- **Blockout lighting** (`lantern`, minimum 7) lights the derived massing for the walk only; detailed places carry their own placed light.
