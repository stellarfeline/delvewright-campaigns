# The Hush Garden — generation record

## Toolchain

- Authored through `/new-delve`, every step in order, from engine `feat/native-entrance` at `ffe9b58ae18cb935fba20b1db738526fd1a32b2b` (spec-0132: a body's native entrance, `outrun` and the bot's `pursuit` stage; spec-0131: every line of the plan declares its activity). The page read is that revision's `.claude/skills/delvewright/skills/new-delve/`.
- `delvec 1.16.0, dsl 0.71.0, mc 1.21.11`, built from source in release mode in that tree (Init I3b, cargo exit 0). `dsl_version` 0.71.0 on every document.
- Init departure: the page's pin names the release `delvec--v1.16.0`, and this campaign needs spec-0132, which no release carries yet. The pin check ran in its dev form (the engine tree's own version compared, its commit recorded), and exited 0.
- Prefabs: this content clone's own `prefabs/`; the campaign's pieces are its own.
- Reference images: `tools/creator/refimg.py` on `gemini-native` (`gemini-3.1-flash-image`).
- Languages: English, and Simplified Chinese as a sidecar (`zh-cn`).

## What the brief pinned, and what was invented

Pinned:
- A maze for two players. Both start in the middle. They may split up: both look for the way out, or one climbs a high platform that overlooks the maze and calls directions to the other. Played alone, the walker finds the way and may die and try again.
- Monsters in the maze, and a warden. The warden starts from its own point, not the players', and arrives only once the players have made some progress. Its arrival is a close-up of it digging out of the ground; then it hunts.
- Two phases. While the warden is searching, the walker sneaks and the guide draws it off: eggs or arrows thrown toward a spot, or buttons on the platform that each ring a bell at a fixed spot in the maze, each with a cooldown or a limited number of uses, so the warden cannot be held forever. Once it is hunting the walker it ignores lures: the walker breaks the chase through the maze's loops while the guide only calls the way.
- The end: the walker sets off a mechanism that raises a bridge or passage straight across the maze, so the guide can cross.
- No combat is encouraged; the warden is too strong to beat.
- A simple story: an escape.
- The feel of a small two-player level of a cheerful co-op game. Fun first.

Invented: everything `DESIGN.md` names beyond that.

## Step 2 — placement

- The map's reference was drawn as a series of single views on `gemini-native`, view 1 from the prompt and every later view chained to view 1's interaction, under one style contract (`design/reference/style.txt`). Kept: view 1 (the whole garden from high in the south-west), the straight-down plan and the eye-height lane. A view from the lookout deck came back twice in breach of the contract (the gate tower inside the maze, the hedge caps gone) and was dropped from the series; it is not redrawn.
- Nearest reference works: The Treehouse Camp (places at two heights joined by a bridge and ladders; a connector is a place) and Vesperhold (one box holding a whole site). The maze is one place whose piece draws every lane; the courts, the well and the bells are stations inside it.
- The maze's size was settled at 85 × 85 against the warden's 16-block hearing reach: 28 lanes of a 3-block pitch, the nearest the pitch allows to 84 with an outer wall on both sides. The pattern, its dead-end and loop counts and its critical route are the generator's, measured on the built map.
- `edge/onto-the-bridge` and `edge/the-great-gate` are both gated on `flag/gate-wound`: one turn of the winch opens the gate and raises the bridge.

## Step 3 — the story documents

- One character, the gardener, met at the end; two classes, Runner and Caller, either playable alone. The level needs no second player (`min_players` is absent).
- The plan is a hub (the note), one mandatory spoke (the crank, which wakes the sleeper), one optional strand (ringing a bell from the deck) and the finale (wind the gate, walk out, talk). The ending is to read whether the caller crossed the bridge, an elective deed.
- The bell budget (three rings a bell, twenty seconds between rings) and the price of a thrown egg or arrow come from the measurements: a bell is a lure with no thrower, a projectile puts its thrower on the warden's list.
- `target_minutes` came down from 30 to 25 when the lines were budgeted by activity.
- The validation state at the end of the step is the step-3 state: the planned quests have no expansion yet (`DW0150`), the gate's flag and its opener are written at step 5 (`DW0818`, `DW0816`, `DW0817`, `DW1028`), the gardener's dialogue tree and the `zh-cn` sidecar are step 5's (`DW0152`, `DW0180`). Beside them, `DW0890` names the three map reference views under `design/reference/`, which have no row in the design record until step 4 writes it.
