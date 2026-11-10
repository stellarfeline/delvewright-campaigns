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

## Step 4 — the design gate

- The walkthrough (the three map views, then seven scenes each with a near and a far view, each under its hour and weather) was handed over, and the answer was an explicit yes to this delve. The approved pictures, their sidecars and prompts are in `design/`, one row each in `design.json`.
- `concept/lane-near` was drawn twice; the first was dark and muddy against the style contract. The deck's near view was drawn once; the deck's far view is the heart's.

## Step 5 — quests and dialogue

- **Posture note.** Three axes off the machine default: Wren names her feeling outright (*I was frightened for you the whole way across*); the note addresses the reader directly (*If you're reading this you're locked in*); and the escalation is uneven, a quiet garden errand broken by one disproportionate beat, the warden digging out in a close-up, with nothing resolved about it at the end (the sleeper is never beaten and is still under the garden).
- The bells are four `use` triggers on the deck's buttons, each a party datum counting its rings (three) and a second datum holding it quiet for 400 ticks after a ring. A ring is a redstone block set beside the bell for 4 ticks and cleared: the measured way to ring a bell a warden hears (`warden-behaviour.md` §5).
- The optional strand's body is reading the bell book on the deck (an `interact` on a bookshelf); a lectern cannot carry a click box (`DW1059`).
- The finale's winch takes the crank from the hand (`requires_item` + `takes_item`), so the line performs `present` and `give` beside `use`; the plan's declaration was brought up to it.
- The warden (`actor/the-sleeper`) is unleashed with `entrance: "native"` and `outrun: true` when the crank is taken, followed by a 7-second push-in on it; the checkpoint moves to the sundial court in the same beat.
- `difficulty` is left to the engine's derivation (`easy`, as the campaign stages waves).
- The `zh-cn` sidecar was transcreated by `tools/creator/i18n-translate.py` on DeepSeek (61 rows, 0 refused); seven lines were then held to one word for the garden's bells (钟) through `delvec l10n-apply`.
- Census at the close of the step: `activity census: 4 line(s) over 8 objective(s) — reach 3, talk 1, take 2, use 2, present 1, give 1; about 14 min of activity (12 on the mandatory lines) against target_minutes 25; 0 line(s) talk-or-reach only`. `DW0822`: 133 blocks of route over the plan's boxes, about 3 minutes; about 17 minutes in all against 25. The route through the maze's lanes is measured on the built map.

## Step 5b — the script review

Script review: ran; the prompt pinned the maze, the two roles, the warden's two phases, the lures and the bridge, and left the note, the crank, the gardener and every line's deed and reason to me.

### Round 1 — verdict `revise`

| Question | Findings | Worst severity |
|---|---|---|
| Q1 | 2 | 2 |
| Q2 | 1 | 1 |
| Q3 | 0 | — |
| Q4 | 2 | 3 |
| Q5 | 3 | 2 |
| Q6 | 1 | 2 |
| Q7 | 1 | 1 |
| Q8 | 0 | — |
| Q9 | 1 | 2 |
| Q10 | 5 | 3 |

