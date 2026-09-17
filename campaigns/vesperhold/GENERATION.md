# Vesperhold — generation record

## Toolchain

- `/new-delve` plugin 1.5.0, engine release `delvec--v1.6.0`, `dsl_version` 0.29.0.
- Placement: `areas[]` with one area bound to one campaign-built piece, `prefab/vesperhold` — the whole site as a grammar program generated from `design/programs/`, ringed by a `valley` surround. A site plan was drafted first and dropped: its derived walls and roofs are the blockout's fixed palette and stay whole-owned after detail, so it cannot give the castle a designed exterior, which is the brief's one standing requirement (the Doune Castle site in this repository is the bar). The same single-area shape rules out a second space, so the second timeline is told as echoes in the present rooms.
- No shipped library piece is bound; the campaign's only piece is its own.
- The engine constitution's operating half (`CLAUDE.local.md`) was not available to this run; nothing here decides dispatch, review, merge or staging.

## What the brief pinned, and what was invented

Pinned: souls-like combat and exploration; a cryptic main plot; one huge Gothic castle with regions and a spectacular exterior; twenty or more designed places; about half of Stormveil Castle; up to four co-op players; an hour or more of play; ruined or whole at the author's choice; a second timeline ten years earlier allowed; research before authoring.

Invented: everything named in `DESIGN.md` — the bell and its price, the Undertide, the cast, the route, the echoes, the two endings.

Research consulted before authoring (ideas only): the anatomy of Stormveil Castle and the lessons of other souls castles for structure, rest spacing, shortcuts, gatekeepers and traps; FromSoftware's fragmented storytelling, recurring allies, tricksters and past-layer precedents for the story and the echoes.

## Decisions

- The second timeline is told as echoes: a sky cut and the people of that morning staged in the present room, because the engine has no timeline primitive and the one-area site holds no second space.
- The castle's exterior is designed block by block and must read at least as well as the Doune Castle site.
- The castle is a ruin in the present and whole in the echoes.
- In-game text ships in English with a `zh-cn` sidecar.
- `difficulty` is `normal`: the souls baseline, without zombie reinforcement muddying the tuned waves.
- `horizon` is a valley with a 64-block rim, so the castle stands in a mountain bowl; the approach and the causeway cross the piece's own valley floor.

## Content decisions

- The past is staged in the present rooms: two echoes put the people of the Last Vesper's morning where they stood (a deferred NPC and skinned actors), the third is the campaign's one camera cutscene. The engine's `DW0351` advisory on the two deferred NPCs is accepted with narrative cover — each appears under the title card of an echo ("the morning of it", "The stair remembers.") and leaves as the rain returns.
- The chapel echo is two quests (`the-chapel-echo`, `the-wardens-key`) because a body spawned mid-quest can only be cast from the next quest on.
- Both forks put their options in one node, each option setting its flag and completing the talk objective, so the two branches are exclusive by construction. Halvard leaves the watch tower on both branches; only what the party finds at the Throne Fire differs.
- Wave mobs that are one kind of creature share one name on purpose: `Nameless Soldier` (barracks and armory), `Hired Knife` (both mobs of the walk ambush). The `zh-cn` sidecar translates each consistently.
- The `zh-cn` sidecar was translated in-agent from the finished English, with each character's speech style held (Halvard archaic and courteous, Pellam wheedling, the apprentice blunt).

## Posture note

Three axes pushed off the default for this campaign: **time order** — the decisive event is shown out of order, in the echoes, after its consequences; **morality** — the final boss is right and the sympathetic keeper caused the ruin; **emotion rendering** — Warden Hesk names her fear outright ("I am afraid of the day I will not know her"). The Silence ending is disproportionate to everything before it and explains nothing.

## The castle piece

The whole site is one grammar-built piece, `prefab/vesperhold`, expanded at **172 x 104 x 292, seed 1** and bound in the campaign's one area under a `valley` horizon. `design/programs/build_castle.py` paints the site into a voxel grid from one module per part (`castle/terrain.py`, `approach.py`, `walls.py`, `ward.py`, `cathedral.py`, `undercroft.py`, `keep.py`, `belltower.py`), reading every position from `castle/layout.py`, derives every stair's shape the way vanilla does, and emits the grammar's partition as `vesperhold.json`. `finish.py` expands it into the prefab library and writes the six gate regions (`gates.json`) into the manifest — the grammar declares point anchors only — then measures the planes and the lighting and audits the piece. Re-run both to regenerate.

Heights in piece coordinates: valley floor feet 8, castle floor 24, keep dais 28, wall walks 36, bell deck 52, undercroft 12.

What the machine said about the piece at admission: every expansion gate passes (blocks exist, shapes and states complete, oriented fills, stair shapes as vanilla derives them, fluid contained); `prefab audit` passes; `walk_y` 8; lighting profile `dark` over 43290 floor cells reachable on foot; the area's torch pass (`min_light` 3) lights the rest at build. With every gate open, all 83 point anchors are reached on foot, and with only the postern open no floor a body can fall to is without a walk back to the Cloister Fire (author-side checks over the painted grid, not engine gates).

The valley field is ringed by a two-course dry-stone wall on the piece's edge, and `world.boundary` holds the party four blocks beyond it, so the party's world ends where the piece does. The causeway's parapets are unbroken, iron bars between merlons, so nothing on the bridge is a way off it.

### What the build asked of the piece

- **Three doors are built open.** The postern, the Keep Doors and the Warden's Door are air in the piece and shut by `close-gate` when the party first speaks with Tamsin, a few steps from the spawn. Built shut, the stake proof (`DW0525`) refused every rest behind them: the delvec 1.6.0 compiler reads a door the piece builds shut as shut again at the two critical-path steps past the last objective, where no opening precedes, so from the Cloister Fire the whole valley read as unreachable. A door built open and sealed at a story step does not carry that reading. The engine side of this is a finding for the engine, not a fence the campaign works round forever; when it is fixed the three doors can be built shut again. The shortcut doors stay built shut, as the engine requires.
- **The Almoner's Door is barred for good.** As a shortcut it failed `DW0374`: from the campaign entry the Keep Doors reach the Great Hall sooner than the cloister lane does, so opening it shortened no walk. The Throne Fire already stands beside the keep's fights. The door stays in the hall's west wall, as the approved image shows it.
- **Every reach volume is sized to its own floor** (`DW0881`), so no cube takes in a parapet top or a floor on the far side of a wall. The Buttress Walk gained a short roofed arch where its objective is, so the parapet under it is no floor, and the Antechamber's floor was filled beneath, closing a hollow.
- **Two flights gained a newel post** at their first tread (the rampart stair, the bell tower's first flight), so the only way onto them is up their climb (`DW0430`).
