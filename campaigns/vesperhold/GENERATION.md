# Vesperhold — generation record

## Toolchain

- `/new-delve` plugin 1.5.0, engine release `delvec--v1.6.0`, `dsl_version` 0.29.0.
- Placement: site plan. The castle is the thing the delve is named after and the story asks the party to read its silhouette from the valley, so no prefab can be it.
- The shipped prefab library was not taken at step 2. The working tree's `prefabs/` holds LFS pointers only; it will be named with its revision if step 13 takes it.
- The engine constitution's operating half (`CLAUDE.local.md`) was not available to this run; nothing here decides dispatch, review, merge or staging.

## What the brief pinned, and what was invented

Pinned: souls-like combat and exploration; a cryptic main plot; one huge Gothic castle with regions and a spectacular exterior; twenty or more designed places; about half of Stormveil Castle; up to four co-op players; an hour or more of play; ruined or whole at the author's choice; a second timeline ten years earlier allowed; research before authoring.

Invented: everything named in `DESIGN.md` — the bell and its price, the Undertide, the cast, the route, the memory wing, the two endings.

Research consulted before authoring (ideas only): the anatomy of Stormveil Castle and the lessons of other souls castles for structure, rest spacing, shortcuts, gatekeepers and traps; FromSoftware's fragmented storytelling, recurring allies, tricksters and past-layer precedents for the story and the memory wing.

## Decisions

- The second timeline is a walkable memory wing with a sky cut at its threshold, because the engine has no timeline primitive.
- The castle is a ruin in the present and whole in the memory.
- In-game text ships in English with a `zh-cn` sidecar.
- `difficulty` is `normal`: the souls baseline, without zombie reinforcement muddying the tuned waves.
- `horizon` is a valley with a 64-block rim, so the castle stands in a mountain bowl and the causeway crosses its floor.

## Posture note

Three axes pushed off the default for this campaign: **time order** — the decisive event is shown out of order, in the memory, after its consequences; **morality** — the final boss is right and the sympathetic keeper caused the ruin; **emotion rendering** — Warden Hesk names her fear outright ("I am afraid of the day I will not know her"). The Silence ending is disproportionate to everything before it and explains nothing.