- F1 (3, the caller is never told how to get out): fixed. Winding the gate now narrates the bridge swinging up to the deck and says whoever is on the deck can walk across; the note says beforehand that winding raises the bridge.
- F2 (3, the ending fires before the caller has crossed): fixed. When nobody has crossed, Wren asks whether anyone else is inside and the runner can answer *I'll wait for them* (closes) or *Just me tonight* (completes). `DESIGN.md` §5 updated.
- F3 (2, the bridge is said to be down, not raised): fixed in the note, the wind beat and Wren's line.
- F4 (2, Wren contradicts herself): fixed; she watched the crossing from the meadow.
- F5 (2, the solo ending asks after a friend): fixed with F2's wording.
- F6 (2, the bell book does not pair colours with buttons): fixed; each button sits under a sign of its quarter's colour, and the book says so.
- F7 (2, the runner's objectives walk them to each place): fixed; the sundial and the gate tower carry no compass.
- F8 (2, the caller has nothing to do after the book): answered; the caller's play after the book is the watching, the bells and the throws, which is the level's other half and no objective.
- F9 (1): fixed; the note says why the crank hangs on the sundial. F14 (1): fixed in the bell book. F11 (1): fixed in the hub's goal. F10, F12, F13 (1): left.

### Round 2 — verdict `build`

| Question | Findings | Worst severity |
|---|---|---|
| Q1 | 3 | 2 |
| Q2 | 1 | 1 |
| Q3 | 0 | — |
| Q4 | 1 | 1 |
| Q5 | 4 | 1 |
| Q6 | 1 | 1 |
| Q7 | 1 | 2 |
| Q8 | 0 | — |
| Q9 | 1 | 1 |
| Q10 | 3 | 2 |

No finding at 3 or 4; the loop stops here. Fifteen findings at 1 and 2. Fixed: F11 (Wren's cast during the optional strand carried `unchanged`, which reads as a node that does not exist; she now carries her bark like the other lines). Answered, standing as designed: F1 (the crank inside the maze is the level's reason to run it); F13 and F14 (the ending reads whether anyone crossed the bridge; a party that both ran the lanes, or a runner who answers *Just me tonight* while a friend is still on the tower, has made that choice in play).

### Ways shut by the story, and what tells the player

- The bridge is shut at both ends until the gate is wound (`edge/onto-the-bridge` and `edge/off-the-bridge`): with only the deck end shut, a body walked round through the gate tower onto the bridge before it rose (`DW1011`). Both ends are `told`: a chain post beside each barred end answers a press (*The bridge is chained up from this post*). The great gate is `seen` from the hall.
- The bridge cutscene stands its camera on the deck looking along the bridge (a styled shot from the bridge itself was occluded, `DW1033`).

## Step 8 — the first builds

- The build over the stand-ins exited 3 on refusals the stand-ins themselves raise (a body on the stand-in gate top jumps onto the shut bridge, `DW0921`; stations placed by the stand-in inside a wave's reach, `DW0478`); they cleared as the places were detailed. Step 9 began on that tree.
- The site is ringed by a low brick garden wall two courses high (`volumes[]`, massif), the wall the reference views show round the lawn.

## Step 9 — detail

Wave bound as `allocation --all` printed it: `concurrency: 5 = min(6, max(1, 10 / 2))`; at most five authors were in flight. Handouts are regenerable files under `.out/handouts/<place>/handout-<n>.md`.

| place | attempt | tokens | duration | repaired | commit exit |
|---|---|---|---|---|---|
| node/meadow | 1 | 136363 | 208 s | — | 3 (battery: `DW0921` on the stand-in bridge) |
| node/bridge | 1 | 172974 | 531 s | — | 3 (battery: `DW0921`) |
| node/gatehouse | 1 | 194004 | 599 s | — | 3 (battery: `DW0478`, stand-in stations) |
| node/gate-top | 1 | 114653 | 263 s | — | 3 (battery: `DW0986`) |
| node/lookout | 1 | 177001 | 699 s | — | 3 (`DW0838`, `DW0986`) |
| node/maze | 1 | 229209 | 814 s | — | 3 (battery: `DW0986`) |
| node/gate-top | 2 | 133613 | 240 s | `DW0986` | 3 (battery: `DW0838` at the lookout) |
| node/lookout | 2 | 93205 | 194 s | `DW0838` | 3 (battery: `DW0322`) |

The maze's generator printed: 784 cells; 80 dead ends before braiding, 13 after, the nearest kept one 26.7 blocks from the well; 67 independent loops, 5 of them with every pair of opposite points more than 16 blocks apart; 142 blocks of route from the heart to the sundial and 211 from the sundial to the gate tower's door; about 45 % of lane columns within 16 blocks of each quarter's bell.
