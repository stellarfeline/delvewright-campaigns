# The Glasshouse — generation record

## What the brief pinned, and what was invented

- **Purpose, pinned**: the engine's standard level for judging the render route (tone curve, light, sky, weather, denoise). Every picture this level owes is a render item: open sky over grass, trees, a path and still water; known material tones (planks, brick and stone, glass); sky light falling under glass; a room lit only by placed light of at least two kinds; one dark low place lit by a single source; a long view to the horizon; and one whole-map picture.
- **Size, pinned**: a demo level — one compact site, 10 to 20 minutes, minimum cast.
- **Working title, pinned and kept**: The Glasshouse — a walled garden around a glass conservatory, with a lit potting room and a cellar.
- **Invented**: the frost-night errand that walks the party through every part in turn; the head gardener; the lemon tree; the stove cellar as the conservatory's stoke-hole; the belvedere on the west wall as the long view; the lime walk as the approach.

## Engine and record

- Engine release `delvec 1.13.0`, `dsl_version` `0.39.0`, skill page of plugin version 1.13.0 (its own pin, `delvec--v1.13.0`).
- Placement model: site plan. The thing the delve is named after — the conservatory — has an exterior silhouette the player reads against the sky, and the shipped library holds no piece that is it.
- Prefab library: the content repository's own `prefabs/`, at the revision the engine pin names.
- Languages: English only, confirmed at the design gate.

## Posture note

Three axes pushed off the default for this campaign: **emotion named outright** — Wenna says she is frightened for the tree, in those words, and no one clenches anything; **resolution left open** — the delve ends before morning and never says whether the lemon tree lives; **thematic explicitness low** — no line states what the evening means, and the one confession (she has never watched the sun go from the belvedere) is handed to the party as an errand, not explained. Quiet and domestic otherwise; no combat, and the frost never arrives on stage.

## Faces

Wenna Hale wears her own skin (`skins/cast.json`, composed with the engine's skin toolchain, slim model).

## Building it

- Every place is a grammar program written by `design/programs-src/places.py` through `vox.py`, a voxel-to-program compiler taken from The Treehouse Camp's design sources in this repository. Re-run `python3 design/programs-src/places.py all`, then `delvec detail <campaign> --all`.
- The site plan moved four times after the design gate, each time because a refusal on the built bytes required it: the stove cellar grew to 10 × 8 so its furnace's interact camera stands inside the room (`DW0724`); the garden's open ceiling came down to 6 because a shared wall must stand to the lower claim's top (`DW0836`); the belvedere came down to y 68 (four steps) to sit under that ceiling; the lime walk grew to 16 × 14 because a crown overhanging a plot edge reads as a cliff (`DW0990`).
- The long-view camera stands 15 blocks over the belvedere: from the terrace's own eye the valley rim (`rim_height` 16, the engine's floor) stands above the eye line and hides the true horizon.

## Findings

| finding | where it stands |
|---|---|
| A dirt path under a block (a step, a lantern post) is turned to dirt by the server; DW1002's survival table does not carry the rule, so only the written-world check (DW0955) saw it | fixed in the pieces (coarse dirt under a block); the engine gap is reported |
| The lawns were sunk one block: a piece's own floor-course cell left unset is air | fixed in the pieces (`lawn`); no gate caught it, a render did |
| From the belvedere the valley rim hides the horizon at every rim height the engine allows | the long-view camera stands above the rim; open as an engine limit |
| A stair through a floor cannot be entered from the side the treads face when its top tread sits in the upper place's floor course — the route is only found from a side with no rail | the potting room's hatch has no rail on its west side; open, not understood |
