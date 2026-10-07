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
